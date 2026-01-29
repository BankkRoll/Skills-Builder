# docker compose bridge transformations list and more

# docker compose bridge transformations list

# docker compose bridge transformations list

| Description | List available transformations |
| --- | --- |
| Usage | docker compose bridge transformations list |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker compose bridge transformations ls |

## Description

List available transformations

## Options

| Option | Default | Description |
| --- | --- | --- |
| --format | table | Format the output. Values: [table | json] |
| -q, --quiet |  | Only display transformer names |

---

# docker compose bridge transformations

# docker compose bridge transformations

| Description | Manage transformation images |
| --- | --- |

## Description

Manage transformation images

## Subcommands

| Command | Description |
| --- | --- |
| docker compose bridge transformations create | Create a new transformation |
| docker compose bridge transformations list | List available transformations |

---

# docker compose bridge

# docker compose bridge

| Description | Convert compose files into another model |
| --- | --- |

## Description

Convert compose files into another model

## Subcommands

| Command | Description |
| --- | --- |
| docker compose bridge convert | Convert compose files to Kubernetes manifests, Helm charts, or another model |
| docker compose bridge transformations | Manage transformation images |

---

# docker compose build

# docker compose build

| Description | Build or rebuild services |
| --- | --- |
| Usage | docker compose build [OPTIONS] [SERVICE...] |

## Description

Services are built once and then tagged, by default as `project-service`.

If the Compose file specifies an
[image](https://github.com/compose-spec/compose-spec/blob/main/spec.md#image) name,
the image is tagged with that name, substituting any variables beforehand. See
[variable interpolation](https://github.com/compose-spec/compose-spec/blob/main/spec.md#interpolation).

If you change a service's `Dockerfile` or the contents of its build directory,
run `docker compose build` to rebuild it.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --build-arg |  | Set build-time variables for services |
| --builder |  | Set builder to use |
| --check |  | Check build configuration |
| -m, --memory |  | Set memory limit for the build container. Not supported by BuildKit. |
| --no-cache |  | Do not use cache when building the image |
| --print |  | Print equivalent bake file |
| --provenance |  | Add a provenance attestation |
| --pull |  | Always attempt to pull a newer version of the image |
| --push |  | Push service images |
| -q, --quiet |  | Suppress the build output |
| --sbom |  | Add a SBOM attestation |
| --ssh |  | Set SSH authentications used when building service images. (use 'default' for using your default SSH Agent) |
| --with-dependencies |  | Also build dependencies (transitively) |

---

# docker compose config

# docker compose config

| Description | Parse, resolve and render compose file in canonical format |
| --- | --- |
| Usage | docker compose config [OPTIONS] [SERVICE...] |

## Description

`docker compose config` renders the actual data model to be applied on the Docker Engine.
It merges the Compose files set by `-f` flags, resolves variables in the Compose file, and expands short-notation into
the canonical format.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --environment |  | Print environment used for interpolation. |
| --format |  | Format the output. Values: [yaml | json] |
| --hash |  | Print the service config hash, one per line. |
| --images |  | Print the image names, one per line. |
| --lock-image-digests |  | Produces an override file with image digests |
| --models |  | Print the model names, one per line. |
| --networks |  | Print the network names, one per line. |
| --no-consistency |  | Don't check model consistency - warning: may produce invalid Compose output |
| --no-env-resolution |  | Don't resolve service env files |
| --no-interpolate |  | Don't interpolate environment variables |
| --no-normalize |  | Don't normalize compose model |
| --no-path-resolution |  | Don't resolve file paths |
| -o, --output |  | Save to file (default to stdout) |
| --profiles |  | Print the profile names, one per line. |
| -q, --quiet |  | Only validate the configuration, don't print anything |
| --resolve-image-digests |  | Pin image tags to digests |
| --services |  | Print the service names, one per line. |
| --variables |  | Print model variables and default values. |
| --volumes |  | Print the volume names, one per line. |

---

# docker compose cp

# docker compose cp

| Description | Copy files/folders between a service container and the local filesystem |
| --- | --- |
| Usage | docker compose cp [OPTIONS] SERVICE:SRC_PATH DEST_PATH|-
docker compose cp [OPTIONS] SRC_PATH|- SERVICE:DEST_PATH |

## Description

Copy files/folders between a service container and the local filesystem

## Options

| Option | Default | Description |
| --- | --- | --- |
| --all |  | Include containers created by the run command |
| -a, --archive |  | Archive mode (copy all uid/gid information) |
| -L, --follow-link |  | Always follow symbol link in SRC_PATH |
| --index |  | Index of the container if service has multiple replicas |

---

# docker compose create

# docker compose create

| Description | Creates containers for a service |
| --- | --- |
| Usage | docker compose create [OPTIONS] [SERVICE...] |

## Description

Creates containers for a service

## Options

| Option | Default | Description |
| --- | --- | --- |
| --build |  | Build images before starting containers |
| --force-recreate |  | Recreate containers even if their configuration and image haven't changed |
| --no-build |  | Don't build an image, even if it's policy |
| --no-recreate |  | If containers already exist, don't recreate them. Incompatible with --force-recreate. |
| --pull | policy | Pull image before running ("always"|"missing"|"never"|"build") |
| --quiet-pull |  | Pull without printing progress information |
| --remove-orphans |  | Remove containers for services not defined in the Compose file |
| --scale |  | Scale SERVICE to NUM instances. Overrides thescalesetting in the Compose file if present. |
| -y, --yes |  | Assume "yes" as answer to all prompts and run non-interactively |

---

# docker compose down

# docker compose down

| Description | Stop and remove containers, networks |
| --- | --- |
| Usage | docker compose down [OPTIONS] [SERVICES] |

## Description

Stops containers and removes containers, networks, volumes, and images created by `up`.

By default, the only things removed are:

- Containers for services defined in the Compose file.
- Networks defined in the networks section of the Compose file.
- The default network, if one is used.

Networks and volumes defined as external are never removed.

Anonymous volumes are not removed by default. However, as they don’t have a stable name, they are not automatically
mounted by a subsequent `up`. For data that needs to persist between updates, use explicit paths as bind mounts or
named volumes.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --remove-orphans |  | Remove containers for services not defined in the Compose file |
| --rmi |  | Remove images used by services. "local" remove only images that don't have a custom tag ("local"|"all") |
| -t, --timeout |  | Specify a shutdown timeout in seconds |
| -v, --volumes |  | Remove named volumes declared in the "volumes" section of the Compose file and anonymous volumes attached to containers |

---

# docker compose events

# docker compose events

| Description | Receive real time events from containers |
| --- | --- |
| Usage | docker compose events [OPTIONS] [SERVICE...] |

## Description

Stream container events for every container in the project.

With the `--json` flag, a json object is printed one per line with the format:

```json
{
    "time": "2015-11-20T18:01:03.615550",
    "type": "container",
    "action": "create",
    "id": "213cf7...5fc39a",
    "service": "web",
    "attributes": {
      "name": "application_web_1",
      "image": "alpine:edge"
    }
}
```

The events that can be received using this can be seen
[here](https://docs.docker.com/reference/cli/docker/system/events/#object-types).

## Options

| Option | Default | Description |
| --- | --- | --- |
| --json |  | Output events as a stream of json objects |
| --since |  | Show all events created since timestamp |
| --until |  | Stream events until this timestamp |

---

# docker compose exec

# docker compose exec

| Description | Execute a command in a running container |
| --- | --- |
| Usage | docker compose exec [OPTIONS] SERVICE COMMAND [ARGS...] |

## Description

This is the equivalent of `docker exec` targeting a Compose service.

With this subcommand, you can run arbitrary commands in your services. Commands allocate a TTY by default, so
you can use a command such as `docker compose exec web sh` to get an interactive prompt.

By default, Compose will enter container in interactive mode and allocate a TTY, while the equivalent `docker exec`
command requires passing `--interactive --tty` flags to get the same behavior. Compose also support those two flags
to offer a smooth migration between commands, whenever they are no-op by default. Still, `interactive` can be used to
force disabling interactive mode (`--interactive=false`), typically when `docker compose exec` command is used inside
a script.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -d, --detach |  | Detached mode: Run command in the background |
| -e, --env |  | Set environment variables |
| --index |  | Index of the container if service has multiple replicas |
| -T, --no-tty | true | Disable pseudo-TTY allocation. By default 'docker compose exec' allocates a TTY. |
| --privileged |  | Give extended privileges to the process |
| -u, --user |  | Run the command as this user |
| -w, --workdir |  | Path to workdir directory for this command |

---

# docker compose images

# docker compose images

| Description | List images used by the created containers |
| --- | --- |
| Usage | docker compose images [OPTIONS] [SERVICE...] |

## Description

List images used by the created containers

## Options

| Option | Default | Description |
| --- | --- | --- |
| --format | table | Format the output. Values: [table | json] |
| -q, --quiet |  | Only display IDs |

---

# docker compose kill

# docker compose kill

| Description | Force stop service containers |
| --- | --- |
| Usage | docker compose kill [OPTIONS] [SERVICE...] |

## Description

Forces running containers to stop by sending a `SIGKILL` signal. Optionally the signal can be passed, for example:

```console
$ docker compose kill -s SIGINT
```

## Options

| Option | Default | Description |
| --- | --- | --- |
| --remove-orphans |  | Remove containers for services not defined in the Compose file |
| -s, --signal | SIGKILL | SIGNAL to send to the container |

---

# docker compose logs

# docker compose logs

| Description | View output from containers |
| --- | --- |
| Usage | docker compose logs [OPTIONS] [SERVICE...] |

## Description

Displays log output from services

## Options

| Option | Default | Description |
| --- | --- | --- |
| -f, --follow |  | Follow log output |
| --index |  | index of the container if service has multiple replicas |
| --no-color |  | Produce monochrome output |
| --no-log-prefix |  | Don't print prefix in logs |
| --since |  | Show logs since timestamp (e.g. 2013-01-02T13:23:37Z) or relative (e.g. 42m for 42 minutes) |
| -n, --tail | all | Number of lines to show from the end of the logs for each container |
| -t, --timestamps |  | Show timestamps |
| --until |  | Show logs before a timestamp (e.g. 2013-01-02T13:23:37Z) or relative (e.g. 42m for 42 minutes) |

---

# docker compose ls

# docker compose ls

| Description | List running compose projects |
| --- | --- |
| Usage | docker compose ls [OPTIONS] |

## Description

Lists running Compose projects

## Options

| Option | Default | Description |
| --- | --- | --- |
| -a, --all |  | Show all stopped Compose projects |
| --filter |  | Filter output based on conditions provided |
| --format | table | Format the output. Values: [table | json] |
| -q, --quiet |  | Only display project names |

---

# docker compose pause

# docker compose pause

| Description | Pause services |
| --- | --- |
| Usage | docker compose pause [SERVICE...] |

## Description

Pauses running containers of a service. They can be unpaused with `docker compose unpause`.

---

# docker compose port

# docker compose port

| Description | Print the public port for a port binding |
| --- | --- |
| Usage | docker compose port [OPTIONS] SERVICE PRIVATE_PORT |

## Description

Prints the public port for a port binding

## Options

| Option | Default | Description |
| --- | --- | --- |
| --index |  | Index of the container if service has multiple replicas |
| --protocol | tcp | tcp or udp |

---

# docker compose ps

# docker compose ps

| Description | List containers |
| --- | --- |
| Usage | docker compose ps [OPTIONS] [SERVICE...] |

## Description

Lists containers for a Compose project, with current status and exposed ports.

```console
$ docker compose ps
NAME            IMAGE     COMMAND           SERVICE    CREATED         STATUS          PORTS
example-foo-1   alpine    "/entrypoint.…"   foo        4 seconds ago   Up 2 seconds    0.0.0.0:8080->80/tcp
```

By default, only running containers are shown. `--all` flag can be used to include stopped containers.

```console
$ docker compose ps --all
NAME            IMAGE     COMMAND           SERVICE    CREATED         STATUS          PORTS
example-foo-1   alpine    "/entrypoint.…"   foo        4 seconds ago   Up 2 seconds    0.0.0.0:8080->80/tcp
example-bar-1   alpine    "/entrypoint.…"   bar        4 seconds ago   exited (0)
```

## Options

| Option | Default | Description |
| --- | --- | --- |
| -a, --all |  | Show all stopped containers (including those created by the run command) |
| --filter |  | Filter services by a property (supported filters: status) |
| --format | table | Format output using a custom template:'table': Print output in table format with column headers (default)'table TEMPLATE': Print output in table format using the given Go template'json': Print in JSON format'TEMPLATE': Print output using the given Go template.Refer tohttps://docs.docker.com/go/formatting/for more information about formatting output with templates |
| --no-trunc |  | Don't truncate output |
| --orphans | true | Include orphaned services (not declared by project) |
| -q, --quiet |  | Only display IDs |
| --services |  | Display services |
| --status |  | Filter services by status. Values: [paused | restarting | removing | running | dead | created | exited] |

## Examples

### Format the output (--format)

By default, the `docker compose ps` command uses a table ("pretty") format to
show the containers. The `--format` flag allows you to specify alternative
presentations for the output. Currently, supported options are `pretty` (default),
and `json`, which outputs information about the containers as a JSON array:

```console
$ docker compose ps --format json
[{"ID":"1553b0236cf4d2715845f053a4ee97042c4f9a2ef655731ee34f1f7940eaa41a","Name":"example-bar-1","Command":"/docker-entrypoint.sh nginx -g 'daemon off;'","Project":"example","Service":"bar","State":"exited","Health":"","ExitCode":0,"Publishers":null},{"ID":"f02a4efaabb67416e1ff127d51c4b5578634a0ad5743bd65225ff7d1909a3fa0","Name":"example-foo-1","Command":"/docker-entrypoint.sh nginx -g 'daemon off;'","Project":"example","Service":"foo","State":"running","Health":"","ExitCode":0,"Publishers":[{"URL":"0.0.0.0","TargetPort":80,"PublishedPort":8080,"Protocol":"tcp"}]}]
```

The JSON output allows you to use the information in other tools for further
processing, for example, using the [jqutility](https://stedolan.github.io/jq/)
to pretty-print the JSON:

```console
$ docker compose ps --format json | jq .
[
  {
    "ID": "1553b0236cf4d2715845f053a4ee97042c4f9a2ef655731ee34f1f7940eaa41a",
    "Name": "example-bar-1",
    "Command": "/docker-entrypoint.sh nginx -g 'daemon off;'",
    "Project": "example",
    "Service": "bar",
    "State": "exited",
    "Health": "",
    "ExitCode": 0,
    "Publishers": null
  },
  {
    "ID": "f02a4efaabb67416e1ff127d51c4b5578634a0ad5743bd65225ff7d1909a3fa0",
    "Name": "example-foo-1",
    "Command": "/docker-entrypoint.sh nginx -g 'daemon off;'",
    "Project": "example",
    "Service": "foo",
    "State": "running",
    "Health": "",
    "ExitCode": 0,
    "Publishers": [
      {
        "URL": "0.0.0.0",
        "TargetPort": 80,
        "PublishedPort": 8080,
        "Protocol": "tcp"
      }
    ]
  }
]
```

### Filter containers by status (--status)

Use the `--status` flag to filter the list of containers by status. For example,
to show only containers that are running or only containers that have exited:

```console
$ docker compose ps --status=running
NAME            IMAGE     COMMAND           SERVICE    CREATED         STATUS          PORTS
example-foo-1   alpine    "/entrypoint.…"   foo        4 seconds ago   Up 2 seconds    0.0.0.0:8080->80/tcp

$ docker compose ps --status=exited
NAME            IMAGE     COMMAND           SERVICE    CREATED         STATUS          PORTS
example-bar-1   alpine    "/entrypoint.…"   bar        4 seconds ago   exited (0)
```

### Filter containers by status (--filter)

The [--statusflag](#status) is a convenient shorthand for the `--filter status=<status>`
flag. The example below is the equivalent to the example from the previous section,
this time using the `--filter` flag:

```console
$ docker compose ps --filter status=running
NAME            IMAGE     COMMAND           SERVICE    CREATED         STATUS          PORTS
example-foo-1   alpine    "/entrypoint.…"   foo        4 seconds ago   Up 2 seconds    0.0.0.0:8080->80/tcp
```

The `docker compose ps` command currently only supports the `--filter status=<status>`
option, but additional filter options may be added in the future.

---

# docker compose publish

# docker compose publish

| Description | Publish compose application |
| --- | --- |
| Usage | docker compose publish [OPTIONS] REPOSITORY[:TAG] |

## Description

Publish compose application

## Options

| Option | Default | Description |
| --- | --- | --- |
| --app |  | Published compose application (includes referenced images) |
| --oci-version |  | OCI image/artifact specification version (automatically determined by default) |
| --resolve-image-digests |  | Pin image tags to digests |
| --with-env |  | Include environment variables in the published OCI artifact |
| -y, --yes |  | Assume "yes" as answer to all prompts |

---

# docker compose pull

# docker compose pull

| Description | Pull service images |
| --- | --- |
| Usage | docker compose pull [OPTIONS] [SERVICE...] |

## Description

Pulls an image associated with a service defined in a `compose.yaml` file, but does not start containers based on those images

## Options

| Option | Default | Description |
| --- | --- | --- |
| --ignore-buildable |  | Ignore images that can be built |
| --ignore-pull-failures |  | Pull what it can and ignores images with pull failures |
| --include-deps |  | Also pull services declared as dependencies |
| --policy |  | Apply pull policy ("missing"|"always") |
| -q, --quiet |  | Pull without printing progress information |

## Examples

Consider the following `compose.yaml`:

```yaml
services:
  db:
    image: postgres
  web:
    build: .
    command: bundle exec rails s -p 3000 -b '0.0.0.0'
    volumes:
      - .:/myapp
    ports:
      - "3000:3000"
    depends_on:
      - db
```

If you run `docker compose pull ServiceName` in the same directory as the `compose.yaml` file that defines the service,
Docker pulls the associated image. For example, to call the postgres image configured as the db service in our example,
you would run `docker compose pull db`.

```console
$ docker compose pull db
[+] Running 1/15
 ⠸ db Pulling                                                             12.4s
   ⠿ 45b42c59be33 Already exists                                           0.0s
   ⠹ 40adec129f1a Downloading  3.374MB/4.178MB                             9.3s
   ⠹ b4c431d00c78 Download complete                                        9.3s
   ⠹ 2696974e2815 Download complete                                        9.3s
   ⠹ 564b77596399 Downloading  5.622MB/7.965MB                             9.3s
   ⠹ 5044045cf6f2 Downloading  216.7kB/391.1kB                             9.3s
   ⠹ d736e67e6ac3 Waiting                                                  9.3s
   ⠹ 390c1c9a5ae4 Waiting                                                  9.3s
   ⠹ c0e62f172284 Waiting                                                  9.3s
   ⠹ ebcdc659c5bf Waiting                                                  9.3s
   ⠹ 29be22cb3acc Waiting                                                  9.3s
   ⠹ f63c47038e66 Waiting                                                  9.3s
   ⠹ 77a0c198cde5 Waiting                                                  9.3s
   ⠹ c8752d5b785c Waiting                                                  9.3s
```

`docker compose pull` tries to pull image for services with a build section. If pull fails, it lets you know this service image must be built. You can skip this by setting `--ignore-buildable` flag.

---

# docker compose push

# docker compose push

| Description | Push service images |
| --- | --- |
| Usage | docker compose push [OPTIONS] [SERVICE...] |

## Description

Pushes images for services to their respective registry/repository.

The following assumptions are made:

- You are pushing an image you have built locally
- You have access to the build key

Examples

```yaml
services:
  service1:
    build: .
    image: localhost:5000/yourimage  ## goes to local registry

  service2:
    build: .
    image: your-dockerid/yourimage  ## goes to your repository on Docker Hub
```

## Options

| Option | Default | Description |
| --- | --- | --- |
| --ignore-push-failures |  | Push what it can and ignores images with push failures |
| --include-deps |  | Also push images of services declared as dependencies |
| -q, --quiet |  | Push without printing progress information |

---

# docker compose restart

# docker compose restart

| Description | Restart service containers |
| --- | --- |
| Usage | docker compose restart [OPTIONS] [SERVICE...] |

## Description

Restarts all stopped and running services, or the specified services only.

If you make changes to your `compose.yml` configuration, these changes are not reflected
after running this command. For example, changes to environment variables (which are added
after a container is built, but before the container's command is executed) are not updated
after restarting.

If you are looking to configure a service's restart policy, refer to
[restart](https://github.com/compose-spec/compose-spec/blob/main/spec.md#restart)
or [restart_policy](https://github.com/compose-spec/compose-spec/blob/main/deploy.md#restart_policy).

## Options

| Option | Default | Description |
| --- | --- | --- |
| --no-deps |  | Don't restart dependent services |
| -t, --timeout |  | Specify a shutdown timeout in seconds |

---

# docker compose rm

# docker compose rm

| Description | Removes stopped service containers |
| --- | --- |
| Usage | docker compose rm [OPTIONS] [SERVICE...] |

## Description

Removes stopped service containers.

By default, anonymous volumes attached to containers are not removed. You can override this with `-v`. To list all
volumes, use `docker volume ls`.

Any data which is not in a volume is lost.

Running the command with no options also removes one-off containers created by `docker compose run`:

```console
$ docker compose rm
Going to remove djangoquickstart_web_run_1
Are you sure? [yN] y
Removing djangoquickstart_web_run_1 ... done
```

## Options

| Option | Default | Description |
| --- | --- | --- |
| -f, --force |  | Don't ask to confirm removal |
| -s, --stop |  | Stop the containers, if required, before removing |
| -v, --volumes |  | Remove any anonymous volumes attached to containers |

---

# docker compose run

# docker compose run

| Description | Run a one-off command on a service |
| --- | --- |
| Usage | docker compose run [OPTIONS] SERVICE [COMMAND] [ARGS...] |

## Description

Runs a one-time command against a service.

The following command starts the `web` service and runs `bash` as its command:

```console
$ docker compose run web bash
```

Commands you use with run start in new containers with configuration defined by that of the service,
including volumes, links, and other details. However, there are two important differences:

First, the command passed by `run` overrides the command defined in the service configuration. For example, if the
`web` service configuration is started with `bash`, then `docker compose run web python app.py` overrides it with
`python app.py`.

The second difference is that the `docker compose run` command does not create any of the ports specified in the
service configuration. This prevents port collisions with already-open ports. If you do want the service’s ports
to be created and mapped to the host, specify the `--service-ports`

```console
$ docker compose run --service-ports web python manage.py shell
```

Alternatively, manual port mapping can be specified with the `--publish` or `-p` options, just as when using docker run:

```console
$ docker compose run --publish 8080:80 -p 2022:22 -p 127.0.0.1:2021:21 web python manage.py shell
```

If you start a service configured with links, the run command first checks to see if the linked service is running
and starts the service if it is stopped. Once all the linked services are running, the run executes the command you
passed it. For example, you could run:

```console
$ docker compose run db psql -h db -U docker
```

This opens an interactive PostgreSQL shell for the linked `db` container.

If you do not want the run command to start linked containers, use the `--no-deps` flag:

```console
$ docker compose run --no-deps web python manage.py shell
```

If you want to remove the container after running while overriding the container’s restart policy, use the `--rm` flag:

```console
$ docker compose run --rm web python manage.py db upgrade
```

This runs a database upgrade script, and removes the container when finished running, even if a restart policy is
specified in the service configuration.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --build |  | Build image before starting container |
| --cap-add |  | Add Linux capabilities |
| --cap-drop |  | Drop Linux capabilities |
| -d, --detach |  | Run container in background and print container ID |
| --entrypoint |  | Override the entrypoint of the image |
| -e, --env |  | Set environment variables |
| --env-from-file |  | Set environment variables from file |
| -i, --interactive | true | Keep STDIN open even if not attached |
| -l, --label |  | Add or override a label |
| --name |  | Assign a name to the container |
| -T, --no-TTY | true | Disable pseudo-TTY allocation (default: auto-detected) |
| --no-deps |  | Don't start linked services |
| -p, --publish |  | Publish a container's port(s) to the host |
| --pull | policy | Pull image before running ("always"|"missing"|"never") |
| -q, --quiet |  | Don't print anything to STDOUT |
| --quiet-build |  | Suppress progress output from the build process |
| --quiet-pull |  | Pull without printing progress information |
| --remove-orphans |  | Remove containers for services not defined in the Compose file |
| --rm |  | Automatically remove the container when it exits |
| -P, --service-ports |  | Run command with all service's ports enabled and mapped to the host |
| --use-aliases |  | Use the service's network useAliases in the network(s) the container connects to |
| -u, --user |  | Run as specified username or uid |
| -v, --volume |  | Bind mount a volume |
| -w, --workdir |  | Working directory inside the container |

---

# docker compose start

# docker compose start

| Description | Start services |
| --- | --- |
| Usage | docker compose start [SERVICE...] |

## Description

Starts existing containers for a service

## Options

| Option | Default | Description |
| --- | --- | --- |
| --wait |  | Wait for services to be running|healthy. Implies detached mode. |
| --wait-timeout |  | Maximum duration in seconds to wait for the project to be running|healthy |

---

# docker compose stop

# docker compose stop

| Description | Stop services |
| --- | --- |
| Usage | docker compose stop [OPTIONS] [SERVICE...] |

## Description

Stops running containers without removing them. They can be started again with `docker compose start`.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -t, --timeout |  | Specify a shutdown timeout in seconds |

---

# docker compose top

# docker compose top

| Description | Display the running processes |
| --- | --- |
| Usage | docker compose top [SERVICES...] |

## Description

Displays the running processes

## Examples

```console
$ docker compose top
example_foo_1
UID    PID      PPID     C    STIME   TTY   TIME       CMD
root   142353   142331   2    15:33   ?     00:00:00   ping localhost -c 5
```

---

# docker compose unpause

# docker compose unpause

| Description | Unpause services |
| --- | --- |
| Usage | docker compose unpause [SERVICE...] |

## Description

Unpauses paused containers of a service

---

# docker compose up

# docker compose up

| Description | Create and start containers |
| --- | --- |
| Usage | docker compose up [OPTIONS] [SERVICE...] |

## Description

Builds, (re)creates, starts, and attaches to containers for a service.

Unless they are already running, this command also starts any linked services.

The `docker compose up` command aggregates the output of each container (like `docker compose logs --follow` does).
One can optionally select a subset of services to attach to using `--attach` flag, or exclude some services using
`--no-attach` to prevent output to be flooded by some verbose services.

When the command exits, all containers are stopped. Running `docker compose up --detach` starts the containers in the
background and leaves them running.

If there are existing containers for a service, and the service’s configuration or image was changed after the
container’s creation, `docker compose up` picks up the changes by stopping and recreating the containers
(preserving mounted volumes). To prevent Compose from picking up changes, use the `--no-recreate` flag.

If you want to force Compose to stop and recreate all containers, use the `--force-recreate` flag.

If the process encounters an error, the exit code for this command is `1`.
If the process is interrupted using `SIGINT` (ctrl + C) or `SIGTERM`, the containers are stopped, and the exit code is `0`.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --abort-on-container-exit |  | Stops all containers if any container was stopped. Incompatible with -d |
| --abort-on-container-failure |  | Stops all containers if any container exited with failure. Incompatible with -d |
| --always-recreate-deps |  | Recreate dependent containers. Incompatible with --no-recreate. |
| --attach |  | Restrict attaching to the specified services. Incompatible with --attach-dependencies. |
| --attach-dependencies |  | Automatically attach to log output of dependent services |
| --build |  | Build images before starting containers |
| -d, --detach |  | Detached mode: Run containers in the background |
| --exit-code-from |  | Return the exit code of the selected service container. Implies --abort-on-container-exit |
| --force-recreate |  | Recreate containers even if their configuration and image haven't changed |
| --menu |  | Enable interactive shortcuts when running attached. Incompatible with --detach. Can also be enable/disable by setting COMPOSE_MENU environment var. |
| --no-attach |  | Do not attach (stream logs) to the specified services |
| --no-build |  | Don't build an image, even if it's policy |
| --no-color |  | Produce monochrome output |
| --no-deps |  | Don't start linked services |
| --no-log-prefix |  | Don't print prefix in logs |
| --no-recreate |  | If containers already exist, don't recreate them. Incompatible with --force-recreate. |
| --no-start |  | Don't start the services after creating them |
| --pull | policy | Pull image before running ("always"|"missing"|"never") |
| --quiet-build |  | Suppress the build output |
| --quiet-pull |  | Pull without printing progress information |
| --remove-orphans |  | Remove containers for services not defined in the Compose file |
| -V, --renew-anon-volumes |  | Recreate anonymous volumes instead of retrieving data from the previous containers |
| --scale |  | Scale SERVICE to NUM instances. Overrides thescalesetting in the Compose file if present. |
| -t, --timeout |  | Use this timeout in seconds for container shutdown when attached or when containers are already running |
| --timestamps |  | Show timestamps |
| --wait |  | Wait for services to be running|healthy. Implies detached mode. |
| --wait-timeout |  | Maximum duration in seconds to wait for the project to be running|healthy |
| -w, --watch |  | Watch source code and rebuild/refresh containers when files are updated. |
| -y, --yes |  | Assume "yes" as answer to all prompts and run non-interactively |

---

# docker compose version

# docker compose version

| Description | Show the Docker Compose version information |
| --- | --- |
| Usage | docker compose version [OPTIONS] |

## Description

Show the Docker Compose version information

## Options

| Option | Default | Description |
| --- | --- | --- |
| -f, --format |  | Format the output. Values: [pretty | json]. (Default: pretty) |
| --short |  | Shows only Compose's version number |

---

# docker compose volumes

# docker compose volumes

| Description | List volumes |
| --- | --- |
| Usage | docker compose volumes [OPTIONS] [SERVICE...] |

## Description

List volumes

## Options

| Option | Default | Description |
| --- | --- | --- |
| --format | table | Format output using a custom template:'table': Print output in table format with column headers (default)'table TEMPLATE': Print output in table format using the given Go template'json': Print in JSON format'TEMPLATE': Print output using the given Go template.Refer tohttps://docs.docker.com/go/formatting/for more information about formatting output with templates |
| -q, --quiet |  | Only display volume names |

---

# docker compose wait

# docker compose wait

| Description | Block until containers of all (or specified) services stop. |
| --- | --- |
| Usage | docker compose wait SERVICE [SERVICE...] [OPTIONS] |

## Description

Block until containers of all (or specified) services stop.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --down-project |  | Drops project when the first container stops |

---

# docker compose watch

# docker compose watch

| Description | Watch build context for service and rebuild/refresh containers when files are updated |
| --- | --- |
| Usage | docker compose watch [SERVICE...] |

## Description

Watch build context for service and rebuild/refresh containers when files are updated

## Options

| Option | Default | Description |
| --- | --- | --- |
| --no-up |  | Do not build & start services before watching |
| --prune | true | Prune dangling images on rebuild |
| --quiet |  | hide build output |
