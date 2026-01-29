# Best practices and more

# Best practices

> Patterns and techniques for building effective cagent agents

# Best practices

   Table of contents

---

Patterns you learn from building and running cagent agents. These aren't
features or configuration options - they're approaches that work well in
practice.

## Handling large command outputs

Shell commands that produce large output can overflow your agent's context
window. Validation tools, test suites, and build logs often generate thousands
of lines. If you capture this output directly, it consumes all available context
and the agent fails.

The solution: redirect output to a file, then read the file. The Read tool
automatically truncates large files to 2000 lines, and your agent can navigate
through it if needed.

**Don't do this:**

```yaml
reviewer:
  instruction: |
    Run validation: `docker buildx bake validate`
    Check the output for errors.
  toolsets:
    - type: shell
```

The validation output goes directly into context. If it's large, the agent fails
with a context overflow error.

**Do this:**

```yaml
reviewer:
  instruction: |
    Run validation and save output:
    `docker buildx bake validate > validation.log 2>&1`

    Read validation.log to check for errors.
    The file can be large - read the first 2000 lines.
    Errors usually appear at the beginning.
  toolsets:
    - type: filesystem
    - type: shell
```

The output goes to a file, not context. The agent reads what it needs using the
filesystem toolset.

## Structuring agent teams

A single agent handling multiple responsibilities makes instructions complex and
behavior unpredictable. Breaking work across specialized agents produces better
results.

The coordinator pattern works well: a root agent understands the overall task
and delegates to specialists. Each specialist focuses on one thing.

**Example: Documentation writing team**

```yaml
agents:
  root:
    description: Technical writing coordinator
    instruction: |
      Coordinate documentation work:
      1. Delegate to writer for content creation
      2. Delegate to editor for formatting polish
      3. Delegate to reviewer for validation
      4. Loop back through editor if reviewer finds issues
    sub_agents: [writer, editor, reviewer]
    toolsets: [filesystem, todo]

  writer:
    description: Creates and edits documentation content
    instruction: |
      Write clear, practical documentation.
      Focus on content quality - the editor handles formatting.
    toolsets: [filesystem, think]

  editor:
    description: Polishes formatting and style
    instruction: |
      Fix formatting issues, wrap lines, run prettier.
      Remove AI-isms and polish style.
      Don't change meaning or add content.
    toolsets: [filesystem, shell]

  reviewer:
    description: Runs validation tools
    instruction: |
      Run validation suite, report failures.
    toolsets: [filesystem, shell]
```

Each agent has clear responsibilities. The writer doesn't worry about line
wrapping. The editor doesn't generate content. The reviewer just runs tools.

This example uses `sub_agents` where root delegates discrete tasks and gets
results back. The root agent maintains control and coordinates all work. For
different coordination patterns where agents should transfer control to each
other, see the `handoffs` mechanism in the [configuration
reference](https://docs.docker.com/ai/cagent/reference/config/#task-delegation-versus-conversation-handoff).

**When to use teams:**

- Multiple distinct steps in your workflow
- Different skills required (writing ↔ editing ↔ testing)
- One step might need to retry based on later feedback

**When to use a single agent:**

- Simple, focused tasks
- All work happens in one step
- Adding coordination overhead doesn't help

## Optimizing RAG performance

RAG indexing takes time when you have many files. A configuration that indexes
your entire codebase might take minutes to start. Optimize for what your agent
actually needs.

**Narrow the scope:**

Don't index everything. Index what's relevant for the agent's work.

```yaml
# Too broad - indexes entire codebase
rag:
  codebase:
    docs: [./]

# Better - indexes only relevant directories
rag:
  codebase:
    docs: [./src/api, ./docs, ./examples]
```

If your agent only works with API code, don't index tests, vendor directories,
or generated files.

**Increase batching and concurrency:**

Process more chunks per API call and make parallel requests.

```yaml
strategies:
  - type: chunked-embeddings
    embedding_model: openai/text-embedding-3-small
    batch_size: 50 # More chunks per API call
    max_embedding_concurrency: 10 # Parallel requests
    chunking:
      size: 2000 # Larger chunks = fewer total chunks
      overlap: 150
```

This reduces both API calls and indexing time.

**Consider BM25 for fast local search:**

If you need exact term matching (function names, error messages, identifiers),
BM25 is fast and runs locally without API calls.

```yaml
strategies:
  - type: bm25
    database: ./bm25.db
    chunking:
      size: 1500
```

Combine with embeddings using hybrid retrieval when you need both semantic
understanding and exact matching.

## Preserving document scope

When building agents that update documentation, a common problem: the agent
transforms minimal guides into tutorials. It adds prerequisites,
troubleshooting, best practices, examples, and detailed explanations to
everything.

These additions might individually be good, but they change the document's
character. A focused 90-line how-to becomes a 200-line reference.

**Build this into instructions:**

```yaml
writer:
  instruction: |
    When updating documentation:

    1. Understand the current document's scope and length
    2. Match that character - don't transform minimal guides into tutorials
    3. Add only what's genuinely missing
    4. Value brevity - not every topic needs comprehensive coverage

    Good additions fill gaps. Bad additions change the document's character.
    When in doubt, add less rather than more.
```

Tell your agents explicitly to preserve the existing document's scope. Without
this guidance, they default to being comprehensive.

## Model selection

Choose models based on the agent's role and complexity.

**Use larger models (Sonnet, GPT-5) for:**

- Complex reasoning and planning
- Writing and editing content
- Coordinating multiple agents
- Tasks requiring judgment and creativity

**Use smaller models (Haiku, GPT-5 Mini) for:**

- Running validation tools
- Simple structured tasks
- Reading logs and reporting errors
- High-volume, low-complexity work

Example from the documentation writing team:

```yaml
agents:
  root:
    model: anthropic/claude-sonnet-4-5 # Complex coordination
  writer:
    model: anthropic/claude-sonnet-4-5 # Creative content work
  editor:
    model: anthropic/claude-sonnet-4-5 # Judgment about style
  reviewer:
    model: anthropic/claude-haiku-4-5 # Just runs validation
```

The reviewer uses Haiku because it runs commands and checks for errors. No
complex reasoning needed, and Haiku is faster and cheaper.

## What's next

- Review [configuration reference](https://docs.docker.com/ai/cagent/reference/config/) for all available
  options
- Check [toolsets reference](https://docs.docker.com/ai/cagent/reference/toolsets/) to understand what tools
  agents can use
- See [example
  configurations](https://github.com/docker/cagent/tree/main/examples) for
  complete working agents
- Read the [RAG guide](https://docs.docker.com/ai/cagent/rag/) for detailed retrieval optimization

---

# Evals

> Test your agents with saved conversations

# Evals

   Table of contents

---

Evaluations (evals) help you track how your agent's behavior changes over time.
When you save a conversation as an eval, you can replay it later to see if the
agent responds differently. Evals measure consistency, not correctness - they
tell you if behavior changed, not whether it's right or wrong.

## What are evals

An eval is a saved conversation you can replay. When you run evals, cagent
replays the user messages and compares the new responses against the original
saved conversation. High scores mean the agent behaved similarly; low scores
mean behavior changed.

What you do with that information depends on why you saved the conversation.
You might save successful conversations to catch regressions, or save failure
cases to document known issues and track whether they improve.

## Common workflows

How you use evals depends on what you're trying to accomplish:

Regression testing: Save conversations where your agent performs well. When you
make changes later (upgrade models, update prompts, refactor code), run the
evals. High scores mean behavior stayed consistent, which is usually what you
want. Low scores mean something changed - examine the new behavior to see if
it's still correct.

Tracking improvements: Save conversations where your agent struggles or fails.
As you make improvements, run these evals to see how behavior evolves. Low
scores indicate the agent now behaves differently, which might mean you fixed
the issue. You'll need to manually verify the new behavior is actually better.

Documenting edge cases: Save interesting or unusual conversations regardless of
quality. Use them to understand how your agent handles edge cases and whether
that behavior changes over time.

Evals measure whether behavior changed. You determine if that change is good or
bad.

## Creating an eval

Save a conversation from an interactive session:

```console
$ cagent run ./agent.yaml
```

Have a conversation with your agent, then save it as an eval:

```console
> /eval test-case-name
Eval saved to evals/test-case-name.json
```

The conversation is saved to the `evals/` directory in your current working
directory. You can organize eval files in subdirectories if needed.

## Running evals

Run all evals in the default directory:

```console
$ cagent eval ./agent.yaml
```

Use a custom eval directory:

```console
$ cagent eval ./agent.yaml ./my-evals
```

Run evals against an agent from a registry:

```console
$ cagent eval agentcatalog/myagent
```

Example output:

```console
$ cagent eval ./agent.yaml
--- 0
First message: tell me something interesting about kil
Eval file: c7e556c5-dae5-4898-a38c-73cc8e0e6abe
Tool trajectory score: 1.000000
Rouge-1 score: 0.447368
Cost: 0.00
Output tokens: 177
```

## Understanding results

For each eval, cagent shows:

- **First message** - The initial user message from the saved conversation
- **Eval file** - The UUID of the eval file being run
- **Tool trajectory score** - How similarly the agent used tools (0-1 scale,
  higher is better)
- **ROUGE-1score** - Text
  similarity between responses (0-1 scale, higher is better)
- **Cost** - The cost for this eval run
- **Output tokens** - Number of tokens generated

Higher scores mean the agent behaved more similarly to the original recorded
conversation. A score of 1.0 means identical behavior.

### What the scores mean

**Tool trajectory score** measures whether the agent called the same tools in
the same order as the original conversation. Lower scores might indicate the
agent found a different approach to solve the problem, which isn't necessarily
wrong but worth investigating.

**Rouge-1 score** measures how similar the response text is to the original.
This is a heuristic measure - different wording might still be correct, so use
this as a signal rather than absolute truth.

### Interpreting your results

Scores close to 1.0 mean your changes maintained consistent behavior - the
agent is using the same approach and producing similar responses. This is
generally good; your changes didn't break existing functionality.

Lower scores mean behavior changed compared to the saved conversation. This
could be a regression where the agent now performs worse, or it could be an
improvement where the agent found a better approach.

When scores drop, examine the actual behavior to determine if it's better or
worse. The eval files are stored as JSON in your evals directory - open the
file to see the original conversation. Then test your modified agent with the
same input to compare responses. If the new response is better, save a new
conversation to replace the eval. If it's worse, you found a regression.

The scores guide you to what changed. Your judgment determines if the change is
good or bad.

## When to use evals

Evals help you track behavior changes over time. They're useful for catching
regressions when you upgrade models or dependencies, documenting known failure
cases you want to fix, and understanding how edge cases evolve as you iterate.

Evals aren't appropriate for determining which agent configuration works best -
they measure similarity to a saved conversation, not correctness. Use manual
testing to evaluate different configurations and decide which works better.

Save conversations worth tracking. Build a collection of important workflows,
interesting edge cases, and known issues. Run your evals when making changes to
see what shifted.

## What's next

- Check the [CLI reference](https://docs.docker.com/ai/cagent/reference/cli/#eval) for all `cagent eval`
  options
- Learn [best practices](https://docs.docker.com/ai/cagent/best-practices/) for building effective agents
- Review [example configurations](https://github.com/docker/cagent/tree/main/examples)
  for different agent types

---

# A2A mode

> Expose cagent agents via the Agent-to-Agent protocol

# A2A mode

   Table of contents

---

A2A mode runs your cagent agent as an HTTP server that other systems can call
using the Agent-to-Agent protocol. This lets you expose your agent as a service
that other agents or applications can discover and invoke over the network.

Use A2A when you want to make your agent callable by other systems over HTTP.
For editor integration, see [ACP integration](https://docs.docker.com/ai/cagent/integrations/acp/). For using agents as
tools in MCP clients, see [MCP integration](https://docs.docker.com/ai/cagent/integrations/mcp/).

## Prerequisites

Before starting an A2A server, you need:

- cagent installed - See the [installation guide](https://docs.docker.com/ai/cagent/#installation)
- Agent configuration - A YAML file defining your agent. See the
  [tutorial](https://docs.docker.com/ai/cagent/tutorial/)
- API keys configured - If using cloud model providers (see [Model
  providers](https://docs.docker.com/ai/cagent/model-providers/))

## Starting an A2A server

Basic usage:

```console
$ cagent a2a ./agent.yaml
```

Your agent is now accessible via HTTP. Other A2A systems can discover your
agent's capabilities and call it.

Custom port:

```console
$ cagent a2a ./agent.yaml --port 8080
```

Specific agent in a team:

```console
$ cagent a2a ./agent.yaml --agent engineer
```

From OCI registry:

```console
$ cagent a2a agentcatalog/pirate --port 9000
```

## HTTP endpoints

When you start an A2A server, it exposes two HTTP endpoints:

### Agent card:/.well-known/agent-card

The agent card describes your agent's capabilities:

```console
$ curl http://localhost:8080/.well-known/agent-card
```

```json
{
  "name": "agent",
  "description": "A helpful coding assistant",
  "skills": [
    {
      "id": "agent_root",
      "name": "root",
      "description": "A helpful coding assistant",
      "tags": ["llm", "cagent"]
    }
  ],
  "preferredTransport": "jsonrpc",
  "url": "http://localhost:8080/invoke",
  "capabilities": {
    "streaming": true
  },
  "version": "0.1.0"
}
```

### Invoke endpoint:/invoke

Call your agent by sending a JSON-RPC request:

```console
$ curl -X POST http://localhost:8080/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "req-1",
    "method": "message/send",
    "params": {
      "message": {
        "role": "user",
        "parts": [
          {
            "kind": "text",
            "text": "What is 2+2?"
          }
        ]
      }
    }
  }'
```

The response includes the agent's reply:

```json
{
  "jsonrpc": "2.0",
  "id": "req-1",
  "result": {
    "artifacts": [
      {
        "parts": [
          {
            "kind": "text",
            "text": "2+2 equals 4."
          }
        ]
      }
    ]
  }
}
```

## Example: Multi-agent workflow

Here's a concrete scenario where A2A is useful. You have two agents:

1. A general-purpose agent that interacts with users
2. A specialized code review agent with access to your codebase

Run the specialist as an A2A server:

```console
$ cagent a2a ./code-reviewer.yaml --port 8080
Listening on 127.0.0.1:8080
```

Configure your main agent to call it:

```yaml
agents:
  root:
    model: anthropic/claude-sonnet-4-5
    instruction: You are a helpful assistant
    toolsets:
      - type: a2a
        url: http://localhost:8080
        name: code-reviewer
```

Now when users ask the main agent about code quality, it can delegate to the
specialist. The main agent sees `code-reviewer` as a tool it can call, and the
specialist has access to the codebase tools it needs.

## Calling other A2A agents

Your cagent agents can call remote A2A agents as tools. Configure the A2A
toolset with the remote agent's URL:

```yaml
agents:
  root:
    toolsets:
      - type: a2a
        url: http://localhost:8080
        name: specialist
```

The `url` specifies where the remote agent is running, and `name` is an
optional identifier for the tool. Your agent can now delegate tasks to the
remote specialist agent.

If the remote agent requires authentication or custom headers:

```yaml
agents:
  root:
    toolsets:
      - type: a2a
        url: http://localhost:8080
        name: specialist
        remote:
          headers:
            Authorization: Bearer token123
            X-Custom-Header: value
```

## What's next

- Review the [CLI reference](https://docs.docker.com/ai/cagent/reference/cli/#a2a) for all `cagent a2a`
  options
- Learn about [MCP mode](https://docs.docker.com/ai/cagent/integrations/mcp/) to expose agents as tools in MCP clients
- Learn about [ACP mode](https://docs.docker.com/ai/cagent/integrations/acp/) for editor integration
- Share your agents with [OCI registries](https://docs.docker.com/ai/cagent/sharing-agents/)

---

# ACP integration

> Configure your editor or IDE to use cagent agents as coding assistants

# ACP integration

   Table of contents

---

Run cagent agents directly in your editor using the Agent Client Protocol (ACP).
Your agent gets access to your editor's filesystem context and can read and
modify files as you work. The editor handles file operations while cagent
provides the AI capabilities.

This guide shows you how to configure Neovim, or Zed to run cagent agents. If
you're looking to expose cagent agents as tools to MCP clients like Claude
Desktop or Claude Code, see [MCP integration](https://docs.docker.com/ai/cagent/integrations/mcp/) instead.

## How it works

When you run cagent with ACP, it becomes part of your editor's environment. You
select code, highlight a function, or reference a file - the agent sees what you
see. No copying file paths or switching to a terminal.

Ask "explain this function" and the agent reads the file you're viewing. Ask it
to "add error handling" and it edits the code right in your editor. The agent
works with your editor's view of the project, not some external file system it
has to navigate.

The difference from running cagent in a terminal: file operations go through
your editor instead of the agent directly accessing your filesystem. When the
agent needs to read or write a file, it requests it from your editor. This keeps
the agent's view of your code synchronized with yours - same working directory,
same files, same state.

## Prerequisites

Before configuring your editor, you need:

- **cagent installed** - See the [installation guide](https://docs.docker.com/ai/cagent/#installation)
- **Agent configuration** - A YAML file defining your agent. See the
  [tutorial](https://docs.docker.com/ai/cagent/tutorial/) or [example
  configurations](https://github.com/docker/cagent/tree/main/examples)
- **Editor with ACP support** - Neovim, Intellij, Zed, etc.

Your agents will use model provider API keys from your shell environment
(`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, etc.). Make sure these are set before
launching your editor.

## Editor configuration

### Zed

Zed has built-in ACP support.

1. Add cagent to your agent servers in `settings.json`:
  ```json
  {
    "agent_servers": {
      "my-cagent-team": {
        "command": "cagent",
        "args": ["acp", "agent.yml"]
      }
    }
  }
  ```
  Replace:
  - `my-cagent-team` with the name you want to use for the agent
  - `agent.yml` with the path to your agent configuration file.
  If you have multiple agent files that you like to run separately, you can
  create multiple entries under `agent_servers` for each agent.
2. Start a new external agent thread. Select your agent in the drop-down list.
  ![New external thread with cagent in Zed](https://docs.docker.com/ai/cagent/images/cagent-acp-zed.avif)  ![New external thread with cagent in Zed](https://docs.docker.com/ai/cagent/images/cagent-acp-zed.avif)

### Neovim

Use the [CodeCompanion](https://github.com/olimorris/codecompanion.nvim) plugin,
which has native support for cagent through a built-in adapter:

1. [Install CodeCompanion](https://codecompanion.olimorris.dev/installation)
  through your plugin manager.
2. Extend the `cagent` adapter in your CodeCompanion config:
  ```lua
  require("codecompanion").setup({
    adapters = {
      acp = {
        cagent = function()
          return require("codecompanion.adapters").extend("cagent", {
            commands = {
              default = {
                "cagent",
                "acp",
                "agent.yml",
              },
            },
          })
        end,
      },
    },
  })
  ```
  Replace `agent.yml` with the path to your agent configuration file. If you
  have multiple agent files that you like to run separately, you can create
  multiple commands for each agent.
3. Restart Neovim and launch CodeCompanion:
  ```plaintext
  :CodeCompanion
  ```
4. Switch to the cagent adapter (keymap `ga` in the CodeCompanion buffer, by
  default).

See the [CodeCompanion ACP
documentation](https://codecompanion.olimorris.dev/usage/acp-protocol) for more
information about ACP support in CodeCompanion. Note that terminal operations
are not supported, so [toolsets](https://docs.docker.com/ai/cagent/reference/toolsets/) like `shell` or
`script_shell` are not usable through CodeCompanion.

## Agent references

You can specify your agent configuration as a local file path or OCI registry
reference:

```console
# Local file path
$ cagent acp ./agent.yml

# OCI registry reference
$ cagent acp agentcatalog/pirate
$ cagent acp dockereng/myagent:v1.0.0
```

Use the same syntax in your editor configuration:

```json
{
  "agent_servers": {
    "myagent": {
      "command": "cagent",
      "args": ["acp", "agentcatalog/pirate"]
    }
  }
}
```

Registry references enable team sharing, version management, and clean
configuration without local file paths. See [Sharing
agents](https://docs.docker.com/ai/cagent/sharing-agents/) for details on using OCI registries.

## Testing your setup

Verify your configuration works:

1. Start the cagent ACP server using your editor's configured method
2. Send a test prompt through your editor's interface
3. Check that the agent responds
4. Verify filesystem operations work by asking the agent to read a file

If the agent starts but can't access files or perform other actions, check:

- Working directory in your editor is set correctly to your project root
- Agent configuration file path is absolute or relative to working directory
- Your editor or plugin properly implements ACP protocol features

## What's next

- Review the [configuration reference](https://docs.docker.com/ai/cagent/reference/config/) for advanced
  agent setup
- Explore the [toolsets reference](https://docs.docker.com/ai/cagent/reference/toolsets/) to learn what tools
  are available
- Add [RAG for codebase search](https://docs.docker.com/ai/cagent/rag/) to your agent
- Check the [CLI reference](https://docs.docker.com/ai/cagent/reference/cli/) for all `cagent acp` options
- Browse [example
  configurations](https://github.com/docker/cagent/tree/main/examples) for
  inspiration

---

# MCP mode

> Expose cagent agents as tools to MCP clients like Claude Desktop and Claude Code

# MCP mode

   Table of contents

---

When you run cagent in MCP mode, your agents show up as tools in Claude Desktop
and other MCP clients. Instead of switching to a terminal to run your security
agent, you ask Claude to use it and Claude calls it for you.

This guide covers setup for Claude Desktop and Claude Code. If you want agents
embedded in your editor instead, see [ACP integration](https://docs.docker.com/ai/cagent/integrations/acp/).

## How it works

You configure Claude Desktop (or another MCP client) to connect to cagent. Your
agents appear in Claude's tool list. When you ask Claude to use one, it calls
that agent through the MCP protocol.

Say you have a security agent configured. Ask Claude Desktop "Use the security
agent to audit this authentication code" and Claude calls it. The agent runs
with its configured tools (filesystem, shell, whatever you gave it), then
returns results to Claude.

If your configuration has multiple agents, each one becomes a separate tool. A
config with `root`, `designer`, and `engineer` agents gives Claude three tools
to choose from. Claude might call the engineer directly or use the root
coordinator—depends on your agent descriptions and what you ask for.

## MCP Gateway

Docker provides an
[MCP Gateway](https://docs.docker.com/ai/mcp-catalog-and-toolkit/mcp-gateway/) that
gives cagent agents access to a catalog of pre-configured MCP servers. Instead
of configuring individual MCP servers, agents can use the gateway to access
tools like web search, database queries, and more.

Configure MCP toolset with gateway reference:

```yaml
agents:
  root:
    toolsets:
      - type: mcp
        ref: docker:duckduckgo # Uses Docker MCP Gateway
```

The `docker:` prefix tells cagent to use the MCP Gateway for this server. See
the
[MCP Gateway documentation](https://docs.docker.com/ai/mcp-catalog-and-toolkit/mcp-gateway/) for
available servers and configuration options.

You can also use the
[MCP Toolkit](https://docs.docker.com/ai/mcp-catalog-and-toolkit/) to explore and
manage MCP servers interactively.

## Prerequisites

Before configuring MCP integration, you need:

- **cagent installed** - See the [installation guide](https://docs.docker.com/ai/cagent/#installation)
- **Agent configuration** - A YAML file defining your agent. See the
  [tutorial](https://docs.docker.com/ai/cagent/tutorial/) or [example
  configurations](https://github.com/docker/cagent/tree/main/examples)
- **MCP client** - Claude Desktop, Claude Code, or another MCP-compatible
  application
- **API keys** - Environment variables for any model providers your agents use
  (`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, etc.)

## MCP client configuration

Your MCP client needs to know how to start cagent and communicate with it. This
typically involves adding cagent as an MCP server in your client's
configuration.

### Claude Desktop

Add cagent to your Claude Desktop MCP settings file:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

Example configuration:

```json
{
  "mcpServers": {
    "myagent": {
      "command": "/usr/local/bin/cagent",
      "args": [
        "mcp",
        "/path/to/agent.yml",
        "--working-dir",
        "/Users/yourname/projects"
      ],
      "env": {
        "ANTHROPIC_API_KEY": "your_anthropic_key_here",
        "OPENAI_API_KEY": "your_openai_key_here"
      }
    }
  }
}
```

Configuration breakdown:

- `command`: Full path to your `cagent` binary (use `which cagent` to find it)
- `args`: MCP command arguments:
  - `mcp`: The subcommand to run cagent in MCP mode
  - `dockereng/myagent`: Your agent configuration (local file path or OCI
    reference)
  - `--working-dir`: Optional working directory for agent execution
- `env`: Environment variables your agents need:
  - Model provider API keys (`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, etc.)
  - Any other environment variables your agents reference

After updating the configuration, restart Claude Desktop. Your agents will
appear as available tools.

### Claude Code

Add cagent as an MCP server using the `claude mcp add` command:

```console
$ claude mcp add --transport stdio myagent \
  --env OPENAI_API_KEY=$OPENAI_API_KEY \
  --env ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
  -- cagent mcp /path/to/agent.yml --working-dir $(pwd)
```

Command breakdown:

- `claude mcp add`: Claude Code command to register an MCP server
- `--transport stdio`: Use stdio transport (standard for local MCP servers)
- `myagent`: Name for this MCP server in Claude Code
- `--env`: Pass environment variables (repeat for each variable)
- `--`: Separates Claude Code options from the MCP server command
- `cagent mcp /path/to/agent.yml`: The cagent MCP command with the path to your
  agent configuration
- `--working-dir $(pwd)`: Set the working directory for agent execution

After adding the server, your agents will be available as tools in Claude Code
sessions.

### Other MCP clients

For other MCP-compatible clients, you need to:

1. Start cagent with `cagent mcp /path/to/agent.yml --working-dir /project/path`
2. Configure the client to communicate with cagent over stdio
3. Pass required environment variables (API keys, etc.)

Consult your MCP client's documentation for specific configuration steps.

## Agent references

You can specify your agent configuration as a local file path or OCI registry
reference:

```console
# Local file path
$ cagent mcp ./agent.yml

# OCI registry reference
$ cagent mcp agentcatalog/pirate
$ cagent mcp dockereng/myagent:v1.0.0
```

Use the same syntax in MCP client configurations:

```json
{
  "mcpServers": {
    "myagent": {
      "command": "/usr/local/bin/cagent",
      "args": ["mcp", "agentcatalog/pirate"]
    }
  }
}
```

Registry references let your team use the same agent configuration without
managing local files. See [Sharing agents](https://docs.docker.com/ai/cagent/sharing-agents/) for details.

## Designing agents for MCP

MCP clients see each of your agents as a separate tool and can call any of them
directly. This changes how you should think about agent design compared to
running agents with `cagent run`.

### Write good descriptions

The `description` field tells the MCP client what the agent does. This is how
the client decides when to call it. "Analyzes code for security vulnerabilities
and compliance issues" is specific. "A helpful security agent" doesn't say what
it actually does.

```yaml
agents:
  security_auditor:
    description: Analyzes code for security vulnerabilities and compliance issues
    # Not: "A helpful security agent"
```

### MCP clients call agents directly

The MCP client can call any of your agents, not just root. If you have `root`,
`designer`, and `engineer` agents, the client might call the engineer directly
instead of going through root. Design each agent to work on its own:

```yaml
agents:
  engineer:
    description: Implements features and writes production code
    instruction: |
      You implement code based on requirements provided.
      You can work independently without a coordinator.
    toolsets:
      - type: filesystem
      - type: shell
```

If an agent needs others to work properly, say so in the description:
"Coordinates design and engineering agents to implement complete features."

### Test each agent on its own

MCP clients call agents individually, so test them that way:

```console
$ cagent run agent.yml --agent engineer
```

Make sure the agent works without going through root first. Check that it has
the right tools and that its instructions make sense when it's called directly.

## Testing your setup

Verify your MCP integration works:

1. Restart your MCP client after configuration changes
2. Check that cagent agents appear as available tools
3. Invoke an agent with a simple test prompt
4. Verify the agent can access its configured tools (filesystem, shell, etc.)

If agents don't appear or fail to execute, check:

- `cagent` binary path is correct and executable
- Agent configuration file exists and is valid
- All required API keys are set in environment variables
- Working directory path exists and has appropriate permissions
- MCP client logs for connection or execution errors

## Common workflows

### Call specialist agents

You have a security agent that knows your compliance rules and common
vulnerabilities. In Claude Desktop, paste some authentication code and ask "Use
the security agent to review this." The agent checks the code and reports what
it finds. You stay in Claude's interface the whole time.

### Work with agent teams

Your configuration has a coordinator that delegates to designer and engineer
agents. Ask Claude Code "Use the coordinator to implement a login form" and the
coordinator hands off UI work to the designer and code to the engineer. You get
a complete implementation without running `cagent run` yourself.

### Run domain-specific tools

You built an infrastructure agent with custom deployment scripts and monitoring
queries. Ask any MCP client "Use the infra agent to check production status" and
it runs your tools and returns results. Your deployment knowledge is now
available wherever you use MCP clients.

### Share agents

Your team keeps agents in an OCI registry. Everyone adds
`agentcatalog/security-expert` to their MCP client config. When you update the
agent, they get the new version on their next restart. No YAML files to pass
around.

## What's next

- Use the
  [MCP Gateway](https://docs.docker.com/ai/mcp-catalog-and-toolkit/mcp-gateway/) to give your
  agents access to pre-configured MCP servers
- Explore MCP servers interactively with the
  [MCP
  Toolkit](https://docs.docker.com/ai/mcp-catalog-and-toolkit/)
- Review the [configuration reference](https://docs.docker.com/ai/cagent/reference/config/) for advanced
  agent setup
- Explore the [toolsets reference](https://docs.docker.com/ai/cagent/reference/toolsets/) to learn what tools
  agents can use
- Add [RAG for codebase search](https://docs.docker.com/ai/cagent/rag/) to your agent
- Check the [CLI reference](https://docs.docker.com/ai/cagent/reference/cli/) for all `cagent mcp` options
- Browse [example
  configurations](https://github.com/docker/cagent/tree/main/examples) for
  different agent types

---

# Integrations

> Connect cagent agents to editors, MCP clients, and other agents

# Integrations

   Table of contents

---

cagent agents can integrate with different environments depending on how you
want to use them. Each integration type serves a specific purpose.

## Integration types

### ACP - Editor integration

Run cagent agents directly in your editor (Neovim, Zed). The agent sees your
editor's file context and can read and modify files through the editor's
interface. Use ACP when you want an AI coding assistant embedded in your
editor.

See [ACP integration](https://docs.docker.com/ai/cagent/integrations/acp/) for setup instructions.

### MCP - Tool integration

Expose cagent agents as tools in MCP clients like Claude Desktop or Claude
Code. Your agents appear in the client's tool list, and the client can call
them when needed. Use MCP when you want Claude Desktop (or another MCP client)
to have access to your specialized agents.

See [MCP integration](https://docs.docker.com/ai/cagent/integrations/mcp/) for setup instructions.

### A2A - Agent-to-agent communication

Run cagent agents as HTTP servers that other agents or systems can call using
the Agent-to-Agent protocol. Your agent becomes a service that other systems
can discover and invoke over the network. Use A2A when you want to build
multi-agent systems or expose your agent as an HTTP service.

See [A2A integration](https://docs.docker.com/ai/cagent/integrations/a2a/) for setup instructions.

## Choosing the right integration

| Feature | ACP | MCP | A2A |
| --- | --- | --- | --- |
| Use case | Editor integration | Agents as tools | Agent-to-agent calls |
| Transport | stdio | stdio/SSE | HTTP |
| Discovery | Editor plugin | Server manifest | Agent card |
| Best for | Code editing | Tool integration | Multi-agent systems |
| Communication | Editor calls agent | Client calls tools | Between agents |

Choose ACP if you want your agent embedded in your editor while you code.
Choose MCP if you want Claude Desktop (or another MCP client) to be able to
call your specialized agents as tools. Choose A2A if you're building
multi-agent systems where agents need to call each other over HTTP.

---

# Local models with Docker Model Runner

> Run AI models locally using Docker Model Runner - no API keys required

# Local models with Docker Model Runner

   Table of contents

---

Docker Model Runner lets you run AI models locally on your machine. No API
keys, no recurring costs, and your data stays private.

## Why use local models

Docker Model Runner lets you run models locally without API keys or recurring
costs. Your data stays on your machine, and you can work offline once models
are downloaded. This is an alternative to [cloud model
providers](https://docs.docker.com/ai/cagent/model-providers/).

## Prerequisites

You need Docker Model Runner installed and running:

- Docker Desktop (macOS/Windows) - Enable Docker Model Runner in
  **Settings > AI > Enable Docker Model Runner**. See
  [Get started with
  DMR](https://docs.docker.com/ai/model-runner/get-started/#enable-docker-model-runner) for
  detailed instructions.
- Docker Engine (Linux) - Install with `sudo apt-get install docker-model-plugin` or `sudo dnf install docker-model-plugin`. See
  [Get
  started with DMR](https://docs.docker.com/ai/model-runner/get-started/#docker-engine).

Verify Docker Model Runner is available:

```console
$ docker model version
```

If the command returns version information, you're ready to use local models.

## Using models with DMR

Docker Model Runner can run any compatible model. Models can come from:

- Docker Hub repositories (`docker.io/namespace/model-name`)
- Your own OCI artifacts packaged and pushed to any registry
- HuggingFace models directly (`hf.co/org/model-name`)
- The Docker Model catalog in Docker Desktop

To see models available to the local Docker catalog, run:

```console
$ docker model list --openai
```

To use a model, reference it in your configuration. DMR automatically pulls
models on first use if they're not already local.

## Configuration

Configure your agent to use Docker Model Runner with the `dmr` provider:

```yaml
agents:
  root:
    model: dmr/ai/qwen3
    instruction: You are a helpful assistant
    toolsets:
      - type: filesystem
```

When you first run your agent, cagent prompts you to pull the model if it's
not already available locally:

```console
$ cagent run agent.yaml
Model not found locally. Do you want to pull it now? ([y]es/[n]o)
```

## How it works

When you configure an agent to use DMR, cagent automatically connects to your
local Docker Model Runner and routes inference requests to it. If a model isn't
available locally, cagent prompts you to pull it on first use. No API keys or
authentication are required.

## Advanced configuration

For more control over model behavior, define a model configuration:

```yaml
models:
  local-qwen:
    provider: dmr
    model: ai/qwen3:14B
    temperature: 0.7
    max_tokens: 8192

agents:
  root:
    model: local-qwen
    instruction: You are a helpful coding assistant
```

### Faster inference with speculative decoding

Speed up model responses using speculative decoding with a smaller draft model:

```yaml
models:
  fast-qwen:
    provider: dmr
    model: ai/qwen3:14B
    provider_opts:
      speculative_draft_model: ai/qwen3:0.6B-Q4_K_M
      speculative_num_tokens: 16
      speculative_acceptance_rate: 0.8
```

The draft model generates token candidates, and the main model validates them.
This can significantly improve throughput for longer responses.

### Runtime flags

Pass engine-specific flags to optimize performance:

```yaml
models:
  optimized-qwen:
    provider: dmr
    model: ai/qwen3
    provider_opts:
      runtime_flags: ["--ngl=33", "--threads=8"]
```

Common flags:

- `--ngl` - Number of GPU layers
- `--threads` - CPU thread count
- `--repeat-penalty` - Repetition penalty

## Using DMR for RAG

Docker Model Runner supports both embeddings and reranking for RAG workflows.

### Embedding with DMR

Use local embeddings for indexing your knowledge base:

```yaml
rag:
  codebase:
    docs: [./src]
    strategies:
      - type: chunked-embeddings
        embedding_model: dmr/ai/embeddinggemma
        database: ./code.db
```

### Reranking with DMR

DMR provides native reranking for improved RAG results:

```yaml
models:
  reranker:
    provider: dmr
    model: hf.co/ggml-org/qwen3-reranker-0.6b-q8_0-gguf

rag:
  docs:
    docs: [./documentation]
    strategies:
      - type: chunked-embeddings
        embedding_model: dmr/ai/embeddinggemma
        limit: 20
    results:
      reranking:
        model: reranker
        threshold: 0.5
      limit: 5
```

Native DMR reranking is the fastest option for reranking RAG results.

## Troubleshooting

If cagent can't find Docker Model Runner:

1. Verify Docker Model Runner status:
  ```console
  $ docker model status
  ```
2. Check available models:
  ```console
  $ docker model list
  ```
3. Check model logs for errors:
  ```console
  $ docker model logs
  ```
4. Ensure Docker Desktop has Model Runner enabled in settings (macOS/Windows)

## What's next

- Follow the [tutorial](https://docs.docker.com/ai/cagent/tutorial/) to build your first agent with local
  models
- Learn about [RAG](https://docs.docker.com/ai/cagent/rag/) to give your agents access to codebases and
  documentation
- See the [configuration reference](https://docs.docker.com/ai/cagent/reference/config/#docker-model-runner-dmr)
  for all DMR options
