# IAM controls for generative AI use casesStay organized with collectionsSave and categorize content based on your preferences. and more

# IAM controls for generative AI use casesStay organized with collectionsSave and categorize content based on your preferences.

> Review the recommended IAM security best practices and guidelines that aren&#39;t common to generative AI workloads on Google Cloud.

# IAM controls for generative AI use casesStay organized with collectionsSave and categorize content based on your preferences.

This document includes the best practices and guidelines for Identity and Access Management (IAM) when running
generative AI workloads on Google Cloud. Use
[IAM](https://cloud.google.com/iam/docs/overview) with Vertex AI to controls who can perform
specific actions on your generative workload resources, such as creating,
editing, or deleting them.

## Required IAM controls

The following controls are strongly recommended when using
IAM.

### Disable automatic Identity and Access Management (IAM) grants for default service accounts

| Google control ID | IAM-CO-4.1 |
| --- | --- |
| Category | Required |
| Description | Use theautomaticIamGrantsForDefaultServiceAccountsboolean constraint to disable automatic role grants when Google Cloud services automatically create default service accounts with overly permissive roles. For example, if you don't enforce this constraint and you create a default service account, the service account is automatically granted the Editor role (roles/editor) on your project. |
| Applicable products | IAMOrganization Policy Service |
| Path | constraints/iam.automaticIamGrantsForDefaultServiceAccounts |
| Operator | Is |
| Value | False |
| Type | Boolean |
| Related NIST-800-53 controls | AC-3AC-17AC-20 |
| Related CRI profile controls | PR.AC-3.1PR.AC-3.2PR.AC-4.1PR.AC-4.2PR.AC-4.3PR.AC-6.1PR.PT-3.1PR.PT-4.1 |
| Related information | Types of service accounts |

### Block the creation of external service account keys

| Google control ID | IAM-CO-4.2 |
| --- | --- |
| Category | Required |
| Description | Use theiam.disableServiceAccountKeyCreationboolean constraint to disable external service account keys from being created. This constraint lets you control the use of unmanaged long-term credentials for service accounts. When this constraint is set, you can't create user-managed credentials for service accounts in projects affected by the constraint. |
| Applicable products | Organization Policy ServiceIAM |
| Path | constraints/iam.disableServiceAccountKeyCreation |
| Operator | Is |
| Value | True |
| Type | Boolean |
| Related NIST-800-53 controls | AC-3AC-17AC-20 |
| Related CRI profile controls | PR.AC-3.1PR.AC-3.2PR.AC-4.1PR.AC-4.2PR.AC-4.3PR.AC-6.1PR.PT-3.1PR.PT-4.1 |
| Related information | Disable service account key creation |

### Block service account key uploads

| Google control ID | IAM-CO-4.3 |
| --- | --- |
| Category | Required |
| Description | Use theiam.disableServiceAccountKeyUploadboolean constraint to disable the upload of external public keys to service accounts. When this constraint is set, users can't upload public keys to service accounts in projects affected by the constraint. |
| Applicable products | Organization Policy ServiceIAM |
| Path | constraints/iam.disableServiceAccountKeyUpload |
| Operator | Is |
| Value | True |
| Type | Boolean |
| Related NIST-800-53 controls | AC-3AC-17AC-20 |
| Related CRI profile controls | PR.AC-3.1PR.AC-3.2PR.AC-4.1PR.AC-4.2PR.AC-4.3PR.AC-6.1PR.PT-3.1PR.PT-4.1 |
| Related information | Disable service account key upload |

## Recommended controls based on generative AI use case

Depending on your use cases around generative AI, you might require additional
IAM controls.

### Implement tags to efficiently assign Identity and Access Management (IAM) policies and organization policies

| Google control ID | IAM-CO-6.1 |
| --- | --- |
| Category | Recommended |
| Description | Tags provide a way to create annotations for resources, and in some cases conditionally allow or deny policies based on whether a resource has a specific tag. Use tags and conditional policy enforcement for fine-grained control across your resource hierarchy. |
| Applicable products | Resource Manager |
| Related NIST-800-53 controls | AC-2AC-3AC-5 |
| Related CRI profile controls | PR.AC-1.1PR.AC-1.2PR.AC-1.3PR.AC-4.1PR.AC-4.2PR.AC-4.3PR.AC-6.1PR.DS-5.1PR.PT-3.1 |
| Related information | Tags overview |

### Audit high-risk changes to Identity and Access Management (IAM)

| Google control ID | IAM-CO-7.1 |
| --- | --- |
| Category | Recommended |
| Description | Use Cloud Audit Logs to monitor for high-risk activity, such as accounts being granted high-risk roles like Organization Admin and Super Admin. Set up alerts for this type of activity. |
| Applicable products | Cloud Audit Logs |
| Related NIST-800-53 controls | AU-2AU-3AU-8AU-9 |
| Related CRI profile controls | DM.ED-7.1DM.ED-7.2DM.ED-7.3DM.ED-7.4PR.IP-1.4 |
| Related information | Identity and Access Management audit loggingCloud Audit Logs overview |

## Optional common controls

You can optionally implement the following controls based on your organization's requirements.

### Configure Context-Aware Access for Google consoles

| Google control ID | IAM-CO-8.2 |
| --- | --- |
| Category | Optional |
| Description | With Context-Aware Access, you can create granular access control security policies for applications based on attributes such as user identity, location, device security status, and IP address. We recommend that you use Context-Aware Access to restrict access to the the Google Cloud console (https://console.cloud.google.com/) and the Google Admin console (https://admin.cloud.google.com). |
| Applicable products | Cloud IdentityContext-Aware Access |
| Related NIST-800-53 controls | AC-3AC-12AC-17AC-20SC-7SC-8 |
| Related CRI profile controls | PR.AC-3.1PR.AC-3.2PR.AC-4.1PR.AC-4.2PR.AC-4.3PR.AC-5.1PR.AC-5.2PR.AC-6.1PR.AC-7.1PR.AC-7.2PR.DS-2.1PR.DS-2.2PR.DS-5.1PR.PT-4.1DE.CM-1.1DE.CM-1.2DE.CM-1.3DE.CM-1.4 |
| Related information | Protect your business with Context-Aware Access |

## What's next

- Review [Organization Policy Service
  controls](https://cloud.google.com/docs/security/security-best-practices-genai/orgpolicy-controls).
- See more [Google Cloud security best practices and guidelines for generative
  AI workloads](https://cloud.google.com/docs/security/security-best-practices-genai).

   Was this helpful?

---

# Organization Policy controls for generative AI use casesStay organized with collectionsSave and categorize content based on your preferences.

> Review the recommended Organization Policy Service security best practices and guidelines that aren&#39;t common to generative AI workloads on Google Cloud.

# Organization Policy controls for generative AI use casesStay organized with collectionsSave and categorize content based on your preferences.

This document includes the best practices and guidelines for Organization Policy Service
when running generative AI workloads on Google Cloud. Use
[Organization Policy](https://cloud.google.com/resource-manager/docs/organization-policy/overview)
with Vertex AI to centrally manage and enforce policies across your
Google Cloud environment. Organization Policy helps to ensure consistent
configuration and security compliance across the projects and resources within
your organization.

## Required Organization Policy controls

The following controls are strongly recommended when using
Organization Policy.

### Configure separation of duties for organization policy administrators

| Google control ID | OPS-CO-6.1 |
| --- | --- |
| Category | Required |
| Description | Assign the Organization Policy Administrator (roles/orgpolicy.policyAdmin) role to groups that are accountable for the security posture of the Google Cloud organization. To avoid resource creation that violates security policy, don't assign this role to project owners. |
| Applicable products | IAMOrganization Policy Service |
| Related NIST-800-53 controls | AC-2AC-3AC-5 |
| Related CRI profile controls | PR.AC-1.1PR.AC-1.2PR.AC-1.3PR.AC-4.1PR.AC-4.2PR.AC-4.3PR.AC-6.1PR.DS-5.1PR.PT-3.1 |
| Related information | Creating and managing organization resourcesDetermine which principals have certain roles or permissions |

## What's next

- Review [Pub/Sub
  controls](https://cloud.google.com/docs/security/security-best-practices-genai/pubsub-controls).
- See more [Google Cloud security best practices and guidelines for generative
  AI workloads](https://cloud.google.com/docs/security/security-best-practices-genai).

   Was this helpful?

---

# Pub/Sub controls for generative AI use casesStay organized with collectionsSave and categorize content based on your preferences.

> Review the recommended Google Cloud security best practices and guidelines that aren&#39;t specific to genAI workloads that use Pub/Sub.

# Pub/Sub controls for generative AI use casesStay organized with collectionsSave and categorize content based on your preferences.

This document includes the best practices and guidelines for Pub/Sub when
running generative AI workloads on Google Cloud. Use [Pub/Sub](https://cloud.google.com/pubsub/docs/overview) with Vertex AI to enable efficient communication and automation within your machine learning workflows.

Consider the following use cases for Pub/Sub with Vertex AI:

- **Asynchronous event-driven architecture**: Pub/Sub enables
  event-driven communication so that you can trigger Vertex AI
  pipelines based on events that are published to Pub/Sub topics.
  These events can include new data and model updates.
- **Scalability and reliability**: Pub/Sub is highly scalable,
  letting you handle numerous events without impacting performance. Scalability
  is critical for processing large datasets or running multiple concurrent ML
  jobs. Pub/Sub also provides reliable message delivery and
  ordering within a topic, ensuring processing consistency even under heavy
  workloads.
- **Flexibility**: You can integrate Vertex AI with other
  services like Cloud Run functions or Dataflow using
  Pub/Sub, creating flexible and dynamic ML pipelines.
- **Real-time monitoring and alerts**: Pub/Sub lets you subscribe
  to specific topics to receive real-time notifications about events in your
  Vertex AI pipelines. Real-time monitoring helps you to monitor
  model training progress, data preprocessing results, and prediction output.
  You can configure alerts based on specific events, like failed jobs or
  anomalies detected during prediction. Alerts enable proactive intervention and
  timely troubleshooting.

For example, you can use Pub/Sub for the following activities:

- Trigger model training when new data arrives in a Cloud Storage bucket.
- Send real-time predictions from a deployed model to downstream systems for
  further processing.
- Monitor and react to changes in model performance metrics.
- Trigger alerts for critical events like failed predictions or data quality
  issues.

## Recommended Pub/Sub controls

Depending on your use cases around generative AI, we recommend additional controls. These controls include data retention controls and other policy-driven
controls that are based on your enterprise policies.

### Use CMEK for Pub/Sub messages

| Google control ID | PS-CO-6.1 |
| --- | --- |
| Category | Recommended |
| Description | When you enable customer-managed encryption keys (CMEK) for Pub/Sub, you obtain greater control of the encryption keys that Pub/Sub uses to protect your messages. At the application layer, Pub/Sub individually encrypts incoming messages when Pub/Sub receives them. Before Pub/Sub publishes messages to a subscription, it encrypts the messages using the newest data encryption key (DEK) that was generated for the topic. Pub/Sub decrypts the messages shortly before they're delivered to subscribers.

Pub/Sub uses a Google Cloud service account to access Cloud Key Management Service. The service account is maintained internally by Pub/Sub for each project, and isn't visible in your list of service accounts. |
| Applicable products | Cloud KMSPub/Sub |
| Related NIST-800-53 controls | SC-12SC-13 |
| Related CRI profile controls | PR.DS-1.1PR.DS-1.2PR.DS-2.1PR.DS-2.2PR.DS-5.1 |
| Related information | Configure message encryption |

## Optional Pub/Sub controls

These controls are optional. Consider enforcing them when they apply to your specific use cases.

### Configure message storage policies

| Google control ID | PS-CO-4.1 |
| --- | --- |
| Category | Optional |
| Description | If you publish messages to the global Pub/Sub endpoint, Pub/Sub automatically stores the messages in the nearest Google Cloud region. To control which regions your messages are stored in, configure a message storage policy on your topic.

Use one of the following ways to configure message storage policies for topics:Set a message storage policy using the Resource Location Restriction (gcp.resourceLocations) organization policy constraint.Configure a message storage policy when creating a topic. For example:gcloud pubsub topics create TOPIC_ID \--message-storage-policy-allowed-regions=REGION1, REGION2 |
| Applicable products | Organization Policy ServicePub/Sub |
| Related NIST-800-53 controls | AC-3AC-17AC-20 |
| Related CRI profile controls | PR.AC-3.1PR.AC-3.2PR.AC-4.1PR.AC-4.2PR.AC-4.3PR.AC-6.1PR.PT-3.1PR.PT-4.1 |
| Related information | Configure message storage policies |

## What's next

- Review [Resource Manager
  controls](https://cloud.google.com/docs/security/security-best-practices-genai/resource-manager-controls).
- See more [Google Cloud security best practices and guidelines for generative
  AI workloads](https://cloud.google.com/docs/security/security-best-practices-genai).

---

# Recommended user groups and Identity and Access Management roles for generative AIStay organized with collectionsSave and categorize content based on your preferences.

> Recommended roles and permissions to use with generative AI workloads on Google.

# Recommended user groups and Identity and Access Management roles for generative AIStay organized with collectionsSave and categorize content based on your preferences.

The following table describes the Identity and Access Management (IAM) roles that
we recommend as a starting point for running generative AI workloads on
Google Cloud. Configure your IAM roles to implement separation of
duties within your environment and to align with your risk appetite and
organizational structure.

As you assign these roles to the user groups in your organization, consider
where you need to apply more fine-grained roles to address specific generative
AI use cases and data access requirements. For environments where highly
sensitive data is used to train models, see the [Import data into a secured
BigQuery data
warehouse](https://cloud.google.com/architecture/blueprints/confidential-data-warehouse-blueprint) for
more information about the roles that you can use to permit access to stored
data.

The following table describes the role recommendations. Apply foundational
recommendations to all generative AI workloads, and Vertex AI specific
recommendations to generative AI workloads that use Vertex AI.

| Service | Group | Description | IAM roles |
| --- | --- | --- | --- |
| Foundational | grp-gcp-org-admin | This group administers the resources that belong to the organization.
  Assign this role sparingly. Organization administrators have access to all of
  your Google Cloud resources. Alternatively, because this function is highly
  privileged, consider using individual accounts instead of creating a
  group. | Organization administrator (roles/resourcemanager.organizationAdmin)Folder Admin (roles/resourcemanager.folderAdmin)Project Creator (roles/resourcemanager.projectCreator)Billing Account User (roles/billing.user)Organization Role Administrator (roles/iam.organizationRoleAdmin)Organization Policy Administrator (roles/orgpolicy.policyAdmin)Security Center Admin (roles/securitycenter.admin)Support Account Administrator (roles/cloudsupport.admin) |
| Foundational | grp-gcp-network-admins | This group can create networks, subnets, firewall rules, and network
  devices such as Cloud Router, Cloud VPN, and cloud load balancers. | Compute Network Admin (roles/compute.networkAdmin)Compute Shared VPC Admin (roles/compute.xpnAdmin)Compute Security Admin (roles/compute.securityAdmin)Folder Viewer (roles/resourcemanager.folderViewer) |
| Foundational | grp-gcp-billing-admin | This group sets up billing accounts and monitors their usage. | Billing Account Administrator (roles/billing.admin)Billing Account Creator (roles/billing.creator)Organization Viewer (roles/resourcemanager.organizationViewer) |
| Foundational | grp-gcp-security-admins | This group establishes and manages security policies for the entire
  organization, including access management and organization constraint policies.
  To plan your Google Cloud security infrastructure, see theEnterprise
  foundations blueprint. | BigQuery Data Viewer (roles/bigquery.dataViewer)Compute Viewer (roles/compute.viewer)Folder IAM Admin (roles/resourcemanager.folderIamAdmin)Kubernetes Engine Viewer (roles/container.viewer)Logs Configuration Writer (roles/logging.configWriter)Organization Role Viewer (roles/iam.organizationRoleViewer)Organization Policy Administrator (roles/orgpolicy.policyAdmin)Organization Policy Viewer (roles/orgpolicy.policyViewer)Private Logs Viewer (roles/logging.privateLogViewer)Security Center Admin (roles/securitycenter.admin)Security Reviewer (roles/iam.securityReviewer) |
| Foundational | grp-gcp-billing-viewer | This group monitors the spend on projects. Typically group members are
  part of the finance team. | Billing Account Viewer (roles/billing.viewer) |
| Foundational | grp-gcp-platform-viewer | This group reviews resource information across the Google Cloud
  organization. | Viewer (roles/viewer) |
| Foundational | grp-gcp-security-reviewer | This group reviews cloud security. | Security Reviewer (roles/iam.securityReviewer) |
| Foundational | grp-gcp-network-viewer | This group reviews network configurations. | Compute Network Viewer (roles/compute.networkViewer) |
| Foundational | grp-gcp-audit-viewer | This group views audit logs. | Private Logs Viewer (roles/logging.privateLogViewer)Viewer (roles/viewer) |
| Foundational | grp-gcp-scc-admin | This group administers Security Command Center. | Security Center Admin (roles/securitycenter.admin) |
| Foundational | grp-gcp-secrets-admin | This group manages secrets in Secret Manager. | Secret Manager Admin (roles/secretmanager.admin) |
| Vertex AI administrators | grp-gcp-vertex-ai-admin | This group has full access to all resources in Vertex AI. | Vertex AI Administrator (roles/aiplatform.admin)) |
| Vertex AI viewers | grp-gcp-vertex-ai-viewer | This group views all resources in Vertex AI. | Vertex AI Viewer (roles/aiplatform.viewer) |
| Vertex AI users | grp-gcp-vertex-ai-user | This group uses all resources in Vertex AI. | Vertex AI User (roles/aiplatform.user) |
| Vertex AI Workbench administrators | grp-gcp-vertex-ai-notebook-admin | This group has full access to all runtime templates and runtimes in
  Vertex AI Workbench. | Notebook Runtime Admin (roles/aiplatform.notebookRuntimeAdmin) |
| Vertex AI Workbench users | grp-gcp-vertex-ai-notebook-user | This group creates runtime resources using a runtime template and manages
  the runtime resources that they created. | Notebook Runtime User (roles/aiplatform.notebookRuntimeUser) |

## What's next

- Review [role
  recommendations](https://cloud.google.com/architecture/blueprints/security-foundations/authentication-authorization#groups_for_access_control)
  in the enterprise foundations blueprint.
- Review [common
  controls](https://cloud.google.com/docs/security/security-best-practices-genai/common-genai-controls).
- See more [Google Cloud security best practices and guidelines for generative
  AI workloads](https://cloud.google.com/docs/security/security-best-practices-genai/common-genai-controls).

   Was this helpful?

---

# Resource Manager controls for generative AI use casesStay organized with collectionsSave and categorize content based on your preferences.

> Review the recommended Resource Manager security best practices and guidelines that aren&#39;t common to generative AI workloads on Google Cloud.

# Resource Manager controls for generative AI use casesStay organized with collectionsSave and categorize content based on your preferences.

This document includes the best practices and guidelines for Resource Manager when
running generative AI workloads on Google Cloud. Use [Resource Manager](https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy) with Vertex AI to help group and manage logical components of your Vertex AI workloads.

Consider the following use cases for Resource Manager with Vertex AI:

- To help ensure resource and data isolation and fine-grained access controls, create separate projects for different teams or departments.
- Apply protective security policies to AI workloads.
- Define quotas for GPU usage in training jobs to prevent cost overruns.
- Automate the creation of required Cloud Storage buckets and Compute Engine instances for new projects.
- Track and analyze resource usage patterns for specific projects to optimize resource allocation.
- Generate audit reports to demonstrate compliance with data governance and security policies.

## Required Resource Manager controls

The following controls are strongly recommended when using
Resource Manager.

### Restrict resource service usage

| Google control ID | RM-CO-4.1 |
| --- | --- |
| Category | Required |
| Description | Thegcp.restrictServiceUsageconstraint ensures that only your approved Google Cloud services are used in the right places. For example, a production or highly sensitive folder has a small list of Google Cloud services that are approved to store data. A sandbox folder might have a larger list of services and accompanying data security controls to help prevent data exfiltration. The value is specific to your systems and matches your approved list of services and dependencies for specific folders and projects. |
| Applicable products | Organization Policy ServiceResource Manager |
| Path | constraints/gcp.restrictServiceUsage |
| Operator | Is |
| Related NIST-800-53 controls | AC-3AC-17AC-20 |
| Related CRI profile controls | PR.AC-3.1PR.AC-3.2PR.AC-4.1PR.AC-4.2PR.AC-4.3PR.AC-6.1PR.PT-3.1PR.PT-4.1 |
| Related information | Restricting resource usage |

### Restrict resource locations

| Google control ID | RM-CO-4.2 |
| --- | --- |
| Category | Required |
| Description | The Resource Location Restriction (gcp.resourceLocations) constraint ensures that only your approved Google Cloud regions are used to store data. The value is specific to your systems and matches your organization's approved list of regions for data residency. |
| Applicable products | Organization Policy ServiceResource Manager |
| Path | constraints/gcp.resourceLocations |
| Operator | Is |
| Related NIST-800-53 controls | AC-3AC-17AC-20 |
| Related CRI profile controls | PR.AC-3.1PR.AC-3.2PR.AC-4.1PR.AC-4.2PR.AC-4.3PR.AC-6.1PR.PT-3.1PR.PT-4.1 |
| Related information | Restricting Resource Locations |

## What's next

- Review [Secret Manager
  controls](https://cloud.google.com/docs/security/security-best-practices-genai/secret-manager-controls).
- See more [Google Cloud security best practices and guidelines for generative
  AI workloads](https://cloud.google.com/docs/security/security-best-practices-genai).

   Was this helpful?

---

# Security Command Center controls for generative AI use casesStay organized with collectionsSave and categorize content based on your preferences.

> Review the recommended Security Command Center security best practices and guidelines that aren&#39;t common to generative AI workloads on Google Cloud.

# Security Command Center controls for generative AI use casesStay organized with collectionsSave and categorize content based on your preferences.

This document includes the best practices and guidelines for Security Command Center when
running generative AI workloads on Google Cloud. Use [Security Command Center](https://cloud.google.com/security-command-center/docs/security-command-center-overview) with Vertex AI to help protect your cloud organization, your AI workloads, and the AI data that you store on Google Cloud.

Security Command Center provides the following:

- Centralized security management
- Threat detection and incident response
- Automated security assessments
- Compliance and regulatory reporting
- Security recommendations and best practices

## Required Security Command Center controls

The following controls are strongly recommended when using
Security Command Center.

### Enable Security Command Center at the organization level

| Google control ID | SCC-CO-6.1 |
| --- | --- |
| Category | Required |
| Description | Enable Security Command Center at the organization level to avoid additional configuration. If you don't want to use Security Command Center, you must enable another posture management solution. |
| Applicable products | Security Command Center |
| Related NIST-800-53 controls | SI-4SI-5 |
| Related CRI profile controls | PR.DS-5.1PR.DS-8.1ID.RA-1.1DE.CM-1.1DE.CM-1.2DE.CM-1.3DE.CM-1.4DE.CM-5.1DE.CM-6.1DE.CM-6.2DE.CM-6.3DE.CM-7.1DE.CM-7.2DE.CM-7.3DE.CM-7.4DE.DP-2.1DE.DP-3.1DE.DP-4.1DE.DP-4.2DE.DP-5.1DE.AE-2.1DE.AE-3.1DE.AE-3.2DE.AE-4.1ID.RA-1.1ID.RA-2.1ID.RA-3.1ID.RA-3.2ID.RA-3.3 |
| Related information | Overview of activating Security Command Center |

## Recommended controls based on generative AI use case

Depending on your use cases around generative AI, we recommend additional
controls. These controls include data retention controls and other policy-driven
controls that are based on your enterprise policies.

### Configure alerts from Security Command Center

| Google control ID | SCC-CO-7.1 |
| --- | --- |
| Category | Recommended |
| Description | Alerts from the Security Command Center provide visibility into your organization and notify you about issues with your Google Cloud services so you can take appropriate action. You can set up alerts in Cloud Logging to get notifications on errors that are related to the Security Command Center service agent (service-org-ORGANIZATION_NUMBER@security-center-api.iam.gserviceaccount.com). |
| Applicable products | Security Command CenterLogging |
| Related NIST-800-53 controls | AU-2AU-3AU-8AU-9 |
| Related CRI profile controls | DM.ED-7.1DM.ED-7.2DM.ED-7.3DM.ED-7.4PR.IP-1.4 |
| Related information | Troubleshooting |

## What's next

- Review [Virtual Private Cloud (VPC)
  controls](https://cloud.google.com/docs/security/security-best-practices-genai/vpc-controls).
- See more [Google Cloud security best practices and guidelines for generative
  AI workloads](https://cloud.google.com/docs/security/security-best-practices-genai).

---

# Secret Manager controls for generative AI use casesStay organized with collectionsSave and categorize content based on your preferences.

> Review the recommended Google Cloud security best practices and guidelines that aren&#39;t specific to genAI workloads that use Secret Manager.

# Secret Manager controls for generative AI use casesStay organized with collectionsSave and categorize content based on your preferences.

This document includes the best practices and guidelines for Secret Manager when
running generative AI workloads on Google Cloud. Use [Secret Manager](https://secret-manager/docs/overview) with Vertex AI to help secure the sensitive data and credentials that are used in Vertex AI projects.

Consider the following use cases for Secret Manager with Vertex AI:

- Store API keys for accessing external data sources used in model training.
- Encrypt database credentials within prediction pipelines for secure access.
- Provision temporary access tokens for secure communication between services.
- Secure private keys and certificates that you use for encrypting communication channels.
- Manage passwords and credentials for third-party services that you use in your ML workflows.

## Required Secret Manager controls

The following controls are strongly recommended when using
Secret Manager.

### Set up automatic secret rotation

| Google control ID | SM-CO-6.2 |
| --- | --- |
| Category | Required |
| Description | Automatically rotate secrets and have emergency rotation procedures available in case of a compromise. |
| Applicable products | Secret Manager |
| Related NIST-800-53 controls | SC-12SC-13 |
| Related CRI profile controls | PR.DS-1.1PR.DS-1.2PR.DS-2.1PR.DS-2.2PR.DS-5.1 |
| Related information | Create rotation schedules in Secret Manager |

### Recommended controls based on generative AI use case

If you handle sensitive data or sensitive generative AI workloads, we recommend
that you implement the following controls in your applicable generative AI use
cases.

### Replicate secrets automatically

| Google control ID | SM-CO-6.1 |
| --- | --- |
| Category | Recommended |
| Description | Choose the automatic replication policy to replicate your secrets unless your workload has specific location requirements. The automatic policy meets the availability and performance needs of most workloads. If your workload has specific location requirements, you can use the API to select the locations for the replication policy when you create the secret. |
| Applicable products | Secret Manager |
| Related NIST-800-53 controls | SC-12SC-13 |
| Related CRI profile controls | PR.DS-1.1PR.DS-1.2PR.DS-2.1PR.DS-2.2PR.DS-5.1 |
| Related information | Choose a replication policy |

## What's next

- Review [Security Command Center
  controls](https://cloud.google.com/docs/security/security-best-practices-genai/scc-controls).
- See more [Google Cloud security best practices and guidelines for generative
  AI workloads](https://cloud.google.com/docs/security/security-best-practices-genai).

   Was this helpful?
