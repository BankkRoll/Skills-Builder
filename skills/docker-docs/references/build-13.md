# Build context and more

# Build context

> Learn how to use the build context to access files from your Dockerfile

# Build context

   Table of contents

---

The `docker build` and `docker buildx build` commands build Docker images from
a
[Dockerfile](https://docs.docker.com/reference/dockerfile/) and a context.

## What is a build context?

The build context is the set of files that your build can access.
The positional argument that you pass to the build command specifies the
context that you want to use for the build:

```console
$ docker build [OPTIONS] PATH | URL | -
                         ^^^^^^^^^^^^^^
```

You can pass any of the following inputs as the context for a build:

- The relative or absolute path to a local directory
- A remote URL of a Git repository, tarball, or plain-text file
- A plain-text file or tarball piped to the `docker build` command through standard input

### Filesystem contexts

When your build context is a local directory, a remote Git repository, or a tar
file, then that becomes the set of files that the builder can access during the
build. Build instructions such as `COPY` and `ADD` can refer to any of the
files and directories in the context.

A filesystem build context is processed recursively:

- When you specify a local directory or a tarball, all subdirectories are included
- When you specify a remote Git repository, the repository and all submodules are included

For more information about the different types of filesystem contexts that you
can use with your builds, see:

- [Local files](#local-context)
- [Git repositories](#git-repositories)
- [Remote tarballs](#remote-tarballs)

### Text file contexts

When your build context is a plain-text file, the builder interprets the file
as a Dockerfile. With this approach, the build doesn't use a filesystem context.

For more information, see [empty build context](#empty-context).

## Local context

To use a local build context, you can specify a relative or absolute filepath
to the `docker build` command. The following example shows a build command that
uses the current directory (`.`) as a build context:

```console
$ docker build .
...
#16 [internal] load build context
#16 sha256:23ca2f94460dcbaf5b3c3edbaaa933281a4e0ea3d92fe295193e4df44dc68f85
#16 transferring context: 13.16MB 2.2s done
...
```

This makes files and directories in the current working directory available to
the builder. The builder loads the files it needs from the build context when
needed.

You can also use local tarballs as build context, by piping the tarball
contents to the `docker build` command. See [Tarballs](#local-tarballs).

### Local directories

Consider the following directory structure:

```text
.
├── index.ts
├── src/
├── Dockerfile
├── package.json
└── package-lock.json
```

Dockerfile instructions can reference and include these files in the build if
you pass this directory as a context.

```dockerfile
# syntax=docker/dockerfile:1
FROM node:latest
WORKDIR /src
COPY package.json package-lock.json .
RUN npm ci
COPY index.ts src .
```

```console
$ docker build .
```

### Local context with Dockerfile from stdin

Use the following syntax to build an image using files on your local
filesystem, while using a Dockerfile from stdin.

```console
$ docker build -f- PATH
```

The syntax uses the -f (or --file) option to specify the Dockerfile to use, and
it uses a hyphen (-) as filename to instruct Docker to read the Dockerfile from
stdin.

The following example uses the current directory (.) as the build context, and
builds an image using a Dockerfile passed through stdin using a here-document.

```bash
# create a directory to work in
mkdir example
cd example

# create an example file
touch somefile.txt

# build an image using the current directory as context
# and a Dockerfile passed through stdin
docker build -t myimage:latest -f- . <<EOF
FROM busybox
COPY somefile.txt ./
RUN cat /somefile.txt
EOF
```

### Local tarballs

When you pipe a tarball to the build command, the build uses the contents of
the tarball as a filesystem context.

For example, given the following project directory:

```text
.
├── Dockerfile
├── Makefile
├── README.md
├── main.c
├── scripts
├── src
└── test.Dockerfile
```

You can create a tarball of the directory and pipe it to the build for use as
a context:

```console
$ tar czf foo.tar.gz *
$ docker build - < foo.tar.gz
```

The build resolves the Dockerfile from the tarball context. You can use the
`--file` flag to specify the name and location of the Dockerfile relative to
the root of the tarball. The following command builds using `test.Dockerfile`
in the tarball:

```console
$ docker build --file test.Dockerfile - < foo.tar.gz
```

## Remote context

You can specify the address of a remote Git repository, tarball, or plain-text
file as your build context.

- For Git repositories, the builder automatically clones the repository. See
  [Git repositories](#git-repositories).
- For tarballs, the builder downloads and extracts the contents of the tarball.
  See [Tarballs](#remote-tarballs).

If the remote tarball is a text file, the builder receives no [filesystem
context](#filesystem-contexts), and instead assumes that the remote
file is a Dockerfile. See [Empty build context](#empty-context).

### Git repositories

When you pass a URL pointing to the location of a Git repository as an argument
to `docker build`, the builder uses the repository as the build context.

The builder performs a shallow clone of the repository, downloading only
the HEAD commit, not the entire history.

The builder recursively clones the repository and any submodules it contains.

```console
$ docker build https://github.com/user/myrepo.git
```

By default, the builder clones the latest commit on the default branch of the
repository that you specify.

#### URL fragments

You can append URL fragments to the Git repository address to make the builder
clone a specific branch, tag, and subdirectory of a repository.

The format of the URL fragment is `#ref:dir`, where:

- `ref` is the name of the branch, tag, or commit hash
- `dir` is a subdirectory inside the repository

For example, the following command uses the `container` branch,
and the `docker` subdirectory in that branch, as the build context:

```console
$ docker build https://github.com/user/myrepo.git#container:docker
```

The following table represents all the valid suffixes with their build
contexts:

| Build Syntax Suffix | Commit Used | Build Context Used |
| --- | --- | --- |
| myrepo.git | refs/heads/<default branch> | / |
| myrepo.git#mytag | refs/tags/mytag | / |
| myrepo.git#mybranch | refs/heads/mybranch | / |
| myrepo.git#pull/42/head | refs/pull/42/head | / |
| myrepo.git#:myfolder | refs/heads/<default branch> | /myfolder |
| myrepo.git#master:myfolder | refs/heads/master | /myfolder |
| myrepo.git#mytag:myfolder | refs/tags/mytag | /myfolder |
| myrepo.git#mybranch:myfolder | refs/heads/mybranch | /myfolder |

When you use a commit hash as the `ref` in the URL fragment, use the full,
40-character string SHA-1 hash of the commit. A short hash, for example a hash
truncated to 7 characters, is not supported.

```bash
# ✅ The following works:
docker build github.com/docker/buildx#d4f088e689b41353d74f1a0bfcd6d7c0b213aed2
# ❌ The following doesn't work because the commit hash is truncated:
docker build github.com/docker/buildx#d4f088e
```

#### URL queries

Requires: Docker Buildx [0.28.0](https://github.com/docker/buildx/releases/tag/v0.28.0) and later, Dockerfile [1.18.0](https://github.com/moby/buildkit/releases/tag/dockerfile%2F1.18.0) and later, and Docker Desktop
[4.46.0](https://docs.docker.com/desktop/release-notes/#4460) and later

URL queries are more structured and recommended over [URL fragments](#url-fragments):

```console
$ docker buildx build 'https://github.com/user/myrepo.git?branch=container&subdir=docker'
```

| Build syntax suffix | Commit used | Build context used |
| --- | --- | --- |
| myrepo.git | refs/heads/<default branch> | / |
| myrepo.git?tag=mytag | refs/tags/mytag | / |
| myrepo.git?branch=mybranch | refs/heads/mybranch | / |
| myrepo.git?ref=pull/42/head | refs/pull/42/head | / |
| myrepo.git?subdir=myfolder | refs/heads/<default branch> | /myfolder |
| myrepo.git?branch=master&subdir=myfolder | refs/heads/master | /myfolder |
| myrepo.git?tag=mytag&subdir=myfolder | refs/tags/mytag | /myfolder |
| myrepo.git?branch=mybranch&subdir=myfolder | refs/heads/mybranch | /myfolder |

A commit hash can be specified as a `checksum` (alias `commit`) query, along with
`tag`, `branch`, or `ref` queries to verify that the reference resolves to the
expected commit:

```console
$ docker buildx build 'https://github.com/moby/buildkit.git?tag=v0.21.1&checksum=66735c67'
```

If it doesn't match, the build fails:

```console
$ docker buildx build 'https://github.com/user/myrepo.git?tag=v0.1.0&commit=deadbeef'
...
#3 [internal] load git source https://github.com/user/myrepo.git?tag=v0.1.0-rc1&commit=deadbeef
#3 0.484 bb41e835b6c3523c7c45b248cf4b45e7f862bc42       refs/tags/v0.1.0
#3 ERROR: expected checksum to match deadbeef, got bb41e835b6c3523c7c45b248cf4b45e7f862bc42
```

> Note
>
> Short commit hash is supported with `checksum` (alias `commit`) query but for
> `ref`, only the full hash of the commit is supported.

#### Keep.gitdirectory

By default, BuildKit doesn't keep the `.git` directory when using Git contexts.
You can configure BuildKit to keep the directory by setting the
[BUILDKIT_CONTEXT_KEEP_GIT_DIRbuild argument](https://docs.docker.com/reference/dockerfile/#buildkit-built-in-build-args).
This can be useful to if you want to retrieve Git information during your build:

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
WORKDIR /src
RUN --mount=target=. \
  make REVISION=$(git rev-parse HEAD) build
```

```console
$ docker build \
  --build-arg BUILDKIT_CONTEXT_KEEP_GIT_DIR=1
  https://github.com/user/myrepo.git#main
```

#### Private repositories

When you specify a Git context that's also a private repository, the builder
needs you to provide the necessary authentication credentials. You can use
either SSH or token-based authentication.

Buildx automatically detects and uses SSH credentials if the Git context you
specify is an SSH or Git address. By default, this uses `$SSH_AUTH_SOCK`.
You can configure the SSH credentials to use with the
[--sshflag](https://docs.docker.com/reference/cli/docker/buildx/build/#ssh).

```console
$ docker buildx build --ssh default git@github.com:user/private.git
```

If you want to use token-based authentication instead, you can pass the token
using the
[--secretflag](https://docs.docker.com/reference/cli/docker/buildx/build/#secret).

```console
$ GIT_AUTH_TOKEN=<token> docker buildx build \
  --secret id=GIT_AUTH_TOKEN \
  https://github.com/user/private.git
```

> Note
>
> Don't use `--build-arg` for secrets.

### Remote context with Dockerfile from stdin

Use the following syntax to build an image using files on your local
filesystem, while using a Dockerfile from stdin.

```console
$ docker build -f- URL
```

The syntax uses the -f (or --file) option to specify the Dockerfile to use, and
it uses a hyphen (-) as filename to instruct Docker to read the Dockerfile from
stdin.

This can be useful in situations where you want to build an image from a
repository that doesn't contain a Dockerfile. Or if you want to build with a
custom Dockerfile, without maintaining your own fork of the repository.

The following example builds an image using a Dockerfile from stdin, and adds
the `hello.c` file from the [hello-world](https://github.com/docker-library/hello-world)
repository on GitHub.

```bash
docker build -t myimage:latest -f- https://github.com/docker-library/hello-world.git <<EOF
FROM busybox
COPY hello.c ./
EOF
```

### Remote tarballs

If you pass the URL to a remote tarball, the URL itself is sent to the builder.

```console
$ docker build http://server/context.tar.gz
#1 [internal] load remote build context
#1 DONE 0.2s

#2 copy /context /
#2 DONE 0.1s
...
```

The download operation will be performed on the host where the BuildKit daemon
is running. Note that if you're using a remote Docker context or a remote
builder, that's not necessarily the same machine as where you issue the build
command. BuildKit fetches the `context.tar.gz` and uses it as the build
context. Tarball contexts must be tar archives conforming to the standard `tar`
Unix format and can be compressed with any one of the `xz`, `bzip2`, `gzip` or
`identity` (no compression) formats.

## Empty context

When you use a text file as the build context, the builder interprets the file
as a Dockerfile. Using a text file as context means that the build has no
filesystem context.

You can build with an empty build context when your Dockerfile doesn't depend
on any local files.

### How to build without a context

You can pass the text file using a standard input stream, or by pointing at the
URL of a remote text file.

```console
$ docker build - < Dockerfile
```

```powershell
Get-Content Dockerfile | docker build -
```

```bash
docker build -t myimage:latest - <<EOF
FROM busybox
RUN echo "hello world"
EOF
```

```console
$ docker build https://raw.githubusercontent.com/dvdksn/clockbox/main/Dockerfile
```

When you build without a filesystem context, Dockerfile instructions such as
`COPY` can't refer to local files:

```console
$ ls
main.c
$ docker build -<<< $'FROM scratch\nCOPY main.c .'
[+] Building 0.0s (4/4) FINISHED
 => [internal] load build definition from Dockerfile       0.0s
 => => transferring dockerfile: 64B                        0.0s
 => [internal] load .dockerignore                          0.0s
 => => transferring context: 2B                            0.0s
 => [internal] load build context                          0.0s
 => => transferring context: 2B                            0.0s
 => ERROR [1/1] COPY main.c .                              0.0s
------
 > [1/1] COPY main.c .:
------
Dockerfile:2
--------------------
   1 |     FROM scratch
   2 | >>> COPY main.c .
   3 |
--------------------
ERROR: failed to solve: failed to compute cache key: failed to calculate checksum of ref 7ab2bb61-0c28-432e-abf5-a4c3440bc6b6::4lgfpdf54n5uqxnv9v6ymg7ih: "/main.c": not found
```

## .dockerignore files

You can use a `.dockerignore` file to exclude files or directories from the
build context.

```text
# .dockerignore
node_modules
bar
```

This helps avoid sending unwanted files and directories to the builder,
improving build speed, especially when using a remote builder.

### Filename and location

When you run a build command, the build client looks for a file named
`.dockerignore` in the root directory of the context. If this file exists, the
files and directories that match patterns in the files are removed from the
build context before it's sent to the builder.

If you use multiple Dockerfiles, you can use different ignore-files for each
Dockerfile. You do so using a special naming convention for the ignore-files.
Place your ignore-file in the same directory as the Dockerfile, and prefix the
ignore-file with the name of the Dockerfile, as shown in the following example.

```text
.
├── index.ts
├── src/
├── docker
│   ├── build.Dockerfile
│   ├── build.Dockerfile.dockerignore
│   ├── lint.Dockerfile
│   ├── lint.Dockerfile.dockerignore
│   ├── test.Dockerfile
│   └── test.Dockerfile.dockerignore
├── package.json
└── package-lock.json
```

A Dockerfile-specific ignore-file takes precedence over the `.dockerignore`
file at the root of the build context if both exist.

### Syntax

The `.dockerignore` file is a newline-separated list of patterns similar to the
file globs of Unix shells. Leading and trailing slashes in ignore patterns are
disregarded. The following patterns all exclude a file or directory named `bar`
in the subdirectory `foo` under the root of the build context:

- `/foo/bar/`
- `/foo/bar`
- `foo/bar/`
- `foo/bar`

If a line in `.dockerignore` file starts with `#` in column 1, then this line
is considered as a comment and is ignored before interpreted by the CLI.

```gitignore
#/this/is/a/comment
```

If you're interested in learning the precise details of the `.dockerignore`
pattern matching logic, check out the
[moby/patternmatcher repository](https://github.com/moby/patternmatcher/tree/main/ignorefile)
on GitHub, which contains the source code.

#### Matching

The following code snippet shows an example `.dockerignore` file.

```text
# comment
*/temp*
*/*/temp*
temp?
```

This file causes the following build behavior:

| Rule | Behavior |
| --- | --- |
| # comment | Ignored. |
| */temp* | Exclude files and directories whose names start withtempin any immediate subdirectory of the root. For example, the plain file/somedir/temporary.txtis excluded, as is the directory/somedir/temp. |
| */*/temp* | Exclude files and directories starting withtempfrom any subdirectory that is two levels below the root. For example,/somedir/subdir/temporary.txtis excluded. |
| temp? | Exclude files and directories in the root directory whose names are a one-character extension oftemp. For example,/tempaand/tempbare excluded. |

Matching is done using Go's
[filepath.Matchfunction](https://golang.org/pkg/path/filepath#Match) rules.
A preprocessing step uses Go's
[filepath.Cleanfunction](https://golang.org/pkg/path/filepath/#Clean)
to trim whitespace and remove `.` and `..`.
Lines that are blank after preprocessing are ignored.

> Note
>
> For historical reasons, the pattern `.` is ignored.

Beyond Go's `filepath.Match` rules, Docker also supports a special wildcard
string `**` that matches any number of directories (including zero). For
example, `**/*.go` excludes all files that end with `.go` found anywhere in the
build context.

You can use the `.dockerignore` file to exclude the `Dockerfile` and
`.dockerignore` files. These files are still sent to the builder as they're
needed for running the build. But you can't copy the files into the image using
`ADD`, `COPY`, or bind mounts.

#### Negating matches

You can prepend lines with a `!` (exclamation mark) to make exceptions to
exclusions. The following is an example `.dockerignore` file that uses this
mechanism:

```text
*.md
!README.md
```

All markdown files right under the context directory *except* `README.md` are
excluded from the context. Note that markdown files under subdirectories are
still included.

The placement of `!` exception rules influences the behavior: the last line of
the `.dockerignore` that matches a particular file determines whether it's
included or excluded. Consider the following example:

```text
*.md
!README*.md
README-secret.md
```

No markdown files are included in the context except README files other than
`README-secret.md`.

Now consider this example:

```text
*.md
README-secret.md
!README*.md
```

All of the README files are included. The middle line has no effect because
`!README*.md` matches `README-secret.md` and comes last.

## Named contexts

In addition to the default build context (the positional argument to the
`docker build` command), you can also pass additional named contexts to builds.

Named contexts are specified using the `--build-context` flag, followed by a
name-value pair. This lets you include files and directories from multiple
sources during the build, while keeping them logically separated.

```console
$ docker build --build-context docs=./docs .
```

In this example:

- The named `docs` context points to the `./docs` directory.
- The default context (`.`) points to the current working directory.

### Using named contexts in a Dockerfile

Dockerfile instructions can reference named contexts as if they are stages in a
multi-stage build.

For example, the following Dockerfile:

1. Uses a `COPY` instruction to copy files from the default context into the
  current build stage.
2. Bind mounts the files in a named context to process the files as part of the
  build.

```dockerfile
# syntax=docker/dockerfile:1
FROM buildbase
WORKDIR /app

# Copy all files from the default context into /app/src in the build container
COPY . /app/src
RUN make bin

# Mount the files from the named "docs" context to build the documentation
RUN --mount=from=docs,target=/app/docs \
    make manpages
```

### Use cases for named contexts

Using named contexts allows for greater flexibility and efficiency when
building Docker images. Here are some scenarios where using named contexts can
be useful:

#### Example: combine local and remote sources

You can define separate named contexts for different types of sources. For
example, consider a project where the application source code is local, but the
deployment scripts are stored in a Git repository:

```console
$ docker build --build-context scripts=https://github.com/user/deployment-scripts.git .
```

In the Dockerfile, you can use these contexts independently:

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine:latest

# Copy application code from the main context
COPY . /opt/app

# Run deployment scripts using the remote "scripts" context
RUN --mount=from=scripts,target=/scripts /scripts/main.sh
```

#### Example: dynamic builds with custom dependencies

In some scenarios, you might need to dynamically inject configuration files or
dependencies into the build from external sources. Named contexts make this
straightforward by allowing you to mount different configurations without
modifying the default build context.

```console
$ docker build --build-context config=./configs/prod .
```

Example Dockerfile:

```dockerfile
# syntax=docker/dockerfile:1
FROM nginx:alpine

# Use the "config" context for environment-specific configurations
COPY --from=config nginx.conf /etc/nginx/nginx.conf
```

#### Example: pin or override images

You can refer to named contexts in a Dockerfile the same way you can refer to
an image. That means you can change an image reference in your Dockerfile by
overriding it with a named context. For example, given the following
Dockerfile:

```dockerfile
FROM alpine:3.23
```

If you want to force image reference to resolve to a different version, without
changing the Dockerfile, you can pass a context with the same name to the
build. For example:

```console
docker buildx build --build-context alpine:3.23=docker-image://alpine:edge .
```

The `docker-image://` prefix marks the context as an image reference. The
reference can be a local image or an image in your registry.

### Named contexts with Bake

[Bake](https://docs.docker.com/build/bake/) is a tool built into `docker build` that
lets you manage your build configuration with a configuration file. Bake fully
supports named contexts.

To define named contexts in a Bake file:

docker-bake.hcl

```hcl
target "app" {
  contexts = {
    docs = "./docs"
  }
}
```

This is equivalent to the following CLI invocation:

```console
$ docker build --build-context docs=./docs .
```

#### Linking targets with named contexts

In addition to making complex builds more manageable, Bake also provides
additional features on top of what you can do with `docker build` on the CLI.
You can use named contexts to create build pipelines, where one target depends
on and builds on top of another. For example, consider a Docker build setup
where you have two Dockerfiles:

- `base.Dockerfile`: for building a base image
- `app.Dockerfile`: for building an application image

The `app.Dockerfile` uses the image produced by `base.Dockerfile` as it's base
image:

app.Dockerfile

```dockerfile
FROM mybaseimage
```

Normally, you would have to build the base image first, and then either load it
to Docker Engine's local image store or push it to a registry. With Bake, you
can reference other targets directly, creating a dependency between the `app`
target and the `base` target.

docker-bake.hcl

```hcl
target "base" {
  dockerfile = "base.Dockerfile"
}

target "app" {
  dockerfile = "app.Dockerfile"
  contexts = {
    # the target: prefix indicates that 'base' is a Bake target
    mybaseimage = "target:base"
  }
}
```

With this configuration, references to `mybaseimage` in `app.Dockerfile` use
the results from building the `base` target. Building the `app` target will
also trigger a rebuild of `mybaseimage`, if necessary:

```console
$ docker buildx bake app
```

### Further reading

For more information about working with named contexts, see:

- [--build-contextCLI reference](https://docs.docker.com/reference/cli/docker/buildx/build/#build-context)
- [Using Bake with additional contexts](https://docs.docker.com/build/bake/contexts/)

---

# Dockerfile overview

> Learn about Dockerfiles and how to use them with Docker Images to build and package your software

# Dockerfile overview

   Table of contents

---

## Dockerfile

It all starts with a Dockerfile.

Docker builds images by reading the instructions from a Dockerfile. A
Dockerfile is a text file containing instructions for building your source
code. The Dockerfile instruction syntax is defined by the specification
reference in the
[Dockerfile reference](https://docs.docker.com/reference/dockerfile/).

Here are the most common types of instructions:

| Instruction | Description |
| --- | --- |
| FROM <image> | Defines a base for your image. |
| RUN <command> | Executes any commands in a new layer on top of the current image and commits the result.RUNalso has a shell form for running commands. |
| WORKDIR <directory> | Sets the working directory for anyRUN,CMD,ENTRYPOINT,COPY, andADDinstructions that follow it in the Dockerfile. |
| COPY <src> <dest> | Copies new files or directories from<src>and adds them to the filesystem of the container at the path<dest>. |
| CMD <command> | Lets you define the default program that is run once you start the container based on this image. Each Dockerfile only has oneCMD, and only the lastCMDinstance is respected when multiple exist. |

Dockerfiles are crucial inputs for image builds and can facilitate automated,
multi-layer image builds based on your unique configurations. Dockerfiles can
start simple and grow with your needs to support more complex scenarios.

### Filename

The default filename to use for a Dockerfile is `Dockerfile`, without a file
extension. Using the default name allows you to run the `docker build` command
without having to specify additional command flags.

Some projects may need distinct Dockerfiles for specific purposes. A common
convention is to name these `<something>.Dockerfile`. You can specify the
Dockerfile filename using the `--file` flag for the `docker build` command.
Refer to the
[docker buildCLI reference](https://docs.docker.com/reference/cli/docker/buildx/build/#file)
to learn about the `--file` flag.

> Note
>
> We recommend using the default (`Dockerfile`) for your project's primary
> Dockerfile.

## Docker images

Docker images consist of layers. Each layer is the result of a build
instruction in the Dockerfile. Layers are stacked sequentially, and each one is
a delta representing the changes applied to the previous layer.

### Example

Here's what a typical workflow for building applications with Docker looks like.

The following example code shows a small "Hello World" application written in
Python, using the Flask framework.

```python
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"
```

In order to ship and deploy this application without Docker Build, you would
need to make sure that:

- The required runtime dependencies are installed on the server
- The Python code gets uploaded to the server's filesystem
- The server starts your application, using the necessary parameters

The following Dockerfile creates a container image, which has all the
dependencies installed and that automatically starts your application.

```dockerfile
# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# install app dependencies
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip install flask==3.0.*

# install app
COPY hello.py /

# final configuration
ENV FLASK_APP=hello
EXPOSE 8000
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "8000"]
```

Here's a breakdown of what this Dockerfile does:

- [Dockerfile syntax](#dockerfile-syntax)
- [Base image](#base-image)
- [Environment setup](#environment-setup)
- [Comments](#comments)
- [Installing dependencies](#installing-dependencies)
- [Copying files](#copying-files)
- [Setting environment variables](#setting-environment-variables)
- [Exposed ports](#exposed-ports)
- [Starting the application](#starting-the-application)

### Dockerfile syntax

The first line to add to a Dockerfile is a
[# syntaxparser directive](https://docs.docker.com/reference/dockerfile/#syntax).
While optional, this directive instructs the Docker builder what syntax to use
when parsing the Dockerfile, and allows older Docker versions with [BuildKit enabled](https://docs.docker.com/build/buildkit/#getting-started)
to use a specific [Dockerfile frontend](https://docs.docker.com/build/buildkit/frontend/) before
starting the build.
[Parser directives](https://docs.docker.com/reference/dockerfile/#parser-directives)
must appear before any other comment, whitespace, or Dockerfile instruction in
your Dockerfile, and should be the first line in Dockerfiles.

```dockerfile
# syntax=docker/dockerfile:1
```

> Tip
>
> We recommend using `docker/dockerfile:1`, which always points to the latest
> release of the version 1 syntax. BuildKit automatically checks for updates of
> the syntax before building, making sure you are using the most current version.

### Base image

The line following the syntax directive defines what base image to use:

```dockerfile
FROM ubuntu:22.04
```

The
[FROMinstruction](https://docs.docker.com/reference/dockerfile/#from) sets your base
image to the 22.04 release of Ubuntu. All instructions that follow are executed
in this base image: an Ubuntu environment. The notation `ubuntu:22.04`, follows
the `name:tag` standard for naming Docker images. When you build images, you
use this notation to name your images. There are many public images you can
leverage in your projects, by importing them into your build steps using the
Dockerfile `FROM` instruction.

[Docker Hub](https://hub.docker.com/search?badges=official)
contains a large set of official images that you can use for this purpose.

### Environment setup

The following line executes a build command inside the base image.

```dockerfile
# install app dependencies
RUN apt-get update && apt-get install -y python3 python3-pip
```

This
[RUNinstruction](https://docs.docker.com/reference/dockerfile/#run) executes a
shell in Ubuntu that updates the APT package index and installs Python tools in
the container.

### Comments

Note the `# install app dependencies` line. This is a comment. Comments in
Dockerfiles begin with the `#` symbol. As your Dockerfile evolves, comments can
be instrumental to document how your Dockerfile works for any future readers
and editors of the file, including your future self.

> Note
>
> You might've noticed that comments are denoted using the same symbol as the
> [syntax directive](#dockerfile-syntax) on the first line of the file.
> The symbol is only interpreted as a directive if the pattern matches a
> directive and appears at the beginning of the Dockerfile. Otherwise, it's
> treated as a comment.

### Installing dependencies

The second `RUN` instruction installs the `flask` dependency required by the
Python application.

```dockerfile
RUN pip install flask==3.0.*
```

A prerequisite for this instruction is that `pip` is installed into the build
container. The first `RUN` command installs `pip`, which ensures that we can
use the command to install the flask web framework.

### Copying files

The next instruction uses the
[COPYinstruction](https://docs.docker.com/reference/dockerfile/#copy) to copy the
`hello.py` file from the local build context into the root directory of our image.

```dockerfile
COPY hello.py /
```

A [build context](https://docs.docker.com/build/concepts/context/) is the set of files that you can access
in Dockerfile instructions such as `COPY` and `ADD`.

After the `COPY` instruction, the `hello.py` file is added to the filesystem
of the build container.

### Setting environment variables

If your application uses environment variables, you can set environment variables
in your Docker build using the
[ENVinstruction](https://docs.docker.com/reference/dockerfile/#env).

```dockerfile
ENV FLASK_APP=hello
```

This sets a Linux environment variable we'll need later. Flask, the framework
used in this example, uses this variable to start the application. Without this,
flask wouldn't know where to find our application to be able to run it.

### Exposed ports

The
[EXPOSEinstruction](https://docs.docker.com/reference/dockerfile/#expose) marks that
our final image has a service listening on port `8000`.

```dockerfile
EXPOSE 8000
```

This instruction isn't required, but it is a good practice and helps tools and
team members understand what this application is doing.

### Starting the application

Finally,
[CMDinstruction](https://docs.docker.com/reference/dockerfile/#cmd) sets the
command that is run when the user starts a container based on this image.

```dockerfile
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "8000"]
```

This command starts the flask development server listening on all addresses
on port `8000`. The example here uses the "exec form" version of `CMD`.
It's also possible to use the "shell form":

```dockerfile
CMD flask run --host 0.0.0.0 --port 8000
```

There are subtle differences between these two versions,
for example in how they trap signals like `SIGTERM` and `SIGKILL`.
For more information about these differences, see
[Shell and exec form](https://docs.docker.com/reference/dockerfile/#shell-and-exec-form)

## Building

To build a container image using the Dockerfile example from the
[previous section](#example), you use the `docker build` command:

```console
$ docker build -t test:latest .
```

The `-t test:latest` option specifies the name and tag of the image.

The single dot (`.`) at the end of the command sets the
[build context](https://docs.docker.com/build/concepts/context/) to the current directory. This means that the
build expects to find the Dockerfile and the `hello.py` file in the directory
where the command is invoked. If those files aren't there, the build fails.

After the image has been built, you can run the application as a container with
`docker run`, specifying the image name:

```console
$ docker run -p 127.0.0.1:8000:8000 test:latest
```

This publishes the container's port 8000 to `http://localhost:8000` on the
Docker host.

> Tip
>
> To improve linting, code navigation, and vulnerability scanning of your Dockerfiles in Visual Studio Code
> see [Docker VS Code Extension](https://marketplace.visualstudio.com/items?itemName=docker.docker).

---

# Docker Build Overview

> Learn about Docker Build and its components.

# Docker Build Overview

   Table of contents

---

Docker Build implements a client-server architecture, where:

- Client: Buildx is the client and the user interface for running and managing builds.
- Server: BuildKit is the server, or builder, that handles the build execution.

When you invoke a build, the Buildx client sends a build request to the
BuildKit backend. BuildKit resolves the build instructions and executes the
build steps. The build output is either sent back to the client or uploaded to
a registry, such as Docker Hub.

Buildx and BuildKit are both installed with Docker Desktop and Docker Engine
out-of-the-box. When you invoke the `docker build` command, you're using Buildx
to run a build using the default BuildKit bundled with Docker.

## Buildx

Buildx is the CLI tool that you use to run builds. The `docker build` command
is a wrapper around Buildx. When you invoke `docker build`, Buildx interprets
the build options and sends a build request to the BuildKit backend.

The Buildx client can do more than just run builds. You can also use Buildx to
create and manage BuildKit backends, referred to as builders. It also supports
features for managing images in registries, and for running multiple builds
concurrently.

Docker Buildx is installed by default with Docker Desktop. You can also build
the CLI plugin from source, or grab a binary from the GitHub repository and
install it manually. See [Buildx README](https://github.com/docker/buildx#manual-download)
on GitHub for more information.

> Note
>
> While `docker build` invokes Buildx under the hood, there are subtle
> differences between this command and the canonical `docker buildx build`.
> For details, see [Difference betweendocker buildanddocker buildx build](https://docs.docker.com/build/builders/#difference-between-docker-build-and-docker-buildx-build).

## BuildKit

BuildKit is the daemon process that executes the build workloads.

A build execution starts with the invocation of a `docker build` command.
Buildx interprets your build command and sends a build request to the BuildKit
backend. The build request includes:

- The Dockerfile
- Build arguments
- Export options
- Caching options

BuildKit resolves the build instructions and executes the build steps. While
BuildKit is executing the build, Buildx monitors the build status and prints
the progress to the terminal.

If the build requires resources from the client, such as local files or build
secrets, BuildKit requests the resources that it needs from Buildx.

This is one way in which BuildKit is more efficient compared to the legacy
builder used in earlier versions of Docker. BuildKit only requests the
resources that the build needs when they're needed. The legacy builder, in
comparison, always takes a copy of the local filesystem.

Examples of resources that BuildKit can request from Buildx include:

- Local filesystem build contexts
- Build secrets
- SSH sockets
- Registry authentication tokens

For more information about BuildKit, see
[BuildKit](https://docs.docker.com/build/buildkit/).

---

# OpenTelemetry support

> Analyze telemetry data for builds

# OpenTelemetry support

---

Both Buildx and BuildKit support [OpenTelemetry](https://opentelemetry.io/).

To capture the trace to [Jaeger](https://github.com/jaegertracing/jaeger),
set `JAEGER_TRACE` environment variable to the collection address using a
`driver-opt`.

First create a Jaeger container:

```console
$ docker run -d --name jaeger -p "6831:6831/udp" -p "16686:16686" --restart unless-stopped jaegertracing/all-in-one
```

Then
[create adocker-containerbuilder](https://docs.docker.com/build/builders/drivers/docker-container/)
that will use the Jaeger instance via the `JAEGER_TRACE` environment variable:

```console
$ docker buildx create --use \
  --name mybuilder \
  --driver docker-container \
  --driver-opt "network=host" \
  --driver-opt "env.JAEGER_TRACE=localhost:6831"
```

Boot and
[inspectmybuilder](https://docs.docker.com/reference/cli/docker/buildx/inspect/):

```console
$ docker buildx inspect --bootstrap
```

Buildx commands should be traced at `http://127.0.0.1:16686/`:

![OpenTelemetry Buildx Bake](https://docs.docker.com/build/images/opentelemetry.png)  ![OpenTelemetry Buildx Bake](https://docs.docker.com/build/images/opentelemetry.png)

---

# Image and registry exporters

> The image and registry exporters create an image that can be loaded to your local image store or pushed to a registry

# Image and registry exporters

   Table of contents

---

The `image` exporter outputs the build result into a container image format. The
`registry` exporter is identical, but it automatically pushes the result by
setting `push=true`.

## Synopsis

Build a container image using the `image` and `registry` exporters:

```console
$ docker buildx build --output type=image[,parameters] .
$ docker buildx build --output type=registry[,parameters] .
```

The following table describes the available parameters that you can pass to
`--output` for `type=image`:

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| name | String |  | Specify image name(s) |
| push | true,false | false | Push after creating the image. |
| push-by-digest | true,false | false | Push image without name. |
| registry.insecure | true,false | false | Allow pushing to insecure registry. |
| dangling-name-prefix | <value> |  | Name image withprefix@<digest>, used for anonymous images |
| name-canonical | true,false |  | Add additional canonical namename@<digest> |
| compression | uncompressed,gzip,estargz,zstd | gzip | Compression type, seecompression |
| compression-level | 0..22 |  | Compression level, seecompression |
| force-compression | true,false | false | Forcefully apply compression, seecompression |
| rewrite-timestamp | true,false | false | Rewrite the file timestamps to theSOURCE_DATE_EPOCHvalue. Seebuild reproducibilityfor how to specify theSOURCE_DATE_EPOCHvalue. |
| oci-mediatypes | true,false | false | Use OCI media types in exporter manifests, seeOCI Media types |
| oci-artifact | true,false | false | Attestations are formatted as OCI artifacts, seeOCI Media types |
| unpack | true,false | false | Unpack image after creation (for use with containerd) |
| store | true,false | true | Store the result images to the worker's (for example, containerd) image store, and ensures that the image has all blobs in the content store. Ignored if the worker doesn't have image store (when using OCI workers, for example). |
| annotation.<key> | String |  | Attach an annotation with the respectivekeyandvalueto the built image,seeannotations |

## Annotations

These exporters support adding OCI annotation using `annotation` parameter,
followed by the annotation name using dot notation. The following example sets
the `org.opencontainers.image.title` annotation:

```console
$ docker buildx build \
    --output "type=<type>,name=<registry>/<image>,annotation.org.opencontainers.image.title=<title>" .
```

For more information about annotations, see
[BuildKit documentation](https://github.com/moby/buildkit/blob/master/docs/annotations.md).

## Further reading

For more information on the `image` or `registry` exporters, see the
[BuildKit README](https://github.com/moby/buildkit/blob/master/README.md#imageregistry).
