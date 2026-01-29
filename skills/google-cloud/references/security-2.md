# Binary Authorization for BorgStay organized with collectionsSave and categorize content based on your preferences. and more

# Binary Authorization for BorgStay organized with collectionsSave and categorize content based on your preferences.

# Binary Authorization for BorgStay organized with collectionsSave and categorize content based on your preferences.

*This content was last updated in May 2024, and represents the status quo as
of the time it was written. Google's security policies and systems may change
going forward, as we continually improve protection for our customers.*

This document describes how we use code reviews, security infrastructure, and an
enforcement check called *Binary Authorization for Borg (BAB)* to help protect
Google's software supply chain against insider risk. BAB helps reduce insider
risk because it ensures that production software is reviewed and approved before
it's deployed, particularly when our code can access sensitive data. BAB applies
to all services that are running on
[Borg](https://cloud.google.com/docs/security/infrastructure/design#secure-service). Since the original
publication of this document, we have included key concepts of BAB into an open
specification called [Supply-chain Levels for Software Artifacts
(SLSA)](https://slsa.dev).

This document is part of a series of technical papers that describes some
projects that the Google security team have developed to help improve security,
including
[BeyondCorp](https://cloud.google.com/beyondcorp)
and
[BeyondProd](https://cloud.google.com/docs/security/beyondprod).
For an overview of our infrastructure's security, see the
[Google infrastructure security design overview](https://cloud.google.com/docs/security/infrastructure/design).

## Introduction

Insider risk  represents a threat to the security of user data, which can
include employment data, financial data, or other proprietary or business data.
 Insider risk is the potential for an employee to use their
organizational knowledge or access to perform malicious acts, or for an external
attacker to use the compromised credentials of an employee to do the same.

To minimize insider risk within our software supply chain, we use BAB. BAB  is an internal enforcement check that occurs when software is
deployed. BAB ensures that code and configuration deployments meet certain
minimum standards and support uniformity in our production systems.

We help protect user data within our production systems by limiting unilateral
access  by our employees. BAB helps ensure that employees, while
acting alone, cannot directly or indirectly access or otherwise affect user data
without proper authorization and justification. BAB and its associated controls
help us enforce least privilege, which improves our security posture
independently from a specific threat actor. In other words, BAB limits
unilateral access regardless of whether the actor has malicious intent, their
account has been compromised, or they have unintentionally been granted access.

## BAB benefits

Adopting BAB and a containerized deployment model provides many security
benefits to Google infrastructure. The benefits include the following:

- **BAB helps reduce overall insider risk:** BAB requires code to meet
  certain standards and change management practices before the code can
  access user data. This requirement reduces the potential for an employee
  acting alone (or a compromised employee account) from accessing user data
  programmatically.
- **BAB supports uniformity of production systems:** By using
  containerized systems and verifying their BAB requirements before
  deployment, our systems become easier to debug, more reliable, and have
  well-defined change management processes. BAB requirements provide a common
  language for production system requirements.
- **BAB dictates a common language for data protection:** BAB tracks
  conformance across Google systems. Data about this conformance is published
  internally and is available to other teams. Publishing BAB data enables
  teams to use common terms when communicating with each other about their
  data access protection. This common language reduces the back-and-forth
  work that is needed when working with data across teams.
- **BAB allows programmatic tracking of compliance requirements:** BAB
  simplifies what were previously manual compliance tasks. Certain processes
  at Google require tighter controls on how we deal with data. For example,
  our financial reporting systems must comply with the Sarbanes-Oxley Act
  (SOX). Before BAB, we had a system that helped us manually perform
  verifications to ensure our compliance. With the introduction of BAB, many
  of these checks were automated based on the BAB policies for the services.
  Automating these checks enabled the compliance team to increase both the
  scope of services covered and the adoption of appropriate controls on these
  services.

BAB is part of the larger
[BeyondProd](https://cloud.google.com/docs/security/beyondprod)
framework that we use to mitigate insider risk.

## Our development and production process

By default, Google's development and production process includes four mandatory
steps: code review, verifiable builds, containerized deployment, and
service-based identity. The following sections describe these steps in more
detail.

### Step 1: Code review

Most of our source code is stored in a
[central monolithic repository](https://research.google/pubs/why-google-stores-billions-of-lines-of-code-in-a-single-repository/),
 and requires review and approval  from at least one engineer other than the author. A monolithic
codebase allows for the enforcement of a single choke point for code
reviews.

At a minimum, our code review process requires that the
owners of a system must approve code modifications to that system.

When importing changes from third-party  or open source code, we verify that the change is appropriate
(for example, the latest version).  However, we often don't have the same review controls in place
for every change made by external developers to the third-party or open source
code we use.

### Step 2: Verifiable builds

Our build system  is similar to
[Bazel](https://bazel.build/),
which builds and compiles source code to create a binary for deployment. Our
build system runs in an isolated and locked-down environment  that is separated from the employees performing the builds. For
each build, the system produces provenance generated by verifiable builds . This provenance is a signed certificate that describes the
sources and dependencies that went into the build, the cryptographic hashes of
any binaries or other build artifacts, and the full build parameters. This
provenance enables the following:

- The ability to trace a binary to the source code that was used in its
  creation. By extension, the provenance can also trace the process around the
  creation and submission of the source code it describes.
- The ability to verify that the binary wasn't modified as any changes to
  the file would automatically invalidate its signature.

Because build actions can be arbitrary code, our build system has been hardened
for multi-tenancy. In other words, our build system is designed to prevent one
build from influencing any other builds. The system prevents builds from making
changes that could compromise the integrity of the build provenance or
of the system itself. After the build is complete, the change is deployed using
Borg.

### Step 3: Containerized deployment

After the build system creates the binary, it's packaged into a container image
 and deployed as a *Borg job*  on our cluster orchestration system,
[Borg](https://research.google.com/pubs/pub43438.html).
 We run hundreds of thousands of jobs from many different
applications, across multiple clusters, each with up to tens of thousands of
machines. Despite this scale, our production environment is fairly homogeneous.
As a result, the touchpoints for access to user data can be more easily
controlled and audited.

Containers  provide notable security benefits. Containers are meant to be
immutable, with frequent redeployments from a complete image rebuild.
Containerization enables us to review a code change in context, and provides a
single choke point for changes that get deployed into our infrastructure.

A Borg job's configuration  specifies the requirements for the job to be deployed: the
container images, runtime parameters, arguments, and flags. Borg schedules the
job, taking into account the job's constraints, priority, quota, and any other
requirements that are listed in the configuration. After the job is deployed,
the Borg job can interact with other jobs in production.

### Step 4: Service-based identity

A Borg job runs as a service identity.  This identity is used to access datastores or remote procedure
call (RPC) methods  of other services.
Multiple jobs might run as the same identity. Only those employees who are
responsible for running the service  (typically
[Site Reliability Engineers (SREs)](https://sre.google/))
can deploy or modify jobs with a particular identity.

When Borg starts a job, it provisions the job with cryptographic credentials. The job uses these credentials to prove its identity when
making requests of other services using
[Application Layer Transport Security (ALTS)](https://cloud.google.com/docs/security/encryption-in-transit/application-layer-transport-security).
For a service to access certain data or another service, its identity must have
the necessary permissions.

Our policies require BAB protection for service identities that have access to
user data and any other sensitive information.  Quality assurance and development jobs that
don't have access to sensitive data are permitted to run with fewer
controls.

## How BAB works

BAB integrates with Borg  to ensure that only authorized jobs are allowed to run with the
identity of each service. BAB also creates an audit trail  of the code and configuration used in BAB-enabled jobs to allow
for monitoring and incident response.

BAB is designed to ensure that all production software and configuration is
properly reviewed, checked in, built verifiably, and authorized, particularly
when that code can access user
data.

### Service-specific policy

When service owners onboard their service to Borg,  they create a BAB policy that defines the security requirements for
their service. This policy is called the *service-specific policy*. Defining or
modifying
a policy is itself a code change that must undergo review.

The service-specific policy defines what code and configuration is allowed to
run as the service's identity, as well as the required properties of that code
and configuration. All jobs running as the service identity must meet the
service-specific policy.

All Borg services at Google are required to configure a service-specific policy.

By default, this practice enforces the following requirements:

- **Code must be auditable:**  We can trace the container image back to its
  human-readable sources through provenance generated by verifiable builds. A
  retention policy keeps the human-readable sources of the code for at least
  18 months, even if the code is not submitted.
- **Code must be submitted:**  The code is built from a specified, defined location in
  our source repository. Submission generally implies that the code has
  undergone a code review.
- **Configurations must be submitted:**  Any configurations that are provided during deployment go
  through the same review and submission process as regular code. Therefore,
  command-line flag values, arguments, and parameters can't be modified
  without review.

Services that don't have access to sensitive data — or, in rare
circumstances, services that have a valid and approved exception — might
have a more permissive policy, such as one that only requires auditability of
code, or even one that turns off BAB entirely.

The systems and components that enforce BAB are tightly controlled using strict
automated requirements and additional manual controls.

### Enforcement modes

BAB uses two *enforcement modes* to ensure that jobs comply with the
service-specific policy:

- Deploy-time enforcement, which blocks non-compliant jobs from deploying.
- Continuous validation, which monitors and alerts on non-compliant jobs that
  were deployed.

Additionally, in case of an emergency, emergency response procedures can bypass
deploy-time enforcement.

#### Deploy-time enforcement mode

Borg Prime is Borg's centralized controller, which acts as the certificate
authority for ALTS. When a new job is submitted, Borg Prime consults BAB to
verify that the job meets the service-specific policy requirements before Borg
Prime grants the ALTS certificate to the job. This check acts as an admission
controller: Borg only starts the job if it satisfies the service-specific
policy. This check occurs even when the employee or service making the deployment
request is otherwise authorized.

In rare cases, services can opt-out of deploy-time enforcement with an adequate
justification.

#### Continuous verification mode

After a job is deployed, it's continuously verified for its lifetime,
regardless of its enforcement mode at deployment time. A BAB process runs at
least once a day to check that jobs that were started (and might still be
running) conform to any updates to their policies.  For example, continuous verification mode is constantly
checking for jobs that are running with outdated policies or were deployed using
emergency response procedures. If a job is found that
doesn't adhere to the latest policy, BAB notifies the service owners so that
they can mitigate the risk.

#### Emergency response procedures

When an incident or outage occurs, our first priority is to restore the
affected service as quickly as possible. In an emergency situation, it might be
necessary to run code that hasn't been reviewed or verifiably built. As a result,
enforcement mode can be overridden using an emergency response flag.  Emergency response procedures also act as a backup in case
there is a failure of BAB that would otherwise block a deployment. When a
developer deploys a job using the emergency response procedure, they must submit
a justification as part of their request.

During an emergency response, BAB logs details about the associated Borg job and
sends a notification to both Google's centralized security team  and the team that owns the service identity.  The
log entry includes a reference to a snapshot of the code that was deployed and
the user-provided justification. Emergency response procedures are only meant to
be used as a last resort.

### Extending BAB to other environments

Initially, BAB only supported protection of Borg jobs and required the software
to be developed using Google's traditional source control, build, and packaging
pipeline. Now, BAB has added support for protecting other software delivery and
deployment environments and support for alternative source control, build, and
packaging systems. The implementation details for these various environments
differ, but the benefits of BAB remain.

There are a few cases that do not lend themselves well to human code reviews
before deployment, notably iterative development of machine learning code and
high-frequency data analysis. In these cases, we have alternative controls that
compensate for human review.

## Adopting similar controls in your organization

This section describes the best practices that we learned as we implemented BAB
so that you can adopt similar controls in your organization.

### Create a homogeneous, containerized CI/CD pipeline

The adoption of BAB was made easier because most teams used a single source
control system, code review process, build system, and deployment system. Code
reviews were already part of our culture, so we were able to make changes
without too many significant user-visible changes. To adopt BAB, we focused on
code reviews, verifiable builds, containerized deployments, and service-based
identities for access control. This approach simplified the adoption of BAB and
strengthened the guarantees that a solution like BAB can provide.

Our widespread use of microservices and service-based identities (like service
accounts), rather than host-based identities (like IP addresses), let us build
fine-grained control over the software that is permitted to run each service.

If your organization is unable to adopt a service identity directly, you could
try protecting identity tokens using other measures as an interim step.

### Determine your goals, and define your policies based on your requirements

Build your policy-driven release process one piece at a time. You might need to
implement certain changes earlier than others in your CI/CD pipeline. For
example, you might need to start conducting formal code reviews before you can
enforce them at deployment time.

A great motivator for a policy-driven release process is compliance. If you can
encode at least some of your compliance requirements in a policy, it can help
automate your tests and ensure that they are reliably in effect. Start with a base
set of requirements and codify more advanced requirements as you go.

### Enforce policies early in development

It's hard to define comprehensive policies on a piece of software without first
knowing where it will run and what data it will access. Therefore,
service-specific policy enforcement is done when code is deployed and when it
accesses data, not when it‘s built. A policy is defined in terms of a runtime
identity, so the same code might run in different environments and be subject to
different policies.

We use BAB in addition to other access mechanisms to limit access to user data.
Service owners can further ensure that data is only accessed by a job that meets
particular BAB requirements.

### Enlist change agents across teams

When we created a Google-wide mandate  for BAB deployment, what most affected our success rate was
finding owners to drive the change in each product group. We identified a
handful of service owners who saw immediate benefits from enforcement and were
willing to provide feedback. We asked these owners to volunteer before making
any changes mandatory. After we had their help, we set up a formal change
management team to track ongoing changes. We then identified accountable owners
in each product team to implement the changes.

### Determine how to manage third-party code

If you must manage third-party code, consider how you will introduce your
policy requirements to your third-party codebase. For example, you could
initially start by keeping a
repository of all third-party code used. We recommend that you regularly vet
that code against your security requirements.

For more information on managing third-party code, see
[Shared success in building a safer open source community](https://blog.google/technology/safety-security/shared-success-in-building-a-safer-open-source-community/).

## What's next

- Read about
  [BeyondProd](https://cloud.google.com/docs/security/beyondprod),
  which we use to build a secure perimeter around our microservices.
- To adopt a secure CI/CD pipeline, see
  [Supply chain Levels for Software Artifacts (SLSA)](https://slsa.dev/).

---

# How Google enforces boot integrity on production machinesStay organized with collectionsSave and categorize content based on your preferences.

> Discover how Google enforces boot integrity on production machines in data centers.

# How Google enforces boot integrity on production machinesStay organized with collectionsSave and categorize content based on your preferences.

*This content was last updated in May 2024, and represents the status quo
as of the time it was written. Google's security policies and systems may change
going forward, as we continually improve protection for our customers.*

This document describes the infrastructure controls that Google uses to enforce
the integrity of the boot process on production machines that are equipped with
[Titan](https://cloud.google.com/docs/security/titan-hardware-chip).
These controls, built on top of a *measured boot* process, help ensure that
Google can recover its data center machines from vulnerabilities throughout
their boot stack and return the machines from arbitrary boot states to known
good configurations.

## Introduction

The security posture of a data center machine is highly dependent on the
machine's configuration at boot time. The machine's boot process configures the
machine's hardware and initializes its operating system, while keeping the
machine safe to run in Google's production environment.

At each step in the boot process, Google implements industry-leading controls
to help enforce the boot state that we expect and to help keep customer data
safe. These controls help ensure that our machines boot into their intended
software, allowing us to remove vulnerabilities that could compromise the
initial security posture of the machine.

This document describes the boot process and demonstrates how our controls
operate during the boot flow. The key objectives of our controls are the following:

- Establish trust in machine credentials through [hardware roots-of-trust](#hardware-roots-of-trust)
- [Seal machine credentials](#credential-sealing-process) to a boot policy that specifies allowed firmware and software versions
- Enforce the boot policy on machines through a [measured boot process](#measured-boot-process)

## Background

This section defines and provides context for the terms *machine credentials*,
*hardware root of trust*, *sealed credentials*, and *cryptographic sealing*.

### Machine credentials

One of the central components in Google's machine management system is our
credential infrastructure, which consists of an internal certificate authority
(CA) and other control plane elements that are responsible for coordinating
credential rotation flows.

Machines in Google's production fleet perform mutual authentication when
establishing secure channels. To perform mutual authentication, each machine
possesses Google's CA public keys. Each machine also possesses its own
public/private key pair, as well as a certificate for that key pair.

Each machine's public/private key pair, together with the certificate signed by
the CA, is known as a *machine credential*, which the machine uses to
authenticate itself to other machines in the fleet. Within the production
network, machines check that other machines' public keys are certified by
Google's CA before exchanging traffic.

### Hardware roots of trust and cryptographic sealing

As computing devices grow more sophisticated, each device's attack surface also
grows. To account for this, devices increasingly feature *hardware roots of
trust (RoTs)* which are small, trusted execution environments that safeguard
sensitive data for the machine. RoTs also appear in mobile devices like laptops
or cell phones, and in more conventional devices like desktop PCs.

Google's data center machines feature custom, Google-designed hardware roots of
trust integrated into each machine's deepest layers, known as
[Titan](https://cloud.google.com/docs/security/titan-hardware-chip).
We use Titan, along with a mechanism called *cryptographic sealing*, to ensure
that each machine is running the configuration and software versions we expect.

Cryptographic sealing is a service offered by Titan that is used to safeguard
secrets. Titan's sealing capabilities are similar to those found in the
[Trusted Platform Module (TPM)](https://en.wikipedia.org/wiki/Trusted_Platform_Module)
specification, which is published by the
[Trusted Computing Group](https://trustedcomputinggroup.org/).
Titan's cryptographic sealing has an additional advantage, in that Titan brings a better
ability to measure and attest to low-level firmware.

Cryptographic sealing comprises the following two controls:

- Encryption of sensitive data
- A policy that must be satisfied before the data can be decrypted

### Sealed credentials

Google's credential infrastructure uses cryptographic sealing to encrypt
machine credentials at rest with a key that is controlled by the machine's
hardware root of trust. The encrypted credential private key, and the
corresponding certificate, is known as a *sealed credential*. In addition to
machine credentials, Google uses this sealing mechanism to protect other pieces
of sensitive data as well.

Each machine can decrypt and access its machine credential only if it can
satisfy a decryption policy that specifies what software the machine must have
booted. For example, sealing a machine's credential to a policy that specifies
the intended release of the operating system kernel helps ensure that the machine
can't participate in its machine cluster unless it booted the intended kernel
version.

The decryption policy is enforced through a process called
[measured boot](#measured-boot-process).
Every layer in the boot stack measures the next layer, and the machine attests
to this chain of measurements at the end of the boot. This measurement is often
a cryptographic hash.

## Credential sealing process

This section describes the credential sealing and measured boot process used by
Google machines. The following diagram illustrates this flow.

![The credential sealing flow.](https://cloud.google.com/static/docs/security/images/boot-attestation-credential-sealing.svg)

To seal a machine's credentials to a particular boot policy, the following
steps happen:

1. Google's machine automation infrastructure initiates a software update
  on the machine. It passes the intended software versions to the credential
  infrastructure.
2. Google's credential infrastructure requests a sealing key from Titan,
  policy-bound such that Titan only uses it if the machine boots into its
  intended software.
3. The credential infrastructure compares the returned key's policy with
  the intent communicated to it by the machine automation infrastructure. If
  the credential infrastructure is satisfied that the policy matches the
  intent, it issues a certified machine credential to the machine.
4. The credential infrastructure encrypts this credential using the sealing
  key that is procured in step 2.
5. The encrypted credential is stored on disk for decryption by Titan on
  subsequent boots.

## Measured boot process

Google machines' boot stack consists of four layers, which are visualized in
the following diagram.

![The four layers of the measured boot process.](https://cloud.google.com/static/docs/security/images/boot-attestation-boot-layers.svg)

The layers are the following:

- **Userspace**: applications like daemons or workloads.
- **System software**: a hypervisor or kernel. The lowest level of
  software that provides an abstraction over hardware features like
  networking, the file system, or virtual memory to the userspace.
- **Boot firmware**: the
  [firmware](https://en.wikipedia.org/wiki/Bootloader)
  that initializes the kernel, such as a BIOS and bootloader.
- **Hardware root of trust**: in Google machines, a Titan chip that
  cryptographically measures the firmware and other low-level CPU services.

Throughout boot, each layer measures the next layer before passing control to
that layer. The machine's sealed credential is only made available to the
operating system if all measurements that are captured during boot conform to
the sealed credential's decryption policy, as specified by Google's credential
infrastructure. Therefore, if the machine can perform operations with its sealed
credentials, that is evidence that the machine satisfied its measured boot
policy. This process is a form of implicit attestation.

If a machine boots software that deviates from the intended state, the machine
cannot decrypt and perform operations with the credentials that it needs to
operate within the fleet. Such machines cannot participate in workload
scheduling until machine management infrastructure triggers automated repair
actions.

## Recovering from vulnerabilities in the kernel

Suppose that a machine is running kernel version A, but security researchers
find that this kernel version has a vulnerability. In these scenarios, Google
patches the vulnerability and rolls out an updated kernel version B to the
fleet.

In addition to patching the vulnerability, Google also issues new machine
credentials to each machine in the fleet. As described in
[Credential sealing process](#credential-sealing-process),
the new machine credentials are bound to a decryption policy that is only
satisfied if kernel version B boots on the machine. Any machine that is not
running its intended kernel cannot decrypt its new machine credentials, as the
boot firmware measurements won't satisfy the machine's boot policy. As part
of this process, the old machine credentials are also revoked.

As a result, these machines are unable to participate in their machine cluster
until their kernel is updated to conform to the control plane's intent. These
controls help ensure that machines running the vulnerable kernel version A
cannot receive jobs or user data until they are upgraded to kernel version B.

## Recovering from vulnerabilities in boot firmware

Suppose that there is a vulnerability in the boot firmware, instead of the
operating system kernel. The same controls described in
[Recovering from vulnerabilities in the kernel](#recovering-vulns-kernel)
help Google recover from such a vulnerability.

Google's Titan chip measures a machine's boot firmware before it runs, so that
Titan can determine whether the boot firmware satisfies the machine credential's
boot policy. Any machine that is not running its intended boot firmware cannot
obtain new machine credentials, and that machine cannot participate in its
machine cluster until its boot firmware conforms to the control plane's
intent.

## Recovering from vulnerabilities in root-of-trust firmware

RoTs are not immune to vulnerabilities, but Google's boot controls enable
recovery from bugs even at this layer of the boot stack, within the RoT's own
mutable code.

Titan's boot stack implements a secure and measured boot flow of its own. When
a Titan chip powers on, its hardware cryptographically measures Titan's
bootloader, which in turn measures Titan's firmware. Similarly to the machine's
kernel and boot firmware, Titan firmware is cryptographically signed with a
version number. Titan's bootloader validates the signature and extracts the
version number of Titan firmware, feeding the version number to Titan's
hardware-based key derivation subsystem.

Titan's hardware subsystem implements a versioned key derivation scheme,
whereby Titan firmware with version *X* can obtain chip-unique keys bound to all
versions less than or equal to X. Titan hardware allows firmware with version X
to access keys that are bound to versions that are less than or equal to X, but
that are not greater than X. All secrets sealed to Titan, including the machine
credential, are encrypted using a versioned key.

Attestation and sealing keys are unique to each Titan chip. Unique keys let
Google trust only those Titan chips that are expected to be running within a
Google data center.

The following diagram shows Titan with version keys. The Version X+1 key cannot
be accessed by version X firmware, but all keys older than that are
accessible.

![Titan versions.](https://cloud.google.com/static/docs/security/images/boot-attestation-titan-versions.svg)

In the event of a severe vulnerability in Titan firmware, Google rolls out a
patch with a greater version number, then issues new machine credentials that
are bound to the higher Titan firmware version. Any older, vulnerable Titan
firmware is unable to decrypt these new credentials. Therefore, if a machine
performs operations with its new credentials in production, Google can assert
with confidence that the machine's Titan chip booted up-to-date Titan
firmware.

## Ensuring root of trust authenticity

The controls described in this document all rest on the functionality of the
hardware RoT itself. Google's credential infrastructure relies on signatures
emitted by these RoTs to know whether the machine is running intended software.

It is critical, therefore, that the credential infrastructure can determine
whether a hardware RoT is authentic and whether the RoT is running up-to-date
firmware.

When each Titan chip is manufactured, it is programmed with unique entropy.
Titan's low-level boot routine turns that entropy into a device-unique key. A
secure element on the Titan manufacturing line endorses this chip-unique key
such that Google will recognize it as a legitimate Titan chip.

The following diagram illustrates this endorsement process.

![The Titan endorsement process.](https://cloud.google.com/static/docs/security/images/boot-attestation-titan-endorsement.svg)

When in production, Titan uses its device-unique key to endorse any signature
it emits. Titan chips use a flow that is similar to
[Device Identifier Composition Engine (DICE)](https://trustedcomputinggroup.org/accurately-attest-the-integrity-of-devices-with-dice/).
The endorsement includes Titan firmware's version information. This attestation
helps prevent an attacker from impersonating a signature that is emitted by a
Titan chip, and from rolling back to older Titan firmware and impersonating
newer Titan firmware. These controls help Google verify that signatures received
from Titan were emitted by authentic Titan hardware running authentic Titan
firmware.

## Building on boot integrity

This paper described mechanisms for ensuring that machines' application
processors boot intended code. These mechanisms rely on a measured boot flow,
coupled with a hardware root-of-trust chip.

Google's threat model includes attackers who may physically interpose on the
bus between the CPU and RoT, with the goal of improperly obtaining the machine's
decrypted credential. To help minimize this risk, Google is driving development of a
standards-based approach for defeating active interposers, bringing together the
[TPM](https://trustedcomputinggroup.org/wp-content/uploads/2019_TCG_TPM2_BriefOverview_DR02web.pdf)
and
[DPE](https://trustedcomputinggroup.org/wp-content/uploads/TCG-DICE-Protection-Environment-Specification_14february2023-1.pdf)
APIs from Trusted Computing Group and the
[Caliptra](https://chipsalliance.github.io/Caliptra/)
integrated root of trust.

## What's next

- For information about how Google helps ensure the integrity of complex
  disaggregated machines' boot stacks, see
  [Remote attestation of disaggregated machines](https://cloud.google.com/docs/security/remote-attestation).
- For overview information about Google's security infrastructure, see
  [Google infrastructure security design overview](https://cloud.google.com/docs/security/infrastructure/design).
- For more on how Google is contributing Titan security solutions to
  industry standards, see the
  [TPM Attested Boot in Big, Distributed Environments](https://youtu.be/z0Joifl7JS0?t=70)
  talk on the Trusted Computing Group YouTube channel.

   Was this helpful?
