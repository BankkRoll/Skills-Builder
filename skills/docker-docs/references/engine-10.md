# Install Docker Engine on Debian and more

# Install Docker Engine on Debian

> Learn how to install Docker Engine on Debian. These instructions cover the different installation methods, how to uninstall, and next steps.

# Install Docker Engine on Debian

   Table of contents

---

To get started with Docker Engine on Debian, make sure you
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

To install Docker Engine, you need one of these Debian versions:

- Debian Trixie 13 (stable)
- Debian Bookworm 12 (oldstable)
- Debian Bullseye 11 (oldoldstable)

Docker Engine for Debian is compatible with x86_64 (or amd64), armhf (arm/v7),
arm64, and ppc64le (ppc64el) architectures.

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
$ sudo apt remove $(dpkg --get-selections docker.io docker-compose docker-doc podman-docker containerd runc | cut -f1)
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
  sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
  sudo chmod a+r /etc/apt/keyrings/docker.asc
  # Add the repository to Apt sources:
  sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
  Types: deb
  URIs: https://download.docker.com/linux/debian
  Suites: $(. /etc/os-release && echo "$VERSION_CODENAME")
  Components: stable
  Signed-By: /etc/apt/keyrings/docker.asc
  EOF
  sudo apt update
  ```
  > Note
  >
  > If you use a derivative distribution, such as Kali Linux,
  > you may need to substitute the part of this command that's expected to
  > print the version codename:
  >
  >
  >
  > ```console
  > $(. /etc/os-release && echo "$VERSION_CODENAME")
  > ```
  >
  >
  >
  > Replace this part with the codename of the corresponding Debian release,
  > such as `bookworm`.
2. Install the Docker packages.
  To install the latest version, run:
  ```console
  $ sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
  ```
  To install a specific version of Docker Engine, start by listing the
  available versions in the repository:
  ```console
  $ apt list --all-versions docker-ce
  docker-ce/bookworm 5:29.2.0-1~debian.12~bookworm <arch>
  docker-ce/bookworm 5:29.1.5-1~debian.12~bookworm <arch>
  ...
  ```
  Select the desired version and install:
  ```console
  $ VERSION_STRING=5:29.2.0-1~debian.12~bookworm
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

1. Go to [https://download.docker.com/linux/debian/dists/](https://download.docker.com/linux/debian/dists/).
2. Select your Debian version in the list.
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

---

# Install Docker Engine on Fedora

> Learn how to install Docker Engine on Fedora. These instructions cover the different installation methods, how to uninstall, and next steps.

# Install Docker Engine on Fedora

   Table of contents

---

To get started with Docker Engine on Fedora, make sure you
[meet the prerequisites](#prerequisites), and then follow the
[installation steps](#installation-methods).

## Prerequisites

### OS requirements

To install Docker Engine, you need a maintained version of one of the following
Fedora versions:

- Fedora 43
- Fedora 42
- Fedora 41

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
                  docker-selinux \
                  docker-engine-selinux \
                  docker-engine
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

```console
$ sudo dnf config-manager addrepo --from-repofile https://download.docker.com/linux/fedora/docker-ce.repo
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
  docker-ce.x86_64    3:29.2.0-1.fc41    docker-ce-stable
  docker-ce.x86_64    3:29.1.5-1.fc41    docker-ce-stable
  <...>
  ```
  The list returned depends on which repositories are enabled, and is specific
  to your version of Fedora (indicated by the `.fc40` suffix in this example).
  Install a specific version by its fully qualified package name, which is
  the package name (`docker-ce`) plus the version string (2nd column),
  separated by a hyphen (`-`). For example, `docker-ce-3:29.2.0-1.fc41`.
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

1. Go to [https://download.docker.com/linux/fedora/](https://download.docker.com/linux/fedora/)
  and choose your version of Fedora. Then browse to `x86_64/stable/Packages/`
  and download the `.rpm` file for the Docker version you want to install.
2. Install Docker Engine, changing the following path to the path where you downloaded
  the Docker package.
  ```console
  $ sudo dnf install /path/to/package.rpm
  ```
  Docker is installed but not started. The `docker` group is created, but no
  users are added to the group.
3. Start Docker Engine.
  ```console
  $ sudo systemctl enable --now docker
  ```
  This configures the Docker systemd service to start automatically when you
  boot your system. If you don't want Docker to start automatically, use `sudo systemctl start docker` instead.
4. Verify that the installation is successful by running the `hello-world` image:
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

# Linux post

> Find the recommended Docker Engine post-installation steps for Linux users, including how to run Docker as a non-root user and more.

# Linux post-installation steps for Docker Engine

   Table of contents

---

These optional post-installation procedures describe how to configure your
Linux host machine to work better with Docker.

## Manage Docker as a non-root user

The Docker daemon binds to a Unix socket, not a TCP port. By default it's the
`root` user that owns the Unix socket, and other users can only access it using
`sudo`. The Docker daemon always runs as the `root` user.

If you don't want to preface the `docker` command with `sudo`, create a Unix
group called `docker` and add users to it. When the Docker daemon starts, it
creates a Unix socket accessible by members of the `docker` group. On some Linux
distributions, the system automatically creates this group when installing
Docker Engine using a package manager. In that case, there is no need for you to
manually create the group.

> Warning
>
> The `docker` group grants root-level privileges to the user. For
> details on how this impacts security in your system, see
> [Docker Daemon Attack Surface](https://docs.docker.com/engine/security/#docker-daemon-attack-surface).

> Note
>
> To run Docker without root privileges, see
> [Run the Docker daemon as a non-root user (Rootless mode)](https://docs.docker.com/engine/security/rootless/).

To create the `docker` group and add your user:

1. Create the `docker` group.
  ```console
  $ sudo groupadd docker
  ```
2. Add your user to the `docker` group.
  ```console
  $ sudo usermod -aG docker $USER
  ```
3. Log out and log back in so that your group membership is re-evaluated.
  > If you're running Linux in a virtual machine, it may be necessary to
  > restart the virtual machine for changes to take effect.
  You can also run the following command to activate the changes to groups:
  ```console
  $ newgrp docker
  ```
4. Verify that you can run `docker` commands without `sudo`.
  ```console
  $ docker run hello-world
  ```
  This command downloads a test image and runs it in a container. When the
  container runs, it prints a message and exits.
  If you initially ran Docker CLI commands using `sudo` before adding your user
  to the `docker` group, you may see the following error:
  ```text
  WARNING: Error loading config file: /home/user/.docker/config.json -
  stat /home/user/.docker/config.json: permission denied
  ```
  This error indicates that the permission settings for the `~/.docker/`
  directory are incorrect, due to having used the `sudo` command earlier.
  To fix this problem, either remove the `~/.docker/` directory (it's recreated
  automatically, but any custom settings are lost), or change its ownership and
  permissions using the following commands:
  ```console
  $ sudo chown "$USER":"$USER" /home/"$USER"/.docker -R
  $ sudo chmod g+rwx "$HOME/.docker" -R
  ```

## Configure Docker to start on boot with systemd

Many modern Linux distributions use [systemd](https://systemd.io/) to
manage which services start when the system boots. On Debian and Ubuntu, the
Docker service starts on boot by default. To automatically start Docker and
containerd on boot for other Linux distributions using systemd, run the
following commands:

```console
$ sudo systemctl enable docker.service
$ sudo systemctl enable containerd.service
```

To stop this behavior, use `disable` instead.

```console
$ sudo systemctl disable docker.service
$ sudo systemctl disable containerd.service
```

You can use systemd unit files to configure the Docker service on startup,
for example to add an HTTP proxy, set a different directory or partition for the
Docker runtime files, or other customizations. For an example, see
[Configure the daemon to use a proxy](https://docs.docker.com/engine/daemon/proxy/#systemd-unit-file).

## Configure default logging driver

Docker provides
[logging drivers](https://docs.docker.com/engine/logging/) for
collecting and viewing log data from all containers running on a host. The
default logging driver, `json-file`, writes log data to JSON-formatted files on
the host filesystem. Over time, these log files expand in size, leading to
potential exhaustion of disk resources.

To avoid issues with overusing disk for log data, consider one of the following
options:

- Configure the `json-file` logging driver to turn on
  [log rotation](https://docs.docker.com/engine/logging/drivers/json-file/).
- Use an
  [alternative logging driver](https://docs.docker.com/engine/logging/configure/#configure-the-default-logging-driver)
  such as the
  ["local" logging driver](https://docs.docker.com/engine/logging/drivers/local/)
  that performs log rotation by default.
- Use a logging driver that sends logs to a remote logging aggregator.

## Next steps

- Take a look at the
  [Docker workshop](https://docs.docker.com/get-started/workshop/) to learn how to build an image and run it as a containerized application.
