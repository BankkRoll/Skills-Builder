# Observability and monitoring and more

# Observability and monitoring

> Documentation and resources for observability and monitoring across Google Cloud products and services.

[Get started for free](https://console.cloud.google.com/freetrial)

#### Start your proof of concept with $300 in free credit

- Develop with our latest Generative AI models and tools.
- Get free usage of 20+ popular products, including Compute Engine and AI APIs.
- No automatic charges, no commitment.

       [View free product offers](https://cloud.google.com/free/docs/free-cloud-features#free-tier)

#### Keep exploring with 20+ always-free products.

Access 20+ free products for common use cases, including AI APIs, VMs, data warehouses,
          and more.

                        Monitoring, logging, tracing, profiling, and debugging for observability.

                        Collect Prometheus metrics for your workloads.

                        Collect telemetry from your applications with instrumentation.

                        Collect telemetry from your Compute Engine instances.

                        Collect and manage logs with storage, search, analysis, and monitoring support.

                        Learn about Cloud Monitoring, the integrated monitoring service for Google Cloud.

                        Plan your approach with Architecture Center resources across a variety of monitoring and logging topics.
                        Plan how to implmement monitoring and logging architectures for hybrid and multi-cloud deployments.
                        View how to troubleshoot distributed applications by using Cloud Trace and Cloud Logging together.
                        View how to access detailed logs of events and activities within your cloud environment.
                        View how the relevance of what we are monitoring can help us support triage in advance.
                        View step by step instructions on how you can get started with Google Cloud synthetic monitoring.
                        View how Cloud Audit logs can help customers meet their compliance and security requirements.
                        View these best practices to learn how to get the most out of your Google Cloud and third-party logging tools.
                        Study how to use application performance management tools, including Error Reporting, Cloud Trace, and Cloud Profiler.
                        Study how to implement efficient and reliable software delivery and infrastructure management.

Integrated monitoring, logging, and trace managed services for applications and systems running on Google Cloud and beyond.

     ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/observability-color.svg)
                                      Monitor, log, trace, and profile your apps and services.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/observability-color.svg)
                                      Store, search, analyze, monitor, and alert on log data and events from Google Cloud and AWS.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/observability-color.svg)
                                      Analyze, monitor, and display the performance data collected from your applications and the Google Cloud services that you use.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/observability-color.svg)
                                      Find performance bottlenecks in production.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/observability-color.svg)
                                      Identify and understand application errors.

Continuous profiling of production systems for large-scale operations.

     ![](https://cloud.google.com/_static/clouddocs/images/icons/products/sql-color.svg)
                                      Continuously gather performance information using a low-impact CPU and heap profiling service.
                                                ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/observability-color.svg)
                                      Understand the health of your applications and maintain application availability and reliability.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/observability-color.svg)
                                      Use Compute Engine instances that run the public images for Linux and Windows Server that Google provides, or that run your own private custom images.

                                      Access and view virtual machine (VM) metrics.

                                      Build and connect cloud services in a serverless execution environment.

                                      Use the Prometheus sidecar to get Prometheus-style monitoring for Cloud Run services.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/developer-tools-color.svg)
                                      Learn how to use Terraform to reliably provision infrastructure on Google Cloud.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/operations-color.svg)
                                      Discover and organize infrastructure resources into applications.

                                      View a post for migrating from BigQuery log sink to Log Analytics.

                                      Learn how to deliver Cloud Monitoring alert notifications to third-party services that don't have supported notification channels.
                                              ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/operations-color.svg)
                                      Manage Cloud Logging.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/operations-color.svg)
                                      Manage Monitoring dashboards.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/observability-color.svg)
                                      View a list of the available monitoring APIs and reference content.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/observability-color.svg)
                                      View a list of the available logging APIs and reference content.
                                                Was this helpful?

---

# Google Cloud overviewStay organized with collectionsSave and categorize content based on your preferences.

> Get a basic overview of Google Cloud Platform, learn about overall concepts and gain pointers to our resources.

# Google Cloud overviewStay organized with collectionsSave and categorize content based on your preferences.

This overview is designed to help you understand the overall landscape of
Google Cloud. You'll learn about how Google Cloud is structured,
how its functionality is provided as services, and the different ways that
you can interact with it when designing, creating, and running your applications.

As you explore the rest of this Get started section, you'll learn more about Google Cloud's tooling and resources, and how to get started creating and managing your own applications on Google Cloud.

For general information on cloud computing, see
[Advantages and disadvantages of cloud computing](https://cloud.google.com/learn/advantages-of-cloud-computing).

## Universes,regions,and zones

Underlying everything you do with Google Cloud technology
are the physical machines that run your workloads and Google Cloud
services. These machines live in data centers, and are logically structured into
universes, regions, and zones.

At the top of this hierarchy is the *universe*. A universe is a fully
self-contained cloud, with its own networking that is separate from the public
internet and other universes. Google Cloud is the original
universe, with resources in data centers all over the world.  There are also other universes, based on the same technology as Google Cloud but with all their resources in a single jurisdiction and running in partner-operated datacenters. These self-contained smaller clouds are created as part of a program called Google Cloud Dedicated and provide strong data and operational sovereignty guarantees for users whose workloads require them.

Within each universe there are geographic *regions*. Google Cloud
has regions in
Asia, Australia, Europe, Africa, the Middle East, North America, and South
America.

Finally, regions are divided into *zones*. Each zone is identified by a
name that combines a letter identifier with the name of the region. For example,
zone `a` in the East Asia region is named `asia-east1-a`. Zones have high-bandwidth,
low-latency network connections to other zones in the same region.

This distribution of resources in a universe into regions and zones provides several benefits, including redundancy
in case of failure and reduced latency by locating resources closer to clients.
This distribution also introduces some rules about how resources can be used
together.

## Global,regional,and zonal resources

Some resources can be accessed by any other resource in their universe, across regions and zones.
These *global resources* include preconfigured disk images, disk snapshots,
and networks. Some resources can be accessed only by
resources that are located in the same region. These *regional resources*
include static external IP addresses. Other resources can be accessed only by
resources that are located in the same zone. These *zonal resources* include VM
instances, their types, and disks.

The following diagram shows the relationship
between global scope, regions and zones, and some of their resources:

![A global network can contain region-specific resources such as IP
         addresses and zone-specific resources such as VMs and disks.](https://cloud.google.com/static/docs/images/overview/regions-zones.svg)

The scope of an operation varies depending on what kind of resources
you're working with. For example, creating a network is a global operation
because a network is a global resource, while reserving an IP address is a
regional operation because the address is a regional resource.

As you start to design and optimize your Google Cloud applications, it's important to
understand how these regions and zones interact. For example, even if you could,
you wouldn't want to attach a disk in one region to a computer in a different
region because the latency you'd introduce would make for poor performance.
Thankfully, Google Cloud won't let you do that; disks can only be attached
to computers in the same zone.

Depending on the level of self-management required for the
[computing and hosting service](https://cloud.google.com/docs/overview/cloud-platform-services#computing-hosting) you
choose, you might or might not need to think about how and where resources are
allocated.

For more information about the geographical distribution of Google Cloud,
see [Geography and Regions](https://cloud.google.com/docs/geography-and-regions).

## Accessing resources through services

In cloud computing, what you might be used to thinking of as software and
hardware products, become *services*. These services provide access to the
underlying resources, letting you add a wide range of functionality—from
managed Kubernetes to data storage—to your applications. You can see the list
of available Google Cloud services in our
[product list](https://cloud.google.com/products/).

When you develop your website or application on
Google Cloud, you mix and match these services into combinations that
provide the infrastructure you need, and then add your code to enable the
scenarios you want to build.

## Projects

Any Google Cloud resources that you allocate and use must belong to a
project. You can think of a project as the organizing entity for what you're
building. A project is made up of the settings, permissions, and other metadata
that describe your applications. Resources within a single project can work
together easily, for example by communicating through an internal network,
subject to the regions-and-zones rules. A project can't access another project's
resources unless you use [Shared VPC](https://cloud.google.com/vpc/docs/shared-vpc) or
[VPC Network Peering](https://cloud.google.com/vpc/docs/vpc-peering).

Each Google Cloud project has the following:

- A project name, which you provide.
- A project ID, which you can provide or Google Cloud can provide for you.
- A project number, which Google Cloud provides.

So, for example, the same project might have:

- The project name **Example Project**
- The project ID **example-id**
- The project number **123456789012**

As you work with Google Cloud, you use these
identifiers in commands and API calls. For example, you might specify that you
want to use the project as your default for the Google Cloud CLI with the
following command:

```
gcloud config set project example-id
```

You can create multiple projects and use them to separate your work in whatever
way makes sense for you and your organization. For example, you might have one project that can be
accessed by all team members and a separate project that can only be accessed by
certain team members.

A project serves as a namespace. This means every resource within each project
must have a unique name, but you can usually reuse resource names if they are in
separate projects. Some resource names must be unique within Google Cloud. Refer to the documentation for the resource for details.

Each project is associated with one billing account. Multiple projects can have
their resource usage billed to the same account.

For more information, see
[Creating and managing projects](https://cloud.google.com/resource-manager/docs/creating-managing-projects).

## Interacting with Google Cloud

There are multiple ways to interact with resources and services in Google Cloud, including the following:

- The [Google Cloud console](https://console.cloud.google.com/) provides a web-based, graphical user
  interface that you can use to manage your Google Cloud
  projects and resources.
- The [Google Cloud CLI](https://cloud.google.com/sdk/gcloud) lets you manage development workflow and
  Google Cloud resources directly from the
  command line. For example, you can create a Compute Engine virtual machine
  (VM) instance by running the `gcloud compute instances create` command in
  your shell environment. You can choose between installing the Google Cloud CLI on your local machine, or using it in [Cloud Shell](https://cloud.google.com/shell/docs/features),
  a convenient browser-based shell that you can access from the Google Cloud console and which has many tools pre-installed.
- Our provided [client libraries](https://cloud.google.com/apis/docs/client-libraries-explained) help
  you to interact with services programmatically in a variety of popular
  languages. Cloud Client Libraries provide an optimized developer experience by
  using each supported language's natural conventions and styles. They also
  reduce the boilerplate code you have to write because they're designed to
  enable you to work with service metaphors in mind, rather than
  implementation details or service API concepts.
- You can use an "infrastructure as code" (IaC) approach by using
  [Terraform](https://cloud.google.com/docs/terraform) and the Google Cloud Terraform
  provider.

You can learn more in [Interacting with Google Cloud](https://cloud.google.com/docs/get-started/interact-with-resources).

## Pricing

To learn how to explore and evaluate Google Cloud at no cost, see
[Free Google Cloud features and trial offer](https://cloud.google.com/free/docs/free-cloud-features).

To browse pricing details for individual services, see the
[price list](https://cloud.google.com/pricing/list).

To estimate your total costs for running a specific workload on
Google Cloud, see the
[pricing calculator](https://cloud.google.com/products/calculator).

## What's next

- Visit [Get started with Google Cloud](https://cloud.google.com/docs/get-started) to explore setup paths and resources for IT administrators, security engineers, application developers, and more.
- Delve deeper into [interacting with Google Cloud](https://cloud.google.com/docs/get-started/interact-with-resources).
- For administrators of new organizations on Google Cloud, our [Google Cloud Setup](https://cloud.google.com/docs/enterprise/cloud-setup) guided flow helps you build a robust foundation for your organization's workloads that embodies best practices for enterprise infrastructure.

If you're new to Google Cloud, create an account to evaluate how our
      products perform in real-world scenarios. New customers also get $300 in
      free credits to run, test, and deploy workloads.

 [Get started for free](https://console.cloud.google.com/freetrial)      Was this helpful?

---

# Google Cloud products at a glance

> A quick reference for Google Cloud products.

A quick reference for Google Cloud products

## Cross-product tools

- [Cloud BillingBilling & cost management tools](https://cloud.google.com/billing/docs)
- [Cloud IdentityManage users, devices & apps](https://cloud.google.com/identity/docs)
- [Cloud QuotasManage service quotas & usage](https://cloud.google.com/docs/quotas)
- [Config ConnectorKubernetes add-on to manage resources](https://cloud.google.com/config-connector/docs)
- [Deployment ManagerTemplated infrastructure deployment](https://cloud.google.com/deployment-manager/docs)
- [Identity PlatformCustomer identity access management](https://cloud.google.com/identity-platform/docs)
- [Infra ManagerAutomate infrastructure resource deployment](https://cloud.google.com/infrastructure-manager/docs)
- [Managed Microsoft ADManaged Microsoft Active Directory](https://cloud.google.com/managed-microsoft-ad/docs)
- [RecommenderCloud usage recommendations & insights](https://cloud.google.com/recommender/docs)
- [Service CatalogManage internal enterprise solutions](https://cloud.google.com/service-catalog/docs)
- [Service UsageManage APIs & services in projects](https://cloud.google.com/service-usage/docs)

## AI and ML

- [Cloud TPUHardware acceleration for ML](https://cloud.google.com/tpu/docs)
- [Colab EnterpriseColab notebooks for enterprises](https://cloud.google.com/colab/docs)
- [Deep Learning ContainersPreconfigured containers for deep learning](https://cloud.google.com/deep-learning-containers/docs)
- [Deep Learning VMPreconfigured VMs for deep learning](https://cloud.google.com/deep-learning-vm/docs)
- [DocAIAnalyze, classify, search documents](https://cloud.google.com/document-ai/docs)
- [Enterprise Knowledge GraphConsolidate & reconcile organizational knowledge](https://cloud.google.com/enterprise-knowledge-graph/docs)
- [Immersive Stream for XRHost & serve interactive 3D & AR](https://cloud.google.com/immersive-stream/xr/docs)
- [Speech-to-TextConvert audio to text](https://cloud.google.com/speech-to-text/docs)
- [TensorFlow EnterpriseScalable TensorFlow development experience](https://cloud.google.com/tensorflow-enterprise/docs)
- [Text-to-SpeechConvert text to audio](https://cloud.google.com/text-to-speech/docs)
- [TranslationLanguage detection & translation](https://cloud.google.com/translate/docs)
- [Vertex AIManaged platform for ML](https://cloud.google.com/vertex-ai/docs)
- [Vertex AI VisionIngest, analyze & store video data](https://cloud.google.com/vision-ai/docs)
- [Vertex AI WorkbenchJupyter-based environment for data science](https://cloud.google.com/vertex-ai/docs/workbench/instances)
- [Vision APIImage recognition & classification](https://cloud.google.com/vision/docs)

## App development

- [API GatewayFully-managed API gateway](https://cloud.google.com/api-gateway/docs)
- [ApigeeNative API management platform](https://cloud.google.com/apigee/docs)
- [App HubView & understand app resources](https://cloud.google.com/app-hub/docs)
- [Application IntegrationEnterprise application integrations](https://cloud.google.com/application-integration/docs)
- [Artifact AnalysisAutomated security scanning](https://cloud.google.com/artifact-analysis/docs)
- [Cloud BuildDevOps automation platform](https://cloud.google.com/build/docs)
- [Cloud CodeIntelliJ Google Cloud tools](https://cloud.google.com/code/docs/intellij)
- [Cloud DeployContinuous delivery for GKE](https://cloud.google.com/deploy/docs)
- [Cloud SchedulerManaged cron job service](https://cloud.google.com/scheduler/docs)
- [Cloud ShellBrowser-based terminal/CLI](https://cloud.google.com/shell/docs)
- [Cloud TasksAsynchronous task execution](https://cloud.google.com/tasks/docs)
- [Cloud WorkstationsCloud-based developer workstations](https://cloud.google.com/workstations/docs)
- [Developer ConnectConnect source control systems](https://cloud.google.com/developer-connect/docs)
- [EventarcAsynchronous event delivery](https://cloud.google.com/eventarc/docs)
- [gcloud CLIGoogle Cloud command-line tool](https://cloud.google.com/sdk/docs)
- [Integration ConnectorsEnterprise application connectivity](https://cloud.google.com/integration-connectors/docs)
- [Pub/SubGlobal real-time messaging](https://cloud.google.com/pubsub/docs)
- [Secure Source ManagerManaged single-tenant source code repository](https://cloud.google.com/secure-source-manager/docs)
- [Service InfrastructureCross-organization foundational service platform](https://cloud.google.com/service-infrastructure/docs)
- [Software supply chain securitySecure software supply chain](https://cloud.google.com/software-supply-chain-security/docs)
- [Tools for Visual StudioVisual Studio Google Cloud tools](https://cloud.google.com/tools/visual-studio/docs)
- [WorkflowsHTTP services orchestration](https://cloud.google.com/workflows/docs)

## App hosting

- [App EngineManaged app platform](https://cloud.google.com/appengine/docs)
- [Blockchain Node EngineFully-managed blockchain nodes](https://cloud.google.com/blockchain-node-engine/docs)
- [Blockchain RPCRead/write to multiple blockchains](https://cloud.google.com/blockchain-rpc/docs)
- [Cloud RunFully-managed serverless application platform](https://cloud.google.com/run/docs)
- [Google Kubernetes Engine (GKE)Managed Kubernetes/containers](https://cloud.google.com/kubernetes-engine/docs)

## Compute

- [AI HypercomputerSupercomputer architecture for AI](https://cloud.google.com/ai-hypercomputer/docs)
- [BatchManaged batch processing service](https://cloud.google.com/batch/docs)
- [Capacity PlannerView & forecast compute usage](https://cloud.google.com/capacity-planner/docs)
- [Cluster toolkitDeploy HPC, AI & ML workloads](https://cloud.google.com/cluster-toolkit/docs)
- [Compute EngineVMs, GPUs, TPUs, disks](https://cloud.google.com/compute/docs)
- [Migrate to ContainersMigrate VMs to Kubernetes Engine](https://cloud.google.com/migrate/containers/docs)
- [Migrate to VMsMigrate VMs to Compute Engine](https://cloud.google.com/migrate/virtual-machines/docs/5.0)
- [Migration CenterAccelerate end-to-end migration](https://cloud.google.com/migration-center/docs)
- [Shielded VMsVM boot-time protection](https://cloud.google.com/compute/shielded-vm/docs)
- [VM ManagerManage OS VM Fleets](https://cloud.google.com/compute/vm-manager/docs)
- [VMware EngineVMware as a service](https://cloud.google.com/vmware-engine/docs)
- [Workload ManagerRule-based workload evaluation](https://cloud.google.com/workload-manager/docs)

## Data analytics and pipelines

- [BigQueryData warehouse & analytics](https://cloud.google.com/bigquery/docs)
- [Blockchain AnalyticsIndexed blockchain data for analysis](https://cloud.google.com/blockchain-analytics/docs)
- [Cloud ComposerManaged workflow orchestration service](https://cloud.google.com/composer/docs)
- [Cloud Data FusionGraphically manage data pipelines](https://cloud.google.com/data-fusion/docs)
- [DataflowStream/batch data processing](https://cloud.google.com/dataflow/docs)
- [DataformELT & SQL workflow tool](https://cloud.google.com/dataform/docs)
- [DataplexCentrally manage & govern data](https://cloud.google.com/dataplex/docs)
- [DataprocManaged Spark & Hadoop](https://cloud.google.com/dataproc/docs)
- [Dataproc ServerlessRun serverless Spark batch workloads](https://cloud.google.com/dataproc-serverless/docs)
- [DatastreamChange data capture/replication service](https://cloud.google.com/datastream/docs)
- [LookerEnterprise BI & analytics](https://cloud.google.com/looker/docs)

## Databases

- [AlloyDB for PostgreSQLScalable & performant PostgreSQL-compatible DB](https://cloud.google.com/alloydb/docs)
- [BigtablePetabyte-scale, low-latency, non-relational](https://cloud.google.com/bigtable/docs)
- [Cloud SQLManaged MySQL, PostgreSQL, SQL Server](https://cloud.google.com/sql/docs)
- [Database Migration ServiceMigrate to Google Cloud databases](https://cloud.google.com/database-migration/docs)
- [FirestoreServerless NoSQL document DB](https://cloud.google.com/firestore/docs)
- [Memorystore for MemcachedManaged Memcached service](https://cloud.google.com/memorystore/docs/memcached)
- [SpannerHorizontally scalable relational DB](https://cloud.google.com/spanner/docs)

## Distributed,hybrid,and multicloud

- [GKE Multi-CloudMulti-cloud cluster creation](https://cloud.google.com/kubernetes-engine/multi-cloud/docs)

## Industry solutions

- [Anti Money Laundering AI (AML AI)Detect potential money laundering activity](https://cloud.google.com/financial-services/anti-money-laundering/docs)
- [Healthcare Data EngineHealthcare system Google Cloud interoperability](https://cloud.google.com/healthcare-api/docs)
- [Talent SolutionsJob search with ML](https://cloud.google.com/talent-solution/job-search/docs)
- [Telecom Network AutomationManaged cloud implementation of Nephio](https://cloud.google.com/telecom-network-automation/docs)
- [Telecom Subscriber Insights APIInsights for communication service providers](https://cloud.google.com/telecom-subscriber-insights/docs)
- [Vertex AI Search for retailPersonalized search for retail](https://cloud.google.com/retail/docs)

## Networking

- [Cloud CDNCache content near users](https://cloud.google.com/cdn/docs)
- [Cloud DNSProgrammable DNS serving](https://cloud.google.com/dns/docs)
- [Cloud Intrusion Detection System (Cloud IDS)Detect network-based threats](https://cloud.google.com/intrusion-detection-system/docs)
- [Cloud InterconnectConnect networks to Google](https://cloud.google.com/network-connectivity/docs/interconnect)
- [Cloud Load BalancingMulti-region load distribution/balancing](https://cloud.google.com/load-balancing/docs)
- [Cloud NATNetwork address translation service](https://cloud.google.com/nat/docs)
- [Cloud Next Generation Firewall (Cloud NGFW)Fully-distributed firewall service](https://cloud.google.com/firewall/docs)
- [Cloud RouterVPC/on-prem network route exchange (BGP)](https://cloud.google.com/network-connectivity/docs/router)
- [Cloud Service MeshService mesh traffic management](https://cloud.google.com/service-mesh/docs)
- [Cloud VPNVirtual private network connection](https://cloud.google.com/network-connectivity/docs/vpn)
- [Google Cloud ArmorDDoS protection & WAF](https://cloud.google.com/armor/docs)
- [Media CDNCDN for streaming & videos](https://cloud.google.com/media-cdn/docs)
- [Network Connectivity CenterConnect VPC & on-prem](https://cloud.google.com/network-connectivity/docs/network-connectivity-center)
- [Network Intelligence CenterNetwork monitoring & topology](https://cloud.google.com/network-intelligence-center/docs)
- [Network Service TiersPrice versus performance tiering](https://cloud.google.com/network-tiers/docs)
- [Secure Web ProxySecure egress web traffic](https://cloud.google.com/secure-web-proxy/docs)
- [Service ExtensionsAdd custom logic for edge applications](https://cloud.google.com/service-extensions/docs)
- [Virtual Private Cloud (VPC)Software-defined networking](https://cloud.google.com/vpc/docs)
- [VPC Service ControlsSecurity perimeters for service segregation](https://cloud.google.com/vpc-service-controls/docs)

## Observability and monitoring

- [Error ReportingApp error reporting](https://cloud.google.com/error-reporting/docs)
- [LoggingCentralized data & event logging](https://cloud.google.com/logging/docs)
- [MonitoringInfrastructure & application monitoring](https://cloud.google.com/monitoring/docs)
- [ProfilerCPU & heap reporting](https://cloud.google.com/profiler/docs)
- [TraceApp latency insights](https://cloud.google.com/trace/docs)

## Security

- [Access Context ManagerFine-grained, attribute-based access control](https://cloud.google.com/access-context-manager/docs)
- [Access TransparencyAudit cloud provider support access](https://cloud.google.com/assured-workloads/access-transparency/docs)
- [Advisory NotificationsPrivacy & security event notifications](https://cloud.google.com/advisory-notifications/docs)
- [Assured OSSGet verified open-source packages](https://cloud.google.com/assured-open-source-software/docs)
- [Binary AuthorizationKubernetes deploy-time security](https://cloud.google.com/binary-authorization/docs)
- [Certificate AuthorityCreate & manage private CAs](https://cloud.google.com/certificate-authority-service/docs)
- [Certificate ManagerAcquire & manage TLS certificates](https://cloud.google.com/certificate-manager/docs)
- [Chrome Enterprise PremiumZero-trust secure access](https://cloud.google.com/chrome-enterprise-premium/docs)
- [Cloud Asset InventoryAll assets, one place](https://cloud.google.com/asset-inventory/docs)
- [Cloud KMSHosted key management service](https://cloud.google.com/kms/docs)
- [Confidential VMEncrypt data in-use](https://cloud.google.com/confidential-computing/confidential-vm/docs)
- [Endpoint VerificationAccess control for business devices](https://cloud.google.com/endpoint-verification/docs)
- [Google SecOpsTool for SecOps, SIEM & SOAR](https://cloud.google.com/chronicle/docs)
- [Identity and Access Management (IAM)Resource access control](https://cloud.google.com/iam/docs)
- [Identity-Aware ProxyIdentity-based app access](https://cloud.google.com/iap/docs)
- [Policy IntelligenceUnderstand policies & usage](https://cloud.google.com/policy-intelligence/docs)
- [reCAPTCHAAdvanced bot & fraud detection](https://cloud.google.com/recaptcha/docs)
- [Resource ManagerCloud project metadata management](https://cloud.google.com/resource-manager/docs)
- [Secret ManagerStore & manage secrets](https://cloud.google.com/secret-manager/docs)
- [Security Command CenterSecurity management & data risk platform](https://cloud.google.com/security-command-center/docs)
- [Sensitive Data ProtectionClassify & redact sensitive data](https://cloud.google.com/sensitive-data-protection/docs)
- [Service HealthIdentify cloud service disruptions](https://cloud.google.com/service-health/docs)
- [Web RiskCheck URLs for safety](https://cloud.google.com/web-risk/docs)

## Storage

- [Backup and DR ServiceBackup & DR SaaS](https://cloud.google.com/backup-disaster-recovery/docs)
- [Cloud StorageMulti-class multi-region object storage](https://cloud.google.com/storage/docs)
- [FilestoreManaged network-attached storage](https://cloud.google.com/filestore/docs)

---

# Cloud Quotas documentation

> Get documentation for Cloud Quotas

# Cloud Quotas documentation

  [Read product documentation](https://docs.cloud.google.com/docs/quotas/overview)

Cloud Quotas enables customers to manage quotas for all of their Google Cloud services. With
    Cloud Quotas, users are able to easily monitor quota usage, create and modify quota
    alerts, and request limit adjustments for quotas. Quotas are managed through the Cloud Quotas
    dashboard or the Cloud Quotas API.
    [Learn more](https://cloud.google.com/docs/quotas/overview).

               [Get started for free](https://console.cloud.google.com/freetrial)

#### Start your proof of concept with $300 in free credit

- Develop with our latest Generative AI models and tools.
- Get free usage of 20+ popular products, including Compute Engine and AI APIs.
- No automatic charges, no commitment.

       [View free product offers](https://cloud.google.com/free/docs/free-cloud-features#free-tier)

#### Keep exploring with 20+ always-free products.

Access 20+ free products for common use cases, including AI APIs, VMs, data warehouses,
          and more.

- [Overview](https://cloud.google.com/docs/quotas/overview)
- [View and manage quotas](https://cloud.google.com/docs/quotas/view-manage)
- [Predefined roles and permissions](https://cloud.google.com/docs/quotas/permissions)

- [REST API](https://cloud.google.com/docs/quotas/reference/rest)
- [Client libraries](https://cloud.google.com/docs/quotas/reference/libraries)

- [Release notes](https://cloud.google.com/docs/quotas/release-notes)

          Was this helpful?

---

# Security

> Documentation and resources for helping organizations secure their compute environments, protect data, and comply with regulations using Google Cloud products.

[Get started for free](https://console.cloud.google.com/freetrial)

#### Start your proof of concept with $300 in free credit

- Develop with our latest Generative AI models and tools.
- Get free usage of 20+ popular products, including Compute Engine and AI APIs.
- No automatic charges, no commitment.

       [View free product offers](https://cloud.google.com/free/docs/free-cloud-features#free-tier)

#### Keep exploring with 20+ always-free products.

Access 20+ free products for common use cases, including AI APIs, VMs, data warehouses,
          and more.

                        Learn the physical, administrative, and technical controls we use to help protect your organization's data.

                        Learn how IAM works in Google Cloud and how you can use it to manage access.

                        Learn what organization policies and constraints are.

                        Learn the key authentication methods and concepts to confirm a user's identity.

                        Learn how security is designed into Google's technical infrastructure.

                        Remove a user's access to a Google Cloud project.

                        Plan how to deploy a foundational set of resources in Google Cloud using best practices.
                        Study how to develop, implement, and monitor your organization's security infrastructure.
                        Listen to industry experts talk about some of the most interesting areas of cloud security.
                        Read the latest blog posts about Google Cloud security benefits and customer stories.
                        Study how to use SIEM and SOAR tools to parse data, build rules, develop playbooks, and respond to incidents.
                        Study how to develop, implement, and monitor your organization’s security infrastructure.

Detect vulnerabilities, threats, and misconfigurations.

     ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/security-and-identity-color.svg)
                                      Receive well-targeted, timely, and compliant communications about security and privacy events in the Google Cloud console.

                                      Evaluate your organization's security posture and connect with insurance partners to obtain exclusive cyber insurance coverage and personalized pricing.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/products/secops-color.svg)
                                      Detect, investigate, and respond to cyber threats with SIEM and SOAR technology. Extract signals to find threats and automate the response.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/products/threat-intelligence-color.svg)
                                      Know who's targeting your organization with unparalleled visibility into the global threat landscape.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/products/model-armor-color.svg)
                                      Enhance AI security and safety by screening LLM prompts and responses.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/products/security-command-center-color.svg)
                                      Understand your security and data attack surface.

Provide unified, federated identity with least privilege policies to reduce the risk of data breaches and other security incidents.

     ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/security-and-identity-color.svg)
                                      Allow organization administrators to define fine-grained, attribute-based access control for projects and resources in Google Cloud.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/security-and-identity-color.svg)
                                      Simplify, automate, and customize the deployment, management, and security of private certificate authorities (CA).
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/security-and-identity-color.svg)
                                      Establish fine-grained identity and access management for Google Cloud resources.

                                      Identify excess permissions using policy insights.

                                      Plan your design for granting the right individuals access to the right resources for the right reasons.
                                      Study fundamental features of cloud security related to access management and identity.
                                      Plan your approach with Architecture Center resources across a variety of identity and access management topics.

Protect your workloads against denial-of-service attacks, web application attacks, and other security threats.

     ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/security-and-identity-color.svg)
                                      Deploy only trusted containers on Google Kubernetes Engine.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/security-and-identity-color.svg)
                                      Acquire and manage TLS (SSL) certificates for use with Cloud Load Balancing and Media CDN.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/security-and-identity-color.svg)
                                      Manage access to applications running in App Engine standard environment, App Engine flexible environment, Compute Engine, and GKE.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/security-and-identity-color.svg)
                                      Protect your organization's website from fraudulent activity, spam, and abuse.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/networking-color.svg)
                                      Migrate to Google Cloud while keeping your organization's existing security policies and requirements for outbound web traffic.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/security-and-identity-color.svg)
                                      Detect malicious URLs on your organization's website and in client applications.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/networking-color.svg)
                                      Help protect your services against DoS and web attacks.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/networking-color.svg)
                                      Scale and distribute app access with high-performance load balancing.

                                      Follow guidance to install and run the sample app to detect malicious URLs in a Go environment.

Collect, store, analyze, and monitor your organization's aggregated platform and system logs with a comprehensive solution.

     ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/security-and-identity-color.svg)
                                      Get visibility over your organization's cloud provider through near real-time logs.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/security-and-identity-color.svg)
                                      Provides assessments about a project or folder's adherence to compliance requirements.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/observability-color.svg)
                                      Gain visibility into who did what, when, and where for all user activity on Google Cloud.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/security-and-identity-color.svg)
                                      Use this group of products for progressively greater transparency and control over access to your content stored in Google Cloud.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/security-and-identity-color.svg)
                                      Create an inventory of devices running Chrome OS and Chrome Browser that access your organization's data.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/operations-color.svg)
                                      Identify Google Cloud service disruptions relevant to your projects so you can manage and respond to them efficiently.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/security-and-identity-color.svg)
                                      Manage planned maintenance across Google Cloud services.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/observability-color.svg)
                                      Store, search, analyze, monitor, and alert on log data and events from Google Cloud and AWS.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/observability-color.svg)
                                      Get visibility into the performance, availability, and overall health of cloud-powered applications.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/networking-color.svg)
                                      Use a single console for comprehensive network monitoring, verification, and optimization.

Manage your resources in a secure and compliant way with visibility and control over your cloud environment.

     ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/security-and-identity-color.svg)
                                      Secure your workloads and accelerate your path to running compliant workloads on Google Cloud.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/security-and-identity-color.svg)
                                      View, monitor, and analyze Google Cloud and Anthos assets across projects and services.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/security-and-identity-color.svg)
                                      Centralized and programmatic control over your organization's cloud resources.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/security-and-identity-color.svg)
                                      Control resources and manage access through policies to proactively improve your security configuration.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/security-and-identity-color.svg)
                                      Centralized and programmatic control over your organization's cloud resources.

                                      Reduce security risk and gain access to exclusive cyber insurance policies tailored for Google Cloud customers.

Handle key management for secrets, disks, images, and log retention.

     ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/devops-color.svg)
                                      Use key management for secrets, disks, images, and log retention.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/security-and-identity-color.svg)
                                      Control the location and distribution of your externally-managed keys.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/security-and-identity-color.svg)
                                      Protect cryptographic keys with a fully managed hardware security module service.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/security-and-identity-color.svg)
                                      Manage encryption keys on Google Cloud.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/security-and-identity-color.svg)
                                      Protect data in-use with Confidential VM, Confidential GKE, Confidential Dataflow, Confidential Dataproc, and Confidential Space.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/security-and-identity-color.svg)
                                      Store API keys, passwords, certificates, and other sensitive data.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/security-and-identity-color.svg)
                                      Discover and redact sensitive data.

                                      Discover and understand your data using a fully managed and scalable data discovery and metadata management service. (Deprecated)

Centrally manage network resources, establish scalable segmentation for different security zones, and detect network threats.

     ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/security-and-identity-color.svg)
                                      Use a zero-trust solution that enables secure access with integrated threat and data protection.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/security-and-identity-color.svg)
                                      Manage the wireless communications of devices transmitting in the Citizens Broadband Radio Spectrum (CBRS) band.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/networking-color.svg)
                                      Help protect your services against DoS and web attacks.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/networking-color.svg)
                                      Implement advanced protection capabilities and pervasive coverage to protect your Google Cloud workloads from internal and external attacks.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/security-and-identity-color.svg)
                                      Use identity and context to guard access to your applications and VMs.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/networking-color.svg)
                                      Connect your infrastructure to Google Cloud on your terms, from anywhere.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/networking-color.svg)
                                      Get alerts when Cloud Intrusion Detection System detects malicious activity.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/networking-color.svg)
                                      Connect your infrastructure to Google Cloud on your terms, from anywhere.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/networking-color.svg)
                                      Protect sensitive data in Google Cloud services using security perimeters.

                                      Get help with secrets and Cloud KMS keys.

                                      Get recommendations for which Assured Workload control package to use.

                                      View certifications, documentation, and third-party audits to help support your compliance.

                                      Discover how we protect the privacy of Google Cloud and Google Workspace customers.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/security-and-identity-color.svg)
                                      Secure your workloads and accelerate your path to running compliant workloads.

                                      View answers to frequently asked questions about Google Cloud policy violations.
                                      View a list of services that can be configured for data location.        ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/security-and-identity-color.svg)
                                      Meet digital sovereignty requirements for Google Cloud by Partners.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/security-and-identity-color.svg)
                                      Meet digital sovereignty requirements for Google Cloud by T-Systems.
                                              ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/devops-color.svg)
                                      Use a modular set of Google Cloud products to protect your software supply chain.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/devops-color.svg)
                                      Store, manage, and secure container images and language packages.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/devops-color.svg)
                                      Provide software composition analysis, metadata storage and retrieval.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/security-and-identity-color.svg)
                                      Provide enterprise users of open source software with trusted OSS packages.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/devops-color.svg)
                                      Continuously build, test, and deploy containers using the Google Cloud infrastructure.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/security-and-identity-color.svg)
                                      Deploy only trusted containers on Google Kubernetes Engine.

                                      Basics of authentication methods and concepts for Google Cloud services and get help with implementation or troubleshooting.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/developer-tools-color.svg)
                                      Manage user identities, devices, and applications from one console.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/security-and-identity-color.svg)
                                      Add Google-grade identity and access management to your apps.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/security-and-identity-color.svg)
                                      Use a highly available, hardened service running Microsoft Active Directory (AD).
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/security-and-identity-color.svg)
                                      Provides phishing-resistant 2nd factor of authentication for high-value users.
                                      Study fundamental features of cloud security related to access management and identity.           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/operations-color.svg)
                                      A managed backup and disaster recovery (DR) service for centralized and application-consistent data protection in Google Cloud.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/business-intelligence-color.svg)
                                      Increase anti money laundering detection accuracy and efficiency.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/networking-color.svg)
                                      Optimize connectivity between systems on the internet and your Google Cloud instances.

                                      Evaluate your organization's security posture and connect with insurance partners to obtain exclusive cyber insurance coverage and personalized pricing.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/compute-color.svg)
                                      VMs on Google Cloud hardened by a set of security controls that help defend against rootkits and bootkits.

---

# Keyboard shortcuts for Google CloudStay organized with collectionsSave and categorize content based on your preferences.

> Get an overview of Google Cloud keyboard shortcuts.

# Keyboard shortcuts for Google CloudStay organized with collectionsSave and categorize content based on your preferences.

The following table contains the universal shortcuts for Google Cloud console.

| Action | Keyboard shortcut |
| --- | --- |
| Open shortcut help | ?orControl+Shift+/(Command+Shift+/on macOS) |
| Open navigation menu | . |
| Go up one page | U |
| Open project navigator | Control+O(Command+Oon macOS) |
| Find products and services | / |
| Send feedback | @ |
| Open help menu | GthenH |
| Open notifications panel | GthenN |
| Activate Cloud Shell | GthenS |
| Jump to and from popup notification (if one is showing) | Control+F6(Command+F6on macOS) |
| Open or close Gemini AI chat | Alt+G(Option+Gon macOS) |

## Change or disable keyboard shortcuts

To change or disable keyboard shortcuts in the Google Cloud console, complete
the following instructions:

1. Open the [Google Cloud console](https://console.cloud.google.com/).
2. Open the keyboard shortcuts dialog by pressing ? or
  Control+Shift+/ (Command+Shift+/ on macOS).
  Alternatively, click  **Support**, and then click **Configure keyboard shortcuts**.
3. To disable a shortcut, clear its checkbox. To change it, click
  **Edit shortcut**, and then enter a new shortcut.
4. When done, click **Save**.

When changing keyboard shortcuts, keep the following things in mind:

- Your replacement shortcut must be a combination of Control or
  Shift with a printable key.
- You can't have the same shortcut assigned to multiple actions.
- To return to the original keyboard shortcuts, click **Restore all defaults**
  in the keyboard shortcuts dialog.

## View contextual keyboard shortcuts

You can open an overlay that displays contextual keyboard shortcuts based on
what's on the screen, or which UI element is focused such as code editors,
tables, and menu bars.

To show the overlay in the Google Cloud console, complete the following
instructions:

1. Open the [Google Cloud console](https://console.cloud.google.com/).
2. Open the keyboard shortcuts dialog by pressing ? or
  Control+Shift+/ (Command+Shift+/ on macOS).
  Alternatively, click  **Support**, and then click **Configure keyboard shortcuts**.
3. Select **Show the shortcuts helper**, and then click **Save**.

   Was this helpful?

---

# Storage

> Documentation and resources for Google Cloud data storage products, including transfer, backup, and disaster recovery solutions.

[Get started for free](https://console.cloud.google.com/freetrial)

#### Start your proof of concept with $300 in free credit

- Develop with our latest Generative AI models and tools.
- Get free usage of 20+ popular products, including Compute Engine and AI APIs.
- No automatic charges, no commitment.

       [View free product offers](https://cloud.google.com/free/docs/free-cloud-features#free-tier)

#### Keep exploring with 20+ always-free products.

Access 20+ free products for common use cases, including AI APIs, VMs, data warehouses,
          and more.

                        Learn about Cloud Storage, including how it works and what tools you can use to store your data.

                        Learn about Filestore as a network-attached file storage option.

                        Back up and recover your data resources.

                        Get fully-managed volume provisioning for your file-based applications.

                        Learn the storage options that GKE supports and considerations for selecting the best option for your needs.

                        Learn the storage options that Compute Engine supports and considerations for selecting the best option for your needs.

                        Learn about how NetApp Volumes provides high-performance file storage for demanding enterprise applications and workloads.
                        View an example of how Filestore integration with GKE can significantly accelerate your AI/ML workload performance.
                        Study creating, performing basics tasks, and managing object retention with Cloud Storage.
                        Study using the gcloud CLI command-line tool, APIs, and the APIs Explorer tool with Cloud Storage.
                        Study how to store, protect, and govern your data.
                        View a decision tree to choose storage options to meet your workload needs.

Create and execute backup plans for databases, VMs, and file systems to protect all of your data resources consistently and efficiently.

     ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/operations-color.svg)
                                      A managed backup and disaster recovery (DR) service for centralized and application-consistent data protection.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/products/kubernetes-engine-color.svg)
                                      Protect, manage, and restore your containerized applications and data for workloads running on GKE clusters.

                                      Create and execute backup plans for your VMware VMs.

                                      Create and execute backup plans for your Microsoft SQL Server databases.

                                      Create and execute backup plans for your Compute Engine instances.

                                      Create and execute backup plans for your SAP HANA databases in Compute Engine instances.

                                      Review and report on the backup status of your data resources.

Choose your block, file, or object storage options.

     ![](https://cloud.google.com/_static/clouddocs/images/icons/products/storage-color.svg)
                                      Store objects with global edge caching.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/storage-color.svg)
                                      Create fully managed, high-performance NFS file servers on Google Cloud.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/storage-color.svg)
                                      A fully managed, cloud-based data storage service that provides advanced data management capabilities and highly scalable performance.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/storage-color.svg)
                                      A high-performance, fully managed parallel file system optimized for AI and HPC applications.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/storage-color.svg)
                                      Persistent Disk volumes are durable network storage devices that your VMs can access like physical disks in a desktop or a server.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/storage-color.svg)
                                      A scalable, high-performance storage service with a comprehensive suite of data persistence and management capabilities.

Transfer your data into, within, or from Google Cloud.

     ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/storage-color.svg)
                                      Transfer data between Cloud Storage services such as AWS S3 and Cloud Storage.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/migration-color.svg)
                                      Ship large volumes of data to Google Cloud using rackable storage.
                                               ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/storage-color.svg)
                                      Optimize share usage within your Filestore instances.

                                      Transfer your data from S3 or Azure into Cloud Storage.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/products/kubernetes-engine-color.svg)
                                      A service for backing up and restoring workloads in GKE clusters.

                                      Store, process, and secure large amounts of structured, semistructured, and unstructured data in its native format and process any variety of it.        ![](https://cloud.google.com/_static/clouddocs/images/icons/products/storage-color.svg)
                                      Use a powerful, simple, and cost-effective object storage service built for Google scale.
                                      Generate inventory reports containing metadata information about your objects.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/storage-color.svg)
                                      Store, share, and collaborate on files and folders from your mobile device, tablet, or computer.

                                      Plan and evaluate the features, design options, and relative advantages of block storage, file storage, and object storage services.
                                      Plan using content resources across a wide variety of storage subjects.             Was this helpful?

---

# Terraform on Google Cloud documentation

> Using Terraform with Google Cloud.

# Terraform on Google Cloud documentation

  [Read product documentation](https://docs.cloud.google.com/docs/terraform/terraform-overview)

Learn how to use Terraform to reliably provision infrastructure on Google Cloud.
  [Learn more](https://cloud.google.com/docs/terraform/terraform-overview)

    Start building and deploying on Google Cloud with a
    [free trial](https://console.cloud.google.com/freetrial).
                    [Get started for free](https://console.cloud.google.com/freetrial)

#### Start your proof of concept with $300 in free credit

- Develop with our latest Generative AI models and tools.
- Get free usage of 20+ popular products, including Compute Engine and AI APIs.
- No automatic charges, no commitment.

       [View free product offers](https://cloud.google.com/free/docs/free-cloud-features#free-tier)

#### Keep exploring with 20+ always-free products.

Access 20+ free products for common use cases, including AI APIs, VMs, data warehouses,
          and more.

- Quickstart
  [Create a VM instance using Terraform](https://cloud.google.com/docs/terraform/create-vm-instance)
- Reference
  [Basic Terraform commands](https://cloud.google.com/docs/terraform/basic-commands)
- Tutorial
  [Store Terraform state](https://cloud.google.com/docs/terraform/resource-management/store-state)
- Tutorial
  [HashiCorp tutorials](https://learn.hashicorp.com/collections/terraform/gcp-get-started)
- Reference
  [Google Cloud provider](https://registry.terraform.io/providers/hashicorp/google/latest/docs)

- Best practice
  [Terraform best practices](https://cloud.google.com/docs/terraform/best-practices-for-terraform)
- Conceptual guide
  [Understanding APIs and Terraform](https://cloud.google.com/docs/terraform/understanding-apis-and-terraform)
- Tutorial
  [Manage infrastructure as code](https://cloud.google.com/architecture/managing-infrastructure-as-code)
- Tutorial
  [Deploy a basic Flask web server by using Terraform](https://cloud.google.com/docs/terraform/deploy-flask-web-server)
- Reference
  [Get support for Terraform issues](https://cloud.google.com/docs/terraform/getting-support)

- Tutorial
  [Export resources into Terraform](https://cloud.google.com/docs/terraform/resource-management/export)
- Tutorial
  [Import resources into Terraform state](https://cloud.google.com/docs/terraform/resource-management/import)
- Tutorial
  [Create a configuration with Service Catalog](https://cloud.google.com/service-catalog/docs/terraform-configuration)
- Technical
  [Use policy validation](https://cloud.google.com/docs/terraform/policy-validation)

      Training

   Training and tutorials

In this lab, you install Terraform and create a VM instance using Terraform.

      Training

   Training and tutorials

In this lab, you write infrastructure as code with Terraform.

      Training

   Training and tutorials

In this lab, you learn how to describe and launch cloud resources with Terraform.

      Training

   Training and tutorials

In this lab, you learn how to store Terraform state in Google Cloud Storage.

      Training

   Training and tutorials

In this lab, you learn how modules can address problems of code complexity, duplication, and reuse.

      Training

   Training and tutorials

In this lab, you learn how to enforce policies on Terraform configurations.

                 Was this helpful?
