# Completion and more

# Completion

> Set up your shell to get autocomplete for Docker commands and flags

# Completion

   Table of contents

---

You can generate a shell completion script for the Docker CLI using the `docker completion` command. The completion script gives you word completion for
commands, flags, and Docker objects (such as container and volume names) when
you hit `<Tab>` as you type into your terminal.

You can generate completion scripts for the following shells:

- [Bash](#bash)
- [Zsh](#zsh)
- [fish](#fish)

## Bash

To get Docker CLI completion with Bash, you first need to install the
`bash-completion` package which contains a number of Bash functions for shell
completion.

```bash
# Install using APT:
sudo apt install bash-completion

# Install using Homebrew (Bash version 4 or later):
brew install bash-completion@2
# Homebrew install for older versions of Bash:
brew install bash-completion

# With pacman:
sudo pacman -S bash-completion
```

After installing `bash-completion`, source the script in your shell
configuration file (in this example, `.bashrc`):

```bash
# On Linux:
cat <<EOT >> ~/.bashrc
if [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
fi
EOT

# On macOS / with Homebrew:
cat <<EOT >> ~/.bash_profile
[[ -r "$(brew --prefix)/etc/profile.d/bash_completion.sh" ]] && . "$(brew --prefix)/etc/profile.d/bash_completion.sh"
EOT
```

And reload your shell configuration:

```console
$ source ~/.bashrc
```

Now you can generate the Bash completion script using the `docker completion` command:

```console
$ mkdir -p ~/.local/share/bash-completion/completions
$ docker completion bash > ~/.local/share/bash-completion/completions/docker
```

## Zsh

The Zsh [completion system](http://zsh.sourceforge.net/Doc/Release/Completion-System.html)
takes care of things as long as the completion can be sourced using `FPATH`.

If you use Oh My Zsh, you can install completions without modifying `~/.zshrc`
by storing the completion script in the `~/.oh-my-zsh/completions` directory.

```console
$ mkdir -p ~/.oh-my-zsh/completions
$ docker completion zsh > ~/.oh-my-zsh/completions/_docker
```

If you're not using Oh My Zsh, store the completion script in a directory of
your choice and add the directory to `FPATH` in your `.zshrc`.

```console
$ mkdir -p ~/.docker/completions
$ docker completion zsh > ~/.docker/completions/_docker
```

```console
$ cat <<"EOT" >> ~/.zshrc
FPATH="$HOME/.docker/completions:$FPATH"
autoload -Uz compinit
compinit
EOT
```

## Fish

fish shell supports a [completion system](https://fishshell.com/docs/current/#tab-completion) natively.
To activate completion for Docker commands, copy or symlink the completion script to your fish shell `completions/` directory:

```console
$ mkdir -p ~/.config/fish/completions
$ docker completion fish > ~/.config/fish/completions/docker.fish
```

---

# Filter commands

> Use the filtering function in the CLI to selectively include resources that match the pattern you define.

# Filter commands

   Table of contents

---

You can use the `--filter` flag to scope your commands. When filtering, the
commands only include entries that match the pattern you specify.

## Using filters

The `--filter` flag expects a key-value pair separated by an operator.

```console
$ docker COMMAND --filter "KEY=VALUE"
```

The key represents the field that you want to filter on.
The value is the pattern that the specified field must match.
The operator can be either equals (`=`) or not equals (`!=`).

For example, the command `docker images --filter reference=alpine` filters the
output of the `docker images` command to only print `alpine` images.

```console
$ docker images
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
ubuntu       24.04     33a5cc25d22c   36 minutes ago   101MB
ubuntu       22.04     152dc042452c   36 minutes ago   88.1MB
alpine       3.21      a8cbb8c69ee7   40 minutes ago   8.67MB
alpine       latest    7144f7bab3d4   40 minutes ago   11.7MB
busybox      uclibc    3e516f71d880   48 minutes ago   2.4MB
busybox      glibc     7338d0c72c65   48 minutes ago   6.09MB
$ docker images --filter reference=alpine
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
alpine       3.21      a8cbb8c69ee7   40 minutes ago   8.67MB
alpine       latest    7144f7bab3d4   40 minutes ago   11.7MB
```

The available fields (`reference` in this case) depend on the command you run.
Some filters expect an exact match. Others handle partial matches. Some filters
let you use regular expressions.

Refer to the [CLI reference description](#reference) for each command to learn
about the supported filtering capabilities for each command.

## Combining filters

You can combine multiple filters by passing multiple `--filter` flags. The
following example shows how to print all images that match `alpine:latest` or
`busybox` - a logical `OR`.

```console
$ docker images
REPOSITORY   TAG       IMAGE ID       CREATED       SIZE
ubuntu       24.04     33a5cc25d22c   2 hours ago   101MB
ubuntu       22.04     152dc042452c   2 hours ago   88.1MB
alpine       3.21      a8cbb8c69ee7   2 hours ago   8.67MB
alpine       latest    7144f7bab3d4   2 hours ago   11.7MB
busybox      uclibc    3e516f71d880   2 hours ago   2.4MB
busybox      glibc     7338d0c72c65   2 hours ago   6.09MB
$ docker images --filter reference=alpine:latest --filter=reference=busybox
REPOSITORY   TAG       IMAGE ID       CREATED       SIZE
alpine       latest    7144f7bab3d4   2 hours ago   11.7MB
busybox      uclibc    3e516f71d880   2 hours ago   2.4MB
busybox      glibc     7338d0c72c65   2 hours ago   6.09MB
```

### Multiple negated filters

Some commands support negated filters on
[labels](https://docs.docker.com/engine/manage-resources/labels/).
Negated filters only consider results that don't match the specified patterns.
The following command prunes all containers that aren't labeled `foo`.

```console
$ docker container prune --filter "label!=foo"
```

There's a catch in combining multiple negated label filters. Multiple negated
filters create a single negative constraint - a logical `AND`. The following
command prunes all containers except those labeled both `foo` and `bar`.
Containers labeled either `foo` or `bar`, but not both, will be pruned.

```console
$ docker container prune --filter "label!=foo" --filter "label!=bar"
```

## Reference

For more information about filtering commands, refer to the CLI reference
description for commands that support the `--filter` flag:

- [docker config ls](https://docs.docker.com/reference/cli/docker/config/ls/)
- [docker container prune](https://docs.docker.com/reference/cli/docker/container/prune/)
- [docker image prune](https://docs.docker.com/reference/cli/docker/image/prune/)
- [docker image ls](https://docs.docker.com/reference/cli/docker/image/ls/)
- [docker network ls](https://docs.docker.com/reference/cli/docker/network/ls/)
- [docker network prune](https://docs.docker.com/reference/cli/docker/network/prune/)
- [docker node ls](https://docs.docker.com/reference/cli/docker/node/ls/)
- [docker node ps](https://docs.docker.com/reference/cli/docker/node/ps/)
- [docker plugin ls](https://docs.docker.com/reference/cli/docker/plugin/ls/)
- [docker container ls](https://docs.docker.com/reference/cli/docker/container/ls/)
- [docker search](https://docs.docker.com/reference/cli/docker/search/)
- [docker secret ls](https://docs.docker.com/reference/cli/docker/secret/ls/)
- [docker service ls](https://docs.docker.com/reference/cli/docker/service/ls/)
- [docker service ps](https://docs.docker.com/reference/cli/docker/service/ps/)
- [docker stack ps](https://docs.docker.com/reference/cli/docker/stack/ps/)
- [docker system prune](https://docs.docker.com/reference/cli/docker/system/prune/)
- [docker volume ls](https://docs.docker.com/reference/cli/docker/volume/ls/)
- [docker volume prune](https://docs.docker.com/reference/cli/docker/volume/prune/)

---

# Format command and log output

> CLI and log output formatting reference

# Format command and log output

   Table of contents

---

Docker supports [Go templates](https://golang.org/pkg/text/template/) which you
can use to manipulate the output format of certain commands and log drivers.

Docker provides a set of basic functions to manipulate template elements.
All of these examples use the `docker inspect` command, but many other CLI
commands have a `--format` flag, and many of the CLI command references
include examples of customizing the output format.

> Note
>
> When using the `--format` flag, you need to observe your shell environment.
> In a POSIX shell, you can run the following with a single quote:
>
>
>
> ```console
> $ docker inspect --format '{{join .Args " , "}}'
> ```
>
>
>
> Otherwise, in a Windows shell (for example, PowerShell), you need to use single quotes, but
> escape the double quotes inside the parameters as follows:
>
>
>
> ```console
> $ docker inspect --format '{{join .Args \" , \"}}'
> ```

## join

`join` concatenates a list of strings to create a single string.
It puts a separator between each element in the list.

```console
$ docker inspect --format '{{join .Args " , "}}' container
```

## table

`table` specifies which fields you want to see its output.

```console
$ docker image list --format "table {{.ID}}\t{{.Repository}}\t{{.Tag}}\t{{.Size}}"
```

## json

`json` encodes an element as a json string.

```console
$ docker inspect --format '{{json .Mounts}}' container
```

## lower

`lower` transforms a string into its lowercase representation.

```console
$ docker inspect --format "{{lower .Name}}" container
```

## split

`split` slices a string into a list of strings separated by a separator.

```console
$ docker inspect --format '{{split .Image ":"}}' container
```

## title

`title` capitalizes the first character of a string.

```console
$ docker inspect --format "{{title .Name}}" container
```

## upper

`upper` transforms a string into its uppercase representation.

```console
$ docker inspect --format "{{upper .Name}}" container
```

## pad

`pad` adds whitespace padding to a string. You can specify the number of spaces to add before and after the string.

```console
$ docker image list --format '{{pad .Repository 5 10}}'
```

This example adds 5 spaces before the image repository name and 10 spaces after.

## truncate

`truncate` shortens a string to a specified length. If the string is shorter than the specified length, it remains unchanged.

```console
$ docker image list --format '{{truncate .Repository 15}}'
```

This example displays the image repository name, truncating it to the first 15 characters if it's longer.

## println

`println` prints each value on a new line.

```console
$ docker inspect --format='{{range .NetworkSettings.Networks}}{{println .IPAddress}}{{end}}' container
```

## Hint

To find out what data can be printed, show all content as json:

```console
$ docker container ls --format='{{json .}}'
```

---

# OpenTelemetry for the Docker CLI

> Learn about how to capture OpenTelemetry metrics for the Docker command line

# OpenTelemetry for the Docker CLI

   Table of contents

---

Requires: Docker Engine
[26.1.0](https://docs.docker.com/engine/release-notes/26.1/#2610) and later

The Docker CLI supports [OpenTelemetry](https://opentelemetry.io/docs/) instrumentation
for emitting metrics about command invocations. This is disabled by default.
You can configure the CLI to start emitting metrics to the endpoint that you
specify. This allows you to capture information about your `docker` command
invocations for more insight into your Docker usage.

Exporting metrics is opt-in, and you control where data is being sent by
specifying the destination address of the metrics collector.

## What is OpenTelemetry?

OpenTelemetry, or OTel for short, is an open observability framework for
creating and managing telemetry data, such as traces, metrics, and logs.
OpenTelemetry is vendor- and tool-agnostic, meaning that it can be used with a
broad variety of Observability backends.

Support for OpenTelemetry instrumentation in the Docker CLI means that the CLI can emit
information about events that take place, using the protocols and conventions
defined in the Open Telemetry specification.

## How it works

The Docker CLI doesn't emit telemetry data by default. Only if you've set an
environment variable on your system will Docker CLI attempt to emit OpenTelemetry
metrics, to the endpoint that you specify.

```bash
DOCKER_CLI_OTEL_EXPORTER_OTLP_ENDPOINT=<endpoint>
```

The variable specifies the endpoint of an OpenTelemetry collector, where telemetry data
about `docker` CLI invocation should be sent. To capture the data, you'll need
an OpenTelemetry collector listening on that endpoint.

The purpose of a collector is to receive the telemetry data, process it, and
exports it to a backend. The backend is where the telemetry data gets stored.
You can choose from a number of different backends, such as Prometheus or
InfluxDB.

Some backends provide tools for visualizing the metrics directly.
Alternatively, you can also run a dedicated frontend with support for
generating more useful graphs, such as Grafana.

## Setup

To get started capturing telemetry data for the Docker CLI, you'll need to:

- Set the `DOCKER_CLI_OTEL_EXPORTER_OTLP_ENDPOINT` environment variable to point to an OpenTelemetry collector endpoint
- Run an OpenTelemetry collector that receives the signals from CLI command invocations
- Run a backend for storing the data received from the collector

The following Docker Compose file bootstraps a set of services to get started with OpenTelemetry.
It includes an OpenTelemetry collector that the CLI can send metrics to,
and a Prometheus backend that scrapes the metrics off the collector.

compose.yaml

```yaml
name: cli-otel
services:
  prometheus:
    image: prom/prometheus
    command:
      - "--config.file=/etc/prometheus/prom.yml"
    ports:
      # Publish the Prometheus frontend on localhost:9091
      - 9091:9090
    restart: always
    volumes:
      # Store Prometheus data in a volume:
      - prom_data:/prometheus
      # Mount the prom.yml config file
      - ./prom.yml:/etc/prometheus/prom.yml
  otelcol:
    image: otel/opentelemetry-collector
    restart: always
    depends_on:
      - prometheus
    ports:
      - 4317:4317
    volumes:
      # Mount the otelcol.yml config file
      - ./otelcol.yml:/etc/otelcol/config.yaml

volumes:
  prom_data:
```

This service assumes that the following two configuration files exist alongside
`compose.yaml`:

- otelcol.yml
  ```yaml
  # Receive signals over gRPC and HTTP
  receivers:
    otlp:
      protocols:
        grpc:
        http:
  # Establish an endpoint for Prometheus to scrape from
  exporters:
    prometheus:
      endpoint: "0.0.0.0:8889"
  service:
    pipelines:
      metrics:
        receivers: [otlp]
        exporters: [prometheus]
  ```
- prom.yml
  ```yaml
  # Configure Prometheus to scrape the OpenTelemetry collector endpoint
  scrape_configs:
    - job_name: "otel-collector"
      scrape_interval: 1s
      static_configs:
        - targets: ["otelcol:8889"]
  ```

With these files in place:

1. Start the Docker Compose services:
  ```console
  $ docker compose up
  ```
2. Configure Docker CLI to export telemetry to the OpenTelemetry collector.
  ```console
  $ export DOCKER_CLI_OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
  ```
3. Run a `docker` command to trigger the CLI into sending a metric signal to
  the OpenTelemetry collector.
  ```console
  $ docker version
  ```
4. To view telemetry metrics created by the CLI, open the Prometheus expression
  browser by going to [http://localhost:9091/graph](http://localhost:9091/graph).
5. In the **Query** field, enter `command_time_milliseconds_total`, and execute
  the query to see the telemetry data.

## Available metrics

Docker CLI currently exports a single metric, `command.time`, which measures
the execution duration of a command in milliseconds. This metric has the
following attributes:

- `command.name`: the name of the command
- `command.status.code`: the exit code of the command
- `command.stderr.isatty`: true if stderr is attached to a TTY
- `command.stdin.isatty`: true if stdin is attached to a TTY
- `command.stdout.isatty`: true if stdout is attached to a TTY

---

# Use a proxy server with the Docker CLI

> How to configure the Docker client CLI to use a proxy server

# Use a proxy server with the Docker CLI

   Table of contents

---

This page describes how to configure the Docker CLI to use proxies via
environment variables in containers.

This page doesn't describe how to configure proxies for Docker Desktop.
For instructions, see
[configuring Docker Desktop to use HTTP/HTTPS proxies](https://docs.docker.com/desktop/settings-and-maintenance/settings/#proxies).

If you're running Docker Engine without Docker Desktop, refer to
[Configure the Docker daemon to use a proxy](https://docs.docker.com/engine/daemon/proxy/)
to learn how to configure a proxy server for the Docker daemon (`dockerd`) itself.

If your container needs to use an HTTP, HTTPS, or FTP proxy server, you can
configure it in different ways:

- [Configure the Docker client](#configure-the-docker-client)
- [Set proxy using the CLI](#set-proxy-using-the-cli)

> Note
>
> Unfortunately, there's no standard that defines how web clients should handle proxy
> environment variables, or the format for defining them.
>
>
>
> If you're interested in the history of these variables, check out this blog
> post on the subject, by the GitLab team:
> [We need to talk: Can we standardize NO_PROXY?](https://about.gitlab.com/blog/2021/01/27/we-need-to-talk-no-proxy/).

## Configure the Docker client

You can add proxy configurations for the Docker client using a JSON
configuration file, located in `~/.docker/config.json`.
Builds and containers use the configuration specified in this file.

```json
{
 "proxies": {
   "default": {
     "httpProxy": "http://proxy.example.com:3128",
     "httpsProxy": "https://proxy.example.com:3129",
     "noProxy": "*.test.example.com,.example.org,127.0.0.0/8"
   }
 }
}
```

> Warning
>
> Proxy settings may contain sensitive information. For example, some proxy servers
> require authentication information to be included in their URL, or their
> address may expose IP-addresses or hostnames of your company's environment.
>
>
>
> Environment variables are stored as plain text in the container's configuration,
> and as such can be inspected through the remote API or committed to an image
> when using `docker commit`.

The configuration becomes active after saving the file, you don't need to
restart Docker. However, the configuration only applies to new containers and
builds, and doesn't affect existing containers.

The following table describes the available configuration parameters.

| Property | Description |
| --- | --- |
| httpProxy | Sets theHTTP_PROXYandhttp_proxyenvironment variables and build arguments. |
| httpsProxy | Sets theHTTPS_PROXYandhttps_proxyenvironment variables and build arguments. |
| ftpProxy | Sets theFTP_PROXYandftp_proxyenvironment variables and build arguments. |
| noProxy | Sets theNO_PROXYandno_proxyenvironment variables and build arguments. |
| allProxy | Sets theALL_PROXYandall_proxyenvironment variables and build arguments. |

These settings are used to configure proxy environment variables for containers
only, and not used as proxy settings for the Docker CLI or the Docker Engine
itself.
Refer to the
[environment variables](https://docs.docker.com/reference/cli/docker/#environment-variables)
and
[configure the Docker daemon to use a proxy server](https://docs.docker.com/engine/daemon/proxy/)
sections for configuring proxy settings for the CLI and daemon.

### Run containers with a proxy configuration

When you start a container, its proxy-related environment variables are set
to reflect your proxy configuration in `~/.docker/config.json`.

For example, assuming a proxy configuration like the example
shown in the [earlier section](#configure-the-docker-client), environment
variables for containers that you run are set as follows:

```console
$ docker run --rm alpine sh -c 'env | grep -i  _PROXY'
https_proxy=http://proxy.example.com:3129
HTTPS_PROXY=http://proxy.example.com:3129
http_proxy=http://proxy.example.com:3128
HTTP_PROXY=http://proxy.example.com:3128
no_proxy=*.test.example.com,.example.org,127.0.0.0/8
NO_PROXY=*.test.example.com,.example.org,127.0.0.0/8
```

### Build with a proxy configuration

When you invoke a build, proxy-related build arguments are pre-populated
automatically, based on the proxy settings in your Docker client configuration
file.

Assuming a proxy configuration like the example shown in the
[earlier section](#configure-the-docker-client), environment
are set as follows during builds:

```console
$ docker build \
  --no-cache \
  --progress=plain \
  - <<EOF
FROM alpine
RUN env | grep -i _PROXY
EOF
```

```console
#5 [2/2] RUN env | grep -i _PROXY
#5 0.100 HTTPS_PROXY=https://proxy.example.com:3129
#5 0.100 no_proxy=*.test.example.com,.example.org,127.0.0.0/8
#5 0.100 NO_PROXY=*.test.example.com,.example.org,127.0.0.0/8
#5 0.100 https_proxy=https://proxy.example.com:3129
#5 0.100 http_proxy=http://proxy.example.com:3128
#5 0.100 HTTP_PROXY=http://proxy.example.com:3128
#5 DONE 0.1s
```

### Configure proxy settings per daemon

The `default` key under `proxies` in `~/.docker/config.json` configures the proxy
settings for all daemons that the client connects to.
To configure the proxies for individual daemons,
use the address of the daemon instead of the `default` key.

The following example configures both a default proxy config,
and a no-proxy override for the Docker daemon on address
`tcp://docker-daemon1.example.com`:

```json
{
 "proxies": {
   "default": {
     "httpProxy": "http://proxy.example.com:3128",
     "httpsProxy": "https://proxy.example.com:3129",
     "noProxy": "*.test.example.com,.example.org,127.0.0.0/8"
   },
   "tcp://docker-daemon1.example.com": {
     "noProxy": "*.internal.example.net"
   }
 }
}
```

## Set proxy using the CLI

Instead of [configuring the Docker client](#configure-the-docker-client),
you can specify proxy configurations on the command-line when you invoke the
`docker build` and `docker run` commands.

Proxy configuration on the command-line uses the `--build-arg` flag for builds,
and the `--env` flag for when you want to run containers with a proxy.

```console
$ docker build --build-arg HTTP_PROXY="http://proxy.example.com:3128" .
$ docker run --env HTTP_PROXY="http://proxy.example.com:3128" redis
```

For a list of all the proxy-related build arguments that you can use with the
`docker build` command, see
[Predefined ARGs](https://docs.docker.com/reference/dockerfile/#predefined-args).
These proxy values are only available in the build container.
They're not included in the build output.

## Proxy as environment variable for builds

Don't use the `ENV` Dockerfile instruction to specify proxy settings for builds.
Use build arguments instead.

Using environment variables for proxies embeds the configuration into the image.
If the proxy is an internal proxy, it might not be accessible for containers
created from that image.

Embedding proxy settings in images also poses a security risk, as the values
may include sensitive information.

---

# Run multiple processes in a container

> Learn how to run more than one process in a single container

# Run multiple processes in a container

   Table of contents

---

A container's main running process is the `ENTRYPOINT` and/or `CMD` at the
end of the `Dockerfile`. It's best practice to separate areas of concern by
using one service per container. That service may fork into multiple
processes (for example, Apache web server starts multiple worker processes).
It's ok to have multiple processes, but to get the most benefit out of Docker,
avoid one container being responsible for multiple aspects of your overall
application. You can connect multiple containers using user-defined networks and
shared volumes.

The container's main process is responsible for managing all processes that it
starts. In some cases, the main process isn't well-designed, and doesn't handle
"reaping" (stopping) child processes gracefully when the container exits. If
your process falls into this category, you can use the `--init` option when you
run the container. The `--init` flag inserts a tiny init-process into the
container as the main process, and handles reaping of all processes when the
container exits. Handling such processes this way is superior to using a
full-fledged init process such as `sysvinit` or `systemd` to handle process
lifecycle within your container.

If you need to run more than one service within a container, you can achieve
this in a few different ways.

## Use a wrapper script

Put all of your commands in a wrapper script, complete with testing and
debugging information. Run the wrapper script as your `CMD`. The following is a
naive example. First, the wrapper script:

```bash
#!/bin/bash

# Start the first process
./my_first_process &

# Start the second process
./my_second_process &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?
```

Next, the Dockerfile:

```dockerfile
# syntax=docker/dockerfile:1
FROM ubuntu:latest
COPY my_first_process my_first_process
COPY my_second_process my_second_process
COPY my_wrapper_script.sh my_wrapper_script.sh
CMD ./my_wrapper_script.sh
```

## Use Bash job controls

If you have one main process that needs to start first and stay running but you
temporarily need to run some other processes (perhaps to interact with the main
process) then you can use bash's job control. First, the wrapper script:

```bash
#!/bin/bash

# turn on bash's job control
set -m

# Start the primary process and put it in the background
./my_main_process &

# Start the helper process
./my_helper_process

# the my_helper_process might need to know how to wait on the
# primary process to start before it does its work and returns

# now we bring the primary process back into the foreground
# and leave it there
fg %1
```

```dockerfile
# syntax=docker/dockerfile:1
FROM ubuntu:latest
COPY my_main_process my_main_process
COPY my_helper_process my_helper_process
COPY my_wrapper_script.sh my_wrapper_script.sh
CMD ./my_wrapper_script.sh
```

## Use a process manager

Use a process manager like `supervisord`. This is more involved than the other
options, as it requires you to bundle `supervisord` and its configuration into
your image (or base your image on one that includes `supervisord`), along with
the different applications it manages. Then you start `supervisord`, which
manages your processes for you.

The following Dockerfile example shows this approach. The example assumes that
these files exist at the root of the build context:

- `supervisord.conf`
- `my_first_process`
- `my_second_process`

```dockerfile
# syntax=docker/dockerfile:1
FROM ubuntu:latest
RUN apt-get update && apt-get install -y supervisor
RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY my_first_process my_first_process
COPY my_second_process my_second_process
CMD ["/usr/bin/supervisord"]
```

If you want to make sure both processes output their `stdout` and `stderr` to
the container logs, you can add the following to the `supervisord.conf` file:

```ini
[supervisord]
nodaemon=true
logfile=/dev/null
logfile_maxbytes=0

[program:app]
stdout_logfile=/dev/fd/1
stdout_logfile_maxbytes=0
redirect_stderr=true
```
