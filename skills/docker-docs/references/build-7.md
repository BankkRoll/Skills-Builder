# Container Device Interface (CDI) and more

# Container Device Interface (CDI)

> Using CDI to access GPUs and other devices in your builds

# Container Device Interface (CDI)

   Table of contents

---

The [Container Device Interface (CDI)](https://github.com/cncf-tags/container-device-interface/blob/main/SPEC.md)
is a specification designed to standardize how devices (like GPUs, FPGAs, and
other hardware accelerators) are exposed to and used by containers. The aim is
to provide a more consistent and secure mechanism for using hardware devices in
containerized environments, addressing the challenges associated with
device-specific setups and configurations.

In addition to enabling the container to interact with the device node, CDI also
lets you specify additional configuration for the device, such as environment
variables, host mounts (such as shared objects), and executable hooks.

## Getting started

To get started with CDI, you need to have a compatible environment set up. This
includes having Docker v27+ installed with
[CDI configured](https://docs.docker.com/reference/cli/dockerd/#configure-cdi-devices)
and Buildx v0.22+.

You also need to create the [device specifications using JSON or YAML files](https://github.com/cncf-tags/container-device-interface/blob/main/SPEC.md#cdi-json-specification)
in one of the following locations:

- `/etc/cdi`
- `/var/run/cdi`
- `/etc/buildkit/cdi`

> Note
>
> Location can be changed by setting the `specDirs` option in the `cdi` section
> of the [buildkitd.tomlconfiguration file](https://docs.docker.com/build/buildkit/configure/) if you
> are using BuildKit directly. If you're building using the Docker Daemon with
> the `docker` driver, see
> [Configure CDI devices](https://docs.docker.com/reference/cli/dockerd/#configure-cdi-devices)
> documentation.

> Note
>
> If you are creating a container builder on WSL, you need to ensure that
> [Docker Desktop](https://docs.docker.com/desktop/) is installed and [WSL 2 GPU Paravirtualization](https://docs.docker.com/desktop/features/gpu/#prerequisites)
> is enabled. Buildx v0.27+ is also required to mount the WSL libraries in the
> container.

## Building with a simple CDI specification

Let's start with a simple CDI specification that injects an environment variable
into the build environment and write it to `/etc/cdi/foo.yaml`:

/etc/cdi/foo.yaml

```yaml
cdiVersion: "0.6.0"
kind: "vendor1.com/device"
devices:
- name: foo
  containerEdits:
    env:
    - FOO=injected
```

Inspect the `default` builder to verify that `vendor1.com/device` is detected
as a device:

```console
$ docker buildx inspect
Name:   default
Driver: docker

Nodes:
Name:             default
Endpoint:         default
Status:           running
BuildKit version: v0.23.2
Platforms:        linux/amd64, linux/amd64/v2, linux/amd64/v3, linux/amd64/v4, linux/386
Labels:
 org.mobyproject.buildkit.worker.moby.host-gateway-ip: 172.17.0.1
Devices:
 Name:                  vendor1.com/device=foo
 Automatically allowed: false
GC Policy rule#0:
 All:            false
 Filters:        type==source.local,type==exec.cachemount,type==source.git.checkout
 Keep Duration:  48h0m0s
 Max Used Space: 658.9MiB
GC Policy rule#1:
 All:            false
 Keep Duration:  1440h0m0s
 Reserved Space: 4.657GiB
 Max Used Space: 953.7MiB
 Min Free Space: 2.794GiB
GC Policy rule#2:
 All:            false
 Reserved Space: 4.657GiB
 Max Used Space: 953.7MiB
 Min Free Space: 2.794GiB
GC Policy rule#3:
 All:            true
 Reserved Space: 4.657GiB
 Max Used Space: 953.7MiB
 Min Free Space: 2.794GiB
```

Now let's create a Dockerfile to use this device:

```dockerfile
# syntax=docker/dockerfile:1-labs
FROM busybox
RUN --device=vendor1.com/device \
  env | grep ^FOO=
```

Here we use the
[RUN --devicecommand](https://docs.docker.com/reference/dockerfile/#run---device)
and set `vendor1.com/device` which requests the first device available in the
specification. In this case it uses `foo`, which is the first device in
`/etc/cdi/foo.yaml`.

> Note
>
> [RUN --devicecommand](https://docs.docker.com/reference/dockerfile/#run---device) is only
> featured in [labschannel](https://docs.docker.com/build/buildkit/frontend/#labs-channel) since
> [Dockerfile frontend v1.14.0-labs](https://github.com/moby/buildkit/releases/tag/dockerfile%2F1.14.0-labs)
> and not yet available in stable syntax.

Now let's build this Dockerfile:

```console
$ docker buildx build .
[+] Building 0.4s (5/5) FINISHED                                                                                                        docker:default
 => [internal] load build definition from Dockerfile                                                                                    0.0s
 => => transferring dockerfile: 155B                                                                                                    0.0s
 => resolve image config for docker-image://docker/dockerfile:1-labs                                                                    0.1s
 => CACHED docker-image://docker/dockerfile:1-labs@sha256:9187104f31e3a002a8a6a3209ea1f937fb7486c093cbbde1e14b0fa0d7e4f1b5              0.0s
 => [internal] load metadata for docker.io/library/busybox:latest                                                                       0.1s
 => [internal] load .dockerignore                                                                                                       0.0s
 => => transferring context: 2B                                                                                                         0.0s
ERROR: failed to build: failed to solve: failed to load LLB: device vendor1.com/device=foo is requested by the build but not allowed
```

It fails because the device `vendor1.com/device=foo` is not automatically
allowed by the build as shown in the `buildx inspect` output above:

```text
Devices:
 Name:                  vendor1.com/device=foo
 Automatically allowed: false
```

To allow the device, you can use the
[--allowflag](https://docs.docker.com/reference/cli/docker/buildx/build/#allow)
with the `docker buildx build` command:

```console
$ docker buildx build --allow device .
```

Or you can set the `org.mobyproject.buildkit.device.autoallow` annotation in
the CDI specification to automatically allow the device for all builds:

/etc/cdi/foo.yaml

```yaml
cdiVersion: "0.6.0"
kind: "vendor1.com/device"
devices:
- name: foo
  containerEdits:
    env:
    - FOO=injected
annotations:
  org.mobyproject.buildkit.device.autoallow: true
```

Now running the build again with the `--allow device` flag:

```console
$ docker buildx build --progress=plain --allow device .
#0 building with "default" instance using docker driver

#1 [internal] load build definition from Dockerfile
#1 transferring dockerfile: 159B done
#1 DONE 0.0s

#2 resolve image config for docker-image://docker/dockerfile:1-labs
#2 DONE 0.1s

#3 docker-image://docker/dockerfile:1-labs@sha256:9187104f31e3a002a8a6a3209ea1f937fb7486c093cbbde1e14b0fa0d7e4f1b5
#3 CACHED

#4 [internal] load metadata for docker.io/library/busybox:latest
#4 DONE 0.1s

#5 [internal] load .dockerignore
#5 transferring context: 2B done
#5 DONE 0.0s

#6 [1/2] FROM docker.io/library/busybox:latest@sha256:f85340bf132ae937d2c2a763b8335c9bab35d6e8293f70f606b9c6178d84f42b
#6 CACHED

#7 [2/2] RUN --device=vendor1.com/device   env | grep ^FOO=
#7 0.155 FOO=injected
#7 DONE 0.2s
```

The build is successful and the output shows that the `FOO` environment variable
was injected into the build environment as specified in the CDI specification.

## Set up a container builder with GPU support

In this section, we will show you how to set up a [container builder](https://docs.docker.com/build/builders/drivers/docker-container/)
using NVIDIA GPUs. Since Buildx v0.22, when creating a new container builder, a
GPU request is automatically added to the container builder if the host has GPU
drivers installed in the kernel. This is similar to using
[--gpus=allwith thedocker run](https://docs.docker.com/reference/cli/docker/container/run/#gpus)
command.

Now let's create a container builder named `gpubuilder` using Buildx:

```console
$ docker buildx create --name gpubuilder --driver-opt "image=moby/buildkit:buildx-stable-1-gpu" --bootstrap
#1 [internal] booting buildkit
#1 pulling image moby/buildkit:buildx-stable-1-gpu
#1 pulling image moby/buildkit:buildx-stable-1-gpu 1.0s done
#1 creating container buildx_buildkit_gpubuilder0
#1 creating container buildx_buildkit_gpubuilder0 8.8s done
#1 DONE 9.8s
gpubuilder
```

> Note
>
> We made a specially crafted BuildKit image because the current BuildKit
> release image is based on Alpine that doesn't support NVIDIA drivers. The
> following image is based on Ubuntu and installs the NVIDIA client libraries
> and generates the CDI specification for your GPU in the container builder if
> a device is requested during a build.

Let's inspect this builder:

```console
$ docker buildx inspect gpubuilder
Name:          gpubuilder
Driver:        docker-container
Last Activity: 2025-07-10 08:18:09 +0000 UTC

Nodes:
Name:                  gpubuilder0
Endpoint:              unix:///var/run/docker.sock
Driver Options:        image="moby/buildkit:buildx-stable-1-gpu"
Status:                running
BuildKit daemon flags: --allow-insecure-entitlement=network.host
BuildKit version:      v0.26.2
Platforms:             linux/amd64, linux/amd64/v2, linux/amd64/v3, linux/arm64, linux/riscv64, linux/ppc64le, linux/s390x, linux/386, linux/arm/v7, linux/arm/v6
Labels:
 org.mobyproject.buildkit.worker.executor:         oci
 org.mobyproject.buildkit.worker.hostname:         d6aa9cbe8462
 org.mobyproject.buildkit.worker.network:          host
 org.mobyproject.buildkit.worker.oci.process-mode: sandbox
 org.mobyproject.buildkit.worker.selinux.enabled:  false
 org.mobyproject.buildkit.worker.snapshotter:      overlayfs
Devices:
 Name:      nvidia.com/gpu
 On-Demand: true
GC Policy rule#0:
 All:            false
 Filters:        type==source.local,type==exec.cachemount,type==source.git.checkout
 Keep Duration:  48h0m0s
 Max Used Space: 488.3MiB
GC Policy rule#1:
 All:            false
 Keep Duration:  1440h0m0s
 Reserved Space: 9.313GiB
 Max Used Space: 93.13GiB
 Min Free Space: 188.1GiB
GC Policy rule#2:
 All:            false
 Reserved Space: 9.313GiB
 Max Used Space: 93.13GiB
 Min Free Space: 188.1GiB
GC Policy rule#3:
 All:            true
 Reserved Space: 9.313GiB
 Max Used Space: 93.13GiB
 Min Free Space: 188.1GiB
```

We can see `nvidia.com/gpu` vendor is detected as a device in the builder which
means that drivers were detected.

Optionally you can check if NVIDIA GPU devices are available in the container
using `nvidia-smi`:

```console
$ docker exec -it buildx_buildkit_gpubuilder0 nvidia-smi -L
GPU 0: Tesla T4 (UUID: GPU-6cf00fa7-59ac-16f2-3e83-d24ccdc56f84)
```

## Building with GPU support

Let's create a simple Dockerfile that will use the GPU device:

```dockerfile
# syntax=docker/dockerfile:1-labs
FROM ubuntu
RUN --device=nvidia.com/gpu nvidia-smi -L
```

Now run the build using the `gpubuilder` builder we created earlier:

```console
$ docker buildx --builder gpubuilder build --progress=plain .
#0 building with "gpubuilder" instance using docker-container driver
...

#7 preparing device nvidia.com/gpu
#7 0.000 > apt-get update
...
#7 4.872 > apt-get install -y gpg
...
#7 10.16 Downloading NVIDIA GPG key
#7 10.21 > apt-get update
...
#7 12.15 > apt-get install -y --no-install-recommends nvidia-container-toolkit-base
...
#7 17.80 time="2025-04-15T08:58:16Z" level=info msg="Generated CDI spec with version 0.8.0"
#7 DONE 17.8s

#8 [2/2] RUN --device=nvidia.com/gpu nvidia-smi -L
#8 0.527 GPU 0: Tesla T4 (UUID: GPU-6cf00fa7-59ac-16f2-3e83-d24ccdc56f84)
#8 DONE 1.6s
```

As you might have noticed, the step `#7` is preparing the `nvidia.com/gpu`
device by installing client libraries and the toolkit to generate the CDI
specifications for the GPU.

The `nvidia-smi -L` command is then executed in the container using the GPU
device. The output shows the GPU UUID.

You can check the generated CDI specification within the container builder with
the following command:

```console
$ docker exec -it buildx_buildkit_gpubuilder0 cat /etc/cdi/nvidia.yaml
```

For the EC2 instance [g4dn.xlarge](https://aws.amazon.com/ec2/instance-types/g4/)
used here, it looks like this:

```yaml
cdiVersion: 0.6.0
containerEdits:
  deviceNodes:
  - path: /dev/nvidia-modeset
  - path: /dev/nvidia-uvm
  - path: /dev/nvidia-uvm-tools
  - path: /dev/nvidiactl
  env:
  - NVIDIA_VISIBLE_DEVICES=void
  hooks:
  - args:
    - nvidia-cdi-hook
    - create-symlinks
    - --link
    - ../libnvidia-allocator.so.1::/usr/lib/x86_64-linux-gnu/gbm/nvidia-drm_gbm.so
    hookName: createContainer
    path: /usr/bin/nvidia-cdi-hook
  - args:
    - nvidia-cdi-hook
    - create-symlinks
    - --link
    - libcuda.so.1::/usr/lib/x86_64-linux-gnu/libcuda.so
    hookName: createContainer
    path: /usr/bin/nvidia-cdi-hook
  - args:
    - nvidia-cdi-hook
    - enable-cuda-compat
    - --host-driver-version=570.133.20
    hookName: createContainer
    path: /usr/bin/nvidia-cdi-hook
  - args:
    - nvidia-cdi-hook
    - update-ldcache
    - --folder
    - /usr/lib/x86_64-linux-gnu
    hookName: createContainer
    path: /usr/bin/nvidia-cdi-hook
  mounts:
  - containerPath: /run/nvidia-persistenced/socket
    hostPath: /run/nvidia-persistenced/socket
    options:
    - ro
    - nosuid
    - nodev
    - bind
    - noexec
  - containerPath: /usr/bin/nvidia-cuda-mps-control
    hostPath: /usr/bin/nvidia-cuda-mps-control
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /usr/bin/nvidia-cuda-mps-server
    hostPath: /usr/bin/nvidia-cuda-mps-server
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /usr/bin/nvidia-debugdump
    hostPath: /usr/bin/nvidia-debugdump
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /usr/bin/nvidia-persistenced
    hostPath: /usr/bin/nvidia-persistenced
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /usr/bin/nvidia-smi
    hostPath: /usr/bin/nvidia-smi
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /usr/lib/x86_64-linux-gnu/libcuda.so.570.133.20
    hostPath: /usr/lib/x86_64-linux-gnu/libcuda.so.570.133.20
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /usr/lib/x86_64-linux-gnu/libcudadebugger.so.570.133.20
    hostPath: /usr/lib/x86_64-linux-gnu/libcudadebugger.so.570.133.20
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /usr/lib/x86_64-linux-gnu/libnvidia-allocator.so.570.133.20
    hostPath: /usr/lib/x86_64-linux-gnu/libnvidia-allocator.so.570.133.20
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /usr/lib/x86_64-linux-gnu/libnvidia-cfg.so.570.133.20
    hostPath: /usr/lib/x86_64-linux-gnu/libnvidia-cfg.so.570.133.20
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /usr/lib/x86_64-linux-gnu/libnvidia-gpucomp.so.570.133.20
    hostPath: /usr/lib/x86_64-linux-gnu/libnvidia-gpucomp.so.570.133.20
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /usr/lib/x86_64-linux-gnu/libnvidia-ml.so.570.133.20
    hostPath: /usr/lib/x86_64-linux-gnu/libnvidia-ml.so.570.133.20
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /usr/lib/x86_64-linux-gnu/libnvidia-nscq.so.570.133.20
    hostPath: /usr/lib/x86_64-linux-gnu/libnvidia-nscq.so.570.133.20
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /usr/lib/x86_64-linux-gnu/libnvidia-nvvm.so.570.133.20
    hostPath: /usr/lib/x86_64-linux-gnu/libnvidia-nvvm.so.570.133.20
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /usr/lib/x86_64-linux-gnu/libnvidia-opencl.so.570.133.20
    hostPath: /usr/lib/x86_64-linux-gnu/libnvidia-opencl.so.570.133.20
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /usr/lib/x86_64-linux-gnu/libnvidia-pkcs11-openssl3.so.570.133.20
    hostPath: /usr/lib/x86_64-linux-gnu/libnvidia-pkcs11-openssl3.so.570.133.20
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /usr/lib/x86_64-linux-gnu/libnvidia-pkcs11.so.570.133.20
    hostPath: /usr/lib/x86_64-linux-gnu/libnvidia-pkcs11.so.570.133.20
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /usr/lib/x86_64-linux-gnu/libnvidia-ptxjitcompiler.so.570.133.20
    hostPath: /usr/lib/x86_64-linux-gnu/libnvidia-ptxjitcompiler.so.570.133.20
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /lib/firmware/nvidia/570.133.20/gsp_ga10x.bin
    hostPath: /lib/firmware/nvidia/570.133.20/gsp_ga10x.bin
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /lib/firmware/nvidia/570.133.20/gsp_tu10x.bin
    hostPath: /lib/firmware/nvidia/570.133.20/gsp_tu10x.bin
    options:
    - ro
    - nosuid
    - nodev
    - bind
devices:
- containerEdits:
    deviceNodes:
    - path: /dev/nvidia0
  name: "0"
- containerEdits:
    deviceNodes:
    - path: /dev/nvidia0
  name: GPU-6cf00fa7-59ac-16f2-3e83-d24ccdc56f84
- containerEdits:
    deviceNodes:
    - path: /dev/nvidia0
  name: all
kind: nvidia.com/gpu
```

Congrats on your first build using a GPU device with BuildKit and CDI.

---

# Export binaries

> Using Docker builds to create and export executable binaries

# Export binaries

   Table of contents

---

Did you know that you can use Docker to build your application to standalone
binaries? Sometimes, you don’t want to package and distribute your application
as a Docker image. Use Docker to build your application, and use exporters to
save the output to disk.

The default output format for `docker build` is a container image. That image is
automatically loaded to your local image store, where you can run a container
from that image, or push it to a registry. Under the hood, this uses the default
exporter, called the `docker` exporter.

To export your build results as files instead, you can use the `--output` flag,
or `-o` for short. the `--output` flag lets you change the output format of
your build.

## Export binaries from a build

If you specify a filepath to the `docker build --output` flag, Docker exports
the contents of the build container at the end of the build to the specified
location on your host's filesystem. This uses the `local` [exporter](https://docs.docker.com/build/exporters/local-tar/).

The neat thing about this is that you can use Docker's powerful isolation and
build features to create standalone binaries. This
works well for Go, Rust, and other languages that can compile to a single
binary.

The following example creates a simple Rust program that prints "Hello,
World!", and exports the binary to the host filesystem.

1. Create a new directory for this example, and navigate to it:
  ```console
  $ mkdir hello-world-bin
  $ cd hello-world-bin
  ```
2. Create a Dockerfile with the following contents:
  ```Dockerfile
  # syntax=docker/dockerfile:1
  FROM rust:alpine AS build
  WORKDIR /src
  COPY <<EOT hello.rs
  fn main() {
      println!("Hello World!");
  }
  EOT
  RUN rustc -o /bin/hello hello.rs
  FROM scratch
  COPY --from=build /bin/hello /
  ENTRYPOINT ["/hello"]
  ```
  > Tip
  >
  > The `COPY <<EOT` syntax is a
  > [here-document](https://docs.docker.com/reference/dockerfile/#here-documents).
  > It lets you write multi-line strings in a Dockerfile. Here it's used to
  > create a simple Rust program inline in the Dockerfile.
  This Dockerfile uses a multi-stage build to compile the program in the first
  stage, and then copies the binary to a scratch image in the second. The
  final image is a minimal image that only contains the binary. This use case
  for the `scratch` image is common for creating minimal build artifacts for
  programs that don't require a full operating system to run.
3. Build the Dockerfile and export the binary to the current working directory:
  ```console
  $ docker build --output=. .
  ```
  This command builds the Dockerfile and exports the binary to the current
  working directory. The binary is named `hello`, and it's created in the
  current working directory.

## Exporting multi-platform builds

You use the `local` exporter to export binaries in combination with
[multi-platform builds](https://docs.docker.com/build/building/multi-platform/). This lets you
compile multiple binaries at once, that can be run on any machine of any
architecture, provided that the target platform is supported by the compiler
you use.

Continuing on the example Dockerfile in the
[Export binaries from a build](#export-binaries-from-a-build) section:

```dockerfile
# syntax=docker/dockerfile:1
FROM rust:alpine AS build
WORKDIR /src
COPY <<EOT hello.rs
fn main() {
    println!("Hello World!");
}
EOT
RUN rustc -o /bin/hello hello.rs

FROM scratch
COPY --from=build /bin/hello /
ENTRYPOINT ["/hello"]
```

You can build this Rust program for multiple platforms using the `--platform`
flag with the `docker build` command. In combination with the `--output` flag,
the build exports the binaries for each target to the specified directory.

For example, to build the program for both `linux/amd64` and `linux/arm64`:

```console
$ docker build --platform=linux/amd64,linux/arm64 --output=out .
$ tree out/
out/
├── linux_amd64
│   └── hello
└── linux_arm64
    └── hello

3 directories, 2 files
```

## Additional information

In addition to the `local` exporter, there are other exporters available. To
learn more about the available exporters and how to use them, see the
[exporters](https://docs.docker.com/build/exporters/) documentation.

---

# Multi

> Introduction to what multi-platform builds are and how to execute them using Docker Buildx.

# Multi-platform builds

   Table of contents

---

A multi-platform build refers to a single build invocation that targets
multiple different operating system or CPU architecture combinations. When
building images, this lets you create a single image that can run on multiple
platforms, such as `linux/amd64`, `linux/arm64`, and `windows/amd64`.

## Why multi-platform builds?

Docker solves the "it works on my machine" problem by packaging applications
and their dependencies into containers. This makes it easy to run the same
application on different environments, such as development, testing, and
production.

But containerization by itself only solves part of the problem. Containers
share the host kernel, which means that the code that's running inside the
container must be compatible with the host's architecture. This is why you
can't run a `linux/amd64` container on an arm64 host (without using emulation),
or a Windows container on a Linux host.

Multi-platform builds solve this problem by packaging multiple variants of the
same application into a single image. This enables you to run the same image on
different types of hardware, such as development machines running x86-64 or
ARM-based Amazon EC2 instances in the cloud, without the need for emulation.

### Difference between single-platform and multi-platform images

Multi-platform images have a different structure than single-platform images.
Single-platform images contain a single manifest that points to a single
configuration and a single set of layers. Multi-platform images contain a
manifest list, pointing to multiple manifests, each of which points to a
different configuration and set of layers.

![Multi-platform image structure](https://docs.docker.com/build/images/single-vs-multiplatform-image.svg)  ![Multi-platform image structure](https://docs.docker.com/build/images/single-vs-multiplatform-image.svg)

When you push a multi-platform image to a registry, the registry stores the
manifest list and all the individual manifests. When you pull the image, the
registry returns the manifest list, and Docker automatically selects the
correct variant based on the host's architecture. For example, if you run a
multi-platform image on an ARM-based Raspberry Pi, Docker selects the
`linux/arm64` variant. If you run the same image on an x86-64 laptop, Docker
selects the `linux/amd64` variant (if you're using Linux containers).

## Prerequisites

To build multi-platform images, you first need to make sure that your Docker
environment is set up to support it. There are two ways you can do that:

- You can switch from the "classic" image store to the containerd image store.
- You can create and use a custom builder.

The "classic" image store of the Docker Engine does not support multi-platform
images. Switching to the containerd image store ensures that your Docker Engine
can push, pull, and build multi-platform images.

Creating a custom builder that uses a driver with multi-platform support,
such as the `docker-container` driver, will let you build multi-platform images
without switching to a different image store. However, you still won't be able
to load the multi-platform images you build into your Docker Engine image
store. But you can push them to a container registry directly with `docker build --push`.

The steps for enabling the containerd image store depends on whether you're
using Docker Desktop or Docker Engine standalone:

- If you're using Docker Desktop, enable the containerd image store in the
  [Docker Desktop settings](https://docs.docker.com/desktop/features/containerd/).
- If you're using Docker Engine standalone, enable the containerd image store
  using the
  [daemon configuration file](https://docs.docker.com/engine/storage/containerd/).

To create a custom builder, use the `docker buildx create` command to create a
builder that uses the `docker-container` driver.

```console
$ docker buildx create \
  --name container-builder \
  --driver docker-container \
  --bootstrap --use
```

> Note
>
> Builds with the `docker-container` driver aren't automatically loaded to your
> Docker Engine image store. For more information, see
> [Build
> drivers](https://docs.docker.com/build/builders/drivers/).

If you're using Docker Engine standalone and you need to build multi-platform
images using emulation, you also need to install QEMU, see [Install QEMU
manually](#install-qemu-manually).

## Build multi-platform images

When triggering a build, use the `--platform` flag to define the target
platforms for the build output, such as `linux/amd64` and `linux/arm64`:

```console
$ docker buildx build --platform linux/amd64,linux/arm64 .
```

## Strategies

You can build multi-platform images using three different strategies,
depending on your use case:

1. Using emulation, via [QEMU](#qemu)
2. Use a builder with [multiple native nodes](#multiple-native-nodes)
3. Use [cross-compilation](#cross-compilation) with multi-stage builds

### QEMU

Building multi-platform images under emulation with QEMU is the easiest way to
get started if your builder already supports it. Using emulation requires no
changes to your Dockerfile, and BuildKit automatically detects the
architectures that are available for emulation.

> Note
>
> Emulation with QEMU can be much slower than native builds, especially for
> compute-heavy tasks like compilation and compression or decompression.
>
>
>
> Use [multiple native nodes](#multiple-native-nodes) or
> [cross-compilation](#cross-compilation) instead, if possible.

Docker Desktop supports running and building multi-platform images under
emulation by default. No configuration is necessary as the builder uses the
QEMU that's bundled within the Docker Desktop VM.

#### Install QEMU manually

If you're using a builder outside of Docker Desktop, such as if you're using
Docker Engine on Linux, or a custom remote builder, you need to install QEMU
and register the executable types on the host OS. The prerequisites for
installing QEMU are:

- Linux kernel version 4.8 or later
- `binfmt-support` version 2.1.7 or later
- The QEMU binaries must be statically compiled and registered with the
  `fix_binary` flag

Use the [tonistiigi/binfmt](https://github.com/tonistiigi/binfmt) image to
install QEMU and register the executable types on the host with a single
command:

```console
$ docker run --privileged --rm tonistiigi/binfmt --install all
```

This installs the QEMU binaries and registers them with
[binfmt_misc](https://en.wikipedia.org/wiki/Binfmt_misc), enabling QEMU to
execute non-native file formats for emulation.

Once QEMU is installed and the executable types are registered on the host OS,
they work transparently inside containers. You can verify your registration by
checking if `F` is among the flags in `/proc/sys/fs/binfmt_misc/qemu-*`.

### Multiple native nodes

Using multiple native nodes provide better support for more complicated cases
that QEMU can't handle, and also provides better performance.

You can add additional nodes to a builder using the `--append` flag.

The following command creates a multi-node builder from Docker contexts named
`node-amd64` and `node-arm64`. This example assumes that you've already added
those contexts.

```console
$ docker buildx create --use --name mybuild node-amd64
mybuild
$ docker buildx create --append --name mybuild node-arm64
$ docker buildx build --platform linux/amd64,linux/arm64 .
```

While this approach has advantages over emulation, managing multi-node builders
introduces some overhead of setting up and managing builder clusters.
Alternatively, you can use Docker Build Cloud, a service that provides managed
multi-node builders on Docker's infrastructure. With Docker Build Cloud, you
get native multi-platform ARM and X86 builders without the burden of
maintaining them. Using cloud builders also provides additional benefits, such
as a shared build cache.

After signing up for Docker Build Cloud, add the builder to your local
environment and start building.

```console
$ docker buildx create --driver cloud ORG/BUILDER_NAME
cloud-ORG-BUILDER_NAME
$ docker build \
  --builder cloud-ORG-BUILDER_NAME \
  --platform linux/amd64,linux/arm64,linux/arm/v7 \
  --tag IMAGE_NAME \
  --push .
```

For more information, see
[Docker Build Cloud](https://docs.docker.com/build-cloud/).

### Cross-compilation

Depending on your project, if the programming language you use has good support
for cross-compilation, you can leverage multi-stage builds to build binaries
for target platforms from the native architecture of the builder. Special build
arguments, such as `BUILDPLATFORM` and `TARGETPLATFORM`, are automatically
available for use in your Dockerfile.

In the following example, the `FROM` instruction is pinned to the native
platform of the builder (using the `--platform=$BUILDPLATFORM` option) to
prevent emulation from kicking in. Then the pre-defined `$BUILDPLATFORM` and
`$TARGETPLATFORM` build arguments are interpolated in a `RUN` instruction. In
this case, the values are just printed to stdout with `echo`, but this
illustrates how you would pass them to the compiler for cross-compilation.

```dockerfile
# syntax=docker/dockerfile:1
FROM --platform=$BUILDPLATFORM golang:alpine AS build
ARG TARGETPLATFORM
ARG BUILDPLATFORM
RUN echo "I am running on $BUILDPLATFORM, building for $TARGETPLATFORM" > /log
FROM alpine
COPY --from=build /log /log
```

## Examples

Here are some examples of multi-platform builds:

- [Simple multi-platform build using emulation](#simple-multi-platform-build-using-emulation)
- [Multi-platform Neovim build using Docker Build Cloud](#multi-platform-neovim-build-using-docker-build-cloud)
- [Cross-compiling a Go application](#cross-compiling-a-go-application)

### Simple multi-platform build using emulation

This example demonstrates how to build a simple multi-platform image using
emulation with QEMU. The image contains a single file that prints the
architecture of the container.

Prerequisites:

- Docker Desktop, or Docker Engine with [QEMU installed](#install-qemu-manually)
- containerd image store enabled

Steps:

1. Create an empty directory and navigate to it:
  ```console
  $ mkdir multi-platform
  $ cd multi-platform
  ```
2. Create a simple Dockerfile that prints the architecture of the container:
  ```dockerfile
  # syntax=docker/dockerfile:1
  FROM alpine
  RUN uname -m > /arch
  ```
3. Build the image for `linux/amd64` and `linux/arm64`:
  ```console
  $ docker build --platform linux/amd64,linux/arm64 -t multi-platform .
  ```
4. Run the image and print the architecture:
  ```console
  $ docker run --rm multi-platform cat /arch
  ```
  - If you're running on an x86-64 machine, you should see `x86_64`.
  - If you're running on an ARM machine, you should see `aarch64`.

### Multi-platform Neovim build using Docker Build Cloud

This example demonstrates how run a multi-platform build using Docker Build
Cloud to compile and export [Neovim](https://github.com/neovim/neovim) binaries
for the `linux/amd64` and `linux/arm64` platforms.

Docker Build Cloud provides managed multi-node builders that support native
multi-platform builds without the need for emulation, making it much faster to
do CPU-intensive tasks like compilation.

Prerequisites:

- You've
  [signed up for Docker Build Cloud and created a builder](https://docs.docker.com/build-cloud/setup/)

Steps:

1. Create an empty directory and navigate to it:
  ```console
  $ mkdir docker-build-neovim
  $ cd docker-build-neovim
  ```
2. Create a Dockerfile that builds Neovim.
  ```dockerfile
  # syntax=docker/dockerfile:1
  FROM debian:bookworm AS build
  WORKDIR /work
  RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
      --mount=type=cache,target=/var/lib/apt,sharing=locked \
      apt-get update && apt-get install -y \
      build-essential \
      cmake \
      curl \
      gettext \
      ninja-build \
      unzip
  ADD https://github.com/neovim/neovim.git#stable .
  RUN make CMAKE_BUILD_TYPE=RelWithDebInfo
  FROM scratch
  COPY --from=build /work/build/bin/nvim /
  ```
3. Build the image for `linux/amd64` and `linux/arm64` using Docker Build Cloud:
  ```console
  $ docker build \
     --builder <cloud-builder> \
     --platform linux/amd64,linux/arm64 \
     --output ./bin .
  ```
  This command builds the image using the cloud builder and exports the
  binaries to the `bin` directory.
4. Verify that the binaries are built for both platforms. You should see the
  `nvim` binary for both `linux/amd64` and `linux/arm64`.
  ```console
  $ tree ./bin
  ./bin
  ├── linux_amd64
  │   └── nvim
  └── linux_arm64
      └── nvim
  3 directories, 2 files
  ```

### Cross-compiling a Go application

This example demonstrates how to cross-compile a Go application for multiple
platforms using multi-stage builds. The application is a simple HTTP server
that listens on port 8080 and returns the architecture of the container.
This example uses Go, but the same principles apply to other programming
languages that support cross-compilation.

Cross-compilation with Docker builds works by leveraging a series of
pre-defined (in BuildKit) build arguments that give you information about
platforms of the builder and the build targets. You can use these pre-defined
arguments to pass the platform information to the compiler.

In Go, you can use the `GOOS` and `GOARCH` environment variables to specify the
target platform to build for.

Prerequisites:

- Docker Desktop or Docker Engine

Steps:

1. Create an empty directory and navigate to it:
  ```console
  $ mkdir go-server
  $ cd go-server
  ```
2. Create a base Dockerfile that builds the Go application:
  ```dockerfile
  # syntax=docker/dockerfile:1
  FROM golang:alpine AS build
  WORKDIR /app
  ADD https://github.com/dvdksn/buildme.git#eb6279e0ad8a10003718656c6867539bd9426ad8 .
  RUN go build -o server .
  FROM alpine
  COPY --from=build /app/server /server
  ENTRYPOINT ["/server"]
  ```
  This Dockerfile can't build multi-platform with cross-compilation yet. If
  you were to try to build this Dockerfile with `docker build`, the builder
  would attempt to use emulation to build the image for the specified
  platforms.
3. To add cross-compilation support, update the Dockerfile to use the
  pre-defined `BUILDPLATFORM`, `TARGETOS` and `TARGETARCH` build arguments.
  - Pin the `golang` image to the platform of the builder using the
    `--platform=$BUILDPLATFORM` option.
  - Add `ARG` instructions for the Go compilation stages to make the
    `TARGETOS` and `TARGETARCH` build arguments available to the commands in
    this stage.
  - Set the `GOOS` and `GOARCH` environment variables to the values of
    `TARGETOS` and `TARGETARCH`. The Go compiler uses these variables to do
    cross-compilation.
  ```dockerfile
  # syntax=docker/dockerfile:1
  FROM --platform=$BUILDPLATFORM golang:alpine AS build
  ARG TARGETOS
  ARG TARGETARCH
  WORKDIR /app
  ADD https://github.com/dvdksn/buildme.git#eb6279e0ad8a10003718656c6867539bd9426ad8 .
  RUN GOOS=${TARGETOS} GOARCH=${TARGETARCH} go build -o server .
  FROM alpine
  COPY --from=build /app/server /server
  ENTRYPOINT ["/server"]
  ```
  ```dockerfile
  # syntax=docker/dockerfile:1
  FROM golang:alpine AS build
  WORKDIR /app
  ADD https://github.com/dvdksn/buildme.git#eb6279e0ad8a10003718656c6867539bd9426ad8 .
  RUN go build -o server .
  FROM alpine
  COPY --from=build /app/server /server
  ENTRYPOINT ["/server"]
  ```
  ```diff
  # syntax=docker/dockerfile:1
  -FROM golang:alpine AS build
  +FROM --platform=$BUILDPLATFORM golang:alpine AS build
  +ARG TARGETOS
  +ARG TARGETARCH
  WORKDIR /app
  ADD https://github.com/dvdksn/buildme.git#eb6279e0ad8a10003718656c6867539bd9426ad8 .
  -RUN go build -o server .
  +RUN GOOS=${TARGETOS} GOARCH=${TARGETARCH} go build -o server .
  FROM alpine
  COPY --from=build /app/server /server
  ENTRYPOINT ["/server"]
  ```
4. Build the image for `linux/amd64` and `linux/arm64`:
  ```console
  $ docker build --platform linux/amd64,linux/arm64 -t go-server .
  ```

This example has shown how to cross-compile a Go application for multiple
platforms with Docker builds. The specific steps on how to do cross-compilation
may vary depending on the programming language you're using. Consult the
documentation for your programming language to learn more about cross-compiling
for different platforms.

> Tip
>
> You may also want to consider checking out
> [xx - Dockerfile cross-compilation helpers](https://github.com/tonistiigi/xx).
> `xx` is a Docker image containing utility scripts that make cross-compiling with Docker builds easier.

---

# Multi

> Learn about multi-stage builds and how you can use them to improve your builds and get smaller images

# Multi-stage builds

   Table of contents

---

Multi-stage builds are useful to anyone who has struggled to optimize
Dockerfiles while keeping them easy to read and maintain.

## Use multi-stage builds

With multi-stage builds, you use multiple `FROM` statements in your Dockerfile.
Each `FROM` instruction can use a different base, and each of them begins a new
stage of the build. You can selectively copy artifacts from one stage to
another, leaving behind everything you don't want in the final image.

The following Dockerfile has two separate stages: one for building a binary,
and another where the binary gets copied from the first stage into the next stage.

```dockerfile
# syntax=docker/dockerfile:1
FROM golang:1.25
WORKDIR /src
COPY <<EOF ./main.go
package main

import "fmt"

func main() {
  fmt.Println("hello, world")
}
EOF
RUN go build -o /bin/hello ./main.go

FROM scratch
COPY --from=0 /bin/hello /bin/hello
CMD ["/bin/hello"]
```

You only need the single Dockerfile. No need for a separate build script. Just
run `docker build`.

```console
$ docker build -t hello .
```

The end result is a tiny production image with nothing but the binary inside.
None of the build tools required to build the application are included in the
resulting image.

How does it work? The second `FROM` instruction starts a new build stage with
the `scratch` image as its base. The `COPY --from=0` line copies just the
built artifact from the previous stage into this new stage. The Go SDK and any
intermediate artifacts are left behind, and not saved in the final image.

## Name your build stages

By default, the stages aren't named, and you refer to them by their integer
number, starting with 0 for the first `FROM` instruction. However, you can
name your stages, by adding an `AS <NAME>` to the `FROM` instruction. This
example improves the previous one by naming the stages and using the name in
the `COPY` instruction. This means that even if the instructions in your
Dockerfile are re-ordered later, the `COPY` doesn't break.

```dockerfile
# syntax=docker/dockerfile:1
FROM golang:1.25 AS build
WORKDIR /src
COPY <<EOF /src/main.go
package main

import "fmt"

func main() {
  fmt.Println("hello, world")
}
EOF
RUN go build -o /bin/hello ./main.go

FROM scratch
COPY --from=build /bin/hello /bin/hello
CMD ["/bin/hello"]
```

## Stop at a specific build stage

When you build your image, you don't necessarily need to build the entire
Dockerfile including every stage. You can specify a target build stage. The
following command assumes you are using the previous `Dockerfile` but stops at
the stage named `build`:

```console
$ docker build --target build -t hello .
```

A few scenarios where this might be useful are:

- Debugging a specific build stage
- Using a `debug` stage with all debugging symbols or tools enabled, and a
  lean `production` stage
- Using a `testing` stage in which your app gets populated with test data, but
  building for production using a different stage which uses real data

## Use an external image as a stage

When using multi-stage builds, you aren't limited to copying from stages you
created earlier in your Dockerfile. You can use the `COPY --from` instruction to
copy from a separate image, either using the local image name, a tag available
locally or on a Docker registry, or a tag ID. The Docker client pulls the image
if necessary and copies the artifact from there. The syntax is:

```dockerfile
COPY --from=nginx:latest /etc/nginx/nginx.conf /nginx.conf
```

## Use a previous stage as a new stage

You can pick up where a previous stage left off by referring to it when using
the `FROM` directive. For example:

```dockerfile
# syntax=docker/dockerfile:1

FROM alpine:latest AS builder
RUN apk --no-cache add build-base

FROM builder AS build1
COPY source1.cpp source.cpp
RUN g++ -o /binary source.cpp

FROM builder AS build2
COPY source2.cpp source.cpp
RUN g++ -o /binary source.cpp
```

## Differences between legacy builder and BuildKit

The legacy Docker Engine builder processes all stages of a Dockerfile leading
up to the selected `--target`. It will build a stage even if the selected
target doesn't depend on that stage.

[BuildKit](https://docs.docker.com/build/buildkit/) only builds the stages that the target stage
depends on.

For example, given the following Dockerfile:

```dockerfile
# syntax=docker/dockerfile:1
FROM ubuntu AS base
RUN echo "base"

FROM base AS stage1
RUN echo "stage1"

FROM base AS stage2
RUN echo "stage2"
```

With [BuildKit enabled](https://docs.docker.com/build/buildkit/#getting-started), building the
`stage2` target in this Dockerfile means only `base` and `stage2` are processed.
There is no dependency on `stage1`, so it's skipped.

```console
$ DOCKER_BUILDKIT=1 docker build --no-cache -f Dockerfile --target stage2 .
[+] Building 0.4s (7/7) FINISHED
 => [internal] load build definition from Dockerfile                                            0.0s
 => => transferring dockerfile: 36B                                                             0.0s
 => [internal] load .dockerignore                                                               0.0s
 => => transferring context: 2B                                                                 0.0s
 => [internal] load metadata for docker.io/library/ubuntu:latest                                0.0s
 => CACHED [base 1/2] FROM docker.io/library/ubuntu                                             0.0s
 => [base 2/2] RUN echo "base"                                                                  0.1s
 => [stage2 1/1] RUN echo "stage2"                                                              0.2s
 => exporting to image                                                                          0.0s
 => => exporting layers                                                                         0.0s
 => => writing image sha256:f55003b607cef37614f607f0728e6fd4d113a4bf7ef12210da338c716f2cfd15    0.0s
```

On the other hand, building the same target without BuildKit results in all
stages being processed:

```console
$ DOCKER_BUILDKIT=0 docker build --no-cache -f Dockerfile --target stage2 .
Sending build context to Docker daemon  219.1kB
Step 1/6 : FROM ubuntu AS base
 ---> a7870fd478f4
Step 2/6 : RUN echo "base"
 ---> Running in e850d0e42eca
base
Removing intermediate container e850d0e42eca
 ---> d9f69f23cac8
Step 3/6 : FROM base AS stage1
 ---> d9f69f23cac8
Step 4/6 : RUN echo "stage1"
 ---> Running in 758ba6c1a9a3
stage1
Removing intermediate container 758ba6c1a9a3
 ---> 396baa55b8c3
Step 5/6 : FROM base AS stage2
 ---> d9f69f23cac8
Step 6/6 : RUN echo "stage2"
 ---> Running in bbc025b93175
stage2
Removing intermediate container bbc025b93175
 ---> 09fc3770a9c4
Successfully built 09fc3770a9c4
```

The legacy builder processes `stage1`, even if `stage2` doesn't depend on it.
