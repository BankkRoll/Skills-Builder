# Environment variables precedence in Docker Compose and more

# Environment variables precedence in Docker Compose

> Scenario overview illustrating how environment variables are resolved in Compose

# Environment variables precedence in Docker Compose

   Table of contents

---

When the same environment variable is set in multiple sources, Docker Compose follows a precedence rule to determine the value for that variable in your container's environment.

This page explains how Docker Compose determines the final value of an environment variable when it's defined in multiple locations.

The order of precedence (highest to lowest) is as follows:

1. Set using [docker compose run -ein the CLI](https://docs.docker.com/compose/how-tos/environment-variables/set-environment-variables/#set-environment-variables-with-docker-compose-run---env).
2. Set with either the `environment` or `env_file` attribute but with the value interpolated from your [shell](https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/#substitute-from-the-shell) or an environment file. (either your default [.envfile](https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/#env-file), or with the [--env-fileargument](https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/#substitute-with---env-file) in the CLI).
3. Set using just the [environmentattribute](https://docs.docker.com/compose/how-tos/environment-variables/set-environment-variables/#use-the-environment-attribute) in the Compose file.
4. Use of the [env_fileattribute](https://docs.docker.com/compose/how-tos/environment-variables/set-environment-variables/#use-the-env_file-attribute) in the Compose file.
5. Set in a container image in the
  [ENV directive](https://docs.docker.com/reference/dockerfile/#env).
  Having any `ARG` or `ENV` setting in a `Dockerfile` evaluates only if there is no Docker Compose entry for `environment`, `env_file` or `run --env`.

## Simple example

In the following example, a different value for the same environment variable in an `.env` file and with the `environment` attribute in the Compose file:

```console
$ cat ./webapp.env
NODE_ENV=test

$ cat compose.yaml
services:
  webapp:
    image: 'webapp'
    env_file:
     - ./webapp.env
    environment:
     - NODE_ENV=production
```

The environment variable defined with the `environment` attribute takes precedence.

```console
$ docker compose run webapp env | grep NODE_ENV
NODE_ENV=production
```

## Advanced example

The following table uses `VALUE`, an environment variable defining the version for an image, as an example.

### How the table works

Each column represents a context from where you can set a value, or substitute in a value for `VALUE`.

The columns `Host OS environment` and `.env` file is listed only for illustration purposes. In reality, they don't result in a variable in the container by itself, but in conjunction with either the `environment` or `env_file` attribute.

Each row represents a combination of contexts where `VALUE` is set, substituted, or both. The **Result** column indicates the final value for `VALUE` in each scenario.

| # | docker compose run | environmentattribute | env_fileattribute | ImageENV | Host OSenvironment | .envfile | Result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | - | - | - | - | VALUE=1.4 | VALUE=1.3 | - |
| 2 | - | - | VALUE=1.6 | VALUE=1.5 | VALUE=1.4 | - | VALUE=1.6 |
| 3 | - | VALUE=1.7 | - | VALUE=1.5 | VALUE=1.4 | - | VALUE=1.7 |
| 4 | - | - | - | VALUE=1.5 | VALUE=1.4 | VALUE=1.3 | VALUE=1.5 |
| 5 | --env VALUE=1.8 | - | - | VALUE=1.5 | VALUE=1.4 | VALUE=1.3 | VALUE=1.8 |
| 6 | --env VALUE | - | - | VALUE=1.5 | VALUE=1.4 | VALUE=1.3 | VALUE=1.4 |
| 7 | --env VALUE | - | - | VALUE=1.5 | - | VALUE=1.3 | VALUE=1.3 |
| 8 | - | - | VALUE | VALUE=1.5 | VALUE=1.4 | VALUE=1.3 | VALUE=1.4 |
| 9 | - | - | VALUE | VALUE=1.5 | - | VALUE=1.3 | VALUE=1.3 |
| 10 | - | VALUE | - | VALUE=1.5 | VALUE=1.4 | VALUE=1.3 | VALUE=1.4 |
| 11 | - | VALUE | - | VALUE=1.5 | - | VALUE=1.3 | VALUE=1.3 |
| 12 | --env VALUE | VALUE=1.7 | - | VALUE=1.5 | VALUE=1.4 | VALUE=1.3 | VALUE=1.4 |
| 13 | --env VALUE=1.8 | VALUE=1.7 | - | VALUE=1.5 | VALUE=1.4 | VALUE=1.3 | VALUE=1.8 |
| 14 | --env VALUE=1.8 | - | VALUE=1.6 | VALUE=1.5 | VALUE=1.4 | VALUE=1.3 | VALUE=1.8 |
| 15 | --env VALUE=1.8 | VALUE=1.7 | VALUE=1.6 | VALUE=1.5 | VALUE=1.4 | VALUE=1.3 | VALUE=1.8 |

### Understanding precedence results

Result 1: The local environment takes precedence, but the Compose file is not set to replicate this inside the container, so no such variable is set.

Result 2: The `env_file` attribute in the Compose file defines an explicit value for `VALUE` so the container environment is set accordingly.

Result 3: The `environment` attribute in the Compose file defines an explicit value for `VALUE`, so the container environment is set accordingly.

Result 4: The image's `ENV` directive declares the variable `VALUE`, and since the Compose file is not set to override this value, this variable is defined by image

Result 5: The `docker compose run` command has the `--env` flag set with an explicit value, and overrides the value set by the image.

Result 6: The `docker compose run` command has the `--env` flag set to replicate the value from the environment. Host OS value takes precedence and is replicated into the container's environment.

Result 7: The `docker compose run` command has the `--env` flag set to replicate the value from the environment. Value from `.env` file is selected to define the container's environment.

Result 8: The `env_file` attribute in the Compose file is set to replicate `VALUE` from the local environment. Host OS value takes precedence and is replicated into the container's environment.

Result 9: The `env_file` attribute in the Compose file is set to replicate `VALUE` from the local environment. Value from `.env` file is selected to define the container's environment.

Result 10: The `environment` attribute in the Compose file is set to replicate `VALUE` from the local environment. Host OS value takes precedence and is replicated into the container's environment.

Result 11: The `environment` attribute in the Compose file is set to replicate `VALUE` from the local environment. Value from `.env` file is selected to define the container's environment.

Result 12: The `--env` flag has higher precedence than the `environment` and `env_file` attributes and is to set to replicate `VALUE` from the local environment. Host OS value takes precedence and is replicated into the container's environment.

Results 13 to 15: The `--env` flag has higher precedence than the `environment` and `env_file` attributes and so sets the value.

## Next steps

- [Set environment variables in Compose](https://docs.docker.com/compose/how-tos/environment-variables/set-environment-variables/)
- [Use variable interpolation in Compose files](https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/)

---

# Configure pre

> Compose pre-defined environment variables

# Configure pre-defined environment variables in Docker Compose

   Table of contents

---

Docker Compose includes several pre-defined environment variables. It also inherits common Docker CLI environment variables, such as `DOCKER_HOST` and `DOCKER_CONTEXT`. See
[Docker CLI environment variable reference](https://docs.docker.com/reference/cli/docker/#environment-variables) for details.

This page explains how to set or change the following pre-defined environment variables:

- `COMPOSE_PROJECT_NAME`
- `COMPOSE_FILE`
- `COMPOSE_PROFILES`
- `COMPOSE_CONVERT_WINDOWS_PATHS`
- `COMPOSE_PATH_SEPARATOR`
- `COMPOSE_IGNORE_ORPHANS`
- `COMPOSE_REMOVE_ORPHANS`
- `COMPOSE_PARALLEL_LIMIT`
- `COMPOSE_ANSI`
- `COMPOSE_STATUS_STDOUT`
- `COMPOSE_ENV_FILES`
- `COMPOSE_DISABLE_ENV_FILE`
- `COMPOSE_MENU`
- `COMPOSE_EXPERIMENTAL`
- `COMPOSE_PROGRESS`

## Methods to override

| Method | Description |
| --- | --- |
| .envfile | Located in the working directory. |
| Shell | Defined in the host operating system shell. |
| CLI | Passed with--envor-eflag at runtime. |

When changing or setting any environment variables, be aware of [Environment variable precedence](https://docs.docker.com/compose/how-tos/environment-variables/envvars-precedence/).

## Configuration details

### Project and file configuration

#### COMPOSE_PROJECT_NAME

Sets the project name. This value is prepended along with the service name to
the container's name on startup.

For example, if your project name is `myapp` and it includes two services `db` and `web`,
then Compose starts containers named `myapp-db-1` and `myapp-web-1` respectively.

Compose can set the project name in different ways. The level of precedence (from highest to lowest) for each method is as follows:

1. The `-p` command line flag
2. `COMPOSE_PROJECT_NAME`
3. The top-level `name:` variable from the config file (or the last `name:` from
  a series of config files specified using `-f`)
4. The `basename` of the project directory containing the config file (or
  containing the first config file specified using `-f`)
5. The `basename` of the current directory if no config file is specified

Project names must contain only lowercase letters, decimal digits, dashes, and
underscores, and must begin with a lowercase letter or decimal digit. If the
`basename` of the project directory or current directory violates this
constraint, you must use one of the other mechanisms.

See also the
[command-line options overview](https://docs.docker.com/reference/cli/docker/compose/#command-options-overview-and-help) and
[using-pto specify a project name](https://docs.docker.com/reference/cli/docker/compose/#use--p-to-specify-a-project-name).

#### COMPOSE_FILE

Specifies the path to a Compose file. Specifying multiple Compose files is supported.

- Default behavior: If not provided, Compose looks for a file named `compose.yaml` in the current directory and, if not found, then Compose searches each parent directory recursively until a file by that name is found.
- When specifying multiple Compose files, the path separators are, by default, on:
  - Mac and Linux: `:` (colon)
  - Windows: `;` (semicolon)
    For example:
    ```console
    COMPOSE_FILE=compose.yaml:compose.prod.yaml
    ```
  The path separator can also be customized using [COMPOSE_PATH_SEPARATOR](#compose_path_separator).

See also the
[command-line options overview](https://docs.docker.com/reference/cli/docker/compose/#command-options-overview-and-help) and
[using-fto specify name and path of one or more Compose files](https://docs.docker.com/reference/cli/docker/compose/#use--f-to-specify-the-name-and-path-of-one-or-more-compose-files).

#### COMPOSE_PROFILES

Specifies one or more profiles to be enabled when `docker compose up` is run.

Services with matching profiles are started as well as any services for which no profile has been defined.

For example, calling `docker compose up` with `COMPOSE_PROFILES=frontend` selects services with the
`frontend` profile as well as any services without a profile specified.

If specifying multiple profiles, use a comma as a separator.

The following example enables all services matching both the `frontend` and `debug` profiles and services without a profile.

```console
COMPOSE_PROFILES=frontend,debug
```

See also [Using profiles with Compose](https://docs.docker.com/compose/how-tos/profiles/) and the
[--profilecommand-line option](https://docs.docker.com/reference/cli/docker/compose/#use-profiles-to-enable-optional-services).

#### COMPOSE_PATH_SEPARATOR

Specifies a different path separator for items listed in `COMPOSE_FILE`.

- Defaults to:
  - On macOS and Linux to `:`
  - On Windows to`;`

#### COMPOSE_ENV_FILES

Specifies which environment files Compose should use if `--env-file` isn't used.

When using multiple environment files, use a comma as a separator. For example:

```console
COMPOSE_ENV_FILES=.env.envfile1,.env.envfile2
```

If `COMPOSE_ENV_FILES` is not set, and you don't provide `--env-file` in the CLI, Docker Compose uses the default behavior, which is to look for an `.env` file in the project directory.

#### COMPOSE_DISABLE_ENV_FILE

Lets you disable the use of the default `.env` file.

- Supported values:
  - `true` or `1`, Compose ignores the `.env` file
  - `false` or `0`, Compose looks for an `.env` file in the project directory
- Defaults to: `0`

### Environment handling and container lifecycle

#### COMPOSE_CONVERT_WINDOWS_PATHS

When enabled, Compose performs path conversion from Windows-style to Unix-style in volume definitions.

- Supported values:
  - `true` or `1`, to enable
  - `false` or `0`, to disable
- Defaults to: `0`

#### COMPOSE_IGNORE_ORPHANS

When enabled, Compose doesn't try to detect orphaned containers for the project.

- Supported values:
  - `true` or `1`, to enable
  - `false` or `0`, to disable
- Defaults to: `0`

#### COMPOSE_REMOVE_ORPHANS

When enabled, Compose automatically removes orphaned containers when updating a service or stack. Orphaned containers are those that were created by a previous configuration but are no longer defined in the current `compose.yaml` file.

- Supported values:
  - `true` or `1`, to enable automatic removal of orphaned containers
  - `false` or `0`, to disable automatic removal. Compose displays a warning about orphaned containers instead.
- Defaults to: `0`

#### COMPOSE_PARALLEL_LIMIT

Specifies the maximum level of parallelism for concurrent engine calls.

### Output

#### COMPOSE_ANSI

Specifies when to print ANSI control characters.

- Supported values:
  - `auto`, Compose detects if TTY mode can be used. Otherwise, use plain text mode
  - `never`, use plain text mode
  - `always` or `0`, use TTY mode
- Defaults to: `auto`

#### COMPOSE_STATUS_STDOUT

When enabled, Compose writes its internal status and progress messages to `stdout` instead of `stderr`.
The default value is false to clearly separate the output streams between Compose messages and your container's logs.

- Supported values:
  - `true` or `1`, to enable
  - `false` or `0`, to disable
- Defaults to: `0`

#### COMPOSE_PROGRESS

Requires: Docker Compose [2.36.0](https://github.com/docker/compose/releases/tag/v2.36.0) and later

Defines the type of progress output, if `--progress` isn't used.

Supported values are `auto`, `tty`, `plain`, `json`, and `quiet`.
Default is `auto`.

### User experience

#### COMPOSE_MENU

Requires: Docker Compose [2.26.0](https://github.com/docker/compose/releases/tag/v2.26.0) and later

When enabled, Compose displays a navigation menu where you can choose to open the Compose stack in Docker Desktop, switch on [watchmode](https://docs.docker.com/compose/how-tos/file-watch/), or use
[Docker Debug](https://docs.docker.com/reference/cli/docker/debug/).

- Supported values:
  - `true` or `1`, to enable
  - `false` or `0`, to disable
- Defaults to: `1` if you obtained Docker Compose through Docker Desktop, otherwise the default is `0`

#### COMPOSE_EXPERIMENTAL

Requires: Docker Compose [2.26.0](https://github.com/docker/compose/releases/tag/v2.26.0) and later

This is an opt-out variable. When turned off it deactivates the experimental features.

- Supported values:
  - `true` or `1`, to enable
  - `false` or `0`, to disable
- Defaults to: `1`

## Unsupported in Compose V2

The following environment variables have no effect in Compose V2.

- `COMPOSE_API_VERSION`
  By default the API version is negotiated with the server. Use `DOCKER_API_VERSION`.
  See the
  [Docker CLI environment variable reference](https://docs.docker.com/reference/cli/docker/#environment-variables) page.
- `COMPOSE_HTTP_TIMEOUT`
- `COMPOSE_TLS_VERSION`
- `COMPOSE_FORCE_WINDOWS_HOST`
- `COMPOSE_INTERACTIVE_NO_CLI`
- `COMPOSE_DOCKER_CLI_BUILD`
  Use `DOCKER_BUILDKIT` to select between BuildKit and the classic builder. If `DOCKER_BUILDKIT=0` then `docker compose build` uses the classic builder to build images.

---

# Set environment variables within your container's environment

> How to set, use, and manage environment variables with Compose

# Set environment variables within your container's environment

   Table of contents

---

A container's environment is not set until there's an explicit entry in the service configuration to make this happen. With Compose, there are two ways you can set environment variables in your containers with your Compose file.

> Tip
>
> Don't use environment variables to pass sensitive information, such as passwords, in to your containers. Use [secrets](https://docs.docker.com/compose/how-tos/use-secrets/) instead.

## Use theenvironmentattribute

You can set environment variables directly in your container's environment with the
[environmentattribute](https://docs.docker.com/reference/compose-file/services/#environment) in your `compose.yaml`.

It supports both list and mapping syntax:

```yaml
services:
  webapp:
    environment:
      DEBUG: "true"
```

is equivalent to

```yaml
services:
  webapp:
    environment:
      - DEBUG=true
```

See
[environmentattribute](https://docs.docker.com/reference/compose-file/services/#environment) for more examples on how to use it.

### Additional information

- You can choose not to set a value and pass the environment variables from your shell straight through to your containers. It works in the same way as `docker run -e VARIABLE ...`:
  ```yaml
  web:
    environment:
      - DEBUG
  ```

The value of the `DEBUG` variable in the container is taken from the value for the same variable in the shell in which Compose is run. Note that in this case no warning is issued if the `DEBUG` variable in the shell environment is not set.

- You can also take advantage of [interpolation](https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/#interpolation-syntax). In the following example, the result is similar to the one above but Compose gives you a warning if the `DEBUG` variable is not set in the shell environment or in an `.env` file in the project directory.
  ```yaml
  web:
    environment:
      - DEBUG=${DEBUG}
  ```

## Use theenv_fileattribute

A container's environment can also be set using [.envfiles](https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/#env-file) along with the
[env_fileattribute](https://docs.docker.com/reference/compose-file/services/#env_file).

```yaml
services:
  webapp:
    env_file: "webapp.env"
```

Using an `.env` file lets you use the same file for use by a plain `docker run --env-file ...` command, or to share the same `.env` file within multiple services without the need to duplicate a long `environment` YAML block.

It can also help you keep your environment variables separate from your main configuration file, providing a more organized and secure way to manage sensitive information, as you do not need to place your `.env` file in the root of your project's directory.

The
[env_fileattribute](https://docs.docker.com/reference/compose-file/services/#env_file) also lets you use multiple `.env` files in your Compose application.

The paths to your `.env` file, specified in the `env_file` attribute, are relative to the location of your `compose.yaml` file.

> Important
>
> Interpolation in `.env` files is a Docker Compose CLI feature.
>
>
>
> It is not supported when running `docker run --env-file ...`.

### Additional information

- If multiple files are specified, they are evaluated in order and can override values set in previous files.
- As of Docker Compose version 2.24.0, you can set your `.env` file, defined by the `env_file` attribute, to be optional by using the `required` field. When `required` is set to `false` and the `.env` file is missing, Compose silently ignores the entry.
  ```yaml
  env_file:
    - path: ./default.env
      required: true # default
    - path: ./override.env
      required: false
  ```
- As of Docker Compose version 2.30.0, you can use an alternative file format for the `env_file` with the `format` attribute. For more information, see
  [format](https://docs.docker.com/reference/compose-file/services/#format).
- Values in your `.env` file can be overridden from the command line by using [docker compose run -e](#set-environment-variables-with-docker-compose-run---env).

## Set environment variables withdocker compose run --env

Similar to `docker run --env`, you can set environment variables temporarily with `docker compose run --env` or its short form `docker compose run -e`:

```console
$ docker compose run -e DEBUG=1 web python console.py
```

### Additional information

- You can also pass a variable from the shell or your environment files by not giving it a value:
  ```console
  $ docker compose run -e DEBUG web python console.py
  ```

The value of the `DEBUG` variable in the container is taken from the value for the same variable in the shell in which Compose is run or from the environment files.

## Further resources

- [Understand environment variable precedence](https://docs.docker.com/compose/how-tos/environment-variables/envvars-precedence/).
- [Set or change predefined environment variables](https://docs.docker.com/compose/how-tos/environment-variables/envvars/)
- [Explore best practices](https://docs.docker.com/compose/how-tos/environment-variables/best-practices/)
- [Understand interpolation](https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/)

---

# Set, use, and manage variables in a Compose file with interpolation

> How to set, use, and manage variables in your Compose file with interpolation

# Set, use, and manage variables in a Compose file with interpolation

   Table of contents

---

A Compose file can use variables to offer more flexibility. If you want to quickly switch
between image tags to test multiple versions, or want to adjust a volume source to your local
environment, you don't need to edit the Compose file each time, you can just set variables that insert values into your Compose file at runtime.

Interpolation can also be used to insert values into your Compose file at runtime, which is then used to pass variables into your container's environment

Below is a simple example:

```console
$ cat .env
TAG=v1.5
$ cat compose.yaml
services:
  web:
    image: "webapp:${TAG}"
```

When you run `docker compose up`, the `web` service defined in the Compose file [interpolates](https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/) in the image `webapp:v1.5` which was set in the `.env` file. You can verify this with the
[config command](https://docs.docker.com/reference/cli/docker/compose/config/), which prints your resolved application config to the terminal:

```console
$ docker compose config
services:
  web:
    image: 'webapp:v1.5'
```

## Interpolation syntax

Interpolation is applied for unquoted and double-quoted values.
Both braced (`${VAR}`) and unbraced (`$VAR`) expressions are supported.

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

For more information, see
[Interpolation](https://docs.docker.com/reference/compose-file/interpolation/) in the Compose Specification.

## Ways to set variables with interpolation

Docker Compose can interpolate variables into your Compose file from multiple sources.

Note that when the same variable is declared by multiple sources, precedence applies:

1. Variables from your shell environment
2. If `--env-file` is not set, variables set by an `.env` file in local working directory (`PWD`)
3. Variables from a file set by `--env-file` or an `.env` file in project directory

You can check variables and values used by Compose to interpolate the Compose model by running `docker compose config --environment`.

### .envfile

An `.env` file in Docker Compose is a text file used to define variables that should be made available for interpolation when running `docker compose up`. This file typically contains key-value pairs of variables, and it lets you centralize and manage configuration in one place. The `.env` file is useful if you have multiple variables you need to store.

The `.env` file is the default method for setting variables. The `.env` file should be placed at the root of the project directory next to your `compose.yaml` file. For more information on formatting an environment file, see [Syntax for environment files](#env-file-syntax).

Basic example:

```console
$ cat .env
## define COMPOSE_DEBUG based on DEV_MODE, defaults to false
COMPOSE_DEBUG=${DEV_MODE:-false}

$ cat compose.yaml
  services:
    webapp:
      image: my-webapp-image
      environment:
        - DEBUG=${COMPOSE_DEBUG}

$ DEV_MODE=true docker compose config
services:
  webapp:
    environment:
      DEBUG: "true"
```

#### Additional information

- If you define a variable in your `.env` file, you can reference it directly in your `compose.yaml` with the
  [environmentattribute](https://docs.docker.com/reference/compose-file/services/#environment). For example, if your `.env` file contains the environment variable `DEBUG=1` and your `compose.yaml` file looks like this:
  ```yaml
  services:
     webapp:
       image: my-webapp-image
       environment:
         - DEBUG=${DEBUG}
  ```
  Docker Compose replaces `${DEBUG}` with the value from the `.env` file
  > Important
  >
  > Be aware of [Environment variables precedence](https://docs.docker.com/compose/how-tos/environment-variables/envvars-precedence/) when using variables in an `.env` file that as environment variables in your container's environment.
- You can place your `.env` file in a location other than the root of your project's directory, and then use the [--env-fileoption in the CLI](#substitute-with---env-file) so Compose can navigate to it.
- Your `.env` file can be overridden by another `.env` if it is [substituted with--env-file](#substitute-with---env-file).

> Important
>
> Substitution from `.env` files is a Docker Compose CLI feature.
>
>
>
> It is not supported by Swarm when running `docker stack deploy`.

#### .envfile syntax

The following syntax rules apply to environment files:

- Lines beginning with `#` are processed as comments and ignored.
- Blank lines are ignored.
- Unquoted and double-quoted (`"`) values have interpolation applied.
- Each line represents a key-value pair. Values can optionally be quoted.
- Delimiter separating key and value can be either `=` or `:`.
- Spaces before and after value are ignored.
  - `VAR=VAL` -> `VAL`
  - `VAR="VAL"` -> `VAL`
  - `VAR='VAL'` -> `VAL`
  - `VAR: VAL` -> `VAL`
  - `VAR = VAL `-> `VAL`
- Inline comments for unquoted values must be preceded with a space.
  - `VAR=VAL # comment` -> `VAL`
  - `VAR=VAL# not a comment` -> `VAL# not a comment`
- Inline comments for quoted values must follow the closing quote.
  - `VAR="VAL # not a comment"` -> `VAL # not a comment`
  - `VAR="VAL" # comment` -> `VAL`
- Single-quoted (`'`) values are used literally.
  - `VAR='$OTHER'` -> `$OTHER`
  - `VAR='${OTHER}'` -> `${OTHER}`
- Quotes can be escaped with `\`.
  - `VAR='Let\'s go!'` -> `Let's go!`
  - `VAR="{\"hello\": \"json\"}"` -> `{"hello": "json"}`
- Common shell escape sequences including `\n`, `\r`, `\t`, and `\\` are supported in double-quoted values.
  - `VAR="some\tvalue"` -> `some value`
  - `VAR='some\tvalue'` -> `some\tvalue`
  - `VAR=some\tvalue` -> `some\tvalue`
- Single-quoted values can span multiple lines. Example:
  ```yaml
  KEY='SOME
  VALUE'
  ```
  If you then run `docker compose config`, you'll see:
  ```yaml
  environment:
    KEY: |-
      SOME
      VALUE
  ```

### Substitute with--env-file

You can set default values for multiple environment variables, in an `.env` file and then pass the file as an argument in the CLI.

The advantage of this method is that you can store the file anywhere and name it appropriately, for example,
This file path is relative to the current working directory where the Docker Compose command is executed. Passing the file path is done using the `--env-file` option:

```console
$ docker compose --env-file ./config/.env.dev up
```

#### Additional information

- This method is useful if you want to temporarily override an `.env` file that is already referenced in your `compose.yaml` file. For example you may have different `.env` files for production ( `.env.prod`) and testing (`.env.test`).
  In the following example, there are two environment files, `.env` and `.env.dev`. Both have different values set for `TAG`.
  ```console
  $ cat .env
  TAG=v1.5
  $ cat ./config/.env.dev
  TAG=v1.6
  $ cat compose.yaml
  services:
    web:
      image: "webapp:${TAG}"
  ```
  If the `--env-file` is not used in the command line, the `.env` file is loaded by default:
  ```console
  $ docker compose config
  services:
    web:
      image: 'webapp:v1.5'
  ```
  Passing the `--env-file` argument overrides the default file path:
  ```console
  $ docker compose --env-file ./config/.env.dev config
  services:
    web:
      image: 'webapp:v1.6'
  ```
  When an invalid file path is being passed as an `--env-file` argument, Compose returns an error:
  ```console
  $ docker compose --env-file ./doesnotexist/.env.dev  config
  ERROR: Couldn't find env file: /home/user/./doesnotexist/.env.dev
  ```
- You can use multiple `--env-file` options to specify multiple environment files, and Docker Compose reads them in order. Later files can override variables from earlier files.
  ```console
  $ docker compose --env-file .env --env-file .env.override up
  ```
- You can override specific environment variables from the command line when starting containers.
  ```console
  $ docker compose --env-file .env.dev up -e DATABASE_URL=mysql://new_user:new_password@new_db:3306/new_database
  ```

### local.envfile versus <project directory>.envfile

An `.env` file can also be used to declare [pre-defined environment variables](https://docs.docker.com/compose/how-tos/environment-variables/envvars/) used to control Compose behavior and files to be loaded.

When executed without an explicit `--env-file` flag, Compose searches for an `.env` file in your working directory ([PWD](https://www.gnu.org/software/bash/manual/html_node/Bash-Variables.html#index-PWD)) and loads values
both for self-configuration and interpolation. If the values in this file define the `COMPOSE_FILE` pre-defined variable, which results in a project directory being set to another folder,
Compose will load a second `.env` file, if present. This second `.env` file has a lower precedence.

This mechanism makes it possible to invoke an existing Compose project with a custom set of variables as overrides, without the need to pass environment variables by the command line.

```console
$ cat .env
COMPOSE_FILE=../compose.yaml
POSTGRES_VERSION=9.3

$ cat ../compose.yaml
services:
  db:
    image: "postgres:${POSTGRES_VERSION}"
$ cat ../.env
POSTGRES_VERSION=9.2

$ docker compose config
services:
  db:
    image: "postgres:9.3"
```

### Substitute from the shell

You can use existing environment variables from your host machine or from the shell environment where you execute `docker compose` commands. This lets you dynamically inject values into your Docker Compose configuration at runtime.
For example, suppose the shell contains `POSTGRES_VERSION=9.3` and you supply the following configuration:

```yaml
db:
  image: "postgres:${POSTGRES_VERSION}"
```

When you run `docker compose up` with this configuration, Compose looks for the `POSTGRES_VERSION` environment variable in the shell and substitutes its value in. For this example, Compose resolves the image to `postgres:9.3` before running the configuration.

If an environment variable is not set, Compose substitutes with an empty string. In the previous example, if `POSTGRES_VERSION` is not set, the value for the image option is `postgres:`.

> Note
>
> `postgres:` is not a valid image reference. Docker expects either a reference without a tag, like `postgres` which defaults to the latest image, or with a tag such as `postgres:15`.

---

# Environment variables in Compose

> Explains how to set, use, and manage environment variables in Docker Compose.

# Environment variables in Compose

---

Environment variables and interpolation in Docker Compose help you create reusable, flexible configurations. This makes Dockerized applications easier to manage and deploy across environments.

> Tip
>
> Before using environment variables, read through all of the information first to get a full picture of environment variables in Docker Compose.

This section covers:

- [How to set environment variables within your container's environment](https://docs.docker.com/compose/how-tos/environment-variables/set-environment-variables/).
- [How environment variable precedence works within your container's environment](https://docs.docker.com/compose/how-tos/environment-variables/envvars-precedence/).
- [Pre-defined environment variables](https://docs.docker.com/compose/how-tos/environment-variables/envvars/).

It also covers:

- How [interpolation](https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/) can be used to set variables within your Compose file and how it relates to a container's environment.
- Some [best practices](https://docs.docker.com/compose/how-tos/environment-variables/best-practices/).

---

# Use Compose Watch

> Use File watch to automatically update running services as you work

# Use Compose Watch

   Table of contents

---

Requires: Docker Compose [2.22.0](https://github.com/docker/compose/releases/tag/v2.22.0) and later

The `watch` attribute automatically updates and previews your running Compose services as you edit and save your code. For many projects, this enables a hands-off development workflow once Compose is running, as services automatically update themselves when you save your work.

`watch` adheres to the following file path rules:

- All paths are relative to the project directory, apart from ignore file patterns
- Directories are watched recursively
- Glob patterns aren't supported
- Rules from `.dockerignore` apply
  - Use `ignore` option to define additional paths to be ignored (same syntax)
  - Temporary/backup files for common IDEs (Vim, Emacs, JetBrains, & more) are ignored automatically
  - `.git` directories are ignored automatically

You don't need to switch on `watch` for all services in a Compose project. In some instances, only part of the project, for example the Javascript frontend, might be suitable for automatic updates.

Compose Watch is designed to work with services built from local source code using the `build` attribute. It doesn't track changes for services that rely on pre-built images specified by the `image` attribute.

## Compose Watch versus bind mounts

Compose supports sharing a host directory inside service containers. Watch mode does not replace this functionality but exists as a companion specifically suited to developing in containers.

More importantly, `watch` allows for greater granularity than is practical with a bind mount. Watch rules let you ignore specific files or entire directories within the watched tree.

For example, in a JavaScript project, ignoring the `node_modules/` directory has two benefits:

- Performance. File trees with many small files can cause a high I/O load in some configurations
- Multi-platform. Compiled artifacts cannot be shared if the host OS or architecture is different from the container

For example, in a Node.js project, it's not recommended to sync the `node_modules/` directory. Even though JavaScript is interpreted, `npm` packages can contain native code that is not portable across platforms.

## Configuration

The `watch` attribute defines a list of rules that control automatic service updates based on local file changes.

Each rule requires a `path` pattern and `action` to take when a modification is detected. There are two possible actions for `watch` and depending on
the `action`, additional fields might be accepted or required.

Watch mode can be used with many different languages and frameworks.
The specific paths and rules will vary from project to project, but the concepts remain the same.

### Prerequisites

In order to work properly, `watch` relies on common executables. Make sure your service image contains the following binaries:

- stat
- mkdir
- rmdir

`watch` also requires that the container's `USER` can write to the target path so it can update files. A common pattern is for
initial content to be copied into the container using the `COPY` instruction in a Dockerfile. To ensure such files are owned
by the configured user, use the `COPY --chown` flag:

```dockerfile
# Run as a non-privileged user
FROM node:18
RUN useradd -ms /bin/sh -u 1001 app
USER app

# Install dependencies
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install

# Copy source files into application directory
COPY --chown=app:app . /app
```

### action

#### Sync

If `action` is set to `sync`, Compose makes sure any changes made to files on your host automatically match with the corresponding files within the service container.

`sync` is ideal for frameworks that support "Hot Reload" or equivalent functionality.

More generally, `sync` rules can be used in place of bind mounts for many development use cases.

#### Rebuild

If `action` is set to `rebuild`, Compose automatically builds a new image with BuildKit and replaces the running service container.

The behavior is the same as running `docker compose up --build <svc>`.

Rebuild is ideal for compiled languages or as a fallback for modifications to particular files that require a full
image rebuild (e.g. `package.json`).

#### Sync + Restart

If `action` is set to `sync+restart`, Compose synchronizes your changes with the service containers and restarts them.

`sync+restart` is ideal when the config file changes, and you don't need to rebuild the image but just restart the main process of the service containers.
It will work well when you update a database configuration or your `nginx.conf` file, for example.

> Tip
>
> Optimize your `Dockerfile` for speedy
> incremental rebuilds with
> [image layer caching](https://docs.docker.com/build/cache)
> and
> [multi-stage builds](https://docs.docker.com/build/building/multi-stage/).

### pathandtarget

The `target` field controls how the path is mapped into the container.

For `path: ./app/html` and a change to `./app/html/index.html`:

- `target: /app/html` -> `/app/html/index.html`
- `target: /app/static` -> `/app/static/index.html`
- `target: /assets` -> `/assets/index.html`

### ignore

The `ignore` patterns are relative to the `path` defined in the current `watch` action, not to the project directory. In the following Example 1, the ignore path would be relative to the `./web` directory specified in the `path` attribute.

### initial_sync

When using a `sync+x` action, the `initial_sync` attribute tells Compose to ensure files that are part of the defined `path` are up to date before starting a new watch session.

## Example 1

This minimal example targets a Node.js application with the following structure:

```text
myproject/
├── web/
│   ├── App.jsx
│   ├── index.js
│   └── node_modules/
├── Dockerfile
├── compose.yaml
└── package.json
```

```yaml
services:
  web:
    build: .
    command: npm start
    develop:
      watch:
        - action: sync
          path: ./web
          target: /src/web
          initial_sync: true
          ignore:
            - node_modules/
        - action: rebuild
          path: package.json
```

In this example, when running `docker compose up --watch`, a container for the `web` service is launched using an image built from the `Dockerfile` in the project's root.
The `web` service runs `npm start` for its command, which then launches a development version of the application with Hot Module Reload enabled in the bundler (Webpack, Vite, Turbopack, etc).

After the service is up, the watch mode starts monitoring the target directories and files.
Then, whenever a source file in the `web/` directory is changed, Compose syncs the file to the corresponding location under `/src/web` inside the container.
For example, `./web/App.jsx` is copied to `/src/web/App.jsx`.

Once copied, the bundler updates the running application without a restart.

And in this case, the `ignore` rule would apply to `myproject/web/node_modules/`, not `myproject/node_modules/`.

Unlike source code files, adding a new dependency can’t be done on-the-fly, so whenever `package.json` is changed, Compose
rebuilds the image and recreates the `web` service container.

This pattern can be followed for many languages and frameworks, such as Python with Flask: Python source files can be synced while a change to `requirements.txt` should trigger a rebuild.

## Example 2

Adapting the previous example to demonstrate `sync+restart`:

```yaml
services:
  web:
    build: .
    command: npm start
    develop:
      watch:
        - action: sync
          path: ./web
          target: /app/web
          ignore:
            - node_modules/
        - action: sync+restart
          path: ./proxy/nginx.conf
          target: /etc/nginx/conf.d/default.conf

  backend:
    build:
      context: backend
      target: builder
```

This setup demonstrates how to use the `sync+restart` action in Docker Compose to efficiently develop and test a Node.js application with a frontend web server and backend service. The configuration ensures that changes to the application code and configuration files are quickly synchronized and applied, with the `web` service restarting as needed to reflect the changes.

## Usewatch

1. Add `watch` sections to one or more services in `compose.yaml`.
2. Run `docker compose up --watch` to build and launch a Compose project and start the file watch mode.
3. Edit service source files using your preferred IDE or editor.

> Note
>
> Watch can also be used with the dedicated `docker compose watch` command if you don't want to
> get the application logs mixed with the (re)build logs and filesystem sync events.

> Tip
>
> Check out [dockersamples/avatars](https://github.com/dockersamples/avatars),
> or [local setup for Docker docs](https://github.com/docker/docs/blob/main/CONTRIBUTING.md)
> for a demonstration of Compose `watch`.

## Reference

- [Compose Develop Specification](https://docs.docker.com/reference/compose-file/develop/)
