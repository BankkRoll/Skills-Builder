# Troubleshooting and more

# Troubleshooting

> Troubleshooting the Rootless mode

# Troubleshooting

   Table of contents

---

### Distribution-specific hint

- Ubuntu 24.04 and later enables restricted unprivileged user namespaces by
  default, which prevents unprivileged processes in creating user namespaces
  unless an AppArmor profile is configured to allow programs to use
  unprivileged user namespaces.
  If you install `docker-ce-rootless-extras` using the deb package (`apt-get install docker-ce-rootless-extras`), then the AppArmor profile for
  `rootlesskit` is already bundled with the `apparmor` deb package. With this
  installation method, you don't need to add any manual the AppArmor
  configuration. If you install the rootless extras using the [installation
  script](https://get.docker.com/rootless), however, you must add an AppArmor
  profile for `rootlesskit` manually:
  1. Create and install the currently logged-in user's AppArmor profile:
    ```console
    $ filename=$(echo $HOME/bin/rootlesskit | sed -e 's@^/@@' -e 's@/@.@g')
    $ [ ! -z "${filename}" ] && sudo cat <<EOF > /etc/apparmor.d/${filename}
    abi <abi/4.0>,
    include <tunables/global>
    "$HOME/bin/rootlesskit" flags=(unconfined) {
      userns,
      include if exists <local/${filename}>
    }
    EOF
    ```
  2. Restart AppArmor.
    ```console
    $ systemctl restart apparmor.service
    ```

- Add `kernel.unprivileged_userns_clone=1` to `/etc/sysctl.conf` (or
  `/etc/sysctl.d`) and run `sudo sysctl --system`

- `sudo modprobe ip_tables iptable_mangle iptable_nat iptable_filter` is required.
  This might be required on other distributions as well depending on the configuration.
- Known to work on openSUSE 15 and SLES 15.

- For RHEL 8 and similar distributions, installing `fuse-overlayfs` is recommended. Run `sudo dnf install -y fuse-overlayfs`.
  This step is not required on RHEL 9 and similar distributions.
- You might need `sudo dnf install -y iptables`.

## Known limitations

- Only the following storage drivers are supported:
  - `overlay2` (only if running with kernel 5.11 or later)
  - `fuse-overlayfs` (only if running with kernel 4.18 or later, and `fuse-overlayfs` is installed)
  - `btrfs` (only if running with kernel 4.18 or later, or `~/.local/share/docker` is mounted with `user_subvol_rm_allowed` mount option)
  - `vfs`
- cgroup is supported only when running with cgroup v2 and systemd. See [Limiting resources](https://docs.docker.com/engine/security/rootless/tips/#limiting-resources).
- Following features are not supported:
  - AppArmor
  - Checkpoint
  - Overlay network
  - Exposing SCTP ports
- To use the `ping` command, see [Routing ping packets](https://docs.docker.com/engine/security/rootless/tips/#routing-ping-packets).
- To expose privileged TCP/UDP ports (< 1024), see [Exposing privileged ports](https://docs.docker.com/engine/security/rootless/tips/#exposing-privileged-ports).
- `IPAddress` shown in `docker inspect` is namespaced inside RootlessKit's network namespace.
  This means the IP address is not reachable from the host without `nsenter`-ing into the network namespace.
- Host network (`docker run --net=host`) is also namespaced inside RootlessKit.
- NFS mounts as the docker "data-root" is not supported. This limitation is not specific to rootless mode.

## Troubleshooting

### Unable to install with systemd when systemd is present on the system

```console
$ dockerd-rootless-setuptool.sh install
[INFO] systemd not detected, dockerd-rootless.sh needs to be started manually:
...
```

`rootlesskit` cannot detect systemd properly if you switch to your user via `sudo su`. For users which cannot be logged-in, you must use the `machinectl` command which is part of the `systemd-container` package. After installing `systemd-container` switch to `myuser` with the following command:

```console
$ sudo machinectl shell myuser@
```

Where `myuser@` is your desired username and @ signifies this machine.

### Errors when starting the Docker daemon

**[rootlesskit:parent] error: failed to start the child: fork/exec /proc/self/exe: operation not permitted**

This error occurs mostly when the value of `/proc/sys/kernel/unprivileged_userns_clone` is set to 0:

```console
$ cat /proc/sys/kernel/unprivileged_userns_clone
0
```

To fix this issue, add `kernel.unprivileged_userns_clone=1` to
`/etc/sysctl.conf` (or `/etc/sysctl.d`) and run `sudo sysctl --system`.

**[rootlesskit:parent] error: failed to start the child: fork/exec /proc/self/exe: no space left on device**

This error occurs mostly when the value of `/proc/sys/user/max_user_namespaces` is too small:

```console
$ cat /proc/sys/user/max_user_namespaces
0
```

To fix this issue, add `user.max_user_namespaces=28633` to
`/etc/sysctl.conf` (or `/etc/sysctl.d`) and run `sudo sysctl --system`.

**[rootlesskit:parent] error: failed to setup UID/GID map: failed to compute uid/gid map: No subuid ranges found for user 1001 ("testuser")**

This error occurs when `/etc/subuid` and `/etc/subgid` are not configured. See [Prerequisites](https://docs.docker.com/engine/security/rootless/#prerequisites).

**could not get XDG_RUNTIME_DIR**

This error occurs when `$XDG_RUNTIME_DIR` is not set.

On a non-systemd host, you need to create a directory and then set the path:

```console
$ export XDG_RUNTIME_DIR=$HOME/.docker/xrd
$ rm -rf $XDG_RUNTIME_DIR
$ mkdir -p $XDG_RUNTIME_DIR
$ dockerd-rootless.sh
```

> Note
>
> You must remove the directory every time you log out.

On a systemd host, log into the host using `pam_systemd` (see below).
The value is automatically set to `/run/user/$UID` and cleaned up on every logout.

**systemctl --userfails with "Failed to connect to bus: No such file or directory"**

This error occurs mostly when you switch from the root user to a non-root user with `sudo`:

```console
# sudo -iu testuser
$ systemctl --user start docker
Failed to connect to bus: No such file or directory
```

Instead of `sudo -iu <USERNAME>`, you need to log in using `pam_systemd`. For example:

- Log in through the graphic console
- `ssh <USERNAME>@localhost`
- `machinectl shell <USERNAME>@`

**The daemon does not start up automatically**

You need `sudo loginctl enable-linger $(whoami)` to enable the daemon to start
up automatically. See [Advanced Usage](https://docs.docker.com/engine/security/rootless/tips/#advanced-usage).

### docker pullerrors

**docker: failed to register layer: Error processing tar file(exit status 1): lchown <FILE>: invalid argument**

This error occurs when the number of available entries in `/etc/subuid` or
`/etc/subgid` is not sufficient. The number of entries required vary across
images. However, 65,536 entries are sufficient for most images. See
[Prerequisites](https://docs.docker.com/engine/security/rootless/#prerequisites).

**docker: failed to register layer: ApplyLayer exit status 1 stdout: stderr: lchown <FILE>: operation not permitted**

This error occurs mostly when `~/.local/share/docker` is located on NFS.

A workaround is to specify non-NFS `data-root` directory in `~/.config/docker/daemon.json` as follows:

```json
{"data-root":"/somewhere-out-of-nfs"}
```

### docker runerrors

**docker: Error response from daemon: OCI runtime create failed: ...: read unix @->/run/systemd/private: read: connection reset by peer: unknown.**

This error occurs on cgroup v2 hosts mostly when the dbus daemon is not running for the user.

```console
$ systemctl --user is-active dbus
inactive

$ docker run hello-world
docker: Error response from daemon: OCI runtime create failed: container_linux.go:380: starting container process caused: process_linux.go:385: applying cgroup configuration for process caused: error while starting unit "docker
-931c15729b5a968ce803784d04c7421f791d87e5ca1891f34387bb9f694c488e.scope" with properties [{Name:Description Value:"libcontainer container 931c15729b5a968ce803784d04c7421f791d87e5ca1891f34387bb9f694c488e"} {Name:Slice Value:"use
r.slice"} {Name:PIDs Value:@au [4529]} {Name:Delegate Value:true} {Name:MemoryAccounting Value:true} {Name:CPUAccounting Value:true} {Name:IOAccounting Value:true} {Name:TasksAccounting Value:true} {Name:DefaultDependencies Val
ue:false}]: read unix @->/run/systemd/private: read: connection reset by peer: unknown.
```

To fix the issue, run `sudo apt-get install -y dbus-user-session` or `sudo dnf install -y dbus-daemon`, and then relogin.

If the error still occurs, try running `systemctl --user enable --now dbus` (without sudo).

**--cpus,--memory, and--pids-limitare ignored**

This is an expected behavior on cgroup v1 mode.
To use these flags, the host needs to be configured for enabling cgroup v2.
For more information, see [Limiting resources](https://docs.docker.com/engine/security/rootless/tips/#limiting-resources).

### Networking errors

This section provides troubleshooting tips for networking in rootless mode.

Networking in rootless mode is supported via network and port drivers in
RootlessKit. Network performance and characteristics depend on the combination
of network and port driver you use. If you're experiencing unexpected behavior
or performance related to networking, review the following table which shows
the configurations supported by RootlessKit, and how they compare:

| Network driver | Port driver | Net throughput | Port throughput | Source IP propagation | No SUID | Note |
| --- | --- | --- | --- | --- | --- | --- |
| slirp4netns | builtin | Slow | Fast ✅ | ❌ | ✅ | Default in a typical setup |
| vpnkit | builtin | Slow | Fast ✅ | ❌ | ✅ | Default whenslirp4netnsisn't installed |
| slirp4netns | slirp4netns | Slow | Slow | ✅ | ✅ |  |
| pasta | implicit | Slow | Fast ✅ | ✅ | ✅ | Experimental; Needs pasta version 2023_12_04 or later |
| lxc-user-nic | builtin | Fast ✅ | Fast ✅ | ❌ | ❌ | Experimental |
| bypass4netns | bypass4netns | Fast ✅ | Fast ✅ | ✅ | ✅ | Note:Not integrated to RootlessKit as it needs a custom seccomp profile |

For information about troubleshooting specific networking issues, see:

- [docker run -pfails withcannot expose privileged port](#docker-run--p-fails-with-cannot-expose-privileged-port)
- [Ping doesn't work](#ping-doesnt-work)
- [IPAddressshown indocker inspectis unreachable](#ipaddress-shown-in-docker-inspect-is-unreachable)
- [--net=hostdoesn't listen ports on the host network namespace](#--nethost-doesnt-listen-ports-on-the-host-network-namespace)
- [Network is slow](#network-is-slow)
- [docker run -pdoes not propagate source IP addresses](#docker-run--p-does-not-propagate-source-ip-addresses)

#### docker run -pfails withcannot expose privileged port

`docker run -p` fails with this error when a privileged port (< 1024) is specified as the host port.

```console
$ docker run -p 80:80 nginx:alpine
docker: Error response from daemon: driver failed programming external connectivity on endpoint focused_swanson (9e2e139a9d8fc92b37c36edfa6214a6e986fa2028c0cc359812f685173fa6df7): Error starting userland proxy: error while calling PortManager.AddPort(): cannot expose privileged port 80, you might need to add "net.ipv4.ip_unprivileged_port_start=0" (currently 1024) to /etc/sysctl.conf, or set CAP_NET_BIND_SERVICE on rootlesskit binary, or choose a larger port number (>= 1024): listen tcp 0.0.0.0:80: bind: permission denied.
```

When you experience this error, consider using an unprivileged port instead. For example, 8080 instead of 80.

```console
$ docker run -p 8080:80 nginx:alpine
```

To allow exposing privileged ports, see [Exposing privileged ports](https://docs.docker.com/engine/security/rootless/tips/#exposing-privileged-ports).

#### Ping doesn't work

Ping does not work when `/proc/sys/net/ipv4/ping_group_range` is set to `1 0`:

```console
$ cat /proc/sys/net/ipv4/ping_group_range
1       0
```

For details, see [Routing ping packets](https://docs.docker.com/engine/security/rootless/tips/#routing-ping-packets).

#### IPAddressshown indocker inspectis unreachable

This is an expected behavior, as the daemon is namespaced inside RootlessKit's
network namespace. Use `docker run -p` instead.

#### --net=hostdoesn't listen ports on the host network namespace

This is an expected behavior, as the daemon is namespaced inside RootlessKit's
network namespace. Use `docker run -p` instead.

#### Network is slow

Docker with rootless mode uses [slirp4netns](https://github.com/rootless-containers/slirp4netns) as the default network stack if slirp4netns v0.4.0 or later is installed.
If slirp4netns is not installed, Docker falls back to [VPNKit](https://github.com/moby/vpnkit).
Installing slirp4netns may improve the network throughput.

For more information about network drivers for RootlessKit, see
[RootlessKit documentation](https://github.com/rootless-containers/rootlesskit/blob/v2.0.0/docs/network.md).

Also, changing MTU value may improve the throughput.
The MTU value can be specified by creating `~/.config/systemd/user/docker.service.d/override.conf` with the following content:

```systemd
[Service]
Environment="DOCKERD_ROOTLESS_ROOTLESSKIT_MTU=INTEGER"
```

And then restart the daemon:

```console
$ systemctl --user daemon-reload
$ systemctl --user restart docker
```

#### docker run -pdoes not propagate source IP addresses

This is because Docker in rootless mode uses RootlessKit's `builtin` port
driver by default, which doesn't support source IP propagation. To enable
source IP propagation, you can:

- Use the `slirp4netns` RootlessKit port driver
- Use the `pasta` RootlessKit network driver, with the `implicit` port driver

The `pasta` network driver is experimental, but provides improved throughput
performance compared to the `slirp4netns` port driver. The `pasta` driver
requires Docker Engine version 25.0 or later.

To change the RootlessKit networking configuration:

1. Create a file at `~/.config/systemd/user/docker.service.d/override.conf`.
2. Add the following contents, depending on which configuration you would like to use:
  - `slirp4netns`
    ```systemd
    [Service]
    Environment="DOCKERD_ROOTLESS_ROOTLESSKIT_NET=slirp4netns"
    Environment="DOCKERD_ROOTLESS_ROOTLESSKIT_PORT_DRIVER=slirp4netns"
    ```
  - `pasta` network driver with `implicit` port driver
    ```systemd
    [Service]
    Environment="DOCKERD_ROOTLESS_ROOTLESSKIT_NET=pasta"
    Environment="DOCKERD_ROOTLESS_ROOTLESSKIT_PORT_DRIVER=implicit"
    ```
3. Restart the daemon:
  ```console
  $ systemctl --user daemon-reload
  $ systemctl --user restart docker
  ```

For more information about networking options for RootlessKit, see:

- [Network drivers](https://github.com/rootless-containers/rootlesskit/blob/v2.0.0/docs/network.md)
- [Port drivers](https://github.com/rootless-containers/rootlesskit/blob/v2.0.0/docs/port.md)

### Tips for debugging

**Entering intodockerdnamespaces**

The `dockerd-rootless.sh` script executes `dockerd` in its own user, mount, and network namespaces.

For debugging, you can enter the namespaces by running
`nsenter -U --preserve-credentials -n -m -t $(cat $XDG_RUNTIME_DIR/docker.pid)`.

## Uninstall

To remove the systemd service of the Docker daemon, run `dockerd-rootless-setuptool.sh uninstall`:

```console
$ dockerd-rootless-setuptool.sh uninstall
+ systemctl --user stop docker.service
+ systemctl --user disable docker.service
Removed /home/testuser/.config/systemd/user/default.target.wants/docker.service.
[INFO] Uninstalled docker.service
[INFO] This uninstallation tool does NOT remove Docker binaries and data.
[INFO] To remove data, run: `/usr/bin/rootlesskit rm -rf /home/testuser/.local/share/docker`
```

Unset environment variables PATH and DOCKER_HOST if you have added them to `~/.bashrc`.

To remove the data directory, run `rootlesskit rm -rf ~/.local/share/docker`.

To remove the binaries, remove `docker-ce-rootless-extras` package if you installed Docker with package managers.
If you installed Docker with [https://get.docker.com/rootless](https://get.docker.com/rootless) ([Install without packages](https://docs.docker.com/engine/security/rootless/#install)),
remove the binary files under `~/bin`:

```console
$ cd ~/bin
$ rm -f containerd containerd-shim containerd-shim-runc-v2 ctr docker docker-init docker-proxy dockerd dockerd-rootless-setuptool.sh dockerd-rootless.sh rootlesskit rootlesskit-docker-proxy runc vpnkit
```

---

# Rootless mode

> Run the Docker daemon as a non-root user (Rootless mode)

# Rootless mode

   Table of contents

---

Rootless mode lets you run the Docker daemon and containers as a non-root
user to mitigate potential vulnerabilities in the daemon and
the container runtime.

Rootless mode does not require root privileges even during the installation of
the Docker daemon, as long as the [prerequisites](#prerequisites) are met.

## How it works

Rootless mode executes the Docker daemon and containers inside a user namespace.
This is similar to [userns-remapmode](https://docs.docker.com/engine/security/userns-remap/), except that
with `userns-remap` mode, the daemon itself is running with root privileges,
whereas in rootless mode, both the daemon and the container are running without
root privileges.

Rootless mode does not use binaries with `SETUID` bits or file capabilities,
except `newuidmap` and `newgidmap`, which are needed to allow multiple
UIDs/GIDs to be used in the user namespace.

## Prerequisites

- You must install `newuidmap` and `newgidmap` on the host. These commands
  are provided by the `uidmap` package on most distributions.
- `/etc/subuid` and `/etc/subgid` should contain at least 65,536 subordinate
  UIDs/GIDs for the user. In the following example, the user `testuser` has
  65,536 subordinate UIDs/GIDs (231072-296607).

```console
$ id -u
1001
$ whoami
testuser
$ grep ^$(whoami): /etc/subuid
testuser:231072:65536
$ grep ^$(whoami): /etc/subgid
testuser:231072:65536
```

The `dockerd-rootless-setuptool.sh install` script (see following) automatically shows help
when the prerequisites are not satisfied.

## Install

> Note
>
> If the system-wide Docker daemon is already running, consider disabling it:
>
>
>
> ```console
> $ sudo systemctl disable --now docker.service docker.socket
> $ sudo rm /var/run/docker.sock
> ```
>
>
>
> Should you choose not to shut down the `docker` service and socket, you will need to use the `--force`
> parameter in the next section. There are no known issues, but until you shutdown and disable you're
> still running rootful Docker.

If you installed Docker 20.10 or later with
[RPM/DEB packages](https://docs.docker.com/engine/install), you should have `dockerd-rootless-setuptool.sh` in `/usr/bin`.

Run `dockerd-rootless-setuptool.sh install` as a non-root user to set up the daemon:

```console
$ dockerd-rootless-setuptool.sh install
[INFO] Creating /home/testuser/.config/systemd/user/docker.service
...
[INFO] Installed docker.service successfully.
[INFO] To control docker.service, run: `systemctl --user (start|stop|restart) docker.service`
[INFO] To run docker.service on system startup, run: `sudo loginctl enable-linger testuser`

[INFO] Creating CLI context "rootless"
Successfully created context "rootless"
[INFO] Using CLI context "rootless"
Current context is now "rootless"

[INFO] Make sure the following environment variable(s) are set (or add them to ~/.bashrc):
export PATH=/usr/bin:$PATH

[INFO] Some applications may require the following environment variable too:
export DOCKER_HOST=unix:///run/user/1000/docker.sock
```

If `dockerd-rootless-setuptool.sh` is not present, you may need to install the `docker-ce-rootless-extras` package manually, e.g.,

```console
$ sudo apt-get install -y docker-ce-rootless-extras
```

If you do not have permission to run package managers like `apt-get` and `dnf`,
consider using the installation script available at [https://get.docker.com/rootless](https://get.docker.com/rootless).
Since static packages are not available for `s390x`, hence it is not supported for `s390x`.

```console
$ curl -fsSL https://get.docker.com/rootless | sh
...
[INFO] Creating /home/testuser/.config/systemd/user/docker.service
...
[INFO] Installed docker.service successfully.
[INFO] To control docker.service, run: `systemctl --user (start|stop|restart) docker.service`
[INFO] To run docker.service on system startup, run: `sudo loginctl enable-linger testuser`

[INFO] Creating CLI context "rootless"
Successfully created context "rootless"
[INFO] Using CLI context "rootless"
Current context is now "rootless"

[INFO] Make sure the following environment variable(s) are set (or add them to ~/.bashrc):
export PATH=/home/testuser/bin:$PATH

[INFO] Some applications may require the following environment variable too:
export DOCKER_HOST=unix:///run/user/1000/docker.sock
```

The binaries will be installed at `~/bin`.

Run `docker info` to confirm that the `docker` client is connecting to the Rootless daemon:

```console
$ docker info
Client: Docker Engine - Community
 Version:    28.3.3
 Context:    rootless
...
Server:
...
 Security Options:
  seccomp
   Profile: builtin
  rootless
  cgroupns
...
```

See [Troubleshooting](https://docs.docker.com/engine/security/rootless/troubleshoot/) if you faced an error.

---

# Seccomp security profiles for Docker

> Enabling seccomp in Docker

# Seccomp security profiles for Docker

   Table of contents

---

Secure computing mode (`seccomp`) is a Linux kernel feature. You can use it to
restrict the actions available within the container. The `seccomp()` system
call operates on the seccomp state of the calling process. You can use this
feature to restrict your application's access.

This feature is available only if Docker has been built with `seccomp` and the
kernel is configured with `CONFIG_SECCOMP` enabled. To check if your kernel
supports `seccomp`:

```console
$ grep CONFIG_SECCOMP= /boot/config-$(uname -r)
CONFIG_SECCOMP=y
```

## Pass a profile for a container

The [defaultseccompprofile](https://github.com/moby/profiles/blob/main/seccomp/default.json)
provides a sane default for running containers with seccomp and disables around
44 system calls out of 300+. It is moderately protective while providing wide
application compatibility.

In effect, the profile is an allowlist that denies access to system calls by
default and then allows specific system calls. The profile works by defining a
`defaultAction` of `SCMP_ACT_ERRNO` and overriding that action only for specific
system calls. The effect of `SCMP_ACT_ERRNO` is to cause a `Permission Denied`
error. Next, the profile defines a specific list of system calls which are fully
allowed, because their `action` is overridden to be `SCMP_ACT_ALLOW`. Finally,
some specific rules are for individual system calls such as `personality`, and others,
to allow variants of those system calls with specific arguments.

`seccomp` is instrumental for running Docker containers with least privilege. It
is not recommended to change the default `seccomp` profile.

When you run a container, it uses the default profile unless you override it
with the `--security-opt` option. For example, the following explicitly
specifies a policy:

```console
$ docker run --rm \
             -it \
             --security-opt seccomp=/path/to/seccomp/profile.json \
             hello-world
```

### Significant syscalls blocked by the default profile

Docker's default seccomp profile is an allowlist which specifies the calls that
are allowed. The table below lists the significant (but not all) syscalls that
are effectively blocked because they are not on the allowlist. The table includes
the reason each syscall is blocked rather than white-listed.

| Syscall | Description |
| --- | --- |
| acct | Accounting syscall which could let containers disable their own resource limits or process accounting. Also gated byCAP_SYS_PACCT. |
| add_key | Prevent containers from using the kernel keyring, which is not namespaced. |
| bpf | Deny loading potentially persistent BPF programs into kernel, already gated byCAP_SYS_ADMIN. |
| clock_adjtime | Time/date is not namespaced. Also gated byCAP_SYS_TIME. |
| clock_settime | Time/date is not namespaced. Also gated byCAP_SYS_TIME. |
| clone | Deny cloning new namespaces. Also gated byCAP_SYS_ADMINfor CLONE_* flags, exceptCLONE_NEWUSER. |
| create_module | Deny manipulation and functions on kernel modules. Obsolete. Also gated byCAP_SYS_MODULE. |
| delete_module | Deny manipulation and functions on kernel modules. Also gated byCAP_SYS_MODULE. |
| finit_module | Deny manipulation and functions on kernel modules. Also gated byCAP_SYS_MODULE. |
| get_kernel_syms | Deny retrieval of exported kernel and module symbols. Obsolete. |
| get_mempolicy | Syscall that modifies kernel memory and NUMA settings. Already gated byCAP_SYS_NICE. |
| init_module | Deny manipulation and functions on kernel modules. Also gated byCAP_SYS_MODULE. |
| ioperm | Prevent containers from modifying kernel I/O privilege levels. Already gated byCAP_SYS_RAWIO. |
| iopl | Prevent containers from modifying kernel I/O privilege levels. Already gated byCAP_SYS_RAWIO. |
| kcmp | Restrict process inspection capabilities, already blocked by droppingCAP_SYS_PTRACE. |
| kexec_file_load | Sister syscall ofkexec_loadthat does the same thing, slightly different arguments. Also gated byCAP_SYS_BOOT. |
| kexec_load | Deny loading a new kernel for later execution. Also gated byCAP_SYS_BOOT. |
| keyctl | Prevent containers from using the kernel keyring, which is not namespaced. |
| lookup_dcookie | Tracing/profiling syscall, which could leak a lot of information on the host. Also gated byCAP_SYS_ADMIN. |
| mbind | Syscall that modifies kernel memory and NUMA settings. Already gated byCAP_SYS_NICE. |
| mount | Deny mounting, already gated byCAP_SYS_ADMIN. |
| move_pages | Syscall that modifies kernel memory and NUMA settings. |
| nfsservctl | Deny interaction with the kernel NFS daemon. Obsolete since Linux 3.1. |
| open_by_handle_at | Cause of an old container breakout. Also gated byCAP_DAC_READ_SEARCH. |
| perf_event_open | Tracing/profiling syscall, which could leak a lot of information on the host. |
| personality | Prevent container from enabling BSD emulation. Not inherently dangerous, but poorly tested, potential for a lot of kernel vulnerabilities. |
| pivot_root | Denypivot_root, should be privileged operation. |
| process_vm_readv | Restrict process inspection capabilities, already blocked by droppingCAP_SYS_PTRACE. |
| process_vm_writev | Restrict process inspection capabilities, already blocked by droppingCAP_SYS_PTRACE. |
| ptrace | Tracing/profiling syscall. Blocked in Linux kernel versions before 4.8 to avoid seccomp bypass. Tracing/profiling arbitrary processes is already blocked by droppingCAP_SYS_PTRACE, because it could leak a lot of information on the host. |
| query_module | Deny manipulation and functions on kernel modules. Obsolete. |
| quotactl | Quota syscall which could let containers disable their own resource limits or process accounting. Also gated byCAP_SYS_ADMIN. |
| reboot | Don't let containers reboot the host. Also gated byCAP_SYS_BOOT. |
| request_key | Prevent containers from using the kernel keyring, which is not namespaced. |
| set_mempolicy | Syscall that modifies kernel memory and NUMA settings. Already gated byCAP_SYS_NICE. |
| setns | Deny associating a thread with a namespace. Also gated byCAP_SYS_ADMIN. |
| settimeofday | Time/date is not namespaced. Also gated byCAP_SYS_TIME. |
| stime | Time/date is not namespaced. Also gated byCAP_SYS_TIME. |
| swapon | Deny start/stop swapping to file/device. Also gated byCAP_SYS_ADMIN. |
| swapoff | Deny start/stop swapping to file/device. Also gated byCAP_SYS_ADMIN. |
| sysfs | Obsolete syscall. |
| _sysctl | Obsolete, replaced by /proc/sys. |
| umount | Should be a privileged operation. Also gated byCAP_SYS_ADMIN. |
| umount2 | Should be a privileged operation. Also gated byCAP_SYS_ADMIN. |
| unshare | Deny cloning new namespaces for processes. Also gated byCAP_SYS_ADMIN, with the exception ofunshare --user. |
| uselib | Older syscall related to shared libraries, unused for a long time. |
| userfaultfd | Userspace page fault handling, largely needed for process migration. |
| ustat | Obsolete syscall. |
| vm86 | In kernel x86 real mode virtual machine. Also gated byCAP_SYS_ADMIN. |
| vm86old | In kernel x86 real mode virtual machine. Also gated byCAP_SYS_ADMIN. |

## Run without the default seccomp profile

You can pass `unconfined` to run a container without the default seccomp
profile.

```console
$ docker run --rm -it --security-opt seccomp=unconfined debian:latest \
    unshare --map-root-user --user sh -c whoami
```

---

# Deploy Notary Server with Compose

> Deploying Notary

# Deploy Notary Server with Compose

   Table of contents

---

The easiest way to deploy Notary Server is by using Docker Compose. To follow the procedure on this page, you must have already
[installed Docker Compose](https://docs.docker.com/compose/install/).

1. Clone the Notary repository.
  ```console
  $ git clone https://github.com/theupdateframework/notary.git
  ```
2. Build and start Notary Server with the sample certificates.
  ```console
  $ docker compose up -d
  ```
  For more detailed documentation about how to deploy Notary Server, see the [instructions to run a Notary service](https://github.com/theupdateframework/notary/blob/master/docs/running_a_service.md) as well as [the Notary repository](https://github.com/theupdateframework/notary) for more information.
3. Make sure that your Docker or Notary client trusts Notary Server's certificate before you try to interact with the Notary server.

See the instructions for
[Docker](https://docs.docker.com/reference/cli/docker/#notary) or
for [Notary](https://github.com/docker/notary#using-notary) depending on which one you are using.

## If you want to use Notary in production

Check back here for instructions after Notary Server has an official
stable release. To get a head start on deploying Notary in production, see
[the Notary repository](https://github.com/theupdateframework/notary).

---

# Automation with content trust

> Automating content push pulls with trust

# Automation with content trust

   Table of contents

---

It is very common for Docker Content Trust to be built into existing automation
systems. To allow tools to wrap Docker and push trusted content, there are
environment variables that can be passed through to the client.

This guide follows the steps as described in
[Signing images with Docker Content Trust](https://docs.docker.com/engine/security/trust/#signing-images-with-docker-content-trust). Make sure you understand and follow the prerequisites.

When working directly with the Notary client, it uses its [own set of environment variables](https://github.com/theupdateframework/notary/blob/master/docs/reference/client-config.md#environment-variables-optional).

## Add a delegation private key

To automate importing a delegation private key to the local Docker trust store, we
need to pass a passphrase for the new key. This passphrase will be required
everytime that delegation signs a tag.

```console
$ export DOCKER_CONTENT_TRUST_REPOSITORY_PASSPHRASE="mypassphrase123"

$ docker trust key load delegation.key --name jeff
Loading key from "delegation.key"...
Successfully imported key from delegation.key
```

## Add a delegation public key

If you initialize a repository at the same time as adding a delegation
public key, then you will need to use the local Notary Canonical Root Key's
passphrase to create the repositories trust data. If the repository has already
been initiated then you only need the repositories passphrase.

```console
# Export the Local Root Key Passphrase if required.
$ export DOCKER_CONTENT_TRUST_ROOT_PASSPHRASE="rootpassphrase123"

# Export the Repository Passphrase
$ export DOCKER_CONTENT_TRUST_REPOSITORY_PASSPHRASE="repopassphrase123"

# Initialize Repo and Push Delegation
$ docker trust signer add --key delegation.crt jeff registry.example.com/admin/demo
Adding signer "jeff" to registry.example.com/admin/demo...
Initializing signed repository for registry.example.com/admin/demo...
Successfully initialized "registry.example.com/admin/demo"
Successfully added signer: registry.example.com/admin/demo
```

## Sign an image

Finally when signing an image, we will need to export the passphrase of the
signing key. This was created when the key was loaded into the local Docker
trust store with `$ docker trust key load`.

```console
$ export DOCKER_CONTENT_TRUST_REPOSITORY_PASSPHRASE="mypassphrase123"

$ docker trust sign registry.example.com/admin/demo:1
Signing and pushing trust data for local image registry.example.com/admin/demo:1, may overwrite remote trust data
The push refers to repository [registry.example.com/admin/demo]
428c97da766c: Layer already exists
2: digest: sha256:1a6fd470b9ce10849be79e99529a88371dff60c60aab424c077007f6979b4812 size: 524
Signing and pushing trust metadata
Successfully signed registry.example.com/admin/demo:1
```

## Build with content trust

You can also build with content trust. Before running the `docker build` command,
you should set the environment variable `DOCKER_CONTENT_TRUST` either manually or
in a scripted fashion. Consider the simple Dockerfile below.

```dockerfile
# syntax=docker/dockerfile:1
FROM docker/trusttest:latest
RUN echo
```

The `FROM` tag is pulling a signed image. You cannot build an image that has a
`FROM` that is not either present locally or signed. Given that content trust
data exists for the tag `latest`, the following build should succeed:

```console
$  docker build -t docker/trusttest:testing .
Using default tag: latest
latest: Pulling from docker/trusttest

b3dbab3810fc: Pull complete
a9539b34a6ab: Pull complete
Digest: sha256:d149ab53f871
```

If content trust is enabled, building from a Dockerfile that relies on tag
without trust data, causes the build command to fail:

```console
$  docker build -t docker/trusttest:testing .
unable to process Dockerfile: No trust data for notrust
```

## Related information

- [Delegations for content trust](https://docs.docker.com/engine/security/trust/trust_delegation/)
- [Content trust in Docker](https://docs.docker.com/engine/security/trust/)
- [Manage keys for content trust](https://docs.docker.com/engine/security/trust/trust_key_mng/)
- [Play in a content trust sandbox](https://docs.docker.com/engine/security/trust/trust_sandbox/)
