# docker swarm join and more

# docker swarm join

# docker swarm join

| Description | Join a swarm as a node and/or manager |
| --- | --- |
| Usage | docker swarm join [OPTIONS] HOST:PORT |

Swarm
This command works with the Swarm orchestrator.

## Description

Join a node to a swarm. The node joins as a manager node or worker node based upon the token you
pass with the `--token` flag. If you pass a manager token, the node joins as a manager. If you
pass a worker token, the node joins as a worker.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --advertise-addr |  | Advertised address (format:<ip|interface>[:port]) |
| --availability | active | Availability of the node (active,pause,drain) |
| --data-path-addr |  | API 1.31+Address or interface to use for data path traffic (format:<ip|interface>) |
| --listen-addr | 0.0.0.0:2377 | Listen address (format:<ip|interface>[:port]) |
| --token |  | Token for entry into the swarm |

## Examples

### Join a node to swarm as a manager

The example below demonstrates joining a manager node using a manager token.

```console
$ docker swarm join --token SWMTKN-1-3pu6hszjas19xyp7ghgosyx9k8atbfcr8p2is99znpy26u2lkl-7p73s1dx5in4tatdymyhg9hu2 192.168.99.121:2377
This node joined a swarm as a manager.

$ docker node ls
ID                           HOSTNAME  STATUS  AVAILABILITY  MANAGER STATUS
dkp8vy1dq1kxleu9g4u78tlag *  manager2  Ready   Active        Reachable
dvfxp4zseq4s0rih1selh0d20    manager1  Ready   Active        Leader
```

A cluster should only have 3-7 managers at most, because a majority of managers must be available
for the cluster to function. Nodes that aren't meant to participate in this management quorum
should join as workers instead. Managers should be stable hosts that have static IP addresses.

### Join a node to swarm as a worker

The example below demonstrates joining a worker node using a worker token.

```console
$ docker swarm join --token SWMTKN-1-3pu6hszjas19xyp7ghgosyx9k8atbfcr8p2is99znpy26u2lkl-1awxwuwd3z9j1z3puu7rcgdbx 192.168.99.121:2377
This node joined a swarm as a worker.

$ docker node ls
ID                           HOSTNAME  STATUS  AVAILABILITY  MANAGER STATUS
7ln70fl22uw2dvjn2ft53m3q5    worker2   Ready   Active
dkp8vy1dq1kxleu9g4u78tlag    worker1   Ready   Active        Reachable
dvfxp4zseq4s0rih1selh0d20 *  manager1  Ready   Active        Leader
```

### --listen-addr value

If the node is a manager, it will listen for inbound swarm manager traffic on this
address. The default is to listen on 0.0.0.0:2377. It is also possible to specify a
network interface to listen on that interface's address; for example `--listen-addr eth0:2377`.

Specifying a port is optional. If the value is a bare IP address, or interface
name, the default port 2377 will be used.

This flag is generally not necessary when joining an existing swarm.

### --advertise-addr value

This flag specifies the address that will be advertised to other members of the
swarm for API access. If unspecified, Docker will check if the system has a
single IP address, and use that IP address with the listening port (see
`--listen-addr`). If the system has multiple IP addresses, `--advertise-addr`
must be specified so that the correct address is chosen for inter-manager
communication and overlay networking.

It is also possible to specify a network interface to advertise that interface's address;
for example `--advertise-addr eth0:2377`.

Specifying a port is optional. If the value is a bare IP address, or interface
name, the default port 2377 will be used.

This flag is generally not necessary when joining an existing swarm. If
you're joining new nodes through a load balancer, you should use this flag to
ensure the node advertises its IP address and not the IP address of the load
balancer.

### --data-path-addr

This flag specifies the address that global scope network drivers will publish towards
other nodes in order to reach the containers running on this node.
Using this parameter it is then possible to separate the container's data traffic from the
management traffic of the cluster.
If unspecified, Docker will use the same IP address or interface that is used for the
advertise address.

### --token string

Secret value required for nodes to join the swarm

### --availability

This flag specifies the availability of the node at the time the node joins a master.
Possible availability values are `active`, `pause`, or `drain`.

This flag is useful in certain situations. For example, a cluster may want to have
dedicated manager nodes that are not served as worker nodes. This could be achieved
by passing `--availability=drain` to `docker swarm join`.

---

# docker swarm leave

# docker swarm leave

| Description | Leave the swarm |
| --- | --- |
| Usage | docker swarm leave [OPTIONS] |

Swarm
This command works with the Swarm orchestrator.

## Description

When you run this command on a worker, that worker leaves the swarm.

You can use the `--force` option on a manager to remove it from the swarm.
However, this does not reconfigure the swarm to ensure that there are enough
managers to maintain a quorum in the swarm. The safe way to remove a manager
from a swarm is to demote it to a worker and then direct it to leave the quorum
without using `--force`. Only use `--force` in situations where the swarm will
no longer be used after the manager leaves, such as in a single-node swarm.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -f, --force |  | Force this node to leave the swarm, ignoring warnings |

## Examples

Consider the following swarm, as seen from the manager:

```console
$ docker node ls

ID                           HOSTNAME  STATUS  AVAILABILITY  MANAGER STATUS
7ln70fl22uw2dvjn2ft53m3q5    worker2   Ready   Active
dkp8vy1dq1kxleu9g4u78tlag    worker1   Ready   Active
dvfxp4zseq4s0rih1selh0d20 *  manager1  Ready   Active        Leader
```

To remove `worker2`, issue the following command from `worker2` itself:

```console
$ docker swarm leave

Node left the default swarm.
```

The node will still appear in the node list, and marked as `down`. It no longer
affects swarm operation, but a long list of `down` nodes can clutter the node
list. To remove an inactive node from the list, use the
[node rm](https://docs.docker.com/reference/cli/docker/node/rm/)
command.

---

# docker swarm unlock

# docker swarm unlock-key

| Description | Manage the unlock key |
| --- | --- |
| Usage | docker swarm unlock-key [OPTIONS] |

Swarm
This command works with the Swarm orchestrator.

## Description

An unlock key is a secret key needed to unlock a manager after its Docker daemon
restarts. These keys are only used when the autolock feature is enabled for the
swarm.

You can view or rotate the unlock key using `swarm unlock-key`. To view the key,
run the `docker swarm unlock-key` command without any arguments:

> Note
>
> This is a cluster management command, and must be executed on a swarm
> manager node. To learn about managers and workers, refer to the
> [Swarm mode section](https://docs.docker.com/engine/swarm/) in the
> documentation.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -q, --quiet |  | Only display token |
| --rotate |  | Rotate unlock key |

## Examples

```console
$ docker swarm unlock-key

To unlock a swarm manager after it restarts, run the `docker swarm unlock`
command and provide the following key:

    SWMKEY-1-fySn8TY4w5lKcWcJPIpKufejh9hxx5KYwx6XZigx3Q4

Remember to store this key in a password manager, since without it you
will not be able to restart the manager.
```

Use the `--rotate` flag to rotate the unlock key to a new, randomly-generated
key:

```console
$ docker swarm unlock-key --rotate

Successfully rotated manager unlock key.

To unlock a swarm manager after it restarts, run the `docker swarm unlock`
command and provide the following key:

    SWMKEY-1-7c37Cc8654o6p38HnroywCi19pllOnGtbdZEgtKxZu8

Remember to store this key in a password manager, since without it you
will not be able to restart the manager.
```

The `-q` (or `--quiet`) flag only prints the key:

```console
$ docker swarm unlock-key -q

SWMKEY-1-7c37Cc8654o6p38HnroywCi19pllOnGtbdZEgtKxZu8
```

### --rotate

This flag rotates the unlock key, replacing it with a new randomly-generated
key. The old unlock key will no longer be accepted.

### --quiet

Only print the unlock key, without instructions.

---

# docker swarm unlock

# docker swarm unlock

| Description | Unlock swarm |
| --- | --- |
| Usage | docker swarm unlock |

Swarm
This command works with the Swarm orchestrator.

## Description

Unlocks a locked manager using a user-supplied unlock key. This command must be
used to reactivate a manager after its Docker daemon restarts if the autolock
setting is turned on. The unlock key is printed at the time when autolock is
enabled, and is also available from the `docker swarm unlock-key` command.

> Note
>
> This is a cluster management command, and must be executed on a swarm
> manager node. To learn about managers and workers, refer to the
> [Swarm mode section](https://docs.docker.com/engine/swarm/) in the
> documentation.

## Examples

```console
$ docker swarm unlock
Enter unlock key:
```

---

# docker swarm update

# docker swarm update

| Description | Update the swarm |
| --- | --- |
| Usage | docker swarm update [OPTIONS] |

Swarm
This command works with the Swarm orchestrator.

## Description

Updates a swarm with new parameter values.

> Note
>
> This is a cluster management command, and must be executed on a swarm
> manager node. To learn about managers and workers, refer to the
> [Swarm mode section](https://docs.docker.com/engine/swarm/) in the
> documentation.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --autolock |  | Change manager autolocking setting (true|false) |
| --cert-expiry | 2160h0m0s | Validity period for node certificates (ns|us|ms|s|m|h) |
| --dispatcher-heartbeat | 5s | Dispatcher heartbeat period (ns|us|ms|s|m|h) |
| --external-ca |  | Specifications of one or more certificate signing endpoints |
| --max-snapshots |  | API 1.25+Number of additional Raft snapshots to retain |
| --snapshot-interval | 10000 | API 1.25+Number of log entries between Raft snapshots |
| --task-history-limit | 5 | Task history retention limit |

## Examples

```console
$ docker swarm update --cert-expiry 720h
```

---

# docker swarm

# docker swarm

| Description | Manage Swarm |
| --- | --- |
| Usage | docker swarm |

Swarm
This command works with the Swarm orchestrator.

## Description

Manage the swarm.

## Subcommands

| Command | Description |
| --- | --- |
| docker swarm ca | Display and rotate the root CA |
| docker swarm init | Initialize a swarm |
| docker swarm join | Join a swarm as a node and/or manager |
| docker swarm join-token | Manage join tokens |
| docker swarm leave | Leave the swarm |
| docker swarm unlock | Unlock swarm |
| docker swarm unlock-key | Manage the unlock key |
| docker swarm update | Update the swarm |

---

# docker system df

# docker system df

| Description | Show docker disk usage |
| --- | --- |
| Usage | docker system df [OPTIONS] |

## Description

The `docker system df` command displays information regarding the
amount of disk space used by the Docker daemon.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --format |  | Format output using a custom template:'table': Print output in table format with column headers (default)'table TEMPLATE': Print output in table format using the given Go template'json': Print in JSON format'TEMPLATE': Print output using the given Go template.Refer tohttps://docs.docker.com/go/formatting/for more information about formatting output with templates |
| -v, --verbose |  | Show detailed information on space usage |

## Examples

By default the command displays a summary of the data used:

```console
$ docker system df

TYPE                TOTAL               ACTIVE              SIZE                RECLAIMABLE
Images              5                   2                   16.43 MB            11.63 MB (70%)
Containers          2                   0                   212 B               212 B (100%)
Local Volumes       2                   1                   36 B                0 B (0%)
```

Use the `-v, --verbose` flag to get more detailed information:

```console
$ docker system df -v

Images space usage:

REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE                SHARED SIZE         UNIQUE SIZE         CONTAINERS
my-curl             latest              b2789dd875bf        6 minutes ago       11 MB               11 MB               5 B                 0
my-jq               latest              ae67841be6d0        6 minutes ago       9.623 MB            8.991 MB            632.1 kB            0
<none>              <none>              a0971c4015c1        6 minutes ago       11 MB               11 MB               0 B                 0
alpine              latest              4e38e38c8ce0        9 weeks ago         4.799 MB            0 B                 4.799 MB            1
alpine              3.3                 47cf20d8c26c        9 weeks ago         4.797 MB            4.797 MB            0 B                 1

Containers space usage:

CONTAINER ID        IMAGE               COMMAND             LOCAL VOLUMES       SIZE                CREATED             STATUS                      NAMES
4a7f7eebae0f        alpine:latest       "sh"                1                   0 B                 16 minutes ago      Exited (0) 5 minutes ago    hopeful_yalow
f98f9c2aa1ea        alpine:3.3          "sh"                1                   212 B               16 minutes ago      Exited (0) 48 seconds ago   anon-vol

Local Volumes space usage:

NAME                                                               LINKS               SIZE
07c7bdf3e34ab76d921894c2b834f073721fccfbbcba792aa7648e3a7a664c2e   2                   36 B
my-named-vol                                                       0                   0 B
```

- `SHARED SIZE` is the amount of space that an image shares with another one (i.e. their common data)
- `UNIQUE SIZE` is the amount of space that's only used by a given image
- `SIZE` is the virtual size of the image, it's the sum of `SHARED SIZE` and `UNIQUE SIZE`

> Note
>
> Network information isn't shown, because it doesn't consume disk space.

---

# docker system events

# docker system events

| Description | Get real time events from the server |
| --- | --- |
| Usage | docker system events [OPTIONS] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker events |

## Description

Use `docker events` to get real-time events from the server. These events differ
per Docker object type. Different event types have different scopes. Local
scoped events are only seen on the node they take place on, and Swarm scoped
events are seen on all managers.

Only the last 256 log events are returned. You can use filters to further limit
the number of events returned.

### Object types

#### Containers

Docker containers report the following events:

- `attach`
- `commit`
- `copy`
- `create`
- `destroy`
- `detach`
- `die`
- `exec_create`
- `exec_detach`
- `exec_die`
- `exec_start`
- `export`
- `health_status`
- `kill`
- `oom`
- `pause`
- `rename`
- `resize`
- `restart`
- `start`
- `stop`
- `top`
- `unpause`
- `update`

#### Images

Docker images report the following events:

- `delete`
- `import`
- `load`
- `pull`
- `push`
- `save`
- `tag`
- `untag`

#### Plugins

Docker plugins report the following events:

- `enable`
- `disable`
- `install`
- `remove`

#### Volumes

Docker volumes report the following events:

- `create`
- `destroy`
- `mount`
- `unmount`

#### Networks

Docker networks report the following events:

- `create`
- `connect`
- `destroy`
- `disconnect`
- `remove`

#### Daemons

Docker daemons report the following events:

- `reload`

#### Services

Docker services report the following events:

- `create`
- `remove`
- `update`

#### Nodes

Docker nodes report the following events:

- `create`
- `remove`
- `update`

#### Secrets

Docker secrets report the following events:

- `create`
- `remove`
- `update`

#### Configs

Docker configs report the following events:

- `create`
- `remove`
- `update`

### Limiting, filtering, and formatting the output

#### Limit events by time (--since, --until)

The `--since` and `--until` parameters can be Unix timestamps, date formatted
timestamps, or Go duration strings supported by [ParseDuration](https://pkg.go.dev/time#ParseDuration) (e.g. `10m`, `1h30m`) computed
relative to the client machine’s time. If you do not provide the `--since` option,
the command returns only new and/or live events. Supported formats for date
formatted time stamps include RFC3339Nano, RFC3339, `2006-01-02T15:04:05`,
`2006-01-02T15:04:05.999999999`, `2006-01-02T07:00`, and `2006-01-02`. The local
timezone on the client will be used if you do not provide either a `Z` or a
`+-00:00` timezone offset at the end of the timestamp. When providing Unix
timestamps enter seconds[.nanoseconds], where seconds is the number of seconds
that have elapsed since January 1, 1970 (midnight UTC/GMT), not counting leap
seconds (aka Unix epoch or Unix time), and the optional .nanoseconds field is a
fraction of a second no more than nine digits long.

Only the last 256 log events are returned. You can use filters to further limit
the number of events returned.

#### Filtering (--filter)

The filtering flag (`-f` or `--filter`) format is of "key=value". If you would
like to use multiple filters, pass multiple flags (e.g.,
`--filter "foo=bar" --filter "bif=baz"`)

Using the same filter multiple times is interpreted as a logical `OR`; for example,
`--filter container=588a23dac085 --filter container=a8f7720b8c22` displays
events for container `588a23dac085` or container `a8f7720b8c22`.

Using multiple filters is interpreted as a logical `AND`; for example,
`--filter container=588a23dac085 --filter event=start` displays events for
container `588a23dac085` and where the event type is `start`.

The currently supported filters are:

- config (`config=<name or id>`)
- container (`container=<name or id>`)
- daemon (`daemon=<name or id>`)
- event (`event=<event action>`)
- image (`image=<repository or tag>`)
- label (`label=<key>` or `label=<key>=<value>`)
- network (`network=<name or id>`)
- node (`node=<id>`)
- plugin (`plugin=<name or id>`)
- scope (`scope=<local or swarm>`)
- secret (`secret=<name or id>`)
- service (`service=<name or id>`)
- type (`type=<container or image or volume or network or daemon or plugin or service or node or secret or config>`)
- volume (`volume=<name>`)

#### Format the output (--format)

If you specify a format (`--format`), the given template is executed
instead of the default format. Go's [text/template](https://pkg.go.dev/text/template)
package describes all the details of the format.

If a format is set to `{{json .}}`, events are streamed in the JSON Lines format.
For information about JSON Lines, see [https://jsonlines.org/](https://jsonlines.org/).

## Options

| Option | Default | Description |
| --- | --- | --- |
| -f, --filter |  | Filter output based on conditions provided |
| --format |  | Format output using a custom template:'json': Print in JSON format'TEMPLATE': Print output using the given Go template.Refer tohttps://docs.docker.com/go/formatting/for more information about formatting output with templates |
| --since |  | Show all events created since timestamp |
| --until |  | Stream events until this timestamp |

## Examples

### Basic example

You'll need two shells for this example.

**Shell 1: Listening for events:**

```console
$ docker events
```

**Shell 2: Start and Stop containers:**

```console
$ docker create --name test alpine:latest top
$ docker start test
$ docker stop test
```

**Shell 1: (Again .. now showing events):**

```console
2017-01-05T00:35:58.859401177+08:00 container create 0fdb48addc82871eb34eb23a847cfd033dedd1a0a37bef2e6d9eb3870fc7ff37 (image=alpine:latest, name=test)
2017-01-05T00:36:04.703631903+08:00 network connect e2e1f5ceda09d4300f3a846f0acfaa9a8bb0d89e775eb744c5acecd60e0529e2 (container=0fdb...ff37, name=bridge, type=bridge)
2017-01-05T00:36:04.795031609+08:00 container start 0fdb...ff37 (image=alpine:latest, name=test)
2017-01-05T00:36:09.830268747+08:00 container kill 0fdb...ff37 (image=alpine:latest, name=test, signal=15)
2017-01-05T00:36:09.840186338+08:00 container die 0fdb...ff37 (exitCode=143, image=alpine:latest, name=test)
2017-01-05T00:36:09.880113663+08:00 network disconnect e2e...29e2 (container=0fdb...ff37, name=bridge, type=bridge)
2017-01-05T00:36:09.890214053+08:00 container stop 0fdb...ff37 (image=alpine:latest, name=test)
```

To exit the `docker events` command, use `CTRL+C`.

### Filter events by time

You can filter the output by an absolute timestamp or relative time on the host
machine, using the following different time formats:

```console
$ docker events --since 1483283804
2017-01-05T00:35:41.241772953+08:00 volume create testVol (driver=local)
2017-01-05T00:35:58.859401177+08:00 container create d9cd...4d70 (image=alpine:latest, name=test)
2017-01-05T00:36:04.703631903+08:00 network connect e2e1...29e2 (container=0fdb...ff37, name=bridge, type=bridge)
2017-01-05T00:36:04.795031609+08:00 container start 0fdb...ff37 (image=alpine:latest, name=test)
2017-01-05T00:36:09.830268747+08:00 container kill 0fdb...ff37 (image=alpine:latest, name=test, signal=15)
2017-01-05T00:36:09.840186338+08:00 container die 0fdb...ff37 (exitCode=143, image=alpine:latest, name=test)
2017-01-05T00:36:09.880113663+08:00 network disconnect e2e...29e2 (container=0fdb...ff37, name=bridge, type=bridge)
2017-01-05T00:36:09.890214053+08:00 container stop 0fdb...ff37 (image=alpine:latest, name=test)

$ docker events --since '2017-01-05'
2017-01-05T00:35:41.241772953+08:00 volume create testVol (driver=local)
2017-01-05T00:35:58.859401177+08:00 container create d9cd...4d70 (image=alpine:latest, name=test)
2017-01-05T00:36:04.703631903+08:00 network connect e2e1...29e2 (container=0fdb...ff37, name=bridge, type=bridge)
2017-01-05T00:36:04.795031609+08:00 container start 0fdb...ff37 (image=alpine:latest, name=test)
2017-01-05T00:36:09.830268747+08:00 container kill 0fdb...ff37 (image=alpine:latest, name=test, signal=15)
2017-01-05T00:36:09.840186338+08:00 container die 0fdb...ff37 (exitCode=143, image=alpine:latest, name=test)
2017-01-05T00:36:09.880113663+08:00 network disconnect e2e...29e2 (container=0fdb...ff37, name=bridge, type=bridge)
2017-01-05T00:36:09.890214053+08:00 container stop 0fdb...ff37 (image=alpine:latest, name=test)

$ docker events --since '2013-09-03T15:49:29'
2017-01-05T00:35:41.241772953+08:00 volume create testVol (driver=local)
2017-01-05T00:35:58.859401177+08:00 container create d9cd...4d70 (image=alpine:latest, name=test)
2017-01-05T00:36:04.703631903+08:00 network connect e2e1...29e2 (container=0fdb...ff37, name=bridge, type=bridge)
2017-01-05T00:36:04.795031609+08:00 container start 0fdb...ff37 (image=alpine:latest, name=test)
2017-01-05T00:36:09.830268747+08:00 container kill 0fdb...ff37 (image=alpine:latest, name=test, signal=15)
2017-01-05T00:36:09.840186338+08:00 container die 0fdb...ff37 (exitCode=143, image=alpine:latest, name=test)
2017-01-05T00:36:09.880113663+08:00 network disconnect e2e...29e2 (container=0fdb...ff37, name=bridge, type=bridge)
2017-01-05T00:36:09.890214053+08:00 container stop 0fdb...ff37 (image=alpine:latest, name=test)

$ docker events --since '10m'
2017-01-05T00:35:41.241772953+08:00 volume create testVol (driver=local)
2017-01-05T00:35:58.859401177+08:00 container create d9cd...4d70 (image=alpine:latest, name=test)
2017-01-05T00:36:04.703631903+08:00 network connect e2e1...29e2 (container=0fdb...ff37, name=bridge, type=bridge)
2017-01-05T00:36:04.795031609+08:00 container start 0fdb...ff37 (image=alpine:latest, name=test)
2017-01-05T00:36:09.830268747+08:00 container kill 0fdb...ff37 (image=alpine:latest, name=test, signal=15)
2017-01-05T00:36:09.840186338+08:00 container die 0fdb...ff37 (exitCode=143, image=alpine:latest, name=test)
2017-01-05T00:36:09.880113663+08:00 network disconnect e2e...29e2 (container=0fdb...ff37, name=bridge, type=bridge)
2017-01-05T00:36:09.890214053+08:00 container stop 0fdb...ff37 (image=alpine:latest, name=test)

$ docker events --since '2017-01-05T00:35:30' --until '2017-01-05T00:36:05'
2017-01-05T00:35:41.241772953+08:00 volume create testVol (driver=local)
2017-01-05T00:35:58.859401177+08:00 container create d9cd...4d70 (image=alpine:latest, name=test)
2017-01-05T00:36:04.703631903+08:00 network connect e2e1...29e2 (container=0fdb...ff37, name=bridge, type=bridge)
2017-01-05T00:36:04.795031609+08:00 container start 0fdb...ff37 (image=alpine:latest, name=test)
```

### Filter events by criteria

The following commands show several different ways to filter the `docker event`
output.

```console
$ docker events --filter 'event=stop'

2017-01-05T00:40:22.880175420+08:00 container stop 0fdb...ff37 (image=alpine:latest, name=test)
2017-01-05T00:41:17.888104182+08:00 container stop 2a8f...4e78 (image=alpine, name=kickass_brattain)

$ docker events --filter 'image=alpine'

2017-01-05T00:41:55.784240236+08:00 container create d9cd...4d70 (image=alpine, name=happy_meitner)
2017-01-05T00:41:55.913156783+08:00 container start d9cd...4d70 (image=alpine, name=happy_meitner)
2017-01-05T00:42:01.106875249+08:00 container kill d9cd...4d70 (image=alpine, name=happy_meitner, signal=15)
2017-01-05T00:42:11.111934041+08:00 container kill d9cd...4d70 (image=alpine, name=happy_meitner, signal=9)
2017-01-05T00:42:11.119578204+08:00 container die d9cd...4d70 (exitCode=137, image=alpine, name=happy_meitner)
2017-01-05T00:42:11.173276611+08:00 container stop d9cd...4d70 (image=alpine, name=happy_meitner)

$ docker events --filter 'container=test'

2017-01-05T00:43:00.139719934+08:00 container start 0fdb...ff37 (image=alpine:latest, name=test)
2017-01-05T00:43:09.259951086+08:00 container kill 0fdb...ff37 (image=alpine:latest, name=test, signal=15)
2017-01-05T00:43:09.270102715+08:00 container die 0fdb...ff37 (exitCode=143, image=alpine:latest, name=test)
2017-01-05T00:43:09.312556440+08:00 container stop 0fdb...ff37 (image=alpine:latest, name=test)

$ docker events --filter 'container=test' --filter 'container=d9cdb1525ea8'

2017-01-05T00:44:11.517071981+08:00 container start 0fdb...ff37 (image=alpine:latest, name=test)
2017-01-05T00:44:17.685870901+08:00 container start d9cd...4d70 (image=alpine, name=happy_meitner)
2017-01-05T00:44:29.757658470+08:00 container kill 0fdb...ff37 (image=alpine:latest, name=test, signal=9)
2017-01-05T00:44:29.767718510+08:00 container die 0fdb...ff37 (exitCode=137, image=alpine:latest, name=test)
2017-01-05T00:44:29.815798344+08:00 container destroy 0fdb...ff37 (image=alpine:latest, name=test)

$ docker events --filter 'container=test' --filter 'event=stop'

2017-01-05T00:46:13.664099505+08:00 container stop a9d1...e130 (image=alpine, name=test)

$ docker events --filter 'type=volume'

2015-12-23T21:05:28.136212689Z volume create test-event-volume-local (driver=local)
2015-12-23T21:05:28.383462717Z volume mount test-event-volume-local (read/write=true, container=562f...5025, destination=/foo, driver=local, propagation=rprivate)
2015-12-23T21:05:28.650314265Z volume unmount test-event-volume-local (container=562f...5025, driver=local)
2015-12-23T21:05:28.716218405Z volume destroy test-event-volume-local (driver=local)

$ docker events --filter 'type=network'

2015-12-23T21:38:24.705709133Z network create 8b11...2c5b (name=test-event-network-local, type=bridge)
2015-12-23T21:38:25.119625123Z network connect 8b11...2c5b (name=test-event-network-local, container=b4be...c54e, type=bridge)

$ docker events --filter 'container=container_1' --filter 'container=container_2'

2014-09-03T15:49:29.999999999Z07:00 container die 4386fb97867d (image=ubuntu:24.04)
2014-05-10T17:42:14.999999999Z07:00 container stop 4386fb97867d (image=ubuntu:24.04)
2014-05-10T17:42:14.999999999Z07:00 container die 7805c1d35632 (imager=redis:7.2)
2014-09-03T15:49:29.999999999Z07:00 container stop 7805c1d35632 (image=redis:7.2)

$ docker events --filter 'type=volume'

2015-12-23T21:05:28.136212689Z volume create test-event-volume-local (driver=local)
2015-12-23T21:05:28.383462717Z volume mount test-event-volume-local (read/write=true, container=562fe10671e9273da25eed36cdce26159085ac7ee6707105fd534866340a5025, destination=/foo, driver=local, propagation=rprivate)
2015-12-23T21:05:28.650314265Z volume unmount test-event-volume-local (container=562fe10671e9273da25eed36cdce26159085ac7ee6707105fd534866340a5025, driver=local)
2015-12-23T21:05:28.716218405Z volume destroy test-event-volume-local (driver=local)

$ docker events --filter 'type=network'

2015-12-23T21:38:24.705709133Z network create 8b111217944ba0ba844a65b13efcd57dc494932ee2527577758f939315ba2c5b (name=test-event-network-local, type=bridge)
2015-12-23T21:38:25.119625123Z network connect 8b111217944ba0ba844a65b13efcd57dc494932ee2527577758f939315ba2c5b (name=test-event-network-local, container=b4be644031a3d90b400f88ab3d4bdf4dc23adb250e696b6328b85441abe2c54e, type=bridge)

$ docker events --filter 'type=plugin'

2016-07-25T17:30:14.825557616Z plugin pull ec7b87f2ce84330fe076e666f17dfc049d2d7ae0b8190763de94e1f2d105993f (name=tiborvass/sample-volume-plugin:latest)
2016-07-25T17:30:14.888127370Z plugin enable ec7b87f2ce84330fe076e666f17dfc049d2d7ae0b8190763de94e1f2d105993f (name=tiborvass/sample-volume-plugin:latest)

$ docker events -f type=service

2017-07-12T06:34:07.999446625Z service create wj64st89fzgchxnhiqpn8p4oj (name=reverent_albattani)
2017-07-12T06:34:21.405496207Z service remove wj64st89fzgchxnhiqpn8p4oj (name=reverent_albattani)

$ docker events -f type=node

2017-07-12T06:21:51.951586759Z node update 3xyz5ttp1a253q74z1thwywk9 (name=ip-172-31-23-42, state.new=ready, state.old=unknown)

$ docker events -f type=secret

2017-07-12T06:32:13.915704367Z secret create s8o6tmlnndrgzbmdilyy5ymju (name=new_secret)
2017-07-12T06:32:37.052647783Z secret remove s8o6tmlnndrgzbmdilyy5ymju (name=new_secret)

$  docker events -f type=config
2017-07-12T06:44:13.349037127Z config create u96zlvzdfsyb9sg4mhyxfh3rl (name=abc)
2017-07-12T06:44:36.327694184Z config remove u96zlvzdfsyb9sg4mhyxfh3rl (name=abc)

$ docker events --filter 'scope=swarm'

2017-07-10T07:46:50.250024503Z service create m8qcxu8081woyof7w3jaax6gk (name=affectionate_wilson)
2017-07-10T07:47:31.093797134Z secret create 6g5pufzsv438p9tbvl9j94od4 (name=new_secret)
```

### Format the output

```console
$ docker events --filter 'type=container' --format 'Type={{.Type}}  Status={{.Status}}  ID={{.ID}}'

Type=container  Status=create  ID=2ee349dac409e97974ce8d01b70d250b85e0ba8189299c126a87812311951e26
Type=container  Status=attach  ID=2ee349dac409e97974ce8d01b70d250b85e0ba8189299c126a87812311951e26
Type=container  Status=start  ID=2ee349dac409e97974ce8d01b70d250b85e0ba8189299c126a87812311951e26
Type=container  Status=resize  ID=2ee349dac409e97974ce8d01b70d250b85e0ba8189299c126a87812311951e26
Type=container  Status=die  ID=2ee349dac409e97974ce8d01b70d250b85e0ba8189299c126a87812311951e26
Type=container  Status=destroy  ID=2ee349dac409e97974ce8d01b70d250b85e0ba8189299c126a87812311951e26
```

#### Format as JSON

To list events in JSON format, use the `json` directive, which is the same
`--format '{{ json . }}`.

```console
$ docker events --format json

{"status":"create","id":"196016a57679bf42424484918746a9474cd905dd993c4d0f4..
{"status":"attach","id":"196016a57679bf42424484918746a9474cd905dd993c4d0f4..
{"Type":"network","Action":"connect","Actor":{"ID":"1b50a5bf755f6021dfa78e..
{"status":"start","id":"196016a57679bf42424484918746a9474cd905dd993c4d0f42..
{"status":"resize","id":"196016a57679bf42424484918746a9474cd905dd993c4d0f4..
```

---

# docker system info

# docker system info

| Description | Display system-wide information |
| --- | --- |
| Usage | docker system info [OPTIONS] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker info |

## Description

This command displays system wide information regarding the Docker installation.
Information displayed includes the kernel version, number of containers and images.
The number of images shown is the number of unique images. The same image tagged
under different names is counted only once.

If a format is specified, the given template will be executed instead of the
default format. Go's [text/template](https://pkg.go.dev/text/template) package
describes all the details of the format.

Depending on the storage driver in use, additional information can be shown, such
as pool name, data file, metadata file, data space used, total data space, metadata
space used, and total metadata space.

The data file is where the images are stored and the metadata file is where the
meta data regarding those images are stored. When run for the first time Docker
allocates a certain amount of data space and meta data space from the space
available on the volume where `/var/lib/docker` is mounted.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -f, --format |  | Format output using a custom template:'json': Print in JSON format'TEMPLATE': Print output using the given Go template.Refer tohttps://docs.docker.com/go/formatting/for more information about formatting output with templates |

## Examples

### Show output

The example below shows the output for a daemon running on Ubuntu Linux,
using the `overlay2` storage driver. As can be seen in the output, additional
information about the `overlay2` storage driver is shown:

```console
$ docker info

Client:
 Version:    25.0.0
 Context:    default
 Debug Mode: false
 Plugins:
  buildx: Docker Buildx (Docker Inc.)
    Version:  v0.12.1
    Path:     /usr/local/libexec/docker/cli-plugins/docker-buildx
  compose: Docker Compose (Docker Inc.)
    Version:  v2.24.1
    Path:     /usr/local/libexec/docker/cli-plugins/docker-compose

Server:
 Containers: 14
  Running: 3
  Paused: 1
  Stopped: 10
 Images: 52
 Server Version: 25.0.0
 Storage Driver: overlayfs
  driver-type: io.containerd.snapshotter.v1
 Logging Driver: json-file
 Cgroup Driver: cgroupfs
 Cgroup Version: 2
 Plugins:
  Volume: local
  Network: bridge host ipvlan macvlan null overlay
  Log: awslogs fluentd gcplogs gelf journald json-file local splunk syslog
 CDI spec directories:
  /etc/cdi
  /var/run/cdi
 Swarm: inactive
 Runtimes: runc io.containerd.runc.v2
 Default Runtime: runc
 Init Binary: docker-init
 containerd version: 71909c1814c544ac47ab91d2e8b84718e517bb99
 runc version: v1.1.11-0-g4bccb38
 init version: de40ad0
 Security Options:
  seccomp
   Profile: builtin
  cgroupns
 Kernel Version: 6.5.11-linuxkit
 Operating System: Alpine Linux v3.19
 OSType: linux
 Architecture: aarch64
 CPUs: 10
 Total Memory: 7.663GiB
 Name: 4a7ed206a70d
 ID: c20f7230-59a2-4824-a2f4-fda71c982ee6
 Docker Root Dir: /var/lib/docker
 Debug Mode: false
 Experimental: false
 Insecure Registries:
  127.0.0.0/8
 Live Restore Enabled: false
 Product License: Community Engine
```

### Format the output (--format)

You can also specify the output format:

```console
$ docker info --format '{{json .}}'

{"ID":"4cee4408-10d2-4e17-891c-a41736ac4536","Containers":14, ...}
```

### Rundocker infoon Windows

Here is a sample output for a daemon running on Windows Server:

```console
C:\> docker info

Client: Docker Engine - Community
 Version:    24.0.0
 Context:    default
 Debug Mode: false
 Plugins:
  buildx: Docker Buildx (Docker Inc.)
    Version:  v0.10.4
    Path:     C:\Program Files\Docker\cli-plugins\docker-buildx.exe
  compose: Docker Compose (Docker Inc.)
    Version:  v2.17.2
    Path:     C:\Program Files\Docker\cli-plugins\docker-compose.exe

Server:
 Containers: 1
  Running: 0
  Paused: 0
  Stopped: 1
 Images: 17
 Server Version: 23.0.3
 Storage Driver: windowsfilter
 Logging Driver: json-file
 Plugins:
  Volume: local
  Network: ics internal l2bridge l2tunnel nat null overlay private transparent
  Log: awslogs etwlogs fluentd gcplogs gelf json-file local splunk syslog
 Swarm: inactive
 Default Isolation: process
 Kernel Version: 10.0 20348 (20348.1.amd64fre.fe_release.210507-1500)
 Operating System: Microsoft Windows Server Version 21H2 (OS Build 20348.707)
 OSType: windows
 Architecture: x86_64
 CPUs: 8
 Total Memory: 3.999 GiB
 Name: WIN-V0V70C0LU5P
 ID: 2880d38d-464e-4d01-91bd-c76f33ba3981
 Docker Root Dir: C:\ProgramData\docker
 Debug Mode: false
 Experimental: true
 Insecure Registries:
  myregistry:5000
  127.0.0.0/8
 Registry Mirrors:
   http://192.168.1.2/
   http://registry-mirror.example.com:5000/
 Live Restore Enabled: false
```

---

# docker system prune

# docker system prune

| Description | Remove unused data |
| --- | --- |
| Usage | docker system prune [OPTIONS] |

## Description

Remove all unused containers, networks, images (both dangling and unused),
and optionally, volumes.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -a, --all |  | Remove all unused images not just dangling ones |
| --filter |  | API 1.28+Provide filter values (e.g.label=<key>=<value>) |
| -f, --force |  | Do not prompt for confirmation |
| --volumes |  | Prune anonymous volumes |

## Examples

```console
$ docker system prune

WARNING! This will remove:
        - all stopped containers
        - all networks not used by at least one container
        - all dangling images
        - unused build cache
Are you sure you want to continue? [y/N] y

Deleted Containers:
f44f9b81948b3919590d5f79a680d8378f1139b41952e219830a33027c80c867
792776e68ac9d75bce4092bc1b5cc17b779bc926ab04f4185aec9bf1c0d4641f

Deleted Networks:
network1
network2

Deleted Images:
untagged: hello-world@sha256:f3b3b28a45160805bb16542c9531888519430e9e6d6ffc09d72261b0d26ff74f
deleted: sha256:1815c82652c03bfd8644afda26fb184f2ed891d921b20a0703b46768f9755c57
deleted: sha256:45761469c965421a92a69cc50e92c01e0cfa94fe026cdd1233445ea00e96289a

Total reclaimed space: 1.84kB
```

By default, volumes aren't removed to prevent important data from being
deleted if there is currently no container using the volume. Use the `--volumes`
flag when running the command to prune anonymous volumes as well:

```console
$ docker system prune -a --volumes

WARNING! This will remove:
        - all stopped containers
        - all networks not used by at least one container
        - all anonymous volumes not used by at least one container
        - all images without at least one container associated to them
        - all build cache
Are you sure you want to continue? [y/N] y

Deleted Containers:
0998aa37185a1a7036b0e12cf1ac1b6442dcfa30a5c9650a42ed5010046f195b
73958bfb884fa81fa4cc6baf61055667e940ea2357b4036acbbe25a60f442a4d

Deleted Networks:
my-network-a
my-network-b

Deleted Volumes:
1e31bcd425e913d9f65ec0c3841e9c4ebb543aead2a1cfe0d95a7c5e88bb5026
6a6ab3d6b8d740a1c1d4dbe36a9c5f043dd4bac5f78abfa7d1f2ae5789fe60b0

Deleted Images:
untagged: my-curl:latest
deleted: sha256:7d88582121f2a29031d92017754d62a0d1a215c97e8f0106c586546e7404447d
deleted: sha256:dd14a93d83593d4024152f85d7c63f76aaa4e73e228377ba1d130ef5149f4d8b
untagged: alpine:3.3
deleted: sha256:695f3d04125db3266d4ab7bbb3c6b23aa4293923e762aa2562c54f49a28f009f
untagged: alpine:latest
deleted: sha256:ee4603260daafe1a8c2f3b78fd760922918ab2441cbb2853ed5c439e59c52f96
deleted: sha256:9007f5987db353ec398a223bc5a135c5a9601798ba20a1abba537ea2f8ac765f
deleted: sha256:71fa90c8f04769c9721459d5aa0936db640b92c8c91c9b589b54abd412d120ab
deleted: sha256:bb1c3357b3c30ece26e6604aea7d2ec0ace4166ff34c3616701279c22444c0f3
untagged: my-jq:latest
deleted: sha256:6e66d724542af9bc4c4abf4a909791d7260b6d0110d8e220708b09e4ee1322e1
deleted: sha256:07b3fa89d4b17009eb3988dfc592c7d30ab3ba52d2007832dffcf6d40e3eda7f
deleted: sha256:3a88a5c81eb5c283e72db2dbc6d65cbfd8e80b6c89bb6e714cfaaa0eed99c548

Total reclaimed space: 13.5 MB
```

### Filtering (--filter)

The filtering flag (`--filter`) format is of "key=value". If there is more
than one filter, then pass multiple flags (e.g., `--filter "foo=bar" --filter "bif=baz"`)

The currently supported filters are:

- until (`<timestamp>`) - only remove containers, images, and networks created before given timestamp
- label (`label=<key>`, `label=<key>=<value>`, `label!=<key>`, or `label!=<key>=<value>`) - only remove containers, images, networks, and volumes with (or without, in case `label!=...` is used) the specified labels.

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
which removes containers, images, networks, and volumes with the specified labels. The other
format is the `label!=...` (`label!=<key>` or `label!=<key>=<value>`), which removes
containers, images, networks, and volumes without the specified labels.

---

# docker system

# docker system

| Description | Manage Docker |
| --- | --- |
| Usage | docker system |

## Description

Manage Docker.

## Subcommands

| Command | Description |
| --- | --- |
| docker system df | Show docker disk usage |
| docker system events | Get real time events from the server |
| docker system info | Display system-wide information |
| docker system prune | Remove unused data |

---

# docker trust inspect

# docker trust inspect

| Description | Return low-level information about keys and signatures |
| --- | --- |
| Usage | docker trust inspect IMAGE[:TAG] [IMAGE[:TAG]...] |

## Description

`docker trust inspect` provides low-level JSON information on signed repositories.
This includes all image tags that are signed, who signed them, and who can sign
new tags.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --pretty |  | Print the information in a human friendly format |

## Examples

### Get low-level details about signatures for a single image tag

Use the `docker trust inspect` to get trust information about an image. The
following example prints trust information for the `alpine:latest` image:

```console
$ docker trust inspect alpine:latest
```

The output is in JSON format, for example:

```json
[
  {
    "Name": "alpine:latest",
    "SignedTags": [
      {
        "SignedTag": "latest",
        "Digest": "d6bfc3baf615dc9618209a8d607ba2a8103d9c8a405b3bd8741d88b4bef36478",
        "Signers": [
          "Repo Admin"
        ]
      }
    ],
    "Signers": [],
    "AdministrativeKeys": [
      {
        "Name": "Repository",
        "Keys": [
            {
                "ID": "5a46c9aaa82ff150bb7305a2d17d0c521c2d784246807b2dc611f436a69041fd"
            }
        ]
      },
      {
        "Name": "Root",
        "Keys": [
            {
                "ID": "a2489bcac7a79aa67b19b96c4a3bf0c675ffdf00c6d2fabe1a5df1115e80adce"
            }
        ]
      }
    ]
  }
]
```

The `SignedTags` key will list the `SignedTag` name, its `Digest`,
and the `Signers` responsible for the signature.

`AdministrativeKeys` will list the `Repository` and `Root` keys.

If signers are set up for the repository via other `docker trust`
commands, `docker trust inspect` includes a `Signers` key:

```console
$ docker trust inspect my-image:purple
```

The output is in JSON format, for example:

```json
[
  {
    "Name": "my-image:purple",
    "SignedTags": [
      {
        "SignedTag": "purple",
        "Digest": "941d3dba358621ce3c41ef67b47cf80f701ff80cdf46b5cc86587eaebfe45557",
        "Signers": [
          "alice",
          "bob",
          "carol"
        ]
      }
    ],
    "Signers": [
      {
        "Name": "alice",
        "Keys": [
            {
                "ID": "04dd031411ed671ae1e12f47ddc8646d98f135090b01e54c3561e843084484a3"
            },
            {
                "ID": "6a11e4898a4014d400332ab0e096308c844584ff70943cdd1d6628d577f45fd8"
            }
        ]
      },
      {
        "Name": "bob",
        "Keys": [
            {
                "ID": "433e245c656ae9733cdcc504bfa560f90950104442c4528c9616daa45824ccba"
            }
        ]
      },
      {
        "Name": "carol",
        "Keys": [
            {
                "ID": "d32fa8b5ca08273a2880f455fcb318da3dc80aeae1a30610815140deef8f30d9"
            },
            {
                "ID": "9a8bbec6ba2af88a5fad6047d428d17e6d05dbdd03d15b4fc8a9a0e8049cd606"
            }
        ]
      }
    ],
    "AdministrativeKeys": [
      {
        "Name": "Repository",
        "Keys": [
            {
                "ID": "27df2c8187e7543345c2e0bf3a1262e0bc63a72754e9a7395eac3f747ec23a44"
            }
        ]
      },
      {
        "Name": "Root",
        "Keys": [
            {
                "ID": "40b66ccc8b176be8c7d365a17f3e046d1c3494e053dd57cfeacfe2e19c4f8e8f"
            }
        ]
      }
    ]
  }
]
```

If the image tag is unsigned or unavailable, `docker trust inspect` does not
display any signed tags.

```console
$ docker trust inspect unsigned-img

no signatures or cannot access unsigned-img
```

However, if other tags are signed in the same image repository,
`docker trust inspect` reports relevant key information:

```console
$ docker trust inspect alpine:unsigned
```

The output is in JSON format, for example:

```json
[
  {
    "Name": "alpine:unsigned",
    "Signers": [],
    "AdministrativeKeys": [
      {
        "Name": "Repository",
        "Keys": [
          {
            "ID": "5a46c9aaa82ff150bb7305a2d17d0c521c2d784246807b2dc611f436a69041fd"
          }
        ]
      },
      {
        "Name": "Root",
        "Keys": [
          {
            "ID": "a2489bcac7a79aa67b19b96c4a3bf0c675ffdf00c6d2fabe1a5df1115e80adce"
          }
        ]
      }
    ]
  }
]
```

### Get details about signatures for all image tags in a repository

If no tag is specified, `docker trust inspect` will report details for all
signed tags in the repository:

```console
$ docker trust inspect alpine
```

The output is in JSON format, for example:

```json
[
  {
    "Name": "alpine",
    "SignedTags": [
      {
        "SignedTag": "3.5",
        "Digest": "b007a354427e1880de9cdba533e8e57382b7f2853a68a478a17d447b302c219c",
        "Signers": [
          "Repo Admin"
        ]
      },
      {
        "SignedTag": "3.6",
        "Digest": "d6bfc3baf615dc9618209a8d607ba2a8103d9c8a405b3bd8741d88b4bef36478",
        "Signers": [
          "Repo Admin"
        ]
      },
      {
        "SignedTag": "edge",
        "Digest": "23e7d843e63a3eee29b6b8cfcd10e23dd1ef28f47251a985606a31040bf8e096",
        "Signers": [
          "Repo Admin"
        ]
      },
      {
        "SignedTag": "latest",
        "Digest": "d6bfc3baf615dc9618209a8d607ba2a8103d9c8a405b3bd8741d88b4bef36478",
        "Signers": [
          "Repo Admin"
        ]
      }
    ],
    "Signers": [],
    "AdministrativeKeys": [
      {
        "Name": "Repository",
        "Keys": [
          {
            "ID": "5a46c9aaa82ff150bb7305a2d17d0c521c2d784246807b2dc611f436a69041fd"
          }
        ]
      },
      {
        "Name": "Root",
        "Keys": [
          {
            "ID": "a2489bcac7a79aa67b19b96c4a3bf0c675ffdf00c6d2fabe1a5df1115e80adce"
          }
        ]
      }
    ]
  }
]
```

### Get details about signatures for multiple images

`docker trust inspect` can take multiple repositories and images as arguments,
and reports the results in an ordered list:

```console
$ docker trust inspect alpine notary
```

The output is in JSON format, for example:

```json
[
  {
    "Name": "alpine",
    "SignedTags": [
      {
        "SignedTag": "3.5",
        "Digest": "b007a354427e1880de9cdba533e8e57382b7f2853a68a478a17d447b302c219c",
        "Signers": [
          "Repo Admin"
        ]
      },
      {
        "SignedTag": "3.6",
        "Digest": "d6bfc3baf615dc9618209a8d607ba2a8103d9c8a405b3bd8741d88b4bef36478",
        "Signers": [
          "Repo Admin"
        ]
      },
      {
        "SignedTag": "edge",
        "Digest": "23e7d843e63a3eee29b6b8cfcd10e23dd1ef28f47251a985606a31040bf8e096",
        "Signers": [
          "Repo Admin"
        ]
      },
      {
        "SignedTag": "integ-test-base",
        "Digest": "3952dc48dcc4136ccdde37fbef7e250346538a55a0366e3fccc683336377e372",
        "Signers": [
          "Repo Admin"
        ]
      },
      {
        "SignedTag": "latest",
        "Digest": "d6bfc3baf615dc9618209a8d607ba2a8103d9c8a405b3bd8741d88b4bef36478",
        "Signers": [
          "Repo Admin"
        ]
      }
    ],
    "Signers": [],
    "AdministrativeKeys": [
      {
        "Name": "Repository",
        "Keys": [
          {
            "ID": "5a46c9aaa82ff150bb7305a2d17d0c521c2d784246807b2dc611f436a69041fd"
          }
        ]
      },
      {
        "Name": "Root",
        "Keys": [
          {
            "ID": "a2489bcac7a79aa67b19b96c4a3bf0c675ffdf00c6d2fabe1a5df1115e80adce"
          }
        ]
      }
    ]
  },
  {
    "Name": "notary",
    "SignedTags": [
      {
        "SignedTag": "server",
        "Digest": "71f64ab718a3331dee103bc5afc6bc492914738ce37c2d2f127a8133714ecf5c",
        "Signers": [
          "Repo Admin"
        ]
      },
      {
        "SignedTag": "signer",
        "Digest": "a6122d79b1e74f70b5dd933b18a6d1f99329a4728011079f06b245205f158fe8",
        "Signers": [
          "Repo Admin"
        ]
      }
    ],
    "Signers": [],
    "AdministrativeKeys": [
      {
        "Name": "Root",
        "Keys": [
          {
            "ID": "8cdcdef5bd039f4ab5a029126951b5985eebf57cabdcdc4d21f5b3be8bb4ce92"
          }
        ]
      },
      {
        "Name": "Repository",
        "Keys": [
          {
            "ID": "85bfd031017722f950d480a721f845a2944db26a3dc084040a70f1b0d9bbb3df"
          }
        ]
      }
    ]
  }
]
```

### Formatting

You can print the inspect output in a human-readable format instead of the default
JSON output, by using the `--pretty` option:

### Get details about signatures for a single image tag

```console
$ docker trust inspect --pretty alpine:latest

SIGNED TAG          DIGEST                                                             SIGNERS
latest              1072e499f3f655a032e88542330cf75b02e7bdf673278f701d7ba61629ee3ebe   (Repo Admin)

Administrative keys for alpine:latest:
Repository Key: 5a46c9aaa82ff150bb7305a2d17d0c521c2d784246807b2dc611f436a69041fd
Root Key:       a2489bcac7a79aa67b19b96c4a3bf0c675ffdf00c6d2fabe1a5df1115e80adce
```

The `SIGNED TAG` is the signed image tag with a unique content-addressable
`DIGEST`. `SIGNERS` lists all entities who have signed.

The administrative keys listed specify the root key of trust, as well as
the administrative repository key. These keys are responsible for modifying
signers, and rotating keys for the signed repository.

If signers are set up for the repository via other `docker trust` commands,
`docker trust inspect --pretty` displays them appropriately as a `SIGNER`
and specify their `KEYS`:

```console
$ docker trust inspect --pretty my-image:purple

SIGNED TAG          DIGEST                                                              SIGNERS
purple              941d3dba358621ce3c41ef67b47cf80f701ff80cdf46b5cc86587eaebfe45557    alice, bob, carol

List of signers and their keys:

SIGNER              KEYS
alice               47caae5b3e61, a85aab9d20a4
bob                 034370bcbd77, 82a66673242c
carol               b6f9f8e1aab0

Administrative keys for my-image:
Repository Key: 27df2c8187e7543345c2e0bf3a1262e0bc63a72754e9a7395eac3f747ec23a44
Root Key:       40b66ccc8b176be8c7d365a17f3e046d1c3494e053dd57cfeacfe2e19c4f8e8f
```

However, if other tags are signed in the same image repository,
`docker trust inspect` reports relevant key information.

```console
$ docker trust inspect --pretty alpine:unsigned

No signatures for alpine:unsigned

Administrative keys for alpine:unsigned:
Repository Key: 5a46c9aaa82ff150bb7305a2d17d0c521c2d784246807b2dc611f436a69041fd
Root Key:       a2489bcac7a79aa67b19b96c4a3bf0c675ffdf00c6d2fabe1a5df1115e80adce
```

### Get details about signatures for all image tags in a repository

```console
$ docker trust inspect --pretty alpine

SIGNED TAG          DIGEST                                                             SIGNERS
2.6                 9ace551613070689a12857d62c30ef0daa9a376107ec0fff0e34786cedb3399b   (Repo Admin)
2.7                 9f08005dff552038f0ad2f46b8e65ff3d25641747d3912e3ea8da6785046561a   (Repo Admin)
3.1                 d9477888b78e8c6392e0be8b2e73f8c67e2894ff9d4b8e467d1488fcceec21c8   (Repo Admin)
3.2                 19826d59171c2eb7e90ce52bfd822993bef6a6fe3ae6bb4a49f8c1d0a01e99c7   (Repo Admin)
3.3                 8fd4b76819e1e5baac82bd0a3d03abfe3906e034cc5ee32100d12aaaf3956dc7   (Repo Admin)
3.4                 833ad81ace8277324f3ca8c91c02bdcf1d13988d8ecf8a3f97ecdd69d0390ce9   (Repo Admin)
3.5                 af2a5bd2f8de8fc1ecabf1c76611cdc6a5f1ada1a2bdd7d3816e121b70300308   (Repo Admin)
3.6                 1072e499f3f655a032e88542330cf75b02e7bdf673278f701d7ba61629ee3ebe   (Repo Admin)
edge                79d50d15bd7ea48ea00cf3dd343b0e740c1afaa8e899bee475236ef338e1b53b   (Repo Admin)
latest              1072e499f3f655a032e88542330cf75b02e7bdf673278f701d7ba61629ee3ebe   (Repo Admin)

Administrative keys for alpine:
Repository Key: 5a46c9aaa82ff150bb7305a2d17d0c521c2d784246807b2dc611f436a69041fd
Root Key:       a2489bcac7a79aa67b19b96c4a3bf0c675ffdf00c6d2fabe1a5df1115e80adce
```

Here's an example with signers that are set up by `docker trust` commands:

```console
$ docker trust inspect --pretty my-image

SIGNED TAG          DIGEST                                                              SIGNERS
red                 852cc04935f930a857b630edc4ed6131e91b22073bcc216698842e44f64d2943    alice
blue                f1c38dbaeeb473c36716f6494d803fbfbe9d8a76916f7c0093f227821e378197    alice, bob
green               cae8fedc840f90c8057e1c24637d11865743ab1e61a972c1c9da06ec2de9a139    alice, bob
yellow              9cc65fc3126790e683d1b92f307a71f48f75fa7dd47a7b03145a123eaf0b45ba    carol
purple              941d3dba358621ce3c41ef67b47cf80f701ff80cdf46b5cc86587eaebfe45557    alice, bob, carol
orange              d6c271baa6d271bcc24ef1cbd65abf39123c17d2e83455bdab545a1a9093fc1c    alice

List of signers and their keys for my-image:

SIGNER              KEYS
alice               47caae5b3e61, a85aab9d20a4
bob                 034370bcbd77, 82a66673242c
carol               b6f9f8e1aab0

Administrative keys for my-image:
Repository Key: 27df2c8187e7543345c2e0bf3a1262e0bc63a72754e9a7395eac3f747ec23a44
Root Key:       40b66ccc8b176be8c7d365a17f3e046d1c3494e053dd57cfeacfe2e19c4f8e8f
```
