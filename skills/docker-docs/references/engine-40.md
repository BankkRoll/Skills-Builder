# Administer and maintain a swarm of Docker Engines and more

# Administer and maintain a swarm of Docker Engines

> Manager administration guide

# Administer and maintain a swarm of Docker Engines

   Table of contents

---

When you run a swarm of Docker Engines, manager nodes are the key components
for managing the swarm and storing the swarm state. It is important to
understand some key features of manager nodes to properly deploy and
maintain the swarm.

Refer to [How nodes work](https://docs.docker.com/engine/swarm/how-swarm-mode-works/nodes/)
for a brief overview of Docker Swarm mode and the difference between manager and
worker nodes.

## Operate manager nodes in a swarm

Swarm manager nodes use the [Raft Consensus Algorithm](https://docs.docker.com/engine/swarm/raft/) to manage the
swarm state. You only need to understand some general concepts of Raft in
order to manage a swarm.

There is no limit on the number of manager nodes. The decision about how many
manager nodes to implement is a trade-off between performance and
fault-tolerance. Adding manager nodes to a swarm makes the swarm more
fault-tolerant. However, additional manager nodes reduce write performance
because more nodes must acknowledge proposals to update the swarm state.
This means more network round-trip traffic.

Raft requires a majority of managers, also called the quorum, to agree on
proposed updates to the swarm, such as node additions or removals. Membership
operations are subject to the same constraints as state replication.

### Maintain the quorum of managers

If the swarm loses the quorum of managers, the swarm cannot perform management
tasks. If your swarm has multiple managers, always have more than two.
To maintain quorum, a majority of managers must be available. An odd number of
managers is recommended, because the next even number does not make the quorum
easier to keep. For instance, whether you have 3 or 4 managers, you can still
only lose 1 manager and maintain the quorum. If you have 5 or 6 managers, you
can still only lose two.

Even if a swarm loses the quorum of managers, swarm tasks on existing worker
nodes continue to run. However, swarm nodes cannot be added, updated, or
removed, and new or existing tasks cannot be started, stopped, moved, or
updated.

See [Recovering from losing the quorum](#recover-from-losing-the-quorum) for
troubleshooting steps if you do lose the quorum of managers.

## Configure the manager to advertise on a static IP address

When initiating a swarm, you must specify the `--advertise-addr` flag to
advertise your address to other manager nodes in the swarm. For more
information, see [Run Docker Engine in swarm mode](https://docs.docker.com/engine/swarm/swarm-mode/#configure-the-advertise-address). Because manager nodes are
meant to be a stable component of the infrastructure, you should use a *fixed
IP address* for the advertise address to prevent the swarm from becoming
unstable on machine reboot.

If the whole swarm restarts and every manager node subsequently gets a new IP
address, there is no way for any node to contact an existing manager. Therefore
the swarm is hung while nodes try to contact one another at their old IP addresses.

Dynamic IP addresses are OK for worker nodes.

## Add manager nodes for fault tolerance

You should maintain an odd number of managers in the swarm to support manager
node failures. Having an odd number of managers ensures that during a network
partition, there is a higher chance that the quorum remains available to process
requests if the network is partitioned into two sets. Keeping the quorum is not
guaranteed if you encounter more than two network partitions.

| Swarm Size | Majority | Fault Tolerance |
| --- | --- | --- |
| 1 | 1 | 0 |
| 2 | 2 | 0 |
| 3 | 2 | 1 |
| 4 | 3 | 1 |
| 5 | 3 | 2 |
| 6 | 4 | 2 |
| 7 | 4 | 3 |
| 8 | 5 | 3 |
| 9 | 5 | 4 |

For example, in a swarm with *5 nodes*, if you lose *3 nodes*, you don't have a
quorum. Therefore you can't add or remove nodes until you recover one of the
unavailable manager nodes or recover the swarm with disaster recovery
commands. See [Recover from disaster](#recover-from-disaster).

While it is possible to scale a swarm down to a single manager node, it is
impossible to demote the last manager node. This ensures you maintain access to
the swarm and that the swarm can still process requests. Scaling down to a
single manager is an unsafe operation and is not recommended. If
the last node leaves the swarm unexpectedly during the demote operation, the
swarm becomes unavailable until you reboot the node or restart with
`--force-new-cluster`.

You manage swarm membership with the `docker swarm` and `docker node`
subsystems. Refer to [Add nodes to a swarm](https://docs.docker.com/engine/swarm/join-nodes/) for more information
on how to add worker nodes and promote a worker node to be a manager.

### Distribute manager nodes

In addition to maintaining an odd number of manager nodes, pay attention to
datacenter topology when placing managers. For optimal fault-tolerance, distribute
manager nodes across a minimum of 3 availability-zones to support failures of an
entire set of machines or common maintenance scenarios. If you suffer a failure
in any of those zones, the swarm should maintain the quorum of manager nodes
available to process requests and rebalance workloads.

| Swarm manager nodes | Repartition (on 3 Availability zones) |
| --- | --- |
| 3 | 1-1-1 |
| 5 | 2-2-1 |
| 7 | 3-2-2 |
| 9 | 3-3-3 |

### Run manager-only nodes

By default manager nodes also act as a worker nodes. This means the scheduler
can assign tasks to a manager node. For small and non-critical swarms
assigning tasks to managers is relatively low-risk as long as you schedule
services using resource constraints for cpu and memory.

However, because manager nodes use the Raft consensus algorithm to replicate data
in a consistent way, they are sensitive to resource starvation. You should
isolate managers in your swarm from processes that might block swarm
operations like swarm heartbeat or leader elections.

To avoid interference with manager node operation, you can drain manager nodes
to make them unavailable as worker nodes:

```console
$ docker node update --availability drain NODE
```

When you drain a node, the scheduler reassigns any tasks running on the node to
other available worker nodes in the swarm. It also prevents the scheduler from
assigning tasks to the node.

## Add worker nodes for load balancing

[Add nodes to the swarm](https://docs.docker.com/engine/swarm/join-nodes/) to balance your swarm's
load. Replicated service tasks are distributed across the swarm as evenly as
possible over time, as long as the worker nodes are matched to the requirements
of the services. When limiting a service to run on only specific types of nodes,
such as nodes with a specific number of CPUs or amount of memory, remember that
worker nodes that do not meet these requirements cannot run these tasks.

## Monitor swarm health

You can monitor the health of manager nodes by querying the docker `nodes` API
in JSON format through the `/nodes` HTTP endpoint. Refer to the
[nodes API documentation](https://docs.docker.com/reference/api/engine/version/v1.25/#tag/Node)
for more information.

From the command line, run `docker node inspect <id-node>` to query the nodes.
For instance, to query the reachability of the node as a manager:

```console
$ docker node inspect manager1 --format "{{ .ManagerStatus.Reachability }}"
reachable
```

To query the status of the node as a worker that accept tasks:

```console
$ docker node inspect manager1 --format "{{ .Status.State }}"
ready
```

From those commands, we can see that `manager1` is both at the status
`reachable` as a manager and `ready` as a worker.

An `unreachable` health status means that this particular manager node is unreachable
from other manager nodes. In this case you need to take action to restore the unreachable
manager:

- Restart the daemon and see if the manager comes back as reachable.
- Reboot the machine.
- If neither restarting nor rebooting works, you should add another manager node or promote a worker to be a manager node. You also need to cleanly remove the failed node entry from the manager set with `docker node demote <NODE>` and `docker node rm <id-node>`.

Alternatively you can also get an overview of the swarm health from a manager
node with `docker node ls`:

```console
$ docker node ls
ID                           HOSTNAME  MEMBERSHIP  STATUS  AVAILABILITY  MANAGER STATUS
1mhtdwhvsgr3c26xxbnzdc3yp    node05    Accepted    Ready   Active
516pacagkqp2xc3fk9t1dhjor    node02    Accepted    Ready   Active        Reachable
9ifojw8of78kkusuc4a6c23fx *  node01    Accepted    Ready   Active        Leader
ax11wdpwrrb6db3mfjydscgk7    node04    Accepted    Ready   Active
bb1nrq2cswhtbg4mrsqnlx1ck    node03    Accepted    Ready   Active        Reachable
di9wxgz8dtuh9d2hn089ecqkf    node06    Accepted    Ready   Active
```

## Troubleshoot a manager node

You should never restart a manager node by copying the `raft` directory from another node. The data directory is unique to a node ID. A node can only use a node ID once to join the swarm. The node ID space should be globally unique.

To cleanly re-join a manager node to a cluster:

1. Demote the node to a worker using `docker node demote <NODE>`.
2. Remove the node from the swarm using `docker node rm <NODE>`.
3. Re-join the node to the swarm with a fresh state using `docker swarm join`.

For more information on joining a manager node to a swarm, refer to
[Join nodes to a swarm](https://docs.docker.com/engine/swarm/join-nodes/).

## Forcibly remove a node

In most cases, you should shut down a node before removing it from a swarm with
the `docker node rm` command. If a node becomes unreachable, unresponsive, or
compromised you can forcefully remove the node without shutting it down by
passing the `--force` flag. For instance, if `node9` becomes compromised:

```console
$ docker node rm node9

Error response from daemon: rpc error: code = 9 desc = node node9 is not down and can't be removed

$ docker node rm --force node9

Node node9 removed from swarm
```

Before you forcefully remove a manager node, you must first demote it to the
worker role. Make sure that you always have an odd number of manager nodes if
you demote or remove a manager.

## Back up the swarm

Docker manager nodes store the swarm state and manager logs in the
`/var/lib/docker/swarm/` directory. This data includes the keys used to encrypt
the Raft logs. Without these keys, you cannot restore the swarm.

You can back up the swarm using any manager. Use the following procedure.

1. If the swarm has auto-lock enabled, you need the unlock key
  to restore the swarm from backup. Retrieve the unlock key if necessary and
  store it in a safe location. If you are unsure, read
  [Lock your swarm to protect its encryption key](https://docs.docker.com/engine/swarm/swarm_manager_locking/).
2. Stop Docker on the manager before backing up the data, so that no data is
  being changed during the backup. It is possible to take a backup while the
  manager is running (a "hot" backup), but this is not recommended and your
  results are less predictable when restoring. While the manager is down,
  other nodes continue generating swarm data that is not part of this backup.
  > Note
  >
  > Be sure to maintain the quorum of swarm managers. During the
  > time that a manager is shut down, your swarm is more vulnerable to
  > losing the quorum if further nodes are lost. The number of managers you
  > run is a trade-off. If you regularly take down managers to do backups,
  > consider running a five manager swarm, so that you can lose an additional
  > manager while the backup is running, without disrupting your services.
3. Back up the entire `/var/lib/docker/swarm` directory.
4. Restart the manager.

To restore, see [Restore from a backup](#restore-from-a-backup).

## Recover from disaster

### Restore from a backup

After backing up the swarm as described in
[Back up the swarm](#back-up-the-swarm), use the following procedure to
restore the data to a new swarm.

1. Shut down Docker on the target host machine for the restored swarm.
2. Remove the contents of the `/var/lib/docker/swarm` directory on the new
  swarm.
3. Restore the `/var/lib/docker/swarm` directory with the contents of the
  backup.
  > Note
  >
  > The new node uses the same encryption key for on-disk
  > storage as the old one. It is not possible to change the on-disk storage
  > encryption keys at this time.
  >
  >
  >
  > In the case of a swarm with auto-lock enabled, the unlock key is also the
  > same as on the old swarm, and the unlock key is needed to restore the
  > swarm.
4. Start Docker on the new node. Unlock the swarm if necessary. Re-initialize
  the swarm using the following command, so that this node does not attempt
  to connect to nodes that were part of the old swarm, and presumably no
  longer exist.
  ```console
  $ docker swarm init --force-new-cluster
  ```
5. Verify that the state of the swarm is as expected. This may include
  application-specific tests or simply checking the output of
  `docker service ls` to be sure that all expected services are present.
6. If you use auto-lock,
  [rotate the unlock key](https://docs.docker.com/engine/swarm/swarm_manager_locking/#rotate-the-unlock-key).
7. Add manager and worker nodes to bring your new swarm up to operating
  capacity.
8. Reinstate your previous backup regimen on the new swarm.

### Recover from losing the quorum

Swarm is resilient to failures and can recover from any number
of temporary node failures (machine reboots or crash with restart) or other
transient errors. However, a swarm cannot automatically recover if it loses a
quorum. Tasks on existing worker nodes continue to run, but administrative
tasks are not possible, including scaling or updating services and joining or
removing nodes from the swarm. The best way to recover is to bring the missing
manager nodes back online. If that is not possible, continue reading for some
options for recovering your swarm.

In a swarm of `N` managers, a quorum (a majority) of manager nodes must always
be available. For example, in a swarm with five managers, a minimum of three must be
operational and in communication with each other. In other words, the swarm can
tolerate up to `(N-1)/2` permanent failures beyond which requests involving
swarm management cannot be processed. These types of failures include data
corruption or hardware failures.

If you lose the quorum of managers, you cannot administer the swarm. If you have
lost the quorum and you attempt to perform any management operation on the swarm,
an error occurs:

```text
Error response from daemon: rpc error: code = 4 desc = context deadline exceeded
```

The best way to recover from losing the quorum is to bring the failed nodes back
online. If you can't do that, the only way to recover from this state is to use
the `--force-new-cluster` action from a manager node. This removes all managers
except the manager the command was run from. The quorum is achieved because
there is now only one manager. Promote nodes to be managers until you have the
desired number of managers.

From the node to recover, run:

```console
$ docker swarm init --force-new-cluster --advertise-addr node01:2377
```

When you run the `docker swarm init` command with the `--force-new-cluster`
flag, the Docker Engine where you run the command becomes the manager node of a
single-node swarm which is capable of managing and running services. The manager
has all the previous information about services and tasks, worker nodes are
still part of the swarm, and services are still running. You need to add or
re-add manager nodes to achieve your previous task distribution and ensure that
you have enough managers to maintain high availability and prevent losing the
quorum.

## Force the swarm to rebalance

Generally, you do not need to force the swarm to rebalance its tasks. When you
add a new node to a swarm, or a node reconnects to the swarm after a
period of unavailability, the swarm does not automatically give a workload to
the idle node. This is a design decision. If the swarm periodically shifted tasks
to different nodes for the sake of balance, the clients using those tasks would
be disrupted. The goal is to avoid disrupting running services for the sake of
balance across the swarm. When new tasks start, or when a node with running
tasks becomes unavailable, those tasks are given to less busy nodes. The goal
is eventual balance, with minimal disruption to the end user.

You can use the `--force` or `-f` flag with the `docker service update` command
to force the service to redistribute its tasks across the available worker nodes.
This causes the service tasks to restart. Client applications may be disrupted.
If you have configured it, your service uses a [rolling update](https://docs.docker.com/engine/swarm/swarm-tutorial/rolling-update/).

If you use an earlier version and you want to achieve an even balance of load
across workers and don't mind disrupting running tasks, you can force your swarm
to re-balance by temporarily scaling the service upward. Use
`docker service inspect --pretty <servicename>` to see the configured scale
of a service. When you use `docker service scale`, the nodes with the lowest
number of tasks are targeted to receive the new workloads. There may be multiple
under-loaded nodes in your swarm. You may need to scale the service up by modest
increments a few times to achieve the balance you want across all the nodes.

When the load is balanced to your satisfaction, you can scale the service back
down to the original scale. You can use `docker service ps` to assess the current
balance of your service across nodes.

See also
[docker service scale](https://docs.docker.com/reference/cli/docker/service/scale/) and
[docker service ps](https://docs.docker.com/reference/cli/docker/service/ps/).

---

# Store configuration data using Docker Configs

> How to store configuration data separate from the runtime

# Store configuration data using Docker Configs

   Table of contents

---

## About configs

Docker swarm service configs allow you to store non-sensitive information,
such as configuration files, outside a service's image or running containers.
This allows you to keep your images as generic as possible, without the need to
bind-mount configuration files into the containers or use environment variables.

Configs operate in a similar way to [secrets](https://docs.docker.com/engine/swarm/secrets/), except that they are
not encrypted at rest and are mounted directly into the container's filesystem
without the use of RAM disks. Configs can be added or removed from a service at
any time, and services can share a config. You can even use configs in
conjunction with environment variables or labels, for maximum flexibility.
Config values can be generic strings or binary content (up to 500 kb in size).

> Note
>
> Docker configs are only available to swarm services, not to
> standalone containers. To use this feature, consider adapting your container
> to run as a service with a scale of 1.

Configs are supported on both Linux and Windows services.

### Windows support

Docker includes support for configs on Windows containers, but there are differences
in the implementations, which are called out in the examples below. Keep the
following notable differences in mind:

- Config files with custom targets are not directly bind-mounted into Windows
  containers, since Windows does not support non-directory file bind-mounts.
  Instead, configs for a container are all mounted in
  `C:\ProgramData\Docker\internal\configs` (an implementation detail which
  should not be relied upon by applications) within the container. Symbolic
  links are used to point from there to the desired target of the config within
  the container. The default target is `C:\ProgramData\Docker\configs`.
- When creating a service which uses Windows containers, the options to specify
  UID, GID, and mode are not supported for configs. Configs are currently only
  accessible by administrators and users with `system` access within the
  container.
- On Windows, create or update a service using `--credential-spec` with the
  `config://<config-name>` format. This passes the gMSA credentials file
  directly to nodes before a container starts. No gMSA credentials are written
  to disk on worker nodes. For more information, refer to
  [Deploy services to a swarm](https://docs.docker.com/engine/swarm/services/#gmsa-for-swarm).

## How Docker manages configs

When you add a config to the swarm, Docker sends the config to the swarm manager
over a mutual TLS connection. The config is stored in the Raft log, which is
encrypted. The entire Raft log is replicated across the other managers, ensuring
the same high availability guarantees for configs as for the rest of the swarm
management data.

When you grant a newly-created or running service access to a config, the config
is mounted as a file in the container. The location of the mount point within
the container defaults to `/<config-name>` in Linux containers. In Windows
containers, configs are all mounted into `C:\ProgramData\Docker\configs` and
symbolic links are created to the desired location, which defaults to
`C:\<config-name>`.

You can set the ownership (`uid` and `gid`) for the config, using either the
numerical ID or the name of the user or group. You can also specify the file
permissions (`mode`). These settings are ignored for Windows containers.

- If not set, the config is owned by the user running the container
  command (often `root`) and that user's default group (also often `root`).
- If not set, the config has world-readable permissions (mode `0444`), unless a
  `umask` is set within the container, in which case the mode is impacted by
  that `umask` value.

You can update a service to grant it access to additional configs or revoke its
access to a given config at any time.

A node only has access to configs if the node is a swarm manager or if it is
running service tasks which have been granted access to the config. When a
container task stops running, the configs shared to it are unmounted from the
in-memory filesystem for that container and flushed from the node's memory.

If a node loses connectivity to the swarm while it is running a task container
with access to a config, the task container still has access to its configs, but
cannot receive updates until the node reconnects to the swarm.

You can add or inspect an individual config at any time, or list all
configs. You cannot remove a config that a running service is
using. See [Rotate a config](https://docs.docker.com/engine/swarm/configs/#example-rotate-a-config) for a way to
remove a config without disrupting running services.

To update or roll back configs more easily, consider adding a version
number or date to the config name. This is made easier by the ability to control
the mount point of the config within a given container.

To update a stack, make changes to your Compose file, then re-run `docker stack deploy -c <new-compose-file> <stack-name>`. If you use a new config in
that file, your services start using them. Keep in mind that configurations
are immutable, so you can't change the file for an existing service.
Instead, you create a new config to use a different file

You can run `docker stack rm` to stop the app and take down the stack. This
removes any config that was created by `docker stack deploy` with the same stack
name. This removes *all* configs, including those not referenced by services and
those remaining after a `docker service update --config-rm`.

## Read more aboutdocker configcommands

Use these links to read about specific commands, or continue to the
[example about using configs with a service](#advanced-example-use-configs-with-a-nginx-service).

- [docker config create](https://docs.docker.com/reference/cli/docker/config/create/)
- [docker config inspect](https://docs.docker.com/reference/cli/docker/config/inspect/)
- [docker config ls](https://docs.docker.com/reference/cli/docker/config/ls/)
- [docker config rm](https://docs.docker.com/reference/cli/docker/config/rm/)

## Examples

This section includes graduated examples which illustrate how to use
Docker configs.

> Note
>
> These examples use a single-engine swarm and unscaled services for
> simplicity. The examples use Linux containers, but Windows containers also
> support configs.

### Defining and using configs in compose files

The `docker stack` command supports defining configs in a Compose file.
However, the `configs` key is not supported for `docker compose`. See
[the Compose file reference](https://docs.docker.com/reference/compose-file/legacy-versions/) for details.

### Simple example: Get started with configs

This simple example shows how configs work in just a few commands. For a
real-world example, continue to
[Advanced example: Use configs with a Nginx service](#advanced-example-use-configs-with-a-nginx-service).

1. Add a config to Docker. The `docker config create` command reads standard
  input because the last argument, which represents the file to read the
  config from, is set to `-`.
  ```console
  $ echo "This is a config" | docker config create my-config -
  ```
2. Create a `redis` service and grant it access to the config. By default,
  the container can access the config at `/my-config`, but
  you can customize the file name on the container using the `target` option.
  ```console
  $ docker service create --name redis --config my-config redis:alpine
  ```
3. Verify that the task is running without issues using `docker service ps`. If
  everything is working, the output looks similar to this:
  ```console
  $ docker service ps redis
  ID            NAME     IMAGE         NODE              DESIRED STATE  CURRENT STATE          ERROR  PORTS
  bkna6bpn8r1a  redis.1  redis:alpine  ip-172-31-46-109  Running        Running 8 seconds ago
  ```
4. Get the ID of the `redis` service task container using `docker ps`, so that
  you can use `docker container exec` to connect to the container and read the contents
  of the config data file, which defaults to being readable by all and has the
  same name as the name of the config. The first command below illustrates
  how to find the container ID, and the second and third commands use shell
  completion to do this automatically.
  ```console
  $ docker ps --filter name=redis -q
  5cb1c2348a59
  $ docker container exec $(docker ps --filter name=redis -q) ls -l /my-config
  -r--r--r--    1 root     root            12 Jun  5 20:49 my-config
  $ docker container exec $(docker ps --filter name=redis -q) cat /my-config
  This is a config
  ```
5. Try removing the config. The removal fails because the `redis` service is
  running and has access to the config.
  ```console
  $ docker config ls
  ID                          NAME                CREATED             UPDATED
  fzwcfuqjkvo5foqu7ts7ls578   hello               31 minutes ago      31 minutes ago
  $ docker config rm my-config
  Error response from daemon: rpc error: code = 3 desc = config 'my-config' is
  in use by the following service: redis
  ```
6. Remove access to the config from the running `redis` service by updating the
  service.
  ```console
  $ docker service update --config-rm my-config redis
  ```
7. Repeat steps 3 and 4 again, verifying that the service no longer has access
  to the config. The container ID is different, because the
  `service update` command redeploys the service.
  ```console
  $ docker container exec -it $(docker ps --filter name=redis -q) cat /my-config
  cat: can't open '/my-config': No such file or directory
  ```
8. Stop and remove the service, and remove the config from Docker.
  ```console
  $ docker service rm redis
  $ docker config rm my-config
  ```

### Simple example: Use configs in a Windows service

This is a very simple example which shows how to use configs with a Microsoft
IIS service running on Docker for Windows running Windows containers on
Microsoft Windows 10. It is a naive example that stores the webpage in a config.

This example assumes that you have PowerShell installed.

1. Save the following into a new file `index.html`.
  ```html
  <html lang="en">
    <head><title>Hello Docker</title></head>
    <body>
      <p>Hello Docker! You have deployed a HTML page.</p>
    </body>
  </html>
  ```
2. If you have not already done so, initialize or join the swarm.
  ```powershell
  docker swarm init
  ```
3. Save the `index.html` file as a swarm config named `homepage`.
  ```powershell
  docker config create homepage index.html
  ```
4. Create an IIS service and grant it access to the `homepage` config.
  ```powershell
  docker service create
      --name my-iis
      --publish published=8000,target=8000
      --config src=homepage,target="\inetpub\wwwroot\index.html"
      microsoft/iis:nanoserver
  ```
5. Access the IIS service at `http://localhost:8000/`. It should serve
  the HTML content from the first step.
6. Remove the service and the config.
  ```powershell
  docker service rm my-iis
  docker config rm homepage
  ```

### Example: Use a templated config

To create a configuration in which the content will be generated using a
template engine, use the `--template-driver` parameter and specify the engine
name as its argument. The template will be rendered when container is created.

1. Save the following into a new file `index.html.tmpl`.
  ```html
  <html lang="en">
    <head><title>Hello Docker</title></head>
    <body>
      <p>Hello {{ env "HELLO" }}! I'm service {{ .Service.Name }}.</p>
    </body>
  </html>
  ```
2. Save the `index.html.tmpl` file as a swarm config named `homepage`. Provide
  parameter `--template-driver` and specify `golang` as template engine.
  ```console
  $ docker config create --template-driver golang homepage index.html.tmpl
  ```
3. Create a service that runs Nginx and has access to the environment variable
  HELLO and to the config.
  ```console
  $ docker service create \
       --name hello-template \
       --env HELLO="Docker" \
       --config source=homepage,target=/usr/share/nginx/html/index.html \
       --publish published=3000,target=80 \
       nginx:alpine
  ```
4. Verify that the service is operational: you can reach the Nginx server, and
  that the correct output is being served.
  ```console
  $ curl http://0.0.0.0:3000
  <html lang="en">
    <head><title>Hello Docker</title></head>
    <body>
      <p>Hello Docker! I'm service hello-template.</p>
    </body>
  </html>
  ```

### Advanced example: Use configs with a Nginx service

This example is divided into two parts.
[The first part](#generate-the-site-certificate) is all about generating
the site certificate and does not directly involve Docker configs at all, but
it sets up [the second part](#configure-the-nginx-container), where you store
and use the site certificate as a series of secrets and the Nginx configuration
as a config. The example shows how to set options on the config, such as the
target location within the container and the file permissions (`mode`).

#### Generate the site certificate

Generate a root CA and TLS certificate and key for your site. For production
sites, you may want to use a service such as `Let’s Encrypt` to generate the
TLS certificate and key, but this example uses command-line tools. This step
is a little complicated, but is only a set-up step so that you have
something to store as a Docker secret. If you want to skip these sub-steps,
you can [use Let's Encrypt](https://letsencrypt.org/getting-started/) to
generate the site key and certificate, name the files `site.key` and
`site.crt`, and skip to
[Configure the Nginx container](#configure-the-nginx-container).

1. Generate a root key.
  ```console
  $ openssl genrsa -out "root-ca.key" 4096
  ```
2. Generate a CSR using the root key.
  ```console
  $ openssl req \
            -new -key "root-ca.key" \
            -out "root-ca.csr" -sha256 \
            -subj '/C=US/ST=CA/L=San Francisco/O=Docker/CN=Swarm Secret Example CA'
  ```
3. Configure the root CA. Edit a new file called `root-ca.cnf` and paste
  the following contents into it. This constrains the root CA to only sign
  leaf certificates and not intermediate CAs.
  ```ini
  [root_ca]
  basicConstraints = critical,CA:TRUE,pathlen:1
  keyUsage = critical, nonRepudiation, cRLSign, keyCertSign
  subjectKeyIdentifier=hash
  ```
4. Sign the certificate.
  ```console
  $ openssl x509 -req -days 3650 -in "root-ca.csr" \
                 -signkey "root-ca.key" -sha256 -out "root-ca.crt" \
                 -extfile "root-ca.cnf" -extensions \
                 root_ca
  ```
5. Generate the site key.
  ```console
  $ openssl genrsa -out "site.key" 4096
  ```
6. Generate the site certificate and sign it with the site key.
  ```console
  $ openssl req -new -key "site.key" -out "site.csr" -sha256 \
            -subj '/C=US/ST=CA/L=San Francisco/O=Docker/CN=localhost'
  ```
7. Configure the site certificate. Edit a new file called `site.cnf` and
  paste the following contents into it. This constrains the site
  certificate so that it can only be used to authenticate a server and
  can't be used to sign certificates.
  ```ini
  [server]
  authorityKeyIdentifier=keyid,issuer
  basicConstraints = critical,CA:FALSE
  extendedKeyUsage=serverAuth
  keyUsage = critical, digitalSignature, keyEncipherment
  subjectAltName = DNS:localhost, IP:127.0.0.1
  subjectKeyIdentifier=hash
  ```
8. Sign the site certificate.
  ```console
  $ openssl x509 -req -days 750 -in "site.csr" -sha256 \
      -CA "root-ca.crt" -CAkey "root-ca.key" -CAcreateserial \
      -out "site.crt" -extfile "site.cnf" -extensions server
  ```
9. The `site.csr` and `site.cnf` files are not needed by the Nginx service, but
  you need them if you want to generate a new site certificate. Protect
  the `root-ca.key` file.

#### Configure the Nginx container

1. Produce a very basic Nginx configuration that serves static files over HTTPS.
  The TLS certificate and key are stored as Docker secrets so that they
  can be rotated easily.
  In the current directory, create a new file called `site.conf` with the
  following contents:
  ```nginx
  server {
      listen                443 ssl;
      server_name           localhost;
      ssl_certificate       /run/secrets/site.crt;
      ssl_certificate_key   /run/secrets/site.key;
      location / {
          root   /usr/share/nginx/html;
          index  index.html index.htm;
      }
  }
  ```
2. Create two secrets, representing the key and the certificate. You can store
  any file as a secret as long as it is smaller than 500 KB. This allows you
  to decouple the key and certificate from the services that use them.
  In these examples, the secret name and the file name are the same.
  ```console
  $ docker secret create site.key site.key
  $ docker secret create site.crt site.crt
  ```
3. Save the `site.conf` file in a Docker config. The first parameter is the
  name of the config, and the second parameter is the file to read it from.
  ```console
  $ docker config create site.conf site.conf
  ```
  List the configs:
  ```console
  $ docker config ls
  ID                          NAME                CREATED             UPDATED
  4ory233120ccg7biwvy11gl5z   site.conf           4 seconds ago       4 seconds ago
  ```
4. Create a service that runs Nginx and has access to the two secrets and the
  config. Set the mode to `0440` so that the file is only readable by its
  owner and that owner's group, not the world.
  ```console
  $ docker service create \
       --name nginx \
       --secret site.key \
       --secret site.crt \
       --config source=site.conf,target=/etc/nginx/conf.d/site.conf,mode=0440 \
       --publish published=3000,target=443 \
       nginx:latest \
       sh -c "exec nginx -g 'daemon off;'"
  ```
  Within the running containers, the following three files now exist:
  - `/run/secrets/site.key`
  - `/run/secrets/site.crt`
  - `/etc/nginx/conf.d/site.conf`
5. Verify that the Nginx service is running.
  ```console
  $ docker service ls
  ID            NAME   MODE        REPLICAS  IMAGE
  zeskcec62q24  nginx  replicated  1/1       nginx:latest
  $ docker service ps nginx
  NAME                  IMAGE         NODE  DESIRED STATE  CURRENT STATE          ERROR  PORTS
  nginx.1.9ls3yo9ugcls  nginx:latest  moby  Running        Running 3 minutes ago
  ```
6. Verify that the service is operational: you can reach the Nginx
  server, and that the correct TLS certificate is being used.
  ```console
  $ curl --cacert root-ca.crt https://0.0.0.0:3000
  <!DOCTYPE html>
  <html>
  <head>
  <title>Welcome to nginx!</title>
  <style>
      body {
          width: 35em;
          margin: 0 auto;
          font-family: Tahoma, Verdana, Arial, sans-serif;
      }
  </style>
  </head>
  <body>
  <h1>Welcome to nginx!</h1>
  <p>If you see this page, the nginx web server is successfully installed and
  working. Further configuration is required.</p>
  <p>For online documentation and support, refer to
  <a href="https://nginx.org">nginx.org</a>.<br/>
  Commercial support is available at
  <a href="https://www.nginx.com">www.nginx.com</a>.</p>
  <p><em>Thank you for using nginx.</em></p>
  </body>
  </html>
  ```
  ```console
  $ openssl s_client -connect 0.0.0.0:3000 -CAfile root-ca.crt
  CONNECTED(00000003)
  depth=1 /C=US/ST=CA/L=San Francisco/O=Docker/CN=Swarm Secret Example CA
  verify return:1
  depth=0 /C=US/ST=CA/L=San Francisco/O=Docker/CN=localhost
  verify return:1
  ---
  Certificate chain
   0 s:/C=US/ST=CA/L=San Francisco/O=Docker/CN=localhost
     i:/C=US/ST=CA/L=San Francisco/O=Docker/CN=Swarm Secret Example CA
  ---
  Server certificate
  -----BEGIN CERTIFICATE-----
  …
  -----END CERTIFICATE-----
  subject=/C=US/ST=CA/L=San Francisco/O=Docker/CN=localhost
  issuer=/C=US/ST=CA/L=San Francisco/O=Docker/CN=Swarm Secret Example CA
  ---
  No client certificate CA names sent
  ---
  SSL handshake has read 1663 bytes and written 712 bytes
  ---
  New, TLSv1/SSLv3, Cipher is AES256-SHA
  Server public key is 4096 bit
  Secure Renegotiation IS supported
  Compression: NONE
  Expansion: NONE
  SSL-Session:
      Protocol  : TLSv1
      Cipher    : AES256-SHA
      Session-ID: A1A8BF35549C5715648A12FD7B7E3D861539316B03440187D9DA6C2E48822853
      Session-ID-ctx:
      Master-Key: F39D1B12274BA16D3A906F390A61438221E381952E9E1E05D3DD784F0135FB81353DA38C6D5C021CB926E844DFC49FC4
      Key-Arg   : None
      Start Time: 1481685096
      Timeout   : 300 (sec)
      Verify return code: 0 (ok)
  ```
7. Unless you are going to continue to the next example, clean up after running
  this example by removing the `nginx` service and the stored secrets and
  config.
  ```console
  $ docker service rm nginx
  $ docker secret rm site.crt site.key
  $ docker config rm site.conf
  ```

You have now configured a Nginx service with its configuration decoupled from
its image. You could run multiple sites with exactly the same image but
separate configurations, without the need to build a custom image at all.

### Example: Rotate a config

To rotate a config, you first save a new config with a different name than the
one that is currently in use. You then redeploy the service, removing the old
config and adding the new config at the same mount point within the container.
This example builds upon the previous one by rotating the `site.conf`
configuration file.

1. Edit the `site.conf` file locally. Add `index.php` to the `index` line, and
  save the file.
  ```nginx
  server {
      listen                443 ssl;
      server_name           localhost;
      ssl_certificate       /run/secrets/site.crt;
      ssl_certificate_key   /run/secrets/site.key;
      location / {
          root   /usr/share/nginx/html;
          index  index.html index.htm index.php;
      }
  }
  ```
2. Create a new Docker config using the new `site.conf`, called `site-v2.conf`.
  ```bah
  $ docker config create site-v2.conf site.conf
  ```
3. Update the `nginx` service to use the new config instead of the old one.
  ```console
  $ docker service update \
    --config-rm site.conf \
    --config-add source=site-v2.conf,target=/etc/nginx/conf.d/site.conf,mode=0440 \
    nginx
  ```
4. Verify that the `nginx` service is fully re-deployed, using
  `docker service ps nginx`. When it is, you can remove the old `site.conf`
  config.
  ```console
  $ docker config rm site.conf
  ```
5. To clean up, you can remove the `nginx` service, as well as the secrets and
  configs.
  ```console
  $ docker service rm nginx
  $ docker secret rm site.crt site.key
  $ docker config rm site-v2.conf
  ```

You have now updated your `nginx` service's configuration without the need to
rebuild its image.
