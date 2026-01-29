# docker stack config and more

# docker stack config

# docker stack config

| Description | Outputs the final config file, after doing merges and interpolations |
| --- | --- |
| Usage | docker stack config [OPTIONS] |

Swarm
This command works with the Swarm orchestrator.

## Description

Outputs the final Compose file, after doing the merges and interpolations of the input Compose files.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -c, --compose-file |  | Path to a Compose file, or-to read from stdin |
| --skip-interpolation |  | Skip interpolation and output only merged config |

## Examples

The following command outputs the result of the merge and interpolation of two Compose files.

```console
$ docker stack config --compose-file docker-compose.yml --compose-file docker-compose.prod.yml
```

The Compose file can also be provided as standard input with `--compose-file -`:

```console
$ cat docker-compose.yml | docker stack config --compose-file -
```

### Skipping interpolation

In some cases, it might be useful to skip interpolation of environment variables.
For example, when you want to pipe the output of this command back to `stack deploy`.

If you have a regex for a redirect route in an environment variable for your webserver you would use two `$` signs to prevent `stack deploy` from interpolating `${1}`.

```yaml
service: webserver
  environment:
    REDIRECT_REGEX=http://host/redirect/$${1}
```

With interpolation, the `stack config` command will replace the environment variable in the Compose file
with `REDIRECT_REGEX=http://host/redirect/${1}`, but then when piping it back to the `stack deploy`
command it will be interpolated again and result in undefined behavior.
That is why, when piping the output back to `stack deploy` one should always prefer the `--skip-interpolation` option.

```console
$ docker stack config --compose-file web.yml --compose-file web.prod.yml --skip-interpolation | docker stack deploy --compose-file -
```

---

# docker stack deploy

# docker stack deploy

| Description | Deploy a new stack or update an existing stack |
| --- | --- |
| Usage | docker stack deploy [OPTIONS] STACK |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker stack up |

Swarm
This command works with the Swarm orchestrator.

## Description

Create and update a stack from a `compose` file on the swarm.

> Note
>
> This is a cluster management command, and must be executed on a swarm
> manager node. To learn about managers and workers, refer to the
> [Swarm mode section](https://docs.docker.com/engine/swarm/) in the
> documentation.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -c, --compose-file |  | API 1.25+Path to a Compose file, or-to read from stdin |
| -d, --detach | true | Exit immediately instead of waiting for the stack services to converge |
| --prune |  | API 1.27+Prune services that are no longer referenced |
| -q, --quiet |  | Suppress progress output |
| --resolve-image | always | API 1.30+Query the registry to resolve image digest and supported platforms (always,changed,never) |
| --with-registry-auth |  | Send registry authentication details to Swarm agents |

## Examples

### Compose file (--compose-file)

The `deploy` command supports Compose file version `3.0` and above.

```console
$ docker stack deploy --compose-file docker-compose.yml vossibility

Ignoring unsupported options: links

Creating network vossibility_vossibility
Creating network vossibility_default
Creating service vossibility_nsqd
Creating service vossibility_logstash
Creating service vossibility_elasticsearch
Creating service vossibility_kibana
Creating service vossibility_ghollector
Creating service vossibility_lookupd
```

The Compose file can also be provided as standard input with `--compose-file -`:

```console
$ cat docker-compose.yml | docker stack deploy --compose-file - vossibility

Ignoring unsupported options: links

Creating network vossibility_vossibility
Creating network vossibility_default
Creating service vossibility_nsqd
Creating service vossibility_logstash
Creating service vossibility_elasticsearch
Creating service vossibility_kibana
Creating service vossibility_ghollector
Creating service vossibility_lookupd
```

If your configuration is split between multiple Compose files, e.g. a base
configuration and environment-specific overrides, you can provide multiple
`--compose-file` flags.

```console
$ docker stack deploy --compose-file docker-compose.yml -c docker-compose.prod.yml vossibility

Ignoring unsupported options: links

Creating network vossibility_vossibility
Creating network vossibility_default
Creating service vossibility_nsqd
Creating service vossibility_logstash
Creating service vossibility_elasticsearch
Creating service vossibility_kibana
Creating service vossibility_ghollector
Creating service vossibility_lookupd
```

You can verify that the services were correctly created:

```console
$ docker service ls

ID            NAME                               MODE        REPLICAS  IMAGE
29bv0vnlm903  vossibility_lookupd                replicated  1/1       nsqio/nsq@sha256:eeba05599f31eba418e96e71e0984c3dc96963ceb66924dd37a47bf7ce18a662
4awt47624qwh  vossibility_nsqd                   replicated  1/1       nsqio/nsq@sha256:eeba05599f31eba418e96e71e0984c3dc96963ceb66924dd37a47bf7ce18a662
4tjx9biia6fs  vossibility_elasticsearch          replicated  1/1       elasticsearch@sha256:12ac7c6af55d001f71800b83ba91a04f716e58d82e748fa6e5a7359eed2301aa
7563uuzr9eys  vossibility_kibana                 replicated  1/1       kibana@sha256:6995a2d25709a62694a937b8a529ff36da92ebee74bafd7bf00e6caf6db2eb03
9gc5m4met4he  vossibility_logstash               replicated  1/1       logstash@sha256:2dc8bddd1bb4a5a34e8ebaf73749f6413c101b2edef6617f2f7713926d2141fe
axqh55ipl40h  vossibility_vossibility-collector  replicated  1/1       icecrime/vossibility-collector@sha256:f03f2977203ba6253988c18d04061c5ec7aab46bca9dfd89a9a1fa4500989fba
```

---

# docker stack ls

# docker stack ls

| Description | List stacks |
| --- | --- |
| Usage | docker stack ls [OPTIONS] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker stack list |

Swarm
This command works with the Swarm orchestrator.

## Description

Lists the stacks.

> Note
>
> This is a cluster management command, and must be executed on a swarm
> manager node. To learn about managers and workers, refer to the
> [Swarm mode section](https://docs.docker.com/engine/swarm/) in the
> documentation.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --format |  | Format output using a custom template:'table': Print output in table format with column headers (default)'table TEMPLATE': Print output in table format using the given Go template'json': Print in JSON format'TEMPLATE': Print output using the given Go template.Refer tohttps://docs.docker.com/go/formatting/for more information about formatting output with templates |

## Examples

The following command shows all stacks and some additional information:

```console
$ docker stack ls

ID                 SERVICES            ORCHESTRATOR
myapp              2                   Kubernetes
vossibility-stack  6                   Swarm
```

### Format the output (--format)

The formatting option (`--format`) pretty-prints stacks using a Go template.

Valid placeholders for the Go template are listed below:

| Placeholder | Description |
| --- | --- |
| .Name | Stack name |
| .Services | Number of services |
| .Orchestrator | Orchestrator name |
| .Namespace | Namespace |

When using the `--format` option, the `stack ls` command either outputs
the data exactly as the template declares or, when using the
`table` directive, includes column headers as well.

The following example uses a template without headers and outputs the
`Name` and `Services` entries separated by a colon (`:`) for all stacks:

```console
$ docker stack ls --format "{{.Name}}: {{.Services}}"
web-server: 1
web-cache: 4
```

To list all stacks in JSON format, use the `json` directive:

```console
$ docker stack ls --format json
{"Name":"myapp","Namespace":"","Orchestrator":"Swarm","Services":"3"}
```

---

# docker stack ps

# docker stack ps

| Description | List the tasks in the stack |
| --- | --- |
| Usage | docker stack ps [OPTIONS] STACK |

Swarm
This command works with the Swarm orchestrator.

## Description

Lists the tasks that are running as part of the specified stack.

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
| --no-resolve |  | Do not map IDs to Names |
| --no-trunc |  | Do not truncate output |
| -q, --quiet |  | Only display task IDs |

## Examples

### List the tasks that are part of a stack

The following command shows all the tasks that are part of the `voting` stack:

```console
$ docker stack ps voting

ID                  NAME                  IMAGE                                          NODE   DESIRED STATE  CURRENT STATE          ERROR  PORTS
xim5bcqtgk1b        voting_worker.1       dockersamples/examplevotingapp_worker:latest   node2  Running        Running 2 minutes ago
q7yik0ks1in6        voting_result.1       dockersamples/examplevotingapp_result:before   node1  Running        Running 2 minutes ago
rx5yo0866nfx        voting_vote.1         dockersamples/examplevotingapp_vote:before     node3  Running        Running 2 minutes ago
tz6j82jnwrx7        voting_db.1           postgres:9.4                                   node1  Running        Running 2 minutes ago
w48spazhbmxc        voting_redis.1        redis:alpine                                   node2  Running        Running 3 minutes ago
6jj1m02freg1        voting_visualizer.1   dockersamples/visualizer:stable                node1  Running        Running 2 minutes ago
kqgdmededccb        voting_vote.2         dockersamples/examplevotingapp_vote:before     node2  Running        Running 2 minutes ago
t72q3z038jeh        voting_redis.2        redis:alpine                                   node3  Running        Running 3 minutes ago
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
$ docker stack ps -f "id=t" voting

ID                  NAME                IMAGE               NODE         DESIRED STATE       CURRENTSTATE            ERROR  PORTS
tz6j82jnwrx7        voting_db.1         postgres:9.4        node1        Running             Running 14 minutes ago
t72q3z038jeh        voting_redis.2      redis:alpine        node3        Running             Running 14 minutes ago
```

#### name

The `name` filter matches on task names.

```console
$ docker stack ps -f "name=voting_redis" voting

ID                  NAME                IMAGE               NODE         DESIRED STATE       CURRENTSTATE            ERROR  PORTS
w48spazhbmxc        voting_redis.1      redis:alpine        node2        Running             Running 17 minutes ago
t72q3z038jeh        voting_redis.2      redis:alpine        node3        Running             Running 17 minutes ago
```

#### node

The `node` filter matches on a node name or a node ID.

```console
$ docker stack ps -f "node=node1" voting

ID                  NAME                  IMAGE                                          NODE   DESIRED STATE  CURRENT STATE          ERROR  PORTS
q7yik0ks1in6        voting_result.1       dockersamples/examplevotingapp_result:before   node1  Running        Running 18 minutes ago
tz6j82jnwrx7        voting_db.1           postgres:9.4                                   node1  Running        Running 18 minutes ago
6jj1m02freg1        voting_visualizer.1   dockersamples/visualizer:stable                node1  Running        Running 18 minutes ago
```

#### desired-state

The `desired-state` filter can take the values `running`, `shutdown`, `ready` or `accepted`.

```console
$ docker stack ps -f "desired-state=running" voting

ID                  NAME                  IMAGE                                          NODE   DESIRED STATE  CURRENT STATE           ERROR  PORTS
xim5bcqtgk1b        voting_worker.1       dockersamples/examplevotingapp_worker:latest   node2  Running        Running 21 minutes ago
q7yik0ks1in6        voting_result.1       dockersamples/examplevotingapp_result:before   node1  Running        Running 21 minutes ago
rx5yo0866nfx        voting_vote.1         dockersamples/examplevotingapp_vote:before     node3  Running        Running 21 minutes ago
tz6j82jnwrx7        voting_db.1           postgres:9.4                                   node1  Running        Running 21 minutes ago
w48spazhbmxc        voting_redis.1        redis:alpine                                   node2  Running        Running 21 minutes ago
6jj1m02freg1        voting_visualizer.1   dockersamples/visualizer:stable                node1  Running        Running 21 minutes ago
kqgdmededccb        voting_vote.2         dockersamples/examplevotingapp_vote:before     node2  Running        Running 21 minutes ago
t72q3z038jeh        voting_redis.2        redis:alpine                                   node3  Running        Running 21 minutes ago
```

### Format the output (--format)

The formatting options (`--format`) pretty-prints tasks output using a Go template.

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

When using the `--format` option, the `stack ps` command will either
output the data exactly as the template declares or, when using the
`table` directive, includes column headers as well.

The following example uses a template without headers and outputs the
`Name` and `Image` entries separated by a colon (`:`) for all tasks:

```console
$ docker stack ps --format "{{.Name}}: {{.Image}}" voting

voting_worker.1: dockersamples/examplevotingapp_worker:latest
voting_result.1: dockersamples/examplevotingapp_result:before
voting_vote.1: dockersamples/examplevotingapp_vote:before
voting_db.1: postgres:9.4
voting_redis.1: redis:alpine
voting_visualizer.1: dockersamples/visualizer:stable
voting_vote.2: dockersamples/examplevotingapp_vote:before
voting_redis.2: redis:alpine
```

To list all tasks in JSON format, use the `json` directive:

```console
$ docker stack ps --format json myapp
{"CurrentState":"Preparing 23 seconds ago","DesiredState":"Running","Error":"","ID":"2ufjubh79tn0","Image":"localstack/localstack:latest","Name":"myapp_localstack.1","Node":"docker-desktop","Ports":""}
{"CurrentState":"Running 20 seconds ago","DesiredState":"Running","Error":"","ID":"roee387ngf5r","Image":"redis:6.0.9-alpine3.12","Name":"myapp_redis.1","Node":"docker-desktop","Ports":""}
{"CurrentState":"Preparing 13 seconds ago","DesiredState":"Running","Error":"","ID":"yte68ouq7glh","Image":"postgres:13.2-alpine","Name":"myapp_repos-db.1","Node":"docker-desktop","Ports":""}
```

### Do not map IDs to Names (--no-resolve)

The `--no-resolve` option shows IDs for task name, without mapping IDs to Names.

```console
$ docker stack ps --no-resolve voting

ID                  NAME                          IMAGE                                          NODE                        DESIRED STATE  CURRENT STATE            ERROR  PORTS
xim5bcqtgk1b        10z9fjfqzsxnezo4hb81p8mqg.1   dockersamples/examplevotingapp_worker:latest   qaqt4nrzo775jrx6detglho01   Running        Running 30 minutes ago
q7yik0ks1in6        hbxltua1na7mgqjnidldv5m65.1   dockersamples/examplevotingapp_result:before   mxpaef1tlh23s052erw88a4w5   Running        Running 30 minutes ago
rx5yo0866nfx        qyprtqw1g5nrki557i974ou1d.1   dockersamples/examplevotingapp_vote:before     kanqcxfajd1r16wlnqcblobmm   Running        Running 31 minutes ago
tz6j82jnwrx7        122f0xxngg17z52be7xspa72x.1   postgres:9.4                                   mxpaef1tlh23s052erw88a4w5   Running        Running 31 minutes ago
w48spazhbmxc        tg61x8myx563ueo3urmn1ic6m.1   redis:alpine                                   qaqt4nrzo775jrx6detglho01   Running        Running 31 minutes ago
6jj1m02freg1        8cqlyi444kzd3panjb7edh26v.1   dockersamples/visualizer:stable                mxpaef1tlh23s052erw88a4w5   Running        Running 31 minutes ago
kqgdmededccb        qyprtqw1g5nrki557i974ou1d.2   dockersamples/examplevotingapp_vote:before     qaqt4nrzo775jrx6detglho01   Running        Running 31 minutes ago
t72q3z038jeh        tg61x8myx563ueo3urmn1ic6m.2   redis:alpine                                   kanqcxfajd1r16wlnqcblobmm   Running        Running 31 minutes ago
```

### Do not truncate output (--no-trunc)

When deploying a service, docker resolves the digest for the service's
image, and pins the service to that digest. The digest is not shown by
default, but is printed if `--no-trunc` is used. The `--no-trunc` option
also shows the non-truncated task IDs, and error-messages, as can be seen below:

```console
$ docker stack ps --no-trunc voting

ID                          NAME                  IMAGE                                                                                                                 NODE   DESIRED STATE  CURREN STATE           ERROR  PORTS
xim5bcqtgk1bxqz91jzo4a1s5   voting_worker.1       dockersamples/examplevotingapp_worker:latest@sha256:3e4ddf59c15f432280a2c0679c4fc5a2ee5a797023c8ef0d3baf7b1385e9fed   node2  Running        Runnin 32 minutes ago
q7yik0ks1in6kv32gg6y6yjf7   voting_result.1       dockersamples/examplevotingapp_result:before@sha256:83b56996e930c292a6ae5187fda84dd6568a19d97cdb933720be15c757b7463   node1  Running        Runnin 32 minutes ago
rx5yo0866nfxc58zf4irsss6n   voting_vote.1         dockersamples/examplevotingapp_vote:before@sha256:8e64b182c87de902f2b72321c89b4af4e2b942d76d0b772532ff27ec4c6ebf6     node3  Running        Runnin 32 minutes ago
tz6j82jnwrx7n2offljp3mn03   voting_db.1           postgres:9.4@sha256:6046af499eae34d2074c0b53f9a8b404716d415e4a03e68bc1d2f8064f2b027                                   node1  Running        Runnin 32 minutes ago
w48spazhbmxcmbjfi54gs7x90   voting_redis.1        redis:alpine@sha256:9cd405cd1ec1410eaab064a1383d0d8854d1ef74a54e1e4a92fb4ec7bdc3ee7                                   node2  Running        Runnin 32 minutes ago
6jj1m02freg1n3z9n1evrzsbl   voting_visualizer.1   dockersamples/visualizer:stable@sha256:f924ad66c8e94b10baaf7bdb9cd491ef4e982a1d048a56a17e02bf5945401e5                node1  Running        Runnin 32 minutes ago
kqgdmededccbhz2wuc0e9hx7g   voting_vote.2         dockersamples/examplevotingapp_vote:before@sha256:8e64b182c87de902f2b72321c89b4af4e2b942d76d0b772532ff27ec4c6ebf6     node2  Running        Runnin 32 minutes ago
t72q3z038jehe1wbh9gdum076   voting_redis.2        redis:alpine@sha256:9cd405cd1ec1410eaab064a1383d0d8854d1ef74a54e1e4a92fb4ec7bdc3ee7                                   node3  Running        Runnin 32 minutes ago
```

### Only display task IDs (-q, --quiet)

The `-q `or `--quiet` option only shows IDs of the tasks in the stack.
This example outputs all task IDs of the `voting` stack:

```console
$ docker stack ps -q voting
xim5bcqtgk1b
q7yik0ks1in6
rx5yo0866nfx
tz6j82jnwrx7
w48spazhbmxc
6jj1m02freg1
kqgdmededccb
t72q3z038jeh
```

This option can be used to perform batch operations. For example, you can use
the task IDs as input for other commands, such as `docker inspect`. The
following example inspects all tasks of the `voting` stack:

```console
$ docker inspect $(docker stack ps -q voting)

[
    {
        "ID": "xim5bcqtgk1b1gk0krq1",
        "Version": {
<...>
```

---

# docker stack rm

# docker stack rm

| Description | Remove one or more stacks |
| --- | --- |
| Usage | docker stack rm [OPTIONS] STACK [STACK...] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker stack removedocker stack down |

Swarm
This command works with the Swarm orchestrator.

## Description

Remove the stack from the swarm.

> Note
>
> This is a cluster management command, and must be executed on a swarm
> manager node. To learn about managers and workers, refer to the
> [Swarm mode section](https://docs.docker.com/engine/swarm/) in the
> documentation.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -d, --detach | true | Do not wait for stack removal |

## Examples

### Remove a stack

This will remove the stack with the name `myapp`. Services, networks, and secrets
associated with the stack will be removed.

```console
$ docker stack rm myapp

Removing service myapp_redis
Removing service myapp_web
Removing service myapp_lb
Removing network myapp_default
Removing network myapp_frontend
```

### Remove multiple stacks

This will remove all the specified stacks, `myapp` and `vossibility`. Services,
networks, and secrets associated with all the specified stacks will be removed.

```console
$ docker stack rm myapp vossibility

Removing service myapp_redis
Removing service myapp_web
Removing service myapp_lb
Removing network myapp_default
Removing network myapp_frontend
Removing service vossibility_nsqd
Removing service vossibility_logstash
Removing service vossibility_elasticsearch
Removing service vossibility_kibana
Removing service vossibility_ghollector
Removing service vossibility_lookupd
Removing network vossibility_default
Removing network vossibility_vossibility
```

---

# docker stack services

# docker stack services

| Description | List the services in the stack |
| --- | --- |
| Usage | docker stack services [OPTIONS] STACK |

Swarm
This command works with the Swarm orchestrator.

## Description

Lists the services that are running as part of the specified stack.

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

The following command shows all services in the `myapp` stack:

```console
$ docker stack services myapp

ID            NAME            REPLICAS  IMAGE                                                                          COMMAND
7be5ei6sqeye  myapp_web       1/1       nginx@sha256:23f809e7fd5952e7d5be065b4d3643fbbceccd349d537b62a123ef2201bc886f
dn7m7nhhfb9y  myapp_db        1/1       mysql@sha256:a9a5b559f8821fe73d58c3606c812d1c044868d42c63817fa5125fd9d8b7b539
```

### Filtering (--filter)

The filtering flag (`-f` or `--filter`) format is a `key=value` pair. If there
is more than one filter, then pass multiple flags (e.g. `--filter "foo=bar" --filter "bif=baz"`).
Multiple filter flags are combined as an `OR` filter.

The following command shows both the `web` and `db` services:

```console
$ docker stack services --filter name=myapp_web --filter name=myapp_db myapp

ID            NAME            REPLICAS  IMAGE                                                                          COMMAND
7be5ei6sqeye  myapp_web       1/1       nginx@sha256:23f809e7fd5952e7d5be065b4d3643fbbceccd349d537b62a123ef2201bc886f
dn7m7nhhfb9y  myapp_db        1/1       mysql@sha256:a9a5b559f8821fe73d58c3606c812d1c044868d42c63817fa5125fd9d8b7b539
```

The currently supported filters are:

- id / ID (`--filter id=7be5ei6sqeye`, or `--filter ID=7be5ei6sqeye`)
- label (`--filter label=key=value`)
- mode (`--filter mode=replicated`, or `--filter mode=global`)
  - Swarm: not supported
- name (`--filter name=myapp_web`)
- node (`--filter node=mynode`)
  - Swarm: not supported
- service (`--filter service=web`)
  - Swarm: not supported

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

When using the `--format` option, the `stack services` command will either
output the data exactly as the template declares or, when using the
`table` directive, includes column headers as well.

The following example uses a template without headers and outputs the
`ID`, `Mode`, and `Replicas` entries separated by a colon (`:`) for all services:

```console
$ docker stack services --format "{{.ID}}: {{.Mode}} {{.Replicas}}"

0zmvwuiu3vue: replicated 10/10
fm6uf97exkul: global 5/5
```

To list all services in JSON format, use the `json` directive:

```console
$ docker stack services ls --format json
{"ID":"0axqbl293vwm","Image":"localstack/localstack:latest","Mode":"replicated","Name":"myapp_localstack","Ports":"*:4566-\u003e4566/tcp, *:8080-\u003e8080/tcp","Replicas":"0/1"}
{"ID":"384xvtzigz3p","Image":"redis:6.0.9-alpine3.12","Mode":"replicated","Name":"myapp_redis","Ports":"*:6379-\u003e6379/tcp","Replicas":"1/1"}
{"ID":"hyujct8cnjkk","Image":"postgres:13.2-alpine","Mode":"replicated","Name":"myapp_repos-db","Ports":"*:5432-\u003e5432/tcp","Replicas":"0/1"}
```

---

# docker stack

# docker stack

| Description | Manage Swarm stacks |
| --- | --- |
| Usage | docker stack [OPTIONS] |

Swarm
This command works with the Swarm orchestrator.

## Description

Manage stacks.

## Subcommands

| Command | Description |
| --- | --- |
| docker stack config | Outputs the final config file, after doing merges and interpolations |
| docker stack deploy | Deploy a new stack or update an existing stack |
| docker stack ls | List stacks |
| docker stack ps | List the tasks in the stack |
| docker stack rm | Remove one or more stacks |
| docker stack services | List the services in the stack |

---

# docker swarm ca

# docker swarm ca

| Description | Display and rotate the root CA |
| --- | --- |
| Usage | docker swarm ca [OPTIONS] |

Swarm
This command works with the Swarm orchestrator.

## Description

View or rotate the current swarm CA certificate.

> Note
>
> This is a cluster management command, and must be executed on a swarm
> manager node. To learn about managers and workers, refer to the
> [Swarm mode section](https://docs.docker.com/engine/swarm/) in the
> documentation.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --ca-cert |  | Path to the PEM-formatted root CA certificate to use for the new cluster |
| --ca-key |  | Path to the PEM-formatted root CA key to use for the new cluster |
| --cert-expiry | 2160h0m0s | Validity period for node certificates (ns|us|ms|s|m|h) |
| -d, --detach |  | Exit immediately instead of waiting for the root rotation to converge |
| --external-ca |  | Specifications of one or more certificate signing endpoints |
| -q, --quiet |  | Suppress progress output |
| --rotate |  | Rotate the swarm CA - if no certificate or key are provided, new ones will be generated |

## Examples

Run the `docker swarm ca` command without any options to view the current root CA certificate
in PEM format.

```console
$ docker swarm ca

-----BEGIN CERTIFICATE-----
MIIBazCCARCgAwIBAgIUJPzo67QC7g8Ebg2ansjkZ8CbmaswCgYIKoZIzj0EAwIw
EzERMA8GA1UEAxMIc3dhcm0tY2EwHhcNMTcwNTAzMTcxMDAwWhcNMzcwNDI4MTcx
MDAwWjATMREwDwYDVQQDEwhzd2FybS1jYTBZMBMGByqGSM49AgEGCCqGSM49AwEH
A0IABKL6/C0sihYEb935wVPRA8MqzPLn3jzou0OJRXHsCLcVExigrMdgmLCC+Va4
+sJ+SLVO1eQbvLHH8uuDdF/QOU6jQjBAMA4GA1UdDwEB/wQEAwIBBjAPBgNVHRMB
Af8EBTADAQH/MB0GA1UdDgQWBBSfUy5bjUnBAx/B0GkOBKp91XvxzjAKBggqhkjO
PQQDAgNJADBGAiEAnbvh0puOS5R/qvy1PMHY1iksYKh2acsGLtL/jAIvO4ACIQCi
lIwQqLkJ48SQqCjG1DBTSBsHmMSRT+6mE2My+Z3GKA==
-----END CERTIFICATE-----
```

Pass the `--rotate` flag (and optionally a `--ca-cert`, along with a `--ca-key` or
`--external-ca` parameter flag), in order to rotate the current swarm root CA.

```console
$ docker swarm ca --rotate
desired root digest: sha256:05da740cf2577a25224c53019e2cce99bcc5ba09664ad6bb2a9425d9ebd1b53e
  rotated TLS certificates:  [=========================>                         ] 1/2 nodes
  rotated CA certificates:   [>                                                  ] 0/2 nodes
```

Once the rotation os finished (all the progress bars have completed) the now-current
CA certificate will be printed:

```console
$ docker swarm ca --rotate
desired root digest: sha256:05da740cf2577a25224c53019e2cce99bcc5ba09664ad6bb2a9425d9ebd1b53e
  rotated TLS certificates:  [==================================================>] 2/2 nodes
  rotated CA certificates:   [==================================================>] 2/2 nodes
-----BEGIN CERTIFICATE-----
MIIBazCCARCgAwIBAgIUFynG04h5Rrl4lKyA4/E65tYKg8IwCgYIKoZIzj0EAwIw
EzERMA8GA1UEAxMIc3dhcm0tY2EwHhcNMTcwNTE2MDAxMDAwWhcNMzcwNTExMDAx
MDAwWjATMREwDwYDVQQDEwhzd2FybS1jYTBZMBMGByqGSM49AgEGCCqGSM49AwEH
A0IABC2DuNrIETP7C7lfiEPk39tWaaU0I2RumUP4fX4+3m+87j0DU0CsemUaaOG6
+PxHhGu2VXQ4c9pctPHgf7vWeVajQjBAMA4GA1UdDwEB/wQEAwIBBjAPBgNVHRMB
Af8EBTADAQH/MB0GA1UdDgQWBBSEL02z6mCI3SmMDmITMr12qCRY2jAKBggqhkjO
PQQDAgNJADBGAiEA263Eb52+825EeNQZM0AME+aoH1319Zp9/J5ijILW+6ACIQCg
gyg5u9Iliel99l7SuMhNeLkrU7fXs+Of1nTyyM73ig==
-----END CERTIFICATE-----
```

### Root CA rotation (--rotate)

> Note
>
> Mirantis Kubernetes Engine (MKE), formerly known as Docker UCP, provides an external
> certificate manager service for the swarm. If you run swarm on MKE, you shouldn't
> rotate the CA certificates manually. Instead, contact Mirantis support if you need
> to rotate a certificate.

Root CA Rotation is recommended if one or more of the swarm managers have been
compromised, so that those managers can no longer connect to or be trusted by
any other node in the cluster.

Alternately, root CA rotation can be used to give control of the swarm CA
to an external CA, or to take control back from an external CA.

The `--rotate` flag does not require any parameters to do a rotation, but you can
optionally specify a certificate and key, or a certificate and external CA URL,
and those will be used instead of an automatically-generated certificate/key pair.

Because the root CA key should be kept secret, if provided it will not be visible
when viewing swarm any information via the CLI or API.

The root CA rotation will not be completed until all registered nodes have
rotated their TLS certificates. If the rotation is not completing within a
reasonable amount of time, try running
`docker node ls --format '{{.ID}} {{.Hostname}} {{.Status}} {{.TLSStatus}}'` to
see if any nodes are down or otherwise unable to rotate TLS certificates.

### Run root CA rotation in detached mode (--detach)

Initiate the root CA rotation, but do not wait for the completion of or display the
progress of the rotation.

---

# docker swarm init

# docker swarm init

| Description | Initialize a swarm |
| --- | --- |
| Usage | docker swarm init [OPTIONS] |

Swarm
This command works with the Swarm orchestrator.

## Description

Initialize a swarm. The Docker Engine targeted by this command becomes a manager
in the newly created single-node swarm.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --advertise-addr |  | Advertised address (format:<ip|interface>[:port]) |
| --autolock |  | Enable manager autolocking (requiring an unlock key to start a stopped manager) |
| --availability | active | Availability of the node (active,pause,drain) |
| --cert-expiry | 2160h0m0s | Validity period for node certificates (ns|us|ms|s|m|h) |
| --data-path-addr |  | API 1.31+Address or interface to use for data path traffic (format:<ip|interface>) |
| --data-path-port |  | API 1.40+Port number to use for data path traffic (1024 - 49151). If no value is set or is set to 0, the default port (4789) is used. |
| --default-addr-pool |  | API 1.39+default address pool in CIDR format |
| --default-addr-pool-mask-length | 24 | API 1.39+default address pool subnet mask length |
| --dispatcher-heartbeat | 5s | Dispatcher heartbeat period (ns|us|ms|s|m|h) |
| --external-ca |  | Specifications of one or more certificate signing endpoints |
| --force-new-cluster |  | Force create a new cluster from current state |
| --listen-addr | 0.0.0.0:2377 | Listen address (format:<ip|interface>[:port]) |
| --max-snapshots |  | API 1.25+Number of additional Raft snapshots to retain |
| --snapshot-interval | 10000 | API 1.25+Number of log entries between Raft snapshots |
| --task-history-limit | 5 | Task history retention limit |

## Examples

```console
$ docker swarm init --advertise-addr 192.168.99.121

Swarm initialized: current node (bvz81updecsj6wjz393c09vti) is now a manager.

To add a worker to this swarm, run the following command:

    docker swarm join --token SWMTKN-1-3pu6hszjas19xyp7ghgosyx9k8atbfcr8p2is99znpy26u2lkl-1awxwuwd3z9j1z3puu7rcgdbx 172.17.0.2:2377

To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.
```

The `docker swarm init` command generates two random tokens: a worker token and
a manager token. When you join a new node to the swarm, the node joins as a
worker or manager node based upon the token you pass to
[swarm
join](https://docs.docker.com/reference/cli/docker/swarm/join/).

After you create the swarm, you can display or rotate the token using
[swarm join-token](https://docs.docker.com/reference/cli/docker/swarm/join-token/).

### Protect manager keys and data (--autolock)

The `--autolock` flag enables automatic locking of managers with an encryption
key. The private keys and data stored by all managers are protected by the
encryption key printed in the output, and is inaccessible without it. Make sure
to store this key securely, in order to reactivate a manager after it restarts.
Pass the key to the `docker swarm unlock` command to reactivate the manager.
You can disable autolock by running `docker swarm update --autolock=false`.
After disabling it, the encryption key is no longer required to start the
manager, and it will start up on its own without user intervention.

### Configure node healthcheck frequency (--dispatcher-heartbeat)

The `--dispatcher-heartbeat` flag sets the frequency at which nodes are told to
report their health.

### Use an external certificate authority (--external-ca)

This flag sets up the swarm to use an external CA to issue node certificates.
The value takes the form `protocol=X,url=Y`. The value for `protocol` specifies
what protocol should be used to send signing requests to the external CA.
Currently, the only supported value is `cfssl`. The URL specifies the endpoint
where signing requests should be submitted.

### Force-restart node as a single-mode manager (--force-new-cluster)

This flag forces an existing node that was part of a quorum that was lost to
restart as a single-node Manager without losing its data.

### Specify interface for inbound control plane traffic (--listen-addr)

The node listens for inbound swarm manager traffic on this address. The default
is to listen on `0.0.0.0:2377`. It is also possible to specify a network
interface to listen on that interface's address; for example `--listen-addr eth0:2377`.

Specifying a port is optional. If the value is a bare IP address or interface
name, the default port 2377 is used.

### Specify interface for outbound control plane traffic (--advertise-addr)

The `--advertise-addr` flag specifies the address that will be advertised to
other members of the swarm for API access and overlay networking. If
unspecified, Docker will check if the system has a single IP address, and use
that IP address with the listening port (see `--listen-addr`). If the system
has multiple IP addresses, `--advertise-addr` must be specified so that the
correct address is chosen for inter-manager communication and overlay
networking.

It is also possible to specify a network interface to advertise that
interface's address; for example `--advertise-addr eth0:2377`.

Specifying a port is optional. If the value is a bare IP address or interface
name, the default port 2377 is used.

### Specify interface for data traffic (--data-path-addr)

The `--data-path-addr` flag specifies the address that global scope network
drivers will publish towards other nodes in order to reach the containers
running on this node. Using this parameter you can separate the container's
data traffic from the management traffic of the cluster.

If unspecified, the IP address or interface of the advertise address is used.

Setting `--data-path-addr` does not restrict which interfaces or source IP
addresses the VXLAN socket is bound to. Similar to `--advertise-addr`, the
purpose of this flag is to inform other members of the swarm about which
address to use for control plane traffic. To restrict access to the VXLAN port
of the node, use firewall rules.

### Configure port number for data traffic (--data-path-port)

The `--data-path-port` flag allows you to configure the UDP port number to use
for data path traffic. The provided port number must be within the 1024 - 49151
range. If this flag isn't set, or if it's set to 0, the default port number
4789 is used. The data path port can only be configured when initializing the
swarm, and applies to all nodes that join the swarm. The following example
initializes a new Swarm, and configures the data path port to UDP port 7777;

```console
$ docker swarm init --data-path-port=7777
```

After the swarm is initialized, use the `docker info` command to verify that
the port is configured:

```console
$ docker info
<...>
ClusterID: 9vs5ygs0gguyyec4iqf2314c0
Managers: 1
Nodes: 1
Data Path Port: 7777
<...>
```

### Specify default subnet pools (--default-addr-pool)

The `--default-addr-pool` flag specifies default subnet pools for global scope
networks. For example, to specify two address pools:

```console
$ docker swarm init \
  --default-addr-pool 30.30.0.0/16 \
  --default-addr-pool 40.40.0.0/16
```

Use the `--default-addr-pool-mask-length` flag to specify the default subnet
pools mask length for the subnet pools.

### Set limit for number of snapshots to keep (--max-snapshots)

This flag sets the number of old Raft snapshots to retain in addition to the
current Raft snapshots. By default, no old snapshots are retained. This option
may be used for debugging, or to store old snapshots of the swarm state for
disaster recovery purposes.

### Configure Raft snapshot log interval (--snapshot-interval)

The `--snapshot-interval` flag specifies how many log entries to allow in
between Raft snapshots. Setting this to a high number will trigger snapshots
less frequently. Snapshots compact the Raft log and allow for more efficient
transfer of the state to new managers. However, there is a performance cost to
taking snapshots frequently.

### Configure the availability of a manager (--availability)

The `--availability` flag specifies the availability of the node at the time
the node joins a master. Possible availability values are `active`, `pause`, or
`drain`.

This flag is useful in certain situations. For example, a cluster may want to
have dedicated manager nodes that don't serve as worker nodes. You can do this
by passing `--availability=drain` to `docker swarm init`.

---

# docker swarm join

# docker swarm join-token

| Description | Manage join tokens |
| --- | --- |
| Usage | docker swarm join-token [OPTIONS] (worker|manager) |

Swarm
This command works with the Swarm orchestrator.

## Description

Join tokens are secrets that allow a node to join the swarm. There are two
different join tokens available, one for the worker role and one for the manager
role. You pass the token using the `--token` flag when you run
[swarm join](https://docs.docker.com/reference/cli/docker/swarm/join/). Nodes use the join token only when they join the
swarm.

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
| --rotate |  | Rotate join token |

## Examples

You can view or rotate the join tokens using `swarm join-token`.

As a convenience, you can pass `worker` or `manager` as an argument to
`join-token` to print the full `docker swarm join` command to join a new node to
the swarm:

```console
$ docker swarm join-token worker

To add a worker to this swarm, run the following command:

    docker swarm join \
    --token SWMTKN-1-3pu6hszjas19xyp7ghgosyx9k8atbfcr8p2is99znpy26u2lkl-1awxwuwd3z9j1z3puu7rcgdbx \
    172.17.0.2:2377

$ docker swarm join-token manager

To add a manager to this swarm, run the following command:

    docker swarm join \
    --token SWMTKN-1-3pu6hszjas19xyp7ghgosyx9k8atbfcr8p2is99znpy26u2lkl-7p73s1dx5in4tatdymyhg9hu2 \
    172.17.0.2:2377
```

Use the `--rotate` flag to generate a new join token for the specified role:

```console
$ docker swarm join-token --rotate worker

Successfully rotated worker join token.

To add a worker to this swarm, run the following command:

    docker swarm join \
    --token SWMTKN-1-3pu6hszjas19xyp7ghgosyx9k8atbfcr8p2is99znpy26u2lkl-b30ljddcqhef9b9v4rs7mel7t \
    172.17.0.2:2377
```

After using `--rotate`, only the new token will be valid for joining with the specified role.

The `-q` (or `--quiet`) flag only prints the token:

```console
$ docker swarm join-token -q worker

SWMTKN-1-3pu6hszjas19xyp7ghgosyx9k8atbfcr8p2is99znpy26u2lkl-b30ljddcqhef9b9v4rs7mel7t
```

### --rotate

Because tokens allow new nodes to join the swarm, you should keep them secret.
Be particularly careful with manager tokens since they allow new manager nodes
to join the swarm. A rogue manager has the potential to disrupt the operation of
your swarm.

Rotate your swarm's join token if a token gets checked-in to version control,
stolen, or a node is compromised. You may also want to periodically rotate the
token to ensure any unknown token leaks do not allow a rogue node to join
the swarm.

To rotate the join token and print the newly generated token, run
`docker swarm join-token --rotate` and pass the role: `manager` or `worker`.

Rotating a join-token means that no new nodes will be able to join the swarm
using the old token. Rotation does not affect existing nodes in the swarm
because the join token is only used for authorizing new nodes joining the swarm.

### --quiet

Only print the token. Do not print a complete command for joining.
