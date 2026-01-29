# Networking overview and more

# Networking overview

> Learn how networking works from the container's point of view

# Networking overview

   Table of contents

---

Container networking refers to the ability for containers to connect to and
communicate with each other, and with non-Docker network services.

Containers have networking enabled by default, and they can make outgoing
connections. A container has no information about what kind of network it's
attached to, or whether its network peers are also Docker containers. A
container only sees a network interface with an IP address, a gateway, a
routing table, DNS services, and other networking details.

This page describes networking from the point of view of the container,
and the concepts around container networking.

When Docker Engine on Linux starts for the first time, it has a single
built-in network called the "default bridge" network. When you run a
container without the `--network` option, it is connected to the default
bridge.

Containers attached to the default bridge have access to network services
outside the Docker host. They use "masquerading" which means, if the
Docker host has Internet access, no additional configuration is needed
for the container to have Internet access.

For example, to run a container on the default bridge network, and have
it ping an Internet host:

```console
$ docker run --rm -ti busybox ping -c1 docker.com
PING docker.com (23.185.0.4): 56 data bytes
64 bytes from 23.185.0.4: seq=0 ttl=62 time=6.564 ms

--- docker.com ping statistics ---
1 packets transmitted, 1 packets received, 0% packet loss
round-trip min/avg/max = 6.564/6.564/6.564 ms
```

## User-defined networks

With the default configuration, containers attached to the default
bridge network have unrestricted network access to each other using
container IP addresses. They cannot refer to each other by name.

It can be useful to separate groups of containers that should have full
access to each other, but restricted access to containers in other groups.

You can create custom, user-defined networks, and connect groups of containers
to the same network. Once connected to a user-defined network, containers
can communicate with each other using container IP addresses or container names.

The following example creates a network using the `bridge` network driver and
runs a container in that network:

```console
$ docker network create -d bridge my-net
$ docker run --network=my-net -it busybox
```

### Drivers

Docker Engine has a number of network drivers, as well as the default "bridge".
On Linux, the following built-in network drivers are available:

| Driver | Description |
| --- | --- |
| bridge | The default network driver. |
| host | Remove network isolation between the container and the Docker host. |
| none | Completely isolate a container from the host and other containers. |
| overlay | Swarm Overlay networks connect multiple Docker daemons together. |
| ipvlan | Connect containers to external VLANs. |
| macvlan | Containers appear as devices on the host's network. |

More information can be found in the network driver specific pages, including
their configuration options and details about their functionality.

Native Windows containers have a different set of drivers, see
[Windows container network drivers](https://learn.microsoft.com/en-us/virtualization/windowscontainers/container-networking/network-drivers-topologies).

### Connecting to multiple networks

Connecting a container to a network can be compared to connecting an Ethernet
cable to a physical host. Just as a host can be connected to multiple Ethernet
networks, a container can be connected to multiple Docker networks.

For example, a frontend container may be connected to a bridge network
with external access, and a
[--internal](https://docs.docker.com/reference/cli/docker/network/create/#internal) network
to communicate with containers running backend services that do not need
external network access.

A container may also be connected to different types of network. For example,
an `ipvlan` network to provide internet access, and a `bridge` network for
access to local services.

Containers can also share networking stacks, see [Container networks](#container-networks).

When sending packets, if the destination is an address in a directly connected
network, packets are sent to that network. Otherwise, packets are sent to
a default gateway for routing to their destination. In the example above,
the `ipvlan` network's gateway must be the default gateway.

The default gateway is selected by Docker, and may change whenever a
container's network connections change.
To make Docker choose a specific default gateway when creating the container
or connecting a new network, set a gateway priority. See option `gw-priority`
for the
[docker run](https://docs.docker.com/reference/cli/docker/container/run/) and
[docker network connect](https://docs.docker.com/reference/cli/docker/network/connect/) commands.

The default `gw-priority` is `0` and the gateway in the network with the
highest priority is the default gateway. So, when a network should always
be the default gateway, it is enough to set its `gw-priority` to `1`.

```console
$ docker run --network name=gwnet,gw-priority=1 --network anet1 --name myctr myimage
$ docker network connect anet2 myctr
```

## Published ports

When you create or run a container using `docker create` or `docker run`, all
ports of containers on bridge networks are accessible from the Docker host and
other containers connected to the same network. Ports are not accessible from
outside the host or, with the default configuration, from containers in other
networks.

Use the `--publish` or `-p` flag to make a port available outside the host,
and to containers in other bridge networks.

For more information about port mapping, including how to disable it and use
direct routing to containers, see
[port publishing](https://docs.docker.com/engine/network/port-publishing/).

## IP address and hostname

When creating a network, IPv4 address allocation is enabled by default, it
can be disabled using `--ipv4=false`. IPv6 address allocation can be enabled
using `--ipv6`.

```console
$ docker network create --ipv6 --ipv4=false v6net
```

By default, the container gets an IP address for every Docker network it attaches to.
A container receives an IP address out of the IP subnet of the network.
The Docker daemon performs dynamic subnetting and IP address allocation for containers.
Each network also has a default subnet mask and gateway.

You can connect a running container to multiple networks,
either by passing the `--network` flag multiple times when creating the container,
or using the `docker network connect` command for already running containers.
In both cases, you can use the `--ip` or `--ip6` flags to specify the container's IP address on that particular network.

In the same way, a container's hostname defaults to be the container's ID in Docker.
You can override the hostname using `--hostname`.
When connecting to an existing network using `docker network connect`,
you can use the `--alias` flag to specify an additional network alias for the container on that network.

### Subnet allocation

Docker networks can use either explicitly configured subnets or automatically allocated ones from default pools.

#### Explicit subnet configuration

You can specify exact subnets when creating a network:

```console
$ docker network create --ipv6 --subnet 192.0.2.0/24 --subnet 2001:db8::/64 mynet
```

#### Automatic subnet allocation

When no `--subnet` option is provided, Docker automatically selects a subnet from predefined "default address pools".
These pools can be configured in `/etc/docker/daemon.json`. Docker's built-in default is equivalent to:

```json
{
  "default-address-pools": [
    {"base":"172.17.0.0/16","size":16},
    {"base":"172.18.0.0/16","size":16},
    {"base":"172.19.0.0/16","size":16},
    {"base":"172.20.0.0/14","size":16},
    {"base":"172.24.0.0/14","size":16},
    {"base":"172.28.0.0/14","size":16},
    {"base":"192.168.0.0/16","size":20}
  ]
}
```

- `base`: The subnet that can be allocated from.
- `size`: The prefix length used for each allocated subnet.

When an IPv6 subnet is required and there are no IPv6 addresses in `default-address-pools`, Docker allocates
subnets from a Unique Local Address (ULA) prefix. To use specific IPv6 subnets instead, add them to your
`default-address-pools`. See [Dynamic IPv6 subnet allocation](https://docs.docker.com/engine/daemon/ipv6/#dynamic-ipv6-subnet-allocation)
for more information.

Docker attempts to avoid address prefixes already in use on the host. However, you may need to customize
`default-address-pools` to prevent routing conflicts in some network environments.

The default pools use large subnets, which limits the number of networks you can create. You can divide base
subnets into smaller pools to support more networks.

For example, this configuration allows Docker to create 256 networks from `172.17.0.0/16`.
Docker will allocate subnets `172.17.0.0/24`, `172.17.1.0/24`, and so on, up to `172.17.255.0/24`:

```json
{
  "default-address-pools": [
    {"base": "172.17.0.0/16", "size": 24}
  ]
}
```

You can also request a subnet with a specific prefix length from the default pools by using unspecified
addresses in the `--subnet` option:

```console
$ docker network create --ipv6 --subnet ::/56 --subnet 0.0.0.0/24 mynet
6686a6746b17228f5052528113ddad0e6d68e2e3905d648e336b33409f2d3b64
$ docker network inspect mynet -f '{{json .IPAM.Config}}' | jq .
[
  {
    "Subnet": "172.19.0.0/24",
    "Gateway": "172.19.0.1"
  },
  {
    "Subnet": "fdd3:6f80:972c::/56",
    "Gateway": "fdd3:6f80:972c::1"
  }
]
```

> Note
>
> Support for unspecified addresses in `--subnet` was introduced in Docker 29.0.0.
> If Docker is downgraded to an older version, networks created in this way will become unusable.
> They can be removed and re-created, or will function again if the daemon is restored to 29.0.0 or later.

## DNS services

Containers use the same DNS servers as the host by default, but you can
override this with `--dns`.

By default, containers inherit the DNS settings as defined in the
`/etc/resolv.conf` configuration file.
Containers that attach to the default `bridge` network receive a copy of this file.
Containers that attach to a
[custom network](https://docs.docker.com/engine/network/drivers/bridge/#use-user-defined-bridge-networks)
use Docker's embedded DNS server.
The embedded DNS server forwards external DNS lookups to the DNS servers configured on the host.

You can configure DNS resolution on a per-container basis, using flags for the
`docker run` or `docker create` command used to start the container.
The following table describes the available `docker run` flags related to DNS
configuration.

| Flag | Description |
| --- | --- |
| --dns | The IP address of a DNS server. To specify multiple DNS servers, use multiple--dnsflags. DNS requests will be forwarded from the container's network namespace so, for example,--dns=127.0.0.1refers to the container's own loopback address. |
| --dns-search | A DNS search domain to search non-fully qualified hostnames. To specify multiple DNS search prefixes, use multiple--dns-searchflags. |
| --dns-opt | A key-value pair representing a DNS option and its value. See your operating system's documentation forresolv.conffor valid options. |
| --hostname | The hostname a container uses for itself. Defaults to the container's ID if not specified. |

### Custom hosts

Your container will have lines in `/etc/hosts` which define the hostname of the
container itself, as well as `localhost` and a few other common things. Custom
hosts, defined in `/etc/hosts` on the host machine, aren't inherited by
containers. To pass additional hosts into a container, refer to
[add entries to
container hosts file](https://docs.docker.com/reference/cli/docker/container/run/#add-host) in the
`docker run` reference documentation.

## Container networks

In addition to user-defined networks, you can attach a container to another
container's networking stack directly, using the `--network container:<name|id>` flag format.

The following flags aren't supported for containers using the `container:`
networking mode:

- `--add-host`
- `--hostname`
- `--dns`
- `--dns-search`
- `--dns-option`
- `--mac-address`
- `--publish`
- `--publish-all`
- `--expose`

The following example runs a Redis container, with Redis binding to
127.0.0.1, then running the `redis-cli` command and connecting to the Redis
server over 127.0.0.1.

```console
$ docker run -d --name redis redis --bind 127.0.0.1
$ docker run --rm -it --network container:redis redis redis-cli -h 127.0.0.1
```

---

# Docker Engine 17.03 release notes

# Docker Engine 17.03 release notes

   Table of contents

---

## 17.03.3-ce

2018-08-30

### Runtime

- Update go-connections to d217f8e [#28](https://github.com/docker/engine/pull/28)

## 17.03.2-ce

2017-05-29

### Networking

- Fix a concurrency issue preventing network creation [#33273](https://github.com/moby/moby/pull/33273)

### Runtime

- Relabel secrets path to avoid a Permission Denied on selinux enabled systems [#33236](https://github.com/moby/moby/pull/33236) (ref [#32529](https://github.com/moby/moby/pull/32529)
- Fix cases where local volume were not properly relabeled if needed [#33236](https://github.com/moby/moby/pull/33236) (ref [#29428](https://github.com/moby/moby/pull/29428))
- Fix an issue while upgrading if a plugin rootfs was still mounted [#33236](https://github.com/moby/moby/pull/33236) (ref [#32525](https://github.com/moby/moby/pull/32525))
- Fix an issue where volume wouldn't default to the `rprivate` propagation mode [#33236](https://github.com/moby/moby/pull/33236) (ref [#32851](https://github.com/moby/moby/pull/32851))
- Fix a panic that could occur when a volume driver could not be retrieved [#33236](https://github.com/moby/moby/pull/33236) (ref [#32347](https://github.com/moby/moby/pull/32347))

- Add a warning in `docker info` when the `overlay` or `overlay2` graphdriver is used on a filesystem without `d_type` support [#33236](https://github.com/moby/moby/pull/33236) (ref [#31290](https://github.com/moby/moby/pull/31290))

- Fix an issue with backporting mount spec to older volumes [#33207](https://github.com/moby/moby/pull/33207)
- Fix issue where a failed unmount can lead to data loss on local volume remove [#33120](https://github.com/moby/moby/pull/33120)

### Swarm Mode

- Fix a case where tasks could get killed unexpectedly [#33118](https://github.com/moby/moby/pull/33118)
- Fix an issue preventing to deploy services if the registry cannot be reached despite the needed images being locally present [#33117](https://github.com/moby/moby/pull/33117)

## 17.03.1-ce

2017-03-27

### Remote API (v1.27) & Client

- Fix autoremove on older api [#31692](https://github.com/docker/docker/pull/31692)
- Fix default network customization for a stack [#31258](https://github.com/docker/docker/pull/31258/)
- Correct CPU usage calculation in presence of offline CPUs and newer Linux [#31802](https://github.com/docker/docker/pull/31802)
- Fix issue where service healthcheck is `{}` in remote API [#30197](https://github.com/docker/docker/pull/30197)

### Runtime

- Update runc to 54296cf40ad8143b62dbcaa1d90e520a2136ddfe [#31666](https://github.com/docker/docker/pull/31666)
- Ignore cgroup2 mountpoints [opencontainers/runc#1266](https://github.com/opencontainers/runc/pull/1266)
- Update containerd to 4ab9917febca54791c5f071a9d1f404867857fcc [#31662](https://github.com/docker/docker/pull/31662) [#31852](https://github.com/docker/docker/pull/31852)
- Register healtcheck service before calling restore() [docker/containerd#609](https://github.com/docker/containerd/pull/609)
- Fix `docker exec` not working after unattended upgrades that reload apparmor profiles [#31773](https://github.com/docker/docker/pull/31773)
- Fix unmounting layer without merge dir with Overlay2 [#31069](https://github.com/docker/docker/pull/31069)
- Do not ignore "volume in use" errors when force-delete [#31450](https://github.com/docker/docker/pull/31450)

### Swarm Mode

- Update swarmkit to 17756457ad6dc4d8a639a1f0b7a85d1b65a617bb [#31807](https://github.com/docker/docker/pull/31807)
- Scheduler now correctly considers tasks which have been assigned to a node but aren't yet running [docker/swarmkit#1980](https://github.com/docker/swarmkit/pull/1980)
- Allow removal of a network when only dead tasks reference it [docker/swarmkit#2018](https://github.com/docker/swarmkit/pull/2018)
- Retry failed network allocations less aggressively [docker/swarmkit#2021](https://github.com/docker/swarmkit/pull/2021)
- Avoid network allocation for tasks that are no longer running [docker/swarmkit#2017](https://github.com/docker/swarmkit/pull/2017)
- Bookkeeping fixes inside network allocator allocator [docker/swarmkit#2019](https://github.com/docker/swarmkit/pull/2019) [docker/swarmkit#2020](https://github.com/docker/swarmkit/pull/2020)

### Windows

- Cleanup HCS on restore [#31503](https://github.com/docker/docker/pull/31503)

## 17.03.0-ce

2017-03-01

> Important
>
> Starting with this release, Docker is on a monthly release cycle and uses a new YY.MM versioning scheme to reflect this. Two channels are available: monthly and quarterly. Any given monthly release will only receive security and bugfixes until the next monthly release is available. Quarterly releases receive security and bugfixes for 4 months after initial release. This release includes bugfixes for 1.13.1 but there are no major feature additions and the API version stays the same. Upgrading from Docker 1.13.1 to 17.03.0 is expected to be simple and low-risk.

### Client

- Fix panic in `docker stats --format` [#30776](https://github.com/docker/docker/pull/30776)

### Contrib

- Update various `bash` and `zsh` completion scripts [#30823](https://github.com/docker/docker/pull/30823), [#30945](https://github.com/docker/docker/pull/30945) and more...
- Block obsolete socket families in default seccomp profile - mitigates unpatched kernels' CVE-2017-6074 [#29076](https://github.com/docker/docker/pull/29076)

### Networking

- Fix bug on overlay encryption keys rotation in cross-datacenter swarm [#30727](https://github.com/docker/docker/pull/30727)
- Fix side effect panic in overlay encryption and network control plane communication failure ("No installed keys could decrypt the message") on frequent swarm leader re-election [#25608](https://github.com/docker/docker/pull/25608)
- Several fixes around system responsiveness and datapath programming when using overlay network with external kv-store [docker/libnetwork#1639](https://github.com/docker/libnetwork/pull/1639), [docker/libnetwork#1632](https://github.com/docker/libnetwork/pull/1632) and more...
- Discard incoming plain vxlan packets for encrypted overlay network [#31170](https://github.com/docker/docker/pull/31170)
- Release the network attachment on allocation failure [#31073](https://github.com/docker/docker/pull/31073)
- Fix port allocation when multiple published ports map to the same target port [docker/swarmkit#1835](https://github.com/docker/swarmkit/pull/1835)

### Runtime

- Fix a deadlock in docker logs [#30223](https://github.com/docker/docker/pull/30223)
- Fix CPU spin waiting for log write events [#31070](https://github.com/docker/docker/pull/31070)
- Fix a possible crash when using journald [#31231](https://github.com/docker/docker/pull/31231) [#31263](https://github.com/docker/docker/pull/31263)
- Fix a panic on close of nil channel [#31274](https://github.com/docker/docker/pull/31274)
- Fix duplicate mount point for `--volumes-from` in `docker run` [#29563](https://github.com/docker/docker/pull/29563)
- Fix `--cache-from` does not cache last step [#31189](https://github.com/docker/docker/pull/31189)

### Swarm Mode

- Shutdown leaks an error when the container was never started [#31279](https://github.com/docker/docker/pull/31279)
- Fix possibility of tasks getting stuck in the "NEW" state during a leader failover [docker/swarmkit#1938](https://github.com/docker/swarmkit/pull/1938)
- Fix extraneous task creations for global services that led to confusing replica counts in `docker service ls` [docker/swarmkit#1957](https://github.com/docker/swarmkit/pull/1957)
- Fix problem that made rolling updates slow when `task-history-limit` was set to 1 [docker/swarmkit#1948](https://github.com/docker/swarmkit/pull/1948)
- Restart tasks elsewhere, if appropriate, when they are shut down as a result of nodes no longer satisfying constraints [docker/swarmkit#1958](https://github.com/docker/swarmkit/pull/1958)
- (experimental)

---

# Docker Engine 17.04 release notes

# Docker Engine 17.04 release notes

   Table of contents

---

## 17.04.0-ce

2017-04-05

### Builder

- Disable container logging for build containers [#29552](https://github.com/docker/docker/pull/29552)
- Fix use of `**/` in `.dockerignore` [#29043](https://github.com/docker/docker/pull/29043)

### Client

- Sort `docker stack ls` by name [#31085](https://github.com/docker/docker/pull/31085)
- Flags for specifying bind mount consistency [#31047](https://github.com/docker/docker/pull/31047)

- Output of docker CLI --help is now wrapped to the terminal width [#28751](https://github.com/docker/docker/pull/28751)
- Suppress image digest in docker ps [#30848](https://github.com/docker/docker/pull/30848)
- Hide command options that are related to Windows [#30788](https://github.com/docker/docker/pull/30788)
- Fix `docker plugin install` prompt to accept "enter" for the "N" default [#30769](https://github.com/docker/docker/pull/30769)

- Add `truncate` function for Go templates [#30484](https://github.com/docker/docker/pull/30484)

- Support expanded syntax of ports in `stack deploy` [#30476](https://github.com/docker/docker/pull/30476)
- Support expanded syntax of mounts in `stack deploy` [#30597](https://github.com/docker/docker/pull/30597) [#31795](https://github.com/docker/docker/pull/31795)

- Add `--add-host` for docker build [#30383](https://github.com/docker/docker/pull/30383)
- Add `.CreatedAt` placeholder for `docker network ls --format` [#29900](https://github.com/docker/docker/pull/29900)

- Update order of `--secret-rm` and `--secret-add` [#29802](https://github.com/docker/docker/pull/29802)

- Add `--filter enabled=true` for `docker plugin ls` [#28627](https://github.com/docker/docker/pull/28627)
- Add `--format` to `docker service ls` [#28199](https://github.com/docker/docker/pull/28199)
- Add `publish` and `expose` filter for `docker ps --filter` [#27557](https://github.com/docker/docker/pull/27557)

- Support multiple service IDs on `docker service ps` [#25234](https://github.com/docker/docker/pull/25234)

- Allow swarm join with `--availability=drain` [#24993](https://github.com/docker/docker/pull/24993)

- Docker inspect now shows "docker-default" when AppArmor is enabled and no other profile was defined [#27083](https://github.com/docker/docker/pull/27083)

### Logging

- Implement optional ring buffer for container logs [#28762](https://github.com/docker/docker/pull/28762)
- Add `--log-opt awslogs-create-group=<true|false>` for awslogs (CloudWatch) to support creation of log groups as needed [#29504](https://github.com/docker/docker/pull/29504)

- Fix segfault when using the gcplogs logging driver with a "static" binary [#29478](https://github.com/docker/docker/pull/29478)

### Networking

- Check parameter `--ip`, `--ip6` and `--link-local-ip` in `docker network connect` [#30807](https://github.com/docker/docker/pull/30807)

- Added support for `dns-search` [#30117](https://github.com/docker/docker/pull/30117)
- Added --verbose option for docker network inspect to show task details from all swarm nodes [#31710](https://github.com/docker/docker/pull/31710)

- Clear stale datapath encryption states when joining the cluster [docker/libnetwork#1354](https://github.com/docker/libnetwork/pull/1354)

- Ensure iptables initialization only happens once [docker/libnetwork#1676](https://github.com/docker/libnetwork/pull/1676)

- Fix bad order of iptables filter rules [docker/libnetwork#961](https://github.com/docker/libnetwork/pull/961)

- Add anonymous container alias to service record on attachable network [docker/libnetwork#1651](https://github.com/docker/libnetwork/pull/1651)
- Support for `com.docker.network.container_iface_prefix` driver label [docker/libnetwork#1667](https://github.com/docker/libnetwork/pull/1667)
- Improve network list performance by omitting network details that are not used [#30673](https://github.com/docker/docker/pull/30673)

### Runtime

- Handle paused container when restoring without live-restore set [#31704](https://github.com/docker/docker/pull/31704)

- Do not allow sub second in healthcheck options in Dockerfile [#31177](https://github.com/docker/docker/pull/31177)

- Support name and id prefix in `secret update` [#30856](https://github.com/docker/docker/pull/30856)
- Use binary frame for websocket attach endpoint [#30460](https://github.com/docker/docker/pull/30460)
- Fix linux mount calls not applying propagation type changes [#30416](https://github.com/docker/docker/pull/30416)
- Fix ExecIds leak on failed `exec -i` [#30340](https://github.com/docker/docker/pull/30340)
- Prune named but untagged images if `danglingOnly=true` [#30330](https://github.com/docker/docker/pull/30330)

- Add daemon flag to set `no_new_priv` as default for unprivileged containers [#29984](https://github.com/docker/docker/pull/29984)
- Add daemon option `--default-shm-size` [#29692](https://github.com/docker/docker/pull/29692)
- Support registry mirror config reload [#29650](https://github.com/docker/docker/pull/29650)

- Ignore the daemon log config when building images [#29552](https://github.com/docker/docker/pull/29552)

- Move secret name or ID prefix resolving from client to daemon [#29218](https://github.com/docker/docker/pull/29218)

- Allow adding rules to `cgroup devices.allow` on container create/run [#22563](https://github.com/docker/docker/pull/22563)

- Fix `cpu.cfs_quota_us` being reset when running `systemd daemon-reload` [#31736](https://github.com/docker/docker/pull/31736)

### Swarm Mode

- Topology-aware scheduling [#30725](https://github.com/docker/docker/pull/30725)
- Automatic service rollback on failure [#31108](https://github.com/docker/docker/pull/31108)
- Worker and manager on the same node are now connected through a UNIX socket [docker/swarmkit#1828](https://github.com/docker/swarmkit/pull/1828), [docker/swarmkit#1850](https://github.com/docker/swarmkit/pull/1850), [docker/swarmkit#1851](https://github.com/docker/swarmkit/pull/1851)

- Improve raft transport package [docker/swarmkit#1748](https://github.com/docker/swarmkit/pull/1748)
- No automatic manager shutdown on demotion/removal [docker/swarmkit#1829](https://github.com/docker/swarmkit/pull/1829)
- Use TransferLeadership to make leader demotion safer [docker/swarmkit#1939](https://github.com/docker/swarmkit/pull/1939)
- Decrease default monitoring period [docker/swarmkit#1967](https://github.com/docker/swarmkit/pull/1967)

- Add Service logs formatting [#31672](https://github.com/docker/docker/pull/31672)

- Fix service logs API to be able to specify stream [#31313](https://github.com/docker/docker/pull/31313)

- Add `--stop-signal` for `service create` and `service update` [#30754](https://github.com/docker/docker/pull/30754)
- Add `--read-only` for `service create` and `service update` [#30162](https://github.com/docker/docker/pull/30162)
- Renew the context after communicating with the registry [#31586](https://github.com/docker/docker/pull/31586)
- (experimental) Add `--tail` and `--since` options to `docker service logs` [#31500](https://github.com/docker/docker/pull/31500)
- (experimental) Add `--no-task-ids` and `--no-trunc` options to `docker service logs` [#31672](https://github.com/docker/docker/pull/31672)

### Windows

- Block pulling Windows images on non-Windows daemons [#29001](https://github.com/docker/docker/pull/29001)

---

# Docker Engine 17.05 release notes

# Docker Engine 17.05 release notes

   Table of contents

---

## 17.05.0-ce

2017-05-04

### Builder

- Add multi-stage build support [#31257](https://github.com/docker/docker/pull/31257) [#32063](https://github.com/docker/docker/pull/32063)
- Allow using build-time args (`ARG`) in `FROM` [#31352](https://github.com/docker/docker/pull/31352)
- Add an option for specifying build target [#32496](https://github.com/docker/docker/pull/32496)

- Accept `-f -` to read Dockerfile from `stdin`, but use local context for building [#31236](https://github.com/docker/docker/pull/31236)
- The values of default build time arguments (e.g `HTTP_PROXY`) are no longer displayed in docker image history unless a corresponding `ARG` instruction is written in the Dockerfile. [#31584](https://github.com/docker/docker/pull/31584)

- Fix setting command if a custom shell is used in a parent image [#32236](https://github.com/docker/docker/pull/32236)
- Fix `docker build --label` when the label includes single quotes and a space [#31750](https://github.com/docker/docker/pull/31750)

### Client

- Add `--mount` flag to `docker run` and `docker create` [#32251](https://github.com/docker/docker/pull/32251)
- Add `--type=secret` to `docker inspect` [#32124](https://github.com/docker/docker/pull/32124)
- Add `--format` option to `docker secret ls` [#31552](https://github.com/docker/docker/pull/31552)
- Add `--filter` option to `docker secret ls` [#30810](https://github.com/docker/docker/pull/30810)
- Add `--filter scope=<swarm|local>` to `docker network ls` [#31529](https://github.com/docker/docker/pull/31529)
- Add `--cpus` support to `docker update` [#31148](https://github.com/docker/docker/pull/31148)
- Add label filter to `docker system prune` and other `prune` commands [#30740](https://github.com/docker/docker/pull/30740)
- `docker stack rm` now accepts multiple stacks as input [#32110](https://github.com/docker/docker/pull/32110)
- Improve `docker version --format` option when the client has downgraded the API version [#31022](https://github.com/docker/docker/pull/31022)
- Prompt when using an encrypted client certificate to connect to a docker daemon [#31364](https://github.com/docker/docker/pull/31364)
- Display created tags on successful `docker build` [#32077](https://github.com/docker/docker/pull/32077)
- Cleanup compose convert error messages [#32087](https://github.com/moby/moby/pull/32087)

### Contrib

- Add support for building docker debs for Ubuntu 17.04 Zesty on amd64 [#32435](https://github.com/docker/docker/pull/32435)

### Daemon

- Fix `--api-cors-header` being ignored if `--api-enable-cors` is not set [#32174](https://github.com/docker/docker/pull/32174)
- Cleanup docker tmp dir on start [#31741](https://github.com/docker/docker/pull/31741)
- Deprecate `--graph` flag in favor or `--data-root` [#28696](https://github.com/docker/docker/pull/28696)

### Logging

- Add support for logging driver plugins [#28403](https://github.com/docker/docker/pull/28403)

- Add support for showing logs of individual tasks to `docker service logs`, and add `/task/{id}/logs` REST endpoint [#32015](https://github.com/docker/docker/pull/32015)
- Add `--log-opt env-regex` option to match environment variables using a regular expression [#27565](https://github.com/docker/docker/pull/27565)

### Networking

- Allow user to replace, and customize the ingress network [#31714](https://github.com/docker/docker/pull/31714)

- Fix UDP traffic in containers not working after the container is restarted [#32505](https://github.com/docker/docker/pull/32505)
- Fix files being written to `/var/lib/docker` if a different data-root is set [#32505](https://github.com/docker/docker/pull/32505)

### Runtime

- Ensure health probe is stopped when a container exits [#32274](https://github.com/docker/docker/pull/32274)

### Swarm Mode

- Add update/rollback order for services (`--update-order` / `--rollback-order`) [#30261](https://github.com/docker/docker/pull/30261)
- Add support for synchronous `service create` and `service update` [#31144](https://github.com/docker/docker/pull/31144)
- Add support for "grace periods" on healthchecks through the `HEALTHCHECK --start-period` and `--health-start-period` flag to
  `docker service create`, `docker service update`, `docker create`, and `docker run` to support containers with an initial startup
  time [#28938](https://github.com/docker/docker/pull/28938)

- `docker service create` now omits fields that are not specified by the user, when possible. This will allow defaults to be applied inside the manager [#32284](https://github.com/docker/docker/pull/32284)
- `docker service inspect` now shows default values for fields that are not specified by the user [#32284](https://github.com/docker/docker/pull/32284)
- Move `docker service logs` out of experimental [#32462](https://github.com/docker/docker/pull/32462)
- Add support for Credential Spec and SELinux to services to the API [#32339](https://github.com/docker/docker/pull/32339)
- Add `--entrypoint` flag to `docker service create` and `docker service update` [#29228](https://github.com/docker/docker/pull/29228)
- Add `--network-add` and `--network-rm` to `docker service update` [#32062](https://github.com/docker/docker/pull/32062)
- Add `--credential-spec` flag to `docker service create` and `docker service update` [#32339](https://github.com/docker/docker/pull/32339)
- Add `--filter mode=<global|replicated>` to `docker service ls` [#31538](https://github.com/docker/docker/pull/31538)
- Resolve network IDs on the client side, instead of in the daemon when creating services [#32062](https://github.com/docker/docker/pull/32062)
- Add `--format` option to `docker node ls` [#30424](https://github.com/docker/docker/pull/30424)
- Add `--prune` option to `docker stack deploy` to remove services that are no longer defined in the docker-compose file [#31302](https://github.com/docker/docker/pull/31302)
- Add `PORTS` column for `docker service ls` when using `ingress` mode [#30813](https://github.com/docker/docker/pull/30813)

- Fix unnecessary re-deploying of tasks when environment-variables are used [#32364](https://github.com/docker/docker/pull/32364)
- Fix `docker stack deploy` not supporting `endpoint_mode` when deploying from a docker compose file [#32333](https://github.com/docker/docker/pull/32333)
- Proceed with startup if cluster component cannot be created to allow recovering from a broken swarm setup [#31631](https://github.com/docker/docker/pull/31631)

### Security

- Allow setting SELinux type or MCS labels when using `--ipc=container:` or `--ipc=host` [#30652](https://github.com/docker/docker/pull/30652)

### Deprecation

- Deprecate `--api-enable-cors` daemon flag. This flag was marked deprecated in Docker 1.6.0 but not listed in deprecated features [#32352](https://github.com/docker/docker/pull/32352)
- Remove Ubuntu 12.04 (Precise Pangolin) as supported platform. Ubuntu 12.04 is EOL, and no longer receives updates [#32520](https://github.com/docker/docker/pull/32520)

---

# Docker Engine 17.06 release notes

# Docker Engine 17.06 release notes

   Table of contents

---

## 17.06.2-ce

2017-09-05

### Client

- Enable TCP keepalive in the client to prevent loss of connection [docker/cli#415](https://github.com/docker/cli/pull/415)

### Runtime

- Devmapper: ensure UdevWait is called after calls to setCookie [moby/moby#33732](https://github.com/moby/moby/pull/33732)
- Aufs: ensure diff layers are correctly removed to prevent leftover files from using up storage [moby/moby#34587](https://github.com/moby/moby/pull/34587)

### Swarm mode

- Ignore PullOptions for running tasks [docker/swarmkit#2351](https://github.com/docker/swarmkit/pull/2351)

## 17.06.1-ce

2017-08-15

### Builder

- Fix a regression, where `ADD` from remote URL's extracted archives [#89](https://github.com/docker/docker-ce/pull/89)
- Fix handling of remote "git@" notation [#100](https://github.com/docker/docker-ce/pull/100)
- Fix copy `--from` conflict with force pull [#86](https://github.com/docker/docker-ce/pull/86)

### Client

- Make pruning volumes optional when running `docker system prune`, and add a `--volumes` flag [#109](https://github.com/docker/docker-ce/pull/109)
- Show progress of replicated tasks before they are assigned [#97](https://github.com/docker/docker-ce/pull/97)
- Fix `docker wait` hanging if the container does not exist [#106](https://github.com/docker/docker-ce/pull/106)
- If `docker swarm ca` is called without the `--rotate` flag, warn if other flags are passed [#110](https://github.com/docker/docker-ce/pull/110)
- Fix API version negotiation not working if the daemon returns an error [#115](https://github.com/docker/docker-ce/pull/115)
- Print an error if "until" filter is combined with "--volumes" on system prune [#154](https://github.com/docker/docker-ce/pull/154)

### Logging

- Fix stderr logging for `journald` and `syslog` [#95](https://github.com/docker/docker-ce/pull/95)
- Fix log readers can block writes indefinitely [#98](https://github.com/docker/docker-ce/pull/98)
- Fix `awslogs` driver repeating last event [#151](https://github.com/docker/docker-ce/pull/151)

### Networking

- Fix issue with driver options not received by network drivers [#127](https://github.com/docker/docker-ce/pull/127)

### Plugins

- Make plugin removes more resilient to failure [#91](https://github.com/docker/docker-ce/pull/91)

### Runtime

- Prevent a `goroutine` leak when `healthcheck` gets stopped [#90](https://github.com/docker/docker-ce/pull/90)
- Do not error on relabel when relabel not supported [#92](https://github.com/docker/docker-ce/pull/92)
- Limit max backoff delay to 2 seconds for GRPC connection [#94](https://github.com/docker/docker-ce/pull/94)
- Fix issue preventing containers to run when memory cgroup was specified due to bug in certain kernels [#102](https://github.com/docker/docker-ce/pull/102)
- Fix container not responding to SIGKILL when paused [#102](https://github.com/docker/docker-ce/pull/102)
- Improve error message if an image for an incompatible OS is loaded [#108](https://github.com/docker/docker-ce/pull/108)
- Fix a handle leak in `go-winio` [#112](https://github.com/docker/docker-ce/pull/112)
- Fix issue upon upgrade, preventing docker from showing running containers when `--live-restore` is enabled [#117](https://github.com/docker/docker-ce/pull/117)
- Fix bug where services using secrets would fail to start on daemons using the `userns-remap` feature [#121](https://github.com/docker/docker-ce/pull/121)
- Fix error handling with `not-exist` errors on remove [#142](https://github.com/docker/docker-ce/pull/142)
- Fix REST API Swagger representation cannot be loaded with SwaggerUI [#156](https://github.com/docker/docker-ce/pull/156)

### Security

- Redact secret data on secret creation [#99](https://github.com/docker/docker-ce/pull/99)

### Swarm mode

- Do not add duplicate platform information to service spec [#107](https://github.com/docker/docker-ce/pull/107)
- Cluster update and memory issue fixes [#114](https://github.com/docker/docker-ce/pull/114)
- Changing get network request to return predefined network in swarm [#150](https://github.com/docker/docker-ce/pull/150)

## 17.06.0-ce

2017-06-28

> Note
>
> of the `ADD` instruction of Dockerfile when referencing a remote `.tar.gz` file. The issue will be
> fixed in Docker 17.06.1.

> Note
>
> for IBM Z using the s390x architecture.

> Note
>
> registries. If you require interaction with registries that have not yet
> migrated to the v2 protocol, set the `--disable-legacy-registry=false` daemon
> option. Interaction with v1 registries will be removed in Docker 17.12.

### Builder

- Add `--iidfile` option to docker build. It allows specifying a location where to save the resulting image ID
- Allow specifying any remote ref in git checkout URLs [#32502](https://github.com/moby/moby/pull/32502)

### Client

- Add `--format` option to `docker stack ls` [#31557](https://github.com/moby/moby/pull/31557)
- Add support for labels in compose initiated builds [#32632](https://github.com/moby/moby/pull/32632) [#32972](https://github.com/moby/moby/pull/32972)
- Add `--format` option to `docker history` [#30962](https://github.com/moby/moby/pull/30962)
- Add `--format` option to `docker system df` [#31482](https://github.com/moby/moby/pull/31482)
- Allow specifying Nameservers and Search Domains in stack files [#32059](https://github.com/moby/moby/pull/32059)
- Add support for `read_only` service to `docker stack deploy` [#docker/cli/73](https://github.com/docker/cli/pull/73)

- Display Swarm cluster and node TLS information [#docker/cli/44](https://github.com/docker/cli/pull/44)

- Add support for placement preference to `docker stack deploy` [#docker/cli/35](https://github.com/docker/cli/pull/35)
- Add new `ca` subcommand to `docker swarm` to allow managing a swarm CA [#docker/cli/48](https://github.com/docker/cli/pull/48)
- Add credential-spec to compose [#docker/cli/71](https://github.com/docker/cli/pull/71)
- Add support for csv format options to `--network` and `--network-add` [#docker/cli/62](https://github.com/docker/cli/pull/62) [#33130](https://github.com/moby/moby/pull/33130)

- Fix stack compose bind-mount volumes on Windows [#docker/cli/136](https://github.com/docker/cli/pull/136)
- Correctly handle a Docker daemon without registry info [#docker/cli/126](https://github.com/docker/cli/pull/126)

- Allow `--detach` and `--quiet` flags when using --rollback [#docker/cli/144](https://github.com/docker/cli/pull/144)
- Remove deprecated `--email` flag from `docker login` [#docker/cli/143](https://github.com/docker/cli/pull/143)

- Adjusted `docker stats` memory output [#docker/cli/80](https://github.com/docker/cli/pull/80)

### Distribution

- Select digest over tag when both are provided during a pull [#33214](https://github.com/moby/moby/pull/33214)

### Logging

- Add monitored resource type metadata for GCP logging driver [#32930](https://github.com/moby/moby/pull/32930)
- Add multiline processing to the AWS CloudWatch logs driver [#30891](https://github.com/moby/moby/pull/30891)

### Networking

- Add Support swarm-mode services with node-local networks such as macvlan, ipvlan, bridge, host [#32981](https://github.com/moby/moby/pull/32981)
- Pass driver-options to network drivers on service creation [#32981](https://github.com/moby/moby/pull/33130)
- Isolate Swarm Control-plane traffic from Application data traffic using --data-path-addr [#32717](https://github.com/moby/moby/pull/32717)

- Several improvements to Service Discovery [#docker/libnetwork/1796](https://github.com/docker/libnetwork/pull/1796)

### Packaging

- Rely on `container-selinux` on Centos/Fedora/RHEL when available [#32437](https://github.com/moby/moby/pull/32437)

### Runtime

- Add build & engine info prometheus metrics [#32792](https://github.com/moby/moby/pull/32792)

- Update containerd to d24f39e203aa6be4944f06dd0fe38a618a36c764 [#33007](https://github.com/moby/moby/pull/33007)
- Update runc to 992a5be178a62e026f4069f443c6164912adbf09 [#33007](https://github.com/moby/moby/pull/33007)

- Add option to auto-configure blkdev for devmapper [#31104](https://github.com/moby/moby/pull/31104)
- Add log driver list to `docker info` [#32540](https://github.com/moby/moby/pull/32540)
- Add API endpoint to allow retrieving an image manifest [#32061](https://github.com/moby/moby/pull/32061)

- Do not remove container from memory on error with `forceremove` [#31012](https://github.com/moby/moby/pull/31012)

- Add support for metric plugins [#32874](https://github.com/moby/moby/pull/32874)

- Return an error when an invalid filter is given to `prune` commands [#33023](https://github.com/moby/moby/pull/33023)

- Add daemon option to allow pushing foreign layers [#33151](https://github.com/moby/moby/pull/33151)

- Fix an issue preventing containerd to be restarted after it died [#32986](https://github.com/moby/moby/pull/32986)

- Add cluster events to Docker event stream. [#32421](https://github.com/moby/moby/pull/32421)
- Add support for DNS search on windows [#33311](https://github.com/moby/moby/pull/33311)

- Upgrade to Go 1.8.3 [#33387](https://github.com/moby/moby/pull/33387)

- Prevent a containerd crash when journald is restarted [#containerd/930](https://github.com/containerd/containerd/pull/930)
- Fix healthcheck failures due to invalid environment variables [#33249](https://github.com/moby/moby/pull/33249)
- Prevent a directory to be created in lieu of the daemon socket when a container mounting it is to be restarted during a shutdown [#30348](https://github.com/moby/moby/pull/33330)
- Prevent a container to be restarted upon stop if its stop signal is set to `SIGKILL` [#33335](https://github.com/moby/moby/pull/33335)
- Ensure log drivers get passed the same filename to both StartLogging and StopLogging endpoints [#33583](https://github.com/moby/moby/pull/33583)
- Remove daemon data structure dump on `SIGUSR1` to avoid a panic [#33598](https://github.com/moby/moby/pull/33598)

### Security

- Allow personality with UNAME26 bit set in default seccomp profile [#32965](https://github.com/moby/moby/pull/32965)

### Swarm Mode

- Add an option to allow specifying a different interface for the data traffic (as opposed to control traffic) [#32717](https://github.com/moby/moby/pull/32717)

- Allow specifying a secret location within the container [#32571](https://github.com/moby/moby/pull/32571)

- Add support for secrets on Windows [#32208](https://github.com/moby/moby/pull/32208)
- Add TLS Info to swarm info and node info endpoint [#32875](https://github.com/moby/moby/pull/32875)
- Add support for services to carry arbitrary config objects [#32336](https://github.com/moby/moby/pull/32336), [#docker/cli/45](https://github.com/docker/cli/pull/45),[#33169](https://github.com/moby/moby/pull/33169)
- Add API to rotate swarm CA certificate [#32993](https://github.com/moby/moby/pull/32993)

- Service digest pining is now handled client side [#32388](https://github.com/moby/moby/pull/32388), [#33239](https://github.com/moby/moby/pull/33239)

- Placement now also take platform in account [#33144](https://github.com/moby/moby/pull/33144)

- Fix possible hang when joining fails [#docker-ce/19](https://github.com/docker/docker-ce/pull/19)
- Fix an issue preventing external CA to be accepted [#33341](https://github.com/moby/moby/pull/33341)
- Fix possible orchestration panic in mixed version clusters [#swarmkit/2233](https://github.com/docker/swarmkit/pull/2233)
- Avoid assigning duplicate IPs during initialization [#swarmkit/2237](https://github.com/docker/swarmkit/pull/2237)

### Deprecation

- Disable legacy registry (v1) by default [#33629](https://github.com/moby/moby/pull/33629)

---

# Docker Engine 17.07 release notes

# Docker Engine 17.07 release notes

   Table of contents

---

## 17.07.0-ce

2017-08-29

### API & Client

- Add support for proxy configuration in config.json [docker/cli#93](https://github.com/docker/cli/pull/93)
- Enable pprof/debug endpoints by default [moby/moby#32453](https://github.com/moby/moby/pull/32453)
- Passwords can now be passed using `STDIN` using the new `--password-stdin` flag on `docker login` [docker/cli#271](https://github.com/docker/cli/pull/271)

- Add `--detach` to docker scale [docker/cli#243](https://github.com/docker/cli/pull/243)

- Prevent `docker logs --no-stream` from hanging due to non-existing containers [moby/moby#34004](https://github.com/moby/moby/pull/34004)

- Fix `docker stack ps` printing error to `stdout` instead of `stderr` [docker/cli#298](https://github.com/docker/cli/pull/298)

- Fix progress bar being stuck on `docker service create` if an error occurs during deploy [docker/cli#259](https://github.com/docker/cli/pull/259)
- Improve presentation of progress bars in interactive mode [docker/cli#260](https://github.com/docker/cli/pull/260) [docker/cli#237](https://github.com/docker/cli/pull/237)
- Print a warning if `docker login --password` is used, and recommend `--password-stdin` [docker/cli#270](https://github.com/docker/cli/pull/270)
- Make API version negotiation more robust [moby/moby#33827](https://github.com/moby/moby/pull/33827)
- Hide `--detach` when connected to daemons older than Docker 17.05 [docker/cli#219](https://github.com/docker/cli/pull/219)

- Add `scope` filter in `GET /networks/(id or name)` [moby/moby#33630](https://github.com/moby/moby/pull/33630)

### Builder

- Implement long running interactive session and sending build context incrementally [moby/moby#32677](https://github.com/moby/moby/pull/32677) [docker/cli#231](https://github.com/docker/cli/pull/231) [moby/moby#33859](https://github.com/moby/moby/pull/33859)
- Warn on empty continuation lines [moby/moby#33719](https://github.com/moby/moby/pull/33719)

- Fix `.dockerignore` entries with a leading `/` not matching anything [moby/moby#32088](https://github.com/moby/moby/pull/32088)

### Logging

- Fix wrong filemode for rotate log files [moby/moby#33926](https://github.com/moby/moby/pull/33926)
- Fix stderr logging for journald and syslog [moby/moby#33832](https://github.com/moby/moby/pull/33832)

### Runtime

- Allow stopping of paused container [moby/moby#34027](https://github.com/moby/moby/pull/34027)

- Add quota support for the overlay2 storage driver [moby/moby#32977](https://github.com/moby/moby/pull/32977)

- Remove container locks on `docker ps` [moby/moby#31273](https://github.com/moby/moby/pull/31273)
- Store container names in memdb [moby/moby#33886](https://github.com/moby/moby/pull/33886)
- Fix race condition between `docker exec` and `docker pause` [moby/moby#32881](https://github.com/moby/moby/pull/32881)
- Devicemapper: Rework logging and add `--storage-opt dm.libdm_log_level` [moby/moby#33845](https://github.com/moby/moby/pull/33845)
- Devicemapper: Prevent "device in use" errors if deferred removal is enabled, but not deferred deletion [moby/moby#33877](https://github.com/moby/moby/pull/33877)
- Devicemapper: Use KeepAlive to prevent tasks being garbage-collected while still in use [moby/moby#33376](https://github.com/moby/moby/pull/33376)
- Report intermediate prune results if prune is cancelled [moby/moby#33979](https://github.com/moby/moby/pull/33979)

- Fix run `docker rename <container-id> new_name` concurrently resulting in the having multiple names [moby/moby#33940](https://github.com/moby/moby/pull/33940)

- Fix file-descriptor leak and error handling [moby/moby#33713](https://github.com/moby/moby/pull/33713)

- Fix SIGSEGV when running containers [docker/cli#303](https://github.com/docker/cli/pull/303)

- Prevent a goroutine leak when healthcheck gets stopped [moby/moby#33781](https://github.com/moby/moby/pull/33781)
- Image: Improve store locking [moby/moby#33755](https://github.com/moby/moby/pull/33755)
- Fix Btrfs quota groups not being removed when container is destroyed [moby/moby#29427](https://github.com/moby/moby/pull/29427)
- Libcontainerd: fix defunct containerd processes not being properly reaped [moby/moby#33419](https://github.com/moby/moby/pull/33419)
- Preparations for Linux Containers on Windows
  - LCOW: Dedicated scratch space for service VM utilities [moby/moby#33809](https://github.com/moby/moby/pull/33809)
  - LCOW: Support most operations excluding remote filesystem [moby/moby#33241](https://github.com/moby/moby/pull/33241) [moby/moby#33826](https://github.com/moby/moby/pull/33826)
  - LCOW: Change directory from lcow to "Linux Containers" [moby/moby#33835](https://github.com/moby/moby/pull/33835)
  - LCOW: pass command arguments without extra quoting [moby/moby#33815](https://github.com/moby/moby/pull/33815)
  - LCOW: Updates necessary due to platform schema change [moby/moby#33785](https://github.com/moby/moby/pull/33785)

### Swarm mode

- Initial support for plugable secret backends [moby/moby#34157](https://github.com/moby/moby/pull/34157) [moby/moby#34123](https://github.com/moby/moby/pull/34123)
- Sort swarm stacks and nodes using natural sorting [docker/cli#315](https://github.com/docker/cli/pull/315)
- Make engine support cluster config event [moby/moby#34032](https://github.com/moby/moby/pull/34032)
- Only pass a join address when in the process of joining a cluster [moby/moby#33361](https://github.com/moby/moby/pull/33361)
- Fix error during service creation if a network with the same name exists both as "local" and "swarm" scoped network [docker/cli#184](https://github.com/docker/cli/pull/184)
- (experimental) Add support for plugins on swarm [moby/moby#33575](https://github.com/moby/moby/pull/33575)
