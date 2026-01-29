# Configure CI/CD for your PHP application and more

# Configure CI/CD for your PHP application

> Learn how to Configure CI/CD for your PHP application

# Configure CI/CD for your PHP application

   Table of contents

---

## Prerequisites

Complete all the previous sections of this guide, starting with [Containerize a PHP application](https://docs.docker.com/guides/php/containerize/). You must have a [GitHub](https://github.com/signup) account and a verified [Docker](https://hub.docker.com/signup) account to complete this section.

## Overview

In this section, you'll learn how to set up and use GitHub Actions to build and test your Docker image as well as push it to Docker Hub. You will complete the following steps:

1. Create a new repository on GitHub.
2. Define the GitHub Actions workflow.
3. Run the workflow.

## Step one: Create the repository

Create a GitHub repository, configure the Docker Hub credentials, and push your source code.

1. [Create a new repository](https://github.com/new) on GitHub.
2. Open the repository **Settings**, and go to **Secrets and variables** >
  **Actions**.
3. Create a new **Repository variable** named `DOCKER_USERNAME` and your Docker ID as a value.
4. Create a new
  [Personal Access Token (PAT)](https://docs.docker.com/security/access-tokens/#create-an-access-token) for Docker Hub. You can name this token `docker-tutorial`. Make sure access permissions include Read and Write.
5. Add the PAT as a **Repository secret** in your GitHub repository, with the name
  `DOCKERHUB_TOKEN`.
6. In your local repository on your machine, run the following command to change
  the origin to the repository you just created. Make sure you change
  `your-username` to your GitHub username and `your-repository` to the name of
  the repository you created.
  ```console
  $ git remote set-url origin https://github.com/your-username/your-repository.git
  ```
7. In your local repository on your machine, run the following command to rename
  the branch to main.
  ```console
  $ git branch -M main
  ```
8. Run the following commands to stage, commit, and then push your local
  repository to GitHub.
  ```console
  $ git add -A
  $ git commit -m "my first commit"
  $ git push -u origin main
  ```

## Step two: Set up the workflow

Set up your GitHub Actions workflow for building, testing, and pushing the image
to Docker Hub.

1. Go to your repository on GitHub and then select the **Actions** tab.
2. Select **set up a workflow yourself**.
  This takes you to a page for creating a new GitHub actions workflow file in
  your repository, under `.github/workflows/main.yml` by default.
3. In the editor window, copy and paste the following YAML configuration.
  ```yaml
  name: ci
  on:
    push:
      branches:
        - main
  jobs:
    build:
      runs-on: ubuntu-latest
      steps:
        - name: Login to Docker Hub
          uses: docker/login-action@v3
          with:
            username: ${{ vars.DOCKER_USERNAME }}
            password: ${{ secrets.DOCKERHUB_TOKEN }}
        - name: Set up Docker Buildx
          uses: docker/setup-buildx-action@v3
        - name: Build and test
          uses: docker/build-push-action@v6
          with:
            target: test
            load: true
        - name: Build and push
          uses: docker/build-push-action@v6
          with:
            platforms: linux/amd64,linux/arm64
            push: true
            target: final
            tags: ${{ vars.DOCKER_USERNAME }}/${{ github.event.repository.name }}:latest
  ```
  For more information about the YAML syntax for `docker/build-push-action`,
  refer to the [GitHub Action README](https://github.com/docker/build-push-action/blob/master/README.md).

## Step three: Run the workflow

Save the workflow file and run the job.

1. Select **Commit changes...** and push the changes to the `main` branch.
  After pushing the commit, the workflow starts automatically.
2. Go to the **Actions** tab. It displays the workflow.
  Selecting the workflow shows you the breakdown of all the steps.
3. When the workflow is complete, go to your
  [repositories on Docker Hub](https://hub.docker.com/repositories).
  If you see the new repository in that list, it means the GitHub Actions
  successfully pushed the image to Docker Hub.

## Summary

In this section, you learned how to set up a GitHub Actions workflow for your application.

Related information:

- [Introduction to GitHub Actions](https://docs.docker.com/guides/gha/)
- [Docker Build GitHub Actions](https://docs.docker.com/build/ci/github-actions/)
- [Workflow syntax for GitHub Actions](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

## Next steps

Next, learn how you can locally test and debug your workloads on Kubernetes before deploying.

---

# Containerize a PHP application

> Learn how to containerize a PHP application.

# Containerize a PHP application

   Table of contents

---

## Prerequisites

- You have installed the latest version of
  [Docker
  Desktop](https://docs.docker.com/get-started/get-docker/).
- You have a [git client](https://git-scm.com/downloads). The examples in this
  section use a command-line based git client, but you can use any client.

## Overview

This section walks you through containerizing and running a PHP
application.

## Get the sample applications

In this guide, you will use a pre-built PHP application. The application uses Composer for library dependency management. You'll serve the application via an Apache web server.

Open a terminal, change directory to a directory that you want to work in, and
run the following command to clone the repository.

```console
$ git clone https://github.com/docker/docker-php-sample
```

The sample application is a basic hello world application and an application that increments a counter in a database. In addition, the application uses PHPUnit for testing.

## Initialize Docker assets

Now that you have an application, you can use `docker init` to create the
necessary Docker assets to containerize your application. Inside the
`docker-php-sample` directory, run the `docker init` command in a terminal.
`docker init` provides some default configuration, but you'll need to answer a
few questions about your application. For example, this application uses PHP
version 8.2. Refer to the following `docker init` example and use the same
answers for your prompts.

```console
$ docker init
Welcome to the Docker Init CLI!

This utility will walk you through creating the following files with sensible defaults for your project:
  - .dockerignore
  - Dockerfile
  - compose.yaml
  - README.Docker.md

Let's get started!

? What application platform does your project use? PHP with Apache
? What version of PHP do you want to use? 8.2
? What's the relative directory (with a leading .) for your app? ./src
? What local port do you want to use to access your server? 9000
```

You should now have the following contents in your `docker-php-sample`
directory.

```text
├── docker-php-sample/
│ ├── .git/
│ ├── src/
│ ├── tests/
│ ├── .dockerignore
│ ├── .gitignore
│ ├── compose.yaml
│ ├── composer.json
│ ├── composer.lock
│ ├── Dockerfile
│ ├── README.Docker.md
│ └── README.md
```

To learn more about the files that `docker init` added, see the following:

- [Dockerfile](https://docs.docker.com/reference/dockerfile/)
- [.dockerignore](https://docs.docker.com/reference/dockerfile/#dockerignore-file)
- [compose.yaml](https://docs.docker.com/reference/compose-file/)

## Run the application

Inside the `docker-php-sample` directory, run the following command in a
terminal.

```console
$ docker compose up --build
```

Open a browser and view the application at [http://localhost:9000/hello.php](http://localhost:9000/hello.php). You should see a simple hello world application.

In the terminal, press `ctrl`+`c` to stop the application.

### Run the application in the background

You can run the application detached from the terminal by adding the `-d`
option. Inside the `docker-php-sample` directory, run the following command
in a terminal.

```console
$ docker compose up --build -d
```

Open a browser and view the application at [http://localhost:9000/hello.php](http://localhost:9000/hello.php). You should see a simple hello world application.

In the terminal, run the following command to stop the application.

```console
$ docker compose down
```

For more information about Compose commands, see the
[Compose CLI
reference](https://docs.docker.com/reference/cli/docker/compose/).

## Summary

In this section, you learned how you can containerize and run a simple PHP
application using Docker.

Related information:

- [docker init reference](https://docs.docker.com/reference/cli/docker/init/)

## Next steps

In the next section, you'll learn how you can develop your application using
Docker containers.

---

# Test your PHP deployment

> Learn how to deploy your application

# Test your PHP deployment

   Table of contents

---

## Prerequisites

- Complete all the previous sections of this guide, starting with [Containerize
  a PHP application](https://docs.docker.com/guides/php/containerize/).
- [Turn on Kubernetes](https://docs.docker.com/desktop/use-desktop/kubernetes/#enable-kubernetes) in Docker
  Desktop.

## Overview

In this section, you'll learn how to use Docker Desktop to deploy your
application to a fully-featured Kubernetes environment on your development
machine. This allows you to test and debug your workloads on Kubernetes locally
before deploying.

## Create a Kubernetes YAML file

In your `docker-php-sample` directory, create a file named
`docker-php-kubernetes.yaml`. Open the file in an IDE or text editor and add
the following contents. Replace `DOCKER_USERNAME/REPO_NAME` with your Docker
username and the name of the repository that you created in [Configure CI/CD for
your PHP application](https://docs.docker.com/guides/php/configure-ci-cd/).

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: docker-php-demo
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      hello-php: web
  template:
    metadata:
      labels:
        hello-php: web
    spec:
      containers:
        - name: hello-site
          image: DOCKER_USERNAME/REPO_NAME
          imagePullPolicy: Always
---
apiVersion: v1
kind: Service
metadata:
  name: php-entrypoint
  namespace: default
spec:
  type: NodePort
  selector:
    hello-php: web
  ports:
    - port: 80
      targetPort: 80
      nodePort: 30001
```

In this Kubernetes YAML file, there are two objects, separated by the `---`:

- A Deployment, describing a scalable group of identical pods. In this case,
  you'll get just one replica, or copy of your pod. That pod, which is
  described under `template`, has just one container in it. The container is
  created from the image built by GitHub Actions in [Configure CI/CD for your
  PHP application](https://docs.docker.com/guides/php/configure-ci-cd/).
- A NodePort service, which will route traffic from port 30001 on your host to
  port 80 inside the pods it routes to, allowing you to reach your app
  from the network.

To learn more about Kubernetes objects, see the [Kubernetes documentation](https://kubernetes.io/docs/home/).

## Deploy and check your application

1. In a terminal, navigate to the `docker-php-sample` directory
  and deploy your application to Kubernetes.
  ```console
  $ kubectl apply -f docker-php-kubernetes.yaml
  ```
  You should see output that looks like the following, indicating your Kubernetes objects were created successfully.
  ```text
  deployment.apps/docker-php-demo created
  service/php-entrypoint created
  ```
2. Make sure everything worked by listing your deployments.
  ```console
  $ kubectl get deployments
  ```
  Your deployment should be listed as follows:
  ```text
  NAME                 READY   UP-TO-DATE   AVAILABLE   AGE
  docker-php-demo      1/1     1            1           6s
  ```
  This indicates all of the pods are up and running. Do the same check for your services.
  ```console
  $ kubectl get services
  ```
  You should get output like the following.
  ```text
  NAME              TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
  kubernetes        ClusterIP   10.96.0.1        <none>        443/TCP          7d22h
  php-entrypoint    NodePort    10.111.101.229   <none>        80:30001/TCP     33s
  ```
  In addition to the default `kubernetes` service, you can see your `php-entrypoint` service. The `php-entrypoint` service is accepting traffic on port 30001/TCP.
3. Open a browser and visit your app at
  [http://localhost:30001/hello.php](http://localhost:30001/hello.php). You
  should see your application.
4. Run the following command to tear down your application.
  ```console
  $ kubectl delete -f docker-php-kubernetes.yaml
  ```

## Summary

In this section, you learned how to use Docker Desktop to deploy your application to a fully-featured Kubernetes environment on your development machine.

Related information:

- [Kubernetes documentation](https://kubernetes.io/docs/home/)
- [Deploy on Kubernetes with Docker Desktop](https://docs.docker.com/desktop/use-desktop/kubernetes/)
- [Swarm mode overview](https://docs.docker.com/engine/swarm/)

---

# Use containers for PHP development

> Learn how to develop your PHP application locally using containers.

# Use containers for PHP development

   Table of contents

---

## Prerequisites

Complete [Containerize a PHP application](https://docs.docker.com/guides/php/containerize/).

## Overview

In this section, you'll learn how to set up a development environment for your containerized application. This includes:

- Adding a local database and persisting data
- Adding phpMyAdmin to interact with the database
- Configuring Compose to automatically update your running Compose services as
  you edit and save your code
- Creating a development container that contains the dev dependencies

## Add a local database and persist data

You can use containers to set up local services, like a database.
To do this for the sample application, you'll need to do the following:

- Update the `Dockerfile` to install extensions to connect to the database
- Update the `compose.yaml` file to add a database service and volume to persist data

### Update the Dockerfile to install extensions

To install PHP extensions, you need to update the `Dockerfile`. Open your
Dockerfile in an IDE or text editor and then update the contents. The following
`Dockerfile` includes one new line that installs the `pdo` and `pdo_mysql`
extensions. All comments have been removed.

```dockerfile
# syntax=docker/dockerfile:1

FROM composer:lts as deps
WORKDIR /app
RUN --mount=type=bind,source=composer.json,target=composer.json \
    --mount=type=bind,source=composer.lock,target=composer.lock \
    --mount=type=cache,target=/tmp/cache \
    composer install --no-dev --no-interaction

FROM php:8.2-apache as final
RUN docker-php-ext-install pdo pdo_mysql
RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"
COPY --from=deps app/vendor/ /var/www/html/vendor
COPY ./src /var/www/html
USER www-data
```

For more details about installing PHP extensions, see the [Official Docker Image for PHP](https://hub.docker.com/_/php).

### Update the compose.yaml file to add a db and persist data

Open the `compose.yaml` file in an IDE or text editor. You'll notice it
already contains commented-out instructions for a PostgreSQL database and volume. For this application, you'll use MariaDB. For more details about MariaDB, see the [MariaDB Official Docker image](https://hub.docker.com/_/mariadb).

Open the `src/database.php` file in an IDE or text editor. You'll notice that it reads environment variables in order to connect to the database.

In the `compose.yaml` file, you'll need to update the following:

1. Uncomment and update the database instructions for MariaDB.
2. Add a secret to the server service to pass in the database password.
3. Add the database connection environment variables to the server service.
4. Uncomment the volume instructions to persist data.

The following is the updated `compose.yaml` file. All comments have been removed.

```yaml
services:
  server:
    build:
      context: .
    ports:
      - 9000:80
    depends_on:
      db:
        condition: service_healthy
    secrets:
      - db-password
    environment:
      - PASSWORD_FILE_PATH=/run/secrets/db-password
      - DB_HOST=db
      - DB_NAME=example
      - DB_USER=root
  db:
    image: mariadb
    restart: always
    user: root
    secrets:
      - db-password
    volumes:
      - db-data:/var/lib/mysql
    environment:
      - MARIADB_ROOT_PASSWORD_FILE=/run/secrets/db-password
      - MARIADB_DATABASE=example
    expose:
      - 3306
    healthcheck:
      test:
        [
          "CMD",
          "/usr/local/bin/healthcheck.sh",
          "--su-mysql",
          "--connect",
          "--innodb_initialized",
        ]
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

In the `docker-php-sample` directory, create a new directory named `db` and
inside that directory create a file named `password.txt`. Open `password.txt` in an IDE or text editor and add the following password. The password must be on a single line, with no additional lines in the file.

```text
example
```

Save and close the `password.txt` file.

You should now have the following in your `docker-php-sample` directory.

```text
├── docker-php-sample/
│ ├── .git/
│ ├── db/
│ │ └── password.txt
│ ├── src/
│ ├── tests/
│ ├── .dockerignore
│ ├── .gitignore
│ ├── compose.yaml
│ ├── composer.json
│ ├── composer.lock
│ ├── Dockerfile
│ ├── README.Docker.md
│ └── README.md
```

Run the following command to start your application.

```console
$ docker compose up --build
```

Open a browser and view the application at [http://localhost:9000/database.php](http://localhost:9000/database.php). You should see a simple web application with text and a counter that increments every time you refresh.

Press `ctrl+c` in the terminal to stop your application.

## Verify that data persists in the database

In the terminal, run `docker compose rm` to remove your containers and then run `docker compose up` to run your application again.

```console
$ docker compose rm
$ docker compose up --build
```

Refresh [http://localhost:9000/database.php](http://localhost:9000/database.php) in your browser and verify that the previous count still exists. Without a volume, the database data wouldn't persist after you remove the container.

Press `ctrl+c` in the terminal to stop your application.

## Add phpMyAdmin to interact with the database

You can easily add services to your application stack by updating the `compose.yaml` file.

Update your `compose.yaml` to add a new service for phpMyAdmin. For more details, see the [phpMyAdmin Official Docker Image](https://hub.docker.com/_/phpmyadmin). The following is the updated `compose.yaml` file.

```yaml
services:
  server:
    build:
      context: .
    ports:
      - 9000:80
    depends_on:
      db:
        condition: service_healthy
    secrets:
      - db-password
    environment:
      - PASSWORD_FILE_PATH=/run/secrets/db-password
      - DB_HOST=db
      - DB_NAME=example
      - DB_USER=root
  db:
    image: mariadb
    restart: always
    user: root
    secrets:
      - db-password
    volumes:
      - db-data:/var/lib/mysql
    environment:
      - MARIADB_ROOT_PASSWORD_FILE=/run/secrets/db-password
      - MARIADB_DATABASE=example
    expose:
      - 3306
    healthcheck:
      test:
        [
          "CMD",
          "/usr/local/bin/healthcheck.sh",
          "--su-mysql",
          "--connect",
          "--innodb_initialized",
        ]
      interval: 10s
      timeout: 5s
      retries: 5
  phpmyadmin:
    image: phpmyadmin
    ports:
      - 8080:80
    depends_on:
      - db
    environment:
      - PMA_HOST=db
volumes:
  db-data:
secrets:
  db-password:
    file: db/password.txt
```

In the terminal, run `docker compose up` to run your application again.

```console
$ docker compose up --build
```

Open [http://localhost:8080](http://localhost:8080) in your browser to access phpMyAdmin. Log in using `root` as the username and `example` as the password. You can now interact with the database through phpMyAdmin.

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
    ports:
      - 9000:80
    depends_on:
      db:
        condition: service_healthy
    secrets:
      - db-password
    environment:
      - PASSWORD_FILE_PATH=/run/secrets/db-password
      - DB_HOST=db
      - DB_NAME=example
      - DB_USER=root
    develop:
      watch:
        - action: sync
          path: ./src
          target: /var/www/html
  db:
    image: mariadb
    restart: always
    user: root
    secrets:
      - db-password
    volumes:
      - db-data:/var/lib/mysql
    environment:
      - MARIADB_ROOT_PASSWORD_FILE=/run/secrets/db-password
      - MARIADB_DATABASE=example
    expose:
      - 3306
    healthcheck:
      test:
        [
          "CMD",
          "/usr/local/bin/healthcheck.sh",
          "--su-mysql",
          "--connect",
          "--innodb_initialized",
        ]
      interval: 10s
      timeout: 5s
      retries: 5
  phpmyadmin:
    image: phpmyadmin
    ports:
      - 8080:80
    depends_on:
      - db
    environment:
      - PMA_HOST=db
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

Open a browser and verify that the application is running at [http://localhost:9000/hello.php](http://localhost:9000/hello.php).

Any changes to the application's source files on your local machine will now be
immediately reflected in the running container.

Open `hello.php` in an IDE or text editor and update the string `Hello, world!` to `Hello, Docker!`.

Save the changes to `hello.php` and then wait a few seconds for the application to sync. Refresh [http://localhost:9000/hello.php](http://localhost:9000/hello.php) in your browser and verify that the updated text appears.

Press `ctrl+c` in the terminal to stop Compose Watch. Run `docker compose down` in the terminal to stop the application.

## Create a development container

At this point, when you run your containerized application, Composer isn't installing the dev dependencies. While this small image is good for production, it lacks the tools and dependencies you may need when developing and it doesn't include the `tests` directory. You can use multi-stage builds to build stages for both development and production in the same Dockerfile. For more details, see
[Multi-stage builds](https://docs.docker.com/build/building/multi-stage/).

In the `Dockerfile`, you'll need to update the following:

1. Split the `deps` staged into two stages. One stage for production
  (`prod-deps`) and one stage (`dev-deps`) to install development dependencies.
2. Create a common `base` stage.
3. Create a new `development` stage for development.
4. Update the `final` stage to copy dependencies from the new `prod-deps` stage.

The following is the `Dockerfile` before and after the changes.

```dockerfile
# syntax=docker/dockerfile:1

FROM composer:lts as deps
WORKDIR /app
RUN --mount=type=bind,source=composer.json,target=composer.json \
    --mount=type=bind,source=composer.lock,target=composer.lock \
    --mount=type=cache,target=/tmp/cache \
    composer install --no-dev --no-interaction

FROM php:8.2-apache as final
RUN docker-php-ext-install pdo pdo_mysql
RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"
COPY --from=deps app/vendor/ /var/www/html/vendor
COPY ./src /var/www/html
USER www-data
```

```dockerfile
# syntax=docker/dockerfile:1

FROM composer:lts as prod-deps
WORKDIR /app
RUN --mount=type=bind,source=./composer.json,target=composer.json \
    --mount=type=bind,source=./composer.lock,target=composer.lock \
    --mount=type=cache,target=/tmp/cache \
    composer install --no-dev --no-interaction

FROM composer:lts as dev-deps
WORKDIR /app
RUN --mount=type=bind,source=./composer.json,target=composer.json \
    --mount=type=bind,source=./composer.lock,target=composer.lock \
    --mount=type=cache,target=/tmp/cache \
    composer install --no-interaction

FROM php:8.2-apache as base
RUN docker-php-ext-install pdo pdo_mysql
COPY ./src /var/www/html

FROM base as development
COPY ./tests /var/www/html/tests
RUN mv "$PHP_INI_DIR/php.ini-development" "$PHP_INI_DIR/php.ini"
COPY --from=dev-deps app/vendor/ /var/www/html/vendor

FROM base as final
RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"
COPY --from=prod-deps app/vendor/ /var/www/html/vendor
USER www-data
```

Update your `compose.yaml` file by adding an instruction to target the
development stage.

The following is the updated section of the `compose.yaml` file.

```yaml
services:
  server:
    build:
      context: .
      target: development
      # ...
```

Your containerized application will now install the dev dependencies.

Run the following command to start your application.

```console
$ docker compose up --build
```

Open a browser and view the application at [http://localhost:9000/hello.php](http://localhost:9000/hello.php). You should still see the simple "Hello, Docker!" application.

Press `ctrl+c` in the terminal to stop your application.

While the application appears the same, you can now make use of the dev dependencies. Continue to the next section to learn how you can run tests using Docker.

## Summary

In this section, you took a look at setting up your Compose file to add a local
database and persist data. You also learned how to use Compose Watch to automatically sync your application when you update your code. And finally, you learned how to create a development container that contains the dependencies needed for development.

Related information:

- [Compose file reference](https://docs.docker.com/reference/compose-file/)
- [Compose file watch](https://docs.docker.com/compose/how-tos/file-watch/)
- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
- [Official Docker Image for PHP](https://hub.docker.com/_/php)

## Next steps

In the next section, you'll learn how to run unit tests using Docker.

---

# Run PHP tests in a container

> Learn how to run your PHP tests in a container.

# Run PHP tests in a container

   Table of contents

---

## Prerequisites

Complete all the previous sections of this guide, starting with [Containerize a PHP application](https://docs.docker.com/guides/php/containerize/).

## Overview

Testing is an essential part of modern software development. Testing can mean a
lot of things to different development teams. There are unit tests, integration
tests and end-to-end testing. In this guide you take a look at running your unit
tests in Docker when developing and when building.

## Run tests when developing locally

The sample application already has a PHPUnit test inside the `tests` directory. When developing locally, you can use Compose to run your tests.

Run the following command in the `docker-php-sample` directory to run the tests inside a container.

```console
$ docker compose run --build --rm server ./vendor/bin/phpunit tests/HelloWorldTest.php
```

You should see output that contains the following.

```console
Hello, Docker!PHPUnit 9.6.13 by Sebastian Bergmann and contributors.

.                                                                   1 / 1 (100%)

Time: 00:00.003, Memory: 4.00 MB

OK (1 test, 1 assertion)
```

To learn more about the command, see
[docker compose run](https://docs.docker.com/reference/cli/docker/compose/run/).

## Run tests when building

To run your tests when building, you need to update your Dockerfile. Create a new test stage that runs the tests.

The following is the updated Dockerfile.

```dockerfile
# syntax=docker/dockerfile:1

FROM composer:lts as prod-deps
WORKDIR /app
RUN --mount=type=bind,source=./composer.json,target=composer.json \
    --mount=type=bind,source=./composer.lock,target=composer.lock \
    --mount=type=cache,target=/tmp/cache \
    composer install --no-dev --no-interaction

FROM composer:lts as dev-deps
WORKDIR /app
RUN --mount=type=bind,source=./composer.json,target=composer.json \
    --mount=type=bind,source=./composer.lock,target=composer.lock \
    --mount=type=cache,target=/tmp/cache \
    composer install --no-interaction

FROM php:8.2-apache as base
RUN docker-php-ext-install pdo pdo_mysql
COPY ./src /var/www/html

FROM base as development
COPY ./tests /var/www/html/tests
RUN mv "$PHP_INI_DIR/php.ini-development" "$PHP_INI_DIR/php.ini"
COPY --from=dev-deps app/vendor/ /var/www/html/vendor

FROM development as test
WORKDIR /var/www/html
RUN ./vendor/bin/phpunit tests/HelloWorldTest.php

FROM base as final
RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"
COPY --from=prod-deps app/vendor/ /var/www/html/vendor
USER www-data
```

Run the following command to build an image using the test stage as the target and view the test results. Include `--progress plain` to view the build output, `--no-cache` to ensure the tests always run, and `--target test` to target the test stage.

```console
$ docker build -t php-docker-image-test --progress plain --no-cache --target test .
```

You should see output containing the following.

```console
#18 [test 2/2] RUN ./vendor/bin/phpunit tests/HelloWorldTest.php
#18 0.385 Hello, Docker!PHPUnit 9.6.13 by Sebastian Bergmann and contributors.
#18 0.392
#18 0.394 .                                                                   1 / 1 (100%)
#18 0.395
#18 0.395 Time: 00:00.003, Memory: 4.00 MB
#18 0.395
#18 0.395 OK (1 test, 1 assertion)
```

## Summary

In this section, you learned how to run tests when developing locally using Compose and how to run tests when building your image.

Related information:

- [docker compose run](https://docs.docker.com/reference/cli/docker/compose/run/)

## Next steps

Next, you’ll learn how to set up a CI/CD pipeline using GitHub Actions.

---

# PHP language

> Containerize and develop PHP apps using Docker

# PHP language-specific guide

---

The PHP language-specific guide teaches you how to create a containerized PHP application using Docker. In this guide, you'll learn how to:

- Containerize and run a PHP application
- Set up a local environment to develop a PHP application using containers
- Run tests for a PHP application within containers
- Configure a CI/CD pipeline for a containerized PHP application using GitHub Actions
- Deploy your containerized application locally to Kubernetes to test and debug your deployment

After completing the PHP language-specific guide, you should be able to containerize your own PHP application based on the examples and instructions provided in this guide.

Start by containerizing an existing PHP application.

## Modules

1. [Containerize your app](https://docs.docker.com/guides/php/containerize/)
  Learn how to containerize a PHP application.
2. [Develop your app](https://docs.docker.com/guides/php/develop/)
  Learn how to develop your PHP application locally using containers.
3. [Run your tests](https://docs.docker.com/guides/php/run-tests/)
  Learn how to run your PHP tests in a container.
4. [Configure CI/CD](https://docs.docker.com/guides/php/configure-ci-cd/)
  Learn how to Configure CI/CD for your PHP application
5. [Test your deployment](https://docs.docker.com/guides/php/deploy/)
  Learn how to deploy your application

---

# Pre

> Pre-seeding database with schema and data at startup for development environment

# Pre-seeding database with schema and data at startup for development environment

   Table of contents

---

Pre-seeding databases with essential data and schema during local development is a common practice to enhance the development and testing workflow. By simulating real-world scenarios, this practice helps catch frontend issues early, ensures alignment between Database Administrators and Software Engineers, and facilitates smoother collaboration. Pre-seeding offers benefits like confident deployments, consistency across environments, and early issue detection, ultimately improving the overall development process.

In this guide, you will learn how to:

- Use Docker to launch up a Postgres container
- Pre-seed Postgres using a SQL script
- Pre-seed Postgres by copying SQL files into Docker image
- Pre-seed Postgres using JavaScript code

## Using Postgres with Docker

The [official Docker image for Postgres](https://hub.docker.com/_/postgres) provides a convenient way to run Postgres database on your development machine. A Postgres Docker image is a pre-configured environment that encapsulates the PostgreSQL database system. It's a self-contained unit, ready to run in a Docker container. By using this image, you can quickly and easily set up a Postgres instance without the need for manual configuration.

## Prerequisites

The following prerequisites are required to follow along with this how-to guide:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

## Launching Postgres

Launch a quick demo of Postgres by using the following steps:

1. Open the terminal and run the following command to start a Postgres container.
  This example will launch a Postgres container, expose port `5432` onto the host to let a native-running application to connect to it with the password `mysecretpassword`.
  ```console
  $ docker run -d --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword postgres
  ```
2. Verify that Postgres is up and running by selecting the container and checking the logs on Docker Dashboard.
  ```plaintext
  PostgreSQL Database directory appears to contain a database; Skipping initialization
  2024-09-08 09:09:47.136 UTC [1] LOG:  starting PostgreSQL 16.4 (Debian 16.4-1.pgdg120+1) on aarch64-unknown-linux-gnu, compiled by gcc (Debian 12.2.0-14) 12.2.0, 64-bit
  2024-09-08 09:09:47.137 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
  2024-09-08 09:09:47.137 UTC [1] LOG:  listening on IPv6 address "::", port 5432
  2024-09-08 09:09:47.139 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
  2024-09-08 09:09:47.142 UTC [29] LOG:  database system was shut down at 2024-09-08 09:07:09 UTC
  2024-09-08 09:09:47.148 UTC [1] LOG:  database system is ready to accept connections
  ```
3. Connect to Postgres from the local system.
  The `psql` is the PostgreSQL interactive shell that is used to connect to a Postgres database and let you start executing SQL commands. Assuming that you already have `psql` utility installed on your local system, it's time to connect to the Postgres database. Run the following command on your local terminal:
  ```console
  $ docker exec -it postgres psql -h localhost -U postgres
  ```
  You can now execute any SQL queries or commands you need within the `psql` prompt.
  Use `\q` or `\quit` to exit from the Postgres interactive shell.

## Pre-seed the Postgres database using a SQL script

Now that you've familiarized yourself with Postgres, it's time to see how to pre-seed it with sample data. In this demonstration, you'll first create a script that holds SQL commands. The script defines the database, and table structure and inserts sample data. Then you will connect the database to verify the data.

Assuming that you have an existing Postgres database instance up and running, follow these steps to seed the database.

1. Create an empty file named `seed.sql` and add the following content.
  ```sql
  CREATE DATABASE sampledb;
  \c sampledb
  CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(100) UNIQUE
  );
  INSERT INTO users (name, email) VALUES
    ('Alpha', 'alpha@example.com'),
    ('Beta', 'beta@example.com'),
    ('Gamma', 'gamma@example.com');
  ```
  The SQL script creates a new database called `sampledb`, connects to it, and creates a `users` table. The table includes an auto-incrementing `id` as the primary key, a `name` field with a maximum length of 50 characters, and a unique `email` field with up to 100 characters.
  After creating the table, the `INSERT` command inserts three users into the `users` table with their respective names and emails. This setup forms a basic database structure to store user information with unique email addresses.
2. Seed the database.
  It’s time to feed the content of the `seed.sql` directly into the database by using the `<` operator. The command is used to execute a SQL script named `seed.sql` against a Postgres database named `sampledb`.
  ```console
  $ cat seed.sql | docker exec -i postgres psql -h localhost -U postgres -f-
  ```
  Once the query is executed, you will see the following results:
  ```plaintext
  CREATE DATABASE
  You are now connected to database "sampledb" as user "postgres".
  CREATE TABLE
  INSERT 0 3
  ```
3. Run the following `psql` command to verify if the table named users is populated in the database `sampledb` or not.
  ```console
  $ docker exec -it postgres psql -h localhost -U postgres sampledb
  ```
  You can now run `\l` in the `psql` shell to list all the databases on the Postgres server.
  ```console
  sampledb=# \l
                                               List of databases
  Name    |  Owner   | Encoding |  Collate   |   Ctype    | ICU Locale | Locale Provider |   Access privileges
  -----------+----------+----------+------------+------------+------------+-----------------+-----------------------
  postgres  | postgres | UTF8     | en_US.utf8 | en_US.utf8 |            | libc            |
  sampledb  | postgres | UTF8     | en_US.utf8 | en_US.utf8 |            | libc            |
  template0 | postgres | UTF8     | en_US.utf8 | en_US.utf8 |            | libc            | =c/postgres          +
            |          |          |            |            |            |                 | postgres=CTc/postgres
  template1 | postgres | UTF8     | en_US.utf8 | en_US.utf8 |            | libc            | =c/postgres          +
            |          |          |            |            |            |                 | postgres=CTc/postgres
  (4 rows)
  ```
  To retrieve all the data from the users table, enter the following query:
  ```console
  sampledb=# SELECT * FROM users;
  id | name  |       email
  ----+-------+-------------------
   1 | Alpha | alpha@example.com
   2 | Beta  | beta@example.com
   3 | Gamma | gamma@example.com
  (3 rows)
  ```
  Use `\q` or `\quit` to exit from the Postgres interactive shell.

## Pre-seed the database by bind-mounting a SQL script

In Docker, mounting refers to making files or directories from the host system accessible within a container. This let you to share data or configuration files between the host and the container, enabling greater flexibility and persistence.

Now that you have learned how to launch Postgres and pre-seed the database using an SQL script, it’s time to learn how to mount an SQL file directly into the Postgres containers’ initialization directory (`/docker-entrypoint-initdb.d`). The `/docker-entrypoint-initdb.d` is a special directory in PostgreSQL Docker containers that is used for initializing the database when the container is first started

Make sure you stop any running Postgres containers (along with volumes) to prevent port conflicts before you follow the steps:

```console
$ docker container stop postgres
```

1. Modify the `seed.sql` with the following entries:
  ```sql
  CREATE TABLE IF NOT EXISTS users (
   id SERIAL PRIMARY KEY,
   name VARCHAR(50),
   email VARCHAR(100) UNIQUE
  );
  INSERT INTO users (name, email) VALUES
   ('Alpha', 'alpha@example.com'),
   ('Beta', 'beta@example.com'),
   ('Gamma', 'gamma@example.com')
  ON CONFLICT (email) DO NOTHING;
  ```
2. Create a text file named `Dockerfile` and copy the following content.
  ```plaintext
  # syntax=docker/dockerfile:1
  FROM postgres:18
  COPY seed.sql /docker-entrypoint-initdb.d/
  ```
  This Dockerfile copies the `seed.sql` script directly into the PostgreSQL container's initialization directory.
3. Use Docker Compose.
  Using Docker Compose makes it even easier to manage and deploy the PostgreSQL container with the seeded database. This compose.yml file defines a Postgres service named `db` using the latest Postgres image, which sets up a database with the name `sampledb`, along with a user `postgres` and a password `mysecretpassword`.
  ```yaml
  services:
    db:
      build:
        context: .
        dockerfile: Dockerfile
      container_name: my_postgres_db
      environment:
        POSTGRES_USER: postgres
        POSTGRES_PASSWORD: mysecretpassword
        POSTGRES_DB: sampledb
      ports:
        - "5432:5432"
      volumes:
        - data_sql:/var/lib/postgresql   # Persistent data storage
  volumes:
    data_sql:
  ```
  It maps port `5432` on the host to the container's `5432`, let you access to the Postgres database from outside the container. It also define `data_sql` for persisting the database data, ensuring that data is not lost when the container is stopped.
  It is important to note that the port mapping to the host is only necessary if you want to connect to the database from non-containerized programs. If you containerize the service that connects to the DB, you should connect to the database over a custom bridge network.
4. Bring up the Compose service.
  Assuming that you've placed the `seed.sql` file in the same directory as the Dockerfile, execute the following command:
  ```console
  $ docker compose up -d --build
  ```
5. It’s time to verify if the table `users` get populated with the data.
  ```console
  $ docker exec -it my_postgres_db psql -h localhost -U postgres sampledb
  ```
  ```sql
  sampledb=# SELECT * FROM users;
    id | name  |       email
  ----+-------+-------------------
     1 | Alpha | alpha@example.com
     2 | Beta  | beta@example.com
     3 | Gamma | gamma@example.com
   (3 rows)
  sampledb=#
  ```

## Pre-seed the database using JavaScript code

Now that you have learned how to seed the database using various methods like SQL script, mounting volumes etc., it's time to try to achieve it using JavaScript code.

1. Create a .env file with the following:
  ```plaintext
  POSTGRES_USER=postgres
  POSTGRES_DB_HOST=localhost
  POSTGRES_DB=sampledb
  POSTGRES_PASSWORD=mysecretpassword
  POSTGRES_PORT=5432
  ```
2. Create a new JavaScript file called seed.js with the following content:
  The following JavaScript code imports the `dotenv` package which is used to load environment variables from an `.env` file. The `.config()` method reads the `.env` file and sets the environment variables as properties of the `process.env` object. This let you to securely store sensitive information like database credentials outside of your code.
  Then, it creates a new Pool instance from the pg library, which provides a connection pool for efficient database interactions. The `seedData` function is defined to perform the database seeding operations.
  It is called at the end of the script to initiate the seeding process. The try...catch...finally block is used for error handling.
  ```plaintext
  require('dotenv').config();  // Load environment variables from .env file
  const { Pool } = require('pg');
  // Create a new pool using environment variables
  const pool = new Pool({
    user: process.env.POSTGRES_USER,
    host: process.env.POSTGRES_DB_HOST,
    database: process.env.POSTGRES_DB,
    port: process.env.POSTGRES_PORT,
    password: process.env.POSTGRES_PASSWORD,
  });
  const seedData = async () => {
    try {
       // Drop the table if it already exists (optional)
       await pool.query(`DROP TABLE IF EXISTS todos;`);
       // Create the table with the correct structure
       await pool.query(`
         CREATE TABLE todos (
           id SERIAL PRIMARY KEY,
           task VARCHAR(255) NOT NULL,
           completed BOOLEAN DEFAULT false
             );
       `   );
       // Insert seed data
       await pool.query(`
         INSERT INTO todos (task, completed) VALUES
         ('Watch netflix', false),
         ('Finish podcast', false),
         ('Pick up kid', false);
         `);
         console.log('Database seeded successfully!');
       } catch (err) {
         console.error('Error seeding the database', err);
       } finally {
         pool.end();
      }
    };
    // Call the seedData function to run the script
    seedData();
  ```
3. Kick off the seeding process
  ```console
  $ node seed.js
  ```
  You should see the following command:
  ```plaintext
  Database seeded successfully!
  ```
4. Verify if the database is seeded correctly:
  ```console
  $ docker exec -it postgres psql -h localhost -U postgres sampledb
  ```
  ```console
  sampledb=# SELECT * FROM todos;
  id |      task      | completed
  ----+----------------+-----------
  1 | Watch netflix  | f
  2 | Finish podcast | f
  3 | Pick up kid    | f
  (3 rows)
  ```

## Recap

Pre-seeding a database with schema and data at startup is essential for creating a consistent and realistic testing environment, which helps in identifying issues early in development and aligning frontend and backend work. This guide has equipped you with the knowledge and practical steps to achieve pre-seeding using various methods, including SQL script, Docker integration, and JavaScript code.
