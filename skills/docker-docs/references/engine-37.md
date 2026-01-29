# OverlayFS storage driver and more

# OverlayFS storage driver

> Learn how to optimize your use of OverlayFS driver.

# OverlayFS storage driver

   Table of contents

---

OverlayFS is a union filesystem.

This page refers to the Linux kernel driver as `OverlayFS` and to the Docker
storage driver as `overlay2`.

> Note
>
> Docker Engine 29.0 and later uses the
> [containerd image store](https://docs.docker.com/engine/storage/containerd/) by default.
> The `overlay2` driver is a legacy storage driver that is superseded by the
> `overlayfs` containerd snapshotter. For more information, see
> [Select a storage driver](https://docs.docker.com/engine/storage/drivers/select-storage-driver/).

> Note
>
> For `fuse-overlayfs` driver, check
> [Rootless mode documentation](https://docs.docker.com/engine/security/rootless/).

## Prerequisites

The `overlay2` driver is supported if you meet the following prerequisites:

- Version 4.0 or higher of the Linux kernel, or RHEL or CentOS using
  version 3.10.0-514 of the kernel or higher.
- The `overlay2` driver is supported on `xfs` backing filesystems,
  but only with `d_type=true` enabled.
  Use `xfs_info` to verify that the `ftype` option is set to `1`. To format an
  `xfs` filesystem correctly, use the flag `-n ftype=1`.
- Changing the storage driver makes existing containers and images inaccessible
  on the local system. Use `docker save` to save any images you have built or
  push them to Docker Hub or a private registry before changing the storage driver,
  so that you don't need to re-create them later.

## Configure Docker with theoverlay2storage driver

Before following this procedure, you must first meet all the
[prerequisites](#prerequisites).

The following steps outline how to configure the `overlay2` storage driver.

1. Stop Docker.
  ```console
  $ sudo systemctl stop docker
  ```
2. Copy the contents of `/var/lib/docker` to a temporary location.
  ```console
  $ cp -au /var/lib/docker /var/lib/docker.bk
  ```
3. If you want to use a separate backing filesystem from the one used by
  `/var/lib/`, format the filesystem and mount it into `/var/lib/docker`.
  Make sure to add this mount to `/etc/fstab` to make it permanent.
4. Edit `/etc/docker/daemon.json`. If it doesn't yet exist, create it. Assuming
  that the file was empty, add the following contents.
  ```json
  {
    "storage-driver": "overlay2"
  }
  ```
  Docker doesn't start if the `daemon.json` file contains invalid JSON.
5. Start Docker.
  ```console
  $ sudo systemctl start docker
  ```
6. Verify that the daemon is using the `overlay2` storage driver.
  Use the `docker info` command and look for `Storage Driver` and
  `Backing filesystem`.
  ```console
  $ docker info
  Containers: 0
  Images: 0
  Storage Driver: overlay2
   Backing Filesystem: xfs
   Supports d_type: true
   Native Overlay Diff: true
  <...>
  ```

Docker is now using the `overlay2` storage driver and has automatically
created the overlay mount with the required `lowerdir`, `upperdir`, `merged`,
and `workdir` constructs.

Continue reading for details about how OverlayFS works within your Docker
containers, as well as performance advice and information about limitations of
its compatibility with different backing filesystems.

## How theoverlay2driver works

OverlayFS layers two directories on a single Linux host and presents them as
a single directory. These directories are called layers, and the unification
process is referred to as a union mount. OverlayFS refers to the lower directory
as `lowerdir` and the upper directory as `upperdir`. The unified view is exposed
through its own directory called `merged`.

The `overlay2` driver natively supports up to 128 lower OverlayFS layers. This
capability provides better performance for layer-related Docker commands such
as `docker build` and `docker commit`, and consumes fewer inodes on the backing
filesystem.

### Image and container layers on-disk

After downloading a five-layer image using `docker pull ubuntu`, you can see
six directories under `/var/lib/docker/overlay2`.

> Warning
>
> Don't directly manipulate any files or directories within
> `/var/lib/docker/`. These files and directories are managed by Docker.

```console
$ ls -l /var/lib/docker/overlay2

total 24
drwx------ 5 root root 4096 Jun 20 07:36 223c2864175491657d238e2664251df13b63adb8d050924fd1bfcdb278b866f7
drwx------ 3 root root 4096 Jun 20 07:36 3a36935c9df35472229c57f4a27105a136f5e4dbef0f87905b2e506e494e348b
drwx------ 5 root root 4096 Jun 20 07:36 4e9fa83caff3e8f4cc83693fa407a4a9fac9573deaf481506c102d484dd1e6a1
drwx------ 5 root root 4096 Jun 20 07:36 e8876a226237217ec61c4baf238a32992291d059fdac95ed6303bdff3f59cff5
drwx------ 5 root root 4096 Jun 20 07:36 eca1e4e1694283e001f200a667bb3cb40853cf2d1b12c29feda7422fed78afed
drwx------ 2 root root 4096 Jun 20 07:36 l
```

The new `l` (lowercase `L`) directory contains shortened layer identifiers as
symbolic links. These identifiers are used to avoid hitting the page size
limitation on arguments to the `mount` command.

```console
$ ls -l /var/lib/docker/overlay2/l

total 20
lrwxrwxrwx 1 root root 72 Jun 20 07:36 6Y5IM2XC7TSNIJZZFLJCS6I4I4 -> ../3a36935c9df35472229c57f4a27105a136f5e4dbef0f87905b2e506e494e348b/diff
lrwxrwxrwx 1 root root 72 Jun 20 07:36 B3WWEFKBG3PLLV737KZFIASSW7 -> ../4e9fa83caff3e8f4cc83693fa407a4a9fac9573deaf481506c102d484dd1e6a1/diff
lrwxrwxrwx 1 root root 72 Jun 20 07:36 JEYMODZYFCZFYSDABYXD5MF6YO -> ../eca1e4e1694283e001f200a667bb3cb40853cf2d1b12c29feda7422fed78afed/diff
lrwxrwxrwx 1 root root 72 Jun 20 07:36 NFYKDW6APBCCUCTOUSYDH4DXAT -> ../223c2864175491657d238e2664251df13b63adb8d050924fd1bfcdb278b866f7/diff
lrwxrwxrwx 1 root root 72 Jun 20 07:36 UL2MW33MSE3Q5VYIKBRN4ZAGQP -> ../e8876a226237217ec61c4baf238a32992291d059fdac95ed6303bdff3f59cff5/diff
```

The lowest layer contains a file called `link`, which contains the name of the
shortened identifier, and a directory called `diff` which contains the
layer's contents.

```console
$ ls /var/lib/docker/overlay2/3a36935c9df35472229c57f4a27105a136f5e4dbef0f87905b2e506e494e348b/

diff  link

$ cat /var/lib/docker/overlay2/3a36935c9df35472229c57f4a27105a136f5e4dbef0f87905b2e506e494e348b/link

6Y5IM2XC7TSNIJZZFLJCS6I4I4

$ ls  /var/lib/docker/overlay2/3a36935c9df35472229c57f4a27105a136f5e4dbef0f87905b2e506e494e348b/diff

bin  boot  dev  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
```

The second-lowest layer, and each higher layer, contain a file called `lower`,
which denotes its parent, and a directory called `diff` which contains its
contents. It also contains a `merged` directory, which contains the unified
contents of its parent layer and itself, and a `work` directory which is used
internally by OverlayFS.

```console
$ ls /var/lib/docker/overlay2/223c2864175491657d238e2664251df13b63adb8d050924fd1bfcdb278b866f7

diff  link  lower  merged  work

$ cat /var/lib/docker/overlay2/223c2864175491657d238e2664251df13b63adb8d050924fd1bfcdb278b866f7/lower

l/6Y5IM2XC7TSNIJZZFLJCS6I4I4

$ ls /var/lib/docker/overlay2/223c2864175491657d238e2664251df13b63adb8d050924fd1bfcdb278b866f7/diff/

etc  sbin  usr  var
```

To view the mounts which exist when you use the `overlay` storage driver with
Docker, use the `mount` command. The output below is truncated for readability.

```console
$ mount | grep overlay

overlay on /var/lib/docker/overlay2/9186877cdf386d0a3b016149cf30c208f326dca307529e646afce5b3f83f5304/merged
type overlay (rw,relatime,
lowerdir=l/DJA75GUWHWG7EWICFYX54FIOVT:l/B3WWEFKBG3PLLV737KZFIASSW7:l/JEYMODZYFCZFYSDABYXD5MF6YO:l/UL2MW33MSE3Q5VYIKBRN4ZAGQP:l/NFYKDW6APBCCUCTOUSYDH4DXAT:l/6Y5IM2XC7TSNIJZZFLJCS6I4I4,
upperdir=9186877cdf386d0a3b016149cf30c208f326dca307529e646afce5b3f83f5304/diff,
workdir=9186877cdf386d0a3b016149cf30c208f326dca307529e646afce5b3f83f5304/work)
```

The `rw` on the second line shows that the `overlay` mount is read-write.

The following diagram shows how a Docker image and a Docker container are
layered. The image layer is the `lowerdir` and the container layer is the
`upperdir`. If the image has multiple layers, multiple `lowerdir` directories
are used. The unified view is exposed through a directory called `merged` which
is effectively the containers mount point.

![How Docker constructs map to OverlayFS constructs](https://docs.docker.com/engine/storage/drivers/images/overlay_constructs.webp)  ![How Docker constructs map to OverlayFS constructs](https://docs.docker.com/engine/storage/drivers/images/overlay_constructs.webp)

Where the image layer and the container layer contain the same files, the
container layer (`upperdir`) takes precedence and obscures the existence of the
same files in the image layer.

To create a container, the `overlay2` driver combines the directory representing
the image's top layer plus a new directory for the container. The image's
layers are the `lowerdirs` in the overlay and are read-only. The new directory for
the container is the `upperdir` and is writable.

### Image and container layers on-disk

The following `docker pull` command shows a Docker host downloading a Docker
image comprising five layers.

```console
$ docker pull ubuntu

Using default tag: latest
latest: Pulling from library/ubuntu

5ba4f30e5bea: Pull complete
9d7d19c9dc56: Pull complete
ac6ad7efd0f9: Pull complete
e7491a747824: Pull complete
a3ed95caeb02: Pull complete
Digest: sha256:46fb5d001b88ad904c5c732b086b596b92cfb4a4840a3abd0e35dbb6870585e4
Status: Downloaded newer image for ubuntu:latest
```

#### The image layers

Each image layer has its own directory within `/var/lib/docker/overlay/`, which
contains its contents, as shown in the following example. The image layer IDs
don't correspond to the directory IDs.

> Warning
>
> Don't directly manipulate any files or directories within
> `/var/lib/docker/`. These files and directories are managed by Docker.

```console
$ ls -l /var/lib/docker/overlay/

total 20
drwx------ 3 root root 4096 Jun 20 16:11 38f3ed2eac129654acef11c32670b534670c3a06e483fce313d72e3e0a15baa8
drwx------ 3 root root 4096 Jun 20 16:11 55f1e14c361b90570df46371b20ce6d480c434981cbda5fd68c6ff61aa0a5358
drwx------ 3 root root 4096 Jun 20 16:11 824c8a961a4f5e8fe4f4243dab57c5be798e7fd195f6d88ab06aea92ba931654
drwx------ 3 root root 4096 Jun 20 16:11 ad0fe55125ebf599da124da175174a4b8c1878afe6907bf7c78570341f308461
drwx------ 3 root root 4096 Jun 20 16:11 edab9b5e5bf73f2997524eebeac1de4cf9c8b904fa8ad3ec43b3504196aa3801
```

The image layer directories contain the files unique to that layer as well as
hard links to the data shared with lower layers. This allows for efficient use
of disk space.

```console
$ ls -i /var/lib/docker/overlay2/38f3ed2eac129654acef11c32670b534670c3a06e483fce313d72e3e0a15baa8/root/bin/ls

19793696 /var/lib/docker/overlay2/38f3ed2eac129654acef11c32670b534670c3a06e483fce313d72e3e0a15baa8/root/bin/ls

$ ls -i /var/lib/docker/overlay2/55f1e14c361b90570df46371b20ce6d480c434981cbda5fd68c6ff61aa0a5358/root/bin/ls

19793696 /var/lib/docker/overlay2/55f1e14c361b90570df46371b20ce6d480c434981cbda5fd68c6ff61aa0a5358/root/bin/ls
```

#### The container layer

Containers also exist on-disk in the Docker host's filesystem under
`/var/lib/docker/overlay/`. If you list a running container's subdirectory
using the `ls -l` command, three directories and one file exist:

```console
$ ls -l /var/lib/docker/overlay2/<directory-of-running-container>

total 16
-rw-r--r-- 1 root root   64 Jun 20 16:39 lower-id
drwxr-xr-x 1 root root 4096 Jun 20 16:39 merged
drwxr-xr-x 4 root root 4096 Jun 20 16:39 upper
drwx------ 3 root root 4096 Jun 20 16:39 work
```

The `lower-id` file contains the ID of the top layer of the image the container
is based on, which is the OverlayFS `lowerdir`.

```console
$ cat /var/lib/docker/overlay2/ec444863a55a9f1ca2df72223d459c5d940a721b2288ff86a3f27be28b53be6c/lower-id

55f1e14c361b90570df46371b20ce6d480c434981cbda5fd68c6ff61aa0a5358
```

The `upper` directory contains the contents of the container's read-write layer,
which corresponds to the OverlayFS `upperdir`.

The `merged` directory is the union mount of the `lowerdir` and `upperdirs`, which
comprises the view of the filesystem from within the running container.

The `work` directory is internal to OverlayFS.

To view the mounts which exist when you use the `overlay2` storage driver with
Docker, use the `mount` command. The following output is truncated for
readability.

```console
$ mount | grep overlay

overlay on /var/lib/docker/overlay2/l/ec444863a55a.../merged
type overlay (rw,relatime,lowerdir=/var/lib/docker/overlay2/l/55f1e14c361b.../root,
upperdir=/var/lib/docker/overlay2/l/ec444863a55a.../upper,
workdir=/var/lib/docker/overlay2/l/ec444863a55a.../work)
```

The `rw` on the second line shows that the `overlay` mount is read-write.

## How container reads and writes work withoverlay2

### Reading files

Consider three scenarios where a container opens a file for read access with
overlay.

#### The file does not exist in the container layer

If a container opens a file for read access and the file does not already exist
in the container (`upperdir`) it is read from the image (`lowerdir`). This
incurs very little performance overhead.

#### The file only exists in the container layer

If a container opens a file for read access and the file exists in the
container (`upperdir`) and not in the image (`lowerdir`), it's read directly
from the container.

#### The file exists in both the container layer and the image layer

If a container opens a file for read access and the file exists in the image
layer and the container layer, the file's version in the container layer is
read. Files in the container layer (`upperdir`) obscure files with the same
name in the image layer (`lowerdir`).

### Modifying files or directories

Consider some scenarios where files in a container are modified.

#### Writing to a file for the first time

The first time a container writes to an existing file, that file does not
exist in the container (`upperdir`). The `overlay2` driver performs a
`copy_up` operation to copy the file from the image (`lowerdir`) to the
container (`upperdir`). The container then writes the changes to the new copy
of the file in the container layer.

However, OverlayFS works at the file level rather than the block level. This
means that all OverlayFS `copy_up` operations copy the entire file, even if
the file is large and only a small part of it's being modified. This can have
a noticeable impact on container write performance. However, two things are
worth noting:

- The `copy_up` operation only occurs the first time a given file is written
  to. Subsequent writes to the same file operate against the copy of the file
  already copied up to the container.
- OverlayFS works with multiple layers. This means that performance can be
  impacted when searching for files in images with many layers.

#### Deleting files and directories

- When a *file* is deleted within a container, a *whiteout* file is created in
  the container (`upperdir`). The version of the file in the image layer
  (`lowerdir`) is not deleted (because the `lowerdir` is read-only). However,
  the whiteout file prevents it from being available to the container.
- When a *directory* is deleted within a container, an *opaque directory* is
  created within the container (`upperdir`). This works in the same way as a
  whiteout file and effectively prevents the directory from being accessed,
  even though it still exists in the image (`lowerdir`).

#### Renaming directories

Calling `rename(2)` for a directory is allowed only when both the source and
the destination path are on the top layer. Otherwise, it returns `EXDEV` error
("cross-device link not permitted"). Your application needs to be designed to
handle `EXDEV` and fall back to a "copy and unlink" strategy.

## OverlayFS and Docker Performance

`overlay2` may perform better than `btrfs`. However, be aware of the following details:

### Page caching

OverlayFS supports page cache sharing. Multiple containers accessing the same
file share a single page cache entry for that file. This makes the `overlay2`
drivers efficient with memory and a good option for high-density use cases such
as PaaS.

### Copyup

As with other copy-on-write filesystems, OverlayFS performs copy-up operations
whenever a container writes to a file for the first time. This can add latency
into the write operation, especially for large files. However, once the file
has been copied up, all subsequent writes to that file occur in the upper
layer, without the need for further copy-up operations.

### Performance best practices

The following generic performance best practices apply to OverlayFS.

#### Use fast storage

Solid-state drives (SSDs) provide faster reads and writes than spinning disks.

#### Use volumes for write-heavy workloads

Volumes provide the best and most predictable performance for write-heavy
workloads. This is because they bypass the storage driver and don't incur any
of the potential overheads introduced by thin provisioning and copy-on-write.
Volumes have other benefits, such as allowing you to share data among
containers and persisting your data even if no running container is using them.

## Limitations on OverlayFS compatibility

To summarize the OverlayFS's aspect which is incompatible with other
filesystems:

[open(2)](https://linux.die.net/man/2/open)OverlayFS only implements a subset of the POSIX standards.
This can result in certain OverlayFS operations breaking POSIX standards. One
such operation is the copy-up operation. Suppose that your application calls
`fd1=open("foo", O_RDONLY)` and then `fd2=open("foo", O_RDWR)`. In this case,
your application expects `fd1` and `fd2` to refer to the same file. However, due
to a copy-up operation that occurs after the second calling to `open(2)`, the
descriptors refer to different files. The `fd1` continues to reference the file
in the image (`lowerdir`) and the `fd2` references the file in the container
(`upperdir`). A workaround for this is to `touch` the files which causes the
copy-up operation to happen. All subsequent `open(2)` operations regardless of
read-only or read-write access mode reference the file in the
container (`upperdir`).

`yum` is known to be affected unless the `yum-plugin-ovl` package is installed.
If the `yum-plugin-ovl` package is not available in your distribution such as
RHEL/CentOS prior to 6.8 or 7.2, you may need to run `touch /var/lib/rpm/*`
before running `yum install`. This package implements the `touch` workaround
referenced above for `yum`.

[rename(2)](https://linux.die.net/man/2/rename)OverlayFS does not fully support the `rename(2)` system call. Your
application needs to detect its failure and fall back to a "copy and unlink"
strategy.

---

# Select a storage driver

> Learn how to select the proper storage driver for your container.

# Select a storage driver

   Table of contents

---

Ideally, very little data is written to a container's writable layer, and you
use Docker volumes to write data. However, some workloads require you to be able
to write to the container's writable layer. This is where storage drivers come
in.

> Note
>
> Docker Engine 29.0 and later uses the
> [containerd image store](https://docs.docker.com/engine/storage/containerd/) by default for fresh installations.
> If you upgraded from an earlier version, your daemon continues using the
> classic storage drivers described on this page. You can migrate to the
> containerd image store following the instructions in the
> [containerd image store](https://docs.docker.com/engine/storage/containerd/) documentation.

Docker supports several storage drivers, using a pluggable architecture. The
storage driver controls how images and containers are stored and managed on your
Docker host. After you have read the [storage driver overview](https://docs.docker.com/engine/storage/drivers/), the
next step is to choose the best storage driver for your workloads. Use the storage
driver with the best overall performance and stability in the most usual scenarios.

> Note
>
> This page discusses storage drivers for Docker Engine on Linux. If you're
> running the Docker daemon with Windows as the host OS, the only supported
> storage driver is windowsfilter. For more information, see
> [windowsfilter](https://docs.docker.com/engine/storage/drivers/windowsfilter-driver/).

The Docker Engine provides the following storage backends on Linux:

| Backend | Description |
| --- | --- |
| containerd(snapshotters) | The default for Docker Engine 29.0 and later. Uses containerd snapshotters for image storage. Supports multi-platform images and attestations. Seecontainerd image storefor details. |
| overlay2 | Classic storage driver. Most widely compatible across all currently supported Linux distributions, and requires no extra configuration. |
| fuse-overlayfs | Preferred only for running Rootless Docker on hosts that don't support rootlessoverlay2. Not needed since Linux kernel 5.11, asoverlay2works in rootless mode. Seerootless mode documentationfor details. |
| btrfsandzfs | Allow for advanced options, such as creating snapshots, but require more maintenance and setup. Each relies on the backing filesystem being configured correctly. |
| vfs | Intended for testing purposes, and for situations where no copy-on-write filesystem can be used. Performance is poor, and not generally recommended for production use. |

The Docker Engine has a prioritized list of which storage driver to use if no
storage driver is explicitly configured, assuming that the storage driver meets
the prerequisites, and automatically selects a compatible storage driver. You
can see the order in the [source code for Docker Engine 29.2.0](https://github.com/moby/moby/blob/v29.2.0/daemon/graphdriver/driver_linux.go#L52-L53).

Some storage drivers require you to use a specific format for the backing filesystem.
If you have external requirements to use a specific backing filesystem, this may
limit your choices. See [Supported backing filesystems](#supported-backing-filesystems).

After you have narrowed down which storage drivers you can choose from, your choice
is determined by the characteristics of your workload and the level of stability
you need. See [Other considerations](#other-considerations) for help in making
the final decision.

## Supported storage drivers per Linux distribution

> Note
>
> Modifying the storage driver by editing the daemon configuration file isn't
> supported on Docker Desktop. Docker Desktop uses the
> [containerd image store](https://docs.docker.com/desktop/features/containerd/) by default
> (version 4.34 and later for clean installs). The following table is also not
> applicable for the Docker Engine in rootless mode. For the drivers available
> in rootless mode, see the
> [Rootless mode documentation](https://docs.docker.com/engine/security/rootless/).

This section applies to classic storage drivers only. If you're using the
containerd image store (the default for Docker Engine 29.0+), see the
[containerd image store documentation](https://docs.docker.com/engine/storage/containerd/) instead.

Your operating system and kernel may not support every classic storage driver.
For example, `btrfs` is only supported if your system uses `btrfs` as storage.
In general, the following configurations work on recent versions of the Linux
distribution:

| Linux distribution | Default classic driver | Alternative drivers |
| --- | --- | --- |
| Ubuntu | overlay2 | zfs,vfs |
| Debian | overlay2 | vfs |
| CentOS | overlay2 | zfs,vfs |
| Fedora | overlay2 | zfs,vfs |
| SLES 15 | overlay2 | vfs |
| RHEL | overlay2 | vfs |

For systems using classic storage drivers, `overlay2` provides broad
compatibility across Linux distributions. Use Docker volumes for write-heavy
workloads instead of relying on writing data to the container's writable layer.

The `vfs` storage driver is usually not the best choice, and primarily intended
for debugging purposes in situations where no other storage-driver is supported.
Before using the `vfs` storage driver, be sure to read about
[its performance and storage characteristics and limitations](https://docs.docker.com/engine/storage/drivers/vfs-driver/).

The recommendations in the table above are known to work for a large number of
users. If you use a recommended configuration and find a reproducible issue,
it's likely to be fixed very quickly. If the driver that you want to use is
not recommended according to this table, you can run it at your own risk. You
can and should still report any issues you run into. However, such issues
have a lower priority than issues encountered when using a recommended
configuration.

Depending on your Linux distribution, other storage-drivers, such as `btrfs` may
be available. These storage drivers can have advantages for specific use-cases,
but may require additional set-up or maintenance, which make them not recommended
for common scenarios. Refer to the documentation for those storage drivers for
details.

## Supported backing filesystems

With regard to Docker, the backing filesystem is the filesystem where
`/var/lib/docker/` is located. Some storage drivers only work with specific
backing filesystems.

| Storage driver | Supported backing filesystems |
| --- | --- |
| overlay2 | xfswith ftype=1,ext4,btrfs, (and more) |
| fuse-overlayfs | any filesystem |
| btrfs | btrfs |
| zfs | zfs |
| vfs | any filesystem |

> Note
>
> Most filesystems should work if they have the required features.
> Consult [OverlayFS](https://www.kernel.org/doc/html/latest/filesystems/overlayfs.html)
> for more information.

## Other considerations

### Suitability for your workload

Among other things, each storage driver has its own performance characteristics
that make it more or less suitable for different workloads. Consider the
following generalizations:

- `overlay2` operates at the file level rather than
  the block level. This uses memory more efficiently, but the container's
  writable layer may grow quite large in write-heavy workloads.
- Block-level storage drivers such as `btrfs`, and `zfs` perform
  better for write-heavy workloads (though not as well as Docker volumes).
- `btrfs` and `zfs` require a lot of memory.
- `zfs` is a good choice for high-density workloads such as PaaS.

More information about performance, suitability, and best practices is available
in the documentation for each storage driver.

### Shared storage systems and the storage driver

If you use SAN, NAS, hardware RAID, or other shared storage systems, those
systems may provide high availability, increased performance, thin
provisioning, deduplication, and compression. In many cases, Docker can work on
top of these storage systems, but Docker doesn't closely integrate with them.

Each Docker storage driver is based on a Linux filesystem or volume manager. Be
sure to follow existing best practices for operating your storage driver
(filesystem or volume manager) on top of your shared storage system. For
example, if using the ZFS storage driver on top of a shared storage system, be
sure to follow best practices for operating ZFS filesystems on top of that
specific shared storage system.

### Stability

For some users, stability is more important than performance. Though Docker
considers all of the storage drivers mentioned here to be stable, some are newer
and are still under active development. In general, `overlay2` provides the
highest stability.

### Test with your own workloads

You can test Docker's performance when running your own workloads on different
storage drivers. Make sure to use equivalent hardware and workloads to match
production conditions, so you can see which storage driver offers the best
overall performance.

## Check your current storage driver

The detailed documentation for each individual storage driver details all of the
set-up steps to use a given storage driver.

To see what storage driver Docker is currently using, use `docker info` and look
for the `Storage Driver` line:

```console
$ docker info

Containers: 0
Images: 0
Storage Driver: overlay2
 Backing Filesystem: xfs
<...>
```

To change the storage driver, see the specific instructions for the new storage
driver. Some drivers require additional configuration, including configuration
to physical or logical disks on the Docker host.

> Important
>
> When you change the storage driver, any existing images and containers become
> inaccessible. This is because their layers can't be used by the new storage
> driver. If you revert your changes, you can access the old images and containers
> again, but any that you pulled or created using the new driver are then
> inaccessible.

## Related information

- [Storage drivers](https://docs.docker.com/engine/storage/drivers/)
- [overlay2storage driver](https://docs.docker.com/engine/storage/drivers/overlayfs-driver/)
- [btrfsstorage driver](https://docs.docker.com/engine/storage/drivers/btrfs-driver/)
- [zfsstorage driver](https://docs.docker.com/engine/storage/drivers/zfs-driver/)
- [windowsfilterstorage driver](https://docs.docker.com/engine/storage/drivers/windowsfilter-driver/)

---

# VFS storage driver

> Learn how to optimize your use of VFS driver.

# VFS storage driver

   Table of contents

---

The VFS storage driver isn't a union filesystem. Each layer is a
directory on disk, and there is no copy-on-write support. To create a new
layer, a "deep copy" is done of the previous layer. This leads to lower
performance and more space used on disk than other storage drivers. However, it
is robust, stable, and works in every environment. It can also be used as a
mechanism to verify other storage back-ends against, in a testing environment.

## Configure Docker with thevfsstorage driver

1. Stop Docker.
  ```console
  $ sudo systemctl stop docker
  ```
2. Edit `/etc/docker/daemon.json`. If it doesn't yet exist, create it. Assuming
  that the file was empty, add the following contents.
  ```json
  {
    "storage-driver": "vfs"
  }
  ```
  If you want to set a quota to control the maximum size the VFS storage
  driver can use, set the `size` option on the `storage-opts` key.
  ```json
  {
    "storage-driver": "vfs",
    "storage-opts": ["size=256M"]
  }
  ```
  Docker doesn't start if the `daemon.json` file contains invalid JSON.
3. Start Docker.
  ```console
  $ sudo systemctl start docker
  ```
4. Verify that the daemon is using the `vfs` storage driver.
  Use the `docker info` command and look for `Storage Driver`.
  ```console
  $ docker info
  Storage Driver: vfs
  ...
  ```

Docker is now using the `vfs` storage driver. Docker has automatically
created the `/var/lib/docker/vfs/` directory, which contains all the layers
used by running containers.

## How thevfsstorage driver works

Each image layer and the writable container layer are represented on the Docker
host as subdirectories within `/var/lib/docker/`. The union mount provides the
unified view of all layers. The directory names don't directly correspond to
the IDs of the layers themselves.

VFS doesn't support copy-on-write (COW). Each time a new layer is created,
it's a deep copy of its parent layer. These layers are all located under
`/var/lib/docker/vfs/dir/`.

### Example: Image and container on-disk constructs

The following `docker pull` command shows a Docker host downloading a Docker
image comprising five layers.

```console
$ docker pull ubuntu

Using default tag: latest
latest: Pulling from library/ubuntu
e0a742c2abfd: Pull complete
486cb8339a27: Pull complete
dc6f0d824617: Pull complete
4f7a5649a30e: Pull complete
672363445ad2: Pull complete
Digest: sha256:84c334414e2bfdcae99509a6add166bbb4fa4041dc3fa6af08046a66fed3005f
Status: Downloaded newer image for ubuntu:latest
```

After pulling, each of these layers is represented as a subdirectory of
`/var/lib/docker/vfs/dir/`. The directory names do not correlate with the
image layer IDs shown in the `docker pull` command. To see the size taken up on
disk by each layer, you can use the `du -sh` command, which gives the size as a
human-readable value.

```console
$ ls -l /var/lib/docker/vfs/dir/

total 0
drwxr-xr-x.  2 root root  19 Aug  2 18:19 3262dfbe53dac3e1ab7dcc8ad5d8c4d586a11d2ac3c4234892e34bff7f6b821e
drwxr-xr-x. 21 root root 224 Aug  2 18:23 6af21814449345f55d88c403e66564faad965d6afa84b294ae6e740c9ded2561
drwxr-xr-x. 21 root root 224 Aug  2 18:23 6d3be4585ba32f9f5cbff0110e8d07aea5f5b9fbb1439677c27e7dfee263171c
drwxr-xr-x. 21 root root 224 Aug  2 18:23 9ecd2d88ca177413ab89f987e1507325285a7418fc76d0dcb4bc021447ba2bab
drwxr-xr-x. 21 root root 224 Aug  2 18:23 a292ac6341a65bf3a5da7b7c251e19de1294bd2ec32828de621d41c7ad31f895
drwxr-xr-x. 21 root root 224 Aug  2 18:23 e92be7a4a4e3ccbb7dd87695bca1a0ea373d4f673f455491b1342b33ed91446b
```

```console
$ du -sh /var/lib/docker/vfs/dir/*

4.0K	/var/lib/docker/vfs/dir/3262dfbe53dac3e1ab7dcc8ad5d8c4d586a11d2ac3c4234892e34bff7f6b821e
125M	/var/lib/docker/vfs/dir/6af21814449345f55d88c403e66564faad965d6afa84b294ae6e740c9ded2561
104M	/var/lib/docker/vfs/dir/6d3be4585ba32f9f5cbff0110e8d07aea5f5b9fbb1439677c27e7dfee263171c
125M	/var/lib/docker/vfs/dir/9ecd2d88ca177413ab89f987e1507325285a7418fc76d0dcb4bc021447ba2bab
104M	/var/lib/docker/vfs/dir/a292ac6341a65bf3a5da7b7c251e19de1294bd2ec32828de621d41c7ad31f895
104M	/var/lib/docker/vfs/dir/e92be7a4a4e3ccbb7dd87695bca1a0ea373d4f673f455491b1342b33ed91446b
```

The above output shows that three layers each take 104M and two take 125M.
These directories have only small differences from each other, but they all
consume the same amount of disk space. This is one of the disadvantages of
using the `vfs` storage driver.

## Related information

- [Understand images, containers, and storage drivers](https://docs.docker.com/engine/storage/drivers/)
- [Select a storage driver](https://docs.docker.com/engine/storage/drivers/select-storage-driver/)

---

# windowsfilter storage driver

> Learn about the windowsfilter storage driver

# windowsfilter storage driver

   Table of contents

---

The windowsfilter storage driver is the default storage driver for Docker
Engine on Windows. The windowsfilter driver uses Windows-native file system
layers to for storing Docker layers and volume data on disk. The windowsfilter
storage driver only works on file systems formatted with NTFS.

## Configure the windowsfilter storage driver

For most use case, no configuring the windowsfilter storage driver is not
necessary.

The default storage limit for Docker Engine on Windows is 127GB. To use a
different storage size, set the `size` option for the windowsfilter storage
driver. See
[windowsfilter options](https://docs.docker.com/reference/cli/dockerd/#windowsfilter-options).

Data is stored on the Docker host in `image` and `windowsfilter` subdirectories
within `C:\ProgramData\docker` by default. You can change the storage location
by configuring the `data-root` option in the
[Daemon configuration file](https://docs.docker.com/reference/cli/dockerd/#on-windows):

```json
{
  "data-root": "d:\\docker"
}
```

You must restart the daemon for the configuration change to take effect.

## Additional information

For more information about how container storage works on Windows, refer to
Microsoft's [Containers on Windows documentation](https://learn.microsoft.com/en-us/virtualization/windowscontainers/manage-containers/container-storage).
