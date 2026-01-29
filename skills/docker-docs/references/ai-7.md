# DMR REST API and more

# DMR REST API

> Reference documentation for the Docker Model Runner REST API endpoints, including OpenAI, Anthropic, and Ollama compatibility.

# DMR REST API

   Table of contents

---

Once Model Runner is enabled, new API endpoints are available. You can use
these endpoints to interact with a model programmatically. Docker Model Runner
provides compatibility with OpenAI, Anthropic, and Ollama API formats.

## Determine the base URL

The base URL to interact with the endpoints depends on how you run Docker and
which API format you're using.

| Access from | Base URL |
| --- | --- |
| Containers | http://model-runner.docker.internal |
| Host processes (TCP) | http://localhost:12434 |

> Note
>
> TCP host access must be enabled. See [Enable Docker Model Runner](https://docs.docker.com/ai/model-runner/get-started/#enable-docker-model-runner-in-docker-desktop).

| Access from | Base URL |
| --- | --- |
| Containers | http://172.17.0.1:12434 |
| Host processes | http://localhost:12434 |

> Note
>
> The `172.17.0.1` interface may not be available by default to containers
> within a Compose project.
> In this case, add an `extra_hosts` directive to your Compose service YAML:
>
>
>
> ```yaml
> extra_hosts:
>   - "model-runner.docker.internal:host-gateway"
> ```
>
>
>
> Then you can access the Docker Model Runner APIs at `http://model-runner.docker.internal:12434/`

### Base URLs for third-party tools

When configuring third-party tools that expect OpenAI-compatible APIs, use these base URLs:

| Tool type | Base URL format |
| --- | --- |
| OpenAI SDK / clients | http://localhost:12434/engines/v1 |
| Anthropic SDK / clients | http://localhost:12434 |
| Ollama-compatible clients | http://localhost:12434 |

See [IDE and tool integrations](https://docs.docker.com/ai/model-runner/ide-integrations/) for specific configuration examples.

## Supported APIs

Docker Model Runner supports multiple API formats:

| API | Description | Use case |
| --- | --- | --- |
| OpenAI API | OpenAI-compatible chat completions, embeddings | Most AI frameworks and tools |
| Anthropic API | Anthropic-compatible messages endpoint | Tools built for Claude |
| Ollama API | Ollama-compatible endpoints | Tools built for Ollama |
| Image Generation API | Diffusers-based image generation | Generating images from text prompts |
| DMR API | Native Docker Model Runner endpoints | Model management |

## OpenAI-compatible API

DMR implements the OpenAI API specification for maximum compatibility with existing tools and frameworks.

### Endpoints

| Endpoint | Method | Description |
| --- | --- | --- |
| /engines/v1/models | GET | List models |
| /engines/v1/models/{namespace}/{name} | GET | Retrieve model |
| /engines/v1/chat/completions | POST | Create chat completion |
| /engines/v1/completions | POST | Create completion |
| /engines/v1/embeddings | POST | Create embeddings |

> Note
>
> You can optionally include the engine name in the path: `/engines/llama.cpp/v1/chat/completions`.
> This is useful when running multiple inference engines.

### Model name format

When specifying a model in API requests, use the full model identifier including the namespace:

```json
{
  "model": "ai/smollm2",
  "messages": [...]
}
```

Common model name formats:

- Docker Hub models: `ai/smollm2`, `ai/llama3.2`, `ai/qwen2.5-coder`
- Tagged versions: `ai/smollm2:360M-Q4_K_M`
- Custom models: `myorg/mymodel`

### Supported parameters

The following OpenAI API parameters are supported:

| Parameter | Type | Description |
| --- | --- | --- |
| model | string | Required. The model identifier. |
| messages | array | Required for chat completions. The conversation history. |
| prompt | string | Required for completions. The prompt text. |
| max_tokens | integer | Maximum tokens to generate. |
| temperature | float | Sampling temperature (0.0-2.0). |
| top_p | float | Nucleus sampling parameter (0.0-1.0). |
| stream | Boolean | Enable streaming responses. |
| stop | string/array | Stop sequences. |
| presence_penalty | float | Presence penalty (-2.0 to 2.0). |
| frequency_penalty | float | Frequency penalty (-2.0 to 2.0). |

### Limitations and differences from OpenAI

Be aware of these differences when using DMR's OpenAI-compatible API:

| Feature | DMR behavior |
| --- | --- |
| API key | Not required. DMR ignores theAuthorizationheader. |
| Function calling | Supported with llama.cpp for compatible models. |
| Vision | Supported for multi-modal models (e.g., LLaVA). |
| JSON mode | Supported viaresponse_format: {"type": "json_object"}. |
| Logprobs | Supported. |
| Token counting | Uses the model's native token encoder, which may differ from OpenAI's. |

## Anthropic-compatible API

DMR provides [Anthropic Messages API](https://platform.claude.com/docs/en/api/messages) compatibility for tools and frameworks built for Claude.

### Endpoints

| Endpoint | Method | Description |
| --- | --- | --- |
| /anthropic/v1/messages | POST | Create a message |
| /anthropic/v1/messages/count_tokens | POST | Count tokens |

### Supported parameters

The following Anthropic API parameters are supported:

| Parameter | Type | Description |
| --- | --- | --- |
| model | string | Required. The model identifier. |
| messages | array | Required. The conversation messages. |
| max_tokens | integer | Maximum tokens to generate. |
| temperature | float | Sampling temperature (0.0-1.0). |
| top_p | float | Nucleus sampling parameter. |
| top_k | integer | Top-k sampling parameter. |
| stream | Boolean | Enable streaming responses. |
| stop_sequences | array | Custom stop sequences. |
| system | string | System prompt. |

### Example: Chat with Anthropic API

```bash
curl http://localhost:12434/v1/messages \
  -H "Content-Type: application/json" \
  -d '{
    "model": "ai/smollm2",
    "max_tokens": 1024,
    "messages": [
      {"role": "user", "content": "Hello!"}
    ]
  }'
```

### Example: Streaming response

```bash
curl http://localhost:12434/v1/messages \
  -H "Content-Type: application/json" \
  -d '{
    "model": "ai/smollm2",
    "max_tokens": 1024,
    "stream": true,
    "messages": [
      {"role": "user", "content": "Count from 1 to 10"}
    ]
  }'
```

## Ollama-compatible API

DMR also provides Ollama-compatible endpoints for tools and frameworks built for Ollama.

### Endpoints

| Endpoint | Method | Description |
| --- | --- | --- |
| /api/tags | GET | List available models |
| /api/show | POST | Show model information |
| /api/chat | POST | Generate chat completion |
| /api/generate | POST | Generate completion |
| /api/embeddings | POST | Generate embeddings |

### Example: Chat with Ollama API

```bash
curl http://localhost:12434/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "ai/smollm2",
    "messages": [
      {"role": "user", "content": "Hello!"}
    ]
  }'
```

### Example: List models

```bash
curl http://localhost:12434/api/tags
```

## Image generation API (Diffusers)

DMR supports image generation through the Diffusers backend, enabling you to generate
images from text prompts using models like Stable Diffusion.

> Note
>
> The Diffusers backend requires an NVIDIA GPU with CUDA support and is only
> available on Linux (x86_64 and ARM64). See [Inference engines](https://docs.docker.com/ai/model-runner/inference-engines/#diffusers)
> for setup instructions.

### Endpoint

| Endpoint | Method | Description |
| --- | --- | --- |
| /engines/diffusers/v1/images/generations | POST | Generate an image from a text prompt |

### Supported parameters

| Parameter | Type | Description |
| --- | --- | --- |
| model | string | Required. The model identifier (e.g.,stable-diffusion:Q4). |
| prompt | string | Required. The text description of the image to generate. |
| size | string | Image dimensions inWIDTHxHEIGHTformat (e.g.,512x512). |

### Response format

The API returns a JSON response with the generated image encoded in base64:

```json
{
  "data": [
    {
      "b64_json": "<base64-encoded-image-data>"
    }
  ]
}
```

### Example: Generate an image

```bash
curl -s -X POST http://localhost:12434/engines/diffusers/v1/images/generations \
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
3. Extracts the base64-encoded image from the response using `jq`
4. Decodes the base64 data and saves it as `image.png`

## DMR native endpoints

These endpoints are specific to Docker Model Runner for model management:

| Endpoint | Method | Description |
| --- | --- | --- |
| /models/create | POST | Pull/create a model |
| /models | GET | List local models |
| /models/{namespace}/{name} | GET | Get model details |
| /models/{namespace}/{name} | DELETE | Delete a local model |

## REST API examples

### Request from within a container

To call the `chat/completions` OpenAI endpoint from within another container using `curl`:

```bash
#!/bin/sh

curl http://model-runner.docker.internal/engines/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "ai/smollm2",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "Please write 500 words about the fall of Rome."
            }
        ]
    }'
```

### Request from the host using TCP

To call the `chat/completions` OpenAI endpoint from the host via TCP:

1. Enable the host-side TCP support from the Docker Desktop GUI, or via the
  [Docker Desktop CLI](https://docs.docker.com/desktop/features/desktop-cli/).
  For example: `docker desktop enable model-runner --tcp <port>`.
  If you are running on Windows, also enable GPU-backed inference.
  See [Enable Docker Model Runner](https://docs.docker.com/ai/model-runner/get-started/#enable-docker-model-runner-in-docker-desktop).
2. Interact with it as documented in the previous section using `localhost` and the correct port.

```bash
#!/bin/sh

curl http://localhost:12434/engines/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
      "model": "ai/smollm2",
      "messages": [
          {
              "role": "system",
              "content": "You are a helpful assistant."
          },
          {
              "role": "user",
              "content": "Please write 500 words about the fall of Rome."
          }
      ]
  }'
```

### Request from the host using a Unix socket

To call the `chat/completions` OpenAI endpoint through the Docker socket from the host using `curl`:

```bash
#!/bin/sh

curl --unix-socket $HOME/.docker/run/docker.sock \
    localhost/exp/vDD4.40/engines/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "ai/smollm2",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "Please write 500 words about the fall of Rome."
            }
        ]
    }'
```

### Streaming responses

To receive streaming responses, set `stream: true`:

```bash
curl http://localhost:12434/engines/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
      "model": "ai/smollm2",
      "stream": true,
      "messages": [
          {"role": "user", "content": "Count from 1 to 10"}
      ]
  }'
```

## Using with OpenAI SDKs

### Python

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:12434/engines/v1",
    api_key="not-needed"  # DMR doesn't require an API key
)

response = client.chat.completions.create(
    model="ai/smollm2",
    messages=[
        {"role": "user", "content": "Hello!"}
    ]
)

print(response.choices[0].message.content)
```

### Node.js

```javascript
import OpenAI from 'openai';

const client = new OpenAI({
  baseURL: 'http://localhost:12434/engines/v1',
  apiKey: 'not-needed',
});

const response = await client.chat.completions.create({
  model: 'ai/smollm2',
  messages: [{ role: 'user', content: 'Hello!' }],
});

console.log(response.choices[0].message.content);
```

## What's next

- [IDE and tool integrations](https://docs.docker.com/ai/model-runner/ide-integrations/) - Configure Cline, Continue, Cursor, and other tools
- [Configuration options](https://docs.docker.com/ai/model-runner/configuration/) - Adjust context size and runtime parameters
- [Inference engines](https://docs.docker.com/ai/model-runner/inference-engines/) - Learn about llama.cpp, vLLM, and Diffusers options

---

# Configuration options

> Configure context size, runtime parameters, and model behavior in Docker Model Runner.

# Configuration options

   Table of contents

---

Docker Model Runner provides several configuration options to tune model behavior,
memory usage, and inference performance. This guide covers the key settings and
how to apply them.

## Context size (context length)

The context size determines the maximum number of tokens a model can process in
a single request, including both the input prompt and generated output. This is
one of the most important settings affecting memory usage and model capabilities.

### Default context size

By default, Docker Model Runner uses a context size that balances capability with
resource efficiency:

| Engine | Default behavior |
| --- | --- |
| llama.cpp | 4096 tokens |
| vLLM | Uses the model's maximum trained context size |

> Note
>
> The actual default varies by model. Most models support between 2,048 and 8,192
> tokens by default. Some newer models support 32K, 128K, or even larger contexts.

### Configure context size

You can adjust context size per model using the `docker model configure` command:

```console
$ docker model configure --context-size 8192 ai/qwen2.5-coder
```

Or in a Compose file:

```yaml
models:
  llm:
    model: ai/qwen2.5-coder
    context_size: 8192
```

### Context size guidelines

| Context size | Typical use case | Memory impact |
| --- | --- | --- |
| 2,048 | Simple queries, short code snippets | Low |
| 4,096 | Standard conversations, medium code files | Moderate |
| 8,192 | Long conversations, larger code files | Higher |
| 16,384+ | Extended documents, multi-file context | High |

> Important
>
> Larger context sizes require more memory (RAM/VRAM). If you experience out-of-memory
> errors, reduce the context size. As a rough guide, each additional 1,000 tokens
> requires approximately 100-500 MB of additional memory, depending on the model size.

### Check a model's maximum context

To see a model's configuration including context size:

```console
$ docker model inspect ai/qwen2.5-coder
```

> Note
>
> The `docker model inspect` command shows the model's maximum supported context length
> (e.g., `gemma3.context_length`), not the configured context size. The configured context
> size is what you set with `docker model configure --context-size` and represents the
> actual limit used during inference, which should be less than or equal to the model's
> maximum supported context length.

## Runtime flags

Runtime flags let you pass parameters directly to the underlying inference engine.
This provides fine-grained control over model behavior.

### Using runtime flags

Runtime flags can be provided through multiple mechanisms:

#### Using Docker Compose

In a Compose file:

```yaml
models:
  llm:
    model: ai/qwen2.5-coder
    context_size: 4096
    runtime_flags:
      - "--temp"
      - "0.7"
      - "--top-p"
      - "0.9"
```

#### Using Command Line

With the `docker model configure` command:

```console
$ docker model configure --runtime-flag "--temp" --runtime-flag "0.7" --runtime-flag "--top-p" --runtime-flag "0.9" ai/qwen2.5-coder
```

### Common llama.cpp parameters

These are the most commonly used llama.cpp parameters. You don't need to look up
the llama.cpp documentation for typical use cases.

#### Sampling parameters

| Flag | Description | Default | Range |
| --- | --- | --- | --- |
| --temp | Temperature for sampling. Lower = more deterministic, higher = more creative | 0.8 | 0.0-2.0 |
| --top-k | Limit sampling to top K tokens. Lower = more focused | 40 | 1-100 |
| --top-p | Nucleus sampling threshold. Lower = more focused | 0.9 | 0.0-1.0 |
| --min-p | Minimum probability threshold | 0.05 | 0.0-1.0 |
| --repeat-penalty | Penalty for repeating tokens | 1.1 | 1.0-2.0 |

**Example: Deterministic output (for code generation)**

```yaml
runtime_flags:
  - "--temp"
  - "0"
  - "--top-k"
  - "1"
```

**Example: Creative output (for storytelling)**

```yaml
runtime_flags:
  - "--temp"
  - "1.2"
  - "--top-p"
  - "0.95"
```

#### Performance parameters

| Flag | Description | Default | Notes |
| --- | --- | --- | --- |
| --threads | CPU threads for generation | Auto | Set to number of performance cores |
| --threads-batch | CPU threads for batch processing | Auto | Usually same as--threads |
| --batch-size | Batch size for prompt processing | 512 | Higher = faster prompt processing |
| --mlock | Lock model in memory | Off | Prevents swapping, requires sufficient RAM |
| --no-mmap | Disable memory mapping | Off | May improve performance on some systems |

**Example: Optimized for multi-core CPU**

```yaml
runtime_flags:
  - "--threads"
  - "8"
  - "--batch-size"
  - "1024"
```

#### GPU parameters

| Flag | Description | Default | Notes |
| --- | --- | --- | --- |
| --n-gpu-layers | Layers to offload to GPU | All (if GPU available) | Reduce if running out of VRAM |
| --main-gpu | GPU to use for computation | 0 | For multi-GPU systems |
| --split-mode | How to split across GPUs | layer | Options:none,layer,row |

**Example: Partial GPU offload (limited VRAM)**

```yaml
runtime_flags:
  - "--n-gpu-layers"
  - "20"
```

#### Advanced parameters

| Flag | Description | Default |
| --- | --- | --- |
| --rope-scaling | RoPE scaling method | Auto |
| --rope-freq-base | RoPE base frequency | Model default |
| --rope-freq-scale | RoPE frequency scale | Model default |
| --no-prefill-assistant | Disable assistant pre-fill | Off |
| --reasoning-budget | Token budget for reasoning models | 0 (disabled) |

### vLLM parameters

When using the vLLM backend, different parameters are available.

Use `--hf_overrides` to pass HuggingFace model config overrides as JSON:

```console
$ docker model configure --hf_overrides '{"rope_scaling": {"type": "dynamic", "factor": 2.0}}' ai/model-vllm
```

## Configuration presets

Here are complete configuration examples for common use cases.

### Code completion (fast, deterministic)

```yaml
models:
  coder:
    model: ai/qwen2.5-coder
    context_size: 4096
    runtime_flags:
      - "--temp"
      - "0.1"
      - "--top-k"
      - "1"
      - "--batch-size"
      - "1024"
```

### Chat assistant (balanced)

```yaml
models:
  assistant:
    model: ai/llama3.2
    context_size: 8192
    runtime_flags:
      - "--temp"
      - "0.7"
      - "--top-p"
      - "0.9"
      - "--repeat-penalty"
      - "1.1"
```

### Creative writing (high temperature)

```yaml
models:
  writer:
    model: ai/llama3.2
    context_size: 8192
    runtime_flags:
      - "--temp"
      - "1.2"
      - "--top-p"
      - "0.95"
      - "--repeat-penalty"
      - "1.0"
```

### Long document analysis (large context)

```yaml
models:
  analyzer:
    model: ai/qwen2.5-coder:14B
    context_size: 32768
    runtime_flags:
      - "--mlock"
      - "--batch-size"
      - "2048"
```

### Low memory system

```yaml
models:
  efficient:
    model: ai/smollm2:360M-Q4_K_M
    context_size: 2048
    runtime_flags:
      - "--threads"
      - "4"
```

## Environment-based configuration

You can also configure models via environment variables in containers:

| Variable | Description |
| --- | --- |
| LLM_URL | Auto-injected URL of the model endpoint |
| LLM_MODEL | Auto-injected model identifier |

See
[Models and Compose](https://docs.docker.com/ai/compose/models-and-compose/) for details on how these are populated.

## Reset configuration

Configuration set via `docker model configure` persists until the model is removed.
To reset configuration:

```console
$ docker model configure --context-size -1 ai/qwen2.5-coder
```

Using `-1` resets to the default value.

## What's next

- [Inference engines](https://docs.docker.com/ai/model-runner/inference-engines/) - Learn about llama.cpp and vLLM
- [API reference](https://docs.docker.com/ai/model-runner/api-reference/) - API parameters for per-request configuration
- [Models and Compose](https://docs.docker.com/ai/compose/models-and-compose/) - Configure models in Compose applications

---

# DMR examples

> Example projects and CI/CD workflows for Docker Model Runner.

# DMR examples

   Table of contents

---

See some examples of complete workflows using Docker Model Runner.

## Sample project

You can now start building your generative AI application powered by Docker
Model Runner.

If you want to try an existing GenAI application, follow these steps:

1. Set up the sample app. Clone and run the following repository:
  ```console
  $ git clone https://github.com/docker/hello-genai.git
  ```
2. In your terminal, go to the `hello-genai` directory.
3. Run `run.sh` to pull the chosen model and run the app.
4. Open your app in the browser at the addresses specified in the repository
  [README](https://github.com/docker/hello-genai).

You see the GenAI app's interface where you can start typing your prompts.

You can now interact with your own GenAI app, powered by a local model. Try a
few prompts and notice how fast the responses are — all running on your machine
with Docker.

## Use Model Runner in GitHub Actions

Here is an example of how to use Model Runner as part of a GitHub workflow.
The example installs Model Runner, tests the installation, pulls and runs a
model, interacts with the model via the API, and deletes the model.

dmr-run.yml

```yaml
name: Docker Model Runner Example Workflow

permissions:
  contents: read

on:
  workflow_dispatch:
    inputs:
      test_model:
        description: 'Model to test with (default: ai/smollm2:360M-Q4_K_M)'
        required: false
        type: string
        default: 'ai/smollm2:360M-Q4_K_M'

jobs:
  dmr-test:
    runs-on: ubuntu-latest
    timeout-minutes: 30

    steps:
      - name: Set up Docker
        uses: docker/setup-docker-action@v4

      - name: Install docker-model-plugin
        run: |
          echo "Installing docker-model-plugin..."
          # Add Docker's official GPG key:
          sudo apt-get update
          sudo apt-get install ca-certificates curl
          sudo install -m 0755 -d /etc/apt/keyrings
          sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
          sudo chmod a+r /etc/apt/keyrings/docker.asc

          # Add the repository to Apt sources:
          echo \
          "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
          $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
          sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
          sudo apt-get update
          sudo apt-get install -y docker-model-plugin

          echo "Installation completed successfully"

      - name: Test docker model version
        run: |
          echo "Testing docker model version command..."
          sudo docker model version

          # Verify the command returns successfully
          if [ $? -eq 0 ]; then
            echo "✅ docker model version command works correctly"
          else
            echo "❌ docker model version command failed"
            exit 1
          fi

      - name: Pull the provided model and run it
        run: |
          MODEL="${{ github.event.inputs.test_model || 'ai/smollm2:360M-Q4_K_M' }}"
          echo "Testing with model: $MODEL"

          # Test model pull
          echo "Pulling model..."
          sudo docker model pull "$MODEL"

          if [ $? -eq 0 ]; then
            echo "✅ Model pull successful"
          else
            echo "❌ Model pull failed"
            exit 1
          fi

          # Test basic model run (with timeout to avoid hanging)
          echo "Testing docker model run..."
          timeout 60s sudo docker model run "$MODEL" "Give me a fact about whales." || {
            exit_code=$?
            if [ $exit_code -eq 124 ]; then
              echo "✅ Model run test completed (timed out as expected for non-interactive test)"
            else
              echo "❌ Model run failed with exit code: $exit_code"
              exit 1
            fi
          }
               - name: Test model pull and run
        run: |
          MODEL="${{ github.event.inputs.test_model || 'ai/smollm2:360M-Q4_K_M' }}"
          echo "Testing with model: $MODEL"

          # Test model pull
          echo "Pulling model..."
          sudo docker model pull "$MODEL"

          if [ $? -eq 0 ]; then
            echo "✅ Model pull successful"
          else
            echo "❌ Model pull failed"
            exit 1
          fi

          # Test basic model run (with timeout to avoid hanging)
          echo "Testing docker model run..."
          timeout 60s sudo docker model run "$MODEL" "Give me a fact about whales." || {
            exit_code=$?
            if [ $exit_code -eq 124 ]; then
              echo "✅ Model run test completed (timed out as expected for non-interactive test)"
            else
              echo "❌ Model run failed with exit code: $exit_code"
              exit 1
            fi
          }

      - name: Test API endpoint
        run: |
          MODEL="${{ github.event.inputs.test_model || 'ai/smollm2:360M-Q4_K_M' }}"
          echo "Testing API endpoint with model: $MODEL"

          # Test API call with curl
          echo "Testing API call..."
          RESPONSE=$(curl -s http://localhost:12434/engines/llama.cpp/v1/chat/completions \
            -H "Content-Type: application/json" \
            -d "{
                \"model\": \"$MODEL\",
                \"messages\": [
                    {
                        \"role\": \"user\",
                        \"content\": \"Say hello\"
                    }
                ],
                \"top_k\": 1,
                \"temperature\": 0
            }")

          if [ $? -eq 0 ]; then
            echo "✅ API call successful"
            echo "Response received: $RESPONSE"

            # Check if response contains "hello" (case-insensitive)
            if echo "$RESPONSE" | grep -qi "hello"; then
              echo "✅ Response contains 'hello' (case-insensitive)"
            else
              echo "❌ Response does not contain 'hello'"
              echo "Full response: $RESPONSE"
              exit 1
            fi
          else
            echo "❌ API call failed"
            exit 1
          fi

      - name: Test model cleanup
        run: |
          MODEL="${{ github.event.inputs.test_model || 'ai/smollm2:360M-Q4_K_M' }}"

          echo "Cleaning up test model..."
          sudo docker model rm "$MODEL" || echo "Model removal failed or model not found"

          # Verify model was removed
          echo "Verifying model cleanup..."
          sudo docker model ls

          echo "✅ Model cleanup completed"

      - name: Report success
        if: success()
        run: |
          echo "🎉 Docker Model Runner daily health check completed successfully!"
          echo "All tests passed:"
          echo "  ✅ docker-model-plugin installation successful"
          echo "  ✅ docker model version command working"
          echo "  ✅ Model pull and run operations successful"
          echo "  ✅ API endpoint operations successful"
          echo "  ✅ Cleanup operations successful"
```

## Related pages

- [Models and Compose](https://docs.docker.com/ai/compose/models-and-compose/)

---

# Get started with DMR

> How to install, enable, and use Docker Model Runner to manage and run AI models.

# Get started with DMR

   Table of contents

---

Docker Model Runner (DMR) lets you run and manage AI models locally using Docker. This page shows you how to enable DMR, pull and run a model, configure model settings, and publish custom models.

## Enable Docker Model Runner

You can enable DMR using Docker Desktop or Docker Engine. Follow the instructions below based on your setup.

### Docker Desktop

1. In the settings view, go to the **AI** tab.
2. Select the **Enable Docker Model Runner** setting.
3. If you use Windows with a supported NVIDIA GPU, you also see and can select
  **Enable GPU-backed inference**.
4. Optional: To enable TCP support, select **Enable host-side TCP support**.
  1. In the **Port** field, type the port you want to use.
  2. If you interact with Model Runner from a local frontend web app, in
    **CORS Allows Origins**, select the origins that Model Runner should
    accept requests from. An origin is the URL where your web app runs, for
    example `http://localhost:3131`.

You can now use the `docker model` command in the CLI and view and interact
with your local models in the **Models** tab in the Docker Desktop Dashboard.

> Important
>
> For Docker Desktop versions 4.45 and earlier, this setting was under the
> **Beta features** tab.

### Docker Engine

1. Ensure you have installed
  [Docker Engine](https://docs.docker.com/engine/install/).
2. Docker Model Runner is available as a package. To install it, run:
  ```bash
  $ sudo apt-get update
  $ sudo apt-get install docker-model-plugin
  ```
  ```bash
  $ sudo dnf update
  $ sudo dnf install docker-model-plugin
  ```
3. Test the installation:
  ```bash
  $ docker model version
  $ docker model run ai/smollm2
  ```

> Note
>
> TCP support is enabled by default for Docker Engine on port `12434`.

### Update DMR in Docker Engine

To update Docker Model Runner in Docker Engine, uninstall it with
[docker model uninstall-runner](https://docs.docker.com/reference/cli/docker/model/uninstall-runner/)
then reinstall it:

```bash
docker model uninstall-runner --images && docker model install-runner
```

> Note
>
> With the above command, local models are preserved.
> To delete the models during the upgrade, add the `--models` option to the
> `uninstall-runner` command.

## Pull a model

Models are cached locally.

> Note
>
> When you use the Docker CLI, you can also pull models directly from
> [HuggingFace](https://huggingface.co/).

1. Select **Models** and select the **Docker Hub** tab.
2. Find the model you want and select **Pull**.

![Screenshot showing the Docker Hub view.](https://docs.docker.com/ai/model-runner/images/dmr-catalog.png)  ![Screenshot showing the Docker Hub view.](https://docs.docker.com/ai/model-runner/images/dmr-catalog.png)

Use the
[docker model pullcommand](https://docs.docker.com/reference/cli/docker/model/pull/).
For example:

Pulling from Docker Hub

```bash
docker model pull ai/smollm2:360M-Q4_K_M
```

Pulling from HuggingFace

```bash
docker model pull hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF
```

## Run a model

1. Select **Models** and select the **Local** tab.
2. Select the play button. The interactive chat screen opens.

![Screenshot showing the Local view.](https://docs.docker.com/ai/model-runner/images/dmr-run.png)  ![Screenshot showing the Local view.](https://docs.docker.com/ai/model-runner/images/dmr-run.png)

Use the
[docker model runcommand](https://docs.docker.com/reference/cli/docker/model/run/).

## Configure a model

You can configure a model, such as its maximum token limit and more,
use Docker Compose.
See [Models and Compose - Model configuration options](https://docs.docker.com/ai/compose/models-and-compose/#model-configuration-options).

## Publish a model

> Note
>
> This works for any Container Registry supporting OCI Artifacts, not only
> Docker Hub.

You can tag existing models with a new name and publish them under a different
namespace and repository:

```bash
# Tag a pulled model under a new name
$ docker model tag ai/smollm2 myorg/smollm2

# Push it to Docker Hub
$ docker model push myorg/smollm2
```

For more details, see the
[docker model tag](https://docs.docker.com/reference/cli/docker/model/tag)
and
[docker model push](https://docs.docker.com/reference/cli/docker/model/push) command
documentation.

You can also package a model file in GGUF format as an OCI Artifact and publish
it to Docker Hub.

```bash
# Download a model file in GGUF format, for example from HuggingFace
$ curl -L -o model.gguf https://huggingface.co/TheBloke/Mistral-7B-v0.1-GGUF/resolve/main/mistral-7b-v0.1.Q4_K_M.gguf

# Package it as OCI Artifact and push it to Docker Hub
$ docker model package --gguf "$(pwd)/model.gguf" --push myorg/mistral-7b-v0.1:Q4_K_M
```

For more details, see the
[docker model package](https://docs.docker.com/reference/cli/docker/model/package/) command
documentation.

## Troubleshooting

### Display the logs

To troubleshoot issues, display the logs:

Select **Models** and select the **Logs** tab.

![Screenshot showing the Models view.](https://docs.docker.com/ai/model-runner/images/dmr-logs.png)  ![Screenshot showing the Models view.](https://docs.docker.com/ai/model-runner/images/dmr-logs.png)

Use the
[docker model logscommand](https://docs.docker.com/reference/cli/docker/model/logs/).

### Inspect requests and responses

Inspecting requests and responses helps you diagnose model-related issues.
For example, you can evaluate context usage to verify you stay within the model's context
window or display the full body of a request to control the parameters you are passing to your models
when developing with a framework.

In Docker Desktop, to inspect the requests and responses for each model:

1. Select **Models** and select the **Requests** tab. This view displays all the requests to all models:
  - The time the request was sent.
  - The model name and version
  - The prompt/request
  - The context usage
  - The time it took for the response to be generated.
2. Select one of the requests to display further details:
  - In the **Overview** tab, view the token usage, response metadata and generation speed, and the actual prompt and response.
  - In the **Request** and **Response** tabs, view the full JSON payload of the request and the response.

> Note
>
> You can also display the requests for a specific model when you select a model and then select the **Requests** tab.

## Related pages

- [API reference](https://docs.docker.com/ai/model-runner/api-reference/) - OpenAI and Ollama-compatible API documentation
- [Configuration options](https://docs.docker.com/ai/model-runner/configuration/) - Context size and runtime parameters
- [Inference engines](https://docs.docker.com/ai/model-runner/inference-engines/) - llama.cpp and vLLM details
- [IDE integrations](https://docs.docker.com/ai/model-runner/ide-integrations/) - Connect Cline, Continue, Cursor, and more
- [Open WebUI integration](https://docs.docker.com/ai/model-runner/openwebui-integration/) - Set up a web chat interface
- [Models and Compose](https://docs.docker.com/ai/compose/models-and-compose/) - Use models in Compose applications
- [Docker Model Runner CLI reference](https://docs.docker.com/reference/cli/docker/model) - Complete CLI documentation

---

# IDE and tool integrations

> Configure popular AI coding assistants and tools to use Docker Model Runner as their backend.

# IDE and tool integrations

   Table of contents

---

Docker Model Runner can serve as a local backend for popular AI coding assistants
and development tools. This guide shows how to configure common tools to use
models running in DMR.

## Prerequisites

Before configuring any tool:

1. [Enable Docker Model Runner](https://docs.docker.com/ai/model-runner/get-started/#enable-docker-model-runner) in Docker Desktop or Docker Engine.
2. Enable TCP host access:
  - Docker Desktop: Enable **host-side TCP support** in Settings > AI, or run:
    ```console
    $ docker desktop enable model-runner --tcp 12434
    ```
  - Docker Engine: TCP is enabled by default on port 12434.
3. Pull a model:
  ```console
  $ docker model pull ai/qwen2.5-coder
  ```

## Cline (VS Code)

[Cline](https://github.com/cline/cline) is an AI coding assistant for VS Code.

### Configuration

1. Open VS Code and go to the Cline extension settings.
2. Select **OpenAI Compatible** as the API provider.
3. Configure the following settings:

| Setting | Value |
| --- | --- |
| Base URL | http://localhost:12434/engines/v1 |
| API Key | not-needed(or any placeholder value) |
| Model ID | ai/qwen2.5-coder(or your preferred model) |

> Important
>
> The base URL must include `/engines/v1` at the end. Do not include a trailing slash.

### Troubleshooting Cline

If Cline fails to connect:

1. Verify DMR is running:
  ```console
  $ docker model status
  ```
2. Test the endpoint directly:
  ```console
  $ curl http://localhost:12434/engines/v1/models
  ```
3. Check that CORS is configured if running a web-based version:
  - In Docker Desktop Settings > AI, add your origin to **CORS Allowed Origins**

## Continue (VS Code / JetBrains)

[Continue](https://continue.dev) is an open-source AI code assistant that works with VS Code and JetBrains IDEs.

### Configuration

Edit your Continue configuration file (`~/.continue/config.json`):

```json
{
  "models": [
    {
      "title": "Docker Model Runner",
      "provider": "openai",
      "model": "ai/qwen2.5-coder",
      "apiBase": "http://localhost:12434/engines/v1",
      "apiKey": "not-needed"
    }
  ]
}
```

### Using Ollama provider

Continue also supports the Ollama provider, which works with DMR:

```json
{
  "models": [
    {
      "title": "Docker Model Runner (Ollama)",
      "provider": "ollama",
      "model": "ai/qwen2.5-coder",
      "apiBase": "http://localhost:12434"
    }
  ]
}
```

## Cursor

[Cursor](https://cursor.sh) is an AI-powered code editor.

### Configuration

1. Open Cursor Settings (Cmd/Ctrl + ,).
2. Navigate to **Models** > **OpenAI API Key**.
3. Configure:
  | Setting | Value |
  | --- | --- |
  | OpenAI API Key | not-needed |
  | Override OpenAI Base URL | http://localhost:12434/engines/v1 |
4. In the model drop-down, enter your model name: `ai/qwen2.5-coder`

> Note
>
> Some Cursor features may require models with specific capabilities (e.g., function calling).
> Use capable models like `ai/qwen2.5-coder` or `ai/llama3.2` for best results.

## Zed

[Zed](https://zed.dev) is a high-performance code editor with AI features.

### Configuration

Edit your Zed settings (`~/.config/zed/settings.json`):

```json
{
  "language_models": {
    "openai": {
      "api_url": "http://localhost:12434/engines/v1",
      "available_models": [
        {
          "name": "ai/qwen2.5-coder",
          "display_name": "Qwen 2.5 Coder (DMR)",
          "max_tokens": 8192
        }
      ]
    }
  }
}
```

## Open WebUI

[Open WebUI](https://github.com/open-webui/open-webui) provides a ChatGPT-like interface for local models.

See [Open WebUI integration](https://docs.docker.com/ai/model-runner/openwebui-integration/) for detailed setup instructions.

## Aider

[Aider](https://aider.chat) is an AI pair programming tool for the terminal.

### Configuration

Set environment variables or use command-line flags:

```bash
export OPENAI_API_BASE=http://localhost:12434/engines/v1
export OPENAI_API_KEY=not-needed

aider --model openai/ai/qwen2.5-coder
```

Or in a single command:

```console
$ aider --openai-api-base http://localhost:12434/engines/v1 \
        --openai-api-key not-needed \
        --model openai/ai/qwen2.5-coder
```

## LangChain

### Python

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    base_url="http://localhost:12434/engines/v1",
    api_key="not-needed",
    model="ai/qwen2.5-coder"
)

response = llm.invoke("Write a hello world function in Python")
print(response.content)
```

### JavaScript/TypeScript

```typescript
import { ChatOpenAI } from "@langchain/openai";

const model = new ChatOpenAI({
  configuration: {
    baseURL: "http://localhost:12434/engines/v1",
  },
  apiKey: "not-needed",
  modelName: "ai/qwen2.5-coder",
});

const response = await model.invoke("Write a hello world function");
console.log(response.content);
```

## LlamaIndex

```python
from llama_index.llms.openai_like import OpenAILike

llm = OpenAILike(
    api_base="http://localhost:12434/engines/v1",
    api_key="not-needed",
    model="ai/qwen2.5-coder"
)

response = llm.complete("Write a hello world function")
print(response.text)
```

## Common issues

### "Connection refused" errors

1. Ensure Docker Model Runner is enabled and running:
  ```console
  $ docker model status
  ```
2. Verify TCP access is enabled:
  ```console
  $ curl http://localhost:12434/engines/v1/models
  ```
3. Check if another service is using port 12434.

### "Model not found" errors

1. Verify the model is pulled:
  ```console
  $ docker model list
  ```
2. Use the full model name including namespace (e.g., `ai/qwen2.5-coder`, not just `qwen2.5-coder`).

### Slow responses or timeouts

1. For first requests, models need to load into memory. Subsequent requests are faster.
2. Consider using a smaller model or adjusting the context size:
  ```console
  $ docker model configure --context-size 4096 ai/qwen2.5-coder
  ```
3. Check available system resources (RAM, GPU memory).

### CORS errors (web-based tools)

If using browser-based tools, add the origin to CORS allowed origins:

1. Docker Desktop: Settings > AI > CORS Allowed Origins
2. Add your tool's URL (e.g., `http://localhost:3000`)

## Recommended models by use case

| Use case | Recommended model | Notes |
| --- | --- | --- |
| Code completion | ai/qwen2.5-coder | Optimized for coding tasks |
| General assistant | ai/llama3.2 | Good balance of capabilities |
| Small/fast | ai/smollm2 | Low resource usage |
| Embeddings | ai/all-minilm | For RAG and semantic search |

## What's next

- [API reference](https://docs.docker.com/ai/model-runner/api-reference/) - Full API documentation
- [Configuration options](https://docs.docker.com/ai/model-runner/configuration/) - Tune model behavior
- [Open WebUI integration](https://docs.docker.com/ai/model-runner/openwebui-integration/) - Set up a web interface
