# Remote attestation of disaggregated machinesStay organized with collectionsSave and categorize content based on your preferences. and more

# Remote attestation of disaggregated machinesStay organized with collectionsSave and categorize content based on your preferences.

> Discover how Google attests the integrity of data center machines.

# Remote attestation of disaggregated machinesStay organized with collectionsSave and categorize content based on your preferences.

*This content was last updated in May 2024, and represents the status quo
as of the time it was written. Google's security policies and systems may change
going forward, as we continually improve protection for our customers.*

This document describes the Google approach to data center machine attestation.
The architecture described in this document is designed to be integrated with
open standards such as
[Trusted Platform Module (TPM)](https://trustedcomputinggroup.org/work-groups/trusted-platform-module/),
[Security Protocol and Data Model (SPDM)](https://www.dmtf.org/content/dmtf-releases-security-specification-12),
and
[Redfish](https://www.dmtf.org/standards/redfish).
For new standards or reference implementations that are proposed by Google and
related to data center machine attestation, see our
[Platform Integrity (PINT)](https://github.com/google/PINT)
project in GitHub. This document is intended for security executives, security
architects, and auditors.

## Overview

Increasingly, Google designs and deploys disaggregated data center machines. Instead
of a single root of trust, many machines contain separate roots of trust, including
roots of trust for measurement (RTM), storage, update, and recovery. Each RTM
serves a subsection of the entire machine. For example, a machine might have one
RTM that measures and attests to what was booted on the main CPU, and another
RTM that measures and attests to what was booted on a SmartNIC that is plugged into a
PCIe slot. The following diagram shows an example machine.

![An example machine.](https://cloud.google.com/static/docs/security/images/remote-attestation-example-dc.svg)

The complexity of multiple RTMs in a machine adds to the enormous scale and
expectations of data center machines, and many complications that can
occur because of human, hardware, or software faults. In summary, ensuring
firmware integrity of our fleet is a non-trivial endeavor.

The system described in this document is designed to make the problem of remote
attestation for disaggregated machines more manageable. This attestation
infrastructure is extensible, letting it adapt to serve ever-more-complex
machines as they appear in the data center.

By sharing this work, we aim to provide our perspective on how disaggregated
machine attestation can be done at scale. Through collaboration with industry
partners and contributions to standards bodies such as Distributed Management
Task Force (DMTF), Trusted Computing Group (TCG), and Open Compute Project
(OCP), we intend to continue supporting security innovation in this space.

## Recommended RTM properties

This section introduces some properties that we recommend for RTMs.

### RTM hardware integration

When a processor is paired with an RTM, the RTM should capture measurements
over the first mutable code that runs on that processor. Subsequent mutable code
should have its measurements captured and reported to a root of trust before the code
runs. This arrangement produces a measured boot chain that allows for robust
attestation of the security-critical state of the processor.

### RTM hardware and firmware identity attestation

Each RTM should have a signing key pair that is used to emit attestations for
external validation. The certificate chain for this key pair should include
cryptographic evidence of the RTM's unique *hardware identity* and the *firmware
identity* for any mutable code that runs within the RTM. The certificate chain
should be rooted in the RTM manufacturer. This approach lets machines recover
from critical RTM firmware vulnerabilities.

The
[Device Identifier Composition Engine (DICE)](https://trustedcomputinggroup.org/work-groups/dice-architectures)
specification is a formalization of the pattern that is used in our attestation
solution. The RTM manufacturer certifies a unique device key pair, which
certifies an alias key pair that is specific to the RTM's hardware identity and
firmware image. The alias key certificate chain contains a measurement of the
RTM firmware and the RTM's serial number. Verifiers can be confident that any
data signed by a given alias key was emitted from an RTM that is described by
the cryptographic hardware and firmware identity measurements that are embedded
within that alias key's certificate chain.

## Remote attestation operations

The attestation scheme is designed to ensure that user data and jobs are only
issued to machines that are running their intended boot stack, while still
allowing fleet maintenance automation to occur at scale to remediate issues. The
job scheduler service, hosted in our internal cloud, can challenge the
collection of RTMs within the machine, and compare the resulting attested
measurements to a policy that is unique to that machine. The scheduler only
issues jobs and user data to machines if the attested measurements conform to
the machine's policy.

Remote attestation includes the following two operations:

- Attestation policy generation, which occurs whenever a machine's
  intended hardware or software is changed.
- Attestation verification, which occurs at defined points in our machine
  management flows. One of these points is just before work is scheduled on a
  machine. The machine only gains access to jobs and user data after
  attestation verification passes.

## The attestation policy

Google uses a signed machine-readable document, referred to as a *policy*, to
describe the hardware and software that is expected to be running within a
machine. This policy can be attested by the machine's collection of RTMs. The
following details for each RTM are represented in the policy:

- The trusted *identity root certificate* that can validate
  attestations that are emitted by the RTM.
- The globally unique *hardware identity* that uniquely identifies the RTM.
- The *firmware identity* that describes the expected version that the
  RTM should be running.
- The *measurement expectations* for each boot stage that is reported by
  the RTM.
- An *identifier for the RTM*, analogous to a
  [Redfish resource name](https://www.dmtf.org/sites/default/files/standards/documents/DSP2046_2021.1.pdf).
- An *identifier that links the RTM to its physical location* within a
  machine. This identifier is analogous to a
  [Redfish resource](https://www.dmtf.org/sites/default/files/standards/documents/DSP2046_2021.1.pdf)
  name, and is used by automated machine repair systems.

In addition, the policy also contains a globally unique revocation serial
number that helps prevent unauthorized policy rollback. The following diagram
shows a policy.

![An example attestation policy.](https://cloud.google.com/static/docs/security/images/remote-attestation-policy.svg)

The diagram shows the following items in the policy:

- The signature provides policy authentication.
- The revocation serial number provides policy freshness to help prevent
  rollback.
- The RTM expectations enumerate details for each RTM in the machine.

The following sections describe these items in more detail.

### Policy assembly

When a machine's hardware is assembled or repaired, a hardware model is created
that defines the expected RTMs on that machine. Our control plane helps ensure
that this information remains current across events such as repairs that involve
part swaps or hardware upgrades.

In addition, the control plane maintains a set of expectations about the
software that is intended to be installed on a machine, along with expectations
about which RTMs should measure which software. The control plane uses these
expectations, along with the hardware model, to generate a signed and revocable
attestation policy that describes the expected state of the machine.

The signed policy is then written to persistent storage on the machine that it
describes. This approach helps reduce the number of network and service
dependencies that are needed by the remote verifier when attesting a machine.
Rather than query a database for the policy, the verifier can fetch the policy
from the machine itself. This approach is an important design feature, as the
job schedulers have strict SLO requirements and must remain highly available.
Reducing the network dependencies of these machines on other services helps to
reduce the risk of outages. The following diagram shows this flow of events.

![Policy assembly flow.](https://cloud.google.com/static/docs/security/images/remote-attestation-control-plane.svg)

The diagram describes the following steps that the control plane completes in
the policy assembly process:

- Derives the attestation policy from the software package assignment and
  machine hardware model.
- Signs the policy.
- Stores the policy on the data center machine.

### Policy revocation

The hardware and software intent for a given machine changes over time. When
the intent changes, old policies must be revoked. Each signed attestation policy
includes a unique revocation serial number. Verifiers obtain the appropriate
public key for authenticating a signed policy, and the appropriate certificate
revocation list for ensuring that the policy is still valid.

Interactively querying a key server or revocation database affects the job
schedulers' availability. Instead, Google uses an asynchronous model. The set of
public keys that are used to authenticate signed attestation policies are pushed
as part of each machine's base operating system image. The CRL is pushed
asynchronously using the same centralized revocation deployment system that
Google uses for other credential types. This system is already engineered for
reliable operation during normal conditions, with the ability to perform rapid
emergency pushes during incident response conditions.

By using verification public keys and CRL files that are stored locally on the
verifier's machine, verifiers can validate attestation statements from remote
machines without having any external services in the critical path.

## Retrieving attestation policies and validating measurements

The process of remotely attesting a machine consists of the following stages:

- Retrieving and validating the attestation policy.
- Obtaining attested measurements from the machine's RTMs.
- Evaluating the attested measurements against the policy.

The following diagram and sections describe these stages further.

![Remote attestation stages.](https://cloud.google.com/static/docs/security/images/remote-attestation-stages.svg)

### Retrieving and validating the attestation policy

The remote verifier retrieves the signed attestation policy for the machine. As
mentioned in
[Policy assembly](#policy-assembly),
for availability reasons, the policy is stored as a signed document on the
target machine.

To verify that the returned policy is authentic, the remote verifier consults
the verifier's local copy of the relevant CRL. This action helps ensure that the
retrieved policy was cryptographically signed by a trusted entity and that the
policy wasn't revoked.

### Obtaining attested measurements

The remote verifier challenges the machine, requesting measurements from each
RTM. The verifier ensures freshness by including cryptographic nonces in these
requests. An on-machine entity, such as a baseboard management controller (BMC),
routes each request to its respective RTM, gathers the signed responses, and
sends them back to the remote verifier. This on-machine entity is unprivileged
from an attestation perspective, as it serves only as a transport for the RTM's
signed measurements.

Google uses internal APIs for attesting to measurements. We also contribute
enhancements to Redfish to enable off-machine verifiers to challenge a BMC for
an RTM's measurements by using SPDM. Internal machine routing is done over
implementation-specific protocols and channels, including the following:

- Redfish over subnet
- Intelligent Platform Management Interface (IPMI)
- Management Component Transport Protocol (MCTP) over i2c/i3c
- PCIe
- Serial Peripheral Interface (SPI)
- USB

### Evaluating attested measurements

Google's remote verifier validates the signatures that are emitted by each RTM,
ensuring that they root back to the RTM's identity that is included in the
machine's attestation policy. Hardware and firmware identities that are
present in the RTM's certificate chain are validated against the policy,
ensuring that each RTM is the correct instance and runs the correct firmware. To
ensure freshness, the signed cryptographic nonce is checked. Finally, the attested
measurements are evaluated to ensure that they correspond with the policy's
expectations for that device.

## Reacting to remote attestation results

After attestation is complete, the results must be used to determine the fate
of the machine being attested. As shown in the diagram, there are two possible
results: the attestation is successful and the machine is issued task
credentials and user data, or the attestation fails and alerts are sent to the
repairs infrastructure.

![Remote attestation results.](https://cloud.google.com/static/docs/security/images/remote-attestation-results.svg)

The following sections provide more information about these processes.

### Failed attestation

If attestation of a machine isn't successful, Google doesn't use the machine to
serve customer jobs. Instead, an alert is sent to the repairs infrastructure,
which attempts to automatically reimage the machine. Although attestation failures
might be due to malicious intent, most attestation failures are due to
bugs in software rollouts. Therefore, rollouts with rising
attestation failures are stopped automatically to help prevent more
machines from failing attestation. When this event occurs, an alert is sent to SREs. For machines that aren't fixed by automated reimaging, the rollout is rolled back, or there is a rollout of fixed software. Until a machine undergoes
successful remote attestation again, it isn't used to serve customer jobs.

### Successful attestation

If remote attestation of a machine is successful, Google uses the machine to
serve production jobs such as VMs for Google Cloud customers or image processing
for Google Photos. Google requires meaningful job actions that
involve networked services to be gated behind short-lived
[LOAS](https://www.usenix.org/system/files/login/articles/login_winter16_05_cittadini.pdf)
task credentials. These credentials are granted over a secure connection after a
successful attestation challenge, and provide privileges required by the job.
For more information about these credentials, see
[Application Layer Transport Security](https://cloud.google.com/docs/security/encryption-in-transit/application-layer-transport-security).

Software attestation is only as good as the infrastructure that builds that
software. To help ensure that resulting artifacts are an accurate reflection of
our intent, we have invested significantly in the integrity of our build
pipeline. For more information about a standard that was proposed by Google to
address software supply chain integrity and authenticity, see
[Software Supply Chain Integrity](https://www.nist.gov/system/files/documents/noindex/2021/06/08/Google%20NIST%20statement%20on%20%285%29%20integrity.pdf).

## What's next

Learn how
    [BeyondProd](https://cloud.google.com/docs/security/beyondprod)
    helps Google's data center machines establish secure connections.

   Was this helpful?

---

# Respond to abuse notifications and warnings in Google CloudStay organized with collectionsSave and categorize content based on your preferences.

> Learn how to respond to an abuse notification in Google Cloud and protect Google Cloud from abuse and misuse.

# Respond to abuse notifications and warnings in Google CloudStay organized with collectionsSave and categorize content based on your preferences.

To help keep Google Cloud systems and our customers safe, we work to
ensure that our products are used in the intended manner and that our platform
isn't misused or abused. As described in the
[Cloud Privacy Notice](https://cloud.google.com/terms/cloud-privacy-notice), we work to protect against
the violations defined in the [Terms of Service](https://cloud.google.com/terms/) and
[Acceptable Use Policy](https://cloud.google.com/terms/aup).

Examples of abuse or misuse include the following issues:

- Potentially compromised service account credentials
- Potentially compromised API keys
- Cryptocurrency alerting
- Malware or unwanted software
- Phishing

Google Cloud has a dedicated team of engineers and security experts who
work to protect our systems and customers. When Google becomes aware
of abusive activity, we notify affected customers and take measures to help
prevent future abuse. We strive to ensure that our interventions don't impact
your critical work. For more information, see
[Project suspension guidelines](https://cloud.google.com/resource-manager/docs/project-suspension-guidelines).

This page describes what you can do if you receive a notification about abuse or
misuse from us.

## Respond to an abuse notification

If you receive an abuse notification or warning, you must promptly address or
remedy any violations that are noted in the notification and review the
Terms of Service and Acceptable Use Policy.

You can check your
[Google Cloud abuse logs](https://cloud.google.com/logging/docs/view/logs-viewer-interface)
and troubleshoot your environment using the diagnostic tools that are part of
Google Cloud (such as Security Command Center).

## Example issues and responses

This section includes examples that describe how to remediate and respond to
issues that might have caused an alert. If you cannot resolve the issue on your
own, and you have a [Cloud Customer Care package](https://cloud.google.com/support), contact
[Customer Care](https://enterprise.google.com/supportcenter/managecases).
You can also consult the
[Google Cloud Community Forum](https://www.googlecloudcommunity.com/gc/Google-Cloud/ct-p/google-cloud)
to help resolve issues.

### Potentially compromised service account credentials

An alert for detected leaked credentials indicates that your organization might
have inadvertently published the specified service account credentials in public
repositories or websites.

To resolve this issue, complete the following steps:

1. In the Google Cloud console, review the activity on your account.
  [Go to Dashboard](https://console.cloud.google.com/home/dashboard)
2. Revoke all credentials for the compromised service accounts. Rotate all
  credentials in the affected projects because every resource that is accessible
  to the service account might have been affected. For instructions, see
  [Handling compromised Google Cloud credentials](https://cloud.google.com/security/compromised-credentials).
3. Delete all unauthorized VMs or resources.
4. Verify that your service account credentials are not embedded in public
  repositories, stored in download directories, or unintentionally shared in
  other ways.

To help protect your organization against compromised credentials, see
[Best practices to avoid compromised credentials](https://cloud.google.com/docs/security/compromised-credentials#best_practices_to_avoid_compromised_credentials).

### Potentially compromised API keys

An alert for detected compromised API keys indicates that your
organization might have inadvertently published the affected API key in public
repositories or websites.

To resolve this issue, complete the following steps:

1. If this key is supposed to be public, complete the following steps:
  1. In the Google Cloud console, review the API and billing activity on
    your account. Verify that the usage and billing are what you expect.
    [Go to Dashboard](https://console.cloud.google.com/home/dashboard)
  2. If applicable, add
    [API key restrictions](https://cloud.google.com/docs/authentication/api-keys#api_key_restrictions)
    to your API key.
2. If this key isn't supposed to be public, complete the following steps:
  1. In the Google Cloud console, generate a new API key. For
    instructions, see
    [Regenerate API keys](https://cloud.google.com/docs/security/compromised-credentials#regenerate_api_keys)
  2. Verify that your API keys are not embedded in public repositories, stored
    in download directories, or unintentionally shared in other ways.
  3. If applicable, add
    [API key restrictions](https://cloud.google.com/docs/authentication/api-keys#api_key_restrictions)
    to your API key.
  4. If you're using Google Maps APIs, see
    [Google Maps Platform security guidance](https://developers.google.com/maps/api-security-best-practices).

To help protect your organization against compromised credentials, see
[Best practices to avoid compromised credentials](https://cloud.google.com/docs/security/compromised-credentials#best_practices_to_avoid_compromised_credentials).

### Cryptocurrency mining

This alert indicates that a project is engaged in cryptocurrency mining. This
issue is usually preceded by a compromise, such as a leaked service account
credential, that grants a bad actor access to your Google Cloud project.

To resolve this issue, complete the following steps:

1. In the Google Cloud console, review the project's activity.
  [Go to Logs Explorer](https://console.cloud.google.com/logs/query)
2. Terminate any unauthorized cryptomining activity and take measures to secure
  your account and any affected projects.
3. If you have suspended resources, you can [submit an appeal](#submit-appeal)
  to regain access.

To help protect your organization against cryptocurrency mining attacks, see
[Best practices for protecting against cryptocurrency mining attacks](https://cloud.google.com/architecture/bps-for-protecting-against-crytocurrency-attacks).

### Malware or unwanted software

This alert indicates that your organization includes a project that hosts,
distributes, or facilitates distribution of
[malware, unwanted software, or viruses](https://developers.google.com/search/docs/advanced/security/malware).
To resolve this issue, complete the following steps:

1. Remove any malicious content and mechanisms from your projects.
  [Go to Logs Explorer](https://console.cloud.google.com/logs/query)
2. Verify that your project wasn't compromised by checking its usage and logs.
3. If necessary,
  [shut down (delete) your project](https://cloud.google.com/resource-manager/docs/creating-managing-projects#shutting_down_projects).
4. To regain access to your suspended resources,
  [submit an appeal](#submit-appeal).

To help protect your organization against malware or unwanted software, see
[Mitigate ransomware attacks using Google Cloud](https://cloud.google.com/architecture/mitigating-ransomware-attacks).

If your site has a red browser warning, it was identified by Google's
[Safe Browsing program](https://safebrowsing.google.com/) as malicious. Safe
Browsing operates separately from Google Cloud. You can
[submit a review request](https://developers.google.com/search/docs/monitor-debug/security/malware#fixing-the-problem) for the page using the Search Console. For more information, see
[Google Search Console](http://search.google.com/search-console) and
[Get started with Search Console](https://developers.google.com/search/docs/monitor-debug/search-console-start).

### Phishing

This alert indicates that
[phishing or deceptive social engineering](https://developers.google.com/search/docs/monitor-debug/security/social-engineering)
content was published from your Google Cloud project. Hackers might try to take
control of your site and use it to host deceptive content.

To resolve this issue, complete the following steps:

1. Remove any phishing content and mechanisms from your projects.
2. Verify that your project wasn't compromised by checking its usage and logs.
3. If necessary,
  [shut down (delete) your project](https://cloud.google.com/resource-manager/docs/creating-managing-projects#shutting_down_projects).
4. To regain access to your suspended resources,
  [submit an appeal](#submit-appeal).

If your site has a red browser warning, it was identified by Google's
[Safe Browsing program](https://safebrowsing.google.com/) as malicious. Safe
Browsing operates separately from Google Cloud. You can
[submit a review request](https://developers.google.com/search/docs/monitor-debug/security/malware#fixing-the-problem) for the page using the Search Console. For more information, see
[Google Search Console](http://search.google.com/search-console) and
[Get started with Search Console](https://developers.google.com/search/docs/monitor-debug/search-console-start).

## Submit an appeal

You can submit an appeal to Google Cloud after you receive a warning or
suspension notification and complete the remediation steps so that you can
restore access to services.

To submit an appeal, in the Google Cloud console, select the project and
access the **Appeals** page for the project. Ensure that your response includes
the following:

- What caused the issue.
- The steps that you've taken to resolve the issue.
- Whether the behavior was intentional.
- Your [billing account ID](https://cloud.google.com/billing/docs/how-to/find-billing-account-id).
- Whether your project was compromised.

If you see an error message telling you that you don't have sufficient
permission to access the page, verify that you're logged in as the project owner
and have the
[appropriate IAM permissions to edit the project](https://cloud.google.com/iam/docs/granting-changing-revoking-access).
If you're logged into multiple accounts, log out of all other accounts and try
logging in again.

After you submit your appeal, Google Cloud reviews your appeal and
responds back with a resolution and final disposition.

## Report suspected abuse

The protection of your data and workloads is a [shared
responsibility](https://cloud.google.com/architecture/framework/security/shared-responsibility-shared-fate).
You must actively monitor your Google Cloud environment and implement
appropriate security controls and best practices. If you believe that your
Google Cloud services are being abused, take immediate action to secure
any
affected services and accounts and report the abuse to [Google Cloud Customer Care](https://support.cloud.google.com/portal/). As described in the Terms of
Service, we investigate reports of unauthorized financial charges that are
related to abuse or compromise. You are financially responsible for charges that
result from improperly secured resources.

To report
an issue that isn't related to your services, use the
[Report suspected abuse on Google Cloud](https://support.google.com/code/contact/cloud_platform_report)
form.

## Best practices to help protect yourself from abuse

To help protect yourself from abuse on Google Cloud, consider the
following:

- Use strong passwords and enable two-factor authentication for your
  Google Cloud accounts. For more information, see
  [Single sign-on](https://cloud.google.com/architecture/identity/single-sign-on).
- Be careful about which third-party applications are granted access to
  your Google Cloud resources, and the authentication method they use.
  For more information about securing applications, see
  [Use IAM securely](https://cloud.google.com/iam/docs/using-iam-securely)
  and
  [Authentication methods at Google](https://cloud.google.com/docs/authentication).
- Monitor third-party software to help ensure that your project doesn't
  become compromised by vulnerabilities in third-party software you have
  installed. For more information on security best practices, see the
  [Securing instances](https://support.google.com/cloud/answer/6262505#gcp-instance)
  section of the Cloud Security FAQ.
- If your primary business is to host third-party content or services or
  facilitate the sale of goods and services between third parties, enforce
  compliance with the Google Cloud Acceptable Use Policy. Implement the
  following:
  - Publish policies that define what content is prohibited on your
    platform.
  - Maintain a reporting intake process (for example, a webform or
    email alias) to receive notices of illegal or abusive content (in
    addition to a monitored communication channel for Google).
  - Promptly review and address any alerts, and remove content where
    appropriate.
- Implement logging and detective controls and
  [monitor your Google Cloud logs](https://cloud.google.com/logging/docs/alerting/monitoring-logs)
  for suspicious activity. For more information, see the following:
  - [Cloud Audit Logs](https://cloud.google.com/guides/product-specific/auditlogs/audit-log)
  - [Google Cloud platform logs](https://cloud.google.com/logging/docs/api/platform-logs)
  - [Network Intelligence Center   overview](https://cloud.google.com/network-intelligence-center/docs/overview)
  - [Sensitive Data Protection overview](https://cloud.google.com/sensitive-data-protection/docs/sensitive-data-protection-overview)
- Use
  [Security Command Center](https://cloud.google.com/security-command-center/docs/security-command-center-overview)
  to help identify vulnerabilities in your environment and remediate them.
- Monitor the relevant Essential Contacts email addresses for your
  projects so that you know as soon as your project is warned. Make sure that
  email messages from `google-cloud-compliance@google.com` don't go to a spam
  folder.

   Was this helpful?

---

# Artifact Registry controls for generative AI use casesStay organized with collectionsSave and categorize content based on your preferences.

> Review the recommended Google Cloud security best practices and guidelines that are specific to genAI workloads that use Artifact Registry.

# Artifact Registry controls for generative AI use casesStay organized with collectionsSave and categorize content based on your preferences.

This document includes the best practices and guidelines for Artifact Registry when
running generative AI workloads on Google Cloud. Use
[Artifact Registry](https://cloud.google.com/artifact-registry/docs/overview) with Vertex AI to
streamline your machine learning (ML) development and deployment process,
improve collaboration, and ensure the security and reliability of your ML
models.

Consider the following use cases for Artifact Registry with
Vertex AI:

- **Manage your ML artifacts:** Artifact Registry lets you store and manage all
  your ML artifacts in a single place, including model training code, datasets,
  trained models, and prediction serving containers. You can use this centralized repository to track, share, and reuse your ML artifacts across different
  teams and projects.
- **Version control and reproducibility:** Artifact Registry provides version
  control for your ML artifacts, helping you track changes and roll back to
  previous versions, if needed. This feature is crucial for ensuring the
  reproducibility of your ML experiments and deployments.
- **Secure and reliable storage:** Artifact Registry offers secure and
  reliable storage for your ML artifacts. These artifacts are encrypted at
  rest and in transit. Configure access control to restrict who can access the
  artifacts to help protect your valuable data and intellectual property.
- **Integration with Vertex AI Pipelines:** Integrate Artifact Registry with
  Vertex AI Pipelines to build and automate your ML workflows. Use
  Artifact Registry to store your pipeline artifacts (for example, your
  pipeline
  definitions, code, and data) and to automatically trigger pipeline runs when
  new artifacts are uploaded.
- **Streamline CI/CD for ML:** Integrate Artifact Registry with your CI/CD
  tooling to streamline the development and deployment of your ML models. For
  example, use Artifact Registry to automatically build and deploy your model
  serving container whenever you push a new version of your model to
  Artifact Registry.
- **Multi-region support:** Artifact Registry lets you store your artifacts in
  multiple regions, which can help improve the performance and availability of
  your ML models, especially if you have users located in different parts of
  the world.

## Required Artifact Registry controls

The following controls are strongly recommended when using Artifact Registry.

### Configure vulnerability scanning for artifacts

| Google control ID | AR-CO-6.2 |
| --- | --- |
| Category | Required |
| Description | Use Artifact Analysis or another tool to scan for vulnerabilities in images and packages within Artifact Registry.If you use a third-party scanning tool, you must deploy these tools correctly to scan Artifact Registry for vulnerabilities in images and packages. |
| Applicable products | Artifact RegistryArtifact Analysis |
| Path | serviceusage.getservice |
| Operator | = |
| Value | containerscanning.googleapis.com |
| Related NIST-800-53 controls | RA-5SI-5SA-5SR-8CA-7 |
| Related CRI profile controls | ID-RA-1.1ID-RA-1.2ID-RA-3.1ID-RA-3.2ID-RA-3.3PR.IP-7.1PR.IP-8.1PR.IP-12.1PR.IP-12.2PR.IP-12.3PR.IP-12.4DE.CM-8.1DE.CM-8.2DE.DP-4.1DE-DP-4.2DE-DP-5.1RS.CO-3.1RS.CO-3.2RS.CO-5.2RS.CO-5.3RS.AN-5.1RS.AN-5.2RS-AN-5.3RS.MI-3.1RS-MI-3.2 |
| Related information | Artifact analysis and vulnerability scanning |

### Recommended controls based on generative AI use case

If you handle sensitive data or sensitive generative AI workloads, we recommend
that you implement the following controls in your applicable generative AI use
cases.

### Create cleanup policies for artifacts

| Google control ID | AR-CO-6.1 |
| --- | --- |
| Category | Recommended based on use case |
| Description | Cleanup policies are useful if you store many versions of your artifacts but only need to keep specific versions that you release to production. Create separate cleanup policies for deleting artifacts and retaining artifacts. |
| Applicable products | Artifact Registry |
| Related NIST-800-53 controls | SI-12 |
| Related CRI profile controls | PR.IP-2.1PR.IP-2.2PR.IP-2.3 |
| Related information | Configure cleanup policies |

## What's next

- Review [BigQuery
  controls](https://cloud.google.com/docs/security/security-best-practices-genai/bigquery-controls).
- See more [Google Cloud security best practices and guidelines for generative
  AI workloads](https://cloud.google.com/docs/security/security-best-practices-genai).

   Was this helpful?

---

# BigQuery controls for generative AI use casesStay organized with collectionsSave and categorize content based on your preferences.

> Review the recommended BigQuery security best practices and guidelines that aren&#39;t common to generative AI workloads on Google Cloud.

# BigQuery controls for generative AI use casesStay organized with collectionsSave and categorize content based on your preferences.

This document includes the best practices and guidelines for BigQuery
when running generative AI workloads on Google Cloud. Use
[BigQuery](https://cloud.google.com/bigquery/docs/introduction)
with Vertex AI to store data. Using BigQuery with
Vertex AI can significantly enhance your ML workflow because you can simplify
data access, enable scalable analysis, and use its ML capabilities.

Consider the following use cases for BigQuery with Vertex AI:

- **Seamless integration**: BigQuery and Vertex AI
  are tightly integrated, letting you access and analyze your data directly
  within the Vertex AI platform. This integration eliminates the
  need for data movement, streamlines your ML workflow, and reduces friction.
- **Scalable data analysis**: BigQuery offers a petabyte-scale
  data warehouse,
  letting you analyze massive datasets without worrying about infrastructure
  limitations. This scalability is critical for training and deploying ML
  models that require vast amounts of data.
- **SQL-based ML**: BigQuery ML lets you use familiar SQL commands to
  train
  and deploy models directly within BigQuery. This feature lets data analysts
  and SQL practitioners use ML capabilities without requiring advanced coding
  skills.
- **Online and batch predictions**: BigQuery ML supports online
  and batch
  predictions. You can run real-time predictions on individual rows or
  generate predictions for large datasets in batch mode. This flexibility
  permits diverse use cases with varying latency requirements.
- **Reduced data movement**: With BigQuery ML, you don't need to
  move your
  data to separate storage or compute resources for model training and
  deployment. This reduced movement simplifies your workflow, reduces latency,
  and minimizes cost associated with data transfer.
- **Model monitoring**: Vertex AI provides comprehensive model
  monitoring
  capabilities, letting you track the performance, fairness, and
  explainability of your BigQuery ML models. Model monitoring helps you ensure
  that your models are performing as expected and address potential issues.
- **Pretrained models**: Vertex AI offers access to pretrained
  models,
  including those for natural language processing and computer vision. You can
  use these models within BigQuery to enhance your analysis and extract deeper
  insights from your data.
- **Cost-effective solution**: BigQuery ML offers a
  cost-effective, flexible
  way to train and deploy ML models. You only pay for the resources you use,
  making it an affordable option for organizations of all sizes.
- **Advanced analytics capabilities**: BigQuery provides tools
  for advanced
  analytics, including geospatial analysis and forecasting. These tools let
  you combine ML with other analytical techniques for deeper data exploration
  and richer insights.
- **Enhanced collaboration**: By using BigQuery with
  Vertex AI, data
  scientists, ML engineers, and analysts can collaborate seamlessly on ML
  projects. This collaboration helps create a more integrated and efficient
  approach to tackling complex data problems.

## Required BigQuery controls

The following controls are strongly recommended when using
BigQuery.

### Ensure BigQuery datasets aren't publicly readable or set to allAuthenticatedUsers

| Google control ID | BQ-CO-6.1 |
| --- | --- |
| Category | Required |
| Description | Restrict access to the information in a BigQuery dataset to specific users only. To configure this protection, you must set up detailed roles. |
| Applicable products | Organization Policy ServiceBigQueryIdentity and Access Management (IAM) |
| Path | cloudasset.assets/assetType |
| Operator | == |
| Value | bigquery.googleapis.com/Dataset |
| Type | String |
| Related NIST-800-53 controls | AC-3AC-12AC-17AC-20 |
| Related CRI profile controls | PR.AC-3.1PR.AC-3.2PR.AC-4.1PR.AC-4.2PR.AC-4.3PR.AC-6.1PR.AC-7.1PR.AC-7.2PR.PT-3.1PR-PT-4.1 |
| Related information | Revoke access to a datasetallAuthenticatedUsersControl access to resources with IAM |

### Ensure BigQuery tables aren't publicly readable or set to allAuthenticatedUsers

| Google control ID | BQ-CO-6.2 |
| --- | --- |
| Category | Required |
| Description | Restrict access to the information in a BigQuery table to specific users only. To configure this protection, you must set up detailed roles. |
| Applicable products | Identity and Access Management (IAM)BigQuery |
| Path | cloudasset.assets/iamPolicy.bindings.members |
| Operator | anyof |
| Value | allUsersallAuthenticatedUsers |
| Type | String |
| Related NIST-800-53 controls | AC-3AC-12AC-17AC-20 |
| Related CRI profile controls | PR.AC-3.1PR.AC-3.2PR.AC-4.1PR.AC-4.2PR.AC-4.3PR.AC-6.1PR.AC-7.1PR.AC-7.2PR.PT-3.1PR-PT-4.1 |
| Related information | Revoke access to a table or viewallAuthenticatedUsersControl access to resources with IAM |

## Optional BigQuery controls

These controls are optional. Consider enforcing them when they apply to your specific use cases.

### Encrypt individual values in a BigQuery table

| Google control ID | BQ-CO-6.3 |
| --- | --- |
| Category | Optional |
| Description | If your organization requires that you encrypt individual values within a BigQuery table, use the Authenticated Encryption with Associated Data (AEAD) encryption functions. |
| Applicable products | BigQuery |
| Related NIST-800-53 controls | SC-13 |
| Related CRI profile controls | PR.DS-5.1 |
| Related information | AEAD encryption functions |

### Use authorized views for BigQuery datasets

| Google control ID | BQ-CO-6.4 |
| --- | --- |
| Category | Optional |
| Description | Authorized views let you share a subset of data in a dataset to specific users. For example, an authorized view lets you share query results with particular users and groups without giving them access to the underlying source data. |
| Applicable products | BigQuery |
| Related NIST-800-53 controls | AC-3AC-12AC-17AC-20 |
| Related CRI profile controls | PR.AC-3.1PR.AC-3.2PR.AC-4.1PR.AC-4.2PR.AC-4.3PR.AC-6.1PR.AC-7.1PR.AC-7.2PR.PT-3.1PR-PT-4.1 |
| Related information | Authorized views |

### Use BigQuery column-level security

| Google control ID | BQ-CO-6.5 |
| --- | --- |
| Category | Optional |
| Description | Use BigQuery column-level security to create policies that check at query time whether a user has proper access. BigQuery provides fine-grained access to sensitive columns using policy tags or type-based classification of data. |
| Applicable products | BigQuery |
| Related NIST-800-53 controls | AC-3AC-12AC-17AC-20 |
| Related CRI profile controls | PR.AC-3.1PR.AC-3.2PR.AC-4.1PR.AC-4.2PR.AC-4.3PR.AC-6.1PR.AC-7.1PR.AC-7.2PR.PT-3.1PR-PT-4.1 |
| Related information | Introduction to column-level access control |

### Use BigQuery row-level security

| Google control ID | BQ-CO-6.6 |
| --- | --- |
| Category | Optional |
| Description | Use row-level security and access policies to enable fine-grained access control to a subset of data in a BigQuery table. |
| Applicable products | BigQuery |
| Related NIST-800-53 controls | AC-3AC-12AC-17AC-20 |
| Related CRI profile controls | PR.AC-3.1PR.AC-3.2PR.AC-4.1PR.AC-4.2PR.AC-4.3PR.AC-6.1PR.AC-7.1PR.AC-7.2PR.PT-3.1PR-PT-4.1 |
| Related information | Introduction to row-level access control |

### Use BigQuery resource charts

| Google control ID | BQ-CO-7.1 |
| --- | --- |
| Category | Optional |
| Description | BigQuery resource charts let BigQuery administrators observe how their organization, folder, or reservation uses BigQuery slots and how their queries perform. |
| Applicable products | BigQuery |
| Related NIST-800-53 controls | AC-3AC-12AC-17AC-20 |
| Related CRI profile controls | PR.AC-3.1PR.AC-3.2PR.AC-4.1PR.AC-4.2PR.AC-4.3PR.AC-6.1PR.AC-7.1PR.AC-7.2PR.PT-3.1PR-PT-4.1 |
| Related information | Monitor health, resource utilization, and jobs |

## What's next

- Review [Cloud Billing
  controls](https://cloud.google.com/docs/security/security-best-practices-genai/billing-controls).
- See more [Google Cloud security best practices and guidelines for generative
  AI workloads](https://cloud.google.com/docs/security/security-best-practices-genai/common-genai-controls).

---

# Cloud Billing controls for generative AI use casesStay organized with collectionsSave and categorize content based on your preferences.

> Review the recommended Google Cloud security best practices and guidelines that aren&#39;t specific to genAI workloads that use Cloud Billing.

# Cloud Billing controls for generative AI use casesStay organized with collectionsSave and categorize content based on your preferences.

This document includes the best practices and guidelines for Cloud Billing when
running generative AI workloads on Google Cloud. Use
[Cloud Billing](https://cloud.google.com/billing/docs/concepts) with Vertex AI to
review usage and billing of the Vertex AI workloads.

## Recommended Cloud Billing controls

The following controls are recommended when using Cloud Billing.

### Configure billing alerts

| Google control ID | CB-CO-6.1 |
| --- | --- |
| Category | Recommended |
| Description | Avoid surprises on your bill by creating Cloud Billing budgets to monitor all of your Google Cloud charges in one place. After you've established a budget amount, set budget alert threshold rules on a per-project basis to trigger email notifications. These notifications help you track your spending against your budget. You can also use Cloud Billing budgets to automate cost-control responses. |
| Applicable products | Cloud Billing |
| Related NIST-800-53 controls | SI-4SI-5 |
| Related CRI profile controls | PR.DS-5.1PR.DS-8.1ID.RA-1.1DE.CM-1.1DE.CM-1.2DE.CM-1.3DE.CM-1.4DE.CM-5.1DE.CM-6.1DE.CM-6.2DE.CM-6.3DE.CM-7.1DE.CM-7.2DE.CM-7.3DE.CM-7.4DE.DP-2.1DE.DP-3.1DE.DP-4.1DE.DP-4.2DE.DP-5.1DE.AE-2.1DE.AE-3.1DE.AE-3.2DE.AE-4.1ID.RA-1.1ID.RA-2.1ID.RA-3.1ID.RA-3.2ID.RA-3.3 |
| Related information | Create, edit, or delete budgets and budget alerts |

## Optional Cloud Billing controls

You can optionally implement the following controls based on your organization's requirements.

### Export billing data for detailed analysis

| Google control ID | CB-CO-6.2 |
| --- | --- |
| Category | Optional |
| Description | For further billing analysis, you can export Google Cloud billing data to BigQuery or a JSON file. For example, you can automatically export detailed data, such as usage, cost estimates, and pricing, throughout the day to a BigQuery dataset that you specify. You can then access your Cloud Billing data from BigQuery for detailed analysis, or use a tool like Looker Studio to visualize your data. |
| Applicable products | BigQuery Data Transfer ServiceBigQueryCloud Billing |
| Related NIST-800-53 controls | SI-4SI-5 |
| Related CRI profile controls | PR.DS-5.1PR.DS-8.1ID.RA-1.1DE.CM-1.1DE.CM-1.2DE.CM-1.3DE.CM-1.4DE.CM-5.1DE.CM-6.1DE.CM-6.2DE.CM-6.3DE.CM-7.1DE.CM-7.2DE.CM-7.3DE.CM-7.4DE.DP-2.1DE.DP-3.1DE.DP-4.1DE.DP-4.2DE.DP-5.1DE.AE-2.1DE.AE-3.1DE.AE-3.2DE.AE-4.1ID.RA-1.1ID.RA-2.1ID.RA-3.1ID.RA-3.2ID.RA-3.3 |
| Related information | Export Cloud Billing data to BigQuery |

## What's next

- Review [Cloud Build
  controls](https://cloud.google.com/docs/security/security-best-practices-genai/build-controls).
- See more [Google Cloud security best practices and guidelines for generative
  AI workloads](https://cloud.google.com/docs/security/security-best-practices-genai).
