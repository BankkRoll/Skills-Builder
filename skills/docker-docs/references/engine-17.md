# Overlay network driver and more

# Overlay network driver

> All about using overlay networks

# Overlay network driver

   Table of contents

---

The `overlay` network driver creates a distributed network among multiple
Docker daemon hosts. This network sits on top of (overlays) the host-specific
networks, allowing containers connected to it to communicate securely when
encryption is enabled. Docker transparently handles routing of each packet to
and from the correct Docker daemon host and the correct destination container.

You can create user-defined `overlay` networks using `docker network create`,
in the same way that you can create user-defined `bridge` networks. Services
or containers can be connected to more than one network at a time. Services or
containers can only communicate across networks they're each connected to.

Overlay networks are often used to create a connection between Swarm services,
but you can also use it to connect standalone containers running on different
hosts. When using standalone containers, it's still required that you use
Swarm mode to establish a connection between the hosts.

This page describes overlay networks in general, and when used with standalone
containers. For information about overlay for Swarm services, see
[Manage Swarm service networks](https://docs.docker.com/engine/swarm/networking/).

## Requirements

Docker hosts must be part of a swarm to use overlay networks, even when
connecting standalone containers. The following ports must be open between
participating hosts:

- `2377/tcp`: Swarm control plane (configurable)
- `4789/udp`: Overlay traffic (configurable)
- `7946/tcp` and `7946/udp`: Node communication (not configurable)

## Create an overlay network

The following table lists the ports that need to be open to each host
participating in an overlay network:

| Ports | Description |
| --- | --- |
| 2377/tcp | The default Swarm control plane port, is configurable withdocker swarm join --listen-addr |
| 4789/udp | The default overlay traffic port, configurable withdocker swarm init --data-path-addr |
| 7946/tcp,7946/udp | Used for communication among nodes, not configurable |

To create an overlay network that containers on other Docker hosts can connect to,
run the following command:

```console
$ docker network create -d overlay --attachable my-attachable-overlay
```

The `--attachable` option enables both standalone containers
and Swarm services to connect to the overlay network.
Without `--attachable`, only Swarm services can connect to the network.

You can specify the IP address range, subnet, gateway, and other options. See
`docker network create --help` for details.

## Encrypt traffic on an overlay network

Use the `--opt encrypted` flag to encrypt the application data
transmitted over the overlay network:

```console
$ docker network create \
  --opt encrypted \
  --driver overlay \
  --attachable \
  my-attachable-multi-host-network
```

This enables IPsec encryption at the level of the Virtual Extensible LAN (VXLAN).
This encryption imposes a non-negligible performance penalty,
so you should test this option before using it in production.

> Warning
>
> Don't attach Windows containers to encrypted overlay networks.
>
>
>
> Overlay network encryption isn't supported on Windows.
> Swarm doesn't report an error when a Windows host
> attempts to connect to an encrypted overlay network,
> but networking for the Windows containers is affected as follows:
>
>
>
> - Windows containers can't communicate with Linux containers on the network
> - Data traffic between Windows containers on the network isn't encrypted

## Attach a container to an overlay network

Adding containers to an overlay network gives them the ability to communicate
with other containers without having to set up routing on the individual Docker
daemon hosts. A prerequisite for doing this is that the hosts have joined the same Swarm.

To join an overlay network named `multi-host-network` with a `busybox` container:

```console
$ docker run --network multi-host-network busybox sh
```

> Note
>
> This only works if the overlay network is attachable
> (created with the `--attachable` flag).

## Container discovery

Publishing ports of a container on an overlay network opens the ports to other
containers on the same network. Containers are discoverable by doing a DNS lookup
using the container name.

| Flag value | Description |
| --- | --- |
| -p 8080:80 | Map TCP port 80 in the container to port8080on the overlay network. |
| -p 8080:80/udp | Map UDP port 80 in the container to port8080on the overlay network. |
| -p 8080:80/sctp | Map SCTP port 80 in the container to port8080on the overlay network. |
| -p 8080:80/tcp -p 8080:80/udp | Map TCP port 80 in the container to TCP port8080on the overlay network, and map UDP port 80 in the container to UDP port8080on the overlay network. |

## Connection limit for overlay networks

Due to limitations set by the Linux kernel, overlay networks become unstable and
inter-container communications may break when 1000 containers are co-located on
the same host.

For more information about this limitation, see
[moby/moby#44973](https://github.com/moby/moby/issues/44973#issuecomment-1543747718).

## Usage examples

This section provides hands-on examples for working with overlay networks. These
examples cover swarm services and standalone containers on multiple Docker hosts.

### Prerequisites

All examples require at least a single-node swarm. Initialize one by running
`docker swarm init` on the host. You can run these examples on multi-node
swarms as well.

### Use the default overlay network

This example shows how the default overlay network works with swarm services.
You'll create an `nginx` service and examine the network from the service
containers' perspective.

#### Prerequisites for multi-node setup

This walkthrough requires three Docker hosts that can communicate with each
other on the same network with no firewall blocking traffic between them:

- `manager`: Functions as both manager and worker
- `worker-1`: Functions as worker only
- `worker-2`: Functions as worker only

If you don't have three hosts available, you can set up three virtual machines
on a cloud provider with Docker installed.

#### Create the swarm

1. On `manager`, initialize the swarm. If the host has one network interface,
  the `--advertise-addr` flag is optional:
  ```console
  $ docker swarm init --advertise-addr=<IP-ADDRESS-OF-MANAGER>
  ```
  Save the join token displayed for use with workers.
2. On `worker-1`, join the swarm:
  ```console
  $ docker swarm join --token TOKEN \
    --advertise-addr <IP-ADDRESS-OF-WORKER-1> \
    <IP-ADDRESS-OF-MANAGER>:2377
  ```
3. On `worker-2`, join the swarm:
  ```console
  $ docker swarm join --token TOKEN \
    --advertise-addr <IP-ADDRESS-OF-WORKER-2> \
    <IP-ADDRESS-OF-MANAGER>:2377
  ```
4. On `manager`, list all nodes:
  ```console
  $ docker node ls
  ID                            HOSTNAME            STATUS              AVAILABILITY        MANAGER STATUS
  d68ace5iraw6whp7llvgjpu48 *   ip-172-31-34-146    Ready               Active              Leader
  nvp5rwavvb8lhdggo8fcf7plg     ip-172-31-35-151    Ready               Active
  ouvx2l7qfcxisoyms8mtkgahw     ip-172-31-36-89     Ready               Active
  ```
  Filter by role if needed:
  ```console
  $ docker node ls --filter role=manager
  $ docker node ls --filter role=worker
  ```
5. List Docker networks on all hosts. Each now has an overlay network called
  `ingress` and a bridge network called `docker_gwbridge`:
  ```console
  $ docker network ls
  NETWORK ID          NAME                DRIVER              SCOPE
  495c570066be        bridge              bridge              local
  961c6cae9945        docker_gwbridge     bridge              local
  ff35ceda3643        host                host                local
  trtnl4tqnc3n        ingress             overlay             swarm
  c8357deec9cb        none                null                local
  ```

The `docker_gwbridge` connects the `ingress` network to the Docker host's
network interface. If you create services without specifying a network, they
connect to `ingress`. It's recommended to use separate overlay networks for each
application or group of related applications.

#### Create the services

1. On `manager`, create a new overlay network:
  ```console
  $ docker network create -d overlay nginx-net
  ```
  The overlay network is automatically created on worker nodes when they run
  service tasks that need it.
2. On `manager`, create a 5-replica Nginx service connected to `nginx-net`:
  > Note
  >
  > Services can only be created on a manager.
  ```console
  $ docker service create \
    --name my-nginx \
    --publish target=80,published=80 \
    --replicas=5 \
    --network nginx-net \
    nginx
  ```
  The default `ingress` publish mode means you can browse to port 80 on any
  node and connect to one of the 5 service tasks, even if no tasks run on that
  node.
3. Monitor service creation progress:
  ```console
  $ docker service ls
  ```
4. Inspect the `nginx-net` network on all hosts. The `Containers` section lists
  all service tasks connected to the overlay network from that host.
5. From `manager`, inspect the service:
  ```console
  $ docker service inspect my-nginx
  ```
  Notice the information about ports and endpoints.
6. Create a second network and update the service to use it:
  ```console
  $ docker network create -d overlay nginx-net-2
  $ docker service update \
    --network-add nginx-net-2 \
    --network-rm nginx-net \
    my-nginx
  ```
7. Verify the update completed:
  ```console
  $ docker service ls
  ```
  Inspect both networks to verify containers moved from `nginx-net` to
  `nginx-net-2`.
  > Note
  >
  > Overlay networks are automatically created on swarm worker nodes as needed,
  > but aren't automatically removed.
8. Clean up:
  ```console
  $ docker service rm my-nginx
  $ docker network rm nginx-net nginx-net-2
  ```

### Use a user-defined overlay network

This example shows the recommended approach for production services using custom
overlay networks.

#### Prerequisites

This assumes the swarm is already set up and you're on a manager node.

#### Steps

1. Create a user-defined overlay network:
  ```console
  $ docker network create -d overlay my-overlay
  ```
2. Start a service using the overlay network, publishing port 80 to port 8080:
  ```console
  $ docker service create \
    --name my-nginx \
    --network my-overlay \
    --replicas 1 \
    --publish published=8080,target=80 \
    nginx:latest
  ```
3. Verify the service task is connected to the network:
  ```console
  $ docker network inspect my-overlay
  ```
  Check the `Containers` section for the `my-nginx` service task.
4. Clean up:
  ```console
  $ docker service rm my-nginx
  $ docker network rm my-overlay
  ```

### Use an overlay network for standalone containers

This example demonstrates DNS container discovery between standalone containers
on different Docker hosts using an overlay network.

#### Prerequisites

You need two Docker hosts that can communicate with each other with the
following ports open between them:

- TCP port 2377
- TCP and UDP port 7946
- UDP port 4789

This example refers to the hosts as `host1` and `host2`.

#### Steps

1. Set up the swarm:
  On `host1`, initialize a swarm:
  ```console
  $ docker swarm init
  Swarm initialized: current node (vz1mm9am11qcmo979tlrlox42) is now a manager.
  To add a worker to this swarm, run the following command:
      docker swarm join --token SWMTKN-1-5g90q48weqrtqryq4kj6ow0e8xm9wmv9o6vgqc5j320ymybd5c-8ex8j0bc40s6hgvy5ui5gl4gy 172.31.47.252:2377
  ```
  On `host2`, join the swarm using the token from the previous output:
  ```console
  $ docker swarm join --token <your_token> <your_ip_address>:2377
  This node joined a swarm as a worker.
  ```
  If the join fails, run `docker swarm leave --force` on `host2`, verify
  network and firewall settings, and try again.
2. On `host1`, create an attachable overlay network:
  ```console
  $ docker network create --driver=overlay --attachable test-net
  uqsof8phj3ak0rq9k86zta6ht
  ```
  Note the returned network ID.
3. On `host1`, start an interactive container that connects to `test-net`:
  ```console
  $ docker run -it --name alpine1 --network test-net alpine
  / #
  ```
4. On `host2`, list available networks. Notice that `test-net` doesn't exist yet:
  ```console
  $ docker network ls
  NETWORK ID          NAME                DRIVER              SCOPE
  ec299350b504        bridge              bridge              local
  66e77d0d0e9a        docker_gwbridge     bridge              local
  9f6ae26ccb82        host                host                local
  omvdxqrda80z        ingress             overlay             swarm
  b65c952a4b2b        none                null                local
  ```
5. On `host2`, start a detached, interactive container that connects to
  `test-net`:
  ```console
  $ docker run -dit --name alpine2 --network test-net alpine
  fb635f5ece59563e7b8b99556f816d24e6949a5f6a5b1fbd92ca244db17a4342
  ```
  > Note
  >
  > Automatic DNS container discovery only works with unique container names.
6. On `host2`, verify that `test-net` was created with the same network ID as on
  `host1`:
  ```console
  $ docker network ls
  NETWORK ID          NAME                DRIVER              SCOPE
  ...
  uqsof8phj3ak        test-net            overlay             swarm
  ```
7. On `host1`, ping `alpine2` from within `alpine1`:
  ```console
  / # ping -c 2 alpine2
  PING alpine2 (10.0.0.5): 56 data bytes
  64 bytes from 10.0.0.5: seq=0 ttl=64 time=0.600 ms
  64 bytes from 10.0.0.5: seq=1 ttl=64 time=0.555 ms
  --- alpine2 ping statistics ---
  2 packets transmitted, 2 packets received, 0% packet loss
  round-trip min/avg/max = 0.555/0.577/0.600 ms
  ```
  The two containers communicate over the overlay network connecting the two
  hosts. You can also run another container on `host2` and ping `alpine1`:
  ```console
  $ docker run -it --rm --name alpine3 --network test-net alpine
  / # ping -c 2 alpine1
  / # exit
  ```
8. On `host1`, close the `alpine1` session (which stops the container):
  ```console
  / # exit
  ```
9. Clean up. You must stop and remove containers on each host independently:
  On `host2`:
  ```console
  $ docker container stop alpine2
  $ docker network ls
  $ docker container rm alpine2
  ```
  When you stop `alpine2`, `test-net` disappears from `host2`.
  On `host1`:
  ```console
  $ docker container rm alpine1
  $ docker network rm test-net
  ```

## Next steps

- Learn about [networking from the container's point of view](https://docs.docker.com/engine/network/)
- Learn about [standalone bridge networks](https://docs.docker.com/engine/network/drivers/bridge/)
- Learn about [Macvlan networks](https://docs.docker.com/engine/network/drivers/macvlan/)

---

# Network drivers

> Learn the basics of Docker network drivers

# Network drivers

   Table of contents

---

Docker's networking subsystem is pluggable, using drivers. Several drivers
exist by default, and provide core networking functionality:

- `bridge`: The default network driver. If you don't specify a driver, this is
  the type of network you are creating. Bridge networks are commonly used when
  your application runs in a container that needs to communicate with other
  containers on the same host.
  See [Bridge network driver](https://docs.docker.com/engine/network/drivers/bridge/).
- `host`: Remove network isolation between the container and the Docker host,
  and use the host's networking directly.
  See [Host network driver](https://docs.docker.com/engine/network/drivers/host/).
- `overlay`: Overlay networks connect multiple Docker daemons together and
  enable Swarm services and containers to communicate across nodes. This
  strategy removes the need to do OS-level routing.
  See [Overlay network driver](https://docs.docker.com/engine/network/drivers/overlay/).
- `ipvlan`: IPvlan networks give users total control over both IPv4 and IPv6
  addressing. The VLAN driver builds on top of that in giving operators complete
  control of layer 2 VLAN tagging and even IPvlan L3 routing for users
  interested in underlay network integration.
  See [IPvlan network driver](https://docs.docker.com/engine/network/drivers/ipvlan/).
- `macvlan`: Macvlan networks allow you to assign a MAC address to a container,
  making it appear as a physical device on your network. The Docker daemon
  routes traffic to containers by their MAC addresses. Using the `macvlan`
  driver is sometimes the best choice when dealing with legacy applications that
  expect to be directly connected to the physical network, rather than routed
  through the Docker host's network stack.
  See [Macvlan network driver](https://docs.docker.com/engine/network/drivers/macvlan/).
- `none`: Completely isolate a container from the host and other containers.
  `none` is not available for Swarm services.
  See [None network driver](https://docs.docker.com/engine/network/drivers/none/).
- [Network plugins](https://docs.docker.com/engine/extend/plugins_network/): You can install and use
  third-party network plugins with Docker.

### Network driver summary

- The default bridge network is good for running containers that don't require
  special networking capabilities.
- User-defined bridge networks enable containers on the same Docker host to
  communicate with each other. A user-defined network typically defines an
  isolated network for multiple containers belonging to a common project or
  component.
- Host network shares the host's network with the container. When you use this
  driver, the container's network isn't isolated from the host.
- Overlay networks are best when you need containers running on different
  Docker hosts to communicate, or when multiple applications work together
  using Swarm services.
- Macvlan networks are best when you are migrating from a VM setup or need your
  containers to look like physical hosts on your network, each with a unique
  MAC address.
- IPvlan is similar to Macvlan, but doesn't assign unique MAC addresses to
  containers. Consider using IPvlan when there's a restriction on the number of
  MAC addresses that can be assigned to a network interface or port.
- Third-party network plugins allow you to integrate Docker with specialized
  network stacks.

## Next steps

Each driver page includes detailed explanations, configuration options, and
hands-on usage examples to help you work with that driver effectively.

---

# Docker with iptables

> How Docker works with iptables

# Docker with iptables

   Table of contents

---

Docker creates iptables rules in the host's network namespace for bridge
networks. For bridge and other network types, iptables rules for DNS are
also created in the container's network namespace.

Creation of iptables rules can be disabled using daemon options `iptables`
and `ip6tables`, see [Prevent Docker from manipulating firewall rules](https://docs.docker.com/engine/network/packet-filtering-firewalls/#prevent-docker-from-manipulating-firewall-rules).
However, this is not recommended for most users as it will likely break
container networking.

### Docker and iptables chains

To support bridge and overlay networks, Docker creates the following custom
`iptables` chains in the `filter` table:

- `DOCKER-USER`
  - A placeholder for user-defined rules that will be processed before rules
    in the `DOCKER-FORWARD` and `DOCKER` chains.
- `DOCKER-FORWARD`
  - The first stage of processing for Docker's networks. Rules that pass packets
    that are not related to established connections to the other Docker chains,
    as well as rules to accept packets that are part of established connections.
- `DOCKER`, `DOCKER-BRIDGE`, `DOCKER-INTERNAL`
  - Rules that determine whether a packet that is not part of an established
    connection should be accepted, based on the port forwarding configuration
    of running containers.
- `DOCKER-CT`
  - Per-bridge connection tracking rules.
- `DOCKER-INGRESS`
  - Rules related to Swarm networking.

In the `FORWARD` chain, Docker adds rules that unconditionally jump to the
`DOCKER-USER`, `DOCKER-FORWARD` and `DOCKER-INGRESS` chains.

In the `nat` table, Docker creates chain `DOCKER` and adds rules to implement
masquerading and port-mapping.

Docker requires IP Forwarding to be enabled on the host for its default
bridge network configuration. If it enables IP Forwarding, it also sets the
default policy of the iptables `FORWARD` chain in the `filter` table to `DROP`.

### Add iptables policies before Docker's rules

Packets that get accepted or rejected by rules in these custom chains will not
be seen by user-defined rules appended to the `FORWARD` chain. So, to add
additional rules to filter these packets, use the `DOCKER-USER` chain.

Rules appended to the `FORWARD` chain will be processed after Docker's rules.

### Match the original IP and ports for requests

When packets arrive to the `DOCKER-USER` chain, they have already passed through
a Destination Network Address Translation (DNAT) filter. That means that the
`iptables` flags you use can only match internal IP addresses and ports of
containers.

If you want to match traffic based on the original IP and port in the network
request, you must use the
[conntrackiptables extension](https://ipset.netfilter.org/iptables-extensions.man.html#lbAO).
For example:

```console
$ sudo iptables -I DOCKER-USER -p tcp -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
$ sudo iptables -I DOCKER-USER -p tcp -m conntrack --ctorigdst 198.51.100.2 --ctorigdstport 80 -j ACCEPT
```

> Important
>
> Using the `conntrack` extension may result in degraded performance.

### Allow forwarding between host interfaces

If Docker has set the default policy of the `FORWARD` chain in the `filter`
table to `DROP`, a rule in `DOCKER-USER` can be used to allow forwarding
between host interfaces. For example:

```console
$ iptables -I DOCKER-USER -i src_if -o dst_if -j ACCEPT
```

### Restrict external connections to containers

By default, all external source IPs are allowed to connect to ports that have
been published to the Docker host's addresses.

To allow only a specific IP or network to access the containers, insert a
negated rule at the top of the `DOCKER-USER` filter chain. For example, the
following rule drops packets from all IP addresses except `192.0.2.2`:

```console
$ iptables -I DOCKER-USER -i ext_if ! -s 192.0.2.2 -j DROP
```

You will need to change `ext_if` to correspond with your
host's actual external interface. You could instead allow connections from a
source subnet. The following rule only allows access from the subnet `192.0.2.0/24`:

```console
$ iptables -I DOCKER-USER -i ext_if ! -s 192.0.2.0/24 -j DROP
```

Finally, you can specify a range of IP addresses to accept using `--src-range`
(Remember to also add `-m iprange` when using `--src-range` or `--dst-range`):

```console
$ iptables -I DOCKER-USER -m iprange -i ext_if ! --src-range 192.0.2.1-192.0.2.3 -j DROP
```

You can combine `-s` or `--src-range` with `-d` or `--dst-range` to control both
the source and destination. For example, if the Docker host has addresses
`2001:db8:1111::2` and `2001:db8:2222::2`, you can make rules specific to
`2001:db8:1111::2` and leave `2001:db8:2222::2` open.

You may need to allow responses from servers outside the permitted external address
ranges. For example, containers may send DNS or HTTP requests to hosts that are
not allowed to access the container's services. The following rule accepts any
incoming or outgoing packet belonging to a flow that has already been accepted
by other rules. It must be placed before `DROP` rules that restrict access from
external address ranges.

```console
$ iptables -I DOCKER-USER -m state --state RELATED,ESTABLISHED -j ACCEPT
```

For more information about iptables configuration and advanced usage,
refer to the [Netfilter.org HOWTO](https://www.netfilter.org/documentation/HOWTO/NAT-HOWTO.html).

---

# Docker with nftables

> How Docker works with nftables

# Docker with nftables

   Table of contents

---

> Warning
>
> Support for nftables introduced in Docker 29.0.0 is experimental, configuration
> options, behavior and implementation may all change in future releases.
> The rules for overlay networks have not yet been migrated from iptables.
> Therefore, nftables cannot be enabled when the Docker daemon is running in
> Swarm mode.

To use nftables instead of iptables, use Docker Engine option
`--firewall-backend=nftables` on its command line, or `"firewall-backend": "nftables"`
in its configuration file. You may also need to modify IP forwarding configuration
on the host, and migrate rules from the iptables `DOCKER-USER` chain, see
[migrating from iptables to nftables](#migrating-from-iptables-to-nftables).

For bridge networks, Docker creates nftables rules in the host's network
namespace. For bridge and other network types, nftables rules for DNS are
also created in the container's network namespace.

Creation of nftables rules can be disabled using daemon options `iptables`
and `ip6tables`. *These options apply to both iptables and nftables.*
See [Prevent Docker from manipulating firewall rules](https://docs.docker.com/engine/network/packet-filtering-firewalls/#prevent-docker-from-manipulating-firewall-rules).
However, this is not recommended for most users as it will likely break
container networking.

## Docker's nftables tables

For bridge networks, Docker creates two tables, `ip docker-bridges` and
`ip6 docker-bridges`.

Each table contains a number of [base chains](https://wiki.nftables.org/wiki-nftables/index.php/Configuring_chains#Adding_base_chains),
and further chains are added for each bridge network. The moby project
has some [internal documentation](https://github.com/moby/moby/blob/master/integration/network/bridge/nftablesdoc/index.md)
describing its nftables, and how they depend on network and container
configuration. However, the tables and their rules are likely to change
between Docker Engine releases.

> Note
>
> Do not modify Docker's tables directly as the modifications are likely to
> be lost, Docker expects to have full ownership of its tables.

> Note
>
> Because iptables has a fixed set of chains, equivalent to nftables base
> chains, all rules are included in those chains. The `DOCKER-USER` chain
> is supplied as a way to insert rules into the `filter` table's `FORWARD`
> chain, to run before Docker's rules.
> In Docker's nftables implementation, there is no `DOCKER-USER` chain.
> Instead, rules can be added in separate tables, with base chains that
> have the same types and hook points as Docker's base chains. If necessary,
> [base chain priority](https://wiki.nftables.org/wiki-nftables/index.php/Configuring_chains#Base_chain_priority)
> can be used to tell nftables which order to call the chains in.
> Docker uses well known [priority values](https://wiki.nftables.org/wiki-nftables/index.php/Netfilter_hooks#Priority_within_hook) for each of its base chains.

## Migrating from iptables to nftables

If the Docker daemon has been running with the iptables firewall backend,
restarting it with the nftables backend will delete most of Docker's iptables
chains and rules, and create nftables rules instead.

If IP forwarding is not enabled, Docker will report an error when creating
a bridge network that needs it. Because of the default bridge, if IPv4
forwarding is disabled, the error will be reported during daemon startup.
See [IP forwarding](#ip-forwarding).

If you have rules in the `DOCKER-USER` chain, see [MigratingDOCKER-USER](#migrating-docker-user).

You may need to manually update the iptables `FORWARD` policy if it has
been set to `DROP` by Docker with iptables, or as part of your host's
firewall configuration. See [FORWARD policy in iptables](#forward-policy-in-iptables).

### IP forwarding

IP forwarding on the Docker host enables Docker functionality including port
publishing, communication between bridge networks, and direct routing from
outside the host to containers in bridge networks.

When running with iptables, depending on network and daemon configuration,
Docker may enable IPv4 and IPv6 forwarding on the host.

With its nftables firewall backend enabled, Docker will not enable IP forwarding
itself. It will report an error if forwarding is needed, but not already enabled.
To disable Docker's check for IP forwarding, letting it start and create networks
when it determines that forwarding is disabled, use Daemon option `--ip-forward=false`,
or `"ip-forward": false` in its configuration file.

> Warning
>
> When enabling IP forwarding, make sure you have firewall rules to block
> unwanted forwarding between non-Docker interfaces.

> Note
>
> If you stop Docker to migrate to nftables, Docker may have already enabled
> IP forwarding on your system. After a reboot, if no other service re-enables
> forwarding, Docker will fail to start.

If Docker is in a VM that has a single network interface and no other
software running, there is probably no unwanted forwarding to block.
But, on a physical host with multiple network interfaces, forwarding
between those interfaces should probably be blocked with nftables rules
unless the host is acting as a router.

To enable IP forwarding on the host, set the following sysctls:

- `net.ipv4.ip_forward=1`
- `net.ipv6.conf.all.forwarding=1`

If your host uses `systemd`, you may be able to use `systemd-sysctl`. For
example, by editing `/etc/sysctl.d/99-sysctl.conf`.

If the host is running `firewalld`, you may be able to use it to block
unwanted forwarding. Docker's bridges are in a firewalld zone called
`docker`, it creates a forwarding policy called `docker-forwarding` that
accepts forwarding from `ANY` zone to the `docker` zone.

For example, to use nftables to block forwarding between interfaces `eth0`
and `eth1`, you could use:

```console
table inet no-ext-forwarding {
	chain no-ext-forwarding {
		type filter hook forward priority filter; policy accept;
		iifname "eth0" oifname "eth1" drop
		iifname "eth1" oifname "eth0" drop
	}
}
```

### FORWARD policy in iptables

An iptables chain with `FORWARD` policy `DROP` will drop packets that have
been accepted by Docker's nftables rules, because the packet will be processed
by the iptables chains as well as Docker's nftables chains.

Some features, including port publishing, will not work unless the `DROP`
policy is removed, or additional iptables rules are added to the iptables
`FORWARD` chain to accept Docker-related traffic.

When Docker is using iptables, and it enables IP forwarding on the host,
it sets the default policy of the iptables `FORWARD` chain to `DROP`. So,
if you stop Docker to migrate to nftables, it may have set a `DROP` that
you need to remove. It will be removed anyway on reboot.

To keep using rules in `DOCKER-USER` that rely on the chain having policy
`DROP`, you must add explicit `ACCEPT` rules for Docker related traffic.

To check the current iptables `FORWARD` policy, use:

```console
$ iptables -L FORWARD
Chain FORWARD (policy DROP)
target     prot opt source               destination
$ ip6tables -L FORWARD
Chain FORWARD (policy ACCEPT)
target     prot opt source               destination
```

To set the iptables policies to `ACCEPT` for IPv4 and IPv6:

```console
$ iptables -P FORWARD ACCEPT
$ ip6tables -P FORWARD ACCEPT
```

### MigratingDOCKER-USER

With firewall backend "iptables", rules added to the iptables `DOCKER-USER`
are processed before Docker's rules in the filter table's `FORWARD` chain.

When starting the daemon with nftables after running with iptables, Docker
will not remove the jump from the `FORWARD` chain to `DOCKER-USER`. So,
rules created in `DOCKER-USER` will continue to run until the jump is
removed or the host is rebooted.

When starting with nftables, the daemon will not add the jump. So, unless
there is an existing jump, rules in `DOCKER-USER` will be ignored.

#### Migrating ACCEPT rules

Some rules in the `DOCKER-USER` chain will continue to work. For example, if a
packet is dropped, it will be dropped before or after the nftables rules in
Docker's `filter-FORWARD` chain. But other rules, particularly `ACCEPT` rules
to override Docker's `DROP` rules, will not work.

In nftables, an "accept" rule is not final. It terminates processing
for its base chain, but the accepted packet will still be processed by
other base chains, which may drop it.

To override Docker's `drop` rule, you must use a firewall mark. Select a
mark not already in use on your host, and use Docker Engine option
`--bridge-accept-fwmark`.

For example, `--bridge-accept-fwmark=1` tells the daemon to accept any
packet with an `fwmark` value of `1`. Optionally, you can supply a mask
to match specific bits in the mark, `--bridge-accept-fwmark=0x1/0x3`.

Then, instead of accepting the packet in `DOCKER-USER`, add the firewall
mark you have chosen and Docker will not drop it.

The firewall mark must be added before Docker's rules run. So if the mark
is added in a chain with type `filter` and hook `forward`, it must have
priority `filter - 1` or lower.

#### ReplacingDOCKER-USERwith an nftables table

Because nftables doesn't have pre-defined chains, to replace the `DOCKER-USER`
chain you can create your own table and add chains and rules to it.

The `DOCKER-USER` chain has type `filter` and hook `forward`, so it can
only have rules in the filter forward chain. The base chains in your
table can have any `type` or `hook`. If your rules need to run before
Docker's rules, give the base chains a lower `priority` number than
Docker's chain. Or, a higher priority to make sure they run after Docker's
rules.

Docker's base chains use the priority values defined at
[priority values](https://wiki.nftables.org/wiki-nftables/index.php/Netfilter_hooks#Priority_within_hook)

#### Example: restricting external connections to containers

By default, any remote host can connect to ports published to the Docker
host's external addresses.

To allow only a specific IP or network to access the containers, create a
table with a base chain that has a drop rule. For example, the
following table drops packets from all IP addresses except `192.0.2.2`:

```console
table ip my-table {
	chain my-filter-forward {
		type filter hook forward priority filter; policy accept;
		iifname "ext_if" ip saddr != 192.0.2.2 counter drop
	}
}
```

You will need to change `ext_if` to your host's external interface name.

You could instead accept connections from a source subnet. The following
table only accepts access from the subnet `192.0.2.0/24`:

```console
table ip my-table {
	chain my-filter-forward {
		type filter hook forward priority filter; policy accept;
		iifname "ext_if" ip saddr != 192.0.2.0/24 counter drop
	}
}
```

If you are running other services on the host that use IP forwarding
and need to be accessed by different external hosts, you will need more
specific filters. For example, to match the default prefix `br-` of
bridge devices belonging to Docker's user-defined bridge networks:

```console
table ip my-table {
	chain my-filter-forward {
		type filter hook forward priority filter; policy accept;
		iifname "ext_if" oifname "br-*" ip saddr != 192.0.2.0/24 counter drop
	}
}
```

For more information about nftables configuration and advanced usage,
refer to the [nftables wiki](https://wiki.nftables.org/wiki-nftables/index.php/Main_Page).
