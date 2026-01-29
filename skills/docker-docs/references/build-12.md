# Multi and more

# Multi

> Build for multiple architectures with GitHub Actions using QEMU emulation or multiple native builders

# Multi-platform image with GitHub Actions

   Table of contents

---

You can build [multi-platform images](https://docs.docker.com/build/building/multi-platform/) using
the `platforms` option, as shown in the following example:

> Note
>
> - For a list of available platforms, see the [Docker Setup Buildx](https://github.com/marketplace/actions/docker-setup-buildx)
>   action.
> - If you want support for more platforms, you can use QEMU with the [Docker Setup QEMU](https://github.com/docker/setup-qemu-action)
>   action.

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          platforms: linux/amd64,linux/arm64
          push: true
          tags: user/app:latest
```

## Build and load multi-platform images

The default Docker setup for GitHub Actions runners does not support loading
multi-platform images to the local image store of the runner after building
them. To load a multi-platform image, you need to enable the containerd image
store option for the Docker Engine.

There is no way to configure the default Docker setup in the GitHub Actions
runners directly, but you can use `docker/setup-docker-action` to customize the
Docker Engine and CLI settings for a job.

The following example workflow enables the containerd image store, builds a
multi-platform image, and loads the results into the GitHub runner's local
image store.

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Set up Docker
        uses: docker/setup-docker-action@v4
        with:
          daemon-config: |
            {
              "debug": true,
              "features": {
                "containerd-snapshotter": true
              }
            }

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          platforms: linux/amd64,linux/arm64
          load: true
          tags: user/app:latest
```

## Distribute build across multiple runners

Building multiple platforms on the same runner can significantly extend build
times, particularly when dealing with complex Dockerfiles or a high number of
target platforms. By distributing platform-specific builds across multiple
runners using a matrix strategy, you can drastically reduce build durations and
streamline your CI pipeline. These examples demonstrate how to allocate each
platform build to a dedicated runner, including ARM-native runners where
applicable, and create a unified manifest list using the
[buildx imagetools createcommand](https://docs.docker.com/reference/cli/docker/buildx/imagetools/create/).

The following workflow will build the image for each platform on a dedicated
runner using a matrix strategy and push by digest. Then, the `merge` job will
create manifest lists and push them to Docker Hub. The [metadataaction](https://github.com/docker/metadata-action)
is used to set tags and labels.

```yaml
name: ci

on:
  push:

env:
  REGISTRY_IMAGE: user/app

jobs:
  build:
    strategy:
      fail-fast: false
      matrix:
        include:
        - platform: linux/amd64
          runner: ubuntu-latest
        - platform: linux/arm64
          runner: ubuntu-24.04-arm
    runs-on: ${{ matrix.runner }}
    steps:
      - name: Prepare
        run: |
          platform=${{ matrix.platform }}
          echo "PLATFORM_PAIR=${platform//\//-}" >> $GITHUB_ENV

      - name: Docker meta
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY_IMAGE }}

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build and push by digest
        id: build
        uses: docker/build-push-action@v6
        with:
          platforms: ${{ matrix.platform }}
          labels: ${{ steps.meta.outputs.labels }}
          tags: ${{ env.REGISTRY_IMAGE }}
          outputs: type=image,push-by-digest=true,name-canonical=true,push=true

      - name: Export digest
        run: |
          mkdir -p ${{ runner.temp }}/digests
          digest="${{ steps.build.outputs.digest }}"
          touch "${{ runner.temp }}/digests/${digest#sha256:}"

      - name: Upload digest
        uses: actions/upload-artifact@v4
        with:
          name: digests-${{ env.PLATFORM_PAIR }}
          path: ${{ runner.temp }}/digests/*
          if-no-files-found: error
          retention-days: 1

  merge:
    runs-on: ubuntu-latest
    needs:
      - build
    steps:
      - name: Download digests
        uses: actions/download-artifact@v4
        with:
          path: ${{ runner.temp }}/digests
          pattern: digests-*
          merge-multiple: true

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Docker meta
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY_IMAGE }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}

      - name: Create manifest list and push
        working-directory: ${{ runner.temp }}/digests
        run: |
          docker buildx imagetools create $(jq -cr '.tags | map("-t " + .) | join(" ")' <<< "$DOCKER_METADATA_OUTPUT_JSON") \
            $(printf '${{ env.REGISTRY_IMAGE }}@sha256:%s ' *)

      - name: Inspect image
        run: |
          docker buildx imagetools inspect ${{ env.REGISTRY_IMAGE }}:${{ steps.meta.outputs.version }}
```

### With Bake

It's also possible to build on multiple runners using Bake, with the
[bake action](https://github.com/docker/bake-action).

You can find a live example [in this GitHub repository](https://github.com/crazy-max/docker-linguist).

The following example achieves the same results as described in
[the previous section](#distribute-build-across-multiple-runners).

```hcl
variable "DEFAULT_TAG" {
  default = "app:local"
}

// Special target: https://github.com/docker/metadata-action#bake-definition
target "docker-metadata-action" {
  tags = ["${DEFAULT_TAG}"]
}

// Default target if none specified
group "default" {
  targets = ["image-local"]
}

target "image" {
  inherits = ["docker-metadata-action"]
}

target "image-local" {
  inherits = ["image"]
  output = ["type=docker"]
}

target "image-all" {
  inherits = ["image"]
  platforms = [
    "linux/amd64",
    "linux/arm/v6",
    "linux/arm/v7",
    "linux/arm64"
  ]
}
```

```yaml
name: ci

on:
  push:

env:
  REGISTRY_IMAGE: user/app

jobs:
  prepare:
    runs-on: ubuntu-latest
    outputs:
      matrix: ${{ steps.platforms.outputs.matrix }}
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Create matrix
        id: platforms
        run: |
          echo "matrix=$(docker buildx bake image-all --print | jq -cr '.target."image-all".platforms')" >>${GITHUB_OUTPUT}

      - name: Show matrix
        run: |
          echo ${{ steps.platforms.outputs.matrix }}

      - name: Docker meta
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY_IMAGE }}

      - name: Rename meta bake definition file
        run: |
          mv "${{ steps.meta.outputs.bake-file }}" "${{ runner.temp }}/bake-meta.json"

      - name: Upload meta bake definition
        uses: actions/upload-artifact@v4
        with:
          name: bake-meta
          path: ${{ runner.temp }}/bake-meta.json
          if-no-files-found: error
          retention-days: 1

  build:
    needs:
      - prepare
    strategy:
      fail-fast: false
      matrix:
        platform: ${{ fromJson(needs.prepare.outputs.matrix) }}
    runs-on: ${{ startsWith(matrix.platform, 'linux/arm') && 'ubuntu-24.04-arm' || 'ubuntu-latest' }}
    steps:
      - name: Prepare
        run: |
          platform=${{ matrix.platform }}
          echo "PLATFORM_PAIR=${platform//\//-}" >> $GITHUB_ENV

      - name: Download meta bake definition
        uses: actions/download-artifact@v4
        with:
          name: bake-meta
          path: ${{ runner.temp }}

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build
        id: bake
        uses: docker/bake-action@v6
        with:
          files: |
            ./docker-bake.hcl
            cwd://${{ runner.temp }}/bake-meta.json
          targets: image
          set: |
            *.tags=${{ env.REGISTRY_IMAGE }}
            *.platform=${{ matrix.platform }}
            *.output=type=image,push-by-digest=true,name-canonical=true,push=true

      - name: Export digest
        run: |
          mkdir -p ${{ runner.temp }}/digests
          digest="${{ fromJSON(steps.bake.outputs.metadata).image['containerimage.digest'] }}"
          touch "${{ runner.temp }}/digests/${digest#sha256:}"

      - name: Upload digest
        uses: actions/upload-artifact@v4
        with:
          name: digests-${{ env.PLATFORM_PAIR }}
          path: ${{ runner.temp }}/digests/*
          if-no-files-found: error
          retention-days: 1

  merge:
    runs-on: ubuntu-latest
    needs:
      - build
    steps:
      - name: Download meta bake definition
        uses: actions/download-artifact@v4
        with:
          name: bake-meta
          path: ${{ runner.temp }}

      - name: Download digests
        uses: actions/download-artifact@v4
        with:
          path: ${{ runner.temp }}/digests
          pattern: digests-*
          merge-multiple: true

      - name: Login to DockerHub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Create manifest list and push
        working-directory: ${{ runner.temp }}/digests
        run: |
          docker buildx imagetools create $(jq -cr '.target."docker-metadata-action".tags | map(select(startswith("${{ env.REGISTRY_IMAGE }}")) | "-t " + .) | join(" ")' ${{ runner.temp }}/bake-meta.json) \
            $(printf '${{ env.REGISTRY_IMAGE }}@sha256:%s ' *)

      - name: Inspect image
        run: |
          docker buildx imagetools inspect ${{ env.REGISTRY_IMAGE }}:$(jq -r '.target."docker-metadata-action".args.DOCKER_META_VERSION' ${{ runner.temp }}/bake-meta.json)
```

---

# Named contexts with GitHub Actions

> Use additional contexts in multi-stage builds with GitHub Actions

# Named contexts with GitHub Actions

   Table of contents

---

You can define
[additional build contexts](https://docs.docker.com/reference/cli/docker/buildx/build/#build-context),
and access them in your Dockerfile with `FROM name` or `--from=name`. When
Dockerfile defines a stage with the same name it's overwritten.

This can be useful with GitHub Actions to reuse results from other builds or pin
an image to a specific tag in your workflow.

## Pin image to a tag

Replace `alpine:latest` with a pinned one:

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
RUN echo "Hello World"
```

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build
        uses: docker/build-push-action@v6
        with:
          build-contexts: |
            alpine=docker-image://alpine:3.23
          tags: myimage:latest
```

## Use image in subsequent steps

By default, the [Docker Setup Buildx](https://github.com/marketplace/actions/docker-setup-buildx)
action uses `docker-container` as a build driver, so built Docker images aren't
loaded automatically.

With named contexts you can reuse the built image:

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
RUN echo "Hello World"
```

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
        with:
          driver: docker

      - name: Build base image
        uses: docker/build-push-action@v6
        with:
          context: "{{defaultContext}}:base"
          load: true
          tags: my-base-image:latest

      - name: Build
        uses: docker/build-push-action@v6
        with:
          build-contexts: |
            alpine=docker-image://my-base-image:latest
          tags: myimage:latest
```

## Using with a container builder

As shown in the previous section we are not using the default
[docker-containerdriver](https://docs.docker.com/build/builders/drivers/docker-container/) for building with
named contexts. That's because this driver can't load an image from the Docker
store as it's isolated. To solve this problem you can use a [local registry](https://docs.docker.com/build/ci/github-actions/local-registry/)
to push your base image in your workflow:

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
RUN echo "Hello World"
```

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    services:
      registry:
        image: registry:3
        ports:
          - 5000:5000
    steps:
      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
        with:
          # network=host driver-opt needed to push to local registry
          driver-opts: network=host

      - name: Build base image
        uses: docker/build-push-action@v6
        with:
          context: "{{defaultContext}}:base"
          tags: localhost:5000/my-base-image:latest
          push: true

      - name: Build
        uses: docker/build-push-action@v6
        with:
          build-contexts: |
            alpine=docker-image://localhost:5000/my-base-image:latest
          tags: myimage:latest
```

---

# Push to multiple registries with GitHub Actions

> Push to multiple registries with GitHub Actions

# Push to multiple registries with GitHub Actions

---

The following workflow will connect you to Docker Hub and GitHub Container
Registry, and push the image to both registries:

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Login to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.repository_owner }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          platforms: linux/amd64,linux/arm64
          push: true
          tags: |
            user/app:latest
            user/app:1.0.0
            ghcr.io/user/app:latest
            ghcr.io/user/app:1.0.0
```

---

# Reproducible builds with GitHub Actions

> How to create reproducible builds in GitHub Actions using the SOURCE_EPOCH environment variable

# Reproducible builds with GitHub Actions

   Table of contents

---

`SOURCE_DATE_EPOCH` is a [standardized environment variable](https://reproducible-builds.org/docs/source-date-epoch/)
for instructing build tools to produce a reproducible output.
Setting the environment variable for a build makes the timestamps in the
image index, config, and file metadata reflect the specified Unix time.

To set the environment variable in GitHub Actions,
use the built-in `env` property on the build step.

## Unix epoch timestamps

The following example sets the `SOURCE_DATE_EPOCH` variable to 0, Unix epoch.

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build
        uses: docker/build-push-action@v6
        with:
          tags: user/app:latest
        env:
          SOURCE_DATE_EPOCH: 0
```

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build
        uses: docker/bake-action@v6
        env:
          SOURCE_DATE_EPOCH: 0
```

## Git commit timestamps

The following example sets `SOURCE_DATE_EPOCH` to the Git commit timestamp.

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Get Git commit timestamps
        run: echo "TIMESTAMP=$(git log -1 --pretty=%ct)" >> $GITHUB_ENV

      - name: Build
        uses: docker/build-push-action@v6
        with:
          tags: user/app:latest
        env:
          SOURCE_DATE_EPOCH: ${{ env.TIMESTAMP }}
```

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Get Git commit timestamps
        run: echo "TIMESTAMP=$(git log -1 --pretty=%ct)" >> $GITHUB_ENV

      - name: Build
        uses: docker/bake-action@v6
        env:
          SOURCE_DATE_EPOCH: ${{ env.TIMESTAMP }}
```

## Additional information

For more information about the `SOURCE_DATE_EPOCH` support in BuildKit,
see [BuildKit documentation](https://github.com/moby/buildkit/blob/master/docs/build-repro.md#source_date_epoch).

---

# Using secrets with GitHub Actions

> Example using secret mounts with GitHub Actions

# Using secrets with GitHub Actions

   Table of contents

---

A build secret is sensitive information, such as a password or API token, consumed as part of the build process.
Docker Build supports two forms of secrets:

- [Secret mounts](#secret-mounts) add secrets as files in the build container
  (under `/run/secrets` by default).
- [SSH mounts](#ssh-mounts) add SSH agent sockets or keys into the build container.

This page shows how to use secrets with GitHub Actions.
For an introduction to secrets in general, see
[Build secrets](https://docs.docker.com/build/building/secrets/).

## Secret mounts

In the following example uses and exposes the [GITHUB_TOKENsecret](https://docs.github.com/en/actions/security-guides/automatic-token-authentication#about-the-github_token-secret)
as provided by GitHub in your workflow.

First, create a `Dockerfile` that uses the secret:

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
RUN --mount=type=secret,id=github_token,env=GITHUB_TOKEN ...
```

In this example, the secret name is `github_token`. The following workflow
exposes this secret using the `secrets` input:

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build
        uses: docker/build-push-action@v6
        with:
          platforms: linux/amd64,linux/arm64
          tags: user/app:latest
          secrets: |
            "github_token=${{ secrets.GITHUB_TOKEN }}"
```

> Note
>
> You can also expose a secret file to the build with the `secret-files` input:
>
>
>
> ```yaml
> secret-files: |
>   "MY_SECRET=./secret.txt"
> ```

If you're using [GitHub secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
and need to handle multi-line value, you will need to place the key-value pair
between quotes:

```yaml
secrets: |
  "MYSECRET=${{ secrets.GPG_KEY }}"
  GIT_AUTH_TOKEN=abcdefghi,jklmno=0123456789
  "MYSECRET=aaaaaaaa
  bbbbbbb
  ccccccccc"
  FOO=bar
  "EMPTYLINE=aaaa

  bbbb
  ccc"
  "JSON_SECRET={""key1"":""value1"",""key2"":""value2""}"
```

| Key | Value |
| --- | --- |
| MYSECRET | *********************** |
| GIT_AUTH_TOKEN | abcdefghi,jklmno=0123456789 |
| MYSECRET | aaaaaaaa\nbbbbbbb\nccccccccc |
| FOO | bar |
| EMPTYLINE | aaaa\n\nbbbb\nccc |
| JSON_SECRET | {"key1":"value1","key2":"value2"} |

> Note
>
> Double escapes are needed for quote signs.

## SSH mounts

SSH mounts let you authenticate with SSH servers.
For example to perform a `git clone`,
or to fetch application packages from a private repository.

The following Dockerfile example uses an SSH mount
to fetch Go modules from a private GitHub repository.

```dockerfile
# syntax=docker/dockerfile:1

ARG GO_VERSION="1.25"

FROM golang:${GO_VERSION}-alpine AS base
ENV CGO_ENABLED=0
ENV GOPRIVATE="github.com/foo/*"
RUN apk add --no-cache file git rsync openssh-client
RUN mkdir -p -m 0700 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts
WORKDIR /src

FROM base AS vendor
# this step configure git and checks the ssh key is loaded
RUN --mount=type=ssh <<EOT
  set -e
  echo "Setting Git SSH protocol"
  git config --global url."git@github.com:".insteadOf "https://github.com/"
  (
    set +e
    ssh -T git@github.com
    if [ ! "$?" = "1" ]; then
      echo "No GitHub SSH key loaded exiting..."
      exit 1
    fi
  )
EOT
# this one download go modules
RUN --mount=type=bind,target=. \
    --mount=type=cache,target=/go/pkg/mod \
    --mount=type=ssh \
    go mod download -x

FROM vendor AS build
RUN --mount=type=bind,target=. \
    --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache \
    go build ...
```

To build this Dockerfile, you must specify an SSH mount that the builder can
use in the steps with `--mount=type=ssh`.

The following GitHub Action workflow uses the `MrSquaare/ssh-setup-action`
third-party action to bootstrap SSH setup on the GitHub runner. The action
creates a private key defined by the GitHub Action secret `SSH_GITHUB_PPK` and
adds it to the SSH agent socket file at `SSH_AUTH_SOCK`. The SSH mount in the
build step assume `SSH_AUTH_SOCK` by default, so there's no need to specify the
ID or path for the SSH agent socket explicitly.

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Set up SSH
        uses: MrSquaare/ssh-setup-action@2d028b70b5e397cf8314c6eaea229a6c3e34977a # v3.1.0
        with:
          host: github.com
          private-key: ${{ secrets.SSH_GITHUB_PPK }}
          private-key-name: github-ppk

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          ssh: default
          push: true
          tags: user/app:latest
```

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Set up SSH
        uses: MrSquaare/ssh-setup-action@2d028b70b5e397cf8314c6eaea229a6c3e34977a # v3.1.0
        with:
          host: github.com
          private-key: ${{ secrets.SSH_GITHUB_PPK }}
          private-key-name: github-ppk

      - name: Build
        uses: docker/bake-action@v6
        with:
          set: |
            *.ssh=default
```

---

# Share built image between jobs with GitHub Actions

> Share an image between runners without pushing to a registry

# Share built image between jobs with GitHub Actions

---

As each job is isolated in its own runner, you can't use your built image
between jobs, except if you're using [self-hosted runners](https://docs.github.com/en/actions/hosting-your-own-runners/about-self-hosted-runners)
or
[Docker Build Cloud](https://docs.docker.com/build-cloud).
However, you can [pass data between jobs](https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts#passing-data-between-jobs-in-a-workflow)
in a workflow using the [actions/upload-artifact](https://github.com/actions/upload-artifact)
and [actions/download-artifact](https://github.com/actions/download-artifact)
actions:

```yaml
name: ci

on:
  push:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build and export
        uses: docker/build-push-action@v6
        with:
          tags: myimage:latest
          outputs: type=docker,dest=${{ runner.temp }}/myimage.tar

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: myimage
          path: ${{ runner.temp }}/myimage.tar

  use:
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Download artifact
        uses: actions/download-artifact@v4
        with:
          name: myimage
          path: ${{ runner.temp }}

      - name: Load image
        run: |
          docker load --input ${{ runner.temp }}/myimage.tar
          docker image ls -a
```

---

# Test before push with GitHub Actions

> Here's how you can validate an image, before pushing it to a registry

# Test before push with GitHub Actions

---

In some cases, you might want to validate that the image works as expected
before pushing it. The following workflow implements several steps to achieve
this:

1. Build and export the image to Docker
2. Test your image
3. Multi-platform build and push the image

```yaml
name: ci

on:
  push:

env:
  TEST_TAG: user/app:test
  LATEST_TAG: user/app:latest

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build and export to Docker
        uses: docker/build-push-action@v6
        with:
          load: true
          tags: ${{ env.TEST_TAG }}

      - name: Test
        run: |
          docker run --rm ${{ env.TEST_TAG }}

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          platforms: linux/amd64,linux/arm64
          push: true
          tags: ${{ env.LATEST_TAG }}
```

> Note
>
> The `linux/amd64` image is only built once in this workflow. The image is
> built once, and the following steps use the internal cache from the first
> `Build and push` step. The second `Build and push` step only builds
> `linux/arm64`.

---

# Update Docker Hub description with GitHub Actions

> How to update the repository README in Docker Hub using with GitHub Actions

# Update Docker Hub description with GitHub Actions

---

You can update the Docker Hub repository description using a third party action
called [Docker Hub Description](https://github.com/peter-evans/dockerhub-description)
with this action:

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          push: true
          tags: user/app:latest

      - name: Update repo description
        uses: peter-evans/dockerhub-description@e98e4d1628a5f3be2be7c231e50981aee98723ae # v4.0.0
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
          repository: user/app
```

---

# Docker Build GitHub Actions

> Docker maintains a set of official GitHub Actions for building Docker images.

# Docker Build GitHub Actions

   Table of contents

---

GitHub Actions is a popular CI/CD platform for automating your build, test, and
deployment pipeline. Docker provides a set of official GitHub Actions for you to
use in your workflows. These official actions are reusable, easy-to-use
components for building, annotating, and pushing images.

The following GitHub Actions are available:

- [Build and push Docker images](https://github.com/marketplace/actions/build-and-push-docker-images):
  build and push Docker images with BuildKit.
- [Docker Buildx Bake](https://github.com/marketplace/actions/docker-buildx-bake):
  enables using high-level builds with [Bake](https://docs.docker.com/build/bake/).
- [Docker Login](https://github.com/marketplace/actions/docker-login):
  sign in to a Docker registry.
- [Docker Setup Buildx](https://github.com/marketplace/actions/docker-setup-buildx):
  creates and boots a BuildKit builder.
- [Docker Metadata action](https://github.com/marketplace/actions/docker-metadata-action):
  extracts metadata from Git reference and GitHub events to generate tags,
  labels, and annotations.
- [Docker Setup Compose](https://github.com/marketplace/actions/docker-setup-compose):
  installs and sets up [Compose](https://docs.docker.com/compose/).
- [Docker Setup Docker](https://github.com/marketplace/actions/docker-setup-docker):
  installs Docker Engine.
- [Docker Setup QEMU](https://github.com/marketplace/actions/docker-setup-qemu):
  installs [QEMU](https://github.com/qemu/qemu) static binaries for
  multi-platform builds.
- [Docker Scout](https://github.com/docker/scout-action):
  analyze Docker images for security vulnerabilities.

Using Docker's actions provides an easy-to-use interface, while still allowing
flexibility for customizing build parameters.

## Examples

If you're looking for examples on how to use the Docker GitHub Actions,
refer to the following sections:

- [Add image annotations with GitHub Actions](https://docs.docker.com/build/ci/github-actions/annotations/)
- [Add SBOM and provenance attestations with GitHub Actions](https://docs.docker.com/build/ci/github-actions/attestations/)
- [Validating build configuration with GitHub Actions](https://docs.docker.com/build/ci/github-actions/checks/)
- [Using secrets with GitHub Actions](https://docs.docker.com/build/ci/github-actions/secrets/)
- [GitHub Actions build summary](https://docs.docker.com/build/ci/github-actions/build-summary/)
- [Configuring your GitHub Actions builder](https://docs.docker.com/build/ci/github-actions/configure-builder/)
- [Cache management with GitHub Actions](https://docs.docker.com/build/ci/github-actions/cache/)
- [Copy image between registries with GitHub Actions](https://docs.docker.com/build/ci/github-actions/copy-image-registries/)
- [Export to Docker with GitHub Actions](https://docs.docker.com/build/ci/github-actions/export-docker/)
- [Local registry with GitHub Actions](https://docs.docker.com/build/ci/github-actions/local-registry/)
- [Multi-platform image with GitHub Actions](https://docs.docker.com/build/ci/github-actions/multi-platform/)
- [Named contexts with GitHub Actions](https://docs.docker.com/build/ci/github-actions/named-contexts/)
- [Push to multiple registries with GitHub Actions](https://docs.docker.com/build/ci/github-actions/push-multi-registries/)
- [Reproducible builds with GitHub Actions](https://docs.docker.com/build/ci/github-actions/reproducible-builds/)
- [Share built image between jobs with GitHub Actions](https://docs.docker.com/build/ci/github-actions/share-image-jobs/)
- [Manage tags and labels with GitHub Actions](https://docs.docker.com/build/ci/github-actions/manage-tags-labels/)
- [Test before push with GitHub Actions](https://docs.docker.com/build/ci/github-actions/test-before-push/)
- [Update Docker Hub description with GitHub Actions](https://docs.docker.com/build/ci/github-actions/update-dockerhub-desc/)

## Get started with GitHub Actions

The
[Introduction to GitHub Actions with Docker](https://docs.docker.com/guides/gha/) guide walks
you through the process of setting up and using Docker GitHub Actions for
building Docker images, and pushing images to Docker Hub.

---

# Continuous integration with Docker

> Using Docker for continuous integration

# Continuous integration with Docker

   Table of contents

---

Continuous Integration (CI) is the part of the development process where you're
looking to get your code changes merged with the main branch of the project. At
this point, development teams run tests and builds to vet that the code changes
don't cause any unwanted or unexpected behaviors.

![Git branches about to get merged](https://docs.docker.com/build/ci/images/continuous-integration.svg)  ![Git branches about to get merged](https://docs.docker.com/build/ci/images/continuous-integration.svg)

There are several uses for Docker at this stage of development, even if you
don't end up packaging your application as a container image.

## Docker as a build environment

Containers are reproducible, isolated environments that yield predictable
results. Building and testing your application in a Docker container makes it
easier to prevent unexpected behaviors from occurring. Using a Dockerfile, you
define the exact requirements for the build environment, including programming
runtimes, operating system, binaries, and more.

Using Docker to manage your build environment also eases maintenance. For
example, updating to a new version of a programming runtime can be as simple as
changing a tag or digest in a Dockerfile. No need to SSH into a pet VM to
manually reinstall a newer version and update the related configuration files.

Additionally, just as you expect third-party open source packages to be secure,
the same should go for your build environment. You can scan and index a builder
image, just like you would for any other containerized application.

The following links provide instructions for how you can get started using
Docker for building your applications in CI:

- [GitHub Actions](https://docs.github.com/en/actions/creating-actions/creating-a-docker-container-action)
- [GitLab](https://docs.gitlab.com/runner/executors/docker.html)
- [Circle CI](https://circleci.com/docs/using-docker/)
- [Render](https://render.com/docs/docker)

### Docker in Docker

You can also use a Dockerized build environment to build container images using
Docker. That is, your build environment runs inside a container which itself is
equipped to run Docker builds. This method is referred to as "Docker in Docker".

Docker provides an official [Docker image](https://hub.docker.com/_/docker)
that you can use for this purpose.

## What's next

Docker maintains a set of official GitHub Actions that you can use to build,
annotate, and push container images on the GitHub Actions platform. See
[Introduction to GitHub Actions](https://docs.docker.com/build/ci/github-actions/) to learn more and
get started.
