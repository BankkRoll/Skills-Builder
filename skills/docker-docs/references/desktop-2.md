# Wasm workloads and more

# Wasm workloads

> How to run Wasm workloads with Docker Desktop

# Wasm workloads

   Table of contents

---

Availability: Beta

> Important
>
> Wasm workloads will be deprecated and removed in a future Docker Desktop release. It is no longer actively maintained.

WebAssembly (Wasm) is a fast, light alternative to Linux and
Windows containers. With Docker Desktop, you can now run Wasm workloads side by side with traditional containers.

This page provides information about the ability to run Wasm applications
alongside your Linux containers in Docker.

> Tip
>
> Learn more about Wasm use cases and tradeoffs in the [Docker Wasm technical preview blog post](https://www.docker.com/blog/docker-wasm-technical-preview/).

## Turn on Wasm workloads

Wasm workloads require the [containerd image store](https://docs.docker.com/desktop/features/containerd/)
feature to be turned on. If you’re not already using the containerd image store,
then pre-existing images and containers will be inaccessible.

1. Navigate to **Settings** in Docker Desktop.
2. In the **General** tab, check **Use containerd for pulling and storing images**.
3. Go to **Features in development** and check the **Enable Wasm** option.
4. Select **Apply** to save the settings.
5. In the confirmation dialog, select **Install** to install the Wasm runtimes.

Docker Desktop downloads and installs the following runtimes:

- `io.containerd.slight.v1`
- `io.containerd.spin.v2`
- `io.containerd.wasmedge.v1`
- `io.containerd.wasmtime.v1`
- `io.containerd.lunatic.v1`
- `io.containerd.wws.v1`
- `io.containerd.wasmer.v1`

## Usage examples

### Running a Wasm application withdocker run

The following `docker run` command starts a Wasm container on your system:

```console
$ docker run \
  --runtime=io.containerd.wasmedge.v1 \
  --platform=wasi/wasm \
  secondstate/rust-example-hello
```

After running this command, you can visit [http://localhost:8080/](http://localhost:8080/) to see the "Hello world" output from this example module.

If you are receiving an error message, see the [troubleshooting section](#troubleshooting) for help.

Note the `--runtime` and `--platform` flags used in this command:

- `--runtime=io.containerd.wasmedge.v1`: Informs the Docker engine that you want
  to use the Wasm containerd shim instead of the standard Linux container
  runtime
- `--platform=wasi/wasm`: Specifies the architecture of the image you want to
  use. By leveraging a Wasm architecture, you don’t need to build separate
  images for the different machine architectures. The Wasm runtime takes care of
  the final step of converting the Wasm binary to machine instructions.

### Running a Wasm application with Docker Compose

The same application can be run using the following Docker Compose file:

```yaml
services:
  app:
    image: secondstate/rust-example-hello
    platform: wasi/wasm
    runtime: io.containerd.wasmedge.v1
```

Start the application using the normal Docker Compose commands:

```console
$ docker compose up
```

### Running a multi-service application with Wasm

Networking works the same as you'd expect with Linux containers, giving you the
flexibility to combine Wasm applications with other containerized workloads,
such as a database, in a single application stack.

In the following example, the Wasm application leverages a MariaDB database
running in a container.

1. Clone the repository.
  ```console
  $ git clone https://github.com/second-state/microservice-rust-mysql.git
  Cloning into 'microservice-rust-mysql'...
  remote: Enumerating objects: 75, done.
  remote: Counting objects: 100% (75/75), done.
  remote: Compressing objects: 100% (42/42), done.
  remote: Total 75 (delta 29), reused 48 (delta 14), pack-reused 0
  Receiving objects: 100% (75/75), 19.09 KiB | 1.74 MiB/s, done.
  Resolving deltas: 100% (29/29), done.
  ```
2. Navigate into the cloned project and start the project using Docker Compose.
  ```console
  $ cd microservice-rust-mysql
  $ docker compose up
  [+] Running 0/1
  ⠿ server Warning                                                                                                  0.4s
  [+] Building 4.8s (13/15)
  ...
  microservice-rust-mysql-db-1      | 2022-10-19 19:54:45 0 [Note] mariadbd: ready for connections.
  microservice-rust-mysql-db-1      | Version: '10.9.3-MariaDB-1:10.9.3+maria~ubu2204'  socket: '/run/mysqld/mysqld.sock'  port: 3306  mariadb.org binary distribution
  ```
  If you run `docker image ls` from another terminal window, you can see the
  Wasm image in your image store.
  ```console
  $ docker image ls
  REPOSITORY   TAG       IMAGE ID       CREATED         SIZE
  server       latest    2c798ddecfa1   2 minutes ago   3MB
  ```
  Inspecting the image shows the image has a `wasi/wasm` platform, a
  combination of OS and architecture:
  ```console
  $ docker image inspect server | grep -A 3 "Architecture"
          "Architecture": "wasm",
          "Os": "wasi",
          "Size": 3001146,
          "VirtualSize": 3001146,
  ```
3. Open the URL `http://localhost:8090` in a browser and create a few sample
  orders. All of these are interacting with the Wasm server.
4. When you're all done, tear everything down by hitting `Ctrl+C` in the
  terminal you launched the application.

### Building and pushing a Wasm module

1. Create a Dockerfile that builds your Wasm application.
  Exactly how to do this varies depending on the programming language you use.
2. In a separate stage in your `Dockerfile`, extract the module and set it as
  the `ENTRYPOINT`.
  ```dockerfile
  # syntax=docker/dockerfile:1
  FROM scratch
  COPY --from=build /build/hello_world.wasm /hello_world.wasm
  ENTRYPOINT [ "/hello_world.wasm" ]
  ```
3. Build and push the image specifying the `wasi/wasm` architecture. Buildx
  makes this easy to do in a single command.
  ```console
  $ docker buildx build --platform wasi/wasm -t username/hello-world .
  ...
  => exporting to image                                                                             0.0s
  => => exporting layers                                                                            0.0s
  => => exporting manifest sha256:2ca02b5be86607511da8dc688234a5a00ab4d58294ab9f6beaba48ab3ba8de56  0.0s
  => => exporting config sha256:a45b465c3b6760a1a9fd2eda9112bc7e3169c9722bf9e77cf8c20b37295f954b    0.0s
  => => naming to docker.io/username/hello-world:latest                                            0.0s
  => => unpacking to docker.io/username/hello-world:latest                                         0.0s
  $ docker push username/hello-world
  ```

## Troubleshooting

This section contains instructions on how to resolve common issues.

### Unknown runtime specified

If you try to run a Wasm container without the [containerd image
store](https://docs.docker.com/desktop/features/containerd/), an error similar to the following displays:

```text
docker: Error response from daemon: Unknown runtime specified io.containerd.wasmedge.v1.
```

[Turn on the containerd feature](https://docs.docker.com/desktop/features/containerd/#enable-the-containerd-image-store)
in Docker Desktop settings and try again.

### Failed to start shim: failed to resolve runtime path

If you use an older version of Docker Desktop that doesn't support running Wasm
workloads, you will see an error message similar to the following:

```text
docker: Error response from daemon: failed to start shim: failed to resolve runtime path: runtime "io.containerd.wasmedge.v1" binary not installed "containerd-shim-wasmedge-v1": file does not exist: unknown.
```

Update your Docker Desktop to the latest version and try again.

## Known issues

- Docker Compose may not exit cleanly when interrupted. As a workaround, clean up `docker-compose` processes by sending them a SIGKILL (`killall -9 docker-compose`).
- Pushes to Docker Hub might give an error stating `server message: insufficient_scope: authorization failed`, even after signing in through Docker Desktop. As a workaround, run `docker login` in the CLI

---

# Best practices

> Best practices for using Docker Desktop with WSL 2

# Best practices

---

- Always use the latest version of WSL. At a minimum you must use WSL version 2.1.5, otherwise Docker Desktop may not work as expected. Testing, development, and documentation is based on the newest kernel versions. Older versions of WSL can cause:
  - Docker Desktop to hang periodically or when upgrading
  - Deployment via SCCM to fail
  - The `vmmem.exe` to consume all memory
  - Network filter policies to be applied globally, not to specific objects
  - GPU failures with containers
- To get the best out of the file system performance when bind-mounting files, it's recommended that you store source code and other data that is bind-mounted into Linux containers. For instance, use `docker run -v <host-path>:<container-path>` in the Linux file system, rather than the Windows file system. You can also refer to the [recommendation](https://learn.microsoft.com/en-us/windows/wsl/compare-versions) from Microsoft.
  - Linux containers only receive file change events, “inotify events”, if the original files are stored in the Linux filesystem. For example, some web development workflows rely on inotify events for automatic reloading when files have changed.
  - Performance is much higher when files are bind-mounted from the Linux filesystem, rather than remoted from the Windows host. Therefore avoid `docker run -v /mnt/c/users:/users,` where `/mnt/c` is mounted from Windows.
  - Instead, from a Linux shell use a command like `docker run -v ~/my-project:/sources <my-image>` where `~` is expanded by the Linux shell to `$HOME`.
- If you have concerns about the size of the `docker-desktop-data` distribution, take a look at the [WSL tooling built into Windows](https://learn.microsoft.com/en-us/windows/wsl/disk-space).
  - Installations of Docker Desktop version 4.30 and later no longer rely on the `docker-desktop-data` distribution; instead Docker Desktop creates and manages its own virtual hard disk (VHDX) for storage. (note, however, that Docker Desktop keeps using the `docker-desktop-data` distribution if it was already created by an earlier version of the software).
  - Starting from version 4.34 and later, Docker Desktop automatically manages the size of the managed VHDX and returns unused space to the operating system.
- If you have concerns about CPU or memory usage, you can configure limits on the memory, CPU, and swap size allocated to the [WSL 2 utility VM](https://learn.microsoft.com/en-us/windows/wsl/wsl-config#global-configuration-options-with-wslconfig).

---

# Custom kernels on WSL

> Using custom kernels with Docker Desktop on WSL 2

# Custom kernels on WSL

---

Docker Desktop depends on several kernel features built into the default
WSL 2 Linux kernel distributed by Microsoft. Consequently, using a
custom kernel with Docker Desktop on WSL 2 is not officially supported
and may cause issues with Docker Desktop startup or operation.

However, in some cases it may be necessary
to run custom kernels; Docker Desktop does not block their use, and
some users have reported success using them.

If you choose to use a custom kernel, it is recommended you start
from the kernel tree distributed by Microsoft from their [official
repository](https://github.com/microsoft/WSL2-Linux-Kernel) and then add
the features you need on top of that.

It's also recommended that you:

- Use the same kernel version as the one distributed by the latest WSL2
  release. You can find the version by running `wsl.exe --system uname -r`
  in a terminal.
- Start from the default kernel configuration as provided by Microsoft
  from their [repository](https://github.com/microsoft/WSL2-Linux-Kernel)
  and add the features you need on top of that.
- Make sure that your kernel build environment includes `pahole` and
  its version is properly reflected in the corresponding kernel config
  (`CONFIG_PAHOLE_VERSION`).

---

# Use WSL

> How to develop with Docker and WSL 2 and understand GPU support for WSL

# Use WSL

   Table of contents

---

The following section describes how to start developing your applications using Docker and WSL 2. We recommend that you have your code in your default Linux distribution for the best development experience using Docker and WSL 2. After you have turned on the WSL 2 feature on Docker Desktop, you can start working with your code inside the Linux distribution and ideally with your IDE still in Windows. This workflow is straightforward if you are using [VS Code](https://code.visualstudio.com/download).

## Develop with Docker and WSL 2

1. Open VS Code and install the [Remote - WSL](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-wsl) extension. This extension lets you work with a remote server in the Linux distribution and your IDE client still on Windows.
2. Open your terminal and type:
  ```console
  $ wsl
  ```
3. Navigate to your project directory and then type:
  ```console
  $ code .
  ```
  This opens a new VS Code window connected remotely to your default Linux distribution which you can check in the bottom corner of the screen.

Alternatively, you can open your default Linux distribution from the **Start** menu, navigate to your project directory, and then run `code .`

---

# Docker Desktop WSL 2 backend on Windows

> Turn on the Docker WSL 2 backend and get to work using best practices, GPU support, and more in this thorough guide.

# Docker Desktop WSL 2 backend on Windows

   Table of contents

---

Windows Subsystem for Linux (WSL) 2 is a full Linux kernel built by Microsoft, which lets Linux distributions run without managing virtual machines. With Docker Desktop running on WSL 2, users can leverage Linux workspaces and avoid maintaining both Linux and Windows build scripts. In addition, WSL 2 provides improvements to file system sharing and boot time.

Docker Desktop uses the dynamic memory allocation feature in WSL 2 to improve the resource consumption. This means Docker Desktop only uses the required amount of CPU and memory resources it needs, while allowing CPU and memory-intensive tasks such as building a container, to run much faster.

Additionally, with WSL 2, the time required to start a Docker daemon after a cold start is significantly faster.

## Prerequisites

Before you turn on the Docker Desktop WSL 2 feature, ensure you have:

- At a minimum WSL version 2.1.5, but ideally the latest version of WSL to [avoid Docker Desktop not working as expected](https://docs.docker.com/desktop/features/wsl/best-practices/).
- Met the Docker Desktop for Windows'
  [system requirements](https://docs.docker.com/desktop/setup/install/windows-install/#system-requirements).
- Installed the WSL 2 feature on Windows. For detailed instructions, refer to the [Microsoft documentation](https://docs.microsoft.com/en-us/windows/wsl/install-win10).

> Tip
>
> For a better experience on WSL, consider enabling the WSL
> [autoMemoryReclaim](https://learn.microsoft.com/en-us/windows/wsl/wsl-config#experimental-settings)
> setting available since WSL 1.3.10 (experimental).
>
>
>
> This feature enhances the Windows host's ability to reclaim unused memory within the WSL virtual machine, ensuring improved memory availability for other host applications. This capability is especially beneficial for Docker Desktop, as it prevents the WSL VM from retaining large amounts of memory (in GBs) within the Linux kernel's page cache during Docker container image builds, without releasing it back to the host when no longer needed within the VM.

## Turn on Docker Desktop WSL 2

> Important
>
> To avoid any potential conflicts with using WSL 2 on Docker Desktop, you must uninstall any previous versions of Docker Engine and CLI installed directly through Linux distributions before installing Docker Desktop.

1. Download and install the latest version of [Docker Desktop for Windows](https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-windows).
2. Follow the usual installation instructions to install Docker Desktop. Depending on which version of Windows you are using, Docker Desktop may prompt you to turn on WSL 2 during installation. Read the information displayed on the screen and turn on the WSL 2 feature to continue.
3. Start Docker Desktop from the **Windows Start** menu.
4. Navigate to **Settings**.
5. From the **General** tab, select **Use WSL 2 based engine**..
  If you have installed Docker Desktop on a system that supports WSL 2, this option is turned on by default.
6. Select **Apply**.

Now `docker` commands work from Windows using the new WSL 2 engine.

> Tip
>
> By default, Docker Desktop stores the data for the WSL 2 engine at `C:\Users\[USERNAME]\AppData\Local\Docker\wsl`.
> If you want to change the location, for example, to another drive you can do so via the `Settings -> Resources -> Advanced` page from the Docker Dashboard.
> Read more about this and other Windows settings at
> [Changing settings](https://docs.docker.com/desktop/settings-and-maintenance/settings/)

## Enabling Docker support in WSL 2 distributions

WSL 2 adds support for "Linux distributions" to Windows, where each distribution behaves like a VM except they all run on top of a single shared Linux kernel.

Docker Desktop does not require any particular Linux distributions to be installed. The `docker` CLI and UI all work fine from Windows without any additional Linux distributions. However for the best developer experience, we recommend installing at least one additional distribution and enable Docker support:

1. Ensure the distribution runs in WSL 2 mode. WSL can run distributions in both v1 or v2 mode.
  To check the WSL mode, run:
  ```console
  $ wsl.exe -l -v
  ```
  To upgrade the Linux distribution to v2, run:
  ```console
  $ wsl.exe --set-version (distribution name) 2
  ```
  To set v2 as the default version for future installations, run:
  ```console
  $ wsl.exe --set-default-version 2
  ```
2. When Docker Desktop starts, go to **Settings** > **Resources** > **WSL Integration**.
  The Docker-WSL integration is enabled on the default WSL distribution, which is [Ubuntu](https://learn.microsoft.com/en-us/windows/wsl/install). To change your default WSL distribution, run:
  ```console
  $ wsl.exe --set-default <distribution name>
  ```
  If **WSL integrations** isn't available under **Resources**, Docker may be in Windows container mode. In your taskbar, select the Docker menu and then **Switch to Linux containers**.
3. Select **Apply**.

> Note
>
> With Docker Desktop version 4.30 and earlier, Docker Desktop installed two special-purpose internal Linux distributions `docker-desktop` and `docker-desktop-data`. `docker-desktop` is used to run the Docker engine `dockerd`, while `docker-desktop-data` stores containers and images. Neither can be used for general development.
>
>
>
> With fresh installations of Docker Desktop 4.30 and later, `docker-desktop-data` is no longer created. Instead, Docker Desktop creates and
> manages its own virtual hard disk for storage. The `docker-desktop` distribution is still created and used to run the Docker engine.
>
>
>
> Note that Docker Desktop version 4.30 and later keeps using the `docker-desktop-data` distribution if it was already created by an earlier version of Docker Desktop and has not been freshly installed or factory reset.

## WSL 2 security in Docker Desktop

Docker Desktop’s WSL 2 integration operates within the existing security model of WSL and does not introduce additional security risks beyond standard WSL behavior.

Docker Desktop runs within its own dedicated WSL distribution, `docker-desktop`, which follows the same isolation properties as any other WSL distribution. The only interaction between Docker Desktop and other installed WSL distributions occurs when the Docker Desktop **WSL integration** feature is enabled in settings. This feature allows easy access to the Docker CLI from integrated distributions.

WSL is designed to facilitate interoperability between Windows and Linux environments. Its file system is accessible from the Windows host `\\wsl$`, meaning Windows processes can read and modify files within WSL. This behavior is not specific to Docker Desktop, but rather a core aspect of WSL itself.

For organizations concerned about security risks related to WSL and want stricter isolation and security controls, run Docker Desktop in Hyper-V mode instead of WSL 2. Alternatively, run your container workloads with
[Enhanced Container Isolation](https://docs.docker.com/enterprise/security/hardened-desktop/enhanced-container-isolation/) enabled.

## Additional resources

- [Explore best practices](https://docs.docker.com/desktop/features/wsl/best-practices/)
- [Understand how to develop with Docker and WSL 2](https://docs.docker.com/desktop/features/wsl/use-wsl/)
- [Learn about GPU support with WSL 2](https://docs.docker.com/desktop/features/gpu/)
- [Custom kernels on WSL](https://docs.docker.com/desktop/features/wsl/custom-kernels/)
