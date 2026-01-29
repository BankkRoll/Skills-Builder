# Using build policies and more

# Using build policies

> Apply policies to builds and develop policies iteratively

# Using build policies

   Table of contents

---

Build policies validate inputs before builds execute. This guide covers how to
develop policies iteratively and apply them to real builds with `docker buildx build` and `docker buildx bake`.

## Prerequisites

- Buildx 0.31.0 or later - Check your version: `docker buildx version`
- BuildKit 0.26.0 or later - Verify with: `docker buildx inspect --bootstrap`

If you're using Docker Desktop, ensure you're on a version that includes these
updates.

## Policy development workflow

Buildx automatically loads policies that match your Dockerfile name. When you
build with `Dockerfile`, Buildx looks for `Dockerfile.rego` in the same
directory. For a file named `app.Dockerfile`, it looks for
`app.Dockerfile.rego`. See the [Advanced: Policy configuration](#advanced-policy-configuration)
section for configuration options and manual policy loading.

Writing policies is an iterative process:

1. Start with a basic deny-all policy.
2. Build with debug logging to see what inputs your Dockerfile uses.
3. Add rules to allow specific sources based on the debug output.
4. Test and refine.

### Viewing inputs from your Dockerfile

To see the inputs that your Dockerfile references (images, Git repos, HTTP
downloads), build with debug logging:

```console
$ docker buildx build --progress=plain --policy log-level=debug .
```

Example output for an image source:

```text
#1 0.010 checking policy for source docker-image://alpine:3.19 (linux/arm64)
#1 0.011 policy input: {
#1 0.011   "env": {
#1 0.011     "filename": "."
#1 0.011   },
#1 0.011   "image": {
#1 0.011     "ref": "docker.io/library/alpine:3.19",
#1 0.011     "host": "docker.io",
#1 0.011     "repo": "alpine",
#1 0.011     "tag": "3.19",
#1 0.011     "platform": "linux/arm64"
#1 0.011   }
#1 0.011 }
#1 0.011 unknowns for policy evaluation: [input.image.checksum input.image.labels ...]
#1 0.012 policy decision for source docker-image://alpine:3.19: ALLOW
```

This shows the complete input structure, which fields are unresolved, and the
policy decision for each source. See [Input reference](https://docs.docker.com/build/policies/inputs/) for all
available fields.

### Testing policies with policy eval

Use
[docker buildx policy eval](https://docs.docker.com/reference/cli/docker/buildx/policy/eval/) to
test whether your policy allows a specific source without running a full build.

Note: `docker buildx policy eval` tests the source specified as the argument.
It doesn't parse your Dockerfile to evaluate all inputs - for that, [build with
--progress=plain](#viewing-inputs-from-your-dockerfile).

Test if your policy allows the local context:

```console
$ docker buildx policy eval .
```

No output means the policy allowed the source. If denied, you see:

```console
ERROR: policy denied
```

Test other sources:

```console
$ docker buildx policy eval https://example.com              # Test HTTP
$ docker buildx policy eval https://github.com/org/repo.git  # Test Git
```

By default, `--print` shows reference information parsed from the source string
(like `repo`, `tag`, `host`) without fetching from registries. To inspect
metadata that requires fetching the source (like `labels`, `checksum`, or
`hasProvenance`), specify which fields to fetch with `--fields`:

```console
$ docker buildx policy eval --print --fields image.labels docker-image://alpine:3.19
```

Multiple fields can be specified as a comma-separated list.

### Iterative development example

Here's a practical workflow for developing policies:

1. Start with basic deny-all policy:
  Dockerfile.rego
  ```rego
  package docker
  default allow := false
  allow if input.local
  decision := {"allow": allow}
  ```
2. Build with debug logging to see what inputs your Dockerfile uses:
  ```console
  $ docker buildx build --progress=plain --policy log-level=debug .
  ```
  The output shows the denied image and its input structure:
  ```text
  #1 0.026 checking policy for source docker-image://docker.io/library/alpine:3.19
  #1 0.027 policy input: {
  #1 0.027   "image": {
  #1 0.027     "repo": "alpine",
  #1 0.027     "tag": "3.19",
  #1 0.027     ...
  #1 0.027   }
  #1 0.027 }
  #1 0.028 policy decision for source docker-image://alpine:3.19: DENY
  #1 ERROR: source "docker-image://alpine:3.19" not allowed by policy
  ```
3. Add a rule allowing the alpine image:
  ```rego
  allow if {
      input.image.repo == "alpine"
  }
  ```
4. Build again to verify the policy works:
  ```console
  $ docker buildx build .
  ```

If it fails, see [Debugging](https://docs.docker.com/build/policies/debugging/) for troubleshooting guidance.

## Using policies withdocker build

Once you've developed and tested your policy, apply it to real builds.

### Basic usage

Create a policy alongside your Dockerfile:

Dockerfile

```dockerfile
FROM alpine:3.19
RUN echo "hello"
```

Dockerfile.rego

```rego
package docker

default allow := false

allow if input.local

allow if {
    input.image.repo == "alpine"
}

decision := {"allow": allow}
```

Build normally:

```console
$ docker buildx build .
```

Buildx loads the policy automatically and validates the `alpine:3.19` image
before building.

### Build with different Dockerfile names

Specify the Dockerfile with `-f`:

```console
$ docker buildx build -f app.Dockerfile .
```

Buildx looks for `app.Dockerfile.rego` in the same directory.

### Build with manual policy

Add an extra policy to the automatic one:

```console
$ docker buildx build --policy filename=extra-checks.rego .
```

Both `Dockerfile.rego` (automatic) and `extra-checks.rego` (manual) must pass.

### Build without automatic policy

Use only your specified policy:

```console
$ docker buildx build --policy reset=true,filename=strict.rego .
```

## Using policies with bake

[Bake](https://docs.docker.com/build/bake/) supports automatic policy loading just like `docker buildx build`. Place `Dockerfile.rego` alongside your Dockerfile and run:

```console
$ docker buildx bake
```

### Manual policy in bake files

Specify additional policies in your `docker-bake.hcl`:

docker-bake.hcl

```hcl
target "default" {
  dockerfile = "Dockerfile"
  policy = ["extra.rego"]
}
```

The `policy` attribute takes a list of policy files. Bake loads these in
addition to the automatic `Dockerfile.rego` (if it exists).

### Multiple policies in bake

docker-bake.hcl

```hcl
target "webapp" {
  dockerfile = "Dockerfile"
  policy = [
    "shared/base-policy.rego",
    "security/image-signing.rego"
  ]
}
```

All policies must pass for the target to build successfully.

### Different policies per target

Apply different validation rules to different targets:

docker-bake.hcl

```hcl
target "development" {
  dockerfile = "dev.Dockerfile"
  policy = ["policies/permissive.rego"]
}

target "production" {
  dockerfile = "prod.Dockerfile"
  policy = ["policies/strict.rego", "policies/signing-required.rego"]
}
```

Build with the appropriate target:

```console
$ docker buildx bake development  # Uses permissive policy
$ docker buildx bake production   # Uses strict policies
```

### Bake with policy options

Currently, bake doesn't support policy options (reset, strict, disabled) in the
HCL file. Use command-line flags instead:

```console
$ docker buildx bake --policy disabled=true production
```

## Testing in CI/CD

Validate policies in continuous integration by running builds with the `--policy` flag. For unit testing policies before running builds, see [Test build policies](https://docs.docker.com/build/policies/testing/).

Test policies during CI builds:

.github/workflows/test-policies.yml

```yaml
name: Test Build Policies
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - name: Test build with policy
        run: docker buildx build --policy strict=true .
```

This ensures policy changes don't break builds and that new rules work as
intended. The `strict=true` flag fails the build if policies aren't loaded (for
example, if the BuildKit instance used by the build is too old and doesn't
support policies).

## Advanced: Policy configuration

This section covers advanced policy loading mechanisms and configuration
options.

### Automatic policy loading

Buildx automatically loads policies that match your Dockerfile name. When you
build with `Dockerfile`, Buildx looks for `Dockerfile.rego` in the same
directory. For a file named `app.Dockerfile`, it looks for
`app.Dockerfile.rego`.

```text
project/
├── Dockerfile
├── Dockerfile.rego          # Loaded automatically for Dockerfile
├── app.Dockerfile
├── app.Dockerfile.rego      # Loaded automatically for app.Dockerfile
└── src/
```

This automatic loading means you don't need command-line flags in most cases.
Create the policy file alongside your Dockerfile and build:

```console
$ docker buildx build .
```

Buildx detects `Dockerfile.rego` and evaluates it before running the build.

> Note
>
> Policy files must be in the same directory as the Dockerfile they validate.
> Buildx doesn't search parent directories or subdirectories.

### When policies don't load

If buildx can't find a matching `.rego` file, the build proceeds without policy
evaluation. To require policies and fail if none are found, use strict mode:

```console
$ docker buildx build --policy strict=true .
```

This fails the build if no policy loads or if the BuildKit daemon doesn't
support policies.

### Manual policy configuration

The `--policy` flag lets you specify additional policies, override automatic
loading, or control policy behavior.

Basic syntax:

```console
$ docker buildx build --policy filename=custom.rego .
```

This loads `custom.rego` in addition to the automatic `Dockerfile.rego` (if it
exists).

Multiple policies:

```console
$ docker buildx build --policy filename=policy1.rego --policy filename=policy2.rego .
```

All policies must pass for the build to succeed. Use this to enforce layered
requirements (base policy + project-specific rules).

Available options:

| Option | Description | Example |
| --- | --- | --- |
| filename=<path> | Load policy from specified file | filename=custom.rego |
| reset=true | Ignore automatic policies, use only specified ones | reset=true |
| disabled=true | Disable all policy evaluation | disabled=true |
| strict=true | Fail if BuildKit doesn't support policies | strict=true |
| log-level=<level> | Control policy logging (error, warn, info, debug, none). Usedebugto see complete input JSON and unresolved fields | log-level=debug |

Combine options with commas:

```console
$ docker buildx build --policy filename=extra.rego,strict=true .
```

### Exploring sources with policy eval

The `docker buildx policy eval` command lets you quickly explore and test
sources without running a build.

#### Inspect input structure with --print

Use `--print` to see the input structure for any source without running policy
evaluation:

```console
$ docker buildx policy eval --print https://github.com/moby/buildkit.git
```

```json
{
  "git": {
    "schema": "https",
    "host": "github.com",
    "remote": "https://github.com/moby/buildkit.git"
  }
}
```

Test different source types:

```console
# HTTP downloads
$ docker buildx policy eval --print https://releases.hashicorp.com/terraform/1.5.0/terraform.zip

# Images (requires docker-image:// prefix)
$ docker buildx policy eval --print docker-image://alpine:3.19

# Local context
$ docker buildx policy eval --print .
```

Shows information parsed from the source without fetching. Use `--fields` to
fetch specific metadata (see [above](#testing-policies-with-policy-eval)).

#### Test with specific policy files

The `--filename` flag specifies which policy file to load by providing the base
Dockerfile name (without the `.rego` extension). This is useful for testing
sources against policies associated with different Dockerfiles.

For example, to test a source against the policy for `app.Dockerfile`:

```console
$ docker buildx policy eval --filename app.Dockerfile .
```

This loads `app.Dockerfile.rego` and tests whether it allows the source `.`
(the local directory). The flag defaults to `Dockerfile` if not specified.

Test different sources against your policy:

```console
$ docker buildx policy eval --filename app.Dockerfile https://github.com/org/repo.git
$ docker buildx policy eval --filename app.Dockerfile docker-image://alpine:3.19
```

### Reset automatic loading

To use only your specified policies and ignore automatic `.rego` files:

```console
$ docker buildx build --policy reset=true,filename=custom.rego .
```

This skips `Dockerfile.rego` and loads only `custom.rego`.

### Disable policies temporarily

Disable policy evaluation for testing or emergencies:

```console
$ docker buildx build --policy disabled=true .
```

The build proceeds without any policy checks. Use this carefully - you're
bypassing security controls.

## Next steps

- Write unit tests for your policies: [Test build policies](https://docs.docker.com/build/policies/testing/)
- Debug policy failures: [Debugging](https://docs.docker.com/build/policies/debugging/)
- Browse working examples: [Example policies](https://docs.docker.com/build/policies/examples/)
- Reference all input fields: [Input reference](https://docs.docker.com/build/policies/inputs/)

---

# Validating Git repositories

> Write policies to validate Git repositories used in your builds

# Validating Git repositories

   Table of contents

---

Git repositories often appear in Docker builds as source code inputs. The `ADD`
instruction can clone repositories, and build contexts can reference Git URLs.
Validating these inputs ensures you're building from trusted sources with
verified versions.

This guide teaches you to write policies that validate Git inputs, from basic
version pinning to verifying signed commits and tags.

## Prerequisites

You should understand the policy basics from the [Introduction](https://docs.docker.com/build/policies/intro/):
creating policy files, basic Rego syntax, and how policies evaluate during
builds.

## What are Git inputs?

Git inputs come from `ADD` instructions that reference Git repositories:

```dockerfile
# Clone a specific tag
ADD https://github.com/moby/buildkit.git#v0.26.1 /buildkit

# Clone a branch
ADD https://github.com/user/repo.git#main /src

# Clone a commit
ADD https://github.com/user/repo.git#abcde123 /src
```

The build context can also be a Git repository when you build with:

```console
$ docker build https://github.com/user/repo.git#main
```

Each Git reference triggers a policy evaluation. Your policy can inspect
repository URLs, validate versions, check commit metadata, and verify
signatures.

## Match specific repositories

The simplest Git policy restricts which repositories can be used:

Dockerfile.rego

```rego
package docker

default allow := false

allow if input.local

allow if {
  input.git.host == "github.com"
  input.git.remote == "https://github.com/moby/buildkit.git"
}

decision := {"allow": allow}
```

This policy:

- Denies all inputs by default
- Allows local build context
- Allows only the BuildKit repository from GitHub

The `host` field contains the Git server hostname, and `remote` contains the
full repository URL. Test it:

Dockerfile

```dockerfile
FROM scratch
ADD https://github.com/moby/buildkit.git#v0.26.1 /
```

```console
$ docker build .
```

The build succeeds. Try a different repository and it fails.

You can match multiple repositories with additional rules:

```rego
allow if {
  input.git.host == "github.com"
  input.git.remote == "https://github.com/moby/buildkit.git"
}

allow if {
  input.git.host == "github.com"
  input.git.remote == "https://github.com/docker/cli.git"
}

decision := {"allow": allow}
```

## Pin to specific versions

Tags and branches can change over time. Pin to specific versions to ensure
reproducible builds:

```rego
package docker

default allow := false

allow if input.local

allow if {
  input.git.remote == "https://github.com/moby/buildkit.git"
  input.git.tagName == "v0.26.1"
}

decision := {"allow": allow}
```

The `tagName` field contains the tag name when the Git reference points to a
tag. Use `branch` for branches:

```rego
allow if {
  input.git.remote == "https://github.com/user/repo.git"
  input.git.branch == "main"
}
```

Or use `ref` for any type of reference (branch, tag, or commit SHA):

```rego
allow if {
  input.git.ref == "v0.26.1"
}
```

## Use version allowlists

For repositories you trust but want to control versions, maintain an allowlist:

```rego
package docker

default allow := false

allowed_versions = [
    {"tag": "v0.26.1", "annotated": true, "sha": "abc123"},
]

is_buildkit if {
    input.git.remote == "https://github.com/moby/buildkit.git"
}

allow if {
    not is_buildkit
}

allow if {
    is_buildkit
    some version in allowed_versions
    input.git.tagName == version.tag
    input.git.isAnnotatedTag == version.annotated
    startswith(input.git.commitChecksum, version.sha)
}

decision := {"allow": allow}
```

This policy:

- Defines an allowlist of approved versions with metadata
- Uses a helper rule (`is_buildkit`) for readability
- Allows all non-BuildKit inputs
- For BuildKit, checks the tag name, whether it's an annotated tag, and the commit SHA against the allowlist

The helper rule makes complex policies more maintainable. You can expand the
allowlist as new versions are approved:

```rego
allowed_versions = [
    {"tag": "v0.26.1", "annotated": true, "sha": "abc123"},
    {"tag": "v0.27.0", "annotated": true, "sha": "def456"},
    {"tag": "v0.27.1", "annotated": true, "sha": "789abc"},
]
```

## Validate with regex patterns

Use pattern matching for semantic versioning:

```rego
package docker

default allow := false

allow if input.local

allow if {
  input.git.remote == "https://github.com/moby/buildkit.git"
  regex.match(`^v[0-9]+\.[0-9]+\.[0-9]+$`, input.git.tagName)
}

decision := {"allow": allow}
```

This allows any BuildKit tag matching the pattern `vX.Y.Z` where X, Y, and Z
are numbers. The regex ensures you're using release versions, not pre-release
tags like `v0.26.0-rc1`.

Match major versions:

```rego
# Only allow v0.x releases
allow if {
  input.git.remote == "https://github.com/moby/buildkit.git"
  regex.match(`^v0\.[0-9]+\.[0-9]+$`, input.git.tagName)
}
```

## Inspect commit metadata

The `commit` object provides detailed information about commits:

```rego
package docker

default allow := false

allow if input.local

# Check commit author
allow if {
  input.git.remote == "https://github.com/user/repo.git"
  input.git.commit.author.email == "trusted@example.com"
}

decision := {"allow": allow}
```

The `commit` object includes:

- `author.name`: Author's name
- `author.email`: Author's email
- `author.when`: When the commit was authored
- `committer.name`: Committer's name
- `committer.email`: Committer's email
- `committer.when`: When the commit was committed
- `message`: Commit message

Validate commit messages:

```rego
allow if {
  input.git.commit
  contains(input.git.commit.message, "Signed-off-by:")
}
```

Pin to specific commit SHA:

```rego
allow if {
  input.git.commitChecksum == "abc123def456..."
}
```

## Require signed commits

GPG-signed commits prove authenticity. Check for commit signatures:

```rego
package docker

default allow := false

allow if input.local

allow if {
  input.git.remote == "https://github.com/moby/buildkit.git"
  input.git.commit.pgpSignature != null
}

decision := {"allow": allow}
```

The `pgpSignature` field is `null` for unsigned commits. For signed commits, it
contains signature details.

SSH signatures work similarly:

```rego
allow if {
  input.git.commit.sshSignature != null
}
```

## Require signed tags

Annotated tags can be signed, providing a cryptographic guarantee of the
release:

```rego
package docker

default allow := false

allow if input.local

allow if {
  input.git.remote == "https://github.com/moby/buildkit.git"
  input.git.tag.pgpSignature != null
}

decision := {"allow": allow}
```

The `tag` object is only available for annotated tags. It includes:

- `tagger.name`: Who created the tag
- `tagger.email`: Tagger's email
- `tagger.when`: When the tag was created
- `message`: Tag message
- `pgpSignature`: GPP signature (if signed)
- `sshSignature`: SSH signature (if signed)

Lightweight tags don't have a `tag` object, so this policy effectively requires
annotated, signed tags.

## Verify signatures with public keys

Use the `verify_git_signature()` function to cryptographically verify Git
signatures against trusted public keys:

```rego
package docker

default allow := false

allow if input.local

allow if {
  input.git.remote == "https://github.com/moby/buildkit.git"
  input.git.tagName != ""
  verify_git_signature(input.git.tag, "keys.asc")
}

decision := {"allow": allow}
```

This verifies that Git tags are signed by keys in the `keys.asc` public
key file. To set this up:

1. Export maintainer public keys:
  ```console
  $ curl https://github.com/user.gpg > keys.asc
  ```
2. Place `keys.asc` alongside your policy file

The function verifies PGP signatures on commits or tags. See [Built-in
functions](https://docs.docker.com/build/policies/built-ins/) for more details.

## Apply conditional rules

Use different rules for different contexts. Allow unsigned refs during
development but require signing for production:

```rego
package docker

default allow := false

allow if input.local

is_buildkit if {
    input.git.remote == "https://github.com/moby/buildkit.git"
}

is_version_tag if {
    is_buildkit
    regex.match(`^v[0-9]+\.[0-9]+\.[0-9]+$`, input.git.tagName)
}

# Version tags must be signed
allow if {
    is_version_tag
    input.git.tagName != ""
    verify_git_signature(input.git.tag, "keys.asc")
}

# Non-version refs allowed in development
allow if {
    is_buildkit
    not is_version_tag
    input.env.target != "release"
}

decision := {"allow": allow}
```

This policy:

- Defines helper rules for readability
- Requires signed version tags from maintainers
- Allows unsigned refs (branches, commits) unless building the release target
- Uses `input.env.target` to detect the build target

Build a development target without signatures:

```console
$ docker buildx build --target=dev .
```

Build the release target, and signing is enforced:

```console
$ docker buildx build --target=release .
```

## Next steps

You now understand how to validate Git repositories in build policies. To
continue learning:

- Browse [Example policies](https://docs.docker.com/build/policies/examples/) for complete policy patterns
- Read [Built-in functions](https://docs.docker.com/build/policies/built-ins/) for Git signature verification
  functions
- Check the [Input reference](https://docs.docker.com/build/policies/inputs/) for all available Git fields

---

# Validating image inputs

> Write policies to validate container images used in your builds

# Validating image inputs

   Table of contents

---

Container images are the most common build inputs. Every `FROM` instruction
pulls an image, and `COPY --from` references pull additional images. Validating
these images protects your build supply chain from compromised registries,
unexpected updates, and unauthorized base images.

This guide teaches you to write policies that validate image inputs,
progressing from basic allowlisting to advanced attestation checks.

## Prerequisites

You should understand the policy basics from the [Introduction](https://docs.docker.com/build/policies/intro/):
creating policy files, basic Rego syntax, and how policies evaluate during
builds.

## What are image inputs?

Image inputs come from two Dockerfile instructions:

```dockerfile
# FROM instructions
FROM alpine:3.22
FROM golang:1.25-alpine AS builder

# COPY --from references
COPY --from=builder /app /app
COPY --from=nginx:latest /etc/nginx/nginx.conf /nginx.conf
```

Each of these references triggers a policy evaluation. Your policy can inspect
image metadata, verify attestations, and enforce constraints before the build
proceeds.

## Allowlist specific repositories

The simplest image policy restricts which repositories can be used. This
prevents developers from using arbitrary images that haven't been vetted.

Create a policy that only allows Alpine:

Dockerfile.rego

```rego
package docker

default allow := false

allow if input.local

allow if {
  input.image.repo == "alpine"
}

decision := {"allow": allow}
```

This policy:

- Denies all inputs by default
- Allows local build context
- Allows any image from the `alpine` repository (any tag or digest)

Test it with a Dockerfile:

Dockerfile

```dockerfile
FROM alpine
RUN echo "hello"
```

```console
$ docker build .
```

The build succeeds. Try changing to `FROM ubuntu`:

```console
$ docker build .
```

The build fails because `ubuntu` doesn't match the allowed repository.

## Compare semantic versions

Restrict images to specific version ranges using Rego's `semver` functions:

```rego
package docker

default allow := false

allow if input.local

# Allow Go 1.21 or newer
allow if {
  input.image.repo == "golang"
  semver.is_valid(input.image.tag)
  semver.compare(input.image.tag, "1.21.0") >= 0
}

decision := {"allow": allow}
```

The `semver.compare(a, b)` function compares semantic versions and returns:

- `-1` if version `a` is less than `b`
- `0` if versions are equal
- `1` if version `a` is greater than `b`

Use `semver.is_valid()` to check if a tag is a valid semantic version before
comparing.

Restrict to specific version ranges:

```rego
allow if {
  input.image.repo == "node"
  version := input.image.tag
  semver.is_valid(version)
  semver.compare(version, "20.0.0") >= 0  # 20.0.0 or newer
  semver.compare(version, "21.0.0") < 0   # older than 21.0.0
}
```

This allows only Node.js 20.x versions. The pattern works for any image using
semantic versioning.

These `semver` functions are standard Rego built-ins documented in the [OPA
policy
reference](https://www.openpolicyagent.org/docs/latest/policy-reference/#semver).

## Require digest references

Tags like `alpine:3.22` can change - someone could push a new image with the
same tag. Digests like `alpine@sha256:abc123...` are immutable.

### Requiring users to provide digests

You can require that users always specify digests in their Dockerfiles:

```rego
package docker

default allow := false

allow if input.local

allow if {
  input.image.isCanonical
}

decision := {"allow": allow}
```

The `isCanonical` field is `true` when the user's reference includes a digest.
This policy would allow:

```dockerfile
FROM alpine@sha256:4b7ce07002c69e8f3d704a9c5d6fd3053be500b7f1c69fc0d80990c2ad8dd412
```

But reject tag-only references like `FROM alpine:3.22`.

### Pinning to specific digests

Alternatively (or additionally), you can validate that an image's actual digest
matches a specific value, regardless of how the user wrote the reference:

```rego
allow if {
  input.image.repo == "alpine"
  input.image.checksum == "sha256:4b7ce07002c69e8f3d704a9c5d6fd3053be500b7f1c69fc0d80990c2ad8dd412"
}

decision := {"allow": allow}
```

This checks the actual content digest of the pulled image. It would allow both:

```dockerfile
FROM alpine:3.22
FROM alpine@sha256:4b7ce...
```

As long as the resolved image has the specified digest. This is useful for
pinning critical base images to known-good versions.

## Restrict registries

Control which registries your builds can pull from. This helps enforce
corporate policies or restrict to trusted sources.

```rego
package docker

default allow := false

allow if input.local

# Allow Docker Hub images
allow if {
  input.image.host == "docker.io"  # Docker Hub
  input.image.repo == "alpine"
}

# Allow images from internal registry
allow if {
  input.image.host == "registry.company.com"
}

decision := {"allow": allow}
```

The `host` field contains the registry hostname. Docker Hub images use
`"docker.io"` as the host value. Test with:

```dockerfile
FROM alpine                                    # Allowed (Docker Hub)
FROM registry.company.com/myapp:latest         # Allowed (company registry)
FROM ghcr.io/someorg/image:latest              # Denied (wrong registry)
```

Use `fullRepo` when you need the complete path including registry:

```rego
allow if {
  input.image.fullRepo == "docker.io/library/alpine"
}
```

## Validate platform constraints

Multi-architecture images support different operating systems and CPU
architectures. You can restrict builds to specific platforms:

```rego
package docker

default allow := false

allow if input.local

allow if {
  input.image.os == "linux"
  input.image.arch in ["amd64", "arm64"]
}

decision := {"allow": allow}
```

This policy:

- Defines supported architectures in a list
- Checks `input.image.os` matches Linux
- Verifies `input.image.arch` is in the supported list

The `os` and `arch` fields come from the image manifest, reflecting the actual
image platform. This works with Docker's automatic platform selection -
policies validate what Buildx resolves, not what you specify.

## Inspect image metadata

Images contain metadata like environment variables, labels, and working
directories. You can validate these to ensure images meet requirements.

Check for specific environment variables:

```rego
package docker

default allow := false

allow if input.local

allow if {
  input.image.repo == "golang"
  input.image.workingDir == "/go"
  some ver in input.image.env
  startswith(ver, "GOLANG_VERSION=")
  some toolchain in input.image.env
  toolchain == "GOTOOLCHAIN=local"
}

decision := {"allow": allow}
```

This policy validates the official Go image by checking:

- The working directory is `/go`
- The environment has `GOLANG_VERSION` set
- The environment includes `GOTOOLCHAIN=local`

The `input.image.env` field is an array of strings in `KEY=VALUE` format.
Use Rego's `some` iteration to search the array.

Check image labels:

```rego
allow if {
  input.image.labels["org.opencontainers.image.vendor"] == "Example Corp"
  input.image.labels["org.opencontainers.image.version"] != ""
}
```

The `labels` field is a map, so you access values with bracket notation.

## Require attestations and provenance

Modern images include
[attestations](https://docs.docker.com/build/metadata/attestations/):
machine-readable metadata about how the image was built.
[Provenance](https://docs.docker.com/build/metadata/attestations/slsa-provenance/) attestations
describe the build process, and
[SBOMs](https://docs.docker.com/build/metadata/attestations/sbom/)
list the software inside.

Require provenance:

```rego
package docker

default allow := false

allow if input.local

allow if {
  input.image.hasProvenance
}

decision := {"allow": allow}
```

The `hasProvenance` field is `true` when the image has provenance or SBOM
[attestations](https://docs.docker.com/build/metadata/attestations/).

## Verify GitHub Actions signatures

For images built with GitHub Actions, verify they came from trusted workflows by
inspecting signature metadata:

```rego
allow if {
  input.image.repo == "myapp"
  input.image.hasProvenance
  some sig in input.image.signatures
  valid_github_signature(sig)
}

# Helper to validate GitHub Actions signature
valid_github_signature(sig) if {
  sig.signer.certificateIssuer == "CN=sigstore-intermediate,O=sigstore.dev"
  sig.signer.issuer == "https://token.actions.githubusercontent.com"
  startswith(sig.signer.buildSignerURI, "https://github.com/myorg/")
  sig.signer.runnerEnvironment == "github-hosted"
}

decision := {"allow": allow}
```

This pattern works with any GitHub Actions workflow using Sigstore keyless
signing. The signature metadata provides cryptographic proof of the build's
origin. For complete signature verification examples, see [Example
policies](https://docs.docker.com/build/policies/examples/).

## Combine multiple checks

Real policies often combine several checks. Multiple conditions in one `allow`
rule means AND - all must be true:

```rego
package docker

default allow := false

allow if input.local

# Production images need everything
allow if {
  input.image.repo == "alpine"
  input.image.isCanonical
  input.image.hasProvenance
}

decision := {"allow": allow}
```

Multiple `allow` rules means OR - any rule can match:

```rego
package docker

default allow := false

allow if input.local

# Allow Alpine with strict checks
allow if {
  input.image.repo == "alpine"
  input.image.isCanonical
}

# Allow Go with different checks
allow if {
  input.image.repo == "golang"
  input.image.workingDir == "/go"
}

decision := {"allow": allow}
```

Use this pattern to apply different requirements to different base images.

## Next steps

You now understand how to validate container images in build policies. To
continue learning:

- Learn [Git repository validation](https://docs.docker.com/build/policies/validate-git/) for source code inputs
- Browse [Example policies](https://docs.docker.com/build/policies/examples/) for complete policy patterns
- Read [Built-in functions](https://docs.docker.com/build/policies/built-ins/) for signature verification and
  attestation checking
- Check the [Input reference](https://docs.docker.com/build/policies/inputs/) for all available image fields

---

# Validating build inputs with policies

> Secure your Docker builds by validating images, Git repositories, and dependencies with build policies

# Validating build inputs with policies

   Table of contents

---

Building with Docker often involves downloading remote resources. These
external dependencies, such as Docker images, Git repositories, remote files,
and other artifacts, are called build inputs.

For example:

- Pulling images from a registry
- Cloning a source code repository
- Fetching files from a server over HTTPS

When consuming build inputs, it's a good idea to verify the contents are what
you expect them to be. One way to do this is to use the `--checksum` option for
the `ADD` Dockerfile instruction. This lets you verify the SHA256 checksum of a
remote resource when pulling it into a build:

```dockerfile
ADD --checksum=sha256:c0ff3312345… https://example.com/archive.tar.gz /
```

If the remote `archive.tar.gz` file does not match the checksum that the
Dockerfile expects, the build fails.

Checksums verify that content matches what you expect, but only for the `ADD`
instruction. They don't tell you anything about where the content came from or
how it was produced. You can't use checksums to enforce constraints like
"images must be signed" or "dependencies must come from approved sources."

Build policies solve this problem. They let you define rules that validate all
your build inputs, enforcing requirements like provenance attestations,
approved registries, and signed Git tags across your entire build process.

## Prerequisites

Build policies is currently an experimental feature. To try it out, you'll
need:

- Buildx 0.31.0 or later - Check your version: `docker buildx version`
- BuildKit 0.27.0 or later - Verify with: `docker buildx inspect --bootstrap`

If you're using Docker Desktop, ensure you're on a version that includes these
updates.

## Build policies

Buildx version 0.31.0 added support for build policies. Build policies are
rules for securing your Docker build supply chain, and help protect against
upstream compromises, malicious dependencies, and unauthorized modifications to
your build inputs.

Build policies let you enforce extended verifications on inputs used to build
your projects, such as:

- Docker images must use digest references (not tags alone)
- Images must have provenance attestations and cosign signatures
- Git tags are signed by maintainers with a PGP public key
- All remote artifacts must use HTTPS and include a checksum for verification

Build policies are defined in a declarative policy language, called Rego,
created for the [Open Policy Agent (OPA)](https://www.openpolicyagent.org/).
The following example shows a minimal build policy in Rego.

Dockerfile.rego

```rego
package docker

default allow := false

# Allow any local inputs for this build
# For example: a local build context, or a local Dockerfile
allow if input.local

# Allow images, but only if they have provenance attestations
allow if {
    input.image.hasProvenance
}

decision := {"allow": allow}
```

If the Dockerfile associated with this policy references an image with no
provenance attestation in a `FROM` instruction, the policy would be violated
and the build would fail.

## How policies work

When you run `docker buildx build`, Buildx:

1. Resolves all build inputs (images, Git repos, HTTP downloads)
2. Looks for a policy file matching your Dockerfile name (e.g.,
  `Dockerfile.rego`)
3. Evaluates each input against the policy before the build starts
4. Allows the build to proceed only if all inputs pass the policy

Policies are written in Rego (Open Policy Agent's policy language). You don't
need to be a Rego expert - the [Introduction](https://docs.docker.com/build/policies/intro/) tutorial teaches you
everything needed.

Policy files live alongside your Dockerfile:

```text
project/
├── Dockerfile
├── Dockerfile.rego
└── src/
```

No additional configuration is needed - Buildx automatically finds and loads
the policy when you build.

## Use cases

Build policies help you enforce security and compliance requirements on your
Docker builds. Common scenarios where policies provide value:

### Enforce base image standards

Require all production Dockerfiles to use specific, approved base images with
digest references. Prevent developers from using arbitrary images that haven't
been vetted by your security team.

### Validate third-party dependencies

When your build downloads files, libraries, or tools from the internet, verify
they come from trusted sources and match expected checksums or signatures. This
protects against supply chain attacks where an upstream dependency is
compromised.

### Ensure signed releases

Require that all dependencies have valid signatures from trusted parties.

- Check GPG signatures for Git repositories you clone in your builds
- Verify provenance attestation signatures with Sigstore

### Meet compliance requirements

Some regulatory frameworks require evidence that you validate your build
inputs. Build policies give you an auditable, declarative way to demonstrate
you're checking dependencies against security standards.

### Separate development and production rules

Apply stricter validation for production builds while allowing more flexibility
during development. The same policy file can contain conditional rules based on
build context or target.

## Get started

Ready to start writing policies? The [Introduction](https://docs.docker.com/build/policies/intro/) tutorial walks
you through creating your first policy and teaches the Rego basics you need.

For practical usage guidance, see [Using build policies](https://docs.docker.com/build/policies/usage/).

For practical examples you can copy and adapt, see the [Example
policies](https://docs.docker.com/build/policies/examples/) library.

---

# Search code, repositories, users, issues, pull requests...

> Docker CLI plugin for extended build capabilities with BuildKit - Releases · docker/buildx

buildx 0.31.1

Welcome to the v0.31.1 release of buildx!

Please try out the release binaries and report any issues at
 [https://github.com/docker/buildx/issues](https://github.com/docker/buildx/issues).

### Contributors

- Tõnis Tiigi

### Notable Changes

- Fix excessive HTTP requests when using `buildx imagetools create` command [#3632](https://github.com/docker/buildx/pull/3632)

### Dependency Changes

This release has no dependency changes

Previous release can be found at [v0.31.0](https://github.com/docker/buildx/releases/tag/v0.31.0)
