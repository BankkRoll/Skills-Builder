# Cache storage backends and more

# Cache storage backends

> Cache backends let you manage your build cache externally. External cache is useful to create a shared cache that can help speed up inner loop and CI builds.

# Cache storage backends

   Table of contents

---

To ensure fast builds, BuildKit automatically caches the build result in its own
internal cache. Additionally, BuildKit also supports exporting build cache to an
external location, making it possible to import in future builds.

An external cache becomes almost essential in CI/CD build environments. Such
environments usually have little-to-no persistence between runs, but it's still
important to keep the runtime of image builds as low as possible.

The default `docker` driver supports the `inline`, `local`, `registry`, and
`gha` cache backends, but only if you have enabled the
[containerd image store](https://docs.docker.com/desktop/features/containerd/).
Other cache backends require you to select a different
[driver](https://docs.docker.com/build/builders/drivers/).

> Warning
>
> If you use secrets or credentials inside your build process, ensure you
> manipulate them using the dedicated
> [--secretoption](https://docs.docker.com/reference/cli/docker/buildx/build/#secret).
> Manually managing secrets using `COPY` or `ARG` could result in leaked
> credentials.

## Backends

Buildx supports the following cache storage backends:

- `inline`: embeds the build cache into the image.
  The inline cache gets pushed to the same location as the main output result.
  This only works with the [imageexporter](https://docs.docker.com/build/exporters/image-registry/).
- `registry`: embeds the build cache into a separate image, and pushes to a
  dedicated location separate from the main output.
- `local`: writes the build cache to a local directory on the filesystem.
- `gha`: uploads the build cache to
  [GitHub Actions cache](https://docs.github.com/en/rest/actions/cache) (beta).
- `s3`: uploads the build cache to an
  [AWS S3 bucket](https://aws.amazon.com/s3/) (unreleased).
- `azblob`: uploads the build cache to
  [Azure Blob Storage](https://azure.microsoft.com/en-us/services/storage/blobs/)
  (unreleased).

## Command syntax

To use any of the cache backends, you first need to specify it on build with the
[--cache-tooption](https://docs.docker.com/reference/cli/docker/buildx/build/#cache-to)
to export the cache to your storage backend of choice. Then, use the
[--cache-fromoption](https://docs.docker.com/reference/cli/docker/buildx/build/#cache-from)
to import the cache from the storage backend into the current build. Unlike the
local BuildKit cache (which is always enabled), all of the cache storage
backends must be explicitly exported to, and explicitly imported from.

Example `buildx` command using the `registry` backend, using import and export
cache:

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=registry,ref=<registry>/<cache-image>[,parameters...] \
  --cache-from type=registry,ref=<registry>/<cache-image>[,parameters...] .
```

> Warning
>
> As a general rule, each cache writes to some location. No location can be
> written to twice, without overwriting the previously cached data. If you want
> to maintain multiple scoped caches (for example, a cache per Git branch), then
> ensure that you use different locations for exported cache.

## Multiple caches

BuildKit supports multiple cache exporters, allowing you to push cache to more
than one destination. You can also import from as many remote caches as you'd
like. For example, a common pattern is to use the cache of both the current
branch and the main branch. The following example shows importing cache from
multiple locations using the registry cache backend:

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=registry,ref=<registry>/<cache-image>:<branch> \
  --cache-from type=registry,ref=<registry>/<cache-image>:<branch> \
  --cache-from type=registry,ref=<registry>/<cache-image>:main .
```

## Configuration options

This section describes some configuration options available when generating
cache exports. The options described here are common for at least two or more
backend types. Additionally, the different backend types support specific
parameters as well. See the detailed page about each backend type for more
information about which configuration parameters apply.

The common parameters described here are:

- [Cache mode](#cache-mode)
- [Cache compression](#cache-compression)
- [OCI media type](#oci-media-types)

### Cache mode

When generating a cache output, the `--cache-to` argument accepts a `mode`
option for defining which layers to include in the exported cache. This is
supported by all cache backends except for the `inline` cache.

Mode can be set to either of two options: `mode=min` or `mode=max`. For example,
to build the cache with `mode=max` with the registry backend:

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=registry,ref=<registry>/<cache-image>,mode=max \
  --cache-from type=registry,ref=<registry>/<cache-image> .
```

This option is only set when exporting a cache, using `--cache-to`. When
importing a cache (`--cache-from`) the relevant parameters are automatically
detected.

In `min` cache mode (the default), only layers that are exported into the
resulting image are cached, while in `max` cache mode, all layers are cached,
even those of intermediate steps.

While `min` cache is typically smaller (which speeds up import/export times, and
reduces storage costs), `max` cache is more likely to get more cache hits.
Depending on the complexity and location of your build, you should experiment
with both parameters to find the results that work best for you.

### Cache compression

The cache compression options are the same as the
[exporter compression options](https://docs.docker.com/build/exporters/#compression). This is
supported by the `local` and `registry` cache backends.

For example, to compress the `registry` cache with `zstd` compression:

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=registry,ref=<registry>/<cache-image>,compression=zstd \
  --cache-from type=registry,ref=<registry>/<cache-image> .
```

### OCI media types

The cache OCI options are the same as the
[exporter OCI options](https://docs.docker.com/build/exporters/#oci-media-types). These are
supported by the `local` and `registry` cache backends.

For example, to export OCI media type cache, use the `oci-mediatypes` property:

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=registry,ref=<registry>/<cache-image>,oci-mediatypes=true \
  --cache-from type=registry,ref=<registry>/<cache-image> .
```

This property is only meaningful with the `--cache-to` flag. When fetching
cache, BuildKit will auto-detect the correct media types to use.

By default, the OCI media type generates an image index for the cache image.
Some OCI registries, such as Amazon ECR, don't support the image index media
type: `application/vnd.oci.image.index.v1+json`. If you export cache images to
ECR, or any other registry that doesn't support image indices, set the
`image-manifest` parameter to `true` to generate a single image manifest
instead of an image index for the cache image:

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=registry,ref=<registry>/<cache-image>,oci-mediatypes=true,image-manifest=true \
  --cache-from type=registry,ref=<registry>/<cache-image> .
```

> Note
>
> Since BuildKit v0.21, `image-manifest` is enabled by default.

---

# Build garbage collection

> Learn about garbage collection in the BuildKit daemon

# Build garbage collection

   Table of contents

---

While
[docker builder prune](https://docs.docker.com/reference/cli/docker/builder/prune/)
or
[docker buildx prune](https://docs.docker.com/reference/cli/docker/buildx/prune/)
commands run at once, Garbage Collection (GC) runs periodically and follows an
ordered list of prune policies. The BuildKit daemon clears the build cache when
the cache size becomes too big, or when the cache age expires.

For most users, the default GC behavior is sufficient and doesn't require any
intervention. Advanced users, particularly those working with large-scale
builds, self-managed builders, or constrained storage environments, might
benefit from customizing these settings to better align with their workflow
needs. The following sections explain how GC works and provide guidance on
tailoring its behavior through custom configuration.

## Garbage collection policies

GC policies define a set of rules that determine how the build cache is managed
and cleaned up. These policies include criteria for when to remove cache
entries, such as the age of the cache, the amount of space being used, and the
type of cache records to prune.

Each GC policy is evaluated in sequence, starting with the most specific
criteria, and proceeds to broader rules if previous policies do not free up
enough cache. This lets BuildKit prioritize cache entries, preserving the most
valuable cache while ensuring the system maintains performance and
availability.

For example, say you have the following GC policies:

1. Find "stale" cache records that haven't been used in the past 48 hours, and
  delete records until there's maximum 5GB of "stale" cache left.
2. If the build cache size exceeds 10GB, delete records until the total cache
  size is no more than 10GB.

The first rule is more specific, prioritizing stale cache records and setting a
lower limit for a less valuable type of cache. The second rule imposes a higher
hard limit that applies to any type of cache records. With these policies, if
you have 11GB worth of build cache, where:

- 7GB of which is "stale" cache
- 4GB is other, more valuable cache

A GC sweep would delete 5GB of stale cache as part of the 1st policy, with a
remainder of 6GB, meaning the 2nd policy does not need to clear any more cache.

The default GC policies are (approximately):

1. Remove cache that can be easily regenerated, such as build contexts from
  local directories or remote Git repositories, and cache mounts, if hasn't
  been used for more than 48 hours.
2. Remove cache that hasn't been used in a build for more than 60 days.
3. Remove unshared cache that exceeds the build cache size limit. Unshared
  cache records refers to layer blobs that are not used by other resources
  (typically, as image layers).
4. Remove any build cache that exceeds the build cache size limit.

The precise algorithm and the means of configuring the policies differ slightly
depending on what kind of builder you're using. Refer to
[Configuration](#configuration) for more details.

## Configuration

> Note
>
> If you're satisfied with the default garbage collection behavior and don't
> need to fine-tune its settings, you can skip this section. Default
> configurations work well for most use cases and require no additional setup.

Depending on the type of [build driver](https://docs.docker.com/build/builders/drivers/) you use,
you will use different configuration files to change the builder's GC settings:

- If you use the default builder for Docker Engine (the `docker` driver), use
  the [Docker daemon configuration file](#docker-daemon-configuration-file).
- If you use a custom builder, use a [BuildKit configuration file](#buildkit-configuration-file).

### Docker daemon configuration file

If you're using the default [dockerdriver](https://docs.docker.com/build/builders/drivers/docker/),
GC is configured in the
[daemon.jsonconfiguration file](https://docs.docker.com/reference/cli/dockerd/#daemon-configuration-file),
or if you use Docker Desktop, in
[Settings > Docker Engine](https://docs.docker.com/desktop/settings-and-maintenance/settings/).

The following snippet shows the default builder configuration for the `docker`
driver for Docker Desktop users:

```json
{
  "builder": {
    "gc": {
      "defaultKeepStorage": "20GB",
      "enabled": true
    }
  }
}
```

The `defaultKeepStorage` option configures the size limit of the build cache,
which influences the GC policies. The default policies for the `docker` driver
work as follows:

1. Remove ephemeral, unused build cache older than 48 hours if it exceeds 13.8%
  of `defaultKeepStorage`, or at minimum 512MB.
2. Remove unused build cache older than 60 days.
3. Remove unshared build cache that exceeds the `defaultKeepStorage` limit.
4. Remove any build cache that exceeds the `defaultKeepStorage` limit.

Given the Docker Desktop default value for `defaultKeepStorage` of 20GB, the
default GC policies resolve to:

```json
{
  "builder": {
    "gc": {
      "enabled": true,
      "policy": [
        {
          "reservedSpace": "2.764GB",
          "keepDuration": "48h",
          "filter": [
            "type=source.local,type=exec.cachemount,type=source.git.checkout"
          ]
        },
        { "reservedSpace": "20GB", "keepDuration": ["1440h"] },
        { "reservedSpace": "20GB" },
        { "reservedSpace": "20GB", "all": true }
      ]
    }
  }
}
```

The easiest way to tweak the build cache configuration for the `docker` driver
is to adjust the `defaultKeepStorage` option:

- Increase the limit if you feel like you think the GC is too aggressive.
- Decrease the limit if you need to preserve space.

#### Custom GC policies in the Docker daemon configuration file

If you need even more control, you can define your own GC policies directly.
The following example defines a more conservative GC configuration with the
following policies:

1. Remove unused cache entries older than 1440 hours, or 60 days, if build cache exceeds 50GB.
2. Remove unshared cache entries if build cache exceeds 50GB.
3. Remove any cache entries if build cache exceeds 100GB.

```json
{
  "builder": {
    "gc": {
      "enabled": true,
      "policy": [
        { "reservedSpace": "50GB", "keepDuration": ["1440h"] },
        { "reservedSpace": "50GB" },
        { "reservedSpace": "100GB", "all": true }
      ]
    }
  }
}
```

> Note
>
> In the Docker daemon configuration file, the "equals" operator in GC filters
> is denoted using a single `=`, whereas BuildKit's configuration file uses
> `==`:
>
>
>
> | daemon.json | buildkitd.toml |
> | --- | --- |
> | type=source.local | type==source.local |
> | private=true | private==true |
> | shared=true | shared==true |
>
>
>
> See
> [prune filters](https://docs.docker.com/reference/cli/docker/buildx/prune/#filter) for
> information about available GC filters. GC configuration in `daemon.json`
> supports all filters except `mutable` and `immutable`.

### BuildKit configuration file

For build drivers other than `docker`, GC is configured using a
[buildkitd.toml](https://docs.docker.com/build/buildkit/toml-configuration/) configuration file. This
file uses the following high-level configuration options that you can use to
tweak the thresholds for how much disk space BuildKit should use for cache:

| Option | Description | Default value |
| --- | --- | --- |
| reservedSpace | The minimum amount of disk space BuildKit is allowed to allocate for cache. Usage below this threshold will not be reclaimed during garbage collection. | 10% of total disk space or 10GB (whichever is lower) |
| maxUsedSpace | The maximum amount of disk space that BuildKit is allowed to use. Usage above this threshold will be reclaimed during garbage collection. | 60% of total disk space or 100GB (whichever is lower) |
| minFreeSpace | The amount of disk space that must be kept free. | 20GB |

You can set these options either as number of bytes, a unit string (for
example, `512MB`), or as a percentage of the total disk size. Changing these
options influences the default GC policies used by the BuildKit worker. With
the default thresholds, the GC policies resolve as follows:

```toml
# Global defaults
[worker.oci]
  gc = true
  reservedSpace = "10GB"
  maxUsedSpace = "100GB"
  minFreeSpace = "20%"

# Policy 1
[[worker.oci.gcpolicy]]
  filters = [ "type==source.local", "type==exec.cachemount", "type==source.git.checkout" ]
  keepDuration = "48h"
  maxUsedSpace = "512MB"

# Policy 2
[[worker.oci.gcpolicy]]
  keepDuration = "1440h" # 60 days
  reservedSpace = "10GB"
  maxUsedSpace = "100GB"

# Policy 3
[[worker.oci.gcpolicy]]
  reservedSpace = "10GB"
  maxUsedSpace = "100GB"

# Policy 4
[[worker.oci.gcpolicy]]
  all = true
  reservedSpace = "10GB"
  maxUsedSpace = "100GB"
```

In practical terms, this means:

- Policy 1: If the build cache exceeds 512MB, BuildKit removes cache records
  for local build contexts, remote Git contexts, and cache mounts that haven’t
  been used in the last 48 hours.
- Policy 2: If disk usage exceeds 100GB, unshared build cache older than 60
  days is removed, ensuring at least 10GB of disk space is reserved for cache.
- Policy 3: If disk usage exceeds 100GB, any unshared cache is removed,
  ensuring at least 10GB of disk space is reserved for cache.
- Policy 4: If disk usage exceeds 100GB, all cache—including shared and
  internal records—is removed, ensuring at least 10GB of disk space is reserved
  for cache.

`reservedSpace` has the highest priority in defining the lower limit for build
cache size. If `maxUsedSpace` or `minFreeSpace` would define a lower value, the
minimum cache size would never be brought below `reservedSpace`.

If both `reservedSpace` and `maxUsedSpace` are set, a GC sweep results in a
cache size between those thresholds. For example, if `reservedSpace` is set to
10GB, and `maxUsedSpace` is set to 20GB, the resulting amount of cache after a
GC run is less than 20GB, but at least 10GB.

You can also define completely custom GC policies. Custom policies also let you
define filters, which lets you pinpoint the types of cache entries that a given
policy is allowed to prune.

#### Custom GC policies in BuildKit

Custom GC policies let you fine-tune how BuildKit manages its cache, and gives
you full control over cache retention based on criteria such as cache type,
duration, or disk space thresholds. If you need full control over the cache
thresholds and how cache records should be prioritized, defining custom GC
policies is the way to go.

To define a custom GC policy, use the `[[worker.oci.gcpolicy]]` configuration
block in `buildkitd.toml`. Each policy define the thresholds that will be used
for that policy. The global values for `reservedSpace`, `maxUsedSpace`, and
`minFreeSpace` do not apply if you use custom policies.

Here’s an example configuration:

```toml
# Custom GC Policy 1: Remove unused local contexts older than 24 hours
[[worker.oci.gcpolicy]]
  filters = ["type==source.local"]
  keepDuration = "24h"
  reservedSpace = "5GB"
  maxUsedSpace = "50GB"

# Custom GC Policy 2: Remove remote Git contexts older than 30 days
[[worker.oci.gcpolicy]]
  filters = ["type==source.git.checkout"]
  keepDuration = "720h"
  reservedSpace = "5GB"
  maxUsedSpace = "30GB"

# Custom GC Policy 3: Aggressively clean all cache if disk usage exceeds 90GB
[[worker.oci.gcpolicy]]
  all = true
  reservedSpace = "5GB"
  maxUsedSpace = "90GB"
```

In addition to the `reservedSpace`, `maxUsedSpace`, and `minFreeSpace` threshold,
when defining a GC policy you have two additional configuration options:

- `all`: By default, BuildKit will exclude some cache records from being pruned
  during GC. Setting this option to `true` will allow any cache records to be
  pruned.
- `filters`: Filters let you specify specific types of cache records that a GC
  policy is allowed to prune.

See
[buildx prune filters](https://docs.docker.com/reference/cli/docker/buildx/prune/#filter) for
information about available GC filters.

---

# Build cache invalidation

> Dig into the details about how cache invalidation works for Docker's build cache

# Build cache invalidation

   Table of contents

---

When building an image, Docker steps through the instructions in your
Dockerfile, executing each in the order specified. For each instruction, the
[builder](https://docs.docker.com/build/builders/) checks whether it can reuse the
instruction from the build cache.

## General rules

The basic rules of build cache invalidation are as follows:

- The builder begins by checking if the base image is already cached. Each
  subsequent instruction is compared against the cached layers. If no cached
  layer matches the instruction exactly, the cache is invalidated.
- In most cases, comparing the Dockerfile instruction with the corresponding
  cached layer is sufficient. However, some instructions require additional
  checks and explanations.
- For the `ADD` and `COPY` instructions, and for `RUN` instructions with bind
  mounts (`RUN --mount=type=bind`), the builder calculates a cache checksum
  from file metadata to determine whether cache is valid. During cache lookup,
  cache is invalidated if the file metadata has changed for any of the files
  involved.
  The modification time of a file (`mtime`) is not taken into account when
  calculating the cache checksum. If only the `mtime` of the copied files have
  changed, the cache is not invalidated.
- Aside from the `ADD` and `COPY` commands, cache checking doesn't look at the
  files in the container to determine a cache match. For example, when processing
  a `RUN apt-get -y update` command the files updated in the container
  aren't examined to determine if a cache hit exists. In that case just
  the command string itself is used to find a match.

Once the cache is invalidated, all subsequent Dockerfile commands generate new
images and the cache isn't used.

If your build contains several layers and you want to ensure the build cache is
reusable, order the instructions from less frequently changed to more
frequently changed where possible.

## WORKDIR and SOURCE_DATE_EPOCH

The `WORKDIR` instruction respects the `SOURCE_DATE_EPOCH` build argument when
determining cache validity. Changing `SOURCE_DATE_EPOCH` between builds
invalidates the cache for `WORKDIR` and all subsequent instructions.

`SOURCE_DATE_EPOCH` sets timestamps for files created during the build. If you
set this to a dynamic value like a Git commit timestamp, the cache breaks with
each commit. This is expected behavior when tracking build provenance.

For reproducible builds without frequent cache invalidation, use a fixed
timestamp:

```console
$ docker build --build-arg SOURCE_DATE_EPOCH=0 .
```

## RUN instructions

The cache for `RUN` instructions isn't invalidated automatically between builds.
Suppose you have a step in your Dockerfile to install `curl`:

```dockerfile
FROM alpine:3.23 AS install
RUN apk add curl
```

This doesn't mean that the version of `curl` in your image is always up-to-date.
Rebuilding the image one week later will still get you the same packages as before.
To force a re-execution of the `RUN` instruction, you can:

- Make sure that a layer before it has changed
- Clear the build cache ahead of the build using
  [docker builder prune](https://docs.docker.com/reference/cli/docker/builder/prune/)
- Use the `--no-cache` or `--no-cache-filter` options

The `--no-cache-filter` option lets you specify a specific build stage to
invalidate the cache for:

```console
$ docker build --no-cache-filter install .
```

## Build secrets

The contents of build secrets are not part of the build cache.
Changing the value of a secret doesn't result in cache invalidation.

If you want to force cache invalidation after changing a secret value,
you can pass a build argument with an arbitrary value that you also change when changing the secret.
Build arguments do result in cache invalidation.

```dockerfile
FROM alpine
ARG CACHEBUST
RUN --mount=type=secret,id=TOKEN,env=TOKEN \
    some-command ...
```

```console
$ TOKEN="tkn_pat123456" docker build --secret id=TOKEN --build-arg CACHEBUST=1 .
```

Properties of secrets such as IDs and mount paths do participate in the cache
checksum, and result in cache invalidation if changed.

---

# Optimize cache usage in builds

> An overview on how to optimize cache utilization in Docker builds.

# Optimize cache usage in builds

   Table of contents

---

When building with Docker, a layer is reused from the build cache if the
instruction and the files it depends on hasn't changed since it was previously
built. Reusing layers from the cache speeds up the build process because Docker
doesn't have to rebuild the layer again.

Here are a few techniques you can use to optimize build caching and speed up
the build process:

- [Order your layers](#order-your-layers): Putting the commands in your
  Dockerfile into a logical order can help you avoid unnecessary cache
  invalidation.
- [Keep the context small](#keep-the-context-small): The context is the set of
  files and directories that are sent to the builder to process a build
  instruction. Keeping the context as small as possible reduces the amount of data that
  needs to be sent to the builder, and reduces the likelihood of cache
  invalidation.
- [Use bind mounts](#use-bind-mounts): Bind mounts let you mount a file or
  directory from the host machine into the build container. Using bind mounts
  can help you avoid unnecessary layers in the image, which can slow down the
  build process.
- [Use cache mounts](#use-cache-mounts): Cache mounts let you specify a
  persistent package cache to be used during builds. The persistent cache helps
  speed up build steps, especially steps that involve installing packages using
  a package manager. Having a persistent cache for packages means that even if
  you rebuild a layer, you only download new or changed packages.
- [Use an external cache](#use-an-external-cache): An external cache lets you
  store build cache at a remote location. The external cache image can be
  shared between multiple builds, and across different environments.

## Order your layers

Putting the commands in your Dockerfile into a logical order is a great place
to start. Because a change causes a rebuild for steps that follow, try to make
expensive steps appear near the beginning of the Dockerfile. Steps that change
often should appear near the end of the Dockerfile, to avoid triggering
rebuilds of layers that haven't changed.

Consider the following example. A Dockerfile snippet that runs a JavaScript
build from the source files in the current directory:

```dockerfile
# syntax=docker/dockerfile:1
FROM node
WORKDIR /app
COPY . .          # Copy over all files in the current directory
RUN npm install   # Install dependencies
RUN npm build     # Run build
```

This Dockerfile is rather inefficient. Updating any file causes a reinstall of
all dependencies every time you build the Docker image even if the dependencies
didn't change since last time.

Instead, the `COPY` command can be split in two. First, copy over the package
management files (in this case, `package.json` and `yarn.lock`). Then, install
the dependencies. Finally, copy over the project source code, which is subject
to frequent change.

```dockerfile
# syntax=docker/dockerfile:1
FROM node
WORKDIR /app
COPY package.json yarn.lock .    # Copy package management files
RUN npm install                  # Install dependencies
COPY . .                         # Copy over project files
RUN npm build                    # Run build
```

By installing dependencies in earlier layers of the Dockerfile, there is
no need to rebuild those layers when a project file has changed.

## Keep the context small

The easiest way to make sure your context doesn't include unnecessary files is
to create a `.dockerignore` file in the root of your build context. The
`.dockerignore` file works similarly to `.gitignore` files, and lets you
exclude files and directories from the build context.

Here's an example `.dockerignore` file that excludes the `node_modules`
directory, all files and directories that start with `tmp`:

.dockerignore

```plaintext
node_modules
tmp*
```

Ignore-rules specified in the `.dockerignore` file apply to the entire build
context, including subdirectories. This means it's a rather coarse-grained
mechanism, but it's a good way to exclude files and directories that you know
you don't need in the build context, such as temporary files, log files, and
build artifacts.

## Use bind mounts

You might be familiar with bind mounts for when you run containers with `docker run` or Docker Compose. Bind mounts let you mount a file or directory from the
host machine into a container.

```bash
# bind mount using the -v flag
docker run -v $(pwd):/path/in/container image-name
# bind mount using the --mount flag
docker run --mount=type=bind,src=.,dst=/path/in/container image-name
```

To use bind mounts in a build, you can use the `--mount` flag with the `RUN`
instruction in your Dockerfile:

```dockerfile
FROM golang:latest
WORKDIR /app
RUN --mount=type=bind,target=. go build -o /app/hello
```

In this example, the current directory is mounted into the build container
before the `go build` command gets executed. The source code is available in
the build container for the duration of that `RUN` instruction. When the
instruction is done executing, the mounted files are not persisted in the final
image, or in the build cache. Only the output of the `go build` command
remains.

The `COPY` and `ADD` instructions in a Dockerfile lets you copy files from the
build context into the build container. Using bind mounts is beneficial for
build cache optimization because you're not adding unnecessary layers to the
cache. If you have build context that's on the larger side, and it's only used
to generate an artifact, you're better off using bind mounts to temporarily
mount the source code required to generate the artifact into the build. If you
use `COPY` to add the files to the build container, BuildKit will include all
of those files in the cache, even if the files aren't used in the final image.

There are a few things to be aware of when using bind mounts in a build:

- Bind mounts are read-only by default. If you need to write to the mounted
  directory, you need to specify the `rw` option. However, even with the `rw`
  option, the changes are not persisted in the final image or the build cache.
  The file writes are sustained for the duration of the `RUN` instruction, and
  are discarded after the instruction is done.
- Mounted files are not persisted in the final image. Only the output of the
  `RUN` instruction is persisted in the final image. If you need to include
  files from the build context in the final image, you need to use the `COPY`
  or `ADD` instructions.
- If the target directory is not empty, the contents of the target directory
  are hidden by the mounted files. The original contents are restored after the
  `RUN` instruction is done.
  For example, given a build context with only a `Dockerfile` in it:
  ```plaintext
  .
  └── Dockerfile
  ```
  And a Dockerfile that mounts the current directory into the build container:
  ```dockerfile
  FROM alpine:latest
  WORKDIR /work
  RUN touch foo.txt
  RUN --mount=type=bind,target=. ls
  RUN ls
  ```
  The first `ls` command with the bind mount shows the contents of the mounted
  directory. The second `ls` lists the contents of the original build context.
  Build log
  ```plaintext
  #8 [stage-0 3/5] RUN touch foo.txt
  #8 DONE 0.1s
  #9 [stage-0 4/5] RUN --mount=target=. ls -1
  #9 0.040 Dockerfile
  #9 DONE 0.0s
  #10 [stage-0 5/5] RUN ls -1
  #10 0.046 foo.txt
  #10 DONE 0.1s
  ```

## Use cache mounts

Regular cache layers in Docker correspond to an exact match of the instruction
and the files it depends on. If the instruction and the files it depends on
have changed since the layer was built, the layer is invalidated, and the build
process has to rebuild the layer.

Cache mounts are a way to specify a persistent cache location to be used during
builds. The cache is cumulative across builds, so you can read and write to the
cache multiple times. This persistent caching means that even if you need to
rebuild a layer, you only download new or changed packages. Any unchanged
packages are reused from the cache mount.

To use cache mounts in a build, you can use the `--mount` flag with the `RUN`
instruction in your Dockerfile:

```dockerfile
FROM node:latest
WORKDIR /app
RUN --mount=type=cache,target=/root/.npm npm install
```

In this example, the `npm install` command uses a cache mount for the
`/root/.npm` directory, the default location for the npm cache. The cache mount
is persisted across builds, so even if you end up rebuilding the layer, you
only download new or changed packages. Any changes to the cache are persisted
across builds, and the cache is shared between multiple builds.

How you specify cache mounts depends on the build tool you're using. If you're
unsure how to specify cache mounts, refer to the documentation for the build
tool you're using. Here are a few examples:

```dockerfile
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    go build -o /app/hello
```

```dockerfile
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
  --mount=type=cache,target=/var/lib/apt,sharing=locked \
  apt update && apt-get --no-install-recommends install -y gcc
```

```dockerfile
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt
```

```dockerfile
RUN --mount=type=cache,target=/root/.gem \
    bundle install
```

```dockerfile
RUN --mount=type=cache,target=/app/target/ \
    --mount=type=cache,target=/usr/local/cargo/git/db \
    --mount=type=cache,target=/usr/local/cargo/registry/ \
    cargo build
```

```dockerfile
RUN --mount=type=cache,target=/root/.nuget/packages \
    dotnet restore
```

```dockerfile
RUN --mount=type=cache,target=/tmp/cache \
    composer install
```

It's important that you read the documentation for the build tool you're using
to make sure you're using the correct cache mount options. Package managers
have different requirements for how they use the cache, and using the wrong
options can lead to unexpected behavior. For example, Apt needs exclusive
access to its data, so the caches use the option `sharing=locked` to ensure
parallel builds using the same cache mount wait for each other and not access
the same cache files at the same time.

## Use an external cache

The default cache storage for builds is internal to the builder (BuildKit
instance) you're using. Each builder uses its own cache storage. When you
switch between different builders, the cache is not shared between them. Using
an external cache lets you define a remote location for pushing and pulling
cache data.

External caches are especially useful for CI/CD pipelines, where the builders
are often ephemeral, and build minutes are precious. Reusing the cache between
builds can drastically speed up the build process and reduce cost. You can even
make use of the same cache in your local development environment.

To use an external cache, you specify the `--cache-to` and `--cache-from`
options with the `docker buildx build` command.

- `--cache-to` exports the build cache to the specified location.
- `--cache-from` specifies remote caches for the build to use.

The following example shows how to set up a GitHub Actions workflow using
`docker/build-push-action`, and push the build cache layers to an OCI registry
image:

.github/workflows/ci.yml

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

This setup tells BuildKit to look for cache in the `user/app:buildcache` image.
And when the build is done, the new build cache is pushed to the same image,
overwriting the old cache.

This cache can be used locally as well. To pull the cache in a local build,
you can use the `--cache-from` option with the `docker buildx build` command:

```console
$ docker buildx build --cache-from type=registry,ref=user/app:buildcache .
```

## Summary

Optimizing cache usage in builds can significantly speed up the build process.
Keeping the build context small, using bind mounts, cache mounts, and external
caches are all techniques you can use to make the most of the build cache and
speed up the build process.

For more information about the concepts discussed in this guide, see:

- [.dockerignore files](https://docs.docker.com/build/concepts/context/#dockerignore-files)
- [Cache invalidation](https://docs.docker.com/build/cache/invalidation/)
- [Cache mounts](https://docs.docker.com/reference/dockerfile/#run---mounttypecache)
- [Cache backend types](https://docs.docker.com/build/cache/backends/)
- [Building best practices](https://docs.docker.com/build/building/best-practices/)

---

# Docker build cache

> Improve your build speed with effective use of the build cache

# Docker build cache

   Table of contents

---

When you build the same Docker image multiple times, knowing how to optimize
the build cache is a great tool for making sure the builds run fast.

## How the build cache works

Understanding Docker's build cache helps you write better Dockerfiles that
result in faster builds.

The following example shows a small Dockerfile for a program written in C.

```dockerfile
# syntax=docker/dockerfile:1
FROM ubuntu:latest

RUN apt-get update && apt-get install -y build-essentials
COPY main.c Makefile /src/
WORKDIR /src/
RUN make build
```

Each instruction in this Dockerfile translates to a layer in your final image.
You can think of image layers as a stack, with each layer adding more content
on top of the layers that came before it:

![Image layer diagram](https://docs.docker.com/build/images/cache-stack.png)  ![Image layer diagram](https://docs.docker.com/build/images/cache-stack.png)

Whenever a layer changes, that layer will need to be re-built. For example,
suppose you make a change to your program in the `main.c` file. After this
change, the `COPY` command will have to run again in order for those changes to
appear in the image. In other words, Docker will invalidate the cache for this
layer.

If a layer changes, all other layers that come after it are also affected. When
the layer with the `COPY` command gets invalidated, all layers that follow will
need to run again, too:

![Image layer diagram, showing cache invalidation](https://docs.docker.com/build/images/cache-stack-invalidated.png)  ![Image layer diagram, showing cache invalidation](https://docs.docker.com/build/images/cache-stack-invalidated.png)

And that's the Docker build cache in a nutshell. Once a layer changes, then all
downstream layers need to be rebuilt as well. Even if they wouldn't build
anything differently, they still need to re-run.

## Other resources

For more information on using cache to do efficient builds, see:

- [Cache invalidation](https://docs.docker.com/build/cache/invalidation/)
- [Optimize build cache](https://docs.docker.com/build-cloud/optimization/)
- [Garbage collection](https://docs.docker.com/build/cache/garbage-collection/)
- [Cache storage backends](https://docs.docker.com/build/cache/backends/)
