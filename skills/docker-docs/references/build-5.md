# Manage builders and more

# Manage builders

# Manage builders

   Table of contents

---

You can create, inspect, and manage builders using `docker buildx` commands,
or [using Docker Desktop](#manage-builders-with-docker-desktop).

## Create a new builder

The default builder uses the [dockerdriver](https://docs.docker.com/build/builders/drivers/docker/).
You can't manually create new `docker` builders, but you can create builders
that use other drivers, such as the
[docker-containerdriver](https://docs.docker.com/build/builders/drivers/docker-container/),
which runs the BuildKit daemon in a container.

Use the
[docker buildx create](https://docs.docker.com/reference/cli/docker/buildx/create/)
command to create a builder.

```console
$ docker buildx create --name=<builder-name>
```

Buildx uses the `docker-container` driver by default if you omit the `--driver`
flag. For more information about available drivers, see
[Build drivers](https://docs.docker.com/build/builders/drivers/).

## List available builders

Use `docker buildx ls` to see builder instances available on your system, and
the drivers they're using.

```console
$ docker buildx ls
NAME/NODE       DRIVER/ENDPOINT      STATUS   BUILDKIT PLATFORMS
default *       docker
  default       default              running  v0.11.6  linux/amd64, linux/amd64/v2, linux/amd64/v3, linux/386
my_builder      docker-container
  my_builder0   default              running  v0.11.6  linux/amd64, linux/amd64/v2, linux/amd64/v3, linux/386
```

The asterisk (`*`) next to the builder name indicates the
[selected builder](https://docs.docker.com/build/builders/#selected-builder).

## Inspect a builder

To inspect a builder with the CLI, use `docker buildx inspect <name>`.
You can only inspect a builder if the builder is active.
You can add the `--bootstrap` flag to the command to start the builder.

```console
$ docker buildx inspect --bootstrap my_builder
[+] Building 1.7s (1/1) FINISHED
 => [internal] booting buildkit                                                              1.7s
 => => pulling image moby/buildkit:buildx-stable-1                                           1.3s
 => => creating container buildx_buildkit_my_builder0                                        0.4s
Name:          my_builder
Driver:        docker-container
Last Activity: 2023-06-21 18:28:37 +0000 UTC

Nodes:
Name:      my_builder0
Endpoint:  unix:///var/run/docker.sock
Status:    running
Buildkit:  v0.11.6
Platforms: linux/arm64, linux/amd64, linux/amd64/v2, linux/riscv64, linux/ppc64le, linux/s390x, linux/386, linux/mips64le, linux/mips64, linux/arm/v7, linux/arm/v6
```

If you want to see how much disk space a builder is using, use the
`docker buildx du` command. By default, this command shows the total disk usage
for all available builders. To see usage for a specific builder, use the
`--builder` flag.

```console
$ docker buildx du --builder my_builder
ID                                        RECLAIMABLE SIZE        LAST ACCESSED
olkri5gq6zsh8q2819i69aq6l                 true        797.2MB     37 seconds ago
6km4kasxgsywxkm6cxybdumbb*                true        438.5MB     36 seconds ago
qh3wwwda7gx2s5u4hsk0kp4w7                 true        213.8MB     37 seconds ago
54qq1egqem8max3lxq6180cj8                 true        200.2MB     37 seconds ago
ndlp969ku0950bmrw9muolw0c*                true        116.7MB     37 seconds ago
u52rcsnfd1brwc0chwsesb3io*                true        116.7MB     37 seconds ago
rzoeay0s4nmss8ub59z6lwj7d                 true        46.25MB     4 minutes ago
itk1iibhmv7awmidiwbef633q                 true        33.33MB     37 seconds ago
4p78yqnbmgt6xhcxqitdieeln                 true        19.46MB     4 minutes ago
dgkjvv4ay0szmr9bl7ynla7fy*                true        19.24MB     36 seconds ago
tuep198kmcw299qc9e4d1a8q2                 true        8.663MB     4 minutes ago
n1wzhauk9rpmt6ib1es7dktvj                 true        20.7kB      4 minutes ago
0a2xfhinvndki99y69157udlm                 true        16.56kB     37 seconds ago
gf0z1ypz54npfererqfeyhinn                 true        16.38kB     37 seconds ago
nz505f12cnsu739dw2pw0q78c                 true        8.192kB     37 seconds ago
hwpcyq5hdfvioltmkxu7fzwhb*                true        8.192kB     37 seconds ago
acekq89snc7j6im1rjdizvsg1*                true        8.192kB     37 seconds ago
Reclaimable:  2.01GB
Total:        2.01GB
```

## Remove a builder

Use the
[docker buildx remove](https://docs.docker.com/reference/cli/docker/buildx/create/)
command to remove a builder.

```console
$ docker buildx rm <builder-name>
```

If you remove your currently selected builder,
the default `docker` builder is automatically selected.
You can't remove the default builder.

Local build cache for the builder is also removed.

### Removing remote builders

Removing a remote builder doesn't affect the remote build cache.
It also doesn't stop the remote BuildKit daemon.
It only removes your connection to the builder.

## Manage builders with Docker Desktop

If you have turned on the
[Docker Desktop Builds view](https://docs.docker.com/desktop/use-desktop/builds/),
you can inspect builders in
[Docker Desktop settings](https://docs.docker.com/desktop/settings-and-maintenance/settings/#builders).

---

# Builders

> Learn about builders and how to manage them

# Builders

   Table of contents

---

A builder is a BuildKit daemon that you can use to run your builds. BuildKit
is the build engine that solves the build steps in a Dockerfile to produce a
container image or other artifacts.

You can create and manage builders, inspect them, and even connect to builders
running remotely. You interact with builders using the Docker CLI.

## Default builder

Docker Engine automatically creates a builder that becomes the default backend
for your builds. This builder uses the BuildKit library bundled with the
daemon. This builder requires no configuration.

The default builder is directly bound to the Docker daemon and its
[context](https://docs.docker.com/engine/manage-resources/contexts/). If you change the
Docker context, your `default` builder refers to the new Docker context.

## Build drivers

Buildx implements a concept of [build drivers](https://docs.docker.com/build/builders/drivers/) to refer to
different builder configurations. The default builder created by the daemon
uses the [dockerdriver](https://docs.docker.com/build/builders/drivers/docker/).

Buildx supports the following build drivers:

- `docker`: uses the BuildKit library bundled into the Docker daemon.
- `docker-container`: creates a dedicated BuildKit container using Docker.
- `kubernetes`: creates BuildKit pods in a Kubernetes cluster.
- `remote`: connects directly to a manually managed BuildKit daemon.

## Selected builder

Selected builder refers to the builder that's used by default when you run
build commands.

When you run a build, or interact with builders in some way using the CLI,
you can use the optional `--builder` flag, or the `BUILDX_BUILDER` [environment variable](https://docs.docker.com/build/building/variables/#buildx_builder),
to specify a builder by name. If you don't specify a builder,
the selected builder is used.

Use the `docker buildx ls` command to see the available builder instances.
The asterisk (`*`) next to a builder name indicates the selected builder.

```console
$ docker buildx ls
NAME/NODE       DRIVER/ENDPOINT      STATUS   BUILDKIT PLATFORMS
default *       docker
  default       default              running  v0.11.6  linux/amd64, linux/amd64/v2, linux/amd64/v3, linux/386
my_builder      docker-container
  my_builder0   default              running  v0.11.6  linux/amd64, linux/amd64/v2, linux/amd64/v3, linux/386
```

### Select a different builder

To switch between builders, use the `docker buildx use <name>` command.

After running this command, the builder you specify is automatically
selected when you invoke builds.

### Difference betweendocker buildanddocker buildx build

Even though `docker build` is an alias for `docker buildx build`, there are
subtle differences between the two commands. With Buildx, the build client and
the daemon (BuildKit) are decoupled. This means you can use multiple
builders from a single client, even remote ones.

The `docker build` command always defaults to using the default builder that
comes bundled with the Docker Engine, to ensure backwards compatibility with
older versions of the Docker CLI. The `docker buildx build` command, on the
other hand, checks whether you've set a different builder as the default
builder before it sends your build to BuildKit.

To use the `docker build` command with a non-default builder, you must either
specify the builder explicitly:

- Using the `--builder` flag:
  ```console
  $ docker build --builder my_builder .
  ```
- Or the `BUILDX_BUILDER` environment variable:
  ```console
  $ BUILDX_BUILDER=my_builder docker build .
  ```

In general, we recommend that you use the `docker buildx build` command when
you want to use custom builders. This ensures that your [selected
builder](#selected-builder) configuration is interpreted correctly.

## Additional information

- For information about how to interact with and manage builders,
  see [Manage builders](https://docs.docker.com/build/builders/manage/)
- To learn about different types of builders,
  see [Build drivers](https://docs.docker.com/build/builders/drivers/)

---

# Base images

> Learn about base images and how they're created

# Base images

   Table of contents

---

All Dockerfiles start from a base image.
A base is the image that your image extends.
It refers to the contents of the `FROM` instruction in the Dockerfile.

```dockerfile
FROM debian
```

For most cases, you don't need to create your own base image. Docker Hub
contains a vast library of Docker images that are suitable for use as a base
image in your build. [Docker Official
Images](https://docs.docker.com/docker-hub/image-library/trusted-content/#docker-official-images)
have clear documentation, promote best practices, and are regularly updated.
There are also [Docker Verified
Publisher](https://docs.docker.com/docker-hub/image-library/trusted-content/#verified-publisher-images)
images, created by trusted publishing partners, verified by Docker.

## Create a base image

If you need to completely control the contents of your image, you can create
your own base image from a Linux distribution of your choosing, or use the
special `FROM scratch` base:

```dockerfile
FROM scratch
```

The `scratch` image is typically used to create minimal images containing only
just what an application needs. See [Create a minimal base image using scratch](#create-a-minimal-base-image-using-scratch).

To create a distribution base image, you can use a root filesystem, packaged as
a `tar` file, and import it to Docker with `docker import`. The process for
creating your own base image depends on the Linux distribution you want to
package. See [Create a full image using tar](#create-a-full-image-using-tar).

## Create a minimal base image using scratch

The reserved, minimal `scratch` image serves as a starting point for
building containers. Using the `scratch` image signals to the build process
that you want the next command in the `Dockerfile` to be the first filesystem
layer in your image.

While `scratch` appears in Docker's [repository on Docker Hub](https://hub.docker.com/_/scratch),
you can't pull it, run it, or tag any image with the name `scratch`.
Instead, you can refer to it in your `Dockerfile`.
For example, to create a minimal container using `scratch`:

```dockerfile
# syntax=docker/dockerfile:1
FROM scratch
ADD hello /
CMD ["/hello"]
```

Assuming an executable binary named `hello` exists at the root of the
[build context](https://docs.docker.com/build/concepts/context/).
You can build this Docker image using the following `docker build` command:

```console
$ docker build --tag hello .
```

To run your new image, use the `docker run` command:

```console
$ docker run --rm hello
```

This example image can only be successfully executed as long as the `hello` binary
doesn't have any runtime dependencies. Computer programs tend to depend on
certain other programs or resources to exist in the runtime environment. For
example:

- Programming language runtimes
- Dynamically linked C libraries
- CA certificates

When building a base image, or any image, this is an important aspect to
consider. And this is why creating a base image using `FROM scratch` can be
difficult, for anything other than small, simple programs. On the other hand,
it's also important to include only the things you need in your image, to
reduce the image size and attack surface.

## Create a full image using tar

In general, start with a working machine that is running
the distribution you'd like to package as a base image, though that is
not required for some tools like Debian's [Debootstrap](https://wiki.debian.org/Debootstrap),
which you can also use to build Ubuntu images.

For example, to create an Ubuntu base image:

```dockerfile
$ sudo debootstrap noble noble > /dev/null
$ sudo tar -C noble -c . | docker import - noble

sha256:81ec9a55a92a5618161f68ae691d092bf14d700129093158297b3d01593f4ee3

$ docker run noble cat /etc/lsb-release

DISTRIB_ID=Ubuntu
DISTRIB_RELEASE=24.04
DISTRIB_CODENAME=noble
DISTRIB_DESCRIPTION="Ubuntu 24.04.2 LTS"
```

There are more example scripts for creating base images in
[the Moby GitHub repository](https://github.com/moby/moby/blob/master/contrib).

## More resources

For more information about building images and writing Dockerfiles, see:

- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
- [Dockerfile best practices](https://docs.docker.com/build/building/best-practices/)
- [Docker Official Images](https://docs.docker.com/docker-hub/image-library/trusted-content/#docker-official-images)
