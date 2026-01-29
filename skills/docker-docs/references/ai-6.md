# Get started with Docker MCP Toolkit and more

# Get started with Docker MCP Toolkit

> Learn how to quickly install and use the MCP Toolkit to set up servers and clients.

# Get started with Docker MCP Toolkit

   Table of contents

---

Availability: Beta

The Docker MCP Toolkit makes it easy to set up, manage, and run containerized
Model Context Protocol (MCP) servers, and connect them to AI agents. It
provides secure defaults and support for a growing ecosystem of LLM-based
clients. This page shows you how to get started quickly with the Docker MCP
Toolkit.

## Setup

Before you begin, make sure you meet the following requirements to get started with Docker MCP Toolkit.

1. Download and install the latest version of
  [Docker Desktop](https://docs.docker.com/get-started/get-docker/).
2. Open the Docker Desktop settings and select **Beta features**.
3. Select **Enable Docker MCP Toolkit**.
4. Select **Apply**.

The **Learning center** in Docker Desktop provides walkthroughs and resources
to help you get started with Docker products and features. On the **MCP
Toolkit** page, the **Get started** walkthrough that guides you through
installing an MCP server, connecting a client, and testing your setup.

Alternatively, follow the step-by-step instructions on this page to:

- [Install MCP servers](#install-mcp-servers)
- [Connect clients](#connect-clients)
- [Verify connections](#verify-connections)

## Install MCP servers

1. In Docker Desktop, select **MCP Toolkit** and select the **Catalog** tab.
2. Search for the **GitHub Official** server from the catalog and then select the plus icon to add it.
3. In the **GitHub Official** server page, select the **Configuration** tab and select **OAuth**.
  > Note
  >
  > The type of configuration required depends on the server you select. For the GitHub Official server, you must authenticate using OAuth.
  Your browser opens the GitHub authorization page. Follow the on-screen instructions to
  [authenticate via OAuth](https://docs.docker.com/ai/mcp-catalog-and-toolkit/toolkit/#authenticate-via-oauth).
4. Return to Docker Desktop when the authentication process is complete.
5. Search for the **Playwright** server from the catalog and add it.

1. Add the GitHub Official MCP server. Run:
  ```console
  $ docker mcp server enable github-official
  ```
2. Authenticate the server by running the following command:
  ```console
  $ docker mcp oauth authorize github
  ```
  > Note
  >
  > The type of configuration required depends on the server you select. For the GitHub Official server, you must authenticate using OAuth.
  Your browser opens the GitHub authorization page. Follow the on-screen instructions to
  [authenticate via OAuth](https://docs.docker.com/ai/mcp-catalog-and-toolkit/toolkit/#authenticate-via-oauth).
3. Add the **Playwright** server. Run:
  ```console
  $ docker mcp server enable playwright
  ```

You’ve now successfully added an MCP server. Next, connect an MCP client to use
the MCP Toolkit in an AI application.

## Connect clients

To connect a client to MCP Toolkit:

1. In Docker Desktop, select **MCP Toolkit** and select the **Clients** tab.
2. Find your application in the list.
3. Select **Connect** to configure the client.

If your client isn't listed, you can connect the MCP Toolkit manually over
`stdio` by configuring your client to run the following command:

```plaintext
docker mcp gateway run
```

For example, if your client uses a JSON file to configure MCP servers, you may
add an entry like:

```json
{
  "servers": {
    "MCP_DOCKER": {
      "command": "docker",
      "args": ["mcp", "gateway", "run"],
      "type": "stdio"
    }
  }
}
```

Consult the documentation of the application you're using for instructions on
how to set up MCP servers manually.

## Verify connections

Refer to the relevant section for instructions on how to verify that your setup
is working:

- [Claude Code](#claude-code)
- [Claude Desktop](#claude-desktop)
- [OpenAI Codex](#codex)
- [Continue](#continue)
- [Cursor](#cursor)
- [Gemini](#gemini)
- [Goose](#goose)
- [Gordon](#gordon)
- [LM Studio](#lm-studio)
- [OpenCode](#opencode)
- [Sema4.ai](#sema4)
- [Visual Studio Code](#vscode)
- [Zed](#zed)

### Claude Code

If you configured the MCP Toolkit for a specific project, navigate to the
relevant project directory. Then run `claude mcp list`. The output should show
`MCP_DOCKER` with a "connected" status:

```console
$ claude mcp list
Checking MCP server health...

MCP_DOCKER: docker mcp gateway run - ✓ Connected
```

Test the connection by submitting a prompt that invokes one of your installed
MCP servers:

```console
$ claude "Use the GitHub MCP server to show me my open pull requests"
```

### Claude Desktop

Restart Claude Desktop and check the **Search and tools** menu in the chat
input. You should see the `MCP_DOCKER` server listed and enabled:

![Claude Desktop](https://docs.docker.com/ai/mcp-catalog-and-toolkit/images/claude-desktop.avif)  ![Claude Desktop](https://docs.docker.com/ai/mcp-catalog-and-toolkit/images/claude-desktop.avif)

Test the connection by submitting a prompt that invokes one of your installed
MCP servers:

```plaintext
Use the GitHub MCP server to show me my open pull requests
```

### Codex

Run `codex mcp list` to view active MCP servers and their statuses. The
`MCP_DOCKER` server should appear in the list with an "enabled" status:

```console
$ codex mcp list
Name        Command  Args             Env  Cwd  Status   Auth
MCP_DOCKER  docker   mcp gateway run  -    -    enabled  Unsupported
```

Test the connection by submitting a prompt that invokes one of your installed
MCP servers:

```console
$ codex "Use the GitHub MCP server to show me my open pull requests"
```

### Continue

Launch the Continue terminal UI by running `cn`. Use the `/mcp` command to view
active MCP servers and their statuses. The `MCP_DOCKER` server should appear in
the list with a "connected" status:

```plaintext
MCP Servers

   ➤ 🟢 MCP_DOCKER (🔧75 📝3)
     🔄 Restart all servers
     ⏹️ Stop all servers
     🔍 Explore MCP Servers
     Back

   ↑/↓ to navigate, Enter to select, Esc to go back
```

Test the connection by submitting a prompt that invokes one of your installed
MCP servers:

```console
$ cn "Use the GitHub MCP server to show me my open pull requests"
```

### Cursor

Open Cursor. If you configured the MCP Toolkit for a specific project, open the
relevant project directory. Then navigate to **Cursor Settings > Tools & MCP**.
You should see `MCP_DOCKER` under **Installed MCP Servers**:

![Cursor](https://docs.docker.com/ai/mcp-catalog-and-toolkit/images/cursor.avif)  ![Cursor](https://docs.docker.com/ai/mcp-catalog-and-toolkit/images/cursor.avif)

Test the connection by submitting a prompt that invokes one of your installed
MCP servers:

```plaintext
Use the GitHub MCP server to show me my open pull requests
```

### Gemini

Run `gemini mcp list` to view active MCP servers and their statuses. The
`MCP_DOCKER` should appear in the list with a "connected" status.

```console
$ gemini mcp list
Configured MCP servers:

✓ MCP_DOCKER: docker mcp gateway run (stdio) - Connected
```

Test the connection by submitting a prompt that invokes one of your installed
MCP servers:

```console
$ gemini "Use the GitHub MCP server to show me my open pull requests"
```

### Goose

Open the Goose desktop application and select **Extensions** in the sidebar.
Under **Enabled Extensions**, you should see an extension named `Mcpdocker`:

![Goose desktop app](https://docs.docker.com/ai/mcp-catalog-and-toolkit/images/goose.avif)  ![Goose desktop app](https://docs.docker.com/ai/mcp-catalog-and-toolkit/images/goose.avif)

Run `goose info -v` and look for an entry named `mcpdocker` under extensions.
The status should show `enabled: true`:

```console
$ goose info -v
…
    mcpdocker:
      args:
      - mcp
      - gateway
      - run
      available_tools: []
      bundled: null
      cmd: docker
      description: The Docker MCP Toolkit allows for easy configuration and consumption of MCP servers from the Docker MCP Catalog
      enabled: true
      env_keys: []
      envs: {}
      name: mcpdocker
      timeout: 300
      type: stdio
```

Test the connection by submitting a prompt that invokes one of your installed
MCP servers:

```plaintext
Use the GitHub MCP server to show me my open pull requests
```

### Gordon

Open the **Ask Gordon** view in Docker Desktop and select the toolbox icon in
the chat input area. The **MCP Toolkit** tab shows whether MCP Toolkit is
enabled and displays all the provided tools:

![MCP Toolkit in the Ask Gordon UI](https://docs.docker.com/ai/mcp-catalog-and-toolkit/images/ask-gordon.avif)  ![MCP Toolkit in the Ask Gordon UI](https://docs.docker.com/ai/mcp-catalog-and-toolkit/images/ask-gordon.avif)

Test the connection by submitting a prompt that invokes one of your installed
MCP servers, either directly in Docker Desktop or using the CLI:

```console
$ docker ai "Use the GitHub MCP server to show me my open pull requests"
```

### LM Studio

Restart LM Studio and start a new chat. Open the integrations menu and look for
an entry named `mcp/mcp-docker`. Use the toggle to enable the server:

![LM Studio](https://docs.docker.com/ai/mcp-catalog-and-toolkit/images/lm-studio.avif)  ![LM Studio](https://docs.docker.com/ai/mcp-catalog-and-toolkit/images/lm-studio.avif)

Test the connection by submitting a prompt that invokes one of your installed
MCP servers:

```plaintext
Use the GitHub MCP server to show me my open pull requests
```

### OpenCode

The OpenCode configuration file (at `~/.config/opencode/opencode.json` by
default) contains the setup for MCP Toolkit:

```json
{
  "mcp": {
    "MCP_DOCKER": {
      "type": "local",
      "command": ["docker", "mcp", "gateway", "run"],
      "enabled": true
    }
  },
  "$schema": "https://opencode.ai/config.json"
}
```

Test the connection by submitting a prompt that invokes one of your installed
MCP servers:

```console
$ opencode "Use the GitHub MCP server to show me my open pull requests"
```

### Sema4.ai Studio

In Sema4.ai Studio, select **Actions** in the sidebar, then select the **MCP
Servers** tab. You should see Docker MCP Toolkit in the list:

![Docker MCP Toolkit in Sema4.ai Studio](https://docs.docker.com/ai/mcp-catalog-and-toolkit/images/sema4-mcp-list.avif)  ![Docker MCP Toolkit in Sema4.ai Studio](https://docs.docker.com/ai/mcp-catalog-and-toolkit/images/sema4-mcp-list.avif)

To use MCP Toolkit with Sema4.ai, add it as an agent action. Find the agent you
want to connect to the MCP Toolkit and open the agent editor. Select **Add
Action**, enable Docker MCP Toolkit in the list, then save your agent:

![Editing an agent in Sema4.ai Studio](https://docs.docker.com/ai/mcp-catalog-and-toolkit/images/sema4-edit-agent.avif)  ![Editing an agent in Sema4.ai Studio](https://docs.docker.com/ai/mcp-catalog-and-toolkit/images/sema4-edit-agent.avif)

Test the connection by submitting a prompt that invokes one of your installed
MCP servers:

```plaintext
Use the GitHub MCP server to show me my open pull requests
```

### Visual Studio Code

Open Visual Studio Code. If you configured the MCP Toolkit for a specific
project, open the relevant project directory. Then open the **Extensions**
pane. You should see the `MCP_DOCKER` server listed under installed MCP
servers.

![MCP_DOCKER installed in Visual Studio Code](https://docs.docker.com/ai/mcp-catalog-and-toolkit/images/vscode-extensions.avif)  ![MCP_DOCKER installed in Visual Studio Code](https://docs.docker.com/ai/mcp-catalog-and-toolkit/images/vscode-extensions.avif)

Test the connection by submitting a prompt that invokes one of your installed
MCP servers:

```plaintext
Use the GitHub MCP server to show me my open pull requests
```

### Zed

Launch Zed and open agent settings:

![Opening Zed agent settings from command palette](https://docs.docker.com/ai/mcp-catalog-and-toolkit/images/zed-cmd-palette.avif)  ![Opening Zed agent settings from command palette](https://docs.docker.com/ai/mcp-catalog-and-toolkit/images/zed-cmd-palette.avif)

Ensure that `MCP_DOCKER` is listed and enabled in the MCP Servers section:

![MCP_DOCKER in Zed's agent settings](https://docs.docker.com/ai/mcp-catalog-and-toolkit/images/zed-agent-settings.avif)  ![MCP_DOCKER in Zed's agent settings](https://docs.docker.com/ai/mcp-catalog-and-toolkit/images/zed-agent-settings.avif)

Test the connection by submitting a prompt that invokes one of your installed
MCP servers:

```plaintext
Use the GitHub MCP server to show me my open pull requests
```

## Further reading

- [MCP Toolkit](https://docs.docker.com/ai/mcp-catalog-and-toolkit/toolkit/)
- [MCP Catalog](https://docs.docker.com/ai/mcp-catalog-and-toolkit/catalog/)
- [MCP Gateway](https://docs.docker.com/ai/mcp-catalog-and-toolkit/mcp-gateway/)

---

# Docker Hub MCP server

> The Docker Hub MCP Server makes Docker Hub image metadata accessible to LLMs for content discovery.

# Docker Hub MCP server

   Table of contents

---

The Docker Hub MCP Server is a Model Context Protocol (MCP) server that
interfaces with Docker Hub APIs to make rich image metadata accessible to LLMs,
enabling intelligent content discovery and repository management.

For more information about MCP concepts and how MCP servers work, see the [Docker MCP Catalog and Toolkit](https://docs.docker.com/ai/mcp-catalog-and-toolkit/) overview page.

## Key features

- Advanced LLM context: Docker's MCP Server provides LLMs with detailed, structured context for Docker Hub images, enabling smarter, more relevant recommendations for developers, whether they're choosing a base image or automating CI/CD workflows.
- Natural language image discovery: Developers can find the right container image using natural language, no need to remember tags or repository names. Just describe what you need, and Docker Hub will return images that match your intent.
- Simplified repository management: Hub MCP Server enables agents to manage repositories through natural language fetching image details, viewing stats, searching content, and performing key operations quickly and easily.

## Install Docker Hub MCP server

1. From the **MCP Toolkit** menu, select the **Catalog** tab and search for **Docker Hub** and select the plus icon to add the Docker Hub MCP server.
2. In the server's **Configuration** tab, insert your Docker Hub username and personal access token (PAT).
3. In the **Clients** tab in MCP Toolkit, ensure Gordon is connected.
4. From the **Ask Gordon** menu, you can now send requests related to your
  Docker Hub account, in accordance to the tools provided by the Docker Hub MCP server. To test it, ask Gordon:
  ```text
  What repositories are in my namespace?
  ```

> Tip
>
> By default, the Gordon
> [client](https://docs.docker.com/ai/mcp-catalog-and-toolkit/toolkit/#install-an-mcp-client) is enabled,
> which means Gordon can automatically interact with your MCP servers.

## Use Claude Desktop as a client

1. Add the Docker Hub MCP Server configuration to your `claude_desktop_config.json`:
  ```json
  {
    "mcpServers": {
      "docker-hub": {
        "command": "node",
        "args": ["/FULL/PATH/TO/YOUR/docker-hub-mcp-server/dist/index.js", "--transport=stdio"]
      }
    }
  }
  ```
  Where :
  - `/FULL/PATH/TO/YOUR/docker-hub-mcp-server` is the complete path to where you cloned the repository
  ```json
  {
    "mcpServers": {
      "docker-hub": {
        "command": "node",
        "args": ["/FULL/PATH/TO/YOUR/docker-hub-mcp-server/dist/index.js", "--transport=stdio", "--username=YOUR_DOCKER_HUB_USERNAME"],
        "env": {
          "HUB_PAT_TOKEN": "YOUR_DOCKER_HUB_PERSONAL_ACCESS_TOKEN"
        }
      }
    }
  }
  ```
  Where :
  - `YOUR_DOCKER_HUB_USERNAME` is your Docker Hub username.
  - `YOUR_DOCKER_HUB_PERSONAL_ACCESS_TOKEN` is Docker Hub personal access token
  - `/FULL/PATH/TO/YOUR/docker-hub-mcp-server` is the complete path to where you cloned the repository
2. Save the configuration file and completely restart Claude Desktop for the changes to take effect.

## Usage with Visual Studio Code

1. Add the Docker Hub MCP Server configuration to your User Settings (JSON)
  file in Visual Studio Code. You can do this by opening the `Command Palette` and
  typing `Preferences: Open User Settings (JSON)`.
  ```json
  {
    "mcpServers": {
      "docker-hub": {
        "command": "node",
        "args": ["/FULL/PATH/TO/YOUR/docker-hub-mcp-server/dist/index.js", "--transport=stdio"]
      }
    }
  }
  ```
  Where :
  - `/FULL/PATH/TO/YOUR/docker-hub-mcp-server` is the complete path to where you cloned the repository
  ```json
  {
    "mcpServers": {
      "docker-hub": {
        "command": "node",
        "args": ["/FULL/PATH/TO/YOUR/docker-hub-mcp-server/dist/index.js", "--transport=stdio"],
        "env": {
          "HUB_USERNAME": "YOUR_DOCKER_HUB_USERNAME",
          "HUB_PAT_TOKEN": "YOUR_DOCKER_HUB_PERSONAL_ACCESS_TOKEN"
        }
      }
    }
  }
  ```
  Where :
  - `YOUR_DOCKER_HUB_USERNAME` is your Docker Hub username.
  - `YOUR_DOCKER_HUB_PERSONAL_ACCESS_TOKEN` is Docker Hub personal access token
  - `/FULL/PATH/TO/YOUR/docker-hub-mcp-server` is the complete path to where you cloned the repository
2. Open the `Command Palette` and type `MCP: List Servers`.
3. Select `docker-hub` and select `Start Server`.

## Using other clients

To integrate the Docker Hub MCP Server into your own development
environment, see the source code and installation instructions on the
[hub-mcpGitHub repository](https://github.com/docker/hub-mcp).

## Usage examples

This section provides task-oriented examples for common operations with Docker Hub
tools.

### Finding images

```console
# Search for official images
$ docker ai "Search for official nginx images on Docker Hub"

# Search for lightweight images to reduce deployment size and improve performance
$ docker ai "Search for minimal Node.js images with small footprint"

# Get the most recent tag of a base image
$ docker ai "Show me the latest tag details for go"

# Find a production-ready database with enterprise features and reliability
$ docker ai "Search for production ready database images"

# Compare Ubuntu versions to choose the right one for my project
$ docker ai "Help me find the right Ubuntu version for my project"
```

### Repository management

```console
# Create a repository
$ docker ai "Create a repository in my namespace"

# List all repositories in my namespace
$ docker ai "List all repositories in my namespace"

# Find the largest repository in my namespace
$ docker ai "Which of my repositories takes up the most space?"

# Find repositories that haven't been updated recently
$ docker ai "Which of my repositories haven't had any pushes in the last 60 days?"

# Find which repositories are currently active and being used
$ docker ai "Show me my most recently updated repositories"

# Get details about a repository
$ docker ai "Show me information about my '<repository-name>' repository"
```

### Pull/push images

```console
# Pull latest PostgreSQL version
$ docker ai "Pull the latest postgres image"

# Push image to your Docker Hub repository
$ docker ai "Push my <image-name> to my <repository-name> repository"
```

### Tag management

```console
# List all tags for a repository
$ $ docker ai "Show me all tags for my '<repository-name>' repository"

# Find the most recently pushed tag
$ docker ai "What's the most recent tag pushed to my '<repository-name>' repository?"

# List tags with architecture filtering
$ docker ai "List tags for in the '<repository-name>' repository that support amd64 architecture"

# Get detailed information about a specific tag
$ docker ai "Show me details about the '<tag-name>' tag in the '<repository-name>' repository"

# Check if a specific tag exists
$ docker ai "Check if version 'v1.2.0' exists for my 'my-web-app' repository"
```

### Docker Hardened Images

```console
# List available hardened images
$ docker ai "What is the most secure image I can use to run a node.js application?"

# Convert Dockerfile to use a hardened image
$ docker ai "Can you help me update my Dockerfile to use a docker hardened image instead of the current one"
```

> Note
>
> To access Docker Hardened Images, a subscription is required. If you're interested in using Docker Hardened Images, visit [Docker Hardened Images](https://www.docker.com/products/hardened-images/).

## Reference

This section provides a comprehensive listing of the tools you can find
in the Docker Hub MCP Server.

### Docker Hub MCP server tools

Tools to interact with your Docker repositories and discover content on Docker Hub.

| Name | Description |
| --- | --- |
| check-repository | Check repository |
| check-repository-tag | Check repository tag |
| check-repository-tags | Check repository tags |
| create-repository | Creates a new repository |
| docker-hardened-images | Lists availableDocker Hardened Imagesin specified namespace |
| get-namespaces | Get organizations/namespaces for a user |
| get-repository-dockerfile | Gets Dockerfile for repository |
| get-repository-info | Gets repository info |
| list-repositories-by-namespace | Lists repositories under namespace |
| list-repository-tags | List repository tags |
| read-repository-tag | Read repository tag |
| search | Search content on Docker Hub |
| set-repository-dockerfile | Sets Dockerfile for repository |
| update-repository-info | Updates repository info |

---

# MCP Gateway

> Docker's MCP Gateway provides secure, centralized, and scalable orchestration of AI tools through containerized MCP servers—empowering developers, operators, and security teams.

# MCP Gateway

   Table of contents

---

The MCP Gateway is Docker's open source solution for orchestrating Model
Context Protocol (MCP) servers. It acts as a centralized proxy between clients
and servers, managing configuration, credentials, and access control.

When using MCP servers without the MCP Gateway, you need to configure
applications individually for each AI application. With the MCP Gateway, you
configure applications to connect to the Gateway. The Gateway then handles
server lifecycle, routing, and authentication across all your servers.

> Note
>
> If you use Docker Desktop with MCP Toolkit enabled, the Gateway runs
> automatically in the background. You don't need to start or configure it
> manually. This documentation is for users who want to understand how the
> Gateway works or run it directly for advanced use cases.

> Tip
>
> E2B sandboxes now include direct access to the Docker MCP Catalog, giving developers
> access to over 200 tools and services to seamlessly build and run AI agents. For
> more information, see [E2B Sandboxes](https://docs.docker.com/ai/sandboxes/).

## How it works

MCP Gateway runs MCP servers in isolated Docker containers with restricted
privileges, network access, and resource usage. It includes built-in logging
and call-tracing capabilities to ensure full visibility and governance of AI
tool activity.

The MCP Gateway manages the server's entire lifecycle. When an AI application
needs to use a tool, it sends a request to the Gateway. The Gateway identifies
which server handles that tool and, if the server isn't already running, starts
it as a Docker container. The Gateway then injects any required credentials,
applies security restrictions, and forwards the request to the server. The
server processes the request and returns the result through the Gateway back to
the AI application.

The MCP Gateway solves a fundamental problem: MCP servers are just programs
that need to run somewhere. Running them directly on your machine means dealing
with installation, dependencies, updates, and security risks. By running them
as containers managed by the Gateway, you get isolation, consistent
environments, and centralized control.

## Usage

To use the MCP Gateway, you'll need Docker Desktop with MCP Toolkit enabled.
Follow the [MCP Toolkit guide](https://docs.docker.com/ai/mcp-catalog-and-toolkit/toolkit/) to enable and configure servers
through the graphical interface.

### Manage the MCP Gateway from the CLI

With MCP Toolkit enabled, you can also interact with the MCP Gateway using the
CLI. The `docker mcp` suite of commands lets you manage servers and tools
directly from your terminal. You can also manually run Gateways with custom
configurations, including security restrictions, server catalogs, and more.

To run an MCP Gateway manually, with customized parameters, use the `docker mcp` suite of commands.

1. Browse the [MCP Catalog](https://hub.docker.com/mcp) for a server that you
  want to use, and copy the install command from the **Manual installation**
  section.
  For example, run this command in your terminal to install the `duckduckgo`
  MCP server:
  ```console
  docker mcp server enable duckduckgo
  ```
2. Connect a client, like Claude Code:
  ```console
  docker mcp client connect claude-code
  ```
3. Run the gateway:
  ```console
  docker mcp gateway run
  ```

Now your MCP gateway is running and you can leverage all the servers set up
behind it from Claude Code.

### Install the MCP Gateway manually

For Docker Engine without Docker Desktop, you'll need to download and install
the MCP Gateway separately before you can run it.

1. Download the latest binary from the [GitHub releases page](https://github.com/docker/mcp-gateway/releases/latest).
2. Move or symlink the binary to the destination matching your OS:
  | OS | Binary destination |
  | --- | --- |
  | Linux | ~/.docker/cli-plugins/docker-mcp |
  | macOS | ~/.docker/cli-plugins/docker-mcp |
  | Windows | %USERPROFILE%\.docker\cli-plugins |
3. Make the binaries executable:
  ```bash
  $ chmod +x ~/.docker/cli-plugins/docker-mcp
  ```

You can now use the `docker mcp` command:

```bash
docker mcp --help
```

## Additional information

For more details on how the MCP Gateway works and available customization
options, see the complete documentation [on GitHub](https://github.com/docker/mcp-gateway).

---

# Docker MCP Toolkit

> Use the MCP Toolkit to set up MCP servers and MCP clients.

# Docker MCP Toolkit

   Table of contents

---

Availability: Beta

The Docker MCP Toolkit is a management interface integrated into Docker Desktop
that lets you set up, manage, and run containerized MCP servers and connect
them to AI agents. It removes friction from tool usage by offering secure
defaults, easy setup, and support for a growing ecosystem of LLM-based clients.
It is the fastest way from MCP tool discovery to local execution.

## Key features

- Cross-LLM compatibility: Works with Claude, Cursor, and other MCP clients.
- Integrated tool discovery: Browse and launch MCP servers from the Docker MCP Catalog directly in Docker Desktop.
- Zero manual setup: No dependency management, runtime configuration, or setup required.
- Functions as both an MCP server aggregator and a gateway for clients to access installed MCP servers.

> Tip
>
> The MCP Toolkit includes
> [Dynamic MCP](https://docs.docker.com/ai/mcp-catalog-and-toolkit/dynamic-mcp/),
> which enables AI agents to discover, add, and compose MCP servers on-demand during
> conversations, without manual configuration. Your agent can search the catalog and
> add tools as needed when you connect to the gateway.

## How the MCP Toolkit works

MCP introduces two core concepts: MCP clients and MCP servers.

- MCP clients are typically embedded in LLM-based applications, such as the
  Claude Desktop app. They request resources or actions.
- MCP servers are launched by the client to perform the requested tasks, using
  any necessary tools, languages, or processes.

Docker standardizes the development, packaging, and distribution of
applications, including MCP servers. By packaging MCP servers as containers,
Docker eliminates issues related to isolation and environment differences. You
can run a container directly, without managing dependencies or configuring
runtimes.

Depending on the MCP server, the tools it provides might run within the same
container as the server or in dedicated containers for better isolation.

## Security

The Docker MCP Toolkit combines passive and active measures to reduce attack
surfaces and ensure safe runtime behavior.

### Passive security

Passive security refers to measures implemented at build-time, when the MCP
server code is packaged into a Docker image.

- Image signing and attestation: All MCP server images under `mcp/` in the [MCP
  Catalog](https://docs.docker.com/ai/mcp-catalog-and-toolkit/catalog/) are built by Docker and digitally signed to verify their
  source and integrity. Each image includes a Software Bill of Materials (SBOM)
  for full transparency.

### Active security

Active security refers to security measures at runtime, before and after tools
are invoked, enforced through resource and access limitations.

- CPU allocation: MCP tools are run in their own container. They are
  restricted to 1 CPU, limiting the impact of potential misuse of computing
  resources.
- Memory allocation: Containers for MCP tools are limited to 2 GB.
- Filesystem access: By default, MCP Servers have no access to the host filesystem.
  The user explicitly selects the servers that will be granted file mounts.
- Interception of tool requests: Requests to and from tools that contain sensitive
  information such as secrets are blocked.

### OAuth authentication

Some MCP servers require authentication to access external services like
GitHub, Notion, and Linear. The MCP Toolkit handles OAuth authentication
automatically. You authorize access through your browser, and the Toolkit
manages credentials securely. You don't need to manually create API tokens or
configure authentication for each service.

#### Authorize a server with OAuth

1. In Docker Desktop, go to **MCP Toolkit** and select the **Catalog** tab.
2. Find and add an MCP server that requires OAuth.
3. In the server's **Configuration** tab, select the **OAuth** authentication
  method. Follow the link to begin the OAuth authorization.
4. Your browser opens the authorization page for the service. Follow the
  on-screen instructions to complete authentication.
5. Return to Docker Desktop when authentication is complete.

View all authorized services in the **OAuth** tab. To revoke access, select
**Revoke** next to the service you want to disconnect.

Enable an MCP server:

```console
$ docker mcp server enable github-official
```

If the server requires OAuth, authorize the connection:

```console
$ docker mcp oauth authorize github
```

Your browser opens the authorization page. Complete the authentication process,
then return to your terminal.

View authorized services:

```console
$ docker mcp oauth ls
```

Revoke access to a service:

```console
$ docker mcp oauth revoke github
```

## Usage examples

### Example: Use the GitHub Official MCP server with Ask Gordon

To illustrate how the MCP Toolkit works, here's how to enable the GitHub
Official MCP server and use
[Ask Gordon](https://docs.docker.com/ai/gordon/) to
interact with your GitHub account:

1. From the **MCP Toolkit** menu in Docker Desktop, select the **Catalog** tab
  and find the **GitHub Official** server and add it.
2. In the server's **Configuration** tab, authenticate via OAuth.
3. In the **Clients** tab, ensure Gordon is connected.
4. From the **Ask Gordon** menu, you can now send requests related to your
  GitHub account, in accordance to the tools provided by the GitHub Official
  server. To test it, ask Gordon:
  ```text
  What's my GitHub handle?
  ```
  Make sure to allow Gordon to interact with GitHub by selecting **Always
  allow** in Gordon's answer.

> Tip
>
> The Gordon client is enabled by default,
> which means Gordon can automatically interact with your MCP servers.

### Example: Use Claude Desktop as a client

Imagine you have Claude Desktop installed, and you want to use the GitHub MCP server,
and the Puppeteer MCP server, you do not have to install the servers in Claude Desktop.
You can simply install these 2 MCP servers in the MCP Toolkit,
and add Claude Desktop as a client:

1. From the **MCP Toolkit** menu, select the **Catalog** tab and find the **Puppeteer** server and add it.
2. Repeat for the **GitHub Official** server.
3. From the **Clients** tab, select **Connect** next to **Claude Desktop**. Restart
  Claude Desktop if it's running, and it can now access all the servers in the MCP Toolkit.
4. Within Claude Desktop, run a test by submitting the following prompt using the Sonnet 3.5 model:
  ```text
  Take a screenshot of docs.docker.com and then invert the colors
  ```

### Example: Use Visual Studio Code as a client

You can interact with all your installed MCP servers in Visual Studio Code:

1. To enable the MCP Toolkit:
  1. Insert the following in your Visual Studio Code's User `mcp.json`:
    ```json
    "mcp": {
     "servers": {
       "MCP_DOCKER": {
         "command": "docker",
         "args": [
           "mcp",
           "gateway",
           "run"
         ],
         "type": "stdio"
       }
     }
    }
    ```
  1. In your terminal, navigate to your project's folder.
  2. Run:
    ```bash
    docker mcp client connect vscode
    ```
    > Note
    >
    > This command creates a `.vscode/mcp.json` file in the current
    > directory. As this is a user-specific file, add it to your `.gitignore`
    > file to prevent it from being committed to the repository.
    >
    >
    >
    > ```console
    > echo ".vscode/mcp.json" >> .gitignore
    > ```
2. In Visual Studio Code, open a new Chat and select the **Agent** mode:
  ![Copilot mode switching](https://docs.docker.com/ai/mcp-catalog-and-toolkit/images/copilot-mode.png)  ![Copilot mode switching](https://docs.docker.com/ai/mcp-catalog-and-toolkit/images/copilot-mode.png)
3. You can also check the available MCP tools:
  ![Displaying tools in VSCode](https://docs.docker.com/ai/mcp-catalog-and-toolkit/images/tools.png)  ![Displaying tools in VSCode](https://docs.docker.com/ai/mcp-catalog-and-toolkit/images/tools.png)

For more information about the Agent mode, see the
[Visual Studio Code documentation](https://code.visualstudio.com/docs/copilot/chat/mcp-servers#_use-mcp-tools-in-agent-mode).

## Further reading

- [MCP Catalog](https://docs.docker.com/ai/mcp-catalog-and-toolkit/catalog/)
- [MCP Gateway](https://docs.docker.com/ai/mcp-catalog-and-toolkit/mcp-gateway/)

---

# Docker MCP Catalog and Toolkit

> Learn about Docker's MCP catalog on Docker Hub

# Docker MCP Catalog and Toolkit

   Table of contents

---

Availability: Beta

[Model Context Protocol](https://modelcontextprotocol.io/introduction) (MCP) is
an open protocol that standardizes how AI applications access external tools
and data sources. By connecting LLMs to local development tools, databases,
APIs, and other resources, MCP extends their capabilities beyond their base
training.

Through a client-server architecture, applications such as Claude, ChatGPT, and
[Gordon](https://docs.docker.com/ai/gordon/) act as clients that send requests to MCP
servers, which then process these requests and deliver the necessary context to
AI models.

MCP servers extend the utility of AI applications, but running servers locally
also presents several operational challenges. Typically, servers must be
installed directly on your machine and configured individually for each
application. Running untrusted code locally requires careful vetting, and the
responsibility of keeping servers up-to-date and resolving environment
conflicts falls on the user.

## Docker MCP features

Docker provides three integrated components that address the challenges of
running local MCP servers:

MCP CatalogA curated collection of verified MCP servers, packaged and distributed as
container images via Docker Hub. All servers are versioned, come with full
provenance and SBOM metadata, and are continuously maintained and updated with
security patches.MCP ToolkitA graphical interface in Docker Desktop for discovering, configuring, and
managing MCP servers. The Toolkit provides a unified way to search for servers,
handle authentication, and connect them to AI applications.MCP GatewayThe core open source component that powers the MCP Toolkit. The MCP Gateway
manages MCP containers provides a unified endpoint that exposes your enabled
servers to all AI applications you use.

This integrated approach ensures:

- Simplified discovery and setup of trusted MCP servers from a curated catalog
  of tools
- Centralized configuration and authentication from within Docker Desktop
- A secure, consistent execution environment by default
- Improved performance since applications can share a single server runtime,
  compared to having to spin up duplicate servers for each application.

![MCP overview](https://docs.docker.com/ai/mcp-catalog-and-toolkit/images/mcp-overview.svg)  ![MCP overview](https://docs.docker.com/ai/mcp-catalog-and-toolkit/images/mcp-overview.svg)

## Learn more

[Get started with MCP ToolkitLearn how to quickly install and use the MCP Toolkit to set up servers and clients.](https://docs.docker.com/ai/mcp-catalog-and-toolkit/get-started/)[MCP CatalogLearn about the benefits of the MCP Catalog, how you can use it, and how you can contribute](https://docs.docker.com/ai/mcp-catalog-and-toolkit/catalog/)[MCP ToolkitLearn about the MCP Toolkit to manage MCP servers and clients](https://docs.docker.com/ai/mcp-catalog-and-toolkit/toolkit/)[Dynamic MCPDiscover and add MCP servers on-demand using natural language](https://docs.docker.com/ai/mcp-catalog-and-toolkit/dynamic-mcp/)[MCP GatewayLearn about the underlying technology that powers the MCP Toolkit](https://docs.docker.com/ai/mcp-catalog-and-toolkit/mcp-gateway/)[Docker Hub MCP serverExplore about the Docker Hub server for searching images, managing repositories, and more](https://docs.docker.com/ai/mcp-catalog-and-toolkit/hub-mcp/)
