# Migrating from legacy sandboxes and more

# Migrating from legacy sandboxes

> Migrate from container-based sandboxes to microVM-based sandboxes

# Migrating from legacy sandboxes

   Table of contents

---

Availability: Experimental
Requires: Docker Desktop
[4.58](https://docs.docker.com/desktop/release-notes/#4580) or later

Docker Desktop 4.58 introduces microVM-based sandboxes, replacing the previous
container-based implementation. This guide helps you migrate from legacy
sandboxes to the new architecture.

## What changed

Docker Sandboxes now run in lightweight microVMs instead of containers. Each
sandbox has a private Docker daemon, better isolation, and network filtering
policies.

> Note
>
> If you need to use legacy container-based sandboxes, install
> [Docker Desktop 4.57](https://docs.docker.com/desktop/release-notes/#4570).

After upgrading to Docker Desktop 4.58:

- Old sandboxes don't appear in `docker sandbox ls`
- They still exist as regular Docker containers and volumes
- You can see them with `docker ps -a` and `docker volume ls`
- Old sandboxes won't work with the new CLI commands
- Running `docker sandbox run` creates a new microVM-based sandbox

## Migration options

Choose the approach that fits your situation:

### Option 1: Start fresh (recommended)

This is the simplest approach for experimental features. You'll recreate your
sandbox with the new architecture.

1. Note any important configuration or installed packages in your old sandbox.
2. Remove the old sandbox containers:
  ```console
  $ docker rm -f $(docker ps -q -a --filter="label=docker/sandbox=true")
  ```
3. Remove the credential volume:
  ```console
  $ docker volume rm docker-claude-sandbox-data
  ```
4. Create a new microVM sandbox:
  ```console
  $ docker sandbox create claude ~/project
  $ docker sandbox run <sandbox-name>
  ```
5. Reinstall dependencies. Ask the agent to install needed tools:
  ```plaintext
  You: "Install all the tools needed to build and test this project"
  Claude: [Installs tools]
  ```

What you lose:

- API keys (re-authenticate on first run, or set `ANTHROPIC_API_KEY`)
- Installed packages (reinstall via the agent)
- Custom configuration (reconfigure as needed)

What you gain:

- Better isolation (microVM versus container)
- Private Docker daemon for test containers
- Network filtering policies
- Improved security

### Option 2: Migrate configuration

If you have extensive customization, preserve your setup by creating a custom
template.

1. Inspect your old sandbox to see what's installed:
  ```console
  $ docker exec <old-sandbox-container> dpkg -l
  ```
2. Create a custom template with your tools:
  ```dockerfile
  FROM docker/sandbox-templates:claude-code
  USER root
  # Install your tools
  RUN apt-get update && apt-get install -y \
      build-essential \
      nodejs \
      npm
  # Install language-specific packages
  RUN npm install -g typescript eslint
  # Add any custom configuration
  ENV EDITOR=vim
  USER agent
  ```
3. Build your template:
  ```console
  $ docker build -t my-sandbox-template:v1 .
  ```
4. Create a new sandbox with your template:
  ```console
  $ docker sandbox create --template my-sandbox-template:v1 \
      --load-local-template \
      claude ~/project
  ```
5. Run the sandbox:
  ```console
  $ docker sandbox run <sandbox-name>
  ```

If you want to share this template with your team, push it to a registry. See
[Custom templates](https://docs.docker.com/ai/sandboxes/templates/) for details.

## Cleanup old resources

After migrating, clean up legacy containers and volumes:

Remove specific sandbox:

```console
$ docker rm -f <old-sandbox-container>
$ docker volume rm docker-claude-sandbox-data
```

Remove all stopped containers and unused volumes:

```console
$ docker container prune
$ docker volume prune
```

> Warning
>
> `docker volume prune` removes ALL unused volumes, not just sandbox volumes.
> Make sure you don't have other important unused volumes before running this
> command.

## Understanding the differences

### Architecture

Old (container-based):

- Sandboxes were Docker containers
- Appeared in `docker ps`
- Mounted host Docker socket for container access
- Stored credentials in Docker volume

New (microVM-based):

- Sandboxes are lightweight microVMs
- Use `docker sandbox ls` to see them
- Private Docker daemon inside VM
- Credentials via `ANTHROPIC_API_KEY` environment variable or interactive auth

### CLI changes

Old command structure:

```console
$ docker sandbox run ~/project
```

New command structure:

```console
$ docker sandbox run claude ~/project
```

The agent name (`claude`, `codex`, `gemini`, `cagent`, `kiro`) is now a
required parameter when creating sandboxes, and you run the sandbox by name.

---

# Network policies

> Configure network filtering policies to control outbound HTTP and HTTPS access from sandboxed agents.

# Network policies

   Table of contents

---

Availability: Experimental
Requires: Docker Desktop
[4.58](https://docs.docker.com/desktop/release-notes/#4580) or later

Network policies control what external resources a sandbox can access through
an HTTP/HTTPS filtering proxy. Use policies to prevent agents from accessing
internal networks, enforce compliance requirements, or restrict internet access
to specific services.

Each sandbox has a filtering proxy that enforces policies for outbound HTTP and
HTTPS traffic. Connection to external services over other protocols, such as
raw TCP and UDP connections, are blocked. All agent communication must go
through the HTTP proxy or remain contained within the sandbox.

The proxy runs on an ephemeral port on your host, but from the agent
container's perspective it is accessible at `host.docker.internal:3128`.

### Security considerations

Use network policies as one layer of security, not the only layer. The microVM
boundary provides the primary isolation. Network policies add an additional
control for HTTP/HTTPS traffic.

The network filtering restricts which domains processes can connect to, but
doesn't inspect the traffic content. When configuring policies:

- Allowing broad domains like `github.com` permits access to any content on
  that domain, including user-generated content. Agents could use these as
  channels for data exfiltration.
- Domain fronting techniques may bypass filters by routing traffic through
  allowed domains. This is inherent to HTTPS proxying.

Only allow domains you trust with your data. You're responsible for
understanding what your policies permit.

## How network filtering works

Each sandbox has an HTTP/HTTPS proxy running on your host. The proxy is
accessible from inside the sandbox at `host.docker.internal:3128`.

When an agent makes HTTP or HTTPS requests, the proxy:

1. Checks the policy rules against the host in the request. If the host is
  blocked, the request is stopped immediately
2. Connects to the server. If the host was not explicitly allowed, checks the
  server's IP address against BlockCIDR rules

For example, `localhost` is not in the default allow-list, but it's allowed by the
default "allow" policy. Because it's not explicitly allowed, the proxy then checks
the resolved IP addresses (`127.0.0.1` or `::1`) against the BlockCIDR rules.
Since `127.0.0.1/8` and `::1/128` are both blocked by default, this catches any
DNS aliases for localhost like `ip6-localhost`.

If an agent needs access to a service on localhost, include a port number in
the allow-list (e.g., `localhost:1234`).

HTTP requests to `host.docker.internal` are rewritten to `localhost`, so only
the name `localhost` will work in the allow-list.

## Monitor network activity

View what your agent is accessing and whether requests are being blocked:

```console
$ docker sandbox network log
```

Network logs help you understand agent behavior and define policies.

## Applying policies

Use `docker sandbox network proxy` to configure network policies for your
sandboxes. The sandbox must be running when you apply policy changes. Changes
take effect immediately and persist across sandbox restarts.

### Example: Block internal networks

Prevent agents from accessing your local network, Docker networks, and cloud
metadata services. It prevents accidental access to internal services while
allowing agents to install packages and access public APIs.

```console
$ docker sandbox network proxy my-sandbox \
  --policy allow \
  --block-cidr 10.0.0.0/8 \
  --block-cidr 172.16.0.0/12 \
  --block-cidr 192.168.0.0/16 \
  --block-cidr 127.0.0.0/8
```

This policy:

- Allows internet access
- Blocks RFC 1918 private networks (10.x.x.x, 172.16-31.x.x, 192.168.x.x)
- Blocks localhost (127.x.x.x)

> Note
>
> These CIDR blocks are already blocked by default. The example above shows how
> to explicitly configure them if needed. The default policy blocks:
>
>
>
> - `10.0.0.0/8`
> - `127.0.0.0/8`
> - `169.254.0.0/16`
> - `172.16.0.0/12`
> - `192.168.0.0/16`
> - `::1/128`
> - `fc00::/7`
> - `fe80::/10`

### Example: Restrict to package managers only

For strict control, use a denylist policy that only allows package repositories:

```console
$ docker sandbox network proxy my-sandbox \
  --policy deny \
  --allow-host "*.npmjs.org" \
  --allow-host "*.pypi.org" \
  --allow-host "files.pythonhosted.org" \
  --allow-host "*.rubygems.org" \
  --allow-host github.com
```

> Note
>
> This policy would block the backend of your AI coding agent (e.g., for Claude
> Code: `xyz.anthropic.com`). Make sure you also include hostnames that the
> agent requires.

The agent can install dependencies but can't access arbitrary internet
resources. This is useful for CI/CD environments or when running untrusted code.

### Example: Allow AI APIs and development tools

Combine AI service access with package managers and version control:

```console
$ docker sandbox network proxy my-sandbox \
  --policy deny \
  --allow-host api.anthropic.com \
  --allow-host "*.npmjs.org" \
  --allow-host "*.pypi.org" \
  --allow-host github.com \
  --allow-host "*.githubusercontent.com"
```

This allows agents to call AI APIs, install packages, and fetch code from
GitHub while blocking other internet access.

### Example: Allow specific APIs while blocking subdomains

Use port-specific rules and subdomain patterns for fine-grained control:

```console
$ docker sandbox network proxy my-sandbox \
  --policy deny \
  --allow-host api.example.com:443 \
  --allow-host cdn.example.com \
  --allow-host "*.storage.example.com:443"
```

This policy allows:

- Requests to `api.example.com` on port 443 (typically
  `https://api.example.com`)
- Requests to `cdn.example.com` on any port
- Requests to any subdomain of `storage.example.com` on port 443, like
  `us-west.storage.example.com:443` or `eu-central.storage.example.com:443`

Requests to `example.com` (any port), `www.example.com` (any port), or
`api.example.com:8080` would all be blocked because none match the specific
patterns.

To allow both a domain and all its subdomains, specify both patterns:

```console
$ docker sandbox network proxy my-sandbox \
  --policy deny \
  --allow-host example.com \
  --allow-host "*.example.com"
```

## Policy modes: allowlist versus denylist

Policies have two modes that determine default behavior.

### Allowlist mode

Default: Allow all traffic, block specific destinations.

```console
$ docker sandbox network proxy my-sandbox \
  --policy allow \
  --block-cidr 192.0.2.0/24 \
  --block-host example.com
```

Use allowlist mode when you want agents to access most resources but need to
block specific networks or domains. This is less restrictive and works well for
development environments where the agent needs broad internet access.

### Denylist mode

Default: Block all traffic, allow specific destinations.

```console
$ docker sandbox network proxy my-sandbox \
  --policy deny \
  --allow-host api.anthropic.com \
  --allow-host "*.npmjs.org"
```

Use denylist mode when you want tight control over external access. This
requires explicitly allowing each service the agent needs, making it more
secure but also more restrictive. Good for production deployments, CI/CD
pipelines, or untrusted code.

### Domain and CIDR matching

Domain patterns support exact matches, wildcards, and port specifications:

- `example.com` matches only that exact domain (any port)
- `example.com:443` matches requests to `example.com` on port 443 (the default
  HTTPS port)
- `*.example.com` matches all subdomains like `api.example.com` or
  `www.example.com`
- `*.example.com:443` matches requests to any subdomain on port 443

Important pattern behaviors:

- `example.com` does NOT match subdomains. A request to `api.example.com`
  won't match a rule for `example.com`.
- `*.example.com` does NOT match the root domain. A request to `example.com`
  won't match a rule for `*.example.com`.
- To allow both a domain and its subdomains, specify both patterns:
  `example.com` and `*.example.com`.

When multiple patterns could match a request, the most specific pattern wins:

1. Exact hostname and port: `api.example.com:443`
2. Exact hostname, any port: `api.example.com`
3. Wildcard patterns (longest match first): `*.api.example.com:443`,
  `*.api.example.com`, `*.example.com:443`, `*.example.com`
4. Catch-all wildcards: `*:443`, `*`
5. Default policy (allow or deny)

This specificity lets you block broad patterns while allowing specific
exceptions. For example, you can block `example.com` and `*.example.com` but
allow `api.example.com:443`.

CIDR blocks match IP addresses after DNS resolution:

- `192.0.2.0/24` blocks all 192.0.2.x addresses
- `198.51.100.0/24` blocks all 198.51.100.x addresses
- `203.0.113.0/24` blocks all 203.0.113.x addresses

When you block or allow a domain, the proxy resolves it to IP addresses and
checks those IPs against CIDR rules. This means blocking a CIDR range affects
any domain that resolves to an IP in that range.

## Bypass mode for HTTPS tunneling

By default, the proxy acts as a man-in-the-middle for HTTPS connections,
terminating TLS and re-encrypting traffic with its own certificate authority.
This allows the proxy to enforce policies and inject authentication credentials
for certain services. The sandbox container trusts the proxy's CA certificate.

Some applications use certificate pinning or other techniques that don't work
with MITM proxies. For these cases, use bypass mode to tunnel HTTPS traffic
directly without inspection:

```console
$ docker sandbox network proxy my-sandbox \
  --bypass-host api.service-with-pinning.com
```

You can also bypass traffic to specific IP ranges:

```console
$ docker sandbox network proxy my-sandbox \
  --bypass-cidr 203.0.113.0/24
```

When traffic is bypassed, the proxy:

- Acts as a simple TCP tunnel without inspecting content
- Cannot inject authentication credentials into requests
- Cannot detect domain fronting or other evasion techniques
- Still enforces domain and port matching based on the initial connection

Use bypass mode only when necessary. Bypassed traffic loses the visibility and
security benefits of MITM inspection. If you bypass broad domains like
`github.com`, the proxy has no visibility into what the agent accesses on that
domain.

## Policy persistence

Network policies are stored in JSON configuration files.

### Per-sandbox configuration

When you run `docker sandbox network proxy my-sandbox`, the command updates the
configuration for that specific sandbox only. The policy is persisted to
`~/.docker/sandboxes/vm/my-sandbox/proxy-config.json`.

The default policy (used when creating new sandboxes) remains unchanged unless
you modify it directly.

### Default configuration

The default network policy for new sandboxes is stored at
`~/.sandboxd/proxy-config.json`. This file is created automatically when the
first sandbox starts, but only if it doesn't already exist.

The current default policy is `allow`, which permits all outbound connections
except to blocked CIDR ranges (private networks, localhost, and cloud metadata
services). This default will change to `deny` in a future release to provide
more restrictive defaults.

You can modify the default policy:

1. Edit `~/.sandboxd/proxy-config.json` directly
2. Or copy a sandbox policy to the default location:
  ```console
  $ cp ~/.docker/sandboxes/vm/my-sandbox/proxy-config.json ~/.sandboxd/proxy-config.json
  ```

Review and customize the default policy to match your security requirements
before creating new sandboxes. Once created, the default policy file won't be
modified by upgrades, preserving your custom configuration.

## Next steps

- [Architecture](https://docs.docker.com/ai/sandboxes/architecture/)
- [Using sandboxes effectively](https://docs.docker.com/ai/sandboxes/workflows/)
- [Custom templates](https://docs.docker.com/ai/sandboxes/templates/)

---

# Custom templates

> Create custom sandbox templates to standardize development environments with pre-installed tools and configurations.

# Custom templates

   Table of contents

---

Availability: Experimental
Requires: Docker Desktop
[4.58](https://docs.docker.com/desktop/release-notes/#4580) or later

Custom templates let you create reusable sandbox environments with
pre-installed tools and configuration. Instead of asking the agent to install
packages each time, build a template with everything ready.

## When to use custom templates

Use custom templates when:

- Multiple team members need the same environment
- You're creating many sandboxes with identical tooling
- Setup involves complex steps that are tedious to repeat
- You need specific versions of tools or libraries

For one-off work or simple setups, use the default template and ask the agent
to install what's needed.

## Building a template

Start from Docker's official sandbox templates:

```dockerfile
FROM docker/sandbox-templates:claude-code

USER root

# Install system packages
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install development tools
RUN pip3 install --no-cache-dir \
    pytest \
    black \
    pylint

USER agent
```

Official templates include the agent binary, Ubuntu base, development tools
(Git, Docker CLI, Node.js, Python, Go), and the non-root `agent` user with
sudo access.

### The USER pattern

Switch to `root` for system-level installations, then back to `agent` at the
end. The base template defaults to `USER agent`, so you need to explicitly
switch to root for package installations. Always switch back to `agent` before
the end of your Dockerfile so the agent runs with the correct permissions.

### Using templates

Build your template:

```console
$ docker build -t my-template:v1 .
```

Then choose how to use it:

Option 1: Load from local images (quick, for personal use)

```console
$ docker sandbox create --template my-template:v1 \
    --load-local-template \
    claude ~/project
$ docker sandbox run <sandbox-name>
```

The `--load-local-template` flag loads the image from your local Docker daemon
into the sandbox VM. This works for quick iteration and personal templates.

Option 2: Push to a registry (for sharing and persistence)

```console
$ docker tag my-template:v1 myorg/my-template:v1
$ docker push myorg/my-template:v1
$ docker sandbox create --template myorg/my-template:v1 claude ~/project
$ docker sandbox run <sandbox-name>
```

Pushing to a registry makes templates available to your team and persists them
beyond your local machine.

## Example: Node.js template

```dockerfile
FROM docker/sandbox-templates:claude-code

USER root

RUN apt-get update && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 20 LTS
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install common tools
RUN npm install -g \
    typescript@5.1.6 \
    eslint@8.46.0 \
    prettier@3.0.0

USER agent
```

Pin versions for reproducible builds.

## Using standard images

You can use standard Docker images (like `python:3.11` or `node:20`) as a
base, but they don't include agent binaries or sandbox configuration.

Using a standard image directly creates the sandbox but fails at runtime:

```console
$ docker sandbox create --template python:3-slim claude ~/project
✓ Created sandbox claude-sandbox-2026-01-16-170525 in VM claude-project

$ docker sandbox run claude-project
agent binary "claude" not found in sandbox: verify this is the correct sandbox type
```

To use a standard image, you'd need to install the agent binary, add sandbox
dependencies, configure the shell, and set up the `agent` user. Building from
`docker/sandbox-templates:claude-code` is simpler.

## Sharing with teams

Push templates to a registry and version them:

```console
$ docker build -t myorg/sandbox-templates:python-v1.0 .
$ docker push myorg/sandbox-templates:python-v1.0
```

Team members can then use the template:

```console
$ docker sandbox create --template myorg/sandbox-templates:python-v1.0 claude ~/project
```

Using version tags (`:v1.0`, `:v2.0`) instead of `:latest` ensures stability
across your team.

## Next steps

- [Using sandboxes effectively](https://docs.docker.com/ai/sandboxes/workflows/)
- [Architecture](https://docs.docker.com/ai/sandboxes/architecture/)
- [Network policies](https://docs.docker.com/ai/sandboxes/network-policies/)

---

# Troubleshooting

> Resolve common issues when sandboxing agents locally.

# Troubleshooting

   Table of contents

---

Availability: Experimental
Requires: Docker Desktop
[4.58](https://docs.docker.com/desktop/release-notes/#4580) or later

This guide helps you resolve common issues when sandboxing Claude Code locally.

## 'sandbox' is not a docker command

When you run `docker sandbox`, you see an error saying the command doesn't exist.

This means the CLI plugin isn't installed or isn't in the correct location. To fix:

1. Verify the plugin exists:
  ```console
  $ ls -la ~/.docker/cli-plugins/docker-sandbox
  ```
  The file should exist and be executable.
2. If using Docker Desktop, restart it to detect the plugin.

## "Experimental Features" needs to be enabled by your administrator

You see an error about beta features being disabled when trying to use sandboxes.

This happens when your Docker Desktop installation is managed by an
administrator who has locked settings. If your organization uses
[Settings Management](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/),
ask your administrator to
[allow beta features](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/configure-json-file/#beta-features):

```json
{
  "configurationFileVersion": 2,
  "allowBetaFeatures": {
    "locked": false,
    "value": true
  }
}
```

## Authentication failure

Claude can't authenticate, or you see API key errors.

The API key is likely invalid, expired, or not configured correctly.

## Workspace contains API key configuration

You see a warning about conflicting credentials when starting a sandbox.

This happens when your workspace has a `.claude.json` file with a `primaryApiKey` field. Choose one of these approaches:

- Remove the `primaryApiKey` field from your `.claude.json`:
  ```json
  {
    "apiKeyHelper": "/path/to/script",
    "env": {
      "ANTHROPIC_BASE_URL": "https://api.anthropic.com"
    }
  }
  ```
- Or proceed with the warning - workspace credentials will be ignored in favor of sandbox credentials.

## Permission denied when accessing workspace files

Claude or commands fail with "Permission denied" errors when accessing files in the workspace.

This usually means the workspace path isn't accessible to Docker, or file permissions are too restrictive.

If using Docker Desktop:

1. Check File Sharing settings at Docker Desktop → **Settings** → **Resources** → **File Sharing**.
2. Ensure your workspace path (or a parent directory) is listed under Virtual file shares.
3. If missing, click "+" to add the directory containing your workspace.
4. Restart Docker Desktop.

For all platforms, verify file permissions:

```console
$ ls -la <workspace>
```

Ensure files are readable. If needed:

```console
$ chmod -R u+r <workspace>
```

Also verify the workspace path exists:

```console
$ cd <workspace>
$ pwd
```

## Sandbox crashes on Windows when launching multiple sandboxes

On Windows, launching too many sandboxes simultaneously can cause crashes.

If this happens, recover by closing the OpenVMM processes:

1. Open Task Manager (Ctrl+Shift+Esc).
2. Find all `docker.openvmm.exe` processes.
3. End each process.
4. Restart Docker Desktop if needed.

To avoid this issue, launch sandboxes one at a time rather than creating
multiple sandboxes concurrently.

---

# Using sandboxes effectively

> Best practices and common workflows for Docker Sandboxes including dependency management, testing, and multi-project setups.

# Using sandboxes effectively

   Table of contents

---

Availability: Experimental
Requires: Docker Desktop
[4.58](https://docs.docker.com/desktop/release-notes/#4580) or later

This guide covers practical patterns for working with sandboxed agents.

## Basic workflow

Create a sandbox for your project:

```console
$ cd ~/my-project
$ docker sandbox run claude .
```

The sandbox persists. Stop and restart it without losing installed packages or
configuration:

```console
$ docker sandbox run <sandbox-name>  # Reconnect later
```

## Installing dependencies

Ask the agent to install what's needed:

```plaintext
You: "Install pytest and black"
Claude: [Installs packages via pip]

You: "Install build-essential"
Claude: [Installs via apt]
```

The agent has sudo access. Installed packages persist for the sandbox lifetime.
This works for system packages, language packages, and development tools.

For teams or repeated setups, use [Custom templates](https://docs.docker.com/ai/sandboxes/templates/) to
pre-install tools.

## Docker inside sandboxes

Agents can build images, run containers, and use Docker Compose. Everything
runs inside the sandbox's private Docker daemon.

### Testing containerized apps

```plaintext
You: "Build the Docker image and run the tests"

Claude: *runs*
  docker build -t myapp:test .
  docker run myapp:test npm test
```

Containers started by the agent run inside the sandbox, not on your host. They
don't appear in your host's `docker ps`.

### Multi-container stacks

```plaintext
You: "Start the application with docker-compose and run integration tests"

Claude: *runs*
  docker-compose up -d
  docker-compose exec api pytest tests/integration
  docker-compose down
```

Remove the sandbox, and all images, containers, and volumes are deleted.

## What persists

While a sandbox exists:

- Installed packages (apt, pip, npm, etc.)
- Docker images and containers inside the sandbox
- Configuration changes
- Command history

When you remove a sandbox:

- Everything inside is deleted
- Your workspace files remain on your host (synced back)

To preserve a configured environment, create a [Custom template](https://docs.docker.com/ai/sandboxes/templates/).

## Security considerations

Agents can create and modify any files in your mounted workspace, including
scripts, configuration files, and hidden files.

After an agent works in a workspace, review changes before performing actions
on your host that might execute code:

- Committing changes (executes Git hooks)
- Opening the workspace in an IDE (may auto-run scripts or extensions)
- Running scripts or executables the agent created or modified

Review what changed:

```console
$ git status                        # See modified and new files
$ git diff                          # Review changes to tracked files
```

Check for untracked files and be aware that some changes, like Git hooks in
`.git/hooks/`, won't appear in standard diffs.

This is the same trust model used by editors like Visual Studio Code, which
warn when opening new workspaces for similar reasons.

## Named sandboxes

Use meaningful names for sandboxes you'll reuse:

```console
$ docker sandbox run --name myproject claude ~/project
```

Create multiple sandboxes for the same workspace:

```console
$ docker sandbox create --name dev claude ~/project
$ docker sandbox create --name staging claude ~/project
$ docker sandbox run dev
```

Each maintains separate packages, Docker images, and state, but share the
workspace files.

## Debugging

Access the sandbox directly with an interactive shell:

```console
$ docker sandbox exec -it <sandbox-name> bash
```

Inside the shell, you can inspect the environment, manually install packages,
or check Docker containers:

```console
agent@sandbox:~$ docker ps
agent@sandbox:~$ docker images
```

List all sandboxes:

```console
$ docker sandbox ls
```

## Managing multiple projects

Create sandboxes for different projects:

```console
$ docker sandbox create claude ~/project-a
$ docker sandbox create claude ~/project-b
$ docker sandbox create claude ~/work/client-project
```

Each sandbox is completely isolated. Switch between them by running the
appropriate sandbox name.

Remove unused sandboxes to reclaim disk space:

```console
$ docker sandbox rm <sandbox-name>
```

## Next steps

- [Custom templates](https://docs.docker.com/ai/sandboxes/templates/)
- [Architecture](https://docs.docker.com/ai/sandboxes/architecture/)
- [Network policies](https://docs.docker.com/ai/sandboxes/network-policies/)

---

# Docker Sandboxes

> Run AI agents in isolated environments

# Docker Sandboxes

   Table of contents

---

Availability: Experimental
Requires: Docker Desktop
[4.58](https://docs.docker.com/desktop/release-notes/#4580) or later

Docker Sandboxes lets you run AI coding agents in isolated environments on your
machine. If you're building with agents like Claude Code, Sandboxes provides a
secure way to give agents autonomy without compromising your system.

## Why use Docker Sandboxes

AI agents need to execute commands, install packages, and test code. Running
them directly on your host machine means they have full access to your files,
processes, and network. Docker Sandboxes isolates agents in microVMs, each with
its own Docker daemon. Agents can spin up test containers and modify their
environment without affecting your host.

You get:

- Agent autonomy without host system risk
- Private Docker daemon for running test containers
- File sharing between host and sandbox
- Network access control

For a comparison between Docker Sandboxes and other approaches to isolating
coding agents, see [Comparison to alternatives](https://docs.docker.com/ai/sandboxes/architecture/#comparison-to-alternatives).

> Note
>
> MicroVM-based sandboxes require macOS or Windows (experimental). Linux users
> can use legacy container-based sandboxes with
> [Docker Desktop 4.57](https://docs.docker.com/desktop/release-notes/#4570).

## How to use sandboxes

To create and run a sandbox:

```console
$ docker sandbox run claude ~/my-project
```

This command creates a sandbox for your workspace (`~/my-project`) and starts
the Claude Code agent inside it. The agent can now work with your code, install
tools, and run containers inside the isolated sandbox.

## How it works

Sandboxes run in lightweight microVMs with private Docker daemons. Each sandbox
is completely isolated - the agent runs inside the VM and can't access your
host Docker daemon, containers, or files outside the workspace.

Your workspace directory syncs between host and sandbox at the same absolute
path, so file paths in error messages match between environments.

Sandboxes don't appear in `docker ps` on your host because they're VMs, not
containers. Use `docker sandbox ls` to see them.

For technical details on the architecture, isolation model, and networking, see
[Architecture](https://docs.docker.com/ai/sandboxes/architecture/).

### Multiple sandboxes

Create separate sandboxes for different projects:

```console
$ docker sandbox run claude ~/project-a
$ docker sandbox run claude ~/project-b
```

Each sandbox is completely isolated from the others. Sandboxes persist until
you remove them, so installed packages and configuration stay available for
that workspace.

## Supported agents

Docker Sandboxes works with multiple AI coding agents:

- **Claude Code** - Anthropic's coding agent
- **Codex** - OpenAI's Codex agent (partial support; in development)
- **Gemini** - Google's Gemini agent (partial support; in development)
- **cagent** - Docker's
  [cagent](https://docs.docker.com/ai/cagent/) (partial support; in development)
- **Kiro** - by AWS (partial support; in development)

## Get started

Head to the [Get started guide](https://docs.docker.com/ai/sandboxes/get-started/) to run your first sandboxed agent.

## Troubleshooting

See [Troubleshooting](https://docs.docker.com/ai/sandboxes/troubleshooting/) for common configuration errors, or
report issues on the [Docker Desktop issue tracker](https://github.com/docker/desktop-feedback).
