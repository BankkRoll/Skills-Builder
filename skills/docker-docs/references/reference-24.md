# docker container pause and more

# docker container pause

# docker container pause

| Description | Pause all processes within one or more containers |
| --- | --- |
| Usage | docker container pause CONTAINER [CONTAINER...] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker pause |

## Description

The `docker pause` command suspends all processes in the specified containers.
On Linux, this uses the freezer cgroup. Traditionally, when suspending a process
the `SIGSTOP` signal is used, which is observable by the process being suspended.
With the freezer cgroup the process is unaware, and unable to capture,
that it is being suspended, and subsequently resumed. On Windows, only Hyper-V
containers can be paused.

See the
[freezer cgroup documentation](https://www.kernel.org/doc/Documentation/cgroup-v1/freezer-subsystem.txt)
for further details.

## Examples

```console
$ docker pause my_container
```

---

# docker container port

# docker container port

| Description | List port mappings or a specific mapping for the container |
| --- | --- |
| Usage | docker container port CONTAINER [PRIVATE_PORT[/PROTO]] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker port |

## Description

List port mappings or a specific mapping for the container

## Examples

### Show all mapped ports

You can find out all the ports mapped by not specifying a `PRIVATE_PORT`, or
just a specific mapping:

```console
$ docker ps

CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS                                            NAMES
b650456536c7        busybox:latest      top                 54 minutes ago      Up 54 minutes       0.0.0.0:1234->9876/tcp, 0.0.0.0:4321->7890/tcp   test

$ docker port test

7890/tcp -> 0.0.0.0:4321
9876/tcp -> 0.0.0.0:1234

$ docker port test 7890/tcp

0.0.0.0:4321

$ docker port test 7890/udp

2014/06/24 11:53:36 Error: No public port '7890/udp' published for test

$ docker port test 7890

0.0.0.0:4321
```

---

# docker container prune

# docker container prune

| Description | Remove all stopped containers |
| --- | --- |
| Usage | docker container prune [OPTIONS] |

## Description

Removes all stopped containers.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --filter |  | Provide filter values (e.g.until=<timestamp>) |
| -f, --force |  | Do not prompt for confirmation |

## Examples

### Prune containers

```console
$ docker container prune
WARNING! This will remove all stopped containers.
Are you sure you want to continue? [y/N] y
Deleted Containers:
4a7f7eebae0f63178aff7eb0aa39cd3f0627a203ab2df258c1a00b456cf20063
f98f9c2aa1eaf727e4ec9c0283bc7d4aa4762fbdba7f26191f26c97f64090360

Total reclaimed space: 212 B
```

### Filtering (--filter)

The filtering flag (`--filter`) format is of "key=value". If there is more
than one filter, then pass multiple flags (e.g., `--filter "foo=bar" --filter "bif=baz"`)

The currently supported filters are:

- until (`<timestamp>`) - only remove containers created before given timestamp
- label (`label=<key>`, `label=<key>=<value>`, `label!=<key>`, or `label!=<key>=<value>`) - only remove containers with (or without, in case `label!=...` is used) the specified labels.

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
which removes containers with the specified labels. The other
format is the `label!=...` (`label!=<key>` or `label!=<key>=<value>`), which removes
containers without the specified labels.

The following removes containers created more than 5 minutes ago:

```console
$ docker ps -a --format 'table {{.ID}}\t{{.Image}}\t{{.Command}}\t{{.CreatedAt}}\t{{.Status}}'

CONTAINER ID        IMAGE               COMMAND             CREATED AT                      STATUS
61b9efa71024        busybox             "sh"                2017-01-04 13:23:33 -0800 PST   Exited (0) 41 seconds ago
53a9bc23a516        busybox             "sh"                2017-01-04 13:11:59 -0800 PST   Exited (0) 12 minutes ago

$ docker container prune --force --filter "until=5m"

Deleted Containers:
53a9bc23a5168b6caa2bfbefddf1b30f93c7ad57f3dec271fd32707497cb9369

Total reclaimed space: 25 B

$ docker ps -a --format 'table {{.ID}}\t{{.Image}}\t{{.Command}}\t{{.CreatedAt}}\t{{.Status}}'

CONTAINER ID        IMAGE               COMMAND             CREATED AT                      STATUS
61b9efa71024        busybox             "sh"                2017-01-04 13:23:33 -0800 PST   Exited (0) 44 seconds ago
```

The following removes containers created before `2017-01-04T13:10:00`:

```console
$ docker ps -a --format 'table {{.ID}}\t{{.Image}}\t{{.Command}}\t{{.CreatedAt}}\t{{.Status}}'

CONTAINER ID        IMAGE               COMMAND             CREATED AT                      STATUS
53a9bc23a516        busybox             "sh"                2017-01-04 13:11:59 -0800 PST   Exited (0) 7 minutes ago
4a75091a6d61        busybox             "sh"                2017-01-04 13:09:53 -0800 PST   Exited (0) 9 minutes ago

$ docker container prune --force --filter "until=2017-01-04T13:10:00"

Deleted Containers:
4a75091a6d618526fcd8b33ccd6e5928ca2a64415466f768a6180004b0c72c6c

Total reclaimed space: 27 B

$ docker ps -a --format 'table {{.ID}}\t{{.Image}}\t{{.Command}}\t{{.CreatedAt}}\t{{.Status}}'

CONTAINER ID        IMAGE               COMMAND             CREATED AT                      STATUS
53a9bc23a516        busybox             "sh"                2017-01-04 13:11:59 -0800 PST   Exited (0) 9 minutes ago
```

---

# docker container rename

# docker container rename

| Description | Rename a container |
| --- | --- |
| Usage | docker container rename CONTAINER NEW_NAME |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker rename |

## Description

The `docker rename` command renames a container.

## Examples

```console
$ docker rename my_container my_new_container
```

---

# docker container restart

# docker container restart

| Description | Restart one or more containers |
| --- | --- |
| Usage | docker container restart [OPTIONS] CONTAINER [CONTAINER...] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker restart |

## Description

Restart one or more containers

## Options

| Option | Default | Description |
| --- | --- | --- |
| -s, --signal |  | Signal to send to the container |
| -t, --timeout |  | Seconds to wait before killing the container |

## Examples

```console
$ docker restart my_container
```

### Stop container with signal (-s, --signal)

The `--signal` flag sends the system call signal to the container to exit.
This signal can be a signal name in the format `SIG<NAME>`, for instance
`SIGKILL`, or an unsigned number that matches a position in the kernel's
syscall table, for instance `9`. Refer to [signal(7)](https://man7.org/linux/man-pages/man7/signal.7.html)
for available signals.

The default signal to use is defined by the image's [StopSignal](https://github.com/opencontainers/image-spec/blob/v1.1.0/config.md),
which can be set through the
[STOPSIGNAL](https://docs.docker.com/reference/dockerfile/#stopsignal)
Dockerfile instruction when building the image, or configured using the
[--stop-signal](https://docs.docker.com/reference/cli/docker/container/run/#stop-signal)
option when creating the container. If no signal is configured for the
container, `SIGTERM` is used as default.

### Stop container with timeout (-t, --timeout)

The `--timeout` flag sets the number of seconds to wait for the container
to stop after sending the pre-defined (see [--signal](#signal)) system call signal.
If the container does not exit after the timeout elapses, it's forcibly killed
with a `SIGKILL` signal.

If you set `--timeout` to `-1`, no timeout is applied, and the daemon
waits indefinitely for the container to exit.

The default timeout can be specified using the
[--stop-timeout](https://docs.docker.com/reference/cli/docker/container/run/#stop-timeout)
option when creating the container. If no default is configured for the container,
the Daemon determines the default, and is 10 seconds for Linux containers, and
30 seconds for Windows containers.

---

# docker container rm

# docker container rm

| Description | Remove one or more containers |
| --- | --- |
| Usage | docker container rm [OPTIONS] CONTAINER [CONTAINER...] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker container removedocker rm |

## Description

Remove one or more containers

## Options

| Option | Default | Description |
| --- | --- | --- |
| -f, --force |  | Force the removal of a running container (uses SIGKILL) |
| -l, --link |  | Remove the specified link |
| -v, --volumes |  | Remove anonymous volumes associated with the container |

## Examples

### Remove a container

This removes the container referenced under the link `/redis`.

```console
$ docker rm /redis

/redis
```

### Remove a link specified with--linkon the default bridge network (--link)

This removes the underlying link between `/webapp` and the `/redis`
containers on the default bridge network, removing all network communication
between the two containers. This does not apply when `--link` is used with
user-specified networks.

```console
$ docker rm --link /webapp/redis

/webapp/redis
```

### Force-remove a running container (--force)

This command force-removes a running container.

```console
$ docker rm --force redis

redis
```

The main process inside the container referenced under the link `redis` will receive
`SIGKILL`, then the container will be removed.

### Remove all stopped containers

Use the
[docker container prune](https://docs.docker.com/reference/cli/docker/container/prune/) command to remove all
stopped containers, or refer to the
[docker system prune](https://docs.docker.com/reference/cli/docker/system/prune/)
command to remove unused containers in addition to other Docker resources, such
as (unused) images and networks.

Alternatively, you can use the `docker ps` with the `-q` / `--quiet` option to
generate a list of container IDs to remove, and use that list as argument for
the `docker rm` command.

Combining commands can be more flexible, but is less portable as it depends
on features provided by the shell, and the exact syntax may differ depending on
what shell is used. To use this approach on Windows, consider using PowerShell
or Bash.

The example below uses `docker ps -q` to print the IDs of all containers that
have exited (`--filter status=exited`), and removes those containers with
the `docker rm` command:

```console
$ docker rm $(docker ps --filter status=exited -q)
```

Or, using the `xargs` Linux utility:

```console
$ docker ps --filter status=exited -q | xargs docker rm
```

### Remove a container and its volumes (-v, --volumes)

```console
$ docker rm --volumes redis
redis
```

This command removes the container and any volumes associated with it.
Note that if a volume was specified with a name, it will not be removed.

### Remove a container and selectively remove volumes

```console
$ docker create -v awesome:/foo -v /bar --name hello redis
hello

$ docker rm -v hello
```

In this example, the volume for `/foo` remains intact, but the volume for
`/bar` is removed. The same behavior holds for volumes inherited with
`--volumes-from`.
