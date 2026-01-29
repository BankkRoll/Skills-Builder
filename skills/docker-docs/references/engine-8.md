# Plugin Config Version 1 of Plugin V2 and more

# Plugin Config Version 1 of Plugin V2

> How to develop and use a plugin with the managed plugin system

# Plugin Config Version 1 of Plugin V2

   Table of contents

---

This document outlines the format of the V0 plugin configuration.

Plugin configs describe the various constituents of a Docker engine plugin.
Plugin configs can be serialized to JSON format with the following media types:

| Config Type | Media Type |
| --- | --- |
| config | application/vnd.docker.plugin.v1+json |

## Config Field Descriptions

Config provides the base accessible fields for working with V0 plugin format in
the registry.

- `description` string
  Description of the plugin
- `documentation` string
  Link to the documentation about the plugin
- `interface` PluginInterface
  Interface implemented by the plugins, struct consisting of the following fields:
  - `types` string array
    Types indicate what interface(s) the plugin currently implements.
    Supported types:
    - `docker.volumedriver/1.0`
    - `docker.networkdriver/1.0`
    - `docker.ipamdriver/1.0`
    - `docker.authz/1.0`
    - `docker.logdriver/1.0`
    - `docker.metricscollector/1.0`
  - `socket` string
    Socket is the name of the socket the engine should use to communicate with the plugins.
    the socket will be created in `/run/docker/plugins`.
- `entrypoint` string array
  Entrypoint of the plugin, see [ENTRYPOINT](https://docs.docker.com/reference/dockerfile/#entrypoint)
- `workdir` string
  Working directory of the plugin, see [WORKDIR](https://docs.docker.com/reference/dockerfile/#workdir)
- `network` PluginNetwork
  Network of the plugin, struct consisting of the following fields:
  - `type` string
    Network type.
    Supported types:
    - `bridge`
    - `host`
    - `none`
- `mounts` PluginMount array
  Mount of the plugin, struct consisting of the following fields.
  See [MOUNTS](https://github.com/opencontainers/runtime-spec/blob/master/config.md#mounts).
  - `name` string
    Name of the mount.
  - `description` string
    Description of the mount.
  - `source` string
    Source of the mount.
  - `destination` string
    Destination of the mount.
  - `type` string
    Mount type.
  - `options` string array
    Options of the mount.
- `ipchost` Boolean
  Access to host ipc namespace.
- `pidhost` Boolean
  Access to host PID namespace.
- `propagatedMount` string
  Path to be mounted as rshared, so that mounts under that path are visible to
  Docker. This is useful for volume plugins. This path will be bind-mounted
  outside of the plugin rootfs so it's contents are preserved on upgrade.
- `env` PluginEnv array
  Environment variables of the plugin, struct consisting of the following fields:
  - `name` string
    Name of the environment variable.
  - `description` string
    Description of the environment variable.
  - `value` string
    Value of the environment variable.
- `args` PluginArgs
  Arguments of the plugin, struct consisting of the following fields:
  - `name` string
    Name of the arguments.
  - `description` string
    Description of the arguments.
  - `value` string array
    Values of the arguments.
- `linux` PluginLinux
  - `capabilities` string array
    Capabilities of the plugin (Linux only), see list [here](https://github.com/opencontainers/runc/blob/master/libcontainer/SPEC.md#security)
  - `allowAllDevices` Boolean
    If `/dev` is bind mounted from the host, and allowAllDevices is set to true, the plugin will have `rwm` access to all devices on the host.
  - `devices` PluginDevice array
    Device of the plugin, (Linux only), struct consisting of the following fields.
    See [DEVICES](https://github.com/opencontainers/runtime-spec/blob/master/config-linux.md#devices).
    - `name` string
      Name of the device.
    - `description` string
      Description of the device.
    - `path` string
      Path of the device.

## Example Config

The following example shows the 'tiborvass/sample-volume-plugin' plugin config.

```json
{
  "Args": {
    "Description": "",
    "Name": "",
    "Settable": null,
    "Value": null
  },
  "Description": "A sample volume plugin for Docker",
  "Documentation": "https://docs.docker.com/engine/extend/plugins/",
  "Entrypoint": [
    "/usr/bin/sample-volume-plugin",
    "/data"
  ],
  "Env": [
    {
      "Description": "",
      "Name": "DEBUG",
      "Settable": [
        "value"
      ],
      "Value": "0"
    }
  ],
  "Interface": {
    "Socket": "plugin.sock",
    "Types": [
      "docker.volumedriver/1.0"
    ]
  },
  "Linux": {
    "Capabilities": null,
    "AllowAllDevices": false,
    "Devices": null
  },
  "Mounts": null,
  "Network": {
    "Type": ""
  },
  "PropagatedMount": "/data",
  "User": {},
  "Workdir": ""
}
```

---

# Use Docker Engine plugins

> How to add additional functionality to Docker with plugins extensions

# Use Docker Engine plugins

   Table of contents

---

This document describes the Docker Engine plugins generally available in Docker
Engine. To view information on plugins managed by Docker,
refer to [Docker Engine plugin system](https://docs.docker.com/engine/extend/).

You can extend the capabilities of the Docker Engine by loading third-party
plugins. This page explains the types of plugins and provides links to several
volume and network plugins for Docker.

## Types of plugins

Plugins extend Docker's functionality. They come in specific types. For
example, a [volume plugin](https://docs.docker.com/engine/extend/plugins_volume/) might enable Docker
volumes to persist across multiple Docker hosts and a
[network plugin](https://docs.docker.com/engine/extend/plugins_network/) might provide network plumbing.

Currently Docker supports authorization, volume and network driver plugins. In the future it
will support additional plugin types.

## Installing a plugin

Follow the instructions in the plugin's documentation.

## Finding a plugin

The sections below provide an overview of available third-party plugins.

### Network plugins

| Plugin | Description |
| --- | --- |
| Contiv Networking | An open source network plugin to provide infrastructure and security policies for a multi-tenant micro services deployment, while providing an integration to physical network for non-container workload. Contiv Networking implements the remote driver and IPAM APIs available in Docker 1.9 onwards. |
| Kuryr Network Plugin | A network plugin is developed as part of the OpenStack Kuryr project and implements the Docker networking (libnetwork) remote driver API by utilizing Neutron, the OpenStack networking service. It includes an IPAM driver as well. |
| Kathará Network Plugin | Docker Network Plugin used by Kathará, an open source container-based network emulation system for showing interactive demos/lessons, testing production networks in a sandbox environment, or developing new network protocols. |

### Volume plugins

| Plugin | Description |
| --- | --- |
| Azure File Storage plugin | Lets you mount MicrosoftAzure File Storageshares to Docker containers as volumes using the SMB 3.0 protocol.Learn more. |
| BeeGFS Volume Plugin | An open source volume plugin to create persistent volumes in a BeeGFS parallel file system. |
| Blockbridge plugin | A volume plugin that provides access to an extensible set of container-based persistent storage options. It supports single and multi-host Docker environments with features that include tenant isolation, automated provisioning, encryption, secure deletion, snapshots and QoS. |
| Contiv Volume Plugin | An open source volume plugin that provides multi-tenant, persistent, distributed storage with intent based consumption. It has support for Ceph and NFS. |
| Convoy plugin | A volume plugin for a variety of storage back-ends including device mapper and NFS. It's a simple standalone executable written in Go and provides the framework to support vendor-specific extensions such as snapshots, backups and restore. |
| DigitalOcean Block Storage plugin | Integrates DigitalOcean'sblock storage solutioninto the Docker ecosystem by automatically attaching a given block storage volume to a DigitalOcean droplet and making the contents of the volume available to Docker containers running on that droplet. |
| DRBD plugin | A volume plugin that provides highly available storage replicated byDRBD. Data written to the docker volume is replicated in a cluster of DRBD nodes. |
| Flocker plugin | A volume plugin that provides multi-host portable volumes for Docker, enabling you to run databases and other stateful containers and move them around across a cluster of machines. |
| Fuxi Volume Plugin | A volume plugin that is developed as part of the OpenStack Kuryr project and implements the Docker volume plugin API by utilizing Cinder, the OpenStack block storage service. |
| gce-docker plugin | A volume plugin able to attach, format and mount Google Computepersistent-disks. |
| GlusterFS plugin | A volume plugin that provides multi-host volumes management for Docker using GlusterFS. |
| Horcrux Volume Plugin | A volume plugin that allows on-demand, version controlled access to your data. Horcrux is an open-source plugin, written in Go, and supports SCP,Minioand Amazon S3. |
| HPE 3Par Volume Plugin | A volume plugin that supports HPE 3Par and StoreVirtual iSCSI storage arrays. |
| Infinit volume plugin | A volume plugin that makes it easy to mount and manage Infinit volumes using Docker. |
| IPFS Volume Plugin | An open source volume plugin that allows using anipfsfilesystem as a volume. |
| Keywhiz plugin | A plugin that provides credentials and secret management using Keywhiz as a central repository. |
| Linode Volume Plugin | A plugin that adds the ability to manage Linode Block Storage as Docker Volumes from within a Linode. |
| Local Persist Plugin | A volume plugin that extends the defaultlocaldriver's functionality by allowing you specify a mountpoint anywhere on the host, which enables the files toalways persist, even if the volume is removed viadocker volume rm. |
| NetApp Plugin(nDVP) | A volume plugin that provides direct integration with the Docker ecosystem for the NetApp storage portfolio. The nDVP package supports the provisioning and management of storage resources from the storage platform to Docker hosts, with a robust framework for adding additional platforms in the future. |
| Netshare plugin | A volume plugin that provides volume management for NFS 3/4, AWS EFS and CIFS file systems. |
| Nimble Storage Volume Plugin | A volume plug-in that integrates with Nimble Storage Unified Flash Fabric arrays. The plug-in abstracts array volume capabilities to the Docker administrator to allow self-provisioning of secure multi-tenant volumes and clones. |
| OpenStorage Plugin | A cluster-aware volume plugin that provides volume management for file and block storage solutions. It implements a vendor neutral specification for implementing extensions such as CoS, encryption, and snapshots. It has example drivers based on FUSE, NFS, NBD and EBS to name a few. |
| Portworx Volume Plugin | A volume plugin that turns any server into a scale-out converged compute/storage node, providing container granular storage and highly available volumes across any node, using a shared-nothing storage backend that works with any docker scheduler. |
| Quobyte Volume Plugin | A volume plugin that connects Docker toQuobyte's data center file system, a general-purpose scalable and fault-tolerant storage platform. |
| REX-Ray plugin | A volume plugin which is written in Go and provides advanced storage functionality for many platforms including VirtualBox, EC2, Google Compute Engine, OpenStack, and EMC. |
| Virtuozzo Storage and Ploop plugin | A volume plugin with support for Virtuozzo Storage distributed cloud file system as well as ploop devices. |
| VMware vSphere Storage Plugin | Docker Volume Driver for vSphere enables customers to address persistent storage requirements for Docker containers in vSphere environments. |

### Authorization plugins

| Plugin | Description |
| --- | --- |
| Casbin AuthZ Plugin | An authorization plugin based onCasbin, which supports access control models like ACL, RBAC, ABAC. The access control model can be customized. The policy can be persisted into file or DB. |
| HBM plugin | An authorization plugin that prevents from executing commands with certains parameters. |
| Twistlock AuthZ Broker | A basic extendable authorization plugin that runs directly on the host or inside a container. This plugin allows you to define user policies that it evaluates during authorization. Basic authorization is provided if Docker daemon is started with the --tlsverify flag (username is extracted from the certificate common name). |

## Troubleshooting a plugin

If you are having problems with Docker after loading a plugin, ask the authors
of the plugin for help. The Docker team may not be able to assist you.

## Writing a plugin

If you are interested in writing a plugin for Docker, or seeing how they work
under the hood, see the [Docker plugins reference](https://docs.docker.com/engine/extend/plugin_api/).

---

# Docker Plugin API

> How to write Docker plugins extensions

# Docker Plugin API

   Table of contents

---

Docker plugins are out-of-process extensions which add capabilities to the
Docker Engine.

This document describes the Docker Engine plugin API. To view information on
plugins managed by Docker Engine, refer to [Docker Engine plugin system](https://docs.docker.com/engine/extend/).

This page is intended for people who want to develop their own Docker plugin.
If you just want to learn about or use Docker plugins, look
[here](https://docs.docker.com/engine/extend/legacy_plugins/).

## What plugins are

A plugin is a process running on the same or a different host as the Docker daemon,
which registers itself by placing a file on the daemon host in one of the plugin
directories described in [Plugin discovery](#plugin-discovery).

Plugins have human-readable names, which are short, lowercase strings. For
example, `flocker` or `weave`.

Plugins can run inside or outside containers. Currently running them outside
containers is recommended.

## Plugin discovery

Docker discovers plugins by looking for them in the plugin directory whenever a
user or container tries to use one by name.

There are three types of files which can be put in the plugin directory.

- `.sock` files are Unix domain sockets.
- `.spec` files are text files containing a URL, such as `unix:///other.sock` or `tcp://localhost:8080`.
- `.json` files are text files containing a full json specification for the plugin.

Plugins with Unix domain socket files must run on the same host as the Docker daemon.
Plugins with `.spec` or `.json` files can run on a different host if you specify a remote URL.

Unix domain socket files must be located under `/run/docker/plugins`, whereas
spec files can be located either under `/etc/docker/plugins` or `/usr/lib/docker/plugins`.

The name of the file (excluding the extension) determines the plugin name.

For example, the `flocker` plugin might create a Unix socket at
`/run/docker/plugins/flocker.sock`.

You can define each plugin into a separated subdirectory if you want to isolate definitions from each other.
For example, you can create the `flocker` socket under `/run/docker/plugins/flocker/flocker.sock` and only
mount `/run/docker/plugins/flocker` inside the `flocker` container.

Docker always searches for Unix sockets in `/run/docker/plugins` first. It checks for spec or json files under
`/etc/docker/plugins` and `/usr/lib/docker/plugins` if the socket doesn't exist. The directory scan stops as
soon as it finds the first plugin definition with the given name.

### JSON specification

This is the JSON format for a plugin:

```json
{
  "Name": "plugin-example",
  "Addr": "https://example.com/docker/plugin",
  "TLSConfig": {
    "InsecureSkipVerify": false,
    "CAFile": "/usr/shared/docker/certs/example-ca.pem",
    "CertFile": "/usr/shared/docker/certs/example-cert.pem",
    "KeyFile": "/usr/shared/docker/certs/example-key.pem"
  }
}
```

The `TLSConfig` field is optional and TLS will only be verified if this configuration is present.

## Plugin lifecycle

Plugins should be started before Docker, and stopped after Docker. For
example, when packaging a plugin for a platform which supports `systemd`, you
might use [systemddependencies](https://www.freedesktop.org/software/systemd/man/systemd.unit.html#Before=) to
manage startup and shutdown order.

When upgrading a plugin, you should first stop the Docker daemon, upgrade the
plugin, then start Docker again.

## Plugin activation

When a plugin is first referred to -- either by a user referring to it by name
(e.g. `docker run --volume-driver=foo`) or a container already configured to
use a plugin being started -- Docker looks for the named plugin in the plugin
directory and activates it with a handshake. See Handshake API below.

Plugins are not activated automatically at Docker daemon startup. Rather,
they are activated only lazily, or on-demand, when they are needed.

## Systemd socket activation

Plugins may also be socket activated by `systemd`. The official [Plugins helpers](https://github.com/docker/go-plugins-helpers)
natively supports socket activation. In order for a plugin to be socket activated it needs
a `service` file and a `socket` file.

The `service` file (for example `/lib/systemd/system/your-plugin.service`):

```systemd
[Unit]
Description=Your plugin
Before=docker.service
After=network.target your-plugin.socket
Requires=your-plugin.socket docker.service

[Service]
ExecStart=/usr/lib/docker/your-plugin

[Install]
WantedBy=multi-user.target
```

The `socket` file (for example `/lib/systemd/system/your-plugin.socket`):

```systemd
[Unit]
Description=Your plugin

[Socket]
ListenStream=/run/docker/plugins/your-plugin.sock

[Install]
WantedBy=sockets.target
```

This will allow plugins to be actually started when the Docker daemon connects to
the sockets they're listening on (for instance the first time the daemon uses them
or if one of the plugin goes down accidentally).

## API design

The Plugin API is RPC-style JSON over HTTP, much like webhooks.

Requests flow from the Docker daemon to the plugin. The plugin needs to
implement an HTTP server and bind this to the Unix socket mentioned in the
"plugin discovery" section.

All requests are HTTP `POST` requests.

The API is versioned via an Accept header, which currently is always set to
`application/vnd.docker.plugins.v1+json`.

## Handshake API

Plugins are activated via the following "handshake" API call.

### /Plugin.Activate

Request: empty body

Response:

```json
{
    "Implements": ["VolumeDriver"]
}
```

Responds with a list of Docker subsystems which this plugin implements.
After activation, the plugin will then be sent events from this subsystem.

Possible values are:

- [authz](https://docs.docker.com/engine/extend/plugins_authorization/)
- [NetworkDriver](https://docs.docker.com/engine/extend/plugins_network/)
- [VolumeDriver](https://docs.docker.com/engine/extend/plugins_volume/)

## Plugin retries

Attempts to call a method on a plugin are retried with an exponential backoff
for up to 30 seconds. This may help when packaging plugins as containers, since
it gives plugin containers a chance to start up before failing any user
containers which depend on them.

## Plugins helpers

To ease plugins development, we're providing an `sdk` for each kind of plugins
currently supported by Docker at [docker/go-plugins-helpers](https://github.com/docker/go-plugins-helpers).

---

# Access authorization plugin

> How to create authorization plugins to manage access control to your Docker daemon.

# Access authorization plugin

   Table of contents

---

This document describes the Docker Engine plugins available in Docker
Engine. To view information on plugins managed by Docker Engine,
refer to [Docker Engine plugin system](https://docs.docker.com/engine/extend/).

Docker's out-of-the-box authorization model is all or nothing. Any user with
permission to access the Docker daemon can run any Docker client command. The
same is true for callers using Docker's Engine API to contact the daemon. If you
require greater access control, you can create authorization plugins and add
them to your Docker daemon configuration. Using an authorization plugin, a
Docker administrator can configure granular access policies for managing access
to the Docker daemon.

Anyone with the appropriate skills can develop an authorization plugin. These
skills, at their most basic, are knowledge of Docker, understanding of REST, and
sound programming knowledge. This document describes the architecture, state,
and methods information available to an authorization plugin developer.

## Basic principles

Docker's [plugin infrastructure](https://docs.docker.com/engine/extend/plugin_api/) enables
extending Docker by loading, removing and communicating with
third-party components using a generic API. The access authorization subsystem
was built using this mechanism.

Using this subsystem, you don't need to rebuild the Docker daemon to add an
authorization plugin. You can add a plugin to an installed Docker daemon. You do
need to restart the Docker daemon to add a new plugin.

An authorization plugin approves or denies requests to the Docker daemon based
on both the current authentication context and the command context. The
authentication context contains all user details and the authentication method.
The command context contains all the relevant request data.

Authorization plugins must follow the rules described in [Docker Plugin API](https://docs.docker.com/engine/extend/plugin_api/).
Each plugin must reside within directories described under the
[Plugin discovery](https://docs.docker.com/engine/extend/plugin_api/#plugin-discovery) section.

> Note
>
> The abbreviations `AuthZ` and `AuthN` mean authorization and authentication
> respectively.

## Default user authorization mechanism

If TLS is enabled in the [Docker daemon](https://docs.docker.com/engine/security/https/), the default user authorization flow extracts the user details from the certificate subject name.
That is, the `User` field is set to the client certificate subject common name, and the `AuthenticationMethod` field is set to `TLS`.

## Basic architecture

You are responsible for registering your plugin as part of the Docker daemon
startup. You can install multiple plugins and chain them together. This chain
can be ordered. Each request to the daemon passes in order through the chain.
Only when all the plugins grant access to the resource, is the access granted.

When an HTTP request is made to the Docker daemon through the CLI or via the
Engine API, the authentication subsystem passes the request to the installed
authentication plugin(s). The request contains the user (caller) and command
context. The plugin is responsible for deciding whether to allow or deny the
request.

The sequence diagrams below depict an allow and deny authorization flow:

![Authorization Allow flow](https://docs.docker.com/engine/extend/images/authz_allow.png)  ![Authorization Allow flow](https://docs.docker.com/engine/extend/images/authz_allow.png)![Authorization Deny flow](https://docs.docker.com/engine/extend/images/authz_deny.png)  ![Authorization Deny flow](https://docs.docker.com/engine/extend/images/authz_deny.png)

Each request sent to the plugin includes the authenticated user, the HTTP
headers, and the request/response body. Only the user name and the
authentication method used are passed to the plugin. Most importantly, no user
credentials or tokens are passed. Finally, not all request/response bodies
are sent to the authorization plugin. Only those request/response bodies where
the `Content-Type` is either `text/*` or `application/json` are sent.

For commands that can potentially hijack the HTTP connection (`HTTP Upgrade`), such as `exec`, the authorization plugin is only called for the
initial HTTP requests. Once the plugin approves the command, authorization is
not applied to the rest of the flow. Specifically, the streaming data is not
passed to the authorization plugins. For commands that return chunked HTTP
response, such as `logs` and `events`, only the HTTP request is sent to the
authorization plugins.

During request/response processing, some authorization flows might
need to do additional queries to the Docker daemon. To complete such flows,
plugins can call the daemon API similar to a regular user. To enable these
additional queries, the plugin must provide the means for an administrator to
configure proper authentication and security policies.

## Docker client flows

To enable and configure the authorization plugin, the plugin developer must
support the Docker client interactions detailed in this section.

### Setting up Docker daemon

Enable the authorization plugin with a dedicated command line flag in the
`--authorization-plugin=PLUGIN_ID` format. The flag supplies a `PLUGIN_ID`
value. This value can be the plugin’s socket or a path to a specification file.
Authorization plugins can be loaded without restarting the daemon. Refer
to the [dockerddocumentation](https://docs.docker.com/reference/cli/dockerd/#configuration-reload-behavior) for more information.

```console
$ dockerd --authorization-plugin=plugin1 --authorization-plugin=plugin2,...
```

Docker's authorization subsystem supports multiple `--authorization-plugin` parameters.

### Calling authorized command (allow)

```console
$ docker pull centos
<...>
f1b10cd84249: Pull complete
<...>
```

### Calling unauthorized command (deny)

```console
$ docker pull centos
<...>
docker: Error response from daemon: authorization denied by plugin PLUGIN_NAME: volumes are not allowed.
```

### Error from plugins

```console
$ docker pull centos
<...>
docker: Error response from daemon: plugin PLUGIN_NAME failed with error: AuthZPlugin.AuthZReq: Cannot connect to the Docker daemon. Is the docker daemon running on this host?.
```

## API schema and implementation

In addition to Docker's standard plugin registration method, each plugin
should implement the following two methods:

- `/AuthZPlugin.AuthZReq` This authorize request method is called before the Docker daemon processes the client request.
- `/AuthZPlugin.AuthZRes` This authorize response method is called before the response is returned from Docker daemon to the client.

#### /AuthZPlugin.AuthZReq

Request

```json
{
    "User":              "The user identification",
    "UserAuthNMethod":   "The authentication method used",
    "RequestMethod":     "The HTTP method",
    "RequestURI":        "The HTTP request URI",
    "RequestBody":       "Byte array containing the raw HTTP request body",
    "RequestHeader":     "Byte array containing the raw HTTP request header as a map[string][]string "
}
```

Response

```json
{
    "Allow": "Determined whether the user is allowed or not",
    "Msg":   "The authorization message",
    "Err":   "The error message if things go wrong"
}
```

#### /AuthZPlugin.AuthZRes

Request:

```json
{
    "User":              "The user identification",
    "UserAuthNMethod":   "The authentication method used",
    "RequestMethod":     "The HTTP method",
    "RequestURI":        "The HTTP request URI",
    "RequestBody":       "Byte array containing the raw HTTP request body",
    "RequestHeader":     "Byte array containing the raw HTTP request header as a map[string][]string",
    "ResponseBody":      "Byte array containing the raw HTTP response body",
    "ResponseHeader":    "Byte array containing the raw HTTP response header as a map[string][]string",
    "ResponseStatusCode":"Response status code"
}
```

Response:

```json
{
   "Allow":              "Determined whether the user is allowed or not",
   "Msg":                "The authorization message",
   "Err":                "The error message if things go wrong"
}
```

### Request authorization

Each plugin must support two request authorization messages formats, one from the daemon to the plugin and then from the plugin to the daemon. The tables below detail the content expected in each message.

#### Daemon -> Plugin

| Name | Type | Description |
| --- | --- | --- |
| User | string | The user identification |
| Authentication method | string | The authentication method used |
| Request method | enum | The HTTP method (GET/DELETE/POST) |
| Request URI | string | The HTTP request URI including API version (e.g., v.1.17/containers/json) |
| Request headers | map[string]string | Request headers as key value pairs (without the authorization header) |
| Request body | []byte | Raw request body |

#### Plugin -> Daemon

| Name | Type | Description |
| --- | --- | --- |
| Allow | bool | Boolean value indicating whether the request is allowed or denied |
| Msg | string | Authorization message (will be returned to the client in case the access is denied) |
| Err | string | Error message (will be returned to the client in case the plugin encounter an error. The string value supplied may appear in logs, so should not include confidential information) |

### Response authorization

The plugin must support two authorization messages formats, one from the daemon to the plugin and then from the plugin to the daemon. The tables below detail the content expected in each message.

#### Daemon -> Plugin

| Name | Type | Description |
| --- | --- | --- |
| User | string | The user identification |
| Authentication method | string | The authentication method used |
| Request method | string | The HTTP method (GET/DELETE/POST) |
| Request URI | string | The HTTP request URI including API version (e.g., v.1.17/containers/json) |
| Request headers | map[string]string | Request headers as key value pairs (without the authorization header) |
| Request body | []byte | Raw request body |
| Response status code | int | Status code from the Docker daemon |
| Response headers | map[string]string | Response headers as key value pairs |
| Response body | []byte | Raw Docker daemon response body |

#### Plugin -> Daemon

| Name | Type | Description |
| --- | --- | --- |
| Allow | bool | Boolean value indicating whether the response is allowed or denied |
| Msg | string | Authorization message (will be returned to the client in case the access is denied) |
| Err | string | Error message (will be returned to the client in case the plugin encounter an error. The string value supplied may appear in logs, so should not include confidential information) |

---

# Docker log driver plugins

> Log driver plugins.

# Docker log driver plugins

   Table of contents

---

This document describes logging driver plugins for Docker.

Logging drivers enables users to forward container logs to another service for
processing. Docker includes several logging drivers as built-ins, however can
never hope to support all use-cases with built-in drivers. Plugins allow Docker
to support a wide range of logging services without requiring to embed client
libraries for these services in the main Docker codebase. See the
[plugin documentation](https://docs.docker.com/engine/extend/legacy_plugins/) for more information.

## Create a logging plugin

The main interface for logging plugins uses the same JSON+HTTP RPC protocol used
by other plugin types. See the
[example](https://github.com/cpuguy83/docker-log-driver-test) plugin for a
reference implementation of a logging plugin. The example wraps the built-in
`jsonfilelog` log driver.

## LogDriver protocol

Logging plugins must register as a `LogDriver` during plugin activation. Once
activated users can specify the plugin as a log driver.

There are two HTTP endpoints that logging plugins must implement:

### /LogDriver.StartLogging

Signals to the plugin that a container is starting that the plugin should start
receiving logs for.

Logs will be streamed over the defined file in the request. On Linux this file
is a FIFO. Logging plugins are not currently supported on Windows.

Request:

```json
{
  "File": "/path/to/file/stream",
  "Info": {
          "ContainerID": "123456"
  }
}
```

`File` is the path to the log stream that needs to be consumed. Each call to
`StartLogging` should provide a different file path, even if it's a container
that the plugin has already received logs for prior. The file is created by
Docker with a randomly generated name.

`Info` is details about the container that's being logged. This is fairly
free-form, but is defined by the following struct definition:

```go
type Info struct {
	Config              map[string]string
	ContainerID         string
	ContainerName       string
	ContainerEntrypoint string
	ContainerArgs       []string
	ContainerImageID    string
	ContainerImageName  string
	ContainerCreated    time.Time
	ContainerEnv        []string
	ContainerLabels     map[string]string
	LogPath             string
	DaemonName          string
}
```

`ContainerID` will always be supplied with this struct, but other fields may be
empty or missing.

Response:

```json
{
  "Err": ""
}
```

If an error occurred during this request, add an error message to the `Err` field
in the response. If no error then you can either send an empty response (`{}`)
or an empty value for the `Err` field.

The driver should at this point be consuming log messages from the passed in file.
If messages are unconsumed, it may cause the container to block while trying to
write to its stdio streams.

Log stream messages are encoded as protocol buffers. The protobuf definitions are
in the
[moby repository](https://github.com/moby/moby/blob/master/api/types/plugins/logdriver/entry.proto).

Since protocol buffers are not self-delimited you must decode them from the stream
using the following stream format:

```text
[size][message]
```

Where `size` is a 4-byte big endian binary encoded uint32. `size` in this case
defines the size of the next message. `message` is the actual log entry.

A reference golang implementation of a stream encoder/decoder can be found
[here](https://github.com/docker/docker/blob/master/api/types/plugins/logdriver/io.go)

### /LogDriver.StopLogging

Signals to the plugin to stop collecting logs from the defined file.
Once a response is received, the file will be removed by Docker. You must make
sure to collect all logs on the stream before responding to this request or risk
losing log data.

Requests on this endpoint does not mean that the container has been removed
only that it has stopped.

Request:

```json
{
  "File": "/path/to/file/stream"
}
```

Response:

```json
{
  "Err": ""
}
```

If an error occurred during this request, add an error message to the `Err` field
in the response. If no error then you can either send an empty response (`{}`)
or an empty value for the `Err` field.

## Optional endpoints

Logging plugins can implement two extra logging endpoints:

### /LogDriver.Capabilities

Defines the capabilities of the log driver. You must implement this endpoint for
Docker to be able to take advantage of any of the defined capabilities.

Request:

```json
{}
```

Response:

```json
{
  "ReadLogs": true
}
```

Supported capabilities:

- `ReadLogs` - this tells Docker that the plugin is capable of reading back logs
  to clients. Plugins that report that they support `ReadLogs` must implement the
  `/LogDriver.ReadLogs` endpoint

### /LogDriver.ReadLogs

Reads back logs to the client. This is used when `docker logs <container>` is
called.

In order for Docker to use this endpoint, the plugin must specify as much when
`/LogDriver.Capabilities` is called.

Request:

```json
{
  "ReadConfig": {},
  "Info": {
    "ContainerID": "123456"
  }
}
```

`ReadConfig` is the list of options for reading, it is defined with the following
golang struct:

```go
type ReadConfig struct {
	Since  time.Time
	Tail   int
	Follow bool
}
```

- `Since` defines the oldest log that should be sent.
- `Tail` defines the number of lines to read (e.g. like the command `tail -n 10`)
- `Follow` signals that the client wants to stay attached to receive new log messages
  as they come in once the existing logs have been read.

`Info` is the same type defined in `/LogDriver.StartLogging`. It should be used
to determine what set of logs to read.

Response:

```text
{{ log stream }}
```

The response should be the encoded log message using the same format as the
messages that the plugin consumed from Docker.

---

# Docker network driver plugins

> Network driver plugins.

# Docker network driver plugins

   Table of contents

---

This document describes Docker Engine network driver plugins generally
available in Docker Engine. To view information on plugins
managed by Docker Engine, refer to [Docker Engine plugin system](https://docs.docker.com/engine/extend/).

Docker Engine network plugins enable Engine deployments to be extended to
support a wide range of networking technologies, such as VXLAN, IPVLAN, MACVLAN
or something completely different. Network driver plugins are supported via the
LibNetwork project. Each plugin is implemented as a "remote driver" for
LibNetwork, which shares plugin infrastructure with Engine. Effectively, network
driver plugins are activated in the same way as other plugins, and use the same
kind of protocol.

## Network plugins and Swarm mode

[Legacy plugins](https://docs.docker.com/engine/extend/legacy_plugins/) do not work in Swarm mode. However,
plugins written using the [v2 plugin system](https://docs.docker.com/engine/extend/) do work in Swarm mode, as
long as they are installed on each Swarm worker node.

## Use network driver plugins

The means of installing and running a network driver plugin depend on the
particular plugin. So, be sure to install your plugin according to the
instructions obtained from the plugin developer.

Once running however, network driver plugins are used just like the built-in
network drivers: by being mentioned as a driver in network-oriented Docker
commands. For example,

```console
$ docker network create --driver weave mynet
```

Some network driver plugins are listed in [plugins](https://docs.docker.com/engine/extend/legacy_plugins/)

The `mynet` network is now owned by `weave`, so subsequent commands
referring to that network will be sent to the plugin,

```console
$ docker run --network=mynet busybox top
```

## Find network plugins

Network plugins are written by third parties, and are published by those
third parties, either on
[Docker Hub](https://hub.docker.com/search?q=&type=plugin)
or on the third party's site.

## Write a network plugin

Network plugins implement the [Docker plugin API](https://docs.docker.com/engine/extend/plugin_api/) and the network
plugin protocol

## Network plugin protocol

The network driver protocol, in addition to the plugin activation call, is
documented as part of libnetwork:
[https://github.com/moby/moby/blob/master/daemon/libnetwork/docs/remote.md](https://github.com/moby/moby/blob/master/daemon/libnetwork/docs/remote.md).
