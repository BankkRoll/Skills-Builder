# containerd image store and more

# containerd image store

> How to activate the containerd integration feature in Docker Desktop

# containerd image store

   Table of contents

---

Docker Desktop is transitioning to use containerd for image and filesystem management. This page outlines the benefits, setup process, and new capabilities enabled by the containerd image store.

> Note
>
> Docker Desktop maintains separate image stores for the classic and containerd image stores.
> When switching between them, images and containers from the inactive store remain on disk but are hidden until you switch back.

## What iscontainerd?

`containerd` is a container runtime that provides a lightweight, consistent interface for container lifecycle management. It is already used under the hood by Docker Engine for creating, starting, and stopping containers.

Docker Desktop’s ongoing integration of containerd now extends to the image store, offering more flexibility and modern image support.

## What is thecontainerdimage store?

The image store is the component responsible for pushing, pulling,
and storing images on the filesystem.

The classic Docker image store is limited in the types of images that it supports.
For example, it doesn't support image indices, containing manifest lists.
When you create multi-platform images, for example,
the image index resolves all the platform-specific variants of the image.
An image index is also required when building images with attestations.

The containerd image store extends the range of image types
that the Docker Engine can natively interact with.
While this is a low-level architectural change,
it's a prerequisite for unlocking a range of new use cases, including:

- [Build multi-platform images](#build-multi-platform-images) and images with attestations
- Support for using containerd snapshotters with unique characteristics,
  such as [stargz](https://github.com/containerd/stargz-snapshotter) for lazy-pulling images on container startup,
  or [nydus](https://github.com/containerd/nydus-snapshotter) and [dragonfly](https://github.com/dragonflyoss/image-service) for peer-to-peer image distribution.
- Ability to run [Wasm](https://docs.docker.com/desktop/features/wasm/) containers

## Enable the containerd image store

The containerd image store is enabled by default in Docker Desktop version 4.34
and later, but only for clean installs or if you perform a factory reset. If
you upgrade from an earlier version of Docker Desktop, or if you use an older
version of Docker Desktop you must manually switch to the containerd image
store.

To manually enable this feature in Docker Desktop:

1. Navigate to **Settings** in Docker Desktop.
2. In the **General** tab, check **Use containerd for pulling and storing images**.
3. Select **Apply**.

To disable the containerd image store,
clear the **Use containerd for pulling and storing images** checkbox.

## Build multi-platform images

The term multi-platform image refers to a bundle of images for multiple different architectures.
Out of the box, the default builder for Docker Desktop doesn't support building multi-platform images.

```console
$ docker build --platform=linux/amd64,linux/arm64 .
[+] Building 0.0s (0/0)
ERROR: Multi-platform build is not supported for the docker driver.
Switch to a different driver, or turn on the containerd image store, and try again.
Learn more at https://docs.docker.com/go/build-multi-platform/
```

Enabling the containerd image store lets you build multi-platform images
and load them to your local image store:

---

# Use the Docker Desktop CLI

> How to use the Docker Desktop CLI

# Use the Docker Desktop CLI

   Table of contents

---

Requires: Docker Desktop
[4.37](https://docs.docker.com/desktop/release-notes/#4370) and later

The Docker Desktop CLI lets you perform key operations such as starting, stopping, restarting, and updating Docker Desktop directly from the command line.

The Docker Desktop CLI provides:

- Simplified automation for local development: Execute Docker Desktop operations more efficiently in scripts and tests.
- An improved developer experience: Restart, quit, or reset Docker Desktop from the command line, reducing dependency on the Docker Desktop Dashboard and improving flexibility and efficiency.

## Usage

```console
docker desktop COMMAND [OPTIONS]
```

## Commands

| Command | Description |
| --- | --- |
| start | Starts Docker Desktop |
| stop | Stops Docker Desktop |
| restart | Restarts Docker Desktop |
| status | Displays whether Docker Desktop is running or stopped. |
| engine ls | Lists available engines (Windows only) |
| engine use | Switch between Linux and Windows containers (Windows only) |
| update | Manage Docker Desktop updates. Available for Mac only with Docker Desktop version 4.38, or all OSs with Docker Desktop version 4.39 and later. |
| logs | Print log entries |
| disable | Disable a feature |
| enable | Enable a feature |
| version | Show the Docker Desktop CLI plugin version information |
| kubernetes | List Kubernetes images used by Docker Desktop or restart the cluster. Available with Docker Desktop version 4.44 and later. |

For more details on each command, see the
[Docker Desktop CLI reference](https://docs.docker.com/reference/cli/docker/desktop/).

---

# GPU support in Docker Desktop for Windows

> How to use GPU in Docker Desktop

# GPU support in Docker Desktop for Windows

   Table of contents

---

> Note
>
> Currently GPU support in Docker Desktop is only available on Windows with the WSL2 backend.

Docker Desktop for Windows supports NVIDIA GPU Paravirtualization (GPU-PV) on NVIDIA GPUs, allowing containers to access GPU resources for compute-intensive workloads like AI, machine learning, or video processing.

## Prerequisites

To enable WSL 2 GPU Paravirtualization, you need:

- A Windows machine with an NVIDIA GPU
- Up to date Windows 10 or Windows 11 installation
- [Up to date drivers](https://developer.nvidia.com/cuda/wsl) from NVIDIA supporting WSL 2 GPU Paravirtualization
- The latest version of the WSL 2 Linux kernel. Use `wsl --update` on the command line
- To make sure the [WSL 2 backend is turned on](https://docs.docker.com/desktop/features/wsl/#turn-on-docker-desktop-wsl-2) in Docker Desktop

## Validate GPU support

To confirm GPU access is working inside Docker, run the following:

```console
$ docker run --rm -it --gpus=all nvcr.io/nvidia/k8s/cuda-sample:nbody nbody -gpu -benchmark
```

This runs an n-body simulation benchmark on the GPU. The output will be similar to:

```console
Run "nbody -benchmark [-numbodies=<numBodies>]" to measure performance.
        -fullscreen       (run n-body simulation in fullscreen mode)
        -fp64             (use double precision floating point values for simulation)
        -hostmem          (stores simulation data in host memory)
        -benchmark        (run benchmark to measure performance)
        -numbodies=N    (number of bodies (>= 1) to run in simulation)
        -device=<d>       (where d=0,1,2.... for the CUDA device to use)
        -numdevices=<i>   (where i=(number of CUDA devices > 0) to use for simulation)
        -compare          (compares simulation results running once on the default GPU and once on the CPU)
        -cpu              (run n-body simulation on the CPU)
        -tipsy=<file.bin> (load a tipsy model file for simulation)

> NOTE: The CUDA Samples are not meant for performance measurements. Results may vary when GPU Boost is enabled.

> Windowed mode
> Simulation data stored in video memory
> Single precision floating point simulation
> 1 Devices used for simulation
MapSMtoCores for SM 7.5 is undefined.  Default to use 64 Cores/SM
GPU Device 0: "GeForce RTX 2060 with Max-Q Design" with compute capability 7.5

> Compute 7.5 CUDA device: [GeForce RTX 2060 with Max-Q Design]
30720 bodies, total time for 10 iterations: 69.280 ms
= 136.219 billion interactions per second
= 2724.379 single-precision GFLOP/s at 20 flops per interaction
```

## Run a real-world model: SmolLM2 with Docker Model Runner

> Note
>
> Docker Model Runner with vLLM for Windows with WSL2 is available starting with Docker Desktop 4.54.

Use Docker Model Runner to run the SmolLM2 LLM with vLLM and GPU acceleration:

```console
$ docker model install-runner --backend vllm --gpu cuda
```

Check it's correctly installed:

```console
$ docker model status
Docker Model Runner is running

Status:
llama.cpp: running llama.cpp version: c22473b
vllm: running vllm version: 0.11.0
```

Run the model:

```console
$ docker model run ai/smollm2-vllm hi
Hello! I'm sure everything goes smoothly here. How can I assist you today?
```

---

# Explore networking how

> Learn how to connect containers to the host, across containers, or through proxies and VPNs in Docker Desktop.

# Explore networking how-tos on Docker Desktop

   Table of contents

---

This page explains how to configure and use networking features, connect containers to host services, work behind proxies or VPNs, and troubleshoot common issues.

For details on how Docker Desktop routes network traffic and file I/O between containers, the VM, and the host, see
[Network overview](https://docs.docker.com/desktop/features/networking/#overview).

## Core networking how-tos

### Connect a container to a service on the host

The host has a changing IP address, or none if you have no network access. To connect to services running on your host, use the special DNS name:

| Name | Description |
| --- | --- |
| host.docker.internal | Resolves to the internal IP address of your host |
| gateway.docker.internal | Resolves to the gateway IP of the Docker VM |

#### Example

Run a simple HTTP server on port `8000`:

```console
$ python -m http.server 8000
```

Then run a container, install `curl`, and try to connect to the host using the following commands:

```console
$ docker run --rm -it alpine sh
# apk add curl
# curl http://host.docker.internal:8000
# exit
```

### Connect to a container from the host

To access containerized services from your host or local network, publish ports with the `-p` or `--publish` flag. For example:

```console
$ docker run -d -p 80:80 --name webserver nginx
```

Docker Desktop makes whatever is running on port `80` in the container, in
this case, `nginx`, available on port `80` of `localhost`.

> Tip
>
> The syntax for `-p` is `HOST_PORT:CLIENT_PORT`.

To publish all ports, use the `-P` flag. For example, the following command
starts a container (in detached mode) and the `-P` flag publishes all exposed ports of the
container to random ports on the host.

```console
$ docker run -d -P --name webserver nginx
```

Alternatively, you can also use
[host networking](https://docs.docker.com/engine/network/drivers/host/#docker-desktop)
to give the container direct access to the network stack of the host.

See the
[run command](https://docs.docker.com/reference/cli/docker/container/run/) for more details on
publish options used with `docker run`.

All inbound connections pass through the Docker Desktop backend process (`com.docker.backend` (Mac), `com.docker.backend` (Windows), or `qemu` (Linux), which handles port forwarding into the VM.
For more details, see
[How exposed ports work](https://docs.docker.com/desktop/features/networking/#how-exposed-ports-work)

### Working with VPNs

Docker Desktop networking can work when attached to a VPN.

To do this, Docker Desktop intercepts traffic from the containers and injects it into
the host as if it originated from the Docker application.

For details about how this traffic appears to host firewalls and endpoint detection systems, see
[Firewalls and endpoint visibility](https://docs.docker.com/desktop/features/networking/#firewalls-and-endpoint-visibility.md).

### Working with proxies

Docker Desktop can use your system proxy or a manual configuration.
To configure proxies:

1. Navigate to the **Resources** tab in **Settings**.
2. From the dropdown menu select **Proxies**.
3. Switch on the **Manual proxy configuration** toggle.
4. Enter your HTTP, HTTPS or SOCKS5 proxy URLS.

For more details on proxies and proxy configurations, see the
[Proxy settings documentation](https://docs.docker.com/desktop/settings-and-maintenance/settings/#proxies).

## Network how-tos for Mac and Windows

With Docker Desktop version 4.42 and later, you can control how Docker handles container networking and DNS resolution to better support a range of environments — from IPv4-only to dual-stack and IPv6-only systems. These settings help prevent timeouts and connectivity issues caused by incompatible or misconfigured host networks.

You can set the following settings on the **Network** tab in the Docker Desktop Dashboard settings, or if you're an admin, with Settings Management via the
[admin-settings.jsonfile](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/configure-json-file/#networking), or the
[Admin Console](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/configure-admin-console/)

> Note
>
> These settings can be overridden on a per-network basis using CLI flags or Compose file options.

### Default networking mode

Choose the default IP protocol used when Docker creates new networks. This allows you to align Docker with your host’s network capabilities or organizational requirements, such as enforcing IPv6-only access.

| Mode | Description |
| --- | --- |
| Dual IPv4/IPv6 (default) | Supports both IPv4 and IPv6. Most flexible. |
| IPv4 only | Uses only IPv4 addressing. |
| IPv6 only | Uses only IPv6 addressing. |

### DNS resolution behavior

Control how Docker filters DNS records returned to containers, improving reliability in environments where only IPv4 or IPv6 is supported. This setting is especially useful for preventing apps from trying to connect using IP families that aren't actually available, which can cause avoidable delays or failures.

| Option | Description |
| --- | --- |
| Auto (recommended) | Automatically filters unsupported record types. (A for IPv4, AAAA for IPv6) |
| Filter IPv4 (A records) | Blocks IPv4 lookups. Only available in dual-stack mode. |
| Filter IPv6 (AAAA records) | Blocks IPv6 lookups. Only available in dual-stack mode. |
| No filtering | Returns both A and AAAA records. |

> Important
>
> Switching the default networking mode resets the DNS filter to Auto.

## Network how-tos for Mac and Linux

### SSH agent forwarding

Docker Desktop for Mac and Linux lets you use the host’s SSH agent inside a container. To do this:

1. Bind mount the SSH agent socket by adding the following parameter to your `docker run` command:
  ```console
  $--mount type=bind,src=/run/host-services/ssh-auth.sock,target=/run/host-services/ssh-auth.sock
  ```
2. Add the `SSH_AUTH_SOCK` environment variable in your container:
  ```console
  $ -e SSH_AUTH_SOCK="/run/host-services/ssh-auth.sock"
  ```

To enable the SSH agent in Docker Compose, add the following flags to your service:

```yaml
services:
 web:
   image: nginx:alpine
   volumes:
     - type: bind
       source: /run/host-services/ssh-auth.sock
       target: /run/host-services/ssh-auth.sock
   environment:
     - SSH_AUTH_SOCK=/run/host-services/ssh-auth.sock
```

## Known limitations

### Changing internal IP addresses

The internal IP addresses used by Docker can be changed from **Settings**. After changing IPs, you need to reset the Kubernetes cluster and to leave any active Swarm.

### There is nodocker0bridge on the host

Because of the way networking is implemented in Docker Desktop, you cannot
see a `docker0` interface on the host. This interface is actually within the
virtual machine.

### I cannot ping my containers

Docker Desktop can't route traffic to Linux containers. However if you're a Windows user, you can
ping the Windows containers.

### Per-container IP addressing is not possible

This is because the Docker `bridge` network is not reachable from the host.
However if you are a Windows user, per-container IP addressing is possible with Windows containers.

---

# Networking on Docker Desktop

> Understand how Docker Desktop handles networking, firewalls, file access, proxies, and endpoint visibility.

# Networking on Docker Desktop

   Table of contents

---

This page explains how Docker Desktop routes network traffic and file I/O between containers, the VM, and the host, and how this behavior is visible to firewalls and endpoint protection tools.

## Overview

Docker Desktop runs the Docker Engine inside a lightweight Linux virtual machine (VM). Depending on your system configuration and operating system, Docker Desktop routes network and file operations between the Docker VM and the host using different backend components.

### Backend components and responsibilities

The backend acts as:

- Network proxy: Translates traffic between the host and Linux VM.
  - On Windows and Mac, this is handled by the `com.docker.backend` process.
  - On Linux, the `qemu` process performs this function.
- File server: Handles file access from containers to the host filesystem.
  - When using gRPC FUSE, the backend performs the file sharing.
  - When using `virtiofs`, `osxfs`, or `krun`, file access is handled by those respective daemons rather than the backend process.
- Control plane: Manages Docker API calls, port forwarding, and proxy configuration.

The following table summarizes typical setups in more detail:

| Platform | Setup | Networking handled by | File sharing handled by | Notes |
| --- | --- | --- | --- | --- |
| Windows | Hyper-V | com.docker.backend.exe | com.docker.backend.exe | Simplest setup with full visibility to EDR/firewall tools |
| Windows (WSL 2) | WSL 2 | com.docker.backend.exe | WSL 2 kernel (no visibility from host) | Recommended only when WSL 2 integration is needed |
| Mac | Virtualization framework + gRPC FUSE | com.docker.backend | com.docker.backend | Recommended for performance and visibility |
| Mac | Virtualization framework +virtiofs | com.docker.backend | Apple's Virtualization framework | Higher performance but no file access visibility from host |
| Mac | Virtualization framework +osxfs | com.docker.backend | osxfs | Legacy setup, not recommended |
| Mac | DockerVMM +virtiofs | com.docker.backend | krun | Currently in Beta |
| Linux | Native Linux VM | qemu | virtiofsd | Nocom.docker.backendprocess on Linux |

## How containers connect to the internet

Each Linux container in Docker Desktop runs inside a small virtual network managed by Docker and every container is attached to a Docker-managed network and receives its own internal IP address. You can view and these networks with `docker network ls`, `docker network create`, and `docker network inspect`. They are managed by the
[daemon.json](https://docs.docker.com/engine/daemon/).

When a container initiates a network request, for example with `apt-get update` or `docker pull`:

- The container’s `eth0` interface connects to a virtual bridge (`docker0`) inside the VM.
- Outbound traffic from the container is sent through Network Address Translation (NAT) using a virtual adapter (typically with an internal IP such as `192.168.65.3`). You can view or change this with the
  [Docker Desktop settings](https://docs.docker.com/desktop/settings-and-maintenance/settings/#network).
- The traffic is transferred to the host system over a shared-memory channel rather than through a traditional virtual network interface. This approach ensures reliable communication and avoids conflicts with host-level network adapters or firewall configurations.
- On the host, Docker Desktop’s backend process receives the traffic and creates standard TCP/IP connections using the same networking APIs as other applications.

All outbound container network traffic originates from the `com.docker.backend` process. Firewalls, VPNs, and security tools, like Crowdstrike, see traffic coming from this process — not from a VM or unknown source so firewall and endpoint security software can apply rules directly to `com.docker.backend`.

## How exposed ports work

When you publish a container port using the `-p` or `--publish` flag, Docker Desktop makes that container port accessible from your host system or local network.

For example, with `docker run -p 80:80 nginx`:

- Docker Desktop's backend process listens on the specified host port, in this case, port `80`.
- When an application such as a web browser connects to that port, Docker Desktop forwards the connection into the Linux VM where the container is running over a shared-memory channel.
- Inside the VM, the connection is routed to the container’s internal IP address and port, for example `172.17.0.2:80`.
- The container responds through the same path, so you can access it from your host just like any other local service.

By default, `docker run -p` listens on all network interfaces (`0.0.0.0`), but you can restrict it to a specific address, such as `127.0.0.1` (`localhost`) or a particular network adapter. This behavior can be modified to bind to `localhost` by default in
[Docker Desktop's network settings](https://docs.docker.com/desktop/settings-and-maintenance/settings/#network)

Host firewalls can permit or deny inbound connections by filtering on `com.docker.backend`.

## Using Docker Desktop with a proxy

Docker Desktop can use your system’s default proxy settings or custom settings that you configure with
[Docker Desktop's proxy setting](https://docs.docker.com/desktop/settings-and-maintenance/settings/#proxies). All proxy traffic passes through `com.docker.backend.exe`.

When a proxy is enabled:

- The backend process forwards the network requests, for example `docker pull`, through an internal proxy at `http.docker.internal:3128`.
- The internal proxy then connects either directly to the internet or through your upstream proxy, depending on your configuration and adding authentication if necessary.
- Docker Desktop then downloads the requested images or data through the proxy as usual.

Note that:

- The proxy honors system or manual proxy configuration.
- On Windows, Basic, NTLM, and Kerberos authentication is supported.
- For Mac, NTLM/Kerberos is not supported natively. Run a local proxy on `localhost` as a workaround.
- CLI plugins and other tools that use the Docker API directly must be configured separately with the `HTTP_PROXY`, `HTTPS_PROXY`, and `NO_PROXY` environment variables.

## Firewalls and endpoint visibility

To restrict VM or container networking apply rules to `com.docker.backend.exe` (Windows) `com.docker.backend` (Mac) or `qemu` (Linux) as all VM networking is funneled through these processes.

Use Windows Defender Firewall or enterprise endpoint firewalls for control. This enables traffic inspection and restriction at the host level without modifying the Docker Engine.

Crowdstrike and similar tools can observe all traffic and file access that passes through the backend process.

| Action | Visible to host EDR? | Reason |
| --- | --- | --- |
| Container reads host files | Yes | Access handled bycom.docker.backend |
| Container writes host files | Yes | Same process performs the write |
| Container accesses its own filesystem layers | No | Exists only inside the VM |

---

# Synchronized file shares

> Get started with Synchronized file shares on Docker Desktop.

# Synchronized file shares

   Table of contents

---

Subscription: Pro  Team  Business

Synchronized file shares is an alternative file sharing mechanism that provides fast and flexible host-to-VM file sharing, enhancing bind mount performance through the use of synchronized filesystem caches.

![Image of Synchronized file shares pane](https://docs.docker.com/desktop/images/synched-file-shares.webp)  ![Image of Synchronized file shares pane](https://docs.docker.com/desktop/images/synched-file-shares.webp)

## Who is it for?

Synchronized file shares is ideal for developers who:

- Have large repositories or monorepos with 100 000 files or more totaling hundreds of megabytes or even gigabytes.
- Are using virtual filesystems, such as VirtioFS, gRPC FUSE, and osxfs, which are no longer scaling well with their codebases.
- Regularly encounter performance limitations.
- Don't want to worry about file ownership or spend time resolving conflicting file-ownership information when modifying multiple containers.

## How does Synchronized file shares work?

A Synchronized file share behaves just like a virtual file share, but takes advantage of a high-performance, low-latency code synchronization engine to create a synchronized cache of the host files on an ext4 filesystem within the Docker Desktop VM. If you make filesystem changes on the host or in the VM’s containers, it propagates via bidirectional synchronization.

After creating a file share instance, any container using a bind mount that points to a location on the host filesystem matching the specified synchronized file share location, or a subdirectory within it, utilizes the Synchronized File Shares feature. Bind mounts that don't satisfy this condition are passed to the normal virtual filesystem
[bind-mounting mechanism](https://docs.docker.com/engine/storage/bind-mounts/), for example VirtioFS or gRPC-FUSE.

> Note
>
> Synchronized file shares is not used by Kubernetes' `hostPath` volumes in Docker Desktop.

> Important
>
> Synchronized file shares isn't available on WSL or when using Windows containers.

## Create a file share instance

To create a file share instance:

1. Sign in to Docker Desktop.
2. In **Settings**, navigate to the **File sharing** tab within the **Resources** section.
3. In the **Synchronized file shares** section, select **Create share**.
4. Select a host folder to share. The synchronized file share should initialize and be usable.

File shares take a few seconds to initialize as files are copied into the Docker Desktop VM. During this time, the status indicator displays **Preparing**. There is also a status icon in the footer of the Docker Desktop Dashboard that keeps you updated.

When the status indicator displays **Watching for filesystem changes**, your files are available to the VM through all the standard bind mount mechanisms, whether that's `-v` in the command line or specified in your `compose.yml` file.

> Note
>
> When you create a new service, setting the
> [bind mount option consistency](https://docs.docker.com/reference/cli/docker/service/create/#options-for-bind-mounts) to `:consistent` bypasses Synchronized file shares.

> Tip
>
> Docker Compose can automatically create file shares for bind mounts.
> Ensure you're signed in to Docker with a paid subscription and have enabled both **Access experimental features** and **Manage Synchronized file shares with Compose** in Docker Desktop's settings.

## Explore your file share instance

The **Synchronized file shares** section displays all your file share instances and provides useful information about each instance including:

- The origin of the file share content
- A status update
- How much space each file share is using
- The number of filesystem entry counts
- The number of symbolic links
- Which container(s) is using the file share instance

Selecting a file share instance expands the dropdown and exposes this information.

## Use.syncignore

You can use a `.syncignore` file at the root of each file share, to exclude local files from your file share instance. It supports the same syntax as `.dockerignore` files and excludes, and/or re-includes, paths from synchronization. `.syncignore` files are ignored at any location other than the root of the file share.

Some example of things you might want to add to your `.syncignore` file are:

- Large dependency directories, for example `node_modules` and `composer` directories (unless you rely on accessing them via a bind mount)
- `.git` directories (again, unless you need them)

In general, use your `.syncignore` file to exclude items that aren't critical to your workflow, especially those that would be slow to sync or use significant storage.

## Known issues

- Changes made to `.syncignore` don't lead to immediate deletions unless the file share is recreated. In other words, files that are newly ignored due to modifications in the `.syncignore` file remain in their current location, but are no longer updated during synchronization.
- File share instances are currently limited to approximately 2 million files per share. For best performance, if you have a file share instance of this size, try to decompose it into multiple shares corresponding to individual bind mount locations.
- Case conflicts, due to Linux being case-sensitive and macOS/Windows only being case-preserving, display as **File exists** problems in the GUI. These can be ignored. However, if they persist, you can report the issue.
- Synchronized file shares proactively reports temporary issues, which can result in occasional **Conflict** and **Problem** indicators appearing in the GUI during synchronization. These can be ignored. However, if they persist, you can report the issue.
- If you switch from WSL2 to Hyper-V on Windows, Docker Desktop needs to be fully restarted.
- POSIX-style Windows paths are not supported. Avoid setting the
  [COMPOSE_CONVERT_WINDOWS_PATHS](https://docs.docker.com/compose/how-tos/environment-variables/envvars/#compose_convert_windows_paths) environment variable in Docker Compose.
- If you don't have the correct permissions to create symbolic links and your container attempts to create symbolic links in your file share instance, an **unable to create symbolic link** error message displays. For Windows users, see Microsoft's [Create symbolic links documentation](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/security-policy-settings/create-symbolic-links) for best practices and location of the **Create symbolic links** security policy setting. For Mac and Linux users, check that you have write permissions on the folder.

---

# Using USB/IP with Docker Desktop

> How to use USB/IP in Docker Desktop

# Using USB/IP with Docker Desktop

   Table of contents

---

Requires: Docker Desktop
[4.35.0](https://docs.docker.com/desktop/release-notes/#4350) and later For: Docker Desktop for Mac, Linux, and Windows with the Hyper-V backend

USB/IP enables you to share USB devices over the network, which can then be accessed from within Docker containers. This page focuses on sharing USB devices connected to the machine you run Docker Desktop on. You can repeat the following process to attach and use additional USB devices as needed.

> Note
>
> Docker Desktop includes built-in drivers for many common USB devices but Docker can't guarantee every possible USB device works with this setup.

## Setup and use

### Step one: Run a USB/IP server

To use USB/IP, you need to run a USB/IP server. For this guide, the implementation provided by [jiegec/usbip](https://github.com/jiegec/usbip) will be used.

1. Clone the repository.
  ```console
  $ git clone https://github.com/jiegec/usbip
  $ cd usbip
  ```
2. Run the emulated Human Interface Device (HID) device example.
  ```console
  $ env RUST_LOG=info cargo run --example hid_keyboard
  ```

### Step two: Start a privileged Docker container

To attach the USB device, start a privileged Docker container with the PID namespace set to `host`:

```console
$ docker run --rm -it --privileged --pid=host alpine
```

`--privileged` gives the container full access to the host, and `--pid=host` allows it to share the host’s process namespace.

### Step three: Enter the mount namespace of PID 1

Inside the container, enter the mount namespace of the `init` process to gain access to the pre-installed USB/IP tools:

```console
$ nsenter -t 1 -m
```

### Step four: Use the USB/IP tools

Now you can use the USB/IP tools as you would on any other system:

#### List USB devices

To list exportable USB devices from the host:

```console
$ usbip list -r host.docker.internal
```

Expected output:

```console
Exportable USB devices
======================
 - host.docker.internal
      0-0-0: unknown vendor : unknown product (0000:0000)
           : /sys/bus/0/0/0
           : (Defined at Interface level) (00/00/00)
           :  0 - unknown class / unknown subclass / unknown protocol (03/00/00)
```

#### Attach a USB device

To attach a specific USB device, or the emulated keyboard in this case:

```console
$ usbip attach -r host.docker.internal -d 0-0-0
```

#### Verify device attachment

After attaching the emulated keyboard, check the `/dev/input` directory for the device node:

```console
$ ls /dev/input/
```

Example output:

```console
event0  mice
```

### Step five: Access the device from another container

While the initial container remains running to keep the USB device operational, you can access the attached device from another container. For example:

1. Start a new container with the attached device.
  ```console
  $ docker run --rm -it --device "/dev/input/event0" alpine
  ```
2. Install a tool like `evtest` to test the emulated keyboard.
  ```console
  $ apk add evtest
  $ evtest /dev/input/event0
  ```
3. Interact with the device, and observe the output.
  Example output:
  ```console
  Input driver version is 1.0.1
  Input device ID: bus 0x3 vendor 0x0 product 0x0 version 0x111
  ...
  Properties:
  Testing ... (interrupt to exit)
  Event: time 1717575532.881540, type 4 (EV_MSC), code 4 (MSC_SCAN), value 7001e
  Event: time 1717575532.881540, type 1 (EV_KEY), code 2 (KEY_1), value 1
  Event: time 1717575532.881540, -------------- SYN_REPORT ------------
  ...
  ```

> Important
>
> The initial container must remain running to maintain the connection to the USB device. Exiting the container will stop the device from working.

---

# Virtual Machine Manager for Docker Desktop on Mac

> Discover Docker Desktop for Mac's Virtual Machine Manager (VMM) options, including the new Docker VMM for Apple Silicon, offering enhanced performance and efficiency

# Virtual Machine Manager for Docker Desktop on Mac

   Table of contents

---

Docker Desktop supports multiple Virtual Machine Managers (VMMs) to power the Linux VM that runs containers. You can choose the most suitable option based on your system architecture (Intel or Apple Silicon), performance needs, and feature requirements. This page provides an overview of the available options.

To change the VMM, go to **Settings** > **General** > **Virtual Machine Manager**.

## Docker VMM

Requires: Docker Desktop
[4.35.0](https://docs.docker.com/desktop/release-notes/#4350) and later For: Docker Desktop on Mac with Apple Silicon

Docker VMM is a new, container-optimized hypervisor. By optimizing both the Linux kernel and hypervisor layers, Docker VMM delivers significant performance enhancements across common developer tasks.

Some key performance enhancements provided by Docker VMM include:

- Faster I/O operations: With a cold cache, iterating over a large shared filesystem with `find` is 2x faster than when the Apple Virtualization framework is used.
- Improved caching: With a warm cache, performance can improve by as much as 25x, even surpassing native Mac operations.

These improvements directly impact developers who rely on frequent file access and overall system responsiveness during containerized development. Docker VMM marks a significant leap in speed, enabling smoother workflows and faster iteration cycles.

> Note
>
> Docker VMM requires a minimum of 4GB of memory to be allocated to the Docker Linux VM. The memory needs to be increased before Docker VMM is enabled, and this can be done from the **Resources** tab in **Settings**.

### Known issues

As Docker VMM is still in Beta, there are a few known limitations:

- Docker VMM does not currently support Rosetta, so emulation of amd64 architectures is slow. Docker is exploring potential solutions.
- Certain databases, like MongoDB and Cassandra, may fail when using virtiofs with Docker VMM. This issue is expected to be resolved in a future release.

## Apple Virtualization framework

The Apple Virtualization framework is a stable and well-established option for managing virtual machines on Mac. It has been a reliable choice for many Mac users over the years. This framework is best suited for developers who prefer a proven solution with solid performance and broad compatibility.

## QEMU (Legacy) for Apple Silicon

> Note
>
> QEMU has been deprecated in versions 4.44 and later. For more information, see the [blog announcement](https://www.docker.com/blog/docker-desktop-for-mac-qemu-virtualization-option-to-be-deprecated-in-90-days/)

QEMU is a legacy virtualization option for Apple Silicon Macs, primarily supported for older use cases.

Docker recommends transitioning to newer alternatives, such as Docker VMM or the Apple Virtualization framework, as they offer superior performance and ongoing support. Docker VMM, in particular, offers substantial speed improvements and a more efficient development environment, making it a compelling choice for developers working with Apple Silicon.

Note that this is not related to using QEMU to emulate non-native architectures in
[multi-platform builds](https://docs.docker.com/build/building/multi-platform/#qemu).

## HyperKit (Legacy) for Intel-based Macs

> Note
>
> HyperKit will be deprecated in a future release.

HyperKit is another legacy virtualization option, specifically for Intel-based Macs. Like QEMU, it is still available but considered deprecated. Docker recommends switching to modern alternatives for better performance and to future-proof your setup.
