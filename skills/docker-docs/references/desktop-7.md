# General FAQs for Desktop and more

# General FAQs for Desktop

> Frequently asked Docker Desktop questions for all platforms

# General FAQs for Desktop

   Table of contents

---

### Can I use Docker Desktop offline?

Yes, you can use Docker Desktop offline. However, you
cannot access features that require an active internet
connection. Additionally, any functionality that requires you to sign in won't work while using Docker Desktop offline or in air-gapped environments.
This includes:

- The resources in the
  [Learning Center](https://docs.docker.com/desktop/use-desktop/)
- Pulling or pushing an image to Docker Hub
- [Image Access Management](https://docs.docker.com/security/access-tokens/)
- [Static vulnerability scanning](https://docs.docker.com/docker-hub/repos/manage/vulnerability-scanning/)
- Viewing remote images in the Docker Dashboard
- Docker Build when using
  [BuildKit](https://docs.docker.com/build/buildkit/#getting-started).
  You can work around this by disabling BuildKit. Run `DOCKER_BUILDKIT=0 docker build .` to disable BuildKit.
- [Kubernetes](https://docs.docker.com/desktop/use-desktop/kubernetes/) (Images are download when you enable Kubernetes for the first time)
- Checking for updates
- [In-app diagnostics](https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/#diagnose-from-the-app) (including the
  [Self-diagnose tool](https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/#diagnose-from-the-app))
- Sending usage statistics
- When `networkMode` is set to `mirrored`

### How do I connect to the remote Docker Engine API?

To connect to the remote Engine API, you might need to provide the location of the Engine API for Docker clients and development tools.

Mac and Windows WSL 2 users can connect to the Docker Engine through a Unix socket: `unix:///var/run/docker.sock`.

If you are working with applications like [Apache Maven](https://maven.apache.org/)
that expect settings for `DOCKER_HOST` and `DOCKER_CERT_PATH` environment
variables, specify these to connect to Docker instances through Unix sockets.

For example:

```console
$ export DOCKER_HOST=unix:///var/run/docker.sock
```

Docker Desktop Windows users can connect to the Docker Engine through a **named pipe**: `npipe:////./pipe/docker_engine`, or **TCP socket** at this URL:
`tcp://localhost:2375`.

For details, see
[Docker Engine API](https://docs.docker.com/reference/api/engine/).

### How do I connect from a container to a service on the host?

The host has a changing IP address, or none if you have no network access.
It is recommend that you connect to the special DNS name `host.docker.internal`,
which resolves to the internal IP address used by the host.

For more information and examples, see
[how to connect from a container to a service on the host](https://docs.docker.com/desktop/features/networking/#connect-a-container-to-a-service-on-the-host).

### Can I pass through a USB device to a container?

Docker Desktop does not support direct USB device passthrough. However, you can use USB over IP to connect common USB devices to the Docker Desktop VM and in turn be forwarded to a container. For more details, see
[Using USB/IP with Docker Desktop](https://docs.docker.com/desktop/features/usbip/).

### How do I verify Docker Desktop is using a proxy server ?

To verify, look at the most recent events logged in `httpproxy.log`. This is located at `~/Library/Containers/com.docker.docker/Data/log/host` on macOS or `%LOCALAPPDATA%/Docker/log/host/` on Windows.

The following shows a few examples of what you can expect to see:

- Docker Desktop using app level settings (proxy mode manual) for proxy:
  ```console
  host will use proxy: app settings http_proxy=http://172.211.16.3:3128 https_proxy=http://172.211.16.3:3128
  Linux will use proxy: app settings http_proxy=http://172.211.16.3:3128 https_proxy=http://172.211.16.3:3128
  ```
- Docker Desktop using system level settings (proxy mode system) for proxy:
  ```console
  host will use proxy: static system http_proxy=http://172.211.16.3:3128 https_proxy=http://172.211.16.3:3128 no_proxy=
  Linux will use proxy: static system http_proxy=http://172.211.16.3:3128 https_proxy=http://172.211.16.3:3128 no_proxy=
  ```
- Docker Desktop is not configured to use a proxy server:
  ```console
  host will use proxy: disabled
  Linux will use proxy: disabled
  ```
- Docker Desktop is configured to use app level settings (proxy mode manual) and using a PAC file:
  ```console
  using a proxy PAC file: http://127.0.0.1:8081/proxy.pac
  host will use proxy: app settings from PAC file http://127.0.0.1:8081/proxy.pac
  Linux will use proxy: app settings from PAC file http://127.0.0.1:8081/proxy.pac
  ```
- Connect request using the configured proxy server:
  ```console
  CONNECT desktop.docker.com:443: host connecting via static system HTTPS proxy http://172.211.16.3:3128
  ```

### How do I run Docker Desktop without administrator privileges?

Docker Desktop requires administrator privileges only for installation. Once installed, administrator privileges are not needed to run it. However, for non-admin users to run Docker Desktop, it must be installed using a specific installer flag and meet certain prerequisites, which vary by platform.

To run Docker Desktop on Mac without requiring administrator privileges, install via the command line and pass the `—user=<userid>` installer flag:

```console
$ /Applications/Docker.app/Contents/MacOS/install --user=<userid>
```

You can then sign in to your machine with the user ID specified, and launch Docker Desktop.

> Note
>
> Before launching Docker Desktop, if a `settings-store.json` file (or `settings.json` for Docker Desktop versions 4.34 and earlier) already exists in the `~/Library/Group Containers/group.com.docker/` directory, you will see a **Finish setting up Docker Desktop** window that prompts for administrator privileges when you select **Finish**. To avoid this, ensure you delete the `settings-store.json` file (or `settings.json` for Docker Desktop versions 4.34 and earlier) left behind from any previous installations before launching the application.

> Note
>
> If you are using the WSL 2 backend, first make sure that you meet the
> [minimum required version](https://docs.docker.com/desktop/features/wsl/best-practices/) for WSL 2. Otherwise, update WSL 2 first.

To run Docker Desktop on Windows without requiring administrator privileges, install via the command line and pass the `—always-run-service` installer flag.

```console
$ "Docker Desktop Installer.exe" install —always-run-service
```

---

# FAQs for Docker Desktop for Linux

> Frequently asked questions for Docker Desktop for Linux

# FAQs for Docker Desktop for Linux

   Table of contents

---

### Why does Docker Desktop for Linux run a VM?

Docker Desktop for Linux runs a Virtual Machine (VM) for the following reasons:

1. To ensure that Docker Desktop provides a consistent experience across platforms.
  During research, the most frequently cited reason for users wanting Docker Desktop for Linux was to ensure a consistent Docker Desktop
  experience with feature parity across all major operating systems. Utilizing
  a VM ensures that the Docker Desktop experience for Linux users will closely
  match that of Windows and macOS.
2. To make use of new kernel features.
  Sometimes we want to make use of new operating system features. Because we control the kernel and the OS inside the VM, we can roll these out to all users immediately, even to users who are intentionally sticking on an LTS version of their machine OS.
3. To enhance security.
  Container image vulnerabilities pose a security risk for the host environment. There is a large number of unofficial images that are not guaranteed to be verified for known vulnerabilities. Malicious users can push images to public registries and use different methods to trick users into pulling and running them. The VM approach mitigates this threat as any malware that gains root privileges is restricted to the VM environment without access to the host.
  Why not run rootless Docker? Although this has the benefit of superficially limiting access to the root user so everything looks safer in "top", it allows unprivileged users to gain `CAP_SYS_ADMIN` in their own user namespace and access kernel APIs which are not expecting to be used by unprivileged users, resulting in [vulnerabilities](https://www.openwall.com/lists/oss-security/2022/01/18/7).
4. To provide the benefits of feature parity and enhanced security, with minimal impact on performance.
  The VM utilized by Docker Desktop for Linux uses [VirtioFS](https://virtio-fs.gitlab.io), a shared file system that allows virtual machines to access a directory tree located on the host. Our internal benchmarking shows that with the right resource allocation to the VM, near native file system performance can be achieved with VirtioFS.
  As such, we have adjusted the default memory available to the VM in Docker Desktop for Linux. You can tweak this setting to your specific needs by using the **Memory** slider within the **Settings** > **Resources** tab of Docker Desktop.

### How do I enable file sharing?

Docker Desktop for Linux uses [VirtioFS](https://virtio-fs.gitlab.io/) as the
default (and currently only) mechanism to enable file sharing between the host
and Docker Desktop VM.

In order not to require elevated privileges, without
unnecessarily restricting operations on the shared files, Docker Desktop runs
the file sharing service (`virtiofsd`) inside a user namespace (see
`user_namespaces(7)`) with UID and GID mapping configured. As a result Docker
Desktop relies on the host being configured to enable the current user to use
subordinate ID delegation. For this to be true `/etc/subuid` (see `subuid(5)`)
and `/etc/subgid` (see `subgid(5)`) must be present. Docker Desktop only
supports subordinate ID delegation configured via files. Docker Desktop maps the
current user ID and GID to 0 in the containers. It uses the first entry
corresponding to the current user in `/etc/subuid` and `/etc/subgid` to set up
mappings for IDs greater than 0 in the containers.

| ID in container | ID on host |
| --- | --- |
| 0 (root) | ID of the user running Docker Desktop (e.g. 1000) |
| 1 | 0 + beginning of ID range specified in/etc/subuid//etc/subgid(e.g. 100000) |
| 2 | 1 + beginning of ID range specified in/etc/subuid//etc/subgid(e.g. 100001) |
| 3 | 2 + beginning of ID range specified in/etc/subuid//etc/subgid(e.g. 100002) |
| ... | ... |

If `/etc/subuid` and `/etc/subgid` are missing, they need to be created.
Both should contain entries in the form -
`<username>:<start of id range>:<id range size>`. For example, to allow the current user
to use IDs from 100 000 to 165 535:

```console
$ grep "$USER" /etc/subuid >> /dev/null 2&>1 || (echo "$USER:100000:65536" | sudo tee -a /etc/subuid)
$ grep "$USER" /etc/subgid >> /dev/null 2&>1 || (echo "$USER:100000:65536" | sudo tee -a /etc/subgid)
```

To verify the configs have been created correctly, inspect their contents:

```console
$ echo $USER
exampleuser
$ cat /etc/subuid
exampleuser:100000:65536
$ cat /etc/subgid
exampleuser:100000:65536
```

In this scenario if a shared file is `chown`ed inside a Docker Desktop container
owned by a user with a UID of 1000, it shows up on the host as owned by
a user with a UID of 100999. This has the unfortunate side effect of preventing
easy access to such a file on the host. The problem is resolved by creating
a group with the new GID and adding our user to it, or by setting a recursive
ACL (see `setfacl(1)`) for folders shared with the Docker Desktop VM.

### Where does Docker Desktop store Linux containers?

Docker Desktop stores Linux containers and images in a single, large "disk image" file in the Linux filesystem. This is different from Docker on Linux, which usually stores containers and images in the `/var/lib/docker` directory on the host's filesystem.

#### Where is the disk image file?

To locate the disk image file, select **Settings** from the Docker Desktop Dashboard then **Advanced** from the **Resources** tab.

The **Advanced** tab displays the location of the disk image. It also displays the maximum size of the disk image and the actual space the disk image is consuming. Note that other tools might display space usage of the file in terms of the maximum file size, and not the actual file size.

##### What if the file is too large?

If the disk image file is too large, you can:

- Move it to a bigger drive
- Delete unnecessary containers and images
- Reduce the maximum allowable size of the file

##### How do I move the file to a bigger drive?

To move the disk image file to a different location:

1. Select **Settings** then **Advanced** from the **Resources** tab.
2. In the **Disk image location** section, select **Browse** and choose a new location for the disk image.
3. Select **Apply** for the changes to take effect.

Do not move the file directly in Finder as this can cause Docker Desktop to lose track of the file.

##### How do I delete unnecessary containers and images?

Check whether you have any unnecessary containers and images. If your client and daemon API are running version 1.25 or later (use the `docker version` command on the client to check your client and daemon API versions), you can see the detailed space usage information by running:

```console
$ docker system df -v
```

Alternatively, to list images, run:

```console
$ docker image ls
```

To list containers, run:

```console
$ docker container ls -a
```

If there are lots of redundant objects, run the command:

```console
$ docker system prune
```

This command removes all stopped containers, unused networks, dangling images, and build cache.

It might take a few minutes to reclaim space on the host depending on the format of the disk image file:

- If the file is named `Docker.raw`: space on the host should be reclaimed within a few seconds.
- If the file is named `Docker.qcow2`: space will be freed by a background process after a few minutes.

Space is only freed when images are deleted. Space is not freed automatically when files are deleted inside running containers. To trigger a space reclamation at any point, run the command:

```console
$ docker run --privileged --pid=host docker/desktop-reclaim-space
```

Note that many tools report the maximum file size, not the actual file size.
To query the actual size of the file on the host from a terminal, run:

```console
$ cd ~/.docker/desktop/vms/0/data
$ ls -klsh Docker.raw
2333548 -rw-r--r--@ 1 username  staff    64G Dec 13 17:42 Docker.raw
```

In this example, the actual size of the disk is `2333548` KB, whereas the maximum size of the disk is `64` GB.

##### How do I reduce the maximum size of the file?

To reduce the maximum size of the disk image file:

1. From Docker Desktop Dashboard select **Settings** then **Advanced** from the **Resources** tab.
2. The **Disk image size** section contains a slider that allows you to change the maximum size of the disk image. Adjust the slider to set a lower limit.
3. Select **Apply**.

When you reduce the maximum size, the current disk image file is deleted, and therefore, all containers and images are lost.

---

# FAQs for Docker Desktop for Mac

> Frequently asked questions for Docker Desktop for Mac

# FAQs for Docker Desktop for Mac

   Table of contents

---

### What is HyperKit?

HyperKit is a hypervisor built on top of the Hypervisor.framework in macOS. It runs entirely in userspace and has no other dependencies.

Docker uses HyperKit to eliminate the need for other VM products, such as Oracle
VirtualBox or VMware Fusion.

### What is the benefit of HyperKit?

HyperKit is thinner than VirtualBox and VMware fusion, and the version included is customized for Docker workloads on Mac.

### Where does Docker Desktop store Linux containers and images?

Docker Desktop stores Linux containers and images in a single, large "disk image" file in the Mac filesystem. This is different from Docker on Linux, which usually stores containers and images in the `/var/lib/docker` directory.

#### Where is the disk image file?

To locate the disk image file, select **Settings** from the Docker Desktop Dashboard then **Advanced** from the **Resources** tab.

The **Advanced** tab displays the location of the disk image. It also displays the maximum size of the disk image and the actual space the disk image is consuming. Note that other tools might display space usage of the file in terms of the maximum file size, and not the actual file size.

#### What if the file is too big?

If the disk image file is too big, you can:

- Move it to a bigger drive
- Delete unnecessary containers and images
- Reduce the maximum allowable size of the file

##### How do I move the file to a bigger drive?

To move the disk image file to a different location:

1. Select **Settings** then **Advanced** from the **Resources** tab.
2. In the **Disk image location** section, select **Browse** and choose a new location for the disk image.
3. Select **Apply** for the changes to take effect.

> Important
>
> Do not move the file directly in Finder as this can cause Docker Desktop to lose track of the file.

##### How do I delete unnecessary containers and images?

Check whether you have any unnecessary containers and images. If your client and daemon API are running version 1.25 or later (use the `docker version` command on the client to check your client and daemon API versions), you can see the detailed space usage information by running:

```console
$ docker system df -v
```

Alternatively, to list images, run:

```console
$ docker image ls
```

To list containers, run:

```console
$ docker container ls -a
```

If there are lots of redundant objects, run the command:

```console
$ docker system prune
```

This command removes all stopped containers, unused networks, dangling images, and build cache.

It might take a few minutes to reclaim space on the host depending on the format of the disk image file. If the file is named:

- `Docker.raw`, space on the host is reclaimed within a few seconds.
- `Docker.qcow2`, space is freed by a background process after a few minutes.

Space is only freed when images are deleted. Space is not freed automatically when files are deleted inside running containers. To trigger a space reclamation at any point, run the command:

```console
$ docker run --privileged --pid=host docker/desktop-reclaim-space
```

Note that many tools report the maximum file size, not the actual file size.
To query the actual size of the file on the host from a terminal, run:

```console
$ cd ~/Library/Containers/com.docker.docker/Data/vms/0/data
$ ls -klsh Docker.raw
2333548 -rw-r--r--@ 1 username  staff    64G Dec 13 17:42 Docker.raw
```

In this example, the actual size of the disk is `2333548` KB, whereas the maximum size of the disk is `64` GB.

##### How do I reduce the maximum size of the file?

To reduce the maximum size of the disk image file:

1. Select **Settings** then **Advanced** from the **Resources** tab.
2. The **Disk image size** section contains a slider that allows you to change the maximum size of the disk image. Adjust the slider to set a lower limit.
3. Select **Apply**.

When you reduce the maximum size, the current disk image file is deleted, and therefore, all containers and images are lost.

### How do I add TLS certificates?

You can add trusted Certificate Authorities (CAs) (used to verify registry
server certificates) and client certificates (used to authenticate to
registries) to your Docker daemon.

#### Add custom CA certificates (server side)

All trusted CAs (root or intermediate) are supported. Docker Desktop creates a
certificate bundle of all user-trusted CAs based on the Mac Keychain, and
appends it to Moby trusted certificates. So if an enterprise SSL certificate is
trusted by the user on the host, it is trusted by Docker Desktop.

To manually add a custom, self-signed certificate, start by adding the
certificate to the macOS keychain, which is picked up by Docker Desktop. Here is
an example:

```console
$ sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain ca.crt
```

Or, if you prefer to add the certificate to your own local keychain only (rather
than for all users), run this command instead:

```console
$ security add-trusted-cert -d -r trustRoot -k ~/Library/Keychains/login.keychain ca.crt
```

See also, [Directory structures for
certificates](#directory-structures-for-certificates).

> Note
>
> You need to restart Docker Desktop after making any changes to the keychain or
> to the `~/.docker/certs.d` directory in order for the changes to take effect.

For a complete explanation of how to do this, see the blog post [Adding
Self-signed Registry Certs to Docker & Docker Desktop for
Mac](https://blog.container-solutions.com/adding-self-signed-registry-certs-docker-mac).

#### Add client certificates

You can put your client certificates in
`~/.docker/certs.d/<MyRegistry>:<Port>/client.cert` and
`~/.docker/certs.d/<MyRegistry>:<Port>/client.key`.

When the Docker Desktop application starts, it copies the `~/.docker/certs.d`
folder on your Mac to the `/etc/docker/certs.d` directory on Moby (the Docker
Desktop `xhyve` virtual machine).

> Note
>
> - You need to restart Docker Desktop after making any changes to the keychain
>   or to the `~/.docker/certs.d` directory in order for the changes to take
>   effect.
> - The registry cannot be listed as an *insecure registry*. Docker Desktop ignores certificates listed
>   under insecure registries, and does not send client certificates. Commands
>   like `docker run` that attempt to pull from the registry produce error
>   messages on the command line, as well as on the registry.

#### Directory structures for certificates

If you have this directory structure, you do not need to manually add the CA
certificate to your Mac OS system login:

```text
/Users/<user>/.docker/certs.d/
└── <MyRegistry>:<Port>
   ├── ca.crt
   ├── client.cert
   └── client.key
```

The following further illustrates and explains a configuration with custom
certificates:

```text
/etc/docker/certs.d/        <-- Certificate directory
└── localhost:5000          <-- Hostname:port
   ├── client.cert          <-- Client certificate
   ├── client.key           <-- Client key
   └── ca.crt               <-- Certificate authority that signed
                                the registry certificate
```

You can also have this directory structure, as long as the CA certificate is
also in your keychain.

```text
/Users/<user>/.docker/certs.d/
└── <MyRegistry>:<Port>
    ├── client.cert
    └── client.key
```

To learn more about how to install a CA root certificate for the registry and
how to set the client TLS certificate for verification, see
[Verify repository client with certificates](https://docs.docker.com/engine/security/certificates/)
in the Docker Engine topics.

---

# FAQs on Docker Desktop releases

> Frequently asked Docker Desktop questions for all platforms

# FAQs on Docker Desktop releases

   Table of contents

---

### How frequent will new releases be?

New releases are available roughly every month, unless there are critical fixes that need to be released sooner.

The **Automatically check for updates** setting in the **Software updates** tab is turned on by default. This means you receive notifications in the Docker menu and a notification badge on the Docker Desktop Dashboard when a new version is available.

You can also let Docker Desktop automatically download new updates in the background by selecting the **Always download updates** checkbox.

Sometimes new versions are rolled out gradually over a few days. Therefore, if you wait, it will turn up soon. Alternatively, you can select **Check for updates** in the Docker menu to get the latest version immediately.

### How do I ensure that all users in my organization are using the same version?

This is managed through your IT administrator's endpoint management software.

---

# FAQs for Docker Desktop for Windows

> Frequently asked questions for Docker Desktop for Windows

# FAQs for Docker Desktop for Windows

   Table of contents

---

### Can I use VirtualBox alongside Docker Desktop?

Yes, you can run VirtualBox along with Docker Desktop if you have enabled the [Windows Hypervisor Platform](https://docs.microsoft.com/en-us/virtualization/api/) feature on your machine.

### Why is Windows 10 or Windows 11 required?

Docker Desktop uses the Windows Hyper-V features. While older Windows versions have Hyper-V, their Hyper-V implementations lack features critical for Docker Desktop to work.

### Can I run Docker Desktop on Windows Server?

No, running Docker Desktop on Windows Server is not supported.

### How do symlinks work on Windows?

Docker Desktop supports two types of symlinks: Windows native symlinks and symlinks created inside a container.

The Windows native symlinks are visible within the containers as symlinks, whereas symlinks created inside a container are represented as [mfsymlinks](https://wiki.samba.org/index.php/UNIX_Extensions#Minshall.2BFrench_symlinks). These are regular Windows files with a special metadata. Therefore the symlinks created inside a container appear as symlinks inside the container, but not on the host.

### File sharing with Kubernetes and WSL 2

Docker Desktop mounts the Windows host filesystem under `/run/desktop` inside the container running Kubernetes.
See the [Stack Overflow post](https://stackoverflow.com/questions/67746843/clear-persistent-volume-from-a-kubernetes-cluster-running-on-docker-desktop/69273405#69273) for an example of how to configure a Kubernetes Persistent Volume to represent directories on the host.

### How do I add custom CA certificates?

You can add trusted Certificate Authorities (CAs) to your Docker daemon to verify registry server certificates, and client certificates, to authenticate to registries.

Docker Desktop supports all trusted Certificate Authorities (CAs) (root or
intermediate). Docker recognizes certs stored under Trust Root
Certification Authorities or Intermediate Certification Authorities.

Docker Desktop creates a certificate bundle of all user-trusted CAs based on
the Windows certificate store, and appends it to Moby trusted certificates. Therefore, if an enterprise SSL certificate is trusted by the user on the host, it is trusted by Docker Desktop.

To learn more about how to install a CA root certificate for the registry, see
[Verify repository client with certificates](https://docs.docker.com/engine/security/certificates/)
in the Docker Engine topics.

### How do I add client certificates?

You can add your client certificates
in `~/.docker/certs.d/<MyRegistry><Port>/client.cert` and
`~/.docker/certs.d/<MyRegistry><Port>/client.key`. You do not need to push your certificates with `git` commands.

When the Docker Desktop application starts, it copies the
`~/.docker/certs.d` folder on your Windows system to the `/etc/docker/certs.d`
directory on Moby (the Docker Desktop virtual machine running on Hyper-V).

You need to restart Docker Desktop after making any changes to the keychain
or to the `~/.docker/certs.d` directory in order for the changes to take effect.

The registry cannot be listed as an insecure registry (see
[Docker Daemon](https://docs.docker.com/desktop/settings-and-maintenance/settings/#docker-engine)). Docker Desktop ignores
certificates listed under insecure registries, and does not send client
certificates. Commands like `docker run` that attempt to pull from the registry
produce error messages on the command line, as well as on the registry.

To learn more about how to set the client TLS certificate for verification, see
[Verify repository client with certificates](https://docs.docker.com/engine/security/certificates/)
in the Docker Engine topics.

---

# Give feedback

> Find a way to provide feedback that's right for you

# Give feedback

   Table of contents

---

There are many ways you can provide feedback on Docker Desktop or Docker Desktop features.

### In-product feedback

On each Docker Desktop Dashboard view, there is a **Give feedback** link. This opens a feedback form where you can share ideas directly with the Docker Team.

### Feedback via Docker Community forums

To get help from the community, review current user topics, join or start a
discussion, sign in to the appropriate Docker forums:

- [Docker Desktop for Mac forum](https://forums.docker.com/c/docker-for-mac)
- [Docker Desktop for Windows forum](https://forums.docker.com/c/docker-for-windows)
- [Docker Desktop for Linux forum](https://forums.docker.com/c/docker-desktop-for-linux/60)

### Report bugs or problems on GitHub

To report bugs or problems, visit:

- [Docker Desktop issues on GitHub](https://github.com/docker/desktop-feedback)
- [Docker Extensions issues on GitHub](https://github.com/docker/extensions-sdk/issues)

### Feedback via Community Slack channels

You can also provide feedback through the following [Docker Community Slack](https://dockr.ly/comm-slack) channels:

- #docker-desktop-mac
- #docker-desktop-windows
- #docker-desktop-linux
- #extensions

---

# Known issues

> Find known issues for Docker Desktop

# Known issues

---

- The Mac Activity Monitor reports that Docker is using twice the amount of memory it's actually using. This is due to a [bug in macOS](https://docs.google.com/document/d/17ZiQC1Tp9iH320K-uqVLyiJmk4DHJ3c4zgQetJiKYQM/edit?usp=sharing).
- **"Docker.app is damaged" dialog**: If you see a "Docker.app is damaged and can't be opened" dialog during installation or updates, this is typically caused by non-atomic copy operations when other applications are using the Docker CLI. See [Fix "Docker.app is damaged" on macOS](https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/mac-damaged-dialog/) for resolution steps.
- Force-ejecting the `.dmg` after running `Docker.app` from it can cause the
  whale icon to become unresponsive, Docker tasks to show as not responding in the Activity Monitor, and for some processes to consume a large amount of CPU resources. Reboot and restart Docker to resolve these issues.
- Docker Desktop uses the `HyperKit` hypervisor
  ([https://github.com/docker/hyperkit](https://github.com/docker/hyperkit)) in macOS 10.10 Yosemite and higher. If
  you are developing with tools that have conflicts with `HyperKit`, such as
  [Intel Hardware Accelerated Execution Manager
  (HAXM)](https://software.intel.com/en-us/android/articles/intel-hardware-accelerated-execution-manager/),
  the current workaround is not to run them at the same time. You can pause
  `HyperKit` by quitting Docker Desktop temporarily while you work with HAXM.
  This allows you to continue work with the other tools and prevent `HyperKit`
  from interfering.
- If you are working with applications like [Apache
  Maven](https://maven.apache.org/) that expect settings for `DOCKER_HOST` and
  `DOCKER_CERT_PATH` environment variables, specify these to connect to Docker
  instances through Unix sockets. For example:
  ```console
  $ export DOCKER_HOST=unix:///var/run/docker.sock
  ```

- Some command line tools do not work when Rosetta 2 is not installed.
  - The old version 1.x of `docker-compose`. Use Compose V2 instead - type `docker compose`.
  - The `docker-credential-ecr-login` credential helper.
- Some images do not support the ARM64 architecture. You can add `--platform linux/amd64` to run (or build) an Intel image using emulation.
  However, attempts to run Intel-based containers on Apple silicon machines under emulation can crash as QEMU sometimes fails to run the container. In addition, filesystem change notification APIs (`inotify`) do not work under QEMU emulation. Even when the containers do run correctly under emulation, they will be slower and use more memory than the native equivalent.
  In summary, running Intel-based containers on Arm-based machines should be regarded as "best effort" only. We recommend running `arm64` containers on Apple silicon machines whenever possible, and encouraging container authors to produce `arm64`, or multi-arch, versions of their containers. This issue should become less common over time, as more and more images are rebuilt [supporting multiple architectures](https://www.docker.com/blog/multi-arch-build-and-images-the-simple-way/).
- Users may occasionally experience data drop when a TCP stream is half-closed.

---

# Fix "Docker.app is damaged and can't be opened" on macOS

> Fix "Docker.app is damaged and can't be opened. You should move it to the Trash" dialog on macOS

# Fix "Docker.app is damaged and can't be opened" on macOS

   Table of contents

---

## Error message

macOS shows the following dialog when you try to open Docker Desktop:

```text
Docker.app is damaged and can't be opened. You should move it to the Trash.
```

This error prevents Docker Desktop from launching and can occur during installation or after updates.

## Possible cause

This issue occurs due to a non-atomic copy during a drag/drop installation. When you drag and drop `Docker.app` from a DMG file while another application, like VS Code, is invoking the Docker CLI through symlinks, the copy operation may be interrupted, leaving the app in a partially copied state that Gatekeeper marks as "damaged".

## Solution

Follow these steps to resolve the issue:

### Step one: Quit third-party software

Close any applications that might call Docker in the background:

- Visual Studio Code and other IDEs
- Terminal applications
- Agent apps or development tools
- Any scripts or processes that use the Docker CLI

### Step two: Remove any partial installation

1. Move `/Applications/Docker.app` to Trash and empty Trash.
2. If you used a DMG installer, eject and re-mount the Docker DMG.

### Step three: Reinstall Docker Desktop

Follow the instructions in the
[macOS installation guide](https://docs.docker.com/desktop/setup/install/mac-install/) to reinstall Docker Desktop.

### If the dialog persists

If you continue to see the "damaged" dialog after following the recovery steps:

1. Gather diagnostics using the terminal. Follow the instructions in
  [Diagnose from the terminal](https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/#diagnose-from-the-terminal).
  - Note down the your diagnostics ID displayed in the terminal after running diagnostics.
2. Get help:
  - If you have a paid Docker subscription,
    [contact support](https://docs.docker.com/support/) and include your diagnostics ID
  - For community users, [open an issue on GitHub](https://github.com/docker/desktop-feedback) and include your diagnostics ID

## Prevention

To avoid this issue in the future:

- If your organization allows, update Docker Desktop via the in-app update flow
- Always quit applications that use Docker before installing Docker Desktop via the DMG installer drag-and-drop approach
- In managed environments, use PKG installations over DMG drag-and-drop
- Keep installer volumes mounted until installation is complete

## Related information

- [Install Docker Desktop on Mac](https://docs.docker.com/desktop/setup/install/mac-install/)
- [PKG installer documentation](https://docs.docker.com/enterprise/enterprise-deployment/pkg-install-and-configure/)
- [Troubleshoot Docker Desktop](https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/)
- [Known issues](https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/known-issues/)
