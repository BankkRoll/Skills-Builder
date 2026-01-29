# LegacyKeyValueFormat and more

# LegacyKeyValueFormat

> Legacy key/value format with whitespace separator should not be used

# LegacyKeyValueFormat

   Table of contents

---

## Output

```text
"ENV key=value" should be used instead of legacy "ENV key value" format
```

## Description

The correct format for declaring environment variables and build arguments in a
Dockerfile is `ENV key=value` and `ARG key=value`, where the variable name
(`key`) and value (`value`) are separated by an equals sign (`=`).
Historically, Dockerfiles have also supported a space separator between the key
and the value (for example, `ARG key value`). This legacy format is deprecated,
and you should only use the format with the equals sign.

## Examples

❌ Bad: using a space separator for variable key and value.

```dockerfile
FROM alpine
ARG foo bar
```

✅ Good: use an equals sign to separate key and value.

```dockerfile
FROM alpine
ARG foo=bar
```

❌ Bad: multi-line variable declaration with a space separator.

```dockerfile
ENV DEPS \
    curl \
    git \
    make
```

✅ Good: use an equals sign and wrap the value in quotes.

```dockerfile
ENV DEPS="\
    curl \
    git \
    make"
```

---

# MaintainerDeprecated

> The MAINTAINER instruction is deprecated, use a label instead to define an image author

# MaintainerDeprecated

   Table of contents

---

## Output

```text
MAINTAINER instruction is deprecated in favor of using label
```

## Description

The `MAINTAINER` instruction, used historically for specifying the author of
the Dockerfile, is deprecated. To set author metadata for an image, use the
`org.opencontainers.image.authors` [OCI label](https://github.com/opencontainers/image-spec/blob/main/annotations.md#pre-defined-annotation-keys).

## Examples

❌ Bad: don't use the `MAINTAINER` instruction

```dockerfile
MAINTAINER moby@example.com
```

✅ Good: specify the author using the `org.opencontainers.image.authors` label

```dockerfile
LABEL org.opencontainers.image.authors="moby@example.com"
```

---

# MultipleInstructionsDisallowed

> Multiple instructions of the same type should not be used in the same stage

# MultipleInstructionsDisallowed

   Table of contents

---

## Output

```text
Multiple CMD instructions should not be used in the same stage because only the last one will be used
```

## Description

If you have multiple `CMD`, `HEALTHCHECK`, or `ENTRYPOINT` instructions in your
Dockerfile, only the last occurrence is used. An image can only ever have one
`CMD`, `HEALTHCHECK`, and `ENTRYPOINT`.

## Examples

❌ Bad: Duplicate instructions.

```dockerfile
FROM alpine
ENTRYPOINT ["echo", "Hello, Norway!"]
ENTRYPOINT ["echo", "Hello, Sweden!"]
# Only "Hello, Sweden!" will be printed
```

✅ Good: only one `ENTRYPOINT` instruction.

```dockerfile
FROM alpine
ENTRYPOINT ["echo", "Hello, Norway!\nHello, Sweden!"]
```

You can have both a regular, top-level `CMD`
and a separate `CMD` for a `HEALTHCHECK` instruction.

✅ Good: only one top-level `CMD` instruction.

```dockerfile
FROM python:alpine
RUN apk add curl
HEALTHCHECK --interval=1s --timeout=3s \
  CMD ["curl", "-f", "http://localhost:8080"]
CMD ["python", "-m", "http.server", "8080"]
```

---

# NoEmptyContinuation

> Empty continuation lines will become errors in a future release

# NoEmptyContinuation

   Table of contents

---

## Output

```text
Empty continuation line found in: RUN apk add     gnupg     curl
```

## Description

Support for empty continuation (`/`) lines have been deprecated and will
generate errors in future versions of the Dockerfile syntax.

Empty continuation lines are empty lines following a newline escape:

```dockerfile
FROM alpine
RUN apk add \

    gnupg \

    curl
```

Support for such empty lines is deprecated, and a future BuildKit release will
remove support for this syntax entirely, causing builds to break. To avoid
future errors, remove the empty lines, or add comments, since lines with
comments aren't considered empty.

## Examples

❌ Bad: empty continuation line between `EXPOSE` and 80.

```dockerfile
FROM alpine
EXPOSE \

80
```

✅ Good: comments do not count as empty lines.

```dockerfile
FROM alpine
EXPOSE \
# Port
80
```

---

# RedundantTargetPlatform

> Setting platform to predefined $TARGETPLATFORM in FROM is redundant as this is the default behavior

# RedundantTargetPlatform

   Table of contents

---

## Output

```text
Setting platform to predefined $TARGETPLATFORM in FROM is redundant as this is the default behavior
```

## Description

A custom platform can be used for a base image. The default platform is the
same platform as the target output so setting the platform to `$TARGETPLATFORM`
is redundant and unnecessary.

## Examples

❌ Bad: this usage of `--platform` is redundant since `$TARGETPLATFORM` is the default.

```dockerfile
FROM --platform=$TARGETPLATFORM alpine AS builder
RUN apk add --no-cache git
```

✅ Good: omit the `--platform` argument.

```dockerfile
FROM alpine AS builder
RUN apk add --no-cache git
```

---

# ReservedStageName

> Reserved words should not be used as stage names

# ReservedStageName

   Table of contents

---

## Output

```text
'scratch' is reserved and should not be used as a stage name
```

## Description

Reserved words should not be used as names for stages in multi-stage builds.
The reserved words are:

- `context`
- `scratch`

## Examples

❌ Bad: `scratch` and `context` are reserved names.

```dockerfile
FROM alpine AS scratch
FROM alpine AS context
```

✅ Good: the stage name `builder` is not reserved.

```dockerfile
FROM alpine AS builder
```

---

# SecretsUsedInArgOrEnv

> Sensitive data should not be used in the ARG or ENV commands

# SecretsUsedInArgOrEnv

   Table of contents

---

## Output

```text
Potentially sensitive data should not be used in the ARG or ENV commands
```

## Description

While it is common to pass secrets to running processes
through environment variables during local development,
setting secrets in a Dockerfile using `ENV` or `ARG`
is insecure because they persist in the final image.
This rule reports violations where `ENV` and `ARG` keys
indicate that they contain sensitive data.

Instead of `ARG` or `ENV`, you should use secret mounts,
which expose secrets to your builds in a secure manner,
and do not persist in the final image or its metadata.
See [Build secrets](https://docs.docker.com/build/building/secrets/).

## Examples

❌ Bad: `AWS_SECRET_ACCESS_KEY` is a secret value.

```dockerfile
FROM scratch
ARG AWS_SECRET_ACCESS_KEY
```

---

# StageNameCasing

> Stage names should be lowercase

# StageNameCasing

   Table of contents

---

## Output

```text
Stage name 'BuilderBase' should be lowercase
```

## Description

To help distinguish Dockerfile instruction keywords from identifiers, this rule
forces names of stages in a multi-stage Dockerfile to be all lowercase.

## Examples

❌ Bad: mixing uppercase and lowercase characters in the stage name.

```dockerfile
FROM alpine AS BuilderBase
```

✅ Good: stage name is all in lowercase.

```dockerfile
FROM alpine AS builder-base
```

---

# UndefinedArgInFrom

> FROM command must use declared ARGs

# UndefinedArgInFrom

   Table of contents

---

## Output

```text
FROM argument 'VARIANT' is not declared
```

## Description

This rule warns for cases where you're consuming an undefined build argument in
`FROM` instructions.

Interpolating build arguments in `FROM` instructions can be a good way to add
flexibility to your build, and lets you pass arguments that overriding the base
image of a stage. For example, you might use a build argument to specify the
image tag:

```dockerfile
ARG ALPINE_VERSION=3.20

FROM alpine:${ALPINE_VERSION}
```

This makes it possible to run the build with a different `alpine` version by
specifying a build argument:

```console
$ docker buildx build --build-arg ALPINE_VERSION=edge .
```

This check also tries to detect and warn when a `FROM` instruction reference
miss-spelled built-in build arguments, like `BUILDPLATFORM`.

## Examples

❌ Bad: the `VARIANT` build argument is undefined.

```dockerfile
FROM node:22${VARIANT} AS jsbuilder
```

✅ Good: the `VARIANT` build argument is defined.

```dockerfile
ARG VARIANT="-alpine3.20"
FROM node:22${VARIANT} AS jsbuilder
```

---

# UndefinedVar

> Variables should be defined before their use

# UndefinedVar

   Table of contents

---

## Output

```text
Usage of undefined variable '$foo'
```

## Description

This check ensures that environment variables and build arguments are correctly
declared before being used. While undeclared variables might not cause an
immediate build failure, they can lead to unexpected behavior or errors later
in the build process.

This check does not evaluate undefined variables for `RUN`, `CMD`, and
`ENTRYPOINT` instructions where you use the [shell form](https://docs.docker.com/reference/dockerfile/#shell-form).
That's because when you use shell form, variables are resolved by the command
shell.

It also detects common mistakes like typos in variable names. For example, in
the following Dockerfile:

```dockerfile
FROM alpine
ENV PATH=$PAHT:/app/bin
```

The check identifies that `$PAHT` is undefined and likely a typo for `$PATH`:

```text
Usage of undefined variable '$PAHT' (did you mean $PATH?)
```

## Examples

❌ Bad: `$foo` is an undefined build argument.

```dockerfile
FROM alpine AS base
COPY $foo .
```

✅ Good: declaring `foo` as a build argument before attempting to access it.

```dockerfile
FROM alpine AS base
ARG foo
COPY $foo .
```

❌ Bad: `$foo` is undefined.

```dockerfile
FROM alpine AS base
ARG VERSION=$foo
```

✅ Good: the base image defines `$PYTHON_VERSION`

```dockerfile
FROM python AS base
ARG VERSION=$PYTHON_VERSION
```

---

# WorkdirRelativePath

> Relative workdir without an absolute workdir declared within the build can have unexpected results if the base image changes

# WorkdirRelativePath

   Table of contents

---

## Output

```text
Relative workdir 'app/src' can have unexpected results if the base image changes
```

## Description

When specifying `WORKDIR` in a build stage, you can use an absolute path, like
`/build`, or a relative path, like `./build`. Using a relative path means that
the working directory is relative to whatever the previous working directory
was. So if your base image uses `/usr/local/foo` as a working directory, and
you specify a relative directory like `WORKDIR build`, the effective working
directory becomes `/usr/local/foo/build`.

The `WorkdirRelativePath` build rule warns you if you use a `WORKDIR` with a
relative path without first specifying an absolute path in the same Dockerfile.
The rationale for this rule is that using a relative working directory for base
image built externally is prone to breaking, since working directory may change
upstream without warning, resulting in a completely different directory
hierarchy for your build.

## Examples

❌ Bad: this assumes that `WORKDIR` in the base image is `/`
(if that changes upstream, the `web` stage is broken).

```dockerfile
FROM nginx AS web
WORKDIR usr/share/nginx/html
COPY public .
```

✅ Good: a leading slash ensures that `WORKDIR` always ends up at the desired path.

```dockerfile
FROM nginx AS web
WORKDIR /usr/share/nginx/html
COPY public .
```

---

# Build checks

> BuildKit has built-in support for analyzing your build configuration based on a set of pre-defined rules for enforcing Dockerfile and building best practices.

# Build checks

---

BuildKit has built-in support for analyzing your build configuration based on a
set of pre-defined rules for enforcing Dockerfile and building best practices.
Adhering to these rules helps avoid errors and ensures good readability of your
Dockerfile.

Checks run as a build invocation, but instead of producing a build output, it
performs a series of checks to validate that your build doesn't violate any of
the rules. To run a check, use the `--check` flag:

```console
$ docker build --check .
```

To learn more about how to use build checks, see
[Checking your build configuration](https://docs.docker.com/build/checks/).

| Name | Description |
| --- | --- |
| StageNameCasing | Stage names should be lowercase |
| FromAsCasing | The 'as' keyword should match the case of the 'from' keyword |
| NoEmptyContinuation | Empty continuation lines will become errors in a future release |
| ConsistentInstructionCasing | All commands within the Dockerfile should use the same casing (either upper or lower) |
| DuplicateStageName | Stage names should be unique |
| ReservedStageName | Reserved words should not be used as stage names |
| JSONArgsRecommended | JSON arguments recommended for ENTRYPOINT/CMD to prevent unintended behavior related to OS signals |
| MaintainerDeprecated | The MAINTAINER instruction is deprecated, use a label instead to define an image author |
| UndefinedArgInFrom | FROM command must use declared ARGs |
| WorkdirRelativePath | Relative workdir without an absolute workdir declared within the build can have unexpected results if the base image changes |
| UndefinedVar | Variables should be defined before their use |
| MultipleInstructionsDisallowed | Multiple instructions of the same type should not be used in the same stage |
| LegacyKeyValueFormat | Legacy key/value format with whitespace separator should not be used |
| RedundantTargetPlatform | Setting platform to predefined $TARGETPLATFORM in FROM is redundant as this is the default behavior |
| SecretsUsedInArgOrEnv | Sensitive data should not be used in the ARG or ENV commands |
| InvalidDefaultArgInFrom | Default value for global ARG results in an empty or invalid base image name |
| FromPlatformFlagConstDisallowed | FROM --platform flag should not use a constant value |
| CopyIgnoredFile | Attempting to Copy file that is excluded by .dockerignore |
| InvalidDefinitionDescription (experimental) | Comment for build stage or argument should follow the format: `#`. If this is not intended to be a description comment, add an empty line or comment between the instruction and the comment. |
| ExposeProtoCasing | Protocol in EXPOSE instruction should be lowercase |
| ExposeInvalidFormat | IP address and host-port mapping should not be used in EXPOSE instruction. This will become an error in a future release |

---

# docker build (legacy builder)

# docker build (legacy builder)

| Description | Build an image from a Dockerfile |
| --- | --- |
| Usage | docker image build [OPTIONS] PATH | URL | - |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker image builddocker builddocker builder build |

## Description

> Important
>
> This page refers to the **legacy implementation** of `docker build`,
> using the legacy (pre-BuildKit) build backend.
> This configuration is only relevant if you're building Windows containers.
>
>
>
> For information about the default `docker build`, using Buildx,
> see
> [docker buildx build](https://docs.docker.com/reference/cli/docker/build/).

When building with legacy builder, images are created from a Dockerfile by
running a sequence of
[commits](https://docs.docker.com/reference/cli/docker/container/commit/). This process is
inefficient and slow compared to using BuildKit, which is why this build
strategy is deprecated for all use cases except for building Windows
containers. It's still useful for building Windows containers because BuildKit
doesn't yet have full feature parity for Windows.

Builds invoked with `docker build` use Buildx (and BuildKit) by default, unless:

- You're running Docker Engine in Windows container mode
- You explicitly opt out of using BuildKit by setting the environment variable `DOCKER_BUILDKIT=0`.

The descriptions on this page only covers information that's exclusive to the
legacy builder, and cases where behavior in the legacy builder deviates from
behavior in BuildKit. For information about features and flags that are common
between the legacy builder and BuildKit, such as `--tag` and `--target`, refer
to the documentation for
[docker buildx build](https://docs.docker.com/reference/cli/docker/buildx/build/).

### Build context with the legacy builder

The build context is the positional argument you pass when invoking the build
command. In the following example, the context is `.`, meaning current the
working directory.

```console
$ docker build .
```

When using the legacy builder, the build context is sent over to the daemon in
its entirety. With BuildKit, only the files you use in your builds are
transmitted. The legacy builder doesn't calculate which files it needs
beforehand. This means that for builds with a large context, context transfer
can take a long time, even if you're only using a subset of the files included
in the context.

When using the legacy builder, it's therefore extra important that you
carefully consider what files you include in the context you specify. Use a
[.dockerignore](https://docs.docker.com/build/concepts/context/#dockerignore-files)
file to exclude files and directories that you don't require in your build from
being sent as part of the build context.

#### Accessing paths outside the build context

The legacy builder will error out if you try to access files outside of the
build context using relative paths in your Dockerfile.

```dockerfile
FROM alpine
COPY ../../some-dir .
```

```console
$ docker build .
...
Step 2/2 : COPY ../../some-dir .
COPY failed: forbidden path outside the build context: ../../some-dir ()
```

BuildKit on the other hand strips leading relative paths that traverse outside
of the build context. Re-using the previous example, the path `COPY ../../some-dir .` evaluates to `COPY some-dir .` with BuildKit.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --add-host |  | Add a custom host-to-IP mapping (host:ip) |
| --build-arg |  | Set build-time variables |
| --cache-from |  | Images to consider as cache sources |
| --cgroup-parent |  | Set the parent cgroup for theRUNinstructions during build |
| --compress |  | Compress the build context using gzip |
| --cpu-period |  | Limit the CPU CFS (Completely Fair Scheduler) period |
| --cpu-quota |  | Limit the CPU CFS (Completely Fair Scheduler) quota |
| -c, --cpu-shares |  | CPU shares (relative weight) |
| --cpuset-cpus |  | CPUs in which to allow execution (0-3, 0,1) |
| --cpuset-mems |  | MEMs in which to allow execution (0-3, 0,1) |
| -f, --file |  | Name of the Dockerfile (Default isPATH/Dockerfile) |
| --force-rm |  | Always remove intermediate containers |
| --iidfile |  | Write the image ID to the file |
| --isolation |  | Container isolation technology |
| --label |  | Set metadata for an image |
| -m, --memory |  | Memory limit |
| --memory-swap |  | Swap limit equal to memory plus swap: -1 to enable unlimited swap |
| --network |  | API 1.25+Set the networking mode for the RUN instructions during build |
| --no-cache |  | Do not use cache when building the image |
| --platform |  | API 1.38+Set platform if server is multi-platform capable |
| --pull |  | Always attempt to pull a newer version of the image |
| -q, --quiet |  | Suppress the build output and print image ID on success |
| --rm | true | Remove intermediate containers after a successful build |
| --security-opt |  | Security options |
| --shm-size |  | Size of/dev/shm |
| --squash |  | API 1.25+experimental (daemon)Squash newly built layers into a single new layer |
| -t, --tag |  | Name and optionally a tag in thename:tagformat |
| --target |  | Set the target build stage to build. |
| --ulimit |  | Ulimit options |

## Examples

### Specify isolation technology for container (--isolation)

This option is useful in situations where you are running Docker containers on
Windows. The `--isolation=<value>` option sets a container's isolation
technology. On Linux, the only supported is the `default` option which uses
Linux namespaces. On Microsoft Windows, you can specify these values:

| Value | Description |
| --- | --- |
| default | Use the value specified by the Docker daemon's--exec-opt. If thedaemondoes not specify an isolation technology, Microsoft Windows usesprocessas its default value. |
| process | Namespace isolation only. |
| hyperv | Hyper-V hypervisor partition-based isolation. |

### Optional security options (--security-opt)

This flag is only supported on a daemon running on Windows, and only supports
the `credentialspec` option. The `credentialspec` must be in the format
`file://spec.txt` or `registry://keyname`.

### Squash an image's layers (--squash) (experimental)

#### Overview

> Note
>
> The `--squash` option is an experimental feature, and should not be considered
> stable.

Once the image is built, this flag squashes the new layers into a new image with
a single new layer. Squashing doesn't destroy any existing image, rather it
creates a new image with the content of the squashed layers. This effectively
makes it look like all `Dockerfile` commands were created with a single layer.
The `--squash` flag preserves the build cache.

Squashing layers can be beneficial if your Dockerfile produces multiple layers
modifying the same files. For example, files created in one step and
removed in another step. For other use-cases, squashing images may actually have
a negative impact on performance. When pulling an image consisting of multiple
layers, the daemon can pull layers in parallel and allows sharing layers between
images (saving space).

For most use cases, multi-stage builds are a better alternative, as they give more
fine-grained control over your build, and can take advantage of future
optimizations in the builder. Refer to the
[Multi-stage builds](https://docs.docker.com/build/building/multi-stage/)
section for more information.

#### Known limitations

The `--squash` option has a number of known limitations:

- When squashing layers, the resulting image can't take advantage of layer
  sharing with other images, and may use significantly more space. Sharing the
  base image is still supported.
- When using this option you may see significantly more space used due to
  storing two copies of the image, one for the build cache with all the cache
  layers intact, and one for the squashed version.
- While squashing layers may produce smaller images, it may have a negative
  impact on performance, as a single layer takes longer to extract, and
  you can't parallelize downloading a single layer.
- When attempting to squash an image that doesn't make changes to the
  filesystem (for example, the Dockerfile only contains `ENV` instructions),
  the squash step will fail (see [issue #33823](https://github.com/moby/moby/issues/33823)).

#### Prerequisites

The example on this page is using experimental mode in Docker 23.03.

You can enable experimental mode by using the `--experimental` flag when starting
the Docker daemon or setting `experimental: true` in the `daemon.json` configuration
file.

By default, experimental mode is disabled. To see the current configuration of
the Docker daemon, use the `docker version` command and check the `Experimental`
line in the `Engine` section:

```console
Client: Docker Engine - Community
 Version:           28.5.1
 API version:       1.51
 Go version:        go1.24.8
 Git commit:        e180ab8
 Built:             Wed Oct  8 12:16:17 2025
 OS/Arch:           darwin/arm64
 Context:           desktop-linux

Server: Docker Engine - Community
 Engine:
  Version:          28.5.1
  API version:      1.51 (minimum version 1.24)
  Go version:       go1.24.8
  Git commit:       f8215cc
  Built:            Wed Oct  8 12:18:25 2025
  OS/Arch:          linux/arm64
  Experimental:     true
 [...]
```

#### Build an image with the--squashflag

The following is an example of a build with the `--squash` flag. Below is the
`Dockerfile`:

```dockerfile
FROM busybox
RUN echo hello > /hello
RUN echo world >> /hello
RUN touch remove_me /remove_me
ENV HELLO=world
RUN rm /remove_me
```

Next, build an image named `test` using the `--squash` flag.

```console
$ docker build --squash -t test .
```

After the build completes, the history looks like the below. The history could show that a layer's
name is `<missing>`, and there is a new layer with COMMENT `merge`.

```console
$ docker history test

IMAGE               CREATED             CREATED BY                                      SIZE                COMMENT
4e10cb5b4cac        3 seconds ago                                                       12 B                merge sha256:88a7b0112a41826885df0e7072698006ee8f621c6ab99fca7fe9151d7b599702 to sha256:47bcc53f74dc94b1920f0b34f6036096526296767650f223433fe65c35f149eb
<missing>           5 minutes ago       /bin/sh -c rm /remove_me                        0 B
<missing>           5 minutes ago       /bin/sh -c #(nop) ENV HELLO=world               0 B
<missing>           5 minutes ago       /bin/sh -c touch remove_me /remove_me           0 B
<missing>           5 minutes ago       /bin/sh -c echo world >> /hello                 0 B
<missing>           6 minutes ago       /bin/sh -c echo hello > /hello                  0 B
<missing>           7 weeks ago         /bin/sh -c #(nop) CMD ["sh"]                    0 B
<missing>           7 weeks ago         /bin/sh -c #(nop) ADD file:47ca6e777c36a4cfff   1.113 MB
```

Test the image, check for `/remove_me` being gone, make sure `hello\nworld` is
in `/hello`, make sure the `HELLO` environment variable's value is `world`.

---

# docker builder prune

# docker builder prune

| Description | Remove build cache |
| --- | --- |
| Usage | docker builder prune |

## Description

Remove build cache

## Options

| Option | Default | Description |
| --- | --- | --- |
| -a, --all |  | Remove all unused build cache, not just dangling ones |
| --filter |  | Provide filter values (e.g.until=24h) |
| -f, --force |  | Do not prompt for confirmation |
| --keep-storage |  | Amount of disk space to keep for cache |

---

# docker builder

# docker builder

| Description | Manage builds |
| --- | --- |
| Usage | docker builder |

## Description

Manage builds

## Subcommands

| Command | Description |
| --- | --- |
| docker builder prune | Remove build cache |

---

# docker buildx bake

# docker buildx bake

| Description | Build from a file |
| --- | --- |
| Usage | docker buildx bake [OPTIONS] [TARGET...] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker buildx f |

## Description

Bake is a high-level build command. Each specified target runs in parallel
as part of the build.

Read
[High-level build options with Bake](https://docs.docker.com/build/bake/)
guide for introduction to writing bake files.

> Note
>
> `buildx bake` command may receive backwards incompatible features in the future
> if needed. We are looking for feedback on improving the command and extending
> the functionality further.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --allow |  | Allow build to access specified resources |
| --call | build | Set method for evaluating build (check,outline,targets) |
| --check |  | Shorthand for--call=check |
| -f, --file |  | Build definition file |
| --list |  | List targets or variables |
| --load |  | Shorthand for--set=*.output=type=docker. Conditional. |
| --metadata-file |  | Write build result metadata to a file |
| --no-cache |  | Do not use cache when building the image |
| --print |  | Print the options without building |
| --progress | auto | Set type of progress output (auto,none,plain,quiet,rawjson,tty). Use plain to show container output |
| --provenance |  | Shorthand for--set=*.attest=type=provenance |
| --pull |  | Always attempt to pull all referenced images |
| --push |  | Shorthand for--set=*.output=type=registry. Conditional. |
| --sbom |  | Shorthand for--set=*.attest=type=sbom |
| --set |  | Override target value (e.g.,targetpattern.key=value) |
| --var |  | Set a variable value (e.g.,name=value) |

## Examples

### Allow extra privileged entitlement (--allow)

```text
--allow=ENTITLEMENT[=VALUE]
```

Entitlements are designed to provide controlled access to privileged
operations. By default, Buildx and BuildKit operates with restricted
permissions to protect users and their systems from unintended side effects or
security risks. The `--allow` flag explicitly grants access to additional
entitlements, making it clear when a build or bake operation requires elevated
privileges.

In addition to BuildKit's `network.host` and `security.insecure` entitlements
(see
[docker buildx build --allow](https://docs.docker.com/reference/cli/docker/buildx/build/#allow)),
Bake supports file system entitlements that grant granular control over file
system access. These are particularly useful when working with builds that need
access to files outside the default working directory.

Bake supports the following filesystem entitlements:

- `--allow fs=<path|*>` - Grant read and write access to files outside of the
  working directory.
- `--allow fs.read=<path|*>` - Grant read access to files outside of the
  working directory.
- `--allow fs.write=<path|*>` - Grant write access to files outside of the
  working directory.

The `fs` entitlements take a path value (relative or absolute) to a directory
on the filesystem. Alternatively, you can pass a wildcard (`*`) to allow Bake
to access the entire filesystem.

### Example: fs.read

Given the following Bake configuration, Bake would need to access the parent
directory, relative to the Bake file.

```hcl
target "app" {
  context = "../src"
}
```

Assuming `docker buildx bake app` is executed in the same directory as the
`docker-bake.hcl` file, you would need to explicitly allow Bake to read from
the `../src` directory. In this case, the following invocations all work:

```console
$ docker buildx bake --allow fs.read=* app
$ docker buildx bake --allow fs.read=../src app
$ docker buildx bake --allow fs=* app
```

### Example: fs.write

The following `docker-bake.hcl` file requires write access to the `/tmp`
directory.

```hcl
target "app" {
  output = "/tmp"
}
```

Assuming `docker buildx bake app` is executed outside of the `/tmp` directory,
you would need to allow the `fs.write` entitlement, either by specifying the
path or using a wildcard:

```console
$ docker buildx bake --allow fs=/tmp app
$ docker buildx bake --allow fs.write=/tmp app
$ docker buildx bake --allow fs.write=* app
```

### Override the configured builder instance (--builder)

Same as
[buildx --builder](https://docs.docker.com/reference/cli/docker/buildx/#builder).

### Invoke a frontend method (--call)

Same as
[build --call](https://docs.docker.com/reference/cli/docker/buildx/build/#call).

#### Call: check (--check)

Same as
[build --check](https://docs.docker.com/reference/cli/docker/buildx/build/#check).

### Specify a build definition file (-f, --file)

Use the `-f` / `--file` option to specify the build definition file to use.
The file can be an HCL, JSON or Compose file. If multiple files are specified,
all are read and the build configurations are combined.

Alternatively, the environment variable `BUILDX_BAKE_FILE` can be used to specify the build definition to use.
This is mutually exclusive with `-f` / `--file`; if both are specified, the environment variable is ignored.
Multiple definitions can be specified by separating them with the system's path separator
(typically `;` on Windows and `:` elsewhere), but can be changed with `BUILDX_BAKE_PATH_SEPARATOR`.

You can pass the names of the targets to build, to build only specific target(s).
The following example builds the `db` and `webapp-release` targets that are
defined in the `docker-bake.dev.hcl` file:

```hcl
# docker-bake.dev.hcl
group "default" {
  targets = ["db", "webapp-dev"]
}

target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp"]
}

target "webapp-release" {
  inherits = ["webapp-dev"]
  platforms = ["linux/amd64", "linux/arm64"]
}

target "db" {
  dockerfile = "Dockerfile.db"
  tags = ["docker.io/username/db"]
}
```

```console
$ docker buildx bake -f docker-bake.dev.hcl db webapp-release
```

See the
[Bake file reference](https://docs.docker.com/build/bake/reference/)
for more details.

### List targets and variables (--list)

The `--list` flag displays all available targets or variables in the Bake
configuration, along with a description (if set using the `description`
property in the Bake file).

To list all targets:

List targets

```console
$ docker buildx bake --list=targets
TARGET              DESCRIPTION
binaries
default             binaries
update-docs
validate
validate-golangci   Validate .golangci.yml schema (does not run Go linter)
```

To list variables:

```console
$ docker buildx bake --list=variables
VARIABLE      TYPE      VALUE                DESCRIPTION
REGISTRY      string    docker.io/username   Registry and namespace
IMAGE_NAME    string    my-app               Image name
GO_VERSION              <null>
DEBUG         bool      false                Add debug symbols
```

Variable types will be shown when set using the `type` property in the Bake file.

By default, the output of `docker buildx bake --list` is presented in a table
format. Alternatively, you can use a long-form CSV syntax and specify a
`format` attribute to output the list in JSON.

```console
$ docker buildx bake --list=type=targets,format=json
```

### Load images into Docker (--load)

The `--load` flag is a convenience shorthand for adding an image export of type
`docker`:

```console
--load   ≈   --set=*.output=type=docker
```

However, its behavior is conditional:

- If the build definition has no output defined, `--load` adds
  `type=docker`.
- If the build definition’s outputs are `docker`, `image`, `registry`,
  `oci`, `--load` will add a `type=docker` export if one is not already present.
- If the build definition contains `local` or `tar` outputs,
  `--load` does nothing. It will not override those outputs.

For example, with the following bake file:

```hcl
target "default" {
  output = ["type=tar,dest=hi.tar"]
}
```

With `--load`:

```console
$ docker buildx bake --load --print
...
"output": [
  {
    "dest": "hi.tar"
    "type": "tar",
   }
]
```

The `tar` output remains unchanged.

### Write build results metadata to a file (--metadata-file)

Similar to
[buildx build --metadata-file](https://docs.docker.com/reference/cli/docker/buildx/build/#metadata-file) but
writes a map of results for each target such as:

```hcl
# docker-bake.hcl
group "default" {
  targets = ["db", "webapp-dev"]
}

target "db" {
  dockerfile = "Dockerfile.db"
  tags = ["docker.io/username/db"]
}

target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp"]
}
```

```console
$ docker buildx bake --load --metadata-file metadata.json .
$ cat metadata.json
```

```json
{
  "buildx.build.warnings": {},
  "db": {
    "buildx.build.provenance": {},
    "buildx.build.ref": "mybuilder/mybuilder0/0fjb6ubs52xx3vygf6fgdl611",
    "containerimage.config.digest": "sha256:2937f66a9722f7f4a2df583de2f8cb97fc9196059a410e7f00072fc918930e66",
    "containerimage.descriptor": {
      "annotations": {
        "config.digest": "sha256:2937f66a9722f7f4a2df583de2f8cb97fc9196059a410e7f00072fc918930e66",
        "org.opencontainers.image.created": "2022-02-08T21:28:03Z"
      },
      "digest": "sha256:19ffeab6f8bc9293ac2c3fdf94ebe28396254c993aea0b5a542cfb02e0883fa3",
      "mediaType": "application/vnd.oci.image.manifest.v1+json",
      "size": 506
    },
    "containerimage.digest": "sha256:19ffeab6f8bc9293ac2c3fdf94ebe28396254c993aea0b5a542cfb02e0883fa3"
  },
  "webapp-dev": {
    "buildx.build.provenance": {},
    "buildx.build.ref": "mybuilder/mybuilder0/kamngmcgyzebqxwu98b4lfv3n",
    "containerimage.config.digest": "sha256:9651cc2b3c508f697c9c43b67b64c8359c2865c019e680aac1c11f4b875b67e0",
    "containerimage.descriptor": {
      "annotations": {
        "config.digest": "sha256:9651cc2b3c508f697c9c43b67b64c8359c2865c019e680aac1c11f4b875b67e0",
        "org.opencontainers.image.created": "2022-02-08T21:28:15Z"
      },
      "digest": "sha256:6d9ac9237a84afe1516540f40a0fafdc86859b2141954b4d643af7066d598b74",
      "mediaType": "application/vnd.oci.image.manifest.v1+json",
      "size": 506
    },
    "containerimage.digest": "sha256:6d9ac9237a84afe1516540f40a0fafdc86859b2141954b4d643af7066d598b74"
  }
}
```

> Note
>
> Build record
> [provenance](https://docs.docker.com/build/metadata/attestations/slsa-provenance/#provenance-attestation-example)
> (`buildx.build.provenance`) includes minimal provenance by default. Set the
> `BUILDX_METADATA_PROVENANCE` environment variable to customize this behavior:
>
>
>
> - `min` sets minimal provenance (default).
> - `max` sets full provenance.
> - `disabled`, `false` or `0` does not set any provenance.

> Note
>
> Build warnings (`buildx.build.warnings`) are not included by default. Set the
> `BUILDX_METADATA_WARNINGS` environment variable to `1` or `true` to
> include them.

### Don't use cache when building the image (--no-cache)

Same as `build --no-cache`. Don't use cache when building the image.

### Print the options without building (--print)

Prints the resulting options of the targets desired to be built, in a JSON
format, without starting a build.

```console
$ docker buildx bake -f docker-bake.hcl --print db
{
  "group": {
    "default": {
      "targets": [
        "db"
      ]
    }
  },
  "target": {
    "db": {
      "context": "./",
      "dockerfile": "Dockerfile",
      "tags": [
        "docker.io/tiborvass/db"
      ]
    }
  }
}
```

### Set type of progress output (--progress)

Same as
[build --progress](https://docs.docker.com/reference/cli/docker/buildx/build/#progress).

### Create provenance attestations (--provenance)

Same as
[build --provenance](https://docs.docker.com/reference/cli/docker/buildx/build/#provenance).

### Always attempt to pull a newer version of the image (--pull)

Same as `build --pull`.

### Push images to a registry (--push)

The `--push` flag follows the same logic as `--load`:

- If no outputs are defined, it adds a `type=image,push=true` export.
- For existing `image` outputs, it sets `push=true`.
- If outputs are set to `local` or `tar`, it does not override them.

### Create SBOM attestations (--sbom)

Same as
[build --sbom](https://docs.docker.com/reference/cli/docker/buildx/build/#sbom).

### Override target configurations from command line (--set)

```text
--set targetpattern.key[.subkey]=value
```

Override target configurations from command line. The pattern matching syntax
is defined in [https://golang.org/pkg/path/#Match](https://golang.org/pkg/path/#Match).

```console
$ docker buildx bake --set target.args.mybuildarg=value
$ docker buildx bake --set target.platform=linux/arm64
$ docker buildx bake --set foo*.args.mybuildarg=value   # overrides build arg for all targets starting with 'foo'
$ docker buildx bake --set *.platform=linux/arm64       # overrides platform for all targets
$ docker buildx bake --set foo*.no-cache                # bypass caching only for targets starting with 'foo'
$ docker buildx bake --set target.platform+=linux/arm64 # appends 'linux/arm64' to the platform list
$ docker buildx bake --set target.contexts.bar=../bar   # overrides 'bar' named context
```

> Note
>
> `--set` is a repeatable flag. For array fields such as `tags`, repeat `--set`
> to provide multiple values or use the `+=` operator to append without
> replacing. Array literal syntax like `--set target.tags=[a,b]` is not
> supported.

You can override the following fields:

- `annotations`
- `attest`
- `args`
- `cache-from`
- `cache-to`
- `call`
- `context`
- `contexts`
- `dockerfile`
- `entitlements`
- `extra-hosts`
- `labels`
- `load`
- `no-cache`
- `no-cache-filter`
- `output`
- `platform`
- `pull`
- `push`
- `secrets`
- `ssh`
- `tags`
- `target`

You can append using `+=` operator for the following fields:

- `annotations`¹
- `attest`¹
- `cache-from`
- `cache-to`
- `entitlements`¹
- `no-cache-filter`
- `output`
- `platform`
- `secrets`
- `ssh`
- `tags`

> Note
>
> ¹ These fields already append by default.
