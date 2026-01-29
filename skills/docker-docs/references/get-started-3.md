# Publishing and exposing ports and more

# Publishing and exposing ports

> This concept page will teach you the significance of publishing and exposing ports in Docker

# Publishing and exposing ports

   Table of contents

---

## Explanation

If you've been following the guides so far, you understand that containers provide isolated processes for each component of your application. Each component - a React frontend, a Python API, and a Postgres database - runs in its own sandbox environment, completely isolated from everything else on your host machine. This isolation is great for security and managing dependencies, but it also means you can’t access them directly. For example, you can’t access the web app in your browser.

That’s where port publishing comes in.

### Publishing ports

Publishing a port provides the ability to break through a little bit of networking isolation by setting up a forwarding rule. As an example, you can indicate that requests on your host’s port `8080` should be forwarded to the container’s port `80`. Publishing ports happens during container creation using the `-p` (or `--publish`) flag with `docker run`. The syntax is:

```console
$ docker run -d -p HOST_PORT:CONTAINER_PORT nginx
```

- `HOST_PORT`: The port number on your host machine where you want to receive traffic
- `CONTAINER_PORT`: The port number within the container that's listening for connections

For example, to publish the container's port `80` to host port `8080`:

```console
$ docker run -d -p 8080:80 nginx
```

Now, any traffic sent to port `8080` on your host machine will be forwarded to port `80` within the container.

> Important
>
> When a port is published, it's published to all network interfaces by default. This means any traffic that reaches your machine can access the published application. Be mindful of publishing databases or any sensitive information.
> [Learn more about published ports here](https://docs.docker.com/engine/network/#published-ports).

### Publishing to ephemeral ports

At times, you may want to simply publish the port but don’t care which host port is used. In these cases, you can let Docker pick the port for you. To do so, simply omit the `HOST_PORT` configuration.

For example, the following command will publish the container’s port `80` onto an ephemeral port on the host:

```console
$ docker run -p 80 nginx
```

Once the container is running, using `docker ps` will show you the port that was chosen:

```console
docker ps
CONTAINER ID   IMAGE         COMMAND                  CREATED          STATUS          PORTS                    NAMES
a527355c9c53   nginx         "/docker-entrypoint.…"   4 seconds ago    Up 3 seconds    0.0.0.0:54772->80/tcp    romantic_williamson
```

In this example, the app is exposed on the host at port `54772`.

### Publishing all ports

When creating a container image, the `EXPOSE` instruction is used to indicate the packaged application will use the specified port. These ports aren't published by default.

With the `-P` or `--publish-all` flag, you can automatically publish all exposed ports to ephemeral ports. This is quite useful when you’re trying to avoid port conflicts in development or testing environments.

For example, the following command will publish all of the exposed ports configured by the image:

```console
$ docker run -P nginx
```

## Try it out

In this hands-on guide, you'll learn how to publish container ports using both the CLI and Docker Compose for deploying a web application.

### Use the Docker CLI

In this step, you will run a container and publish its port using the Docker CLI.

1. [Download and install](https://docs.docker.com/get-started/get-docker/) Docker Desktop.
2. In a terminal, run the following command to start a new container:
  ```console
  $ docker run -d -p 8080:80 docker/welcome-to-docker
  ```
  The first `8080` refers to the host port. This is the port on your local machine that will be used to access the application running inside the container. The second `80` refers to the container port. This is the port that the application inside the container listens on for incoming connections. Hence, the command binds to port `8080` of the host to port `80` on the container system.
3. Verify the published port by going to the **Containers** view of the Docker Desktop Dashboard.
  ![A screenshot of Docker Desktop Dashboard showing the published port](https://docs.docker.com/get-started/docker-concepts/running-containers/images/published-ports.webp)  ![A screenshot of Docker Desktop Dashboard showing the published port](https://docs.docker.com/get-started/docker-concepts/running-containers/images/published-ports.webp)
4. Open the website by either selecting the link in the **Port(s)** column of your container or visiting [http://localhost:8080](http://localhost:8080) in your browser.
  ![A screenshot of the landing page of the Nginx web server running in a container](https://docs.docker.com/get-started/docker-concepts/the-basics/images/access-the-frontend.webp?border=true)  ![A screenshot of the landing page of the Nginx web server running in a container](https://docs.docker.com/get-started/docker-concepts/the-basics/images/access-the-frontend.webp?border=true)

### Use Docker Compose

This example will launch the same application using Docker Compose:

1. Create a new directory and inside that directory, create a `compose.yaml` file with the following contents:
  ```yaml
  services:
    app:
      image: docker/welcome-to-docker
      ports:
        - 8080:80
  ```
  The `ports` configuration accepts a few different forms of syntax for the port definition. In this case, you’re using the same `HOST_PORT:CONTAINER_PORT` used in the `docker run` command.
2. Open a terminal and navigate to the directory you created in the previous step.
3. Use the `docker compose up` command to start the application.
4. Open your browser to [http://localhost:8080](http://localhost:8080).

## Additional resources

If you’d like to dive in deeper on this topic, be sure to check out the following resources:

- [docker container portCLI reference](https://docs.docker.com/reference/cli/docker/container/port/)
- [Published ports](https://docs.docker.com/engine/network/#published-ports)

## Next steps

Now that you understand how to publish and expose ports, you're ready to learn how to override the container defaults using the `docker run` command.

[Overriding container defaults](https://docs.docker.com/get-started/docker-concepts/running-containers/overriding-container-defaults/)

---

# Sharing local files with containers

> This concept page will teach you the various storage options available in Docker and their common usage.

# Sharing local files with containers

   Table of contents

---

## Explanation

Each container has everything it needs to function with no reliance on any pre-installed dependencies on the host machine. Since containers run in isolation, they have minimal influence on the host and other containers. This isolation has a major benefit: containers minimize conflicts with the host system and other containers. However, this isolation also means containers can't directly access data on the host machine by default.

Consider a scenario where you have a web application container that requires access to configuration settings stored in a file on your host system. This file may contain sensitive data such as database credentials or API keys. Storing such sensitive information directly within the container image poses security risks, especially during image sharing. To address this challenge, Docker offers storage options that bridge the gap between container isolation and your host machine's data.

Docker offers two primary storage options for persisting data and sharing files between the host machine and containers: volumes and bind mounts.

### Volume versus bind mounts

If you want to ensure that data generated or modified inside the container persists even after the container stops running, you would opt for a volume. See
[Persisting container data](https://docs.docker.com/get-started/docker-concepts/running-containers/persisting-container-data/) to learn more about volumes and their use cases.

If you have specific files or directories on your host system that you want to directly share with your container, like configuration files or development code, then you would use a bind mount. It's like opening a direct portal between your host and container for sharing. Bind mounts are ideal for development environments where real-time file access and sharing between the host and container are crucial.

### Sharing files between a host and container

Both `-v` (or `--volume`) and `--mount` flags used with the `docker run` command let you share files or directories between your local machine (host) and a Docker container. However, there are some key differences in their behavior and usage.

The `-v` flag is simpler and more convenient for basic volume or bind mount operations. If the host location doesn’t exist when using `-v` or `--volume`, a directory will be automatically created.

Imagine you're a developer working on a project. You have a source directory on your development machine where your code resides. When you compile or build your code, the generated artifacts (compiled code, executables, images, etc.) are saved in a separate subdirectory within your source directory. In the following examples, this subdirectory is `/HOST/PATH`. Now you want these build artifacts to be accessible within a Docker container running your application. Additionally, you want the container to automatically access the latest build artifacts whenever you rebuild your code.

Here's a way to use `docker run` to start a container using a bind mount and map it to the container file location.

```console
$ docker run -v /HOST/PATH:/CONTAINER/PATH -it nginx
```

The `--mount` flag offers more advanced features and granular control, making it suitable for complex mount scenarios or production deployments. If you use `--mount` to bind-mount a file or directory that doesn't yet exist on the Docker host, the `docker run` command doesn't automatically create it for you but generates an error.

```console
$ docker run --mount type=bind,source=/HOST/PATH,target=/CONTAINER/PATH,readonly nginx
```

> Note
>
> Docker recommends using the `--mount` syntax instead of `-v`. It provides better control over the mounting process and avoids potential issues with missing directories.

### File permissions for Docker access to host files

When using bind mounts, it's crucial to ensure that Docker has the necessary permissions to access the host directory. To grant read/write access, you can use the `:ro` flag (read-only) or `:rw` (read-write) with the `-v` or `--mount` flag during container creation.
For example, the following command grants read-write access permission.

```console
$ docker run -v HOST-DIRECTORY:/CONTAINER-DIRECTORY:rw nginx
```

Read-only bind mounts let the container access the mounted files on the host for reading, but it can't change or delete the files. With read-write bind mounts, containers can modify or delete mounted files, and these changes or deletions will also be reflected on the host system. Read-only bind mounts ensures that files on the host can't be accidentally modified or deleted by a container.

> **Synchronized File Share**
>
>
>
> As your codebase grows larger, traditional methods of file sharing like bind mounts may become inefficient or slow, especially in development environments where frequent access to files is necessary.
> [Synchronized file shares](https://docs.docker.com/desktop/features/synchronized-file-sharing/) improve bind mount performance by leveraging synchronized filesystem caches. This optimization ensures that file access between the host and virtual machine (VM) is fast and efficient.

## Try it out

In this hands-on guide, you’ll practice how to create and use a bind mount to share files between a host and a container.

### Run a container

1. [Download and install](https://docs.docker.com/get-started/get-docker/) Docker Desktop.
2. Start a container using the [httpd](https://hub.docker.com/_/httpd) image with the following command:
  ```console
  $ docker run -d -p 8080:80 --name my_site httpd:2.4
  ```
  This will start the `httpd` service in the background, and publish the webpage to port `8080` on the host.
3. Open the browser and access [http://localhost:8080](http://localhost:8080) or use the curl command to verify if it's working fine or not.
  ```console
  $ curl localhost:8080
  ```

### Use a bind mount

Using a bind mount, you can map the configuration file on your host computer to a specific location within the container. In this example, you’ll see how to change the look and feel of the webpage by using bind mount:

1. Delete the existing container by using the Docker Desktop Dashboard:
  ![A screenshot of Docker Desktop Dashboard showing how to delete the httpd container](https://docs.docker.com/get-started/docker-concepts/running-containers/images/delete-httpd-container.webp)  ![A screenshot of Docker Desktop Dashboard showing how to delete the httpd container](https://docs.docker.com/get-started/docker-concepts/running-containers/images/delete-httpd-container.webp)
2. Create a new directory called `public_html` on your host system.
  ```console
  $ mkdir public_html
  ```
3. Navigate into the newly created directory `public_html` and create a file called `index.html` with the following content. This is a basic HTML document that creates a simple webpage that welcomes you with a friendly whale.
  ```html
  <!DOCTYPE html>
  <html lang="en">
  <head>
  <meta charset="UTF-8">
  <title> My Website with a Whale & Docker!</title>
  </head>
  <body>
  <h1>Whalecome!!</h1>
  <p>Look! There's a friendly whale greeting you!</p>
  <pre id="docker-art">
     ##         .
    ## ## ##        ==
   ## ## ## ## ##    ===
   /"""""""""""""""""\___/ ===
  {                       /  ===-
  \______ O           __/
  \    \         __/
   \____\_______/
  Hello from Docker!
  </pre>
  </body>
  </html>
  ```
4. It's time to run the container. The `--mount` and `-v` examples produce the same result. You can't run them both unless you remove the `my_site` container after running the first one.
  ```console
  $ docker run -d --name my_site -p 8080:80 -v .:/usr/local/apache2/htdocs/ httpd:2.4
  ```
  ```console
  $ docker run -d --name my_site -p 8080:80 --mount type=bind,source=./,target=/usr/local/apache2/htdocs/ httpd:2.4
  ```
  > Tip
  >
  > When using the `-v` or `--mount` flag in Windows PowerShell, you need to provide the absolute path to your directory instead of just `./`. This is because PowerShell handles relative paths differently from bash (commonly used in Mac and Linux environments).
  With everything now up and running, you should be able to access the site via [http://localhost:8080](http://localhost:8080) and find a new webpage that welcomes you with a friendly whale.

### Access the file on the Docker Desktop Dashboard

1. You can view the mounted files inside a container by selecting the container's **Files** tab and then selecting a file inside the `/usr/local/apache2/htdocs/` directory. Then, select **Open file editor**.
  ![A screenshot of Docker Desktop Dashboard showing the mounted files inside the a container](https://docs.docker.com/get-started/docker-concepts/running-containers/images/mounted-files.webp)  ![A screenshot of Docker Desktop Dashboard showing the mounted files inside the a container](https://docs.docker.com/get-started/docker-concepts/running-containers/images/mounted-files.webp)
2. Delete the file on the host and verify the file is also deleted in the container. You will find that the files no longer exist under **Files** in the Docker Desktop Dashboard.
  ![A screenshot of Docker Desktop Dashboard showing the deleted files inside the a container](https://docs.docker.com/get-started/docker-concepts/running-containers/images/deleted-files.webp)  ![A screenshot of Docker Desktop Dashboard showing the deleted files inside the a container](https://docs.docker.com/get-started/docker-concepts/running-containers/images/deleted-files.webp)
3. Recreate the HTML file on the host system and see that file re-appears under the **Files** tab under **Containers** on the Docker Desktop Dashboard. By now, you will be able to access the site too.

### Stop your container

The container continues to run until you stop it.

1. Go to the **Containers** view in the Docker Desktop Dashboard.
2. Locate the container you'd like to stop.
3. Select the **Stop** action in the Actions column.

## Additional resources

The following resources will help you learn more about bind mounts:

- [Manage data in Docker](https://docs.docker.com/storage/)
- [Volumes](https://docs.docker.com/storage/volumes/)
- [Bind mounts](https://docs.docker.com/storage/bind-mounts/)
- [Running containers](https://docs.docker.com/reference/run/)
- [Troubleshoot storage errors](https://docs.docker.com/storage/troubleshooting_volume_errors/)
- [Persisting container data](https://docs.docker.com/get-started/docker-concepts/running-containers/persisting-container-data/)

## Next steps

Now that you have learned about sharing local files with containers, it’s time to learn about multi-container applications.

[Multi-container applications](https://docs.docker.com/get-started/docker-concepts/running-containers/multi-container-applications/)

---

# What is a container?

> What is a container? This concept page will teach you about containers and provide a quick hands-on where you will run your first container.

# What is a container?

   Table of contents

---

## Explanation

Imagine you're developing a killer web app that has three main components - a React frontend, a Python API, and a PostgreSQL database. If you wanted to work on this project, you'd have to install Node, Python, and PostgreSQL.

How do you make sure you have the same versions as the other developers on your team? Or your CI/CD system? Or what's used in production?

How do you ensure the version of Python (or Node or the database) your app needs isn't affected by what's already on your machine? How do you manage potential conflicts?

Enter containers!

What is a container? Simply put, containers are isolated processes for each of your app's components. Each component - the frontend React app, the Python API engine, and the database - runs in its own isolated environment, completely isolated from everything else on your machine.

Here's what makes them awesome. Containers are:

- Self-contained. Each container has everything it needs to function with no reliance on any pre-installed dependencies on the host machine.
- Isolated. Since containers run in isolation, they have minimal influence on the host and other containers, increasing the security of your applications.
- Independent. Each container is independently managed. Deleting one container won't affect any others.
- Portable. Containers can run anywhere! The container that runs on your development machine will work the same way in a data center or anywhere in the cloud!

### Containers versus virtual machines (VMs)

Without getting too deep, a VM is an entire operating system with its own kernel, hardware drivers, programs, and applications. Spinning up a VM only to isolate a single application is a lot of overhead.

A container is simply an isolated process with all of the files it needs to run. If you run multiple containers, they all share the same kernel, allowing you to run more applications on less infrastructure.

> **Using VMs and containers together**
>
>
>
> Quite often, you will see containers and VMs used together. As an example, in a cloud environment, the provisioned machines are typically VMs. However, instead of provisioning one machine to run one application, a VM with a container runtime can run multiple containerized applications, increasing resource utilization and reducing costs.

## Try it out

In this hands-on, you will see how to run a Docker container using the Docker Desktop GUI.

Use the following instructions to run a container.

1. Open Docker Desktop and select the **Search** field on the top navigation bar.
2. Specify `welcome-to-docker` in the search input and then select the **Pull** button.
  ![A screenshot of the Docker Desktop Dashboard showing the search result for welcome-to-docker Docker image ](https://docs.docker.com/get-started/docker-concepts/the-basics/images/search-the-docker-image.webp)  ![A screenshot of the Docker Desktop Dashboard showing the search result for welcome-to-docker Docker image ](https://docs.docker.com/get-started/docker-concepts/the-basics/images/search-the-docker-image.webp)
3. Once the image is successfully pulled, select the **Run** button.
4. Expand the **Optional settings**.
5. In the **Container name**, specify `welcome-to-docker`.
6. In the **Host port**, specify `8080`.
  ![A screenshot of Docker Desktop Dashboard showing the container run dialog with welcome-to-docker typed in as the container name and 8080 specified as the port number](https://docs.docker.com/get-started/docker-concepts/the-basics/images/run-a-new-container.webp)  ![A screenshot of Docker Desktop Dashboard showing the container run dialog with welcome-to-docker typed in as the container name and 8080 specified as the port number](https://docs.docker.com/get-started/docker-concepts/the-basics/images/run-a-new-container.webp)
7. Select **Run** to start your container.

Congratulations! You just ran your first container! 🎉

### View your container

You can view all of your containers by going to the **Containers** view of the Docker Desktop Dashboard.

![Screenshot of the container view of the Docker Desktop GUI showing the welcome-to-docker container running on the host port 8080](https://docs.docker.com/get-started/docker-concepts/the-basics/images/view-your-containers.webp)  ![Screenshot of the container view of the Docker Desktop GUI showing the welcome-to-docker container running on the host port 8080](https://docs.docker.com/get-started/docker-concepts/the-basics/images/view-your-containers.webp)

This container runs a web server that displays a simple website. When working with more complex projects, you'll run different parts in different containers. For example, you might run a different container for the frontend, backend, and database.

### Access the frontend

When you launched the container, you exposed one of the container's ports onto your machine. Think of this as creating configuration to let you to connect through the isolated environment of the container.

For this container, the frontend is accessible on port `8080`. To open the website, select the link in the **Port(s)** column of your container or visit [http://localhost:8080](http://localhost:8080) in your browser.

![Screenshot of the landing page coming from the running container](https://docs.docker.com/get-started/docker-concepts/the-basics/images/access-the-frontend.webp)  ![Screenshot of the landing page coming from the running container](https://docs.docker.com/get-started/docker-concepts/the-basics/images/access-the-frontend.webp)

### Explore your container

Docker Desktop lets you explore and interact with different aspects of your container. Try it out yourself.

1. Go to the **Containers** view in the Docker Desktop Dashboard.
2. Select your container.
3. Select the **Files** tab to explore your container's isolated file system.
  ![Screenshot of the Docker Desktop Dashboard showing the files and directories inside a running container](https://docs.docker.com/get-started/docker-concepts/the-basics/images/explore-your-container.webp)  ![Screenshot of the Docker Desktop Dashboard showing the files and directories inside a running container](https://docs.docker.com/get-started/docker-concepts/the-basics/images/explore-your-container.webp)

### Stop your container

The `docker/welcome-to-docker` container continues to run until you stop it.

1. Go to the **Containers** view in the Docker Desktop Dashboard.
2. Locate the container you'd like to stop.
3. Select the **Stop** action in the **Actions** column.
  ![Screenshot of the Docker Desktop Dashboard with the welcome container selected and being prepared to stop](https://docs.docker.com/get-started/docker-concepts/the-basics/images/stop-your-container.webp)  ![Screenshot of the Docker Desktop Dashboard with the welcome container selected and being prepared to stop](https://docs.docker.com/get-started/docker-concepts/the-basics/images/stop-your-container.webp)

Follow the instructions to run a container using the CLI:

1. Open your CLI terminal and start a container by using the
  [docker run](https://docs.docker.com/reference/cli/docker/container/run/) command:
  ```console
  $ docker run -d -p 8080:80 docker/welcome-to-docker
  ```
  The output from this command is the full container ID.

Congratulations! You just fired up your first container! 🎉

### View your running containers

You can verify if the container is up and running by using the
[docker ps](https://docs.docker.com/reference/cli/docker/container/ls/) command:

```console
docker ps
```

You will see output like the following:

```console
CONTAINER ID   IMAGE                      COMMAND                  CREATED          STATUS          PORTS                      NAMES
 a1f7a4bb3a27   docker/welcome-to-docker   "/docker-entrypoint.…"   11 seconds ago   Up 11 seconds   0.0.0.0:8080->80/tcp       gracious_keldysh
```

This container runs a web server that displays a simple website. When working with more complex projects, you'll run different parts in different containers. For example, a different container for the `frontend`, `backend`, and `database`.

> Tip
>
> The `docker ps` command will show you *only* running containers. To view stopped containers, add the `-a` flag to list all containers: `docker ps -a`

### Access the frontend

When you launched the container, you exposed one of the container's ports onto your machine. Think of this as creating configuration to let you to connect through the isolated environment of the container.

For this container, the frontend is accessible on port `8080`. To open the website, select the link in the **Port(s)** column of your container or visit [http://localhost:8080](http://localhost:8080) in your browser.

![Screenshot of the landing page of the Nginx web server, coming from the running container](https://docs.docker.com/get-started/docker-concepts/the-basics/images/access-the-frontend.webp)  ![Screenshot of the landing page of the Nginx web server, coming from the running container](https://docs.docker.com/get-started/docker-concepts/the-basics/images/access-the-frontend.webp)

### Stop your container

The `docker/welcome-to-docker` container continues to run until you stop it. You can stop a container using the `docker stop` command.

1. Run `docker ps` to get the ID of the container
2. Provide the container ID or name to the
  [docker stop](https://docs.docker.com/reference/cli/docker/container/stop/) command:
  ```console
  docker stop <the-container-id>
  ```

> Tip
>
> When referencing containers by ID, you don't need to provide the full ID. You only need to provide enough of the ID to make it unique. As an example, the previous container could be stopped by running the following command:
>
>
>
> ```console
> docker stop a1f
> ```

## Additional resources

The following links provide additional guidance into containers:

- [Running a container](https://docs.docker.com/engine/containers/run/)
- [Overview of container](https://www.docker.com/resources/what-container/)
- [Why Docker?](https://www.docker.com/why-docker/)

## Next steps

Now that you have learned the basics of a Docker container, it's time to learn about Docker images.

[What is an image?](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-an-image/)

---

# What is a registry?

> What is a registry? This Docker Concept will explain what a registry is, explore their interoperability, and have you interact with registries.

# What is a registry?

   Table of contents

---

## Explanation

Now that you know what a container image is and how it works, you might wonder - where do you store these images?

Well, you can store your container images on your computer system, but what if you want to share them with your friends or use them on another machine? That's where the image registry comes in.

An image registry is a centralized location for storing and sharing your container images. It can be either public or private. [Docker Hub](https://hub.docker.com) is a public registry that anyone can use and is the default registry.

While Docker Hub is a popular option, there are many other available container registries available today, including [Amazon Elastic Container Registry (ECR)](https://aws.amazon.com/ecr/), [Azure Container Registry (ACR)](https://azure.microsoft.com/en-in/products/container-registry), and [Google Container Registry (GCR)](https://cloud.google.com/artifact-registry). You can even run your private registry on your local system or inside your organization. For example, Harbor, JFrog Artifactory, GitLab Container registry etc.

### Registry vs. repository

While you're working with registries, you might hear the terms *registry* and *repository* as if they're interchangeable. Even though they're related, they're not quite the same thing.

A *registry* is a centralized location that stores and manages container images, whereas a *repository* is a collection of related container images within a registry. Think of it as a folder where you organize your images based on projects. Each repository contains one or more container images.

The following diagram shows the relationship between a registry, repositories, and images.

> Note
>
> You can create one private repository and unlimited public repositories using the free version of Docker Hub. For more information, visit the [Docker Hub subscription page](https://www.docker.com/pricing/).

## Try it out

In this hands-on, you will learn how to build and push a Docker image to the Docker Hub repository.

### Sign up for a free Docker account

1. If you haven't created one yet, head over to the [Docker Hub](https://hub.docker.com) page to sign up for a new Docker account. Be sure to finish the verification steps sent to your email.
  ![Screenshot of the official Docker Hub page showing the Sign up page](https://docs.docker.com/get-started/docker-concepts/the-basics/images/dockerhub-signup.webp)  ![Screenshot of the official Docker Hub page showing the Sign up page](https://docs.docker.com/get-started/docker-concepts/the-basics/images/dockerhub-signup.webp)
  You can use your Google or GitHub account to authenticate.

### Create your first repository

1. Sign in to [Docker Hub](https://hub.docker.com).
2. Select the **Create repository** button in the top-right corner.
3. Select your namespace (most likely your username) and enter `docker-quickstart` as the repository name.
  ![Screenshot of the Docker Hub page that shows how to create a public repository](https://docs.docker.com/get-started/docker-concepts/the-basics/images/create-hub-repository.webp)  ![Screenshot of the Docker Hub page that shows how to create a public repository](https://docs.docker.com/get-started/docker-concepts/the-basics/images/create-hub-repository.webp)
4. Set the visibility to **Public**.
5. Select the **Create** button to create the repository.

That's it. You've successfully created your first repository. 🎉

This repository is empty right now. You'll now fix this by pushing an image to it.

### Sign in with Docker Desktop

1. [Download and install](https://www.docker.com/products/docker-desktop/) Docker Desktop, if not already installed.
2. In the Docker Desktop GUI, select the **Sign in** button in the top-right corner

### Clone sample Node.js code

In order to create an image, you first need a project. To get you started quickly, you'll use a sample Node.js project found at [github.com/dockersamples/helloworld-demo-node](https://github.com/dockersamples/helloworld-demo-node). This repository contains a pre-built Dockerfile necessary for building a Docker image.

Don't worry about the specifics of the Dockerfile, as you'll learn about that in later sections.

1. Clone the GitHub repository using the following command:
  ```console
  git clone https://github.com/dockersamples/helloworld-demo-node
  ```
2. Navigate into the newly created directory.
  ```console
  cd helloworld-demo-node
  ```
3. Run the following command to build a Docker image, swapping out `YOUR_DOCKER_USERNAME` with your username.
  ```console
  docker build -t YOUR_DOCKER_USERNAME/docker-quickstart .
  ```
  > Note
  >
  > Make sure you include the dot (.) at the end of the `docker build` command. This tells Docker where to find the Dockerfile.
4. Run the following command to list the newly created Docker image:
  ```console
  docker images
  ```
  You will see output like the following:
  ```console
  REPOSITORY                                 TAG       IMAGE ID       CREATED         SIZE
  YOUR_DOCKER_USERNAME/docker-quickstart   latest    476de364f70e   2 minutes ago   170MB
  ```
5. Start a container to test the image by running the following command (swap out the username with your own username):
  ```console
  docker run -d -p 8080:8080 YOUR_DOCKER_USERNAME/docker-quickstart
  ```
  You can verify if the container is working by visiting [http://localhost:8080](http://localhost:8080) with your browser.
6. Use the
  [docker tag](https://docs.docker.com/reference/cli/docker/image/tag/) command to tag the Docker image. Docker tags allow you to label and version your images.
  ```console
  docker tag YOUR_DOCKER_USERNAME/docker-quickstart YOUR_DOCKER_USERNAME/docker-quickstart:1.0
  ```
7. Finally, it's time to push the newly built image to your Docker Hub repository by using the
  [docker push](https://docs.docker.com/reference/cli/docker/image/push/) command:
  ```console
  docker push YOUR_DOCKER_USERNAME/docker-quickstart:1.0
  ```
8. Open [Docker Hub](https://hub.docker.com) and navigate to your repository. Navigate to the **Tags** section and see your newly pushed image.
  ![Screenshot of the Docker Hub page that displays the newly added image tag](https://docs.docker.com/get-started/docker-concepts/the-basics/images/dockerhub-tags.webp)  ![Screenshot of the Docker Hub page that displays the newly added image tag](https://docs.docker.com/get-started/docker-concepts/the-basics/images/dockerhub-tags.webp)

In this walkthrough, you signed up for a Docker account, created your first Docker Hub repository, and built, tagged, and pushed a container image to your Docker Hub repository.

## Additional resources

- [Docker Hub Quickstart](https://docs.docker.com/docker-hub/quickstart/)
- [Manage Docker Hub Repositories](https://docs.docker.com/docker-hub/repos/)

## Next steps

Now that you understand the basics of containers and images, you're ready to learn about Docker Compose.

[What is Docker Compose?](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-docker-compose/)

---

# What is an image?

> What is an image

# What is an image?

   Table of contents

---

## Explanation

Seeing as a [container](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/) is an isolated process, where does it get its files and configuration? How do you share those environments?

That's where container images come in. A container image is a standardized package that includes all of the files, binaries, libraries, and configurations to run a container.

For a [PostgreSQL](https://hub.docker.com/_/postgres) image, that image will package the database binaries, config files, and other dependencies. For a Python web app, it'll include the Python runtime, your app code, and all of its dependencies.

There are two important principles of images:

1. Images are immutable. Once an image is created, it can't be modified. You can only make a new image or add changes on top of it.
2. Container images are composed of layers. Each layer represents a set of file system changes that add, remove, or modify files.

These two principles let you to extend or add to existing images. For example, if you are building a Python app, you can start from the [Python image](https://hub.docker.com/_/python) and add additional layers to install your app's dependencies and add your code. This lets you focus on your app, rather than Python itself.

### Finding images

[Docker Hub](https://hub.docker.com) is the default global marketplace for storing and distributing images. It has over 100,000 images created by developers that you can run locally. You can search for Docker Hub images and run them directly from Docker Desktop.

Docker Hub provides a variety of Docker-supported and endorsed images known as Docker Trusted Content. These provide fully managed services or great starters for your own images. These include:

- [Docker Official Images](https://hub.docker.com/search?badges=official) - a curated set of Docker repositories, serve as the starting point for the majority of users, and are some of the most secure on Docker Hub
- [Docker Hardened Images](https://hub.docker.com/hardened-images/catalog) - minimal, secure, production-ready images with near-zero CVEs, designed to reduce attack surface and simplify compliance. Free and open source under Apache 2.0
- [Docker Verified Publishers](https://hub.docker.com/search?badges=verified_publisher) - high-quality images from commercial publishers verified by Docker
- [Docker-Sponsored Open Source](https://hub.docker.com/search?badges=open_source) - images published and maintained by open-source projects sponsored by Docker through Docker's open source program

For example, [Redis](https://hub.docker.com/_/redis) and [Memcached](https://hub.docker.com/_/memcached) are a few popular ready-to-go Docker Official Images. You can download these images and have these services up and running in a matter of seconds. There are also base images, like the [Node.js](https://hub.docker.com/_/node) Docker image, that you can use as a starting point and add your own files and configurations. For production workloads requiring enhanced security, Docker Hardened Images offer minimal variants of popular images like Node.js, Python, and Go.

## Try it out

In this hands-on, you will learn how to search and pull a container image using the Docker Desktop GUI.

### Search for and download an image

1. Open the Docker Desktop Dashboard and select the **Images** view in the left-hand navigation menu.
  ![A screenshot of the Docker Desktop Dashboard showing the image view on the left sidebar](https://docs.docker.com/get-started/docker-concepts/the-basics/images/click-image.webp)  ![A screenshot of the Docker Desktop Dashboard showing the image view on the left sidebar](https://docs.docker.com/get-started/docker-concepts/the-basics/images/click-image.webp)
2. Select the **Search images to run** button. If you don't see it, select the *global search bar* at the top of the screen.
  ![A screenshot of the Docker Desktop Dashboard showing the search ta](https://docs.docker.com/get-started/docker-concepts/the-basics/images/search-image.webp)  ![A screenshot of the Docker Desktop Dashboard showing the search ta](https://docs.docker.com/get-started/docker-concepts/the-basics/images/search-image.webp)
3. In the **Search** field, enter "welcome-to-docker". Once the search has completed, select the `docker/welcome-to-docker` image.
  ![A screenshot of the Docker Desktop Dashboard showing the search results for the docker/welcome-to-docker image](https://docs.docker.com/get-started/docker-concepts/the-basics/images/select-image.webp)  ![A screenshot of the Docker Desktop Dashboard showing the search results for the docker/welcome-to-docker image](https://docs.docker.com/get-started/docker-concepts/the-basics/images/select-image.webp)
4. Select **Pull** to download the image.

### Learn about the image

Once you have an image downloaded, you can learn quite a few details about the image either through the GUI or the CLI.

1. In the Docker Desktop Dashboard, select the **Images** view.
2. Select the **docker/welcome-to-docker** image to open details about the image.
  ![A screenshot of the Docker Desktop Dashboard showing the images view with an arrow pointing to the docker/welcome-to-docker image](https://docs.docker.com/get-started/docker-concepts/the-basics/images/pulled-image.webp)  ![A screenshot of the Docker Desktop Dashboard showing the images view with an arrow pointing to the docker/welcome-to-docker image](https://docs.docker.com/get-started/docker-concepts/the-basics/images/pulled-image.webp)
3. The image details page presents you with information regarding the layers of the image, the packages and libraries installed in the image, and any discovered vulnerabilities.
  ![A screenshot of the image details view for the docker/welcome-to-docker image](https://docs.docker.com/get-started/docker-concepts/the-basics/images/image-layers.webp)  ![A screenshot of the image details view for the docker/welcome-to-docker image](https://docs.docker.com/get-started/docker-concepts/the-basics/images/image-layers.webp)

Follow the instructions to search and pull a Docker image using CLI to view its layers.

### Search for and download an image

1. Open a terminal and search for images using the
  [docker search](https://docs.docker.com/reference/cli/docker/search/) command:
  ```console
  docker search docker/welcome-to-docker
  ```
  You will see output like the following:
  ```console
  NAME                       DESCRIPTION                                     STARS     OFFICIAL
  docker/welcome-to-docker   Docker image for new users getting started w…   20
  ```
  This output shows you information about relevant images available on Docker Hub.
2. Pull the image using the
  [docker pull](https://docs.docker.com/reference/cli/docker/image/pull/) command.
  ```console
  docker pull docker/welcome-to-docker
  ```
  You will see output like the following:
  ```console
  Using default tag: latest
  latest: Pulling from docker/welcome-to-docker
  579b34f0a95b: Download complete
  d11a451e6399: Download complete
  1c2214f9937c: Download complete
  b42a2f288f4d: Download complete
  54b19e12c655: Download complete
  1fb28e078240: Download complete
  94be7e780731: Download complete
  89578ce72c35: Download complete
  Digest: sha256:eedaff45e3c78538087bdd9dc7afafac7e110061bbdd836af4104b10f10ab693
  Status: Downloaded newer image for docker/welcome-to-docker:latest
  docker.io/docker/welcome-to-docker:latest
  ```
  Each of line represents a different downloaded layer of the image. Remember that each layer is a set of filesystem changes and provides functionality of the image.

### Learn about the image

1. List your downloaded images using the
  [docker image ls](https://docs.docker.com/reference/cli/docker/image/ls/) command:
  ```console
  docker image ls
  ```
  You will see output like the following:
  ```console
  REPOSITORY                 TAG       IMAGE ID       CREATED        SIZE
  docker/welcome-to-docker   latest    eedaff45e3c7   4 months ago   29.7MB
  ```
  The command shows a list of Docker images currently available on your system. The `docker/welcome-to-docker` has a total size of approximately 29.7MB.
  > **Image size**
  >
  >
  >
  > The image size represented here reflects the uncompressed size of the image, not the download size of the layers.
2. List the image's layers using the
  [docker image history](https://docs.docker.com/reference/cli/docker/image/history/) command:
  ```console
  docker image history docker/welcome-to-docker
  ```
  You will see output like the following:
  ```console
  IMAGE          CREATED        CREATED BY                                      SIZE      COMMENT
  648f93a1ba7d   4 months ago   COPY /app/build /usr/share/nginx/html # buil…   1.6MB     buildkit.dockerfile.v0
  <missing>      5 months ago   /bin/sh -c #(nop)  CMD ["nginx" "-g" "daemon…   0B
  <missing>      5 months ago   /bin/sh -c #(nop)  STOPSIGNAL SIGQUIT           0B
  <missing>      5 months ago   /bin/sh -c #(nop)  EXPOSE 80                    0B
  <missing>      5 months ago   /bin/sh -c #(nop)  ENTRYPOINT ["/docker-entr…   0B
  <missing>      5 months ago   /bin/sh -c #(nop) COPY file:9e3b2b63db9f8fc7…   4.62kB
  <missing>      5 months ago   /bin/sh -c #(nop) COPY file:57846632accc8975…   3.02kB
  <missing>      5 months ago   /bin/sh -c #(nop) COPY file:3b1b9915b7dd898a…   298B
  <missing>      5 months ago   /bin/sh -c #(nop) COPY file:caec368f5a54f70a…   2.12kB
  <missing>      5 months ago   /bin/sh -c #(nop) COPY file:01e75c6dd0ce317d…   1.62kB
  <missing>      5 months ago   /bin/sh -c set -x     && addgroup -g 101 -S …   9.7MB
  <missing>      5 months ago   /bin/sh -c #(nop)  ENV PKG_RELEASE=1            0B
  <missing>      5 months ago   /bin/sh -c #(nop)  ENV NGINX_VERSION=1.25.3     0B
  <missing>      5 months ago   /bin/sh -c #(nop)  LABEL maintainer=NGINX Do…   0B
  <missing>      5 months ago   /bin/sh -c #(nop)  CMD ["/bin/sh"]              0B
  <missing>      5 months ago   /bin/sh -c #(nop) ADD file:ff3112828967e8004…   7.66MB
  ```
  This output shows you all of the layers, their sizes, and the command used to create the layer.
  > **Viewing the full command**
  >
  >
  >
  > If you add the `--no-trunc` flag to the command, you will see the full command. Note that, since the output is in a table-like format, longer commands will cause the output to be very difficult to navigate.

In this walkthrough, you searched and pulled a Docker image. In addition to pulling a Docker image, you also learned about the layers of a Docker Image.

## Additional resources

The following resources will help you learn more about exploring, finding, and building images:

- [Docker trusted content](https://docs.docker.com/docker-hub/image-library/trusted-content/)
- [Explore the Image view in Docker Desktop](https://docs.docker.com/desktop/use-desktop/images/)
- [Docker Build overview](https://docs.docker.com/build/concepts/overview/)
- [Docker Hub](https://hub.docker.com)

## Next steps

Now that you have learned the basics of images, it's time to learn about distributing images through registries.

[What is a registry?](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-registry/)
