# Writing a Dockerfile and more

# Writing a Dockerfile

> This concept page will teach you how to create image using Dockerfile.

# Writing a Dockerfile

   Table of contents

---

## Explanation

A Dockerfile is a text-based document that's used to create a container image. It provides instructions to the image builder on the commands to run, files to copy, startup command, and more.

As an example, the following Dockerfile would produce a ready-to-run Python application:

```dockerfile
FROM python:3.13
WORKDIR /usr/local/app

# Install the application dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy in the source code
COPY src ./src
EXPOSE 8080

# Setup an app user so the container doesn't run as the root user
RUN useradd app
USER app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

### Common instructions

Some of the most common instructions in a `Dockerfile` include:

- `FROM <image>` - this specifies the base image that the build will extend.
- `WORKDIR <path>` - this instruction specifies the "working directory" or the path in the image where files will be copied and commands will be executed.
- `COPY <host-path> <image-path>` - this instruction tells the builder to copy files from the host and put them into the container image.
- `RUN <command>` - this instruction tells the builder to run the specified command.
- `ENV <name> <value>` - this instruction sets an environment variable that a running container will use.
- `EXPOSE <port-number>` - this instruction sets configuration on the image that indicates a port the image would like to expose.
- `USER <user-or-uid>` - this instruction sets the default user for all subsequent instructions.
- `CMD ["<command>", "<arg1>"]` - this instruction sets the default command a container using this image will run.

To read through all of the instructions or go into greater detail, check out the [Dockerfile reference](https://docs.docker.com/engine/reference/builder/).

## Try it out

Just as you saw with the previous example, a Dockerfile typically follows these steps:

1. Determine your base image
2. Install application dependencies
3. Copy in any relevant source code and/or binaries
4. Configure the final image

In this quick hands-on guide, you'll write a Dockerfile that builds a simple Node.js application. If you're not familiar with JavaScript-based applications, don't worry. It isn't necessary for following along with this guide.

### Set up

[Download this ZIP file](https://github.com/docker/getting-started-todo-app/archive/refs/heads/build-image-from-scratch.zip) and extract the contents into a directory on your machine.

If you'd rather not download a ZIP file, clone the [https://github.com/docker/getting-started-todo-app](https://github.com/docker/getting-started-todo-app) project and checkout the `build-image-from-scratch` branch.

### Creating the Dockerfile

Now that you have the project, you’re ready to create the `Dockerfile`.

1. [Download and install](https://www.docker.com/products/docker-desktop/) Docker Desktop.
2. Examine the project.
  Explore the contents of `getting-started-todo-app/app/`. You'll notice that a
  `Dockerfile` already exists. It is a simple text file that you can open in
  any text or code editor.
3. Delete the existing `Dockerfile`.
  For this exercise, you'll pretend you're starting from scratch and will
  create a new `Dockerfile`.
4. Create a file named `Dockerfile` in the `getting-started-todo-app/app/` folder.
  > **Dockerfile file extensions**
  >
  >
  >
  > It's important to note that the `Dockerfile` has *no* file extension. Some editors
  > will automatically add an extension to the file (or complain it doesn't have one).
5. In the `Dockerfile`, define your base image by adding the following line:
  ```dockerfile
  FROM node:22-alpine
  ```
6. Now, define the working directory by using the `WORKDIR` instruction. This will specify where future commands will run and the directory files will be copied inside the container image.
  ```dockerfile
  WORKDIR /app
  ```
7. Copy all of the files from your project on your machine into the container image by using the `COPY` instruction:
  ```dockerfile
  COPY . .
  ```
8. Install the app's dependencies by using the `yarn` CLI and package manager. To do so, run a command using the `RUN` instruction:
  ```dockerfile
  RUN yarn install --production
  ```
9. Finally, specify the default command to run by using the `CMD` instruction:
  ```dockerfile
  CMD ["node", "./src/index.js"]
  ```
  And with that, you should have the following Dockerfile:
  ```dockerfile
  FROM node:22-alpine
  WORKDIR /app
  COPY . .
  RUN yarn install --production
  CMD ["node", "./src/index.js"]
  ```

> **This Dockerfile isn't production-ready yet**
>
>
>
> It's important to note that this Dockerfile is *not* following all
> of the best practices yet (by design). It will build the app, but the
> builds won't be as fast, or the images as secure, as they could be.
>
>
>
> Keep reading to learn more about how to make the image maximize the
> build cache, run as a non-root user, and multi-stage builds.

> **Containerize new projects quickly withdocker init**
>
>
>
> The `docker init` command will analyze your project and quickly create
> a Dockerfile, a `compose.yaml`, and a `.dockerignore`, helping you get
> up and going. Since you're learning about Dockerfiles specifically here,
> you won't use it now. But,
> [learn more about it here](https://docs.docker.com/engine/reference/commandline/init/).

## Additional resources

To learn more about writing a Dockerfile, visit the following resources:

- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
- [Dockerfile best practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Base images](https://docs.docker.com/build/building/base-images/)
- [Getting started with Docker Init](https://docs.docker.com/reference/cli/docker/init/)

## Next steps

Now that you have created a Dockerfile and learned the basics, it's time to learn about building, tagging, and pushing the images.

[Build, tag and publish the Image](https://docs.docker.com/get-started/docker-concepts/building-images/build-tag-and-publish-an-image/)

---

# Building images

> Learn how to build Docker images from a Dockerfile. You'll understand the structure of a Dockerfile, how to build an image, and how to customize the build process.

# Building images

Building container images is both technical and an art. You want to keep the
image small and focused to increase your security posture, but also need to
balance potential tradeoffs, such as caching impacts. In this series, you’ll
deep dive into the secrets of images, how they are built and best practices.**Skill level** Beginner**Time to complete** 25 minutes**Prerequisites** None

## About this series

Learn how to build production-ready images that are lean and efficient Docker
images, essential for minimizing overhead and enhancing deployment in
production environments.

## What you'll learn

- Understanding image layers
- Writing a Dockerfile
- Build, tag and publish an image
- Using the build cache
- Multi-stage builds

## Modules

Have you ever wondered how images work? This guide will help you to
understand image layers - the fundamental building blocks of container
images. You'll gain a comprehensive understanding of how layers are created,
stacked, and utilized to ensure efficient and optimized containers.

[Start](https://docs.docker.com/get-started/docker-concepts/building-images/understanding-image-layers/)

Mastering Dockerfile practices is vital for leveraging container technology
effectively, enhancing application reliability and supporting DevOps and
CI/CD methodologies. In this guide, you’ll learn how to write a Dockerfile,
how to define a base image and setup instructions, including software
installation and copying necessary files.

[Start](https://docs.docker.com/get-started/docker-concepts/building-images/writing-a-dockerfile/)

Building, tagging, and publishing Docker images are key steps in the
containerization workflow. In this guide, you’ll learn how to create Docker
images, how to tag those images with a unique identifier, and how to publish
your image to a public registry.

[Start](https://docs.docker.com/get-started/docker-concepts/building-images/build-tag-and-publish-an-image/)

Using the build cache effectively allows you to achieve faster builds by
reusing results from previous builds and skipping unnecessary steps. To
maximize cache usage and avoid resource-intensive and time-consuming
rebuilds, it's crucial to understand how cache invalidation works. In this
guide, you’ll learn how to use the Docker build cache efficiently for
streamlined Docker image development and continuous integration workflows.

[Start](https://docs.docker.com/get-started/docker-concepts/building-images/using-the-build-cache/)

By separating the build environment from the final runtime environment, you
can significantly reduce the image size and attack surface. In this guide,
you'll unlock the power of multi-stage builds to create lean and efficient
Docker images, essential for minimizing overhead and enhancing deployment in
production environments.

[Start](https://docs.docker.com/get-started/docker-concepts/building-images/multi-stage-builds/)

---

# Multi

> This concept page will teach you the significance of multi-container application and how it is different from single-container application

# Multi-container applications

   Table of contents

---

## Explanation

Starting up a single-container application is easy. For example, a Python script that performs a specific data processing task runs within a container with all its dependencies. Similarly, a Node.js application serving a static website with a small API endpoint can be effectively containerized with all its necessary libraries and dependencies. However, as applications grow in size, managing them as individual containers becomes more difficult.

Imagine the data processing Python script needs to connect to a database. Suddenly, you're now managing not just the script but also a database server within the same container. If the script requires user logins, you'll need an authentication mechanism, further bloating the container size.

One best practice for containers is that each container should do one thing and do it well. While there are exceptions to this rule, avoid the tendency to have one container do multiple things.

Now you might ask, "Do I need to run these containers separately? If I run them separately, how shall I connect them all together?"

While `docker run` is a convenient tool for launching containers, it becomes difficult to manage a growing application stack with it. Here's why:

- Imagine running several `docker run` commands (frontend, backend, and database) with different configurations for development, testing, and production environments. It's error-prone and time-consuming.
- Applications often rely on each other. Manually starting containers in a specific order and managing network connections become difficult as the stack expands.
- Each application needs its `docker run` command, making it difficult to scale individual services. Scaling the entire application means potentially wasting resources on components that don't need a boost.
- Persisting data for each application requires separate volume mounts or configurations within each `docker run` command. This creates a scattered data management approach.
- Setting environment variables for each application through separate `docker run` commands is tedious and error-prone.

That's where Docker Compose comes to the rescue.

Docker Compose defines your entire multi-container application in a single YAML file called `compose.yml`. This file specifies configurations for all your containers, their dependencies, environment variables, and even volumes and networks. With Docker Compose:

- You don't need to run multiple `docker run` commands. All you need to do is define your entire multi-container application in a single YAML file. This centralizes configuration and simplifies management.
- You can run containers in a specific order and manage network connections easily.
- You can simply scale individual services up or down within the multi-container setup. This allows for efficient allocation based on real-time needs.
- You can implement persistent volumes with ease.
- It's easy to set environment variables once in your Docker Compose file.

By leveraging Docker Compose for running multi-container setups, you can build complex applications with modularity, scalability, and consistency at their core.

## Try it out

In this hands-on guide, you'll first see how to build and run a counter web application based on Node.js, an Nginx reverse proxy, and a Redis database using the `docker run` commands. You’ll also see how you can simplify the entire deployment process using Docker Compose.

### Set up

1. Get the sample application. If you have Git, you can clone the repository for the sample application. Otherwise, you can download the sample application. Choose one of the following options.
  Use the following command in a terminal to clone the sample application repository.
  ```console
  $ git clone https://github.com/dockersamples/nginx-node-redis
  ```
  Navigate into the `nginx-node-redis` directory:
  ```console
  $ cd nginx-node-redis
  ```
  Inside this directory, you'll find two sub-directories - `nginx` and `web`.
  Download the source and extract it.
  [Download the source](https://github.com/dockersamples/nginx-node-redis/archive/refs/heads/main.zip)
  Navigate into the `nginx-node-redis-main` directory:
  ```console
  $ cd nginx-node-redis-main
  ```
  Inside this directory, you'll find two sub-directories - `nginx` and `web`.
2. [Download and install](https://docs.docker.com/get-started/get-docker/) Docker Desktop.

### Build the images

1. Navigate into the `nginx` directory to build the image by running the following command:
  ```console
  $ docker build -t nginx .
  ```
2. Navigate into the `web` directory and run the following command to build the first web image:
  ```console
  $ docker build -t web .
  ```

### Run the containers

1. Before you can run a multi-container application, you need to create a network for them all to communicate through. You can do so using the `docker network create` command:
  ```console
  $ docker network create sample-app
  ```
2. Start the Redis container by running the following command, which will attach it to the previously created network and create a network alias (useful for DNS lookups):
  ```console
  $ docker run -d  --name redis --network sample-app --network-alias redis redis
  ```
3. Start the first web container by running the following command:
  ```console
  $ docker run -d --name web1 -h web1 --network sample-app --network-alias web1 web
  ```
4. Start the second web container by running the following:
  ```console
  $ docker run -d --name web2 -h web2 --network sample-app --network-alias web2 web
  ```
5. Start the Nginx container by running the following command:
  ```console
  $ docker run -d --name nginx --network sample-app  -p 80:80 nginx
  ```
  > Note
  >
  > Nginx is typically used as a reverse proxy for web applications, routing traffic to backend servers. In this case, it routes to the Node.js backend containers (web1 or web2).
6. Verify the containers are up by running the following command:
  ```console
  $ docker ps
  ```
  You will see output like the following:
  ```text
  CONTAINER ID   IMAGE     COMMAND                  CREATED              STATUS              PORTS                NAMES
  2cf7c484c144   nginx     "/docker-entrypoint.…"   9 seconds ago        Up 8 seconds        0.0.0.0:80->80/tcp   nginx
  7a070c9ffeaa   web       "docker-entrypoint.s…"   19 seconds ago       Up 18 seconds                            web2
  6dc6d4e60aaf   web       "docker-entrypoint.s…"   34 seconds ago       Up 33 seconds                            web1
  008e0ecf4f36   redis     "docker-entrypoint.s…"   About a minute ago   Up About a minute   6379/tcp             redis
  ```
7. If you look at the Docker Desktop Dashboard, you can see the containers and dive deeper into their configuration.
  ![A screenshot of the Docker Desktop Dashboard showing multi-container applications](https://docs.docker.com/get-started/docker-concepts/running-containers/images/multi-container-apps.webp)  ![A screenshot of the Docker Desktop Dashboard showing multi-container applications](https://docs.docker.com/get-started/docker-concepts/running-containers/images/multi-container-apps.webp)
8. With everything up and running, you can open [http://localhost](http://localhost) in your browser to see the site. Refresh the page several times to see the host that’s handling the request and the total number of requests:
  ```console
  web2: Number of visits is: 9
  web1: Number of visits is: 10
  web2: Number of visits is: 11
  web1: Number of visits is: 12
  ```
  > Note
  >
  > You might have noticed that Nginx, acting as a reverse proxy, likely distributes incoming requests in a round-robin fashion between the two backend containers. This means each request might be directed to a different container (web1 and web2) on a rotating basis. The output shows consecutive increments for both the web1 and web2 containers and the actual counter value stored in Redis is updated only after the response is sent back to the client.
9. You can use the Docker Desktop Dashboard to remove the containers by selecting the containers and selecting the **Delete** button.
  ![A screenshot of Docker Desktop Dashboard showing how to delete the multi-container applications](https://docs.docker.com/get-started/docker-concepts/running-containers/images/delete-multi-container-apps.webp)  ![A screenshot of Docker Desktop Dashboard showing how to delete the multi-container applications](https://docs.docker.com/get-started/docker-concepts/running-containers/images/delete-multi-container-apps.webp)

## Simplify the deployment using Docker Compose

Docker Compose provides a structured and streamlined approach for managing multi-container deployments. As stated earlier, with Docker Compose, you don’t need to run multiple `docker run` commands. All you need to do is define your entire multi-container application in a single YAML file called `compose.yml`. Let’s see how it works.

Navigate to the root of the project directory. Inside this directory, you'll find a file named `compose.yml`. This YAML file is where all the magic happens. It defines all the services that make up your application, along with their configurations. Each service specifies its image, ports, volumes, networks, and any other settings necessary for its functionality.

1. Use the `docker compose up` command to start the application:
  ```console
  $ docker compose up -d --build
  ```
  When you run this command, you should see output similar to the following:
  ```console
  ✔ Network nginx-node-redis_default   Created                                                                                                   0.0s
   ✔ Container nginx-node-redis-web2-1  Created                                                                                                   0.1s
   ✔ Container nginx-node-redis-web1-1  Created                                                                                                   0.1s
   ✔ Container nginx-node-redis-redis-1 Created                                                                                                   0.1s
   ✔ Container nginx-node-redis-nginx-1 Created
  ```
2. If you look at the Docker Desktop Dashboard, you can see the containers and dive deeper into their configuration.
  ![A screenshot of the Docker Desktop Dashboard showing the containers of the application stack deployed using Docker Compose](https://docs.docker.com/get-started/docker-concepts/running-containers/images/list-containers.webp)  ![A screenshot of the Docker Desktop Dashboard showing the containers of the application stack deployed using Docker Compose](https://docs.docker.com/get-started/docker-concepts/running-containers/images/list-containers.webp)
3. Alternatively, you can use the Docker Desktop Dashboard to remove the containers by selecting the application stack and selecting the **Delete** button.
  ![A screenshot of Docker Desktop Dashboard that shows how to remove the containers that you deployed using Docker Compose](https://docs.docker.com/get-started/docker-concepts/running-containers/images/delete-containers.webp)  ![A screenshot of Docker Desktop Dashboard that shows how to remove the containers that you deployed using Docker Compose](https://docs.docker.com/get-started/docker-concepts/running-containers/images/delete-containers.webp)

In this guide, you learned how easy it is to use Docker Compose to start and stop a multi-container application compared to `docker run` which is error-prone and difficult to manage.

## Additional resources

- [docker container runCLI reference](https://docs.docker.com/reference/cli/docker/container/run/)
- [What is Docker Compose](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-docker-compose/)

---

# Overriding container defaults

> This concept page will teach you how to override the container defaults using the `docker run` command.

# Overriding container defaults

   Table of contents

---

## Explanation

When a Docker container starts, it executes an application or command. The container gets this executable (script or file) from its image’s configuration. Containers come with default settings that usually work well, but you can change them if needed. These adjustments help the container's program run exactly how you want it to.

For example, if you have an existing database container that listens on the standard port and you want to run a new instance of the same database container, then you might want to change the port settings the new container listens on so that it doesn’t conflict with the existing container. Sometimes you might want to increase the memory available to the container if the program needs more resources to handle a heavy workload or set the environment variables to provide specific configuration details the program needs to function properly.

The `docker run` command offers a powerful way to override these defaults and tailor the container's behavior to your liking. The command offers several flags that let you to customize container behavior on the fly.

Here's a few ways you can achieve this.

### Overriding the network ports

Sometimes you might want to use separate database instances for development and testing purposes. Running these database instances on the same port might conflict. You can use the `-p` option in `docker run` to map container ports to host ports, allowing you to run the multiple instances of the container without any conflict.

```console
$ docker run -d -p HOST_PORT:CONTAINER_PORT postgres
```

### Setting environment variables

This option sets an environment variable `foo` inside the container with the value `bar`.

```console
$ docker run -e foo=bar postgres env
```

You will see output like the following:

```console
HOSTNAME=2042f2e6ebe4
foo=bar
```

> Tip
>
> The `.env` file acts as a convenient way to set environment variables for your Docker containers without cluttering your command line with numerous `-e` flags. To use a `.env` file, you can pass `--env-file` option with the `docker run` command.
>
>
>
> ```console
> $ docker run --env-file .env postgres env
> ```

### Restricting the container to consume the resources

You can use the `--memory` and `--cpus` flags with the `docker run` command to restrict how much CPU and memory a container can use. For example, you can set a memory limit for the Python API container, preventing it from consuming excessive resources on your host. Here's the command:

```console
$ docker run -e POSTGRES_PASSWORD=secret --memory="512m" --cpus="0.5" postgres
```

This command limits container memory usage to 512 MB and defines the CPU quota of 0.5 for half a core.

> **Monitor the real-time resource usage**
>
>
>
> You can use the `docker stats` command to monitor the real-time resource usage of running containers. This helps you understand whether the allocated resources are sufficient or need adjustment.

By effectively using these `docker run` flags, you can tailor your containerized application's behavior to fit your specific requirements.

## Try it out

In this hands-on guide, you'll see how to use the `docker run` command to override the container defaults.

1. [Download and install](https://docs.docker.com/get-started/get-docker/) Docker Desktop.

### Run multiple instances of the Postgres database

1. Start a container using the [Postgres image](https://hub.docker.com/_/postgres) with the following command:
  ```console
  $ docker run -d -e POSTGRES_PASSWORD=secret -p 5432:5432 postgres
  ```
  This will start the Postgres database in the background, listening on the standard container port `5432` and mapped to port `5432` on the host machine.
2. Start a second Postgres container mapped to a different port.
  ```console
  $ docker run -d -e POSTGRES_PASSWORD=secret -p 5433:5432 postgres
  ```
  This will start another Postgres container in the background, listening on the standard postgres port `5432` in the container, but mapped to port `5433` on the host machine. You override the host port just to ensure that this new container doesn't conflict with the existing running container.
3. Verify that both containers are running by going to the **Containers** view in the Docker Desktop Dashboard.
  ![A screenshot of the Docker Desktop Dashboard showing the running instances of Postgres containers](https://docs.docker.com/get-started/docker-concepts/running-containers/images/running-postgres-containers.webp)  ![A screenshot of the Docker Desktop Dashboard showing the running instances of Postgres containers](https://docs.docker.com/get-started/docker-concepts/running-containers/images/running-postgres-containers.webp)

### Run Postgres container in a controlled network

By default, containers automatically connect to a special network called a bridge network when you run them. This bridge network acts like a virtual bridge, allowing containers on the same host to communicate with each other while keeping them isolated from the outside world and other hosts. It's a convenient starting point for most container interactions. However, for specific scenarios, you might want more control over the network configuration.

Here's where the custom network comes in. You create a custom network by passing `--network` flag with the `docker run` command. All containers without a `--network` flag are attached to the default bridge network.

Follow the steps to see how to connect a Postgres container to a custom network.

1. Create a new custom network by using the following command:
  ```console
  $ docker network create mynetwork
  ```
2. Verify the network by running the following command:
  ```console
  $ docker network ls
  ```
  This command lists all networks, including the newly created "mynetwork".
3. Connect Postgres to the custom network by using the following command:
  ```console
  $ docker run -d -e POSTGRES_PASSWORD=secret -p 5434:5432 --network mynetwork postgres
  ```
  This will start Postgres container in the background, mapped to the host port 5434 and attached to the `mynetwork` network. You passed the `--network` parameter to override the container default by connecting the container to custom Docker network for better isolation and communication with other containers. You can use `docker network inspect` command to see if the container is tied to this new bridge network.
  > **Key difference between default bridge and custom networks**
  >
  >
  >
  > 1. DNS resolution: By default, containers connected to the default bridge network can communicate with each other, but only by IP address. (unless you use `--link` option which is considered legacy). It is not recommended for production use due to the various
  >   [technical shortcomings](https://docs.docker.com/engine/network/drivers/bridge/#differences-between-user-defined-bridges-and-the-default-bridge). On a custom network, containers can resolve each other by name or alias.
  > 2. Isolation: All containers without a `--network` specified are attached to the default bridge network, hence can be a risk, as unrelated containers are then able to communicate. Using a custom network provides a scoped network in which only containers attached to that network are able to communicate, hence providing better isolation.

### Manage the resources

By default, containers are not limited in their resource usage. However, on shared systems, it's crucial to manage resources effectively. It's important not to let a running container consume too much of the host machine's memory.

This is where the `docker run` command shines again. It offers flags like `--memory` and `--cpus` to restrict how much CPU and memory a container can use.

```console
$ docker run -d -e POSTGRES_PASSWORD=secret --memory="512m" --cpus=".5" postgres
```

The `--cpus` flag specifies the CPU quota for the container. Here, it's set to half a CPU core (0.5) whereas the `--memory` flag specifies the memory limit for the container. In this case, it's set to 512 MB.

### Override the default CMD and ENTRYPOINT in Docker Compose

Sometimes, you might need to override the default commands (`CMD`) or entry points (`ENTRYPOINT`) defined in a Docker image, especially when using Docker Compose.

1. Create a `compose.yml` file with the following content:
  ```yaml
  services:
    postgres:
      image: postgres:18
      entrypoint: ["docker-entrypoint.sh", "postgres"]
      command: ["-h", "localhost", "-p", "5432"]
      environment:
        POSTGRES_PASSWORD: secret
  ```
  The Compose file defines a service named `postgres` that uses the official Postgres image, sets an entrypoint script, and starts the container with password authentication.
2. Bring up the service by running the following command:
  ```console
  $ docker compose up -d
  ```
  This command starts the Postgres service defined in the Docker Compose file.
3. Verify the authentication with Docker Desktop Dashboard.
  Open the Docker Desktop Dashboard, select the **Postgres** container and select **Exec** to enter into the container shell. You can type the following command to connect to the Postgres database:
  ```console
  # psql -U postgres
  ```
  ![A screenshot of the Docker Desktop Dashboard selecting the Postgres container and entering into its shell using EXEC button](https://docs.docker.com/get-started/docker-concepts/running-containers/images/exec-into-postgres-container.webp)  ![A screenshot of the Docker Desktop Dashboard selecting the Postgres container and entering into its shell using EXEC button](https://docs.docker.com/get-started/docker-concepts/running-containers/images/exec-into-postgres-container.webp)
  > Note
  >
  > The PostgreSQL image sets up trust authentication locally so you may notice a password isn't required when connecting from localhost (inside the same container). However, a password will be required if connecting from a different host/container.

### Override the default CMD and ENTRYPOINT withdocker run

You can also override defaults directly using the `docker run` command with the following command:

```console
$ docker run -e POSTGRES_PASSWORD=secret postgres docker-entrypoint.sh -h localhost -p 5432
```

This command runs a Postgres container, sets an environment variable for password authentication, overrides the default startup commands and configures hostname and port mapping.

## Additional resources

- [Ways to set environment variables with Compose](https://docs.docker.com/compose/how-tos/environment-variables/set-environment-variables/)
- [What is a container](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/)

## Next steps

Now that you have learned about overriding container defaults, it's time to learn how to persist container data.

[Persisting container data](https://docs.docker.com/get-started/docker-concepts/running-containers/persisting-container-data/)

---

# Persisting container data

> This concept page will teach you the significance of data persistence in Docker

# Persisting container data

   Table of contents

---

## Explanation

When a container starts, it uses the files and configuration provided by the image. Each container is able to create, modify, and delete files and does so without affecting any other containers. When the container is deleted, these file changes are also deleted.

While this ephemeral nature of containers is great, it poses a challenge when you want to persist the data. For example, if you restart a database container, you might not want to start with an empty database. So, how do you persist files?

### Container volumes

Volumes are a storage mechanism that provide the ability to persist data beyond the lifecycle of an individual container. Think of it like providing a shortcut or symlink from inside the container to outside the container.

As an example, imagine you create a volume named `log-data`.

```console
$ docker volume create log-data
```

When starting a container with the following command, the volume will be mounted (or attached) into the container at `/logs`:

```console
$ docker run -d -p 80:80 -v log-data:/logs docker/welcome-to-docker
```

If the volume `log-data` doesn't exist, Docker will automatically create it for you.

When the container runs, all files it writes into the `/logs` folder will be saved in this volume, outside of the container. If you delete the container and start a new container using the same volume, the files will still be there.

> **Sharing files using volumes**
>
>
>
> You can attach the same volume to multiple containers to share files between containers. This might be helpful in scenarios such as log aggregation, data pipelines, or other event-driven applications.

### Managing volumes

Volumes have their own lifecycle beyond that of containers and can grow quite large depending on the type of data and applications you’re using. The following commands will be helpful to manage volumes:

- `docker volume ls` - list all volumes
- `docker volume rm <volume-name-or-id>` - remove a volume (only works when the volume is not attached to any containers)
- `docker volume prune` - remove all unused (unattached) volumes

## Try it out

In this guide, you'll practice creating and using volumes to persist data created by a Postgres container. When the database runs, it stores files into the `/var/lib/postgresql` directory. By attaching the volume here, you will be able to restart the container multiple times while keeping the data.

### Use volumes

1. [Download and install](https://docs.docker.com/get-started/get-docker/) Docker Desktop.
2. Start a container using the [Postgres image](https://hub.docker.com/_/postgres) with the following command:
  ```console
  $ docker run --name=db -e POSTGRES_PASSWORD=secret -d -v postgres_data:/var/lib/postgresql postgres:18
  ```
  This will start the database in the background, configure it with a password, and attach a volume to the directory PostgreSQL will persist the database files.
3. Connect to the database by using the following command:
  ```console
  $ docker exec -ti db psql -U postgres
  ```
4. In the PostgreSQL command line, run the following to create a database table and insert two records:
  ```text
  CREATE TABLE tasks (
      id SERIAL PRIMARY KEY,
      description VARCHAR(100)
  );
  INSERT INTO tasks (description) VALUES ('Finish work'), ('Have fun');
  ```
5. Verify the data is in the database by running the following in the PostgreSQL command line:
  ```text
  SELECT * FROM tasks;
  ```
  You should get output that looks like the following:
  ```text
  id | description
  ----+-------------
    1 | Finish work
    2 | Have fun
  (2 rows)
  ```
6. Exit out of the PostgreSQL shell by running the following command:
  ```console
  \q
  ```
7. Stop and remove the database container. Remember that, even though the container has been deleted, the data is persisted in the `postgres_data` volume.
  ```console
  $ docker stop db
  $ docker rm db
  ```
8. Start a new container by running the following command, attaching the same volume with the persisted data:
  ```console
  $ docker run --name=new-db -d -v postgres_data:/var/lib/postgresql postgres:18
  ```
  You might have noticed that the `POSTGRES_PASSWORD` environment variable has been omitted. That’s because that variable is only used when bootstrapping a new database.
9. Verify the database still has the records by running the following command:
  ```console
  $ docker exec -ti new-db psql -U postgres -c "SELECT * FROM tasks"
  ```

### View volume contents

The Docker Desktop Dashboard provides the ability to view the contents of any volume, as well as the ability to export, import, empty, delete and clone volumes.

1. Open the Docker Desktop Dashboard and navigate to the **Volumes** view. In this view, you should see the **postgres_data** volume.
2. Select the **postgres_data** volume’s name.
3. The **Stored Data** tab shows the contents of the volume and provides the ability to navigate the files. The **Container in-use** tab displays the name of the container using the volume, the image name, the port number used by the container, and the target. A target is a path inside a container that gives access to the files in the volume. The **Exports** tab lets you export the volume. Double-clicking on a file will let you see the contents and make changes.
4. Right-click on any file to save it or delete it.

### Remove volumes

Before removing a volume, it must not be attached to any containers. If you haven’t removed the previous container, do so with the following command (the `-f` will stop the container first and then remove it):

```console
$ docker rm -f new-db
```

There are a few methods to remove volumes, including the following:

- Select the **Delete Volume** option on a volume in the Docker Desktop Dashboard.
- Use the `docker volume rm` command:
  ```console
  $ docker volume rm postgres_data
  ```
- Use the `docker volume prune` command to remove all unused volumes:
  ```console
  $ docker volume prune
  ```

## Additional resources

The following resources will help you learn more about volumes:

- [Manage data in Docker](https://docs.docker.com/engine/storage)
- [Volumes](https://docs.docker.com/engine/storage/volumes)
- [Volume mounts](https://docs.docker.com/engine/containers/run/#volume-mounts)

## Next steps

Now that you have learned about persisting container data, it’s time to learn about sharing local files with containers.

[Sharing local files with containers](https://docs.docker.com/get-started/docker-concepts/running-containers/sharing-local-files/)
