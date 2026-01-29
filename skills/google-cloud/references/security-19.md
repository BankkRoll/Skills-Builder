# Cloud Storage controls for generative AI use casesStay organized with collectionsSave and categorize content based on your preferences. and more

# Cloud Storage controls for generative AI use casesStay organized with collectionsSave and categorize content based on your preferences.

> Review the recommended Cloud Storage security best practices and guidelines that aren&#39;t common to generative AI workloads on Google Cloud.

# Cloud Storage controls for generative AI use casesStay organized with collectionsSave and categorize content based on your preferences.

This document includes the best practices and guidelines for Cloud Storage when
running generative AI workloads that use Google Cloud. Use [Cloud Storage](https://cloud.google.com/storage/docs/introduction) with Vertex AI to store training data, model artifacts, and production data.

Consider the following use cases for Cloud Storage with Vertex AI:

- **Store training data storage**: Vertex AI lets you store your
  training datasets in Cloud Storage buckets. Using Cloud Storage
  offers several advantages:
  - Cloud Storage can handle datasets of any size, allowing you to train
    models on massive amounts of data without storage limitations.
  - You can set granular access controls and encryption on your
    Cloud Storage buckets to ensure that your sensitive training data is
    protected.
  - Cloud Storage lets you track changes and revert to previous versions of
    your data, providing valuable audit trails and facilitating reproducible
    training experiments.
  - Vertex AI seamlessly integrates with Cloud Storage,
    letting you access your training data within the platform.
- **Store model artifacts**: You can store trained model artifacts such as
  including model files, hyperparameter configurations, and training logs, in
  Cloud Storage buckets. Using Cloud Storage lets you do the following:
  - Keep all your model artifacts in Cloud Storage as a centralized
    repository to conveniently access and manage them.
  - Track and manage different versions of your models, facilitating comparisons
    and rollbacks if needed.
  - Grant teammates and collaborators access to specific Cloud Storage
    buckets to efficiently share models.
- **Store production data**: For models used in production, Cloud Storage
  can store the data being fed to the model for prediction. For example, you can
  use Cloud Storage to do the following:
  - Store user data and interactions for real-time personalized recommendations.
  - Keep images for on-demand processing and classification using your models.
  - Maintain transaction data for real-time fraud identification using your
    models.
- **Integrate with other services**: Cloud Storage integrates seamlessly
  with other Google Cloud services used in Vertex AI
  workflows, such as the following:
  - Dataflow for streamline data preprocessing and transformation
    pipelines.
  - BigQuery for access to large datasets stored in
    BigQuery for model training and inference.
  - Cloud Run functions for actions based on model predictions or data
    changes in Cloud Storage buckets.
- **Manage costs**: Cloud Storage offers a pay-as-you-go pricing model,
  meaning you only pay for the storage you use. This provides cost efficiency,
  especially for large datasets.
- **Enable high availability and durability**: Cloud Storage ensures your
  data is highly available and protected against failures or outages,
  guaranteeing reliability and robust access to your ML assets.
- **Enable multi-region support**: Store your data in multiple
  Cloud Storage regions that are geographically closer to your users or
  applications, enhancing performance and reducing latency for data access and
  model predictions.

## Required Cloud Storage controls

The following controls are strongly recommended when using
Cloud Storage.

### Block public access to Cloud Storage buckets

| Google control ID | GCS-CO-4.1 |
| --- | --- |
| Category | Required |
| Description | Thestorage.publicAccessPreventionboolean constraint prevents access to existing and future resources over the internet. It disables and blocks access control lists (ACLs) and Identity and Access Management (IAM) permissions that grant access toallUsersandallAuthenticatedUsers. |
| Applicable products | Organization Policy ServiceCloud Storage |
| Path | constraints/storage.publicAccessPrevention |
| Operator | == |
| Value | True |
| Type | Boolean |
| Related NIST-800-53 controls | AC-3AC-17AC-20 |
| Related CRI profile controls | PR.AC-3.1PR.AC-3.2PR.AC-4.1PR.AC-4.2PR.AC-4.3PR.AC-6.1PR.PT-3.1PR.PT-4.1 |
| Related information | Public access prevention |

### Use uniform bucket-level access

| Google control ID | GCS-CO-4.2 |
| --- | --- |
| Category | Required |
| Description | Thestorage.uniformBucketLevelAccessboolean constraint requires buckets to use uniform bucket-level access. Uniform bucket-level access lets you only use bucket-level Identity and Access Management (IAM) permissions to grant access to your Cloud Storage resources. |
| Applicable products | Organization Policy ServiceCloud Storage |
| Path | constraints/storage.uniformBucketLevelAccess |
| Operator | == |
| Value | True |
| Type | Boolean |
| Related NIST-800-53 controls | AC-3AC-17AC-20 |
| Related CRI profile controls | PR.AC-3.1PR.AC-3.2PR.AC-4.1PR.AC-4.2PR.AC-4.3PR.AC-6.1PR.PT-3.1PR.PT-4.1 |
| Related information | Require uniform bucket-level access |

### Protect HMAC keys for service accounts

| Google control ID | GCS-CO-6.9 |
| --- | --- |
| Category | Required |
| Description | An HMAC key is a long-lived type of credential that is associated with a service account or a user account in Cloud Storage. Use an HMAC key to create signatures that are included in requests to Cloud Storage. A signature proves a user or service account has authorized a request.Unlike short-lived credentials (such as. OAuth 2.0 tokens), HMAC keys don't expire automatically and remain valid until manually revoked. HMAC keys are high-risk credentials: if compromised, they provide persistent access to your resources. You must ensure appropriate mechanisms are in place to help protect them. |
| Applicable products | Cloud Storage |
| Path | storage.projects.hmacKeys/id |
| Operator | Exists |
| Value | [] |
| Type | String |
| Related NIST-800-53 controls | SC-12SC-13 |
| Related CRI profile controls | PR.DS-1.1PR.DS-1.2PR.DS-2.1PR.DS-2.2PR.DS-5.1 |
| Related information | Manage HMAC keys for service accounts |

### Detect enumeration of Cloud Storage buckets by service accounts

| Google control ID | GCS-CO-7.2 |
| --- | --- |
| Category | Required |
| Description | Service accounts are non-human identities that are designed for applications, and their behavior is predictable and automated. Normally, service accounts don't need to itemize buckets, as they're already mapped. Therefore, if you detect a service account attempting to retrieve a list of all Cloud Storage buckets, investigate it immediately. Reconnaissance enumeration is often used as a recon technique by a malicious actor that has gained access to the service account. |
| Applicable products | Cloud StorageCloud Audit Logs |
| Operator | == |
| Value | storage.bucket.list |
| Type | String |
| Related NIST-800-53 controls | AU-2AU-3AU-8AU-9 |
| Related CRI profile controls | DM.ED-7.1DM.ED-7.2DM.ED-7.3DM.ED-7.4PR.IP-1.4 |
| Related information | Cloud Audit Logs with Cloud Storage |

### Detect Identity and Access Management (IAM) policy modifications of Cloud Storage buckets by service accounts

| Google control ID | GCS-CO-7.3 |
| --- | --- |
| Category | Required |
| Description | Configure an alert that detects when a Cloud Storage bucket's IAM policy is modified to grant public access. This alert fires when theallUsersorallAuthenticatedUsersprincipals are added to a bucket's IAM policy. This alert is a critical, high-severity event because it can expose all data in the bucket. Investigate this alert immediately to confirm if the change was authorized or is a sign of a misconfiguration or malicious actor.In the alert, set thedata.protoPayload.serviceData.policyData.bindingDeltas.memberJSON attribute toallUsersorallAuthenticatedUsersand the action toADD. |
| Applicable products | Cloud StorageCloud Audit Logs |
| Related NIST-800-53 controls | AU-2AU-3AU-8AU-9 |
| Related CRI profile controls | DM.ED-7.1DM.ED-7.2DM.ED-7.3DM.ED-7.4PR.IP-1.4 |
| Related information | Cloud Audit Logs with Cloud Storage |

## Recommended controls based on generative AI use case

Depending on your use cases around generative AI, we recommend that you use additional
controls. These controls include data retention controls and other policy-driven
controls that are based on your enterprise policies.

### Ensure Cloud Storage bucket retention policy uses Bucket Lock

| Google control ID | GCS-CO-6.1 |
| --- | --- |
| Category | Recommended |
| Description | Depending on your regulatory requirements, ensure that each Cloud Storage bucket retention policy is locked. Set the retention period to a timeframe that meets your requirements. |
| Applicable products | Cloud Storage |
| Path | storage.buckets/retentionPolicy.isLocked |
| Operator | != |
| Value | True |
| Type | Boolean |
| Related NIST-800-53 controls | SI-12 |
| Related CRI profile controls | PR.IP-2.1PR.IP-2.2PR.IP-2.3 |
| Related information | Use and lock retention policies |

### Set lifecycle rules for the SetStorageClass action

| Google control ID | GCS-CO-6.11 |
| --- | --- |
| Category | Recommended |
| Description | Apply lifecycle rules to each Cloud Storage bucket that has aSetStorageClassaction type. |
| Applicable products | Cloud Storage |
| Path | storage.buckets/lifecycle.rule.action.type |
| Operator | == |
| Value | SetStorageClass |
| Type | String |
| Related NIST-800-53 controls | SI-12 |
| Related CRI profile controls | PR.IP-2.1PR.IP-2.2PR.IP-2.3 |
| Related information | Object Lifecycle Management |

### Set permitted regions for storage classes

| Google control ID | GCS-CO-6.12 |
| --- | --- |
| Category | Recommended |
| Description | Ensure that storage classes for the lifecycle configuration aren't within permitted regional classifications. |
| Applicable products | Cloud Storage |
| Path | storage.buckets/lifecycle.rule.action.storageClass |
| Operator | nin |
| Value | MULTI_REGIONALREGIONAL |
| Type | String |
| Related NIST-800-53 controls | SI-12 |
| Related CRI profile controls | PR.IP-2.1PR.IP-2.2PR.IP-2.3 |
| Related information | Bucket locationsObject Lifecycle Management |

### Enable lifecycle management for Cloud Storage buckets

| Google control ID | GCS-CO-6.13 |
| --- | --- |
| Category | Recommended |
| Description | Ensure that lifecycle management of Cloud Storage is enabled and configured. The lifecycle control contains the configuration for the storage lifecycle. Verify that the policies in this setting match your requirements. |
| Applicable products | Cloud Storage |
| Path | storage.buckets/lifecycle |
| Operator | Exists |
| Value | [] |
| Type | Object |
| Related NIST-800-53 controls | SI-12 |
| Related CRI profile controls | PR.IP-2.1PR.IP-2.2PR.IP-2.3 |
| Related information | Object Lifecycle Management |

### Enable lifecycle management rules for Cloud Storage buckets

| Google control ID | GCS-CO-6.14 |
| --- | --- |
| Category | Recommended |
| Description | Ensure that lifecycle management rules for Cloud Storage are enabled and configured. The rule control contains the configuration for the storage lifecycle. Verify that the policies in this setting match your requirements. |
| Applicable products | Cloud Storage |
| Path | storage.buckets/lifecycle.rule |
| Operator | Empty |
| Value | [] |
| Type | Array |
| Related NIST-800-53 controls | SI-12 |
| Related CRI profile controls | PR.IP-2.1PR.IP-2.2PR.IP-2.3 |
| Related information | Object Lifecycle Management |

### Review and evaluate temporary holds on active objects

| Google control ID | GCS-CO-6.16 |
| --- | --- |
| Category | Recommended |
| Description | Identify all objects where temporaryHold is set to TRUE and start an investigation and validation process. This evaluation is appropriate for the following use cases:Legal hold:To comply with legal requirements for storing data, temporary hold can be used to prevent the deletion of sensitive data that may be relevant to ongoing investigations or litigation.Data loss prevention:To prevent accidental deletion of important data, temporary hold can be used as a safety measure to protect critical business information.Content moderation:To review potentially sensitive or inappropriate content before it becomes publicly accessible, apply a temporary hold to content uploaded to Cloud Storage for further inspection and moderation decisions. |
| Applicable products | Cloud Storage |
| Path | storage.objects/temporaryHold |
| Operator | == |
| Value | TRUE |
| Type | Boolean |
| Related NIST-800-53 controls | SI-12 |
| Related CRI profile controls | PR.IP-2.1PR.IP-2.2PR.IP-2.3 |
| Related information | Object holds |

### Enforce retention policies on Cloud Storage buckets

| Google control ID | GCS-CO-6.17 |
| --- | --- |
| Category | Recommended |
| Description | Ensure that all the Cloud Storage buckets have a retention policy. |
| Applicable products | Cloud Storage |
| Path | storage.buckets/retentionPolicy.retentionPeriod |
| Operator | agesmaller |
| Value | [90,"DAY","AFTER","yyyy-MM-dd'T'HH:mm:ss'Z'"] |
| Type | int64 |
| Related NIST-800-53 controls | SI-12 |
| Related CRI profile controls | PR.IP-2.1PR.IP-2.2PR.IP-2.3 |
| Related information | Bucket Lock |

### Enforce classification tags for Cloud Storage buckets

| Google control ID | GCS-CO-6.18 |
| --- | --- |
| Category | Recommended |
| Description | Data classification is a foundational component of any data governance and security program. Applying a classification label with values like public, internal, confidential, or restricted to each bucket is essential.Confirm thatgoogle_storage_bucket.labelshas an expression for classification and create a violation if it doesn't. |
| Applicable products | Cloud Storage |
| Path | storage.buckets/labels.classification |
| Operator | notexists |
| Value | [] |
| Type | Extended |
| Related NIST-800-53 controls | SI-12 |
| Related CRI profile controls | PR.IP-2.1PR.IP-2.2PR.IP-2.3 |
| Related information | Tags and labels |

### Enforce log buckets for Cloud Storage buckets

| Google control ID | GCS-CO-6.3 |
| --- | --- |
| Category | Recommended |
| Description | Ensure that every Cloud Storage bucket includes a log bucket. |
| Applicable products | Cloud Storage |
| Path | storage.buckets/logging.logBucket |
| Operator | notexists |
| Value | [] |
| Type | String |
| Related NIST-800-53 controls | AU-2AU-3AU-8AU-9 |
| Related CRI profile controls | DM.ED-7.1DM.ED-7.2DM.ED-7.3DM.ED-7.4PR.IP-1.4 |
| Related information | Configure log buckets |

### Configure deletion rules for Cloud Storage buckets

| Google control ID | GCS-CO-6.5 |
| --- | --- |
| Category | Recommended |
| Description | In Cloud Storage,storage.buckets/lifecycle.rule.action.typerefers to the type of action to be taken on a specific object based on a lifecycle rule within a bucket. This configuration helps automate the management and lifecycle of your data stored in the cloud.Configure thestorage.buckets/lifecycle.rule.action.typeto ensure that objects are permanently deleted from the bucket. |
| Applicable products | Cloud Storage |
| Path | storage.buckets/lifecycle.rule.action.type |
| Operator | == |
| Value | Delete |
| Type | String |
| Related NIST-800-53 controls | SI-12 |
| Related CRI profile controls | PR.IP-2.1PR.IP-2.2PR.IP-2.3 |
| Related information | Manage object lifecycles |

### Ensure isLive condition is False for deletion rules

| Google control ID | GCS-CO-6.6 |
| --- | --- |
| Category | Recommended |
| Description | For deletion rules, ensure that theisLivecondition of the rule is set tofalse.In Cloud Storage,storage.buckets/lifecycle.rule.condition.isLiveis a boolean condition that is used in lifecycle rules to determine whether an object is considered live. This filter helps ensure that actions within a lifecycle rule are applied only to desired objects based on their live status.Use cases:Archive historical versions:Archive only non-current versions of objects to save storage costs while keeping the latest version readily accessible.Clean up deleted objects:Automate permanent deletion of objects that have been deleted by users, freeing up space in the bucket.Protect live data:Ensure that actions like setting temporary holds are applied only to live objects, preventing accidental modification of archived or deleted versions |
| Applicable products | Cloud Storage |
| Path | storage.buckets/lifecycle.rule.condition.isLive |
| Operator | == |
| Value | False |
| Type | Boolean |
| Related NIST-800-53 controls | SI-12 |
| Related CRI profile controls | PR.IP-2.1PR.IP-2.2PR.IP-2.3 |
| Related information | isLive |

### Enforce versioning for Cloud Storage buckets

| Google control ID | GCS-CO-6.7 |
| --- | --- |
| Category | Recommended |
| Description | Ensure that all Cloud Storage buckets have versioning enabled. Use cases include the following:Data protection and recovery:Protect against accidental data loss by preventing overwrites and enabling recovery of deleted or modified data.Compliance and auditing:Maintain a history of all object edits for regulatory compliance or internal auditing purposes.Version control:Track changes to files and data sets, enabling collaboration and rollback to previous versions if necessary. |
| Applicable products | Cloud Storage |
| Path | storage.buckets/versioning.enabled |
| Operator | != |
| Value | True |
| Type | Boolean |
| Related NIST-800-53 controls | SI-12 |
| Related CRI profile controls | PR.IP-2.1PR.IP-2.2PR.IP-2.3 |
| Related information | Object Versioning |

### Enforce owners for Cloud Storage buckets

| Google control ID | GCS-CO-6.8 |
| --- | --- |
| Category | Recommended |
| Description | Ensure thatgoogle_storage_bucket.labelshas an expression for an owner. |
| Applicable products | Cloud Storage |
| Path | storage.buckets/labels.owner |
| Operator | notexists |
| Value | [] |
| Type | Extended |
| Related NIST-800-53 controls | SI-12 |
| Related CRI profile controls | PR.IP-2.1PR.IP-2.2PR.IP-2.3 |
| Related information | Using bucket labels |

### Enable logging of key Cloud Storage activities

| Google control ID | GCS-CO-7.4 |
| --- | --- |
| Category | Recommended |
| Description | Enable additional logging around particular storage objects based on their use case. For example, log access to sensitive data buckets so that you can trace who gained access and when. When enabling additional logging, consider the volume of logs that you might generate. |
| Applicable products | Cloud Storage |
| Related NIST-800-53 controls | AU-2AU-3AU-8AU-9 |
| Related CRI profile controls | DM.ED-7.1DM.ED-7.2DM.ED-7.3DM.ED-7.4PR.IP-1.4 |
| Related information | Cloud Audit Logs with Cloud Storage |

## What's next

- Review [Dataflow
  controls](https://cloud.google.com/docs/security/security-best-practices-genai/dataflow-controls).
- See more [Google Cloud security best practices and guidelines for generative
  AI workloads](https://cloud.google.com/docs/security/security-best-practices-genai).

   Was this helpful?

---

# Vertex AI controls for generative AI use casesStay organized with collectionsSave and categorize content based on your preferences.

> Review the recommended Vertex AI security best practices and guidelines that aren&#39;t common to generative AI workloads on Google Cloud.

# Vertex AI controls for generative AI use casesStay organized with collectionsSave and categorize content based on your preferences.

[Vertex AI](https://cloud.google.com/vertex-ai/docs/start/introduction-unified-platform) lets
you build and use generative AI, including AI solutions, search, and
conversation, on a single platform. This document includes the best practices
and guidelines for Vertex AI when running generative AI workloads
on Google Cloud.

## Required Vertex AI controls

The following controls are strongly recommended for your Vertex AI
environment.

### Define the access mode for Vertex AI Workbench notebooks and instances

| Google control ID | VAI-CO-4.1 |
| --- | --- |
| Category | Required |
| Description | This list constraint defines the permitted access modes for Vertex AI Workbench notebooks and instances. The allow or deny list can specify multiple users usingservice-accountmode or single-user access usingsingle-usermode. |
| Applicable products | Vertex AI WorkbenchOrganization Policy Service |
| Path | constraints/ainotebooks.accessMode |
| Operator | Is |
| Value | service-accountsingle-user |
| Related NIST-800-53 controls | AC-3AC-17AC-20 |
| Related CRI profile controls | PR.AC-3.1PR.AC-3.2PR.AC-4.1PR.AC-4.2PR.AC-4.3PR.AC-6.1PR.PT-3.1PR.PT-4.1 |

### Disable file downloads on Vertex AI Workbench instances

| Google control ID | VAI-CO-4.2 |
| --- | --- |
| Category | Required |
| Description | Theainotebooks.disableFileDownloadsboolean constraint prevents you from creating Vertex AI Workbench instances with the file download option enabled. By default, you can enable the file download option on any Vertex AI Workbench instance. |
| Applicable products | Organization Policy ServiceVertex AI Workbench |
| Path | constraints/ainotebooks.disableFileDownloads |
| Operator | Is |
| Value | True |
| Type | Boolean |
| Related NIST-800-53 controls | AC-3AC-17AC-20 |
| Related CRI profile controls | PR.AC-3.1PR.AC-3.2PR.AC-4.1PR.AC-4.2PR.AC-4.3PR.AC-6.1PR.PT-3.1PR.PT-4.1 |

### Disable root access on Vertex AI Workbench user-managed notebooks and instances

| Google control ID | VAI-CO-4.3 |
| --- | --- |
| Category | Required |
| Description | Theainotebooks.disableRootAccessboolean constraint prevents you from creating Vertex AI Workbench user-managed notebooks and instances with root access enabled. By default, Vertex AI Workbench user-managed notebooks and instances can have root access enabled. |
| Applicable products | Organization Policy ServiceVertex AI Workbench |
| Path | constraints/ainotebooks.disableRootAccess |
| Operator | Is |
| Value | True |
| Type | Boolean |
| Related NIST-800-53 controls | AC-3AC-17AC-20 |
| Related CRI profile controls | PR.AC-3.1PR.AC-3.2PR.AC-4.1PR.AC-4.2PR.AC-4.3PR.AC-6.1PR.PT-3.1PR.PT-4.1 |

### Disable terminal on Vertex AI Workbench instances

| Google control ID | VAI-CO-4.4 |
| --- | --- |
| Category | Required |
| Description | Theainotebooks.disableTerminalboolean constraint prevents you from creating Vertex AI Workbench instances with the terminal enabled. By default, you can enable the terminal on Vertex AI Workbench instances. |
| Applicable products | Organization Policy ServiceVertex AI Workbench |
| Path | constraints/ainotebooks.disableTerminal |
| Operator | Is |
| Value | True |
| Type | Boolean |
| Related NIST-800-53 controls | AC-3AC-17AC-20 |
| Related CRI profile controls | PR.AC-3.1PR.AC-3.2PR.AC-4.1PR.AC-4.2PR.AC-4.3PR.AC-6.1PR.PT-3.1PR.PT-4.1 |

### Restrict environment options on Vertex AI Workbench notebooks and instances

| Google control ID | VAI-CO-4.5 |
| --- | --- |
| Category | Required |
| Description | Theainotebooks.environmentOptionslist constraint defines the VM and container image options that you can select when creating Vertex AI Workbench notebooks and instances. You must explicitly specify the options that you want to allow or deny.The expected format for VM instances is:ainotebooks-vm/PROJECT_ID/IMAGE_TYPE/CONSTRAINED_VALUE. ReplaceIMAGE_TYPEwithimage-familyorimage-nameFor example:ainotebooks-vm/deeplearning-platform-release/image-family/pytorch-1-4-cpu ainotebooks-vm/deeplearning-platform-release/image-name/pytorch-latest-cpu-20200615The expected format for container images is:ainotebooks-container/CONTAINER_REPOSITORY:TAGFor example:ainotebooks-container/gcr.io/deeplearning-platform-release/tf-gpu.1-15:latest ainotebooks-container/gcr.io/deeplearning-platform-release/tf-gpu.1-15:m48 |
| Applicable products | Organization Policy ServiceVertex AI Workbench |
| Path | constraints/ainotebooks.environmentOptions |
| Operator | Is |
| Type | List |
| Related NIST-800-53 controls | AC-3AC-17AC-20 |
| Related CRI profile controls | PR.AC-3.1PR.AC-3.2PR.AC-4.1PR.AC-4.2PR.AC-4.3PR.AC-6.1PR.PT-3.1PR.PT-4.1 |

### Enforce automatic scheduled upgrades on Vertex AI Workbench user-managed notebooks and instances

| Google control ID | VAI-CO-4.6 |
| --- | --- |
| Category | Required |
| Description | Theainotebooks.requireAutoUpgradeScheduleboolean constraint prevents you from creating Vertex AI Workbench user-managed notebooks and instances without an automatic upgrade schedule.To define a cron schedule for the automatic upgrades, use thenotebook-upgrade-schedulemetadata flag. For example:--metadata=notebook-upgrade-schedule="00 19 * * MON" |
| Applicable products | Organization Policy ServiceVertex AI Workbench |
| Path | constraints/ainotebooks.requireAutoUpgradeSchedule |
| Operator | Is |
| Value | True |
| Type | Boolean |
| Related NIST-800-53 controls | MA-2MA-3 |
| Related CRI profile controls | PR.AC-3.1PR.AC-3.2PR.AC-4.1PR.AC-4.2PR.AC-4.3PR.AC-6.1PR.PT-3.1PR.PT-4.1 |

### Restrict public access on new Vertex AI Workbench notebooks and instances

| Google control ID | VAI-CO-4.7 |
| --- | --- |
| Category | Required |
| Description | This boolean constraint restricts access from public IP addresses to Vertex AI Workbench notebooks and instances. By default, public IP addresses can access Vertex AI Workbench notebooks and instances. |
| Applicable products | Organization Policy ServiceVertex AI Workbench |
| Path | constraints/ainotebooks.restrictPublicIp |
| Operator | is |
| Value | True |
| Type | Boolean |
| Related NIST-800-53 controls | AC-3AC-17AC-20SC-7SC-8 |
| Related CRI profile controls | PR.AC-3.1PR.AC-3.2PR.AC-4.1PR.AC-4.2PR.AC-4.3PR.AC-6.1PR.DS-2.1PR.DS-2.2PR.DS-5.1PR.PT-3.1PR.PT-4.1DE.CM-1.1DE.CM-1.2DE.CM-1.3DE.CM-1.4 |

### Restrict VPC networks on Vertex AI Workbench instances

| Google control ID | VAI-CO-4.8 |
| --- | --- |
| Category | Required |
| Description | Theainotebooks.restrictVpcNetworkslist constraint defines the VPC networks that a user can select when creating Vertex AI Workbench instances. By default, a Vertex AI Workbench instance can be created in any VPC network.Use one of the following formats to define an allowed or denied list of networks:under:organizations/ORGANIZATION_IDunder:folders/FOLDER_IDunder:projects/PROJECT_IDprojects/PROJECT_ID/global/networks/NETWORK_NAME |
| Applicable products | Organization Policy ServiceVertex AI Workbench |
| Path | constraints/ainotebooks.restrictVpcNetworks |
| Operator | is |
| Type | List |
| Related NIST-800-53 controls | AC-3AC-17AC-20SC-7SC-8 |
| Related CRI profile controls | PR.AC-3.1PR.AC-3.2PR.AC-4.1PR.AC-4.2PR.AC-4.3PR.AC-5.1PR.AC-5.2PR.AC-6.1PR.DS-2.1PR.DS-2.2PR.DS-5.1PR.PT-3.1PR.PT-4.1DE.CM-1.1DE.CM-1.2DE.CM-1.3DE.CM-1.4 |

## What's next

- Review [Artifact Registry
  controls](https://cloud.google.com/docs/security/security-best-practices-genai/artifact-registry-controls).
- See more [Google Cloud security best practices and guidelines for generative
  AI workloads](https://cloud.google.com/docs/security/security-best-practices-genai).

---

# VPC controls for generative AI use casesStay organized with collectionsSave and categorize content based on your preferences.

> Review the recommended Virtual Private Cloud security best practices and guidelines that aren&#39;t common to generative AI workloads on Google Cloud.

# VPC controls for generative AI use casesStay organized with collectionsSave and categorize content based on your preferences.

This document includes the best practices and guidelines for
Virtual Private Cloud (VPC) when running generative AI workloads on
Google Cloud. Use [VPC](https://cloud.google.com/vpc/docs/overview) with
Vertex AI to isolate your AI resources from the internet in a secure
environment. This network configuration helps protect sensitive data and models
from unauthorized access and potential cyberattacks.

You can define granular firewall rules and access controls within your VPC
network to restrict traffic and only allow authorized connections to specific
resources.

Organize your Vertex AI resources into separate VPC networks
based on function or security requirements. This type of organization helps
isolate resources and prevents unauthorized access between different projects or
teams. You can create dedicated VPC networks for sensitive workloads, such as
training models with confidential data, ensuring that only authorized users and
services have network access.

You can use Cloud VPN or Cloud Interconnect to establish a secure network
connection between your on-premises infrastructure and your
Vertex AI environment. Cloud VPN or
Cloud Interconnect help enable seamless data transfer and communication
between your private network and Google Cloud resources. Consider this
integration for scenarios like accessing on-premises data for model training or
deploying models to on-premises resources for inference.

## Required VPC controls

The following controls are strongly recommended when using
VPC.

### Block default network creation

| Google control ID | VPC-CO-6.1 |
| --- | --- |
| Category | Required |
| Description | Thecompute.skipDefaultNetworkCreationboolean constraint skips the creation of the default network and related resources when creating Google Cloud projects. By default, a network is automatically created with firewall rules and network configurations which might not be considered secure. |
| Applicable products | Organization Policy ServiceVirtual Private Cloud (VPC) |
| Path | constraints/compute.skipDefaultNetworkCreation |
| Value | True |
| Type | Boolean |
| Related NIST-800-53 controls | SC-7SC-8 |
| Related CRI profile controls | PR.AC-5.1PR.AC-5.2PR.DS-2.1PR.DS-2.2PR.DS-5.1PR.PT-4.1DE.CM-1.1DE.CM-1.2DE.CM-1.3DE.CM-1.4 |
| Related information | Organization policy constraints |

### Define list of VM instances that are permitted external IP addresses

| Google control ID | VPC-CO-6.2 |
| --- | --- |
| Category | Required |
| Description | Thecompute.vmExternalIpAccesslist constraint defines the set of Compute Engine VM instances that can have external IP addresses. This constraint isn't retroactive. |
| Applicable products | Organization Policy ServiceVirtual Private Cloud (VPC)Compute Engine |
| Path | constraints/compute.vmExternalIpAccess |
| Operator | = |
| Value | The list of VM instances in your organization that can have external IP addresses. |
| Type | List |
| Related NIST-800-53 controls | SC-7SC-8 |
| Related CRI profile controls | PR.AC-5.1PR.AC-5.2PR.DS-2.1PR.DS-2.2PR.DS-5.1PR.PT-4.1DE.CM-1.1DE.CM-1.2DE.CM-1.3DE.CM-1.4 |
| Related information | Restrict external IP addresses to specific instances |

### Define VM instances that can enable IP forwarding

| Google control ID | VPC-CO-6.3 |
| --- | --- |
| Category | Required |
| Description | Thecompute.vmCanIpForwardconstraint defines the VM instances that can enable IP forwarding. By default, any VM can enable IP forwarding in any virtual network. Specify VM instances using one of the following formats:under:organizations/ORGANIZATION_IDunder:folders/FOLDER_IDunder:projects/PROJECT_IDprojects/PROJECT_ID/zones/ZONE/instances/INSTANCE_NAME.This constraint isn't retroactive. |
| Applicable products | Organization Policy ServiceVirtual Private Cloud (VPC)Compute Engine |
| Path | constraints/compute.vmCanIpForward |
| Operator | = |
| Value | Your list of VM instances that can enable IP forwarding. |
| Type | List |
| Related NIST-800-53 controls | SC-7SC-8 |
| Related CRI profile controls | PR.AC-5.1PR.AC-5.2PR.DS-2.1PR.DS-2.2PR.DS-5.1PR.PT-4.1DE.CM-1.1DE.CM-1.2DE.CM-1.3DE.CM-1.4 |
| Related information | RecommendationsEnable IP forwarding for instances |

### Disable VM-nested virtualization

| Google control ID | VPC-CO-6.6 |
| --- | --- |
| Category | Required |
| Description | Thecompute.disableNestedVirtualizationboolean constraint disables hardware-accelerated nested virtualization for Compute Engine VMs. |
| Applicable products | Organization Policy ServiceVirtual Private Cloud (VPC)Compute Engine |
| Path | constraints/compute.disableNestedVirtualization |
| Operator | Is |
| Value | True |
| Type | Boolean |
| Related NIST-800-53 controls | SC-7SC-8 |
| Related CRI profile controls | PR.AC-5.1PR.AC-5.2PR.DS-2.1PR.DS-2.2PR.DS-5.1PR.PT-4.1DE.CM-1.1DE.CM-1.2DE.CM-1.3DE.CM-1.4 |
| Related information | Manage the nested virtualization constraint |

## What's next

- See more [Google Cloud security best practices and guidelines for generative
  AI workloads](https://cloud.google.com/docs/security/security-best-practices-genai).

   Was this helpful?

---

# Google Cloud security best practices and guidelines for generative AI workloadsStay organized with collectionsSave and categorize content based on your preferences.

> Overview of security best practices recommended by Google for genAI workloads.

# Google Cloud security best practices and guidelines for generative AI workloadsStay organized with collectionsSave and categorize content based on your preferences.

You can use Google Cloud security best practices and guidelines for
generative AI to discover and implement security features for your generative AI
workloads and supporting services on
Google Cloud.

The security best practices are a Google-driven supplementary guide to existing
regulatory and security practices in industries such as the financial services
sector. The Google Cloud best practices and guidelines focus on
foundational workload security controls and unique considerations that are
specific to generative AI workloads.

These security best practices are intended to help chief information security
officers (CISO), security practitioners, and risk and compliance officers adopt
and deploy workloads in Google Cloud, while focusing on safety, security,
and compliance. We align our recommendations with the requirements of the
[National Institute of Standards and Technology (NIST)
800-53](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final) and [Cyber Risk
Institute (CRI)](https://cyberriskinstitute.org/) frameworks.

These best practices also support the [shared fate
model](https://cloud.google.com/architecture/framework/security/shared-responsibility-shared-fate),
where we strive to collaborate with industries to build a more secure and
resilient cloud infrastructure for various workloads. The shared fate model
includes deployment, operations, and risk transfer. Therefore, these
recommendations focus on workload deployment and operations, particularly in
relation to compliance.

We understand that implementing compliance and security isn't a simple
exercise. For additional help, [contact Google Cloud
Security](https://cloud.google.com/contact/security).

## Structure for security best practices

The security best practices are structured as *controls* that you can review and
implement. The controls are as follows:

- [Recommended IAM
  roles](https://cloud.google.com/docs/security/security-best-practices-genai/recommended-iam-groups):
  Recommendations for IAM roles to assign to user groups in your
  organization.
- [Common
  controls:](https://cloud.google.com/docs/security/security-best-practices-genai/common-genai-controls)
  These best practices apply to all generative AI workloads in
  Google Cloud.
- **Service-specific controls**: These best practices apply to generative AI
  workloads that make use of the following Google Cloud services:
  - [Vertex AI controls](https://cloud.google.com/docs/security/security-best-practices-genai/vertex-ai-controls)
  - [Artifact Registry controls](https://cloud.google.com/docs/security/security-best-practices-genai/artifact-registry-controls)
  - [BigQuery controls](https://cloud.google.com/docs/security/security-best-practices-genai/bigquery-controls)
  - [Cloud Billing controls](https://cloud.google.com/docs/security/security-best-practices-genai/billing-controls)
  - [Cloud Build controls](https://cloud.google.com/docs/security/security-best-practices-genai/build-controls)
  - [Cloud DNS controls](https://cloud.google.com/docs/security/security-best-practices-genai/dns-controls)
  - [Cloud Identity controls](https://cloud.google.com/docs/security/security-best-practices-genai/cloud-identity-controls)
  - [Cloud Run functions controls](https://cloud.google.com/docs/security/security-best-practices-genai/cloud-run-functions-controls)
  - [Cloud Storage controls](https://cloud.google.com/docs/security/security-best-practices-genai/storage-controls)
  - [Dataflow controls](https://cloud.google.com/docs/security/security-best-practices-genai/dataflow-controls)
  - [Identity and Access Management controls](https://cloud.google.com/docs/security/security-best-practices-genai/iam-controls)
  - [Organization Policy Service controls](https://cloud.google.com/docs/security/security-best-practices-genai/orgpolicy-controls)
  - [Pub/Sub controls](https://cloud.google.com/docs/security/security-best-practices-genai/pubsub-controls)
  - [Resource Manager controls](https://cloud.google.com/docs/security/security-best-practices-genai/resource-manager-controls)
  - [Secret Manager controls](https://cloud.google.com/docs/security/security-best-practices-genai/secret-manager-controls)
  - [Security Command Center controls](https://cloud.google.com/docs/security/security-best-practices-genai/scc-controls)
  - [Virtual Private Cloud controls](https://cloud.google.com/docs/security/security-best-practices-genai/vpc-controls)

Each recommendation is auditable and ensures a baseline of security controls
are met.

## Control categories

Control categories are **Required**, **Recommended**, or **Optional**. The
categories help identify key activities that we highly recommend you do,
activities that we highly advise you consider, and activities that you might
consider based on your specific requirements and goals.

The following table describes these categories.

| Category | Description |
| --- | --- |
| Required | Implement these guidelines for your Google Cloud environment. |
| Recommended | Implement these guidelines based on use cases such as monitoring
sensitive data inside the generative AI workloads if your environment includes that type of data. |
| Optional | Consider additional guidelines based on your use case and risk appetite. |

## Sample generative AI architecture

The following diagram shows the Google Cloud services that are present in
a typical generative AI architecture that uses Vertex AI.

![Sample architecture for generative AI workloads that use Vertex AI.](https://docs.cloud.google.com/docs/security/images/sec-genai-architecture.svg)

## What's next

- Review [Recommended IAM
  roles](https://cloud.google.com/docs/security/security-best-practices-genai/recommended-iam-groups).

   Was this helpful?
