# Install Docker Engine and more

# Install Docker Engine

> Learn how to choose the best method for you to install Docker Engine. This client-server application is available on Linux, Mac, Windows, and as a static binary.

# Install Docker Engine

   Table of contents

---

This section describes how to install Docker Engine on Linux, also known as
Docker CE. Docker Engine is also available for Windows, macOS, and Linux,
through Docker Desktop. For instructions on how to install Docker Desktop,
see:
[Overview of Docker Desktop](https://docs.docker.com/desktop/).

## Installation procedures for supported platforms

Click on a platform's link to view the relevant installation procedure.

| Platform | x86_64 / amd64 | arm64 / aarch64 | arm (32-bit) | ppc64le | s390x |
| --- | --- | --- | --- | --- | --- |
| CentOS | ✅ | ✅ |  | ✅ |  |
| Debian | ✅ | ✅ | ✅ | ✅ |  |
| Fedora | ✅ | ✅ |  | ✅ |  |
| Raspberry Pi OS (32-bit) |  |  | ⚠️ |  |  |
| RHEL | ✅ | ✅ |  |  | ✅ |
| SLES |  |  |  |  | ❌ |
| Ubuntu | ✅ | ✅ | ✅ | ✅ | ✅ |
| Binaries | ✅ | ✅ | ✅ |  |  |

### Other Linux distributions

> Note
>
> While the following instructions may work, Docker doesn't test or verify
> installation on distribution derivatives.

- If you use Debian derivatives such as "BunsenLabs Linux", "Kali Linux" or
  "LMDE" (Debian-based Mint) should follow the installation instructions for
  [Debian](https://docs.docker.com/engine/install/debian/), substitute the version of your distribution for the
  corresponding Debian release. Refer to the documentation of your distribution to find
  which Debian release corresponds with your derivative version.
- Likewise, if you use Ubuntu derivatives such as "Kubuntu", "Lubuntu" or "Xubuntu"
  you should follow the installation instructions for [Ubuntu](https://docs.docker.com/engine/install/ubuntu/),
  substituting the version of your distribution for the corresponding Ubuntu release.
  Refer to the documentation of your distribution to find which Ubuntu release
  corresponds with your derivative version.
- Some Linux distributions provide a package of Docker Engine through their
  package repositories. These packages are built and maintained by the Linux
  distribution's package maintainers and may have differences in configuration
  or are built from modified source code. Docker isn't involved in releasing these
  packages and you should report any bugs or issues involving these packages to
  your Linux distribution's issue tracker.

Docker provides [binaries](https://docs.docker.com/engine/install/binaries/) for manual installation of Docker Engine.
These binaries are statically linked and you can use them on any Linux distribution.

## Release channels

Docker Engine has two types of update channels, **stable** and **test**:

- The **stable** channel gives you the latest versions released for general availability.
- The **test** channel gives you pre-release versions that are ready for testing before
  general availability.

Use the test channel with caution. Pre-release versions include experimental and
early-access features that are subject to breaking changes.

## Support

Docker Engine is an open source project, supported by the Moby project maintainers
and community members. Docker doesn't provide support for Docker Engine.
Docker provides support for Docker products, including Docker Desktop, which uses
Docker Engine as one of its components.

For information about the open source project, refer to the
[Moby project website](https://mobyproject.org/).

### Upgrade path

Patch releases are always backward compatible with its major and minor version.

### Licensing

Commercial use of Docker Engine obtained via Docker Desktop
within larger enterprises (exceeding 250 employees OR with annual revenue surpassing
$10 million USD), requires a [paid subscription](https://www.docker.com/pricing/).
Apache License, Version 2.0. See [LICENSE](https://github.com/moby/moby/blob/master/LICENSE) for the full license.

## Reporting security issues

If you discover a security issue, we request that you bring it to our attention immediately.

DO NOT file a public issue. Instead, submit your report privately to [security@docker.com](mailto:security@docker.com).

Security reports are greatly appreciated, and Docker will publicly thank you for it.

## Get started

After setting up Docker, you can learn the basics with
[Getting started with Docker](https://docs.docker.com/get-started/introduction/).

---

# Configure logging drivers

> Learn how to configure logging driver for the Docker daemon

# Configure logging drivers

   Table of contents

---

Docker includes multiple logging mechanisms to help you get information from
running containers and services. These mechanisms are called logging drivers.
Each Docker daemon has a default logging driver, which each container uses
unless you configure it to use a different logging driver, or log driver for
short.

As a default, Docker uses the [json-filelogging driver](https://docs.docker.com/engine/logging/drivers/json-file/), which
caches container logs as JSON internally. In addition to using the logging drivers
included with Docker, you can also implement and use [logging driver plugins](https://docs.docker.com/engine/logging/plugins/).

> Tip
>
> Use the `local` logging driver to prevent disk-exhaustion. By default, no log-rotation is performed. As a result, log-files stored by the
> default [json-filelogging driver](https://docs.docker.com/engine/logging/drivers/json-file/) logging driver can cause
> a significant amount of disk space to be used for containers that generate much
> output, which can lead to disk space exhaustion.
>
>
>
> Docker keeps the json-file logging driver (without log-rotation) as a default
> to remain backwards compatible with older versions of Docker, and for situations
> where Docker is used as runtime for Kubernetes.
>
>
>
> For other situations, the `local` logging driver is recommended as it performs
> log-rotation by default, and uses a more efficient file format. Refer to the
> [Configure the default logging driver](#configure-the-default-logging-driver)
> section below to learn how to configure the `local` logging driver as a default,
> and the [local file logging driver](https://docs.docker.com/engine/logging/drivers/local/) page for more details about the
> `local` logging driver.

## Configure the default logging driver

To configure the Docker daemon to default to a specific logging driver, set the
value of `log-driver` to the name of the logging driver in the `daemon.json`
configuration file. Refer to the "daemon configuration file" section in the
[dockerdreference manual](https://docs.docker.com/reference/cli/dockerd/#daemon-configuration-file)
for details.

The default logging driver is `json-file`. The following example sets the default
logging driver to the [locallog driver](https://docs.docker.com/engine/logging/drivers/local/):

```json
{
  "log-driver": "local"
}
```

If the logging driver has configurable options, you can set them in the
`daemon.json` file as a JSON object with the key `log-opts`. The following
example sets four configurable options on the `json-file` logging driver:

```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3",
    "labels": "production_status",
    "env": "os,customer"
  }
}
```

Restart Docker for the changes to take effect for newly created containers.
Existing containers don't use the new logging configuration automatically.

> Note
>
> `log-opts` configuration options in the `daemon.json` configuration file must
> be provided as strings. Boolean and numeric values (such as the value for
> `max-file` in the example above) must therefore be enclosed in quotes (`"`).

If you don't specify a logging driver, the default is `json-file`.
To find the current default logging driver for the Docker daemon, run
`docker info` and search for `Logging Driver`. You can use the following
command on Linux, macOS, or PowerShell on Windows:

```console
$ docker info --format '{{.LoggingDriver}}'

json-file
```

> Note
>
> Changing the default logging driver or logging driver options in the daemon
> configuration only affects containers that are created after the configuration
> is changed. Existing containers retain the logging driver options that were
> used when they were created. To update the logging driver for a container, the
> container has to be re-created with the desired options.
> Refer to the [configure the logging driver for a container](#configure-the-logging-driver-for-a-container)
> section below to learn how to find the logging-driver configuration of a
> container.

## Configure the logging driver for a container

When you start a container, you can configure it to use a different logging
driver than the Docker daemon's default, using the `--log-driver` flag. If the
logging driver has configurable options, you can set them using one or more
instances of the `--log-opt <NAME>=<VALUE>` flag. Even if the container uses the
default logging driver, it can use different configurable options.

The following example starts an Alpine container with the `none` logging driver.

```console
$ docker run -it --log-driver none alpine ash
```

To find the current logging driver for a running container, if the daemon
is using the `json-file` logging driver, run the following `docker inspect`
command, substituting the container name or ID for `<CONTAINER>`:

```console
$ docker inspect -f '{{.HostConfig.LogConfig.Type}}' CONTAINER

json-file
```

## Configure the delivery mode of log messages from container to log driver

Docker provides two modes for delivering messages from the container to the log
driver:

- (default) direct, blocking delivery from container to driver
- non-blocking delivery that stores log messages in an intermediate per-container buffer for consumption by driver

The `non-blocking` message delivery mode prevents applications from blocking due
to logging back pressure. Applications are likely to fail in unexpected ways when
STDERR or STDOUT streams block.

> Warning
>
> When the buffer is full, new messages will not be enqueued. Dropping messages is often preferred to blocking the
> log-writing process of an application.

The `mode` log option controls whether to use the `blocking` (default) or
`non-blocking` message delivery.

The `max-buffer-size` controls the size of the buffer used for
intermediate message storage when `mode` is set to `non-blocking`.
The default is `1m` meaning 1 MB (1 million bytes).
See [functionFromHumanSize()in thego-unitspackage](https://pkg.go.dev/github.com/docker/go-units#FromHumanSize) for the allowed format strings,
some examples are `1KiB` for 1024 bytes, `2g` for 2 billion bytes.

The following example starts an Alpine container with log output in non-blocking
mode and a 4 megabyte buffer:

```console
$ docker run -it --log-opt mode=non-blocking --log-opt max-buffer-size=4m alpine ping 127.0.0.1
```

### Use environment variables or labels with logging drivers

Some logging drivers add the value of a container's `--env|-e` or `--label`
flags to the container's logs. This example starts a container using the Docker
daemon's default logging driver (in the following example, `json-file`) but
sets the environment variable `os=ubuntu`.

```console
$ docker run -dit --label production_status=testing -e os=ubuntu alpine sh
```

If the logging driver supports it, this adds additional fields to the logging
output. The following output is generated by the `json-file` logging driver:

```json
"attrs":{"production_status":"testing","os":"ubuntu"}
```

## Supported logging drivers

The following logging drivers are supported. See the link to each driver's
documentation for its configurable options, if applicable. If you are using
[logging driver plugins](https://docs.docker.com/engine/logging/plugins/), you may
see more options.

| Driver | Description |
| --- | --- |
| none | No logs are available for the container anddocker logsdoes not return any output. |
| local | Logs are stored in a custom format designed for minimal overhead. |
| json-file | The logs are formatted as JSON. The default logging driver for Docker. |
| syslog | Writes logging messages to thesyslogfacility. Thesyslogdaemon must be running on the host machine. |
| journald | Writes log messages tojournald. Thejournalddaemon must be running on the host machine. |
| gelf | Writes log messages to a Graylog Extended Log Format (GELF) endpoint such as Graylog or Logstash. |
| fluentd | Writes log messages tofluentd(forward input). Thefluentddaemon must be running on the host machine. |
| awslogs | Writes log messages to Amazon CloudWatch Logs. |
| splunk | Writes log messages tosplunkusing the HTTP Event Collector. |
| etwlogs | Writes log messages as Event Tracing for Windows (ETW) events. Only available on Windows platforms. |
| gcplogs | Writes log messages to Google Cloud Platform (GCP) Logging. |

## Limitations of logging drivers

- Reading log information requires decompressing rotated log files, which causes
  a temporary increase in disk usage (until the log entries from the rotated
  files are read) and an increased CPU usage while decompressing.
- The capacity of the host storage where the Docker data directory resides
  determines the maximum size of the log file information.

---

# Amazon CloudWatch Logs logging driver

> Learn how to use the Amazon CloudWatch Logs logging driver with Docker Engine

# Amazon CloudWatch Logs logging driver

   Table of contents

---

The `awslogs` logging driver sends container logs to
[Amazon CloudWatch Logs](https://aws.amazon.com/cloudwatch/details/#log-monitoring).
Log entries can be retrieved through the [AWS Management
Console](https://console.aws.amazon.com/cloudwatch/home#logs:) or the [AWS SDKs
and Command Line Tools](https://docs.aws.amazon.com/cli/latest/reference/logs/index.html).

## Usage

To use the `awslogs` driver as the default logging driver, set the `log-driver`
and `log-opt` keys to appropriate values in the `daemon.json` file, which is
located in `/etc/docker/` on Linux hosts or
`C:\ProgramData\docker\config\daemon.json` on Windows Server. For more about
configuring Docker using `daemon.json`, see
[daemon.json](https://docs.docker.com/reference/cli/dockerd/#daemon-configuration-file).
The following example sets the log driver to `awslogs` and sets the
`awslogs-region` option.

```json
{
  "log-driver": "awslogs",
  "log-opts": {
    "awslogs-region": "us-east-1"
  }
}
```

Restart Docker for the changes to take effect.

You can set the logging driver for a specific container by using the
`--log-driver` option to `docker run`:

```console
$ docker run --log-driver=awslogs ...
```

If you are using Docker Compose, set `awslogs` using the following declaration example:

```yaml
myservice:
  logging:
    driver: awslogs
    options:
      awslogs-region: us-east-1
```

## Amazon CloudWatch Logs options

You can add logging options to the `daemon.json` to set Docker-wide defaults,
or use the `--log-opt NAME=VALUE` flag to specify Amazon CloudWatch Logs
logging driver options when starting a container.

### awslogs-region

The `awslogs` logging driver sends your Docker logs to a specific region. Use
the `awslogs-region` log option or the `AWS_REGION` environment variable to set
the region. By default, if your Docker daemon is running on an EC2 instance
and no region is set, the driver uses the instance's region.

```console
$ docker run --log-driver=awslogs --log-opt awslogs-region=us-east-1 ...
```

### awslogs-endpoint

By default, Docker uses either the `awslogs-region` log option or the
detected region to construct the remote CloudWatch Logs API endpoint.
Use the `awslogs-endpoint` log option to override the default endpoint
with the provided endpoint.

> Note
>
> The `awslogs-region` log option or detected region controls the
> region used for signing. You may experience signature errors if the
> endpoint you've specified with `awslogs-endpoint` uses a different region.

### awslogs-group

You must specify a
[log group](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html)
for the `awslogs` logging driver. You can specify the log group with the
`awslogs-group` log option:

```console
$ docker run --log-driver=awslogs --log-opt awslogs-region=us-east-1 --log-opt awslogs-group=myLogGroup ...
```

### awslogs-stream

To configure which
[log stream](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html)
should be used, you can specify the `awslogs-stream` log option. If not
specified, the container ID is used as the log stream.

> Note
>
> Log streams within a given log group should only be used by one container
> at a time. Using the same log stream for multiple containers concurrently
> can cause reduced logging performance.

### awslogs-create-group

Log driver returns an error by default if the log group doesn't exist. However, you can set the
`awslogs-create-group` to `true` to automatically create the log group as needed.
The `awslogs-create-group` option defaults to `false`.

```console
$ docker run \
    --log-driver=awslogs \
    --log-opt awslogs-region=us-east-1 \
    --log-opt awslogs-group=myLogGroup \
    --log-opt awslogs-create-group=true \
    ...
```

> Note
>
> Your AWS IAM policy must include the `logs:CreateLogGroup` permission before
> you attempt to use `awslogs-create-group`.

### awslogs-create-stream

By default, the log driver creates the AWS CloudWatch Logs stream used for container log persistence.

Set `awslogs-create-stream` to `false` to disable log stream creation. When disabled, the Docker daemon assumes
the log stream already exists. A use case where this is beneficial is when log stream creation is handled by
another process avoiding redundant AWS CloudWatch Logs API calls.

If `awslogs-create-stream` is set to `false` and the log stream does not exist, log persistence to CloudWatch
fails during container runtime, resulting in `Failed to put log events` error messages in daemon logs.

```console
$ docker run \
    --log-driver=awslogs \
    --log-opt awslogs-region=us-east-1 \
    --log-opt awslogs-group=myLogGroup \
    --log-opt awslogs-stream=myLogStream \
    --log-opt awslogs-create-stream=false \
    ...
```

### awslogs-datetime-format

The `awslogs-datetime-format` option defines a multi-line start pattern in [Pythonstrftimeformat](https://strftime.org). A log message consists of a line that
matches the pattern and any following lines that don't match the pattern. Thus
the matched line is the delimiter between log messages.

One example of a use case for using
this format is for parsing output such as a stack dump, which might otherwise
be logged in multiple entries. The correct pattern allows it to be captured in a
single entry.

This option always takes precedence if both `awslogs-datetime-format` and
`awslogs-multiline-pattern` are configured.

> Note
>
> Multi-line logging performs regular expression parsing and matching of all log
> messages, which may have a negative impact on logging performance.

Consider the following log stream, where new log messages start with a
timestamp:

```console
[May 01, 2017 19:00:01] A message was logged
[May 01, 2017 19:00:04] Another multi-line message was logged
Some random message
with some random words
[May 01, 2017 19:01:32] Another message was logged
```

The format can be expressed as a `strftime` expression of
`[%b %d, %Y %H:%M:%S]`, and the `awslogs-datetime-format` value can be set to
that expression:

```console
$ docker run \
    --log-driver=awslogs \
    --log-opt awslogs-region=us-east-1 \
    --log-opt awslogs-group=myLogGroup \
    --log-opt awslogs-datetime-format='\[%b %d, %Y %H:%M:%S\]' \
    ...
```

This parses the logs into the following CloudWatch log events:

```console
# First event
[May 01, 2017 19:00:01] A message was logged

# Second event
[May 01, 2017 19:00:04] Another multi-line message was logged
Some random message
with some random words

# Third event
[May 01, 2017 19:01:32] Another message was logged
```

The following `strftime` codes are supported:

| Code | Meaning | Example |
| --- | --- | --- |
| %a | Weekday abbreviated name. | Mon |
| %A | Weekday full name. | Monday |
| %w | Weekday as a decimal number where 0 is Sunday and 6 is Saturday. | 0 |
| %d | Day of the month as a zero-padded decimal number. | 08 |
| %b | Month abbreviated name. | Feb |
| %B | Month full name. | February |
| %m | Month as a zero-padded decimal number. | 02 |
| %Y | Year with century as a decimal number. | 2008 |
| %y | Year without century as a zero-padded decimal number. | 08 |
| %H | Hour (24-hour clock) as a zero-padded decimal number. | 19 |
| %I | Hour (12-hour clock) as a zero-padded decimal number. | 07 |
| %p | AM or PM. | AM |
| %M | Minute as a zero-padded decimal number. | 57 |
| %S | Second as a zero-padded decimal number. | 04 |
| %L | Milliseconds as a zero-padded decimal number. | .123 |
| %f | Microseconds as a zero-padded decimal number. | 000345 |
| %z | UTC offset in the form +HHMM or -HHMM. | +1300 |
| %Z | Time zone name. | PST |
| %j | Day of the year as a zero-padded decimal number. | 363 |

### awslogs-multiline-pattern

The `awslogs-multiline-pattern` option defines a multi-line start pattern using a
regular expression. A log message consists of a line that matches the pattern
and any following lines that don't match the pattern. Thus the matched line is
the delimiter between log messages.

This option is ignored if `awslogs-datetime-format` is also configured.

> Note
>
> Multi-line logging performs regular expression parsing and matching of all log
> messages. This may have a negative impact on logging performance.

Consider the following log stream, where each log message should start with the
pattern `INFO`:

```console
INFO A message was logged
INFO Another multi-line message was logged
     Some random message
INFO Another message was logged
```

You can use the regular expression of `^INFO`:

```console
$ docker run \
    --log-driver=awslogs \
    --log-opt awslogs-region=us-east-1 \
    --log-opt awslogs-group=myLogGroup \
    --log-opt awslogs-multiline-pattern='^INFO' \
    ...
```

This parses the logs into the following CloudWatch log events:

```console
# First event
INFO A message was logged

# Second event
INFO Another multi-line message was logged
     Some random message

# Third event
INFO Another message was logged
```

### tag

Specify `tag` as an alternative to the `awslogs-stream` option. `tag` interprets
Go template markup, such as `{{.ID}}`, `{{.FullID}}`
or `{{.Name}}` `docker.{{.ID}}`. See
the [tag option documentation](https://docs.docker.com/engine/logging/log_tags/) for details on supported template
substitutions.

When both `awslogs-stream` and `tag` are specified, the value supplied for
`awslogs-stream` overrides the template specified with `tag`.

If not specified, the container ID is used as the log stream.

> Note
>
> The CloudWatch log API doesn't support `:` in the log name. This can cause
> some issues when using the `{{ .ImageName }}` as a tag,
> since a Docker image has a format of `IMAGE:TAG`, such as `alpine:latest`.
> Template markup can be used to get the proper format. To get the image name
> and the first 12 characters of the container ID, you can use:
>
>
>
> ```bash
> --log-opt tag='{{ with split .ImageName ":" }}{{join . "_"}}{{end}}-{{.ID}}'
> ```
>
>
>
> the output is something like: `alpine_latest-bf0072049c76`

### awslogs-force-flush-interval-seconds

The `awslogs` driver periodically flushes logs to CloudWatch.

The `awslogs-force-flush-interval-seconds` option changes log flush interval seconds.

Default is 5 seconds.

### awslogs-max-buffered-events

The `awslogs` driver buffers logs.

The `awslogs-max-buffered-events` option changes log buffer size.

Default is 4K.

## Credentials

You must provide AWS credentials to the Docker daemon to use the `awslogs`
logging driver. You can provide these credentials with the `AWS_ACCESS_KEY_ID`,
`AWS_SECRET_ACCESS_KEY`, and `AWS_SESSION_TOKEN` environment variables, the
default AWS shared credentials file (`~/.aws/credentials` of the root user), or
if you are running the Docker daemon on an Amazon EC2 instance, the Amazon EC2
instance profile.

Credentials must have a policy applied that allows the `logs:CreateLogStream`
and `logs:PutLogEvents` actions, as shown in the following example.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": ["logs:CreateLogStream", "logs:PutLogEvents"],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
```

---

# ETW logging driver

> Learn how to use the Event Tracing for Windows (ETW) logging driver with Docker Engine

# ETW logging driver

   Table of contents

---

The Event Tracing for Windows (ETW) logging driver forwards container logs as ETW events.
ETW stands for Event Tracing in Windows, and is the common framework
for tracing applications in Windows. Each ETW event contains a message
with both the log and its context information. A client can then create
an ETW listener to listen to these events.

The ETW provider that this logging driver registers with Windows, has the
GUID identifier of: `{a3693192-9ed6-46d2-a981-f8226c8363bd}`. A client creates an
ETW listener and registers to listen to events from the logging driver's provider.
It doesn't matter the order in which the provider and listener are created.
A client can create their ETW listener and start listening for events from the provider,
before the provider has been registered with the system.

## Usage

Here is an example of how to listen to these events using the logman utility program
included in most installations of Windows:

1. `logman start -ets DockerContainerLogs -p "{a3693192-9ed6-46d2-a981-f8226c8363bd}" 0x0 -o trace.etl`
2. Run your container(s) with the etwlogs driver, by adding
  `--log-driver=etwlogs` to the Docker run command, and generate log messages.
3. `logman stop -ets DockerContainerLogs`
4. This generates an etl file that contains the events. One way to convert this
  file into human-readable form is to run: `tracerpt -y trace.etl`.

Each ETW event contains a structured message string in this format:

```text
container_name: %s, image_name: %s, container_id: %s, image_id: %s, source: [stdout | stderr], log: %s
```

Details on each item in the message can be found below:

| Field | Description |
| --- | --- |
| container_name | The container name at the time it was started. |
| image_name | The name of the container's image. |
| container_id | The full 64-character container ID. |
| image_id | The full ID of the container's image. |
| source | stdoutorstderr. |
| log | The container log message. |

Here is an example event message (output formatted for readability):

```yaml
container_name: backstabbing_spence,
image_name: windowsservercore,
container_id: f14bb55aa862d7596b03a33251c1be7dbbec8056bbdead1da8ec5ecebbe29731,
image_id: sha256:2f9e19bd998d3565b4f345ac9aaf6e3fc555406239a4fb1b1ba879673713824b,
source: stdout,
log: Hello world!
```

A client can parse this message string to get both the log message, as well as its
context information. The timestamp is also available within the ETW event.

> Note
>
> This ETW provider only emits a message string, and not a specially structured
> ETW event. Therefore, you don't have to register a manifest file with the
> system to read and interpret its ETW events.

---

# Fluentd logging driver

> Learn how to use the fluentd logging driver

# Fluentd logging driver

   Table of contents

---

The `fluentd` logging driver sends container logs to the
[Fluentd](https://www.fluentd.org) collector as structured log data. Then, users
can use any of the [various output plugins of
Fluentd](https://www.fluentd.org/plugins) to write these logs to various
destinations.

In addition to the log message itself, the `fluentd` log
driver sends the following metadata in the structured log message:

| Field | Description |
| --- | --- |
| container_id | The full 64-character container ID. |
| container_name | The container name at the time it was started. If you usedocker renameto rename a container, the new name isn't reflected in the journal entries. |
| source | stdoutorstderr |
| log | The container log |

## Usage

Some options are supported by specifying `--log-opt` as many times as needed:

- `fluentd-address`: specify a socket address to connect to the Fluentd daemon, ex `fluentdhost:24224` or `unix:///path/to/fluentd.sock`.
- `tag`: specify a tag for Fluentd messages. Supports some Go template markup, ex `{{.ID}}`, `{{.FullID}}` or `{{.Name}}` `docker.{{.ID}}`.

To use the `fluentd` driver as the default logging driver, set the `log-driver`
and `log-opt` keys to appropriate values in the `daemon.json` file, which is
located in `/etc/docker/` on Linux hosts or
`C:\ProgramData\docker\config\daemon.json` on Windows Server. For more about
configuring Docker using `daemon.json`, see
[daemon.json](https://docs.docker.com/reference/cli/dockerd/#daemon-configuration-file).

The following example sets the log driver to `fluentd` and sets the
`fluentd-address` option.

```json
{
  "log-driver": "fluentd",
  "log-opts": {
    "fluentd-address": "fluentdhost:24224"
  }
}
```

Restart Docker for the changes to take effect.

> Note
>
> `log-opts` configuration options in the `daemon.json` configuration file must
> be provided as strings. Boolean and numeric values (such as the value for
> `fluentd-async` or `fluentd-max-retries`) must therefore be enclosed
> in quotes (`"`).

To set the logging driver for a specific container, pass the
`--log-driver` option to `docker run`:

```console
$ docker run --log-driver=fluentd ...
```

Before using this logging driver, launch a Fluentd daemon. The logging driver
connects to this daemon through `localhost:24224` by default. Use the
`fluentd-address` option to connect to a different address.

```console
$ docker run --log-driver=fluentd --log-opt fluentd-address=fluentdhost:24224
```

If container cannot connect to the Fluentd daemon, the container stops
immediately unless the `fluentd-async` option is used.

## Options

Users can use the `--log-opt NAME=VALUE` flag to specify additional Fluentd logging driver options.

### fluentd-address

By default, the logging driver connects to `localhost:24224`. Supply the
`fluentd-address` option to connect to a different address. `tcp`(default) and `unix` sockets are supported.

```console
$ docker run --log-driver=fluentd --log-opt fluentd-address=fluentdhost:24224
$ docker run --log-driver=fluentd --log-opt fluentd-address=tcp://fluentdhost:24224
$ docker run --log-driver=fluentd --log-opt fluentd-address=unix:///path/to/fluentd.sock
```

Two of the above specify the same address, because `tcp` is default.

### tag

By default, Docker uses the first 12 characters of the container ID to tag log messages.
Refer to the [log tag option documentation](https://docs.docker.com/engine/logging/log_tags/) for customizing
the log tag format.

### labels, labels-regex, env, and env-regex

The `labels` and `env` options each take a comma-separated list of keys. If
there is collision between `label` and `env` keys, the value of the `env` takes
precedence. Both options add additional fields to the extra attributes of a
logging message.

The `env-regex` and `labels-regex` options are similar to and compatible with
respectively `env` and `labels`. Their values are regular expressions to match
logging-related environment variables and labels. It is used for advanced
[log tag options](https://docs.docker.com/engine/logging/log_tags/).

### fluentd-async

Docker connects to Fluentd in the background. Messages are buffered until the
connection is established. Defaults to `false`.

### fluentd-async-reconnect-interval

When `fluentd-async` is enabled, the `fluentd-async-reconnect-interval` option
defines the interval, in milliseconds, at which the connection to
`fluentd-address` is re-established. This option is useful if the address
resolves to one or more IP addresses, for example a Consul service address.

### fluentd-buffer-limit

Sets the number of events buffered on the memory. Records will be stored in memory
up to this number. If the buffer is full, the call to record logs will fail.
The default is 1048576.
([https://github.com/fluent/fluent-logger-golang/tree/master#bufferlimit](https://github.com/fluent/fluent-logger-golang/tree/master#bufferlimit))

### fluentd-retry-wait

How long to wait between retries. Defaults to 1 second.

### fluentd-max-retries

The maximum number of retries. Defaults to `4294967295` (2**32 - 1).

### fluentd-sub-second-precision

Generates event logs in nanosecond resolution. Defaults to `false`.

### fluentd-write-timeout

Sets the timeout for the write call to the `fluentd` daemon. By default,
writes have no timeout and will block indefinitely.

## Fluentd daemon management with Docker

About `Fluentd` itself, see [the project webpage](https://www.fluentd.org)
and [its documents](https://docs.fluentd.org).

To use this logging driver, start the `fluentd` daemon on a host. We recommend
that you use [the Fluentd docker
image](https://hub.docker.com/r/fluent/fluentd/). This image is
especially useful if you want to aggregate multiple container logs on each
host then, later, transfer the logs to another Fluentd node to create an
aggregate store.

### Test container loggers

1. Write a configuration file (`test.conf`) to dump input logs:
  ```text
  <source>
    @type forward
  </source>
  <match *>
    @type stdout
  </match>
  ```
2. Launch Fluentd container with this configuration file:
  ```console
  $ docker run -it -p 24224:24224 -v /path/to/conf/test.conf:/fluentd/etc/test.conf -e FLUENTD_CONF=test.conf fluent/fluentd:latest
  ```
3. Start one or more containers with the `fluentd` logging driver:
  ```console
  $ docker run --log-driver=fluentd your/application
  ```

---

# Google Cloud Logging driver

> Learn how to use the Google Cloud Logging driver with Docker Engine

# Google Cloud Logging driver

   Table of contents

---

The Google Cloud Logging driver sends container logs to
[Google Cloud Logging](https://cloud.google.com/logging/docs/)
Logging.

## Usage

To use the `gcplogs` driver as the default logging driver, set the `log-driver`
and `log-opt` keys to appropriate values in the `daemon.json` file, which is
located in `/etc/docker/` on Linux hosts or
`C:\ProgramData\docker\config\daemon.json` on Windows Server. For more about
configuring Docker using `daemon.json`, see
[daemon.json](https://docs.docker.com/reference/cli/dockerd/#daemon-configuration-file).

The following example sets the log driver to `gcplogs` and sets the
`gcp-meta-name` option.

```json
{
  "log-driver": "gcplogs",
  "log-opts": {
    "gcp-meta-name": "example-instance-12345"
  }
}
```

Restart Docker for the changes to take effect.

You can set the logging driver for a specific container by using the
`--log-driver` option to `docker run`:

```console
$ docker run --log-driver=gcplogs ...
```

If Docker detects that it's running in a Google Cloud Project, it discovers
configuration from the
[instance metadata service](https://cloud.google.com/compute/docs/metadata).
Otherwise, the user must specify
which project to log to using the `--gcp-project` log option and Docker
attempts to obtain credentials from the
[Google Application Default Credential](https://developers.google.com/identity/protocols/application-default-credentials).
The `--gcp-project` flag takes precedence over information discovered from the
metadata server, so a Docker daemon running in a Google Cloud project can be
overridden to log to a different project using `--gcp-project`.

Docker fetches the values for zone, instance name and instance ID from Google
Cloud metadata server. Those values can be provided via options if metadata
server isn't available. They don't override the values from metadata server.

## gcplogs options

You can use the `--log-opt NAME=VALUE` flag to specify these additional Google
Cloud Logging driver options:

| Option | Required | Description |
| --- | --- | --- |
| gcp-project | optional | Which Google Cloud project to log to. Defaults to discovering this value from the Google Cloud metadata server. |
| gcp-log-cmd | optional | Whether to log the command that the container was started with. Defaults to false. |
| labels | optional | Comma-separated list of keys of labels, which should be included in message, if these labels are specified for the container. |
| labels-regex | optional | Similar to and compatible withlabels. A regular expression to match logging-related labels. Used for advancedlog tag options. |
| env | optional | Comma-separated list of keys of environment variables, which should be included in message, if these variables are specified for the container. |
| env-regex | optional | Similar to and compatible withenv. A regular expression to match logging-related environment variables. Used for advancedlog tag options. |
| gcp-meta-zone | optional | Zone name for the instance. |
| gcp-meta-name | optional | Instance name. |
| gcp-meta-id | optional | Instance ID. |

If there is collision between `label` and `env` keys, the value of the `env`
takes precedence. Both options add additional fields to the attributes of a
logging message.

The following is an example of the logging options required to log to the default
logging destination which is discovered by querying the Google Cloud metadata server.

```console
$ docker run \
    --log-driver=gcplogs \
    --log-opt labels=location \
    --log-opt env=TEST \
    --log-opt gcp-log-cmd=true \
    --env "TEST=false" \
    --label location=west \
    your/application
```

This configuration also directs the driver to include in the payload the label
`location`, the environment variable `ENV`, and the command used to start the
container.

The following example shows logging options for running outside of Google
Cloud. The `GOOGLE_APPLICATION_CREDENTIALS` environment variable must be set
for the daemon, for example via systemd:

```ini
[Service]
Environment="GOOGLE_APPLICATION_CREDENTIALS=uQWVCPkMTI34bpssr1HI"
```

```console
$ docker run \
    --log-driver=gcplogs \
    --log-opt gcp-project=test-project \
    --log-opt gcp-meta-zone=west1 \
    --log-opt gcp-meta-name=`hostname` \
    your/application
```
