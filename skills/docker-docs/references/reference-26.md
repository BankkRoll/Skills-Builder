# docker container start and more

# docker container start

# docker container start

| Description | Start one or more stopped containers |
| --- | --- |
| Usage | docker container start [OPTIONS] CONTAINER [CONTAINER...] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker start |

## Description

Start one or more stopped containers

## Options

| Option | Default | Description |
| --- | --- | --- |
| -a, --attach |  | Attach STDOUT/STDERR and forward signals |
| --checkpoint |  | experimental (daemon)Restore from this checkpoint |
| --checkpoint-dir |  | experimental (daemon)Use a custom checkpoint storage directory |
| --detach-keys |  | Override the key sequence for detaching a container |
| -i, --interactive |  | Attach container's STDIN |

## Examples

```console
$ docker start my_container
```

---

# docker container stats

# docker container stats

| Description | Display a live stream of container(s) resource usage statistics |
| --- | --- |
| Usage | docker container stats [OPTIONS] [CONTAINER...] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker stats |

## Description

The `docker stats` command returns a live data stream for running containers. To
limit data to one or more specific containers, specify a list of container names
or ids separated by a space. You can specify a stopped container but stopped
containers do not return any data.

If you need more detailed information about a container's resource usage, use
the `/containers/(id)/stats` API endpoint.

> Note
>
> On Linux, the Docker CLI reports memory usage by subtracting cache usage from
> the total memory usage. The API does not perform such a calculation but rather
> provides the total memory usage and the amount from the cache so that clients
> can use the data as needed. The cache usage is defined as the value of
> `total_inactive_file` field in the `memory.stat` file on cgroup v1 hosts.
>
>
>
> On Docker 19.03 and older, the cache usage was defined as the value of `cache`
> field. On cgroup v2 hosts, the cache usage is defined as the value of
> `inactive_file` field.

> Note
>
> The `PIDS` column contains the number of processes and kernel threads created
> by that container. Threads is the term used by Linux kernel. Other equivalent
> terms are "lightweight process" or "kernel task", etc. A large number in the
> `PIDS` column combined with a small number of processes (as reported by `ps`
> or `top`) may indicate that something in the container is creating many threads.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -a, --all |  | Show all containers (default shows just running) |
| --format |  | Format output using a custom template:'table': Print output in table format with column headers (default)'table TEMPLATE': Print output in table format using the given Go template'json': Print in JSON format'TEMPLATE': Print output using the given Go template.Refer tohttps://docs.docker.com/go/formatting/for more information about formatting output with templates |
| --no-stream |  | Disable streaming stats and only pull the first result |
| --no-trunc |  | Do not truncate output |

## Examples

Running `docker stats` on all running containers against a Linux daemon.

```console
$ docker stats

CONTAINER ID        NAME                                    CPU %               MEM USAGE / LIMIT     MEM %               NET I/O             BLOCK I/O           PIDS
b95a83497c91        awesome_brattain                        0.28%               5.629MiB / 1.952GiB   0.28%               916B / 0B           147kB / 0B          9
67b2525d8ad1        foobar                                  0.00%               1.727MiB / 1.952GiB   0.09%               2.48kB / 0B         4.11MB / 0B         2
e5c383697914        test-1951.1.kay7x1lh1twk9c0oig50sd5tr   0.00%               196KiB / 1.952GiB     0.01%               71.2kB / 0B         770kB / 0B          1
4bda148efbc0        random.1.vnc8on831idyr42slu578u3cr      0.00%               1.672MiB / 1.952GiB   0.08%               110kB / 0B          578kB / 0B          2
```

If you don't [specify a format string using--format](#format), the
following columns are shown.

| Column name | Description |
| --- | --- |
| CONTAINER IDandName | the ID and name of the container |
| CPU %andMEM % | the percentage of the host's CPU and memory the container is using |
| MEM USAGE / LIMIT | the total memory the container is using, and the total amount of memory it is allowed to use |
| NET I/O | The amount of data the container has received and sent over its network interface |
| BLOCK I/O | The amount of data the container has written to and read from block devices on the host |
| PIDs | the number of processes or threads the container has created |

Running `docker stats` on multiple containers by name and id against a Linux daemon.

```console
$ docker stats awesome_brattain 67b2525d8ad1

CONTAINER ID        NAME                CPU %               MEM USAGE / LIMIT     MEM %               NET I/O             BLOCK I/O           PIDS
b95a83497c91        awesome_brattain    0.28%               5.629MiB / 1.952GiB   0.28%               916B / 0B           147kB / 0B          9
67b2525d8ad1        foobar              0.00%               1.727MiB / 1.952GiB   0.09%               2.48kB / 0B         4.11MB / 0B         2
```

Running `docker stats` on container with name `nginx` and getting output in `json` format.

```console
$ docker stats nginx --no-stream --format "{{ json . }}"
{"BlockIO":"0B / 13.3kB","CPUPerc":"0.03%","Container":"nginx","ID":"ed37317fbf42","MemPerc":"0.24%","MemUsage":"2.352MiB / 982.5MiB","Name":"nginx","NetIO":"539kB / 606kB","PIDs":"2"}
```

Running `docker stats` with customized format on all (running and stopped) containers.

```console
$ docker stats --all --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}" fervent_panini 5acfcb1b4fd1 humble_visvesvaraya big_heisenberg

CONTAINER                CPU %               MEM USAGE / LIMIT
fervent_panini           0.00%               56KiB / 15.57GiB
5acfcb1b4fd1             0.07%               32.86MiB / 15.57GiB
humble_visvesvaraya      0.00%               0B / 0B
big_heisenberg           0.00%               0B / 0B
```

`humble_visvesvaraya` and `big_heisenberg` are stopped containers in the above example.

Running `docker stats` on all running containers against a Windows daemon.

```powershell
PS E:\> docker stats
CONTAINER ID        CPU %               PRIV WORKING SET    NET I/O             BLOCK I/O
09d3bb5b1604        6.61%               38.21 MiB           17.1 kB / 7.73 kB   10.7 MB / 3.57 MB
9db7aa4d986d        9.19%               38.26 MiB           15.2 kB / 7.65 kB   10.6 MB / 3.3 MB
3f214c61ad1d        0.00%               28.64 MiB           64 kB / 6.84 kB     4.42 MB / 6.93 MB
```

Running `docker stats` on multiple containers by name and id against a Windows daemon.

```powershell
PS E:\> docker ps -a
CONTAINER ID        NAME                IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
3f214c61ad1d        awesome_brattain    nanoserver          "cmd"               2 minutes ago       Up 2 minutes                            big_minsky
9db7aa4d986d        mad_wilson          windowsservercore   "cmd"               2 minutes ago       Up 2 minutes                            mad_wilson
09d3bb5b1604        fervent_panini      windowsservercore   "cmd"               2 minutes ago       Up 2 minutes                            affectionate_easley

PS E:\> docker stats 3f214c61ad1d mad_wilson
CONTAINER ID        NAME                CPU %               PRIV WORKING SET    NET I/O             BLOCK I/O
3f214c61ad1d        awesome_brattain    0.00%               46.25 MiB           76.3 kB / 7.92 kB   10.3 MB / 14.7 MB
9db7aa4d986d        mad_wilson          9.59%               40.09 MiB           27.6 kB / 8.81 kB   17 MB / 20.1 MB
```

### Format the output (--format)

The formatting option (`--format`) pretty prints container output
using a Go template.

Valid placeholders for the Go template are listed below:

| Placeholder | Description |
| --- | --- |
| .Container | Container name or ID (user input) |
| .Name | Container name |
| .ID | Container ID |
| .CPUPerc | CPU percentage |
| .MemUsage | Memory usage |
| .NetIO | Network IO |
| .BlockIO | Block IO |
| .MemPerc | Memory percentage (Not available on Windows) |
| .PIDs | Number of PIDs (Not available on Windows) |

When using the `--format` option, the `stats` command either
outputs the data exactly as the template declares or, when using the
`table` directive, includes column headers as well.

The following example uses a template without headers and outputs the
`Container` and `CPUPerc` entries separated by a colon (`:`) for all images:

```console
$ docker stats --format "{{.Container}}: {{.CPUPerc}}"

09d3bb5b1604: 6.61%
9db7aa4d986d: 9.19%
3f214c61ad1d: 0.00%
```

To list all containers statistics with their name, CPU percentage and memory
usage in a table format you can use:

```console
$ docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"

CONTAINER           CPU %               PRIV WORKING SET
1285939c1fd3        0.07%               796 KiB / 64 MiB
9c76f7834ae2        0.07%               2.746 MiB / 64 MiB
d1ea048f04e4        0.03%               4.583 MiB / 64 MiB
```

The default format is as follows:

On Linux:

```
"table {{.ID}}\t{{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}\t{{.NetIO}}\t{{.BlockIO}}\t{{.PIDs}}"
```

On Windows:

```
"table {{.ID}}\t{{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}"
```

---

# docker container stop

# docker container stop

| Description | Stop one or more running containers |
| --- | --- |
| Usage | docker container stop [OPTIONS] CONTAINER [CONTAINER...] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker stop |

## Description

The main process inside the container will receive `SIGTERM`, and after a grace
period, `SIGKILL`. The first signal can be changed with the `STOPSIGNAL`
instruction in the container's Dockerfile, or the `--stop-signal` option to
`docker run` and `docker create`.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -s, --signal |  | Signal to send to the container |
| -t, --timeout |  | Seconds to wait before killing the container |

## Examples

```console
$ docker stop my_container
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
to stop after sending the pre-defined (see [`--signal`]{#signal)) system call signal.
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

# docker container top

# docker container top

| Description | Display the running processes of a container |
| --- | --- |
| Usage | docker container top CONTAINER [ps OPTIONS] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker top |

## Description

Display the running processes of a container

---

# docker container unpause

# docker container unpause

| Description | Unpause all processes within one or more containers |
| --- | --- |
| Usage | docker container unpause CONTAINER [CONTAINER...] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker unpause |

## Description

The `docker unpause` command un-suspends all processes in the specified containers.
On Linux, it does this using the freezer cgroup.

See the
[freezer cgroup documentation](https://www.kernel.org/doc/Documentation/cgroup-v1/freezer-subsystem.txt)
for further details.

## Examples

```console
$ docker unpause my_container
my_container
```

---

# docker container update

# docker container update

| Description | Update configuration of one or more containers |
| --- | --- |
| Usage | docker container update [OPTIONS] CONTAINER [CONTAINER...] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker update |

## Description

The `docker update` command dynamically updates container configuration.
You can use this command to prevent containers from consuming too many
resources from their Docker host. With a single command, you can place
limits on a single container or on many. To specify more than one container,
provide space-separated list of container names or IDs.

With the exception of the `--kernel-memory` option, you can specify these
options on a running or a stopped container. On kernel version older than
4.6, you can only update `--kernel-memory` on a stopped container or on
a running container with kernel memory initialized.

> Warning
>
> The `docker update` and `docker container update` commands are not supported
> for Windows containers.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --blkio-weight |  | Block IO (relative weight), between 10 and 1000, or 0 to disable (default 0) |
| --cpu-period |  | Limit CPU CFS (Completely Fair Scheduler) period |
| --cpu-quota |  | Limit CPU CFS (Completely Fair Scheduler) quota |
| --cpu-rt-period |  | API 1.25+Limit the CPU real-time period in microseconds |
| --cpu-rt-runtime |  | API 1.25+Limit the CPU real-time runtime in microseconds |
| -c, --cpu-shares |  | CPU shares (relative weight) |
| --cpus |  | API 1.29+Number of CPUs |
| --cpuset-cpus |  | CPUs in which to allow execution (0-3, 0,1) |
| --cpuset-mems |  | MEMs in which to allow execution (0-3, 0,1) |
| -m, --memory |  | Memory limit |
| --memory-reservation |  | Memory soft limit |
| --memory-swap |  | Swap limit equal to memory plus swap: -1 to enable unlimited swap |
| --pids-limit |  | API 1.40+Tune container pids limit (set -1 for unlimited) |
| --restart |  | Restart policy to apply when a container exits |

## Examples

The following sections illustrate ways to use this command.

### Update a container's cpu-shares (--cpu-shares)

To limit a container's cpu-shares to 512, first identify the container
name or ID. You can use `docker ps` to find these values. You can also
use the ID returned from the `docker run` command. Then, do the following:

```console
$ docker update --cpu-shares 512 abebf7571666
```

### Update a container with cpu-shares and memory (-m, --memory)

To update multiple resource configurations for multiple containers:

```console
$ docker update --cpu-shares 512 -m 300M abebf7571666 hopeful_morse
```

### Update a container's kernel memory constraints (--kernel-memory)

You can update a container's kernel memory limit using the `--kernel-memory`
option. On kernel version older than 4.6, this option can be updated on a
running container only if the container was started with `--kernel-memory`.
If the container was started without `--kernel-memory` you need to stop
the container before updating kernel memory.

> Note
>
> The `--kernel-memory` option has been deprecated since Docker 20.10.

For example, if you started a container with this command:

```console
$ docker run -dit --name test --kernel-memory 50M ubuntu bash
```

You can update kernel memory while the container is running:

```console
$ docker update --kernel-memory 80M test
```

If you started a container without kernel memory initialized:

```console
$ docker run -dit --name test2 --memory 300M ubuntu bash
```

Update kernel memory of running container `test2` will fail. You need to stop
the container before updating the `--kernel-memory` setting. The next time you
start it, the container uses the new value.

Kernel version newer than (include) 4.6 does not have this limitation, you
can use `--kernel-memory` the same way as other options.

### Update a container's restart policy (--restart)

You can change a container's restart policy on a running container. The new
restart policy takes effect instantly after you run `docker update` on a
container.

To update restart policy for one or more containers:

```console
$ docker update --restart=on-failure:3 abebf7571666 hopeful_morse
```

Note that if the container is started with `--rm` flag, you cannot update the restart
policy for it. The `AutoRemove` and `RestartPolicy` are mutually exclusive for the
container.

---

# docker container wait

# docker container wait

| Description | Block until one or more containers stop, then print their exit codes |
| --- | --- |
| Usage | docker container wait CONTAINER [CONTAINER...] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker wait |

## Description

Block until one or more containers stop, then print their exit codes

## Examples

Start a container in the background.

```console
$ docker run -dit --name=my_container ubuntu bash
```

Run `docker wait`, which should block until the container exits.

```console
$ docker wait my_container
```

In another terminal, stop the first container. The `docker wait` command above
returns the exit code.

```console
$ docker stop my_container
```

This is the same `docker wait` command from above, but it now exits, returning
`0`.

```console
$ docker wait my_container

0
```

---

# docker container

# docker container

| Description | Manage containers |
| --- | --- |
| Usage | docker container |

## Description

Manage containers.

## Subcommands

| Command | Description |
| --- | --- |
| docker container attach | Attach local standard input, output, and error streams to a running container |
| docker container commit | Create a new image from a container's changes |
| docker container cp | Copy files/folders between a container and the local filesystem |
| docker container create | Create a new container |
| docker container diff | Inspect changes to files or directories on a container's filesystem |
| docker container exec | Execute a command in a running container |
| docker container export | Export a container's filesystem as a tar archive |
| docker container inspect | Display detailed information on one or more containers |
| docker container kill | Kill one or more running containers |
| docker container logs | Fetch the logs of a container |
| docker container ls | List containers |
| docker container pause | Pause all processes within one or more containers |
| docker container port | List port mappings or a specific mapping for the container |
| docker container prune | Remove all stopped containers |
| docker container rename | Rename a container |
| docker container restart | Restart one or more containers |
| docker container rm | Remove one or more containers |
| docker container run | Create and run a new container from an image |
| docker container start | Start one or more stopped containers |
| docker container stats | Display a live stream of container(s) resource usage statistics |
| docker container stop | Stop one or more running containers |
| docker container top | Display the running processes of a container |
| docker container unpause | Unpause all processes within one or more containers |
| docker container update | Update configuration of one or more containers |
| docker container wait | Block until one or more containers stop, then print their exit codes |

---

# docker context create

# docker context create

| Description | Create a context |
| --- | --- |
| Usage | docker context create [OPTIONS] CONTEXT |

## Description

Creates a new `context`. This lets you switch the daemon your `docker` CLI
connects to.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --description |  | Description of the context |
| --docker |  | set the docker endpoint |
| --from |  | create context from a named context |

## Examples

### Create a context with a Docker endpoint (--docker)

Use the `--docker` flag to create a context with a custom endpoint. The
following example creates a context named `my-context` with a docker endpoint
of `/var/run/docker.sock`:

```console
$ docker context create \
    --docker host=unix:///var/run/docker.sock \
    my-context
```

### Create a context based on an existing context (--from)

Use the `--from=<context-name>` option to create a new context from
an existing context. The example below creates a new context named `my-context`
from the existing context `existing-context`:

```console
$ docker context create --from existing-context my-context
```

If the `--from` option isn't set, the `context` is created from the current context:

```console
$ docker context create my-context
```

This can be used to create a context out of an existing `DOCKER_HOST` based script:

```console
$ source my-setup-script.sh
$ docker context create my-context
```

To source the `docker` endpoint configuration from an existing context
use the `--docker from=<context-name>` option. The example below creates a
new context named `my-context` using the docker endpoint configuration from
the existing context `existing-context`:

```console
$ docker context create \
    --docker from=existing-context \
    my-context
```

Docker endpoints configurations, as well as the description can be modified with
`docker context update`.

Refer to the
[docker context updatereference](https://docs.docker.com/reference/cli/docker/context/update/) for details.

---

# docker context export

# docker context export

| Description | Export a context to a tar archive FILE or a tar stream on STDOUT. |
| --- | --- |
| Usage | docker context export [OPTIONS] CONTEXT [FILE|-] |

## Description

Exports a context to a file that can then be used with `docker context import`.

The default output filename is `<CONTEXT>.dockercontext`. To export to `STDOUT`,
use `-` as filename, for example:

```console
$ docker context export my-context -
```

---

# docker context import

# docker context import

| Description | Import a context from a tar or zip file |
| --- | --- |
| Usage | docker context import CONTEXT FILE|- |

## Description

Imports a context previously exported with `docker context export`. To import
from stdin, use a hyphen (`-`) as filename.

---

# docker context inspect

# docker context inspect

| Description | Display detailed information on one or more contexts |
| --- | --- |
| Usage | docker context inspect [OPTIONS] [CONTEXT] [CONTEXT...] |

## Description

Inspects one or more contexts.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -f, --format |  | Format output using a custom template:'json': Print in JSON format'TEMPLATE': Print output using the given Go template.Refer tohttps://docs.docker.com/go/formatting/for more information about formatting output with templates |

## Examples

### Inspect a context by name

```console
$ docker context inspect "local+aks"

[
  {
    "Name": "local+aks",
    "Metadata": {
      "Description": "Local Docker Engine",
      "StackOrchestrator": "swarm"
    },
    "Endpoints": {
      "docker": {
        "Host": "npipe:////./pipe/docker_engine",
        "SkipTLSVerify": false
      }
    },
    "TLSMaterial": {},
    "Storage": {
      "MetadataPath": "C:\\Users\\simon\\.docker\\contexts\\meta\\cb6d08c0a1bfa5fe6f012e61a442788c00bed93f509141daff05f620fc54ddee",
      "TLSPath": "C:\\Users\\simon\\.docker\\contexts\\tls\\cb6d08c0a1bfa5fe6f012e61a442788c00bed93f509141daff05f620fc54ddee"
    }
  }
]
```

---

# docker context ls

# docker context ls

| Description | List contexts |
| --- | --- |
| Usage | docker context ls [OPTIONS] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker context list |

## Description

List contexts

## Options

| Option | Default | Description |
| --- | --- | --- |
| --format |  | Format output using a custom template:'table': Print output in table format with column headers (default)'table TEMPLATE': Print output in table format using the given Go template'json': Print in JSON format'TEMPLATE': Print output using the given Go template.Refer tohttps://docs.docker.com/go/formatting/for more information about formatting output with templates |
| -q, --quiet |  | Only show context names |

## Examples

Use `docker context ls` to print all contexts. The currently active context is
indicated with an `*`:

```console
$ docker context ls

NAME                DESCRIPTION                               DOCKER ENDPOINT                      ORCHESTRATOR
default *           Current DOCKER_HOST based configuration   unix:///var/run/docker.sock          swarm
production                                                    tcp:///prod.corp.example.com:2376
staging                                                       tcp:///stage.corp.example.com:2376
```

---

# docker context rm

# docker context rm

| Description | Remove one or more contexts |
| --- | --- |
| Usage | docker context rm CONTEXT [CONTEXT...] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker context remove |

## Description

Remove one or more contexts

## Options

| Option | Default | Description |
| --- | --- | --- |
| -f, --force |  | Force the removal of a context in use |

---

# docker context show

# docker context show

| Description | Print the name of the current context |
| --- | --- |
| Usage | docker context show |

## Description

Print the name of the current context, possibly set by `DOCKER_CONTEXT` environment
variable or `--context` global option.

## Examples

### Print the current context

The following example prints the currently used
[docker context](https://docs.docker.com/reference/cli/docker/context/):

```console
$ docker context show'
default
```

As an example, this output can be used to dynamically change your shell prompt
to indicate your active context. The example below illustrates how this output
could be used when using Bash as your shell.

Declare a function to obtain the current context in your `~/.bashrc`, and set
this command as your `PROMPT_COMMAND`

```console
function docker_context_prompt() {
        PS1="context: $(docker context show)> "
}

PROMPT_COMMAND=docker_context_prompt
```

After reloading the `~/.bashrc`, the prompt now shows the currently selected
`docker context`:

```console
$ source ~/.bashrc
context: default> docker context create --docker host=unix:///var/run/docker.sock my-context
my-context
Successfully created context "my-context"
context: default> docker context use my-context
my-context
Current context is now "my-context"
context: my-context> docker context use default
default
Current context is now "default"
context: default>
```

---

# docker context update

# docker context update

| Description | Update a context |
| --- | --- |
| Usage | docker context update [OPTIONS] CONTEXT |

## Description

Updates an existing `context`.
See
[context create](https://docs.docker.com/reference/cli/docker/context/create/).

## Options

| Option | Default | Description |
| --- | --- | --- |
| --description |  | Description of the context |
| --docker |  | set the docker endpoint |

## Examples

### Update an existing context

```console
$ docker context update \
    --description "some description" \
    --docker "host=tcp://myserver:2376,ca=~/ca-file,cert=~/cert-file,key=~/key-file" \
    my-context
```

---

# docker context use

# docker context use

| Description | Set the current docker context |
| --- | --- |
| Usage | docker context use CONTEXT |

## Description

Set the default context to use, when `DOCKER_HOST`, `DOCKER_CONTEXT` environment
variables and `--host`, `--context` global options aren't set.
To disable usage of contexts, you can use the special `default` context.

---

# docker context

# docker context

| Description | Manage contexts |
| --- | --- |
| Usage | docker context |

## Description

Manage contexts.

## Subcommands

| Command | Description |
| --- | --- |
| docker context create | Create a context |
| docker context export | Export a context to a tar archive FILE or a tar stream on STDOUT. |
| docker context import | Import a context from a tar or zip file |
| docker context inspect | Display detailed information on one or more contexts |
| docker context ls | List contexts |
| docker context rm | Remove one or more contexts |
| docker context show | Print the name of the current context |
| docker context update | Update a context |
| docker context use | Set the current docker context |

---

# docker debug

# docker debug

| Description | Get a shell into any container or image. An alternative to debugging with `docker exec`. |
| --- | --- |
| Usage | debug [OPTIONS] {CONTAINER|IMAGE} |

Requires: Docker Desktop 4.49 and later. For Docker Desktop versions 4.48.0 and earlier, you must have a Pro, Team, or Business subscription

## Description

Docker Debug is a CLI command that helps you follow best practices by keeping your images small and secure.
With Docker Debug, you can debug your images while they contain the bare minimum to run your application.
It does this by letting you create and work with slim images or containers that are often difficult to debug because all tools have been removed.
For example, while typical debug approaches like `docker exec -it my-app bash` may not work on a slim container, `docker debug` will work.

With `docker debug` you can get a debug shell into any container or image, even if they don't contain a shell.
You don't need to modify the image to use Docker Debug.
However, using Docker Debug still won't modify your image.
Docker Debug brings its own toolbox that you can easily customize.
The toolbox comes with many standard Linux tools pre-installed, such as `vim`, `nano`, `htop`, and `curl`.
Use the builtin `install` command to add additional tools available on [https://search.nixos.org/packages](https://search.nixos.org/packages).
Docker Debug supports `bash`, `fish`, and `zsh`.
By default it tries to auto-detect your shell.

Custom builtin tools:

- `install [tool1] [tool2]`: Add Nix packages from: [https://search.nixos.org/packages](https://search.nixos.org/packages), see [example](#managing-your-toolbox-using-the-install-command).
- `uninstall [tool1] [tool2]`: Uninstall Nix packages.
- `entrypoint`: Print, lint, or run the entrypoint, see [example](#understanding-the-default-startup-command-of-a-container-entry-points).
- `builtins`: Show custom builtin tools.

> Note
>
> For images and stopped containers, all changes are discarded when leaving the shell.
> At no point, do changes affect the actual image or container.
> When accessing running or paused containers, all filesystem changes are directly visible to the container.
> The `/nix` directory is never visible to the actual image or container.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --shell | auto | Select a shell. Supported:bash,fish,zsh,auto. |
| -c, --command |  | Evaluate the specified commands instead of starting an interactive session, seeexample. |
| --host |  | Daemon docker socket to connect to. E.g.:ssh://root@example.org,unix:///some/path/docker.sock, seeexample. |

## Examples

### Debugging containers that have no shell (slim containers)

The `hello-world` image is very simple and only contains the `/hello` binary.
It's a good example of a slim image.
There are no other tools and no shell.

Run a container from the `hello-world` image:

```console
$ docker run --name my-app hello-world
```

The container exits immediately. To get a debug shell inside, run:

```console
$ docker debug my-app
```

The debug shell allows you to inspect the filesystem:

```console
docker > ls
dev  etc  hello  nix  proc  sys
```

The file `/hello` is the binary that was executed when running the container.
You can confirm this by running it directly:

```console
docker > /hello
```

After running the binary, it produces the same output.

### Debugging (slim) images

You can debug images directly by running:

```console
$ docker debug hello-world
...
docker > ls
dev  etc  hello  nix  proc  sys
```

You don't even need to pull the image as `docker debug` will do this automatically like the `docker run` command.

### Modifying files of a running container

Docker debug lets you modify files in any running container.
The toolbox comes with `vim` and `nano` pre-installed.

Run an nginx container and change the default `index.html`:

```console
$ docker run -d --name web-app -p 8080:80 nginx
d3d6074d0ea901c96cac8e49e6dad21359616bef3dc0623b3c2dfa536c31dfdb
```

To confirm nginx is running, open a browser and navigate to http://localhost:8080.
You should see the default nginx page.
Now, change it using vim:

```console
vim /usr/share/nginx/html/index.html
```

Change the title to "Welcome to my app!" and save the file.
Now, reload the page in the browser and you should see the updated page.

### Managing your toolbox using theinstallcommand

The builtin `install` command lets you add any tool from [https://search.nixos.org/packages](https://search.nixos.org/packages) to the toolbox.
Keep in mind adding a tool never modifies the actual image or container.
Tools get added to only your toolbox.
Run `docker debug` and then install `nmap`:

```console
$ docker debug nginx
...
docker > install nmap
Tip: You can install any package available at: https://search.nixos.org/packages.
installing 'nmap-7.93'
these 2 paths will be fetched (5.58 MiB download, 26.27 MiB unpacked):
/nix/store/brqjf4i23fagizaq2gn4d6z0f406d0kg-lua-5.3.6
/nix/store/xqd17rhgmn6pg85a3g18yqxpcya6d06r-nmap-7.93
copying path '/nix/store/brqjf4i23fagizaq2gn4d6z0f406d0kg-lua-5.3.6' from 'https://cache.nixos.org'...
copying path '/nix/store/xqd17rhgmn6pg85a3g18yqxpcya6d06r-nmap-7.93' from 'https://cache.nixos.org'...
building '/nix/store/k8xw5wwarh8dc1dvh5zx8rlwamxfsk3d-user-environment.drv'...

docker > nmap --version
Nmap version 7.93 ( https://nmap.org )
Platform: x86_64-unknown-linux-gnu
Compiled with: liblua-5.3.6 openssl-3.0.11 libssh2-1.11.0 nmap-libz-1.2.12 libpcre-8.45 libpcap-1.10.4 nmap-libdnet-1.12 ipv6
Compiled without:
Available nsock engines: epoll poll select
```

You can confirm `nmap` is now part of your toolbox by getting a debug shell into a different image:

```console
$ docker debug hello-world
...
docker > nmap --version

Nmap version 7.93 ( https://nmap.org )
Platform: x86_64-unknown-linux-gnu
Compiled with: liblua-5.3.6 openssl-3.0.11 libssh2-1.11.0 nmap-libz-1.2.12 libpcre-8.45 libpcap-1.10.4 nmap-libdnet-1.12 ipv6
Compiled without:
Available nsock engines: epoll poll select

docker > exit
```

`nmap` is still there.

### Understanding the default startup command of a container (entry points)

Docker Debug comes with a builtin tool, `entrypoint`.
Enter the `hello-world` image and confirm the entrypoint is `/hello`:

```console
$ docker debug hello-world
...
docker > entrypoint --print
/hello
```

The `entrypoint` command evaluates the `ENTRYPOINT` and `CMD` statement of the underlying image
and lets you print, lint, or run the resulting entrypoint.
However, it can be difficult to understand all the corner cases from
[Understand how CMD and ENTRYPOINT interact](https://docs.docker.com/reference/dockerfile/#understand-how-cmd-and-entrypoint-interact).
In these situations, `entrypoint` can help.

Use `entrypoint` to investigate what actually happens when you run a container from the Nginx image:

```console
$ docker debug nginx
...
docker > entrypoint
Understand how ENTRYPOINT/CMD work and if they are set correctly.
From CMD in Dockerfile:
 ['nginx', '-g', 'daemon off;']

From ENTRYPOINT in Dockerfile:
 ['/docker-entrypoint.sh']

By default, any container from this image will be started with following   command:

/docker-entrypoint.sh nginx -g daemon off;

path: /docker-entrypoint.sh
args: nginx -g daemon off;
cwd:
PATH: /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

Lint results:
 PASS: '/docker-entrypoint.sh' found
 PASS: no mixing of shell and exec form
 PASS: no double use of shell form

Docs:
- https://docs.docker.com/reference/dockerfile/#cmd
- https://docs.docker.com/reference/dockerfile/#entrypoint
- https://docs.docker.com/reference/dockerfile/#understand-how-cmd-and-entrypoint-interact
```

The output tells you that on startup of the nginx image, a script `/docker-entrypoint.sh` is executed with the arguments `nginx -g daemon off;`.
You can test the entrypoint by using the `--run` option:

```console
$ docker debug nginx
...
docker > entrypoint --run
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
/docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
/docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
/docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
/docker-entrypoint.sh: Configuration complete; ready for start up
2024/01/19 17:34:39 [notice] 50#50: using the "epoll" event method
2024/01/19 17:34:39 [notice] 50#50: nginx/1.25.3
2024/01/19 17:34:39 [notice] 50#50: built by gcc 12.2.0 (Debian 12.2.0-14)
2024/01/19 17:34:39 [notice] 50#50: OS: Linux 5.15.133.1-microsoft-standard-WSL2
2024/01/19 17:34:39 [notice] 50#50: getrlimit(RLIMIT_NOFILE): 1048576:1048576
2024/01/19 17:34:39 [notice] 50#50: start worker processes
2024/01/19 17:34:39 [notice] 50#50: start worker process 77
...
```

This starts nginx in your debug shell without having to actually run a container.
You can shutdown nginx by pressing `Ctrl`+`C`.

### Running commands directly (e.g., for scripting)

Use the `--command` option to evaluate a command directly instead of starting an interactive session.
For example, this is similar to `bash -c "arg1 arg2 ..."`.
The following example runs the `cat` command in the nginx image without starting an interactive session.

```console
$ docker debug --command "cat /usr/share/nginx/html/index.html" nginx

<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```

### Remote debugging using the --host option

The following examples shows how to use the `--host` option. The first example uses SSH to connect to a remote Docker instance at `example.org` as the `root` user, and get a shell into the `my-container` container.

```console
$ docker debug --host ssh://root@example.org my-container
```

The following example connects to a different local Docker Engine, and gets a
shell into the `my-container` container.

```console
$ docker debug --host=unix:///some/path/docker.sock my-container
```

---

# docker desktop disable model

# docker desktop disable model-runner

| Description | Disable Docker Model Runner |
| --- | --- |
| Usage | docker desktop disable model-runner |

## Description

Disable Docker Model Runner

---

# docker desktop disable

# docker desktop disable

| Description | Disable a feature |
| --- | --- |

## Description

Disable an individual feature

## Subcommands

| Command | Description |
| --- | --- |
| docker desktop disable model-runner | Disable Docker Model Runner |

---

# docker desktop enable model

# docker desktop enable model-runner

| Description | Manage Docker Model Runner settings |
| --- | --- |
| Usage | docker desktop enable model-runner [OPTIONS] |

## Description

Enable and manage Docker Model Runner settings used by 'docker model'

## Options

| Option | Default | Description |
| --- | --- | --- |
| --no-tcp |  | Disable TCP connection. Cannot be used with --tcp. |
| --tcp | 12434 | Enable or change TCP port for connection (1-65535). Cannot be used with --no-tcp. |
| --cors | all | CORS configuration. Can beall,none, or comma-separated list of allowed origins. |

---

# docker desktop enable

# docker desktop enable

| Description | Enable a feature |
| --- | --- |

## Description

Enable or manage an individual feature

## Subcommands

| Command | Description |
| --- | --- |
| docker desktop enable model-runner | Manage Docker Model Runner settings |

---

# docker desktop engine ls

# docker desktop engine ls

| Description | List available engines (Windows only) |
| --- | --- |
| Usage | docker desktop engine ls |

## Options

| Option | Default | Description |
| --- | --- | --- |
| --format | pretty | Format the output. Accepted values are: pretty, json |
