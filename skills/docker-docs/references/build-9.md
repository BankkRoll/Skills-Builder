# buildkitd.toml and more

# buildkitd.toml

# buildkitd.toml

---

The TOML file used to configure the buildkitd daemon settings has a short
list of global settings followed by a series of sections for specific areas
of daemon configuration.

The file path is `/etc/buildkit/buildkitd.toml` for rootful mode,
`~/.config/buildkit/buildkitd.toml` for rootless mode.

The following is a complete `buildkitd.toml` configuration example.
Note that some configuration options are only useful in edge cases.

```toml
# debug enables additional debug logging
debug = true
# trace enables additional trace logging (very verbose, with potential performance impacts)
trace = true
# root is where all buildkit state is stored.
root = "/var/lib/buildkit"
# insecure-entitlements allows insecure entitlements, disabled by default.
insecure-entitlements = [ "network.host", "security.insecure", "device" ]
# provenanceEnvDir is the directory where extra config is loaded that is added
# to the provenance of builds:
# slsa v0.2: invocation.environment.*
# slsa v1: buildDefinition.internalParameters.*
provenanceEnvDir = "/etc/buildkit/provenance.d"

[log]
  # log formatter: json or text
  format = "text"

[dns]
  nameservers=["1.1.1.1","8.8.8.8"]
  options=["edns0"]
  searchDomains=["example.com"]

[grpc]
  address = [ "tcp://0.0.0.0:1234" ]
  # debugAddress is address for attaching go profiles and debuggers.
  debugAddress = "0.0.0.0:6060"
  uid = 0
  gid = 0
  [grpc.tls]
    cert = "/etc/buildkit/tls.crt"
    key = "/etc/buildkit/tls.key"
    ca = "/etc/buildkit/tlsca.crt"

[otel]
  # OTEL collector trace socket path
  socketPath = "/run/buildkit/otel-grpc.sock"

[cdi]
  # Disables support of the Container Device Interface (CDI).
  disabled = true
  # List of directories to scan for CDI spec files. For more details about CDI
  # specification, please refer to https://github.com/cncf-tags/container-device-interface/blob/main/SPEC.md#cdi-json-specification
  specDirs = ["/etc/cdi", "/var/run/cdi", "/etc/buildkit/cdi"]

# config for build history API that stores information about completed build commands
[history]
  # maxAge is the maximum age of history entries to keep, in seconds.
  maxAge = 172800
  # maxEntries is the maximum number of history entries to keep.
  maxEntries = 50

[worker.oci]
  enabled = true
  # platforms is manually configure platforms, detected automatically if unset.
  platforms = [ "linux/amd64", "linux/arm64" ]
  snapshotter = "auto" # overlayfs or native, default value is "auto".
  rootless = false # see docs/rootless.md for the details on rootless mode.
  # Whether run subprocesses in main pid namespace or not, this is useful for
  # running rootless buildkit inside a container.
  noProcessSandbox = false
  # gc enables/disables garbage collection
  gc = true
  # reservedSpace is the minimum amount of disk space guaranteed to be
  # retained by this buildkit worker - any usage below this threshold will not
  # be reclaimed during garbage collection.
  # all disk space parameters can be an integer number of bytes (e.g.
  # 512000000), a string with a unit (e.g. "512MB"), or a string percentage
  # of the total disk space (e.g. "10%")
  reservedSpace = "30%"
  # maxUsedSpace is the maximum amount of disk space that may be used by
  # this buildkit worker - any usage above this threshold will be reclaimed
  # during garbage collection.
  maxUsedSpace = "60%"
  # minFreeSpace is the target amount of free disk space that the garbage
  # collector will attempt to leave - however, it will never be bought below
  # reservedSpace.
  minFreeSpace = "20GB"
  # alternate OCI worker binary name(example 'crun'), by default either
  # buildkit-runc or runc binary is used
  binary = ""
  # name of the apparmor profile that should be used to constrain build containers.
  # the profile should already be loaded (by a higher level system) before creating a worker.
  apparmor-profile = ""
  # limit the number of parallel build steps that can run at the same time
  max-parallelism = 4
  # maintain a pool of reusable CNI network namespaces to amortize the overhead
  # of allocating and releasing the namespaces
  cniPoolSize = 16

  [worker.oci.labels]
    "foo" = "bar"

  [[worker.oci.gcpolicy]]
    # reservedSpace is the minimum amount of disk space guaranteed to be
    # retained by this policy - any usage below this threshold will not be
    # reclaimed during # garbage collection.
    reservedSpace = "512MB"
    # maxUsedSpace is the maximum amount of disk space that may be used by this
    # policy - any usage above this threshold will be reclaimed during garbage
    # collection.
    maxUsedSpace = "1GB"
    # minFreeSpace is the target amount of free disk space that the garbage
    # collector will attempt to leave - however, it will never be bought below
    # reservedSpace.
    minFreeSpace = "10GB"
    # keepDuration can be an integer number of seconds (e.g. 172800), or a
    # string duration (e.g. "48h")
    keepDuration = "48h"
    filters = [ "type==source.local", "type==exec.cachemount", "type==source.git.checkout"]
  [[worker.oci.gcpolicy]]
    all = true
    reservedSpace = 1024000000

[worker.containerd]
  address = "/run/containerd/containerd.sock"
  enabled = true
  platforms = [ "linux/amd64", "linux/arm64" ]
  namespace = "buildkit"

  # gc enables/disables garbage collection
  gc = true
  # reservedSpace is the minimum amount of disk space guaranteed to be
  # retained by this buildkit worker - any usage below this threshold will not
  # be reclaimed during garbage collection.
  # all disk space parameters can be an integer number of bytes (e.g.
  # 512000000), a string with a unit (e.g. "512MB"), or a string percentage
  # of the total disk space (e.g. "10%")
  reservedSpace = "30%"
  # maxUsedSpace is the maximum amount of disk space that may be used by
  # this buildkit worker - any usage above this threshold will be reclaimed
  # during garbage collection.
  maxUsedSpace = "60%"
  # minFreeSpace is the target amount of free disk space that the garbage
  # collector will attempt to leave - however, it will never be bought below
  # reservedSpace.
  minFreeSpace = "20GB"
  # limit the number of parallel build steps that can run at the same time
  max-parallelism = 4
  # maintain a pool of reusable CNI network namespaces to amortize the overhead
  # of allocating and releasing the namespaces
  cniPoolSize = 16
  # defaultCgroupParent sets the parent cgroup of all containers.
  defaultCgroupParent = "buildkit"

  [worker.containerd.labels]
    "foo" = "bar"

  # configure the containerd runtime
  [worker.containerd.runtime]
    name = "io.containerd.runc.v2"
    path = "/path/to/containerd/runc/shim"
    options = { BinaryName = "runc" }

  [[worker.containerd.gcpolicy]]
    reservedSpace = 512000000
    keepDuration = 172800
    filters = [ "type==source.local", "type==exec.cachemount", "type==source.git.checkout"]
  [[worker.containerd.gcpolicy]]
    all = true
    reservedSpace = 1024000000

# registry configures a new Docker register used for cache import or output.
[registry."docker.io"]
  # mirror configuration to handle path in case a mirror registry requires a /project path rather than just a host:port
  mirrors = ["yourmirror.local:5000", "core.harbor.domain/proxy.docker.io"]
  # Use plain HTTP to connect to the mirrors.
  http = true
  # Use HTTPS with self-signed certificates. Do not enable this together with `http`.
  insecure = true
  # If you use token auth with self-signed certificates,
  # then buildctl also needs to trust the token provider CA (for example, certificates that are configured for registry)
  # because buildctl pulls tokens directly without daemon process
  ca=["/etc/config/myca.pem"]
  [[registry."docker.io".keypair]]
    key="/etc/config/key.pem"
    cert="/etc/config/cert.pem"

# optionally mirror configuration can be done by defining it as a registry.
[registry."yourmirror.local:5000"]
  http = true

# Frontend control
[frontend."dockerfile.v0"]
  enabled = true

[frontend."gateway.v0"]
  enabled = true
  # If allowedRepositories is empty, all gateway sources are allowed.
  # Otherwise, only the listed repositories are allowed as a gateway source.
  #
  # NOTE: Only the repository name (without tag) is compared.
  #
  # Example:
  # allowedRepositories = [ "docker-registry.wikimedia.org/repos/releng/blubber/buildkit" ]
  allowedRepositories = []

[system]
  # how often buildkit scans for changes in the supported emulated platforms
  platformsCacheMaxAge = "1h"

# optional signed cache configuration for GitHub Actions backend
[ghacache.sign]
# command that signs the payload in stdin and outputs the signature to stdout. Normally you want cosign to produce the signature bytes.
cmd = ""
[ghacache.verify]
required = false
[ghacache.verify.policy]
timestampThreshold = 1
tlogThreshold = 1
# cetificate properties that need to match. Simple wildcards (*) are supported.
certificateIssuer = ""
subjectAlternativeName = ""
buildSignerURI = ""
```

---

# BuildKit

> Introduction and overview of BuildKit

# BuildKit

   Table of contents

---

## Overview

[BuildKit](https://github.com/moby/buildkit)
is an improved backend to replace the legacy builder. BuildKit is the default builder
for users on Docker Desktop, and Docker Engine as of version 23.0.

BuildKit provides new functionality and improves your builds' performance.
It also introduces support for handling more complex scenarios:

- Detect and skip executing unused build stages
- Parallelize building independent build stages
- Incrementally transfer only the changed files in your
  [build context](https://docs.docker.com/build/concepts/context/) between builds
- Detect and skip transferring unused files in your
  [build context](https://docs.docker.com/build/concepts/context/)
- Use [Dockerfile frontend](https://docs.docker.com/build/buildkit/frontend/) implementations with many
  new features
- Avoid side effects with rest of the API (intermediate images and containers)
- Prioritize your build cache for automatic pruning

Apart from many new features, the main areas BuildKit improves on the current
experience are performance, storage management, and extensibility. From the
performance side, a significant update is a new fully concurrent build graph
solver. It can run build steps in parallel when possible and optimize out
commands that don't have an impact on the final result.
The access to the local source files has also been optimized. By tracking
only the updates made to these
files between repeated build invocations, there is no need to wait for local
files to be read or uploaded before the work can begin.

## LLB

At the core of BuildKit is a
[Low-Level Build (LLB)](https://github.com/moby/buildkit#exploring-llb) definition format. LLB is an intermediate binary format
that allows developers to extend BuildKit. LLB defines a content-addressable
dependency graph that can be used to put together complex build
definitions. It also supports features not exposed in Dockerfiles, like direct
data mounting and nested invocation.

![image](https://docs.docker.com/build/images/buildkit-dag.svg)

Everything about execution and caching of your builds is defined in LLB. The
caching model is entirely rewritten compared to the legacy builder. Rather than
using heuristics to compare images, LLB directly tracks the checksums of build
graphs and content mounted to specific operations. This makes it much faster,
more precise, and portable. The build cache can even be exported to a registry,
where it can be pulled on-demand by subsequent invocations on any host.

LLB can be generated directly using a
[golang client package](https://pkg.go.dev/github.com/moby/buildkit/client/llb) that allows defining the relationships between your
build operations using Go language primitives. This gives you full power to run
anything you can imagine, but will probably not be how most people will define
their builds. Instead, most users would use a frontend component, or LLB nested
invocation, to run a prepared set of build steps.

## Frontend

A frontend is a component that takes a human-readable build format and converts
it to LLB so BuildKit can execute it. Frontends can be distributed as images,
and the user can target a specific version of a frontend that is guaranteed to
work for the features used by their definition.

For example, to build a
[Dockerfile](https://docs.docker.com/reference/dockerfile/) with
BuildKit, you would
[use an external Dockerfile frontend](https://docs.docker.com/build/buildkit/frontend/).

## Getting started

BuildKit is the default builder for users on Docker Desktop and Docker Engine
v23.0 and later.

If you have installed Docker Desktop, you don't need to enable BuildKit. If you
are running a version of Docker Engine version earlier than 23.0, you can enable
BuildKit either by setting an environment variable, or by making BuildKit the
default setting in the daemon configuration.

To set the BuildKit environment variable when running the `docker build`
command, run:

```console
$ DOCKER_BUILDKIT=1 docker build .
```

> Note
>
> Buildx always uses BuildKit.

To use Docker BuildKit by default, edit the Docker daemon configuration in
`/etc/docker/daemon.json` as follows, and restart the daemon.

```json
{
  "features": {
    "buildkit": true
  }
}
```

If the `/etc/docker/daemon.json` file doesn't exist, create new file called
`daemon.json` and then add the following to the file. And restart the Docker
daemon.

## BuildKit on Windows

> Warning
>
> BuildKit only fully supports building Linux containers. Windows container
> support is experimental.

BuildKit has experimental support for Windows containers (WCOW) as of version 0.13.
This section walks you through the steps for trying it out.
To share feedback, [open an issue in the repository](https://github.com/moby/buildkit/issues/new), especially `buildkitd.exe`.

### Known limitations

For information about open bugs and limitations related to BuildKit on Windows,
see [GitHub issues](https://github.com/moby/buildkit/issues?q=is%3Aissue%20state%3Aopen%20label%3Aarea%2Fwindows-wcow).

### Prerequisites

- Architecture: `amd64`, `arm64` (binaries available but not officially tested yet).
- Supported OS: Windows Server 2019, Windows Server 2022, Windows 11.
- Base images: `ServerCore:ltsc2019`, `ServerCore:ltsc2022`, `NanoServer:ltsc2022`.
  See the [compatibility map here](https://learn.microsoft.com/en-us/virtualization/windowscontainers/deploy-containers/version-compatibility?tabs=windows-server-2019%2Cwindows-11#windows-server-host-os-compatibility).
- Docker Desktop version 4.29 or later

### Steps

> Note
>
> The following commands require administrator (elevated) privileges in a PowerShell terminal.

1. Enable the **Hyper-V** and **Containers** Windows features.
  ```console
  > Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V, Containers -All
  ```
  If you see `RestartNeeded` as `True`, restart your machine and re-open a PowerShell terminal as an administrator.
  Otherwise, continue with the next step.
2. Switch to Windows containers in Docker Desktop.
  Select the Docker icon in the taskbar, and then **Switch to Windows containers...**.
3. Install containerd version 1.7.7 or later following the [setup instructions](https://github.com/containerd/containerd/blob/main/docs/getting-started.md#installing-containerd-on-windows).
4. Download and extract the latest BuildKit release.
  ```powershell
  $version = "v0.22.0" # specify the release version, v0.13+
  $arch = "amd64" # arm64 binary available too
  curl.exe -LO https://github.com/moby/buildkit/releases/download/$version/buildkit-$version.windows-$arch.tar.gz
  # there could be another `.\bin` directory from containerd instructions
  # you can move those
  mv bin bin2
  tar.exe xvf .\buildkit-$version.windows-$arch.tar.gz
  ## x bin/
  ## x bin/buildctl.exe
  ## x bin/buildkitd.exe
  ```
5. Install BuildKit binaries on `PATH`.
  ```powershell
  # after the binaries are extracted in the bin directory
  # move them to an appropriate path in your $Env:PATH directories or:
  Copy-Item -Path ".\bin" -Destination "$Env:ProgramFiles\buildkit" -Recurse -Force
  # add `buildkitd.exe` and `buildctl.exe` binaries in the $Env:PATH
  $Path = [Environment]::GetEnvironmentVariable("PATH", "Machine") + `
      [IO.Path]::PathSeparator + "$Env:ProgramFiles\buildkit"
  [Environment]::SetEnvironmentVariable( "Path", $Path, "Machine")
  $Env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + `
      [System.Environment]::GetEnvironmentVariable("Path","User")
  ```
6. Start the BuildKit daemon.
  ```console
  > buildkitd.exe
  ```
  > Note
  >
  > If you are running a *dockerd-managed* `containerd` process, use that instead, by supplying the address:
  > `buildkitd.exe --containerd-worker-addr "npipe:////./pipe/docker-containerd"`
7. In another terminal with administrator privileges, create a remote builder that uses the local BuildKit daemon.
  > Note
  >
  > This requires Docker Desktop version 4.29 or later.
  ```console
  > docker buildx create --name buildkit-exp --use --driver=remote npipe:////./pipe/buildkitd
  buildkit-exp
  ```
8. Verify the builder connection by running `docker buildx inspect`.
  ```console
  > docker buildx inspect
  ```
  The output should indicate that the builder platform is Windows,
  and that the endpoint of the builder is a named pipe.
  ```text
  Name:          buildkit-exp
   Driver:        remote
   Last Activity: 2024-04-15 17:51:58 +0000 UTC
   Nodes:
   Name:             buildkit-exp0
   Endpoint:         npipe:////./pipe/buildkitd
   Status:           running
   BuildKit version: v0.13.1
   Platforms:        windows/amd64
  ...
  ```
9. Create a Dockerfile and build a `hello-buildkit` image.
  ```console
  > mkdir sample_dockerfile
  > cd sample_dockerfile
  > Set-Content Dockerfile @"
  FROM mcr.microsoft.com/windows/nanoserver:ltsc2022
  USER ContainerAdministrator
  COPY hello.txt C:/
  RUN echo "Goodbye!" >> hello.txt
  CMD ["cmd", "/C", "type C:\\hello.txt"]
  "@
  Set-Content hello.txt @"
  Hello from BuildKit!
  This message shows that your installation appears to be working correctly.
  "@
  ```
10. Build and push the image to a registry.
  ```console
  > docker buildx build --push -t <username>/hello-buildkit .
  ```
11. After pushing to the registry, run the image with `docker run`.
  ```console
  > docker run <username>/hello-buildkit
  ```

---

# Azure Blob Storage cache

> Manage build cache with Azure blob storage

# Azure Blob Storage cache

   Table of contents

---

Availability: Experimental

The `azblob` cache store uploads your resulting build cache to
[Azure's blob storage service](https://azure.microsoft.com/en-us/services/storage/blobs/).

This cache storage backend is not supported with the default `docker` driver.
To use this feature, create a new builder using a different driver. See
[Build drivers](https://docs.docker.com/build/builders/drivers/) for more information.

## Synopsis

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=azblob,name=<cache-image>[,parameters...] \
  --cache-from type=azblob,name=<cache-image>[,parameters...] .
```

The following table describes the available CSV parameters that you can pass to
`--cache-to` and `--cache-from`.

| Name | Option | Type | Default | Description |
| --- | --- | --- | --- | --- |
| name | cache-to,cache-from | String |  | Required. The name of the cache image. |
| account_url | cache-to,cache-from | String |  | Base URL of the storage account. |
| secret_access_key | cache-to,cache-from | String |  | Blob storage account key, seeauthentication. |
| mode | cache-to | min,max | min | Cache layers to export, seecache mode. |
| ignore-error | cache-to | Boolean | false | Ignore errors caused by failed cache exports. |

## Authentication

The `secret_access_key`, if left unspecified, is read from environment variables
on the BuildKit server following the scheme for the
[Azure Go SDK](https://docs.microsoft.com/en-us/azure/developer/go/azure-sdk-authentication).
The environment variables are read from the server, not the Buildx client.

## Further reading

For an introduction to caching see [Docker build cache](https://docs.docker.com/build/cache/).

For more information on the `azblob` cache backend, see the
[BuildKit README](https://github.com/moby/buildkit#azure-blob-storage-cache-experimental).

---

# GitHub Actions cache

> Use the GitHub Actions cache to manage your build cache in CI

# GitHub Actions cache

   Table of contents

---

Availability: Experimental

The GitHub Actions cache utilizes the
[GitHub-provided Action's cache](https://github.com/actions/cache) or other
cache services supporting the GitHub Actions cache protocol. This is the
recommended cache to use inside your GitHub Actions workflows, as long as your
use case falls within the
[size and usage limits set by GitHub](https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows#usage-limits-and-eviction-policy).

This cache storage backend is not supported with the default `docker` driver.
To use this feature, create a new builder using a different driver. See
[Build drivers](https://docs.docker.com/build/builders/drivers/) for more information.

## Synopsis

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=gha[,parameters...] \
  --cache-from type=gha[,parameters...] .
```

The following table describes the available CSV parameters that you can pass to
`--cache-to` and `--cache-from`.

| Name | Option | Type | Default | Description |
| --- | --- | --- | --- | --- |
| url | cache-to,cache-from | String | $ACTIONS_CACHE_URLor$ACTIONS_RESULTS_URL | Cache server URL, seeauthentication. Ignored whenversion=2. |
| url_v2 | cache-to,cache-from | String | $ACTIONS_RESULTS_URL | Cache v2 server URL, seeauthentication. |
| token | cache-to,cache-from | String | $ACTIONS_RUNTIME_TOKEN | Access token, seeauthentication. |
| scope | cache-to,cache-from | String | buildkit | Which scope cache object belongs to, seescope |
| mode | cache-to | min,max | min | Cache layers to export, seecache mode. |
| ignore-error | cache-to | Boolean | false | Ignore errors caused by failed cache exports. |
| timeout | cache-to,cache-from | String | 10m | Max duration for importing or exporting cache before it's timed out. |
| repository | cache-to | String |  | GitHub repository used for cache storage. |
| ghtoken | cache-to | String |  | GitHub token required for accessing the GitHub API. |
| version | cache-to,cache-from | String | 1unless$ACTIONS_CACHE_SERVICE_V2is set, then2 | Selects GitHub Actions cache version, seeversion |

## Authentication

If the `url`, `url_v2` or `token` parameters are left unspecified, the `gha`
cache backend will fall back to using environment variables. If you invoke the
`docker buildx` command manually from an inline step, then the variables must
be manually exposed. Consider using the
[crazy-max/ghaction-github-runtime](https://github.com/crazy-max/ghaction-github-runtime),
GitHub Action as a helper for exposing the variables.

## Scope

Scope is a key used to identify the cache object. By default, it is set to
`buildkit`. If you build multiple images, each build will overwrite the cache
of the previous, leaving only the final cache.

To preserve the cache for multiple builds, you can specify this scope attribute
with a specific name. In the following example, the cache is set to the image
name, to ensure each image gets its own cache:

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=gha,url=...,token=...,scope=image \
  --cache-from type=gha,url=...,token=...,scope=image .
$ docker buildx build --push -t <registry>/<image2> \
  --cache-to type=gha,url=...,token=...,scope=image2 \
  --cache-from type=gha,url=...,token=...,scope=image2 .
```

GitHub's [cache access restrictions](https://docs.github.com/en/actions/advanced-guides/caching-dependencies-to-speed-up-workflows#restrictions-for-accessing-a-cache),
still apply. Only the cache for the current branch, the base branch and the
default branch is accessible by a workflow.

## Version

If you don’t set `version` explicitly, the default is v1. However, if the environment variable `$ACTIONS_CACHE_SERVICE_V2` is set to a value interpreted as `true` ( `1`, `true`, `yes`), then v2 is used automatically.

Only one URL is relevant at a time:

- With v1, use `url` (defaults to `$ACTIONS_CACHE_URL`).
- With v2, use `url_v2` (defaults to `$ACTIONS_RESULTS_URL`).

### Usingdocker/build-push-action

When using the
[docker/build-push-action](https://github.com/docker/build-push-action), the
`url` and `token` parameters are automatically populated. No need to manually
specify them, or include any additional workarounds.

For example:

```yaml
- name: Build and push
  uses: docker/build-push-action@v6
  with:
    context: .
    push: true
    tags: "<registry>/<image>:latest"
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

## Avoid GitHub Actions cache API throttling

GitHub's [usage limits and eviction policy](https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows#usage-limits-and-eviction-policy)
causes stale cache entries to be removed after a certain period of time. By
default, the `gha` cache backend uses the GitHub Actions cache API to check the
status of cache entries.

The GitHub Actions cache API is subject to rate limiting if you make too many
requests in a short period of time, which may happen as a result of cache
lookups during a build using the `gha` cache backend.

```text
#31 exporting to GitHub Actions Cache
#31 preparing build cache for export
#31 preparing build cache for export 600.3s done
#31 ERROR: maximum timeout reached
------
 > exporting to GitHub Actions Cache:
------
ERROR: failed to solve: maximum timeout reached
make: *** [Makefile:35: release] Error 1
Error: Process completed with exit code 2.
```

To mitigate this issue, you can supply a GitHub token to BuildKit. This lets
BuildKit utilize the standard GitHub API for checking cache keys, thereby
reducing the number of requests made to the cache API.

To provide a GitHub token, you can use the `ghtoken` parameter, and a
`repository` parameter to specify the repository to use for cache storage. The
`ghtoken` parameter is a GitHub token with the `repo` scope, which is required
to access the GitHub Actions cache API.

The `ghtoken` parameter is automatically set to the value of
`secrets.GITHUB_TOKEN` when you build with the `docker/build-push-action`
action. You can also set the `ghtoken` parameter manually using the
`github-token` input, as shown in the following example:

```yaml
- name: Build and push
  uses: docker/build-push-action@v6
  with:
    context: .
    push: true
    tags: "<registry>/<image>:latest"
    cache-from: type=gha
    cache-to: type=gha,mode=max
    github-token: ${{ secrets.MY_CUSTOM_TOKEN }}
```

## Further reading

For an introduction to caching see [Docker build cache](https://docs.docker.com/build/cache/).

For more information on the `gha` cache backend, see the
[BuildKit README](https://github.com/moby/buildkit#github-actions-cache-experimental).

For more information about using GitHub Actions with Docker, see
[Introduction to GitHub Actions](https://docs.docker.com/build/ci/github-actions/)

---

# Inline cache

> Embed the build cache into the image

# Inline cache

   Table of contents

---

The `inline` cache storage backend is the simplest way to get an external cache
and is easy to get started using if you're already building and pushing an
image.

The downside of inline cache is that it doesn't scale with multi-stage builds
as well as the other drivers do. It also doesn't offer separation between your
output artifacts and your cache output. This means that if you're using a
particularly complex build flow, or not exporting your images directly to a
registry, then you may want to consider the [registry](https://docs.docker.com/build/cache/backends/registry/) cache.

## Synopsis

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=inline \
  --cache-from type=registry,ref=<registry>/<image> .
```

No additional parameters are supported for the `inline` cache.

To export cache using `inline` storage, pass `type=inline` to the `--cache-to`
option:

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=inline .
```

Alternatively, you can also export inline cache by setting the build argument
`BUILDKIT_INLINE_CACHE=1`, instead of using the `--cache-to` flag:

```console
$ docker buildx build --push -t <registry>/<image> \
  --build-arg BUILDKIT_INLINE_CACHE=1 .
```

To import the resulting cache on a future build, pass `type=registry` to
`--cache-from` which lets you extract the cache from inside a Docker image in
the specified registry:

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-from type=registry,ref=<registry>/<image> .
```

## Further reading

For an introduction to caching see [Docker build cache](https://docs.docker.com/build/cache/).

For more information on the `inline` cache backend, see the
[BuildKit README](https://github.com/moby/buildkit#inline-push-image-and-cache-together).

---

# Local cache

> Manage build cache with Amazon S3 buckets

# Local cache

   Table of contents

---

The `local` cache store is a simple cache option that stores your cache as files
in a directory on your filesystem, using an
[OCI image layout](https://github.com/opencontainers/image-spec/blob/main/image-layout.md)
for the underlying directory structure. Local cache is a good choice if you're
just testing, or if you want the flexibility to self-manage a shared storage
solution.

## Synopsis

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=local,dest=path/to/local/dir[,parameters...] \
  --cache-from type=local,src=path/to/local/dir .
```

The following table describes the available CSV parameters that you can pass to
`--cache-to` and `--cache-from`.

| Name | Option | Type | Default | Description |
| --- | --- | --- | --- | --- |
| src | cache-from | String |  | Path of the local directory where cache gets imported from. |
| digest | cache-from | String |  | Digest of manifest to import, seecache versioning. |
| dest | cache-to | String |  | Path of the local directory where cache gets exported to. |
| mode | cache-to | min,max | min | Cache layers to export, seecache mode. |
| oci-mediatypes | cache-to | true,false | true | Use OCI media types in exported manifests, seeOCI media types. |
| image-manifest | cache-to | true,false | true | When using OCI media types, generate an image manifest instead of an image index for the cache image, seeOCI media types. |
| compression | cache-to | gzip,estargz,zstd | gzip | Compression type, seecache compression. |
| compression-level | cache-to | 0..22 |  | Compression level, seecache compression. |
| force-compression | cache-to | true,false | false | Forcibly apply compression, seecache compression. |
| ignore-error | cache-to | Boolean | false | Ignore errors caused by failed cache exports. |

If the `src` cache doesn't exist, then the cache import step will fail, but the
build continues.

## Cache versioning

This section describes how versioning works for caches on a local filesystem,
and how you can use the `digest` parameter to use older versions of cache.

If you inspect the cache directory manually, you can see the resulting OCI image
layout:

```console
$ ls cache
blobs  index.json  ingest
$ cat cache/index.json | jq
{
  "schemaVersion": 2,
  "manifests": [
    {
      "mediaType": "application/vnd.oci.image.index.v1+json",
      "digest": "sha256:6982c70595cb91769f61cd1e064cf5f41d5357387bab6b18c0164c5f98c1f707",
      "size": 1560,
      "annotations": {
        "org.opencontainers.image.ref.name": "latest"
      }
    }
  ]
}
```

Like other cache types, local cache gets replaced on export, by replacing the
contents of the `index.json` file. However, previous caches will still be
available in the `blobs` directory. These old caches are addressable by digest,
and kept indefinitely. Therefore, the size of the local cache will continue to
grow (see [moby/buildkit#1896](https://github.com/moby/buildkit/issues/1896)
for more information).

When importing cache using `--cache-from`, you can specify the `digest` parameter
to force loading an older version of the cache, for example:

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=local,dest=path/to/local/dir \
  --cache-from type=local,ref=path/to/local/dir,digest=sha256:6982c70595cb91769f61cd1e064cf5f41d5357387bab6b18c0164c5f98c1f707 .
```

## Further reading

For an introduction to caching see [Docker build cache](https://docs.docker.com/build/cache/).

For more information on the `local` cache backend, see the
[BuildKit README](https://github.com/moby/buildkit#local-directory-1).

---

# Registry cache

> Manage build cache with an OCI registry

# Registry cache

   Table of contents

---

The `registry` cache storage can be thought of as an extension to the `inline`
cache. Unlike the `inline` cache, the `registry` cache is entirely separate from
the image, which allows for more flexible usage - `registry`-backed cache can do
everything that the inline cache can do, and more:

- Allows for separating the cache and resulting image artifacts so that you can
  distribute your final image without the cache inside.
- It can efficiently cache multi-stage builds in `max` mode, instead of only the
  final stage.
- It works with other exporters for more flexibility, instead of only the
  `image` exporter.

This cache storage backend is not supported with the default `docker` driver.
To use this feature, create a new builder using a different driver. See
[Build drivers](https://docs.docker.com/build/builders/drivers/) for more information.

## Synopsis

Unlike the simpler `inline` cache, the `registry` cache supports several
configuration parameters:

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=registry,ref=<registry>/<cache-image>[,parameters...] \
  --cache-from type=registry,ref=<registry>/<cache-image> .
```

The following table describes the available CSV parameters that you can pass to
`--cache-to` and `--cache-from`.

| Name | Option | Type | Default | Description |
| --- | --- | --- | --- | --- |
| ref | cache-to,cache-from | String |  | Full name of the cache image to import. |
| mode | cache-to | min,max | min | Cache layers to export, seecache mode. |
| oci-mediatypes | cache-to | true,false | true | Use OCI media types in exported manifests, seeOCI media types. |
| image-manifest | cache-to | true,false | true | When using OCI media types, generate an image manifest instead of an image index for the cache image, seeOCI media types. |
| compression | cache-to | gzip,estargz,zstd | gzip | Compression type, seecache compression. |
| compression-level | cache-to | 0..22 |  | Compression level, seecache compression. |
| force-compression | cache-to | true,false | false | Forcibly apply compression, seecache compression. |
| ignore-error | cache-to | Boolean | false | Ignore errors caused by failed cache exports. |

You can choose any valid value for `ref`, as long as it's not the same as the
target location that you push your image to. You might choose different tags
(e.g. `foo/bar:latest` and `foo/bar:build-cache`), separate image names (e.g.
`foo/bar` and `foo/bar-cache`), or even different repositories (e.g.
`docker.io/foo/bar` and `ghcr.io/foo/bar`). It's up to you to decide the
strategy that you want to use for separating your image from your cache images.

If the `--cache-from` target doesn't exist, then the cache import step will
fail, but the build continues.

## Further reading

For an introduction to caching see [Docker build cache](https://docs.docker.com/build/cache/).

For more information on the `registry` cache backend, see the
[BuildKit README](https://github.com/moby/buildkit#registry-push-image-and-cache-separately).

---

# Amazon S3 cache

> Manage build cache with Amazon S3 buckets

# Amazon S3 cache

   Table of contents

---

Availability: Experimental

The `s3` cache storage uploads your resulting build cache to
[Amazon S3 file storage service](https://aws.amazon.com/s3/)
or other S3-compatible services, such as [MinIO](https://min.io/).

This cache storage backend is not supported with the default `docker` driver.
To use this feature, create a new builder using a different driver. See
[Build drivers](https://docs.docker.com/build/builders/drivers/) for more information.

## Synopsis

```console
$ docker buildx build --push -t <user>/<image> \
  --cache-to type=s3,region=<region>,bucket=<bucket>,name=<cache-image>[,parameters...] \
  --cache-from type=s3,region=<region>,bucket=<bucket>,name=<cache-image> .
```

The following table describes the available CSV parameters that you can pass to
`--cache-to` and `--cache-from`.

| Name | Option | Type | Default | Description |
| --- | --- | --- | --- | --- |
| region | cache-to,cache-from | String |  | Required. Geographic location. |
| bucket | cache-to,cache-from | String |  | Required. Name of the S3 bucket. |
| name | cache-to,cache-from | String | buildkit | Name of the cache image. |
| endpoint_url | cache-to,cache-from | String |  | Endpoint of the S3 bucket. |
| prefix | cache-to,cache-from | String |  | Prefix to prepend to all filenames. |
| blobs_prefix | cache-to,cache-from | String | blobs/ | Prefix to prepend to blob filenames. |
| upload_parallelism | cache-to | Integer | 4 | Number of parallel layer uploads. |
| touch_refresh | cache-to | Time | 24h | Interval for updating the timestamp of unchanged cache layers. |
| manifests_prefix | cache-to,cache-from | String | manifests/ | Prefix to prepend to manifest filenames. |
| use_path_style | cache-to,cache-from | Boolean | false | Whentrue, usesbucketin the URL instead of hostname. |
| access_key_id | cache-to,cache-from | String |  | Seeauthentication. |
| secret_access_key | cache-to,cache-from | String |  | Seeauthentication. |
| session_token | cache-to,cache-from | String |  | Seeauthentication. |
| mode | cache-to | min,max | min | Cache layers to export, seecache mode. |
| ignore-error | cache-to | Boolean | false | Ignore errors caused by failed cache exports. |

## Authentication

Buildx can reuse existing AWS credentials, configured either using a
credentials file or environment variables, for pushing and pulling cache to S3.
Alternatively, you can use the `access_key_id`, `secret_access_key`, and
`session_token` attributes to specify credentials directly on the CLI.

Refer to [AWS Go SDK, Specifying Credentials](https://docs.aws.amazon.com/sdk-for-go/v2/developer-guide/configure-gosdk.html#specifying-credentials) for details about
authentication using environment variables and credentials file.

## Further reading

For an introduction to caching see [Docker build cache](https://docs.docker.com/build/cache/).

For more information on the `s3` cache backend, see the
[BuildKit README](https://github.com/moby/buildkit#s3-cache-experimental).
