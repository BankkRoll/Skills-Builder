# Run your Go image as a container and more

# Run your Go image as a container

> Learn how to run the image as a container.

# Run your Go image as a container

   Table of contents

---

## Prerequisites

Work through the steps to containerize a Go application in [Build your Go image](https://docs.docker.com/guides/golang/build-images/).

## Overview

In the previous module you created a `Dockerfile` for your example application and then you created your Docker image using the command `docker build`. Now that you have the image, you can run that image and see if your application is running correctly.

A container is a normal operating system process except that this process is isolated and has its own file system, its own networking, and its own isolated process tree separate from the host.

To run an image inside of a container, you use the `docker run` command. It requires one parameter and that's the image name. Start your image and make sure it's running correctly. Run the following command in your terminal.

```console
$ docker run docker-gs-ping
```

```text
____    __
  / __/___/ /  ___
 / _// __/ _ \/ _ \
/___/\__/_//_/\___/ v4.10.2
High performance, minimalist Go web framework
https://echo.labstack.com
____________________________________O/_______
                                    O\
⇨ http server started on [::]:8080
```

When you run this command, you’ll notice that you weren't returned to the command prompt. This is because your application is a REST server and will run in a loop waiting for incoming requests without returning control back to the OS until you stop the container.

Make a GET request to the server using the curl command.

```console
$ curl http://localhost:8080/
curl: (7) Failed to connect to localhost port 8080: Connection refused
```

Your curl command failed because the connection to your server was refused.
Meaning that you weren't able to connect to localhost on port 8080. This is
expected because your container is running in isolation which includes
networking. Stop the container and restart with port 8080 published on your
local network.

To stop the container, press ctrl-c. This will return you to the terminal prompt.

To publish a port for your container, you’ll use the `--publish` flag (`-p` for short) on the `docker run` command. The format of the `--publish` command is `[host_port]:[container_port]`. So if you wanted to expose port `8080` inside the container to port `3000` outside the container, you would pass `3000:8080` to the `--publish` flag.

Start the container and expose port `8080` to port `8080` on the host.

```console
$ docker run --publish 8080:8080 docker-gs-ping
```

Now, rerun the curl command.

```console
$ curl http://localhost:8080/
Hello, Docker! <3
```

Success! You were able to connect to the application running inside of your container on port 8080. Switch back to the terminal where your container is running and you should see the `GET` request logged to the console.

Press `ctrl-c` to stop the container.

## Run in detached mode

This is great so far, but your sample application is a web server and you
shouldn't have to have your terminal connected to the container. Docker can run
your container in detached mode in the background. To do this, you can use the
`--detach` or `-d` for short. Docker will start your container the same as
before but this time will detach from the container and return you to the
terminal prompt.

```console
$ docker run -d -p 8080:8080 docker-gs-ping
d75e61fcad1e0c0eca69a3f767be6ba28a66625ce4dc42201a8a323e8313c14e
```

Docker started your container in the background and printed the container ID on the terminal.

Again, make sure that your container is running. Run the same `curl` command:

```console
$ curl http://localhost:8080/
Hello, Docker! <3
```

## List containers

Since you ran your container in the background, how do you know if your container is running or what other containers are running on your machine? Well, to see a list of containers running on your machine, run `docker ps`. This is similar to how the ps command is used to see a list of processes on a Linux machine.

```console
$ docker ps

CONTAINER ID   IMAGE            COMMAND             CREATED          STATUS          PORTS                    NAMES
d75e61fcad1e   docker-gs-ping   "/docker-gs-ping"   41 seconds ago   Up 40 seconds   0.0.0.0:8080->8080/tcp   inspiring_ishizaka
```

The `ps` command tells you a bunch of stuff about your running containers. You can see the container ID, the image running inside the container, the command that was used to start the container, when it was created, the status, ports that are exposed, and the names of the container.

You are probably wondering where the name of your container is coming from. Since you didn’t provide a name for the container when you started it, Docker generated a random name. You'll fix this in a minute but first you need to stop the container. To stop the container, run the `docker stop` command, passing the container's name or ID.

```console
$ docker stop inspiring_ishizaka
inspiring_ishizaka
```

Now rerun the `docker ps` command to see a list of running containers.

```console
$ docker ps

CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

## Stop, start, and name containers

Docker containers can be started, stopped and restarted. When you stop a container, it's not removed but the status is changed to stopped and the process inside of the container is stopped. When you ran the `docker ps` command, the default output is to only show running containers. If you pass the `--all` or `-a` for short, you will see all containers on your system, including stopped containers and running containers.

```console
$ docker ps --all

CONTAINER ID   IMAGE            COMMAND                  CREATED              STATUS                      PORTS     NAMES
d75e61fcad1e   docker-gs-ping   "/docker-gs-ping"        About a minute ago   Exited (2) 23 seconds ago             inspiring_ishizaka
f65dbbb9a548   docker-gs-ping   "/docker-gs-ping"        3 minutes ago        Exited (2) 2 minutes ago              wizardly_joliot
aade1bf3d330   docker-gs-ping   "/docker-gs-ping"        3 minutes ago        Exited (2) 3 minutes ago              magical_carson
52d5ce3c15f0   docker-gs-ping   "/docker-gs-ping"        9 minutes ago        Exited (2) 3 minutes ago              gifted_mestorf
```

If you’ve been following along, you should see several containers listed. These are containers that you started and stopped but haven't removed yet.

Restart the container that you have just stopped. Locate the name of the container and replace the name of the container in the following `restart` command:

```console
$ docker restart inspiring_ishizaka
```

Now, list all the containers again using the `ps` command:

```console
$ docker ps -a

CONTAINER ID   IMAGE            COMMAND                  CREATED          STATUS                     PORTS                    NAMES
d75e61fcad1e   docker-gs-ping   "/docker-gs-ping"        2 minutes ago    Up 5 seconds               0.0.0.0:8080->8080/tcp   inspiring_ishizaka
f65dbbb9a548   docker-gs-ping   "/docker-gs-ping"        4 minutes ago    Exited (2) 2 minutes ago                            wizardly_joliot
aade1bf3d330   docker-gs-ping   "/docker-gs-ping"        4 minutes ago    Exited (2) 4 minutes ago                            magical_carson
52d5ce3c15f0   docker-gs-ping   "/docker-gs-ping"        10 minutes ago   Exited (2) 4 minutes ago                            gifted_mestorf
```

Notice that the container you just restarted has been started in detached mode and has port `8080` exposed. Also, note that the status of the container is `Up X seconds`. When you restart a container, it will be started with the same flags or commands that it was originally started with.

Stop and remove all of your containers and take a look at fixing the random naming issue.

Stop the container you just started. Find the name of your running container and replace the name in the following command with the name of the container on your system:

```console
$ docker stop inspiring_ishizaka
inspiring_ishizaka
```

Now that all of your containers are stopped, remove them. When a container is removed, it's no longer running nor is it in the stopped state. Instead, the process inside the container is terminated and the metadata for the container is removed.

To remove a container, run the `docker rm` command passing the container name. You can pass multiple container names to the command in one command.

Again, make sure you replace the containers names in the following command with the container names from your system:

```console
$ docker rm inspiring_ishizaka wizardly_joliot magical_carson gifted_mestorf

inspiring_ishizaka
wizardly_joliot
magical_carson
gifted_mestorf
```

Run the `docker ps --all` command again to verify that all containers are gone.

Now, address the pesky random name issue. Standard practice is to name your containers for the simple reason that it's easier to identify what's running in the container and what application or service it's associated with. Just like good naming conventions for variables in your code makes it simpler to read. So goes naming your containers.

To name a container, you must pass the `--name` flag to the `run` command:

```console
$ docker run -d -p 8080:8080 --name rest-server docker-gs-ping
3bbc6a3102ea368c8b966e1878a5ea9b1fc61187afaac1276c41db22e4b7f48f
```

```console
$ docker ps

CONTAINER ID   IMAGE            COMMAND             CREATED          STATUS          PORTS                    NAMES
3bbc6a3102ea   docker-gs-ping   "/docker-gs-ping"   25 seconds ago   Up 24 seconds   0.0.0.0:8080->8080/tcp   rest-server
```

Now, you can easily identify your container based on the name.

## Next steps

In this module, you learned how to run containers and publish ports. You also learned to manage the lifecycle of containers. You then learned the importance of naming your containers so that they're more easily identifiable. In the next module, you’ll learn how to run a database in a container and connect it to your application.

---

# Run your tests using Go test

> How to build and run your Go tests in a container

# Run your tests using Go test

   Table of contents

---

## Prerequisites

Complete the [Build your Go image](https://docs.docker.com/guides/golang/build-images/) section of this guide.

## Overview

Testing is an essential part of modern software development. Testing can mean a
lot of things to different development teams. There are unit tests, integration
tests and end-to-end testing. In this guide you take a look at running your unit
tests in Docker when building.

For this section, use the `docker-gs-ping` project that you cloned in [Build
your Go image](https://docs.docker.com/guides/golang/build-images/).

## Run tests when building

To run your tests when building, you need to add a test stage to the
`Dockerfile.multistage`. The `Dockerfile.multistage` in the sample application's
repository already has the following content:

```dockerfile
# syntax=docker/dockerfile:1

# Build the application from source
FROM golang:1.19 AS build-stage

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY *.go ./

RUN CGO_ENABLED=0 GOOS=linux go build -o /docker-gs-ping

# Run the tests in the container
FROM build-stage AS run-test-stage
RUN go test -v ./...

# Deploy the application binary into a lean image
FROM gcr.io/distroless/base-debian11 AS build-release-stage

WORKDIR /

COPY --from=build-stage /docker-gs-ping /docker-gs-ping

EXPOSE 8080

USER nonroot:nonroot

ENTRYPOINT ["/docker-gs-ping"]
```

Run the following command to build an image using the `run-test-stage` stage as the target and view the test results. Include `--progress plain` to view the build output, `--no-cache` to ensure the tests always run, and `--target run-test-stage` to target the test stage.

```console
$ docker build -f Dockerfile.multistage -t docker-gs-ping-test --progress plain --no-cache --target run-test-stage .
```

You should see output containing the following.

```text
#13 [run-test-stage 1/1] RUN go test -v ./...
#13 4.915 === RUN   TestIntMinBasic
#13 4.915 --- PASS: TestIntMinBasic (0.00s)
#13 4.915 === RUN   TestIntMinTableDriven
#13 4.915 === RUN   TestIntMinTableDriven/0,1
#13 4.915 === RUN   TestIntMinTableDriven/1,0
#13 4.915 === RUN   TestIntMinTableDriven/2,-2
#13 4.915 === RUN   TestIntMinTableDriven/0,-1
#13 4.915 === RUN   TestIntMinTableDriven/-1,0
#13 4.915 --- PASS: TestIntMinTableDriven (0.00s)
#13 4.915     --- PASS: TestIntMinTableDriven/0,1 (0.00s)
#13 4.915     --- PASS: TestIntMinTableDriven/1,0 (0.00s)
#13 4.915     --- PASS: TestIntMinTableDriven/2,-2 (0.00s)
#13 4.915     --- PASS: TestIntMinTableDriven/0,-1 (0.00s)
#13 4.915     --- PASS: TestIntMinTableDriven/-1,0 (0.00s)
#13 4.915 PASS
```

## Next steps

In this section, you learned how to run tests when building your image. Next,
you’ll learn how to set up a CI/CD pipeline using GitHub Actions.

---

# Go language

> Containerize Go apps using Docker

# Go language-specific guide

Table of contents

---

This guide will show you how to create, test, and deploy containerized Go applications using Docker.

> **Acknowledgment**
>
>
>
> Docker would like to thank [Oliver Frolovs](https://www.linkedin.com/in/ofr/) for his contribution to this guide.

## What will you learn?

In this guide, you’ll learn how to:

- Create a `Dockerfile` which contains the instructions for building a container image for a program written in Go.
- Run the image as a container in your local Docker instance and manage the container's lifecycle.
- Use multi-stage builds for building small images efficiently while keeping your Dockerfiles easy to read and maintain.
- Use Docker Compose to orchestrate running of multiple related containers together in a development environment.
- Configure a CI/CD pipeline for your application using [GitHub Actions](https://docs.github.com/en/actions)
- Deploy your containerized Go application.

## Prerequisites

Some basic understanding of Go and its toolchain is assumed. This isn't a Go tutorial. If you are new to the : languages:,
the [Go website](https://golang.org/) is a great place to explore,
so *go* (pun intended) check it out!

You also must know some basic
[Docker concepts](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/) as well as to
be at least vaguely familiar with the
[Dockerfile format](https://docs.docker.com/build/concepts/dockerfile/).

Your Docker set-up must have BuildKit enabled. BuildKit is enabled by default for all users on
[Docker Desktop](https://docs.docker.com/desktop/).
If you have installed Docker Desktop, you don’t have to manually enable BuildKit. If you are running Docker on Linux,
please check out BuildKit
[getting started](https://docs.docker.com/build/buildkit/#getting-started) page.

Some familiarity with the command line is also expected.

## What's next?

The aim of this guide is to provide enough examples and instructions for you to containerize your own Go application and deploy it into the Cloud.

Start by building your first Go image.

## Modules

1. [Build images](https://docs.docker.com/guides/golang/build-images/)
  Learn how to build your first Docker image by writing a Dockerfile
2. [Run containers](https://docs.docker.com/guides/golang/run-containers/)
  Learn how to run the image as a container.
3. [Develop your app](https://docs.docker.com/guides/golang/develop/)
  Learn how to develop your application locally.
4. [Run your tests](https://docs.docker.com/guides/golang/run-tests/)
  How to build and run your Go tests in a container
5. [Configure CI/CD](https://docs.docker.com/guides/golang/configure-ci-cd/)
  Learn how to Configure CI/CD for your Go application
6. [Test your deployment](https://docs.docker.com/guides/golang/deploy/)
  Learn how to deploy your Go application

---

# Configure CI/CD for your Java application

> Learn how to Configure CI/CD for your Java application

# Configure CI/CD for your Java application

   Table of contents

---

## Prerequisites

Complete the previous sections of this guide, starting with [Containerize your app](https://docs.docker.com/guides/java/containerize/). You must have a [GitHub](https://github.com/signup) account and a verified [Docker](https://hub.docker.com/signup) account to complete this section.

## Overview

In this section, you'll learn how to set up and use GitHub Actions to build and push your Docker image to Docker Hub. You will complete the following steps:

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
7. Run the following commands to stage, commit, and push your local repository to GitHub.
  ```console
  $ git add -A
  $ git commit -m "my commit"
  $ git push -u origin main
  ```

## Step two: Set up the workflow

Set up your GitHub Actions workflow for building, testing, and pushing the image
to Docker Hub.

1. Go to your repository on GitHub and then select the **Actions** tab.
  The project already has the `maven-build` workflow to build and test your Java application with Maven. If you want, you can optionally disable this workflow because you won't use it in this guide. You'll create a new, alternate workflow to build, test, and push your image.
2. Select **New workflow**.
3. Select **set up a workflow yourself**.
  This takes you to a page for creating a new GitHub actions workflow file in
  your repository, under `.github/workflows/main.yml` by default.
4. In the editor window, copy and paste the following YAML configuration.
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

# Containerize a Java application

> Learn how to containerize a Java application.

# Containerize a Java application

   Table of contents

---

## Prerequisites

- You have installed the latest version of
  [Docker Desktop](https://docs.docker.com/get-started/get-docker/).
  Docker adds new features regularly and some parts of this guide may
  work only with the latest version of Docker Desktop.

- You have a [Git client](https://git-scm.com/downloads). The examples in this
  section use a command-line based Git client, but you can use any client.

## Overview

This section walks you through containerizing and running a Java
application.

## Get the sample applications

Clone the sample application that you'll be using to your local development machine. Run the following command in a terminal to clone the repository.

```console
$ git clone https://github.com/spring-projects/spring-petclinic.git
```

The sample application is a Spring Boot application built using Maven. For more details, see `readme.md` in the repository.

## Initialize Docker assets

Now that you have an application, you can create the necessary Docker assets to
containerize your application. You can use Docker Desktop's built-in Docker Init
feature to help streamline the process, or you can manually create the assets.

Inside the `spring-petclinic` directory, run the `docker init` command. `docker init` provides some default configuration, but you'll need to answer a few
questions about your application. Refer to the following example to answer the
prompts from `docker init` and use the same answers for your prompts.

The sample application already contains Docker assets. You'll be prompted to overwrite the existing Docker assets. To continue with this guide, select `y` to overwrite them.

```console
$ docker init
Welcome to the Docker Init CLI!

This utility will walk you through creating the following files with sensible defaults for your project:
  - .dockerignore
  - Dockerfile
  - compose.yaml
  - README.Docker.md

Let's get started!

WARNING: The following Docker files already exist in this directory:
  - docker-compose.yml
? Do you want to overwrite them? Yes
? What application platform does your project use? Java
? What's the relative directory (with a leading .) for your app? ./src
? What version of Java do you want to use? 21
? What port does your server listen on? 8080
```

In the previous example, notice the `WARNING`. `docker-compose.yaml` already
exists, so `docker init` overwrites that file rather than creating a new
`compose.yaml` file. This prevents having multiple Compose files in the
directory. Both names are supported, but Compose prefers the canonical
`compose.yaml`.

If you don't have Docker Desktop installed or prefer creating the assets
manually, you can create the following files in your project directory.

Create a file named `Dockerfile` with the following contents.

Dockerfile

```dockerfile
# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

################################################################################

# Create a stage for resolving and downloading dependencies.
FROM eclipse-temurin:21-jdk-jammy as deps

WORKDIR /build

# Copy the mvnw wrapper with executable permissions.
COPY --chmod=0755 mvnw mvnw
COPY .mvn/ .mvn/

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.m2 so that subsequent builds don't have to
# re-download packages.
RUN --mount=type=bind,source=pom.xml,target=pom.xml \
    --mount=type=cache,target=/root/.m2 ./mvnw dependency:go-offline -DskipTests

################################################################################

# Create a stage for building the application based on the stage with downloaded dependencies.
# This Dockerfile is optimized for Java applications that output an uber jar, which includes
# all the dependencies needed to run your app inside a JVM. If your app doesn't output an uber
# jar and instead relies on an application server like Apache Tomcat, you'll need to update this
# stage with the correct filename of your package and update the base image of the "final" stage
# use the relevant app server, e.g., using tomcat (https://hub.docker.com/_/tomcat/) as a base image.
FROM deps as package

WORKDIR /build

COPY ./src src/
RUN --mount=type=bind,source=pom.xml,target=pom.xml \
    --mount=type=cache,target=/root/.m2 \
    ./mvnw package -DskipTests && \
    mv target/$(./mvnw help:evaluate -Dexpression=project.artifactId -q -DforceStdout)-$(./mvnw help:evaluate -Dexpression=project.version -q -DforceStdout).jar target/app.jar

################################################################################

# Create a stage for extracting the application into separate layers.
# Take advantage of Spring Boot's layer tools and Docker's caching by extracting
# the packaged application into separate layers that can be copied into the final stage.
# See Spring's docs for reference:
# https://docs.spring.io/spring-boot/docs/current/reference/html/container-images.html
FROM package as extract

WORKDIR /build

RUN java -Djarmode=layertools -jar target/app.jar extract --destination target/extracted

################################################################################

# Create a new stage for running the application that contains the minimal
# runtime dependencies for the application. This often uses a different base
# image from the install or build stage where the necessary files are copied
# from the install stage.
#
# The example below uses eclipse-turmin's JRE image as the foundation for running the app.
# By specifying the "17-jre-jammy" tag, it will also use whatever happens to be the
# most recent version of that tag when you build your Dockerfile.
# If reproducibility is important, consider using a specific digest SHA, like
# eclipse-temurin@sha256:99cede493dfd88720b610eb8077c8688d3cca50003d76d1d539b0efc8cca72b4.
FROM eclipse-temurin:21-jre-jammy AS final

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
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

# Copy the executable from the "package" stage.
COPY --from=extract build/target/extracted/dependencies/ ./
COPY --from=extract build/target/extracted/spring-boot-loader/ ./
COPY --from=extract build/target/extracted/snapshot-dependencies/ ./
COPY --from=extract build/target/extracted/application/ ./

EXPOSE 8080

ENTRYPOINT [ "java", "org.springframework.boot.loader.launch.JarLauncher" ]
```

The sample already contains a Compose file. Overwrite this file to follow along with the guide. Update the`docker-compose.yaml` with the following contents.

docker-compose.yaml

```yaml
# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Docker Compose reference guide at
# https://docs.docker.com/go/compose-spec-reference/

# Here the instructions define your application as a service called "server".
# This service is built from the Dockerfile in the current directory.
# You can add other services your application may depend on here, such as a
# database or a cache. For examples, see the Awesome Compose repository:
# https://github.com/docker/awesome-compose
services:
  server:
    build:
      context: .
    ports:
      - 8080:8080
# The commented out section below is an example of how to define a PostgreSQL
# database that your application can use. `depends_on` tells Docker Compose to
# start the database before your application. The `db-data` volume persists the
# database data between container restarts. The `db-password` secret is used
# to set the database password. You must create `db/password.txt` and add
# a password of your choosing to it before running `docker compose up`.
#     depends_on:
#       db:
#         condition: service_healthy
#   db:
#     image: postgres:18
#     restart: always
#     user: postgres
#     secrets:
#       - db-password
#     volumes:
#       - db-data:/var/lib/postgresql
#     environment:
#       - POSTGRES_DB=example
#       - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
#     expose:
#       - 5432
#     healthcheck:
#       test: [ "CMD", "pg_isready" ]
#       interval: 10s
#       timeout: 5s
#       retries: 5
# volumes:
#   db-data:
# secrets:
#   db-password:
#     file: db/password.txt
```

Create a file named `.dockerignore` with the following contents.

.dockerignore

```text
# Include any files or directories that you don't want to be copied to your
# container here (e.g., local build artifacts, temporary files, etc.).
#
# For more help, visit the .dockerignore file reference guide at
# https://docs.docker.com/go/build-context-dockerignore/

**/.classpath
**/.dockerignore
**/.env
**/.git
**/.gitignore
**/.project
**/.settings
**/.toolstarget
**/.vs
**/.vscode
**/.next
**/.cache
**/*.*proj.user
**/*.dbmdl
**/*.jfm
**/charts
**/docker-compose*
**/compose.y*ml
**/target
**/Dockerfile*
**/node_modules
**/npm-debug.log
**/obj
**/secrets.dev.yaml
**/values.dev.yaml
**/vendor
LICENSE
README.md
```

You should now have the following three files in your `spring-petclinic`
directory.

- [Dockerfile](https://docs.docker.com/reference/dockerfile/)
- [.dockerignore](https://docs.docker.com/reference/dockerfile/#dockerignore-file)
- [docker-compose.yaml](https://docs.docker.com/reference/compose-file/)

## Run the application

Inside the `spring-petclinic` directory, run the following command in a
terminal.

```console
$ docker compose up --build
```

The first time you build and run the app, Docker downloads dependencies and builds the app. It may take several minutes depending on your network connection.

Open a browser and view the application at [http://localhost:8080](http://localhost:8080). You should see a simple app for a pet clinic.

In the terminal, press `ctrl`+`c` to stop the application.

### Run the application in the background

You can run the application detached from the terminal by adding the `-d`
option. Inside the `spring-petclinic` directory, run the following command
in a terminal.

```console
$ docker compose up --build -d
```

Open a browser and view the application at [http://localhost:8080](http://localhost:8080). You should see a simple app for a pet clinic.

In the terminal, run the following command to stop the application.

```console
$ docker compose down
```

For more information about Compose commands, see the
[Compose CLI reference](https://docs.docker.com/reference/cli/docker/compose/).

## Summary

In this section, you learned how you can containerize and run a Java
application using Docker.

Related information:

- [docker init reference](https://docs.docker.com/reference/cli/docker/init/)

## Next steps

In the next section, you'll learn how you can develop your application using
Docker containers.

---

# Test your Java deployment

> Learn how to develop locally using Kubernetes

# Test your Java deployment

   Table of contents

---

## Prerequisites

- Complete all the previous sections of this guide, starting with [Containerize your app](https://docs.docker.com/guides/java/containerize/).
- [Turn on Kubernetes](https://docs.docker.com/desktop/use-desktop/kubernetes/#enable-kubernetes) in Docker Desktop.

## Overview

In this section, you'll learn how to use Docker Desktop to deploy your
application to a fully-featured Kubernetes environment on your development
machine. This lets you test and debug your workloads on Kubernetes locally
before deploying.

## Create a Kubernetes YAML file

In your `spring-petclinic` directory, create a file named
`docker-java-kubernetes.yaml`. Open the file in an IDE or text editor and add
the following contents. Replace `DOCKER_USERNAME/REPO_NAME` with your Docker
username and the name of the repository that you created in [Configure CI/CD for
your Java application](https://docs.docker.com/guides/java/configure-ci-cd/).

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: docker-java-demo
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      service: server
  template:
    metadata:
      labels:
        service: server
    spec:
      containers:
        - name: server-service
          image: DOCKER_USERNAME/REPO_NAME
          imagePullPolicy: Always
---
apiVersion: v1
kind: Service
metadata:
  name: service-entrypoint
  namespace: default
spec:
  type: NodePort
  selector:
    service: server
  ports:
    - port: 8080
      targetPort: 8080
      nodePort: 30001
```

In this Kubernetes YAML file, there are two objects, separated by the `---`:

- A Deployment, describing a scalable group of identical pods. In this case,
  you'll get just one replica, or copy of your pod. That pod, which is
  described under `template`, has just one container in it. The
  container is created from the image built by GitHub Actions in [Configure CI/CD for
  your Java application](https://docs.docker.com/guides/java/configure-ci-cd/).
- A NodePort service, which will route traffic from port 30001 on your host to
  port 8080 inside the pods it routes to, allowing you to reach your app
  from the network.

To learn more about Kubernetes objects, see the [Kubernetes documentation](https://kubernetes.io/docs/home/).

## Deploy and check your application

1. In a terminal, navigate to `spring-petclinic` and deploy your application to
  Kubernetes.
  ```console
  $ kubectl apply -f docker-java-kubernetes.yaml
  ```
  You should see output that looks like the following, indicating your Kubernetes objects were created successfully.
  ```shell
  deployment.apps/docker-java-demo created
  service/service-entrypoint created
  ```
2. Make sure everything worked by listing your deployments.
  ```console
  $ kubectl get deployments
  ```
  Your deployment should be listed as follows:
  ```shell
  NAME                 READY   UP-TO-DATE   AVAILABLE   AGE
  docker-java-demo     1/1     1            1           15s
  ```
  This indicates all one of the pods you asked for in your YAML are up and running. Do the same check for your services.
  ```console
  $ kubectl get services
  ```
  You should get output like the following.
  ```shell
  NAME                 TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
  kubernetes           ClusterIP   10.96.0.1       <none>        443/TCP          23h
  service-entrypoint   NodePort    10.99.128.230   <none>        8080:30001/TCP   75s
  ```
  In addition to the default `kubernetes` service, you can see your `service-entrypoint` service, accepting traffic on port 30001/TCP.
3. In a terminal, curl the service. Note that a database wasn't deployed in
  this example.
  ```console
  $ curl --request GET \
    --url http://localhost:30001/actuator/health \
    --header 'content-type: application/json'
  ```
  You should get output like the following.
  ```console
  {"status":"UP","groups":["liveness","readiness"]}
  ```
4. Run the following command to tear down your application.
  ```console
  $ kubectl delete -f docker-java-kubernetes.yaml
  ```

## Summary

In this section, you learned how to use Docker Desktop to deploy your application to a fully-featured Kubernetes environment on your development machine.

Related information:

- [Kubernetes documentation](https://kubernetes.io/docs/home/)
- [Deploy on Kubernetes with Docker Desktop](https://docs.docker.com/desktop/use-desktop/kubernetes/)
- [Swarm mode overview](https://docs.docker.com/engine/swarm/)
