# Configure MCP servers with YAML and more

# Configure MCP servers with YAML

> Use MCP servers with Gordon

# Configure MCP servers with YAML

   Table of contents

---

Docker works with Anthropic to provide container images for the
[reference implementations](https://github.com/modelcontextprotocol/servers/)
of MCP servers. These are available on Docker Hub under
[the mcp namespace](https://hub.docker.com/u/mcp).

When you run the `docker ai` command in your terminal, Gordon checks for a
`gordon-mcp.yml` file in your working directory. If present, this file lists
the MCP servers Gordon should use in that context. The `gordon-mcp.yml` file
is a Docker Compose file that configures MCP servers as Compose services for
Gordon to access.

The following minimal example shows how to use the
[mcp-time server](https://hub.docker.com/r/mcp/time) to provide temporal
capabilities to Gordon. For more details, see the
[source code and documentation](https://github.com/modelcontextprotocol/servers/tree/main/src/time).

Create a `gordon-mcp.yml` file in your working directory and add the time
server:

```yaml
services:
  time:
    image: mcp/time
```

With this file present, you can now ask Gordon to tell you the time in another
timezone:

```bash
$ docker ai 'what time is it now in kiribati?'

    • Calling get_current_time

  The current time in Kiribati (Tarawa) is 9:38 PM on January 7, 2025.
```

Gordon finds the MCP time server and calls its tool when needed.

## Use advanced MCP server features

Some MCP servers need access to your filesystem or system environment variables.
Docker Compose helps with this. Because `gordon-mcp.yml` is a Compose file, you
can add bind mounts using standard Docker Compose syntax. This makes your
filesystem resources available to the container:

```yaml
services:
  fs:
    image: mcp/filesystem
    command:
      - /rootfs
    volumes:
      - .:/rootfs
```

The `gordon-mcp.yml` file adds filesystem access capabilities to Gordon. Because
everything runs inside a container, Gordon only has access to the directories
you specify.

Gordon can use any number of MCP servers. For example, to give Gordon internet
access with the `mcp/fetch` server:

```yaml
services:
  fetch:
    image: mcp/fetch
  fs:
    image: mcp/filesystem
    command:
      - /rootfs
    volumes:
      - .:/rootfs
```

You can now ask Gordon to fetch content and write it to a file:

```bash
$ docker ai can you fetch rumpl.dev and write the summary to a file test.txt

    • Calling fetch ✔️
    • Calling write_file ✔️

  The summary of the website rumpl.dev has been successfully written to the
  file test.txt in the allowed directory. Let me know if you need further
  assistance!

$ cat test.txt
The website rumpl.dev features a variety of blog posts and articles authored
by the site owner. Here's a summary of the content:

1. **Wasmio 2023 (March 25, 2023)**: A recap of the WasmIO 2023 conference
   held in Barcelona. The author shares their experience as a speaker and
   praises the organizers for a successful event.

2. **Writing a Window Manager in Rust - Part 2 (January 3, 2023)**: The
   second part of a series on creating a window manager in Rust. This
   installment focuses on enhancing the functionality to manage windows
   effectively.

3. **2022 in Review (December 29, 2022)**: A personal and professional recap
   of the year 2022. The author reflects on the highs and lows of the year,
   emphasizing professional achievements.

4. **Writing a Window Manager in Rust - Part 1 (December 28, 2022)**: The
   first part of the series on building a window manager in Rust. The author
   discusses setting up a Linux machine and the challenges of working with
   X11 and Rust.

5. **Add docker/docker to your dependencies (May 10, 2020)**: A guide for Go
   developers on how to use the Docker client library in their projects. The
   post includes a code snippet demonstrating the integration.

6. **First (October 11, 2019)**: The inaugural post on the blog, featuring a
   simple "Hello World" program in Go.
```

## What’s next?

Now that you know how to use MCP servers with Gordon, try these next steps:

- Experiment: Try integrating one or more of the tested MCP servers into your
  `gordon-mcp.yml` file and explore their capabilities.
- Explore the ecosystem. See the [reference implementations on
  GitHub](https://github.com/modelcontextprotocol/servers/) or browse the
  [Docker Hub MCP namespace](https://hub.docker.com/u/mcp) for more servers
  that might suit your needs.
- Build your own. If none of the existing servers meet your needs, or you want
  to learn more, develop a custom MCP server. Use the
  [MCP specification](https://www.anthropic.com/news/model-context-protocol)
  as a guide.
- Share your feedback. If you discover new servers that work well with Gordon
  or encounter issues, [share your findings to help improve the
  ecosystem](https://docker.qualtrics.com/jfe/form/SV_9tT3kdgXfAa6cWa).

With MCP support, Gordon gives you powerful extensibility and flexibility for
your use cases, whether you need temporal awareness, file management, or
internet access.

---

# Model Context Protocol (MCP)

> Learn how to use Model Context Protocol (MCP) servers with Gordon to extend AI capabilities in Docker Desktop.

# Model Context Protocol (MCP)

---

[Model Context Protocol](https://modelcontextprotocol.io/introduction) (MCP) is
an open protocol that standardizes how applications provide context and
additional functionality to large language models. MCP functions as a
client-server protocol, where the client, for example an application like
Gordon, sends requests, and the server processes those requests to deliver the
necessary context to the AI. This context may be gathered by the MCP server by
executing code to perform an action and retrieving the result, calling external
APIs, or other similar operations.

Gordon, along with other MCP clients like Claude Desktop or Cursor, can interact
with MCP servers running as containers.

[Built-in toolsUse the built-in tools.](https://docs.docker.com/ai/gordon/mcp/built-in-tools)[MCP configurationConfigure MCP tools on a per-project basis.](https://docs.docker.com/ai/gordon/mcp/yaml)

---

# Ask Gordon

> Streamline your workflow with Docker's AI-powered assistant in Docker Desktop and CLI.

# Ask Gordon

   Table of contents

---

Availability: Beta
Requires: Docker Desktop
[4.38.0](https://docs.docker.com/desktop/release-notes/#4380) or later

Ask Gordon is your personal AI assistant embedded in Docker Desktop and the
Docker CLI. It's designed to streamline your workflow and help you make the most
of the Docker ecosystem.

## Key features

Ask Gordon provides AI-powered assistance in Docker tools. It can:

- Improve Dockerfiles
- Run and troubleshoot containers
- Interact with your images and code
- Find vulnerabilities or configuration issues
- Migrate a Dockerfile to use
  [Docker Hardened Images](https://docs.docker.com/dhi/)

It understands your local environment, including source code, Dockerfiles, and
images, to provide personalized and actionable guidance.

Ask Gordon remembers conversations, allowing you to switch topics more easily.

Ask Gordon is not enabled by default, and is not
production-ready. You may also encounter the term "Docker AI" as a broader
reference to this technology.

> Note
>
> Ask Gordon is powered by Large Language Models (LLMs). Like all
> LLM-based tools, its responses may sometimes be inaccurate. Always verify the
> information provided.

### What data does Gordon access?

When you use Ask Gordon, the data it accesses depends on your query:

- Local files: If you use the `docker ai` command, Ask Gordon can access files
  and directories in the current working directory where the command is
  executed. In Docker Desktop, if you ask about a specific file or directory in
  the **Ask Gordon** view, you'll be prompted to select the relevant context.
- Local images: Gordon integrates with Docker Desktop and can view all images in
  your local image store. This includes images you've built or pulled from a
  registry.

To provide accurate responses, Ask Gordon may send relevant files, directories,
or image metadata to the Gordon backend with your query. This data transfer
occurs over the network but is never stored persistently or shared with third
parties. It is used only to process your request and formulate a response. For
details about privacy terms and conditions for Docker AI, review [Gordon's
Supplemental Terms](https://www.docker.com/legal/docker-ai-supplemental-terms/).

All data transferred is encrypted in transit.

### How your data is collected and used

Docker collects anonymized data from your interactions with Ask Gordon to
improve the service. This includes:

- Your queries: Questions you ask Gordon.
- Responses: Answers provided by Gordon.
- Feedback: Thumbs-up and thumbs-down ratings.

To ensure privacy and security:

- Data is anonymized and cannot be traced back to you or your account.
- Docker does not use this data to train AI models or share it with third
  parties.

By using Ask Gordon, you help improve Docker AI's reliability and accuracy for
everyone.

If you have concerns about data collection or usage, you can
[disable](#disable-ask-gordon) the feature at any time.

## Enable Ask Gordon

1. Sign in to your Docker account.
2. Go to the **Beta features** tab in settings.
3. Check the **Enable Docker AI** checkbox.
  The Docker AI terms of service agreement appears. You must agree to the terms
  before you can enable the feature. Review the terms and select **Accept and
  enable** to continue.
4. Select **Apply**.

> Important
>
> For Docker Desktop versions 4.41 and earlier, this setting is under the
> **Experimental features** tab on the **Features in development** page.

## Using Ask Gordon

You can access Gordon:

- In Docker Desktop, in the **Ask Gordon** view.
- In the Docker CLI, with the `docker ai` command.

After you enable Docker AI features, you will also see **Ask Gordon** in other
places in Docker Desktop. Whenever you see a button with the **Sparkles** (✨)
icon, you can use it to get contextual support from Ask Gordon.

## Example workflows

Ask Gordon is a general-purpose AI assistant for Docker tasks and workflows. Here
are some things you can try:

- [Troubleshoot a crashed container](#troubleshoot-a-crashed-container)
- [Get help with running a container](#get-help-with-running-a-container)
- [Improve a Dockerfile](#improve-a-dockerfile)
- [Migrate a Dockerfile to DHI](#migrate-a-dockerfile-to-dhi)

For more examples, try asking Gordon directly. For example:

```console
$ docker ai "What can you do?"
```

### Troubleshoot a crashed container

If you start a container with an invalid configuration or command, use Ask Gordon
to troubleshoot the error. For example, try starting a Postgres container without
a database password:

```console
$ docker run postgres
Error: Database is uninitialized and superuser password is not specified.
       You must specify POSTGRES_PASSWORD to a non-empty value for the
       superuser. For example, "-e POSTGRES_PASSWORD=password" on "docker run".

       You may also use "POSTGRES_HOST_AUTH_METHOD=trust" to allow all
       connections without a password. This is *not* recommended.

       See PostgreSQL documentation about "trust":
       https://www.postgresql.org/docs/current/auth-trust.html
```

In the **Containers** view in Docker Desktop, select the ✨ icon next to the
container's name, or inspect the container and open the **Ask Gordon** tab.

### Get help with running a container

If you want to run a specific image but are not sure how, Gordon can help you get
set up:

1. Pull an image from Docker Hub (for example, `postgres`).
2. Open the **Images** view in Docker Desktop and select the image.
3. Select the **Run** button.

In the **Run a new container** dialog, you see a message about **Ask Gordon**.

![Screenshot showing Ask Gordon hint in Docker Desktop.](https://docs.docker.com/images/gordon-run-ctr.png)  ![Screenshot showing Ask Gordon hint in Docker Desktop.](https://docs.docker.com/images/gordon-run-ctr.png)

The linked text in the hint is a suggested prompt to start a conversation with
Ask Gordon.

### Improve a Dockerfile

Gordon can analyze your Dockerfile and suggest improvements. To have Gordon
evaluate your Dockerfile using the `docker ai` command:

1. Go to your project directory:
  ```console
  $ cd <path-to-your-project>
  ```
2. Use the `docker ai` command to rate your Dockerfile:
  ```console
  $ docker ai rate my Dockerfile
  ```

Gordon will analyze your Dockerfile and identify opportunities for improvement
across several dimensions:

- Build cache optimization
- Security
- Image size efficiency
- Best practices compliance
- Maintainability
- Reproducibility
- Portability
- Resource efficiency

### Migrate a Dockerfile to DHI

Migrating your Dockerfile to use
[Docker Hardened Images](https://docs.docker.com/dhi/)
helps you build more secure, minimal, and production-ready containers. DHIs
reduce vulnerabilities, enforce best practices, and simplify compliance, making
them a strong foundation for secure software supply chains.

To request Gordon's help for the migration:

1. Ensure Gordon is
  [enabled](https://docs.docker.com/ai/gordon/#enable-ask-gordon).
2. In Gordon's Toolbox, ensure Gordon's
  [Developer MCP Toolkit is enabled](https://docs.docker.com/ai/gordon/mcp/built-in-tools/#configuration).
3. In the terminal, navigate to the directory containing your Dockerfile.
4. Start a conversation with Gordon:
  ```bash
  docker ai
  ```
5. Type:
  ```console
  "Migrate my dockerfile to DHI"
  ```
6. Follow the conversation with Gordon. Gordon will edit your Dockerfile, so when
  it requests access to the filesystem and more, type `yes` to allow Gordon to proceed.
  > Note
  >
  > To learn more about Gordon's data retention and the data it
  > can access, see
  > [Gordon](https://docs.docker.com/ai/gordon/#what-data-does-gordon-access).

When the migration is complete, you see a success message:

```text
The migration to Docker Hardened Images (DHI) is complete. The updated Dockerfile
successfully builds the image, and no vulnerabilities were detected in the final image.
The functionality and optimizations of the original Dockerfile have been preserved.
```

> Important
>
> As with any AI tool, you must verify Gordon's edits and test your image.

## Disable Ask Gordon

### For individual users

If you've enabled Ask Gordon and you want to disable it again:

1. Open the **Settings** view in Docker Desktop.
2. Go to **Beta features**.
3. Clear the **Enable Docker AI** checkbox.
4. Select **Apply**.

### For organizations

To disable Ask Gordon for your entire Docker organization, use
[Settings
Management](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/)
and add this property to your `admin-settings.json` file:

```json
{
  "enableDockerAI": {
    "value": false,
    "locked": true
  }
}
```

Or disable all Beta features by setting `allowBetaFeatures` to false:

```json
{
  "allowBetaFeatures": {
    "value": false,
    "locked": true
  }
}
```

## Feedback

We value your input on Ask Gordon and encourage you to share your experience.
Your feedback helps us improve and refine Ask Gordon for all users. If you
encounter issues, have suggestions, or simply want to share what you like,
here's how you can get in touch:

- Thumbs-up and thumbs-down buttons
  Rate Ask Gordon's responses using the thumbs-up or thumbs-down buttons in the
  response.
- Feedback survey
  You can access the Ask Gordon survey by following the *Give feedback* link in
  the **Ask Gordon** view in Docker Desktop, or from the CLI by running the
  `docker ai feedback` command.

---

# Docker MCP Catalog

> Learn about the benefits of the MCP Catalog, how you can use it, and how you can contribute

# Docker MCP Catalog

   Table of contents

---

Availability: Beta

The [Docker MCP Catalog](https://hub.docker.com/mcp) is a centralized, trusted
registry for discovering, sharing, and running MCP-compatible tools. Integrated
with Docker Hub, it offers verified, versioned, and curated MCP servers
packaged as Docker images. The catalog is also available in Docker Desktop.

The catalog solves common MCP server challenges:

- Environment conflicts. Tools often need specific runtimes that might clash
  with existing setups.
- Lack of isolation. Traditional setups risk exposing the host system.
- Setup complexity. Manual installation and configuration slow adoption.
- Inconsistency across platforms. Tools might behave unpredictably on different
  operating systems.

With Docker, each MCP server runs as a self-contained container. This makes it
portable, isolated, and consistent. You can launch tools instantly using the
Docker CLI or Docker Desktop, without worrying about dependencies or
compatibility.

## Key features

- Extensive collection of verified MCP servers in one place.
- Publisher verification and versioned releases.
- Pull-based distribution using Docker infrastructure.
- Tools provided by partners such as New Relic, Stripe, Grafana, and more.

> Note
>
> E2B sandboxes now include direct access to the Docker MCP Catalog, giving developers
> access to over 200 tools and services to seamlessly build and run AI agents. For
> more information, see [E2B Sandboxes](https://docs.docker.com/ai/sandboxes/).

## How it works

Each tool in the MCP Catalog is packaged as a Docker image with metadata.

- Discover tools on Docker Hub under the `mcp/` namespace.
- Connect tools to your preferred agents with simple configuration through the
  [MCP Toolkit](https://docs.docker.com/ai/mcp-catalog-and-toolkit/toolkit/).
- Pull and run tools using Docker Desktop or the CLI.

Each catalog entry displays:

- Tool description and metadata.
- Version history.
- List of tools provided by the MCP server.
- Example configuration for agent integration.

## Server deployment types

The Docker MCP Catalog supports both local and remote server deployments, each optimized for different use cases and requirements.

### Local MCP servers

Local MCP servers are containerized applications that run directly on your machine. All local servers are built and digitally signed by Docker, providing enhanced security through verified provenance and integrity. These servers run as containers on your local environment and function without internet connectivity once downloaded. Local servers display a Docker icon
![docker whale icon](https://docs.docker.com/desktop/images/whale-x.svg)
to indicate they are built by Docker.

Local servers offer predictable performance, complete data privacy, and independence from external service availability. They work well for development workflows, sensitive data processing, and scenarios requiring offline functionality.

### Remote MCP servers

Remote MCP servers are hosted services that run on the provider's
infrastructure and connect to external services like GitHub, Notion, and
Linear. Many remote servers use OAuth authentication. When a remote server
requires OAuth, the MCP Toolkit handles authentication automatically - you
authorize access through your browser, and the Toolkit manages credentials
securely. You don't need to manually create API tokens or configure
authentication.

Remote servers display a cloud icon in the catalog. For setup instructions, see
[MCP Toolkit](https://docs.docker.com/ai/mcp-catalog-and-toolkit/toolkit/#oauth-authentication).

## Use an MCP server from the catalog

To use an MCP server from the catalog, see [MCP Toolkit](https://docs.docker.com/ai/mcp-catalog-and-toolkit/toolkit/).

## Contribute an MCP server to the catalog

The MCP server registry is available at
[https://github.com/docker/mcp-registry](https://github.com/docker/mcp-registry). To submit an MCP server, follow the
[contributing guidelines](https://github.com/docker/mcp-registry/blob/main/CONTRIBUTING.md).

When your pull request is reviewed and approved, your MCP server is available
within 24 hours on:

- Docker Desktop's [MCP Toolkit feature](https://docs.docker.com/ai/mcp-catalog-and-toolkit/toolkit/).
- The [Docker MCP Catalog](https://hub.docker.com/mcp).
- The [Docker Hub](https://hub.docker.com/u/mcp) `mcp` namespace (for MCP
  servers built by Docker).

---

# Dynamic MCP

> Discover and add MCP servers on-demand using natural language with Dynamic MCP servers

# Dynamic MCP

   Table of contents

---

Dynamic MCP enables AI agents to discover and add MCP servers on-demand during
a conversation, without manual configuration. Instead of pre-configuring every
MCP server before starting your agent session, clients can search the
[MCP Catalog](https://docs.docker.com/ai/mcp-catalog-and-toolkit/catalog/) and add servers
as needed.

This capability is enabled automatically when you connect an MCP client to the
[MCP Toolkit](https://docs.docker.com/ai/mcp-catalog-and-toolkit/toolkit/). The gateway
provides a set of primordial tools that agents use to discover and manage
servers during runtime.

**Experimental**

Dynamic MCP is an experimental feature in early development. While you're
welcome to try it out and explore its capabilities, you may encounter
unexpected behavior or limitations. Feedback is welcome via at [GitHub
issues](https://github.com/docker/mcp-gateway/issues) for bug reports and
[GitHub discussions](https://github.com/docker/mcp-gateway/discussions) for
general questions and feature requests.

## How it works

When you connect a client to the MCP Gateway, the gateway exposes a small set
of management tools alongside any MCP servers you've already enabled. These
management tools let agents interact with the gateway's configuration:

| Tool | Description |
| --- | --- |
| mcp-find | Search for MCP servers in the catalog by name or description |
| mcp-add | Add a new MCP server to the current session |
| mcp-config-set | Configure settings for an MCP server |
| mcp-remove | Remove an MCP server from the session |
| mcp-exec | Execute a tool by name that exists in the current session |
| code-mode | Create a JavaScript-enabled tool that combines multiple MCP server tools |

With these tools available, an agent can search the catalog, add servers,
handle authentication, and use newly added tools directly without requiring a
restart or manual configuration.

Dynamically added servers and tools are associated with your *current session
only*. When you start a new session, previously added servers are not
automatically included.

## Prerequisites

To use Dynamic MCP, you need:

- Docker Desktop version 4.50 or later, with
  [MCP Toolkit](https://docs.docker.com/ai/mcp-catalog-and-toolkit/toolkit/) enabled
- An LLM application that supports MCP (such as Claude Desktop, Visual Studio Code, or Claude Code)
- Your client configured to connect to the MCP Gateway

See
[Get started with Docker MCP Toolkit](https://docs.docker.com/ai/mcp-catalog-and-toolkit/get-started/)
for setup instructions.

## Usage

Dynamic MCP is enabled automatically when you use the MCP Toolkit. Your
connected clients can now use `mcp-find`, `mcp-add`, and other management tools
during conversations.

To see Dynamic MCP in action, connect your AI client to the Docker MCP Toolkit
and try this prompt:

```plaintext
What MCP servers can I use for working with SQL databases?
```

Given this prompt, your agent will use the `mcp-find` tool provided by MCP
Toolkit to search for SQL-related servers in the [MCP Catalog](https://docs.docker.com/ai/mcp-catalog-and-toolkit/catalog/).

And to add a server to a session, simply write a prompt and the MCP Toolkit
takes care of installing and running the server:

```plaintext
Add the postgres mcp server
```

## Tool composition with code mode

The `code-mode` tool is available as an experimental capability for creating
custom JavaScript functions that combine multiple MCP server tools. The
intended use case is to enable workflows that coordinate multiple services
in a single operation.

> **Note**
>
>
>
> Code mode is in early development and is not yet reliable for general use.
> The documentation intentionally omits usage examples at this time.
>
>
>
> The core Dynamic MCP capabilities (`mcp-find`, `mcp-add`, `mcp-config-set`,
> `mcp-remove`) work as documented and are the recommended focus for current
> use.

The architecture works as follows:

1. The agent calls `code-mode` with a list of server names and a tool name
2. The gateway creates a sandbox with access to those servers' tools
3. A new tool is registered in the current session with the specified name
4. The agent calls the newly created tool
5. The code executes in the sandbox with access to the specified tools
6. Results are returned to the agent

The sandbox can only interact with the outside world through MCP tools,
which are already running in isolated containers with restricted privileges.

## Security considerations

Dynamic MCP maintains the same security model as static MCP server
configuration in MCP Toolkit:

- All servers in the MCP Catalog are built, signed, and maintained by Docker
- Servers run in isolated containers with restricted resources
- Code mode runs agent-written JavaScript in an isolated sandbox that can only
  interact through MCP tools
- Credentials are managed by the gateway and injected securely into containers

The key difference with dynamic capabilities is that agents can add new tools
during runtime.

## Disabling Dynamic MCP

Dynamic MCP is enabled by default in the MCP Toolkit. If you prefer to use only
statically configured MCP servers, you can disable the dynamic tools feature:

```console
$ docker mcp feature disable dynamic-tools
```

To re-enable the feature later:

```console
$ docker mcp feature enable dynamic-tools
```

After changing this setting, you may need to restart any connected MCP clients.

## Further reading

Check out the [Dynamic MCP servers with Docker](https://docker.com/blog) blog
post for more examples and inspiration on how you can use dynamic tools.

---

# E2B sandboxes

> Cloud-based secure sandboxes for AI agents with built-in Docker MCP Gateway integration

# E2B sandboxes

   Table of contents

---

Docker has partnered with [E2B](https://e2b.dev/), a provider of secure cloud sandboxes for AI agents. Through this partnership, every E2B sandbox includes direct access to Docker's [MCP Catalog](https://hub.docker.com/mcp), a collection of 200+ tools from publishers including GitHub, Notion, and Stripe.

When you create a sandbox, you specify which MCP tools it should access. E2B launches these tools and provides access through the Docker MCP Gateway.

## Example: Using GitHub and Notion MCP server

This example demonstrates how to connect multiple MCP servers in an E2B sandbox. You'll analyze data in Notion and create GitHub issues using Claude.

### Prerequisites

Before you begin, make sure you have the following:

- [E2B account](https://e2b.dev/docs/quickstart) with API access
- Anthropic API key for Claude
  > Note
  >
  > This example uses Claude Code which comes pre-installed in E2B sandboxes.
  > However, you can adapt the example to work with other AI assistants of your
  > choice. See [E2B's MCP documentation](https://e2b.dev/docs/mcp/quickstart)
  > for alternative connection methods.
- Node.js 18+ installed on your machine
- Notion account with:
  - A database containing sample data
  - [Integration token](https://www.notion.com/help/add-and-manage-connections-with-the-api)
- GitHub account with:
  - A repository for testing
  - Personal access token with `repo` scope

### Set up your environment

Create a new directory and initialize a Node.js project:

```console
$ mkdir mcp-e2b-quickstart
$ cd mcp-e2b-quickstart
$ npm init -y
```

Configure your project for ES modules by updating `package.json`:

```json
{
  "name": "mcp-e2b-quickstart",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "start": "node index.js"
  }
}
```

Install required dependencies:

```console
$ npm install e2b dotenv
```

Create a `.env` file with your credentials:

```console
$ cat > .env << 'EOF'
E2B_API_KEY=your_e2b_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
NOTION_INTEGRATION_TOKEN=ntn_your_notion_integration_token_here
GITHUB_TOKEN=ghp_your_github_pat_here
EOF
```

Protect your credentials:

```console
$ echo ".env" >> .gitignore
$ echo "node_modules/" >> .gitignore
```

### Create an E2B sandbox with MCP servers

Create a file named `index.ts`:

```typescript
import "dotenv/config";
import { Sandbox } from "e2b";

async function quickstart(): Promise<void> {
  console.log("Creating E2B sandbox with Notion and GitHub MCP servers...\n");

  const sbx: Sandbox = await Sandbox.create({
    envs: {
      ANTHROPIC_API_KEY: process.env.ANTHROPIC_API_KEY as string,
    },
    mcp: {
      notion: {
        internalIntegrationToken: process.env
          .NOTION_INTEGRATION_TOKEN as string,
      },
      githubOfficial: {
        githubPersonalAccessToken: process.env.GITHUB_TOKEN as string,
      },
    },
  });

  const mcpUrl = sbx.getMcpUrl();
  const mcpToken = await sbx.getMcpToken();

  console.log("Sandbox created successfully!");
  console.log(`MCP Gateway URL: ${mcpUrl}\n`);

  // Wait for MCP initialization
  await new Promise<void>((resolve) => setTimeout(resolve, 1000));

  // Connect Claude to MCP gateway
  console.log("Connecting Claude to MCP gateway...");
  await sbx.commands.run(
    `claude mcp add --transport http e2b-mcp-gateway ${mcpUrl} --header "Authorization: Bearer ${mcpToken}"`,
    {
      timeoutMs: 0,
      onStdout: console.log,
      onStderr: console.log,
    },
  );

  console.log("\nConnection successful! Cleaning up...");
  await sbx.kill();
}

quickstart().catch(console.error);
```

Run the script:

```console
$ npx tsx index.ts
```

Create a file named `index.py`:

```python
import os
import asyncio
from dotenv import load_dotenv
from e2b import Sandbox

load_dotenv()

async def quickstart():
    print("Creating E2B sandbox with Notion and GitHub MCP servers...\n")

    sbx = await Sandbox.beta_create(
        envs={
            "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
        },
        mcp={
            "notion": {
                "internalIntegrationToken": os.getenv("NOTION_INTEGRATION_TOKEN"),
            },
            "githubOfficial": {
                "githubPersonalAccessToken": os.getenv("GITHUB_TOKEN"),
            },
        },
    )

    mcp_url = sbx.beta_get_mcp_url()
    mcp_token = await sbx.beta_get_mcp_token()

    print("Sandbox created successfully!")
    print(f"MCP Gateway URL: {mcp_url}\n")

    # Wait for MCP initialization
    await asyncio.sleep(1)

    # Connect Claude to MCP gateway
    print("Connecting Claude to MCP gateway...")

    def on_stdout(output):
        print(output, end='')

    def on_stderr(output):
        print(output, end='')

    await sbx.commands.run(
        f'claude mcp add --transport http e2b-mcp-gateway {mcp_url} --header "Authorization: Bearer {mcp_token}"',
        timeout_ms=0,
        on_stdout=on_stdout,
        on_stderr=on_stderr
    )

    print("\nConnection successful! Cleaning up...")
    await sbx.kill()

if __name__ == "__main__":
    try:
        asyncio.run(quickstart())
    except Exception as e:
        print(f"Error: {e}")
```

Run the script:

```console
$ python index.py
```

You should see:

```console
Creating E2B sandbox with Notion and GitHub MCP servers...

Sandbox created successfully!
MCP Gateway URL: https://50005-xxxxx.e2b.app/mcp

Connecting Claude to MCP gateway...
Added HTTP MCP server e2b-mcp-gateway with URL: https://50005-xxxxx.e2b.app/mcp

Connection successful! Cleaning up...
```

### Test with example workflow

Now, test the setup by running a simple workflow that searches Notion and creates a GitHub issue.

> Important
>
> Replace `owner/repo` in the prompt with your actual GitHub username and repository
> name (for example, `yourname/test-repo`).

Update `index.ts` with the following example:

```typescript
import "dotenv/config";
import { Sandbox } from "e2b";

async function exampleWorkflow(): Promise<void> {
  console.log("Creating sandbox...\n");

  const sbx: Sandbox = await Sandbox.create({
    envs: {
      ANTHROPIC_API_KEY: process.env.ANTHROPIC_API_KEY as string,
    },
    mcp: {
      notion: {
        internalIntegrationToken: process.env
          .NOTION_INTEGRATION_TOKEN as string,
      },
      githubOfficial: {
        githubPersonalAccessToken: process.env.GITHUB_TOKEN as string,
      },
    },
  });

  const mcpUrl = sbx.getMcpUrl();
  const mcpToken = await sbx.getMcpToken();

  console.log("Sandbox created successfully\n");

  // Wait for MCP servers to initialize
  await new Promise<void>((resolve) => setTimeout(resolve, 3000));

  console.log("Connecting Claude to MCP gateway...\n");
  await sbx.commands.run(
    `claude mcp add --transport http e2b-mcp-gateway ${mcpUrl} --header "Authorization: Bearer ${mcpToken}"`,
    {
      timeoutMs: 0,
      onStdout: console.log,
      onStderr: console.log,
    },
  );

  console.log("\nRunning example: Search Notion and create GitHub issue...\n");

  const prompt: string = `Using Notion and GitHub MCP tools:
1. Search my Notion workspace for databases
2. Create a test issue in owner/repo titled "MCP Toolkit Test" with description "Testing E2B + Docker MCP integration"
3. Confirm both operations completed successfully`;

  await sbx.commands.run(
    `echo '${prompt.replace(/'/g, "'\\''")}' | claude -p --dangerously-skip-permissions`,
    {
      timeoutMs: 0,
      onStdout: console.log,
      onStderr: console.log,
    },
  );

  await sbx.kill();
}

exampleWorkflow().catch(console.error);
```

Run the script:

```console
$ npx tsx index.ts
```

Update `index.py` with this example:

> Important
>
> Replace `owner/repo` in the prompt with your actual GitHub username and repository
> name (for example, `yourname/test-repo`).

```python
import os
import asyncio
import shlex
from dotenv import load_dotenv
from e2b import Sandbox

load_dotenv()

async def example_workflow():
    print("Creating sandbox...\n")

    sbx = await Sandbox.beta_create(
        envs={
            "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
        },
        mcp={
            "notion": {
                "internalIntegrationToken": os.getenv("NOTION_INTEGRATION_TOKEN"),
            },
            "githubOfficial": {
                "githubPersonalAccessToken": os.getenv("GITHUB_TOKEN"),
            },
        },
    )

    mcp_url = sbx.beta_get_mcp_url()
    mcp_token = await sbx.beta_get_mcp_token()

    print("Sandbox created successfully\n")

    # Wait for MCP servers to initialize
    await asyncio.sleep(3)

    print("Connecting Claude to MCP gateway...\n")

    def on_stdout(output):
        print(output, end='')

    def on_stderr(output):
        print(output, end='')

    await sbx.commands.run(
        f'claude mcp add --transport http e2b-mcp-gateway {mcp_url} --header "Authorization: Bearer {mcp_token}"',
        timeout_ms=0,
        on_stdout=on_stdout,
        on_stderr=on_stderr
    )

    print("\nRunning example: Search Notion and create GitHub issue...\n")

    prompt = """Using Notion and GitHub MCP tools:
1. Search my Notion workspace for databases
2. Create a test issue in owner/repo titled "MCP Toolkit Test" with description "Testing E2B + Docker MCP integration"
3. Confirm both operations completed successfully"""

    # Escape single quotes for shell
    escaped_prompt = prompt.replace("'", "'\\''")

    await sbx.commands.run(
        f"echo '{escaped_prompt}' | claude -p --dangerously-skip-permissions",
        timeout_ms=0,
        on_stdout=on_stdout,
        on_stderr=on_stderr
    )

    await sbx.kill()

if __name__ == "__main__":
    try:
        asyncio.run(example_workflow())
    except Exception as e:
        print(f"Error: {e}")
```

Run the script:

```console
$ python workflow.py
```

You should see:

```console
Creating sandbox...

Running example: Search Notion and create GitHub issue...

## Task Completed Successfully

I've completed both operations using the Notion and GitHub MCP tools:

### 1. Notion Workspace Search

Found 3 databases in your Notion workspace:
- **Customer Feedback** - Database with 12 entries tracking feature requests
- **Product Roadmap** - Planning database with 8 active projects
- **Meeting Notes** - Shared workspace with 45 pages

### 2. GitHub Issue Creation

Successfully created test issue:
- **Repository**: your-org/your-repo
- **Issue Number**: #47
- **Title**: "MCP Test"
- **Description**: "Testing E2B + Docker MCP integration"
- **Status**: Open
- **URL**: https://github.com/your-org/your-repo/issues/47

Both operations completed successfully. The MCP servers are properly configured and working.
```

The sandbox connected multiple MCP servers and orchestrated a workflow across Notion and GitHub. You can extend this pattern to combine any of the 200+ MCP servers in the Docker MCP Catalog.

## Related pages

- [How to build an AI-powered code quality workflow with SonarQube and E2B](https://docs.docker.com/guides/github-sonarqube-sandbox/)
- [Docker + E2B: Building the Future of Trusted AI](https://www.docker.com/blog/docker-e2b-building-the-future-of-trusted-ai/)
- [Docker Sandboxes](https://docs.docker.com/ai/sandboxes/)
- [Docker MCP Toolkit and Catalog](https://docs.docker.com/ai/mcp-catalog-and-toolkit/)
- [Docker MCP Gateway](https://docs.docker.com/ai/mcp-catalog-and-toolkit/mcp-gateway/)
- [E2B MCP documentation](https://e2b.dev/docs/mcp)

---

# Security FAQs

> Frequently asked questions related to MCP Catalog and Toolkit security

# Security FAQs

   Table of contents

---

Docker MCP Catalog and Toolkit is a solution for securely building, sharing, and
running MCP tools. This page answers common questions about MCP Catalog and Toolkit security.

### What process does Docker follow to add a new MCP server to the catalog?

Developers can submit a pull request to the [Docker MCP Registry](https://github.com/docker/mcp-registry) to propose new servers. Docker provides detailed [contribution guidelines](https://github.com/docker/mcp-registry/blob/main/CONTRIBUTING.md) to help developers meet the required standards.

Currently, a majority of the servers in the catalog are built directly by Docker. Each server includes attestations such as:

- Build attestation: Servers are built on Docker Build Cloud.
- Source provenance: Verifiable source code origins.
- Signed SBOMs: Software Bill of Materials with cryptographic signatures.

> Note
>
> When using the images with
> [Docker MCP gateway](https://docs.docker.com/ai/mcp-catalog-and-toolkit/mcp-gateway/),
> you can verify attestations at runtime using the `docker mcp gateway run --verify-signatures` CLI command.

In addition to Docker-built servers, the catalog includes select servers from trusted registries such as GitHub and HashiCorp. Each third-party server undergoes a verification process that includes:

- Pulling and building the code in an ephemeral build environment.
- Testing initialization and functionality.
- Verifying that tools can be successfully listed.

### Under what conditions does Docker reject MCP server submissions?

Docker rejects MCP server submissions that fail automated testing and validation processes during pull request review. Additionally, Docker reviewers evaluate submissions against specific requirements and reject MCP servers that don't meet these criteria.

### Does Docker take accountability for malicious MCP servers in the Toolkit?

Docker’s security measures currently represent a best-effort approach. While Docker implements automated testing, scanning, and metadata extraction for each server in the catalog, these security measures are not yet exhaustive. Docker is actively working to enhance its security processes and expand testing coverage. Enterprise customers can contact their Docker account manager for specific security requirements and implementation details.

### How are credentials managed for MCP servers?

Starting with Docker Desktop version 4.43.0, credentials are stored securely in the Docker Desktop VM. The storage implementation depends on the platform (for example, macOS, WSL2). You can manage the credentials using the following CLI commands:

- `docker mcp secret ls` - List stored credentials
- `docker mcp secret rm` - Remove specific credentials
- `docker mcp oauth revoke` - Revoke OAuth-based credentials

In the upcoming versions of Docker Desktop, Docker plans to support pluggable storage for these secrets and additional out-of-the-box storage providers to give users more flexibility in managing credentials.

### Are credentials removed when an MCP server is uninstalled?

No. MCP servers are not technically uninstalled since they exist as Docker containers pulled to your local Docker Desktop. Removing an MCP server stops the container but leaves the image on your system. Even if the container is deleted, credentials remain stored until you remove them manually.

### Why don't I see remote MCP servers in the catalog?

If remote MCP servers aren't visible in the Docker Desktop catalog, your local
catalog may be out of date. Remote servers are indicated by a cloud icon and
include services like GitHub, Notion, and Linear.

Update your catalog by running:

```console
$ docker mcp catalog update
```

After the update completes, refresh the **Catalog** tab in Docker Desktop.

## Related pages

- [Get started with MCP Toolkit](https://docs.docker.com/ai/mcp-catalog-and-toolkit/get-started/)
- [Open-source MCP Gateway](https://docs.docker.com/ai/mcp-catalog-and-toolkit/mcp-gateway/)
