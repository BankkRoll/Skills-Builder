# Deploy a stack to a swarm and more

# Deploy a stack to a swarm

> How to deploy a stack to a swarm

# Deploy a stack to a swarm

   Table of contents

---

When running Docker Engine in swarm mode, you can use `docker stack deploy` to
deploy a complete application stack to the swarm. The `deploy` command accepts
a stack description in the form of a
[Compose file](https://docs.docker.com/reference/compose-file/legacy-versions/).

> Note
>
> The `docker stack deploy` command uses the legacy
> [Compose file version 3](https://docs.docker.com/reference/compose-file/legacy-versions/)
> format, used by Compose V1. The latest format, defined by the
> [Compose specification](https://docs.docker.com/reference/compose-file/)
> isn't compatible with the `docker stack deploy` command.
>
>
>
> For more information about the evolution of Compose, see
> [History of Compose](https://docs.docker.com/compose/history/).

To run through this tutorial, you need:

1. A Docker Engine running in [Swarm mode](https://docs.docker.com/engine/swarm/swarm-mode/).
  If you're not familiar with Swarm mode, you might want to read
  [Swarm mode key concepts](https://docs.docker.com/engine/swarm/key-concepts/)
  and [How services work](https://docs.docker.com/engine/swarm/how-swarm-mode-works/services/).
  > Note
  >
  > If you're trying things out on a local development environment,
  > you can put your engine into Swarm mode with `docker swarm init`.
  >
  >
  >
  > If you've already got a multi-node swarm running, keep in mind that all
  > `docker stack` and `docker service` commands must be run from a manager
  > node.
2. A current version of
  [Docker Compose](https://docs.docker.com/compose/install/).

## Set up a Docker registry

Because a swarm consists of multiple Docker Engines, a registry is required to
distribute images to all of them. You can use the
[Docker Hub](https://hub.docker.com) or maintain your own. Here's how to create
a throwaway registry, which you can discard afterward.

1. Start the registry as a service on your swarm:
  ```console
  $ docker service create --name registry --publish published=5000,target=5000 registry:2
  ```
2. Check its status with `docker service ls`:
  ```console
  $ docker service ls
  ID            NAME      REPLICAS  IMAGE                                                                               COMMAND
  l7791tpuwkco  registry  1/1       registry:2@sha256:1152291c7f93a4ea2ddc95e46d142c31e743b6dd70e194af9e6ebe530f782c17
  ```
  Once it reads `1/1` under `REPLICAS`, it's running. If it reads `0/1`, it's
  probably still pulling the image.
3. Check that it's working with `curl`:
  ```console
  $ curl http://127.0.0.1:5000/v2/
  {}
  ```

## Create the example application

The app used in this guide is based on the hit counter app in the
[Get started with Docker Compose](https://docs.docker.com/compose/gettingstarted/) guide. It consists
of a Python app which maintains a counter in a Redis instance and increments the
counter whenever you visit it.

1. Create a directory for the project:
  ```console
  $ mkdir stackdemo
  $ cd stackdemo
  ```
2. Create a file called `app.py` in the project directory and paste this in:
  ```python
  from flask import Flask
  from redis import Redis
  app = Flask(__name__)
  redis = Redis(host='redis', port=6379)
  @app.route('/')
  def hello():
      count = redis.incr('hits')
      return 'Hello World! I have been seen {} times.\n'.format(count)
  if __name__ == "__main__":
      app.run(host="0.0.0.0", port=8000, debug=True)
  ```
3. Create a file called `requirements.txt` and paste these two lines in:
  ```text
  flask
  redis
  ```
4. Create a file called `Dockerfile` and paste this in:
  ```dockerfile
  # syntax=docker/dockerfile:1
  FROM python:3.4-alpine
  ADD . /code
  WORKDIR /code
  RUN pip install -r requirements.txt
  CMD ["python", "app.py"]
  ```
5. Create a file called `compose.yaml` and paste this in:
  ```yaml
  services:
      web:
        image: 127.0.0.1:5000/stackdemo
        build: .
        ports:
          - "8000:8000"
      redis:
        image: redis:alpine
  ```
  The image for the web app is built using the Dockerfile defined
  above. It's also tagged with `127.0.0.1:5000` - the address of the registry
  created earlier. This is important when distributing the app to the
  swarm.

## Test the app with Compose

1. Start the app with `docker compose up`. This builds the web app image,
  pulls the Redis image if you don't already have it, and creates two
  containers.
  You see a warning about the Engine being in swarm mode. This is because
  Compose doesn't take advantage of swarm mode, and deploys everything to a
  single node. You can safely ignore this.
  ```console
  $ docker compose up -d
  WARNING: The Docker Engine you're using is running in swarm mode.
  Compose does not use swarm mode to deploy services to multiple nodes in
  a swarm. All containers are scheduled on the current node.
  To deploy your application across the swarm, use `docker stack deploy`.
  Creating network "stackdemo_default" with the default driver
  Building web
  ...(build output)...
  Creating stackdemo_redis_1
  Creating stackdemo_web_1
  ```
2. Check that the app is running with `docker compose ps`:
  ```console
  $ docker compose ps
        Name                     Command               State           Ports
  -----------------------------------------------------------------------------------
  stackdemo_redis_1   docker-entrypoint.sh redis ...   Up      6379/tcp
  stackdemo_web_1     python app.py                    Up      0.0.0.0:8000->8000/tcp
  ```
  You can test the app with `curl`:
  ```console
  $ curl http://localhost:8000
  Hello World! I have been seen 1 times.
  $ curl http://localhost:8000
  Hello World! I have been seen 2 times.
  $ curl http://localhost:8000
  Hello World! I have been seen 3 times.
  ```
3. Bring the app down:
  ```console
  $ docker compose down --volumes
  Stopping stackdemo_web_1 ... done
  Stopping stackdemo_redis_1 ... done
  Removing stackdemo_web_1 ... done
  Removing stackdemo_redis_1 ... done
  Removing network stackdemo_default
  ```

## Push the generated image to the registry

To distribute the web app's image across the swarm, it needs to be pushed to the
registry you set up earlier. With Compose, this is very simple:

```console
$ docker compose push

Pushing web (127.0.0.1:5000/stackdemo:latest)...
The push refers to a repository [127.0.0.1:5000/stackdemo]
5b5a49501a76: Pushed
be44185ce609: Pushed
bd7330a79bcf: Pushed
c9fc143a069a: Pushed
011b303988d2: Pushed
latest: digest: sha256:a81840ebf5ac24b42c1c676cbda3b2cb144580ee347c07e1bc80e35e5ca76507 size: 1372
```

The stack is now ready to be deployed.

## Deploy the stack to the swarm

1. Create the stack with `docker stack deploy`:
  ```console
  $ docker stack deploy --compose-file compose.yaml stackdemo
  Ignoring unsupported options: build
  Creating network stackdemo_default
  Creating service stackdemo_web
  Creating service stackdemo_redis
  ```
  The last argument is a name for the stack. Each network, volume and service
  name is prefixed with the stack name.
2. Check that it's running with `docker stack services stackdemo`:
  ```console
  $ docker stack services stackdemo
  ID            NAME             MODE        REPLICAS  IMAGE
  orvjk2263y1p  stackdemo_redis  replicated  1/1       redis:3.2-alpine@sha256:f1ed3708f538b537eb9c2a7dd50dc90a706f7debd7e1196c9264edeea521a86d
  s1nf0xy8t1un  stackdemo_web    replicated  1/1       127.0.0.1:5000/stackdemo@sha256:adb070e0805d04ba2f92c724298370b7a4eb19860222120d43e0f6351ddbc26f
  ```
  Once it's running, you should see `1/1` under `REPLICAS` for both services.
  This might take some time if you have a multi-node swarm, as images need to
  be pulled.
  As before, you can test the app with `curl`:
  ```console
  $ curl http://localhost:8000
  Hello World! I have been seen 1 times.
  $ curl http://localhost:8000
  Hello World! I have been seen 2 times.
  $ curl http://localhost:8000
  Hello World! I have been seen 3 times.
  ```
  With Docker's built-in routing mesh, you can access any node in the
  swarm on port `8000` and get routed to the app:
  ```console
  $ curl http://address-of-other-node:8000
  Hello World! I have been seen 4 times.
  ```
3. Bring the stack down with `docker stack rm`:
  ```console
  $ docker stack rm stackdemo
  Removing service stackdemo_web
  Removing service stackdemo_redis
  Removing network stackdemo_default
  ```
4. Bring the registry down with `docker service rm`:
  ```console
  $ docker service rm registry
  ```
5. If you're just testing things out on a local machine and want to bring your
  Docker Engine out of Swarm mode, use `docker swarm leave`:
  ```console
  $ docker swarm leave --force
  Node left the swarm.
  ```

---

# Run Docker Engine in swarm mode

> Run Docker Engine in swarm mode

# Run Docker Engine in swarm mode

   Table of contents

---

When you first install and start working with Docker Engine, Swarm mode is
disabled by default. When you enable Swarm mode, you work with the concept of
services managed through the `docker service` command.

There are two ways to run the engine in Swarm mode:

- Create a new swarm, covered in this article.
- [Join an existing swarm](https://docs.docker.com/engine/swarm/join-nodes/).

When you run the engine in Swarm mode on your local machine, you can create and
test services based upon images you've created or other available images. In
your production environment, Swarm mode provides a fault-tolerant platform with
cluster management features to keep your services running and available.

These instructions assume you have installed the Docker Engine on
a machine to serve as a manager node in your swarm.

If you haven't already, read through the [Swarm mode key concepts](https://docs.docker.com/engine/swarm/key-concepts/)
and try the [Swarm mode tutorial](https://docs.docker.com/engine/swarm/swarm-tutorial/).

## Create a swarm

When you run the command to create a swarm, Docker Engine starts running in Swarm mode.

Run
[docker swarm init](https://docs.docker.com/reference/cli/docker/swarm/init/)
to create a single-node swarm on the current node. The engine sets up the swarm
as follows:

- Switches the current node into Swarm mode.
- Creates a swarm named `default`.
- Designates the current node as a leader manager node for the swarm.
- Names the node with the machine hostname.
- Configures the manager to listen on an active network interface on port `2377`.
- Sets the current node to `Active` availability, meaning it can receive tasks
  from the scheduler.
- Starts an internal distributed data store for Engines participating in the
  swarm to maintain a consistent view of the swarm and all services running on it.
- By default, generates a self-signed root CA for the swarm.
- By default, generates tokens for worker and manager nodes to join the
  swarm.
- Creates an overlay network named `ingress` for publishing service ports
  external to the swarm.
- Creates an overlay default IP addresses and subnet mask for your networks

The output for `docker swarm init` provides the connection command to use when
you join new worker nodes to the swarm:

```console
$ docker swarm init
Swarm initialized: current node (dxn1zf6l61qsb1josjja83ngz) is now a manager.

To add a worker to this swarm, run the following command:

    docker swarm join \
    --token SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c \
    192.168.99.100:2377

To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.
```

### Configuring default address pools

By default Swarm mode uses a default address pool `10.0.0.0/8` for global scope (overlay) networks. Every
network that does not have a subnet specified will have a subnet sequentially allocated from this pool. In
some circumstances it may be desirable to use a different default IP address pool for networks.

For example, if the default `10.0.0.0/8` range conflicts with already allocated address space in your network,
then it is desirable to ensure that networks use a different range without requiring swarm users to specify
each subnet with the `--subnet` command.

To configure custom default address pools, you must define pools at swarm initialization using the
`--default-addr-pool` command line option. This command line option uses CIDR notation for defining the subnet mask.
To create the custom address pool for Swarm, you must define at least one default address pool, and an optional default address pool subnet mask. For example, for the `10.0.0.0/27`, use the value `27`.

Docker allocates subnet addresses from the address ranges specified by the `--default-addr-pool` option. For example, a command line option `--default-addr-pool 10.10.0.0/16` indicates that Docker will allocate subnets from that `/16` address range. If `--default-addr-pool-mask-len` were unspecified or set explicitly to 24, this would result in 256 `/24` networks of the form `10.10.X.0/24`.

The subnet range comes from the `--default-addr-pool`, (such as `10.10.0.0/16`). The size of 16 there represents the number of networks one can create within that `default-addr-pool` range. The `--default-addr-pool` option may occur multiple times with each option providing additional addresses for docker to use for overlay subnets.

The format of the command is:

```console
$ docker swarm init --default-addr-pool <IP range in CIDR> [--default-addr-pool <IP range in CIDR> --default-addr-pool-mask-length <CIDR value>]
```

The command to create a default IP address pool with a /16 (class B) for the `10.20.0.0` network looks like this:

```console
$ docker swarm init --default-addr-pool 10.20.0.0/16
```

The command to create a default IP address pool with a `/16` (class B) for the `10.20.0.0` and `10.30.0.0` networks, and to
create a subnet mask of `/26` for each network looks like this:

```console
$ docker swarm init --default-addr-pool 10.20.0.0/16 --default-addr-pool 10.30.0.0/16 --default-addr-pool-mask-length 26
```

In this example, `docker network create -d overlay net1` will result in `10.20.0.0/26` as the allocated subnet for `net1`,
and `docker network create -d overlay net2` will result in `10.20.0.64/26` as the allocated subnet for `net2`. This continues until
all the subnets are exhausted.

Refer to the following pages for more information:

- [Swarm networking](https://docs.docker.com/engine/swarm/networking/) for more information about the default address pool usage
- `docker swarm init` [CLI reference](https://docs.docker.com/reference/cli/docker/swarm/init/) for more detail on the `--default-addr-pool` flag.

### Configure the advertise address

Manager nodes use an advertise address to allow other nodes in the swarm access
to the Swarmkit API and overlay networking. The other nodes on the swarm must be
able to access the manager node on its advertise address.

If you don't specify an advertise address, Docker checks if the system has a
single IP address. If so, Docker uses the IP address with the listening port
`2377` by default. If the system has multiple IP addresses, you must specify the
correct `--advertise-addr` to enable inter-manager communication and overlay
networking:

```console
$ docker swarm init --advertise-addr <MANAGER-IP>
```

You must also specify the `--advertise-addr` if the address where other nodes
reach the first manager node is not the same address the manager sees as its
own. For instance, in a cloud setup that spans different regions, hosts have
both internal addresses for access within the region and external addresses that
you use for access from outside that region. In this case, specify the external
address with `--advertise-addr` so that the node can propagate that information
to other nodes that subsequently connect to it.

Refer to the `docker swarm init` [CLI reference](https://docs.docker.com/reference/cli/docker/swarm/init/)
for more detail on the advertise address.

### View the join command or update a swarm join token

Nodes require a secret token to join the swarm. The token for worker nodes is
different from the token for manager nodes. Nodes only use the join-token at the
moment they join the swarm. Rotating the join token after a node has already
joined a swarm does not affect the node's swarm membership. Token rotation
ensures an old token cannot be used by any new nodes attempting to join the
swarm.

To retrieve the join command including the join token for worker nodes, run:

```console
$ docker swarm join-token worker

To add a worker to this swarm, run the following command:

    docker swarm join \
    --token SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c \
    192.168.99.100:2377

This node joined a swarm as a worker.
```

To view the join command and token for manager nodes, run:

```console
$ docker swarm join-token manager

To add a manager to this swarm, run the following command:

    docker swarm join \
    --token SWMTKN-1-59egwe8qangbzbqb3ryawxzk3jn97ifahlsrw01yar60pmkr90-bdjfnkcflhooyafetgjod97sz \
    192.168.99.100:2377
```

Pass the `--quiet` flag to print only the token:

```console
$ docker swarm join-token --quiet worker

SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c
```

Be careful with the join tokens because they are the secrets necessary to join
the swarm. In particular, checking a secret into version control is a bad
practice because it would allow anyone with access to the application source
code to add new nodes to the swarm. Manager tokens are especially sensitive
because they allow a new manager node to join and gain control over the whole
swarm.

We recommend that you rotate the join tokens in the following circumstances:

- If a token was checked-in by accident into a version control system, group
  chat or accidentally printed to your logs.
- If you suspect a node has been compromised.
- If you wish to guarantee that no new nodes can join the swarm.

Additionally, it is a best practice to implement a regular rotation schedule for
any secret including swarm join tokens. We recommend that you rotate your tokens
at least every 6 months.

Run `swarm join-token --rotate` to invalidate the old token and generate a new
token. Specify whether you want to rotate the token for `worker` or `manager`
nodes:

```console
$ docker swarm join-token  --rotate worker

To add a worker to this swarm, run the following command:

    docker swarm join \
    --token SWMTKN-1-2kscvs0zuymrsc9t0ocyy1rdns9dhaodvpl639j2bqx55uptag-ebmn5u927reawo27s3azntd44 \
    192.168.99.100:2377
```

## Learn more

- [Join nodes to a swarm](https://docs.docker.com/engine/swarm/join-nodes/)
- `swarm init` [command line reference](https://docs.docker.com/reference/cli/docker/swarm/init/)
- [Swarm mode tutorial](https://docs.docker.com/engine/swarm/swarm-tutorial/)

---

# Add nodes to the swarm

> Add nodes to the swarm

# Add nodes to the swarm

---

Once you've [created a swarm](https://docs.docker.com/engine/swarm/swarm-tutorial/create-swarm/) with a manager node, you're ready
to add worker nodes.

1. Open a terminal and ssh into the machine where you want to run a worker node.
  This tutorial uses the name `worker1`.
2. Run the command produced by the `docker swarm init` output from the
  [Create a swarm](https://docs.docker.com/engine/swarm/swarm-tutorial/create-swarm/) tutorial step to create a worker node
  joined to the existing swarm:
  ```console
  $ docker swarm join \
    --token  SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c \
    192.168.99.100:2377
  This node joined a swarm as a worker.
  ```
  If you don't have the command available, you can run the following command
  on a manager node to retrieve the join command for a worker:
  ```console
  $ docker swarm join-token worker
  To add a worker to this swarm, run the following command:
      docker swarm join \
      --token SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c \
      192.168.99.100:2377
  ```
3. Open a terminal and ssh into the machine where you want to run a second
  worker node. This tutorial uses the name `worker2`.
4. Run the command produced by the `docker swarm init` output from the
  [Create a swarm](https://docs.docker.com/engine/swarm/swarm-tutorial/create-swarm/) tutorial step to create a second worker
  node joined to the existing swarm:
  ```console
  $ docker swarm join \
    --token SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c \
    192.168.99.100:2377
  This node joined a swarm as a worker.
  ```
5. Open a terminal and ssh into the machine where the manager node runs and
  run the `docker node ls` command to see the worker nodes:
  ```console
  $ docker node ls
  ID                           HOSTNAME  STATUS  AVAILABILITY  MANAGER STATUS
  03g1y59jwfg7cf99w4lt0f662    worker2   Ready   Active
  9j68exjopxe7wfl6yuxml7a7j    worker1   Ready   Active
  dxn1zf6l61qsb1josjja83ngz *  manager1  Ready   Active        Leader
  ```
  The `MANAGER` column identifies the manager nodes in the swarm. The empty
  status in this column for `worker1` and `worker2` identifies them as worker nodes.
  Swarm management commands like `docker node ls` only work on manager nodes.

## What's next?

Now your swarm consists of a manager and two worker nodes. Next, you'll deploy a service.

[Deploy a service](https://docs.docker.com/engine/swarm/swarm-tutorial/deploy-service/)

---

# Create a swarm

> Initialize the swarm

# Create a swarm

---

After you complete the [tutorial setup](https://docs.docker.com/engine/swarm/swarm-tutorial/) steps, you're ready
to create a swarm. Make sure the Docker Engine daemon is started on the host
machines.

1. Open a terminal and ssh into the machine where you want to run your manager
  node. This tutorial uses a machine named `manager1`.
2. Run the following command to create a new swarm:
  ```console
  $ docker swarm init --advertise-addr <MANAGER-IP>
  ```
  In the tutorial, the following command creates a swarm on the `manager1`
  machine:
  ```console
  $ docker swarm init --advertise-addr 192.168.99.100
  Swarm initialized: current node (dxn1zf6l61qsb1josjja83ngz) is now a manager.
  To add a worker to this swarm, run the following command:
      docker swarm join \
      --token SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c \
      192.168.99.100:2377
  To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.
  ```
  The `--advertise-addr` flag configures the manager node to publish its
  address as `192.168.99.100`. The other nodes in the swarm must be able
  to access the manager at the IP address.
  The output includes the commands to join new nodes to the swarm. Nodes will
  join as managers or workers depending on the value for the `--token`
  flag.
3. Run `docker info` to view the current state of the swarm:
  ```console
  $ docker info
  Containers: 2
  Running: 0
  Paused: 0
  Stopped: 2
    ...snip...
  Swarm: active
    NodeID: dxn1zf6l61qsb1josjja83ngz
    Is Manager: true
    Managers: 1
    Nodes: 1
    ...snip...
  ```
4. Run the `docker node ls` command to view information about nodes:
  ```console
  $ docker node ls
  ID                           HOSTNAME  STATUS  AVAILABILITY  MANAGER STATUS
  dxn1zf6l61qsb1josjja83ngz *  manager1  Ready   Active        Leader
  ```
  The `*` next to the node ID indicates that you're currently connected on
  this node.
  Docker Engine Swarm mode automatically names the node with the machine host
  name. The tutorial covers other columns in later steps.

## Next steps

Next, you'll add two more nodes to the cluster.

[Add two more nodes](https://docs.docker.com/engine/swarm/swarm-tutorial/add-nodes/)

---

# Delete the service running on the swarm

> Remove the service from the swarm

# Delete the service running on the swarm

---

The remaining steps in the tutorial don't use the `helloworld` service, so now
you can delete the service from the swarm.

1. If you haven't already, open a terminal and ssh into the machine where you
  run your manager node. For example, the tutorial uses a machine named
  `manager1`.
2. Run `docker service rm helloworld` to remove the `helloworld` service.
  ```console
  $ docker service rm helloworld
  helloworld
  ```
3. Run `docker service inspect <SERVICE-ID>` to verify that the swarm manager
  removed the service. The CLI returns a message that the service is not
  found:
  ```console
  $ docker service inspect helloworld
  []
  Status: Error: no such service: helloworld, Code: 1
  ```
4. Even though the service no longer exists, the task containers take a few
  seconds to clean up. You can use `docker ps` on the nodes to verify when the
  tasks have been removed.
  ```console
  $ docker ps
  CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS     NAMES
  db1651f50347        alpine:latest       "ping docker.com"        44 minutes ago      Up 46 seconds                 helloworld.5.9lkmos2beppihw95vdwxy1j3w
  43bf6e532a92        alpine:latest       "ping docker.com"        44 minutes ago      Up 46 seconds                 helloworld.3.a71i8rp6fua79ad43ycocl4t2
  5a0fb65d8fa7        alpine:latest       "ping docker.com"        44 minutes ago      Up 45 seconds                 helloworld.2.2jpgensh7d935qdc857pxulfr
  afb0ba67076f        alpine:latest       "ping docker.com"        44 minutes ago      Up 46 seconds                 helloworld.4.1c47o7tluz7drve4vkm2m5olx
  688172d3bfaa        alpine:latest       "ping docker.com"        45 minutes ago      Up About a minute             helloworld.1.74nbhb3fhud8jfrhigd7s29we
  $ docker ps
  CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS     NAMES
  ```

## Next steps

Next, you'll set up a new service and apply a rolling update.

[Apply rolling updates](https://docs.docker.com/engine/swarm/swarm-tutorial/rolling-update/)

---

# Deploy a service to the swarm

> Deploy a service to the swarm

# Deploy a service to the swarm

---

After you [create a swarm](https://docs.docker.com/engine/swarm/swarm-tutorial/create-swarm/), you can deploy a service to the
swarm. For this tutorial, you also [added worker nodes](https://docs.docker.com/engine/swarm/swarm-tutorial/add-nodes/), but that
is not a requirement to deploy a service.

1. Open a terminal and ssh into the machine where you run your manager node.
  For example, the tutorial uses a machine named `manager1`.
2. Run the following command:
  ```console
  $ docker service create --replicas 1 --name helloworld alpine ping docker.com
  9uk4639qpg7npwf3fn2aasksr
  ```
  - The `docker service create` command creates the service.
  - The `--name` flag names the service `helloworld`.
  - The `--replicas` flag specifies the desired state of 1 running instance.
  - The arguments `alpine ping docker.com` define the service as an Alpine
    Linux container that executes the command `ping docker.com`.
3. Run `docker service ls` to see the list of running services:
  ```console
  $ docker service ls
  ID            NAME        SCALE  IMAGE   COMMAND
  9uk4639qpg7n  helloworld  1/1    alpine  ping docker.com
  ```

## Next steps

Now you're ready to inspect the service.

[Inspect the service](https://docs.docker.com/engine/swarm/swarm-tutorial/inspect-service/)

---

# Drain a node on the swarm

> Drain nodes on the swarm

# Drain a node on the swarm

---

In earlier steps of the tutorial, all the nodes have been running with `Active`
availability. The swarm manager can assign tasks to any `Active` node, so up to
now all nodes have been available to receive tasks.

Sometimes, such as planned maintenance times, you need to set a node to `Drain`
availability. `Drain` availability prevents a node from receiving new tasks
from the swarm manager. It also means the manager stops tasks running on the
node and launches replica tasks on a node with `Active` availability.

> Important
>
> Setting a node to `Drain` does not remove standalone containers from that node,
> such as those created with `docker run`, `docker compose up`, or the Docker Engine
> API. A node's status, including `Drain`, only affects the node's ability to schedule
> swarm service workloads.

1. If you haven't already, open a terminal and ssh into the machine where you
  run your manager node. For example, the tutorial uses a machine named
  `manager1`.
2. Verify that all your nodes are actively available.
  ```console
  $ docker node ls
  ID                           HOSTNAME  STATUS  AVAILABILITY  MANAGER STATUS
  1bcef6utixb0l0ca7gxuivsj0    worker2   Ready   Active
  38ciaotwjuritcdtn9npbnkuz    worker1   Ready   Active
  e216jshn25ckzbvmwlnh5jr3g *  manager1  Ready   Active        Leader
  ```
3. If you aren't still running the `redis` service from the
  [rolling update](https://docs.docker.com/engine/swarm/swarm-tutorial/rolling-update/) tutorial, start it now:
  ```console
  $ docker service create --replicas 3 --name redis --update-delay 10s redis:7.4.0
  c5uo6kdmzpon37mgj9mwglcfw
  ```
4. Run `docker service ps redis` to see how the swarm manager assigned the
  tasks to different nodes:
  ```console
  $ docker service ps redis
  NAME                               IMAGE        NODE     DESIRED STATE  CURRENT STATE
  redis.1.7q92v0nr1hcgts2amcjyqg3pq  redis:7.4.0  manager1 Running        Running 26 seconds
  redis.2.7h2l8h3q3wqy5f66hlv9ddmi6  redis:7.4.0  worker1  Running        Running 26 seconds
  redis.3.9bg7cezvedmkgg6c8yzvbhwsd  redis:7.4.0  worker2  Running        Running 26 seconds
  ```
  In this case the swarm manager distributed one task to each node. You may
  see the tasks distributed differently among the nodes in your environment.
5. Run `docker node update --availability drain <NODE-ID>` to drain a node that
  had a task assigned to it:
  ```console
  $ docker node update --availability drain worker1
  worker1
  ```
6. Inspect the node to check its availability:
  ```console
  $ docker node inspect --pretty worker1
  ID:			38ciaotwjuritcdtn9npbnkuz
  Hostname:		worker1
  Status:
   State:			Ready
   Availability:		Drain
  ...snip...
  ```
  The drained node shows `Drain` for `Availability`.
7. Run `docker service ps redis` to see how the swarm manager updated the
  task assignments for the `redis` service:
  ```console
  $ docker service ps redis
  NAME                                    IMAGE        NODE      DESIRED STATE  CURRENT STATE           ERROR
  redis.1.7q92v0nr1hcgts2amcjyqg3pq       redis:7.4.0  manager1  Running        Running 4 minutes
  redis.2.b4hovzed7id8irg1to42egue8       redis:7.4.0  worker2   Running        Running About a minute
   \_ redis.2.7h2l8h3q3wqy5f66hlv9ddmi6   redis:7.4.0  worker1   Shutdown       Shutdown 2 minutes ago
  redis.3.9bg7cezvedmkgg6c8yzvbhwsd       redis:7.4.0  worker2   Running        Running 4 minutes
  ```
  The swarm manager maintains the desired state by ending the task on a node
  with `Drain` availability and creating a new task on a node with `Active`
  availability.
8. Run `docker node update --availability active <NODE-ID>` to return the
  drained node to an active state:
  ```console
  $ docker node update --availability active worker1
  worker1
  ```
9. Inspect the node to see the updated state:
  ```console
  $ docker node inspect --pretty worker1
  ID:			38ciaotwjuritcdtn9npbnkuz
  Hostname:		worker1
  Status:
   State:			Ready
   Availability:		Active
  ...snip...
  ```
  When you set the node back to `Active` availability, it can receive new tasks:
  - during a service update to scale up
  - during a rolling update
  - when you set another node to `Drain` availability
  - when a task fails on another active node

## Next steps

Next, you'll learn how to use a Swarm mode routing mesh

[Use a Swarm mode routing mesh](https://docs.docker.com/engine/swarm/ingress/)

---

# Inspect a service on the swarm

> Inspect the application

# Inspect a service on the swarm

---

When you have [deployed a service](https://docs.docker.com/engine/swarm/swarm-tutorial/deploy-service/) to your swarm, you can use
the Docker CLI to see details about the service running in the swarm.

1. If you haven't already, open a terminal and ssh into the machine where you
  run your manager node. For example, the tutorial uses a machine named
  `manager1`.
2. Run `docker service inspect --pretty <SERVICE-ID>` to display the details
  about a service in an easily readable format.
  To see the details on the `helloworld` service:
  ```console
  [manager1]$ docker service inspect --pretty helloworld
  ID:		9uk4639qpg7npwf3fn2aasksr
  Name:		helloworld
  Service Mode:	REPLICATED
   Replicas:		1
  Placement:
  UpdateConfig:
   Parallelism:	1
  ContainerSpec:
   Image:		alpine
   Args:	ping docker.com
  Resources:
  Endpoint Mode:  vip
  ```
  > Tip
  >
  > To return the service details in json format, run the same command
  > without the `--pretty` flag.
  ```console
  [manager1]$ docker service inspect helloworld
  [
  {
      "ID": "9uk4639qpg7npwf3fn2aasksr",
      "Version": {
          "Index": 418
      },
      "CreatedAt": "2016-06-16T21:57:11.622222327Z",
      "UpdatedAt": "2016-06-16T21:57:11.622222327Z",
      "Spec": {
          "Name": "helloworld",
          "TaskTemplate": {
              "ContainerSpec": {
                  "Image": "alpine",
                  "Args": [
                      "ping",
                      "docker.com"
                  ]
              },
              "Resources": {
                  "Limits": {},
                  "Reservations": {}
              },
              "RestartPolicy": {
                  "Condition": "any",
                  "MaxAttempts": 0
              },
              "Placement": {}
          },
          "Mode": {
              "Replicated": {
                  "Replicas": 1
              }
          },
          "UpdateConfig": {
              "Parallelism": 1
          },
          "EndpointSpec": {
              "Mode": "vip"
          }
      },
      "Endpoint": {
          "Spec": {}
      }
  }
  ]
  ```
3. Run `docker service ps <SERVICE-ID>` to see which nodes are running the
  service:
  ```console
  [manager1]$ docker service ps helloworld
  NAME                                    IMAGE   NODE     DESIRED STATE  CURRENT STATE           ERROR               PORTS
  helloworld.1.8p1vev3fq5zm0mi8g0as41w35  alpine  worker2  Running        Running 3 minutes
  ```
  In this case, the one instance of the `helloworld` service is running on the
  `worker2` node. You may see the service running on your manager node. By
  default, manager nodes in a swarm can execute tasks just like worker nodes.
  Swarm also shows you the `DESIRED STATE` and `CURRENT STATE` of the service
  task so you can see if tasks are running according to the service
  definition.
4. Run `docker ps` on the node where the task is running to see details about
  the container for the task.
  > Tip
  >
  > If `helloworld` is running on a node other than your manager node,
  > you must ssh to that node.
  ```console
  [worker2]$ docker ps
  CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
  e609dde94e47        alpine:latest       "ping docker.com"   3 minutes ago       Up 3 minutes                            helloworld.1.8p1vev3fq5zm0mi8g0as41w35
  ```

## Next steps

Next, you'll change the scale for the service running in the swarm.

[Change the scale](https://docs.docker.com/engine/swarm/swarm-tutorial/scale-service/)

---

# Apply rolling updates to a service

> Apply rolling updates to a service on the swarm

# Apply rolling updates to a service

---

In a previous step of the tutorial, you [scaled](https://docs.docker.com/engine/swarm/swarm-tutorial/scale-service/) the number of
instances of a service. In this part of the tutorial, you deploy a service based
on the Redis 7.4.0 container tag. Then you upgrade the service to use the
Redis 7.4.1 container image using rolling updates.

1. If you haven't already, open a terminal and ssh into the machine where you
  run your manager node. For example, the tutorial uses a machine named
  `manager1`.
2. Deploy your Redis tag to the swarm and configure the swarm with a 10 second
  update delay. Note that the following example shows an older Redis tag:
  ```console
  $ docker service create \
    --replicas 3 \
    --name redis \
    --update-delay 10s \
    redis:7.4.0
  0u6a4s31ybk7yw2wyvtikmu50
  ```
  You configure the rolling update policy at service deployment time.
  The `--update-delay` flag configures the time delay between updates to a
  service task or sets of tasks. You can describe the time `T` as a
  combination of the number of seconds `Ts`, minutes `Tm`, or hours `Th`. So
  `10m30s` indicates a 10 minute 30 second delay.
  By default the scheduler updates 1 task at a time. You can pass the
  `--update-parallelism` flag to configure the maximum number of service tasks
  that the scheduler updates simultaneously.
  By default, when an update to an individual task returns a state of
  `RUNNING`, the scheduler schedules another task to update until all tasks
  are updated. If at any time during an update a task returns `FAILED`, the
  scheduler pauses the update. You can control the behavior using the
  `--update-failure-action` flag for `docker service create` or
  `docker service update`.
3. Inspect the `redis` service:
  ```console
  $ docker service inspect --pretty redis
  ID:             0u6a4s31ybk7yw2wyvtikmu50
  Name:           redis
  Service Mode:   Replicated
   Replicas:      3
  Placement:
   Strategy:	    Spread
  UpdateConfig:
   Parallelism:   1
   Delay:         10s
  ContainerSpec:
   Image:         redis:7.4.0
  Resources:
  Endpoint Mode:  vip
  ```
4. Now you can update the container image for `redis`. The swarm manager
  applies the update to nodes according to the `UpdateConfig` policy:
  ```console
  $ docker service update --image redis:7.4.1 redis
  redis
  ```
  The scheduler applies rolling updates as follows by default:
  - Stop the first task.
  - Schedule update for the stopped task.
  - Start the container for the updated task.
  - If the update to a task returns `RUNNING`, wait for the
    specified delay period then start the next task.
  - If, at any time during the update, a task returns `FAILED`, pause the
    update.
5. Run `docker service inspect --pretty redis` to see the new image in the
  desired state:
  ```console
  $ docker service inspect --pretty redis
  ID:             0u6a4s31ybk7yw2wyvtikmu50
  Name:           redis
  Service Mode:   Replicated
   Replicas:      3
  Placement:
   Strategy:	    Spread
  UpdateConfig:
   Parallelism:   1
   Delay:         10s
  ContainerSpec:
   Image:         redis:7.4.1
  Resources:
  Endpoint Mode:  vip
  ```
  The output of `service inspect` shows if your update paused due to failure:
  ```console
  $ docker service inspect --pretty redis
  ID:             0u6a4s31ybk7yw2wyvtikmu50
  Name:           redis
  ...snip...
  Update status:
   State:      paused
   Started:    11 seconds ago
   Message:    update paused due to failure or early termination of task 9p7ith557h8ndf0ui9s0q951b
  ...snip...
  ```
  To restart a paused update run `docker service update <SERVICE-ID>`. For example:
  ```console
  $ docker service update redis
  ```
  To avoid repeating certain update failures, you may need to reconfigure the
  service by passing flags to `docker service update`.
6. Run `docker service ps <SERVICE-ID>` to watch the rolling update:
  ```console
  $ docker service ps redis
  NAME                                   IMAGE        NODE       DESIRED STATE  CURRENT STATE            ERROR
  redis.1.dos1zffgeofhagnve8w864fco      redis:7.4.1  worker1    Running        Running 37 seconds
   \_ redis.1.88rdo6pa52ki8oqx6dogf04fh  redis:7.4.0  worker2    Shutdown       Shutdown 56 seconds ago
  redis.2.9l3i4j85517skba5o7tn5m8g0      redis:7.4.1  worker2    Running        Running About a minute
   \_ redis.2.66k185wilg8ele7ntu8f6nj6i  redis:7.4.0  worker1    Shutdown       Shutdown 2 minutes ago
  redis.3.egiuiqpzrdbxks3wxgn8qib1g      redis:7.4.1  worker1    Running        Running 48 seconds
   \_ redis.3.ctzktfddb2tepkr45qcmqln04  redis:7.4.0  mmanager1  Shutdown       Shutdown 2 minutes ago
  ```
  Before Swarm updates all of the tasks, you can see that some are running
  `redis:7.4.0` while others are running `redis:7.4.1`. The output above shows
  the state once the rolling updates are done.

## Next steps

Next, you'll learn how to drain a node in the swarm.

[Drain a node](https://docs.docker.com/engine/swarm/swarm-tutorial/drain-node/)

---

# Scale the service in the swarm

> Scale the service running in the swarm

# Scale the service in the swarm

---

Once you have [deployed a service](https://docs.docker.com/engine/swarm/swarm-tutorial/deploy-service/) to a swarm, you are ready
to use the Docker CLI to scale the number of containers in
the service. Containers running in a service are called tasks.

1. If you haven't already, open a terminal and ssh into the machine where you
  run your manager node. For example, the tutorial uses a machine named
  `manager1`.
2. Run the following command to change the desired state of the
  service running in the swarm:
  ```console
  $ docker service scale <SERVICE-ID>=<NUMBER-OF-TASKS>
  ```
  For example:
  ```console
  $ docker service scale helloworld=5
  helloworld scaled to 5
  ```
3. Run `docker service ps <SERVICE-ID>` to see the updated task list:
  ```console
  $ docker service ps helloworld
  NAME                                    IMAGE   NODE      DESIRED STATE  CURRENT STATE
  helloworld.1.8p1vev3fq5zm0mi8g0as41w35  alpine  worker2   Running        Running 7 minutes
  helloworld.2.c7a7tcdq5s0uk3qr88mf8xco6  alpine  worker1   Running        Running 24 seconds
  helloworld.3.6crl09vdcalvtfehfh69ogfb1  alpine  worker1   Running        Running 24 seconds
  helloworld.4.auky6trawmdlcne8ad8phb0f1  alpine  manager1  Running        Running 24 seconds
  helloworld.5.ba19kca06l18zujfwxyc5lkyn  alpine  worker2   Running        Running 24 seconds
  ```
  You can see that swarm has created 4 new tasks to scale to a total of 5
  running instances of Alpine Linux. The tasks are distributed between the
  three nodes of the swarm. One is running on `manager1`.
4. Run `docker ps` to see the containers running on the node where you're
  connected. The following example shows the tasks running on `manager1`:
  ```console
  $ docker ps
  CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
  528d68040f95        alpine:latest       "ping docker.com"   About a minute ago   Up About a minute                       helloworld.4.auky6trawmdlcne8ad8phb0f1
  ```
  If you want to see the containers running on other nodes, ssh into
  those nodes and run the `docker ps` command.

## Next steps

At this point in the tutorial, you're finished with the `helloworld` service. Next, you'll delete the service

[Delete the service](https://docs.docker.com/engine/swarm/swarm-tutorial/delete-service/)
