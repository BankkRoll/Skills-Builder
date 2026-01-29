# How nodes work and more

# How nodes work

> How swarm nodes work

# How nodes work

   Table of contents

---

Swarm mode lets you create a
cluster of one or more Docker Engines called a swarm. A swarm consists
of one or more nodes: physical or virtual machines running Docker
Engine.

There are two types of nodes: [managers](#manager-nodes) and
[workers](#worker-nodes).

![Swarm mode cluster](https://docs.docker.com/engine/swarm/images/swarm-diagram.webp)  ![Swarm mode cluster](https://docs.docker.com/engine/swarm/images/swarm-diagram.webp)

If you haven't already, read through the
[Swarm mode overview](https://docs.docker.com/engine/swarm/) and
[key concepts](https://docs.docker.com/engine/swarm/key-concepts/).

## Manager nodes

Manager nodes handle cluster management tasks:

- Maintaining cluster state
- Scheduling services
- Serving Swarm mode
  [HTTP API endpoints](https://docs.docker.com/reference/api/engine/)

Using a [Raft](https://raft.github.io/raft.pdf) implementation, the managers
maintain a consistent internal state of the entire swarm and all the services
running on it. For testing purposes it is OK to run a swarm with a single
manager. If the manager in a single-manager swarm fails, your services
continue to run, but you need to create a new cluster to recover.

To take advantage of Swarm mode's fault-tolerance features, we recommend
you implement an odd number of nodes according to your organization's
high-availability requirements. When you have multiple managers you can recover
from the failure of a manager node without downtime.

- A three-manager swarm tolerates a maximum loss of one manager.
- A five-manager swarm tolerates a maximum simultaneous loss of two
  manager nodes.
- An odd number `N` of manager nodes in the cluster tolerates the loss of at most `(N-1)/2` managers.
  Docker recommends a maximum of seven manager nodes for a swarm.
  > Important
  >
  > Adding more managers does NOT mean increased scalability or higher performance. In general, the opposite is true.

## Worker nodes

Worker nodes are also instances of Docker Engine whose sole purpose is to
execute containers. Worker nodes don't participate in the Raft distributed
state, make scheduling decisions, or serve the swarm mode HTTP API.

You can create a swarm of one manager node, but you cannot have a worker node
without at least one manager node. By default, all managers are also workers.
In a single manager node cluster, you can run commands like `docker service create` and the scheduler places all tasks on the local engine.

To prevent the scheduler from placing tasks on a manager node in a multi-node
swarm, set the availability for the manager node to `Drain`. The scheduler
gracefully stops tasks on nodes in `Drain` mode and schedules the tasks on an
`Active` node. The scheduler does not assign new tasks to nodes with `Drain`
availability.

Refer to the
[docker node update](https://docs.docker.com/reference/cli/docker/node/update/)
command line reference to see how to change node availability.

## Change roles

You can promote a worker node to be a manager by running `docker node promote`.
For example, you may want to promote a worker node when you
take a manager node offline for maintenance. See
[node promote](https://docs.docker.com/reference/cli/docker/node/promote/).

You can also demote a manager node to a worker node. See
[node demote](https://docs.docker.com/reference/cli/docker/node/demote/).

## Learn more

- Read about how Swarm mode [services](https://docs.docker.com/engine/swarm/how-swarm-mode-works/services/) work.
- Learn how [PKI](https://docs.docker.com/engine/swarm/how-swarm-mode-works/pki/) works in Swarm mode.

---

# Manage swarm security with public key infrastructure (PKI)

> How PKI works in swarm mode

# Manage swarm security with public key infrastructure (PKI)

   Table of contents

---

The Swarm mode public key infrastructure (PKI) system built into Docker
makes it simple to securely deploy a container orchestration system. The nodes
in a swarm use mutual Transport Layer Security (TLS) to authenticate, authorize,
and encrypt the communications with other nodes in the swarm.

When you create a swarm by running `docker swarm init`, Docker designates itself
as a manager node. By default, the manager node generates a new root Certificate
Authority (CA) along with a key pair, which are used to secure communications
with other nodes that join the swarm. If you prefer, you can specify your own
externally-generated root CA, using the `--external-ca` flag of the
[docker swarm init](https://docs.docker.com/reference/cli/docker/swarm/init/) command.

The manager node also generates two tokens to use when you join additional nodes
to the swarm: one worker token and one manager token. Each token
includes the digest of the root CA's certificate and a randomly generated
secret. When a node joins the swarm, the joining node uses the digest to
validate the root CA certificate from the remote manager. The remote manager
uses the secret to ensure the joining node is an approved node.

Each time a new node joins the swarm, the manager issues a certificate to the
node. The certificate contains a randomly generated node ID to identify the node
under the certificate common name (CN) and the role under the organizational
unit (OU). The node ID serves as the cryptographically secure node identity for
the lifetime of the node in the current swarm.

The diagram below illustrates how manager nodes and worker nodes encrypt
communications using a minimum of TLS 1.2.

![TLS diagram](https://docs.docker.com/engine/swarm/images/tls.webp?w=600)  ![TLS diagram](https://docs.docker.com/engine/swarm/images/tls.webp?w=600)

The example below shows the information from a certificate from a worker node:

```text
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number:
            3b:1c:06:91:73:fb:16:ff:69:c3:f7:a2:fe:96:c1:73:e2:80:97:3b
        Signature Algorithm: ecdsa-with-SHA256
        Issuer: CN=swarm-ca
        Validity
            Not Before: Aug 30 02:39:00 2016 GMT
            Not After : Nov 28 03:39:00 2016 GMT
        Subject: O=ec2adilxf4ngv7ev8fwsi61i7, OU=swarm-worker, CN=dw02poa4vqvzxi5c10gm4pq2g
...snip...
```

By default, each node in the swarm renews its certificate every three months.
You can configure this interval by running the `docker swarm update --cert-expiry <TIME PERIOD>` command. The minimum rotation value is 1 hour.
Refer to the
[docker swarm update](https://docs.docker.com/reference/cli/docker/swarm/update/) CLI
reference for details.

## Rotating the CA certificate

> Note
>
> Mirantis Kubernetes Engine (MKE), formerly known as Docker UCP, provides an external
> certificate manager service for the swarm. If you run swarm on MKE, you shouldn't
> rotate the CA certificates manually. Instead, contact Mirantis support if you need
> to rotate a certificate.

In the event that a cluster CA key or a manager node is compromised, you can
rotate the swarm root CA so that none of the nodes trust certificates
signed by the old root CA anymore.

Run `docker swarm ca --rotate` to generate a new CA certificate and key. If you
prefer, you can pass the `--ca-cert` and `--external-ca` flags to specify the
root certificate and to use a root CA external to the swarm. Alternately,
you can pass the `--ca-cert` and `--ca-key` flags to specify the exact
certificate and key you would like the swarm to use.

When you issue the `docker swarm ca --rotate` command, the following things
happen in sequence:

1. Docker generates a cross-signed certificate. This means that a version of
  the new root CA certificate is signed with the old root CA certificate.
  This cross-signed certificate is used as an intermediate certificate for all
  new node certificates. This ensures that nodes that still trust the old root
  CA can still validate a certificate signed by the new CA.
2. Docker also tells all nodes to immediately renew their TLS certificates.
  This process may take several minutes, depending on the number of nodes in
  the swarm.
3. After every node in the swarm has a new TLS certificate signed by the new CA,
  Docker forgets about the old CA certificate and key material, and tells
  all the nodes to trust the new CA certificate only.
  This also causes a change in the swarm's join tokens. The previous
  join tokens are no longer valid.

From this point on, all new node certificates issued are signed with the new
root CA, and do not contain any intermediates.

## Learn More

- Read about how [nodes](https://docs.docker.com/engine/swarm/how-swarm-mode-works/nodes/) work.
- Learn how Swarm mode [services](https://docs.docker.com/engine/swarm/how-swarm-mode-works/services/) work.

---

# How services work

> How swarm mode services work

# How services work

   Table of contents

---

To deploy an application image when Docker Engine is in Swarm mode, you create a
service. Frequently a service is the image for a microservice within the
context of some larger application. Examples of services might include an HTTP
server, a database, or any other type of executable program that you wish to run
in a distributed environment.

When you create a service, you specify which container image to use and which
commands to execute inside running containers. You also define options for the
service including:

- The port where the swarm makes the service available outside the swarm
- An overlay network for the service to connect to other services in the swarm
- CPU and memory limits and reservations
- A rolling update policy
- The number of replicas of the image to run in the swarm

## Services, tasks, and containers

When you deploy the service to the swarm, the swarm manager accepts your service
definition as the desired state for the service. Then it schedules the service
on nodes in the swarm as one or more replica tasks. The tasks run independently
of each other on nodes in the swarm.

For example, imagine you want to load balance between three instances of an HTTP
listener. The diagram below shows an HTTP listener service with three replicas.
Each of the three instances of the listener is a task in the swarm.

![ HTTP listener service with three replicas](https://docs.docker.com/engine/swarm/images/services-diagram.webp)  ![ HTTP listener service with three replicas](https://docs.docker.com/engine/swarm/images/services-diagram.webp)

A container is an isolated process. In the Swarm mode model, each task invokes
exactly one container. A task is analogous to a “slot” where the scheduler
places a container. Once the container is live, the scheduler recognizes that
the task is in a running state. If the container fails health checks or
terminates, the task terminates.

## Tasks and scheduling

A task is the atomic unit of scheduling within a swarm. When you declare a
desired service state by creating or updating a service, the orchestrator
realizes the desired state by scheduling tasks. For instance, you define a
service that instructs the orchestrator to keep three instances of an HTTP
listener running at all times. The orchestrator responds by creating three
tasks. Each task is a slot that the scheduler fills by spawning a container. The
container is the instantiation of the task. If an HTTP listener task subsequently
fails its health check or crashes, the orchestrator creates a new replica task
that spawns a new container.

A task is a one-directional mechanism. It progresses monotonically through a
series of states: assigned, prepared, running, etc. If the task fails, the
orchestrator removes the task and its container and then creates a new task to
replace it according to the desired state specified by the service.

The underlying logic of Docker's Swarm mode is a general purpose scheduler and
orchestrator. The service and task abstractions themselves are unaware of the
containers they implement. Hypothetically, you could implement other types of
tasks such as virtual machine tasks or non-containerized process tasks. The
scheduler and orchestrator are agnostic about the type of the task. However, the
current version of Docker only supports container tasks.

The diagram below shows how Swarm mode accepts service create requests and
schedules tasks to worker nodes.

![Services flow](https://docs.docker.com/engine/swarm/images/service-lifecycle.webp)  ![Services flow](https://docs.docker.com/engine/swarm/images/service-lifecycle.webp)

### Pending services

A service may be configured in such a way that no node currently in the
swarm can run its tasks. In this case, the service remains in state `pending`.
Here are a few examples of when a service might remain in state `pending`.

> Tip
>
> If your only intention is to prevent a service from
> being deployed, scale the service to 0 instead of trying to configure it in
> such a way that it remains in `pending`.

- If all nodes are paused or drained, and you create a service, it is
  pending until a node becomes available. In reality, the first node to become
  available gets all of the tasks, so this is not a good thing to do in a
  production environment.
- You can reserve a specific amount of memory for a service. If no node in the
  swarm has the required amount of memory, the service remains in a pending
  state until a node is available which can run its tasks. If you specify a very
  large value, such as 500 GB, the task stays pending forever, unless you
  really have a node which can satisfy it.
- You can impose placement constraints on the service, and the constraints may
  not be able to be honored at a given time.

This behavior illustrates that the requirements and configuration of your tasks
are not tightly tied to the current state of the swarm. As the administrator of
a swarm, you declare the desired state of your swarm, and the manager works with
the nodes in the swarm to create that state. You do not need to micro-manage the
tasks on the swarm.

## Replicated and global services

There are two types of service deployments, replicated and global.

For a replicated service, you specify the number of identical tasks you want to
run. For example, you decide to deploy an HTTP service with three replicas, each
serving the same content.

A global service is a service that runs one task on every node. There is no
pre-specified number of tasks. Each time you add a node to the swarm, the
orchestrator creates a task and the scheduler assigns the task to the new node.
Good candidates for global services are monitoring agents, anti-virus scanners
or other types of containers that you want to run on every node in the swarm.

The diagram below shows a three-service replica in gray and a global service
in black.

![Global vs replicated services](https://docs.docker.com/engine/swarm/images/replicated-vs-global.webp)  ![Global vs replicated services](https://docs.docker.com/engine/swarm/images/replicated-vs-global.webp)

## Learn more

- Read about how Swarm mode [nodes](https://docs.docker.com/engine/swarm/how-swarm-mode-works/nodes/) work.
- Learn how [PKI](https://docs.docker.com/engine/swarm/how-swarm-mode-works/pki/) works in Swarm mode.

---

# Swarm task states

> Learn about tasks that are scheduled on your swarm.

# Swarm task states

   Table of contents

---

Docker lets you create services, which can start tasks. A service is a
description of a desired state, and a task does the work. Work is scheduled on
swarm nodes in this sequence:

1. Create a service by using `docker service create`.
2. The request goes to a Docker manager node.
3. The Docker manager node schedules the service to run on particular nodes.
4. Each service can start multiple tasks.
5. Each task has a life cycle, with states like `NEW`, `PENDING`, and `COMPLETE`.

Tasks are execution units that run once to completion. When a task stops, it
isn't executed again, but a new task may take its place.

Tasks advance through a number of states until they complete or fail. Tasks are
initialized in the `NEW` state. The task progresses forward through a number of
states, and its state doesn't go backward. For example, a task never goes from
`COMPLETE` to `RUNNING`.

Tasks go through the states in the following order:

| Task state | Description |
| --- | --- |
| NEW | The task was initialized. |
| PENDING | Resources for the task were allocated. |
| ASSIGNED | Docker assigned the task to nodes. |
| ACCEPTED | The task was accepted by a worker node. If a worker node rejects the task, the state changes toREJECTED. |
| READY | The worker node is ready to start the task |
| PREPARING | Docker is preparing the task. |
| STARTING | Docker is starting the task. |
| RUNNING | The task is executing. |
| COMPLETE | The task exited without an error code. |
| FAILED | The task exited with an error code. |
| SHUTDOWN | Docker requested the task to shut down. |
| REJECTED | The worker node rejected the task. |
| ORPHANED | The node was down for too long. |
| REMOVE | The task is not terminal but the associated service was removed or scaled down. |

## View task state

Run `docker service ps <service-name>` to get the state of a task. The
`CURRENT STATE` field shows the task's state and how long it's been
there.

```console
$ docker service ps webserver
ID             NAME              IMAGE    NODE        DESIRED STATE  CURRENT STATE            ERROR                              PORTS
owsz0yp6z375   webserver.1       nginx    UbuntuVM    Running        Running 44 seconds ago
j91iahr8s74p    \_ webserver.1   nginx    UbuntuVM    Shutdown       Failed 50 seconds ago    "No such container: webserver.…"
7dyaszg13mw2    \_ webserver.1   nginx    UbuntuVM    Shutdown       Failed 5 hours ago       "No such container: webserver.…"
```

## Where to go next

- [Learn about swarm tasks](https://github.com/docker/swarmkit/blob/master/design/task_model.md)

---

# Use Swarm mode routing mesh

> Use the routing mesh to publish services externally to a swarm

# Use Swarm mode routing mesh

   Table of contents

---

Docker Engine Swarm mode makes it easy to publish ports for services to make
them available to resources outside the swarm. All nodes participate in an
ingress routing mesh. The routing mesh enables each node in the swarm to
accept connections on published ports for any service running in the swarm, even
if there's no task running on the node. The routing mesh routes all
incoming requests to published ports on available nodes to an active container.

To use the ingress network in the swarm, you need to have the following
ports open between the swarm nodes before you enable Swarm mode:

- Port `7946` TCP/UDP for container network discovery.
- Port `4789` UDP (configurable) for the container ingress network.

When setting up networking in a Swarm, special care should be taken. Consult
the [tutorial](https://docs.docker.com/engine/swarm/swarm-tutorial/#open-protocols-and-ports-between-the-hosts)
for an overview.

You must also open the published port between the swarm nodes and any external
resources, such as an external load balancer, that require access to the port.

You can also [bypass the routing mesh](#bypass-the-routing-mesh) for a given
service.

## Publish a port for a service

Use the `--publish` flag to publish a port when you create a service. `target`
is used to specify the port inside the container, and `published` is used to
specify the port to bind on the routing mesh. If you leave off the `published`
port, a random high-numbered port is bound for each service task. You
need to inspect the task to determine the port.

```console
$ docker service create \
  --name <SERVICE-NAME> \
  --publish published=<PUBLISHED-PORT>,target=<CONTAINER-PORT> \
  IMAGE
```

> Note
>
> The older form of this syntax is a colon-separated string, where
> the published port is first and the target port is second, such as
> `-p 8080:80`. The new syntax is preferred because it is easier to read and
> allows more flexibility.

The `<PUBLISHED-PORT>` is the port where the swarm makes the service available.
If you omit it, a random high-numbered port is bound.
The `<CONTAINER-PORT>` is the port where the container listens. This parameter
is required.

For example, the following command publishes port 80 in the nginx container to
port 8080 for any node in the swarm:

```console
$ docker service create \
  --name my-web \
  --publish published=8080,target=80 \
  --replicas 2 \
  nginx
```

When you access port 8080 on any node, Docker routes your request to an active
container. On the swarm nodes themselves, port 8080 may not actually be bound,
but the routing mesh knows how to route the traffic and prevents any port
conflicts from happening.

The routing mesh listens on the published port for any IP address assigned to
the node. For externally routable IP addresses, the port is available from
outside the host. For all other IP addresses the access is only available from
within the host.

![Service ingress image](https://docs.docker.com/engine/swarm/images/ingress-routing-mesh.webp)  ![Service ingress image](https://docs.docker.com/engine/swarm/images/ingress-routing-mesh.webp)

You can publish a port for an existing service using the following command:

```console
$ docker service update \
  --publish-add published=<PUBLISHED-PORT>,target=<CONTAINER-PORT> \
  SERVICE
```

You can use `docker service inspect` to view the service's published port. For
instance:

```console
$ docker service inspect --format="{{json .Endpoint.Spec.Ports}}" my-web

[{"Protocol":"tcp","TargetPort":80,"PublishedPort":8080}]
```

The output shows the `<CONTAINER-PORT>` (labeled `TargetPort`) from the containers and the
`<PUBLISHED-PORT>` (labeled `PublishedPort`) where nodes listen for requests for the service.

### Publish a port for TCP only or UDP only

By default, when you publish a port, it is a TCP port. You can
specifically publish a UDP port instead of or in addition to a TCP port. When
you publish both TCP and UDP ports, if you omit the protocol specifier,
the port is published as a TCP port. If you use the longer syntax (recommended),
set the `protocol` key to either `tcp` or `udp`.

#### TCP only

Long syntax:

```console
$ docker service create --name dns-cache \
  --publish published=53,target=53 \
  dns-cache
```

Short syntax:

```console
$ docker service create --name dns-cache \
  -p 53:53 \
  dns-cache
```

#### TCP and UDP

Long syntax:

```console
$ docker service create --name dns-cache \
  --publish published=53,target=53 \
  --publish published=53,target=53,protocol=udp \
  dns-cache
```

Short syntax:

```console
$ docker service create --name dns-cache \
  -p 53:53 \
  -p 53:53/udp \
  dns-cache
```

#### UDP only

Long syntax:

```console
$ docker service create --name dns-cache \
  --publish published=53,target=53,protocol=udp \
  dns-cache
```

Short syntax:

```console
$ docker service create --name dns-cache \
  -p 53:53/udp \
  dns-cache
```

## Bypass the routing mesh

By default, swarm services which publish ports do so using the routing mesh.
When you connect to a published port on any swarm node (whether it is running a
given service or not), you are redirected to a worker which is running that
service, transparently. Effectively, Docker acts as a load balancer for your
swarm services.

You can bypass the routing mesh, so that when you access the bound port on a
given node, you are always accessing the instance of the service running on
that node. This is referred to as `host` mode. There are a few things to keep
in mind.

- If you access a node which is not running a service task, the service does not
  listen on that port. It is possible that nothing is listening, or
  that a completely different application is listening.
- If you expect to run multiple service tasks on each node (such as when you
  have 5 nodes but run 10 replicas), you cannot specify a static target port.
  Either allow Docker to assign a random high-numbered port (by leaving off the
  `published`), or ensure that only a single instance of the service runs on a
  given node, by using a global service rather than a replicated one, or by
  using placement constraints.

To bypass the routing mesh, you must use the long `--publish` service and
set `mode` to `host`. If you omit the `mode` key or set it to `ingress`, the
routing mesh is used. The following command creates a global service using
`host` mode and bypassing the routing mesh.

```console
$ docker service create --name dns-cache \
  --publish published=53,target=53,protocol=udp,mode=host \
  --mode global \
  dns-cache
```

## Configure an external load balancer

You can configure an external load balancer for swarm services, either in
combination with the routing mesh or without using the routing mesh at all.

### Using the routing mesh

You can configure an external load balancer to route requests to a swarm
service. For example, you could configure [HAProxy](https://www.haproxy.org) to
balance requests to an nginx service published to port 8080.

![Ingress with external load balancer image](https://docs.docker.com/engine/swarm/images/ingress-lb.webp)  ![Ingress with external load balancer image](https://docs.docker.com/engine/swarm/images/ingress-lb.webp)

In this case, port 8080 must be open between the load balancer and the nodes in
the swarm. The swarm nodes can reside on a private network that is accessible to
the proxy server, but that is not publicly accessible.

You can configure the load balancer to balance requests between every node in
the swarm even if there are no tasks scheduled on the node. For example, you
could have the following HAProxy configuration in `/etc/haproxy/haproxy.cfg`:

```bash
global
        log /dev/log    local0
        log /dev/log    local1 notice
...snip...

# Configure HAProxy to listen on port 80
frontend http_front
   bind *:80
   stats uri /haproxy?stats
   default_backend http_back

# Configure HAProxy to route requests to swarm nodes on port 8080
backend http_back
   balance roundrobin
   server node1 192.168.99.100:8080 check
   server node2 192.168.99.101:8080 check
   server node3 192.168.99.102:8080 check
```

When you access the HAProxy load balancer on port 80, it forwards requests to
nodes in the swarm. The swarm routing mesh routes the request to an active task.
If, for any reason the swarm scheduler dispatches tasks to different nodes, you
don't need to reconfigure the load balancer.

You can configure any type of load balancer to route requests to swarm nodes.
To learn more about HAProxy, see the [HAProxy documentation](https://cbonte.github.io/haproxy-dconv/).

### Without the routing mesh

To use an external load balancer without the routing mesh, set `--endpoint-mode`
to `dnsrr` instead of the default value of `vip`. In this case, there is not a
single virtual IP. Instead, Docker sets up DNS entries for the service such that
a DNS query for the service name returns a list of IP addresses, and the client
connects directly to one of these.

You can't use `--endpoint-mode dnsrr` together with `--publish mode=ingress`.
You must run your own load balancer in front of the service. A DNS query for
the service name on the Docker host returns a list of IP addresses for the
nodes running the service. Configure your load balancer to consume this list
and balance the traffic across the nodes.
See [Configure service discovery](https://docs.docker.com/engine/swarm/networking/#configure-service-discovery).

## Learn more

- [Deploy services to a swarm](https://docs.docker.com/engine/swarm/services/)

---

# Join nodes to a swarm

> Add worker and manager nodes to a swarm

# Join nodes to a swarm

   Table of contents

---

When you first create a swarm, you place a single Docker Engine into
Swarm mode. To take full advantage of Swarm mode you can add nodes to the swarm:

- Adding worker nodes increases capacity. When you deploy a service to a swarm,
  the engine schedules tasks on available nodes whether they are worker nodes or
  manager nodes. When you add workers to your swarm, you increase the scale of
  the swarm to handle tasks without affecting the manager raft consensus.
- Manager nodes increase fault-tolerance. Manager nodes perform the
  orchestration and cluster management functions for the swarm. Among manager
  nodes, a single leader node conducts orchestration tasks. If a leader node
  goes down, the remaining manager nodes elect a new leader and resume
  orchestration and maintenance of the swarm state. By default, manager nodes
  also run tasks.

Docker Engine joins the swarm depending on the **join-token** you provide to
the `docker swarm join` command. The node only uses the token at join time. If
you subsequently rotate the token, it doesn't affect existing swarm nodes. Refer
to [Run Docker Engine in swarm mode](https://docs.docker.com/engine/swarm/swarm-mode/#view-the-join-command-or-update-a-swarm-join-token).

## Join as a worker node

To retrieve the join command including the join token for worker nodes, run the
following command on a manager node:

```console
$ docker swarm join-token worker

To add a worker to this swarm, run the following command:

    docker swarm join \
    --token SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c \
    192.168.99.100:2377
```

Run the command from the output on the worker to join the swarm:

```console
$ docker swarm join \
  --token SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c \
  192.168.99.100:2377

This node joined a swarm as a worker.
```

The `docker swarm join` command does the following:

- Switches Docker Engine on the current node into Swarm mode.
- Requests a TLS certificate from the manager.
- Names the node with the machine hostname.
- Joins the current node to the swarm at the manager listen address based upon the swarm token.
- Sets the current node to `Active` availability, meaning it can receive tasks
  from the scheduler.
- Extends the `ingress` overlay network to the current node.

## Join as a manager node

When you run `docker swarm join` and pass the manager token, Docker Engine
switches into Swarm mode the same as for workers. Manager nodes also participate
in the raft consensus. The new nodes should be `Reachable`, but the existing
manager remains the swarm `Leader`.

Docker recommends three or five manager nodes per cluster to implement high
availability. Because Swarm-mode manager nodes share data using Raft, there
must be an odd number of managers. The swarm can continue to function after as
long as a quorum of more than half of the manager nodes are available.

For more detail about swarm managers and administering a swarm, see
[Administer and maintain a swarm of Docker Engines](https://docs.docker.com/engine/swarm/admin_guide/).

To retrieve the join command including the join token for manager nodes, run the
following command on a manager node:

```console
$ docker swarm join-token manager

To add a manager to this swarm, run the following command:

    docker swarm join \
    --token SWMTKN-1-61ztec5kyafptydic6jfc1i33t37flcl4nuipzcusor96k7kby-5vy9t8u35tuqm7vh67lrz9xp6 \
    192.168.99.100:2377
```

Run the command from the output on the new manager node to join it to the swarm:

```console
$ docker swarm join \
  --token SWMTKN-1-61ztec5kyafptydic6jfc1i33t37flcl4nuipzcusor96k7kby-5vy9t8u35tuqm7vh67lrz9xp6 \
  192.168.99.100:2377

This node joined a swarm as a manager.
```

## Learn More

- `swarm join` [command line reference](https://docs.docker.com/reference/cli/docker/swarm/join/)
- [Swarm mode tutorial](https://docs.docker.com/engine/swarm/swarm-tutorial/)

---

# Swarm mode key concepts

> Introducing key concepts for Docker Engine swarm mode

# Swarm mode key concepts

   Table of contents

---

This topic introduces some of the concepts unique to the cluster management and
orchestration features of Docker Engine 1.12.

## What is a swarm?

The cluster management and orchestration features embedded in Docker Engine
are built using [swarmkit](https://github.com/docker/swarmkit/). Swarmkit is a
separate project which implements Docker's orchestration layer and is used
directly within Docker.

A swarm consists of multiple Docker hosts which run in Swarm mode and act as
managers, to manage membership and delegation, and workers, which run
[swarm services](#services-and-tasks). A given Docker host can
be a manager, a worker, or perform both roles. When you create a service, you
define its optimal state - number of replicas, network and storage resources
available to it, ports the service exposes to the outside world, and more.
Docker works to maintain that desired state. For instance, if a worker node
becomes unavailable, Docker schedules that node's tasks on other nodes. A task
is a running container which is part of a swarm service and is managed by a
swarm manager, as opposed to a standalone container.

One of the key advantages of swarm services over standalone containers is that
you can modify a service's configuration, including the networks and volumes it
is connected to, without the need to manually restart the service. Docker will
update the configuration, stop the service tasks with out of date
configuration, and create new ones matching the desired configuration.

When Docker is running in Swarm mode, you can still run standalone containers
on any of the Docker hosts participating in the swarm, as well as swarm
services. A key difference between standalone containers and swarm services is
that only swarm managers can manage a swarm, while standalone containers can be
started on any daemon. Docker daemons can participate in a swarm as managers,
workers, or both.

In the same way that you can use
[Docker Compose](https://docs.docker.com/compose/) to define and run
containers, you can define and run [Swarm service](https://docs.docker.com/engine/swarm/services/) stacks.

Keep reading for details about concepts related to Docker swarm services,
including nodes, services, tasks, and load balancing.

## Nodes

A node is an instance of the Docker engine participating in the swarm. You can also think of this as a Docker node. You can run one or more nodes on a single physical computer or cloud server, but production swarm deployments typically include Docker nodes distributed across multiple physical and cloud machines.

To deploy your application to a swarm, you submit a service definition to a
manager node. The manager node dispatches units of work called
[tasks](#services-and-tasks) to worker nodes.

Manager nodes also perform the orchestration and cluster management functions
required to maintain the desired state of the swarm. Manager nodes select a
single leader to conduct orchestration tasks.

Worker nodes receive and execute tasks dispatched from manager nodes.
By default manager nodes also run services as worker nodes, but you can
configure them to run manager tasks exclusively and be manager-only
nodes. An agent runs on each worker node and reports on the tasks assigned to
it. The worker node notifies the manager node of the current state of its
assigned tasks so that the manager can maintain the desired state of each
worker.

## Services and tasks

A service is the definition of the tasks to execute on the manager or worker nodes. It
is the central structure of the swarm system and the primary root of user
interaction with the swarm.

When you create a service, you specify which container image to use and which
commands to execute inside running containers.

In the replicated services model, the swarm manager distributes a specific
number of replica tasks among the nodes based upon the scale you set in the
desired state.

For global services, the swarm runs one task for the service on every
available node in the cluster.

A task carries a Docker container and the commands to run inside the
container. It is the atomic scheduling unit of swarm. Manager nodes assign tasks
to worker nodes according to the number of replicas set in the service scale.
Once a task is assigned to a node, it cannot move to another node. It can only
run on the assigned node or fail.

## Load balancing

The swarm manager uses ingress load balancing to expose the services you
want to make available externally to the swarm. The swarm manager can
automatically assign the service a published port or you can configure a
published port for the service. You can specify any unused port. If you do not
specify a port, the swarm manager assigns the service a port in the 30000-32767
range.

External components, such as cloud load balancers, can access the service on the
published port of any node in the cluster whether or not the node is currently
running the task for the service. All nodes in the swarm route ingress
connections to a running task instance.

Swarm mode has an internal DNS component that automatically assigns each service
in the swarm a DNS entry. The swarm manager uses internal load balancing to
distribute requests among services within the cluster based upon the DNS name of
the service.

## What's next?

- Read the [Swarm mode overview](https://docs.docker.com/engine/swarm/).
- Get started with the [Swarm mode tutorial](https://docs.docker.com/engine/swarm/swarm-tutorial/).
