# docker service inspect and more

# docker service inspect

# docker service inspect

| Description | Display detailed information on one or more services |
| --- | --- |
| Usage | docker service inspect [OPTIONS] SERVICE [SERVICE...] |

Swarm
This command works with the Swarm orchestrator.

## Description

Inspects the specified service.

By default, this renders all results in a JSON array. If a format is specified,
the given template will be executed for each result.

Go's [text/template](https://pkg.go.dev/text/template) package
describes all the details of the format.

> Note
>
> This is a cluster management command, and must be executed on a swarm
> manager node. To learn about managers and workers, refer to the
> [Swarm mode section](https://docs.docker.com/engine/swarm/) in the
> documentation.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -f, --format |  | Format output using a custom template:'json': Print in JSON format'TEMPLATE': Print output using the given Go template.Refer tohttps://docs.docker.com/go/formatting/for more information about formatting output with templates |
| --pretty |  | Print the information in a human friendly format |

## Examples

### Inspect a service by name or ID

You can inspect a service, either by its *name*, or *ID*

For example, given the following service;

```console
$ docker service ls
ID            NAME   MODE        REPLICAS  IMAGE
dmu1ept4cxcf  redis  replicated  3/3       redis:7.4.1
```

Both `docker service inspect redis`, and `docker service inspect dmu1ept4cxcf`
produce the same result:

```console
$ docker service inspect redis
```

The output is in JSON format, for example:

```json
[
  {
    "ID": "dmu1ept4cxcfe8k8lhtux3ro3",
    "Version": {
      "Index": 12
    },
    "CreatedAt": "2016-06-17T18:44:02.558012087Z",
    "UpdatedAt": "2016-06-17T18:44:02.558012087Z",
    "Spec": {
      "Name": "redis",
      "TaskTemplate": {
        "ContainerSpec": {
          "Image": "redis:7.4.1"
        },
        "Resources": {
          "Limits": {},
          "Reservations": {}
        },
        "RestartPolicy": {
          "Condition": "any",
          "MaxAttempts": 0
        },
        "Placement": {}
      },
      "Mode": {
        "Replicated": {
          "Replicas": 1
        }
      },
      "UpdateConfig": {},
      "EndpointSpec": {
        "Mode": "vip"
      }
    },
    "Endpoint": {
      "Spec": {}
    }
  }
]
```

```console
$ docker service inspect dmu1ept4cxcf

[
  {
    "ID": "dmu1ept4cxcfe8k8lhtux3ro3",
    "Version": {
      "Index": 12
    },
    ...
  }
]
```

### Formatting (--pretty)

You can print the inspect output in a human-readable format instead of the default
JSON output, by using the `--pretty` option:

```console
$ docker service inspect --pretty frontend

ID:     c8wgl7q4ndfd52ni6qftkvnnp
Name:   frontend
Labels:
 - org.example.projectname=demo-app
Service Mode:   REPLICATED
 Replicas:      5
Placement:
UpdateConfig:
 Parallelism:   0
 On failure:    pause
 Max failure ratio: 0
ContainerSpec:
 Image:     nginx:alpine
Resources:
Networks:   net1
Endpoint Mode:  vip
Ports:
 PublishedPort = 4443
  Protocol = tcp
  TargetPort = 443
  PublishMode = ingress
```

You can also use `--format pretty` for the same effect.

### Format the output (--format)

You can use the --format option to obtain specific information about a
The `--format` option can be used to obtain specific information about a
service. For example, the following command outputs the number of replicas
of the "redis" service.

```console
$ docker service inspect --format='{{.Spec.Mode.Replicated.Replicas}}' redis

10
```

---

# docker service logs

# docker service logs

| Description | Fetch the logs of a service or task |
| --- | --- |
| Usage | docker service logs [OPTIONS] SERVICE|TASK |

Swarm
This command works with the Swarm orchestrator.

## Description

The `docker service logs` command batch-retrieves logs present at the time of execution.

> Note
>
> This is a cluster management command, and must be executed on a swarm
> manager node. To learn about managers and workers, refer to the
> [Swarm mode section](https://docs.docker.com/engine/swarm/) in the
> documentation.

The `docker service logs` command can be used with either the name or ID of a
service, or with the ID of a task. If a service is passed, it will display logs
for all of the containers in that service. If a task is passed, it will only
display logs from that particular task.

> Note
>
> This command is only functional for services that are started with
> the `json-file` or `journald` logging driver.

For more information about selecting and configuring logging drivers, refer to
[Configure logging drivers](https://docs.docker.com/engine/logging/configure/).

The `docker service logs --follow` command will continue streaming the new output from
the service's `STDOUT` and `STDERR`.

Passing a negative number or a non-integer to `--tail` is invalid and the
value is set to `all` in that case.

The `docker service logs --timestamps` command will add an [RFC3339Nano timestamp](https://pkg.go.dev/time#RFC3339Nano)
, for example `2014-09-16T06:17:46.000000000Z`, to each
log entry. To ensure that the timestamps are aligned the
nano-second part of the timestamp will be padded with zero when necessary.

The `docker service logs --details` command will add on extra attributes, such as
environment variables and labels, provided to `--log-opt` when creating the
service.

The `--since` option shows only the service logs generated after
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
| --details |  | API 1.30+Show extra details provided to logs |
| -f, --follow |  | Follow log output |
| --no-resolve |  | Do not map IDs to Names in output |
| --no-task-ids |  | Do not include task IDs in output |
| --no-trunc |  | Do not truncate output |
| --raw |  | API 1.30+Do not neatly format logs |
| --since |  | Show logs since timestamp (e.g.2013-01-02T13:23:37Z) or relative (e.g.42mfor 42 minutes) |
| -n, --tail | all | Number of lines to show from the end of the logs |
| -t, --timestamps |  | Show timestamps |

---

# docker service ls

# docker service ls

| Description | List services |
| --- | --- |
| Usage | docker service ls [OPTIONS] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker service list |

Swarm
This command works with the Swarm orchestrator.

## Description

This command lists services that are running in the swarm.

> Note
>
> This is a cluster management command, and must be executed on a swarm
> manager node. To learn about managers and workers, refer to the
> [Swarm mode section](https://docs.docker.com/engine/swarm/) in the
> documentation.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -f, --filter |  | Filter output based on conditions provided |
| --format |  | Format output using a custom template:'table': Print output in table format with column headers (default)'table TEMPLATE': Print output in table format using the given Go template'json': Print in JSON format'TEMPLATE': Print output using the given Go template.Refer tohttps://docs.docker.com/go/formatting/for more information about formatting output with templates |
| -q, --quiet |  | Only display IDs |

## Examples

On a manager node:

```console
$ docker service ls

ID            NAME      MODE            REPLICAS             IMAGE
c8wgl7q4ndfd  frontend  replicated      5/5                  nginx:alpine
dmu1ept4cxcf  redis     replicated      3/3                  redis:7.4.1
iwe3278osahj  mongo     global          7/7                  mongo:3.3
hh08h9uu8uwr  job       replicated-job  1/1 (3/5 completed)  nginx:latest
```

The `REPLICAS` column shows both the actual and desired number of tasks for
the service. If the service is in `replicated-job` or `global-job`, it will
additionally show the completion status of the job as completed tasks over
total tasks the job will execute.

### Filtering (--filter)

The filtering flag (`-f` or `--filter`) format is of "key=value". If there is more
than one filter, then pass multiple flags (e.g., `--filter "foo=bar" --filter "bif=baz"`).

The currently supported filters are:

- [id](https://docs.docker.com/reference/cli/docker/service/ls/#id)
- [label](https://docs.docker.com/reference/cli/docker/service/ls/#label)
- [mode](https://docs.docker.com/reference/cli/docker/service/ls/#mode)
- [name](https://docs.docker.com/reference/cli/docker/service/ls/#name)

#### id

The `id` filter matches all or the prefix of a service's ID.

The following filter matches services with an ID starting with `0bcjw`:

```console
$ docker service ls -f "id=0bcjw"
ID            NAME   MODE        REPLICAS  IMAGE
0bcjwfh8ychr  redis  replicated  1/1       redis:7.4.1
```

#### label

The `label` filter matches services based on the presence of a `label` alone or
a `label` and a value.

The following filter matches all services with a `project` label regardless of
its value:

```console
$ docker service ls --filter label=project
ID            NAME       MODE        REPLICAS  IMAGE
01sl1rp6nj5u  frontend2  replicated  1/1       nginx:alpine
36xvvwwauej0  frontend   replicated  5/5       nginx:alpine
74nzcxxjv6fq  backend    replicated  3/3       redis:7.4.1
```

The following filter matches only services with the `project` label with the
`project-a` value.

```console
$ docker service ls --filter label=project=project-a
ID            NAME      MODE        REPLICAS  IMAGE
36xvvwwauej0  frontend  replicated  5/5       nginx:alpine
74nzcxxjv6fq  backend   replicated  3/3       redis:7.4.1
```

#### mode

The `mode` filter matches on the mode (either `replicated` or `global`) of a service.

The following filter matches only `global` services.

```console
$ docker service ls --filter mode=global
ID                  NAME                MODE                REPLICAS            IMAGE
w7y0v2yrn620        top                 global              1/1                 busybox
```

#### name

The `name` filter matches on all or the prefix of a service's name.

The following filter matches services with a name starting with `redis`.

```console
$ docker service ls --filter name=redis
ID            NAME   MODE        REPLICAS  IMAGE
0bcjwfh8ychr  redis  replicated  1/1       redis:7.4.1
```

### Format the output (--format)

The formatting options (`--format`) pretty-prints services output
using a Go template.

Valid placeholders for the Go template are listed below:

| Placeholder | Description |
| --- | --- |
| .ID | Service ID |
| .Name | Service name |
| .Mode | Service mode (replicated, global) |
| .Replicas | Service replicas |
| .Image | Service image |
| .Ports | Service ports published in ingress mode |

When using the `--format` option, the `service ls` command will either
output the data exactly as the template declares or, when using the
`table` directive, includes column headers as well.

The following example uses a template without headers and outputs the
`ID`, `Mode`, and `Replicas` entries separated by a colon (`:`) for all services:

```console
$ docker service ls --format "{{.ID}}: {{.Mode}} {{.Replicas}}"

0zmvwuiu3vue: replicated 10/10
fm6uf97exkul: global 5/5
```

To list all services in JSON format, use the `json` directive:

```console
$ docker service ls --format json
{"ID":"ssniordqolsi","Image":"hello-world:latest","Mode":"replicated","Name":"hello","Ports":"","Replicas":"0/1"}
```

---

# docker service ps

# docker service ps

| Description | List the tasks of one or more services |
| --- | --- |
| Usage | docker service ps [OPTIONS] SERVICE [SERVICE...] |

Swarm
This command works with the Swarm orchestrator.

## Description

Lists the tasks that are running as part of the specified services.

> Note
>
> This is a cluster management command, and must be executed on a swarm
> manager node. To learn about managers and workers, refer to the
> [Swarm mode section](https://docs.docker.com/engine/swarm/) in the
> documentation.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -f, --filter |  | Filter output based on conditions provided |
| --format |  | Pretty-print tasks using a Go template |
| --no-resolve |  | Do not map IDs to Names |
| --no-trunc |  | Do not truncate output |
| -q, --quiet |  | Only display task IDs |

## Examples

### List the tasks that are part of a service

The following command shows all the tasks that are part of the `redis` service:

```console
$ docker service ps redis

ID             NAME      IMAGE        NODE      DESIRED STATE  CURRENT STATE          ERROR  PORTS
0qihejybwf1x   redis.1   redis:7.4.0  manager1  Running        Running 8 seconds
bk658fpbex0d   redis.2   redis:7.4.0  worker2   Running        Running 9 seconds
5ls5s5fldaqg   redis.3   redis:7.4.0  worker1   Running        Running 9 seconds
8ryt076polmc   redis.4   redis:7.4.0  worker1   Running        Running 9 seconds
1x0v8yomsncd   redis.5   redis:7.4.0  manager1  Running        Running 8 seconds
71v7je3el7rr   redis.6   redis:7.4.0  worker2   Running        Running 9 seconds
4l3zm9b7tfr7   redis.7   redis:7.4.0  worker2   Running        Running 9 seconds
9tfpyixiy2i7   redis.8   redis:7.4.0  worker1   Running        Running 9 seconds
3w1wu13yupln   redis.9   redis:7.4.0  manager1  Running        Running 8 seconds
8eaxrb2fqpbn   redis.10  redis:7.4.0  manager1  Running        Running 8 seconds
```

In addition to running tasks, the output also shows the task history. For
example, after updating the service to use the `redis:7.4.1` image, the output
may look like this:

```console
$ docker service ps redis

ID            NAME         IMAGE        NODE      DESIRED STATE  CURRENT STATE                   ERROR  PORTS
50qe8lfnxaxk  redis.1      redis:7.4.1  manager1  Running        Running 6 seconds ago
ky2re9oz86r9   \_ redis.1  redis:7.4.0  manager1  Shutdown       Shutdown 8 seconds ago
3s46te2nzl4i  redis.2      redis:7.4.1  worker2   Running        Running less than a second ago
nvjljf7rmor4   \_ redis.2  redis:7.4.1  worker2   Shutdown       Rejected 23 seconds ago        "No such image: redis@sha256:6…"
vtiuz2fpc0yb   \_ redis.2  redis:7.4.0  worker2   Shutdown       Shutdown 1 second ago
jnarweeha8x4  redis.3      redis:7.4.1  worker1   Running        Running 3 seconds ago
vs448yca2nz4   \_ redis.3  redis:7.4.0  worker1   Shutdown       Shutdown 4 seconds ago
jf1i992619ir  redis.4      redis:7.4.1  worker1   Running        Running 10 seconds ago
blkttv7zs8ee   \_ redis.4  redis:7.4.0  worker1   Shutdown       Shutdown 11 seconds ago
```

The number of items in the task history is determined by the
`--task-history-limit` option that was set when initializing the swarm. You can
change the task history retention limit using the
[docker swarm update](https://docs.docker.com/reference/cli/docker/swarm/update/) command.

When deploying a service, docker resolves the digest for the service's image,
and pins the service to that digest. The digest is not shown by default, but is
printed if `--no-trunc` is used. The `--no-trunc` option also shows the
non-truncated task ID, and error messages, as can be seen in the following
example:

```console
$ docker service ps --no-trunc redis

ID                          NAME         IMAGE                                                                                NODE      DESIRED STATE  CURRENT STATE            ERROR                                                                                           PORTS
50qe8lfnxaxksi9w2a704wkp7   redis.1      redis:7.4.1@sha256:6a692a76c2081888b589e26e6ec835743119fe453d67ecf03df7de5b73d69842  manager1  Running        Running 5 minutes ago
ky2re9oz86r9556i2szb8a8af   \_ redis.1   redis:7.4.0@sha256:f8829e00d95672c48c60f468329d6693c4bdd28d1f057e755f8ba8b40008682e  worker2   Shutdown       Shutdown 5 minutes ago
bk658fpbex0d57cqcwoe3jthu   redis.2      redis:7.4.1@sha256:6a692a76c2081888b589e26e6ec835743119fe453d67ecf03df7de5b73d69842  worker2   Running        Running 5 seconds
nvjljf7rmor4htv7l8rwcx7i7   \_ redis.2   redis:7.4.1@sha256:6a692a76c2081888b589e26e6ec835743119fe453d67ecf03df7de5b73d69842  worker2   Shutdown       Rejected 5 minutes ago   "No such image: redis@sha256:6a692a76c2081888b589e26e6ec835743119fe453d67ecf03df7de5b73d69842"
```

### Filtering (--filter)

The filtering flag (`-f` or `--filter`) format is a `key=value` pair. If there
is more than one filter, then pass multiple flags (e.g. `--filter "foo=bar" --filter "bif=baz"`).
Multiple filter flags are combined as an `OR` filter. For example,
`-f name=redis.1 -f name=redis.7` returns both `redis.1` and `redis.7` tasks.

The currently supported filters are:

- [id](#id)
- [name](#name)
- [node](#node)
- [desired-state](#desired-state)

#### id

The `id` filter matches on all or a prefix of a task's ID.

```console
$ docker service ps -f "id=8" redis

ID             NAME      IMAGE        NODE      DESIRED STATE  CURRENT STATE      ERROR  PORTS
8ryt076polmc   redis.4   redis:7.4.1  worker1   Running        Running 9 seconds
8eaxrb2fqpbn   redis.10  redis:7.4.1  manager1  Running        Running 8 seconds
```

#### name

The `name` filter matches on task names.

```console
$ docker service ps -f "name=redis.1" redis

ID            NAME     IMAGE        NODE      DESIRED STATE  CURRENT STATE      ERROR  PORTS
qihejybwf1x5  redis.1  redis:7.4.1  manager1  Running        Running 8 seconds
```

#### node

The `node` filter matches on a node name or a node ID.

```console
$ docker service ps -f "node=manager1" redis

ID            NAME      IMAGE        NODE      DESIRED STATE  CURRENT STATE      ERROR  PORTS
0qihejybwf1x  redis.1   redis:7.4.1  manager1  Running        Running 8 seconds
1x0v8yomsncd  redis.5   redis:7.4.1  manager1  Running        Running 8 seconds
3w1wu13yupln  redis.9   redis:7.4.1  manager1  Running        Running 8 seconds
8eaxrb2fqpbn  redis.10  redis:7.4.1  manager1  Running        Running 8 seconds
```

#### desired-state

The `desired-state` filter can take the values `running`, `shutdown`, or `accepted`.

### Format the output (--format)

The formatting options (`--format`) pretty-prints tasks output
using a Go template.

Valid placeholders for the Go template are listed below:

| Placeholder | Description |
| --- | --- |
| .ID | Task ID |
| .Name | Task name |
| .Image | Task image |
| .Node | Node ID |
| .DesiredState | Desired state of the task (running,shutdown, oraccepted) |
| .CurrentState | Current state of the task |
| .Error | Error |
| .Ports | Task published ports |

When using the `--format` option, the `service ps` command will either
output the data exactly as the template declares or, when using the
`table` directive, includes column headers as well.

The following example uses a template without headers and outputs the
`Name` and `Image` entries separated by a colon (`:`) for all tasks:

```console
$ docker service ps --format "{{.Name}}: {{.Image}}" top

top.1: busybox
top.2: busybox
top.3: busybox
```

---

# docker service rm

# docker service rm

| Description | Remove one or more services |
| --- | --- |
| Usage | docker service rm SERVICE [SERVICE...] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker service remove |

Swarm
This command works with the Swarm orchestrator.

## Description

Removes the specified services from the swarm.

> Note
>
> This is a cluster management command, and must be executed on a swarm
> manager node. To learn about managers and workers, refer to the
> [Swarm mode section](https://docs.docker.com/engine/swarm/) in the
> documentation.

## Examples

Remove the `redis` service:

```console
$ docker service rm redis

redis

$ docker service ls

ID  NAME  MODE  REPLICAS  IMAGE
```

> Warning
>
> Unlike `docker rm`, this command does not ask for confirmation before removing
> a running service.

---

# docker service rollback

# docker service rollback

| Description | Revert changes to a service's configuration |
| --- | --- |
| Usage | docker service rollback [OPTIONS] SERVICE |

Swarm
This command works with the Swarm orchestrator.

## Description

Roll back a specified service to its previous version from the swarm.

> Note
>
> This is a cluster management command, and must be executed on a swarm
> manager node. To learn about managers and workers, refer to the
> [Swarm mode section](https://docs.docker.com/engine/swarm/) in the
> documentation.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -d, --detach |  | API 1.29+Exit immediately instead of waiting for the service to converge |
| -q, --quiet |  | Suppress progress output |

## Examples

### Roll back to the previous version of a service

Use the `docker service rollback` command to roll back to the previous version
of a service. After executing this command, the service is reverted to the
configuration that was in place before the most recent `docker service update`
command.

The following example creates a service with a single replica, updates the
service to use three replicas, and then rolls back the service to the
previous version, having one replica.

Create a service with a single replica:

```console
$ docker service create --name my-service -p 8080:80 nginx:alpine
```

Confirm that the service is running with a single replica:

```console
$ docker service ls

ID                  NAME                MODE                REPLICAS            IMAGE               PORTS
xbw728mf6q0d        my-service          replicated          1/1                 nginx:alpine        *:8080->80/tcp
```

Update the service to use three replicas:

```console
$ docker service update --replicas=3 my-service

$ docker service ls

ID                  NAME                MODE                REPLICAS            IMAGE               PORTS
xbw728mf6q0d        my-service          replicated          3/3                 nginx:alpine        *:8080->80/tcp
```

Now roll back the service to its previous version, and confirm it is
running a single replica again:

```console
$ docker service rollback my-service

$ docker service ls

ID                  NAME                MODE                REPLICAS            IMAGE               PORTS
xbw728mf6q0d        my-service          replicated          1/1                 nginx:alpine        *:8080->80/tcp
```

---

# docker service scale

# docker service scale

| Description | Scale one or multiple replicated services |
| --- | --- |
| Usage | docker service scale SERVICE=REPLICAS [SERVICE=REPLICAS...] |

Swarm
This command works with the Swarm orchestrator.

## Description

The scale command enables you to scale one or more replicated services either up
or down to the desired number of replicas. This command cannot be applied on
services which are global mode. The command will return immediately, but the
actual scaling of the service may take some time. To stop all replicas of a
service while keeping the service active in the swarm you can set the scale to 0.

> Note
>
> This is a cluster management command, and must be executed on a swarm
> manager node. To learn about managers and workers, refer to the
> [Swarm mode section](https://docs.docker.com/engine/swarm/) in the
> documentation.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -d, --detach |  | API 1.29+Exit immediately instead of waiting for the service to converge |

## Examples

### Scale a single service

The following command scales the "frontend" service to 50 tasks.

```console
$ docker service scale frontend=50

frontend scaled to 50
```

The following command tries to scale a global service to 10 tasks and returns an error.

```console
$ docker service create --mode global --name backend backend:latest

b4g08uwuairexjub6ome6usqh

$ docker service scale backend=10

backend: scale can only be used with replicated or replicated-job mode
```

Directly afterwards, run `docker service ls`, to see the actual number of
replicas.

```console
$ docker service ls --filter name=frontend

ID            NAME      MODE        REPLICAS  IMAGE
3pr5mlvu3fh9  frontend  replicated  15/50     nginx:alpine
```

You can also scale a service using the
[docker service update](https://docs.docker.com/reference/cli/docker/service/update/)
command. The following commands are equivalent:

```console
$ docker service scale frontend=50
$ docker service update --replicas=50 frontend
```

### Scale multiple services

The `docker service scale` command allows you to set the desired number of
tasks for multiple services at once. The following example scales both the
backend and frontend services:

```console
$ docker service scale backend=3 frontend=5

backend scaled to 3
frontend scaled to 5

$ docker service ls

ID            NAME      MODE        REPLICAS  IMAGE
3pr5mlvu3fh9  frontend  replicated  5/5       nginx:alpine
74nzcxxjv6fq  backend   replicated  3/3       redis:7.4.1
```

---

# docker service update

# docker service update

| Description | Update a service |
| --- | --- |
| Usage | docker service update [OPTIONS] SERVICE |

Swarm
This command works with the Swarm orchestrator.

## Description

Updates a service as described by the specified parameters. The parameters are
the same as
[docker service create](https://docs.docker.com/reference/cli/docker/service/create/). Refer to the description
there for further information.

Normally, updating a service will only cause the service's tasks to be replaced with new ones if a change to the
service requires recreating the tasks for it to take effect. For example, only changing the
`--update-parallelism` setting will not recreate the tasks, because the individual tasks are not affected by this
setting. However, the `--force` flag will cause the tasks to be recreated anyway. This can be used to perform a
rolling restart without any changes to the service parameters.

> Note
>
> This is a cluster management command, and must be executed on a swarm
> manager node. To learn about managers and workers, refer to the
> [Swarm mode section](https://docs.docker.com/engine/swarm/) in the
> documentation.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --args |  | Service command args |
| --cap-add |  | API 1.41+Add Linux capabilities |
| --cap-drop |  | API 1.41+Drop Linux capabilities |
| --config-add |  | API 1.30+Add or update a config file on a service |
| --config-rm |  | API 1.30+Remove a configuration file |
| --constraint-add |  | Add or update a placement constraint |
| --constraint-rm |  | Remove a constraint |
| --container-label-add |  | Add or update a container label |
| --container-label-rm |  | Remove a container label by its key |
| --credential-spec |  | API 1.29+Credential spec for managed service account (Windows only) |
| -d, --detach |  | API 1.29+Exit immediately instead of waiting for the service to converge |
| --dns-add |  | API 1.25+Add or update a custom DNS server |
| --dns-option-add |  | API 1.25+Add or update a DNS option |
| --dns-option-rm |  | API 1.25+Remove a DNS option |
| --dns-rm |  | API 1.25+Remove a custom DNS server |
| --dns-search-add |  | API 1.25+Add or update a custom DNS search domain |
| --dns-search-rm |  | API 1.25+Remove a DNS search domain |
| --endpoint-mode |  | Endpoint mode (vip or dnsrr) |
| --entrypoint |  | Overwrite the default ENTRYPOINT of the image |
| --env-add |  | Add or update an environment variable |
| --env-rm |  | Remove an environment variable |
| --force |  | API 1.25+Force update even if no changes require it |
| --generic-resource-add |  | API 1.32+Add a Generic resource |
| --generic-resource-rm |  | API 1.32+Remove a Generic resource |
| --group-add |  | API 1.25+Add an additional supplementary user group to the container |
| --group-rm |  | API 1.25+Remove a previously added supplementary user group from the container |
| --health-cmd |  | API 1.25+Command to run to check health |
| --health-interval |  | API 1.25+Time between running the check (ms|s|m|h) |
| --health-retries |  | API 1.25+Consecutive failures needed to report unhealthy |
| --health-start-interval |  | API 1.44+Time between running the check during the start period (ms|s|m|h) |
| --health-start-period |  | API 1.29+Start period for the container to initialize before counting retries towards unstable (ms|s|m|h) |
| --health-timeout |  | API 1.25+Maximum time to allow one check to run (ms|s|m|h) |
| --host-add |  | API 1.25+Add a custom host-to-IP mapping (host:ip) |
| --host-rm |  | API 1.25+Remove a custom host-to-IP mapping (host:ip) |
| --hostname |  | API 1.25+Container hostname |
| --image |  | Service image tag |
| --init |  | API 1.37+Use an init inside each service container to forward signals and reap processes |
| --isolation |  | API 1.35+Service container isolation mode |
| --label-add |  | Add or update a service label |
| --label-rm |  | Remove a label by its key |
| --limit-cpu |  | Limit CPUs |
| --limit-memory |  | Limit Memory |
| --limit-pids |  | API 1.41+Limit maximum number of processes (default 0 = unlimited) |
| --log-driver |  | Logging driver for service |
| --log-opt |  | Logging driver options |
| --max-concurrent |  | API 1.41+Number of job tasks to run concurrently (default equal to --replicas) |
| --memory-swap |  | API 1.52+Swap Bytes (-1 for unlimited) |
| --memory-swappiness | -1 | API 1.52+Tune memory swappiness (0-100), -1 to reset to default |
| --mount-add |  | Add or update a mount on a service |
| --mount-rm |  | Remove a mount by its target path |
| --network-add |  | API 1.29+Add a network |
| --network-rm |  | API 1.29+Remove a network |
| --no-healthcheck |  | API 1.25+Disable any container-specified HEALTHCHECK |
| --no-resolve-image |  | API 1.30+Do not query the registry to resolve image digest and supported platforms |
| --oom-score-adj |  | API 1.46+Tune host's OOM preferences (-1000 to 1000) |
| --placement-pref-add |  | API 1.28+Add a placement preference |
| --placement-pref-rm |  | API 1.28+Remove a placement preference |
| --publish-add |  | Add or update a published port |
| --publish-rm |  | Remove a published port by its target port |
| -q, --quiet |  | Suppress progress output |
| --read-only |  | API 1.28+Mount the container's root filesystem as read only |
| --replicas |  | Number of tasks |
| --replicas-max-per-node |  | API 1.40+Maximum number of tasks per node (default 0 = unlimited) |
| --reserve-cpu |  | Reserve CPUs |
| --reserve-memory |  | Reserve Memory |
| --restart-condition |  | Restart when condition is met (none,on-failure,any) |
| --restart-delay |  | Delay between restart attempts (ns|us|ms|s|m|h) |
| --restart-max-attempts |  | Maximum number of restarts before giving up |
| --restart-window |  | Window used to evaluate the restart policy (ns|us|ms|s|m|h) |
| --rollback |  | API 1.25+Rollback to previous specification |
| --rollback-delay |  | API 1.28+Delay between task rollbacks (ns|us|ms|s|m|h) |
| --rollback-failure-action |  | API 1.28+Action on rollback failure (pause,continue) |
| --rollback-max-failure-ratio |  | API 1.28+Failure rate to tolerate during a rollback |
| --rollback-monitor |  | API 1.28+Duration after each task rollback to monitor for failure (ns|us|ms|s|m|h) |
| --rollback-order |  | API 1.29+Rollback order (start-first,stop-first) |
| --rollback-parallelism |  | API 1.28+Maximum number of tasks rolled back simultaneously (0 to roll back all at once) |
| --secret-add |  | API 1.25+Add or update a secret on a service |
| --secret-rm |  | API 1.25+Remove a secret |
| --stop-grace-period |  | Time to wait before force killing a container (ns|us|ms|s|m|h) |
| --stop-signal |  | API 1.28+Signal to stop the container |
| --sysctl-add |  | API 1.40+Add or update a Sysctl option |
| --sysctl-rm |  | API 1.40+Remove a Sysctl option |
| -t, --tty |  | API 1.25+Allocate a pseudo-TTY |
| --ulimit-add |  | API 1.41+Add or update a ulimit option |
| --ulimit-rm |  | API 1.41+Remove a ulimit option |
| --update-delay |  | Delay between updates (ns|us|ms|s|m|h) |
| --update-failure-action |  | Action on update failure (pause,continue,rollback) |
| --update-max-failure-ratio |  | API 1.25+Failure rate to tolerate during an update |
| --update-monitor |  | API 1.25+Duration after each task update to monitor for failure (ns|us|ms|s|m|h) |
| --update-order |  | API 1.29+Update order (start-first,stop-first) |
| --update-parallelism |  | Maximum number of tasks updated simultaneously (0 to update all at once) |
| -u, --user |  | Username or UID (format: <name|uid>[:<group|gid>]) |
| --with-registry-auth |  | Send registry authentication details to swarm agents |
| -w, --workdir |  | Working directory inside the container |

## Examples

### Update a service

```console
$ docker service update --limit-cpu 2 redis
```

### Perform a rolling restart with no parameter changes

```console
$ docker service update --force --update-parallelism 1 --update-delay 30s redis
```

In this example, the `--force` flag causes the service's tasks to be shut down
and replaced with new ones even though none of the other parameters would
normally cause that to happen. The `--update-parallelism 1` setting ensures
that only one task is replaced at a time (this is the default behavior). The
`--update-delay 30s` setting introduces a 30 second delay between tasks, so
that the rolling restart happens gradually.

### Add or remove mounts (--mount-add, --mount-rm)

Use the `--mount-add` or `--mount-rm` options add or remove a service's bind mounts
or volumes.

The following example creates a service which mounts the `test-data` volume to
`/somewhere`. The next step updates the service to also mount the `other-volume`
volume to `/somewhere-else`volume, The last step unmounts the `/somewhere` mount
point, effectively removing the `test-data` volume. Each command returns the
service name.

- The `--mount-add` flag takes the same parameters as the `--mount` flag on
  `service create`. Refer to the
  [volumes and bind mounts](https://docs.docker.com/reference/cli/docker/service/create/#mount)
  section in the `service create` reference for details.
- The `--mount-rm` flag takes the `target` path of the mount.

```console
$ docker service create \
    --name=myservice \
    --mount type=volume,source=test-data,target=/somewhere \
    nginx:alpine

myservice

$ docker service update \
    --mount-add type=volume,source=other-volume,target=/somewhere-else \
    myservice

myservice

$ docker service update --mount-rm /somewhere myservice

myservice
```

### Add or remove published service ports (--publish-add, --publish-rm)

Use the `--publish-add` or `--publish-rm` flags to add or remove a published
port for a service. You can use the short or long syntax discussed in the
[docker service create](https://docs.docker.com/reference/cli/docker/service/create/#publish)
reference.

The following example adds a published service port to an existing service.

```console
$ docker service update \
  --publish-add published=8080,target=80 \
  myservice
```

### Add or remove network (--network-add, --network-rm)

Use the `--network-add` or `--network-rm` flags to add or remove a network for
a service. You can use the short or long syntax discussed in the
[docker service create](https://docs.docker.com/reference/cli/docker/service/create/#network)
reference.

The following example adds a new alias name to an existing service already connected to network my-network:

```console
$ docker service update \
  --network-rm my-network \
  --network-add name=my-network,alias=web1 \
  myservice
```

### Roll back to the previous version of a service (--rollback)

Use the `--rollback` option to roll back to the previous version of the service.

This will revert the service to the configuration that was in place before the most recent `docker service update` command.

The following example updates the number of replicas for the service from 4 to 5, and then rolls back to the previous configuration.

```console
$ docker service update --replicas=5 web

web

$ docker service ls

ID            NAME  MODE        REPLICAS  IMAGE
80bvrzp6vxf3  web   replicated  0/5       nginx:alpine
```

The following example rolls back the `web` service:

```console
$ docker service update --rollback web

web

$ docker service ls

ID            NAME  MODE        REPLICAS  IMAGE
80bvrzp6vxf3  web   replicated  0/4       nginx:alpine
```

Other options can be combined with `--rollback` as well, for example, `--update-delay 0s` to execute the rollback without a delay between tasks:

```console
$ docker service update \
  --rollback \
  --update-delay 0s
  web

web
```

Services can also be set up to roll back to the previous version automatically
when an update fails. To set up a service for automatic rollback, use
`--update-failure-action=rollback`. A rollback will be triggered if the fraction
of the tasks which failed to update successfully exceeds the value given with
`--update-max-failure-ratio`.

The rate, parallelism, and other parameters of a rollback operation are
determined by the values passed with the following flags:

- `--rollback-delay`
- `--rollback-failure-action`
- `--rollback-max-failure-ratio`
- `--rollback-monitor`
- `--rollback-parallelism`

For example, a service set up with `--update-parallelism 1 --rollback-parallelism 3`
will update one task at a time during a normal update, but during a rollback, 3
tasks at a time will get rolled back. These rollback parameters are respected both
during automatic rollbacks and for rollbacks initiated manually using `--rollback`.

### Add or remove secrets (--secret-add, --secret-rm)

Use the `--secret-add` or `--secret-rm` options add or remove a service's
secrets.

The following example adds a secret named `ssh-2` and removes `ssh-1`:

```console
$ docker service update \
    --secret-add source=ssh-2,target=ssh-2 \
    --secret-rm ssh-1 \
    myservice
```

### Update services using templates

Some flags of `service update` support the use of templating.
See
[service create](https://docs.docker.com/reference/cli/docker/service/create/#create-services-using-templates) for the reference.

### Specify isolation mode on Windows (--isolation)

`service update` supports the same `--isolation` flag as `service create`
See
[service create](https://docs.docker.com/reference/cli/docker/service/create/) for the reference.

### Updating Jobs

When a service is created as a job, by setting its mode to `replicated-job` or
to `global-job` when doing `service create`, options for updating it are
limited.

Updating a Job immediately stops any Tasks that are in progress. The operation
creates a new set of Tasks for the job and effectively resets its completion
status. If any Tasks were running before the update, they are stopped, and new
Tasks are created.

Jobs cannot be rolled out or rolled back. None of the flags for configuring
update or rollback settings are valid with job modes.

To run a job again with the same parameters that it was run previously, it can
be force updated with the `--force` flag.

---

# docker service

# docker service

| Description | Manage Swarm services |
| --- | --- |
| Usage | docker service |

Swarm
This command works with the Swarm orchestrator.

## Description

Manage Swarm services.

> Note
>
> This is a cluster management command, and must be executed on a swarm
> manager node. To learn about managers and workers, refer to the
> [Swarm mode section](https://docs.docker.com/engine/swarm/) in the
> documentation.

## Subcommands

| Command | Description |
| --- | --- |
| docker service create | Create a new service |
| docker service inspect | Display detailed information on one or more services |
| docker service logs | Fetch the logs of a service or task |
| docker service ls | List services |
| docker service ps | List the tasks of one or more services |
| docker service rm | Remove one or more services |
| docker service rollback | Revert changes to a service's configuration |
| docker service scale | Scale one or multiple replicated services |
| docker service update | Update a service |
