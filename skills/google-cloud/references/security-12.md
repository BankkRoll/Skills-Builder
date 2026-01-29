# Cloud Key Management Service encryptionStay organized with collectionsSave and categorize content based on your preferences.

# Cloud Key Management Service encryptionStay organized with collectionsSave and categorize content based on your preferences.

> Whitepaper that describes how Cloud KMS architecture provides Google key management of HSM, CMEK, BYOK, and Autokeys for data-at-rest encryption.

# Cloud Key Management Service encryptionStay organized with collectionsSave and categorize content based on your preferences.

*This content was last updated in January 2025, and represents the status quo
as of the time it was written. Google's security policies and systems may change
going forward, as we continually improve protection for our customers.*

This document describes how Cloud Key Management Service (Cloud KMS) provides
key management services in Google Cloud for data-at-rest encryption.
Google Cloud works off the fundamental premise that Google Cloud customers own
their data and should control how it is used.

When you store data with Google Cloud, your data is [encrypted at
rest](https://cloud.google.com/docs/security/encryption/default-encryption) by default. When you use the
Cloud KMS platform, you can gain greater control over
how your data is encrypted at rest and how your encryption keys are managed.

This document focuses on the inner workings of the Cloud KMS platform.
These options help you protect the keys and other confidential data that you
store in Google Cloud. This document is intended for technical decision
makers who need details about Cloud KMS architecture, infrastructure,
and features. This document assumes that you have a basic understanding of
encryption concepts and cloud architectures.

## Keys in Google Cloud

The following table describes the different types of keys in Google Cloud.

| Type of key | Cloud KMS Autokey | Cloud KMS customer-managed (manual) | Google-owned and Google-managed encryption key (Google default encryption) |
| --- | --- | --- | --- |
| Can view key metadata | Yes | Yes | No |
| Ownership of keys1 | Customer | Customer | Google |
| Can manage2and control3keys | Key creation and assignment is automated. Customer manual control is
fully supported. | Customer, manual control only | Google |
| Supports regulatory requirements for customer-managed keys | Yes | Yes | No |
| Key sharing | Unique to a customer | Unique to a customer | Data from multiple customers is typically protected by shared key encryption
keys (KEKs). |
| Control of key rotation | Yes | Yes | No |
| CMEK
organization policies | Yes | Yes | No |
| Log
administrative and data access to encryption keys | Yes | Yes | No |
| Logical data separation through encryption | Yes | Yes | No |
| Pricing | Varies | Varies | Free |

1 The owner of the key indicates who holds the
rights to the key. Keys that you own have tightly restricted access or no access
by Google.

2 Management of keys includes the following
tasks:

- Create keys.
- Choose the protection level of the keys.
- Assign authority for management of the keys.
- Control access to keys.
- Control usage of keys.
- Set and modify the rotation period of keys, or trigger a rotation of keys.
- Change key status.
- Destroy key versions.

3 Control of keys means setting controls on the
kind of keys and how the keys are used, detecting variance, and planning
corrective action if needed. You can control your keys, but delegate management
of the keys to a third party.

## Cloud KMS principles

With Cloud KMS, Google's focus is to provide a scalable, reliable, and
performant solution, with the widest spectrum of options that you can control.
Cloud KMS is supported by the following principles:

- **Customer control:** Cloud KMS lets you control your own
  software and hardware keys for encryption and signing. This pillar includes
  support for bring-your-own-keys (BYOK) and hold-your-own-keys (HYOK).
- **Access control and monitoring:** With Cloud KMS, you can
  manage permissions on individual keys and monitor how the keys are used.
- **Regionality:** Cloud KMS offers regionalization out of the
  box. The service is configured to create, store, and process keys only in
  the Google Cloud location that you select.
- **Backups:** To help guard against data corruption and to verify that
  data can be decrypted successfully, Cloud KMS periodically scans
  and backs up all key material and metadata.
- **Security:** Cloud KMS offers strong protection against
  unauthorized access to keys and is fully integrated with
  Identity and Access Management (IAM) and Cloud Audit Logs controls.
- **Logical data separation:** Cloud KMS encryption provides *logical
  data separation* through encryption. Logical data separation means that data
  owners don’t share encryption keys (KEKs and DEKs).

## Sources and management options for cryptographic keys

The Cloud KMS platform lets you manage cryptographic keys in a central
cloud service for direct use or for use by other cloud resources and
applications.

The Google Cloud portfolio for keys include the following:

- **Default encryption:** All data that is stored by Google is encrypted
  at the storage layer using the Advanced Encryption Standard (AES)
  algorithm, AES-256. We generate and manage the keys for default encryption,
  and customers don't have access to the keys or control of key rotation and
  management. Default encryption keys might be shared among customers. For
  more information, see
  [Default encryption at rest](https://cloud.google.com/docs/security/encryption/default-encryption).
- **Cloud KMS with software-protected keys:** You can control the
  keys that are generated in Cloud KMS. The Cloud KMS
  software backend gives you the flexibility to encrypt or sign your data with
  either a symmetric or asymmetric key that you control.
- **Cloud KMS with hardware-protected keys (Cloud HSM):**
  Using Cloud KMS with the Cloud HSM backend, you can own keys
  that are generated and stored in Google-owned and operated hardware security
  modules (HSMs). If you require a hardware-protected key, you can use the
  Cloud HSM backend to help ensure that your keys are only used in [FIPS
  140-2 Level 3](https://wikipedia.org/wiki/FIPS_140-2#Level_3)–validated
  HSMs. You can provision hardware-protected keys using a manual method that
  requires a Cloud KMS administrator or automatically using
  [Cloud KMS Autokey](https://cloud.google.com/kms/docs/kms-autokey). Autokey lets you
  automate the key provisioning and key assignment processes for
  customer-managed encryption keys (CMEK). Conventional HSM keys require that
  a KMS administrator creates the keys on request.
- **Cloud KMS with key import:** To satisfy BYOK requirements,
  you can import
  [your own cryptographic keys](https://cloud.google.com/kms/docs/key-import)
  that you generate yourself. You can use and manage these keys outside of
  Google Cloud, and use the key material in Cloud KMS to
  encrypt or sign data that you store in Google Cloud.
- **Cloud KMS with external key manager
  (Cloud EKM):**
  To satisfy HYOK requirements, you can create and control keys that are
  stored in a key manager that is external to Google Cloud. You then
  set up the Cloud KMS platform to use the external keys to help
  protect your data at rest. You can use these encryption keys with a
  Cloud EKM key. For more information about external key management
  and Cloud EKM, see
  [Reference architectures for Cloud EKM](https://cloud.google.com/kms/docs/ekm-architectures).

You can choose to use keys that are generated by Cloud KMS with other
Google Cloud services. Such keys are known as
[CMEKs](#cmek). The CMEK feature lets you generate, use, rotate, and destroy
encryption keys that help protect your data in other Google Cloud
services. When you use CMEK with Google Cloud services, key access and
tracking is managed for you.

## Encryption and key management at Google

This section defines some terms for key management in the context of Google's
multi-layered key management infrastructure.

### Key rings, keys, and key versions

The following diagram illustrates key groupings, and shows key rings, and keys
with a single primary version and multiple previous versions.

![Diagram of key groupings.](https://cloud.google.com/static/docs/security/key-management-deep-dive/images/kms-keys-keyrings.svg)

The concepts that are shown in the preceding diagram are the following:

- **Key:** A named object representing a
  [cryptographic key](https://cloud.google.com/kms/docs/resource-hierarchy#keys)
  that is used for a specific purpose. The key material—the actual bits used
  for cryptographic operations—can change over time as you create new key
  versions.  You can assign IAM allow policies at the key level in the
  resource hierarchy.
  The key purpose and other attributes of the key are connected with and
  managed using the key. Thus, the key is the most important object for
  understanding KMS usage.
  Cloud KMS supports both asymmetric keys and symmetric keys. A
  symmetric key is used for creating or validating MAC signatures or for symmetric encryption to protect some corpus of data. For example, you can
  use AES-256 in GCM mode to encrypt a block of plaintext. An asymmetric key
  can be used for asymmetric encryption or asymmetric signing. For more
  information, see
  [Supported purposes and algorithms](https://cloud.google.com/kms/docs/algorithms).
- **Key ring:** A grouping of keys for organizational purposes. A
  [key ring](https://cloud.google.com/kms/docs/resource-hierarchy#key_rings)
  belongs to a Google Cloud project and resides in a specific location. Keys
  inherit allow policies from their key ring. Grouping keys with related
  permissions in a key ring lets you grant, revoke, or modify permissions to
  those keys at the key-ring level without you needing to act on each key
  individually. Key rings provide convenience and categorization, but if the
  grouping of key rings isn't useful to you, you can manage permissions
  directly on keys.
  [Tags](https://cloud.google.com/kms/docs/creating-managing-labels#labels_and_tags)
  let you conditionally allow or deny policies based on whether a resource
  has a specific tag. You can apply tags at the key-ring level in the
  resource hierarchy.
  To prevent resource name collisions, you cannot delete a key ring or
  key. Key rings and keys don't have billable costs or quota limitations, so their continued existence doesn't affect costs or production limits.
- **Key metadata:** Resource names, properties of KMS resources such as
  allow policies, key type, key size, key state, and any data derived from
  keys and key rings.
- **Key version:** The key material associated with a key at some point in
  time. The
  [key version](https://cloud.google.com/kms/docs/resource-hierarchy#key_versions)
  is the resource that contains the actual key material. Versions are
  numbered sequentially, beginning with version 1. When a key is rotated, a
  new key version is created with new key material. The same logical key can
  have multiple versions over time, which means that your data is encrypted
  using different key versions. Symmetric keys have a *primary version*. By
  default, the primary version is used for encryption. When
  Cloud KMS performs decryption using symmetric keys, it
  automatically identifies which key version is needed to perform the decryption.

### Key hierarchy

The following diagram illustrates the key hierarchy and envelope encryption for
Cloud KMS and Google's internal Keystore. [Envelope
encryption](https://cloud.google.com/kms/docs/envelope-encryption) is the process of encrypting one key
using another key, in order to securely store it or transmit it over an
untrusted channel. All of the keys in this diagram are symmetric keys.

![Diagram of internal key hierarchy.](https://cloud.google.com/static/docs/security/key-management-deep-dive/images/kms-key-hierarchy-simple.svg)

Within the key hierarchy, a data encryption key (DEK) encrypts the data chunks.
A key encryption key (KEK) is used to encrypt, or *wrap*, the DEK. All
Cloud KMS platform options (software, hardware, and external backends)
let you control the KEK. KEKs are stored in Cloud KMS. Key material
never leaves the Cloud KMS system boundary.

For software-protected keys, a location-specific KMS master key encrypts the KEK.
The KMS master key is stored in Keystore. There is a separate KMS master key in
Keystore for each [Cloud KMS location](https://cloud.google.com/kms/docs/locations). Each
Cloud KMS server fetches a copy of the KMS master key during startup as
a hard dependency, and a new copy of the KMS master key is retrieved every day.
The KMS master key is re-encrypted periodically using the Keystore master key in
Keystore. The Keystore master key is protected by the root Keystore master key.

For hardware-protected keys, a location-specific HSM wrapping key encrypts the
KEK, and the HSM wrapping key is then encrypted with the KMS master key. For
more information, see [Creating
keys](https://cloud.google.com/docs/security/cloud-hsm-architecture#creating_keys). For external keys,
an EKM wrapping key encrypts the wrapped DEK, and the EKM wrapping key is then
encrypted with the KMS master key.

Cloud KMS uses Keystore, which is Google's
internal key management service, to wrap Cloud KMS-encrypted keys.
Cloud KMS uses the
same root of trust as Keystore. For more information about Keystore, see
[Key management](https://cloud.google.com/docs/security/encryption/default-encryption#key_management)
in the Encryption at rest paper.

### Operational constraints

Cloud KMS operates within the following constraints:

- **Project:** Cloud KMS resources belong to a [Google Cloud
  project](https://cloud.google.com/docs/overview#projects), just like all other Google Cloud
  resources. Your Cloud KMS keys can reside in a different project
  than the data that the keys protect. If you keep the keys in the same
  project as the data that the resources protect, then, to support the best
  practice of [separation of duties](https://cloud.google.com/kms/docs/separation-of-duties) between
  the key administrators and data administrators, you can remove the owner
  role from the project.
- **Locations:** Within a project, Cloud KMS resources are
  created in a
  [location](https://cloud.google.com/kms/docs/locations).
  For more information about locations, see
  [Geography and regions](https://cloud.google.com/docs/geography-and-regions).
- **Consistency**: Cloud KMS propagates operations on keys, key
  rings, and key versions using strong consistency or eventual consistency.
  For more information, see
  [Cloud KMS resource consistency](https://cloud.google.com/kms/docs/consistency).

## Customer-managed encryption keys

By default, Google Cloud encrypts all customer data stored at rest, with
Google managing the keys used for encryption. For [compatible Google Cloud
products](https://cloud.google.com/kms/docs/compatible-services) that persistently store your customer
content (for example, Cloud Storage), you can instead use Cloud KMS
to manage customer-managed encryption keys (CMEKs). CMEKs are encryption keys
that you own and can be used with external keys, software-protected keys, and
hardware-protected keys.

CMEKs let you have greater control over the keys that are used to encrypt data
at rest within compatible Google Cloud services, and provide a
cryptographic boundary around your data. You can manage CMEKs directly in
Cloud KMS, or automate provisioning and assignment by using
Autokey. When a service uses CMEK, your workloads can access resources
in the same way as when you are only using default encryption.

Cloud KMS lets you control many aspects of keys (such as creating,
enabling, disabling, rotating, and destroying keys) and manage appropriate IAM
permissions on them. To enforce a recommended separation of duties,
Cloud KMS includes
[several predefined IAM roles](https://cloud.google.com/kms/docs/reference/permissions-and-roles#predefined_roles)
that have specific privileges and limitations and can be granted to specific
users and service accounts.

Because Cloud KMS uses envelope encryption, a CMEK is a KEK that
encrypts the DEKs. For more information, see [Key hierarchy](#key-hierarchy).

CMEK rotation works differently depending on the resource type that the key
protects. Consider the following examples:

- In [Spanner](https://cloud.google.com/spanner/docs/cmek), a new key version reencrypts the
  DEK.
- For other resource types, such as [Cloud Storage
  buckets](https://cloud.google.com/storage/docs/encryption/customer-managed-keys#key-rotation), only
  newly created resources are encrypted using the new key version, which means
  that different versions of a key protect different subsets of data.
- In some scenarios, the cloud resource must be recreated with the new key
  version. For example, by default, [BigQuery doesn't automatically
  rotate a table encryption
  key](https://cloud.google.com/bigquery/docs/customer-managed-encryption#key_rotation) when the
  Cloud KMS key associated with the table rotates. Existing
  BigQuery tables continue to use the key version with which they were
  created.

For more information about key rotation, see the documentation for each
product.

[CMEK organization policies](https://cloud.google.com/kms/docs/cmek-org-policy)
provide greater control over how CMEK is used within your projects.  These
policies let you control the services and projects that hold keys allowed
for CMEK, and the protection level for the keys.

Google Cloud supports CMEK for many services, including Cloud Storage,
BigQuery, and Compute Engine. See
[CMEK integrations](https://cloud.google.com/kms/docs/use-keys-google-cloud#cmek_integrations)
for the full list of CMEK integrations and CMEK-compliant services. Google
continues to invest in CMEK integration for other Google Cloud products.

## Cloud KMS Autokey

Autokey lets you streamline the CMEK provisioning process. During a
manual CMEK provisioning process, a Cloud KMS administrator must plan
for the types of key rings, keys, and service accounts before they are required
and coordinate with developers to provision keys. With Autokey, the
Cloud KMS administrator delegates their authority to the
Cloud KMS service agent in the project. When you enable
Autokey, a developer can request a key from Cloud KMS, and the
service agent provisions the right key for the developer’s intent. With
Autokey, keys are available on demand, are consistent, and follow
industry-standard practices.

Autokey provisions and assigns key rings, keys, and service accounts on
demand as developers create that cloud resources, while respecting separation of
duties. Key provisioning and assignment follows industry-standard practices and
recommendations for data security, including the following:

- **HSM protection level:** The keys created using Autokey are always
  HSM keys and are therefore stored in the Cloud HSM backend. They are
  AES-256 GCM encryption keys.
- **Duty separation:** To maintain separation of duties, identities that can use
  the key to encrypt and decrypt are different from the identities that manage
  the key (including its rotation, destruction, or state change).
- **Key rotation:** Keys are rotated yearly.
- **Key co-location with resources:** The key resides in the same
  location as the resource that the key protects.
- **Key specificity:** The specificity of the key is appropriate for the
  resource type that the key protects, on a per-resource-type basis. Specificity
  means that you don’t have to manually review each service’s resource types and
  decide on how many of each resource type a single key should protect.

Keys requested using Autokey work identically to other
Cloud HSM keys with the same settings. Autokey simplifies
Terraform usage because it removes the need to run infrastructure-as-code with
elevated key-creation privileges. Autokey is available in all
Google Cloud locations where Cloud HSM is available.

Autokey is available for specific Google Cloud resources only. For more
information, see [Autokey overview](https://cloud.google.com/kms/docs/autokey-overview).

## Cloud KMS platform architecture and components

The Cloud KMS platform supports multiple cryptographic algorithms and
provides methods to encrypt and digitally sign using external keys,
hardware-protected keys, and software-protected keys. The Cloud KMS
platform is integrated with [Identity and Access Management (IAM)](https://cloud.google.com/iam)
and [Cloud Audit Logs](https://cloud.google.com/logging/docs/audit) so that you can manage
permissions on individual keys and audit how they are used.

![Cloud KMS architecture diagram.](https://cloud.google.com/static/docs/security/key-management-deep-dive/images/cloud-kms-platform.svg)

The preceding diagram shows the following main components of the
Cloud KMS platform:

- Administrators access key management services by using the Cloud console or the Google Cloud CLI.
- Applications access key management services by implementing the
  [REST API](https://cloud.google.com/kms/docs/reference/rest),
  [gRPC](https://www.grpc.io/),
  or
  [client libraries](https://cloud.google.com/kms/docs/reference/libraries).
  Applications can use Google services that are enabled to use CMEK. CMEK in
  turn uses the Cloud Key Management Service API. If your application uses PKCS #11, you can
  integrate it with Cloud KMS using the
  [library for PKCS #11](https://cloud.google.com/kms/docs/reference/pkcs11-library).
- The Cloud KMS API lets you use software, hardware, or external keys.
   You can generate and manage software-protected and hardware-protected keys
   using the Cloud KMS service endpoint. Both software-protected and
   hardware-protected keys use Google's redundant backup protections.
- If you use hardware-protected keys, FIPS 140-2 Level 3 certified HSMs in
  Google Cloud store the keys. For more information about our
  certification, see
  [Certificate #4399](https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/4399).
- Cloud KMS uses Google's internal datastore to store encrypted
  customer key material. This datastore is highly available and supports many
  of Google's critical systems. See [Datastore
  protection](#datastore-protection).
- At regular intervals, the independent backup system backs up the entire
  datastore to both online and archival storage. This backup allows
  Cloud KMS to achieve its durability goals. See
  [Datastore protection](#datastore-protection).

### FIPS 140-2 validation

Cloud KMS cryptographic operations are performed by our FIPS
140-2-validated modules. Keys with the `SOFTWARE` protection level, and the
cryptographic operations performed with them, comply with FIPS 140-2 Level 1.
These cryptography operations use
[BoringCrypto](https://boringssl.googlesource.com/boringssl/+/refs/heads/main/crypto/fipsmodule/FIPS.md),
which is a Google-maintained, open-source cryptographic library. Keys with the
`HSM` protection level, and the cryptographic operations performed with them,
comply with FIPS 140-2 Level 3.

### Security of key materials

In Cloud KMS, the key material is always encrypted at rest and in
transit. Key material is decrypted only in the following cases:

- When the customer is using it.
- When Google's internal key that is used to protect customer key material is
  being rotated or checked for integrity.

Customer requests to Cloud KMS are encrypted in transit by using TLS
between the customer and the [Google Front End
(GFE)](https://cloud.google.com/security/infrastructure/design#google_front_end_service).

Authentication occurs between all Cloud KMS jobs, both within and
between Google data centers.

Google's policy is to ensure that jobs use only source code that has been built,
tested, and reviewed in a verifiable manner.
[Binary Authorization for Borg (BAB)](https://cloud.google.com/docs/security/binary-authorization-for-borg)
enforces this policy at the operational level.

Cloud KMS API jobs can access key metadata (for example, the allow policy or
the rotation period). A Google employee with a valid, documented business
justification (such as a bug or a customer issue) can also access key metadata.
These access events are logged internally, and logs pertaining to data that is
covered by [Access Transparency](https://cloud.google.com/assured-workloads/access-transparency/docs/overview)
are also available to qualified customers.

Decrypted key material cannot be exported or viewed through the API interface or
another user interface. No Google employee has access to unencrypted customer
key material. Additionally, key material is encrypted with a master key in
Keystore, which cannot be directly accessed by any individual. On an HSM, key
material is never accessed in a decrypted state by Cloud KMS API jobs.

### Datastore protection

The datastore for Cloud KMS is highly available, durable, and
protected.

**Availability.** Cloud KMS uses Google's internal datastore, which is
highly available and supports a number of Google's critical systems.

**Durability.** Cloud KMS uses authenticated encryption to store
customer key material in the datastore. Additionally, all metadata is
authenticated using a hash-based message authentication code (HMAC) to ensure it
hasn't been altered or corrupted at rest. Every hour, a batch job scans all key
material and metadata and verifies that the HMACs are valid and that the key
material can decrypt successfully. If any data is corrupted, Cloud KMS
engineers are immediately alerted so that they can take action.

Cloud KMS uses several types of backups for the datastore:

- By default, the datastore keeps a change history of every row for four
  days. In an emergency, this lifetime can be extended to provide more time
  to remediate issues.
- Every hour, the datastore records a snapshot. The snapshot can be
  validated and used for restoration, if needed. These snapshots are kept for
  four days.
- Every day, a full backup is copied to disk and to archival storage.

The Cloud KMS team has documented procedures for restoring backups to
mitigate data loss when a service-side emergency occurs.

**Backups.** Cloud KMS datastore backups are located in their
associated Google Cloud region. These backups are all encrypted at rest.
Access to data in backups is gated based on access justifications (such as a
ticket number that you filed with Google support), and human access is logged in
[Access Transparency logs](https://cloud.google.com/assured-workloads/access-transparency/docs/reading-logs).

**Protection.** At the Cloud KMS application layer, your key material
is encrypted before it is stored. Engineers with access to the datastore don't
have access to plaintext customer key material. Additionally, the datastore
encrypts all data that it manages before writing to permanent storage. Therefore
access to underlying storage layers, including disks or archival storage,
doesn't allow access to even the encrypted Cloud KMS data without
access to the datastore encryption keys, which are stored in Keystore.

**Rotation policy.** Key rotation is part of the generally accepted best practices for the handling
of key material. A rotation policy exists for the keys used to protect
Cloud KMS datastores. A key rotation policy is also applied to the
Keystore master keys that wrap the Cloud KMS master keys. The Keystore
master key has a scheduled ciphertext maximum age of 90 days with a client
cached key maximum age of one day. Cloud KMS refreshes the KMS master
keys in KMS tasks every 24 hours and re-encrypts all customer keys on a monthly
basis.

**Data residency.** The data underlying each Cloud KMS datastore remains exclusively
within the Google Cloud region with which the data is associated. This
applies to locations that are multi-regions as well, for example, the `us`
multi-region.

### Key availability after creation

Cloud KMS allows a key to be used immediately after the
Cloud KMS datastore commits the transaction that creates the key and
after the storage layer acknowledges its creation.

## Key backends and protection levels

When you create a key with Cloud KMS, you can choose a
[protection level](https://cloud.google.com/kms/docs/algorithms#protection_levels)
to determine which key backend creates the key and performs all future
cryptographic operations on that key. The backends are exposed in the
Cloud KMS API as the following protection levels:

- `SOFTWARE`: Applies to keys that may be unwrapped by a software
  security module to perform cryptographic operations.
- `HSM`: Applies to keys that can only be unwrapped by HSMs that perform
  all cryptographic operations with the keys.
- `EXTERNAL` or `EXTERNAL-VPC`: Apply to external key manager (EKM).
  `EXTERNAL-VPC` lets you connect the EKM to Google Cloud over a VPC
  network.

### Cloud KMS software backend: SOFTWARE protection level

The protection level `SOFTWARE` applies to keys whose cryptographic operations
are performed in software. This section describes the details of how this level
is implemented.

#### Algorithmic implementations

For software keys, Cloud KMS uses the BoringCrypto module within
Google's
[BoringSSL](https://opensource.google/projects/boringssl)
implementation for all related cryptographic work. The BoringCrypto module is
[FIPS 140-2 validated](https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/4407).
The Cloud KMS binary is built against
[FIPS 140-2](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.140-2.pdf)
Level 1–validated cryptographic primitives of this module. The most current
algorithms covered by this module are listed on
[Key purposes and algorithms](https://cloud.google.com/kms/docs/algorithms),
and include encrypt, decrypt, and sign operations with AES256-GCM symmetric and
RSA 2048, RSA 3072, RSA 4096, EC P256, and EC P384 asymmetric cryptographic
keys.

#### Random number generation and entropy

When generating encryption keys, Cloud KMS uses BoringSSL. FIPS 140-2
requires that its own PRNGs be used (also known as DRBGs). In BoringCrypto,
Cloud KMS exclusively uses CTR-DRBG with AES-256. This provides output
for `RAND_bytes`, the primary interface by which the rest of the system gets
random data. This PRNG is seeded from the Linux kernel's RNG, which itself is
seeded from multiple independent entropy sources. This seeding includes entropic
events from the data center environment, such as fine-grained measurements of
disk seeks and inter-packet arrival times, and
[Intel's RDRAND instruction](https://software.intel.com/en-us/articles/intel-digital-random-number-generator-drng-software-implementation-guide)
where available. For more information about the behavior of the random number
generator for BoringSSL (FIPS-compliant mode), see the
[RNG design](https://github.com/google/boringssl/blob/main/crypto/fipsmodule/FIPS.md#rng-design).

### Cloud HSM backend: HARDWARE protection level

Cloud HSM provides hardware-protected keys to Cloud KMS. It
lets you use cryptographic keys that are protected by fully
managed, FIPS 140-2 Level 3 certified HSMs in Google data centers.
Cloud HSM is highly available and provides elastic scale, just like
Cloud KMS. You can access the Cloud HSM backend
using the same API and client libraries as Cloud KMS. For more
information about the Cloud HSM backend, see
[Cloud HSM architecture](https://cloud.google.com/docs/security/cloud-hsm-architecture).

### Cloud EKM: EXTERNAL protection level

Cloud EKM lets you encrypt data using off-cloud encryption keys that
remain in your control.

Keys with the `EXTERNAL` and `EXTERNAL_VPC` protection levels are stored and
managed in an external key management system. For more information, see
[Reference architectures for Cloud EKM](https://cloud.google.com/kms/docs/ekm-architectures).

## Key creation process

The following diagram illustrates the key creation process for the different key
backends and protection levels.

![Diagram of key creation process.](https://cloud.google.com/static/docs/security/key-management-deep-dive/images/kms-key-creation.svg)

The key creation process includes the following:

1. Using the Cloud KMS API, a user asks Cloud KMS to create a key.
  This request includes the protection level (whether the key is
  software-protected, hardware-protected, or external).
2. Cloud KMS verifies the user identity and whether the user has the
  permission to create the key.
3. The key is generated as follows:
  - For software-protected keys, Cloud KMS generates the customer
    key.
  - For hardware-protected keys, Cloud KMS sends a request to
    Cloud HSM. Cloud HSM sends the request to the HSM to
    generate a new key. The HSM generates a customer key and encrypts (wraps)
    this key with the HSM regional wrapping key. Cloud HSM sends the
    wrapped key back to Cloud KMS.
  - For external keys, Cloud KMS sends a request to
    Cloud EKM. Cloud EKM sends the request to the external
    key manager to generate a new key. The EKM generates a new key and
    encrypts this key with the EKM wrapping key. Cloud EKM sends the
    wrapped key back to Cloud KMS.
4. Cloud KMS encrypts the wrapped customer key with the KMS master key
  and sends it to the KMS datastore for storage.
5. Cloud KMS sends a success response with the full URI for the key
  version to the user.

## Key import

You might want to import your own keys that you created on-premises or in an
EKM into your cloud environment. For example, you might have a regulatory
requirement that the keys used to encrypt your cloud data are generated in a
specific manner or environment. [Key import](https://cloud.google.com/kms/docs/key-import)
lets you import these keys and meet your regulatory obligations. To extend your
signing capabilities to the cloud, you can also import asymmetric keys.

As part of key import, Cloud KMS generates a public wrapping key which
is a public/private key pair, using one of the
[supported import methods](https://cloud.google.com/kms/docs/key-wrapping#import_methods).
Encrypting your key material with this wrapping key protects the key material in
transit.

You use the public wrapping key to encrypt the key to be imported on the client.
The private key that matches the public key is stored within Google Cloud
and is used to unwrap the public key after it reaches the
Google Cloud project. The import method that you choose determines the
algorithm that is used to create the wrapping key. After your key material is
wrapped, you can import it into a new key or key version on Cloud KMS.

You can use imported keys with the `HSM` or `SOFTWARE` protection level. For
Cloud HSM, the private key portion of the wrapping key is available
only within Cloud HSM. Restricting the private key portion to
Cloud HSM prevents Google from unwrapping your key material outside of
Cloud HSM.

## Lifecycle of a Cloud KMS request

This section describes the lifecycle of a Cloud KMS request, including
a discussion of the destruction of key material. The following diagram shows a
client requesting access to Cloud KMS service instances in `us-east1` and
`us-west1`, and how the requests are routed using the Google Front End (GFE).

![Diagram of KMS request lifecycle.](https://cloud.google.com/static/docs/security/key-management-deep-dive/images/kms-lifecycle.svg)

The steps in this lifecycle include the following:

1. Personnel in your organization or a job running on your organization's
  behalf composes a request to the Cloud KMS service,
  https://cloudkms.googleapis.com. DNS resolves this address to an anycast IP
  address of the GFE.
2. The GFE provides public IP hosting of its public DNS name, denial of
  service (DoS) protection, and TLS termination. When you send
  your request, it is generally routed to a GFE near you,
  regardless of the location that your request is targeted for. GFEs
  handle the TLS negotiation and, using the request URL and parameters,
  determine which Global Software Load Balancer (GSLB) routes the request.
3. There is a separate GSLB target for each Cloud KMS region. If
  the request arrives at a GFE in `us-east1`, and the request is destined
  for `us-west1`, the request is routed between the `us-east1` and `us-west1`
  data centers. All communication between data centers is encrypted in
  transit using ALTS, which mutually authenticates the GFE and
  Cloud KMS jobs.
4. When the request reaches the Cloud KMS job, it is first
  processed by a framework that handles much of the work common to all
  Google Cloud services. This framework authenticates the account and
  performs a number of checks to verify the following:
  - The account has a valid credential and can be authenticated.
  - The project has the Cloud KMS API enabled and
    has a valid billing account.
  - The quota is sufficient to run the request.
  - The account is on the allowlist to use the relevant
    Google Cloud region.
  - The request isn't rejected by VPC Service Controls.
5. After these checks pass, the framework forwards the request and credential
  to Cloud KMS. Cloud KMS parses the request to determine
  what resources are being accessed, and then checks with IAM
  to see whether the caller is authorized to make the request.
  IAM also indicates whether the request occurrence should be
  written to audit logs. If
  [Key Access Justifications](https://cloud.google.com/assured-workloads/key-access-justifications/docs/overview)
  is enabled, a justification notice is sent that you must approve.
6. After the request is authenticated and authorized, Cloud KMS
  calls its in-region datastore backends to fetch the requested resource.
  After the resource is fetched, your key material is decrypted for use.
7. With the key material, Cloud KMS then performs the
  cryptographic operation, forwarding the wrapped version of the key to
  the Cloud KMS software backend, Cloud HSM backend,
  or the Cloud EKM backend, depending on the protection level of the key.
8. After the cryptographic operation is completed, the response is sent
  back to you along the same type of GFE-to-KMS channel as the request.
9. As the response is returned, Cloud KMS also triggers the following
  events asynchronously:
  - Audit and request logs are filled and queued to be written.
  - Reports are sent for billing and quota management purposes.
  - If the request updated the metadata of a resource, the change is
    sent to
    [Cloud Asset Inventory](https://cloud.google.com/asset-inventory/docs/overview)
    through batch job updates.

## End-to-end data integrity

Cloud KMS lets you calculate checksums for keys and key materials to
help ensure that they aren't corrupted. These checksums help protect you from
data loss that might be caused by hardware corruption or software corruption.
Helper libraries let you verify key integrity. You can use helper libraries to
verify key integrity by providing checksums to Cloud KMS, which are
verified by the server. Also, these libraries let you receive checksums to
verify response data on the client.

End-to-end data integrity helps protect your environment from threats such as
the following:

- Corruption during transit; such as in the stack between when data is
  sent and when it gets protected by TLS.
- Issues in any intermediate proxies between your endpoint and KMS (for
  example, for incoming requests).
- Faulty crypto operations, machine memory corruption, or HSM corruption
  in the Cloud KMS architecture.
- Corruption during communication with an external EKM.

For more information, see
[Verifying end-to-end data integrity](https://cloud.google.com/kms/docs/data-integrity-guidelines).

## Destruction of key material

Key material is considered to be customer data, so the approach described in
[Data deletion on Google Cloud](https://cloud.google.com/docs/security/deletion)
also applies to Cloud KMS. Key material is destroyed on request, when
the *Scheduled for destruction* period is complete and backups expire. The key
material that is still present in backups (after the scheduled for destruction
period is over) can only be used for regional disaster recovery, and not for
restoring individual keys. This process isn't guaranteed for copies of imported
keys that exist outside of Cloud KMS control.

By default, keys in Cloud KMS spend 30 days in the *Scheduled for
destruction*
([soft deleted](https://cloud.google.com/security/deletion#stage_2_-_soft_deletion))
state before the key material is
[logically deleted](https://cloud.google.com/security/deletion#stage_3_-_logical_deletion_from_active_systems)
from the system. You can change this duration. For more information, see
[Variable duration of the Scheduled for destruction state](https://cloud.google.com/kms/docs/key-states#variable_duration_of_the_scheduled_for_destruction_state).

Although key material is destroyed, keys and key rings cannot be deleted. Key
versions also cannot be deleted, but key version material can be destroyed so
that the resources can no longer be used. Key rings and keys don't have billable
costs or quota limitations, so their continued existence doesn't affect costs or
production limits.

After a key version is scheduled for destruction, the key version isn't
available for cryptographic operations. Within the pending delete period, you
can restore the key version so that it isn't destroyed.

If you delete an imported key by mistake, you can re-import it. For more
information, see
[Re-importing a destroyed key](https://cloud.google.com/kms/docs/importing-a-key#re-importing_a_destroyed_key).

To avoid accidentally deleting a key, consider the following best practices:

- Set the **Minimum destroy scheduled duration per key** constraint to a
  longer duration. This
  [constraint](https://cloud.google.com/kms/docs/control-key-destruction#require-minimum) defines the
  minimum amount of time for the *scheduled for destruction* period for new
  keys.
- Enforce the **Restrict key destruction to disabled keys** constraint so that
  only disabled keys can be destroyed. For more information, see [Require keys
  to be disabled before
  destruction](https://cloud.google.com/kms/docs/control-key-destruction#require-disable).
- Create a custom KMS role that doesn't include the
  `cloudkms.cryptoKeyVersions.destroy` permission.
- Change the `destroy_scheduled_duration` field to a longer period of time.
- Monitor and add alerts for key destruction events. For example, create
  the following Cloud Logging filter:
  ```
  resource.type="cloudkms_cryptokeyversion"
    protoPayload.methodName="DestroyCryptoKeyVersion"
  ```
- Create processes that
  [disable the key](https://cloud.google.com/kms/docs/enable-disable#disable)
  for a couple days before the key is deleted.

## Google infrastructure dependencies

Cloud KMS platform elements run as production Borg jobs.
[Borg](https://research.google/pubs/pub43438)
is Google's large-scale cluster manager for handling API serving jobs and batch
jobs.

For information about the security of our physical and production
infrastructure, see the
[Google infrastructure security design overview](https://cloud.google.com/docs/security/infrastructure/design).

### Cloud KMS API serving jobs

Cloud KMS API serving jobs are production Borg jobs that serve customers'
requests to manage and use their keys. Cloud KMS API serving jobs also
process deferred actions from customer requests, like rotating keys on schedule,
creating asymmetric keys, and importing keys. These serving jobs run in every
Google Cloud region where
[Cloud KMS is available](https://cloud.google.com/kms/docs/locations).
Each job is associated with a single region and is configured to only access
data from systems geographically located within the associated
Google Cloud region.

### Cloud KMS batch jobs

The Cloud KMS platform also maintains a number of batch jobs that run
as production Borg jobs on various schedules. Batch jobs are region-specific and
only aggregate data from, and run within, the associated Google Cloud
region. Tasks that these jobs perform include the following:

- Count active keys for
  [customer billing](https://cloud.google.com/kms/pricing).
- Aggregate resources from the
  [public protocol buffer API](https://protobuf.dev/overview/) for Cloud KMS
  and forward the metadata to
  [Cloud Asset Inventory](https://cloud.google.com/asset-inventory/docs/overview).
  *Resources* in this context are any resources that Cloud KMS
  manages—for example, keys and key rings.
- Aggregate all resources and reporting information for business analytics.
- Snapshot data for high availability.
- Validate that all data stored in the underlying datastore is uncorrupted.
- Re-encrypt customer key material when the KMS master key is being rotated.

### Cloud KMS key snapshotter

To maintain high availability, the Cloud KMS platform maintains a
redundant datastore in each instance of the shared service that hosts the
Cloud KMS API server tasks. Each shared service deploys its own instance of
the snapshotter service. This redundancy makes services highly independent so
that a failure in one zone has a limited effect on other zones. When the
Cloud KMS API job needs to perform a cryptographic operation, it queries the
primary datastore along with the local snapshotter jobs in parallel. If the
primary datastore is slow or unavailable, the response may be served from a
snapshot, if the snapshot is no more than two hours old. Snapshots are
created as the output of a batch job that runs continuously for each region.
Snapshots reside in the cloud region associated with the key material.

### Client-server communications

Google uses
[Application Layer Transport Security (ALTS)](https://cloud.google.com/security/encryption-in-transit/application-layer-transport-security)
to help provide security for client-server communications that use Google's
remote procedure call (RPC) mechanism.

For more information, see
[Service-to-service authentication, integrity, and encryption](https://cloud.google.com/docs/security/encryption-in-transit#service_integrity_encryption).

## Cloud KMS platform operational environment

The operational environment for the Cloud KMS platform includes data
storage and security policies, access restrictions, and risk mitigation
strategies that are designed to optimize reliability, durability, and
availability while safeguarding key material. This section discusses the
service's operating structure, responsibilities for operations team members,
authentication mechanisms, and auditing and logging protocols. This section
applies to both the software-protected and hardware-protected key capabilities.

### Software engineers, site reliability engineers, and system operators

Software engineers are responsible for partnering with other stakeholders such
as product managers and site reliability engineers (SREs) to design the system
and write much of the code and tests for the Cloud KMS service. The
code includes the main job that serves customer requests, as well as secondary
jobs for activities such as data replication and billing. SREs also might write
code. However, software engineers and SRE duties are separated; SREs are
primarily responsible for maintaining the production environment for
Cloud KMS jobs. SREs measure and achieve reliability through
engineering and operations work.

System operators are responsible for the build-and-release process, monitoring,
alerting, and capacity planning for Cloud KMS. They are the first
responders to customer issues and outages for Cloud KMS. As an example,
system operators leverage tooling and automation to minimize manual systems work
so that they can focus on efforts that bring long-term value.

The duties for system operators are defined in standard operating procedures.
System operators don't access customer key material while performing their
duties.

### Regionality of Cloud KMS resources

To help you meet any key residency requirements, you can create
Cloud KMS resources in one of four types of
[Google Cloud locations](https://cloud.google.com/about/locations):

- A *region location* consists of
  [zones](https://cloud.google.com/docs/geography-and-regions)
  in a specific geographical place, such as Iowa.
- A *dual-region location* consists of
  zones in two specific geographical places, such as Iowa and South Carolina.
- A *multi-region location* consists of
  zones spread across a general geographical area, such as the United States.
- The *global location* consists of zones spread
  around the world. When you create your Cloud KMS resources in the
  global location, they are available from zones worldwide.

Locations represent the geographical regions where requests to
Cloud KMS for a given resource are handled, and where the corresponding
cryptographic keys are stored.

For more information on available Cloud KMS locations, see
[Cloud KMS locations](https://cloud.google.com/kms/docs/locations).

#### Cloud regions and data centers

A Google Cloud region contains a specific data center or a specified set
of data centers, determined by its designation as a single-region, dual-region,
multi-region, or global. For more information on Google Cloud regions, see
[Google Cloud locations](https://cloud.google.com/about/locations).

Each data center contains racks of machines for computing, networking, or
storage of data.These machines run Google's Borg infrastructure.

Google data centers have strict physical security
[requirements](https://www.google.com/about/datacenters/inside/data-security/).
Any physical space that might contain user data requires entryways with badge
readers and iris scanners that are used to authenticate entrants. Doors aren't
held open for multiple people; each person must authenticate themselves
individually. Bags aren't permitted to be brought in or out of these areas,
unless they are clear bags that are explicitly authorized after inspection by
security personnel. Special permission is required to bring in or out any
electronic device that might transmit or record data.

#### Key residency

Some industries require that cryptographic keys reside in a specific location.
Cloud KMS has
[data location terms](https://cloud.google.com/terms/data-residency)
with assurances on data residency. As introduced in
[Regionality of Cloud KMS resources](#regionality-of-kms-resources),
Cloud KMS offers four types of regional locations to help you meet
those requirements.

For single, dual, or multi-region locations, Cloud KMS creates, stores,
and processes your software-protected and hardware-protected keys and key
material only in that location. The storage and data processing systems that
Cloud KMS uses are configured to only use resources within the
Google Cloud region that is associated with the key material. Key material
created in dual-region or multi-region locations doesn't leave the boundaries of
the selected locations.

For the global region, there are no regionality guarantees specified.

Cloud KMS doesn't guarantee residency for key metadata, usage logs, or
for key material in transit. Key metadata includes resource names; properties of
Cloud KMS resources such as key type, key size, and key state; IAM
policies; and any data derived from metadata.

When using CMEK, the following Cloud KMS geographic restrictions apply
to your keys regardless of the custom, dual-region, or multi-region locations that
you choose in other Google Cloud products that support
CMEK:

- **For a specific region:** Because the region of a customer-managed KMS
  key must always correlate to the region of the resource it protects in a
  given Google Cloud service, residency restrictions for single-region
  keys and resources are guaranteed to be compatible and enforced.
- **For dual-region or multi-region locations:** Users can select
  Google-defined multi-regions for their keys and Google Cloud
  resources to guarantee residency compliance. To ensure this geographic
  residency, make sure that your regions in other products line up with your
  chosen Cloud KMS regional location.

The following table summarizes residency of key material for
Cloud KMS.

| Region type | At rest, in use |
| --- | --- |
| Single region | Resident |
| Dual-region or multi-region | Resident in the regions that constitute the dual or
multi-region |

#### Regionality monitoring

Google's internal data monitoring services actively monitor key residency.
Cloud KMS sends alerts to SRE team members if it detects accidental
misconfigurations, or if key material leaves the boundaries of its configured
region, is stored in the wrong region, or is accessed from the wrong region.

#### High availability

Cloud KMS can help simplify your availability requirements based on
the regions that you select.  The more granular the location, the more
redundancy you have to build. For applications with higher levels of
availability, use multi-region locations rather than trying to build your own
replication system of keys. You must balance the built-in redundancy
capabilities with your data regionalization needs.

### Authentication and authorization

Cloud KMS accepts a variety of authentication mechanisms, such as
OAuth2, JWT, and ALTS. Whatever the mechanism, Cloud KMS resolves the
provided credential to identify the principal (the entity which is authenticated
and is authorizing the request), and calls IAM to see whether the principal is
authorized to make the request and whether an audit log is written.

Cloud KMS uses an internal version of the public
[Service Control API](https://cloud.google.com/service-infrastructure/docs/service-control/reference/rpc)
for many aspects of service management. Before a Cloud KMS job handles
a request, it first sends a check request to the Service Control API, which
enforces many controls common to all Google Cloud services, such as the
following:

- Checking whether you activated the Cloud KMS API and have an active
  billing account.
- Checking whether you haven't exceeded your quota, and reporting quota usage.
- Enforcing
  [VPC Service Controls](https://cloud.google.com/vpc-service-controls).
- Checking whether you are on the allowlist for applicable private cloud
  regions.

### Quota management

Cloud KMS has usage limits, called *quotas*, on requests made to the
service. Cloud KMS contains the following quotas:

- *Cryptographic requests* quotas for operations such as encrypt,
  decrypt, or sign.
- *Read requests* quotas for operations such as getting key metadata or
  getting an IAM policy.
- *Write requests* quotas for operations such as creating a key or setting
  an IAM policy.

These quotas are charged to the project that is associated with the caller.
These quotas are also global, which means that they are applied for the caller's
KMS usage across all regions and multi-regions.  These quotas are evaluated for
all protection levels.

Cloud HSM and Cloud EKM have additional quotas for
cryptographic operations.  These quotas must be satisfied *in addition to* the
cryptographic requests quota.  Cloud HSM and Cloud EKM quotas
are charged to the project where the key resides, and the quotas are enforced
for each location.

Consider the following examples:

- Calling decrypt with a software key in `asia-northeast1` requires one
  unit of (global) *cryptographic requests* quota.
- Creating an HSM key in `us-central1` requires one unit of *write requests*
  quota and no HSM quota.
- Calling encrypt with an EKM key in `europe` requires one unit of
  (global) *cryptographic requests* quota, and one unit of *external KMS
  requests* quota in `europe`.

For more information about the type of quotas available, see
[Quotas on the usage of Cloud KMS resources](https://cloud.google.com/kms/quotas#usage-quotas).
 You can view your quota limit in the Cloud console.  The initial
quotas limits are soft limits that you can request be
[adjusted](https://cloud.google.com/kms/docs/monitor-adjust-quotas#increase_quotas)
based on your workload needs.

### Logging

Three types of logs are associated with Cloud KMS:
Cloud Audit Logs, Access Transparency logs, and internal request logs.

#### Cloud Audit Logs

Cloud KMS
[records](https://cloud.google.com/kms/docs/audit-logging) your activity in
[Cloud Audit Logs](https://cloud.google.com/logging/docs/audit). You can view these logs in the
Cloud console. All admin activity—for example, creating or destroying a key—is
recorded in these logs. You can also choose to enable logging for all other
actions that use a key—for example, using a key to encrypt or decrypt data. You
control how long you wish to retain the logs and who may view the logs.

#### Access Transparency logs

Eligible customers might choose to enable
[Access Transparency](https://cloud.google.com/assured-workloads/access-transparency/docs/overview)
logs, which provide them with logs of actions that Google employees take in your
Google Cloud organization. Access Transparency logs, alongside the logs
from Cloud Audit Logs, can help you answer questions about who did what,
where, and when.

You can integrate Access Transparency logs with your existing security
information and event management (SIEM) tools to automate your audits of these
actions. These logs are available in the Cloud console alongside your
Cloud Audit Logs.

Access Transparency log entries include the following types of details:

- The affected resource and action.
- The time of the action.
- The
  [reasons](https://cloud.google.com/logging/docs/audit/reading-access-transparency-logs#justification-reason-codes)
  for the action. Examples of reasons include customer-initiated support
  (with a case number), Google-initiated support, third-party data requests,
  and Google-initiated review requests.
- Data about who is acting on the data (for example, the Google staff
  member's location).

#### Internal request logs

Request logs store a record for every request sent to the Cloud KMS
platform. This record contains details about the type of request (such as API
method or protocol), and the resource being accessed (such as resource name, key
algorithm, or key protection level). These logs don't store customer plaintext,
ciphertext, or key material. Before new types of data are added to these logs, a
team that specializes in privacy reviews must approve changes to the data that
is logged.

Log entries are permanently deleted when the configured time to live (TTL) has
expired.

Cloud KMS SREs and engineers in the on-call rotation can access request
logs. Human access to logs and any access that returns customer data requires a
valid and documented business justification. With some specific
[exceptions](https://cloud.google.com/cloud-provider-access-management/access-transparency/docs/overview),
human access is logged and accessible to qualifying customers in
Access Transparency logs.

### Monitoring

Cloud KMS integrates with Cloud Monitoring. This integration lets
you monitor, build dashboards, and create alerts on many Cloud KMS
operations. For example, you can monitor when keys are scheduled for destruction
or
[monitor and adjust Cloud KMS quotas](https://cloud.google.com/kms/docs/monitor-adjust-quotas)
when cryptographic operations are past a threshold you define. For more
information about the available Cloud KMS metrics, see
[Using Cloud Monitoring with Cloud KMS](https://cloud.google.com/kms/docs/monitoring).

In addition, Security Command Center has built-in KMS vulnerability detectors. These
detectors help ensure that your projects which include keys follow our
recommended best practices. For more information about the KMS vulnerability
detector, see
[Vulnerability findings for Cloud KMS](https://cloud.google.com/security-command-center/docs/concepts-vulnerabilities-findings#kms-findings).

## What's next

- To learn more about Cloud KMS, explore the following resources:
  - [Cloud KMS documentation](https://cloud.google.com/kms/docs)
  - [Cloud HSM documentation](https://cloud.google.com/kms/docs/hsm)
- For information about using your own encryption keys in
  Google Cloud, see
  [Customer-managed encryption keys (CMEK)](https://cloud.google.com/kms/docs/cmek).
- To learn more about Google infrastructure security, see
  [Google infrastructure security design overview](https://cloud.google.com/docs/security/infrastructure/design).
