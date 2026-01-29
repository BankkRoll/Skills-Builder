# Committed use discountsStay organized with collectionsSave and categorize content based on your preferences. and more

# Committed use discountsStay organized with collectionsSave and categorize content based on your preferences.

> Get an overview of Google Cloud committed use discounts.

# Committed use discountsStay organized with collectionsSave and categorize content based on your preferences.

This document provides information about committed use discounts (CUDs) for
Google Cloud and how they apply for various services.

CUDs provide discounted prices for eligible Google Cloud resources in
exchange for purchasing committed use contracts (also known as commitments).
When you purchase Google Cloud commitments, you commit to either using a
minimum level of resources or spending a minimum amount, for a term duration of
one or three years.

CUDs for Google Cloud are broadly available as spend-based or
resource-based CUDs and cover a wide range of services and resources.
You can choose the type of commitment that you want to purchase depending on
the service that you use and whether you have predictable or unpredictable
resource needs.

## Spend-based commitments

Spend-based CUDs provide a discount in exchange for your commitment to spend a
minimum amount for any of the services listed in this section. The discount
applies to the set of eligible resources for each service.

With spend-based commitments, you commit to spending a specified minimum hourly
amount on eligible resources or services throughout the commitment's term of one
or three years. In return, you receive those resources and services at
discounted rates. You keep receiving discounted rates until your hourly
spend on those eligible resources and services meets your hourly committed spend
amount. Any overage usage that takes your hourly spend amount over your
committed amount is charged at the on-demand rate.

Spend-based CUDs apply to eligible usage in any projects that the
Cloud Billing account pays for.

Depending on the Google Cloud service that you use, you can purchase
spend-based commitments in one of the following ways:

- Compute flexible commitments
- Service-specific spend-based commitments

### Compute flexible commitments

Compute flexible commitments are ideal for scenarios where you have predictable
Google Cloud spend needs that span usage beyond a single service. Compute
Flexible CUDs apply to your spend across one or more of the following services:

- Compute Engine
- Google Kubernetes Engine
- Cloud Run

You can purchase a single flexible commitment to cover your eligible spend
across all three services. For more information about how Compute flexible CUDs
apply to each service, see the service-specific CUDs documentation:

- [CUDs documentation for Compute Engine](https://cloud.google.com/compute/docs/instances/committed-use-discounts-overview)
- [CUDs documentation for GKE](https://cloud.google.com/kubernetes-engine/cud)
- [CUDs documentation for Cloud Run](https://cloud.google.com/run/cud)

### Service-specific spend-based commitments

These commitments are ideal for scenarios where you have predictable spend needs
within a Google Cloud service. You must purchase these commitments
separately for each Google Cloud service and CUDs from these commitments
apply only to spend within that service. You can get spend-based CUDs for the
following Google Cloud services:

- [AlloyDB for PostgreSQL](#alloydb_cuds)
- [Backup and DR Service](#backupdr_cuds)
- [Backup for GKE](#backup_gke_cuds)
- [BigQuery](#bigquery_cuds)
- [Bigtable](#bigtable_cuds)
- [Dataflow](#dataflow_cuds)
- [Firestore](#firestore_cuds)
- [Spanner](#spanner_cuds)
- [Cloud SQL](#sql_cuds)
- [Google Cloud Managed Service for Apache Kafka](#kafka_cuds)
- [Google Cloud NetApp Volumes](#netapp_cuds)
- [Google Cloud VMware Engine](#vmware_cuds)
- [Google Kubernetes Engine (Autopilot)](#gke_cuds)
- [Memorystore](#memorystore_cuds)

#### AlloyDB for PostgreSQL

AlloyDB for PostgreSQL committed use discounts are spend-based CUDs that apply
to all AlloyDB for PostgreSQL instance vCPU and memory usage. The discount
applies to AlloyDB for PostgreSQL instances in any project or region that is
associated with a single Cloud Billing account.

AlloyDB for PostgreSQL commitments *don't apply* to storage, backup, and network
egress.

For current rates, see [AlloyDB for PostgreSQL pricing](https://cloud.google.com/alloydb/pricing#cpu-mem-pricing).

#### Backup and DR Service

[Backup and DR (for VMware Engine) committed use discounts](https://cloud.google.com/backup-disaster-recovery/docs/configuration/cud)
apply to the combined node usage in a region. This gives you low, predictable
costs, without the need to make any manual changes or updates yourself. They
apply to VMware Engine backups in the regions where the service
is available and to which you have committed.

[Backup and DR (for protecting Oracle databases into a backup vault) committed
use discounts](https://cloud.google.com/backup-disaster-recovery/docs/configuration/cud) apply to
aggregate Oracle database protection into backup vault usage. This gives you
low, predictable costs, without the need to make any manual changes or updates
yourself. This flexibility saves you time and helps you to save more by
achieving high utilization rates across your commitments.

For current rates, see [Backup and DR pricing](https://cloud.google.com/backup-disaster-recovery/pricing).

#### Backup for GKE

[Backup for GKE committed use discounts](https://cloud.google.com/kubernetes-engine/docs/add-on/backup-for-gke/cud)
are spend-based CUDs that apply to Backup for GKE backup management, that
is Pods per plan in a region. Committed use discounts don't apply to backup
storage (GiB) or inter-region data transfer (GiB).

For current rates, see [Backup for GKE CUDs pricing](https://cloud.google.com/kubernetes-engine/pricing#backup-for-gke).

#### BigQuery

[BigQuery CUDs](https://cloud.google.com/bigquery/docs/bigquery-cud) provide discounted
prices in exchange for your commitment to use BigQuery PAYG
compute capacity for a one- or three-year term, with the commitment fee billed
monthly. BigQuery CUDs apply to all compute types.

For current rates, see [BigQuery pricing](https://cloud.google.com/bigquery/pricing).

#### Bigtable

As a Bigtable customer, you can purchase a commitment to receive a
committed use discount on the price of Bigtable nodes. The
discount applies to nodes in any project or region that is associated with a
single Cloud Billing account. The discount does not apply to the cost of
storage, backup storage, or network egress. For details, see [Bigtable committed use
discounts](https://cloud.google.com/bigtable/docs/cuds). For current rates, see [Bigtable pricing](https://cloud.google.com/bigtable/pricing).

#### Cloud Run

[Cloud Run committed use discounts](https://cloud.google.com/run/cud)
apply to all aggregated
Cloud Run CPU, memory, and request usage in a region, giving you
low, predictable costs when your code is running in one of the supported
container ecosystems. Cloud Run commitments *don't apply* to
networking changes.

For current rates, see the
[Cloud Run pricing details](https://cloud.google.com/run/pricing#tables).

#### Dataflow

[Dataflow committed use discounts](https://cloud.google.com/dataflow/docs/cuds) apply to your
spending on the Dataflow compute capacity used by streaming jobs across
projects. The discount applies to any eligible usage in Dataflow
projects associated with the Cloud Billing account used to purchase the
commitment, regardless of instance configuration or region. All CUDs apply to
both regional and multi-region configurations.

The discount doesn't apply to the cost of worker CPU and memory for batch and
FlexRS jobs, Dataflow Shuffle data processed, Data Compute Units (DCUs)
for batch jobs, Persistent Disk storage, GPUs, snapshots, and confidential VMs.

For current rates and other details, see
[Dataflow pricing](https://cloud.google.com/dataflow/pricing).

#### Firestore

As a Firestore customer, you can purchase a commitment to receive a
committed use discount on the price of Firestore
Read/Write/Delete operations. The discount applies to Read/Write/Delete
operations in any project or region that is associated with a single
Cloud Billing account. The discount doesn't apply to any other
Firestore resource. For details, see
[Firestore committed use discounts](https://cloud.google.com/firestore/docs/cuds).

For current rates, see
[Firestore pricing](https://cloud.google.com/firestore/pricing).

#### Spanner

[Spanner committed use discounts](https://cloud.google.com/spanner/docs/cuds) apply to
all Spanner compute capacity associated with a single
Cloud Billing account, regardless of region. This includes all
instances in all projects, whether configured as single-region or
multi-region instances.

Spanner CUDs *don't apply* to Spanner storage, backup,
or network egress.

For current rates and other details, see [Spanner
pricing](https://cloud.google.com/spanner/pricing).

#### Cloud SQL

[Cloud SQL committed use discounts](https://cloud.google.com/sql/cud)
provide you the flexibility to use
any machine shapes with the supported Cloud SQL database engines,
without having to modify your commitments. They
apply to all Cloud SQL database instance vCPU
and memory usage for the service in the region you purchased the
commitments, *except* shared CPU machine types (such as db-f1-micro and
db-g1-small). The commitments apply to usage from all supported database
engines, such as MySQL, PostgreSQL, and SQL Server.

Cloud SQL commitments *don't apply* to persistent disk snapshots,
storage, IP addresses, network egress, or licensing.

For current rates, see
[Cloud SQL pricing](https://cloud.google.com/sql/pricing).

#### Google Cloud Managed Service for Apache Kafka

[Managed Service for Apache Kafka committed use discounts (CUDs)](https://cloud.google.com/managed-service-for-apache-kafka/docs/cuds)
are discounts that apply to the Kafka compute (vCPU and RAM) costs for running
Managed Service for Apache Kafka clusters across projects. You can apply
the CUDs to any Managed Service for Apache Kafka project that is
associated with the Cloud Billing account used to purchase the commitment.
You can apply CUDs to any available region. You cannot apply the
Managed Service for Apache Kafka CUDs to the cost of storage, networking or
Private Service Connect.

For current rates and other details, see [Managed Service for Apache Kafka
pricing](https://cloud.google.com/managed-service-for-apache-kafka/pricing).

#### Google Cloud NetApp Volumes

[Google Cloud NetApp Volumes committed use discounts](https://cloud.google.com/netapp/volumes/docs/cuds)
apply to the aggregate storage capacity on Flex, Standard, Premium, and Extreme
service levels and regions at your billing account level. CUDs can keep your
storage costs low when you have predictable storage needs.
NetApp Volumes CUDs are'nt available for volume replications and
backups.

For current rates, see [NetApp Volumes pricing](https://cloud.google.com/netapp/volumes/pricing).

#### Google Cloud VMware Engine

[VMware Engine committed use discounts](https://cloud.google.com/vmware-engine/docs/cud)
apply to aggregate
VMware Engine node usage in a region, giving you low,
predictable costs, without the need to make any manual changes or updates
yourself. They apply to VMware Engine node CPU and memory
usage in the regions where the service is available and you have committed.

Current rates and supported regions for Google Cloud VMware Engine
CUDs are detailed on the
[VMware Engine pricing page](https://cloud.google.com/vmware-engine/pricing).

#### Google Kubernetes Engine

[Google Kubernetes Engine (Autopilot Mode) committed use discounts](https://cloud.google.com/kubernetes-engine/cud)
apply to all Autopilot Pod workload vCPU, memory, and ephemeral storage
usage in the region in which you have purchased commitments. Google Kubernetes Engine
(Autopilot Mode) CUDs don't apply to the cluster management fee or to
GKE Standard mode compute nodes.

For current rates, see the [Google Kubernetes Engine pricing details](https://cloud.google.com/kubernetes-engine/pricing#autopilot_mode).

#### Memorystore

Memorystore CUDs apply to Memorystore for Valkey, Memorystore for Redis Cluster,
Memorystore for Redis, and Memorystore for Memcached usage. A Memorystore
CUD gives you the flexibility to use Valkey, Redis Cluster, Redis, or
Memcached instance spending toward a commitment on a single Cloud Billing
account.

Memorystore commitments *don't apply* to Cloud Storage
storage for backups, persistence, network egress, or Memorystore for Redis M1
capacity tier instances (less than 5 GB).

For current rates, see the following pages:

- [Memorystore for Valkey committed use discounts](https://cloud.google.com/memorystore/docs/valkey/cuds)
- [Memorystore for Redis Cluster committed use discounts](https://cloud.google.com/memorystore/docs/cluster/cuds)
- [Memorystore for Redis committed use discounts](https://cloud.google.com/memorystore/docs/redis/cuds)
- [Memorystore for Memcached committed use discounts](https://cloud.google.com/memorystore/docs/memcached/cuds)

## Resource-based commitments

Resource-based CUDs are available only for Compute Engine.
[Compute Engine resource-based CUDs](https://cloud.google.com/compute/docs/instances/signing-up-committed-use-discounts) provide discounts
in exchange for committing to using a minimum amount of Compute Engine
resources in a specific region and a project. These CUDs are ideal when you
have predictable resource needs. You can purchase Compute Engine
resource-based commitments for the following hardware and software resources
for a term duration of one or three years:

- vCPUs
- Memory
- GPUs
- Local SSD disks
- Sole-tenant nodes
- Operating system (OS) licenses

Commitments for hardware resources are separate from the ones for OS licenses.
You can purchase both categories of commitments for the same virtual machine
(VM) instance, but you cannot purchase a single commitment that covers both
hardware resources and licenses.

For current rates, see
[VM instance pricing](https://cloud.google.com/compute/vm-instance-pricing#general-purpose_machine_type_family).

## Spend-based versus resource-based commitments

The following table demonstrates the differences between
[spend-based](#spend_based_commitments)
and [resource-based](#resource_based_commitments)
CUDs, using Compute Engine as the example service.

| Spend-based CUDs | Resource-based CUDs |
| --- | --- |
| Spend-basedcommitments for Compute Engine
      are purchased and measured in terms of the dollars per hour of equivalent
      discount spend. | Resource-basedcommitments for Compute Engine
      are purchased and measured in terms of the underlying vCPU, memory,
      GPU, and Local SSD disk resources. |
| Spend-basedcommitments are purchased from your
      Cloud Billing account; they apply to eligible usage in any
      projects paid for by that Cloud Billing account. | Resource-basedcommitments
        are purchased in the context of an individual project, rather than that
        of a Cloud Billing account.You can enablediscount sharingso that Compute Engine resource-based CUDs are shared
      across all projects that are paid for by the same Cloud Billing
      account.You can change the
      Cloud Billing account that pays for the project
      where you purchased the resource-based commitments.Learn about changing the Cloud Billing account for projects. |

## CUDs summary

The following table summarizes the differences between resource-based CUDs and
spend-based CUDs.

|  | Resource-based CUDs | Spend-based CUDs |
| --- | --- | --- |
| Products covered | Compute Engine | Compute Flexible CUDsCloud RunCompute EngineGoogle Kubernetes EngineService-specific spend-based commitmentsAlloyDB for PostgreSQLBackup and DR ServiceBackup for GKEBigtableCloud RunCloud SQLDataflowFirestoreGoogle Cloud NetApp VolumesGoogle Cloud VMware EngineGoogle Kubernetes Engine (Autopilot)MemorystoreSpanner |
| Purchase unit | Resource-based (available for vCPUs, memory, Local SSD disks and GPUs).You commit to purchasing a minimum amount of eligible resources. | Spend-based (for example, $100/hour).You commit to spending a minimum dollar amount per hour of equivalent discount spend on eligible services. |
| Scope | These CUDs apply to a specific project by default, but you canshare themacross all projects linked to the same billing account. | You can buy spend-based commitments measured in dollars per hour of equivalent discount spend. You buy these commitments at the billing account level and they apply to eligible usage in any project linked to that billing account, across all regions. |
| Discount of on-demand rate | Compute Engine | Pricing for CUDs is unique for each Google Cloud product:AlloyDB for PostgreSQLBackup and DR ServiceBackup for GKEBigtableCloud RunCloud SQLCompute EngineDataflowFirestoreGoogle Cloud NetApp VolumesGoogle Cloud VMware EngineGoogle Kubernetes Engine (Autopilot)MemorystoreSpanner |
| Regional eligibility | Applies to a specific region. | Depending on the service, CUDs can apply to a specific region or all regions. |
| Attribution | Supports proportional and prioritized attribution. | Supports proportional attribution only. |

## View your commitments and discounts

To view your spend-based and resource-based CUDs in the dashboard, complete the
following steps:

1. In the Google Cloud console, open the **Committed use discounts (CUDs)**
  page for **Billing**.
  [Go to Committed use discounts (CUDs)](https://console.cloud.google.com/billing/reports/commitments)
2. At the prompt, choose the Cloud Billing account for which you want
  to view commitments.

The **Committed use discounts (CUDs)** dashboard displays a list of all the
commitments, across services, that are associated with your Cloud Billing
account. You can view which of your commitments are expiring in the next 30 days.
You can also specify your *resource-based* commitments to automatically renew
at the end of their ongoing terms by changing the setting in the **Auto-renew**
column.

For information about viewing *spend-based* CUDs, see
[Viewing spend-based commitments](https://cloud.google.com/billing/docs/how-to/cuds-list-overview).

For information about viewing *resource-based* CUDs, see
[Viewing resource-based commitments](https://cloud.google.com/compute/docs/instances/signing-up-committed-use-discounts#console_3).

## Pricing for commitments

You are billed a monthly fee for the commitments you purchase. This fee is
calculated when you purchase the commitments, based on the list
price on the date you made the purchase. This monthly fee applies
to your purchased commitments for the entire duration of the commitment period.
Future changes to the list prices don't affect your commitment fee during
the commitment period.

To understand how your commitment fees and credits are applied to your
Cloud Billing account and projects, see
[Attribution of committed use discount fees and credits](https://cloud.google.com/docs/cuds-attribution).

Pricing for CUDs is unique for each Google Cloud
product:

- [Backup and DR Service](https://cloud.google.com/backup-disaster-recovery/docs/configuration/cud#cud_pricing)
- [Backup for GKE](https://cloud.google.com/kubernetes-engine/pricing#backup-for-gke)
- [Bigtable CUD pricing](https://cloud.google.com/bigtable/docs/cuds#pricing)
- [Cloud Run pricing details](https://cloud.google.com/run/pricing#tables)
- [Cloud SQL pricing](https://cloud.google.com/sql/pricing/)
- [Firestore CUD pricing](https://cloud.google.com/firestore/docs/cuds#pricing)
- [Spanner CUD pricing](https://cloud.google.com/spanner/docs/cuds#pricing)
- [Compute Engine pricing](https://cloud.google.com/compute/vm-instance-pricing#committed_use)
- [Google Cloud VMware Engine pricing](https://cloud.google.com/vmware-engine/pricing/)
- [Google Kubernetes Engine (Autopilot Mode) pricing details](https://cloud.google.com/kubernetes-engine/pricing#autopilot_mode)
- [Memorystore for Memcached CUD pricing](https://cloud.google.com/memorystore/docs/memcached/cuds#pricing)
- [Memorystore for Redis CUD pricing](https://cloud.google.com/memorystore/docs/redis/cuds#pricing)

## Purchase commitments

To purchase *spend-based* commitments, see
[Purchasing spend-based commitments](https://cloud.google.com/docs/cuds-spend-based#purchasing).

To purchase *resource-based* commitments for Compute Engine,
see one of the following, depending on your use case:

- [Purchase commitments without attached reservations](https://cloud.google.com/compute/docs/instances/signing-up-committed-use-discounts#purchasecommitment)
- [Purchase commitments with attached reservations](https://cloud.google.com/compute/docs/instances/signing-up-committed-use-discounts#purchasecommitmentgpuslocalssd)
- [Purchase commitments for software licenses](https://cloud.google.com/compute/docs/instances/signing-up-committed-use-discounts#purchaselicensecommitment)

## Related topics

- Learn about [spend-based CUDs program improvements](https://cloud.google.com/docs/cuds-multiprice).
- Learn how to
  [purchase spend-based CUDs](https://cloud.google.com/docs/cuds-spend-based#purchasing).
- Learn more about
  [resource-based CUDs for Compute Engine](https://cloud.google.com/compute/docs/instances/signing-up-committed-use-discounts).
- Learn how to
  [view your CUDs reports](https://cloud.google.com/billing/docs/how-to/cud-analysis).
- Learn how to
  [view your Cloud Billing reports and cost trends](https://cloud.google.com/billing/docs/how-to/reports#credits).
- [Understand your savings with cost breakdown reports](https://cloud.google.com/billing/docs/how-to/cost-breakdown).
- Learn how to
  [export Cloud Billing data to BigQuery](https://cloud.google.com/billing/docs/how-to/export-data-bigquery).
- Learn how to
  [view your cost and payment history](https://cloud.google.com/billing/docs/how-to/view-history).

   Was this helpful?

---

# Dammam region accessStay organized with collectionsSave and categorize content based on your preferences.

# Dammam region accessStay organized with collectionsSave and categorize content based on your preferences.

This document provides information about region-specific access controls and how
to purchase Google Cloud resources in the Dammam, Kingdom of Saudi Arabia (KSA)
region for the following customers:

- KSA-based customers
- non-KSA-based customers

## KSA-based customers

Google Cloud is partnering with
[CNTXT](https://cntxt.com/products/google-cloud-solutions/), our exclusive reseller in the region, to bring
Google Cloud to the Kingdom of Saudi Arabia. If you have a KSA billing address,
you are required to purchase Google Cloud services for the Dammam
`me-central2` region or any other Google Cloud region through CNTXT.
Be aware of the following sales and regional access paths:

- Access to Google Cloud services from the (`me-central2`) Dammam
   region is available only to KSA-based customers that have signed up to
   purchase cloud services through CNTXT.
- KSA-based customers requiring technical support must reach out to CNTXT to
   explore the available options. You can't directly purchase Google Customer
   Care offerings.
- If you are interested in setting up [Invoiced Billing](https://cloud.google.com/billing/docs/how-to/invoiced-billing)
   through CNTXT, contact [CNTXT directly](https://cntxt.com/products/google-cloud-solutions/#book-a-meeting).

If you are an existing Google Cloud customer with a KSA billing address, then
regardless of which Google Cloud data center regions you use, you are required
to migrate your current billing account to CNTXT. You will receive a
notification from Google with additional information on how and when to migrate
your billing account to CNTXT.

## Non-KSA-based customers

If your billing address is outside of the KSA, you can continue to purchase
Google Cloud services directly from Google or any authorized Google Cloud
partner. Access to the Dammam region is limited to customers that are set up
for [Invoiced Billing](https://cloud.google.com/billing/docs/how-to/invoiced-billing).

If you pay for Google Cloud services with a credit card you must sign up for
Invoiced Billing in order to access the Dammam region.

## Assured Workloads

KSA-based customers, as well as any Google Cloud customers using the Dammam
region, who are interested in Google's
[Assured Workloads](https://cloud.google.com/assured-workloads/docs/overview) product
have a few options for enabling these controls:

1. [Sovereign Controls Foundation by CNTXT](https://cloud.google.com/sovereign-controls-by-partners/docs/sovereign-controls-cntxt-foundation)
  and [Sovereign Controls Advanced by CNTXT](https://cloud.google.com/sovereign-controls-by-partners/docs/sovereign-controls-cntxt-advanced):
  These control packages are built on Google Cloud's
  [Class C-certified](https://cloud.google.com/security/compliance/ksa)
  infrastructure and have additional CNTXT-operated controls to help
  organizations meet more stringent data sovereignty requirements. With these
  offerings, CNTXT augments Google Cloud by offering a managed
  [Cloud External Key Manager (EKM)](https://cloud.google.com/kms/docs/ekm) with
  [Key Access Justifications (KAJ)](https://cloud.google.com/assured-workloads/key-access-justifications/docs/overview)
  service as well as localized support.
2. [KSA Data Boundary with Access Justifications](https://cloud.google.com/assured-workloads/docs/control-packages/ksa-data-boundary-access-justifications):
  This control package is intended for organizations that don't need the
  additional assurance of a local partner. It can help non-Saudi domiciled
  organizations deploy cloud-based applications and services in the region while
  adhering to local regulations and industry standards.

You can read more about this in
[Google's launch announcement of sovereign control offerings for the Dammam region and KSA customers](https://cloud.google.com/blog/products/identity-security/google-cloud-expands-services-in-saudi-arabia-delivering-enhanced-data-sovereignty-and-ai-capabilities).

## KSA regulations and compliance

The [Communications, Space and Technology Commission](https://www.cst.gov.sa/en/Pages/default.aspx#?) (CST)
in the Kingdom of Saudi Arabia has granted a
[Class C license](https://www.cst.gov.sa/en/services/licensing/Pages/ApprovedServiceRegistery.aspx?ver=1&name=Google%20cloud)
(covering Qualifying, Class A, B, and C licenses) to Google Cloud in the Dammam
region.

The qualification is based on an assessment by the
[National Cybersecurity Agency](https://nca.gov.sa/en) (NCA) against the
NCA's [Essential Cybersecurity Controls](https://nca.gov.sa/ecc-en.pdf) (ECC)
and the [Cloud Cybersecurity Controls](https://nca.gov.sa/ccc-en.pdf) (CCC).

The ECC sets the minimum cybersecurity requirements for organizations that are
within its scope, while the CCC is an extension to the ECC with the goal of
minimizing cybersecurity risks of Cloud Service Providers and Cloud Services
Tenants. Customers can find Google's licensing information on the
[CST website](https://www.cst.gov.sa/en/services/licensing/Pages/ApprovedServiceRegistery.aspx?ver=1&name=Google%20cloud).

    Was this helpful?

---

# Data analytics

> Documentation and resources for unlocking your data's potential and transforming it into actionable AI insights with Google Cloud products.

[Get started for free](https://console.cloud.google.com/freetrial)

#### Start your proof of concept with $300 in free credit

- Develop with our latest Generative AI models and tools.
- Get free usage of 20+ popular products, including Compute Engine and AI APIs.
- No automatic charges, no commitment.

       [View free product offers](https://cloud.google.com/free/docs/free-cloud-features#free-tier)

#### Keep exploring with 20+ always-free products.

Access 20+ free products for common use cases, including AI APIs, VMs, data warehouses,
          and more.

                        Learn how BigQuery helps organizations to get insights into their data.
                        Plan your approach with Architecture Center resources across a variety of data and analytics topics.
                        Plan how to design an analytics lakehouse to store, process, and activate data.
                        Study Google Cloud technologies essential to the data analyst role.
                        Study how to explore data in Looker and set up self-serve analytics for your users.
                        Choose the services to run your data and analytics workloads.

Use a serverless, cost-effective, and multi-cloud data and AI platform designed to help you turn big data into valuable business insights powered by Gemini.

     ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/data-analytics-color.svg)
                                      Understand your data using a fully managed, highly scalable data platform with built-in machine learning (ML).

Get business intelligence in real time, built on governed data, that offers repeatable analysis and inspires in-depth understanding of the data.

                                      Maximize your data analysis investments when running analytic queries on large datasets.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/products/looker-color.svg)
                                      Access, analyze, and act on an up-to-date, trusted version of your data.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/products/looker-color.svg)
                                      Tell great data stories to support better business decisions.

Manage the end-to-end data lifecycle and make it easier to manage, discover, govern, and share data and AI assets.

                                      Enable intelligent data management with unified metadata and governance and security policies.

                                      Share data and insights at scale across organizational boundaries with a robust security and privacy framework.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/data-analytics-color.svg)
                                      Unify distributed data, automate data management and governance, and enable data discovery and quality checks across various Google Cloud and third party sources.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/security-and-identity-color.svg)
                                      Discover and redact sensitive data.

                                      Discover and understand your data using a fully managed and scalable data discovery and metadata management service. (Deprecated)

Ingest, transform, and load data from disparate data sources in a scalable and secure fashion, and build end-to-end orchestration for the enterprise.

                                      Automate data ingestion at scale into BigQuery without writing code, on a scheduled or ad hoc basis.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/data-analytics-color.svg)
                                      Create, schedule, monitor, and manage workflows using a fully managed orchestration service built on Apache Airflow.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/data-analytics-color.svg)
                                      Quickly build and manage data pipelines using fully managed, code-free data integration with a graphical interface.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/data-analytics-color.svg)
                                      Get an end-to-end experience that helps data teams build, version control, and orchestrate SQL pipelines in BigQuery.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/data-analytics-color.svg)
                                      Use a serverless and easy-to-use change data capture (CDC) and replication service for real-time data ingestion.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/storage-color.svg)
                                      Transfer data between Cloud Storage services such as AWS S3 and Cloud Storage.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/migration-color.svg)
                                      Ship large volumes of data to Google Cloud using rackable storage.

Migrate your lakehouse or warehouse to BigQuery with easy to use tools powered by Gemini that assist in every phase of migration.

                                      Learn about general concepts and a framework that you can use to organize and structure your migration to BigQuery.

                                      Learn about the BigQuery Migration Service, which is a comprehensive solution for migrating your data warehouse or lakehouse to BigQuery.

Empower your data journey, from robust batch processing using managed Apache Spark and Apache Hadoop, to dynamic real-time stream processing with serverless, scalable pipelines using Apache Beam.

     ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/data-analytics-color.svg)
                                      Develop real-time batch and streaming data processing pipelines.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/data-analytics-color.svg)
                                      Perform batch processing, querying, and streaming using a managed Apache Spark and Apache Hadoop service.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/data-analytics-color.svg)
                                      Use Serverless for Apache Spark to run Apache Spark batch workloads without provisioning and managing your own cluster.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/data-analytics-color.svg)
                                      A fully managed Apache Hive metastore (HMS) that runs on Google Cloud.

Ingest, process, and analyze event streams in real time, and generate actionable, real-time insights.

     ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/data-analytics-color.svg)
                                      Develop real-time batch and streaming data processing pipelines.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/data-analytics-color.svg)
                                      Use a managed cloud service that lets you ingest Apache Kafka streams directly into Google Cloud.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/data-analytics-color.svg)
                                      Ingest event streams from anywhere, at any scale.

Seamlessly integrate the power of generative AI and machine learning directly within your data to unlock deeper insights.

                                      Build and train machine learning (ML) models directly using SQL queries.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/data-analytics-color.svg)
                                      Deploy and manage complete machine learning (ML) pipelines.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/products/gemini-color.svg)
                                      Use AI-powered assistance to help you work with your data in BigQuery.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/products/gemini-color.svg)
                                      Get AI-powered assistance to help you work with your data in Looker.
                                               ![](https://cloud.google.com/_static/clouddocs/images/icons/products/vertex-ai-color.svg)
                                      Build and use generative AI using a fully managed, unified AI development platform.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/data-analytics-color.svg)
                                      Get indexed blockchain data made available through BigQuery for easy analysis through SQL.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/data-analytics-color.svg)
                                      Get reference architectures, packaged solution deployment content, and integration services to kickstart your data and AI cloud journey with open source Cortex Framework.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/data-analytics-color.svg)
                                      Everything you need to rapidly build, deploy, and manage data with AI solutions for your business from the Google Cloud console.

                                      Learn about Google Earth Engine, which is a geospatial processing service. With Earth Engine, you can perform geospatial processing at scale, powered by Google Cloud.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/data-analytics-color.svg)
                                      Use an end-to-end solution that delivers scalable and seamless connectivity between the factory floor and the cloud.
                                                Was this helpful?

---

# Databases

> Documentation and resources for migrating and managing enterprise data with security, reliability, high availability, and fully-managed data services on Google Cloud.

[Get started for free](https://console.cloud.google.com/freetrial)

#### Start your proof of concept with $300 in free credit

- Develop with our latest Generative AI models and tools.
- Get free usage of 20+ popular products, including Compute Engine and AI APIs.
- No automatic charges, no commitment.

       [View free product offers](https://cloud.google.com/free/docs/free-cloud-features#free-tier)

#### Keep exploring with 20+ always-free products.

Access 20+ free products for common use cases, including AI APIs, VMs, data warehouses,
          and more.

                        Plan your approach with Architecture Center resources across a variety of database topics.
                        Plan with architectures, use cases, and best practices for multicloud database management.
                        Study how to design, create, manage, migrate, and troubleshoot databases used by applications to store and retrieve data.

Expand this section to see relevant products and documentation.

     ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/databases-color.svg)
                                      Store terabytes or petabytes of data using a NoSQL wide-column database service.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/databases-color.svg)
                                      A NoSQL document database built for automatic scaling, high performance, and ease of application development.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/databases-color.svg)
                                      A NoSQL document database with MongoDB compatibility built for automatic scaling, high performance, and ease of application development.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/databases-color.svg)
                                      A flexible, scalable NoSQL document database for mobile, web, and server development.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/databases-color.svg)
                                      Achieve extreme performance using a managed in-memory Valkey service.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/databases-color.svg)
                                      Achieve extreme performance using a managed in-memory Redis Cluster service.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/databases-color.svg)
                                      Achieve extreme performance using a managed in-memory data store service.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/databases-color.svg)
                                      Applications running on Google Cloud can achieve extreme performance by leveraging the scalable, available, secure, and managed Memcached service.

Expand this section to see relevant products and documentation.

     ![](https://cloud.google.com/_static/clouddocs/images/icons/products/alloydb-color.svg)
                                      A fully-managed, PostgreSQL-compatible database for demanding transactional workloads.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/products/alloydb-color.svg)
                                      A downloadable edition of AlloyDB for PostgreSQL, designed to run anywhere—in your data center, on your laptop, at the edge, and in any cloud.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/products/spanner-color.svg)
                                      Back your apps with a mission-critical, global-scale database service.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/products/sql-color.svg)
                                      General information about the Cloud SQL options, each a fully-managed database service that helps you set up, maintain, manage, and administer your relational databases.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/products/sql-color.svg)
                                      A fully-managed database service that helps you set up, maintain, manage, and administer your MySQL relational databases on Google Cloud.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/products/sql-color.svg)
                                      A fully-managed database service that helps you set up, maintain, manage, and administer your PostgreSQL relational databases on Google Cloud.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/products/sql-color.svg)
                                      A managed database service that helps you set up, maintain, manage, and administer your SQL Server databases on Google Cloud.

Expand this section to see relevant products and documentation.

     ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/databases-color.svg)
                                      Serverless, easy, minimal downtime migrations to Cloud SQL.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/data-analytics-color.svg)
                                      A serverless and easy-to-use change data capture (CDC) and replication service.

Expand this section to see relevant products and documentation.

     ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/databases-color.svg)
                                      Fleet management solution that gives you one centralized view across your entire database fleet.
                                               ![](https://cloud.google.com/_static/clouddocs/images/icons/products/bigquery-color.svg)
                                      Understand your data using a fully managed, highly scalable data warehouse with built-in ML.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/products/bigquery-color.svg)
                                      Query structured data in external data stores with access delegation.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/products/bigquery-color.svg)
                                      Storage optimized for running analytic queries over large datasets and high-throughput streaming ingestion and high-throughput reads.

---

# Google Cloud SDK,languages,frameworks,and tools

> Documentation and resources for using Google Cloud SDK, languages, frameworks, and tools effectively in cloud development.

[Get started for free](https://console.cloud.google.com/freetrial)

#### Start your proof of concept with $300 in free credit

- Develop with our latest Generative AI models and tools.
- Get free usage of 20+ popular products, including Compute Engine and AI APIs.
- No automatic charges, no commitment.

       [View free product offers](https://cloud.google.com/free/docs/free-cloud-features#free-tier)

#### Keep exploring with 20+ always-free products.

Access 20+ free products for common use cases, including AI APIs, VMs, data warehouses,
          and more.

                        Use client libraries to significantly reduce the amount of code you need to write.

                        Search for samples demonstrating the usage of Google Cloud products.

                        Review key authentication methods and concepts for Google Cloud products and services.

                        Study how to write infrastructure as code with Terraform in Google Cloud.
                        Study how to use Kubernetes, a software layer that sits between your applications and your hardware infrastructure, in Google Cloud.
                        Study how to design and develop cloud-native applications that seamlessly integrate managed services from Google Cloud.
                        Study Go by reviewing Go code, and then creating and deploying simple Go apps on Google Cloud.

Expand this section to see relevant products and documentation.

      ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/developer-tools-color.svg)
                                      Create and manage Google Cloud resources and services directly on the command line or via scripts using the gcloud CLI.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/developer-tools-color.svg)
                                      Manage Google Cloud resources programmatically.

                                      Learn how to use Cloud Client Libraries for .NET to access Google Cloud APIs programmatically.

                                      Learn how to use Cloud Client Libraries for C++ to access Google Cloud APIs programmatically.

                                      Learn how to use Google Cloud product libraries and frameworks to build and iterate Go apps on Google Cloud.

                                      Learn how to use Google Cloud product libraries and frameworks to build and iterate Java apps on Google Cloud.

                                      Learn how to use Google Cloud product libraries and frameworks to build and iterate Node.js apps on Google Cloud.

                                      Learn how to use Google Cloud product libraries and frameworks to build and iterate PHP apps on Google Cloud.

                                      Learn how to use Google Cloud product libraries and frameworks to build and iterate Python apps on Google Cloud.

                                      Learn how to use Google Cloud product libraries and frameworks to build and iterate Ruby apps on Google Cloud.

Expand this section to see relevant products and documentation.

     ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/developer-tools-color.svg)
                                      Simplify application development by providing the infrastructure for enterprise applications to accomplish common tasks.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/products/kubernetes-engine-color.svg)
                                      Reliably, efficiently, and securely deploy and scale containerized applications on Kubernetes.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/developer-tools-color.svg)
                                      Use Google and Google Cloud services in your AI-powered applications with our remote Model Context Protocol servers.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/observability-color.svg)
                                      Globally monitor and alert on your workloads, using Prometheus, without having to manually manage and operate Prometheus at scale.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/developer-tools-color.svg)
                                      Learn to use Terraform to reliably provision infrastructure on Google Cloud.
                                               ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/developer-tools-color.svg)
                                      Use an online development and operations environment accessible anywhere with your browser.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/developer-tools-color.svg)
                                      IDE support for the full development cycle of Kubernetes and Cloud Run applications.

---

# Distributed,hybrid,and multicloud

> Documentation and resources for extending your Google Cloud topology to the edge, on-premises, and other cloud platforms.

[Get started for free](https://console.cloud.google.com/freetrial)

#### Start your proof of concept with $300 in free credit

- Develop with our latest Generative AI models and tools.
- Get free usage of 20+ popular products, including Compute Engine and AI APIs.
- No automatic charges, no commitment.

       [View free product offers](https://cloud.google.com/free/docs/free-cloud-features#free-tier)

#### Keep exploring with 20+ always-free products.

Access 20+ free products for common use cases, including AI APIs, VMs, data warehouses,
          and more.

                        Extend Google Cloud infrastructure to the edge and into your data centers.

                        Plan your approach with Architecture Center resources across a variety of hybrid and multicloud topics.
                        Plan with best practices to build and deploy hybrid and multicloud architecture patterns.
                        Study managing container-based applications across multiple clouds, or between on-premises and cloud environments.
                        Study designing, building, analyzing, and maintaining cloud-native applications.
                        Study Google Cloud networking technologies, including common network design patterns, connectivity to VPC networks, and private connection options.

Extend Google Cloud infrastructure and services to the edge and into your data centers.

     ![](https://cloud.google.com/_static/clouddocs/images/icons/products/distributed-cloud-color.svg)
                                      A private cloud that enables public sector organizations and regulated enterprises to address strict data residency and security requirements.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/products/distributed-cloud-color.svg)
                                      Run GKE clusters on dedicated hardware provided and maintained by Google that is separate from the Google Cloud data center.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/products/distributed-cloud-color.svg)
                                      Create, manage, and upgrade GKE clusters on premises while using Google Cloud features. Your clusters and workloads run directly on your on-premises hardware.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/products/distributed-cloud-color.svg)
                                      Create, manage, and upgrade GKE clusters on premises while `using Google Cloud features. Your clusters and workloads run in a VMware vSphere environment on your on-premises hardware.

Identify where to deploy resources across cloud providers, and create and manage Kubernetes clusters from Google Cloud in both AWS and Azure cloud environments.

     ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/hybrid-multicloud-color.svg)
                                      Provides a unified way to work with Kubernetes clusters, extending GKE to work in multiple environments.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/hybrid-multicloud-color.svg)
                                      Manage any standard, CNCF-compliant Kubernetes installation, including clusters in production. Add GKE Enterprise features to standardize and secure your clusters across multiple cloud environments and Kubernetes vendors.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/hybrid-multicloud-color.svg)
                                      Manage GKE clusters running on AWS infrastructure.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/hybrid-multicloud-color.svg)
                                      Manage GKE clusters running on Azure infrastructure.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/compute-color.svg)
                                      Abstracts away the complexity of Kubernetes, making it easy to build and deploy your serverless workloads across hybrid and multicloud environments.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/operations-color.svg)
                                      Find cloud locations across cloud providers based on proximity, jurisdiction, and carbon footprint.

Simplify managing multi-cluster deployments, including  clusters outside Google Cloud.

                                      Manage clusters, infrastructure, and workloads together as a fleet of Kubernetes clusters and other resources.
                                               ![](https://cloud.google.com/_static/clouddocs/images/icons/products/kubernetes-engine-color.svg)
                                      Deploy, manage, and scale containerized applications on Kubernetes, powered by Google Cloud.

                                      View the features included in each GKE tier - Standard and Enterprise.

                                      Check, audit, and enforce your clusters' compliance with policies related to security, regulations, or business rules.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/networking-color.svg)
                                      Monitor and manage a reliable service mesh on-premises or on Google Cloud.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/products/kubernetes-engine-color.svg)
                                      Lets cluster operators and platform administrators deploy configurations from a source of truth.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/products/kubernetes-engine-color.svg)
                                      Check, audit, and enforce your clusters' compliance with policies related to security, regulations, or business rules.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/networking-color.svg)
                                      Extend your external network to the Google network through a high-availability, low-latency connection.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/hybrid-multicloud-color.svg)
                                      A flexible serverless development platform on GKE.
                                           ![](https://cloud.google.com/_static/clouddocs/images/icons/categories/serverless-color.svg)
                                      Fully managed node hosting for developing on the blockchain.
                                                Was this helpful?
