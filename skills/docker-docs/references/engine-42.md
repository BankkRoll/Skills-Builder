# Manage nodes in a swarm and more

# Manage nodes in a swarm

> Manage existing nodes in a swarm

# Manage nodes in a swarm

   Table of contents

---

As part of the swarm management lifecycle, you may need to:

- [List nodes in the swarm](#list-nodes)
- [Inspect an individual node](#inspect-an-individual-node)
- [Update a node](#update-a-node)
- [Leave the swarm](#leave-the-swarm)

## List nodes

To view a list of nodes in the swarm run `docker node ls` from a manager node:

```console
$ docker node ls

ID                           HOSTNAME  STATUS  AVAILABILITY  MANAGER STATUS
46aqrk4e473hjbt745z53cr3t    node-5    Ready   Active        Reachable
61pi3d91s0w3b90ijw3deeb2q    node-4    Ready   Active        Reachable
a5b2m3oghd48m8eu391pefq5u    node-3    Ready   Active
e7p8btxeu3ioshyuj6lxiv6g0    node-2    Ready   Active
ehkv3bcimagdese79dn78otj5 *  node-1    Ready   Active        Leader
```

The `AVAILABILITY` column shows whether or not the scheduler can assign tasks to
the node:

- `Active` means that the scheduler can assign tasks to the node.
- `Pause` means the scheduler doesn't assign new tasks to the node, but existing
  tasks remain running.
- `Drain` means the scheduler doesn't assign new tasks to the node. The
  scheduler shuts down any existing tasks and schedules them on an available
  node.

The `MANAGER STATUS` column shows node participation in the Raft consensus:

- No value indicates a worker node that does not participate in swarm
  management.
- `Leader` means the node is the primary manager node that makes all swarm
  management and orchestration decisions for the swarm.
- `Reachable` means the node is a manager node participating in the Raft
  consensus quorum. If the leader node becomes unavailable, the node is eligible for
  election as the new leader.
- `Unavailable` means the node is a manager that can't communicate with
  other managers. If a manager node becomes unavailable, you should either join a
  new manager node to the swarm or promote a worker node to be a
  manager.

For more information on swarm administration refer to the [Swarm administration guide](https://docs.docker.com/engine/swarm/admin_guide/).

## Inspect an individual node

You can run `docker node inspect <NODE-ID>` on a manager node to view the
details for an individual node. The output defaults to JSON format, but you can
pass the `--pretty` flag to print the results in human-readable format. For example:

```console
$ docker node inspect self --pretty

ID:                     ehkv3bcimagdese79dn78otj5
Hostname:               node-1
Joined at:              2016-06-16 22:52:44.9910662 +0000 utc
Status:
 State:                 Ready
 Availability:          Active
Manager Status:
 Address:               172.17.0.2:2377
 Raft Status:           Reachable
 Leader:                Yes
Platform:
 Operating System:      linux
 Architecture:          x86_64
Resources:
 CPUs:                  2
 Memory:                1.954 GiB
Plugins:
  Network:              overlay, host, bridge, overlay, null
  Volume:               local
Engine Version:         1.12.0-dev
```

## Update a node

You can modify node attributes to:

- [Change node availability](#change-node-availability)
- [Add or remove label metadata](#add-or-remove-label-metadata)
- [Change a node role](#promote-or-demote-a-node)

### Change node availability

Changing node availability lets you:

- Drain a manager node so that it only performs swarm management tasks and is
  unavailable for task assignment.
- Drain a node so you can take it down for maintenance.
- Pause a node so it can't receive new tasks.
- Restore unavailable or paused nodes availability status.

For example, to change a manager node to `Drain` availability:

```console
$ docker node update --availability drain node-1

node-1
```

See [list nodes](#list-nodes) for descriptions of the different availability
options.

### Add or remove label metadata

Node labels provide a flexible method of node organization. You can also use
node labels in service constraints. Apply constraints when you create a service
to limit the nodes where the scheduler assigns tasks for the service.

Run `docker node update --label-add` on a manager node to add label metadata to
a node. The `--label-add` flag supports either a `<key>` or a `<key>=<value>`
pair.

Pass the `--label-add` flag once for each node label you want to add:

```console
$ docker node update --label-add foo --label-add bar=baz node-1

node-1
```

The labels you set for nodes using `docker node update` apply only to the node
entity within the swarm. Do not confuse them with the Docker daemon labels for
[dockerd](https://docs.docker.com/engine/manage-resources/labels/).

Therefore, node labels can be used to limit critical tasks to nodes that meet
certain requirements. For example, schedule only on machines where special
workloads should be run, such as machines that meet [PCI-SS
compliance](https://www.pcisecuritystandards.org/).

A compromised worker could not compromise these special workloads because it
cannot change node labels.

Engine labels, however, are still useful because some features that do not
affect secure orchestration of containers might be better off set in a
decentralized manner. For instance, an engine could have a label to indicate
that it has a certain type of disk device, which may not be relevant to security
directly. These labels are more easily "trusted" by the swarm orchestrator.

Refer to the `docker service create` [CLI reference](https://docs.docker.com/reference/cli/docker/service/create/)
for more information about service constraints.

### Promote or demote a node

You can promote a worker node to the manager role. This is useful when a
manager node becomes unavailable or if you want to take a manager offline for
maintenance. Similarly, you can demote a manager node to the worker role.

> Note
>
> Regardless of your reason to promote or demote
> a node, you must always maintain a quorum of manager nodes in the
> swarm. For more information refer to the [Swarm administration guide](https://docs.docker.com/engine/swarm/admin_guide/).

To promote a node or set of nodes, run `docker node promote` from a manager
node:

```console
$ docker node promote node-3 node-2

Node node-3 promoted to a manager in the swarm.
Node node-2 promoted to a manager in the swarm.
```

To demote a node or set of nodes, run `docker node demote` from a manager node:

```console
$ docker node demote node-3 node-2

Manager node-3 demoted in the swarm.
Manager node-2 demoted in the swarm.
```

`docker node promote` and `docker node demote` are convenience commands for
`docker node update --role manager` and `docker node update --role worker`
respectively.

## Install plugins on swarm nodes

If your swarm service relies on one or more
[plugins](https://docs.docker.com/engine/extend/plugin_api/), these plugins need to be available on
every node where the service could potentially be deployed. You can manually
install the plugin on each node or script the installation. You can also deploy
the plugin in a similar way as a global service using the Docker API, by specifying
a `PluginSpec` instead of a `ContainerSpec`.

> Note
>
> There is currently no way to deploy a plugin to a swarm using the
> Docker CLI or Docker Compose. In addition, it is not possible to install
> plugins from a private repository.

The
[PluginSpec](https://docs.docker.com/engine/extend/plugin_api/#json-specification)
is defined by the plugin developer. To add the plugin to all Docker nodes, use
the
[service/create](https://docs.docker.com/reference/api/engine/v1.31/#operation/ServiceCreate) API, passing
the `PluginSpec` JSON defined in the `TaskTemplate`.

## Leave the swarm

Run the `docker swarm leave` command on a node to remove it from the swarm.

For example to leave the swarm on a worker node:

```console
$ docker swarm leave

Node left the swarm.
```

When a node leaves the swarm, Docker Engine stops running in Swarm
mode. The orchestrator no longer schedules tasks to the node.

If the node is a manager node, you receive a warning about maintaining the
quorum. To override the warning, pass the `--force` flag. If the last manager
node leaves the swarm, the swarm becomes unavailable requiring you to take
disaster recovery measures.

For information about maintaining a quorum and disaster recovery, refer to the
[Swarm administration guide](https://docs.docker.com/engine/swarm/admin_guide/).

After a node leaves the swarm, you can run `docker node rm` on a
manager node to remove the node from the node list.

For instance:

```console
$ docker node rm node-2
```

## Learn more

- [Swarm administration guide](https://docs.docker.com/engine/swarm/admin_guide/)
- [Docker Engine command line reference](https://docs.docker.com/reference/cli/docker/)
- [Swarm mode tutorial](https://docs.docker.com/engine/swarm/swarm-tutorial/)

---

# Manage swarm service networks

> Use swarm mode overlay networking features

# Manage swarm service networks

   Table of contents

---

This page describes networking for swarm services.

## Swarm and types of traffic

A Docker swarm generates two different kinds of traffic:

- Control and management plane traffic: This includes swarm management
  messages, such as requests to join or leave the swarm. This traffic is
  always encrypted.
- Application data plane traffic: This includes container traffic and
  traffic to and from external clients.

## Key network concepts

The following three network concepts are important to swarm services:

- Overlay networks manage communications among the Docker daemons
  participating in the swarm. You can create overlay networks, in the same way
  as user-defined networks for standalone containers. You can attach a service
  to one or more existing overlay networks as well, to enable service-to-service
  communication. Overlay networks are Docker networks that use the `overlay`
  network driver.
- The ingress network is a special overlay network that facilitates
  load balancing among a service's nodes. When any swarm node receives a
  request on a published port, it hands that request off to a module called
  `IPVS`. `IPVS` keeps track of all the IP addresses participating in that
  service, selects one of them, and routes the request to it, over the
  `ingress` network.
  The `ingress` network is created automatically when you initialize or join a
  swarm. Most users do not need to customize its configuration, but Docker allows
  you to do so.
- The docker_gwbridge is a bridge network that connects the overlay
  networks (including the `ingress` network) to an individual Docker daemon's
  physical network. By default, each container a service is running is connected
  to its local Docker daemon host's `docker_gwbridge` network.
  The `docker_gwbridge` network is created automatically when you initialize or
  join a swarm. Most users do not need to customize its configuration, but
  Docker allows you to do so.

> Tip
>
> See also
> [Networking overview](https://docs.docker.com/engine/network/) for more details about Swarm networking in general.

## Firewall considerations

Docker daemons participating in a swarm need the ability to communicate with
each other over the following ports:

- Port `7946` TCP/UDP for container network discovery.
- Port `4789` UDP (configurable) for the overlay network (including ingress) data path.

When setting up networking in a Swarm, special care should be taken. Consult
the [tutorial](https://docs.docker.com/engine/swarm/swarm-tutorial/#open-protocols-and-ports-between-the-hosts)
for an overview.

## Overlay networking

When you initialize a swarm or join a Docker host to an existing swarm, two
new networks are created on that Docker host:

- An overlay network called `ingress`, which handles the control and data traffic
  related to swarm services. When you create a swarm service and do not
  connect it to a user-defined overlay network, it connects to the `ingress`
  network by default.
- A bridge network called `docker_gwbridge`, which connects the individual
  Docker daemon to the other daemons participating in the swarm.

### Create an overlay network

To create an overlay network, specify the `overlay` driver when using the
`docker network create` command:

```console
$ docker network create \
  --driver overlay \
  my-network
```

The above command doesn't specify any custom options, so Docker assigns a
subnet and uses default options. You can see information about the network using
`docker network inspect`.

When no containers are connected to the overlay network, its configuration is
not very exciting:

```console
$ docker network inspect my-network
[
    {
        "Name": "my-network",
        "Id": "fsf1dmx3i9q75an49z36jycxd",
        "Created": "0001-01-01T00:00:00Z",
        "Scope": "swarm",
        "Driver": "overlay",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": null,
            "Config": []
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "Containers": null,
        "Options": {
            "com.docker.network.driver.overlay.vxlanid_list": "4097"
        },
        "Labels": null
    }
]
```

In the above output, notice that the driver is `overlay` and that the scope is
`swarm`, rather than `local`, `host`, or `global` scopes you might see in
other types of Docker networks. This scope indicates that only hosts which are
participating in the swarm can access this network.

The network's subnet and gateway are dynamically configured when a service
connects to the network for the first time. The following example shows
the same network as above, but with three containers of a `redis` service
connected to it.

```console
$ docker network inspect my-network
[
    {
        "Name": "my-network",
        "Id": "fsf1dmx3i9q75an49z36jycxd",
        "Created": "2017-05-31T18:35:58.877628262Z",
        "Scope": "swarm",
        "Driver": "overlay",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": null,
            "Config": [
                {
                    "Subnet": "10.0.0.0/24",
                    "Gateway": "10.0.0.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "Containers": {
            "0e08442918814c2275c31321f877a47569ba3447498db10e25d234e47773756d": {
                "Name": "my-redis.1.ka6oo5cfmxbe6mq8qat2djgyj",
                "EndpointID": "950ce63a3ace13fe7ef40724afbdb297a50642b6d47f83a5ca8636d44039e1dd",
                "MacAddress": "02:42:0a:00:00:03",
                "IPv4Address": "10.0.0.3/24",
                "IPv6Address": ""
            },
            "88d55505c2a02632c1e0e42930bcde7e2fa6e3cce074507908dc4b827016b833": {
                "Name": "my-redis.2.s7vlybipal9xlmjfqnt6qwz5e",
                "EndpointID": "dd822cb68bcd4ae172e29c321ced70b731b9994eee5a4ad1d807d9ae80ecc365",
                "MacAddress": "02:42:0a:00:00:05",
                "IPv4Address": "10.0.0.5/24",
                "IPv6Address": ""
            },
            "9ed165407384f1276e5cfb0e065e7914adbf2658794fd861cfb9b991eddca754": {
                "Name": "my-redis.3.hbz3uk3hi5gb61xhxol27hl7d",
                "EndpointID": "f62c686a34c9f4d70a47b869576c37dffe5200732e1dd6609b488581634cf5d2",
                "MacAddress": "02:42:0a:00:00:04",
                "IPv4Address": "10.0.0.4/24",
                "IPv6Address": ""
            }
        },
        "Options": {
            "com.docker.network.driver.overlay.vxlanid_list": "4097"
        },
        "Labels": {},
        "Peers": [
            {
                "Name": "moby-e57c567e25e2",
                "IP": "192.168.65.2"
            }
        ]
    }
]
```

### Customize an overlay network

There may be situations where you don't want to use the default configuration
for an overlay network. For a full list of configurable options, run the
command `docker network create --help`. The following are some of the most
common options to change.

#### Configure the subnet and gateway

By default, the network's subnet and gateway are configured automatically when
the first service is connected to the network. You can configure these when
creating a network using the `--subnet` and `--gateway` flags. The following
example extends the previous one by configuring the subnet and gateway.

```console
$ docker network create \
  --driver overlay \
  --subnet 10.0.9.0/24 \
  --gateway 10.0.9.99 \
  my-network
```

##### Using custom default address pools

To customize subnet allocation for your Swarm networks, you can [optionally configure them](https://docs.docker.com/engine/swarm/swarm-mode/) during `swarm init`.

For example, the following command is used when initializing Swarm:

```console
$ docker swarm init --default-addr-pool 10.20.0.0/16 --default-addr-pool-mask-length 26
```

Whenever a user creates a network, but does not use the `--subnet` command line option, the subnet for this network will be allocated sequentially from the next available subnet from the pool. If the specified network is already allocated, that network will not be used for Swarm.

Multiple pools can be configured if discontiguous address space is required. However, allocation from specific pools is not supported. Network subnets will be allocated sequentially from the IP pool space and subnets will be reused as they are deallocated from networks that are deleted.

The default mask length can be configured and is the same for all networks. It is set to `/24` by default. To change the default subnet mask length, use the `--default-addr-pool-mask-length` command line option.

> Note
>
> Default address pools can only be configured on `swarm init` and cannot be altered after cluster creation.

##### Overlay network size limitations

Docker recommends creating overlay networks with `/24` blocks. The `/24` overlay network blocks limit the network to 256 IP addresses.

This recommendation addresses [limitations with swarm mode](https://github.com/moby/moby/issues/30820).
If you need more than 256 IP addresses, do not increase the IP block size. You can either use `dnsrr`
endpoint mode with an external load balancer, or use multiple smaller overlay networks. See
[Configure service discovery](#configure-service-discovery) for more information about different endpoint modes.

#### Configure encryption of application data

Management and control plane data related to a swarm is always encrypted.
For more details about the encryption mechanisms, see the
[Docker swarm mode overlay network security model](https://docs.docker.com/engine/network/drivers/overlay/).

Application data among swarm nodes is not encrypted by default. To encrypt this
traffic on a given overlay network, use the `--opt encrypted` flag on `docker network create`. This enables IPSEC encryption at the level of the vxlan. This
encryption imposes a non-negligible performance penalty, so you should test this
option before using it in production.

> Note
>
> You must [customize the automatically created ingress](#customize-ingress)
> to enable encryption. By default, all ingress traffic is unencrypted, as encryption
> is a network-level option.

## Attach a service to an overlay network

To attach a service to an existing overlay network, pass the `--network` flag to
`docker service create`, or the `--network-add` flag to `docker service update`.

```console
$ docker service create \
  --replicas 3 \
  --name my-web \
  --network my-network \
  nginx
```

Service containers connected to an overlay network can communicate with
each other across it.

To see which networks a service is connected to, use `docker service ls` to find
the name of the service, then `docker service ps <service-name>` to list the
networks. Alternately, to see which services' containers are connected to a
network, use `docker network inspect <network-name>`. You can run these commands
from any swarm node which is joined to the swarm and is in a `running` state.

### Configure service discovery

Service discovery is the mechanism Docker uses to route a request from your
service's external clients to an individual swarm node, without the client
needing to know how many nodes are participating in the service or their
IP addresses or ports. You don't need to publish ports which are used between
services on the same network. For instance, if you have a
[WordPress service that stores its data in a MySQL service](https://training.play-with-docker.com/swarm-service-discovery/),
and they are connected to the same overlay network, you do not need to publish
the MySQL port to the client, only the WordPress HTTP port.

Service discovery can work in two different ways: internal connection-based
load-balancing at Layers 3 and 4 using the embedded DNS and a virtual IP (VIP),
or external and customized request-based load-balancing at Layer 7 using DNS
round robin (DNSRR). You can configure this per service.

- By default, when you attach a service to a network and that service publishes
  one or more ports, Docker assigns the service a virtual IP (VIP), which is the
  "front end" for clients to reach the service. Docker keeps a list of all
  worker nodes in the service, and routes requests between the client and one of
  the nodes. Each request from the client might be routed to a different node.
- If you configure a service to use DNS round-robin (DNSRR) service discovery,
  there is not a single virtual IP. Instead, Docker sets up DNS entries for the
  service such that a DNS query for the service name returns a list of IP
  addresses, and the client connects directly to one of these.
  DNS round-robin is useful in cases where you want to use your own load
  balancer, such as HAProxy. To configure a service to use DNSRR, use the flag
  `--endpoint-mode dnsrr` when creating a new service or updating an existing
  one.

## Customize the ingress network

Most users never need to configure the `ingress` network, but Docker allows you
to do so. This can be useful if the automatically-chosen subnet
conflicts with one that already exists on your network, or you need to customize
other low-level network settings such as the MTU, or if you want to
[enable encryption](#encryption).

Customizing the `ingress` network involves removing and recreating it. This is
usually done before you create any services in the swarm. If you have existing
services which publish ports, those services need to be removed before you can
remove the `ingress` network.

During the time that no `ingress` network exists, existing services which do not
publish ports continue to function but are not load-balanced. This affects
services which publish ports, such as a WordPress service which publishes port
80.

1. Inspect the `ingress` network using `docker network inspect ingress`, and
  remove any services whose containers are connected to it. These are services
  that publish ports, such as a WordPress service which publishes port 80. If
  all such services are not stopped, the next step fails.
2. Remove the existing `ingress` network:
  ```console
  $ docker network rm ingress
  WARNING! Before removing the routing-mesh network, make sure all the nodes
  in your swarm run the same docker engine version. Otherwise, removal may not
  be effective and functionality of newly created ingress networks will be
  impaired.
  Are you sure you want to continue? [y/N]
  ```
3. Create a new overlay network using the `--ingress` flag, along with the
  custom options you want to set. This example sets the MTU to 1200, sets
  the subnet to `10.11.0.0/16`, and sets the gateway to `10.11.0.2`.
  ```console
  $ docker network create \
    --driver overlay \
    --ingress \
    --subnet=10.11.0.0/16 \
    --gateway=10.11.0.2 \
    --opt com.docker.network.driver.mtu=1200 \
    my-ingress
  ```
  > Note
  >
  > You can name your `ingress` network something other than
  > `ingress`, but you can only have one. An attempt to create a second one
  > fails.
4. Restart the services that you stopped in the first step.

## Customize the docker_gwbridge

The `docker_gwbridge` is a virtual bridge that connects the overlay networks
(including the `ingress` network) to an individual Docker daemon's physical
network. Docker creates it automatically when you initialize a swarm or join a
Docker host to a swarm, but it is not a Docker device. It exists in the kernel
of the Docker host. If you need to customize its settings, you must do so before
joining the Docker host to the swarm, or after temporarily removing the host
from the swarm.

You need to have the `brctl` application installed on your operating system in
order to delete an existing bridge. The package name is `bridge-utils`.

1. Stop Docker.
2. Use the `brctl show docker_gwbridge` command to check whether a bridge
  device exists called `docker_gwbridge`. If so, remove it using
  `brctl delbr docker_gwbridge`.
3. Start Docker. Do not join or initialize the swarm.
4. Create or re-create the `docker_gwbridge` bridge with your custom settings.
  This example uses the subnet `10.11.0.0/16`. For a full list of customizable
  options, see
  [Bridge driver options](https://docs.docker.com/reference/cli/docker/network/create/#bridge-driver-options).
  ```console
  $ docker network create \
  --subnet 10.11.0.0/16 \
  --opt com.docker.network.bridge.name=docker_gwbridge \
  --opt com.docker.network.bridge.enable_icc=false \
  --opt com.docker.network.bridge.enable_ip_masquerade=true \
  docker_gwbridge
  ```
5. Initialize or join the swarm.

## Use a separate interface for control and data traffic

By default, all swarm traffic is sent over the same interface, including control
and management traffic for maintaining the swarm itself and data traffic to and
from the service containers.

You can separate this traffic by passing
the `--data-path-addr` flag when initializing or joining the swarm. If there are
multiple interfaces, `--advertise-addr` must be specified explicitly, and
`--data-path-addr` defaults to `--advertise-addr` if not specified. Traffic about
joining, leaving, and managing the swarm is sent over the
`--advertise-addr` interface, and traffic among a service's containers is sent
over the `--data-path-addr` interface. These flags can take an IP address or
a network device name, such as `eth0`.

This example initializes a swarm with a separate `--data-path-addr`. It assumes
that your Docker host has two different network interfaces: 10.0.0.1 should be
used for control and management traffic and 192.168.0.1 should be used for
traffic relating to services.

```console
$ docker swarm init --advertise-addr 10.0.0.1 --data-path-addr 192.168.0.1
```

This example joins the swarm managed by host `192.168.99.100:2377` and sets the
`--advertise-addr` flag to `eth0` and the `--data-path-addr` flag to `eth1`.

```console
$ docker swarm join \
  --token SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2d7c \
  --advertise-addr eth0 \
  --data-path-addr eth1 \
  192.168.99.100:2377
```

## Publish ports on an overlay network

Swarm services connected to the same overlay network effectively expose all
ports to each other. For a port to be accessible outside of the service, that
port must be *published* using the `-p` or `--publish` flag on `docker service create` or `docker service update`. Both the legacy colon-separated syntax and
the newer comma-separated value syntax are supported. The longer syntax is
preferred because it is somewhat self-documenting.

| Flag value | Description |
| --- | --- |
| -p 8080:80or-p published=8080,target=80 | Map TCP port 80 on the service to port 8080 on the routing mesh. |
| -p 8080:80/udpor-p published=8080,target=80,protocol=udp | Map UDP port 80 on the service to port 8080 on the routing mesh. |
| -p 8080:80/tcp -p 8080:80/udpor-p published=8080,target=80,protocol=tcp -p published=8080,target=80,protocol=udp | Map TCP port 80 on the service to TCP port 8080 on the routing mesh, and map UDP port 80 on the service to UDP port 8080 on the routing mesh. |

## Learn more

- [Deploy services to a swarm](https://docs.docker.com/engine/swarm/services/)
- [Swarm administration guide](https://docs.docker.com/engine/swarm/admin_guide/)
- [Swarm mode tutorial](https://docs.docker.com/engine/swarm/swarm-tutorial/)
- [Networking overview](https://docs.docker.com/engine/network/)
- [Docker CLI reference](https://docs.docker.com/reference/cli/docker/)

---

# Raft consensus in swarm mode

> Raft consensus algorithm in swarm mode

# Raft consensus in swarm mode

---

When Docker Engine runs in Swarm mode, manager nodes implement the
[Raft Consensus Algorithm](http://thesecretlivesofdata.com/raft/) to manage the global cluster state.

The reason why Swarm mode is using a consensus algorithm is to make sure that
all the manager nodes that are in charge of managing and scheduling tasks in the cluster
are storing the same consistent state.

Having the same consistent state across the cluster means that in case of a failure,
any Manager node can pick up the tasks and restore the services to a stable state.
For example, if the Leader Manager which is responsible for scheduling tasks in the
cluster dies unexpectedly, any other Manager can pick up the task of scheduling and
re-balance tasks to match the desired state.

Systems using consensus algorithms to replicate logs in a distributed systems
do require special care. They ensure that the cluster state stays consistent
in the presence of failures by requiring a majority of nodes to agree on values.

Raft tolerates up to `(N-1)/2` failures and requires a majority or quorum of
`(N/2)+1` members to agree on values proposed to the cluster. This means that in
a cluster of 5 Managers running Raft, if 3 nodes are unavailable, the system
cannot process any more requests to schedule additional tasks. The existing
tasks keep running but the scheduler cannot rebalance tasks to
cope with failures if the manager set is not healthy.

The implementation of the consensus algorithm in Swarm mode means it features
the properties inherent to distributed systems:

- Agreement on values in a fault tolerant system. (Refer to [FLP impossibility theorem](https://www.the-paper-trail.org/post/2008-08-13-a-brief-tour-of-flp-impossibility/)
  and the [Raft Consensus Algorithm paper](https://www.usenix.org/system/files/conference/atc14/atc14-paper-ongaro.pdf))
- Mutual exclusion through the leader election process
- Cluster membership management
- Globally consistent object sequencing and CAS (compare-and-swap) primitives
