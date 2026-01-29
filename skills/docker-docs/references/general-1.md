# Docker accounts and more

# Docker accounts

> Learn how to create and manage your Docker account

# Docker accounts

---

This section covers individual Docker accounts and Docker IDs. It does
not cover organizations, companies, or administrator roles.

A Docker account is required to:

- Create a Docker ID
- Access Docker products and services like Docker Hub and Docker Desktop
- Receive organization invitations
- Manage your personal settings and security features

[Create a Docker IDGet started with Docker and create an account.](https://docs.docker.com/accounts/create-account/)[Manage accountLearn how to manage the settings for your account.](https://docs.docker.com/accounts/manage-account/)[Personal access tokensLearn how to create and manage access tokens for your account.](https://docs.docker.com/security/access-tokens/)[Set up two-factor authenticationAdd an extra layer of authentication to your Docker account.](https://docs.docker.com/security/2fa/)[Deactivate an accountLearn how to deactivate a Docker user account.](https://docs.docker.com/accounts/deactivate-user-account/)[Account FAQExplore frequently asked questions about Docker accounts.](https://docs.docker.com/accounts/general-faqs/)

---

# Administration

> Overview of administration features and roles in the Docker Admin Console

# Administration

   Table of contents

---

Administrators can manage companies and organizations using the
[Docker Admin Console](https://app.docker.com/admin). The Admin Console
provides centralized observability, access management, and security controls
across Docker environments.

## Company and organization hierarchy

The [Docker Admin Console](https://app.docker.com/admin) provides administrators with centralized observability, access management, and controls for their company and organizations. To provide these features, Docker uses the following hierarchy and roles.

![Diagram showing Docker’s administration hierarchy with Company at the top, followed by Organizations, Teams, and Members](https://docs.docker.com/admin/images/docker-admin-structure.webp)  ![Diagram showing Docker’s administration hierarchy with Company at the top, followed by Organizations, Teams, and Members](https://docs.docker.com/admin/images/docker-admin-structure.webp)

### Company

A company groups multiple Docker organizations for centralized configuration.
Companies are only available for Docker Business subscribers.

Companies have the following administrator role available:

- Company owner: Can view and manage all organizations within the company.
  Has full access to company-wide settings and inherits the same permissions as
  organization owners.

### Organization

An organization contains teams and repositories. All Docker Team and Business
subscribers must have at least one organization.

Organizations have the following administrator role available:

- Organization owner: Can manage organization settings, users, and access
  controls.

### Team

Teams are optional and let you group members to assign repository permissions
collectively. Teams simplify permission management across projects
or functions.

### Member

A member is any Docker user added to an organization. Organization and company
owners can assign roles to members to define their level of access.

> Note
>
> Creating a company is optional, but organizations are required for Team and
> Business subscriptions.

## Admin Console features

Docker's [Admin Console](https://app.docker.com/admin) allows you to:

- Create and manage companies and organizations
- Assign roles and permissions to members
- Group members into teams to manage access by project or role
- Set company-wide policies, including SCIM provisioning and security
  enforcement

## Manage companies and organizations

Learn how to manage companies and organizations in the following sections.

[Company administrationExplore how to manage a company.](https://docs.docker.com/admin/company/)[Organization administrationLearn about organization administration.](https://docs.docker.com/admin/organization/)[Onboard your organizationLearn how to onboard and secure your organization.](https://docs.docker.com/admin/organization/onboard)[Company FAQDiscover common questions and answers about companies.](https://docs.docker.com/faq/admin/company-faqs/)[Organization FAQExplore popular FAQ topics about organizations.](https://docs.docker.com/faq/admin/organization-faqs/)[SecurityExplore security features for administrators.](https://docs.docker.com/security/)

---

# Manage billing and payments

> Find information about managing billing and payments for Docker subscriptions.

# Manage billing and payments

---

Use the resources in this section to manage billing and payments for your Docker
subscriptions.

[Add or update a payment methodLearn how to add or update a payment method for your personal account or organization.](https://docs.docker.com/billing/payment-method/)[Update billing informationDiscover how to update the billing information for your personal account or organization.](https://docs.docker.com/billing/details/)[View billing historyLearn how to view billing history and download past invoices.](https://docs.docker.com/billing/history/)[Billing FAQsFind the answers you need and explore common questions.](https://docs.docker.com/billing/faqs/)[Register a tax certificateLearn how to register a tax exemption certificate.](https://docs.docker.com/billing/tax-certificate/)[3D Secure authenticationDiscover how Docker billing supports 3DS and how to troubleshoot potential issues.](https://docs.docker.com/billing/3d-secure/)

---

# Docker Build Cloud

> Find documentation on Docker Build Cloud to help you build your container images faster, both locally and in CI

# Docker Build Cloud

   Table of contents

---

Subscription: Pro  Team  Business

Docker Build Cloud is a service that lets you build your container images
faster, both locally and in CI. Builds run on cloud infrastructure optimally
dimensioned for your workloads, no configuration required. The service uses a
remote build cache, ensuring fast builds anywhere and for all team members.

## How Docker Build Cloud works

Using Docker Build Cloud is no different from running a regular build. You invoke a
build the same way you normally would, using `docker buildx build`. The
difference is in where and how that build gets executed.

By default when you invoke a build command, the build runs on a local instance
of BuildKit, bundled with the Docker daemon. With Docker Build Cloud, you send
the build request to a BuildKit instance running remotely, in the cloud.
All data is encrypted in transit.

The remote builder executes the build steps, and sends the resulting build
output to the destination that you specify. For example, back to your local
Docker Engine image store, or to an image registry.

Docker Build Cloud provides several benefits over local builds:

- Improved build speed
- Shared build cache
- Native multi-platform builds

And the best part: you don't need to worry about managing builders or
infrastructure. Just connect to your builders, and start building.
Each cloud builder provisioned to an organization is completely
isolated to a single Amazon EC2 instance, with a dedicated EBS volume for build
cache, and encryption in transit. That means there are no shared processes or
data between cloud builders.

> Note
>
> Docker Build Cloud is currently only available in the US East region. Users
> in Europe and Asia may experience increased latency compared to users based
> in North America.
>
>
>
> Support for multi-region builders is on the roadmap.

## Get Docker Build Cloud

To get started with Docker Build Cloud,
[create a Docker account](https://docs.docker.com/accounts/create-account/). There are two options
to get access to Docker Build Cloud:

- Users with a free Personal account can opt-in to a 7-day free trial, with the option
  to subscribe for access. To start your free trial, sign in to [Docker Build Cloud Dashboard](https://app.docker.com/build/) and follow the on-screen instructions.
- All users with a paid Docker subscription have access to Docker Build Cloud included
  with their Docker suite of products. See [Docker subscriptions and features](https://www.docker.com/pricing/) for more information.

Once you've signed up and created a builder, continue by
[setting up the builder in your local environment](https://docs.docker.com/build-cloud/setup/).

For information about roles and permissions related to Docker Build Cloud, see
[Roles and Permissions](https://docs.docker.com/enterprise/security/roles-and-permissions/#docker-build-cloud-permissions).

---

# Docker Build

> Get an overview of Docker Build to package and bundle your code and ship it anywhere

# Docker Build

---

Docker Build is one of Docker Engine's most used features. Whenever you are
creating an image you are using Docker Build. Build is a key part of your
software development life cycle allowing you to package and bundle your code and
ship it anywhere.

Docker Build is more than a command for building images, and it's not only about
packaging your code. It's a whole ecosystem of tools and features that support
not only common workflow tasks but also provides support for more complex and
advanced scenarios.

[Packaging your softwareBuild and package your application to run it anywhere: locally or in the cloud.](https://docs.docker.com/build/concepts/overview/)[Multi-stage buildsKeep your images small and secure with minimal dependencies.](https://docs.docker.com/build/building/multi-stage/)[Multi-platform imagesBuild, push, pull, and run images seamlessly on different computer architectures.](https://docs.docker.com/build/building/multi-platform/)[BuildKitExplore BuildKit, the open source build engine.](https://docs.docker.com/build/buildkit/)[Build driversConfigure where and how you run your builds.](https://docs.docker.com/build/builders/drivers/)[ExportersExport any artifact you like, not just Docker images.](https://docs.docker.com/build/exporters/)[Build cachingAvoid unnecessary repetitions of costly operations, such as package installs.](https://docs.docker.com/build/cache/)[BakeOrchestrate your builds with Bake.](https://docs.docker.com/build/bake/)

---

# Docker Compose

> Learn how to use Docker Compose to define and run multi-container applications with this detailed introduction to the tool.

# Docker Compose

---

Docker Compose is a tool for defining and running multi-container applications.
It is the key to unlocking a streamlined and efficient development and deployment experience.

Compose simplifies the control of your entire application stack, making it easy to manage services, networks, and volumes in a single YAML configuration file. Then, with a single command, you create and start all the services
from your configuration file.

Compose works in all environments - production, staging, development, testing, as
well as CI workflows. It also has commands for managing the whole lifecycle of your application:

- Start, stop, and rebuild services
- View the status of running services
- Stream the log output of running services
- Run a one-off command on a service

[Why use Compose?Understand Docker Compose's key benefits](https://docs.docker.com/compose/intro/features-uses/)[How Compose worksUnderstand how Compose works](https://docs.docker.com/compose/intro/compose-application-model/)[Install ComposeFollow the instructions on how to install Docker Compose.](https://docs.docker.com/compose/install)[QuickstartLearn the key concepts of Docker Compose whilst building a simple Python web application.](https://docs.docker.com/compose/gettingstarted)[View the release notesFind out about the latest enhancements and bug fixes.](https://github.com/docker/compose/releases)[Explore the Compose file referenceFind information on defining services, networks, and volumes for a Docker application.](https://docs.docker.com/reference/compose-file)[Use Compose BridgeTransform your Compose configuration file into configuration files for different platforms, such as Kubernetes.](https://docs.docker.com/compose/bridge)[Browse common FAQsExplore general FAQs and find out how to give feedback.](https://docs.docker.com/compose/faq)

---

# Contribute to Docker's docs

# Contribute to Docker's docs

   Table of contents

---

We value documentation contributions from the Docker community. We'd like to
make it as easy as possible for you to contribute to the Docker documentation.

Find the contribution guidelines in
[CONTRIBUTING.md](https://github.com/docker/docs/blob/main/CONTRIBUTING.md) in
the `docker/docs` GitHub repository. Use the following links to review our
style guide and instructions on how to use our page templates and components.

[Grammar and styleExplore Docker's grammar and style guide](https://docs.docker.com/contribute/style/grammar)[FormattingFormat your content to match the rest of our documentation.](https://docs.docker.com/contribute/style/formatting)[Recommended word listChoose the right words for your content.](https://docs.docker.com/contribute/style/recommended-words)[Source file conventionsGuidelines for creating a new page.](https://docs.docker.com/contribute/file-conventions)[TerminologyExplore commonly used Docker terms.](https://docs.docker.com/contribute/style/terminology)[Voice and toneLearn about how we use voice and tone in our writing.](https://docs.docker.com/contribute/style/voice-tone)

### Additional resources

See also:

- A section of useful components you can add to your documentation.
- Information on Docker's [tone and voice](https://docs.docker.com/contribute/style/voice-tone/).
- A [writing checklist](https://docs.docker.com/contribute/checklist/) to help you when you're contributing to Docker's documentation.

---

# Docker Desktop

> Explore Docker Desktop, what it has to offer, and its key features. Take the next step by downloading or find additional resources

# Docker Desktop

   Table of contents

---

Docker Desktop is a one-click-install application for your Mac, Linux, or Windows environment
that lets you build, share, and run containerized applications and microservices.

It provides a straightforward GUI (Graphical User Interface) that lets you manage your containers, applications, and images directly from your machine.

Docker Desktop reduces the time spent on complex setups so you can focus on writing code. It takes care of port mappings, file system concerns, and other default settings, and is regularly updated with bug fixes and security updates.

Docker Desktop integrates with your preferred development tools and languages, and gives you access to a vast ecosystem of trusted images and templates via Docker Hub. This empowers teams to accelerate development, automate builds, enable CI/CD workflows, and collaborate securely through shared repositories.

## Key features

- Ability to containerize and share any application on any cloud platform, in multiple languages and frameworks.
- Quick installation and setup of a complete Docker development environment.
- Includes the latest version of Kubernetes.
- On Windows, the ability to toggle between Linux and Windows containers to build applications.
- Fast and reliable performance with native Windows Hyper-V virtualization.
- Ability to work natively on Linux through WSL 2 on Windows machines.
- Volume mounting for code and data, including file change notifications and easy access to running containers on the localhost network.

## Products inside Docker Desktop

- [Docker MCP Toolkit and Catalog](https://docs.docker.com/ai/mcp-catalog-and-toolkit/)
- [Docker Model Runner](https://docs.docker.com/ai/model-runner/)
- [Ask Gordon](https://docs.docker.com/ai/gordon/)
- [Docker Offload](https://docs.docker.com/offload/)
- [Docker Engine](https://docs.docker.com/engine/)
- Docker CLI client
- [Docker Build](https://docs.docker.com/build/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Docker Scout](https://docs.docker.com/scout/)
- [Kubernetes](https://github.com/kubernetes/kubernetes/)

## Next steps

### Install Docker Desktop

Install Docker Desktop on
[Mac](https://docs.docker.com/desktop/setup/install/mac-install/),
[Windows](https://docs.docker.com/desktop/setup/install/windows-install/), or
[Linux](https://docs.docker.com/desktop/setup/install/linux/).

[Learn about Docker DesktopNavigate Docker Desktop.](https://docs.docker.com/desktop/use-desktop/)

### Explore its key features

Find information about
[Networking](https://docs.docker.com/desktop/features/networking/),
[Docker VMM](https://docs.docker.com/desktop/features/vmm/),
[WSL](https://docs.docker.com/desktop/features/wsl/), and more.

[View the release notesFind out about new features, improvements, and bug fixes.](https://docs.docker.com/desktop/release-notes/)[Browse common FAQsExplore general FAQs or FAQs for specific platforms.](https://docs.docker.com/desktop/troubleshoot-and-support/faqs/general/)[Give feedbackProvide feedback on Docker Desktop or Docker Desktop features.](https://docs.docker.com/desktop/troubleshoot-and-support/feedback/)

---

# Docker Hardened Images

> Secure, minimal, and production-ready base images

# Docker Hardened Images

---

Docker Hardened Images (DHI) are minimal, secure, and production-ready container
base and application images maintained by Docker. Designed to reduce
vulnerabilities and simplify compliance, DHI integrates easily into your
existing Docker-based workflows with little to no retooling required.

DHI is available in two tiers: **DHI Free** provides core security features at
no cost, while **DHI Enterprise** adds SLA-backed support, compliance variants,
customization, and Extended Lifecycle Support for organizations with advanced
requirements.

![DHI Subscription](https://docs.docker.com/dhi/images/dhi-subscription.png)  ![DHI Subscription](https://docs.docker.com/dhi/images/dhi-subscription.png)

Explore the sections below to get started with Docker Hardened Images, integrate
them into your workflow, and learn what makes them secure and enterprise-ready.

[QuickstartFollow a step-by-step guide to explore and run a Docker Hardened Image.](https://docs.docker.com/dhi/get-started/)[ExploreLearn what Docker Hardened Images are, how they're built, and what sets them apart from typical base images.](https://docs.docker.com/dhi/explore/)[FeaturesDiscover the security, compliance, and enterprise-readiness features built into Docker Hardened Images.](https://docs.docker.com/dhi/features/)[How-tosStep-by-step guides for using, verifying, scanning, and migrating to Docker Hardened Images.](https://docs.docker.com/dhi/how-to/)[Core conceptsUnderstand the secure supply chain principles that make Docker Hardened Images production-ready.](https://docs.docker.com/dhi/core-concepts/)[TroubleshootResolve common issues with building, running, or debugging Docker Hardened Images.](https://docs.docker.com/dhi/troubleshoot/)[Additional resourcesLinks to blog posts, Docker Hub catalog, GitHub repositories, and more.](https://docs.docker.com/dhi/resources/)

---

# Docker Hub

> Get an overview on Docker Hub to find and share container images

# Docker Hub

---

Docker Hub simplifies development with the world's largest container registry
for storing, managing, and sharing Docker images. By integrating seamlessly with
your tools, it enhances productivity and ensures reliable deployment,
distribution, and access to containerized applications. It also provides
developers with pre-built images and assets to speed up development workflows.

Key features of Docker Hub:

- Unlimited public repositories
- Private repositories
- Webhooks to automate workflows
- GitHub and Bitbucket integrations
- Concurrent and automated builds
- Trusted content featuring high-quality, secure images

In addition to the graphical interface, you can interact with Docker Hub using
the [Docker Hub API](https://docs.docker.com/reference/api/hub/latest/) or experimental [Docker
Hub CLI tool](https://github.com/docker/hub-tool#readme).

[QuickstartStep-by-step instructions on getting started on Docker Hub.](https://docs.docker.com/docker-hub/quickstart)[LibraryExplore the content library, featuring millions of images for operating systems, frameworks, databases, and more.](https://docs.docker.com/docker-hub/image-library/)[RepositoriesCreate a repository to share your images with your team, customers, or the Docker community.](https://docs.docker.com/docker-hub/repos)[OrganizationsLearn about organization administration.](https://docs.docker.com/admin/)[Usage and limitsExplore usage limits and how to better utilize Docker Hub.](https://docs.docker.com/docker-hub/usage/)[Release notesFind out about new features, improvements, and bug fixes.](https://docs.docker.com/docker-hub/release-notes)

---

# Docker Engine

> Find a comprehensive overview of Docker Engine, including how to install, storage details, networking, and more

# Docker Engine

   Table of contents

---

Docker Engine is an open source containerization technology for building and
containerizing your applications. Docker Engine acts as a client-server
application with:

- A server with a long-running daemon process
  [dockerd](https://docs.docker.com/reference/cli/dockerd).
- APIs which specify interfaces that programs can use to talk to and instruct
  the Docker daemon.
- A command line interface (CLI) client
  [docker](https://docs.docker.com/reference/cli/docker/).

The CLI uses
[Docker APIs](https://docs.docker.com/reference/api/engine/) to control or interact with the Docker
daemon through scripting or direct CLI commands. Many other Docker applications
use the underlying API and CLI. The daemon creates and manages Docker objects,
such as images, containers, networks, and volumes.

For more details, see
[Docker Architecture](https://docs.docker.com/get-started/docker-overview/#docker-architecture).

[Install Docker EngineLearn how to install the open source Docker Engine for your distribution.](https://docs.docker.com/engine/install)[StorageUse persistent data with Docker containers.](https://docs.docker.com/storage)[NetworkingManage network connections between containers.](https://docs.docker.com/network)[Container logsLearn how to view and read container logs.](https://docs.docker.com/config/containers/logging/)[PruneTidy up unused resources.](https://docs.docker.com/config/pruning)[Configure the daemonDelve into the configuration options of the Docker daemon.](https://docs.docker.com/config/daemon)[Rootless modeRun Docker without root privileges.](https://docs.docker.com/engine/security/rootless)[Deprecated featuresFind out what features of Docker Engine you should stop using.](https://docs.docker.com/engine/deprecated/)[Release notesRead the release notes for the latest version.](https://docs.docker.com/engine/release-notes)

## Licensing

Commercial use of Docker Engine obtained via Docker Desktop
within larger enterprises (exceeding 250 employees OR with annual revenue surpassing
$10 million USD), requires a [paid subscription](https://www.docker.com/pricing/).
Apache License, Version 2.0. See [LICENSE](https://github.com/moby/moby/blob/master/LICENSE) for the full license.

---

# Docker Extensions

> Extensions

# Docker Extensions

   Table of contents

---

Docker Extensions let you use third-party tools within Docker Desktop to extend its functionality.

You can seamlessly connect your favorite development tools to your application development and deployment workflows. Augment Docker Desktop with debugging, testing, security, and networking functionalities, and create custom add-ons using the Extensions [SDK](https://docs.docker.com/extensions/extensions-sdk/).

Anyone can use Docker Extensions and there is no limit to the number of extensions you can install.

![Extensions Marketplace](https://docs.docker.com/assets/images/extensions.webp)  ![Extensions Marketplace](https://docs.docker.com/assets/images/extensions.webp)

## What extensions are available?

There is a mix of partner and community-built extensions and Docker-built extensions.
You can explore the list of available extensions in [Docker Hub](https://hub.docker.com/search?q=&type=extension) or in the Extensions Marketplace within Docker Desktop.

To find out more about Docker Extensions, we recommend the video walkthrough from DockerCon 2022:

---

# Get started

> Get started with Docker

# Get started

---

If you're new to Docker, this section guides you through the essential resources to get started.

Follow the guides to help you get started and learn how Docker can optimize your development workflows.

For more advanced concepts and scenarios in Docker, see
[Guides](https://docs.docker.com/guides/).

## Foundations of Docker

Install Docker and jump into discovering what Docker is.

[Get DockerChoose the best installation path for your setup.](https://docs.docker.com/get-started/get-docker/)[What is Docker?Learn about the Docker platform.](https://docs.docker.com/get-started/docker-overview/)

Learn the foundational concepts and workflows of Docker.

[IntroductionGet started with the basics and the benefits of containerizing your applications.](https://docs.docker.com/get-started/introduction/)[Docker conceptsGain a better understanding of foundational Docker concepts.](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/)[Docker workshopGet guided through a 45-minute workshop to learn about Docker.](https://docs.docker.com/get-started/workshop/)

---

# Docker guides

> Explore the Docker guides

# Docker guides

Explore our collection of guides to learn how Docker can optimize your
development workflows and how to use it with specific languages, frameworks, or
technologies.

Can't find the guide you're looking for? Open an issue on the
[docker/docs](https://github.com/docker/docs/issues/new) repository to let us
know.

## Featured guides

[Migrate a Go app to DHI](https://docs.docker.com/guides/dhi-go-example/)

Example showing how to migrate a Go application to Docker Hardened Images

 Docker Hardened Images 10 minutes[Migrate a Node.js app to DHI](https://docs.docker.com/guides/dhi-nodejs-example/)

Example showing how to migrate a Node.js application to Docker Hardened
Images

 Docker Hardened Images 10 minutes[Migrate a Python app to DHI](https://docs.docker.com/guides/dhi-python-example/)

Example showing how to migrate a Python application to Docker Hardened Images

 Docker Hardened Images 10 minutes[Migrate to DHI from Docker Official Images](https://docs.docker.com/guides/dhi-from-doi/)

Step-by-step guide to migrate from Docker Official Images to Docker Hardened Images

 Docker Hardened Images 10 minutes[Migrate to DHI from Wolfi](https://docs.docker.com/guides/dhi-from-wolfi/)

Step-by-step guide to migrate from Wolfi to Docker Hardened Images

 Docker Hardened Images 10 minutes

---

## All guides

Filtered results: showing
60 out of
60 guides.

 Administration AI App development Best practices Cloud services Data science Databases Deployment DevOps Docker Hardened Images Distributed systems FAQ Frameworks Networking Observability Product demo Release notes Secrets Troubleshooting![image](https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/csharp/csharp-original.svg) C#![image](https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/cplusplus/cplusplus-original.svg) C++![image](https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/go/go-original.svg) Go![image](https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/java/java-original.svg) Java![image](https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/javascript/javascript-original.svg) JavaScript![image](https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/php/php-original.svg) PHP![image](https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg) Python![image](https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/r/r-original.svg) R![image](https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/ruby/ruby-original.svg) Ruby![image](https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/rust/rust-original.svg) Rust[Set up your company for success with Docker](https://docs.docker.com/guides/admin-set-up/) Administration 20 minutes[Build and run agentic AI applications with Docker](https://docs.docker.com/guides/agentic-ai/) AI 30 minutes[Angular language-specific guide](https://docs.docker.com/guides/angular/)![image](https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/javascript/javascript-original.svg) JavaScript 20 minutes[Develop and test AWS Cloud applications using LocalStack and Docker](https://docs.docker.com/guides/localstack/)![image](https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/javascript/javascript-original.svg) JavaScript  Cloud services 20 minutes[Introduction to Azure Pipelines with Docker](https://docs.docker.com/guides/azure-pipelines/) DevOps 10 minutes[How to build an AI-powered code quality workflow with SonarQube and E2B](https://docs.docker.com/guides/github-sonarqube-sandbox/) DevOps 40 minutes[Building Compose projects with Bake](https://docs.docker.com/guides/compose-bake/) DevOps 20 minutes[Bun language-specific guide](https://docs.docker.com/guides/bun/)![image](https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/javascript/javascript-original.svg) JavaScript 10 minutes[.NET language-specific guide](https://docs.docker.com/guides/dotnet/)![image](https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/csharp/csharp-original.svg) C# 20 minutes[C++ language-specific guide](https://docs.docker.com/guides/cpp/)![image](https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/cplusplus/cplusplus-original.svg) C++ 20 minutes[Faster development and testing with container-supported development](https://docs.docker.com/guides/container-supported-development/) App development 20 minutes[Data science with JupyterLab](https://docs.docker.com/guides/jupyter/)![image](https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg) Python  Data science 20 minutes[Deno language-specific guide](https://docs.docker.com/guides/deno/)![image](https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/javascript/javascript-original.svg) JavaScript 10 minutes[Deploy to Kubernetes](https://docs.docker.com/guides/kube-deploy/) Deployment 10 minutes[Deploy to Swarm](https://docs.docker.com/guides/swarm-deploy/) Deployment 10 minutes[Deployment and orchestration](https://docs.docker.com/guides/orchestration/) Deployment 10 minutes[Docker Build Cloud: Reclaim your time with fast, multi-architecture builds](https://docs.docker.com/guides/docker-build-cloud/) Product demo 10 minutes[Defining and running multi-container applications with Docker Compose](https://docs.docker.com/guides/docker-compose/) Product demo 10 minutes[Securing your software supply chain with Docker Scout](https://docs.docker.com/guides/docker-scout/) Product demo 20 minutes[Developing event-driven applications with Kafka and Docker](https://docs.docker.com/guides/kafka/)![image](https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/javascript/javascript-original.svg) JavaScript  Distributed systems 20 minutes[Face detection with TensorFlow.js](https://docs.docker.com/guides/tensorflowjs/)![image](https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/javascript/javascript-original.svg) JavaScript  AI 20 minutes[Generate Docker Compose Files with Claude Code and Docker MCP Toolkit](https://docs.docker.com/guides/genai-claude-code-mcp/claude-code-mcp-guide/) AI 15 minutes[Introduction to GitHub Actions with Docker](https://docs.docker.com/guides/gha/) DevOps 10 minutes[Go language-specific guide](https://docs.docker.com/guides/golang/)![image](https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/go/go-original.svg) Go 30 minutes[HTTP routing with Traefik](https://docs.docker.com/guides/traefik/) Networking 20 minutes[Instrumenting a JavaScript App with OpenTelemetry](https://docs.docker.com/guides/opentelemetry/)![image](https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/javascript/javascript-original.svg) JavaScript  App development
 Observability 10 minutes[Java language-specific guide](https://docs.docker.com/guides/java/)![image](https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/java/java-original.svg) Java 20 minutes[Build a language translation app](https://docs.docker.com/guides/language-translation/)![image](https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg) Python  AI 20 minutes[Develop and Deploy Laravel applications with Docker Compose](https://docs.docker.com/guides/frameworks/laravel/)![image](https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/php/php-original.svg) PHP  Frameworks 30 minutes[Leveraging RAG in GenAI to teach new information](https://docs.docker.com/guides/genai-leveraging-rag/) AI 35 minutes[Mastering multi-platform builds, testing, and more with Docker Buildx Bake](https://docs.docker.com/guides/bake/)![image](https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/go/go-original.svg) Go  DevOps 30 minutes[Mastering user and access management](https://docs.docker.com/guides/admin-user-management/) Administration 20 minutes[Migrate a Go app to DHI](https://docs.docker.com/guides/dhi-go-example/) Docker Hardened Images 10 minutes[Migrate a Node.js app to DHI](https://docs.docker.com/guides/dhi-nodejs-example/) Docker Hardened Images 10 minutes[Migrate a Python app to DHI](https://docs.docker.com/guides/dhi-python-example/) Docker Hardened Images 10 minutes[Migrate to DHI from Docker Official Images](https://docs.docker.com/guides/dhi-from-doi/) Docker Hardened Images 10 minutes[Migrate to DHI from Wolfi](https://docs.docker.com/guides/dhi-from-wolfi/) Docker Hardened Images 10 minutes[Mocking API services in development and testing with WireMock](https://docs.docker.com/guides/wiremock/)![image](https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/javascript/javascript-original.svg) JavaScript  App development
 Distributed systems 20 minutes[Mocking OAuth services in testing with Dex](https://docs.docker.com/guides/dex/) App development
 Distributed systems 10 minutes[Monitor a Golang application with Prometheus and Grafana](https://docs.docker.com/guides/go-prometheus-monitoring/)![image](https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/go/go-original.svg) Go 45 minutes[Build a named entity recognition app](https://docs.docker.com/guides/named-entity-recognition/)![image](https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg) Python  AI 20 minutes[Node.js language-specific guide](https://docs.docker.com/guides/nodejs/)![image](https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/javascript/javascript-original.svg) JavaScript 20 minutes[PDF analysis and chat](https://docs.docker.com/guides/genai-pdf-bot/) AI 20 minutes[PHP language-specific guide](https://docs.docker.com/guides/php/)![image](https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/php/php-original.svg) PHP 20 minutes[Pre-seeding database with schema and data at startup for development environment](https://docs.docker.com/guides/pre-seeding/) App development
 Databases 20 minutes[Python language-specific guide](https://docs.docker.com/guides/python/)![image](https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg) Python 20 minutes[R language-specific guide](https://docs.docker.com/guides/r/)![image](https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/r/r-original.svg) R 10 minutes[Build a RAG application using Ollama and Docker](https://docs.docker.com/guides/rag-ollama/) AI 20 minutes[React.js language-specific guide](https://docs.docker.com/guides/reactjs/)![image](https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/javascript/javascript-original.svg) JavaScript 20 minutes[Ruby on Rails language-specific guide](https://docs.docker.com/guides/ruby/)![image](https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/ruby/ruby-original.svg) Ruby  Frameworks 20 minutes[Rust language-specific guide](https://docs.docker.com/guides/rust/)![image](https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/rust/rust-original.svg) Rust 20 minutes[Build a sentiment analysis app](https://docs.docker.com/guides/sentiment-analysis/)![image](https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg) Python  AI 20 minutes[Mastering Testcontainers Cloud by Docker: streamlining integration testing with containers](https://docs.docker.com/guides/testcontainers-cloud/) Product demo 12 minutes[Build a text recognition app](https://docs.docker.com/guides/text-classification/)![image](https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg) Python  AI 20 minutes[Build a text summarization app](https://docs.docker.com/guides/text-summarization/)![image](https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg) Python  AI 20 minutes[Use containerized databases](https://docs.docker.com/guides/databases/) Databases 20 minutes[Using Docker with Zscaler](https://docs.docker.com/guides/zscaler/) Networking
 Administration 10 minutes[GenAI video transcription and chat](https://docs.docker.com/guides/genai-video-bot/) AI 20 minutes[Visualizing your PostgreSQL databases with pgAdmin](https://docs.docker.com/guides/pgadmin/) Databases 10 minutes[Vue.js language-specific guide](https://docs.docker.com/guides/vuejs/)![image](https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/javascript/javascript-original.svg) JavaScript  Frameworks 20 minutes

---

# How can we help?

> Docker Documentation is the official Docker library of resources, manuals, and guides to help you containerize applications.

# How can we help?

      [Get startedLearn Docker basics.](https://docs.docker.com/get-started/)[GuidesOptimize your development workflows with Docker.](https://docs.docker.com/guides/)[ManualsInstall, set up, configure, and use Docker products.](https://docs.docker.com/manuals/)[ReferenceBrowse the CLI and API documentation.](https://docs.docker.com/reference/)

## Featured topics

[Docker Hardened Images](https://docs.docker.com/dhi/)[Docker Sandboxes](https://docs.docker.com/ai/sandboxes/)[Docker Desktop overview](https://docs.docker.com/desktop/)[Install Docker Engine](https://docs.docker.com/engine/install/)[Dockerfile reference](https://docs.docker.com/reference/dockerfile/)[Docker Build overview](https://docs.docker.com/build/)

---

# Manuals

> Learn how to install, set up, configure, and use Docker products with this collection of user guides

# Manuals

---

This section contains user guides on how to install, set up, configure, and use
Docker products.

## Open source

Open source development and containerization technologies.

[Docker BuildBuild and ship any application anywhere.](https://docs.docker.com/build/)[Docker EngineThe industry-leading container runtime.](https://docs.docker.com/engine/)[Docker ComposeDefine and run multi-container applications.](https://docs.docker.com/compose/)[TestcontainersRun containers programmatically in your preferred programming language.](https://docs.docker.com/testcontainers/)[CagentThe open-source multi-agent solution to assist you in your tasks.](https://docs.docker.com/ai/cagent)

## AI

All the Docker AI tools in one easy-to-access location.

[Ask GordonStreamline your workflow and get the most out of the Docker ecosystem with your personal AI assistant.](https://docs.docker.com/ai/gordon/)[Docker Model RunnerView and manage your local models.](https://docs.docker.com/ai/model-runner/)[MCP Catalog and ToolkitAugment your AI workflow with MCP servers.](https://docs.docker.com/ai/mcp-catalog-and-toolkit/)

## Products

End-to-end developer solutions for innovative teams.

[Docker DesktopYour command center for container development.](https://docs.docker.com/desktop/)[Docker Hardened ImagesSecure, minimal images for trusted software delivery.](https://docs.docker.com/dhi/)[Docker OffloadBuild and run containers in the cloud.](https://docs.docker.com/offload/)[Build CloudBuild your images faster in the cloud.](https://docs.docker.com/build-cloud/)[Docker HubDiscover, share, and integrate container images.](https://docs.docker.com/docker-hub/)[Docker ScoutImage analysis and policy evaluation.](https://docs.docker.com/scout/)[Docker ExtensionsCustomize your Docker Desktop workflow.](https://docs.docker.com/extensions/)[Testcontainers CloudRun integration tests, with real dependencies, in the cloud.](https://testcontainers.com/cloud/docs/)

## Platform

Documentation related to the Docker platform, such as administration and
subscription management.

[AdministrationCentralized observability for companies and organizations.](https://docs.docker.com/admin/)[BillingManage billing and payment methods.](https://docs.docker.com/billing/)[AccountsManage your Docker account.](https://docs.docker.com/accounts/)[SecuritySecurity guardrails for both administrators and developers.](https://docs.docker.com/security/)[SubscriptionCommercial use licenses for Docker products.](https://docs.docker.com/subscription/)

## Enterprise

Targeted at IT administrators with help on deploying Docker Desktop at scale with configuration guidance on security related features.

[Deploy Docker DesktopDeploy Docker Desktop at scale within your company](https://docs.docker.com/enterprise/enterprise-deployment/)

---

# Docker Offload

> Find documentation on Docker Offload to help you build and run your container images faster, both locally and in CI

# Docker Offload

---

Availability: Early Access
Requires: Docker Desktop 4.50 and later

Docker Offload is a fully managed service that lets you offload building and
running containers to the cloud using the Docker tools you already know. It
enables developers to work efficiently in virtual desktop infrastructure (VDI)
environments or systems that don't support nested virtualization.

In the following topics, learn about Docker Offload, how to set it up, use it
for your workflows, and troubleshoot common issues.

[QuickstartGet up and running with Docker Offload in just a few steps.](https://docs.docker.com/offload/quickstart/)[AboutLearn about Docker Offload and how it works.](https://docs.docker.com/offload/about/)[ConfigureSet up and customize your cloud build environments.](https://docs.docker.com/offload/configuration/)[Usage and billingLearn about Docker Offload usage and billing, and how to monitor your cloud resources.](https://docs.docker.com/offload/usage/)[OptimizeImprove performance and cost efficiency in Docker Offload.](https://docs.docker.com/offload/optimize/)[TroubleshootLearn how to troubleshoot issues with Docker Offload.](https://docs.docker.com/offload/troubleshoot/)[FeedbackProvide feedback on Docker Offload.](https://docs.docker.com/offload/feedback/)

---

# Release notes for Docker Home, the Admin Console, billing, security, and subscription features

> Learn about the new features, bug fixes, and breaking changes for Docker Home, the Admin Console, and billing and subscription features

# Release notes for Docker Home, the Admin Console, billing, security, and subscription features

   Table of contents

---

This page provides details on new features, enhancements, known issues, and bug fixes across Docker Home, the Admin Console, billing, security, and subscription functionalities.

## 2026-01-27

### New

- Administrators can now use an allow list with
  [Image Access
  Management](https://docs.docker.com/enterprise/security/hardened-desktop/image-access-management/)
  to approve specific repositories that bypass image access controls.

## 2025-01-30

### New

- Installing Docker Desktop via the PKG installer is now generally available.
- Enforcing sign-in via configuration profiles is now generally available.

## 2024-12-10

### New

- New Docker subscriptions are now available. For more information, see [Docker
  subscriptions and features](https://www.docker.com/pricing/) and [Announcing
  Upgraded Docker Plans: Simpler, More Value, Better Development and
  Productivity](https://www.docker.com/blog/november-2024-updated-plans-announcement/).

## 2024-11-18

### New

- Administrators can now:
  - Enforce sign-in with
    [configuration profiles](https://docs.docker.com/enterprise/security/enforce-sign-in/methods/#configuration-profiles-method-mac-only) (Early Access).
  - Enforce sign-in for more than one organization at a time (Early Access).
  - Deploy Docker Desktop for Mac in bulk with the
    [PKG installer](https://docs.docker.com/enterprise/enterprise-deployment/pkg-install-and-configure/) (Early Access).
  - [Use Desktop Settings Management via the Docker Admin Console](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/configure-admin-console/) (Early Access).

### Bug fixes and enhancements

- Enhance Container Isolation (ECI) has been improved to:
  - Permit admins to
    [turn off Docker socket mount restrictions](https://docs.docker.com/enterprise/security/hardened-desktop/enhanced-container-isolation/config/#allowing-all-containers-to-mount-the-docker-socket).
  - Support wildcard tags when using the
    [allowedDerivedImagessetting](https://docs.docker.com/enterprise/security/hardened-desktop/enhanced-container-isolation/config/#docker-socket-mount-permissions-for-derived-images).

## 2024-11-11

### New

- [Personal access tokens](https://docs.docker.com/security/access-tokens/) (PATs) now support expiration dates.

## 2024-10-15

### New

- Beta: You can now create
  [organization access tokens](https://docs.docker.com/security/for-admins/access-tokens/) (OATs) to enhance security for organizations and streamline access management for organizations in the Docker Admin Console.

## 2024-08-29

### New

- Deploying Docker Desktop via the
  [MSI installer](https://docs.docker.com/enterprise/enterprise-deployment/msi-install-and-configure/) is now generally available.
- Two new methods to
  [enforce sign-in](https://docs.docker.com/enterprise/security/enforce-sign-in/) (Windows registry key and `.plist` file) are now generally available.

## 2024-08-24

### New

- Administrators can now view
  [organization Insights](https://docs.docker.com/admin/organization/insights/).

## 2024-07-17

### New

- You can now centrally access and manage Docker products in [Docker Home](https://app.docker.com).

---

# Reference documentation

> Find reference documentation for the Docker platform’s various APIs, CLIs, and file formats

# Reference documentation

---

This section includes the reference documentation for the Docker platform's
various APIs, CLIs, drivers and specifications, and file formats.

## File formats

[DockerfileDefines the contents and startup behavior of a single container.](https://docs.docker.com/reference/dockerfile/)[Compose fileDefines a multi-container application.](https://docs.docker.com/reference/compose-file/)

## Command-line interfaces (CLIs)

[Docker CLIThe main Docker CLI, includes alldockercommands.](https://docs.docker.com/reference/cli/docker/)[Compose CLIThe CLI for Docker Compose, for building and running multi-container applications.](https://docs.docker.com/reference/cli/docker/compose/)[Daemon CLI (dockerd)Persistent process that manages containers.](https://docs.docker.com/reference/cli/dockerd/)

## Application programming interfaces (APIs)

[Engine APIThe main API for Docker, provides programmatic access to a daemon.](https://docs.docker.com/reference/api/engine/)[Docker Hub APIAPI to interact with Docker Hub.](https://docs.docker.com/reference/api/hub/latest/)[DVP Data APIAPI for Docker Verified Publishers to fetch analytics data.](https://docs.docker.com/reference/api/dvp/latest/)[Registry APIAPI for Docker Registry.](https://docs.docker.com/reference/api/registry/latest/)

---

# Docker's product release lifecycle

> Describes the various stages of feature lifecycle from beta to GA.

# Docker's product release lifecycle

   Table of contents

---

This page details Docker's product release lifecycle and how Docker defines each stage. It also provides information on the product retirement process. Features and products may progress through some or all of these phases.

> Note
>
> Our [Subscription Service Agreement](https://www.docker.com/legal/docker-subscription-service-agreement) governs your use of Docker and covers details of eligibility, content, use, payments and billing, and warranties. This document is not a contract and all use of Docker’s services are subject to Docker’s [Subscription Service Agreement](https://www.docker.com/legal/docker-subscription-service-agreement).

## Lifecycle stage

| Lifecycle stage | Customer availability | Support availability | Limitations | Retirement |
| --- | --- | --- | --- | --- |
| Experimental | Limited availability | Community support | Software may have limitations, bugs and/or stability concerns | Can be discontinued without notice |
| Beta | All or those involved in a Beta Feedback Program | Community support | Software may have limitations, bugs and/or stability concerns | Can be discontinued without notice |
| Early Access (EA) | All or those involved in an Early Access Feedback Program | Full | Software may have limitations, bugs and/or stability concerns. These limitations will be documented. | Follows theretirement process |
| General Availability (GA) | All | Full | Few or no limitations for supported use cases | Follows theretirement process |

### Experimental

Experimental offerings are features that Docker is currently experimenting with. Customers who access experimental features have the opportunity to test, validate, and provide feedback on future functionality. This helps us focus our efforts on what provides the most value to our customers.

**Customer availability:** Availability of experimental features is limited. A portion of users may have access to none, one or many experimental features.

**Support:** Support for experimental features is best effort via Community support channels and forums.

**Limitations:** Experimental features may have potentially significant limitations such as functional limitations, performance limitations, and API limitations. Features and programmatic interfaces may change at any time without notice.

**Retirement:** During the experimental period, Docker will determine whether to continue an offering through its lifecycle. We reserve the right to change the scope of or discontinue an Experimental product or feature at any point in time without notice, as outlined in our [Subscription Service Agreement](https://www.docker.com/legal/docker-subscription-service-agreement).

### Beta

Beta offerings are initial releases of potential future products or features. Customers who participate in our beta programs have the opportunity to test, validate, and provide feedback on future functionality. This helps us focus our efforts on what provides the most value to our customers.

**Customer availability:** Participation in beta releases is by invitation or via use of clearly identified beta features in product. Beta invitations may be public or private.

**Support:** Support for beta features is best effort via Community support channels and forums.

**Limitations:** Beta releases may have potentially significant limitations such as functional limitations, performance limitations, and API limitations. Features and programmatic interfaces may change at any time without notice.

**Retirement:** During the beta period, Docker will determine whether to continue an offering through its lifecycle. We reserve the right to change the scope of or discontinue a Beta product or feature at any point in time without notice, as outlined in our [Subscription Service Agreement](https://www.docker.com/legal/docker-subscription-service-agreement).

### Early Access (EA)

Early Access offerings are products or features that may have potential feature limitations and are enabled for specific user groups as part of an incremental roll-out strategy. They are ready to be released to the world, pending some fine tuning.

**Customer availability:** Early Access functionality can be rolled out to all customers or specific segments of users in addition to or in place of existing functionality.

**Support:** Early Access offerings are provided with the same level of support as General Availability features and products.

**Limitations:** Early Access releases may have potentially significant limitations such as functional limitations, performance limitations, and API limitations, though these limitations will be documented. Breaking changes to features and programmatic interfaces will follow the [retirement process](#retirement-process) outlined below.

**Retirement:** In the event we retire an Early Access product before General Availability, we will strive to follow the [retirement process](#retirement-process) outlined below.

### General Availability (GA)

General Availability offerings are fully functional products or features that are openly accessible to all Docker customers.

**Customer availability:** All Docker users have access to GA offerings according to their subscription levels.

**Limitations:** General Availability features and products will have few or no limitations for supported use cases.

**Support:** All GA offerings are fully supported, as described in our [support page](https://www.docker.com/support/).

**Retirement:** General Availability offerings follow the [retirement process](#retirement-process) outlined below.

## Retirement process

The decision to retire or deprecate features follows a rigorous process including understanding the demand, use, impact of feature retirement and, most importantly, customer feedback. Our goal is to invest resources in areas that will add the most value for the most customers

Docker is committed to being clear, transparent, and proactive when interacting with our customers, especially about changes to our platform. To that end, we will make best efforts to follow these guidelines when retiring functionality:

- **Advance notice:** For retirement of major features or products, we will attempt to notify customers at least 6 months in advance.
- **Viable alternatives:** Docker will strive to provide viable alternatives to our customers when retiring functionality. These may be alternative offerings from Docker or recommended alternatives from 3rd party providers. Where possible and appropriate, Docker will automatically migrate customers to alternatives for retired functionality.
- **Continued support:** Docker commits to providing continued support for functionality until its retirement date.

We may need to accelerate the timeline for retirement of functionality in extenuating circumstances, such as essential changes necessary to protect the integrity of our platform or the security of our customers and others. In these cases, it is important that those changes occur as quickly as possible.

Similarly, integrated third party software or services may need to be retired due to the third-party decision to change or retire their solution. In these situations, the pace of retirement will be out of our control.

However, even under these circumstances, we will provide as much advance notice as possible.
