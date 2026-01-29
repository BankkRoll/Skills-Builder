# Bind mounts and more

# Bind mounts

> Using bind mounts

# Bind mounts

   Table of contents

---

When you use a bind mount, a file or directory on the host machine is mounted
from the host into a container. By contrast, when you use a volume, a new
directory is created within Docker's storage directory on the host machine, and
Docker manages that directory's contents.

## When to use bind mounts

Bind mounts are appropriate for the following types of use case:

- Sharing source code or build artifacts between a development environment on
  the Docker host and a container.
- When you want to create or generate files in a container and persist the
  files onto the host's filesystem.
- Sharing configuration files from the host machine to containers. This is how
  Docker provides DNS resolution to containers by default, by mounting
  `/etc/resolv.conf` from the host machine into each container.

Bind mounts are also available for builds: you can bind mount source code from
the host into the build container to test, lint, or compile a project.

## Bind-mounting over existing data

If you bind mount file or directory into a directory in the container in which
files or directories exist, the pre-existing files are obscured by the mount.
This is similar to if you were to save files into `/mnt` on a Linux host, and
then mounted a USB drive into `/mnt`. The contents of `/mnt` would be obscured
by the contents of the USB drive until the USB drive was unmounted.

With containers, there's no straightforward way of removing a mount to reveal
the obscured files again. Your best option is to recreate the container without
the mount.

## Considerations and constraints

- Bind mounts have write access to files on the host by default.
  One side effect of using bind mounts is that you can change the host
  filesystem via processes running in a container, including creating,
  modifying, or deleting important system files or directories. This capability
  can have security implications. For example, it may affect non-Docker
  processes on the host system.
  You can use the `readonly` or `ro` option to prevent the container from
  writing to the mount.
- Bind mounts are created to the Docker daemon host, not the client.
  If you're using a remote Docker daemon, you can't create a bind mount to
  access files on the client machine in a container.
  For Docker Desktop, the daemon runs inside a Linux VM, not directly on the
  native host. Docker Desktop has built-in mechanisms that transparently handle
  bind mounts, allowing you to share native host filesystem paths with
  containers running in the virtual machine.
- Containers with bind mounts are strongly tied to the host.
  Bind mounts rely on the host machine's filesystem having a specific directory
  structure available. This reliance means that containers with bind mounts may
  fail if run on a different host without the same directory structure.

## Syntax

To create a bind mount, you can use either the `--mount` or `--volume` flag.

```console
$ docker run --mount type=bind,src=<host-path>,dst=<container-path>
$ docker run --volume <host-path>:<container-path>
```

In general, `--mount` is preferred. The main difference is that the `--mount`
flag is more explicit and supports all the available options.

If you use `--volume` to bind-mount a file or directory that does not yet
exist on the Docker host, Docker automatically creates the directory on the
host for you. It's always created as a directory.

`--mount` does not automatically create a directory if the specified mount
path does not exist on the host. Instead, it produces an error:

```console
$ docker run --mount type=bind,src=/dev/noexist,dst=/mnt/foo alpine
docker: Error response from daemon: invalid mount config for type "bind": bind source path does not exist: /dev/noexist.
```

### Options for --mount

The `--mount` flag consists of multiple key-value pairs, separated by commas
and each consisting of a `<key>=<value>` tuple. The order of the keys isn't
significant.

```console
$ docker run --mount type=bind,src=<host-path>,dst=<container-path>[,<key>=<value>...]
```

Valid options for `--mount type=bind` include:

| Option | Description |
| --- | --- |
| source,src | The location of the file or directory on the host. This can be an absolute or relative path. |
| destination,dst,target | The path where the file or directory is mounted in the container. Must be an absolute path. |
| readonly,ro | If present, causes the bind mount to bemounted into the container as read-only. |
| bind-propagation | If present, changes thebind propagation. |

Example

```console
$ docker run --mount type=bind,src=.,dst=/project,ro,bind-propagation=rshared
```

### Options for --volume

The `--volume` or `-v` flag consists of three fields, separated by colon
characters (`:`). The fields must be in the correct order.

```console
$ docker run -v <host-path>:<container-path>[:opts]
```

The first field is the path on the host to bind mount into the container. The
second field is the path where the file or directory is mounted in the
container.

The third field is optional, and is a comma-separated list of options. Valid
options for `--volume` with a bind mount include:

| Option | Description |
| --- | --- |
| readonly,ro | If present, causes the bind mount to bemounted into the container as read-only. |
| z,Z | Configures SELinux labeling. SeeConfigure the SELinux label |
| rprivate(default) | Sets bind propagation torprivatefor this mount. SeeConfigure bind propagation. |
| private | Sets bind propagation toprivatefor this mount. SeeConfigure bind propagation. |
| rshared | Sets bind propagation torsharedfor this mount. SeeConfigure bind propagation. |
| shared | Sets bind propagation tosharedfor this mount. SeeConfigure bind propagation. |
| rslave | Sets bind propagation torslavefor this mount. SeeConfigure bind propagation. |
| slave | Sets bind propagation toslavefor this mount. SeeConfigure bind propagation. |

Example

```console
$ docker run -v .:/project:ro,rshared
```

## Start a container with a bind mount

Consider a case where you have a directory `source` and that when you build the
source code, the artifacts are saved into another directory, `source/target/`.
You want the artifacts to be available to the container at `/app/`, and you
want the container to get access to a new build each time you build the source
on your development host. Use the following command to bind-mount the `target/`
directory into your container at `/app/`. Run the command from within the
`source` directory. The `$(pwd)` sub-command expands to the current working
directory on Linux or macOS hosts.
If you're on Windows, see also
[Path conversions on Windows](https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/topics/).

The following `--mount` and `-v` examples produce the same result. You can't
run them both unless you remove the `devtest` container after running the first
one.

```console
$ docker run -d \
  -it \
  --name devtest \
  --mount type=bind,source="$(pwd)"/target,target=/app \
  nginx:latest
```

```console
$ docker run -d \
  -it \
  --name devtest \
  -v "$(pwd)"/target:/app \
  nginx:latest
```

Use `docker inspect devtest` to verify that the bind mount was created
correctly. Look for the `Mounts` section:

```json
"Mounts": [
    {
        "Type": "bind",
        "Source": "/tmp/source/target",
        "Destination": "/app",
        "Mode": "",
        "RW": true,
        "Propagation": "rprivate"
    }
],
```

This shows that the mount is a `bind` mount, it shows the correct source and
destination, it shows that the mount is read-write, and that the propagation is
set to `rprivate`.

Stop and remove the container:

```console
$ docker container rm -fv devtest
```

### Mount into a non-empty directory on the container

If you bind-mount a directory into a non-empty directory on the container, the
directory's existing contents are obscured by the bind mount. This can be
beneficial, such as when you want to test a new version of your application
without building a new image. However, it can also be surprising and this
behavior differs from that of [volumes](https://docs.docker.com/engine/storage/volumes/).

This example is contrived to be extreme, but replaces the contents of the
container's `/usr/` directory with the `/tmp/` directory on the host machine. In
most cases, this would result in a non-functioning container.

The `--mount` and `-v` examples have the same end result.

```console
$ docker run -d \
  -it \
  --name broken-container \
  --mount type=bind,source=/tmp,target=/usr \
  nginx:latest

docker: Error response from daemon: oci runtime error: container_linux.go:262:
starting container process caused "exec: \"nginx\": executable file not found in $PATH".
```

```console
$ docker run -d \
  -it \
  --name broken-container \
  -v /tmp:/usr \
  nginx:latest

docker: Error response from daemon: oci runtime error: container_linux.go:262:
starting container process caused "exec: \"nginx\": executable file not found in $PATH".
```

The container is created but does not start. Remove it:

```console
$ docker container rm broken-container
```

## Use a read-only bind mount

For some development applications, the container needs to
write into the bind mount, so changes are propagated back to the
Docker host. At other times, the container only needs read access.

This example modifies the previous one, but mounts the directory as a read-only
bind mount, by adding `ro` to the (empty by default) list of options, after the
mount point within the container. Where multiple options are present, separate
them by commas.

The `--mount` and `-v` examples have the same result.

```console
$ docker run -d \
  -it \
  --name devtest \
  --mount type=bind,source="$(pwd)"/target,target=/app,readonly \
  nginx:latest
```

```console
$ docker run -d \
  -it \
  --name devtest \
  -v "$(pwd)"/target:/app:ro \
  nginx:latest
```

Use `docker inspect devtest` to verify that the bind mount was created
correctly. Look for the `Mounts` section:

```json
"Mounts": [
    {
        "Type": "bind",
        "Source": "/tmp/source/target",
        "Destination": "/app",
        "Mode": "ro",
        "RW": false,
        "Propagation": "rprivate"
    }
],
```

Stop and remove the container:

```console
$ docker container rm -fv devtest
```

## Recursive mounts

When you bind mount a path that itself contains mounts, those submounts are
also included in the bind mount by default. This behavior is configurable,
using the `bind-recursive` option for `--mount`. This option is only supported
with the `--mount` flag, not with `-v` or `--volume`.

If the bind mount is read-only, the Docker Engine makes a best-effort attempt
at making the submounts read-only as well. This is referred to as recursive
read-only mounts. Recursive read-only mounts require Linux kernel version 5.12
or later. If you're running an older kernel version, submounts are
automatically mounted as read-write by default. Attempting to set submounts to
be read-only on a kernel version earlier than 5.12, using the
`bind-recursive=readonly` option, results in an error.

Supported values for the `bind-recursive` option are:

| Value | Description |
| --- | --- |
| enabled(default) | Read-only mounts are made recursively read-only if kernel is v5.12 or later. Otherwise, submounts are read-write. |
| disabled | Submounts are ignored (not included in the bind mount). |
| writable | Submounts are read-write. |
| readonly | Submounts are read-only. Requires kernel v5.12 or later. |

## Configure bind propagation

Bind propagation defaults to `rprivate` for both bind mounts and volumes. It is
only configurable for bind mounts, and only on Linux host machines. Bind
propagation is an advanced topic and many users never need to configure it.

Bind propagation refers to whether or not mounts created within a given
bind-mount can be propagated to replicas of that mount. Consider
a mount point `/mnt`, which is also mounted on `/tmp`. The propagation settings
control whether a mount on `/tmp/a` would also be available on `/mnt/a`. Each
propagation setting has a recursive counterpoint. In the case of recursion,
consider that `/tmp/a` is also mounted as `/foo`. The propagation settings
control whether `/mnt/a` and/or `/tmp/a` would exist.

> Note
>
> Mount propagation doesn't work with Docker Desktop.

| Propagation setting | Description |
| --- | --- |
| shared | Sub-mounts of the original mount are exposed to replica mounts, and sub-mounts of replica mounts are also propagated to the original mount. |
| slave | similar to a shared mount, but only in one direction. If the original mount exposes a sub-mount, the replica mount can see it. However, if the replica mount exposes a sub-mount, the original mount cannot see it. |
| private | The mount is private. Sub-mounts within it are not exposed to replica mounts, and sub-mounts of replica mounts are not exposed to the original mount. |
| rshared | The same as shared, but the propagation also extends to and from mount points nested within any of the original or replica mount points. |
| rslave | The same as slave, but the propagation also extends to and from mount points nested within any of the original or replica mount points. |
| rprivate | The default. The same as private, meaning that no mount points anywhere within the original or replica mount points propagate in either direction. |

Before you can set bind propagation on a mount point, the host filesystem needs
to already support bind propagation.

For more information about bind propagation, see the
[Linux kernel documentation for shared subtree](https://www.kernel.org/doc/Documentation/filesystems/sharedsubtree.txt).

The following example mounts the `target/` directory into the container twice,
and the second mount sets both the `ro` option and the `rslave` bind propagation
option.

The `--mount` and `-v` examples have the same result.

```console
$ docker run -d \
  -it \
  --name devtest \
  --mount type=bind,source="$(pwd)"/target,target=/app \
  --mount type=bind,source="$(pwd)"/target,target=/app2,readonly,bind-propagation=rslave \
  nginx:latest
```

```console
$ docker run -d \
  -it \
  --name devtest \
  -v "$(pwd)"/target:/app \
  -v "$(pwd)"/target:/app2:ro,rslave \
  nginx:latest
```

Now if you create `/app/foo/`, `/app2/foo/` also exists.

## Configure the SELinux label

If you use SELinux, you can add the `z` or `Z` options to modify the SELinux
label of the host file or directory being mounted into the container. This
affects the file or directory on the host machine itself and can have
consequences outside of the scope of Docker.

- The `z` option indicates that the bind mount content is shared among multiple
  containers.
- The `Z` option indicates that the bind mount content is private and unshared.

Use extreme caution with these options. Bind-mounting a system directory
such as `/home` or `/usr` with the `Z` option renders your host machine
inoperable and you may need to relabel the host machine files by hand.

> Important
>
> When using bind mounts with services, SELinux labels
> (`:Z` and `:z`), as well as `:ro` are ignored. See
> [moby/moby #32579](https://github.com/moby/moby/issues/32579) for details.

This example sets the `z` option to specify that multiple containers can share
the bind mount's contents:

It is not possible to modify the SELinux label using the `--mount` flag.

```console
$ docker run -d \
  -it \
  --name devtest \
  -v "$(pwd)"/target:/app:z \
  nginx:latest
```

## Use a bind mount with Docker Compose

A single Docker Compose service with a bind mount looks like this:

```yaml
services:
  frontend:
    image: node:lts
    volumes:
      - type: bind
        source: ./static
        target: /opt/app/static
volumes:
  myapp:
```

For more information about using volumes of the `bind` type with Compose, see
[Compose reference on the volumes top-level element](https://docs.docker.com/reference/compose-file/volumes/).
and
[Compose reference on the volume attribute](https://docs.docker.com/reference/compose-file/services/#volumes).

## Next steps

- Learn about [volumes](https://docs.docker.com/engine/storage/volumes/).
- Learn about [tmpfs mounts](https://docs.docker.com/engine/storage/tmpfs/).
- Learn about
  [storage drivers](https://docs.docker.com/engine/storage/drivers/).

---

# containerd image store with Docker Engine

> Learn about the containerd image store

# containerd image store with Docker Engine

   Table of contents

---

The containerd image store is the default storage backend for Docker Engine
29.0 and later on fresh installations. If you upgraded from an earlier version,
your daemon continues using the legacy graph drivers (overlay2) until you
enable the containerd image store.

containerd, the industry-standard container runtime, uses snapshotters instead
of classic storage drivers for storing image and container data.

> Note
>
> The containerd image store is not available when using user namespace
> remapping (`userns-remap`). See
> [moby#47377](https://github.com/moby/moby/issues/47377) for details.

## Why use the containerd image store

The containerd image store uses snapshotters to manage how image layers are
stored and accessed on the filesystem. This differs from the classic graph
drivers like overlay2.

The containerd image store enables:

- Building and storing multi-platform images locally. With classic storage
  drivers, you need external builders for multi-platform images.
- Working with images that include attestations (provenance, SBOM). These use
  image indices that the classic store doesn't support.
- Running Wasm containers. The containerd image store supports WebAssembly
  workloads.
- Using advanced snapshotters. containerd supports pluggable snapshotters that
  provide features like lazy-pulling of images (stargz) or peer-to-peer image
  distribution (nydus, dragonfly).

For most users, switching to the containerd image store is transparent. The
storage backend changes, but your workflows remain the same.

## Disk space usage

The containerd image store uses more disk space than the legacy storage
drivers for the same images. This is because containerd stores images in both
compressed and uncompressed formats, while the legacy drivers stored only the
uncompressed layers.

When you pull an image, containerd keeps the compressed layers (as received
from the registry) and also extracts them to disk. This dual storage means
each layer occupies more space. The compressed format enables faster pulls and
pushes, but requires additional disk capacity.

This difference is particularly noticeable with multiple images sharing the
same base layers. With legacy storage drivers, shared base layers were stored
once locally, and reused images that depended on them. With containerd, each
image stores its own compressed version of shared layers, even though the
uncompressed layers are still de-duplicated through snapshotters. The
compressed storage adds overhead proportional to the number of images using
those layers.

If disk space is constrained, consider the following:

- Regularly prune unused images with `docker image prune`
- Use `docker system df` to monitor disk usage
- [Configure the data directory](https://docs.docker.com/engine/daemon/#configure-the-data-directory-location)
  to use a partition with adequate space

## Enable containerd image store on Docker Engine

If you're upgrading from an earlier Docker Engine version, you need to manually
enable the containerd image store.

> Important
>
> Switching storage backends temporarily hides images and containers created
> with the other backend. Your data remains on disk. To access the old images
> again, switch back to your previous storage configuration.

Add the following configuration to your `/etc/docker/daemon.json` file:

```json
{
  "features": {
    "containerd-snapshotter": true
  }
}
```

Save the file and restart the daemon:

```console
$ sudo systemctl restart docker
```

After restarting the daemon, verify you're using the containerd image store:

```console
$ docker info -f '{{ .DriverStatus }}'
[[driver-type io.containerd.snapshotter.v1]]
```

Docker Engine uses the `overlayfs` containerd snapshotter by default.

> Note
>
> When you enable the containerd image store, existing images and containers
> from the overlay2 driver remain on disk but become hidden. They reappear if
> you switch back to overlay2. To use your existing images with the containerd
> image store, push them to a registry first, or use `docker save` to export
> them.

## Experimental automatic migration

Docker Engine includes an experimental feature that can automatically switch to
the containerd image store under certain conditions. **This feature is
experimental**. It's provided for those who want to test it, but [starting
fresh](#enable-containerd-image-store-on-docker-engine) is the recommended
approach.

> Caution
>
> The automatic migration feature is experimental and may not work reliably in
> all scenarios. Create backups before attempting to use it.

To enable automatic migration, add the `containerd-migration` feature to your
`/etc/docker/daemon.json`:

```json
{
  "features": {
    "containerd-migration": true
  }
}
```

You can also set the `DOCKER_MIGRATE_SNAPSHOTTER_THRESHOLD` environment
variable to make the daemon switch automatically if you have no containers and
your image count is at or below the threshold. For systemd:

```console
$ sudo systemctl edit docker.service
```

Add:

```ini
[Service]
Environment="DOCKER_MIGRATE_SNAPSHOTTER_THRESHOLD=5"
```

If you have no running or stopped containers and 5 or fewer images, the daemon
switches to the containerd image store on restart. Your overlay2 data remains
on disk but becomes hidden.

## Additional resources

To learn more about the containerd image store and its capabilities in Docker
Desktop, see
[containerd image store on Docker Desktop](https://docs.docker.com/desktop/features/containerd/).

---

# BTRFS storage driver

> Learn how to optimize your use of Btrfs driver.

# BTRFS storage driver

   Table of contents

---

> Important
>
> In most cases you should use the `overlay2` storage driver - it's not
> required to use the `btrfs` storage driver simply because your system uses
> Btrfs as its root filesystem.
>
>
>
> Btrfs driver has known issues. See [Moby issue #27653](https://github.com/moby/moby/issues/27653)
> for more information.

Btrfs is a copy-on-write filesystem that supports many advanced storage
technologies, making it a good fit for Docker. Btrfs is included in the
mainline Linux kernel.

Docker's `btrfs` storage driver leverages many Btrfs features for image and
container management. Among these features are block-level operations, thin
provisioning, copy-on-write snapshots, and ease of administration. You can
combine multiple physical block devices into a single Btrfs filesystem.

This page refers to Docker's Btrfs storage driver as `btrfs` and the overall
Btrfs Filesystem as Btrfs.

> Note
>
> The `btrfs` storage driver is only supported with Docker Engine CE on SLES,
> Ubuntu, and Debian systems.

## Prerequisites

`btrfs` is supported if you meet the following prerequisites:

- `btrfs` is only recommended with Docker CE on Ubuntu or Debian systems.
- Changing the storage driver makes any containers you have already
  created inaccessible on the local system. Use `docker save` to save containers,
  and push existing images to Docker Hub or a private repository, so that you
  do not need to re-create them later.
- `btrfs` requires a dedicated block storage device such as a physical disk. This
  block device must be formatted for Btrfs and mounted into `/var/lib/docker/`.
  The configuration instructions below walk you through this procedure. By
  default, the SLES `/` filesystem is formatted with Btrfs, so for SLES, you do
  not need to use a separate block device, but you can choose to do so for
  performance reasons.
- `btrfs` support must exist in your kernel. To check this, run the following
  command:
  ```console
  $ grep btrfs /proc/filesystems
  btrfs
  ```
- To manage Btrfs filesystems at the level of the operating system, you need the
  `btrfs` command. If you don't have this command, install the `btrfsprogs`
  package (SLES) or `btrfs-tools` package (Ubuntu).

## Configure Docker to use the btrfs storage driver

This procedure is essentially identical on SLES and Ubuntu.

1. Stop Docker.
2. Copy the contents of `/var/lib/docker/` to a backup location, then empty
  the contents of `/var/lib/docker/`:
  ```console
  $ sudo cp -au /var/lib/docker /var/lib/docker.bk
  $ sudo rm -rf /var/lib/docker/*
  ```
3. Format your dedicated block device or devices as a Btrfs filesystem. This
  example assumes that you are using two block devices called `/dev/xvdf` and
  `/dev/xvdg`. Double-check the block device names because this is a
  destructive operation.
  ```console
  $ sudo mkfs.btrfs -f /dev/xvdf /dev/xvdg
  ```
  There are many more options for Btrfs, including striping and RAID. See the
  [Btrfs documentation](https://btrfs.wiki.kernel.org/index.php/Using_Btrfs_with_Multiple_Devices).
4. Mount the new Btrfs filesystem on the `/var/lib/docker/` mount point. You
  can specify any of the block devices used to create the Btrfs filesystem.
  ```console
  $ sudo mount -t btrfs /dev/xvdf /var/lib/docker
  ```
  > Note
  >
  > Make the change permanent across reboots by adding an entry to
  > `/etc/fstab`.
5. Copy the contents of `/var/lib/docker.bk` to `/var/lib/docker/`.
  ```console
  $ sudo cp -au /var/lib/docker.bk/* /var/lib/docker/
  ```
6. Configure Docker to use the `btrfs` storage driver. This is required even
  though `/var/lib/docker/` is now using a Btrfs filesystem.
  Edit or create the file `/etc/docker/daemon.json`. If it is a new file, add
  the following contents. If it is an existing file, add the key and value
  only, being careful to end the line with a comma if it isn't the final
  line before an ending curly bracket (`}`).
  ```json
  {
    "storage-driver": "btrfs"
  }
  ```
  See all storage options for each storage driver in the
  [daemon reference documentation](https://docs.docker.com/reference/cli/dockerd/#options-per-storage-driver)
7. Start Docker. When it's running, verify that `btrfs` is being used as the
  storage driver.
  ```console
  $ docker info
  Containers: 0
   Running: 0
   Paused: 0
   Stopped: 0
  Images: 0
  Server Version: 17.03.1-ce
  Storage Driver: btrfs
   Build Version: Btrfs v4.4
   Library Version: 101
  <...>
  ```
8. When you are ready, remove the `/var/lib/docker.bk` directory.

## Manage a Btrfs volume

One of the benefits of Btrfs is the ease of managing Btrfs filesystems without
the need to unmount the filesystem or restart Docker.

When space gets low, Btrfs automatically expands the volume in chunks of
roughly 1 GB.

To add a block device to a Btrfs volume, use the `btrfs device add` and
`btrfs filesystem balance` commands.

```console
$ sudo btrfs device add /dev/svdh /var/lib/docker

$ sudo btrfs filesystem balance /var/lib/docker
```

> Note
>
> While you can do these operations with Docker running, performance suffers.
> It might be best to plan an outage window to balance the Btrfs filesystem.

## How thebtrfsstorage driver works

The `btrfs` storage driver works differently from other
storage drivers in that your entire `/var/lib/docker/` directory is stored on a
Btrfs volume.

### Image and container layers on-disk

Information about image layers and writable container layers is stored in
`/var/lib/docker/btrfs/subvolumes/`. This subdirectory contains one directory
per image or container layer, with the unified filesystem built from a layer
plus all its parent layers. Subvolumes are natively copy-on-write and have space
allocated to them on-demand from an underlying storage pool. They can also be
nested and snapshotted. The diagram below shows 4 subvolumes. 'Subvolume 2' and
'Subvolume 3' are nested, whereas 'Subvolume 4' shows its own internal directory
tree.

![Subvolume example](https://docs.docker.com/engine/storage/drivers/images/btfs_subvolume.webp)  ![Subvolume example](https://docs.docker.com/engine/storage/drivers/images/btfs_subvolume.webp)

Only the base layer of an image is stored as a true subvolume. All the other
layers are stored as snapshots, which only contain the differences introduced
in that layer. You can create snapshots of snapshots as shown in the diagram
below.

![Snapshots diagram](https://docs.docker.com/engine/storage/drivers/images/btfs_snapshots.webp)  ![Snapshots diagram](https://docs.docker.com/engine/storage/drivers/images/btfs_snapshots.webp)

On disk, snapshots look and feel just like subvolumes, but in reality they are
much smaller and more space-efficient. Copy-on-write is used to maximize storage
efficiency and minimize layer size, and writes in the container's writable layer
are managed at the block level. The following image shows a subvolume and its
snapshot sharing data.

![Snapshot and subvolume sharing data](https://docs.docker.com/engine/storage/drivers/images/btfs_pool.webp)  ![Snapshot and subvolume sharing data](https://docs.docker.com/engine/storage/drivers/images/btfs_pool.webp)

For maximum efficiency, when a container needs more space, it is allocated in
chunks of roughly 1 GB in size.

Docker's `btrfs` storage driver stores every image layer and container in its
own Btrfs subvolume or snapshot. The base layer of an image is stored as a
subvolume whereas child image layers and containers are stored as snapshots.
This is shown in the diagram below.

![Btrfs container layers](https://docs.docker.com/engine/storage/drivers/images/btfs_container_layer.webp)  ![Btrfs container layers](https://docs.docker.com/engine/storage/drivers/images/btfs_container_layer.webp)

The high level process for creating images and containers on Docker hosts
running the `btrfs` driver is as follows:

1. The image's base layer is stored in a Btrfs *subvolume* under
  `/var/lib/docker/btrfs/subvolumes`.
2. Subsequent image layers are stored as a Btrfs *snapshot* of the parent
  layer's subvolume or snapshot, but with the changes introduced by this
  layer. These differences are stored at the block level.
3. The container's writable layer is a Btrfs snapshot of the final image layer,
  with the differences introduced by the running container. These differences
  are stored at the block level.

## How container reads and writes work withbtrfs

### Reading files

A container is a space-efficient snapshot of an image. Metadata in the snapshot
points to the actual data blocks in the storage pool. This is the same as with
a subvolume. Therefore, reads performed against a snapshot are essentially the
same as reads performed against a subvolume.

### Writing files

As a general caution, writing and updating a large number of small files with
Btrfs can result in slow performance.

Consider three scenarios where a container opens a file for write access with
Btrfs.

#### Writing new files

Writing a new file to a container invokes an allocate-on-demand operation to
allocate new data block to the container's snapshot. The file is then written
to this new space. The allocate-on-demand operation is native to all writes
with Btrfs and is the same as writing new data to a subvolume. As a result,
writing new files to a container's snapshot operates at native Btrfs speeds.

#### Modifying existing files

Updating an existing file in a container is a copy-on-write operation
(redirect-on-write is the Btrfs terminology). The original data is read from
the layer where the file currently exists, and only the modified blocks are
written into the container's writable layer. Next, the Btrfs driver updates the
filesystem metadata in the snapshot to point to this new data. This behavior
incurs minor overhead.

#### Deleting files or directories

If a container deletes a file or directory that exists in a lower layer, Btrfs
masks the existence of the file or directory in the lower layer. If a container
creates a file and then deletes it, this operation is performed in the Btrfs
filesystem itself and the space is reclaimed.

## Btrfs and Docker performance

There are several factors that influence Docker's performance under the `btrfs`
storage driver.

> Note
>
> Many of these factors are mitigated by using Docker volumes for write-heavy
> workloads, rather than relying on storing data in the container's writable
> layer. However, in the case of Btrfs, Docker volumes still suffer from these
> draw-backs unless `/var/lib/docker/volumes/` isn't backed by Btrfs.

### Page caching

Btrfs doesn't support page cache sharing. This means that each process
accessing the same file copies the file into the Docker host's memory. As a
result, the `btrfs` driver may not be the best choice for high-density use cases
such as PaaS.

### Small writes

Containers performing lots of small writes (this usage pattern matches what
happens when you start and stop many containers in a short period of time, as
well) can lead to poor use of Btrfs chunks. This can prematurely fill the Btrfs
filesystem and lead to out-of-space conditions on your Docker host. Use `btrfs filesys show` to closely monitor the amount of free space on your Btrfs device.

### Sequential writes

Btrfs uses a journaling technique when writing to disk. This can impact the
performance of sequential writes, reducing performance by up to 50%.

### Fragmentation

Fragmentation is a natural byproduct of copy-on-write filesystems like Btrfs.
Many small random writes can compound this issue. Fragmentation can manifest as
CPU spikes when using SSDs or head thrashing when using spinning disks. Either
of these issues can harm performance.

If your Linux kernel version is 3.9 or higher, you can enable the `autodefrag`
feature when mounting a Btrfs volume. Test this feature on your own workloads
before deploying it into production, as some tests have shown a negative impact
on performance.

### SSD performance

Btrfs includes native optimizations for SSD media. To enable these features,
mount the Btrfs filesystem with the `-o ssd` mount option. These optimizations
include enhanced SSD write performance by avoiding optimization such as seek
optimizations that don't apply to solid-state media.

### Balance Btrfs filesystems often

Use operating system utilities such as a `cron` job to balance the Btrfs
filesystem regularly, during non-peak hours. This reclaims unallocated blocks
and helps to prevent the filesystem from filling up unnecessarily. You can't
rebalance a totally full Btrfs filesystem unless you add additional physical
block devices to the filesystem.

See the [Btrfs
Wiki](https://btrfs.wiki.kernel.org/index.php/Balance_Filters#Balancing_to_fix_filesystem_full_errors).

### Use fast storage

Solid-state drives (SSDs) provide faster reads and writes than spinning disks.

### Use volumes for write-heavy workloads

Volumes provide the best and most predictable performance for write-heavy
workloads. This is because they bypass the storage driver and don't incur any
of the potential overheads introduced by thin provisioning and copy-on-write.
Volumes have other benefits, such as allowing you to share data among
containers and persisting even when no running container is using them.

## Related Information

- [Volumes](https://docs.docker.com/engine/storage/volumes/)
- [Understand images, containers, and storage drivers](https://docs.docker.com/engine/storage/drivers/)
- [Select a storage driver](https://docs.docker.com/engine/storage/drivers/select-storage-driver/)
