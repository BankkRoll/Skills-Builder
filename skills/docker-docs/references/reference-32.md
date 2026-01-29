# docker node update and more

# docker node update

# docker node update

| Description | Update a node |
| --- | --- |
| Usage | docker node update [OPTIONS] NODE |

Swarm
This command works with the Swarm orchestrator.

## Description

Update metadata about a node, such as its availability, labels, or roles.

> Note
>
> This is a cluster management command, and must be executed on a swarm
> manager node. To learn about managers and workers, refer to the
> [Swarm mode section](https://docs.docker.com/engine/swarm/) in the
> documentation.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --availability |  | Availability of the node (active,pause,drain) |
| --label-add |  | Add or update a node label (key=value) |
| --label-rm |  | Remove a node label if exists |
| --role |  | Role of the node (worker,manager) |

## Examples

### Add label metadata to a node (--label-add)

Add metadata to a swarm node using node labels. You can specify a node label as
a key with an empty value:

```bash
$ docker node update --label-add foo worker1
```

To add multiple labels to a node, pass the `--label-add` flag for each label:

```console
$ docker node update --label-add foo --label-add bar worker1
```

When you
[create a service](https://docs.docker.com/reference/cli/docker/service/create/),
you can use node labels as a constraint. A constraint limits the nodes where the
scheduler deploys tasks for a service.

For example, to add a `type` label to identify nodes where the scheduler should
deploy message queue service tasks:

```bash
$ docker node update --label-add type=queue worker1
```

The labels you set for nodes using `docker node update` apply only to the node
entity within the swarm. Do not confuse them with the docker daemon labels for
[dockerd](https://docs.docker.com/reference/cli/dockerd/).

For more information about labels, refer to
[apply custom
metadata](https://docs.docker.com/engine/userguide/labels-custom-metadata/).

---

# docker node

# docker node

| Description | Manage Swarm nodes |
| --- | --- |
| Usage | docker node |

Swarm
This command works with the Swarm orchestrator.

## Description

Manage nodes.

## Subcommands

| Command | Description |
| --- | --- |
| docker node demote | Demote one or more nodes from manager in the swarm |
| docker node inspect | Display detailed information on one or more nodes |
| docker node ls | List nodes in the swarm |
| docker node promote | Promote one or more nodes to manager in the swarm |
| docker node ps | List tasks running on one or more nodes, defaults to current node |
| docker node rm | Remove one or more nodes from the swarm |
| docker node update | Update a node |

---

# docker offload diagnose

# docker offload diagnose

| Description | Print diagnostic information for Docker Offload |
| --- | --- |
| Usage | docker offload diagnose |

Availability: Early Access
Requires: Docker Desktop 4.50 and later

---

# docker offload start

# docker offload start

| Description | Start a Docker Offload session |
| --- | --- |
| Usage | docker offload start |

Availability: Early Access
Requires: Docker Desktop 4.50 and later

## Options

| Option | Default | Description |
| --- | --- | --- |
| -a, --account |  | The Docker account to use |
| -g, --gpu |  | Request an engine with a gpu |
| --idle-timeout |  | How long before the engine idles |
| --timeout | 10s | How long to wait for the engine to be ready |

---

# docker offload status

# docker offload status

| Description | Show the status of the Docker Offload connection |
| --- | --- |
| Usage | docker offload status [OPTIONS] |

Availability: Early Access
Requires: Docker Desktop 4.50 and later

## Options

| Option | Default | Description |
| --- | --- | --- |
| -f, --format | pretty | Format of output (default: pretty, one of: pretty|json) |
| -w, --watch |  | Watch for status updates |

---

# docker offload stop

# docker offload stop

| Description | Stop a Docker Offload session |
| --- | --- |
| Usage | docker offload stop [OPTIONS] |

Availability: Early Access
Requires: Docker Desktop 4.50 and later

## Options

| Option | Default | Description |
| --- | --- | --- |
| -f, --force |  | Don't prompt for confirmation |

---

# docker offload version

# docker offload version

| Description | Prints the version |
| --- | --- |
| Usage | docker offload version [OPTIONS] |

Availability: Early Access
Requires: Docker Desktop 4.50 and later

## Options

| Option | Default | Description |
| --- | --- | --- |
| --json |  | Prints the version as JSON |
| --short |  | Prints the short version |

---

# docker offload

# docker offload

| Description | Control Docker Offload from the CLI |
| --- | --- |
| Usage | docker offload |

Availability: Early Access
Requires: Docker Desktop 4.50 and later

## Subcommands

| Command | Description |
| --- | --- |
| docker offload diagnose | Print diagnostic information for Docker Offload |
| docker offload start | Start a Docker Offload session |
| docker offload status | Show the status of the Docker Offload connection |
| docker offload stop | Stop a Docker Offload session |
| docker offload version | Prints the version |

---

# docker pass get

# docker pass get

| Description | Get a secret |
| --- | --- |
| Usage | docker pass get NAME |

Availability: Beta
Requires: Docker Desktop 4.54 and later

**Experimental**

**This command is experimental.**

Experimental features are intended for testing and feedback as their
functionality or design may change between releases without warning or
can be removed entirely in a future release.

---

# docker pass ls

# docker pass ls

| Description | List secrets |
| --- | --- |
| Usage | docker pass ls |

Availability: Beta
Requires: Docker Desktop 4.54 and later

**Experimental**

**This command is experimental.**

Experimental features are intended for testing and feedback as their
functionality or design may change between releases without warning or
can be removed entirely in a future release.

---

# docker pass rm

# docker pass rm

| Description | Remove a secret |
| --- | --- |
| Usage | docker pass rm NAME |

Availability: Beta
Requires: Docker Desktop 4.54 and later

**Experimental**

**This command is experimental.**

Experimental features are intended for testing and feedback as their
functionality or design may change between releases without warning or
can be removed entirely in a future release.

---

# docker pass set

# docker pass set

| Description | Set a secret |
| --- | --- |
| Usage | docker pass set NAME=VALUE |

Availability: Beta
Requires: Docker Desktop 4.54 and later

**Experimental**

**This command is experimental.**

Experimental features are intended for testing and feedback as their
functionality or design may change between releases without warning or
can be removed entirely in a future release.

## Description

Secrets can also be created from STDIN:

```console
<some command> | docker pass set <name>
```

---

# docker pass

# docker pass

| Description | Manage your local OS keychain secrets. |
| --- | --- |
| Usage | docker pass set|get|ls|rm |

Availability: Beta
Requires: Docker Desktop 4.54 and later

**Experimental**

**This command is experimental.**

Experimental features are intended for testing and feedback as their
functionality or design may change between releases without warning or
can be removed entirely in a future release.

## Description

Docker Pass is a helper that allows you to store secrets securely in your
local OS keychain and inject them into containers later.

On Windows: Uses the Windows Credential Manager API.

On macOS: Uses macOS Keychain services API.

On Linux: `org.freedesktop.secrets` API (requires DBus and `gnome-keyring` or
`kdewallet` to be installed).

## Examples

### Using keychain secrets in containers

Create a secret:

```console
$ docker pass set GH_TOKEN=123456789
```

Creating a secret from STDIN:

```console
echo 123456789 > token.txt
cat token.txt | docker pass set GH_TOKEN
```

Run a container that uses the secret:

```console
$ docker run -e GH_TOKEN= -dt --name demo busybox
```

Inspect your secret from inside the container

```console
$ docker exec demo sh -c 'echo $GH_TOKEN'
123456789
```

Explicitly assigning a secret to another environment variable:

```console
$ docker run -e GITHUB_TOKEN=se://GH_TOKEN -dt --name demo busybox
```

## Subcommands

| Command | Description |
| --- | --- |
| docker pass get | Get a secret |
| docker pass ls | List secrets |
| docker pass rm | Remove a secret |
| docker pass set | Set a secret |

---

# docker plugin create

# docker plugin create

| Description | Create a plugin from a rootfs and configuration. Plugin data directory must contain config.json and rootfs directory. |
| --- | --- |
| Usage | docker plugin create [OPTIONS] PLUGIN PLUGIN-DATA-DIR |

## Description

Creates a plugin. Before creating the plugin, prepare the plugin's root
filesystem as well as the
[config.json](https://docs.docker.com/engine/extend/config/).

## Options

| Option | Default | Description |
| --- | --- | --- |
| --compress |  | Compress the context using gzip |

## Examples

The following example shows how to create a sample `plugin`.

```console
$ ls -ls /home/pluginDir

total 4
4 -rw-r--r--  1 root root 431 Nov  7 01:40 config.json
0 drwxr-xr-x 19 root root 420 Nov  7 01:40 rootfs

$ docker plugin create plugin /home/pluginDir

plugin

$ docker plugin ls

ID              NAME            DESCRIPTION                  ENABLED
672d8144ec02    plugin:latest   A sample plugin for Docker   false
```

The plugin can subsequently be enabled for local use or pushed to the public registry.

---

# docker plugin disable

# docker plugin disable

| Description | Disable a plugin |
| --- | --- |
| Usage | docker plugin disable [OPTIONS] PLUGIN |

## Description

Disables a plugin. The plugin must be installed before it can be disabled,
see
[docker plugin install](https://docs.docker.com/reference/cli/docker/plugin/install/). Without the `-f` option,
a plugin that has references (e.g., volumes, networks) cannot be disabled.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -f, --force |  | Force the disable of an active plugin |

## Examples

The following example shows that the `sample-volume-plugin` plugin is installed
and enabled:

```console
$ docker plugin ls

ID            NAME                                    DESCRIPTION                ENABLED
69553ca1d123  tiborvass/sample-volume-plugin:latest   A test plugin for Docker   true
```

To disable the plugin, use the following command:

```console
$ docker plugin disable tiborvass/sample-volume-plugin

tiborvass/sample-volume-plugin

$ docker plugin ls

ID            NAME                                    DESCRIPTION                ENABLED
69553ca1d123  tiborvass/sample-volume-plugin:latest   A test plugin for Docker   false
```

---

# docker plugin enable

# docker plugin enable

| Description | Enable a plugin |
| --- | --- |
| Usage | docker plugin enable [OPTIONS] PLUGIN |

## Description

Enables a plugin. The plugin must be installed before it can be enabled,
see
[docker plugin install](https://docs.docker.com/reference/cli/docker/plugin/install/).

## Options

| Option | Default | Description |
| --- | --- | --- |
| --timeout | 30 | HTTP client timeout (in seconds) |

## Examples

The following example shows that the `sample-volume-plugin` plugin is installed,
but disabled:

```console
$ docker plugin ls

ID            NAME                                    DESCRIPTION                ENABLED
69553ca1d123  tiborvass/sample-volume-plugin:latest   A test plugin for Docker   false
```

To enable the plugin, use the following command:

```console
$ docker plugin enable tiborvass/sample-volume-plugin

tiborvass/sample-volume-plugin

$ docker plugin ls

ID            NAME                                    DESCRIPTION                ENABLED
69553ca1d123  tiborvass/sample-volume-plugin:latest   A test plugin for Docker   true
```

---

# docker plugin inspect

# docker plugin inspect

| Description | Display detailed information on one or more plugins |
| --- | --- |
| Usage | docker plugin inspect [OPTIONS] PLUGIN [PLUGIN...] |

## Description

Returns information about a plugin. By default, this command renders all results
in a JSON array.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -f, --format |  | Format output using a custom template:'json': Print in JSON format'TEMPLATE': Print output using the given Go template.Refer tohttps://docs.docker.com/go/formatting/for more information about formatting output with templates |

## Examples

### Inspect a plugin

The following example inspects the `tiborvass/sample-volume-plugin` plugin:

```console
$ docker plugin inspect tiborvass/sample-volume-plugin:latest
```

Output is in JSON format (output below is formatted for readability):

```json
{
  "Id": "8c74c978c434745c3ade82f1bc0acf38d04990eaf494fa507c16d9f1daa99c21",
  "Name": "tiborvass/sample-volume-plugin:latest",
  "PluginReference": "tiborvas/sample-volume-plugin:latest",
  "Enabled": true,
  "Config": {
    "Mounts": [
      {
        "Name": "",
        "Description": "",
        "Settable": null,
        "Source": "/data",
        "Destination": "/data",
        "Type": "bind",
        "Options": [
          "shared",
          "rbind"
        ]
      },
      {
        "Name": "",
        "Description": "",
        "Settable": null,
        "Source": null,
        "Destination": "/foobar",
        "Type": "tmpfs",
        "Options": null
      }
    ],
    "Env": [
      "DEBUG=1"
    ],
    "Args": null,
    "Devices": null
  },
  "Manifest": {
    "ManifestVersion": "v0",
    "Description": "A test plugin for Docker",
    "Documentation": "/engine/extend/plugins/",
    "Interface": {
      "Types": [
        "docker.volumedriver/1.0"
      ],
      "Socket": "plugins.sock"
    },
    "Entrypoint": [
      "plugin-sample-volume-plugin",
      "/data"
    ],
    "Workdir": "",
    "User": {
    },
    "Network": {
      "Type": "host"
    },
    "Capabilities": null,
    "Mounts": [
      {
        "Name": "",
        "Description": "",
        "Settable": null,
        "Source": "/data",
        "Destination": "/data",
        "Type": "bind",
        "Options": [
          "shared",
          "rbind"
        ]
      },
      {
        "Name": "",
        "Description": "",
        "Settable": null,
        "Source": null,
        "Destination": "/foobar",
        "Type": "tmpfs",
        "Options": null
      }
    ],
    "Devices": [
      {
        "Name": "device",
        "Description": "a host device to mount",
        "Settable": null,
        "Path": "/dev/cpu_dma_latency"
      }
    ],
    "Env": [
      {
        "Name": "DEBUG",
        "Description": "If set, prints debug messages",
        "Settable": null,
        "Value": "1"
      }
    ],
    "Args": {
      "Name": "args",
      "Description": "command line arguments",
      "Settable": null,
      "Value": [

      ]
    }
  }
}
```

### Format the output (--format)

```console
$ docker plugin inspect -f '{{.Id}}' tiborvass/sample-volume-plugin:latest

8c74c978c434745c3ade82f1bc0acf38d04990eaf494fa507c16d9f1daa99c21
```

---

# docker plugin install

# docker plugin install

| Description | Install a plugin |
| --- | --- |
| Usage | docker plugin install [OPTIONS] PLUGIN [KEY=VALUE...] |

## Description

Installs and enables a plugin. Docker looks first for the plugin on your Docker
host. If the plugin does not exist locally, then the plugin is pulled from
the registry. Note that the minimum required registry version to distribute
plugins is 2.3.0.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --alias |  | Local name for plugin |
| --disable |  | Do not enable the plugin on install |
| --grant-all-permissions |  | Grant all permissions necessary to run the plugin |

## Examples

The following example installs `vieus/sshfs` plugin and
[sets](https://docs.docker.com/reference/cli/docker/plugin/set/) its
`DEBUG` environment variable to `1`. To install, `pull` the plugin from Docker
Hub and prompt the user to accept the list of privileges that the plugin needs,
set the plugin's parameters and enable the plugin.

```console
$ docker plugin install vieux/sshfs DEBUG=1

Plugin "vieux/sshfs" is requesting the following privileges:
 - network: [host]
 - device: [/dev/fuse]
 - capabilities: [CAP_SYS_ADMIN]
Do you grant the above permissions? [y/N] y
vieux/sshfs
```

After the plugin is installed, it appears in the list of plugins:

```console
$ docker plugin ls

ID             NAME                  DESCRIPTION                ENABLED
69553ca1d123   vieux/sshfs:latest    sshFS plugin for Docker    true
```

---

# docker plugin ls

# docker plugin ls

| Description | List plugins |
| --- | --- |
| Usage | docker plugin ls [OPTIONS] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker plugin list |

## Description

Lists all the plugins that are currently installed. You can install plugins
using the
[docker plugin install](https://docs.docker.com/reference/cli/docker/plugin/install/) command.
You can also filter using the `-f` or `--filter` flag.
Refer to the [filtering](#filter) section for more information about available filter options.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -f, --filter |  | Provide filter values (e.g.enabled=true) |
| --format |  | Format output using a custom template:'table': Print output in table format with column headers (default)'table TEMPLATE': Print output in table format using the given Go template'json': Print in JSON format'TEMPLATE': Print output using the given Go template.Refer tohttps://docs.docker.com/go/formatting/for more information about formatting output with templates |
| --no-trunc |  | Don't truncate output |
| -q, --quiet |  | Only display plugin IDs |

## Examples

```console
$ docker plugin ls

ID            NAME                                    DESCRIPTION                ENABLED
69553ca1d123  tiborvass/sample-volume-plugin:latest   A test plugin for Docker   true
```

### Filtering (--filter)

The filtering flag (`-f` or `--filter`) format is of "key=value". If there is more
than one filter, then pass multiple flags (e.g., `--filter "foo=bar" --filter "bif=baz"`).

The currently supported filters are:

- enabled (boolean - true or false, 0 or 1)
- capability (string - currently `volumedriver`, `networkdriver`, `ipamdriver`, `logdriver`, `metricscollector`, or `authz`)

#### enabled

The `enabled` filter matches on plugins enabled or disabled.

#### capability

The `capability` filter matches on plugin capabilities. One plugin
might have multiple capabilities. Currently `volumedriver`, `networkdriver`,
`ipamdriver`, `logdriver`, `metricscollector`, and `authz` are supported capabilities.

```console
$ docker plugin install --disable vieux/sshfs

Installed plugin vieux/sshfs

$ docker plugin ls --filter enabled=true

ID                  NAME                DESCRIPTION         ENABLED
```

### Format the output (--format)

The formatting options (`--format`) pretty-prints plugins output
using a Go template.

Valid placeholders for the Go template are listed below:

| Placeholder | Description |
| --- | --- |
| .ID | Plugin ID |
| .Name | Plugin name and tag |
| .Description | Plugin description |
| .Enabled | Whether plugin is enabled or not |
| .PluginReference | The reference used to push/pull from a registry |

When using the `--format` option, the `plugin ls` command will either
output the data exactly as the template declares or, when using the
`table` directive, includes column headers as well.

The following example uses a template without headers and outputs the
`ID` and `Name` entries separated by a colon (`:`) for all plugins:

```console
$ docker plugin ls --format "{{.ID}}: {{.Name}}"

4be01827a72e: vieux/sshfs:latest
```

To list all plugins in JSON format, use the `json` directive:

```console
$ docker plugin ls --format json
{"Description":"sshFS plugin for Docker","Enabled":false,"ID":"856d89febb1c","Name":"vieux/sshfs:latest","PluginReference":"docker.io/vieux/sshfs:latest"}
```

---

# docker plugin push

# docker plugin push

| Description | Push a plugin to a registry |
| --- | --- |
| Usage | docker plugin push [OPTIONS] PLUGIN[:TAG] |

## Description

After you have created a plugin using `docker plugin create` and the plugin is
ready for distribution, use `docker plugin push` to share your images to Docker
Hub or a self-hosted registry.

Registry credentials are managed by
[docker login](https://docs.docker.com/reference/cli/docker/login/).

## Examples

The following example shows how to push a sample `user/plugin`.

```console
$ docker plugin ls

ID             NAME                    DESCRIPTION                  ENABLED
69553ca1d456   user/plugin:latest      A sample plugin for Docker   false

$ docker plugin push user/plugin
```

---

# docker plugin rm

# docker plugin rm

| Description | Remove one or more plugins |
| --- | --- |
| Usage | docker plugin rm [OPTIONS] PLUGIN [PLUGIN...] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker plugin remove |

## Description

Removes a plugin. You cannot remove a plugin if it is enabled, you must disable
a plugin using the
[docker plugin disable](https://docs.docker.com/reference/cli/docker/plugin/disable/) before removing
it, or use `--force`. Use of `--force` is not recommended, since it can affect
functioning of running containers using the plugin.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -f, --force |  | Force the removal of an active plugin |

## Examples

The following example disables and removes the `sample-volume-plugin:latest`
plugin:

```console
$ docker plugin disable tiborvass/sample-volume-plugin

tiborvass/sample-volume-plugin

$ docker plugin rm tiborvass/sample-volume-plugin:latest

tiborvass/sample-volume-plugin
```

---

# docker plugin set

# docker plugin set

| Description | Change settings for a plugin |
| --- | --- |
| Usage | docker plugin set PLUGIN KEY=VALUE [KEY=VALUE...] |

## Description

Change settings for a plugin. The plugin must be disabled.

The settings currently supported are:

- env variables
- source of mounts
- path of devices
- args

## Examples

### Change an environment variable

The following example change the env variable `DEBUG` on the
`sample-volume-plugin` plugin.

```console
$ docker plugin inspect -f {{.Settings.Env}} tiborvass/sample-volume-plugin
[DEBUG=0]

$ docker plugin set tiborvass/sample-volume-plugin DEBUG=1

$ docker plugin inspect -f {{.Settings.Env}} tiborvass/sample-volume-plugin
[DEBUG=1]
```

### Change the source of a mount

The following example change the source of the `mymount` mount on
the `myplugin` plugin.

```console
$ docker plugin inspect -f '{{with $mount := index .Settings.Mounts 0}}{{$mount.Source}}{{end}}' myplugin
/foo

$ docker plugins set myplugin mymount.source=/bar

$ docker plugin inspect -f '{{with $mount := index .Settings.Mounts 0}}{{$mount.Source}}{{end}}' myplugin
/bar
```

> Note
>
> Since only `source` is settable in `mymount`,
> `docker plugins set mymount=/bar myplugin` would work too.

### Change a device path

The following example change the path of the `mydevice` device on
the `myplugin` plugin.

```console
$ docker plugin inspect -f '{{with $device := index .Settings.Devices 0}}{{$device.Path}}{{end}}' myplugin

/dev/foo

$ docker plugins set myplugin mydevice.path=/dev/bar

$ docker plugin inspect -f '{{with $device := index .Settings.Devices 0}}{{$device.Path}}{{end}}' myplugin

/dev/bar
```

> Note
>
> Since only `path` is settable in `mydevice`,
> `docker plugins set mydevice=/dev/bar myplugin` would work too.

### Change the source of the arguments

The following example change the value of the args on the `myplugin` plugin.

```console
$ docker plugin inspect -f '{{.Settings.Args}}' myplugin

["foo", "bar"]

$ docker plugins set myplugin myargs="foo bar baz"

$ docker plugin inspect -f '{{.Settings.Args}}' myplugin

["foo", "bar", "baz"]
```

---

# docker plugin upgrade

# docker plugin upgrade

| Description | Upgrade an existing plugin |
| --- | --- |
| Usage | docker plugin upgrade [OPTIONS] PLUGIN [REMOTE] |

## Description

Upgrades an existing plugin to the specified remote plugin image. If no remote
is specified, Docker will re-pull the current image and use the updated version.
All existing references to the plugin will continue to work.
The plugin must be disabled before running the upgrade.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --grant-all-permissions |  | Grant all permissions necessary to run the plugin |
| --skip-remote-check |  | Do not check if specified remote plugin matches existing plugin image |

## Examples

The following example installs `vieus/sshfs` plugin, uses it to create and use
a volume, then upgrades the plugin.

```console
$ docker plugin install vieux/sshfs DEBUG=1

Plugin "vieux/sshfs:next" is requesting the following privileges:
 - network: [host]
 - device: [/dev/fuse]
 - capabilities: [CAP_SYS_ADMIN]
Do you grant the above permissions? [y/N] y
vieux/sshfs:next

$ docker volume create -d vieux/sshfs:next -o sshcmd=root@1.2.3.4:/tmp/shared -o password=XXX sshvolume

sshvolume

$ docker run -it -v sshvolume:/data alpine sh -c "touch /data/hello"

$ docker plugin disable -f vieux/sshfs:next

viex/sshfs:next

# Here docker volume ls doesn't show 'sshfsvolume', since the plugin is disabled
$ docker volume ls

DRIVER              VOLUME NAME

$ docker plugin upgrade vieux/sshfs:next vieux/sshfs:next

Plugin "vieux/sshfs:next" is requesting the following privileges:
 - network: [host]
 - device: [/dev/fuse]
 - capabilities: [CAP_SYS_ADMIN]
Do you grant the above permissions? [y/N] y
Upgrade plugin vieux/sshfs:next to vieux/sshfs:next

$ docker plugin enable vieux/sshfs:next

viex/sshfs:next

$ docker volume ls

DRIVER              VOLUME NAME
viuex/sshfs:next    sshvolume

$ docker run -it -v sshvolume:/data alpine sh -c "ls /data"

hello
```

---

# docker plugin

# docker plugin

| Description | Manage plugins |
| --- | --- |
| Usage | docker plugin |

## Description

Manage plugins.

## Subcommands

| Command | Description |
| --- | --- |
| docker plugin create | Create a plugin from a rootfs and configuration. Plugin data directory must contain config.json and rootfs directory. |
| docker plugin disable | Disable a plugin |
| docker plugin enable | Enable a plugin |
| docker plugin inspect | Display detailed information on one or more plugins |
| docker plugin install | Install a plugin |
| docker plugin ls | List plugins |
| docker plugin push | Push a plugin to a registry |
| docker plugin rm | Remove one or more plugins |
| docker plugin set | Change settings for a plugin |
| docker plugin upgrade | Upgrade an existing plugin |

---

# docker sandbox create cagent

# docker sandbox create cagent

| Description | Create a sandbox for cagent |
| --- | --- |
| Usage | docker sandbox create cagent WORKSPACE |

## Description

Create a sandbox with access to a host workspace for cagent.

The workspace path is required and will be exposed inside the sandbox at the same path as on the host.

Use 'docker sandbox run SANDBOX' to start cagent after creation.

---

# docker sandbox create codex

# docker sandbox create codex

| Description | Create a sandbox for codex |
| --- | --- |
| Usage | docker sandbox create codex WORKSPACE |

## Description

Create a sandbox with access to a host workspace for codex.

The workspace path is required and will be exposed inside the sandbox at the same path as on the host.

Use 'docker sandbox run SANDBOX' to start codex after creation.

---

# docker sandbox create gemini

# docker sandbox create gemini

| Description | Create a sandbox for gemini |
| --- | --- |
| Usage | docker sandbox create gemini WORKSPACE |

## Description

Create a sandbox with access to a host workspace for gemini.

The workspace path is required and will be exposed inside the sandbox at the same path as on the host.

Use 'docker sandbox run SANDBOX' to start gemini after creation.

---

# docker sandbox create kiro

# docker sandbox create kiro

| Description | Create a sandbox for kiro |
| --- | --- |
| Usage | docker sandbox create kiro WORKSPACE |

## Description

Create a sandbox with access to a host workspace for kiro.

The workspace path is required and will be exposed inside the sandbox at the same path as on the host.

Use 'docker sandbox run SANDBOX' to start kiro after creation.

---

# docker sandbox create

# docker sandbox create

| Description | Create a sandbox for an agent |
| --- | --- |
| Usage | docker sandbox create [OPTIONS] AGENT WORKSPACE |

## Description

Create a sandbox with access to a host workspace for an agent.

Available agents are provided as subcommands. Use "create AGENT --help" for agent-specific options.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --load-local-template |  | Load a locally built template image into the sandbox (useful for testing local changes) |
| --name |  | Name for the sandbox (default:-, letters, numbers, hyphens, and underscores) |
| -q, --quiet |  | Suppress verbose output |
| -t, --template |  | Container image to use for the sandbox (default: agent-specific image) |

---

# docker sandbox exec

# docker sandbox exec

| Description | Execute a command inside a sandbox |
| --- | --- |
| Usage | docker sandbox exec [OPTIONS] SANDBOX COMMAND [ARG...] |

## Description

Execute a command in a sandbox that was previously created with 'docker sandbox create'.

The command and any additional arguments are executed inside the sandbox container.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -d, --detach |  | Detached mode: run command in the background |
| --detach-keys |  | Override the key sequence for detaching a container |
| -e, --env |  | Set environment variables |
| --env-file |  | Read in a file of environment variables |
| -i, --interactive |  | Keep STDIN open even if not attached |
| --privileged |  | Give extended privileges to the command |
| -t, --tty |  | Allocate a pseudo-TTY |
| -u, --user |  | Username or UID (format: <name|uid>[:<group|gid>]) |
| -w, --workdir |  | Working directory inside the container |

---

# docker sandbox inspect

# docker sandbox inspect

| Description | Display detailed information on one or more sandboxes |
| --- | --- |
| Usage | docker sandbox inspect [OPTIONS] SANDBOX [SANDBOX...] |

## Description

Display detailed information on one or more sandboxes.

This command retrieves and displays detailed information about the specified
sandboxes using the Docker API. Each sandbox is identified by its unique ID or name.

## Examples

### Inspect a sandbox

```console
$ docker sandbox inspect abc123def
[
  {
    "id": "abc123def69b16c5c0dab4cf699e26f8d01e1ace3aeee06254e0999492e11647",
    "name": "claude-sandbox-2025-11-04-170333",
    "created_at": "2025-11-04T16:03:33.910642347Z",
    "status": "running",
    "template": "docker/sandbox-templates:claude-code",
    "labels": {
      "com.docker.sandbox.agent": "claude",
      "com.docker.sandbox.workingDirectory": "/Users/moby/code/docker/sandboxes",
      "com.docker.sandbox.workingDirectoryInode": "3041007",
      "com.docker.sandboxes": "templates",
      "com.docker.sandboxes.base": "ubuntu:questing",
      "com.docker.sandboxes.flavor": "claude-code",
      "com.docker.sdk": "true",
      "com.docker.sdk.client": "0.1.0-alpha011",
      "com.docker.sdk.container": "0.1.0-alpha012",
      "com.docker.sdk.lang": "go",
      "docker/sandbox": "true",
      "org.opencontainers.image.ref.name": "ubuntu",
      "org.opencontainers.image.version": "25.10"
    }
  }
]
```

---

# docker sandbox ls

# docker sandbox ls

| Description | List VMs |
| --- | --- |
| Usage | docker sandbox ls [OPTIONS] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker sandbox list |

## Description

List all VMs managed by sandboxd with their sandboxes

## Options

| Option | Default | Description |
| --- | --- | --- |
| --json |  | Output in JSON format |
| --no-trunc |  | Don't truncate output |
| -q, --quiet |  | Only display VM names |

## Examples

### List all VMs

```console
$ docker sandbox ls
VM ID         NAME       STATUS    WORKSPACE                    SOCKET PATH                           SANDBOXES    AGENTS
abc123def     claude-vm  running   /home/user/my-project        /Users/.../docker-1764682554072.sock  2           claude
def456ghi     gemini-vm  stopped   /home/user/ml-projects
```

### Show only VM names (--quiet)

```text
--quiet
```

Output only VM names:

```console
$ docker sandbox ls --quiet
claude-vm
gemini-vm
```

### Don't truncate output (--no-trunc)

```text
--no-trunc
```

By default, long VM IDs, workspace paths, and socket paths are truncated for readability. Use `--no-trunc` to display the full values:

```console
$ docker sandbox ls
VM ID         NAME       STATUS    WORKSPACE                   SOCKET PATH                           SANDBOXES    AGENTS
abc123def     claude-vm  running   /home/user/.../my-project   ...sandboxes/vm/claude-vm/docker.sock  2           claude

$ docker sandbox ls --no-trunc
VM ID                     NAME       STATUS    WORKSPACE                                          SOCKET PATH                                                              SANDBOXES    AGENTS
abc123def456ghi789jkl     claude-vm  running   /home/user/very/long/path/to/my-project           /Users/user/.docker/sandboxes/vm/claude-vm/docker-1764682554072.sock    2           claude
```

### JSON output (--json)

```text
--json
```

Output detailed VM information in JSON format:

```console
$ docker sandbox ls --json
{
  "vms": [
    {
      "name": "claude-vm",
      "agent": "claude",
      "status": "running",
      "socket_path": "/Users/user/.docker/sandboxes/vm/claude-vm/docker-1234567890.sock",
      "sandbox_count": 2,
      "workspaces": [
        "/home/user/my-project",
        "/home/user/another-project"
      ]
    },
    {
      "name": "gemini-vm",
      "agent": "gemini",
      "status": "stopped",
      "sandbox_count": 0
    }
  ]
}
```

---

# docker sandbox network log

# docker sandbox network log

| Description | Show network logs |
| --- | --- |
| Usage | docker sandbox network log |

## Description

Show network logs

## Options

| Option | Default | Description |
| --- | --- | --- |
| --json |  | Output in JSON format |
| --limit |  | Maximum number of log entries to show |
| -q, --quiet |  | Only display log entries |

---

# docker sandbox network proxy

# docker sandbox network proxy

| Description | Manage proxy configuration for a sandbox |
| --- | --- |
| Usage | docker sandbox network proxy <sandbox> [OPTIONS] |

## Description

Manage proxy configuration for a sandbox

## Options

| Option | Default | Description |
| --- | --- | --- |
| --allow-cidr |  | Remove an IP range in CIDR notation from the block or bypass lists (can be specified multiple times) |
| --allow-host |  | Permit access to a domain or IP (can be specified multiple times) |
| --block-cidr |  | Block access to an IP range in CIDR notation (can be specified multiple times) |
| --block-host |  | Block access to a domain or IP (can be specified multiple times) |
| --bypass-cidr |  | Bypass proxy for an IP range in CIDR notation (can be specified multiple times) |
| --bypass-host |  | Bypass proxy for a domain or IP (can be specified multiple times) |
| --policy |  | Set the default policy |

---

# docker sandbox network

# docker sandbox network

| Description | Manage sandbox networking |
| --- | --- |
| Usage | docker sandbox network |

## Description

Manage sandbox networking

## Subcommands

| Command | Description |
| --- | --- |
| docker sandbox network log | Show network logs |
| docker sandbox network proxy | Manage proxy configuration for a sandbox |

---

# docker sandbox reset

# docker sandbox reset

| Description | Reset all VM sandboxes and clean up state |
| --- | --- |
| Usage | docker sandbox reset [OPTIONS] |

## Description

Reset all VM sandboxes and permanently delete all VM data.

This command will:

- Stop all running VMs gracefully (30s timeout)
- Delete all VM state directories in ~/.docker/sandboxes/vm/
- Clear all internal registries

The daemon will continue running with fresh state after reset.

⚠️ WARNING: This is a destructive operation that cannot be undone!
All running agents will be forcefully terminated and their work will be lost.

By default, you will be prompted to confirm (y/N).
Use --force to skip the confirmation prompt.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -f, --force |  | Skip confirmation prompt |

---

# docker sandbox rm

# docker sandbox rm

| Description | Remove one or more sandboxes |
| --- | --- |
| Usage | docker sandbox rm SANDBOX [SANDBOX...] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker sandbox remove |

## Description

Remove one or more sandboxes and all their associated resources.

This command will:

- Check if the sandbox exists
- Remove the sandbox and clean up its associated resources

## Examples

### Remove a sandbox

```console
$ docker sandbox rm abc123def
abc123def
```

### Remove multiple sandboxes

```console
$ docker sandbox rm abc123def def456ghi
abc123def
def456ghi
```

### Remove all sandboxes

```console
$ docker sandbox rm $(docker sandbox ls -q)
```

---

# docker sandbox run

# docker sandbox run

| Description | Run an agent in a sandbox |
| --- | --- |
| Usage | docker sandbox run SANDBOX [-- AGENT_ARGS...] | AGENT WORKSPACE [-- AGENT_ARGS...] |

## Description

Run an agent in a sandbox. Create the sandbox if it does not exist.

Pass agent arguments after the "--" separator.

Examples:

# Create and run a sandbox with claude in current directory

docker sandbox run claude .

# Run an existing sandbox

docker sandbox run existing-sandbox

# Run a sandbox with agent arguments

docker sandbox run claude . -- -p "What version are you running?"

## Options

| Option | Default | Description |
| --- | --- | --- |
| --load-local-template |  | Load a locally built template image into the sandbox |
| --name |  | Name for the sandbox (default:-) |
| -t, --template |  | Container image to use for the sandbox (default: agent-specific image) |

## Examples

### Run Claude in the current directory

```console
$ docker sandbox run claude
```

### Specify a workspace directory (-w, --workspace)

```text
--workspace PATH
```

Run the agent in a specific directory:

```console
$ docker sandbox run --workspace ~/projects/my-app claude
```

The workspace directory is mounted at the same absolute path inside the sandbox.

### Enable Docker-in-Docker (--mount-docker-socket)

```text
--mount-docker-socket
```

Mount the host's Docker socket into the sandbox, giving the agent access to Docker commands:

```console
$ docker sandbox run --mount-docker-socket claude
```

> Caution
>
> This grants the agent full access to your Docker daemon with root-level
> privileges. Only use when you trust the code being executed.

The agent can now build images, run containers, and manage your Docker environment.

### Set environment variables (-e, --env)

```text
--env KEY=VALUE
```

Pass environment variables to the sandbox:

```console
$ docker sandbox run \
  --env NODE_ENV=development \
  --env DATABASE_URL=postgresql://localhost/myapp \
  claude
```

### Mount additional volumes (-v, --volume)

```text
--volume HOST_PATH:CONTAINER_PATH[:ro]
```

Mount additional directories or files into the sandbox:

```console
$ docker sandbox run \
  --volume ~/datasets:/data:ro \
  --volume ~/models:/models \
  claude
```

Use `:ro` or `:readonly` to make mounts read-only.

### Use a custom base image (-t, --template)

```text
--template IMAGE
```

Specify a custom container image to use as the sandbox base:

```console
$ docker sandbox run --template python:3-alpine claude
```

By default, each agent uses a pre-configured image. The `--template` option
lets you substitute a different image.

### Name the sandbox (--name)

```text
--name NAME
```

Assign a custom name to the sandbox for easier identification:

```console
$ docker sandbox run --name my-project claude
```

---

# docker sandbox stop

# docker sandbox stop

| Description | Stop one or more sandboxes without removing them |
| --- | --- |
| Usage | docker sandbox stop SANDBOX [SANDBOX...] |

## Description

Stop one or more sandboxes without removing them. The sandboxes can be restarted later.

---

# docker sandbox version

# docker sandbox version

| Description | Show sandbox version information |
| --- | --- |
| Usage | docker sandbox version |

## Description

Show sandbox version information
