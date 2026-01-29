# Build secrets and more

# Build secrets

> Manage credentials and other secrets securely

# Build secrets

   Table of contents

---

A build secret is any piece of sensitive information, such as a password or API
token, consumed as part of your application's build process.

Build arguments and environment variables are inappropriate for passing secrets
to your build, because they persist in the final image. Instead, you should use
secret mounts or SSH mounts, which expose secrets to your builds securely.

## Types of build secrets

- [Secret mounts](#secret-mounts) are general-purpose mounts for passing
  secrets into your build. A secret mount takes a secret from the build client
  and makes it temporarily available inside the build container, for the
  duration of the build instruction. This is useful if, for example, your build
  needs to communicate with a private artifact server or API.
- [SSH mounts](#ssh-mounts) are special-purpose mounts for making SSH sockets
  or keys available inside builds. They're commonly used when you need to fetch
  private Git repositories in your builds.
- [Git authentication for remote contexts](#git-authentication-for-remote-contexts)
  is a set of pre-defined secrets for when you build with a remote Git context
  that's also a private repository. These secrets are "pre-flight" secrets:
  they are not consumed within your build instruction, but they're used to
  provide the builder with the necessary credentials to fetch the context.

## Using build secrets

For secret mounts and SSH mounts, using build secrets is a two-step process.
First you need to pass the secret into the `docker build` command, and then you
need to consume the secret in your Dockerfile.

To pass a secret to a build, use the
[docker build --secretflag](https://docs.docker.com/reference/cli/docker/buildx/build/#secret), or the
equivalent options for [Bake](https://docs.docker.com/build/bake/reference/#targetsecret).

```console
$ docker build --secret id=aws,src=$HOME/.aws/credentials .
```

```hcl
variable "HOME" {
  default = null
}

target "default" {
  secret = [
    "id=aws,src=${HOME}/.aws/credentials"
  ]
}
```

To consume a secret in a build and make it accessible to the `RUN` instruction,
use the
[--mount=type=secret](https://docs.docker.com/reference/dockerfile/#run---mounttypesecret)
flag in the Dockerfile.

```dockerfile
RUN --mount=type=secret,id=aws \
    AWS_SHARED_CREDENTIALS_FILE=/run/secrets/aws \
    aws s3 cp ...
```

## Secret mounts

Secret mounts expose secrets to the build containers, as files or environment
variables. You can use secret mounts to pass sensitive information to your
builds, such as API tokens, passwords, or SSH keys.

### Sources

The source of a secret can be either a
[file](https://docs.docker.com/reference/cli/docker/buildx/build/#file) or an
[environment variable](https://docs.docker.com/reference/cli/docker/buildx/build/#env).
When you use the CLI or Bake, the type can be detected automatically. You can
also specify it explicitly with `type=file` or `type=env`.

The following example mounts the environment variable `KUBECONFIG` to secret ID `kube`,
as a file in the build container at `/run/secrets/kube`.

```console
$ docker build --secret id=kube,env=KUBECONFIG .
```

When you use secrets from environment variables, you can omit the `env` parameter
to bind the secret to a file with the same name as the variable.
In the following example, the value of the `API_TOKEN` variable
is mounted to `/run/secrets/API_TOKEN` in the build container.

```console
$ docker build --secret id=API_TOKEN .
```

### Target

When consuming a secret in a Dockerfile, the secret is mounted to a file by
default. The default file path of the secret, inside the build container, is
`/run/secrets/<id>`. You can customize how the secrets get mounted in the build
container using the `target` and `env` options for the `RUN --mount` flag in
the Dockerfile.

The following example takes secret id `aws` and mounts it to a file at
`/run/secrets/aws` in the build container.

```dockerfile
RUN --mount=type=secret,id=aws \
    AWS_SHARED_CREDENTIALS_FILE=/run/secrets/aws \
    aws s3 cp ...
```

To mount a secret as a file with a different name, use the `target` option in
the `--mount` flag.

```dockerfile
RUN --mount=type=secret,id=aws,target=/root/.aws/credentials \
    aws s3 cp ...
```

To mount a secret as an environment variable instead of a file, use the
`env` option in the `--mount` flag.

```dockerfile
RUN --mount=type=secret,id=aws-key-id,env=AWS_ACCESS_KEY_ID \
    --mount=type=secret,id=aws-secret-key,env=AWS_SECRET_ACCESS_KEY \
    --mount=type=secret,id=aws-session-token,env=AWS_SESSION_TOKEN \
    aws s3 cp ...
```

It's possible to use the `target` and `env` options together to mount a secret
as both a file and an environment variable.

## SSH mounts

If the credential you want to use in your build is an SSH agent socket or key,
you can use the SSH mount instead of a secret mount. Cloning private Git
repositories is a common use case for SSH mounts.

The following example clones a private GitHub repository using a
[Dockerfile
SSH mount](https://docs.docker.com/reference/dockerfile/#run---mounttypessh).

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
ADD git@github.com:me/myprivaterepo.git /src/
```

To pass an SSH socket the build, you use the
[docker build --sshflag](https://docs.docker.com/reference/cli/docker/buildx/build/#ssh), or equivalent
options for [Bake](https://docs.docker.com/build/bake/reference/#targetssh).

```console
$ docker buildx build --ssh default .
```

## Git authentication for remote contexts

BuildKit supports two pre-defined build secrets, `GIT_AUTH_TOKEN` and
`GIT_AUTH_HEADER`. Use them to specify HTTP authentication parameters when
building with remote, private Git repositories, including:

- Building with a private Git repository as build context
- Fetching private Git repositories in a build with `ADD`

For example, say you have a private GitLab project at
`https://gitlab.com/example/todo-app.git`, and you want to run a build using
that repository as the build context. An unauthenticated `docker build` command
fails because the builder isn't authorized to pull the repository:

```console
$ docker build https://gitlab.com/example/todo-app.git
[+] Building 0.4s (1/1) FINISHED
 => ERROR [internal] load git source https://gitlab.com/example/todo-app.git
------
 > [internal] load git source https://gitlab.com/example/todo-app.git:
0.313 fatal: could not read Username for 'https://gitlab.com': terminal prompts disabled
------
```

To authenticate the builder to the Git server, set the `GIT_AUTH_TOKEN`
environment variable to contain a valid GitLab access token, and pass it as a
secret to the build:

```console
$ GIT_AUTH_TOKEN=$(cat gitlab-token.txt) docker build \
  --secret id=GIT_AUTH_TOKEN \
  https://gitlab.com/example/todo-app.git
```

The `GIT_AUTH_TOKEN` also works with `ADD` to fetch private Git repositories as
part of your build:

```dockerfile
FROM alpine
ADD https://gitlab.com/example/todo-app.git /src
```

### HTTP authentication scheme

By default, Git authentication over HTTP uses the Bearer authentication scheme:

```http
Authorization: Bearer GIT_AUTH_TOKEN
```

If you need to use a Basic scheme, with a username and password, you can set
the `GIT_AUTH_HEADER` build secret:

```console
$ export GIT_AUTH_TOKEN=$(cat gitlab-token.txt)
$ export GIT_AUTH_HEADER=basic
$ docker build \
  --secret id=GIT_AUTH_TOKEN \
  --secret id=GIT_AUTH_HEADER \
  https://gitlab.com/example/todo-app.git
```

BuildKit currently only supports the Bearer and Basic schemes.

### Multiple hosts

You can set the `GIT_AUTH_TOKEN` and `GIT_AUTH_HEADER` secrets on a per-host
basis, which lets you use different authentication parameters for different
hostnames. To specify a hostname, append the hostname as a suffix to the secret
ID:

```console
$ export GITLAB_TOKEN=$(cat gitlab-token.txt)
$ export GERRIT_TOKEN=$(cat gerrit-username-password.txt)
$ export GERRIT_SCHEME=basic
$ docker build \
  --secret id=GIT_AUTH_TOKEN.gitlab.com,env=GITLAB_TOKEN \
  --secret id=GIT_AUTH_TOKEN.gerrit.internal.example,env=GERRIT_TOKEN \
  --secret id=GIT_AUTH_HEADER.gerrit.internal.example,env=GERRIT_SCHEME \
  https://gitlab.com/example/todo-app.git
```

---

# Build variables

> Using build arguments and environment variables to configure builds

# Build variables

   Table of contents

---

In Docker Build, build arguments (`ARG`) and environment variables (`ENV`)
both serve as a means to pass information into the build process.
You can use them to parameterize the build, allowing for more flexible and configurable builds.

> Warning
>
> Build arguments and environment variables are inappropriate for passing secrets
> to your build, because they're exposed in the final image. Instead, use
> secret mounts or SSH mounts, which expose secrets to your builds securely.
>
>
>
> See [Build secrets](https://docs.docker.com/build/building/secrets/) for more information.

## Similarities and differences

Build arguments and environment variables are similar.
They're both declared in the Dockerfile and can be set using flags for the `docker build` command.
Both can be used to parameterize the build.
But they each serve a distinct purpose.

### Build arguments

Build arguments are variables for the Dockerfile itself.
Use them to parameterize values of Dockerfile instructions.
For example, you might use a build argument to specify the version of a dependency to install.

Build arguments have no effect on the build unless it's used in an instruction.
They're not accessible or present in containers instantiated from the image
unless explicitly passed through from the Dockerfile into the image filesystem or configuration.
They may persist in the image metadata, as provenance attestations and in the image history,
which is why they're not suitable for holding secrets.

They make Dockerfiles more flexible, and easier to maintain.

For an example on how you can use build arguments,
see [ARGusage example](#arg-usage-example).

### Environment variables

Environment variables are passed through to the build execution environment,
and persist in containers instantiated from the image.

Environment variables are primarily used to:

- Configure the execution environment for builds
- Set default environment variables for containers

Environment variables, if set, can directly influence the execution of your build,
and the behavior or configuration of the application.

You can't override or set an environment variable at build-time.
Values for environment variables must be declared in the Dockerfile.
You can combine environment variables and build arguments to allow
environment variables to be configured at build-time.

For an example on how to use environment variables for configuring builds,
see [ENVusage example](#env-usage-example).

## ARGusage example

Build arguments are commonly used to specify versions of components,
such as image variants or package versions, used in a build.

Specifying versions as build arguments lets you build with different versions
without having to manually update the Dockerfile.
It also makes it easier to maintain the Dockerfile,
since it lets you declare versions at the top of the file.

Build arguments can also be a way to reuse a value in multiple places.
For example, if you use multiple flavors of `alpine` in your build,
you can ensure you're using the same version of `alpine` everywhere:

- `golang:1.22-alpine${ALPINE_VERSION}`
- `python:3.12-alpine${ALPINE_VERSION}`
- `nginx:1-alpine${ALPINE_VERSION}`

The following example defines the version of `node` and `alpine` using build arguments.

```dockerfile
# syntax=docker/dockerfile:1

ARG NODE_VERSION="24"
ARG ALPINE_VERSION="3.23"

FROM node:${NODE_VERSION}-alpine${ALPINE_VERSION} AS base
WORKDIR /src

FROM base AS build
COPY package*.json ./
RUN npm ci
RUN npm run build

FROM base AS production
COPY package*.json ./
RUN npm ci --omit=dev && npm cache clean --force
COPY --from=build /src/dist/ .
CMD ["node", "app.js"]
```

In this case, the build arguments have default values.
Specifying their values when you invoke a build is optional.
To override the defaults, you would use the `--build-arg` CLI flag:

```console
$ docker build --build-arg NODE_VERSION=current .
```

For more information on how to use build arguments, refer to:

- [ARGDockerfile reference](https://docs.docker.com/reference/dockerfile/#arg)
- [docker build --build-argreference](https://docs.docker.com/reference/cli/docker/buildx/build/#build-arg)

## ENVusage example

Declaring an environment variable with `ENV` makes the variable
available to all subsequent instructions in the build stage.
The following example shows an example setting `NODE_ENV` to `production`
before installing JavaScript dependencies with `npm`.
Setting the variable makes `npm` omits packages needed only for local development.

```dockerfile
# syntax=docker/dockerfile:1

FROM node:20
WORKDIR /app
COPY package*.json ./
ENV NODE_ENV=production
RUN npm ci && npm cache clean --force
COPY . .
CMD ["node", "app.js"]
```

Environment variables aren't configurable at build-time by default.
If you want to change the value of an `ENV` at build-time,
you can combine environment variables and build arguments:

```dockerfile
# syntax=docker/dockerfile:1

FROM node:20
ARG NODE_ENV=production
ENV NODE_ENV=$NODE_ENV
WORKDIR /app
COPY package*.json ./
RUN npm ci && npm cache clean --force
COPY . .
CMD ["node", "app.js"]
```

With this Dockerfile, you can use `--build-arg` to override the default value of `NODE_ENV`:

```console
$ docker build --build-arg NODE_ENV=development .
```

Note that, because the environment variables you set persist in containers,
using them can lead to unintended side-effects for the application's runtime.

For more information on how to use environment variables in builds, refer to:

- [ENVDockerfile reference](https://docs.docker.com/reference/dockerfile/#env)

## Scoping

Build arguments declared in the global scope of a Dockerfile
aren't automatically inherited into the build stages.
They're only accessible in the global scope.

```dockerfile
# syntax=docker/dockerfile:1

# The following build argument is declared in the global scope:
ARG NAME="joe"

FROM alpine
# The following instruction doesn't have access to the $NAME build argument
# because the argument was defined in the global scope, not for this stage.
RUN echo "hello ${NAME}!"
```

The `echo` command in this example evaluates to `hello !`
because the value of the `NAME` build argument is out of scope.
To inherit global build arguments into a stage, you must consume them:

```dockerfile
# syntax=docker/dockerfile:1

# Declare the build argument in the global scope
ARG NAME="joe"

FROM alpine
# Consume the build argument in the build stage
ARG NAME
RUN echo $NAME
```

Once a build argument is declared or consumed in a stage,
it's automatically inherited by child stages.

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine AS base
# Declare the build argument in the build stage
ARG NAME="joe"

# Create a new stage based on "base"
FROM base AS build
# The NAME build argument is available here
# since it's declared in a parent stage
RUN echo "hello $NAME!"
```

The following diagram further exemplifies how build argument
and environment variable inheritance works for multi-stage builds.

![image](https://docs.docker.com/build/images/build-variables.svg)

## Pre-defined build arguments

This section describes pre-defined build arguments available to all builds by default.

### Multi-platform build arguments

Multi-platform build arguments describe the build and target platforms for the build.

The build platform is the operating system, architecture, and platform variant
of the host system where the builder (the BuildKit daemon) is running.

- `BUILDPLATFORM`
- `BUILDOS`
- `BUILDARCH`
- `BUILDVARIANT`

The target platform arguments hold the same values for the target platforms for the build,
specified using the `--platform` flag for the `docker build` command.

- `TARGETPLATFORM`
- `TARGETOS`
- `TARGETARCH`
- `TARGETVARIANT`

These arguments are useful for doing cross-compilation in multi-platform builds.
They're available in the global scope of the Dockerfile,
but they aren't automatically inherited by build stages.
To use them inside stage, you must declare them:

```dockerfile
# syntax=docker/dockerfile:1

# Pre-defined build arguments are available in the global scope
FROM --platform=$BUILDPLATFORM golang
# To inherit them to a stage, declare them with ARG
ARG TARGETOS
RUN GOOS=$TARGETOS go build -o ./exe .
```

For more information about multi-platform build arguments, refer to
[Multi-platform arguments](https://docs.docker.com/reference/dockerfile/#automatic-platform-args-in-the-global-scope)

### Proxy arguments

Proxy build arguments let you specify proxies to use for your build.
You don't need to declare or reference these arguments in the Dockerfile.
Specifying a proxy with `--build-arg` is enough to make your build use the proxy.

Proxy arguments are automatically excluded from the build cache
and the output of `docker history` by default.
If you do reference the arguments in your Dockerfile,
the proxy configuration ends up in the build cache.

The builder respects the following proxy build arguments.
The variables are case insensitive.

- `HTTP_PROXY`
- `HTTPS_PROXY`
- `FTP_PROXY`
- `NO_PROXY`
- `ALL_PROXY`

To configure a proxy for your build:

```console
$ docker build --build-arg HTTP_PROXY=https://my-proxy.example.com .
```

For more information about proxy build arguments, refer to
[Proxy arguments](https://docs.docker.com/reference/dockerfile/#predefined-args).

## Build tool configuration variables

The following environment variables enable, disable, or change the behavior of Buildx and BuildKit.
Note that these variables aren't used to configure the build container;
they aren't available inside the build and they have no relation to the `ENV` instruction.
They're used to configure the Buildx client, or the BuildKit daemon.

| Variable | Type | Description |
| --- | --- | --- |
| BUILDKIT_COLORS | String | Configure text color for the terminal output. |
| BUILDKIT_HOST | String | Specify host to use for remote builders. |
| BUILDKIT_PROGRESS | String | Configure type of progress output. |
| BUILDKIT_TTY_LOG_LINES | String | Number of log lines (for active steps in TTY mode). |
| BUILDX_BAKE_FILE | String | Specify the build definition file(s) fordocker buildx bake. |
| BUILDX_BAKE_FILE_SEPARATOR | String | Specify the file-path separator forBUILDX_BAKE_FILE. |
| BUILDX_BAKE_GIT_AUTH_HEADER | String | HTTP authentication scheme for remote Bake files. |
| BUILDX_BAKE_GIT_AUTH_TOKEN | String | HTTP authentication token for remote Bake files. |
| BUILDX_BAKE_GIT_SSH | String | SSH authentication for remote Bake files. |
| BUILDX_BUILDER | String | Specify the builder instance to use. |
| BUILDX_CONFIG | String | Specify location for configuration, state, and logs. |
| BUILDX_CPU_PROFILE | String | Generate approfCPU profile at the specified location. |
| BUILDX_EXPERIMENTAL | Boolean | Turn on experimental features. |
| BUILDX_GIT_CHECK_DIRTY | Boolean | Enable dirty Git checkout detection. |
| BUILDX_GIT_INFO | Boolean | Remove Git information in provenance attestations. |
| BUILDX_GIT_LABELS | String | Boolean | Add Git provenance labels to images. |
| BUILDX_MEM_PROFILE | String | Generate approfmemory profile at the specified location. |
| BUILDX_METADATA_PROVENANCE | String | Boolean | Customize provenance information included in the metadata file. |
| BUILDX_METADATA_WARNINGS | String | Include build warnings in the metadata file. |
| BUILDX_NO_DEFAULT_ATTESTATIONS | Boolean | Turn off default provenance attestations. |
| BUILDX_NO_DEFAULT_LOAD | Boolean | Turn off loading images to image store by default. |
| EXPERIMENTAL_BUILDKIT_SOURCE_POLICY | String | Specify a BuildKit source policy file. |

BuildKit also supports a few additional configuration parameters. Refer to
[BuildKit built-in build args](https://docs.docker.com/reference/dockerfile/#buildkit-built-in-build-args).

You can express Boolean values for environment variables in different ways.
For example, `true`, `1`, and `T` all evaluate to true.
Evaluation is done using the `strconv.ParseBool` function in the Go standard library.
See the [reference documentation](https://pkg.go.dev/strconv#ParseBool) for details.

### BUILDKIT_COLORS

Changes the colors of the terminal output. Set `BUILDKIT_COLORS` to a CSV string
in the following format:

```console
$ export BUILDKIT_COLORS="run=123,20,245:error=yellow:cancel=blue:warning=white"
```

Color values can be any valid RGB hex code, or one of the
[BuildKit predefined colors](https://github.com/moby/buildkit/blob/master/util/progress/progressui/colors.go).

Setting `NO_COLOR` to anything turns off colorized output, as recommended by
[no-color.org](https://no-color.org/).

### BUILDKIT_HOST

Requires: Docker Buildx [0.9.0](https://github.com/docker/buildx/releases/tag/v0.9.0) and later

You use the `BUILDKIT_HOST` to specify the address of a BuildKit daemon to use
as a remote builder. This is the same as specifying the address as a positional
argument to `docker buildx create`.

Usage:

```console
$ export BUILDKIT_HOST=tcp://localhost:1234
$ docker buildx create --name=remote --driver=remote
```

If you specify both the `BUILDKIT_HOST` environment variable and a positional
argument, the argument takes priority.

### BUILDKIT_PROGRESS

Sets the type of the BuildKit progress output. Valid values are:

- `auto` (default): automatically uses `tty` in interactive terminals, `plain` otherwise
- `plain`: displays build steps sequentially in simple text format
- `tty`: interactive output with formatted progress bars and build steps
- `quiet`: suppresses progress output, only shows errors and final image ID
- `none`: no progress output, only shows errors
- `rawjson`: outputs build progress as raw JSON (useful for parsing by other tools)

Usage:

```console
$ export BUILDKIT_PROGRESS=plain
```

### BUILDKIT_TTY_LOG_LINES

You can change how many log lines are visible for active steps in TTY mode by
setting `BUILDKIT_TTY_LOG_LINES` to a number (default to `6`).

```console
$ export BUILDKIT_TTY_LOG_LINES=8
```

### EXPERIMENTAL_BUILDKIT_SOURCE_POLICY

Lets you specify a
[BuildKit source policy](https://github.com/moby/buildkit/blob/master/docs/build-repro.md#reproducing-the-pinned-dependencies)
file for creating reproducible builds with pinned dependencies.

```console
$ export EXPERIMENTAL_BUILDKIT_SOURCE_POLICY=./policy.json
```

Example:

```json
{
  "rules": [
    {
      "action": "CONVERT",
      "selector": {
        "identifier": "docker-image://docker.io/library/alpine:latest"
      },
      "updates": {
        "identifier": "docker-image://docker.io/library/alpine:latest@sha256:4edbd2beb5f78b1014028f4fbb99f3237d9561100b6881aabbf5acce2c4f9454"
      }
    },
    {
      "action": "CONVERT",
      "selector": {
        "identifier": "https://raw.githubusercontent.com/moby/buildkit/v0.10.1/README.md"
      },
      "updates": {
        "attrs": {"http.checksum": "sha256:6e4b94fc270e708e1068be28bd3551dc6917a4fc5a61293d51bb36e6b75c4b53"}
      }
    },
    {
      "action": "DENY",
      "selector": {
        "identifier": "docker-image://docker.io/library/golang*"
      }
    }
  ]
}
```

### BUILDX_BAKE_FILE

Requires: Docker Buildx [0.26.0](https://github.com/docker/buildx/releases/tag/v0.26.0) and later

Specify one or more build definition files for `docker buildx bake`.

This environment variable provides an alternative to the `-f` / `--file` command-line flag.

Multiple files can be specified by separating them with the system path separator (":" on Linux/macOS, ";" on Windows):

```console
export BUILDX_BAKE_FILE=file1.hcl:file2.hcl
```

Or with a custom separator defined by the [BUILDX_BAKE_FILE_SEPARATOR](#buildx_bake_file_separator) variable:

```console
export BUILDX_BAKE_FILE_SEPARATOR=@
export BUILDX_BAKE_FILE=file1.hcl@file2.hcl
```

If both `BUILDX_BAKE_FILE` and the `-f` flag are set, only the files provided via `-f` are used.

If a listed file does not exist or is invalid, bake returns an error.

### BUILDX_BAKE_FILE_SEPARATOR

Requires: Docker Buildx [0.26.0](https://github.com/docker/buildx/releases/tag/v0.26.0) and later

Controls the separator used between file paths in the `BUILDX_BAKE_FILE` environment variable.

This is useful if your file paths contain the default separator character or if you want to standardize separators across different platforms.

```console
export BUILDX_BAKE_PATH_SEPARATOR=@
export BUILDX_BAKE_FILE=file1.hcl@file2.hcl
```

### BUILDX_BAKE_GIT_AUTH_HEADER

Requires: Docker Buildx [0.14.0](https://github.com/docker/buildx/releases/tag/v0.14.0) and later

Sets the HTTP authentication scheme when using a remote Bake definition in a private Git repository.
This is equivalent to the [GIT_AUTH_HEADERsecret](https://docs.docker.com/build/building/secrets/#http-authentication-scheme),
but facilitates the pre-flight authentication in Bake when loading the remote Bake file.
Supported values are `bearer` (default) and `basic`.

Usage:

```console
$ export BUILDX_BAKE_GIT_AUTH_HEADER=basic
```

### BUILDX_BAKE_GIT_AUTH_TOKEN

Requires: Docker Buildx [0.14.0](https://github.com/docker/buildx/releases/tag/v0.14.0) and later

Sets the HTTP authentication token when using a remote Bake definition in a private Git repository.
This is equivalent to the [GIT_AUTH_TOKENsecret](https://docs.docker.com/build/building/secrets/#git-authentication-for-remote-contexts),
but facilitates the pre-flight authentication in Bake when loading the remote Bake file.

Usage:

```console
$ export BUILDX_BAKE_GIT_AUTH_TOKEN=$(cat git-token.txt)
```

### BUILDX_BAKE_GIT_SSH

Requires: Docker Buildx [0.14.0](https://github.com/docker/buildx/releases/tag/v0.14.0) and later

Lets you specify a list of SSH agent socket filepaths to forward to Bake
for authenticating to a Git server when using a remote Bake definition in a private repository.
This is similar to SSH mounts for builds, but facilitates the pre-flight authentication in Bake when resolving the build definition.

Setting this environment is typically not necessary, because Bake will use the `SSH_AUTH_SOCK` agent socket by default.
You only need to specify this variable if you want to use a socket with a different filepath.
This variable can take multiple paths using a comma-separated string.

Usage:

```console
$ export BUILDX_BAKE_GIT_SSH=/run/foo/listener.sock,~/.creds/ssh.sock
```

### BUILDX_BUILDER

Overrides the configured builder instance. Same as the `docker buildx --builder`
CLI flag.

Usage:

```console
$ export BUILDX_BUILDER=my-builder
```

### BUILDX_CONFIG

You can use `BUILDX_CONFIG` to specify the directory to use for build
configuration, state, and logs. The lookup order for this directory is as
follows:

- `$BUILDX_CONFIG`
- `$DOCKER_CONFIG/buildx`
- `~/.docker/buildx` (default)

Usage:

```console
$ export BUILDX_CONFIG=/usr/local/etc
```

### BUILDX_CPU_PROFILE

Requires: Docker Buildx [0.18.0](https://github.com/docker/buildx/releases/tag/v0.18.0) and later

If specified, Buildx generates a `pprof` CPU profile at the specified location.

> Note
>
> This property is only useful for when developing Buildx. The profiling data
> is not relevant for analyzing a build's performance.

Usage:

```console
$ export BUILDX_CPU_PROFILE=buildx_cpu.prof
```

### BUILDX_EXPERIMENTAL

Enables experimental build features.

Usage:

```console
$ export BUILDX_EXPERIMENTAL=1
```

### BUILDX_GIT_CHECK_DIRTY

Requires: Docker Buildx [0.10.4](https://github.com/docker/buildx/releases/tag/v0.10.4) and later

When set to true, checks for dirty state in source control information for
[provenance attestations](https://docs.docker.com/build/metadata/attestations/slsa-provenance/).

Usage:

```console
$ export BUILDX_GIT_CHECK_DIRTY=1
```

### BUILDX_GIT_INFO

Requires: Docker Buildx [0.10.0](https://github.com/docker/buildx/releases/tag/v0.10.0) and later

When set to false, removes source control information from
[provenance attestations](https://docs.docker.com/build/metadata/attestations/slsa-provenance/).

Usage:

```console
$ export BUILDX_GIT_INFO=0
```

### BUILDX_GIT_LABELS

Requires: Docker Buildx [0.10.0](https://github.com/docker/buildx/releases/tag/v0.10.0) and later

Adds provenance labels, based on Git information, to images that you build. The
labels are:

- `com.docker.image.source.entrypoint`: Location of the Dockerfile relative to
  the project root
- `org.opencontainers.image.revision`: Git commit revision
- `org.opencontainers.image.source`: SSH or HTTPS address of the repository

Example:

```json
"Labels": {
    "com.docker.image.source.entrypoint": "Dockerfile",
    "org.opencontainers.image.revision": "5734329c6af43c2ae295010778cd308866b95d9b",
    "org.opencontainers.image.source": "git@github.com:foo/bar.git"
  }
```

Usage:

- Set `BUILDX_GIT_LABELS=1` to include the `entrypoint` and `revision` labels.
- Set `BUILDX_GIT_LABELS=full` to include all labels.

If the repository is in a dirty state, the `revision` gets a `-dirty` suffix.

### BUILDX_MEM_PROFILE

Requires: Docker Buildx [0.18.0](https://github.com/docker/buildx/releases/tag/v0.18.0) and later

If specified, Buildx generates a `pprof` memory profile at the specified
location.

> Note
>
> This property is only useful for when developing Buildx. The profiling data
> is not relevant for analyzing a build's performance.

Usage:

```console
$ export BUILDX_MEM_PROFILE=buildx_mem.prof
```

### BUILDX_METADATA_PROVENANCE

Requires: Docker Buildx [0.14.0](https://github.com/docker/buildx/releases/tag/v0.14.0) and later

By default, Buildx includes minimal provenance information in the metadata file
through
[--metadata-fileflag](https://docs.docker.com/reference/cli/docker/buildx/build/#metadata-file).
This environment variable allows you to customize the provenance information
included in the metadata file:

- `min` sets minimal provenance (default).
- `max` sets full provenance.
- `disabled`, `false` or `0` does not set any provenance.

### BUILDX_METADATA_WARNINGS

Requires: Docker Buildx [0.16.0](https://github.com/docker/buildx/releases/tag/v0.16.0) and later

By default, Buildx does not include build warnings in the metadata file through
[--metadata-fileflag](https://docs.docker.com/reference/cli/docker/buildx/build/#metadata-file).
You can set this environment variable to `1` or `true` to include them.

### BUILDX_NO_DEFAULT_ATTESTATIONS

Requires: Docker Buildx [0.10.4](https://github.com/docker/buildx/releases/tag/v0.10.4) and later

By default, BuildKit v0.11 and later adds
[provenance attestations](https://docs.docker.com/build/metadata/attestations/slsa-provenance/) to images you
build. Set `BUILDX_NO_DEFAULT_ATTESTATIONS=1` to disable the default provenance
attestations.

Usage:

```console
$ export BUILDX_NO_DEFAULT_ATTESTATIONS=1
```

### BUILDX_NO_DEFAULT_LOAD

When you build an image using the `docker` driver, the image is automatically
loaded to the image store when the build finishes. Set `BUILDX_NO_DEFAULT_LOAD`
to disable automatic loading of images to the local container store.

Usage:

```console
$ export BUILDX_NO_DEFAULT_LOAD=1
```

---

# Configure BuildKit

> Learn how to configure BuildKit for your builder.

# Configure BuildKit

   Table of contents

---

If you create a `docker-container` or `kubernetes` builder with Buildx, you can
apply a custom [BuildKit configuration](https://docs.docker.com/build/buildkit/toml-configuration/) by passing the
[--buildkitd-configflag](https://docs.docker.com/reference/cli/docker/buildx/create/#buildkitd-config)
to the `docker buildx create` command.

## Registry mirror

You can define a registry mirror to use for your builds. Doing so redirects
BuildKit to pull images from a different hostname. The following steps exemplify
defining a mirror for `docker.io` (Docker Hub) to `mirror.gcr.io`.

1. Create a TOML at `/etc/buildkitd.toml` with the following content:
  ```toml
  debug = true
  [registry."docker.io"]
    mirrors = ["mirror.gcr.io"]
  ```
  > Note
  >
  > `debug = true` turns on debug requests in the BuildKit daemon, which logs a
  > message that shows when a mirror is being used.
2. Create a `docker-container` builder that uses this BuildKit configuration:
  ```console
  $ docker buildx create --use --bootstrap \
    --name mybuilder \
    --driver docker-container \
    --buildkitd-config /etc/buildkitd.toml
  ```
3. Build an image:
  ```bash
  docker buildx build --load . -f - <<EOF
  FROM alpine
  RUN echo "hello world"
  EOF
  ```

The BuildKit logs for this builder now shows that it uses the GCR mirror. You
can tell by the fact that the response messages include the `x-goog-*` HTTP
headers.

```console
$ docker logs buildx_buildkit_mybuilder0
```

```text
...
time="2022-02-06T17:47:48Z" level=debug msg="do request" request.header.accept="application/vnd.docker.container.image.v1+json, */*" request.header.user-agent=containerd/1.5.8+unknown request.method=GET spanID=9460e5b6e64cec91 traceID=b162d3040ddf86d6614e79c66a01a577
time="2022-02-06T17:47:48Z" level=debug msg="fetch response received" response.header.accept-ranges=bytes response.header.age=1356 response.header.alt-svc="h3=\":443\"; ma=2592000,h3-29=\":443\"; ma=2592000,h3-Q050=\":443\"; ma=2592000,h3-Q046=\":443\"; ma=2592000,h3-Q043=\":443\"; ma=2592000,quic=\":443\"; ma=2592000; v=\"46,43\"" response.header.cache-control="public, max-age=3600" response.header.content-length=1469 response.header.content-type=application/octet-stream response.header.date="Sun, 06 Feb 2022 17:25:17 GMT" response.header.etag="\"774380abda8f4eae9a149e5d5d3efc83\"" response.header.expires="Sun, 06 Feb 2022 18:25:17 GMT" response.header.last-modified="Wed, 24 Nov 2021 21:07:57 GMT" response.header.server=UploadServer response.header.x-goog-generation=1637788077652182 response.header.x-goog-hash="crc32c=V3DSrg==" response.header.x-goog-hash.1="md5=d0OAq9qPTq6aFJ5dXT78gw==" response.header.x-goog-metageneration=1 response.header.x-goog-storage-class=STANDARD response.header.x-goog-stored-content-encoding=identity response.header.x-goog-stored-content-length=1469 response.header.x-guploader-uploadid=ADPycduqQipVAXc3tzXmTzKQ2gTT6CV736B2J628smtD1iDytEyiYCgvvdD8zz9BT1J1sASUq9pW_ctUyC4B-v2jvhIxnZTlKg response.status="200 OK" spanID=9460e5b6e64cec91 traceID=b162d3040ddf86d6614e79c66a01a577
time="2022-02-06T17:47:48Z" level=debug msg="fetch response received" response.header.accept-ranges=bytes response.header.age=760 response.header.alt-svc="h3=\":443\"; ma=2592000,h3-29=\":443\"; ma=2592000,h3-Q050=\":443\"; ma=2592000,h3-Q046=\":443\"; ma=2592000,h3-Q043=\":443\"; ma=2592000,quic=\":443\"; ma=2592000; v=\"46,43\"" response.header.cache-control="public, max-age=3600" response.header.content-length=1471 response.header.content-type=application/octet-stream response.header.date="Sun, 06 Feb 2022 17:35:13 GMT" response.header.etag="\"35d688bd15327daafcdb4d4395e616a8\"" response.header.expires="Sun, 06 Feb 2022 18:35:13 GMT" response.header.last-modified="Wed, 24 Nov 2021 21:07:12 GMT" response.header.server=UploadServer response.header.x-goog-generation=1637788032100793 response.header.x-goog-hash="crc32c=aWgRjA==" response.header.x-goog-hash.1="md5=NdaIvRUyfar8201DleYWqA==" response.header.x-goog-metageneration=1 response.header.x-goog-storage-class=STANDARD response.header.x-goog-stored-content-encoding=identity response.header.x-goog-stored-content-length=1471 response.header.x-guploader-uploadid=ADPycdtR-gJYwC7yHquIkJWFFG8FovDySvtmRnZBqlO3yVDanBXh_VqKYt400yhuf0XbQ3ZMB9IZV2vlcyHezn_Pu3a1SMMtiw response.status="200 OK" spanID=9460e5b6e64cec91 traceID=b162d3040ddf86d6614e79c66a01a577
time="2022-02-06T17:47:48Z" level=debug msg=fetch spanID=9460e5b6e64cec91 traceID=b162d3040ddf86d6614e79c66a01a577
time="2022-02-06T17:47:48Z" level=debug msg=fetch spanID=9460e5b6e64cec91 traceID=b162d3040ddf86d6614e79c66a01a577
time="2022-02-06T17:47:48Z" level=debug msg=fetch spanID=9460e5b6e64cec91 traceID=b162d3040ddf86d6614e79c66a01a577
time="2022-02-06T17:47:48Z" level=debug msg=fetch spanID=9460e5b6e64cec91 traceID=b162d3040ddf86d6614e79c66a01a577
time="2022-02-06T17:47:48Z" level=debug msg="do request" request.header.accept="application/vnd.docker.image.rootfs.diff.tar.gzip, */*" request.header.user-agent=containerd/1.5.8+unknown request.method=GET spanID=9460e5b6e64cec91 traceID=b162d3040ddf86d6614e79c66a01a577
time="2022-02-06T17:47:48Z" level=debug msg="fetch response received" response.header.accept-ranges=bytes response.header.age=1356 response.header.alt-svc="h3=\":443\"; ma=2592000,h3-29=\":443\"; ma=2592000,h3-Q050=\":443\"; ma=2592000,h3-Q046=\":443\"; ma=2592000,h3-Q043=\":443\"; ma=2592000,quic=\":443\"; ma=2592000; v=\"46,43\"" response.header.cache-control="public, max-age=3600" response.header.content-length=2818413 response.header.content-type=application/octet-stream response.header.date="Sun, 06 Feb 2022 17:25:17 GMT" response.header.etag="\"1d55e7be5a77c4a908ad11bc33ebea1c\"" response.header.expires="Sun, 06 Feb 2022 18:25:17 GMT" response.header.last-modified="Wed, 24 Nov 2021 21:07:06 GMT" response.header.server=UploadServer response.header.x-goog-generation=1637788026431708 response.header.x-goog-hash="crc32c=ZojF+g==" response.header.x-goog-hash.1="md5=HVXnvlp3xKkIrRG8M+vqHA==" response.header.x-goog-metageneration=1 response.header.x-goog-storage-class=STANDARD response.header.x-goog-stored-content-encoding=identity response.header.x-goog-stored-content-length=2818413 response.header.x-guploader-uploadid=ADPycdsebqxiTBJqZ0bv9zBigjFxgQydD2ESZSkKchpE0ILlN9Ibko3C5r4fJTJ4UR9ddp-UBd-2v_4eRpZ8Yo2llW_j4k8WhQ response.status="200 OK" spanID=9460e5b6e64cec91 traceID=b162d3040ddf86d6614e79c66a01a577
...
```

## Setting registry certificates

If you specify registry certificates in the BuildKit configuration, the daemon
copies the files into the container under `/etc/buildkit/certs`. The following
steps show adding a self-signed registry certificate to the BuildKit
configuration.

1. Add the following configuration to `/etc/buildkitd.toml`:
  ```toml
  # /etc/buildkitd.toml
  debug = true
  [registry."myregistry.com"]
    ca=["/etc/certs/myregistry.pem"]
    [[registry."myregistry.com".keypair]]
      key="/etc/certs/myregistry_key.pem"
      cert="/etc/certs/myregistry_cert.pem"
  ```
  This tells the builder to push images to the `myregistry.com` registry using
  the certificates in the specified location (`/etc/certs`).
2. Create a `docker-container` builder that uses this configuration:
  ```console
  $ docker buildx create --use --bootstrap \
    --name mybuilder \
    --driver docker-container \
    --buildkitd-config /etc/buildkitd.toml
  ```
3. Inspect the builder's configuration file (`/etc/buildkit/buildkitd.toml`), it
  shows that the certificate configuration is now configured in the builder.
  ```console
  $ docker exec -it buildx_buildkit_mybuilder0 cat /etc/buildkit/buildkitd.toml
  ```
  ```toml
  debug = true
  [registry]
    [registry."myregistry.com"]
      ca = ["/etc/buildkit/certs/myregistry.com/myregistry.pem"]
      [[registry."myregistry.com".keypair]]
        cert = "/etc/buildkit/certs/myregistry.com/myregistry_cert.pem"
        key = "/etc/buildkit/certs/myregistry.com/myregistry_key.pem"
  ```
4. Verify that the certificates are inside the container:
  ```console
  $ docker exec -it buildx_buildkit_mybuilder0 ls /etc/buildkit/certs/myregistry.com/
  myregistry.pem    myregistry_cert.pem   myregistry_key.pem
  ```

Now you can push to the registry using this builder, and it will authenticate
using the certificates:

```console
$ docker buildx build --push --tag myregistry.com/myimage:latest .
```

## CNI networking

CNI networking for builders can be useful for dealing with network port
contention during concurrent builds. CNI is [not yet](https://github.com/moby/buildkit/issues/28)
available in the default BuildKit image. But you can create your own image that
includes CNI support.

The following Dockerfile example shows a custom BuildKit image with CNI support.
It uses the [CNI config for integration tests](https://github.com/moby/buildkit/blob/master//hack/fixtures/cni.json)
in BuildKit as an example. Feel free to include your own CNI configuration.

```dockerfile
# syntax=docker/dockerfile:1

ARG BUILDKIT_VERSION=v0.27.0
ARG CNI_VERSION=v1.0.1

FROM --platform=$BUILDPLATFORM alpine AS cni-plugins
RUN apk add --no-cache curl
ARG CNI_VERSION
ARG TARGETOS
ARG TARGETARCH
WORKDIR /opt/cni/bin
RUN curl -Ls https://github.com/containernetworking/plugins/releases/download/$CNI_VERSION/cni-plugins-$TARGETOS-$TARGETARCH-$CNI_VERSION.tgz | tar xzv

FROM moby/buildkit:${BUILDKIT_VERSION}
ARG BUILDKIT_VERSION
RUN apk add --no-cache iptables
COPY --from=cni-plugins /opt/cni/bin /opt/cni/bin
ADD https://raw.githubusercontent.com/moby/buildkit/${BUILDKIT_VERSION}/hack/fixtures/cni.json /etc/buildkit/cni.json
```

Now you can build this image, and create a builder instance from it using
[the--driver-opt imageoption](https://docs.docker.com/reference/cli/docker/buildx/create/#driver-opt):

```console
$ docker buildx build --tag buildkit-cni:local --load .
$ docker buildx create --use --bootstrap \
  --name mybuilder \
  --driver docker-container \
  --driver-opt "image=buildkit-cni:local" \
  --buildkitd-flags "--oci-worker-net=cni"
```

## Resource limiting

### Max parallelism

You can limit the parallelism of the BuildKit solver, which is particularly useful
for low-powered machines, using a [BuildKit configuration](https://docs.docker.com/build/buildkit/toml-configuration/)
while creating a builder with the
[--buildkitd-configflag](https://docs.docker.com/reference/cli/docker/buildx/create/#buildkitd-config).

```toml
# /etc/buildkitd.toml
[worker.oci]
  max-parallelism = 4
```

Now you can
[create adocker-containerbuilder](https://docs.docker.com/build/builders/drivers/docker-container/)
that will use this BuildKit configuration to limit parallelism.

```console
$ docker buildx create --use \
  --name mybuilder \
  --driver docker-container \
  --buildkitd-config /etc/buildkitd.toml
```

### TCP connection limit

TCP connections are limited to 4 simultaneous connections per registry for
pulling and pushing images, plus one additional connection dedicated to metadata
requests. This connection limit prevents your build from getting stuck while
pulling images. The dedicated metadata connection helps reduce the overall build
time.

More information: [moby/buildkit#2259](https://github.com/moby/buildkit/pull/2259)

---

# Search code, repositories, users, issues, pull requests...

> concurrent, cache-efficient, and Dockerfile-agnostic builder toolkit - Releases · moby/buildkit

Welcome to the v0.27.1 release of buildkit!

Please try out the release binaries and report any issues at
 [https://github.com/moby/buildkit/issues](https://github.com/moby/buildkit/issues).

### Contributors

- CrazyMax
- Sebastiaan van Stijn
- Tõnis Tiigi

### Notable Changes

- Fix possible panic when verifying signature of GitHub Actions cache [moby/policy-helpers#21](https://github.com/moby/policy-helpers/pull/21)

### Dependency Changes

- **github.com/klauspost/compress**   v1.18.2 -> v1.18.3
- **github.com/moby/policy-helpers**  9fcc1a9ec5c9 -> eeebf1a0ab2b

Previous release can be found at [v0.27.0](https://github.com/moby/buildkit/releases/tag/v0.27.0)

---

# Custom Dockerfile syntax

> Dive deep into the Dockerfile frontend, and learn about custom frontends

# Custom Dockerfile syntax

   Table of contents

---

## Dockerfile frontend

BuildKit supports loading frontends dynamically from container images. To use
an external Dockerfile frontend, the first line of your
[Dockerfile](https://docs.docker.com/reference/dockerfile/)
needs to set the
[syntaxdirective](https://docs.docker.com/reference/dockerfile/#syntax)
pointing to the specific image you want to use:

```dockerfile
# syntax=[remote image reference]
```

For example:

```dockerfile
# syntax=docker/dockerfile:1
# syntax=docker.io/docker/dockerfile:1
# syntax=example.com/user/repo:tag@sha256:abcdef...
```

You can also use the predefined `BUILDKIT_SYNTAX` build argument to set the
frontend image reference on the command line:

```console
$ docker build --build-arg BUILDKIT_SYNTAX=docker/dockerfile:1 .
```

This defines the location of the Dockerfile syntax that is used to build the
Dockerfile. The BuildKit backend allows seamlessly using external
implementations that are distributed as Docker images and execute inside a
container sandbox environment.

Custom Dockerfile implementations allow you to:

- Automatically get bug fixes without updating the Docker daemon
- Make sure all users are using the same implementation to build your Dockerfile
- Use the latest features without updating the Docker daemon
- Try out new features or third-party features before they are integrated in the Docker daemon
- Use [alternative build definitions, or create your own](https://github.com/moby/buildkit#exploring-llb)
- Build your own Dockerfile frontend with custom features

> Note
>
> BuildKit ships with a built-in Dockerfile frontend, but it's recommended
> to use an external image to make sure that all users use the same version on
> the builder and to pick up bug fixes automatically without waiting for a new
> version of BuildKit or Docker Engine.

## Official releases

Docker distributes official versions of the images that can be used for building
Dockerfiles under `docker/dockerfile` repository on Docker Hub. There are two
channels where new images are released: `stable` and `labs`.

### Stable channel

The `stable` channel follows [semantic versioning](https://semver.org).
For example:

- `docker/dockerfile:1` - kept updated with the latest `1.x.x` minor *and* patch
  release.
- `docker/dockerfile:1.2` - kept updated with the latest `1.2.x` patch release,
  and stops receiving updates once version `1.3.0` is released.
- `docker/dockerfile:1.2.1` - immutable: never updated.

We recommend using `docker/dockerfile:1`, which always points to the latest
stable release of the version 1 syntax, and receives both "minor" and "patch"
updates for the version 1 release cycle. BuildKit automatically checks for
updates of the syntax when performing a build, making sure you are using the
most current version.

If a specific version is used, such as `1.2` or `1.2.1`, the Dockerfile needs
to be updated manually to continue receiving bugfixes and new features. Old
versions of the Dockerfile remain compatible with the new versions of the
builder.

### Labs channel

The `labs` channel provides early access to Dockerfile features that are not yet
available in the `stable` channel. `labs` images are released at the same time
as stable releases, and follow the same version pattern, but use the `-labs`
suffix, for example:

- `docker/dockerfile:labs` - latest release on `labs` channel.
- `docker/dockerfile:1-labs` - same as `dockerfile:1`, with experimental
  features enabled.
- `docker/dockerfile:1.2-labs` - same as `dockerfile:1.2`, with experimental
  features enabled.
- `docker/dockerfile:1.2.1-labs` - immutable: never updated. Same as
  `dockerfile:1.2.1`, with experimental features enabled.

Choose a channel that best fits your needs. If you want to benefit from
new features, use the `labs` channel. Images in the `labs` channel contain
all the features in the `stable` channel, plus early access features.
Stable features in the `labs` channel follow [semantic versioning](https://semver.org),
but early access features don't, and newer releases may not be backwards
compatible. Pin the version to avoid having to deal with breaking changes.

## Other resources

For documentation on `labs` features, master builds, and nightly feature
releases, refer to the description in [the BuildKit source repository on GitHub](https://github.com/moby/buildkit/blob/master/README.md).
For a full list of available images, visit the [docker/dockerfilerepository on Docker Hub](https://hub.docker.com/r/docker/dockerfile),
and the [docker/dockerfile-upstreamrepository on Docker Hub](https://hub.docker.com/r/docker/dockerfile-upstream)
for development builds.
