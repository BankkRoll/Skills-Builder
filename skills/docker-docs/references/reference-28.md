# docker image pull and more

# docker image pull

# docker image pull

| Description | Download an image from a registry |
| --- | --- |
| Usage | docker image pull [OPTIONS] NAME[:TAG|@DIGEST] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker pull |

## Description

Most of your images will be created on top of a base image from the
[Docker Hub](https://hub.docker.com) registry.

[Docker Hub](https://hub.docker.com) contains many pre-built images that you
can `pull` and try without needing to define and configure your own.

To download a particular image, or set of images (i.e., a repository),
use `docker pull`.

### Proxy configuration

If you are behind an HTTP proxy server, for example in corporate settings,
before open a connect to registry, you may need to configure the Docker
daemon's proxy settings, refer to the
[dockerd command-line reference](https://docs.docker.com/reference/cli/dockerd/#proxy-configuration)
for details.

### Concurrent downloads

By default the Docker daemon will pull three layers of an image at a time.
If you are on a low bandwidth connection this may cause timeout issues and you may want to lower
this via the `--max-concurrent-downloads` daemon option. See the
[daemon documentation](https://docs.docker.com/reference/cli/dockerd/) for more details.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -a, --all-tags |  | Download all tagged images in the repository |
| --platform |  | API 1.32+Set platform if server is multi-platform capable |
| -q, --quiet |  | Suppress verbose output |

## Examples

### Pull an image from Docker Hub

To download a particular image, or set of images (i.e., a repository), use
`docker image pull` (or the `docker pull` shorthand). If no tag is provided,
Docker Engine uses the `:latest` tag as a default. This example pulls the
`debian:latest` image:

```console
$ docker image pull debian

Using default tag: latest
latest: Pulling from library/debian
e756f3fdd6a3: Pull complete
Digest: sha256:3f1d6c17773a45c97bd8f158d665c9709d7b29ed7917ac934086ad96f92e4510
Status: Downloaded newer image for debian:latest
docker.io/library/debian:latest
```

Docker images can consist of multiple layers. In the example above, the image
consists of a single layer; `e756f3fdd6a3`.

Layers can be reused by images. For example, the `debian:bookworm` image shares
its layer with the `debian:latest`. Pulling the `debian:bookworm` image therefore
only pulls its metadata, but not its layers, because the layer is already present
locally:

```console
$ docker image pull debian:bookworm

bookworm: Pulling from library/debian
Digest: sha256:3f1d6c17773a45c97bd8f158d665c9709d7b29ed7917ac934086ad96f92e4510
Status: Downloaded newer image for debian:bookworm
docker.io/library/debian:bookworm
```

To see which images are present locally, use the
[docker images](https://docs.docker.com/reference/cli/docker/image/ls/)
command:

```console
$ docker images

REPOSITORY   TAG        IMAGE ID       CREATED        SIZE
debian       bookworm   4eacea30377a   8 days ago     124MB
debian       latest     4eacea30377a   8 days ago     124MB
```

Docker uses a content-addressable image store, and the image ID is a SHA256
digest covering the image's configuration and layers. In the example above,
`debian:bookworm` and `debian:latest` have the same image ID because they are
the same image tagged with different names. Because they are the same image,
their layers are stored only once and do not consume extra disk space.

For more information about images, layers, and the content-addressable store,
refer to
[understand images, containers, and storage drivers](https://docs.docker.com/engine/storage/drivers/).

### Pull an image by digest (immutable identifier)

So far, you've pulled images by their name (and "tag"). Using names and tags is
a convenient way to work with images. When using tags, you can `docker pull` an
image again to make sure you have the most up-to-date version of that image.
For example, `docker pull ubuntu:24.04` pulls the latest version of the Ubuntu
24.04 image.

In some cases you don't want images to be updated to newer versions, but prefer
to use a fixed version of an image. Docker enables you to pull an image by its
digest. When pulling an image by digest, you specify exactly which version
of an image to pull. Doing so, allows you to "pin" an image to that version,
and guarantee that the image you're using is always the same.

To know the digest of an image, pull the image first. Let's pull the latest
`ubuntu:24.04` image from Docker Hub:

```console
$ docker pull ubuntu:24.04

24.04: Pulling from library/ubuntu
125a6e411906: Pull complete
Digest: sha256:2e863c44b718727c860746568e1d54afd13b2fa71b160f5cd9058fc436217b30
Status: Downloaded newer image for ubuntu:24.04
docker.io/library/ubuntu:24.04
```

Docker prints the digest of the image after the pull has finished. In the example
above, the digest of the image is:

```console
sha256:2e863c44b718727c860746568e1d54afd13b2fa71b160f5cd9058fc436217b30
```

Docker also prints the digest of an image when pushing to a registry. This
may be useful if you want to pin to a version of the image you just pushed.

A digest takes the place of the tag when pulling an image, for example, to
pull the above image by digest, run the following command:

```console
$ docker pull ubuntu@sha256:2e863c44b718727c860746568e1d54afd13b2fa71b160f5cd9058fc436217b30

docker.io/library/ubuntu@sha256:2e863c44b718727c860746568e1d54afd13b2fa71b160f5cd9058fc436217b30: Pulling from library/ubuntu
Digest: sha256:2e863c44b718727c860746568e1d54afd13b2fa71b160f5cd9058fc436217b30
Status: Image is up to date for ubuntu@sha256:2e863c44b718727c860746568e1d54afd13b2fa71b160f5cd9058fc436217b30
docker.io/library/ubuntu@sha256:2e863c44b718727c860746568e1d54afd13b2fa71b160f5cd9058fc436217b30
```

Digest can also be used in the `FROM` of a Dockerfile, for example:

```dockerfile
FROM ubuntu@sha256:2e863c44b718727c860746568e1d54afd13b2fa71b160f5cd9058fc436217b30
LABEL org.opencontainers.image.authors="some maintainer <maintainer@example.com>"
```

> Note
>
> Using this feature "pins" an image to a specific version in time.
> Docker does therefore not pull updated versions of an image, which may include
> security updates. If you want to pull an updated image, you need to change the
> digest accordingly.

### Pull from a different registry

By default, `docker pull` pulls images from [Docker Hub](https://hub.docker.com). It is also possible to
manually specify the path of a registry to pull from. For example, if you have
set up a local registry, you can specify its path to pull from it. A registry
path is similar to a URL, but does not contain a protocol specifier (`https://`).

The following command pulls the `testing/test-image` image from a local registry
listening on port 5000 (`myregistry.local:5000`):

```console
$ docker image pull myregistry.local:5000/testing/test-image
```

Registry credentials are managed by
[docker login](https://docs.docker.com/reference/cli/docker/login/).

Docker uses the `https://` protocol to communicate with a registry, unless the
registry is allowed to be accessed over an insecure connection. Refer to the
[insecure registries](https://docs.docker.com/reference/cli/dockerd/#insecure-registries) section for more information.

### Pull a repository with multiple images (-a, --all-tags)

By default, `docker pull` pulls a single image from the registry. A repository
can contain multiple images. To pull all images from a repository, provide the
`-a` (or `--all-tags`) option when using `docker pull`.

This command pulls all images from the `ubuntu` repository:

```console
$ docker image pull --all-tags ubuntu

Pulling repository ubuntu
ad57ef8d78d7: Download complete
105182bb5e8b: Download complete
511136ea3c5a: Download complete
73bd853d2ea5: Download complete
....

Status: Downloaded newer image for ubuntu
```

After the pull has completed use the `docker image ls` command (or the `docker images`
shorthand) to see the images that were pulled. The example below shows all the
`ubuntu` images that are present locally:

```console
$ docker image ls --filter reference=ubuntu
REPOSITORY   TAG       IMAGE ID       CREATED        SIZE
ubuntu       22.04     8a3cdc4d1ad3   3 weeks ago    77.9MB
ubuntu       jammy     8a3cdc4d1ad3   3 weeks ago    77.9MB
ubuntu       24.04     35a88802559d   6 weeks ago    78.1MB
ubuntu       latest    35a88802559d   6 weeks ago    78.1MB
ubuntu       noble     35a88802559d   6 weeks ago    78.1MB
```

### Cancel a pull

Killing the `docker pull` process, for example by pressing `CTRL-c` while it is
running in a terminal, will terminate the pull operation.

```console
$ docker pull ubuntu

Using default tag: latest
latest: Pulling from library/ubuntu
a3ed95caeb02: Pulling fs layer
236608c7b546: Pulling fs layer
^C
```

The Engine terminates a pull operation when the connection between the daemon
and the client (initiating the pull) is cut or lost for any reason or the
command is manually terminated.

---

# docker image push

# docker image push

| Description | Upload an image to a registry |
| --- | --- |
| Usage | docker image push [OPTIONS] NAME[:TAG] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker push |

## Description

Use `docker image push` to share your images to the [Docker Hub](https://hub.docker.com)
registry or to a self-hosted one.

Refer to the
[docker image tag](https://docs.docker.com/reference/cli/docker/image/tag/) reference for more information
about valid image and tag names.

Killing the `docker image push` process, for example by pressing `CTRL-c` while it is
running in a terminal, terminates the push operation.

Progress bars are shown during docker push, which show the uncompressed size.
The actual amount of data that's pushed will be compressed before sending, so
the uploaded size will not be reflected by the progress bar.

Registry credentials are managed by
[docker login](https://docs.docker.com/reference/cli/docker/login/).

### Concurrent uploads

By default the Docker daemon will push five layers of an image at a time.
If you are on a low bandwidth connection this may cause timeout issues and you may want to lower
this via the `--max-concurrent-uploads` daemon option. See the
[daemon documentation](https://docs.docker.com/reference/cli/dockerd/) for more details.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -a, --all-tags |  | Push all tags of an image to the repository |
| --platform |  | API 1.46+Push a platform-specific manifest as a single-platform image to the registry.Image index won't be pushed, meaning that other manifests, including attestations won't be preserved.'os[/arch[/variant]]': Explicit platform (eg. linux/amd64) |
| -q, --quiet |  | Suppress verbose output |

## Examples

### Push a new image to a registry

First save the new image by finding the container ID (using
[docker container ls](https://docs.docker.com/reference/cli/docker/container/ls/)) and then committing it to a new image name. Note that
only `a-z0-9-_.` are allowed when naming images:

```console
$ docker container commit c16378f943fe rhel-httpd:latest
```

Now, push the image to the registry using the image ID. In this example the
registry is on host named `registry-host` and listening on port `5000`. To do
this, tag the image with the host name or IP address, and the port of the
registry:

```console
$ docker image tag rhel-httpd:latest registry-host:5000/myadmin/rhel-httpd:latest

$ docker image push registry-host:5000/myadmin/rhel-httpd:latest
```

Check that this worked by running:

```console
$ docker image ls
```

You should see both `rhel-httpd` and `registry-host:5000/myadmin/rhel-httpd`
listed.

### Push all tags of an image (-a, --all-tags)

Use the `-a` (or `--all-tags`) option to push all tags of a local image.

The following example creates multiple tags for an image, and pushes all those
tags to Docker Hub.

```console
$ docker image tag myimage registry-host:5000/myname/myimage:latest
$ docker image tag myimage registry-host:5000/myname/myimage:v1.0.1
$ docker image tag myimage registry-host:5000/myname/myimage:v1.0
$ docker image tag myimage registry-host:5000/myname/myimage:v1
```

The image is now tagged under multiple names:

```console
$ docker image ls

REPOSITORY                          TAG        IMAGE ID       CREATED      SIZE
myimage                             latest     6d5fcfe5ff17   2 hours ago  1.22MB
registry-host:5000/myname/myimage   latest     6d5fcfe5ff17   2 hours ago  1.22MB
registry-host:5000/myname/myimage   v1         6d5fcfe5ff17   2 hours ago  1.22MB
registry-host:5000/myname/myimage   v1.0       6d5fcfe5ff17   2 hours ago  1.22MB
registry-host:5000/myname/myimage   v1.0.1     6d5fcfe5ff17   2 hours ago  1.22MB
```

When pushing with the `--all-tags` option, all tags of the `registry-host:5000/myname/myimage`
image are pushed:

```console
$ docker image push --all-tags registry-host:5000/myname/myimage

The push refers to repository [registry-host:5000/myname/myimage]
195be5f8be1d: Pushed
latest: digest: sha256:edafc0a0fb057813850d1ba44014914ca02d671ae247107ca70c94db686e7de6 size: 4527
195be5f8be1d: Layer already exists
v1: digest: sha256:edafc0a0fb057813850d1ba44014914ca02d671ae247107ca70c94db686e7de6 size: 4527
195be5f8be1d: Layer already exists
v1.0: digest: sha256:edafc0a0fb057813850d1ba44014914ca02d671ae247107ca70c94db686e7de6 size: 4527
195be5f8be1d: Layer already exists
v1.0.1: digest: sha256:edafc0a0fb057813850d1ba44014914ca02d671ae247107ca70c94db686e7de6 size: 4527
```

---

# docker image rm

# docker image rm

| Description | Remove one or more images |
| --- | --- |
| Usage | docker image rm [OPTIONS] IMAGE [IMAGE...] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker image removedocker rmi |

## Description

Removes (and un-tags) one or more images from the host node. If an image has
multiple tags, using this command with the tag as a parameter only removes the
tag. If the tag is the only one for the image, both the image and the tag are
removed.

This does not remove images from a registry. You cannot remove an image of a
running container unless you use the `-f` option. To see all images on a host
use the
[docker image ls](https://docs.docker.com/reference/cli/docker/image/ls/) command.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -f, --force |  | Force removal of the image |
| --no-prune |  | Do not delete untagged parents |
| --platform |  | API 1.50+Remove only the given platform variant. Formatted asos[/arch[/variant]](e.g.,linux/amd64) |

## Examples

You can remove an image using its short or long ID, its tag, or its digest. If
an image has one or more tags referencing it, you must remove all of them before
the image is removed. Digest references are removed automatically when an image
is removed by tag.

```console
$ docker images

REPOSITORY                TAG                 IMAGE ID            CREATED             SIZE
test1                     latest              fd484f19954f        23 seconds ago      7 B (virtual 4.964 MB)
test                      latest              fd484f19954f        23 seconds ago      7 B (virtual 4.964 MB)
test2                     latest              fd484f19954f        23 seconds ago      7 B (virtual 4.964 MB)

$ docker rmi fd484f19954f

Error: Conflict, cannot delete image fd484f19954f because it is tagged in multiple repositories, use -f to force
2013/12/11 05:47:16 Error: failed to remove one or more images

$ docker rmi test1:latest

Untagged: test1:latest

$ docker rmi test2:latest

Untagged: test2:latest

$ docker images

REPOSITORY                TAG                 IMAGE ID            CREATED             SIZE
test                      latest              fd484f19954f        23 seconds ago      7 B (virtual 4.964 MB)

$ docker rmi test:latest

Untagged: test:latest
Deleted: fd484f19954f4920da7ff372b5067f5b7ddb2fd3830cecd17b96ea9e286ba5b8
```

If you use the `-f` flag and specify the image's short or long ID, then this
command untags and removes all images that match the specified ID.

```console
$ docker images

REPOSITORY                TAG                 IMAGE ID            CREATED             SIZE
test1                     latest              fd484f19954f        23 seconds ago      7 B (virtual 4.964 MB)
test                      latest              fd484f19954f        23 seconds ago      7 B (virtual 4.964 MB)
test2                     latest              fd484f19954f        23 seconds ago      7 B (virtual 4.964 MB)

$ docker rmi -f fd484f19954f

Untagged: test1:latest
Untagged: test:latest
Untagged: test2:latest
Deleted: fd484f19954f4920da7ff372b5067f5b7ddb2fd3830cecd17b96ea9e286ba5b8
```

An image pulled by digest has no tag associated with it:

```console
$ docker images --digests

REPOSITORY                     TAG       DIGEST                                                                    IMAGE ID        CREATED         SIZE
localhost:5000/test/busybox    <none>    sha256:cbbf2f9a99b47fc460d422812b6a5adff7dfee951d8fa2e4a98caa0382cfbdbf   4986bf8c1536    9 weeks ago     2.43 MB
```

To remove an image using its digest:

```console
$ docker rmi localhost:5000/test/busybox@sha256:cbbf2f9a99b47fc460d422812b6a5adff7dfee951d8fa2e4a98caa0382cfbdbf
Untagged: localhost:5000/test/busybox@sha256:cbbf2f9a99b47fc460d422812b6a5adff7dfee951d8fa2e4a98caa0382cfbdbf
Deleted: 4986bf8c15363d1c5d15512d5266f8777bfba4974ac56e3270e7760f6f0a8125
Deleted: ea13149945cb6b1e746bf28032f02e9b5a793523481a0a18645fc77ad53c4ea2
Deleted: df7546f9f060a2268024c8a230d8639878585defcc1bc6f79d2728a13957871b
```

### Remove specific platforms (--platform)

The `--platform` option allows you to specify which platform variants of the
image to remove. By default, `docker image remove` removes all platform variants
that are present. Use the `--platform` option to specify which platform variant
of the image to remove.

Removing a specific platform removes the image from all images that reference
the same content, and requires the `--force` option to be used. Omitting the
`--force` option produces a warning, and the remove is canceled:

```console
$ docker image rm --platform=linux/amd64 alpine
Error response from daemon: Content will be removed from all images referencing this variant. Use —-force to force delete.
```

The platform option takes the `os[/arch[/variant]]` format; for example,
`linux/amd64` or `linux/arm64/v8`. Architecture and variant are optional,
and default to the daemon's native architecture if omitted.

You can pass multiple platforms either by passing the `--platform` flag
multiple times, or by passing a comma-separated list of platforms to remove.
The following uses of this option are equivalent;

```console
$ docker image rm --plaform linux/amd64 --platform linux/ppc64le myimage
$ docker image rm --plaform linux/amd64,linux/ppc64le myimage
```

The following example removes the `linux/amd64` and `linux/ppc64le` variants
of an `alpine` image that contains multiple platform variants in the image
cache:

```console
$ docker image ls --tree

IMAGE                   ID             DISK USAGE   CONTENT SIZE   EXTRA
alpine:latest           a8560b36e8b8       37.8MB         11.2MB    U
├─ linux/amd64          1c4eef651f65       12.1MB         3.64MB    U
├─ linux/arm/v6         903bfe2ae994           0B             0B
├─ linux/arm/v7         9c2d245b3c01           0B             0B
├─ linux/arm64/v8       757d680068d7       12.8MB         3.99MB
├─ linux/386            2436f2b3b7d2           0B             0B
├─ linux/ppc64le        9ed53fd3b831       12.8MB         3.58MB
├─ linux/riscv64        1de5eb4a9a67           0B             0B
└─ linux/s390x          fe0dcdd1f783           0B             0B

$ docker image --platform=linux/amd64,linux/ppc64le --force alpine
Deleted: sha256:1c4eef651f65e2f7daee7ee785882ac164b02b78fb74503052a26dc061c90474
Deleted: sha256:9ed53fd3b83120f78b33685d930ce9bf5aa481f6e2d165c42cbbddbeaa196f6f
```

After the command completes, the given variants of the `alpine` image are removed
from the image cache:

```console
$ docker image ls --tree

IMAGE                   ID             DISK USAGE   CONTENT SIZE   EXTRA
alpine:latest           a8560b36e8b8       12.8MB         3.99MB
├─ linux/amd64          1c4eef651f65           0B             0B
├─ linux/arm/v6         903bfe2ae994           0B             0B
├─ linux/arm/v7         9c2d245b3c01           0B             0B
├─ linux/arm64/v8       757d680068d7       12.8MB         3.99MB
├─ linux/386            2436f2b3b7d2           0B             0B
├─ linux/ppc64le        9ed53fd3b831           0B             0B
├─ linux/riscv64        1de5eb4a9a67           0B             0B
└─ linux/s390x          fe0dcdd1f783           0B             0B
```

---

# docker image save

# docker image save

| Description | Save one or more images to a tar archive (streamed to STDOUT by default) |
| --- | --- |
| Usage | docker image save [OPTIONS] IMAGE [IMAGE...] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker save |

## Description

Produces a tarred repository to the standard output stream.
Contains all parent layers, and all tags + versions, or specified `repo:tag`, for
each argument provided.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -o, --output |  | Write to a file, instead of STDOUT |
| --platform |  | API 1.48+Save only the given platform(s). Formatted as a comma-separated list ofos[/arch[/variant]](e.g.,linux/amd64,linux/arm64/v8) |

## Examples

### Create a backup that can then be used withdocker load.

```console
$ docker save busybox > busybox.tar

$ ls -sh busybox.tar

2.7M busybox.tar

$ docker save --output busybox.tar busybox

$ ls -sh busybox.tar

2.7M busybox.tar

$ docker save -o fedora-all.tar fedora

$ docker save -o fedora-latest.tar fedora:latest
```

### Save an image to a tar.gz file using gzip

You can use gzip to save the image file and make the backup smaller.

```console
$ docker save myimage:latest | gzip > myimage_latest.tar.gz
```

### Cherry-pick particular tags

You can even cherry-pick particular tags of an image repository.

```console
$ docker save -o ubuntu.tar ubuntu:lucid ubuntu:saucy
```

### Save a specific platform (--platform)

The `--platform` option allows you to specify which platform variant of the
image to save. By default, `docker save` saves all platform variants that
are present in the daemon's image store. Use the `--platform` option
to specify which platform variant of the image to save. An error is produced
if the given platform is not present in the local image store.

The platform option takes the `os[/arch[/variant]]` format; for example,
`linux/amd64` or `linux/arm64/v8`. Architecture and variant are optional,
and default to the daemon's native architecture if omitted.

The following example pulls the RISC-V variant of the `alpine:latest` image
and saves it to a tar archive.

```console
$ docker pull --platform=linux/riscv64 alpine:latest
latest: Pulling from library/alpine
8c4a05189a5f: Download complete
Digest: sha256:beefdbd8a1da6d2915566fde36db9db0b524eb737fc57cd1367effd16dc0d06d
Status: Downloaded newer image for alpine:latest
docker.io/library/alpine:latest

$ docker image save --platform=linux/riscv64 -o alpine-riscv.tar alpine:latest

$ ls -lh image.tar
-rw-------  1 thajeztah  staff   3.9M Oct  7 11:06 alpine-riscv.tar
```

The following example attempts to save a platform variant of `alpine:latest`
that doesn't exist in the local image store, resulting in an error.

```console
$ docker image ls --tree
IMAGE                   ID             DISK USAGE   CONTENT SIZE   IN USE
alpine:latest           beefdbd8a1da       10.6MB         3.37MB
├─ linux/riscv64        80cde017a105       10.6MB         3.37MB
├─ linux/amd64          33735bd63cf8           0B             0B
├─ linux/arm/v6         50f635c8b04d           0B             0B
├─ linux/arm/v7         f2f82d424957           0B             0B
├─ linux/arm64/v8       9cee2b382fe2           0B             0B
├─ linux/386            b3e87f642f5c           0B             0B
├─ linux/ppc64le        c7a6800e3dc5           0B             0B
└─ linux/s390x          2b5b26e09ca2           0B             0B

$ docker image save --platform=linux/s390x -o alpine-s390x.tar alpine:latest
Error response from daemon: no suitable export target found for platform linux/s390x
```

---

# docker image tag

# docker image tag

| Description | Create a tag TARGET_IMAGE that refers to SOURCE_IMAGE |
| --- | --- |
| Usage | docker image tag SOURCE_IMAGE[:TAG] TARGET_IMAGE[:TAG] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker tag |

## Description

A Docker image reference consists of several components that describe where the
image is stored and its identity. These components are:

```text
[HOST[:PORT]/]NAMESPACE/REPOSITORY[:TAG]
```

`HOST`Specifies the registry location where the image resides. If omitted, Docker
defaults to Docker Hub (`docker.io`).`PORT`An optional port number for the registry, if necessary (for example, `:5000`).`NAMESPACE/REPOSITORY`The namespace (optional) usually represents a user or organization. The
repository is required and identifies the specific image. If the namespace is
omitted, Docker defaults to `library`, the namespace reserved for Docker
Official Images.`TAG`An optional identifier used to specify a particular version or variant of the
image. If no tag is provided, Docker defaults to `latest`.

### Example image references

`example.com:5000/team/my-app:2.0`

- Host: `example.com`
- Port: `5000`
- Namespace: `team`
- Repository: `my-app`
- Tag: `2.0`

`alpine`

- Host: `docker.io` (default)
- Namespace: `library` (default)
- Repository: `alpine`
- Tag: `latest` (default)

For more information on the structure and rules of image naming, refer to the
[Distribution reference](https://pkg.go.dev/github.com/distribution/reference#pkg-overview)
as the canonical definition of the format.

## Examples

### Tag an image referenced by ID

To tag a local image with ID `0e5574283393` as `fedora/httpd` with the tag
`version1.0`:

```console
$ docker tag 0e5574283393 fedora/httpd:version1.0
```

### Tag an image referenced by Name

To tag a local image `httpd` as `fedora/httpd` with the tag `version1.0`:

```console
$ docker tag httpd fedora/httpd:version1.0
```

Note that since the tag name isn't specified, the alias is created for an
existing local version `httpd:latest`.

### Tag an image referenced by Name and Tag

To tag a local image with the name `httpd` and the tag `test` as `fedora/httpd`
with the tag `version1.0.test`:

```console
$ docker tag httpd:test fedora/httpd:version1.0.test
```

### Tag an image for a private registry

To push an image to a private registry and not the public Docker registry you
must include the registry hostname and port (if needed).

```console
$ docker tag 0e5574283393 myregistryhost:5000/fedora/httpd:version1.0
```

---

# docker image

# docker image

| Description | Manage images |
| --- | --- |
| Usage | docker image |

## Description

Manage images.

## Subcommands

| Command | Description |
| --- | --- |
| docker image history | Show the history of an image |
| docker image import | Import the contents from a tarball to create a filesystem image |
| docker image inspect | Display detailed information on one or more images |
| docker image load | Load an image from a tar archive or STDIN |
| docker image ls | List images |
| docker image prune | Remove unused images |
| docker image pull | Download an image from a registry |
| docker image push | Upload an image to a registry |
| docker image rm | Remove one or more images |
| docker image save | Save one or more images to a tar archive (streamed to STDOUT by default) |
| docker image tag | Create a tag TARGET_IMAGE that refers to SOURCE_IMAGE |

---

# docker init

# docker init

| Description | Creates Docker-related starter files for your project |
| --- | --- |
| Usage | docker init [OPTIONS] |

Requires: Docker Desktop
[4.27](https://docs.docker.com/desktop/release-notes/#4270) and later

## Description

Initialize a project with the files necessary to run the project in a container.

Docker Desktop provides the `docker init` CLI command. Run `docker init` in your project directory to be walked through the creation of the following files with sensible defaults for your project:

- .dockerignore
- Dockerfile
- compose.yaml
- README.Docker.md

If any of the files already exist, a prompt appears and provides a warning
as well as giving you the option to overwrite all the files. If
`docker-compose.yaml` already exists instead of `compose.yaml`, `docker init` can overwrite it, using `docker-compose.yaml` as the name for the
Compose file.

> Warning
>
> You can't recover overwritten files.
> To back up an existing file before selecting to overwrite it, rename the file or copy it to another directory.

After running `docker init`, you can choose one of the following templates:

- ASP.NET Core: Suitable for an ASP.NET Core application.
- Go: Suitable for a Go server application.
- Java: suitable for a Java application that uses Maven and packages as an uber jar.
- Node: Suitable for a Node server application.
- PHP with Apache: Suitable for a PHP web application.
- Python: Suitable for a Python server application.
- Rust: Suitable for a Rust server application.
- Other: General purpose starting point for containerizing your application.

After `docker init` has completed, you may need to modify the created files and tailor them to your project. Visit the following topics to learn more about the files:

- [.dockerignore](https://docs.docker.com/reference/dockerfile/#dockerignore-file)
- [Dockerfile](https://docs.docker.com/reference/dockerfile/)
- [compose.yaml](https://docs.docker.com/compose/intro/compose-application-model/)

## Options

| Option | Default | Description |
| --- | --- | --- |
| --version |  | Display version of the init plugin |

## Examples

### Example of runningdocker init

The following example shows the initial menu after running `docker init`. See the additional examples to view the options for each language or framework.

```console
$ docker init

Welcome to the Docker Init CLI!

This utility will walk you through creating the following files with sensible defaults for your project:
  - .dockerignore
  - Dockerfile
  - compose.yaml
  - README.Docker.md

Let's get started!

? What application platform does your project use?  [Use arrows to move, type to filter]
> PHP with Apache - (detected) suitable for a PHP web application
  Go - suitable for a Go server application
  Java - suitable for a Java application that uses Maven and packages as an uber jar
  Python - suitable for a Python server application
  Node - suitable for a Node server application
  Rust - suitable for a Rust server application
  ASP.NET Core - suitable for an ASP.NET Core application
  Other - general purpose starting point for containerizing your application
  Don't see something you need? Let us know!
  Quit
```

### Example of selecting Go

The following example shows the prompts that appear after selecting `Go` and example input.

```console
? What application platform does your project use? Go
? What version of Go do you want to use? 1.20
? What's the relative directory (with a leading .) of your main package? .
? What port does your server listen on? 3333

CREATED: .dockerignore
CREATED: Dockerfile
CREATED: compose.yaml
CREATED: README.Docker.md

✔ Your Docker files are ready!

Take a moment to review them and tailor them to your application.

When you're ready, start your application by running: docker compose up --build

Your application will be available at http://localhost:3333

Consult README.Docker.md for more information about using the generated files.
```

### Example of selecting Node

The following example shows the prompts that appear after selecting `Node` and example input.

```console
? What application platform does your project use? Node
? What version of Node do you want to use? 18
? Which package manager do you want to use? yarn
? Do you want to run "yarn run build" before starting your server? Yes
? What directory is your build output to? (comma-separate if multiple) output
? What command do you want to use to start the app? node index.js
? What port does your server listen on? 8000

CREATED: .dockerignore
CREATED: Dockerfile
CREATED: compose.yaml
CREATED: README.Docker.md

✔ Your Docker files are ready!

Take a moment to review them and tailor them to your application.

When you're ready, start your application by running: docker compose up --build

Your application will be available at http://localhost:8000

Consult README.Docker.md for more information about using the generated files.
```

### Example of selecting Python

The following example shows the prompts that appear after selecting `Python` and example input.

```console
? What application platform does your project use? Python
? What version of Python do you want to use? 3.8
? What port do you want your app to listen on? 8000
? What is the command to run your app (e.g., gunicorn 'myapp.example:app' --bind=0.0.0.0:8000)? python ./app.py

CREATED: .dockerignore
CREATED: Dockerfile
CREATED: compose.yaml
CREATED: README.Docker.md

✔ Your Docker files are ready!

Take a moment to review them and tailor them to your application.

When you're ready, start your application by running: docker compose up --build

Your application will be available at http://localhost:8000

Consult README.Docker.md for more information about using the generated files.
```

### Example of selecting Rust

The following example shows the prompts that appear after selecting `Rust` and example input.

```console
? What application platform does your project use? Rust
? What version of Rust do you want to use? 1.70.0
? What port does your server listen on? 8000

CREATED: .dockerignore
CREATED: Dockerfile
CREATED: compose.yaml
CREATED: README.Docker.md

✔ Your Docker files are ready!

Take a moment to review them and tailor them to your application.

When you're ready, start your application by running: docker compose up --build

Your application will be available at http://localhost:8000

Consult README.Docker.md for more information about using the generated files.
```

### Example of selecting ASP.NET Core

The following example shows the prompts that appear after selecting `ASP.NET Core` and example input.

```console
? What application platform does your project use? ASP.NET Core
? What's the name of your solution's main project? myapp
? What version of .NET do you want to use? 6.0
? What local port do you want to use to access your server? 8000

CREATED: .dockerignore
CREATED: Dockerfile
CREATED: compose.yaml
CREATED: README.Docker.md

✔ Your Docker files are ready!

Take a moment to review them and tailor them to your application.

When you're ready, start your application by running: docker compose up --build

Your application will be available at http://localhost:8000

Consult README.Docker.md for more information about using the generated files.
```

### Example of selecting PHP with Apache

The following example shows the prompts that appear after selecting `PHP with Apache` and example input. The PHP with Apache template is suitable for both pure PHP applications and applications using Composer as a dependency manager. After running `docker init`, you must manually add any PHP extensions that are required by your application to the Dockerfile.

```console
? What application platform does your project use? PHP with Apache
? What version of PHP do you want to use? 8.2
? What's the relative directory (with a leading .) for your app? ./src
? What local port do you want to use to access your server? 9000

CREATED: .dockerignore
CREATED: Dockerfile
CREATED: compose.yaml
CREATED: README.Docker.md

✔ Your Docker files are ready!

Take a moment to review them and tailor them to your application.

If your application requires specific PHP extensions, you can follow the instructions in the Dockerfile to add them.

When you're ready, start your application by running: docker compose up --build

Your application will be available at http://localhost:9000

Consult README.Docker.md for more information about using the generated files.
```

### Example of selecting Java

The following example shows the prompts that appear after selecting `Java` and example input.

```console
? What application platform does your project use? Java
? What version of Java do you want to use? 17
? What's the relative directory (with a leading .) for your app? ./src
? What port does your server listen on? 9000

CREATED: .dockerignore
CREATED: Dockerfile
CREATED: compose.yaml
CREATED: README.Docker.md

✔ Your Docker files are ready!

Take a moment to review them and tailor them to your application.

When you're ready, start your application by running: docker compose up --build

Your application will be available at http://localhost:9000

Consult README.Docker.md for more information about using the generated files.
```

### Example of selecting Other

The following example shows the output after selecting `Other`.

```console
? What application platform does your project use? Other

CREATED: .dockerignore
CREATED: Dockerfile
CREATED: compose.yaml
CREATED: README.Docker.md

✔ Your Docker files are ready!

Take a moment to review them and tailor them to your application.

When you're ready, start your application by running: docker compose up --build

Consult README.Docker.md for more information about using the generated files.
```

---

# docker inspect

# docker inspect

| Description | Return low-level information on Docker objects |
| --- | --- |
| Usage | docker inspect [OPTIONS] NAME|ID [NAME|ID...] |

## Description

Docker inspect provides detailed information on constructs controlled by Docker.

By default, `docker inspect` will render results in a JSON array.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -f, --format |  | Format output using a custom template:'json': Print in JSON format'TEMPLATE': Print output using the given Go template.Refer tohttps://docs.docker.com/go/formatting/for more information about formatting output with templates |
| -s, --size |  | Display total file sizes if the type is container |
| --type |  | Only inspect objects of the given type |

## Examples

### Format the output (--format)

If a format is specified, the given template will be executed for each result.

Go's [text/template](https://pkg.go.dev/text/template) package describes
all the details of the format.

### Specify target type (--type)

`--type config|container|image|node|network|secret|service|volume|task|plugin`

The `docker inspect` command matches any type of object by either ID or name. In
some cases multiple type of objects (for example, a container and a volume)
exist with the same name, making the result ambiguous.

To restrict `docker inspect` to a specific type of object, use the `--type`
option.

The following example inspects a volume named `myvolume`.

```console
$ docker inspect --type=volume myvolume
```

### Inspect the size of a container (-s, --size)

The `--size`, or short-form `-s`, option adds two additional fields to the
`docker inspect` output. This option only works for containers. The container
doesn't have to be running, it also works for stopped containers.

```console
$ docker inspect --size mycontainer
```

The output includes the full output of a regular `docker inspect` command, with
the following additional fields:

- `SizeRootFs`: the total size of all the files in the container, in bytes.
- `SizeRw`: the size of the files that have been created or changed in the
  container, compared to it's image, in bytes.

```console
$ docker run --name database -d redis
3b2cbf074c99db4a0cad35966a9e24d7bc277f5565c17233386589029b7db273
$ docker inspect --size database -f '{{ .SizeRootFs }}'
123125760
$ docker inspect --size database -f '{{ .SizeRw }}'
8192
$ docker exec database fallocate -l 1000 /newfile
$ docker inspect --size database -f '{{ .SizeRw }}'
12288
```

### Get an instance's IP address

For the most part, you can pick out any field from the JSON in a fairly
straightforward manner.

```console
$ docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $INSTANCE_ID
```

### Get an instance's MAC address

```console
$ docker inspect --format='{{range .NetworkSettings.Networks}}{{.MacAddress}}{{end}}' $INSTANCE_ID
```

### Get an instance's log path

```console
$ docker inspect --format='{{.LogPath}}' $INSTANCE_ID
```

### Get an instance's image name

```console
$ docker inspect --format='{{.Config.Image}}' $INSTANCE_ID
```

### List all port bindings

You can loop over arrays and maps in the results to produce simple text output:

```console
$ docker inspect --format='{{range $p, $conf := .NetworkSettings.Ports}} {{$p}} -> {{(index $conf 0).HostPort}} {{end}}' $INSTANCE_ID
```

### Find a specific port mapping

The `.Field` syntax doesn't work when the field name begins with a number, but
the template language's `index` function does. The `.NetworkSettings.Ports`
section contains a map of the internal port mappings to a list of external
address/port objects. To grab just the numeric public port, you use `index` to
find the specific port map, and then `index` 0 contains the first object inside
of that. Then, specify the `HostPort` field to get the public address.

```console
$ docker inspect --format='{{(index (index .NetworkSettings.Ports "8787/tcp") 0).HostPort}}' $INSTANCE_ID
```

### Get a subsection in JSON format

If you request a field which is itself a structure containing other fields, by
default you get a Go-style dump of the inner values. Docker adds a template
function, `json`, which can be applied to get results in JSON format.

```console
$ docker inspect --format='{{json .Config}}' $INSTANCE_ID
```
