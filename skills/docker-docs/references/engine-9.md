# Docker volume plugins and more

# Docker volume plugins

> How to manage data with external volume plugins

# Docker volume plugins

   Table of contents

---

Docker Engine volume plugins enable Engine deployments to be integrated with
external storage systems such as Amazon EBS, and enable data volumes to persist
beyond the lifetime of a single Docker host. See the
[plugin documentation](https://docs.docker.com/engine/extend/legacy_plugins/) for more information.

## Changelog

### 1.13.0

- If used as part of the v2 plugin architecture, mountpoints that are part of
  paths returned by the plugin must be mounted under the directory specified by
  `PropagatedMount` in the plugin configuration
  ([#26398](https://github.com/docker/docker/pull/26398))

### 1.12.0

- Add `Status` field to `VolumeDriver.Get` response
  ([#21006](https://github.com/docker/docker/pull/21006#))
- Add `VolumeDriver.Capabilities` to get capabilities of the volume driver
  ([#22077](https://github.com/docker/docker/pull/22077))

### 1.10.0

- Add `VolumeDriver.Get` which gets the details about the volume
  ([#16534](https://github.com/docker/docker/pull/16534))
- Add `VolumeDriver.List` which lists all volumes owned by the driver
  ([#16534](https://github.com/docker/docker/pull/16534))

### 1.8.0

- Initial support for volume driver plugins
  ([#14659](https://github.com/docker/docker/pull/14659))

## Command-line changes

To give a container access to a volume, use the `--volume` and `--volume-driver`
flags on the `docker container run` command. The `--volume` (or `-v`) flag
accepts a volume name and path on the host, and the `--volume-driver` flag
accepts a driver type.

```console
$ docker volume create --driver=flocker volumename

$ docker container run -it --volume volumename:/data busybox sh
```

### --volume

The `--volume` (or `-v`) flag takes a value that is in the format
`<volume_name>:<mountpoint>`. The two parts of the value are
separated by a colon (`:`) character.

- The volume name is a human-readable name for the volume, and cannot begin with
  a `/` character. It is referred to as `volume_name` in the rest of this topic.
- The `Mountpoint` is the path on the host (v1) or in the plugin (v2) where the
  volume has been made available.

### volumedriver

Specifying a `volumedriver` in conjunction with a `volumename` allows you to
use plugins such as [Flocker](https://github.com/ScatterHQ/flocker) to manage
volumes external to a single host, such as those on EBS.

## Create a VolumeDriver

The container creation endpoint (`/containers/create`) accepts a `VolumeDriver`
field of type `string` allowing to specify the name of the driver. If not
specified, it defaults to `"local"` (the default driver for local volumes).

## Volume plugin protocol

If a plugin registers itself as a `VolumeDriver` when activated, it must
provide the Docker Daemon with writeable paths on the host filesystem. The Docker
daemon provides these paths to containers to consume. The Docker daemon makes
the volumes available by bind-mounting the provided paths into the containers.

> Note
>
> Volume plugins should *not* write data to the `/var/lib/docker/` directory,
> including `/var/lib/docker/volumes`. The `/var/lib/docker/` directory is
> reserved for Docker.

### /VolumeDriver.Create

Request:

```json
{
    "Name": "volume_name",
    "Opts": {}
}
```

Instruct the plugin that the user wants to create a volume, given a user
specified volume name. The plugin does not need to actually manifest the
volume on the filesystem yet (until `Mount` is called).
`Opts` is a map of driver specific options passed through from the user request.

Response:

```json
{
    "Err": ""
}
```

Respond with a string error if an error occurred.

### /VolumeDriver.Remove

Request:

```json
{
    "Name": "volume_name"
}
```

Delete the specified volume from disk. This request is issued when a user
invokes `docker rm -v` to remove volumes associated with a container.

Response:

```json
{
    "Err": ""
}
```

Respond with a string error if an error occurred.

### /VolumeDriver.Mount

Request:

```json
{
    "Name": "volume_name",
    "ID": "b87d7442095999a92b65b3d9691e697b61713829cc0ffd1bb72e4ccd51aa4d6c"
}
```

Docker requires the plugin to provide a volume, given a user specified volume
name. `Mount` is called once per container start. If the same `volume_name` is requested
more than once, the plugin may need to keep track of each new mount request and provision
at the first mount request and deprovision at the last corresponding unmount request.

`ID` is a unique ID for the caller that is requesting the mount.

Response:

- v1
  ```json
  {
      "Mountpoint": "/path/to/directory/on/host",
      "Err": ""
  }
  ```
- v2
  ```json
  {
      "Mountpoint": "/path/under/PropagatedMount",
      "Err": ""
  }
  ```

`Mountpoint` is the path on the host (v1) or in the plugin (v2) where the volume
has been made available.

`Err` is either empty or contains an error string.

### /VolumeDriver.Path

Request:

```json
{
    "Name": "volume_name"
}
```

Request the path to the volume with the given `volume_name`.

Response:

- v1
  ```json
  {
      "Mountpoint": "/path/to/directory/on/host",
      "Err": ""
  }
  ```
- v2
  ```json
  {
      "Mountpoint": "/path/under/PropagatedMount",
      "Err": ""
  }
  ```

Respond with the path on the host (v1) or inside the plugin (v2) where the
volume has been made available, and/or a string error if an error occurred.

`Mountpoint` is optional. However, the plugin may be queried again later if one
is not provided.

### /VolumeDriver.Unmount

Request:

```json
{
    "Name": "volume_name",
    "ID": "b87d7442095999a92b65b3d9691e697b61713829cc0ffd1bb72e4ccd51aa4d6c"
}
```

Docker is no longer using the named volume. `Unmount` is called once per
container stop. Plugin may deduce that it is safe to deprovision the volume at
this point.

`ID` is a unique ID for the caller that is requesting the mount.

Response:

```json
{
    "Err": ""
}
```

Respond with a string error if an error occurred.

### /VolumeDriver.Get

Request:

```json
{
    "Name": "volume_name"
}
```

Get info about `volume_name`.

Response:

- v1
  ```json
  {
    "Volume": {
      "Name": "volume_name",
      "Mountpoint": "/path/to/directory/on/host",
      "Status": {}
    },
    "Err": ""
  }
  ```
- v2
  ```json
  {
    "Volume": {
      "Name": "volume_name",
      "Mountpoint": "/path/under/PropagatedMount",
      "Status": {}
    },
    "Err": ""
  }
  ```

Respond with a string error if an error occurred. `Mountpoint` and `Status` are
optional.

### /VolumeDriver.List

Request:

```json
{}
```

Get the list of volumes registered with the plugin.

Response:

- v1
  ```json
  {
    "Volumes": [
      {
        "Name": "volume_name",
        "Mountpoint": "/path/to/directory/on/host"
      }
    ],
    "Err": ""
  }
  ```
- v2
  ```json
  {
    "Volumes": [
      {
        "Name": "volume_name",
        "Mountpoint": "/path/under/PropagatedMount"
      }
    ],
    "Err": ""
  }
  ```

Respond with a string error if an error occurred. `Mountpoint` is optional.

### /VolumeDriver.Capabilities

Request:

```json
{}
```

Get the list of capabilities the driver supports.

The driver is not required to implement `Capabilities`. If it is not
implemented, the default values are used.

Response:

```json
{
  "Capabilities": {
    "Scope": "global"
  }
}
```

Supported scopes are `global` and `local`. Any other value in `Scope` will be
ignored, and `local` is used. `Scope` allows cluster managers to handle the
volume in different ways. For instance, a scope of `global`, signals to the
cluster manager that it only needs to create the volume once instead of on each
Docker host. More capabilities may be added in the future.

---

# Docker Engine managed plugin system

> Develop and use a plugin with the managed plugin system

# Docker Engine managed plugin system

   Table of contents

---

- [Installing and using a plugin](https://docs.docker.com/engine/extend/#installing-and-using-a-plugin)
- [Developing a plugin](https://docs.docker.com/engine/extend/#developing-a-plugin)
- [Debugging plugins](https://docs.docker.com/engine/extend/#debugging-plugins)

Docker Engine's plugin system lets you install, start, stop, and remove
plugins using Docker Engine.

For information about legacy (non-managed) plugins, refer to
[Understand legacy Docker Engine plugins](https://docs.docker.com/engine/extend/legacy_plugins/).

> Note
>
> Docker Engine managed plugins are currently not supported on Windows daemons.

## Installing and using a plugin

Plugins are distributed as Docker images and can be hosted on Docker Hub or on
a private registry.

To install a plugin, use the `docker plugin install` command, which pulls the
plugin from Docker Hub or your private registry, prompts you to grant
permissions or capabilities if necessary, and enables the plugin.

To check the status of installed plugins, use the `docker plugin ls` command.
Plugins that start successfully are listed as enabled in the output.

After a plugin is installed, you can use it as an option for another Docker
operation, such as creating a volume.

In the following example, you install the [rcloneplugin](https://rclone.org/docker/), verify that it is
enabled, and use it to create a volume.

> Note
>
> This example is intended for instructional purposes only.

1. Set up the pre-requisite directories. By default they must exist on the host at the following locations:
  - `/var/lib/docker-plugins/rclone/config`. Reserved for the `rclone.conf` config file and must exist even if it's empty and the config file is not present.
  - `/var/lib/docker-plugins/rclone/cache`. Holds the plugin state file as well as optional VFS caches.
2. Install the `rclone` plugin.
  ```console
  $ docker plugin install rclone/docker-volume-rclone --alias rclone
  Plugin "rclone/docker-volume-rclone" is requesting the following privileges:
   - network: [host]
   - mount: [/var/lib/docker-plugins/rclone/config]
   - mount: [/var/lib/docker-plugins/rclone/cache]
   - device: [/dev/fuse]
   - capabilities: [CAP_SYS_ADMIN]
  Do you grant the above permissions? [y/N]
  ```
  The plugin requests 5 privileges:
  - It needs access to the `host` network.
  - Access to pre-requisite directories to mount to store:
    - Your Rclone config files
    - Temporary cache data
  - Gives access to the FUSE (Filesystem in Userspace) device. This is required because Rclone uses FUSE to mount remote storage as if it were a local filesystem.
  - It needs the `CAP_SYS_ADMIN` capability, which allows the plugin to run
    the `mount` command.
3. Check that the plugin is enabled in the output of `docker plugin ls`.
  ```console
  $ docker plugin ls
  ID                    NAME                      DESCRIPTION                                ENABLED
  aede66158353          rclone:latest             Rclone volume plugin for Docker            true
  ```
4. Create a volume using the plugin.
  This example mounts the `/remote` directory on host `1.2.3.4` into a
  volume named `rclonevolume`.
  This volume can now be mounted into containers.
  ```console
  $ docker volume create \
    -d rclone \
    --name rclonevolume \
    -o type=sftp \
    -o path=remote \
    -o sftp-host=1.2.3.4 \
    -o sftp-user=user \
    -o "sftp-password=$(cat file_containing_password_for_remote_host)"
  ```
5. Verify that the volume was created successfully.
  ```console
  $ docker volume ls
  DRIVER              NAME
  rclone         rclonevolume
  ```
6. Start a container that uses the volume `rclonevolume`.
  ```console
  $ docker run --rm -v rclonevolume:/data busybox ls /data
  <content of /remote on machine 1.2.3.4>
  ```
7. Remove the volume `rclonevolume`
  ```console
  $ docker volume rm rclonevolume
  sshvolume
  ```

To disable a plugin, use the `docker plugin disable` command. To completely
remove it, use the `docker plugin remove` command. For other available
commands and options, see the
[command line reference](https://docs.docker.com/reference/cli/docker/).

## Developing a plugin

#### The rootfs directory

The `rootfs` directory represents the root filesystem of the plugin. In this
example, it was created from a Dockerfile:

> Note
>
> The `/run/docker/plugins` directory is mandatory inside of the
> plugin's filesystem for Docker to communicate with the plugin.

```console
$ git clone https://github.com/vieux/docker-volume-sshfs
$ cd docker-volume-sshfs
$ docker build -t rootfsimage .
$ id=$(docker create rootfsimage true) # id was cd851ce43a403 when the image was created
$ sudo mkdir -p myplugin/rootfs
$ sudo docker export "$id" | sudo tar -x -C myplugin/rootfs
$ docker rm -vf "$id"
$ docker rmi rootfsimage
```

#### The config.json file

The `config.json` file describes the plugin. See the [plugins config reference](https://docs.docker.com/engine/extend/config/).

Consider the following `config.json` file.

```json
{
  "description": "sshFS plugin for Docker",
  "documentation": "https://docs.docker.com/engine/extend/plugins/",
  "entrypoint": ["/docker-volume-sshfs"],
  "network": {
    "type": "host"
  },
  "interface": {
    "types": ["docker.volumedriver/1.0"],
    "socket": "sshfs.sock"
  },
  "linux": {
    "capabilities": ["CAP_SYS_ADMIN"]
  }
}
```

This plugin is a volume driver. It requires a `host` network and the
`CAP_SYS_ADMIN` capability. It depends upon the `/docker-volume-sshfs`
entrypoint and uses the `/run/docker/plugins/sshfs.sock` socket to communicate
with Docker Engine. This plugin has no runtime parameters.

#### Creating the plugin

A new plugin can be created by running
`docker plugin create <plugin-name> ./path/to/plugin/data` where the plugin
data contains a plugin configuration file `config.json` and a root filesystem
in subdirectory `rootfs`.

After that the plugin `<plugin-name>` will show up in `docker plugin ls`.
Plugins can be pushed to remote registries with
`docker plugin push <plugin-name>`.

## Debugging plugins

Stdout of a plugin is redirected to dockerd logs. Such entries have a
`plugin=<ID>` suffix. Here are a few examples of commands for pluginID
`f52a3df433b9aceee436eaada0752f5797aab1de47e5485f1690a073b860ff62` and their
corresponding log entries in the docker daemon logs.

```console
$ docker plugin install tiborvass/sample-volume-plugin

INFO[0036] Starting...       Found 0 volumes on startup  plugin=f52a3df433b9aceee436eaada0752f5797aab1de47e5485f1690a073b860ff62
```

```console
$ docker volume create -d tiborvass/sample-volume-plugin samplevol

INFO[0193] Create Called...  Ensuring directory /data/samplevol exists on host...  plugin=f52a3df433b9aceee436eaada0752f5797aab1de47e5485f1690a073b860ff62
INFO[0193] open /var/lib/docker/plugin-data/local-persist.json: no such file or directory  plugin=f52a3df433b9aceee436eaada0752f5797aab1de47e5485f1690a073b860ff62
INFO[0193]                   Created volume samplevol with mountpoint /data/samplevol  plugin=f52a3df433b9aceee436eaada0752f5797aab1de47e5485f1690a073b860ff62
INFO[0193] Path Called...    Returned path /data/samplevol  plugin=f52a3df433b9aceee436eaada0752f5797aab1de47e5485f1690a073b860ff62
```

```console
$ docker run -v samplevol:/tmp busybox sh

INFO[0421] Get Called...     Found samplevol                plugin=f52a3df433b9aceee436eaada0752f5797aab1de47e5485f1690a073b860ff62
INFO[0421] Mount Called...   Mounted samplevol              plugin=f52a3df433b9aceee436eaada0752f5797aab1de47e5485f1690a073b860ff62
INFO[0421] Path Called...    Returned path /data/samplevol  plugin=f52a3df433b9aceee436eaada0752f5797aab1de47e5485f1690a073b860ff62
INFO[0421] Unmount Called... Unmounted samplevol            plugin=f52a3df433b9aceee436eaada0752f5797aab1de47e5485f1690a073b860ff62
```

#### Using runc to obtain logfiles and shell into the plugin.

Use `runc`, the default docker container runtime, for debugging plugins by
collecting plugin logs redirected to a file.

```console
$ sudo runc --root /run/docker/runtime-runc/plugins.moby list

ID                                                                 PID         STATUS      BUNDLE                                                                                                                                       CREATED                          OWNER
93f1e7dbfe11c938782c2993628c895cf28e2274072c4a346a6002446c949b25   15806       running     /run/docker/containerd/daemon/io.containerd.runtime.v1.linux/moby-plugins/93f1e7dbfe11c938782c2993628c895cf28e2274072c4a346a6002446c949b25   2018-02-08T21:40:08.621358213Z   root
9b4606d84e06b56df84fadf054a21374b247941c94ce405b0a261499d689d9c9   14992       running     /run/docker/containerd/daemon/io.containerd.runtime.v1.linux/moby-plugins/9b4606d84e06b56df84fadf054a21374b247941c94ce405b0a261499d689d9c9   2018-02-08T21:35:12.321325872Z   root
c5bb4b90941efcaccca999439ed06d6a6affdde7081bb34dc84126b57b3e793d   14984       running     /run/docker/containerd/daemon/io.containerd.runtime.v1.linux/moby-plugins/c5bb4b90941efcaccca999439ed06d6a6affdde7081bb34dc84126b57b3e793d   2018-02-08T21:35:12.321288966Z   root
```

```console
$ sudo runc --root /run/docker/runtime-runc/plugins.moby exec 93f1e7dbfe11c938782c2993628c895cf28e2274072c4a346a6002446c949b25 cat /var/log/plugin.log
```

If the plugin has a built-in shell, then exec into the plugin can be done as
follows:

```console
$ sudo runc --root /run/docker/runtime-runc/plugins.moby exec -t 93f1e7dbfe11c938782c2993628c895cf28e2274072c4a346a6002446c949b25 sh
```

#### Using curl to debug plugin socket issues.

To verify if the plugin API socket that the docker daemon communicates with
is responsive, use curl. In this example, we will make API calls from the
docker host to volume and network plugins using curl 7.47.0 to ensure that
the plugin is listening on the said socket. For a well functioning plugin,
these basic requests should work. Note that plugin sockets are available on the host under `/var/run/docker/plugins/<pluginID>`

```console
$ curl -H "Content-Type: application/json" -XPOST -d '{}' --unix-socket /var/run/docker/plugins/e8a37ba56fc879c991f7d7921901723c64df6b42b87e6a0b055771ecf8477a6d/plugin.sock http:/VolumeDriver.List

{"Mountpoint":"","Err":"","Volumes":[{"Name":"myvol1","Mountpoint":"/data/myvol1"},{"Name":"myvol2","Mountpoint":"/data/myvol2"}],"Volume":null}
```

```console
$ curl -H "Content-Type: application/json" -XPOST -d '{}' --unix-socket /var/run/docker/plugins/45e00a7ce6185d6e365904c8bcf62eb724b1fe307e0d4e7ecc9f6c1eb7bcdb70/plugin.sock http:/NetworkDriver.GetCapabilities

{"Scope":"local"}
```

When using curl 7.5 and above, the URL should be of the form
`http://hostname/APICall`, where `hostname` is the valid hostname where the
plugin is installed and `APICall` is the call to the plugin API.

For example, `http://localhost/VolumeDriver.List`

---

# Install Docker Engine from binaries

> Learn how to install Docker as a binary. These instructions are most suitable for testing purposes.

# Install Docker Engine from binaries

   Table of contents

---

> Important
>
> This page contains information on how to install Docker using binaries. These
> instructions are mostly suitable for testing purposes. We do not recommend
> installing Docker using binaries in production environments as they don't have automatic security updates. The Linux binaries described on this
> page are statically linked, which means that vulnerabilities in build-time
> dependencies are not automatically patched by security updates of your Linux
> distribution.
>
>
>
> Updating binaries is also slightly more involved when compared to Docker packages
> installed using a package manager or through Docker Desktop, as it requires
> (manually) updating the installed version whenever there is a new release of
> Docker.
>
>
>
> Also, static binaries may not include all functionalities provided by the dynamic
> packages.
>
>
>
> On Windows and Mac, we recommend that you install
> [Docker Desktop](https://docs.docker.com/desktop/)
> instead. For Linux, we recommend that you follow the instructions specific for
> your distribution.

If you want to try Docker or use it in a testing environment, but you're not on
a supported platform, you can try installing from static binaries. If possible,
you should use packages built for your operating system, and use your operating
system's package management system to manage Docker installation and upgrades.

Static binaries for the Docker daemon binary are only available for Linux (as
`dockerd`) and Windows (as `dockerd.exe`).
Static binaries for the Docker client are available for Linux, Windows, and macOS (as `docker`).

This topic discusses binary installation for Linux, Windows, and macOS:

- [Install daemon and client binaries on Linux](#install-daemon-and-client-binaries-on-linux)
- [Install client binaries on macOS](#install-client-binaries-on-macos)
- [Install server and client binaries on Windows](#install-server-and-client-binaries-on-windows)

## Install daemon and client binaries on Linux

### Prerequisites

Before attempting to install Docker from binaries, be sure your host machine
meets the prerequisites:

- A 64-bit installation
- Version 3.10 or higher of the Linux kernel. The latest version of the kernel
  available for your platform is recommended.
- `iptables` version 1.4 or higher
- `git` version 1.7 or higher
- A `ps` executable, usually provided by `procps` or a similar package.
- [XZ Utils](https://tukaani.org/xz/) 4.9 or higher
- A [properly mounted](https://github.com/tianon/cgroupfs-mount/blob/master/cgroupfs-mount) `cgroupfs` hierarchy; a single, all-encompassing `cgroup` mount
  point is not sufficient. See Github issues
  [#2683](https://github.com/moby/moby/issues/2683),
  [#3485](https://github.com/moby/moby/issues/3485),
  [#4568](https://github.com/moby/moby/issues/4568)).

#### Secure your environment as much as possible

##### OS considerations

Enable SELinux or AppArmor if possible.

It is recommended to use AppArmor or SELinux if your Linux distribution supports
either of the two. This helps improve security and blocks certain
types of exploits. Review the documentation for your Linux distribution for
instructions for enabling and configuring AppArmor or SELinux.

> **Security warning**
>
>
>
> If either of the security mechanisms is enabled, do not disable it as a
> work-around to make Docker or its containers run. Instead, configure it
> correctly to fix any problems.

##### Docker daemon considerations

- Enable `seccomp` security profiles if possible. See
  [Enablingseccompfor Docker](https://docs.docker.com/engine/security/seccomp/).
- Enable user namespaces if possible. See the
  [Daemon user namespace options](https://docs.docker.com/reference/cli/dockerd/#daemon-user-namespace-options).

### Install static binaries

1. Download the static binary archive. Go to
  [https://download.docker.com/linux/static/stable/](https://download.docker.com/linux/static/stable/),
  choose your hardware platform, and download the `.tgz` file relating to the
  version of Docker Engine you want to install.
2. Extract the archive using the `tar` utility. The `dockerd` and `docker`
  binaries are extracted.
  ```console
  $ tar xzvf /path/to/FILE.tar.gz
  ```
3. **Optional**: Move the binaries to a directory on your executable path, such
  as `/usr/bin/`. If you skip this step, you must provide the path to the
  executable when you invoke `docker` or `dockerd` commands.
  ```console
  $ sudo cp docker/* /usr/bin/
  ```
4. Start the Docker daemon:
  ```console
  $ sudo dockerd &
  ```
  If you need to start the daemon with additional options, modify the above
  command accordingly or create and edit the file `/etc/docker/daemon.json`
  to add the custom configuration options.
5. Verify that Docker is installed correctly by running the `hello-world`
  image.
  ```console
  $ sudo docker run hello-world
  ```
  This command downloads a test image and runs it in a container. When the
  container runs, it prints a message and exits.

You have now successfully installed and started Docker Engine.

> Tip
>
> Receiving errors when trying to run without root?
>
>
>
> The `docker` user group exists but contains no users, which is why you’re required
> to use `sudo` to run Docker commands. Continue to
> [Linux postinstall](https://docs.docker.com/engine/install/linux-postinstall)
> to allow non-privileged users to run Docker commands and for other optional configuration steps.

## Install client binaries on macOS

> Note
>
> The following instructions are mostly suitable for testing purposes. The macOS
> binary includes the Docker client only. It does not include the `dockerd` daemon
> which is required to run containers. Therefore, we recommend that you install
> [Docker Desktop](https://docs.docker.com/desktop/) instead.

The binaries for Mac also do not contain:

- A runtime environment. You must set up a functional engine either in a Virtual Machine, or on a remote Linux machine.
- Docker components such as `buildx` and `docker compose`.

To install client binaries, perform the following steps:

1. Download the static binary archive. Go to
  [https://download.docker.com/mac/static/stable/](https://download.docker.com/mac/static/stable/) and select `x86_64` (for Mac on Intel chip) or `aarch64` (for Mac on Apple silicon),
  and then download the `.tgz` file relating to the version of Docker Engine you want
  to install.
2. Extract the archive using the `tar` utility. The `docker` binary is
  extracted.
  ```console
  $ tar xzvf /path/to/FILE.tar.gz
  ```
3. Clear the extended attributes to allow it run.
  ```console
  $ sudo xattr -rc docker
  ```
  Now, when you run the following command, you can see the Docker CLI usage instructions:
  ```console
  $ docker/docker
  ```
4. **Optional**: Move the binary to a directory on your executable path, such
  as `/usr/local/bin/`. If you skip this step, you must provide the path to the
  executable when you invoke `docker` or `dockerd` commands.
  ```console
  $ sudo cp docker/docker /usr/local/bin/
  ```
5. Verify that Docker is installed correctly by running the `hello-world`
  image. The value of `<hostname>` is a hostname or IP address running the
  Docker daemon and accessible to the client.
  ```console
  $ sudo docker -H <hostname> run hello-world
  ```
  This command downloads a test image and runs it in a container. When the
  container runs, it prints a message and exits.

## Install server and client binaries on Windows

> Note
>
> The following section describes how to install the Docker daemon on Windows
> Server which allows you to run Windows containers only. When you install the
> Docker daemon on Windows Server, the daemon doesn't contain Docker components
> such as `buildx` and `compose`. If you're running Windows 10 or 11,
> we recommend that you install
> [Docker Desktop](https://docs.docker.com/desktop/) instead.

Binary packages on Windows include both `dockerd.exe` and `docker.exe`. On Windows,
these binaries only provide the ability to run native Windows containers (not
Linux containers).

To install server and client binaries, perform the following steps:

1. Download the static binary archive. Go to
  [https://download.docker.com/win/static/stable/x86_64](https://download.docker.com/win/static/stable/x86_64) and select the latest version from the list.
2. Run the following PowerShell commands to install and extract the archive to your program files:
  ```powershell
  PS C:\> Expand-Archive /path/to/<FILE>.zip -DestinationPath $Env:ProgramFiles
  ```
3. Register the service and start the Docker Engine:
  ```powershell
  PS C:\> &$Env:ProgramFiles\Docker\dockerd --register-service
  PS C:\> Start-Service docker
  ```
4. Verify that Docker is installed correctly by running the `hello-world`
  image.
  ```powershell
  PS C:\> &$Env:ProgramFiles\Docker\docker run hello-world:nanoserver
  ```
  This command downloads a test image and runs it in a container. When the
  container runs, it prints a message and exits.

## Upgrade static binaries

To upgrade your manual installation of Docker Engine, first stop any
`dockerd` or `dockerd.exe` processes running locally, then follow the
regular installation steps to install the new version on top of the existing
version.

## Next steps

- Continue to [Post-installation steps for Linux](https://docs.docker.com/engine/install/linux-postinstall/).

---

# Install Docker Engine on CentOS

> Learn how to install Docker Engine on CentOS. These instructions cover the different installation methods, how to uninstall, and next steps.

# Install Docker Engine on CentOS

   Table of contents

---

To get started with Docker Engine on CentOS, make sure you
[meet the prerequisites](#prerequisites), and then follow the
[installation steps](#installation-methods).

## Prerequisites

### OS requirements

To install Docker Engine, you need a maintained version of one of the following
CentOS versions:

- CentOS Stream 10
- CentOS Stream 9

The `centos-extras` repository must be enabled. This repository is enabled by
default. If you have disabled it, you need to re-enable it.

### Uninstall old versions

Before you can install Docker Engine, you need to uninstall any conflicting packages.

Your Linux distribution may provide unofficial Docker packages, which may conflict
with the official packages provided by Docker. You must uninstall these packages
before you install the official version of Docker Engine.

```console
$ sudo dnf remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-engine
```

`dnf` might report that you have none of these packages installed.

Images, containers, volumes, and networks stored in `/var/lib/docker/` aren't
automatically removed when you uninstall Docker.

## Installation methods

You can install Docker Engine in different ways, depending on your needs:

- You can
  [set up Docker's repositories](#install-using-the-repository) and install
  from them, for ease of installation and upgrade tasks. This is the
  recommended approach.
- You can download the RPM package,
  [install it manually](#install-from-a-package), and manage
  upgrades completely manually. This is useful in situations such as installing
  Docker on air-gapped systems with no access to the internet.
- In testing and development environments, you can use automated
  [convenience scripts](#install-using-the-convenience-script) to install Docker.

Apache License, Version 2.0. See [LICENSE](https://github.com/moby/moby/blob/master/LICENSE) for the full license.

### Install using the rpm repository

Before you install Docker Engine for the first time on a new host machine, you
need to set up the Docker repository. Afterward, you can install and update
Docker from the repository.

#### Set up the repository

Install the `dnf-plugins-core` package (which provides the commands to manage
your DNF repositories) and set up the repository.

```console
$ sudo dnf -y install dnf-plugins-core
$ sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
```

#### Install Docker Engine

1. Install the Docker packages.
  To install the latest version, run:
  ```console
  $ sudo dnf install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
  ```
  If prompted to accept the GPG key, verify that the fingerprint matches
  `060A 61C5 1B55 8A7F 742B 77AA C52F EB6B 621E 9F35`, and if so, accept it.
  This command installs Docker, but it doesn't start Docker. It also creates a
  `docker` group, however, it doesn't add any users to the group by default.
  To install a specific version, start by listing the available versions in
  the repository:
  ```console
  $ dnf list docker-ce --showduplicates | sort -r
  docker-ce.x86_64    3:29.2.0-1.el9    docker-ce-stable
  docker-ce.x86_64    3:29.1.5-1.el9    docker-ce-stable
  <...>
  ```
  The list returned depends on which repositories are enabled, and is specific
  to your version of CentOS (indicated by the `.el9` suffix in this example).
  Install a specific version by its fully qualified package name, which is
  the package name (`docker-ce`) plus the version string (2nd column),
  separated by a hyphen (`-`). For example, `docker-ce-3:29.2.0-1.el9`.
  Replace `<VERSION_STRING>` with the desired version and then run the following
  command to install:
  ```console
  $ sudo dnf install docker-ce-VERSION_STRING docker-ce-cli-VERSION_STRING containerd.io docker-buildx-plugin docker-compose-plugin
  ```
  This command installs Docker, but it doesn't start Docker. It also creates a
  `docker` group, however, it doesn't add any users to the group by default.
2. Start Docker Engine.
  ```console
  $ sudo systemctl enable --now docker
  ```
  This configures the Docker systemd service to start automatically when you
  boot your system. If you don't want Docker to start automatically, use `sudo systemctl start docker` instead.
3. Verify that the installation is successful by running the `hello-world` image:
  ```console
  $ sudo docker run hello-world
  ```
  This command downloads a test image and runs it in a container. When the
  container runs, it prints a confirmation message and exits.

You have now successfully installed and started Docker Engine.

> Tip
>
> Receiving errors when trying to run without root?
>
>
>
> The `docker` user group exists but contains no users, which is why you’re required
> to use `sudo` to run Docker commands. Continue to
> [Linux postinstall](https://docs.docker.com/engine/install/linux-postinstall)
> to allow non-privileged users to run Docker commands and for other optional configuration steps.

#### Upgrade Docker Engine

To upgrade Docker Engine, follow the [installation instructions](#install-using-the-repository),
choosing the new version you want to install.

### Install from a package

If you can't use Docker's `rpm` repository to install Docker Engine, you can
download the `.rpm` file for your release and install it manually. You need to
download a new file each time you want to upgrade Docker Engine.

1. Go to [https://download.docker.com/linux/centos/](https://download.docker.com/linux/centos/)
  and choose your version of CentOS. Then browse to `x86_64/stable/Packages/`
  and download the `.rpm` file for the Docker version you want to install.
2. Install Docker Engine, changing the following path to the path where you downloaded
  the Docker package.
  ```console
  $ sudo dnf install /path/to/package.rpm
  ```
  Docker is installed but not started. The `docker` group is created, but no
  users are added to the group.
3. Start Docker Engine.
  ```console
  $ sudo systemctl enable --now docker
  ```
  This configures the Docker systemd service to start automatically when you
  boot your system. If you don't want Docker to start automatically, use `sudo systemctl start docker` instead.
4. Verify that the installation is successful by running the `hello-world` image:
  ```console
  $ sudo docker run hello-world
  ```
  This command downloads a test image and runs it in a container. When the
  container runs, it prints a confirmation message and exits.

You have now successfully installed and started Docker Engine.

> Tip
>
> Receiving errors when trying to run without root?
>
>
>
> The `docker` user group exists but contains no users, which is why you’re required
> to use `sudo` to run Docker commands. Continue to
> [Linux postinstall](https://docs.docker.com/engine/install/linux-postinstall)
> to allow non-privileged users to run Docker commands and for other optional configuration steps.

#### Upgrade Docker Engine

To upgrade Docker Engine, download the newer package files and repeat the
[installation procedure](#install-from-a-package), using `dnf upgrade`
instead of `dnf install`, and point to the new files.

### Install using the convenience script

Docker provides a convenience script at
[https://get.docker.com/](https://get.docker.com/) to install Docker into
development environments non-interactively. The convenience script isn't
recommended for production environments, but it's useful for creating a
provisioning script tailored to your needs. Also refer to the
[install using the repository](#install-using-the-repository) steps to learn
about installation steps to install using the package repository. The source code
for the script is open source, and you can find it in the
[docker-installrepository on GitHub](https://github.com/docker/docker-install).

Always examine scripts downloaded from the internet before running them locally.
Before installing, make yourself familiar with potential risks and limitations
of the convenience script:

- The script requires `root` or `sudo` privileges to run.
- The script attempts to detect your Linux distribution and version and
  configure your package management system for you.
- The script doesn't allow you to customize most installation parameters.
- The script installs dependencies and recommendations without asking for
  confirmation. This may install a large number of packages, depending on the
  current configuration of your host machine.
- By default, the script installs the latest stable release of Docker,
  containerd, and runc. When using this script to provision a machine, this may
  result in unexpected major version upgrades of Docker. Always test upgrades in
  a test environment before deploying to your production systems.
- The script isn't designed to upgrade an existing Docker installation. When
  using the script to update an existing installation, dependencies may not be
  updated to the expected version, resulting in outdated versions.

> Tip
>
> Preview script steps before running. You can run the script with the `--dry-run` option to learn what steps the
> script will run when invoked:
>
>
>
> ```console
> $ curl -fsSL https://get.docker.com -o get-docker.sh
> $ sudo sh ./get-docker.sh --dry-run
> ```

This example downloads the script from
[https://get.docker.com/](https://get.docker.com/) and runs it to install the
latest stable release of Docker on Linux:

```console
$ curl -fsSL https://get.docker.com -o get-docker.sh
$ sudo sh get-docker.sh
Executing docker install script, commit: 7cae5f8b0decc17d6571f9f52eb840fbc13b2737
<...>
```

You have now successfully installed and started Docker Engine. The `docker`
service starts automatically on Debian based distributions. On `RPM` based
distributions, such as CentOS, Fedora or RHEL, you need to start it
manually using the appropriate `systemctl` or `service` command. As the message
indicates, non-root users can't run Docker commands by default.

> **Use Docker as a non-privileged user, or install in rootless mode?**
>
>
>
> The installation script requires `root` or `sudo` privileges to install and
> use Docker. If you want to grant non-root users access to Docker, refer to the
> [post-installation steps for Linux](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user).
> You can also install Docker without `root` privileges, or configured to run in
> rootless mode. For instructions on running Docker in rootless mode, refer to
> [run the Docker daemon as a non-root user (rootless mode)](https://docs.docker.com/engine/security/rootless/).

#### Install pre-releases

Docker also provides a convenience script at
[https://test.docker.com/](https://test.docker.com/) to install pre-releases of
Docker on Linux. This script is equal to the script at `get.docker.com`, but
configures your package manager to use the test channel of the Docker package
repository. The test channel includes both stable and pre-releases (beta
versions, release-candidates) of Docker. Use this script to get early access to
new releases, and to evaluate them in a testing environment before they're
released as stable.

To install the latest version of Docker on Linux from the test channel, run:

```console
$ curl -fsSL https://test.docker.com -o test-docker.sh
$ sudo sh test-docker.sh
```

#### Upgrade Docker after using the convenience script

If you installed Docker using the convenience script, you should upgrade Docker
using your package manager directly. There's no advantage to re-running the
convenience script. Re-running it can cause issues if it attempts to re-install
repositories which already exist on the host machine.

## Uninstall Docker Engine

1. Uninstall the Docker Engine, CLI, containerd, and Docker Compose packages:
  ```console
  $ sudo dnf remove docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras
  ```
2. Images, containers, volumes, or custom configuration files on your host
  aren't automatically removed. To delete all images, containers, and volumes:
  ```console
  $ sudo rm -rf /var/lib/docker
  $ sudo rm -rf /var/lib/containerd
  ```

You have to delete any edited configuration files manually.

## Next steps

- Continue to [Post-installation steps for Linux](https://docs.docker.com/engine/install/linux-postinstall/).
