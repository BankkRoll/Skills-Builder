# Building with Bake from a Compose file and more

# Building with Bake from a Compose file

> Build your compose services with Bake

# Building with Bake from a Compose file

   Table of contents

---

Bake supports the
[Compose file format](https://docs.docker.com/reference/compose-file/)
to parse a Compose file and translate each service to a [target](https://docs.docker.com/build/bake/reference/#target).

```yaml
# compose.yaml
services:
  webapp-dev:
    build: &build-dev
      dockerfile: Dockerfile.webapp
      tags:
        - docker.io/username/webapp:latest
      cache_from:
        - docker.io/username/webapp:cache
      cache_to:
        - docker.io/username/webapp:cache

  webapp-release:
    build:
      <<: *build-dev
      x-bake:
        platforms:
          - linux/amd64
          - linux/arm64

  db:
    image: docker.io/username/db
    build:
      dockerfile: Dockerfile.db
```

```console
$ docker buildx bake --print
```

```json
{
  "group": {
    "default": {
      "targets": ["db", "webapp-dev", "webapp-release"]
    }
  },
  "target": {
    "db": {
      "context": ".",
      "dockerfile": "Dockerfile.db",
      "tags": ["docker.io/username/db"]
    },
    "webapp-dev": {
      "context": ".",
      "dockerfile": "Dockerfile.webapp",
      "tags": ["docker.io/username/webapp:latest"],
      "cache-from": [
        {
          "ref": "docker.io/username/webapp:cache",
          "type": "registry"
        }
      ],
      "cache-to": [
        {
          "ref": "docker.io/username/webapp:cache",
          "type": "registry"
        }
      ]
    },
    "webapp-release": {
      "context": ".",
      "dockerfile": "Dockerfile.webapp",
      "tags": ["docker.io/username/webapp:latest"],
      "cache-from": [
        {
          "ref": "docker.io/username/webapp:cache",
          "type": "registry"
        }
      ],
      "cache-to": [
        {
          "ref": "docker.io/username/webapp:cache",
          "type": "registry"
        }
      ],
      "platforms": ["linux/amd64", "linux/arm64"]
    }
  }
}
```

The compose format has some limitations compared to the HCL format:

- Specifying variables or global scope attributes is not yet supported
- `inherits` service field is not supported, but you can use
  [YAML anchors](https://docs.docker.com/reference/compose-file/fragments/)
  to reference other services, as demonstrated in the previous example with `&build-dev`.

## .envfile

You can declare default environment variables in an environment file named
`.env`. This file will be loaded from the current working directory,
where the command is executed and applied to compose definitions passed
with `-f`.

```yaml
# compose.yaml
services:
  webapp:
    image: docker.io/username/webapp:${TAG:-v1.0.0}
    build:
      dockerfile: Dockerfile
```

```sh
# .env
TAG=v1.1.0
```

```console
$ docker buildx bake --print
```

```json
{
  "group": {
    "default": {
      "targets": ["webapp"]
    }
  },
  "target": {
    "webapp": {
      "context": ".",
      "dockerfile": "Dockerfile",
      "tags": ["docker.io/username/webapp:v1.1.0"]
    }
  }
}
```

> Note
>
> System environment variables take precedence over environment variables
> in `.env` file.

## Extension field withx-bake

Where some fields are not available in the compose specification, you can use
the
[special extension](https://docs.docker.com/reference/compose-file/extension/) field
`x-bake` in your compose file to evaluate extra fields:

```yaml
# compose.yaml
services:
  addon:
    image: ct-addon:bar
    build:
      context: .
      dockerfile: ./Dockerfile
      args:
        CT_ECR: foo
        CT_TAG: bar
      x-bake:
        tags:
          - ct-addon:foo
          - ct-addon:alp
        platforms:
          - linux/amd64
          - linux/arm64
        cache-from:
          - user/app:cache
          - type=local,src=path/to/cache
        cache-to:
          - type=local,dest=path/to/cache
        pull: true

  aws:
    image: ct-fake-aws:bar
    build:
      dockerfile: ./aws.Dockerfile
      args:
        CT_ECR: foo
        CT_TAG: bar
      x-bake:
        secret:
          - id=mysecret,src=./secret
          - id=mysecret2,src=./secret2
        platforms: linux/arm64
        output: type=docker
        no-cache: true
```

```console
$ docker buildx bake --print
```

```json
{
  "group": {
    "default": {
      "targets": ["addon", "aws"]
    }
  },
  "target": {
    "addon": {
      "context": ".",
      "dockerfile": "./Dockerfile",
      "args": {
        "CT_ECR": "foo",
        "CT_TAG": "bar"
      },
      "tags": ["ct-addon:foo", "ct-addon:alp"],
      "cache-from": [
        {
          "ref": "user/app:cache",
          "type": "registry"
        },
        {
          "src": "path/to/cache",
          "type": "local"
        }
      ],
      "cache-to": [
        {
          "dest": "path/to/cache",
          "type": "local"
        }
      ],
      "platforms": ["linux/amd64", "linux/arm64"],
      "pull": true
    },
    "aws": {
      "context": ".",
      "dockerfile": "./aws.Dockerfile",
      "args": {
        "CT_ECR": "foo",
        "CT_TAG": "bar"
      },
      "tags": ["ct-fake-aws:bar"],
      "secret": [
        {
          "id": "mysecret",
          "src": "./secret"
        },
        {
          "id": "mysecret2",
          "src": "./secret2"
        }
      ],
      "platforms": ["linux/arm64"],
      "output": [
        {
          "type": "docker"
        }
      ],
      "no-cache": true
    }
  }
}
```

Complete list of valid fields for `x-bake`:

- `cache-from`
- `cache-to`
- `contexts`
- `no-cache`
- `no-cache-filter`
- `output`
- `platforms`
- `pull`
- `secret`
- `ssh`
- `tags`

---

# Using Bake with additional contexts

> Additional contexts are useful when you want to pin image versions, or reference the output of other targets

# Using Bake with additional contexts

   Table of contents

---

In addition to the main `context` key that defines the build context, each
target can also define additional named contexts with a map defined with key
`contexts`. These values map to the `--build-context` flag in the
[build
command](https://docs.docker.com/reference/cli/docker/buildx/build/#build-context).

Inside the Dockerfile these contexts can be used with the `FROM` instruction or
`--from` flag.

Supported context values are:

- Local filesystem directories
- Container images
- Git URLs
- HTTP URLs
- Name of another target in the Bake file

## Pinning alpine image

Dockerfile

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
RUN echo "Hello world"
```

docker-bake.hcl

```hcl
target "app" {
  contexts = {
    alpine = "docker-image://alpine:3.13"
  }
}
```

## Using a secondary source directory

Dockerfile

```dockerfile
FROM golang
COPY --from=src . .
```

docker-bake.hcl

```hcl
# Running `docker buildx bake app` will result in `src` not pointing
# to some previous build stage but to the client filesystem, not part of the context.
target "app" {
  contexts = {
    src = "../path/to/source"
  }
}
```

## Using a target as a build context

To use a result of one target as a build context of another, specify the target
name with `target:` prefix.

baseapp.Dockerfile

```dockerfile
FROM scratch
```

Dockerfile

```dockerfile
# syntax=docker/dockerfile:1
FROM baseapp
RUN echo "Hello world"
```

docker-bake.hcl

```hcl
target "base" {
  dockerfile = "baseapp.Dockerfile"
}

target "app" {
  contexts = {
    baseapp = "target:base"
  }
}
```

In most cases you should just use a single multi-stage Dockerfile with multiple
targets for similar behavior. This case is only recommended when you have
multiple Dockerfiles that can't be easily merged into one.

## Deduplicate context transfer

> Note
>
> As of Buildx version 0.17.0 and later, Bake automatically de-duplicates
> context transfer for targets that share the same context. In addition to
> Buildx version 0.17.0, the builder must be running BuildKit version 0.16.0 or
> later, and the Dockerfile syntax must be `docker/dockerfile:1.10` or later.
>
>
>
> If you meet these requirements, you don't need to manually de-duplicate
> context transfer as described in this section.
>
>
>
> - To check your Buildx version, run `docker buildx version`.
> - To check your BuildKit version, run `docker buildx inspect --bootstrap` and
>   look for the `BuildKit version` field.
> - To check your Dockerfile syntax version, check the `syntax` [parser directive](https://docs.docker.com/reference/dockerfile/#syntax) in your Dockerfile. If
>   it's not present, the default version whatever comes bundled with your
>   current version of BuildKit. To set the version explicitly, add
>   `#syntax=docker/dockerfile:1.10` at the top of your Dockerfile.

When you build targets concurrently, using groups, build contexts are loaded
independently for each target. If the same context is used by multiple targets
in a group, that context is transferred once for each time it's used. This can
result in significant impact on build time, depending on your build
configuration. For example, say you have a Bake file that defines the following
group of targets:

docker-bake.hcl

```hcl
group "default" {
  targets = ["target1", "target2"]
}

target "target1" {
  target = "target1"
  context = "."
}

target "target2" {
  target = "target2"
  context = "."
}
```

In this case, the context `.` is transferred twice when you build the default
group: once for `target1` and once for `target2`.

If your context is small, and if you are using a local builder, duplicate
context transfers may not be a big deal. But if your build context is big, or
you have a large number of targets, or you're transferring the context over a
network to a remote builder, context transfer becomes a performance bottleneck.

To avoid transferring the same context multiple times, you can define a named
context that only loads the context files, and have each target that needs
those files reference that named context. For example, the following Bake file
defines a named target `ctx`, which is used by both `target1` and `target2`:

docker-bake.hcl

```hcl
group "default" {
  targets = ["target1", "target2"]
}

target "ctx" {
  context = "."
  target = "ctx"
}

target "target1" {
  target = "target1"
  contexts = {
    ctx = "target:ctx"
  }
}

target "target2" {
  target = "target2"
  contexts = {
    ctx = "target:ctx"
  }
}
```

The named context `ctx` represents a Dockerfile stage, which copies the files
from its context (`.`). Other stages in the Dockerfile can now reference the
`ctx` named context and, for example, mount its files with `--mount=from=ctx`.

Dockerfile

```dockerfile
FROM scratch AS ctx
COPY --link . .

FROM golang:alpine AS target1
WORKDIR /work
RUN --mount=from=ctx \
    go build -o /out/client ./cmd/client \

FROM golang:alpine AS target2
WORKDIR /work
RUN --mount=from=ctx \
    go build -o /out/server ./cmd/server
```

---

# Expression evaluation in Bake

> Learn about advanced Bake features, like user-defined functions

# Expression evaluation in Bake

   Table of contents

---

Bake files in the HCL format support expression evaluation, which lets you
perform arithmetic operations, conditionally set values, and more.

## Arithmetic operations

You can perform arithmetic operations in expressions. The following example
shows how to multiply two numbers.

docker-bake.hcl

```hcl
sum = 7*6

target "default" {
  args = {
    answer = sum
  }
}
```

Printing the Bake file with the `--print` flag shows the evaluated value for
the `answer` build argument.

```console
$ docker buildx bake --print
```

```json
{
  "target": {
    "default": {
      "context": ".",
      "dockerfile": "Dockerfile",
      "args": {
        "answer": "42"
      }
    }
  }
}
```

## Ternary operators

You can use ternary operators to conditionally register a value.

The following example adds a tag only when a variable is not empty, using the
built-in `notequal` [function](https://docs.docker.com/build/bake/funcs/).

docker-bake.hcl

```hcl
variable "TAG" {}

target "default" {
  context="."
  dockerfile="Dockerfile"
  tags = [
    "my-image:latest",
    notequal("",TAG) ? "my-image:${TAG}": ""
  ]
}
```

In this case, `TAG` is an empty string, so the resulting build configuration
only contains the hard-coded `my-image:latest` tag.

```console
$ docker buildx bake --print
```

```json
{
  "target": {
    "default": {
      "context": ".",
      "dockerfile": "Dockerfile",
      "tags": ["my-image:latest"]
    }
  }
}
```

## Expressions with variables

You can use expressions with [variables](https://docs.docker.com/build/bake/variables/) to conditionally set
values, or to perform arithmetic operations.

The following example uses expressions to set values based on the value of
variables. The `v1` build argument is set to "higher" if the variable `FOO` is
greater than 5, otherwise it is set to "lower". The `v2` build argument is set
to "yes" if the `IS_FOO` variable is true, otherwise it is set to "no".

docker-bake.hcl

```hcl
variable "FOO" {
  default = 3
}

variable "IS_FOO" {
  default = true
}

target "app" {
  args = {
    v1 = FOO > 5 ? "higher" : "lower"
    v2 = IS_FOO ? "yes" : "no"
  }
}
```

Printing the Bake file with the `--print` flag shows the evaluated values for
the `v1` and `v2` build arguments.

```console
$ docker buildx bake --print app
```

```json
{
  "group": {
    "default": {
      "targets": ["app"]
    }
  },
  "target": {
    "app": {
      "context": ".",
      "dockerfile": "Dockerfile",
      "args": {
        "v1": "lower",
        "v2": "yes"
      }
    }
  }
}
```

---

# Functions

> Learn about built-in and user-defined HCL functions with Bake

# Functions

   Table of contents

---

HCL functions are great for when you need to manipulate values in your build
configuration in more complex ways than just concatenation or interpolation.

## Standard library

Bake ships with built-in support for the
[standard library functions](https://docs.docker.com/build/bake/stdlib/).

The following example shows the `add` function:

docker-bake.hcl

```hcl
variable "TAG" {
  default = "latest"
}

group "default" {
  targets = ["webapp"]
}

target "webapp" {
  args = {
    buildno = "${add(123, 1)}"
  }
}
```

```console
$ docker buildx bake --print webapp
```

```json
{
  "group": {
    "default": {
      "targets": ["webapp"]
    }
  },
  "target": {
    "webapp": {
      "context": ".",
      "dockerfile": "Dockerfile",
      "args": {
        "buildno": "124"
      }
    }
  }
}
```

## User-defined functions

You can create [user-defined functions](https://github.com/hashicorp/hcl/tree/main/ext/userfunc)
that do just what you want, if the built-in standard library functions don't
meet your needs.

The following example defines an `increment` function.

docker-bake.hcl

```hcl
function "increment" {
  params = [number]
  result = number + 1
}

group "default" {
  targets = ["webapp"]
}

target "webapp" {
  args = {
    buildno = "${increment(123)}"
  }
}
```

```console
$ docker buildx bake --print webapp
```

```json
{
  "group": {
    "default": {
      "targets": ["webapp"]
    }
  },
  "target": {
    "webapp": {
      "context": ".",
      "dockerfile": "Dockerfile",
      "args": {
        "buildno": "124"
      }
    }
  }
}
```

## Variables in functions

You can make references to [variables](https://docs.docker.com/build/bake/variables/) and standard library
functions inside your functions.

You can't reference user-defined functions from other functions.

The following example uses a global variable (`REPO`) in a custom function.

docker-bake.hcl

```hcl
# docker-bake.hcl
variable "REPO" {
  default = "user/repo"
}

function "tag" {
  params = [tag]
  result = ["${REPO}:${tag}"]
}

target "webapp" {
  tags = tag("v1")
}
```

Printing the Bake file with the `--print` flag shows that the `tag` function
uses the value of `REPO` to set the prefix of the tag.

```console
$ docker buildx bake --print webapp
```

```json
{
  "group": {
    "default": {
      "targets": ["webapp"]
    }
  },
  "target": {
    "webapp": {
      "context": ".",
      "dockerfile": "Dockerfile",
      "tags": ["user/repo:v1"]
    }
  }
}
```

---

# Inheritance in Bake

> Learn how to inherit attributes from other targets in Bake

# Inheritance in Bake

   Table of contents

---

Targets can inherit attributes from other targets, using the `inherits`
attribute. For example, imagine that you have a target that builds a Docker
image for a development environment:

docker-bake.hcl

```hcl
target "app-dev" {
  args = {
    GO_VERSION = "1.25"
  }
  tags = ["docker.io/username/myapp:dev"]
  labels = {
    "org.opencontainers.image.source" = "https://github.com/username/myapp"
    "org.opencontainers.image.author" = "moby.whale@example.com"
  }
}
```

You can create a new target that uses the same build configuration, but with
slightly different attributes for a production build. In this example, the
`app-release` target inherits the `app-dev` target, but overrides the `tags`
attribute and adds a new `platforms` attribute:

docker-bake.hcl

```hcl
target "app-release" {
  inherits = ["app-dev"]
  tags = ["docker.io/username/myapp:latest"]
  platforms = ["linux/amd64", "linux/arm64"]
}
```

## Common reusable targets

One common inheritance pattern is to define a common target that contains
shared attributes for all or many of the build targets in the project. For
example, the following `_common` target defines a common set of build
arguments:

docker-bake.hcl

```hcl
target "_common" {
  args = {
    GO_VERSION = "1.25"
    BUILDKIT_CONTEXT_KEEP_GIT_DIR = 1
  }
}
```

You can then inherit the `_common` target in other targets to apply the shared
attributes:

docker-bake.hcl

```hcl
target "lint" {
  inherits = ["_common"]
  dockerfile = "./dockerfiles/lint.Dockerfile"
  output = [{ type = "cacheonly" }]
}

target "docs" {
  inherits = ["_common"]
  dockerfile = "./dockerfiles/docs.Dockerfile"
  output = ["./docs/reference"]
}

target "test" {
  inherits = ["_common"]
  target = "test-output"
  output = ["./test"]
}

target "binaries" {
  inherits = ["_common"]
  target = "binaries"
  output = ["./build"]
  platforms = ["local"]
}
```

## Overriding inherited attributes

When a target inherits another target, it can override any of the inherited
attributes. For example, the following target overrides the `args` attribute
from the inherited target:

docker-bake.hcl

```hcl
target "app-dev" {
  inherits = ["_common"]
  args = {
    GO_VERSION = "1.17"
  }
  tags = ["docker.io/username/myapp:dev"]
}
```

The `GO_VERSION` argument in `app-release` is set to `1.17`, overriding the
`GO_VERSION` argument from the `app-dev` target.

For more information about overriding attributes, see the [Overriding
configurations](https://docs.docker.com/build/bake/overrides/) page.

## Inherit from multiple targets

The `inherits` attribute is a list, meaning you can reuse attributes from
multiple other targets. In the following example, the app-release target reuses
attributes from both the `app-dev` and `_common` targets.

docker-bake.hcl

```hcl
target "_common" {
  args = {
    GO_VERSION = "1.25"
    BUILDKIT_CONTEXT_KEEP_GIT_DIR = 1
  }
}

target "app-dev" {
  inherits = ["_common"]
  args = {
    BUILDKIT_CONTEXT_KEEP_GIT_DIR = 0
  }
  tags = ["docker.io/username/myapp:dev"]
  labels = {
    "org.opencontainers.image.source" = "https://github.com/username/myapp"
    "org.opencontainers.image.author" = "moby.whale@example.com"
  }
}

target "app-release" {
  inherits = ["app-dev", "_common"]
  tags = ["docker.io/username/myapp:latest"]
  platforms = ["linux/amd64", "linux/arm64"]
}
```

When inheriting attributes from multiple targets and there's a conflict, the
target that appears last in the inherits list takes precedence. The previous
example defines the `BUILDKIT_CONTEXT_KEEP_GIT_DIR` in the `_common` target and
overrides it in the `app-dev` target.

The `app-release` target inherits both `app-dev` target and the `_common` target.
The `BUILDKIT_CONTEXT_KEEP_GIT_DIR` argument is set to 0 in the `app-dev` target
and 1 in the `_common` target. The `BUILDKIT_CONTEXT_KEEP_GIT_DIR` argument in
the `app-release` target is set to 1, not 0, because the `_common` target appears
last in the inherits list.

## Reusing single attributes from targets

If you only want to inherit a single attribute from a target, you can reference
an attribute from another target using dot notation. For example, in the
following Bake file, the `bar` target reuses the `tags` attribute from the
`foo` target:

docker-bake.hcl

```hcl
target "foo" {
  dockerfile = "foo.Dockerfile"
  tags       = ["myapp:latest"]
}
target "bar" {
  dockerfile = "bar.Dockerfile"
  tags       = target.foo.tags
}
```

---

# Introduction to Bake

> Get started with using Bake to build your project

# Introduction to Bake

   Table of contents

---

Bake is an abstraction for the `docker build` command that lets you more easily
manage your build configuration (CLI flags, environment variables, etc.) in a
consistent way for everyone on your team.

Bake is a command built into the Buildx CLI, so as long as you have Buildx
installed, you also have access to bake, via the `docker buildx bake` command.

## Building a project with Bake

Here's a simple example of a `docker build` command:

```console
$ docker build -f Dockerfile -t myapp:latest .
```

This command builds the Dockerfile in the current directory and tags the
resulting image as `myapp:latest`.

To express the same build configuration using Bake:

docker-bake.hcl

```hcl
target "myapp" {
  context = "."
  dockerfile = "Dockerfile"
  tags = ["myapp:latest"]
}
```

Bake provides a structured way to manage your build configuration, and it saves
you from having to remember all the CLI flags for `docker build` every time.
With this file, building the image is as simple as running:

```console
$ docker buildx bake myapp
```

For simple builds, the difference between `docker build` and `docker buildx bake` is minimal. However, as your build configuration grows more complex, Bake
provides a more structured way to manage that complexity, that would be
difficult to manage with CLI flags for the `docker build`. It also provides a
way to share build configurations across your team, so that everyone is
building images in a consistent way, with the same configuration.

## The Bake file format

You can write Bake files in HCL, YAML (Docker Compose files), or JSON. In
general, HCL is the most expressive and flexible format, which is why you'll
see it used in most of the examples in this documentation, and in projects that
use Bake.

The properties that can be set for a target closely resemble the CLI flags for
`docker build`. For instance, consider the following `docker build` command:

```console
$ docker build \
  -f Dockerfile \
  -t myapp:latest \
  --build-arg foo=bar \
  --no-cache \
  --platform linux/amd64,linux/arm64 \
  .
```

The Bake equivalent would be:

docker-bake.hcl

```hcl
target "myapp" {
  context = "."
  dockerfile = "Dockerfile"
  tags = ["myapp:latest"]
  args = {
    foo = "bar"
  }
  no-cache = true
  platforms = ["linux/amd64", "linux/arm64"]
}
```

> Tip
>
> Want a better editing experience for Bake files in VS Code?
> Check out the [Docker VS Code Extension (Beta)](https://marketplace.visualstudio.com/items?itemName=docker.docker) for linting, code navigation, and vulnerability scanning.

## Next steps

To learn more about using Bake, see the following topics:

- Learn how to define and use [targets](https://docs.docker.com/build/bake/targets/) in Bake
- To see all the properties that can be set for a target, refer to the
  [Bake file reference](https://docs.docker.com/build/bake/reference/).

---

# Matrix targets

> Learn how to define and use matrix targets in Bake to fork a single target into multiple different variants

# Matrix targets

   Table of contents

---

A matrix strategy lets you fork a single target into multiple different
variants, based on parameters that you specify. This works in a similar way to
[Matrix strategies for GitHub Actions](https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs).
You can use this to reduce duplication in your Bake definition.

The matrix attribute is a map of parameter names to lists of values. Bake
builds each possible combination of values as a separate target.

Each generated target must have a unique name. To specify how target names
should resolve, use the name attribute.

The following example resolves the app target to `app-foo` and `app-bar`. It
also uses the matrix value to define the
[target build stage](https://docs.docker.com/build/bake/reference/#targettarget).

docker-bake.hcl

```hcl
target "app" {
  name = "app-${tgt}"
  matrix = {
    tgt = ["foo", "bar"]
  }
  target = tgt
}
```

```console
$ docker buildx bake --print app
[+] Building 0.0s (0/0)
{
  "group": {
    "app": {
      "targets": [
        "app-foo",
        "app-bar"
      ]
    },
    "default": {
      "targets": [
        "app"
      ]
    }
  },
  "target": {
    "app-bar": {
      "context": ".",
      "dockerfile": "Dockerfile",
      "target": "bar"
    },
    "app-foo": {
      "context": ".",
      "dockerfile": "Dockerfile",
      "target": "foo"
    }
  }
}
```

## Multiple axes

You can specify multiple keys in your matrix to fork a target on multiple axes.
When using multiple matrix keys, Bake builds every possible variant.

The following example builds four targets:

- `app-foo-1-0`
- `app-foo-2-0`
- `app-bar-1-0`
- `app-bar-2-0`

docker-bake.hcl

```hcl
target "app" {
  name = "app-${tgt}-${replace(version, ".", "-")}"
  matrix = {
    tgt = ["foo", "bar"]
    version = ["1.0", "2.0"]
  }
  target = tgt
  args = {
    VERSION = version
  }
}
```

## Multiple values per matrix target

If you want to differentiate the matrix on more than just a single value, you
can use maps as matrix values. Bake creates a target for each map, and you can
access the nested values using dot notation.

The following example builds two targets:

- `app-foo-1-0`
- `app-bar-2-0`

docker-bake.hcl

```hcl
target "app" {
  name = "app-${item.tgt}-${replace(item.version, ".", "-")}"
  matrix = {
    item = [
      {
        tgt = "foo"
        version = "1.0"
      },
      {
        tgt = "bar"
        version = "2.0"
      }
    ]
  }
  target = item.tgt
  args = {
    VERSION = item.version
  }
}
```

---

# Overriding configurations

> Learn how to override configurations in Bake files to build with different attributes.

# Overriding configurations

   Table of contents

---

Bake supports loading build definitions from files, but sometimes you need even
more flexibility to configure these definitions. For example, you might want to
override an attribute when building in a particular environment or for a
specific target.

The following list of attributes can be overridden:

- `args`
- `attest`
- `cache-from`
- `cache-to`
- `context`
- `contexts`
- `dockerfile`
- `entitlements`
- `labels`
- `network`
- `no-cache`
- `output`
- `platform`
- `pull`
- `secrets`
- `ssh`
- `tags`
- `target`

To override these attributes, you can use the following methods:

- [File overrides](#file-overrides)
- [CLI overrides](#command-line)
- [Environment variable overrides](#environment-variables)

## File overrides

You can load multiple Bake files that define build configurations for your
targets. This is useful when you want to separate configurations into different
files for better organization, or to conditionally override configurations
based on which files are loaded.

### Default file lookup

You can use the `--file` or `-f` flag to specify which files to load.
If you don't specify any files, Bake will use the following lookup order:

1. `compose.yaml`
2. `compose.yml`
3. `docker-compose.yml`
4. `docker-compose.yaml`
5. `docker-bake.json`
6. `docker-bake.hcl`
7. `docker-bake.override.json`
8. `docker-bake.override.hcl`

If more than one Bake file is found, all files are loaded and merged into a
single definition. Files are merged according to the lookup order.

```console
$ docker buildx bake --print
[+] Building 0.0s (1/1) FINISHED
 => [internal] load local bake definitions                                                                                                                                                                             0.0s
 => => reading compose.yaml 45B / 45B                                                                                                                                                                                  0.0s
 => => reading docker-bake.hcl 113B / 113B                                                                                                                                                                             0.0s
 => => reading docker-bake.override.hcl 65B / 65B
```

If merged files contain duplicate attribute definitions, those definitions are
either merged or overridden by the last occurrence, depending on the attribute.

Bake will attempt to load all of the files in the order they are found. If
multiple files define the same target, attributes are either merged or
overridden. In the case of overrides, the last one loaded takes precedence.

For example, given the following files:

docker-bake.hcl

```hcl
variable "TAG" {
  default = "foo"
}

target "default" {
  tags = ["username/my-app:${TAG}"]
}
```

docker-bake.override.hcl

```hcl
variable "TAG" {
  default = "bar"
}
```

Since `docker-bake.override.hcl` is loaded last in the default lookup order,
the `TAG` variable is overridden with the value `bar`.

```console
$ docker buildx bake --print
{
  "target": {
    "default": {
      "context": ".",
      "dockerfile": "Dockerfile",
      "tags": ["username/my-app:bar"]
    }
  }
}
```

### Manual file overrides

You can use the `--file` flag to explicitly specify which files to load,
and use this as a way to conditionally apply override files.

For example, you can create a file that defines a set of configurations for a
specific environment, and load it only when building for that environment. The
following example shows how to load an `override.hcl` file that sets the `TAG`
variable to `bar`. The `TAG` variable is then used in the `default` target.

docker-bake.hcl

```hcl
variable "TAG" {
  default = "foo"
}

target "default" {
  tags = ["username/my-app:${TAG}"]
}
```

overrides.hcl

```hcl
variable "TAG" {
  default = "bar"
}
```

Printing the build configuration without the `--file` flag shows the `TAG`
variable is set to the default value `foo`.

```console
$ docker buildx bake --print
{
  "target": {
    "default": {
      "context": ".",
      "dockerfile": "Dockerfile",
      "tags": [
        "username/my-app:foo"
      ]
    }
  }
}
```

Using the `--file` flag to load the `overrides.hcl` file overrides the `TAG`
variable with the value `bar`.

```console
$ docker buildx bake -f docker-bake.hcl -f overrides.hcl --print
{
  "target": {
    "default": {
      "context": ".",
      "dockerfile": "Dockerfile",
      "tags": [
        "username/my-app:bar"
      ]
    }
  }
}
```

## Command line

You can also override target configurations from the command line with the
[--setflag](https://docs.docker.com/reference/cli/docker/buildx/bake/#set):

```hcl
# docker-bake.hcl
target "app" {
  args = {
    mybuildarg = "foo"
  }
}
```

```console
$ docker buildx bake --set app.args.mybuildarg=bar --set app.platform=linux/arm64 app --print
```

```json
{
  "group": {
    "default": {
      "targets": ["app"]
    }
  },
  "target": {
    "app": {
      "context": ".",
      "dockerfile": "Dockerfile",
      "args": {
        "mybuildarg": "bar"
      },
      "platforms": ["linux/arm64"]
    }
  }
}
```

> Note
>
> `--set` is a repeatable flag. For array fields such as `tags`, repeat `--set` to provide multiple values or use the `+=` operator to append without replacing.
> Array literal syntax like `--set target.tags=[a,b]` is not supported.

Pattern matching syntax defined in [https://golang.org/pkg/path/#Match](https://golang.org/pkg/path/#Match)
is also supported:

```console
$ docker buildx bake --set foo*.args.mybuildarg=value  # overrides build arg for all targets starting with "foo"
$ docker buildx bake --set *.platform=linux/arm64      # overrides platform for all targets
$ docker buildx bake --set foo*.no-cache               # bypass caching only for targets starting with "foo"
```

Complete list of attributes that can be overridden with `--set` are:

- `args`
- `attest`
- `cache-from`
- `cache-to`
- `context`
- `contexts`
- `dockerfile`
- `entitlements`
- `labels`
- `network`
- `no-cache`
- `output`
- `platform`
- `pull`
- `secrets`
- `ssh`
- `tags`
- `target`

## Environment variables

You can also use environment variables to override configurations.

Bake lets you use environment variables to override the value of a `variable`
block. Only `variable` blocks can be overridden with environment variables.
This means you need to define the variables in the bake file and then set the
environment variable with the same name to override it.

The following example shows how you can define a `TAG` variable with a default
value in the Bake file, and override it with an environment variable.

```hcl
variable "TAG" {
  default = "latest"
}

target "default" {
  context = "."
  dockerfile = "Dockerfile"
  tags = ["docker.io/username/webapp:${TAG}"]
}
```

```console
$ export TAG=$(git rev-parse --short HEAD)
$ docker buildx bake --print webapp
```

The `TAG` variable is overridden with the value of the environment variable,
which is the short commit hash generated by `git rev-parse --short HEAD`.

```json
{
  "group": {
    "default": {
      "targets": ["webapp"]
    }
  },
  "target": {
    "webapp": {
      "context": ".",
      "dockerfile": "Dockerfile",
      "tags": ["docker.io/username/webapp:985e9e9"]
    }
  }
}
```

### Type coercion

Overriding non-string variables with environment variables is supported. Values
passed as environment variables are coerced into suitable types first.

The following example defines a `PORT` variable. The `backend` target uses the
`PORT` variable as-is, and the `frontend` target uses the value of `PORT`
incremented by one.

```hcl
variable "PORT" {
  default = 3000
}

group "default" {
  targets = ["backend", "frontend"]
}

target "backend" {
  args = {
    PORT = PORT
  }
}

target "frontend" {
  args = {
    PORT = add(PORT, 1)
  }
}
```

Overriding `PORT` using an environment variable will first coerce the value
into the expected type, an integer, before the expression in the `frontend`
target runs.

```console
$ PORT=7070 docker buildx bake --print
```

```json
{
  "group": {
    "default": {
      "targets": [
        "backend",
        "frontend"
      ]
    }
  },
  "target": {
    "backend": {
      "context": ".",
      "dockerfile": "Dockerfile",
      "args": {
        "PORT": "7070"
      }
    },
    "frontend": {
      "context": ".",
      "dockerfile": "Dockerfile",
      "args": {
        "PORT": "7071"
      }
    }
  }
}
```
