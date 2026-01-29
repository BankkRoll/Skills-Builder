# Run Docker Compose services with GPU access and more

# Run Docker Compose services with GPU access

> Learn how to configure Docker Compose to use NVIDIA GPUs with CUDA-based containers

# Run Docker Compose services with GPU access

   Table of contents

---

Compose services can define GPU device reservations if the Docker host contains such devices and the Docker Daemon is set accordingly. For this, make sure you install the
[prerequisites](https://docs.docker.com/engine/containers/resource_constraints/#gpu) if you haven't already done so.

The examples in the following sections focus specifically on providing service containers access to GPU devices with Docker Compose.

## Enabling GPU access to service containers

GPUs are referenced in a `compose.yaml` file using the
[device](https://docs.docker.com/reference/compose-file/deploy/#devices) attribute from the Compose Deploy specification, within your services that need them.

This provides more granular control over a GPU reservation as custom values can be set for the following device properties:

- `capabilities`. This value is specified as a list of strings. For example, `capabilities: [gpu]`. You must set this field in the Compose file. Otherwise, it returns an error on service deployment.
- `count`. Specified as an integer or the value `all`, represents the number of GPU devices that should be reserved (providing the host holds that number of GPUs). If `count` is set to `all` or not specified, all GPUs available on the host are used by default.
- `device_ids`. This value, specified as a list of strings, represents GPU device IDs from the host. You can find the device ID in the output of `nvidia-smi` on the host. If no `device_ids` are set, all GPUs available on the host are used by default.
- `driver`. Specified as a string, for example `driver: 'nvidia'`
- `options`. Key-value pairs representing driver specific options.

> Important
>
> You must set the `capabilities` field. Otherwise, it returns an error on service deployment.

> Note
>
> `count` and `device_ids` are mutually exclusive. You must only define one field at a time.

For more information on these properties, see the
[Compose Deploy Specification](https://docs.docker.com/reference/compose-file/deploy/#devices).

### Example of a Compose file for running a service with access to 1 GPU device

```yaml
services:
  test:
    image: nvidia/cuda:12.9.0-base-ubuntu22.04
    command: nvidia-smi
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

Run with Docker Compose:

```console
$ docker compose up
Creating network "gpu_default" with the default driver
Creating gpu_test_1 ... done
Attaching to gpu_test_1
test_1  | +-----------------------------------------------------------------------------+
test_1  | | NVIDIA-SMI 450.80.02    Driver Version: 450.80.02    CUDA Version: 11.1     |
test_1  | |-------------------------------+----------------------+----------------------+
test_1  | | GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
test_1  | | Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
test_1  | |                               |                      |               MIG M. |
test_1  | |===============================+======================+======================|
test_1  | |   0  Tesla T4            On   | 00000000:00:1E.0 Off |                    0 |
test_1  | | N/A   23C    P8     9W /  70W |      0MiB / 15109MiB |      0%      Default |
test_1  | |                               |                      |                  N/A |
test_1  | +-------------------------------+----------------------+----------------------+
test_1  |
test_1  | +-----------------------------------------------------------------------------+
test_1  | | Processes:                                                                  |
test_1  | |  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
test_1  | |        ID   ID                                                   Usage      |
test_1  | |=============================================================================|
test_1  | |  No running processes found                                                 |
test_1  | +-----------------------------------------------------------------------------+
gpu_test_1 exited with code 0
```

On machines hosting multiple GPUs, the `device_ids` field can be set to target specific GPU devices and `count` can be used to limit the number of GPU devices assigned to a service container.

You can use `count` or `device_ids` in each of your service definitions. An error is returned if you try to combine both, specify an invalid device ID, or use a value of count that’s higher than the number of GPUs in your system.

```console
$ nvidia-smi
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 450.80.02    Driver Version: 450.80.02    CUDA Version: 11.0     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  Tesla T4            On   | 00000000:00:1B.0 Off |                    0 |
| N/A   72C    P8    12W /  70W |      0MiB / 15109MiB |      0%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
|   1  Tesla T4            On   | 00000000:00:1C.0 Off |                    0 |
| N/A   67C    P8    11W /  70W |      0MiB / 15109MiB |      0%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
|   2  Tesla T4            On   | 00000000:00:1D.0 Off |                    0 |
| N/A   74C    P8    12W /  70W |      0MiB / 15109MiB |      0%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
|   3  Tesla T4            On   | 00000000:00:1E.0 Off |                    0 |
| N/A   62C    P8    11W /  70W |      0MiB / 15109MiB |      0%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
```

## Access specific devices

To allow access only to GPU-0 and GPU-3 devices:

```yaml
services:
  test:
    image: tensorflow/tensorflow:latest-gpu
    command: python -c "import tensorflow as tf;tf.test.gpu_device_name()"
    deploy:
      resources:
        reservations:
          devices:
          - driver: nvidia
            device_ids: ['0', '3']
            capabilities: [gpu]
```

---

# Using lifecycle hooks with Compose

> Learn how to use Docker Compose lifecycle hooks like post_start and pre_stop to customize container behavior.

# Using lifecycle hooks with Compose

   Table of contents

---

Requires: Docker Compose [2.30.0](https://github.com/docker/compose/releases/tag/v2.30.0) and later

## Services lifecycle hooks

When Docker Compose runs a container, it uses two elements,
[ENTRYPOINT and COMMAND](https://docs.docker.com/engine/containers/run/#default-command-and-options),
to manage what happens when the container starts and stops.

However, it can sometimes be easier to handle these tasks separately with lifecycle hooks -
commands that run right after the container starts or just before it stops.

Lifecycle hooks are particularly useful because they can have special privileges
(like running as the root user), even when the container itself runs with lower privileges
for security. This means that certain tasks requiring higher permissions can be done without
compromising the overall security of the container.

### Post-start hooks

Post-start hooks are commands that run after the container has started, but there's no
set time for when exactly they will execute. The hook execution timing is not assured during
the execution of the container's `entrypoint`.

In the example provided:

- The hook is used to change the ownership of a volume to a non-root user (because volumes
  are created with root ownership by default).
- After the container starts, the `chown` command changes the ownership of the `/data` directory to user `1001`.

```yaml
services:
  app:
    image: backend
    user: 1001
    volumes:
      - data:/data
    post_start:
      - command: chown -R /data 1001:1001
        user: root

volumes:
  data: {} # a Docker volume is created with root ownership
```

### Pre-stop hooks

Pre-stop hooks are commands that run before the container is stopped by a specific
command (like `docker compose down` or stopping it manually with `Ctrl+C`).
These hooks won't run if the container stops by itself or gets killed suddenly.

In the following example, before the container stops, the `./data_flush.sh` script is
run to perform any necessary cleanup.

```yaml
services:
  app:
    image: backend
    pre_stop:
      - command: ./data_flush.sh
```

## Reference information

- [post_start](https://docs.docker.com/reference/compose-file/services/#post_start)
- [pre_stop](https://docs.docker.com/reference/compose-file/services/#pre_stop)

---

# Extend your Compose file

> Learn how to reuse service configurations across files and projects using Docker Compose’s extends attribute.

# Extend your Compose file

   Table of contents

---

Docker Compose's
[extendsattribute](https://docs.docker.com/reference/compose-file/services/#extends)
lets you share common configurations among different files, or even different
projects entirely.

Extending services is useful if you have several services that reuse a common
set of configuration options. With `extends` you can define a common set of
service options in one place and refer to it from anywhere. You can refer to
another Compose file and select a service you want to also use in your own
application, with the ability to override some attributes for your own needs.

> Important
>
> When you use multiple Compose files, you must make sure all paths in the files
> are relative to the base Compose file (i.e. the Compose file in your main-project folder). This is required because extend files
> need not be valid Compose files. Extend files can contain small fragments of
> configuration. Tracking which fragment of a service is relative to which path is
> difficult and confusing, so to keep paths easier to understand, all paths must
> be defined relative to the base file.

## How theextendsattribute works

### Extending services from another file

Take the following example:

```yaml
services:
  web:
    extends:
      file: common-services.yml
      service: webapp
```

This instructs Compose to re-use only the properties of the `webapp` service
defined in the `common-services.yml` file. The `webapp` service itself is not part of the final project.

If `common-services.yml`
looks like this:

```yaml
services:
  webapp:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - "/data"
```

You get exactly the same result as if you wrote
`compose.yaml` with the same `build`, `ports`, and `volumes` configuration
values defined directly under `web`.

To include the service `webapp` in the final project when extending services from another file, you need to explicitly include both services in your current Compose file. For example (this is for illustrative purposes only):

```yaml
services:
  web:
    build: alpine
    command: echo
    extends:
      file: common-services.yml
      service: webapp
  webapp:
    extends:
      file: common-services.yml
      service: webapp
```

Alternatively, you can use [include](https://docs.docker.com/compose/how-tos/multiple-compose-files/include/).

### Extending services within the same file

If you define services in the same Compose file and extend one service from another, both the original service and the extended service will be part of your final configuration. For example:

```yaml
services:
  web:
    build: alpine
    extends: webapp
  webapp:
    environment:
      - DEBUG=1
```

### Extending services within the same file and from another file

You can go further and define, or re-define, configuration locally in
`compose.yaml`:

```yaml
services:
  web:
    extends:
      file: common-services.yml
      service: webapp
    environment:
      - DEBUG=1
    cpu_shares: 5

  important_web:
    extends: web
    cpu_shares: 10
```

## Additional example

Extending an individual service is useful when you have multiple services that
have a common configuration. The example below is a Compose app with two
services, a web application and a queue worker. Both services use the same
codebase and share many configuration options.

The `common.yaml` file defines the common configuration:

```yaml
services:
  app:
    build: .
    environment:
      CONFIG_FILE_PATH: /code/config
      API_KEY: xxxyyy
    cpu_shares: 5
```

The `compose.yaml` defines the concrete services which use the common
configuration:

```yaml
services:
  webapp:
    extends:
      file: common.yaml
      service: app
    command: /code/run_web_app
    ports:
      - 8080:8080
    depends_on:
      - queue
      - db

  queue_worker:
    extends:
      file: common.yaml
      service: app
    command: /code/run_worker
    depends_on:
      - queue
```

## Relative paths

When using `extends` with a `file` attribute which points to another folder, relative paths
declared by the service being extended are converted so they still point to the
same file when used by the extending service. This is illustrated in the following example:

Base Compose file:

```yaml
services:
  webapp:
    image: example
    extends:
      file: ../commons/compose.yaml
      service: base
```

The `commons/compose.yaml` file:

```yaml
services:
  base:
    env_file: ./container.env
```

The resulting service refers to the original `container.env` file
within the `commons` directory. This can be confirmed with `docker compose config`
which inspects the actual model:

```yaml
services:
  webapp:
    image: example
    env_file:
      - ../commons/container.env
```

## Reference information

- [extends](https://docs.docker.com/reference/compose-file/services/#extends)

---

# Include

> How to use Docker Compose's include top-level element

# Include

   Table of contents

---

Requires: Docker Compose [2.20.3](https://github.com/docker/compose/releases/tag/v2.20.3) and later

With `include`, you can incorporate a separate `compose.yaml` file directly in your current `compose.yaml` file. This makes it easy to modularize complex applications into sub-Compose files, which in turn enables application configurations to be made simpler and more explicit.

The
[includetop-level element](https://docs.docker.com/reference/compose-file/include/) helps to reflect the engineering team responsible for the code directly in the config file's organization. It also solves the relative path problem that [extends](https://docs.docker.com/compose/how-tos/multiple-compose-files/extends/) and [merge](https://docs.docker.com/compose/how-tos/multiple-compose-files/merge/) present.

Each path listed in the `include` section loads as an individual Compose application model, with its own project directory, in order to resolve relative paths.

Once the included Compose application loads, all resources are copied into the current Compose application model.

> Note
>
> `include` applies recursively so an included Compose file which declares its own `include` section, causes those files to also be included.

## Example

```yaml
include:
  - my-compose-include.yaml  #with serviceB declared
services:
  serviceA:
    build: .
    depends_on:
      - serviceB #use serviceB directly as if it was declared in this Compose file
```

`my-compose-include.yaml` manages `serviceB` which details some replicas, web UI to inspect data, isolated networks, volumes for data persistence, etc. The application relying on `serviceB` doesn’t need to know about the infrastructure details, and consumes the Compose file as a building block it can rely on.

This means the team managing `serviceB` can refactor its own database component to introduce additional services without impacting any dependent teams. It also means that the dependent teams don't need to include additional flags on each Compose command they run.

```yaml
include:
  - oci://docker.io/username/my-compose-app:latest # use a Compose file stored as an OCI artifact
services:
  serviceA:
    build: .
    depends_on:
      - serviceB
```

`include` allows you to reference Compose files from remote sources, such as OCI artifacts or Git repositories.
Here `serviceB` is defined in a Compose file stored on Docker Hub.

## Using overrides with included Compose files

Compose reports an error if any resource from `include` conflicts with resources from the included Compose file. This rule prevents
unexpected conflicts with resources defined by the included compose file author. However, there may be some circumstances where you might want to customize the
included model. This can be achieved by adding an override file to the include directive:

```yaml
include:
  - path :
      - third-party/compose.yaml
      - override.yaml  # local override for third-party model
```

The main limitation with this approach is that you need to maintain a dedicated override file per include. For complex projects with multiple
includes this would result in many Compose files.

The other option is to use a `compose.override.yaml` file. While conflicts will be rejected from the file using `include` when same
resource is declared, a global Compose override file can override the resulting merged model, as demonstrated in following example:

Main `compose.yaml` file:

```yaml
include:
  - team-1/compose.yaml # declare service-1
  - team-2/compose.yaml # declare service-2
```

Override `compose.override.yaml` file:

```yaml
services:
  service-1:
    # override included service-1 to enable debugger port
    ports:
      - 2345:2345

  service-2:
    # override included service-2 to use local data folder containing test data
    volumes:
      - ./data:/data
```

Combined together, this allows you to benefit from third-party reusable components, and adjust the Compose model for your needs.

## Reference information

[includetop-level element](https://docs.docker.com/reference/compose-file/include/)

---

# Merge Compose files

> How merging Compose files works

# Merge Compose files

   Table of contents

---

Docker Compose lets you merge and override a set of Compose files together to create a composite Compose file.

By default, Compose reads two files, a `compose.yaml` and an optional
`compose.override.yaml` file. By convention, the `compose.yaml`
contains your base configuration. The override file can
contain configuration overrides for existing services or entirely new
services.

If a service is defined in both files, Compose merges the configurations using
the rules described below and in the
[Compose Specification](https://docs.docker.com/reference/compose-file/merge/).

## How to merge multiple Compose files

To use multiple override files, or an override file with a different name, you
can either use the pre-defined [COMPOSE_FILE](https://docs.docker.com/compose/how-tos/environment-variables/envvars/#compose_file) environment variable, or use the `-f` option to specify the list of files.

Compose merges files in
the order they're specified on the command line. Subsequent files may merge, override, or
add to their predecessors.

For example:

```console
$ docker compose -f compose.yaml -f compose.admin.yaml run backup_db
```

The `compose.yaml` file might specify a `webapp` service.

```yaml
webapp:
  image: examples/web
  ports:
    - "8000:8000"
  volumes:
    - "/data"
```

The `compose.admin.yaml` may also specify this same service:

```yaml
webapp:
  environment:
    - DEBUG=1
```

Any matching
fields override the previous file. New values, add to the `webapp` service
configuration:

```yaml
webapp:
  image: examples/web
  ports:
    - "8000:8000"
  volumes:
    - "/data"
  environment:
    - DEBUG=1
```

## Merging rules

- Paths are evaluated relative to the base file. When you use multiple Compose files, you must make sure all paths in the files are relative to the base Compose file (the first Compose file specified
  with `-f`). This is required because override files need not be valid
  Compose files. Override files can contain small fragments of configuration.
  Tracking which fragment of a service is relative to which path is difficult and
  confusing, so to keep paths easier to understand, all paths must be defined
  relative to the base file.
  > Tip
  >
  > You can use `docker compose config` to review your merged configuration and avoid path-related issues.
- Compose copies configurations from the original service over to the local one.
  If a configuration option is defined in both the original service and the local
  service, the local value replaces or extends the original value.
  - For single-value options like `image`, `command` or `mem_limit`, the new value replaces the old value.
    original service:
    ```yaml
    services:
      myservice:
        # ...
        command: python app.py
    ```
    local service:
    ```yaml
    services:
      myservice:
        # ...
        command: python otherapp.py
    ```
    result:
    ```yaml
    services:
      myservice:
        # ...
        command: python otherapp.py
    ```
  - For the multi-value options `ports`, `expose`, `external_links`, `dns`, `dns_search`, and `tmpfs`, Compose concatenates both sets of values:
    original service:
    ```yaml
    services:
      myservice:
        # ...
        expose:
          - "3000"
    ```
    local service:
    ```yaml
    services:
      myservice:
        # ...
        expose:
          - "4000"
          - "5000"
    ```
    result:
    ```yaml
    services:
      myservice:
        # ...
        expose:
          - "3000"
          - "4000"
          - "5000"
    ```
  - In the case of `environment`, `labels`, `volumes`, and `devices`, Compose "merges" entries together with locally defined values taking precedence. For `environment` and `labels`, the environment variable or label name determines which value is used:
    original service:
    ```yaml
    services:
      myservice:
        # ...
        environment:
          - FOO=original
          - BAR=original
    ```
    local service:
    ```yaml
    services:
      myservice:
        # ...
        environment:
          - BAR=local
          - BAZ=local
    ```
    result:
    ```yaml
    services:
      myservice:
        # ...
        environment:
          - FOO=original
          - BAR=local
          - BAZ=local
    ```
  - Entries for `volumes` and `devices` are merged using the mount path in the container:
    original service:
    ```yaml
    services:
      myservice:
        # ...
        volumes:
          - ./original:/foo
          - ./original:/bar
    ```
    local service:
    ```yaml
    services:
      myservice:
        # ...
        volumes:
          - ./local:/bar
          - ./local:/baz
    ```
    result:
    ```yaml
    services:
      myservice:
        # ...
        volumes:
          - ./original:/foo
          - ./local:/bar
          - ./local:/baz
    ```

For more merging rules, see
[Merge and override](https://docs.docker.com/reference/compose-file/merge/) in the Compose Specification.

### Additional information

- Using `-f` is optional. If not provided, Compose searches the working directory and its parent directories for a `compose.yaml` and a `compose.override.yaml` file. You must supply at least the `compose.yaml` file. If both files exist on the same directory level, Compose combines them into a single configuration.
- You can use a `-f` with `-` (dash) as the filename to read the configuration from `stdin`. For example:
  ```console
  $ docker compose -f - <<EOF
    webapp:
      image: examples/web
      ports:
       - "8000:8000"
      volumes:
       - "/data"
      environment:
       - DEBUG=1
    EOF
  ```
  When `stdin` is used, all paths in the configuration are relative to the current working directory.
- You can use the `-f` flag to specify a path to a Compose file that is not located in the current directory, either from the command line or by setting up a [COMPOSE_FILE environment variable](https://docs.docker.com/compose/how-tos/environment-variables/envvars/#compose_file) in your shell or in an environment file.
  For example, if you are running the [Compose Rails sample](https://github.com/docker/awesome-compose/tree/master/official-documentation-samples/rails/README.md), and have a `compose.yaml` file in a directory called `sandbox/rails`. You can use a command like
  [docker compose pull](https://docs.docker.com/reference/cli/docker/compose/pull/) to get the postgres image for the `db` service from anywhere by using the `-f` flag as follows: `docker compose -f ~/sandbox/rails/compose.yaml pull db`
  Here's the full example:
  ```console
  $ docker compose -f ~/sandbox/rails/compose.yaml pull db
  Pulling db (postgres:18)...
  18: Pulling from library/postgres
  ef0380f84d05: Pull complete
  50cf91dc1db8: Pull complete
  d3add4cd115c: Pull complete
  467830d8a616: Pull complete
  089b9db7dc57: Pull complete
  6fba0a36935c: Pull complete
  81ef0e73c953: Pull complete
  338a6c4894dc: Pull complete
  15853f32f67c: Pull complete
  044c83d92898: Pull complete
  17301519f133: Pull complete
  dcca70822752: Pull complete
  cecf11b8ccf3: Pull complete
  Digest: sha256:1364924c753d5ff7e2260cd34dc4ba05ebd40ee8193391220be0f9901d4e1651
  Status: Downloaded newer image for postgres:18
  ```

## Example

A common use case for multiple files is changing a development Compose app
for a production-like environment (which may be production, staging or CI).
To support these differences, you can split your Compose configuration into
a few different files:

Start with a base file that defines the canonical configuration for the
services.

`compose.yaml`

```yaml
services:
  web:
    image: example/my_web_app:latest
    depends_on:
      - db
      - cache

  db:
    image: postgres:18

  cache:
    image: redis:latest
```

In this example the development configuration exposes some ports to the
host, mounts our code as a volume, and builds the web image.

`compose.override.yaml`

```yaml
services:
  web:
    build: .
    volumes:
      - '.:/code'
    ports:
      - 8883:80
    environment:
      DEBUG: 'true'

  db:
    command: '-d'
    ports:
     - 5432:5432

  cache:
    ports:
      - 6379:6379
```

When you run `docker compose up` it reads the overrides automatically.

To use this Compose app in a production environment, another override file is created, which might be stored in a different git
repository or managed by a different team.

`compose.prod.yaml`

```yaml
services:
  web:
    ports:
      - 80:80
    environment:
      PRODUCTION: 'true'

  cache:
    environment:
      TTL: '500'
```

To deploy with this production Compose file you can run

```console
$ docker compose -f compose.yaml -f compose.prod.yaml up -d
```

This deploys all three services using the configuration in
`compose.yaml` and `compose.prod.yaml` but not the
dev configuration in `compose.override.yaml`.

For more information, see [Using Compose in production](https://docs.docker.com/compose/how-tos/production/).

## Limitations

Docker Compose supports relative paths for the many resources to be included in the application model: build context for service images, location of file defining environment variables, path to a local directory used in a bind-mounted volume.
With such a constraint, code organization in a monorepo can become hard as a natural choice would be to have dedicated folders per team or component, but then the Compose files relative paths become irrelevant.

## Reference information

- [Merge rules](https://docs.docker.com/reference/compose-file/merge/)

---

# Use multiple Compose files

> General overview for the different ways you can work with multiple compose files in Docker Compose

# Use multiple Compose files

---

This section contains information on the ways you can work with multiple Compose files.

Using multiple Compose files lets you customize a Compose application for different environments or workflows. This is useful for large applications that may use dozens of containers, with ownership distributed across multiple teams. For example, if your organization or team uses a monorepo, each team may have their own “local” Compose file to run a subset of the application. They then need to rely on other teams to provide a reference Compose file that defines the expected way to run their own subset. Complexity moves from the code in to the infrastructure and the configuration file.

The quickest way to work with multiple Compose files is to [merge](https://docs.docker.com/compose/how-tos/multiple-compose-files/merge/) Compose files using the `-f` flag in the command line to list out your desired Compose files. However, [merging rules](https://docs.docker.com/compose/how-tos/multiple-compose-files/merge/#merging-rules) means this can soon get quite complicated.

Docker Compose provides two other options to manage this complexity when working with multiple Compose files. Depending on your project's needs, you can:

- [Extend a Compose file](https://docs.docker.com/compose/how-tos/multiple-compose-files/extends/) by referring to another Compose file and selecting the bits you want to use in your own application, with the ability to override some attributes.
- [Include other Compose files](https://docs.docker.com/compose/how-tos/multiple-compose-files/include/) directly in your Compose file.

---

# Networking in Compose

> How Docker Compose sets up networking between containers

# Networking in Compose

   Table of contents

---

By default Compose sets up a single
[network](https://docs.docker.com/reference/cli/docker/network/create/) for your app. Each
container for a service joins the default network and is both reachable by
other containers on that network, and discoverable by the service's name.

> Note
>
> Your app's network is given a name based on the "project name",
> which is based on the name of the directory it lives in. You can override the
> project name with either the
> [--project-nameflag](https://docs.docker.com/reference/cli/docker/compose/)
> or the [COMPOSE_PROJECT_NAMEenvironment variable](https://docs.docker.com/compose/how-tos/environment-variables/envvars/#compose_project_name).

For example, suppose your app is in a directory called `myapp`, and your `compose.yaml` looks like this:

```yaml
services:
  web:
    build: .
    ports:
      - "8000:8000"
  db:
    image: postgres:18
    ports:
      - "8001:5432"
```

When you run `docker compose up`, the following happens:

1. A network called `myapp_default` is created.
2. A container is created using `web`'s configuration. It joins the network
  `myapp_default` under the name `web`.
3. A container is created using `db`'s configuration. It joins the network
  `myapp_default` under the name `db`.

Each container can now look up the service name `web` or `db` and
get back the appropriate container's IP address. For example, `web`'s
application code could connect to the URL `postgres://db:5432` and start
using the Postgres database.

It is important to note the distinction between `HOST_PORT` and `CONTAINER_PORT`.
In the above example, for `db`, the `HOST_PORT` is `8001` and the container port is
`5432` (postgres default). Networked service-to-service
communication uses the `CONTAINER_PORT`. When `HOST_PORT` is defined,
the service is accessible outside the swarm as well.

Within the `web` container, your connection string to `db` would look like
`postgres://db:5432`, and from the host machine, the connection string would
look like `postgres://{DOCKER_IP}:8001` for example `postgres://localhost:8001` if your container is running locally.

## Update containers on the network

If you make a configuration change to a service and run `docker compose up` to update it, the old container is removed and the new one joins the network under a different IP address but the same name. Running containers can look up that name and connect to the new address, but the old address stops working.

If any containers have connections open to the old container, they are closed. It is a container's responsibility to detect this condition, look up the name again and reconnect.

> Tip
>
> Reference containers by name, not IP, whenever possible. Otherwise you’ll need to constantly update the IP address you use.

## Link containers

Links allow you to define extra aliases by which a service is reachable from another service. They are not required to enable services to communicate. By default, any service can reach any other service at that service's name. In the following example, `db` is reachable from `web` at the hostnames `db` and `database`:

```yaml
services:
  web:
    build: .
    links:
      - "db:database"
  db:
    image: postgres:18
```

See the
[links reference](https://docs.docker.com/reference/compose-file/services/#links) for more information.

## Multi-host networking

When deploying a Compose application on a Docker Engine with
[Swarm mode enabled](https://docs.docker.com/engine/swarm/),
you can make use of the built-in `overlay` driver to enable multi-host communication.

Overlay networks are always created as `attachable`. You can optionally set the
[attachable](https://docs.docker.com/reference/compose-file/networks/#attachable) property to `false`.

Consult the
[Swarm mode section](https://docs.docker.com/engine/swarm/) to see how to set up
a Swarm cluster, and the
[overlay network driver documentation](https://docs.docker.com/engine/network/drivers/overlay/)
to learn about multi-host overlay networks.

## Specify custom networks

Instead of just using the default app network, you can specify your own networks with the top-level `networks` key. This lets you create more complex topologies and specify
[custom network drivers](https://docs.docker.com/engine/extend/plugins_network/) and options. You can also use it to connect services to externally-created networks which aren't managed by Compose.

Each service can specify what networks to connect to with the service-level `networks` key, which is a list of names referencing entries under the top-level `networks` key.

The following example shows a Compose file which defines two custom networks. The `proxy` service is isolated from the `db` service, because they do not share a network in common. Only `app` can talk to both.

```yaml
services:
  proxy:
    build: ./proxy
    networks:
      - frontend
  app:
    build: ./app
    networks:
      - frontend
      - backend
  db:
    image: postgres:18
    networks:
      - backend

networks:
  frontend:
    # Specify driver options
    driver: bridge
    driver_opts:
      com.docker.network.bridge.host_binding_ipv4: "127.0.0.1"
  backend:
    # Use a custom driver
    driver: custom-driver
```

Networks can be configured with static IP addresses by setting the
[ipv4_address and/or ipv6_address](https://docs.docker.com/reference/compose-file/services/#ipv4_address-ipv6_address) for each attached network.

Networks can also be given a
[custom name](https://docs.docker.com/reference/compose-file/networks/#name):

```yaml
services:
  # ...
networks:
  frontend:
    name: custom_frontend
    driver: custom-driver-1
```

## Configure the default network

Instead of, or as well as, specifying your own networks, you can also change the settings of the app-wide default network by defining an entry under `networks` named `default`:

```yaml
services:
  web:
    build: .
    ports:
      - "8000:8000"
  db:
    image: postgres:18

networks:
  default:
    # Use a custom driver
    driver: custom-driver-1
```

## Use an existing network

If you've manually created a bridge network outside of Compose using the `docker network create` command, you can connect your Compose services to it by marking the network as `external`.

If you want your containers to join a pre-existing network, use the
[externaloption](https://docs.docker.com/reference/compose-file/networks/#external)

```yaml
services:
  # ...
networks:
  network1:
    name: my-pre-existing-network
    external: true
```

Instead of attempting to create a network called `[projectname]_default`, Compose looks for a network called `my-pre-existing-network` and connects your app's containers to it.

## Further reference information

For full details of the network configuration options available, see the following references:

- [Top-levelnetworkselement](https://docs.docker.com/reference/compose-file/networks/)
- [Service-levelnetworksattribute](https://docs.docker.com/reference/compose-file/services/#networks)

---

# Package and deploy Docker Compose applications as OCI artifacts

> Learn how to package, publish, and securely run Docker Compose applications from OCI-compliant registries.

# Package and deploy Docker Compose applications as OCI artifacts

   Table of contents

---

Requires: Docker Compose [2.34.0](https://github.com/docker/compose/releases/tag/v2.34.0) and later

Docker Compose supports working with
[OCI artifacts](https://docs.docker.com/docker-hub/repos/manage/hub-images/oci-artifacts/), allowing you to package and distribute your Compose applications through container registries. This means you can store your Compose files alongside your container images, making it easier to version, share, and deploy your multi-container applications.

## Publish your Compose application as an OCI artifact

To distribute your Compose application as an OCI artifact, you can use the `docker compose publish` command, to publish it to an OCI-compliant registry.
This allows others to then deploy your application directly from the registry.

The publish function supports most of the composition capabilities of Compose, like overrides, extends or include, [with some limitations](#limitations).

### General steps

1. Navigate to your Compose application's directory.
  Ensure you're in the directory containing your `compose.yml` file or that you are specifying your Compose file with the `-f` flag.
2. In your terminal, sign in to your Docker account so you're authenticated with Docker Hub.
  ```console
  $ docker login
  ```
3. Use the `docker compose publish` command to push your application as an OCI artifact:
  ```console
  $ docker compose publish username/my-compose-app:latest
  ```
  If you have multiple Compose files, run:
  ```console
  $ docker compose -f compose-base.yml -f compose-production.yml publish username/my-compose-app:latest
  ```

### Advanced publishing options

When publishing, you can pass additional options:

- `--oci-version`: Specify the OCI version (default is automatically determined).
- `--resolve-image-digests`: Pin image tags to digests.
- `--with-env`: Include environment variables in the published OCI artifact.

Compose checks to make sure there isn't any sensitive data in your configuration and displays your environment variables to confirm you want to publish them.

```text
...
you are about to publish sensitive data within your OCI artifact.
please double check that you are not leaking sensitive data
AWS Client ID
"services.serviceA.environment.AWS_ACCESS_KEY_ID": xxxxxxxxxx
AWS Secret Key
"services.serviceA.environment.AWS_SECRET_ACCESS_KEY": aws"xxxx/xxxx+xxxx+"
Github authentication
"GITHUB_TOKEN": ghp_xxxxxxxxxx
JSON Web Token
"": xxxxxxx.xxxxxxxx.xxxxxxxx
Private Key
"": -----BEGIN DSA PRIVATE KEY-----
xxxxx
-----END DSA PRIVATE KEY-----
Are you ok to publish these sensitive data? [y/N]:y

you are about to publish environment variables within your OCI artifact.
please double check that you are not leaking sensitive data
Service/Config  serviceA
FOO=bar
Service/Config  serviceB
FOO=bar
QUIX=
BAR=baz
Are you ok to publish these environment variables? [y/N]:
```

If you decline, the publish process stops without sending anything to the registry.

## Limitations

There are limitations to publishing Compose applications as OCI artifacts. You can't publish a Compose configuration:

- With service(s) containing bind mounts
- With service(s) containing only a `build` section
- That includes local files with the `include` attribute. To publish successfully, ensure that any included local files are also published. You can then use `include` to reference these files as remote `include` is supported.

## Start an OCI artifact application

To start a Docker Compose application that uses an OCI artifact, you can use the `-f` (or `--file`) flag followed by the OCI artifact reference. This allows you to specify a Compose file stored as an OCI artifact in a registry.

The `oci://` prefix indicates that the Compose file should be pulled from an OCI-compliant registry rather than loaded from the local filesystem.

```console
$ docker compose -f oci://docker.io/username/my-compose-app:latest up
```

To then run the Compose application, use the `docker compose up` command with the `-f` flag pointing to your OCI artifact:

```console
$ docker compose -f oci://docker.io/username/my-compose-app:latest up
```

### Troubleshooting

When you run an application from an OCI artifact, Compose may display warning messages that require you to confirm the following so as to limit the risk of running a malicious application:

- A list of the interpolation variables used along with their values
- A list of all environment variables used by the application
- If your OCI artifact application is using another remote resources, for example via
  [include](https://docs.docker.com/reference/compose-file/include/).

```text
$ REGISTRY=myregistry.com docker compose -f oci://docker.io/username/my-compose-app:latest up

Found the following variables in configuration:
VARIABLE     VALUE                SOURCE        REQUIRED    DEFAULT
REGISTRY     myregistry.com      command-line   yes
TAG          v1.0                environment    no          latest
DOCKERFILE   Dockerfile          default        no          Dockerfile
API_KEY      <unset>             none           no

Do you want to proceed with these variables? [Y/n]:y

Warning: This Compose project includes files from remote sources:
- oci://registry.example.com/stack:latest
Remote includes could potentially be malicious. Make sure you trust the source.
Do you want to continue? [y/N]:
```

If you agree to start the application, Compose displays the directory where all the resources from the OCI artifact have been downloaded:

```text
...
Do you want to continue? [y/N]: y

Your compose stack "oci://registry.example.com/stack:latest" is stored in "~/Library/Caches/docker-compose/964e715660d6f6c3b384e05e7338613795f7dcd3613890cfa57e3540353b9d6d"
```

The `docker compose publish` command supports non-interactive execution, letting you skip the confirmation prompt by including the `-y` (or `--yes`) flag:

```console
$ docker compose publish -y username/my-compose-app:latest
```

## Next steps

- [Learn about OCI artifacts in Docker Hub](https://docs.docker.com/docker-hub/repos/manage/hub-images/oci-artifacts/)
- [Compose publish command](https://docs.docker.com/reference/cli/docker/compose/publish/)
- [Understandinclude](https://docs.docker.com/reference/compose-file/include/)

---

# Use Compose in production

> Learn how to configure, deploy, and update Docker Compose applications for production environments.

# Use Compose in production

   Table of contents

---

When you define your app with Compose in development, you can use this
definition to run your application in different environments such as CI,
staging, and production.

The easiest way to deploy an application is to run it on a single server,
similar to how you would run your development environment. If you want to scale
up your application, you can run Compose apps on a Swarm cluster.

### Modify your Compose file for production

You may need to make changes to your app configuration to make it ready for
production. These changes might include:

- Removing any volume bindings for application code, so that code stays inside
  the container and can't be changed from outside
- Binding to different ports on the host
- Setting environment variables differently, such as reducing the verbosity of
  logging, or to specify settings for external services such as an email server
- Specifying a restart policy like
  [restart: always](https://docs.docker.com/reference/compose-file/services/#restart)to avoid downtime
- Adding extra services such as a log aggregator

For this reason, consider defining an additional Compose file, for example
`compose.production.yaml`, with production-specific
configuration details. This configuration file only needs to include the changes you want to make from the original Compose file. The additional Compose file
is then applied over the original `compose.yaml` to create a new configuration.

Once you have a second configuration file, you can use it with the
`-f` option:

```console
$ docker compose -f compose.yaml -f compose.production.yaml up -d
```

See [Using multiple compose files](https://docs.docker.com/compose/how-tos/multiple-compose-files/) for a more complete example, and other options.

### Deploying changes

When you make changes to your app code, remember to rebuild your image and
recreate your app's containers. To redeploy a service called
`web`, use:

```console
$ docker compose build web
$ docker compose up --no-deps -d web
```

This first command rebuilds the image for `web` and then stops, destroys, and recreates
just the `web` service. The `--no-deps` flag prevents Compose from also
recreating any services that `web` depends on.

### Running Compose on a single server

You can use Compose to deploy an app to a remote Docker host by setting the
`DOCKER_HOST`, `DOCKER_TLS_VERIFY`, and `DOCKER_CERT_PATH` environment variables
appropriately. For more information, see [pre-defined environment variables](https://docs.docker.com/compose/how-tos/environment-variables/envvars/).

Once you've set up your environment variables, all the normal `docker compose`
commands work with no further configuration.

## Next steps

- [Using multiple Compose files](https://docs.docker.com/compose/how-tos/multiple-compose-files/)
