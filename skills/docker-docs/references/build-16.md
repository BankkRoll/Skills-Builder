# Policy templates and examples and more

# Policy templates and examples

> Browse policy examples from quick-start configs to production-grade security templates

# Policy templates and examples

   Table of contents

---

This page provides complete, working policy examples you can copy and adapt.
The examples are organized into two sections: getting started policies for
quick adoption, and production templates for comprehensive security.

If you're new to policies, start with the tutorials:
[Introduction](https://docs.docker.com/build/policies/intro/), [Image validation](https://docs.docker.com/build/policies/validate-images/), and [Git
validation](https://docs.docker.com/build/policies/validate-git/). Those pages teach individual techniques. This
page shows complete policies combining those techniques.

## How to use these examples

1. Copy the policy code into a `Dockerfile.rego` file next to your
  Dockerfile
2. Customize any todo comments with your specific values
3. Test by running `docker build .` and verifying the policy works as
  expected
4. Refine based on your team's needs

### Using examples with bake

These policies work with both `docker buildx build` and `docker buildx bake`.
For bake, place the policy alongside your Dockerfile and it loads
automatically. To use additional policies:

```hcl
target "default" {
  dockerfile = "Dockerfile"
  policy = ["extra.rego"]
}
```

See the [Usage guide](https://docs.docker.com/build/policies/usage/) for complete bake integration details.

## Getting started

These policies work immediately with minimal or no customization. Use them to
adopt policies quickly and demonstrate value to your team.

### Development-friendly baseline

A permissive policy that allows typical development workflows while blocking
obvious security issues.

```rego
package docker

default allow := false

allow if input.local
allow if input.git

# Allow common public registries
allow if {
  input.image.host == "docker.io"  # Docker Hub
}

allow if {
  input.image.host == "ghcr.io"  # GitHub Container Registry
}

allow if {
  input.image.host == "dhi.io"  # Docker Hardened Images
}

# Require HTTPS for all downloads
allow if {
  input.http.schema == "https"
}

decision := {"allow": allow}
```

This policy allows local and Git contexts, images from Docker Hub, GitHub
Container Registry, and
[Docker Hardened Images](https://docs.docker.com/dhi/), and `ADD` downloads
over HTTPS. It blocks HTTP downloads and non-standard registries.

When to use: Starting point for teams new to policies. Provides basic security
without disrupting development workflows.

### Registry allowlist

Control which registries your builds can pull images from.

```rego
package docker

default allow := false

allow if input.local

# TODO: Add your internal registry hostname
allowed_registries := ["docker.io", "ghcr.io", "dhi.io", "registry.company.com"]

allow if {
  input.image.host in allowed_registries
}

# Allow mirrored DHI images from Docker Hub (DHI Enterprise users)
# TODO: Replace with your organization namespace
allow if {
  input.image.host == "docker.io"
  startswith(input.image.repo, "myorg/dhi-")
}

deny_msg contains msg if {
  not allow
  input.image
  msg := sprintf("registry %s is not in the allowlist", [input.image.host])
}

decision := {"allow": allow, "deny_msg": deny_msg}
```

This policy restricts image pulls to approved registries. Customize and add
your internal registry to the list. If you have a DHI Enterprise subscription
and have mirrored Docker Hardened Images to Docker Hub, add a rule to allow
images from your organization's namespace.

When to use: Enforce corporate policies about approved image sources. Prevents
developers from using arbitrary public registries.

### Pin base images to digests

Require digest references for reproducible builds.

```rego
package docker

default allow := false

allow if input.local

# Require digest references for all images
allow if {
  input.image.isCanonical
}

deny_msg contains msg if {
  not allow
  input.image
  msg := sprintf("image %s must use digest reference (e.g., @sha256:...)", [input.image.ref])
}

decision := {"allow": allow, "deny_msg": deny_msg}
```

This policy requires images use digest references like
`alpine@sha256:abc123...` instead of tags like `alpine:3.19`. Digests are
immutable - the same digest always resolves to the same image content.

When to use: Ensure build reproducibility. Prevents builds from breaking when
upstream tags are updated. Required for compliance in some environments.

### Control external dependencies

Pin specific versions of dependencies downloaded during builds.

```rego
package docker

default allow := false

allow if input.local

# Allow any image (add restrictions as needed)
allow if input.image

# TODO: Add your allowed Git repositories and tags
allowed_repos := {
  "https://github.com/moby/buildkit.git": ["v0.26.1", "v0.27.0"],
}
# Only allow Git input from allowed_repos
allow if {
  some repo, versions in allowed_repos
  input.git.remote == repo
  input.git.tagName in versions
}

# TODO: Add your allowed downloads
allow if {
  input.http.url == "https://example.com/app-v1.0.tar.gz"
}

decision := {"allow": allow}
```

This policy creates allowlists for external dependencies. Add your Git
repositories with approved version tags, and URLs.

When to use: Control which external dependencies can be used in builds.
Prevents builds from pulling arbitrary versions or unverified downloads.

## Production templates

These templates demonstrate comprehensive security patterns. They require
customization but show best practices for production environments.

### Image attestation and provenance

Require images have provenance attestations from trusted builders.

```rego
package docker

default allow := false

allow if input.local

# TODO: Add your repository names
allowed_repos := ["myorg/backend", "myorg/frontend", "myorg/worker"]

# Production images need full attestations
allow if {
  some repo in allowed_repos
  input.image.repo == repo
  input.image.hasProvenance
  some sig in input.image.signatures
  trusted_github_builder(sig, repo)
}

# Helper to validate GitHub Actions build from main branch
trusted_github_builder(sig, repo) if {
  sig.signer.certificateIssuer == "CN=sigstore-intermediate,O=sigstore.dev"
  sig.signer.issuer == "https://token.actions.githubusercontent.com"
  startswith(sig.signer.buildSignerURI, sprintf("https://github.com/myorg/%s/.github/workflows/", [repo]))
  sig.signer.sourceRepositoryRef == "refs/heads/main"
  sig.signer.runnerEnvironment == "github-hosted"
}

# Allow Docker Hardened Images with built-in attestations
allow if {
  input.image.host == "dhi.io"
  input.image.isCanonical
  input.image.hasProvenance
}

# Allow official base images with digests
allow if {
  input.image.repo == "alpine"
  input.image.host == "docker.io"
  input.image.isCanonical
}

decision := {"allow": allow}
```

This template validates that your application images have provenance
attestations, and were built by GitHub Actions from your main branch. Docker
Hardened Images are allowed when using digests since they include comprehensive
attestations by default. Other base images must use digests.

Customize:

- Replace `allowed_repos` with your image names
- Update the organization name in `trusted_github_builder()`
- Add rules for other base images you use

When to use: Enforce supply chain security for production deployments. Ensures
images are built by trusted CI/CD pipelines with auditable provenance.

### Signed Git releases

Enforce signed tags from trusted maintainers for Git dependencies.

```rego
package docker

default allow := false

allow if input.local

allow if input.image

# TODO: Replace with your repository URL
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
    verify_git_signature(input.git.tag, "maintainers.asc")
}

# Allow unsigned refs for development
allow if {
    is_buildkit
    not is_version_tag
}

decision := {"allow": allow}
```

This template requires production release tags to be signed by trusted
maintainers. Development branches and commits can be unsigned.

Setup:

1. Export maintainer PGP public keys to `maintainers.asc`:
  ```console
  $ gpg --export --armor user1@example.com user2@example.com > maintainers.asc
  ```
2. Place `maintainers.asc` in the same directory as your policy file

Customize:

- Replace the repository URL in `is_buildkit`
- Update the maintainers in the PGP keyring file
- Adjust the version tag regex pattern if needed

When to use: Validate that production dependencies come from signed releases.
Protects against compromised releases or unauthorized updates.

### Multi-registry policy

Apply different validation rules for internal and external registries.

```rego
package docker

default allow := false

allow if input.local

# TODO: Replace with your internal registry hostname
internal_registry := "registry.company.com"

# Internal registry: basic validation
allow if {
  input.image.host == internal_registry
}

# External registries: strict validation
allow if {
  input.image.host != internal_registry
  input.image.host != ""
  input.image.isCanonical
  input.image.hasProvenance
}

# Docker Hub: allowlist specific images
allow if {
  input.image.host == "docker.io"
  # TODO: Add your approved base images
  input.image.repo in ["alpine", "golang", "node"]
  input.image.isCanonical
}

# Docker Hardened Images: trusted by default with built-in attestations
allow if {
  input.image.host == "dhi.io"
  input.image.isCanonical
}

decision := {"allow": allow}
```

This template defines a trust boundary between internal and external image
sources. Internal images require minimal validation, while external images need
digests and provenance. Docker Hardened Images from `dhi.io` are treated as
trusted since they include comprehensive attestations and security guarantees.

Customize:

- Set your internal registry hostname
- Add your approved Docker Hub base images
- Adjust validation requirements based on your security policies

When to use: Organizations with internal registries that need different rules
for internal and external sources. Balances security with practical workflow
needs.

### Multi-environment policy

Apply different rules based on the build target or stage. For example,

```rego
package docker

default allow := false

allow if input.local

# TODO: Define your environment detection logic
is_production if {
  input.env.target == "production"
}

is_development if {
  input.env.target == "development"
}

# Production: strict rules - only digest images with provenance
allow if {
  is_production
  input.image.isCanonical
  input.image.hasProvenance
}

# Development: permissive rules - any image
allow if {
  is_development
  input.image
}

# Staging inherits production rules (default target detection)
allow if {
  not is_production
  not is_development
  input.image.isCanonical
}

decision := {"allow": allow}
```

This template uses build targets to apply different validation levels.
Production requires attestations and digests, development is permissive, and
staging uses moderate rules.

Customize:

- Update environment detection logic (target names, build args, etc.)
- Adjust validation requirements for each environment
- Add more environments as needed

When to use: Teams with separate build configurations for different deployment
stages. Allows flexibility in development while enforcing strict rules for
production.

### Complete dependency pinning

Pin all external dependencies to specific versions across all input types.

```rego
package docker

default allow := false

allow if input.local

# TODO: Add your pinned images with exact digests
# Docker Hub images use docker.io as host
allowed_dockerhub := {
  "alpine": "sha256:4b7ce07002c69e8f3d704a9c5d6fd3053be500b7f1c69fc0d80990c2ad8dd412",
  "golang": "sha256:abc123...",
}

allow if {
  input.image.host == "docker.io"
  some repo, digest in allowed_dockerhub
  input.image.repo == repo
  input.image.checksum == digest
}

# TODO: Add your pinned DHI images
allowed_dhi := {
  "python": "sha256:def456...",
  "node": "sha256:ghi789...",
}

allow if {
  input.image.host == "dhi.io"
  some repo, digest in allowed_dhi
  input.image.repo == repo
  input.image.checksum == digest
}

# TODO: Add your pinned Git dependencies
allowed_git := {
  "https://github.com/moby/buildkit.git": {
    "tag": "v0.26.1",
    "commit": "abc123...",
  },
}

allow if {
  some url, version in allowed_git
  input.git.remote == url
  input.git.tagName == version.tag
  input.git.commitChecksum == version.commit
}

# TODO: Add your pinned HTTP downloads
allowed_downloads := {
  "https://releases.example.com/app-v1.0.tar.gz": "sha256:def456...",
}

allow if {
  some url, checksum in allowed_downloads
  input.http.url == url
  input.http.checksum == checksum
}

decision := {"allow": allow}
```

This template pins every external dependency to exact versions with cryptographic
verification. Images use digests, Git repos use commit SHAs, and downloads use
checksums.

Customize:

- Add all your dependencies with exact versions/checksums
- Maintain this file when updating dependencies
- Consider automating updates through CI/CD

When to use: Maximum reproducibility and security. Ensures builds always use
exact versions of all dependencies. Required for high-security or regulated
environments.

### Manual signature verification

Verify image signatures by inspecting signature metadata fields.

```rego
package docker

default allow := false

allow if input.local

# Require valid GitHub Actions signatures
allow if {
    input.image
    input.image.hasProvenance
    some sig in input.image.signatures
    valid_github_signature(sig)
}

# Helper function to validate GitHub Actions signature
valid_github_signature(sig) if {
    # Sigstore keyless signing
    sig.signer.certificateIssuer == "CN=sigstore-intermediate,O=sigstore.dev"
    sig.signer.issuer == "https://token.actions.githubusercontent.com"

    # TODO: Replace with your organization
    startswith(sig.signer.buildSignerURI, "https://github.com/myorg/.github/workflows/")
    startswith(sig.signer.sourceRepositoryURI, "https://github.com/myorg/")

    # Verify GitHub hosted runner
    sig.signer.runnerEnvironment == "github-hosted"

    # Require timestamp
    count(sig.timestamps) > 0
}

decision := {"allow": allow}
```

This policy validates that images were built by GitHub Actions using Sigstore
keyless signing.

Customize:

- Replace `myorg` with your GitHub organization
- Adjust workflow path restrictions
- Add additional signature field checks as needed

When to use: Enforce that images are built by CI/CD with verifiable signatures,
not manually pushed by developers.

## Next steps

- Write unit tests for your policies: [Test build policies](https://docs.docker.com/build/policies/testing/)
- Review [Built-in functions](https://docs.docker.com/build/policies/built-ins/) for signature verification and
  attestation checking
- Check the [Input reference](https://docs.docker.com/build/policies/inputs/) for all available fields you can
  validate
- Read the tutorials for detailed explanations:
  [Introduction](https://docs.docker.com/build/policies/intro/), [Image validation](https://docs.docker.com/build/policies/validate-images/), [Git
  validation](https://docs.docker.com/build/policies/validate-git/)

---

# Input reference

> Reference documentation for policy input fields

# Input reference

   Table of contents

---

When Buildx evaluates policies, it provides information about build inputs
through the `input` object. The structure of `input` depends on the type of
resource your Dockerfile references.

## Input types

Build inputs correspond to Dockerfile instructions:

| Dockerfile instruction | Input type | Access pattern |
| --- | --- | --- |
| FROM alpine:latest | Image | input.image |
| COPY --from=builder /app /app | Image | input.image |
| ADD https://example.com/file.tar.gz / | HTTP | input.http |
| ADD git@github.com:user/repo.git /src | Git | input.git |
| Build context (.) | Local | input.local |

Each input type has specific fields available for policy evaluation.

## HTTP inputs

HTTP inputs represent files downloaded over HTTP or HTTPS using the `ADD`
instruction.

### Example Dockerfile

```dockerfile
FROM alpine
ADD --checksum=sha256:abc123... https://example.com/app.tar.gz /app.tar.gz
```

### Available fields

#### input.http.url

The complete URL of the resource.

```rego
allow if {
    input.http.url == "https://example.com/app.tar.gz"
}
```

#### input.http.schema

The URL scheme (`http` or `https`).

```rego
# Require HTTPS for all downloads
allow if {
    input.http.schema == "https"
}
```

#### input.http.host

The hostname from the URL.

```rego
# Allow downloads from approved domains
allow if {
    input.http.host == "cdn.example.com"
}
```

#### input.http.path

The path component of the URL.

```rego
allow if {
    startswith(input.http.path, "/releases/")
}
```

#### input.http.checksum

The checksum specified with `ADD --checksum=...`, if present. Empty string if
no checksum was provided.

```rego
# Require checksums for all downloads
allow if {
    input.http.checksum != ""
}
```

#### input.http.hasAuth

Boolean indicating if the request includes authentication (HTTP basic auth or
bearer token).

```rego
# Require authentication for internal servers
allow if {
    input.http.host == "internal.company.com"
    input.http.hasAuth
}
```

## Image inputs

Image inputs represent container images from `FROM` instructions or
`COPY --from` references.

### Example Dockerfile

```dockerfile
FROM alpine:3.19@sha256:abc123...
COPY --from=builder:latest /app /app
```

### Available fields

#### input.image.ref

The complete image reference as written in the Dockerfile.

```rego
allow if {
    input.image.ref == "alpine:3.19@sha256:abc123..."
}
```

#### input.image.host

The registry hostname. Docker Hub images use `"docker.io"`.

```rego
# Only allow Docker Hub images
allow if {
    input.image.host == "docker.io"
}

# Only allow images from GitHub Container Registry
allow if {
    input.image.host == "ghcr.io"
}
```

#### input.image.repo

The repository name without the registry host.

```rego
allow if {
    input.image.repo == "library/alpine"
}
```

#### input.image.fullRepo

The full repository path including registry host.

```rego
allow if {
    input.image.fullRepo == "docker.io/library/alpine"
}
```

#### input.image.tag

The tag portion of the reference. Empty if using a digest reference.

```rego
# Allow only specific tags
allow if {
    input.image.tag == "3.19"
}
```

#### input.image.isCanonical

Boolean indicating if the reference uses a digest (`@sha256:...`).

```rego
# Require digest references
allow if {
    input.image.isCanonical
}
```

#### input.image.checksum

The SHA256 digest of the image manifest.

```rego
allow if {
    input.image.checksum == "sha256:abc123..."
}
```

#### input.image.platform

The target platform for multi-platform images.

```rego
allow if {
    input.image.platform == "linux/amd64"
}
```

#### input.image.os

The operating system from the image configuration.

```rego
allow if {
    input.image.os == "linux"
}
```

#### input.image.arch

The CPU architecture from the image configuration.

```rego
allow if {
    input.image.arch == "amd64"
}
```

#### input.image.hasProvenance

Boolean indicating if the image has provenance attestations.

```rego
# Require provenance for production images
allow if {
    input.image.hasProvenance
}
```

#### input.image.labels

A map of image labels from the image configuration.

```rego
# Check for specific labels
allow if {
    input.image.labels["org.opencontainers.image.vendor"] == "Example Corp"
}
```

#### input.image.signatures

Array of attestation signatures. Each signature in the array has the following
fields:

- `kind`: Signature kind (e.g., `"docker-github-builder"`, `"self-signed"`)
- `type`: Signature type (e.g., `"bundle-v0.3"`, `"simplesigning-v1"`)
- `timestamps`: Trusted timestamps from transparency logs
- `dockerReference`: Docker image reference
- `isDHI`: Boolean indicating if this is a Docker Hardened Image
- `signer`: Sigstore certificate details

```rego
# Require at least one signature
allow if {
    count(input.image.signatures) > 0
}
```

For Sigstore signatures, the `signer` object provides detailed certificate
information from the signing workflow:

- `certificateIssuer`: Certificate issuer
- `subjectAlternativeName`: Subject alternative name from certificate
- `buildSignerURI`: URI of the build signer
- `buildSignerDigest`: Digest of the build signer
- `runnerEnvironment`: CI/CD runner environment
- `sourceRepositoryURI`: Source repository URL
- `sourceRepositoryDigest`: Source repository digest
- `sourceRepositoryRef`: Source repository ref (branch/tag)
- `sourceRepositoryIdentifier`: Source repository identifier
- `sourceRepositoryOwnerURI`: Repository owner URI
- `buildConfigURI`: Build configuration URI
- `buildTrigger`: What triggered the build
- `runInvocationURI`: CI/CD run invocation URI

```rego
# Require signatures from GitHub Actions
allow if {
    some sig in input.image.signatures
    sig.signer.runnerEnvironment == "github-hosted"
    startswith(sig.signer.sourceRepositoryURI, "https://github.com/myorg/")
}
```

## Git inputs

Git inputs represent Git repositories referenced in `ADD` instructions or used
as build context.

### Example Dockerfile

```dockerfile
ADD git@github.com:moby/buildkit.git#v0.12.0 /src
```

### Available fields

#### input.git.schema

The URL scheme (`https`, `http`, `git`, or `ssh`).

```rego
# Require HTTPS for Git clones
allow if {
    input.git.schema == "https"
}
```

#### input.git.host

The Git host (e.g., `github.com`, `gitlab.com`).

```rego
allow if {
    input.git.host == "github.com"
}
```

#### input.git.remote

The complete Git URL.

```rego
allow if {
    input.git.remote == "https://github.com/moby/buildkit.git"
}
```

#### input.git.ref

The Git reference.

```rego
allow if {
    input.git.ref == "refs/heads/master"
}
```

#### input.git.tagName

The tag name if the reference is a tag.

```rego
# Only allow version tags
allow if {
    regex.match(`^v[0-9]+\.[0-9]+\.[0-9]+$`, input.git.tagName)
}
```

#### input.git.branch

The branch name if the reference is a branch.

```rego
allow if {
    input.git.branch == "main"
}
```

#### input.git.subDir

The subdirectory path within the repository, if specified.

```rego
# Ensure clones are from the root
allow if {
    input.git.subDir == ""
}
```

#### input.git.isCommitRef

Boolean indicating if the reference is a commit SHA (as opposed to a branch or
tag name).

```rego
# Require commit SHAs for production
allow if {
    input.env.target == "production"
    input.git.isCommitRef
}
```

#### input.git.checksum

The checksum of the Git reference. For commit references and branches, this is
the commit hash. For annotated tags, this is the tag object hash.

```rego
allow if {
    input.git.checksum == "abc123..."
}
```

#### input.git.commitChecksum

The commit hash that the reference points to. For annotated tags, this differs
from `checksum` (which is the tag object hash). For commit references and
branches, this is the same as `checksum`.

```rego
allow if {
    input.git.commitChecksum == "abc123..."
}
```

#### input.git.isAnnotatedTag

Boolean indicating if the reference is an annotated tag (as opposed to a
lightweight tag).

```rego
# Require annotated tags
allow if {
    input.git.tagName != ""
    input.git.isAnnotatedTag
}
```

#### input.git.commit

Object containing commit metadata:

- `author`: Author name, email, when
- `committer`: Committer name, email, when
- `message`: Commit message
- `pgpSignature`: PGP signature details if signed
- `sshSignature`: SSH signature details if signed

```rego
# Check commit author
allow if {
    input.git.commit.author.email == "maintainer@example.com"
}
```

#### input.git.tag

Object containing tag metadata for annotated tags:

- `tagger`: Tagger name, email, when
- `message`: Tag message
- `pgpSignature`: PGP signature details if signed
- `sshSignature`: SSH signature details if signed

```rego
# Require signed tags
allow if {
    input.git.tag.pgpSignature != null
}
```

## Local inputs

Local inputs represent the build context directory.

### Available fields

#### input.local.name

The name or path of the local context.

```rego
allow if {
    input.local.name == "."
}
```

Local inputs are typically less restricted than remote inputs, but you can
still write policies to enforce context requirements.

## Environment fields

The `input.env` object provides build configuration information set by user on
invoking the build, not specific to a resource type.

### Available fields

#### input.env.filename

The name of the Dockerfile being built.

```rego
# Stricter rules for production Dockerfile
allow if {
    input.env.filename == "Dockerfile"
    input.image.isCanonical
}

# Relaxed rules for development
allow if {
    input.env.filename == "Dockerfile.dev"
}
```

#### input.env.target

The build target from multi-stage builds.

```rego
# Require signing only for release builds
allow if {
    input.env.target == "release"
    input.git.tagName != ""
    verify_git_signature(input.git.tag, "maintainer.asc")
}
```

#### input.env.args

Build arguments passed with `--build-arg`. Access specific arguments by key.

```rego
# Check build argument values
allow if {
    input.env.args.ENVIRONMENT == "production"
    input.image.hasProvenance
}
```

## Next steps

- See [Built-in functions](https://docs.docker.com/build/policies/built-ins/) for built-in helper functions to
  check and validate input properties
- Browse [Example policies](https://docs.docker.com/build/policies/examples/) for common patterns
- Read about [Rego](https://www.openpolicyagent.org/docs/latest/policy-language/)
  for advanced policy logic

---

# Introduction to build policies

> Get started with writing and evaluating build policies

# Introduction to build policies

   Table of contents

---

Build policies let you validate the inputs to your Docker builds before they
run. This tutorial walks you through creating your first policy, teaching the
Rego basics you need along the way.

## What you'll learn

By the end of this tutorial, you'll understand:

- How to create and organize policy files
- Basic Rego syntax and patterns
- How to write policies that validate URLs, checksums, and images
- How policies evaluate during builds

## Prerequisites

- Buildx version 0.31 or later
- Basic familiarity with Dockerfiles and building images

## How policies work

When you build an image, Buildx resolves all the inputs your
Dockerfile references: base images from `FROM` instructions, files
from `ADD` or `COPY` or build contexts, and Git repositories. Before
running the build, Buildx evaluates your policies against these
inputs. If any input violates a policy, the build fails before any
instructions execute.

Policies are written in Rego, a declarative language designed for expressing
rules and constraints. You don't need to know Rego to get started - this
tutorial teaches you what you need.

## Create your first policy

Create a new directory for this tutorial and add a Dockerfile:

```console
$ mkdir policy-tutorial
$ cd policy-tutorial
```

Create a `Dockerfile` that downloads a file with `ADD`:

```dockerfile
FROM scratch
ADD https://example.com/index.html /index.html
```

Now create a policy file. Policies use the `.rego` extension and live alongside
your Dockerfile. Create `Dockerfile.rego`:

Dockerfile.rego

```rego
package docker

default allow := false

allow if input.local
allow if {
  input.http.host == "example.com"
}

decision := {"allow": allow}
```

Save this file as `Dockerfile.rego` in the same directory as your Dockerfile.

Let's break down what this policy does:

- `package docker` - All build policies must start with this package declaration
- `default allow := false` - This example uses a deny-by-default rule: if inputs do not match an `allow` rule, the policy check fails
- `allow if input.local` - The first rule allows any local files (your build context)
- `allow if { input.http.host == "example.com" }` - The second rule allows HTTP downloads from `example.com`
- `decision := {"allow": allow}` - The final decision object tells Buildx whether to allow or deny the input

This policy says: "Only allow local files and HTTP downloads from
`example.com`". Rego evaluates all the policy rules to figure out the return
value for the `decision` variable, for each build input. The evaluations happen
in parallel and on-demand; the order of the policy rules has no significance.

### Aboutinput.local

You'll see `allow if input.local` in nearly every policy. This rule allows
local file access, which includes your build context (typically, the `.`
directory) and importantly, the Dockerfile itself. Without this rule, Buildx
can't read your Dockerfile to start the build.

Even builds that don't reference any files from the build context often need
`input.local` because the Dockerfile is a local file. The policy evaluates
before the build starts, and denying local access means denying access to the
Dockerfile.

In rare cases, you might want stricter local file policies - for example, in CI
builds where the build context uses a Git URL as a context directly. In these
cases, you may want to deny local sources to prevent untracked files or changes
from making their way into your build.

## Automatic policy loading

Buildx automatically loads policies that match your Dockerfile name. When you
build with `Dockerfile`, Buildx looks for `Dockerfile.rego` in the same
directory. For a file named `app.Dockerfile`, it looks for
`app.Dockerfile.rego`.

This automatic loading means you don't need any command-line flags in most
cases - create the policy file and build.

The policy file must be in the same directory as the Dockerfile. If Buildx
can't find a matching policy, the build proceeds without policy evaluation
(unless you use `--policy strict=true`).

For more control over policy loading, see the [Usage guide](https://docs.docker.com/build/policies/usage/).

## Run a build with your policy

Build the image with policy evaluation enabled:

```console
$ docker build .
```

The build succeeds because the URL in your Dockerfile matches the policy. Now
try changing the URL in your Dockerfile to something else:

```dockerfile
FROM scratch
ADD https://api.github.com/users/octocat /user.json
```

Build again:

```console
$ docker build .
```

This time the build fails with a policy violation. The `api.github.com`
hostname doesn't match the rule in your policy, so Buildx rejects it before
running any build steps.

## Debugging policy failures

If your build fails with a policy violation, use `--progress=plain` to see
exactly what went wrong:

```console
$ docker buildx build --progress=plain .
```

This shows all policy checks, the input data for each source, and allow/deny
decisions. For complete debugging guidance, see [Debugging](https://docs.docker.com/build/policies/debugging/).

## Add helpful error messages

When a policy denies an input, users see a generic error message. You can
provide custom messages that explain why the build was denied:

Dockerfile.rego

```rego
package docker

default allow := false

allow if input.local
allow if {
  input.http.host == "example.com"
  input.http.schema == "https"
}

deny_msg contains msg if {
  not allow
  input.http
  msg := "only HTTPS downloads from example.com are allowed"
}

decision := {"allow": allow, "deny_msg": deny_msg}
```

Now when a build is denied, users see your custom message explaining what went
wrong:

```console
$ docker buildx build .
Policy: only HTTPS downloads from example.com are allowed
ERROR: failed to build: ... source not allowed by policy
```

The `deny_msg` rule uses `contains` to add messages to a set. You can add
multiple deny messages for different failure conditions to help users understand
exactly what needs to change.

## Understand Rego rules

Rego policies are built from rules. A rule defines when something is allowed.
The basic pattern is:

```rego
allow if {
    condition_one
    condition_two
    condition_three
}
```

All conditions must be true for the rule to match. Think of it as an AND
operation - the URL must match AND the checksum must match AND any other
conditions you specify.

You can have multiple `allow` rules in one policy. If any rule matches, the
input is allowed:

```rego
# Allow downloads from example.com
allow if {
    input.http.host == "example.com"
}

# Also allow downloads from api.github.com
allow if {
    input.http.host == "api.github.com"
}
```

This works like OR - the input can match the first rule OR the second rule.

## Access input fields

The `input` object gives you access to information about build inputs. The
structure depends on the input type:

- `input.http` - Files downloaded with `ADD https://...`
- `input.image` - Container images from `FROM` or `COPY --from`
- `input.git` - Git repositories from `ADD git://...` or build context
- `input.local` - Local file context

Refer to the [Input reference](https://docs.docker.com/build/policies/inputs/) for all available input fields.

For HTTP downloads, you can access:

| Key | Description | Example |
| --- | --- | --- |
| input.http.url | The full URL | https://example.com/index.html |
| input.http.schema | The protocol (HTTP/HTTPS) | https |
| input.http.host | The hostname | example.com |
| input.http.path | The URL path, including parameters | /index.html |

Update your policy to require HTTPS:

```rego
package docker

default allow := false

allow if {
    input.http.host == "example.com"
    input.http.schema == "https"
}

decision := {"allow": allow}
```

Now the policy requires both the hostname to be `example.com` and the protocol
to be HTTPS. HTTP URLs (without TLS) would fail the policy check.

## Pattern matching and strings

Rego provides [built-in functions](https://www.openpolicyagent.org/docs/policy-language#built-in-functions) for pattern matching. Use `startswith()` to
match URL prefixes:

```rego
allow if {
    startswith(input.http.url, "https://example.com/")
}
```

This allows any URL that starts with `https://example.com/`.

Use `regex.match()` for complex patterns:

```rego
allow if {
    regex.match(`^https://example\.com/.+\.json$`, input.http.url)
}
```

This matches URLs that:

- Start with `https://example.com/`
- End with `.json`
- Have at least one character between the domain and extension

## Policy file location

Policy files live adjacent to the Dockerfile they validate, using the naming
pattern `<dockerfile-name>.rego`:

```text
project/
├── Dockerfile           # Main Dockerfile
├── Dockerfile.rego      # Policy for Dockerfile
├── lint.Dockerfile      # Linting Dockerfile
└── lint.Dockerfile.rego # Policy for lint.Dockerfile
```

When you build, Buildx automatically loads the corresponding policy file:

```console
$ docker buildx build -f Dockerfile .        # Loads Dockerfile.rego
$ docker buildx build -f lint.Dockerfile .   # Loads lint.Dockerfile.rego
```

## Next steps

You now understand how to write basic build policies for HTTP resources. To
continue learning:

- Apply and test policies: [Using build policies](https://docs.docker.com/build/policies/usage/)
- Learn [Image validation](https://docs.docker.com/build/policies/validate-images/) to validate container images
  from `FROM` instructions
- Learn [Git validation](https://docs.docker.com/build/policies/validate-git/) to validate Git repositories used
  in builds
- See [Example policies](https://docs.docker.com/build/policies/examples/) for copy-paste-ready policies covering
  common scenarios
- Write unit tests for your policies: [Test build policies](https://docs.docker.com/build/policies/testing/)
- Debug policy failures: [Debugging](https://docs.docker.com/build/policies/debugging/)
- Read the [Input reference](https://docs.docker.com/build/policies/inputs/) for all available input fields
- Check the [Built-in functions](https://docs.docker.com/build/policies/built-ins/) for signature verification,
  attestations, and other security checks

---

# Test build policies

> Write and run unit tests for build policies, similar to the opa test command

# Test build policies

   Table of contents

---

The
[docker buildx policy test](https://docs.docker.com/reference/cli/docker/buildx/policy/test/)
command runs unit tests for build policies using OPA's [standard test
framework](https://www.openpolicyagent.org/docs/policy-testing).

```console
$ docker buildx policy test <path>
```

This validates policy logic with mocked inputs.

For testing against real sources (actual image metadata, Git repositories), use
[docker buildx policy eval](https://docs.docker.com/reference/cli/docker/buildx/policy/eval/)
instead. You can use the `eval --print` option to resolve input for a specific
source for writing a test case.

## Basic example

Start with a simple policy that only allows `alpine` images:

Dockerfile.rego

```rego
package docker

default allow = false

allow if {
    input.image.repo == "alpine"
}

decision := {"allow": allow}
```

Create a test file with the `*_test.rego` suffix. Test functions must start
with `test_`:

Dockerfile_test.rego

```rego
package docker

test_alpine_allowed if {
    decision.allow with input as {"image": {"repo": "alpine"}}
}

test_ubuntu_denied if {
    not decision.allow with input as {"image": {"repo": "ubuntu"}}
}
```

Run the tests:

```console
$ docker buildx policy test .
test_alpine_allowed: PASS (allow=true)
test_ubuntu_denied: PASS (allow=false)
```

`PASS` indicates that the tests defined in `Dockerfile_test.rego` executed
successfully and all assertions were satisfied.

## Command options

Filter tests by name with `--run`:

```console
$ docker buildx policy test --run alpine .
test_alpine_allowed: PASS (allow=true)
```

Test policies with non-default filenames using `--filename`:

```console
$ docker buildx policy test --filename app.Dockerfile .
```

This loads `app.Dockerfile.rego` and runs `*_test.rego` files against it.

## Test output

Passed tests show the allow status and any deny messages:

```console
test_alpine_allowed: PASS (allow=true)
test_ubuntu_denied: PASS (allow=false, deny_msg=only alpine images are allowed)
```

Failed tests show input, decision output, and missing fields:

```console
test_invalid: FAIL (allow=false)
input:
  {
    "image": {}
  }
decision:
  {
    "allow": false,
    "deny_msg": [
      "only alpine images are allowed"
    ]
  }
missing_input: input.image.repo
```

## Test deny messages

To test custom error messages, capture the full decision result and assert on
the `deny_msg` field.

For a policy with deny messages:

Dockerfile.rego

```rego
package docker

default allow = false

allow if {
    input.image.repo == "alpine"
}

deny_msg contains msg if {
    not allow
    msg := "only alpine images are allowed"
}

decision := {"allow": allow, "deny_msg": deny_msg}
```

Test the deny message:

Dockerfile_test.rego

```rego
test_deny_message if {
    result := decision with input as {"image": {"repo": "ubuntu"}}
    not result.allow
    "only alpine images are allowed" in result.deny_msg
}
```

## Test patterns

**Test environment-specific rules:**

```rego
test_production_requires_digest if {
    decision.allow with input as {
        "env": {"target": "production"},
        "image": {"isCanonical": true}
    }
}

test_development_allows_tags if {
    decision.allow with input as {
        "env": {"target": "development"},
        "image": {"isCanonical": false}
    }
}
```

**Test multiple registries:**

```rego
test_dockerhub_allowed if {
    decision.allow with input as {
        "image": {
            "ref": "docker.io/library/alpine",
            "host": "docker.io",
            "repo": "alpine"
        }
    }
}

test_ghcr_allowed if {
    decision.allow with input as {
        "image": {
            "ref": "ghcr.io/myorg/myapp",
            "host": "ghcr.io",
            "repo": "myorg/myapp"
        }
    }
}
```

For available input fields, see the [Input reference](https://docs.docker.com/build/policies/inputs/).

## Organize test files

The test runner discovers all `*_test.rego` files recursively:

```plaintext
build-policies/
├── Dockerfile.rego
├── Dockerfile_test.rego
└── tests/
    ├── registries_test.rego
    ├── signatures_test.rego
    └── environments_test.rego
```

Run all tests:

```console
$ docker buildx policy test .
```

Or test specific files:

```console
$ docker buildx policy test tests/registries_test.rego
```
