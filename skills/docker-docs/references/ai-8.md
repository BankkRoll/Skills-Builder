# Inference engines and more

# Inference engines

> Learn about the llama.cpp, vLLM, and Diffusers inference engines in Docker Model Runner.

# Inference engines

   Table of contents

---

Docker Model Runner supports three inference engines: **llama.cpp**, **vLLM**, and **Diffusers**.
Each engine has different strengths, supported platforms, and model format
requirements. This guide helps you choose the right engine and configure it for
your use case.

## Engine comparison

| Feature | llama.cpp | vLLM | Diffusers |
| --- | --- | --- | --- |
| Model formats | GGUF | Safetensors, HuggingFace | DDUF |
| Platforms | All (macOS, Windows, Linux) | Linux x86_64 only | Linux (x86_64, ARM64) |
| GPU support | NVIDIA, AMD, Apple Silicon, Vulkan | NVIDIA CUDA only | NVIDIA CUDA only |
| CPU inference | Yes | No | No |
| Quantization | Built-in (Q4, Q5, Q8, etc.) | Limited | Limited |
| Memory efficiency | High (with quantization) | Moderate | Moderate |
| Throughput | Good | High (with batching) | Good |
| Best for | Local development, resource-constrained environments | Production, high throughput | Image generation |
| Use case | Text generation (LLMs) | Text generation (LLMs) | Image generation (Stable Diffusion) |

## llama.cpp

[llama.cpp](https://github.com/ggerganov/llama.cpp) is the default inference
engine in Docker Model Runner. It's designed for efficient local inference and
supports a wide range of hardware configurations.

### Platform support

| Platform | GPU support | Notes |
| --- | --- | --- |
| macOS (Apple Silicon) | Metal | Automatic GPU acceleration |
| Windows (x64) | NVIDIA CUDA | Requires NVIDIA drivers 576.57+ |
| Windows (ARM64) | Adreno OpenCL | Qualcomm 6xx series and later |
| Linux (x64) | NVIDIA, AMD, Vulkan | Multiple backend options |
| Linux | CPU only | Works on any x64/ARM64 system |

### Model format: GGUF

llama.cpp uses the GGUF format, which supports efficient quantization for reduced
memory usage without significant quality loss.

#### Quantization levels

| Quantization | Bits per weight | Memory usage | Quality |
| --- | --- | --- | --- |
| Q2_K | ~2.5 | Lowest | Reduced |
| Q3_K_M | ~3.5 | Minimal | Acceptable |
| Q4_K_M | ~4.5 | Low | Good |
| Q5_K_M | ~5.5 | Moderate | Excellent |
| Q6_K | ~6.5 | Higher | Excellent |
| Q8_0 | 8 | High | Near-original |
| F16 | 16 | Highest | Original |

**Recommended**: Q4_K_M offers the best balance of quality and memory usage for
most use cases.

#### Pulling quantized models

Models on Docker Hub often include quantization in the tag:

```console
$ docker model pull ai/llama3.2:3B-Q4_K_M
```

### Using llama.cpp

llama.cpp is the default engine. No special configuration is required:

```console
$ docker model run ai/smollm2
```

To explicitly specify llama.cpp when running models:

```console
$ docker model run ai/smollm2 --backend llama.cpp
```

### llama.cpp API endpoints

When using llama.cpp, API calls use the llama.cpp engine path:

```text
POST /engines/llama.cpp/v1/chat/completions
```

Or without the engine prefix:

```text
POST /engines/v1/chat/completions
```

## vLLM

[vLLM](https://github.com/vllm-project/vllm) is a high-performance inference
engine optimized for production workloads with high throughput requirements.

### Platform support

| Platform | GPU | Support status |
| --- | --- | --- |
| Linux x86_64 | NVIDIA CUDA | Supported |
| Windows with WSL2 | NVIDIA CUDA | Supported (Docker Desktop 4.54+) |
| macOS | - | Not supported |
| Linux ARM64 | - | Not supported |
| AMD GPUs | - | Not supported |

> Important
>
> vLLM requires an NVIDIA GPU with CUDA support. It does not support CPU-only
> inference.

### Model format: Safetensors

vLLM works with models in Safetensors format, which is the standard format for
HuggingFace models. These models typically use more memory than quantized GGUF
models but may offer better quality and faster inference on powerful hardware.

### Setting up vLLM

#### Docker Engine (Linux)

Install the Model Runner with vLLM backend:

```console
$ docker model install-runner --backend vllm --gpu cuda
```

Verify the installation:

```console
$ docker model status
Docker Model Runner is running

Status:
llama.cpp: running llama.cpp version: c22473b
vllm: running vllm version: 0.11.0
```

#### Docker Desktop (Windows with WSL2)

1. Ensure you have:
  - Docker Desktop 4.54 or later
  - NVIDIA GPU with updated drivers
  - WSL2 enabled
2. Install vLLM backend:
  ```console
  $ docker model install-runner --backend vllm --gpu cuda
  ```

### Running models with vLLM

vLLM models are typically tagged with `-vllm` suffix:

```console
$ docker model run ai/smollm2-vllm
```

To specify the vLLM backend explicitly:

```console
$ docker model run ai/model --backend vllm
```

### vLLM API endpoints

When using vLLM, specify the engine in the API path:

```text
POST /engines/vllm/v1/chat/completions
```

### vLLM configuration

#### HuggingFace overrides

Use `--hf_overrides` to pass model configuration overrides:

```console
$ docker model configure --hf_overrides '{"max_model_len": 8192}' ai/model-vllm
```

#### Common vLLM settings

| Setting | Description | Example |
| --- | --- | --- |
| max_model_len | Maximum context length | 8192 |
| gpu_memory_utilization | Fraction of GPU memory to use | 0.9 |
| tensor_parallel_size | GPUs for tensor parallelism | 2 |

### vLLM and llama.cpp performance comparison

| Scenario | Recommended engine |
| --- | --- |
| Single user, local development | llama.cpp |
| Multiple concurrent requests | vLLM |
| Limited GPU memory | llama.cpp (with quantization) |
| Maximum throughput | vLLM |
| CPU-only system | llama.cpp |
| Apple Silicon Mac | llama.cpp |
| Production deployment | vLLM (if hardware supports it) |

## Diffusers

[Diffusers](https://github.com/huggingface/diffusers) is an inference engine
for image generation models, including Stable Diffusion. Unlike llama.cpp and
vLLM which focus on text generation with LLMs, Diffusers enables you to generate
images from text prompts.

### Platform support

| Platform | GPU | Support status |
| --- | --- | --- |
| Linux x86_64 | NVIDIA CUDA | Supported |
| Linux ARM64 | NVIDIA CUDA | Supported |
| Windows | - | Not supported |
| macOS | - | Not supported |

> Important
>
> Diffusers requires an NVIDIA GPU with CUDA support. It does not support
> CPU-only inference.

### Setting up Diffusers

Install the Model Runner with Diffusers backend:

```console
$ docker model reinstall-runner --backend diffusers --gpu cuda
```

Verify the installation:

```console
$ docker model status
Docker Model Runner is running

Status:
llama.cpp: running llama.cpp version: 34ce48d
mlx: not installed
sglang: sglang package not installed
vllm: vLLM binary not found
diffusers: running diffusers version: 0.36.0
```

### Pulling Diffusers models

Pull a Stable Diffusion model:

```console
$ docker model pull stable-diffusion:Q4
```

### Generating images with Diffusers

Diffusers uses an image generation API endpoint. To generate an image:

```console
$ curl -s -X POST http://localhost:12434/engines/diffusers/v1/images/generations \
  -H "Content-Type: application/json" \
  -d '{
    "model": "stable-diffusion:Q4",
    "prompt": "A picture of a nice cat",
    "size": "512x512"
  }' | jq -r '.data[0].b64_json' | base64 -d > image.png
```

This command:

1. Sends a POST request to the Diffusers image generation endpoint
2. Specifies the model, prompt, and output image size
3. Extracts the base64-encoded image from the response
4. Decodes it and saves it as `image.png`

### Diffusers API endpoint

When using Diffusers, specify the engine in the API path:

```text
POST /engines/diffusers/v1/images/generations
```

### Supported parameters

| Parameter | Type | Description |
| --- | --- | --- |
| model | string | Required. The model identifier (e.g.,stable-diffusion:Q4). |
| prompt | string | Required. The text description of the image to generate. |
| size | string | Image dimensions inWIDTHxHEIGHTformat (e.g.,512x512). |

## Running multiple engines

You can run llama.cpp, vLLM, and Diffusers simultaneously. Docker Model Runner routes
requests to the appropriate engine based on the model or explicit engine selection.

Check which engines are running:

```console
$ docker model status
Docker Model Runner is running

Status:
llama.cpp: running llama.cpp version: 34ce48d
mlx: not installed
sglang: sglang package not installed
vllm: running vllm version: 0.11.0
diffusers: running diffusers version: 0.36.0
```

### Engine-specific API paths

| Engine | API path | Use case |
| --- | --- | --- |
| llama.cpp | /engines/llama.cpp/v1/chat/completions | Text generation |
| vLLM | /engines/vllm/v1/chat/completions | Text generation |
| Diffusers | /engines/diffusers/v1/images/generations | Image generation |
| Auto-select | /engines/v1/chat/completions | Text generation (auto-selects engine) |

## Managing inference engines

### Install an engine

```console
$ docker model install-runner --backend <engine> [--gpu <type>]
```

Options:

- `--backend`: `llama.cpp`, `vllm`, or `diffusers`
- `--gpu`: `cuda`, `rocm`, `vulkan`, or `metal` (depends on platform)

### Reinstall an engine

```console
$ docker model reinstall-runner --backend <engine>
```

### Check engine status

```console
$ docker model status
```

### View engine logs

```console
$ docker model logs
```

## Packaging models for each engine

### Package a GGUF model (llama.cpp)

```console
$ docker model package --gguf ./model.gguf --push myorg/mymodel:Q4_K_M
```

### Package a Safetensors model (vLLM)

```console
$ docker model package --safetensors ./model/ --push myorg/mymodel-vllm
```

## Troubleshooting

### vLLM won't start

1. Verify NVIDIA GPU is available:
  ```console
  $ nvidia-smi
  ```
2. Check Docker has GPU access:
  ```console
  $ docker run --rm --gpus all nvidia/cuda:12.0-base nvidia-smi
  ```
3. Verify you're on a supported platform (Linux x86_64 or Windows WSL2).

### llama.cpp is slow

1. Ensure GPU acceleration is working (check logs for Metal/CUDA messages).
2. Try a more aggressive quantization:
  ```console
  $ docker model pull ai/model:Q4_K_M
  ```
3. Reduce context size:
  ```console
  $ docker model configure --context-size 2048 ai/model
  ```

### Out of memory errors

1. Use a smaller quantization (Q4 instead of Q8).
2. Reduce context size.
3. For vLLM, adjust `gpu_memory_utilization`:
  ```console
  $ docker model configure --hf_overrides '{"gpu_memory_utilization": 0.8}' ai/model
  ```

## What's next

- [Configuration options](https://docs.docker.com/ai/model-runner/configuration/) - Detailed parameter reference
- [API reference](https://docs.docker.com/ai/model-runner/api-reference/) - API documentation
- [GPU support](https://docs.docker.com/desktop/features/gpu/) - GPU configuration for Docker Desktop

---

# Open WebUI integration

> Set up Open WebUI as a ChatGPT-like interface for Docker Model Runner.

# Open WebUI integration

   Table of contents

---

[Open WebUI](https://github.com/open-webui/open-webui) is an open-source,
self-hosted web interface that provides a ChatGPT-like experience for local
AI models. You can connect it to Docker Model Runner to get a polished chat
interface for your models.

## Prerequisites

- Docker Model Runner enabled with TCP access
- A model pulled (e.g., `docker model pull ai/llama3.2`)

## Quick start with Docker Compose

The easiest way to run Open WebUI with Docker Model Runner is using Docker Compose.

Create a `compose.yaml` file:

```yaml
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    ports:
      - "3000:8080"
    environment:
      - OLLAMA_BASE_URL=http://host.docker.internal:12434
      - WEBUI_AUTH=false
    extra_hosts:
      - "host.docker.internal:host-gateway"
    volumes:
      - open-webui:/app/backend/data

volumes:
  open-webui:
```

Start the services:

```console
$ docker compose up -d
```

Open your browser to [http://localhost:3000](http://localhost:3000).

## Configuration options

### Environment variables

| Variable | Description | Default |
| --- | --- | --- |
| OLLAMA_BASE_URL | URL of Docker Model Runner | Required |
| WEBUI_AUTH | Enable authentication | true |
| OPENAI_API_BASE_URL | Use OpenAI-compatible API instead | - |
| OPENAI_API_KEY | API key (use any value for DMR) | - |

### Using OpenAI-compatible API

If you prefer to use the OpenAI-compatible API instead of the Ollama API:

```yaml
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    ports:
      - "3000:8080"
    environment:
      - OPENAI_API_BASE_URL=http://host.docker.internal:12434/engines/v1
      - OPENAI_API_KEY=not-needed
      - WEBUI_AUTH=false
    extra_hosts:
      - "host.docker.internal:host-gateway"
    volumes:
      - open-webui:/app/backend/data

volumes:
  open-webui:
```

## Network configuration

### Docker Desktop

On Docker Desktop, `host.docker.internal` automatically resolves to the host machine.
The previous example works without modification.

### Docker Engine (Linux)

On Docker Engine, you may need to configure the network differently:

```yaml
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    network_mode: host
    environment:
      - OLLAMA_BASE_URL=http://localhost:12434
      - WEBUI_AUTH=false
    volumes:
      - open-webui:/app/backend/data

volumes:
  open-webui:
```

Or use the host gateway:

```yaml
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    ports:
      - "3000:8080"
    environment:
      - OLLAMA_BASE_URL=http://172.17.0.1:12434
      - WEBUI_AUTH=false
    volumes:
      - open-webui:/app/backend/data

volumes:
  open-webui:
```

## Using Open WebUI

### Select a model

1. Open [http://localhost:3000](http://localhost:3000)
2. Select the model drop-down in the top-left
3. Select from your pulled models (they appear with `ai/` prefix)

### Pull models through the UI

Open WebUI can pull models directly:

1. Select the model drop-down
2. Enter a model name: `ai/llama3.2`
3. Select the download icon

### Chat features

Open WebUI provides:

- Multi-turn conversations with context
- Message editing and regeneration
- Code syntax highlighting
- Markdown rendering
- Conversation history and search
- Export conversations

## Complete example with multiple models

This example sets up Open WebUI with Docker Model Runner and pre-pulls several models:

```yaml
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    ports:
      - "3000:8080"
    environment:
      - OLLAMA_BASE_URL=http://host.docker.internal:12434
      - WEBUI_AUTH=false
      - DEFAULT_MODELS=ai/llama3.2
    extra_hosts:
      - "host.docker.internal:host-gateway"
    volumes:
      - open-webui:/app/backend/data
    depends_on:
      model-setup:
        condition: service_completed_successfully

  model-setup:
    image: docker:cli
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    command: >
      sh -c "
        docker model pull ai/llama3.2 &&
        docker model pull ai/qwen2.5-coder &&
        docker model pull ai/smollm2
      "

volumes:
  open-webui:
```

## Enabling authentication

For multi-user setups or security, enable authentication:

```yaml
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    ports:
      - "3000:8080"
    environment:
      - OLLAMA_BASE_URL=http://host.docker.internal:12434
      - WEBUI_AUTH=true
    extra_hosts:
      - "host.docker.internal:host-gateway"
    volumes:
      - open-webui:/app/backend/data

volumes:
  open-webui:
```

On first visit, you'll create an admin account.

## Troubleshooting

### Models don't appear in the drop-down

1. Verify Docker Model Runner is accessible:
  ```console
  $ curl http://localhost:12434/api/tags
  ```
2. Check that models are pulled:
  ```console
  $ docker model list
  ```
3. Verify the `OLLAMA_BASE_URL` is correct and accessible from the container.

### "Connection refused" errors

1. Ensure TCP access is enabled for Docker Model Runner.
2. On Docker Desktop, verify `host.docker.internal` resolves:
  ```console
  $ docker run --rm alpine ping -c 1 host.docker.internal
  ```
3. On Docker Engine, try using `network_mode: host` or the explicit host IP.

### Slow response times

1. First requests load the model into memory, which takes time.
2. Subsequent requests are much faster.
3. If consistently slow, consider:
  - Using a smaller model
  - Reducing context size
  - Checking GPU acceleration is working

### CORS errors

If running Open WebUI on a different host:

1. In Docker Desktop, go to Settings > AI
2. Add the Open WebUI URL to **CORS Allowed Origins**

## Customization

### Custom system prompts

Open WebUI supports setting system prompts per model. Configure these in the UI under Settings > Models.

### Model parameters

Adjust model parameters in the chat interface:

1. Select the settings icon next to the model name
2. Adjust temperature, top-p, max tokens, etc.

These settings are passed through to Docker Model Runner.

## Running on a different port

To run Open WebUI on a different port:

```yaml
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    ports:
      - "8080:8080"  # Change first port number
    # ... rest of config
```

## What's next

- [API reference](https://docs.docker.com/ai/model-runner/api-reference/) - Learn about the APIs Open WebUI uses
- [Configuration options](https://docs.docker.com/ai/model-runner/configuration/) - Tune model behavior
- [IDE integrations](https://docs.docker.com/ai/model-runner/ide-integrations/) - Connect other tools to DMR

---

# Docker Model Runner

> Learn how to use Docker Model Runner to manage and run AI models.

# Docker Model Runner

   Table of contents

---

Requires: Docker Engine or Docker Desktop (Windows) 4.41+ or Docker Desktop (MacOS) 4.40+ For: See Requirements section below

Docker Model Runner (DMR) makes it easy to manage, run, and
deploy AI models using Docker. Designed for developers,
Docker Model Runner streamlines the process of pulling, running, and serving
large language models (LLMs) and other AI models directly from Docker Hub or any
OCI-compliant registry.

With seamless integration into Docker Desktop and Docker
Engine, you can serve models via OpenAI and Ollama-compatible APIs, package GGUF files as
OCI Artifacts, and interact with models from both the command line and graphical
interface.

Whether you're building generative AI applications, experimenting with machine
learning workflows, or integrating AI into your software development lifecycle,
Docker Model Runner provides a consistent, secure, and efficient way to work
with AI models locally.

## Key features

- [Pull and push models to and from Docker Hub](https://hub.docker.com/u/ai)
- Serve models on [OpenAI and Ollama-compatible APIs](https://docs.docker.com/ai/model-runner/api-reference/) for easy integration with existing apps
- Support for [llama.cpp, vLLM, and Diffusers inference engines](https://docs.docker.com/ai/model-runner/inference-engines/) (vLLM and Diffusers on Linux with NVIDIA GPUs)
- [Generate images from text prompts](https://docs.docker.com/ai/model-runner/inference-engines/#diffusers) using Stable Diffusion models with the Diffusers backend
- Package GGUF and Safetensors files as OCI Artifacts and publish them to any Container Registry
- Run and interact with AI models directly from the command line or from the Docker Desktop GUI
- [Connect to AI coding tools](https://docs.docker.com/ai/model-runner/ide-integrations/) like Cline, Continue, Cursor, and Aider
- [Configure context size and model parameters](https://docs.docker.com/ai/model-runner/configuration/) to tune performance
- [Set up Open WebUI](https://docs.docker.com/ai/model-runner/openwebui-integration/) for a ChatGPT-like web interface
- Manage local models and display logs
- Display prompt and response details
- Conversational context support for multi-turn interactions

## Requirements

Docker Model Runner is supported on the following platforms:

Windows(amd64):

- NVIDIA GPUs
- NVIDIA drivers 576.57+

Windows(arm64):

- OpenCL for Adreno
- Qualcomm Adreno GPU (6xx series and later)
  > Note
  >
  > Some llama.cpp features might not be fully supported on the 6xx series.

- Apple Silicon

Docker Engine only:

- Supports CPU, NVIDIA (CUDA), AMD (ROCm), and Vulkan backends
- Requires NVIDIA driver 575.57.08+ when using NVIDIA GPUs

## How Docker Model Runner works

Models are pulled from Docker Hub the first time you use them and are stored
locally. They load into memory only at runtime when a request is made, and
unload when not in use to optimize resources. Because models can be large, the
initial pull may take some time. After that, they're cached locally for faster
access. You can interact with the model using
[OpenAI and Ollama-compatible APIs](https://docs.docker.com/ai/model-runner/api-reference/).

### Inference engines

Docker Model Runner supports three inference engines:

| Engine | Best for | Model format |
| --- | --- | --- |
| llama.cpp | Local development, resource efficiency | GGUF (quantized) |
| vLLM | Production, high throughput | Safetensors |
| Diffusers | Image generation (Stable Diffusion) | Safetensors |

llama.cpp is the default engine and works on all platforms. vLLM requires NVIDIA GPUs and is supported on Linux x86_64 and Windows with WSL2. Diffusers enables image generation and requires NVIDIA GPUs on Linux (x86_64 or ARM64). See [Inference engines](https://docs.docker.com/ai/model-runner/inference-engines/) for detailed comparison and setup.

### Context size

Models have a configurable context size (context length) that determines how many tokens they can process. The default varies by model but is typically 2,048-8,192 tokens. You can adjust this per-model:

```console
$ docker model configure --context-size 8192 ai/qwen2.5-coder
```

See [Configuration options](https://docs.docker.com/ai/model-runner/configuration/) for details on context size and other parameters.

> Tip
>
> Using Testcontainers or Docker Compose?
> [Testcontainers for Java](https://java.testcontainers.org/modules/docker_model_runner/)
> and [Go](https://golang.testcontainers.org/modules/dockermodelrunner/), and
> [Docker Compose](https://docs.docker.com/ai/compose/models-and-compose/) now support Docker
> Model Runner.

## Known issues

### docker modelis not recognised

If you run a Docker Model Runner command and see:

```text
docker: 'model' is not a docker command
```

It means Docker can't find the plugin because it's not in the expected CLI plugins directory.

To fix this, create a symlink so Docker can detect it:

```console
$ ln -s /Applications/Docker.app/Contents/Resources/cli-plugins/docker-model ~/.docker/cli-plugins/docker-model
```

Once linked, rerun the command.

## Privacy and data collection

Docker Model Runner respects your privacy settings in Docker Desktop. Data collection is controlled by the **Send usage statistics** setting:

- **Disabled**: No usage data is collected
- **Enabled**: Only minimal, non-personal data is collected:
  - [Model names](https://github.com/docker/model-runner/blob/eb76b5defb1a598396f99001a500a30bbbb48f01/pkg/metrics/metrics.go#L96) (via HEAD requests to Docker Hub)
  - User agent information
  - Whether requests originate from the host or containers

When using Docker Model Runner with Docker Engine, HEAD requests to Docker Hub are made to track model names, regardless of any settings.

No prompt content, responses, or personally identifiable information is ever collected.

## Share feedback

Thanks for trying out Docker Model Runner. To report bugs or request features, [open an issue on GitHub](https://github.com/docker/model-runner/issues). You can also give feedback through the **Give feedback** link next to the **Enable Docker Model Runner** setting.

## Next steps

- [Get started with DMR](https://docs.docker.com/ai/model-runner/get-started/) - Enable DMR and run your first model
- [API reference](https://docs.docker.com/ai/model-runner/api-reference/) - OpenAI and Ollama-compatible API documentation
- [Configuration options](https://docs.docker.com/ai/model-runner/configuration/) - Context size and runtime parameters
- [Inference engines](https://docs.docker.com/ai/model-runner/inference-engines/) - llama.cpp, vLLM, and Diffusers details
- [IDE integrations](https://docs.docker.com/ai/model-runner/ide-integrations/) - Connect Cline, Continue, Cursor, and more
- [Open WebUI integration](https://docs.docker.com/ai/model-runner/openwebui-integration/) - Set up a web chat interface

---

# Supported agents

> AI coding agents supported by Docker Sandboxes with experimental status and configuration details.

# Supported agents

   Table of contents

---

Availability: Experimental
Requires: Docker Desktop
[4.58](https://docs.docker.com/desktop/release-notes/#4580) or later

Docker Sandboxes supports multiple AI coding agents. All agents run isolated
inside microVMs with private Docker daemons.

## Supported agents

| Agent | Command | Status | Notes |
| --- | --- | --- | --- |
| Claude Code | claude | Experimental | Most tested implementation |
| Codex | codex | Experimental | In development |
| Gemini | gemini | Experimental | In development |
| cagent | cagent | Experimental | In development |
| Kiro | kiro | Experimental | In development |

## Experimental status

All agents are experimental features. This means:

- Breaking changes may occur between Docker Desktop versions
- Features may be incomplete or change significantly
- Stability and performance are not production-ready
- Limited support and documentation

Use sandboxes for development and testing, not production workloads.

## Using different agents

The agent type is specified when creating a sandbox:

```console
$ docker sandbox create claude ~/my-project
$ docker sandbox create codex ~/my-project
$ docker sandbox create gemini ~/my-project
$ docker sandbox create cagent ~/my-project
$ docker sandbox create kiro ~/my-project
```

Each agent runs in its own isolated sandbox. The agent type is bound to the
sandbox when created and cannot be changed later.

## Agent-specific configuration

Different agents may require different authentication methods or configuration.
See the agent-specific documentation:

- [Claude Code configuration](https://docs.docker.com/ai/sandboxes/claude-code/)

## Requirements

- Docker Desktop 4.58 or later
- Platform support:
  - macOS with virtualization.framework
  - Windows with Hyper-V
    Experimental
- API keys or credentials for your chosen agent

## Next steps

- [Claude Code configuration](https://docs.docker.com/ai/sandboxes/claude-code/)
- [Custom templates](https://docs.docker.com/ai/sandboxes/templates/)
- [Using sandboxes effectively](https://docs.docker.com/ai/sandboxes/workflows/)

---

# Architecture

> Technical architecture of Docker Sandboxes including microVM isolation, private Docker daemon, and workspace syncing.

# Architecture

   Table of contents

---

Availability: Experimental
Requires: Docker Desktop
[4.58](https://docs.docker.com/desktop/release-notes/#4580) or later

This page explains how Docker Sandboxes works and the design decisions behind
it.

## Why microVMs?

AI coding agents need to build images, run containers, and use Docker Compose.
Giving an agent access to your host Docker daemon means it can see your
containers, pull images, and run workloads directly on your system. That's too
much access for autonomous code execution.

Running the agent in a container doesn't solve this. Containers share the host
kernel (or in the case of Docker Desktop, share the same virtual machine) and
can't safely isolate something that needs its own Docker daemon.
Docker-in-Docker approaches either compromise isolation (privileged mode with
host socket mounting) or create nested daemon complexity.

MicroVMs provide the isolation boundary needed. Each sandbox gets its own VM
with a private Docker daemon. The agent can build images, start containers, and
run tests without any access to your host Docker environment. When you remove
the sandbox, everything inside - images, containers, packages - is gone.

## Isolation model

### Private Docker daemon per sandbox

Each sandbox runs a complete Docker daemon inside its VM. This daemon is
isolated from your host and from other sandboxes.

```plaintext
Host system (your Docker Desktop)
  ├── Your containers and images
  │
  ├── Sandbox VM 1
  │   ├── Docker daemon (isolated)
  │   ├── Agent container
  │   └── Other containers (created by agent)
  │
  └── Sandbox VM 2
      ├── Docker daemon (isolated)
      └── Agent container
```

When an agent runs `docker build` or `docker compose up`, those commands
execute inside the sandbox using the private daemon. The agent sees only
containers it creates. It cannot access your host containers, images, or
volumes.

This architecture solves a fundamental constraint: autonomous agents need full
Docker capabilities but cannot safely share your Docker daemon.

### Hypervisor-level isolation

Sandboxes use your system's native virtualization:

- macOS: virtualization.framework
- Windows: Hyper-V
  Experimental

This provides hypervisor-level isolation between the sandbox and your host.
Unlike containers (which share the host kernel), VMs have separate kernels and
cannot access host resources outside their defined boundaries.

### What this means for security

The VM boundary provides:

- Process isolation - Agent processes run in a separate kernel
- Filesystem isolation - Only your workspace is accessible
- Network isolation - Sandboxes cannot reach each other
- Docker isolation - No access to host daemon, containers, or images

Network filtering adds an additional control layer for HTTP/HTTPS traffic. See
[Network policies](https://docs.docker.com/ai/sandboxes/network-policies/) for details on that mechanism.

## Workspace syncing

### Bidirectional file sync

Your workspace syncs to the sandbox at the same absolute path:

- Host: `/Users/alice/projects/myapp`
- Sandbox: `/Users/alice/projects/myapp`

Changes sync both ways. Edit a file on your host, and the agent sees it. The
agent modifies a file, and you see the change on your host.

This is file synchronization, not volume mounting. Files are copied between
host and VM. This approach works across different filesystems and maintains
consistent paths regardless of platform differences.

### Path preservation

Preserving absolute paths means:

- File paths in error messages match between host and sandbox
- Hard-coded paths in configuration files work correctly
- Build outputs reference paths you can find on your host

The agent sees the same directory structure you see, reducing confusion when
debugging issues or reviewing changes.

## Storage and persistence

### What persists

When you create a sandbox, these persist until you remove it:

- Docker images and containers - Built or pulled by the agent
- Installed packages - System packages added with apt, yum, etc.
- Agent state - Credentials, configuration, history
- Workspace changes - Files created or modified sync back to host

### What's ephemeral

Sandboxes are lightweight but not stateless. They persist between runs but are
isolated from each other. Each sandbox maintains its own:

- Docker daemon state
- Image cache
- Package installations

When you remove a sandbox with `docker sandbox rm`, the entire VM and its
contents are deleted. Images built inside the sandbox, packages installed, and
any state not synced to your workspace are gone.

### Disk usage

Each sandbox consumes disk space for:

- VM disk image (grows as you build images and install packages)
- Docker images pulled or built inside the sandbox
- Container layers and volumes

Multiple sandboxes do not share images or layers. Each has its own isolated
Docker daemon and storage.

## Networking

### Internet access

Sandboxes have outbound internet access through your host's network connection.
Agents can install packages, pull images, and access APIs.

An HTTP/HTTPS filtering proxy runs on your host and is available at
`host.docker.internal:3128`. Agents automatically use this proxy for outbound
web requests. You can configure network policies to control which destinations
are allowed. See [Network policies](https://docs.docker.com/ai/sandboxes/network-policies/).

### Sandbox isolation

Sandboxes cannot communicate with each other. Each VM has its own private
network namespace. An agent in one sandbox cannot reach services or containers
in another sandbox.

Sandboxes also cannot access your host's `localhost` services. The VM boundary
prevents direct access to services running on your host machine.

## Lifecycle

### Creating and running

`docker sandbox run` initializes a VM with a workspace for a specified agent,
and starts the agent inside an existing sandbox. You can stop and restart the
agent without recreating the VM, preserving installed packages and Docker
images.

`docker sandbox create` initializes the VM with a workspace but doesn't start
the agent automatically. This separates environment setup from agent execution.

### State management

Sandboxes persist until explicitly removed. Stopping an agent doesn't delete
the VM. This means:

- Installed packages remain available
- Built images stay cached
- Environment setup persists between runs

Use `docker sandbox rm` to delete a sandbox and reclaim disk space.

## Comparison to alternatives

Understanding when to use sandboxes versus other approaches:

| Approach | Isolation | Agent Docker access | Host impact | Use case |
| --- | --- | --- | --- | --- |
| Sandboxes (microVMs) | Hypervisor-level | Private daemon | None - fully isolated | Autonomous agents building/running containers |
| Container with socket mount | Kernel namespaces | Host daemon (shared) | Agent sees all host containers | Trusted tools that need Docker CLI |
| Docker-in-Docker | Nested containers | Private daemon (complex) | Moderate - privileged mode required | CI/CD environments |
| Host execution | None | Host daemon | Full - direct system access | Manual development by trusted humans |

Sandboxes trade higher resource overhead (VM + daemon) for complete isolation.
Use containers when you need lightweight packaging without Docker access. Use
sandboxes when you need to give something autonomous full Docker capabilities
without trusting it with your host environment.

## Next steps

- [Network policies](https://docs.docker.com/ai/sandboxes/network-policies/)
- [Custom templates](https://docs.docker.com/ai/sandboxes/templates/)
- [Using sandboxes effectively](https://docs.docker.com/ai/sandboxes/workflows/)

---

# Configure Claude Code

> Learn how to configure Claude Code authentication, pass CLI options, and customize your sandboxed agent environment with Docker.

# Configure Claude Code

   Table of contents

---

Availability: Experimental
Requires: Docker Desktop
[4.58](https://docs.docker.com/desktop/release-notes/#4580) or later

This guide covers authentication, configuration files, and common options for
running Claude Code in a sandboxed environment.

## Quick start

To create a sandbox and run Claude Code for a project directory:

```console
$ docker sandbox run claude ~/my-project
```

### Pass a prompt directly

Start Claude with a specific prompt:

```console
$ docker sandbox run <sandbox-name> -- "Add error handling to the login function"
```

Or:

```console
$ docker sandbox run <sandbox-name> -- "$(cat prompt.txt)"
```

This starts Claude and immediately processes the prompt.

## Authentication

Claude Code requires an Anthropic API key. You can authenticate using an environment variable (recommended) or through interactive login.

### Environment variable (recommended)

The recommended approach is to set the `ANTHROPIC_API_KEY` environment variable in your shell configuration file.

Docker Sandboxes use a daemon process that doesn't inherit environment
variables from your current shell session. To make your API key available to
sandboxes, set it globally in your shell configuration file.

Add the API key to your shell configuration file:

~/.bashrc or ~/.zshrc

```plaintext
export ANTHROPIC_API_KEY=sk-ant-api03-xxxxx
```

Apply the changes:

1. Source your shell configuration: `source ~/.bashrc` (or `~/.zshrc`)
2. Restart Docker Desktop so the daemon picks up the new environment variable
3. Create and run your sandbox:

```console
$ docker sandbox create claude ~/project
$ docker sandbox run <sandbox-name>
```

The sandbox detects the environment variable and uses it automatically.

### Interactive authentication

If no credentials are found, Claude Code prompts you to authenticate interactively when it starts. You can also trigger the login flow manually using the `/login` command within Claude Code.

When using interactive authentication:

- You'll need to authenticate for each workspace/sandbox separately
- If the sandbox is removed or destroyed, you'll need to authenticate again when you recreate it
- Authentication sessions aren't persisted outside the sandbox

To avoid repeated authentication, use the `ANTHROPIC_API_KEY` environment variable method described above.

## Configuration

Claude Code can be configured through CLI options. Any arguments you pass after
the sandbox name and a `--` separator are passed directly to Claude Code.

Pass options after the sandbox name:

```console
$ docker sandbox run <sandbox-name> -- [claude-options]
```

For example:

```console
$ docker sandbox run <sandbox-name> -- --continue
```

See the [Claude Code CLI reference](https://docs.claude.com/en/docs/claude-code/cli-reference)
for available options.

## Base image

The Claude Code sandbox template is a container image that runs inside the
sandbox VM. It includes:

- Ubuntu-based environment with Claude Code
- Development tools: Docker CLI, GitHub CLI, Node.js, Go, Python 3, Git, ripgrep, jq
- Non-root `agent` user with sudo access
- Private Docker daemon for running additional containers

Claude launches with `--dangerously-skip-permissions` by default in sandboxes.

You can build custom templates based on `docker/sandbox-templates:claude-code`.
See [Custom templates](https://docs.docker.com/ai/sandboxes/templates/) for details.

## Next steps

- [Using sandboxes effectively](https://docs.docker.com/ai/sandboxes/workflows/)
- [Custom templates](https://docs.docker.com/ai/sandboxes/templates/)
- [Network policies](https://docs.docker.com/ai/sandboxes/network-policies/)
- [Troubleshooting](https://docs.docker.com/ai/sandboxes/troubleshooting/)
- [CLI Reference](https://docs.docker.com/reference/cli/docker/sandbox/)

---

# Get started with Docker Sandboxes

> Run Claude Code in an isolated sandbox. Quick setup guide with prerequisites and essential commands.

# Get started with Docker Sandboxes

   Table of contents

---

Availability: Experimental
Requires: Docker Desktop
[4.58](https://docs.docker.com/desktop/release-notes/#4580) or later

This guide shows how to run Claude Code in an isolated sandbox for the first time.

> Note
>
> Upgrading from an earlier version of Docker Desktop? See the
> [migration guide](https://docs.docker.com/ai/sandboxes/migration/) for information about the new microVM
> architecture.

## Prerequisites

Before you begin, ensure you have:

- Docker Desktop 4.58 or later
- macOS, or Windows
  Experimental
- A Claude API key (can be provided via environment variable or interactively)

## Run your first sandbox

Follow these steps to run Claude Code:

1. (Optional but recommended) Set your Anthropic API key as an environment variable.
  Add the API key to your shell configuration file:
  ~/.bashrc or ~/.zshrc
  ```plaintext
  export ANTHROPIC_API_KEY=sk-ant-api03-xxxxx
  ```
  Docker Sandboxes use a daemon process that runs independently of your
  current shell session. This means setting the environment variable inline or
  in your current session will not work. You must set it globally in your
  shell configuration file to ensure the daemon can access it.
  Apply the changes:
  1. Source your shell configuration.
  2. Restart Docker Desktop so the daemon picks up the new environment variable.
  Alternatively, you can skip this step and authenticate interactively when
  Claude Code starts. If no credentials are found, you'll be prompted to log
  in. Note that interactive authentication requires you to authenticate for
  each workspace separately.
2. Create and run a sandbox for Claude Code for your workspace:
  ```console
  $ docker sandbox run claude ~/my-project
  ```
  This creates a microVM sandbox. Docker assigns it a name automatically.
3. Claude Code starts and you can begin working. The first run takes longer
  while Docker initializes the microVM and pulls the template image.

## What just happened?

When you ran `docker sandbox run`:

- Docker created a lightweight microVM with a private Docker daemon
- The sandbox was assigned a name based on the workspace path
- Your workspace synced into the VM
- Docker started the Claude Code agent as a container inside the sandbox VM

The sandbox persists until you remove it. Installed packages and configuration
remain available. Run `docker sandbox run <sandbox-name>` again to reconnect.

> Note
>
> Agents can modify files in your workspace. Review changes before executing
> code or performing actions that auto-run scripts. See
> [Security considerations](https://docs.docker.com/ai/sandboxes/workflows/#security-considerations) for details.

## Basic commands

Here are essential commands to manage your sandboxes:

### List sandboxes

```console
$ docker sandbox ls
```

Shows all your sandboxes with their IDs, names, status, and creation time.

> Note
>
> Sandboxes don't appear in `docker ps` because they're microVMs, not
> containers. Use `docker sandbox ls` to see them.

### Access a running sandbox

```console
$ docker sandbox exec -it <sandbox-name> bash
```

Executes a command inside the container in the sandbox. Use `-it` to open an
interactive shell for debugging or installing additional tools.

### Remove a sandbox

```console
$ docker sandbox rm <sandbox-name>
```

Deletes the sandbox VM and all installed packages inside it. You can remove
multiple sandboxes at once by specifying multiple names:

```console
$ docker sandbox rm <sandbox-1> <sandbox-2>
```

### Recreate a sandbox

To start fresh with a clean environment, remove and recreate the sandbox:

```console
$ docker sandbox rm <sandbox-name>
$ docker sandbox run claude ~/project
```

Configuration like custom templates and workspace paths are set when you create
the sandbox. To change these settings, remove and recreate.

For a complete list of commands and options, see the
[CLI reference](https://docs.docker.com/reference/cli/docker/sandbox/).

## Next steps

Now that you have Claude running in a sandbox, learn more about:

- [Claude Code configuration](https://docs.docker.com/ai/sandboxes/claude-code/)
- [Supported agents](https://docs.docker.com/ai/sandboxes/agents/)
- [Using sandboxes effectively](https://docs.docker.com/ai/sandboxes/workflows/)
- [Custom templates](https://docs.docker.com/ai/sandboxes/templates/)
- [Network policies](https://docs.docker.com/ai/sandboxes/network-policies/)
- [Troubleshooting](https://docs.docker.com/ai/sandboxes/troubleshooting/)
