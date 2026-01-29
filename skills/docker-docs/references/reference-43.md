# Fragments and more

# Fragments

> Reuse configuration with YAML anchors and fragments

# Fragments

   Table of contents

---

With Compose, you can use built-in [YAML](https://www.yaml.org/spec/1.2/spec.html#id2765878) features to make your Compose file neater and more efficient. Anchors and aliases let you create re-usable blocks. This is useful if you start to find common configurations that span multiple services. Having re-usable blocks minimizes potential mistakes.

Anchors are created using the `&` sign. The sign is followed by an alias name. You can use this alias with the `*` sign later to reference the value following the anchor. Make sure there is no space between the `&` and the `*` characters and the following alias name.

You can use more than one anchor and alias in a single Compose file.

## Example 1

```yml
volumes:
  db-data: &default-volume
    driver: default
  metrics: *default-volume
```

In the example above, a `default-volume` anchor is created based on the `db-data` volume. It is later reused by the alias `*default-volume` to define the `metrics` volume.

Anchor resolution takes place before [variables interpolation](https://docs.docker.com/reference/compose-file/interpolation/), so variables can't be used to set anchors or aliases.

## Example 2

```yml
services:
  first:
    image: my-image:latest
    environment: &env
      - CONFIG_KEY
      - EXAMPLE_KEY
      - DEMO_VAR
  second:
    image: another-image:latest
    environment: *env
```

If you have an anchor that you want to use in more than one service, use it in conjunction with an [extension](https://docs.docker.com/reference/compose-file/extension/) to make your Compose file easier to maintain.

## Example 3

You may want to partially override values. Compose follows the rule outlined by [YAML merge type](https://yaml.org/type/merge.html).

In the following example, `metrics` volume specification uses alias
to avoid repetition but overrides `name` attribute:

```yml
services:
  backend:
    image: example/database
    volumes:
      - db-data
      - metrics
volumes:
  db-data: &default-volume
    driver: default
    name: "data"
  metrics:
    <<: *default-volume
    name: "metrics"
```

## Example 4

You can also extend the anchor to add additional values.

```yml
services:
  first:
    image: my-image:latest
    environment: &env
      FOO: BAR
      ZOT: QUIX
  second:
    image: another-image:latest
    environment:
      <<: *env
      YET_ANOTHER: VARIABLE
```

> Note
>
> [YAML merge](https://yaml.org/type/merge.html) only applies to mappings, and can't be used with sequences.

In example above, the environment variables must be declared using the `FOO: BAR` mapping syntax, while the sequence syntax `- FOO=BAR` is only valid when no fragments are involved.

---

# Use include to modularize Compose files

> Reference external Compose files using the include top-level element

# Use include to modularize Compose files

   Table of contents

---

Requires: Docker Compose [2.20.0](https://github.com/docker/compose/releases/tag/v2.20.0) and later

You can reuse and modularize Docker Compose configurations by including other Compose files. This is useful if:

- You want to reuse other Compose files.
- You need to factor out parts of your application model into separate Compose files so they can be managed separately or shared with others.
- Teams need to maintain a Compose file with only necessary complexity for the limited amount of resources it has to declare for its own sub-domain within a larger deployment.

The `include` top-level section is used to define the dependency on another Compose application, or sub-domain.
Each path listed in the `include` section is loaded as an individual Compose application model, with its own project directory, in order to resolve relative paths.

Once the included Compose application is loaded, all resource definitions are copied into the
current Compose application model. Compose displays a warning if resource names conflict and doesn't
try to merge them. To enforce this, `include` is evaluated after the Compose file(s) selected
to define the Compose application model have been parsed and merged, so that conflicts
between Compose files are detected.

`include` applies recursively so an included Compose file which declares its own `include` section triggers those other files to be included as well.

Any volumes, networks, or other resources pulled in from the included Compose file can be used by the current Compose application for cross-service references. For example:

```yaml
include:
  - my-compose-include.yaml  #with serviceB declared
services:
  serviceA:
    build: .
    depends_on:
      - serviceB #use serviceB directly as if it was declared in this Compose file
```

Compose also supports the use of interpolated variables with `include`. It's recommended that you [specify mandatory variables](https://docs.docker.com/reference/compose-file/interpolation/). For example:

```text
include:
  -${INCLUDE_PATH:?FOO}/compose.yaml
```

## Short syntax

The short syntax only defines paths to other Compose files. The file is loaded with the parent
folder as the project directory, and an optional `.env` file that is loaded to define any variables' default values
by interpolation. The local project's environment can override those values.

```yaml
include:
  - ../commons/compose.yaml
  - ../another_domain/compose.yaml

services:
  webapp:
    depends_on:
      - included-service # defined by another_domain
```

In the previous example, both `../commons/compose.yaml` and
`../another_domain/compose.yaml` are loaded as individual Compose projects. Relative paths
in Compose files being referred by `include` are resolved relative to their own Compose
file path, not based on the local project's directory. Variables are interpolated using values set in the optional
`.env` file in same folder and are overridden by the local project's environment.

## Long syntax

The long syntax offers more control over the sub-project parsing:

```yaml
include:
   - path: ../commons/compose.yaml
     project_directory: ..
     env_file: ../another/.env
```

### path

`path` is required and defines the location of the Compose file(s) to be parsed and included into the
local Compose model.

`path` can be set as:

- A string: When using a single Compose file.
- A list of strings: When multiple Compose files need to be [merged together](https://docs.docker.com/reference/compose-file/merge/) to define the Compose model for the local application.

```yaml
include:
   - path:
       - ../commons/compose.yaml
       - ./commons-override.yaml
```

### project_directory

`project_directory` defines a base path to resolve relative paths set in the Compose file. It defaults to
the directory of the included Compose file.

### env_file

`env_file` defines an environment file(s) to use to define default values when interpolating variables
in the Compose file being parsed. It defaults to `.env` file in the `project_directory` for the Compose
file being parsed.

`env_file` can be set to either a string or a list of strings when multiple environment files need to be merged
to define a project environment.

```yaml
include:
   - path: ../another/compose.yaml
     env_file:
       - ../another/.env
       - ../another/dev.env
```

The local project's environment has precedence over the values set by the Compose file, so that the local project can
override values for customization.

## Additional resources

For more information on using `include`, see
[Working with multiple Compose files](https://docs.docker.com/compose/how-tos/multiple-compose-files/)

---

# Interpolation

> Substitute environment variables in Docker Compose files using interpolation syntax.

# Interpolation

---

Values in a Compose file can be set by variables and interpolated at runtime. Compose files use a Bash-like
syntax `${VARIABLE}`. Both `$VARIABLE` and `${VARIABLE}` syntax is supported.

For braced expressions, the following formats are supported:

- Direct substitution
  - `${VAR}` -> value of `VAR`
- Default value
  - `${VAR:-default}` -> value of `VAR` if set and non-empty, otherwise `default`
  - `${VAR-default}` -> value of `VAR` if set, otherwise `default`
- Required value
  - `${VAR:?error}` -> value of `VAR` if set and non-empty, otherwise exit with error
  - `${VAR?error}` -> value of `VAR` if set, otherwise exit with error
- Alternative value
  - `${VAR:+replacement}` -> `replacement` if `VAR` is set and non-empty, otherwise empty
  - `${VAR+replacement}` -> `replacement` if `VAR` is set, otherwise empty

Interpolation can also be nested:

- `${VARIABLE:-${FOO}}`
- `${VARIABLE?$FOO}`
- `${VARIABLE:-${FOO:-default}}`

Other extended shell-style features, such as `${VARIABLE/foo/bar}`, are not
supported by Compose.

Compose processes any string following a `$` sign as long as it makes it
a valid variable definition - either an alphanumeric name (`[_a-zA-Z][_a-zA-Z0-9]*`)
or a braced string starting with `${`. In other circumstances, it will be preserved without attempting to interpolate a value.

You can use a `$$` (double-dollar sign) when your configuration needs a literal
dollar sign. This also prevents Compose from interpolating a value, so a `$$`
allows you to refer to environment variables that you don't want processed by
Compose.

```yml
web:
  build: .
  command: "$$VAR_NOT_INTERPOLATED_BY_COMPOSE"
```

If Compose can't resolve a substituted variable and no default value is defined, it displays a warning and substitutes the variable with an empty string.

As any values in a Compose file can be interpolated with variable substitution, including compact string notation
for complex elements, interpolation is applied before a merge on a per-file basis.

Interpolation applies only to YAML values, not to keys. For the few places where keys are actually arbitrary
user-defined strings, such as [labels](https://docs.docker.com/reference/compose-file/services/#labels) or [environment](https://docs.docker.com/reference/compose-file/services/#environment), an alternate equal sign syntax
must be used for interpolation to apply. For example:

```yml
services:
  foo:
    labels:
      "$VAR_NOT_INTERPOLATED_BY_COMPOSE": "BAR"
```

```yml
services:
  foo:
    labels:
      - "$VAR_INTERPOLATED_BY_COMPOSE=BAR"
```

---

# Legacy versions

# Legacy versions

---

The legacy versions of the Compose file reference has moved to the [V1 branch of the Compose repository](https://github.com/docker/compose/tree/v1/docs). They are no longer being actively maintained.

The latest and recommended version of the Compose file format is defined by the [Compose Specification](https://docs.docker.com/reference/compose-file/). This format merges the 2.x and 3.x versions and is implemented by **Compose 1.27.0+**. For more information, see the
[History and development of Docker Compose](https://docs.docker.com/compose/intro/history/).

---

# Merge Compose files

> Understand how Docker Compose merges multiple files and resolves conflicts

# Merge Compose files

   Table of contents

---

Compose lets you define a Compose application model through multiple Compose files.
When doing so, Compose follows certain rules to merge Compose files.

These rules are outlined below.

## Mapping

A YAML `mapping` gets merged by adding missing entries and merging the conflicting ones.

Merging the following example YAML trees:

```yaml
services:
  foo:
    key1: value1
    key2: value2
```

```yaml
services:
  foo:
    key2: VALUE
    key3: value3
```

Results in a Compose application model equivalent to the YAML tree:

```yaml
services:
  foo:
    key1: value1
    key2: VALUE
    key3: value3
```

## Sequence

A YAML `sequence` is merged by appending values from the overriding Compose file to the previous one.

Merging the following example YAML trees:

```yaml
services:
  foo:
    DNS:
      - 1.1.1.1
```

```yaml
services:
  foo:
    DNS:
      - 8.8.8.8
```

Results in a Compose application model equivalent to the YAML tree:

```yaml
services:
  foo:
    DNS:
      - 1.1.1.1
      - 8.8.8.8
```

## Exceptions

### Shell commands

When merging Compose files that use the services attributes [command](https://docs.docker.com/reference/compose-file/services/#command), [entrypoint](https://docs.docker.com/reference/compose-file/services/#entrypoint) and [healthcheck:test](https://docs.docker.com/reference/compose-file/services/#healthcheck), the value is overridden by the latest Compose file, and not appended.

Merging the following example YAML trees:

```yaml
services:
  foo:
    command: ["echo", "foo"]
```

```yaml
services:
  foo:
    command: ["echo", "bar"]
```

Results in a Compose application model equivalent to the YAML tree:

```yaml
services:
  foo:
    command: ["echo", "bar"]
```

### Unique resources

Applies to the [ports](https://docs.docker.com/reference/compose-file/services/#ports), [volumes](https://docs.docker.com/reference/compose-file/services/#volumes), [secrets](https://docs.docker.com/reference/compose-file/services/#secrets) and [configs](https://docs.docker.com/reference/compose-file/services/#configs) services attributes.
While these types are modeled in a Compose file as a sequence, they have special uniqueness requirements:

| Attribute | Unique key |
| --- | --- |
| volumes | target |
| secrets | target |
| configs | target |
| ports | {ip, target, published, protocol} |

When merging Compose files, Compose appends new entries that do not violate a uniqueness constraint and merge entries that share a unique key.

Merging the following example YAML trees:

```yaml
services:
  foo:
    volumes:
      - foo:/work
```

```yaml
services:
  foo:
    volumes:
      - bar:/work
```

Results in a Compose application model equivalent to the YAML tree:

```yaml
services:
  foo:
    volumes:
      - bar:/work
```

### Reset value

In addition to the previously described mechanism, an override Compose file can also be used to remove elements from your application model.
For this purpose, the custom [YAML tag](https://yaml.org/spec/1.2.2/#24-tags) `!reset` can be set to
override a value set by the overridden Compose file. A valid value for attribute must be provided,
but will be ignored and target attribute will be set with type's default value or `null`.

For readability, it is recommended to explicitly set the attribute value to the null (`null`) or empty
array `[]` (with `!reset null` or `!reset []`) so that it is clear that resulting attribute will be
cleared.

A base `compose.yaml` file:

```yaml
services:
  app:
    image: myapp
    ports:
      - "8080:80"
    environment:
      FOO: BAR
```

And a `compose.override.yaml` file:

```yaml
services:
  app:
    image: myapp
    ports: !reset []
    environment:
      FOO: !reset null
```

Results in:

```yaml
services:
  app:
    image: myapp
```

### Replace value

Requires: Docker Compose [2.24.4](https://github.com/docker/compose/releases/tag/v2.24.4) and later

While `!reset` can be used to remove a declaration from a Compose file using an override file, `!override` allows you
to fully replace an attribute, bypassing the standard merge rules. A typical example is to fully replace a resource definition, to rely on a distinct model but using the same name.

A base `compose.yaml` file:

```yaml
services:
  app:
    image: myapp
    ports:
      - "8080:80"
```

To remove the original port, but expose a new one, the following override file is used:

```yaml
services:
  app:
    ports: !override
      - "8443:443"
```

This results in:

```yaml
services:
  app:
    image: myapp
    ports:
      - "8443:443"
```

If `!override` had not been used, both `8080:80` and `8443:443` would be exposed as per the [merging rules outlined above](#sequence).

## Additional resources

For more information on how merge can be used to create a composite Compose file, see
[Working with multiple Compose files](https://docs.docker.com/compose/how-tos/multiple-compose-files/)

---

# Models

> Learn about the models top-level element

# Models

   Table of contents

---

Requires: Docker Compose [2.38.0](https://github.com/docker/compose/releases/tag/v2.38.0) and later

The top-level `models` section declares AI models that are used by your Compose application. These models are typically pulled as OCI artifacts, run by a model runner, and exposed as an API that your service containers can consume.

Services can only access models when explicitly granted by a [modelsattribute](https://docs.docker.com/reference/compose-file/services/#models) within the `services` top-level element.

## Examples

### Example 1

```yaml
services:
  app:
    image: app
    models:
      - ai_model

models:
  ai_model:
    model: ai/model
```

In this basic example:

- The app service uses the `ai_model`.
- The `ai_model` is defined as an OCI artifact (`ai/model`) that is pulled and served by the model runner.
- Docker Compose injects connection info, for example `AI_MODEL_URL`, into the container.

### Example 2

```yaml
services:
  app:
    image: app
    models:
      my_model:
        endpoint_var: MODEL_URL

models:
  my_model:
    model: ai/model
    context_size: 1024
    runtime_flags:
      - "--a-flag"
      - "--another-flag=42"
```

In this advanced setup:

- The service app references `my_model` using the long syntax.
- Compose injects the model runner's URL as the environment variable `MODEL_URL`.

## Attributes

- `model` (required): The OCI artifact identifier for the model. This is what Compose pulls and runs via the model runner.
- `context_size`: Defines the maximum token context size for the model.
- `runtime_flags`: A list of raw command-line flags passed to the inference engine when the model is started.

## Additional resources

For more examples and information on using `model`, see
[Use AI models in Compose](https://docs.docker.com/ai/compose/models-and-compose/)

---

# Define and manage networks in Docker Compose

> Learn how to configure and control networks using the top-level networks element in Docker Compose.

# Define and manage networks in Docker Compose

   Table of contents

---

Networks let services communicate with each other. By default Compose sets up a single network for your app. Each container for a service joins the default network and is both reachable by other containers on that network, and discoverable by the service's name. The top-level `networks` element lets you configure named networks that can be reused across multiple services.

To use a network across multiple services, you must explicitly grant each service access by using the [networks](https://docs.docker.com/reference/compose-file/services/) attribute within the `services` top-level element. The `networks` top-level element has additional syntax that provides more granular control.

## Examples

### Basic example

In the following example, at runtime, networks `front-tier` and `back-tier` are created and the `frontend` service
is connected to `front-tier` and `back-tier` networks.

```yml
services:
  frontend:
    image: example/webapp
    networks:
      - front-tier
      - back-tier

networks:
  front-tier:
  back-tier:
```

### Advanced example

```yml
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

This example shows a Compose file which defines two custom networks. The `proxy` service is isolated from the `db` service, because they do not share a network in common. Only `app` can talk to both.

## The default network

When a Compose file doesn't declare explicit networks, Compose uses an implicit `default` network. Services without an explicit [networks](https://docs.docker.com/reference/compose-file/services/#networks) declaration are connected by Compose to this `default` network:

```yml
services:
  some-service:
    image: foo
```

This example is actually equivalent to:

```yml
services:
  some-service:
    image: foo
    networks:
      default: {}
networks:
  default: {}
```

You can customize the `default` network with an explicit declaration:

```yml
networks:
  default:
    name: a_network # Use a custom name
    driver_opts:    # pass options to driver for network creation
      com.docker.network.bridge.host_binding_ipv4: 127.0.0.1
```

For options, see the [Docker Engine docs](https://docs.docker.com/engine/network/drivers/bridge/#options).

## Attributes

### attachable

If `attachable` is set to `true`, then standalone containers should be able to attach to this network, in addition to services.
If a standalone container attaches to the network, it can communicate with services and other standalone containers
that are also attached to the network.

```yml
networks:
  mynet1:
    driver: overlay
    attachable: true
```

### driver

`driver` specifies which driver should be used for this network. Compose returns an error if the
driver is not available on the platform.

```yml
networks:
  db-data:
    driver: bridge
```

For more information on drivers and available options, see
[Network drivers](https://docs.docker.com/engine/network/drivers/).

### driver_opts

`driver_opts` specifies a list of options as key-value pairs to pass to the driver. These options are
driver-dependent.

```yml
networks:
  frontend:
    driver: bridge
    driver_opts:
      com.docker.network.bridge.host_binding_ipv4: "127.0.0.1"
```

Consult the
[network drivers documentation](https://docs.docker.com/engine/network/) for more information.

### enable_ipv4

Requires: Docker Compose [2.33.1](https://github.com/docker/compose/releases/tag/v2.33.1) and later

`enable_ipv4` can be used to disable IPv4 address assignment.

```yml
networks:
    ip6net:
      enable_ipv4: false
      enable_ipv6: true
```

### enable_ipv6

`enable_ipv6` enables IPv6 address assignment.

```yml
networks:
    ip6net:
      enable_ipv6: true
```

### external

If set to `true`:

- `external` specifies that this network’s lifecycle is maintained outside of that of the application.
  Compose doesn't attempt to create these networks, and returns an error if one doesn't exist.
- All other attributes apart from name are irrelevant. If Compose detects any other attribute, it rejects the Compose file as invalid.

In the following example, `proxy` is the gateway to the outside world. Instead of attempting to create a network, Compose
queries the platform for an existing network called `outside` and connects the
`proxy` service's containers to it.

```yml
services:
  proxy:
    image: example/proxy
    networks:
      - outside
      - default
  app:
    image: example/app
    networks:
      - default

networks:
  outside:
    external: true
```

### ipam

`ipam` specifies a custom IPAM configuration. This is an object with several properties, each of which is optional:

- `driver`: Custom IPAM driver, instead of the default.
- `config`: A list with zero or more configuration elements, each containing a:
  - `subnet`: Subnet in CIDR format that represents a network segment
  - `ip_range`: Range of IPs from which to allocate container IPs
  - `gateway`: IPv4 or IPv6 gateway for the master subnet
  - `aux_addresses`: Auxiliary IPv4 or IPv6 addresses used by Network driver, as a mapping from hostname to IP
- `options`: Driver-specific options as a key-value mapping.

```yml
networks:
  mynet1:
    ipam:
      driver: default
      config:
        - subnet: 172.28.0.0/16
          ip_range: 172.28.5.0/24
          gateway: 172.28.5.254
          aux_addresses:
            host1: 172.28.1.5
            host2: 172.28.1.6
            host3: 172.28.1.7
      options:
        foo: bar
        baz: "0"
```

### internal

By default, Compose provides external connectivity to networks. `internal`, when set to `true`, lets you
create an externally isolated network.

### labels

Add metadata to containers using `labels`. You can use either an array or a dictionary.

It is recommended that you use reverse-DNS notation to prevent labels from conflicting with those used by other software.

```yml
networks:
  mynet1:
    labels:
      com.example.description: "Financial transaction network"
      com.example.department: "Finance"
      com.example.label-with-empty-value: ""
```

```yml
networks:
  mynet1:
    labels:
      - "com.example.description=Financial transaction network"
      - "com.example.department=Finance"
      - "com.example.label-with-empty-value"
```

Compose sets `com.docker.compose.project` and `com.docker.compose.network` labels.

### name

`name` sets a custom name for the network. The name field can be used to reference networks which contain special characters.
The name is used as is and is not scoped with the project name.

```yml
networks:
  network1:
    name: my-app-net
```

It can also be used in conjunction with the `external` property to define the platform network that Compose
should retrieve, typically by using a parameter so the Compose file doesn't need to hard-code runtime specific values:

```yml
networks:
  network1:
    external: true
    name: "${NETWORK_ID}"
```

## Additional resources

For more examples, see
[Networking in Compose](https://docs.docker.com/compose/how-tos/networking/).

---

# Learn how to use profiles in Docker Compose

> Learn about profiles

# Learn how to use profiles in Docker Compose

   Table of contents

---

With profiles you can define a set of active profiles so your Compose application model is adjusted for various usages and environments.

The [services](https://docs.docker.com/reference/compose-file/services/) top-level element supports a `profiles` attribute to define a list of named profiles.
Services without a `profiles` attribute are always enabled.

A service is ignored by Compose when none of the listed `profiles` match the active ones, unless the service is
explicitly targeted by a command. In that case its profile is added to the set of active profiles.

> Note
>
> All other top-level elements are not affected by `profiles` and are always active.

References to other services (by `links`, `extends` or shared resource syntax `service:xxx`) do not
automatically enable a component that would otherwise have been ignored by active profiles. Instead
Compose returns an error.

## Illustrative example

```yaml
services:
  web:
    image: web_image

  test_lib:
    image: test_lib_image
    profiles:
      - test

  coverage_lib:
    image: coverage_lib_image
    depends_on:
      - test_lib
    profiles:
      - test

  debug_lib:
    image: debug_lib_image
    depends_on:
      - test_lib
    profiles:
      - debug
```

In the above example:

- If the Compose application model is parsed when no profile is enabled, it only contains the `web` service.
- If the profile `test` is enabled, the model contains the services `test_lib` and `coverage_lib`, and service `web`, which is always enabled.
- If the profile `debug` is enabled, the model contains both `web` and `debug_lib` services, but not `test_lib` and `coverage_lib`,
  and as such the model is invalid regarding the `depends_on` constraint of `debug_lib`.
- If the profiles `debug` and `test` are enabled, the model contains all services; `web`, `test_lib`, `coverage_lib` and `debug_lib`.
- If Compose is executed with `test_lib` as the explicit service to run, `test_lib` and the `test` profile
  are active even if `test` profile is not enabled.
- If Compose is executed with `coverage_lib` as the explicit service to run, the service `coverage_lib` and the
  profile `test` are active and `test_lib` is pulled in by the `depends_on` constraint.
- If Compose is executed with `debug_lib` as the explicit service to run, again the model is
  invalid regarding the `depends_on` constraint of `debug_lib`, since `debug_lib` and `test_lib` have no common `profiles`
  listed.
- If Compose is executed with `debug_lib` as the explicit service to run and profile `test` is enabled,
  profile `debug` is automatically enabled and service `test_lib` is pulled in as a dependency starting both
  services `debug_lib` and `test_lib`.

Learn how to use `profiles` in
[Docker Compose](https://docs.docker.com/compose/how-tos/profiles/).

---

# Secrets

> Explore all the attributes the secrets top-level element can have.

# Secrets

   Table of contents

---

Secrets are a flavor of [Configs](https://docs.docker.com/reference/compose-file/configs/) focusing on sensitive data, with specific constraint for this usage.

Services can only access secrets when explicitly granted by a [secretsattribute](https://docs.docker.com/reference/compose-file/services/#secrets) within the `services` top-level element.

The top-level `secrets` declaration defines or references sensitive data that is granted to the services in your Compose
application. The source of the secret is either `file` or `environment`.

- `file`: The secret is created with the contents of the file at the specified path.
- `environment`: The secret is created with the value of an environment variable on the host.

## Example 1

`server-certificate` secret is created as `<project_name>_server-certificate` when the application is deployed,
by registering content of the `server.cert` as a platform secret.

```yml
secrets:
  server-certificate:
    file: ./server.cert
```

## Example 2

`token` secret is created as `<project_name>_token` when the application is deployed,
by registering the content of the `OAUTH_TOKEN` environment variable as a platform secret.

```yml
secrets:
  token:
    environment: "OAUTH_TOKEN"
```

## Additional resources

For more information, see
[How to use secrets in Compose](https://docs.docker.com/compose/how-tos/use-secrets/).
