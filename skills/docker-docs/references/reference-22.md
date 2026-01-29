# docker compose and more

# docker compose

# docker compose

| Description | Docker Compose |
| --- | --- |
| Usage | docker compose |

## Description

Define and run multi-container applications with Docker

## Options

| Option | Default | Description |
| --- | --- | --- |
| --all-resources |  | Include all resources, even those not used by services |
| --ansi | auto | Control when to print ANSI control characters ("never"|"always"|"auto") |
| --compatibility |  | Run compose in backward compatibility mode |
| --dry-run |  | Execute command in dry run mode |
| --env-file |  | Specify an alternate environment file |
| -f, --file |  | Compose configuration files |
| --parallel | -1 | Control max parallelism, -1 for unlimited |
| --profile |  | Specify a profile to enable |
| --progress |  | Set type of progress output (auto, tty, plain, json, quiet) |
| --project-directory |  | Specify an alternate working directory(default: the path of the, first specified, Compose file) |
| -p, --project-name |  | Project name |

## Examples

### Use-fto specify the name and path of one or more Compose files

Use the `-f` flag to specify the location of a Compose
[configuration file](https://docs.docker.com/reference/compose-file/).

#### Specifying multiple Compose files

You can supply multiple `-f` configuration files. When you supply multiple files, Compose combines them into a single
configuration. Compose builds the configuration in the order you supply the files. Subsequent files override and add
to their predecessors.

For example, consider this command line:

```console
$ docker compose -f compose.yaml -f compose.admin.yaml run backup_db
```

The `compose.yaml` file might specify a `webapp` service.

```yaml
services:
  webapp:
    image: examples/web
    ports:
      - "8000:8000"
    volumes:
      - "/data"
```

If the `compose.admin.yaml` also specifies this same service, any matching fields override the previous file.
New values, add to the `webapp` service configuration.

```yaml
services:
  webapp:
    build: .
    environment:
      - DEBUG=1
```

When you use multiple Compose files, all paths in the files are relative to the first configuration file specified
with `-f`. You can use the `--project-directory` option to override this base path.

Use a `-f` with `-` (dash) as the filename to read the configuration from stdin. When stdin is used all paths in the
configuration are relative to the current working directory.

The `-f` flag is optional. If you don’t provide this flag on the command line, Compose traverses the working directory
and its parent directories looking for a `compose.yaml` or `docker-compose.yaml` file.

#### Specifying a path to a single Compose file

You can use the `-f` flag to specify a path to a Compose file that is not located in the current directory, either
from the command line or by setting up a `COMPOSE_FILE` environment variable in your shell or in an environment file.

For an example of using the `-f` option at the command line, suppose you are running the Compose Rails sample, and
have a `compose.yaml` file in a directory called `sandbox/rails`. You can use a command like `docker compose pull` to
get the postgres image for the db service from anywhere by using the `-f` flag as follows:

```console
$ docker compose -f ~/sandbox/rails/compose.yaml pull db
```

#### Using an OCI published artifact

You can use the `-f` flag with the `oci://` prefix to reference a Compose file that has been published to an OCI registry.
This allows you to distribute and version your Compose configurations as OCI artifacts.

To use a Compose file from an OCI registry:

```console
$ docker compose -f oci://registry.example.com/my-compose-project:latest up
```

You can also combine OCI artifacts with local files:

```console
$ docker compose -f oci://registry.example.com/my-compose-project:v1.0 -f compose.override.yaml up
```

The OCI artifact must contain a valid Compose file. You can publish Compose files to an OCI registry using the
`docker compose publish` command.

#### Using a git repository

You can use the `-f` flag to reference a Compose file from a git repository. Compose supports various git URL formats:

Using HTTPS:

```console
$ docker compose -f https://github.com/user/repo.git up
```

Using SSH:

```console
$ docker compose -f git@github.com:user/repo.git up
```

You can specify a specific branch, tag, or commit:

```console
$ docker compose -f https://github.com/user/repo.git@main up
$ docker compose -f https://github.com/user/repo.git@v1.0.0 up
$ docker compose -f https://github.com/user/repo.git@abc123 up
```

You can also specify a subdirectory within the repository:

```console
$ docker compose -f https://github.com/user/repo.git#main:path/to/compose.yaml up
```

When using git resources, Compose will clone the repository and use the specified Compose file. You can combine
git resources with local files:

```console
$ docker compose -f https://github.com/user/repo.git -f compose.override.yaml up
```

### Use-pto specify a project name

Each configuration has a project name. Compose sets the project name using
the following mechanisms, in order of precedence:

- The `-p` command line flag
- The `COMPOSE_PROJECT_NAME` environment variable
- The top level `name:` variable from the config file (or the last `name:`
  from a series of config files specified using `-f`)
- The `basename` of the project directory containing the config file (or
  containing the first config file specified using `-f`)
- The `basename` of the current directory if no config file is specified
  Project names must contain only lowercase letters, decimal digits, dashes,
  and underscores, and must begin with a lowercase letter or decimal digit. If
  the `basename` of the project directory or current directory violates this
  constraint, you must use one of the other mechanisms.

```console
$ docker compose -p my_project ps -a
NAME                 SERVICE    STATUS     PORTS
my_project_demo_1    demo       running

$ docker compose -p my_project logs
demo_1  | PING localhost (127.0.0.1): 56 data bytes
demo_1  | 64 bytes from 127.0.0.1: seq=0 ttl=64 time=0.095 ms
```

### Use profiles to enable optional services

Use `--profile` to specify one or more active profiles
Calling `docker compose --profile frontend up` starts the services with the profile `frontend` and services
without any specified profiles.
You can also enable multiple profiles, e.g. with `docker compose --profile frontend --profile debug up` the profiles `frontend` and `debug` is enabled.

Profiles can also be set by `COMPOSE_PROFILES` environment variable.

### Configuring parallelism

Use `--parallel` to specify the maximum level of parallelism for concurrent engine calls.
Calling `docker compose --parallel 1 pull` pulls the pullable images defined in the Compose file
one at a time. This can also be used to control build concurrency.

Parallelism can also be set by the `COMPOSE_PARALLEL_LIMIT` environment variable.

### Set up environment variables

You can set environment variables for various docker compose options, including the `-f`, `-p` and `--profiles` flags.

Setting the `COMPOSE_FILE` environment variable is equivalent to passing the `-f` flag,
`COMPOSE_PROJECT_NAME` environment variable does the same as the `-p` flag,
`COMPOSE_PROFILES` environment variable is equivalent to the `--profiles` flag
and `COMPOSE_PARALLEL_LIMIT` does the same as the `--parallel` flag.

If flags are explicitly set on the command line, the associated environment variable is ignored.

Setting the `COMPOSE_IGNORE_ORPHANS` environment variable to `true` stops docker compose from detecting orphaned
containers for the project.

Setting the `COMPOSE_MENU` environment variable to `false` disables the helper menu when running `docker compose up`
in attached mode. Alternatively, you can also run `docker compose up --menu=false` to disable the helper menu.

### Use Dry Run mode to test your command

Use `--dry-run` flag to test a command without changing your application stack state.
Dry Run mode shows you all the steps Compose applies when executing a command, for example:

```console
$ docker compose --dry-run up --build -d
[+] Pulling 1/1
 ✔ DRY-RUN MODE -  db Pulled                                                                                                                                                                                                               0.9s
[+] Running 10/8
 ✔ DRY-RUN MODE -    build service backend                                                                                                                                                                                                 0.0s
 ✔ DRY-RUN MODE -  ==> ==> writing image dryRun-754a08ddf8bcb1cf22f310f09206dd783d42f7dd                                                                                                                                                   0.0s
 ✔ DRY-RUN MODE -  ==> ==> naming to nginx-golang-mysql-backend                                                                                                                                                                            0.0s
 ✔ DRY-RUN MODE -  Network nginx-golang-mysql_default                                    Created                                                                                                                                           0.0s
 ✔ DRY-RUN MODE -  Container nginx-golang-mysql-db-1                                     Created                                                                                                                                           0.0s
 ✔ DRY-RUN MODE -  Container nginx-golang-mysql-backend-1                                Created                                                                                                                                           0.0s
 ✔ DRY-RUN MODE -  Container nginx-golang-mysql-proxy-1                                  Created                                                                                                                                           0.0s
 ✔ DRY-RUN MODE -  Container nginx-golang-mysql-db-1                                     Healthy                                                                                                                                           0.5s
 ✔ DRY-RUN MODE -  Container nginx-golang-mysql-backend-1                                Started                                                                                                                                           0.0s
 ✔ DRY-RUN MODE -  Container nginx-golang-mysql-proxy-1                                  Started                                     Started
```

From the example above, you can see that the first step is to pull the image defined by `db` service, then build the `backend` service.
Next, the containers are created. The `db` service is started, and the `backend` and `proxy` wait until the `db` service is healthy before starting.

Dry Run mode works with almost all commands. You cannot use Dry Run mode with a command that doesn't change the state of a Compose stack such as `ps`, `ls`, `logs` for example.

## Subcommands

| Command | Description |
| --- | --- |
| docker compose alpha | Experimental commands |
| docker compose attach | Attach local standard input, output, and error streams to a service's running container |
| docker compose bridge | Convert compose files into another model |
| docker compose build | Build or rebuild services |
| docker compose config | Parse, resolve and render compose file in canonical format |
| docker compose cp | Copy files/folders between a service container and the local filesystem |
| docker compose create | Creates containers for a service |
| docker compose down | Stop and remove containers, networks |
| docker compose events | Receive real time events from containers |
| docker compose exec | Execute a command in a running container |
| docker compose images | List images used by the created containers |
| docker compose kill | Force stop service containers |
| docker compose logs | View output from containers |
| docker compose ls | List running compose projects |
| docker compose pause | Pause services |
| docker compose port | Print the public port for a port binding |
| docker compose ps | List containers |
| docker compose publish | Publish compose application |
| docker compose pull | Pull service images |
| docker compose push | Push service images |
| docker compose restart | Restart service containers |
| docker compose rm | Removes stopped service containers |
| docker compose run | Run a one-off command on a service |
| docker compose start | Start services |
| docker compose stop | Stop services |
| docker compose top | Display the running processes |
| docker compose unpause | Unpause services |
| docker compose up | Create and start containers |
| docker compose version | Show the Docker Compose version information |
| docker compose volumes | List volumes |
| docker compose wait | Block until containers of all (or specified) services stop. |
| docker compose watch | Watch build context for service and rebuild/refresh containers when files are updated |

---

# docker config create

# docker config create

| Description | Create a config from a file or STDIN |
| --- | --- |
| Usage | docker config create [OPTIONS] CONFIG file|- |

Swarm
This command works with the Swarm orchestrator.

## Description

Creates a config using standard input or from a file for the config content.

For detailed information about using configs, refer to
[store configuration data using Docker Configs](https://docs.docker.com/engine/swarm/configs/).

> Note
>
> This is a cluster management command, and must be executed on a Swarm
> manager node. To learn about managers and workers, refer to the
> [Swarm mode section](https://docs.docker.com/engine/swarm/) in the
> documentation.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -l, --label |  | Config labels |
| --template-driver |  | API 1.37+Template driver |

## Examples

### Create a config

```console
$ printf <config> | docker config create my_config -

onakdyv307se2tl7nl20anokv

$ docker config ls

ID                          NAME                CREATED             UPDATED
onakdyv307se2tl7nl20anokv   my_config           6 seconds ago       6 seconds ago
```

### Create a config with a file

```console
$ docker config create my_config ./config.json

dg426haahpi5ezmkkj5kyl3sn

$ docker config ls

ID                          NAME                CREATED             UPDATED
dg426haahpi5ezmkkj5kyl3sn   my_config           7 seconds ago       7 seconds ago
```

### Create a config with labels (-l, --label)

```console
$ docker config create \
    --label env=dev \
    --label rev=20170324 \
    my_config ./config.json

eo7jnzguqgtpdah3cm5srfb97
```

```console
$ docker config inspect my_config

[
    {
        "ID": "eo7jnzguqgtpdah3cm5srfb97",
        "Version": {
            "Index": 17
        },
        "CreatedAt": "2017-03-24T08:15:09.735271783Z",
        "UpdatedAt": "2017-03-24T08:15:09.735271783Z",
        "Spec": {
            "Name": "my_config",
            "Labels": {
                "env": "dev",
                "rev": "20170324"
            },
            "Data": "aGVsbG8K"
        }
    }
]
```

---

# docker config inspect

# docker config inspect

| Description | Display detailed information on one or more configs |
| --- | --- |
| Usage | docker config inspect [OPTIONS] CONFIG [CONFIG...] |

Swarm
This command works with the Swarm orchestrator.

## Description

Inspects the specified config.

By default, this renders all results in a JSON array. If a format is specified,
the given template will be executed for each result.

Go's [text/template](https://pkg.go.dev/text/template) package
describes all the details of the format.

For detailed information about using configs, refer to
[store configuration data using Docker Configs](https://docs.docker.com/engine/swarm/configs/).

> Note
>
> This is a cluster management command, and must be executed on a Swarm
> manager node. To learn about managers and workers, refer to the
> [Swarm mode section](https://docs.docker.com/engine/swarm/) in the
> documentation.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -f, --format |  | Format output using a custom template:'json': Print in JSON format'TEMPLATE': Print output using the given Go template.Refer tohttps://docs.docker.com/go/formatting/for more information about formatting output with templates |
| --pretty |  | Print the information in a human friendly format |

## Examples

### Inspect a config by name or ID

You can inspect a config, either by its *name*, or *ID*

For example, given the following config:

```console
$ docker config ls

ID                          NAME                CREATED             UPDATED
eo7jnzguqgtpdah3cm5srfb97   my_config           3 minutes ago       3 minutes ago
```

```console
$ docker config inspect config.json
```

The output is in JSON format, for example:

```json
[
  {
    "ID": "eo7jnzguqgtpdah3cm5srfb97",
    "Version": {
      "Index": 17
    },
    "CreatedAt": "2017-03-24T08:15:09.735271783Z",
    "UpdatedAt": "2017-03-24T08:15:09.735271783Z",
    "Spec": {
      "Name": "my_config",
      "Labels": {
        "env": "dev",
        "rev": "20170324"
      },
      "Data": "aGVsbG8K"
    }
  }
]
```

### Format the output (--format)

You can use the --format option to obtain specific information about a
config. The following example command outputs the creation time of the
config.

```console
$ docker config inspect --format='{{.CreatedAt}}' eo7jnzguqgtpdah3cm5srfb97

2017-03-24 08:15:09.735271783 +0000 UTC
```

---

# docker config ls

# docker config ls

| Description | List configs |
| --- | --- |
| Usage | docker config ls [OPTIONS] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker config list |

Swarm
This command works with the Swarm orchestrator.

## Description

Run this command on a manager node to list the configs in the Swarm.

For detailed information about using configs, refer to
[store configuration data using Docker Configs](https://docs.docker.com/engine/swarm/configs/).

> Note
>
> This is a cluster management command, and must be executed on a Swarm
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

```console
$ docker config ls

ID                          NAME                        CREATED             UPDATED
6697bflskwj1998km1gnnjr38   q5s5570vtvnimefos1fyeo2u2   6 weeks ago         6 weeks ago
9u9hk4br2ej0wgngkga6rp4hq   my_config                   5 weeks ago         5 weeks ago
mem02h8n73mybpgqjf0kfi1n0   test_config                 3 seconds ago       3 seconds ago
```

### Filtering (-f, --filter)

The filtering flag (`-f` or `--filter`) format is a `key=value` pair. If there is more
than one filter, then pass multiple flags (e.g., `--filter "foo=bar" --filter "bif=baz"`)

The currently supported filters are:

- [id](#id) (config's ID)
- [label](#label) (`label=<key>` or `label=<key>=<value>`)
- [name](#name) (config's name)

#### id

The `id` filter matches all or prefix of a config's id.

```console
$ docker config ls -f "id=6697bflskwj1998km1gnnjr38"

ID                          NAME                        CREATED             UPDATED
6697bflskwj1998km1gnnjr38   q5s5570vtvnimefos1fyeo2u2   6 weeks ago         6 weeks ago
```

#### label

The `label` filter matches configs based on the presence of a `label` alone or
a `label` and a value.

The following filter matches all configs with a `project` label regardless of
its value:

```console
$ docker config ls --filter label=project

ID                          NAME                        CREATED             UPDATED
mem02h8n73mybpgqjf0kfi1n0   test_config                 About an hour ago   About an hour ago
```

The following filter matches only services with the `project` label with the
`project-a` value.

```console
$ docker service ls --filter label=project=test

ID                          NAME                        CREATED             UPDATED
mem02h8n73mybpgqjf0kfi1n0   test_config                 About an hour ago   About an hour ago
```

#### name

The `name` filter matches on all or prefix of a config's name.

The following filter matches config with a name containing a prefix of `test`.

```console
$ docker config ls --filter name=test_config

ID                          NAME                        CREATED             UPDATED
mem02h8n73mybpgqjf0kfi1n0   test_config                 About an hour ago   About an hour ago
```

### Format the output (--format)

The formatting option (`--format`) pretty prints configs output
using a Go template.

Valid placeholders for the Go template are listed below:

| Placeholder | Description |
| --- | --- |
| .ID | Config ID |
| .Name | Config name |
| .CreatedAt | Time when the config was created |
| .UpdatedAt | Time when the config was updated |
| .Labels | All labels assigned to the config |
| .Label | Value of a specific label for this config. For example{{.Label "my-label"}} |

When using the `--format` option, the `config ls` command will either
output the data exactly as the template declares or, when using the
`table` directive, will include column headers as well.

The following example uses a template without headers and outputs the
`ID` and `Name` entries separated by a colon (`:`) for all images:

```console
$ docker config ls --format "{{.ID}}: {{.Name}}"

77af4d6b9913: config-1
b6fa739cedf5: config-2
78a85c484f71: config-3
```

To list all configs with their name and created date in a table format you
can use:

```console
$ docker config ls --format "table {{.ID}}\t{{.Name}}\t{{.CreatedAt}}"

ID                  NAME                      CREATED
77af4d6b9913        config-1                  5 minutes ago
b6fa739cedf5        config-2                  3 hours ago
78a85c484f71        config-3                  10 days ago
```

---

# docker config rm

# docker config rm

| Description | Remove one or more configs |
| --- | --- |
| Usage | docker config rm CONFIG [CONFIG...] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker config remove |

Swarm
This command works with the Swarm orchestrator.

## Description

Removes the specified configs from the Swarm.

For detailed information about using configs, refer to
[store configuration data using Docker Configs](https://docs.docker.com/engine/swarm/configs/).

> Note
>
> This is a cluster management command, and must be executed on a Swarm
> manager node. To learn about managers and workers, refer to the
> [Swarm mode section](https://docs.docker.com/engine/swarm/) in the
> documentation.

## Examples

This example removes a config:

```console
$ docker config rm my_config
sapth4csdo5b6wz2p5uimh5xg
```

> Warning
>
> This command doesn't ask for confirmation before removing a config.

---

# docker config

# docker config

| Description | Manage Swarm configs |
| --- | --- |
| Usage | docker config |

Swarm
This command works with the Swarm orchestrator.

## Description

Manage configs.

## Subcommands

| Command | Description |
| --- | --- |
| docker config create | Create a config from a file or STDIN |
| docker config inspect | Display detailed information on one or more configs |
| docker config ls | List configs |
| docker config rm | Remove one or more configs |

---

# docker container attach

# docker container attach

| Description | Attach local standard input, output, and error streams to a running container |
| --- | --- |
| Usage | docker container attach [OPTIONS] CONTAINER |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker attach |

## Description

Use `docker attach` to attach your terminal's standard input, output, and error
(or any combination of the three) to a running container using the container's
ID or name. This lets you view its output or control it interactively, as
though the commands were running directly in your terminal.

> Note
>
> The `attach` command displays the output of the container's `ENTRYPOINT` and
> `CMD` process. This can appear as if the attach command is hung when in fact
> the process may simply not be writing any output at that time.

You can attach to the same contained process multiple times simultaneously,
from different sessions on the Docker host.

To stop a container, use `CTRL-c`. This key sequence sends `SIGKILL` to the
container. If `--sig-proxy` is true (the default),`CTRL-c` sends a `SIGINT` to
the container. If the container was run with `-i` and `-t`, you can detach from
a container and leave it running using the `CTRL-p CTRL-q` key sequence.

> Note
>
> A process running as PID 1 inside a container is treated specially by
> Linux: it ignores any signal with the default action. So, the process
> doesn't terminate on `SIGINT` or `SIGTERM` unless it's coded to do so.

You can't redirect the standard input of a `docker attach` command while
attaching to a TTY-enabled container (using the `-i` and `-t` options).

While a client is connected to container's `stdio` using `docker attach`,
Docker uses a ~1MB memory buffer to maximize the throughput of the application.
Once this buffer is full, the speed of the API connection is affected, and so
this impacts the output process' writing speed. This is similar to other
applications like SSH. Because of this, it isn't recommended to run
performance-critical applications that generate a lot of output in the
foreground over a slow client connection. Instead, use the `docker logs`
command to get access to the logs.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --detach-keys |  | Override the key sequence for detaching a container |
| --no-stdin |  | Do not attach STDIN |
| --sig-proxy | true | Proxy all received signals to the process |

## Examples

### Attach to and detach from a running container

The following example starts an Alpine container running `top` in detached mode,
then attaches to the container;

```console
$ docker run -d --name topdemo alpine top -b

$ docker attach topdemo

Mem: 2395856K used, 5638884K free, 2328K shrd, 61904K buff, 1524264K cached
CPU:   0% usr   0% sys   0% nic  99% idle   0% io   0% irq   0% sirq
Load average: 0.15 0.06 0.01 1/567 6
  PID  PPID USER     STAT   VSZ %VSZ CPU %CPU COMMAND
    1     0 root     R     1700   0%   3   0% top -b
```

As the container was started without the `-i`, and `-t` options, signals are
forwarded to the attached process, which means that the default `CTRL-p CTRL-q`
detach key sequence produces no effect, but pressing `CTRL-c` terminates the
container:

```console
<...>
  PID  PPID USER     STAT   VSZ %VSZ CPU %CPU COMMAND
    1     0 root     R     1700   0%   7   0% top -b
^P^Q
^C

$ docker ps -a --filter name=topdemo

CONTAINER ID   IMAGE     COMMAND    CREATED          STATUS                       PORTS     NAMES
96254a235bd6   alpine    "top -b"   44 seconds ago   Exited (130) 8 seconds ago             topdemo
```

Repeating the example above, but this time with the `-i` and `-t` options set;

```console
$ docker run -dit --name topdemo2 alpine /usr/bin/top -b
```

Now, when attaching to the container, and pressing the `CTRL-p CTRL-q` ("read
escape sequence"), the Docker CLI is handling the detach sequence, and the
`attach` command is detached from the container. Checking the container's status
with `docker ps` shows that the container is still running in the background:

```console
$ docker attach topdemo2

Mem: 2405344K used, 5629396K free, 2512K shrd, 65100K buff, 1524952K cached
CPU:   0% usr   0% sys   0% nic  99% idle   0% io   0% irq   0% sirq
Load average: 0.12 0.12 0.05 1/594 6
  PID  PPID USER     STAT   VSZ %VSZ CPU %CPU COMMAND
    1     0 root     R     1700   0%   3   0% top -b
read escape sequence

$ docker ps -a --filter name=topdemo2

CONTAINER ID   IMAGE     COMMAND    CREATED          STATUS          PORTS     NAMES
fde88b83c2c2   alpine    "top -b"   22 seconds ago   Up 21 seconds             topdemo2
```

### Get the exit code of the container's command

And in this second example, you can see the exit code returned by the `bash`
process is returned by the `docker attach` command to its caller too:

```console
$ docker run --name test -dit alpine
275c44472aebd77c926d4527885bb09f2f6db21d878c75f0a1c212c03d3bcfab

$ docker attach test
/# exit 13

$ echo $?
13

$ docker ps -a --filter name=test

CONTAINER ID   IMAGE     COMMAND     CREATED              STATUS                       PORTS     NAMES
a2fe3fd886db   alpine    "/bin/sh"   About a minute ago   Exited (13) 40 seconds ago             test
```

### Override the detach sequence (--detach-keys)

Use the `--detach-keys` option to override the Docker key sequence for detach.
This is useful if the Docker default sequence conflicts with key sequence you
use for other applications. There are two ways to define your own detach key
sequence, as a per-container override or as a configuration property on your
entire configuration.

To override the sequence for an individual container, use the
`--detach-keys="<sequence>"` flag with the `docker attach` command. The format of
the `<sequence>` is either a letter [a-Z], or the `ctrl-` combined with any of
the following:

- `a-z` (a single lowercase alpha character )
- `@` (at sign)
- `[` (left bracket)
- `\\` (two backward slashes)
- `_` (underscore)
- `^` (caret)

These `a`, `ctrl-a`, `X`, or `ctrl-\\` values are all examples of valid key
sequences. To configure a different configuration default key sequence for all
containers, see
[Configuration filesection](https://docs.docker.com/reference/cli/docker/#configuration-files).

---

# docker container commit

# docker container commit

| Description | Create a new image from a container's changes |
| --- | --- |
| Usage | docker container commit [OPTIONS] CONTAINER [REPOSITORY[:TAG]] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker commit |

## Description

It can be useful to commit a container's file changes or settings into a new
image. This lets you debug a container by running an interactive shell, or
export a working dataset to another server.

Commits do not include any data contained in mounted volumes.

By default, the container being committed and its processes will be paused
while the image is committed. This reduces the likelihood of encountering data
corruption during the process of creating the commit. If this behavior is
undesired, set the `--pause` option to false.

The `--change` option will apply `Dockerfile` instructions to the image that's
created. Supported `Dockerfile` instructions:
`CMD`|`ENTRYPOINT`|`ENV`|`EXPOSE`|`LABEL`|`ONBUILD`|`USER`|`VOLUME`|`WORKDIR`

## Options

| Option | Default | Description |
| --- | --- | --- |
| -a, --author |  | Author (e.g.,John Hannibal Smith <hannibal@a-team.com>) |
| -c, --change |  | Apply Dockerfile instruction to the created image |
| -m, --message |  | Commit message |
| --no-pause |  | Disable pausing container during commit |

## Examples

### Commit a container

```console
$ docker ps

CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS              NAMES
c3f279d17e0a        ubuntu:24.04        /bin/bash           7 days ago          Up 25 hours                            desperate_dubinsky
197387f1b436        ubuntu:24.04        /bin/bash           7 days ago          Up 25 hours                            focused_hamilton

$ docker commit c3f279d17e0a  svendowideit/testimage:version3

f5283438590d

$ docker images

REPOSITORY                        TAG                 ID                  CREATED             SIZE
svendowideit/testimage            version3            f5283438590d        16 seconds ago      335.7 MB
```

### Commit a container with new configurations (--change)

```console
$ docker ps

CONTAINER ID       IMAGE               COMMAND             CREATED             STATUS              PORTS              NAMES
c3f279d17e0a       ubuntu:24.04        /bin/bash           7 days ago          Up 25 hours                            desperate_dubinsky
197387f1b436       ubuntu:24.04        /bin/bash           7 days ago          Up 25 hours                            focused_hamilton

$ docker inspect -f "{{ .Config.Env }}" c3f279d17e0a

[HOME=/ PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin]

$ docker commit --change "ENV DEBUG=true" c3f279d17e0a  svendowideit/testimage:version3

f5283438590d

$ docker inspect -f "{{ .Config.Env }}" f5283438590d

[HOME=/ PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin DEBUG=true]
```

### Commit a container with newCMDandEXPOSEinstructions

```console
$ docker ps

CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS              NAMES
c3f279d17e0a        ubuntu:24.04        /bin/bash           7 days ago          Up 25 hours                            desperate_dubinsky
197387f1b436        ubuntu:24.04        /bin/bash           7 days ago          Up 25 hours                            focused_hamilton

$ docker commit --change='CMD ["apachectl", "-DFOREGROUND"]' -c "EXPOSE 80" c3f279d17e0a  svendowideit/testimage:version4

f5283438590d

$ docker run -d svendowideit/testimage:version4

89373736e2e7f00bc149bd783073ac43d0507da250e999f3f1036e0db60817c0

$ docker ps

CONTAINER ID        IMAGE               COMMAND                 CREATED             STATUS              PORTS              NAMES
89373736e2e7        testimage:version4  "apachectl -DFOREGROU"  3 seconds ago       Up 2 seconds        80/tcp             distracted_fermat
c3f279d17e0a        ubuntu:24.04        /bin/bash               7 days ago          Up 25 hours                            desperate_dubinsky
197387f1b436        ubuntu:24.04        /bin/bash               7 days ago          Up 25 hours                            focused_hamilton
```

---

# docker container cp

# docker container cp

| Description | Copy files/folders between a container and the local filesystem |
| --- | --- |
| Usage | docker container cp [OPTIONS] CONTAINER:SRC_PATH DEST_PATH|-
docker cp [OPTIONS] SRC_PATH|- CONTAINER:DEST_PATH |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker cp |

## Description

The `docker cp` utility copies the contents of `SRC_PATH` to the `DEST_PATH`.
You can copy from the container's file system to the local machine or the
reverse, from the local filesystem to the container. If `-` is specified for
either the `SRC_PATH` or `DEST_PATH`, you can also stream a tar archive from
`STDIN` or to `STDOUT`. The `CONTAINER` can be a running or stopped container.
The `SRC_PATH` or `DEST_PATH` can be a file or directory.

The `docker cp` command assumes container paths are relative to the container's
`/` (root) directory. This means supplying the initial forward slash is optional;
The command sees `compassionate_darwin:/tmp/foo/myfile.txt` and
`compassionate_darwin:tmp/foo/myfile.txt` as identical. Local machine paths can
be an absolute or relative value. The command interprets a local machine's
relative paths as relative to the current working directory where `docker cp` is
run.

The `cp` command behaves like the Unix `cp -a` command in that directories are
copied recursively with permissions preserved if possible. Ownership is set to
the user and primary group at the destination. For example, files copied to a
container are created with `UID:GID` of the root user. Files copied to the local
machine are created with the `UID:GID` of the user which invoked the `docker cp`
command. However, if you specify the `-a` option, `docker cp` sets the ownership
to the user and primary group at the source.
If you specify the `-L` option, `docker cp` follows any symbolic link
in the `SRC_PATH`. `docker cp` doesn't create parent directories for
`DEST_PATH` if they don't exist.

Assuming a path separator of `/`, a first argument of `SRC_PATH` and second
argument of `DEST_PATH`, the behavior is as follows:

- `SRC_PATH` specifies a file
  - `DEST_PATH` does not exist
    - the file is saved to a file created at `DEST_PATH`
  - `DEST_PATH` does not exist and ends with `/`
    - Error condition: the destination directory must exist.
  - `DEST_PATH` exists and is a file
    - the destination is overwritten with the source file's contents
  - `DEST_PATH` exists and is a directory
    - the file is copied into this directory using the basename from
      `SRC_PATH`
- `SRC_PATH` specifies a directory
  - `DEST_PATH` does not exist
    - `DEST_PATH` is created as a directory and the *contents* of the source
      directory are copied into this directory
  - `DEST_PATH` exists and is a file
    - Error condition: cannot copy a directory to a file
  - `DEST_PATH` exists and is a directory
    - `SRC_PATH` does not end with `/.` (that is: *slash* followed by *dot*)
      - the source directory is copied into this directory
    - `SRC_PATH` does end with `/.` (that is: *slash* followed by *dot*)
      - the *content* of the source directory is copied into this
        directory

The command requires `SRC_PATH` and `DEST_PATH` to exist according to the above
rules. If `SRC_PATH` is local and is a symbolic link, the symbolic link, not
the target, is copied by default. To copy the link target and not the link, specify
the `-L` option.

A colon (`:`) is used as a delimiter between `CONTAINER` and its path. You can
also use `:` when specifying paths to a `SRC_PATH` or `DEST_PATH` on a local
machine, for example `file:name.txt`. If you use a `:` in a local machine path,
you must be explicit with a relative or absolute path, for example:

```
`/path/to/file:name.txt` or `./file:name.txt`
```

## Options

| Option | Default | Description |
| --- | --- | --- |
| -a, --archive |  | Archive mode (copy all uid/gid information) |
| -L, --follow-link |  | Always follow symbol link in SRC_PATH |
| -q, --quiet |  | Suppress progress output during copy. Progress output is automatically suppressed if no terminal is attached |

## Examples

Copy a local file into container

```console
$ docker cp ./some_file CONTAINER:/work
```

Copy files from container to local path

```console
$ docker cp CONTAINER:/var/logs/ /tmp/app_logs
```

Copy a file from container to stdout. Note `cp` command produces a tar stream

```console
$ docker cp CONTAINER:/var/logs/app.log - | tar x -O | grep "ERROR"
```

### Corner cases

It isn't possible to copy certain system files such as resources under
`/proc`, `/sys`, `/dev`,
[tmpfs](https://docs.docker.com/reference/cli/docker/container/run/#tmpfs), and mounts created by
the user in the container. However, you can still copy such files by manually
running `tar` in `docker exec`. Both of the following examples do the same thing
in different ways (consider `SRC_PATH` and `DEST_PATH` are directories):

```console
$ docker exec CONTAINER tar Ccf $(dirname SRC_PATH) - $(basename SRC_PATH) | tar Cxf DEST_PATH -
```

```console
$ tar Ccf $(dirname SRC_PATH) - $(basename SRC_PATH) | docker exec -i CONTAINER tar Cxf DEST_PATH -
```

Using `-` as the `SRC_PATH` streams the contents of `STDIN` as a tar archive.
The command extracts the content of the tar to the `DEST_PATH` in container's
filesystem. In this case, `DEST_PATH` must specify a directory. Using `-` as
the `DEST_PATH` streams the contents of the resource as a tar archive to `STDOUT`.
