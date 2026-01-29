# Builder settings and more

# Builder settings

> Set your builder settings relating to private registries, disk allocation .

# Builder settings

   Table of contents

---

The **Builder settings** page in Docker Build Cloud lets you configure disk allocation, private resource access, and firewall settings for your cloud builders in your organization. These configurations help optimize storage, enable access to private registries, and secure outbound network traffic.

## Storage and cache management

### Disk allocation

The **Disk allocation** setting lets you control how much of the available
storage is dedicated to the build cache. A lower allocation increases
storage available for active builds.

To make disk allocation changes, navigate to **Builder settings** in Docker
Build Cloud and then adjust the **Disk allocation** slider to specify the
percentage of storage used for build caching.

Any changes take effect immediately.

### Build cache space

Your subscription includes the following Build cache space:

| Subscription | Build cache space |
| --- | --- |
| Personal | N/A |
| Pro | 50GB |
| Team | 100GB |
| Business | 200GB |

### Multi-architecture storage allocation

Docker Build Cloud automatically provisions builders for both amd64 and arm64 architectures. Your total build cache space is split equally between these
two builders:

- Pro (50GB total): 25GB for amd64 builder + 25GB for arm64 builder
- Team (100GB total): 50GB for amd64 builder + 50GB for arm64 builder
- Business (200GB total): 100GB for amd64 builder + 100GB for arm64 builder

> Important
>
> If you only build for one architecture, be aware that your effective cache
> space is half of your subscription's total allocation.

### Get more build cache space

To get more Build cache space,
[upgrade your subscription](https://docs.docker.com/subscription/scale/).

> Tip
>
> If you build large images, consider allocating less storage for caching to
> leave more space for active builds.

## Private resource access

Private resource access lets cloud builders pull images and packages from private resources. This feature is useful when builds rely on self-hosted artifact repositories or private OCI registries.

For example, if your organization hosts a private [PyPI](https://pypi.org/) repository on a private network, Docker Build Cloud would not be able to access it by default, since the cloud builder is not connected to your private network.

To enable your cloud builders to access your private resources, enter the host name and port of your private resource and then select **Add**.

### Authentication

If your internal artifacts require authentication, make sure that you
authenticate with the repository either before or during the build. For
internal package repositories for npm or PyPI, use
[build secrets](https://docs.docker.com/build/building/secrets/)
to authenticate during the build. For internal OCI registries, use `docker login` to authenticate before building.

Note that if you use a private registry that requires authentication, you will
need to authenticate with `docker login` twice before building. This is because
the cloud builder needs to authenticate with Docker to use the cloud builder,
and then again to authenticate with the private registry.

```console
$ echo $DOCKER_PAT | docker login docker.io -u <username> --password-stdin
$ echo $REGISTRY_PASSWORD | docker login registry.example.com -u <username> --password-stdin
$ docker build --builder <cloud-builder> --tag registry.example.com/<image> --push .
```

## Firewall

Firewall settings let you restrict cloud builder egress traffic to specific IP addresses. This helps enhance security by limiting external network egress from the builder.

1. Select the **Enable firewall: Restrict cloud builder egress to specific public IP address** checkbox.
2. Enter the IP address you want to allow.
3. Select **Add** to apply the restriction.

---

# Use Docker Build Cloud in CI

> Speed up your continuous integration pipelines with Docker Build Cloud in CI

# Use Docker Build Cloud in CI

   Table of contents

---

Using Docker Build Cloud in CI can speed up your build pipelines, which means less time
spent waiting and context switching. You control your CI workflows as usual,
and delegate the build execution to Docker Build Cloud.

Building with Docker Build Cloud in CI involves the following steps:

1. Sign in to a Docker account.
2. Set up Buildx and connect to the builder.
3. Run the build.

When using Docker Build Cloud in CI, it's recommended that you push the result to a
registry directly, rather than loading the image and then pushing it. Pushing
directly speeds up your builds and avoids unnecessary file transfers.

If you just want to build and discard the output, export the results to the
build cache or build without tagging the image. When you use Docker Build Cloud,
Buildx automatically loads the build result if you build a tagged image.
See [Loading build results](https://docs.docker.com/build-cloud/usage/#loading-build-results) for details.

> Note
>
> Builds on Docker Build Cloud have a timeout limit of 90 minutes. Builds that
> run for longer than 90 minutes are automatically cancelled.

## Setting up credentials for CI/CD

To enable your CI/CD system to build and push images using Docker Build Cloud, provide both an access token and a username. The type of token and the username you use depend on your account type and permissions.

- If you are an organization administrator or have permission to create
  [organization access tokens (OAT)](https://docs.docker.com/enterprise/security/access-tokens/), use an OAT and set `DOCKER_ACCOUNT` to your Docker Hub organization name.
- If you do not have permission to create OATs or are using a personal account, use a
  [personal access token (PAT)](https://docs.docker.com/security/access-tokens/) and set `DOCKER_ACCOUNT` to your Docker Hub username.

### Creating access tokens

#### For organization accounts

If you are an organization administrator:

- Create an
  [organization access token (OAT)](https://docs.docker.com/enterprise/security/access-tokens/). The token must have these permissions:
  1. **cloud-connect** scope
  2. **Read public repositories** permission
  3. **Repository access** with **Image push** permission for the target repository:
    - Expand the **Repository** drop-down.
    - Select **Add repository** and choose your target repository.
    - Set the **Image push** permission for the repository.

If you are not an organization administrator:

- Ask your organization administrator for an access token with the permissions listed above, or use a personal access token.

#### For personal accounts

- Create a
  [personal access token (PAT)](https://docs.docker.com/security/access-tokens/) with the following permissions:
  1. **Read & write** access.
    - Note: Building with Docker Build Cloud only requires read access, but you need write access to push images to a Docker Hub repository.

## CI platform examples

> Note
>
> In your CI/CD configuration, set the following variables/secrets:
>
>
>
> - `DOCKER_ACCESS_TOKEN` — your access token (PAT or OAT). Use a secret to store the token.
> - `DOCKER_ACCOUNT` — your Docker Hub organization name (for OAT) or username (for PAT)
> - `CLOUD_BUILDER_NAME` — the name of the cloud builder you created in the [Docker Build Cloud Dashboard](https://app.docker.com/build/)
>
>
>
> This ensures your builds authenticate correctly with Docker Build Cloud.

### GitHub Actions

```yaml
name: ci

on:
  push:
    branches:
      - "main"

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKER_ACCOUNT }}
          password: ${{ secrets.DOCKER_ACCESS_TOKEN }}

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
        with:
          driver: cloud
          endpoint: "${{ vars.DOCKER_ACCOUNT }}/${{ vars.CLOUD_BUILDER_NAME }}" # for example, "acme/default"

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          tags: "IMAGE" # for example, "acme/my-image:latest"
          # For pull requests, export results to the build cache.
          # Otherwise, push to a registry.
          outputs: ${{ github.event_name == 'pull_request' && 'type=cacheonly' || 'type=registry' }}
```

The example above uses `docker/build-push-action`, which automatically uses the
builder set up by `setup-buildx-action`. If you need to use the `docker build`
command directly instead, you have two options:

- Use `docker buildx build` instead of `docker build`
- Set the `BUILDX_BUILDER` environment variable to use the cloud builder:
  ```yaml
  - name: Set up Docker Buildx
    id: builder
    uses: docker/setup-buildx-action@v3
    with:
      driver: cloud
      endpoint: "${{ vars.DOCKER_ACCOUNT }}/${{ vars.CLOUD_BUILDER_NAME }}"
  - name: Build
    run: |
      docker build .
    env:
      BUILDX_BUILDER: ${{ steps.builder.outputs.name }}
  ```

For more information about the `BUILDX_BUILDER` environment variable, see
[Build variables](https://docs.docker.com/build/building/variables/#buildx_builder).

### GitLab

```yaml
default:
  image: docker:24-dind
  services:
    - docker:24-dind
  before_script:
    - docker info
    - echo "$DOCKER_ACCESS_TOKEN" | docker login --username "$DOCKER_ACCOUNT" --password-stdin
    - |
      apk add curl jq
      ARCH=${CI_RUNNER_EXECUTABLE_ARCH#*/}
      BUILDX_URL=$(curl -s https://raw.githubusercontent.com/docker/actions-toolkit/main/.github/buildx-lab-releases.json | jq -r ".latest.assets[] | select(endswith(\"linux-$ARCH\"))")
      mkdir -vp ~/.docker/cli-plugins/
      curl --silent -L --output ~/.docker/cli-plugins/docker-buildx $BUILDX_URL
      chmod a+x ~/.docker/cli-plugins/docker-buildx
    - docker buildx create --use --driver cloud ${DOCKER_ACCOUNT}/${CLOUD_BUILDER_NAME}

variables:
  IMAGE_NAME: IMAGE
  DOCKER_ACCOUNT: DOCKER_ACCOUNT # your Docker Hub organization name (or username when using a personal account)
  CLOUD_BUILDER_NAME: CLOUD_BUILDER_NAME # the name of the cloud builder you created in the [Docker Build Cloud Dashboard](https://app.docker.com/build/)

# Build multi-platform image and push to a registry
build_push:
  stage: build
  script:
    - |
      docker buildx build \
        --platform linux/amd64,linux/arm64 \
        --tag "${IMAGE_NAME}:${CI_COMMIT_SHORT_SHA}" \
        --push .

# Build an image and discard the result
build_cache:
  stage: build
  script:
    - |
      docker buildx build \
        --platform linux/amd64,linux/arm64 \
        --tag "${IMAGE_NAME}:${CI_COMMIT_SHORT_SHA}" \
        --output type=cacheonly \
        .
```

### Circle CI

```yaml
version: 2.1

jobs:
  # Build multi-platform image and push to a registry
  build_push:
    machine:
      image: ubuntu-2204:current
    steps:
      - checkout

      - run: |
          mkdir -vp ~/.docker/cli-plugins/
          ARCH=amd64
          BUILDX_URL=$(curl -s https://raw.githubusercontent.com/docker/actions-toolkit/main/.github/buildx-lab-releases.json | jq -r ".latest.assets[] | select(endswith(\"linux-$ARCH\"))")
          curl --silent -L --output ~/.docker/cli-plugins/docker-buildx $BUILDX_URL
          chmod a+x ~/.docker/cli-plugins/docker-buildx

      - run: echo "$DOCKER_ACCESS_TOKEN" | docker login --username $DOCKER_ --password-stdin
      - run: docker buildx create --use --driver cloud "${DOCKER_ACCOUNT}/${CLOUD_BUILDER_NAME}"

      - run: |
          docker buildx build \
          --platform linux/amd64,linux/arm64 \
          --push \
          --tag "IMAGE" .

  # Build an image and discard the result
  build_cache:
    machine:
      image: ubuntu-2204:current
    steps:
      - checkout

      - run: |
          mkdir -vp ~/.docker/cli-plugins/
          ARCH=amd64
          BUILDX_URL=$(curl -s https://raw.githubusercontent.com/docker/actions-toolkit/main/.github/buildx-lab-releases.json | jq -r ".latest.assets[] | select(endswith(\"linux-$ARCH\"))")
          curl --silent -L --output ~/.docker/cli-plugins/docker-buildx $BUILDX_URL
          chmod a+x ~/.docker/cli-plugins/docker-buildx

      - run: echo "$DOCKER_ACCESS_TOKEN" | docker login --username $DOCKER_ --password-stdin
      - run: docker buildx create --use --driver cloud "${DOCKER_ACCOUNT}/${CLOUD_BUILDER_NAME}"

      - run: |
          docker buildx build \
          --tag temp \
          --output type=cacheonly \
          .

workflows:
  pull_request:
    jobs:
      - build_cache
  release:
    jobs:
      - build_push
```

### Buildkite

The following example sets up a Buildkite pipeline using Docker Build Cloud. The
example assumes that the pipeline name is `build-push-docker` and that you
manage the Docker access token using environment hooks, but feel free to adapt
this to your needs.

Add the following `environment` hook agent's hook directory:

```bash
#!/bin/bash
set -euo pipefail

if [[ "$BUILDKITE_PIPELINE_NAME" == "build-push-docker" ]]; then
 export DOCKER_ACCESS_TOKEN="DOCKER_ACCESS_TOKEN"
fi
```

Create a `pipeline.yml` that uses the `docker-login` plugin:

```yaml
env:
  DOCKER_ACCOUNT: DOCKER_ACCOUNT # your Docker Hub organization name (or username when using a personal account)
  CLOUD_BUILDER_NAME: CLOUD_BUILDER_NAME # the name of the cloud builder you created in the [Docker Build Cloud Dashboard](https://app.docker.com/build/)
  IMAGE_NAME: IMAGE

steps:
  - command: ./build.sh
    key: build-push
    plugins:
      - docker-login#v2.1.0:
          username: DOCKER_ACCOUNT
          password-env: DOCKER_ACCESS_TOKEN # the variable name in the environment hook
```

Create the `build.sh` script:

```bash
DOCKER_DIR=/usr/libexec/docker

# Get download link for latest buildx binary.
# Set $ARCH to the CPU architecture (e.g. amd64, arm64)
UNAME_ARCH=`uname -m`
case $UNAME_ARCH in
  aarch64)
    ARCH="arm64";
    ;;
  amd64)
    ARCH="amd64";
    ;;
  *)
    ARCH="amd64";
    ;;
esac
BUILDX_URL=$(curl -s https://raw.githubusercontent.com/docker/actions-toolkit/main/.github/buildx-lab-releases.json | jq -r ".latest.assets[] | select(endswith(\"linux-$ARCH\"))")

# Download docker buildx with Build Cloud support
curl --silent -L --output $DOCKER_DIR/cli-plugins/docker-buildx $BUILDX_URL
chmod a+x ~/.docker/cli-plugins/docker-buildx

# Connect to your builder and set it as the default builder
docker buildx create --use --driver cloud "${DOCKER_ACCOUNT}/${CLOUD_BUILDER_NAME}"

# Cache-only image build
docker buildx build \
    --platform linux/amd64,linux/arm64 \
    --tag "$IMAGE_NAME:$BUILDKITE_COMMIT" \
    --output type=cacheonly \
    .

# Build, tag, and push a multi-arch docker image
docker buildx build \
    --platform linux/amd64,linux/arm64 \
    --push \
    --tag "$IMAGE_NAME:$BUILDKITE_COMMIT" \
    .
```

### Jenkins

```groovy
pipeline {
  agent any

  environment {
    ARCH = 'amd64'
    DOCKER_ACCESS_TOKEN = credentials('docker-access-token')
    DOCKER_ACCOUNT = credentials('docker-account')
    CLOUD_BUILDER_NAME = 'CLOUD_BUILDER_NAME'
    IMAGE_NAME = 'IMAGE'
  }

  stages {
    stage('Build') {
      environment {
        BUILDX_URL = sh (returnStdout: true, script: 'curl -s https://raw.githubusercontent.com/docker/actions-toolkit/main/.github/buildx-lab-releases.json | jq -r ".latest.assets[] | select(endswith(\\"linux-$ARCH\\"))"').trim()
      }
      steps {
        sh 'mkdir -vp ~/.docker/cli-plugins/'
        sh 'curl --silent -L --output ~/.docker/cli-plugins/docker-buildx $BUILDX_URL'
        sh 'chmod a+x ~/.docker/cli-plugins/docker-buildx'
        sh 'echo "$DOCKER_ACCESS_TOKEN" | docker login --username $DOCKER_ACCOUNT --password-stdin'
        sh 'docker buildx create --use --driver cloud "${DOCKER_ACCOUNT}/${CLOUD_BUILDER_NAME}"'
        // Cache-only build
        sh 'docker buildx build --platform linux/amd64,linux/arm64 --tag "$IMAGE_NAME" --output type=cacheonly .'
        // Build and push a multi-platform image
        sh 'docker buildx build --platform linux/amd64,linux/arm64 --push --tag "$IMAGE_NAME" .'
      }
    }
  }
}
```

### Travis CI

```yaml
language: minimal
dist: jammy

services:
  - docker

env:
  global:
    - IMAGE_NAME=IMAGE # for example, "acme/my-image:latest"

before_install: |
  echo "$DOCKER_ACCESS_TOKEN" | docker login --username "$DOCKER_ACCOUNT" --password-stdin

install: |
  set -e
  BUILDX_URL=$(curl -s https://raw.githubusercontent.com/docker/actions-toolkit/main/.github/buildx-lab-releases.json | jq -r ".latest.assets[] | select(endswith(\"linux-$TRAVIS_CPU_ARCH\"))")
  mkdir -vp ~/.docker/cli-plugins/
  curl --silent -L --output ~/.docker/cli-plugins/docker-buildx $BUILDX_URL
  chmod a+x ~/.docker/cli-plugins/docker-buildx
  docker buildx create --use --driver cloud "${DOCKER_ACCOUNT}/${CLOUD_BUILDER_NAME}"

script: |
  docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --push \
  --tag "$IMAGE_NAME" .
```

### BitBucket Pipelines

```yaml
# Prerequisites: $DOCKER_ACCOUNT, $CLOUD_BUILDER_NAME, $DOCKER_ACCESS_TOKEN setup as deployment variables
# This pipeline assumes $BITBUCKET_REPO_SLUG as the image name

image: atlassian/default-image:3

pipelines:
  default:
    - step:
        name: Build multi-platform image
        script:
          - mkdir -vp ~/.docker/cli-plugins/
          - ARCH=amd64
          - BUILDX_URL=$(curl -s https://raw.githubusercontent.com/docker/actions-toolkit/main/.github/buildx-lab-releases.json | jq -r ".latest.assets[] | select(endswith(\"linux-$ARCH\"))")
          - curl --silent -L --output ~/.docker/cli-plugins/docker-buildx $BUILDX_URL
          - chmod a+x ~/.docker/cli-plugins/docker-buildx
          - echo "$DOCKER_ACCESS_TOKEN" | docker login --username $DOCKER_ACCOUNT --password-stdin
          - docker buildx create --use --driver cloud "${DOCKER_ACCOUNT}/${CLOUD_BUILDER_NAME}"
          - IMAGE_NAME=$BITBUCKET_REPO_SLUG
          - docker buildx build
            --platform linux/amd64,linux/arm64
            --push
            --tag "$IMAGE_NAME" .
        services:
          - docker
```

### Shell script

```bash
#!/bin/bash

# Get download link for latest buildx binary. Set $ARCH to the CPU architecture (e.g. amd64, arm64)
ARCH=amd64
BUILDX_URL=$(curl -s https://raw.githubusercontent.com/docker/actions-toolkit/main/.github/buildx-lab-releases.json | jq -r ".latest.assets[] | select(endswith(\"linux-$ARCH\"))")

# Download docker buildx with Build Cloud support
mkdir -vp ~/.docker/cli-plugins/
curl --silent -L --output ~/.docker/cli-plugins/docker-buildx $BUILDX_URL
chmod a+x ~/.docker/cli-plugins/docker-buildx

# Login to Docker Hub with an access token. See https://docs.docker.com/build-cloud/ci/#creating-access-tokens
echo "$DOCKER_ACCESS_TOKEN" | docker login --username $DOCKER_ACCOUNT --password-stdin

# Connect to your builder and set it as the default builder
docker buildx create --use --driver cloud "${DOCKER_ACCOUNT}/${CLOUD_BUILDER_NAME}"

# Cache-only image build
docker buildx build \
    --tag temp \
    --output type=cacheonly \
    .

# Build, tag, and push a multi-arch docker image
docker buildx build \
    --platform linux/amd64,linux/arm64 \
    --push \
    --tag "IMAGE" \
    .
```

### Docker Compose

Use this implementation if you want to use `docker compose build` with
Docker Build Cloud in CI.

```bash
#!/bin/bash

# Get download link for latest buildx binary. Set $ARCH to the CPU architecture (e.g. amd64, arm64)
ARCH=amd64
BUILDX_URL=$(curl -s https://raw.githubusercontent.com/docker/actions-toolkit/main/.github/buildx-lab-releases.json | jq -r ".latest.assets[] | select(endswith(\"linux-$ARCH\"))")
COMPOSE_URL=$(curl -sL \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer GITHUB_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/docker/compose-desktop/releases \
  | jq "[ .[] | select(.prerelease==false and .draft==false) ] | .[0].assets.[] | select(.name | endswith(\"linux-${ARCH}\")) | .browser_download_url")

# Download docker buildx with Build Cloud support
mkdir -vp ~/.docker/cli-plugins/
curl --silent -L --output ~/.docker/cli-plugins/docker-buildx $BUILDX_URL
curl --silent -L --output ~/.docker/cli-plugins/docker-compose $COMPOSE_URL
chmod a+x ~/.docker/cli-plugins/docker-buildx
chmod a+x ~/.docker/cli-plugins/docker-compose

# Login to Docker Hub with an access token. See https://docs.docker.com/build-cloud/ci/#creating-access-tokens
echo "$DOCKER_ACCESS_TOKEN" | docker login --username $DOCKER_ACCOUNT --password-stdin

# Connect to your builder and set it as the default builder
docker buildx create --use --driver cloud "${DOCKER_ACCOUNT}/${CLOUD_BUILDER_NAME}"

# Build the image build
docker compose build
```

---

# Optimize for building in the cloud

> Building remotely is different from building locally. Here's how to optimize for remote builders.

# Optimize for building in the cloud

   Table of contents

---

Docker Build Cloud runs your builds remotely, and not on the machine where you
invoke the build. This means that file transfers between the client and builder
happen over the network.

Transferring files over the network has a higher latency and lower bandwidth
than local transfers. Docker Build Cloud has several features to mitigate this:

- It uses attached storage volumes for build cache, which makes reading and
  writing cache very fast.
- Loading build results back to the client only pulls the layers that were
  changed compared to previous builds.

Despite these optimizations, building remotely can still yield slow context
transfers and image loads, for large projects or if the network connection is
slow. Here are some ways that you can optimize your builds to make the transfer
more efficient:

- [Dockerignore files](#dockerignore-files)
- [Slim base images](#slim-base-images)
- [Multi-stage builds](#multi-stage-builds)
- [Fetch remote files in build](#fetch-remote-files-in-build)
- [Multi-threaded tools](#multi-threaded-tools)

For more information on how to optimize your builds, see
[Building best practices](https://docs.docker.com/build/building/best-practices/).

### Dockerignore files

Using a
[.dockerignorefile](https://docs.docker.com/build/concepts/context/#dockerignore-files),
you can be explicit about which local files you don’t want to include in the
build context. Files caught by the glob patterns you specify in your
ignore-file aren't transferred to the remote builder.

Some examples of things you might want to add to your `.dockerignore` file are:

- `.git` — skip sending the version control history in the build context. Note
  that this means you won’t be able to run Git commands in your build steps,
  such as `git rev-parse`.
- Directories containing build artifacts, such as binaries. Build artifacts
  created locally during development.
- Vendor directories for package managers, such as `node_modules`.

In general, the contents of your `.dockerignore` file should be similar to what
you have in your `.gitignore`.

### Slim base images

Selecting smaller images for your `FROM` instructions in your Dockerfile can
help reduce the size of the final image. The [Alpine image](https://hub.docker.com/_/alpine)
is a good example of a minimal Docker image that provides all of the OS
utilities you would expect from a Linux container.

There’s also the [specialscratchimage](https://hub.docker.com/_/scratch),
which contains nothing at all. Useful for creating images of statically linked
binaries, for example.

### Multi-stage builds

[Multi-stage builds](https://docs.docker.com/build/building/multi-stage/) can make your build run faster,
because stages can run in parallel. It can also make your end-result smaller.
Write your Dockerfile in such a way that the final runtime stage uses the
smallest possible base image, with only the resources that your program requires
to run.

It’s also possible to
[copy resources from other images or stages](https://docs.docker.com/build/building/multi-stage/#name-your-build-stages),
using the Dockerfile `COPY --from` instruction. This technique can reduce the
number of layers, and the size of those layers, in the final stage.

### Fetch remote files in build

When possible, you should fetch files from a remote location in the build,
rather than bundling the files into the build context. Downloading files on the
Docker Build Cloud server directly is better, because it will likely be faster
than transferring the files with the build context.

You can fetch remote files during the build using the
[DockerfileADDinstruction](https://docs.docker.com/reference/dockerfile/#add),
or in your `RUN` instructions with tools like `wget` and `rsync`.

### Multi-threaded tools

Some tools that you use in your build instructions may not utilize multiple
cores by default. One such example is `make` which uses a single thread by
default, unless you specify the `make --jobs=<n>` option. For build steps
involving such tools, try checking if you can optimize the execution with
parallelization.

---

# Docker Build Cloud release notes

> Learn about the latest features of Docker Build Cloud

# Docker Build Cloud release notes

   Table of contents

---

This page contains information about the new features, improvements, known
issues, and bug fixes in Docker Build Cloud releases.

## 2025-02-24

### New

Added a new **Build settings** page where you can configure disk allocation, private resource access, and firewall settings for your cloud builders in your organization. These configurations help optimize storage, enable access to private registries, and secure outbound network traffic.

---

# Docker Build Cloud setup

> How to get started with Docker Build Cloud

# Docker Build Cloud setup

   Table of contents

---

Before you can start using Docker Build Cloud, you must add the builder to your local
environment.

## Prerequisites

To get started with Docker Build Cloud, you need to:

- Download and install Docker Desktop version 4.26.0 or later.
- Create a cloud builder on the [Docker Build Cloud Dashboard](https://app.docker.com/build/).
  - When you create the builder, choose a name for it (for example, `default`). You will use this name as `BUILDER_NAME` in the CLI steps below.

### Use Docker Build Cloud without Docker Desktop

To use Docker Build Cloud without Docker Desktop, you must download and install
a version of Buildx with support for Docker Build Cloud (the `cloud` driver).
You can find compatible Buildx binaries on the releases page of
[this repository](https://github.com/docker/buildx-desktop).

If you plan on building with Docker Build Cloud using the `docker compose build` command, you also need a version of Docker Compose that supports Docker
Build Cloud. You can find compatible Docker Compose binaries on the releases
page of [this repository](https://github.com/docker/compose-desktop).

## Steps

You can add a cloud builder using the CLI, with the `docker buildx create`
command, or using the Docker Desktop settings GUI.

1. Sign in to your Docker account.
  ```console
  $ docker login
  ```
2. Add the cloud builder endpoint.
  ```console
  $ docker buildx create --driver cloud ORG/BUILDER_NAME
  ```
  Replace `<ORG>` with the Docker Hub namespace of your Docker organization (or your username if you are using a personal account), and `<BUILDER_NAME>` with the name you chose when creating the builder in the dashboard.
  This creates a local instance of the cloud builder named `cloud-ORG-BUILDER_NAME`.
  > Note
  >
  > If your organization is `acme` and you named your builder `default`, use:
  >
  >
  >
  > ```console
  > $ docker buildx create --driver cloud acme/default
  > ```

1. Sign in to your Docker account using the **Sign in** button in Docker Desktop.
2. Open the Docker Desktop settings and navigate to the **Builders** tab.
3. Under **Available builders**, select **Connect to builder**.

The builder has native support for the `linux/amd64` and `linux/arm64`
architectures. This gives you a high-performance build cluster for building
multi-platform images natively.

## Firewall configuration

To use Docker Build Cloud behind a firewall, ensure that your firewall allows
traffic to the following addresses:

- 3.211.38.21
- [https://auth.docker.io](https://auth.docker.io)
- [https://build-cloud.docker.com](https://build-cloud.docker.com)
- [https://hub.docker.com](https://hub.docker.com)

## What's next

- See [Building with Docker Build Cloud](https://docs.docker.com/build-cloud/usage/) for examples on how to use Docker Build Cloud.
- See [Use Docker Build Cloud in CI](https://docs.docker.com/build-cloud/ci/) for examples on how to use Docker Build Cloud with CI systems.

---

# Building with Docker Build Cloud

> Invoke your cloud builds with the Buildx CLI client

# Building with Docker Build Cloud

   Table of contents

---

To build using Docker Build Cloud, invoke a build command and specify the name of the
builder using the `--builder` flag.

```console
$ docker buildx build --builder cloud-ORG-BUILDER_NAME --tag IMAGE .
```

## Use by default

If you want to use Docker Build Cloud without having to specify the `--builder` flag
each time, you can set it as the default builder.

Run the following command:

```console
$ docker buildx use cloud-ORG-BUILDER_NAME --global
```

1. Open the Docker Desktop settings and navigate to the **Builders** tab.
2. Find the cloud builder under **Available builders**.
3. Open the drop-down menu and select **Use**.
  ![Selecting the cloud builder as default using the Docker Desktop GUI](https://docs.docker.com/build/images/set-default-builder-gui.webp)  ![Selecting the cloud builder as default using the Docker Desktop GUI](https://docs.docker.com/build/images/set-default-builder-gui.webp)

Changing your default builder with `docker buildx use` only changes the default
builder for the `docker buildx build` command. The `docker build` command still
uses the `default` builder, unless you specify the `--builder` flag explicitly.

If you use build scripts, such as `make`, that use the `docker build` command,
we recommend updating your build commands to `docker buildx build`. Alternatively,
you can set the
[BUILDX_BUILDERenvironment
variable](https://docs.docker.com/build/building/variables/#buildx_builder) to specify which
builder `docker build` should use.

## Use with Docker Compose

To build with Docker Build Cloud using `docker compose build`, first set the
cloud builder as your selected builder, then run your build.

> Note
>
> Make sure you're using a supported version of Docker Compose, see
> [Prerequisites](https://docs.docker.com/build-cloud/setup/#prerequisites).

```console
$ docker buildx use cloud-ORG-BUILDER_NAME
$ docker compose build
```

In addition to `docker buildx use`, you can also use the `docker compose build --builder` flag or the
[BUILDX_BUILDERenvironment
variable](https://docs.docker.com/build/building/variables/#buildx_builder) to select the cloud builder.

## Loading build results

Building with `--tag` loads the build result to the local image store
automatically when the build finishes. To build without a tag and load the
result, you must pass the `--load` flag.

Loading the build result for multi-platform images is not supported. Use the
`docker buildx build --push` flag when building multi-platform images to push
the output to a registry.

```console
$ docker buildx build --builder cloud-ORG-BUILDER_NAME \
  --platform linux/amd64,linux/arm64 \
  --tag IMAGE \
  --push .
```

If you want to build with a tag, but you don't want to load the results to your
local image store, you can export the build results to the build cache only:

```console
$ docker buildx build --builder cloud-ORG-BUILDER_NAME \
  --platform linux/amd64,linux/arm64 \
  --tag IMAGE \
  --output type=cacheonly .
```

## Multi-platform builds

To run multi-platform builds, you must specify all of the platforms that you
want to build for using the `--platform` flag.

```console
$ docker buildx build --builder cloud-ORG-BUILDER_NAME \
  --platform linux/amd64,linux/arm64 \
  --tag IMAGE \
  --push .
```

If you don't specify the platform, the cloud builder automatically builds for the
architecture matching your local environment.

To learn more about building for multiple platforms, refer to
[Multi-platform
builds](https://docs.docker.com/build/building/multi-platform/).

## Cloud builds in Docker Desktop

The Docker Desktop
[Builds view](https://docs.docker.com/desktop/use-desktop/builds/) works with
Docker Build Cloud out of the box. This view can show information about not only your
own builds, but also builds initiated by your team members using the same
builder.

Teams using a shared builder get access to information such as:

- Ongoing and completed builds
- Build configuration, statistics, dependencies, and results
- Build source (Dockerfile)
- Build logs and errors

This lets you and your team work collaboratively on troubleshooting and
improving build speeds, without having to send build logs and benchmarks back
and forth between each other.

## Use secrets with Docker Build Cloud

To use build secrets with Docker Build Cloud,
such as authentication credentials or tokens,
use the `--secret` and `--ssh` CLI flags for the `docker buildx` command.
The traffic is encrypted and secrets are never stored in the build cache.

> Warning
>
> If you're misusing build arguments to pass credentials, authentication
> tokens, or other secrets, you should refactor your build to pass the secrets using
> [secret mounts](https://docs.docker.com/reference/cli/docker/buildx/build/#secret) instead.
> Build arguments are stored in the cache and their values are exposed through attestations.
> Secret mounts don't leak outside of the build and are never included in attestations.

For more information, refer to:

- [docker buildx build --secret](https://docs.docker.com/reference/cli/docker/buildx/build/#secret)
- [docker buildx build --ssh](https://docs.docker.com/reference/cli/docker/buildx/build/#ssh)

## Managing build cache

You don't need to manage Docker Build Cloud cache manually.
The system manages it for you through
[garbage collection](https://docs.docker.com/build/cache/garbage-collection/).

Old cache is automatically removed if you hit your storage limit.
You can check your current cache state using the
[docker buildx ducommand](https://docs.docker.com/reference/cli/docker/buildx/du/).

To clear the builder's cache manually,
use the
[docker buildx prunecommand](https://docs.docker.com/reference/cli/docker/buildx/prune/).
This works like pruning the cache for any other builder.

> Warning
>
> Pruning a cloud builder's cache also removes the cache for other team members
> using the same builder.

## Unset Docker Build Cloud as the default builder

If you've set a cloud builder as the default builder
and want to revert to the default `docker` builder,
run the following command:

```console
$ docker context use default
```

This doesn't remove the builder from your system.
It only changes the builder that's automatically selected to run your builds.

## Registries on internal networks

It is possible to use Docker Build Cloud with a
[private registry](https://docs.docker.com/build-cloud/builder-settings/#private-resource-access)
or registry mirror on an internal network.
