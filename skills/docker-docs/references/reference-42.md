# Compose Build Specification and more

# Compose Build Specification

> Learn about the Compose Build Specification

# Compose Build Specification

   Table of contents

---

Build is an optional part of the Compose Specification. It tells Compose how to (re)build an application from source and lets you define the build process within a Compose file in a portable way. `build` can be either specified as a single string defining a context path, or as a detailed build definition.

In the former case, the whole path is used as a Docker context to execute a Docker build, looking for a canonical
`Dockerfile` at the root of the directory. The path can be absolute or relative. If it is relative, it is resolved
from the directory containing your Compose file. If it is absolute, the path prevents the Compose file from being portable so Compose displays a warning.

In the latter case, build arguments can be specified, including an alternate `Dockerfile` location. The path can be absolute or relative. If it is relative, it is resolved
from the directory containing your Compose file. If it is absolute, the path prevents the Compose file from being portable so Compose displays a warning.

## Usingbuildandimage

When Compose is confronted with both a `build` subsection for a service and an `image` attribute, it follows the rules defined by the [pull_policy](https://docs.docker.com/reference/compose-file/services/#pull_policy) attribute.

If `pull_policy` is missing from the service definition, Compose attempts to pull the image first and then builds from source if the image isn't found in the registry or platform cache.

## Publishing built images

Compose with `build` support offers an option to push built images to a registry. When doing so, it doesn't try to push service images without an `image` attribute. Compose warns you about the missing `image` attribute which prevents images being pushed.

## Illustrative example

The following example illustrates Compose Build Specification concepts with a concrete sample application. The sample is non-normative.

```yaml
services:
  frontend:
    image: example/webapp
    build: ./webapp

  backend:
    image: example/database
    build:
      context: backend
      dockerfile: ../backend.Dockerfile

  custom:
    build: ~/custom
```

When used to build service images from source, the Compose file creates three Docker images:

- `example/webapp`: A Docker image is built using `webapp` sub-directory, within the Compose file's folder, as the Docker build context. Lack of a `Dockerfile` within this folder returns an error.
- `example/database`: A Docker image is built using `backend` sub-directory within the Compose file's folder. `backend.Dockerfile` file is used to define build steps, this file is searched relative to the context path, which means `..` resolves to the Compose file's folder, so `backend.Dockerfile` is a sibling file.
- A Docker image is built using the `custom` directory with the user's `$HOME` as the Docker context. Compose displays a warning about the non-portable path used to build image.

On push, both `example/webapp` and `example/database` Docker images are pushed to the default registry. The `custom` service image is skipped as no `image` attribute is set and Compose displays a warning about this missing attribute.

## Attributes

The `build` subsection defines configuration options that are applied by Compose to build Docker images from source.
`build` can be specified either as a string containing a path to the build context or as a detailed structure:

Using the string syntax, only the build context can be configured as either:

- A relative path to the Compose file's folder. This path must be a directory and must contain a `Dockerfile`
  ```yml
  services:
    webapp:
      build: ./dir
  ```
- A Git repository URL. Git URLs accept context configuration in their fragment section, separated by a colon (`:`).
  The first part represents the reference that Git checks out, and can be either a branch, a tag, or a remote reference.
  The second part represents a subdirectory inside the repository that is used as a build context.
  ```yml
  services:
    webapp:
      build: https://github.com/mycompany/example.git#branch_or_tag:subdirectory
  ```

Alternatively `build` can be an object with fields defined as follows:

### additional_contexts

Requires: Docker Compose [2.17.0](https://github.com/docker/compose/releases/tag/v2.17.0) and later

`additional_contexts` defines a list of named contexts the image builder should use during image build.

`additional_contexts` can be a mapping or a list:

```yml
build:
  context: .
  additional_contexts:
    - resources=/path/to/resources
    - app=docker-image://my-app:latest
    - source=https://github.com/myuser/project.git
```

```yml
build:
  context: .
  additional_contexts:
    resources: /path/to/resources
    app: docker-image://my-app:latest
    source: https://github.com/myuser/project.git
```

When used as a list, the syntax follows the `NAME=VALUE` format, where `VALUE` is a string. Validation beyond that
is the responsibility of the image builder (and is builder specific). Compose supports at least
absolute and relative paths to a directory and Git repository URLs, like [context](#context) does. Other context flavours
must be prefixed to avoid ambiguity with a `type://` prefix.

Compose warns you if the image builder does not support additional contexts and may list
the unused contexts.

Refer to the reference documentation for [docker buildx build --build-context](https://github.com/docker/buildx/blob/master/docs/reference/buildx_build.md#-additional-build-contexts---build-context)
for example usage.

`additional_contexts` can also refer to an image built by another service.
This allows a service image to be built using another service image as a base image, and to share
layers between service images.

```yaml
services:
 base:
  build:
    context: .
    dockerfile_inline: |
      FROM alpine
      RUN ...
 my-service:
  build:
    context: .
    dockerfile_inline: |
      FROM base # image built for service base
      RUN ...
    additional_contexts:
      base: service:base
```

### args

`args` define build arguments, that is Dockerfile `ARG` values.

Using the following Dockerfile as an example:

```Dockerfile
ARG GIT_COMMIT
RUN echo "Based on commit: $GIT_COMMIT"
```

`args` can be set in the Compose file under the `build` key to define `GIT_COMMIT`. `args` can be set as a mapping or a list:

```yml
build:
  context: .
  args:
    GIT_COMMIT: cdc3b19
```

```yml
build:
  context: .
  args:
    - GIT_COMMIT=cdc3b19
```

Values can be omitted when specifying a build argument, in which case its value at build time must be obtained by user interaction,
otherwise the build argument won't be set when building the Docker image.

```yml
args:
  - GIT_COMMIT
```

### cache_from

`cache_from` defines a list of sources the image builder should use for cache resolution.

Cache location syntax follows the global format `[NAME|type=TYPE[,KEY=VALUE]]`. Simple `NAME` is actually a shortcut notation for `type=registry,ref=NAME`.

Compose Build implementations may support custom types, the Compose Specification defines canonical types which must be supported:

- `registry` to retrieve build cache from an OCI image set by key `ref`

```yml
build:
  context: .
  cache_from:
    - alpine:latest
    - type=local,src=path/to/cache
    - type=gha
```

Unsupported caches are ignored and don't prevent you from building images.

### cache_to

`cache_to` defines a list of export locations to be used to share build cache with future builds.

```yml
build:
  context: .
  cache_to:
   - user/app:cache
   - type=local,dest=path/to/cache
```

Cache target is defined using the same `type=TYPE[,KEY=VALUE]` syntax defined by [cache_from](#cache_from).

Unsupported caches are ignored and don't prevent you from building images.

### context

`context` defines either a path to a directory containing a Dockerfile, or a URL to a Git repository.

When the value supplied is a relative path, it is interpreted as relative to the project directory.
Compose warns you about the absolute path used to define the build context as those prevent the Compose file
from being portable.

```yml
build:
  context: ./dir
```

```yml
services:
  webapp:
    build: https://github.com/mycompany/webapp.git
```

If not set explicitly, `context` defaults to project directory (`.`).

### dockerfile

`dockerfile` sets an alternate Dockerfile. A relative path is resolved from the build context.
Compose warns you about the absolute path used to define the Dockerfile as it prevents Compose files
from being portable.

When set, `dockerfile_inline` attribute is not allowed and Compose
rejects any Compose file having both set.

```yml
build:
  context: .
  dockerfile: webapp.Dockerfile
```

### dockerfile_inline

Requires: Docker Compose [2.17.0](https://github.com/docker/compose/releases/tag/v2.17.0) and later

`dockerfile_inline` defines the Dockerfile content as an inlined string in a Compose file. When set, the `dockerfile`
attribute is not allowed and Compose rejects any Compose file having both set.

Use of YAML multi-line string syntax is recommended to define the Dockerfile content:

```yml
build:
  context: .
  dockerfile_inline: |
    FROM baseimage
    RUN some command
```

### entitlements

Requires: Docker Compose [2.27.1](https://github.com/docker/compose/releases/tag/v2.27.1) and later

`entitlements` defines extra privileged entitlements to be allowed during the build.

```yaml
entitlements:
  - network.host
  - security.insecure
```

### extra_hosts

`extra_hosts` adds hostname mappings at build-time. Use the same syntax as [extra_hosts](https://docs.docker.com/reference/compose-file/services/#extra_hosts).

```yml
extra_hosts:
  - "somehost=162.242.195.82"
  - "otherhost=50.31.209.229"
  - "myhostv6=::1"
```

IPv6 addresses can be enclosed in square brackets, for example:

```yml
extra_hosts:
  - "myhostv6=[::1]"
```

The separator `=` is preferred, but `:` can also be used. Introduced in Docker Compose version [2.24.1](https://github.com/docker/compose/releases/tag/v2.24.1). For example:

```yml
extra_hosts:
  - "somehost:162.242.195.82"
  - "myhostv6:::1"
```

Compose creates matching entry with the IP address and hostname in the container's network
configuration, which means for Linux `/etc/hosts` will get extra lines:

```text
162.242.195.82  somehost
50.31.209.229   otherhost
::1             myhostv6
```

### isolation

`isolation` specifies a build’s container isolation technology. Like [isolation](https://docs.docker.com/reference/compose-file/services/#isolation), supported values
are platform specific.

### labels

`labels` add metadata to the resulting image. `labels` can be set either as an array or a map.

It's recommended that you use reverse-DNS notation to prevent your labels from conflicting with other software.

```yml
build:
  context: .
  labels:
    com.example.description: "Accounting webapp"
    com.example.department: "Finance"
    com.example.label-with-empty-value: ""
```

```yml
build:
  context: .
  labels:
    - "com.example.description=Accounting webapp"
    - "com.example.department=Finance"
    - "com.example.label-with-empty-value"
```

### network

Set the network containers connect to for the `RUN` instructions during build.

```yaml
build:
  context: .
  network: host
```

```yaml
build:
  context: .
  network: custom_network_1
```

Use `none` to disable networking during build:

```yaml
build:
  context: .
  network: none
```

### no_cache

`no_cache` disables image builder cache and enforces a full rebuild from source for all image layers. This only
applies to layers declared in the Dockerfile, referenced images can be retrieved from local image store whenever tag
has been updated on registry (see [pull](#pull)).

### platforms

`platforms` defines a list of target [platforms](https://docs.docker.com/reference/compose-file/services/#platform).

```yml
build:
  context: "."
  platforms:
    - "linux/amd64"
    - "linux/arm64"
```

When the `platforms` attribute is omitted, Compose includes the service's platform
in the list of the default build target platforms.

When the `platforms` attribute is defined, Compose includes the service's
platform, otherwise users won't be able to run images they built.

Composes reports an error in the following cases:

- When the list contains multiple platforms but the implementation is incapable of storing multi-platform images.
- When the list contains an unsupported platform.
  ```yml
  build:
    context: "."
    platforms:
      - "linux/amd64"
      - "unsupported/unsupported"
  ```
- When the list is non-empty and does not contain the service's platform.
  ```yml
  services:
    frontend:
      platform: "linux/amd64"
      build:
        context: "."
        platforms:
          - "linux/arm64"
  ```

### privileged

Requires: Docker Compose [2.15.0](https://github.com/docker/compose/releases/tag/v2.15.0) and later

`privileged` configures the service image to build with elevated privileges. Support and actual impacts are platform specific.

```yml
build:
  context: .
  privileged: true
```

### provenance

Requires: Docker Compose [2.39.0](https://github.com/docker/compose/releases/tag/v2.39.0) and later

`provenance` configures the builder to add a [provenance attestation](https://slsa.dev/provenance/v0.2#schema) to the published image.

The value can be either a boolean to enable/disable provenance attestation, or a key=value string to set provenance configuration. You can
use this to select the level of detail to be included in the provenance attestation by setting the `mode` parameter.

```yaml
build:
  context: .
  provenance: true
```

```yaml
build:
  context: .
  provenance: mode=max
```

### pull

`pull` requires the image builder to pull referenced images (`FROM` Dockerfile directive), even if those are already
available in the local image store.

### sbom

Requires: Docker Compose [2.39.0](https://github.com/docker/compose/releases/tag/v2.39.0) and later

`sbom` configures the builder to add a [provenance attestation](https://slsa.dev/provenance/v0.2#schema) to the published image.
The value can be either a boolean to enable/disable sbom attestation, or a key=value string to set SBOM generator configuration. This let you
select an alternative SBOM generator image (see [https://github.com/moby/buildkit/blob/master/docs/attestations/sbom-protocol.md](https://github.com/moby/buildkit/blob/master/docs/attestations/sbom-protocol.md))

```yaml
build:
  context: .
  sbom: true
```

```yaml
build:
  context: .
  sbom: generator=docker/scout-sbom-indexer:latest # Use an alternative SBOM generator
```

### secrets

`secrets` grants access to sensitive data defined by [secrets](https://docs.docker.com/reference/compose-file/services/#secrets) on a per-service build basis. Two
different syntax variants are supported: the short syntax and the long syntax.

Compose reports an error if the secret isn't defined in the
[secrets](https://docs.docker.com/reference/compose-file/secrets/) section of this Compose file.

#### Short syntax

The short syntax variant only specifies the secret name. This grants the
container access to the secret and mounts it as read-only to `/run/secrets/<secret_name>`
within the container. The source name and destination mountpoint are both set
to the secret name.

The following example uses the short syntax to grant the build of the `frontend` service
access to the `server-certificate` secret. The value of `server-certificate` is set
to the contents of the file `./server.cert`.

```yml
services:
  frontend:
    build:
      context: .
      secrets:
        - server-certificate
secrets:
  server-certificate:
    file: ./server.cert
```

#### Long syntax

The long syntax provides more granularity in how the secret is created within
the service's containers.

- `source`: The name of the secret as it exists on the platform.
- `target`: The ID of the secret as declared in the Dockerfile. Defaults to `source` if not specified.
- `uid` and `gid`: The numeric uid or gid that owns the file within
  `/run/secrets/` in the service's task containers. Default value is `USER`.
- `mode`: The [permissions](https://wintelguy.com/permissions-calc.pl) for the file to be mounted in `/run/secrets/`
  in the service's task containers, in octal notation.
  Default value is world-readable permissions (mode `0444`).
  The writable bit must be ignored if set. The executable bit may be set.

The following example sets the name of the `server-certificate` secret file to `server.crt`
within the container, sets the mode to `0440` (group-readable) and sets the user and group
to `103`. The value of `server-certificate` secret is provided by the platform through a lookup and
the secret lifecycle not directly managed by Compose.

```yml
services:
  frontend:
    build:
      context: .
      secrets:
        - source: server-certificate
          target: cert # secret ID in Dockerfile
          uid: "103"
          gid: "103"
          mode: 0440
secrets:
  server-certificate:
    external: true
```

```dockerfile
# Dockerfile
FROM nginx
RUN --mount=type=secret,id=cert,required=true,target=/root/cert ...
```

Service builds may be granted access to multiple secrets. Long and short syntax for secrets may be used in the
same Compose file. Defining a secret in the top-level `secrets` must not imply granting any service build access to it.
Such grant must be explicit within service specification as [secrets](https://docs.docker.com/reference/compose-file/services/#secrets) service element.

### ssh

`ssh` defines SSH authentications that the image builder should use during image build (e.g., cloning private repository).

`ssh` property syntax can be either:

- `default`: Let the builder connect to the SSH-agent.
- `ID=path`: A key/value definition of an ID and the associated path. It can be either a [PEM](https://en.wikipedia.org/wiki/Privacy-Enhanced_Mail) file, or path to ssh-agent socket.

```yaml
build:
  context: .
  ssh:
    - default   # mount the default SSH agent
```

or

```yaml
build:
  context: .
  ssh: ["default"]   # mount the default SSH agent
```

Using a custom id `myproject` with path to a local SSH key:

```yaml
build:
  context: .
  ssh:
    - myproject=~/.ssh/myproject.pem
```

The image builder can then rely on this to mount the SSH key during build.

For illustration, [SSH mounts](https://github.com/moby/buildkit/blob/master/frontend/dockerfile/docs/reference.md#run---mounttypessh) can be used to mount the SSH key set by ID and access a secured resource:

```console
RUN --mount=type=ssh,id=myproject git clone ...
```

### shm_size

`shm_size` sets the size of the shared memory (`/dev/shm` partition on Linux) allocated for building Docker images. Specify
as an integer value representing the number of bytes or as a string expressing a [byte value](https://docs.docker.com/reference/compose-file/extension/#specifying-byte-values).

```yml
build:
  context: .
  shm_size: '2gb'
```

```yaml
build:
  context: .
  shm_size: 10000000
```

### tags

`tags` defines a list of tag mappings that must be associated to the build image. This list comes in addition to
the `image` [property defined in the service section](https://docs.docker.com/reference/compose-file/services/#image)

```yml
tags:
  - "myimage:mytag"
  - "registry/username/myrepos:my-other-tag"
```

### target

`target` defines the stage to build as defined inside a multi-stage `Dockerfile`.

```yml
build:
  context: .
  target: prod
```

### ulimits

Requires: Docker Compose [2.23.1](https://github.com/docker/compose/releases/tag/v2.23.1) and later

`ulimits` overrides the default `ulimits` for a container. It's specified either as an integer for a single limit
or as mapping for soft/hard limits.

```yml
services:
  frontend:
    build:
      context: .
      ulimits:
        nproc: 65535
        nofile:
          soft: 20000
          hard: 40000
```

---

# Configs top

> Manage and share configuration data using the configs element in Docker Compose.

# Configs top-level element

   Table of contents

---

Configs let services adapt their behaviour without the need to rebuild a Docker image. As with volumes, configs are mounted as files into a container's filesystem. The location of the mount point within the container defaults to `/<config-name>` in Linux containers and `C:\<config-name>` in Windows containers.

Services can only access configs when explicitly granted by a [configs](https://docs.docker.com/reference/compose-file/services/#configs) attribute within the `services` top-level element.

By default, the config:

- Is owned by the user running the container command but can be overridden by service configuration.
- Has world-readable permissions (mode 0444), unless the service is configured to override this.

The top-level `configs` declaration defines or references configuration data that is granted to services in your Compose application. The source of the config is either `file`, `environment`, `content`, or `external`.

- `file`: The config is created with the contents of the file at the specified path.
- `environment`: The config content is created with the value of an environment variable. Introduced in Docker Compose version [2.23.1](https://github.com/docker/compose/releases/tag/v2.23.1).
- `content`: The content is created with the inlined value. Introduced in Docker Compose version [2.23.1](https://github.com/docker/compose/releases/tag/v2.23.1).
- `external`: If set to true, `external` specifies that this config has already been created. Compose does not
  attempt to create it, and if it does not exist, an error occurs.
- `name`: The name of the config object in the container engine to look up. This field can be used to
  reference configs that contain special characters. The name is used as is
  and will **not** be scoped with the project name.

## Example 1

`<project_name>_http_config` is created when the application is deployed,
by registering the content of the `httpd.conf` as the configuration data.

```yml
configs:
  http_config:
    file: ./httpd.conf
```

Alternatively, `http_config` can be declared as external. Compose looks up `http_config` to expose the configuration data to relevant services.

```yml
configs:
  http_config:
    external: true
```

## Example 2

External configs lookup can also use a distinct key by specifying a `name`.

The following
example modifies the previous one to look up a config using the parameter `HTTP_CONFIG_KEY`. The actual lookup key is set at deployment time by the [interpolation](https://docs.docker.com/reference/compose-file/interpolation/) of
variables, but exposed to containers as hard-coded ID `http_config`.

```yml
configs:
  http_config:
    external: true
    name: "${HTTP_CONFIG_KEY}"
```

## Example 3

`<project_name>_app_config` is created when the application is deployed,
by registering the inlined content as the configuration data. This means Compose infers variables when creating the config, which allows you to
adjust content according to service configuration:

```yml
configs:
  app_config:
    content: |
      debug=${DEBUG}
      spring.application.admin.enabled=${DEBUG}
      spring.application.name=${COMPOSE_PROJECT_NAME}
```

## Example 4

`<project_name>_simple_config` is created when the application is deployed,
using the value of an environment variable as the configuration data. This is useful for simple configuration values that don’t require interpolation:

```yml
configs:
  simple_config:
    environment: "SIMPLE_CONFIG_VALUE"
```

If `external` is set to `true`, all other attributes apart from `name` are irrelevant. If Compose detects any other attribute, it rejects the Compose file as invalid.

---

# Compose Deploy Specification

> Learn about the Compose Deploy Specification

# Compose Deploy Specification

   Table of contents

---

Deploy is an optional part of the Compose Specification. It provides a set of deployment specifications for managing the behavior of containers across different environments.

## Attributes

### endpoint_mode

`endpoint_mode` specifies a service discovery method for external clients connecting to a service. The Compose Deploy Specification defines two canonical values:

- `endpoint_mode: vip`: Assigns the service a virtual IP (VIP) that acts as the front end for clients to reach the service
  on a network. Platform routes requests between the client and nodes running the service, without client knowledge of how
  many nodes are participating in the service or their IP addresses or ports.
- `endpoint_mode: dnsrr`: Platform sets up DNS entries for the service such that a DNS query for the service name returns a
  list of IP addresses (DNS round-robin), and the client connects directly to one of these.

```yml
services:
  frontend:
    image: example/webapp
    ports:
      - "8080:80"
    deploy:
      mode: replicated
      replicas: 2
      endpoint_mode: vip
```

### labels

`labels` specifies metadata for the service. These labels are only set on the service and not on any containers for the service.
This assumes the platform has some native concept of "service" that can match the Compose application model.

```yml
services:
  frontend:
    image: example/webapp
    deploy:
      labels:
        com.example.description: "This label will appear on the web service"
```

### mode

`mode` defines the replication model used to run a service or job. Options include:

- `global`: Ensures exactly one task continuously runs per physical node until stopped.
- `replicated`: Continuously runs a specified number of tasks across nodes until stopped (default).
- `replicated-job`: Executes a defined number of tasks until a completion state (exits with code 0)'.
  - Total tasks are determined by `replicas`.
  - Concurrency can be limited using the `max-concurrent` option (CLI only).
- `global-job`: Executes one task per physical node with a completion state (exits with code 0).
  - Automatically runs on new nodes as they are added.

```yml
services:
  frontend:
    image: example/webapp
    deploy:
      mode: global

  batch-job:
    image: example/processor
    deploy:
      mode: replicated-job
      replicas: 5

  maintenance:
    image: example/updater
    deploy:
      mode: global-job
```

> Note
>
> - Job modes (`replicated-job` and `global-job`) are designed for tasks that complete and exit with code 0.
> - Completed tasks remain until explicitly removed.
> - Options like `max-concurrent` for controlling concurrency are supported only via the CLI and are not available in Compose.

For more detailed information about job options and behavior, see the
[Docker CLI documentation](https://docs.docker.com/reference/cli/docker/service/create/#running-as-a-job)

### placement

`placement` specifies constraints and preferences for the platform to select a physical node to run service containers.

#### constraints

`constraints` defines a required property the platform's node must fulfill to run the service container. For a further example, see the
[CLI reference docs](https://docs.docker.com/reference/cli/docker/service/create/#constraint).

```yml
deploy:
  placement:
    constraints:
      - node.labels.disktype==ssd
```

#### preferences

`preferences` defines a strategy (currently `spread` is the only supported strategy) to spread tasks evenly
over the values of the datacenter node label. For a further example, see the
[CLI reference docs](https://docs.docker.com/reference/cli/docker/service/create/#placement-pref)

```yml
deploy:
  placement:
    preferences:
      - spread: node.labels.zone
```

### replicas

If the service is `replicated` (which is the default), `replicas` specifies the number of containers that should be
running at any given time.

```yml
services:
  frontend:
    image: example/webapp
    deploy:
      mode: replicated
      replicas: 6
```

### resources

`resources` configures physical resource constraints for container to run on platform. Those constraints can be configured
as:

- `limits`: The platform must prevent the container from allocating more resources.
- `reservations`: The platform must guarantee the container can allocate at least the configured amount.

```yml
services:
  frontend:
    image: example/webapp
    deploy:
      resources:
        limits:
          cpus: '0.50'
          memory: 50M
          pids: 1
        reservations:
          cpus: '0.25'
          memory: 20M
```

#### cpus

`cpus` configures a limit or reservation for how much of the available CPU resources, as number of cores, a container can use.

#### memory

`memory` configures a limit or reservation on the amount of memory a container can allocate, set as a string expressing a [byte value](https://docs.docker.com/reference/compose-file/extension/#specifying-byte-values).

#### pids

`pids` tunes a container’s PIDs limit, set as an integer.

#### devices

`devices` configures reservations of the devices a container can use. It contains a list of reservations, each set as an object with the following parameters: `capabilities`, `driver`, `count`, `device_ids` and `options`.

Devices are reserved using a list of capabilities, making `capabilities` the only required field. A device must satisfy all the requested capabilities for a successful reservation.

##### capabilities

`capabilities` are set as a list of strings, expressing both generic and driver specific capabilities.
The following generic capabilities are recognized today:

- `gpu`: Graphics accelerator
- `tpu`: AI accelerator

To avoid name clashes, driver specific capabilities must be prefixed with the driver name.
For example, reserving an NVIDIA CUDA-enabled accelerator might look like this:

```yml
deploy:
  resources:
    reservations:
      devices:
        - capabilities: ["nvidia-compute"]
```

##### driver

A different driver for the reserved device(s) can be requested using `driver` field. The value is specified as a string.

```yml
deploy:
  resources:
    reservations:
      devices:
        - capabilities: ["nvidia-compute"]
          driver: nvidia
```

##### count

If `count` is set to `all` or not specified, Compose reserves all devices that satisfy the requested capabilities. Otherwise, Compose reserves at least the number of devices specified. The value is specified as an integer.

```yml
deploy:
  resources:
    reservations:
      devices:
        - capabilities: ["tpu"]
          count: 2
```

`count` and `device_ids` fields are exclusive. Compose returns an error if both are specified.

##### device_ids

If `device_ids` is set, Compose reserves devices with the specified IDs provided they satisfy the requested capabilities. The value is specified as a list of strings.

```yml
deploy:
  resources:
    reservations:
      devices:
        - capabilities: ["gpu"]
          device_ids: ["GPU-f123d1c9-26bb-df9b-1c23-4a731f61d8c7"]
```

`count` and `device_ids` fields are exclusive. Compose returns an error if both are specified.

##### options

Driver specific options can be set with `options` as key-value pairs.

```yml
deploy:
  resources:
    reservations:
      devices:
        - capabilities: ["gpu"]
          driver: gpuvendor
          options:
            virtualization: false
```

### restart_policy

`restart_policy` configures if and how to restart containers when they exit. If `restart_policy` is not set, Compose considers the `restart` field set by the service configuration.

- `condition`. When set to:
  - `none`, containers are not automatically restarted regardless of the exit status.
  - `on-failure`, the container is restarted if it exits due to an error, which manifests as a non-zero exit code.
  - `any` (default), containers are restarted regardless of the exit status.
- `delay`: How long to wait between restart attempts, specified as a [duration](https://docs.docker.com/reference/compose-file/extension/#specifying-durations). The default is 0, meaning restart attempts can occur immediately.
- `max_attempts`: The maximum number of failed restart attempts allowed before giving up. (Default: unlimited retries.)
  A failed attempt only counts toward `max_attempts` if the container does not successfully restart within the time defined by `window`.
  For example, if `max_attempts` is set to `2` and the container fails to restart within the window on the first try, Compose continues retrying until two such failed attempts occur, even if that means trying more than twice.
- `window`: The amount of time to wait after a restart to determine whether it was successful, specified as a [duration](https://docs.docker.com/reference/compose-file/extension/#specifying-durations) (default: the result is evaluated immediately after the restart).

```yml
deploy:
  restart_policy:
    condition: on-failure
    delay: 5s
    max_attempts: 3
    window: 120s
```

### rollback_config

`rollback_config` configures how the service should be rolled back in case of a failing update.

- `parallelism`: The number of containers to rollback at a time. If set to 0, all containers rollback simultaneously.
- `delay`: The time to wait between each container group's rollback (default 0s).
- `failure_action`: What to do if a rollback fails. One of `continue` or `pause` (default `pause`)
- `monitor`: Duration after each task update to monitor for failure `(ns|us|ms|s|m|h)` (default 0s).
- `max_failure_ratio`: Failure rate to tolerate during a rollback (default 0).
- `order`: Order of operations during rollbacks. One of `stop-first` (old task is stopped before starting new one),
  or `start-first` (new task is started first, and the running tasks briefly overlap) (default `stop-first`).

### update_config

`update_config` configures how the service should be updated. Useful for configuring rolling updates.

- `parallelism`: The number of containers to update at a time.
- `delay`: The time to wait between updating a group of containers.
- `failure_action`: What to do if an update fails. One of `continue`, `rollback`, or `pause` (default: `pause`).
- `monitor`: Duration after each task update to monitor for failure `(ns|us|ms|s|m|h)` (default 0s).
- `max_failure_ratio`: Failure rate to tolerate during an update.
- `order`: Order of operations during updates. One of `stop-first` (old task is stopped before starting new one),
  or `start-first` (new task is started first, and the running tasks briefly overlap) (default `stop-first`).

```yml
deploy:
  update_config:
    parallelism: 2
    delay: 10s
    order: stop-first
```

---

# Compose Develop Specification

> Learn about the Compose Develop Specification

# Compose Develop Specification

   Table of contents

---

> Note
>
> Develop is an optional part of the Compose Specification. It is available with Docker Compose version 2.22.0 and later.

This page defines how Compose behaves to efficiently assist you and defines the development constraints and workflows set by Compose. Only a subset of Compose file services may require a `develop` subsection.

## Illustrative example

```yaml
services:
  frontend:
    image: example/webapp
    build: ./webapp
    develop:
      watch:
        # sync static content
        - path: ./webapp/html
          action: sync
          target: /var/www
          ignore:
            - node_modules/

  backend:
    image: example/backend
    build: ./backend
    develop:
      watch:
        # rebuild image and recreate service
        - path: ./backend/src
          action: rebuild
```

## Attributes

The `develop` subsection defines configuration options that are applied by Compose to assist you during development of a service with optimized workflows.

### watch

The `watch` attribute defines a list of rules that control automatic service updates based on local file changes. `watch` is a sequence, each individual item in the sequence defines a rule to be applied by
Compose to monitor source code for changes. For more information, see
[Use Compose Watch](https://docs.docker.com/compose/how-tos/file-watch/).

#### action

`action` defines the action to take when changes are detected. If `action` is set to:

- `rebuild`: Compose rebuilds the service image based on the `build` section and recreates the service with the updated image.
- `restart`: Compose restarts the service container. Available with Docker Compose version 2.32.0 and later.
- `sync`: Compose keeps the existing service container(s) running, but synchronizes source files with container content according to the `target` attribute.
- `sync+restart`: Compose synchronizes source files with container content according to the `target` attribute, and then restarts the container. Available with Docker Compose version 2.23.0 and later.
- `sync+exec`: Compose synchronizes source files with container content according to the `target` attribute, and then executes a command inside the container. Available with Docker Compose version 2.32.0 and later.

#### exec

Requires: Docker Compose [2.32.2](https://github.com/docker/compose/releases/tag/v2.32.2) and later

`exec` is only relevant when `action` is set to `sync+exec`. Like [service hooks](https://docs.docker.com/reference/compose-file/services/#post_start), `exec` is used to define the command to be run inside the container once it has started.

- `command`: Specifies the command to run once the container starts. This attribute is required, and you can choose to use either the shell form or the exec form.
- `user`: The user to run the command. If not set, the command is run with the same user as the main service command.
- `privileged`: Lets the command run with privileged access.
- `working_dir`: The working directory in which to run the command. If not set, it is run in the same working directory as the main service command.
- `environment`: Sets the environment variables to run the command. While the command inherits the environment variables defined for the service’s main command, this section lets you add new variables or override existing ones.

```yaml
services:
  frontend:
    image: ...
    develop:
      watch:
        # sync content then run command to reload service without interruption
        - path: ./etc/config
          action: sync+exec
          target: /etc/config/
          exec:
            command: app reload
```

#### ignore

The `ignore` attribute is used to define a list of patterns for paths to be ignored. Any updated file
that matches a pattern, or belongs to a folder that matches a pattern, won't trigger services to be re-created.
The syntax is the same as `.dockerignore` file:

- `*` matches 0 or more characters in a filename.
- `?` matches a single character in filename.
- `*/*` matches two nested folders with arbitrary names
- `**` matches an arbitrary number of nested folders

If the build context includes a `.dockerignore` file, the patterns in this file is loaded as implicit content
for the `ignores` file, and values set in the Compose model are appended.

#### include

It is sometimes easier to select files to be watched instead of declaring those that shouldn't be watched with `ignore`.

The `include` attribute is used to define a pattern, or a list of patterns, for paths to be considered for watching.
Only files that match these patterns will be considered when applying a watch rule. The syntax is the same as `ignore`.

```yaml
services:
  backend:
    image: example/backend
    develop:
      watch:
        # rebuild image and recreate service
        - path: ./src
          include: "*.go"
          action: rebuild
```

> Note
>
> In many cases `include` patterns start with a wildcard (`*`) character. This has special meaning in YAML syntax
> to define an [alias node](https://yaml.org/spec/1.2.2/#alias-nodes) so you have to wrap pattern expression with quotes.

#### initial_sync

When using `sync+x` actions, it can be useful to ensure that files inside containers are up to date at the start of a new watch session.

The `initial_sync` attribute instructs the Compose runtime, if containers for the service already exist, to check that the files from the path attribute are in sync within the service containers.

#### path

`path` attribute defines the path to source code (relative to the project directory) to monitor for changes. Updates to any file
inside the path, which doesn't match any `ignore` rule, triggers the configured action.

#### target

`target` attribute only applies when `action` is configured for `sync`. Files within `path` that have changes are synchronized with the container's filesystem, so that the latter is always running with up-to-date content.

---

# Extensions

> Define and reuse custom fragments with extensions in Docker Compose

# Extensions

   Table of contents

---

Extensions can be used to make your Compose file more efficient and easier to maintain.

Use the prefix `x-` as a top-level element to modularize configurations that you want to reuse.
Compose ignores any fields that start with `x-`, this is the sole exception where Compose silently ignores unrecognized fields.

Extensions can also be used with [anchors and aliases](https://docs.docker.com/reference/compose-file/fragments/).

They also can be used within any structure in a Compose file where user-defined keys are not expected.
Compose uses those to enable experimental features, the same way browsers add support for [custom CSS features](https://www.w3.org/TR/2011/REC-CSS2-20110607/syndata.html#vendor-keywords)

## Example 1

```yml
x-custom:
  foo:
    - bar
    - zot

services:
  webapp:
    image: example/webapp
    x-foo: bar
```

```yml
service:
  backend:
    deploy:
      placement:
        x-aws-role: "arn:aws:iam::XXXXXXXXXXXX:role/foo"
        x-aws-region: "eu-west-3"
        x-azure-region: "france-central"
```

## Example 2

```yml
x-env: &env
  environment:
    - CONFIG_KEY
    - EXAMPLE_KEY

services:
  first:
    <<: *env
    image: my-image:latest
  second:
    <<: *env
    image: another-image:latest
```

In this example, the environment variables do not belong to either of the services. They’ve been lifted out completely into the `x-env` extension field.
This defines a new node which contains the environment field. The `&env` YAML anchor is used so both services can reference the extension field’s value as `*env`.

## Example 3

```yml
x-function: &function
 labels:
   function: "true"
 depends_on:
   - gateway
 networks:
   - functions
 deploy:
   placement:
     constraints:
       - 'node.platform.os == linux'
services:
 # Node.js gives OS info about the node (Host)
 nodeinfo:
   <<: *function
   image: functions/nodeinfo:latest
   environment:
     no_proxy: "gateway"
     https_proxy: $https_proxy
 # Uses `cat` to echo back response, fastest function to execute.
 echoit:
   <<: *function
   image: functions/alpine:health
   environment:
     fprocess: "cat"
     no_proxy: "gateway"
     https_proxy: $https_proxy
```

The `nodeinfo` and `echoit` services both include the `x-function` extension via the `&function` anchor, then set their specific image and environment.

## Example 4

Using [YAML merge](https://yaml.org/type/merge.html) it is also possible to use multiple extensions and share
and override additional attributes for specific needs:

```yml
x-environment: &default-environment
  FOO: BAR
  ZOT: QUIX
x-keys: &keys
  KEY: VALUE
services:
  frontend:
    image: example/webapp
    environment:
      << : [*default-environment, *keys]
      YET_ANOTHER: VARIABLE
```

> Note
>
> [YAML merge](https://yaml.org/type/merge.html) only applies to mappings, and can't be used with sequences.
>
>
>
> In the example above, the environment variables are declared using the `FOO: BAR` mapping syntax, while the sequence syntax `- FOO=BAR` is only valid when no fragments are involved.

## Informative historical notes

This section is informative. At the time of writing, the following prefixes are known to exist:

| Prefix | Vendor/Organization |
| --- | --- |
| docker | Docker |
| kubernetes | Kubernetes |

## Specifying byte values

Values express a byte value as a string in `{amount}{byte unit}` format:
The supported units are `b` (bytes), `k` or `kb` (kilo bytes), `m` or `mb` (mega bytes) and `g` or `gb` (giga bytes).

```text
2b
    1024kb
    2048k
    300m
    1gb
```

## Specifying durations

Values express a duration as a string in the form of `{value}{unit}`.
The supported units are `us` (microseconds), `ms` (milliseconds), `s` (seconds), `m` (minutes) and `h` (hours).
Values can combine multiple values without separator.

```text
10ms
  40s
  1m30s
  1h5m30s20ms
```
