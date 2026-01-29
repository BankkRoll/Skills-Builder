# Cloud HSM architectureStay organized with collectionsSave and categorize content based on your preferences. and more

# Cloud HSM architectureStay organized with collectionsSave and categorize content based on your preferences.

# Cloud HSM architectureStay organized with collectionsSave and categorize content based on your preferences.

*This content was last updated in October 2025 and represents the status quo as
of the time that it was written. Google's security policies and systems may
change going forward, as we continually improve protection for our customers.*

Cloud HSM is part of the Cloud Key Management Service (Cloud KMS) architecture, and
provides the backend for provisioning and managing hardware-protected keys. To
help you meet corporate and compliance regulations, Cloud HSM lets you
generate your encryption keys and perform cryptographic operations in FIPS
140-2 Level 3 certified hardware security modules (HSM).

Cloud HSM provides two protection levels for hardware-backed keys:

- **Multi-tenant Cloud HSM**: Multi-tenant keys are housed on clusters of
  HSMs that serve multiple Google Cloud customers.
- **Single-tenant Cloud HSM**: Single-tenant keys are housed in dedicated
  partitions on clusters of HSMs, where each partition serves only one
  customer. You create and manage your own Single-tenant Cloud HSM
  instances, which are cryptographically isolated from other
  Google Cloud customers. Single-tenant Cloud HSM instances incur
  additional costs compared to Multi-tenant Cloud HSM keys. For more
  information, see [Single-tenant Cloud HSM](https://cloud.google.com/kms/docs/single-tenant-hsm).

Throughout this guide, references to Cloud HSM refer to both
Multi-tenant Cloud HSM and Single-tenant Cloud HSM.

This paper describes Cloud HSM architecture, including how the hardware
is managed and keys are attested and created. For more information about
Cloud KMS, see [Cloud Key Management Service encryption](https://cloud.google.com/docs/security/key-management-deep-dive).

## Overview

Cryptographic operations include the following:

- Encrypting data at rest
- Protecting the private keys for
  [Certificate Authority Service](https://cloud.google.com/certificate-authority-service)
- Protecting data encryption keys so that they can be stored together with the encrypted data
- Generating and using asymmetric keys for cryptographic operations such as
  digital signatures and authentication

Cloud HSM uses Marvell LiquidSecurity HSMs (models
CNL3560-NFBE-2.0-G and CNL3560-NFBE-3.0-G) with the firmware versions 3.4 build
09. For more information about our certification, see
[Certificate #4399](https://csrc.nist.gov/projects/cryptographic-module-validation-program/Certificate/4399).
For information about the HSM devices and hardware-protected
keys, see [key attestation](https://cloud.google.com/kms/docs/attest-key).

Multi-tenant Cloud HSM is fully managed so that you can protect your
workloads without the operational overhead of managing an HSM cluster.
Single-tenant Cloud HSM is jointly managed between your instance
administrators and Google. The Cloud HSM service provides the following
advantages:

- Global availability
- A consistent and unified API
- Automatic scaling based on your use
- Centralized management and regulatory compliance

Multi-tenant Cloud HSM is available in many Google Cloud regions around the
globe, including multi-regions that span larger geographies.
Single-tenant Cloud HSM is available in a subset of these regions. You must
use the Cloud KMS service endpoint to create and use hardware-protected
keys in Cloud HSM to protect your data, including data that you store
in other Google Cloud services, such as BigQuery, Cloud Storage, and
Persistent Disk.

With Cloud HSM, you can use hardware-protected keys without having to
manage HSM hardware yourself. Google owns and manages the HSM hardware,
including deployment, configuration, monitoring, patching, and maintenance. When
you use Cloud HSM, your data is strictly isolated from other tenants
and services in Google Cloud. The Cloud HSM data plane API, which is
part of the Cloud Key Management Service API, lets you manage hardware-protected keys
programmatically.

Cloud HSM supports hardware-protected [customer-managed encryption keys
(CMEKs)](https://cloud.google.com/kms/docs/cmek), wherever CMEKs are supported by Google Cloud services.
For example, you can encrypt data in Cloud Storage buckets or
Cloud SQL tables using a Cloud HSM
key that you manage. Multi-tenant Cloud HSM also supports
Cloud KMS Autokey for streamlined creation and management of CMEKs.

## Cloud HSM management

Within Cloud HSM, clusters of HSMs are maintained by Google
site reliability engineers (SREs) and technicians who work in each Google Cloud
data center location. Google handles physical security, logical security,
infrastructure, capacity planning, geo-expansion, and data center
disaster-recovery planning.

### Abstraction of HSM hardware

Typically, applications communicate directly with HSMs using both PKCS#11 and a
cluster management API. This communication requires that you maintain
specialized code for workloads that use or manage hardware-protected keys.

Cloud HSM abstracts communication away from the HSM by proxying
requests for hardware-protected keys through the Cloud Key Management Service API. The abstraction
reduces the need for HSM-specific code. Cloud HSM inherits tight
integration with Cloud KMS.

Tight integration with Cloud KMS provides substantial security
benefits. The Cloud Key Management Service API significantly reduces the breadth of the HSM interface
available, reducing risk in the case of a customer security breach. For example,
an attacker would be unable to wipe entire HSMs. By default, attempts to destroy
individual keys are mitigated through a default [30-day safety
period](https://cloud.google.com/kms/docs/destroy-restore). You can set the
`constraints/cloudkms.minimumDestroyScheduledDuration` organization policy to
enforce a minimum length for the *scheduled for destruction* duration for new
keys and the `constraints/cloudkms.disableBeforeDestroy` organization policy to
delete key versions only when they are disabled. For more information, see
[Control key version destruction](https://cloud.google.com/kms/docs/control-key-destruction).

You can control access to HSM resources using
[Identity and Access Management (IAM)](https://cloud.google.com/iam/docs). IAM configuration is
less likely to suffer from misconfigurations and bugs than a custom HSM
solution. In addition to IAM controls, managing a
Single-tenant Cloud HSM instance also requires two-factor authentication
(2FA) from a [quorum of at least two designated
approvers](https://cloud.google.com/kms/docs/single-tenant-hsm#quorum). When you create an instance, you
decide how many approvals are required for every change to a
Single-tenant Cloud HSM instance. Approvals require challenges that are
signed with private key material that you create outside of Google Cloud.

The following diagram shows the Cloud HSM architecture.

![Cloud HSM architecture diagram.](https://cloud.google.com/static/docs/security/cloud-hsm-architecture/images/hsm-hardware.svg)

### Strict geographic separation, by design

In Multi-tenant Cloud HSM, you can choose to make keys globally available or
to enforce strict geographic restrictions on keys that require restrictions.
Single-tenant Cloud HSM is only available in individual regions.

Often, HSMs are divided into partitions, so that a single physical device can
operate as multiple logical devices. You might use partitions to reduce
deployment costs in cases where you need to separate HSM administration and
keys. The following diagram shows Multi-tenant Cloud HSM partitions in three
regions.

![Diagram of Cloud HSM geography using Multi-tenant Cloud HSM partitions.](https://cloud.google.com/static/docs/security/cloud-hsm-architecture/images/hsm-geography.svg)

To isolate the keys for each region and multi-region, each Cloud HSM
region is associated with a separate HSM regional wrapping key (see diagram in
[Creating keys](#creating-keys)). To support high availability, the wrapping key
is cloned onto partitions in each HSM that is physically located in the region.
HSM regional keys don't leave the HSM in that location. Cloning lets HSMs in the
same region serve the same set of customer keys, and ensures that HSMs outside
the region cannot serve those keys.

Cloud HSM also creates multi-regions using wrapping keys. All customer
keys for a multi-region are wrapped using a wrapping key present on a partition
in all locations that constitute the multi-region. The service uses the
same hardware for multi-regions, but provides the same strong isolation between
regions and multi-regions that exists between different regions.

The regionalization scheme requires that wrapping keys are only replicated to
appropriate partitions. Each configuration change must be approved by multiple
members of the Cloud HSM team before it becomes active. Data center
technicians can't access an HSM configuration, runtime, or storage.

When you create keys in a Single-tenant Cloud HSM instance, the wrapping keys
on your dedicated partitions ensure that your keys can't be served outside
of your partitions or the region.

### Centralized management

In a conventional data center that hosts HSMs, management of the HSMs and their
resources is entirely separate from management of other hardware-protected keys.
Cloud HSM is tightly integrated into Google Cloud, allowing you to
seamlessly manage your Cloud HSM resources. For example, you can manage
the following:

- You manage your hardware-protected keys alongside your other keys in
  Cloud KMS and externally managed keys in
  [Cloud External Key Manager (Cloud EKM)](https://cloud.google.com/kms/docs/ekm).
- You manage access to hardware-protected keys within IAM.
- Costs for cryptographic operations using hardware-protected keys
  are reported in Cloud Billing.
- You can use hardware-protected keys transparently in all Google Cloud
  services that support encrypting resources using CMEK. CMEK integrations
  require the CMEK key and the data it encrypts to be located in compatible
  geographic locations. Because of the strict geographic restriction of the
  Cloud HSM keys, all encryption and decryption of the CMEK data are
  also geographically restricted.
- Administrative operations on hardware-protected keys are always logged at
  the API layer in Cloud Audit Logs. You can choose to enable data-access
  logging as well. For more information, see
  [Cloud KMS audit logging information](https://cloud.google.com/kms/docs/audit-logging).
- Google works directly with the HSM manufacturer to keep the hardware and
  software on each HSM updated, and to find and fix issues in real time. In
  the event of a zero-day exploit on the HSM, Google can selectively disable
  affected code paths on affected HSM clusters until the exploit is fixed.
- You can track your keys, including your hardware-protected keys and the
  resources that they encrypt using [key usage tracking
  dashboards](https://cloud.google.com/kms/docs/view-key-usage).

## Developer and user experience

Because Google is responsible for HSM management, Cloud HSM offers
significant benefits to developers and end users. When you use
Multi-tenant Cloud HSM, you don't have to do anything to maintain your HSM
clusters. When you use Single-tenant Cloud HSM, you are responsible for
ongoing cluster maintenance operations using the gcloud CLI.

There are four main user personas for using Cloud HSM:

- **End users**: Cloud HSM is usually transparent to end users of your
  products and resources. For example, if your Google Cloud resources
  are protected with a CMEK, the data is automatically encrypted and decrypted
  as needed for your users by service agents.
- **Developers**: Your developers use your Cloud HSM keys. If you use
  Autokey, your developers can request new keys on-demand. If
  you don't use Autokey, your Cloud KMS administrators
  create and manage keys for your developers to use.
- **Cloud KMS administrators**: Your Cloud KMS
  administrators are responsible for creating and rotating your
  Cloud HSM keys. They can also manage your Autokey settings
  or organization policies, if these responsibilities are not handled by
  dedicated organization administrators.
- **Single-tenant Cloud HSM administrators**: If you use
  Single-tenant Cloud HSM, you must have a team of administrators that you
  trust to approve creation and maintenance operations on your
  Single-tenant Cloud HSM instances. Separate IAM roles
  control who is authorized to propose, approve, and execute changes to your
  instance. Changes can't be applied without prior approval, which requires
  quorum authentication using 2FA keys.

### HSMs at Google scale

When you rely on hardware that exists on-premises or in data centers, the
hardware can create a performance bottleneck or become a single point of
failure. Cloud HSM is designed to be extremely resilient to
unpredictable workloads and hardware failures. The Cloud HSM backend
uses a pool of HSMs in [each region](https://cloud.google.com/kms/docs/locations#hsm-regions)
to ensure high availability and scalability. This pool of HSMs lets
Cloud HSM also provide high throughput. For more information, see
[Monitor and adjust Cloud KMS quotas](https://cloud.google.com/kms/docs/monitor-adjust-quotas).

All customer keys are stored wrapped with a regional wrapping key in the
Cloud KMS database and can only be unwrapped by an HSM in the region as
part of a cryptographic operation. This wrapping has the following benefits:

- A key's durability is not tied to a specific HSM or subset of HSMs in a
  region.
- Each Cloud HSM customer experiences the full scale and availability
  of the Cloud HSM clusters that serve their keys.
- Cloud HSM can handle a much larger set of keys that can be stored
  on an HSM.
- Adding or replacing an HSM is rapid and secure.

### Unified API design

Cloud HSM and Cloud KMS share a common management and data
plane API. The internal details of communicating with an HSM are abstracted from
the caller.

Consequently, no code changes are required to update an existing application
that uses software keys in Cloud KMS to support hardware-protected
keys. Instead, you update the resource name of the key to use.

### PKCS#11 support

You can use Cloud Key Management Service API to connect your existing applications to
Cloud HSM to manage cryptographic keys. The [PKCS#11
library](https://cloud.google.com/kms/docs/reference/pkcs11-library) lets you use hardware-protected
keys to sign your binaries and serve TLS web sessions.

## Security and regulatory compliance

Cloud HSM has obtained compliance with numerous regulations, including
[FedRAMP High](https://cloud.google.com/security/compliance/fedramp),
[C5:2020](https://cloud.google.com/security/compliance/bsi-c5), and
[OSPAR](https://cloud.google.com/security/compliance/ospar). In addition,
Cloud HSM helps you enforce regulatory compliance for your workloads in
the cloud.

### Cryptographic key attestation

Each time that you generate or import a Cloud HSM key, the HSM
generates an [attestation statement](https://cloud.google.com/kms/docs/attest-key) that is signed with a
signing key that is associated with the partition. The statement contains
information about your key's attributes. The signing key is backed by
certificate chains that are rooted in both Google and the HSM manufacturer. You
can download the attestation statement and certificates to verify the
statement's authenticity and validate properties of the key and the HSM that
generated or imported it.

The certificate chain lets you check the following:

- The HSM hardware and firmware are genuine.
- The HSM partition and HSM are managed by Google.
- The HSM is in the FIPS mode of operation.

The content of the attestation statement lets you check the following:

- The key is not extractable.
- The key was generated for your CryptoKeyVersion.
- The public key in an asymmetric key pair corresponds to a hardware-protected
  private key.
- The key material of an imported symmetric key matches the value you wrapped.

### Secure key import directly into HSMs

You can securely import existing keys into Cloud HSM to maintain a backup
of your key material outside of Google Cloud, or to simplify migrating certain
workloads to Google Cloud. The key-import process does not allow Google any
direct access to the unwrapped key material. Cloud HSM provides you with an
attestation statement for the HSM-generated wrapping key to validate that no
access occurred.

Because key import potentially creates security and compliance risks by allowing
users to bring keys from unknown sources, separate IAM roles
allow fine-grained control over who can import keys into a project. Imported
keys can be distinguished by the attestation statement that the HSM generates on
import.

For more information, see
[Importing a key into Cloud Key Management Service](https://cloud.google.com/kms/docs/importing-a-key).

### Strict security procedures safeguard HSM hardware

As mandated by FIPS 140-2 level 3, HSM devices have built-in mechanisms to help
protect against, and provide evidence of, physical tampering.

In addition to the assurances provided by the HSM hardware itself, the
infrastructure for Cloud HSM is managed according to
[Google infrastructure security design overview](https://cloud.google.com/docs/security/infrastructure/design).

The following documented and auditable procedures protect the integrity of each
HSM during provisioning, deployment, and in production:

- All HSM configurations must be verified by multiple Cloud HSM SREs
  before the HSM can be deployed into a data center.
- After an HSM is put into service, configuration change can only be
  initiated and verified by multiple Cloud HSM SREs.
- An HSM can only receive firmware that is signed by the HSM manufacturer.
- HSM hardware is not directly exposed to any network.
- Servers that host HSM hardware are prevented from running unauthorized
  processes.

The duties for system operators are defined in standard operating procedures.
System operators are prevented from accessing, using, or extracting customer key
material while performing their duties.

### Service and tenant isolation

The Cloud HSM architecture ensures that HSMs are protected from
malicious or inadvertent interference from other services or tenants.

An HSM that is part of this architecture accepts requests only from
Cloud HSM, and the Cloud HSM service accepts requests only
from the Cloud KMS service. The Cloud KMS service enforces
that callers have appropriate IAM permissions on the keys that
they attempt to use. Unauthorized requests don't reach HSMs.

Multi-tenant Cloud HSM keys are also subject to
[quotas](https://cloud.google.com/kms/quotas#cloud_hsm_quotas) for cryptographic operations. These
quotas protect your ability to run your workloads by helping to prevent
inadvertent or malicious attempts to overload the service. The default quotas
are based on observed usage patterns. The quotas are significantly below the
service capacity and can be increased upon request.

## Request flows

This section demonstrates how the Cloud HSM architecture applies in
practice by showing the steps for different types of requests. These flows
emphasize the Cloud HSM portions. For more information about steps
common to all keys, see the
[Cloud Key Management Service deep dive](https://cloud.google.com/docs/security/key-management-deep-dive).

### Creating keys

When you create a hardware-protected key, the Cloud Key Management Service API doesn't create the key
material, but requests that the HSM create it.

An HSM can only create keys in locations that it supports. For
Multi-tenant Cloud HSM, each partition on an HSM contains a wrapping key that
corresponds to a Cloud KMS location. For a Single-tenant Cloud HSM
instance, your dedicated partition uses a wrapping key that's dedicated to your
instance. The wrapping key is shared among all partitions that support the
Cloud KMS location or the Single-tenant Cloud HSM instance.

The following diagram shows how hardware-protected keys are wrapped in
Cloud KMS.

![HSM key creation diagram.](https://cloud.google.com/static/docs/security/cloud-hsm-architecture/images/hsm-key-security.svg)

The key-creation process looks like the following:

1. The [Google Front End Service
  (GFE)](https://cloud.google.com/docs/security/infrastructure/design#google-frontend-service) routes
  the key creation request to a Cloud KMS server in the location that
  corresponds to the request.
2. The Cloud Key Management Service API verifies the caller's identity, the caller's permission to
  create keys in the project, and that the caller has sufficient write request
  quota. If the caller is requesting a Single-tenant Cloud HSM key, the API
  also verifies that the selected Single-tenant Cloud HSM instance is
  available.
3. The Cloud Key Management Service API forwards the request to Cloud HSM.
4. Cloud HSM directly interfaces with the HSM. The HSM:
  1. Creates the key and wraps it with the location-specific or
    instance-specific wrapping key.
  2. Creates the attestation statement for the key and signs it with
    the partition signing key.
5. After Cloud HSM returns the wrapped key and attestation to
  Cloud KMS, the Cloud Key Management Service API wraps the HSM-wrapped key according to
  the [Cloud KMS key
  hierarchy](https://cloud.google.com/docs/security/key-management-deep-dive#software_key_hierarchy),
  then writes it to the project.

This design ensures that the key can't be unwrapped or used outside of an HSM,
can't be extracted from the HSM, and exists in its unwrapped state only within
specified locations.

### Cryptographic operations

When you perform a cryptographic operation in Cloud KMS, you don't need
to know whether you are using a hardware-protected or software-protected key.
When the
Cloud Key Management Service API detects that an operation involves a hardware-protected key, it
forwards the
request to an HSM in the same location. The following are the steps for a
cryptographic operation:

1. The [GFE](https://cloud.google.com/docs/security/infrastructure/design#google-frontend-service)
  routes the request to a Cloud KMS server in the appropriate
  location. The
  Cloud Key Management Service API verifies the caller's identity, the caller's permission to
  access the key and perform the operation, and the project's quota for
  cryptographic operations.
2. The Cloud Key Management Service API retrieves the wrapped key from the datastore and decrypts
  one level of encryption using the Cloud KMS master key. The key is
  still wrapped with the HSM wrapping key for the KMS location.
3. The Cloud Key Management Service API detects that the [protection
  level](https://cloud.google.com/kms/docs/algorithms#protection_levels) is `HSM` or
  `HSM_SINGLE_TENANT` and sends the partially unwrapped key, along with the
  inputs to the cryptographic operation, to Cloud HSM.
4. Cloud HSM directly interfaces with the HSM. The HSM completes the
  following operations:
  1. Checks that the wrapped key and its attributes have not been modified.
  2. Unwraps the key and loads it into the HSM storage.
  3. Performs the cryptographic operation and returns the result.
5. The Cloud Key Management Service API passes the result back to the caller.

Cryptographic operations using hardware-protected keys are performed entirely
within an HSM in the configured location, and only the result is visible to the
caller.

This diagram shows the difference between creating hardware-protected keys and
software-protected keys in Cloud KMS.

### CMEK integrations

All hardware-protected keys are [CMEKs](https://cloud.google.com/kms/docs/cmek). Configuring a
[CMEK-enabled service](https://cloud.google.com/kms/docs/using-other-products#cmek_integrations) to use
Cloud HSM keys is as simple as choosing a key with an `HSM` or
`HSM_SINGLE_TENANT` protection level when following the service-specific
instructions.

When a caller reads or writes data to a CMEK-enabled service, the caller doesn't
need direct permission to use the key, and the caller doesn't need to know
whether the key is stored in an HSM.

The same CMEK operation flow is used with hardware-protected keys and
software-protected keys, with the following exceptions when using
hardware-protected keys:

- The request from the CMEK-enabled service is initiated within Google's
  network, and doesn't need to traverse the GFE.
- The Cloud Key Management Service API verifies that the service account for the CMEK-enabled
  service has proper permissions to use the key. The Cloud Key Management Service API doesn't
  validate permissions on the end user of the CMEK-enabled service.

Cloud HSM is required if you want to use Autokey to provision
Cloud KMS keys. Autokey lets the Cloud KMS service
agent provision hardware-protected keys automatically on request. For more
information, see [Automatic provisioning for CMEK](https://cloud.google.com/docs/security/key-management-deep-dive#autokey).

## Use your own HSMs

The HSMs that Cloud HSM uses are managed by Google. However, under
certain circumstances, your organization might want to use your own HSMs to
store the hardware-protected keys for your workloads. For example, using your
own HSMs might help you with migrating your workloads to Google Cloud.

In certain locations only, Google offers an infrastructure HSM-as-a-service that
provides cryptographic key operations for secure cryptographic transactions in
Google Cloud. The products are known as *Bare Metal Rack HSM* and *Bare Metal
HSM*. With Bare Metal Rack HSM or Bare Metal HSM, you purchase and configure
your own HSMs and then ship them to Google data centers, so that they can be
hosted by Google. You maintain full logical access to your HSMs and must work
directly with your HSM vendor to manage and troubleshoot your devices. Google
provides physical and network security, rack space, power, and network
integration for a fee. For more information, see [Bare Metal Rack
HSM](https://cloud.google.com/kms/docs/bare-metal-rack-hsm) and [Bare Metal
HSM](https://cloud.google.com/kms/docs/bare-metal-hsm).

## What's next

To learn more, explore the following resources:

- [Cloud HSM documentation](https://cloud.google.com/kms/docs/hsm)
- [Cloud KMS documentation](https://cloud.google.com/kms/docs)
- [Cloud Key Management Service encryption](https://cloud.google.com/docs/security/key-management-deep-dive)
- [Google infrastructure security design overview](https://cloud.google.com/docs/security/infrastructure/design)
- [Data encryption at rest](https://cloud.google.com/docs/security/encryption/default-encryption)

   Was this helpful?

---

# Handle compromised Google Cloud credentialsStay organized with collectionsSave and categorize content based on your preferences.

> Discover how to secure Google Cloud credentials that have been compromised and additional Cloud protection best practices

# Handle compromised Google Cloud credentialsStay organized with collectionsSave and categorize content based on your preferences.

Google Cloud credentials control access to your resources hosted
on Google Cloud. To help keep your data secure and protected from
attackers, you must handle
your credentials with utmost care.

We recommend that you protect all of your Google Cloud credentials from
unintended access. These
credentials include but are not limited to the following:

- Service credentials:
  - [Service account private keys](https://cloud.google.com/iam/docs/keys-create-delete)
    (JSON and p12 files)
  - [API keys](https://cloud.google.com/docs/authentication/api-keys)
  - [OAuth2 client ID
    secrets](https://developers.google.com/identity/protocols/oauth2)
- User credentials that are created and managed on developer workstations or
  other computers:
  - [Google Cloud CLI credentials](https://cloud.google.com/sdk/docs/authorizing)
  - [Application Default Credentials](https://cloud.google.com/docs/authentication#adc)
  - Browser cookies

Google Cloud CLI credentials are stored in the
user's home directory. You can list them in Google Cloud CLI using the `gcloud
auth list` command.
Application Default Credentials are stored on the developer's workstation.
Browser cookies are browser-specific, but are typically stored on the developer's
workstation.

If you suspect that any of your credentials have been compromised, you must
take immediate action to limit the impact of the compromise on your
Google Cloud account.

## Monitor for credential compromise

To monitor for potential compromise, consider the following:

- Monitor for suspicious account activity such as privilege escalation and
  multiple account creations. Monitor for these activities using
  [Cloud Audit Logs](https://cloud.google.com/logging/docs/audit),
  [Policy Intelligence](https://cloud.google.com/policy-intelligence/docs/overview) and
  [Security Command Center](https://cloud.google.com/security-command-center/docs/security-command-center-overview).
  Use the following Security Command Center services and capabilities:
  - [Event Threat Detection](https://cloud.google.com/security-command-center/docs/concepts-event-threat-detection-overview)
    to identify threats that are based on administrator activities, Groups
    changes, and Identity and Access Management (IAM) permission changes. For each threat
    category, [recommended investigation
    steps](https://cloud.google.com/security-command-center/docs/how-to-investigate-threats) are
    provided to aid in your response.
  - [Sensitive Actions
    Service](https://cloud.google.com/security-command-center/docs/concepts-sensitive-actions-overview)
    to track actions in your organization, folders, and projects that could be
    damaging to your business if they are taken by a malicious actor.
  - [Cloud Infrastructure Entitlement Management
    (CIEM)](https://cloud.google.com/security-command-center/docs/ciem-overview) (Preview) to manage
    access for identities and generate findings for misconfigurations.
- Monitor user logins in
  [Google Workspace](https://support.google.com/a/answer/6000239) and
  [Cloud Identity](https://support.google.com/cloudidentity/answer/7420688).
  To better track issues, consider exporting the logs to
  [Cloud Logging](https://cloud.google.com/logging/docs/audit/configure-gsuite-audit-logs).
- Monitor for secrets in your code repositories, using tools such as [Anomaly
   Detection](https://cloud.google.com/security-command-center/docs/concepts-security-sources#anomaly_detection)
   or
  [secret scanning](https://docs.github.com/en/code-security/secret-scanning/about-secret-scanning).
- Monitor for anomalies in service account key usage using
  [Cloud Monitoring](https://cloud.google.com/iam/docs/service-account-monitoring) or CIEM.

Ensure that your security operations center (SOC) is notified promptly and has
the playbooks, tools, and access that are required to respond quickly to a
suspected credential compromise. Use the
[Security Command Center Enterprise tier](https://cloud.google.com/security-command-center/docs/service-tiers)
to enable SIEM and SOAR capabilities such as playbooks, response workflows, and
automated actions. You can also integrate
[Security Command Center with your existing SIEM](https://cloud.google.com/security-command-center/docs/how-to-configure-scc-splunk)
or [import logs into Google Security Operations](https://cloud.google.com/chronicle/docs/ingestion/cloud/ingest-gcp-logs)
for further analysis.

## Protect your Google Cloud resources from a compromised credential

Complete the steps in the following sections as soon as you can to help protect
your resources if you suspect a credential is compromised.

### Revoke and reissue credentials

If you suspect a credential is compromised, revoke and re-issue it. Proceed
carefully to ensure you don't suffer a service outage as a result of revoking
credentials.

In general, to reissue credentials, you generate a new credential, push it to
all services and users that need it, and then revoke the old credential.

The following sections provide specific instructions for each type of
credential.

#### Replace a service account key

1. In the Google Cloud console, go to the **Service accounts** page.
  [Go to Service accounts](https://console.cloud.google.com/iam-admin/serviceaccounts)
2. Locate the affected service account.
3. Create a new key for the service account.
4. Push the new key to all the locations in which the old key was in use.
5. Delete the old key.

For more information, see [Create service
accounts](https://cloud.google.com/iam/docs/service-accounts-create).

#### Regenerate API keys

1. In the Google Cloud console, go to the **Credentials** page.
  [Go to Credentials](https://console.cloud.google.com/apis/credentials)
2. Create a new API key using the **Create credentials** button. Configure the
  new key to be the same as the compromised API key. The restrictions on the API
  key must match; otherwise you might suffer an outage.
3. Push the API key to all locations in which the old key was in use.
4. Delete the old key.

For more information, see [Authenticate by using API
keys](https://cloud.google.com/docs/authentication/api-keys).

#### Reset an OAuth2 client ID secret

Changing a client ID secret will cause a temporary outage while the
secret is rotated.

1. In the Google Cloud console, go to the **Credentials** page.
  [Go to Credentials](https://console.cloud.google.com/apis/credentials)
2. Select the compromised OAuth2 client ID and edit it.
3. Click **Reset Secret**.
4. Push the new secret to your application.

For more information, see [Setting up OAuth
2.0](https://support.google.com/cloud/answer/6158849) and [Using OAuth 2.0 to
access Google APIs](https://developers.google.com/identity/protocols/oauth2).

#### Remove Google Cloud CLI credentials as an administrator

As a Google Workspace administrator, remove access to Google Cloud CLI from the
user's list of connected apps. For more information, see [View and remove access
to third-party
applications](https://support.google.com/a/answer/2537800#zippy=%2Cview-and-remove-access-to-third-party-applications).

When the user accesses Google Cloud CLI again, it will automatically ask
them to re-authorize the application.

#### Remove Google Cloud CLI credentials as a user

1. Open the list of [apps with access to your Google Account](https://myaccount.google.com/permissions).
2. Remove Google Cloud CLI from the list of connected apps.

When you access Google Cloud CLI again, it will automatically ask
you to re-authorize the application.

#### Revoke Application Default Credentials as an administrator

If you suspect that an Application Default Credential is
compromised, you can revoke it. This procedure can cause a temporary outage
until the credentials file is recreated.

As a Google Workspace administrator, remove access to the
Google Auth Library from the user's list of connected apps. For more
information, see [View and remove access to third-party
applications](https://support.google.com/a/answer/2537800#zippy=%2Cview-and-remove-access-to-third-party-applications).

#### Revoke Application Default Credentials as a user

If you suspect that an Application Default Credential that you created is
compromised, you can revoke it. This procedure can cause a temporary outage
until the credentials file is recreated. This procedure can only be completed by
the owner of the compromised credential.

1. [Install and initialize the Google Cloud CLI](https://cloud.google.com/sdk/docs/install), if you
  haven't
  already.
2. Authorize gcloud CLI with your user identity, not with a service
  account:
  ```
  gcloud auth login
  ```
  For more information, see [Authorize the
   gcloud CLI](https://cloud.google.com/sdk/docs/authorizing).
3. Revoke the credentials:
  ```
  gcloud auth application-default revoke
  ```
4. Optionally, delete the
  `application_default_credentials.json` file. The location depends on your
  operating system:
  - Linux, macOS: `$HOME/.config/gcloud/`
  - Windows: `%APPDATA%\gcloud\`
5. Recreate the credentials file:
  ```
  gcloud auth application-default login
  ```

#### Invalidate browser cookies as an administrator

If you suspect browser cookies are compromised, Google Workspace administrators
can [sign a user out](https://support.google.com/a/answer/178854) of their
account.

In addition, immediately [force a password change](https://support.google.com/a/answer/2537800#zippy=%2Creset-a-users-password).

These actions invalidate all
existing cookies, and the user is asked to sign in again.

#### Invalidate browser cookies as a user

If you suspect browser cookies are compromised, sign out of your [Google
Account](https://accounts.google.com) and change your password immediately.

These actions invalidate all your existing cookies. The next time you access
Google Cloud, you must sign in again.

### Look for unauthorized access and resources

After you revoke compromised credentials and restored your service, review all
access to your Google Cloud resources. You can use Logging
or Security Command Center.

In Logging, complete the following:

1. Examine your [audit logs](https://cloud.google.com/logging/docs/audit) in the
  Google Cloud console.
  [Go to Logs Explorer](https://console.cloud.google.com/logs/query)
2. Search all potentially affected resources, and make sure that all
  account activity (especially related to the compromised credentials) are
  as expected.

In Security Command Center, complete the following:

1. In the Google Cloud console, go to the Security Command Center **Findings** page.
  [Go to Findings](https://console.cloud.google.com/security/command-center/findings)
2. If necessary, select your Google Cloud project or organization.
3. In the **Quick filters** section, click an appropriate filter to display
  the finding that you need in the **Findings query results** table. For
  example, if you select **Event Threat Detection** or **Container Threat Detection**
  in the **Source display name** subsection, only findings from the
  selected service appear in the results.
  The table is populated with findings for the source you selected.
4. To view details of a specific finding, click the finding name under
  **Category**. The finding details pane expands to display a summary
  of the finding's details.
5. To display all findings that were caused by the same user's actions:
  1. On the finding details pane, copy the email address next to
    **Principal email**.
  2. Close the pane.
  3. In **Query editor**, enter the following query:
    ```
    access.principal_email="USER_EMAIL"
    ```
    Replace
    USER_EMAIL with the email address that you
    previously copied.
    Security Command Center displays all findings that are associated with actions
    taken by the user that you specified.

### Delete all unauthorized resources

Make sure that there are no unexpected resources, such as VMs, App Engine
apps, service accounts, Cloud Storage buckets, and so forth,
that the compromised credential could access.

After you are satisfied that you have identified all unauthorized resources, you
can choose to delete these resources immediately. This is especially important
for
Compute Engine resources, because attackers can use compromised accounts to
exfiltrate data or otherwise
compromise your production systems.

Alternatively, you can try to isolate unauthorized resources to allow your own
forensics teams to perform additional analysis.

### Contact Cloud Customer Care

For help with finding the Google Cloud logs and tools that you require for your
investigation and mitigation steps, contact [Customer Care](https://cloud.google.com/support)
and open a [support case](https://cloud.google.com/support/docs/customer-care-procedures#create_a_support_case).

## Best practices to avoid compromised credentials

This section describes best practices that you can implement to help you avoid
compromised credentials.

### Separate credentials from code

Manage and store your credentials separately from your source code. It is
extremely common to accidentally push both credentials and source code to a
source management site like GitHub, which makes your credentials vulnerable to
attack.

If you are using GitHub or other public repository, you can implement tools such
as [Anomaly
Detection](https://cloud.google.com/security-command-center/docs/concepts-security-sources#anomaly_detection)
or [secret
scanning](https://docs.github.com/en/code-security/secret-scanning/about-secret-scanning),
which warns you about exposed secrets in your GitHub repositories. To stop keys
from being committed to your GitHub repositories, consider using tools such as
[git-secrets](https://github.com/awslabs/git-secrets).

Use secret management solutions such as [Secret
Manager](https://cloud.google.com/secret-manager/docs/overview) and [Hashicorp
Vault](https://www.vaultproject.io/) to store your secrets, rotate them
regularly, and apply least privilege.

### Implement service account best practices

To help protect service accounts, review the
[best practices for working with service accounts](https://cloud.google.com/iam/docs/best-practices-service-accounts).

### Limit session lengths

To force periodic re-authentication, limit the time that sessions remain active
for Google and Google Cloud accounts. For more information, see the
following:

- [Set session length for Google Workspace](https://support.google.com/a/answer/7576830)
- [Set session length for Google Cloud services](https://support.google.com/a/answer/9368756)
- [Set session length for Cloud Identity](https://support.google.com/cloudidentity/answer/7576830)

### Use VPC Service Controls to limit access

To limit the impact of compromised
credentials, create [service perimeters using VPC Service Controls](https://cloud.google.com/vpc-service-controls/docs/overview). When you configure VPC Service Controls,
resources inside the perimeter can only communicate with other resources inside
the perimeter.
