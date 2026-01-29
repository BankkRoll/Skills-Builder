# Toolsets reference and more

# Toolsets reference

> Complete reference for cagent toolsets and their capabilities

# Toolsets reference

   Table of contents

---

This reference documents the toolsets available in cagent and what each one
does. Tools give agents the ability to take action—interacting with files,
executing commands, accessing external resources, and managing state.

For configuration file syntax and how to set up toolsets in your agent YAML,
see the [Configuration file reference](https://docs.docker.com/ai/cagent/reference/config/).

## How agents use tools

When you configure toolsets for an agent, those tools become available in the
agent's context. The agent can invoke tools by name with appropriate parameters
based on the task at hand.

Tool invocation flow:

1. Agent analyzes the task and determines which tool to use
2. Agent constructs tool parameters based on requirements
3. cagent executes the tool and returns results
4. Agent processes results and decides next steps

Agents can call multiple tools in sequence or make decisions based on tool
results. Tool selection is automatic based on the agent's understanding of the
task and available capabilities.

## Tool types

cagent supports three types of toolsets:

Built-in toolsetsCore functionality built directly into cagent (`filesystem`, `shell`,
`memory`, etc.). These provide essential capabilities for file operations,
command execution, and state management.
MCP toolsetsTools provided by Model Context Protocol servers, either local processes
(stdio) or remote servers (HTTP/SSE). MCP enables access to a wide ecosystem
of standardized tools.
Custom toolsetsShell scripts wrapped as tools with typed parameters (`script_shell`). This
lets you define domain-specific tools for your use case.

## Configuration

Toolsets are configured in your agent's YAML file under the `toolsets` array:

```yaml
agents:
  my_agent:
    model: anthropic/claude-sonnet-4-5
    description: A helpful coding assistant
    toolsets:
      # Built-in toolset
      - type: filesystem

      # Built-in toolset with configuration
      - type: memory
        path: ./memories.db

      # Local MCP server (stdio)
      - type: mcp
        command: npx
        args: ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/dir"]

      # Remote MCP server (SSE)
      - type: mcp
        remote:
          url: https://mcp.example.com/sse
          transport_type: sse
          headers:
            Authorization: Bearer ${API_TOKEN}

      # Custom shell tools
      - type: script_shell
        tools:
          build:
            cmd: npm run build
            description: Build the project
```

### Common configuration options

All toolset types support these optional properties:

| Property | Type | Description |
| --- | --- | --- |
| instruction | string | Additional instructions for using the toolset |
| tools | array | Specific tool names to enable (defaults to all) |
| env | object | Environment variables for the toolset |
| toon | string | Comma-delimited regex patterns matching tool names whose JSON outputs should be compressed. Reduces token usage by simplifying/compressing JSON responses from matched tools using automatic encoding. Example:"search.*,list.*" |
| defer | boolean or array | Control which tools load into initial context. Set totrueto defer all tools, or array of tool names to defer specific tools. Deferred tools don't consume context until explicitly loaded viasearch_tool/add_tool. |

### Tool selection

By default, agents have access to all tools from their configured toolsets. You
can restrict this using the `tools` option:

```yaml
toolsets:
  - type: filesystem
    tools: [read_file, write_file, list_directory]
```

This is useful for:

- Limiting agent capabilities for security
- Reducing context size for smaller models
- Creating specialized agents with focused tool access

### Deferred loading

Deferred loading keeps tools out of the initial context window, loading them
only when explicitly requested. This is useful for large toolsets where most
tools won't be used, significantly reducing context consumption.

Defer all tools in a toolset:

```yaml
toolsets:
  - type: mcp
    command: npx
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/path"]
    defer: true # All tools load on-demand
```

Or defer specific tools while loading others immediately:

```yaml
toolsets:
  - type: mcp
    command: npx
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/path"]
    defer: [search_files, list_directory] # Only these are deferred
```

Agents can discover deferred tools via `search_tool` and load them into context
via `add_tool` when needed. Best for toolsets with dozens of tools where only a
few are typically used.

### Output compression

The `toon` property compresses JSON outputs from matched tools to reduce token
usage. When a tool's output is JSON, it's automatically compressed using
efficient encoding before being returned to the agent:

```yaml
toolsets:
  - type: mcp
    command: npx
    args: ["-y", "@modelcontextprotocol/server-github"]
    toon: "search.*,list.*" # Compress outputs from search/list tools
```

Useful for tools that return large JSON responses (API results, file listings,
search results). The compression is transparent to the agent but can
significantly reduce context consumption for verbose tool outputs.

### Per-agent tool configuration

Different agents can have different toolsets:

```yaml
agents:
  coordinator:
    model: anthropic/claude-sonnet-4-5
    sub_agents: [code_writer, code_reviewer]
    toolsets:
      - type: filesystem
        tools: [read_file]

  code_writer:
    model: openai/gpt-5-mini
    toolsets:
      - type: filesystem
      - type: shell

  code_reviewer:
    model: anthropic/claude-sonnet-4-5
    toolsets:
      - type: filesystem
        tools: [read_file, read_multiple_files]
```

This allows specialized agents with focused capabilities, security boundaries,
and optimized performance.

## Built-in tools reference

### Filesystem

The `filesystem` toolset gives your agent the ability to work with
files and directories. Your agent can read files to understand
context, write new files, make targeted edits to existing files,
search for content, and explore directory structures. Essential for
code analysis, documentation updates, configuration management, and
any agent that needs to understand or modify project files.

Access is restricted to the current working directory by default. Agents can
request access to additional directories at runtime, which requires your
approval.

#### Configuration

```yaml
toolsets:
  - type: filesystem

  # Optional: restrict to specific tools
  - type: filesystem
    tools: [read_file, write_file, edit_file]
```

### Shell

The `shell` toolset lets your agent execute commands in your system's shell
environment. Use this for agents that need to run builds, execute tests, manage
processes, interact with CLI tools, or perform system operations. The agent can
run commands in the foreground or background.

Commands execute in the current working directory and inherit environment
variables from the cagent process. This toolset is powerful but should be used
with appropriate security considerations.

#### Configuration

```yaml
toolsets:
  - type: shell
```

### Think

The `think` toolset provides your agent with a reasoning scratchpad. The agent
can record thoughts and reasoning steps without taking actions or modifying
data. Particularly useful for complex tasks where the agent needs to plan
multiple steps, verify requirements, or maintain context across a long
conversation.

Agents use this to break down problems, list applicable rules, verify they have
all needed information, and document their reasoning process before acting.

#### Configuration

```yaml
toolsets:
  - type: think
```

### Todo

The `todo` toolset gives your agent task-tracking capabilities for managing
multi-step operations. Your agent can break down complex work into discrete
tasks, track progress through each step, and ensure nothing is missed before
completing a request. Especially valuable for agents handling complex
workflows with multiple dependencies.

The `shared` option allows todos to persist across different agents in a
multi-agent system, enabling coordination.

#### Configuration

```yaml
toolsets:
  - type: todo

  # Optional: share todos across agents
  - type: todo
    shared: true
```

### Memory

The `memory` toolset allows your agent to store and retrieve information across
conversations and sessions. Your agent can remember user preferences, project
context, previous decisions, and other information that should persist. Useful
for agents that interact with users over time or need to maintain state about
a project or environment.

Memories are stored in a local database file and persist across cagent
sessions.

#### Configuration

```yaml
toolsets:
  - type: memory

  # Optional: specify database location
  - type: memory
    path: ./agent-memories.db
```

### Fetch

The `fetch` toolset enables your agent to retrieve content from HTTP/HTTPS URLs.
Your agent can fetch documentation, API responses, web pages, or any content
accessible via HTTP GET requests. Useful for agents that need to access
external resources, check API documentation, or retrieve web content.

The agent can specify custom HTTP headers when needed for authentication or
other purposes.

#### Configuration

```yaml
toolsets:
  - type: fetch
```

### API

The `api` toolset lets you define custom tools that call HTTP APIs. Similar to
`script_shell` but for web services, this allows you to expose REST APIs,
webhooks, or any HTTP endpoint as a tool your agent can use. The agent sees
these as typed tools with automatic parameter validation.

Use this to integrate with external services, call internal APIs, trigger
webhooks, or interact with any HTTP-based system.

#### Configuration

Each API tool is defined with an `api_config` containing the endpoint, HTTP method, and optional typed parameters:

```yaml
toolsets:
  - type: api
    api_config:
      name: search_docs
      endpoint: https://api.example.com/search
      method: GET
      instruction: Search the documentation database
      headers:
        Authorization: Bearer ${API_TOKEN}
      args:
        query:
          type: string
          description: Search query
        limit:
          type: number
          description: Maximum results
      required: [query]

  - type: api
    api_config:
      name: create_ticket
      endpoint: https://api.example.com/tickets
      method: POST
      instruction: Create a support ticket
      args:
        title:
          type: string
          description: Ticket title
        description:
          type: string
          description: Ticket description
      required: [title, description]
```

For GET requests, parameters are interpolated into the endpoint URL. For POST
requests, parameters are sent as JSON in the request body.

Supported argument types: `string`, `number`, `boolean`, `array`, `object`.

### Script Shell

The `script_shell` toolset lets you define custom tools by wrapping shell
commands with typed parameters. This allows you to expose domain-specific
operations to your agent as first-class tools. The agent sees these custom
tools just like built-in tools, with parameter validation and type checking
handled automatically.

Use this to create tools for deployment scripts, build commands, test runners,
or any operation specific to your project or workflow.

#### Configuration

Each custom tool is defined with a command, description, and optional typed
parameters:

```yaml
toolsets:
  - type: script_shell
    tools:
      deploy:
        cmd: ./deploy.sh
        description: Deploy the application to an environment
        args:
          environment:
            type: string
            description: Target environment (dev, staging, prod)
          version:
            type: string
            description: Version to deploy
        required: [environment]

      run_tests:
        cmd: npm test
        description: Run the test suite
        args:
          filter:
            type: string
            description: Test name filter pattern
```

Supported argument types: `string`, `number`, `boolean`, `array`, `object`.

#### Tools

The tools you define become available to your agent. In the previous example,
the agent would have access to `deploy` and `run_tests` tools.

## Automatic tools

Some tools are automatically added to agents based on their configuration. You
don't configure these explicitly—they appear when needed.

### transfer_task

Automatically available when your agent has `sub_agents` configured. Allows
the agent to delegate tasks to sub-agents and receive results back.

### handoff

Automatically available when your agent has `handoffs` configured. Allows the
agent to transfer the entire conversation to a different agent.

## What's next

- Read the [Configuration file reference](https://docs.docker.com/ai/cagent/reference/config/) for YAML file structure
- Review the [CLI reference](https://docs.docker.com/ai/cagent/reference/cli/) for running agents
- Explore
  [MCP servers](https://docs.docker.com/ai/mcp-catalog-and-toolkit/mcp-gateway/) for extended capabilities
- Browse [example configurations](https://github.com/docker/cagent/tree/main/examples)

---

# Sharing agents

> Distribute agent configurations through OCI registries

# Sharing agents

   Table of contents

---

Push your agent to a registry and share it by name. Your teammates
reference `agentcatalog/security-expert` instead of copying YAML files
around or asking you where your agent configuration lives.

When you update the agent in the registry, everyone gets the new version
the next time they pull or restart their client.

## Prerequisites

To push agents to a registry, authenticate first:

```console
$ docker login
```

For other registries, use their authentication method.

## Publishing agents

Push your agent configuration to a registry:

```console
$ cagent push ./agent.yml myusername/agent-name
```

Push creates the repository if it doesn't exist yet. Use Docker Hub or
any OCI-compatible registry.

Tag specific versions:

```console
$ cagent push ./agent.yml myusername/agent-name:v1.0.0
$ cagent push ./agent.yml myusername/agent-name:latest
```

## Using published agents

Pull an agent to inspect it locally:

```console
$ cagent pull agentcatalog/pirate
```

This saves the configuration as a local YAML file.

Run agents directly from the registry:

```console
$ cagent run agentcatalog/pirate
```

Or reference it directly in integrations:

### Editor integration (ACP)

Use registry references in ACP configurations so your editor always uses
the latest version:

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

### MCP client integration

Agents can be exposed as tools in MCP clients:

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

## What's next

- Set up [ACP integration](https://docs.docker.com/ai/cagent/integrations/acp/) with shared agents
- Configure [MCP integration](https://docs.docker.com/ai/cagent/integrations/mcp/) with shared agents
- Browse the [agent catalog](https://hub.docker.com/u/agentcatalog) for examples

---

# Building a coding agent

> Create a coding agent that can read, write, and validate code changes in your projects

# Building a coding agent

   Table of contents

---

This tutorial teaches you how to build a coding agent that can help with
software development tasks. You'll start with a basic agent and progressively
add capabilities until you have a production-ready assistant that can read code,
make changes, run tests, and even look up documentation.

By the end, you'll understand how to structure agent instructions, configure
tools, and compose multiple agents for complex workflows.

## What you'll build

A coding agent that can:

- Read and modify files in your project
- Run commands like tests and linters
- Follow a structured development workflow
- Look up documentation when needed
- Track progress through multi-step tasks

## What you'll learn

- How to configure cagent agents in YAML
- How to give agents access to tools (filesystem, shell, etc.)
- How to write effective agent instructions
- How to compose multiple agents for specialized tasks
- How to adapt agents for your own projects

## Prerequisites

Before starting, you need:

- **cagent installed** - See the [installation guide](https://docs.docker.com/ai/cagent/#installation)
- **API key configured** - Set `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` in your
  environment. Get keys from [Anthropic](https://console.anthropic.com/) or
  [OpenAI](https://platform.openai.com/api-keys)
- **A project to work with** - Any codebase where you want agent assistance

## Creating your first agent

A cagent agent is defined in a YAML configuration file. The minimal agent needs
just a model and instructions that define its purpose.

Create a file named `agents.yml`:

```yaml
agents:
  root:
    model: openai/gpt-5
    description: A basic coding assistant
    instruction: |
      You are a helpful coding assistant.
      Help me write and understand code.
```

Run your agent:

```console
$ cagent run agents.yml
```

Try asking it: "How do I read a file in Python?"

The agent can answer coding questions, but it can't see your files or run
commands yet. To make it useful for real development work, it needs access to
tools.

## Adding tools

A coding agent needs to interact with your project files and run commands. You
enable these capabilities by adding toolsets.

Update `agents.yml` to add filesystem and shell access:

```yaml
agents:
  root:
    model: openai/gpt-5
    description: A coding assistant with filesystem access
    instruction: |
      You are a helpful coding assistant.
      You can read and write files to help me develop software.
      Always check if code works before finishing a task.
    toolsets:
      - type: filesystem
      - type: shell
```

Run the updated agent and try: "Read the README.md file and summarize it."

Your agent can now:

- Read and write files in the current directory
- Execute shell commands
- Explore your project structure

> Note
>
> directory. The agent will request permission if it needs to access other
> directories.

The agent can now interact with your code, but its behavior is still generic.
Next, you'll teach it how to work effectively.

## Structuring agent instructions

Generic instructions produce generic results. For production use, you want your
agent to follow a specific workflow and understand your project's conventions.

Update your agent with structured instructions. This example shows a Go
development agent, but you can adapt the pattern for any language:

```yaml
agents:
  root:
    model: anthropic/claude-sonnet-4-5
    description: Expert Go developer
    instruction: |
      Your goal is to help with code-related tasks by examining, modifying,
      and validating code changes.

      TASK
          # Workflow:
          # 1. Analyze: Understand requirements and identify relevant code.
          # 2. Examine: Search for files, analyze structure and dependencies.
          # 3. Modify: Make changes following best practices.
          # 4. Validate: Run linters/tests. If issues found, return to Modify.
      </TASK>

      Constraints:
      - Be thorough in examination before making changes
      - Always validate changes before considering the task complete
      - Write code to files, don't show it in chat

      ## Development Workflow
      - `go build ./...` - Build the application
      - `go test ./...` - Run tests
      - `golangci-lint run` - Check code quality

    add_date: true
    add_environment_info: true
    toolsets:
      - type: filesystem
      - type: shell
      - type: todo
```

Try asking: "Add error handling to the `parseConfig` function in main.go"

The structured instructions give your agent:

- A clear workflow to follow (analyze, examine, modify, validate)
- Project-specific commands to run
- Constraints that prevent common mistakes
- Context about the environment (`add_date` and `add_environment_info`)

The `todo` toolset helps the agent track progress through multi-step tasks. When
you ask for complex changes, the agent will break down the work and update its
progress as it goes.

## Composing multiple agents

Complex tasks often benefit from specialized agents. You can add sub-agents that
handle specific responsibilities, like researching documentation while your main
agent stays focused on coding.

Add a librarian agent that can search for documentation:

```yaml
agents:
  root:
    model: anthropic/claude-sonnet-4-5
    description: Expert Go developer
    instruction: |
      Your goal is to help with code-related tasks by examining, modifying,
      and validating code changes.

      When you need to look up documentation or research how something works,
      ask the librarian agent.

      (rest of instructions from previous section...)
    toolsets:
      - type: filesystem
      - type: shell
      - type: todo
    sub_agents:
      - librarian

  librarian:
    model: anthropic/claude-haiku-4-5
    description: Documentation researcher
    instruction: |
      You are the librarian. Your job is to find relevant documentation,
      articles, or resources to help the developer agent.

      Search the internet and fetch web pages as needed.
    toolsets:
      - type: mcp
        ref: docker:duckduckgo
      - type: fetch
```

Try asking: "How do I use `context.Context` in Go? Then add it to my server
code."

Your main agent will delegate the research to the librarian, then use that
information to modify your code. This keeps the main agent's context focused on
the coding task while still having access to up-to-date documentation.

Using a smaller, faster model (Haiku) for the librarian saves costs since
documentation lookup doesn't need the same reasoning depth as code changes.

## Adapting for your project

Now that you understand the core concepts, adapt the agent for your specific
project:

### Update the development commands

Replace the Go commands with your project's workflow:

```yaml
## Development Workflow
- `npm test` - Run tests
- `npm run lint` - Check code quality
- `npm run build` - Build the application
```

### Add project-specific constraints

If your agent keeps making the same mistakes, add explicit constraints:

```yaml
Constraints:
  - Always run tests before considering a task complete
  - Follow the existing code style in src/ directories
  - Never modify files in the generated/ directory
  - Use TypeScript strict mode for new files
```

### Choose the right models

For coding tasks, use reasoning-focused models:

- `anthropic/claude-sonnet-4-5` - Strong reasoning, good for complex code
- `openai/gpt-5` - Fast, good general coding ability

For auxiliary tasks like documentation lookup, smaller models work well:

- `anthropic/claude-haiku-4-5` - Fast and cost-effective
- `openai/gpt-5-mini` - Good for simple tasks

### Iterate based on usage

The best way to improve your agent is to use it. When you notice issues:

1. Add specific instructions to prevent the problem
2. Update constraints to guide behavior
3. Add relevant commands to the development workflow
4. Consider adding specialized sub-agents for complex areas

## What you learned

You now know how to:

- Create a basic cagent configuration
- Add tools to enable agent capabilities
- Write structured instructions for consistent behavior
- Compose multiple agents for specialized tasks
- Adapt agents for different programming languages and workflows

## Next steps

- Learn [best practices](https://docs.docker.com/ai/cagent/best-practices/) for handling large outputs,
  structuring agent teams, and optimizing performance
- Integrate cagent with your [editor](https://docs.docker.com/ai/cagent/integrations/acp/) or use agents as
  [tools in MCP clients](https://docs.docker.com/ai/cagent/integrations/mcp/)
- Review the [Configuration reference](https://docs.docker.com/ai/cagent/reference/config/) for all available
  options
- Explore the [Tools reference](https://docs.docker.com/ai/cagent/reference/toolsets/) to see what capabilities
  you can enable
- Check out [example
  configurations](https://github.com/docker/cagent/tree/main/examples) for
  different use cases
- See the full
  [golang_developer.yaml](https://github.com/docker/cagent/blob/main/golang_developer.yaml)
  that the Docker team uses to develop cagent

---

# cagent

> cagent lets you build, orchestrate, and share AI agents that work together as a team.

# cagent

   Table of contents

---

Availability: Experimental

[cagent](https://github.com/docker/cagent) is an open source tool for building
teams of specialized AI agents. Instead of prompting one generalist model, you
define agents with specific roles and instructions that collaborate to solve
problems. Run these agent teams from your terminal using any LLM provider.

## Why agent teams

One agent handling complex work means constant context-switching. Split the work
across focused agents instead - each handles what it's best at. cagent manages
the coordination.

Here's a two-agent team that debugs problems:

```yaml
agents:
  root:
    model: openai/gpt-5-mini # Change to the model that you want to use
    description: Bug investigator
    instruction: |
      Analyze error messages, stack traces, and code to find bug root causes.
      Explain what's wrong and why it's happening.
      Delegate fix implementation to the fixer agent.
    sub_agents: [fixer]
    toolsets:
      - type: filesystem
      - type: mcp
        ref: docker:duckduckgo

  fixer:
    model: anthropic/claude-sonnet-4-5 # Change to the model that you want to use
    description: Fix implementer
    instruction: |
      Write fixes for bugs diagnosed by the investigator.
      Make minimal, targeted changes and add tests to prevent regression.
    toolsets:
      - type: filesystem
      - type: shell
```

The root agent investigates and explains the problem. When it understands the
issue, it hands off to `fixer` for implementation. Each agent stays focused on
its specialty.

## Installation

cagent is included in Docker Desktop 4.49 and later.

For Docker Engine users or custom installations:

- **Homebrew**: `brew install cagent`
- **Winget**: `winget install Docker.Cagent`
- **Pre-built binaries**: [GitHub
  releases](https://github.com/docker/cagent/releases)
- **From source**: See the [cagent
  repository](https://github.com/docker/cagent?tab=readme-ov-file#build-from-source)

## Get started

Try the bug analyzer team:

1. Set your API key for the model provider you want to use:
  ```console
  $ export ANTHROPIC_API_KEY=<your_key>  # For Claude models
  $ export OPENAI_API_KEY=<your_key>     # For OpenAI models
  $ export GOOGLE_API_KEY=<your_key>     # For Gemini models
  ```
2. Save the [example configuration](#why-agent-teams) as `debugger.yaml`.
3. Run your agent team:
  ```console
  $ cagent run debugger.yaml
  ```

You'll see a prompt where you can describe bugs or paste error messages. The
investigator analyzes the problem, then hands off to the fixer for
implementation.

## How it works

You interact with the *root agent*, which can delegate work to sub-agents you
define. Each agent:

- Uses its own model and parameters
- Has its own context (agents don't share knowledge)
- Can access built-in tools like todo lists, memory, and task delegation
- Can use external tools via
  [MCP
  servers](https://docs.docker.com/ai/mcp-catalog-and-toolkit/mcp-gateway/)

The root agent delegates tasks to agents listed under `sub_agents`. Sub-agents
can have their own sub-agents for deeper hierarchies.

## Configuration options

Agent configurations are YAML files. A basic structure looks like this:

```yaml
agents:
  root:
    model: claude-sonnet-4-0
    description: Brief role summary
    instruction: |
      Detailed instructions for this agent...
    sub_agents: [helper]

  helper:
    model: gpt-5-mini
    description: Specialist agent role
    instruction: |
      Instructions for the helper agent...
```

You can also configure model settings (like context limits), tools (including
MCP servers), and more. See the [configuration
reference](https://docs.docker.com/ai/cagent/reference/config/)
for complete details.

## Share agent teams

Agent configurations are packaged as OCI artifacts. Push and pull them like
container images:

```console
$ cagent push ./debugger.yaml myusername/debugger
$ cagent pull myusername/debugger
```

Use Docker Hub or any OCI-compatible registry. Pushing creates the repository if
it doesn't exist yet.

## What's next

- Follow the [tutorial](https://docs.docker.com/ai/cagent/tutorial/) to build your first coding agent
- Learn [best practices](https://docs.docker.com/ai/cagent/best-practices/) for building effective agents
- Integrate cagent with your [editor](https://docs.docker.com/ai/cagent/integrations/acp/) or use agents as
  [tools in MCP clients](https://docs.docker.com/ai/cagent/integrations/mcp/)
- Browse example agent configurations in the [cagent
  repository](https://github.com/docker/cagent/tree/main/examples)
- Use `cagent new` to generate agent teams with AI
- Connect agents to external tools via the
  [Docker MCP
  Gateway](https://docs.docker.com/ai/mcp-catalog-and-toolkit/mcp-gateway/)
- Read the full [configuration
  reference](https://github.com/docker/cagent?tab=readme-ov-file#-configuration-reference)

---

# Define AI Models in Docker Compose applications

> Learn how to define and use AI models in Docker Compose applications using the models top-level element

# Define AI Models in Docker Compose applications

   Table of contents

---

Requires: Docker Compose [2.38.0](https://github.com/docker/compose/releases/tag/v2.38.0) and later

Compose lets you define AI models as core components of your application, so you can declare model dependencies alongside services and run the application on any platform that supports the Compose Specification.

## Prerequisites

- Docker Compose v2.38 or later
- A platform that supports Compose models such as Docker Model Runner (DMR) or compatible cloud providers.
  If you are using DMR, see the
  [requirements](https://docs.docker.com/ai/model-runner/#requirements).

## What are Compose models?

Compose `models` are a standardized way to define AI model dependencies in your application. By using the
[modelstop-level element](https://docs.docker.com/reference/compose-file/models/) in your Compose file, you can:

- Declare which AI models your application needs
- Specify model configurations and requirements
- Make your application portable across different platforms
- Let the platform handle model provisioning and lifecycle management

## Basic model definition

To define models in your Compose application, use the `models` top-level element:

```yaml
services:
  chat-app:
    image: my-chat-app
    models:
      - llm

models:
  llm:
    model: ai/smollm2
```

This example defines:

- A service called `chat-app` that uses a model named `llm`
- A model definition for `llm` that references the `ai/smollm2` model image

## Model configuration options

Models support various configuration options:

```yaml
models:
  llm:
    model: ai/smollm2
    context_size: 1024
    runtime_flags:
      - "--a-flag"
      - "--another-flag=42"
```

Common configuration options include:

- `model` (required): The OCI artifact identifier for the model. This is what Compose pulls and runs via the model runner.
- `context_size`: Defines the maximum token context size for the model.
  > Note
  >
  > Each model has its own maximum context size. When increasing the context length,
  > consider your hardware constraints. In general, try to keep context size
  > as small as feasible for your specific needs.
- `runtime_flags`: A list of raw command-line flags passed to the inference engine when the model is started.
  See
  [Configuration options](https://docs.docker.com/ai/model-runner/configuration/) for commonly used parameters and examples.
- Platform-specific options may also be available via extension attributes `x-*`

> Tip
>
> See more example in the [Common runtime configurations](#common-runtime-configurations) section.

## Service model binding

Services can reference models in two ways: short syntax and long syntax.

### Short syntax

The short syntax is the simplest way to bind a model to a service:

```yaml
services:
  app:
    image: my-app
    models:
      - llm
      - embedding-model

models:
  llm:
    model: ai/smollm2
  embedding-model:
    model: ai/all-minilm
```

With short syntax, the platform automatically generates environment variables based on the model name:

- `LLM_URL` - URL to access the LLM model
- `LLM_MODEL` - Model identifier for the LLM model
- `EMBEDDING_MODEL_URL` - URL to access the embedding-model
- `EMBEDDING_MODEL_MODEL` - Model identifier for the embedding-model

### Long syntax

The long syntax allows you to customize environment variable names:

```yaml
services:
  app:
    image: my-app
    models:
      llm:
        endpoint_var: AI_MODEL_URL
        model_var: AI_MODEL_NAME
      embedding-model:
        endpoint_var: EMBEDDING_URL
        model_var: EMBEDDING_NAME

models:
  llm:
    model: ai/smollm2
  embedding-model:
    model: ai/all-minilm
```

With this configuration, your service receives:

- `AI_MODEL_URL` and `AI_MODEL_NAME` for the LLM model
- `EMBEDDING_URL` and `EMBEDDING_NAME` for the embedding model

## Platform portability

One of the key benefits of using Compose models is portability across different platforms that support the Compose specification.

### Docker Model Runner

When
[Docker Model Runner is enabled](https://docs.docker.com/ai/model-runner/):

```yaml
services:
  chat-app:
    image: my-chat-app
    models:
      llm:
        endpoint_var: AI_MODEL_URL
        model_var: AI_MODEL_NAME

models:
  llm:
    model: ai/smollm2
    context_size: 4096
    runtime_flags:
      - "--no-prefill-assistant"
```

Docker Model Runner will:

- Pull and run the specified model locally
- Provide endpoint URLs for accessing the model
- Inject environment variables into the service

### Cloud providers

The same Compose file can run on cloud providers that support Compose models:

```yaml
services:
  chat-app:
    image: my-chat-app
    models:
      - llm

models:
  llm:
    model: ai/smollm2
    # Cloud-specific configurations
    x-cloud-options:
      - "cloud.instance-type=gpu-small"
      - "cloud.region=us-west-2"
```

Cloud providers might:

- Use managed AI services instead of running models locally
- Apply cloud-specific optimizations and scaling
- Provide additional monitoring and logging capabilities
- Handle model versioning and updates automatically

## Common runtime configurations

Below are some example configurations for various use cases.

### Development

```yaml
services:
  app:
    image: app
    models:
      dev_model:
        endpoint_var: DEV_URL
        model_var: DEV_MODEL

models:
  dev_model:
    model: ai/model
    context_size: 4096
    runtime_flags:
      - "--verbose"                       # Set verbosity level to infinity
      - "--verbose-prompt"                # Print a verbose prompt before generation
      - "--log-prefix"                    # Enable prefix in log messages
      - "--log-timestamps"                # Enable timestamps in log messages
      - "--log-colors"                    # Enable colored logging
```

### Conservative with disabled reasoning

```yaml
services:
  app:
    image: app
    models:
      conservative_model:
        endpoint_var: CONSERVATIVE_URL
        model_var: CONSERVATIVE_MODEL

models:
  conservative_model:
    model: ai/model
    context_size: 4096
    runtime_flags:
      - "--temp"                # Temperature
      - "0.1"
      - "--top-k"               # Top-k sampling
      - "1"
      - "--reasoning-budget"    # Disable reasoning
      - "0"
```

### Creative with high randomness

```yaml
services:
  app:
    image: app
    models:
      creative_model:
        endpoint_var: CREATIVE_URL
        model_var: CREATIVE_MODEL

models:
  creative_model:
    model: ai/model
    context_size: 4096
    runtime_flags:
      - "--temp"                # Temperature
      - "1"
      - "--top-p"               # Top-p sampling
      - "0.9"
```

### Highly deterministic

```yaml
services:
  app:
    image: app
    models:
      deterministic_model:
        endpoint_var: DET_URL
        model_var: DET_MODEL

models:
  deterministic_model:
    model: ai/model
    context_size: 4096
    runtime_flags:
      - "--temp"                # Temperature
      - "0"
      - "--top-k"               # Top-k sampling
      - "1"
```

### Concurrent processing

```yaml
services:
  app:
    image: app
    models:
      concurrent_model:
        endpoint_var: CONCURRENT_URL
        model_var: CONCURRENT_MODEL

models:
  concurrent_model:
    model: ai/model
    context_size: 2048
    runtime_flags:
      - "--threads"             # Number of threads to use during generation
      - "8"
      - "--mlock"               # Lock memory to prevent swapping
```

### Rich vocabulary model

```yaml
services:
  app:
    image: app
    models:
      rich_vocab_model:
        endpoint_var: RICH_VOCAB_URL
        model_var: RICH_VOCAB_MODEL

models:
  rich_vocab_model:
    model: ai/model
    context_size: 4096
    runtime_flags:
      - "--temp"                # Temperature
      - "0.1"
      - "--top-p"               # Top-p sampling
      - "0.9"
```

### Embeddings

When using embedding models with the `/v1/embeddings` endpoint, you must include the `--embeddings` runtime flag for the model to be properly configured.

```yaml
services:
  app:
    image: app
    models:
      embedding_model:
        endpoint_var: EMBEDDING_URL
        model_var: EMBEDDING_MODEL

models:
  embedding_model:
    model: ai/all-minilm
    context_size: 2048
    runtime_flags:
      - "--embeddings"          # Required for embedding models
```

## Alternative configuration with provider services

> Important
>
> This approach is deprecated. Use the [modelstop-level element](#basic-model-definition) instead.

You can also use the `provider` service type, which allows you to declare platform capabilities required by your application.
For AI models, you can use the `model` type to declare model dependencies.

To define a model provider:

```yaml
services:
  chat:
    image: my-chat-app
    depends_on:
      - ai_runner

  ai_runner:
    provider:
      type: model
      options:
        model: ai/smollm2
        context-size: 1024
        runtime-flags: "--no-prefill-assistant"
```

## Reference

- [modelstop-level element](https://docs.docker.com/reference/compose-file/models/)
- [modelsattribute](https://docs.docker.com/reference/compose-file/services/#models)
- [Docker Model Runner documentation](https://docs.docker.com/ai/model-runner/)
- [Configuration options](https://docs.docker.com/ai/model-runner/configuration/) - Context size and runtime parameters
- [Inference engines](https://docs.docker.com/ai/model-runner/inference-engines/) - llama.cpp and vLLM details
- [API reference](https://docs.docker.com/ai/model-runner/api-reference/) - OpenAI and Ollama-compatible APIs

---

# Built

> Use and configure Gordon's built-in tools for Docker, Kubernetes, security, and development workflows

# Built-in tools in Gordon

   Table of contents

---

Gordon includes an integrated toolbox that gives you access to system tools and
capabilities. These tools extend Gordon's functionality so you can interact with
the Docker Engine, Kubernetes, Docker Scout security scanning, and other
developer utilities. This article describes the available tools, how to
configure them, and usage patterns.

## Configure tools

Configure tools globally in the toolbox to make them available throughout
Gordon, including Docker Desktop and the CLI.

To configure tools:

1. In the **Ask Gordon** view in Docker Desktop, select the **Toolbox** button at the bottom left of the input area.
  ![Screenshot showing Gordon page with the toolbox button.](https://docs.docker.com/ai/gordon/images/gordon.png)  ![Screenshot showing Gordon page with the toolbox button.](https://docs.docker.com/ai/gordon/images/gordon.png)
2. To enable or disable a tool, select it in the left menu and select the toggle.
  ![Screenshot showing Gordon's Toolbox.](https://docs.docker.com/ai/gordon/images/toolbox.png)  ![Screenshot showing Gordon's Toolbox.](https://docs.docker.com/ai/gordon/images/toolbox.png)
  For more information about Docker tools, see [Reference](#reference).

## Usage examples

This section shows common tasks you can perform with Gordon tools.

### Manage Docker containers

#### List and monitor containers

```console
# List all running containers
$ docker ai "Show me all running containers"

# List containers using specific resources
$ docker ai "List all containers using more than 1GB of memory"

# View logs from a specific container
$ docker ai "Show me logs from my running api-container from the last hour"
```

#### Manage container lifecycle

```console
# Run a new container
$ docker ai "Run a nginx container with port 80 exposed to localhost"

# Stop a specific container
$ docker ai "Stop my database container"

# Clean up unused containers
$ docker ai "Remove all stopped containers"
```

### Work with Docker images

```console
# List available images
$ docker ai "Show me all my local Docker images"

# Pull a specific image
$ docker ai "Pull the latest Ubuntu image"

# Build an image from a Dockerfile
$ docker ai "Build an image from my current directory and tag it as myapp:latest"

# Clean up unused images
$ docker ai "Remove all my unused images"
```

### Manage Docker volumes

```console
# List volumes
$ docker ai "List all my Docker volumes"

# Create a new volume
$ docker ai "Create a new volume called postgres-data"

# Back up data from a container to a volume
$ docker ai "Create a backup of my postgres container data to a new volume"
```

### Perform Kubernetes operations

```console
# Create a deployment
$ docker ai "Create an nginx deployment and make sure it's exposed locally"

# List resources
$ docker ai "Show me all deployments in the default namespace"

# Get logs
$ docker ai "Show me logs from the auth-service pod"
```

### Run security analysis

```console
# Scan for CVEs
$ docker ai "Scan my application for security vulnerabilities"

# Get security recommendations
$ docker ai "Give me recommendations for improving the security of my nodejs-app image"
```

### Use development workflows

```console
# Analyze and commit changes
$ docker ai "Look at my local changes, create multiple commits with sensible commit messages"

# Review branch status
$ docker ai "Show me the status of my current branch compared to main"
```

## Reference

This section lists the built-in tools in Gordon's toolbox.

### Docker tools

Interact with Docker containers, images, and volumes.

#### Container management

| Name | Description |
| --- | --- |
| docker | Access the Docker CLI |
| list_builds | List builds in the Docker daemon |
| build_logs | Show build logs |

#### Volume management

| Tool | Description |
| --- | --- |
| list_volumes | List all Docker volumes |
| remove_volume | Remove a Docker volume |
| create_volume | Create a new Docker volume |

#### Image management

| Tool | Description |
| --- | --- |
| list_images | List all Docker images |
| remove_images | Remove Docker images |
| pull_image | Pull an image from a registry |
| push_image | Push an image to a registry |
| build_image | Build a Docker image |
| tag_image | Tag a Docker image |
| inspect | Inspect a Docker object |

### Kubernetes tools

Interact with your Kubernetes cluster.

#### Pod management

| Tool | Description |
| --- | --- |
| list_pods | List all pods in the cluster |
| get_pod_logs | Get logs from a specific pod |

#### Deployment management

| Tool | Description |
| --- | --- |
| list_deployments | List all deployments |
| create_deployment | Create a new deployment |
| expose_deployment | Expose a deployment as a service |
| remove_deployment | Remove a deployment |

#### Service management

| Tool | Description |
| --- | --- |
| list_services | List all services |
| remove_service | Remove a service |

#### Cluster information

| Tool | Description |
| --- | --- |
| list_namespaces | List all namespaces |
| list_nodes | List all nodes in the cluster |

### Docker Scout tools

Security analysis powered by Docker Scout.

| Tool | Description |
| --- | --- |
| search_for_cves | Analyze a Docker image, project directory, or other artifacts for vulnerabilities using Docker Scout CVEs. |
| get_security_recommendations | Analyze a Docker image, project directory, or other artifacts for base image update recommendations using Docker Scout. |

### Developer tools

General-purpose development utilities.

| Tool | Description |
| --- | --- |
| fetch | Retrieve content from a URL |
| get_command_help | Get help for CLI commands |
| run_command | Execute shell commands |
| filesystem | Perform filesystem operations |
| git | Execute git commands |

### AI model tools

| Tool | Description |
| --- | --- |
| list_models | List all available Docker models |
| pull_model | Download a Docker model |
| run_model | Query a model with a prompt |
| remove_model | Remove a Docker model |

### Docker MCP Catalog

If you have enabled the [MCP Toolkit feature](https://docs.docker.com/ai/mcp-catalog-and-toolkit/),
all the tools you have enabled and configured are available for Gordon to use.
