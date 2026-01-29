# docker desktop engine use and more

# docker desktop engine use

# docker desktop engine use

| Description | Switch to Windows or Linux containers (Windows only) |
| --- | --- |
| Usage | docker desktop engine use NAME |

---

# docker desktop engine

# docker desktop engine

| Description | Commands to list and switch containers (Windows only) |
| --- | --- |
| Usage | docker desktop engine |

## Subcommands

| Command | Description |
| --- | --- |
| docker desktop engine ls | List available engines (Windows only) |
| docker desktop engine use | Switch to Windows or Linux containers (Windows only) |

---

# docker desktop kubernetes images

# docker desktop kubernetes images

| Description | List Kubernetes images used by Docker Desktop |
| --- | --- |
| Usage | docker desktop kubernetes images |

## Options

| Option | Default | Description |
| --- | --- | --- |
| --format | pretty | Format the output. Accepted values are: pretty, json |

---

# docker desktop kubernetes

# docker desktop kubernetes

| Description | Manage Kubernetes settings |
| --- | --- |
| Usage | docker desktop kubernetes |

Requires: Docker Desktop 4.44 and later

## Subcommands

| Command | Description |
| --- | --- |
| docker desktop kubernetes images | List Kubernetes images used by Docker Desktop |

---

# docker desktop logs

# docker desktop logs

| Description | Print log entries for Docker Desktop |
| --- | --- |
| Usage | docker desktop logs [OPTIONS] |

Requires: Docker Desktop 4.39 and later

## Options

| Option | Default | Description |
| --- | --- | --- |
| -b, --boot |  | Show logs from a specified boot. Zero means the current or boot, one the second last boot, and so on |
| -c, --color |  | Enable colored output. Priority levels are highlighted. |
| -m, --color-mode |  | Color mode to use. Can bedefaultorpriority |
| -D, --directory |  | Specifies a custom directory to search for log entries |
| -p, --priority | %!s(int64=-1) | Filter output by log priorities.-1is all,0is info or above,1filters for warnings or above,2filters for errors. |
| -S, --since |  | Start showing entries on or newer than the specified date and time. Uses the systemd.time(7) format. |
| -u, --unit |  | Filter by one or more categories (e.g.--unit=com.docker.backend.ipc,com.docker.backend.apiproxy) |
| -U, --until |  | Start showing entries on or before the specified date and time. Uses the systemd.time(7) format. |

---

# docker desktop restart

# docker desktop restart

| Description | Restart Docker Desktop |
| --- | --- |
| Usage | docker desktop restart |

## Options

| Option | Default | Description |
| --- | --- | --- |
| -d, --detach |  | Do not synchronously wait for the requested operation to complete. |
| --timeout |  | Terminate the running command after the specified timeout with a non-zero exit code. A value of zero (the default) or -1 means no timeout. |

---

# docker desktop start

# docker desktop start

| Description | Start Docker Desktop |
| --- | --- |
| Usage | docker desktop start [OPTIONS] |

> Note
>
> `docker desktop start` doesn't work when executed via SSH on Windows due to a limitation in how WinCred stores credentials securely.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -d, --detach |  | Do not synchronously wait for the requested operation to complete. |
| --timeout |  | Terminate the running command after the specified timeout with a non-zero exit code. A value of zero (the default) or -1 means no timeout. |

---

# docker desktop status

# docker desktop status

| Description | Display Docker Desktop's status |
| --- | --- |
| Usage | docker desktop status |

## Options

| Option | Default | Description |
| --- | --- | --- |
| --format | pretty | Format the output. Accepted values are: pretty, json |

---

# docker desktop stop

# docker desktop stop

| Description | Stop Docker Desktop |
| --- | --- |
| Usage | docker desktop stop [OPTIONS] |

## Options

| Option | Default | Description |
| --- | --- | --- |
| -d, --detach |  | Do not synchronously wait for the requested operation to complete |
| --force |  | Force Docker Desktop to stop |
| --timeout |  | Terminate the running command after the specified timeout with a non-zero exit code. A value of zero (the default) or -1 means no timeout |

---

# docker desktop update

# docker desktop update

| Description | Manage Docker Desktop updates |
| --- | --- |
| Usage | docker desktop update [OPTIONS] |

Requires: Docker Desktop 4.39 and later

## Options

| Option | Default | Description |
| --- | --- | --- |
| -k, --check-only |  | Check for updates without applying them |
| -q, --quiet |  | Quietly check and apply updates |

---

# docker desktop version

# docker desktop version

| Description | Show the Docker Desktop CLI plugin version information |
| --- | --- |
| Usage | docker desktop version [OPTIONS] |

## Description

Show the Docker Desktop CLI plugin version information

## Options

| Option | Default | Description |
| --- | --- | --- |
| -f, --format |  | Format the output. Values: [pretty | json]. (Default: pretty) |
| --short |  | Shows only the version number |

---

# docker desktop (Beta)

# docker desktop (Beta)

| Description | Docker Desktop |
| --- | --- |
| Usage | docker desktop |

Requires: Docker Desktop
[4.37](https://docs.docker.com/desktop/release-notes/#4370) and later

## Description

Control Docker Desktop from the CLI

## Subcommands

| Command | Description |
| --- | --- |
| docker desktop disable | Disable a feature |
| docker desktop enable | Enable a feature |
| docker desktop engine | Commands to list and switch containers (Windows only) |
| docker desktop kubernetes | Manage Kubernetes settings |
| docker desktop logs | Print log entries for Docker Desktop |
| docker desktop restart | Restart Docker Desktop |
| docker desktop start | Start Docker Desktop |
| docker desktop status | Display Docker Desktop's status |
| docker desktop stop | Stop Docker Desktop |
| docker desktop update | Manage Docker Desktop updates |
| docker desktop version | Show the Docker Desktop CLI plugin version information |

---

# docker image history

# docker image history

| Description | Show the history of an image |
| --- | --- |
| Usage | docker image history [OPTIONS] IMAGE |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker history |

## Description

Show the history of an image

## Options

| Option | Default | Description |
| --- | --- | --- |
| --format |  | Format output using a custom template:'table': Print output in table format with column headers (default)'table TEMPLATE': Print output in table format using the given Go template'json': Print in JSON format'TEMPLATE': Print output using the given Go template.Refer tohttps://docs.docker.com/go/formatting/for more information about formatting output with templates |
| -H, --human | true | Print sizes and dates in human readable format |
| --no-trunc |  | Don't truncate output |
| --platform |  | API 1.48+Show history for the given platform. Formatted asos[/arch[/variant]](e.g.,linux/amd64) |
| -q, --quiet |  | Only show image IDs |

## Examples

To see how the `docker:latest` image was built:

```console
$ docker history docker

IMAGE               CREATED             CREATED BY                                      SIZE                COMMENT
3e23a5875458        8 days ago          /bin/sh -c #(nop) ENV LC_ALL=C.UTF-8            0 B
8578938dd170        8 days ago          /bin/sh -c dpkg-reconfigure locales &&    loc   1.245 MB
be51b77efb42        8 days ago          /bin/sh -c apt-get update && apt-get install    338.3 MB
4b137612be55        6 weeks ago         /bin/sh -c #(nop) ADD jessie.tar.xz in /        121 MB
750d58736b4b        6 weeks ago         /bin/sh -c #(nop) MAINTAINER Tianon Gravi <ad   0 B
511136ea3c5a        9 months ago                                                        0 B                 Imported from -
```

To see how the `docker:apache` image was added to a container's base image:

```console
$ docker history docker:scm
IMAGE               CREATED             CREATED BY                                      SIZE                COMMENT
2ac9d1098bf1        3 months ago        /bin/bash                                       241.4 MB            Added Apache to Fedora base image
88b42ffd1f7c        5 months ago        /bin/sh -c #(nop) ADD file:1fd8d7f9f6557cafc7   373.7 MB
c69cab00d6ef        5 months ago        /bin/sh -c #(nop) MAINTAINER Lokesh Mandvekar   0 B
511136ea3c5a        19 months ago                                                       0 B                 Imported from -
```

### Format the output (--format)

The formatting option (`--format`) will pretty-prints history output
using a Go template.

Valid placeholders for the Go template are listed below:

| Placeholder | Description |
| --- | --- |
| .ID | Image ID |
| .CreatedSince | Elapsed time since the image was created if--human=true, otherwise timestamp of when image was created |
| .CreatedAt | Timestamp of when image was created |
| .CreatedBy | Command that was used to create the image |
| .Size | Image disk size |
| .Comment | Comment for image |

When using the `--format` option, the `history` command either
outputs the data exactly as the template declares or, when using the
`table` directive, includes column headers as well.

The following example uses a template without headers and outputs the
`ID` and `CreatedSince` entries separated by a colon (`:`) for the `busybox`
image:

```console
$ docker history --format "{{.ID}}: {{.CreatedSince}}" busybox

f6e427c148a7: 4 weeks ago
<missing>: 4 weeks ago
```

### Show history for a specific platform (--platform)

The `--platform` option allows you to specify which platform variant to show
history for if multiple platforms are present. By default, `docker history`
shows the history for the daemon's native platform or if not present, the
first available platform.

If the local image store has multiple platform variants of an image, the
`--platform` option selects which variant to show the history for. An error
is produced if the given platform is not present in the local image cache.

The platform option takes the `os[/arch[/variant]]` format; for example,
`linux/amd64` or `linux/arm64/v8`. Architecture and variant are optional,
and if omitted falls back to the daemon's defaults.

The following example pulls the RISC-V variant of the `alpine:latest` image
and shows its history.

```console
$ docker image pull --quiet --platform=linux/riscv64 alpine
docker.io/library/alpine:latest

$ docker image history --platform=linux/s390x alpine
IMAGE          CREATED       CREATED BY                                      SIZE      COMMENT
beefdbd8a1da   3 weeks ago   /bin/sh -c #(nop)  CMD ["/bin/sh"]              0B
<missing>      3 weeks ago   /bin/sh -c #(nop) ADD file:ba2637314e600db5a…   8.46MB
```

The following example attempts to show the history for a platform variant of
`alpine:latest` that doesn't exist in the local image store, resulting in
an error.

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

$ docker image history --platform=linux/s390x alpine
Error response from daemon: image with reference alpine:latest was found but does not match the specified platform: wanted linux/s390x
```

---

# docker image import

# docker image import

| Description | Import the contents from a tarball to create a filesystem image |
| --- | --- |
| Usage | docker image import [OPTIONS] file|URL|- [REPOSITORY[:TAG]] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker import |

## Description

You can specify a `URL` or `-` (dash) to take data directly from `STDIN`. The
`URL` can point to an archive (.tar, .tar.gz, .tgz, .bzip, .tar.xz, or .txz)
containing a filesystem or to an individual file on the Docker host. If you
specify an archive, Docker untars it in the container relative to the `/`
(root). If you specify an individual file, you must specify the full path within
the host. To import from a remote location, specify a `URI` that begins with the
`http://` or `https://` protocol.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -c, --change |  | Apply Dockerfile instruction to the created image |
| -m, --message |  | Set commit message for imported image |
| --platform |  | API 1.32+Set platform if server is multi-platform capable |

## Examples

### Import from a remote location

This creates a new untagged image.

```console
$ docker import https://example.com/exampleimage.tgz
```

### Import from a local file

Import to docker via pipe and `STDIN`.

```console
$ cat exampleimage.tgz | docker import - exampleimagelocal:new
```

Import to docker from a local archive.

```console
$ docker import /path/to/exampleimage.tgz
```

### Import from a local directory

```console
$ sudo tar -c . | docker import - exampleimagedir
```

Note the `sudo` in this example – you must preserve
the ownership of the files (especially root ownership) during the
archiving with tar. If you are not root (or the sudo command) when you
tar, then the ownerships might not get preserved.

### Import with new configurations (-c, --change)

The `--change` option applies `Dockerfile` instructions to the image that is
created. Not all `Dockerfile` instructions are supported; the list of instructions
is limited to metadata (configuration) changes. The following `Dockerfile`
instructions are supported:

- [CMD](https://docs.docker.com/reference/dockerfile/#cmd)
- [ENTRYPOINT](https://docs.docker.com/reference/dockerfile/#entrypoint)
- [ENV](https://docs.docker.com/reference/dockerfile/#env)
- [EXPOSE](https://docs.docker.com/reference/dockerfile/#expose)
- [HEALTHCHECK](https://docs.docker.com/reference/dockerfile/#healthcheck)
- [LABEL](https://docs.docker.com/reference/dockerfile/#label)
- [ONBUILD](https://docs.docker.com/reference/dockerfile/#onbuild)
- [STOPSIGNAL](https://docs.docker.com/reference/dockerfile/#stopsignal)
- [USER](https://docs.docker.com/reference/dockerfile/#user)
- [VOLUME](https://docs.docker.com/reference/dockerfile/#volume)
- [WORKDIR](https://docs.docker.com/reference/dockerfile/#workdir)

The following example imports an image from a TAR-file containing a root-filesystem,
and sets the `DEBUG` environment-variable in the resulting image:

```console
$ docker import --change "ENV DEBUG=true" ./rootfs.tgz exampleimagedir
```

The `--change` option can be set multiple times to apply multiple `Dockerfile`
instructions. The example below sets the `LABEL1` and `LABEL2` labels on
the imported image, in addition to the `DEBUG` environment variable from
the previous example:

```console
$ docker import \
    --change "ENV DEBUG=true" \
    --change "LABEL LABEL1=hello" \
    --change "LABEL LABEL2=world" \
    ./rootfs.tgz exampleimagedir
```

### Import with a commit message (-m, --message)

The `--message` (or `-m`) option allows you to set a custom comment in
the image's metadata. The following example imports an image from a local
archive and sets a custom message.

```console
$ docker import --message "New image imported from tarball" ./rootfs.tgz exampleimagelocal:new
sha256:25e54c0df7dc49da9093d50541e0ed4508a6b78705057f1a9bebf1d564e2cb00
```

After importing, the message is set in the "Comment" field of the image's
configuration, which is shown when viewing the image's history:

```console
$ docker image history exampleimagelocal:new

IMAGE          CREATED         CREATED BY   SIZE      COMMENT
25e54c0df7dc   2 minutes ago                53.6MB    New image imported from tarball
```

### When the daemon supports multiple operating systems

If the daemon supports multiple operating systems, and the image being imported
does not match the default operating system, it may be necessary to add
`--platform`. This would be necessary when importing a Linux image into a Windows
daemon.

```console
$ docker import --platform=linux .\linuximage.tar
```

### Set the platform for the imported image (--platform)

The `--platform` option allows you to specify the platform for the imported
image. By default, the daemon's native platform is used as platform, but
the `--platform` option allows you to override the default, for example, in
situations where the imported root filesystem is for a different architecture
or operating system.

The platform option takes the `os[/arch[/variant]]` format; for example,
`linux/amd64` or `linux/arm64/v8`. Architecture and variant are optional,
and default to the daemon's native architecture if omitted.

The following example imports an image from a root-filesystem in `rootfs.tgz`,
and sets the image's platform to `linux/amd64`;

```console
$ docker image import --platform=linux/amd64  ./rootfs.tgz imported:latest
sha256:44a8b44157dad5edcff85f0c93a3e455f3b20a046d025af4ec50ed990d7ebc09
```

After importing the image, the image's platform is set in the image's
configuration;

```console
$ docker image inspect --format '{{.Os}}/{{.Architecture}}' imported:latest
linux/amd64
```

---

# docker image inspect

# docker image inspect

| Description | Display detailed information on one or more images |
| --- | --- |
| Usage | docker image inspect [OPTIONS] IMAGE [IMAGE...] |

## Description

Display detailed information on one or more images

## Options

| Option | Default | Description |
| --- | --- | --- |
| -f, --format |  | Format output using a custom template:'json': Print in JSON format'TEMPLATE': Print output using the given Go template.Refer tohttps://docs.docker.com/go/formatting/for more information about formatting output with templates |
| --platform |  | API 1.49+Inspect a specific platform of the multi-platform image.If the image or the server is not multi-platform capable, the command will error out if the platform does not match.'os[/arch[/variant]]': Explicit platform (eg. linux/amd64) |

---

# docker image load

# docker image load

| Description | Load an image from a tar archive or STDIN |
| --- | --- |
| Usage | docker image load [OPTIONS] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker load |

## Description

Load an image or repository from a tar archive (even if compressed with gzip,
bzip2, xz or zstd) from a file or STDIN. It restores both images and tags.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -i, --input |  | Read from tar archive file, instead of STDIN |
| --platform |  | API 1.48+Load only the given platform(s). Formatted as a comma-separated list ofos[/arch[/variant]](e.g.,linux/amd64,linux/arm64/v8). |
| -q, --quiet |  | Suppress the load output |

## Examples

```console
$ docker image ls

REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
```

### Load images from STDIN

```console
$ docker load < busybox.tar.gz

Loaded image: busybox:latest
$ docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
busybox             latest              769b9341d937        7 weeks ago         2.489 MB
```

### Load images from a file (--input)

```console
$ docker load --input fedora.tar

Loaded image: fedora:rawhide
Loaded image: fedora:20

$ docker images

REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
busybox             latest              769b9341d937        7 weeks ago         2.489 MB
fedora              rawhide             0d20aec6529d        7 weeks ago         387 MB
fedora              20                  58394af37342        7 weeks ago         385.5 MB
fedora              heisenbug           58394af37342        7 weeks ago         385.5 MB
fedora              latest              58394af37342        7 weeks ago         385.5 MB
```

### Load a specific platform (--platform)

The `--platform` option allows you to specify which platform variant of the
image to load. By default, `docker load` loads all platform variants that
are present in the archive. Use the `--platform` option to specify which
platform variant of the image to load. An error is produced if the given
platform is not present in the archive.

The platform option takes the `os[/arch[/variant]]` format; for example,
`linux/amd64` or `linux/arm64/v8`. Architecture and variant are optional,
and default to the daemon's native architecture if omitted.

The following example loads the `linux/amd64` variant of an `alpine` image
from an archive that contains multiple platform variants.

```console
$ docker image load -i image.tar --platform=linux/amd64
Loaded image: alpine:latest
```

The following example attempts to load a `linux/ppc64le` image from an
archive, but the given platform is not present in the archive;

```console
$ docker image load -i image.tar --platform=linux/ppc64le
requested platform (linux/ppc64le) not found: image might be filtered out
```

---

# docker image ls

# docker image ls

| Description | List images |
| --- | --- |
| Usage | docker image ls [OPTIONS] [REPOSITORY[:TAG]] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker image listdocker images |

## Description

The default `docker images` will show all top level
images, their repository and tags, and their size.

Docker images have intermediate layers that increase reusability,
decrease disk usage, and speed up `docker build` by
allowing each step to be cached. These intermediate layers are not shown
by default.

Untagged (dangling) images are also hidden by default. Use the `-a` (`--all`)
flag to show intermediate layers and dangling images.

The `SIZE` is the cumulative space taken up by the image and all
its parent images. This is also the disk space used by the contents of the
Tar file created when you `docker save` an image.

An image will be listed more than once if it has multiple repository names
or tags. This single image (identifiable by its matching `IMAGE ID`)
uses up the `SIZE` listed only once.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -a, --all |  | Show all images (default hides intermediate and dangling images) |
| --digests |  | Show digests |
| -f, --filter |  | Filter output based on conditions provided |
| --format |  | Format output using a custom template:'table': Print output in table format with column headers (default)'table TEMPLATE': Print output in table format using the given Go template'json': Print in JSON format'TEMPLATE': Print output using the given Go template.Refer tohttps://docs.docker.com/go/formatting/for more information about formatting output with templates |
| --no-trunc |  | Don't truncate output |
| -q, --quiet |  | Only show image IDs |
| --tree |  | API 1.47+experimental (CLI)List multi-platform images as a tree (EXPERIMENTAL) |

## Examples

### List the most recently created images

```console
$ docker images

REPOSITORY                TAG                 IMAGE ID            CREATED             SIZE
<none>                    <none>              77af4d6b9913        19 hours ago        1.089 GB
committ                   latest              b6fa739cedf5        19 hours ago        1.089 GB
<none>                    <none>              78a85c484f71        19 hours ago        1.089 GB
docker                    latest              30557a29d5ab        20 hours ago        1.089 GB
<none>                    <none>              5ed6274db6ce        24 hours ago        1.089 GB
postgres                  9                   746b819f315e        4 days ago          213.4 MB
postgres                  9.3                 746b819f315e        4 days ago          213.4 MB
postgres                  9.3.5               746b819f315e        4 days ago          213.4 MB
postgres                  latest              746b819f315e        4 days ago          213.4 MB
```

### List images by name and tag

The `docker images` command takes an optional `[REPOSITORY[:TAG]]` argument
that restricts the list to images that match the argument. If you specify
`REPOSITORY`but no `TAG`, the `docker images` command lists all images in the
given repository.

For example, to list all images in the `java` repository, run the following command:

```console
$ docker images java

REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
java                8                   308e519aac60        6 days ago          824.5 MB
java                7                   493d82594c15        3 months ago        656.3 MB
java                latest              2711b1d6f3aa        5 months ago        603.9 MB
```

The `[REPOSITORY[:TAG]]` value must be an exact match. This means that, for example,
`docker images jav` does not match the image `java`.

If both `REPOSITORY` and `TAG` are provided, only images matching that
repository and tag are listed. To find all local images in the `java`
repository with tag `8` you can use:

```console
$ docker images java:8

REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
java                8                   308e519aac60        6 days ago          824.5 MB
```

If nothing matches `REPOSITORY[:TAG]`, the list is empty.

```console
$ docker images java:0

REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
```

### List the full length image IDs (--no-trunc)

```console
$ docker images --no-trunc

REPOSITORY                    TAG                 IMAGE ID                                                                  CREATED             SIZE
<none>                        <none>              sha256:77af4d6b9913e693e8d0b4b294fa62ade6054e6b2f1ffb617ac955dd63fb0182   19 hours ago        1.089 GB
committest                    latest              sha256:b6fa739cedf5ea12a620a439402b6004d057da800f91c7524b5086a5e4749c9f   19 hours ago        1.089 GB
<none>                        <none>              sha256:78a85c484f71509adeaace20e72e941f6bdd2b25b4c75da8693efd9f61a37921   19 hours ago        1.089 GB
docker                        latest              sha256:30557a29d5abc51e5f1d5b472e79b7e296f595abcf19fe6b9199dbbc809c6ff4   20 hours ago        1.089 GB
<none>                        <none>              sha256:0124422dd9f9cf7ef15c0617cda3931ee68346455441d66ab8bdc5b05e9fdce5   20 hours ago        1.089 GB
<none>                        <none>              sha256:18ad6fad340262ac2a636efd98a6d1f0ea775ae3d45240d3418466495a19a81b   22 hours ago        1.082 GB
<none>                        <none>              sha256:f9f1e26352f0a3ba6a0ff68167559f64f3e21ff7ada60366e2d44a04befd1d3a   23 hours ago        1.089 GB
tryout                        latest              sha256:2629d1fa0b81b222fca63371ca16cbf6a0772d07759ff80e8d1369b926940074   23 hours ago        131.5 MB
<none>                        <none>              sha256:5ed6274db6ceb2397844896966ea239290555e74ef307030ebb01ff91b1914df   24 hours ago        1.089 GB
```

### List image digests (--digests)

Images that use the v2 or later format have a content-addressable identifier
called a `digest`. As long as the input used to generate the image is
unchanged, the digest value is predictable. To list image digest values, use
the `--digests` flag:

```console
$ docker images --digests
REPOSITORY                         TAG                 DIGEST                                                                    IMAGE ID            CREATED             SIZE
localhost:5000/test/busybox        <none>              sha256:cbbf2f9a99b47fc460d422812b6a5adff7dfee951d8fa2e4a98caa0382cfbdbf   4986bf8c1536        9 weeks ago         2.43 MB
```

When pushing or pulling to a 2.0 registry, the `push` or `pull` command
output includes the image digest. You can `pull` using a digest value. You can
also reference by digest in `create`, `run`, and `rmi` commands, as well as the
`FROM` image reference in a Dockerfile.

### Filtering (--filter)

The filtering flag (`-f` or `--filter`) format is of "key=value". If there is more
than one filter, then pass multiple flags (e.g., `--filter "foo=bar" --filter "bif=baz"`).

The currently supported filters are:

- dangling (boolean - true or false)
- label (`label=<key>` or `label=<key>=<value>`)
- before (`<image-name>[:<tag>]`, `<image id>` or `<image@digest>`) - filter images created before given id or references
- since (`<image-name>[:<tag>]`, `<image id>` or `<image@digest>`) - filter images created since given id or references
- reference (pattern of an image reference) - filter images whose reference matches the specified pattern

#### Show untagged images (dangling)

```console
$ docker images --filter "dangling=true"

REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
<none>              <none>              8abc22fbb042        4 weeks ago         0 B
<none>              <none>              48e5f45168b9        4 weeks ago         2.489 MB
<none>              <none>              bf747efa0e2f        4 weeks ago         0 B
<none>              <none>              980fe10e5736        12 weeks ago        101.4 MB
<none>              <none>              dea752e4e117        12 weeks ago        101.4 MB
<none>              <none>              511136ea3c5a        8 months ago        0 B
```

This will display untagged images that are the leaves of the images tree (not
intermediary layers). These images occur when a new build of an image takes the
`repo:tag` away from the image ID, leaving it as `<none>:<none>` or untagged.
A warning will be issued if trying to remove an image when a container is presently
using it. By having this flag it allows for batch cleanup.

You can use this in conjunction with `docker rmi`:

```console
$ docker rmi $(docker images -f "dangling=true" -q)

8abc22fbb042
48e5f45168b9
bf747efa0e2f
980fe10e5736
dea752e4e117
511136ea3c5a
```

Docker warns you if any containers exist that are using these untagged images.

#### Show images with a given label

The `label` filter matches images based on the presence of a `label` alone or a `label` and a
value.

The following filter matches images with the `com.example.version` label regardless of its value.

```console
$ docker images --filter "label=com.example.version"

REPOSITORY          TAG                 IMAGE ID            CREATED              SIZE
match-me-1          latest              eeae25ada2aa        About a minute ago   188.3 MB
match-me-2          latest              dea752e4e117        About a minute ago   188.3 MB
```

The following filter matches images with the `com.example.version` label with the `1.0` value.

```console
$ docker images --filter "label=com.example.version=1.0"

REPOSITORY          TAG                 IMAGE ID            CREATED              SIZE
match-me            latest              511136ea3c5a        About a minute ago   188.3 MB
```

In this example, with the `0.1` value, it returns an empty set because no matches were found.

```console
$ docker images --filter "label=com.example.version=0.1"
REPOSITORY          TAG                 IMAGE ID            CREATED              SIZE
```

#### Filter images by time

The `before` filter shows only images created before the image with
a given ID or reference. For example, having these images:

```console
$ docker images

REPOSITORY          TAG                 IMAGE ID            CREATED              SIZE
image1              latest              eeae25ada2aa        4 minutes ago        188.3 MB
image2              latest              dea752e4e117        9 minutes ago        188.3 MB
image3              latest              511136ea3c5a        25 minutes ago       188.3 MB
```

Filtering with `before` would give:

```console
$ docker images --filter "before=image1"

REPOSITORY          TAG                 IMAGE ID            CREATED              SIZE
image2              latest              dea752e4e117        9 minutes ago        188.3 MB
image3              latest              511136ea3c5a        25 minutes ago       188.3 MB
```

Filtering with `since` would give:

```console
$ docker images --filter "since=image3"
REPOSITORY          TAG                 IMAGE ID            CREATED              SIZE
image1              latest              eeae25ada2aa        4 minutes ago        188.3 MB
image2              latest              dea752e4e117        9 minutes ago        188.3 MB
```

#### Filter images by reference

The `reference` filter shows only images whose reference matches
the specified pattern.

```console
$ docker images

REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
busybox             latest              e02e811dd08f        5 weeks ago         1.09 MB
busybox             uclibc              e02e811dd08f        5 weeks ago         1.09 MB
busybox             musl                733eb3059dce        5 weeks ago         1.21 MB
busybox             glibc               21c16b6787c6        5 weeks ago         4.19 MB
```

Filtering with `reference` would give:

```console
$ docker images --filter=reference='busy*:*libc'

REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
busybox             uclibc              e02e811dd08f        5 weeks ago         1.09 MB
busybox             glibc               21c16b6787c6        5 weeks ago         4.19 MB
```

Filtering with multiple `reference` would give, either match A or B:

```console
$ docker images --filter=reference='busy*:uclibc' --filter=reference='busy*:glibc'

REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
busybox             uclibc              e02e811dd08f        5 weeks ago         1.09 MB
busybox             glibc               21c16b6787c6        5 weeks ago         4.19 MB
```

### Format the output (--format)

The formatting option (`--format`) will pretty print container output
using a Go template.

Valid placeholders for the Go template are listed below:

| Placeholder | Description |
| --- | --- |
| .ID | Image ID |
| .Repository | Image repository |
| .Tag | Image tag |
| .Digest | Image digest |
| .CreatedSince | Elapsed time since the image was created |
| .CreatedAt | Time when the image was created |
| .Size | Image disk size |

When using the `--format` option, the `image` command will either
output the data exactly as the template declares or, when using the
`table` directive, will include column headers as well.

The following example uses a template without headers and outputs the
`ID` and `Repository` entries separated by a colon (`:`) for all images:

```console
$ docker images --format "{{.ID}}: {{.Repository}}"

77af4d6b9913: <none>
b6fa739cedf5: committ
78a85c484f71: <none>
30557a29d5ab: docker
5ed6274db6ce: <none>
746b819f315e: postgres
746b819f315e: postgres
746b819f315e: postgres
746b819f315e: postgres
```

To list all images with their repository and tag in a table format you
can use:

```console
$ docker images --format "table {{.ID}}\t{{.Repository}}\t{{.Tag}}"

IMAGE ID            REPOSITORY                TAG
77af4d6b9913        <none>                    <none>
b6fa739cedf5        committ                   latest
78a85c484f71        <none>                    <none>
30557a29d5ab        docker                    latest
5ed6274db6ce        <none>                    <none>
746b819f315e        postgres                  9
746b819f315e        postgres                  9.3
746b819f315e        postgres                  9.3.5
746b819f315e        postgres                  latest
```

To list all images in JSON format, use the `json` directive:

```console
$ docker images --format json
{"Containers":"N/A","CreatedAt":"2021-03-04 03:24:42 +0100 CET","CreatedSince":"5 days ago","Digest":"\u003cnone\u003e","ID":"4dd97cefde62","Repository":"ubuntu","SharedSize":"N/A","Size":"72.9MB","Tag":"latest","UniqueSize":"N/A"}
{"Containers":"N/A","CreatedAt":"2021-02-17 22:19:54 +0100 CET","CreatedSince":"2 weeks ago","Digest":"\u003cnone\u003e","ID":"28f6e2705743","Repository":"alpine","SharedSize":"N/A","Size":"5.61MB","Tag":"latest","UniqueSize":"N/A"}
```

---

# docker image prune

# docker image prune

| Description | Remove unused images |
| --- | --- |
| Usage | docker image prune [OPTIONS] |

## Description

Remove all dangling images. If `-a` is specified, also remove all images not referenced by any container.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -a, --all |  | Remove all unused images, not just dangling ones |
| --filter |  | Provide filter values (e.g.until=<timestamp>) |
| -f, --force |  | Do not prompt for confirmation |

## Examples

Example output:

```console
$ docker image prune -a

WARNING! This will remove all images without at least one container associated to them.
Are you sure you want to continue? [y/N] y
Deleted Images:
untagged: alpine:latest
untagged: alpine@sha256:3dcdb92d7432d56604d4545cbd324b14e647b313626d99b889d0626de158f73a
deleted: sha256:4e38e38c8ce0b8d9041a9c4fefe786631d1416225e13b0bfe8cfa2321aec4bba
deleted: sha256:4fe15f8d0ae69e169824f25f1d4da3015a48feeeeebb265cd2e328e15c6a869f
untagged: alpine:3.3
untagged: alpine@sha256:4fa633f4feff6a8f02acfc7424efd5cb3e76686ed3218abf4ca0fa4a2a358423
untagged: my-jq:latest
deleted: sha256:ae67841be6d008a374eff7c2a974cde3934ffe9536a7dc7ce589585eddd83aff
deleted: sha256:34f6f1261650bc341eb122313372adc4512b4fceddc2a7ecbb84f0958ce5ad65
deleted: sha256:cf4194e8d8db1cb2d117df33f2c75c0369c3a26d96725efb978cc69e046b87e7
untagged: my-curl:latest
deleted: sha256:b2789dd875bf427de7f9f6ae001940073b3201409b14aba7e5db71f408b8569e
deleted: sha256:96daac0cb203226438989926fc34dd024f365a9a8616b93e168d303cfe4cb5e9
deleted: sha256:5cbd97a14241c9cd83250d6b6fc0649833c4a3e84099b968dd4ba403e609945e
deleted: sha256:a0971c4015c1e898c60bf95781c6730a05b5d8a2ae6827f53837e6c9d38efdec
deleted: sha256:d8359ca3b681cc5396a4e790088441673ed3ce90ebc04de388bfcd31a0716b06
deleted: sha256:83fc9ba8fb70e1da31dfcc3c88d093831dbd4be38b34af998df37e8ac538260c
deleted: sha256:ae7041a4cc625a9c8e6955452f7afe602b401f662671cea3613f08f3d9343b35
deleted: sha256:35e0f43a37755b832f0bbea91a2360b025ee351d7309dae0d9737bc96b6d0809
deleted: sha256:0af941dd29f00e4510195dd00b19671bc591e29d1495630e7e0f7c44c1e6a8c0
deleted: sha256:9fc896fc2013da84f84e45b3096053eb084417b42e6b35ea0cce5a3529705eac
deleted: sha256:47cf20d8c26c46fff71be614d9f54997edacfe8d46d51769706e5aba94b16f2b
deleted: sha256:2c675ee9ed53425e31a13e3390bf3f539bf8637000e4bcfbb85ee03ef4d910a1

Total reclaimed space: 16.43 MB
```

### Filtering (--filter)

The filtering flag (`--filter`) format is of "key=value". If there is more
than one filter, then pass multiple flags (e.g., `--filter "foo=bar" --filter "bif=baz"`)

The currently supported filters are:

- until (`<timestamp>`) - only remove images created before given timestamp
- label (`label=<key>`, `label=<key>=<value>`, `label!=<key>`, or `label!=<key>=<value>`) - only remove images with (or without, in case `label!=...` is used) the specified labels.

The `until` filter can be Unix timestamps, date formatted
timestamps, or Go duration strings supported by [ParseDuration](https://pkg.go.dev/time#ParseDuration) (e.g. `10m`, `1h30m`) computed
relative to the daemon machine’s time. Supported formats for date
formatted time stamps include RFC3339Nano, RFC3339, `2006-01-02T15:04:05`,
`2006-01-02T15:04:05.999999999`, `2006-01-02T07:00`, and `2006-01-02`. The local
timezone on the daemon will be used if you do not provide either a `Z` or a
`+-00:00` timezone offset at the end of the timestamp. When providing Unix
timestamps enter seconds[.nanoseconds], where seconds is the number of seconds
that have elapsed since January 1, 1970 (midnight UTC/GMT), not counting leap
seconds (aka Unix epoch or Unix time), and the optional .nanoseconds field is a
fraction of a second no more than nine digits long.

The `label` filter accepts two formats. One is the `label=...` (`label=<key>` or `label=<key>=<value>`),
which removes images with the specified labels. The other
format is the `label!=...` (`label!=<key>` or `label!=<key>=<value>`), which removes
images without the specified labels.

> Note
>
> **Predicting what will be removed**
>
>
>
> If you are using positive filtering (testing for the existence of a label or
> that a label has a specific value), you can use `docker image ls` with the
> same filtering syntax to see which images match your filter.
>
>
>
> However, if you are using negative filtering (testing for the absence of a
> label or that a label doesn't have a specific value), this type of filter
> doesn't work with `docker image ls` so you cannot easily predict which images
> will be removed. In addition, the confirmation prompt for `docker image prune`
> always warns that all dangling images will be removed, even if you are using
> `--filter`.

The following removes images created before `2017-01-04T00:00:00`:

```console
$ docker images --format 'table {{.Repository}}\t{{.Tag}}\t{{.ID}}\t{{.CreatedAt}}\t{{.Size}}'
REPOSITORY          TAG                 IMAGE ID            CREATED AT                      SIZE
foo                 latest              2f287ac753da        2017-01-04 13:42:23 -0800 PST   3.98 MB
alpine              latest              88e169ea8f46        2016-12-27 10:17:25 -0800 PST   3.98 MB
busybox             latest              e02e811dd08f        2016-10-07 14:03:58 -0700 PDT   1.09 MB

$ docker image prune -a --force --filter "until=2017-01-04T00:00:00"

Deleted Images:
untagged: alpine:latest
untagged: alpine@sha256:dfbd4a3a8ebca874ebd2474f044a0b33600d4523d03b0df76e5c5986cb02d7e8
untagged: busybox:latest
untagged: busybox@sha256:29f5d56d12684887bdfa50dcd29fc31eea4aaf4ad3bec43daf19026a7ce69912
deleted: sha256:e02e811dd08fd49e7f6032625495118e63f597eb150403d02e3238af1df240ba
deleted: sha256:e88b3f82283bc59d5e0df427c824e9f95557e661fcb0ea15fb0fb6f97760f9d9

Total reclaimed space: 1.093 MB

$ docker images --format 'table {{.Repository}}\t{{.Tag}}\t{{.ID}}\t{{.CreatedAt}}\t{{.Size}}'

REPOSITORY          TAG                 IMAGE ID            CREATED AT                      SIZE
foo                 latest              2f287ac753da        2017-01-04 13:42:23 -0800 PST   3.98 MB
```

The following removes images created more than 10 days (`240h`) ago:

```console
$ docker images

REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
foo                 latest              2f287ac753da        14 seconds ago      3.98 MB
alpine              latest              88e169ea8f46        8 days ago          3.98 MB
debian              jessie              7b0a06c805e8        2 months ago        123 MB
busybox             latest              e02e811dd08f        2 months ago        1.09 MB
golang              1.7.0               138c2e655421        4 months ago        670 MB

$ docker image prune -a --force --filter "until=240h"

Deleted Images:
untagged: golang:1.7.0
untagged: golang@sha256:6765038c2b8f407fd6e3ecea043b44580c229ccfa2a13f6d85866cf2b4a9628e
deleted: sha256:138c2e6554219de65614d88c15521bfb2da674cbb0bf840de161f89ff4264b96
deleted: sha256:ec353c2e1a673f456c4b78906d0d77f9d9456cfb5229b78c6a960bfb7496b76a
deleted: sha256:fe22765feaf3907526b4921c73ea6643ff9e334497c9b7e177972cf22f68ee93
deleted: sha256:ff845959c80148421a5c3ae11cc0e6c115f950c89bc949646be55ed18d6a2912
deleted: sha256:a4320831346648c03db64149eafc83092e2b34ab50ca6e8c13112388f25899a7
deleted: sha256:4c76020202ee1d9709e703b7c6de367b325139e74eebd6b55b30a63c196abaf3
deleted: sha256:d7afd92fb07236c8a2045715a86b7d5f0066cef025018cd3ca9a45498c51d1d6
deleted: sha256:9e63c5bce4585dd7038d830a1f1f4e44cb1a1515b00e620ac718e934b484c938
untagged: debian:jessie
untagged: debian@sha256:c1af755d300d0c65bb1194d24bce561d70c98a54fb5ce5b1693beb4f7988272f
deleted: sha256:7b0a06c805e8f23807fb8856621c60851727e85c7bcb751012c813f122734c8d
deleted: sha256:f96222d75c5563900bc4dd852179b720a0885de8f7a0619ba0ac76e92542bbc8

Total reclaimed space: 792.6 MB

$ docker images

REPOSITORY          TAG                 IMAGE ID            CREATED              SIZE
foo                 latest              2f287ac753da        About a minute ago   3.98 MB
alpine              latest              88e169ea8f46        8 days ago           3.98 MB
busybox             latest              e02e811dd08f        2 months ago         1.09 MB
```

The following example removes images with the label `deprecated`:

```console
$ docker image prune --filter="label=deprecated"
```

The following example removes images with the label `maintainer` set to `john`:

```console
$ docker image prune --filter="label=maintainer=john"
```

This example removes images which have no `maintainer` label:

```console
$ docker image prune --filter="label!=maintainer"
```

This example removes images which have a maintainer label not set to `john`:

```console
$ docker image prune --filter="label!=maintainer=john"
```

> Note
>
> You are prompted for confirmation before the `prune` removes
> anything, but you are not shown a list of what will potentially be removed.
> In addition, `docker image ls` doesn't support negative filtering, so it
> difficult to predict what images will actually be removed.
