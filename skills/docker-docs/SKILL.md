---
name: "docker-docs"
description: "Scraped from https://docs.docker.com/ Source: https://docs.docker.com. Use when questions involve: accounts, admin, ai, billing, build, build cloud."
---

# Docker Docs

> Official documentation: https://docs.docker.com

## Overview

This skill provides comprehensive documentation for docker docs.

**Total references:** 215 files (~1,665,395 tokens)

**Topics covered:**
The anatomy of a context, Optional steps, Callouts, Part one Build the foundations, Step 3 Compare with the other images, Dockerfile frontend, Recursive mounts, Set up role mapping, View task state, Update the application, Integration with firewalld, Enable immutable tags...

## Reference Files

Load only the reference files relevant to the user's question:

### Accounts

- **[Create a Docker account and more](references/accounts.md)** (~2,265 tokens)
  - Topics: Create an account, Sign in to your account, Reset your password

### Admin

- **[Create a company and more](references/admin-1.md)** (~6,346 tokens)
  - Topics: Prerequisites, Create a company, Next steps
- **[Insights and more](references/admin-2.md)** (~7,390 tokens)
  - Topics: Prerequisites, View Insights for organization users, Export Docker Desktop user data
- **[Create your organization and more](references/admin-3.md)** (~1,037 tokens)
  - Topics: Prerequisites, Create an organization, View an organization

### Ai

- **[Best practices and more](references/ai-1.md)** (~7,489 tokens)
  - Topics: Handling large command outputs, Structuring agent teams, Optimizing RAG performance
- **[Model providers and more](references/ai-2.md)** (~5,297 tokens)
  - Topics: Supported providers, Anthropic, OpenAI
- **[Configuration file reference and more](references/ai-3.md)** (~6,178 tokens)
  - Topics: File structure, Agents, Models
- **[Toolsets reference and more](references/ai-4.md)** (~7,941 tokens)
  - Topics: How agents use tools, Tool types, Configuration
- **[Configure MCP servers with YAML and more](references/ai-5.md)** (~7,270 tokens)
  - Topics: Use advanced MCP server features, Whats next, Key features
- **[Get started with Docker MCP Toolkit and more](references/ai-6.md)** (~6,747 tokens)
  - Topics: Setup, Install MCP servers, Connect clients
- **[DMR REST API and more](references/ai-7.md)** (~7,337 tokens)
  - Topics: Determine the base URL, Supported APIs, OpenAI-compatible API
- **[Inference engines and more](references/ai-8.md)** (~7,755 tokens)
  - Topics: Engine comparison, llamacpp, vLLM
- **[Migrating from legacy sandboxes and more](references/ai-9.md)** (~5,813 tokens)
  - Topics: What changed, Migration options, Cleanup old resources

### Billing

- **[Use 3D Secure authentication for Docker billing and more](references/billing.md)** (~6,258 tokens)
  - Topics: How it works, When you need to verify, Troubleshooting payment verification

### Build

- **[Building with Bake from a Compose file and more](references/build-1.md)** (~6,136 tokens)
  - Topics: envfile, Extension field withx-bake, Pinning alpine image
- **[Bake file reference](references/build-2.md)** (~7,160 tokens)
  - Topics: File format, Syntax, Target
- **[Remote Bake file definition and more](references/build-3.md)** (~7,365 tokens)
  - Topics: Use the local context with a remote definition, Specify the Bake definition to use, Combine local and remote Bake definitions
- **[Bake targets and more](references/build-4.md)** (~7,731 tokens)
  - Topics: Default target, Target properties, Grouping targets
- **[Manage builders and more](references/build-5.md)** (~2,228 tokens)
  - Topics: Create a new builder, List available builders, Inspect a builder
- **[Building best practices](references/build-6.md)** (~5,939 tokens)
  - Topics: Use multi-stage builds, Choose the right base image, Rebuild your images often
- **[Container Device Interface (CDI) and more](references/build-7.md)** (~7,276 tokens)
  - Topics: Getting started, Building with a simple CDI specification, Set up a container builder with GPU support
- **[Build secrets and more](references/build-8.md)** (~7,289 tokens)
  - Topics: Types of build secrets, Using build secrets, Secret mounts
- **[buildkitd.toml and more](references/build-9.md)** (~6,929 tokens)
  - Topics: Overview, LLB, Frontend
- **[Cache storage backends and more](references/build-10.md)** (~7,372 tokens)
  - Topics: Backends, Command syntax, Multiple caches
- **[Checking your build configuration and more](references/build-11.md)** (~7,501 tokens)
  - Topics: How build checks work, Build with checks, Check a build without building
- **[Multi and more](references/build-12.md)** (~4,964 tokens)
  - Topics: Build and load multi-platform images, Distribute build across multiple runners, Pin image to a tag
- **[Build context and more](references/build-13.md)** (~7,740 tokens)
  - Topics: What is a build context, Local context, Remote context
- **[Local and tar exporters and more](references/build-14.md)** (~6,477 tokens)
  - Topics: Synopsis, Multi-platform builds with local exporter, Further reading
- **[SLSA definitions and more](references/build-15.md)** (~7,928 tokens)
  - Topics: SLSA v1, SLSA v02, Create provenance attestations
- **[Policy templates and examples and more](references/build-16.md)** (~6,948 tokens)
  - Topics: How to use these examples, Getting started, Production templates
- **[Using build policies and more](references/build-17.md)** (~6,783 tokens)
  - Topics: Prerequisites, Policy development workflow, Using policies withdocker build

### Build Cloud

- **[Builder settings and more](references/build-cloud.md)** (~5,859 tokens)
  - Topics: Storage and cache management, Private resource access, Firewall

### Compose

- **[Customize Compose Bridge and more](references/compose-1.md)** (~7,818 tokens)
  - Topics: How it works, Customize the default templates, Use the default Compose Bridge transformation
- **[Environment variables precedence in Docker Compose and more](references/compose-2.md)** (~7,642 tokens)
  - Topics: Simple example, Advanced example, Next steps
- **[Run Docker Compose services with GPU access and more](references/compose-3.md)** (~7,784 tokens)
  - Topics: Enabling GPU access to service containers, Access specific devices, Services lifecycle hooks
- **[Using profiles with Compose and more](references/compose-4.md)** (~7,900 tokens)
  - Topics: Assigning profiles to services, Start specific profiles, Auto-starting profiles and dependency resolution
- **[Frequently asked questions about Docker Compose and more](references/compose-5.md)** (~1,093 tokens)

### Contribute

- **[Writing checklist and more](references/contribute-1.md)** (~6,104 tokens)
  - Topics: Example, Markup, Examples
- **[Guidelines for writing Docker usage guides and more](references/contribute-2.md)** (~7,935 tokens)
  - Topics: Purpose of the guides, Audience, Metadata for guides
- **[UI elements in content](references/contribute-3.md)** (~587 tokens)
  - Topics: Format UI element names, Write task-focused instructions, Use correct prepositions with UI elements

### Desktop

- **[containerd image store and more](references/desktop-1.md)** (~7,105 tokens)
  - Topics: What iscontainerd, What is thecontainerdimage store, Enable the containerd image store
- **[Wasm workloads and more](references/desktop-2.md)** (~3,755 tokens)
  - Topics: Turn on Wasm workloads, Usage examples, Troubleshooting
- **[Docker Desktop release notes](references/desktop-3.md)** (~39,633 tokens)
  - Topics: 4581, 4580, 4570
- **[How to back up and restore your Docker Desktop data and more](references/desktop-4.md)** (~7,056 tokens)
  - Topics: If Docker Desktop is functioning normally, If Docker Desktop fails to start, General
- **[Install Docker Desktop on Debian and more](references/desktop-5.md)** (~7,863 tokens)
  - Topics: Prerequisites, Install Docker Desktop, Launch Docker Desktop
- **[Understand permission requirements for Docker Desktop on Mac and more](references/desktop-6.md)** (~7,403 tokens)
  - Topics: Permission requirements, Installing from the command line, Privileged helper
- **[General FAQs for Desktop and more](references/desktop-7.md)** (~6,650 tokens)
  - Topics: Error message, Possible cause, Solution
- **[Troubleshoot topics for Docker Desktop and more](references/desktop-8.md)** (~7,845 tokens)
  - Topics: Topics for all platforms, Topics for Linux and Mac, Topics for Mac
- **[Explore the Containers view in Docker Desktop and more](references/desktop-9.md)** (~7,387 tokens)
  - Topics: Container actions, Resource usage, Inspect a container

### Dhi

- **[Attestations and more](references/dhi-1.md)** (~7,624 tokens)
  - Topics: What is an attestation, Why are attestations important, How Docker Hardened Images and charts use attestations
- **[Software Bill of Materials (SBOMs) and more](references/dhi-2.md)** (~7,868 tokens)
  - Topics: What is an SBOM, Why are SBOMs important, Docker Hardened Image SBOMs
- **[Understanding roles and responsibilities for Docker Hardened Images and more](references/dhi-3.md)** (~7,420 tokens)
  - Topics: Releases, Patching, Testing
- **[Customize a Docker Hardened Image or chartDHI Enterprise and more](references/dhi-4.md)** (~6,418 tokens)
  - Topics: Customize a Docker Hardened Image, Customize a DHI Helm chart, Edit or delete a customization
- **[Mirror a Docker Hardened Image repositoryDHI Enterprise and more](references/dhi-5.md)** (~7,872 tokens)
  - Topics: How to mirror, Mirror a DHI repository to Docker Hub, Mirror a DHI repository to a third-party registry
- **[How and more](references/dhi-6.md)** (~7,360 tokens)
  - Topics: Discover, Adopt, Evaluate

### Docker Hub

- **[Docker Hub catalogs and more](references/docker-hub-1.md)** (~6,923 tokens)
  - Topics: MCP Catalog, AI Models Catalog, Use-case
- **[Docker Hub release notes and more](references/docker-hub-2.md)** (~7,818 tokens)
  - Topics: 2025-02-18, 2024-12-12, 2024-03-23
- **[Set up automated builds and more](references/docker-hub-3.md)** (~7,659 tokens)
  - Topics: Configure automated builds, Advanced automated build options, Autobuild for teams
- **[Software artifacts on Docker Hub and more](references/docker-hub-4.md)** (~5,421 tokens)
  - Topics: What are OCI artifacts, Using OCI artifacts with Docker Hub, Examples
- **[Insights and analytics and more](references/docker-hub-5.md)** (~7,802 tokens)
  - Topics: Available reports, View the images analytics data, Extension analytics data
- **[Webhooks and more](references/docker-hub-6.md)** (~4,534 tokens)
  - Topics: Create a webhook, View webhook delivery history, Example webhook payload

### Engine

- **[Completion and more](references/engine-1.md)** (~4,730 tokens)
  - Topics: Bash, Zsh, Fish
- **[Resource constraints](references/engine-2.md)** (~3,412 tokens)
  - Topics: Memory, Understand the risks of running out of memory, CPU
- **[Running containers](references/engine-3.md)** (~9,308 tokens)
  - Topics: General form, Foreground and background, Container identification
- **[Runtime metrics and more](references/engine-4.md)** (~7,386 tokens)
  - Topics: Docker stats, Control groups, Tips for high-performance metric collection
- **[Live restore and more](references/engine-5.md)** (~5,057 tokens)
  - Topics: Enable live restore, Live restore during upgrades, Live restore upon restart
- **[Troubleshooting the Docker daemon and more](references/engine-6.md)** (~3,936 tokens)
  - Topics: Daemon, Networking, Volumes
- **[Deprecated Docker Engine features](references/engine-7.md)** (~10,141 tokens)
  - Topics: Feature deprecation policy, Deprecated engine features
- **[Plugin Config Version 1 of Plugin V2 and more](references/engine-8.md)** (~7,146 tokens)
  - Topics: Config Field Descriptions, Example Config, Types of plugins
- **[Docker volume plugins and more](references/engine-9.md)** (~6,990 tokens)
  - Topics: Changelog, Command-line changes, Create a VolumeDriver
- **[Install Docker Engine on Debian and more](references/engine-10.md)** (~5,717 tokens)
  - Topics: Prerequisites, Installation methods, Uninstall Docker Engine
- **[Install Docker Engine on Raspberry Pi OS (32 and more](references/engine-11.md)** (~7,904 tokens)
  - Topics: Prerequisites, Installation methods, Uninstall Docker Engine
- **[Install Docker Engine and more](references/engine-12.md)** (~7,170 tokens)
  - Topics: Installation procedures for supported platforms, Release channels, Support
- **[Graylog Extended Format logging driver and more](references/engine-13.md)** (~7,844 tokens)
  - Topics: Usage, Usage, Options
- **[Docker contexts and more](references/engine-14.md)** (~4,401 tokens)
  - Topics: Introduction, Prerequisites, The anatomy of a context
- **[Bridge network driver and more](references/engine-15.md)** (~5,664 tokens)
  - Topics: Differences between user-defined bridges and the default bridge, Options, Manage a user-defined bridge
- **[IPvlan network driver and more](references/engine-16.md)** (~7,506 tokens)
  - Topics: Options, Examples, Platform support and requirements
- **[Overlay network driver and more](references/engine-17.md)** (~6,567 tokens)
  - Topics: Requirements, Create an overlay network, Encrypt traffic on an overlay network
- **[Legacy container links and more](references/engine-18.md)** (~6,617 tokens)
  - Topics: Connect using network port mapping, Connect with the linking system, Communication across links
- **[Networking overview and more](references/engine-19.md)** (~7,356 tokens)
  - Topics: User-defined networks, Published ports, IP address and hostname
- **[Docker Engine 17.09 release notes and more](references/engine-20.md)** (~7,112 tokens)
  - Topics: 17091-ce, 17090-ce, 17100-ce
- **[Docker Engine 18.06 release notes and more](references/engine-21.md)** (~6,087 tokens)
  - Topics: 18063-ce, 18062, 18061-ce
- **[Docker Engine 19.03 release notes](references/engine-22.md)** (~4,925 tokens)
  - Topics: 190315, 190314, 190313
- **[Docker Engine 20.10 release notes](references/engine-23.md)** (~7,928 tokens)
  - Topics: 201024, 201023, 201022
- **[Docker Engine 23.0 release notes](references/engine-24.md)** (~5,660 tokens)
  - Topics: 2306, 2305, 2304
- **[Docker Engine 24.0 release notes and more](references/engine-25.md)** (~6,874 tokens)
  - Topics: 2409, Security, 2408
- **[Docker Engine 26.0 release notes and more](references/engine-26.md)** (~2,749 tokens)
  - Topics: 2602, 2601, 2600
- **[Docker Engine version 27 release notes](references/engine-27.md)** (~6,446 tokens)
  - Topics: 275, 274, 273
- **[Docker Engine version 28 release notes](references/engine-28.md)** (~12,935 tokens)
  - Topics: 2852, 2851, 2850
- **[Docker Engine version 29 release notes](references/engine-29.md)** (~7,426 tokens)
  - Topics: 2920, 2915, 2914
- **[Docker Engine prior releases](references/engine-30.md)** (~30,761 tokens)
  - Topics: 1131 2017-02-08, 1130 2017-01-18, 1126 2017-01-10
- **[Antivirus software and Docker and more](references/engine-31.md)** (~5,969 tokens)
  - Topics: Understand the policies, Load and unload profiles, Nginx example profile
- **[Troubleshooting and more](references/engine-32.md)** (~5,722 tokens)
  - Topics: Known limitations, Troubleshooting, Uninstall
- **[Delegations for content trust and more](references/engine-33.md)** (~8,000 tokens)
  - Topics: Configuring the Docker client, Configuring the Notary client, Creating delegation keys
- **[Isolate containers with a user namespace and more](references/engine-34.md)** (~5,018 tokens)
  - Topics: About remapping and subordinate user and group IDs, Prerequisites, Enable userns-remap on the daemon
- **[Bind mounts and more](references/engine-35.md)** (~6,818 tokens)
  - Topics: When to use bind mounts, Bind-mounting over existing data, Considerations and constraints
- **[Device Mapper storage driver (deprecated)](references/engine-36.md)** (~5,877 tokens)
  - Topics: Prerequisites, Configure Docker with thedevicemapperstorage driver, Manage devicemapper
- **[OverlayFS storage driver and more](references/engine-37.md)** (~6,107 tokens)
  - Topics: Prerequisites, Configure Docker with theoverlay2storage driver, How theoverlay2driver works
- **[ZFS storage driver and more](references/engine-38.md)** (~7,956 tokens)
  - Topics: Prerequisites, Configure Docker with thezfsstorage driver, Managezfs
- **[Volumes and more](references/engine-39.md)** (~5,816 tokens)
  - Topics: When to use volumes, A volumes lifecycle, Mounting a volume over existing data
- **[Administer and maintain a swarm of Docker Engines and more](references/engine-40.md)** (~7,896 tokens)
  - Topics: Operate manager nodes in a swarm, Configure the manager to advertise on a static IP address, Add manager nodes for fault tolerance
- **[How nodes work and more](references/engine-41.md)** (~7,363 tokens)
  - Topics: Manager nodes, Worker nodes, Change roles
- **[Manage nodes in a swarm and more](references/engine-42.md)** (~5,521 tokens)
  - Topics: List nodes, Inspect an individual node, Update a node
- **[Manage sensitive data with Docker secrets](references/engine-43.md)** (~7,018 tokens)
  - Topics: About secrets, How Docker manages secrets, Read more aboutdocker secretcommands
- **[Deploy services to a swarm](references/engine-44.md)** (~8,611 tokens)
  - Topics: Create a service, Update a service, Remove a service
- **[Deploy a stack to a swarm and more](references/engine-45.md)** (~7,510 tokens)
  - Topics: Set up a Docker registry, Create the example application, Test the app with Compose
- **[Getting started with Swarm mode and more](references/engine-46.md)** (~2,797 tokens)
  - Topics: Set up, Next steps, Initialize a swarm with autolocking enabled

### Enterprise

- **[Docker Desktop in Microsoft Dev Box and more](references/enterprise-1.md)** (~7,728 tokens)
  - Topics: Key benefits, Setup, Support
- **[Configure sign and more](references/enterprise-2.md)** (~7,514 tokens)
  - Topics: Choose your method, Windows Registry key method, macOS Configuration profiles method recommended
- **[Enhanced Container Isolation and more](references/enterprise-3.md)** (~5,695 tokens)
  - Topics: Who should use Enhanced Container Isolation, How Enhanced Container Isolation works, Key security features
- **[Configure Settings Management with a JSON file](references/enterprise-4.md)** (~3,363 tokens)
  - Topics: Prerequisites, Step one Create the settings file, Step two Configure settings
- **[Settings reference](references/enterprise-5.md)** (~9,631 tokens)
  - Topics: General settings, Resources settings, Docker Engine settings
- **[Settings Management and more](references/enterprise-6.md)** (~7,946 tokens)
  - Topics: Who should use Settings Management, How Settings Management works, Configurable settings
- **[Provision users and more](references/enterprise-7.md)** (~7,797 tokens)
  - Topics: What is provisioning, Default provisioning setup, SSO attributes
- **[SSO user management FAQs and more](references/enterprise-8.md)** (~4,894 tokens)
  - Topics: Do I need to manually add users to my organization, Can users use different email addresses to authenticate through SSO, How will users know theyre being added to a Docker organization

### Extensions

- **[Extension metadata and more](references/extensions-1.md)** (~7,852 tokens)
  - Topics: The metadatajson file, Extension capabilities, The frontend
- **[MUI best practices and more](references/extensions-2.md)** (~7,905 tokens)
  - Topics: Assume the theme can change at any time, When you go custom centralize it, Whats next
- **[Share your extension and more](references/extensions-3.md)** (~7,727 tokens)
  - Topics: Create a share URL, Release your extension, Promote your extension
- **[Settings and feedback for Docker Extensions](references/extensions-4.md)** (~609 tokens)
  - Topics: Settings, Submit feedback

### General

- **[Docker accounts and more](references/general-1.md)** (~7,313 tokens)
  - Topics: Company and organization hierarchy, Admin Console features, Manage companies and organizations
- **[Deprecated and retired Docker products and features and more](references/general-2.md)** (~3,162 tokens)
  - Topics: Products and features, Open source projects, For developers

### Get Started

- **[Build, tag, and publish an image and more](references/get-started-1.md)** (~7,722 tokens)
  - Topics: Explanation, Try it out, Additional resources
- **[Writing a Dockerfile and more](references/get-started-2.md)** (~7,004 tokens)
  - Topics: Explanation, Try it out, Additional resources
- **[Publishing and exposing ports and more](references/get-started-3.md)** (~7,848 tokens)
  - Topics: Explanation, Try it out, Additional resources
- **[What is Docker Compose? and more](references/get-started-4.md)** (~7,762 tokens)
  - Topics: Explanation, Try it out, Additional resources
- **[Introduction and more](references/get-started-5.md)** (~5,232 tokens)
  - Topics: About this series, What youll learn, Modules
- **[Use bind mounts and more](references/get-started-6.md)** (~6,848 tokens)
  - Topics: Quick volume type comparisons, Trying out bind mounts, Development containers
- **[Image and more](references/get-started-7.md)** (~2,281 tokens)
  - Topics: Image layering, Layer caching, Multi-stage builds

### Guides

- **[Communication and information gathering and more](references/guides-1.md)** (~7,164 tokens)
  - Topics: Communicate with your developers and IT teams, Identify Docker organizations, Gather requirements
- **[Automate your builds with GitHub Actions and more](references/guides-2.md)** (~7,641 tokens)
  - Topics: Prerequisites, Overview, Connect your GitHub repository to Docker Hub
- **[Run Angular tests in a container and more](references/guides-3.md)** (~7,589 tokens)
  - Topics: Prerequisites, Overview, Run tests during development
- **[Test your Bun deployment and more](references/guides-4.md)** (~7,603 tokens)
  - Topics: Prerequisites, Overview, Create a Kubernetes YAML file
- **[Supply and more](references/guides-5.md)** (~7,571 tokens)
  - Topics: Prerequisites, Overview, Generate an SBOM
- **[Test your Deno deployment and more](references/guides-6.md)** (~7,395 tokens)
  - Topics: Prerequisites, Overview, Create a Kubernetes YAML file
- **[Common challenges and questions and more](references/guides-7.md)** (~6,477 tokens)
  - Topics: What youll learn, Whos this for, Tools integration
- **[Use containers for .NET development and more](references/guides-8.md)** (~5,894 tokens)
  - Topics: Prerequisites, Overview, Update the application
- **[Laravel Production Setup with Docker Compose and more](references/guides-9.md)** (~7,516 tokens)
  - Topics: Project structure, Create a Dockerfile for PHP-FPM production, Create a Dockerfile for PHP-CLI production
- **[Containerize a generative AI application and more](references/guides-10.md)** (~7,664 tokens)
  - Topics: Prerequisites, Overview, Get the sample application
- **[Build a code quality check workflow and more](references/guides-11.md)** (~7,975 tokens)
  - Topics: Prerequisites, Set up your project, Step 1 Create your first sandbox
- **[Connecting services with Docker Compose and more](references/guides-12.md)** (~7,338 tokens)
  - Topics: Creating a Docker Compose file, Understanding the Docker Compose file, Building and running the services
- **[Configure CI/CD for your Go application and more](references/guides-13.md)** (~7,160 tokens)
  - Topics: Prerequisites, Overview, Step one Create the repository
- **[Run your Go image as a container and more](references/guides-14.md)** (~6,403 tokens)
  - Topics: Prerequisites, Overview, Run in detached mode
- **[Use containers for Java development and more](references/guides-15.md)** (~6,138 tokens)
  - Topics: Prerequisites, Overview, Add a local database and persist data
- **[Developing event and more](references/guides-16.md)** (~5,657 tokens)
  - Topics: Prerequisites, Launching Kafka, Connecting to Kafka from a non-containerized app
- **[Develop and test AWS Cloud applications using LocalStack and Docker and more](references/guides-17.md)** (~7,055 tokens)
  - Topics: What is LocalStack, Why use LocalStack, Using LocalStack with Docker
- **[Containerize a Node.js application and more](references/guides-18.md)** (~6,383 tokens)
  - Topics: Prerequisites, Overview, Get the sample application
- **[Use containers for Node.js development and more](references/guides-19.md)** (~7,527 tokens)
  - Topics: Prerequisites, Overview, Add a local database and persist data
- **[Configure CI/CD for your PHP application and more](references/guides-20.md)** (~7,746 tokens)
  - Topics: Prerequisites, Overview, Step one Create the repository
- **[Automate your builds with GitHub Actions and more](references/guides-21.md)** (~7,671 tokens)
  - Topics: Prerequisites, Overview, 1 Define the GitHub Actions workflow
- **[Configure CI/CD for your R application and more](references/guides-22.md)** (~7,074 tokens)
  - Topics: Prerequisites, Overview, Step one Create the repository
- **[Containerize a React.js Application and more](references/guides-23.md)** (~7,165 tokens)
  - Topics: Prerequisites, Overview, Get the sample application
- **[Automate your builds with GitHub Actions and more](references/guides-24.md)** (~7,701 tokens)
  - Topics: Prerequisites, Overview, 1 Define the GitHub Actions workflow
- **[Configure CI/CD for your Rust application and more](references/guides-25.md)** (~6,061 tokens)
  - Topics: Prerequisites, Overview, Step one Create the repository
- **[Build a sentiment analysis app and more](references/guides-26.md)** (~7,848 tokens)
  - Topics: Overview, Prerequisites, Get the sample application
- **[Why Testcontainers Cloud? and more](references/guides-27.md)** (~7,989 tokens)
  - Topics: What youll learn, Tools integration, Whos this for
- **[Automate your builds with GitHub Actions and more](references/guides-28.md)** (~7,822 tokens)
  - Topics: Prerequisites, Overview, Connect your GitHub repository to Docker Hub
- **[Run vue.js tests in a container and more](references/guides-29.md)** (~4,468 tokens)
  - Topics: Prerequisites, Overview, Run tests during development

### Offload

- **[About Docker Offload and more](references/offload.md)** (~3,772 tokens)
  - Topics: Key features, Why use Docker Offload, How Docker Offload works

### Reference

- **[Docker Verified Publisher API changelog and more](references/reference-1.md)** (~5,201 tokens)
  - Topics: 2025-06-27, Endpoint deprecation policy, Deprecated endpoints
- **[Docker Engine API(1.44)](references/reference-2.md)** (~21,772 tokens)
  - Topics: Errors, Versioning, Authentication
- **[Docker Engine API(1.45)](references/reference-3.md)** (~21,691 tokens)
  - Topics: Errors, Versioning, Authentication
- **[Docker Engine API(1.46)](references/reference-4.md)** (~21,794 tokens)
  - Topics: Errors, Versioning, Authentication
- **[Docker Engine API(1.47)](references/reference-5.md)** (~21,868 tokens)
  - Topics: Errors, Versioning, Authentication
- **[Docker Engine API(1.48)](references/reference-6.md)** (~22,743 tokens)
  - Topics: Errors, Versioning, Authentication
- **[Docker Engine API(1.49)](references/reference-7.md)** (~22,738 tokens)
  - Topics: Errors, Versioning, Authentication
- **[Docker Engine API(1.50)](references/reference-8.md)** (~22,760 tokens)
  - Topics: Errors, Versioning, Authentication
- **[Docker Engine API(1.51)](references/reference-9.md)** (~22,787 tokens)
  - Topics: Errors, Versioning, Authentication
- **[Docker Engine API(1.52)](references/reference-10.md)** (~22,493 tokens)
  - Topics: Errors, Versioning, Authentication
- **[Docker Engine API(1.53)](references/reference-11.md)** (~22,573 tokens)
  - Topics: Errors, Versioning, Authentication
- **[Engine API version history](references/reference-12.md)** (~13,418 tokens)
  - Topics: v153 API changes, v152 API changes, v151 API changes
- **[Docker Engine API and more](references/reference-13.md)** (~7,723 tokens)
  - Topics: View the API reference, Versioned API and SDK, Container Methods
- **[Interface: NavigationIntents and more](references/reference-14.md)** (~2,306 tokens)
  - Topics: Container Methods, Images Methods, Volume Methods
- **[Docker HUB API(2](references/reference-15.md)** (~9,737 tokens)
  - Topics: Changelog, Resources, Rate Limiting
- **[Registry authentication and more](references/reference-16.md)** (~7,992 tokens)
  - Topics: Requirements, Authorization server endpoint descriptions, How to authenticate
- **[LegacyKeyValueFormat and more](references/reference-17.md)** (~7,437 tokens)
  - Topics: Output, Description, Examples
- **[docker buildx build](references/reference-18.md)** (~6,949 tokens)
  - Topics: Description, Options, Examples
- **[docker buildx create and more](references/reference-19.md)** (~7,956 tokens)
  - Topics: Description, Options, Examples
- **[docker buildx imagetools create and more](references/reference-20.md)** (~7,987 tokens)
  - Topics: Description, Options, Examples
- **[docker compose bridge transformations list and more](references/reference-21.md)** (~7,398 tokens)
  - Topics: Description, Options, Description
- **[docker compose and more](references/reference-22.md)** (~7,307 tokens)
  - Topics: Description, Options, Examples
- **[docker container create and more](references/reference-23.md)** (~7,953 tokens)
  - Topics: Description, Options, Examples
- **[docker container pause and more](references/reference-24.md)** (~2,169 tokens)
  - Topics: Description, Examples, Description
- **[docker container run](references/reference-25.md)** (~12,655 tokens)
  - Topics: Description, Options, Examples
- **[docker container start and more](references/reference-26.md)** (~8,010 tokens)
  - Topics: Description, Options, Examples
- **[docker desktop engine use and more](references/reference-27.md)** (~7,556 tokens)
  - Topics: Subcommands, Options, Subcommands
- **[docker image pull and more](references/reference-28.md)** (~7,601 tokens)
  - Topics: Description, Options, Examples
- **[docker login and more](references/reference-29.md)** (~7,991 tokens)
  - Topics: Description, Options, Examples
- **[docker mcp oauth authorize and more](references/reference-30.md)** (~6,734 tokens)
  - Topics: Description, Options, Description
- **[docker network create and more](references/reference-31.md)** (~7,962 tokens)
  - Topics: Description, Options, Examples
- **[docker node update and more](references/reference-32.md)** (~8,005 tokens)
  - Topics: Description, Options, Examples
- **[docker sandbox and more](references/reference-33.md)** (~7,800 tokens)
  - Topics: Description, Options, Subcommands
- **[docker scout repo enable and more](references/reference-34.md)** (~5,557 tokens)
  - Topics: Description, Options, Examples
- **[docker service create](references/reference-35.md)** (~8,524 tokens)
  - Topics: Description, Options, Examples
- **[docker service inspect and more](references/reference-36.md)** (~7,710 tokens)
  - Topics: Description, Options, Examples
- **[docker stack config and more](references/reference-37.md)** (~7,202 tokens)
  - Topics: Description, Options, Examples
- **[docker swarm join and more](references/reference-38.md)** (~8,000 tokens)
  - Topics: Description, Options, Examples
- **[docker trust key generate and more](references/reference-39.md)** (~6,535 tokens)
  - Topics: Description, Options, Examples
- **[docker](references/reference-40.md)** (~3,757 tokens)
  - Topics: Description, Options, Examples
- **[dockerd](references/reference-41.md)** (~9,362 tokens)
  - Topics: Description, Examples
- **[Compose Build Specification and more](references/reference-42.md)** (~7,771 tokens)
  - Topics: Usingbuildandimage, Publishing built images, Illustrative example
- **[Fragments and more](references/reference-43.md)** (~5,155 tokens)
  - Topics: Example 1, Example 2, Example 3
- **[Define services in Docker Compose](references/reference-44.md)** (~13,361 tokens)
  - Topics: Examples, Attributes
- **[Version and name top and more](references/reference-45.md)** (~1,575 tokens)
  - Topics: Version top-level element obsolete, Name top-level element, Example
- **[Dockerfile reference](references/reference-46.md)** (~20,649 tokens)
  - Topics: Overview, Format, Parser directives
- **[Glossary and more](references/reference-47.md)** (~7,984 tokens)
  - Topics: Looking for more samples, Looking for more samples, Looking for more samples
- **[React samples and more](references/reference-48.md)** (~1,909 tokens)
  - Topics: Looking for more samples, Looking for more samples, Looking for more samples

### Scout

- **[Advisory database sources and matching service and more](references/scout-1.md)** (~6,917 tokens)
  - Topics: Advisory database sources, Severity and scoring priority, Vulnerability matching
- **[Docker Scout metrics exporter and more](references/scout-2.md)** (~7,928 tokens)
  - Topics: Metrics, Creating an access token, Prometheus
- **[Install Docker Scout and more](references/scout-3.md)** (~7,209 tokens)
  - Topics: Installation script, Manual installation, Container image
- **[Integrate Docker Scout with Artifactory Container Registry and more](references/scout-4.md)** (~6,875 tokens)
  - Topics: How it works, Integrate an Artifactory registry, How it works
- **[Docker Scout health scores and more](references/scout-5.md)** (~7,147 tokens)
  - Topics: Viewing health scores, Scoring system, Improving your health score
- **[Docker Scout release notes](references/scout-6.md)** (~2,120 tokens)
  - Topics: Q4 2024, Q3 2024, Q2 2024

### Security

- **[Recover your Docker account and more](references/security.md)** (~6,627 tokens)
  - Topics: Generate a new recovery code, Recover your account without access, Key benefits

### Subscription

- **[Change your subscription and more](references/subscription.md)** (~3,047 tokens)
  - Topics: Upgrade your subscription, Downgrade your subscription, Subscription pause policy

### Tags

- **[Administration and more](references/tags.md)** (~1,327 tokens)
  - Topics: Guides, Manuals, Guides

## Usage Guidelines

1. **Identify relevant sections** - Match the user's question to the appropriate reference file(s)
2. **Load minimally** - Only read files directly relevant to the question to conserve context
3. **Cite sources** - Reference specific sections when answering
4. **Combine knowledge** - For complex questions, you may need multiple reference files

### When to use each reference:

- **Accounts**: Accounts-related features and documentation
- **Admin**: Admin-related features and documentation
- **Ai**: AI features and third-party integrations
- **Billing**: Billing-related features and documentation
- **Build**: Build-related features and documentation
- **Build Cloud**: Build Cloud-related features and documentation
- **Compose**: Compose-related features and documentation
- **Contribute**: Contribute-related features and documentation
- **Desktop**: Desktop-related features and documentation
- **Dhi**: Dhi-related features and documentation
- **Docker Hub**: Docker Hub-related features and documentation
- **Engine**: Engine-related features and documentation
- **Enterprise**: Enterprise-related features and documentation
- **Extensions**: Extensions-related features and documentation
- **General**: General documentation, overview, and getting started
- **Get Started**: Get Started-related features and documentation
- **Guides**: Guides-related features and documentation
- **Offload**: Offload-related features and documentation
- **Reference**: Reference-related features and documentation
- **Scout**: Scout-related features and documentation
- **Security**: Security-related features and documentation
- **Subscription**: Subscription-related features and documentation
- **Tags**: Tags-related features and documentation
