# What is Docker Compose? and more

# What is Docker Compose?

> What is Docker Compose?

# What is Docker Compose?

   Table of contents

---

## Explanation

If you've been following the guides so far, you've been working with single container applications. But, now you're wanting to do something more complicated - run databases, message queues, caches, or a variety of other services. Do you install everything in a single container? Run multiple containers? If you run multiple, how do you connect them all together?

One best practice for containers is that each container should do one thing and do it well. While there are exceptions to this rule, avoid the tendency to have one container do multiple things.

You can use multiple `docker run` commands to start multiple containers. But, you'll soon realize you'll need to manage networks, all of the flags needed to connect containers to those networks, and more. And when you're done, cleanup is a little more complicated.

With Docker Compose, you can define all of your containers and their configurations in a single YAML file. If you include this file in your code repository, anyone that clones your repository can get up and running with a single command.

It's important to understand that Compose is a declarative tool - you simply define it and go. You don't always need to recreate everything from scratch. If you make a change, run `docker compose up` again and Compose will reconcile the changes in your file and apply them intelligently.

> **Dockerfile versus Compose file**
>
>
>
> A Dockerfile provides instructions to build a container image while a Compose file defines your running containers. Quite often, a Compose file references a Dockerfile to build an image to use for a particular service.

## Try it out

In this hands-on, you will learn how to use a Docker Compose to run a multi-container application. You'll use a simple to-do list app built with Node.js and MySQL as a database server.

### Start the application

Follow the instructions to run the to-do list app on your system.

1. [Download and install](https://www.docker.com/products/docker-desktop/) Docker Desktop.
2. Open a terminal and [clone this sample application](https://github.com/dockersamples/todo-list-app).
  ```console
  git clone https://github.com/dockersamples/todo-list-app
  ```
3. Navigate into the `todo-list-app` directory:
  ```console
  cd todo-list-app
  ```
  Inside this directory, you'll find a file named `compose.yaml`. This YAML file is where all the magic happens! It defines all the services that make up your application, along with their configurations. Each service specifies its image, ports, volumes, networks, and any other settings necessary for its functionality. Take some time to explore the YAML file and familiarize yourself with its structure.
4. Use the
  [docker compose up](https://docs.docker.com/reference/cli/docker/compose/up/) command to start the application:
  ```console
  docker compose up -d --build
  ```
  When you run this command, you should see an output like this:
  ```console
  [+] Running 5/5
  ✔ app 3 layers [⣿⣿⣿]      0B/0B            Pulled          7.1s
    ✔ e6f4e57cc59e Download complete                          0.9s
    ✔ df998480d81d Download complete                          1.0s
    ✔ 31e174fedd23 Download complete                          2.5s
    ✔ 43c47a581c29 Download complete                          2.0s
  [+] Running 4/4
    ⠸ Network todo-list-app_default           Created         0.3s
    ⠸ Volume "todo-list-app_todo-mysql-data"  Created         0.3s
    ✔ Container todo-list-app-app-1           Started         0.3s
    ✔ Container todo-list-app-mysql-1         Started         0.3s
  ```
  A lot happened here! A couple of things to call out:
  - Two container images were downloaded from Docker Hub - node and MySQL
  - A network was created for your application
  - A volume was created to persist the database files between container restarts
  - Two containers were started with all of their necessary config
  If this feels overwhelming, don't worry! You'll get there!
5. With everything now up and running, you can open [http://localhost:3000](http://localhost:3000) in your browser to see the site. Note that the application may take 10-15 seconds to fully start. If the page doesn't load right away, wait a moment and refresh. Feel free to add items to the list, check them off, and remove them.
  ![A screenshot of a webpage showing the todo-list application running on port 3000](https://docs.docker.com/get-started/docker-concepts/the-basics/images/todo-list-app.webp)  ![A screenshot of a webpage showing the todo-list application running on port 3000](https://docs.docker.com/get-started/docker-concepts/the-basics/images/todo-list-app.webp)
6. If you look at the Docker Desktop GUI, you can see the containers and dive deeper into their configuration.
  ![A screenshot of Docker Desktop dashboard showing the list of containers running todo-list app](https://docs.docker.com/get-started/docker-concepts/the-basics/images/todo-list-containers.webp)  ![A screenshot of Docker Desktop dashboard showing the list of containers running todo-list app](https://docs.docker.com/get-started/docker-concepts/the-basics/images/todo-list-containers.webp)

### Tear it down

Since this application was started using Docker Compose, it's easy to tear it all down when you're done.

1. In the CLI, use the
  [docker compose down](https://docs.docker.com/reference/cli/docker/compose/down/) command to remove everything:
  ```console
  docker compose down
  ```
  You'll see output similar to the following:
  ```console
  [+] Running 3/3
  ✔ Container todo-list-app-mysql-1  Removed        2.9s
  ✔ Container todo-list-app-app-1    Removed        0.1s
  ✔ Network todo-list-app_default    Removed        0.1s
  ```
  > **Volume persistence**
  >
  >
  >
  > By default, volumes *aren't* automatically removed when you tear down a Compose stack. The idea is that you might want the data back if you start the stack again.
  >
  >
  >
  > If you do want to remove the volumes, add the `--volumes` flag when running the `docker compose down` command:
  >
  >
  >
  > ```console
  > docker compose down --volumes
  > [+] Running 1/0
  > ✔ Volume todo-list-app_todo-mysql-data  Removed
  > ```
2. Alternatively, you can use the Docker Desktop GUI to remove the containers by selecting the application stack and selecting the **Delete** button.
  ![A screenshot of the Docker Desktop GUI showing the containers view with an arrow pointing to the "Delete" button](https://docs.docker.com/get-started/docker-concepts/the-basics/images/todo-list-delete.webp)  ![A screenshot of the Docker Desktop GUI showing the containers view with an arrow pointing to the "Delete" button](https://docs.docker.com/get-started/docker-concepts/the-basics/images/todo-list-delete.webp)
  > **Using the GUI for Compose stacks**
  >
  >
  >
  > Note that if you remove the containers for a Compose app in the GUI, it's removing only the containers. You'll have to manually remove the network and volumes if you want to do so.

In this walkthrough, you learned how to use Docker Compose to start and stop a multi-container application.

## Additional resources

This page was a brief introduction to Compose. In the following resources, you can dive deeper into Compose and how to write Compose files.

- [Overview of Docker Compose](https://docs.docker.com/compose/)
- [Overview of Docker Compose CLI](https://docs.docker.com/compose/reference/)
- [How Compose works](https://docs.docker.com/compose/intro/compose-application-model/)

---

# What is Docker?

> Get an in-depth overview of the Docker platform including what it can be used for, the architecture it employs, and its underlying technology.

# What is Docker?

   Table of contents

---

Docker is an open platform for developing, shipping, and running applications.
Docker enables you to separate your applications from your infrastructure so
you can deliver software quickly. With Docker, you can manage your infrastructure
in the same ways you manage your applications. By taking advantage of Docker's
methodologies for shipping, testing, and deploying code, you can
significantly reduce the delay between writing code and running it in production.

## The Docker platform

Docker provides the ability to package and run an application in a loosely isolated
environment called a container. The isolation and security lets you run many
containers simultaneously on a given host. Containers are lightweight and contain
everything needed to run the application, so you don't need to rely on what's
installed on the host. You can share containers while you work,
and be sure that everyone you share with gets the same container that works in the
same way.

Docker provides tooling and a platform to manage the lifecycle of your containers:

- Develop your application and its supporting components using containers.
- The container becomes the unit for distributing and testing your application.
- When you're ready, deploy your application into your production environment,
  as a container or an orchestrated service. This works the same whether your
  production environment is a local data center, a cloud provider, or a hybrid
  of the two.

## What can I use Docker for?

### Fast, consistent delivery of your applications

Docker streamlines the development lifecycle by allowing developers to work in
standardized environments using local containers which provide your applications
and services. Containers are great for continuous integration and continuous
delivery (CI/CD) workflows.

Consider the following example scenario:

- Your developers write code locally and share their work with their colleagues
  using Docker containers.
- They use Docker to push their applications into a test environment and run
  automated and manual tests.
- When developers find bugs, they can fix them in the development environment
  and redeploy them to the test environment for testing and validation.
- When testing is complete, getting the fix to the customer is as simple as
  pushing the updated image to the production environment.

### Responsive deployment and scaling

Docker's container-based platform allows for highly portable workloads. Docker
containers can run on a developer's local laptop, on physical or virtual
machines in a data center, on cloud providers, or in a mixture of environments.

Docker's portability and lightweight nature also make it easy to dynamically
manage workloads, scaling up or tearing down applications and services as
business needs dictate, in near real time.

### Running more workloads on the same hardware

Docker is lightweight and fast. It provides a viable, cost-effective alternative
to hypervisor-based virtual machines, so you can use more of your server
capacity to achieve your business goals. Docker is perfect for high density
environments and for small and medium deployments where you need to do more with
fewer resources.

## Docker architecture

Docker uses a client-server architecture. The Docker client talks to the
Docker daemon, which does the heavy lifting of building, running, and
distributing your Docker containers. The Docker client and daemon can
run on the same system, or you can connect a Docker client to a remote Docker
daemon. The Docker client and daemon communicate using a REST API, over UNIX
sockets or a network interface. Another Docker client is Docker Compose,
that lets you work with applications consisting of a set of containers.

![Docker Architecture diagram](https://docs.docker.com/get-started/images/docker-architecture.webp)  ![Docker Architecture diagram](https://docs.docker.com/get-started/images/docker-architecture.webp)

### The Docker daemon

The Docker daemon (`dockerd`) listens for Docker API requests and manages Docker
objects such as images, containers, networks, and volumes. A daemon can also
communicate with other daemons to manage Docker services.

### The Docker client

The Docker client (`docker`) is the primary way that many Docker users interact
with Docker. When you use commands such as `docker run`, the client sends these
commands to `dockerd`, which carries them out. The `docker` command uses the
Docker API. The Docker client can communicate with more than one daemon.

### Docker Desktop

Docker Desktop is an easy-to-install application for your Mac, Windows, or Linux environment that enables you to build and share containerized applications and microservices. Docker Desktop includes the Docker daemon (`dockerd`), the Docker client (`docker`), Docker Compose, Docker Content Trust, Kubernetes, and Credential Helper. For more information, see
[Docker Desktop](https://docs.docker.com/desktop/).

### Docker registries

A Docker registry stores Docker images. Docker Hub is a public
registry that anyone can use, and Docker looks for images on
Docker Hub by default. You can even run your own private registry.

When you use the `docker pull` or `docker run` commands, Docker pulls the required images from your configured registry. When you use the `docker push` command, Docker pushes
your image to your configured registry.

### Docker objects

When you use Docker, you are creating and using images, containers, networks,
volumes, plugins, and other objects. This section is a brief overview of some
of those objects.

#### Images

An image is a read-only template with instructions for creating a Docker
container. Often, an image is based on another image, with some additional
customization. For example, you may build an image that is based on the Ubuntu image
but includes the Apache web server and your application, as well as the
configuration details needed to make your application run.

You might create your own images or you might only use those created by others
and published in a registry. To build your own image, you create a Dockerfile
with a simple syntax for defining the steps needed to create the image and run
it. Each instruction in a Dockerfile creates a layer in the image. When you
change the Dockerfile and rebuild the image, only those layers which have
changed are rebuilt. This is part of what makes images so lightweight, small,
and fast, when compared to other virtualization technologies.

#### Containers

A container is a runnable instance of an image. You can create, start, stop,
move, or delete a container using the Docker API or CLI. You can connect a
container to one or more networks, attach storage to it, or even create a new
image based on its current state.

By default, a container is relatively well isolated from other containers and
its host machine. You can control how isolated a container's network, storage,
or other underlying subsystems are from other containers or from the host
machine.

A container is defined by its image as well as any configuration options you
provide to it when you create or start it. When a container is removed, any changes to
its state that aren't stored in persistent storage disappear.

##### Exampledocker runcommand

The following command runs an `ubuntu` container, attaches interactively to your
local command-line session, and runs `/bin/bash`.

```console
$ docker run -i -t ubuntu /bin/bash
```

When you run this command, the following happens (assuming you are using
the default registry configuration):

1. If you don't have the `ubuntu` image locally, Docker pulls it from your
  configured registry, as though you had run `docker pull ubuntu` manually.
2. Docker creates a new container, as though you had run a `docker container create`
  command manually.
3. Docker allocates a read-write filesystem to the container, as its final
  layer. This allows a running container to create or modify files and
  directories in its local filesystem.
4. Docker creates a network interface to connect the container to the default
  network, since you didn't specify any networking options. This includes
  assigning an IP address to the container. By default, containers can
  connect to external networks using the host machine's network connection.
5. Docker starts the container and executes `/bin/bash`. Because the container
  is running interactively and attached to your terminal (due to the `-i` and `-t`
  flags), you can provide input using your keyboard while Docker logs the output to
  your terminal.
6. When you run `exit` to terminate the `/bin/bash` command, the container
  stops but isn't removed. You can start it again or remove it.

## The underlying technology

Docker is written in the [Go programming language](https://golang.org/) and takes
advantage of several features of the Linux kernel to deliver its functionality.
Docker uses a technology called `namespaces` to provide the isolated workspace
called the container. When you run a container, Docker creates a set of
namespaces for that container.

These namespaces provide a layer of isolation. Each aspect of a container runs
in a separate namespace and its access is limited to that namespace.

## Next steps

- [Install Docker](https://docs.docker.com/get-started/get-docker/)
- [Get started with Docker](https://docs.docker.com/get-started/introduction/)

---

# Get Docker

> Download and install Docker on the platform of your choice, including Mac, Linux, or Windows.

# Get Docker

---

Docker is an open platform for developing, shipping, and running applications.

Docker allows you to separate your applications from your infrastructure so you
can deliver software quickly. With Docker, you can manage your infrastructure in
the same ways you manage your applications.

By taking advantage of Docker’s
methodologies for shipping, testing, and deploying code quickly, you can
significantly reduce the delay between writing code and running it in production.

You can download and install Docker on multiple platforms. Refer to the following
section and choose the best installation path for you.

> **Docker Desktop terms**
>
>
>
> Commercial use of Docker Desktop in larger enterprises (more than 250
> employees OR more than $10 million USD in annual revenue) requires a [paid
> subscription](https://www.docker.com/pricing/).

[Docker Desktop for MacA native application using the macOS sandbox security model that delivers all Docker tools to your Mac.](https://docs.docker.com/desktop/setup/install/mac-install/)[Docker Desktop for WindowsA native Windows application that delivers all Docker tools to your Windows computer.](https://docs.docker.com/desktop/setup/install/windows-install/)[Docker Desktop for LinuxA native Linux application that delivers all Docker tools to your Linux computer.](https://docs.docker.com/desktop/setup/install/linux/)

> Note
>
> If you're looking for information on how to install Docker Engine, see
> [Docker Engine installation overview](https://docs.docker.com/engine/install/).

---

# Build and push your first image

> This concept page will teach you how to build and push your first image

# Build and push your first image

   Table of contents

---

## Explanation

Now that you've updated the [to-do list app](https://docs.docker.com/get-started/introduction/develop-with-containers/), you’re ready to create a container image for the application and share it on Docker Hub. To do so, you will need to do the following:

1. Sign in with your Docker account
2. Create an image repository on Docker Hub
3. Build the container image
4. Push the image to Docker Hub

Before you dive into the hands-on guide, the following are a few core concepts that you should be aware of.

### Container images

If you’re new to container images, think of them as a standardized package that contains everything needed to run an application, including its files, configuration, and dependencies. These packages can then be distributed and shared with others.

### Docker Hub

To share your Docker images, you need a place to store them. This is where registries come in. While there are many registries, Docker Hub is the default and go-to registry for images. Docker Hub provides both a place for you to store your own images and to find images from others to either run or use as the bases for your own images.

When choosing base images, Docker Hub offers two categories of trusted, Docker-maintained images:

- [Docker Official Images (DOI)](https://docs.docker.com/docker-hub/image-library/trusted-content/#docker-official-images) – Curated images for popular software, following best practices and regularly updated.
- [Docker Hardened Images (DHI)](https://docs.docker.com/dhi/) – Minimal, secure, production-ready images with near-zero CVEs, designed to reduce attack surface and simplify compliance. DHI images are free and open source under Apache 2.0.

In [Develop with containers](https://docs.docker.com/get-started/introduction/develop-with-containers/), you used the following images that came from Docker Hub, each of which are
[Docker Official Images](https://docs.docker.com/docker-hub/image-library/trusted-content/#docker-official-images):

- [node](https://hub.docker.com/_/node) - provides a Node environment and is used as the base of your development efforts. This image is also used as the base for the final application image.
- [mysql](https://hub.docker.com/_/mysql) - provides a MySQL database to store the to-do list items
- [phpmyadmin](https://hub.docker.com/_/phpmyadmin) - provides phpMyAdmin, a web-based interface to the MySQL database
- [traefik](https://hub.docker.com/_/traefik) - provides Traefik, a modern HTTP reverse proxy and load balancer that routes requests to the appropriate container based on routing rules

Explore the full catalog of trusted content on Docker Hub:

- [Docker Official Images](https://hub.docker.com/search?badges=official) – Curated images for popular software
- [Docker Hardened Images](https://hub.docker.com/hardened-images/catalog) – Security-hardened, minimal production images (also available at [dhi.io](https://dhi.io))
- [Docker Verified Publishers](https://hub.docker.com/search?badges=verified_publisher) – Images from verified software vendors
- [Docker Sponsored Open Source](https://hub.docker.com/search?badges=open_source) – Images from sponsored OSS projects

## Try it out

In this hands-on guide, you'll learn how to sign in to Docker Hub and push images to Docker Hub repository.

## Sign in with your Docker account

To push images to Docker Hub, you will need to sign in with a Docker account.

1. Open the Docker Dashboard.
2. Select **Sign in** at the top-right corner.
3. If needed, create an account and then complete the sign-in flow.

Once you're done, you should see the **Sign in** button turn into a profile picture.

## Create an image repository

Now that you have an account, you can create an image repository. Just as a Git repository holds source code, an image repository stores container images.

1. Go to [Docker Hub](https://hub.docker.com).
2. Select **Create repository**.
3. On the **Create repository** page, enter the following information:
  - **Repository name** - `getting-started-todo-app`
  - **Short description** - feel free to enter a description if you'd like
  - **Visibility** - select **Public** to allow others to pull your customized to-do app
4. Select **Create** to create the repository.

## Build and push the image

Now that you have a repository, you are ready to build and push your image. An important note is that the image you are building extends the Node image, meaning you don't need to install or configure Node, yarn, etc. You can simply focus on what makes your application unique.

> **What is an image/Dockerfile?**
>
>
>
> Without going too deep yet, think of a container image as a single package that contains
> everything needed to run a process. In this case, it will contain a Node environment,
> the backend code, and the compiled React code.
>
>
>
> Any machine that runs a container using the image, will then be able to run the application as
> it was built without needing anything else pre-installed on the machine.
>
>
>
> A `Dockerfile` is a text-based script that provides the instruction set on how to build
> the image. For this quick start, the repository already contains the Dockerfile.

1. To get started, either clone or [download the project as a ZIP file](https://github.com/docker/getting-started-todo-app/archive/refs/heads/main.zip) to your local machine.
  ```console
  $ git clone https://github.com/docker/getting-started-todo-app
  ```
  And after the project is cloned, navigate into the new directory created by the clone:
  ```console
  $ cd getting-started-todo-app
  ```
2. Build the project by running the following command, swapping out `DOCKER_USERNAME` with your username.
  ```console
  $ docker build -t DOCKER_USERNAME/getting-started-todo-app .
  ```
  For example, if your Docker username was `mobydock`, you would run the following:
  ```console
  $ docker build -t mobydock/getting-started-todo-app .
  ```
3. To verify the image exists locally, you can use the `docker image ls` command:
  ```console
  $ docker image ls
  ```
  You will see output similar to the following:
  ```console
  REPOSITORY                          TAG       IMAGE ID       CREATED          SIZE
  mobydock/getting-started-todo-app   latest    1543656c9290   2 minutes ago    1.12GB
  ...
  ```
4. To push the image, use the `docker push` command. Be sure to replace `DOCKER_USERNAME` with your username:
  ```console
  $ docker push DOCKER_USERNAME/getting-started-todo-app
  ```
  Depending on your upload speeds, this may take a moment to push.

1. Open Visual Studio Code. Ensure you have the **Docker extension for VS Code** installed from [Extension Marketplace](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker).
  ![Screenshot of VS code extension marketplace](https://docs.docker.com/get-started/introduction/images/install-docker-extension.webp)  ![Screenshot of VS code extension marketplace](https://docs.docker.com/get-started/introduction/images/install-docker-extension.webp)
2. In the **File** menu, select **Open Folder**. Choose **Clone Git Repository** and paste this URL: [https://github.com/docker/getting-started-todo-app](https://github.com/docker/getting-started-todo-app)
  ![Screenshot of VS code showing how to clone a repository](https://docs.docker.com/get-started/introduction/images/clone-the-repo.webp)  ![Screenshot of VS code showing how to clone a repository](https://docs.docker.com/get-started/introduction/images/clone-the-repo.webp)
3. Right-click the `Dockerfile` and select the **Build Image...** menu item.
  ![Screenshot of VS Code showing the right-click menu and "Build Image" menu item](https://docs.docker.com/get-started/introduction/images/build-vscode-menu-item.webp)  ![Screenshot of VS Code showing the right-click menu and "Build Image" menu item](https://docs.docker.com/get-started/introduction/images/build-vscode-menu-item.webp)
4. In the dialog that appears, enter a name of `DOCKER_USERNAME/getting-started-todo-app`, replacing `DOCKER_USERNAME` with your Docker username.
5. After pressing **Enter**, you'll see a terminal appear where the build will occur. Once it's completed, feel free to close the terminal.
6. Open the Docker Extension for VS Code by selecting the Docker logo in the left nav menu.
7. Find the image you created. It'll have a name of `docker.io/DOCKER_USERNAME/getting-started-todo-app`.
8. Expand the image to view the tags (or different versions) of the image. You should see a tag named `latest`, which is the default tag given to an image.
9. Right-click on the **latest** item and select the **Push...** option.
  ![Screenshot of the Docker Extension and the right-click menu to push an image](https://docs.docker.com/get-started/introduction/images/build-vscode-push-image.webp)  ![Screenshot of the Docker Extension and the right-click menu to push an image](https://docs.docker.com/get-started/introduction/images/build-vscode-push-image.webp)
10. Press **Enter** to confirm and then watch as your image is pushed to Docker Hub. Depending on your upload speeds, it might take a moment to push the image.
  Once the upload is finished, feel free to close the terminal.

## Recap

Before you move on, take a moment and reflect on what happened here. Within a few moments, you were able to build a container image that packages your application and push it to Docker Hub.

Going forward, you’ll want to remember that:

- Docker Hub is the go-to registry for finding trusted content. Docker provides a collection of trusted content, composed of Docker Official Images, Docker Verified Publishers, and Docker Sponsored Open Source Software, to use directly or as bases for your own images.
- Docker Hub provides a marketplace to distribute your own applications. Anyone can create an account and distribute images. While you are publicly distributing the image you created, private repositories can ensure your images are accessible to only authorized users.

> **Usage of other registries**
>
>
>
> While Docker Hub is the default registry, registries are standardized and made
> interoperable through the [Open Container Initiative](https://opencontainers.org/). This allows companies and
> organizations to run their own private registries. Quite often, trusted content
> is mirrored (or copied) from Docker Hub into these private registries.

## Next steps

Now that you’ve built an image, it's time to discuss why you as a developer should learn more about Docker and how it will help you in your day-to-day tasks.

[What's Next](https://docs.docker.com/get-started/introduction/whats-next/)

---

# Develop with containers

> This concept page will teach you how to develop with containers

# Develop with containers

   Table of contents

---

## Explanation

Now that you have Docker Desktop installed, you are ready to do some application development. Specifically, you will do the following:

1. Clone and start a development project
2. Make changes to the backend and frontend
3. See the changes immediately

## Try it out

In this hands-on guide, you'll learn how to develop with containers.

## Start the project

1. To get started, either clone or [download the project as a ZIP file](https://github.com/docker/getting-started-todo-app/archive/refs/heads/main.zip) to your local machine.
  ```console
  $ git clone https://github.com/docker/getting-started-todo-app
  ```
  And after the project is cloned, navigate into the new directory created by the clone:
  ```console
  $ cd getting-started-todo-app
  ```
2. Once you have the project, start the development environment using Docker Compose.
  To start the project using the CLI, run the following command:
  ```console
  $ docker compose watch
  ```
  You will see an output that shows container images being pulled down, containers starting, and more. Don't worry if you don't understand it all at this point. But, within a moment or two, things should stabilize and finish.
3. Open your browser to [http://localhost](http://localhost) to see the application up and running. It may take a few minutes for the app to run. The app is a simple to-do application, so feel free to add an item or two, mark some as done, or even delete an item.
  ![Screenshot of the getting started to-do app after its first launch](https://docs.docker.com/get-started/introduction/images/develop-getting-started-app-first-launch.webp)  ![Screenshot of the getting started to-do app after its first launch](https://docs.docker.com/get-started/introduction/images/develop-getting-started-app-first-launch.webp)

### What's in the environment?

Now that the environment is up and running, what's actually in it? At a high-level, there are several containers (or processes) that each serve a specific need for the application:

- React frontend - a Node container that's running the React dev server, using [Vite](https://vitejs.dev/).
- Node backend - the backend provides an API that provides the ability to retrieve, create, and delete to-do items.
- MySQL database - a database to store the list of the items.
- phpMyAdmin - a web-based interface to interact with the database that is accessible at [http://db.localhost](http://db.localhost).
- Traefik proxy - [Traefik](https://traefik.io/traefik/) is an application proxy that routes requests to the right service. It sends all requests for `localhost/api/*` to the backend, requests for `localhost/*` to the frontend, and then requests for `db.localhost` to phpMyAdmin. This provides the ability to access all applications using port 80 (instead of different ports for each service).

With this environment, you as the developer don’t need to install or configure any services, populate a database schema, configure database credentials, or anything. You only need Docker Desktop. The rest just works.

## Make changes to the app

With this environment up and running, you’re ready to make a few changes to the application and see how Docker helps provide a fast feedback loop.

### Change the greeting

The greeting at the top of the page is populated by an API call at `/api/greeting`. Currently, it always returns "Hello world!". You’ll now modify it to return one of three randomized messages (that you'll get to choose).

1. Open the `backend/src/routes/getGreeting.js` file in a text editor. This file provides the handler for the API endpoint.
2. Modify the variable at the top to an array of greetings. Feel free to use the following modifications or customize it to your own liking. Also, update the endpoint to send a random greeting from this list.
  | 1234567891011 | constGREETINGS=["Whalecome!","All hands on deck!","Charting the course ahead!",];module.exports=async(req,res)=>{res.send({greeting:GREETINGS[Math.floor(Math.random()*GREETINGS.length)],});}; |
  | --- | --- |
3. If you haven't done so yet, save the file. If you refresh your browser, you should see a new greeting. If you keep refreshing, you should see all of the messages appear.
  ![Screenshot of the to-do app with a new greeting](https://docs.docker.com/get-started/introduction/images/develop-app-with-greetings.webp)  ![Screenshot of the to-do app with a new greeting](https://docs.docker.com/get-started/introduction/images/develop-app-with-greetings.webp)

### Change the placeholder text

When you look at the app, you'll see the placeholder text is simply "New Item". You’ll now make that a little more descriptive and fun. You’ll also make a few changes to the styling of the app too.

1. Open the `client/src/components/AddNewItemForm.jsx` file. This provides the component to add a new item to the to-do list.
2. Modify the `placeholder` attribute of the `Form.Control` element to whatever you'd like to display.
  | 33343536373839 | <Form.Controlvalue={newItem}onChange={(e)=>setNewItem(e.target.value)}type="text"placeholder="What do you need to do?"aria-label="New item"/> |
  | --- | --- |
3. Save the file and go back to your browser. You should see the change already hot-reloaded into your browser. If you don't like it, feel free to tweak it until it looks just right.

![Screenshot of the to-do app with an updated placeholder in the add item text field"](https://docs.docker.com/get-started/introduction/images/develop-app-with-updated-placeholder.webp)  ![Screenshot of the to-do app with an updated placeholder in the add item text field"](https://docs.docker.com/get-started/introduction/images/develop-app-with-updated-placeholder.webp)

### Change the background color

Before you consider the application finalized, you need to make the colors better.

1. Open the `client/src/index.scss` file.
2. Adjust the `background-color` attribute to any color you'd like. The provided snippet is a soft blue to go along with Docker's nautical theme.
  If you're using an IDE, you can pick a color using the integrated color pickers. Otherwise, feel free to use an online [Color Picker](https://www.w3schools.com/colors/colors_picker.asp).
  | 34567 | body{background-color:#99bbff;margin-top:50px;font-family:'Lato';} |
  | --- | --- |
  Each save should let you see the change immediately in the browser. Keep adjusting it until it's the perfect setup for you.
  ![Screenshot of the to-do app with a new placeholder and background color"](https://docs.docker.com/get-started/introduction/images/develop-app-with-updated-client.webp)  ![Screenshot of the to-do app with a new placeholder and background color"](https://docs.docker.com/get-started/introduction/images/develop-app-with-updated-client.webp)

And with that, you're done. Congrats on updating your website.

## Recap

Before you move on, take a moment and reflect on what happened here. Within a few moments, you were able to:

- Start a complete development project with zero installation effort. The containerized environment provided the development environment, ensuring you have everything you need. You didn't have to install Node, MySQL, or any of the other dependencies directly on your machine. All you needed was Docker Desktop and a code editor.
- Make changes and see them immediately. This was made possible because 1) the processes running in each container are watching and responding to file changes and 2) the files are shared with the containerized environment.

Docker Desktop enables all of this and so much more. Once you start thinking with containers, you can create almost any environment and easily share it with your team.

## Next steps

Now that the application has been updated, you’re ready to learn about packaging it as a container image and pushing it to a registry, specifically Docker Hub.

[Build and push your first image](https://docs.docker.com/get-started/introduction/build-and-push-first-image/)

---

# Get Docker Desktop

> This concept page will teach you download Docker Desktop and install it on Windows, Mac, and Linux

# Get Docker Desktop

   Table of contents

---

## Explanation

Docker Desktop is the all-in-one package to build images, run containers, and so much more.
This guide will walk you through the installation process, enabling you to experience Docker Desktop firsthand.

> **Docker Desktop terms**
>
>
>
> Commercial use of Docker Desktop in larger enterprises (more than 250
> employees OR more than $10 million USD in annual revenue) requires a [paid subscription](https://www.docker.com/pricing/?_gl=1*1nyypal*_ga*MTYxMTUxMzkzOS4xNjgzNTM0MTcw*_ga_XJWPQMJYHQ*MTcxNjk4MzU4Mi4xMjE2LjEuMTcxNjk4MzkzNS4xNy4wLjA.).

### Docker Desktop for Mac

[Download (Apple Silicon)](https://desktop.docker.com/mac/main/arm64/Docker.dmg?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-mac-arm64) | [Download (Intel)](https://desktop.docker.com/mac/main/amd64/Docker.dmg?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-mac-amd64) |
[Install instructions](https://docs.docker.com/desktop/setup/install/mac-install)

### Docker Desktop for Windows

[Download](https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-windows) |
[Install instructions](https://docs.docker.com/desktop/setup/install/windows-install)

### Docker Desktop for Linux

[Install instructions](https://docs.docker.com/desktop/setup/install/linux/)

Once it's installed, complete the setup process and you're all set to run a Docker container.

## Try it out

In this hands-on guide, you will see how to run a Docker container using Docker Desktop.

Follow the instructions to run a container using the CLI.

## Run your first container

Open your CLI terminal and start a container by running the `docker run` command:

```console
$ docker run -d -p 8080:80 docker/welcome-to-docker
```

## Access the frontend

For this container, the frontend is accessible on port `8080`. To open the website, visit [http://localhost:8080](http://localhost:8080) in your browser.

![Screenshot of the landing page of the Nginx web server, coming from the running container](https://docs.docker.com/get-started/docker-concepts/the-basics/images/access-the-frontend.webp)  ![Screenshot of the landing page of the Nginx web server, coming from the running container](https://docs.docker.com/get-started/docker-concepts/the-basics/images/access-the-frontend.webp)

## Manage containers using Docker Desktop

1. Open Docker Desktop and select the **Containers** field on the left sidebar.
2. You can view information about your container including logs, and files, and even access the shell by selecting the **Exec** tab.
  ![Screenshot of exec into the running container in Docker Desktop](https://docs.docker.com/get-started/introduction/images/exec-into-docker-container.webp)  ![Screenshot of exec into the running container in Docker Desktop](https://docs.docker.com/get-started/introduction/images/exec-into-docker-container.webp)
3. Select the **Inspect** field to obtain detailed information about the container. You can perform various actions such as pause, resume, start or stop containers, or explore the **Logs**, **Bind mounts**, **Exec**, **Files**, and **Stats** tabs.

![Screenshot of inspecting the running container in Docker Desktop](https://docs.docker.com/get-started/introduction/images/inspecting-container.webp)  ![Screenshot of inspecting the running container in Docker Desktop](https://docs.docker.com/get-started/introduction/images/inspecting-container.webp)

Docker Desktop simplifies container management for developers by streamlining the setup, configuration, and compatibility of applications across different environments, thereby addressing the pain points of environment inconsistencies and deployment challenges.

## What's next?

Now that you have Docker Desktop installed and ran your first container, it's time to start developing with containers.

[Develop with containers](https://docs.docker.com/get-started/introduction/develop-with-containers/)

---

# What's next

> Explore step-by-step guides to hep you understand core Docker concepts, building images, and running containers.

# What's next

---

The following sections provide step-by-step guides to help you understand core Docker concepts, building images, and running containers.

## The basics

Get started learning the core concepts of containers, images, registries, and Docker Compose.

[What is a container?Learn how to run your first container.](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/)[What is an image?Learn the basics of image layers.](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-an-image/)[What is a registry?Learn about container registries, explore their interoperability, and interact with registries.](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-registry/)[What is Docker Compose?Gain a better understanding of Docker Compose.](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-docker-compose/)

## Building images

Craft optimized container images with Dockerfiles, build cache, and multi-stage builds.

[Understanding image layersLearn about the layers of container images.](https://docs.docker.com/get-started/docker-concepts/building-images/understanding-image-layers/)[Writing a DockerfileLearn how to create an image using a Dockerfile.](https://docs.docker.com/get-started/docker-concepts/building-images/writing-a-dockerfile/)[Build, tag and publish an imageLearn how to build, tag, and publish an image to Docker Hub or any other registry.](https://docs.docker.com/get-started/docker-concepts/building-images/build-tag-and-publish-an-image/)[Using the build cacheLearn about the build cache, what changes invalidate the cache, and how to effectively use the build cache.](https://docs.docker.com/get-started/docker-concepts/building-images/using-the-build-cache/)[Multi-stage buildsGet a better understanding of multi-stage builds and their benefits.](https://docs.docker.com/get-started/docker-concepts/building-images/multi-stage-builds/)

## Running containers

Master essential techniques for exposing ports, overriding defaults, persisting data, sharing files, and managing multi-container applications.

[Publishing portsUnderstand the significance of publishing and exposing ports in Docker.](https://docs.docker.com/get-started/docker-concepts/running-containers/publishing-ports/)[Overriding container defaultsLearn how to override the container defaults using thedocker runcommand.](https://docs.docker.com/get-started/docker-concepts/running-containers/overriding-container-defaults/)[Persisting container dataLearn the significance of data persistence in Docker.](https://docs.docker.com/get-started/docker-concepts/running-containers/persisting-container-data/)[Sharing local files with containersExplore the various storage options available in Docker and their common usage.](https://docs.docker.com/get-started/docker-concepts/running-containers/sharing-local-files/)[Multi-container applicationsLearn the significance of multi-container applications and how they're different from single-container applications.](https://docs.docker.com/get-started/docker-concepts/running-containers/multi-container-applications/)
