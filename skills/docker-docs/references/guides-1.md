# Communication and information gathering and more

# Communication and information gathering

> Gather your company's requirements from key stakeholders and communicate to your developers.

# Communication and information gathering

   Table of contents

---

## Communicate with your developers and IT teams

Before rolling out Docker Desktop across your organization, coordinate with key stakeholders to ensure a smooth transition.

### Notify Docker Desktop users

You may already have Docker Desktop users within your company. Some steps in
this onboarding process may affect how they interact with the platform.

Communicate early with users to inform them that:

- They'll be upgraded to a supported version of Docker Desktop as part of the subscription onboarding
- Settings will be reviewed and optimized for productivity
- They'll need to sign in to the company's Docker organization using their
  business email to access subscription benefits

### Engage with your MDM team

Device management solutions, such as Intune and Jamf, are commonly used for
software distribution across enterprises. These tools are typically managed by a dedicated MDM team.

Engage with this team early in the process to:

- Understand their requirements and lead time for deploying changes
- Coordinate the distribution of configuration files

Several setup steps in this guide require JSON files, registry keys, or .plist
files to be distributed to developer machines. Use MDM tools to deploy these configuration files and ensure their integrity.

## Identify Docker organizations

Some companies may have more than one
[Docker organization](https://docs.docker.com/admin/organization/) created. These
organizations may have been created for specific purposes, or may not be
needed anymore.

If you suspect your company has multiple Docker organizations:

- Survey your teams to see if they have their own organizations
- Contact your Docker Support to get a list of organizations with users whose
  emails match your domain name

## Gather requirements

[Settings Management](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/) lets you preset numerous configuration parameters for Docker Desktop.

Work with the following stakeholders to establish your company's baseline
configuration:

- Docker organization owner
- Development lead
- Information security representative

Review these areas together:

- Security features and
  [enforcing sign-in](https://docs.docker.com/enterprise/security/enforce-sign-in/)
  for Docker Desktop users
- Additional Docker products included in your subscriptions

To view the parameters that can be preset, see
[Configure Settings Management](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/configure-json-file/#step-two-configure-the-settings-you-want-to-lock-in).

## Optional: Meet with the Docker Implementation team

The Docker Implementation team can help you set up your organization,
configure SSO, enforce sign-in, and configure Docker Desktop.

To schedule a meeting, email [successteam@docker.com](mailto:successteam@docker.com).

---

# Deploy your Docker setup

> Deploy your Docker setup across your company.

# Deploy your Docker setup

   Table of contents

---

> Warning
>
> Communicate with your users before proceeding, and confirm that your IT and
> MDM teams are prepared to handle any unexpected issues, as these steps will
> affect all existing users signing into your Docker organization.

## Enforce SSO

Enforcing SSO means that anyone who has a Docker profile with an email address
that matches your verified domain must sign in using your SSO connection. Make
sure the Identity provider groups associated with your SSO connection cover all
the developer groups that you want to have access to the Docker subscription.

For instructions on how to enforce SSO, see
[Enforce SSO](https://docs.docker.com/enterprise/security/single-sign-on/connect/).

## Deploy configuration settings and enforce sign-in to users

Have the MDM team deploy the configuration files for Docker to all users.

## Next steps

Congratulations, you've successfully completed the admin implementation process
for Docker.

To continue optimizing your Docker environment:

- Review your
  [organization's usage data](https://docs.docker.com/admin/organization/insights/) to track adoption
- Monitor
  [Docker Scout findings](https://docs.docker.com/scout/explore/analysis/) for security insights
- Explore
  [additional security features](https://docs.docker.com/enterprise/security/) to enhance your configuration

---

# Finalize plans and begin setup

> Collaborate with your MDM team to distribute configurations and set up SSO and Docker product trials.

# Finalize plans and begin setup

   Table of contents

---

## Send finalized settings files to the MDM team

After reaching an agreement with the relevant teams about your baseline and
security configurations as outlined in the previous section, configure Settings Management using either the
[Docker Admin Console](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/configure-admin-console/) or an
[admin-settings.jsonfile](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/configure-json-file/).

Once the file is ready, collaborate with your MDM team to deploy your chosen
settings, along with your chosen method for
[enforcing sign-in](https://docs.docker.com/enterprise/security/enforce-sign-in/).

> Important
>
> Test this first with a small number of Docker Desktop developers to verify the functionality works as expected before deploying more widely.

## Manage your organizations

If you have more than one organization, consider either
[consolidating them
into one organization](https://docs.docker.com/admin/organization/orgs/) or creating a
[Docker company](https://docs.docker.com/admin/company/) to manage multiple
organizations.

## Begin setup

### Set up single sign-on and domain verification

Single sign-on (SSO) lets developers authenticate using their identity
providers (IdPs) to access Docker. SSO is available for a whole company and all associated organizations, or an individual organization that has a Docker
Business subscription. For more information, see the
[documentation](https://docs.docker.com/enterprise/security/single-sign-on/).

You can also enable
[SCIM](https://docs.docker.com/enterprise/security/provisioning/scim/)
for further automation of provisioning and deprovisioning of users.

### Set up Docker product entitlements included in the subscription

[Docker Build Cloud](https://docs.docker.com/build-cloud/) significantly reduces
build times, both locally and in CI, by providing a dedicated remote builder
and shared cache. Powered by the cloud, developer time and local resources are
freed up so your team can focus on more important things, like innovation.
To get started, [set up a cloud builder](https://app.docker.com/build/).

[Docker Scout](https://docs.docker.com/scout/) is a solution for proactively enhancing
your software supply chain security. By analyzing your images, Docker Scout
compiles an inventory of components, also known as a Software Bill of Materials
(SBOM). The SBOM is matched against a continuously updated vulnerability
database to pinpoint security weaknesses. To get started, see
[Quickstart](https://docs.docker.com/scout/quickstart/).

[Testcontainers Cloud](https://testcontainers.com/cloud/docs/) allows
developers to run containers in the cloud, removing the need to run heavy
containers on your local machine.

[Docker Hardened Images](https://docs.docker.com/dhi/) are minimal, secure, and production-ready container base and application images maintained by Docker.
Designed to reduce vulnerabilities and simplify compliance, DHIs integrate
easily into your existing Docker-based workflows with little to no retooling
required.

### Ensure you're running a supported version of Docker Desktop

> Warning
>
> This step could affect the experience for users on older versions of Docker
> Desktop.

Existing users may be running outdated or unsupported versions of
Docker Desktop. All users should update to a supported version. Docker Desktop
versions released within the past 6 months from the latest release are supported.

Use an MDM solution to manage the version of Docker Desktop for users. Users
may also get Docker Desktop directly from Docker or through a company software
portal.

---

# Testing

> Test your Docker setup.

# Testing

   Table of contents

---

## SSO and SCIM testing

Test SSO and SCIM by signing in to Docker Desktop or Docker Hub with the email
address linked to a Docker account that is part of the verified domain.
Developers who sign in using their Docker usernames remain unaffected by the
SSO and SCIM setup.

> Important
>
> Some users may need CLI based logins to Docker Hub, and for this they will
> need a
> [personal access token (PAT)](https://docs.docker.com/security/access-tokens/).

## Test Registry Access Management and Image Access Management

> Warning
>
> Communicate with your users before proceeding, as this step will impact all
> existing users signing into your Docker organization.

If you plan to use
[Registry Access Management (RAM)](https://docs.docker.com/enterprise/security/hardened-desktop/registry-access-management/) and/or
[Image Access Management (IAM)](https://docs.docker.com/enterprise/security/hardened-desktop/image-access-management/):

1. Ensure your test developer signs in to Docker Desktop using their
  organization credentials
2. Have them attempt to pull an unauthorized image or one from a disallowed
  registry via the Docker CLI
3. Verify they receive an error message indicating that the registry is
  restricted by the organization

## Deploy settings and enforce sign in to test group

Deploy the Docker settings and enforce sign-in for a small group of test users
via MDM. Have this group test their development workflows with containers on
Docker Desktop and Docker Hub to ensure all settings and the sign-in enforcement
function as expected.

## Test Docker Build Cloud capabilities

Have one of your Docker Desktop testers
[connect to the cloud builder you created and use it to build](https://docs.docker.com/build-cloud/usage/).

## Test Testcontainers Cloud

Have a test developer [connect to Testcontainers Cloud](https://testcontainers.com/cloud/docs/#getting-started) and run a container in
the cloud to verify the setup is working correctly.

## Verify Docker Scout monitoring of repositories

Check the [Docker Scout dashboard](https://scout.docker.com/) to confirm that
data is being properly received for the repositories where Docker Scout has
been enabled.

## Verify access to Docker Hardened Images

Have a test developer attempt to
[pull a Docker Hardened Image](https://docs.docker.com/dhi/get-started/) to confirm that
the team has proper access and can integrate these images into their workflows.

---

# Set up your company for success with Docker

> Learn how to onboard your company and take advantage of all of the Docker products and features.

# Set up your company for success with Docker

Table of contents

---

Docker's tools provide a scalable, secure platform that empowers your
developers to create, ship, and run applications faster. As an administrator,
you can streamline workflows, standardize development environments, and ensure
smooth deployments across your organization.

By configuring Docker products to suit your company's needs, you can optimize
performance, simplify user management, and maintain control over resources.
This guide helps you set up and configure Docker products to maximize
productivity and success for your team while meeting compliance and security
policies.

## Who’s this for?

- Administrators responsible for managing Docker environments within their
  organization
- IT leaders looking to streamline development and deployment workflows
- Teams aiming to standardize application environments across multiple users
- Organizations seeking to optimize their use of Docker products for greater
  scalability and efficiency
- Organizations with a
  [Docker Business subscription](https://www.docker.com/pricing/)

## What you’ll learn

- Why signing into your company's Docker organization provides access to usage
  data and enhanced functionality
- How to standardize Docker Desktop versions and settings to create a consistent
  baseline for all users, while allowing flexibility for advanced developers
- Strategies for implementing Docker's security configurations to meet company
  IT and software development security requirements without hindering developer productivity

## Features covered

This guide covers the following Docker features:

- [Organizations](https://docs.docker.com/admin/organization/): The core structure
  for managing your Docker environment, grouping users, teams, and image
  repositories. Your organization was created with your subscription and is
  managed by one or more owners. Users signed into the organization are
  assigned seats based on the purchased subscription.
- [Enforce sign-in](https://docs.docker.com/enterprise/security/enforce-sign-in/):
  By default, Docker Desktop doesn't require sign-in. You can configure
  settings to enforce this and ensure your developers sign in to your
  Docker organization.
- [SSO](https://docs.docker.com/enterprise/security/single-sign-on/): Without SSO,
  user management in a Docker organization is manual. Setting
  up an SSO connection between your identity provider and Docker ensures
  compliance with your security policy and automates user provisioning. Adding
  SCIM further automates user provisioning and de-provisioning.
- General and security settings: Configuring key settings ensures smooth
  onboarding and usage of Docker products within your environment. You can also
  enable security features based on your company's specific security needs.

## Who needs to be involved

- Docker organization owner: Must be involved in the process and is required
  for several key steps
- DNS team: Needed during the SSO setup to verify the company domain
- MDM team: Responsible for distributing Docker-specific configuration files to
  developer machines
- Identity Provider team: Required for configuring the identity provider and
  establishing the SSO connection during setup
- Development lead: A development lead with knowledge of Docker configurations
  to help establish a baseline for developer settings
- IT team: An IT representative familiar with company desktop policies to
  assist with aligning Docker configuration to those policies
- Infosec: A security team member with knowledge of company development
  security policies to help configure security features
- Docker testers: A small group of developers to test the new settings and
  configurations before full deployment

## Tools integration

This guide covers integration with:

- Okta
- Entra ID SAML 2.0
- Azure Connect (OIDC)
- MDM solutions like Intune

## Modules

1. [Communication and information gathering](https://docs.docker.com/guides/admin-set-up/comms-and-info-gathering/)
  Gather your company's requirements from key stakeholders and communicate to your developers.
2. [Finalize plans and begin setup](https://docs.docker.com/guides/admin-set-up/finalize-plans-and-setup/)
  Collaborate with your MDM team to distribute configurations and set up SSO and Docker product trials.
3. [Testing](https://docs.docker.com/guides/admin-set-up/testing/)
  Test your Docker setup.
4. [Deploy your Docker setup](https://docs.docker.com/guides/admin-set-up/deploy/)
  Deploy your Docker setup across your company.

---

# Monitoring and insights

> Track user actions, team workflows, and organizational trends with Activity logs and Insights to enhance security and productivity in Docker.

# Monitoring and insights

   Table of contents

---

Activity logs and Insights are useful tools for user and access management in Docker. They provide visibility into user actions, team workflows, and organizational trends, helping enhance security, ensure compliance, and boost productivity.

## Activity logs

Activity logs track events at the organization and repository levels, offering a clear view of activities like repository changes, team updates, and billing adjustments.

Activity logs are available for Docker Team or Docker Business plans, with data retained for three months.

### Key features

- Change tracking: View what changed, who made the change, and when.
- Comprehensive reporting: Monitor critical events such as repository creation, deletion, privacy changes, and role assignments.

### Example scenarios

- Audit trail for security: A repository’s privacy settings were updated unexpectedly. The activity logs reveal which user made the change and when, helping administrators address potential security risks.
- Team collaboration review: Logs show which team members pushed updates to a critical repository, ensuring accountability during a development sprint.
- Billing adjustments: Track who added or removed subscription seats to maintain budgetary control and compliance.

For more information, see
[Activity logs](https://docs.docker.com/admin/organization/activity-logs/).

## Insights

Insights provide data-driven views of Docker usage to improve team productivity and resource allocation.

### Key benefits

- Standardized environments: Ensure consistent configurations and enforce best practices across teams.
- Improved visibility: Monitor metrics like Docker Desktop usage, builds, and container activity to understand team workflows and engagement.
- Optimized resources: Track license usage and feature adoption to maximize the value of your Docker subscription.

### Example scenarios

- Usage trends: Identify underutilized licenses or resources, allowing reallocation to more active teams.
- Build efficiency: Track average build times and success rates to pinpoint bottlenecks in development processes.
- Container utilization: Analyze container activity across departments to ensure proper resource distribution and cost efficiency.

For more information, see
[Insights](https://docs.docker.com/admin/organization/insights/).

## Next steps

Now that you've mastered user and access management in Docker, you can:

- Review your
  [activity logs](https://docs.docker.com/admin/organization/activity-logs/) regularly to maintain security awareness
- Check your
  [Insights dashboard](https://docs.docker.com/admin/organization/insights/) to identify opportunities for optimization
- Explore
  [advanced security features](https://docs.docker.com/enterprise/security/) to further enhance your Docker environment
- Share best practices with your team to ensure consistent adoption of security policies

---

# Onboarding and managing roles and permissions in Docker

> Learn how to manage roles, invite members, and implement scalable access control in Docker for secure and efficient collaboration.

# Onboarding and managing roles and permissions in Docker

   Table of contents

---

This page guides you through onboarding owners and members, and using tools like SSO and SCIM to future-proof onboarding going forward.

## Invite owners

When you create a Docker organization, you automatically become its sole owner. While optional, adding additional owners can significantly ease the process of onboarding and managing your organization by distributing administrative responsibilities. It also ensures continuity and prevents blockers if the primary owner is unavailable.

For detailed information on owners, see
[Roles and permissions](https://docs.docker.com/enterprise/security/roles-and-permissions/).

## Invite members and assign roles

Members are granted controlled access to resources and enjoy enhanced organizational benefits. When you invite members to join your Docker organization, you immediately assign them a role.

### Benefits of inviting members

- Enhanced visibility: Gain insights into user activity, making it easier to monitor access and enforce security policies.
- Streamlined collaboration: Help members collaborate effectively by granting access to shared resources and repositories.
- Improved resource management: Organize and track users within your organization, ensuring optimal allocation of resources.
- Access to enhanced features: Members benefit from organization-wide perks, such as increased pull limits and access to premium Docker features.
- Security control: Apply and enforce security settings at an organizational level, reducing risks associated with unmanaged accounts.

For detailed information, see
[Manage organization members](https://docs.docker.com/admin/organization/members/).

## Future-proof user management

A robust, future-proof approach to user management combines automated provisioning, centralized authentication, and dynamic access control. Implementing these practices ensures a scalable, secure, and efficient environment.

### Secure user authentication with single sign-on (SSO)

Integrating Docker with your identity provider streamlines user access and enhances security.

SSO:

- Simplifies sign in, as users sign in with their organizational credentials.
- Reduces password-related vulnerabilities.
- Simplifies onboarding as it works seamlessly with SCIM and group mapping for automated provisioning.

For more information, see the
[SSO documentation](https://docs.docker.com/enterprise/security/single-sign-on/).

### Automate onboarding with SCIM and JIT provisioning

Streamline user provisioning and role management with
[SCIM](https://docs.docker.com/enterprise/security/provisioning/scim/) and
[Just-in-Time (JIT) provisioning](https://docs.docker.com/enterprise/security/provisioning/just-in-time/).

With SCIM you can:

- Sync users and roles automatically with your identity provider.
- Automate adding, updating, or removing users based on directory changes.

With JIT provisioning you can:

- Automatically add users upon first sign in based on [group mapping](#simplify-access-with-group-mapping).
- Reduce overhead by eliminating pre-invite steps.

### Simplify access with group mapping

Group mapping automates permissions management by linking identity provider groups to Docker roles and teams.

It also:

- Reduces manual errors in role assignments.
- Ensures consistent access control policies.
- Help you scale permissions as teams grow or change.

For more information on how it works, see
[Group mapping](https://docs.docker.com/enterprise/security/provisioning/group-mapping/).

---

# Setting up roles and permissions in Docker

> A guide to securely managing access and collaboration in Docker through roles and teams.

# Setting up roles and permissions in Docker

   Table of contents

---

With the right configurations, you can ensure your developers have easy access to necessary resources while preventing unauthorized access. This page guides you through identifying Docker users so you can allocate subscription seats efficiently within your Docker organization, and assigning roles to align with your organization's structure.

## Identify your Docker users and accounts

Before setting up roles and permissions, it's important to have a clear understanding of who in your organization requires Docker access. Focus on gathering a comprehensive view of active users, their roles within projects, and how they interact with Docker resources. This process can be supported by tools like device management software or manual assessments. Encourage all users to update their Docker accounts to use organizational email addresses, ensuring seamless integration with your subscription.

For steps on how you can do this, see
[step 1 of onboarding your organization](https://docs.docker.com/admin/organization/onboard/).

## Assign roles strategically

When you invite members to join your Docker organization, you assign them a role.

Docker's predefined roles offer flexibility for various organizational needs. Assigning roles effectively ensures a balance of accessibility and security.

- Member: Non-administrative role. Members can view other members that are in the same organization.
- Editor: Partial administrative access to the organization. Editors can create, edit, and delete repositories. They can also edit an existing team's access permissions.
- Owner: Full organization administrative access. Owners can manage organization repositories, teams, members, settings, and billing.

For more information, see
[Roles and permissions](https://docs.docker.com/enterprise/security/roles-and-permissions/).

### Enhance with teams

Teams in Docker provide a structured way to manage member access and they provide an additional level of permissions. They simplify permission management and enable consistent application of policies.

- Organize users into teams aligned with projects, departments, or functional roles. This approach helps streamline resource allocation and ensures clarity in access control.
- Assign permissions at the team level rather than individually. For instance, a development team might have "Read & Write" access to certain repositories, while a QA team has "Read-only" access.
- As teams grow or responsibilities shift, you can easily update permissions or add new members, maintaining consistency without reconfiguring individual settings.

For more information, see
[Create and manage a team](https://docs.docker.com/admin/organization/manage-a-team/).

### Example scenarios

- Development teams: Assign the member role to developers, granting access to the repositories needed for coding and testing.
- Team leads: Assign the editor role to team leads for resource management and repository control within their teams.
- Organizational oversight: Restrict the organization owner or company owner roles to a select few trusted individuals responsible for billing and security settings.

### Best practices

- Apply the principle of least privilege. Assign users only the minimum permissions necessary for their roles.
- Conduct regular reviews of role assignments to ensure they align with evolving team structures and organizational responsibilities.

---

# Mastering user and access management

> A guide for managing roles, provisioning users, and optimizing Docker access with tools like SSO and activity logs.

# Mastering user and access management

Table of contents

---

Managing roles and permissions is key to securing your Docker environment while enabling easy collaboration and operational efficiency. This guide walks IT administrators through the essentials of user and access management, offering strategies for assigning roles, provisioning users, and using tools like activity logs and Insights to monitor and optimize Docker usage.

## Who's this for?

- IT teams tasked with configuring and maintaining secure user access
- Security professionals focused on enforcing secure access practices
- Project managers overseeing team collaboration and resource management

## What you'll learn

- How to assess and manage Docker user access and align accounts with organizational needs
- When to use team configurations for scalable access control
- How to automate and streamline user provisioning with SSO, SCIM, and JIT
- How to get the most out of Docker's monitoring tools

## Tools integration

This guide covers integration with:

- Okta
- Entra ID SAML 2.0
- Azure Connect (OIDC)

## Modules

1. [Setting up roles and permissions in Docker](https://docs.docker.com/guides/admin-user-management/setup/)
  A guide to securely managing access and collaboration in Docker through roles and teams.
2. [Onboarding and managing roles and permissions in Docker](https://docs.docker.com/guides/admin-user-management/onboard/)
  Learn how to manage roles, invite members, and implement scalable access control in Docker for secure and efficient collaboration.
3. [Monitoring and insights](https://docs.docker.com/guides/admin-user-management/audit-and-monitor/)
  Track user actions, team workflows, and organizational trends with Activity logs and Insights to enhance security and productivity in Docker.

---

# Build and run agentic AI applications with Docker

# Build and run agentic AI applications with Docker

   Table of contents

---

> Tip
>
> This guide uses the familiar Docker Compose workflow to orchestrate agentic AI
> applications. For a smoother development experience, check out [Docker
> cagent](https://docs.docker.com/ai/cagent/), a purpose-built agent runtime that
> simplifies running and managing AI agents.

## Introduction

Agentic applications are transforming how software gets built. These apps don't
just respond, they decide, plan, and act. They're powered by models,
orchestrated by agents, and integrated with APIs, tools, and services in real
time.

All these new agentic applications, no matter what they do, share a common
architecture. It's a new kind of stack, built from three core components:

- Models: These are your GPTs, CodeLlamas, Mistrals. They're doing the
  reasoning, writing, and planning. They're the engine behind the intelligence.
- Agent: This is where the logic lives. Agents take a goal, break it down, and
  figure out how to get it done. They orchestrate everything. They talk to the
  UI, the tools, the model, and the gateway.
- MCP gateway: This is what links your agents to the outside world, including
  APIs, tools, and services. It provides a standard way for agents to call
  capabilities via the Model Context Protocol (MCP).

Docker makes this AI-powered stack simpler, faster, and more secure by unifying
models, and tool gateways into a developer-friendly workflow that uses Docker
Compose.

![A diagram of the agentic stack](https://docs.docker.com/guides/images/agentic-ai-diagram.webp)  ![A diagram of the agentic stack](https://docs.docker.com/guides/images/agentic-ai-diagram.webp)

This guide walks you through the core components of agentic development and
shows how Docker ties them all together with the following tools:

- [Docker Model Runner](https://docs.docker.com/ai/model-runner/) lets you run LLMs
  locally with simple command and OpenAI-compatible APIs.
- [Docker MCP Catalog and
  Toolkit](https://docs.docker.com/ai/mcp-catalog-and-toolkit/) helps you discover
  and securely run external tools, like APIs and databases, using the Model
  Context Protocol (MCP).
- [Docker MCP Gateway](https://docs.docker.com/ai/mcp-catalog-and-toolkit/mcp-gateway/) lets you orchestrate and manage MCP servers.
- [Docker Compose](https://docs.docker.com/ai/compose/models-and-compose/) is the tool that ties it all
  together, letting you define and run multi-container applications with a
  single file.

For this guide, you'll use the same Compose workflow you're already familiar
with. Then, you'll dig into the Compose file, Dockerfile, and app to see how it
all works together.

## Prerequisites

To follow this guide, you need to:

- [Install Docker Desktop 4.43 or later](https://docs.docker.com/get-started/get-docker/)
- [Enable Docker Model Runner](https://docs.docker.com/ai/model-runner/#enable-dmr-in-docker-desktop)
- At least the following hardware specifications:
  - VRAM: 3.5 GB
  - Storage: 2.31 GB

## Step 1: Clone the sample application

You'll use an existing sample application that demonstrates how to connect a
model to an external tool using Docker's AI features.

```console
$ git clone https://github.com/docker/compose-for-agents.git
$ cd compose-for-agents/adk/
```

## Step 2: Run the application locally

Your machine must meet the necessary hardware requirements to run the
entire application stack locally using Docker Compose. This lets you test the
application end-to-end, including the model and MCP gateway, without needing to
run in the cloud. This particular example uses the [Gemma 3 4B
model](https://hub.docker.com/r/ai/gemma3) with a context size of `10000`.

Hardware requirements:

- VRAM: 3.5 GB
- Storage: 2.31 GB

If your machine exceeds those requirements, consider running the application with a larger
context size or a larger model to improve the agents performance. You can easily
update model and context size in the `compose.yaml` file.

To run the application locally, follow these steps:

1. In the `adk/` directory of the cloned repository, run the following command in a
  terminal to build and run the application:
  ```console
  $ docker compose up
  ```
  The first time you run this command, Docker pulls the
  model from Docker Hub, which may take some time.
2. Visit [http://localhost:8080](http://localhost:8080). Enter a correct or
  incorrect fact in the prompt and hit enter. An agent searches DuckDuckGo to
  verify it and another agent revises the output.
  ![Screenshot of the application](https://docs.docker.com/guides/images/agentic-ai-app.png)  ![Screenshot of the application](https://docs.docker.com/guides/images/agentic-ai-app.png)
3. Press ctrl-c in the terminal to stop the application when you're done.

## Step 3: Review the application environment

You can find the `compose.yaml` file in the `adk/` directory. Open it in a text
editor to see how the services are defined.

compose.yaml

```yaml
services:
  adk:
    build:
      context: .
    ports:
      # expose port for web interface
      - "8080:8080"
    environment:
      # point adk at the MCP gateway
      - MCPGATEWAY_ENDPOINT=http://mcp-gateway:8811/sse
    depends_on:
      - mcp-gateway
    models:
      gemma3 :
        endpoint_var: MODEL_RUNNER_URL
        model_var: MODEL_RUNNER_MODEL

  mcp-gateway:
    # mcp-gateway secures your MCP servers
    image: docker/mcp-gateway:latest
    use_api_socket: true
    command:
      - --transport=sse
      # add any MCP servers you want to use
      - --servers=duckduckgo

models:
  gemma3:
    # pre-pull the model when starting Docker Model Runner
    model: ai/gemma3:4B-Q4_0
    context_size: 10000 # 3.5 GB VRAM
    # increase context size to handle search results
    # context_size: 131000 # 7.6 GB VRAM
```

The app consists of three main components:

- The `adk` service, which is the web application that runs the agentic AI
  application. This service talks to the MCP gateway and model.
- The `mcp-gateway` service, which is the MCP gateway that connects the app
  to external tools and services.
- The `models` block, which defines the model to use with the application.

When you examine the `compose.yaml` file, you'll notice two notable elements for the model:

- A service‑level `models` block in the `adk` service
- A top-level `models` block

These two blocks together let Docker Compose automatically start and connect
your ADK web app to the specified LLM.

> Tip
>
> Looking for more models to use? Check out the [Docker AI Model
> Catalog](https://hub.docker.com/catalogs/models/).

When examining the `compose.yaml` file, you'll notice the gateway service is a
Docker-maintained image,
[docker/mcp-gateway:latest](https://hub.docker.com/r/docker/agents_gateway).
This image is Docker's open source [MCP
Gateway](https://github.com/docker/docker-mcp/) that enables your application to
connect to MCP servers, which expose tools that models can call. In this
example, it uses the [duckduckgoMCP
server](https://hub.docker.com/mcp/server/duckduckgo/overview) to perform web
searches.

> Tip
>
> Looking for more MCP servers to use? Check out the [Docker MCP
> Catalog](https://hub.docker.com/catalogs/mcp/).

With only a few lines of instructions in a Compose file, you're able to run and
connect all the necessary services of an agentic AI application.

In addition to the Compose file, the Dockerfile and the
`entrypoint.sh` script it creates, play a role in wiring up the AI stack at build and
runtime. You can find the `Dockerfile` in the `adk/` directory. Open it in a
text editor.

Dockerfile

```dockerfile
# Use Python 3.11 slim image as base
FROM python:3.13-slim
ENV PYTHONUNBUFFERED=1

RUN pip install uv

WORKDIR /app
# Install system dependencies
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy \
    uv pip install --system .
# Copy application code
COPY agents/ ./agents/
RUN python -m compileall -q .

COPY <<EOF /entrypoint.sh
#!/bin/sh
set -e

if test -f /run/secrets/openai-api-key; then
    export OPENAI_API_KEY=$(cat /run/secrets/openai-api-key)
fi

if test -n "\${OPENAI_API_KEY}"; then
    echo "Using OpenAI with \${OPENAI_MODEL_NAME}"
else
    echo "Using Docker Model Runner with \${MODEL_RUNNER_MODEL}"
    export OPENAI_BASE_URL=\${MODEL_RUNNER_URL}
    export OPENAI_MODEL_NAME=openai/\${MODEL_RUNNER_MODEL}
    export OPENAI_API_KEY=cannot_be_empty
fi
exec adk web --host 0.0.0.0 --port 8080 --log_level DEBUG
EOF
RUN chmod +x /entrypoint.sh

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

ENTRYPOINT [ "/entrypoint.sh" ]
```

The `entrypoint.sh` has five key environment variables:

- `MODEL_RUNNER_URL`: Injected by Compose (via the service-level `models:`
  block) to point at your Docker Model Runner HTTP endpoint.
- `MODEL_RUNNER_MODEL`: Injected by Compose to select which model to launch in
  Model Runner.
- `OPENAI_API_KEY`: If you define an `openai-api-key` secret in your Compose
  file, Compose will mount it at `/run/secrets/openai-api-key`. The entrypoint
  script reads that file and exports it as `OPENAI_API_KEY`, causing the app to
  use hosted OpenAI instead of Model Runner.
- `OPENAI_BASE_URL`: When no real key is present, this is set to
  `MODEL_RUNNER_URL` so the ADK's OpenAI-compatible client sends requests to
  Docker Model Runner.
- `OPENAI_MODEL_NAME`: When falling back to Model Runner, the model is prefixed
  with `openai/` so the client picks up the right model alias.

Together, these variables let the same ADK web server code seamlessly target either:

- Hosted OpenAI: if you supply `OPENAI_API_KEY` (and optionally `OPENAI_MODEL_NAME`)
- Model Runner: by remapping `MODEL_RUNNER_URL` and `MODEL_RUNNER_MODEL` into the OpenAI client’s expected variables

## Step 4: Review the application

The `adk` web application is an agent implementation that connects to the MCP
gateway and a model through environment variables and API calls. It uses the
[ADK (Agent Development Kit)](https://github.com/google/adk-python) to define a
root agent named Auditor, which coordinates two sub-agents, Critic and Reviser,
to verify and refine model-generated answers.

The three agents are:

- Critic: Verifies factual claims using the toolset, such as DuckDuckGo.
- Reviser: Edits answers based on the verification verdicts provided by the Critic.
- Auditor: A higher-level agent that sequences the
  Critic and Reviser. It acts as the entry point, evaluating LLM-generated
  answers, verifying them, and refining the final output.

All of the application's behavior is defined in Python under the `agents/`
directory. Here's a breakdown of the notable files:

- `agents/agent.py`: Defines the Auditor, a SequentialAgent that chains together
  the Critic and Reviser agents. This agent is the main entry point of the
  application and is responsible for auditing LLM-generated content using
  real-world verification tools.
- `agents/sub_agents/critic/agent.py`: Defines the Critic agent. It loads the
  language model (via Docker Model Runner), sets the agent’s name and behavior,
  and connects to MCP tools (like DuckDuckGo).
- `agents/sub_agents/critic/prompt.py`: Contains the Critic prompt, which
  instructs the agent to extract and verify claims using external tools.
- `agents/sub_agents/critic/tools.py`: Defines the MCP toolset configuration,
  including parsing `mcp/` strings, creating tool connections, and handling MCP
  gateway communication.
- `agents/sub_agents/reviser/agent.py`: Defines the Reviser agent, which takes
  the Critic’s findings and minimally rewrites the original answer. It also
  includes callbacks to clean up the LLM output and ensure it's in the right
  format.
- `agents/sub_agents/reviser/prompt.py`: Contains the Reviser prompt, which
  instructs the agent to revise the answer text based on the verified claim
  verdicts.

The MCP gateway is configured via the `MCPGATEWAY_ENDPOINT` environment
variable. In this case, `http://mcp-gateway:8811/sse`. This allows the app to
use Server-Sent Events (SSE) to communicate with the MCP gateway container,
which itself brokers access to external tool services like DuckDuckGo.

## Summary

Agent-based AI applications are emerging as a powerful new software
architecture. In this guide, you explored a modular, chain-of-thought system
where an Auditor agent coordinates the work of a Critic and a Reviser to
fact-check and refine model-generated answers. This architecture shows how to
combine local model inference with external tool integrations in a structured,
modular way.

You also saw how Docker simplifies this process by providing a suite of tools
that support agentic AI development:

- [Docker Model Runner](https://docs.docker.com/ai/model-runner/): Run and serve
  open-source models locally via OpenAI-compatible APIs.
- [Docker MCP Catalog and
  Toolkit](https://docs.docker.com/ai/mcp-catalog-and-toolkit/): Launch and manage
  tool integrations that follow the Model Context Protocol (MCP) standard.
- [Docker MCP Gateway](https://docs.docker.com/ai/mcp-catalog-and-toolkit/mcp-gateway/): Orchestrate and manage
  MCP servers to connect agents to external tools and services.
- [Docker Compose](https://docs.docker.com/ai/compose/models-and-compose/): Define and run
  multi-container agentic AI applications with a single file, using the same
  workflow.

With these tools, you can develop and test agentic AI applications efficiently,
using the same consistent workflow throughout.
