# Graylog Extended Format logging driver and more

# Graylog Extended Format logging driver

> Learn how to use the Graylog Extended Format logging driver with Docker Engine

# Graylog Extended Format logging driver

   Table of contents

---

The `gelf` logging driver is a convenient format that's understood by a number of tools such as
[Graylog](https://www.graylog.org/), [Logstash](https://www.elastic.co/products/logstash), and
[Fluentd](https://www.fluentd.org). Many tools use this format.

In GELF, every log message is a dict with the following fields:

- Version
- Host (who sent the message in the first place)
- Timestamp
- Short and long version of the message
- Any custom fields you configure yourself

## Usage

To use the `gelf` driver as the default logging driver, set the `log-driver` and
`log-opt` keys to appropriate values in the `daemon.json` file, which is located
in `/etc/docker/` on Linux hosts or `C:\ProgramData\docker\config\daemon.json`
on Windows Server. For more about configuring Docker using `daemon.json`, see
[daemon.json](https://docs.docker.com/reference/cli/dockerd/#daemon-configuration-file).

The following example sets the log driver to `gelf` and sets the `gelf-address`
option.

```json
{
  "log-driver": "gelf",
  "log-opts": {
    "gelf-address": "udp://1.2.3.4:12201"
  }
}
```

Restart Docker for the changes to take effect.

> Note
>
> `log-opts` configuration options in the `daemon.json` configuration file must
> be provided as strings. Boolean and numeric values (such as the value for
> `gelf-tcp-max-reconnect`) must therefore be enclosed in quotes (`"`).

You can set the logging driver for a specific container by setting the
`--log-driver` flag when using `docker container create` or `docker run`:

```console
$ docker run \
      --log-driver gelf --log-opt gelf-address=udp://1.2.3.4:12201 \
      alpine echo hello world
```

### GELF options

The `gelf` logging driver supports the following options:

| Option | Required | Description | Example value |
| --- | --- | --- | --- |
| gelf-address | required | The address of the GELF server.tcpandudpare the only supported URI specifier and you must specify the port. | --log-opt gelf-address=udp://192.168.0.42:12201 |
| gelf-compression-type | optional | UDP OnlyThe type of compression the GELF driver uses to compress each log message. Allowed values aregzip,zlibandnone. The default isgzip. Note that enabled compression leads to excessive CPU usage, so it's highly recommended to set this tonone. | --log-opt gelf-compression-type=gzip |
| gelf-compression-level | optional | UDP OnlyThe level of compression whengziporzlibis thegelf-compression-type. An integer in the range of-1to9(BestCompression). Default value is 1 (BestSpeed). Higher levels provide more compression at lower speed. Either-1or0disables compression. | --log-opt gelf-compression-level=2 |
| gelf-tcp-max-reconnect | optional | TCP OnlyThe maximum number of reconnection attempts when the connection drop. A positive integer. Default value is 3. | --log-opt gelf-tcp-max-reconnect=3 |
| gelf-tcp-reconnect-delay | optional | TCP OnlyThe number of seconds to wait between reconnection attempts. A positive integer. Default value is 1. | --log-opt gelf-tcp-reconnect-delay=1 |
| tag | optional | A string that's appended to theAPP-NAMEin thegelfmessage. By default, Docker uses the first 12 characters of the container ID to tag log messages. Refer to thelog tag option documentationfor customizing the log tag format. | --log-opt tag=mailer |
| labels | optional | Applies when starting the Docker daemon. A comma-separated list of logging-related labels this daemon accepts. Adds additional key on theextrafields, prefixed by an underscore (_). Used for advancedlog tag options. | --log-opt labels=production_status,geo |
| labels-regex | optional | Similar to and compatible withlabels. A regular expression to match logging-related labels. Used for advancedlog tag options. | --log-opt labels-regex=^(production_status|geo) |
| env | optional | Applies when starting the Docker daemon. A comma-separated list of logging-related environment variables this daemon accepts. Adds additional key on theextrafields, prefixed by an underscore (_). Used for advancedlog tag options. | --log-opt env=os,customer |
| env-regex | optional | Similar to and compatible withenv. A regular expression to match logging-related environment variables. Used for advancedlog tag options. | --log-opt env-regex=^(os|customer) |

> Note
>
> The `gelf` driver doesn't support TLS for TCP connections. Messages sent to TLS-protected inputs can silently fail.

### Examples

This example configures the container to use the GELF server running at
`192.168.0.42` on port `12201`.

```console
$ docker run -dit \
    --log-driver=gelf \
    --log-opt gelf-address=udp://192.168.0.42:12201 \
    alpine sh
```

---

# Journald logging driver

> Learn how to use the Journald logging driver with Docker Engine

# Journald logging driver

   Table of contents

---

The `journald` logging driver sends container logs to the
[systemdjournal](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html).
Log entries can be retrieved using the `journalctl` command, through use of the
`journal` API, or using the `docker logs` command.

In addition to the text of the log message itself, the `journald` log driver
stores the following metadata in the journal with each message:

| Field | Description |
| --- | --- |
| CONTAINER_ID | The container ID truncated to 12 characters. |
| CONTAINER_ID_FULL | The full 64-character container ID. |
| CONTAINER_NAME | The container name at the time it was started. If you usedocker renameto rename a container, the new name isn't reflected in the journal entries. |
| CONTAINER_TAG,SYSLOG_IDENTIFIER | The container tag (log tag option documentation). |
| CONTAINER_PARTIAL_MESSAGE | A field that flags log integrity. Improve logging of long log lines. |
| IMAGE_NAME | The name of the container image. |

## Usage

To use the `journald` driver as the default logging driver, set the `log-driver`
and `log-opts` keys to appropriate values in the `daemon.json` file, which is
located in `/etc/docker/` on Linux hosts or
`C:\ProgramData\docker\config\daemon.json` on Windows Server. For more about
configuring Docker using `daemon.json`, see
[daemon.json](https://docs.docker.com/reference/cli/dockerd/#daemon-configuration-file).

The following example sets the log driver to `journald`:

```json
{
  "log-driver": "journald"
}
```

Restart Docker for the changes to take effect.

To configure the logging driver for a specific container, use the `--log-driver`
flag on the `docker run` command.

```console
$ docker run --log-driver=journald ...
```

## Options

Use the `--log-opt NAME=VALUE` flag to specify additional `journald` logging
driver options.

| Option | Required | Description |
| --- | --- | --- |
| tag | optional | Specify template to setCONTAINER_TAGandSYSLOG_IDENTIFIERvalue in journald logs. Refer tolog tag option documentationto customize the log tag format. |
| labels | optional | Comma-separated list of keys of labels, which should be included in message, if these labels are specified for the container. |
| labels-regex | optional | Similar to and compatible with labels. A regular expression to match logging-related labels. Used for advancedlog tag options. |
| env | optional | Comma-separated list of keys of environment variables, which should be included in message, if these variables are specified for the container. |
| env-regex | optional | Similar to and compatible withenv. A regular expression to match logging-related environment variables. Used for advancedlog tag options. |

If a collision occurs between `label` and `env` options, the value of the `env`
takes precedence. Each option adds additional fields to the attributes of a
logging message.

The following is an example of the logging options required to log to journald.

```console
$ docker run \
    --log-driver=journald \
    --log-opt labels=location \
    --log-opt env=TEST \
    --env "TEST=false" \
    --label location=west \
    your/application
```

This configuration also directs the driver to include in the payload the label
location, and the environment variable `TEST`. If the `--env "TEST=false"`
or `--label location=west` arguments were omitted, the corresponding key would
not be set in the journald log.

## Note regarding container names

The value logged in the `CONTAINER_NAME` field is the name of the container that
was set at startup. If you use `docker rename` to rename a container, the new
name isn't reflected in the journal entries. Journal entries continue
to use the original name.

## Retrieve log messages withjournalctl

Use the `journalctl` command to retrieve log messages. You can apply filter
expressions to limit the retrieved messages to those associated with a specific
container:

```console
$ sudo journalctl CONTAINER_NAME=webserver
```

You can use additional filters to further limit the messages retrieved. The `-b`
flag only retrieves messages generated since the last system boot:

```console
$ sudo journalctl -b CONTAINER_NAME=webserver
```

The `-o` flag specifies the format for the retrieved log messages. Use `-o json`
to return the log messages in JSON format.

```console
$ sudo journalctl -o json CONTAINER_NAME=webserver
```

### View logs for a container with a TTY enabled

If TTY is enabled on a container you may see `[10B blob data]` in the output
when retrieving log messages.
The reason for that is that `\r` is appended to the end of the line and
`journalctl` doesn't strip it automatically unless `--all` is set:

```console
$ sudo journalctl -b CONTAINER_NAME=webserver --all
```

## Retrieve log messages with thejournalAPI

This example uses the `systemd` Python module to retrieve container
logs:

```python
import systemd.journal

reader = systemd.journal.Reader()
reader.add_match('CONTAINER_NAME=web')

for msg in reader:
    print '{CONTAINER_ID_FULL}: {MESSAGE}'.format(**msg)
```

---

# JSON File logging driver

> Learn how to use the json-file logging driver with Docker Engine

# JSON File logging driver

   Table of contents

---

By default, Docker captures the standard output (and standard error) of all your containers,
and writes them in files using the JSON format. The JSON format annotates each line with its
origin (`stdout` or `stderr`) and its timestamp. Each log file contains information about
only one container.

```json
{
  "log": "Log line is here\n",
  "stream": "stdout",
  "time": "2019-01-01T11:11:11.111111111Z"
}
```

> Warning
>
> The `json-file` logging driver uses file-based storage. These files are designed
> to be exclusively accessed by the Docker daemon. Interacting with these files
> with external tools may interfere with Docker's logging system and result in
> unexpected behavior, and should be avoided.

## Usage

To use the `json-file` driver as the default logging driver, set the `log-driver`
and `log-opts` keys to appropriate values in the `daemon.json` file, which is
located in `/etc/docker/` on Linux hosts or
`C:\ProgramData\docker\config\` on Windows Server. If the file does not exist, create it first. For more information about
configuring Docker using `daemon.json`, see
[daemon.json](https://docs.docker.com/reference/cli/dockerd/#daemon-configuration-file).

The following example sets the log driver to `json-file` and sets the `max-size`
and `max-file` options to enable automatic log-rotation.

```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

> Note
>
> `log-opts` configuration options in the `daemon.json` configuration file must
> be provided as strings. Boolean and numeric values (such as the value for
> `max-file` in the example above) must therefore be enclosed in quotes (`"`).

Restart Docker for the changes to take effect for newly created containers.
Existing containers don't use the new logging configuration automatically.

You can set the logging driver for a specific container by using the
`--log-driver` flag to `docker container create` or `docker run`:

```console
$ docker run \
      --log-driver json-file --log-opt max-size=10m \
      alpine echo hello world
```

### Options

The `json-file` logging driver supports the following logging options:

| Option | Description | Example value |
| --- | --- | --- |
| max-size | The maximum size of the log before it is rolled. A positive integer plus a modifier representing the unit of measure (k,m, org). Defaults to -1 (unlimited). | --log-opt max-size=10m |
| max-file | The maximum number of log files that can be present. If rolling the logs creates excess files, the oldest file is removed.Only effective whenmax-sizeis also set.A positive integer. Defaults to 1. | --log-opt max-file=3 |
| labels | Applies when starting the Docker daemon. A comma-separated list of logging-related labels this daemon accepts. Used for advancedlog tag options. | --log-opt labels=production_status,geo |
| labels-regex | Similar to and compatible withlabels. A regular expression to match logging-related labels. Used for advancedlog tag options. | --log-opt labels-regex=^(production_status|geo) |
| env | Applies when starting the Docker daemon. A comma-separated list of logging-related environment variables this daemon accepts. Used for advancedlog tag options. | --log-opt env=os,customer |
| env-regex | Similar to and compatible withenv. A regular expression to match logging-related environment variables. Used for advancedlog tag options. | --log-opt env-regex=^(os|customer) |
| compress | Toggles compression for rotated logs. Default isdisabled. | --log-opt compress=true |

### Examples

This example starts an `alpine` container which can have a maximum of 3 log
files no larger than 10 megabytes each.

```console
$ docker run -it --log-opt max-size=10m --log-opt max-file=3 alpine ash
```

---

# Local file logging driver

> Learn how to use the local logging driver with Docker Engine

# Local file logging driver

   Table of contents

---

The `local` logging driver captures output from container's stdout/stderr and
writes them to an internal storage that's optimized for performance and disk
use.

By default, the `local` driver preserves 100MB of log messages per container and
uses automatic compression to reduce the size on disk. The 100MB default value is based on a 20M default size
for each file and a default count of 5 for the number of such files (to account for log rotation).

> Warning
>
> The `local` logging driver uses file-based storage. These files are designed
> to be exclusively accessed by the Docker daemon. Interacting with these files
> with external tools may interfere with Docker's logging system and result in
> unexpected behavior, and should be avoided.

## Usage

To use the `local` driver as the default logging driver, set the `log-driver`
and `log-opt` keys to appropriate values in the `daemon.json` file, which is
located in `/etc/docker/` on Linux hosts or
`C:\ProgramData\docker\config\daemon.json` on Windows Server. For more about
configuring Docker using `daemon.json`, see
[daemon.json](https://docs.docker.com/reference/cli/dockerd/#daemon-configuration-file).

The following example sets the log driver to `local` and sets the `max-size`
option.

```json
{
  "log-driver": "local",
  "log-opts": {
    "max-size": "10m"
  }
}
```

Restart Docker for the changes to take effect for newly created containers.
Existing containers don't use the new logging configuration automatically.

You can set the logging driver for a specific container by using the
`--log-driver` flag to `docker container create` or `docker run`:

```console
$ docker run \
      --log-driver local --log-opt max-size=10m \
      alpine echo hello world
```

Note that `local` is a bash reserved keyword, so you may need to quote it in scripts.

### Options

The `local` logging driver supports the following logging options:

| Option | Description | Example value |
| --- | --- | --- |
| max-size | The maximum size of the log before it's rolled. A positive integer plus a modifier representing the unit of measure (k,m, org). Defaults to 20m. | --log-opt max-size=10m |
| max-file | The maximum number of log files that can be present. If rolling the logs creates excess files, the oldest file is removed. A positive integer. Defaults to 5. | --log-opt max-file=3 |
| compress | Toggle compression of rotated log files. Enabled by default. | --log-opt compress=false |

### Examples

This example starts an `alpine` container which can have a maximum of 3 log
files no larger than 10 megabytes each.

```console
$ docker run -it --log-driver local --log-opt max-size=10m --log-opt max-file=3 alpine ash
```

---

# Splunk logging driver

> Learn how to use the Splunk logging driver with Docker Engine

# Splunk logging driver

   Table of contents

---

The `splunk` logging driver sends container logs to
[HTTP Event Collector](https://dev.splunk.com/enterprise/docs/devtools/httpeventcollector/)
in Splunk Enterprise and Splunk Cloud.

## Usage

You can configure Docker logging to use the `splunk` driver by default or on a
per-container basis.

To use the `splunk` driver as the default logging driver, set the keys
`log-driver` and `log-opts` to appropriate values in the `daemon.json`
configuration file and restart Docker. For example:

```json
{
  "log-driver": "splunk",
  "log-opts": {
    "splunk-token": "",
    "splunk-url": "",
    ...
  }
}
```

The daemon.json file is located in `/etc/docker/` on Linux hosts or
`C:\ProgramData\docker\config\daemon.json` on Windows Server. For more about
configuring Docker using `daemon.json`, see
[daemon.json](https://docs.docker.com/reference/cli/dockerd/#daemon-configuration-file).

> Note
>
> `log-opts` configuration options in the `daemon.json` configuration file must
> be provided as strings. Boolean and numeric values (such as the value for
> `splunk-gzip` or `splunk-gzip-level`) must therefore be enclosed in quotes
> (`"`).

To use the `splunk` driver for a specific container, use the commandline flags
`--log-driver` and `log-opt` with `docker run`:

```console
$ docker run --log-driver=splunk --log-opt splunk-token=VALUE --log-opt splunk-url=VALUE ...
```

## Splunk options

The following properties let you configure the Splunk logging driver.

- To configure the `splunk` driver across the Docker environment, edit
  `daemon.json` with the key, `"log-opts": {"NAME": "VALUE", ...}`.
- To configure the `splunk` driver for an individual container, use `docker run`
  with the flag, `--log-opt NAME=VALUE ...`.

| Option | Required | Description |
| --- | --- | --- |
| splunk-token | required | Splunk HTTP Event Collector token. |
| splunk-url | required | Path to your Splunk Enterprise, self-service Splunk Cloud instance, or Splunk Cloud managed cluster (including port and scheme used by HTTP Event Collector) in one of the following formats:https://your_splunk_instance:8088,https://input-prd-p-XXXXXXX.cloud.splunk.com:8088, orhttps://http-inputs-XXXXXXXX.splunkcloud.com. |
| splunk-source | optional | Event source. |
| splunk-sourcetype | optional | Event source type. |
| splunk-index | optional | Event index. |
| splunk-capath | optional | Path to root certificate. |
| splunk-caname | optional | Name to use for validating server certificate; by default the hostname of thesplunk-urlis used. |
| splunk-insecureskipverify | optional | Ignore server certificate validation. |
| splunk-format | optional | Message format. Can beinline,jsonorraw. Defaults toinline. |
| splunk-verify-connection | optional | Verify on start, that Docker can connect to Splunk server. Defaults to true. |
| splunk-gzip | optional | Enable/disable gzip compression to send events to Splunk Enterprise or Splunk Cloud instance. Defaults to false. |
| splunk-gzip-level | optional | Set compression level for gzip. Valid values are -1 (default), 0 (no compression), 1 (best speed) ... 9 (best compression). Defaults toDefaultCompression. |
| tag | optional | Specify tag for message, which interpret some markup. Default value is{{.ID}}(12 characters of the container ID). Refer to thelog tag option documentationfor customizing the log tag format. |
| labels | optional | Comma-separated list of keys of labels, which should be included in message, if these labels are specified for container. |
| labels-regex | optional | Similar to and compatible withlabels. A regular expression to match logging-related labels. Used for advancedlog tag options. |
| env | optional | Comma-separated list of keys of environment variables, which should be included in message, if these variables are specified for container. |
| env-regex | optional | Similar to and compatible withenv. A regular expression to match logging-related environment variables. Used for advancedlog tag options. |

If there is collision between the `label` and `env` keys, the value of the `env`
takes precedence. Both options add additional fields to the attributes of a
logging message.

Below is an example of the logging options specified for the Splunk Enterprise
instance. The instance is installed locally on the same machine on which the
Docker daemon is running.

The path to the root certificate and Common Name is specified using an HTTPS
scheme. This is used for verification. The `SplunkServerDefaultCert` is
automatically generated by Splunk certificates.

```console
$ docker run \
    --log-driver=splunk \
    --log-opt splunk-token=176FCEBF-4CF5-4EDF-91BC-703796522D20 \
    --log-opt splunk-url=https://splunkhost:8088 \
    --log-opt splunk-capath=/path/to/cert/cacert.pem \
    --log-opt splunk-caname=SplunkServerDefaultCert \
    --log-opt tag="{{.Name}}/{{.FullID}}" \
    --log-opt labels=location \
    --log-opt env=TEST \
    --env "TEST=false" \
    --label location=west \
    your/application
```

The `splunk-url` for Splunk instances hosted on Splunk Cloud is in a format
like `https://http-inputs-XXXXXXXX.splunkcloud.com` and does not include a
port specifier.

### Message formats

There are three logging driver messaging formats: `inline` (default), `json`,
and `raw`.

The default format is `inline` where each log message is embedded as a string.
For example:

```json
{
  "attrs": {
    "env1": "val1",
    "label1": "label1"
  },
  "tag": "MyImage/MyContainer",
  "source": "stdout",
  "line": "my message"
}
```

```json
{
  "attrs": {
    "env1": "val1",
    "label1": "label1"
  },
  "tag": "MyImage/MyContainer",
  "source": "stdout",
  "line": "{\"foo\": \"bar\"}"
}
```

To format messages as `json` objects, set `--log-opt splunk-format=json`. The
driver attempts to parse every line as a JSON object and send it as an embedded
object. If it can't parse the message, it's sent `inline`. For example:

```json
{
  "attrs": {
    "env1": "val1",
    "label1": "label1"
  },
  "tag": "MyImage/MyContainer",
  "source": "stdout",
  "line": "my message"
}
```

```json
{
  "attrs": {
    "env1": "val1",
    "label1": "label1"
  },
  "tag": "MyImage/MyContainer",
  "source": "stdout",
  "line": {
    "foo": "bar"
  }
}
```

To format messages as `raw`, set `--log-opt splunk-format=raw`. Attributes
(environment variables and labels) and tags are prefixed to the message. For
example:

```console
MyImage/MyContainer env1=val1 label1=label1 my message
MyImage/MyContainer env1=val1 label1=label1 {"foo": "bar"}
```

## Advanced options

The Splunk logging driver lets you configure a few advanced options by setting
environment variables for the Docker daemon.

| Environment variable name | Default value | Description |
| --- | --- | --- |
| SPLUNK_LOGGING_DRIVER_POST_MESSAGES_FREQUENCY | 5s | The time to wait for more messages to batch. |
| SPLUNK_LOGGING_DRIVER_POST_MESSAGES_BATCH_SIZE | 1000 | The number of messages that should accumulate before sending them in one batch. |
| SPLUNK_LOGGING_DRIVER_BUFFER_MAX | 10 * 1000 | The maximum number of messages held in buffer for retries. |
| SPLUNK_LOGGING_DRIVER_CHANNEL_SIZE | 4 * 1000 | The maximum number of pending messages that can be in the channel used to send messages to background logger worker, which batches them. |

---

# Syslog logging driver

> Learn how to use the syslog logging driver with Docker Engine

# Syslog logging driver

   Table of contents

---

The `syslog` logging driver routes logs to a `syslog` server. The `syslog` protocol uses
a raw string as the log message and supports a limited set of metadata. The syslog
message must be formatted in a specific way to be valid. From a valid message, the
receiver can extract the following information:

- Priority: the logging level, such as `debug`, `warning`, `error`, `info`.
- Timestamp: when the event occurred.
- Hostname: where the event happened.
- Facility: which subsystem logged the message, such as `mail` or `kernel`.
- Process name and process ID (PID): The name and ID of the process that generated the log.

The format is defined in [RFC 5424](https://tools.ietf.org/html/rfc5424) and Docker's syslog driver implements the
[ABNF reference](https://tools.ietf.org/html/rfc5424#section-6) in the following way:

```text
TIMESTAMP SP HOSTNAME SP APP-NAME SP PROCID SP MSGID
                    +          +             +           |        +
                    |          |             |           |        |
                    |          |             |           |        |
       +------------+          +----+        |           +----+   +---------+
       v                            v        v                v             v
2017-04-01T17:41:05.616647+08:00 a.vm {taskid:aa,version:} 1787791 {taskid:aa,version:}
```

## Usage

To use the `syslog` driver as the default logging driver, set the `log-driver`
and `log-opt` keys to appropriate values in the `daemon.json` file, which is
located in `/etc/docker/` on Linux hosts or
`C:\ProgramData\docker\config\daemon.json` on Windows Server. For more about
configuring Docker using `daemon.json`, see
[daemon.json](https://docs.docker.com/reference/cli/dockerd/#daemon-configuration-file).

The following example sets the log driver to `syslog` and sets the
`syslog-address` option. The `syslog-address` options supports both UDP and TCP;
this example uses UDP.

```json
{
  "log-driver": "syslog",
  "log-opts": {
    "syslog-address": "udp://1.2.3.4:1111"
  }
}
```

Restart Docker for the changes to take effect.

> Note
>
> `log-opts` configuration options in the `daemon.json` configuration file must
> be provided as strings. Numeric and Boolean values (such as the value for
> `syslog-tls-skip-verify`) must therefore be enclosed in quotes (`"`).

You can set the logging driver for a specific container by using the
`--log-driver` flag to `docker container create` or `docker run`:

```console
$ docker run \
      --log-driver syslog --log-opt syslog-address=udp://1.2.3.4:1111 \
      alpine echo hello world
```

## Options

The following logging options are supported as options for the `syslog` logging
driver. They can be set as defaults in the `daemon.json`, by adding them as
key-value pairs to the `log-opts` JSON array. They can also be set on a given
container by adding a `--log-opt <key>=<value>` flag for each option when
starting the container.

| Option | Description | Example value |
| --- | --- | --- |
| syslog-address | The address of an externalsyslogserver. The URI specifier may be[tcp|udp|tcp+tls]://host:port,unix://path, orunixgram://path. If the transport istcp,udp, ortcp+tls, the default port is514. | --log-opt syslog-address=tcp+tls://192.168.1.3:514,--log-opt syslog-address=unix:///tmp/syslog.sock |
| syslog-facility | Thesyslogfacility to use. Can be the number or name for any validsyslogfacility. See thesyslog documentation. | --log-opt syslog-facility=daemon |
| syslog-tls-ca-cert | The absolute path to the trust certificates signed by the CA. Ignored if the address protocol isn'ttcp+tls. | --log-opt syslog-tls-ca-cert=/etc/ca-certificates/custom/ca.pem |
| syslog-tls-cert | The absolute path to the TLS certificate file. Ignored if the address protocol isn'ttcp+tls. | --log-opt syslog-tls-cert=/etc/ca-certificates/custom/cert.pem |
| syslog-tls-key | The absolute path to the TLS key file. Ignored if the address protocol isn'ttcp+tls. | --log-opt syslog-tls-key=/etc/ca-certificates/custom/key.pem |
| syslog-tls-skip-verify | If set totrue, TLS verification is skipped when connecting to thesyslogdaemon. Defaults tofalse. Ignored if the address protocol isn'ttcp+tls. | --log-opt syslog-tls-skip-verify=true |
| tag | A string that's appended to theAPP-NAMEin thesyslogmessage. By default, Docker uses the first 12 characters of the container ID to tag log messages. Refer to thelog tag option documentationfor customizing the log tag format. | --log-opt tag=mailer |
| syslog-format | Thesyslogmessage format to use. If not specified the local Unix syslog format is used, without a specified hostname. Specifyrfc3164for the RFC-3164 compatible format,rfc5424for RFC-5424 compatible format, orrfc5424microfor RFC-5424 compatible format with microsecond timestamp resolution. | --log-opt syslog-format=rfc5424micro |
| labels | Applies when starting the Docker daemon. A comma-separated list of logging-related labels this daemon accepts. Used for advancedlog tag options. | --log-opt labels=production_status,geo |
| labels-regex | Applies when starting the Docker daemon. Similar to and compatible withlabels. A regular expression to match logging-related labels. Used for advancedlog tag options. | --log-opt labels-regex=^(production_status|geo) |
| env | Applies when starting the Docker daemon. A comma-separated list of logging-related environment variables this daemon accepts. Used for advancedlog tag options. | --log-opt env=os,customer |
| env-regex | Applies when starting the Docker daemon. Similar to and compatible withenv. A regular expression to match logging-related environment variables. Used for advancedlog tag options. | --log-opt env-regex=^(os|customer) |

---

# Use docker logs with remote logging drivers

> Learn how to read container logs locally when using a third party logging solution.

# Use docker logs with remote logging drivers

   Table of contents

---

## Overview

You can use the `docker logs` command to read container logs regardless of the
configured logging driver or plugin. Docker Engine uses the [local](https://docs.docker.com/engine/logging/drivers/local/)
logging driver to act as cache for reading the latest logs of your containers.
This is called dual logging. By default, the cache has log-file rotation
enabled, and is limited to a maximum of 5 files of 20 MB each (before
compression) per container.

Refer to the [configuration options](#configuration-options) section to customize
these defaults, or to the [disable dual logging](#disable-the-dual-logging-cache)
section to disable this feature.

## Prerequisites

Docker Engine automatically enables dual logging if the configured logging
driver doesn't support reading logs.

The following examples show the result of running a `docker logs` command with
and without dual logging availability:

### Without dual logging capability

When a container is configured with a remote logging driver such as `splunk`, and
dual logging is disabled, an error is displayed when attempting to read container
logs locally:

- Step 1: Configure Docker daemon
  ```console
  $ cat /etc/docker/daemon.json
  {
    "log-driver": "splunk",
    "log-opts": {
      "cache-disabled": "true",
      ... (options for "splunk" logging driver)
    }
  }
  ```
- Step 2: Start the container
  ```console
  $ docker run -d busybox --name testlog top
  ```
- Step 3: Read the container logs
  ```console
  $ docker logs 7d6ac83a89a0
  Error response from daemon: configured logging driver does not support reading
  ```

### With dual logging capability

With the dual logging cache enabled, the `docker logs` command can be used to
read logs, even if the logging driver doesn't support reading logs. The following
example shows a daemon configuration that uses the `splunk` remote logging driver
as a default, with dual logging caching enabled:

- Step 1: Configure Docker daemon
  ```console
  $ cat /etc/docker/daemon.json
  {
    "log-driver": "splunk",
    "log-opts": {
      ... (options for "splunk" logging driver)
    }
  }
  ```
- Step 2: Start the container
  ```console
  $ docker run -d busybox --name testlog top
  ```
- Step 3: Read the container logs
  ```console
  $ docker logs 7d6ac83a89a0
  2019-02-04T19:48:15.423Z [INFO]  core: marked as sealed
  2019-02-04T19:48:15.423Z [INFO]  core: pre-seal teardown starting
  2019-02-04T19:48:15.423Z [INFO]  core: stopping cluster listeners
  2019-02-04T19:48:15.423Z [INFO]  core: shutting down forwarding rpc listeners
  2019-02-04T19:48:15.423Z [INFO]  core: forwarding rpc listeners stopped
  2019-02-04T19:48:15.599Z [INFO]  core: rpc listeners successfully shut down
  2019-02-04T19:48:15.599Z [INFO]  core: cluster listeners successfully shut down
  ```

> Note
>
> For logging drivers that support reading logs, such as the `local`, `json-file`
> and `journald` drivers, there is no difference in functionality before or after
> the dual logging capability became available. For these drivers, Logs can be
> read using `docker logs` in both scenarios.

### Configuration options

The dual logging cache accepts the same configuration options as the
[locallogging driver](https://docs.docker.com/engine/logging/drivers/local/), but with a `cache-` prefix. These options
can be specified per container, and defaults for new containers can be set using
the
[daemon configuration file](https://docs.docker.com/reference/cli/dockerd/#daemon-configuration-file).

By default, the cache has log-file rotation enabled, and is limited to a maximum
of 5 files of 20MB each (before compression) per container. Use the configuration
options described below to customize these defaults.

| Option | Default | Description |
| --- | --- | --- |
| cache-disabled | "false" | Disable local caching. Boolean value passed as a string (true,1,0, orfalse). |
| cache-max-size | "20m" | The maximum size of the cache before it is rotated. A positive integer plus a modifier representing the unit of measure (k,m, org). |
| cache-max-file | "5" | The maximum number of cache files that can be present. If rotating the logs creates excess files, the oldest file is removed. A positive integer. |
| cache-compress | "true" | Enable or disable compression of rotated log files. Boolean value passed as a string (true,1,0, orfalse). |

## Disable the dual logging cache

Use the `cache-disabled` option to disable the dual logging cache. Disabling the
cache can be useful to save storage space in situations where logs are only read
through a remote logging system, and if there is no need to read logs through
`docker logs` for debugging purposes.

Caching can be disabled for individual containers or by default for new containers,
when using the
[daemon configuration file](https://docs.docker.com/reference/cli/dockerd/#daemon-configuration-file).

The following example uses the daemon configuration file to use the [splunk](https://docs.docker.com/engine/logging/drivers/splunk/)
logging driver as a default, with caching disabled:

```console
$ cat /etc/docker/daemon.json
{
  "log-driver": "splunk",
  "log-opts": {
    "cache-disabled": "true",
    ... (options for "splunk" logging driver)
  }
}
```

> Note
>
> For logging drivers that support reading logs, such as the `local`, `json-file`
> and `journald` drivers, dual logging isn't used, and disabling the option has
> no effect.

## Limitations

- If a container using a logging driver or plugin that sends logs remotely
  has a network issue, no `write` to the local cache occurs.
- If a write to `logdriver` fails for any reason (file system full, write
  permissions removed), the cache write fails and is logged in the daemon log.
  The log entry to the cache isn't retried.
- Some logs might be lost from the cache in the default configuration because a
  ring buffer is used to prevent blocking the stdio of the container in case of
  slow file writes. An admin must repair these while the daemon is shut down.

---

# Customize log driver output

> Learn about how to format log output with Go templates

# Customize log driver output

---

The `tag` log option specifies how to format a tag that identifies the
container's log messages. By default, the system uses the first 12 characters of
the container ID. To override this behavior, specify a `tag` option:

```console
$ docker run --log-driver=fluentd --log-opt fluentd-address=myhost.local:24224 --log-opt tag="mailer"
```

Docker supports some special template markup you can use when specifying a tag's value:

| Markup | Description |
| --- | --- |
| {{.ID}} | The first 12 characters of the container ID. |
| {{.FullID}} | The full container ID. |
| {{.Name}} | The container name. |
| {{.ImageID}} | The first 12 characters of the container's image ID. |
| {{.ImageFullID}} | The container's full image ID. |
| {{.ImageName}} | The name of the image used by the container. |
| {{.DaemonName}} | The name of the Docker program (docker). |

For example, specifying a `--log-opt tag="{{.ImageName}}/{{.Name}}/{{.ID}}"` value yields `syslog` log lines like:

```text
Aug  7 18:33:19 HOSTNAME hello-world/foobar/5790672ab6a0[9103]: Hello from Docker.
```

At startup time, the system sets the `container_name` field and `{{.Name}}` in
the tags. If you use `docker rename` to rename a container, the new name isn't
reflected in the log messages. Instead, these messages continue to use the
original container name.

---

# Use a logging driver plugin

> Learn about logging driver plugins for extending and customizing Docker's logging capabilities

# Use a logging driver plugin

   Table of contents

---

Docker logging plugins allow you to extend and customize Docker's logging
capabilities beyond those of the [built-in logging drivers](https://docs.docker.com/engine/logging/configure/).
A logging service provider can
[implement their own plugins](https://docs.docker.com/engine/extend/plugins_logging/) and make them
available on Docker Hub, or a private registry. This topic shows
how a user of that logging service can configure Docker to use the plugin.

## Install the logging driver plugin

To install a logging driver plugin, use `docker plugin install <org/image>`,
using the information provided by the plugin developer.

You can list all installed plugins using `docker plugin ls`, and you can inspect
a specific plugin using `docker inspect`.

## Configure the plugin as the default logging driver

When the plugin is installed, you can configure the Docker daemon to use it as
the default by setting the plugin's name as the value of the `log-driver`
key in the `daemon.json`, as detailed in the
[logging overview](https://docs.docker.com/engine/logging/configure/#configure-the-default-logging-driver). If the
logging driver supports additional options, you can set those as the values of
the `log-opts` array in the same file.

## Configure a container to use the plugin as the logging driver

After the plugin is installed, you can configure a container to use the plugin
as its logging driver by specifying the `--log-driver` flag to `docker run`, as
detailed in the
[logging overview](https://docs.docker.com/engine/logging/configure/#configure-the-logging-driver-for-a-container).
If the logging driver supports additional options, you can specify them using
one or more `--log-opt` flags with the option name as the key and the option
value as the value.

---

# View container logs

> Learn how to write to, view, and configure a container's logs

# View container logs

   Table of contents

---

The `docker logs` command shows information logged by a running container. The
`docker service logs` command shows information logged by all containers
participating in a service. The information that's logged and the format of the
log depends almost entirely on the container's endpoint command.

By default, `docker logs` or `docker service logs` shows the command's output
just as it would appear if you ran the command interactively in a terminal. Unix
and Linux commands typically open three I/O streams when they run, called
`STDIN`, `STDOUT`, and `STDERR`. `STDIN` is the command's input stream, which
may include input from the keyboard or input from another command. `STDOUT` is
usually a command's normal output, and `STDERR` is typically used to output
error messages. By default, `docker logs` shows the command's `STDOUT` and
`STDERR`. To read more about I/O and Linux, see the
[Linux Documentation Project article on I/O redirection](https://tldp.org/LDP/abs/html/io-redirection.html).

In some cases, `docker logs` may not show useful information unless you take
additional steps.

- If you use a [logging driver](https://docs.docker.com/engine/logging/configure/) which sends logs to a file, an
  external host, a database, or another logging back-end, and have ["dual logging"](https://docs.docker.com/engine/logging/dual-logging/)
  disabled, `docker logs` may not show useful information.
- If your image runs a non-interactive process such as a web server or a
  database, that application may send its output to log files instead of `STDOUT`
  and `STDERR`.

In the first case, your logs are processed in other ways and you may choose not
to use `docker logs`. In the second case, the official `nginx` image shows one
workaround, and the official Apache `httpd` image shows another.

The official `nginx` image creates a symbolic link from `/var/log/nginx/access.log`
to `/dev/stdout`, and creates another symbolic link
from `/var/log/nginx/error.log` to `/dev/stderr`, overwriting the log files and
causing logs to be sent to the relevant special device instead. See the
[Dockerfile](https://github.com/nginxinc/docker-nginx/blob/8921999083def7ba43a06fabd5f80e4406651353/mainline/jessie/Dockerfile#L21-L23).

The official `httpd` driver changes the `httpd` application's configuration to
write its normal output directly to `/proc/self/fd/1` (which is `STDOUT`) and
its errors to `/proc/self/fd/2` (which is `STDERR`). See the
[Dockerfile](https://github.com/docker-library/httpd/blob/b13054c7de5c74bbaa6d595dbe38969e6d4f860c/2.2/Dockerfile#L72-L75).

## Next steps

- Configure [logging drivers](https://docs.docker.com/engine/logging/configure/).
- Write a
  [Dockerfile](https://docs.docker.com/reference/dockerfile/).
