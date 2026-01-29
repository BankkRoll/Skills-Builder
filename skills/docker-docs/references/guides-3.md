# Run Angular tests in a container and more

# Run Angular tests in a container

> Learn how to run your Angular tests in a container.

# Run Angular tests in a container

   Table of contents

---

## Prerequisites

Complete all the previous sections of this guide, starting with [Containerize Angular application](https://docs.docker.com/guides/angular/containerize/).

## Overview

Testing is a critical part of the development process. In this section, you'll learn how to:

- Run Jasmine unit tests using the Angular CLI inside a Docker container.
- Use Docker Compose to isolate your test environment.
- Ensure consistency between local and container-based testing.

The `docker-angular-sample` project comes pre-configured with Jasmine, so you can get started quickly without extra setup.

---

## Run tests during development

The `docker-angular-sample` application includes a sample test file at the following location:

```console
$ src/app/app.component.spec.ts
```

This test uses Jasmine to validate the AppComponent logic.

### Step 1: Update compose.yaml

Add a new service named `angular-test` to your `compose.yaml` file. This service allows you to run your test suite in an isolated, containerized environment.

| 1234567891011121314151617181920212223242526 | services:angular-dev:build:context:.dockerfile:Dockerfile.devports:-"5173:5173"develop:watch:-action:syncpath:.target:/appangular-prod:build:context:.dockerfile:Dockerfileimage:docker-angular-sampleports:-"8080:8080"angular-test:build:context:.dockerfile:Dockerfile.devcommand:["npm","run","test"] |
| --- | --- |

The angular-test service reuses the same `Dockerfile.dev` used for [development](https://docs.docker.com/guides/angular/develop/) and overrides the default command to run tests with `npm run test`. This setup ensures a consistent test environment that matches your local development configuration.

After completing the previous steps, your project directory should contain the following files:

```text
├── docker-angular-sample/
│ ├── Dockerfile
│ ├── Dockerfile.dev
│ ├── .dockerignore
│ ├── compose.yaml
│ ├── nginx.conf
│ └── README.Docker.md
```

### Step 2: Run the tests

To execute your test suite inside the container, run the following command from your project root:

```console
$ docker compose run --rm angular-test
```

This command will:

- Start the `angular-test` service defined in your `compose.yaml` file.
- Execute the `npm run test` script using the same environment as development.
- Automatically removes the container after tests complete, using the
  [docker compose run --rm](https://docs.docker.com/engine/reference/commandline/compose_run) command.

You should see output similar to the following:

```shell
Test Suites: 1 passed, 1 total
Tests:       3 passed, 3 total
Snapshots:   0 total
Time:        1.529 s
```

> Note
>
> For more information about Compose commands, see the
> [Compose CLI
> reference](https://docs.docker.com/reference/cli/docker/compose/).

---

## Summary

In this section, you learned how to run unit tests for your Angular application inside a Docker container using Jasmine and Docker Compose.

What you accomplished:

- Created a `angular-test` service in `compose.yaml` to isolate test execution.
- Reused the development `Dockerfile.dev` to ensure consistency between dev and test environments.
- Ran tests inside the container using `docker compose run --rm angular-test`.
- Ensured reliable, repeatable testing across environments without depending on your local machine setup.

---

## Related resources

Explore official references and best practices to sharpen your Docker testing workflow:

- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/) – Understand all Dockerfile instructions and syntax.
- [Best practices for writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/) – Write efficient, maintainable, and secure Dockerfiles.
- [Compose file reference](https://docs.docker.com/compose/compose-file/) – Learn the full syntax and options available for configuring services in `compose.yaml`.
- [docker compose runCLI reference](https://docs.docker.com/reference/cli/docker/compose/run/) – Run one-off commands in a service container.

---

## Next steps

Next, you’ll learn how to set up a CI/CD pipeline using GitHub Actions to automatically build and test your Angular application in a containerized environment. This ensures your code is validated on every push or pull request, maintaining consistency and reliability across your development workflow.

---

# Angular language

> Containerize and develop Angular apps using Docker

# Angular language-specific guide

Table of contents

---

The Angular language-specific guide shows you how to containerize an Angular application using Docker, following best practices for creating efficient, production-ready containers.

[Angular](https://angular.dev/) is a robust and widely adopted framework for building dynamic, enterprise-grade web applications. However, managing dependencies, environments, and deployments can become complex as applications scale. Docker streamlines these challenges by offering a consistent, isolated environment for development and production.

> **Acknowledgment**
>
>
>
> Docker extends its sincere gratitude to [Kristiyan Velkov](https://www.linkedin.com/in/kristiyan-velkov-763130b3/) for authoring this guide. As a Docker Captain and experienced Front-end engineer, his expertise in Docker, DevOps, and modern web development has made this resource essential for the community, helping developers navigate and optimize their Docker workflows.

---

## What will you learn?

In this guide, you will learn how to:

- Containerize and run an Angular application using Docker.
- Set up a local development environment for Angular inside a container.
- Run tests for your Angular application within a Docker container.
- Configure a CI/CD pipeline using GitHub Actions for your containerized app.
- Deploy the containerized Angular application to a local Kubernetes cluster for testing and debugging.

You'll start by containerizing an existing Angular application and work your way up to production-level deployments.

---

## Prerequisites

Before you begin, ensure you have a working knowledge of:

- Basic understanding of [TypeScript](https://www.typescriptlang.org/) and [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript).
- Familiarity with [Node.js](https://nodejs.org/en) and [npm](https://docs.npmjs.com/about-npm) for managing dependencies and running scripts.
- Familiarity with [Angular](https://angular.io/) fundamentals.
- Understanding of core Docker concepts such as images, containers, and Dockerfiles. If you're new to Docker, start with the
  [Docker basics](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/) guide.

Once you've completed the Angular getting started modules, you’ll be fully prepared to containerize your own Angular application using the detailed examples and best practices outlined in this guide.

## Modules

1. [Containerize](https://docs.docker.com/guides/angular/containerize/)
  Learn how to containerize an Angular application with Docker by creating an optimized, production-ready image using best practices for performance, security, and scalability.
2. [Develop your app](https://docs.docker.com/guides/angular/develop/)
  Learn how to develop your Angular application locally using containers.
3. [Run your tests](https://docs.docker.com/guides/angular/run-tests/)
  Learn how to run your Angular tests in a container.
4. [Automate your builds with GitHub Actions](https://docs.docker.com/guides/angular/configure-github-actions/)
  Learn how to configure CI/CD using GitHub Actions for your Angular application.
5. [Test your deployment](https://docs.docker.com/guides/angular/deploy/)
  Learn how to deploy locally to test and debug your Kubernetes deployment

---

# Introduction to Azure Pipelines with Docker

# Introduction to Azure Pipelines with Docker

   Table of contents

---

> This guide is a community contribution. Docker would like to thank [Kristiyan Velkov](https://www.linkedin.com/in/kristiyan-velkov-763130b3/) for his valuable contribution.

## Prerequisites

Before you begin, ensure you have the following requirements:

- A [Docker Hub account](https://hub.docker.com) with a generated access token.
- An active [Azure DevOps project](https://dev.azure.com/) with a connected [Git repository](https://learn.microsoft.com/en-us/azure/devops/repos/git/?view=azure-devops).
- A project that includes a valid [Dockerfile](https://docs.docker.com/engine/reference/builder/) at its root or appropriate build context.

## Overview

This guide walks you through building and pushing Docker images using [Azure Pipelines](https://azure.microsoft.com/en-us/products/devops/pipelines), enabling a streamlined and secure CI workflow for containerized applications. You’ll learn how to:

- Configure Docker authentication securely.
- Set up an automated pipeline to build and push images.

## Set up Azure DevOps to work with Docker Hub

### Step 1: Configure a Docker Hub service connection

To securely authenticate with Docker Hub using Azure Pipelines:

1. Navigate to **Project Settings > Service Connections** in your Azure DevOps project.
2. Select **New service connection > Docker Registry**.
3. Choose **Docker Hub** and provide your Docker Hub credentials or access token.
4. Give the service connection a recognizable name, such as `my-docker-registry`.
5. Grant access only to the specific pipeline(s) that require it for improved security and least privilege.

> Important
>
> Avoid selecting the option to grant access to all pipelines unless absolutely necessary. Always apply the principle of least privilege.

### Step 2: Create your pipeline

Add the following `azure-pipelines.yml` file to the root of your repository:

```yaml
# Trigger pipeline on commits to the main branch
trigger:
  - main

# Trigger pipeline on pull requests targeting the main branch
pr:
  - main

# Define variables for reuse across the pipeline
variables:
  imageName: 'docker.io/$(dockerUsername)/my-image'
  buildTag: '$(Build.BuildId)'
  latestTag: 'latest'

stages:
  - stage: BuildAndPush
    displayName: Build and Push Docker Image
    jobs:
      - job: DockerJob
        displayName: Build and Push
        pool:
          vmImage: ubuntu-latest
          demands:
            - docker
        steps:
          - checkout: self
            displayName: Checkout Code

          - task: Docker@2
            displayName: Docker Login
            inputs:
              command: login
              containerRegistry: 'my-docker-registry'  # Service connection name

          - task: Docker@2
            displayName: Build Docker Image
            inputs:
              command: build
              repository: $(imageName)
              tags: |
                $(buildTag)
                $(latestTag)
              dockerfile: './Dockerfile'
              arguments: |
                --sbom=true
                --attest type=provenance
                --cache-from $(imageName):latest
            env:
              DOCKER_BUILDKIT: 1

          - task: Docker@2
            displayName: Push Docker Image
            condition: eq(variables['Build.SourceBranch'], 'refs/heads/main')
            inputs:
              command: push
              repository: $(imageName)
              tags: |
                $(buildTag)
                $(latestTag)

          # Optional: logout for self-hosted agents
          - script: docker logout
            displayName: Docker Logout (Self-hosted only)
            condition: ne(variables['Agent.OS'], 'Windows_NT')
```

## What this pipeline does

This pipeline automates the Docker image build and deployment process for the main branch. It ensures a secure and efficient workflow with best practices like caching, tagging, and conditional cleanup. Here's what it does:

- Triggers on commits and pull requests targeting the `main` branch.
- Authenticates securely with Docker Hub using an Azure DevOps service connection.
- Builds and tags the Docker image using Docker BuildKit for caching.
- Pushes both buildId and latest tags to Docker Hub.
- Logs out from Docker if running on a self-hosted Linux agent.

## How the pipeline works

### Step 1: Define pipeline triggers

```yaml
trigger:
  - main

pr:
  - main
```

This pipeline is triggered automatically on:

- Commits pushed to the `main` branch
- Pull requests targeting `main` main branch

> Tip
>
> Learn more: [Define pipeline triggers in Azure Pipelines](https://learn.microsoft.com/en-us/azure/devops/pipelines/build/triggers?view=azure-devops)

### Step 2: Define common variables

```yaml
variables:
  imageName: 'docker.io/$(dockerUsername)/my-image'
  buildTag: '$(Build.BuildId)'
  latestTag: 'latest'
```

These variables ensure consistent naming, versioning, and reuse throughout the pipeline steps:

- `imageName`: your image path on Docker Hub
- `buildTag`: a unique tag for each pipeline run
- `latestTag`: a stable alias for your most recent image

> Important
>
> The variable `dockerUsername` is not set automatically.
> Set it securely in your Azure DevOps pipeline variables:
>
>
>
> 1. Go to **Pipelines > Edit > Variables**
> 2. Add `dockerUsername` with your Docker Hub username
>
>
>
> Learn more: [Define and use variables in Azure Pipelines](https://learn.microsoft.com/en-us/azure/devops/pipelines/process/variables?view=azure-devops&tabs=yaml%2Cbatch)

### Step 3: Define pipeline stages and jobs

```yaml
stages:
  - stage: BuildAndPush
    displayName: Build and Push Docker Image
```

This stage executes only if the source branch is `main`.

> Tip
>
> Learn more: [Stage conditions in Azure Pipelines](https://learn.microsoft.com/en-us/azure/devops/pipelines/process/stages?view=azure-devops&tabs=yaml)

### Step 4: Job configuration

```yaml
jobs:
  - job: DockerJob
  displayName: Build and Push
  pool:
    vmImage: ubuntu-latest
    demands:
      - docker
```

This job utilizes the latest Ubuntu VM image with Docker support, provided by Microsoft-hosted agents. It can be replaced with a custom pool for self-hosted agents if necessary.

> Tip
>
> Learn more: [Specify a pool in your pipeline](https://learn.microsoft.com/en-us/azure/devops/pipelines/agents/pools-queues?view=azure-devops&tabs=yaml%2Cbrowser)

#### Step 4.1: Checkout code

```yaml
steps:
  - checkout: self
    displayName: Checkout Code
```

This step pulls your repository code into the build agent, so the pipeline can access the Dockerfile and application files.

> Tip
>
> Learn more: [checkout step documentation](https://learn.microsoft.com/en-us/azure/devops/pipelines/yaml-schema/steps-checkout?view=azure-pipelines)

#### Step 4.2: Authenticate to Docker Hub

```yaml
- task: Docker@2
  displayName: Docker Login
  inputs:
    command: login
    containerRegistry: 'my-docker-registry'  # Replace with your service connection name
```

Uses a pre-configured Azure DevOps Docker registry service connection to authenticate securely without exposing credentials directly.

> Tip
>
> Learn more: [Use service connections for Docker Hub](https://learn.microsoft.com/en-us/azure/devops/pipelines/library/service-endpoints?view=azure-devops#docker-hub-or-others)

#### Step 4.3: Build the Docker image

```yaml
- task: Docker@2
    displayName: Build Docker Image
    inputs:
      command: build
      repository: $(imageName)
      tags: |
          $(buildTag)
          $(latestTag)
      dockerfile: './Dockerfile'
      arguments: |
          --sbom=true
          --attest type=provenance
          --cache-from $(imageName):latest
    env:
      DOCKER_BUILDKIT: 1
```

This builds the image with:

- Two tags: one with the unique Build ID and one as latest
- Docker BuildKit enabled for faster builds and efficient layer caching
- Cache pull from the most recent pushed latest image
- Software Bill of Materials (SBOM) for supply chain transparency
- Provenance attestation to verify how and where the image was built

> Tip
>
> Learn more:
>
>
>
> - [Docker task for Azure Pipelines](https://learn.microsoft.com/en-us/azure/devops/pipelines/tasks/reference/docker-v2?view=azure-pipelines&tabs=yaml)
> - [Docker SBOM Attestations](https://docs.docker.com/build/metadata/attestations/slsa-provenance/)

#### Step 4.4: Push the Docker image

```yaml
- task: Docker@2
  displayName: Push Docker Image
  condition: eq(variables['Build.SourceBranch'], 'refs/heads/main')
  inputs:
      command: push
      repository: $(imageName)
      tags: |
        $(buildTag)
        $(latestTag)
```

By applying this condition, the pipeline builds the Docker image on every run to ensure early detection of issues, but only pushes the image to the registry when changes are merged into the main branch—keeping your Docker Hub clean and focused

This uploads both tags to Docker Hub:

- `$(buildTag)` ensures traceability per run.
- `latest` is used for most recent image references.

#### Step 4.5 Logout of Docker (self-hosted agents)

```yaml
- script: docker logout
  displayName: Docker Logout (Self-hosted only)
  condition: ne(variables['Agent.OS'], 'Windows_NT')
```

Executes docker logout at the end of the pipeline on Linux-based self-hosted agents to proactively clean up credentials and enhance security posture.

## Summary

With this Azure Pipelines CI setup, you get:

- Secure Docker authentication using a built-in service connection.
- Automated image building and tagging triggered by code changes.
- Efficient builds leveraging Docker BuildKit cache.
- Safe cleanup with logout on persistent agents.
- Build images that meet modern software supply chain requirements with SBOM and attestation

## Learn more

- [Azure Pipelines Documentation](https://learn.microsoft.com/en-us/azure/devops/pipelines/?view=azure-devops): Comprehensive guide to configuring and managing CI/CD pipelines in Azure DevOps.
- [Docker Task for Azure Pipelines](https://learn.microsoft.com/en-us/azure/devops/pipelines/tasks/build/docker): Detailed reference for using the Docker task in Azure Pipelines to build and push images.
- [Docker Buildx Bake](https://docs.docker.com/build/bake/): Explore Docker's advanced build tool for complex, multi-stage, and multi-platform build setups. See also the
  [Mastering Buildx Bake Guide](https://docs.docker.com/guides/bake/) for practical examples and best practices.
- [Docker Build Cloud](https://docs.docker.com/guides/docker-build-cloud/): Learn about Docker's managed build service for faster, scalable, and multi-platform image builds in the cloud.

---

# Mastering multi

> Learn how to manage simple and complex build configurations with Buildx Bake.

# Mastering multi-platform builds, testing, and more with Docker Buildx Bake

   Table of contents

---

This guide demonstrates how to simplify and automate the process of building
images, testing, and generating build artifacts using Docker Buildx Bake. By
defining build configurations in a declarative `docker-bake.hcl` file, you can
eliminate manual scripts and enable efficient workflows for complex builds,
testing, and artifact generation.

## Assumptions

This guide assumes that you're familiar with:

- Docker
- [Buildx](https://docs.docker.com/build/concepts/overview/#buildx)
- [BuildKit](https://docs.docker.com/build/concepts/overview/#buildkit)
- [Multi-stage builds](https://docs.docker.com/build/building/multi-stage/)
- [Multi-platform builds](https://docs.docker.com/build/building/multi-platform/)

## Prerequisites

- You have a recent version of Docker installed on your machine.
- You have Git installed for cloning repositories.
- You're using the
  [containerd](https://docs.docker.com/desktop/features/containerd/) image store.

## Introduction

This guide uses an example project to demonstrate how Docker Buildx Bake can
streamline your build and test workflows. The repository includes both a
Dockerfile and a `docker-bake.hcl` file, giving you a ready-to-use setup to try
out Bake commands.

Start by cloning the example repository:

```bash
git clone https://github.com/dvdksn/bakeme.git
cd bakeme
```

The Bake file, `docker-bake.hcl`, defines the build targets in a declarative
syntax, using targets and groups, allowing you to manage complex builds
efficiently.

Here's what the Bake file looks like out-of-the-box:

```hcl
target "default" {
  target = "image"
  tags = [
    "bakeme:latest",
  ]
  attest = [
    "type=provenance,mode=max",
    "type=sbom",
  ]
  platforms = [
    "linux/amd64",
    "linux/arm64",
    "linux/riscv64",
  ]
}
```

The `target` keyword defines a build target for Bake. The `default` target
defines the target to build when no specific target is specified on the command
line. Here's a quick summary of the options for the `default` target:

- `target`: The target build stage in the Dockerfile.
- `tags`: Tags to assign to the image.
- `attest`:
  [Attestations](https://docs.docker.com/build/metadata/attestations/) to attach to the image.
  > Tip
  >
  > The attestations provide metadata such as build provenance, which tracks
  > the source of the image's build, and an SBOM (Software Bill of Materials),
  > useful for security audits and compliance.
- `platforms`: Platform variants to build.

To execute this build, simply run the following command in the root of the
repository:

```console
$ docker buildx bake
```

With Bake, you avoid long, hard-to-remember command-line incantations,
simplifying build configuration management by replacing manual, error-prone
scripts with a structured configuration file.

For contrast, here's what this build command would look like without Bake:

```console
$ docker buildx build \
  --target=image \
  --tag=bakeme:latest \
  --provenance=true \
  --sbom=true \
  --platform=linux/amd64,linux/arm64,linux/riscv64 \
  .
```

## Testing and linting

Bake isn't just for defining build configurations and running builds. You can
also use Bake to run your tests, effectively using BuildKit as a task runner.
Running your tests in containers is great for ensuring reproducible results.
This section shows how to add two types of tests:

- Unit testing with `go test`.
- Linting for style violations with `golangci-lint`.

In Test-Driven Development (TDD) fashion, start by adding a new `test` target
to the Bake file:

```hcl
target "test" {
  target = "test"
  output = ["type=cacheonly"]
}
```

> Tip
>
> Using `type=cacheonly` ensures that the build output is effectively
> discarded; the layers are saved to BuildKit's cache, but Buildx will not
> attempt to load the result to the Docker Engine's image store.
>
>
>
> For test runs, you don't need to export the build output — only the test
> execution matters.

To execute this Bake target, run `docker buildx bake test`. At this time,
you'll receive an error indicating that the `test` stage does not exist in the
Dockerfile.

```console
$ docker buildx bake test
[+] Building 1.2s (6/6) FINISHED
 => [internal] load local bake definitions
...
ERROR: failed to solve: target stage "test" could not be found
```

To satisfy this target, add the corresponding Dockerfile target. The `test`
stage here is based on the same base stage as the build stage.

```dockerfile
FROM base AS test
RUN --mount=target=. \
    --mount=type=cache,target=/go/pkg/mod \
    go test .
```

> Tip
>
> The
> [--mount=type=cachedirective](https://docs.docker.com/build/cache/optimize/#use-cache-mounts)
> caches Go modules between builds, improving build performance by avoiding the
> need to re-download dependencies. This shared cache ensures that the same
> dependency set is available across build, test, and other stages.

Now, running the `test` target with Bake will evaluate the unit tests for this
project. If you want to verify that it works, you can make an arbitrary change
to `main_test.go` to cause the test to fail.

Next, to enable linting, add another target to the Bake file, named `lint`:

```hcl
target "lint" {
  target = "lint"
  output = ["type=cacheonly"]
}
```

And in the Dockerfile, add the build stage. This stage will use the official
`golangci-lint` image on Docker Hub.

> Tip
>
> Because this stage relies on executing an external dependency, it's generally
> a good idea to define the version you want to use as a build argument. This
> lets you more easily manage version upgrades in the future by collocating
> dependency versions to the beginning of the Dockerfile.

```dockerfile
ARG GO_VERSION="1.23"
ARG GOLANGCI_LINT_VERSION="1.61"

#...

FROM golangci/golangci-lint:v${GOLANGCI_LINT_VERSION}-alpine AS lint
RUN --mount=target=.,rw \
    golangci-lint run
```

Lastly, to enable running both tests simultaneously, you can use the `groups`
construct in the Bake file. A group can specify multiple targets to run with a
single invocation.

```hcl
group "validate" {
  targets = ["test", "lint"]
}
```

Now, running both tests is as simple as:

```console
$ docker buildx bake validate
```

## Building variants

Sometimes you need to build more than one version of a program. The following
example uses Bake to build separate "release" and "debug" variants of the
program, using
[matrices](https://docs.docker.com/build/bake/matrices/). Using matrices lets
you run parallel builds with different configurations, saving time and ensuring
consistency.

A matrix expands a single build into multiple builds, each representing a
unique combination of matrix parameters. This means you can orchestrate Bake
into building both the production and development build of your program in
parallel, with minimal configuration changes.

The example project for this guide is set up to use a build-time option to
conditionally enable debug logging and tracing capabilities.

- If you compile the program with `go build -tags="debug"`, the additional
  logging and tracing capabilities are enabled (development mode).
- If you build without the `debug` tag, the program is compiled with a default
  logger (production mode).

Update the Bake file by adding a matrix attribute which defines the variable
combinations to build:

docker-bake.hcl

```diff
target "default" {
+  matrix = {
+    mode = ["release", "debug"]
+  }
+  name = "image-${mode}"
   target = "image"
```

The `matrix` attribute defines the variants to build ("release" and "debug").
The `name` attribute defines how the matrix gets expanded into multiple
distinct build targets. In this case, the matrix attribute expands the build
into two workflows: `image-release` and `image-debug`, each using different
configuration parameters.

Next, define a build argument named `BUILD_TAGS` which takes the value of the
matrix variable.

docker-bake.hcl

```diff
target = "image"
+  args = {
+    BUILD_TAGS = mode
+  }
   tags = [
```

You'll also want to change how the image tags are assigned to these builds.
Currently, both matrix paths would generate the same image tag names, and
overwrite each other. Update the `tags` attribute use a conditional operator to
set the tag depending on the matrix variable value.

docker-bake.hcl

```diff
tags = [
-    "bakeme:latest",
+    mode == "release" ? "bakeme:latest" : "bakeme:dev"
   ]
```

- If `mode` is `release`, the tag name is `bakeme:latest`
- If `mode` is `debug`, the tag name is `bakeme:dev`

Finally, update the Dockerfile to consume the `BUILD_TAGS` argument during the
compilation stage. When the `-tags="${BUILD_TAGS}"` option evaluates to
`-tags="debug"`, the compiler uses the `configureLogging` function in the
[debug.go](https://github.com/dvdksn/bakeme/blob/75c8a41e613829293c4bd3fc3b4f0c573f458f42/debug.go#L1)
file.

Dockerfile

```diff
# build compiles the program
 FROM base AS build
-ARG TARGETOS TARGETARCH
+ARG TARGETOS TARGETARCH BUILD_TAGS
 ENV GOOS=$TARGETOS
 ENV GOARCH=$TARGETARCH
 RUN --mount=target=. \
        --mount=type=cache,target=/go/pkg/mod \
-       go build -o "/usr/bin/bakeme" .
+       go build -tags="${BUILD_TAGS}" -o "/usr/bin/bakeme" .
```

That's all. With these changes, your `docker buildx bake` command now builds
two multi-platform image variants. You can introspect the canonical build
configuration that Bake generates using the `docker buildx bake --print`
command. Running this command shows that Bake will run a `default` group with
two targets with different build arguments and image tags.

```json
{
  "group": {
    "default": {
      "targets": ["image-release", "image-debug"]
    }
  },
  "target": {
    "image-debug": {
      "attest": ["type=provenance,mode=max", "type=sbom"],
      "context": ".",
      "dockerfile": "Dockerfile",
      "args": {
        "BUILD_TAGS": "debug"
      },
      "tags": ["bakeme:dev"],
      "target": "image",
      "platforms": ["linux/amd64", "linux/arm64", "linux/riscv64"]
    },
    "image-release": {
      "attest": ["type=provenance,mode=max", "type=sbom"],
      "context": ".",
      "dockerfile": "Dockerfile",
      "args": {
        "BUILD_TAGS": "release"
      },
      "tags": ["bakeme:latest"],
      "target": "image",
      "platforms": ["linux/amd64", "linux/arm64", "linux/riscv64"]
    }
  }
}
```

Factoring in all of the platform variants as well, this means that the build
configuration generates 6 different images.

```console
$ docker buildx bake
$ docker image ls --tree

IMAGE                   ID             DISK USAGE   CONTENT SIZE   USED
bakeme:dev              f7cb5c08beac       49.3MB         28.9MB
├─ linux/riscv64        0eae8ba0367a       9.18MB         9.18MB
├─ linux/arm64          56561051c49a         30MB         9.89MB
└─ linux/amd64          e8ca65079c1f        9.8MB          9.8MB

bakeme:latest           20065d2c4d22       44.4MB         25.9MB
├─ linux/riscv64        7cc82872695f       8.21MB         8.21MB
├─ linux/arm64          e42220c2b7a3       27.1MB         8.93MB
└─ linux/amd64          af5b2dd64fde       8.78MB         8.78MB
```

## Exporting build artifacts

Exporting build artifacts like binaries can be useful for deploying to
environments without Docker or Kubernetes. For example, if your programs are
meant to be run on a user's local machine.

> Tip
>
> The techniques discussed in this section can be applied not only to build
> output like binaries, but to any type of artifacts, such as test reports.

With programming languages like Go and Rust where the compiled binaries are
usually portable, creating alternate build targets for exporting only the
binary is trivial. All you need to do is add an empty stage in the Dockerfile
containing nothing but the binary that you want to export.

First, let's add a quick way to build a binary for your local platform and
export it to `./build/local` on the local filesystem.

In the `docker-bake.hcl` file, create a new `bin` target. In this stage, set
the `output` attribute to a local filesystem path. Buildx automatically detects
that the output looks like a filepath, and exports the results to the specified
path using the
[local exporter](https://docs.docker.com/build/exporters/local-tar/).

```hcl
target "bin" {
  target = "bin"
  output = ["build/bin"]
  platforms = ["local"]
}
```

Notice that this stage specifies a `local` platform. By default, if `platforms`
is unspecified, builds target the OS and architecture of the BuildKit host. If
you're using Docker Desktop, this often means builds target `linux/amd64` or
`linux/arm64`, even if your local machine is macOS or Windows, because Docker
runs in a Linux VM. Using the `local` platform forces the target platform to
match your local environment.

Next, add the `bin` stage to the Dockerfile which copies the compiled binary
from the build stage.

```dockerfile
FROM scratch AS bin
COPY --from=build "/usr/bin/bakeme" /
```

Now you can export your local platform version of the binary with `docker buildx bake bin`. For example, on macOS, this build target generates an
executable in the [Mach-O format](https://en.wikipedia.org/wiki/Mach-O) — the
standard executable format for macOS.

```console
$ docker buildx bake bin
$ file ./build/bin/bakeme
./build/bin/bakeme: Mach-O 64-bit executable arm64
```

Next, let's add a target to build all of the platform variants of the program.
To do this, you can
[inherit](https://docs.docker.com/build/bake/inheritance/) the `bin`
target that you just created, and extend it by adding the desired platforms.

```hcl
target "bin-cross" {
  inherits = ["bin"]
  platforms = [
    "linux/amd64",
    "linux/arm64",
    "linux/riscv64",
  ]
}
```

Now, building the `bin-cross` target creates binaries for all platforms.
Subdirectories are automatically created for each variant.

```console
$ docker buildx bake bin-cross
$ tree build/
build/
└── bin
    ├── bakeme
    ├── linux_amd64
    │   └── bakeme
    ├── linux_arm64
    │   └── bakeme
    └── linux_riscv64
        └── bakeme

5 directories, 4 files
```

To also generate "release" and "debug" variants, you can use a matrix just like
you did with the default target. When using a matrix, you also need to
differentiate the output directory based on the matrix value, otherwise the
binary gets written to the same location for each matrix run.

```hcl
target "bin-all" {
  inherits = ["bin-cross"]
  matrix = {
    mode = ["release", "debug"]
  }
  name = "bin-${mode}"
  args = {
    BUILD_TAGS = mode
  }
  output = ["build/bin/${mode}"]
}
```

```console
$ rm -r ./build/
$ docker buildx bake bin-all
$ tree build/
build/
└── bin
    ├── debug
    │   ├── linux_amd64
    │   │   └── bakeme
    │   ├── linux_arm64
    │   │   └── bakeme
    │   └── linux_riscv64
    │       └── bakeme
    └── release
        ├── linux_amd64
        │   └── bakeme
        ├── linux_arm64
        │   └── bakeme
        └── linux_riscv64
            └── bakeme

10 directories, 6 files
```

## Conclusion

Docker Buildx Bake streamlines complex build workflows, enabling efficient
multi-platform builds, testing, and artifact export. By integrating Buildx Bake
into your projects, you can simplify your Docker builds, make your build
configuration portable, and wrangle complex configurations more easily.

Experiment with different configurations and extend your Bake files to suit
your project's needs. You might consider integrating Bake into your CI/CD
pipelines to automate builds, testing, and artifact deployment. The flexibility
and power of Buildx Bake can significantly improve your development and
deployment processes.

### Further reading

For more information about how to use Bake, check out these resources:

- [Bake documentation](https://docs.docker.com/build/bake/)
- [Matrix targets](https://docs.docker.com/build/bake/matrices/)
- [Bake file reference](https://docs.docker.com/build/bake/reference/)
- [Bake GitHub Action](https://github.com/docker/bake-action)

---

# Configure CI/CD for your Bun application

> Learn how to configure CI/CD using GitHub Actions for your Bun application.

# Configure CI/CD for your Bun application

   Table of contents

---

## Prerequisites

Complete all the previous sections of this guide, starting with [Containerize a Bun application](https://docs.docker.com/guides/bun/containerize/). You must have a [GitHub](https://github.com/signup) account and a verified [Docker](https://hub.docker.com/signup) account to complete this section.

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
  [Personal Access Token (PAT)](https://docs.docker.com/security/access-tokens/#create-an-access-token)for Docker Hub. You can name this token `docker-tutorial`. Make sure access permissions include Read and Write.
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

In this section, you learned how to set up a GitHub Actions workflow for your Bun application.

Related information:

- [Introduction to GitHub Actions](https://docs.docker.com/guides/gha/)
- [Docker Build GitHub Actions](https://docs.docker.com/build/ci/github-actions/)
- [Workflow syntax for GitHub Actions](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

## Next steps

Next, learn how you can locally test and debug your workloads on Kubernetes before deploying.

---

# Containerize a Bun application

> Learn how to containerize a Bun application.

# Containerize a Bun application

   Table of contents

---

## Prerequisites

- You have a [Git client](https://git-scm.com/downloads). The examples in this section use a command-line based Git client, but you can use any client.

## Overview

For a long time, Node.js has been the de-facto runtime for server-side
JavaScript applications. Recent years have seen a rise in new alternative
runtimes in the ecosystem, including [Bun website](https://bun.sh/). Like
Node.js, Bun is a JavaScript runtime. Bun is a comparatively lightweight
runtime that is designed to be fast and efficient.

Why develop Bun applications with Docker? Having multiple runtimes to choose
from is great. But as the number of runtimes increases, it becomes challenging
to manage the different runtimes and their dependencies consistently across
environments. This is where Docker comes in. Creating and destroying containers
on demand is a great way to manage the different runtimes and their
dependencies. Also, as it's fairly a new runtime, getting a consistent
development environment for Bun can be challenging. Docker can help you set up
a consistent development environment for Bun.

## Get the sample application

Clone the sample application to use with this guide. Open a terminal, change
directory to a directory that you want to work in, and run the following
command to clone the repository:

```console
$ git clone https://github.com/dockersamples/bun-docker.git && cd bun-docker
```

You should now have the following contents in your `bun-docker` directory.

```text
├── bun-docker/
│ ├── compose.yml
│ ├── Dockerfile
│ ├── LICENSE
│ ├── server.js
│ └── README.md
```

## Create a Dockerfile

Before creating a Dockerfile, you need to choose a base image. You can either use the [Bun Docker Official Image](https://hub.docker.com/r/oven/bun) or a Docker Hardened Image (DHI) from the [Hardened Image catalog](https://hub.docker.com/hardened-images/catalog).

Choosing DHI offers the advantage of a production-ready image that is lightweight and secure. For more information, see [Docker Hardened Images](https://docs.docker.com/dhi/).

Docker Hardened Images (DHIs) are available for Bun in the [Docker Hardened Images catalog](https://hub.docker.com/hardened-images/catalog/dhi/bun). You can pull DHIs directly from the `dhi.io` registry.

1. Sign in to the DHI registry:
  ```console
  $ docker login dhi.io
  ```
2. Pull the Bun DHI as `dhi.io/bun:1`. The tag (`1`) in this example refers to the version to the latest 1.x version of Bun.
  ```console
  $ docker pull dhi.io/bun:1
  ```

For other available versions, refer to the [catalog](https://hub.docker.com/hardened-images/catalog/dhi/bun).

```dockerfile
# Use the DHI Bun image as the base image
FROM dhi.io/bun:1

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Expose the port on which the API will listen
EXPOSE 3000

# Run the server when the container launches
CMD ["bun", "server.js"]
```

Using the Docker Official Image is straightforward. In the following Dockerfile, you'll notice that the `FROM` instruction uses `oven/bun` as the base image.

You can find the image on [Docker Hub](https://hub.docker.com/r/oven/bun). This is the Docker Official Image for Bun created by Oven, the company behind Bun, and it's available on Docker Hub.

```dockerfile
# Use the official Bun image
FROM oven/bun:latest

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Expose the port on which the API will listen
EXPOSE 3000

# Run the server when the container launches
CMD ["bun", "server.js"]
```

In addition to specifying the base image, the Dockerfile also:

- Sets the working directory in the container to `/app`.
- Copies the content of the current directory to the `/app` directory in the container.
- Exposes port 3000, where the API is listening for requests.
- And finally, starts the server when the container launches with the command `bun server.js`.

## Run the application

Inside the `bun-docker` directory, run the following command in a terminal.

```console
$ docker compose up --build
```

Open a browser and view the application at [http://localhost:3000](http://localhost:3000). You will see a message `{"Status" : "OK"}` in the browser.

In the terminal, press `ctrl`+`c` to stop the application.

### Run the application in the background

You can run the application detached from the terminal by adding the `-d`
option. Inside the `bun-docker` directory, run the following command
in a terminal.

```console
$ docker compose up --build -d
```

Open a browser and view the application at [http://localhost:3000](http://localhost:3000).

In the terminal, run the following command to stop the application.

```console
$ docker compose down
```

## Summary

In this section, you learned how you can containerize and run your Bun
application using Docker.

Related information:

- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
- [.dockerignore file](https://docs.docker.com/reference/dockerfile/#dockerignore-file)
- [Docker Compose overview](https://docs.docker.com/compose/)
- [Compose file reference](https://docs.docker.com/reference/compose-file/)
- [Docker Hardened Images](https://docs.docker.com/dhi/)

## Next steps

In the next section, you'll learn how you can develop your application using
containers.
