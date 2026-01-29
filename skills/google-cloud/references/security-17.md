# Cloud Build controls for generative AI use casesStay organized with collectionsSave and categorize content based on your preferences. and more

# Cloud Build controls for generative AI use casesStay organized with collectionsSave and categorize content based on your preferences.

> Review the recommended Google Cloud security best practices and guidelines that aren&#39;t specific to genAI workloads that use Cloud Build.

# Cloud Build controls for generative AI use casesStay organized with collectionsSave and categorize content based on your preferences.

This document includes the best practices and guidelines for Cloud Build
when running generative AI workloads on Google Cloud. Use
[Cloud Build](https://cloud.google.com/build/docs/overview) with Vertex AI to build,
test, and deploy a serverless CI/CD platform on Google Cloud.

Consider the following use cases for Cloud Build with Vertex AI:

- **Automate ML pipeline builds**: Cloud Build lets you automate the
  building and testing of your ML pipelines defined in
  Vertex AI Pipelines. This automation helps you build and deploy your
  models faster and with greater consistency.
- **Build custom container images for deployment**: Cloud Build can
  build
  custom container images for your model-serving environments. Cloud Build
  lets you package your model code, dependencies, and runtime environment into
  a single image that you can deploy to Vertex AI Inference for serving
  predictions.
- **Integrate with CI/CD workflows**: Cloud Build lets you automate
  the build
  and deployment of your ML models in your CI/CD workflows. This automation
  ensures that your models are up-to-date and deployed to production.
- **Trigger builds based on code changes**: Cloud Build can
  automatically
  trigger builds when changes are made to your model code or pipeline
  definition. This automation helps to ensure that your models are built with
  the latest code and that any changes are automatically deployed to
  production.
- **Get scalable and secure infrastructure**: Cloud Build uses
  Google Cloud
  scalable and secure infrastructure to build and deploy your models. This
  scalability means you don't need to worry about managing your own
  infrastructure and can focus on developing your models.
- **Support for various programming languages**: Cloud Build supports
  various
  programming languages, including Python, Java, Go, and Node.js. This support
  lets you build your models using the language of your choice.
- **Use prebuilt build steps**: To help simplify the build process,
  Cloud Build offers prebuilt build steps for common ML tasks, such
  as installing
  dependencies, running tests, and pushing images to container registries.
- **Create custom build steps**: You can define your own custom build steps in
  Cloud Build to execute any arbitrary code during the build process.
- **Build artifacts for other Vertex AI services**:
  Cloud Build can build
  artifacts for other Vertex AI services such as Vertex AI Feature Store and
  Vertex AI Data Labeling. This flexibility helps you build a complete ML
  workflow on Google Cloud.
- **Realize a cost-effective solution**: Cloud Build offers a
  pay-as-you-go
  pricing model, so you only pay for the resources you use.

## Required Cloud Build controls

The following controls are strongly recommended when using
Cloud Build.

### Define permitted private pools

| Google control ID | CBD-CO-6.1 |
| --- | --- |
| Category | Required |
| Description | Thecloudbuild.allowedWorkerPoolslist constraint lets you define the permitted private pools that you can use within your organization, folder, or project.Use one of the following formats to define an allowed or denied list of Worker Pools:under:organizations/ORGANIZATION_IDunder:folders/FOLDER_IDunder:projects/PROJECT_IDprojects/PROJECT_ID/locations/REGION/workerPools/WORKER_POOL_ID |
| Applicable products | Organization Policy ServiceCloud Build |
| Path | constraints/cloudbuild.allowedWorkerPools |
| Operator | = |
| Type | String |
| Related NIST-800-53 controls | AC-3AC-5AC-6AC-12AC-17AC-20 |
| Related CRI profile controls | PR.AC-3.1PR.AC-3.2PR.AC-4.1PR.AC-4.2PR.AC-4.3PR.AC-6.1PR.AC-7.1PR.AC-7.2PR.PT-3.1PR-PT-4.1 |
| Related information | Enforcing the usage of private pools |

### Define which external services can invoke build triggers

| Google control ID | CBD-CO-6.2 |
| --- | --- |
| Category | Required |
| Description | Thecloudbuild.allowedIntegrationsconstraint defines which external services (for example, GitHub) can invoke build triggers. For example, if your build trigger listens for changes to a GitHub repository and GitHub is denied in this constraint, your trigger won't run. You can specify any number of allowed or denied values for your organization or project. |
| Applicable products | Organization Policy ServiceCloud Build |
| Path | constraints/cloudbuild.allowedIntegrations |
| Operator | = |
| Type | List |
| Related NIST-800-53 controls | AC-3AC-12AC-17AC-20 |
| Related CRI profile controls | PR.AC-3.1PR.AC-3.2PR.AC-4.1PR.AC-4.2PR.AC-4.3PR.AC-6.1PR.AC-7.1PR.AC-7.2PR.PT-3.1PR-PT-4.1 |
| Related information | Gate builds on organization policy |

### Define permitted external IP addresses for VM instances

| Google control ID | CBD-CO-6.3 |
| --- | --- |
| Category | Required |
| Description | Thecompute.vmExternalIpAccesslist constraint lets you restrict external access to virtual machines by not assigning external IP addresses. Configure this list constraint to deny all external IP addresses to virtual machines. |
| Applicable products | Organization Policy ServiceCloud Build |
| Path | compute.vmExternalIpAccess |
| Operator | = |
| Value | Deny All |
| Type | List |
| Related NIST-800-53 controls | AC-3AC-12AC-17AC-20 |
| Related CRI profile controls | PR.AC-3.1PR.AC-3.2PR.AC-4.1PR.AC-4.2PR.AC-4.3PR.AC-6.1PR.AC-7.1PR.AC-7.2PR.PT-3.1PR-PT-4.1 |
| Related information | Restrict external IP addresses to specific instances |

## What's next

- Review [Cloud DNS
  controls](https://cloud.google.com/docs/security/security-best-practices-genai/dns-controls).
- See more [Google Cloud security best practices and guidelines for generative
  AI workloads](https://cloud.google.com/docs/security/security-best-practices-genai).

   Was this helpful?

---

# Cloud Identity controls for generative AI use casesStay organized with collectionsSave and categorize content based on your preferences.

> Review the recommended Google Cloud security best practices and guidelines that aren&#39;t specific to genAI workloads that use Cloud Identity.

# Cloud Identity controls for generative AI use casesStay organized with collectionsSave and categorize content based on your preferences.

This document includes the best practices and guidelines for Cloud Build
when running generative AI workloads on Google Cloud. Use
[Cloud Identity](https://cloud.google.com/identity/docs/overview) with Vertex AI to unify identity, access, application, and management for Google Cloud.

## Required Cloud Identity controls

The following controls are strongly recommended when using
Cloud Identity.

### Enable two-step verification for super admin accounts

| Google control ID | CI-CO-6.1 |
| --- | --- |
| Category | Required |
| Description | Google recommends Titan Security Keys for 2-step verification (2SV) for super admin accounts. However, for use cases where this isn't possible, we recommend using another security key as an alternative. |
| Applicable products | Cloud IdentityTitan Security Keys |
| Related NIST-800-53 controls | IA-2IA-4IA-5IA-7 |
| Related CRI profile controls | PR.AC-1.1PR.AC-1.2PR.AC-1.3PR.AC-6.1PR.AC-7.1PR.AC-7.2 |
| Related information | Deploy 2-Step Verification |

### Enforce two-step verification on the super admin organization unit

| Google control ID | CI-CO-6.2 |
| --- | --- |
| Category | Required |
| Description | Enforce 2-step verification (2SV) for a specific organization unit (OU) or the entire organization. We recommend that you create an OU for super admins and enforce 2SV on that OU. |
| Applicable products | Cloud Identity |
| Related NIST-800-53 controls | IA-2IA-4IA-5IA-7 |
| Related CRI profile controls | PR.AC-1.1PR.AC-1.2PR.AC-1.3PR.AC-6.1PR.AC-7.1PR.AC-7.2 |
| Related information | Add an organizational unitMove users to an organizational unit |

### Create an exclusive email address for the primary super admin

| Google control ID | CI-CO-6.4 |
| --- | --- |
| Category | Required |
| Description | Create an email address that's not specific to a particular user as the primary Cloud Identity super admin account. |
| Applicable products | Cloud Identity |
| Related NIST-800-53 controls | IA-2IA-4IA-5 |
| Related CRI profile controls | PR.AC-1.1PR.AC-1.2PR.AC-1.3PR.AC-6.1PR.AC-7.1PR.AC-7.2 |
| Related information | Create Cloud Identity user accounts |

### Send audit logs to Google Cloud

| Google control ID | CI-CO-6.5 |
| --- | --- |
| Category | Required |
| Description | You can share data from your Google Workspace, Cloud Identity, or Essentials account with services in Google Cloud. Google Workspace collects login logs, administrator logs, and group logs. Access the shared data through the Cloud Audit Logs. |
| Applicable products | Google WorkspaceCloud Logging |
| Related NIST-800-53 controls | AC-2AC-3AC-8AC-9 |
| Related CRI profile controls | DM.ED-7.1DM.ED-7.2DM.ED-7.3DM.ED-7.4 |
| Related information | Audit logs for Google WorkspaceShare data with Google Cloud services |

### Create backup super admin accounts

| Google control ID | CI-CO-6.7 |
| --- | --- |
| Category | Required |
| Description | Create one or two backup super admin accounts. As a general rule, don't use super admin accounts for day-to-day management tasks. Have only two to three super admin accounts for your organization. |
| Applicable products | Google Workspace |
| Related NIST-800-53 controls | IA-2IA-4IA-5 |
| Related CRI profile controls | PR.AC-1.1PR.AC-1.2PR.AC-1.3PR.AC-6.1PR.AC-7.1PR.AC-7.2 |

## Recommended cloud controls

We recommend that you apply the following Cloud Identity controls to your
Google Cloud environment, regardless of your specific use case.

### Block access to Cloud Shell for Cloud Identity managed user accounts

| Google control ID | CI-CO-6.8 |
| --- | --- |
| Category | Recommended |
| Description | To avoid granting excessive access to Google Cloud, block access to Cloud Shell for Cloud Identity managed user accounts. |
| Applicable products | Cloud IdentityCloud Shell |
| Related NIST-800-53 controls | SC-7SC-8 |
| Related CRI profile controls | PR.AC-5.1PR.AC-5.2PR.DS-2.1PR.DS-2.2PR.DS-5.1PR.PT-4.1DE.CM-1.1DE.CM-1.2DE.CM-1.3DE.CM-1.4 |
| Related information | Disable Cloud Shell for managed user accounts |

## Optional controls

You can optionally implement the following Cloud Identity controls based on your
organization's requirements.

### Block account self-recovery for super admin accounts

| Google control ID | CI-CO-6.3 |
| --- | --- |
| Category | Optional |
| Description | An attacker could use the self-recovery process to reset super admin passwords. To mitigate the security risks associated with Signaling System 7 (SS7) attacks, SIM Swap attacks, or other phishing attacks, we recommend that you turn off this feature. To turn off the feature, go to the account recovery settings in the Google Admin console. |
| Applicable products | Cloud IdentityGoogle Workspace |
| Related NIST-800-53 controls | IA-2IA-4IA-5 |
| Related CRI profile controls | PR.AC-1.1PR.AC-1.2PR.AC-1.3PR.AC-6.1PR.AC-7.1PR.AC-7.2 |
| Related information | Manage a user's security settings |

### Turn off unused Google services

| Google control ID | CI-CO-6.6 |
| --- | --- |
| Category | Optional |
| Description | In general, we recommend turning off the services that you won't use. |
| Applicable products | Cloud Identity |
| Path | http://admin.google.com > Apps > Additional Google Services |
| Operator | Setting |
| Value | False |
| Related NIST-800-53 controls | SC-7SC-8 |
| Related CRI profile controls | PR.AC-5.1PR.AC-5.2PR.DS-2.1PR.DS-2.2PR.DS-5.1PR.PT-4.1DE.CM-1.1DE.CM-1.2DE.CM-1.3DE.CM-1.4 |
| Related information | Turn on or off additional Google services |

## What's next

- Review [Cloud Run functions
  controls](https://cloud.google.com/docs/security/security-best-practices-genai/cloud-run-functions-controls).
- See more [Google Cloud security best practices and guidelines for generative
  AI workloads](https://cloud.google.com/docs/security/security-best-practices-genai).

   Was this helpful?

---

# Cloud Run functions controls for generative AI use casesStay organized with collectionsSave and categorize content based on your preferences.

> Review the recommended Google Cloud security best practices and guidelines that aren&#39;t specific to genAI workloads that use Cloud Run functions.

# Cloud Run functions controls for generative AI use casesStay organized with collectionsSave and categorize content based on your preferences.

This document includes the best practices and guidelines for Cloud Run functions when running generative AI workloads on Google Cloud. Use
[Cloud Run functions](https://cloud.google.com/run/docs/functions-with-run) with Vertex AI to automate tasks, serve predictions, trigger training jobs, integrate with other services, and build event-driven ML pipelines.

Consider the following use cases for Cloud Run functions with Vertex AI:

- **Ability to preprocess and post-process data**: Cloud Run
  functions can preprocess data before sending it to your
  Vertex AI model for training or prediction. For example, a
  function can clean and normalize data, or extract features from it. Similarly,
  Cloud Run functions can post-process the output of your
  Vertex AI model. For example, a function can format the output
  data, or to send it to another service for further analysis.
- **Automatic triggers for Vertex AI training jobs**: To automate the training
  of Vertex AI models, you can trigger Cloud Run
  functions using events from various Google Cloud services, such as
  Cloud Storage, Pub/Sub, and Cloud Scheduler. For example, you can
  create a function that is triggered when a new file is uploaded to
  Cloud Storage. This function can start a Vertex AI
  training job to train your model on the new data.
- **Ability to serve predictions**: Cloud Run functions can serve
  predictions from your Vertex AI models, letting you create an
  API endpoint for your model without having to manage any infrastructure. For
  example, you can write a function that takes an image as input, and outputs a
  prediction from your
  Vertex AI image classification model. You can then deploy this function as an HTTP API endpoint.
- **Event-driven ML workflows**: You can use Cloud Run functions
  to build event-driven ML workflows. For example, a function can trigger a
  Vertex AI prediction job when a new record is added to a
  Pub/Sub topic. This function lets you process data in real time
  and take action based on your model predictions.
- **Integration with other services**: You can integrate
  Cloud Run functions with other Google Cloud services,
  such as Cloud Storage, BigQuery, and Cloud
  Firestore. Integration lets you build complex ML pipelines that connect
  different services together.
- **Cost scaling**: Cloud Run functions lets you only pay for the
  resources that your function uses while it's running. Additionally,
  Cloud Run functions are automatically scaled to meet demand, so
  that you maintain appropriate resources during peak traffic.

## Required Cloud Run functions controls

The following controls are strongly recommended when using
Cloud Run functions.

### Require VPC connector for Cloud Run functions

| Google control ID | CF-CO-4.4 |
| --- | --- |
| Category | Required |
| Description | Thecloudfunctions.requireVPCConnectorboolean constraint requires that administrators specify a Serverless VPC Access connector when they deploy a Cloud Run function. When enforced, functions must specify a connector. |
| Applicable products | Organization Policy ServiceCloud Run functions |
| Path | constraints/cloudfunctions.requireVPCConnector |
| Operator | = |
| Value | True |
| Type | Boolean |
| Related NIST-800-53 controls | SC-7SC-8 |
| Related CRI profile controls | PR.AC-5.1PR.AC-5.2PR.DS-2.1PR.DS-2.2PR.DS-5.1PR.PT-4.1DE.CM-1.1DE.CM-1.2DE.CM-1.3DE.CM-1.4 |
| Related information | Connect to a VPC network |

## What's next

- Review [Cloud Storage
  controls](https://cloud.google.com/docs/security/security-best-practices-genai/storage-controls).
- See more [Google Cloud security best practices and guidelines for generative
  AI workloads](https://cloud.google.com/docs/security/security-best-practices-genai).

   Was this helpful?

---

# Common controls for generative AI use casesStay organized with collectionsSave and categorize content based on your preferences.

> Review the recommended Google Cloud security best practices and guidelines that are common to all workloads on Google Cloud.

# Common controls for generative AI use casesStay organized with collectionsSave and categorize content based on your preferences.

This document describes the common controls that create a baseline security
environment for generative AI workloads in Google Cloud. These
controls help ensure consistent and secure use of the
Google Cloud environment. We recommend that you apply them to your
environment before deploying production services.

These controls are meant to provide you with a starting point only. You can
adapt and add organizational-specific controls as required by your
organization's security policies. In addition, consider additional controls
based on the specific workloads and sensitive data that you have on
Google Cloud.

## Required common controls

The following controls are strongly recommended for your Google Cloud
environment.

### Restrict TLS versions supported by Google APIs

| Google control ID | COM-CO-1.1 |
| --- | --- |
| Category | Required |
| Description | Google Cloud supports multiple TLS protocol versions. To meet compliance requirements, you might want to deny handshake requests from clients that use older TLS versions.To configure this control, use theRestrict TLS Versions(gcp.restrictTLSVersion) organization policy constraint. You can apply this constraint to organizations, folders, or projects in the resource hierarchy. TheRestrict TLS Versionsconstraint uses a deny list, which denies explicit values and allows all others. An error occurs if you try to use an allow list.Due to the behavior of organization policy hierarchy evaluation, the TLS version restriction applies to the specified resource node and all of its folders and projects (children). For example, if you deny TLS version 1.0 for an organization, it is also denied for all children that descend from that organization.You can override the inherited TLS version restriction by updating the organization policy on a child resource. For example, if your organization policy denies TLS 1.0 at the organization level, you can remove the restriction for a child folder by setting a separate organization policy on that folder. If the folder has any children, the folder's policy will also be applied on each child resource due to policy inheritance.To further restrict the TLS version to TLS 1.3 only, you can set this policy to also restrict TLS version 1.2. You must implement this control on applications that you host inside of Google Cloud. For example, at the organization level, set:["TLS_VERSION_1","TLS_VERSION_1.1","TLS_VERSION_1.2"] |
| Applicable products | All; managed by Organization Policy Service |
| Path | gcp.restrictTLSVersion |
| Operator | == |
| Value | TLS_VERSION_1TLS_VERSION_1.1 |
| Type | String |
| Compliance Manager control ID | RESTRICT_LEGACY_TLS_VERSIONS |
| Related NIST-800-53 controls | SC-8SC-13 |
| Related CRI profile controls | PR.DS-2.1PR.DS-2.2PR.DS-5.1 |
| Related information | Restrict TLS versions |

### Encrypt data at rest in Google Cloud

| Google control ID | COM-CO-2.1 |
| --- | --- |
| Category | Required (default) |
| Description | All data in Google Cloud is encrypted at rest by default using NIST-approved algorithms. |
| Applicable products | Google Cloud default |
| Related NIST-800-53 controls | SC-28 |
| Related CRI profile controls | PR.DS-1.1PR.DS-1.2 |
| Related information | Default encryption at rest |

### Use NIST-approved algorithms for encryption and decryption

| Google control ID | COM-CO-2.4 |
| --- | --- |
| Category | Required |
| Description | Ensure that Cloud Key Management Service (Cloud KMS) only uses NIST-approved algorithms to store sensitive keys in the environment. This control ensures secure key usage by only NIST-approved algorithms and security. TheCryptoKeyVersionAlgorithmfield is a provided allowlist.Remove algorithms that don't comply with your organization's policies. |
| Applicable products | Cloud KMS |
| Path | cloudkms.projects.locations.keyRings.cryptoKeys/versionTemplate.algorithm |
| Operator | in |
| Value | RSA_SIGN_PSS_2048_SHA256RSA_SIGN_PSS_3072_SHA256RSA_SIGN_PSS_4096_SHA256RSA_DECRYPT_OAEP_2048_SHA256RSA_DECRYPT_OAEP_4096_SHA256RSA_DECRYPT_OAEP_2048_SHA1RSA_DECRYPT_OAEP_4096_SHA1 |
| Type | String |
| Related NIST-800-53 controls | SC-12SC-13 |
| Related CRI profile controls | PR.DS-1.1PR.DS-1.2PR.DS-2.1PR.DS-2.2PR.DS-5.1 |
| Related information | Key purposes and algorithmsCreate a key |

### Set the purpose for Cloud KMS keys

| Google control ID | COM-CO-2.5 |
| --- | --- |
| Category | Required |
| Description | Set the purpose for Cloud KMS keys toENCRYPT_DECRYPTso that keys are only used to encrypt and decrypt data. This control blocks other functions, such as signing, and ensures that keys are only used for their intended purpose. If you use keys for other functions, validate those use cases and consider creating additional keys. |
| Applicable products | Cloud KMS |
| Path | cloudkms.projects.locations.keyRings.cryptoKeys/purpose |
| Operator | == |
| Value | ENCRYPT_DECRYPT |
| Type | String |
| Related NIST-800-53 controls | SC-12SC-13 |
| Related CRI profile controls | PR.DS-1.1PR.DS-1.2PR.DS-2.1PR.DS-2.2PR.DS-5.1 |
| Related information | Key purposes and algorithmsCreate a key |

### Ensure that CMEK settings are appropriate for secure BigQuery data warehouses

| Google control ID | COM-CO-2.6 |
| --- | --- |
| Category | Required |
| Description | The protection level indicates how cryptographic operations are performed. After you create a customer-managed encryption key (CMEK), you can't change the protection level. Supported protection levels are the following:SOFTWARE:Cryptographic operations are performed in software.HSM:Cryptographic operations are performed in a hardware security module (HSM).EXTERNAL:Cryptographic operations are performed using a key that is stored in an external key manager that is connected to Google Cloud over the internet. Limited to symmetric encryption and asymmetric signing.EXTERNAL_VPC:Cryptographic operations are performed using a key that is stored in an external key manager that is connected to Google Cloud over a Virtual Private Cloud (VPC) network. Limited to symmetric encryption and asymmetric signing. |
| Applicable products | Cloud KMSBigQuery |
| Path | cloudkms.projects.locations.keyRings.cryptoKeys/primary.protectionLevel |
| Operator | in |
| Value | [] |
| Type | String |
| Related NIST-800-53 controls | SC-12SC-13 |
| Related CRI profile controls | PR.DS-1.1PR.DS-1.2PR.DS-2.1PR.DS-2.2PR.DS-5.1 |
| Related information | Cloud KMS protection levelsExternal key managerImport data into a secured BigQuery data warehouse |

### Rotate encryption key every 90 days

| Google control ID | COM-CO-2.7 |
| --- | --- |
| Category | Required |
| Description | Ensure that the rotation period of your Cloud KMS keys are set to 90 days. A general best practice is to rotate your security keys on a regular interval. This control enforces key rotation for keys that are created with HSM services.When you create this rotation period, also create appropriate policies and procedures to securely handle the creation, deletion, and modification of keying material so that you can help protect your information and ensure availability. Ensure that this period adheres to your corporate policies for key rotation. |
| Applicable products | Cloud KMS |
| Path | cloudkms.projects.locations.keyRings.cryptoKeys/rotationPeriod |
| Operator | <= |
| Value | 90 |
| Type | int32 |
| Related NIST-800-53 controls | SC-12SC-13 |
| Related CRI profile controls | PR.DS-1.1PR.DS-1.2PR.DS-2.1PR.DS-2.2PR.DS-5.1 |
| Related information | Key rotation |

### Define authorized principals

| Google control ID | COM-CO-4.1 |
| --- | --- |
| Category | Required |
| Description | Use theDomain restricted sharing(iam.allowedPolicyMemberDomains) organization policy constraint to define one or more Cloud Identity or Google Workspace customer IDs whose principals can be added to Identity and Access Management (IAM) policies. |
| Applicable products | Organization Policy ServiceIAM |
| Path | constraints/iam.allowedPolicyMemberDomains |
| Operator | Is |
| Value | CUSTOMER_ID,ORG_ID |
| Type | List |
| Related NIST-800-53 controls | AC-3AC-17AC-20 |
| Related CRI profile controls | PR.AC-3.1PR.AC-3.2PR.AC-4.1PR.AC-4.2PR.AC-4.3PR.AC-6.1PR.PT-3.1PR.PT-4.1 |
| Related information | Restricting identities by domain |

### Use audit logs

| Google control ID | COM-CO-7.3 |
| --- | --- |
| Category | Required |
| Description | Google Cloud services write audit log entries to answer who did what, where, and when with Google Cloud resources.Enable audit logging at the organization level. You can configure logging using the pipeline that you use to set up the Google Cloud organization. |
| Applicable products | Cloud Audit Logs |
| Related NIST-800-53 controls | AU-2AU-3AU-8AU-9 |
| Related CRI profile controls | DM.ED-7.1DM.ED-7.2DM.ED-7.3DM.ED-7.4PR.IP-1.4 |
| Related information | Cloud Audit Logs overview |

### Enable VPC Flow Logs

| Google control ID | COM-CO-7.4 |
| --- | --- |
| Category | Required |
| Description | VPC Flow Logs record a sample of network flows that are sent from and received by VM instances, including those used as Google Kubernetes Engine (GKE) nodes. The sample is typically 50% or less of the VPC network flows.When you enable VPC Flow Logs, you enable logging for all VMs in a subnet. However, you can reduce the amount of information written to logging.Enable VPC Flow Logs for each VPC subnet. You can configure logging using a pipeline that you use to create a project. |
| Applicable products | Virtual Private Cloud |
| Related NIST-800-53 controls | AU-2AU-3AU-8AU-9 |
| Related CRI profile controls | DM.ED-7.1DM.ED-7.2DM.ED-7.3DM.ED-7.4PR.IP-1.4 |
| Related information | Log sampling and aggregation |

### Enable Firewall Rules Logging

| Google control ID | COM-CO-7.5 |
| --- | --- |
| Category | Required |
| Description | Firewall Rules Logging creates a record each time that a firewall rule allows or denies traffic.Enable logging for each firewall rule. You can configure logging using a pipeline that you use to create a firewall. |
| Applicable products | Virtual Private Cloud |
| Related NIST-800-53 controls | AU-2AU-3AU-8AU-9 |
| Related CRI profile controls | DM.ED-7.1DM.ED-7.2DM.ED-7.3DM.ED-7.4PR.IP-1.4 |
| Related information | Use Firewall Rules Logging |

## Recommended cloud controls

We recommend that you apply the following common controls to your
Google Cloud environment, regardless of your specific use case.

### Restrict customer-managed encryption keys location

| Google control ID | COM-CO-2.2 |
| --- | --- |
| Category | Recommended |
| Description | Use theRestrict which projects may supply KMS CryptoKeys for CMEK(gcp.restrictCmekCryptoKeyProjects) organization policy constraint to define which projects can store customer-managed encryption keys (CMEKs). This constraint lets you to centralize the governance and management of encryption keys. When a selected key doesn't meet this constraint, resource creation fails.To modify this constraint, administrators need theOrganization Policy Administrator(roles/orgpolicy.policyAdmin) IAM role.If you want to add a second layer of protection, such as bring your own key, change this constraint to represent the key names of the CMEK that is enabled.Product specifics:In Vertex AI, you store your keys in theKEY PROJECTSproject. |
| Applicable products | Cloud KMSOrganization Policy |
| Path | constraints/gcp.restrictCmekCryptoKeyProjects |
| Operator | notexists |
| Value | KEY PROJECTS |
| Type | String |
| Related NIST-800-53 controls | SC-12SC-13 |
| Related CRI profile controls | PR.DS-1.1PR.DS-1.2PR.DS-2.1PR.DS-2.2PR.DS-5.1 |
| Related information | Require CMEK protection |

### Use CMEKs for Google Cloud services

| Google control ID | COM-CO-2.3 |
| --- | --- |
| Category | Recommended |
| Description | If you require more control over key operations than what Google-owned and Google-managed encryption keys allow, you can use customer-managed encryption keys (CMEKs). These keys are created and managed using Cloud KMS. Store the keys as software keys, in an HSM cluster, or in an external key management system.Cloud KMS encryption and decryption rates are subject to quotas.Cloud Storage specificsIn Cloud Storage, use CMEKs on individual objects, or configure your Cloud Storage buckets to use a CMEK by default on all new objects added to a bucket. When using a CMEK, an object is encrypted with the key by Cloud Storage at the time it's stored in a bucket, and the object is automatically decrypted by Cloud Storage when the object is served to requesters.The following restrictions apply when using CMEKs with Cloud Storage:You can't encrypt an object with a CMEK by updating the object's metadata. Include the key as part of a rewrite of the object instead.Your Cloud Storage uses the objects update command to set encryption keys on objects, but the command rewrites the object as part of the request.You must create the Cloud KMS key ring in the same location as the data you intend to encrypt. For example, if your bucket is located inus-east1, any key ring used for encrypting objects in that bucket must also be created inus-east1.For most dual-regions, you must create the Cloud KMS key ring in the associated multi-region. For example, if your bucket is located in the pairus-east1,us-west1, any key ring used for encrypting objects in that bucket must be created in the US multi-region.For theasia1,eur4, andnam4predefined dual-regions, you must create the key ring in the same predefined dual-region.The CRC32C checksum and MD5 hash of objects encrypted with CMEKs aren't returned when listing objects with the JSON API.Using tools like Cloud Storage to perform additional metadataGETrequests on each encryption object to retrieve the CRC32C and MD5 information can make listing substantially shorter. Cloud Storage can't use the decryption portion of asymmetric keys stored in Cloud KMS to automatically decrypt relevant objects in the same manner that CMEKs do. |
| Applicable products | Cloud KMSOrganization PolicyCloud Storage |
| Path | constraints/gcp.restrictNonCmekServices |
| Operator | == |
| Value | bigquery.googleapis.comstorage.googleapis.comaiplatform.googleapis.com |
| Type | String |
| Related NIST-800-53 controls | SC-12SC-13 |
| Related CRI profile controls | PR.DS-1.1PR.DS-1.2PR.DS-2.1PR.DS-2.2PR.DS-5.1 |
| Related information | Cloud KMS locationsCloud KMS quotasCustomer-managed encryption keys |

### Enable Sensitive Data Protection for data inspection

| Google control ID | COM-CO-5.1 |
| --- | --- |
| Category | Recommended |
| Description | Google Cloud recommends using Sensitive Data Protection. The infoTypes or job templates that you select depend on your particular systems. |
| Applicable products | Sensitive Data Protection |
| Related NIST-800-53 controls | SI-4IA-7SC-7SC-8 |
| Related CRI profile controls | PR.AC-1.1PR.AC-1.2PR.AC-1.3PR.DS-5.1PR.DS-8.1ID.RA-1.1DE.CM-1.1DE.CM-1.2DE.CM-1.3DE.CM-1.4DE.CM-5.1DE.CM-6.1DE.CM-6.2DE.CM-6.3DE.CM-7.1DE.CM-7.2DE.CM-7.3DE.CM-7.4DE.DP-2.1DE.DP-3.1DE.DP-4.1DE.DP-4.2DE.DP-5.1DE.AE-2.1DE.AE-3.1DE.AE-3.2DE.AE-4.1 |
| Related information | TemplatesInfoTypes and infoType detectors |

### Recommended controls based on generative AI use case

If you handle sensitive data or sensitive generative AI workloads, we recommend
that you implement the following controls in your applicable generative AI use
cases.

### Enable Data Access audit logs

| Google control ID | COM-CO-7.2 |
| --- | --- |
| Category | Recommended for certain use cases |
| Description | To track who accessed data in your Google Cloud environment, enable Data Access audit logs. These logs record API calls that read, create, or modify user data, as well as API calls that read resource configurations.We highly recommend enabling Data Access audit logs for generative AI models and sensitive data to ensure you can audit who hasreadthe information. To use Data Access audit logs, you must set up your own custom detection logic for specific activities, like super admin logins.Data Access audit logs volume can be large. Enabling Data Access logs might result in your Google Cloud project being charged for the additional logs usage. |
| Applicable products | Cloud Audit Logs |
| Related NIST-800-53 controls | AU-2AU-3AU-8AU-9 |
| Related CRI profile controls | DM.ED-7.1DM.ED-7.2DM.ED-7.3DM.ED-7.4PR.IP-1.4 |
| Related information | Enable Data Access audit logs |

### Recommended controls for your workload folders

We recommend that you implement the following security controls in folders that
contain generative AI workloads.

### Enable the service scope restriction in Access Context Manager access policies

| Google control ID | COM-CO-8.1 |
| --- | --- |
| Category | Recommended for generative AI on use cases |
| Description | For every service perimeter, confirm in the Google Cloud console that the perimeter type is set to regular. |
| Applicable products | Access Context ManagerVPC Service Controls |
| Path | accesscontextmanager.accessPolicies.servicePerimeters/perimeterType |
| Operator | == |
| Value | PERIMETER_TYPE_REGULAR |
| Type | String |
| Related NIST-800-53 controls | SC-7SC-8 |
| Related CRI profile controls | PR.AC-5.1PR.AC-5.2PR.DS-2.1PR.DS-2.2PR.DS-5.1PR.PT-4.1DE.CM-1.1DE.CM-1.2DE.CM-1.3DE.CM-1.4 |
| Related information | Access Context Manager overview |

### Restrict APIs within VPC Service Controls service perimeters

| Google control ID | COM-CO-8.2 |
| --- | --- |
| Category | Recommended for generative AI on use cases |
| Description | For every service perimeter, use Access Context Manager to confirm that the perimeter is protecting the API. |
| Applicable products | VPC Service ControlsAccess Context Manager |
| Path | accesscontextmanager.accessPolicies.servicePerimeters/status.restrictedServices |
| Operator | Anyof |
| Value | aiplatform.googleapis.comartifactregistry.googleapis.combigquery.googleapis.comcloudasset.googleapis.comcloudbuild.googleapis.comcloudfunctions.googleapis.comcloudresourcemanager.googleapis.comcontaineranalysis.googleapis.comdiscoveryengine.googleapis.comdns.googleapis.comnotebooks.googleapis.comondemandscanning.googleapis.comorgpolicy.googleapis.compubsub.googleapis.comsecretmanager.googleapis.comstorage.googleapis.comvisionai.googleapis.com |
| Type | String |
| Related NIST-800-53 controls | SC-7SC-8 |
| Related CRI profile controls | PR.AC-5.1PR.AC-5.2PR.DS-2.1PR.DS-2.2PR.DS-5.1PR.PT-4.1DE.CM-1.1DE.CM-1.2DE.CM-1.3DE.CM-1.4 |
| Related information | gcloud access-context-manager perimeters update |

## Optional common controls

You can optionally implement the following common controls based on your
organization's requirements.

### Enable Access Transparency logs

| Google control ID | COM-CO-7.7 |
| --- | --- |
| Category | Optional |
| Description | Access Transparency provides logs that capture the actions that Google personnel take when accessing your content.You can enable Access Transparency at the organization level. |
| Applicable products | Access Transparency |
| Related NIST-800-53 controls | AU-2AU-3AU-8AU-9 |
| Related CRI profile controls | DM.ED-7.1DM.ED-7.2DM.ED-7.3DM.ED-7.4PR.IP-1.4 |
| Related information | Enabling Access Transparency |

## What's next

- Review [Vertex AI
  controls](https://cloud.google.com/docs/security/security-best-practices-genai/vertex-ai-controls).
- See more [Google Cloud security best practices and guidelines for generative
  AI workloads](https://cloud.google.com/docs/security/security-best-practices-genai).

---

# Dataflow controls for generative AI use casesStay organized with collectionsSave and categorize content based on your preferences.

> Review the recommended Google Cloud security best practices and guidelines that aren&#39;t specific to genAI workloads that use Cloud Dataflow.

# Dataflow controls for generative AI use casesStay organized with collectionsSave and categorize content based on your preferences.

This document includes the best practices and guidelines for Dataflow
when running generative AI workloads on Google Cloud. Use
[Dataflow](https://cloud.google.com/dataflow/docs/overview) with Vertex AI to
build complex pipelines that ingest data from various sources and aggregate the
data as appropriate.

## Optional Dataflow controls

We recommend that you implement the following security controls, depending on your data source.

### Turn off external IP addresses for Dataflow jobs

| Google control ID | DF-CO-6.1 |
| --- | --- |
| Category | Optional |
| Description | Turn off external IP addresses for administrative and monitoring tasks that are related to Dataflow jobs. Instead, configure access to your Dataflow worker VMs using SSH.Enable Private Google Access and specify one of the following options in your Dataflow job:--usePublicIps=falseand--network=NETWORK-NAME--subnetwork=SUBNETWORK-NAMEWhere:NETWORK-NAME: The name of your Compute Engine network.SUBNETWORK-NAME: The name of your Compute Engine subnetwork. |
| Applicable products | Compute EngineDataflow |
| Related NIST-800-53 controls | SC-7SC-8 |
| Related CRI profile controls | PR.AC-5.1PR.AC-5.2PR.DS-2.1PR.DS-2.2PR.DS-5.1PR.PT-4.1DE.CM-1.1DE.CM-1.2DE.CM-1.3DE.CM-1.4 |
| Related information | Choose an access methodConfigure Private Google Access |

### Use network tags for firewall rules

| Google control ID | DF-CO-6.2 |
| --- | --- |
| Category | Optional |
| Description | Network tags are text attributes that attach to Compute Engine VMs such as Dataflow worker VMs. Network tags let you make VPC network firewall rules and some custom static routes applicable to specific VM instances. Dataflow supports adding network tags to all worker VMs that run a particular Dataflow job. |
| Applicable products | Compute EngineDataflow |
| Related NIST-800-53 controls | SC-7SC-8 |
| Related CRI profile controls | PR.AC-5.1PR.AC-5.2PR.DS-2.1PR.DS-2.2PR.DS-5.1PR.PT-4.1DE.CM-1.1DE.CM-1.2DE.CM-1.3DE.CM-1.4 |
| Related information | Network tags for Dataflow |

## What's next

- Review [Identity and Access Management (IAM)
  controls](https://cloud.google.com/docs/security/security-best-practices-genai/iam-controls).
- See more [Google Cloud security best practices and guidelines for generative
  AI workloads](https://cloud.google.com/docs/security/security-best-practices-genai).

   Was this helpful?

---

# Cloud DNS controls for generative AI use casesStay organized with collectionsSave and categorize content based on your preferences.

> Review the recommended Google Cloud security best practices and guidelines that aren&#39;t specific to genAI workloads that use Cloud DNS.

# Cloud DNS controls for generative AI use casesStay organized with collectionsSave and categorize content based on your preferences.

This document includes the best practices and guidelines for Cloud DNS when
running generative AI workloads on Google Cloud. Use [Cloud DNS](https://cloud.google.com/dns/docs/overview) with Vertex AI to register, manage, and serve
your domain.

## Required Cloud DNS controls

The following controls are strongly recommended when using
Cloud DNS.

### Enable DNS Security Extensions

| Google control ID | DNS-CO-6.1 |
| --- | --- |
| Category | Required |
| Description | The Domain Name System Security Extensions (DNSSEC) is a feature of the Domain Name System (DNS) that authenticates responses to domain name lookups. It doesn't provide privacy protections for those lookups, but prevents attackers from manipulating or poisoning the responses to DNS requests.Within Cloud DNS, enable DNSSEC in the following places:DNS zoneTop-level domain (TLD)DNS resolution |
| Applicable products | Cloud DNS |
| Related NIST-800-53 controls | SC-7SC-8 |
| Related CRI profile controls | PR.AC-5.1PR.AC-5.2PR.DS-2.1PR.DS-2.2PR.DS-5.1PR.PT-4.1DE.CM-1.1DE.CM-1.2DE.CM-1.3DE.CM-1.4 |
| Related information | Not applicable |

## Optional Cloud DNS controls

We recommend that you implement the following security controls in folders that
contain generative AI workloads.

### Use zonal DNS

| Google control ID | DNS-CO-4.1 |
| --- | --- |
| Category | Optional |
| Description | Thecompute.setNewProjectDefaultToZonalDNSOnlyboolean constraint lets you set the internal DNS setting for new projects to use zonal DNS only. Use zonal DNS because it offers higher reliability compared to individual zones because zonal DNS isolates failures in the DNS registration . |
| Applicable products | Organization policy |
| Path | constraints/compute.setNewProjectDefaultToZonalDNSOnly |
| Operator | = |
| Value | True |
| Type | Boolean |
| Related NIST-800-53 controls | AC-3AC-17AC-20 |
| Related CRI profile controls | PR.AC-3.1PR.AC-3.2PR.AC-4.1PR.AC-4.2PR.AC-4.3PR.AC-6.1PR.PT-3.1PR.PT-4.1 |
| Related information | Zonal and global internal DNS names |

## What's next

- Review [Cloud Identity
  controls](https://cloud.google.com/docs/security/security-best-practices-genai/cloud-identity-controls).
- See more [Google Cloud security best practices and guidelines for generative
  AI workloads](https://cloud.google.com/docs/security/security-best-practices-genai).

   Was this helpful?
