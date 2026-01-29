# Install Docker Desktop on Debian and more

# Install Docker Desktop on Debian

> Instructions for installing Docker Desktop on Debian

# Install Docker Desktop on Debian

   Table of contents

---

> **Docker Desktop terms**
>
>
>
> Commercial use of Docker Desktop in larger enterprises (more than 250
> employees OR more than $10 million USD in annual revenue) requires a [paid
> subscription](https://www.docker.com/pricing/).

This page contains information on how to install, launch, and upgrade Docker Desktop on a Debian distribution.

## Prerequisites

To install Docker Desktop successfully, you must:

- Meet the [general system requirements](https://docs.docker.com/desktop/setup/install/linux/#general-system-requirements).
- Have a 64-bit version of Debian 12.
- For a Gnome Desktop environment, you must also install AppIndicator and KStatusNotifierItem [Gnome extensions](https://extensions.gnome.org/extension/615/appindicator-support/).
- If you're not using GNOME, you must install `gnome-terminal` to enable terminal access from Docker Desktop:
  ```console
  $ sudo apt install gnome-terminal
  ```

## Install Docker Desktop

Recommended approach to install Docker Desktop on Debian:

1. Set up Docker's `apt` repository.
  See step one of
  [Install using theaptrepository](https://docs.docker.com/engine/install/debian/#install-using-the-repository).
2. Download the latest [DEB package](https://desktop.docker.com/linux/main/amd64/docker-desktop-amd64.deb?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-linux-amd64). For checksums, see the
  [Release notes](https://docs.docker.com/desktop/release-notes/).
3. Install the package using `apt`:

```console
$ sudo apt-get update
$ sudo apt-get install ./docker-desktop-amd64.deb
```

> Note
>
> At the end of the installation process, `apt` displays an error due to installing a downloaded package. You
> can ignore this error message.
>
>
>
> ```text
> N: Download is performed unsandboxed as root, as file '/home/user/Downloads/docker-desktop.deb' couldn't be accessed by user '_apt'. - pkgAcquire::Run (13: Permission denied)
> ```

By default, Docker Desktop is installed at `/opt/docker-desktop`.

The RPM package includes a post-install script that completes additional setup steps automatically.

The post-install script:

- Sets the capability on the Docker Desktop binary to map privileged ports and set resource limits.
- Adds a DNS name for Kubernetes to `/etc/hosts`.
- Creates a symlink from `/usr/local/bin/com.docker.cli` to `/usr/bin/docker`.
  This is because the classic Docker CLI is installed at `/usr/bin/docker`. The Docker Desktop installer also installs a Docker CLI binary that includes cloud-integration capabilities and is essentially a wrapper for the Compose CLI, at`/usr/local/bin/com.docker.cli`. The symlink ensures that the wrapper can access the classic Docker CLI.

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

## Upgrade Docker Desktop

Once a new version for Docker Desktop is released, the Docker UI shows a notification.
You need to download the new package each time you want to upgrade Docker Desktop and run:

```console
$ sudo apt-get install ./docker-desktop-amd64.deb
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

---

# Install Docker Desktop on Fedora

> Instructions for installing Docker Desktop on Fedora

# Install Docker Desktop on Fedora

   Table of contents

---

> **Docker Desktop terms**
>
>
>
> Commercial use of Docker Desktop in larger enterprises (more than 250
> employees OR more than $10 million USD in annual revenue) requires a [paid
> subscription](https://www.docker.com/pricing/).

This page contains information on how to install, launch and upgrade Docker Desktop on a Fedora distribution.

## Prerequisites

To install Docker Desktop successfully, you must:

- Meet the [general system requirements](https://docs.docker.com/desktop/setup/install/linux/#general-system-requirements).
- Have a 64-bit version of Fedora 41 or Fedora 42.
- For a GNOME desktop environment you must install AppIndicator and KStatusNotifierItem [GNOME extensions](https://extensions.gnome.org/extension/615/appindicator-support/).
- If you're not using GNOME, you must install `gnome-terminal` to enable terminal access from Docker Desktop:
  ```console
  $ sudo dnf install gnome-terminal
  ```

## Install Docker Desktop

To install Docker Desktop on Fedora:

1. Set up
  [Docker's package repository](https://docs.docker.com/engine/install/fedora/#set-up-the-repository).
2. Download the latest [RPM package](https://desktop.docker.com/linux/main/amd64/docker-desktop-x86_64.rpm?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-linux-amd64). For checksums, see the
  [Release notes](https://docs.docker.com/desktop/release-notes/).
3. Install the package with dnf as follows:
  ```console
  $ sudo dnf install ./docker-desktop-x86_64.rpm
  ```
  By default, Docker Desktop is installed at `/opt/docker-desktop`.

The RPM package includes a post-install script that completes additional setup steps automatically.

The post-install script:

- Sets the capability on the Docker Desktop binary to map privileged ports and set resource limits.
- Adds a DNS name for Kubernetes to `/etc/hosts`.
- Creates a symlink from `/usr/local/bin/com.docker.cli` to `/usr/bin/docker`.
  This is because the classic Docker CLI is installed at `/usr/bin/docker`. The Docker Desktop installer also installs a Docker CLI binary that includes cloud-integration capabilities and is essentially a wrapper for the Compose CLI, at`/usr/local/bin/com.docker.cli`. The symlink ensures that the wrapper can access the classic Docker CLI.

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

## Upgrade Docker Desktop

Once a new version for Docker Desktop is released, the Docker UI shows a notification.
You need to first remove the previous version and then download the new package each time you want to upgrade Docker Desktop. Run:

```console
$ sudo dnf remove docker-desktop
$ sudo dnf install ./docker-desktop-x86_64.rpm
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

---

# Install Docker Desktop on RHEL

> Instructions for installing Docker Desktop on RHEL

# Install Docker Desktop on RHEL

   Table of contents

---

> **Docker Desktop terms**
>
>
>
> Commercial use of Docker Desktop in larger enterprises (more than 250
> employees or more than $10 million USD in annual revenue) requires a [paid
> subscription](https://www.docker.com/pricing/).

This page contains information on how to install, launch and upgrade Docker Desktop on a Red Hat Enterprise Linux (RHEL) distribution.

## Prerequisites

To install Docker Desktop successfully, you must:

- Meet the [general system requirements](https://docs.docker.com/desktop/setup/install/linux/#general-system-requirements).
- Have a 64-bit version of either RHEL 8 or RHEL 9.
- If `pass` is not installed, or it can't be installed, you must enable [CodeReady Linux Builder (CRB) repository](https://access.redhat.com/articles/4348511) and [Extra Packages for Enterprise Linux (EPEL)](https://docs.fedoraproject.org/en-US/epel/).
  ```console
  $ sudo subscription-manager repos --enable codeready-builder-for-rhel-9-$(arch)-rpms
  $ sudo dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm
  $ sudo dnf install pass
  ```
  ```console
  $ sudo subscription-manager repos --enable codeready-builder-for-rhel-8-$(arch)-rpms
  $ sudo dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm
  $ sudo dnf install pass
  ```
- For a GNOME desktop environment you must install AppIndicator and KStatusNotifierItem [GNOME extensions](https://extensions.gnome.org/extension/615/appindicator-support/). You must also enable EPEL.
  ```console
  $ # enable EPEL as described above
  $ sudo dnf install gnome-shell-extension-appindicator
  $ sudo gnome-extensions enable appindicatorsupport@rgcjonas.gmail.com
  ```
  ```console
  $ # enable EPEL as described above
  $ sudo dnf install gnome-shell-extension-appindicator
  $ sudo dnf install gnome-shell-extension-desktop-icons
  $ sudo gnome-shell-extension-tool -e appindicatorsupport@rgcjonas.gmail.com
  ```
- If you're not using GNOME, you must install `gnome-terminal` to enable terminal access from Docker Desktop:
  ```console
  $ sudo dnf install gnome-terminal
  ```

## Install Docker Desktop

To install Docker Desktop on RHEL:

1. Set up Docker's package repository as follows:
  ```console
  $ sudo dnf config-manager --add-repo https://download.docker.com/linux/rhel/docker-ce.repo
  ```
2. Download the latest [RPM package](https://desktop.docker.com/linux/main/amd64/docker-desktop-x86_64-rhel.rpm?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-linux-amd64).
3. Install the package with dnf as follows:
  ```console
  $ sudo dnf install ./docker-desktop-x86_64-rhel.rpm
  ```

The RPM package includes a post-install script that completes additional setup steps automatically.

The post-install script:

- Sets the capability on the Docker Desktop binary to map privileged ports and set resource limits.
- Adds a DNS name for Kubernetes to `/etc/hosts`.
- Creates a symlink from `/usr/local/bin/com.docker.cli` to `/usr/bin/docker`.
  This is because the classic Docker CLI is installed at `/usr/bin/docker`. The Docker Desktop installer also installs a Docker CLI binary that includes cloud-integration capabilities and is essentially a wrapper for the Compose CLI, at `/usr/local/bin/com.docker.cli`. The symlink ensures that the wrapper can access the classic Docker CLI.
- Creates a symlink from `/usr/libexec/qemu-kvm` to `/usr/local/bin/qemu-system-x86_64`.

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

> Tip
>
> To attach Red Hat subscription data to containers, see [Red Hat verified solution](https://access.redhat.com/solutions/5870841).
>
>
>
> For example:
>
>
>
> ```console
> $ docker run --rm -it -v "/etc/pki/entitlement:/etc/pki/entitlement" -v "/etc/rhsm:/etc/rhsm-host" -v "/etc/yum.repos.d/redhat.repo:/etc/yum.repos.d/redhat.repo" registry.access.redhat.com/ubi9
> ```

## Upgrade Docker Desktop

Once a new version for Docker Desktop is released, the Docker UI shows a notification.
You need to first remove the previous version and then download the new package each time you want to upgrade Docker Desktop. Run:

```console
$ sudo dnf remove docker-desktop
$ sudo dnf install ./docker-desktop-<arch>-rhel.rpm
```

## Next steps

- Review [Docker's subscriptions](https://www.docker.com/pricing/) to see what Docker can offer you.
- Take a look at the
  [Docker workshop](https://docs.docker.com/get-started/workshop/) to learn how to build an image and run it as a containerized application.
- [Explore Docker Desktop](https://docs.docker.com/desktop/use-desktop/) and all its features.
- [Troubleshooting](https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/) describes common problems, workarounds, how to run and submit diagnostics, and submit issues.
- [FAQs](https://docs.docker.com/desktop/troubleshoot-and-support/faqs/general/) provide answers to frequently asked questions.
- [Release notes](https://docs.docker.com/desktop/release-notes/) lists component updates, new features, and improvements associated with Docker Desktop releases.
- [Back up and restore data](https://docs.docker.com/desktop/settings-and-maintenance/backup-and-restore/) provides instructions
  on backing up and restoring data related to Docker.

---

# Install Docker Desktop on Ubuntu

> Learn how to install, launch, and upgrade Docker Desktop on Ubuntu. This quick guide will cover prerequisites, installation methods, and more.

# Install Docker Desktop on Ubuntu

   Table of contents

---

> **Docker Desktop terms**
>
>
>
> Commercial use of Docker Desktop in larger enterprises (more than 250
> employees or more than $10 million USD in annual revenue) requires a [paid
> subscription](https://www.docker.com/pricing/).

This page contains information on how to install, launch and upgrade Docker Desktop on an Ubuntu distribution.

## Prerequisites

To install Docker Desktop successfully, you must:

- Meet the [general system requirements](https://docs.docker.com/desktop/setup/install/linux/#general-system-requirements).
- Have an x86-64 system with Ubuntu 22.04, 24.04, or the latest non-LTS version.
- If you're not using GNOME, you must install `gnome-terminal` to enable terminal access from Docker Desktop:
  ```console
  $ sudo apt install gnome-terminal
  ```

## Install Docker Desktop

Recommended approach to install Docker Desktop on Ubuntu:

1. Set up Docker's package repository.
  See step one of
  [Install using theaptrepository](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository).
2. Download the latest [DEB package](https://desktop.docker.com/linux/main/amd64/docker-desktop-amd64.deb?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-linux-amd64). For checksums, see the
  [Release notes](https://docs.docker.com/desktop/release-notes/).
3. Install the package using `apt`:
  ```console
  $ sudo apt-get update
  $ sudo apt install ./docker-desktop-amd64.deb
  ```
  > Note
  >
  > At the end of the installation process, `apt` displays an error due to installing a downloaded package. You
  > can ignore this error message.
  >
  >
  >
  > ```text
  > N: Download is performed unsandboxed as root, as file '/home/user/Downloads/docker-desktop.deb' couldn't be accessed by user '_apt'. - pkgAcquire::Run (13: Permission denied)
  > ```
  By default, Docker Desktop is installed at `/opt/docker-desktop`.

The DEB package includes a post-install script that completes additional setup steps automatically.

The post-install script:

- Sets the capability on the Docker Desktop binary to map privileged ports and set resource limits.
- Adds a DNS name for Kubernetes to `/etc/hosts`.
- Creates a symlink from `/usr/local/bin/com.docker.cli` to `/usr/bin/docker`.
  This is because the classic Docker CLI is installed at `/usr/bin/docker`. The Docker Desktop installer also installs a Docker CLI binary that includes cloud-integration capabilities and is essentially a wrapper for the Compose CLI, at `/usr/local/bin/com.docker.cli`. The symlink ensures that the wrapper can access the classic Docker CLI.

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

## Upgrade Docker Desktop

When a new version for Docker Desktop is released, the Docker UI shows a notification.
You need to download the new package each time you want to upgrade Docker Desktop and run:

```console
$ sudo apt install ./docker-desktop-amd64.deb
```

## Next steps

- Review [Docker's subscriptions](https://www.docker.com/pricing/) to see what Docker can offer you.
- Follow the
  [Docker workshop](https://docs.docker.com/get-started/workshop/) to learn how to build an image and run it as a containerized application.
- [Explore Docker Desktop](https://docs.docker.com/desktop/use-desktop/) and all its features.
- [Troubleshooting](https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/) describes common problems, workarounds, how to run and submit diagnostics, and submit issues.
- [FAQs](https://docs.docker.com/desktop/troubleshoot-and-support/faqs/general/) provide answers to frequently asked questions.
- [Release notes](https://docs.docker.com/desktop/release-notes/) lists component updates, new features, and improvements associated with Docker Desktop releases.
- [Back up and restore data](https://docs.docker.com/desktop/settings-and-maintenance/backup-and-restore/) provides instructions
  on backing up and restoring data related to Docker.

---

# Install Docker Desktop on Linux

> Install Docker on Linux with ease using our step-by-step installation guide covering system requirements, supported platforms, and where to go next.

# Install Docker Desktop on Linux

   Table of contents

---

> **Docker Desktop terms**
>
>
>
> Commercial use of Docker Desktop in larger enterprises (more than 250
> employees or more than $10 million USD in annual revenue) requires a [paid
> subscription](https://www.docker.com/pricing/).

This page contains information about general system requirements, supported platforms, and instructions on how to install Docker Desktop for Linux.

> Important
>
> Docker Desktop on Linux runs a Virtual Machine (VM) which creates and uses a custom docker context, `desktop-linux`, on startup.
>
>
>
> This means images and containers deployed on the Linux Docker Engine (before installation) are not available in Docker Desktop for Linux.
>
>
>
> > Important
> >
> > For commercial use of Docker Engine obtained via Docker Desktop within larger enterprises (exceeding 250 employees or with annual revenue surpassing $10 million USD), a [paid subscription](https://www.docker.com/pricing/) is required.
>
>
>
> Docker Desktop for Linux provides a user-friendly graphical interface that simplifies the management of containers and services. It includes Docker Engine as this is the core technology that powers Docker containers. Docker Desktop for Linux also comes with additional features like Docker Scout and Docker Extensions.
>
>
>
> #### Installing Docker Desktop and Docker Engine
>
>
>
> Docker Desktop for Linux and Docker Engine can be installed side-by-side on the
> same machine. Docker Desktop for Linux stores containers and images in an isolated
> storage location within a VM and offers
> controls to restrict
> [its resources](https://docs.docker.com/desktop/settings-and-maintenance/settings/#resources). Using a dedicated storage
> location for Docker Desktop prevents it from interfering with a Docker Engine
> installation on the same machine.
>
>
>
> While it's possible to run both Docker Desktop and Docker Engine simultaneously,
> there may be situations where running both at the same time can cause issues.
> For example, when mapping network ports (`-p` / `--publish`) for containers, both
> Docker Desktop and Docker Engine may attempt to reserve the same port on your
> machine, which can lead to conflicts ("port already in use").
>
>
>
> We generally recommend stopping the Docker Engine while you're using Docker Desktop
> to prevent the Docker Engine from consuming resources and to prevent conflicts
> as described above.
>
>
>
> Use the following command to stop the Docker Engine service:
>
>
>
> ```console
> $ sudo systemctl stop docker docker.socket containerd
> ```
>
>
>
> Depending on your installation, the Docker Engine may be configured to automatically
> start as a system service when your machine starts. Use the following command to
> disable the Docker Engine service, and to prevent it from starting automatically:
>
>
>
> ```console
> $ sudo systemctl disable docker docker.socket containerd
> ```
>
>
>
> ### Switching between Docker Desktop and Docker Engine
>
>
>
> The Docker CLI can be used to interact with multiple Docker Engines. For example,
> you can use the same Docker CLI to control a local Docker Engine and to control
> a remote Docker Engine instance running in the cloud.
> [Docker Contexts](https://docs.docker.com/engine/manage-resources/contexts/)
> allow you to switch between Docker Engines instances.
>
>
>
> When installing Docker Desktop, a dedicated "desktop-linux" context is created to
> interact with Docker Desktop. On startup, Docker Desktop automatically sets its
> own context (`desktop-linux`) as the current context. This means that subsequent
> Docker CLI commands target Docker Desktop. On shutdown, Docker Desktop resets
> the current context to the `default` context.
>
>
>
> Use the `docker context ls` command to view what contexts are available on your
> machine. The current context is indicated with an asterisk (`*`).
>
>
>
> ```console
> $ docker context ls
> NAME            DESCRIPTION                               DOCKER ENDPOINT                                  ...
> default *       Current DOCKER_HOST based configuration   unix:///var/run/docker.sock                      ...
> desktop-linux                                             unix:///home/<user>/.docker/desktop/docker.sock  ...
> ```
>
>
>
> If you have both Docker Desktop and Docker Engine installed on the same machine,
> you can run the `docker context use` command to switch between the Docker Desktop
> and Docker Engine contexts. For example, use the "default" context to interact
> with the Docker Engine:
>
>
>
> ```console
> $ docker context use default
> default
> Current context is now "default"
> ```
>
>
>
> And use the `desktop-linux` context to interact with Docker Desktop:
>
>
>
> ```console
> $ docker context use desktop-linux
> desktop-linux
> Current context is now "desktop-linux"
> ```
>
>
>
> Refer to the
> [Docker Context documentation](https://docs.docker.com/engine/manage-resources/contexts/) for more details.

## Supported platforms

Docker provides `.deb` and `.rpm` packages for the following Linux distributions
and architectures:

| Platform | x86_64 / amd64 |
| --- | --- |
| Ubuntu | ✅ |
| Debian | ✅ |
| Red Hat Enterprise Linux (RHEL) | ✅ |
| Fedora | ✅ |

An experimental package is available for [Arch](https://docs.docker.com/desktop/setup/install/linux/archlinux/)-based distributions. Docker has not tested or verified the installation.

Docker supports Docker Desktop on the current LTS release of the aforementioned distributions and the most recent version. As new versions are made available, Docker stops supporting the oldest version and supports the newest version.

## General system requirements

To install Docker Desktop successfully, your Linux host must meet the following general requirements:

- 64-bit kernel and CPU support for virtualization.
- KVM virtualization support. Follow the [KVM virtualization support instructions](#kvm-virtualization-support) to check if the KVM kernel modules are enabled and how to provide access to the KVM device.
- QEMU must be version 5.2 or later. We recommend upgrading to the latest version.
- systemd init system.
- GNOME, KDE, or MATE desktop environments are supported but others may work.
  - For many Linux distributions, the GNOME environment does not support tray icons. To add support for tray icons, you need to install a GNOME extension. For example, [AppIndicator](https://extensions.gnome.org/extension/615/appindicator-support/).
- At least 4 GB of RAM.
- Enable configuring ID mapping in user namespaces, see
  [File sharing](https://docs.docker.com/desktop/troubleshoot-and-support/faqs/linuxfaqs/#how-do-i-enable-file-sharing). Note that for Docker Desktop version 4.35 and later, this is not required anymore.
- Recommended:
  [Initializepass](https://docs.docker.com/desktop/setup/sign-in/#credentials-management-for-linux-users) for credentials management.

Docker Desktop for Linux runs a Virtual Machine (VM). For more information on why, see
[Why Docker Desktop for Linux runs a VM](https://docs.docker.com/desktop/troubleshoot-and-support/faqs/linuxfaqs/#why-does-docker-desktop-for-linux-run-a-vm).

> Note
>
> Docker does not provide support for running Docker Desktop for Linux in nested virtualization scenarios. We recommend that you run Docker Desktop for Linux natively on supported distributions.

### KVM virtualization support

Docker Desktop runs a VM that requires [KVM support](https://www.linux-kvm.org).

The `kvm` module should load automatically if the host has virtualization support. To load the module manually, run:

```console
$ modprobe kvm
```

Depending on the processor of the host machine, the corresponding module must be loaded:

```console
$ modprobe kvm_intel  # Intel processors

$ modprobe kvm_amd    # AMD processors
```

If the above commands fail, you can view the diagnostics by running:

```console
$ kvm-ok
```

To check if the KVM modules are enabled, run:

```console
$ lsmod | grep kvm
kvm_amd               167936  0
ccp                   126976  1 kvm_amd
kvm                  1089536  1 kvm_amd
irqbypass              16384  1 kvm
```

#### Set up KVM device user permissions

To check ownership of `/dev/kvm`, run :

```console
$ ls -al /dev/kvm
```

Add your user to the kvm group in order to access the kvm device:

```console
$ sudo usermod -aG kvm $USER
```

Sign out and sign back in so that your group membership is re-evaluated.

## Where to go next

- Install Docker Desktop for Linux for your specific Linux distribution:
  - [Install on Ubuntu](https://docs.docker.com/desktop/setup/install/linux/ubuntu/)
  - [Install on Debian](https://docs.docker.com/desktop/setup/install/linux/debian/)
  - [Install on Red Hat Enterprise Linux (RHEL)](https://docs.docker.com/desktop/setup/install/linux/rhel/)
  - [Install on Fedora](https://docs.docker.com/desktop/setup/install/linux/fedora/)
  - [Install on Arch](https://docs.docker.com/desktop/setup/install/linux/archlinux/)

---

# Install Docker Desktop on Mac

> Install Docker Desktop for Mac to get started. This guide covers system requirements, where to download, and instructions on how to install and update.

# Install Docker Desktop on Mac

   Table of contents

---

> **Docker Desktop terms**
>
>
>
> Commercial use of Docker Desktop in larger enterprises (more than 250
> employees or more than $10 million USD in annual revenue) requires a [paid
> subscription](https://www.docker.com/pricing/).

This page provides download links, system requirements, and step-by-step installation instructions for Docker Desktop on Mac.

[Docker Desktop for Mac with Apple silicon](https://desktop.docker.com/mac/main/arm64/Docker.dmg?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-mac-arm64) [Docker Desktop for Mac with Intel chip](https://desktop.docker.com/mac/main/amd64/Docker.dmg?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-mac-amd64)

*For checksums, seeRelease notes.*

## System requirements

- A supported version of macOS.
  > Important
  >
  > Docker Desktop is supported on the current and two previous major macOS releases. As new major versions of macOS are made generally available, Docker stops supporting the oldest version and supports the newest version of macOS (in addition to the previous two releases).
- At least 4 GB of RAM.

- A supported version of macOS.
  > Important
  >
  > Docker Desktop is supported on the current and two previous major macOS releases. As new major versions of macOS are made generally available, Docker stops supporting the oldest version and supports the newest version of macOS (in addition to the previous two releases).
- At least 4 GB of RAM.
- For the best experience, it's recommended that you install Rosetta 2. Rosetta 2 is no longer strictly required, however there are a few optional command line tools that still require Rosetta 2 when using Darwin/AMD64. See
  [Known issues](https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/known-issues/). To install Rosetta 2 manually from the command line, run the following command:
  ```console
  $ softwareupdate --install-rosetta
  ```

> **Before you install or update**
>
>
>
> - Quit tools that might call Docker in the background (Visual Studio Code, terminals, agent apps).
> - If you manage fleets or install via MDM, use the
>   [PKG installer](https://docs.docker.com/enterprise/enterprise-deployment/pkg-install-and-configure/).
> - Keep the installer volume mounted until the installation completes.
>
>
>
> If you encounter a "Docker.app is damaged" dialog, see
> [Fix "Docker.app is damaged" on macOS](https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/mac-damaged-dialog/).

## Install and run Docker Desktop on Mac

> Tip
>
> See the
> [FAQs](https://docs.docker.com/desktop/troubleshoot-and-support/faqs/general/#how-do-I-run-docker-desktop-without-administrator-privileges) on how to install and run Docker Desktop without needing administrator privileges.

### Install interactively

1. Download the installer using the download buttons at the top of the page, or from the
  [release notes](https://docs.docker.com/desktop/release-notes/).
2. Double-click `Docker.dmg` to open the installer, then drag the Docker icon to the **Applications** folder. By default, Docker Desktop is installed at `/Applications/Docker.app`.
3. Double-click `Docker.app` in the **Applications** folder to start Docker.
4. The Docker menu displays the Docker Subscription Service Agreement.
  Here’s a summary of the key points:
  - Docker Desktop is free for small businesses (fewer than 250 employees AND less than $10 million in annual revenue), personal use, education, and non-commercial open source projects.
  - Otherwise, it requires a paid subscription for professional use.
  - Paid subscriptions are also required for government entities.
  - Docker Pro, Team, and Business subscriptions include commercial use of Docker Desktop.
5. Select **Accept** to continue.
  Note that Docker Desktop won't run if you do not agree to the terms. You can choose to accept the terms at a later date by opening Docker Desktop.
  For more information, see [Docker Desktop Subscription Service Agreement](https://www.docker.com/legal/docker-subscription-service-agreement). It is recommended that you also read the [FAQs](https://www.docker.com/pricing/faq).
6. From the installation window, select either:
  - **Use recommended settings (Requires password)**. This lets Docker Desktop automatically set the necessary configuration settings.
  - **Use advanced settings**. You can then set the location of the Docker CLI tools either in the system or user directory, enable the default Docker socket, and enable privileged port mapping. See
    [Settings](https://docs.docker.com/desktop/settings-and-maintenance/settings/#advanced), for more information and how to set the location of the Docker CLI tools.
7. Select **Finish**. If you have applied any of the previous configurations that require a password in step 6, enter your password to confirm your choice.

### Install from the command line

After downloading `Docker.dmg` from either the download buttons at the top of the page or from the
[release notes](https://docs.docker.com/desktop/release-notes/), run the following commands in a terminal to install Docker Desktop in the **Applications** folder:

```console
$ sudo hdiutil attach Docker.dmg
$ sudo /Volumes/Docker/Docker.app/Contents/MacOS/install
$ sudo hdiutil detach /Volumes/Docker
```

By default, Docker Desktop is installed at `/Applications/Docker.app`. As macOS typically performs security checks the first time an application is used, the `install` command can take several minutes to run.

#### Installer flags

The `install` command accepts the following flags:

##### Installation behavior

- `--accept-license`: Accepts the [Docker Subscription Service Agreement](https://www.docker.com/legal/docker-subscription-service-agreement) now, rather than requiring it to be accepted when the application is first run.
- `--user=<username>`: Performs the privileged configurations once during installation. This removes the need for the user to grant root privileges on first run. For more information, see
  [Privileged helper permission requirements](https://docs.docker.com/desktop/setup/install/mac-permission-requirements/#permission-requirements). To find the username, enter `ls /Users` in the CLI.

##### Security and access

- `--allowed-org=<org name>`: Requires the user to sign in and be part of the specified Docker Hub organization when running the application
- `--user=<username>`: Performs the privileged configurations once during installation. This removes the need for the user to grant root privileges on first run. For more information, see
  [Privileged helper permission requirements](https://docs.docker.com/desktop/setup/install/mac-permission-requirements/#permission-requirements). To find the username, enter `ls /Users` in the CLI.
- `--admin-settings`: Automatically creates an `admin-settings.json` file which is used by administrators to control certain Docker Desktop settings on client machines within their organization. For more information, see
  [Settings Management](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/).
  - It must be used together with the `--allowed-org=<org name>` flag.
  - For example: `--allowed-org=<org name> --admin-settings="{'configurationFileVersion': 2, 'enhancedContainerIsolation': {'value': true, 'locked': false}}"`

##### Proxy configuration

- `--proxy-http-mode=<mode>`: Sets the HTTP Proxy mode. The two modes are `system` (default) or `manual`.
- `--override-proxy-http=<URL>`: Sets the URL of the HTTP proxy that must be used for outgoing HTTP requests. It requires `--proxy-http-mode` to be `manual`.
- `--override-proxy-https=<URL>`: Sets the URL of the HTTP proxy that must be used for outgoing HTTPS requests, requires `--proxy-http-mode` to be `manual`
- `--override-proxy-exclude=<hosts/domains>`: Bypasses proxy settings for the hosts and domains. It's a comma-separated list.
- `--override-proxy-pac=<PAC file URL>`: Sets the PAC file URL. This setting takes effect only when using `manual` proxy mode.
- `--override-proxy-embedded-pac=<PAC script>`: Specifies an embedded PAC (Proxy Auto-Config) script. This setting takes effect only when using `manual` proxy mode and has precedence over the `--override-proxy-pac` flag.

###### Example of specifying PAC file

```console
$ sudo /Applications/Docker.app/Contents/MacOS/install --user testuser --proxy-http-mode="manual" --override-proxy-pac="http://localhost:8080/myproxy.pac"
```

###### Example of specifying PAC script

```console
$ sudo /Applications/Docker.app/Contents/MacOS/install --user testuser --proxy-http-mode="manual" --override-proxy-embedded-pac="function FindProxyForURL(url, host) { return \"DIRECT\"; }"
```

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

## Where to go next

- Explore [Docker's subscriptions](https://www.docker.com/pricing/) to see what Docker can offer you.
- [Get started with Docker](https://docs.docker.com/get-started/introduction/).
- [Explore Docker Desktop](https://docs.docker.com/desktop/use-desktop/) and all its features.
- [Troubleshooting](https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/) describes common problems, workarounds, how
  to run and submit diagnostics, and submit issues.
- [FAQs](https://docs.docker.com/desktop/troubleshoot-and-support/faqs/general/) provide answers to frequently asked questions.
- [Release notes](https://docs.docker.com/desktop/release-notes/) lists component updates, new features, and improvements associated with Docker Desktop releases.
- [Back up and restore data](https://docs.docker.com/desktop/settings-and-maintenance/backup-and-restore/) provides instructions
  on backing up and restoring data related to Docker.
