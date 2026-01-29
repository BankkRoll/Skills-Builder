# How to back up and restore your Docker Desktop data and more

# How to back up and restore your Docker Desktop data

# How to back up and restore your Docker Desktop data

   Table of contents

---

Use this procedure to back up and restore your images and container data. This is useful if you want to reset your VM disk or to move your Docker environment to a new computer, or recover from a failed Docker Desktop update or installation.

> Important
>
> If you use volumes or bind-mounts to store your container data, backing up your containers may not be needed, but make sure to remember the options that were used when creating the container or use a
> [Docker Compose file](https://docs.docker.com/reference/compose-file/) if you want to re-create your containers with the same configuration after re-installation.

## If Docker Desktop is functioning normally

### Save your data

1. Commit your containers to an image with
  [docker container commit](https://docs.docker.com/reference/cli/docker/container/commit/).
  Committing a container stores filesystem changes and some container configurations, such as labels and environment variables, as a local image. Be aware that environment variables may contain sensitive
  information such as passwords or proxy-authentication, so take care when pushing the resulting image to a registry.
  Also note that filesystem changes in a volume that are attached to the
  container are not included in the image, and must be backed up separately.
  If you used a
  [named volume](https://docs.docker.com/engine/storage/#more-details-about-mount-types) to store container data, such as databases, refer to the
  [back up, restore, or migrate data volumes](https://docs.docker.com/engine/storage/volumes/#back-up-restore-or-migrate-data-volumes) page in the storage section.
2. Use
  [docker push](https://docs.docker.com/reference/cli/docker/image/push/) to push any
  images you have built locally and want to keep to the
  [Docker Hub registry](https://docs.docker.com/docker-hub/).
  > Tip
  >
  > [Set the repository visibility to private](https://docs.docker.com/docker-hub/repos/) if your image includes sensitive content.
  Alternatively, use
  [docker image save -o images.tar image1 [image2 ...]](https://docs.docker.com/reference/cli/docker/image/save/)
  to save any images you want to keep to a local `.tar` file.

After backing up your data, you can uninstall the current version of Docker Desktop
and
[install a different version](https://docs.docker.com/desktop/release-notes/) or reset Docker Desktop to factory defaults.

### Restore your data

1. Load your images.
  - If you pushed to Docker Hub:
    ```console
    $ docker pull <my-backup-image>
    ```
  - If you saved a `.tar` file:
    ```console
    $ docker image load -i images.tar
    ```
2. Re-create your containers if needed, using
  [docker run](https://docs.docker.com/reference/cli/docker/container/run/),
  or
  [Docker Compose](https://docs.docker.com/compose/).

To restore volume data, refer to
[backup, restore, or migrate data volumes](https://docs.docker.com/engine/storage/volumes/#back-up-restore-or-migrate-data-volumes).

## If Docker Desktop fails to start

If Docker Desktop cannot launch and must be reinstalled, you can back up its VM disk and image data directly from disk. Docker Desktop must be fully stopped before backing up these files.

1. Back up Docker containers/images.
  Backup the following file:
  ```console
  %LOCALAPPDATA%\Docker\wsl\data\docker_data.vhdx
  ```
  Copy it to a safe location.
2. Back up WSL distributions.
  If you're running any WSL Linux distributions (Ubuntu, Alpine, etc.), back them up using [Microsoft's guide](https://learn.microsoft.com/en-us/windows/wsl/faq#how-can-i-back-up-my-wsl-distributions-).
3. Restore.
  After reinstalling Docker Desktop, restore the `docker_data.vhdx` to the same location and re-import your WSL distributions if needed.

1. Back up Docker containers/images.
  Backup the following file:
  ```console
  ~/Library/Containers/com.docker.docker/Data/vms/0/data/Docker.raw
  ```
  Copy it to a safe location.
2. Restore.
  After reinstalling Docker Desktop, restore the `Docker.raw` to the same location.

1. Back up Docker containers/images:
  Backup the following file:
  ```console
  ~/.docker/desktop/vms/0/data/Docker.raw
  ```
  Copy it to a safe location.
2. Restore.
  After reinstalling Docker Desktop, restore the `Docker.raw` to the same location.

---

# Change your Docker Desktop settings

> Learn about and change Docker Desktop's settings

# Change your Docker Desktop settings

   Table of contents

---

To navigate to **Settings** either:

- Select the Docker menu
  ![whale menu](https://docs.docker.com/desktop/images/whale-x.svg)
  and then **Settings**
- Select the **Settings** icon from the Docker Desktop Dashboard.

You can also locate the `settings-store.json` file (or `settings.json` for Docker Desktop versions 4.34 and earlier) at:

- Mac: `~/Library/Group\ Containers/group.com.docker/settings-store.json`
- Windows: `C:\Users\[USERNAME]\AppData\Roaming\Docker\settings-store.json`
- Linux: `~/.docker/desktop/settings-store.json`

For additional information on settings that can be set in the Docker Desktop Dashboard and by administrators via the Admin Console, see the
[Settings reference](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/settings-reference/).

## General

On the **General** tab, you can configure when to start Docker and specify other settings:

- **Start Docker Desktop when you sign in to your computer**. Select to automatically start Docker
  Desktop when you sign in to your machine.
- **Open Docker Dashboard when Docker Desktop starts**. Select to automatically open the
  dashboard when starting Docker Desktop.
- **Choose theme for Docker Desktop**. Choose whether you want to apply a **Light** or **Dark** theme to Docker Desktop. Alternatively you can set Docker Desktop to **Use system settings**.
- **Configure shell completions**. Automatically edits your shell configuration and gives you word completion for commands, flags, and Docker objects (such as container and volume names) when you hit `<Tab>` as you type into your terminal. For more information, see
  [Completion](https://docs.docker.com/engine/cli/completion/).
- **Choose container terminal**. Determines which terminal is launched when opening the terminal from a container.
  If you choose the integrated terminal, you can run commands in a running container straight from the Docker Desktop Dashboard. For more information, see
  [Explore containers](https://docs.docker.com/desktop/use-desktop/container/).
- **Enable Docker terminal**. Interact with your host machine and execute commands directly from Docker Desktop.
- **Enable Docker Debug by default**. Check this option to use Docker Debug by default when accessing the integrated terminal. For more information, see
  [Explore containers](https://docs.docker.com/desktop/use-desktop/container/#integrated-terminal).
- Mac only
  **Include VM in Time Machine backups**. Select to back up the Docker Desktop
  virtual machine. This option is turned off by default.
- **Use containerd for pulling and storing images**.
  Turns on the containerd image store.
  This brings new features like faster container startup performance by lazy-pulling images,
  and the ability to run Wasm applications with Docker.
  For more information, see
  [containerd image store](https://docs.docker.com/desktop/features/containerd/).
- Windows only
  **Expose daemon on tcp://localhost:2375 without TLS**. Check this option to
  enable legacy clients to connect to the Docker daemon. You must use this option
  with caution as exposing the daemon without TLS can result in remote code
  execution attacks.
- Windows only
  **Use the WSL 2 based engine**. WSL 2 provides better performance than the
  Hyper-V backend. For more information, see
  [Docker Desktop WSL 2 backend](https://docs.docker.com/desktop/features/wsl/).
- Windows only
  **Add the*.docker.internalnames to the host's/etc/hostsfile (Password required)**. Lets you resolve `*.docker.internal` DNS names from both the host and your containers.
- Mac only
  **Choose Virtual Machine Manager (VMM)**. Choose the Virtual Machine Manager for creating and managing the Docker Desktop Linux VM.
  - Select **Docker VMM** for the latest and most performant Hypervisor/Virtual Machine Manager. This option is available only on Apple Silicon Macs running macOS 12.5 or later and is currently in Beta.
    > Tip
    >
    > Turn this setting on to make Docker Desktop run faster.
  - Alternatively, you can choose **Apple Virtualization framework**, **QEMU** (for Apple Silicon in Docker Desktop version 4.43 and earlier), or **HyperKit** (for Intel Macs). For macOS 12.5 and later, Apple Virtualization framework is the default setting.
  For more information, see
  [Virtual Machine Manager](https://docs.docker.com/desktop/features/vmm/).
- Mac only
  **Choose file sharing implementation for your containers**. Choose whether you want to share files using **VirtioFS**, **gRPC FUSE**, or **osxfs (Legacy)**. VirtioFS is only available for macOS 12.5 and later, and is turned on by default.
  > Tip
  >
  > Use VirtioFS for speedy file sharing. VirtioFS has reduced the time taken to complete filesystem operations by [up to 98%](https://github.com/docker/roadmap/issues/7#issuecomment-1044452206). It is the only file sharing implementation supported by Docker VMM.
- Mac only
  **Use Rosetta for x86_64/amd64 emulation on Apple Silicon**. Turns on Rosetta to accelerate x86/AMD64 binary emulation on Apple Silicon. This option is only available if you have selected **Apple Virtualization framework** as the Virtual Machine Manager. You must also be on macOS 13 or later.
- **Send usage statistics**. Select so Docker Desktop sends diagnostics,
  crash reports, and usage data. This information helps Docker improve and
  troubleshoot the application. Clear the checkbox to opt out. Docker may
  periodically prompt you for more information.
- **Use Enhanced Container Isolation**. Select to enhance security by preventing containers from breaching the Linux VM. For more information, see
  [Enhanced Container Isolation](https://docs.docker.com/enterprise/security/hardened-desktop/enhanced-container-isolation/).
  > Note
  >
  > This setting is only available if you are signed in to Docker Desktop and have a Docker Business subscription.
- **Show CLI hints**. Displays CLI hints and tips when running Docker commands in the CLI. This is turned on by default. To turn CLI hints on or off from the CLI, set `DOCKER_CLI_HINTS` to `true` or `false` respectively.
- **Enable Scout image analysis**. When this option is enabled, inspecting an image in Docker Desktop shows a **Start analysis** button that, when selected, analyzes the image with Docker Scout.
- **Enable background SBOM indexing**. When this option is enabled, Docker Scout automatically analyzes images that you build or pull.
- Mac only
  **Automatically check configuration**. Regularly checks your configuration to ensure no unexpected changes have been made by another application.
  Docker Desktop checks if your setup, configured during installation, has been altered by external apps like Orbstack. Docker Desktop checks:
  - The symlinks of Docker binaries to `/usr/local/bin`.
  - The symlink of the default Docker socket.
    Additionally, Docker Desktop ensures that the context is switched to `desktop-linux` on startup.
  You are notified if changes are found and are able to restore the configuration directly from the notification. For more information, see the
  [FAQs](https://docs.docker.com/desktop/troubleshoot-and-support/faqs/macfaqs/#why-do-i-keep-getting-a-notification-telling-me-an-application-has-changed-my-desktop-configurations).

## Resources

The **Resources** tab allows you to configure CPU, memory, disk, proxies,
network, and other resources.

### Advanced

> Note
>
> On Windows, the **Resource allocation** options in the **Advanced** tab are only available in Hyper-V mode, because Windows manages
> the resources in WSL 2 mode and Windows container mode. In WSL 2
> mode, you can configure limits on the memory, CPU, and swap size allocated
> to the [WSL 2 utility VM](https://docs.microsoft.com/en-us/windows/wsl/wsl-config#configure-global-options-with-wslconfig).

On the **Advanced** tab, you can limit resources available to the Docker Linux VM.

Advanced settings are:

- **CPU limit**. Specify the maximum number of CPUs to be used by Docker Desktop.
  By default, Docker Desktop is set to use all the processors available on the host machine.
- **Memory limit**. By default, Docker Desktop is set to use up to 50% of your host's
  memory. To increase the RAM, set this to a higher number; to decrease it,
  lower the number.
- **Swap**. Configure swap file size as needed. The default is 1 GB.
- **Disk usage limit**. Specify the maximum amount of disk space the engine can use.
- **Disk image location**. Specify the location of the Linux volume where containers and images are stored.
  You can also move the disk image to a different location. If you attempt to
  move a disk image to a location that already has one, you are asked if you
  want to use the existing image or replace it.

> Tip
>
> If you feel Docker Desktop starting to get slow or you're running
> multi-container workloads, increase the memory and disk image space allocation

- **Resource Saver**. Enable or disable
  [Resource Saver mode](https://docs.docker.com/desktop/use-desktop/resource-saver/),
  which significantly reduces CPU and memory utilization on the host by
  automatically turning off the Linux VM when Docker Desktop is idle (i.e., no
  containers are running).
  You can also configure the Resource Saver timeout which indicates how long
  should Docker Desktop be idle before Resource Saver mode kicks in. Default is
  5 minutes.
  > Note
  >
  > Exit from Resource Saver mode occurs automatically when containers run. Exit
  > may take a few seconds (~3 to 10 secs) as Docker Desktop restarts the Linux VM.

### File sharing

> Note
>
> On Windows, the **File sharing** tab is only available in Hyper-V mode because the files
> are automatically shared in WSL 2 mode and Windows container mode.

Use File sharing to allow local directories on your machine to be shared with
Linux containers. This is especially useful for editing source code in an IDE on
the host while running and testing the code in a container.

#### Synchronized file shares

Synchronized file shares is an alternative file sharing mechanism that provides fast and flexible host-to-VM file sharing, enhancing bind mount performance through the use of synchronized filesystem caches. Available with Pro, Team, and Business subscriptions.

To learn more, see
[Synchronized file share](https://docs.docker.com/desktop/features/synchronized-file-sharing/).

#### Virtual file shares

By default the `/Users`, `/Volumes`, `/private`, `/tmp` and `/var/folders` directory are shared.
If your project is outside this directory then it must be added to the list,
otherwise you may get `Mounts denied` or `cannot start service` errors at runtime.

File share settings are:

- **Add a Directory**. Select `+` and navigate to the directory you want to add.
- **Remove a Directory**. Select `-` next to the directory you want to remove
- **Apply** makes the directory available to containers using Docker's
  bind mount (`-v`) feature.

> Tip
>
> - Share only the directories that you need with the container. File sharing
>   introduces overhead as any changes to the files on the host need to be notified
>   to the Linux VM. Sharing too many files can lead to high CPU load and slow
>   filesystem performance.
> - Shared folders are designed to allow application code to be edited
>   on the host while being executed in containers. For non-code items
>   such as cache directories or databases, the performance will be much
>   better if they are stored in the Linux VM, using a
>   [data volume](https://docs.docker.com/engine/storage/volumes/)
>   (named volume) or
>   [data container](https://docs.docker.com/engine/storage/volumes/).
> - If you share the whole of your home directory into a container, MacOS may
>   prompt you to give Docker access to personal areas of your home directory such as
>   your Reminders or Downloads.
> - By default, Mac file systems are case-insensitive while Linux is case-sensitive.
>   On Linux, it is possible to create two separate files: `test` and `Test`,
>   while on Mac these filenames would actually refer to the same underlying
>   file. This can lead to problems where an app works correctly on a developer's
>   machine (where the file contents are shared) but fails when run in Linux in
>   production (where the file contents are distinct). To avoid this, Docker Desktop
>   insists that all shared files are accessed as their original case. Therefore,
>   if a file is created called `test`, it must be opened as `test`. Attempts to
>   open `Test` will fail with the error "No such file or directory". Similarly,
>   once a file called `test` is created, attempts to create a second file called
>   `Test` will fail.
>
>
>
> For more information, see
> [Volume mounting requires file sharing for any project directories outside of/Users](https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/topics/)

#### Shared folders on demand

On Windows, you can share a folder "on demand" the first time a particular folder is used by a container.

If you run a Docker command from a shell with a volume mount (as shown in the
example below) or kick off a Compose file that includes volume mounts, you get a
popup asking if you want to share the specified folder.

You can select to **Share it**, in which case it is added to your Docker Desktop Shared Folders list and available to
containers. Alternatively, you can opt not to share it by selecting **Cancel**.

![Shared folder on demand](https://docs.docker.com/desktop/images/shared-folder-on-demand.png)  ![Shared folder on demand](https://docs.docker.com/desktop/images/shared-folder-on-demand.png)

### Proxies

Docker Desktop supports the use of HTTP/HTTPS and SOCKS5 proxies (Requires a business subscription).

HTTP/HTTPS and SOCKS5 proxies can be used when:

- Signing in to Docker
- Pulling or pushing images
- Fetching artifacts during image builds
- Containers interact with the external network
- Scanning images

For more details on how it works, see
[Using Docker Desktop with a proxy](https://docs.docker.com/desktop/features/networking/#useing-docker-desktop-with-a-proxy).

If the host uses a HTTP/HTTPS proxy configuration (static or via Proxy Auto-Configuration (PAC)), Docker Desktop reads
this configuration
and automatically uses these settings for signing in to Docker, for pulling and pushing images, and for
container Internet access. If the proxy requires authorization then Docker Desktop dynamically asks
the developer for a username and password. All passwords are stored securely in the OS credential store.
Note that only the `Basic` proxy authentication method is supported so we recommend using an `https://`
URL of your HTTP/HTTPS proxies to protect passwords while in transit on the network. Docker Desktop
supports TLS 1.3 when communicating with proxies.

To set a different proxy for Docker Desktop, turn on **Manual proxy configuration** and enter a single
upstream proxy URL of the form `http://proxy:port` or `https://proxy:port`.

To prevent developers from accidentally changing the proxy settings, see
[Settings Management](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/#what-features-can-i-configure-with-settings-management).

The HTTPS proxy settings used for scanning images are set using the `HTTPS_PROXY` environment variable.

> Note
>
> If you are using a PAC file hosted on a web server, make sure to add the MIME type `application/x-ns-proxy-autoconfig` for the `.pac` file extension on the server or website. Without this configuration, the PAC file may not be parsed correctly. For more details on PAC files and Docker Desktop, see
> [Hardened Docker Desktop](https://docs.docker.com/enterprise/security/hardened-desktop/air-gapped-containers/#proxy-auto-configuration-files)

> Important
>
> You cannot configure the proxy settings using the Docker daemon configuration
> file (`daemon.json`), and we recommend you do not configure the proxy
> settings via the Docker CLI configuration file (`config.json`).
>
>
>
> To manage proxy configurations for Docker Desktop, configure the settings in
> the Docker Desktop app or use
> [Settings Management](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/).

#### Proxy authentication

##### Basic authentication

If your proxy uses Basic authentication, Docker Desktop prompts developers for a username and password and caches the credentials. All passwords are stored securely in the OS credential store. It will request re-authentication if that cache is removed.

It's recommended that you use an `https://` URL of HTTP/HTTPS proxies to protect passwords during network transit. Docker Desktop also supports TLS 1.3 for communication with proxies.

##### Kerberos and NTLM authentication

> Note
>
> Available for Docker Business subscribers with Docker Desktop for Windows version 4.30 and later.

Developers are no longer interrupted by prompts for proxy credentials as authentication is centralized. This also reduces the risk of account lockouts due to incorrect sign in attempts.

If your proxy offers multiple authentication schemes in 407 (Proxy Authentication Required) response, Docker Desktop by default selects the Basic authentication scheme.

For Docker Desktop version 4.30 to 4.31:

To enable Kerberos or NTLM proxy authentication, no additional configuration is needed beyond specifying the proxy IP address and port.

For Docker Desktop version 4.32 and later:

To enable Kerberos or NTLM proxy authentication you must pass the `--proxy-enable-kerberosntlm` installer flag during installation via the command line, and ensure your proxy server is properly configured for Kerberos or NTLM authentication.

### Network

> Note
>
> On Windows, the **Network** tab isn't available in the Windows container mode because
> Windows manages networking.

Docker Desktop uses a private IPv4 network for internal services such as a DNS server and an HTTP proxy. In case Docker Desktop's choice of subnet clashes with IPs in your environment, you can specify a custom subnet using the **Network** setting.

On Windows and Mac, you can also set the default networking mode and DNS resolution behavior. For more information, see
[Networking](https://docs.docker.com/desktop/features/networking/#networking-mode-and-dns-behaviour-for-mac-and-windows).

On Mac, you can also select the **Use kernel networking for UDP** setting. This lets you use a more efficient kernel networking path for UDP. This may not be compatible with your VPN software.

You can also define the behavior of port bindings. By default Docker Desktop binds all ports on containers to `0.0.0.0` on the host, though this can be overridden by providing a specific IP. You can change this default behavior by changing the **Port binding behavior** setting, allowing you to either bind to `localhost` (`127.0.0.1`) by default, or only allow containers to bind to `localhost` under any circumstances, even if requested otherwise.

### WSL Integration

On Windows in WSL 2 mode, you can configure which WSL 2 distributions will have the Docker
WSL integration.

By default, the integration is enabled on your default WSL distribution.
To change your default WSL distribution, run `wsl --set-default <distribution name>`. (For example,
to set Ubuntu as your default WSL distribution, run `wsl --set-default ubuntu`).

You can also select any additional distributions you would like to enable the WSL 2 integration on.

For more details on configuring Docker Desktop to use WSL 2, see
[Docker Desktop WSL 2 backend](https://docs.docker.com/desktop/features/wsl/).

## Docker Engine

The **Docker Engine** tab allows you to configure the Docker daemon used to run containers with Docker Desktop.

You configure the daemon using a JSON configuration file. Here's what the file might look like:

```json
{
  "builder": {
    "gc": {
      "defaultKeepStorage": "20GB",
      "enabled": true
    }
  },
  "experimental": false
}
```

You can find this file at `$HOME/.docker/daemon.json`. To change the configuration, either
edit the JSON configuration directly from the dashboard in Docker Desktop, or open and
edit the file using your favorite text editor.

To see the full list of possible configuration options, see the
[dockerd command reference](https://docs.docker.com/reference/cli/dockerd/).

Select **Apply** to save your settings.

## Builders

If you have turned on the
[Docker Desktop Builds view](https://docs.docker.com/desktop/use-desktop/builds/), you can use the
**Builders** tab to inspect and manage builders in the Docker Desktop settings.

### Inspect

To inspect builders, find the builder that you want to inspect and select the
expand icon. You can only inspect active builders.

Inspecting an active builder shows:

- BuildKit version
- Status
- Driver type
- Supported capabilities and platforms
- Disk usage
- Endpoint address

### Select a different builder

The **Selected builder** section displays the selected builder.
To select a different builder:

1. Find the builder that you want to use under **Available builders**
2. Open the drop-down menu next to the builder's name.
3. Select **Use** to switch to this builder.

Your build commands now use the selected builder by default.

### Create a builder

To create a builder, use the Docker CLI. See
[Create a new builder](https://docs.docker.com/build/builders/manage/#create-a-new-builder)

### Remove a builder

You can remove a builder if:

- The builder isn't your
  [selected builder](https://docs.docker.com/build/builders/#selected-builder)
- The builder isn't
  [associated with a Docker context](https://docs.docker.com/build/builders/#default-builder).
  To remove builders associated with a Docker context, remove the context using
  the `docker context rm` command.

To remove a builder:

1. Find the builder that you want to remove under **Available builders**
2. Open the drop-down menu.
3. Select **Remove** to remove this builder.

If the builder uses the `docker-container` or `kubernetes` driver,
the build cache is also removed, along with the builder.

### Stop and start a builder

Builders that use the
[docker-containerdriver](https://docs.docker.com/build/builders/drivers/docker-container/)
run the BuildKit daemon in a container.
You can start and stop the BuildKit container using the drop-down menu.

Running a build automatically starts the container if it's stopped.

You can only start and stop builders using the `docker-container` driver.

## Kubernetes

> Note
>
> On Windows the **Kubernetes** tab is not available in Windows container mode.

Docker Desktop includes a standalone Kubernetes server, so that you can test
deploying your Docker workloads on Kubernetes. To turn on Kubernetes support and
install a standalone instance of Kubernetes running as a Docker container,
select **Enable Kubernetes**. This can also be done from the **Kubernetes** view.

You can choose your cluster provisioning method:

- **Kubeadm** creates a single-node cluster and the version is set by Docker Desktop.
- **kind** creates a multi-node cluster and you can set the version and number of nodes.

Select **Show system containers (advanced)** to view internal containers when
using Docker commands.

Select **Reset Kubernetes cluster** to delete all stacks and Kubernetes resources.

For more information about using the Kubernetes integration with Docker Desktop,
see
[Explore the Kubernetes view](https://docs.docker.com/desktop/use-desktop/kubernetes/).

## Software updates

The **Software updates** tab lets you manage your Docker Desktop updates.
When there's a new update, you can choose to download the update right away, or
select the **Release Notes** option to learn what's included in the updated version.

The **Automatically check for updates** setting notifies you of any updates available to Docker Desktop in the Docker menu and the footer of the Docker Desktop Dashboard. This is turned on by default.

To allow Docker Desktop to automatically download new updates in the background,
select **Always download updates**. This downloads newer versions of Docker Desktop
when an update becomes available. After downloading the update, select
**Apply and restart** to install the update. You can do this either through the
Docker menu or in the **Updates** section in the Docker Desktop Dashboard.

The **Automatically update components** setting checks whether components of Docker Desktop, such as Docker Compose, Docker Scout, and the Docker CLI, can be updated independently without the need for a full restart. This is turned on by default.

## Extensions

Use the **Extensions** tab to:

- **Enable Docker Extensions**
- **Allow only extensions distributed through the Docker Marketplace**
- **Show Docker Extensions system containers**

For more information about Docker extensions, see
[Extensions](https://docs.docker.com/extensions/).

## Beta features

Beta features provide access to future product functionality.
These features are intended for testing and feedback only as they may change
between releases without warning or remove them entirely from a future
release. Beta features must not be used in production environments.
Docker doesn't offer support for beta features.

You can also sign up to the [Developer Preview program](https://www.docker.com/community/get-involved/developer-preview/) from the **Beta features** tab.

For a list of current experimental features in the Docker CLI, see [Docker CLI Experimental features](https://github.com/docker/cli/blob/master/experimental/README.md).

> Important
>
> For Docker Desktop versions 4.41 and earlier, there is also an **Experimental features** tab under the **Features in development** page.
>
>
>
> As with beta features, experimental features must not be used in production environments. Docker does not offer support for experimental features.

## Notifications

Use the **Notifications** tab to turn on or turn off notifications for the following events:

- **Status updates on tasks and processes**
- **Recommendations from Docker**
- **Docker announcements**
- **Docker surveys**

By default, all general notifications are turned on. You'll always receive error notifications and notifications about new Docker Desktop releases and updates.

You can also
[configure notification settings for Docker Scout-related issues](https://docs.docker.com/scout/explore/dashboard/#notification-settings).

Notifications momentarily appear in the lower-right of the Docker Desktop Dashboard and then move to the **Notifications** drawer which can be accessed from the top-right of the Docker Desktop Dashboard.

## Advanced

On Mac, you can reconfigure your initial installation settings on the **Advanced** tab:

- **Choose how to configure the installation of Docker's CLI tools**.
  - **System**: Docker CLI tools are installed in the system directory under `/usr/local/bin`
  - **User**: Docker CLI tools are installed in the user directory under `$HOME/.docker/bin`. You must then add `$HOME/.docker/bin` to your PATH. To add `$HOME/.docker/bin` to your path:
    1. Open your shell configuration file. This is `~/.bashrc` if you're using a bash shell, or `~/.zshrc` if you're using a zsh shell.
    2. Copy and paste the following:
      ```console
      $ export PATH=$PATH:~/.docker/bin
      ```
    3. Save and the close the file. Restart your shell to apply the changes to the PATH variable.
- **Allow the default Docker socket to be used (Requires password)**. Creates `/var/run/docker.sock` which some third party clients may use to communicate with Docker Desktop. For more information, see
  [permission requirements for macOS](https://docs.docker.com/desktop/setup/install/mac-permission-requirements/#installing-symlinks).
- **Allow privileged port mapping (Requires password)**. Starts the privileged helper process which binds the ports that are between 1 and 1024. For more information, see
  [permission requirements for macOS](https://docs.docker.com/desktop/setup/install/mac-permission-requirements/#binding-privileged-ports).

For more information on each configuration and use case, see
[Permission requirements](https://docs.docker.com/desktop/setup/install/mac-permission-requirements/).

## Docker Offload

When signed in with a Docker account that has access to [Docker Offload](https://docs.docker.com/offload/), you can manage your
Offload settings from the **Docker Offload** tab.

Use the **Docker Offload** tab to:

- Toggle **Enable Docker Offload**. When enabled, you can start Offload sessions.
- Select **Idle timeout**. This is the duration of time between no activity and Docker Offload entering idle mode.For
  details about idle timeout, see [Active and idle states](https://docs.docker.com/offload/configuration/#understand-active-and-idle-states)
- Check **Enable GPU support**. When enabled, workloads can use cloud GPU if available.

---

# Allowlist for Docker Desktop

> A list of domain URLs required for Docker Desktop to function correctly within an organization.

# Allowlist for Docker Desktop

   Table of contents

---

For: Administrators

This page contains the domain URLs that you need to add to a firewall allowlist to ensure Docker Desktop works properly within your organization.

## Domain URLs to allow

| Domains | Description |
| --- | --- |
| https://api.segment.io | Analytics |
| https://cdn.segment.com | Analytics |
| https://notify.bugsnag.com | Error reports |
| https://sessions.bugsnag.com | Error reports |
| https://auth.docker.io | Authentication |
| https://cdn.auth0.com | Authentication |
| https://login.docker.com | Authentication |
| https://auth.docker.com | Authentication |
| https://desktop.docker.com | Update |
| https://hub.docker.com | Docker Hub |
| https://registry-1.docker.io | Docker Pull/Push |
| https://production.cloudflare.docker.com | Docker Pull/Push (Paid plans) |
| https://docker-images-prod.6aa30f8b08e16409b46e0173d6de2f56.r2.cloudflarestorage.com | Docker Pull/Push (Personal plan / Anonymous) |
| https://docker-pinata-support.s3.amazonaws.com | Troubleshooting |
| https://api.dso.docker.com | Docker Scout service |
| https://api.docker.com | New API |

---

# Install Docker Desktop on Arch

> Instructions for installing Docker Desktop Arch package. Mostly meant for hackers who want to try out Docker Desktop on a variety of Arch-based distributions.

# Install Docker Desktop on Arch-based distributions

   Table of contents

---

Availability: Experimental

> **Docker Desktop terms**
>
>
>
> Commercial use of Docker Desktop in larger enterprises (more than 250
> employees OR more than $10 million USD in annual revenue) requires a [paid
> subscription](https://www.docker.com/pricing/).

This page contains information on how to install, launch and upgrade Docker Desktop on an Arch-based distribution.

## Prerequisites

To install Docker Desktop successfully, you must meet the [general system requirements](https://docs.docker.com/desktop/setup/install/linux/#general-system-requirements).

## Install Docker Desktop

1. [Install the Docker client binary on Linux](https://docs.docker.com/engine/install/binaries/#install-daemon-and-client-binaries-on-linux). Static binaries for the Docker client are available for Linux as `docker`. You can use:
  ```console
  $ wget https://download.docker.com/linux/static/stable/x86_64/docker-29.2.0.tgz -qO- | tar xvfz - docker/docker --strip-components=1
  $ sudo cp -rp ./docker /usr/local/bin/ && rm -r ./docker
  ```
2. Download the latest Arch package from the
  [Release notes](https://docs.docker.com/desktop/release-notes/).
3. Install the package:
  ```console
  $ sudo pacman -U ./docker-desktop-x86_64.pkg.tar.zst
  ```
  By default, Docker Desktop is installed at `/opt/docker-desktop`.

## Launch Docker Desktop

To start Docker Desktop for Linux:

1. Navigate to the Docker Desktop application in your Gnome/KDE Desktop.
2. Select **Docker Desktop** to start Docker.
  The Docker Subscription Service Agreement displays.
3. Select **Accept** to continue. Docker Desktop starts after you accept the terms.
  Note that Docker Desktop won't run if you do not agree to the terms. You can choose to accept the terms at a later date by opening Docker Desktop.
  For more information, see [Docker Desktop Subscription Service Agreement](https://www.docker.com/legal/docker-subscription-service-agreement). It is recommended that you also read the [FAQs](https://www.docker.com/pricing/faq).

Alternatively, open a terminal and run:

```console
$ systemctl --user start docker-desktop
```

When Docker Desktop starts, it creates a dedicated
[context](https://docs.docker.com/engine/context/working-with-contexts) that the Docker CLI
can use as a target and sets it as the current context in use. This is to avoid
a clash with a local Docker Engine that may be running on the Linux host and
using the default context. On shutdown, Docker Desktop resets the current
context to the previous one.

The Docker Desktop installer updates Docker Compose and the Docker CLI binaries
on the host. It installs Docker Compose V2 and gives users the choice to
link it as docker-compose from the Settings panel. Docker Desktop installs
the new Docker CLI binary that includes cloud-integration capabilities in `/usr/local/bin/com.docker.cli`
and creates a symlink to the classic Docker CLI at `/usr/local/bin`.

After you’ve successfully installed Docker Desktop, you can check the versions
of these binaries by running the following commands:

```console
$ docker compose version
Docker Compose version v2.39.4

$ docker --version
Docker version 28.4.0, build d8eb465

$ docker version
Client:
 Version:           28.4.0
 API version:       1.51
 Go version:        go1.24.7
<...>
```

To enable Docker Desktop to start on sign in, from the Docker menu, select
**Settings** > **General** > **Start Docker Desktop when you sign in to your computer**.

Alternatively, open a terminal and run:

```console
$ systemctl --user enable docker-desktop
```

To stop Docker Desktop, select the Docker menu icon to open the Docker menu and select **Quit Docker Desktop**.

Alternatively, open a terminal and run:

```console
$ systemctl --user stop docker-desktop
```

## Next steps

- Explore [Docker's subscriptions](https://www.docker.com/pricing/) to see what Docker can offer you.
- Take a look at the
  [Docker workshop](https://docs.docker.com/get-started/workshop/) to learn how to build an image and run it as a containerized application.
- [Explore Docker Desktop](https://docs.docker.com/desktop/use-desktop/) and all its features.
- [Troubleshooting](https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/) describes common problems, workarounds, how to run and submit diagnostics, and submit issues.
- [FAQs](https://docs.docker.com/desktop/troubleshoot-and-support/faqs/general/) provide answers to frequently asked questions.
- [Release notes](https://docs.docker.com/desktop/release-notes/) lists component updates, new features, and improvements associated with Docker Desktop releases.
- [Back up and restore data](https://docs.docker.com/desktop/settings-and-maintenance/backup-and-restore/) provides instructions
  on backing up and restoring data related to Docker.
