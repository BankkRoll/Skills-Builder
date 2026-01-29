# How Google protects the physical and more

# How Google protects the physical

> Discover how Google protects the physical to logical space in data centers.

# How Google protects the physical-to-logical space in a data centerStay organized with collectionsSave and categorize content based on your preferences.

*This content was last updated in May 2024, and represents the status quo
as of the time it was written. Google's security policies and systems may change
going forward, as we continually improve protection for our customers.*

Each Google data center is a large and diverse environment of machines,
networking devices, and control systems. Data centers are designed as industrial
complexes that require a wide range of roles and skills to manage, maintain, and
operate.

In these complex environments, the security of your data is our top priority.
Google implements
[six layers of physical controls (video)](https://www.youtube.com/watch?v=kd33UVZhnAA)
and many
[logical controls](https://cloud.google.com/docs/security/infrastructure/design)
on the machines themselves. We also continuously model threat scenarios in which
certain controls fail or aren't applied.

Some threat scenarios model insider risk and assume that an attacker already
has legitimate access to the data center floor. These scenarios reveal a space
between physical and logical controls that also requires defense in depth. That
space, defined as *arms-length from a machine in a rack to the machine's runtime
environment,* is known as the *physical-to-logical space*.

The physical-to-logical space is similar to the physical environment around
your mobile phone. Even though your phone is locked, you only give physical access
to people who have a valid reason for access. Google takes the same approach to
the machines that hold your data.

## Physical-to-logical controls summary

Within the physical-to-logical space, Google uses three controls that work
together:

- **Hardware hardening:** Reduce each machine's physical access paths,
  known as the *attack surface*, in the following ways:
  - Minimize physical access vectors, like ports.
  - Lock down remaining paths at the firmware level, including
    the basic input/output system (BIOS), any management controllers, and
    peripheral devices.
- **Anomalous event detection:** Generate alerts when physical-to-logical
  controls detect anomalous events.
- **System self-defense:** Recognize a change in the physical environment
  and respond to threats with defensive actions.

Together, these controls provide a defense-in-depth response to security events
that occur in the physical-to-logical space. The following diagram shows all
three controls that are active on a secure rack enclosure.

![The three controls that are active on a secure rack enclosure.](https://cloud.google.com/static/docs/security/images/rack_protections.svg)

## Hardware hardening

Hardware hardening helps to reduce the physical attack surface to minimize
residual risks.

A conventional enterprise data center has an open floor plan and rows of racks
with no barriers between the front panel and people on the data center floor.
Such a data center might have machines with many external ports—such as USB-A,
Micro-USB, or RJ-45—that increase the risk of an attack. Anyone with physical
access to the data center floor can quickly and easily access removable storage
or plug a USB stick with malware into an exposed front panel port. Google data
centers use *hardware hardening* as a foundational control to help mitigate
these risks.

Hardware hardening is a suite of preventative measures on the rack and its
machines that helps reduce the physical attack surface as much as possible.
Hardening on machines include the following:

- Remove or disable exposed ports and lock down remaining ports at the
  firmware level.
- Monitor storage media with high-fidelity tamper-detection signals.
- [Encrypt data at rest](https://cloud.google.com/docs/security/encryption/default-encryption#default_encryption_of_data_at_rest).
- Where supported by the hardware, use device attestation to help prevent
  unauthorized devices from deploying in the runtime environment.

In certain scenarios, to help ensure that no personnel have physical access to
machines, Google also installs secure rack enclosures that help to prevent or
deter tampering. The secure rack enclosures provide an immediate physical
barrier to passersby and can also trigger alarms and notifications for security
personnel. Enclosures, combined with the machine remediations discussed earlier,
provide a powerful layer of protection for the physical-to-logical space.

The following images illustrate the progression from fully open racks to secure
rack enclosures with full hardware hardening.

- The following image shows a rack with no hardware hardening:
  ![A rack with no hardware hardening.](https://cloud.google.com/static/docs/security/images/no-hardware-hardening.png)
- The following image shows a rack with some hardware hardening:
  ![A rack with some hardware hardening.](https://cloud.google.com/static/docs/security/images/some-hardware-hardening.png)
- The following image shows the front and back of a rack with full hardware hardening:
  ![The front and back of a rack with full hardware hardening.](https://cloud.google.com/static/docs/security/images/full-hardware-hardening.png)

## Anomalous event detection

Anomalous event detection lets security staff know when machines
experience unexpected events.

Industry-wide, organizations can take months or years to discover security
breaches, and often only after significant damage or loss has occurred. The
critical indicator of compromise (IoC) might be lost in a high volume of logging
and telemetry data from millions of production machines. Google, however, uses
multiple data streams to help identify potential physical-to-logical
security events in real time. This control is called *anomalous event
detection*.

Modern machines monitor and record their physical state as well as events that
occur in the physical-to-logical space. Machines receive this information
through ever-present automated system software. This software may run on
miniature computers inside the machine, called *baseboard management controllers
(BMCs)*, or as part of an operating system daemon. This software reports
important events such as login attempts, insertion of physical devices, and
sensor alarms such as an enclosure tamper sensor.

For machines with hardware root-of-trust, anomalous event detection signals
become even stronger. Hardware root-of-trust allows system software, such as BMC
firmware, to attest that it booted safely. Google detection systems, therefore,
have an even higher degree of confidence that reported events are valid. For
more information about independent roots of trust, see
[Remote attestation of disaggregated machines](https://cloud.google.com/docs/security/remote-attestation).

## System self-defense

System self-defense lets systems respond to potential compromises with
immediate defensive action.

Some threat scenarios assume that an attacker in the physical-to-logical space
can defeat the physical access measures discussed in
[Hardware hardening](#hardware-hardening).
Such an attacker might be targeting user data or a sensitive process that is
running on a machine.

To mitigate this risk, Google implements *system self-defense*: a control that
provides an immediate and decisive response to any potential compromise. This
control uses the telemetry from the physical environment to act in the logical
environment.

Most large-scale production environments have multiple physical machines in one
rack. Each physical machine runs multiple workloads, like virtual machines (VMs)
or Kubernetes containers. Each VM runs its own operating system using dedicated
memory and storage.

To determine which workloads are exposed to security events, Google aggregates
the telemetry data from the hardware-hardening controls and anomalous event
detection. We then correlate the data to generate a small set of events that are
high-risk and require immediate action. For example, the combination of a secure
rack door alarm and a machine chassis opening signal might constitute a
high-risk event.

When Google detects these events, systems can take immediate action:

- Exposed workloads can immediately terminate sensitive services and wipe
  any sensitive data.
- The networking fabric can isolate the affected rack.
- The affected workloads can be rescheduled on other machines or even data
  centers, depending on the situation.

Because of the system self-defense control, even if an attacker succeeds in
getting physical access to a machine, the attacker can't extract any data and
can't move laterally in the environment.

## What's next

- For more information about physical controls, read about
  [data center security](https://www.google.com/about/datacenters/data-security/).
- For more information about logical controls, read
  [Google infrastructure security design overview](https://cloud.google.com/docs/security/infrastructure/design).
- To learn about Google security culture, read
  [Building secure and reliable systems (O'Reilly book)](https://www.oreilly.com/library/view/building-secure-and/9781492083115/).

   Was this helpful?

---

# Privileged access in Google CloudStay organized with collectionsSave and categorize content based on your preferences.

> How Google Cloud manages access by its personnel to customer data

# Privileged access in Google CloudStay organized with collectionsSave and categorize content based on your preferences.

*This content was last updated in February 2025, and represents the status quo
as of the time it was written. Google's security policies and systems may change
going forward, as we continually improve protection for our customers*.

This document describes the features and products that help you control the
access that Google personnel have to your customer data. As defined in the
[Google Cloud Terms of Service](https://cloud.google.com/terms), *customer
data* is data that customers or end users provide to Google through the services
under their account.

## Overview of privileged access

Typically, your customer data is only accessed by you and the Google Cloud
services that you enable. In some cases, Google personnel might require access
to your data to help provide a contracted service (for example, you require
support or need to recover from an outage). This type of access is known as
*privileged access*.

Highly-privileged employees who are temporarily granted or acquire elevated
permissions pose a higher insider risk. Our approach to privileged access
focuses on reducing the number of possible attack vectors. For example, we use
the following security controls:

- Redundant authentication schemes
- Limited data access pathways
- Logging and alerting actions across our systems
- Regulated permissions

This approach helps us control and detect internal attacks, limit the impact of
incidents, and reduce the risk to your data.

The privileged access management strategy in Google Cloud limits the
ability of Google personnel to view or modify customer data. In
Google Cloud, limits on privileged access are an integral part of how our
products are designed to work.

For more information about when Google personnel might access your data, see the
[Cloud Data Processing
Addendum](https://cloud.google.com/terms/data-processing-addendum).

## Privileged access philosophy

Google's privileged access philosophy uses the following guiding principles:

- **Access restrictions must be based on roles and multi-party approvals**:
  Google personnel are denied system access by default. When access is granted,
  it is temporary and is no greater than necessary to perform their role. Access
  to customer data, critical operations on production systems, and modifications
  of source code are controlled by manual and automated verification systems.
  Google personnel can't access customer data without another individual
  approving the request. Personnel can only access the resources that are
  necessary to do their jobs and must provide a valid justification to access
  customer data. For more information, see [How Google protects its production
  services](https://cloud.google.com/docs/security/production-services-protection).
- **Workloads must have end-to-end protection**: With [encryption in
  transit](https://cloud.google.com/docs/security/encryption-in-transit),
  [encryption at
  rest](https://cloud.google.com/docs/security/encryption/default-encryption),
  and
  [Confidential Computing](https://cloud.google.com/confidential-computing/docs/confidential-computing-overview)
  for encryption in use, Google Cloud can provide end-to-end encryption
  of customer workloads.
- **Logging and auditing are continuous**: Google personnel access to customer
  data is logged and threat detection systems conduct real-time audits, alerting
  the security team when log entries match threat indicators. Internal security
  teams evaluate alerts and logs to identify and investigate anomalous
  activities, limiting the scope and impact of any incident. For more
  information about incident response, see [Data incident response
  process](https://cloud.google.com/docs/security/incident-response).
- **Access must be transparent and include customer controls**: You can use
  [customer-managed encryption keys
  (CMEK)](https://cloud.google.com/kms/docs/cmek) to manage your own encryption
  keys and control access to them. In addition,
  [Access Transparency](https://cloud.google.com/assured-workloads/access-transparency/docs/overview)
  ensures that all privileged access has a [business justification that is
  logged](https://cloud.google.com/logging/docs/audit/reading-access-transparency-logs#justification_reason_codes).
  [Access Approval](https://cloud.google.com/assured-workloads/access-approval/docs/overview)
  lets you approve or deny access requests by Google personnel to certain
  datasets.

## Google personnel access to customer data

By default, Google personnel don't have access to Google Cloud customer
data.

To obtain access, Google personnel must meet the following conditions:

- Be a member of relevant access control lists (ACLs).
- Read and acknowledge Google's data access policies regularly.
- Use a trusted device.
- Sign in with multi-factor authentication using a
  [Titan Security Key](https://cloud.google.com/security/products/titan-security-key),
  which minimizes the risk of credentials being phished.
- Access tools that evaluate the justification that was provided (for example,
  the support ticket or issue ID), the user's role, and the context.
- If required by the tools, obtain authorization approval from another qualified
  Google personnel.
- If you have enrolled in Access Approval, obtain your approval.

Different personnel roles require different levels of access. For example,
support roles have limited access to customer data that is directly related to a
customer support ticket. Engineering roles might require additional system
privileges to address more complex issues related to service reliability or
deploying services.

When Google works with third parties (like customer support vendors) to provide
Google services, we assess the third party to ensure that they provide the
appropriate level of security and privacy. Google Cloud publishes a [list
of all subprocessors](https://cloud.google.com/terms/subprocessors#1) that are
used to assist in providing the service.

### Reasons for Google personnel to access customer data

Although Google Cloud is designed to automate, minimize, or eliminate the
need for Google personnel to access customer data, there are still some cases
where Google personnel might access customer data. These cases include
customer-initiated support, outage or tool failure, third-party legal requests,
and Google-initiated reviews.

#### Customer-initiated support

Google personnel access to customer data in services that use Access Transparency
are usually the result of customer-initiated events such as contacting
Customer Care. When you contact Customer Care personnel to
resolve
an issue, Customer Care personnel only obtain access to low-sensitive
data. For example, if you lost access to a bucket, Customer Care
personnel only have access to low-sensitive data such as the bucket name.

#### Outage or tool failure

During outages or tool failures, Google personnel can access customer data to
perform a backup or recovery as needed. In these situations, Google personnel
use tools that can directly access customer data to maximize efficiency and
resolve the issue in a timely manner. These tools log this access and the
justifications that are provided by the engineers. Access is also audited and
logged by the Google security response team. [Supported Google Cloud
services](https://cloud.google.com/assured-workloads/access-transparency/docs/supported-services)
generate Access Transparency logs that are visible to you during an outage.
During an outage, engineers can't bypass the allowlist for the resource;
however, they can access the data without your approval.

#### Third-party legal requests

Third-party legal requests are
[rare](https://cloud.google.com/blog/products/identity-security/google-clouds-semi-annual-transparency-report-now-available),
and only the legal team can generate a valid legal access justification. The
legal team reviews the request to ensure that the request meets legal
requirements and Google policies, provides notification to you when legally
permitted, and considers objections to disclose the data to the extent that the
law allows. For more information, see [Government Requests for Cloud Customer
Data
(PDF)](https://services.google.com/fh/files/blogs/government_access_technical_whitepaper.pdf).

#### Google-initiated review

Google-initiated reviews are also rare. When they do occur, they are to ensure
that customer data is safe, secure, and hasn't been compromised. The main
reasons for these reviews are security concerns, fraud, abuse, or compliance
audits. For example, if automated bitcoin mining detectors detect that a VM is
being used for bitcoin mining, Google reviews the issue and confirms that
malware on a VM device is exhausting the VM's capacity. Google removes the
malware so that VM usage returns to normal.

## How Google controls and monitors access to customer data

Google's internal controls include the following:

- Pervasive infrastructure-wide control systems to prevent unauthorized access
- Detection and remediation of unauthorized access through continuous controls
- Monitoring, violation alerting, and regular audits by an internal audit team
  and independent third-party auditors

To learn more about how Google secures the physical infrastructure, see the
[Google infrastructure security design
overview](https://cloud.google.com/docs/security/infrastructure/design).

### Infrastructure-wide controls

Google has built its infrastructure with security at its core. Because Google's
global infrastructure is fairly homogeneous, Google can use automated
infrastructure to implement controls and limit privileged access. The following
sections describe some of the controls that help implement our privilege access
principles.

#### Strong authentication for all access

Google has strong authentication requirements for access by users (like an
employee) and roles (like a service) to data. Jobs running in our production
environment use these identities to access data stores or remote procedure call
(RPC) methods of other services. Multiple jobs might run with the same identity.
Our infrastructure restricts the ability to deploy or modify jobs that have a
particular identity to those responsible for running the service⼀generally our
Site Reliability Engineers (SREs). When a job starts, it is provisioned with
cryptographic credentials. The job uses these credentials to prove its identity
when making requests of other services (using [application layer transport
security
(ALTS)](https://cloud.google.com/docs/security/encryption-in-transit/application-layer-transport-security)).

#### Context-aware access

To achieve zero-trust security, Google's infrastructure uses context to
authenticate and authorize users and devices. Access decisions aren't based
exclusively on static credentials or whether the decisions originate from a
corporate intranet. The complete context of a request (such as the user
identity, location, device ownership and configuration, and fine-grained access
policies) is evaluated to determine the request's validity and guard against
phishing attempts and credential-stealing malware.

By using context, each authentication and authorization request must use strong
passwords with security tokens or other two-factor authentication protocols.
Authenticated users and trusted devices are granted limited, temporary access to
necessary resources. Machine inventories are securely maintained and the state
of each connecting device (for example, OS updates, security patches, device
certificates, installed software, virus scans, and encryption status) is
evaluated for potential security risks.

For example, Chrome Enterprise Premium helps ensure employee credentials aren't stolen or
misused and that connecting devices aren't compromised. By shifting access
controls from the network perimeter to the context of individual users and
devices, Chrome Enterprise Premium also lets Google personnel work more securely from
virtually any location without the need for a VPN.

#### Review and authorization for all production software

Our infrastructure is containerized using a cluster management system called
Borg. [Binary Authorization for
Borg](https://cloud.google.com/docs/security/binary-authorization-for-borg) ensures that production
software is reviewed and approved before it's deployed, particularly when our
code can access sensitive data. Binary Authorization for Borg helps ensure code
and configuration deployments meet certain standards and alerts service owners
when these requirements aren't met. By requiring code to meet certain standards
and change management practices before accessing user data, Binary Authorization
for Borg reduces the potential for Google personnel (or a compromised account)
to act alone to access user data programmatically.

### Access log files

Google infrastructure logs data access and code changes. The types of logging
include the following:

- **Customer logs**: Available using [Cloud Audit Logs](https://cloud.google.com/logging/docs/audit).
- **Administrative access logs**: Available using
  [Access Transparency](https://cloud.google.com/assured-workloads/access-transparency/docs/overview).
- **Deployment integrity logs**: Internal logs about exceptions that are
  monitored by a central security team that is dedicated to auditing access to
  customer data. Exception monitoring helps protect sensitive data and enhance
  production reliability. Exception monitoring helps ensure that unreviewed or
  unsubmitted source code doesn't run in privileged environments, whether
  accidentally or as a result of a deliberate attack.

### Incident detection and response

To detect and respond to suspected access violations, Google uses expert
internal investigation teams and manual and automated controls that combine
machine learning, advanced data processing pipelines, and threat intelligence
incidents.

#### Signal development

The core of Google's detection and response capabilities is threat intelligence,
which is fortified by the continuous analysis of past incidents, network
traffic, internal data, system access logs, anomalous behavior patterns, the
results of offensive security exercises, and many more proprietary alerts. This
data is analyzed by dedicated teams that produce a dynamic database of signals,
or *threat indicators*, that include all of Google. Engineering teams use threat
indicators to develop specialized detection systems to monitor internal systems
for malicious activity, alert appropriate staff, and implement automated
responses (for example, revoking access to a resource).

#### Threat detection

Threats are primarily detected by scanning logs and matching log entries to
threat indicators. As a result of strong authentication, Google can delineate
between human events, service events, and service impersonation events in the
logs to prioritize investigations into actual human access. Activities that
involve the access of user data, source code, and sensitive information are
logged and a business justification or exception is required. Threats can
include an individual attempting to take unilateral action on sensitive systems
or attempting to access user data without a valid business reason. These types
of activities have defined alerting procedures.

#### Incident investigation

When policy violations are detected, security teams who are separate from the
core engineering and operations teams provide independent oversight and conduct
an initial investigation. The security teams complete the following tasks:

- Review details of the incident and determine if the access was intentional,
  unintentional, accidental, caused by a bug or misconfiguration, or the result
  of inadequate controls (for example, an external attacker stealing and using
  the credentials of a compromised employee).
- If the access is unintentional or accidental (for example, Google personnel
  were unaware of, or mistakenly violated, access protocols), the teams can take
  immediate steps to remediate the issue (for example, by recovering
  intellectual property).
- If malicious behavior is suspected, the security team escalates the incident
  and collects additional information, including data and system access logs, to
  determine the scope and impact of the incident.
- Depending on the results of that inquiry, the security team submits incidents
  for additional investigation, documentation and resolution, or, in extreme
  cases, refers the incident to outside authorities or law enforcement.

#### Remediation

The security team uses past incidents to identify and resolve vulnerabilities
and improve detection capabilities. All incidents are documented and metadata is
extracted to identify specific tactics, techniques, and procedures for each
exploit. The team uses that data to develop new threat indicators, reinforce
existing protections, or make feature requests for security improvements.

## Services that monitor and control Google's access to data

The following Google Cloud services provide you with options to achieve
visibility and control over Google's access to your data.

| Google Cloud service | Description |
| --- | --- |
| Access Approval | If you have highly sensitive or restricted data,
Access Approval lets you require your approval before an
authorized Google administrator can access your data to support you. Approved
access requests are logged with Access Transparency logs that are linked to the
approval request. After you approve a request, access must be properly
privileged within Google before access is permitted. For a list of
Google Cloud services that support Access Approval, seeSupported
services. |
| Access Transparency | Access Transparency logs administrative access by Google authorized
personnel when they support your organization or are maintaining service
availability. For a list of Google Cloud services that support
Access Transparency, seeSupported
services. |
| Assured Workloads | UseAssured Workloadsif your enterprise requires dedicated regional support, certified regulatory
programs (for example, FedRAMP or ITAR), or programs like Sovereign Controls for
EU. Assured Workloads provides Google Cloud users with an
enablement workflow to create and monitor the lifespan of the control packages
that you require. |
| Cloud KMS | UseCloud KMSwith Cloud EKM to control your encryption keys. Cloud KMS with
Cloud EKM lets you encrypt data with encryption keys that are stored
and managed in a third-party key management system that's deployed outside
Google's infrastructure. Cloud EKM lets you maintain separation between
data at rest and encryption keys while still using the power of cloud compute
and analytics. |
| Confidential Computing | Use Confidential Computing to encrypt data in use.
Google Cloud includes the following services that enable confidential
computing:Confidential VM: Enable encryption of data in use for
workloads that use VMsConfidential Google Kubernetes Engine Nodes: Enable encryption of data in use for
workloads that use containersConfidential Dataflow: Enable encryption of data in use for
streaming analytics and machine learningConfidential Dataproc: Enable encryption of data in use for
data processingConfidential Space: Enable encryption of data in use for
joint data analysis and machine learningThese services let you reduce yourtrust boundaryso that
fewer resources have access to your confidential data. For more information, seeImplement
confidential computing on Google Cloud. |
| Key Access Justifications | UseKey Access Justificationsfor data sovereignty and discovery.Key Access Justifications gives you a
justification every time your externally hosted keys are used to decrypt data.
Key Access Justifications requires Cloud KMS with Cloud HSM or
Cloud KMS with Cloud EKM to advance the control that you have
over your data. You must approve access before Google personnel can decrypt your
data at rest. |

## What's next

- To know more about our commitment toward protecting the privacy of customer
  data, see [Google Cloud and common privacy
  principles](https://cloud.google.com/privacy/common-privacy-principles).
- To learn about the core principles for controls that prevent unauthorized
  administrative access, see [Overview of administrative access
  controls](https://cloud.google.com/assured-workloads/cloud-provider-access-management/docs/administrative-access).
- To see the list of business justifications for which Google personnel can
  request to access customer data, see [Justification reason
  codes](https://cloud.google.com/assured-workloads/access-transparency/docs/reading-logs#justification-reason-codes).

   Was this helpful?
