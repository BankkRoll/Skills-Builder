# docker mcp oauth authorize and more

# docker mcp oauth authorize

# docker mcp oauth authorize

| Description | Authorize the specified OAuth app. |
| --- | --- |
| Usage | docker mcp oauth authorize <app> |

## Description

Authorize the specified OAuth app.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --scopes |  | OAuth scopes to request (space-separated) |

---

# docker mcp oauth ls

# docker mcp oauth ls

| Description | List available OAuth apps. |
| --- | --- |
| Usage | docker mcp oauth ls |

## Description

List available OAuth apps.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --json |  | Print as JSON. |

---

# docker mcp oauth revoke

# docker mcp oauth revoke

| Description | Revoke the specified OAuth app. |
| --- | --- |
| Usage | docker mcp oauth revoke <app> |

## Description

Revoke the specified OAuth app.

---

# docker mcp oauth

# docker mcp oauth

## Subcommands

| Command | Description |
| --- | --- |
| docker mcp oauth authorize | Authorize the specified OAuth app. |
| docker mcp oauth ls | List available OAuth apps. |
| docker mcp oauth revoke | Revoke the specified OAuth app. |

---

# docker mcp policy dump

# docker mcp policy dump

| Description | Dump the policy content |
| --- | --- |
| Usage | docker mcp policy dump |

## Description

Dump the policy content

---

# docker mcp policy set

# docker mcp policy set

| Description | Set a policy for secret management in Docker Desktop |
| --- | --- |
| Usage | docker mcp policy set <content> |

## Description

Set a policy for secret management in Docker Desktop

## Examples

### Backup the current policy to a file

docker mcp policy dump > policy.conf

### Set a new policy

docker mcp policy set "my-secret allows postgres"

### Restore the previous policy

cat policy.conf | docker mcp policy set

---

# docker mcp policy

# docker mcp policy

| Description | Manage secret policies |
| --- | --- |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker mcp policies |

## Description

Manage secret policies

## Subcommands

| Command | Description |
| --- | --- |
| docker mcp policy dump | Dump the policy content |
| docker mcp policy set | Set a policy for secret management in Docker Desktop |

---

# docker mcp secret export

# docker mcp secret export

| Description | Export secrets for the specified servers |
| --- | --- |
| Usage | docker mcp secret export [server1] [server2] ... |

## Description

Export secrets for the specified servers

---

# docker mcp secret ls

# docker mcp secret ls

| Description | List all secret names in Docker Desktop's secret store |
| --- | --- |
| Usage | docker mcp secret ls |

## Description

List all secret names in Docker Desktop's secret store

## Options

| Option | Default | Description |
| --- | --- | --- |
| --json |  | Print as JSON. |

---

# docker mcp secret rm

# docker mcp secret rm

| Description | Remove secrets from Docker Desktop's secret store |
| --- | --- |
| Usage | docker mcp secret rm name1 name2 ... |

## Description

Remove secrets from Docker Desktop's secret store

## Options

| Option | Default | Description |
| --- | --- | --- |
| --all |  | Remove all secrets |

---

# docker mcp secret set

# docker mcp secret set

| Description | Set a secret in Docker Desktop's secret store |
| --- | --- |
| Usage | docker mcp secret set key[=value] |

## Description

Set a secret in Docker Desktop's secret store

## Options

| Option | Default | Description |
| --- | --- | --- |
| --provider |  | Supported: credstore, oauth/ |

## Examples

### Use secrets for postgres password with default policy

```console
docker mcp secret set POSTGRES_PASSWORD=my-secret-password
docker run -d -l x-secret:POSTGRES_PASSWORD=/pwd.txt -e POSTGRES_PASSWORD_FILE=/pwd.txt -p 5432 postgres
```

### Pass the secret via STDIN

```console
echo my-secret-password > pwd.txt
cat pwd.txt | docker mcp secret set POSTGRES_PASSWORD
```

---

# docker mcp secret

# docker mcp secret

| Description | Manage secrets |
| --- | --- |

## Description

Manage secrets

## Examples

### Use secrets for postgres password with default policy

> docker mcp secret set POSTGRES_PASSWORD=my-secret-password
> docker run -d -l x-secret:POSTGRES_PASSWORD=/pwd.txt -e POSTGRES_PASSWORD_FILE=/pwd.txt -p 5432 postgres

### Pass the secret via STDIN

> echo my-secret-password > pwd.txt
> cat pwd.txt | docker mcp secret set POSTGRES_PASSWORD

## Subcommands

| Command | Description |
| --- | --- |
| docker mcp secret export | Export secrets for the specified servers |
| docker mcp secret ls | List all secret names in Docker Desktop's secret store |
| docker mcp secret rm | Remove secrets from Docker Desktop's secret store |
| docker mcp secret set | Set a secret in Docker Desktop's secret store |

---

# docker mcp server disable

# docker mcp server disable

| Description | Disable a server or multiple servers |
| --- | --- |
| Usage | docker mcp server disable |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker mcp server removedocker mcp server rm |

## Description

Disable a server or multiple servers

---

# docker mcp server enable

# docker mcp server enable

| Description | Enable a server or multiple servers |
| --- | --- |
| Usage | docker mcp server enable |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker mcp server add |

## Description

Enable a server or multiple servers

---

# docker mcp server inspect

# docker mcp server inspect

| Description | Get information about a server or inspect an OCI artifact |
| --- | --- |
| Usage | docker mcp server inspect |

## Description

Get information about a server or inspect an OCI artifact

---

# docker mcp server list

# docker mcp server list

| Description | List enabled servers |
| --- | --- |
| Usage | docker mcp server list |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker mcp server ls |

## Description

List enabled servers

## Options

| Option | Default | Description |
| --- | --- | --- |
| --json |  | Output in JSON format |

---

# docker mcp server reset

# docker mcp server reset

| Description | Disable all the servers |
| --- | --- |
| Usage | docker mcp server reset |

## Description

Disable all the servers

---

# docker mcp server

# docker mcp server

| Description | Manage servers |
| --- | --- |

## Description

Manage servers

## Subcommands

| Command | Description |
| --- | --- |
| docker mcp server disable | Disable a server or multiple servers |
| docker mcp server enable | Enable a server or multiple servers |
| docker mcp server inspect | Get information about a server or inspect an OCI artifact |
| docker mcp server list | List enabled servers |
| docker mcp server reset | Disable all the servers |

---

# docker mcp tools call

# docker mcp tools call

| Description | Call a tool |
| --- | --- |
| Usage | docker mcp tools call |

## Description

Call a tool

---

# docker mcp tools count

# docker mcp tools count

| Description | Count tools |
| --- | --- |
| Usage | docker mcp tools count |

## Description

Count tools

---

# docker mcp tools disable

# docker mcp tools disable

| Description | disable one or more tools |
| --- | --- |
| Usage | docker mcp tools disable [tool1] [tool2] ... |

## Description

disable one or more tools

## Options

| Option | Default | Description |
| --- | --- | --- |
| --server |  | Specify which server provides the tools (optional, will auto-discover if not provided) |

---

# docker mcp tools enable

# docker mcp tools enable

| Description | enable one or more tools |
| --- | --- |
| Usage | docker mcp tools enable [tool1] [tool2] ... |

## Description

enable one or more tools

## Options

| Option | Default | Description |
| --- | --- | --- |
| --server |  | Specify which server provides the tools (optional, will auto-discover if not provided) |

---

# docker mcp tools inspect

# docker mcp tools inspect

| Description | Inspect a tool |
| --- | --- |
| Usage | docker mcp tools inspect |

## Description

Inspect a tool

---

# docker mcp tools ls

# docker mcp tools ls

| Description | List tools |
| --- | --- |
| Usage | docker mcp tools ls |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker mcp tools list |

## Description

List tools

---

# docker mcp tools

# docker mcp tools

| Description | Manage tools |
| --- | --- |

## Description

Manage tools

## Options

| Option | Default | Description |
| --- | --- | --- |
| --format | list | Output format (json|list) |
| --gateway-arg |  | Additional arguments passed to the gateway |
| --verbose |  | Verbose output |
| --version | 2 | Version of the gateway |

## Subcommands

| Command | Description |
| --- | --- |
| docker mcp tools call | Call a tool |
| docker mcp tools count | Count tools |
| docker mcp tools disable | disable one or more tools |
| docker mcp tools enable | enable one or more tools |
| docker mcp tools inspect | Inspect a tool |
| docker mcp tools ls | List tools |

---

# docker mcp version

# docker mcp version

| Description | Show the version information |
| --- | --- |
| Usage | docker mcp version |

## Description

Show the version information

---

# docker mcp

# docker mcp

## Subcommands

| Command | Description |
| --- | --- |
| docker mcp catalog | Manage MCP server catalogs |
| docker mcp client | Manage MCP clients |
| docker mcp config | Manage the configuration |
| docker mcp feature | Manage experimental features |
| docker mcp gateway | Manage the MCP Server gateway |
| docker mcp oauth |  |
| docker mcp policy | Manage secret policies |
| docker mcp secret | Manage secrets |
| docker mcp server | Manage servers |
| docker mcp tools | Manage tools |
| docker mcp version | Show the version information |

---

# docker model bench

# docker model bench

| Description | Benchmark a model's performance at different concurrency levels |
| --- | --- |
| Usage | docker model bench [MODEL] |

## Description

Benchmark a model's performance showing tokens per second at different concurrency levels.

This command runs a series of benchmarks with 1, 2, 4, and 8 concurrent requests by default,
measuring the tokens per second (TPS) that the model can generate.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --concurrency | [1,2,4,8] | Concurrency levels to test |
| --duration | 30s | Duration to run each concurrency test |
| --json |  | Output results in JSON format |
| --prompt | Write a comprehensive 100 word summary on whales and their impact on society. | Prompt to use for benchmarking |
| --timeout | 5m0s | Timeout for each individual request |

---

# docker model inspect

# docker model inspect

| Description | Display detailed information on one model |
| --- | --- |
| Usage | docker model inspect MODEL |

## Description

Display detailed information on one model

## Options

| Option | Default | Description |
| --- | --- | --- |
| --openai |  | List model in an OpenAI format |
| -r, --remote |  | Show info for remote models |

---

# docker model install

# docker model install-runner

| Description | Install Docker Model Runner (Docker Engine only) |
| --- | --- |
| Usage | docker model install-runner |

## Description

This command runs implicitly when a docker model command is executed. You can run this command explicitly to add a new configuration.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --backend |  | Specify backend (llama.cpp|vllm). Default: llama.cpp |
| --debug |  | Enable debug logging |
| --do-not-track |  | Do not track models usage in Docker Model Runner |
| --gpu | auto | Specify GPU support (none|auto|cuda|rocm|musa|cann) |
| --host | 127.0.0.1 | Host address to bind Docker Model Runner |
| --port |  | Docker container port for Docker Model Runner (default: 12434 for Docker Engine, 12435 for Cloud mode) |

---

# docker model list

# docker model list

| Description | List the models pulled to your local environment |
| --- | --- |
| Usage | docker model list [OPTIONS] |
| AliasesAn alias is a short or memorable alternative for a longer command. | docker model ls |

## Description

List the models pulled to your local environment

## Options

| Option | Default | Description |
| --- | --- | --- |
| --json |  | List models in a JSON format |
| --openai |  | List models in an OpenAI format |
| -q, --quiet |  | Only show model IDs |

---

# docker model logs

# docker model logs

| Description | Fetch the Docker Model Runner logs |
| --- | --- |
| Usage | docker model logs [OPTIONS] |

## Description

Fetch the Docker Model Runner logs

## Options

| Option | Default | Description |
| --- | --- | --- |
| -f, --follow |  | View logs with real-time streaming |
| --no-engines |  | Exclude inference engine logs from the output |

---

# docker model package

# docker model package

| Description | Package a GGUF file, Safetensors directory, or existing model into a Docker model OCI artifact. |
| --- | --- |
| Usage | docker model package (--gguf <path> | --safetensors-dir <path> | --from <model>) [--license <path>...] [--context-size <tokens>] [--push] MODEL |

## Description

Package a GGUF file, Safetensors directory, or existing model into a Docker model OCI artifact, with optional licenses. The package is sent to the model-runner, unless --push is specified.
When packaging a sharded GGUF model, --gguf should point to the first shard. All shard files should be siblings and should include the index in the file name (e.g. model-00001-of-00015.gguf).
When packaging a Safetensors model, --safetensors-dir should point to a directory containing .safetensors files and config files (*.json, merges.txt). All files will be auto-discovered and config files will be packaged into a tar archive.
When packaging from an existing model using --from, you can modify properties like context size to create a variant of the original model.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --chat-template |  | absolute path to chat template file (must be Jinja format) |
| --context-size |  | context size in tokens |
| --dir-tar |  | relative path to directory to package as tar (can be specified multiple times) |
| --from |  | reference to an existing model to repackage |
| --gguf |  | absolute path to gguf file |
| -l, --license |  | absolute path to a license file |
| --push |  | push to registry (if not set, the model is loaded into the Model Runner content store) |
| --safetensors-dir |  | absolute path to directory containing safetensors files and config |

---

# docker model pull

# docker model pull

| Description | Pull a model from Docker Hub or HuggingFace to your local environment |
| --- | --- |
| Usage | docker model pull MODEL |

## Description

Pull a model to your local environment. Downloaded models also appear in the Docker Desktop Dashboard.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --ignore-runtime-memory-check |  | Do not block pull if estimated runtime memory for model exceeds system resources. |

## Examples

### Pulling a model from Docker Hub

```console
docker model pull ai/smollm2
```

### Pulling from HuggingFace

You can pull GGUF models directly from [Hugging Face](https://huggingface.co/models?library=gguf).

**Note about quantization:** If no tag is specified, the command tries to pull the `Q4_K_M` version of the model.
If `Q4_K_M` doesn't exist, the command pulls the first GGUF found in the **Files** view of the model on HuggingFace.
To specify the quantization, provide it as a tag, for example:
`docker model pull hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF:Q4_K_S`

```console
docker model pull hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF
```

---

# docker model purge

# docker model purge

| Description | Remove all models |
| --- | --- |
| Usage | docker model purge [OPTIONS] |

## Description

Remove all models

## Options

| Option | Default | Description |
| --- | --- | --- |
| -f, --force |  | Forcefully remove all models |

---

# docker model push

# docker model push

| Description | Push a model to Docker Hub |
| --- | --- |
| Usage | docker model push MODEL |

## Description

Push a model to Docker Hub

---

# docker model reinstall

# docker model reinstall-runner

| Description | Reinstall Docker Model Runner (Docker Engine only) |
| --- | --- |
| Usage | docker model reinstall-runner |

## Description

This command removes the existing Docker Model Runner container and reinstalls it with the specified configuration. Models and images are preserved during reinstallation.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --backend |  | Specify backend (llama.cpp|vllm). Default: llama.cpp |
| --debug |  | Enable debug logging |
| --do-not-track |  | Do not track models usage in Docker Model Runner |
| --gpu | auto | Specify GPU support (none|auto|cuda|rocm|musa|cann) |
| --host | 127.0.0.1 | Host address to bind Docker Model Runner |
| --port |  | Docker container port for Docker Model Runner (default: 12434 for Docker Engine, 12435 for Cloud mode) |

---

# docker model restart

# docker model restart-runner

| Description | Restart Docker Model Runner (Docker Engine only) |
| --- | --- |
| Usage | docker model restart-runner |

## Description

This command restarts the Docker Model Runner without pulling container images. Use this command to restart the runner when you already have the required images locally.

For the first-time setup or to ensure you have the latest images, use `docker model install-runner` instead.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --debug |  | Enable debug logging |
| --do-not-track |  | Do not track models usage in Docker Model Runner |
| --gpu | auto | Specify GPU support (none|auto|cuda|rocm|musa|cann) |
| --host | 127.0.0.1 | Host address to bind Docker Model Runner |
| --port |  | Docker container port for Docker Model Runner (default: 12434 for Docker Engine, 12435 for Cloud mode) |

---

# docker model rm

# docker model rm

| Description | Remove local models downloaded from Docker Hub |
| --- | --- |
| Usage | docker model rm [MODEL...] |

## Description

Remove local models downloaded from Docker Hub

## Options

| Option | Default | Description |
| --- | --- | --- |
| -f, --force |  | Forcefully remove the model |

---

# docker model run

# docker model run

| Description | Run a model and interact with it using a submitted prompt or chat mode |
| --- | --- |
| Usage | docker model run MODEL [PROMPT] |

## Description

When you run a model, Docker calls an inference server API endpoint hosted by the Model Runner through Docker Desktop. The model stays in memory until another model is requested, or until a pre-defined inactivity timeout is reached (currently 5 minutes).

You do not have to use Docker model run before interacting with a specific model from a host process or from within a container. Model Runner transparently loads the requested model on-demand, assuming it has been pulled and is locally available.

You can also use chat mode in the Docker Desktop Dashboard when you select the model in the **Models** tab.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --color | no | Use colored output (auto|yes|no) |
| --debug |  | Enable debug logging |
| -d, --detach |  | Load the model in the background without interaction |
| --ignore-runtime-memory-check |  | Do not block pull if estimated runtime memory for model exceeds system resources. |

## Examples

### One-time prompt

```console
docker model run ai/smollm2 "Hi"
```

Output:

```console
Hello! How can I assist you today?
```

### Interactive chat

```console
docker model run ai/smollm2
```

Output:

```console
> Hi
Hi there! It's SmolLM, AI assistant. How can I help you today?
> /bye
```

### Pre-load a model

```console
docker model run --detach ai/smollm2
```

This loads the model into memory without interaction, ensuring maximum performance for subsequent requests.

---

# docker model start

# docker model start-runner

| Description | Start Docker Model Runner (Docker Engine only) |
| --- | --- |
| Usage | docker model start-runner |

## Description

This command starts the Docker Model Runner without pulling container images. Use this command to start the runner when you already have the required images locally.

For the first-time setup or to ensure you have the latest images, use `docker model install-runner` instead.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --backend |  | Specify backend (llama.cpp|vllm). Default: llama.cpp |
| --debug |  | Enable debug logging |
| --do-not-track |  | Do not track models usage in Docker Model Runner |
| --gpu | auto | Specify GPU support (none|auto|cuda|rocm|musa|cann) |
| --port |  | Docker container port for Docker Model Runner (default: 12434 for Docker Engine, 12435 for Cloud mode) |

---

# docker model status

# docker model status

| Description | Check if the Docker Model Runner is running |
| --- | --- |
| Usage | docker model status |

## Description

Check whether the Docker Model Runner is running and displays the current inference engine.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --json |  | Format output in JSON |

---

# docker model stop

# docker model stop-runner

| Description | Stop Docker Model Runner (Docker Engine only) |
| --- | --- |
| Usage | docker model stop-runner |

## Description

This command stops the Docker Model Runner by removing the running containers, but preserves the container images on disk. Use this command when you want to temporarily stop the runner but plan to start it again later.

To completely remove the runner including images, use `docker model uninstall-runner --images` instead.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --models |  | Remove model storage volume |

---

# docker model tag

# docker model tag

| Description | Tag a model |
| --- | --- |
| Usage | docker model tag SOURCE TARGET |

## Description

Specify a particular version or variant of the model. If no tag is provided, Docker defaults to `latest`.

---

# docker model uninstall

# docker model uninstall-runner

| Description | Uninstall Docker Model Runner (Docker Engine only) |
| --- | --- |
| Usage | docker model uninstall-runner |

## Description

Uninstall Docker Model Runner (Docker Engine only)

## Options

| Option | Default | Description |
| --- | --- | --- |
| --images |  | Remove docker/model-runner images |
| --models |  | Remove model storage volume |

---

# docker model version

# docker model version

| Description | Show the Docker Model Runner version |
| --- | --- |
| Usage | docker model version |

## Description

Show the Docker Model Runner version

---

# docker model

# docker model

| Description | Docker Model Runner |
| --- | --- |

## Description

Use Docker Model Runner to run and interact with AI models directly from the command line.
For more information, see the
[documentation](https://docs.docker.com/ai/model-runner/)

## Subcommands

| Command | Description |
| --- | --- |
| docker model bench | Benchmark a model's performance at different concurrency levels |
| docker model inspect | Display detailed information on one model |
| docker model install-runner | Install Docker Model Runner (Docker Engine only) |
| docker model list | List the models pulled to your local environment |
| docker model logs | Fetch the Docker Model Runner logs |
| docker model package | Package a GGUF file, Safetensors directory, or existing model into a Docker model OCI artifact. |
| docker model pull | Pull a model from Docker Hub or HuggingFace to your local environment |
| docker model purge | Remove all models |
| docker model push | Push a model to Docker Hub |
| docker model reinstall-runner | Reinstall Docker Model Runner (Docker Engine only) |
| docker model restart-runner | Restart Docker Model Runner (Docker Engine only) |
| docker model rm | Remove local models downloaded from Docker Hub |
| docker model run | Run a model and interact with it using a submitted prompt or chat mode |
| docker model start-runner | Start Docker Model Runner (Docker Engine only) |
| docker model status | Check if the Docker Model Runner is running |
| docker model stop-runner | Stop Docker Model Runner (Docker Engine only) |
| docker model tag | Tag a model |
| docker model uninstall-runner | Uninstall Docker Model Runner (Docker Engine only) |
| docker model version | Show the Docker Model Runner version |

---

# docker network connect

# docker network connect

| Description | Connect a container to a network |
| --- | --- |
| Usage | docker network connect [OPTIONS] NETWORK CONTAINER |

## Description

Connects a container to a network. You can connect a container by name
or by ID. Once connected, the container can communicate with other containers in
the same network.

## Options

| Option | Default | Description |
| --- | --- | --- |
| --alias |  | Add network-scoped alias for the container |
| --driver-opt |  | driver options for the network |
| --gw-priority |  | Highest gw-priority provides the default gateway. Accepts positive and negative values. |
| --ip |  | IPv4 address (e.g.,172.30.100.104) |
| --ip6 |  | IPv6 address (e.g.,2001:db8::33) |
| --link |  | Add link to another container |
| --link-local-ip |  | Add a link-local address for the container |

## Examples

### Connect a running container to a network

```console
$ docker network connect multi-host-network container1
```

### Connect a container to a network when it starts

You can also use the `docker run --network=<network-name>` option to start a
container and immediately connect it to a network.

```console
$ docker run -itd --network=multi-host-network busybox
```

### Specify the IP address a container will use on a given network (--ip)

You can specify the IP address you want to be assigned to the container's interface.

```console
$ docker network connect --ip 10.10.36.122 multi-host-network container2
```

### Use the legacy--linkoption (--link)

You can use `--link` option to link another container with a preferred alias.

```console
$ docker network connect --link container1:c1 multi-host-network container2
```

### Create a network alias for a container (--alias)

`--alias` option can be used to resolve the container by another name in the network
being connected to.

```console
$ docker network connect --alias db --alias mysql multi-host-network container2
```

### Set sysctls for a container's interface (--driver-opt)

`sysctl` settings that start with `net.ipv4.` and `net.ipv6.` can be set per-interface
using `--driver-opt` label `com.docker.network.endpoint.sysctls`. The name of the
interface must be replaced by `IFNAME`.

To set more than one `sysctl` for an interface, quote the whole value of the
`driver-opt` field, remembering to escape the quotes for the shell if necessary.
For example, if the interface to `my-net` is given name `eth3`, the following example
sets `net.ipv4.conf.eth3.log_martians=1` and `net.ipv4.conf.eth3.forwarding=0`.

```console
$ docker network connect --driver-opt=\"com.docker.network.endpoint.sysctls=net.ipv4.conf.IFNAME.log_martians=1,net.ipv4.conf.IFNAME.forwarding=0\" multi-host-network container2
```

> Note
>
> Network drivers may restrict the sysctl settings that can be modified and, to protect
> the operation of the network, new restrictions may be added in the future.

### Network implications of stopping, pausing, or restarting containers

You can pause, restart, and stop containers that are connected to a network.
A container connects to its configured networks when it runs.

If specified, the container's IP address(es) is reapplied when a stopped
container is restarted. If the IP address is no longer available, the container
fails to start. One way to guarantee that the IP address is available is
to specify an `--ip-range` when creating the network, and choose the static IP
address(es) from outside that range. This ensures that the IP address is not
given to another container while this container is not on the network.

```console
$ docker network create --subnet 172.20.0.0/16 --ip-range 172.20.240.0/20 multi-host-network
```

```console
$ docker network connect --ip 172.20.128.2 multi-host-network container2
```

To verify the container is connected, use the `docker network inspect` command.
Use `docker network disconnect` to remove a container from the network.

Once connected in network, containers can communicate using only another
container's IP address or name. For `overlay` networks or custom plugins that
support multi-host connectivity, containers connected to the same multi-host
network but launched from different Engines can also communicate in this way.

You can connect a container to one or more networks. The networks need not be
the same type. For example, you can connect a single container bridge and overlay
networks.
