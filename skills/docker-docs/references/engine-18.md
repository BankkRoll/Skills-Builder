# Legacy container links and more

# Legacy container links

> Learn how to connect Docker containers together.

# Legacy container links

   Table of contents

---

> Warning
>
> The `--link` flag is a legacy feature of Docker. It may eventually
> be removed. Unless you absolutely need to continue using it, we recommend that you use
> user-defined networks to facilitate communication between two containers instead of using
> `--link`. One feature that user-defined networks do not support that you can do
> with `--link` is sharing environment variables between containers. However,
> you can use other mechanisms such as volumes to share environment variables
> between containers in a more controlled way.
>
>
>
> See [Differences between user-defined bridges and the default bridge](https://docs.docker.com/engine/network/drivers/bridge/#differences-between-user-defined-bridges-and-the-default-bridge)
> for some alternatives to using `--link`.

The information in this section explains legacy container links within the
Docker default `bridge` network which is created automatically when you install
Docker.

Before the [Docker networks feature](https://docs.docker.com/engine/network/), you could use the
Docker link feature to allow containers to discover each other and securely
transfer information about one container to another container. With the
introduction of the Docker networks feature, you can still create links but they
behave differently between default `bridge` network and
[user defined networks](https://docs.docker.com/engine/network/drivers/bridge/#differences-between-user-defined-bridges-and-the-default-bridge).

This section briefly discusses connecting via a network port and then goes into
detail on container linking in default `bridge` network.

## Connect using network port mapping

Let's say you used this command to run a simple Python Flask application:

```console
$ docker run -d -P training/webapp python app.py
```

When that container was created, the `-P` flag was used to automatically map
any network port inside it to a random high port within an *ephemeral port
range* on your Docker host. Next, when `docker ps` was run, you saw that port
5000 in the container was bound to port 49155 on the host.

```console
$ docker ps nostalgic_morse

CONTAINER ID  IMAGE                   COMMAND       CREATED        STATUS        PORTS                    NAMES
bc533791f3f5  training/webapp:latest  python app.py 5 seconds ago  Up 2 seconds  0.0.0.0:49155->5000/tcp  nostalgic_morse
```

You also saw how you can bind a container's ports to a specific port using
the `-p` flag. Here port 80 of the host is mapped to port 5000 of the
container:

```console
$ docker run -d -p 80:5000 training/webapp python app.py
```

And you saw why this isn't such a great idea because it constrains you to
only one container on that specific port.

Instead, you may specify a range of host ports to bind a container port to
that is different than the default *ephemeral port range*:

```console
$ docker run -d -p 8000-9000:5000 training/webapp python app.py
```

This would bind port 5000 in the container to a randomly available port
between 8000 and 9000 on the host.

There are also a few other ways you can configure the `-p` flag. By
default the `-p` flag binds the specified port to all interfaces on
the host machine. But you can also specify a binding to a specific
interface, for example only to the `localhost`.

```console
$ docker run -d -p 127.0.0.1:80:5000 training/webapp python app.py
```

This would bind port 5000 inside the container to port 80 on the
`localhost` or `127.0.0.1` interface on the host machine.

Or, to bind port 5000 of the container to a dynamic port but only on the
`localhost`, you could use:

```console
$ docker run -d -p 127.0.0.1::5000 training/webapp python app.py
```

You can also bind UDP and SCTP (typically used by telecom protocols such as SIGTRAN, Diameter, and S1AP/X2AP) ports by adding a trailing `/udp` or `/sctp`. For example:

```console
$ docker run -d -p 127.0.0.1:80:5000/udp training/webapp python app.py
```

You also learned about the useful `docker port` shortcut which showed us the
current port bindings. This is also useful for showing you specific port
configurations. For example, if you've bound the container port to the
`localhost` on the host machine, then the `docker port` output reflects that.

```console
$ docker port nostalgic_morse 5000

127.0.0.1:49155
```

> Note
>
> The `-p` flag can be used multiple times to configure multiple ports.

## Connect with the linking system

> Note
>
> This section covers the legacy link feature in the default `bridge` network.
> Refer to [differences between user-defined bridges and the default bridge](https://docs.docker.com/engine/network/drivers/bridge/#differences-between-user-defined-bridges-and-the-default-bridge)
> for more information on links in user-defined networks.

Network port mappings are not the only way Docker containers can connect to one
another. Docker also has a linking system that allows you to link multiple
containers together and send connection information from one to another. When
containers are linked, information about a source container can be sent to a
recipient container. This allows the recipient to see selected data describing
aspects of the source container.

### The importance of naming

To establish links, Docker relies on the names of your containers.
You've already seen that each container you create has an automatically
created name; indeed you've become familiar with our old friend
`nostalgic_morse` during this guide. You can also name containers
yourself. This naming provides two useful functions:

1. It can be useful to name containers that do specific functions in a way
  that makes it easier for you to remember them, for example naming a
  container containing a web application `web`.
2. It provides Docker with a reference point that allows it to refer to other
  containers, for example, you can specify to link the container `web` to container `db`.

You can name your container by using the `--name` flag, for example:

```console
$ docker run -d -P --name web training/webapp python app.py
```

This launches a new container and uses the `--name` flag to
name the container `web`. You can see the container's name using the
`docker ps` command.

```console
$ docker ps -l

CONTAINER ID  IMAGE                  COMMAND        CREATED       STATUS       PORTS                    NAMES
aed84ee21bde  training/webapp:latest python app.py  12 hours ago  Up 2 seconds 0.0.0.0:49154->5000/tcp  web
```

You can also use `docker inspect` to return the container's name.

> Note
>
> Container names must be unique. That means you can only call
> one container `web`. If you want to re-use a container name you must delete
> the old container (with `docker container rm`) before you can create a new
> container with the same name. As an alternative you can use the `--rm`
> flag with the `docker run` command. This deletes the container
> immediately after it is stopped.

## Communication across links

Links allow containers to discover each other and securely transfer information
about one container to another container. When you set up a link, you create a
conduit between a source container and a recipient container. The recipient can
then access select data about the source. To create a link, you use the `--link`
flag. First, create a new container, this time one containing a database.

```console
$ docker run -d --name db training/postgres
```

This creates a new container called `db` from the `training/postgres`
image, which contains a PostgreSQL database.

Now, you need to delete the `web` container you created previously so you can replace it
with a linked one:

```console
$ docker container rm -f web
```

Now, create a new `web` container and link it with your `db` container.

```console
$ docker run -d -P --name web --link db:db training/webapp python app.py
```

This links the new `web` container with the `db` container you created
earlier. The `--link` flag takes the form:

```
--link <name or id>:alias
```

Where `name` is the name of the container we're linking to and `alias` is an
alias for the link name. That alias is used shortly.
The `--link` flag also takes the form:

```
--link <name or id>
```

In this case the alias matches the name. You could write the previous
example as:

```console
$ docker run -d -P --name web --link db training/webapp python app.py
```

Next, inspect your linked containers with `docker inspect`:

```console
$ docker inspect -f "{{ .HostConfig.Links }}" web

[/db:/web/db]
```

You can see that the `web` container is now linked to the `db` container
`web/db`. Which allows it to access information about the `db` container.

So what does linking the containers actually do? You've learned that a link allows a
source container to provide information about itself to a recipient container. In
our example, the recipient, `web`, can access information about the source `db`. To do
this, Docker creates a secure tunnel between the containers that doesn't need to
expose any ports externally on the container; when we started the
`db` container we did not use either the `-P` or `-p` flags. That's a big benefit of
linking: we don't need to expose the source container, here the PostgreSQL database, to
the network.

Docker exposes connectivity information for the source container to the
recipient container in two ways:

- Environment variables,
- Updating the `/etc/hosts` file.

### Environment variables

Docker creates several environment variables when you link containers. Docker
automatically creates environment variables in the target container based on
the `--link` parameters. It also exposes all environment variables
originating from Docker from the source container. These include variables from:

- the `ENV` commands in the source container's Dockerfile
- the `-e`, `--env`, and `--env-file` options on the `docker run`
  command when the source container is started

These environment variables enable programmatic discovery from within the
target container of information related to the source container.

> Warning
>
> It is important to understand that all environment variables originating
> from Docker within a container are made available to any container
> that links to it. This could have serious security implications if sensitive
> data is stored in them.

Docker sets an `<alias>_NAME` environment variable for each target container
listed in the `--link` parameter. For example, if a new container called
`web` is linked to a database container called `db` via `--link db:webdb`,
then Docker creates a `WEBDB_NAME=/web/webdb` variable in the `web` container.

Docker also defines a set of environment variables for each port exposed by the
source container. Each variable has a unique prefix in the form `<name>_PORT_<port>_<protocol>`

The components in this prefix are:

- the alias `<name>` specified in the `--link` parameter (for example, `webdb`)
- the `<port>` number exposed
- a `<protocol>` which is either TCP or UDP

Docker uses this prefix format to define three distinct environment variables:

- The `prefix_ADDR` variable contains the IP Address from the URL, for
  example `WEBDB_PORT_5432_TCP_ADDR=172.17.0.82`.
- The `prefix_PORT` variable contains just the port number from the URL of
  example `WEBDB_PORT_5432_TCP_PORT=5432`.
- The `prefix_PROTO` variable contains just the protocol from the URL of
  example `WEBDB_PORT_5432_TCP_PROTO=tcp`.

If the container exposes multiple ports, an environment variable set is
defined for each one. This means, for example, if a container exposes 4 ports
that Docker creates 12 environment variables, 3 for each port.

Additionally, Docker creates an environment variable called `<alias>_PORT`.
This variable contains the URL of the source container's first exposed port.
The 'first' port is defined as the exposed port with the lowest number.
For example, consider the `WEBDB_PORT=tcp://172.17.0.82:5432` variable. If
that port is used for both tcp and udp, then the tcp one is specified.

Finally, Docker also exposes each Docker originated environment variable
from the source container as an environment variable in the target. For each
variable Docker creates an `<alias>_ENV_<name>` variable in the target
container. The variable's value is set to the value Docker used when it
started the source container.

Returning back to our database example, you can run the `env`
command to list the specified container's environment variables.

```console
$ docker run --rm --name web2 --link db:db training/webapp env

<...>
DB_NAME=/web2/db
DB_PORT=tcp://172.17.0.5:5432
DB_PORT_5432_TCP=tcp://172.17.0.5:5432
DB_PORT_5432_TCP_PROTO=tcp
DB_PORT_5432_TCP_PORT=5432
DB_PORT_5432_TCP_ADDR=172.17.0.5
<...>
```

You can see that Docker has created a series of environment variables with
useful information about the source `db` container. Each variable is prefixed
with
`DB_`, which is populated from the `alias` you specified above. If the `alias`
were `db1`, the variables would be prefixed with `DB1_`. You can use these
environment variables to configure your applications to connect to the database
on the `db` container. The connection is secure and private; only the
linked `web` container can communicate with the `db` container.

### Important notes on Docker environment variables

Unlike host entries in the [/etc/hostsfile](#updating-the-etchosts-file),
IP addresses stored in the environment variables are not automatically updated
if the source container is restarted. We recommend using the host entries in
`/etc/hosts` to resolve the IP address of linked containers.

These environment variables are only set for the first process in the
container. Some daemons, such as `sshd`, scrub them when spawning shells
for connection.

### Updating the/etc/hostsfile

In addition to the environment variables, Docker adds a host entry for the
source container to the `/etc/hosts` file. Here's an entry for the `web`
container:

```console
$ docker run -t -i --rm --link db:webdb training/webapp /bin/bash

root@aed84ee21bde:/opt/webapp# cat /etc/hosts
172.17.0.7  aed84ee21bde
<...>
172.17.0.5  webdb 6e5cdeb2d300 db
```

You can see two relevant host entries. The first is an entry for the `web`
container that uses the Container ID as a host name. The second entry uses the
link alias to reference the IP address of the `db` container. In addition to
the alias you provide, the linked container's name, if unique from the alias
provided to the `--link` parameter, and the linked container's hostname are
also added to `/etc/hosts` for the linked container's IP address. You can ping
that host via any of these entries:

```console
root@aed84ee21bde:/opt/webapp# apt-get install -yqq inetutils-ping
root@aed84ee21bde:/opt/webapp# ping webdb

PING webdb (172.17.0.5): 48 data bytes
56 bytes from 172.17.0.5: icmp_seq=0 ttl=64 time=0.267 ms
56 bytes from 172.17.0.5: icmp_seq=1 ttl=64 time=0.250 ms
56 bytes from 172.17.0.5: icmp_seq=2 ttl=64 time=0.256 ms
```

> Note
>
> In the example, you had to install `ping` because it was not included
> in the container initially.

Here, you used the `ping` command to ping the `db` container using its host entry,
which resolves to `172.17.0.5`. You can use this host entry to configure an application
to make use of your `db` container.

> Note
>
> You can link multiple recipient containers to a single source. For
> example, you could have multiple (differently named) web containers attached to your
> `db` container.

If you restart the source container, the `/etc/hosts` files on the linked containers
are automatically updated with the source container's new IP address,
allowing linked communication to continue.

```console
$ docker restart db
db

$ docker run -t -i --rm --link db:db training/webapp /bin/bash

root@aed84ee21bde:/opt/webapp# cat /etc/hosts
172.17.0.7  aed84ee21bde
<...>
172.17.0.9  db
```

---

# Packet filtering and firewalls

> How Docker works with packet filtering, iptables, and firewalls

# Packet filtering and firewalls

   Table of contents

---

On Linux, Docker creates firewall rules to implement network
isolation, [port publishing](https://docs.docker.com/engine/network/port-publishing/) and filtering.

Because these rules are required for the correct functioning of Docker bridge
networks, you should not modify the rules created by Docker.

This page describes options that control Docker's firewall rules to
implement functionality including port publishing, and NAT/masquerading.

> Note
>
> Docker creates firewall rules for bridge networks.
>
>
>
> No rules are created for `ipvlan`, `macvlan` or `host` networking.

## Firewall backend

By default, Docker Engine creates its firewall rules using iptables,
see [Docker with iptables](https://docs.docker.com/engine/network/firewall-iptables/). It also has
support for nftables, see [Docker with nftables](https://docs.docker.com/engine/network/firewall-nftables/).

For bridge networks, iptables and nftables have the same functionality.

Docker Engine option `firewall-backend` can be used to select whether
iptables or nftables is used. See
[daemon configuration](https://docs.docker.com/reference/cli/dockerd/).

## Docker on a router

On Linux, Docker needs "IP Forwarding" enabled on the host. So, it enables
the `sysctl` settings `net.ipv4.ip_forward` and `net.ipv6.conf.all.forwarding`
if they are not already enabled when it starts. When it does that, it also
configures the firewall to drop forwarded packets unless they are explicitly
accepted.

When Docker sets the default forwarding policy to "drop", it will prevent
your Docker host from acting as a router. This is the recommended setting when
IP Forwarding is enabled, unless router functionality is required.

To stop Docker from setting the forwarding policy to "drop", include
`"ip-forward-no-drop": true` in `/etc/docker/daemon.json`, or add option
`--ip-forward-no-drop` to the `dockerd` command line.

> Note
>
> With the experimental nftables backend, Docker does not enable IP forwarding
> itself, and it will not create a default "drop" nftables policy. See
> [Migrating from iptables to nftables](https://docs.docker.com/engine/network/firewall-nftables/#migrating-from-iptables-to-nftables).

## Prevent Docker from manipulating firewall rules

Setting the `iptables` or `ip6tables` keys to `false` in
[daemon configuration](https://docs.docker.com/reference/cli/dockerd/), will
prevent Docker from creating most of its `iptables` or `nftables` rules. But,
this option is not appropriate for most users, it is likely to break
container networking for the Docker Engine.

For example, with Docker's firewalling disabled and no replacement
rules, containers in bridge networks will not be able to access
internet hosts by masquerading, but all of their ports will be accessible
to hosts on the local network.

It is not possible to completely prevent Docker from creating firewall
rules, and creating rules after-the-fact is extremely involved and beyond
the scope of these instructions.

## Integration with firewalld

If you are running Docker with the `iptables` or `ip6tables` options set to
`true`, and [firewalld](https://firewalld.org) is enabled on your system, in
addition to its usual iptables or nftables rules, Docker creates a `firewalld`
zone called `docker`, with target `ACCEPT`.

All bridge network interfaces created by Docker (for example, `docker0`) are
inserted into the `docker` zone.

Docker also creates a forwarding policy called `docker-forwarding` that allows
forwarding from `ANY` zone to the `docker` zone.

## Docker and ufw

[Uncomplicated Firewall](https://launchpad.net/ufw)
(ufw) is a frontend that ships with Debian and Ubuntu,
and it lets you manage firewall rules. Docker and ufw use firewall rules in
ways that make them incompatible with each other.

When you publish a container's ports using Docker, traffic to and from that
container gets diverted before it goes through the ufw firewall settings.
Docker routes container traffic in the `nat` table, which means that packets
are diverted before it reaches the `INPUT` and `OUTPUT` chains that ufw uses.
Packets are routed before the firewall rules can be applied,
effectively ignoring your firewall configuration.

---

# Port publishing and mapping

> Accessing container ports

# Port publishing and mapping

   Table of contents

---

By default, for both IPv4 and IPv6, the Docker daemon blocks access to ports that
have not been published. Published container ports are mapped to host IP addresses.
To do this, it uses firewall rules to perform Network Address Translation (NAT),
Port Address Translation (PAT), and masquerading.

For example, `docker run -p 8080:80 [...]` creates a mapping
between port 8080 on any address on the Docker host, and the container's
port 80. Outgoing connections from the container will masquerade, using
the Docker host's IP address.

## Publishing ports

When you create or run a container using `docker create` or `docker run`, all
ports of containers on bridge networks are accessible from the Docker host and
other containers connected to the same network. Ports are not accessible from
outside the host or, with the default configuration, from containers in other
networks.

Use the `--publish` or `-p` flag to make a port available outside the host,
and to containers in other bridge networks.

This creates a firewall rule in the host,
mapping a container port to a port on the Docker host to the outside world.
Here are some examples:

| Flag value | Description |
| --- | --- |
| -p 8080:80 | Map port8080on the Docker host to TCP port80in the container. |
| -p 192.168.1.100:8080:80 | Map port8080on the Docker host IP192.168.1.100to TCP port80in the container. |
| -p 8080:80/udp | Map port8080on the Docker host to UDP port80in the container. |
| -p 8080:80/tcp -p 8080:80/udp | Map TCP port8080on the Docker host to TCP port80in the container, and map UDP port8080on the Docker host to UDP port80in the container. |

> Important
>
> Publishing container ports is insecure by default. Meaning, when you publish
> a container's ports it becomes available not only to the Docker host, but to
> the outside world as well.
>
>
>
> If you include the localhost IP address (`127.0.0.1`, or `::1`) with the
> publish flag, only the Docker host can access the published container port.
>
>
>
> ```console
> $ docker run -p 127.0.0.1:8080:80 -p '[::1]:8080:80' nginx
> ```
>
>
>
> > Warning
> >
> > In releases older than 28.0.0, hosts within the same L2 segment (for example,
> > hosts connected to the same network switch) can reach ports published to localhost.
> > For more information, see
> > [moby/moby#45610](https://github.com/moby/moby/issues/45610)

Ports on the host's IPv6 addresses will map to the container's IPv4 address
if no host IP is given in a port mapping, the bridge network is IPv4-only,
and `--userland-proxy=true` (default).

## Direct routing

Port mapping ensures that published ports are accessible on the host's
network addresses, which are likely to be routable for any external
clients. No routes are normally set up in the host's network for container
addresses that exist within a host.

But, particularly with IPv6 you may prefer to avoid using NAT and instead
arrange for external routing to container addresses ("direct routing").

To access containers on a bridge network from outside the Docker host,
you must first set up routing to the bridge network via an address on the
Docker host. This can be achieved using static routes, Border Gateway Protocol (BGP),
or any other means appropriate for your network. For example, within
a local layer 2 network, remote hosts can set up static routes to a container
network via the Docker daemon host's address on the local network.

### Direct routing to containers in bridge networks

By default, remote hosts are not allowed direct access to container IP
addresses in Docker's Linux bridge networks. They can only access ports
published to host IP addresses.

To allow direct access to any published port, on any container, in any
Linux bridge network, use daemon option `"allow-direct-routing": true`
in `/etc/docker/daemon.json` or the equivalent `--allow-direct-routing`.

To allow direct routing from anywhere to containers in a specific bridge
network, see [Gateway modes](#gateway-modes).

Or, to allow direct routing via specific host interfaces, to a specific
bridge network, use the following option when creating the network:

- `com.docker.network.bridge.trusted_host_interfaces`

#### Example

Create a network where published ports on container IP addresses can be
accessed directly from interfaces `vxlan.1` and `eth3`:

```console
$ docker network create --subnet 192.0.2.0/24 --ip-range 192.0.2.0/29 -o com.docker.network.bridge.trusted_host_interfaces="vxlan.1:eth3" mynet
```

Run a container in that network, publishing its port 80 to port 8080 on
the host's loopback interface:

```console
$ docker run -d --ip 192.0.2.100 -p 127.0.0.1:8080:80 nginx
```

The web server running on the container's port 80 can now be accessed
from the Docker host at `http://127.0.0.1:8080`, or directly at
`http://192.0.2.100:80`. If remote hosts on networks connected to
interfaces `vxlan.1` and `eth3` have a route to the `192.0.2.0/24`
network inside the Docker host, they can also access the web server
via `http://192.0.2.100:80`.

## Gateway modes

The bridge network driver has the following options:

- `com.docker.network.bridge.gateway_mode_ipv6`
- `com.docker.network.bridge.gateway_mode_ipv4`

Each of these can be set to one of the gateway modes:

- `nat`
- `nat-unprotected`
- `routed`
- `isolated`

The default is `nat`, NAT and masquerading rules are set up for each
published container port. Packets leaving the host will use a host address.

With mode `routed`, no NAT or masquerading rules are set up, but firewall
rules are still set up so that only published container ports are accessible.
Outgoing packets from the container will use the container's address,
not a host address.

To access a published port in a `routed` network, remote hosts must have
a route to the container network via an external address on the Docker
host ("direct routing"). Hosts on the local layer-2 network can set up
direct routing without needing any additional network configuration.
Hosts outside the local network can only use direct routing to the
container if the network's routers are configured to enable it.

In a `nat` mode network, publishing a port to an address on the loopback
interface means remote hosts cannot access it. Other published container
ports in `routed` and `nat` networks are always accessible from remote
hosts using direct routing, unless the Docker host's firewall has additional
restrictions.

> Note
>
> When a port is published to a specific host address in `nat` mode, if
> IP forwarding is enabled on the Docker host, the published port can be
> accessed via other host interfaces using direct routing to the host
> address.
>
>
>
> For example, a Docker host with IP forwarding enabled has two NICs with
> addresses `192.168.100.10/24` and `10.0.0.10/24`.
> When a port is published to `192.168.100.10`, a host in the `10.0.0.0/24`
> subnet can access that port by routing to `192.168.100.10` via `10.0.0.10`.

In `nat-unprotected` mode, unpublished container ports are also
accessible using direct routing, no port filtering rules are set up.
This mode is included for compatibility with legacy default behaviour.

The gateway mode also affects communication between containers that
are connected to different Docker networks on the same host.

- In `nat` and `nat-unprotected` modes, containers in other bridge
  networks can only access published ports via the host addresses they
  are published to. Direct routing from other networks is not allowed.
- In `routed` mode containers in other networks can use direct
  routing to access ports, without going via a host address.

In `routed` mode, a host port in a `-p` or `--publish` port mapping is
not used, and the host address is only used to decide whether to apply
the mapping to IPv4 or IPv6. So, when a mapping only applies to `routed`
mode, only addresses `0.0.0.0` or `::` should be used, and a host port
should not be given. If a specific address or port is given, it will
have no effect on the published port and a warning message will be
logged.

Mode `isolated` can only be used when the network is also created with
CLI flag `--internal`, or equivalent. An address is normally assigned to the
bridge device in an `internal` network. So, processes on the Docker host can
access the network, and containers in the network can access host services
listening on that bridge address (including services listening on "any" host
address, `0.0.0.0` or `::`). No address is assigned to the bridge when the
network is created with gateway mode `isolated`.

### Example

Create a network suitable for direct routing for IPv6, with NAT enabled
for IPv4:

```console
$ docker network create --ipv6 --subnet 2001:db8::/64 -o com.docker.network.bridge.gateway_mode_ipv6=routed mynet
```

Create a container with a published port:

```console
$ docker run --network=mynet -p 8080:80 myimage
```

Then:

- Only container port 80 will be open, for IPv4 and IPv6.
- For IPv6, using `routed` mode, port 80 will be open on the container's IP
  address. Port 8080 will not be opened on the host's IP addresses, and
  outgoing packets will use the container's IP address.
- For IPv4, using the default `nat` mode, the container's port 80 will be
  accessible via port 8080 on the host's IP addresses, as well as directly
  from within the Docker host. But, container port 80 cannot be accessed
  directly from outside the host.
  Connections originating from the container will masquerade, using the
  host's IP address.

In `docker inspect`, this port mapping will be shown as follows. Note that
there is no `HostPort` for IPv6, because it is using `routed` mode:

```console
$ docker container inspect <id> --format "{{json .NetworkSettings.Ports}}"
{"80/tcp":[{"HostIp":"0.0.0.0","HostPort":"8080"},{"HostIp":"::","HostPort":""}]}
```

Alternatively, to make the mapping IPv6-only, disabling IPv4 access to the
container's port 80, use the unspecified IPv6 address `[::]` and do not
include a host port number:

```console
$ docker run --network mynet -p '[::]::80'
```

## Setting the default bind address for containers

By default, when a container's ports are mapped without any specific host
address, the Docker daemon publishes ports to all host addresses
(`0.0.0.0` and `[::]`).

For example, the following command publishes port 8080 to all network
interfaces on the host, on both IPv4 and IPv6 addresses, potentially
making them available to the outside world.

```console
docker run -p 8080:80 nginx
```

You can change the default binding address for published container ports so that
they're only accessible to the Docker host by default. To do that, you can
configure the daemon to use the loopback address (`127.0.0.1`) instead.

> Warning
>
> In releases older than 28.0.0, hosts within the same L2 segment (for example,
> hosts connected to the same network switch) can reach ports published to
> localhost. For more information, see
> [moby/moby#45610](https://github.com/moby/moby/issues/45610)

To configure this setting for user-defined bridge networks, use
the `com.docker.network.bridge.host_binding_ipv4` [driver option](https://docs.docker.com/engine/network/drivers/bridge/#default-host-binding-address) when you
create the network. Despite the option name, it is possible to specify an
IPv6 address.

```console
$ docker network create mybridge \
  -o "com.docker.network.bridge.host_binding_ipv4=127.0.0.1"
```

Or, to set the default binding address for containers in all user-defined
bridge networks, use daemon configuration option `default-network-opts`.
For example:

```json
{
  "default-network-opts": {
    "bridge": {
      "com.docker.network.bridge.host_binding_ipv4": "127.0.0.1"
    }
  }
}
```

> Note
>
> Setting the default binding address to `::` means port bindings with no host
> address specified will work for any IPv6 address on the host. But, `0.0.0.0`
> means any IPv4 or IPv6 address.
>
>
>
> Changing the default bind address doesn't have any effect on Swarm services.
> Swarm services are always exposed on the `0.0.0.0` network interface.

### Masquerade or SNAT for outgoing packets

NAT is enabled by default for bridge networks, meaning outgoing packets
from containers are masqueraded. The source address of packets leaving
the Docker host is changed to an address on the host interface the packet
is sent on.

Masquerading can be disabled for a user-defined bridge network by using
the `com.docker.network.bridge.enable_ip_masquerade` driver option when
creating the network. For example:

```console
$ docker network create mybridge \
  -o com.docker.network.bridge.enable_ip_masquerade=false ...
```

To use a specific source address for outgoing packets for a user-defined
network, instead of letting masquerading select an address, use options
`com.docker.network.host_ipv4` and `com.docker.network.host_ipv6` to
specify the Source NAT (SNAT) address to use. The
`com.docker.network.bridge.enable_ip_masquerade` option must
be `true`, the default, for these options to have any effect.

### Default bridge

To set the default binding for the default bridge network, configure the `"ip"`
key in the `daemon.json` configuration file:

```json
{
  "ip": "127.0.0.1"
}
```

This changes the default binding address to `127.0.0.1` for published container
ports on the default bridge network.
Restart the daemon for this change to take effect.
Alternatively, you can use the `dockerd --ip` flag when starting the daemon.
