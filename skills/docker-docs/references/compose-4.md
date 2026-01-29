# Using profiles with Compose and more

# Using profiles with Compose

> How to use profiles with Docker Compose

# Using profiles with Compose

   Table of contents

---

Profiles help you adjust your Compose application for different environments or use cases by selectively activating services. Services can be assigned to one or more profiles; unassigned services start/stop by default, while assigned ones only start/stop when their profile is active. This setup means specific services, like those for debugging or development, to be included in a single `compose.yml` file and activated only as needed.

## Assigning profiles to services

Services are associated with profiles through the
[profilesattribute](https://docs.docker.com/reference/compose-file/services/#profiles) which takes an
array of profile names:

```yaml
services:
  frontend:
    image: frontend
    profiles: [frontend]

  phpmyadmin:
    image: phpmyadmin
    depends_on: [db]
    profiles: [debug]

  backend:
    image: backend

  db:
    image: mysql
```

Here the services `frontend` and `phpmyadmin` are assigned to the profiles
`frontend` and `debug` respectively and as such are only started when their
respective profiles are enabled.

Services without a `profiles` attribute are always enabled. In this
case running `docker compose up` would only start `backend` and `db`.

Valid profiles names follow the regex format of `[a-zA-Z0-9][a-zA-Z0-9_.-]+`.

> Tip
>
> The core services of your application shouldn't be assigned `profiles` so
> they are always enabled and automatically started.

## Start specific profiles

To start a specific profile supply the `--profile` [command-line option](https://docs.docker.com/reference/cli/docker/compose/) or
use the [COMPOSE_PROFILESenvironment variable](https://docs.docker.com/compose/how-tos/environment-variables/envvars/#compose_profiles):

```console
$ docker compose --profile debug up
```

```console
$ COMPOSE_PROFILES=debug docker compose up
```

Both commands start the services with the `debug` profile enabled.
In the previous `compose.yaml` file, this starts the services
`db`, `backend` and `phpmyadmin`.

### Start multiple profiles

You can also enable
multiple profiles, e.g. with `docker compose --profile frontend --profile debug up`
the profiles `frontend` and `debug` will be enabled.

Multiple profiles can be specified by passing multiple `--profile` flags or
a comma-separated list for the `COMPOSE_PROFILES` environment variable:

```console
$ docker compose --profile frontend --profile debug up
```

```console
$ COMPOSE_PROFILES=frontend,debug docker compose up
```

If you want to enable all profiles at the same time, you can run `docker compose --profile "*"`.

## Auto-starting profiles and dependency resolution

When you explicitly target a service on the command line that has one or more profiles assigned, you do not need to enable the profile manually as Compose runs that service regardless of whether its profile is activated. This is useful for running one-off services or debugging tools.

Only the targeted service (and any of its declared dependencies via `depends_on`) is started. Other services that share the same profile will not be started unless:

- They are also explicitly targeted, or
- The profile is explicitly enabled using `--profile` or `COMPOSE_PROFILES`.

When a service with assigned `profiles` is explicitly targeted on the command
line its profiles are started automatically so you don't need to start them
manually. This can be used for one-off services and debugging tools.
As an example consider the following configuration:

```yaml
services:
  backend:
    image: backend

  db:
    image: mysql

  db-migrations:
    image: backend
    command: myapp migrate
    depends_on:
      - db
    profiles:
      - tools
```

```sh
# Only start backend and db (no profiles involved)
$ docker compose up -d

# Run the db-migrations service without manually enabling the 'tools' profile
$ docker compose run db-migrations
```

In this example, `db-migrations` runs even though it is assigned to the tools profile, because it was explicitly targeted. The `db` service is also started automatically because it is listed in `depends_on`.

If the targeted service has dependencies that are also gated behind a profile, you must ensure those dependencies are either:

- In the same profile
- Started separately
- Not assigned to any profile so are always enabled

## Stop application and services with specific profiles

As with starting specific profiles, you can use the `--profile` [command-line option](https://docs.docker.com/reference/cli/docker/compose/#use--p-to-specify-a-project-name) or
use the [COMPOSE_PROFILESenvironment variable](https://docs.docker.com/compose/how-tos/environment-variables/envvars/#compose_profiles):

```console
$ docker compose --profile debug down
```

```console
$ COMPOSE_PROFILES=debug docker compose down
```

Both commands stop and remove services with the `debug` profile and services without a profile. In the following `compose.yaml` file, this stops the services `db`, `backend` and `phpmyadmin`.

```yaml
services:
  frontend:
    image: frontend
    profiles: [frontend]

  phpmyadmin:
    image: phpmyadmin
    depends_on: [db]
    profiles: [debug]

  backend:
    image: backend

  db:
    image: mysql
```

if you only want to stop the `phpmyadmin` service, you can run

```console
$ docker compose down phpmyadmin
```

or

```console
$ docker compose stop phpmyadmin
```

> Note
>
> Running `docker compose down` only stops `backend` and `db`.

## Reference information

[profiles](https://docs.docker.com/reference/compose-file/services/#profiles)

---

# Specify a project name

> Learn how to set a custom project name in Compose and understand the precedence of each method.

# Specify a project name

   Table of contents

---

By default, Compose assigns the project name based on the name of the directory that contains the Compose file. You can override this with several methods.

This page offers examples of scenarios where custom project names can be helpful, outlines the various methods to set a project name, and provides the order of precedence for each approach.

> Note
>
> The default project directory is the base directory of the Compose file. A custom value can also be set
> for it using the
> [--project-directorycommand line option](https://docs.docker.com/reference/cli/docker/compose/#options).

## Example use cases

Compose uses a project name to isolate environments from each other. There are multiple contexts where a project name is useful:

- On a development host: Create multiple copies of a single environment, useful for running stable copies for each feature branch of a project.
- On a CI server: Prevent interference between builds by setting the project name to a unique build number.
- On a shared or development host: Avoid interference between different projects that might share the same service names.

## Set a project name

Project names must contain only lowercase letters, decimal digits, dashes, and
underscores, and must begin with a lowercase letter or decimal digit. If the
base name of the project directory or current directory violates this
constraint, alternative mechanisms are available.

The precedence order for each method, from highest to lowest, is as follows:

1. The `-p` command line flag.
2. The [COMPOSE_PROJECT_NAME environment variable](https://docs.docker.com/compose/how-tos/environment-variables/envvars/).
3. The
  [top-levelname:attribute](https://docs.docker.com/reference/compose-file/version-and-name/) in your Compose file. Or the last `name:` if you [specify multiple Compose files](https://docs.docker.com/compose/how-tos/multiple-compose-files/merge/) in the command line with the `-f` flag.
4. The base name of the project directory containing your Compose file. Or the base name of the first Compose file if you [specify multiple Compose files](https://docs.docker.com/compose/how-tos/multiple-compose-files/merge/) in the command line with the `-f` flag.
5. The base name of the current directory if no Compose file is specified.

## What's next?

- Read up on [working with multiple Compose files](https://docs.docker.com/compose/how-tos/multiple-compose-files/).
- Explore some [sample apps](https://github.com/docker/awesome-compose).

---

# Use provider services

> Learn how to use provider services in Docker Compose to integrate external capabilities into your applications

# Use provider services

   Table of contents

---

Requires: Docker Compose [2.36.0](https://github.com/docker/compose/releases/tag/v2.36.0) and later

Docker Compose supports provider services, which allow integration with services whose lifecycles are managed by third-party components rather than by Compose itself.
This feature enables you to define and utilize platform-specific services without the need for manual setup or direct lifecycle management.

## What are provider services?

Provider services are a special type of service in Compose that represents platform capabilities rather than containers.
They allow you to declare dependencies on specific platform features that your application needs.

When you define a provider service in your Compose file, Compose works with the platform to provision and configure
the requested capability, making it available to your application services.

## Using provider services

To use a provider service in your Compose file, you need to:

1. Define a service with the `provider` attribute
2. Specify the `type` of provider you want to use
3. Configure any provider-specific options
4. Declare dependencies from your application services to the provider service

Here's a basic example:

```yaml
services:
  database:
    provider:
      type: awesomecloud
      options:
        type: mysql
        foo: bar
  app:
    image: myapp
    depends_on:
       - database
```

Notice the dedicated `provider` attribute in the `database` service.
This attribute specifies that the service is managed by a provider and lets you define options specific to that provider type.

The `depends_on` attribute in the `app` service specifies that it depends on the `database` service.
This means that the `database` service will be started before the `app` service, allowing the provider information
to be injected into the `app` service.

## How it works

During the `docker compose up` command execution, Compose identifies services relying on providers and works with them to provision
the requested capabilities. The provider then populates Compose model with information about how to access the provisioned resource.

This information is passed to services that declare a dependency on the provider service, typically through environment
variables. The naming convention for these variables is:

```env
<PROVIDER_SERVICE_NAME>_<VARIABLE_NAME>
```

For example, if your provider service is named `database`, your application service might receive environment variables like:

- `DATABASE_URL` with the URL to access the provisioned resource
- `DATABASE_TOKEN` with an authentication token
- Other provider-specific variables

Your application can then use these environment variables to interact with the provisioned resource.

## Provider types

The `type` field in a provider service references the name of either:

1. A Docker CLI plugin (e.g., `docker-model`)
2. A binary available in the user's PATH
3. A path to the binary or script to execute

When Compose encounters a provider service, it looks for a plugin or binary with the specified name to handle the provisioning of the requested capability.

For example, if you specify `type: model`, Compose will look for a Docker CLI plugin named `docker-model` or a binary named `model` in the PATH.

```yaml
services:
  ai-runner:
    provider:
      type: model  # Looks for docker-model plugin or model binary
      options:
        model: ai/example-model
```

The plugin or binary is responsible for:

1. Interpreting the options provided in the provider service
2. Provisioning the requested capability
3. Returning information about how to access the provisioned resource

This information is then passed to dependent services as environment variables.

> Tip
>
> If you're working with AI models in Compose, use the
> [modelstop-level element](https://docs.docker.com/ai/compose/models-and-compose/) instead.

## Benefits of using provider services

Using provider services in your Compose applications offers several benefits:

1. Simplified configuration: You don't need to manually configure and manage platform capabilities
2. Declarative approach: You can declare all your application's dependencies in one place
3. Consistent workflow: You use the same Compose commands to manage your entire application, including platform capabilities

## Creating your own provider

If you want to create your own provider to extend Compose with custom capabilities, you can implement a Compose plugin that registers provider types.

For detailed information on how to create and implement your own provider, refer to the [Compose Extensions documentation](https://github.com/docker/compose/blob/main/docs/extension.md).
This guide explains the extension mechanism that allows you to add new provider types to Compose.

## Reference

- [Docker Model Runner documentation](https://docs.docker.com/ai/model-runner/)
- [Compose Extensions documentation](https://github.com/docker/compose/blob/main/docs/extension.md)

---

# Control startup and shutdown order in Compose

> Learn how to manage service startup and shutdown order in Docker Compose using depends_on and healthchecks.

# Control startup and shutdown order in Compose

   Table of contents

---

You can control the order of service startup and shutdown with the
[depends_on](https://docs.docker.com/reference/compose-file/services/#depends_on) attribute. Compose always starts and stops
containers in dependency order, where dependencies are determined by
`depends_on`, `links`, `volumes_from`, and `network_mode: "service:..."`.

For example, if your application needs to access a database and both services are started with `docker compose up`, there is a chance this will fail since the application service might start before the database service and won't find a database able to handle its SQL statements.

## Control startup

On startup, Compose does not wait until a container is "ready", only until it's running. This can cause issues if, for example, you have a relational database system that needs to start its own services before being able to handle incoming connections.

The solution for detecting the ready state of a service is to use the `condition` attribute with one of the following options:

- `service_started`
- `service_healthy`. This specifies that a dependency is expected to be “healthy”, which is defined with `healthcheck`, before starting a dependent service.
- `service_completed_successfully`. This specifies that a dependency is expected to run to successful completion before starting a dependent service.

## Example

```yaml
services:
  web:
    build: .
    depends_on:
      db:
        condition: service_healthy
        restart: true
      redis:
        condition: service_started
  redis:
    image: redis
  db:
    image: postgres:18
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $${POSTGRES_USER} -d $${POSTGRES_DB}"]
      interval: 10s
      retries: 5
      start_period: 30s
      timeout: 10s
```

Compose creates services in dependency order. `db` and `redis` are created before `web`.

Compose waits for healthchecks to pass on dependencies marked with `service_healthy`. `db` is expected to be "healthy" (as indicated by `healthcheck`) before `web` is created.

`restart: true` ensures that if `db` is updated or restarted due to an explicit Compose operation, for example `docker compose restart`, the `web` service is also restarted automatically, ensuring it re-establishes connections or dependencies correctly.

The healthcheck for the `db` service uses the `pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}` command to check if the PostgreSQL database is ready. The service is retried every 10 seconds, up to 5 times.

Compose also removes services in dependency order. `web` is removed before `db` and `redis`.

## Reference information

- [depends_on](https://docs.docker.com/reference/compose-file/services/#depends_on)
- [healthcheck](https://docs.docker.com/reference/compose-file/services/#healthcheck)

---

# Manage secrets securely in Docker Compose

> Learn how to securely manage runtime and build-time secrets in Docker Compose.

# Manage secrets securely in Docker Compose

   Table of contents

---

A secret is any piece of data, such as a password, certificate, or API key, that shouldn’t be transmitted over a network or stored unencrypted in a Dockerfile or in your application’s source code.

Docker Compose provides a way for you to use secrets without having to use environment variables to store information. If you’re injecting passwords and API keys as environment variables, you risk unintentional information exposure. Services can only access secrets when explicitly granted by a `secrets` attribute within the `services` top-level element.

Environment variables are often available to all processes, and it can be difficult to track access. They can also be printed in logs when debugging errors without your knowledge. Using secrets mitigates these risks.

## Use secrets

Secrets are mounted as a file in `/run/secrets/<secret_name>` inside the container.

Getting a secret into a container is a two-step process. First, define the secret using the
[top-level secrets element in your Compose file](https://docs.docker.com/reference/compose-file/secrets/). Next, update your service definitions to reference the secrets they require with the
[secrets attribute](https://docs.docker.com/reference/compose-file/services/#secrets). Compose grants access to secrets on a per-service basis.

Unlike the other methods, this permits granular access control within a service container via standard filesystem permissions.

## Examples

### Single-service secret injection

In the following example, the frontend service is given access to the `my_secret` secret. In the container, `/run/secrets/my_secret` is set to the contents of the file `./my_secret.txt`.

```yaml
services:
  myapp:
    image: myapp:latest
    secrets:
      - my_secret
secrets:
  my_secret:
    file: ./my_secret.txt
```

### Multi-service secret sharing and password management

```yaml
services:
   db:
     image: mysql:latest
     volumes:
       - db_data:/var/lib/mysql
     environment:
       MYSQL_ROOT_PASSWORD_FILE: /run/secrets/db_root_password
       MYSQL_DATABASE: wordpress
       MYSQL_USER: wordpress
       MYSQL_PASSWORD_FILE: /run/secrets/db_password
     secrets:
       - db_root_password
       - db_password

   wordpress:
     depends_on:
       - db
     image: wordpress:latest
     ports:
       - "8000:80"
     environment:
       WORDPRESS_DB_HOST: db:3306
       WORDPRESS_DB_USER: wordpress
       WORDPRESS_DB_PASSWORD_FILE: /run/secrets/db_password
     secrets:
       - db_password

secrets:
   db_password:
     file: db_password.txt
   db_root_password:
     file: db_root_password.txt

volumes:
    db_data:
```

In the advanced example above:

- The `secrets` attribute under each service defines the secrets you want to inject into the specific container.
- The top-level `secrets` section defines the variables `db_password` and `db_root_password` and provides the `file` that populates their values.
- The deployment of each container means Docker creates a bind mount under `/run/secrets/<secret_name>` with their specific values.

> Note
>
> The `_FILE` environment variables demonstrated here are a convention used by some images, including Docker Official Images like [mysql](https://hub.docker.com/_/mysql) and [postgres](https://hub.docker.com/_/postgres).

### Build secrets

In the following example, the `npm_token` secret is made available at build time. Its value is taken from the `NPM_TOKEN` environment variable.

```yaml
services:
  myapp:
    build:
      secrets:
        - npm_token
      context: .

secrets:
  npm_token:
    environment: NPM_TOKEN
```

## Resources

- [Secrets top-level element](https://docs.docker.com/reference/compose-file/secrets/)
- [Secrets attribute for services top-level element](https://docs.docker.com/reference/compose-file/services/#secrets)
- [Build secrets](https://docs.docker.com/build/building/secrets/)

---

# Install the Docker Compose plugin

> Step-by-step instructions for installing the Docker Compose plugin on Linux using a package repository or manual method.

# Install the Docker Compose plugin

   Table of contents

---

This page contains instructions on how to install the Docker Compose plugin on Linux from the command line.

To install the Docker Compose plugin on Linux, you can either:

- [Set up Docker's repository on your Linux system](#install-using-the-repository).
- [Install manually](#install-the-plugin-manually).

> Note
>
> These instructions assume you already have Docker Engine and Docker CLI installed and now want to install the Docker Compose plugin.

## Install using the repository

1. Set up the repository. Find distribution-specific instructions in:
  [Ubuntu](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository) |
  [CentOS](https://docs.docker.com/engine/install/centos/#set-up-the-repository) |
  [Debian](https://docs.docker.com/engine/install/debian/#install-using-the-repository) |
  [Raspberry Pi OS](https://docs.docker.com/engine/install/raspberry-pi-os/#install-using-the-repository) |
  [Fedora](https://docs.docker.com/engine/install/fedora/#set-up-the-repository) |
  [RHEL](https://docs.docker.com/engine/install/rhel/#set-up-the-repository).
2. Update the package index, and install the latest version of Docker Compose:
  - For Ubuntu and Debian, run:
    ```console
    $ sudo apt-get update
    $ sudo apt-get install docker-compose-plugin
    ```
  - For RPM-based distributions, run:
    ```console
    $ sudo yum update
    $ sudo yum install docker-compose-plugin
    ```
3. Verify that Docker Compose is installed correctly by checking the version.
  ```console
  $ docker compose version
  ```

### Update Docker Compose

To update the Docker Compose plugin, run the following commands:

- For Ubuntu and Debian, run:
  ```console
  $ sudo apt-get update
  $ sudo apt-get install docker-compose-plugin
  ```
- For RPM-based distributions, run:
  ```console
  $ sudo yum update
  $ sudo yum install docker-compose-plugin
  ```

## Install the plugin manually

> Warning
>
> Manual installations don’t auto-update. For ease of maintenance, use the Docker repository method.

1. To download and install the Docker Compose CLI plugin, run:
  ```console
  $ DOCKER_CONFIG=${DOCKER_CONFIG:-$HOME/.docker}
  $ mkdir -p $DOCKER_CONFIG/cli-plugins
  $ curl -SL https://github.com/docker/compose/releases/download/v5.0.1/docker-compose-linux-x86_64 -o $DOCKER_CONFIG/cli-plugins/docker-compose
  ```
  This command downloads and installs the latest release of Docker Compose for the active user under `$HOME` directory.
  To install:
  - Docker Compose for *all users* on your system, replace `~/.docker/cli-plugins` with `/usr/local/lib/docker/cli-plugins`.
  - A different version of Compose, substitute `v5.0.1` with the version of Compose you want to use.
  - For a different architecture, substitute `x86_64` with the [architecture you want](https://github.com/docker/compose/releases).
2. Apply executable permissions to the binary:
  ```console
  $ chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose
  ```
  or, if you chose to install Compose for all users:
  ```console
  $ sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
  ```
3. Test the installation.
  ```console
  $ docker compose version
  ```

## What's next?

- [Understand how Compose works](https://docs.docker.com/compose/intro/compose-application-model/)
- [Try the Quickstart guide](https://docs.docker.com/compose/gettingstarted/)

---

# Install the Docker Compose standalone (Legacy)

> Instructions for installing the legacy Docker Compose standalone tool on Linux and Windows Server

# Install the Docker Compose standalone (Legacy)

   Table of contents

---

> Warning
>
> This install scenario is not recommended and is only supported for backward compatibility purposes.

This page contains instructions on how to install Docker Compose standalone on Linux or Windows Server, from the command line.

> Warning
>
> The Docker Compose standalone uses the `-compose` syntax instead of the current standard syntax `compose`.
> For example, you must type `docker-compose up` when using Docker Compose standalone, instead of `docker compose up`.
> Use it only for backward compatibility.

## On Linux

1. To download and install the Docker Compose standalone, run:
  ```console
  $ curl -SL https://github.com/docker/compose/releases/download/v5.0.1/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
  ```
2. Apply executable permissions to the standalone binary in the target path for the installation.
  ```console
  $ chmod +x /usr/local/bin/docker-compose
  ```
3. Test and execute Docker Compose commands using `docker-compose`.

> Tip
>
> If the command `docker-compose` fails after installation, check your path.
> You can also create a symbolic link to `/usr/bin` or any other directory in your path.
> For example:
>
>
>
> ```console
> $ sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
> ```

## On Windows Server

Follow these instructions if you are
[running the Docker daemon directly
on Microsoft Windows Server](https://docs.docker.com/engine/install/binaries/#install-server-and-client-binaries-on-windows) and want to install Docker Compose.

1. Run PowerShell as an administrator.
  In order to proceed with the installation, select **Yes** when asked if you want this app to make changes to your device.
2. Optional. Ensure TLS1.2 is enabled.
  GitHub requires TLS1.2 for secure connections. If you’re using an older version of Windows Server, for example 2016, or suspect that TLS1.2 is not enabled, run the following command in PowerShell:
  ```powershell
  [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
  ```
3. Download the latest release of Docker Compose (v5.0.1). Run the following command:
  ```powershell
  Start-BitsTransfer -Source "https://github.com/docker/compose/releases/download/v5.0.1/docker-compose-windows-x86_64.exe" -Destination $Env:ProgramFiles\Docker\docker-compose.exe
  ```
  To install a different version of Docker Compose, substitute `v5.0.1` with the version of Compose you want to use.
  > Note
  >
  > On Windows Server 2019 you can add the Compose executable to `$Env:ProgramFiles\Docker`.
  > Because this directory is registered in the system `PATH`, you can run the `docker-compose --version`
  > command on the subsequent step with no additional configuration.
4. Test the installation.
  ```console
  $ docker-compose.exe version
  Docker Compose version v5.0.1
  ```

## What's next?

- [Understand how Compose works](https://docs.docker.com/compose/intro/compose-application-model/)
- [Try the Quickstart guide](https://docs.docker.com/compose/gettingstarted/)

---

# Uninstall Docker Compose

> How to uninstall Docker Compose

# Uninstall Docker Compose

   Table of contents

---

How you uninstall Docker Compose depends on how it was installed. This guide covers uninstallation instructions for:

- Docker Compose installed via Docker Desktop
- Docker Compose installed as a CLI plugin

## Uninstalling Docker Compose with Docker Desktop

If you want to uninstall Docker Compose and you have installed Docker Desktop, see
[Uninstall Docker Desktop](https://docs.docker.com/desktop/uninstall/).

> Warning
>
> Unless you have other Docker instances installed on that specific environment, uninstalling Docker Desktop removes all Docker components, including Docker Engine, Docker CLI, and Docker Compose.

## Uninstalling the Docker Compose CLI plugin

If you installed Docker Compose via a package manager, run:

On Ubuntu or Debian:

```console
$ sudo apt-get remove docker-compose-plugin
```

On RPM-based distributions:

```console
$ sudo yum remove docker-compose-plugin
```

### Manually installed

If you installed Docker Compose manually (using curl), remove it by deleting the binary:

```console
$ rm $DOCKER_CONFIG/cli-plugins/docker-compose
```

### Remove for all users

If installed for all users, remove it from the system directory:

```console
$ rm /usr/local/lib/docker/cli-plugins/docker-compose
```

> Note
>
> If you get a **Permission denied** error using either of the previous
> methods, you do not have the permissions needed to remove
> Docker Compose. To force the removal, prepend `sudo` to either of the previous instructions and run it again.

### Inspect the location of the Compose CLI plugin

To check where Compose is installed, use:

```console
$ docker info --format '{{range .ClientInfo.Plugins}}{{if eq .Name "compose"}}{{.Path}}{{end}}{{end}}'
```

---

# Overview of installing Docker Compose

> Learn how to install Docker Compose. Compose is available natively on Docker Desktop, as a Docker Engine plugin, and as a standalone tool.

# Overview of installing Docker Compose

   Table of contents

---

This page summarizes the different ways you can install Docker Compose, depending on your platform and needs.

## Installation scenarios

### Docker Desktop (Recommended)

The easiest and recommended way to get Docker Compose is to install Docker Desktop.

Docker Desktop includes Docker Compose along with Docker Engine and Docker CLI which are Compose prerequisites.

Docker Desktop is available for:

- [Linux](https://docs.docker.com/desktop/setup/install/linux/)
- [Mac](https://docs.docker.com/desktop/setup/install/mac-install/)
- [Windows](https://docs.docker.com/desktop/setup/install/windows-install/)

> Tip
>
> If you have already installed Docker Desktop, you can check which version of Compose you have by selecting **About Docker Desktop** from the Docker menu
> ![whale menu](https://docs.docker.com/desktop/images/whale-x.svg)
> .

### Plugin (Linux only)

> Important
>
> This method is only available on Linux.

If you already have Docker Engine and Docker CLI installed, you can install the Docker Compose plugin from the command line, by either:

- [Using Docker's repository](https://docs.docker.com/compose/install/linux/#install-using-the-repository)
- [Downloading and installing manually](https://docs.docker.com/compose/install/linux/#install-the-plugin-manually)

### Standalone (Legacy)

> Warning
>
> This install scenario is not recommended and is only supported for backward compatibility purposes.

You can [install the Docker Compose standalone](https://docs.docker.com/compose/install/standalone/) on Linux or on Windows Server.

---

# How Compose works

> Learn how Docker Compose works, from the application model to Compose files and CLI, whilst following a detailed example.

# How Compose works

   Table of contents

---

With Docker Compose you use a YAML configuration file, known as the [Compose file](#the-compose-file), to configure your application’s services, and then you create and start all the services from your configuration with the [Compose CLI](#cli).

The Compose file, or `compose.yaml` file, follows the rules provided by the
[Compose Specification](https://docs.docker.com/reference/compose-file/) in how to define multi-container applications. This is the Docker Compose implementation of the formal [Compose Specification](https://github.com/compose-spec/compose-spec).

Computing components of an application are defined as
[services](https://docs.docker.com/reference/compose-file/services/). A service is an abstract concept implemented on platforms by running the same container image, and configuration, one or more times.

Services communicate with each other through
[networks](https://docs.docker.com/reference/compose-file/networks/). In the Compose Specification, a network is a platform capability abstraction to establish an IP route between containers within services connected together.

Services store and share persistent data into
[volumes](https://docs.docker.com/reference/compose-file/volumes/). The Specification describes such a persistent data as a high-level filesystem mount with global options.

Some services require configuration data that is dependent on the runtime or platform. For this, the Specification defines a dedicated
[configs](https://docs.docker.com/reference/compose-file/configs/) concept. From inside the container, configs behave like volumes—they’re mounted as files. However, configs are defined differently at the platform level.

A
[secret](https://docs.docker.com/reference/compose-file/secrets/) is a specific flavor of configuration data for sensitive data that should not be exposed without security considerations. Secrets are made available to services as files mounted into their containers, but the platform-specific resources to provide sensitive data are specific enough to deserve a distinct concept and definition within the Compose Specification.

> Note
>
> With volumes, configs and secrets you can have a simple declaration at the top-level and then add more platform-specific information at the service level.

A project is an individual deployment of an application specification on a platform. A project's name, set with the top-level
[name](https://docs.docker.com/reference/compose-file/version-and-name/) attribute, is used to group
resources together and isolate them from other applications or other installation of the same Compose-specified application with distinct parameters. If you are creating resources on a platform, you must prefix resource names by project and
set the label `com.docker.compose.project`.

Compose offers a way for you to set a custom project name and override this name, so that the same `compose.yaml` file can be deployed twice on the same infrastructure, without changes, by just passing a distinct name.

## The Compose file

The default path for a Compose file is `compose.yaml` (preferred) or `compose.yml` that is placed in the working directory.
Compose also supports `docker-compose.yaml` and `docker-compose.yml` for backwards compatibility of earlier versions.
If both files exist, Compose prefers the canonical `compose.yaml`.

You can use
[fragments](https://docs.docker.com/reference/compose-file/fragments/) and
[extensions](https://docs.docker.com/reference/compose-file/extension/) to keep your Compose file efficient and easy to maintain.

Multiple Compose files can be
[merged](https://docs.docker.com/reference/compose-file/merge/) together to define the application model. The combination of YAML files is implemented by appending or overriding YAML elements based on the Compose file order you set.
Simple attributes and maps get overridden by the highest order Compose file, lists get merged by appending. Relative
paths are resolved based on the first Compose file's parent folder, whenever complementary files being
merged are hosted in other folders. As some Compose file elements can both be expressed as single strings or complex objects, merges apply to
the expanded form. For more information, see
[Working with multiple Compose files](https://docs.docker.com/compose/how-tos/multiple-compose-files/).

If you want to reuse other Compose files, or factor out parts of your application model into separate Compose files, you can also use
[include](https://docs.docker.com/reference/compose-file/include/). This is useful if your Compose application is dependent on another application which is managed by a different team, or needs to be shared with others.

## CLI

The Docker CLI lets you interact with your Docker Compose applications through the `docker compose` command and its subcommands. If you're using Docker Desktop, the Docker Compose CLI is included by default.

Using the CLI, you can manage the lifecycle of your multi-container applications defined in the `compose.yaml` file. The CLI commands enable you to start, stop, and configure your applications effortlessly.

### Key commands

To start all the services defined in your `compose.yaml` file:

```console
$ docker compose up
```

To stop and remove the running services:

```console
$ docker compose down
```

If you want to monitor the output of your running containers and debug issues, you can view the logs with:

```console
$ docker compose logs
```

To list all the services along with their current status:

```console
$ docker compose ps
```

For a full list of all the Compose CLI commands, see the
[reference documentation](https://docs.docker.com/reference/cli/docker/compose/).

## Illustrative example

The following example illustrates the Compose concepts outlined above. The example is non-normative.

Consider an application split into a frontend web application and a backend service.

The frontend is configured at runtime with an HTTP configuration file managed by infrastructure, providing an external domain name, and an HTTPS server certificate injected by the platform's secured secret store.

The backend stores data in a persistent volume.

Both services communicate with each other on an isolated back-tier network, while the frontend is also connected to a front-tier network and exposes port 443 for external usage.

![Compose application example](https://docs.docker.com/compose/images/compose-application.webp)  ![Compose application example](https://docs.docker.com/compose/images/compose-application.webp)

The example application is composed of the following parts:

- Two services, backed by Docker images: `webapp` and `database`
- One secret (HTTPS certificate), injected into the frontend
- One configuration (HTTP), injected into the frontend
- One persistent volume, attached to the backend
- Two networks

```yml
services:
  frontend:
    image: example/webapp
    ports:
      - "443:8043"
    networks:
      - front-tier
      - back-tier
    configs:
      - httpd-config
    secrets:
      - server-certificate

  backend:
    image: example/database
    volumes:
      - db-data:/etc/data
    networks:
      - back-tier

volumes:
  db-data:
    driver: flocker
    driver_opts:
      size: "10GiB"

configs:
  httpd-config:
    external: true

secrets:
  server-certificate:
    external: true

networks:
  # The presence of these objects is sufficient to define them
  front-tier: {}
  back-tier: {}
```

The `docker compose up` command starts the `frontend` and `backend` services, creates the necessary networks and volumes, and injects the configuration and secret into the frontend service.

`docker compose ps` provides a snapshot of the current state of your services, making it easy to see which containers are running, their status, and the ports they are using:

```text
$ docker compose ps

NAME                IMAGE                COMMAND                  SERVICE             CREATED             STATUS              PORTS
example-frontend-1  example/webapp       "nginx -g 'daemon of…"   frontend            2 minutes ago       Up 2 minutes        0.0.0.0:443->8043/tcp
example-backend-1   example/database     "docker-entrypoint.s…"   backend             2 minutes ago       Up 2 minutes
```

## What's next

- [Try the Quickstart guide](https://docs.docker.com/compose/gettingstarted/)
- [Explore some sample applications](https://github.com/docker/awesome-compose)
- [Familiarize yourself with the Compose Specification](https://docs.docker.com/reference/compose-file/)

---

# Why use Compose?

> Discover the benefits and typical use cases of Docker Compose for containerized application development and deployment

# Why use Compose?

   Table of contents

---

## Key benefits of Docker Compose

Using Docker Compose offers several benefits that streamline the development, deployment, and management of containerized applications:

- Simplified control: Define and manage multi-container apps in one YAML file, streamlining orchestration and replication.
- Efficient collaboration: Shareable YAML files support smooth collaboration between developers and operations, improving workflows and issue resolution, leading to increased overall efficiency.
- Rapid application development: Compose caches the configuration used to create a container. When you restart a service that has not changed, Compose re-uses the existing containers. Re-using containers means that you can make changes to your environment very quickly.
- Portability across environments: Compose supports variables in the Compose file. You can use these variables to customize your composition for different environments, or different users.

## Common use cases of Docker Compose

Compose can be used in many different ways. Some common use cases are outlined
below.

### Development environments

When you're developing software, the ability to run an application in an
isolated environment and interact with it is crucial. The Compose command
line tool can be used to create the environment and interact with it.

The
[Compose file](https://docs.docker.com/reference/compose-file/) provides a way to document and configure
all of the application's service dependencies (databases, queues, caches,
web service APIs, etc). Using the Compose command line tool you can create
and start one or more containers for each dependency with a single command
(`docker compose up`).

Together, these features provide a convenient way for you to get
started on a project. Compose can reduce a multi-page "developer getting
started guide" to a single machine-readable Compose file and a few commands.

### Automated testing environments

An important part of any Continuous Deployment or Continuous Integration process
is the automated test suite. Automated end-to-end testing requires an
environment in which to run tests. Compose provides a convenient way to create
and destroy isolated testing environments for your test suite. By defining the full environment in a
[Compose file](https://docs.docker.com/reference/compose-file/), you can create and destroy these environments in just a few commands:

```console
$ docker compose up -d
$ ./run_tests
$ docker compose down
```

### Single host deployments

Compose has traditionally been focused on development and testing workflows,
but with each release we're making progress on more production-oriented features.

For details on using production-oriented features, see
[Compose in production](https://docs.docker.com/compose/how-tos/production/).

## What's next?

- [Learn about the history of Compose](https://docs.docker.com/compose/intro/history/)
- [Understand how Compose works](https://docs.docker.com/compose/intro/compose-application-model/)
- [Try the Quickstart guide](https://docs.docker.com/compose/gettingstarted/)

---

# History and development of Docker Compose

> Explore the evolution of Docker Compose from v1 to v5, including CLI changes, YAML versioning, and the Compose Specification.

# History and development of Docker Compose

   Table of contents

---

This page provides:

- A brief history of the development of the Docker Compose CLI
- A clear explanation of the major versions and file formats that make up Compose v1, v2, and v5
- The main differences between Compose v1, v2, and v5

## Introduction

![Image showing the main differences between Compose v1, Compose v2, and Compose v5](https://docs.docker.com/compose/images/v1-versus-v2-versus-v5.png)  ![Image showing the main differences between Compose v1, Compose v2, and Compose v5](https://docs.docker.com/compose/images/v1-versus-v2-versus-v5.png)

The diagram above highlights the key differences between Docker Compose v1, v2, and v5. Today, the supported Docker Compose CLI versions are Compose v2 and Compose v5, both of which are defined by the
[Compose Specification](https://docs.docker.com/reference/compose-file/).

The diagram provides a high-level comparison of file formats, command-line syntax, and supported top-level elements. This is covered in more detail in the following sections.

### Docker Compose CLI versioning

Compose v1 was first released in 2014. It was written in Python and invoked with `docker-compose`.
Typically, Compose v1 projects include a top-level `version` element in the `compose.yaml` file, with values ranging from `2.0` to `3.8`, which refer to the specific [file formats](#compose-file-format-versioning).

Compose v2, announced in 2020, is written in Go and is invoked with `docker compose`.
Unlike v1, Compose v2 ignores the `version` top-level element in the `compose.yaml` file and relies entirely on the Compose Specification to interpret the file.

Compose v5, released in 2025, is functionally identical to Compose v2. Its primary distinction is the introduction of an official
[Go SDK](https://docs.docker.com/compose/compose-sdk/). This SDK provides a comprehensive API that lets you integrate Compose functionality directly into your applications, allowing you to load, validate, and manage multi-container environments without relying on the Compose CLI. To avoid confusion with the legacy Compose file formats labeled “v2” and “v3,” the versioning was advanced directly to v5.

### Compose file format versioning

The Docker Compose CLIs are defined by specific file formats.

Three major versions of the Compose file format for Compose v1 were released:

- Compose file format 1 with Compose 1.0.0 in 2014
- Compose file format 2.x with Compose 1.6.0 in 2016
- Compose file format 3.x with Compose 1.10.0 in 2017

Compose file format 1 is substantially different to all the following formats as it lacks a top-level `services` key.
Its usage is historical and files written in this format don't run with Compose v2.

Compose file format 2.x and 3.x are very similar to each other, but the latter introduced many new options targeted at Swarm deployments.

To address confusion around Compose CLI versioning, Compose file format versioning, and feature parity depending on whether Swarm mode was in use, file format 2.x and 3.x were merged into the
[Compose Specification](https://docs.docker.com/reference/compose-file/).

Compose v2 and v5 uses the Compose Specification for project definition. Unlike the prior file formats, the Compose Specification is rolling and makes the `version` top-level element optional. Compose v2 and v5 also makes use of optional specifications -
[Deploy](https://docs.docker.com/reference/compose-file/deploy/),
[Develop](https://docs.docker.com/reference/compose-file/develop/), and
[Build](https://docs.docker.com/reference/compose-file/build/).

To make migration easier, Compose v2 and v5 has backwards compatibility for certain elements that have been deprecated or changed between Compose file format 2.x/3.x and the Compose Specification.

## What's next?

- [How Compose works](https://docs.docker.com/compose/intro/compose-application-model/)
- [Compose Specification reference](https://docs.docker.com/reference/compose-file/)
