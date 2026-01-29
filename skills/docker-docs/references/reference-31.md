# docker network create and more

# docker network create

# docker network create

| Description | Create a network |
| --- | --- |
| Usage | docker network create [OPTIONS] NETWORK |

## Description

Creates a new network. The `DRIVER` accepts `bridge` or `overlay` which are the
built-in network drivers. If you have installed a third party or your own custom
network driver you can specify that `DRIVER` here also. If you don't specify the
`--driver` option, the command automatically creates a `bridge` network for you.
When you install Docker Engine it creates a `bridge` network automatically. This
network corresponds to the `docker0` bridge that Docker Engine has traditionally relied
on. When you launch a new container with `docker run` it automatically connects to
this bridge network. You cannot remove this default bridge network, but you can
create new ones using the `network create` command.

```console
$ docker network create -d bridge my-bridge-network
```

Bridge networks are isolated networks on a single Docker Engine installation. If you
want to create a network that spans multiple Docker hosts each running Docker
Engine, you must enable Swarm mode, and create an `overlay` network. To read more
about overlay networks with Swarm mode, see
["use overlay networks"](https://docs.docker.com/network/overlay/).

Once you have enabled swarm mode, you can create a swarm-scoped overlay network:

```console
$ docker network create --scope=swarm --attachable -d overlay my-multihost-network
```

By default, swarm-scoped networks do not allow manually started containers to
be attached. This restriction is added to prevent someone that has access to
a non-manager node in the swarm cluster from running a container that is able
to access the network stack of a swarm service.

The `--attachable` option used in the example above disables this restriction,
and allows for both swarm services and manually started containers to attach to
the overlay network.

Network names must be unique. The Docker daemon attempts to identify naming
conflicts but this is not guaranteed. It is the user's responsibility to avoid
name conflicts.

### Overlay network limitations

You should create overlay networks with `/24` blocks (the default), which limits
you to 256 IP addresses, when you create networks using the default VIP-based
endpoint-mode. This recommendation addresses
[limitations with swarm mode](https://github.com/moby/moby/issues/30820). If you
need more than 256 IP addresses, do not increase the IP block size. You can
either use `dnsrr` endpoint mode with an external load balancer, or use multiple
smaller overlay networks. See
[Configure service discovery](https://docs.docker.com/engine/swarm/networking/#configure-service-discovery)
for more information about different endpoint modes.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --attachable |  | API 1.25+Enable manual container attachment |
| --aux-address |  | Auxiliary IPv4 or IPv6 addresses used by Network driver |
| --config-from |  | API 1.30+The network from which to copy the configuration |
| --config-only |  | API 1.30+Create a configuration only network |
| -d, --driver | bridge | Driver to manage the Network |
| --gateway |  | IPv4 or IPv6 Gateway for the master subnet |
| --ingress |  | API 1.29+Create swarm routing-mesh network |
| --internal |  | Restrict external access to the network |
| --ip-range |  | Allocate container ip from a sub-range |
| --ipam-driver |  | IP Address Management Driver |
| --ipam-opt |  | Set IPAM driver specific options |
| --ipv4 | true | Enable or disable IPv4 address assignment |
| --ipv6 |  | Enable or disable IPv6 address assignment |
| --label |  | Set metadata on a network |
| -o, --opt |  | Set driver specific options |
| --scope |  | API 1.30+Control the network's scope |
| --subnet |  | Subnet in CIDR format that represents a network segment |

## Examples

### Connect containers

When you start a container, use the `--network` flag to connect it to a network.
This example adds the `busybox` container to the `mynet` network:

```console
$ docker run -itd --network=mynet busybox
```

If you want to add a container to a network after the container is already
running, use the `docker network connect` subcommand.

You can connect multiple containers to the same network. Once connected, the
containers can communicate using only another container's IP address or name.
For `overlay` networks or custom plugins that support multi-host connectivity,
containers connected to the same multi-host network but launched from different
daemons can also communicate in this way.

You can disconnect a container from a network using the `docker network disconnect` command.

### Specify advanced options

When you create a network, Docker Engine creates a non-overlapping subnetwork
for the network by default. This subnetwork is not a subdivision of an existing
network. It is purely for ip-addressing purposes. You can override this default
and specify subnetwork values directly using the `--subnet` option. On a
`bridge` network you can only create a single subnet:

```console
$ docker network create --driver=bridge --subnet=192.168.0.0/16 br0
```

Additionally, you also specify the `--gateway` `--ip-range` and `--aux-address`
options.

```console
$ docker network create \
  --driver=bridge \
  --subnet=172.28.0.0/16 \
  --ip-range=172.28.5.0/24 \
  --gateway=172.28.5.254 \
  br0
```

If you omit the `--gateway` flag, Docker Engine selects one for you from inside
a preferred pool. For `overlay` networks and for network driver plugins that
support it you can create multiple subnetworks. This example uses two `/25`
subnet mask to adhere to the current guidance of not having more than 256 IPs in
a single overlay network. Each of the subnetworks has 126 usable addresses.

```console
$ docker network create -d overlay \
  --subnet=192.168.10.0/25 \
  --subnet=192.168.20.0/25 \
  --gateway=192.168.10.100 \
  --gateway=192.168.20.100 \
  --aux-address="my-router=192.168.10.5" --aux-address="my-switch=192.168.10.6" \
  --aux-address="my-printer=192.168.20.5" --aux-address="my-nas=192.168.20.6" \
  my-multihost-network
```

Be sure that your subnetworks do not overlap. If they do, the network create
fails and Docker Engine returns an error.

### Bridge driver options

When creating a custom `bridge` network, the following additional options can
be passed. Some of these have equivalent flags that can be used on the dockerd
command line or in `daemon.json` to configure the default bridge, `docker0`:

| Network create option | Daemon option fordocker0 | Description |
| --- | --- | --- |
| com.docker.network.bridge.name | - | Bridge name to be used when creating the Linux bridge |
| com.docker.network.bridge.enable_ip_masquerade | --ip-masq | Enable IP masquerading |
| com.docker.network.bridge.enable_icc | --icc | Enable or Disable Inter Container Connectivity |
| com.docker.network.bridge.host_binding_ipv4 | --ip | Default IP when binding container ports |
| com.docker.network.driver.mtu | --mtu | Set the containers network MTU |
| com.docker.network.container_iface_prefix | - | Set a custom prefix for container interfaces |

The following arguments can be passed to `docker network create` for any
network driver, again with their approximate equivalents to Docker daemon
flags used for the `docker0` bridge:

| Network create option | Daemon option fordocker0 | Description |
| --- | --- | --- |
| --gateway | - | IPv4 or IPv6 Gateway for the master subnet |
| --ip-range | --fixed-cidr,--fixed-cidr-v6 | Allocate IP addresses from a range |
| --internal | - | Restrict external access to the network |
| --ipv4 | - | Enable or disable IPv4 address assignment |
| --ipv6 | --ipv6 | Enable or disable IPv6 address assignment |
| --subnet | --bip,--bip6 | Subnet for network |

For example, let's use `-o` or `--opt` options to specify an IP address binding
when publishing ports:

```console
$ docker network create \
    -o "com.docker.network.bridge.host_binding_ipv4"="172.19.0.1" \
    simple-network
```

### Network internal mode (--internal)

Containers on an internal network may communicate between each other, but not
with any other network, as no default route is configured and firewall rules
are set up to drop all traffic to or from other networks. Communication with
the gateway IP address (and thus appropriately configured host services) is
possible, and the host may communicate with any container IP directly.

By default, when you connect a container to an `overlay` network, Docker also
connects a bridge network to it to provide external connectivity. If you want
to create an externally isolated `overlay` network, you can specify the
`--internal` option.

### Network ingress mode (--ingress)

You can create the network which will be used to provide the routing-mesh in the
swarm cluster. You do so by specifying `--ingress` when creating the network. Only
one ingress network can be created at the time. The network can be removed only
if no services depend on it. Any option available when creating an overlay network
is also available when creating the ingress network, besides the `--attachable` option.

```console
$ docker network create -d overlay \
  --subnet=10.11.0.0/16 \
  --ingress \
  --opt com.docker.network.driver.mtu=9216 \
  --opt encrypted=true \
  my-ingress-network
```

### Run services on predefined networks

You can create services on the predefined Docker networks `bridge` and `host`.

```console
$ docker service create --name my-service \
  --network host \
  --replicas 2 \
  busybox top
```

### Swarm networks with local scope drivers

You can create a swarm network with local scope network drivers. You do so
by promoting the network scope to `swarm` during the creation of the network.
You will then be able to use this network when creating services.

```console
$ docker network create -d bridge \
  --scope swarm \
  --attachable \
  swarm-network
```

For network drivers which provide connectivity across hosts (ex. macvlan), if
node specific configurations are needed in order to plumb the network on each
host, you will supply that configuration via a configuration only network.
When you create the swarm scoped network, you will then specify the name of the
network which contains the configuration.

```console
node1$ docker network create --config-only --subnet 192.168.100.0/24 --gateway 192.168.100.115 mv-config
node2$ docker network create --config-only --subnet 192.168.200.0/24 --gateway 192.168.200.202 mv-config
node1$ docker network create -d macvlan --scope swarm --config-from mv-config --attachable swarm-network
```

---

# docker network disconnect

# docker network disconnect

| Description | Disconnect a container from a network |
| --- | --- |
| Usage | docker network disconnect [OPTIONS] NETWORK CONTAINER |

## Description

Disconnects a container from a network. The container must be running to
disconnect it from the network.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -f, --force |  | Force the container to disconnect from a network |

## Examples

```console
$ docker network disconnect multi-host-network container1
```

---

# docker network inspect

# docker network inspect

| Description | Display detailed information on one or more networks |
| --- | --- |
| Usage | docker network inspect [OPTIONS] NETWORK [NETWORK...] |

## Description

Returns information about one or more networks. By default, this command renders
all results in a JSON object.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -f, --format |  | Format output using a custom template:'json': Print in JSON format'TEMPLATE': Print output using the given Go template.Refer tohttps://docs.docker.com/go/formatting/for more information about formatting output with templates |
| -v, --verbose |  | Verbose output for diagnostics |

---

# docker network ls

# docker network ls

| Description | List networks |
| --- | --- |
| Usage | docker network ls [OPTIONS] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker network list |

## Description

Lists all the networks the Engine `daemon` knows about. This includes the
networks that span across multiple hosts in a cluster.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -f, --filter |  | Provide filter values (e.g.driver=bridge) |
| --format |  | Format output using a custom template:'table': Print output in table format with column headers (default)'table TEMPLATE': Print output in table format using the given Go template'json': Print in JSON format'TEMPLATE': Print output using the given Go template.Refer tohttps://docs.docker.com/go/formatting/for more information about formatting output with templates |
| --no-trunc |  | Do not truncate the output |
| -q, --quiet |  | Only display network IDs |

## Examples

### List all networks

```console
$ docker network ls
NETWORK ID          NAME                DRIVER          SCOPE
7fca4eb8c647        bridge              bridge          local
9f904ee27bf5        none                null            local
cf03ee007fb4        host                host            local
78b03ee04fc4        multi-host          overlay         swarm
```

### List networks without truncating the ID column (--no-trun)

Use the `--no-trunc` option to display the full network id:

```console
$ docker network ls --no-trunc
NETWORK ID                                                         NAME                DRIVER           SCOPE
18a2866682b85619a026c81b98a5e375bd33e1b0936a26cc497c283d27bae9b3   none                null             local
c288470c46f6c8949c5f7e5099b5b7947b07eabe8d9a27d79a9cbf111adcbf47   host                host             local
7b369448dccbf865d397c8d2be0cda7cf7edc6b0945f77d2529912ae917a0185   bridge              bridge           local
95e74588f40db048e86320c6526440c504650a1ff3e9f7d60a497c4d2163e5bd   foo                 bridge           local
63d1ff1f77b07ca51070a8c227e962238358bd310bde1529cf62e6c307ade161   dev                 bridge           local
```

### Filtering (--filter)

The filtering flag (`-f` or `--filter`) format is a `key=value` pair. If there
is more than one filter, then pass multiple flags (e.g. `--filter "foo=bar" --filter "bif=baz"`).
Multiple filter flags are combined as an `OR` filter. For example,
`-f type=custom -f type=builtin` returns both `custom` and `builtin` networks.

The currently supported filters are:

- driver
- id (network's id)
- label (`label=<key>` or `label=<key>=<value>`)
- name (network's name)
- scope (`swarm|global|local`)
- type (`custom|builtin`)

#### Driver

The `driver` filter matches networks based on their driver.

The following example matches networks with the `bridge` driver:

```console
$ docker network ls --filter driver=bridge
NETWORK ID          NAME                DRIVER            SCOPE
db9db329f835        test1               bridge            local
f6e212da9dfd        test2               bridge            local
```

#### ID

The `id` filter matches on all or part of a network's ID.

The following filter matches all networks with an ID containing the
`63d1ff1f77b0...` string.

```console
$ docker network ls --filter id=63d1ff1f77b07ca51070a8c227e962238358bd310bde1529cf62e6c307ade161
NETWORK ID          NAME                DRIVER           SCOPE
63d1ff1f77b0        dev                 bridge           local
```

You can also filter for a substring in an ID as this shows:

```console
$ docker network ls --filter id=95e74588f40d
NETWORK ID          NAME                DRIVER          SCOPE
95e74588f40d        foo                 bridge          local

$ docker network ls --filter id=95e
NETWORK ID          NAME                DRIVER          SCOPE
95e74588f40d        foo                 bridge          local
```

#### Label

The `label` filter matches networks based on the presence of a `label` alone or a `label` and a
value.

The following filter matches networks with the `usage` label regardless of its value.

```console
$ docker network ls -f "label=usage"
NETWORK ID          NAME                DRIVER         SCOPE
db9db329f835        test1               bridge         local
f6e212da9dfd        test2               bridge         local
```

The following filter matches networks with the `usage` label with the `prod` value.

```console
$ docker network ls -f "label=usage=prod"
NETWORK ID          NAME                DRIVER        SCOPE
f6e212da9dfd        test2               bridge        local
```

#### Name

The `name` filter matches on all or part of a network's name.

The following filter matches all networks with a name containing the `foobar` string.

```console
$ docker network ls --filter name=foobar
NETWORK ID          NAME                DRIVER       SCOPE
06e7eef0a170        foobar              bridge       local
```

You can also filter for a substring in a name as this shows:

```console
$ docker network ls --filter name=foo
NETWORK ID          NAME                DRIVER       SCOPE
95e74588f40d        foo                 bridge       local
06e7eef0a170        foobar              bridge       local
```

#### Scope

The `scope` filter matches networks based on their scope.

The following example matches networks with the `swarm` scope:

```console
$ docker network ls --filter scope=swarm
NETWORK ID          NAME                DRIVER              SCOPE
xbtm0v4f1lfh        ingress             overlay             swarm
ic6r88twuu92        swarmnet            overlay             swarm
```

The following example matches networks with the `local` scope:

```console
$ docker network ls --filter scope=local
NETWORK ID          NAME                DRIVER              SCOPE
e85227439ac7        bridge              bridge              local
0ca0e19443ed        host                host                local
ca13cc149a36        localnet            bridge              local
f9e115d2de35        none                null                local
```

#### Type

The `type` filter supports two values; `builtin` displays predefined networks
(`bridge`, `none`, `host`), whereas `custom` displays user defined networks.

The following filter matches all user defined networks:

```console
$ docker network ls --filter type=custom
NETWORK ID          NAME                DRIVER       SCOPE
95e74588f40d        foo                 bridge       local
63d1ff1f77b0        dev                 bridge       local
```

By having this flag it allows for batch cleanup. For example, use this filter
to delete all user defined networks:

```console
$ docker network rm `docker network ls --filter type=custom -q`
```

A warning will be issued when trying to remove a network that has containers
attached.

### Format the output (--format)

The formatting options (`--format`) pretty-prints networks output
using a Go template.

Valid placeholders for the Go template are listed below:

| Placeholder | Description |
| --- | --- |
| .ID | Network ID |
| .Name | Network name |
| .Driver | Network driver |
| .Scope | Network scope (local, global) |
| .IPv6 | Whether IPv6 is enabled on the network or not. |
| .Internal | Whether the network is internal or not. |
| .Labels | All labels assigned to the network. |
| .Label | Value of a specific label for this network. For example{{.Label "project.version"}} |
| .CreatedAt | Time when the network was created |

When using the `--format` option, the `network ls` command will either
output the data exactly as the template declares or, when using the
`table` directive, includes column headers as well.

The following example uses a template without headers and outputs the
`ID` and `Driver` entries separated by a colon (`:`) for all networks:

```console
$ docker network ls --format "{{.ID}}: {{.Driver}}"
afaaab448eb2: bridge
d1584f8dc718: host
391df270dc66: null
```

To list all networks in JSON format, use the `json` directive:

```console
$ docker network ls --format json
{"CreatedAt":"2021-03-09 21:41:29.798999529 +0000 UTC","Driver":"bridge","ID":"f33ba176dd8e","IPv6":"false","Internal":"false","Labels":"","Name":"bridge","Scope":"local"}
{"CreatedAt":"2021-03-09 21:41:29.772806592 +0000 UTC","Driver":"host","ID":"caf47bb3ac70","IPv6":"false","Internal":"false","Labels":"","Name":"host","Scope":"local"}
{"CreatedAt":"2021-03-09 21:41:29.752212603 +0000 UTC","Driver":"null","ID":"9d096c122066","IPv6":"false","Internal":"false","Labels":"","Name":"none","Scope":"local"}
```

---

# docker network prune

# docker network prune

| Description | Remove all unused networks |
| --- | --- |
| Usage | docker network prune [OPTIONS] |

## Description

Remove all unused networks. Unused networks are those which are not referenced
by any containers.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --filter |  | Provide filter values (e.g.until=<timestamp>) |
| -f, --force |  | Do not prompt for confirmation |

## Examples

```console
$ docker network prune

WARNING! This will remove all custom networks not used by at least one container.
Are you sure you want to continue? [y/N] y
Deleted Networks:
n1
n2
```

### Filtering (--filter)

The filtering flag (`--filter`) format is of "key=value". If there is more
than one filter, then pass multiple flags (e.g., `--filter "foo=bar" --filter "bif=baz"`)

The currently supported filters are:

- until (`<timestamp>`) - only remove networks created before given timestamp
- label (`label=<key>`, `label=<key>=<value>`, `label!=<key>`, or `label!=<key>=<value>`) - only remove networks with (or without, in case `label!=...` is used) the specified labels.

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
which removes networks with the specified labels. The other
format is the `label!=...` (`label!=<key>` or `label!=<key>=<value>`), which removes
networks without the specified labels.

The following removes networks created more than 5 minutes ago. Note that
system networks such as `bridge`, `host`, and `none` will never be pruned:

```console
$ docker network ls

NETWORK ID          NAME                DRIVER              SCOPE
7430df902d7a        bridge              bridge              local
ea92373fd499        foo-1-day-ago       bridge              local
ab53663ed3c7        foo-1-min-ago       bridge              local
97b91972bc3b        host                host                local
f949d337b1f5        none                null                local

$ docker network prune --force --filter until=5m

Deleted Networks:
foo-1-day-ago

$ docker network ls

NETWORK ID          NAME                DRIVER              SCOPE
7430df902d7a        bridge              bridge              local
ab53663ed3c7        foo-1-min-ago       bridge              local
97b91972bc3b        host                host                local
f949d337b1f5        none                null                local
```

---

# docker network rm

# docker network rm

| Description | Remove one or more networks |
| --- | --- |
| Usage | docker network rm NETWORK [NETWORK...] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker network remove |

## Description

Removes one or more networks by name or identifier. To remove a network,
you must first disconnect any containers connected to it.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -f, --force |  | Do not error if the network does not exist |

## Examples

### Remove a network

To remove the network named 'my-network':

```console
$ docker network rm my-network
```

### Remove multiple networks

To delete multiple networks in a single `docker network rm` command, provide
multiple network names or ids. The following example deletes a network with id
`3695c422697f` and a network named `my-network`:

```console
$ docker network rm 3695c422697f my-network
```

When you specify multiple networks, the command attempts to delete each in turn.
If the deletion of one network fails, the command continues to the next on the
list and tries to delete that. The command reports success or failure for each
deletion.

---

# docker network

# docker network

| Description | Manage networks |
| --- | --- |
| Usage | docker network |

## Description

Manage networks. You can use subcommands to create, inspect, list, remove,
prune, connect, and disconnect networks.

## Subcommands

| Command | Description |
| --- | --- |
| docker network connect | Connect a container to a network |
| docker network create | Create a network |
| docker network disconnect | Disconnect a container from a network |
| docker network inspect | Display detailed information on one or more networks |
| docker network ls | List networks |
| docker network prune | Remove all unused networks |
| docker network rm | Remove one or more networks |

---

# docker node demote

# docker node demote

| Description | Demote one or more nodes from manager in the swarm |
| --- | --- |
| Usage | docker node demote NODE [NODE...] |

Swarm
This command works with the Swarm orchestrator.

## Description

Demotes an existing manager so that it is no longer a manager.

> Note
>
> This is a cluster management command, and must be executed on a swarm
> manager node. To learn about managers and workers, refer to the
> [Swarm mode
> section](https://docs.docker.com/engine/swarm/) in the documentation.

## Examples

```console
$ docker node demote <node name>
```

---

# docker node inspect

# docker node inspect

| Description | Display detailed information on one or more nodes |
| --- | --- |
| Usage | docker node inspect [OPTIONS] self|NODE [NODE...] |

Swarm
This command works with the Swarm orchestrator.

## Description

Returns information about a node. By default, this command renders all results
in a JSON array. You can specify an alternate format to execute a
given template for each result. Go's
[text/template](https://pkg.go.dev/text/template) package describes all the
details of the format.

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

### Inspect a node

```console
$ docker node inspect swarm-manager
```

```json
[
  {
    "ID": "e216jshn25ckzbvmwlnh5jr3g",
    "Version": {
      "Index": 10
    },
    "CreatedAt": "2017-05-16T22:52:44.9910662Z",
    "UpdatedAt": "2017-05-16T22:52:45.230878043Z",
    "Spec": {
      "Role": "manager",
      "Availability": "active"
    },
    "Description": {
      "Hostname": "swarm-manager",
      "Platform": {
        "Architecture": "x86_64",
        "OS": "linux"
      },
      "Resources": {
        "NanoCPUs": 1000000000,
        "MemoryBytes": 1039843328
      },
      "Engine": {
        "EngineVersion": "17.06.0-ce",
        "Plugins": [
          {
            "Type": "Volume",
            "Name": "local"
          },
          {
            "Type": "Network",
            "Name": "overlay"
          },
          {
            "Type": "Network",
            "Name": "null"
          },
          {
            "Type": "Network",
            "Name": "host"
          },
          {
            "Type": "Network",
            "Name": "bridge"
          },
          {
            "Type": "Network",
            "Name": "overlay"
          }
        ]
      },
      "TLSInfo": {
        "TrustRoot": "-----BEGIN CERTIFICATE-----\nMIIBazCCARCgAwIBAgIUOzgqU4tA2q5Yv1HnkzhSIwGyIBswCgYIKoZIzj0EAwIw\nEzERMA8GA1UEAxMIc3dhcm0tY2EwHhcNMTcwNTAyMDAyNDAwWhcNMzcwNDI3MDAy\nNDAwWjATMREwDwYDVQQDEwhzd2FybS1jYTBZMBMGByqGSM49AgEGCCqGSM49AwEH\nA0IABMbiAmET+HZyve35ujrnL2kOLBEQhFDZ5MhxAuYs96n796sFlfxTxC1lM/2g\nAh8DI34pm3JmHgZxeBPKUURJHKWjQjBAMA4GA1UdDwEB/wQEAwIBBjAPBgNVHRMB\nAf8EBTADAQH/MB0GA1UdDgQWBBS3sjTJOcXdkls6WSY2rTx1KIJueTAKBggqhkjO\nPQQDAgNJADBGAiEAoeVWkaXgSUAucQmZ3Yhmx22N/cq1EPBgYHOBZmHt0NkCIQC3\nzONcJ/+WA21OXtb+vcijpUOXtNjyHfcox0N8wsLDqQ==\n-----END CERTIFICATE-----\n",
        "CertIssuerSubject": "MBMxETAPBgNVBAMTCHN3YXJtLWNh",
        "CertIssuerPublicKey": "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAExuICYRP4dnK97fm6OucvaQ4sERCEUNnkyHEC5iz3qfv3qwWV/FPELWUz/aACHwMjfimbcmYeBnF4E8pRREkcpQ=="
      }
    },
    "Status": {
      "State": "ready",
      "Addr": "168.0.32.137"
    },
    "ManagerStatus": {
      "Leader": true,
      "Reachability": "reachable",
      "Addr": "168.0.32.137:2377"
    }
  }
]
```

### Format the output (--format)

```console
$ docker node inspect --format '{{ .ManagerStatus.Leader }}' self

false
```

Use `--format=pretty` or the `--pretty` shorthand to pretty-print the output:

```console
$ docker node inspect --format=pretty self

ID:                     e216jshn25ckzbvmwlnh5jr3g
Hostname:               swarm-manager
Joined at:              2017-05-16 22:52:44.9910662 +0000 utc
Status:
 State:                 Ready
 Availability:          Active
 Address:               172.17.0.2
Manager Status:
 Address:               172.17.0.2:2377
 Raft Status:           Reachable
 Leader:                Yes
Platform:
 Operating System:      linux
 Architecture:          x86_64
Resources:
 CPUs:                  4
 Memory:                7.704 GiB
Plugins:
  Network:              overlay, bridge, null, host, overlay
  Volume:               local
Engine Version:         17.06.0-ce
TLS Info:
 TrustRoot:
-----BEGIN CERTIFICATE-----
MIIBazCCARCgAwIBAgIUOzgqU4tA2q5Yv1HnkzhSIwGyIBswCgYIKoZIzj0EAwIw
EzERMA8GA1UEAxMIc3dhcm0tY2EwHhcNMTcwNTAyMDAyNDAwWhcNMzcwNDI3MDAy
NDAwWjATMREwDwYDVQQDEwhzd2FybS1jYTBZMBMGByqGSM49AgEGCCqGSM49AwEH
A0IABMbiAmET+HZyve35ujrnL2kOLBEQhFDZ5MhxAuYs96n796sFlfxTxC1lM/2g
Ah8DI34pm3JmHgZxeBPKUURJHKWjQjBAMA4GA1UdDwEB/wQEAwIBBjAPBgNVHRMB
Af8EBTADAQH/MB0GA1UdDgQWBBS3sjTJOcXdkls6WSY2rTx1KIJueTAKBggqhkjO
PQQDAgNJADBGAiEAoeVWkaXgSUAucQmZ3Yhmx22N/cq1EPBgYHOBZmHt0NkCIQC3
zONcJ/+WA21OXtb+vcijpUOXtNjyHfcox0N8wsLDqQ==
-----END CERTIFICATE-----

 Issuer Public Key: MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAExuICYRP4dnK97fm6OucvaQ4sERCEUNnkyHEC5iz3qfv3qwWV/FPELWUz/aACHwMjfimbcmYeBnF4E8pRREkcpQ==
 Issuer Subject:    MBMxETAPBgNVBAMTCHN3YXJtLWNh
```

---

# docker node ls

# docker node ls

| Description | List nodes in the swarm |
| --- | --- |
| Usage | docker node ls [OPTIONS] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker node list |

Swarm
This command works with the Swarm orchestrator.

## Description

Lists all the nodes that the Docker Swarm manager knows about. You can filter
using the `-f` or `--filter` flag. Refer to the [filtering](#filter) section
for more information about available filter options.

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

```console
$ docker node ls

ID                           HOSTNAME        STATUS  AVAILABILITY  MANAGER STATUS
1bcef6utixb0l0ca7gxuivsj0    swarm-worker2   Ready   Active
38ciaotwjuritcdtn9npbnkuz    swarm-worker1   Ready   Active
e216jshn25ckzbvmwlnh5jr3g *  swarm-manager1  Ready   Active        Leader
```

> Note
>
> In the above example output, there is a hidden column of `.Self` that indicates
> if the node is the same node as the current docker daemon. A `*` (e.g.,
> `e216jshn25ckzbvmwlnh5jr3g *`) means this node is the current docker daemon.

### Filtering (--filter)

The filtering flag (`-f` or `--filter`) format is of "key=value". If there is more
than one filter, then pass multiple flags (e.g., `--filter "foo=bar" --filter "bif=baz"`)

The currently supported filters are:

- [id](#id)
- [label](#label)
- [node.label](#nodelabel)
- [membership](#membership)
- [name](#name)
- [role](#role)

#### id

The `id` filter matches all or part of a node's id.

```console
$ docker node ls -f id=1

ID                         HOSTNAME       STATUS  AVAILABILITY  MANAGER STATUS
1bcef6utixb0l0ca7gxuivsj0  swarm-worker2  Ready   Active
```

#### label

The `label` filter matches nodes based on engine labels and on the presence of a
`label` alone or a `label` and a value. Engine labels are configured in
the
[daemon configuration](https://docs.docker.com/reference/cli/dockerd/#daemon-configuration-file). To filter on
Swarm `node` labels, use [node.labelinstead](#nodelabel).

The following filter matches nodes with the `foo` label regardless of its value.

```console
$ docker node ls -f "label=foo"

ID                         HOSTNAME       STATUS  AVAILABILITY  MANAGER STATUS
1bcef6utixb0l0ca7gxuivsj0  swarm-worker2  Ready   Active
```

#### node.label

The `node.label` filter matches nodes based on node labels and on the presence
of a `node.label` alone or a `node.label` and a value.

The following filter updates nodes to have a `region` node label:

```console
$ docker node update --label-add region=region-a swarm-test-01
$ docker node update --label-add region=region-a swarm-test-02
$ docker node update --label-add region=region-b swarm-test-03
$ docker node update --label-add region=region-b swarm-test-04
```

Show all nodes that have a `region` node label set:

```console
$ docker node ls --filter node.label=region

ID                            HOSTNAME        STATUS    AVAILABILITY   MANAGER STATUS   ENGINE VERSION
yg550ettvsjn6g6t840iaiwgb *   swarm-test-01   Ready     Active         Leader           23.0.3
2lm9w9kbepgvkzkkeyku40e65     swarm-test-02   Ready     Active         Reachable        23.0.3
hc0pu7ntc7s4uvj4pv7z7pz15     swarm-test-03   Ready     Active         Reachable        23.0.3
n41b2cijmhifxxvz56vwrs12q     swarm-test-04   Ready     Active                          23.0.3
```

Show all nodes that have a `region` node label, with value `region-a`:

```console
$ docker node ls --filter node.label=region=region-a

ID                            HOSTNAME        STATUS    AVAILABILITY   MANAGER STATUS   ENGINE VERSION
yg550ettvsjn6g6t840iaiwgb *   swarm-test-01   Ready     Active         Leader           23.0.3
2lm9w9kbepgvkzkkeyku40e65     swarm-test-02   Ready     Active         Reachable        23.0.3
```

#### membership

The `membership` filter matches nodes based on the presence of a `membership` and a value
`accepted` or `pending`.

The following filter matches nodes with the `membership` of `accepted`.

```console
$ docker node ls -f "membership=accepted"

ID                           HOSTNAME        STATUS  AVAILABILITY  MANAGER STATUS
1bcef6utixb0l0ca7gxuivsj0    swarm-worker2   Ready   Active
38ciaotwjuritcdtn9npbnkuz    swarm-worker1   Ready   Active
```

#### name

The `name` filter matches on all or part of a node hostname.

The following filter matches the nodes with a name equal to `swarm-master` string.

```console
$ docker node ls -f name=swarm-manager1

ID                           HOSTNAME        STATUS  AVAILABILITY  MANAGER STATUS
e216jshn25ckzbvmwlnh5jr3g *  swarm-manager1  Ready   Active        Leader
```

#### role

The `role` filter matches nodes based on the presence of a `role` and a value `worker` or `manager`.

The following filter matches nodes with the `manager` role.

```console
$ docker node ls -f "role=manager"

ID                           HOSTNAME        STATUS  AVAILABILITY  MANAGER STATUS
e216jshn25ckzbvmwlnh5jr3g *  swarm-manager1  Ready   Active        Leader
```

### Format the output (--format)

The formatting options (`--format`) pretty-prints nodes output
using a Go template.

Valid placeholders for the Go template are listed below:

| Placeholder | Description |
| --- | --- |
| .ID | Node ID |
| .Self | Node of the daemon (true/false,trueindicates that the node is the same as current docker daemon) |
| .Hostname | Node hostname |
| .Status | Node status |
| .Availability | Node availability ("active", "pause", or "drain") |
| .ManagerStatus | Manager status of the node |
| .TLSStatus | TLS status of the node ("Ready", or "Needs Rotation" has TLS certificate signed by an old CA) |
| .EngineVersion | Engine version |

When using the `--format` option, the `node ls` command will either
output the data exactly as the template declares or, when using the
`table` directive, includes column headers as well.

The following example uses a template without headers and outputs the
`ID`, `Hostname`, and `TLS Status` entries separated by a colon (`:`) for all
nodes:

```console
$ docker node ls --format "{{.ID}}: {{.Hostname}} {{.TLSStatus}}"

e216jshn25ckzbvmwlnh5jr3g: swarm-manager1 Ready
35o6tiywb700jesrt3dmllaza: swarm-worker1 Needs Rotation
```

To list all nodes in JSON format, use the `json` directive:

```console
$ docker node ls --format json
{"Availability":"Active","EngineVersion":"23.0.3","Hostname":"docker-desktop","ID":"k8f4w7qtzpj5sqzclcqafw35g","ManagerStatus":"Leader","Self":true,"Status":"Ready","TLSStatus":"Ready"}
```

---

# docker node promote

# docker node promote

| Description | Promote one or more nodes to manager in the swarm |
| --- | --- |
| Usage | docker node promote NODE [NODE...] |

Swarm
This command works with the Swarm orchestrator.

## Description

Promotes a node to manager. This command can only be executed on a manager node.

> Note
>
> This is a cluster management command, and must be executed on a swarm
> manager node. To learn about managers and workers, refer to the
> [Swarm mode section](https://docs.docker.com/engine/swarm/) in the
> documentation.

## Examples

```console
$ docker node promote <node name>
```

---

# docker node ps

# docker node ps

| Description | List tasks running on one or more nodes, defaults to current node |
| --- | --- |
| Usage | docker node ps [OPTIONS] [NODE...] |

Swarm
This command works with the Swarm orchestrator.

## Description

Lists all the tasks on a Node that Docker knows about. You can filter using the
`-f` or `--filter` flag. Refer to the [filtering](#filter) section for more
information about available filter options.

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

```console
$ docker node ps swarm-manager1

NAME                                IMAGE        NODE            DESIRED STATE  CURRENT STATE
redis.1.7q92v0nr1hcgts2amcjyqg3pq   redis:7.4.1  swarm-manager1  Running        Running 5 hours
redis.6.b465edgho06e318egmgjbqo4o   redis:7.4.1  swarm-manager1  Running        Running 29 seconds
redis.7.bg8c07zzg87di2mufeq51a2qp   redis:7.4.1  swarm-manager1  Running        Running 5 seconds
redis.9.dkkual96p4bb3s6b10r7coxxt   redis:7.4.1  swarm-manager1  Running        Running 5 seconds
redis.10.0tgctg8h8cech4w0k0gwrmr23  redis:7.4.1  swarm-manager1  Running        Running 5 seconds
```

### Filtering (--filter)

The filtering flag (`-f` or `--filter`) format is of "key=value". If there is
more than one filter, then pass multiple flags (e.g., `--filter "foo=bar" --filter "bif=baz"`).

The currently supported filters are:

- [name](#name)
- [id](#id)
- [label](#label)
- [desired-state](#desired-state)

#### name

The `name` filter matches on all or part of a task's name.

The following filter matches all tasks with a name containing the `redis` string.

```console
$ docker node ps -f name=redis swarm-manager1

NAME                                IMAGE        NODE            DESIRED STATE  CURRENT STATE
redis.1.7q92v0nr1hcgts2amcjyqg3pq   redis:7.4.1  swarm-manager1  Running        Running 5 hours
redis.6.b465edgho06e318egmgjbqo4o   redis:7.4.1  swarm-manager1  Running        Running 29 seconds
redis.7.bg8c07zzg87di2mufeq51a2qp   redis:7.4.1  swarm-manager1  Running        Running 5 seconds
redis.9.dkkual96p4bb3s6b10r7coxxt   redis:7.4.1  swarm-manager1  Running        Running 5 seconds
redis.10.0tgctg8h8cech4w0k0gwrmr23  redis:7.4.1  swarm-manager1  Running        Running 5 seconds
```

#### id

The `id` filter matches a task's id.

```console
$ docker node ps -f id=bg8c07zzg87di2mufeq51a2qp swarm-manager1

NAME                                IMAGE        NODE            DESIRED STATE  CURRENT STATE
redis.7.bg8c07zzg87di2mufeq51a2qp   redis:7.4.1  swarm-manager1  Running        Running 5 seconds
```

#### label

The `label` filter matches tasks based on the presence of a `label` alone or a `label` and a
value.

The following filter matches tasks with the `usage` label regardless of its value.

```console
$ docker node ps -f "label=usage"

NAME                               IMAGE        NODE            DESIRED STATE  CURRENT STATE
redis.6.b465edgho06e318egmgjbqo4o  redis:7.4.1  swarm-manager1  Running        Running 10 minutes
redis.7.bg8c07zzg87di2mufeq51a2qp  redis:7.4.1  swarm-manager1  Running        Running 9 minutes
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

When using the `--format` option, the `node ps` command will either
output the data exactly as the template declares or, when using the
`table` directive, includes column headers as well.

The following example uses a template without headers and outputs the
`Name` and `Image` entries separated by a colon (`:`) for all tasks:

```console
$ docker node ps --format "{{.Name}}: {{.Image}}"

top.1: busybox
top.2: busybox
top.3: busybox
```

---

# docker node rm

# docker node rm

| Description | Remove one or more nodes from the swarm |
| --- | --- |
| Usage | docker node rm [OPTIONS] NODE [NODE...] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker node remove |

Swarm
This command works with the Swarm orchestrator.

## Description

Removes the specified nodes from a swarm.

> Note
>
> This is a cluster management command, and must be executed on a swarm
> manager node. To learn about managers and workers, refer to the
> [Swarm mode section](https://docs.docker.com/engine/swarm/) in the
> documentation.

## Options

| Option | Default | Description |
| --- | --- | --- |
| -f, --force |  | Force remove a node from the swarm |

## Examples

### Remove a stopped node from the swarm

```console
$ docker node rm swarm-node-02

Node swarm-node-02 removed from swarm
```

### Attempt to remove a running node from a swarm

Removes the specified nodes from the swarm, but only if the nodes are in the
down state. If you attempt to remove an active node you will receive an error:

```console
$ docker node rm swarm-node-03

Error response from daemon: rpc error: code = 9 desc = node swarm-node-03 is not
down and can't be removed
```

### Forcibly remove an inaccessible node from a swarm (--force)

If you lose access to a worker node or need to shut it down because it has been
compromised or is not behaving as expected, you can use the `--force` option.
This may cause transient errors or interruptions, depending on the type of task
being run on the node.

```console
$ docker node rm --force swarm-node-03

Node swarm-node-03 removed from swarm
```

A manager node must be demoted to a worker node (using `docker node demote`)
before you can remove it from the swarm.
