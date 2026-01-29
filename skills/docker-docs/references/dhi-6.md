# How and more

# How

> Step-by-step guidance for working with Docker Hardened Images, from discovery to debugging.

# How-tos

   Table of contents

---

This section provides practical, task-based guidance for working with Docker
Hardened Images (DHIs). Whether you're evaluating DHIs for the first time or
integrating them into a production CI/CD pipeline, these topics cover the key
tasks across the adoption journey, from discovery to debugging.

The topics are organized around the typical lifecycle of working with DHIs, but
you can use them as needed based on your specific workflow.

Explore the topics below that match your current needs.

## Discover

Explore available images and metadata in the DHI catalog.

[Explore Docker Hardened ImagesLearn how to find and evaluate image repositories, variants, metadata, and attestations in the DHI catalog on Docker Hub.](https://docs.docker.com/dhi/how-to/explore/)

## Adopt

Mirror trusted images, customize as needed, and integrate into your workflows.

[Mirror a Docker Hardened Image repositoryLearn how to mirror an image into your organization's namespace and optionally push it to another private registry.](https://docs.docker.com/dhi/how-to/mirror/)[Customize a Docker Hardened Image or chartLearn how to customize Docker Hardened Images and charts.](https://docs.docker.com/dhi/how-to/customize/)[Use a Docker Hardened ImageLearn how to pull, run, and reference Docker Hardened Images in Dockerfiles, CI pipelines, and standard development workflows.](https://docs.docker.com/dhi/how-to/use/)[Use a Docker Hardened Image in KubernetesLearn how to use Docker Hardened Images in Kubernetes deployments.](https://docs.docker.com/dhi/how-to/k8s/)[Use a Docker Hardened Image chartLearn how to use a Docker Hardened Image chart.](https://docs.docker.com/dhi/how-to/helm/)[Use Extended Lifecycle Support for Docker Hardened ImagesLearn how to use Extended Lifecycle Support with Docker Hardened Images.](https://docs.docker.com/dhi/how-to/els/)[Manage Docker Hardened Images and chartsLearn how to manage your mirrored and customized Docker Hardened Images in your organization.](https://docs.docker.com/dhi/how-to/manage/)

## Evaluate

Compare with other images to understand security improvements.

[Compare Docker Hardened ImagesLearn how to compare Docker Hardened Images with other container images to evaluate security improvements and differences.](https://docs.docker.com/dhi/how-to/compare/)

## Verify

Check signatures, SBOMs, and provenance, and scan for vulnerabilities.

[Verify a Docker Hardened Image or chartUse Docker Scout or cosign to verify signed attestations like SBOMs, provenance, and vulnerability data for Docker Hardened Images and charts.](https://docs.docker.com/dhi/how-to/verify/)[Scan Docker Hardened ImagesLearn how to scan Docker Hardened Images for known vulnerabilities using Docker Scout, Grype, or Trivy.](https://docs.docker.com/dhi/how-to/scan/)

## Govern

Enforce policies to maintain security and compliance.

[Enforce Docker Hardened Image usage with policiesLearn how to use image policies with Docker Scout for Docker Hardened Images.](https://docs.docker.com/dhi/how-to/policies/)

## Troubleshoot

Debug containers based on DHIs without modifying the image.

[Debug a Docker Hardened ImageUse Docker Debug to inspect a running container based on a hardened image without modifying it.](https://docs.docker.com/dhi/how-to/debug/)

---

# Migration checklist

> A checklist of considerations when migrating to Docker Hardened Images

# Migration checklist

   Table of contents

---

Use this checklist to ensure you address key considerations when migrating to Docker Hardened Images.

## Migration considerations

| Item | Action required |
| --- | --- |
| Base image | Update your DockerfileFROMstatements to reference a Docker Hardened Image instead of your current base image. |
| Package management | Install packages only indev-tagged images during build stages. Useapkfor Alpine-based images oraptfor Debian-based images. Copy the necessary artifacts to your runtime stage, as runtime images don't include package managers. |
| Non-root user | Verify that all files and directories your application needs are readable and writable by the nonroot user (UID 65532), as runtime images run as nonroot by default. |
| Multi-stage build | Usedevorsdk-tagged images for build stages where you need build tools and package managers. Use non-dev images for your final runtime stage. |
| TLS certificates | Remove any steps that install ca-certificates, as DHIs include ca-certificates by default. |
| Ports | Configure your application to listen on port 1025 or higher inside the container, as the nonroot user can't bind to privileged ports (below 1024) in Kubernetes or Docker Engine versions older than 20.10. |
| Entry point | Check the entry point of your chosen DHI usingdocker inspector the image documentation. Update your Dockerfile'sENTRYPOINTorCMDinstructions if your application relies on a different entry point. |
| No shell | Move any shell commands (RUN,SHELL) to build stages usingdev-tagged images. Runtime images don't include a shell, so copy all necessary artifacts from the build stage. |

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

# Migration examples

> Real-world examples of migrating to Docker Hardened Images

# Migration examples

   Table of contents

---

This section provides detailed migration examples for common programming languages and frameworks.

## Available examples

[GoLearn how to migrate Go applications to Docker Hardened Images with practical examples and best practices.](https://docs.docker.com/dhi/migration/examples/go/)[PythonLearn how to migrate Python applications to Docker Hardened Images with practical examples and best practices.](https://docs.docker.com/dhi/migration/examples/python/)[Node.jsLearn how to migrate Node.js applications to Docker Hardened Images with practical examples and best practices.](https://docs.docker.com/dhi/migration/examples/node/)

In addition to this documentation, each Docker Hardened Image repository in
the [Docker Hardened Images
catalog](https://hub.docker.com/hardened-images/catalog) includes image-specific
guidance and best practices for migrating applications built with that language
or framework.

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

# Migrate from Ubuntu

> Step-by-step guide to migrate from Ubuntu-based images to Docker Hardened Images

# Migrate from Ubuntu

   Table of contents

---

Docker Hardened Images (DHI) come in [Alpine-based and Debian-based
variants](https://docs.docker.com/dhi/explore/available/). When migrating from an Ubuntu-based image,
you should migrate to the Debian-based DHI variant, as both Ubuntu and Debian
share the same package management system (APT) and underlying architecture,
making migration straightforward.

This guide helps you migrate from an existing Ubuntu-based image to DHI.

## Key differences

When migrating from Ubuntu-based images to DHI Debian, be aware of these key differences:

| Item | Ubuntu-based images | Docker Hardened Images |
| --- | --- | --- |
| Package management | Varies by image. Some include APT package manager, others don't | Package managers generally only available in images with adevtag. Runtime images don't contain package managers. Use multi-stage builds and copy necessary artifacts from the build stage to the runtime stage. |
| Non-root user | Varies by image. Some run as root, others as non-root | Runtime variants run as the non-root user by default. Ensure that necessary files and directories are accessible to the non-root user. |
| Multi-stage build | Recommended | Recommended. Use images with adevorsdktags for build stages and non-dev images for runtime. |
| Ports | Can bind to privileged ports (under 1024) when running as root | Run as a non-root user by default. Applications can't bind to privileged ports (under 1024) when running in Kubernetes or in Docker Engine versions older than 20.10. Configure your application to listen on port 1025 and up inside the container. |
| Entry point | Varies by image | May have different entry points than Ubuntu-based images. Inspect entry points and update your Dockerfile if necessary. |
| Shell | Varies by image. Some include a shell, others don't | Runtime images don't contain a shell. Usedevimages in build stages to run shell commands and then copy artifacts to the runtime stage. |
| Package repositories | Uses Ubuntu package repositories | Uses Debian package repositories. Most packages have similar names, but some may differ. |

## Migration steps

### Step 1: Update the base image in your Dockerfile

Update the base image in your application's Dockerfile to a hardened image. This
is typically going to be an image tagged as `dev` or `sdk` because it has the tools
needed to install packages and dependencies.

The following example diff snippet from a Dockerfile shows the old Ubuntu-based image
replaced by the new DHI Debian image.

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
- ## Original Ubuntu-based image
- FROM ubuntu/go:1.22-24.04

+ ## Updated to use hardened Debian-based image
+ FROM dhi.io/golang:1-debian13-dev
```

To find the right tag, explore the available tags in the [DHI
Catalog](https://hub.docker.com/hardened-images/catalog/).

### Step 2: Update package installation commands

Since Ubuntu and Debian both use APT for package management, most package
installation commands remain similar. However, you need to ensure that package
installations only occur in `dev` or `sdk` images, as runtime images don't
contain package managers.

```diff
- ## Ubuntu: Installing packages
- FROM ubuntu/go:1.22-24.04
- RUN apt-get update && apt-get install -y \
-     git \
-     && rm -rf /var/lib/apt/lists/*

+ ## DHI: Use a language-specific dev image with package manager
+ FROM dhi.io/golang:1-debian13-dev
+ RUN apt-get update && apt-get install -y \
+     git \
+     && rm -rf /var/lib/apt/lists/*
```

Most Ubuntu packages are available in Debian with the same names. If you
encounter missing packages, you can search for equivalent packages using the
[Debian package search](https://packages.debian.org/) website.

### Step 3: Update the runtime image in your Dockerfile

> Note
>
> Multi-stage builds are recommended to keep your final image minimal and
> secure. Single-stage builds are supported, but they include the full `dev` image
> and therefore result in a larger image with a broader attack surface.

To ensure that your final image is as minimal as possible, you should use a
[multi-stage build](https://docs.docker.com/build/building/multi-stage/). All stages in your
Dockerfile should use a hardened image. While intermediary stages will typically
use images tagged as `dev` or `sdk`, your final runtime stage should use a runtime image.

Utilize the build stage to install dependencies and prepare your application,
then copy the resulting artifacts to the final runtime stage. This ensures that
your final image is minimal and secure.

The following example shows a multi-stage Dockerfile migrating from Ubuntu to DHI Debian:

```dockerfile
# Build stage
FROM dhi.io/golang:1-debian13-dev AS builder
WORKDIR /app

# Install system dependencies (only available in dev images)
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy application files
COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -a -ldflags="-s -w" -o main .

# Runtime stage
FROM dhi.io/golang:1-debian13
WORKDIR /app

# Copy compiled binary from builder
COPY --from=builder /app/main /app/main

# Run the application
ENTRYPOINT ["/app/main"]
```

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

# Migrate using Docker's AI

> Use Docker's AI-powered assistant to automatically migrate your Dockerfile to Docker Hardened Images

# Migrate using Docker's AI-powered assistant

---

Availability: Experimental
Requires: Docker Desktop
[4.38.0](https://docs.docker.com/desktop/release-notes/#4380) or later

You can use Docker's AI-powered assistant to automatically migrate your
Dockerfile to use Docker Hardened Images (DHI).

1. Ensure Docker's AI-powered assistant is
  [enabled](https://docs.docker.com/ai/gordon/#enable-ask-gordon).
2. In the terminal, navigate to the directory containing your Dockerfile.
3. Start a conversation with the assistant:
  ```bash
  docker ai
  ```
4. Type:
  ```console
  "Migrate my dockerfile to DHI"
  ```
5. Follow the conversation with the assistant. The assistant will edit your Dockerfile, so when
  it requests access to the filesystem and more, type `yes` to allow the assistant to proceed.

When the migration is complete, you see a success message:

```text
The migration to Docker Hardened Images (DHI) is complete. The updated Dockerfile
successfully builds the image, and no vulnerabilities were detected in the final image.
The functionality and optimizations of the original Dockerfile have been preserved.
```

> Important
>
> As with any AI tool, you must verify the assistant's edits and test your image.

---

# Migration

> Learn how to migrate your existing applications to Docker Hardened Images

# Migration

   Table of contents

---

This section provides guidance for migrating your applications to Docker
Hardened Images (DHI). Migrating to DHI enhances the security posture of your
containerized applications by leveraging hardened base images with built-in
security features.

## Migration paths

Choose the migration approach that best fits your needs:

[Migrate with Docker's AI assistantUse Docker's AI assistant to automatically migrate your Dockerfile to Docker Hardened Images with guidance and recommendations.](https://docs.docker.com/dhi/migration/migrate-with-ai/)[Migrate from Alpine or Debian imagesManual migration guide for moving from Docker Official Images (Alpine or Debian-based) to Docker Hardened Images.](https://docs.docker.com/dhi/migration/migrate-from-doi/)[Migrate from UbuntuManual migration guide for transitioning from Ubuntu-based images to Docker Hardened Images.](https://docs.docker.com/dhi/migration/migrate-from-ubuntu/)[Migrate from WolfiManual migration guide for transitioning from Wolfi-based images to Docker Hardened Images.](https://docs.docker.com/dhi/migration/migrate-from-wolfi/)

## Resources

[Migration checklistA comprehensive checklist of migration considerations to ensure successful transition to Docker Hardened Images.](https://docs.docker.com/dhi/migration/checklist/)[ExamplesExample Dockerfile migrations for different programming languages and frameworks to guide your migration process.](https://docs.docker.com/dhi/migration/examples/)

---

# Docker Hardened Images resources

> Additional resources including product information, blog posts, and GitHub repositories for Docker Hardened Images

# Docker Hardened Images resources

   Table of contents

---

This page provides links to additional resources related to Docker Hardened
Images (DHI), including blog posts, Docker Hub resources, and GitHub
repositories.

For product information and feature comparison, visit the [Docker Hardened
Images product page](https://www.docker.com/products/hardened-images/).

## Blog posts

The following blog posts provide insights into Docker Hardened Images, security
features, and announcements:

| Date published | Title |
| --- | --- |
| January 25, 2026 | Making the Most of Your Docker Hardened Images Enterprise Trial - Part 3 |
| January 24, 2026 | Making the Most of Your Docker Hardened Images Enterprise Trial - Part 2 |
| December 19, 2025 | Docker Hardened Images: Security Independently Validated by SRLabs |
| December 17, 2025 | A Safer Container Ecosystem with Docker: Free Docker Hardened Images |
| November 14, 2025 | Making the Most of Your Docker Hardened Images Enterprise Trial - Part 1 |
| October 15, 2025 | Docker Hardened Images: Crafted by Humans, Protected by AI |
| September 29, 2025 | Expanding Docker Hardened Images: Secure Helm Charts for Deployments |
| August 6, 2025 | The Next Evolution of Docker Hardened Images: Customizable, FedRAMP Ready, AI Migration Agent, and Deeper Integrations |
| August 6, 2025 | Accelerating FedRAMP Compliance with Docker Hardened Images |
| May 19, 2025 | Introducing Docker Hardened Images: Secure, Minimal, and Ready for Production |

## Docker Hub

Docker Hardened Images are available on Docker Hub:

- [Docker Hardened Images Catalog](https://dhi.io): Browse and pull Docker
  Hardened Images from the official catalog
- [Docker Hub MCP Server](https://hub.docker.com/mcp/server/dockerhub/overview):
  MCP server to list Docker Hardened Images (DHIs) available in your
  organizations

## GitHub repositories and resources

Docker Hardened Images repositories are available in the
[docker-hardened-images](https://github.com/docker-hardened-images) GitHub
organization:

- [Catalog](https://github.com/docker-hardened-images/catalog): DHI definition
  files and catalog metadata
- [Advisories](https://github.com/docker-hardened-images/advisories): CVE
  advisories for OSS packages distributed with DHIs
- [Keyring](https://github.com/docker-hardened-images/keyring): Public signing
  keys and verification tools
- [Log](https://github.com/docker-hardened-images/log): Log of references (tag >
  digest) for Docker Hardened Images
- [Discussions](https://github.com/orgs/docker-hardened-images/discussions):
  Community forum and product discussions

## Additional resources

- [Start a free trial](https://hub.docker.com/hardened-images/start-free-trial):
  Explore DHI Enterprise features including FIPS/STIG variants, customization,
  and SLA-backed support
- [Request a demo](https://www.docker.com/products/hardened-images/#getstarted): Get a
  personalized demo and information about DHI Enterprise subscriptions
- [Request an image](https://github.com/docker-hardened-images/catalog/issues):
  Submit a request for a specific Docker Hardened Image
- [Contact Sales](https://www.docker.com/pricing/contact-sales/): Connect with
  Docker sales team for enterprise inquiries
- [Docker Support](https://www.docker.com/support/): Access support resources
  for DHI Enterprise customers

---

# Troubleshoot

> Resolve common issues when building, running, or debugging Docker Hardened Images, such as non-root behavior, missing shells, and port access.

# Troubleshoot

   Table of contents

---

The following are common issues you may encounter while migrating to or using
Docker Hardened Images (DHIs), along with recommended solutions.

## General debugging

Docker Hardened Images are optimized for security and runtime performance. As
such, they typically don't include a shell or standard debugging tools. The
recommended way to troubleshoot containers built on DHIs is by using [Docker
Debug](https://docs.docker.com/dhi/how-to/debug/).

Docker Debug allows you to:

- Attach a temporary debug container to your existing container.
- Use a shell and familiar tools such as `curl`, `ps`, `netstat`, and `strace`.
- Install additional tools as needed in a writable, ephemeral layer that
  disappears after the session.

## Permissions

DHIs run as a nonroot user by default for enhanced security. This can result in
permission issues when accessing files or directories. Ensure your application
files and runtime directories are owned by the expected UID/GID or have
appropriate permissions.

To find out which user a DHI runs as, check the repository page for the image on
Docker Hub. See [View image variant
details](https://docs.docker.com/dhi/how-to/explore/#view-image-variant-details) for more information.

## Privileged ports

Nonroot containers cannot bind to ports below 1024 by default. This is enforced
by both the container runtime and the kernel (especially in Kubernetes and
Docker Engine < 20.10).

Inside the container, configure your application to listen on an unprivileged
port (1025 or higher). For example `docker run -p 80:8080 my-image` maps
port 8080 in the container to port 80 on the host, allowing you to access it
without needing root privileges.

## No shell

Runtime DHIs omit interactive shells like `sh` or `bash`. If your build or
tooling assumes a shell is present (e.g., for `RUN` instructions), use a `dev`
variant of the image in an earlier build stage and copy the final artifact into
the runtime image.

To find out which shell, if any, a DHI has, check the repository page for the
image on Docker Hub. See [View image variant
details](https://docs.docker.com/dhi/how-to/explore/#view-image-variant-details) for more information.

Also, use [Docker Debug](https://docs.docker.com/dhi/how-to/debug/) when you need shell
access to a running container.

## Entry point differences

DHIs may define different entry points compared to Docker Official Images (DOIs)
or other community images.

To find out the ENTRYPOINT or CMD for a DHI, check the repository page for the
image on Docker Hub. See [View image variant
details](https://docs.docker.com/dhi/how-to/explore/#view-image-variant-details) for more information.

## No package manager

Runtime Docker Hardened Images are stripped down for security and minimal attack
surface. As a result, they don't include a package manager such as `apk` or
`apt`. This means you can't install additional software directly in the runtime
image.

If your build or application setup requires installing packages (for example, to
compile code, install runtime dependencies, or add diagnostic tools), use a `dev`
variant of the image in a build stage. Then, copy only the necessary artifacts
into the final runtime image.
