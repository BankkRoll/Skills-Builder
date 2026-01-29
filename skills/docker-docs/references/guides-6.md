# Test your Deno deployment and more

# Test your Deno deployment

> Learn how to develop locally using Kubernetes

# Test your Deno deployment

   Table of contents

---

## Prerequisites

- Complete all the previous sections of this guide, starting with [Containerize a Deno application](https://docs.docker.com/guides/deno/containerize/).
- [Turn on Kubernetes](https://docs.docker.com/desktop/use-desktop/kubernetes/#enable-kubernetes) in Docker Desktop.

## Overview

In this section, you'll learn how to use Docker Desktop to deploy your application to a fully-featured Kubernetes environment on your development machine. This allows you to test and debug your workloads on Kubernetes locally before deploying.

## Create a Kubernetes YAML file

In your `deno-docker` directory, create a file named
`docker-kubernetes.yml`. Open the file in an IDE or text editor and add
the following contents. Replace `DOCKER_USERNAME/REPO_NAME` with your Docker
username and the name of the repository that you created in [Configure CI/CD for
your Deno application](https://docs.docker.com/guides/deno/configure-ci-cd/).

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: docker-deno-demo
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: deno-api
  template:
    metadata:
      labels:
        app: deno-api
    spec:
      containers:
       - name: deno-api
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
    app: deno-api
  ports:
  - port: 8000
    targetPort: 8000
    nodePort: 30001
```

In this Kubernetes YAML file, there are two objects, separated by the `---`:

- A Deployment, describing a scalable group of identical pods. In this case,
  you'll get just one replica, or copy of your pod. That pod, which is
  described under `template`, has just one container in it. The
  container is created from the image built by GitHub Actions in [Configure CI/CD for
  your Deno application](https://docs.docker.com/guides/deno/configure-ci-cd/).
- A NodePort service, which will route traffic from port 30001 on your host to
  port 8000 inside the pods it routes to, allowing you to reach your app
  from the network.

To learn more about Kubernetes objects, see the [Kubernetes documentation](https://kubernetes.io/docs/home/).

## Deploy and check your application

1. In a terminal, navigate to `deno-docker` and deploy your application to
  Kubernetes.
  ```console
  $ kubectl apply -f docker-kubernetes.yml
  ```
  You should see output that looks like the following, indicating your Kubernetes objects were created successfully.
  ```text
  deployment.apps/docker-deno-demo created
  service/service-entrypoint created
  ```
2. Make sure everything worked by listing your deployments.
  ```console
  $ kubectl get deployments
  ```
  Your deployment should be listed as follows:
  ```shell
  NAME                 READY   UP-TO-DATE   AVAILABLE    AGE
  docker-deno-demo       1/1     1            1           10s
  ```
  This indicates all one of the pods you asked for in your YAML are up and running. Do the same check for your services.
  ```console
  $ kubectl get services
  ```
  You should get output like the following.
  ```shell
  NAME                 TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
  kubernetes           ClusterIP   10.96.0.1        <none>        443/TCP          88m
  service-entrypoint   NodePort    10.105.145.223   <none>        8000:30001/TCP   83s
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

In this section, you learned how to use Docker Desktop to deploy your Deno application to a fully-featured Kubernetes environment on your development machine.

Related information:

- [Kubernetes documentation](https://kubernetes.io/docs/home/)
- [Deploy on Kubernetes with Docker Desktop](https://docs.docker.com/desktop/use-desktop/kubernetes/)
- [Swarm mode overview](https://docs.docker.com/engine/swarm/)

---

# Use containers for Deno development

> Learn how to develop your Deno application locally.

# Use containers for Deno development

   Table of contents

---

## Prerequisites

Complete [Containerize a Deno application](https://docs.docker.com/guides/deno/containerize/).

## Overview

In this section, you'll learn how to set up a development environment for your containerized application. This includes:

- Configuring Compose to automatically update your running Compose services as you edit and save your code

## Get the sample application

Clone the sample application to use with this guide. Open a terminal, change directory to a directory that you want to work in, and run the following command to clone the repository:

```console
$ git clone https://github.com/dockersamples/docker-deno.git && cd docker-deno
```

## Automatically update services

Use Compose Watch to automatically update your running Compose services as you
edit and save your code. For more details about Compose Watch, see
[Use Compose
Watch](https://docs.docker.com/compose/how-tos/file-watch/).

Open your `compose.yml` file in an IDE or text editor and then add the Compose Watch instructions. The following example shows how to add Compose Watch to your `compose.yml` file.

| 123456789101112 | services:server:image:deno-serverbuild:context:.dockerfile:Dockerfileports:-"8000:8000"develop:watch:-action:rebuildpath:. |
| --- | --- |

Run the following command to run your application with Compose Watch.

```console
$ docker compose watch
```

Now, if you modify your `server.ts` you will see the changes in real time without re-building the image.

To test it out, open the `server.ts` file in your favorite text editor and change the message from `{"Status" : "OK"}` to `{"Status" : "Updated"}`. Save the file and refresh your browser at `http://localhost:8000`. You should see the updated message.

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

# Deno language

> Containerize and develop Deno applications using Docker.

# Deno language-specific guide

Table of contents

---

The Deno getting started guide teaches you how to create a containerized Deno application using Docker.

> **Acknowledgment**
>
>
>
> Docker would like to thank [Pradumna Saraf](https://twitter.com/pradumna_saraf) for his contribution to this guide.

## What will you learn?

- Containerize and run a Deno application using Docker
- Set up a local environment to develop a Deno application using containers
- Use Docker Compose to run the application.
- Configure a CI/CD pipeline for a containerized Deno application using GitHub Actions
- Deploy your containerized application locally to Kubernetes to test and debug your deployment

## Prerequisites

- Basic understanding of JavaScript is assumed.
- You must have familiarity with Docker concepts like containers, images, and Dockerfiles. If you are new to Docker, you can start with the
  [Docker basics](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/) guide.

After completing the Deno getting started modules, you should be able to containerize your own Deno application based on the examples and instructions provided in this guide.

Start by containerizing an existing Deno application.

## Modules

1. [Containerize your app](https://docs.docker.com/guides/deno/containerize/)
  Learn how to containerize a Deno application.
2. [Develop your app](https://docs.docker.com/guides/deno/develop/)
  Learn how to develop your Deno application locally.
3. [Configure CI/CD](https://docs.docker.com/guides/deno/configure-ci-cd/)
  Learn how to configure CI/CD using GitHub Actions for your Deno application.
4. [Test your deployment](https://docs.docker.com/guides/deno/deploy/)
  Learn how to develop locally using Kubernetes

---

# Mocking OAuth services in testing with Dex

> Mocking OAuth services in testing with Dex

# Mocking OAuth services in testing with Dex

   Table of contents

---

Dex is an open-source OpenID Connect (OIDC) and OAuth 2.0 identity provider that can be configured to authenticate against various backend identity providers, such as LDAP, SAML, and OAuth. Running Dex in a Docker container allows developers to simulate an OAuth 2.0 server for testing and development purposes. This guide will walk you through setting up Dex as an OAuth mock server using Docker containers.

Nowadays OAuth is the preferred choice to authenticate in web services, the highest part of them give the possibility to access using popular OAuth services like GitHub, Google or Apple. Using OAuth guarantees a higher level of security and simplification since it is not necessary to create new profiles for each service. This means that, by allowing applications to access resources on behalf of users without sharing passwords, OAuth minimizes the risk of credential exposure.

In this guide, you'll learn how to:

- Use Docker to launch up a Dex container.
- Use mock OAuth in the GitHub Action (GHA) without relying on an external OAuth provider.

## Using Dex with Docker

The official [Docker image for Dex](https://hub.docker.com/r/dexidp/dex/) provides a convenient way to deploy and manage Dex instances. Dex is available for various CPU architectures, including amd64, armv7, and arm64, ensuring compatibility with different devices and platforms. You can learn more about Dex standalone on the [Dex docs site](https://dexidp.io/docs/getting-started/).

### Prerequisites

[Docker Compose](https://docs.docker.com/compose/): Recommended for managing multi-container Docker applications.

### Setting Up Dex with Docker

Begin by creating a directory for your Dex project:

```bash
mkdir dex-mock-server
cd dex-mock-server
```

Organize your project with the following structure:

```bash
dex-mock-server/
├── config.yaml
└── compose.yaml
```

Create the Dex Configuration File:
The config.yaml file defines Dex's settings, including connectors, clients, and storage. For a mock server setup, you can use the following minimal configuration:

```yaml
# config.yaml
issuer: http://localhost:5556/dex
storage:
  type: memory
web:
  http: 0.0.0.0:5556
staticClients:
  - id: example-app
    redirectURIs:
      - 'http://localhost:5555/callback'
    name: 'Example App'
    secret: ZXhhbXBsZS1hcHAtc2VjcmV0
enablePasswordDB: true
staticPasswords:
  - email: "admin@example.com"
    hash: "$2a$10$2b2cU8CPhOTaGrs1HRQuAueS7JTT5ZHsHSzYiFPm1leZck7Mc8T4W"
    username: "admin"
    userID: "1234"
```

Explanation:

- issuer: The public URL of Dex.
- storage: Using in-memory storage for simplicity.
- web: Dex will listen on port 5556.
- staticClients: Defines a client application (example-app) with its redirect URI and secret.
- enablePasswordDB: Enables static password authentication.
- staticPasswords: Defines a static user for authentication. The hash is a bcrypt hash of the password.

> Note
>
> Ensure the hash is a valid bcrypt hash of your desired password. You can generate this using tools like [bcrypt-generator.com](https://bcrypt-generator.com/).
> or use CLI tools like [htpasswd](https://httpd.apache.org/docs/2.4/programs/htpasswd.html) like in this following example:`echo password | htpasswd -BinC 10 admin | cut -d: -f2`

With Docker Compose configured, start Dex:

```yaml
# docker-compose.yaml

services:
  dex:
    image: dexidp/dex:latest
    container_name: dex
    ports:
      - "5556:5556"
    volumes:
      - ./config.yaml:/etc/dex/config.yaml
    command: ["dex", "serve", "/etc/dex/config.yaml"]
```

Now it is possible to run the container using the `docker compose` command.

```bash
docker compose up -d
```

This command will download the Dex Docker image (if not already available) and start the container in detached mode.

To verify that Dex is running, check the logs to ensure Dex started successfully:

```bash
docker compose logs -f dex
```

You should see output indicating that Dex is listening on the specified port.

### Using Dex OAuth testing in GHA

To test the OAuth flow, you'll need a client application configured to authenticate against Dex. One of the most typical use cases is to use it inside GitHub Actions. Since Dex supports mock authentication, you can predefine test users as suggested in the [docs](https://dexidp.io/docs). The `config.yaml` file should looks like:

```yaml
issuer: http://127.0.0.1:5556/dex

storage:
  type: memory

web:
  http: 0.0.0.0:5556

oauth2:
  skipApprovalScreen: true

staticClients:
  - name: TestClient
    id: client_test_id
    secret: client_test_secret
    redirectURIs:
      - http://{ip-your-app}/path/to/callback/ # example: http://localhost:5555/callback

connectors:
# mockCallback connector always returns the user 'kilgore@kilgore.trout'.
- type: mockCallback
  id: mock
  name: Mock
```

Now you can insert the Dex service inside your `~/.github/workflows/ci.yaml` file:

```yaml
[...]
jobs:
  test-oauth:
    runs-on: ubuntu-latest
    steps:
      - name: Install Dex
        run: |
          curl -L https://github.com/dexidp/dex/releases/download/v2.37.0/dex_linux_amd64 -o dex
          chmod +x dex

      - name: Start Dex Server
        run: |
          nohup ./dex serve config.yaml > dex.log 2>&1 &
          sleep 5  # Give Dex time to start
[...]
```

### Conclusion

By following this guide, you've set up Dex as an OAuth mock server using Docker. This setup is invaluable for testing and development, allowing you to simulate OAuth flows without relying on external identity providers. For more advanced configurations and integrations, refer to the [Dex documentation](https://dexidp.io/docs/).

---

# Migrate from Alpine or Debian

> Step-by-step guide to migrate from Docker Official Images to Docker Hardened Images

# Migrate from Alpine or Debian

   Table of contents

---

Docker Hardened Images (DHI) come in both [Alpine-based and Debian-based
variants](https://docs.docker.com/dhi/explore/available/). In many cases, migrating from another image
based on these distributions is as simple as changing the base image in your
Dockerfile.

This guide helps you migrate from an existing Alpine-based or Debian-based
Docker Official Image (DOI) to DHI.

If you're currently using a Debian-based Docker Official Image, migrate to the
Debian-based DHI variant. If you're using an Alpine-based image, migrate to the
Alpine-based DHI variant. This minimizes changes to package management and
dependencies during migration.

## Key differences

When migrating from non-hardened images to DHI, be aware of these key differences:

| Item | Non-hardened images | Docker Hardened Images |
| --- | --- | --- |
| Package management | Package managers generally available in all images. | Package managers generally only available in images with adevtag. Runtime images don't contain package managers. Use multi-stage builds and copy necessary artifacts from the build stage to the runtime stage. |
| Non-root user | Usually runs as root by default | Runtime variants run as the nonroot user by default. Ensure that necessary files and directories are accessible to the nonroot user. |
| Multi-stage build | Optional | Recommended. Use images with adevorsdktags for build stages and non-dev images for runtime. |
| TLS certificates | May need to be installed | Contain standard TLS certificates by default. There is no need to install TLS certificates. |
| Ports | Can bind to privileged ports (below 1024) when running as root | Run as a nonroot user by default. Applications can't bind to privileged ports (below 1024) when running in Kubernetes or in Docker Engine versions older than 20.10. Configure your application to listen on port 1025 or higher inside the container. |
| Entry point | Varies by image | May have different entry points than Docker Official Images. Inspect entry points and update your Dockerfile if necessary. |
| Shell | Shell generally available in all images | Runtime images don't contain a shell. Usedevimages in build stages to run shell commands and then copy artifacts to the runtime stage. |

## Migration steps

### Step 1: Update the base image in your Dockerfile

Update the base image in your application's Dockerfile to a hardened image. This
is typically going to be an image tagged as `dev` or `sdk` because it has the tools
needed to install packages and dependencies.

The following example diff snippet from a Dockerfile shows the old base image
replaced by the new hardened image.

> Note
>
> You must authenticate to `dhi.io` before you can pull Docker Hardened Images.
> Use your Docker ID credentials (the same username and password you use for
> Docker Hub). If you don't have a Docker account, [create
> one](https://docs.docker.com/accounts/create-account/) for free.
>
>
>
> Run `docker login dhi.io` to authenticate.

```diff
- ## Original base image
- FROM golang:1.25

+ ## Updated to use hardened base image
+ FROM dhi.io/golang:1.25-debian12-dev
```

Note that DHI does not have a `latest` tag in order to promote best practices
around image versioning. Ensure that you specify the appropriate version tag for
your image. To find the right tag, explore the available tags in the [DHI
Catalog](https://hub.docker.com/hardened-images/catalog/). In addition, the
distribution base is specified in the tag (for example, `-alpine3.22` or
`-debian12`), so be sure to select the correct variant for your application.

### Step 2: Update the runtime image in your Dockerfile

> Note
>
> Multi-stage builds are recommended to keep your final image minimal and
> secure. Single-stage builds are supported, but they include the full `dev` image
> and therefore result in a larger image with a broader attack surface.

To ensure that your final image is as minimal as possible, you should use a
[multi-stage build](https://docs.docker.com/build/building/multi-stage/). All stages in your
Dockerfile should use a hardened image. While intermediary stages will typically
use images tagged as `dev` or `sdk`, your final runtime stage should use a runtime image.

Utilize the build stage to compile your application and copy the resulting
artifacts to the final runtime stage. This ensures that your final image is
minimal and secure.

The following example shows a multi-stage Dockerfile with a build stage and runtime stage:

```dockerfile
# Build stage
FROM dhi.io/golang:1.25-debian12-dev AS builder
WORKDIR /app
COPY . .
RUN go build -o myapp

# Runtime stage
FROM dhi.io/golang:1.25-debian12
WORKDIR /app
COPY --from=builder /app/myapp .
ENTRYPOINT ["/app/myapp"]
```

After updating your Dockerfile, build and test your application. If you encounter
issues, see the
[Troubleshoot](https://docs.docker.com/dhi/troubleshoot/) guide for common
problems and solutions.

## Language-specific examples

See the examples section for language-specific migration examples:

- [Go](https://docs.docker.com/dhi/migration/examples/go/)
- [Python](https://docs.docker.com/dhi/migration/examples/python/)
- [Node.js](https://docs.docker.com/dhi/migration/examples/node/)

---

# Migrate from Wolfi

> Step-by-step guide to migrate from Wolfi distribution images to Docker Hardened Images

# Migrate from Wolfi

   Table of contents

---

This guide helps you migrate from Wolfi-based images to Docker Hardened
Images (DHI). Generally, the migration process is straightforward since Wolfi is
Alpine-like and DHI provides an Alpine-based hardened image.

Like other hardened images, DHI provides comprehensive
[attestations](https://docs.docker.com/dhi/core-concepts/attestations/) including SBOMs and provenance,
allowing you to
[verify](https://docs.docker.com/dhi/how-to/verify/) image signatures and
[scan](https://docs.docker.com/dhi/how-to/scan/) for vulnerabilities to ensure the security
and integrity of your images.

## Migration steps

The following example demonstrates how to migrate a Dockerfile from a
Wolfi-based image to an Alpine-based Docker Hardened Image.

### Step 1: Update the base image in your Dockerfile

Update the base image in your application's Dockerfile to a hardened image. This
is typically going to be an image tagged as `dev` or `sdk` because it has the tools
needed to install packages and dependencies.

The following example diff snippet from a Dockerfile shows the old base image
replaced by the new hardened image.

> Note
>
> You must authenticate to `dhi.io` before you can pull Docker Hardened Images.
> Use your Docker ID credentials (the same username and password you use for
> Docker Hub). If you don't have a Docker account, [create
> one](https://docs.docker.com/accounts/create-account/) for free.
>
>
>
> Run `docker login dhi.io` to authenticate.

```diff
- ## Original base image
- FROM cgr.dev/chainguard/go:latest-dev

+ ## Updated to use hardened base image
+ FROM dhi.io/golang:1.25-alpine3.22-dev
```

Note that DHI does not have a `latest` tag in order to promote best practices
around image versioning. Ensure that you specify the appropriate version tag for your image. To find the right tag, explore the available tags in the [DHI Catalog](https://hub.docker.com/hardened-images/catalog/).

### Step 2: Update the runtime image in your Dockerfile

> Note
>
> Multi-stage builds are recommended to keep your final image minimal and
> secure. Single-stage builds are supported, but they include the full `dev` image
> and therefore result in a larger image with a broader attack surface.

To ensure that your final image is as minimal as possible, you should use a
[multi-stage build](https://docs.docker.com/build/building/multi-stage/). All stages in your
Dockerfile should use a hardened image. While intermediary stages will typically
use images tagged as `dev` or `sdk`, your final runtime stage should use a runtime image.

Utilize the build stage to compile your application and copy the resulting
artifacts to the final runtime stage. This ensures that your final image is
minimal and secure.

The following example shows a multi-stage Dockerfile with a build stage and runtime stage:

```dockerfile
# Build stage
FROM dhi.io/golang:1.25-alpine3.22-dev AS builder
WORKDIR /app
COPY . .
RUN go build -o myapp

# Runtime stage
FROM dhi.io/golang:1.25-alpine3.22
WORKDIR /app
COPY --from=builder /app/myapp .
ENTRYPOINT ["/app/myapp"]
```

After updating your Dockerfile, build and test your application. If you encounter
issues, see the
[Troubleshoot](https://docs.docker.com/dhi/troubleshoot/) guide for common
problems and solutions.

## Language-specific examples

See the examples section for language-specific migration examples:

- [Go](https://docs.docker.com/dhi/migration/examples/go/)
- [Python](https://docs.docker.com/dhi/migration/examples/python/)
- [Node.js](https://docs.docker.com/dhi/migration/examples/node/)

---

# Go

> Migrate a Go application to Docker Hardened Images

# Go

---

This example shows how to migrate a Go application to Docker Hardened Images.

The following examples show Dockerfiles before and after migration to Docker
Hardened Images. Each example includes five variations:

- Before (Ubuntu): A sample Dockerfile using Ubuntu-based images, before migrating to DHI
- Before (Wolfi): A sample Dockerfile using Wolfi distribution images, before migrating to DHI
- Before (DOI): A sample Dockerfile using Docker Official Images, before migrating to DHI
- After (multi-stage): A sample Dockerfile after migrating to DHI with multi-stage builds (recommended for minimal, secure images)
- After (single-stage): A sample Dockerfile after migrating to DHI with single-stage builds (simpler but results in a larger image with a broader attack surface)

> Note
>
> Multi-stage builds are recommended for most use cases. Single-stage builds are
> supported for simplicity, but come with tradeoffs in size and security.
>
>
>
> You must authenticate to `dhi.io` before you can pull Docker Hardened Images.
> Use your Docker ID credentials (the same username and password you use for
> Docker Hub). If you don't have a Docker account, [create
> one](https://docs.docker.com/accounts/create-account/) for free.
>
>
>
> Run `docker login dhi.io` to authenticate.

```dockerfile
#syntax=docker/dockerfile:1

FROM ubuntu/go:1.22-24.04

WORKDIR /app
ADD . ./

# Install any additional packages if needed using apt
# RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

RUN CGO_ENABLED=0 GOOS=linux go build -a -ldflags="-s -w" --installsuffix cgo -o main .

ENTRYPOINT ["/app/main"]
```

```dockerfile
#syntax=docker/dockerfile:1

FROM cgr.dev/chainguard/go:latest-dev

WORKDIR /app
ADD . ./

# Install any additional packages if needed using apk
# RUN apk add --no-cache git

RUN CGO_ENABLED=0 GOOS=linux go build -a -ldflags="-s -w" --installsuffix cgo -o main .

ENTRYPOINT ["/app/main"]
```

```dockerfile
#syntax=docker/dockerfile:1

FROM golang:latest

WORKDIR /app
ADD . ./

# Install any additional packages if needed using apt
# RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

RUN CGO_ENABLED=0 GOOS=linux go build -a -ldflags="-s -w" --installsuffix cgo -o main .

ENTRYPOINT ["/app/main"]
```

```dockerfile
#syntax=docker/dockerfile:1

# === Build stage: Compile Go application ===
FROM dhi.io/golang:1-alpine3.21-dev AS builder

WORKDIR /app
ADD . ./

# Install any additional packages if needed using apk
# RUN apk add --no-cache git

RUN CGO_ENABLED=0 GOOS=linux go build -a -ldflags="-s -w" --installsuffix cgo -o main .

# === Final stage: Create minimal runtime image ===
FROM dhi.io/golang:1-alpine3.21

WORKDIR /app
COPY --from=builder /app/main  /app/main

ENTRYPOINT ["/app/main"]
```

```dockerfile
#syntax=docker/dockerfile:1

FROM dhi.io/golang:1-alpine3.21-dev

WORKDIR /app
ADD . ./

# Install any additional packages if needed using apk
# RUN apk add --no-cache git

RUN CGO_ENABLED=0 GOOS=linux go build -a -ldflags="-s -w" --installsuffix cgo -o main .

ENTRYPOINT ["/app/main"]
```

---

# Node.js

> Migrate a Node.js application to Docker Hardened Images

# Node.js

---

This example shows how to migrate a Node.js application to Docker Hardened Images.

The following examples show Dockerfiles before and after migration to Docker
Hardened Images. Each example includes five variations:

- Before (Ubuntu): A sample Dockerfile using Ubuntu-based images, before migrating to DHI
- Before (Wolfi): A sample Dockerfile using Wolfi distribution images, before migrating to DHI
- Before (DOI): A sample Dockerfile using Docker Official Images, before migrating to DHI
- After (multi-stage): A sample Dockerfile after migrating to DHI with multi-stage builds (recommended for minimal, secure images)
- After (single-stage): A sample Dockerfile after migrating to DHI with single-stage builds (simpler but results in a larger image with a broader attack surface)

> Note
>
> Multi-stage builds are recommended for most use cases. Single-stage builds are
> supported for simplicity, but come with tradeoffs in size and security.
>
>
>
> You must authenticate to `dhi.io` before you can pull Docker Hardened Images.
> Use your Docker ID credentials (the same username and password you use for
> Docker Hub). If you don't have a Docker account, [create
> one](https://docs.docker.com/accounts/create-account/) for free.
>
>
>
> Run `docker login dhi.io` to authenticate.

```dockerfile
#syntax=docker/dockerfile:1

FROM ubuntu/node:18-24.04_edge
WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install

COPY . .

CMD ["node", "index.js"]
```

```dockerfile
#syntax=docker/dockerfile:1

FROM cgr.dev/chainguard/node:latest-dev
WORKDIR /usr/src/app

COPY package*.json ./

# Install any additional packages if needed using apk
# RUN apk add --no-cache python3 make g++

RUN npm install

COPY . .

CMD ["node", "index.js"]
```

```dockerfile
#syntax=docker/dockerfile:1

FROM node:latest
WORKDIR /usr/src/app

COPY package*.json ./

# Install any additional packages if needed using apt
# RUN apt-get update && apt-get install -y python3 make g++ && rm -rf /var/lib/apt/lists/*

RUN npm install

COPY . .

CMD ["node", "index.js"]
```

```dockerfile
#syntax=docker/dockerfile:1

# === Build stage: Install dependencies and build application ===
FROM dhi.io/node:23-alpine3.21-dev AS builder
WORKDIR /usr/src/app

COPY package*.json ./

# Install any additional packages if needed using apk
# RUN apk add --no-cache python3 make g++

RUN npm install

COPY . .

# === Final stage: Create minimal runtime image ===
FROM dhi.io/node:23-alpine3.21
ENV PATH=/app/node_modules/.bin:$PATH

COPY --from=builder --chown=node:node /usr/src/app /app

WORKDIR /app

CMD ["index.js"]
```

```dockerfile
#syntax=docker/dockerfile:1

FROM dhi.io/node:23-alpine3.21-dev
WORKDIR /usr/src/app

COPY package*.json ./

# Install any additional packages if needed using apk
# RUN apk add --no-cache python3 make g++

RUN npm install

COPY . .

CMD ["node", "index.js"]
```

---

# Python

> Migrate a Python application to Docker Hardened Images

# Python

---

This example shows how to migrate a Python application to Docker Hardened Images.

The following examples show Dockerfiles before and after migration to Docker
Hardened Images. Each example includes five variations:

- Before (Ubuntu): A sample Dockerfile using Ubuntu-based images, before migrating to DHI
- Before (Wolfi): A sample Dockerfile using Wolfi distribution images, before migrating to DHI
- Before (DOI): A sample Dockerfile using Docker Official Images, before migrating to DHI
- After (multi-stage): A sample Dockerfile after migrating to DHI with multi-stage builds (recommended for minimal, secure images)
- After (single-stage): A sample Dockerfile after migrating to DHI with single-stage builds (simpler but results in a larger image with a broader attack surface)

> Note
>
> Multi-stage builds are recommended for most use cases. Single-stage builds are
> supported for simplicity, but come with tradeoffs in size and security.
>
>
>
> You must authenticate to `dhi.io` before you can pull Docker Hardened Images.
> Run `docker login dhi.io` to authenticate.

```dockerfile
#syntax=docker/dockerfile:1

FROM ubuntu/python:3.13-24.04_stable AS builder

ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

WORKDIR /app

RUN python -m venv /app/venv
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

FROM ubuntu/python:3.13-24.04_stable

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

COPY app.py ./
COPY --from=builder /app/venv /app/venv

ENTRYPOINT [ "python", "/app/app.py" ]
```

```dockerfile
#syntax=docker/dockerfile:1

FROM cgr.dev/chainguard/python:latest-dev AS builder

ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

WORKDIR /app

RUN python -m venv /app/venv
COPY requirements.txt .

# Install any additional packages if needed using apk
# RUN apk add --no-cache gcc musl-dev

RUN pip install --no-cache-dir -r requirements.txt

FROM cgr.dev/chainguard/python:latest

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

COPY app.py ./
COPY --from=builder /app/venv /app/venv

ENTRYPOINT [ "python", "/app/app.py" ]
```

```dockerfile
#syntax=docker/dockerfile:1

FROM python:latest AS builder

ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

WORKDIR /app

RUN python -m venv /app/venv
COPY requirements.txt .

# Install any additional packages if needed using apt
# RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

FROM python:latest

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

COPY app.py ./
COPY --from=builder /app/venv /app/venv

ENTRYPOINT [ "python", "/app/app.py" ]
```

```dockerfile
#syntax=docker/dockerfile:1

# === Build stage: Install dependencies and create virtual environment ===
FROM dhi.io/python:3.13-alpine3.21-dev AS builder

ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

WORKDIR /app

RUN python -m venv /app/venv
COPY requirements.txt .

# Install any additional packages if needed using apk
# RUN apk add --no-cache gcc musl-dev

RUN pip install --no-cache-dir -r requirements.txt

# === Final stage: Create minimal runtime image ===
FROM dhi.io/python:3.13-alpine3.21

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

COPY app.py ./
COPY --from=builder /app/venv /app/venv

ENTRYPOINT [ "python", "/app/app.py" ]
```

```dockerfile
#syntax=docker/dockerfile:1

FROM dhi.io/python:3.13-alpine3.21-dev

ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

WORKDIR /app

RUN python -m venv /app/venv
COPY requirements.txt .

# Install any additional packages if needed using apk
# RUN apk add --no-cache gcc musl-dev

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py ./

ENTRYPOINT [ "python", "/app/app.py" ]
```

---

# Demo: Using Docker Build Cloud in CI

> Learn how to use Docker Build Cloud to build your app faster in CI.

# Demo: Using Docker Build Cloud in CI

---

Docker Build Cloud can significantly decrease the time it takes for your CI builds
take to run, saving you time and money.

Since the builds run remotely, your CI runner can still use the Docker tooling CLI
without needing elevated permissions, making your builds more secure by default.

In this demo, you will see:

- How to integrate Docker Build Cloud into a variety of CI platforms
- How to use Docker Build Cloud in GitHub Actions to build multi-architecture images
- Speed differences between a workflow using Docker Build Cloud and a workflow running natively
- How to use Docker Build Cloud in a GitLab Pipeline

---

# Common challenges and questions

> Explore common challenges and questions related to Docker Build Cloud.

# Common challenges and questions

   Table of contents

---

### Is Docker Build Cloud a standalone product or a part of Docker Desktop?

Docker Build Cloud is a service that can be used both with Docker Desktop and
standalone. It lets you build your container images faster, both locally and in
CI, with builds running on cloud infrastructure. The service uses a remote
build cache, ensuring fast builds anywhere and for all team members.

When used with Docker Desktop, the
[Builds view](https://docs.docker.com/desktop/use-desktop/builds/)
works with Docker Build Cloud out-of-the-box. It shows information about your
builds and those initiated by your team members using the same builder,
enabling collaborative troubleshooting.

To use Docker Build Cloud without Docker Desktop, you must
[download and install](https://docs.docker.com/build-cloud/setup/#use-docker-build-cloud-without-docker-desktop)
a version of Buildx with support for Docker Build Cloud (the `cloud` driver).
If you plan on building with Docker Build Cloud using the `docker compose build` command, you also need a version of Docker Compose that supports Docker
Build Cloud.

### How does Docker Build Cloud work with Docker Compose?

Docker Compose works out of the box with Docker Build Cloud. Install the Docker
Build Cloud-compatible client (buildx) and it works with both commands.

### How many minutes are included in Docker Build Cloud Team plans?

Pricing details for Docker Build Cloud can be found on the [pricing page](https://www.docker.com/pricing/).

### I’m a Docker personal user. Can I try Docker Build Cloud?

Docker subscribers (Pro, Team, Business) receive a set number of minutes each
month, shared across the account, to use Build Cloud.

If you do not have a Docker subscription, you may sign up for a free Personal
account and start a trial of Docker Build Cloud. Personal accounts are limited to a
single user.

For teams to receive the shared cache benefit, they must either be on a Docker
Team or Docker Business subscription.

### Does Docker Build Cloud support CI platforms? Does it work with GitHub Actions?

Yes, Docker Build Cloud can be used with various CI platforms including GitHub
Actions, CircleCI, Jenkins, and others. It can speed up your build pipelines,
which means less time spent waiting and context switching.

Docker Build Cloud can be used with GitHub Actions to automate your build,
test, and deployment pipeline. Docker provides a set of official GitHub Actions
that you can use in your workflows.

Using GitHub Actions with Docker Build Cloud is straightforward. With a
one-line change in your GitHub Actions configuration, everything else stays the
same. You don't need to create new pipelines. Learn more in the
[CI
documentation](https://docs.docker.com/build-cloud/ci/) for Docker Build Cloud.

---

# Demo: set up and use Docker Build Cloud in development

> Learn how to use Docker Build Cloud for local builds.

# Demo: set up and use Docker Build Cloud in development

---

With Docker Build Cloud, you can easily shift the build workload from local machines
to the cloud, helping you achieve faster build times, especially for multi-platform builds.

In this demo, you'll see:

- How to setup the builder locally
- How to use Docker Build Cloud with Docker Compose
- How the image cache speeds up builds for others on your team

---

# Why Docker Build Cloud?

> Learn how Docker Build Cloud makes your builds faster.

# Why Docker Build Cloud?

---

Docker Build Cloud is a service that lets you build container images faster,
both locally and in CI. Builds run on cloud infrastructure optimally
dimensioned for your workloads, with no configuration required. The service
uses a remote build cache, ensuring fast builds anywhere and for all team
members.

Docker Build Cloud provides several benefits over local builds:

- Improved build speed
- Shared build cache
- Native multi-platform builds

There’s no need to worry about managing builders or infrastructure — simply
connect to your builders and start building. Each cloud builder provisioned to
an organization is completely isolated to a single Amazon EC2 instance, with a
dedicated EBS volume for build cache and encryption in transit. That means
there are no shared processes or data between cloud builders.

---

# Docker Build Cloud: Reclaim your time with fast, multi

> Learn how to build and deploy Docker images to the cloud with Docker Build Cloud.

# Docker Build Cloud: Reclaim your time with fast, multi-architecture builds

Table of contents

---

98% of developers spend up to an hour every day waiting for builds to finish
([Incredibuild: 2022 Big Dev Build Times](https://www.incredibuild.com/survey-report-2022)).
Heavy, complex builds can become a major roadblock for development teams,
slowing down both local development and CI/CD pipelines.

Docker Build Cloud speeds up image build times to improve developer
productivity, reduce frustrations, and help you shorten the release cycle.

## Who’s this for?

- Anyone who wants to tackle common causes of slow image builds: limited local
  resources, slow emulation, and lack of build collaboration across a team.
- Developers working on older machines who want to build faster.
- Development teams working on the same repository who want to cut wait times
  with a shared cache.
- Developers performing multi-architecture builds who don’t want to spend hours
  configuring and rebuilding for emulators.

## What you’ll learn

- Building container images faster locally and in CI
- Accelerating builds for multi-platform images
- Reusing pre-built images to expedite workflows

## Tools integration

Works well with Docker Compose, GitHub Actions, and other CI solutions

## Modules

1. [Why Docker Build Cloud?](https://docs.docker.com/guides/docker-build-cloud/why/)
  Learn how Docker Build Cloud makes your builds faster.
2. [Demo: set up and use Docker Build Cloud in development](https://docs.docker.com/guides/docker-build-cloud/dev/)
  Learn how to use Docker Build Cloud for local builds.
3. [Demo: Using Docker Build Cloud in CI](https://docs.docker.com/guides/docker-build-cloud/ci/)
  Learn how to use Docker Build Cloud to build your app faster in CI.
4. [Common challenges and questions](https://docs.docker.com/guides/docker-build-cloud/common-questions/)
  Explore common challenges and questions related to Docker Build Cloud.
