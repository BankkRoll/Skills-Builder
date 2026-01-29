# Use containers for .NET development and more

# Use containers for .NET development

> Learn how to develop your .NET application locally using containers.

# Use containers for .NET development

   Table of contents

---

## Prerequisites

Complete [Containerize a .NET application](https://docs.docker.com/guides/dotnet/containerize/).

## Overview

In this section, you'll learn how to set up a development environment for your containerized application. This includes:

- Adding a local database and persisting data
- Configuring Compose to automatically update your running Compose services as you edit and save your code
- Creating a development container that contains the .NET Core SDK tools and dependencies

## Update the application

This section uses a different branch of the `docker-dotnet-sample` repository
that contains an updated .NET application. The updated application is on the
`add-db` branch of the repository you cloned in [Containerize a .NET
application](https://docs.docker.com/guides/dotnet/containerize/).

To get the updated code, you need to checkout the `add-db` branch. For the changes you made in [Containerize a .NET application](https://docs.docker.com/guides/dotnet/containerize/), for this section, you can stash them. In a terminal, run the following commands in the `docker-dotnet-sample` directory.

1. Stash any previous changes.
  ```console
  $ git stash -u
  ```
2. Check out the new branch with the updated application.
  ```console
  $ git checkout add-db
  ```

In the `add-db` branch, only the .NET application has been updated. None of the Docker assets have been updated yet.

You should now have the following in your `docker-dotnet-sample` directory.

```text
├── docker-dotnet-sample/
│ ├── .git/
│ ├── src/
│ │ ├── Data/
│ │ ├── Models/
│ │ ├── Pages/
│ │ ├── Properties/
│ │ ├── wwwroot/
│ │ ├── appsettings.Development.json
│ │ ├── appsettings.json
│ │ ├── myWebApp.csproj
│ │ └── Program.cs
│ ├── tests/
│ │ ├── tests.csproj
│ │ ├── UnitTest1.cs
│ │ └── Usings.cs
│ ├── .dockerignore
│ ├── .gitignore
│ ├── compose.yaml
│ ├── Dockerfile
│ ├── README.Docker.md
│ └── README.md
```

## Add a local database and persist data

You can use containers to set up local services, like a database. In this section, you'll update the `compose.yaml` file to define a database service and a volume to persist data.

Open the `compose.yaml` file in an IDE or text editor. You'll notice it
already contains commented-out instructions for a PostgreSQL database and volume.

Open `docker-dotnet-sample/src/appsettings.json` in an IDE or text editor. You'll
notice the connection string with all the database information. The
`compose.yaml` already contains this information, but it's commented out.
Uncomment the database instructions in the `compose.yaml` file.

The following is the updated `compose.yaml` file.

```yaml
services:
  server:
    build:
      context: .
      target: final
    ports:
      - 8080:8080
    depends_on:
      db:
        condition: service_healthy
  db:
    image: postgres:18
    restart: always
    user: postgres
    secrets:
      - db-password
    volumes:
      - db-data:/var/lib/postgresql
    environment:
      - POSTGRES_DB=example
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    expose:
      - 5432
    healthcheck:
      test: ["CMD", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5
volumes:
  db-data:
secrets:
  db-password:
    file: db/password.txt
```

> Note
>
> To learn more about the instructions in the Compose file, see
> [Compose file
> reference](https://docs.docker.com/reference/compose-file/).

Before you run the application using Compose, notice that this Compose file uses
`secrets` and specifies a `password.txt` file to hold the database's password.
You must create this file as it's not included in the source repository.

In the `docker-dotnet-sample` directory, create a new directory named `db` and
inside that directory create a file named `password.txt`. Open `password.txt` in an IDE or text editor and add the following password. The password must be on a single line, with no additional lines in the file.

```text
example
```

Save and close the `password.txt` file.

You should now have the following in your `docker-dotnet-sample` directory.

```text
├── docker-dotnet-sample/
│ ├── .git/
│ ├── db/
│ │ └── password.txt
│ ├── src/
│ ├── tests/
│ ├── .dockerignore
│ ├── .gitignore
│ ├── compose.yaml
│ ├── Dockerfile
│ ├── README.Docker.md
│ └── README.md
```

Run the following command to start your application.

```console
$ docker compose up --build
```

Open a browser and view the application at [http://localhost:8080](http://localhost:8080). You should see a simple web application with the text `Student name is`.

The application doesn't display a name because the database is empty. For this application, you need to access the database and then add records.

## Add records to the database

For the sample application, you must access the database directly to create sample records.

You can run commands inside the database container using the `docker exec`
command. Before running that command, you must get the ID of the database
container. Open a new terminal window and run the following command to list all
your running containers.

```console
$ docker container ls
```

You should see output like the following.

```console
CONTAINER ID   IMAGE                  COMMAND                  CREATED              STATUS                        PORTS                    NAMES
cb36e310aa7e   docker-dotnet-server   "dotnet myWebApp.dll"    About a minute ago   Up About a minute             0.0.0.0:8080->8080/tcp   docker-dotnet-server-1
39fdcf0aff7b   postgres               "docker-entrypoint.s…"   About a minute ago   Up About a minute (healthy)   5432/tcp                 docker-dotnet-db-1
```

In the previous example, the container ID is `39fdcf0aff7b`. Run the following command to connect to the postgres database in the container. Replace the container ID with your own container ID.

```console
$ docker exec -it 39fdcf0aff7b psql -d example -U postgres
```

And finally, insert a record into the database.

```console
example=# INSERT INTO "Students" ("ID", "LastName", "FirstMidName", "EnrollmentDate") VALUES (DEFAULT, 'Whale', 'Moby', '2013-03-20');
```

You should see output like the following.

```console
INSERT 0 1
```

Close the database connection and exit the container shell by running `exit`.

```console
example=# exit
```

## Verify that data persists in the database

Open a browser and view the application at [http://localhost:8080](http://localhost:8080). You should see a simple web application with the text `Student name is Whale Moby`.

Press `ctrl+c` in the terminal to stop your application.

In the terminal, run `docker compose rm` to remove your containers and then run `docker compose up` to run your application again.

```console
$ docker compose rm
$ docker compose up --build
```

Refresh [http://localhost:8080](http://localhost:8080) in your browser and verify that the student name persisted, even after the containers were removed and ran again.

Press `ctrl+c` in the terminal to stop your application.

## Automatically update services

Use Compose Watch to automatically update your running Compose services as you edit and save your code. For more details about Compose Watch, see
[Use Compose Watch](https://docs.docker.com/compose/how-tos/file-watch/).

Open your `compose.yaml` file in an IDE or text editor and then add the Compose Watch instructions. The following is the updated `compose.yaml` file.

```yaml
services:
  server:
    build:
      context: .
      target: final
    ports:
      - 8080:8080
    depends_on:
      db:
        condition: service_healthy
    develop:
      watch:
        - action: rebuild
          path: .
  db:
    image: postgres:18
    restart: always
    user: postgres
    secrets:
      - db-password
    volumes:
      - db-data:/var/lib/postgresql
    environment:
      - POSTGRES_DB=example
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    expose:
      - 5432
    healthcheck:
      test: ["CMD", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5
volumes:
  db-data:
secrets:
  db-password:
    file: db/password.txt
```

Run the following command to run your application with Compose Watch.

```console
$ docker compose watch
```

Open a browser and verify that the application is running at [http://localhost:8080](http://localhost:8080).

Any changes to the application's source files on your local machine will now be
immediately reflected in the running container.

Open `docker-dotnet-sample/src/Pages/Index.cshtml` in an IDE or text editor and update the student name text on line 13 from `Student name is` to `Student name:`.

```diff
-    <p>Student Name is @Model.StudentName</p>
+    <p>Student name: @Model.StudentName</p>
```

Save the changes to `Index.cshmtl` and then wait a few seconds for the application to rebuild. Refresh [http://localhost:8080](http://localhost:8080) in your browser and verify that the updated text appears.

Press `ctrl+c` in the terminal to stop your application.

## Create a development container

At this point, when you run your containerized application, it's using the .NET runtime image. While this small image is good for production, it lacks the SDK tools and dependencies you may need when developing. Also, during development, you may not need to run `dotnet publish`. You can use multi-stage builds to build stages for both development and production in the same Dockerfile. For more details, see
[Multi-stage builds](https://docs.docker.com/build/building/multi-stage/).

Add a new development stage to your Dockerfile and update your `compose.yaml` file to use this stage for local development.

The following is the updated Dockerfile.

```Dockerfile
# syntax=docker/dockerfile:1

FROM --platform=$BUILDPLATFORM mcr.microsoft.com/dotnet/sdk:8.0-alpine AS build
ARG TARGETARCH
COPY . /source
WORKDIR /source/src
RUN --mount=type=cache,id=nuget,target=/root/.nuget/packages \
    dotnet publish -a ${TARGETARCH/amd64/x64} --use-current-runtime --self-contained false -o /app

FROM mcr.microsoft.com/dotnet/sdk:8.0-alpine AS development
COPY . /source
WORKDIR /source/src
CMD dotnet run --no-launch-profile

FROM mcr.microsoft.com/dotnet/aspnet:8.0-alpine AS final
WORKDIR /app
COPY --from=build /app .
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser
USER appuser
ENTRYPOINT ["dotnet", "myWebApp.dll"]
```

The following is the updated `compose.yaml` file.

```yaml
services:
  server:
    build:
      context: .
      target: development
    ports:
      - 8080:8080
    depends_on:
      db:
        condition: service_healthy
    develop:
      watch:
        - action: rebuild
          path: .
    environment:
      - ASPNETCORE_ENVIRONMENT=Development
  db:
    image: postgres:18
    restart: always
    user: postgres
    secrets:
      - db-password
    volumes:
      - db-data:/var/lib/postgresql
    environment:
      - POSTGRES_DB=example
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    expose:
      - 5432
    healthcheck:
      test: ["CMD", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5
volumes:
  db-data:
secrets:
  db-password:
    file: db/password.txt
```

Your containerized application will now use the `mcr.microsoft.com/dotnet/sdk:8.0-alpine` image, which includes development tools like `dotnet test`. Continue to the next section to learn how you can run `dotnet test`.

## Summary

In this section, you took a look at setting up your Compose file to add a local
database and persist data. You also learned how to use Compose Watch to automatically rebuild and run your container when you update your code. And finally, you learned how to create a development container that contains the SDK tools and dependencies needed for development.

Related information:

- [Compose file reference](https://docs.docker.com/reference/compose-file/)
- [Compose file watch](https://docs.docker.com/compose/how-tos/file-watch/)
- [Multi-stage builds](https://docs.docker.com/build/building/multi-stage/)

## Next steps

In the next section, you'll learn how to run unit tests using Docker.

---

# Run .NET tests in a container

> Learn how to run your .NET tests in a container.

# Run .NET tests in a container

   Table of contents

---

## Prerequisites

Complete all the previous sections of this guide, starting with [Containerize a .NET application](https://docs.docker.com/guides/dotnet/containerize/).

## Overview

Testing is an essential part of modern software development. Testing can mean a
lot of things to different development teams. There are unit tests, integration
tests and end-to-end testing. In this guide you take a look at running your unit
tests in Docker when developing and when building.

## Run tests when developing locally

The sample application already has an xUnit test inside the `tests` directory. When developing locally, you can use Compose to run your tests.

Run the following command in the `docker-dotnet-sample` directory to run the tests inside a container.

```console
$ docker compose run --build --rm server dotnet test /source/tests
```

You should see output that contains the following.

```console
Starting test execution, please wait...
A total of 1 test files matched the specified pattern.

Passed!  - Failed:     0, Passed:     1, Skipped:     0, Total:     1, Duration: < 1 ms - /source/tests/bin/Debug/net8.0/tests.dll (net8.0)
```

To learn more about the command, see
[docker compose run](https://docs.docker.com/reference/cli/docker/compose/run/).

## Run tests when building

To run your tests when building, you need to update your Dockerfile. You can create a new test stage that runs the tests, or run the tests in the existing build stage. For this guide, update the Dockerfile to run the tests in the build stage.

The following is the updated Dockerfile.

```dockerfile
# syntax=docker/dockerfile:1

FROM --platform=$BUILDPLATFORM mcr.microsoft.com/dotnet/sdk:8.0-alpine AS build
ARG TARGETARCH
COPY . /source
WORKDIR /source/src
RUN --mount=type=cache,id=nuget,target=/root/.nuget/packages \
    dotnet publish -a ${TARGETARCH/amd64/x64} --use-current-runtime --self-contained false -o /app
RUN dotnet test /source/tests

FROM mcr.microsoft.com/dotnet/sdk:8.0-alpine AS development
COPY . /source
WORKDIR /source/src
CMD dotnet run --no-launch-profile

FROM mcr.microsoft.com/dotnet/aspnet:8.0-alpine AS final
WORKDIR /app
COPY --from=build /app .
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser
USER appuser
ENTRYPOINT ["dotnet", "myWebApp.dll"]
```

Run the following command to build an image using the build stage as the target and view the test results. Include `--progress=plain` to view the build output, `--no-cache` to ensure the tests always run, and `--target build` to target the build stage.

```console
$ docker build -t dotnet-docker-image-test --progress=plain --no-cache --target build .
```

You should see output containing the following.

```console
#11 [build 5/5] RUN dotnet test /source/tests
#11 1.564   Determining projects to restore...
#11 3.421   Restored /source/src/myWebApp.csproj (in 1.02 sec).
#11 19.42   Restored /source/tests/tests.csproj (in 17.05 sec).
#11 27.91   myWebApp -> /source/src/bin/Debug/net8.0/myWebApp.dll
#11 28.47   tests -> /source/tests/bin/Debug/net8.0/tests.dll
#11 28.49 Test run for /source/tests/bin/Debug/net8.0/tests.dll (.NETCoreApp,Version=v8.0)
#11 28.67 Microsoft (R) Test Execution Command Line Tool Version 17.3.3 (x64)
#11 28.67 Copyright (c) Microsoft Corporation.  All rights reserved.
#11 28.68
#11 28.97 Starting test execution, please wait...
#11 29.03 A total of 1 test files matched the specified pattern.
#11 32.07
#11 32.08 Passed!  - Failed:     0, Passed:     1, Skipped:     0, Total:     1, Duration: < 1 ms - /source/tests/bin/Debug/net8.0/tests.dll (net8.0)
#11 DONE 32.2s
```

## Summary

In this section, you learned how to run tests when developing locally using Compose and how to run tests when building your image.

Related information:

- [docker compose run](https://docs.docker.com/reference/cli/docker/compose/run/)

## Next steps

Next, you’ll learn how to set up a CI/CD pipeline using GitHub Actions.

---

# .NET language

> Containerize and develop .NET apps using Docker

# .NET language-specific guide

---

The .NET getting started guide teaches you how to create a containerized .NET application using Docker. In this guide, you'll learn how to:

- Containerize and run a .NET application
- Set up a local environment to develop a .NET application using containers
- Run tests for a .NET application using containers
- Configure a CI/CD pipeline for a containerized .NET application using GitHub Actions
- Deploy your containerized application locally to Kubernetes to test and debug your deployment

After completing the .NET getting started modules, you should be able to containerize your own .NET application based on the examples and instructions provided in this guide.

Start by containerizing an existing .NET application.

## Modules

1. [Containerize your app](https://docs.docker.com/guides/dotnet/containerize/)
  Learn how to containerize an ASP.NET application.
2. [Develop your app](https://docs.docker.com/guides/dotnet/develop/)
  Learn how to develop your .NET application locally using containers.
3. [Run your tests](https://docs.docker.com/guides/dotnet/run-tests/)
  Learn how to run your .NET tests in a container.
4. [Configure CI/CD](https://docs.docker.com/guides/dotnet/configure-ci-cd/)
  Learn how to Configure CI/CD for your .NET application
5. [Test your deployment](https://docs.docker.com/guides/dotnet/deploy/)
  Learn how to deploy your application

---

# Common Questions on Using Laravel with Docker

> Find answers to common questions about setting up and managing Laravel environments with Docker Compose, including troubleshooting and best practices.

# Common Questions on Using Laravel with Docker

   Table of contents

---

## 1. Why should I use Docker Compose for Laravel?

Docker Compose is a powerful tool for managing multi-container environments, particularly in development due to its simplicity. With Docker Compose, you can define and connect all necessary services for Laravel, such as PHP, Nginx, and databases, in a single configuration (`compose.*.yaml`). This setup ensures consistency across development, testing, and production environments, streamlining onboarding and reducing discrepancies between local and server setups.

While Docker Compose is a great choice for development, tools like **Docker Swarm** or **Kubernetes** offer advanced scaling and orchestration features, which may be beneficial for complex production deployments.

## 2. How do I debug my Laravel application with Docker Compose?

To debug your Laravel application in a Docker environment, use **Xdebug**. In the development setup, Xdebug is installed in the `php-fpm` container to enable debugging. Ensure Xdebug is enabled in your `compose.dev.yaml` file by setting the environment variable `XDEBUG_ENABLED=true` and configuring your IDE (e.g., Visual Studio Code or PHPStorm) to connect to the remote container for debugging.

## 3. Can I use Docker Compose with databases other than PostgreSQL?

Yes, Docker Compose supports various database services for Laravel. While PostgreSQL is used in the examples, you can easily substitute **MySQL**, **MariaDB**, or even **SQLite**. Update the `compose.*.yaml` file to specify the required Docker image and adjust your `.env` file to reflect the new database configuration.

## 4. How can I persist data in development and production?

In both development and production, Docker volumes are used to persist data. For instance, in the `compose.*.yaml` file, the `postgres-data-*` volume stores PostgreSQL data, ensuring that data is retained even if the container restarts. You can also define named volumes for other services where data persistence is essential.

## 5. What is the difference between development and production Docker configurations?

In a development environment, Docker configurations include tools that streamline coding and debugging, such as Xdebug for debugging, and volume mounts to enable real-time code updates without requiring image rebuilds.

In production, the configuration is optimized for performance, security, and efficiency. This setup uses multi-stage builds to keep the image lightweight and includes only essential tools, packages, and libraries.

It’s recommended to use `alpine`-based images in production for smaller image sizes, enhancing deployment speed and security.

Additionally, consider using
[Docker Scout](https://docs.docker.com/scout/) to detect and analyze vulnerabilities, especially in production environments.

For additional information about using Docker Compose in production, see
[this guide](https://docs.docker.com/compose/how-tos/production/).

---

# Laravel Development Setup with Docker Compose

> Set up a Laravel development environment using Docker Compose.

# Laravel Development Setup with Docker Compose

   Table of contents

---

This guide demonstrates how to configure a **development** environment for a Laravel application using Docker and Docker Compose. It builds **on top of** the production image for PHP-FPM and then adds developer-focused features—like Xdebug—to streamline debugging. By basing the development container on a known production image, you keep both environments closely aligned.

This setup includes PHP-FPM, Nginx, and PostgreSQL services (although you can easily swap PostgreSQL for another database, like MySQL or MariaDB). Everything runs in containers, so you can develop in isolation without altering your host system.

> Note
>
> To experiment with a ready-to-run configuration, download the [Laravel Docker Examples](https://github.com/dockersamples/laravel-docker-examples) repository. It contains pre-configured setups for both development and production.

## Project structure

```plaintext
my-laravel-app/
├── app/
├── bootstrap/
├── config/
├── database/
├── public/
├── docker/
│   ├── common/
│   │   └── php-fpm/
│   │       └── Dockerfile
│   ├── development/
│   │   ├── php-fpm/
│   │   │   └── entrypoint.sh
│   │   ├── workspace/
│   │   │   └── Dockerfile
│   │   └── nginx
│   │       ├── Dockerfile
│   │       └── nginx.conf
│   └── production/
├── compose.dev.yaml
├── compose.prod.yaml
├── .dockerignore
├── .env
├── vendor/
├── ...
```

This layout represents a typical Laravel project, with Docker configurations stored in a unified `docker` directory. You’ll find **two** Compose files — `compose.dev.yaml` (for development) and `compose.prod.yaml` (for production) — to keep your environments separate and manageable.

The environment includes a `workspace` service, a sidecar container for tasks like building front-end assets, running Artisan commands, and other CLI tools your project may require. While this extra container may seem unusual, it’s a familiar pattern in solutions like **Laravel Sail** and **Laradock**. It also includes **Xdebug** to aid in debugging.

## Create a Dockerfile for PHP-FPM

This Dockerfile **extends** the production image by installing Xdebug and adjusting user permissions to ease local development. That way, your development environment stays consistent with production while still offering extra debug features and improved file mounting.

```dockerfile
# Builds a dev-only layer on top of the production image
FROM production AS development

# Use ARGs to define environment variables passed from the Docker build command or Docker Compose.
ARG XDEBUG_ENABLED=true
ARG XDEBUG_MODE=develop,coverage,debug,profile
ARG XDEBUG_HOST=host.docker.internal
ARG XDEBUG_IDE_KEY=DOCKER
ARG XDEBUG_LOG=/dev/stdout
ARG XDEBUG_LOG_LEVEL=0

USER root

# Configure Xdebug if enabled
RUN if [ "${XDEBUG_ENABLED}" = "true" ]; then \
    pecl install xdebug && \
    docker-php-ext-enable xdebug && \
    echo "xdebug.mode=${XDEBUG_MODE}" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini && \
    echo "xdebug.idekey=${XDEBUG_IDE_KEY}" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini && \
    echo "xdebug.log=${XDEBUG_LOG}" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini && \
    echo "xdebug.log_level=${XDEBUG_LOG_LEVEL}" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini && \
    echo "xdebug.client_host=${XDEBUG_HOST}" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini ; \
    echo "xdebug.start_with_request=yes" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini ; \
fi

# Add ARGs for syncing permissions
ARG UID=1000
ARG GID=1000

# Create a new user with the specified UID and GID, reusing an existing group if GID exists
RUN if getent group ${GID}; then \
      group_name=$(getent group ${GID} | cut -d: -f1); \
      useradd -m -u ${UID} -g ${GID} -s /bin/bash www; \
    else \
      groupadd -g ${GID} www && \
      useradd -m -u ${UID} -g www -s /bin/bash www; \
      group_name=www; \
    fi

# Dynamically update php-fpm to use the new user and group
RUN sed -i "s/user = www-data/user = www/g" /usr/local/etc/php-fpm.d/www.conf && \
    sed -i "s/group = www-data/group = $group_name/g" /usr/local/etc/php-fpm.d/www.conf

# Set the working directory
WORKDIR /var/www

# Copy the entrypoint script
COPY ./docker/development/php-fpm/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Switch back to the non-privileged user to run the application
USER www-data

# Change the default command to run the entrypoint script
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Expose port 9000 and start php-fpm server
EXPOSE 9000
CMD ["php-fpm"]
```

## Create a Dockerfile for Workspace

A workspace container provides a dedicated shell for asset compilation, Artisan/Composer commands, and other CLI tasks. This approach follows patterns from Laravel Sail and Laradock, consolidating all development tools into one container for convenience.

```dockerfile
# docker/development/workspace/Dockerfile
# Use the official PHP CLI image as the base
FROM php:8.4-cli

# Set environment variables for user and group ID
ARG UID=1000
ARG GID=1000
ARG NODE_VERSION=22.0.0

# Install system dependencies and build libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    unzip \
    libpq-dev \
    libonig-dev \
    libssl-dev \
    libxml2-dev \
    libcurl4-openssl-dev \
    libicu-dev \
    libzip-dev \
    && docker-php-ext-install -j$(nproc) \
    pdo_mysql \
    pdo_pgsql \
    pgsql \
    opcache \
    intl \
    zip \
    bcmath \
    soap \
    && pecl install redis xdebug \
    && docker-php-ext-enable redis xdebug\
    && curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer \
    && apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Use ARG to define environment variables passed from the Docker build command or Docker Compose.
ARG XDEBUG_ENABLED
ARG XDEBUG_MODE
ARG XDEBUG_HOST
ARG XDEBUG_IDE_KEY
ARG XDEBUG_LOG
ARG XDEBUG_LOG_LEVEL

# Configure Xdebug if enabled
RUN if [ "${XDEBUG_ENABLED}" = "true" ]; then \
    docker-php-ext-enable xdebug && \
    echo "xdebug.mode=${XDEBUG_MODE}" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini && \
    echo "xdebug.idekey=${XDEBUG_IDE_KEY}" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini && \
    echo "xdebug.log=${XDEBUG_LOG}" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini && \
    echo "xdebug.log_level=${XDEBUG_LOG_LEVEL}" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini && \
    echo "xdebug.client_host=${XDEBUG_HOST}" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini ; \
    echo "xdebug.start_with_request=yes" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini ; \
fi

# If the group already exists, use it; otherwise, create the 'www' group
RUN if getent group ${GID}; then \
      useradd -m -u ${UID} -g ${GID} -s /bin/bash www; \
    else \
      groupadd -g ${GID} www && \
      useradd -m -u ${UID} -g www -s /bin/bash www; \
    fi && \
    usermod -aG sudo www && \
    echo 'www ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# Switch to the non-root user to install NVM and Node.js
USER www

# Install NVM (Node Version Manager) as the www user
RUN export NVM_DIR="$HOME/.nvm" && \
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash && \
    [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh" && \
    nvm install ${NODE_VERSION} && \
    nvm alias default ${NODE_VERSION} && \
    nvm use default

# Ensure NVM is available for all future shells
RUN echo 'export NVM_DIR="$HOME/.nvm"' >> /home/www/.bashrc && \
    echo '[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"' >> /home/www/.bashrc && \
    echo '[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"' >> /home/www/.bashrc

# Set the working directory
WORKDIR /var/www

# Override the entrypoint to avoid the default php entrypoint
ENTRYPOINT []

# Default command to keep the container running
CMD ["bash"]
```

> Note
>
> If you prefer a **one-service-per-container** approach, simply omit the workspace container and run separate containers for each task. For example, you could use a dedicated `php-cli` container for your PHP scripts, and a `node` container to handle the asset building.

## Create a Docker Compose Configuration for development

Here's the `compose.yaml` file to set up the development environment:

```yaml
services:
  web:
    image: nginx:latest # Using the default Nginx image with custom configuration.
    volumes:
      # Mount the application code for live updates
      - ./:/var/www
      # Mount the Nginx configuration file
      - ./docker/development/nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    ports:
      # Map port 80 inside the container to the port specified by 'NGINX_PORT' on the host machine
      - "80:80"
    environment:
      - NGINX_HOST=localhost
    networks:
      - laravel-development
    depends_on:
      php-fpm:
        condition: service_started # Wait for php-fpm to start

  php-fpm:
    # For the php-fpm service, we will use our common PHP-FPM Dockerfile with the development target
    build:
      context: .
      dockerfile: ./docker/common/php-fpm/Dockerfile
      target: development
      args:
        UID: ${UID:-1000}
        GID: ${GID:-1000}
        XDEBUG_ENABLED: ${XDEBUG_ENABLED:-true}
        XDEBUG_MODE: develop,coverage,debug,profile
        XDEBUG_HOST: ${XDEBUG_HOST:-host.docker.internal}
        XDEBUG_IDE_KEY: ${XDEBUG_IDE_KEY:-DOCKER}
        XDEBUG_LOG: /dev/stdout
        XDEBUG_LOG_LEVEL: 0
    env_file:
      # Load the environment variables from the Laravel application
      - .env
    user: "${UID:-1000}:${GID:-1000}"
    volumes:
      # Mount the application code for live updates
      - ./:/var/www
    networks:
      - laravel-development
    depends_on:
      postgres:
        condition: service_started # Wait for postgres to start

  workspace:
    # For the workspace service, we will also create a custom image to install and setup all the necessary stuff.
    build:
      context: .
      dockerfile: ./docker/development/workspace/Dockerfile
      args:
        UID: ${UID:-1000}
        GID: ${GID:-1000}
        XDEBUG_ENABLED: ${XDEBUG_ENABLED:-true}
        XDEBUG_MODE: develop,coverage,debug,profile
        XDEBUG_HOST: ${XDEBUG_HOST:-host.docker.internal}
        XDEBUG_IDE_KEY: ${XDEBUG_IDE_KEY:-DOCKER}
        XDEBUG_LOG: /dev/stdout
        XDEBUG_LOG_LEVEL: 0
    tty: true # Enables an interactive terminal
    stdin_open: true # Keeps standard input open for 'docker exec'
    env_file:
      - .env
    volumes:
      - ./:/var/www
    networks:
      - laravel-development

  postgres:
    image: postgres:18
    ports:
      - "${POSTGRES_PORT:-5432}:5432"
    environment:
      - POSTGRES_DB=app
      - POSTGRES_USER=laravel
      - POSTGRES_PASSWORD=secret
    volumes:
      - postgres-data-development:/var/lib/postgresql
    networks:
      - laravel-development

  redis:
    image: redis:alpine
    networks:
      - laravel-development

networks:
  laravel-development:

volumes:
  postgres-data-development:
```

> Note
>
> Ensure you have an `.env` file at the root of your Laravel project with the necessary configurations. You can use the `.env.example` file as a template.

## Run your development environment

To start the development environment, use:

```console
$ docker compose -f compose.dev.yaml up --build -d
```

Run this command to build and start the development environment in detached mode. When the containers finish initializing, visit [http://localhost/](http://localhost/) to see your Laravel app in action.

## Summary

By building on top of the production image and adding debug tools like Xdebug, you create a Laravel development workflow that closely mirrors production. The optional workspace container simplifies tasks like asset building and running Artisan commands. If you prefer a separate container for every service (e.g., a dedicated `php-cli` and `node` container), you can skip the workspace approach. Either way, Docker Compose provides an efficient, consistent way to develop your Laravel project.

---

# Prerequisites for Setting Up Laravel with Docker Compose

> Ensure you have the required tools and knowledge before setting up Laravel with Docker Compose.

# Prerequisites for Setting Up Laravel with Docker Compose

   Table of contents

---

Before you begin setting up Laravel with Docker Compose, make sure you meet the following prerequisites:

## Docker and Docker Compose

You need Docker and Docker Compose installed on your system. Docker allows you to containerize applications, and Docker Compose helps you manage multi-container applications.

- Docker: Make sure Docker is installed and running on your machine. Refer to the
  [Docker installation guide](https://docs.docker.com/get-docker/) to install Docker.
- Docker Compose: Docker Compose is included with Docker Desktop, but you can also follow the
  [Docker Compose installation guide](https://docs.docker.com/compose/install/) if needed.

## Basic understanding of Docker and containers

A fundamental understanding of Docker and how containers work will be helpful. If you're new to Docker, consider reviewing the
[Docker Overview](https://docs.docker.com/get-started/overview/) to familiarize yourself with containerization concepts.

## Basic knowledge of Laravel

This guide assumes you have a basic understanding of Laravel and PHP. Familiarity with Laravel’s command-line tools, such as [Artisan](https://laravel.com/docs/12.x/artisan), and its project structure is important for following the instructions.

- Laravel CLI: You should be comfortable using Laravel’s command-line tool (`artisan`).
- Laravel Project Structure: Familiarize yourself with Laravel’s folder structure (`app`, `config`, `routes`, `tests`, etc.).
