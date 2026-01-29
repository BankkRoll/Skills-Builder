# IPvlan network driver and more

# IPvlan network driver

> All about using IPvlan to make your containers appear like physical machines on the network

# IPvlan network driver

   Table of contents

---

The IPvlan driver gives users total control over both IPv4 and IPv6 addressing.
The VLAN driver builds on top of that in giving operators complete control of
layer 2 VLAN tagging and even IPvlan L3 routing for users interested in underlay
network integration. For overlay deployments that abstract away physical constraints
see the [multi-host overlay](https://docs.docker.com/engine/network/drivers/overlay/) driver.

IPvlan is a new twist on the tried and true network virtualization technique.
The Linux implementations are extremely lightweight because rather than using
the traditional Linux bridge for isolation, they are associated to a Linux
Ethernet interface or sub-interface to enforce separation between networks and
connectivity to the physical network.

IPvlan offers a number of unique features and plenty of room for further
innovations with the various modes. Two high level advantages of these approaches
are, the positive performance implications of bypassing the Linux bridge and the
simplicity of having fewer moving parts. Removing the bridge that traditionally
resides in between the Docker host NIC and container interface leaves a simple
setup consisting of container interfaces, attached directly to the Docker host
interface. This result is easy to access for external facing services as there
is no need for port mappings in these scenarios.

## Options

The following table describes the driver-specific options that you can pass to
`--opt` when creating a network using the `ipvlan` driver.

| Option | Default | Description |
| --- | --- | --- |
| ipvlan_mode | l2 | Sets the IPvlan operating mode. Can be one of:l2,l3,l3s |
| ipvlan_flag | bridge | Sets the IPvlan mode flag. Can be one of:bridge,private,vepa |
| parent |  | Specifies the parent interface to use. |

## Examples

### Prerequisites

- The examples on this page are all single host.
- All examples can be performed on a single host running Docker. Any
  example using a sub-interface like `eth0.10` can be replaced with `eth0` or
  any other valid parent interface on the Docker host. Sub-interfaces with a `.`
  are created on the fly. `-o parent` interfaces can also be left out of the
  `docker network create` all together and the driver will create a `dummy`
  interface that will enable local host connectivity to perform the examples.
- Kernel requirements:
  - IPvlan Linux kernel v4.2+ (support for earlier kernels exists but is buggy). To check your current kernel version, use `uname -r`

### IPvlan L2 mode example usage

An example of the IPvlan `L2` mode topology is shown in the following image.
The driver is specified with `-d driver_name` option. In this case `-d ipvlan`.

![Simple IPvlan L2 Mode Example](https://docs.docker.com/engine/network/drivers/images/ipvlan_l2_simple.png)  ![Simple IPvlan L2 Mode Example](https://docs.docker.com/engine/network/drivers/images/ipvlan_l2_simple.png)

The parent interface in the next example `-o parent=eth0` is configured as follows:

```console
$ ip addr show eth0
3: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    inet 192.168.1.250/24 brd 192.168.1.255 scope global eth0
```

Use the network from the host's interface as the `--subnet` in the
`docker network create`. The container will be attached to the same network as
the host interface as set via the `-o parent=` option.

Create the IPvlan network and run a container attaching to it:

```console
# IPvlan  (-o ipvlan_mode= Defaults to L2 mode if not specified)
$ docker network create -d ipvlan \
    --subnet=192.168.1.0/24 \
    --gateway=192.168.1.1 \
    -o ipvlan_mode=l2 \
    -o parent=eth0 db_net

# Start a container on the db_net network
$ docker run --net=db_net -it --rm alpine /bin/sh

# NOTE: the containers can NOT ping the underlying host interfaces as
# they are intentionally filtered by Linux for additional isolation.
```

The default mode for IPvlan is `l2`. If `-o ipvlan_mode=` is left unspecified,
the default mode will be used. Similarly, if the `--gateway` is left empty, the
first usable address on the network will be set as the gateway. For example, if
the subnet provided in the network create is `--subnet=192.168.1.0/24` then the
gateway the container receives is `192.168.1.1`.

To help understand how this mode interacts with other hosts, the following
figure shows the same layer 2 segment between two Docker hosts that applies to
and IPvlan L2 mode.

![Multiple IPvlan hosts](https://docs.docker.com/engine/network/drivers/images/macvlan-bridge-ipvlan-l2.webp)  ![Multiple IPvlan hosts](https://docs.docker.com/engine/network/drivers/images/macvlan-bridge-ipvlan-l2.webp)

The following will create the exact same network as the network `db_net` created
earlier, with the driver defaults for `--gateway=192.168.1.1` and `-o ipvlan_mode=l2`.

```console
# IPvlan  (-o ipvlan_mode= Defaults to L2 mode if not specified)
$ docker network create -d ipvlan \
    --subnet=192.168.1.0/24 \
    -o parent=eth0 db_net_ipv

# Start a container with an explicit name in daemon mode
$ docker run --net=db_net_ipv --name=ipv1 -itd alpine /bin/sh

# Start a second container and ping using the container name
# to see the docker included name resolution functionality
$ docker run --net=db_net_ipv --name=ipv2 -it --rm alpine /bin/sh
$ ping -c 4 ipv1

# NOTE: the containers can NOT ping the underlying host interfaces as
# they are intentionally filtered by Linux for additional isolation.
```

The drivers also support the `--internal` flag that will completely isolate
containers on a network from any communications external to that network. Since
network isolation is tightly coupled to the network's parent interface the result
of leaving the `-o parent=` option off of a `docker network create` is the exact
same as the `--internal` option. If the parent interface is not specified or the
`--internal` flag is used, a netlink type `dummy` parent interface is created
for the user and used as the parent interface effectively isolating the network
completely.

The following two `docker network create` examples result in identical networks
that you can attach container to:

```console
# Empty '-o parent=' creates an isolated network
$ docker network create -d ipvlan \
    --subnet=192.168.10.0/24 isolated1

# Explicit '--internal' flag is the same:
$ docker network create -d ipvlan \
    --subnet=192.168.11.0/24 --internal isolated2

# Even the '--subnet=' can be left empty and the default
# IPAM subnet of 172.18.0.0/16 will be assigned
$ docker network create -d ipvlan isolated3

$ docker run --net=isolated1 --name=cid1 -it --rm alpine /bin/sh
$ docker run --net=isolated2 --name=cid2 -it --rm alpine /bin/sh
$ docker run --net=isolated3 --name=cid3 -it --rm alpine /bin/sh

# To attach to any use `docker exec` and start a shell
$ docker exec -it cid1 /bin/sh
$ docker exec -it cid2 /bin/sh
$ docker exec -it cid3 /bin/sh
```

### IPvlan 802.1Q trunk L2 mode example usage

Architecturally, IPvlan L2 mode trunking is the same as Macvlan with regard to
gateways and L2 path isolation. There are nuances that can be advantageous for
CAM table pressure in ToR switches, one MAC per port and MAC exhaustion on a
host's parent NIC to name a few. The 802.1Q trunk scenario looks the same. Both
modes adhere to tagging standards and have seamless integration with the physical
network for underlay integration and hardware vendor plugin integrations.

Hosts on the same VLAN are typically on the same subnet and almost always are
grouped together based on their security policy. In most scenarios, a multi-tier
application is tiered into different subnets because the security profile of each
process requires some form of isolation. For example, hosting your credit card
processing on the same virtual network as the frontend webserver would be a
regulatory compliance issue, along with circumventing the long standing best
practice of layered defense in depth architectures. VLANs or the equivocal VNI
(Virtual Network Identifier) when using the Overlay driver, are the first step
in isolating tenant traffic.

![Docker VLANs in-depth](https://docs.docker.com/engine/network/drivers/images/vlans-deeper-look.webp)  ![Docker VLANs in-depth](https://docs.docker.com/engine/network/drivers/images/vlans-deeper-look.webp)

The Linux sub-interface tagged with a VLAN can either already exist or will be
created when you call a `docker network create`. `docker network rm` will delete
the sub-interface. Parent interfaces such as `eth0` are not deleted, only
sub-interfaces with a netlink parent index > 0.

For the driver to add/delete the VLAN sub-interfaces the format needs to be
`interface_name.vlan_tag`. Other sub-interface naming can be used as the
specified parent, but the link will not be deleted automatically when
`docker network rm` is invoked.

The option to use either existing parent VLAN sub-interfaces or let Docker manage
them enables the user to either completely manage the Linux interfaces and
networking or let Docker create and delete the VLAN parent sub-interfaces
(netlink `ip link`) with no effort from the user.

For example: use `eth0.10` to denote a sub-interface of `eth0` tagged with the
VLAN id of `10`. The equivalent `ip link` command would be
`ip link add link eth0 name eth0.10 type vlan id 10`.

The example creates the VLAN tagged networks and then starts two containers to
test connectivity between containers. Different VLANs cannot ping one another
without a router routing between the two networks. The default namespace is not
reachable per IPvlan design in order to isolate container namespaces from the
underlying host.

#### VLAN ID 20

In the first network tagged and isolated by the Docker host, `eth0.20` is the
parent interface tagged with VLAN id `20` specified with `-o parent=eth0.20`.
Other naming formats can be used, but the links need to be added and deleted
manually using `ip link` or Linux configuration files. As long as the `-o parent`
exists, anything can be used if it is compliant with Linux netlink.

```console
# now add networks and hosts as you would normally by attaching to the master (sub)interface that is tagged
$ docker network create -d ipvlan \
    --subnet=192.168.20.0/24 \
    --gateway=192.168.20.1 \
    -o parent=eth0.20 ipvlan20

# in two separate terminals, start a Docker container and the containers can now ping one another.
$ docker run --net=ipvlan20 -it --name ivlan_test1 --rm alpine /bin/sh
$ docker run --net=ipvlan20 -it --name ivlan_test2 --rm alpine /bin/sh
```

#### VLAN ID 30

In the second network, tagged and isolated by the Docker host, `eth0.30` is the
parent interface tagged with VLAN id `30` specified with `-o parent=eth0.30`. The
`ipvlan_mode=` defaults to l2 mode `ipvlan_mode=l2`. It can also be explicitly
set with the same result as shown in the next example.

```console
# now add networks and hosts as you would normally by attaching to the master (sub)interface that is tagged.
$ docker network create -d ipvlan \
    --subnet=192.168.30.0/24 \
    --gateway=192.168.30.1 \
    -o parent=eth0.30 \
    -o ipvlan_mode=l2 ipvlan30

# in two separate terminals, start a Docker container and the containers can now ping one another.
$ docker run --net=ipvlan30 -it --name ivlan_test3 --rm alpine /bin/sh
$ docker run --net=ipvlan30 -it --name ivlan_test4 --rm alpine /bin/sh
```

The gateway is set inside of the container as the default gateway. That gateway
would typically be an external router on the network.

```console
$$ ip route
  default via 192.168.30.1 dev eth0
  192.168.30.0/24 dev eth0  src 192.168.30.2
```

Example: Multi-Subnet IPvlan L2 Mode starting two containers on the same subnet
and pinging one another. In order for the `192.168.114.0/24` to reach
`192.168.116.0/24` it requires an external router in L2 mode. L3 mode can route
between subnets that share a common `-o parent=`.

Secondary addresses on network routers are common as an address space becomes
exhausted to add another secondary to an L3 VLAN interface or commonly referred
to as a "switched virtual interface" (SVI).

```console
$ docker network create -d ipvlan \
    --subnet=192.168.114.0/24 --subnet=192.168.116.0/24 \
    --gateway=192.168.114.254 --gateway=192.168.116.254 \
    -o parent=eth0.114 \
    -o ipvlan_mode=l2 ipvlan114

$ docker run --net=ipvlan114 --ip=192.168.114.10 -it --rm alpine /bin/sh
$ docker run --net=ipvlan114 --ip=192.168.114.11 -it --rm alpine /bin/sh
```

A key takeaway is, operators have the ability to map their physical network into
their virtual network for integrating containers into their environment with no
operational overhauls required. NetOps drops an 802.1Q trunk into the
Docker host. That virtual link would be the `-o parent=` passed in the network
creation. For untagged (non-VLAN) links, it is as simple as `-o parent=eth0` or
for 802.1Q trunks with VLAN IDs each network gets mapped to the corresponding
VLAN/Subnet from the network.

An example being, NetOps provides VLAN ID and the associated subnets for VLANs
being passed on the Ethernet link to the Docker host server. Those values are
plugged into the `docker network create` commands when provisioning the
Docker networks. These are persistent configurations that are applied every time
the Docker engine starts which alleviates having to manage often complex
configuration files. The network interfaces can also be managed manually by
being pre-created and Docker networking will never modify them, and use them
as parent interfaces. Example mappings from NetOps to Docker network commands
are as follows:

- VLAN: 10, Subnet: 172.16.80.0/24, Gateway: 172.16.80.1
  - `--subnet=172.16.80.0/24 --gateway=172.16.80.1 -o parent=eth0.10`
- VLAN: 20, IP subnet: 172.16.50.0/22, Gateway: 172.16.50.1
  - `--subnet=172.16.50.0/22 --gateway=172.16.50.1 -o parent=eth0.20`
- VLAN: 30, Subnet: 10.1.100.0/16, Gateway: 10.1.100.1
  - `--subnet=10.1.100.0/16 --gateway=10.1.100.1 -o parent=eth0.30`

### IPvlan L3 mode example

IPvlan will require routes to be distributed to each endpoint. The driver only
builds the IPvlan L3 mode port and attaches the container to the interface. Route
distribution throughout a cluster is beyond the initial implementation of this
single host scoped driver. In L3 mode, the Docker host is very similar to a
router starting new networks in the container. They are on networks that the
upstream network will not know about without route distribution. For those
curious how IPvlan L3 will fit into container networking, see the following
examples.

![Docker IPvlan L2 mode](https://docs.docker.com/engine/network/drivers/images/ipvlan-l3.webp)  ![Docker IPvlan L2 mode](https://docs.docker.com/engine/network/drivers/images/ipvlan-l3.webp)

IPvlan L3 mode drops all broadcast and multicast traffic. This reason alone
makes IPvlan L3 mode a prime candidate for those looking for massive scale and
predictable network integrations. It is predictable and in turn will lead to
greater uptimes because there is no bridging involved. Bridging loops have been
responsible for high profile outages that can be hard to pinpoint depending on
the size of the failure domain. This is due to the cascading nature of BPDUs
(Bridge Port Data Units) that are flooded throughout a broadcast domain (VLAN)
to find and block topology loops. Eliminating bridging domains, or at the least,
keeping them isolated to a pair of ToRs (top of rack switches) will reduce hard
to troubleshoot bridging instabilities. IPvlan L2 modes is well suited for
isolated VLANs only trunked into a pair of ToRs that can provide a loop-free
non-blocking fabric. The next step further is to route at the edge via IPvlan L3
mode that reduces a failure domain to a local host only.

- L3 mode needs to be on a separate subnet as the default namespace since it
  requires a netlink route in the default namespace pointing to the IPvlan parent
  interface.
- The parent interface used in this example is `eth0` and it is on the subnet
  `192.168.1.0/24`. Notice the `docker network` is not on the same subnet
  as `eth0`.
- Unlike IPvlan l2 modes, different subnets/networks can ping one another as
  long as they share the same parent interface `-o parent=`.

```console
$$ ip a show eth0
3: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 00:50:56:39:45:2e brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.250/24 brd 192.168.1.255 scope global eth0
```

- A traditional gateway doesn't mean much to an L3 mode IPvlan interface since
  there is no broadcast traffic allowed. Because of that, the container default
  gateway points to the containers `eth0` device. See below for CLI output
  of `ip route` or `ip -6 route` from inside an L3 container for details.

The mode `-o ipvlan_mode=l3` must be explicitly specified since the default
IPvlan mode is `l2`.

The following example does not specify a parent interface. The network drivers
will create a dummy type link for the user rather than rejecting the network
creation and isolating containers from only communicating with one another.

```console
# Create the IPvlan L3 network
$ docker network create -d ipvlan \
    --subnet=192.168.214.0/24 \
    --subnet=10.1.214.0/24 \
    -o ipvlan_mode=l3 ipnet210

# Test 192.168.214.0/24 connectivity
$ docker run --net=ipnet210 --ip=192.168.214.10 -itd alpine /bin/sh
$ docker run --net=ipnet210 --ip=10.1.214.10 -itd alpine /bin/sh

# Test L3 connectivity from 10.1.214.0/24 to 192.168.214.0/24
$ docker run --net=ipnet210 --ip=192.168.214.9 -it --rm alpine ping -c 2 10.1.214.10

# Test L3 connectivity from 192.168.214.0/24 to 10.1.214.0/24
$ docker run --net=ipnet210 --ip=10.1.214.9 -it --rm alpine ping -c 2 192.168.214.10
```

> Note
>
> Notice that there is no `--gateway=` option in the network create. The field
> is ignored if one is specified `l3` mode. Take a look at the container routing
> table from inside of the container:
>
>
>
> ```console
> # Inside an L3 mode container
> $$ ip route
>  default dev eth0
>   192.168.214.0/24 dev eth0  src 192.168.214.10
> ```

In order to ping the containers from a remote Docker host or the container be
able to ping a remote host, the remote host or the physical network in between
need to have a route pointing to the host IP address of the container's Docker
host eth interface.

### Dual stack IPv4 IPv6 IPvlan L2 mode

- Not only does Libnetwork give you complete control over IPv4 addressing, but
  it also gives you total control over IPv6 addressing as well as feature parity
  between the two address families.
- The next example will start with IPv6 only. Start two containers on the same
  VLAN `139` and ping one another. Since the IPv4 subnet is not specified, the
  default IPAM will provision a default IPv4 subnet. That subnet is isolated
  unless the upstream network is explicitly routing it on VLAN `139`.

```console
# Create a v6 network
$ docker network create -d ipvlan \
    --ipv6 --subnet=2001:db8:abc2::/64 --gateway=2001:db8:abc2::22 \
    -o parent=eth0.139 v6ipvlan139

# Start a container on the network
$ docker run --net=v6ipvlan139 -it --rm alpine /bin/sh
```

View the container eth0 interface and v6 routing table:

```console
# Inside the IPv6 container
$$ ip a show eth0
75: eth0@if55: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN group default
    link/ether 00:50:56:2b:29:40 brd ff:ff:ff:ff:ff:ff
    inet 172.18.0.2/16 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 2001:db8:abc4::250:56ff:fe2b:2940/64 scope link
       valid_lft forever preferred_lft forever
    inet6 2001:db8:abc2::1/64 scope link nodad
       valid_lft forever preferred_lft forever

$$ ip -6 route
2001:db8:abc4::/64 dev eth0  proto kernel  metric 256
2001:db8:abc2::/64 dev eth0  proto kernel  metric 256
default via 2001:db8:abc2::22 dev eth0  metric 1024
```

Start a second container and ping the first container's v6 address.

```console
# Test L2 connectivity over IPv6
$ docker run --net=v6ipvlan139 -it --rm alpine /bin/sh

# Inside the second IPv6 container
$$ ip a show eth0
75: eth0@if55: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN group default
    link/ether 00:50:56:2b:29:40 brd ff:ff:ff:ff:ff:ff
    inet 172.18.0.3/16 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 2001:db8:abc4::250:56ff:fe2b:2940/64 scope link tentative dadfailed
       valid_lft forever preferred_lft forever
    inet6 2001:db8:abc2::2/64 scope link nodad
       valid_lft forever preferred_lft forever

$$ ping6 2001:db8:abc2::1
PING 2001:db8:abc2::1 (2001:db8:abc2::1): 56 data bytes
64 bytes from 2001:db8:abc2::1%eth0: icmp_seq=0 ttl=64 time=0.044 ms
64 bytes from 2001:db8:abc2::1%eth0: icmp_seq=1 ttl=64 time=0.058 ms

2 packets transmitted, 2 packets received, 0% packet loss
round-trip min/avg/max/stddev = 0.044/0.051/0.058/0.000 ms
```

The next example with setup a dual stack IPv4/IPv6 network with an example
VLAN ID of `140`.

Next create a network with two IPv4 subnets and one IPv6 subnets, all of which
have explicit gateways:

```console
$ docker network create -d ipvlan \
    --subnet=192.168.140.0/24 --subnet=192.168.142.0/24 \
    --gateway=192.168.140.1 --gateway=192.168.142.1 \
    --subnet=2001:db8:abc9::/64 --gateway=2001:db8:abc9::22 \
    -o parent=eth0.140 \
    -o ipvlan_mode=l2 ipvlan140
```

Start a container and view eth0 and both v4 & v6 routing tables:

```console
$ docker run --net=ipvlan140 --ip6=2001:db8:abc2::51 -it --rm alpine /bin/sh

$ ip a show eth0
78: eth0@if77: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN group default
    link/ether 00:50:56:2b:29:40 brd ff:ff:ff:ff:ff:ff
    inet 192.168.140.2/24 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 2001:db8:abc4::250:56ff:fe2b:2940/64 scope link
       valid_lft forever preferred_lft forever
    inet6 2001:db8:abc9::1/64 scope link nodad
       valid_lft forever preferred_lft forever

$$ ip route
default via 192.168.140.1 dev eth0
192.168.140.0/24 dev eth0  proto kernel  scope link  src 192.168.140.2

$$ ip -6 route
2001:db8:abc4::/64 dev eth0  proto kernel  metric 256
2001:db8:abc9::/64 dev eth0  proto kernel  metric 256
default via 2001:db8:abc9::22 dev eth0  metric 1024
```

Start a second container with a specific `--ip4` address and ping the first host
using IPv4 packets:

```console
$ docker run --net=ipvlan140 --ip=192.168.140.10 -it --rm alpine /bin/sh
```

> Note
>
> Different subnets on the same parent interface in IPvlan `L2` mode cannot ping
> one another. That requires a router to proxy-arp the requests with a secondary
> subnet. However, IPvlan `L3` will route the unicast traffic between disparate
> subnets as long as they share the same `-o parent` parent link.

### Dual stack IPv4 IPv6 IPvlan L3 mode

Example: IPvlan L3 Mode Dual Stack IPv4/IPv6, Multi-Subnet w/ 802.1Q VLAN Tag:118

As in all of the examples, a tagged VLAN interface does not have to be used. The
sub-interfaces can be swapped with `eth0`, `eth1`, `bond0` or any other valid
interface on the host other then the `lo` loopback.

The primary difference you will see is that L3 mode does not create a default
route with a next-hop but rather sets a default route pointing to `dev eth` only
since ARP/Broadcasts/Multicast are all filtered by Linux as per the design. Since
the parent interface is essentially acting as a router, the parent interface IP
and subnet needs to be different from the container networks. That is the opposite
of bridge and L2 modes, which need to be on the same subnet (broadcast domain)
in order to forward broadcast and multicast packets.

```console
# Create an IPv6+IPv4 Dual Stack IPvlan L3 network
# Gateways for both v4 and v6 are set to a dev e.g. 'default dev eth0'
$ docker network create -d ipvlan \
    --subnet=192.168.110.0/24 \
    --subnet=192.168.112.0/24 \
    --subnet=2001:db8:abc6::/64 \
    -o parent=eth0 \
    -o ipvlan_mode=l3 ipnet110

# Start a few of containers on the network (ipnet110)
# in separate terminals and check connectivity
$ docker run --net=ipnet110 -it --rm alpine /bin/sh
# Start a second container specifying the v6 address
$ docker run --net=ipnet110 --ip6=2001:db8:abc6::10 -it --rm alpine /bin/sh
# Start a third specifying the IPv4 address
$ docker run --net=ipnet110 --ip=192.168.112.30 -it --rm alpine /bin/sh
# Start a 4th specifying both the IPv4 and IPv6 addresses
$ docker run --net=ipnet110 --ip6=2001:db8:abc6::50 --ip=192.168.112.50 -it --rm alpine /bin/sh
```

Interface and routing table outputs are as follows:

```console
$$ ip a show eth0
63: eth0@if59: <BROADCAST,MULTICAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN group default
    link/ether 00:50:56:2b:29:40 brd ff:ff:ff:ff:ff:ff
    inet 192.168.112.2/24 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 2001:db8:abc4::250:56ff:fe2b:2940/64 scope link
       valid_lft forever preferred_lft forever
    inet6 2001:db8:abc6::10/64 scope link nodad
       valid_lft forever preferred_lft forever

# Note the default route is the eth device because ARPs are filtered.
$$ ip route
  default dev eth0  scope link
  192.168.112.0/24 dev eth0  proto kernel  scope link  src 192.168.112.2

$$ ip -6 route
2001:db8:abc4::/64 dev eth0  proto kernel  metric 256
2001:db8:abc6::/64 dev eth0  proto kernel  metric 256
default dev eth0  metric 1024
```

> Note
>
> There may be a bug when specifying `--ip6=` addresses when you delete a
> container with a specified v6 address and then start a new container with the
> same v6 address it throws the following like the address isn't properly being
> released to the v6 pool. It will fail to unmount the container and be left dead.

```console
docker: Error response from daemon: Address already in use.
```

### Manually create 802.1Q links

#### VLAN ID 40

If a user does not want the driver to create the VLAN sub-interface, it needs to
exist before running `docker network create`. If you have sub-interface
naming that is not `interface.vlan_id` it is honored in the `-o parent=` option
again as long as the interface exists and is up.

Links, when manually created, can be named anything as long as they exist when
the network is created. Manually created links do not get deleted regardless of
the name when the network is deleted with `docker network rm`.

```console
# create a new sub-interface tied to dot1q vlan 40
$ ip link add link eth0 name eth0.40 type vlan id 40

# enable the new sub-interface
$ ip link set eth0.40 up

# now add networks and hosts as you would normally by attaching to the master (sub)interface that is tagged
$ docker network create -d ipvlan \
    --subnet=192.168.40.0/24 \
    --gateway=192.168.40.1 \
    -o parent=eth0.40 ipvlan40

# in two separate terminals, start a Docker container and the containers can now ping one another.
$ docker run --net=ipvlan40 -it --name ivlan_test5 --rm alpine /bin/sh
$ docker run --net=ipvlan40 -it --name ivlan_test6 --rm alpine /bin/sh
```

Example: VLAN sub-interface manually created with any name:

```console
# create a new sub interface tied to dot1q vlan 40
$ ip link add link eth0 name foo type vlan id 40

# enable the new sub-interface
$ ip link set foo up

# now add networks and hosts as you would normally by attaching to the master (sub)interface that is tagged
$ docker network create -d ipvlan \
    --subnet=192.168.40.0/24 --gateway=192.168.40.1 \
    -o parent=foo ipvlan40

# in two separate terminals, start a Docker container and the containers can now ping one another.
$ docker run --net=ipvlan40 -it --name ivlan_test5 --rm alpine /bin/sh
$ docker run --net=ipvlan40 -it --name ivlan_test6 --rm alpine /bin/sh
```

Manually created links can be cleaned up with:

```console
$ ip link del foo
```

As with all of the Libnetwork drivers, they can be mixed and matched, even as
far as running 3rd party ecosystem drivers in parallel for maximum flexibility
to the Docker user.

---

# Macvlan network driver

> All about using Macvlan to make your containers appear like physical machines on the network

# Macvlan network driver

   Table of contents

---

Some applications, especially legacy applications or applications which monitor
network traffic, expect to be directly connected to the physical network. In
this type of situation, you can use the `macvlan` network driver to assign a MAC
address to each container's virtual network interface, making it appear to be
a physical network interface directly connected to the physical network. In this
case, you need to designate a physical interface on your Docker host to use for
the Macvlan, as well as the subnet and gateway of the network. You can even
isolate your Macvlan networks using different physical network interfaces.

## Platform support and requirements

- The macvlan driver only works on Linux hosts. It is not supported on
  Docker Desktop for Mac or Windows, or Docker Engine on Windows.
- Most cloud providers block macvlan networking. You may need physical access to
  your networking equipment.
- Requires at least Linux kernel version 3.9 (version 4.0 or later is
  recommended).
- The macvlan driver is not supported in rootless mode.

## Considerations

- You may unintentionally degrade your network due to IP address
  exhaustion or to "VLAN spread", a situation that occurs when you have an
  inappropriately large number of unique MAC addresses in your network.
- Your networking equipment needs to be able to handle "promiscuous mode",
  where one physical interface can be assigned multiple MAC addresses.
- If your application can work using a bridge (on a single Docker host) or
  overlay (to communicate across multiple Docker hosts), these solutions may be
  better in the long term.
- Containers attached to a macvlan network cannot communicate with the host
  directly, this is a restriction in the Linux kernel. If you need communication
  between the host and the containers, you can connect the containers to a
  bridge network as well as the macvlan. It is also possible to create a
  macvlan interface on the host with the same parent interface, and assign it
  an IP address in the Docker network's subnet.

## Options

The following table describes the driver-specific options that you can pass to
`--opt` when creating a network using the `macvlan` driver.

| Option | Default | Description |
| --- | --- | --- |
| macvlan_mode | bridge | Sets the Macvlan mode. Can be one of:bridge,vepa,passthru,private |
| parent |  | Specifies the parent interface to use. |

## Create a Macvlan network

When you create a Macvlan network, it can either be in bridge mode or 802.1Q
trunk bridge mode.

- In bridge mode, Macvlan traffic goes through a physical device on the host.
- In 802.1Q trunk bridge mode, traffic goes through an 802.1Q sub-interface
  which Docker creates on the fly. This allows you to control routing and
  filtering at a more granular level.

### Bridge mode

To create a `macvlan` network which bridges with a given physical network
interface, use `--driver macvlan` with the `docker network create` command. You
also need to specify the `parent`, which is the interface the traffic will
physically go through on the Docker host.

```console
$ docker network create -d macvlan \
  --subnet=172.16.86.0/24 \
  --gateway=172.16.86.1 \
  -o parent=eth0 pub_net
```

If you need to exclude IP addresses from being used in the `macvlan` network, such
as when a given IP address is already in use, use `--aux-addresses`:

```console
$ docker network create -d macvlan \
  --subnet=192.168.32.0/24 \
  --ip-range=192.168.32.128/25 \
  --gateway=192.168.32.254 \
  --aux-address="my-router=192.168.32.129" \
  -o parent=eth0 macnet32
```

### 802.1Q trunk bridge mode

If you specify a `parent` interface name with a dot included, such as `eth0.50`,
Docker interprets that as a sub-interface of `eth0` and creates the sub-interface
automatically.

```console
$ docker network create -d macvlan \
    --subnet=192.168.50.0/24 \
    --gateway=192.168.50.1 \
    -o parent=eth0.50 macvlan50
```

### Use an IPvlan instead of Macvlan

An `ipvlan` network created with option `-o ipvlan_mode=l2` is similar
to a macvlan network. The main difference is that the `ipvlan` driver
doesn't assign a MAC address to each container, the layer-2 network stack
is shared by devices in the ipvlan network. So, containers use the parent
interface's MAC address.

The network will see fewer MAC addresses, and the host's MAC address will be
associated with the IP address of each container.

The choice of network type depends on your environment and requirements.
There are some notes about the trade-offs in the [Linux kernel
documentation](https://docs.kernel.org/networking/ipvlan.html#what-to-choose-macvlan-vs-ipvlan).

```console
$ docker network create -d ipvlan \
    --subnet=192.168.210.0/24 \
    --gateway=192.168.210.254 \
     -o ipvlan_mode=l2 -o parent=eth0 ipvlan210
```

## Use IPv6

If you have
[configured the Docker daemon to allow IPv6](https://docs.docker.com/engine/daemon/ipv6/),
you can use dual-stack IPv4/IPv6 `macvlan` networks.

```console
$ docker network create -d macvlan \
    --subnet=192.168.216.0/24 --subnet=192.168.218.0/24 \
    --gateway=192.168.216.1 --gateway=192.168.218.1 \
    --subnet=2001:db8:abc8::/64 --gateway=2001:db8:abc8::10 \
     -o parent=eth0.218 \
     -o macvlan_mode=bridge macvlan216
```

## Usage examples

This section provides hands-on examples for working with macvlan networks,
including bridge mode and 802.1Q trunk bridge mode.

> Note
>
> These examples assume your ethernet interface is `eth0`. If your device has a
> different name, use that instead.

### Bridge mode example

In bridge mode, your traffic flows through `eth0` and Docker routes traffic to
your container using its MAC address. To network devices on your network, your
container appears to be physically attached to the network.

1. Create a macvlan network called `my-macvlan-net`. Modify the `subnet`,
  `gateway`, and `parent` values to match your environment:
  ```console
  $ docker network create -d macvlan \
    --subnet=172.16.86.0/24 \
    --gateway=172.16.86.1 \
    -o parent=eth0 \
    my-macvlan-net
  ```
  Verify the network was created:
  ```console
  $ docker network ls
  $ docker network inspect my-macvlan-net
  ```
2. Start an `alpine` container and attach it to the `my-macvlan-net` network.
  The `-dit` flags start the container in the background. The `--rm` flag
  removes the container when it stops:
  ```console
  $ docker run --rm -dit \
    --network my-macvlan-net \
    --name my-macvlan-alpine \
    alpine:latest \
    ash
  ```
3. Inspect the container and notice the `MacAddress` key within the `Networks`
  section:
  ```console
  $ docker container inspect my-macvlan-alpine
  ```
  Look for output similar to:
  ```json
  "Networks": {
    "my-macvlan-net": {
      "Gateway": "172.16.86.1",
      "IPAddress": "172.16.86.2",
      "IPPrefixLen": 24,
      "MacAddress": "02:42:ac:10:56:02",
      ...
    }
  }
  ```
4. Check how the container sees its own network interfaces:
  ```console
  $ docker exec my-macvlan-alpine ip addr show eth0
  9: eth0@tunl0: <BROADCAST,MULTICAST,UP,LOWER_UP,M-DOWN> mtu 1500 qdisc noqueue state UP
  link/ether 02:42:ac:10:56:02 brd ff:ff:ff:ff:ff:ff
  inet 172.16.86.2/24 brd 172.16.86.255 scope global eth0
     valid_lft forever preferred_lft forever
  ```
  Check the routing table:
  ```console
  $ docker exec my-macvlan-alpine ip route
  default via 172.16.86.1 dev eth0
  172.16.86.0/24 dev eth0 scope link  src 172.16.86.2
  ```
5. Stop the container (Docker removes it automatically) and remove the network:
  ```console
  $ docker container stop my-macvlan-alpine
  $ docker network rm my-macvlan-net
  ```

### 802.1Q trunked bridge mode example

In 802.1Q trunk bridge mode, your traffic flows through a sub-interface of
`eth0` (called `eth0.10`) and Docker routes traffic to your container using its
MAC address. To network devices on your network, your container appears to be
physically attached to the network.

1. Create a macvlan network called `my-8021q-macvlan-net`. Modify the `subnet`,
  `gateway`, and `parent` values to match your environment:
  ```console
  $ docker network create -d macvlan \
    --subnet=172.16.86.0/24 \
    --gateway=172.16.86.1 \
    -o parent=eth0.10 \
    my-8021q-macvlan-net
  ```
  Verify the network was created and has parent `eth0.10`. You can use `ip addr show` on the Docker host to verify that the interface `eth0.10` exists:
  ```console
  $ docker network ls
  $ docker network inspect my-8021q-macvlan-net
  ```
2. Start an `alpine` container and attach it to the `my-8021q-macvlan-net`
  network:
  ```console
  $ docker run --rm -itd \
    --network my-8021q-macvlan-net \
    --name my-second-macvlan-alpine \
    alpine:latest \
    ash
  ```
3. Inspect the container and notice the `MacAddress` key:
  ```console
  $ docker container inspect my-second-macvlan-alpine
  ```
  Look for the `Networks` section with the MAC address.
4. Check how the container sees its own network interfaces:
  ```console
  $ docker exec my-second-macvlan-alpine ip addr show eth0
  11: eth0@if10: <BROADCAST,MULTICAST,UP,LOWER_UP,M-DOWN> mtu 1500 qdisc noqueue state UP
  link/ether 02:42:ac:10:56:02 brd ff:ff:ff:ff:ff:ff
  inet 172.16.86.2/24 brd 172.16.86.255 scope global eth0
     valid_lft forever preferred_lft forever
  ```
  Check the routing table:
  ```console
  $ docker exec my-second-macvlan-alpine ip route
  default via 172.16.86.1 dev eth0
  172.16.86.0/24 dev eth0 scope link  src 172.16.86.2
  ```
5. Stop the container and remove the network:
  ```console
  $ docker container stop my-second-macvlan-alpine
  $ docker network rm my-8021q-macvlan-net
  ```

---

# None network driver

> How to isolate the networking stack of a container using the none driver

# None network driver

   Table of contents

---

If you want to completely isolate the networking stack of a container, you can
use the `--network none` flag when starting the container. Within the container,
only the loopback device is created.

The following example shows the output of `ip link show` in an `alpine`
container using the `none` network driver.

```console
$ docker run --rm --network none alpine:latest ip link show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
```

No IPv6 loopback address is configured for containers using the `none` driver.

```console
$ docker run --rm --network none --name no-net-alpine alpine:latest ip addr show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
```

## Next steps

- Learn about [networking from the container's point of view](https://docs.docker.com/engine/network/)
- Learn about [host networking](https://docs.docker.com/engine/network/drivers/host/)
- Learn about [bridge networks](https://docs.docker.com/engine/network/drivers/bridge/)
- Learn about [overlay networks](https://docs.docker.com/engine/network/drivers/overlay/)
- Learn about [Macvlan networks](https://docs.docker.com/engine/network/drivers/macvlan/)
