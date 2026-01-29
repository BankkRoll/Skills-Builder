# Isolate containers with a user namespace and more

# Isolate containers with a user namespace

> Isolate containers within a user namespace

# Isolate containers with a user namespace

   Table of contents

---

Linux namespaces provide isolation for running processes, limiting their access
to system resources without the running process being aware of the limitations.
For more information on Linux namespaces, see
[Linux namespaces](https://www.linux.com/news/understanding-and-securing-linux-namespaces).

The best way to prevent privilege-escalation attacks from within a container is
to configure your container's applications to run as unprivileged users. For
containers whose processes must run as the `root` user within the container, you
can re-map this user to a less-privileged user on the Docker host. The mapped
user is assigned a range of UIDs which function within the namespace as normal
UIDs from 0 to 65536, but have no privileges on the host machine itself.

## About remapping and subordinate user and group IDs

The remapping itself is handled by two files: `/etc/subuid` and `/etc/subgid`.
Each file works the same, but one is concerned with the user ID range, and the
other with the group ID range. Consider the following entry in `/etc/subuid`:

```text
testuser:231072:65536
```

This means that `testuser` is assigned a subordinate user ID range of `231072`
and the next 65536 integers in sequence. UID `231072` is mapped within the
namespace (within the container, in this case) as UID `0` (`root`). UID `231073`
is mapped as UID `1`, and so forth. If a process attempts to escalate privilege
outside of the namespace, the process is running as an unprivileged high-number
UID on the host, which does not even map to a real user. This means the process
has no privileges on the host system at all.

> Note
>
> It is possible to assign multiple subordinate ranges for a given user or group
> by adding multiple non-overlapping mappings for the same user or group in the
> `/etc/subuid` or `/etc/subgid` file. In this case, Docker uses only the first
> five mappings, in accordance with the kernel's limitation of only five entries
> in `/proc/self/uid_map` and `/proc/self/gid_map`.

When you configure Docker to use the `userns-remap` feature, you can optionally
specify an existing user and/or group, or you can specify `default`. If you
specify `default`, a user and group `dockremap` is created and used for this
purpose.

> Warning
>
> Some distributions do not automatically add the new group to the
> `/etc/subuid` and `/etc/subgid` files. If that's the case, you may have
> to manually edit these files and assign non-overlapping ranges. This step is
> covered in [Prerequisites](#prerequisites).

It is very important that the ranges do not overlap, so that a process cannot gain
access in a different namespace. On most Linux distributions, system utilities
manage the ranges for you when you add or remove users.

This re-mapping is transparent to the container, but introduces some
configuration complexity in situations where the container needs access to
resources on the Docker host, such as bind mounts into areas of the filesystem
that the system user cannot write to. From a security standpoint, it is best to
avoid these situations.

## Prerequisites

1. The subordinate UID and GID ranges must be associated with an existing user,
  even though the association is an implementation detail. The user owns
  the namespaced storage directories under `/var/lib/docker/`. If you don't
  want to use an existing user, Docker can create one for you and use that. If
  you want to use an existing username or user ID, it must already exist.
  Typically, this means that the relevant entries need to be in
  `/etc/passwd` and `/etc/group`, but if you are using a different
  authentication back-end, this requirement may translate differently.
  To verify this, use the `id` command:
  ```console
  $ id testuser
  uid=1001(testuser) gid=1001(testuser) groups=1001(testuser)
  ```
2. The way the namespace remapping is handled on the host is using two files,
  `/etc/subuid` and `/etc/subgid`. These files are typically managed
  automatically when you add or remove users or groups, but on some
  distributions, you may need to manage these files manually.
  Each file contains three fields: the username or ID of the user, followed by
  a beginning UID or GID (which is treated as UID or GID 0 within the namespace)
  and a maximum number of UIDs or GIDs available to the user. For instance,
  given the following entry:
  ```text
  testuser:231072:65536
  ```
  This means that user-namespaced processes started by `testuser` are
  owned by host UID `231072` (which looks like UID `0` inside the
  namespace) through 296607 (231072 + 65536 - 1). These ranges should not overlap,
  to ensure that namespaced processes cannot access each other's namespaces.
  After adding your user, check `/etc/subuid` and `/etc/subgid` to see if your
  user has an entry in each. If not, you need to add it, being careful to
  avoid overlap.
  If you want to use the `dockremap` user automatically created by Docker,
  check for the `dockremap` entry in these files after
  configuring and restarting Docker.
3. If there are any locations on the Docker host where the unprivileged
  user needs to write, adjust the permissions of those locations
  accordingly. This is also true if you want to use the `dockremap` user
  automatically created by Docker, but you can't modify the
  permissions until after configuring and restarting Docker.
4. Enabling `userns-remap` effectively masks existing image and container
  layers, as well as other Docker objects within `/var/lib/docker/`. This is
  because Docker needs to adjust the ownership of these resources and actually
  stores them in a subdirectory within `/var/lib/docker/`. It is best to enable
  this feature on a new Docker installation rather than an existing one.
  Along the same lines, if you disable `userns-remap` you can't access any
  of the resources created while it was enabled.
5. Check the [limitations](#user-namespace-known-limitations) on user
  namespaces to be sure your use case is possible.

## Enable userns-remap on the daemon

You can start `dockerd` with the `--userns-remap` flag or follow this
procedure to configure the daemon using the `daemon.json` configuration file.
The `daemon.json` method is recommended. If you use the flag, use the following
command as a model:

```console
$ dockerd --userns-remap="testuser:testuser"
```

1. Edit `/etc/docker/daemon.json`. Assuming the file was previously empty, the
  following entry enables `userns-remap` using user and group called
  `testuser`. You can address the user and group by ID or name. You only need to
  specify the group name or ID if it is different from the user name or ID. If
  you provide both the user and group name or ID, separate them by a colon
  (`:`) character. The following formats all work for the value, assuming
  the UID and GID of `testuser` are `1001`:
  - `testuser`
  - `testuser:testuser`
  - `1001`
  - `1001:1001`
  - `testuser:1001`
  - `1001:testuser`
  ```json
  {
    "userns-remap": "testuser"
  }
  ```
  > Note
  >
  > To use the `dockremap` user and have Docker create it for you,
  > set the value to `default` rather than `testuser`.
  Save the file and restart Docker.
2. If you are using the `dockremap` user, verify that Docker created it using
  the `id` command.
  ```console
  $ id dockremap
  uid=112(dockremap) gid=116(dockremap) groups=116(dockremap)
  ```
  Verify that the entry has been added to `/etc/subuid` and `/etc/subgid`:
  ```console
  $ grep dockremap /etc/subuid
  dockremap:231072:65536
  $ grep dockremap /etc/subgid
  dockremap:231072:65536
  ```
  If these entries are not present, edit the files as the `root` user and
  assign a starting UID and GID that is the highest-assigned one plus the
  offset (in this case, `65536`). Be careful not to allow any overlap in the
  ranges.
3. Verify that previous images are not available using the `docker image ls`
  command. The output should be empty.
4. Start a container from the `hello-world` image.
  ```console
  $ docker run hello-world
  ```
5. Verify that a namespaced directory exists within `/var/lib/docker/` named
  with the UID and GID of the namespaced user, owned by that UID and GID,
  and not group-or-world-readable. Some of the subdirectories are still
  owned by `root` and have different permissions.
  ```console
  $ sudo ls -ld /var/lib/docker/231072.231072/
  drwx------ 11 231072 231072 11 Jun 21 21:19 /var/lib/docker/231072.231072/
  $ sudo ls -l /var/lib/docker/231072.231072/
  total 14
  drwx------ 5 231072 231072 5 Jun 21 21:19 aufs
  drwx------ 3 231072 231072 3 Jun 21 21:21 containers
  drwx------ 3 root   root   3 Jun 21 21:19 image
  drwxr-x--- 3 root   root   3 Jun 21 21:19 network
  drwx------ 4 root   root   4 Jun 21 21:19 plugins
  drwx------ 2 root   root   2 Jun 21 21:19 swarm
  drwx------ 2 231072 231072 2 Jun 21 21:21 tmp
  drwx------ 2 root   root   2 Jun 21 21:19 trust
  drwx------ 2 231072 231072 3 Jun 21 21:19 volumes
  ```
  Your directory listing may have some differences, especially if you
  use a different container storage driver than `aufs`.
  The directories which are owned by the remapped user are used instead
  of the same directories directly beneath `/var/lib/docker/` and the
  unused versions (such as `/var/lib/docker/tmp/` in the example here)
  can be removed. Docker does not use them while `userns-remap` is
  enabled.

## Disable namespace remapping for a container

If you enable user namespaces on the daemon, all containers are started with
user namespaces enabled by default. In some situations, such as privileged
containers, you may need to disable user namespaces for a specific container.
See
[user namespace known limitations](#user-namespace-known-limitations)
for some of these limitations.

To disable user namespaces for a specific container, add the `--userns=host`
flag to the `docker container create`, `docker container run`, or `docker container exec` command.

There is a side effect when using this flag: user remapping will not be enabled for that container but, because the read-only (image) layers are shared between containers, ownership of the containers filesystem will still be remapped.

What this means is that the whole container filesystem will belong to the user specified in the `--userns-remap` daemon config (`231072` in the example above). This can lead to unexpected behavior of programs inside the container. For instance `sudo` (which checks that its binaries belong to user `0`) or binaries with a `setuid` flag.

## User namespace known limitations

The following standard Docker features are incompatible with running a Docker
daemon with user namespaces enabled:

- Sharing PID or NET namespaces with the host (`--pid=host` or `--network=host`).
- External (volume or storage) drivers which are unaware or incapable of using
  daemon user mappings.
- Using the `--privileged` mode flag on `docker run` without also specifying
  `--userns=host`.

User namespaces are an advanced feature and require coordination with other
capabilities. For example, if volumes are mounted from the host, file ownership
must be pre-arranged if you need read or write access to the volume contents.

While the root user inside a user-namespaced container process has many of the
expected privileges of the superuser within the container, the Linux kernel
imposes restrictions based on internal knowledge that this is a user-namespaced
process. One notable restriction is the inability to use the `mknod` command.
Permission is denied for device creation within the container when run by
the `root` user.

---

# Docker Engine security

> Review of the Docker Daemon attack surface

# Docker Engine security

   Table of contents

---

There are four major areas to consider when reviewing Docker security:

- The intrinsic security of the kernel and its support for
  namespaces and cgroups
- The attack surface of the Docker daemon itself
- Loopholes in the container configuration profile, either by default,
  or when customized by users.
- The "hardening" security features of the kernel and how they
  interact with containers.

## Kernel namespaces

Docker containers are very similar to LXC containers, and they have
similar security features. When you start a container with
`docker run`, behind the scenes Docker creates a set of namespaces and control
groups for the container.

Namespaces provide the first and most straightforward form of
isolation. Processes running within a container cannot see, and even
less affect, processes running in another container, or in the host
system.

Each container also gets its own network stack, meaning that a
container doesn't get privileged access to the sockets or interfaces
of another container. Of course, if the host system is setup
accordingly, containers can interact with each other through their
respective network interfaces — just like they can interact with
external hosts. When you specify public ports for your containers or use
[links](https://docs.docker.com/engine/network/links/)
then IP traffic is allowed between containers. They can ping each other,
send/receive UDP packets, and establish TCP connections, but that can be
restricted if necessary. From a network architecture point of view, all
containers on a given Docker host are sitting on bridge interfaces. This
means that they are just like physical machines connected through a
common Ethernet switch; no more, no less.

How mature is the code providing kernel namespaces and private
networking? Kernel namespaces were introduced [between kernel version
2.6.15 and
2.6.26](https://man7.org/linux/man-pages/man7/namespaces.7.html).
This means that since July 2008 (date of the 2.6.26 release
), namespace code has been exercised and scrutinized on a large
number of production systems. And there is more: the design and
inspiration for the namespaces code are even older. Namespaces are
actually an effort to reimplement the features of [OpenVZ](https://en.wikipedia.org/wiki/OpenVZ) in such a way that they could be
merged within the mainstream kernel. And OpenVZ was initially released
in 2005, so both the design and the implementation are pretty mature.

## Control groups

Control Groups are another key component of Linux containers. They
implement resource accounting and limiting. They provide many
useful metrics, but they also help ensure that each container gets
its fair share of memory, CPU, disk I/O; and, more importantly, that a
single container cannot bring the system down by exhausting one of those
resources.

So while they do not play a role in preventing one container from
accessing or affecting the data and processes of another container, they
are essential to fend off some denial-of-service attacks. They are
particularly important on multi-tenant platforms, like public and
private PaaS, to guarantee a consistent uptime (and performance) even
when some applications start to misbehave.

Control Groups have been around for a while as well: the code was
started in 2006, and initially merged in kernel 2.6.24.

## Docker daemon attack surface

Running containers (and applications) with Docker implies running the
Docker daemon. This daemon requires `root` privileges unless you opt-in
to [Rootless mode](https://docs.docker.com/engine/security/rootless/), and you should therefore be aware of
some important details.

First of all, only trusted users should be allowed to control your
Docker daemon. This is a direct consequence of some powerful Docker
features. Specifically, Docker allows you to share a directory between
the Docker host and a guest container; and it allows you to do so
without limiting the access rights of the container. This means that you
can start a container where the `/host` directory is the `/` directory
on your host; and the container can alter your host filesystem
without any restriction. This is similar to how virtualization systems
allow filesystem resource sharing. Nothing prevents you from sharing your
root filesystem (or even your root block device) with a virtual machine.

This has a strong security implication: for example, if you instrument Docker
from a web server to provision containers through an API, you should be
even more careful than usual with parameter checking, to make sure that
a malicious user cannot pass crafted parameters causing Docker to create
arbitrary containers.

For this reason, the REST API endpoint (used by the Docker CLI to
communicate with the Docker daemon) changed in Docker 0.5.2, and now
uses a Unix socket instead of a TCP socket bound on 127.0.0.1 (the
latter being prone to cross-site request forgery attacks if you happen to run
Docker directly on your local machine, outside of a VM). You can then
use traditional Unix permission checks to limit access to the control
socket.

You can also expose the REST API over HTTP if you explicitly decide to do so.
However, if you do that, be aware of the above mentioned security implications.
Note that even if you have a firewall to limit accesses to the REST API
endpoint from other hosts in the network, the endpoint can be still accessible
from containers, and it can easily result in the privilege escalation.
Therefore it is *mandatory* to secure API endpoints with
[HTTPS and certificates](https://docs.docker.com/engine/security/protect-access/).
Exposing the daemon API over HTTP without TLS is not permitted,
and such a configuration causes the daemon to fail early on startup, see
[Unauthenticated TCP connections](https://docs.docker.com/engine/deprecated/#unauthenticated-tcp-connections).
It is also recommended to ensure that it is reachable only from a trusted
network or VPN.

You can also use `DOCKER_HOST=ssh://USER@HOST` or `ssh -L /path/to/docker.sock:/var/run/docker.sock`
instead if you prefer SSH over TLS.

The daemon is also potentially vulnerable to other inputs, such as image
loading from either disk with `docker load`, or from the network with
`docker pull`. As of Docker 1.3.2, images are now extracted in a chrooted
subprocess on Linux/Unix platforms, being the first-step in a wider effort
toward privilege separation. As of Docker 1.10.0, all images are stored and
accessed by the cryptographic checksums of their contents, limiting the
possibility of an attacker causing a collision with an existing image.

Finally, if you run Docker on a server, it is recommended to run
exclusively Docker on the server, and move all other services within
containers controlled by Docker. Of course, it is fine to keep your
favorite admin tools (probably at least an SSH server), as well as
existing monitoring/supervision processes, such as NRPE and collectd.

## Linux kernel capabilities

By default, Docker starts containers with a restricted set of
capabilities. What does that mean?

Capabilities turn the binary "root/non-root" dichotomy into a
fine-grained access control system. Processes (like web servers) that
just need to bind on a port below 1024 do not need to run as root: they
can just be granted the `net_bind_service` capability instead. And there
are many other capabilities, for almost all the specific areas where root
privileges are usually needed. This means a lot for container security.

Typical servers run several processes as `root`, including the SSH daemon,
`cron` daemon, logging daemons, kernel modules, network configuration tools,
and more. A container is different, because almost all of those tasks are
handled by the infrastructure around the container:

- SSH access are typically managed by a single server running on
  the Docker host
- `cron`, when necessary, should run as a user
  process, dedicated and tailored for the app that needs its
  scheduling service, rather than as a platform-wide facility
- Log management is also typically handed to Docker, or to
  third-party services like Loggly or Splunk
- Hardware management is irrelevant, meaning that you never need to
  run `udevd` or equivalent daemons within
  containers
- Network management happens outside of the containers, enforcing
  separation of concerns as much as possible, meaning that a container
  should never need to perform `ifconfig`,
  `route`, or ip commands (except when a container
  is specifically engineered to behave like a router or firewall, of
  course)

This means that in most cases, containers do not need "real" root
privileges at all* And therefore, containers can run with a reduced
capability set; meaning that "root" within a container has much less
privileges than the real "root". For instance, it is possible to:

- Deny all "mount" operations
- Deny access to raw sockets (to prevent packet spoofing)
- Deny access to some filesystem operations, like creating new device
  nodes, changing the owner of files, or altering attributes (including
  the immutable flag)
- Deny module loading

This means that even if an intruder manages to escalate to root within a
container, it is much harder to do serious damage, or to escalate
to the host.

This doesn't affect regular web apps, but reduces the vectors of attack by
malicious users considerably. By default Docker
drops all capabilities except [those
needed](https://github.com/moby/moby/blob/master/daemon/pkg/oci/caps/defaults.go#L6-L19),
an allowlist instead of a denylist approach. You can see a full list of
available capabilities in [Linux
manpages](https://man7.org/linux/man-pages/man7/capabilities.7.html).

One primary risk with running Docker containers is that the default set
of capabilities and mounts given to a container may provide incomplete
isolation, either independently, or when used in combination with
kernel vulnerabilities.

Docker supports the addition and removal of capabilities, allowing use
of a non-default profile. This may make Docker more secure through
capability removal, or less secure through the addition of capabilities.
The best practice for users would be to remove all capabilities except
those explicitly required for their processes.

## Docker Content Trust signature verification

Docker Engine can be configured to only run signed images. The Docker Content
Trust signature verification feature is built directly into the `dockerd` binary.
This is configured in the Dockerd configuration file.

To enable this feature, trustpinning can be configured in `daemon.json`, whereby
only repositories signed with a user-specified root key can be pulled and run.

This feature provides more insight to administrators than previously available with
the CLI for enforcing and performing image signature verification.

For more information on configuring Docker Content Trust Signature Verification, go to
[Content trust in Docker](https://docs.docker.com/engine/security/trust/).

## Other kernel security features

Capabilities are just one of the many security features provided by
modern Linux kernels. It is also possible to leverage existing,
well-known systems like TOMOYO, AppArmor, SELinux, GRSEC, etc. with
Docker.

While Docker currently only enables capabilities, it doesn't interfere
with the other systems. This means that there are many different ways to
harden a Docker host. Here are a few examples.

- You can run a kernel with GRSEC and PAX. This adds many safety
  checks, both at compile-time and run-time; it also defeats many
  exploits, thanks to techniques like address randomization. It doesn't
  require Docker-specific configuration, since those security features
  apply system-wide, independent of containers.
- If your distribution comes with security model templates for
  Docker containers, you can use them out of the box. For instance, we
  ship a template that works with AppArmor and Red Hat comes with SELinux
  policies for Docker. These templates provide an extra safety net (even
  though it overlaps greatly with capabilities).
- You can define your own policies using your favorite access control
  mechanism.

Just as you can use third-party tools to augment Docker containers, including
special network topologies or shared filesystems, tools exist to harden Docker
containers without the need to modify Docker itself.

As of Docker 1.10 User Namespaces are supported directly by the docker
daemon. This feature allows for the root user in a container to be mapped
to a non uid-0 user outside the container, which can help to mitigate the
risks of container breakout. This facility is available but not enabled
by default.

Refer to the
[daemon command](https://docs.docker.com/reference/cli/dockerd/#daemon-user-namespace-options)
in the command line reference for more information on this feature.
Additional information on the implementation of User Namespaces in Docker
can be found in
[this blog post](https://integratedcode.us/2015/10/13/user-namespaces-have-arrived-in-docker/).

## Conclusions

Docker containers are, by default, quite secure; especially if you
run your processes as non-privileged users inside the container.

You can add an extra layer of safety by enabling AppArmor, SELinux,
GRSEC, or another appropriate hardening system.

If you think of ways to make docker more secure, we welcome feature requests,
pull requests, or comments on the Docker community forums.

## Related information

- [Use trusted images](https://docs.docker.com/engine/security/trust/)
- [Seccomp security profiles for Docker](https://docs.docker.com/engine/security/seccomp/)
- [AppArmor security profiles for Docker](https://docs.docker.com/engine/security/apparmor/)
- [On the Security of Containers (2014)](https://medium.com/@ewindisch/on-the-security-of-containers-2c60ffe25a9e)
- [Docker swarm mode overlay network security model](https://docs.docker.com/engine/network/drivers/overlay/)
