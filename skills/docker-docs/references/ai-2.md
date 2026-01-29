# Model providers and more

# Model providers

> Get API keys and configure cloud model providers for cagent

# Model providers

   Table of contents

---

To run cagent, you need a model provider. You can either use a cloud provider
with an API key or run models locally with [Docker Model
Runner](https://docs.docker.com/ai/cagent/local-models/).

This guide covers cloud providers. For the local alternative, see [Local
models with Docker Model Runner](https://docs.docker.com/ai/cagent/local-models/).

## Supported providers

cagent supports these cloud model providers:

- Anthropic - Claude models
- OpenAI - GPT models
- Google - Gemini models

## Anthropic

Anthropic provides the Claude family of models, including Claude Sonnet and
Claude Opus.

To get an API key:

1. Go to [console.anthropic.com](https://console.anthropic.com/).
2. Sign up or sign in to your account.
3. Navigate to the API Keys section.
4. Create a new API key.
5. Copy the key.

Set your API key as an environment variable:

```console
$ export ANTHROPIC_API_KEY=your_key_here
```

Use Anthropic models in your agent configuration:

```yaml
agents:
  root:
    model: anthropic/claude-sonnet-4-5
    instruction: You are a helpful coding assistant
```

Available models include:

- `anthropic/claude-sonnet-4-5`
- `anthropic/claude-opus-4-5`
- `anthropic/claude-haiku-4-5`

## OpenAI

OpenAI provides the GPT family of models, including GPT-5 and GPT-5 mini.

To get an API key:

1. Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys).
2. Sign up or sign in to your account.
3. Navigate to the API Keys section.
4. Create a new API key.
5. Copy the key.

Set your API key as an environment variable:

```console
$ export OPENAI_API_KEY=your_key_here
```

Use OpenAI models in your agent configuration:

```yaml
agents:
  root:
    model: openai/gpt-5
    instruction: You are a helpful coding assistant
```

Available models include:

- `openai/gpt-5`
- `openai/gpt-5-mini`

## Google Gemini

Google provides the Gemini family of models.

To get an API key:

1. Go to [aistudio.google.com/apikey](https://aistudio.google.com/apikey).
2. Sign in with your Google account.
3. Create an API key.
4. Copy the key.

Set your API key as an environment variable:

```console
$ export GOOGLE_API_KEY=your_key_here
```

Use Gemini models in your agent configuration:

```yaml
agents:
  root:
    model: google/gemini-2.5-flash
    instruction: You are a helpful coding assistant
```

Available models include:

- `google/gemini-2.5-flash`
- `google/gemini-2.5-pro`

## OpenAI-compatible providers

You can use the `openai` provider type to connect to any model or provider that
implements the OpenAI API specification. This includes services like Azure
OpenAI, local inference servers, and other compatible endpoints.

Configure an OpenAI-compatible provider by specifying the base URL:

```yaml
agents:
  root:
    model: openai/your-model-name
    instruction: You are a helpful coding assistant
    provider:
      base_url: https://your-provider.example.com/v1
```

By default, cagent uses the `OPENAI_API_KEY` environment variable for
authentication. If your provider uses a different variable, specify it with
`token_key`:

```yaml
agents:
  root:
    model: openai/your-model-name
    instruction: You are a helpful coding assistant
    provider:
      base_url: https://your-provider.example.com/v1
      token_key: YOUR_PROVIDER_API_KEY
```

## What's next

- Follow the [tutorial](https://docs.docker.com/ai/cagent/tutorial/) to build your first agent
- Learn about [local models with Docker Model Runner](https://docs.docker.com/ai/cagent/local-models/) as an
  alternative to cloud providers
- Review the [configuration reference](https://docs.docker.com/ai/cagent/reference/config/) for advanced model
  settings

---

# RAG

> How RAG gives your cagent agents access to codebases and documentation

# RAG

   Table of contents

---

When you configure a RAG source in cagent, your agent automatically gains a
search tool for that knowledge base. The agent decides when to search, retrieves
only relevant information, and uses it to answer questions or complete tasks -
all without you manually managing what goes in the prompt.

This guide explains how cagent's RAG system works, when to use it, and how to
configure it effectively for your content.

> Note
>
> RAG is an advanced feature that requires configuration and tuning. The defaults
> work well for getting started, but tailoring the configuration to your specific
> content and use case significantly improves results.

## The problem: too much context

Your agent can work with your entire codebase, but it can't fit everything in
its context window. Even with 200K token limits, medium-sized projects are too
large. Finding relevant code buried in hundreds of files wastes context.

Filesystem tools help agents read files, but the agent has to guess which files
to read. It can't search by meaning, only by filename. Ask "find the retry
logic" and the agent reads files hoping to stumble on the right code.

Grep finds exact text matches but misses related concepts. Searching
"authentication" won't find code using "auth" or "login." You either get
hundreds of matches or zero, and grep doesn't understand code structure - it
just matches strings anywhere they appear.

RAG indexes your content ahead of time and enables semantic search. The agent
searches pre-indexed content by meaning, not exact words. It retrieves only
relevant chunks that respect code structure. No wasted context on exploration.

## How RAG works in cagent

Configure a RAG source in your cagent config:

```yaml
rag:
  codebase:
    docs: [./src, ./pkg]
    strategies:
      - type: chunked-embeddings
        embedding_model: openai/text-embedding-3-small
        vector_dimensions: 1536
        database: ./code.db

agents:
  root:
    model: openai/gpt-5
    instruction: You are a coding assistant. Search the codebase when needed.
    rag: [codebase]
```

When you reference `rag: [codebase]`, cagent:

1. **At startup** - Indexes your documents (first run only, blocks until complete)
2. **During conversation** - Gives the agent a search tool
3. **When the agent searches** - Retrieves relevant chunks and adds them to context
4. **On file changes** - Automatically re-indexes modified files

The agent decides when to search based on the conversation. You don't manage
what goes in context - the agent does.

### The indexing process

On first run, cagent:

- Reads files from configured paths
- Respects `.gitignore` patterns (can be disabled)
- Splits documents into chunks
- Creates searchable representations using your chosen strategy
- Stores everything in a local database

Subsequent runs reuse the index. If files change, cagent detects this and
re-indexes only what changed, keeping your knowledge base up to date without
manual intervention.

## Retrieval strategies

Different content requires different retrieval approaches. cagent supports
three strategies, each optimized for different use cases. The defaults work
well, but understanding the trade-offs helps you choose the right approach.

### Semantic search (chunked-embeddings)

Converts text to vectors that represent meaning, enabling search by concept
rather than exact words:

```yaml
strategies:
  - type: chunked-embeddings
    embedding_model: openai/text-embedding-3-small
    vector_dimensions: 1536
    database: ./docs.db
    chunking:
      size: 1000
      overlap: 100
```

During indexing, documents are split into chunks and each chunk is converted
to a 1536-dimensional vector by the embedding model. These vectors are
essentially coordinates in a high-dimensional space where similar concepts are
positioned close together.

When you search for "how do I authenticate users?", your query becomes a vector
and the database finds chunks with nearby vectors using cosine similarity
(measuring the angle between vectors). The embedding model learned that
"authentication," "auth," and "login" are related concepts, so searching for
one finds the others.

Example: The query "how do I authenticate users?" finds both "User
authentication requires a valid API token" and "Token-based auth validates
requests" despite different wording. It won't find "The authentication tests
are failing" because that's a different meaning despite containing the word.

This works well for documentation where users ask questions using different
terminology than your docs. The downside is it may miss exact technical terms
and sometimes you want literal matches, not semantic ones. Requires embedding
API calls during indexing.

### Keyword search (BM25)

Statistical algorithm that matches and ranks by term frequency and rarity:

```yaml
strategies:
  - type: bm25
    database: ./bm25.db
    k1: 1.5
    b: 0.75
    chunking:
      size: 1000
      overlap: 100
```

During indexing, documents are tokenized and the algorithm calculates how often
each term appears (term frequency) and how rare it is across all documents
(inverse document frequency). The scoring index is stored in a local SQLite
database.

When you search for "HandleRequest function", the algorithm finds chunks
containing these exact terms and scores them based on term frequency, term
rarity, and document length. Finding "HandleRequest" is scored as more
significant than finding common words like "function". Think of it as grep with
statistical ranking.

Example: Searching "HandleRequest function" finds `func HandleRequest(w http.ResponseWriter, r *http.Request)` and "The HandleRequest function
processes incoming requests", but not "process HTTP requests" despite that
being semantically similar.

The `k1` parameter (default 1.5) controls how much repeated terms matter -
higher values emphasize repetition more. The `b` parameter (default 0.75)
controls length normalization - higher values penalize longer documents more.

This is fast, local (no API costs), and predictable for finding function names,
class names, API endpoints, and any identifier that appears verbatim. The
trade-off is zero understanding of meaning - "RetryHandler" and "retry logic"
won't match despite being related. Essential complement to semantic search.

### LLM-enhanced semantic search (semantic-embeddings)

Generates semantic summaries with an LLM before embedding, enabling search by
what code does rather than what it's called:

```yaml
strategies:
  - type: semantic-embeddings
    embedding_model: openai/text-embedding-3-small
    chat_model: openai/gpt-5-mini
    vector_dimensions: 1536
    database: ./code.db
    ast_context: true
    chunking:
      size: 1000
      code_aware: true
```

During indexing, code is split using AST structure (functions stay intact),
then the `chat_model` generates a semantic summary of each chunk. The summary
gets embedded, not the raw code. When you search, your query matches against
these summaries, but the original code is returned.

This solves a problem with regular embeddings: raw code embeddings are
dominated by variable names and implementation details. A function called
`processData` that implements retry logic won't semantically match "retry". But
when the LLM summarizes it first, the summary explicitly mentions "retry
logic," making it findable.

Example: Consider this code:

```go
func (c *Client) Do(req *Request) (*Response, error) {
    for i := 0; i < 3; i++ {
        resp, err := c.attempt(req)
        if err == nil { return resp, nil }
        time.Sleep(time.Duration(1<<i) * time.Second)
    }
    return nil, errors.New("max retries exceeded")
}
```

The LLM summary is: "Implements exponential backoff retry logic for HTTP
requests, attempting up to 3 times with delays of 1s, 2s, 4s before failing."

Searching "retry logic exponential backoff" now finds this code, despite the
code never using those words. The `ast_context: true` option includes AST
metadata in prompts for better understanding. The `code_aware: true` chunking
prevents splitting functions mid-implementation.

This approach excels at finding code by behavior in large codebases with
inconsistent naming. The trade-off is significantly slower indexing (LLM call
per chunk) and higher API costs (both chat and embedding models). Often
overkill for well-documented code or simple projects.

## Combining strategies with hybrid retrieval

Each strategy has strengths and weaknesses. Combining them captures both
semantic understanding and exact term matching:

```yaml
rag:
  knowledge:
    docs: [./documentation, ./src]
    strategies:
      - type: chunked-embeddings
        embedding_model: openai/text-embedding-3-small
        vector_dimensions: 1536
        database: ./vector.db
        limit: 20

      - type: bm25
        database: ./bm25.db
        limit: 15

    results:
      fusion:
        strategy: rrf
        k: 60
      deduplicate: true
      limit: 5
```

### How fusion works

Both strategies run in parallel, each returning its top candidates (20 and 15
in this example). Fusion combines results using rank-based scoring, removes
duplicates, and returns the top 5 final results. Your agent gets results that
work for both semantic queries ("how do I...") and exact term searches ("find
`configure_auth` function").

### Fusion strategies

RRF (Reciprocal Rank Fusion) is recommended. It combines results based on rank
rather than absolute scores, which works reliably when strategies use different
scoring scales. No tuning required.

For weighted fusion, you give more importance to one strategy:

```yaml
fusion:
  strategy: weighted
  weights:
    chunked-embeddings: 0.7
    bm25: 0.3
```

This requires tuning for your content. Use it when you know one approach works
better for your use case.

Max score fusion takes the highest score across strategies:

```yaml
fusion:
  strategy: max
```

This only works if strategies use comparable scoring scales. Simple but less
sophisticated than RRF.

## Improving retrieval quality

### Reranking results

Initial retrieval optimizes for speed. Reranking rescores results with a more
sophisticated model for better relevance:

```yaml
results:
  reranking:
    model: openai/gpt-5-mini
    threshold: 0.3
    criteria: |
      When scoring relevance, prioritize:
      - Official documentation over community content
      - Recent information over outdated material
      - Practical examples over theoretical explanations
      - Code implementations over design discussions
  limit: 5
```

The `criteria` field is powerful - use it to encode domain knowledge about what
makes results relevant for your specific use case. The more specific your
criteria, the better the reranking.

Trade-off: Significantly better results but adds latency and API costs (LLM
call for scoring each result).

### Chunking configuration

How you split documents dramatically affects retrieval quality. Tailor chunking
to your content type. Chunk size is measured in characters (Unicode code
points), not tokens.

For documentation and prose, use moderate chunks with overlap:

```yaml
chunking:
  size: 1000
  overlap: 100
  respect_word_boundaries: true
```

Overlap preserves context at chunk boundaries. Respecting word boundaries
prevents cutting words in half.

For code, use larger chunks with AST-based splitting:

```yaml
chunking:
  size: 2000
  code_aware: true
```

This keeps functions intact. The `code_aware` setting uses tree-sitter to
respect code structure.

> Note
>
> Currently only Go is supported; support for additional languages is planned.

For short, focused content like API references:

```yaml
chunking:
  size: 500
  overlap: 50
```

Brief sections need less overlap since they're naturally self-contained.

Experiment with these values. If retrieval misses context, increase chunk size
or overlap. If results are too broad, decrease chunk size.

## Making decisions about RAG

### When to use RAG

Use RAG when:

- Your content is too large for the context window
- You want targeted retrieval, not everything at once
- Content changes and needs to stay current
- Agent needs to search across many files

Don't use RAG when:

- Content is small enough to include in agent instructions
- Information rarely changes (consider prompt engineering instead)
- You need real-time data (RAG uses pre-indexed snapshots)
- Content is already in a searchable format the agent can query directly

### Choosing retrieval strategies

Use semantic search (chunked-embeddings) for user-facing documentation, content
with varied terminology, and conceptual searches where users phrase questions
differently than your docs.

Use keyword search (BM25) for code identifiers, function names, API endpoints,
error messages, and any content where exact term matching matters. Essential
for technical jargon and proper nouns.

Use LLM-enhanced semantic (semantic-embeddings) for code search by
functionality, finding implementations by behavior rather than name, or complex
technical content requiring deep understanding. Choose this when accuracy
matters more than indexing speed.

Use hybrid (multiple strategies) for general-purpose search across mixed
content, when you're unsure which approach works best, or for production
systems where quality matters most. Maximum coverage at the cost of complexity.

### Tuning for your project

Start with defaults, then adjust based on results.

If retrieval misses relevant content:

- Increase `limit` in strategies to retrieve more candidates
- Adjust `threshold` to be less strict
- Increase chunk `size` to capture more context
- Add more retrieval strategies

If retrieval returns irrelevant content:

- Decrease `limit` to fewer candidates
- Increase `threshold` to be more strict
- Add reranking with specific criteria
- Decrease chunk `size` for more focused results

If indexing is too slow:

- Increase `batch_size` for fewer API calls
- Increase `max_embedding_concurrency` for parallelism
- Consider BM25 instead of embeddings (local, no API)
- Use smaller embedding models

If results lack context:

- Increase chunk `overlap`
- Increase chunk `size`
- Use `return_full_content: true` to return entire documents
- Add neighboring chunks to results

## Further reading

- [Configuration reference](https://docs.docker.com/ai/cagent/reference/config/#rag) - Complete RAG options and
  parameters
- [RAG examples](https://github.com/docker/cagent/tree/main/examples/rag) -
  Working configurations for different scenarios
- [Tools reference](https://docs.docker.com/ai/cagent/reference/toolsets/) - How RAG search tools work in agent workflows

---

# CLI reference

> Complete reference for cagent command-line interface

# CLI reference

   Table of contents

---

Command-line interface for running, managing, and deploying AI agents.

For agent configuration file syntax, see the [Configuration file
reference](https://docs.docker.com/ai/cagent/reference/config/). For toolset capabilities, see the [Toolsets
reference](https://docs.docker.com/ai/cagent/reference/toolsets/).

## Synopsis

```console
$ cagent [command] [flags]
```

## Global flags

Work with all commands:

| Flag | Type | Default | Description |
| --- | --- | --- | --- |
| -d,--debug | boolean | false | Enable debug logging |
| -o,--otel | boolean | false | Enable OpenTelemetry |
| --log-file | string | - | Debug log file path |

Debug logs write to `~/.cagent/cagent.debug.log` by default. Override with
`--log-file`.

## Runtime flags

Work with most commands. Supported commands link to this section.

| Flag | Type | Default | Description |
| --- | --- | --- | --- |
| --models-gateway | string | - | Models gateway address |
| --env-from-file | array | - | Load environment variables from file |
| --code-mode-tools | boolean | false | Enable JavaScript tool orchestration |
| --working-dir | string | - | Working directory for the session |

Set `--models-gateway` via `CAGENT_MODELS_GATEWAY` environment variable.

## Commands

### a2a

Expose agent via the Agent2Agent (A2A) protocol. Allows other A2A-compatible
systems to discover and interact with your agent. Auto-selects an available
port if not specified.

```console
$ cagent a2a agent-file|registry-ref
```

> Note
>
> A2A support is currently experimental and needs further work. Tool calls are
> handled internally and not exposed as separate ADK events. Some ADK features
> are not yet integrated.

Arguments:

- `agent-file|registry-ref` - Path to YAML or OCI registry reference (required)

Flags:

| Flag | Type | Default | Description |
| --- | --- | --- | --- |
| -a,--agent | string | root | Agent name |
| --port | integer | 0 | Port (0 = random) |

Supports [runtime flags](#runtime-flags).

Examples:

```console
$ cagent a2a ./agent.yaml --port 8080
$ cagent a2a agentcatalog/pirate --port 9000
```

### acp

Start agent as ACP (Agent Client Protocol) server on stdio for editor integration.
See [ACP integration](https://docs.docker.com/ai/cagent/integrations/acp/) for setup guides.

```console
$ cagent acp agent-file|registry-ref
```

Arguments:

- `agent-file|registry-ref` - Path to YAML or OCI registry reference (required)

Supports [runtime flags](#runtime-flags).

### alias add

Create alias for agent.

```console
$ cagent alias add name target
```

Arguments:

- `name` - Alias name (required)
- `target` - Path to YAML or registry reference (required)

Examples:

```console
$ cagent alias add dev ./dev-agent.yaml
$ cagent alias add prod docker.io/user/prod-agent:latest
$ cagent alias add default ./agent.yaml
```

Setting alias name to "default" lets you run `cagent run` without arguments.

### alias list

List all aliases.

```console
$ cagent alias list
$ cagent alias ls
```

### alias remove

Remove alias.

```console
$ cagent alias remove name
$ cagent alias rm name
```

Arguments:

- `name` - Alias name (required)

### api

HTTP API server.

```console
$ cagent api agent-file|agents-dir
```

Arguments:

- `agent-file|agents-dir` - Path to YAML or directory with agents (required)

Flags:

| Flag | Type | Default | Description |
| --- | --- | --- | --- |
| -l,--listen | string | :8080 | Listen address |
| -s,--session-db | string | session.db | Session database path |
| --pull-interval | integer | 0 | Auto-pull OCI ref every N minutes |

Supports [runtime flags](#runtime-flags).

Examples:

```console
$ cagent api ./agent.yaml
$ cagent api ./agents/ --listen :9000
$ cagent api docker.io/user/agent --pull-interval 10
```

The `--pull-interval` flag works only with OCI references. Automatically pulls and reloads at the specified interval.

### build

Build Docker image for agent.

```console
$ cagent build agent-file|registry-ref [image-name]
```

Arguments:

- `agent-file|registry-ref` - Path to YAML or OCI registry reference (required)
- `image-name` - Docker image name (optional)

Flags:

| Flag | Type | Default | Description |
| --- | --- | --- | --- |
| --dry-run | boolean | false | Print Dockerfile only |
| --push | boolean | false | Push image after build |
| --no-cache | boolean | false | Build without cache |
| --pull | boolean | false | Pull all referenced images |

Example:

```console
$ cagent build ./agent.yaml myagent:latest
$ cagent build ./agent.yaml --dry-run
```

### catalog list

List catalog agents.

```console
$ cagent catalog list [org]
```

Arguments:

- `org` - Organization name (optional, default: `agentcatalog`)

Queries Docker Hub for agent repositories.

### debug config

Show resolved agent configuration.

```console
$ cagent debug config agent-file|registry-ref
```

Arguments:

- `agent-file|registry-ref` - Path to YAML or OCI registry reference (required)

Supports [runtime flags](#runtime-flags).

Shows canonical configuration in YAML after all processing and defaults.

### debug toolsets

List agent tools.

```console
$ cagent debug toolsets agent-file|registry-ref
```

Arguments:

- `agent-file|registry-ref` - Path to YAML or OCI registry reference (required)

Supports [runtime flags](#runtime-flags).

Lists all tools for each agent in the configuration.

### eval

Run evaluation tests.

```console
$ cagent eval agent-file|registry-ref [eval-dir]
```

Arguments:

- `agent-file|registry-ref` - Path to YAML or OCI registry reference (required)
- `eval-dir` - Evaluation files directory (optional, default: `./evals`)

Supports [runtime flags](#runtime-flags).

### exec

Single message execution without TUI.

```console
$ cagent exec agent-file|registry-ref [message|-]
```

Arguments:

- `agent-file|registry-ref` - Path to YAML or OCI registry reference (required)
- `message` - Prompt, or `-` for stdin (optional)

Same flags as [run](#run).

Supports [runtime flags](#runtime-flags).

Examples:

```console
$ cagent exec ./agent.yaml
$ cagent exec ./agent.yaml "Check for security issues"
$ echo "Instructions" | cagent exec ./agent.yaml -
```

### feedback

Submit feedback.

```console
$ cagent feedback
```

Shows link to submit feedback.

### mcp

MCP (Model Context Protocol) server on stdio. Exposes agents as tools to MCP
clients. See [MCP integration](https://docs.docker.com/ai/cagent/integrations/mcp/) for setup guides.

```console
$ cagent mcp agent-file|registry-ref
```

Arguments:

- `agent-file|registry-ref` - Path to YAML or OCI registry reference (required)

Supports [runtime flags](#runtime-flags).

Examples:

```console
$ cagent mcp ./agent.yaml
$ cagent mcp docker.io/user/agent:latest
```

### new

Create agent configuration interactively.

```console
$ cagent new [message...]
```

Flags:

| Flag | Type | Default | Description |
| --- | --- | --- | --- |
| --model | string | - | Model asprovider/model |
| --max-iterations | integer | 0 | Maximum agentic loop iterations |

Supports [runtime flags](#runtime-flags).

Opens interactive TUI to configure and generate agent YAML.

### pull

Pull agent from OCI registry.

```console
$ cagent pull registry-ref
```

Arguments:

- `registry-ref` - OCI registry reference (required)

Flags:

| Flag | Type | Default | Description |
| --- | --- | --- | --- |
| --force | boolean | false | Pull even if already exists |

Example:

```console
$ cagent pull docker.io/user/agent:latest
```

Saves to local YAML file.

### push

Push agent to OCI registry.

```console
$ cagent push agent-file registry-ref
```

Arguments:

- `agent-file` - Path to local YAML (required)
- `registry-ref` - OCI reference like `docker.io/user/agent:latest` (required)

Example:

```console
$ cagent push ./agent.yaml docker.io/myuser/myagent:latest
```

### run

Interactive terminal UI for agent sessions.

```console
$ cagent run [agent-file|registry-ref] [message|-]
```

Arguments:

- `agent-file|registry-ref` - Path to YAML or OCI registry reference (optional)
- `message` - Initial prompt, or `-` for stdin (optional)

Flags:

| Flag | Type | Default | Description |
| --- | --- | --- | --- |
| -a,--agent | string | root | Agent name |
| --yolo | boolean | false | Auto-approve all tool calls |
| --attach | string | - | Attach image file |
| --model | array | - | Override model (repeatable) |
| --dry-run | boolean | false | Initialize without executing |
| --remote | string | - | Remote runtime address |

Supports [runtime flags](#runtime-flags).

Examples:

```console
$ cagent run ./agent.yaml
$ cagent run ./agent.yaml "Analyze this codebase"
$ cagent run ./agent.yaml --agent researcher
$ echo "Instructions" | cagent run ./agent.yaml -
$ cagent run
```

Running without arguments uses the default agent or a "default" alias if configured.

Shows interactive TUI in a terminal. Falls back to exec mode otherwise.

#### Interactive commands

TUI slash commands:

| Command | Description |
| --- | --- |
| /exit | Exit |
| /reset | Clear history |
| /eval | Save conversation for evaluation |
| /compact | Compact conversation |
| /yolo | Toggle auto-approval |

### version

Print version information.

```console
$ cagent version
```

Shows cagent version and commit hash.

## Environment variables

| Variable | Description |
| --- | --- |
| CAGENT_MODELS_GATEWAY | Models gateway address |
| TELEMETRY_ENABLED | Telemetry control (setfalse) |
| CAGENT_HIDE_TELEMETRY_BANNER | Hide telemetry banner (set1) |
| OTEL_EXPORTER_OTLP_ENDPOINT | OpenTelemetry endpoint |

## Model overrides

Override models specified in your configuration file using the `--model` flag.

Format: `[agent=]provider/model`

Without an agent name, the model applies to all agents. With an agent name, it applies only to that specific agent.

Apply to all agents:

```console
$ cagent run ./agent.yaml --model gpt-5
$ cagent run ./agent.yaml --model anthropic/claude-sonnet-4-5
```

Apply to specific agents only:

```console
$ cagent run ./agent.yaml --model researcher=gpt-5
$ cagent run ./agent.yaml --model "agent1=gpt-5,agent2=claude-sonnet-4-5"
```

Providers: `openai`, `anthropic`, `google`, `dmr`

Omit provider for automatic selection based on model name.
