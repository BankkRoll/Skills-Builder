# Checking your build configuration and more

# Checking your build configuration

> Learn how to use build checks to validate your build configuration.

# Checking your build configuration

   Table of contents

---

Availability: Beta
Requires: Docker Buildx [0.15.0](https://github.com/docker/buildx/releases/tag/v0.15.0) and later

Build checks are a feature introduced in Dockerfile 1.8. It lets you validate
your build configuration and conduct a series of checks prior to executing your
build. Think of it as an advanced form of linting for your Dockerfile and build
options, or a dry-run mode for builds.

You can find the list of checks available, and a description of each, in the
[Build checks reference](https://docs.docker.com/reference/build-checks/).

## How build checks work

Typically, when you run a build, Docker executes the build steps in your
Dockerfile and build options as specified. With build checks, rather than
executing the build steps, Docker checks the Dockerfile and options you provide
and reports any issues it detects.

Build checks are useful for:

- Validating your Dockerfile and build options before running a build.
- Ensuring that your Dockerfile and build options are up-to-date with the
  latest best practices.
- Identifying potential issues or anti-patterns in your Dockerfile and build
  options.

> Tip
>
> To improve linting, code navigation, and vulnerability scanning of your Dockerfiles in Visual Studio Code
> see [Docker VS Code Extension](https://marketplace.visualstudio.com/items?itemName=docker.docker).

## Build with checks

Build checks are supported in:

- Buildx version 0.15.0 and later
- [docker/build-push-action](https://github.com/docker/build-push-action) version 6.6.0 and later
- [docker/bake-action](https://github.com/docker/bake-action) version 5.6.0 and later

Invoking a build runs the checks by default, and displays any violations in the
build output. For example, the following command both builds the image and runs
the checks:

```console
$ docker build .
[+] Building 3.5s (11/11) FINISHED
...

1 warning found (use --debug to expand):
  - Lint Rule 'JSONArgsRecommended': JSON arguments recommended for CMD to prevent unintended behavior related to OS signals (line 7)
```

In this example, the build ran successfully, but a
[JSONArgsRecommended](https://docs.docker.com/reference/build-checks/json-args-recommended/) warning
was reported, because `CMD` instructions should use JSON array syntax.

With the GitHub Actions, the checks display in the diff view of pull requests.

```yaml
name: Build and push Docker images
on:
  push:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Build and push
        uses: docker/build-push-action@v6.6.0
```

![GitHub Actions build check annotations](https://docs.docker.com/build/images/gha-check-annotations.png)  ![GitHub Actions build check annotations](https://docs.docker.com/build/images/gha-check-annotations.png)

### More verbose output

Check warnings for a regular `docker build` display a concise message
containing the rule name, the message, and the line number of where in the
Dockerfile the issue originated. If you want to see more detailed information
about the checks, you can use the `--debug` flag. For example:

```console
$ docker --debug build .
[+] Building 3.5s (11/11) FINISHED
...

 1 warning found:
 - JSONArgsRecommended: JSON arguments recommended for CMD to prevent unintended behavior related to OS signals (line 4)
JSON arguments recommended for ENTRYPOINT/CMD to prevent unintended behavior related to OS signals
More info: https://docs.docker.com/go/dockerfile/rule/json-args-recommended/
Dockerfile:4
--------------------
   2 |
   3 |     FROM alpine
   4 | >>> CMD echo "Hello, world!"
   5 |
--------------------
```

With the `--debug` flag, the output includes a link to the documentation for
the check, and a snippet of the Dockerfile where the issue was found.

## Check a build without building

To run build checks without actually building, you can use the `docker build`
command as you typically would, but with the addition of the `--check` flag.
Here's an example:

```console
$ docker build --check .
```

Instead of executing the build steps, this command only runs the checks and
reports any issues it finds. If there are any issues, they will be reported in
the output. For example:

Output with --check

```text
[+] Building 1.5s (5/5) FINISHED
=> [internal] connecting to local controller
=> [internal] load build definition from Dockerfile
=> => transferring dockerfile: 253B
=> [internal] load metadata for docker.io/library/node:22
=> [auth] library/node:pull token for registry-1.docker.io
=> [internal] load .dockerignore
=> => transferring context: 50B
JSONArgsRecommended - https://docs.docker.com/go/dockerfile/rule/json-args-recommended/
JSON arguments recommended for ENTRYPOINT/CMD to prevent unintended behavior related to OS signals
Dockerfile:7
--------------------
5 |
6 |     COPY index.js .
7 | >>> CMD node index.js
8 |
--------------------
```

This output with `--check` shows the [verbose message](#more-verbose-output)
for the check.

Unlike a regular build, if any violations are reported when using the `--check`
flag, the command exits with a non-zero status code.

## Fail build on check violations

Check violations for builds are reported as warnings, with exit code 0, by
default. You can configure Docker to fail the build when violations are
reported, using a `check=error=true` directive in your Dockerfile. This will
cause the build to error out when after the build checks are run, before the
actual build gets executed.

Dockerfile

| 12345 | # syntax=docker/dockerfile:1# check=error=trueFROMalpineCMDecho"Hello, world!" |
| --- | --- |

Without the `# check=error=true` directive, this build would complete with an
exit code of 0. However, with the directive, build check violation results in
non-zero exit code:

```console
$ docker build .
[+] Building 1.5s (5/5) FINISHED
...

 1 warning found (use --debug to expand):
 - JSONArgsRecommended: JSON arguments recommended for CMD to prevent unintended behavior related to OS signals (line 5)
Dockerfile:1
--------------------
   1 | >>> # syntax=docker/dockerfile:1
   2 |     # check=error=true
   3 |
--------------------
ERROR: lint violation found for rules: JSONArgsRecommended
$ echo $?
1
```

You can also set the error directive on the CLI by passing the
`BUILDKIT_DOCKERFILE_CHECK` build argument:

```console
$ docker build --check --build-arg "BUILDKIT_DOCKERFILE_CHECK=error=true" .
```

## Skip checks

By default, all checks are run when you build an image. If you want to skip
specific checks, you can use the `check=skip` directive in your Dockerfile.
The `skip` parameter takes a CSV string of the check IDs you want to skip.
For example:

Dockerfile

```dockerfile
# syntax=docker/dockerfile:1
# check=skip=JSONArgsRecommended,StageNameCasing

FROM alpine AS BASE_STAGE
CMD echo "Hello, world!"
```

Building this Dockerfile results in no check violations.

You can also skip checks by passing the `BUILDKIT_DOCKERFILE_CHECK` build
argument with a CSV string of check IDs you want to skip. For example:

```console
$ docker build --check --build-arg "BUILDKIT_DOCKERFILE_CHECK=skip=JSONArgsRecommended,StageNameCasing" .
```

To skip all checks, use the `skip=all` parameter:

Dockerfile

```dockerfile
# syntax=docker/dockerfile:1
# check=skip=all
```

## Combine error and skip parameters for check directives

To both skip specific checks and error on check violations, pass both the
`skip` and `error` parameters separated by a semi-colon (`;`) to the `check`
directive in your Dockerfile or in a build argument. For example:

Dockerfile

```dockerfile
# syntax=docker/dockerfile:1
# check=skip=JSONArgsRecommended,StageNameCasing;error=true
```

Build argument

```console
$ docker build --check --build-arg "BUILDKIT_DOCKERFILE_CHECK=skip=JSONArgsRecommended,StageNameCasing;error=true" .
```

## Experimental checks

Before checks are promoted to stable, they may be available as experimental
checks. Experimental checks are disabled by default. To see the list of
experimental checks available, refer to the
[Build checks reference](https://docs.docker.com/reference/build-checks/).

To enable all experimental checks, set the `BUILDKIT_DOCKERFILE_CHECK` build
argument to `experimental=all`:

```console
$ docker build --check --build-arg "BUILDKIT_DOCKERFILE_CHECK=experimental=all" .
```

You can also enable experimental checks in your Dockerfile using the `check`
directive:

Dockerfile

```dockerfile
# syntax=docker/dockerfile:1
# check=experimental=all
```

To selectively enable experimental checks, you can pass a CSV string of the
check IDs you want to enable, either to the `check` directive in your Dockerfile
or as a build argument. For example:

Dockerfile

```dockerfile
# syntax=docker/dockerfile:1
# check=experimental=JSONArgsRecommended,StageNameCasing
```

Note that the `experimental` directive takes precedence over the `skip`
directive, meaning that experimental checks will run regardless of the `skip`
directive you have set. For example, if you set `skip=all` and enable
experimental checks, the experimental checks will still run:

Dockerfile

```dockerfile
# syntax=docker/dockerfile:1
# check=skip=all;experimental=all
```

## Further reading

For more information about using build checks, see:

- [Build checks reference](https://docs.docker.com/reference/build-checks/)
- [Validating build configuration with GitHub Actions](https://docs.docker.com/build/ci/github-actions/checks/)

---

# Add image annotations with GitHub Actions

> Add OCI annotations to image components using GitHub Actions

# Add image annotations with GitHub Actions

   Table of contents

---

Annotations let you specify arbitrary metadata for OCI image components, such
as manifests, indexes, and descriptors.

To add annotations when building images with GitHub Actions, use the
[metadata-action](https://github.com/docker/metadata-action#overwrite-labels-and-annotations) to automatically create OCI-compliant annotations. The
metadata action creates an `annotations` output that you can reference, both
with [build-push-action](https://github.com/docker/build-push-action/) and [bake-action](https://github.com/docker/bake-action/).

```yaml
name: ci

on:
  push:

env:
  IMAGE_NAME: user/app

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.IMAGE_NAME }}

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          tags: ${{ steps.meta.outputs.tags }}
          annotations: ${{ steps.meta.outputs.annotations }}
          push: true
```

```yaml
name: ci

on:
  push:

env:
  IMAGE_NAME: user/app

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.IMAGE_NAME }}

      - name: Build
        uses: docker/bake-action@v6
        with:
          files: |
            ./docker-bake.hcl
            cwd://${{ steps.meta.outputs.bake-file-tags }}
            cwd://${{ steps.meta.outputs.bake-file-annotations }}
          push: true
```

## Configure annotation level

By default, annotations are placed on image manifests. To configure the
[annotation level](https://docs.docker.com/build/metadata/annotations/#specify-annotation-level), set
the `DOCKER_METADATA_ANNOTATIONS_LEVELS` environment variable on the
`metadata-action` step to a comma-separated list of all the levels that you
want to annotate. For example, setting `DOCKER_METADATA_ANNOTATIONS_LEVELS` to
`index` results in annotations on the image index instead of the manifests.

The following example creates annotations on both the image index and
manifests.

```yaml
name: ci

on:
  push:

env:
  IMAGE_NAME: user/app

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.IMAGE_NAME }}
        env:
          DOCKER_METADATA_ANNOTATIONS_LEVELS: manifest,index

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          tags: ${{ steps.meta.outputs.tags }}
          annotations: ${{ steps.meta.outputs.annotations }}
          push: true
```

> Note
>
> The build must produce the components that you want to annotate. For example,
> to annotate an image index, the build must produce an index. If the build
> produces only a manifest and you specify `index` or `index-descriptor`, the
> build fails.

---

# Add SBOM and provenance attestations with GitHub Actions

> Add SBOM and provenance attestations to your images with GitHub Actions

# Add SBOM and provenance attestations with GitHub Actions

   Table of contents

---

Software Bill of Material (SBOM) and provenance
[attestations](https://docs.docker.com/build/metadata/attestations/) add metadata about the contents of
your image, and how it was built.

Attestations are supported with version 4 and later of the
`docker/build-push-action`.

## Default provenance

The `docker/build-push-action` GitHub Action automatically adds provenance
attestations to your image, with the following conditions:

- If the GitHub repository is public, provenance attestations with `mode=max`
  are automatically added to the image.
- If the GitHub repository is private, provenance attestations with `mode=min`
  are automatically added to the image.
- If you're using the [dockerexporter](https://docs.docker.com/build/exporters/oci-docker/), or
  you're loading the build results to the runner with `load: true`, no
  attestations are added to the image. These output formats don't support
  attestations.

> Warning
>
> If you're using `docker/build-push-action` to build images for code in a
> public GitHub repository, the provenance attestations attached to your image
> by default contains the values of build arguments. If you're misusing build
> arguments to pass secrets to your build, such as user credentials or
> authentication tokens, those secrets are exposed in the provenance
> attestation. Refactor your build to pass those secrets using
> [secret mounts](https://docs.docker.com/reference/cli/docker/buildx/build/#secret)
> instead. Also remember to rotate any secrets you may have exposed.

## Max-level provenance

It's recommended that you build your images with max-level provenance
attestations. Private repositories only add min-level provenance by default,
but you can manually override the provenance level by setting the `provenance`
input on the `docker/build-push-action` GitHub Action to `mode=max`.

Note that adding attestations to an image means you must push the image to a
registry directly, as opposed to loading the image to the local image store of
the runner. This is because the local image store doesn't support loading
images with attestations.

```yaml
name: ci

on:
  push:

env:
  IMAGE_NAME: user/app

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.IMAGE_NAME }}

      - name: Build and push image
        uses: docker/build-push-action@v6
        with:
          push: true
          provenance: mode=max
          tags: ${{ steps.meta.outputs.tags }}
```

## SBOM

SBOM attestations aren't automatically added to the image. To add SBOM
attestations, set the `sbom` input of the `docker/build-push-action` to true.

Note that adding attestations to an image means you must push the image to a
registry directly, as opposed to loading the image to the local image store of
the runner. This is because the local image store doesn't support loading
images with attestations.

```yaml
name: ci

on:
  push:

env:
  IMAGE_NAME: user/app

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.IMAGE_NAME }}

      - name: Build and push image
        uses: docker/build-push-action@v6
        with:
          sbom: true
          push: true
          tags: ${{ steps.meta.outputs.tags }}
```

---

# GitHub Actions build summary

> Get an overview of your Docker Builds with GitHub Actions

# GitHub Actions build summary

   Table of contents

---

Docker's GitHub Actions for building and pushing images generate a job summary
for your build that outlines the execution and materials used:

- A summary showing the Dockerfile used, the build duration, and cache utilization
- Inputs for the build, such as build arguments, tags, labels, and build contexts
- For builds with [Bake](https://docs.docker.com/build/bake/), the full bake definition for the build

![A GitHub Actions build summary](https://docs.docker.com/build/ci/images/gha_build_summary.png)  ![A GitHub Actions build summary](https://docs.docker.com/build/ci/images/gha_build_summary.png)

Job summaries for Docker builds appear automatically if you use the following
versions of the [Build and push Docker images](https://github.com/marketplace/actions/build-and-push-docker-images)
or [Docker Buildx Bake](https://github.com/marketplace/actions/docker-buildx-bake)
GitHub Actions:

- `docker/build-push-action@v6`
- `docker/bake-action@v6`

To view the job summary, open the details page for the job in GitHub after the
job has finished. The summary is available for both failed and successful
builds. In the case of a failed build, the summary also displays the error
message that caused the build to fail:

![Builds summary error message](https://docs.docker.com/build/ci/images/build_summary_error.png)  ![Builds summary error message](https://docs.docker.com/build/ci/images/build_summary_error.png)

## Import build records to Docker Desktop

Availability: Beta
Requires: Docker Desktop
[4.31](https://docs.docker.com/desktop/release-notes/#4310) and later

The job summary includes a link for downloading a build record archive for the
run. The build record archive is a ZIP file containing the details about a build
(or builds, if you use `docker/bake-action` to build multiple targets). You can
import this build record archive into Docker Desktop, which gives you a
powerful, graphical interface for further analyzing the build's performance via
the
[Docker DesktopBuildsview](https://docs.docker.com/desktop/use-desktop/builds/).

To import the build record archive into Docker Desktop:

1. Download and install
  [Docker Desktop](https://docs.docker.com/get-started/get-docker/).
2. Download the build record archive from the job summary in GitHub Actions.
3. Open the **Builds** view in Docker Desktop.
4. Select the **Import build** button, and then browse for the `.zip` archive
  job summary that you downloaded. Alternatively, you can drag-and-drop the
  build record archive ZIP file onto the Docker Desktop window after opening
  the import build dialog.
5. Select **Import** to add the build records.

After a few seconds, the builds from the GitHub Actions run appear under the
**Completed builds** tab in the Builds view. To inspect a build and see a
detailed view of all the inputs, results, build steps, and cache utilization,
select the item in the list.

## Disable job summary

To disable job summaries, set the `DOCKER_BUILD_SUMMARY` environment variable
in the YAML configuration for your build step:

```yaml
- name: Build
        uses: docker/build-push-action@v6
        env:
          DOCKER_BUILD_SUMMARY: false
        with:
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
```

## Disable build record upload

To disable the upload of the build record archive to GitHub, set the
`DOCKER_BUILD_RECORD_UPLOAD` environment variable in the YAML configuration for
your build step:

```yaml
- name: Build
        uses: docker/build-push-action@v6
        env:
          DOCKER_BUILD_RECORD_UPLOAD: false
        with:
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
```

With this configuration, the build summary is still generated, but does not
contain a link to download the build record archive.

## Limitations

Build summaries are currently not supported for:

- Repositories hosted on GitHub Enterprise Servers. Summaries can only be
  viewed for repositories hosted on GitHub.com.

---

# Cache management with GitHub Actions

# Cache management with GitHub Actions

   Table of contents

---

This page contains examples on using the cache storage backends with GitHub
Actions.

> Note
>
> See [Cache storage backends](https://docs.docker.com/build/cache/backends/) for more
> details about cache storage backends.

## Inline cache

In most cases you want to use the [inline cache exporter](https://docs.docker.com/build/cache/backends/inline/).
However, note that the `inline` cache exporter only supports `min` cache mode.
To use `max` cache mode, push the image and the cache separately using the
registry cache exporter with the `cache-to` option, as shown in the [registry cache example](#registry-cache).

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

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          push: true
          tags: user/app:latest
          cache-from: type=registry,ref=user/app:latest
          cache-to: type=inline
```

## Registry cache

You can import/export cache from a cache manifest or (special) image
configuration on the registry with the [registry cache exporter](https://docs.docker.com/build/cache/backends/registry/).

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

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          push: true
          tags: user/app:latest
          cache-from: type=registry,ref=user/app:buildcache
          cache-to: type=registry,ref=user/app:buildcache,mode=max
```

## GitHub cache

### Cache backend API

Availability: Experimental

The [GitHub Actions cache exporter](https://docs.docker.com/build/cache/backends/gha/)
backend uses the [GitHub Cache service API](https://github.com/tonistiigi/go-actions-cache)
to fetch and upload cache blobs. That's why you should only use this cache
backend in a GitHub Action workflow, as the `url` (`$ACTIONS_RESULTS_URL`) and
`token` (`$ACTIONS_RUNTIME_TOKEN`) attributes only get populated in a workflow
context.

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

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          push: true
          tags: user/app:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

> Important
>
> Starting [April 15th, 2025, only GitHub Cache service API v2 will be supported](https://gh.io/gha-cache-sunset).
>
>
>
> If you encounter the following error during your build:
>
>
>
> ```console
> ERROR: failed to solve: This legacy service is shutting down, effective April 15, 2025. Migrate to the new service ASAP. For more information: https://gh.io/gha-cache-sunset
> ```
>
>
>
> You're probably using outdated tools that only support the legacy GitHub
> Cache service API v1. Here are the minimum versions you need to upgrade to
> depending on your use case:
>
>
>
> - Docker Buildx >= v0.21.0
> - BuildKit >= v0.20.0
> - Docker Compose >= v2.33.1
> - Docker Engine >= v28.0.0 (if you're building using the Docker driver with containerd image store enabled)
>
>
>
> If you're building using the `docker/build-push-action` or `docker/bake-action`
> actions on GitHub hosted runners, Docker Buildx and BuildKit are already up
> to date but on self-hosted runners, you may need to update them yourself.
> Alternatively, you can use the `docker/setup-buildx-action` action to install
> the latest version of Docker Buildx:
>
>
>
> ```yaml
> - name: Set up Docker Buildx
>   uses: docker/setup-buildx-action@v3
>   with:
>    version: latest
> ```
>
>
>
> If you're building using Docker Compose, you can use the
> `docker/setup-compose-action` action:
>
>
>
> ```yaml
> - name: Set up Docker Compose
>   uses: docker/setup-compose-action@v1
>   with:
>    version: latest
> ```
>
>
>
> If you're building using the Docker Engine with the containerd image store
> enabled, you can use the `docker/setup-docker-action` action:
>
>
>
> ```yaml
> -
>   name: Set up Docker
>   uses: docker/setup-docker-action@v4
>   with:
>     version: latest
>     daemon-config: |
>       {
>         "features": {
>           "containerd-snapshotter": true
>         }
>       }
> ```

### Cache mounts

BuildKit doesn't preserve cache mounts in the GitHub Actions cache by default.
To put your cache mounts into GitHub Actions cache and reuse it
between builds, you can use a workaround provided by
[reproducible-containers/buildkit-cache-dance](https://github.com/reproducible-containers/buildkit-cache-dance).

This GitHub Action creates temporary containers to extract and inject the
cache mount data with your Docker build steps.

The following example shows how to use this workaround with a Go project.

Example Dockerfile in `build/package/Dockerfile`

```Dockerfile
FROM golang:1.21.1-alpine as base-build

WORKDIR /build

RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=bind,source=go.mod,target=go.mod \
    --mount=type=bind,source=go.sum,target=go.sum \
    go mod download

RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    --mount=type=bind,target=. \
    go build -o /bin/app ./src
...
```

Example CI action

```yaml
name: ci

on:
  push:

jobs:
  build:
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

      - name: Docker meta
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: user/app
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}

      - name: Go Build Cache for Docker
        uses: actions/cache@v4
        with:
          path: go-build-cache
          key: ${{ runner.os }}-go-build-cache-${{ hashFiles('**/go.sum') }}

      - name: Inject go-build-cache
        uses: reproducible-containers/buildkit-cache-dance@4b2444fec0c0fb9dbf175a96c094720a692ef810 # v2.1.4
        with:
          cache-source: go-build-cache

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          cache-from: type=gha
          cache-to: type=gha,mode=max
          file: build/package/Dockerfile
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          platforms: linux/amd64,linux/arm64
```

For more information about this workaround, refer to the
[GitHub repository](https://github.com/reproducible-containers/buildkit-cache-dance).

### Local cache

> Warning
>
> At the moment, old cache entries aren't deleted, so the cache size [keeps growing](https://github.com/docker/build-push-action/issues/252).
> The following example uses the `Move cache` step as a workaround (see [moby/buildkit#1896](https://github.com/moby/buildkit/issues/1896)
> for more info).

You can also leverage [GitHub cache](https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows)
using the [actions/cache](https://github.com/actions/cache) and [local cache exporter](https://docs.docker.com/build/cache/backends/local/)
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

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Cache Docker layers
        uses: actions/cache@v4
        with:
          path: ${{ runner.temp }}/.buildx-cache
          key: ${{ runner.os }}-buildx-${{ github.sha }}
          restore-keys: |
            ${{ runner.os }}-buildx-

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          push: true
          tags: user/app:latest
          cache-from: type=local,src=${{ runner.temp }}/.buildx-cache
          cache-to: type=local,dest=${{ runner.temp }}/.buildx-cache-new,mode=max

      - # Temp fix
        # https://github.com/docker/build-push-action/issues/252
        # https://github.com/moby/buildkit/issues/1896
        name: Move cache
        run: |
          rm -rf ${{ runner.temp }}/.buildx-cache
          mv ${{ runner.temp }}/.buildx-cache-new ${{ runner.temp }}/.buildx-cache
```

---

# Validating build configuration with GitHub Actions

> Discover how to validate your build configuration and identify best practice violations using build checks in GitHub Actions.

# Validating build configuration with GitHub Actions

   Table of contents

---

[Build checks](https://docs.docker.com/build/checks/) let you validate your `docker build`
configuration without actually running the build.

## Run checks withdocker/build-push-action

To run build checks in a GitHub Actions workflow with the `build-push-action`,
set the `call` input parameter to `check`. With this set, the workflow fails if
any check warnings are detected for your build's configuration.

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
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Validate build configuration
        uses: docker/build-push-action@v6
        with:
          call: check

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          push: true
          tags: user/app:latest
```

## Run checks withdocker/bake-action

If you're using Bake and `docker/bake-action` to run your builds, you don't
need to specify any special inputs in your GitHub Actions workflow
configuration. Instead, define a Bake target that calls the `check` method,
and invoke that target in your CI.

```hcl
target "build" {
  dockerfile = "Dockerfile"
  args = {
    FOO = "bar"
  }
}
target "validate-build" {
  inherits = ["build"]
  call = "check"
}
```

```yaml
name: ci

on:
  push:

env:
  IMAGE_NAME: user/app

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Validate build configuration
        uses: docker/bake-action@v6
        with:
          targets: validate-build

      - name: Build
        uses: docker/bake-action@v6
        with:
          targets: build
          push: true
```

### Using thecallinput directly

You can also set the build method with the `call` input which is equivalent to using the `--call` flag with `docker buildx bake`

For example, to run a check without defining `call` in your Bake file:

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

      - name: Validate build configuration
        uses: docker/bake-action@v6
        with:
          targets: build
          call: check
```

---

# Configuring your GitHub Actions builder

> Configuring BuildKit instances for building in CI with GitHub Actions

# Configuring your GitHub Actions builder

   Table of contents

---

This page contains instructions on configuring your BuildKit instances when
using our [Setup Buildx Action](https://github.com/docker/setup-buildx-action).

## Version pinning

By default, the action will attempt to use the latest version of [Buildx](https://github.com/docker/buildx)
available on the GitHub Runner (the build client) and the latest release of
[BuildKit](https://github.com/moby/buildkit) (the build server).

To pin to a specific version of Buildx, use the `version` input. For example,
to pin to Buildx v0.10.0:

```yaml
- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v3
  with:
    version: v0.10.0
```

To pin to a specific version of BuildKit, use the `image` option in the
`driver-opts` input. For example, to pin to BuildKit v0.11.0:

```yaml
- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v3
  with:
    driver-opts: image=moby/buildkit:v0.11.0
```

## BuildKit container logs

To display BuildKit container logs when using the `docker-container` driver,
you must either [enable step debug logging](https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows/enabling-debug-logging#enabling-step-debug-logging),
or set the `--debug` buildkitd flag in the [Docker Setup Buildx](https://github.com/marketplace/actions/docker-setup-buildx) action:

```yaml
name: ci

on:
  push:

jobs:
  buildx:
    runs-on: ubuntu-latest
    steps:
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
        with:
          buildkitd-flags: --debug

      - name: Build
        uses: docker/build-push-action@v6
```

Logs will be available at the end of a job:

![BuildKit container logs](https://docs.docker.com/build/ci/github-actions/images/buildkit-container-logs.png)  ![BuildKit container logs](https://docs.docker.com/build/ci/github-actions/images/buildkit-container-logs.png)

## BuildKit Daemon configuration

You can provide a [BuildKit configuration](https://docs.docker.com/build/buildkit/toml-configuration/)
to your builder if you're using the
[docker-containerdriver](https://docs.docker.com/build/builders/drivers/docker-container/)
(default) with the `config` or `buildkitd-config-inline` inputs:

### Registry mirror

You can configure a registry mirror using an inline block directly in your
workflow with the `buildkitd-config-inline` input:

```yaml
name: ci

on:
  push:

jobs:
  buildx:
    runs-on: ubuntu-latest
    steps:
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
        with:
          buildkitd-config-inline: |
            [registry."docker.io"]
              mirrors = ["mirror.gcr.io"]
```

For more information about using a registry mirror, see [Registry mirror](https://docs.docker.com/build/buildkit/configure/#registry-mirror).

### Max parallelism

You can limit the parallelism of the BuildKit solver which is particularly
useful for low-powered machines.

You can use the `buildkitd-config-inline` input like the previous example, or you can use
a dedicated BuildKit config file from your repository if you want with the
`config` input:

```toml
# .github/buildkitd.toml
[worker.oci]
  max-parallelism = 4
```

```yaml
name: ci

on:
  push:

jobs:
  buildx:
    runs-on: ubuntu-latest
    steps:
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
        with:
          config: .github/buildkitd.toml
```

## Append additional nodes to the builder

Buildx supports running builds on multiple machines. This is useful for building
[multi-platform images](https://docs.docker.com/build/building/multi-platform/) on native nodes for
more complicated cases that aren't handled by QEMU. Building on native nodes
generally has better performance, and allows you to distribute the build across
multiple machines.

You can append nodes to the builder you're creating using the `append` option.
It takes input in the form of a YAML string document to remove limitations
intrinsically linked to GitHub Actions: you can only use strings in the input
fields:

| Name | Type | Description |
| --- | --- | --- |
| name | String | Name of the node. If empty, it's the name of the builder it belongs to, with an index number suffix. This is useful to set it if you want to modify/remove a node in an underlying step of you workflow. |
| endpoint | String | Docker context or endpointof the node to add to the builder |
| driver-opts | List | List of additionaldriver-specific options |
| buildkitd-flags | String | Flags for buildkitddaemon |
| platforms | String | Fixedplatformsfor the node. If not empty, values take priority over the detected ones. |

Here is an example using remote nodes with the
[remotedriver](https://docs.docker.com/build/builders/drivers/remote/)
and [TLS authentication](#tls-authentication):

```yaml
name: ci

on:
  push:

jobs:
  buildx:
    runs-on: ubuntu-latest
    steps:
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
        with:
          driver: remote
          endpoint: tcp://oneprovider:1234
          append: |
            - endpoint: tcp://graviton2:1234
              platforms: linux/arm64
            - endpoint: tcp://linuxone:1234
              platforms: linux/s390x
        env:
          BUILDER_NODE_0_AUTH_TLS_CACERT: ${{ secrets.ONEPROVIDER_CA }}
          BUILDER_NODE_0_AUTH_TLS_CERT: ${{ secrets.ONEPROVIDER_CERT }}
          BUILDER_NODE_0_AUTH_TLS_KEY: ${{ secrets.ONEPROVIDER_KEY }}
          BUILDER_NODE_1_AUTH_TLS_CACERT: ${{ secrets.GRAVITON2_CA }}
          BUILDER_NODE_1_AUTH_TLS_CERT: ${{ secrets.GRAVITON2_CERT }}
          BUILDER_NODE_1_AUTH_TLS_KEY: ${{ secrets.GRAVITON2_KEY }}
          BUILDER_NODE_2_AUTH_TLS_CACERT: ${{ secrets.LINUXONE_CA }}
          BUILDER_NODE_2_AUTH_TLS_CERT: ${{ secrets.LINUXONE_CERT }}
          BUILDER_NODE_2_AUTH_TLS_KEY: ${{ secrets.LINUXONE_KEY }}
```

## Authentication for remote builders

The following examples show how to handle authentication for remote builders,
using SSH or TLS.

### SSH authentication

To be able to connect to an SSH endpoint using the
[docker-containerdriver](https://docs.docker.com/build/builders/drivers/docker-container/),
you have to set up the SSH private key and configuration on the GitHub Runner:

```yaml
name: ci

on:
  push:

jobs:
  buildx:
    runs-on: ubuntu-latest
    steps:
      - name: Set up SSH
        uses: MrSquaare/ssh-setup-action@2d028b70b5e397cf8314c6eaea229a6c3e34977a # v3.1.0
        with:
          host: graviton2
          private-key: ${{ secrets.SSH_PRIVATE_KEY }}
          private-key-name: aws_graviton2

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
        with:
          endpoint: ssh://me@graviton2
```

### TLS authentication

You can also
[set up a remote BuildKit instance](https://docs.docker.com/build/builders/drivers/remote/#example-remote-buildkit-in-docker-container)
using the remote driver. To ease the integration in your workflow, you can use
an environment variables that sets up authentication using the BuildKit client
certificates for the `tcp://`:

- `BUILDER_NODE_<idx>_AUTH_TLS_CACERT`
- `BUILDER_NODE_<idx>_AUTH_TLS_CERT`
- `BUILDER_NODE_<idx>_AUTH_TLS_KEY`

The `<idx>` placeholder is the position of the node in the list of nodes.

```yaml
name: ci

on:
  push:

jobs:
  buildx:
    runs-on: ubuntu-latest
    steps:
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
        with:
          driver: remote
          endpoint: tcp://graviton2:1234
        env:
          BUILDER_NODE_0_AUTH_TLS_CACERT: ${{ secrets.GRAVITON2_CA }}
          BUILDER_NODE_0_AUTH_TLS_CERT: ${{ secrets.GRAVITON2_CERT }}
          BUILDER_NODE_0_AUTH_TLS_KEY: ${{ secrets.GRAVITON2_KEY }}
```

## Standalone mode

If you don't have the Docker CLI installed on the GitHub Runner, the Buildx
binary gets invoked directly, instead of calling it as a Docker CLI plugin. This
can be useful if you want to use the `kubernetes` driver in your self-hosted
runner:

```yaml
name: ci

on:
  push:

jobs:
  buildx:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
        with:
          driver: kubernetes

      - name: Build
        run: |
          buildx build .
```

## Isolated builders

The following example shows how you can select different builders for different
jobs.

An example scenario where this might be useful is when you are using a monorepo,
and you want to pinpoint different packages to specific builders. For example,
some packages may be particularly resource-intensive to build and require more
compute. Or they require a builder equipped with a particular capability or
hardware.

For more information about remote builder, see
[remotedriver](https://docs.docker.com/build/builders/drivers/remote/)
and the [append builder nodes example](#append-additional-nodes-to-the-builder).

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Set up builder1
        uses: docker/setup-buildx-action@v3
        id: builder1

      - name: Set up builder2
        uses: docker/setup-buildx-action@v3
        id: builder2

      - name: Build against builder1
        uses: docker/build-push-action@v6
        with:
          builder: ${{ steps.builder1.outputs.name }}
          target: mytarget1

      - name: Build against builder2
        uses: docker/build-push-action@v6
        with:
          builder: ${{ steps.builder2.outputs.name }}
          target: mytarget2
```

---

# Copy image between registries with GitHub Actions

> Build multi-platform images and copy them between registries with GitHub Actions

# Copy image between registries with GitHub Actions

---

[Multi-platform images](https://docs.docker.com/build/building/multi-platform/) built using Buildx can
be copied from one registry to another using the
[buildx imagetools createcommand](https://docs.docker.com/reference/cli/docker/buildx/imagetools/create/):

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

      - name: Push image to GHCR
        run: |
          docker buildx imagetools create \
            --tag ghcr.io/user/app:latest \
            --tag ghcr.io/user/app:1.0.0 \
            user/app:latest
```

---

# Export to Docker with GitHub Actions

> Load the build results to the image store with GitHub Actions

# Export to Docker with GitHub Actions

---

You may want your build result to be available in the Docker client through
`docker images` to be able to use it in another step of your workflow:

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
          load: true
          tags: myimage:latest

      - name: Inspect
        run: |
          docker image inspect myimage:latest
```

---

# Local registry with GitHub Actions

> Create and use a local OCI registry with GitHub Actions

# Local registry with GitHub Actions

---

For testing purposes you may need to create a [local registry](https://hub.docker.com/_/registry)
to push images into:

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
          driver-opts: network=host

      - name: Build and push to local registry
        uses: docker/build-push-action@v6
        with:
          push: true
          tags: localhost:5000/name/app:latest

      - name: Inspect
        run: |
          docker buildx imagetools inspect localhost:5000/name/app:latest
```

---

# Manage tags and labels with GitHub Actions

> Assign tags and labels to images automatically with GitHub Actions

# Manage tags and labels with GitHub Actions

---

If you want an "automatic" tag management and [OCI Image Format Specification](https://github.com/opencontainers/image-spec/blob/master/annotations.md)
for labels, you can do it in a dedicated setup step. The following workflow
will use the [Docker Metadata Action](https://github.com/docker/metadata-action)
to handle tags and labels based on GitHub Actions events and Git metadata:

```yaml
name: ci

on:
  schedule:
    - cron: "0 10 * * *"
  push:
    branches:
      - "**"
    tags:
      - "v*.*.*"
  pull_request:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Docker meta
        id: meta
        uses: docker/metadata-action@v5
        with:
          # list of Docker images to use as base name for tags
          images: |
            name/app
            ghcr.io/username/app
          # generate Docker tags based on the following events/attributes
          tags: |
            type=schedule
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=semver,pattern={{major}}
            type=sha

      - name: Login to Docker Hub
        if: github.event_name != 'pull_request'
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Login to GHCR
        if: github.event_name != 'pull_request'
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
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
```
