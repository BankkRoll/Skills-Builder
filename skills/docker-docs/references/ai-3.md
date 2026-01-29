# Configuration file reference and more

# Configuration file reference

> Complete reference for the cagent YAML configuration file format

# Configuration file reference

   Table of contents

---

This reference documents the YAML configuration file format for cagent agents.
It covers file structure, agent parameters, model configuration, toolset setup,
and RAG sources.

For detailed documentation of each toolset's capabilities and specific options,
see the [Toolsets reference](https://docs.docker.com/ai/cagent/reference/toolsets/).

## File structure

A configuration file has four top-level sections:

```yaml
agents: # Required - agent definitions
  root:
    model: anthropic/claude-sonnet-4-5
    description: What this agent does
    instruction: How it should behave

models: # Optional - model configurations
  custom_model:
    provider: openai
    model: gpt-5

rag: # Optional - RAG sources
  docs:
    docs: [./documents]
    strategies: [...]

metadata: # Optional - author, license, readme
  author: Your Name
```

## Agents

| Property | Type | Description | Required |
| --- | --- | --- | --- |
| model | string | Model reference or name | Yes |
| description | string | Brief description of agent's purpose | No |
| instruction | string | Detailed behavior instructions | Yes |
| sub_agents | array | Agent names for task delegation | No |
| handoffs | array | Agent names for conversation handoff | No |
| toolsets | array | Available tools | No |
| welcome_message | string | Message displayed on start | No |
| add_date | boolean | Include current date in context | No |
| add_environment_info | boolean | Include working directory, OS, Git info | No |
| add_prompt_files | array | Prompt file paths to include | No |
| max_iterations | integer | Maximum tool call loops (unlimited if not set) | No |
| num_history_items | integer | Conversation history limit | No |
| code_mode_tools | boolean | Enable Code Mode for tools | No |
| commands | object | Named prompts accessible via/command_name | No |
| structured_output | object | JSON schema for structured responses | No |
| rag | array | RAG source names | No |

### Task delegation versus conversation handoff

Agents support two different delegation mechanisms. Choose based on whether you
need task results or conversation control.

#### Sub_agents: Hierarchical task delegation

Use `sub_agents` for hierarchical task delegation. The parent agent assigns a
specific task to a child agent using the `transfer_task` tool. The child
executes in its own context and returns results. The parent maintains control
and can delegate to multiple agents in sequence.

This works well for structured workflows where you need to combine results from
specialists, or when tasks have clear boundaries. Each delegated task runs
independently and reports back to the parent.

**Example:**

```yaml
agents:
  root:
    sub_agents: [researcher, analyst]
    instruction: |
      Delegate research to researcher.
      Delegate analysis to analyst.
      Combine results and present findings.
```

Root calls: `transfer_task(agent="researcher", task="Find pricing data")`. The
researcher completes the task and returns results to root.

#### Handoffs: Conversation transfer

Use `handoffs` to transfer conversation control to a different agent. When an
agent uses the `handoff` tool, the new agent takes over completely. The
original agent steps back until someone hands back to it.

This works well when different agents should own different parts of an ongoing
conversation, or when specialists need to collaborate as peers without a
coordinator managing every step.

**Example:**

```yaml
agents:
  generalist:
    handoffs: [database_expert, security_expert]
    instruction: |
      Help with general development questions.
      If the conversation moves to database optimization,
      hand off to database_expert.
      If security concerns arise, hand off to security_expert.

  database_expert:
    handoffs: [generalist, security_expert]
    instruction: Handle database design and optimization.

  security_expert:
    handoffs: [generalist, database_expert]
    instruction: Review code for security vulnerabilities.
```

When the user asks about query performance, generalist executes:
`handoff(agent="database_expert")`. The database expert now owns the
conversation and can continue working with the user directly, or hand off to
security_expert if the discussion shifts to SQL injection concerns.

### Commands

Named prompts users invoke with `/command_name`. Supports JavaScript template
literals with `${env.VARIABLE}` for environment variables:

```yaml
commands:
  greet: "Say hello to ${env.USER}"
  analyze: "Analyze ${env.PROJECT_NAME || 'demo'}"
```

Run with: `cagent run config.yaml /greet`

### Structured output

Constrain responses to a JSON schema (OpenAI and Gemini only):

```yaml
structured_output:
  name: code_analysis
  strict: true
  schema:
    type: object
    properties:
      issues:
        type: array
        items: { ... }
    required: [issues]
```

## Models

| Property | Type | Description | Required |
| --- | --- | --- | --- |
| provider | string | openai,anthropic,google,dmr | Yes |
| model | string | Model name | Yes |
| temperature | float | Randomness (0.0-2.0) | No |
| max_tokens | integer | Maximum response length | No |
| top_p | float | Nucleus sampling (0.0-1.0) | No |
| frequency_penalty | float | Repetition penalty (-2.0 to 2.0, OpenAI only) | No |
| presence_penalty | float | Topic penalty (-2.0 to 2.0, OpenAI only) | No |
| base_url | string | Custom API endpoint | No |
| parallel_tool_calls | boolean | Enable parallel tool execution (default: true) | No |
| token_key | string | Authentication token key | No |
| track_usage | boolean | Track token usage | No |
| thinking_budget | mixed | Reasoning effort (provider-specific) | No |
| provider_opts | object | Provider-specific options | No |

### Alloy models

Use multiple models in rotation by separating names with commas:

```yaml
model: anthropic/claude-sonnet-4-5,openai/gpt-5
```

### Thinking budget

Controls reasoning depth. Configuration varies by provider:

- **OpenAI**: String values - `minimal`, `low`, `medium`, `high`
- **Anthropic**: Integer token budget (1024-32768, must be less than
  `max_tokens`)
  - Set `provider_opts.interleaved_thinking: true` for tool use during reasoning
- **Gemini**: Integer token budget (0 to disable, -1 for dynamic, max 24576)
  - Gemini 2.5 Pro: 128-32768, cannot disable (minimum 128)

```yaml
# OpenAI
thinking_budget: low

# Anthropic
thinking_budget: 8192
provider_opts:
  interleaved_thinking: true

# Gemini
thinking_budget: 8192    # Fixed
thinking_budget: -1      # Dynamic
thinking_budget: 0       # Disabled
```

### Docker Model Runner (DMR)

Run local models. If `base_url` is omitted, cagent auto-discovers via Docker
Model plugin.

```yaml
provider: dmr
model: ai/qwen3
max_tokens: 8192
base_url: http://localhost:12434/engines/llama.cpp/v1 # Optional
```

Pass llama.cpp options via `provider_opts.runtime_flags` (array, string, or
multiline):

```yaml
provider_opts:
  runtime_flags: ["--ngl=33", "--threads=8"]
  # or: runtime_flags: "--ngl=33 --threads=8"
```

Model config fields auto-map to runtime flags:

- `temperature` → `--temp`
- `top_p` → `--top-p`
- `max_tokens` → `--context-size`

Explicit `runtime_flags` override auto-mapped flags.

Speculative decoding for faster inference:

```yaml
provider_opts:
  speculative_draft_model: ai/qwen3:0.6B-F16
  speculative_num_tokens: 16
  speculative_acceptance_rate: 0.8
```

## Tools

Configure tools in the `toolsets` array. Three types: built-in, MCP
(local/remote), and Docker Gateway.

> Note
>
> documentation of each toolset's capabilities, available tools, and specific
> configuration options, see the [Toolsets reference](https://docs.docker.com/ai/cagent/reference/toolsets/).

All toolsets support common properties like `tools` (whitelist), `defer`
(deferred loading), `toon` (output compression), `env` (environment variables),
and `instruction` (usage guidance). See the [Toolsets reference](https://docs.docker.com/ai/cagent/reference/toolsets/)
for details on these properties and what each toolset does.

### Built-in tools

```yaml
toolsets:
  - type: filesystem
  - type: shell
  - type: think
  - type: todo
    shared: true
  - type: memory
    path: ./memory.db
```

### MCP tools

Local process:

```yaml
- type: mcp
  command: npx
  args:
    ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/files"]
  tools: ["read_file", "write_file"] # Optional: limit to specific tools
  env:
    NODE_OPTIONS: "--max-old-space-size=8192"
```

Remote server:

```yaml
- type: mcp
  remote:
    url: https://mcp-server.example.com
    transport_type: sse
    headers:
      Authorization: Bearer token
```

### Docker MCP Gateway

Containerized tools from
[Docker MCP
Catalog](https://docs.docker.com/ai/mcp-catalog-and-toolkit/mcp-gateway/):

```yaml
- type: mcp
  ref: docker:duckduckgo
```

## RAG

Retrieval-augmented generation for document knowledge bases. Define sources at
the top level, reference in agents.

```yaml
rag:
  docs:
    docs: [./documents, ./README.md]
    strategies:
      - type: chunked-embeddings
        embedding_model: openai/text-embedding-3-small
        vector_dimensions: 1536
        database: ./embeddings.db

agents:
  root:
    rag: [docs]
```

### Retrieval strategies

All strategies support chunking configuration. Chunk size and overlap are
measured in characters (Unicode code points), not tokens.

#### Chunked-embeddings

Direct semantic search using vector embeddings. Best for understanding intent,
synonyms, and paraphrasing.

| Field | Type | Default |
| --- | --- | --- |
| embedding_model | string | - |
| database | string | - |
| vector_dimensions | integer | - |
| similarity_metric | string | cosine |
| threshold | float | 0.5 |
| limit | integer | 5 |
| chunking.size | integer | 1000 |
| chunking.overlap | integer | 75 |
| chunking.respect_word_boundaries | boolean | true |
| chunking.code_aware | boolean | false |

```yaml
- type: chunked-embeddings
  embedding_model: openai/text-embedding-3-small
  vector_dimensions: 1536
  database: ./vector.db
  similarity_metric: cosine_similarity
  threshold: 0.5
  limit: 10
  chunking:
    size: 1000
    overlap: 100
```

#### Semantic-embeddings

LLM-enhanced semantic search. Uses a language model to generate rich semantic
summaries of each chunk before embedding, capturing deeper meaning.

| Field | Type | Default |
| --- | --- | --- |
| embedding_model | string | - |
| chat_model | string | - |
| database | string | - |
| vector_dimensions | integer | - |
| similarity_metric | string | cosine |
| threshold | float | 0.5 |
| limit | integer | 5 |
| ast_context | boolean | false |
| semantic_prompt | string | - |
| chunking.size | integer | 1000 |
| chunking.overlap | integer | 75 |
| chunking.respect_word_boundaries | boolean | true |
| chunking.code_aware | boolean | false |

```yaml
- type: semantic-embeddings
  embedding_model: openai/text-embedding-3-small
  vector_dimensions: 1536
  chat_model: openai/gpt-5-mini
  database: ./semantic.db
  threshold: 0.3
  limit: 10
  chunking:
    size: 1000
    overlap: 100
```

#### BM25

Keyword-based search using BM25 algorithm. Best for exact terms, technical
jargon, and code identifiers.

| Field | Type | Default |
| --- | --- | --- |
| database | string | - |
| k1 | float | 1.5 |
| b | float | 0.75 |
| threshold | float | 0.0 |
| limit | integer | 5 |
| chunking.size | integer | 1000 |
| chunking.overlap | integer | 75 |
| chunking.respect_word_boundaries | boolean | true |
| chunking.code_aware | boolean | false |

```yaml
- type: bm25
  database: ./bm25.db
  k1: 1.5
  b: 0.75
  threshold: 0.3
  limit: 10
  chunking:
    size: 1000
    overlap: 100
```

### Hybrid retrieval

Combine multiple strategies with fusion:

```yaml
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
    strategy: rrf # Options: rrf, weighted, max
    k: 60 # RRF smoothing parameter
  deduplicate: true
  limit: 5
```

Fusion strategies:

- `rrf`: Reciprocal Rank Fusion (recommended, rank-based, no normalization
  needed)
- `weighted`: Weighted combination (`fusion.weights: {chunked-embeddings: 0.7, bm25: 0.3}`)
- `max`: Maximum score across strategies

### Reranking

Re-score results with a specialized model for improved relevance:

```yaml
results:
  reranking:
    model: openai/gpt-5-mini
    top_k: 10 # Only rerank top K (0 = all)
    threshold: 0.3 # Minimum score after reranking
    criteria: | # Optional domain-specific guidance
      Prioritize official docs over blog posts
  limit: 5
```

DMR native reranking:

```yaml
models:
  reranker:
    provider: dmr
    model: hf.co/ggml-org/qwen3-reranker-0.6b-q8_0-gguf

results:
  reranking:
    model: reranker
```

### Code-aware chunking

For source code, use AST-based chunking. With semantic-embeddings, you can
include AST metadata in the LLM prompts:

```yaml
- type: semantic-embeddings
  embedding_model: openai/text-embedding-3-small
  vector_dimensions: 1536
  chat_model: openai/gpt-5-mini
  database: ./code.db
  ast_context: true # Include AST metadata in semantic prompts
  chunking:
    size: 2000
    code_aware: true # Enable AST-based chunking
```

### RAG properties

Top-level RAG source:

| Field | Type | Description |
| --- | --- | --- |
| docs | []string | Document paths (suppports glob patterns, respects.gitignore) |
| tool | object | Customize RAG tool name/description/instruction |
| strategies | []object | Retrieval strategies (see above for strategy-specific fields) |
| results | object | Post-processing (fusion, reranking, limits) |

Results:

| Field | Type | Default |
| --- | --- | --- |
| limit | integer | 15 |
| deduplicate | boolean | true |
| include_score | boolean | false |
| fusion.strategy | string | - |
| fusion.k | integer | 60 |
| fusion.weights | object | - |
| reranking.model | string | - |
| reranking.top_k | integer | 0 |
| reranking.threshold | float | 0.5 |
| reranking.criteria | string | "" |
| return_full_content | boolean | false |

## Metadata

Documentation and sharing information:

| Property | Type | Description |
| --- | --- | --- |
| author | string | Author name |
| license | string | License (e.g., MIT, Apache-2.0) |
| readme | string | Usage documentation |

```yaml
metadata:
  author: Your Name
  license: MIT
  readme: |
    Description and usage instructions
```

## Example configuration

Complete configuration demonstrating key features:

```yaml
agents:
  root:
    model: claude
    description: Technical lead
    instruction: Coordinate development tasks and delegate to specialists
    sub_agents: [developer, reviewer]
    toolsets:
      - type: filesystem
      - type: mcp
        ref: docker:duckduckgo
    rag: [readmes]
    commands:
      status: "Check project status"

  developer:
    model: gpt
    description: Software developer
    instruction: Write clean, maintainable code
    toolsets:
      - type: filesystem
      - type: shell

  reviewer:
    model: claude
    description: Code reviewer
    instruction: Review for quality and security
    toolsets:
      - type: filesystem

models:
  gpt:
    provider: openai
    model: gpt-5

  claude:
    provider: anthropic
    model: claude-sonnet-4-5
    max_tokens: 64000

rag:
  readmes:
    docs: ["**/README.md"]
    strategies:
      - type: chunked-embeddings
        embedding_model: openai/text-embedding-3-small
        vector_dimensions: 1536
        database: ./embeddings.db
        limit: 10
      - type: bm25
        database: ./bm25.db
        limit: 10
    results:
      fusion:
        strategy: rrf
        k: 60
      limit: 5
```

## What's next

- Read the [Toolsets reference](https://docs.docker.com/ai/cagent/reference/toolsets/) for detailed toolset
  documentation
- Review the [CLI reference](https://docs.docker.com/ai/cagent/reference/cli/) for command-line options
- Browse [example
  configurations](https://github.com/docker/cagent/tree/main/examples)
- Learn about [sharing agents](https://docs.docker.com/ai/cagent/sharing-agents/)

---

# Examples

> Get inspiration from agent examples

# Examples

   Table of contents

---

Get inspiration from the following agent examples.
See more examples in the [cagent GitHub repository](https://github.com/docker/cagent/tree/main/examples).

## Development team

```yaml
#!/usr/bin/env cagent run

models:
  model:
    provider: anthropic
    model: claude-sonnet-4-0
    max_tokens: 64000

agents:
  root:
    model: model
    description: Product Manager - Leads the development team and coordinates iterations
    instruction: |
      You are the Product Manager leading a development team consisting of a designer, frontend engineer, full stack engineer, and QA tester.

      Your responsibilities:
      - Break down user requirements into small, manageable iterations
      - Each iteration should deliver one complete feature end-to-end
      - Ensure each iteration is small enough to be completed quickly but substantial enough to provide value
      - Coordinate between team members to ensure smooth workflow
      - Define clear acceptance criteria for each feature
      - Prioritize features based on user value and technical dependencies

      IMPORTANT ITERATION PRINCIPLES:
      - Start with the most basic, core functionality first
      - Each iteration must result in working, testable code
      - Features should be incrementally built upon previous iterations
      - Don't try to build everything at once - focus on one feature at a time
      - Ensure proper handoffs between designer → frontend → fullstack → QA

      Workflow for each iteration:
      1. Define the feature and acceptance criteria
      2. Have designer create UI mockups/wireframes
      3. Have frontend engineer implement the UI
      4. Have fullstack engineer build backend and integrate
      5. Have QA test the complete feature and report issues
      6. Address any issues before moving to next iteration

      Always start by understanding what the user wants to build, then break it down into logical, small iterations.

      Always make sure to ask the right agent to do the right task using the appropriate toolset. don't try to do everything yourself.

      Always read and write all decisions and important information to a .md file called dev-team.md in the .dev-team directory.
      Make sure to append to the file and edit what is not needed anymore. Consult this file to understand the current state of the project and the team.
      This file might include references to other files that should all be placed inside the .dev-team folder. Don't write anything but code outside of this directory.

    sub_agents: [designer, awesome_engineer]
    toolsets:
      - type: filesystem
      - type: think
      - type: todo
      - type: memory
        path: dev_memory.db
      - type: mcp
        ref: docker:context7

  designer:
    model: model
    description: UI/UX Designer - Creates user interface designs and wireframes
    instruction: |
      You are a UI/UX Designer working on a development team. Your role is to create user-friendly, intuitive designs for each feature iteration.

      Your responsibilities:
      - Create wireframes and mockups for each feature
      - Design responsive layouts that work on different screen sizes
      - Ensure consistent design patterns across the application
      - Consider user experience and accessibility
      - Provide detailed design specifications for the frontend engineer
      - Use modern design principles and best practices

      For each feature you design:
      1. Create a clear wireframe showing layout and components
      2. Specify colors, fonts, spacing, and styling details
      3. Define user interactions and hover states
      4. Consider mobile responsiveness
      5. Provide clear handoff documentation for the frontend engineer

      Keep designs simple and focused on the specific feature being built in the current iteration.
      Build upon previous designs to maintain consistency across the application.

      Always read and write all decisions and important information to a .md file called dev-team.md in the .dev-team directory.
      Make sure to append to the file and edit what is not needed anymore. Consult this file to understand the current state of the project and the team.
      This file might include references to other files that should all be placed inside the .dev-team folder. Don't write anything but code outside of this directory.
    toolsets:
      - type: filesystem
      - type: think
      - type: memory
        path: dev_memory.db
      - type: mcp
        ref: docker:context7

  awesome_engineer:
    model: model
    description: Awesome Engineer - Implements user interfaces based on designs
    instruction: |
      You are an Awesome Engineer responsible for implementing user interfaces based on the designer's specifications.

      Your responsibilities:
      - Convert design mockups into responsive, interactive web interfaces
      - Write clean, maintainable HTML, CSS, and JavaScript
      - Ensure cross-browser compatibility and mobile responsiveness
      - Implement proper accessibility features
      - Create reusable components and maintain code consistency
      - Integrate with backend APIs provided by the fullstack engineer

      Technical guidelines:
      - Use modern frontend frameworks/libraries (React, Vue, or vanilla JS as appropriate)
      - Write semantic HTML with proper structure
      - Use CSS best practices (flexbox, grid, responsive design)
      - Implement proper error handling for API calls
      - Follow accessibility guidelines (WCAG)
      - Write clean, commented code that's easy to maintain

      For each iteration:
      1. Review the design specifications carefully
      2. Break down the UI into logical components
      3. Implement the interface with proper styling
      4. Test the UI functionality before handoff
      5. Document any deviations from the design and rationale

      Focus on creating a working, polished UI for the specific feature in the current iteration.

      You are also a Full Stack Engineer responsible for building backend systems, APIs, and integrating them with the frontend.

      Your responsibilities:
      - Design and implement backend APIs and services
      - Set up databases and data models
      - Handle authentication, authorization, and security
      - Integrate frontend with backend systems
      - Ensure proper error handling and logging
      - Write tests for backend functionality
      - Deploy and maintain the application infrastructure

      Technical guidelines:
      - Choose appropriate technology stack based on requirements
      - Design RESTful APIs with proper HTTP methods and status codes
      - Implement proper data validation and sanitization
      - Use appropriate database design patterns
      - Follow security best practices
      - Write comprehensive error handling
      - Include proper logging and monitoring
      - Write unit and integration tests

      For each iteration:
      1. Design the backend architecture for the feature
      2. Implement necessary APIs and database changes
      3. Test backend functionality thoroughly
      4. Integrate with the frontend implementation
      5. Ensure end-to-end functionality works correctly
      6. Document API endpoints and usage

      Focus on building robust, scalable backend systems that support the current iteration's feature.
      Ensure seamless integration with the frontend implementation.

      Always read and write all decisions and important information to a .md file called dev-team.md in the .dev-team directory.
      Make sure to append to the file and edit what is not needed anymore. Consult this file to understand the current state of the project and the team.
      This file might include references to other files that should all be placed inside the .dev-team folder. Don't write anything but code outside of this directory.
    toolsets:
      - type: filesystem
      - type: shell
      - type: think
      - type: memory
        path: dev_memory.db
      - type: mcp
        ref: docker:context7
```

## Go developer

```yaml
#!/usr/bin/env cagent run

models:
  claude:
    provider: anthropic
    model: claude-opus-4-5
  haiku:
    provider: anthropic
    model: claude-haiku-4-5

agents:
  root:
    model: claude
    description: Expert Golang Developer specialized in implementing features and improving code quality.
    instruction: |
      **Goal:**
      Help with Go code-related tasks by examining, modifying, and validating code changes.

      TASK
          **Workflow:**
          1. **Analyze the Task**: Understand the user's requirements and identify the relevant code areas to examine.

          2. **Code Examination**:
          - Search for relevant code files and functions
          - Analyze code structure and dependencies
          - Identify potential areas for modification

          3. **Code Modification**:
          - Make necessary code changes
          - Ensure changes follow best practices
          - Maintain code style consistency

          4. **Validation Loop**:
          - Run linters and tests to check code quality
          - Verify changes meet requirements
          - If issues found, return to step 3
          - Continue until all requirements are met

          5. **Summary**:
          - Very concisely summarize the changes made (not in a file)
          - For trivial tasks, answer the question without extra information
      </TASK>

      **Details:**
       - Be thorough in code examination before making changes
       - Always validate changes before considering the task complete
       - Follow Go best practices
       - Maintain or improve code quality
       - Be proactive in identifying potential issues
       - Only ask for clarification if necessary, try your best to use all the tools to get the info you need

       **Tools:**
        - When needed and possible, call multiple tools concurrently. It's faster and cheaper.

    add_date: true
    add_environment_info: true
    add_prompt_files:
      - AGENTS.md
    sub_agents:
      - librarian
    toolsets:
      - type: filesystem
      - type: shell
      - type: todo
      - type: mcp
        command: gopls
        args: ["mcp"]
    commands:
      fix-lint:
        description: "Fix the lint issues"
        instruction: |
          Fix the lint issues (if any).

          Here the result of the linting command:
          $ task lint
          ${shell({cmd: "task lint"})}

          $go_diagnostics
          ${go_diagnostics()}

          $go_vulncheck
          ${go_vulncheck()}
      remove-comments-tests: "Remove useless comments in test files (*_test.go)"
      commit:
        description: "Commit local changes"
        instruction: |
            Based on the below changes: create a single commit with an appropriate message.

            - Current git status: !shell(cmd="git status")
            - Current git diff (staged and unstaged changes): !shell(cmd="git diff HEAD")
            - Current branch: !shell(cmd="git branch --show-current")
      simplify: "Look at the local changes and try to simplify the code and architecture but don't remove any feature. I just want the code to be easier to read and maintain."
      init: |
        Create an AGENTS.md file for this project by inspecting the codebase. The AGENTS.md should help AI coding agents understand how to work with this project effectively.

        Analyze the project structure and include:
        1. **Development Commands**: Build, test, lint, and run commands (check Makefile, Taskfile, package.json, Cargo.toml, etc.)
        2. **Architecture Overview**: Key packages/modules, their responsibilities, and how they interact
        3. **Code Style and Conventions**: Patterns used, error handling approaches, naming conventions
        4. **Testing Guidelines**: How to run tests, test patterns used, any special testing setup
        5. **Configuration**: Important config files and environment variables
        6. **Common Development Patterns**: Frequently used patterns specific to this codebase
        7. **Key Files Reference**: Quick reference table of important files and their purposes

        Focus on information that would help an AI agent navigate and modify the codebase correctly. Be concise but comprehensive.
      security-review: |
        Perform a security review of the local changes in this Git repository.

        **Workflow:**
        1. **Identify Changes**: Run `git diff` to see uncommitted changes, and `git diff HEAD~1` or `git log --oneline -5` to understand recent commits if needed.

        2. **Security Analysis**: Review the changes for common security issues:
           - **Input Validation**: Check for missing or inadequate input validation
           - **SQL Injection**: Look for raw SQL queries or improper use of query builders
           - **Command Injection**: Identify unsafe use of exec, shell commands, or system calls
           - **Path Traversal**: Check for unsafe file path handling
           - **Sensitive Data Exposure**: Look for hardcoded secrets, API keys, or credentials
           - **Authentication/Authorization**: Review any auth-related changes
           - **Error Handling**: Check for information leakage in error messages
           - **Dependency Security**: Note any new dependencies that should be vetted
           - **Race Conditions**: Identify potential concurrency issues in Go code
           - **Unsafe Pointer Usage**: Check for unsafe package usage

        3. **Go-Specific Checks**:
           - Run `go_vulncheck` to check for known vulnerabilities
           - Review use of `unsafe` package
           - Check for proper context cancellation and timeout handling
           - Verify proper error wrapping and handling

        4. **Report**: Provide a structured security review with:
           - **Summary**: Overall security posture of the changes
           - **Findings**: List of identified issues with severity (Critical/High/Medium/Low/Info)
           - **Recommendations**: Specific suggestions to improve security
           - **Tips**: General security best practices relevant to the changes

  planner:
    model: claude
    instruction: |
      You are a planning agent responsible for gathering user requirements and creating a development plan.
      Always ask clarifying questions to ensure you fully understand the user's needs before creating the plan.
      Once you have a clear understanding, analyze the existing code and create a detailed development plan in a markdown file. Do not write any code yourself.
      Once the plan is created, you will delegate tasks to the root agent. Make sure to provide the file name of the plan when delegating. Write the plan in the current directory.
    toolsets:
      - type: filesystem
    sub_agents:
      - root

  reviewer:
    model: google/gemini-3-pro-preview
    instruction: |
      Give me feedback about the local changes. Don't be too picky, think about code quality, security, duplication, idiomatic Go,
      performance, maintainability, and best practices.
      Provide suggestions for improvements and point out any potential issues.
      Don't be too verbose, keep your review concise and to the point.
    add_prompt_files:
      - AGENTS.md
    sub_agents:
      - librarian
    toolsets:
      - type: filesystem
      - type: shell
      - type: mcp
        command: gopls
        args: ["mcp"]

  librarian:
    model: haiku
    description: Documentation librarian. Can search the Web and look for relevant documentation to help the golang developer agent.
    instruction: |
      You are the librarian, your job is to look for relevant documentation to help the golang developer agent.
      When given a query, search the internet for relevant documentation, articles, or resources that can assist in completing the task.
      Use context7 for searching documentation and brave for general web searches.
    toolsets:
      - type: mcp
        ref: docker:context7
      - type: mcp
        ref: docker:brave
      - type: fetch

permissions:
  allow:
    - go_diagnostics
    - go_file_context
    - go_package_api
    - go_symbol_references
    - go_vulncheck
    - go_workspace
    - shell:cmd=gh --version
    - shell:cmd=gh pr view *
    - shell:cmd=gh pr diff *
    - shell:cmd=git remote -v
    - shell:cmd=ls *
    - shell:cmd=cat *
    - shell:cmd=head *
    - shell:cmd=tail *
    - shell:cmd=wc *
    - shell:cmd=find *
    - shell:cmd=grep *
    - shell:cmd=pwd
    - shell:cmd=echo *
    - shell:cmd=which *
    - shell:cmd=type *
    - shell:cmd=file *
    - shell:cmd=stat *
    - shell:cmd=git status*
    - shell:cmd=git log*
    - shell:cmd=git diff*
    - shell:cmd=git show*
    - shell:cmd=git branch*
    - shell:cmd=git remote -v*
    - shell:cmd=git commit *
    - shell:cmd=go test*
    - shell:cmd=go build*
```

## Technical blog writer

```yaml
#!/usr/bin/env cagent run

agents:
  root:
    model: anthropic
    description: Writes technical blog posts
    instruction: |
      You are the leader of a team of AI agents for a technical blog writing workflow.

      Here are the members in your team:
      <team_members>
      - web_search_agent: Searches the web
      - writer: Writes a 750-word technical blog post based on the chosen prompt
      </team_members>

      WORKFLOW
        1. Call the `web_search_agent` agent to search for the web to get important information about the task that is asked

        3. Call the `writer` agent to write a 750-word technical blog post based on the research done by the web_search_agent
      </WORKFLOW>

      - Use the transfer_to_agent tool to call the right agent at the right time to complete the workflow.
      - DO NOT transfer to multiple members at once
      - ONLY CALL ONE AGENT AT A TIME
      - When using the `transfer_to_agent` tool, make exactly one call and wait for the result before making another. Do not batch or parallelize tool calls.
    sub_agents:
      - web_search_agent
      - writer
    toolsets:
      - type: think

  web_search_agent:
    model: anthropic
    add_date: true
    description: Search the web for the information
    instruction: |
      Search the web for the information

      Always include sources
    toolsets:
      - type: mcp
        ref: docker:duckduckgo

  writer:
    model: anthropic
    description: Writes a 750-word technical blog post based on the chosen prompt.
    instruction: |
      You are an agent that receives a single technical writing prompt and generates a detailed, informative, and well-structured technical blog post.

      - Ensure the content is technically accurate and includes relevant code examples, diagrams, or technical explanations where appropriate.
      - Structure the blog post with clear sections, including an introduction, main content, and conclusion.
      - Use technical terminology appropriately and explain complex concepts clearly.
      - Include practical examples and real-world applications where relevant.
      - Make sure the content is engaging for a technical audience while maintaining professional standards.

      Constraints:
      - DO NOT use lists

models:
  anthropic:
    provider: anthropic
    model: claude-3-7-sonnet-latest
```
