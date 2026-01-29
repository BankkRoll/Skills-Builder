# Troubleshoot topics for Docker Desktop and more

# Troubleshoot topics for Docker Desktop

> Explore common troubleshooting topics for Docker Desktop

# Troubleshoot topics for Docker Desktop

   Table of contents

---

> Tip
>
> If you do not find a solution in troubleshooting, browse the GitHub repositories or [create a new issue](https://github.com/docker/desktop-feedback).

## Topics for all platforms

### Certificates not set up correctly

#### Error message

When attempting to pull from a registry using `docker run`, you may encounter the following error:

```console
Error response from daemon: Get http://192.168.203.139:5858/v2/: malformed HTTP response "\x15\x03\x01\x00\x02\x02"
```

Additionally, logs from the registry may show:

```console
2017/06/20 18:15:30 http: TLS handshake error from 192.168.203.139:52882: tls: client didn't provide a certificate
2017/06/20 18:15:30 http: TLS handshake error from 192.168.203.139:52883: tls: first record does not look like a TLS handshake
```

#### Possible causes

- Docker Desktop ignores certificates listed under insecure registries.
- Client certificates are not sent to insecure registries, causing handshake failures.

#### Solution

- Ensure that your registry is properly configured with valid SSL certificates.
- If your registry is self-signed, configure Docker to trust the certificate by adding it to Docker’s certificates directory (/etc/docker/certs.d/ on Linux).
- If the issue persists, check your Docker daemon configuration and enable TLS authentication.

### Docker Desktop's UI appears green, distorted, or has visual artifacts

#### Cause

Docker Desktop uses hardware-accelerated graphics by default, which may cause problems for some GPUs.

#### Solution

Disable hardware acceleration:

1. Edit Docker Desktop's `settings-store.json` file (or `settings.json` for Docker Desktop versions 4.34 and earlier). You can find this file at:
  - Mac: `~/Library/Group Containers/group.com.docker/settings-store.json`
  - Windows: `C:\Users\[USERNAME]\AppData\Roaming\Docker\settings-store.json`
  - Linux: `~/.docker/desktop/settings-store.json.`
2. Add the following entry:
  ```JSON
  $ "disableHardwareAcceleration": true
  ```
3. Save the file and restart Docker Desktop.

### Using mounted volumes and getting runtime errors indicating an application file is not found, access to a volume mount is denied, or a service cannot start

#### Cause

If your project directory is located outside your home directory (`/home/<user>`), Docker Desktop requires file sharing permissions to access it.

#### Solution

Enable file sharing in Docker Desktop for Mac and Linux:

1. Navigate to **Settings**, select **Resources** and then **File sharing**.
2. Add the drive or folder that contains the Dockerfile and volume mount paths.

Enable file sharing in Docker Desktop for Windows:

1. From **Settings**, select **Shared Folders**.
2. Share the folder that contains the Dockerfile and volume mount paths.

### port already allocatederrors

#### Error message

When starting a container, you may see an error like:

```text
Bind for 0.0.0.0:8080 failed: port is already allocated
```

Or

```text
listen tcp:0.0.0.0:8080: bind: address is already in use
```

#### Cause

- Another application on your system is already using the specified port.
- A previously running container was not stopped properly and is still bound to the port.

#### Solution

To discover the identity of this software, either:

- Use the `resmon.exe` GUI, select **Network** and then **Listening Ports**
- In PowerShell, use `netstat -aon | find /i "listening "` to discover the PID of the process
  currently using the port (the PID is the number in the rightmost column).

Then, decide whether to shut the other process down, or to use a different port in your
Docker app.

## Topics for Linux and Mac

### Docker Desktop fails to start on Mac or Linux platforms

#### Error message

Docker fails to start due to Unix domain socket path length limitations:

```console
[vpnkit-bridge][F] listen unix HOME/Library/Containers/com.docker.docker/Data/http-proxy-control.sock: bind: invalid argument
```

```console
[com.docker.backend][E] listen(vsock:4099) failed: listen unix HOME/Library/Containers/com.docker.docker/Data/vms/0/00000002.00001003: bind: invalid argument
```

#### Cause

On Mac and Linux, Docker Desktop creates Unix domain sockets used for inter-process communication. These sockets are created under the user's home directory.

Unix domain sockets have a maximum path length:

- 104 characters on Mac
- 108 characters on Linux

If your home directory path is too long, Docker Desktop fails to create necessary sockets.

#### Solution

Ensure your username is short enough to keep paths within the allowed limit:

- Mac: Username should be ≤ 33 characters
- Linux: Username should be ≤ 55 characters

## Topics for Mac

### Upgrade requires administrator privileges

#### Cause

On macOS, users without administrator privileges cannot perform in-app upgrades from the Docker Desktop Dashboard.

#### Solution

> Important
>
> Do not uninstall the current version before upgrading. Doing so deletes all local Docker containers, images, and volumes.

To upgrade Docker Desktop:

- Ask an administrator to install the newer version over the existing one.
- Use the []`--user` install flag](/manuals/desktop/setup/install/mac-install.md#security-and-access) if appropriate for your setup.

### Persistent notification telling me an application has changed my Desktop configurations

#### Cause

You receive this notification because the Configuration integrity check feature has detected that a third-party application has altered your Docker Desktop configuration. This usually happens due to incorrect or missing symlinks. The notification ensures you are aware of these changes so you can review and repair any potential issues to maintain system reliability.

Opening the notification presents a pop-up window which provides detailed information about the detected integrity issues.

#### Solution

If you choose to ignore the notification, it will be shown again only at the next Docker Desktop startup. If you choose to repair your configuration, you won't be prompted again.

If you want to switch off Configuration integrity check notifications, navigate to Docker Desktop's settings and in the **General** tab, clear the **Automatically check configuration** setting.

### com.docker.vmnetdis still running after I quit the app

The privileged helper process `com.docker.vmnetd` is started by `launchd` and
runs in the background. The process does not consume any resources unless
`Docker.app` connects to it, so it's safe to ignore.

### Incompatible CPU detected

#### Cause

Docker Desktop requires a processor (CPU) that supports virtualization and, more
specifically, the [Apple Hypervisor
framework](https://developer.apple.com/library/mac/documentation/DriversKernelHardware/Reference/Hypervisor/).

#### Solution

Check that:

- You've installed the correct Docker Desktop for your architecture
- Your Mac supports Apple's Hypervisor framework. To check if your Mac supports the Hypervisor framework, run the following command in a terminal window.
  ```console
  $ sysctl kern.hv_support
  ```
  If your Mac supports the Hypervisor Framework, the command prints `kern.hv_support: 1`.
  If not, the command prints `kern.hv_support: 0`.

See also, [Hypervisor Framework
Reference](https://developer.apple.com/library/mac/documentation/DriversKernelHardware/Reference/Hypervisor/)
in the Apple documentation, and Docker Desktop
[Mac system requirements](https://docs.docker.com/desktop/setup/install/mac-install/#system-requirements).

### VPNKit keeps breaking

#### Cause

In Docker Desktop version 4.19, gVisor replaced VPNKit to enhance the performance of VM networking when using the Virtualization framework on macOS 13 and later.

#### Solution

To continue using VPNKit:

1. Open your `settings-store.json` file located at `~/Library/Group Containers/group.com.docker/settings-store.json`
2. Add:
  ```JSON
  $ "networkType":"vpnkit"
  ```
3. Save the file and restart Docker Desktop.

## Topics for Windows

### Docker Desktop fails to start when anti-virus software is installed

#### Cause

Some anti-virus software may be incompatible with Hyper-V and Microsoft
Windows 10 builds. The conflict
typically occurs after a Windows update and
manifests as an error response from the Docker daemon and a Docker Desktop start failure.

#### Solution

For a temporary workaround, uninstall the anti-virus software, or
add Docker to the exclusions/exceptions in your antivirus software.

### Permissions errors on data directories for shared volumes

#### Cause

When sharing files from Windows, Docker Desktop sets permissions on
[shared volumes](https://docs.docker.com/desktop/settings-and-maintenance/settings/#file-sharing)
to a default value of [0777](https://chmodcommand.com/chmod-0777/)
(`read`, `write`, `execute` permissions for `user` and for `group`).

The default permissions on shared volumes are not configurable.

#### Solution

If you are
working with applications that require different permissions, either:

- Use non-host-mounted volumes
- Find a way to make the applications work with the default file permissions

### Unexpected syntax errors, use Unix style line endings for files in containers

#### Cause

Docker containers expect Unix-style line `\n` endings, not Windows style: `\r\n`. This includes files referenced at the command line for builds and in RUN commands in Docker files.

Keep this in mind when authoring files such as shell scripts using Windows
tools, where the default is likely to be Windows style line endings. These
commands ultimately get passed to Unix commands inside a Unix based container
(for example, a shell script passed to `/bin/sh`). If Windows style line endings
are used, `docker run` fails with syntax errors.

#### Solution

- Convert files to Unix-style line endings using:
  ```console
  $ dos2unix script.sh
  ```
- In VS Code, set line endings to `LF` (Unix) instead of `CRLF` (Windows).

### Path conversion errors on Windows

#### Cause

Unlike Linux, Windows requires explicit path conversion for volume mounting.

On Linux, the system takes care of mounting a path to another path. For example, when you run the following command on Linux:

```console
$ docker run --rm -ti -v /home/user/work:/work alpine
```

It adds a `/work` directory to the target container to mirror the specified path.

#### Solution

Update the source path. For example, if you are using
the legacy Windows shell (`cmd.exe`), you can use the following command:

```console
$ docker run --rm -ti -v C:\Users\user\work:/work alpine
```

This starts the container and ensures the volume becomes usable. This is possible because Docker Desktop detects
the Windows-style path and provides the appropriate conversion to mount the directory.

Docker Desktop also allows you to use Unix-style path to the appropriate format. For example:

```console
$ docker run --rm -ti -v /c/Users/user/work:/work alpine ls /work
```

### Docker commands failing in Git Bash

#### Error message

```console
$ docker run --rm -ti -v C:\Users\user\work:/work alpine
docker: Error response from daemon: mkdir C:UsersUserwork: Access is denied.
```

```console
$ docker run --rm -ti -v $(pwd):/work alpine
docker: Error response from daemon: OCI runtime create failed: invalid mount {Destination:\Program Files\Git\work Type:bind Source:/run/desktop/mnt/host/c/Users/user/work;C Options:[rbind rprivate]}: mount destination \Program Files\Git\work not absolute: unknown.
```

#### Cause

Git Bash (or MSYS) provides a Unix-like environment on Windows. These tools apply their own
preprocessing on the command line.

This affects `$(pwd)`, colon-separated paths, and tilde (`~`)

Also, the `\` character has a special meaning in Git Bash.

#### Solution

- Disable Git Bash path conversion temporarily. For example, run the command with MSYS path conversion disable:
  ```console
  $ MSYS_NO_PATHCONV=1 docker run --rm -ti -v $(pwd):/work alpine
  ```
- Use proper path formatting:
  - Use double forward and backslashes (`\\` `//`) instead of single (`\` `/`).
  - If referencing `$(pwd)`, add an extra `/`:

Portability of the scripts is not affected as Linux treats multiple `/` as a single entry.

### Docker Desktop fails due to Virtualization not working

#### Error message

A typical error message is "Docker Desktop - Unexpected WSL error" mentioning the error code
`Wsl/Service/RegisterDistro/CreateVm/HCS/HCS_E_HYPERV_NOT_INSTALLED`. Manually executing `wsl` commands
also fails with the same error code.

#### Cause

- Virtualization settings are disabled in the BIOS.
- Windows Hyper-V or WSL 2 components are missing.

Note some third-party software such as Android emulators will disable Hyper-V on install.

#### Solutions

Your machine must have the following features for Docker Desktop to function correctly:

##### WSL 2 and Windows Home

1. Virtual Machine Platform
2. [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10)
3. [Virtualization enabled in the BIOS](https://support.microsoft.com/en-gb/windows/enable-virtualization-on-windows-c5578302-6e43-4b4b-a449-8ced115f58e1)
  Note that many Windows devices already have virtualization enabled, so this may not apply.
4. Hypervisor enabled at Windows startup

![WSL 2 enabled](https://docs.docker.com/desktop/images/wsl2-enabled.png)  ![WSL 2 enabled](https://docs.docker.com/desktop/images/wsl2-enabled.png)

It must be possible to run WSL 2 commands without error, for example:

```console
PS C:\users\> wsl -l -v
  NAME              STATE           VERSION
* Ubuntu            Running         2
  docker-desktop    Stopped         2
PS C:\users\> wsl -d docker-desktop echo WSL 2 is working
WSL 2 is working
```

If the features are enabled but the commands are not working, first check [Virtualization is turned on](#virtualization-must-be-turned-on)
then [enable the Hypervisor at Windows startup](#hypervisor-enabled-at-windows-startup) if required. If running Docker
Desktop in a Virtual Machine, ensure [the hypervisor has nested virtualization enabled](#turn-on-nested-virtualization).

##### Hyper-V

On Windows 10 Pro or Enterprise, you can also use Hyper-V with the following features enabled:

1. [Hyper-V](https://docs.microsoft.com/en-us/windows-server/virtualization/hyper-v/hyper-v-technology-overview)
  installed and working
2. [Virtualization enabled in the BIOS](https://support.microsoft.com/en-gb/windows/enable-virtualization-on-windows-c5578302-6e43-4b4b-a449-8ced115f58e1)
  Note that many Windows devices already have virtualization enabled, so this may not apply.
3. Hypervisor enabled at Windows startup

![Hyper-V on Windows features](https://docs.docker.com/desktop/images/hyperv-enabled.png)  ![Hyper-V on Windows features](https://docs.docker.com/desktop/images/hyperv-enabled.png)

Docker Desktop requires Hyper-V as well as the Hyper-V Module for Windows
PowerShell to be installed and enabled. The Docker Desktop installer enables
it for you.

Docker Desktop also needs two CPU hardware features to use Hyper-V: Virtualization and Second Level Address Translation (SLAT), which is also called Rapid Virtualization Indexing (RVI). On some systems, Virtualization must be enabled in the BIOS. The steps required are vendor-specific, but typically the BIOS option is called `Virtualization Technology (VTx)` or something similar. Run the command `systeminfo` to check all required Hyper-V features. See [Pre-requisites for Hyper-V on Windows 10](https://docs.microsoft.com/en-us/virtualization/hyper-v-on-windows/reference/hyper-v-requirements) for more details.

To install Hyper-V manually, see [Install Hyper-V on Windows 10](https://msdn.microsoft.com/en-us/virtualization/hyperv_on_windows/quick_start/walkthrough_install). A reboot is *required* after installation. If you install Hyper-V without rebooting, Docker Desktop does not work correctly.

From the start menu, type **Turn Windows features on or off** and press enter.
In the subsequent screen, verify that Hyper-V is enabled.

##### Virtualization must be turned on

In addition to [Hyper-V](#hyper-v) or
[WSL 2](https://docs.docker.com/desktop/features/wsl/), virtualization must be turned on. Check the
Performance tab on the Task Manager. Alternatively, you can type `systeminfo` into your terminal. If you see `Hyper-V Requirements: A hypervisor has been detected. Features required for Hyper-V will not be displayed`, then virtualization is enabled.

![Task Manager](https://docs.docker.com/desktop/images/virtualization-enabled.png)  ![Task Manager](https://docs.docker.com/desktop/images/virtualization-enabled.png)

If you manually uninstall Hyper-V, WSL 2 or turn off virtualization,
Docker Desktop cannot start.

To turn on nested virtualization, see
[Run Docker Desktop for Windows in a VM or VDI environment](https://docs.docker.com/desktop/setup/vm-vdi/#turn-on-nested-virtualization).

##### Hypervisor enabled at Windows startup

If you have completed the previous steps and are still experiencing
Docker Desktop startup issues, this could be because the Hypervisor is installed,
but not launched during Windows startup. Some tools (such as older versions of
Virtual Box) and video game installers turn off hypervisor on boot. To turn it back on:

1. Open an administrative console prompt.
2. Run `bcdedit /set hypervisorlaunchtype auto`.
3. Restart Windows.

You can also refer to the [Microsoft TechNet article](https://social.technet.microsoft.com/Forums/en-US/ee5b1d6b-09e2-49f3-a52c-820aafc316f9/hyperv-doesnt-work-after-upgrade-to-windows-10-1809?forum=win10itprovirt) on Code flow guard (CFG) settings.

##### Turn on nested virtualization

If you are using Hyper-V and you get the following error message when running Docker Desktop in a VDI environment:

```console
The Virtual Machine Management Service failed to start the virtual machine 'DockerDesktopVM' because one of the Hyper-V components is not running
```

Try
[enabling nested virtualization](https://docs.docker.com/desktop/setup/vm-vdi/#turn-on-nested-virtualization).

### Docker Desktop with Windows Containers fails with "The media is write protected""

#### Error message

`FSCTL_EXTEND_VOLUME \\?\Volume{GUID}: The media is write protected`

#### Cause

If you're encountering failures when running Docker Desktop with Windows Containers, it might be due to
a specific Windows configuration policy: FDVDenyWriteAccess.

This policy, when enabled, causes Windows to mount all fixed drives not encrypted by BitLocker-encrypted as read-only.
This also affects virtual machine volumes and as a result, Docker Desktop may not be able to start or run containers
correctly because it requires read-write access to these volumes.

FDVDenyWriteAccess is a Windows Group Policy setting that, when enabled, prevents write access to fixed data drives that are not protected
by BitLocker. This is often used in security-conscious environments but can interfere with development tools like Docker.
In the Windows registry it can be found at `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Policies\Microsoft\FVE\FDVDenyWriteAccess`.

#### Solutions

Docker Desktop does not support running Windows Containers on systems where FDVDenyWriteAccess is enabled. This setting interferes with the
ability of Docker to mount volumes correctly, which is critical for container functionality.

To use Docker Desktop with Windows Containers, ensure that FDVDenyWriteAccess is disabled. You can check and change this setting in the registry or through Group Policy Editor (`gpedit.msc`) under:

**Computer Configuration** > **Administrative Templates** > **Windows Components** > **BitLocker Drive Encryption** > **Fixed Data Drives** > **Deny write access to fixed drives not protected by BitLocker**

> Note
>
> Modifying Group Policy settings may require administrator privileges and should comply with your organization's IT policies. If the setting gets reset after some time this usually means that it was overridden by the centralized configuration of your IT department. Talk to them before making any changes.

### Docker Desktop Access Deniederror message when starting Docker Desktop

#### Error message

When starting Docker Desktop, the following error appears:

```text
Docker Desktop - Access Denied
```

#### Cause

The user is not part of the `docker-users` group, which is required for permissions.

#### Solution

If your admin account is different to your user account, add it:

1. Run **Computer Management** as an administrator.
2. Navigate to **Local Users and Groups** > **Groups** > **docker-users**.
3. Right-click to add the user to the group.
4. Sign out and sign back in for the changes to take effect

---

# Troubleshoot Docker Desktop

> Understand how to diagnose and troubleshoot Docker Desktop, and how to check the logs.

# Troubleshoot Docker Desktop

   Table of contents

---

This page contains information on how to diagnose and troubleshoot Docker Desktop, and how to check the logs.

## Troubleshoot menu

To navigate to **Troubleshoot** either:

- Select the Docker menu Docker menu
  ![whale menu](https://docs.docker.com/desktop/images/whale-x.svg)
  and then **Troubleshoot**.
- Select the **Troubleshoot** icon near the top-right corner of Docker Dashboard.

The **Troubleshooting** menu contains the following options:

- **Restart Docker Desktop**.
- **Reset Kubernetes cluster**. Select to delete all stacks and Kubernetes resources. For more information, see
  [Kubernetes](https://docs.docker.com/desktop/settings-and-maintenance/settings/#kubernetes).
- **Clean / Purge data**. This option resets all Docker data without a
  reset to factory defaults. Selecting this option results in the loss of existing settings.
- **Reset to factory defaults**: Choose this option to reset all options on
  Docker Desktop to their initial state, the same as when Docker Desktop was first installed.

If you are a Mac or Linux user, you also have the option to **Uninstall** Docker Desktop from your system.

## Diagnose

> Tip
>
> If you do not find a solution in troubleshooting, browse the GitHub repositories or create a new issue on the [Docker Desktop issue tracker](https://github.com/docker/desktop-feedback).

### Diagnose from the app

1. From **Troubleshoot**, select **Get support**. This opens the in-app Support page and starts collecting the diagnostics.
2. When the diagnostics collection process is complete, select **Upload to get a Diagnostic ID**.
3. When the diagnostics are uploaded, Docker Desktop prints a diagnostic ID. Copy this ID.
4. Use your diagnostics ID to get help:
  - If you have a paid Docker subscription, select **Contact support**. This opens the Docker Desktop support form. Fill in the information required and add the ID you copied in step three to the **Diagnostics ID field**. Then, select **Submit ticket** to request Docker Desktop support.
    > Note
    >
    > You must be signed in to Docker Desktop to access the support form. For information on what's covered as part of Docker Desktop support, see
    > [Support](https://docs.docker.com/support/).
  - If you don't have a paid Docker subscription, select **Report a Bug** to open a new Docker Desktop issue on GitHub. Complete the information required and ensure you add the diagnostic ID you copied in step three.

### Diagnose from an error message

1. When an error message appears, select **Gather diagnostics**.
2. When the diagnostics are uploaded, Docker Desktop prints a diagnostic ID. Copy this ID.
3. Use your diagnostics ID to get help:
  - If you have a paid Docker subscription, select **Contact support**. This opens the Docker Desktop support form. Fill in the information required and add the ID you copied in step three to the **Diagnostics ID field**. Then, select **Submit ticket** to request Docker Desktop support.
    > Note
    >
    > You must be signed in to Docker Desktop to access the support form. For information on what's covered as part of Docker Desktop support, see
    > [Support](https://docs.docker.com/support/).
  - If you don't have a paid Docker subscription, you can open a new [Docker Desktop issue on GitHub](https://github.com/docker/desktop-feedback). Complete the information required and ensure you add the diagnostic ID printed in step two.

### Diagnose from the terminal

In some cases, it's useful to run the diagnostics yourself, for instance, if
Docker Desktop cannot start.

1. Locate the `com.docker.diagnose` tool:
  ```console
  $ C:\Program Files\Docker\Docker\resources\com.docker.diagnose.exe
  ```
2. Create and upload the diagnostics ID. In PowerShell, run:
  ```console
  $ & "C:\Program Files\Docker\Docker\resources\com.docker.diagnose.exe" gather -upload
  ```

After the diagnostics have finished, the terminal displays your diagnostics ID and the path to the diagnostics file. The diagnostics ID is composed of your user ID and a timestamp. For example `BE9AFAAF-F68B-41D0-9D12-84760E6B8740/20190905152051`.

1. Locate the `com.docker.diagnose` tool:
  ```console
  $ /Applications/Docker.app/Contents/MacOS/com.docker.diagnose
  ```
2. Create and upload the diagnostics ID. Run:
  ```console
  $ /Applications/Docker.app/Contents/MacOS/com.docker.diagnose gather -upload
  ```

After the diagnostics have finished, the terminal displays your diagnostics ID and the path to the diagnostics file. The diagnostics ID is composed of your user ID and a timestamp. For example `BE9AFAAF-F68B-41D0-9D12-84760E6B8740/20190905152051`.

1. Locate the `com.docker.diagnose` tool:
  ```console
  $ /opt/docker-desktop/bin/com.docker.diagnose
  ```
2. Create and upload the diagnostics ID. Run:
  ```console
  $ /opt/docker-desktop/bin/com.docker.diagnose gather -upload
  ```

After the diagnostics have finished, the terminal displays your diagnostics ID and the path to the diagnostics file. The diagnostics ID is composed of your user ID and a timestamp. For example `BE9AFAAF-F68B-41D0-9D12-84760E6B8740/20190905152051`.

To view the contents of the diagnostic file:

1. Unzip the file. In PowerShell, copy and paste the path to the diagnostics file into the following command and then run it. It should be similar to the following example:
  ```powershell
  $ Expand-Archive -LiteralPath "C:\Users\testUser\AppData\Local\Temp\5DE9978A-3848-429E-8776-950FC869186F\20230607101602.zip" -DestinationPath "C:\Users\testuser\AppData\Local\Temp\5DE9978A-3848-429E-8776-950FC869186F\20230607101602"
  ```
2. Open the file in your preferred text editor. Run:
  ```powershell
  $ code <path-to-file>
  ```

Run:

```console
$ open /tmp/<your-diagnostics-ID>.zip
```

Run:

```console
$ unzip –l /tmp/<your-diagnostics-ID>.zip
```

#### Use your diagnostics ID to get help

If you have a paid Docker subscription, select **Contact support**. This opens the Docker Desktop support form. Fill in the information required and add the ID you copied in step three to the **Diagnostics ID field**. Then, select **Submit ticket** to request Docker Desktop support.

If you don't have a paid Docker subscription, create an issue on [GitHub](https://github.com/docker/desktop-feedback).

### Self-diagnose tool

> Important
>
> This tool has been deprecated.

## Check the logs

In addition to using the diagnose option to submit logs, you can browse the logs yourself.

In PowerShell, run:

```powershell
$ code $Env:LOCALAPPDATA\Docker\log
```

This opens up all the logs in your preferred text editor for you to explore.

### From terminal

To watch the live flow of Docker Desktop logs in the command line, run the following script from your preferred shell.

```console
$ pred='process matches ".*(ocker|vpnkit).*" || (process in {"taskgated-helper", "launchservicesd", "kernel"} && eventMessage contains[c] "docker")'
$ /usr/bin/log stream --style syslog --level=debug --color=always --predicate "$pred"
```

Alternatively, to collect the last day of logs (`1d`) in a file, run:

```console
$ /usr/bin/log show --debug --info --style syslog --last 1d --predicate "$pred" >/tmp/logs.txt
```

### From the Console app

Mac provides a built-in log viewer, named **Console**, which you can use to check
Docker logs.

The Console lives in `/Applications/Utilities`. You can search for it with
Spotlight Search.

To read the Docker app log messages, type `docker` in the Console window search bar and press Enter. Then select `ANY` to expand the drop-down list next to your `docker` search entry, and select `Process`.

![Mac Console search for Docker app](https://docs.docker.com/desktop/images/console.png)  ![Mac Console search for Docker app](https://docs.docker.com/desktop/images/console.png)

You can use the Console Log Query to search logs, filter the results in various
ways, and create reports.

You can access Docker Desktop logs by running the following command:

```console
$ journalctl --user --unit=docker-desktop
```

You can also find the logs for the internal components included in Docker
Desktop at `$HOME/.docker/desktop/log/`.

## View the Docker daemon logs

Refer to the
[Read the daemon logs](https://docs.docker.com/engine/daemon/logs/) section
to learn how to view the Docker Daemon logs.

## Further resources

- View specific [troubleshoot topics](https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/topics/).
- View information on [known issues](https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/known-issues/)
- [Fix "Docker.app is damaged" on macOS](https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/mac-damaged-dialog/) - Resolve macOS installation issues
- [Get support for Docker products](https://docs.docker.com/support/)

---

# Uninstall Docker Desktop

> How to uninstall Docker Desktop

# Uninstall Docker Desktop

---

> Warning
>
> Uninstalling Docker Desktop destroys Docker containers, images, volumes, and
> other Docker-related data local to the machine, and removes the files generated
> by the application. To learn how to preserve important data before uninstalling, refer to the
> [back up and restore data](https://docs.docker.com/desktop/settings-and-maintenance/backup-and-restore/) section.

#### From the GUI

1. From the Windows **Start** menu, select **Settings** > **Apps** > **Apps & features**.
2. Select **Docker Desktop** from the **Apps & features** list and then select **Uninstall**.
3. Select **Uninstall** to confirm your selection.

#### From the CLI

1. Locate the installer:
  ```console
  $ C:\Program Files\Docker\Docker\Docker Desktop Installer.exe
  ```
2. Uninstall Docker Desktop.

- In PowerShell, run:
  ```console
  $ Start-Process 'Docker Desktop Installer.exe' -Wait uninstall
  ```
- In the Command Prompt, run:
  ```console
  $ start /w "" "Docker Desktop Installer.exe" uninstall
  ```

After uninstalling Docker Desktop, some residual files may remain which you can remove manually. These are:

```console
C:\ProgramData\Docker
C:\ProgramData\DockerDesktop
C:\Program Files\Docker
C:\Users\<your user name>\AppData\Local\Docker
C:\Users\<your user name>\AppData\Roaming\Docker
C:\Users\<your user name>\AppData\Roaming\Docker Desktop
C:\Users\<your user name>\.docker
```

#### From the GUI

1. Open Docker Desktop.
2. In the top-right corner of the Docker Desktop Dashboard, select the **Troubleshoot** icon.
3. Select **Uninstall**.
4. When prompted, confirm by selecting **Uninstall** again.

You can then move the Docker application to the trash.

#### From the CLI

Run:

```console
$ /Applications/Docker.app/Contents/MacOS/uninstall
```

You can then move the Docker application to the trash.

> Note
>
> You may encounter the following error when uninstalling Docker Desktop using the uninstall command.
>
>
>
> ```console
> $ /Applications/Docker.app/Contents/MacOS/uninstall
> Password:
> Uninstalling Docker Desktop...
> Error: unlinkat /Users/USER_HOME/Library/Containers/com.docker.docker/.com.apple.containermanagerd.metadata.plist: > operation not permitted
> ```
>
>
>
> The operation not permitted error is reported either on the file `.com.apple.containermanagerd.metadata.plist` or on the parent directory `/Users/<USER_HOME>/Library/Containers/com.docker.docker/`. This error can be ignored as you have successfully uninstalled Docker Desktop.
> You can remove the directory `/Users/<USER_HOME>/Library/Containers/com.docker.docker/` later by allowing **Full Disk Access** to the terminal application you are using (**System Settings** > **Privacy & Security** > **Full Disk Access**).

After uninstalling Docker Desktop, some residual files may remain which you can remove:

```console
$ rm -rf ~/Library/Group\ Containers/group.com.docker
$ rm -rf ~/.docker
```

With Docker Desktop version 4.36 and earlier, the following files may also be left on the file system. You can remove these with administrative privileges:

```console
/Library/PrivilegedHelperTools/com.docker.vmnetd
/Library/PrivilegedHelperTools/com.docker.socket
```

To uninstall Docker Desktop for Ubuntu:

1. Remove the Docker Desktop application. Run:
  ```console
  $ sudo apt remove docker-desktop
  ```
  This removes the Docker Desktop package itself but doesn’t delete all of its files or settings.
2. Manually remove leftover file.
  ```console
  $ rm -r $HOME/.docker/desktop
  $ sudo rm /usr/local/bin/com.docker.cli
  $ sudo apt purge docker-desktop
  ```
  This removes configuration and data files at `$HOME/.docker/desktop`, the symlink at `/usr/local/bin/com.docker.cli`, and purges the remaining systemd service files.
3. Clean up Docker config settings. In `$HOME/.docker/config.json`, remove the `credsStore` and `currentContext` properties.
  These entries tell Docker where to store credentials and which context is active. If they remain after uninstalling Docker Desktop, they may conflict with a future Docker setup.

To uninstall Docker Desktop for Debian, run:

1. Remove the Docker Desktop application:
  ```console
  $ sudo apt remove docker-desktop
  ```
  This removes the Docker Desktop package itself but doesn’t delete all of its files or settings.
2. Manually remove leftover file.
  ```console
  $ rm -r $HOME/.docker/desktop
  $ sudo rm /usr/local/bin/com.docker.cli
  $ sudo apt purge docker-desktop
  ```
  This removes configuration and data files at `$HOME/.docker/desktop`, the symlink at `/usr/local/bin/com.docker.cli`, and purges the remaining systemd service files.
3. Clean up Docker config settings. In `$HOME/.docker/config.json`, remove the `credsStore` and `currentContext` properties.
  These entries tell Docker where to store credentials and which context is active. If they remain after uninstalling Docker Desktop, they may conflict with a future Docker setup.

To uninstall Docker Desktop for Fedora:

1. Remove the Docker Desktop application. Run:
  ```console
  $ sudo dnf remove docker-desktop
  ```
  This removes the Docker Desktop package itself but doesn’t delete all of its files or settings.
2. Manually remove leftover file.
  ```console
  $ rm -r $HOME/.docker/desktop
  $ sudo rm /usr/local/bin/com.docker.cli
  $ sudo dnf remove docker-desktop
  ```
  This removes configuration and data files at `$HOME/.docker/desktop`, the symlink at `/usr/local/bin/com.docker.cli`, and purges the remaining systemd service files.
3. Clean up Docker config settings. In `$HOME/.docker/config.json`, remove the `credsStore` and `currentContext` properties.
  These entries tell Docker where to store credentials and which context is active. If they remain after uninstalling Docker Desktop, they may conflict with a future Docker setup.

To uninstall Docker Desktop for Arch:

1. Remove the Docker Desktop application. Run:
  ```console
  $ sudo pacman -Rns docker-desktop
  ```
  This removes the Docker Desktop package along with its configuration files and dependencies not required by other packages.
2. Manually remove leftover files.
  ```console
  $ rm -r $HOME/.docker/desktop
  ```
  This removes configuration and data files at `$HOME/.docker/desktop`.
3. Clean up Docker config settings. In `$HOME/.docker/config.json`, remove the `credsStore` and `currentContext` properties.
  These entries tell Docker where to store credentials and which context is active. If they remain after uninstalling Docker Desktop, they may conflict with a future Docker setup.

---

# Explore the Builds view in Docker Desktop

> Understand how to use the Builds view in Docker Desktop

# Explore the Builds view in Docker Desktop

   Table of contents

---

The **Builds** view provides an interactive interface for inspecting build history, monitoring active builds, and managing builders directly in Docker Desktop.

By default, the **Build history** tab displays a list of completed builds, sorted by date (newest first). Switch to the **Active builds** tab to view ongoing builds.

If you're connected to a cloud builder through [Docker Build Cloud](https://docs.docker.com/build-cloud/),
the Builds view also lists any active or completed cloud builds by other team members
connected to the same cloud builder.

> Note
>
> When building Windows container images using the `docker build` command, the legacy builder is used which does not populate the **Builds** view. To switch to using BuildKit, you can either:
>
>
>
> - Set `DOCKER_BUILDKIT=1` in the build command, such as `DOCKER_BUILDKIT=1 docker build .` or
> - Use the `docker buildx build` command

## Show build list

Open the **Builds** view from the Docker Dashboard to access:

- **Build history**: Completed builds with access to logs, dependencies, traces, and more
- **Active builds**: Builds currently in progress

Only builds from active, running builders are listed. Builds from removed or stopped builders are not shown.

### Builder settings

The top-right corner shows the name of your currently selected builder, and the
**Builder settings** button lets you [manage builders](#manage-builders) in the
Docker Desktop settings.

### Import builds

Availability: Beta
Requires: Docker Desktop
[4.31](https://docs.docker.com/desktop/release-notes/#4310) and later

The **Import builds** button lets you import build records for builds by other
people, or builds in a CI environment. When you've imported a build record, it
gives you full access to the logs, traces, and other data for that build,
directly in Docker Desktop.

The
[build summary](https://docs.docker.com/build/ci/github-actions/build-summary/)
for the `docker/build-push-action` and `docker/bake-action` GitHub Actions
includes a link to download the build records, for inspecting CI jobs with
Docker Desktop.

## Inspect builds

To inspect a build, select the build that you want to view in the list.
The inspection view contains a number of tabs.

The **Info** tab displays details about the build.

If you're inspecting a multi-platform build, the drop-down menu in the
top-right of this tab lets you filter the information down to a specific
platform:

The **Source details** section shows information about the frontend
[frontend](https://docs.docker.com/build/buildkit/frontend/) and, if available,
the source code repository used for the build.

### Build timing

The **Build timing** section of the Info tab contains charts
showing a breakdown of the build execution from various angles.

- **Real time** refers to the wall-clock time that it took to complete the build.
- **Accumulated time** shows the total CPU time for all steps.
- **Cache usage** shows the extent to which build operations were cached.
- **Parallel execution** shows how much of the build execution time was spent running steps in parallel.

The chart colors and legend keys describe the different build operations. Build
operations are defined as follows:

| Build operation | Description |
| --- | --- |
| Local file transfers | Time spent transferring local files from the client to the builder. |
| File operations | Any operations that involve creating and copying files in the build. For example, theCOPY,WORKDIR,ADDinstructions in a Dockerfile frontend all incur file operations. |
| Image pulls | Time spent pulling images. |
| Executions | Container executions, for example commands defined asRUNinstructions in a Dockerfile frontend. |
| HTTP | Remote artifact downloads usingADD. |
| Git | Same asHTTPbut for Git URLs. |
| Result exports | Time spent exporting the build results. |
| SBOM | Time spent generating theSBOM attestation. |
| Idle | Idle time for build workers, which can happen if you have configured amax parallelism limit. |

### Build dependencies

The **Dependencies** section shows images and remote resources used during
the build. Resources listed here include:

- Container images used during the build
- Git repositories included using the `ADD` Dockerfile instruction
- Remote HTTPS resources included using the `ADD` Dockerfile instruction

### Arguments, secrets, and other parameters

The **Configuration** section of the Info tab shows parameters passed to the build:

- Build arguments, including the resolved value
- Secrets, including their IDs (but not their values)
- SSH sockets
- Labels
- [Additional contexts](https://docs.docker.com/reference/cli/docker/buildx/build/#build-context)

### Outputs and artifacts

The **Build results** section shows a summary of the generated build artifacts,
including image manifest details, attestations, and build traces.

Attestations are metadata records attached to a container image.
The metadata describes something about the image,
for example how it was built or what packages it contains.
For more information about attestations, see
[Build attestations](https://docs.docker.com/build/metadata/attestations/).

Build traces capture information about the build execution steps in Buildx and
BuildKit. The traces are available in two formats: OTLP and Jaeger. You can
download build traces from Docker Desktop by opening the actions menu and
selecting the format you want to download.

#### Inspect build traces with Jaeger

Using a Jaeger client, you can import and inspect build traces from Docker
Desktop. The following steps show you how to export a trace from Docker Desktop
and view it in [Jaeger](https://www.jaegertracing.io/):

1. Start Jaeger UI:
  ```console
  $ docker run -d --name jaeger -p "16686:16686" jaegertracing/all-in-one
  ```
2. Open the Builds view in Docker Desktop, and select a completed build.
3. Navigate to the **Build results** section, open the actions menu and select **Download as Jaeger format**.
4. Go to [http://localhost:16686](http://localhost:16686) in your browser to open Jaeger UI.
5. Select the **Upload** tab and open the Jaeger build trace you just exported.

Now you can analyze the build trace using the Jaeger UI:

![Jaeger UI screenshot](https://docs.docker.com/desktop/images/build-ui-jaeger-screenshot.png)Screenshot of a build trace in the Jaeger UI ![Jaeger UI screenshot](https://docs.docker.com/desktop/images/build-ui-jaeger-screenshot.png)

### Dockerfile source and errors

When inspecting a successful completed build or an ongoing active build,
the **Source** tab shows the
[frontend](https://docs.docker.com/build/buildkit/frontend/)
used to create the build.

If the build failed, an **Error** tab displays instead of the **Source** tab.
The error message is inlined in the Dockerfile source,
indicating where the failure happened and why.

### Build logs

The **Logs** tab displays the build logs.
For active builds, the logs are updated in real-time.

You can toggle between a **List view** and a **Plain-text view** of a build log.

- The **List view** presents all build steps in a collapsible format,
  with a timeline for navigating the log along a time axis.
- The **Plain-text view** displays the log as plain text.

The **Copy** button lets you copy the plain-text version of the log to your clipboard.

### Build history

The **History** tab displays statistics data about completed builds.

The time series chart illustrates trends in duration, build steps, and cache usage for related builds,
helping you identify patterns and shifts in build operations over time.
For instance, significant spikes in build duration or a high number of cache misses
could signal opportunities for optimizing the Dockerfile.

You can navigate to and inspect a related build by selecting it in the chart,
or using the **Past builds** list below the chart.

## Manage builders

The **Builder** tab in **Settings** lets you:

- Inspect the state and configuration of active builders
- Start and stop a builder
- Delete build history
- Add or remove builders (or connect and disconnect, in the case of cloud builders)

For more information about managing builders, see
[Change settings](https://docs.docker.com/desktop/settings-and-maintenance/settings/#builders)
