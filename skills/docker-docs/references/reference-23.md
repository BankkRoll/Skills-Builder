# docker container create and more

# docker container create

# docker container create

| Description | Create a new container |
| --- | --- |
| Usage | docker container create [OPTIONS] IMAGE [COMMAND] [ARG...] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker create |

## Description

The `docker container create` (or shorthand: `docker create`) command creates a
new container from the specified image, without starting it.

When creating a container, the Docker daemon creates a writeable container layer
over the specified image and prepares it for running the specified command. The
container ID is then printed to `STDOUT`. This is similar to `docker run -d`
except the container is never started. You can then use the `docker container start`
(or shorthand: `docker start`) command to start the container at any point.

This is useful when you want to set up a container configuration ahead of time
so that it's ready to start when you need it. The initial status of the
new container is `created`.

The `docker create` command shares most of its options with the `docker run`
command (which performs a `docker create` before starting it).
Refer to the
[docker runCLI reference](https://docs.docker.com/reference/cli/docker/container/run/)
for details on the available flags and options.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --add-host |  | Add a custom host-to-IP mapping (host:ip) |
| --annotation |  | API 1.43+Add an annotation to the container (passed through to the OCI runtime) |
| -a, --attach |  | Attach to STDIN, STDOUT or STDERR |
| --blkio-weight |  | Block IO (relative weight), between 10 and 1000, or 0 to disable (default 0) |
| --blkio-weight-device |  | Block IO weight (relative device weight) |
| --cap-add |  | Add Linux capabilities |
| --cap-drop |  | Drop Linux capabilities |
| --cgroup-parent |  | Optional parent cgroup for the container |
| --cgroupns |  | API 1.41+Cgroup namespace to use (host|private)'host': Run the container in the Docker host's cgroup namespace'private': Run the container in its own private cgroup namespace'': Use the cgroup namespace as configured by thedefault-cgroupns-mode option on the daemon (default) |
| --cidfile |  | Write the container ID to the file |
| --cpu-count |  | CPU count (Windows only) |
| --cpu-percent |  | CPU percent (Windows only) |
| --cpu-period |  | Limit CPU CFS (Completely Fair Scheduler) period |
| --cpu-quota |  | Limit CPU CFS (Completely Fair Scheduler) quota |
| --cpu-rt-period |  | API 1.25+Limit CPU real-time period in microseconds |
| --cpu-rt-runtime |  | API 1.25+Limit CPU real-time runtime in microseconds |
| -c, --cpu-shares |  | CPU shares (relative weight) |
| --cpus |  | API 1.25+Number of CPUs |
| --cpuset-cpus |  | CPUs in which to allow execution (0-3, 0,1) |
| --cpuset-mems |  | MEMs in which to allow execution (0-3, 0,1) |
| --device |  | Add a host device to the container |
| --device-cgroup-rule |  | Add a rule to the cgroup allowed devices list |
| --device-read-bps |  | Limit read rate (bytes per second) from a device |
| --device-read-iops |  | Limit read rate (IO per second) from a device |
| --device-write-bps |  | Limit write rate (bytes per second) to a device |
| --device-write-iops |  | Limit write rate (IO per second) to a device |
| --dns |  | Set custom DNS servers |
| --dns-option |  | Set DNS options |
| --dns-search |  | Set custom DNS search domains |
| --domainname |  | Container NIS domain name |
| --entrypoint |  | Overwrite the default ENTRYPOINT of the image |
| -e, --env |  | Set environment variables |
| --env-file |  | Read in a file of environment variables |
| --expose |  | Expose a port or a range of ports |
| --gpus |  | API 1.40+GPU devices to add to the container ('all' to pass all GPUs) |
| --group-add |  | Add additional groups to join |
| --health-cmd |  | Command to run to check health |
| --health-interval |  | Time between running the check (ms|s|m|h) (default 0s) |
| --health-retries |  | Consecutive failures needed to report unhealthy |
| --health-start-interval |  | API 1.44+Time between running the check during the start period (ms|s|m|h) (default 0s) |
| --health-start-period |  | API 1.29+Start period for the container to initialize before starting health-retries countdown (ms|s|m|h) (default 0s) |
| --health-timeout |  | Maximum time to allow one check to run (ms|s|m|h) (default 0s) |
| --help |  | Print usage |
| -h, --hostname |  | Container host name |
| --init |  | API 1.25+Run an init inside the container that forwards signals and reaps processes |
| -i, --interactive |  | Keep STDIN open even if not attached |
| --io-maxbandwidth |  | Maximum IO bandwidth limit for the system drive (Windows only) |
| --io-maxiops |  | Maximum IOps limit for the system drive (Windows only) |
| --ip |  | IPv4 address (e.g., 172.30.100.104) |
| --ip6 |  | IPv6 address (e.g., 2001:db8::33) |
| --ipc |  | IPC mode to use |
| --isolation |  | Container isolation technology |
| -l, --label |  | Set meta data on a container |
| --label-file |  | Read in a line delimited file of labels |
| --link |  | Add link to another container |
| --link-local-ip |  | Container IPv4/IPv6 link-local addresses |
| --log-driver |  | Logging driver for the container |
| --log-opt |  | Log driver options |
| --mac-address |  | Container MAC address (e.g., 92:d0:c6:0a:29:33) |
| -m, --memory |  | Memory limit |
| --memory-reservation |  | Memory soft limit |
| --memory-swap |  | Swap limit equal to memory plus swap: '-1' to enable unlimited swap |
| --memory-swappiness | -1 | Tune container memory swappiness (0 to 100) |
| --mount |  | Attach a filesystem mount to the container |
| --name |  | Assign a name to the container |
| --network |  | Connect a container to a network |
| --network-alias |  | Add network-scoped alias for the container |
| --no-healthcheck |  | Disable any container-specified HEALTHCHECK |
| --oom-kill-disable |  | Disable OOM Killer |
| --oom-score-adj |  | Tune host's OOM preferences (-1000 to 1000) |
| --pid |  | PID namespace to use |
| --pids-limit |  | Tune container pids limit (set -1 for unlimited) |
| --platform |  | API 1.32+Set platform if server is multi-platform capable |
| --privileged |  | Give extended privileges to this container |
| -p, --publish |  | Publish a container's port(s) to the host |
| -P, --publish-all |  | Publish all exposed ports to random ports |
| --pull | missing | Pull image before creating (always,|missing,never) |
| -q, --quiet |  | Suppress the pull output |
| --read-only |  | Mount the container's root filesystem as read only |
| --restart | no | Restart policy to apply when a container exits |
| --rm |  | Automatically remove the container and its associated anonymous volumes when it exits |
| --runtime |  | Runtime to use for this container |
| --security-opt |  | Security Options |
| --shm-size |  | Size of /dev/shm |
| --stop-signal |  | Signal to stop the container |
| --stop-timeout |  | API 1.25+Timeout (in seconds) to stop a container |
| --storage-opt |  | Storage driver options for the container |
| --sysctl |  | Sysctl options |
| --tmpfs |  | Mount a tmpfs directory |
| -t, --tty |  | Allocate a pseudo-TTY |
| --ulimit |  | Ulimit options |
| --use-api-socket |  | experimental (CLI)Bind mount Docker API socket and required auth |
| -u, --user |  | Username or UID (format: <name|uid>[:<group|gid>]) |
| --userns |  | User namespace to use |
| --uts |  | UTS namespace to use |
| -v, --volume |  | Bind mount a volume |
| --volume-driver |  | Optional volume driver for the container |
| --volumes-from |  | Mount volumes from the specified container(s) |
| -w, --workdir |  | Working directory inside the container |

## Examples

### Create and start a container

The following example creates an interactive container with a pseudo-TTY attached,
then starts the container and attaches to it:

```console
$ docker container create -i -t --name mycontainer alpine
6d8af538ec541dd581ebc2a24153a28329acb5268abe5ef868c1f1a261221752

$ docker container start --attach -i mycontainer
/ # echo hello world
hello world
```

The above is the equivalent of a `docker run`:

```console
$ docker run -it --name mycontainer2 alpine
/ # echo hello world
hello world
```

### Initialize volumes

Container volumes are initialized during the `docker create` phase
(i.e., `docker run` too). For example, this allows you to `create` the `data`
volume container, and then use it from another container:

```console
$ docker create -v /data --name data ubuntu

240633dfbb98128fa77473d3d9018f6123b99c454b3251427ae190a7d951ad57

$ docker run --rm --volumes-from data ubuntu ls -la /data

total 8
drwxr-xr-x  2 root root 4096 Dec  5 04:10 .
drwxr-xr-x 48 root root 4096 Dec  5 04:11 ..
```

Similarly, `create` a host directory bind mounted volume container, which can
then be used from the subsequent container:

```console
$ docker create -v /home/docker:/docker --name docker ubuntu

9aa88c08f319cd1e4515c3c46b0de7cc9aa75e878357b1e96f91e2c773029f03

$ docker run --rm --volumes-from docker ubuntu ls -la /docker

total 20
drwxr-sr-x  5 1000 staff  180 Dec  5 04:00 .
drwxr-xr-x 48 root root  4096 Dec  5 04:13 ..
-rw-rw-r--  1 1000 staff 3833 Dec  5 04:01 .ash_history
-rw-r--r--  1 1000 staff  446 Nov 28 11:51 .ashrc
-rw-r--r--  1 1000 staff   25 Dec  5 04:00 .gitconfig
drwxr-sr-x  3 1000 staff   60 Dec  1 03:28 .local
-rw-r--r--  1 1000 staff  920 Nov 28 11:51 .profile
drwx--S---  2 1000 staff  460 Dec  5 00:51 .ssh
drwxr-xr-x 32 1000 staff 1140 Dec  5 04:01 docker
```

---

# docker container diff

# docker container diff

| Description | Inspect changes to files or directories on a container's filesystem |
| --- | --- |
| Usage | docker container diff CONTAINER |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker diff |

## Description

List the changed files and directories in a container᾿s filesystem since the
container was created. Three different types of change are tracked:

| Symbol | Description |
| --- | --- |
| A | A file or directory was added |
| D | A file or directory was deleted |
| C | A file or directory was changed |

You can use the full or shortened container ID or the container name set using
`docker run --name` option.

## Examples

Inspect the changes to an `nginx` container:

```console
$ docker diff 1fdfd1f54c1b

C /dev
C /dev/console
C /dev/core
C /dev/stdout
C /dev/fd
C /dev/ptmx
C /dev/stderr
C /dev/stdin
C /run
A /run/nginx.pid
C /var/lib/nginx/tmp
A /var/lib/nginx/tmp/client_body
A /var/lib/nginx/tmp/fastcgi
A /var/lib/nginx/tmp/proxy
A /var/lib/nginx/tmp/scgi
A /var/lib/nginx/tmp/uwsgi
C /var/log/nginx
A /var/log/nginx/access.log
A /var/log/nginx/error.log
```

---

# docker container exec

# docker container exec

| Description | Execute a command in a running container |
| --- | --- |
| Usage | docker container exec [OPTIONS] CONTAINER COMMAND [ARG...] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker exec |

> **Introducing Docker Debug**
>
>
>
> To easily get a debug shell into any container, use `docker debug`. Docker
> Debug is a replacement for debugging with `docker exec`. With it, you can get
> a shell into any container or image, even slim ones, without modifications.
> Plus, you can bring along your favorite debugging tools in its customizable
> toolbox.
>
>
>
> Explore [Docker Debug](https://docs.docker.com/reference/cli/docker/debug/) now.

## Description

The `docker exec` command runs a new command in a running container.

The command you specify with `docker exec` only runs while the container's
primary process (`PID 1`) is running, and it isn't restarted if the container
is restarted.

The command runs in the default working directory of the container.

The command must be an executable. A chained or a quoted command doesn't work.

- This works: `docker exec -it my_container sh -c "echo a && echo b"`
- This doesn't work: `docker exec -it my_container "echo a && echo b"`

## Options

| Option | Default | Description |
| --- | --- | --- |
| -d, --detach |  | Detached mode: run command in the background |
| --detach-keys |  | Override the key sequence for detaching a container |
| -e, --env |  | API 1.25+Set environment variables |
| --env-file |  | API 1.25+Read in a file of environment variables |
| -i, --interactive |  | Keep STDIN open even if not attached |
| --privileged |  | Give extended privileges to the command |
| -t, --tty |  | Allocate a pseudo-TTY |
| -u, --user |  | Username or UID (format:<name|uid>[:<group|gid>]) |
| -w, --workdir |  | API 1.35+Working directory inside the container |

## Examples

### Rundocker execon a running container

First, start a container.

```console
$ docker run --name mycontainer -d -i -t alpine /bin/sh
```

This creates and starts a container named `mycontainer` from an `alpine` image
with an `sh` shell as its main process. The `-d` option (shorthand for `--detach`)
sets the container to run in the background, in detached mode, with a pseudo-TTY
attached (`-t`). The `-i` option is set to keep `STDIN` attached (`-i`), which
prevents the `sh` process from exiting immediately.

Next, execute a command on the container.

```console
$ docker exec -d mycontainer touch /tmp/execWorks
```

This creates a new file `/tmp/execWorks` inside the running container
`mycontainer`, in the background.

Next, execute an interactive `sh` shell on the container.

```console
$ docker exec -it mycontainer sh
```

This starts a new shell session in the container `mycontainer`.

### Set environment variables for the exec process (--env, -e)

Next, set environment variables in the current bash session.

The `docker exec` command inherits the environment variables that are set at the
time the container is created. Use the `--env` (or the `-e` shorthand) to
override global environment variables, or to set additional environment
variables for the process started by `docker exec`.

The following example creates a new shell session in the container `mycontainer`,
with environment variables `$VAR_A` set to `1`, and `$VAR_B` set to `2`.
These environment variables are only valid for the `sh` process started by that
`docker exec` command, and aren't available to other processes running inside
the container.

```console
$ docker exec -e VAR_A=1 -e VAR_B=2 mycontainer env
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
HOSTNAME=f64a4851eb71
VAR_A=1
VAR_B=2
HOME=/root
```

### Escalate container privileges (--privileged)

See
[docker run --privileged](https://docs.docker.com/reference/cli/docker/container/run/#privileged).

### Set the working directory for the exec process (--workdir, -w)

By default `docker exec` command runs in the same working directory set when
the container was created.

```console
$ docker exec -it mycontainer pwd
/
```

You can specify an alternative working directory for the command to execute
using the `--workdir` option (or the `-w` shorthand):

```console
$ docker exec -it -w /root mycontainer pwd
/root
```

### Try to rundocker execon a paused container

If the container is paused, then the `docker exec` command fails with an error:

```console
$ docker pause mycontainer
mycontainer

$ docker ps

CONTAINER ID   IMAGE     COMMAND     CREATED          STATUS                   PORTS     NAMES
482efdf39fac   alpine    "/bin/sh"   17 seconds ago   Up 16 seconds (Paused)             mycontainer

$ docker exec mycontainer sh

Error response from daemon: Container mycontainer is paused, unpause the container before exec

$ echo $?
1
```

---

# docker container export

# docker container export

| Description | Export a container's filesystem as a tar archive |
| --- | --- |
| Usage | docker container export [OPTIONS] CONTAINER |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker export |

## Description

The `docker export` command doesn't export the contents of volumes associated
with the container. If a volume is mounted on top of an existing directory in
the container, `docker export` exports the contents of the underlying
directory, not the contents of the volume.

Refer to
[Backup, restore, or migrate data volumes](https://docs.docker.com/engine/storage/volumes/#back-up-restore-or-migrate-data-volumes)
in the user guide for examples on exporting data in a volume.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -o, --output |  | Write to a file, instead of STDOUT |

## Examples

The following commands produce the same result.

```console
$ docker export red_panda > latest.tar
```

```console
$ docker export --output="latest.tar" red_panda
```

---

# docker container inspect

# docker container inspect

| Description | Display detailed information on one or more containers |
| --- | --- |
| Usage | docker container inspect [OPTIONS] CONTAINER [CONTAINER...] |

## Description

Display detailed information on one or more containers

## Options

| Option | Default | Description |
| --- | --- | --- |
| -f, --format |  | Format output using a custom template:'json': Print in JSON format'TEMPLATE': Print output using the given Go template.Refer tohttps://docs.docker.com/go/formatting/for more information about formatting output with templates |
| -s, --size |  | Display total file sizes |

---

# docker container kill

# docker container kill

| Description | Kill one or more running containers |
| --- | --- |
| Usage | docker container kill [OPTIONS] CONTAINER [CONTAINER...] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker kill |

## Description

The `docker kill` subcommand kills one or more containers. The main process
inside the container is sent `SIGKILL` signal (default), or the signal that is
specified with the `--signal` option. You can reference a container by its
ID, ID-prefix, or name.

The `--signal` flag sets the system call signal that is sent to the container.
This signal can be a signal name in the format `SIG<NAME>`, for instance `SIGINT`,
or an unsigned number that matches a position in the kernel's syscall table,
for instance `2`.

While the default (`SIGKILL`) signal will terminate the container, the signal
set through `--signal` may be non-terminal, depending on the container's main
process. For example, the `SIGHUP` signal in most cases will be non-terminal,
and the container will continue running after receiving the signal.

> Note
>
> `ENTRYPOINT` and `CMD` in the *shell* form run as a child process of
> `/bin/sh -c`, which does not pass signals. This means that the executable is
> not the container’s PID 1 and does not receive Unix signals.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -s, --signal |  | Signal to send to the container |

## Examples

### Send a KILL signal to a container

The following example sends the default `SIGKILL` signal to the container named
`my_container`:

```console
$ docker kill my_container
```

### Send a custom signal to a container (--signal)

The following example sends a `SIGHUP` signal to the container named
`my_container`:

```console
$ docker kill --signal=SIGHUP  my_container
```

You can specify a custom signal either by *name*, or *number*. The `SIG` prefix
is optional, so the following examples are equivalent:

```console
$ docker kill --signal=SIGHUP my_container
$ docker kill --signal=HUP my_container
$ docker kill --signal=1 my_container
```

Refer to the [signal(7)](https://man7.org/linux/man-pages/man7/signal.7.html)
man-page for a list of standard Linux signals.

---

# docker container logs

# docker container logs

| Description | Fetch the logs of a container |
| --- | --- |
| Usage | docker container logs [OPTIONS] CONTAINER |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker logs |

## Description

The `docker logs` command batch-retrieves logs present at the time of execution.

For more information about selecting and configuring logging drivers, refer to
[Configure logging drivers](https://docs.docker.com/engine/logging/configure/).

The `docker logs --follow` command will continue streaming the new output from
the container's `STDOUT` and `STDERR`.

Passing a negative number or a non-integer to `--tail` is invalid and the
value is set to `all` in that case.

The `docker logs --timestamps` command will add an [RFC3339Nano timestamp](https://pkg.go.dev/time#RFC3339Nano)
, for example `2014-09-16T06:17:46.000000000Z`, to each
log entry. To ensure that the timestamps are aligned the
nano-second part of the timestamp will be padded with zero when necessary.

The `docker logs --details` command will add on extra attributes, such as
environment variables and labels, provided to `--log-opt` when creating the
container.

The `--since` option shows only the container logs generated after
a given date. You can specify the date as an RFC 3339 date, a UNIX
timestamp, or a Go duration string (e.g. `1m30s`, `3h`). Besides RFC3339 date
format you may also use RFC3339Nano, `2006-01-02T15:04:05`,
`2006-01-02T15:04:05.999999999`, `2006-01-02T07:00`, and `2006-01-02`. The local
timezone on the client will be used if you do not provide either a `Z` or a
`+-00:00` timezone offset at the end of the timestamp. When providing Unix
timestamps enter seconds[.nanoseconds], where seconds is the number of seconds
that have elapsed since January 1, 1970 (midnight UTC/GMT), not counting leap
seconds (aka Unix epoch or Unix time), and the optional .nanoseconds field is a
fraction of a second no more than nine digits long. You can combine the
`--since` option with either or both of the `--follow` or `--tail` options.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --details |  | Show extra details provided to logs |
| -f, --follow |  | Follow log output |
| --since |  | Show logs since timestamp (e.g.2013-01-02T13:23:37Z) or relative (e.g.42mfor 42 minutes) |
| -n, --tail | all | Number of lines to show from the end of the logs |
| -t, --timestamps |  | Show timestamps |
| --until |  | API 1.35+Show logs before a timestamp (e.g.2013-01-02T13:23:37Z) or relative (e.g.42mfor 42 minutes) |

## Examples

### Retrieve logs until a specific point in time (--until)

In order to retrieve logs before a specific point in time, run:

```console
$ docker run --name test -d busybox sh -c "while true; do $(echo date); sleep 1; done"
$ date
Tue 14 Nov 2017 16:40:00 CET
$ docker logs -f --until=2s test
Tue 14 Nov 2017 16:40:00 CET
Tue 14 Nov 2017 16:40:01 CET
Tue 14 Nov 2017 16:40:02 CET
```

---

# docker container ls

# docker container ls

| Description | List containers |
| --- | --- |
| Usage | docker container ls [OPTIONS] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker container listdocker container psdocker ps |

## Description

List containers

## Options

| Option | Default | Description |
| --- | --- | --- |
| -a, --all |  | Show all containers (default shows just running) |
| -f, --filter |  | Filter output based on conditions provided |
| --format |  | Format output using a custom template:'table': Print output in table format with column headers (default)'table TEMPLATE': Print output in table format using the given Go template'json': Print in JSON format'TEMPLATE': Print output using the given Go template.Refer tohttps://docs.docker.com/go/formatting/for more information about formatting output with templates |
| -n, --last | -1 | Show n last created containers (includes all states) |
| -l, --latest |  | Show the latest created container (includes all states) |
| --no-trunc |  | Don't truncate output |
| -q, --quiet |  | Only display container IDs |
| -s, --size |  | Display total file sizes |

## Examples

### Do not truncate output (--no-trunc)

Running `docker ps --no-trunc` showing 2 linked containers.

```console
$ docker ps --no-trunc

CONTAINER ID                                                     IMAGE                        COMMAND                CREATED              STATUS              PORTS               NAMES
ca5534a51dd04bbcebe9b23ba05f389466cf0c190f1f8f182d7eea92a9671d00 ubuntu:24.04                 bash                   17 seconds ago       Up 16 seconds       3300-3310/tcp       webapp
9ca9747b233100676a48cc7806131586213fa5dab86dd1972d6a8732e3a84a4d crosbymichael/redis:latest   /redis-server --dir    33 minutes ago       Up 33 minutes       6379/tcp            redis,webapp/db
```

### Show both running and stopped containers (-a, --all)

The `docker ps` command only shows running containers by default. To see all
containers, use the `--all` (or `-a`) flag:

```console
$ docker ps -a
```

`docker ps` groups exposed ports into a single range if possible. E.g., a
container that exposes TCP ports `100, 101, 102` displays `100-102/tcp` in
the `PORTS` column.

### Show disk usage by container (--size)

The `docker ps --size` (or `-s`) command displays two different on-disk-sizes for each container:

```console
$ docker ps --size

CONTAINER ID   IMAGE          COMMAND                  CREATED        STATUS       PORTS   NAMES        SIZE
e90b8831a4b8   nginx          "/bin/bash -c 'mkdir "   11 weeks ago   Up 4 hours           my_nginx     35.58 kB (virtual 109.2 MB)
00c6131c5e30   telegraf:1.5   "/entrypoint.sh"         11 weeks ago   Up 11 weeks          my_telegraf  0 B (virtual 209.5 MB)
```

- The "size" information shows the amount of data (on disk) that is used for the *writable* layer of each container
- The "virtual size" is the total amount of disk-space used for the read-only *image* data used by the container and the writable layer.

For more information, refer to the
[container size on disk](https://docs.docker.com/engine/storage/drivers/#container-size-on-disk) section.

### Filtering (--filter)

The `--filter` (or `-f`) flag format is a `key=value` pair. If there is more
than one filter, then pass multiple flags (e.g. `--filter "foo=bar" --filter "bif=baz"`).

The currently supported filters are:

| Filter | Description |
| --- | --- |
| id | Container's ID |
| name | Container's name |
| label | An arbitrary string representing either a key or a key-value pair. Expressed as<key>or<key>=<value> |
| exited | An integer representing the container's exit code. Only useful with--all. |
| status | One ofcreated,restarting,running,removing,paused,exited, ordead |
| ancestor | Filters containers which share a given image as an ancestor. Expressed as<image-name>[:<tag>],<image id>, or<image@digest> |
| beforeorsince | Filters containers created before or after a given container ID or name |
| volume | Filters running containers which have mounted a given volume or bind mount. |
| network | Filters running containers connected to a given network. |
| publishorexpose | Filters containers which publish or expose a given port. Expressed as<port>[/<proto>]or<startport-endport>/[<proto>] |
| health | Filters containers based on their healthcheck status. One ofstarting,healthy,unhealthyornone. |
| isolation | Windows daemon only. One ofdefault,process, orhyperv. |
| is-task | Filters containers that are a "task" for a service. Boolean option (trueorfalse) |

#### label

The `label` filter matches containers based on the presence of a `label` alone or a `label` and a
value.

The following filter matches containers with the `color` label regardless of its value.

```console
$ docker ps --filter "label=color"

CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
673394ef1d4c        busybox             "top"               47 seconds ago      Up 45 seconds                           nostalgic_shockley
d85756f57265        busybox             "top"               52 seconds ago      Up 51 seconds                           high_albattani
```

The following filter matches containers with the `color` label with the `blue` value.

```console
$ docker ps --filter "label=color=blue"

CONTAINER ID        IMAGE               COMMAND             CREATED              STATUS              PORTS               NAMES
d85756f57265        busybox             "top"               About a minute ago   Up About a minute                       high_albattani
```

#### name

The `name` filter matches on all or part of a container's name.

The following filter matches all containers with a name containing the `nostalgic_stallman` string.

```console
$ docker ps --filter "name=nostalgic_stallman"

CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
9b6247364a03        busybox             "top"               2 minutes ago       Up 2 minutes                            nostalgic_stallman
```

You can also filter for a substring in a name as this shows:

```console
$ docker ps --filter "name=nostalgic"

CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
715ebfcee040        busybox             "top"               3 seconds ago       Up 1 second                             i_am_nostalgic
9b6247364a03        busybox             "top"               7 minutes ago       Up 7 minutes                            nostalgic_stallman
673394ef1d4c        busybox             "top"               38 minutes ago      Up 38 minutes                           nostalgic_shockley
```

#### exited

The `exited` filter matches containers by exist status code. For example, to
filter for containers that have exited successfully:

```console
$ docker ps -a --filter 'exited=0'

CONTAINER ID        IMAGE             COMMAND                CREATED             STATUS                   PORTS                      NAMES
ea09c3c82f6e        registry:latest   /srv/run.sh            2 weeks ago         Exited (0) 2 weeks ago   127.0.0.1:5000->5000/tcp   desperate_leakey
106ea823fe4e        fedora:latest     /bin/sh -c 'bash -l'   2 weeks ago         Exited (0) 2 weeks ago                              determined_albattani
48ee228c9464        fedora:20         bash                   2 weeks ago         Exited (0) 2 weeks ago                              tender_torvalds
```

#### Filter by exit signal

You can use a filter to locate containers that exited with status of `137`
meaning a `SIGKILL(9)` killed them.

```console
$ docker ps -a --filter 'exited=137'

CONTAINER ID        IMAGE               COMMAND                CREATED             STATUS                       PORTS               NAMES
b3e1c0ed5bfe        ubuntu:latest       "sleep 1000"           12 seconds ago      Exited (137) 5 seconds ago                       grave_kowalevski
a2eb5558d669        redis:latest        "/entrypoint.sh redi   2 hours ago         Exited (137) 2 hours ago                         sharp_lalande
```

Any of these events result in a `137` status:

- the `init` process of the container is killed manually
- `docker kill` kills the container
- Docker daemon restarts which kills all running containers

#### status

The `status` filter matches containers by status. The possible values for the container status are:

| Status | Description |
| --- | --- |
| created | A container that has never been started. |
| running | A running container, started by eitherdocker startordocker run. |
| paused | A paused container. Seedocker pause. |
| restarting | A container which is starting due to the designated restart policy for that container. |
| exited | A container which is no longer running. For example, the process inside the container completed or the container was stopped using thedocker stopcommand. |
| removing | A container which is in the process of being removed. Seedocker rm. |
| dead | A "defunct" container; for example, a container that was only partially removed because resources were kept busy by an external process.deadcontainers cannot be (re)started, only removed. |

For example, to filter for `running` containers:

```console
$ docker ps --filter status=running

CONTAINER ID        IMAGE                  COMMAND             CREATED             STATUS              PORTS               NAMES
715ebfcee040        busybox                "top"               16 minutes ago      Up 16 minutes                           i_am_nostalgic
d5c976d3c462        busybox                "top"               23 minutes ago      Up 23 minutes                           top
9b6247364a03        busybox                "top"               24 minutes ago      Up 24 minutes                           nostalgic_stallman
```

To filter for `paused` containers:

```console
$ docker ps --filter status=paused

CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS                      PORTS               NAMES
673394ef1d4c        busybox             "top"               About an hour ago   Up About an hour (Paused)                       nostalgic_shockley
```

#### ancestor

The `ancestor` filter matches containers based on its image or a descendant of
it. The filter supports the following image representation:

- `image`
- `image:tag`
- `image:tag@digest`
- `short-id`
- `full-id`

If you don't specify a `tag`, the `latest` tag is used. For example, to filter
for containers that use the latest `ubuntu` image:

```console
$ docker ps --filter ancestor=ubuntu

CONTAINER ID        IMAGE               COMMAND             CREATED              STATUS              PORTS               NAMES
919e1179bdb8        ubuntu-c1           "top"               About a minute ago   Up About a minute                       admiring_lovelace
5d1e4a540723        ubuntu-c2           "top"               About a minute ago   Up About a minute                       admiring_sammet
82a598284012        ubuntu              "top"               3 minutes ago        Up 3 minutes                            sleepy_bose
bab2a34ba363        ubuntu              "top"               3 minutes ago        Up 3 minutes                            focused_yonath
```

Match containers based on the `ubuntu-c1` image which, in this case, is a child
of `ubuntu`:

```console
$ docker ps --filter ancestor=ubuntu-c1

CONTAINER ID        IMAGE               COMMAND             CREATED              STATUS              PORTS               NAMES
919e1179bdb8        ubuntu-c1           "top"               About a minute ago   Up About a minute                       admiring_lovelace
```

Match containers based on the `ubuntu` version `24.04` image:

```console
$ docker ps --filter ancestor=ubuntu:24.04

CONTAINER ID        IMAGE               COMMAND             CREATED              STATUS              PORTS               NAMES
82a598284012        ubuntu:24.04        "top"               3 minutes ago        Up 3 minutes                            sleepy_bose
```

The following matches containers based on the layer `d0e008c6cf02` or an image
that have this layer in its layer stack.

```console
$ docker ps --filter ancestor=d0e008c6cf02

CONTAINER ID        IMAGE               COMMAND             CREATED              STATUS              PORTS               NAMES
82a598284012        ubuntu:24.04        "top"               3 minutes ago        Up 3 minutes                            sleepy_bose
```

#### Create time

##### before

The `before` filter shows only containers created before the container with
a given ID or name. For example, having these containers created:

```console
$ docker ps

CONTAINER ID        IMAGE       COMMAND       CREATED              STATUS              PORTS              NAMES
9c3527ed70ce        busybox     "top"         14 seconds ago       Up 15 seconds                          desperate_dubinsky
4aace5031105        busybox     "top"         48 seconds ago       Up 49 seconds                          focused_hamilton
6e63f6ff38b0        busybox     "top"         About a minute ago   Up About a minute                      distracted_fermat
```

Filtering with `before` would give:

```console
$ docker ps -f before=9c3527ed70ce

CONTAINER ID        IMAGE       COMMAND       CREATED              STATUS              PORTS              NAMES
4aace5031105        busybox     "top"         About a minute ago   Up About a minute                      focused_hamilton
6e63f6ff38b0        busybox     "top"         About a minute ago   Up About a minute                      distracted_fermat
```

##### since

The `since` filter shows only containers created since the container with a given
ID or name. For example, with the same containers as in `before` filter:

```console
$ docker ps -f since=6e63f6ff38b0

CONTAINER ID        IMAGE       COMMAND       CREATED             STATUS              PORTS               NAMES
9c3527ed70ce        busybox     "top"         10 minutes ago      Up 10 minutes                           desperate_dubinsky
4aace5031105        busybox     "top"         10 minutes ago      Up 10 minutes                           focused_hamilton
```

#### volume

The `volume` filter shows only containers that mount a specific volume or have
a volume mounted in a specific path:

```console
$ docker ps --filter volume=remote-volume --format "table {{.ID}}\t{{.Mounts}}"

CONTAINER ID        MOUNTS
9c3527ed70ce        remote-volume

$ docker ps --filter volume=/data --format "table {{.ID}}\t{{.Mounts}}"

CONTAINER ID        MOUNTS
9c3527ed70ce        remote-volume
```

#### network

The `network` filter shows only containers that are connected to a network with
a given name or ID.

The following filter matches all containers that are connected to a network
with a name containing `net1`.

```console
$ docker run -d --net=net1 --name=test1 ubuntu top
$ docker run -d --net=net2 --name=test2 ubuntu top

$ docker ps --filter network=net1

CONTAINER ID        IMAGE       COMMAND       CREATED             STATUS              PORTS               NAMES
9d4893ed80fe        ubuntu      "top"         10 minutes ago      Up 10 minutes                           test1
```

The network filter matches on both the network's name and ID. The following
example shows all containers that are attached to the `net1` network, using
the network ID as a filter:

```console
$ docker network inspect --format "{{.ID}}" net1

8c0b4110ae930dbe26b258de9bc34a03f98056ed6f27f991d32919bfe401d7c5

$ docker ps --filter network=8c0b4110ae930dbe26b258de9bc34a03f98056ed6f27f991d32919bfe401d7c5

CONTAINER ID        IMAGE       COMMAND       CREATED             STATUS              PORTS               NAMES
9d4893ed80fe        ubuntu      "top"         10 minutes ago      Up 10 minutes                           test1
```

#### publish and expose

The `publish` and `expose` filters show only containers that have published or exposed port with a given port
number, port range, and/or protocol. The default protocol is `tcp` when not specified.

The following filter matches all containers that have published port of 80:

```console
$ docker run -d --publish=80 busybox top
$ docker run -d --expose=8080 busybox top

$ docker ps -a

CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS                   NAMES
9833437217a5        busybox             "top"               5 seconds ago       Up 4 seconds        8080/tcp                dreamy_mccarthy
fc7e477723b7        busybox             "top"               50 seconds ago      Up 50 seconds       0.0.0.0:32768->80/tcp   admiring_roentgen

$ docker ps --filter publish=80

CONTAINER ID        IMAGE               COMMAND             CREATED              STATUS              PORTS                   NAMES
fc7e477723b7        busybox             "top"               About a minute ago   Up About a minute   0.0.0.0:32768->80/tcp   admiring_roentgen
```

The following filter matches all containers that have exposed TCP port in the range of `8000-8080`:

```console
$ docker ps --filter expose=8000-8080/tcp

CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
9833437217a5        busybox             "top"               21 seconds ago      Up 19 seconds       8080/tcp            dreamy_mccarthy
```

The following filter matches all containers that have exposed UDP port `80`:

```console
$ docker ps --filter publish=80/udp

CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
```

### Format the output (--format)

The formatting option (`--format`) pretty-prints container output using a Go
template.

Valid placeholders for the Go template are listed below:

| Placeholder | Description |
| --- | --- |
| .ID | Container ID |
| .Image | Image ID |
| .Command | Quoted command |
| .CreatedAt | Time when the container was created. |
| .RunningFor | Elapsed time since the container was started. |
| .Ports | Exposed ports. |
| .State | Container status (for example; "created", "running", "exited"). |
| .Status | Container status with details about duration and health-status. |
| .Size | Container disk size. |
| .Names | Container names. |
| .Labels | All labels assigned to the container. |
| .Label | Value of a specific label for this container. For example'{{.Label "com.docker.swarm.cpu"}}' |
| .Mounts | Names of the volumes mounted in this container. |
| .Networks | Names of the networks attached to this container. |

When using the `--format` option, the `ps` command will either output the data
exactly as the template declares or, when using the `table` directive, includes
column headers as well.

The following example uses a template without headers and outputs the `ID` and
`Command` entries separated by a colon (`:`) for all running containers:

```console
$ docker ps --format "{{.ID}}: {{.Command}}"

a87ecb4f327c: /bin/sh -c #(nop) MA
01946d9d34d8: /bin/sh -c #(nop) MA
c1d3b0166030: /bin/sh -c yum -y up
41d50ecd2f57: /bin/sh -c #(nop) MA
```

To list all running containers with their labels in a table format you can use:

```console
$ docker ps --format "table {{.ID}}\t{{.Labels}}"

CONTAINER ID        LABELS
a87ecb4f327c        com.docker.swarm.node=ubuntu,com.docker.swarm.storage=ssd
01946d9d34d8
c1d3b0166030        com.docker.swarm.node=debian,com.docker.swarm.cpu=6
41d50ecd2f57        com.docker.swarm.node=fedora,com.docker.swarm.cpu=3,com.docker.swarm.storage=ssd
```

To list all running containers in JSON format, use the `json` directive:

```console
$ docker ps --format json
{"Command":"\"/docker-entrypoint.…\"","CreatedAt":"2021-03-10 00:15:05 +0100 CET","ID":"a762a2b37a1d","Image":"nginx","Labels":"maintainer=NGINX Docker Maintainers \u003cdocker-maint@nginx.com\u003e","LocalVolumes":"0","Mounts":"","Names":"boring_keldysh","Networks":"bridge","Ports":"80/tcp","RunningFor":"4 seconds ago","Size":"0B","State":"running","Status":"Up 3 seconds"}
```
