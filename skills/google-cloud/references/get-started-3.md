# Consider geographic distributionStay organized with collectionsSave and categorize content based on your preferences. and more

# Consider geographic distributionStay organized with collectionsSave and categorize content based on your preferences.

# Consider geographic distributionStay organized with collectionsSave and categorize content based on your preferences.

Before you create resources, consider how you plan to distribute resources
geographically to meet your company's unique requirements. Administrators and
architects in your organization usually make decisions about geography, and make
their decisions available to people who deploy resources. For example, your
company might have an [Infrastructure as Code (IaC)](https://cloud.google.com/docs/terraform/iac-overview)
process that automatically assigns geographies as you deploy resources.

This document provides an overview on how geography impacts your workloads.

## Distribute resources to help ensure availability

You can geographically distribute resources to meet your unique requirements, as
in the following examples:

- Latency: Ensure you have resources in zones near your users.
- Availability: Create redundant resources in multiple regions in case of a
  region failure.

## Regions and zones

When you create resources, you might select the following geographic categories:

- *Regions* are independent geographic areas that contain zones. For example,
  `asia-east1` (Taiwan).
- *Zones* are areas that are isolated from each other within a region. For
  example, zone `a` in the `asia-east1` (Taiwan) region is named `asia-east1-a`.

Consider a zone as a single failure domain within a region. To deploy
fault-tolerant applications with high availability and help protect against
unexpected failures, you might deploy your applications across multiple zones in
a region. For more information, see
[Geography and regions](https://cloud.google.com/docs/geography-and-regions).

Each resource has its own location dynamics. For example, see the following
details about Compute Engine and Cloud Storage:

- [Compute Engine regions and zones](https://cloud.google.com/compute/docs/regions-zones)
- [Cloud Storage bucket locations](https://cloud.google.com/storage/docs/bucket-locations)

### Select geographies based on resource interactions

As you create your resource distribution plan, consider resource communication
across zones and regions. Resource interaction capabilities are determined by
the following resource types:

- *Global resources* can be accessed by any other resource, across regions and
  zones. Examples include disk images, disk snapshots, and networks.
- *Regional resources* are redundantly deployed across multiple
  zones within a region. Regional resources can be accessed only by resources that
  are located in the same region. Examples include App Engine
  applications and [regional managed instance groups](https://cloud.google.com/compute/docs/instance-groups#types_of_managed_instance_groups).
- *Multiregional* services are redundantly distributed within and across
  regions. These services optimize availability, performance, and resource
  efficiency. For a list of services that have one or more multiregional
  locations, see [Products available by location](https://cloud.google.com/about/locations#multi-region).
- *Zonal resources* can be accessed only by resources that are located in the
  same zone. An example of a zonal resource is a Compute Engine virtual
  machine (VM) instance.

For example, consider the following resources:

- Globally: a network that can be accessed by all resources.
- In each region: IP addresses that provide external access to resources only
  within a single region.
- In each zone: disks that can connect to VMs that are in the same zone.

![A global network can contain region-specific resources such as IP addresses and zone-specific resources such as VMs and disks](https://cloud.google.com/static/docs/images/overview/regions-zones.svg)

     [PreviousResource planning overview](https://cloud.google.com/docs/get-started/resource-planning-overview)   [NextCreate an ownership hierarchy](https://cloud.google.com/docs/get-started/create-ownership-hierarchy)

---

# Consider resource maintenanceStay organized with collectionsSave and categorize content based on your preferences.

# Consider resource maintenanceStay organized with collectionsSave and categorize content based on your preferences.

Before you create resources, you must consider maintenance requirements for each
resource that you deploy. Additionally, you must consider maintenance on any
underlying resources.

For example, some services deploy to underlying Compute Engine VMs. The
maintenance policy that you set for your deployed service is distinct from the
maintenance policy on the underlying VMs.

The following example maintenance dynamics are provided to help you understand
the planning required to keep your resources available and running efficiently.

## Set virtual machine (VM) maintenance policies

When you create VMs you set a maintenance policy that dictates VM behavior when
there is an update pending, a VM crashes, or other host events occur. For
example, you can create a policy to live migrate workloads to another VM, or
shut down and restart the impacted VM.

For more information, see the following:

- [About host events](https://cloud.google.com/compute/docs/instances/host-maintenance-overview)
- [Monitor and plan for a host maintenance event](https://cloud.google.com/compute/docs/instances/monitor-plan-host-maintenance-event)

### Distinguish between VM maintenance and service maintenance

The maintenance policy that you set for VMs is distinct from maintenance
policies that you set for services that run on your VMs.

For example, GKE deploys clusters on Compute Engine VMs. You
can set maintenance policies to control when some GKE cluster
maintenance happens, but those policies don't prevent automatic maintenance
triggered on the underlying Compute Engine VMs.

To learn more about maintenance policies for services running on
Compute Engine VMs, review the respective documentation for those services.

### Maintain workloads on VMs with GPUs or TPUs

Some Compute Engine resources you create might have GPUs or TPUs attached. For
example, you might create VMs that use GPUs or TPUs to handle AI workloads. If a
host event occurs on these VMs, live migration from the impacted VM to a new VM
is not supported. As a result, host maintenance events result in VM downtime and
potential disruption to your workloads. To handle maintenance events on
resources with GPUs or TPUs, see the following:

- [Handle GPU host maintenance events](https://cloud.google.com/compute/docs/gpus/gpu-host-maintenance)
- [Introduction to Cloud TPU](https://cloud.google.com/tpu/docs/intro-to-tpu)

## Retain connections during network infrastructure maintenance

Network Connectivity products help you connect your peer networks to your
Virtual Private Cloud networks. Google Cloud performs regular maintenance on this
infrastructure. To help prevent downtime during maintenance events, we recommend
that you follow the maintenance recommendations for each networking product, as
in the following examples:

- Cloud Router maintenance does not interrupt routing, but might require you
  to configure settings on your peer network router. For more information, see [Software maintenance and automated task restarts](https://cloud.google.com/network-connectivity/docs/router/concepts/overview#maintenance).
- Cloud Interconnect experiences regular automated maintenance, which might
  require you to set up notifications and create redundant connections. For more
  information, see [Infrastructure maintenance events](https://cloud.google.com/network-connectivity/doocs/interconnect/support/infrastructure-maintenance-events).

     [PreviousCreate an ownership hierarchy](https://cloud.google.com/docs/get-started/create-ownership-hierarchy)   Was this helpful?

---

# Change the appearance of the Google Cloud consoleStay organized with collectionsSave and categorize content based on your preferences.

> Describes how to change the appearance of the Google Cloud console, supporting light mode and dark mode.

# Change the appearance of the Google Cloud consoleStay organized with collectionsSave and categorize content based on your preferences.

You can change the appearance of the Google Cloud console by selecting a color
theme, supporting light mode and dark mode. The console
can also match your operating system's color scheme preference.

## Select a color theme

If you have never manually selected a color theme for the Google Cloud console,
the console automatically matches your operating system's
color scheme preference.

To change the color theme for the console, follow these steps:

1. Open the [Google Cloud console](https://console.cloud.google.com/).
2. On the console toolbar, click
   **Settings and utilities**.
3. In the menu, click **Appearance**.
4. In the dialog that appears, select a color theme from the options:
  **Light**, **Dark**, or **Same as device**.

The page does not reload when you select a color theme, so your context and work
in the console are preserved.

   Was this helpful?

---

# Create an ownership hierarchyStay organized with collectionsSave and categorize content based on your preferences.

# Create an ownership hierarchyStay organized with collectionsSave and categorize content based on your preferences.

As you develop your applications and workloads on Google Cloud, you
create the following resource types:

- *Container resources* help you organize and control access. These resources
  include organizations, folders, and projects.
- *Service resources* are fundamental components that make up
  Google Cloud products and services. These resources include
  Compute Engine virtual machines (VMs) and Google Kubernetes Engine clusters.

You use container resources to organize service resources in a hierarchy. This
structure helps you establish ownership and control access.

## Organize and manage hierarchically

To isolate resources from each other and limit access to users, you can group
and manage resources as a single unit. You do this using the following
structure, known as the resource hierarchy:

- *Organization*: Represents your company, and serves as the root of your
  resource hierarchy.
- *Folders*: An optional grouping mechanism you can use to isolate groups of
  projects. For example, you might create folders for legal entities,
  departments, or teams.
- *Projects*: The base-level organizing entity that contains your service
  resources.

For a detailed overview of the resource hierarchy, see [Resource hierarchy](https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy).

To learn how to use the resource hierarchy to manage access, see [Using resource hierarchy for access control](https://cloud.google.com/iam/docs/resource-hierarchy-access-control).

### Organization: Create the root of your hierarchy

An organization is the root node of the hierarchy, under which you create all
other resources. The access policies you apply to your organization are applied
to all other resources. This means that you can apply an access control at
the organization level instead of duplicating and managing the same control
across all projects.

When you create an organization resource, underlying projects belong to the
organization, instead of the users who create projects. This means that
projects and their underlying resources can continue to exist, even if a user
is removed.

### Folders: Isolate groups of projects

You can use folders to create isolation boundaries between projects. For
example, you might have distinct project collections for department or team.
Folders can contain projects and subfolders. You can apply access controls to
ensure that users in one team cannot access resources in folders assigned to
another team.

### Projects: Isolate resources

Google Cloud resources must belong to a project, which is an organizing
entity that helps you isolate and control access to resources. For example, you
might create distinct projects for development and production environments.

A project contains settings, permissions, and other metadata that describe your
applications. Resources within a single project can work together by
communicating through an internal network, subject to regions-and-zones
rules. A project can't access another project's resources unless you use
[Shared VPC](https://cloud.google.com/vpc/docs/shared-vpc) or [VPC Network Peering](https://cloud.google.com/vpc/docs/vpc-peering).

#### Name and reference your projects

You use identifiers to reference your projects in commands and API calls. Each
Google Cloud project has the following identifiers:

- **Project name**: A name that you provide.
- **Project ID**: An identifier that you can provide or Google Cloud can
  provide for you. Each project ID is unique across Google Cloud. After
  you delete a project, its ID can never be used again.
- **Project number**: Provided by Google Cloud.

For more information, see [Creating and managing projects](https://cloud.google.com/resource-manager/docs/creating-managing-projects).

     [PreviousConsider geographic distribution](https://cloud.google.com/docs/get-started/consider-geographic-distribution)   [NextConsider maintenance](https://cloud.google.com/docs/get-started/consider-resource-maintenance)   Was this helpful?

---

# Use developer toolsStay organized with collectionsSave and categorize content based on your preferences.

# Use developer toolsStay organized with collectionsSave and categorize content based on your preferences.

Google Cloud provides several ways for developers to improve the efficiency of
their development workflow, including the following tools:

- [Cloud Workstations: Develop in standardized environments](#workstations)
- [Google Cloud CLI: Write scripts and automate](#cli)
- [Cloud Code: Develop directly in your IDE](#ide-extensions)

## Before you begin

To make sure you can set up APIs and use tools, ask your administrators to
complete the following tasks:

- Create an account that you use to sign in and use Google Cloud
  products, including Google Cloud console and Google Cloud CLI.
- Create a project that serves as an access boundary for your
  Google Cloud resources.
- Enable billing on your project so you can pay for service and API usage.

For detailed instructions to complete setup steps, see [Google Cloud Setup
guided flow](https://cloud.google.com/docs/enterprise/cloud-setup).

## Cloud Workstations: Develop in standardized environments

As a developer, you require software and specific configurations to perform your
tasks. The administrators at your company can help you with your workflows by
creating and distributing a development environment template that is suited to
your specific project.

Developers can use Cloud Workstations to obtain the following benefits:

- A standardized environment that is consistent for each developer on a team.
- Preconfigured settings established by administrators.
- Options to access the web-based environment from a browser, SSH, or IDE.

For more details, see [Cloud Workstations overview](https://cloud.google.com/workstations/docs/overview).

## Google Cloud CLI: Write scripts and automate

The [Google Cloud CLI](https://cloud.google.com/sdk/gcloud) tools help you create and manage Google Cloud
resources from the command line, or through scripts and other automation. For
example, you might create an automated script to push files to VMs.

Use the gcloud CLI to do the following:

- Manage your local configuration.
- Establish authentication.
- Access Google Cloud services through the command line.

For installation steps, see [Install the Google Cloud CLI](https://cloud.google.com/sdk/docs/install-sdk).

## Cloud Code: Develop directly in your IDE

[Cloud Code](https://cloud.google.com/code/docs) includes tools that help you use
Cloud Client Libraries and develop cloud applications. Use Cloud Code to
do the following directly in VS Code or
[supported JetBrains IDEs](https://cloud.google.com/code/docs/intellij/ides):

- Integrate Google Cloud APIs to work with Google Cloud services.
- Access documentation.
- Debug your application.
- Use [Gemini Code Assist](#code-assist).

Cloud Code is automatically installed on Cloud Workstations and
Cloud Shell. To install the extension for your IDE, see the following:

- [Install the Cloud Code for VS Code extension](https://cloud.google.com/code/docs/vscode/install)
- [Install the Cloud Code for IntelliJ plugin](https://cloud.google.com/code/docs/intellij/install)

### Gemini Code Assist: Develop and deploy with AI assistance

When you install the Cloud Code extension, the
Gemini Code Assist extension is also installed by default.
Gemini Code Assist provides AI assistance with your code, including the
following:

- Generate and debug code.
- Generate unit tests.
- Chat to answer questions about code and other technical topics.

For more information, see the
[Gemini Code Assist overview](https://cloud.google.com/gemini/docs/codeassist/overview).

## What's next?

To explore more developer tools, see [Google Cloud SDK, languages, frameworks, and
tools overview](https://cloud.google.com/docs/devtools).

To get familiar with development workflows, experiment with the following
guides:

- For sample solutions, see the following:
  - [Jump Start Solution guides](https://cloud.google.com/architecture/all-jss-guides).
  - [Google Cloud web hosting](https://cloud.google.com/solutions/web-hosting).
- To learn about deployment options, see the following:
  - [Continuous deployment from Git using
    Cloud Build](https://cloud.google.com/run/docs/continuous-deployment-with-cloud-build).
  - [CI/CD pipeline for developing and delivering containerized
    apps](https://cloud.google.com/architecture/app-development-and-delivery-with-cloud-code-gcb-cd-and-gke).
  - [Quickstart: Deploy a Node.js service toCloud Run](https://cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-nodejs-service).

   Was this helpful?

---

# Getting supportStay organized with collectionsSave and categorize content based on your preferences.

# Getting supportStay organized with collectionsSave and categorize content based on your preferences.

Cloud Customer Care provides support packages that let you access general how-to
advice, best practice help, troubleshooting, and operational knowledge.

The Basic Support package is provided to all Google Cloud customers and includes
free billing and payments support. Other support packages require that you
purchase them, and offer unlimited 1:1 technical support for outages and defects,
unexpected product behavior, product usage questions, billing issues, and
feature requests.

## Confirm your support service

You can confirm the existing level of Customer Care support you have for Google Cloud.

1. In the Google Cloud console, go to the **Support** > **Overview** page.
  [Go to Overview](https://console.cloud.google.com/support/overview)
2. Using the resource selector on the console toolbar, select the organization or project for
    which you'd like to confirm your support level.
3. Your support service is indicated in the **Support information** section. For example:
  `Your current Customer Care service: Premium`

## Choose your support service

You can [compare Customer Care support packages](https://cloud.google.com/support#compare-features)
and choose the service that's right for your organization:

- **Basic Support** is included for all Google Cloud customers and provides access to
      documentation, community support, Cloud Billing support, and Active Assist
      recommendations. You can also request support for technical questions about projects within your
      organization.
- **Standard Support** is recommended for small to medium organizations with workloads under
      development looking to begin their support journey. With Standard Support, you have access to
      the Cloud Support API, Active Assist recommendations, and receive 4-hour response times for
      Priority 2 (P2) cases.
- **Enhanced Support** offers faster response times and additional services designed for
      medium to large companies running their cloud workloads in production. With Enhanced Support,
      you have access to intelligent services, such as the Cloud Support API, Third-Party Technology Support,
      and Recommender.
- **Premium Support** is designed for enterprises that run priority workloads and require
      fast response times, platform stability, and increased operational efficiencies. You also have
      Customer Aware Support and are assigned a Technical Account Manager.

Optionally, you can increase your capabilities with Value-Add Services that are
available as an additional purchase for Enhanced Support and Premium Support
customers. For example, you can purchase elevated levels of technical support or
increased oversight and assistance from experts who are invested in your
organization's success.

For more information, see
[Get support with Cloud Customer Care](https://cloud.google.com/support/docs/overview).

## Onboard to Customer Care

After purchasing a Customer Care support package, make sure that you
understand your package, and any additional Value-Add Services, so that you can
fully benefit from the included features.

You should also complete certain procedures including setting up the
Google Cloud project environment, configuring access control, and optionally using
services that automate and optimize your performance across Google Cloud.

For more information, see
[Onboard to Cloud Customer Care](https://cloud.google.com/support/docs/checklists/onboard-customer-care).

## Contact Customer Care and get help

All users can contact Customer Care with questions about Cloud Billing. You can
  also request support for technical questions about projects within your organization.

1. In the Google Cloud console, go to the **Support** > **Overview** page.
  [Go to Overview](https://console.cloud.google.com/support/overview)
2. Using the resource selector on the console toolbar, select the project for which you'd like
    support.
3. In the navigation menu, select your preferred communication channel:
  - **Billing support**: gives you access to a live chat for billing support
  - **Phone support**: provides a phone number that you can call to receive assistance in
          supported languages
  - **Community support**: provides links to community discussion groups and mailing lists
          that can help you find answers or troubleshoot problems

Other inquiries require purchasing a support package and creating a support
case. A support case is a request for technical assistance or help with a
Google Cloud account, project, or billing issue.

To have the most beneficial support experience and to effectively engage with
Customer Care teams, you should follow certain best practices when
creating and managing support cases in the Google Cloud console. Writing a
detailed and specific support case, and setting the correct priority, makes it
easier for the Customer Care team to respond to you quickly and
efficiently.

For more information, see
[Create and manage support cases](https://cloud.google.com/support/docs/customer-care-procedures) and
[Best practices for working with Customer Care](https://cloud.google.com/support/docs/best-practices).

---

# Ways to interact with Google CloudStay organized with collectionsSave and categorize content based on your preferences.

> Ways you can interact with Google Cloud.

# Ways to interact with Google CloudStay organized with collectionsSave and categorize content based on your preferences.

You can use several methods to interact with Google Cloud and your
resources. The methods you choose can depend on your preferences, your company
workflows, and your goals.

The following are example interaction methods:

- [Google Cloud console](#console): Use a web-based graphical user interface.
- [Google Cloud CLI](#commands-and-scripts): Write commands and scripts.
- [Cloud Client Libraries](#libraries): Create your own application.
- [Infrastructure as Code (IaC)](#infrastructure-as-code): Standardize resource
  deployment.

## Use the browser-based Google Cloud console

If you prefer to manage your Google Cloud projects and resources through a
graphical user interface, use the browser-based Google Cloud console.

Use the Google Cloud console to perform a variety of management and
administrative tasks, including the following:

- Manage resources.
- Store, query, and process data.
- Connect to virtual machines (VMs).
- Analyze activity.
- Diagnose production issues.
- Deploy easy-to-launch solutions.

For more information, see [Google Cloud console](https://cloud.google.com/cloud-console).

To ensure proper console functionality, see also
[Allow access to Google Cloud console domains](https://cloud.google.com/docs/get-started/required-domains).

## Write commands and create scripts

If you prefer to manage development and workflows on the command line or through
automated scripts, use [the Google Cloud CLI](https://cloud.google.com/sdk/gcloud). Use the
Google Cloud CLI to perform tasks efficiently and at scale. For example, you
might do the following:

- Create a script to push a file to all VMs.
- Simulate backend data with a data emulator to help you efficiently write
  client-side code.
- Deploy serverless code.

Run `gcloud` commands using the following methods:

- Install the [Google Cloud CLI](https://cloud.google.com/sdk/docs), which lets you run commands in
  a terminal window on your local computer.
- Use the browser-based [Cloud Shell](https://cloud.google.com/shell/docs/features), which doesn't
  require local installation. Open Cloud Shell from the
  [Google Cloud console](https://console.cloud.google.com/?cloudshell=true) to use the following
  features:
  - A temporary Compute Engine VM instance.
  - A [built-in code editor](https://cloud.google.com/shell/docs/editor-overview).
  - Persistent disk storage.
  - Pre-installed gcloud CLI, Terraform, and other tools.
  - Language support for Java, Go, Python, Node.js, PHP, Ruby and .NET.
  - Web preview.
  - Built-in authorization for access to Google Cloud console projects and
    resources.

For more information about Cloud Shell, see
[How Cloud Shell works](https://cloud.google.com/shell/docs/how-cloud-shell-works).

For a list of `gcloud` commands, as well as flags and examples, see the
[gcloudreference](https://cloud.google.com/sdk/gcloud/reference).

## Develop your own application using Cloud Client Libraries

If you want to create your own applications to manage resources, use
[Cloud Client Libraries](https://cloud.google.com/sdk/cloud-client-libraries) to access Google Cloud APIs.

Cloud Client Libraries provide the following benefits to help you build your
application:

- Use conventions that are specific to your preferred language.
- Use a consistent style across services.
- Handle authentication.

For an overview, see [Cloud Client Libraries explained](https://cloud.google.com/apis/docs/client-libraries-explained).

## Scale resource provisioning and management with Infrastructure as Code (IaC)

Infrastructure as Code (IaC) is the process of provisioning and managing
infrastructure using *code* instead of graphical user interfaces or command-line
scripts.

Your company's administrators and architects might use IaC to obtain the
following benefits:

- Incorporate your change management process.
- Test and audit as you make changes.
- Store configurations in source control.
- Standardize your infrastructure.

Google Cloud is integrated with several IaC tools. For example, you might use [Terraform](https://cloud.google.com/docs/terraform/terraform-overview) to provision and manage your infrastructure
through human-readable configuration files that you can version, reuse, and
share.

For an overview of IaC and a list of tools you can use with Google Cloud, see [Infrastructure as Code on Google Cloud](https://cloud.google.com/docs/terraform/iac-overview).

   Was this helpful?

---

# Allow access to Google Cloud console domainsStay organized with collectionsSave and categorize content based on your preferences.

> Domains required for Google Cloud console functionality.

# Allow access to Google Cloud console domainsStay organized with collectionsSave and categorize content based on your preferences.

If you or your company uses a local networking configuration that denies access
to particular URLs, such as a firewall or proxy server, you might encounter
errors when accessing or using the Google Cloud console. This document lists the
domains and domain patterns that must be allowed for
the Google Cloud console to function properly.

## Required domains

The following domains and domain patterns are required for
Google Cloud console functionality. If any of these domains are blocked,
the console will not function as expected.

Make sure your networking configuration allows access to the following domains:

| Domain or domain pattern | Purpose |
| --- | --- |
| console.cloud.google.com | The Google Cloud console |
| www.gstatic.com | Static content such as scripts, style sheets, and images |
| ssl.gstatic.com | Images |
| fonts.gstatic.com | Fonts |
| *.clients6.google.com | Google APIs |
| *.googleapis.com | Google APIs |
| apis.google.com | Google API Client Libraries |
| reauth.cloud.google.com | Multi-factor authentication (MFA) conformance |
| csp.withgoogle.com | Content Security Policy (CSP) violation reporting |

## Monitoring domains

The following domains and URLs are used for health monitoring of
the Google Cloud console. If any of these are blocked,
the console might continue to function but Google will not be
aware of any errors or behavior issues you encounter while using
the console.

| Domain or URL |
| --- |
| cloud.google.com/log |
| www.google-analytics.com |
| www.googletagmanager.com |

   Was this helpful?

---

# Resource planning overviewStay organized with collectionsSave and categorize content based on your preferences.

# Resource planning overviewStay organized with collectionsSave and categorize content based on your preferences.

Before you create Google Cloud resources, consider geographic location,
organizing structure, and maintenance options. When you consider these options
early, you help ensure that your choices properly align with your business needs.

To create plans for your resources, see the following:

- [Consider geographic distribution](https://cloud.google.com/docs/get-started/consider-geographic-distribution):
  Google Cloud infrastructure services are located across the world, and are
  divided into regions and zones. The locations you choose affect the latency,
  availability, and durability of your resources.
- [Create an ownership hierarchy](https://cloud.google.com/docs/get-started/create-ownership-hierarchy): The
  resource hierarchy helps you organize resources into folders and projects. The
  structure you create helps you control access and separate work streams.
- [Consider resource maintenance](https://cloud.google.com/docs/get-started/consider-resource-maintenance):
  Some resources have maintenance policies that can help you plan for outages
  and required updates. Consider maintenance behaviors early to keep your
  applications running smoothly.

     [NextConsider geographic distribution](https://cloud.google.com/docs/get-started/consider-geographic-distribution)   Was this helpful?

---

# About the Well

> The Google Cloud Architecture Framework contains principles for secure, reliable, and cost-optimized cloud environments.

# About the Well-Architected FrameworkStay organized with collectionsSave and categorize content based on your preferences.

The [Google Cloud Well-Architected Framework](https://cloud.google.com/architecture/framework) provides a comprehensive set of recommendations to
help architects, developers, administrators, and other cloud practitioners
design and manage cloud environments that are secure, efficient, reliable,
high-performing, and cost-effective.

Google experts continuously update the framework's recommendations to
incorporate the latest cloud capabilities and industry best practices.
Recommendations in the framework are applicable to various deployment scenarios
including cloud-first workloads, on-premises workloads that are migrated to the
cloud, hybrid deployments, and multi-cloud environments.

## Well-Architected Framework pillars and perspectives

The recommendations in the Well-Architected Framework are organized under the
following pillars:

- **Operational excellence:** Efficiently deploy, operate, monitor, and manage
  your cloud workloads.
- **Security:** Maximize the security of your data and workloads in the cloud,
  design for privacy, and align with regulatory requirements and standards.
- **Reliability:** Design and operate resilient and highly available workloads
  in the cloud.
- **Cost optimization:** Maximize the business value of your investment in
  Google Cloud.
- **Performance optimization:** Design and tune your cloud resources for
  optimal performance.

The framework also provides cross-pillar perspectives: for specific domains like
AI and ML, and for industries like financial services.

For more information, see [Google Cloud Well-Architected Framework](https://cloud.google.com/architecture/framework) in the Architecture Center.

![Pillars of the Well-Architected Framework.](https://cloud.google.com/static/architecture/framework/images/af-infographic.svg)

   Was this helpful?
