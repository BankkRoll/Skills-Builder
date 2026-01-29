# Revoke access to a Google Cloud projectStay organized with collectionsSave and categorize content based on your preferences. and more

# Revoke access to a Google Cloud projectStay organized with collectionsSave and categorize content based on your preferences.

> Discover best practices and tasks that let you revoke user access on Google Cloud in a seamless manner

# Revoke access to a Google Cloud projectStay organized with collectionsSave and categorize content based on your preferences.

This document describes best practices, scenarios, and procedures for revoking a
user's access to a Google Cloud project. Because each business has different
policies and workloads, we recommend that you use this document to come up with
your own policies and procedures that let you revoke access consistently and in a
timely manner.

When an employee leaves your company, your engagement with a contractor ends, or
a collaborator moves on to other projects, there are a few things you should do
to revoke unneeded access to your cloud resources.

Some of these processes are optional. You should determine which of these steps
to execute depending on your security needs, products in use, and trust in the
person whose access is being revoked.

## Best practices for setting up your project

You can improve your project's ability to efficiently revoke user
access by making thoughtful choices at setup time.

### Federate user accounts with your existing identity provider

When you federate user accounts with your existing identity provider, make sure
that you propagate user suspension and deletion events. With propagation, when
you suspend or remove a user account from your identity provider, the user also
loses access to Google Cloud resources.

For more information, see [Best practices for federating Google Cloud with
an external identity
provider](https://cloud.google.com/architecture/identity/best-practices-for-federating).

For more identity-related best practices, see [Best practices for planning
accounts and
organizations](https://cloud.google.com/architecture/identity/best-practices-for-planning).

For information about Workforce Identity Federation, see
[Workforce Identity Federation](https://cloud.google.com/iam/docs/workforce-identity-federation).

### Consider using Google Groups to manage access to project resources

Google Groups let you organize users based on their team membership, access
requirements, or other criteria. After you create Google Groups, you can
assign access to Google Cloud projects and resources based on group membership. When
a user moves to another team or job function, you can move the user account to
another group, which automatically removes the access that was granted by allow
policies to the previous group.

Using Google Groups isn't appropriate in all circumstances. For example, you
shouldn't use groups that are based only on your business' organization
structure to manage access. For best practices on group usage, see [Best
practices for using Google Groups](https://cloud.google.com/iam/docs/groups-best-practices).

For more information, see
[Managing groups in the Google Cloud console](https://cloud.google.com/iam/docs/groups-in-cloud-console)
and
[Create a group in your organization](https://support.google.com/cloudidentity/answer/9400082)

### Use OS Login

Use OS Login instead of metadata-based SSH keys so that the user's authorized
keys are linked to their Google identity. When you remove a user account, the
authorized keys and access to VMs are revoked automatically. For more
information, see [Use OS Login to ensure continuous access evaluation against
IAM
policies](https://cloud.google.com/compute/docs/connect/ssh-best-practices/login-access#use-oslogin).

For instructions, see [Set up OS Login](https://cloud.google.com/compute/docs/oslogin/set-up-oslogin).

### Restrict access from external user accounts

Don't grant external users access to the project because you can't control the
lifecycle for these user accounts. To restrict external users, use the
[iam.allowedPolicyMemberDomains](https://cloud.google.com/resource-manager/docs/organization-policy/restricting-domains)
list constraint.

For instructions, see [Restricting identities by domain](https://cloud.google.com/resource-manager/docs/organization-policy/restricting-domains).

### Use authentication proxies with databases

Authentication proxies let you connect the lifecycle of database credentials to
the lifecycle of a Google identity. When you suspend or delete a user account in
Cloud Identity or Google Workspace, access to databases is automatically
revoked.

For more information, see [Cloud SQL Auth proxy](https://cloud.google.com/sql/docs/mysql/sql-proxy)
and [AlloyDB for PostgreSQL Auth proxy](https://cloud.google.com/alloydb/docs/auth-proxy/overview).

### Prepare for credential rotation

Design your projects and resources to allow for non-disruptive rotation of
project-level credentials. These are secrets tied to the project itself, such as
service account keys, OAuth client secrets, and application-specific secrets
like database root passwords. For more information, see [Handle compromised
Google Cloud credentials](https://cloud.google.com/docs/security/compromised-credentials).

### Restrict API keys

When creating and managing API keys, restrict the set of web sites, IP
addresses, and apps that can use them. A user account with roles like Viewer or
[API Keys Admin](https://cloud.google.com/iam/docs/understanding-roles#serviceusage.apiKeysAdmin) can
see your project's API keys, so any unrestricted keys must be rotated or deleted
in order to revoke billing access. For more information, see [Secure an API
key](https://cloud.google.com/docs/authentication/api-keys).

### Monitor access permissions

Carefully tracking access helps mitigate against potential access abuse. You can
use [IAM role
recommender](https://cloud.google.com/policy-intelligence/docs/role-recommendations-overview)
to track role usage to help enforce the least privilege principle. In addition,
Security Command Center's [Cloud Infrastructure Entitlement Management
(CIEM)](https://cloud.google.com/security-command-center/docs/ciem-overview) capabilities let you manage
which identities have access to which resources in your deployments and mitigate
potential vulnerabilities that result from misconfigurations.

### Use uniform bucket-level access for Cloud Storage

[Uniform bucket-level access](https://cloud.google.com/storage/docs/uniform-bucket-level-access) lets
you use IAM alone to manage permissions for your
Cloud Storage buckets. Use uniform bucket-level access along with
[other access control
options](https://cloud.google.com/storage/docs/access-control#additional_access_control_options)
to refine who can access the content in your buckets.

### Additional best practices

In addition to the best practices described in this document, review the
following best practices:

- [Best practices for working with service
  accounts](https://cloud.google.com/iam/docs/best-practices-service-accounts)
- [Decide the security for your Google Cloud landing
  zone](https://cloud.google.com/architecture/landing-zones/decide-security)
- [Verify every access attempt explicitly](https://cloud.google.com/architecture/framework/security/implement-zero-trust#verify_every_access_attempt_explicitly)

## Scenarios for revoking access to Google Cloud projects

If you implemented the best practices listed in
[Best practices for setting up your project](#bps-setting-up),
the following table summarizes how you can revoke access.

| Scenario | Revoking access options |
| --- | --- |
| An employee leaves your company. | If you set up federation
between Cloud Identity or Google Workspace with automatic user provisioning,
access revocation can happen automatically.If you didn't follow best
practices and you granted external user identities access to your resources,
then you must manually remove the identities from your projects and
resources. |
| An employee changes their job function. | You remove the employee from the team group. |
| A contract engagement ends. | If you set up federation
between Cloud Identity or Google Workspace with automatic user provisioning,
access revocation can happen automatically.If you didn't follow best
practices and you granted external user identities access to your resources,
then you must manually remove the identities from your projects and resources. |
| An account was compromised. | For instructions, seeHandle compromised
Google Cloud credentials. |

## Revoke access

If you've made good choices in project setup, the following processes will be an
efficient way to revoke a person's access.

To determine what resources a person has access to, use
Policy Analyzer. For instructions, see [Analyze IAM
policies](https://cloud.google.com/policy-intelligence/docs/analyze-iam-policies).

### Delete the user account from your identity provider

If the user is leaving your organization, and you've federated
Cloud Identity or Google Workspace with your identity provider,
with automatic user provisioning, access revocation can happen automatically.

For information about deleting Workforce Identity Federation users, see
[Delete Workforce Identity Federation users and their
data](https://cloud.google.com/iam/docs/workforce-delete-user-data).

### Move the account to another group

If the user is changing roles, remove the user account from their current
Google Groups. If you've federated
Cloud Identity or Google Workspace with your identity provider
to manage group membership, access revocation can happen automatically.

For more information, see [Viewing and editing group details](https://cloud.google.com/iam/docs/groups-in-cloud-console#viewing-editing-details).

### Remove the user account from IAM allow policies

To remove a user account from project-level allow policies, do the following:

1. In the Google Cloud console, go to the **IAM permissions** page.
  [IAM permissions](https://console.cloud.google.com/iam-admin)
2. Select the project that you want to remove a user account from.
3. Click the checkbox next to the row that contains the user account you want
  removed from the member list, then click **Remove**.

To verify other locations where the allow policy can be set, including folders,
organization, or individual resources, see [Verify permissions were
removed](#verify-perms).

### Rotate project credentials

#### Rotate service account keys

If you use service account keys to authenticate to a service
account, you must rotate the keys. In addition, consider if the person might
have had access to service account keys somewhere outside of Google Cloud
tools, such as your source code repository or application configurations.

1. In the Google Cloud console, go to the **API credentials** page.
  [API credentials](https://console.cloud.google.com/apis/credentials)
2. Click the name of the service account that you want to modify.
3. Under the **Key** tab, click **Add Key**.
4. Click **Create new key**.
5. Choose the **Key type** you want to create. In most situations, **JSON** is
  recommended, but **P12** is available for backwards compatibility with
  code that depends on it.
6. Click **Create**. A file containing the new key will be automatically
  downloaded through your browser. Deploy this key to any applications that
  need it.
7. After confirming the new key works as expected, return to the credentials
  page and delete the old key associated with that service account.

#### Rotate OAuth client ID secrets

OAuth client ID secrets don't provide any direct access to your project.
However, if an attacker knows the OAuth client ID secret, they can spoof your
application and request access to your users' Google Accounts from a malicious
application.

You might need to rotate OAuth client ID secrets if the person whose access is
being revoked ever had access to the secret, including in your source code
repository, application configurations, or through IAM roles.

1. In the Google Cloud console, go to the **API credentials** page.
  [API credentials](https://console.cloud.google.com/apis/credentials)
2. Click the name of the OAuth 2.0 client ID that you want to modify.
3. On the **Client ID** page, click **Reset secret**.
4. Click **Reset** in the confirmation dialog to immediately revoke the old
  secret and set a new one. Note that any active users will need to
  reauthenticate upon their next request.
5. Deploy the new secret to any applications that need it.

#### Rotate API keys

API keys don't provide access to your project or your users' data, but they
control who Google bills for API requests. A user account with roles like Viewer
or [API Keys Admin](https://cloud.google.com/iam/docs/understanding-roles#serviceusage.apiKeysAdmin) can
see your project's API keys. If you have any unrestricted keys, you need to
delete or regenerate them when revoking someone's access to your project.

1. In the Google Cloud console, go to the **API credentials** page.
  [API credentials](https://console.cloud.google.com/apis/credentials)
2. Click the name of the API key that you want to modify.
3. Click **Regenerate key**.
4. A dialog will display the newly created key. Deploy this key to any
  applications using the key that you want to replace.
5. After confirming that your applications are working as expected with the new
  key, return to the credentials page and delete the old unrestricted key.

### Revoke access to VMs

If the person whose access you are revoking doesn't have login access to any of
your project VMs, you can skip this step.

1. Remove all [project-level SSH keys](https://cloud.google.com/compute/docs/connect/restrict-ssh-keys#remove-project-key)
  that the person had access to.
2. On each VM where the person had SSH access, [remove any instance-level keys](https://cloud.google.com/compute/docs/connect/restrict-ssh-keys#remove-instance-key).
3. Remove the person's account from any VMs they had login access to.
4. Check for suspicious applications the person might have installed to provide
  backdoor access to the VM. If you are uncertain about the security of any
  code running on the VM, recreate it and redeploy the applications you need
  from source.
5. Verify that the VM firewall settings haven't been changed from your planned
  or expected configuration.
6. If you create new VMs from custom base images, verify that the base images
  haven't been modified in a way that would compromise the security of new
  VMs.

### Revoke access to databases

If your project doesn't use Cloud SQL or AlloyDB for PostgreSQL
resources, you can skip this step.

To revoke access to a Cloud SQL database, complete the following:

1. In the Google Cloud console, go to the **SQL instances** page.
  [SQL instances](https://console.cloud.google.com/sql/instances)
2. Click the instance ID of the database you want to revoke access to.
3. In the left menu, click **Connections**.
4. Confirm that the list of IP addresses
  under **Authorized networks** and list of apps under **App Engine
  authorization** match what you expect. If the person whose access you're
  trying to revoke has access to networks or applications listed here, they
  can access this database.
5. In the left menu, click **Users**.
6. Delete or change the password for any user
  accounts that the person had access to. Be sure to update any applications that
  depend on those user accounts.

To revoke access to an AlloyDB for PostgreSQL database, see [Remove an
IAM user or service account from a
cluster](https://cloud.google.com/alloydb/docs/manage-iam-authn#delete-user).

### Redeploy App Engine

By default, App Engine apps have access to a service account that is an
editor on the associated project. App Engine request handlers can do things
like create new VMs and read or modify data in Cloud Storage. Someone with
the ability to deploy code to App Engine could use this service account to
open a backdoor into your project. If you're concerned about the code integrity
of your deployed apps, you might want to redeploy them (including any modules)
with a known-good image from your version control system.

### Verify permissions were removed

You can verify permissions at the organization level, the project level, or
using Policy Analyzer.

To find resources that a particular user might have access to at the
organization level, use the
[search-all-iam-policiesmethod](https://cloud.google.com/sdk/gcloud/reference/asset/search-all-iam-policies)
in Google Cloud CLI. For example, to determine whether a user has access to your
resources, run:

```
gcloud asset search-all-iam-policies --scope='organizations/ORGANIZATION_ID --query='policy:IDENTITY'
```

Where:

- `ORGANIZATION_ID` is your organization number.
- `IDENTITY` is the user's identity, such as an email
  address.

To verify permissions on a project, see [Permissions a principal has on a
project](https://cloud.google.com/asset-inventory/docs/search-allow-policies#permissions_a_principal_has_on_a_project).

To verify permissions using Policy Analyzer, see [Determine which
resources a principal can
access](https://cloud.google.com/policy-intelligence/docs/analyze-iam-policies#resource-query).

## What's next

- See [Handle compromised Google Cloud
  credentials](https://cloud.google.com/docs/security/compromised-credentials).
- Learn more
  [Best practices for mitigating compromised OAuth tokens for Google Cloud CLI](https://cloud.google.com/architecture/bps-for-mitigating-gcloud-oauth-tokens).
- Create a [deny policy](https://cloud.google.com/iam/docs/deny-overview) to
  specify which permissions the user can't access any longer.

   Was this helpful?

---

# Data deletion on Google CloudStay organized with collectionsSave and categorize content based on your preferences.

# Data deletion on Google CloudStay organized with collectionsSave and categorize content based on your preferences.

*This content was last updated in May 2024, and represents the status quo as of
the time it was written. Google's security policies and systems may change going
forward, as we continually improve protection for our customers.*

This document gives an overview of the secured process that occurs when you
delete your customer data on Google Cloud. As defined in the
[Google Cloud Terms of Service](https://cloud.google.com/terms),
*customer data* is data that is provided to Google by customers or end users
through the services under the account.

This document describes how customer data is stored in Google Cloud, the
deletion pipeline, and how we prevent any reconstruction of data that is stored
in our platform.

For information about our data deletion commitments, see
[Cloud Data Processing Addendum (Customers)](https://cloud.google.com/terms/data-processing-addendum).

## Data storage and replication

Google Cloud offers [storage services](https://cloud.google.com/products#section-21) and
[databases services](https://cloud.google.com/products#section-8) such as [Bigtable](https://cloud.google.com/bigtable)
and [Spanner](https://cloud.google.com/spanner). Most Google Cloud applications and
services access Google's storage infrastructure indirectly using these cloud
services.

Data replication is critical to achieving low latency, highly available,
scalable, and durable solutions. Redundant copies of customer data can be stored
locally and regionally and even globally, depending on your configuration and
the demands of your projects. Actions taken on data in Google Cloud may be
simultaneously replicated in multiple data centers, so that customer data is
highly available. When performance-impacting changes occur in the hardware,
software, or network environment, customer data is automatically shifted from
one system or facility to another, subject to customers' configuration settings,
so that customer projects continue performing at scale and without interruption.

At the physical storage level, customer data is stored at rest in two types of
systems: active storage systems and backup storage systems. These two types of
systems process data differently. Active storage systems are
Google Cloud's production servers that run Google's application and
storage layers. Active systems are mass arrays of disks and drives used to write
new data as well as store and retrieve data in multiple replicated copies.
Active storage systems are optimized to perform live read and write operations
on customer data at speed and scale.

Google's backup storage systems store full and incremental copies of Google's
active systems for a defined period of time to help Google recover data and
systems in the event of a catastrophic outage or disaster. Unlike active
systems, backup systems are designed to receive periodic snapshots of Google
systems and backup copies are retired after a limited window of time as new
backup copies are made.

Throughout the storage systems described above, customer data is encrypted when
stored at rest. For more information, see
[Default encryption at rest](https://cloud.google.com/docs/security/encryption/default-encryption).

## Data deletion pipeline

After customer data is stored in Google Cloud, our systems are designed
to store the data securely until the data deletion pipeline completes its
stages. This section describes the deletion stages.

### Stage 1: Deletion request

The deletion of customer data begins when you initiate a deletion request.
Generally, a deletion request is directed to a specific resource, a
Google Cloud project, or your Google account. Deletion requests might be handled in
different ways depending on the scope of your request:

- **Resource Deletion:** Individual resources containing customer data,
  such as Cloud Storage buckets, can be deleted in a number of ways from
  the Google Cloud console or using API. For example, you can issue a
  remove bucket or
  [gcloud storage rm](https://cloud.google.com/storage/docs/discover-object-storage-gcloud#delete_an_object)
  command to delete a storage bucket through the command line or you can
  select a storage bucket and delete it from the Google Cloud console.
- **Project Deletion:** As a Google Cloud project owner, you can shut
  down a project. Deleting a project acts as a bulk deletion request for all
  resources tied to the corresponding
  [project number](https://cloud.google.com/resource-manager/docs/creating-managing-projects).
- **Google account deletion:** When you delete your Google account, it
  deletes all projects that aren't associated with an organization and that
  are solely owned by you. When there are multiple owners for a
  non-organization project, the project is not deleted until all owners are
  removed from the project or delete their Google accounts. This process
  ensures that projects continue so long as they have an owner.
- **Google Workspace or Cloud Identity account deletion:**
  Organizations that are bound to a Google Workspace or Cloud Identity
  account are deleted when you delete a Google Workspace or
  Cloud Identity account. For more information, see
  [Delete your organization's Google Account](https://support.google.com/a/answer/9468554).

You use deletion requests primarily to manage your data. However, Google can
issue deletion requests automatically; for instance when you end your
relationship with Google.

### Stage 2: Soft deletion

Soft deletion is the point in the process to provide a brief internal staging
and recovery period to help ensure that there is time to recover any data that
has been marked for deletion by accident or error. Individual Google Cloud
products might adopt and configure such a defined recovery period before the
data is deleted from the underlying storage systems so long as the period fits
within Google's overall deletion timeline.

When
[projects are deleted](https://cloud.google.com/resource-manager/docs/creating-managing-projects?visit_id=638488820299910219-3376512512&rd=1#shutting_down_projects),
Google Cloud first identifies the unique project number then it broadcasts
a suspension signal to the Google Cloud products (for example, for example
Compute Engine and Bigtable) that contain that project number.
In this case, Compute Engine suspends operations that are keyed to that
project number and the relevant tables in Bigtable enter an
internal recovery period of up to 30 days. At the end of the recovery period,
Google Cloud broadcasts a signal to the same products to begin logical
deletion of resources tied to the unique project number. Then Google waits (and,
when necessary, rebroadcasts the signal) to collect an acknowledgement signal
(ACK) from the applicable products to complete project deletion.

When a Google account is closed, Google Cloud might impose an internal
recovery period up to 30 days, depending on past account activity. After that
grace period expires, a signal that contains the deleted billing account user ID
is broadcasted to Google products and Google Cloud resources tied solely
to that user ID are marked for deletion.

### Stage 3: Logical deletion from active systems

After the data is marked for deletion and any recovery period has expired, the
data is deleted successively from Google's active and backup storage systems. On
active systems, data is deleted in two ways.

In all Google Cloud products under the [Compute](https://cloud.google.com/products/compute),
[Storage](https://cloud.google.com/products/storage), and [Database](https://cloud.google.com/products/databases) project
categories, except Cloud Storage, copies of the deleted data are marked
as available storage and overwritten over time. In an active storage system like
Bigtable, deleted data is stored as entries within a massive
structured table. Compacting existing tables to overwrite deleted data can be
expensive, as it requires re-writing tables of existing (non-deleted) data, so
mark-and-sweep garbage collection and major compaction events are scheduled to
occur at regular intervals to reclaim storage space and overwrite deleted data.

In Cloud Storage, customer data is also deleted through cryptographic
erasure. This is an industry standard technique that renders data unreadable by
deleting the encryption keys that are needed to decrypt that data. One advantage
of using cryptographic erasure, whether it involves Google-supplied or
customer-supplied encryption keys, is that logical deletion can be completed
even before all deleted blocks of that data are overwritten in
Google Cloud's active and backup storage systems.

### Stage 4: Expiration from backup systems

Similar to deletion from Google's active systems, deleted data is eliminated
from backup systems using both overwriting and cryptographic techniques. In the
case of backup systems, however, customer data is typically stored within large
aggregate snapshots of active systems that are retained for static periods of
time to ensure business continuity in the event of a disaster (for example, an
outage affecting an entire data center), when the time and expense of restoring
a system entirely from backup systems might become necessary. Consistent with
reasonable business continuity practices, full and incremental snapshots of
active systems are made on a daily, weekly, and monthly cycles and retired after
a predefined period of time to make room for the newest snapshots.

When a backup is retired, it is marked as available space and overwritten as new
daily, weekly, or monthly backups are performed.

Note that any reasonable backup cycle imposes a pre-defined delay in propagating
a data deletion request through backup systems. When customer data is deleted
from active systems, it is no longer copied into backup systems. Backups that
were performed before deletion are expired regularly based on the pre-defined
backup cycle.

Finally, cryptographic erasure of the deleted data might occur before the backup
that contains customer data has expired. Without the encryption key that was
used to encrypt specific customer data, the customer data is unrecoverable even
during its remaining lifespan on Google's backup systems.

### Deletion timeline

Google Cloud is engineered to achieve a high degree of speed,
availability, durability, and consistency. The design of systems optimized for
these performance attributes must be balanced carefully with the need to achieve
timely data deletion. Google Cloud commits to delete customer data within
a maximum period of about six months (180 days). This commitment incorporates
the stages of Google's deletion pipeline described above, including the
following:

- **Stage 2:** After the deletion request is made, data is typically
  marked for deletion immediately and our goal is to perform this step within
  a maximum period of 24 hours. After the data is marked for deletion, an
  internal recovery period of up to 30 days might apply depending on the
  service or deletion request.
- **Stage 3:** The time needed to complete garbage collection tasks and
  achieve logical deletion from active systems. These processes might occur
  immediately after the deletion request is received, depending on the level
  of data replication and the timing of ongoing garbage collection cycles.
  After the deletion request is made, it generally takes about two months to
  delete data from active systems, which is typically enough time to complete
  two major garbage collection cycles and ensure that logical deletion is
  completed.
- **Stage 4:** The Google backup cycle is designed to expire deleted data
  within data center backups within six months of the deletion request.
  Deletion may occur sooner depending on the level of data replication and
  the timing of Google's ongoing backup cycles.

The following diagram shows the stages of Google Cloud's deletion
pipeline and when data is erased from active and backup systems.

![Deletion pipeline diagram.](https://cloud.google.com/static/docs/security/images/data-deletion.svg)

## Ensure safe and secure media sanitization

A disciplined media sanitization program enhances the security of the deletion
process by preventing forensic or laboratory attacks on the physical storage
media after it has reached the end of its lifecycle.

Google meticulously tracks the location and status of all storage equipment
within our data centers, through acquisition, installation, retirement, and
destruction, using barcodes and asset tags that are tracked in Google's asset
database. Various techniques such as biometric identification, metal detection,
cameras, vehicle barriers, and laser-based intrusion detection systems are used
to prevent equipment from leaving the data center floor without authorization.
For more information, see the
[Google infrastructure security design overview](https://cloud.google.com/docs/security/infrastructure/design).

Physical storage media can be decommissioned for a range of reasons. If a
component fails to pass a performance test at any point during its lifecycle, it
is removed from inventory and retired. Google also upgrades obsolete hardware to
improve processing speed and energy efficiency, or increase storage capacity.
Whether hardware is decommissioned due to failure, upgrade, or any other reason,
storage media is decommissioned using appropriate safeguards. Google hard drives
use technologies like full disk encryption (FDE) and drive locking to help
protect data at rest during decommission. When a hard drive is retired,
authorized individuals verify that the disk is erased by overwriting the drive
with zeros and performing a multi-step verification process to ensure the drive
contains no data.

If the storage media cannot be erased for any reason, it is stored securely
until it can be physically destroyed. Depending on available equipment, we
either crush and deform the drive or shred the drive into small pieces. In
either case, the disk is recycled at a secure facility, ensuring that no one
will be able to read data on retired Google disks. Each data center adheres to a
strict disposal policy and uses the techniques described to achieve compliance
with
[NIST SP 800-88 Revision 1Guidelines for Media Sanitization](https://csrc.nist.gov/publications/detail/sp/800-88/rev-1/final)
and
[DoD 5220.22-MNational Industrial Security Program Operating Manual](https://www.federalregister.gov/documents/2020/12/21/2020-27698/national-industrial-security-program-operating-manual-nispom).

   Was this helpful?

---

# Customer

> Discover how customer-supplied encryption keys work in Google Cloud.

# Customer-supplied encryption keysStay organized with collectionsSave and categorize content based on your preferences.

*This content was last updated in February 2025 and represents the status quo
as of the time that it was written. Google's security policies and systems may
change going forward, as we continually improve protection for our customers*.

Customer-supplied encryption keys (CSEK) are a feature in
[Cloud Storage](https://cloud.google.com/storage) and
[Compute Engine](https://cloud.google.com/compute). If you supply your own
encryption keys, Google uses your key to protect the Google generated keys that
encrypt and decrypt your data.

This document describes how CSEKs work and how they are protected in
Google Cloud.

## How CSEKs work with Cloud Storage

When you use CSEKs in Cloud Storage, the following keys are part of the
wrapping process:

- **Raw CSEK:** You provide a raw CSEK as part of an API call. The raw CSEK key
  is transmitted from the Google Front End (GFE) to the storage system's memory.
  This key is the key encryption key (KEK) in Cloud Storage for your
  data.
- **Wrapped chunk keys:** The raw CSEK is used to wrap the wrapped chunk keys.
- **Raw chunk keys:** The wrapped chunk keys wrap the raw chunk keys in memory.
  The raw chunk keys are used to encrypt the data chunks that are stored in the
  storage systems. These keys are used as the data encryption keys (DEKs) in
  Cloud Storage for your data.

The following diagram shows the key wrapping process.

![Cloud Storage CSEK.](https://cloud.google.com/static/docs/security/images/csek-cloud-storage.svg)

The following table describes the keys.

| Keys | Stored in | Purpose | Accessible until |
| --- | --- | --- | --- |
| Raw CSEK | Storage system memory | Protects the wrapped chunk keys. | Customer-requested operation (for example,insertObjectorgetObject) is complete. |
| Wrapped chunk keys | Storage devices | Protect raw chunk keys stored at rest. | Storage object is deleted. |
| Raw chunk keys | Storage devices' memory | Protect the data that you read or write to the disk. | Customer-requested operation is complete |

## How CSEKs work with Compute Engine

When you use CSEKs in Compute Engine, the following keys are part of the
wrapping process:

- **Raw CSEK:** You provide a raw CSEK or an [RSA-wrapped
  key](https://cloud.google.com/compute/docs/disks/customer-supplied-encryption#rsa-encryption)
  as part of an API call. The CSEK is transmitted from the GFE to the internal
  cluster manager's front end. The cluster manager is a collection of processes
  running under a cluster manager identity in Google's production infrastructure
  that implements the logic for managing Compute Engine resources such
  as disks and VM instances.
- **Google-owned asymmetric wrapping key:** If an RSA-wrapped key is provided as
  the CSEK, then the key is unwrapped using a Google-owned asymmetric wrapping
  key.
- **CSEK-derived key:** The raw CSEK is combined with a per-persistent disk
  cryptographic nonce to generate a CSEK-derived key. This key is used as the
  KEK in Compute Engine for your data.  In the cluster manager front
  end, both the CSEK and the CSEK-derived key are kept only in the cluster
  manager memory. The CSEK-derived key is used in the cluster manager memory to
  unwrap the wrapped disk keys which are stored in the cluster manager instance
  metadata and instance manager metadata, when automatic restart is enabled
  (this metadata is not the same as the [instance
  metadata](https://cloud.google.com/compute/docs/storing-retrieving-metadata)).
- **Raw disk keys:** The CSEK-derived key is used to wrap raw disk keys when
  creating a disk and to unwrap raw disk keys when accessing a disk. The
  following events occur:
  - If automatic restart is enabled, the wrapped disk keys are stored
    persistently by the cluster manager for the lifespan of the VM so that the
    VM can be restarted in the event of a crash. The wrapped disk keys are
    wrapped with a Google-owned symmetric wrapping key. The permissions of the
    wrapping key allow it to be used only by Compute Engine. If
    automatic restart is turned off, the wrapped disk keys are deleted using the
    deletion process that is described in [Data deletion on
    Google Cloud](https://cloud.google.com/docs/security/deletion).
  - If live migration is enabled, the raw disk key is passed from the old VM
    instance memory to the new VM instance memory without the instance manager
    or cluster manager being involved in the key copy.

The raw disk keys are passed to the memory of the cluster manager (CM), instance
manager, and VM. These keys are used as the DEKs in Compute Engine for
your data.

The following diagram shows how key wrapping works.

![Compute Engine CSEK.](https://cloud.google.com/static/docs/security/images/csek-cloud-compute.svg)

| Keys | Held by | Purpose | Accessible until |
| --- | --- | --- | --- |
| Raw CSEK | Cluster manager front end | Derive the CSEK-derived key by adding a cryptographic nonce. | Customer-requested operation (for example,instances.insert,
instances.attachDisk) is complete. |
| Public-key wrapped CSEK(whenRSA
key wrapping is used) | Cluster Manager front end | Derive the CSEK-derived key by first unwrapping with a Google-owned
asymmetric key. | Customer-requested operation is complete. |
| Google-owned asymmetric key(when RSA key wrapping is
used) | Keystore | Unwrap the RSA-wrapped key. | Indefinitely. |
| CSEK-derived key | Cluster manager front end | Wraps the disk keys. | Key wrapping or unwrapping operation is complete. |
| Google-wrapped disk keys(whenautomatic
restartis used) | Cluster manager front end | Protect disk keys stored at rest, for disks attached to running
instances.Restart the instance in cases where the VM memory is lost (for
example, a host crashes) | VM is stopped or deleted. |
| Raw disk keys | Virtual machine monitor (VMM) memory, cluster manager
memory | Read or write data to the disk, live-migrate the VM, and perform in-place
upgrades | VM is stopped or deleted |
| Google-wrapped CSEK-derived key | Cluster manager database | Restart the operation in case of failure | Customer-requested operation is complete |

## How CSEKs are protected

This section provides information on how CSEKs are protected on disk, as they
move around the Google Cloud infrastructure, and in memory.

Raw CSEKs, CSEK-derived keys, and raw disk keys are never stored on disk
unencrypted. Raw disk keys are stored wrapped with CSEK-derived keys and with
Google keys when automatic restart is used. Google doesn't permanently store
your keys on its servers.

Each service uses access management features provided by the infrastructure to
specify exactly which other services can communicate with it. The service is
configured with the allowlist of the allowed service account identities, and
this access restriction is then automatically enforced by Google Cloud
infrastructure. For more information, see [service identity, integrity, and
isolation](https://cloud.google.com/security/security-design#service_identity_integrity_and_isolation).

The infrastructure also provides cryptographic privacy and integrity for RPC
data on the network. Services can configure the level of cryptographic
protection they want for each infrastructure RPC, and these are enabled for
CSEKs. For more information, see [Encryption of inter-workload
communication](https://cloud.google.com/docs/security/infrastructure/design#encryption-inter-service).

Key material lives in various systems' memory, including cluster manager memory
and VMM memory. Access to these systems' memory is by exception (for example, as
part of an incident) and managed by access control lists. These systems have
memory dumps disabled or automatically scan for key material in memory dumps.
For information about protections to these jobs, see [How Google protects its
production
services](https://cloud.google.com/docs/security/production-services-protection).

## What's next

- [Customer-supplied encryption keys in
  Cloud Storage](https://cloud.google.com/storage/docs/encryption/customer-supplied-keys)
- [Customer-supplied encryption keys in
  Compute Engine](https://cloud.google.com/compute/docs/disks/customer-supplied-encryption)
