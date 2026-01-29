# Generative AI and more

# Generative AI

> Documentation and resources for building and implementing generative AI applications with Google Cloud tools and productss.

[Get started for free](https://console.cloud.google.com/freetrial)

#### Start your proof of concept with $300 in free credit

- Develop with our latest Generative AI models and tools.
- Get free usage of 20+ popular products, including Compute Engine and AI APIs.
- No automatic charges, no commitment.

       [View free product offers](https://cloud.google.com/free/docs/free-cloud-features#free-tier)

#### Keep exploring with 20+ always-free products.

Access 20+ free products for common use cases, including AI APIs, VMs, data warehouses,
          and more.

                        Access Google's large generative AI models so you can test, tune, and deploy them for use in your AI-powered applications.

                        See what it's like to send requests to the Gemini API through Google Cloud's AI-ML platform, Vertex AI.

                        Leverage the power of GKE as a customizable AI/ML platform featuring high performance, cost effective serving and training with industry-leading scale and flexible infrastructure options.

                        Identify whether generative AI, traditional AI, or a combination of both might suit your business use case.

                        Learn how to address the challenges in each stage of developing a generative AI application.

                        View code samples for popular use cases and deploy examples of generative AI applications that are secure, efficient, resilient, high-performing, and cost-effective.

                        Learn about specific terms that are associated with generative AI.

                        Discover test, customize, and deploy Google models and assets from an ML model library.

                        Discover, test, customize, and deploy select OSS models and assets from an ML model library.

                        Learn how to deploy HuggingFace text generation models to Vertex AI or Google Kubernetes Engine (GKE).

                        Attach GPUs to VM instances to accelerate generative AI workloads on Compute Engine.

                        Design, test, and customize your prompts sent to Google's Gemini and PaLM 2 large language models (LLM).

                        Learn the prompt-engineering workflow and common strategies that you can use to affect model responses.

                        View example prompts and responses for specific use cases.

                        You can ground Vertex AI models with Google Search or with your own data stored in Vertex AI Search.

                        Use Grounding with Google Search to connect the model to the up-to-date knowledge available on the internet.

                        Use AlloyDB to generate and store vector embeddings, then index and query the embeddings using the pgvector extension.

                        Store vector embeddings in Postgres SQL, then index and query the embeddings using the pgvector extension.

                        Use LangChain to extract data from BigQuery and enrich and ground your model's responses.

                        Create vector embeddings from your Firestore data, then index and query the embeddings.

                        Use LangChain to extract data from Memorystore and enrich and ground your model's responses.

                        Leverage Google's foundation models, search expertise, and conversational AI technologies for enterprise-grade generative AI applications.

                        Add function calling to your model to enable actions like booking a reservation based on extracted calendar information.

                        Evaluate the performance of foundation models and your tuned generative AI models on Vertex AI.

                        General purpose foundation models can benefit from tuning to improve their performance on specific tasks.

                        TPUs are Google's custom-developed ASICs used to accelerate machine learning workloads, such as training an LLM.
                                        Intermediate
                        Reference architecture for a RAG-capable generative AI application using Vertex AI and Vector Search.
                               Intermediate
                        Reference architecture for a RAG-capable generative AI application using Vertex AI and AlloyDB for PostgreSQL.
                               Intermediate
                        Reference architecture for a RAG-capable generative AI application using GKE, Cloud SQL, and open source tools like Ray, Hugging Face, and LangChain.

- [C# and .NET](https://cloud.google.com/dotnet/docs/setup)
- [C++](https://cloud.google.com/cpp/docs/setup)
- [Go](https://cloud.google.com/go/docs/setup)
- [Java](https://cloud.google.com/java/docs/setup)
- [JavaScript and Node.js](https://cloud.google.com/nodejs/docs/setup)
- [Python](https://cloud.google.com/python/docs/setup)
- [Ruby](https://cloud.google.com/ruby/docs/setup)

                      LangChain is an open source framework for generative AI apps that allows you to build context into your prompts, and take action based on the model's response.

- [Python (LangChain)](https://python.langchain.com/docs/integrations/llms/google_vertex_ai_palm)
- [JavaScript (LangChain.js)](https://js.langchain.com/docs/integrations/platforms/google)
- [Java (LangChain4j)](https://docs.langchain4j.dev/integrations/language-models/google-palm/)
- [Go (LangChainGo)](https://tmc.github.io/langchaingo/docs/)

                      View [code samples for popular use cases and deploy examples of generative AI applications](https://cloud.google.com/docs/generative-ai/code-samples) that are secure, efficient, resilient, high-performing, and cost-effective.

---

# Geography and regionsStay organized with collectionsSave and categorize content based on your preferences.

# Geography and regionsStay organized with collectionsSave and categorize content based on your preferences.

Google Cloud products are served from [specific regional failure domains](https://cloud.google.com/about/locations)
and are fully supported by [Service Level Agreements](https://cloud.google.com/terms/sla) to ensure you
are designing your application architecture within the structure of Google Cloud.

Google Cloud infrastructure services are available in locations across
North America, South America, Europe, Asia, the Middle East, and Australia.
These locations are divided into regions and zones. You can choose where
to locate your applications to meet your latency, availability, and durability
requirements.

If you're new to Google Cloud, create an account to evaluate how our
      products perform in real-world scenarios. New customers also get $300 in
      free credits to run, test, and deploy workloads.

 [Get started for free](https://console.cloud.google.com/freetrial)

## Regions and zones

 *Regions* are independent geographic areas that consist of *zones*. Zones and regions are
logical abstractions of underlying physical resources. A region consists of three or more zones
housed in three or more physical data centers. The regions Stockholm, Mexico, Osaka, and Montreal
have three zones housed in one or two physical data centers. These regions are in the process of
expanding to at least three physical data centers. When you architect your solutions in
Google Cloud, consider the guidance in
[Cloud locations](https://cloud.google.com/about/locations),
[Google Cloud Platform SLAs](https://cloud.google.com/terms/sla),
and the appropriate
[Google Cloud product documentation](https://cloud.google.com/docs).

These data centers might be owned by Google and listed on the
[Google Cloud locations page](https://cloud.google.com/about/locations),
or they might be leased from third-party data center providers. For the full
list of data center locations for Google Cloud, see our
[ISO/IEC 27001 certificate](https://cloud.google.com/security/compliance/iso-27001).
Regardless of whether the data center is owned or leased, Google Cloud selects
data centers and designs its infrastructure to provide a uniform level of
performance, security, and reliability.

A *zone* is a deployment area for Google Cloud resources within a region.
Zones should be considered a single failure domain within a region. To
deploy fault-tolerant applications with high availability and help protect
against unexpected failures, deploy your applications across multiple zones
in a region. Google Cloud also offers specialized AI zones that provide
high-capacity GPUs and TPUs for AI and ML workloads. For more information, see
[AI zones](https://cloud.google.com/compute/docs/regions-zones/ai-zones).

To protect against the loss of an entire region due to
natural disaster, have a disaster recovery plan and know how to bring
up your application in the unlikely event that your primary region is lost. See
[application deployment considerations](#application_deployment_considerations)
for more information.

For more information about the specific resources available within each location
option, see our [Cloud locations](https://cloud.google.com/about/locations/).

Google Cloud's services and resources can be [zonal](#zonal_resources),
[regional](#regional_resources), or [managed by Google across multiple
regions](#multiregional_resources). For more information about what these
options mean for your data, see
[geographic management of data](#geographic_management_of_data).

Google Cloud intends to offer a minimum of three availability zones
(physically and logically distinct zones) in every general-purpose region.

  Related location docs

- [Compute Engine regions and zones](https://cloud.google.com/compute/docs/regions-zones)
- [Cloud Storage bucket locations](https://cloud.google.com/storage/docs/bucket-locations)
- [App Engine locations](https://cloud.google.com/appengine/docs/locations)

### Zonal resources

Zonal resources operate within a single zone. Zonal outages can affect some or
all of the resources in that zone. An example of a zonal resource is a
Compute Engine virtual machine (VM) instance that resides within a
specific zone.

### Regional resources

Regional resources are resources that are redundantly deployed across multiple
zones within a region, for example App Engine applications, or
[regional managed instance groups](https://cloud.google.com/compute/docs/instance-groups#types_of_managed_instance_groups).
This gives them higher availability relative to zonal resources.

### Multiregional resources

Multiple Google Cloud services are managed by Google to be redundant and
distributed within and across regions. These services optimize availability,
performance, and resource efficiency. As a result, these services require a
trade-off between either latency or the consistency model. These trade-offs are
documented on a product specific basis.

The following services have one or more
[multiregional locations](https://cloud.google.com/about/locations#multi-region)
in addition to any regional locations:

- Artifact Registry
- Bigtable
- Sensitive Data Protection
- Cloud Healthcare API
- Cloud KMS
- Container Registry
- Spanner
- Cloud Storage
- Database Migration Service
- Datastore
- Firestore

These multiregional services are designed to be able to function following the
loss of a single region.

For more information, see
[Products available by location](https://cloud.google.com/about/locations#products-available-by-location),
and the documentation for each product.

## Global services

Google Cloud has been designed to operate globally
from the ground up and continually conducts maintenance and upgrades 24/7/365
without inconveniencing you. Our global backbone provides
tremendous flexibility for load-balancing, and reduces end-user latency by
having interconnects close to you. Our global cloud management plane simplifies
managing multi-region developments.

## Internal services

Underpinning and supporting many customer facing Google Cloud services
are a set of proven internal services like Spanner, Colossus, Borg, and
Chubby.

These internal services are either globally load-balanced across multiple
regions, or dedicated to each region in which they are available. Where
services are load-balanced across multiple regions, we deploy updates
progressively region-by-region, allowing us to detect and address problems
without affecting your service usage. None of these internal services are
limited to a single logical data center or to a single region.

Global Internal Services can run in or be replicated in the following cloud
[regions](https://cloud.google.com/compute/docs/regions-zones#available):

**Americas**

- southamerica-west1
- us-central1
- us-east1
- us-east4
- us-west1
- us-west4

**Europe**

- europe-north1
- europe-west1
- europe-west4

**Asia**

- asia-east1
- asia-southeast1

## Service dependencies

In general, for Google Cloud services, if a single region fails, only
customers solely in that region are impacted; customers who have multi-region
products are not impacted. Google Cloud has significant architecture
in place with a goal to prevent correlated failures across regions.

All Google Cloud services rely upon core internal tools to provide
fundamental services such as networking (in and out of data centers), access to
data centers, and identity authorization systems. These tools are resilient to
regional outages, with the goal of one region not being impacted if other
regions become unavailable.

Google Cloud provides clear direction on how customers can architect
their applications for the desired level of resilience on our
[public website](https://cloud.google.com/solutions/disaster-recovery/architecture#common_themes),
especially for commonly-used Google Cloud products such as
Compute Engine, BigQuery, Pub/Sub, and
other services.

Our major dependencies are listed below, starting with dependencies common to
all services, with the proviso that lower level implementation details are
subject to change.

### Common dependencies for all services

- Identity data plane for authentication and authorization
- Internal services that provide logging, metadata storage, and workflow
  management
- Access to Google Cloud APIs depends on DNS, globally-distributed
  load balancers, and points of presence (PoPs).
- The configuration of global resources: For example, IAM
  policies, global firewall rules, global load balancer configurations, and
  Pub/Sub topics are stored in replicated databases.
- When Google Cloud services makes requests to customer-controlled
  endpoints, for example, Cloud EKM fetching customer keys, or
  Pub/Sub delivering messages, those requests depend on our
  global network infrastructure to access those customer-controlled endpoints.

### Services with additional dependencies

- Compute Engine services
  - The Google Cloud VM and Persistent Disk data planes depend on
    lower-level Compute Engine and Cloud Storage services
    such as Borg and Colossus.
- Google Cloud and infrastructure storage services like Spanner,
  Bigtable, and Cloud Storage depend on:
  - Encryption and key management infrastructure for customer
    (Cloud KMS / Cloud EKM) and internal infrastructure for
    Google-owned keys
  - Internal services to provide logging and auditing of data access
  - Internal data replication services, where data is expected to be available
    across multiple regions
  - Explicitly-configured backups and replication to other regions depends
    on cross-region networking
- Messaging services
  - Pub/Sub depends on our global network infrastructure to access
    customer-controlled endpoints
- Networking services
  - Global load balancing, DNS, and failover between regions all depend on
    physical networking infrastructure.
  - Preventing DDos attacks, and the like, depends on lower-level
    Compute Engine infrastructure.
- Managed and hosted services like GKE and Cloud SQL
  - Depend on Compute Engine and either Container Registry or
    Artifact Registry for VM images.
- Self-contained lower-level infrastructure
  - Our internal cluster-level control plane including Borg and network fabrics
  - Cluster-level storage, such as Colossus
  - Encryption and key management infrastructure

## Maintaining and improving availability and resilience

Site Reliability Engineering (SRE) is Google's internal organization dedicated to
working on availability, latency, performance, and capacity. Outages and service
unavailability are correlated to the deployment of new code or changes to the
environment. By using industry best practices, SRE balances the need to release
new software and keeps the environment secure with the understanding that those
necessary changes might cause downtime.

## Partnering with customers to build resilient services

If you have mission-critical needs and need to architect for resilience and
[disaster recovery](https://cloud.google.com/architecture/disaster-recovery), our SRE/CRE and PSO teams
can work with you to architect your applications to bridge multiple regions and
zones and can further assist you with designing High Availability (HA) systems.

If you have heightened availability requirements around specific dates,
such as Black Friday and Cyber Monday, Google Cloud has a program to
partner with you to check and validate your specific application running on
Google Cloud and identify any unexpected service dependencies between your
application and our services.

## Points of presence (POPs)

Google operates a global network of peering points of presence, which means that
customer traffic can travel within the Google network until it's close to its
destination, providing users with a better experience and better security. For
more information, see
[Network edge locations](https://cloud.google.com/vpc/docs/edge-locations).

## Geographic management of data

Data locality for Google Cloud services are governed by the
[terms of service](https://cloud.google.com/terms), including
[service specific terms](https://cloud.google.com/terms/service-terms). Google understands that each
customer might have unique security and compliance needs. The
[Google Cloud sales team](https://cloud.google.com/contact) can help you work towards meeting
your requirements.

When using regional or zonal storage resources, we strongly recommend that
you replicate data to another region or snapshot it to a multiregional storage
resource for disaster recovery purposes.

## Application deployment considerations

  To build highly available services and applications that can withstand zones becoming unavailable

Use the following:

- [Regional resources](#regional_resources), such as App Engine
  applications,
  [regional managed instance groups](https://cloud.google.com/compute/docs/instance-groups#managed_instance_groups),
  or [managed multiregional resources](#multiregional_resources) such as
  Cloud Storage, Datastore, Firestore, or Spanner.
- Zonal resources, such as Compute Engine virtual machines, but manage your
  own compute and storage redundancy across zones or across regions.

 To build disaster recovery capable applications that can withstand the extended loss of entire regions

For data, use one or more of the following strategies:

- Use managed, multiregional storage services such as Cloud Storage,
  Datastore, Firestore, or Spanner.
- Use zonal or regional resources, but snapshot data to a multiregional
  resource such as Cloud Storage, Datastore,
  Firestore, or Spanner.
- Use zonal or regional resources, but manage your own data replication to
  one or more other regions.

For compute, use the following strategy:

- Use zonal or regional resources, such as Compute Engine or
  App Engine, but manually or automatically bring up your
  application in another region (on regional failure) referring to copies of
  your primary data if the data is not already in a managed, multiregional
  resource.

For more information about service dependencies,
[contact sales](https://cloud.google.com/contact/).

## Additional solutions and tutorials

The following solutions and tutorials provide guidance for ensuring your
application is highly available and can withstand outages:

#### Patterns for scalable and resilient apps

Learn how to use Google Cloud to build scalable and resilient
      application architectures using patterns and practices that apply broadly
      to any web application.

#### Creating an HTTPS load balancer

Configure Compute Engine instances in different regions and use HTTP
     load balancing to distribute traffic across the regions to increase
     availability across regions and provide failover in the case of a service
     outage.

#### Designing robust systems

Design your application on the Compute Engine
       service to be robust against failures, network interruptions, and
       unexpected disasters.

#### Cassandra Backup and Restore with Cloud Storage

Learn how to add basic disaster recovery to your Cassandra installation
        by backing up your data into, and restoring your data from,
        Cloud Storage.

#### Disaster recovery planning guide

General principles for designing and testing a disaster
        recovery plan with Google Cloud.

      Was this helpful?

---

# Get started with Google Cloud

> Steps and technical documentation to get started with your platform and environment setup in Google Cloud.

Start by creating a Google Cloud account. Plus, you get $300 in free credits and free usage of 20+ products on signup to run, test, and deploy workloads.
            [Create an account](https://console.cloud.google.com/freetrial?redirectPath=/welcome) [Google Cloud overview](https://cloud.google.com/docs/overview)
            Get hands-on experience with [free usage of 20+ products](https://cloud.google.com/free/docs/free-cloud-features#free-tier), including popular products like AI APIs, Compute Engine, BigQuery, and more.
            [Go to console](https://console.cloud.google.com/welcome) [Google Cloud overview](https://cloud.google.com/docs/overview)

## Start your platform setup

Click to show or hide setup steps by job function:

    IT administration    FinOps administration    Security engineering    DevOps engineering    Application development    Data analysis

Establish administrators, billing accounts, and other settings in your Google Cloud environment.

   [1](https://cloud.google.com/docs/enterprise/setup-checklist) [Establish your organization, administrators, and billing](https://cloud.google.com/docs/enterprise/setup-checklist)   [2](https://cloud.google.com/docs/enterprise/setup-checklist#create_an_initial_architecture) [Create an initial architecture](https://cloud.google.com/docs/enterprise/setup-checklist#create_an_initial_architecture)   [3](https://cloud.google.com/docs/enterprise/setup-checklist#deploy_your_settings) [Deploy or download configuration](https://cloud.google.com/docs/enterprise/setup-checklist#deploy_your_settings)

- [Cloud Quotas overview](https://cloud.google.com/docs/quotas/overview)
- [Google Cloud deployment archetypes (Architecture Center)](https://cloud.google.com/architecture/deployment-archetypes)

Set up billing, spending notifications, and resource structure to facilitate cost monitoring and optimization.

   [1](https://cloud.google.com/billing/docs/concepts) [Learn about Cloud Billing](https://cloud.google.com/billing/docs/concepts)   [2](https://cloud.google.com/billing/docs/how-to/create-billing-account) [Create a billing account](https://cloud.google.com/billing/docs/how-to/create-billing-account)   [3](https://cloud.google.com/billing/docs/how-to/budgets) [Set up spending notifications](https://cloud.google.com/billing/docs/how-to/budgets)   [4](https://cloud.google.com/billing/docs/how-to/export-data-bigquery) [Enable billing data export for custom reporting](https://cloud.google.com/billing/docs/how-to/export-data-bigquery)

- [Monitor costs using billing reports](https://cloud.google.com/billing/docs/reports)
- [Optimize costs with FinOps hub](https://cloud.google.com/billing/docs/how-to/finops-hub)
- [Resource hierarchy options for cost tracking](https://cloud.google.com/billing/docs/onboarding-checklist#projects-folders-labels)
- [Implement cost optimization strategies (Architecture Center)](https://cloud.google.com/architecture/framework/cost-optimization)

Familiarize yourself with core security concepts and tools that impact your security, privacy,
    and compliance controls.

   [1](https://cloud.google.com/apis/docs/getting-started) [Set up API access](https://cloud.google.com/apis/docs/getting-started)   [2](https://cloud.google.com/sdk/docs/install-sdk) [Install the gcloud CLI](https://cloud.google.com/sdk/docs/install-sdk)   [3](https://cloud.google.com/docs/get-started/authorization-access-control) [Learn about IAM in Google Cloud](https://cloud.google.com/docs/get-started/authorization-access-control)   [4](https://cloud.google.com/iam/docs/google-identities) [Understand identity management](https://cloud.google.com/iam/docs/google-identities)   [5](https://cloud.google.com/resource-manager/docs/organization-policy/overview) [Learn about organization policies](https://cloud.google.com/resource-manager/docs/organization-policy/overview)

- [Software supply chain security](https://cloud.google.com/software-supply-chain-security/docs/overview)
- [Security Command Center overview](https://cloud.google.com/security-command-center/docs/security-command-center-overview)
- [Well-Architected Framework: Security, privacy, and compliance (Architecture Center)](https://cloud.google.com/architecture/framework/security)

Start automating infrastructure and secure collaboration with teammates using Google Cloud tools and best practices.

   [1](https://cloud.google.com/apis/docs/getting-started) [Set up API access](https://cloud.google.com/apis/docs/getting-started)   [2](https://cloud.google.com/sdk/docs/install-sdk) [Install the gcloud CLI](https://cloud.google.com/sdk/docs/install-sdk)   [3](https://cloud.google.com/iam/docs/overview) [Enable teammates using IAM](https://cloud.google.com/iam/docs/overview)   [4](https://cloud.google.com/apis/docs/cloud-client-libraries) [Choose and install a Cloud Client Library](https://cloud.google.com/apis/docs/cloud-client-libraries)   [5](https://cloud.google.com/docs/authentication) [Learn about authentication](https://cloud.google.com/docs/authentication)   [6](https://cloud.google.com/docs/get-started/authorization-access-control) [Learn about authorization and access control](https://cloud.google.com/docs/get-started/authorization-access-control)

- [Observability in Google Cloud](https://cloud.google.com/stackdriver/docs)
- [Terraform and Infrastructure Manager](https://cloud.google.com/infrastructure-manager/docs/terraform)
- [CI/CD pipeline for containerized apps (Architecture Center)](https://cloud.google.com/architecture/app-development-and-delivery-with-cloud-code-gcb-cd-and-gke)

Get basic API access and set up a development environment that can interact with Google Cloud services.

   [1](https://cloud.google.com/apis/docs/getting-started) [Set up API access](https://cloud.google.com/apis/docs/getting-started)   [2](https://cloud.google.com/sdk/docs/install-sdk) [Install the gcloud CLI](https://cloud.google.com/sdk/docs/install-sdk)   [3](https://cloud.google.com/apis/docs/cloud-client-libraries) [Choose and install a Cloud Client Library](https://cloud.google.com/apis/docs/cloud-client-libraries)   [4](https://cloud.google.com/code/docs) [Set up IDE extensions](https://cloud.google.com/code/docs)   [5](https://cloud.google.com/docs/authentication) [Learn about authentication](https://cloud.google.com/docs/authentication)   [6](https://cloud.google.com/docs/get-started/authorization-access-control) [Learn about authorization and access control](https://cloud.google.com/docs/get-started/authorization-access-control)

- [Choose models and infrastructure for a generative AI application](https://cloud.google.com/docs/ai-ml/generative-ai)

Analyze sample data using Google Cloud products with minimal setup.

   [1](https://cloud.google.com/bigquery/docs/quickstarts/load-data-console) [Load and query sample data](https://cloud.google.com/bigquery/docs/quickstarts/load-data-console)   [2](https://cloud.google.com/bigquery/docs/visualize-looker-studio) [Explore, analyze, and share data](https://cloud.google.com/bigquery/docs/visualize-looker-studio)   [3](https://cloud.google.com/bigquery/docs/programmatic-analysis) [Learn about programmatic analysis tools](https://cloud.google.com/bigquery/docs/programmatic-analysis)   [4](https://cloud.google.com/bigquery/docs/bqml-introduction) [Introduction to AI and ML in BigQuery](https://cloud.google.com/bigquery/docs/bqml-introduction)

- [Set up the bq command-line tool](https://cloud.google.com/bigquery/docs/bq-command-line-tool)
- [Gemini in BigQuery overview](https://cloud.google.com/gemini/docs/bigquery/overview)
- [Data analytics design patterns (Architecture Center)](https://cloud.google.com/architecture/reference-patterns/overview)

            Learn and experiment with pre-built solution templates.

            Discover tools, resources, and products that enable interaction with Google Cloud using code.

            Follow recommendations and best practices to design and operate a well-architected cloud topology.

            A quick reference for Google Cloud products.

            Compare AWS and Azure services to Google Cloud.

            Explore our curriculum and grow your skills with Google Cloud Training.

---

# 48 results

> Spend smart and procure faster via online discovery, purchasing and fulfillment of enterprise-grade cloud solutions on Google Cloud Marketplace.

Start your Free Trial with $300 in credit. Don’t worry—you won’t be charged if you run out of credits. [Learn more](https://cloud.google.com/free/)      [Skip to main content](https://cloud.google.com/)[Accessibility Help](https://cloud.google.com/docs/accessibility?hl=en_US)[Accessibility Feedback](https://support.google.com/accessibility/contact/feedback?hl=en_US)                                                                                    [Google Cloud Marketplace Terms of Service](https://cloud.google.com/terms/marketplace/launcher)

## Your page may be loading slowly because you're building optimized sources. If you intended on using uncompiled sources,please click this link.

Hide the shortcuts helper

Google Cloud Console has failed to load JavaScript sources from www.gstatic.com.
Possible reasons are:

- www.gstatic.com or its IP addresses are blocked by your network administrator
- Google has temporarily blocked your account or network due to excessive automated requests

Please contact your network administrator for further assistance.HelpCloud HubSolutionsBillingIAM & AdminMarketplaceAPIs & ServicesVertex AICompute EngineKubernetes EngineCloud StorageSecurityBigQueryMonitoringCloud RunVPC NetworkCloud SQLGoogle Maps PlatformAlready on the first page.Previous 40 rowsNext 40 rows

---

# Infrastructure as code

> Documentation and resources for configuring your infrastructure using code with Google Cloud products and services.

[Get started for free](https://console.cloud.google.com/freetrial)

#### Start your proof of concept with $300 in free credit

- Develop with our latest Generative AI models and tools.
- Get free usage of 20+ popular products, including Compute Engine and AI APIs.
- No automatic charges, no commitment.

       [View free product offers](https://cloud.google.com/free/docs/free-cloud-features#free-tier)

#### Keep exploring with 20+ always-free products.

Access 20+ free products for common use cases, including AI APIs, VMs, data warehouses,
          and more.

                        Apply recommendations programmatically by integrating them into your Infrastructure as Code (IaC) pipeline.

                        Study how to write infrastructure as code with Terraform in Google Cloud.
                        Study step-by-step, command-line tutorials that walk you through the Terraform basics.

Expand this section to see relevant products and documentation.

     ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/developer-tools-color.svg)
                                      Automate the deployment and management of Google Cloud infrastructure resources using Terraform.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/developer-tools-color.svg)
                                      Define Google Cloud resources in human-readable configuration files that you can version, reuse, and share.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/developer-tools-color.svg)
                                      Configure Google Cloud services and resources using Kubernetes tooling and APIs.

                                      Configure Terraform to define and provision Google Cloud infrastructure and use your existing toolchain for tasks such as testing and dependency management.
                                      Author infrastructure code using programming languages such as TypeScript, Python, Go, C#, Java or YAML.
                                      Automate provisioning, configuration management, application deployment, orchestration and other IT processes.
                                      Connect your Kubernetes cluster to external, non-Kubernetes resources, and build custom Kubernetes APIs to consume those resources.            ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/developer-tools-color.svg)
                                      Manage cloud resources using simple templates.

---

# Google Cloud Documentation

> Comprehensive documentation, guides, and resources for Google Cloud products and services.

Find user guides, quickstarts, tutorials, use cases, code samples, and more.

                        [Get started for free](https://console.cloud.google.com/freetrial)

#### Start your proof of concept with $300 in free credit

- Develop with our latest Generative AI models and tools.
- Get free usage of 20+ popular products, including Compute Engine and AI APIs.
- No automatic charges, no commitment.

       [View free product offers](https://cloud.google.com/free/docs/free-cloud-features#free-tier)

#### Keep exploring with 20+ always-free products.

Access 20+ free products for common use cases, including AI APIs, VMs, data warehouses,
          and more.

            Learn about Google Cloud, including popular features with pointers to documentation and tutorials.

            Plan and design your infrastructure with architectural guidance and best practices.

            Start building in the console with $300 in free credits for new customers. All customers get free usage of over 20 products.

            Plan how to migrate your workloads, data, and processes.

            Compare AWS and Azure services to Google Cloud.

            Explore product quickstarts, tutorials, and interactive walkthroughs.

            Get generative-AI powered assistance with an always-on collaborator.

            Prepare your organization for scalable, production-ready, enterprise workloads.

            Study emerging cloud technologies and get Google Cloud certified.

            Review samples to demonstrate the use of Google Cloud products.

            Plan and quickly deploy pre-built solutions to solve your business challenges.

                         New guide
            Learn the stages of building a generative AI application, choose the best products and tools for your use case, and access the documentation you need to get started.

                  Popular guide
            Install and initialize the Google Cloud CLI and run core gcloud CLI commands.

            Leverage the power of AI/ML solutions to transform your organization and solve real-world problems.

            Create applications with a comprehensive set of tools and services.

            Run and manage applications on a secure platform.

            Run your workloads on virtual machines with specialized offerings for ML, high-performance computing, and other workloads to match your needs.

            Load, transform, and analyze data to provide business intelligence insights.

            Migrate and manage enterprise data with security, reliability, high availability, and fully-managed data services.

            Extend your Google Cloud topology to the edge, on-premises, and other cloud platforms.

            Build generative AI applications using a range of products and tools across the entire development life cycle.

            Transform your business with Google Cloud solutions for specific industries like retail, healthcare, and financial services.

            Tools and services to help you migrate to Google Cloud.

            Connect your networks and workloads, load balance traffic, and secure your network.

            Documentation, guides, and resources for observability and monitoring across Google Cloud products and services.

            Google Cloud security products help organizations secure their cloud environment, protect their data, and comply with industry regulations.

            Data storage, backup, and disaster recovery.

            Organize, analyze, and manage access to your Google Cloud resources and services.

            Manage costs and usage across Google Cloud products and services.

            Use Google Cloud SDK, languages, frameworks, and tools effectively in cloud development.

            Configure your infrastructure using code instead of graphical interfaces or command-line scripts.

            Use tools and information to help you on your journey to Google Cloud.

---

# Industry solutions

> Documentation and resources for transforming businesses in commerce, healthcare, and financial services with Google Cloud.

[Get started for free](https://console.cloud.google.com/freetrial)

#### Start your proof of concept with $300 in free credit

- Develop with our latest Generative AI models and tools.
- Get free usage of 20+ popular products, including Compute Engine and AI APIs.
- No automatic charges, no commitment.

       [View free product offers](https://cloud.google.com/free/docs/free-cloud-features#free-tier)

#### Keep exploring with 20+ always-free products.

Access 20+ free products for common use cases, including AI APIs, VMs, data warehouses,
          and more.

                        Study the various services Google Cloud offers for modernizing commerce applications and infrastructure.
                        Study the benefits of using Google Cloud to create large-scale visual effects rendering for image and video content.

Transform AML detection by replacing rules-based transaction monitoring with AI.

     ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/business-intelligence-color.svg)
                                      Detect suspicious, potential money laundering activity faster and more precisely with AI.

Digitally transform your healthcare and life sciences business though data-powered innovation.

     ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/ai-and-machine-learning-color.svg)
                                      Use a managed solution for storing and accessing healthcare data in Google Cloud, providing a critical bridge between existing care systems and applications hosted on Google Cloud.

                                      Use a family of foundation text-based models fine-tuned for the healthcare industry, serving specific customer needs such as answering medical questions and drafting summaries.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/ai-and-machine-learning-color.svg)
                                      Use natural language models to extract healthcare information from medical text.

                                      Empower data-driven innovation, transform the patient and caregiver experience, and enable operational efficiencies across your organization.

Transform audience experiences with innovation and insights.

     ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/ai-and-machine-learning-color.svg)
                                      Convert live video and package it for streaming.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/ai-and-machine-learning-color.svg)
                                      Convert video files and package them for optimized delivery to web, mobile, and connected TVs.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/ai-and-machine-learning-color.svg)
                                      Process and analyze your video streams and images at scale. Quickly build an application and deploy it to Google Cloud, using the built-in, low-code user interface.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/ai-and-machine-learning-color.svg)
                                      Dynamically insert ads into video-on-demand and live streams.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/ai-and-machine-learning-color.svg)
                                      Deliver rich, interactive 3D and augmented reality (AR) experiences to more devices by using cloud-based computing power.

                                      Transform audience experiences with innovation and insights.
                                      Train machine learning models to classify your images according to your own defined labels. (Deprecated. Use Vertex AI.)

                                      Train custom machine learning models that are capable of detecting individual objects in a given image along with its bounding box and label. (Deprecated. Use Vertex AI.)

                                      Add powerful search and recommendations capabilities to your media apps. Train search and recommendations models on your media catalog and user events.

Provide Google Search-quality product search, browsing, and recommendations to your commercecustomers.

     ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/business-intelligence-color.svg)
                                      Includes Retail Search and Recommendations to help you implement personalized search and recommendations, based on AI, across your websites and mobile applications.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/business-intelligence-color.svg)
                                      Allows ecommerce companies to create products, each containing reference images that visually describe the product from a set of viewpoints.

Use AI to solve problems at scale, increase quality hires, and improve subscriber acquisition and retention.

     ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/ai-and-machine-learning-color.svg)
                                      Solve your operational optimization problems rapidly and at massive scale.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/ai-and-machine-learning-color.svg)
                                      Service that brings machine learning to the job search experience, returning high quality results to job seekers far beyond the limitations of typical keyword-based methods.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/business-intelligence-color.svg)
                                       Enable communication service providers to extract information to recommend actions to telecom customers.

                                      View examples of how Google Cloud solutions help in various industries to improve efficiency and agility, reduce cost, participate in new business models, and capture new market opportunities.        ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/serverless-color.svg)
                                      Fully managed node hosting for developing on the blockchain.

---

# Migration

> Documentation and resources on available tools and services to help migrate to Google Cloud.

[Get started for free](https://console.cloud.google.com/freetrial)

#### Start your proof of concept with $300 in free credit

- Develop with our latest Generative AI models and tools.
- Get free usage of 20+ popular products, including Compute Engine and AI APIs.
- No automatic charges, no commitment.

       [View free product offers](https://cloud.google.com/free/docs/free-cloud-features#free-tier)

#### Keep exploring with 20+ always-free products.

Access 20+ free products for common use cases, including AI APIs, VMs, data warehouses,
          and more.

                        Plan, design, and implement the process of migrating your workloads to Google Cloud.
                        Plan, design, and implement your migration from AWS to Google Cloud.
                        Plan, design, and implement your migration from Azure to Google Cloud.
                        Plan, design, and implement your migration to a Google Cloud VMware Engine platform.
                        Use Migrate to Containers to modernize traditional applications away from virtual machine (VM) instances and into native containers that run on Google Kubernetes Engine (GKE) or Cloud Run platform.
                        Plan and prepare to migrate your workloads and data across Google Cloud regions.
                        Plan, design, and implement the process of migrating your databases to Google Cloud.
                        Study migrating a stand-alone PostgreSQL database to Cloud SQL for PostgreSQL using a continuous Database Migration Service job and VPC peering for connectivity.
                        Study migrating a MySQL database from an Amazon RDS instance for MySQL to Cloud SQL for MySQL using a one-time Database Migration Service job and an IP allowlist for connectivity.
                        Study Google Cloud technologies essential to the Startup Cloud Engineer role, including migration.
                        Study translating existing Azure knowledge to Google Cloud knowledge, while also preparing for certification.
                        Study Google Cloud solutions in comparison with Azure.
                        Study translating existing AWS knowledge to Google Cloud knowledge, while also preparing for certification.
                        Study Google Cloud solutions in comparison with AWS.

Discover, assess, and plan your migration to Google Cloud.

     ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/migration-color.svg)
                                      Discover, assess, and plan your migration to Google Cloud with a unified platform for your end-to-end cloud migration journey.

Migrate your virtual machines (VMs) to Google Cloud, or convert VM-based workloads into containers.

     ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/migration-color.svg)
                                      Migrate your VMs from a source environment to Google Cloud.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/migration-color.svg)
                                      Modernize traditional applications to run in containers on GKE, GKE Autopilot, or Cloud Run.

Migrate and modernize your mainframe workloads on Google Cloud.

     ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/migration-color.svg)
                                      Accelerate your journey end-to-end from your current mainframe setup to resources on Google Cloud.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/migration-color.svg)
                                      Simultaneously run workloads on your existing mainframes and on Google Cloud, and compare their behavior to gather data on performance and stability.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/migration-color.svg)
                                      Move data located on your mainframe in and out of Cloud Storage and submit BigQuery jobs from mainframe-based batch jobs, defined by job control language (JCL).

Explore related  Google Cloud products, guides, and resources for your migration scenarios.

                                      Compare AWS and Azure services to Google Cloud.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/databases-color.svg)
                                      Migrate your data to Google Cloud, and let the service streamline networking, manage replication, and provide a unified status of your migration.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/migration-color.svg)
                                      Migrate your data warehouse to BigQuery, and let the BigQuery Migration Service handle assessment, planning, SQL translation, data transfer, and validation.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/migration-color.svg)
                                      Migrate your Cloud Foundry workloads to Kubernetes with Kf, and let Kf preserve your developer workflows while you take advantage of GKE Enterprise features for governance.

                                      Migrate your VMware virtual machines to Google Cloud VMware Engine, and let VMware HCX handle site pairing, and workload migration.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/migration-color.svg)
                                      Move data between object and file storage systems, including from on-premises storage or other cloud providers to Cloud Storage.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/migration-color.svg)
                                      A high-capacity storage device that you can use to securely ship your data to a Google upload facility, where it's uploaded to Cloud Storage.
                                                Was this helpful?

---

# Networking

> Documentation and resources for Google Cloud products that connect your networks and workloads, load balance traffic, and help secure your network.

[Get started for free](https://console.cloud.google.com/freetrial)

#### Start your proof of concept with $300 in free credit

- Develop with our latest Generative AI models and tools.
- Get free usage of 20+ popular products, including Compute Engine and AI APIs.
- No automatic charges, no commitment.

       [View free product offers](https://cloud.google.com/free/docs/free-cloud-features#free-tier)

#### Keep exploring with 20+ always-free products.

Access 20+ free products for common use cases, including AI APIs, VMs, data warehouses,
          and more.

                        Deploy and connect resources in a virtual version of a physical network.

                        Choose how to connect your other networks to Google Cloud.

                        Choose a load balancer for your workload.

                        Observe, monitor, and troubleshoot your Google Cloud network and project resources using a single Google Cloud console.

                        Plan your networking approach with resources across a variety of networking topics.
                        Planning guide for cloud network architects and system architects familiar with Google Cloud networking concepts.

                        Planning resources across a wide variety of hybrid and multicloud subjects.
                        View news, updates, and best practices for Google Cloud networking products and services.
                        Study configuring, maintaining, and troubleshooting network components of your cloud-based infrastructure.
                        Get certified as a Google Cloud network engineer.

Set up your Virtual Private Cloud network and connect it to your other networks.

      ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/networking-color.svg)
                                      Scale and control how workloads connect regionally and globally.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/networking-color.svg)
                                      Access managed services, including Google APIs and services, privately from consumer VPC networks. Host managed services in producer VPC networks.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/networking-color.svg)
                                      Initiate outbound connections to the internet or to other VPC networks from VM instances and other resources.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/networking-color.svg)
                                      Optimize connectivity between systems on the internet and your Google Cloud instances.
                                              ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/networking-color.svg)
                                      Connect and manage your networks with a hub-and-spoke architecture, transfer data between your sites, and create VPC spokes to connect VPC networks.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/networking-color.svg)
                                      Securely connect your peer network to Google's network through an IPsec Cloud VPN tunnel or connect two VPCs together by connecting two Cloud VPN gateways.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/networking-color.svg)
                                      Connect your VPC networks and your other networks with low-latency, high-availability connections.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/networking-color.svg)
                                      Dynamically exchange routes between your VPC network and a peered networking using Border Gateway Protocol (BGP).

Make your services available at scale to your internal or external customers.

      ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/networking-color.svg)
                                      Scale, create, and update millions of DNS records reliably from anywhere in the world with Google’s anycast name servers.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/networking-color.svg)
                                      Respond instantaneously to changes in user traffic load, network conditions, and backend health by diverting traffic to other regions in the world.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/networking-color.svg)
                                      Enable programmability and extensibility at the edge and on load balancing data paths. Extends Google Cloud edge applications.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/networking-color.svg)
                                      Register and manage domains.
                                              ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/networking-color.svg)
                                      Deliver high-throughput egress workloads, such as streaming video and large file downloads. Complements Cloud CDN.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/networking-color.svg)
                                      Accelerate delivery of regularly accessed static content by caching it closer to your users. Cloud CDN serves a mix of static and dynamic latency-sensitive web assets.

                                      Establish direct peering links with Google's edge network at various locations to direct your traffic from your VPC networks to a provider's network.

Block unauthorized traffic and implement threat prevention and detection services.

     ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/networking-color.svg)
                                      Protect your Google Cloud workloads from internal and external attacks by using a fully distributed firewall service with advanced protection capabilities.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/networking-color.svg)
                                       Integrate third-party network appliances or service deployments with your Google Cloud workloads.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/networking-color.svg)
                                      Secure egress web traffic (HTTPS or HTTP) by using this cloud-first service.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/networking-color.svg)
                                      Protect sensitive data in Google Cloud services using security perimeters.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/networking-color.svg)
                                      Initiate outbound connections to the internet or to other VPC networks from VM instances and other resources.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/security-and-identity-color.svg)
                                      Acquire and manage Transport Layer Security (TLS) certificates for use with Cloud Load Balancing.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/networking-color.svg)
                                      Protect your Google Cloud deployments from multiple types of threats, including distributed denial-of-service (DDoS) attacks and application attacks.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/networking-color.svg)
                                      Detect threats including intrusions, malware, spyware, and command-and-control attacks on your network.

Monitor and troubleshoot your Google Cloud network.

     ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/networking-color.svg)
                                      Observe, monitor, and troubleshoot your Google Cloud network and project resources using a single Google Cloud console. Reduce the risk of outages and ensure security and compliance.

                                      Record a sample of network flows sent from and received by VM instances, including instances used as GKE nodes.

                                      Audit, verify, and analyze the effects of your firewall rules.

                                      Clone the traffic of specific instances in your VPC network and forward it for examination.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/observability-color.svg)
                                      Store, search, analyze, monitor, and alert on log data and events from Google Cloud and AWS.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/observability-color.svg)
                                      Monitor the performance, availability, and overall health of cloud-powered applications.

                                      Plan your GKE networking infrastructure.

                                      Learn about networking for Google Cloud virtual machines.

                                      Configure internal DNS for your Google Cloud virtual machines.

                                      Connect to your Google Cloud virtual machines using SSH.

                                      Configure VLAN and subnets on VMware Engine.

                                      Send outbound traffic from Cloud Run to a VPC network.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/networking-color.svg)
                                      Implement a service mesh on-premises or on Google Cloud, using open source or Google Cloud APIs.

                                      Implement a suite of tools to monitor and manage a reliable service mesh on-premises or on Google Cloud.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/storage-color.svg)
                                      Store objects with global edge caching.
