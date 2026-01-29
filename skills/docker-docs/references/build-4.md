# Bake targets and more

# Bake targets

> Learn how to define and use targets in Bake

# Bake targets

   Table of contents

---

A target in a Bake file represents a build invocation. It holds all the
information you would normally pass to a `docker build` command using flags.

docker-bake.hcl

```hcl
target "webapp" {
  dockerfile = "webapp.Dockerfile"
  tags = ["docker.io/username/webapp:latest"]
  context = "https://github.com/username/webapp"
}
```

To build a target with Bake, pass name of the target to the `bake` command.

```console
$ docker buildx bake webapp
```

You can build multiple targets at once by passing multiple target names to the
`bake` command.

```console
$ docker buildx bake webapp api tests
```

## Default target

If you don't specify a target when running `docker buildx bake`, Bake will
build the target named `default`.

docker-bake.hcl

```hcl
target "default" {
  dockerfile = "webapp.Dockerfile"
  tags = ["docker.io/username/webapp:latest"]
  context = "https://github.com/username/webapp"
}
```

To build this target, run `docker buildx bake` without any arguments:

```console
$ docker buildx bake
```

## Target properties

The properties you can set for a target closely resemble the CLI flags for
`docker build`, with a few additional properties that are specific to Bake.

For all the properties you can set for a target, see the
[Bake reference](https://docs.docker.com/build/bake/reference#target).

## Grouping targets

You can group targets together using the `group` block. This is useful when you
want to build multiple targets at once.

docker-bake.hcl

```hcl
group "all" {
  targets = ["webapp", "api", "tests"]
}

target "webapp" {
  dockerfile = "webapp.Dockerfile"
  tags = ["docker.io/username/webapp:latest"]
  context = "https://github.com/username/webapp"
}

target "api" {
  dockerfile = "api.Dockerfile"
  tags = ["docker.io/username/api:latest"]
  context = "https://github.com/username/api"
}

target "tests" {
  dockerfile = "tests.Dockerfile"
  contexts = {
    webapp = "target:webapp"
    api = "target:api"
  }
  output = ["type=local,dest=build/tests"]
  context = "."
}
```

To build all the targets in a group, pass the name of the group to the `bake`
command.

```console
$ docker buildx bake all
```

## Pattern matching for targets and groups

Bake supports shell-style wildcard patterns when specifying target or grouped targets.
This makes it easier to build multiple targets without listing each one explicitly.

Supported patterns:

- `*` matches any sequence of characters
- `?` matches any single character
- `[abc]` matches any character in brackets

> Note
>
> Always wrap wildcard patterns in quotes. Without quotes, your shell will expand the
> wildcard to match files in the current directory, which usually causes errors.

Examples:

```console
# Match all targets starting with 'foo-'
$ docker buildx bake "foo-*"

# Match all targets
$ docker buildx bake "*"

# Matches: foo-baz, foo-caz, foo-daz, etc.
$ docker buildx bake "foo-?az"

# Matches: foo-bar, boo-bar
$ docker buildx bake "[fb]oo-bar"

# Matches: mtx-a-b-d, mtx-a-b-e, mtx-a-b-f
$ docker buildx bake "mtx-a-b-*"
```

You can also combine multiple patterns:

```console
$ docker buildx bake "foo*" "tests"
```

## Additional resources

Refer to the following pages to learn more about Bake's features:

- Learn how to use [variables](https://docs.docker.com/build/bake/variables/) in Bake to make your build
  configuration more flexible.
- Learn how you can use matrices to build multiple images with different
  configurations in [Matrices](https://docs.docker.com/build/bake/matrices/).
- Head to the
  [Bake file reference](https://docs.docker.com/build/bake/reference/) to learn about all
  the properties you can set in a Bake file, and its syntax.

---

# Variables in Bake

# Variables in Bake

   Table of contents

---

You can define and use variables in a Bake file to set attribute values,
interpolate them into other values, and perform arithmetic operations.
Variables can be defined with default values, and can be overridden with
environment variables.

## Using variables as attribute values

Use the `variable` block to define a variable.

docker-bake.hcl

```hcl
variable "TAG" {
  default = "docker.io/username/webapp:latest"
}
```

The following example shows how to use the `TAG` variable in a target.

docker-bake.hcl

```hcl
target "webapp" {
  context = "."
  dockerfile = "Dockerfile"
  tags = [ TAG ]
}
```

## Interpolate variables into values

Bake supports string interpolation of variables into values. You can use the
`${}` syntax to interpolate a variable into a value. The following example
defines a `TAG` variable with a value of `latest`.

docker-bake.hcl

```hcl
variable "TAG" {
  default = "latest"
}
```

To interpolate the `TAG` variable into the value of an attribute, use the
`${TAG}` syntax.

docker-bake.hcl

```hcl
group "default" {
  targets = [ "webapp" ]
}

variable "TAG" {
  default = "latest"
}

target "webapp" {
  context = "."
  dockerfile = "Dockerfile"
  tags = ["docker.io/username/webapp:${TAG}"]
}
```

Printing the Bake file with the `--print` flag shows the interpolated value in
the resolved build configuration.

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
      "tags": ["docker.io/username/webapp:latest"]
    }
  }
}
```

## Validating variables

To verify that the value of a variable conforms to an expected type, value
range, or other condition, you can define custom validation rules using the
`validation` block.

In the following example, validation is used to enforce a numeric constraint on
a variable value; the `PORT` variable must be 1024 or greater.

docker-bake.hcl

```hcl
# Define a variable `PORT` with a default value and a validation rule
variable "PORT" {
  default = 3000  # Default value assigned to `PORT`

  # Validation block to ensure `PORT` is a valid number within the acceptable range
  validation {
    condition = PORT >= 1024  # Ensure `PORT` is at least 1024
    error_message = "The variable 'PORT' must be 1024 or greater."  # Error message for invalid values
  }
}
```

If the `condition` expression evaluates to `false`, the variable value is
considered invalid, whereby the build invocation fails and `error_message` is
emitted. For example, if `PORT=443`, the condition evaluates to `false`, and
the error is raised.

Values are coerced into the expected type before the validation is set. This
ensures that any overrides set with environment variables work as expected.

### Validate multiple conditions

To evaluate more than one condition, define multiple `validation` blocks for
the variable. All conditions must be `true`.

Here’s an example:

docker-bake.hcl

```hcl
# Define a variable `VAR` with multiple validation rules
variable "VAR" {
  # First validation block: Ensure the variable is not empty
  validation {
    condition = VAR != ""
    error_message = "The variable 'VAR' must not be empty."
  }

  # Second validation block: Ensure the value contains only alphanumeric characters
  validation {
    # VAR and the regex match must be identical:
    condition = VAR == regex("[a-zA-Z0-9]+", VAR)
    error_message = "The variable 'VAR' can only contain letters and numbers."
  }
}
```

This example enforces:

- The variable must not be empty.
- The variable must match a specific character set.

For invalid inputs like `VAR="hello@world"`, the validation would fail.

### Validating variable dependencies

You can reference other Bake variables in your condition expression, enabling
validations that enforce dependencies between variables. This ensures that
dependent variables are set correctly before proceeding.

Here’s an example:

docker-bake.hcl

```hcl
# Define a variable `FOO`
variable "FOO" {}

# Define a variable `BAR` with a validation rule that references `FOO`
variable "BAR" {
  # Validation block to ensure `FOO` is set if `BAR` is used
  validation {
    condition = FOO != ""  # Check if `FOO` is not an empty string
    error_message = "The variable 'BAR' requires 'FOO' to be set."
  }
}
```

This configuration ensures that the `BAR` variable can only be used if `FOO`
has been assigned a non-empty value. Attempting to build without setting `FOO`
will trigger the validation error.

## Escape variable interpolation

If you want to bypass variable interpolation when parsing the Bake definition,
use double dollar signs (`$${VARIABLE}`).

docker-bake.hcl

```hcl
target "webapp" {
  dockerfile-inline = <<EOF
  FROM alpine
  ARG TARGETARCH
  RUN echo "Building for $${TARGETARCH/amd64/x64}"
  EOF
  platforms = ["linux/amd64", "linux/arm64"]
}
```

```console
$ docker buildx bake --progress=plain
...
#8 [linux/arm64 2/2] RUN echo "Building for arm64"
#8 0.036 Building for arm64
#8 DONE 0.0s

#9 [linux/amd64 2/2] RUN echo "Building for x64"
#9 0.046 Building for x64
#9 DONE 0.1s
...
```

## Using variables in variables across files

When multiple files are specified, one file can use variables defined in
another file. In the following example, the `vars.hcl` file defines a
`BASE_IMAGE` variable with a default value of `docker.io/library/alpine`.

vars.hcl

```hcl
variable "BASE_IMAGE" {
  default = "docker.io/library/alpine"
}
```

The following `docker-bake.hcl` file defines a `BASE_LATEST` variable that
references the `BASE_IMAGE` variable.

docker-bake.hcl

```hcl
variable "BASE_LATEST" {
  default = "${BASE_IMAGE}:latest"
}

target "webapp" {
  contexts = {
    base = BASE_LATEST
  }
}
```

When you print the resolved build configuration, using the `-f` flag to specify
the `vars.hcl` and `docker-bake.hcl` files, you see that the `BASE_LATEST`
variable is resolved to `docker.io/library/alpine:latest`.

```console
$ docker buildx bake -f vars.hcl -f docker-bake.hcl --print app
```

```json
{
  "target": {
    "webapp": {
      "context": ".",
      "contexts": {
        "base": "docker.io/library/alpine:latest"
      },
      "dockerfile": "Dockerfile"
    }
  }
}
```

## Additional resources

Here are some additional resources that show how you can use variables in Bake:

- You can override `variable` values using environment variables. See
  [Overriding configurations](https://docs.docker.com/build/bake/overrides/#environment-variables) for more
  information.
- You can refer to and use global variables in functions. See [HCL
  functions](https://docs.docker.com/build/bake/funcs/#variables-in-functions)
- You can use variable values when evaluating expressions. See [Expression
  evaluation](https://docs.docker.com/build/bake/expressions/#expressions-with-variables)

---

# Bake

# Bake

   Table of contents

---

Bake is a feature of Docker Buildx that lets you define your build configuration
using a declarative file, as opposed to specifying a complex CLI expression. It
also lets you run multiple builds concurrently with a single invocation.

A Bake file can be written in HCL, JSON, or YAML formats, where the YAML format
is an extension of a Docker Compose file. Here's an example Bake file in HCL
format:

docker-bake.hcl

```hcl
group "default" {
  targets = ["frontend", "backend"]
}

target "frontend" {
  context = "./frontend"
  dockerfile = "frontend.Dockerfile"
  args = {
    NODE_VERSION = "22"
  }
  tags = ["myapp/frontend:latest"]
}

target "backend" {
  context = "./backend"
  dockerfile = "backend.Dockerfile"
  args = {
    GO_VERSION = "1.25"
  }
  tags = ["myapp/backend:latest"]
}
```

The `group` block defines a group of targets that can be built concurrently.
Each `target` block defines a build target with its own configuration, such as
the build context, Dockerfile, and tags.

To invoke a build using the above Bake file, you can run:

```console
$ docker buildx bake
```

This executes the `default` group, which builds the `frontend` and `backend`
targets concurrently.

## Get started

To learn how to get started with Bake, head over to the [Bake introduction](https://docs.docker.com/build/bake/introduction/).

---

# Docker container driver

> The Docker container driver runs BuildKit in a container image.

# Docker container driver

   Table of contents

---

The Docker container driver allows creation of a managed and customizable
BuildKit environment in a dedicated Docker container.

Using the Docker container driver has a couple of advantages over the default
Docker driver. For example:

- Specify custom BuildKit versions to use.
- Build multi-arch images, see [QEMU](#qemu)
- Advanced options for
  [cache import and export](https://docs.docker.com/build/cache/backends/)

## Synopsis

Run the following command to create a new builder, named `container`, that uses
the Docker container driver:

```console
$ docker buildx create \
  --name container \
  --driver=docker-container \
  --driver-opt=[key=value,...]
container
```

The following table describes the available driver-specific options that you can
pass to `--driver-opt`:

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| image | String |  | Sets the BuildKit image to use for the container. |
| memory | String |  | Sets the amount of memory the container can use. |
| memory-swap | String |  | Sets the memory swap limit for the container. |
| cpu-quota | String |  | Imposes a CPU CFS quota on the container. |
| cpu-period | String |  | Sets the CPU CFS scheduler period for the container. |
| cpu-shares | String |  | Configures CPU shares (relative weight) of the container. |
| cpuset-cpus | String |  | Limits the set of CPU cores the container can use. |
| cpuset-mems | String |  | Limits the set of CPU memory nodes the container can use. |
| default-load | Boolean | false | Automatically load images to the Docker Engine image store. |
| network | String |  | Sets the network mode for the container. |
| cgroup-parent | String | /docker/buildx | Sets the cgroup parent of the container if Docker is using the "cgroupfs" driver. |
| restart-policy | String | unless-stopped | Sets the container'srestart policy. |
| env.<key> | String |  | Sets the environment variablekeyto the specifiedvaluein the container. |
| provenance-add-gha | Boolean | true | Automatically writes GitHub Actions context into the builder for provenance. |

Before you configure the resource limits for the container,
read about
[configuring runtime resource constraints for containers](https://docs.docker.com/engine/containers/resource_constraints/).

## Usage

When you run a build, Buildx pulls the specified `image` (by default,
[moby/buildkit](https://hub.docker.com/r/moby/buildkit)).
When the container has started, Buildx submits the build submitted to the
containerized build server.

```console
$ docker buildx build -t <image> --builder=container .
WARNING: No output specified with docker-container driver. Build result will only remain in the build cache. To push result image into registry use --push or to load image into docker use --load
#1 [internal] booting buildkit
#1 pulling image moby/buildkit:buildx-stable-1
#1 pulling image moby/buildkit:buildx-stable-1 1.9s done
#1 creating container buildx_buildkit_container0
#1 creating container buildx_buildkit_container0 0.5s done
#1 DONE 2.4s
...
```

## Cache persistence

The `docker-container` driver supports cache persistence, as it stores all the
BuildKit state and related cache into a dedicated Docker volume.

To persist the `docker-container` driver's cache, even after recreating the
driver using `docker buildx rm` and `docker buildx create`, you can destroy the
builder using the `--keep-state` flag:

For example, to create a builder named `container` and then remove it while
persisting state:

```console
# setup a builder
$ docker buildx create --name=container --driver=docker-container --use --bootstrap
container
$ docker buildx ls
NAME/NODE       DRIVER/ENDPOINT              STATUS   BUILDKIT PLATFORMS
container *     docker-container
  container0    desktop-linux                running  v0.10.5  linux/amd64
$ docker volume ls
DRIVER    VOLUME NAME
local     buildx_buildkit_container0_state

# remove the builder while persisting state
$ docker buildx rm --keep-state container
$ docker volume ls
DRIVER    VOLUME NAME
local     buildx_buildkit_container0_state

# the newly created driver with the same name will have all the state of the previous one!
$ docker buildx create --name=container --driver=docker-container --use --bootstrap
container
```

## QEMU

The `docker-container` driver supports using [QEMU](https://www.qemu.org/)
(user mode) to build non-native platforms. Use the `--platform` flag to specify
which architectures that you want to build for.

For example, to build a Linux image for `amd64` and `arm64`:

```console
$ docker buildx build \
  --builder=container \
  --platform=linux/amd64,linux/arm64 \
  -t <registry>/<image> \
  --push .
```

> Note
>
> Emulation with QEMU can be much slower than native builds, especially for
> compute-heavy tasks like compilation and compression or decompression.

## Custom network

You can customize the network that the builder container uses. This is useful
if you need to use a specific network for your builds.

For example, let's
[create a network](https://docs.docker.com/reference/cli/docker/network/create/)
named `foonet`:

```console
$ docker network create foonet
```

Now create a
[docker-containerbuilder](https://docs.docker.com/reference/cli/docker/buildx/create/)
that will use this network:

```console
$ docker buildx create --use \
  --name mybuilder \
  --driver docker-container \
  --driver-opt "network=foonet"
```

Boot and
[inspectmybuilder](https://docs.docker.com/reference/cli/docker/buildx/inspect/):

```console
$ docker buildx inspect --bootstrap
```

[Inspect the builder container](https://docs.docker.com/reference/cli/docker/inspect/)
and see what network is being used:

```console
$ docker inspect buildx_buildkit_mybuilder0 --format={{.NetworkSettings.Networks}}
map[foonet:0xc00018c0c0]
```

## Further reading

For more information on the Docker container driver, see the
[buildx reference](https://docs.docker.com/reference/cli/docker/buildx/create/#driver).

---

# Docker driver

> The Docker driver is the default driver. It uses the BuildKit bundled with the Docker Engine.

# Docker driver

   Table of contents

---

The Buildx Docker driver is the default driver. It uses the BuildKit server
components built directly into the Docker Engine. The Docker driver requires no
configuration.

Unlike the other drivers, builders using the Docker driver can't be manually
created. They're only created automatically from the Docker context.

Images built with the Docker driver are automatically loaded to the local image
store.

## Synopsis

```console
# The Docker driver is used by buildx by default
docker buildx build .
```

It's not possible to configure which BuildKit version to use, or to pass any
additional BuildKit parameters to a builder using the Docker driver. The
BuildKit version and parameters are preset by the Docker Engine internally.

If you need additional configuration and flexibility, consider using the
[Docker container driver](https://docs.docker.com/build/builders/drivers/docker-container/).

## Further reading

For more information on the Docker driver, see the
[buildx reference](https://docs.docker.com/reference/cli/docker/buildx/create/#driver).

---

# Kubernetes driver

> The Kubernetes driver lets you run BuildKit in a Kubernetes cluster. You can connect to, and run your builds in, the cluster using Buildx.

# Kubernetes driver

   Table of contents

---

The Kubernetes driver lets you connect your local development or CI
environments to builders in a Kubernetes cluster to allow access to more
powerful compute resources, optionally on multiple native architectures.

## Synopsis

Run the following command to create a new builder, named `kube`, that uses the
Kubernetes driver:

```console
$ docker buildx create \
  --bootstrap \
  --name=kube \
  --driver=kubernetes \
  --driver-opt=[key=value,...]
```

The following table describes the available driver-specific options that you
can pass to `--driver-opt`:

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| image | String |  | Sets the image to use for running BuildKit. |
| namespace | String | Namespace in current Kubernetes context | Sets the Kubernetes namespace. |
| default-load | Boolean | false | Automatically load images to the Docker Engine image store. |
| replicas | Integer | 1 | Sets the number of Pod replicas to create. Seescaling BuildKit |
| requests.cpu | CPU units |  | Sets the request CPU value specified in units of Kubernetes CPU. For examplerequests.cpu=100morrequests.cpu=2 |
| requests.memory | Memory size |  | Sets the request memory value specified in bytes or with a valid suffix. For examplerequests.memory=500Miorrequests.memory=4G |
| requests.ephemeral-storage | Storage size |  | Sets the request ephemeral-storage value specified in bytes or with a valid suffix. For examplerequests.ephemeral-storage=2Gi |
| limits.cpu | CPU units |  | Sets the limit CPU value specified in units of Kubernetes CPU. For examplerequests.cpu=100morrequests.cpu=2 |
| limits.memory | Memory size |  | Sets the limit memory value specified in bytes or with a valid suffix. For examplerequests.memory=500Miorrequests.memory=4G |
| limits.ephemeral-storage | Storage size |  | Sets the limit ephemeral-storage value specified in bytes or with a valid suffix. For examplerequests.ephemeral-storage=100M |
| buildkit-root-volume-memory | Memory size | Using regular file system | Mounts/var/lib/buildkiton anemptyDirmemory-backed volume, withSizeLimitas the value. For example,buildkit-root-folder-memory=6G |
| nodeselector | CSV string |  | Sets the pod'snodeSelectorlabel(s). Seenode assignment. |
| annotations | CSV string |  | Sets additional annotations on the deployments and pods. |
| labels | CSV string |  | Sets additional labels on the deployments and pods. |
| tolerations | CSV string |  | Configures the pod's taint toleration. Seenode assignment. |
| serviceaccount | String |  | Sets the pod'sserviceAccountName. |
| schedulername | String |  | Sets the scheduler responsible for scheduling the pod. |
| timeout | Time | 120s | Set the timeout limit that determines how long Buildx will wait for pods to be provisioned before a build. |
| rootless | Boolean | false | Run the container as a non-root user. Seerootless mode. |
| loadbalance | String | sticky | Load-balancing strategy (stickyorrandom). If set tosticky, the pod is chosen using the hash of the context path. |
| qemu.install | Boolean | false | Install QEMU emulation for multi platforms support. SeeQEMU. |
| qemu.image | String | tonistiigi/binfmt:latest | Sets the QEMU emulation image. SeeQEMU. |

## Scaling BuildKit

One of the main advantages of the Kubernetes driver is that you can scale the
number of builder replicas up and down to handle increased build load. Scaling
is configurable using the following driver options:

- `replicas=N`
  This scales the number of BuildKit pods to the desired size. By default, it
  only creates a single pod. Increasing the number of replicas lets you take
  advantage of multiple nodes in your cluster.
- `requests.cpu`, `requests.memory`, `requests.ephemeral-storage`, `limits.cpu`, `limits.memory`, `limits.ephemeral-storage`
  These options allow requesting and limiting the resources available to each
  BuildKit pod [according to the official Kubernetes documentation](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/).

For example, to create 4 replica BuildKit pods:

```console
$ docker buildx create \
  --bootstrap \
  --name=kube \
  --driver=kubernetes \
  --driver-opt=namespace=buildkit,replicas=4
```

Listing the pods, you get this:

```console
$ kubectl -n buildkit get deployments
NAME    READY   UP-TO-DATE   AVAILABLE   AGE
kube0   4/4     4            4           8s

$ kubectl -n buildkit get pods
NAME                     READY   STATUS    RESTARTS   AGE
kube0-6977cdcb75-48ld2   1/1     Running   0          8s
kube0-6977cdcb75-rkc6b   1/1     Running   0          8s
kube0-6977cdcb75-vb4ks   1/1     Running   0          8s
kube0-6977cdcb75-z4fzs   1/1     Running   0          8s
```

Additionally, you can use the `loadbalance=(sticky|random)` option to control
the load-balancing behavior when there are multiple replicas. `random` selects
random nodes from the node pool, providing an even workload distribution across
replicas. `sticky` (the default) attempts to connect the same build performed
multiple times to the same node each time, ensuring better use of local cache.

For more information on scalability, see the options for
[docker buildx create](https://docs.docker.com/reference/cli/docker/buildx/create/#driver-opt).

## Node assignment

The Kubernetes driver allows you to control the scheduling of BuildKit pods
using the `nodeSelector` and `tolerations` driver options.
You can also set the `schedulername` option if you want to use a custom scheduler altogether.

You can use the `annotations` and `labels` driver options to apply additional
metadata to the deployments and pods that's hosting your builders.

The value of the `nodeSelector` parameter is a comma-separated string of
key-value pairs, where the key is the node label and the value is the label
text. For example: `"nodeselector=kubernetes.io/arch=arm64"`

The `tolerations` parameter is a semicolon-separated list of taints. It accepts
the same values as the Kubernetes manifest. Each `tolerations` entry specifies
a taint key and the value, operator, or effect. For example:
`"tolerations=key=foo,value=bar;key=foo2,operator=exists;key=foo3,effect=NoSchedule"`

These options accept CSV-delimited strings as values. Due to quoting rules for
shell commands, you must wrap the values in single quotes. You can even wrap all
of `--driver-opt` in single quotes, for example:

```console
$ docker buildx create \
  --bootstrap \
  --name=kube \
  --driver=kubernetes \
  '--driver-opt="nodeselector=label1=value1,label2=value2","tolerations=key=key1,value=value1"'
```

## Multi-platform builds

The Kubernetes driver has support for creating
[multi-platform images](https://docs.docker.com/build/building/multi-platform/),
either using QEMU or by leveraging the native architecture of nodes.

### QEMU

Like the `docker-container` driver, the Kubernetes driver also supports using
[QEMU](https://www.qemu.org/) (user
mode) to build images for non-native platforms. Include the `--platform` flag
and specify which platforms you want to output to.

For example, to build a Linux image for `amd64` and `arm64`:

```console
$ docker buildx build \
  --builder=kube \
  --platform=linux/amd64,linux/arm64 \
  -t <user>/<image> \
  --push .
```

> Warning
>
> QEMU performs full-CPU emulation of non-native platforms, which is much
> slower than native builds. Compute-heavy tasks like compilation and
> compression/decompression will likely take a large performance hit.

Using a custom BuildKit image or invoking non-native binaries in builds may
require that you explicitly turn on QEMU using the `qemu.install` option when
creating the builder:

```console
$ docker buildx create \
  --bootstrap \
  --name=kube \
  --driver=kubernetes \
  --driver-opt=namespace=buildkit,qemu.install=true
```

### Native

If you have access to cluster nodes of different architectures, the Kubernetes
driver can take advantage of these for native builds. To do this, use the
`--append` flag of `docker buildx create`.

First, create your builder with explicit support for a single architecture, for
example `amd64`:

```console
$ docker buildx create \
  --bootstrap \
  --name=kube \
  --driver=kubernetes \
  --platform=linux/amd64 \
  --node=builder-amd64 \
  --driver-opt=namespace=buildkit,nodeselector="kubernetes.io/arch=amd64"
```

This creates a Buildx builder named `kube`, containing a single builder node
named `builder-amd64`. Assigning a node name using `--node` is optional. Buildx
generates a random node name if you don't provide one.

Note that the Buildx concept of a node isn't the same as the Kubernetes concept
of a node. A Buildx node in this case could connect multiple Kubernetes nodes of
the same architecture together.

With the `kube` builder created, you can now introduce another architecture into
the mix using `--append`. For example, to add `arm64`:

```console
$ docker buildx create \
  --append \
  --bootstrap \
  --name=kube \
  --driver=kubernetes \
  --platform=linux/arm64 \
  --node=builder-arm64 \
  --driver-opt=namespace=buildkit,nodeselector="kubernetes.io/arch=arm64"
```

Listing your builders shows both nodes for the `kube` builder:

```console
$ docker buildx ls
NAME/NODE       DRIVER/ENDPOINT                                         STATUS   PLATFORMS
kube            kubernetes
  builder-amd64 kubernetes:///kube?deployment=builder-amd64&kubeconfig= running  linux/amd64*, linux/amd64/v2, linux/amd64/v3, linux/386
  builder-arm64 kubernetes:///kube?deployment=builder-arm64&kubeconfig= running  linux/arm64*
```

You can now build multi-arch `amd64` and `arm64` images, by specifying those
platforms together in your build command:

```console
$ docker buildx build --builder=kube --platform=linux/amd64,linux/arm64 -t <user>/<image> --push .
```

You can repeat the `buildx create --append` command for as many architectures
that you want to support.

## Rootless mode

The Kubernetes driver supports rootless mode. For more information on how
rootless mode works, and its requirements, refer to the
[Rootless Buildkit documentation](https://github.com/moby/buildkit/blob/master/docs/rootless.md).

To turn it on in your cluster, you can use the `rootless=true` driver option:

```console
$ docker buildx create \
  --name=kube \
  --driver=kubernetes \
  --driver-opt=namespace=buildkit,rootless=true
```

This will create your pods without `securityContext.privileged`.

Requires Kubernetes version 1.19 or later. Using Ubuntu as the host kernel is
recommended.

## Example: Creating a Buildx builder in Kubernetes

This guide shows you how to:

- Create a namespace for your Buildx resources
- Create a Kubernetes builder.
- List the available builders
- Build an image using your Kubernetes builders

Prerequisites:

- You have an existing Kubernetes cluster. If you don't already have one, you
  can follow along by installing
  [minikube](https://minikube.sigs.k8s.io/docs/).
- The cluster you want to connect to is accessible via the `kubectl` command,
  with the `KUBECONFIG` environment variable
  [set appropriately](https://kubernetes.io/docs/tasks/access-application-cluster/configure-access-multiple-clusters/#set-the-kubeconfig-environment-variable) if necessary.

1. Create a `buildkit` namespace.
  Creating a separate namespace helps keep your Buildx resources separate from
  other resources in the cluster.
  ```console
  $ kubectl create namespace buildkit
  namespace/buildkit created
  ```
2. Create a new builder with the Kubernetes driver:
  ```console
  $ docker buildx create \
    --bootstrap \
    --name=kube \
    --driver=kubernetes \
    --driver-opt=namespace=buildkit
  ```
  > Note
  >
  > Remember to specify the namespace in driver options.
3. List available builders using `docker buildx ls`
  ```console
  $ docker buildx ls
  NAME/NODE                DRIVER/ENDPOINT STATUS  PLATFORMS
  kube                     kubernetes
    kube0-6977cdcb75-k9h9m                 running linux/amd64, linux/amd64/v2, linux/amd64/v3, linux/386
  default *                docker
    default                default         running linux/amd64, linux/386
  ```
4. Inspect the running pods created by the build driver with `kubectl`.
  ```console
  $ kubectl -n buildkit get deployments
  NAME    READY   UP-TO-DATE   AVAILABLE   AGE
  kube0   1/1     1            1           32s
  $ kubectl -n buildkit get pods
  NAME                     READY   STATUS    RESTARTS   AGE
  kube0-6977cdcb75-k9h9m   1/1     Running   0          32s
  ```
  The build driver creates the necessary resources on your cluster in the
  specified namespace (in this case, `buildkit`), while keeping your driver
  configuration locally.
5. Use your new builder by including the `--builder` flag when running buildx
  commands. For example: :
  ```console
  # Replace <registry> with your Docker username
  # and <image> with the name of the image you want to build
  docker buildx build \
    --builder=kube \
    -t <registry>/<image> \
    --push .
  ```

That's it: you've now built an image from a Kubernetes pod, using Buildx.

## Further reading

For more information on the Kubernetes driver, see the
[buildx reference](https://docs.docker.com/reference/cli/docker/buildx/create/#driver).

---

# Remote driver

> The remote driver lets you connect to a remote BuildKit instance that you set up and configure manually.

# Remote driver

   Table of contents

---

The Buildx remote driver allows for more complex custom build workloads,
allowing you to connect to externally managed BuildKit instances. This is useful
for scenarios that require manual management of the BuildKit daemon, or where a
BuildKit daemon is exposed from another source.

## Synopsis

```console
$ docker buildx create \
  --name remote \
  --driver remote \
  tcp://localhost:1234
```

The following table describes the available driver-specific options that you can
pass to `--driver-opt`:

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| key | String |  | Sets the TLS client key. |
| cert | String |  | Absolute path to the TLS client certificate to present tobuildkitd. |
| cacert | String |  | Absolute path to the TLS certificate authority used for validation. |
| servername | String | Endpoint hostname. | TLS server name used in requests. |
| default-load | Boolean | false | Automatically load images to the Docker Engine image store. |

## Example: Remote BuildKit over Unix sockets

This guide shows you how to create a setup with a BuildKit daemon listening on a
Unix socket, and have Buildx connect through it.

1. Ensure that [BuildKit](https://github.com/moby/buildkit) is installed.
  For example, you can launch an instance of buildkitd with:
  ```console
  $ sudo ./buildkitd --group $(id -gn) --addr unix://$HOME/buildkitd.sock
  ```
  Alternatively, refer to the [Rootless Buildkit documentation](https://github.com/moby/buildkit/blob/master/docs/rootless.md)
  for running buildkitd in rootless mode, or [the BuildKit systemd examples](https://github.com/moby/buildkit/tree/master/examples/systemd)
  for running it as a systemd service.
2. Check that you have a Unix socket that you can connect to.
  ```console
  $ ls -lh /home/user/buildkitd.sock
  srw-rw---- 1 root user 0 May  5 11:04 /home/user/buildkitd.sock
  ```
3. Connect Buildx to it using the remote driver:
  ```console
  $ docker buildx create \
    --name remote-unix \
    --driver remote \
    unix://$HOME/buildkitd.sock
  ```
4. List available builders with `docker buildx ls`. You should then see
  `remote-unix` among them:
  ```console
  $ docker buildx ls
  NAME/NODE           DRIVER/ENDPOINT                        STATUS  PLATFORMS
  remote-unix         remote
    remote-unix0      unix:///home/.../buildkitd.sock        running linux/amd64, linux/amd64/v2, linux/amd64/v3, linux/386
  default *           docker
    default           default                                running linux/amd64, linux/386
  ```

You can switch to this new builder as the default using
`docker buildx use remote-unix`, or specify it per build using `--builder`:

```console
$ docker buildx build --builder=remote-unix -t test --load .
```

Remember that you need to use the `--load` flag if you want to load the build
result into the Docker daemon.

## Example: Remote BuildKit in Docker container

This guide will show you how to create setup similar to the `docker-container`
driver, by manually booting a BuildKit Docker container and connecting to it
using the Buildx remote driver. This procedure will manually create a container
and access it via it's exposed port. (You'd probably be better of just using the
`docker-container` driver that connects to BuildKit through the Docker daemon,
but this is for illustration purposes.)

1. Generate certificates for BuildKit.
  You can use this [bake definition](https://github.com/moby/buildkit/blob/master/examples/create-certs)
  as a starting point:
  ```console
  SAN="localhost 127.0.0.1" docker buildx bake "https://github.com/moby/buildkit.git#master:examples/create-certs"
  ```
  Note that while it's possible to expose BuildKit over TCP without using
  TLS, it's not recommended. Doing so allows arbitrary access to BuildKit
  without credentials.
2. With certificates generated in `.certs/`, startup the container:
  ```console
  $ docker run -d --rm \
    --name=remote-buildkitd \
    --privileged \
    -p 1234:1234 \
    -v $PWD/.certs:/etc/buildkit/certs \
    moby/buildkit:latest \
    --addr tcp://0.0.0.0:1234 \
    --tlscacert /etc/buildkit/certs/daemon/ca.pem \
    --tlscert /etc/buildkit/certs/daemon/cert.pem \
    --tlskey /etc/buildkit/certs/daemon/key.pem
  ```
  This command starts a BuildKit container and exposes the daemon's port 1234
  to localhost.
3. Connect to this running container using Buildx:
  ```console
  $ docker buildx create \
    --name remote-container \
    --driver remote \
    --driver-opt cacert=${PWD}/.certs/client/ca.pem,cert=${PWD}/.certs/client/cert.pem,key=${PWD}/.certs/client/key.pem,servername=TLS_SERVER_NAME \
    tcp://localhost:1234
  ```
  Alternatively, use the `docker-container://` URL scheme to connect to the
  BuildKit container without specifying a port:
  ```console
  $ docker buildx create \
    --name remote-container \
    --driver remote \
    docker-container://remote-container
  ```

## Example: Remote BuildKit in Kubernetes

This guide will show you how to create a setup similar to the `kubernetes`
driver by manually creating a BuildKit `Deployment`. While the `kubernetes`
driver will do this under-the-hood, it might sometimes be desirable to scale
BuildKit manually. Additionally, when executing builds from inside Kubernetes
pods, the Buildx builder will need to be recreated from within each pod or
copied between them.

1. Create a Kubernetes deployment of `buildkitd` by following the instructions
  [in the BuildKit documentation](https://github.com/moby/buildkit/tree/master/examples/kubernetes).
  Create certificates for the BuildKit daemon and client using the
  [create-certs.sh](https://github.com/moby/buildkit/blob/master/examples/kubernetes/create-certs.sh),
  script and create a deployment of BuildKit pods with a service that connects
  to them.
2. Assuming that the service is called `buildkitd`, create a remote builder in
  Buildx, ensuring that the listed certificate files are present:
  ```console
  $ docker buildx create \
    --name remote-kubernetes \
    --driver remote \
    --driver-opt cacert=${PWD}/.certs/client/ca.pem,cert=${PWD}/.certs/client/cert.pem,key=${PWD}/.certs/client/key.pem \
    tcp://buildkitd.default.svc:1234
  ```

Note that this only works internally, within the cluster, since the BuildKit
setup guide only creates a `ClusterIP` service. To access a builder remotely,
you can set up and use an ingress, which is outside the scope of this guide.

### Debug a remote builder in Kubernetes

If you're having trouble accessing a remote builder deployed in Kubernetes, you
can use the `kube-pod://` URL scheme to connect directly to a BuildKit pod
through the Kubernetes API. Note that this method only connects to a single pod
in the deployment.

```console
$ kubectl get pods --selector=app=buildkitd -o json | jq -r '.items[].metadata.name'
buildkitd-XXXXXXXXXX-xxxxx
$ docker buildx create \
  --name remote-container \
  --driver remote \
  kube-pod://buildkitd-XXXXXXXXXX-xxxxx
```

Alternatively, use the port forwarding mechanism of `kubectl`:

```console
$ kubectl port-forward svc/buildkitd 1234:1234
```

Then you can point the remote driver at `tcp://localhost:1234`.

---

# Build drivers

> Build drivers are configurations for how and where the BuildKit backend runs.

# Build drivers

   Table of contents

---

Build drivers are configurations for how and where the BuildKit backend runs.
Driver settings are customizable and allow fine-grained control of the builder.
Buildx supports the following drivers:

- `docker`: uses the BuildKit library bundled into the Docker daemon.
- `docker-container`: creates a dedicated BuildKit container using Docker.
- `kubernetes`: creates BuildKit pods in a Kubernetes cluster.
- `remote`: connects directly to a manually managed BuildKit daemon.

Different drivers support different use cases. The default `docker` driver
prioritizes simplicity and ease of use. It has limited support for advanced
features like caching and output formats, and isn't configurable. Other drivers
provide more flexibility and are better at handling advanced scenarios.

The following table outlines some differences between drivers.

| Feature | docker | docker-container | kubernetes | remote |
| --- | --- | --- | --- | --- |
| Automatically load image | ✅ |  |  |  |
| Cache export | ✅* | ✅ | ✅ | ✅ |
| Tarball output |  | ✅ | ✅ | ✅ |
| Multi-arch images |  | ✅ | ✅ | ✅ |
| BuildKit configuration |  | ✅ | ✅ | Managed externally |

* *Thedockerdriver doesn't support all cache export options.
SeeCache storage backendsfor more information.*

## Loading to local image store

Unlike when using the default `docker` driver, images built using other drivers
aren't automatically loaded into the local image store. If you don't specify an
output, the build result is exported to the build cache only.

To build an image using a non-default driver and load it to the image store,
use the `--load` flag with the build command:

```console
$ docker buildx build --load -t <image> --builder=container .
...
=> exporting to oci image format                                                                                                      7.7s
=> => exporting layers                                                                                                                4.9s
=> => exporting manifest sha256:4e4ca161fa338be2c303445411900ebbc5fc086153a0b846ac12996960b479d3                                      0.0s
=> => exporting config sha256:adf3eec768a14b6e183a1010cb96d91155a82fd722a1091440c88f3747f1f53f                                        0.0s
=> => sending tarball                                                                                                                 2.8s
=> importing to docker
```

With this option, the image is available in the image store after the build finishes:

```console
$ docker image ls
REPOSITORY                       TAG               IMAGE ID       CREATED             SIZE
<image>                          latest            adf3eec768a1   2 minutes ago       197MB
```

### Load by default

Requires: Docker Buildx [0.14.0](https://github.com/docker/buildx/releases/tag/v0.14.0) and later

You can configure the custom build drivers to behave in a similar way to the
default `docker` driver, and load images to the local image store by default.
To do so, set the `default-load` driver option when creating the builder:

```console
$ docker buildx create --driver-opt default-load=true
```

Note that, just like with the `docker` driver, if you specify a different
output format with `--output`, the result will not be loaded to the image store
unless you also explicitly specify `--output type=docker` or use the `--load`
flag.

## What's next

Read about each driver:

- [Docker driver](https://docs.docker.com/build/builders/drivers/docker/)
- [Docker container driver](https://docs.docker.com/build/builders/drivers/docker-container/)
- [Kubernetes driver](https://docs.docker.com/build/builders/drivers/kubernetes/)
- [Remote driver](https://docs.docker.com/build/builders/drivers/remote/)
