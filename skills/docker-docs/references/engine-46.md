# Getting started with Swarm mode and more

# Getting started with Swarm mode

> Getting Started tutorial for Docker Engine Swarm mode

# Getting started with Swarm mode

   Table of contents

---

This tutorial introduces you to the features of Docker Engine Swarm mode. You
may want to familiarize yourself with the [key concepts](https://docs.docker.com/engine/swarm/key-concepts/)
before you begin.

The tutorial guides you through:

- Initializing a cluster of Docker Engines in swarm mode
- Adding nodes to the swarm
- Deploying application services to the swarm
- Managing the swarm once you have everything running

This tutorial uses Docker Engine CLI commands entered on the command line of a
terminal window.

If you are brand new to Docker, see [About Docker Engine](https://docs.docker.com/engine/).

## Set up

To run this tutorial, you need:

- [Three Linux hosts which can communicate over a network, with Docker installed](#three-networked-host-machines)
- [The IP address of the manager machine](#the-ip-address-of-the-manager-machine)
- [Open ports between the hosts](#open-protocols-and-ports-between-the-hosts)

### Three networked host machines

This tutorial requires three Linux hosts which have Docker installed and can
communicate over a network. These can be physical machines, virtual machines,
Amazon EC2 instances, or hosted in some other way. Check out
[Deploy to Swarm](https://docs.docker.com/guides/swarm-deploy/#prerequisites) for one possible set-up for the hosts.

One of these machines is a manager (called `manager1`) and two of them are
workers (`worker1` and `worker2`).

> Note
>
> You can follow many of the tutorial steps to test single-node swarm as well, in which case you need only one host. Multi-node commands do not work, but you can initialize a swarm, create services, and scale them.

#### Install Docker Engine on Linux machines

If you are using Linux based physical computers or cloud-provided computers as
hosts, simply follow the [Linux install instructions](https://docs.docker.com/engine/install/)
for your platform. Spin up the three machines, and you are ready. You can test both
single-node and multi-node swarm scenarios on Linux machines.

### The IP address of the manager machine

The IP address must be assigned to a network interface available to the host
operating system. All nodes in the swarm need to connect to the manager at
the IP address.

Because other nodes contact the manager node on its IP address, you should use a
fixed IP address.

You can run `ifconfig` on Linux or macOS to see a list of the
available network interfaces.

The tutorial uses `manager1` : `192.168.99.100`.

### Open protocols and ports between the hosts

The following ports must be available. On some systems, these ports are open by default.

- Port `2377` TCP for communication with and between manager nodes
- Port `7946` TCP/UDP for overlay network node discovery
- Port `4789` UDP (configurable) for overlay network traffic

If you plan on creating an overlay network with encryption (`--opt encrypted`),
you also need to ensure IP protocol 50 (IPSec ESP) traffic is allowed.

Port `4789` is the default value for the Swarm data path port, also known as the VXLAN port.
It is important to prevent any untrusted traffic from reaching this port, as VXLAN does not
provide authentication. This port should only be opened to a trusted network, and never at a
perimeter firewall.

If the network which Swarm traffic traverses is not fully trusted, it is strongly suggested that
encrypted overlay networks be used. If encrypted overlay networks are in exclusive use, some
additional hardening is suggested:

- [Customize the default ingress network](https://docs.docker.com/engine/swarm/networking/) to use encryption
- Only accept encrypted packets on the Data Path Port:

```bash
# Example iptables rule (order and other tools may require customization)
iptables -I INPUT -m udp --dport 4789 -m policy --dir in --pol none -j DROP
```

## Next steps

Next, you'll create a swarm.

[Create a swarm](https://docs.docker.com/engine/swarm/swarm-tutorial/create-swarm/)

---

# Lock your swarm to protect its encryption key

> Automatically lock Swarm managers to protect encryption keys

# Lock your swarm to protect its encryption key

   Table of contents

---

The Raft logs used by swarm managers are encrypted on disk by default. This at-rest
encryption protects your service's configuration and data from attackers who gain
access to the encrypted Raft logs. One of the reasons this feature was introduced
was in support of the [Docker secrets](https://docs.docker.com/engine/swarm/secrets/) feature.

When Docker restarts, both the TLS key used to encrypt communication among swarm
nodes and the key used to encrypt and decrypt Raft logs on disk are loaded
into each manager node's memory. Docker has the ability to protect the mutual TLS
encryption key and the key used to encrypt and decrypt Raft logs at rest, by
allowing you to take ownership of these keys and to require manual unlocking of
your managers. This feature is called autolock.

When Docker restarts, you must
[unlock the swarm](#unlock-a-swarm) first, using a
key encryption key generated by Docker when the swarm was locked. You can
rotate this key encryption key at any time.

> Note
>
> You don't need to unlock the swarm when a new node joins the swarm,
> because the key is propagated to it over mutual TLS.

## Initialize a swarm with autolocking enabled

When you initialize a new swarm, you can use the `--autolock` flag to
enable autolocking of swarm manager nodes when Docker restarts.

```console
$ docker swarm init --autolock

Swarm initialized: current node (k1q27tfyx9rncpixhk69sa61v) is now a manager.

To add a worker to this swarm, run the following command:

    docker swarm join \
    --token SWMTKN-1-0j52ln6hxjpxk2wgk917abcnxywj3xed0y8vi1e5m9t3uttrtu-7bnxvvlz2mrcpfonjuztmtts9 \
    172.31.46.109:2377

To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.

To unlock a swarm manager after it restarts, run the `docker swarm unlock`
command and provide the following key:

    SWMKEY-1-WuYH/IX284+lRcXuoVf38viIDK3HJEKY13MIHX+tTt8
```

Store the key in a safe place, such as in a password manager.

When Docker restarts, you need to [unlock the swarm](#unlock-a-swarm). A locked
swarm causes an error like the following when you try to start or restart a
service:

```console
$ sudo service docker restart

$ docker service ls

Error response from daemon: Swarm is encrypted and needs to be unlocked before it can be used. Use "docker swarm unlock" to unlock it.
```

## Enable or disable autolock on an existing swarm

To enable autolock on an existing swarm, set the `autolock` flag to `true`.

```console
$ docker swarm update --autolock=true

Swarm updated.
To unlock a swarm manager after it restarts, run the `docker swarm unlock`
command and provide the following key:

    SWMKEY-1-+MrE8NgAyKj5r3NcR4FiQMdgu+7W72urH0EZeSmP/0Y

Please remember to store this key in a password manager, since without it you
will not be able to restart the manager.
```

To disable autolock, set `--autolock` to `false`. The mutual TLS key and the
encryption key used to read and write Raft logs are stored unencrypted on
disk. There is a trade-off between the risk of storing the encryption key
unencrypted at rest and the convenience of restarting a swarm without
needing to unlock each manager.

```console
$ docker swarm update --autolock=false
```

Keep the unlock key around for a short time after disabling autolocking, in case
a manager goes down while it is still configured to lock using the old key.

## Unlock a swarm

To unlock a locked swarm, use `docker swarm unlock`.

```console
$ docker swarm unlock

Please enter unlock key:
```

Enter the encryption key that was generated and shown in the command output when
you locked the swarm or rotated the key, and the swarm unlocks.

## View the current unlock key for a running swarm

Consider a situation where your swarm is running as expected, then a manager
node becomes unavailable. You troubleshoot the problem and bring the physical
node back online, but you need to unlock the manager by providing the unlock
key to read the encrypted credentials and Raft logs.

If the key has not been rotated since the node left the swarm, and you have a
quorum of functional manager nodes in the swarm, you can view the current unlock
key using `docker swarm unlock-key` without any arguments.

```console
$ docker swarm unlock-key

To unlock a swarm manager after it restarts, run the `docker swarm unlock`
command and provide the following key:

    SWMKEY-1-8jDgbUNlJtUe5P/lcr9IXGVxqZpZUXPzd+qzcGp4ZYA

Please remember to store this key in a password manager, since without it you
will not be able to restart the manager.
```

If the key was rotated after the swarm node became unavailable and you do not
have a record of the previous key, you may need to force the manager to leave
the swarm and join it back to the swarm as a new manager.

## Rotate the unlock key

You should rotate the locked swarm's unlock key on a regular schedule.

```console
$ docker swarm unlock-key --rotate

Successfully rotated manager unlock key.

To unlock a swarm manager after it restarts, run the `docker swarm unlock`
command and provide the following key:

    SWMKEY-1-8jDgbUNlJtUe5P/lcr9IXGVxqZpZUXPzd+qzcGp4ZYA

Please remember to store this key in a password manager, since without it you
will not be able to restart the manager.
```

> Warning
>
> When you rotate the unlock key, keep a record of the old key
> around for a few minutes, so that if a manager goes down before it gets the new
> key, it may still be unlocked with the old one.

---

# Swarm mode

> Docker Engine Swarm mode overview

# Swarm mode

   Table of contents

---

> Note
>
> Swarm mode is an advanced feature for managing a cluster of Docker daemons.
>
>
>
> Use Swarm mode if you intend to use Swarm as a production runtime environment.
>
>
>
> If you're not planning on deploying with Swarm, use
> [Docker Compose](https://docs.docker.com/compose/) instead.
> If you're developing for a Kubernetes deployment, consider using the
> [integrated Kubernetes feature](https://docs.docker.com/desktop/use-desktop/kubernetes/) in Docker Desktop.

Current versions of Docker include Swarm mode for natively managing a cluster
of Docker Engines called a swarm. Use the Docker CLI to create a swarm, deploy
application services to a swarm, and manage swarm behavior.

Docker Swarm mode is built into the Docker Engine. Do not confuse Docker Swarm mode
with [Docker Classic Swarm](https://github.com/docker/classicswarm)
which is no longer actively developed.

## Feature highlights

### Cluster management integrated with Docker Engine

Use the Docker Engine CLI to create a swarm of Docker Engines where you can deploy application
services. You don't need additional orchestration software to create or manage
a swarm.

### Decentralized design

Instead of handling differentiation between node roles at deployment time, the Docker Engine handles any specialization at runtime. You can deploy both kinds of nodes, managers and workers, using the
Docker Engine. This means you can build an entire swarm from a single disk
image.

### Declarative service model

Docker Engine uses a declarative approach to
let you define the desired state of the various services in your application
stack. For example, you might describe an application comprised of a web front
end service with message queueing services and a database backend.

### Scaling

For each service, you can declare the number of tasks you want to
run. When you scale up or down, the swarm manager automatically adapts by
adding or removing tasks to maintain the desired state.

### Desired state reconciliation

The swarm manager node constantly monitors
the cluster state and reconciles any differences between the actual state and your
expressed desired state. For example, if you set up a service to run 10
replicas of a container, and a worker machine hosting two of those replicas
crashes, the manager creates two new replicas to replace the replicas that
crashed. The swarm manager assigns the new replicas to workers that are
running and available.

### Multi-host networking

You can specify an overlay network for your
services. The swarm manager automatically assigns addresses to the containers
on the overlay network when it initializes or updates the application.

### Service discovery

Swarm manager nodes assign each service in the swarm a
unique DNS name and load balance running containers. You can query every
container running in the swarm through a DNS server embedded in the swarm.

### Load balancing

You can expose the ports for services to an
external load balancer. Internally, the swarm lets you specify how to distribute
service containers between nodes.

### Secure by default

Each node in the swarm enforces TLS mutual
authentication and encryption to secure communications between itself and all
other nodes. You have the option to use self-signed root certificates or
certificates from a custom root CA.

### Rolling updates

At rollout time you can apply service updates to nodes
incrementally. The swarm manager lets you control the delay between service
deployment to different sets of nodes. If anything goes wrong, you can
roll back to a previous version of the service.

## What's next?

- Learn Swarm mode [key concepts](https://docs.docker.com/engine/swarm/key-concepts/).
- Get started with the [Swarm mode tutorial](https://docs.docker.com/engine/swarm/swarm-tutorial/).
- Explore Swarm mode CLI commands
  - [swarm init](https://docs.docker.com/reference/cli/docker/swarm/init/)
  - [swarm join](https://docs.docker.com/reference/cli/docker/swarm/join/)
  - [service create](https://docs.docker.com/reference/cli/docker/service/create/)
  - [service inspect](https://docs.docker.com/reference/cli/docker/service/inspect/)
  - [service ls](https://docs.docker.com/reference/cli/docker/service/ls/)
  - [service rm](https://docs.docker.com/reference/cli/docker/service/rm/)
  - [service scale](https://docs.docker.com/reference/cli/docker/service/scale/)
  - [service ps](https://docs.docker.com/reference/cli/docker/service/ps/)
  - [service update](https://docs.docker.com/reference/cli/docker/service/update/)
