# Deprecated and retired Docker products and features and more

# Deprecated and retired Docker products and features

> Explore deprecated and retired Docker features, products, and open source projects, including details on transitioned tools and archived initiatives.

# Deprecated and retired Docker products and features

   Table of contents

---

This document provides an overview of Docker features, products, and
open-source projects that have been deprecated, retired, or transitioned.

> Note
>
> This page does not cover deprecated and removed Docker Engine features.
> For a detailed list of deprecated Docker Engine features, refer to the
> [Docker Engine Deprecated Features documentation](https://docs.docker.com/engine/deprecated/).

## Products and features

Support for these deprecated or retired features is no longer provided by
Docker, Inc. The projects that have been transitioned to third parties continue
to receive updates from their new maintainers.

### Docker Machine

Docker Machine was a tool for provisioning and managing Docker hosts across
various platforms, including virtual machines and cloud providers. It is no
longer maintained, and users are encouraged to use
[Docker Desktop](https://docs.docker.com/desktop/)
or
[Docker Engine](https://docs.docker.com/engine/) directly on supported platforms.
Machine's approach to creating and configuring hosts has been superseded by
more modern workflows that integrate more closely with Docker Desktop.

### Docker Toolbox

Docker Toolbox was used on older systems where Docker Desktop could not run. It
bundled Docker Machine, Docker Engine, and Docker Compose into a single
installer. Toolbox is no longer maintained and is effectively replaced by
[Docker Desktop](https://docs.docker.com/desktop/) on current systems. References to
Docker Toolbox occasionally appear in older documentation or community
tutorials, but it is not recommended for new installations.

### Docker Cloud integrations

Docker previously offered integrations for Amazon's Elastic Container Service
(ECS) and Azure Container Instances (ACI) to streamline container workflows.
These integrations have been deprecated, and users should now rely on native
cloud tools or third-party solutions to manage their workloads. The move toward
platform-specific or universal orchestration tools reduced the need for
specialized Docker Cloud integrations.

You can still view the relevant documentation for these integrations in the
[Compose CLI repository](https://github.com/docker-archive/compose-cli/tree/main/docs).

### Docker Enterprise Edition

Docker Enterprise Edition (EE) was Docker's commercial platform for deploying
and managing large-scale container environments. It was acquired by Mirantis in
2019, and users looking for enterprise-level functionality can now explore
Mirantis Kubernetes Engine or other products offered by Mirantis. Much of the
technology and features found in Docker EE have been absorbed into the Mirantis
product line.

> Note
>
> For information about enterprise-level features offered by Docker today,
> see the [Docker Business subscription](https://www.docker.com/pricing/).

### Docker Data Center and Docker Trusted Registry

Docker Data Center (DDC) was an umbrella term that encompassed Docker Universal
Control Plane (UCP) and Docker Trusted Registry (DTR). These components
provided a full-stack solution for managing containers, security, and registry
services in enterprise environments. They are now under the Mirantis portfolio
following the Docker Enterprise acquisition. Users still encountering
references to DDC, UCP, or DTR should refer to Mirantis's documentation for
guidance on modern equivalents.

### Dev Environments

Dev Environments was a feature introduced in Docker Desktop that allowed
developers to spin up development environments quickly. It was deprecated and removed from Docker Desktop version 4.42 and later. Similar workflows can be achieved through
Docker Compose or by creating custom configurations tailored to specific
project requirements.

### GitHub Copilot extension

The Docker for GitHub Copilot extension integrated Docker capabilities with
GitHub Copilot Chat, helping developers containerize applications, generate
Docker assets, and analyze vulnerabilities through conversational prompts. The
extension was available in early access on the GitHub Marketplace. GitHub
[deprecated Copilot Extensions](https://github.blog/changelog/2025-09-24-deprecate-github-copilot-extensions-github-apps/)
which led to the retirement of the Docker for GitHub Copilot extension. If
you're looking for AI-assisted Docker workflows, explore the Docker MCP Toolkit
and MCP Catalog, or use Ask Gordon in Docker Desktop and the Docker CLI.

## Open source projects

Several open-source projects originally maintained by Docker have been
archived, discontinued, or transitioned to other maintainers or organizations.

### Registry (now CNCF Distribution)

The Docker Registry served as the open-source implementation of a container
image registry. It was donated to the Cloud Native Computing Foundation (CNCF)
in 2019 and is maintained under the name "Distribution." It remains a
cornerstone for managing and distributing container images.

[CNCF Distribution](https://github.com/distribution/distribution)

### Docker Compose v1 (replaced by Compose v2)

Docker Compose v1 (`docker-compose`), a Python-based tool for defining
multi-container applications, has been superseded by Compose v2 (`docker compose`), which is written in Go and integrates with the Docker CLI. Compose
v1 is no longer maintained, and users should migrate to Compose v2.

[Compose v2 Documentation](https://docs.docker.com/compose/)

### InfraKit

InfraKit was an open-source toolkit designed to manage declarative
infrastructure and automate container deployments. It has been archived, and
users are encouraged to explore tools such as Terraform for infrastructure
provisioning and orchestration.

[InfraKit GitHub Repository](https://github.com/docker/infrakit)

### Docker Notary (now CNCF Notary)

Docker Notary was a system for signing and verifying the authenticity of
container content. It was donated to the CNCF in 2017 and continues to be
developed as "Notary." Users seeking secure content verification should consult
the CNCF Notary project.

[CNCF Notary](https://github.com/notaryproject/notary)

### SwarmKit

SwarmKit powers Docker Swarm mode by providing orchestration for container
deployments. While Swarm mode remains functional, development has slowed in
favor of Kubernetes-based solutions. Individuals evaluating container
orchestration options should investigate whether SwarmKit meets modern workload
requirements.

[SwarmKit GitHub Repository](https://github.com/docker/swarmkit)

---

# Docker Scout

> Get an overview on Docker Scout to proactively enhance your software supply chain security

# Docker Scout

---

Container images consist of layers and software packages, which are susceptible to vulnerabilities.
These vulnerabilities can compromise the security of containers and applications.

Docker Scout is a solution for proactively enhancing your software supply chain security.
By analyzing your images, Docker Scout compiles an inventory of components, also known as a Software Bill of Materials (SBOM).
The SBOM is matched against a continuously updated vulnerability database to pinpoint security weaknesses.

Docker Scout is a standalone service and platform that you can interact with
using Docker Desktop, Docker Hub, the Docker CLI, and the Docker Scout Dashboard.
Docker Scout also facilitates integrations with third-party systems, such as container registries and CI platforms.

[QuickstartLearn what Docker Scout can do, and how to get started.](https://docs.docker.com/scout/quickstart/)[Image analysisReveal and dig into the composition of your images.](https://docs.docker.com/scout/image-analysis/)[Advisory databaseLearn about the information sources that Docker Scout uses.](https://docs.docker.com/scout/advisory-db-sources/)[IntegrationsConnect Docker Scout with your CI, registries, and other third-party services.](https://docs.docker.com/scout/integrations/)[DashboardThe web interface for Docker Scout.](https://docs.docker.com/scout/dashboard/)[PolicyEnsure that your artifacts align with supply chain best practices.](https://docs.docker.com/scout/policy/)[UpgradeA Personal subscription includes up to 1 repository. Upgrade for more.](https://docs.docker.com/subscription/change/)

---

# Security for developers

> Learn about developer-level security features like 2FA and access tokens

# Security for developers

   Table of contents

---

Docker helps you protect your local environments, infrastructure, and networks
with its developer-level security features.

Use tools like two-factor authentication (2FA), personal access tokens, and
Docker Scout to manage access and detect vulnerabilities early in your workflow.
You can also integrate secrets securely into your development stack using Docker Compose,
or enhance your software supply security with Docker Hardened Images.

Explore the following sections to learn more.

## For developers

[Set up two-factor authenticationAdd an extra layer of authentication to your Docker account.](https://docs.docker.com/security/2fa/)[Manage access tokensCreate personal access tokens as an alternative to your password.](https://docs.docker.com/security/access-tokens/)[Static vulnerability scanningAutomatically run a point-in-time scan on your Docker images for vulnerabilities.](https://docs.docker.com/docker-hub/repos/manage/vulnerability-scanning/)[Docker Engine securityUnderstand how to keep Docker Engine secure.](https://docs.docker.com/engine/security/)[Secrets in Docker ComposeLearn how to use secrets in Docker Compose.](https://docs.docker.com/compose/how-tos/use-secrets/)

## More resources

[Security FAQsExplore common security FAQs.](https://docs.docker.com/faq/security/general/)[Security best practicesUnderstand the steps you can take to improve the security of your container.](https://docs.docker.com/develop/security-best-practices/)[Suppress CVEs with VEXLearn how to suppress non-applicable or fixed vulnerabilities found in your images.](https://docs.docker.com/scout/guides/vex/)[Docker Hardened ImagesLearn how to use Docker Hardened Images to enhance your software supply security.](https://docs.docker.com/dhi/)

---

# Subscription

> Learn about Docker subscription features and how to manage your subscription

# Subscription

---

Docker subscriptions provide licensing for commercial use of Docker products including Docker Desktop, Docker Hub, Docker Build Cloud, Docker Scout, and Testcontainers Cloud.

Use these resources to choose the right subscription for your needs or manage your existing subscription.

[Compare Docker subscriptionsVisit the pricing page to see what's included in different Docker subscriptions.](https://www.docker.com/pricing/)[Set up your subscriptionGet started setting up a personal or organization subscription.](https://docs.docker.com/subscription/setup/)[Scale your subscriptionScale your subscription to fit your needs.](https://docs.docker.com/subscription/scale/)[Change your subscriptionLearn how to upgrade or downgrade your subscription.](https://docs.docker.com/subscription/change/)[Manage seatsLearn how to add or remove seats from your subscription.](https://docs.docker.com/subscription/manage-seats/)[Docker Desktop license agreementReview the terms of the Docker Subscription Service Agreement.](https://docs.docker.com/subscription/desktop-license/)[Subscription FAQsFind the answers you need and explore common questions.](https://docs.docker.com/subscription/faq/)

---

# Get support for Docker products

> Learn about support options for Docker products including paid subscriptions and community resources

# Get support for Docker products

   Table of contents

---

Docker offers multiple support channels depending on your subscription level and needs.

## Paid subscription support

All Docker Pro, Team, and Business subscribers receive email support for Docker products.

### Support response times

- Docker Pro: 3 business day response
- Docker Team: 2 business day response, 24×5 availability
- Docker Business: 1 business day response, 24×5 availability

> Note
>
> Premium Support with faster response times and 24×7 availability is available as an add-on for Docker Business subscribers.

For detailed support features and response times, see [Docker Pricing](https://www.docker.com/pricing/).

### Support severity levels

| Level | Description |
| --- | --- |
| Critical | Widespread or company-wide service outage affecting many customers or all users within a single organization. Business operations are halted with no workaround available. |
| High | Team or department-level impact preventing significant users from accessing core functionality. Severe business impact with no workaround exists. |
| Medium | Individual user or small group impact causing partial loss of functionality. Business operations continue, often with workarounds available but reduced productivity. |

### Request support

> Tip
>
> Before reaching out for support, review the troubleshooting documentation for your product.

If you have a paid Docker subscription, [contact the Support team](https://hub.docker.com/support/contact/).

## Community support

All Docker users can seek support through community resources, where Docker or the community respond on a best effort basis:

- [Docker Community Forums](https://forums.docker.com/)
- [Docker Community Slack](http://dockr.ly/comm-slack)

## Docker Desktop support

Docker Desktop support is available with a paid subscription.

### Scope of support

Docker Desktop support includes:

- Account management and billing
- Configuration and installation issues
- Desktop updates
- Sign-in issues
- Push or pull issues, including rate limiting
- Application crashes or unexpected behavior
- Automated builds
- Basic product 'how to' questions

**Windows-specific:**

- Turning on virtualization in BIOS
- Turning on Windows features
- Running inside
  [certain VM or VDI environments](https://docs.docker.com/desktop/setup/vm-vdi/) (Docker Business only)

Docker Desktop support excludes:

- Unsupported operating systems, including beta/preview versions
- Running containers of a different architecture using emulation
- Docker Engine, Docker CLI, or other bundled Linux components
- Kubernetes
- Features labeled as experimental
- System/Server administration activities
- Desktop as a production runtime
- Scale deployment/multi-machine installation
- Routine product maintenance (data backup, disk space, log rotation)
- Third-party applications not provided by Docker
- Altered or modified Docker software
- Hardware malfunction, abuse, or improper use
- Versions older than the latest release (except Docker Business)
- Training, customization, and integration
- Running multiple instances on a single machine

> Note
>
> Support for
> [running Docker Desktop in a VM or VDI environment](https://docs.docker.com/desktop/setup/vm-vdi/) is only available to Docker Business customers.

### Supported versions

- Docker Business: Versions up to six months older than the latest version (fixes applied to latest version only)
- Docker Pro and Team: Latest version only

### Number of machines

- Docker Pro: One machine
- Docker Team: Number of machines equal to subscription seats
- Docker Business: Unlimited machines

### Supported operating systems

- [Mac system requirements](https://docs.docker.com/desktop/setup/install/mac-install/#system-requirements)
- [Windows system requirements](https://docs.docker.com/desktop/setup/install/windows-install/#system-requirements)
- [Linux system requirements](https://docs.docker.com/desktop/setup/install/linux/#system-requirements)

### Community resources

- [Docker Desktop issue tracker](https://github.com/docker/desktop-feedback)

### Diagnostic data and privacy

When uploading diagnostics, the bundle may contain personal data such as usernames and IP addresses. Diagnostics bundles are only accessible to Docker, Inc. employees directly involved in diagnosing issues.

By default, Docker, Inc. deletes uploaded diagnostics bundles after 30 days. You may request removal of a diagnostics bundle by specifying the diagnostics ID or your GitHub ID. Docker, Inc. only uses the data to investigate specific user issues but may derive high-level (non-personal) metrics.

For more information, see [Docker Data Processing Agreement](https://www.docker.com/legal/data-processing-agreement).

---

# Tags

# Tags

Here you can browse Docker docs by tag.

- [Administration](https://docs.docker.com/tags/admin/)
  (19 pages)
- [AI](https://docs.docker.com/tags/ai/)
  (12 pages)
- [App development](https://docs.docker.com/tags/app-dev/)
  (5 pages)
- [Best practices](https://docs.docker.com/tags/best-practices/)
  (4 pages)
- [Cloud services](https://docs.docker.com/tags/cloud-services/)
  (1 page)
- [Data science](https://docs.docker.com/tags/data-science/)
  (1 page)
- [Databases](https://docs.docker.com/tags/databases/)
  (3 pages)
- [Deployment](https://docs.docker.com/tags/deploy/)
  (3 pages)
- [DevOps](https://docs.docker.com/tags/devops/)
  (5 pages)
- [Docker Hardened Images](https://docs.docker.com/tags/dhi/)
  (5 pages)
- [Distributed systems](https://docs.docker.com/tags/distributed-systems/)
  (3 pages)
- [FAQ](https://docs.docker.com/tags/faq/)
  (21 pages)
- [Frameworks](https://docs.docker.com/tags/frameworks/)
  (3 pages)
- [Networking](https://docs.docker.com/tags/networking/)
  (2 pages)
- [Observability](https://docs.docker.com/tags/observability/)
  (1 page)
- [Product demo](https://docs.docker.com/tags/product-demo/)
  (4 pages)
- [Release notes](https://docs.docker.com/tags/release-notes/)
  (8 pages)
- [Secrets](https://docs.docker.com/tags/secrets/)
  (4 pages)
- [Troubleshooting](https://docs.docker.com/tags/troubleshooting/)
  (12 pages)

---

# Testcontainers

> Learn how to use Testcontainers to run containers programmatically in your preferred programming language.

# Testcontainers

   Table of contents

---

Testcontainers is a set of open source libraries that provides easy and lightweight APIs for bootstrapping local development and test dependencies with real services wrapped in Docker containers.
Using Testcontainers, you can write tests that depend on the same services you use in production without mocks or in-memory services.

[What is Testcontainers?Learn about what Testcontainers does and its key benefits](https://testcontainers.com/getting-started/#what-is-testcontainers)[The Testcontainers workflowUnderstand the Testcontainers workflow](https://testcontainers.com/getting-started/#testcontainers-workflow)

## Quickstart

### Supported languages

Testcontainers provide support for the most popular languages, and Docker sponsors the development of the following Testcontainers implementations:

- [Go](https://golang.testcontainers.org/quickstart/)
- [Java](https://java.testcontainers.org/quickstart/junit_5_quickstart/)

The rest are community-driven and maintained by independent contributors.

### Prerequisites

Testcontainers requires a Docker-API compatible container runtime.
During development, Testcontainers is actively tested against recent versions of Docker on Linux, as well as against Docker Desktop on Mac and Windows.
These Docker environments are automatically detected and used by Testcontainers without any additional configuration being necessary.

It is possible to configure Testcontainers to work for other Docker setups, such as a remote Docker host or Docker alternatives.
However, these are not actively tested in the main development workflow, so not all Testcontainers features might be available
and additional manual configuration might be necessary.

If you have further questions about configuration details for your setup or whether it supports running Testcontainers-based tests,
contact the Testcontainers team and other users from the Testcontainers community on [Slack](https://slack.testcontainers.org/).

[Testcontainers for GoA Go package that makes it simple to create and clean up container-based dependencies for automated integration/smoke tests.](https://golang.testcontainers.org/quickstart/)[Testcontainers for JavaA Java library that supports JUnit tests, providing lightweight, throwaway instances of anything that can run in a Docker container.](https://java.testcontainers.org/)
