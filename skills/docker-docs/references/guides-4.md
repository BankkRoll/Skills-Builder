# Test your Bun deployment and more

# Test your Bun deployment

> Learn how to develop locally using Kubernetes

# Test your Bun deployment

   Table of contents

---

## Prerequisites

- Complete all the previous sections of this guide, starting with [Containerize a Bun application](https://docs.docker.com/guides/bun/containerize/).
- [Turn on Kubernetes](https://docs.docker.com/desktop/use-desktop/kubernetes/#enable-kubernetes) in Docker Desktop.

## Overview

In this section, you'll learn how to use Docker Desktop to deploy your application to a fully-featured Kubernetes environment on your development machine. This allows you to test and debug your workloads on Kubernetes locally before deploying.

## Create a Kubernetes YAML file

In your `bun-docker` directory, create a file named
`docker-kubernetes.yml`. Open the file in an IDE or text editor and add
the following contents. Replace `DOCKER_USERNAME/REPO_NAME` with your Docker
username and the name of the repository that you created in [Configure CI/CD for
your Bun application](https://docs.docker.com/guides/bun/configure-ci-cd/).

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: docker-bun-demo
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: bun-api
  template:
    metadata:
      labels:
        app: bun-api
    spec:
      containers:
       - name: bun-api
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
    app: bun-api
  ports:
  - port: 3000
    targetPort: 3000
    nodePort: 30001
```

In this Kubernetes YAML file, there are two objects, separated by the `---`:

- A Deployment, describing a scalable group of identical pods. In this case,
  you'll get just one replica, or copy of your pod. That pod, which is
  described under `template`, has just one container in it. The
  container is created from the image built by GitHub Actions in [Configure CI/CD for
  your Bun application](https://docs.docker.com/guides/bun/configure-ci-cd/).
- A NodePort service, which will route traffic from port 30001 on your host to
  port 3000 inside the pods it routes to, allowing you to reach your app
  from the network.

To learn more about Kubernetes objects, see the [Kubernetes documentation](https://kubernetes.io/docs/home/).

## Deploy and check your application

1. In a terminal, navigate to `bun-docker` and deploy your application to
  Kubernetes.
  ```console
  $ kubectl apply -f docker-kubernetes.yml
  ```
  You should see output that looks like the following, indicating your Kubernetes objects were created successfully.
  ```text
  deployment.apps/docker-bun-demo created
  service/service-entrypoint created
  ```
2. Make sure everything worked by listing your deployments.
  ```console
  $ kubectl get deployments
  ```
  Your deployment should be listed as follows:
  ```shell
  NAME                 READY   UP-TO-DATE   AVAILABLE    AGE
  docker-bun-demo       1/1     1            1           10s
  ```
  This indicates all one of the pods you asked for in your YAML are up and running. Do the same check for your services.
  ```console
  $ kubectl get services
  ```
  You should get output like the following.
  ```shell
  NAME                 TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
  kubernetes           ClusterIP   10.96.0.1        <none>        443/TCP          88m
  service-entrypoint   NodePort    10.105.145.223   <none>        3000:30001/TCP   83s
  ```
  In addition to the default `kubernetes` service, you can see your `service-entrypoint` service, accepting traffic on port 30001/TCP.
3. In a browser, visit the following address. You should see the message `{"Status" : "OK"}`.
  ```console
  http://localhost:30001/
  ```
4. Run the following command to tear down your application.
  ```console
  $ kubectl delete -f docker-kubernetes.yml
  ```

## Summary

In this section, you learned how to use Docker Desktop to deploy your Bun application to a fully-featured Kubernetes environment on your development machine.

Related information:

- [Kubernetes documentation](https://kubernetes.io/docs/home/)
- [Deploy on Kubernetes with Docker Desktop](https://docs.docker.com/desktop/use-desktop/kubernetes/)
- [Swarm mode overview](https://docs.docker.com/engine/swarm/)

---

# Use containers for Bun development

> Learn how to develop your Bun application locally.

# Use containers for Bun development

   Table of contents

---

## Prerequisites

Complete [Containerize a Bun application](https://docs.docker.com/guides/bun/containerize/).

## Overview

In this section, you'll learn how to set up a development environment for your containerized application. This includes:

- Configuring Compose to automatically update your running Compose services as you edit and save your code

## Get the sample application

Clone the sample application to use with this guide. Open a terminal, change directory to a directory that you want to work in, and run the following command to clone the repository:

```console
$ git clone https://github.com/dockersamples/bun-docker.git && cd bun-docker
```

## Automatically update services

Use Compose Watch to automatically update your running Compose services as you
edit and save your code. For more details about Compose Watch, see
[Use Compose
Watch](https://docs.docker.com/compose/how-tos/file-watch/).

Open your `compose.yml` file in an IDE or text editor and then add the Compose Watch instructions. The following example shows how to add Compose Watch to your `compose.yml` file.

| 123456789101112 | services:server:image:bun-serverbuild:context:.dockerfile:Dockerfileports:-"3000:3000"develop:watch:-action:rebuildpath:. |
| --- | --- |

Run the following command to run your application with Compose Watch.

```console
$ docker compose watch
```

Now, if you modify your `server.js` you will see the changes in real time without re-building the image.

To test it out, open the `server.js` file in your favorite text editor and change the message from `{"Status" : "OK"}` to `{"Status" : "Updated"}`. Save the file and refresh your browser at `http://localhost:3000`. You should see the updated message.

Press `ctrl+c` in the terminal to stop your application.

## Summary

In this section, you also learned how to use Compose Watch to automatically rebuild and run your container when you update your code.

Related information:

- [Compose file reference](https://docs.docker.com/reference/compose-file/)
- [Compose file watch](https://docs.docker.com/compose/how-tos/file-watch/)
- [Multi-stage builds](https://docs.docker.com/build/building/multi-stage/)

## Next steps

In the next section, you'll take a look at how to set up a CI/CD pipeline using GitHub Actions.

---

# Bun language

> Containerize and develop Bun applications using Docker.

# Bun language-specific guide

Table of contents

---

The Bun getting started guide teaches you how to create a containerized Bun application using Docker.

> **Acknowledgment**
>
>
>
> Docker would like to thank [Pradumna Saraf](https://twitter.com/pradumna_saraf) for his contribution to this guide.

## What will you learn?

- Containerize and run a Bun application using Docker
- Set up a local environment to develop a Bun application using containers
- Configure a CI/CD pipeline for a containerized Bun application using GitHub Actions
- Deploy your containerized application locally to Kubernetes to test and debug your deployment

## Prerequisites

- Basic understanding of JavaScript is assumed.
- You must have familiarity with Docker concepts like containers, images, and Dockerfiles. If you are new to Docker, you can start with the
  [Docker basics](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/) guide.

After completing the Bun getting started modules, you should be able to containerize your own Bun application based on the examples and instructions provided in this guide.

Start by containerizing an existing Bun application.

## Modules

1. [Containerize your app](https://docs.docker.com/guides/bun/containerize/)
  Learn how to containerize a Bun application.
2. [Develop your app](https://docs.docker.com/guides/bun/develop/)
  Learn how to develop your Bun application locally.
3. [Configure CI/CD](https://docs.docker.com/guides/bun/configure-ci-cd/)
  Learn how to configure CI/CD using GitHub Actions for your Bun application.
4. [Test your deployment](https://docs.docker.com/guides/bun/deploy/)
  Learn how to develop locally using Kubernetes

---

# Building Compose projects with Bake

> Learn how to build Docker Compose projects with Docker Buildx Bake

# Building Compose projects with Bake

   Table of contents

---

This guide explores how you can use Bake to build images for Docker Compose
projects with multiple services.

[Docker Buildx Bake](https://docs.docker.com/build/bake/) is a build orchestration
tool that enables declarative configuration for your builds, much like Docker
Compose does for defining runtime stacks. For projects where Docker Compose is
used to spin up services for local development, Bake offers a way of seamlessly
extending the project with a production-ready build configuration.

## Prerequisites

This guide assumes that you're familiar with

- Docker Compose
- [Multi-stage builds](https://docs.docker.com/build/building/multi-stage/)
- [Multi-platform builds](https://docs.docker.com/build/building/multi-platform/)

## Orientation

This guide will use the
[dvdksn/example-voting-app](https://github.com/dvdksn/example-voting-app)
repository as an example of a monorepo using Docker Compose that can be
extended with Bake.

```console
$ git clone https://github.com/dvdksn/example-voting-app.git
$ cd example-voting-app
```

This repository uses Docker Compose to define the runtime configurations for
running the application, in the `compose.yaml` file. This app consists of the
following services:

| Service | Description |
| --- | --- |
| vote | A front-end web app in Python which lets you vote between two options. |
| result | A Node.js web app which shows the results of the voting in real time. |
| worker | A .NET worker which consumes votes and stores them in the database. |
| db | A Postgres database backed by a Docker volume. |
| redis | A Redis instance which collects new votes. |
| seed | A utility container that seeds the database with mock data. |

The `vote`, `result`, and `worker` services are built from code in this
repository, whereas `db` and `redis` use pre-existing Postgres and Redis images
from Docker Hub. The `seed` service is a utility that invokes requests against
the front-end service to populate the database, for testing purposes.

## Build with Compose

When you spin up a Docker Compose project, any services that define the `build`
property are automatically built before the service is started. Here's the
build configuration for the `vote` service in the example repository:

compose.yaml

```yaml
services:
  vote:
    build:
      context: ./vote # Build context
      target: dev # Dockerfile stage
```

The `vote`, `result`, and `worker` services all have a build configuration
specified. Running `docker compose up` will trigger a build of these services.

Did you know that you can also use Compose just to build the service images?
The `docker compose build` command lets you invoke a build using the build
configuration specified in the Compose file. For example, to build the `vote`
service with this configuration, run:

```console
$ docker compose build vote
```

Omit the service name to build all services at once:

```console
$ docker compose build
```

The `docker compose build` command is useful when you only need to build images
without running services.

The Compose file format supports a number of properties for defining your
build's configuration. For example, to specify the tag name for the images, set
the `image` property on the service.

```yaml
services:
  vote:
    image: username/vote
    build:
      context: ./vote
      target: dev
    #...

  result:
    image: username/result
    build:
      context: ./result
    #...

  worker:
    image: username/worker
    build:
      context: ./worker
    #...
```

Running `docker compose build` creates three service images with fully
qualified image names that you can push to Docker Hub.

The `build` property supports a
[wide range](https://docs.docker.com/reference/compose-file/build/)
of options for configuring builds. However, building production-grade images
are often different from images used in local development. To avoid cluttering
your Compose file with build configurations that might not be desirable for
local builds, consider separating the production builds from the local builds
by using Bake to build images for release. This approach separates concerns:
using Compose for local development and Bake for production-ready builds, while
still reusing service definitions and fundamental build configurations.

## Build with Bake

Like Compose, Bake parses the build definition for a project from a
configuration file. Bake supports HashiCorp Configuration Language (HCL), JSON,
and the Docker Compose YAML format. When you use Bake with multiple files, it
will find and merge all of the applicable configuration files into one unified
build configuration. The build options defined in your Compose file are
extended, or in some cases overridden, by options specified in the Bake file.

The following section explores how you can use Bake to extend the build options
defined in your Compose file for production.

### View the build configuration

Bake automatically creates a build configuration from the `build` properties of
your services. Use the `--print` flag for Bake to view the build configuration
for a given Compose file. This flag evaluates the build configuration and
outputs the build definition in JSON format.

```console
$ docker buildx bake --print
```

The JSON-formatted output shows the group that would be executed, and all the
targets of that group. A group is a collection of builds, and a target
represents a single build.

```json
{
  "group": {
    "default": {
      "targets": [
        "vote",
        "result",
        "worker",
        "seed"
      ]
    }
  },
  "target": {
    "result": {
      "context": "result",
      "dockerfile": "Dockerfile",
    },
    "seed": {
      "context": "seed-data",
      "dockerfile": "Dockerfile",
    },
    "vote": {
      "context": "vote",
      "dockerfile": "Dockerfile",
      "target": "dev",
    },
    "worker": {
      "context": "worker",
      "dockerfile": "Dockerfile",
    }
  }
}
```

As you can see, Bake has created a `default` group that includes four targets:

- `seed`
- `vote`
- `result`
- `worker`

This group is created automatically from your Compose file; it includes all of
your services containing a build configuration. To build this group of services
with Bake, run:

```console
$ docker buildx bake
```

### Customize the build group

Start by redefining the default build group that Bake executes. The current
default group includes a `seed` target — a Compose service used solely to
populate the database with mock data. Since this target doesn't produce a
production image, it doesn’t need to be included in the build group.

To customize the build configuration that Bake uses, create a new file at the
root of the repository, alongside your `compose.yaml` file, named
`docker-bake.hcl`.

```console
$ touch docker-bake.hcl
```

Open the Bake file and add the following configuration:

docker-bake.hcl

```hcl
group "default" {
  targets = ["vote", "result", "worker"]
}
```

Save the file and print your Bake definition again.

```console
$ docker buildx bake --print
```

The JSON output shows that the `default` group only includes the targets you
care about.

```json
{
  "group": {
    "default": {
      "targets": ["vote", "result", "worker"]
    }
  },
  "target": {
    "result": {
      "context": "result",
      "dockerfile": "Dockerfile",
      "tags": ["username/result"]
    },
    "vote": {
      "context": "vote",
      "dockerfile": "Dockerfile",
      "tags": ["username/vote"],
      "target": "dev"
    },
    "worker": {
      "context": "worker",
      "dockerfile": "Dockerfile",
      "tags": ["username/worker"]
    }
  }
}
```

Here, the build configuration for each target (context, tags, etc.) is picked
up from the `compose.yaml` file. The group is defined by the `docker-bake.hcl`
file.

### Customize targets

The Compose file currently defines the `dev` stage as the build target for the
`vote` service. That's appropriate for the image that you would run in local
development, because the `dev` stage includes additional development
dependencies and configurations. For the production image, however, you'll want
to target the `final` image instead.

To modify the target stage used by the `vote` service, add the following
configuration to the Bake file:

```hcl
target "vote" {
  target = "final"
}
```

This overrides the `target` property specified in the Compose file with a
different value when you run the build with Bake. The other build options in
the Compose file (tag, context) remain unmodified. You can verify by inspecting
the build configuration for the `vote` target with `docker buildx bake --print vote`:

```json
{
  "group": {
    "default": {
      "targets": ["vote"]
    }
  },
  "target": {
    "vote": {
      "context": "vote",
      "dockerfile": "Dockerfile",
      "tags": ["username/vote"],
      "target": "final"
    }
  }
}
```

### Additional build features

Production-grade builds often have different characteristics from development
builds. Here are a few examples of things you might want to add for production
images.

Multi-platformFor local development, you only need to build images for your local platform,
since those images are just going to run on your machine. But for images that
are pushed to a registry, it's often a good idea to build for multiple
platforms, arm64 and amd64 in particular.Attestations[Attestations](https://docs.docker.com/build/metadata/attestations/) are manifests
attached to the image that describe how the image was created and what
components it contains. Attaching attestations to your images helps ensure that
your images follow software supply chain best practices.Annotations[Annotations](https://docs.docker.com/build/metadata/annotations/) provide descriptive
metadata for images. Use annotations to record arbitrary information and attach
it to your image, which helps consumers and tools understand the origin,
contents, and how to use the image.

> Tip
>
> Why not just define these additional build options in the Compose file
> directly?
>
>
>
> The `build` property in the Compose file format does not support all build
> features. Additionally, some features, like multi-platform builds, can
> drastically increase the time it takes to build a service. For local
> development, you're better off keeping your build step simple and fast,
> saving the bells and whistles for release builds.

To add these properties to the images you build with Bake, update the Bake file
as follows:

```hcl
group "default" {
  targets = ["vote", "result", "worker"]
}

target "_common" {
  annotations = ["org.opencontainers.image.authors=username"]
  platforms = ["linux/amd64", "linux/arm64"]
  attest = [
    "type=provenance,mode=max",
    "type=sbom"
  ]
}

target "vote" {
  inherits = ["_common"]
  target = "final"
}

target "result" {
  inherits = ["_common"]
}

target "worker" {
  inherits = ["_common"]
}
```

This defines a new `_common` target that defines reusable build configuration
for adding multi-platform support, annotations, and attestations to your
images. The reusable target is inherited by the build targets.

With these changes, building the project with Bake produces three sets of
multi-platform images for the `linux/amd64` and `linux/arm64` architectures.
Each image is decorated with an author annotation, and both SBOM and provenance
attestation records.

## Conclusions

The pattern demonstrated in this guide provides a useful approach for managing
production-ready Docker images in projects using Docker Compose. Using Bake
gives you access to all the powerful features of Buildx and BuildKit, and also
helps separate your development and build configuration in a reasonable way.

### Further reading

For more information about how to use Bake, check out these resources:

- [Bake documentation](https://docs.docker.com/build/bake/)
- [Building with Bake from a Compose file](https://docs.docker.com/build/bake/compose-file/)
- [Bake file reference](https://docs.docker.com/build/bake/reference/)
- [Mastering multi-platform builds, testing, and more with Docker Buildx Bake](https://docs.docker.com/guides/bake/)
- [Bake GitHub Action](https://github.com/docker/bake-action)

---

# Faster development and testing with container

> Use containers in your local development loop to develop and test faster… even if your main app isn't running in containers.

# Faster development and testing with container-supported development

   Table of contents

---

Containers offer a consistent way to build, share, and run applications across different environments. While containers are typically used to containerize your application, they also make it incredibly easy to run essential services needed for development. Instead of installing or connecting to a remote database, you can easily launch your own database. But the possibilities don't stop there.

With container-supported development, you use containers to enhance your development environment by emulating or running your own instances of the services your app needs. This provides faster feedback loops, less coupling with remote services, and a greater ability to test error states.

And best of all, you can have these benefits regardless of whether the main app under development is running in containers.

## What you'll learn

- The meaning of container-supported development
- How to connect non-containerized applications to containerized services
- Several examples of using containers to emulate or run local instances of services
- How to use containers to add additional troubleshooting and debugging tools to your development environment

## Who's this for?

- Teams that want to reduce the coupling they have on shared or deployed infrastructure or remote API endpoints
- Teams that want to reduce the complexity and costs associated with using cloud services directly during development
- Developers that want to make it easier to visualize what's going on in their databases, queues, etc.
- Teams that want to reduce the complexity of setting up their development environment without impacting the development of the app itself

## Tools integration

Works well with Docker Compose and Testcontainers.

## Modules

### What is container-supported development?

Container-supported development is the idea of using containers to enhance your development environment by running local instances or emulators of the services your application relies on. Once you're using containers, it's easy to add additional services to visualize or troubleshoot what's going on in your services.

### Demo: running databases locally

With container-supported development, it's easy to run databases locally. In this demo, you'll see how to do so, as well as how to connect a non-containerized application to the database.

> Tip
>
> Learn more about running databases in containers in the
> [Use containerized databases](https://docs.docker.com/guides/databases/) guide.

### Demo: mocking API endpoints

Many APIs require data from other data endpoints. In development, this adds complexities such as the sharing of credentials, uptime/availability, and rate limiting. Instead of relying on those services directly, your application can interact with a mock API server.

This demo will demonstrate how using WireMock can make it easy to develop and test an application, including the APIs various error states.

> Tip
>
> Learn more about using WireMock to mock API in the
> [Mocking API services with WireMock](https://docs.docker.com/guides/wiremock/) guide.

### Demo: developing the cloud locally

When developing apps, it's often easier to outsource aspects of the application to cloud services, such as Amazon S3. However, connecting to those services in local development introduces IAM policies, networking constraints, and provisioning complications. While these requirements are important in a production setting, they complicate development environments significantly.

With container-supported development, you can run local instances of these services during development and testing, removing the need for complex setups. In this demo, you'll see how LocalStack makes it easy to develop and test applications entirely from the developer's workstation.

> Tip
>
> Learn more about using LocalStack in the
> [Develop and test AWS Cloud applications using LocalStack](https://docs.docker.com/guides/localstack/) guide.

### Demo: adding additional debug and troubleshooting tools

Once you start using containers in your development environment, it becomes much easier to add additional containers to visualize the contents of the databases or message queues, seed document stores, or event publishers. In this demo, you'll see a few of these examples, as well as how you can connect multiple containers together to make testing even easier.

---

# Configure CI/CD for your C++ application

> Learn how to configure CI/CD using GitHub Actions for your C++ application.

# Configure CI/CD for your C++ application

   Table of contents

---

## Prerequisites

Complete all the previous sections of this guide, starting with [Containerize a C++ application](https://docs.docker.com/guides/cpp/containerize/). You must have a [GitHub](https://github.com/signup) account and a verified [Docker](https://hub.docker.com/signup) account to complete this section.

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
2. Select **set up a workflow yourself**.
  This takes you to a page for creating a new GitHub actions workflow file in
  your repository, under `.github/workflows/main.yml` by default.
3. In the editor window, copy and paste the following YAML configuration and commit the changes.
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
        - name: Build and push
          uses: docker/build-push-action@v6
          with:
            platforms: linux/amd64,linux/arm64
            push: true
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

In this section, you learned how to set up a GitHub Actions workflow for your C++ application.

Related information:

- [Introduction to GitHub Actions](https://docs.docker.com/guides/gha/)
- [Docker Build GitHub Actions](https://docs.docker.com/build/ci/github-actions/)
- [Workflow syntax for GitHub Actions](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

## Next steps

Next, learn how you can locally test and debug your workloads on Kubernetes before deploying.

---

# Containerize a C++ application

> Learn how to use Docker Compose to build and run a C++ application.

# Containerize a C++ application

   Table of contents

---

## Prerequisites

- You have a [Git client](https://git-scm.com/downloads). The examples in this section use a command-line based Git client, but you can use any client.

## Overview

This section walks you through containerizing and running a C++ application, using Docker Compose.

## Get the sample application

We're using the same sample repository that you used in the previous sections of this guide. If you haven't already cloned the repository, clone it now:

```console
$ git clone https://github.com/dockersamples/c-plus-plus-docker.git
```

You should now have the following contents in your `c-plus-plus-docker` (root)
directory.

```text
├── c-plus-plus-docker/
│ ├── compose.yml
│ ├── Dockerfile
│ ├── LICENSE
│ ├── ok_api.cpp
│ └── README.md
```

To learn more about the files in the repository, see the following:

- [Dockerfile](https://docs.docker.com/reference/dockerfile/)
- [.dockerignore](https://docs.docker.com/reference/dockerfile/#dockerignore-file)
- [compose.yml](https://docs.docker.com/reference/compose-file/)

## Run the application

Inside the `c-plus-plus-docker` directory, run the following command in a
terminal.

```console
$ docker compose up --build
```

Open a browser and view the application at [http://localhost:8080](http://localhost:8080). You will see a message `{"Status" : "OK"}` in the browser.

In the terminal, press `ctrl`+`c` to stop the application.

### Run the application in the background

You can run the application detached from the terminal by adding the `-d`
option. Inside the `c-plus-plus-docker` directory, run the following command
in a terminal.

```console
$ docker compose up --build -d
```

Open a browser and view the application at [http://localhost:8080](http://localhost:8080).

In the terminal, run the following command to stop the application.

```console
$ docker compose down
```

For more information about Compose commands, see the
[Compose CLI
reference](https://docs.docker.com/reference/cli/docker/compose/).

## Summary

In this section, you learned how you can containerize and run your C++
application using Docker.

Related information:

- [Docker Compose overview](https://docs.docker.com/compose/)

## Next steps

In the next section, you'll learn how you can develop your application using
containers.

---

# Test your C++ deployment

> Learn how to develop locally using Kubernetes

# Test your C++ deployment

   Table of contents

---

## Prerequisites

- Complete all the previous sections of this guide, starting with [Containerize a C++ application](https://docs.docker.com/guides/cpp/containerize/).
- [Turn on Kubernetes](https://docs.docker.com/desktop/use-desktop/kubernetes/#enable-kubernetes) in Docker Desktop.

## Overview

In this section, you'll learn how to use Docker Desktop to deploy your application to a fully-featured Kubernetes environment on your development machine. This allows you to test and debug your workloads on Kubernetes locally before deploying.

## Create a Kubernetes YAML file

In your `c-plus-plus-docker` directory, create a file named
`docker-kubernetes.yml`. Open the file in an IDE or text editor and add
the following contents. Replace `DOCKER_USERNAME/REPO_NAME` with your Docker
username and the name of the repository that you created in [Configure CI/CD for
your C++ application](https://docs.docker.com/guides/cpp/configure-ci-cd/).

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: docker-c-plus-plus-demo
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      service: ok-api
  template:
    metadata:
      labels:
        service: ok-api
    spec:
      containers:
        - name: ok-api-service
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
    service: ok-api
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
  your C++ application](https://docs.docker.com/guides/cpp/configure-ci-cd/).
- A NodePort service, which will route traffic from port 30001 on your host to
  port 8080 inside the pods it routes to, allowing you to reach your app
  from the network.

To learn more about Kubernetes objects, see the [Kubernetes documentation](https://kubernetes.io/docs/home/).

## Deploy and check your application

1. In a terminal, navigate to `c-plus-plus-docker` and deploy your application to
  Kubernetes.
  ```console
  $ kubectl apply -f docker-kubernetes.yml
  ```
  You should see output that looks like the following, indicating your Kubernetes objects were created successfully.
  ```text
  deployment.apps/docker-c-plus-plus-demo created
  service/service-entrypoint created
  ```
2. Make sure everything worked by listing your deployments.
  ```console
  $ kubectl get deployments
  ```
  Your deployment should be listed as follows:
  ```shell
  NAME                     READY   UP-TO-DATE   AVAILABLE    AGE
  docker-c-plus-plus-demo   1/1     1            1           10s
  ```
  This indicates all one of the pods you asked for in your YAML are up and running. Do the same check for your services.
  ```console
  $ kubectl get services
  ```
  You should get output like the following.
  ```shell
  NAME                 TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
  kubernetes           ClusterIP   10.96.0.1        <none>        443/TCP          88m
  service-entrypoint   NodePort    10.105.145.223   <none>        8080:30001/TCP   83s
  ```
  In addition to the default `kubernetes` service, you can see your `service-entrypoint` service, accepting traffic on port 30001/TCP.
3. In a browser, visit the following address. You should see the message `{"Status" : "OK"}`.
  ```console
  http://localhost:30001/
  ```
4. Run the following command to tear down your application.
  ```console
  $ kubectl delete -f docker-kubernetes.yml
  ```

## Summary

In this section, you learned how to use Docker Desktop to deploy your C++ application to a fully-featured Kubernetes environment on your development machine.

Related information:

- [Kubernetes documentation](https://kubernetes.io/docs/home/)
- [Deploy on Kubernetes with Docker Desktop](https://docs.docker.com/desktop/use-desktop/kubernetes/)
- [Swarm mode overview](https://docs.docker.com/engine/swarm/)

---

# Use containers for C++ development

> Learn how to develop your C++ application locally.

# Use containers for C++ development

   Table of contents

---

## Prerequisites

Complete [Containerize a C++ application](https://docs.docker.com/guides/cpp/containerize/).

## Overview

In this section, you'll learn how to set up a development environment for your containerized application. This includes:

- Configuring Compose to automatically update your running Compose services as you edit and save your code

## Get the sample application

Clone the sample application to use with this guide. Open a terminal, change directory to a directory that you want to work in, and run the following command to clone the repository:

```console
$ git clone https://github.com/dockersamples/c-plus-plus-docker.git && cd c-plus-plus-docker
```

## Automatically update services

Use Compose Watch to automatically update your running Compose services as you
edit and save your code. For more details about Compose Watch, see
[Use Compose
Watch](https://docs.docker.com/compose/how-tos/file-watch/).

Open your `compose.yml` file in an IDE or text editor and then add the Compose Watch instructions. The following example shows how to add Compose Watch to your `compose.yml` file.

| 123456789101112 | services:ok-api:image:ok-apibuild:context:.dockerfile:Dockerfileports:-"8080:8080"develop:watch:-action:rebuildpath:. |
| --- | --- |

Run the following command to run your application with Compose Watch.

```console
$ docker compose watch
```

Now, if you modify your `ok_api.cpp` you will see the changes in real time without re-building the image.

To test it out, open the `ok_api.cpp` file in your favorite text editor and change the message from `{"Status" : "OK"}` to `{"Status" : "Updated"}`. Save the file and refresh your browser at [http://localhost:8080](http://localhost:8080). You should see the updated message.

Press `ctrl+c` in the terminal to stop your application.

## Summary

In this section, you also learned how to use Compose Watch to automatically rebuild and run your container when you update your code.

Related information:

- [Compose file reference](https://docs.docker.com/reference/compose-file/)
- [Compose file watch](https://docs.docker.com/compose/how-tos/file-watch/)
- [Multi-stage builds](https://docs.docker.com/build/building/multi-stage/)

## Next steps

In the next section, you'll take a look at how to set up a CI/CD pipeline using GitHub Actions.

---

# Create a multi

> Learn how to create a multi-stage build for a C++ application.

# Create a multi-stage build for your C++ application

   Table of contents

---

## Prerequisites

- You have a [Git client](https://git-scm.com/downloads). The examples in this section use a command-line based Git client, but you can use any client.

## Overview

This section walks you through creating a multi-stage Docker build for a C++ application.
A multi-stage build is a Docker feature that allows you to use different base images for different stages of the build process,
so you can optimize the size of your final image and separate build dependencies from runtime dependencies.

The standard practice for compiled languages like C++ is to have a build stage that compiles the code and a runtime stage that runs the compiled binary,
because the build dependencies are not needed at runtime.

## Get the sample application

Let's use a simple C++ application that prints `Hello, World!` to the terminal. To do so, clone the sample repository to use with this guide:

```bash
$ git clone https://github.com/dockersamples/c-plus-plus-docker.git
```

The example for this section is under the `hello` directory in the repository. Get inside it and take a look at the files:

```bash
$ cd c-plus-plus-docker/hello
$ ls
```

You should see the following files:

```text
Dockerfile  hello.cpp
```

## Check the Dockerfile

Open the `Dockerfile` in an IDE or text editor. The `Dockerfile` contains the instructions for building the Docker image.

```Dockerfile
# Stage 1: Build stage
FROM ubuntu:latest AS build

# Install build-essential for compiling C++ code
RUN apt-get update && apt-get install -y build-essential

# Set the working directory
WORKDIR /app

# Copy the source code into the container
COPY hello.cpp .

# Compile the C++ code statically to ensure it doesn't depend on runtime libraries
RUN g++ -o hello hello.cpp -static

# Stage 2: Runtime stage
FROM scratch

# Copy the static binary from the build stage
COPY --from=build /app/hello /hello

# Command to run the binary
CMD ["/hello"]
```

The `Dockerfile` has two stages:

1. **Build stage**: This stage uses the `ubuntu:latest` image to compile the C++ code and create a static binary.
2. **Runtime stage**: This stage uses the `scratch` image, which is an empty image, to copy the static binary from the build stage and run it.

## Build the Docker image

To build the Docker image, run the following command in the `hello` directory:

```bash
$ docker build -t hello .
```

The `-t` flag tags the image with the name `hello`.

## Run the Docker container

To run the Docker container, use the following command:

```bash
$ docker run hello
```

You should see the output `Hello, World!` in the terminal.

## Summary

In this section, you learned how to create a multi-stage build for a C++ application. Multi-stage builds help you optimize the size of your final image and separate build dependencies from runtime dependencies.
In this example, the final image only contains the static binary and doesn't include any build dependencies.

As the image has an empty base, the usual OS tools are also absent. So, for example, you can't run a simple `ls` command in the container:

```bash
$ docker run hello ls
```

This makes the image very lightweight and secure.
