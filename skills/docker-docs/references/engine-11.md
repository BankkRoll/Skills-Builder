# Install Docker Engine on Raspberry Pi OS (32 and more

# Install Docker Engine on Raspberry Pi OS (32

> Learn how to install Docker Engine on a 32-bit Raspberry Pi OS system. These instructions cover the different installation methods, how to uninstall, and next steps. Note that 32-bit support will be deprecated in Docker Engine v29 and later.

# Install Docker Engine on Raspberry Pi OS (32-bit / armhf)

   Table of contents

---

> Warning
>
> **Raspberry Pi OS 32-bit (armhf) Deprecation**
>
>
>
> Docker Engine v28 will be the last major version to support Raspberry Pi OS 32-bit (armhf).
> Starting with Docker Engine v29, new major versions will no longer provide packages for Raspberry Pi OS 32-bit (armhf).
>
>
>
> **Migration options**
>
>
>
> - **64-bit ARM:** Install the Debian `arm64` packages (fully supported). See the
>   [Debian installation instructions](https://docs.docker.com/engine/install/debian/).
> - **32-bit ARM (v7):** Install the Debian `armhf` packages (targets ARMv7 CPUs).
>
>
>
> **Note:** Older devices based on the ARMv6 architecture are no longer supported by official packages, including:
>
>
>
> - Raspberry Pi 1 (Model A/B/A+/B+)
> - Raspberry Pi Zero and Zero W

To get started with Docker Engine on Raspberry Pi OS, make sure you
[meet the prerequisites](#prerequisites), and then follow the
[installation steps](#installation-methods).

> Important
>
> This installation instruction refers to the 32-bit (armhf) version of
> Raspberry Pi OS. If you're using the 64-bit (arm64) version, follow the
> instructions for [Debian](https://docs.docker.com/engine/install/debian/).

## Prerequisites

### Firewall limitations

> Warning
>
> Before you install Docker, make sure you consider the following
> security implications and firewall incompatibilities.

- If you use ufw or firewalld to manage firewall settings, be aware that
  when you expose container ports using Docker, these ports bypass your
  firewall rules. For more information, refer to
  [Docker and ufw](https://docs.docker.com/engine/network/packet-filtering-firewalls/#docker-and-ufw).
- Docker is only compatible with `iptables-nft` and `iptables-legacy`.
  Firewall rules created with `nft` are not supported on a system with Docker installed.
  Make sure that any firewall rulesets you use are created with `iptables` or `ip6tables`,
  and that you add them to the `DOCKER-USER` chain,
  see
  [Packet filtering and firewalls](https://docs.docker.com/engine/network/packet-filtering-firewalls/).

### OS requirements

To install Docker Engine, you need one of the following OS versions:

- 32-bit Raspberry Pi OS Bookworm 12 (stable)
- 32-bit Raspberry Pi OS Bullseye 11 (oldstable)

> Warning
>
> Docker Engine v28 is the last major version to support Raspberry Pi OS 32-bit (armhf). Starting with v29,
> no new packages will be provided for 32-bit Raspberry Pi OS.
>
>
>
> Migration options:
>
>
>
> - 64-bit ARM: use Debian `arm64` packages; see the [Debian installation instructions](https://docs.docker.com/engine/install/debian/).
> - 32-bit ARM (v7): use Debian `armhf` packages (targets ARMv7 CPUs).
>
>
>
> Note: ARMv6-based devices (Raspberry Pi 1 models and Raspberry Pi Zero/Zero W) are not supported by
> official packages.

### Uninstall old versions

Before you can install Docker Engine, you need to uninstall any conflicting packages.

Your Linux distribution may provide unofficial Docker packages, which may conflict
with the official packages provided by Docker. You must uninstall these packages
before you install the official version of Docker Engine.

The unofficial packages to uninstall are:

- `docker.io`
- `docker-compose`
- `docker-doc`
- `podman-docker`

Moreover, Docker Engine depends on `containerd` and `runc`. Docker Engine
bundles these dependencies as one bundle: `containerd.io`. If you have
installed the `containerd` or `runc` previously, uninstall them to avoid
conflicts with the versions bundled with Docker Engine.

Run the following command to uninstall all conflicting packages:

```console
$ for pkg in docker.io docker-doc docker-compose podman-docker containerd runc; do sudo apt-get remove $pkg; done
```

`apt-get` might report that you have none of these packages installed.

Images, containers, volumes, and networks stored in `/var/lib/docker/` aren't
automatically removed when you uninstall Docker. If you want to start with a
clean installation, and prefer to clean up any existing data, read the
[uninstall Docker Engine](#uninstall-docker-engine) section.

## Installation methods

You can install Docker Engine in different ways, depending on your needs:

- Docker Engine comes bundled with
  [Docker Desktop for Linux](https://docs.docker.com/desktop/setup/install/linux/). This is
  the easiest and quickest way to get started.
- Set up and install Docker Engine from
  [Docker'saptrepository](#install-using-the-repository).
- [Install it manually](#install-from-a-package) and manage upgrades manually.
- Use a [convenience script](#install-using-the-convenience-script). Only
  recommended for testing and development environments.

Apache License, Version 2.0. See [LICENSE](https://github.com/moby/moby/blob/master/LICENSE) for the full license.

### Install using theaptrepository

Before you install Docker Engine for the first time on a new host machine, you
need to set up the Docker `apt` repository. Afterward, you can install and update
Docker from the repository.

1. Set up Docker's `apt` repository.
  ```bash
  # Add Docker's official GPG key:
  sudo apt-get update
  sudo apt-get install ca-certificates curl
  sudo install -m 0755 -d /etc/apt/keyrings
  sudo curl -fsSL https://download.docker.com/linux/raspbian/gpg -o /etc/apt/keyrings/docker.asc
  sudo chmod a+r /etc/apt/keyrings/docker.asc
  # Add the repository to Apt sources:
  echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/raspbian \
    $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  sudo apt-get update
  ```
2. Install the Docker packages.
  To install the latest version, run:
  ```console
  $ sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
  ```
  To install a specific version of Docker Engine, start by listing the
  available versions in the repository:
  ```console
  # List the available versions:
  $ apt-cache madison docker-ce | awk '{ print $3 }'
  5:29.2.0-1~raspbian.12~bookworm
  5:29.1.5-1~raspbian.12~bookworm
  ...
  ```
  Select the desired version and install:
  ```console
  $ VERSION_STRING=5:29.2.0-1~raspbian.12~bookworm
  $ sudo apt-get install docker-ce=$VERSION_STRING docker-ce-cli=$VERSION_STRING containerd.io docker-buildx-plugin docker-compose-plugin
  ```
  > Note
  >
  > The Docker service starts automatically after installation. To verify that
  > Docker is running, use:
  >
  >
  >
  > ```console
  > $ sudo systemctl status docker
  > ```
  >
  >
  >
  > Some systems may have this behavior disabled and will require a manual start:
  >
  >
  >
  > ```console
  > $ sudo systemctl start docker
  > ```
3. Verify that the installation is successful by running the `hello-world` image:
  ```console
  $ sudo docker run hello-world
  ```
  This command downloads a test image and runs it in a container. When the
  container runs, it prints a confirmation message and exits.

You have now successfully installed and started Docker Engine.

> Tip
>
> Receiving errors when trying to run without root?
>
>
>
> The `docker` user group exists but contains no users, which is why you’re required
> to use `sudo` to run Docker commands. Continue to
> [Linux postinstall](https://docs.docker.com/engine/install/linux-postinstall)
> to allow non-privileged users to run Docker commands and for other optional configuration steps.

#### Upgrade Docker Engine

To upgrade Docker Engine, follow step 2 of the
[installation instructions](#install-using-the-repository),
choosing the new version you want to install.

### Install from a package

If you can't use Docker's `apt` repository to install Docker Engine, you can
download the `deb` file for your release and install it manually. You need to
download a new file each time you want to upgrade Docker Engine.

1. Go to [https://download.docker.com/linux/raspbian/dists/](https://download.docker.com/linux/raspbian/dists/).
2. Select your Raspberry Pi OS version in the list.
3. Go to `pool/stable/` and select the applicable architecture (`amd64`,
  `armhf`, `arm64`, or `s390x`).
4. Download the following `deb` files for the Docker Engine, CLI, containerd,
  and Docker Compose packages:
  - `containerd.io_<version>_<arch>.deb`
  - `docker-ce_<version>_<arch>.deb`
  - `docker-ce-cli_<version>_<arch>.deb`
  - `docker-buildx-plugin_<version>_<arch>.deb`
  - `docker-compose-plugin_<version>_<arch>.deb`
5. Install the `.deb` packages. Update the paths in the following example to
  where you downloaded the Docker packages.
  ```console
  $ sudo dpkg -i ./containerd.io_<version>_<arch>.deb \
    ./docker-ce_<version>_<arch>.deb \
    ./docker-ce-cli_<version>_<arch>.deb \
    ./docker-buildx-plugin_<version>_<arch>.deb \
    ./docker-compose-plugin_<version>_<arch>.deb
  ```
  > Note
  >
  > The Docker service starts automatically after installation. To verify that
  > Docker is running, use:
  >
  >
  >
  > ```console
  > $ sudo systemctl status docker
  > ```
  >
  >
  >
  > Some systems may have this behavior disabled and will require a manual start:
  >
  >
  >
  > ```console
  > $ sudo systemctl start docker
  > ```
6. Verify that the installation is successful by running the `hello-world` image:
  ```console
  $ sudo docker run hello-world
  ```
  This command downloads a test image and runs it in a container. When the
  container runs, it prints a confirmation message and exits.

You have now successfully installed and started Docker Engine.

> Tip
>
> Receiving errors when trying to run without root?
>
>
>
> The `docker` user group exists but contains no users, which is why you’re required
> to use `sudo` to run Docker commands. Continue to
> [Linux postinstall](https://docs.docker.com/engine/install/linux-postinstall)
> to allow non-privileged users to run Docker commands and for other optional configuration steps.

#### Upgrade Docker Engine

To upgrade Docker Engine, download the newer package files and repeat the
[installation procedure](#install-from-a-package), pointing to the new files.

### Install using the convenience script

Docker provides a convenience script at
[https://get.docker.com/](https://get.docker.com/) to install Docker into
development environments non-interactively. The convenience script isn't
recommended for production environments, but it's useful for creating a
provisioning script tailored to your needs. Also refer to the
[install using the repository](#install-using-the-repository) steps to learn
about installation steps to install using the package repository. The source code
for the script is open source, and you can find it in the
[docker-installrepository on GitHub](https://github.com/docker/docker-install).

Always examine scripts downloaded from the internet before running them locally.
Before installing, make yourself familiar with potential risks and limitations
of the convenience script:

- The script requires `root` or `sudo` privileges to run.
- The script attempts to detect your Linux distribution and version and
  configure your package management system for you.
- The script doesn't allow you to customize most installation parameters.
- The script installs dependencies and recommendations without asking for
  confirmation. This may install a large number of packages, depending on the
  current configuration of your host machine.
- By default, the script installs the latest stable release of Docker,
  containerd, and runc. When using this script to provision a machine, this may
  result in unexpected major version upgrades of Docker. Always test upgrades in
  a test environment before deploying to your production systems.
- The script isn't designed to upgrade an existing Docker installation. When
  using the script to update an existing installation, dependencies may not be
  updated to the expected version, resulting in outdated versions.

> Tip
>
> Preview script steps before running. You can run the script with the `--dry-run` option to learn what steps the
> script will run when invoked:
>
>
>
> ```console
> $ curl -fsSL https://get.docker.com -o get-docker.sh
> $ sudo sh ./get-docker.sh --dry-run
> ```

This example downloads the script from
[https://get.docker.com/](https://get.docker.com/) and runs it to install the
latest stable release of Docker on Linux:

```console
$ curl -fsSL https://get.docker.com -o get-docker.sh
$ sudo sh get-docker.sh
Executing docker install script, commit: 7cae5f8b0decc17d6571f9f52eb840fbc13b2737
<...>
```

You have now successfully installed and started Docker Engine. The `docker`
service starts automatically on Debian based distributions. On `RPM` based
distributions, such as CentOS, Fedora or RHEL, you need to start it
manually using the appropriate `systemctl` or `service` command. As the message
indicates, non-root users can't run Docker commands by default.

> **Use Docker as a non-privileged user, or install in rootless mode?**
>
>
>
> The installation script requires `root` or `sudo` privileges to install and
> use Docker. If you want to grant non-root users access to Docker, refer to the
> [post-installation steps for Linux](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user).
> You can also install Docker without `root` privileges, or configured to run in
> rootless mode. For instructions on running Docker in rootless mode, refer to
> [run the Docker daemon as a non-root user (rootless mode)](https://docs.docker.com/engine/security/rootless/).

#### Install pre-releases

Docker also provides a convenience script at
[https://test.docker.com/](https://test.docker.com/) to install pre-releases of
Docker on Linux. This script is equal to the script at `get.docker.com`, but
configures your package manager to use the test channel of the Docker package
repository. The test channel includes both stable and pre-releases (beta
versions, release-candidates) of Docker. Use this script to get early access to
new releases, and to evaluate them in a testing environment before they're
released as stable.

To install the latest version of Docker on Linux from the test channel, run:

```console
$ curl -fsSL https://test.docker.com -o test-docker.sh
$ sudo sh test-docker.sh
```

#### Upgrade Docker after using the convenience script

If you installed Docker using the convenience script, you should upgrade Docker
using your package manager directly. There's no advantage to re-running the
convenience script. Re-running it can cause issues if it attempts to re-install
repositories which already exist on the host machine.

## Uninstall Docker Engine

1. Uninstall the Docker Engine, CLI, containerd, and Docker Compose packages:
  ```console
  $ sudo apt-get purge docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras
  ```
2. Images, containers, volumes, or custom configuration files on your host
  aren't automatically removed. To delete all images, containers, and volumes:
  ```console
  $ sudo rm -rf /var/lib/docker
  $ sudo rm -rf /var/lib/containerd
  ```
3. Remove source list and keyrings
  ```console
  $ sudo rm /etc/apt/sources.list.d/docker.list
  $ sudo rm /etc/apt/keyrings/docker.asc
  ```

You have to delete any edited configuration files manually.

## Next steps

- Continue to [Post-installation steps for Linux](https://docs.docker.com/engine/install/linux-postinstall/).

---

# Install Docker Engine on RHEL

> Learn how to install Docker Engine on RHEL. These instructions cover the different installation methods, how to uninstall, and next steps.

# Install Docker Engine on RHEL

   Table of contents

---

To get started with Docker Engine on RHEL, make sure you
[meet the prerequisites](#prerequisites), and then follow the
[installation steps](#installation-methods).

## Prerequisites

### OS requirements

To install Docker Engine, you need a maintained version of one of the following
RHEL versions:

- RHEL 8
- RHEL 9
- RHEL 10

### Uninstall old versions

Before you can install Docker Engine, you need to uninstall any conflicting packages.

Your Linux distribution may provide unofficial Docker packages, which may conflict
with the official packages provided by Docker. You must uninstall these packages
before you install the official version of Docker Engine.

```console
$ sudo dnf remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-engine \
                  podman \
                  runc
```

`dnf` might report that you have none of these packages installed.

Images, containers, volumes, and networks stored in `/var/lib/docker/` aren't
automatically removed when you uninstall Docker.

## Installation methods

You can install Docker Engine in different ways, depending on your needs:

- You can
  [set up Docker's repositories](#install-using-the-repository) and install
  from them, for ease of installation and upgrade tasks. This is the
  recommended approach.
- You can download the RPM package,
  [install it manually](#install-from-a-package), and manage
  upgrades completely manually. This is useful in situations such as installing
  Docker on air-gapped systems with no access to the internet.
- In testing and development environments, you can use automated
  [convenience scripts](#install-using-the-convenience-script) to install Docker.

Apache License, Version 2.0. See [LICENSE](https://github.com/moby/moby/blob/master/LICENSE) for the full license.

### Install using the rpm repository

Before you install Docker Engine for the first time on a new host machine, you
need to set up the Docker repository. Afterward, you can install and update
Docker from the repository.

#### Set up the repository

Install the `dnf-plugins-core` package (which provides the commands to manage
your DNF repositories) and set up the repository.

```console
$ sudo dnf -y install dnf-plugins-core
$ sudo dnf config-manager --add-repo https://download.docker.com/linux/rhel/docker-ce.repo
```

#### Install Docker Engine

1. Install the Docker packages.
  To install the latest version, run:
  ```console
  $ sudo dnf install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
  ```
  If prompted to accept the GPG key, verify that the fingerprint matches
  `060A 61C5 1B55 8A7F 742B 77AA C52F EB6B 621E 9F35`, and if so, accept it.
  This command installs Docker, but it doesn't start Docker. It also creates a
  `docker` group, however, it doesn't add any users to the group by default.
  To install a specific version, start by listing the available versions in
  the repository:
  ```console
  $ dnf list docker-ce --showduplicates | sort -r
  docker-ce.x86_64    3:29.2.0-1.el9    docker-ce-stable
  docker-ce.x86_64    3:29.1.5-1.el9    docker-ce-stable
  <...>
  ```
  The list returned depends on which repositories are enabled, and is specific
  to your version of RHEL (indicated by the `.el9` suffix in this example).
  Install a specific version by its fully qualified package name, which is
  the package name (`docker-ce`) plus the version string (2nd column),
  separated by a hyphen (`-`). For example, `docker-ce-3:29.2.0-1.el9`.
  Replace `<VERSION_STRING>` with the desired version and then run the following
  command to install:
  ```console
  $ sudo dnf install docker-ce-VERSION_STRING docker-ce-cli-VERSION_STRING containerd.io docker-buildx-plugin docker-compose-plugin
  ```
  This command installs Docker, but it doesn't start Docker. It also creates a
  `docker` group, however, it doesn't add any users to the group by default.
2. Start Docker Engine.
  ```console
  $ sudo systemctl enable --now docker
  ```
  This configures the Docker systemd service to start automatically when you
  boot your system. If you don't want Docker to start automatically, use `sudo systemctl start docker` instead.
3. Verify that the installation is successful by running the `hello-world` image:
  ```console
  $ sudo docker run hello-world
  ```
  This command downloads a test image and runs it in a container. When the
  container runs, it prints a confirmation message and exits.

You have now successfully installed and started Docker Engine.

> Tip
>
> Receiving errors when trying to run without root?
>
>
>
> The `docker` user group exists but contains no users, which is why you’re required
> to use `sudo` to run Docker commands. Continue to
> [Linux postinstall](https://docs.docker.com/engine/install/linux-postinstall)
> to allow non-privileged users to run Docker commands and for other optional configuration steps.

#### Upgrade Docker Engine

To upgrade Docker Engine, follow the [installation instructions](#install-using-the-repository),
choosing the new version you want to install.

### Install from a package

If you can't use Docker's `rpm` repository to install Docker Engine, you can
download the `.rpm` file for your release and install it manually. You need to
download a new file each time you want to upgrade Docker Engine.

1. Go to [https://download.docker.com/linux/rhel/](https://download.docker.com/linux/rhel/).
2. Select your RHEL version in the list.
3. Select the applicable architecture (`x86_64`, `aarch64`, or `s390x`), and
  then go to `stable/Packages/`.
4. Download the following `rpm` files for the Docker Engine, CLI, containerd,
  and Docker Compose packages:
  - `containerd.io-<version>.<arch>.rpm`
  - `docker-ce-<version>.<arch>.rpm`
  - `docker-ce-cli-<version>.<arch>.rpm`
  - `docker-buildx-plugin-<version>.<arch>.rpm`
  - `docker-compose-plugin-<version>.<arch>.rpm`
5. Install Docker Engine, changing the following path to the path where you downloaded
  the packages.
  ```console
  $ sudo dnf install ./containerd.io-<version>.<arch>.rpm \
    ./docker-ce-<version>.<arch>.rpm \
    ./docker-ce-cli-<version>.<arch>.rpm \
    ./docker-buildx-plugin-<version>.<arch>.rpm \
    ./docker-compose-plugin-<version>.<arch>.rpm
  ```
  Docker is installed but not started. The `docker` group is created, but no
  users are added to the group.
6. Start Docker Engine.
  ```console
  $ sudo systemctl enable --now docker
  ```
  This configures the Docker systemd service to start automatically when you
  boot your system. If you don't want Docker to start automatically, use `sudo systemctl start docker` instead.
7. Verify that the installation is successful by running the `hello-world` image:
  ```console
  $ sudo docker run hello-world
  ```
  This command downloads a test image and runs it in a container. When the
  container runs, it prints a confirmation message and exits.

You have now successfully installed and started Docker Engine.

> Tip
>
> Receiving errors when trying to run without root?
>
>
>
> The `docker` user group exists but contains no users, which is why you’re required
> to use `sudo` to run Docker commands. Continue to
> [Linux postinstall](https://docs.docker.com/engine/install/linux-postinstall)
> to allow non-privileged users to run Docker commands and for other optional configuration steps.

#### Upgrade Docker Engine

To upgrade Docker Engine, download the newer package files and repeat the
[installation procedure](#install-from-a-package), using `dnf upgrade`
instead of `dnf install`, and point to the new files.

### Install using the convenience script

Docker provides a convenience script at
[https://get.docker.com/](https://get.docker.com/) to install Docker into
development environments non-interactively. The convenience script isn't
recommended for production environments, but it's useful for creating a
provisioning script tailored to your needs. Also refer to the
[install using the repository](#install-using-the-repository) steps to learn
about installation steps to install using the package repository. The source code
for the script is open source, and you can find it in the
[docker-installrepository on GitHub](https://github.com/docker/docker-install).

Always examine scripts downloaded from the internet before running them locally.
Before installing, make yourself familiar with potential risks and limitations
of the convenience script:

- The script requires `root` or `sudo` privileges to run.
- The script attempts to detect your Linux distribution and version and
  configure your package management system for you.
- The script doesn't allow you to customize most installation parameters.
- The script installs dependencies and recommendations without asking for
  confirmation. This may install a large number of packages, depending on the
  current configuration of your host machine.
- By default, the script installs the latest stable release of Docker,
  containerd, and runc. When using this script to provision a machine, this may
  result in unexpected major version upgrades of Docker. Always test upgrades in
  a test environment before deploying to your production systems.
- The script isn't designed to upgrade an existing Docker installation. When
  using the script to update an existing installation, dependencies may not be
  updated to the expected version, resulting in outdated versions.

> Tip
>
> Preview script steps before running. You can run the script with the `--dry-run` option to learn what steps the
> script will run when invoked:
>
>
>
> ```console
> $ curl -fsSL https://get.docker.com -o get-docker.sh
> $ sudo sh ./get-docker.sh --dry-run
> ```

This example downloads the script from
[https://get.docker.com/](https://get.docker.com/) and runs it to install the
latest stable release of Docker on Linux:

```console
$ curl -fsSL https://get.docker.com -o get-docker.sh
$ sudo sh get-docker.sh
Executing docker install script, commit: 7cae5f8b0decc17d6571f9f52eb840fbc13b2737
<...>
```

You have now successfully installed and started Docker Engine. The `docker`
service starts automatically on Debian based distributions. On `RPM` based
distributions, such as CentOS, Fedora or RHEL, you need to start it
manually using the appropriate `systemctl` or `service` command. As the message
indicates, non-root users can't run Docker commands by default.

> **Use Docker as a non-privileged user, or install in rootless mode?**
>
>
>
> The installation script requires `root` or `sudo` privileges to install and
> use Docker. If you want to grant non-root users access to Docker, refer to the
> [post-installation steps for Linux](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user).
> You can also install Docker without `root` privileges, or configured to run in
> rootless mode. For instructions on running Docker in rootless mode, refer to
> [run the Docker daemon as a non-root user (rootless mode)](https://docs.docker.com/engine/security/rootless/).

#### Install pre-releases

Docker also provides a convenience script at
[https://test.docker.com/](https://test.docker.com/) to install pre-releases of
Docker on Linux. This script is equal to the script at `get.docker.com`, but
configures your package manager to use the test channel of the Docker package
repository. The test channel includes both stable and pre-releases (beta
versions, release-candidates) of Docker. Use this script to get early access to
new releases, and to evaluate them in a testing environment before they're
released as stable.

To install the latest version of Docker on Linux from the test channel, run:

```console
$ curl -fsSL https://test.docker.com -o test-docker.sh
$ sudo sh test-docker.sh
```

#### Upgrade Docker after using the convenience script

If you installed Docker using the convenience script, you should upgrade Docker
using your package manager directly. There's no advantage to re-running the
convenience script. Re-running it can cause issues if it attempts to re-install
repositories which already exist on the host machine.

## Uninstall Docker Engine

1. Uninstall the Docker Engine, CLI, containerd, and Docker Compose packages:
  ```console
  $ sudo dnf remove docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras
  ```
2. Images, containers, volumes, or custom configuration files on your host
  aren't automatically removed. To delete all images, containers, and volumes:
  ```console
  $ sudo rm -rf /var/lib/docker
  $ sudo rm -rf /var/lib/containerd
  ```

You have to delete any edited configuration files manually.

## Next steps

- Continue to [Post-installation steps for Linux](https://docs.docker.com/engine/install/linux-postinstall/).

---

# Docker Engine on SLES (s390x)

> Information about Docker Engine availability on SLES. Docker packages are no longer available for SLES s390x architecture.

# Docker Engine on SLES (s390x)

   Table of contents

---

## Docker Engine is no longer available for SLES

> Important
>
> Docker Engine packages are **no longer available** for SUSE Linux Enterprise Server (SLES) on the **s390x** architecture (IBM Z).

IBM has made the decision to discontinue building and providing Docker Engine
packages for SLES s390x systems. Docker Inc. never directly built these packages
and was only involved in their deployment.

## What this means

- New Docker Engine installations are not available for SLES s390x
- Existing installations will continue to work but will not receive updates
- No new versions or security updates will be provided
- The Docker package repository for SLES s390x is no longer maintained

## If you have Docker currently installed

If you currently have Docker Engine installed on a SLES s390x system:

- Your existing Docker installation will continue to function
- No automatic updates will be available
- You should plan accordingly for your containerization needs
- Consider the security implications of running software without updates

## Next steps

For questions about this decision or alternative solutions, contact IBM support.

---

# Install Docker Engine on Ubuntu

> Jumpstart your client-side server applications with Docker Engine on Ubuntu. This guide details prerequisites and multiple methods to install Docker Engine on Ubuntu.

# Install Docker Engine on Ubuntu

   Table of contents

---

To get started with Docker Engine on Ubuntu, make sure you
[meet the prerequisites](#prerequisites), and then follow the
[installation steps](#installation-methods).

## Prerequisites

### Firewall limitations

> Warning
>
> Before you install Docker, make sure you consider the following
> security implications and firewall incompatibilities.

- If you use ufw or firewalld to manage firewall settings, be aware that
  when you expose container ports using Docker, these ports bypass your
  firewall rules. For more information, refer to
  [Docker and ufw](https://docs.docker.com/engine/network/packet-filtering-firewalls/#docker-and-ufw).
- Docker is only compatible with `iptables-nft` and `iptables-legacy`.
  Firewall rules created with `nft` are not supported on a system with Docker installed.
  Make sure that any firewall rulesets you use are created with `iptables` or `ip6tables`,
  and that you add them to the `DOCKER-USER` chain,
  see
  [Packet filtering and firewalls](https://docs.docker.com/engine/network/packet-filtering-firewalls/).

### OS requirements

To install Docker Engine, you need the 64-bit version of one of these Ubuntu
versions:

- Ubuntu Questing 25.10
- Ubuntu Plucky 25.04
- Ubuntu Noble 24.04 (LTS)
- Ubuntu Jammy 22.04 (LTS)

Docker Engine for Ubuntu is compatible with x86_64 (or amd64), armhf, arm64,
s390x, and ppc64le (ppc64el) architectures.

> Note
>
> Installation on Ubuntu derivative distributions, such as Linux Mint, is not officially
> supported (though it may work).

### Uninstall old versions

Before you can install Docker Engine, you need to uninstall any conflicting packages.

Your Linux distribution may provide unofficial Docker packages, which may conflict
with the official packages provided by Docker. You must uninstall these packages
before you install the official version of Docker Engine.

The unofficial packages to uninstall are:

- `docker.io`
- `docker-compose`
- `docker-compose-v2`
- `docker-doc`
- `podman-docker`

Moreover, Docker Engine depends on `containerd` and `runc`. Docker Engine
bundles these dependencies as one bundle: `containerd.io`. If you have
installed the `containerd` or `runc` previously, uninstall them to avoid
conflicts with the versions bundled with Docker Engine.

Run the following command to uninstall all conflicting packages:

```console
$ sudo apt remove $(dpkg --get-selections docker.io docker-compose docker-compose-v2 docker-doc podman-docker containerd runc | cut -f1)
```

`apt` might report that you have none of these packages installed.

Images, containers, volumes, and networks stored in `/var/lib/docker/` aren't
automatically removed when you uninstall Docker. If you want to start with a
clean installation, and prefer to clean up any existing data, read the
[uninstall Docker Engine](#uninstall-docker-engine) section.

## Installation methods

You can install Docker Engine in different ways, depending on your needs:

- Docker Engine comes bundled with
  [Docker Desktop for Linux](https://docs.docker.com/desktop/setup/install/linux/). This is
  the easiest and quickest way to get started.
- Set up and install Docker Engine from
  [Docker'saptrepository](#install-using-the-repository).
- [Install it manually](#install-from-a-package) and manage upgrades manually.
- Use a [convenience script](#install-using-the-convenience-script). Only
  recommended for testing and development environments.

Apache License, Version 2.0. See [LICENSE](https://github.com/moby/moby/blob/master/LICENSE) for the full license.

### Install using theaptrepository

Before you install Docker Engine for the first time on a new host machine, you
need to set up the Docker `apt` repository. Afterward, you can install and update
Docker from the repository.

1. Set up Docker's `apt` repository.
  ```bash
  # Add Docker's official GPG key:
  sudo apt update
  sudo apt install ca-certificates curl
  sudo install -m 0755 -d /etc/apt/keyrings
  sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
  sudo chmod a+r /etc/apt/keyrings/docker.asc
  # Add the repository to Apt sources:
  sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
  Types: deb
  URIs: https://download.docker.com/linux/ubuntu
  Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
  Components: stable
  Signed-By: /etc/apt/keyrings/docker.asc
  EOF
  sudo apt update
  ```
2. Install the Docker packages.
  To install the latest version, run:
  ```console
  $ sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
  ```
  To install a specific version of Docker Engine, start by listing the
  available versions in the repository:
  ```console
  $ apt list --all-versions docker-ce
  docker-ce/noble 5:29.2.0-1~ubuntu.24.04~noble <arch>
  docker-ce/noble 5:29.1.5-1~ubuntu.24.04~noble <arch>
  ...
  ```
  Select the desired version and install:
  ```console
  $ VERSION_STRING=5:29.2.0-1~ubuntu.24.04~noble
  $ sudo apt install docker-ce=$VERSION_STRING docker-ce-cli=$VERSION_STRING containerd.io docker-buildx-plugin docker-compose-plugin
  ```
  > Note
  >
  > The Docker service starts automatically after installation. To verify that
  > Docker is running, use:
  >
  >
  >
  > ```console
  > $ sudo systemctl status docker
  > ```
  >
  >
  >
  > Some systems may have this behavior disabled and will require a manual start:
  >
  >
  >
  > ```console
  > $ sudo systemctl start docker
  > ```
3. Verify that the installation is successful by running the `hello-world` image:
  ```console
  $ sudo docker run hello-world
  ```
  This command downloads a test image and runs it in a container. When the
  container runs, it prints a confirmation message and exits.

You have now successfully installed and started Docker Engine.

> Tip
>
> Receiving errors when trying to run without root?
>
>
>
> The `docker` user group exists but contains no users, which is why you’re required
> to use `sudo` to run Docker commands. Continue to
> [Linux postinstall](https://docs.docker.com/engine/install/linux-postinstall)
> to allow non-privileged users to run Docker commands and for other optional configuration steps.

#### Upgrade Docker Engine

To upgrade Docker Engine, follow step 2 of the
[installation instructions](#install-using-the-repository),
choosing the new version you want to install.

### Install from a package

If you can't use Docker's `apt` repository to install Docker Engine, you can
download the `deb` file for your release and install it manually. You need to
download a new file each time you want to upgrade Docker Engine.

1. Go to [https://download.docker.com/linux/ubuntu/dists/](https://download.docker.com/linux/ubuntu/dists/).
2. Select your Ubuntu version in the list.
3. Go to `pool/stable/` and select the applicable architecture (`amd64`,
  `armhf`, `arm64`, or `s390x`).
4. Download the following `deb` files for the Docker Engine, CLI, containerd,
  and Docker Compose packages:
  - `containerd.io_<version>_<arch>.deb`
  - `docker-ce_<version>_<arch>.deb`
  - `docker-ce-cli_<version>_<arch>.deb`
  - `docker-buildx-plugin_<version>_<arch>.deb`
  - `docker-compose-plugin_<version>_<arch>.deb`
5. Install the `.deb` packages. Update the paths in the following example to
  where you downloaded the Docker packages.
  ```console
  $ sudo dpkg -i ./containerd.io_<version>_<arch>.deb \
    ./docker-ce_<version>_<arch>.deb \
    ./docker-ce-cli_<version>_<arch>.deb \
    ./docker-buildx-plugin_<version>_<arch>.deb \
    ./docker-compose-plugin_<version>_<arch>.deb
  ```
  > Note
  >
  > The Docker service starts automatically after installation. To verify that
  > Docker is running, use:
  >
  >
  >
  > ```console
  > $ sudo systemctl status docker
  > ```
  >
  >
  >
  > Some systems may have this behavior disabled and will require a manual start:
  >
  >
  >
  > ```console
  > $ sudo systemctl start docker
  > ```
6. Verify that the installation is successful by running the `hello-world` image:
  ```console
  $ sudo docker run hello-world
  ```
  This command downloads a test image and runs it in a container. When the
  container runs, it prints a confirmation message and exits.

You have now successfully installed and started Docker Engine.

> Tip
>
> Receiving errors when trying to run without root?
>
>
>
> The `docker` user group exists but contains no users, which is why you’re required
> to use `sudo` to run Docker commands. Continue to
> [Linux postinstall](https://docs.docker.com/engine/install/linux-postinstall)
> to allow non-privileged users to run Docker commands and for other optional configuration steps.

#### Upgrade Docker Engine

To upgrade Docker Engine, download the newer package files and repeat the
[installation procedure](#install-from-a-package), pointing to the new files.

### Install using the convenience script

Docker provides a convenience script at
[https://get.docker.com/](https://get.docker.com/) to install Docker into
development environments non-interactively. The convenience script isn't
recommended for production environments, but it's useful for creating a
provisioning script tailored to your needs. Also refer to the
[install using the repository](#install-using-the-repository) steps to learn
about installation steps to install using the package repository. The source code
for the script is open source, and you can find it in the
[docker-installrepository on GitHub](https://github.com/docker/docker-install).

Always examine scripts downloaded from the internet before running them locally.
Before installing, make yourself familiar with potential risks and limitations
of the convenience script:

- The script requires `root` or `sudo` privileges to run.
- The script attempts to detect your Linux distribution and version and
  configure your package management system for you.
- The script doesn't allow you to customize most installation parameters.
- The script installs dependencies and recommendations without asking for
  confirmation. This may install a large number of packages, depending on the
  current configuration of your host machine.
- By default, the script installs the latest stable release of Docker,
  containerd, and runc. When using this script to provision a machine, this may
  result in unexpected major version upgrades of Docker. Always test upgrades in
  a test environment before deploying to your production systems.
- The script isn't designed to upgrade an existing Docker installation. When
  using the script to update an existing installation, dependencies may not be
  updated to the expected version, resulting in outdated versions.

> Tip
>
> Preview script steps before running. You can run the script with the `--dry-run` option to learn what steps the
> script will run when invoked:
>
>
>
> ```console
> $ curl -fsSL https://get.docker.com -o get-docker.sh
> $ sudo sh ./get-docker.sh --dry-run
> ```

This example downloads the script from
[https://get.docker.com/](https://get.docker.com/) and runs it to install the
latest stable release of Docker on Linux:

```console
$ curl -fsSL https://get.docker.com -o get-docker.sh
$ sudo sh get-docker.sh
Executing docker install script, commit: 7cae5f8b0decc17d6571f9f52eb840fbc13b2737
<...>
```

You have now successfully installed and started Docker Engine. The `docker`
service starts automatically on Debian based distributions. On `RPM` based
distributions, such as CentOS, Fedora or RHEL, you need to start it
manually using the appropriate `systemctl` or `service` command. As the message
indicates, non-root users can't run Docker commands by default.

> **Use Docker as a non-privileged user, or install in rootless mode?**
>
>
>
> The installation script requires `root` or `sudo` privileges to install and
> use Docker. If you want to grant non-root users access to Docker, refer to the
> [post-installation steps for Linux](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user).
> You can also install Docker without `root` privileges, or configured to run in
> rootless mode. For instructions on running Docker in rootless mode, refer to
> [run the Docker daemon as a non-root user (rootless mode)](https://docs.docker.com/engine/security/rootless/).

#### Install pre-releases

Docker also provides a convenience script at
[https://test.docker.com/](https://test.docker.com/) to install pre-releases of
Docker on Linux. This script is equal to the script at `get.docker.com`, but
configures your package manager to use the test channel of the Docker package
repository. The test channel includes both stable and pre-releases (beta
versions, release-candidates) of Docker. Use this script to get early access to
new releases, and to evaluate them in a testing environment before they're
released as stable.

To install the latest version of Docker on Linux from the test channel, run:

```console
$ curl -fsSL https://test.docker.com -o test-docker.sh
$ sudo sh test-docker.sh
```

#### Upgrade Docker after using the convenience script

If you installed Docker using the convenience script, you should upgrade Docker
using your package manager directly. There's no advantage to re-running the
convenience script. Re-running it can cause issues if it attempts to re-install
repositories which already exist on the host machine.

## Uninstall Docker Engine

1. Uninstall the Docker Engine, CLI, containerd, and Docker Compose packages:
  ```console
  $ sudo apt purge docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras
  ```
2. Images, containers, volumes, or custom configuration files on your host
  aren't automatically removed. To delete all images, containers, and volumes:
  ```console
  $ sudo rm -rf /var/lib/docker
  $ sudo rm -rf /var/lib/containerd
  ```
3. Remove source list and keyrings
  ```console
  $ sudo rm /etc/apt/sources.list.d/docker.sources
  $ sudo rm /etc/apt/keyrings/docker.asc
  ```

You have to delete any edited configuration files manually.

## Next steps

- Continue to [Post-installation steps for Linux](https://docs.docker.com/engine/install/linux-postinstall/).
