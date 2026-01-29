# Understand permission requirements for Docker Desktop on Mac and more

# Understand permission requirements for Docker Desktop on Mac

> Understand permission requirements for Docker Desktop for Mac and the differences between versions

# Understand permission requirements for Docker Desktop on Mac

   Table of contents

---

This page contains information about the permission requirements for running and installing Docker Desktop on Mac.

It also provides clarity on running containers as `root` as opposed to having `root` access on the host.

Docker Desktop on Mac is designed with security in mind. Administrative rights are only required when absolutely necessary.

## Permission requirements

Docker Desktop for Mac is run as an unprivileged user. However, Docker Desktop requires certain functionalities to perform a limited set of privileged configurations such as:

- [Installing symlinks](#installing-symlinks) in`/usr/local/bin`.
- [Binding privileged ports](#binding-privileged-ports) that are less than 1024. Although privileged ports (ports below 1024) are not typically used as a security boundary, operating systems still prevent unprivileged processes from binding to them which breaks commands like `docker run -p 127.0.0.1:80:80 docker/getting-started`.
- [Ensuringlocalhostandkubernetes.docker.internalare defined](#ensuring-localhost-and-kubernetesdockerinternal-are-defined) in `/etc/hosts`. Some old macOS installs don't have `localhost` in `/etc/hosts`, which causes Docker to fail. Defining the DNS name `kubernetes.docker.internal` allows Docker to share Kubernetes contexts with containers.
- Securely caching the Registry Access Management policy which is read-only for the developer.

Privileged access is granted during installation.

The first time Docker Desktop for Mac launches, it presents an installation window where you can choose to either use the default settings, which work for most developers and requires you to grant privileged access, or use advanced settings.

If you work in an environment with elevated security requirements, for instance where local administrative access is prohibited, then you can use the advanced settings to remove the need for granting privileged access. You can configure:

- The location of the Docker CLI tools either in the system or user directory
- The default Docker socket
- Privileged port mapping

Depending on which advanced settings you configure, you must enter your password to confirm.

You can change these configurations at a later date from the **Advanced** page in **Settings**.

### Installing symlinks

The Docker binaries are installed by default in `/Applications/Docker.app/Contents/Resources/bin`. Docker Desktop creates symlinks for the binaries in `/usr/local/bin`, which means they're automatically included in `PATH` on most systems.

You can choose whether to install symlinks either in `/usr/local/bin` or `$HOME/.docker/bin` during installation of Docker Desktop.

If `/usr/local/bin` is chosen, and this location is not writable by unprivileged users, Docker Desktop requires authorization to confirm this choice before the symlinks to Docker binaries are created in `/usr/local/bin`. If `$HOME/.docker/bin` is chosen, authorization is not required, but then you must
[manually add$HOME/.docker/bin](https://docs.docker.com/desktop/settings-and-maintenance/settings/#advanced) to your PATH.

You are also given the option to enable the installation of the `/var/run/docker.sock` symlink. Creating this symlink ensures various Docker clients relying on the default Docker socket path work without additional changes.

As the `/var/run` is mounted as a tmpfs, its content is deleted on restart, symlink to the Docker socket included. To ensure the Docker socket exists after restart, Docker Desktop sets up a `launchd` startup task that creates the symlink by running `ln -s -f /Users/<user>/.docker/run/docker.sock /var/run/docker.sock`. This ensures the you aren't prompted on each startup to create the symlink. If you don't enable this option at installation, the symlink and the startup task is not created and you may have to explicitly set the `DOCKER_HOST` environment variable to `/Users/<user>/.docker/run/docker.sock` in the clients it is using. The Docker CLI relies on the current context to retrieve the socket path, the current context is set to `desktop-linux` on Docker Desktop startup.

### Binding privileged ports

You can choose to enable privileged port mapping during installation, or from the **Advanced** page in **Settings** post-installation. Docker Desktop requires authorization to confirm this choice.

### Ensuringlocalhostandkubernetes.docker.internalare defined

It is your responsibility to ensure that localhost is resolved to `127.0.0.1` and if Kubernetes is used, that `kubernetes.docker.internal` is resolved to `127.0.0.1`.

## Installing from the command line

Privileged configurations are applied during the installation with the `--user` flag on the
[install command](https://docs.docker.com/desktop/setup/install/mac-install/#install-from-the-command-line). In this case, you are not prompted to grant root privileges on the first run of Docker Desktop. Specifically, the `--user` flag:

- Uninstalls the previous `com.docker.vmnetd` if present
- Sets up symlinks
- Ensures that `localhost` is resolved to `127.0.0.1`

The limitation of this approach is that Docker Desktop can only be run by one user-account per machine, namely the one specified in the `-–user` flag.

## Privileged helper

In the limited situations when the privileged helper is needed, for example binding privileged ports or caching the Registry Access Management policy, the privileged helper is started by `launchd` and runs in the background unless it is disabled at runtime as previously described. The Docker Desktop backend communicates with the privileged helper over the UNIX domain socket `/var/run/com.docker.vmnetd.sock`. The functionalities it performs are:

- Binding privileged ports that are less than 1024.
- Securely caching the Registry Access Management policy which is read-only for the developer.
- Uninstalling the privileged helper.

The removal of the privileged helper process is done in the same way as removing `launchd` processes.

```console
$ ps aux | grep vmnetd
root             28739   0.0  0.0 34859128    228   ??  Ss    6:03PM   0:00.06 /Library/PrivilegedHelperTools/com.docker.vmnetd
user             32222   0.0  0.0 34122828    808 s000  R+   12:55PM   0:00.00 grep vmnetd

$ sudo launchctl unload -w /Library/LaunchDaemons/com.docker.vmnetd.plist
Password:

$ ps aux | grep vmnetd
user             32242   0.0  0.0 34122828    716 s000  R+   12:55PM   0:00.00 grep vmnetd

$ rm /Library/LaunchDaemons/com.docker.vmnetd.plist

$ rm /Library/PrivilegedHelperTools/com.docker.vmnetd
```

## Containers running as root within the Linux VM

With Docker Desktop, the Docker daemon and containers run in a lightweight Linux
VM managed by Docker. This means that although containers run by default as
`root`, this doesn't grant `root` access to the Mac host machine. The Linux VM
serves as a security boundary and limits what resources can be accessed from the
host. Any directories from the host bind mounted into Docker containers still
retain their original permissions.

## Enhanced Container Isolation

In addition, Docker Desktop supports
[Enhanced Container Isolation
mode](https://docs.docker.com/enterprise/security/hardened-desktop/enhanced-container-isolation/) (ECI),
available to Business customers only, which further secures containers without
impacting developer workflows.

ECI automatically runs all containers within a Linux user-namespace, such that
root in the container is mapped to an unprivileged user inside the Docker
Desktop VM. ECI uses this and other advanced techniques to further secure
containers within the Docker Desktop Linux VM, such that they are further
isolated from the Docker daemon and other services running inside the VM.

---

# Install Docker Desktop on Windows

> Get started with Docker for Windows. This guide covers system requirements, where to download, and instructions on how to install and update.

# Install Docker Desktop on Windows

   Table of contents

---

> **Docker Desktop terms**
>
>
>
> Commercial use of Docker Desktop in larger enterprises (more than 250
> employees OR more than $10 million USD in annual revenue) requires a [paid
> subscription](https://www.docker.com/pricing/).

This page provides download links, system requirements, and step-by-step installation instructions for Docker Desktop on Windows.

[Docker Desktop for Windows - x86_64](https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-win-amd64) [Docker Desktop for Windows - x86_64 on the Microsoft Store](https://apps.microsoft.com/detail/xp8cbj40xlbwkx?hl=en-GB&gl=GB) [Docker Desktop for Windows - Arm (Early Access)](https://desktop.docker.com/win/main/arm64/Docker%20Desktop%20Installer.exe?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-win-arm64)

*For checksums, seeRelease notes*

## System requirements

> Tip
>
> **Should I use Hyper-V or WSL?**
>
>
>
> Docker Desktop's functionality remains consistent on both WSL and Hyper-V, without a preference for either architecture. Hyper-V and WSL have their own advantages and disadvantages, depending on your specific setup and your planned use case.

- WSL version 2.1.5 or later. To check your version, see [WSL: Verification and setup](#wsl-verification-and-setup)
- Windows 10 64-bit: Enterprise, Pro, or Education version 22H2 (build 19045).
- Windows 11 64-bit: Enterprise, Pro, or Education version 23H2 (build 22631) or higher.
- Turn on the WSL 2 feature on Windows. For detailed instructions, refer to the
  [Microsoft documentation](https://docs.microsoft.com/en-us/windows/wsl/install-win10).
- The following hardware prerequisites are required to successfully run
  WSL 2 on Windows 10 or Windows 11:
  - 64-bit processor with [Second Level Address Translation (SLAT)](https://en.wikipedia.org/wiki/Second_Level_Address_Translation)
  - 4GB system RAM
  - Enable hardware virtualization in BIOS/UEFI. For more information, see
    [Virtualization](https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/topics/#docker-desktop-fails-due-to-virtualization-not-working).

For more information on setting up WSL 2 with Docker Desktop, see
[WSL](https://docs.docker.com/desktop/features/wsl/).

> Note
>
> Docker only supports Docker Desktop on Windows for those versions of Windows that are still within [Microsoft’s servicing timeline](https://support.microsoft.com/en-us/help/13853/windows-lifecycle-fact-sheet). Docker Desktop is not supported on server versions of Windows, such as Windows Server 2019 or Windows Server 2022. For more information on how to run containers on Windows Server, see [Microsoft's official documentation](https://learn.microsoft.com/virtualization/windowscontainers/quick-start/set-up-environment).

> Important
>
> To run [Windows containers](#windows-containers), you need Windows 10 or Windows 11 Professional or Enterprise edition.
> Windows Home or Education editions only allow you to run Linux containers.

- Windows 10 64-bit: Enterprise, Pro, or Education version 22H2 (build 19045).
- Windows 11 64-bit: Enterprise, Pro, or Education version 23H2 (build 22631) or higher.
- Turn on Hyper-V and Containers Windows features.
- The following hardware prerequisites are required to successfully run Client
  Hyper-V on Windows 10:
  - 64 bit processor with [Second Level Address Translation (SLAT)](https://en.wikipedia.org/wiki/Second_Level_Address_Translation)
  - 4GB system RAM
  - Turn on BIOS/UEFI-level hardware virtualization support in the
    BIOS/UEFI settings. For more information, see
    [Virtualization](https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/topics/#virtualization).

> Note
>
> Docker only supports Docker Desktop on Windows for those versions of Windows that are still within [Microsoft’s servicing timeline](https://support.microsoft.com/en-us/help/13853/windows-lifecycle-fact-sheet). Docker Desktop is not supported on server versions of Windows, such as Windows Server 2019 or Windows Server 2022. For more information on how to run containers on Windows Server, see [Microsoft's official documentation](https://learn.microsoft.com/virtualization/windowscontainers/quick-start/set-up-environment).

> Important
>
> To run [Windows containers](#windows-containers), you need Windows 10 or Windows 11 Professional or Enterprise edition.
> Windows Home or Education editions only allow you to run Linux containers.

- WSL version 2.1.5 or later. To check your version, see [WSL: Verification and setup](#wsl-verification-and-setup)
- Windows 10 64-bit: Enterprise, Pro, or Education version 22H2 (build 19045).
- Windows 11 64-bit: Enterprise, Pro, or Education version 23H2 (build 22631) or higher.
- Turn on the WSL 2 feature on Windows. For detailed instructions, refer to the
  [Microsoft documentation](https://docs.microsoft.com/en-us/windows/wsl/install-win10).
- The following hardware prerequisites are required to successfully run
  WSL 2 on Windows 10 or Windows 11:
  - 64-bit processor with [Second Level Address Translation (SLAT)](https://en.wikipedia.org/wiki/Second_Level_Address_Translation)
  - 4GB system RAM
  - Enable hardware virtualization in BIOS/UEFI. For more information, see
    [Virtualization](https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/topics/#virtualization).

> Important
>
> Windows containers are not supported.

Containers and images created with Docker Desktop are shared between all
user accounts on machines where it is installed. This is because all Windows
accounts use the same VM to build and run containers. Note that it is not possible to share containers and images between user accounts when using the Docker Desktop WSL 2 backend.

Running Docker Desktop inside a VMware ESXi or Azure VM is supported for Docker Business customers.
It requires enabling nested virtualization on the hypervisor first.
For more information, see
[Running Docker Desktop in a VM or VDI environment](https://docs.docker.com/desktop/setup/vm-vdi/).

## Install Docker Desktop on Windows

### Install interactively

1. Download the installer using the download button at the top of the page, or from the
  [release notes](https://docs.docker.com/desktop/release-notes/).
2. Double-click `Docker Desktop Installer.exe` to run the installer. By default, Docker Desktop is installed at `C:\Program Files\Docker\Docker`.
3. When prompted, ensure the **Use WSL 2 instead of Hyper-V** option on the Configuration page is selected or not depending on your choice of backend.
  On systems that support only one backend, Docker Desktop automatically selects the available option.
4. Follow the instructions on the installation wizard to authorize the installer and proceed with the installation.
5. When the installation is successful, select **Close** to complete the installation process.
6. [Start Docker Desktop](#start-docker-desktop).

If your administrator account is different to your user account, you must add the user to the **docker-users** group to access features that require higher privileges, such as creating and managing the Hyper-V VM, or using Windows containers:

1. Run **Computer Management** as an **administrator**.
2. Navigate to **Local Users and Groups** > **Groups** > **docker-users**.
3. Right-click to add the user to the group.
4. Sign out and sign back in for the changes to take effect.

### Install from the command line

After downloading `Docker Desktop Installer.exe`, run the following command in a terminal to install Docker Desktop:

```console
$ "Docker Desktop Installer.exe" install
```

If you’re using PowerShell you should run it as:

```powershell
Start-Process 'Docker Desktop Installer.exe' -Wait install
```

If using the Windows Command Prompt:

```sh
start /w "" "Docker Desktop Installer.exe" install
```

By default, Docker Desktop is installed at `C:\Program Files\Docker\Docker`.

If your administrator account is different to your user account, you must add the user to the **docker-users** group to access features that require higher privileges, such as creating and managing the Hyper-V VM, or using Windows containers.

```console
$ net localgroup docker-users <user> /add
```

See the [Installer flags](#installer-flags) section to see what flags the `install` command accepts.

## Start Docker Desktop

Docker Desktop does not start automatically after installation. To start Docker Desktop:

1. Search for Docker, and select **Docker Desktop** in the search results.
2. The Docker menu (
  ![whale menu](https://docs.docker.com/desktop/setup/install/images/whale-x.svg)
  ) displays the Docker Subscription Service Agreement.
  Here’s a summary of the key points:
  - Docker Desktop is free for small businesses (fewer than 250 employees AND less than $10 million in annual revenue), personal use, education, and non-commercial open source projects.
  - Otherwise, it requires a paid subscription for professional use.
  - Paid subscriptions are also required for government entities.
  - The Docker Pro, Team, and Business subscriptions include commercial use of Docker Desktop.
3. Select **Accept** to continue. Docker Desktop starts after you accept the terms.
  Note that Docker Desktop won't run if you do not agree to the terms. You can choose to accept the terms at a later date by opening Docker Desktop.
  For more information, see [Docker Desktop Subscription Service Agreement](https://www.docker.com/legal/docker-subscription-service-agreement/). It is recommended that you read the [FAQs](https://www.docker.com/pricing/faq).

> Tip
>
> As an IT administrator, you can use endpoint management (MDM) software to identify the number of Docker Desktop instances and their versions within your environment. This can provide accurate license reporting, help ensure your machines use the latest version of Docker Desktop, and enable you to
> [enforce sign-in](https://docs.docker.com/enterprise/security/enforce-sign-in/).
>
>
>
> - [Intune](https://learn.microsoft.com/en-us/mem/intune/apps/app-discovered-apps)
> - [Jamf](https://docs.jamf.com/10.25.0/jamf-pro/administrator-guide/Application_Usage.html)
> - [Kandji](https://support.kandji.io/support/solutions/articles/72000559793-view-a-device-application-list)
> - [Kolide](https://www.kolide.com/features/device-inventory/properties/mac-apps)
> - [Workspace One](https://blogs.vmware.com/euc/2022/11/how-to-use-workspace-one-intelligence-to-manage-app-licenses-and-reduce-costs.html)

## Advanced system configuration and installation options

### WSL: Verification and setup

If you have chosen to use WSL, first verify that your installed version meets system requirements by running the following command in your terminal:

```console
wsl --version
```

If version details do not appear, you are likely using the inbox version of WSL. This version does not support modern capabilities and must be updated.

You can update or install WSL using one of the following methods:

#### Option 1: Install or update WSL via the terminal

1. Open PowerShell or Windows Command Prompt in administrator mode.
2. Run either the install or update command. You may be prompted to restart your machine. For more information, refer to [Install WSL](https://learn.microsoft.com/en-us/windows/wsl/install).

```console
wsl --install

wsl --update
```

#### Option 2: Install WSL via the MSI package

If Microsoft Store access is blocked due to security policies:

1. Go to the official [WSL GitHub Releases page](https://github.com/microsoft/WSL/releases).
2. Download the `.msi` installer from the latest stable release (under the Assets drop-down).
3. Run the downloaded installer and follow the setup instructions.

### Installer flags

> Note
>
> If you're using PowerShell, you need to use the `ArgumentList` parameter before any flags.
> For example:
>
>
>
> ```powershell
> Start-Process 'Docker Desktop Installer.exe' -Wait -ArgumentList 'install', '--accept-license'
> ```

#### Installation behavior

- `--quiet`: Suppresses information output when running the installer
- `--accept-license`: Accepts the [Docker Subscription Service Agreement](https://www.docker.com/legal/docker-subscription-service-agreement) now, rather than requiring it to be accepted when the application is first run
- `--installation-dir=<path>`: Changes the default installation location (`C:\Program Files\Docker\Docker`)
- `--backend=<backend name>`: Selects the default backend to use for Docker Desktop, `hyper-v`, `windows` or `wsl-2` (default)
- `--always-run-service`: After installation completes, starts `com.docker.service` and sets the service startup type to Automatic. This circumvents the need for administrator privileges, which are otherwise necessary to start `com.docker.service`. `com.docker.service` is required by Windows containers and Hyper-V backend.

#### Security and access control

- `--allowed-org=<org name>`: Requires the user to sign in and be part of the specified Docker Hub organization when running the application
- `--admin-settings`: Automatically creates an `admin-settings.json` file which is used by admins to control certain Docker Desktop settings on client machines within their organization. For more information, see
  [Settings Management](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/).
  - It must be used together with the `--allowed-org=<org name>` flag.
  - For example:`--allowed-org=<org name> --admin-settings="{'configurationFileVersion': 2, 'enhancedContainerIsolation': {'value': true, 'locked': false}}"`
- `--no-windows-containers`: Disables the Windows containers integration. This can improve security. For more information, see
  [Windows containers](https://docs.docker.com/desktop/setup/install/windows-permission-requirements/#windows-containers).

#### Proxy configuration

- `--proxy-http-mode=<mode>`: Sets the HTTP Proxy mode, `system` (default) or `manual`
- `--override-proxy-http=<URL>`: Sets the URL of the HTTP proxy that must be used for outgoing HTTP requests, requires `--proxy-http-mode` to be `manual`
- `--override-proxy-https=<URL>`: Sets the URL of the HTTP proxy that must be used for outgoing HTTPS requests, requires `--proxy-http-mode` to be `manual`
- `--override-proxy-exclude=<hosts/domains>`: Bypasses proxy settings for the hosts and domains. Uses a comma-separated list.
- `--proxy-enable-kerberosntlm`: Enables Kerberos and NTLM proxy authentication. If you are enabling this, ensure your proxy server is properly configured for Kerberos/NTLM authentication. Available with Docker Desktop 4.32 and later.
- `--override-proxy-pac=<PAC file URL>`: Sets the PAC file URL. This setting takes effect only when using `manual` proxy mode.
- `--override-proxy-embedded-pac=<PAC script>`: Specifies an embedded PAC (Proxy Auto-Config) script. This setting takes effect only when using `manual` proxy mode and has precedence over the `--override-proxy-pac` flag.

##### Example of specifying PAC file

```console
"Docker Desktop Installer.exe" install --proxy-http-mode="manual" --override-proxy-pac="http://localhost:8080/myproxy.pac"
```

##### Example of specifying PAC script

```console
"Docker Desktop Installer.exe" install --proxy-http-mode="manual" --override-proxy-embedded-pac="function FindProxyForURL(url, host) { return \"DIRECT\"; }"
```

#### Data root and disk location

- `--hyper-v-default-data-root=<path>`: Specifies the default location for the Hyper-V VM disk.
- `--windows-containers-default-data-root=<path>`: Specifies the default location for the Windows containers.
- `--wsl-default-data-root=<path>`: Specifies the default location for the WSL distribution disk.

### Administrator privileges

Installing Docker Desktop requires administrator privileges. However, once installed, it can be used without administrative access. Some actions, though, still need elevated permissions. See [Understand permission requirements for Windows](https://docs.docker.com/desktop/setup/install/windows-permission-requirements/) for more detail.

See the
[FAQs](https://docs.docker.com/desktop/troubleshoot-and-support/faqs/general/#how-do-i-run-docker-desktop-without-administrator-privileges) on how to install and run Docker Desktop without needing administrator privileges.

If you're an IT admin and your users do not have administrator rights and plan to perform operations that require elevated privileges, be sure to install Docker Desktop using the `--always-run-service` installer flag. This ensures those actions can still be executed without prompting for User Account Control (UAC) elevation. See [Installer Flags](#installer-flags) for more detail.

### Windows containers

From the Docker Desktop menu, you can toggle which daemon (Linux or Windows)
the Docker CLI talks to. Select **Switch to Windows containers** to use Windows
containers, or select **Switch to Linux containers** to use Linux containers
(the default).

For more information on Windows containers, refer to the following documentation:

- Microsoft documentation on [Windows containers](https://docs.microsoft.com/en-us/virtualization/windowscontainers/about/index).
- [Build and Run Your First Windows Server Container (Blog Post)](https://www.docker.com/blog/build-your-first-docker-windows-server-container/)
  gives a quick tour of how to build and run native Docker Windows containers on Windows 10 and Windows Server 2016 evaluation releases.
- [Getting Started with Windows Containers (Lab)](https://github.com/docker/labs/blob/master/windows/windows-containers/README.md)
  shows you how to use the [MusicStore](https://github.com/aspnet/MusicStore/)
  application with Windows containers. The MusicStore is a standard .NET application and,
  [forked here to use containers](https://github.com/friism/MusicStore), is a good example of a multi-container application.
- To understand how to connect to Windows containers from the local host, see
  [I want to connect to a container from Windows](https://docs.docker.com/desktop/features/networking/#i-want-to-connect-to-a-container-from-the-host)

> Note
>
> When you switch to Windows containers, **Settings** only shows those tabs that are active and apply to your Windows containers.

If you set proxies or daemon configuration in Windows containers mode, these
apply only on Windows containers. If you switch back to Linux containers,
proxies and daemon configurations return to what you had set for Linux
containers. Your Windows container settings are retained and become available
again when you switch back.

## Where to go next

- Explore [Docker's subscriptions](https://www.docker.com/pricing/) to see what Docker can offer you.
- [Get started with Docker](https://docs.docker.com/get-started/introduction/).
- [Explore Docker Desktop](https://docs.docker.com/desktop/use-desktop/) and all its features.
- [Troubleshooting](https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/) describes common problems, workarounds, and
  how to get support.
- [FAQs](https://docs.docker.com/desktop/troubleshoot-and-support/faqs/general/) provide answers to frequently asked questions.
- [Release notes](https://docs.docker.com/desktop/release-notes/) lists component updates, new features, and improvements associated with Docker Desktop releases.
- [Back up and restore data](https://docs.docker.com/desktop/settings-and-maintenance/backup-and-restore/) provides instructions on backing up and restoring data related to Docker.

---

# Understand permission requirements for Windows

> Understand permission requirements for Docker Desktop for Windows

# Understand permission requirements for Windows

   Table of contents

---

This page contains information about the permission requirements for running and installing Docker Desktop on Windows, the functionality of the privileged helper process `com.docker.service`, and the reasoning behind this approach.

It also provides clarity on running containers as `root` as opposed to having `Administrator` access on the host and the privileges of the Windows Docker engine and Windows containers.

Docker Desktop on Windows is designed with security in mind. Administrative rights are only required when absolutely necessary.

## Permission requirements

While Docker Desktop on Windows can be run without having `Administrator` privileges, it does require them during installation. On installation you receive a UAC prompt which allows a privileged helper service to be installed. After that, Docker Desktop can be run without administrator privileges.

Running Docker Desktop on Windows without the privileged helper does not require users to have `docker-users` group membership. However,
some features that require privileged operations will have this requirement.

If you performed the installation, you are automatically added to this group, but other users must be added manually. This allows the administrator to control who has access to features that require higher privileges, such as creating and managing the Hyper-V VM, or using Windows containers.

When Docker Desktop launches, all non-privileged named pipes are created so that only the following users can access them:

- The user that launched Docker Desktop.
- Members of the local `Administrators` group.
- The `LOCALSYSTEM` account.

## Privileged helper

Docker Desktop needs to perform a limited set of privileged operations which are conducted by the privileged helper process `com.docker.service`. This approach allows, following the principle of least privilege, `Administrator` access to be used only for the operations for which it is absolutely necessary, while still being able to use Docker Desktop as an unprivileged user.

The privileged helper `com.docker.service` is a Windows service which runs in the background with `SYSTEM` privileges. It listens on the named pipe `//./pipe/dockerBackendV2`. The developer runs the Docker Desktop application, which connects to the named pipe and sends commands to the service. This named pipe is protected, and only users that are part of the `docker-users` group can have access to it.

The service performs the following functionalities:

- Ensuring that `kubernetes.docker.internal` is defined in the Win32 hosts file. Defining the DNS name `kubernetes.docker.internal` allows Docker to share Kubernetes contexts with containers.
- Ensuring that `host.docker.internal` and `gateway.docker.internal` are defined in the Win32 hosts file. They point to the host local IP address and allow an application to resolve the host IP using the same name from either the host itself or a container.
- Securely caching the Registry Access Management policy which is read-only for the developer.
- Creating the Hyper-V VM `"DockerDesktopVM"` and managing its lifecycle - starting, stopping, and destroying it. The VM name is hard coded in the service code so the service cannot be used for creating or manipulating any other VMs.
- Moving the VHDX file or folder.
- Starting and stopping the Windows Docker engine and querying whether it's running.
- Deleting all Windows containers data files.
- Checking if Hyper-V is enabled.
- Checking if the bootloader activates Hyper-V.
- Checking if required Windows features are both installed and enabled.
- Conducting healthchecks and retrieving the version of the service itself.

The service start mode depends on which container engine is selected, and, for WSL, on whether it is needed to maintain `host.docker.internal` and `gateway.docker.internal` in the Win32 hosts file. This is controlled by a setting under `Use the WSL 2 based engine` in the settings page. When this is set, WSL engine behaves the same as Hyper-V. So:

- With Windows containers, or Hyper-v Linux containers, the service is started when the system boots and runs all the time, even when Docker Desktop isn't running. This is required so you can launch Docker Desktop without admin privileges.
- With WSL2 Linux containers, the service isn't necessary and therefore doesn't run automatically when the system boots. When you switch to Windows containers or Hyper-V Linux containers, or choose to maintain `host.docker.internal` and `gateway.docker.internal` in the Win32 hosts file, a UAC prompt appears asking you to accept the privileged operation to start the service. If accepted, the service is started and set to start automatically upon the next Windows boot.

## Containers running as root within the Linux VM

The Linux Docker daemon and containers run in a minimal, special-purpose Linux
VM managed by Docker. It is immutable so you can’t extend it or change the
installed software. This means that although containers run by default as
`root`, this doesn't allow altering the VM and doesn't grant `Administrator`
access to the Windows host machine. The Linux VM serves as a security boundary
and limits what resources from the host can be accessed. File sharing uses a
user-space crafted file server and any directories from the host bind mounted
into Docker containers still retain their original permissions. Containers don't have access to any host files beyond those explicitly shared.

## Enhanced Container Isolation

In addition, Docker Desktop supports
[Enhanced Container Isolation
mode](https://docs.docker.com/enterprise/security/hardened-desktop/enhanced-container-isolation/) (ECI),
available to Business customers only, which further secures containers without
impacting developer workflows.

ECI automatically runs all containers within a Linux user-namespace, such that
root in the container is mapped to an unprivileged user inside the Docker
Desktop VM. ECI uses this and other advanced techniques to further secure
containers within the Docker Desktop Linux VM, such that they are further
isolated from the Docker daemon and other services running inside the VM.

## Windows containers

> Warning
>
> Enabling Windows containers has important security implications.

Unlike the Linux Docker Engine and containers which run in a VM, Windows containers are implemented using operating system features, and run directly on the Windows host. If you enable Windows containers during installation, the `ContainerAdministrator` user used for administration inside the container is a local administrator on the host machine. Enabling Windows containers during installation makes it so that members of the `docker-users` group are able to elevate to administrators on the host. For organizations who don't want their developers to run Windows containers, a `-–no-windows-containers` installer flag is available to disable their use.

## Networking

For network connectivity, Docker Desktop uses a user-space process (`vpnkit`), which inherits constraints like firewall rules, VPN, HTTP proxy properties etc. from the user that launched it.

---

# Sign in to Docker Desktop

> Explore the Learning center and understand the benefits of signing in to Docker Desktop

# Sign in to Docker Desktop

   Table of contents

---

Docker recommends signing in with the **Sign in** option in the top-right corner of the Docker Dashboard.

In large enterprises where admin access is restricted, administrators can
[enforce sign-in](https://docs.docker.com/enterprise/security/enforce-sign-in/).

> Tip
>
> Explore [Docker's core subscriptions](https://www.docker.com/pricing/) to see what else Docker can offer you.

## Benefits of signing in

- Access your Docker Hub repositories directly from Docker Desktop.
- Increase your pull rate limit compared to anonymous users. See
  [Usage and limits](https://docs.docker.com/docker-hub/usage/).
- Enhance your organization’s security posture for containerized development with
  [Hardened Desktop](https://docs.docker.com/enterprise/security/hardened-desktop/).

> Note
>
> Docker Desktop automatically signs you out after 90 days, or after 30 days of inactivity.

## Signing in with Docker Desktop for Linux

Docker Desktop for Linux relies on [pass](https://www.passwordstore.org/) to store credentials in GPG-encrypted files.
Before signing in to Docker Desktop with your
[Docker ID](https://docs.docker.com/accounts/create-account/), you must initialize `pass`.
Docker Desktop displays a warning if `pass` is not configured.

1. Generate a GPG key. You can initialize pass by using a gpg key. To generate a gpg key, run:
  ```console
  $ gpg --generate-key
  ```
2. Enter your name and email once prompted.
  Once confirmed, GPG creates a key pair. Look for the `pub` line that contains your GPG ID, for example:
  ```text
  ...
  pubrsa3072 2022-03-31 [SC] [expires: 2024-03-30]
   3ABCD1234EF56G78
  uid          Molly <molly@example.com>
  ```
3. Copy the GPG ID and use it to initialize `pass`. For example
  ```console
  $ pass init 3ABCD1234EF56G78
  ```
  You should see output similar to:
  ```text
  mkdir: created directory '/home/molly/.password-store/'
  Password store initialized for <generated_gpg-id_public_key>
  ```

Once you initialize `pass`, you can sign in and pull your private images.
When Docker CLI or Docker Desktop use credentials, a user prompt may pop up for the password you set during the GPG key generation.

```console
$ docker pull molly/privateimage
Using default tag: latest
latest: Pulling from molly/privateimage
3b9cc81c3203: Pull complete
Digest: sha256:3c6b73ce467f04d4897d7a7439782721fd28ec9bf62ea2ad9e81a5fb7fb3ff96
Status: Downloaded newer image for molly/privateimage:latest
docker.io/molly/privateimage:latest
```

## What's next?

- [Explore Docker Desktop](https://docs.docker.com/desktop/use-desktop/) and its features.
- Change your
  [Docker Desktop settings](https://docs.docker.com/desktop/settings-and-maintenance/settings/).
- [Browse common FAQs](https://docs.docker.com/desktop/troubleshoot-and-support/faqs/general/).

---

# Run Docker Desktop for Windows in a VM or VDI environment

> Instructions on how to enable nested virtualization

# Run Docker Desktop for Windows in a VM or VDI environment

   Table of contents

---

Docker recommends running Docker Desktop natively on Mac, Linux, or Windows. However, Docker Desktop for Windows can run inside a virtual desktop provided the virtual desktop is properly configured.

To run Docker Desktop in a virtual desktop environment, you have two options,
depending on whether nested virtualization is supported:

- If your environment supports nested virtualization, you can run Docker Desktop
  with its default local Linux VM.
- If nested virtualization is not supported, Docker recommends subscribing to and using Docker Offload.

## Use Docker Offload

[Docker Offload](https://docs.docker.com/offload/) lets you offload container workloads to a high-performance, fully hosted cloud environment,
enabling a seamless hybrid experience.

Docker Offload is useful in virtual desktop environments where nested virtualization isn't supported. In these
environments, Docker Desktop can use Docker Offload to ensure you can still build and run containers without relying on
local virtualization.

Docker Offload decouples the Docker Desktop client from the Docker Engine,
allowing the Docker CLI and Docker Desktop Dashboard to interact with
cloud-based resources as if they were local. When you run a container, Docker
provisions a secure, isolated, and ephemeral cloud environment connected to
Docker Desktop via an SSH tunnel. Despite running remotely, features like bind
mounts and port forwarding continue to work seamlessly, providing a local-like
experience. To use Docker Offload:

To get started using Docker Offload, see the
[Docker Offload
quickstart](https://docs.docker.com/offload/quickstart/).

## Virtual desktop support when using nested virtualization

> Note
>
> Support for running Docker Desktop on a virtual desktop is available to Docker Business customers, on VMware ESXi or Azure VMs only.

Docker support includes installing and running Docker Desktop within the VM, provided that nested virtualization is correctly enabled. The only hypervisors successfully tested are VMware ESXi and Azure, and there is no support for other VMs. For more information on Docker Desktop support, see
[Get support](https://docs.docker.com/support/).

For troubleshooting problems and intermittent failures that are outside of Docker's control, you should contact your hypervisor vendor. Each hypervisor vendor offers different levels of support. For example, Microsoft supports running nested Hyper-V both on-prem and on Azure, with some version constraints. This may not be the case for VMware ESXi.

Docker does not support running multiple instances of Docker Desktop on the same machine in a VM or VDI environment.

> Tip
>
> If you're running Docker Desktop inside a Citrix VDI, note that Citrix can be used with a variety of underlying hypervisors, for example VMware, Hyper-V, Citrix Hypervisor/XenServer. Docker Desktop requires nested virtualization, which is not supported by Citrix Hypervisor/XenServer.
>
>
>
> Check with your Citrix administrator or VDI infrastructure team to confirm which hypervisor is being used, and whether nested virtualization is enabled.

## Turn on nested virtualization

You must turn on nested virtualization before you install Docker Desktop on a
virtual machine that will not use Docker Cloud.

### Turn on nested virtualization on VMware ESXi

Nested virtualization of other hypervisors like Hyper-V inside a vSphere VM [is not a supported scenario](https://kb.vmware.com/s/article/2009916). However, running Hyper-V VM in a VMware ESXi VM is technically possible and, depending on the version, ESXi includes hardware-assisted virtualization as a supported feature. A VM that had 1 CPU with 4 cores and 12GB of memory was used for internal testing.

For steps on how to expose hardware-assisted virtualization to the guest OS, [see VMware's documentation](https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/7-0/expose-hardware-assisted-virtualization.html).

### Turn on nested virtualization on an Azure Virtual Machine

Nested virtualization is supported by Microsoft for running Hyper-V inside an Azure VM.

For Azure virtual machines, [check that the VM size chosen supports nested virtualization](https://docs.microsoft.com/en-us/azure/virtual-machines/sizes). Microsoft provides [a helpful list on Azure VM sizes](https://docs.microsoft.com/en-us/azure/virtual-machines/acu) and highlights the sizes that currently support nested virtualization. D4s_v5 machines were used for internal testing. Use this specification or above for optimal performance of Docker Desktop.

## Docker Desktop support on Nutanix-powered VDI

Docker Desktop can be used within Nutanix-powered VDI environments provided that the underlying Windows environment supports WSL 2 or Windows container mode. Since Nutanix officially supports WSL 2, Docker Desktop should function as expected, as long as WSL 2 operates correctly within the VDI environment.

If using Windows container mode, confirm that the Nutanix environment supports Hyper-V or alternative Windows container backends.

### Supported configurations

Docker Desktop follows the VDI support definitions outlined [previously](#virtual-desktop-support-when-using-nested-virtualization):

- Persistent VDI environments (Supported): You receive the same virtual desktop instance across sessions, preserving installed software and configurations.
- Non-persistent VDI environments (Not supported): Docker Desktop does not support environments where the OS resets between sessions, requiring re-installation or reconfiguration each time.

### Support scope and responsibilities

For WSL 2-related issues, contact Nutanix support. For Docker Desktop-specific issues, contact Docker support.

## Additional resources

- [Docker Desktop on Microsoft Dev Box](https://docs.docker.com/enterprise/enterprise-deployment/dev-box/)
