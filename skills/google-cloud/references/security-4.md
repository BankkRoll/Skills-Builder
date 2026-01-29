# Confidential Space security overviewStay organized with collectionsSave and categorize content based on your preferences.

# Confidential Space security overviewStay organized with collectionsSave and categorize content based on your preferences.

> Use Confidential Computing and Confidential Space to encrypt data in use on Google Cloud

# Confidential Space security overviewStay organized with collectionsSave and categorize content based on your preferences.

This document describes Confidential Space's security controls
and how the system is designed to mitigate a wide range of threats.
Confidential Space is designed to let parties share confidential
data (for example, regulated data or personal identifiable information (PII))
with a workload while they retain the confidentiality and ownership of the data.
Confidential Space helps create isolation so that data is only
visible to the workload and the original owners of the data.

You can use Confidential Space for scenarios when you can't
establish trust with the workload operator or between the original parties that
created the confidential data. For example, financial institutions can use
Confidential Space to collaborate with each other to identify
fraud or analyze money laundering activities. Confidential Space
permits analysis across customer data sets, while keeping customer identities
private.

## Components of a Confidential Space system

Confidential Space uses a
[trusted execution environment (TEE)](https://en.wikipedia.org/wiki/Trusted_execution_environment)
that is designed to release secrets only to authorized workloads. An attestation
process and hardened OS image help protect the workload and the data that the
workload processes from an untrusted operator.

A Confidential Space system has three core components:

- **A workload:** a containerized image with a hardened OS that runs in a
  cloud-based TEE. You use
  [Confidential Computing](https://cloud.google.com/confidential-computing)
  as the TEE that offers hardware isolation and remote attestation
  capabilities.
- **Google Cloud Attestation:**
  an OpenID Connect (OIDC) token provider. You use this service to verify the
  attestation quotes for TEE and release authentication tokens. The tokens
  contain identification attributes for the workload.
- **A protected resource:** a managed cloud resource such as a Cloud Key Management Service
  key or Cloud Storage bucket. The resource is protected by an allow policy
  that grants access to authorized
  [federated identity tokens](https://cloud.google.com/iam/docs/workload-identity-federation).
  An intermediate step, using workload identity pools, transforms the OIDC
  tokens to federated identity tokens that IAM can consume.

The system helps ensure that access to protected resources is granted only to
authorized workloads. Furthermore, Confidential Space helps
protect the workload from inspection and tampering, before and after
attestation.

In a Confidential Space system, there are three parties:

- **The workload author**, who creates a containerized image that includes an
  application that has access to the protected resources. The author doesn't
  have access to the data or the results. In addition, the author doesn't
  control access to the data or the results.
- **The workload operator**, who runs the workload in a Google Cloud project. The
  operator typically has full administrative privileges to the project. The
  operator can manage Google Cloud resources such as Compute Engine
  instances, disks, and networking rules, and the operator can interact with
  any Google Cloud API that acts on them. The operator doesn't have access to
  the data or the results, and can't influence or modify the code or execution
  environment. In addition, the operator doesn't control access to the data or
  the results.
- **The resource owners** (or data collaborators), who own the protected
  resource. A resource owner can access their own data, set permissions on
  their own data, and access the results. They can't access the data from
  other resource owners or modify the code by themselves.

Confidential Space supports a trust model where the workload
author, workload operator, and resource owners are separate, mutually
distrusting parties.

The following diagram shows the system components and parties. The workload is
located in a separate project from the protected resource.

![Confidential Space system and components.](https://cloud.google.com/static/docs/security/images/confidential-space-components.svg)

## Examples of secure data processing

Confidential Space helps you to preserve a user's privacy while
sharing data. The following table describes three example use cases.

| Use case | Example scenario |
| --- | --- |
| Functional encryption model | In a functional encryption model, Alice wants to share the result of
her confidential data with Bob, without revealing her entire dataset. Alice
encrypts her dataset, and protects the data encryption key (DEK) in
Cloud KMS in her project. Alice writes a program that implements the
workload, and shares the binary with Bob. Alice configures KMS to give the
program access to the DEK. The workload runs in Bob's
Confidential Space, decrypts and processes Alice's dataset, and
writes the result to Bob's
Cloud Storage. |
| Multi-party computation | In multi-party computation, Alice and Bob want to share the result
with each other, while preserving the confidentiality of input
datasets. Similar to the functional encryption model, Alice and Bob
encrypt their respective datasets, and protect the DEKs in the
Cloud KMS instances in their projects. They co-author a
program that determines the results, and run it in a
Confidential Space. Alice and Bob configure KMS to give the
program access to the DEKs. The program reads and processes
both datasets, and writes the result to a shared
Cloud Storage bucket. |
| Key shares | A more complex scheme uses the idea ofkey shares. A key
share is a private key that is split across Alice, Bob, and other owners such
that knowledge of individual shares doesn't give access to the
encrypted dataset. In this scheme, trust is split across multiple
owners. The private key is assembled only in a restricted TEE, by an
authorized workload. |

In these examples, only the workload has access to the encrypted dataset and can
process it. Confidential Space helps ensure that no one can carry
out unaudited operations on data that they don't own. Data owners control how
their data is used, and which workloads are authorized to act on it.

## Protecting the integrity and confidentiality of a workload

To help protect the workload from an untrusted workload operator,
Confidential Space implements the following security controls:

- An [attestation process](#attestation-process) detects modifications to the
  workload image or its TEE. This control helps protect the workload's
  integrity pre-attestation.
- A [hardened base image](#hardened-image) helps reduce the attack surface,
  and helps prevent the workload operator from accessing or compromising the
  instance at runtime. This control helps protect a workload's integrity and
  confidentiality post-attestation. Together, these security controls help
  protect the workload, its secrets, and the data it processes.

### Attestation process

The attestation process is based on
[Shielded VM](https://cloud.google.com/security/products/shielded-vm)
measured boot and extended runtime measurements. This process captures boot
sequence measurements in a protected, extend-only register in the virtual
Trusted Platform Module (vTPM) device.

Measurements cover early boot components, the loaded kernel, and the container
image. Furthermore, they include environment properties such as a flag that
indicates the instance is a
[Confidential VM](https://cloud.google.com/confidential-computing).
The vTPM signs (or quotes) these measurements using a certified attestation key
that is trusted by Google Cloud Attestation.

The following diagram shows the components of a
Confidential Space system and how each component participates in
the attestation process.

![The system components and parties in the attestation process.](https://cloud.google.com/static/docs/security/images/confidential-space-attestation-process.svg)

The attestation process depends on the following components:

- **Guest firmware:** an immutable component that is a trusted part of
  Google Cloud.
- **Attested Confidential Space image:** a hardened image based on
  [Container-Optimized OS](https://cloud.google.com/container-optimized-os/docs)
  that is read from the attached boot disk.
- **Early boot components:** bootloaders and kernels that interact with the
  vTPM to measure the boot components into a Platform Configuration Register
  (PCR).
- **Launcher:**
  a component that downloads the workload binary from the image repository and
  measures the container and its configuration into a PCR. The launcher reads
  its configuration from the instance
  [metadata server](https://cloud.google.com/compute/docs/metadata/querying-metadata).
- **Attestation handling code:** code that is responsible for preparing a PCR
  quote, and returning the vTPM's quote, attestation key, and the full
  eventlog.
- **Google Cloud Attestation:**
  a service that verifies the quote, replays the event log, issues the OIDC
  token, and returns the token with the attributes for the workload access
  policy.

### Hardened image

The Confidential Space image is a minimal, single-purpose OS. The
image runs the container launcher, which in turn launches a single container.
The Confidential Space image builds on the
[existing security](https://cloud.google.com/container-optimized-os/docs/concepts/security)
enhancements of Container-Optimized OS, and adds the following
benefits:

- **Encrypted disk partitions with integrity protection:** the
  Confidential Space image includes the following partitions:
  - A `root-fs` partition and an OEM partition that includes the launcher
    binary. These partitions are immutable and protected by
    [dm-verity](https://gitlab.com/cryptsetup/cryptsetup/-/wikis/DMVerity).
  - A temporary writable partition that stores the downloaded workload
    binary.
    [dm-crypt](https://gitlab.com/cryptsetup/cryptsetup/-/wikis/DMcrypt)
    encrypts this partition and protects its integrity.
  - A `tmp-fs` partition that maps to RAM. In a
    Confidential VM TEE, the VM's memory is encrypted. Also,
    the `swap-fs` system is disabled, which helps prevent a misconfigured
    operating system from storing data to disk.
- **Authenticated, encrypted network connections:** the launcher uses TLS to
  authenticate Google Cloud Attestation, and protect its communication links.
- **Various boot measurements:** these measurements include kernel
  command-line arguments, `dm-verity` configuration for `root-fs`, and the
  workload binary.
- **Disabled remote access and cloud-specific tooling:** these tools include
  *sshd* and
  [OS Login](https://cloud.google.com/compute/docs/oslogin).
- **Reduced state transitions:** for example, the launcher runs a single
  container and then terminates.

## Threat model and mitigations

This section describes the threat models that Confidential Space
helps to mitigate, and the new risks introduced by
Confidential Space.

The following attacks are outside of the
scope of this document:

- Software supply chain attacks that apply to guest Unified Extensible
  Firmware Interface (UEFI) firmware, the Confidential Space
  image bootloader and kernel, the container runtime, and third-party
  dependencies for the workload. Data collaborators assume that resource
  owners have reviewed and audited the container image before the resource
  owners share their resource with an allow policy.
- Attacks on Google Cloud, such as VM escapes.

### Possible attacks

Confidential Space is designed to defend against three possible
attacks:

- **A malicious workload operator:** a malicious workload operator can modify
  disk contents, intercept network connections, and attempt to compromise the
  TEE at runtime. A malicious operator can expand the attack surface or
  restrict the runtime environment. For example, a malicious operator can add
  a serial console to introduce new attack vectors. As another example, a
  malicious operator can constrain resources such as limiting a guest's memory
  size, changing its disk space, or changing firewall rules. These constraints
  might trigger I/O errors that could lead to poorly tested error cases.
- **A malicious attestation client:** this attacker connects to
  Google Cloud Attestation and sends malformed yet signed event log messages.
- **A malicious resource owner:** a malicious resource owner has full control
  over the encrypted dataset that the workload consumes. This attacker might
  present malformed inputs or skewed data, and attempt to trigger parsing
  vulnerabilities in the workload or attempt to circumvent its privacy
  controls.

### Attack surfaces

The following table describes the attack surfaces that are available to
attackers.

| Attacker | Target | Attack surface | Risks |
| --- | --- | --- | --- |
| Workload operator | TEE, Workload | Disk reads | Anything read from the disk is within the attacker's control.Services
such asmulti-writerpersistent disks and dynamic disk attachments mean that an attacker can modify
disk contents dynamically and at will. |
| Workload operator | TEE, Workload | Disk writes | Anything written to disk is visible to an attacker. Seedisk snapshotsandimportcapabilities. |
| Workload operator | TEE, Workload | Metadata server | Instance attributes read from the metadata server are within the
attacker's control, including startup script and environment
variables. |
| Workload operator | TEE, Workload | Network | External network connections to the image repository or
Google Cloud Attestation can be intercepted. This attack is done using a
private VPC with a public-facingCloud Routerinstance. |
| Attestation client | Google Cloud Attestation | Event log and attestation messages | Google Cloud Attestation has complex, crypto-heavy logic that is challenging to
write defensively. |
| Resource owner | Workload | Encrypted dataset | An attacker can poison the workload's input datasets, which means that encrypted
data isn't necessarily trusted data. |

### Google Cloud infrastructure

Google Cloud includes the Compute Engine hypervisor, the vTPM for
the Confidential VM, guest UEFI firmware, and a hosted
Google Cloud Attestation instance. Sensitive key material such as vTPM and OIDC
signing keys
are designed to be securely protected.

Google infrastructure is designed to logically isolate each customer's data from
the data of other customers and users, even when it's stored on the same
physical server. Administrative access for support personnel and engineers is
[limited](https://cloud.google.com/docs/security/overview/whitepaper#administrative_access_for_google_employees),
audited, and
[transparent](https://cloud.google.com/access-transparency)
to customers. In addition, inline memory encryption in
Confidential VMs helps protect the confidentiality of the
instance memory. Inline memory encryption renders direct inspection or
accidental memory logging (kernel crash log) ineffective. For additional
information on how we protect our platform, see the
[Google security overview](https://cloud.google.com/docs/security/overview/whitepaper).

### Threats and mitigations

An encrypted file system with integrity protection is designed to mitigate risks
from disk attacks. Furthermore, after code is read from disk, it's measured and
that data is never re-read from disk again. Secrets are never disclosed in
plaintext form to the disk or to any external device such as a serial console.

Risks from network attacks are mitigated by having authenticated, end-to-end
encrypted channels. External network access, such as SSH, is disabled in the
image. An attestation protocol helps protect the boot sequence and any
configuration read from the metadata server. Finally,
Confidential Space workloads are expected to use differential
privacy controls to mitigate risks from skewed datasets.

The following tables describe the threats and mitigations:

- [Attacks on the measured boot process](#attack-measured-boot)
- [Attacks on the container launcher](#attacks-container-image)
- [Attacks on Google Cloud Attestation](#attacks-attestation-service)
- [Attacks on workloads](#attacks-workloads)

#### Attacks on the measured boot process

This table describes potential threats and mitigation strategies related to the
measured boot process.

| Threat | Mitigation | Mitigation implementation |
| --- | --- | --- |
| An attacker boots a Shielded VM with old firmware that
doesn't support measured boot.If successful, an attacker may play back arbitrary
measurements and defeat remote attestation. | This threat is mitigated by the Google Cloud control
plane.Confidential Space adds a vTPM device and
up-to-date UEFI firmware. Also, Confidential Space
enables measured boot, and measured boot cannot be disabled. | Within Google Cloud infrastructure |
| An attacker overwrites UEFI firmware in guest physical memory,
reboots the guest which resets the vTPM registers, and executes
modified firmware.If successful, an attacker may play back arbitrary
measurements, and defeat remote attestation. | This threat is mitigated by the hypervisor. On guest reboot, the
hypervisor loads a clean copy of the UEFI firmware to guest memory.
Previous modifications in guest memory are discarded. Furthermore,
guest reboot is the only event that resets the vTPM. | Within Google Cloud and by you enabling
Confidential Computing |
| An attacker modifies unmeasured configuration files, which
negatively affects program execution. | This threat is mitigated by the attestation process. All
executable binaries and respective configuration files are fully
measured before running.In particular, secure-boot variables, grub configuration, and
kernel command-line arguments are measured.Thesecurity
reviewfound that no measurements were missed in the attestation
process. | Within the Confidential Space image |
| An attacker triggers memory corruption vulnerabilities in early
boot components, and gains code execution. | Early boot components are written in the C language. These
components process untrusted user data, and might be vulnerable to
memory corruption issues. For a recent example, seeBootHole.This risk is mitigated by the attestation process: early boot
components must measure any user-controlled data before processing
it. A BootHole attack uses a modifiedgrub.cfgto gain
code execution and defeat secure-boot.However, in a Confidential Space system, that
attack fails to pass attestation, asgrub.cfgmeasurements don't match the expected configuration.A related risk comes from complex file system logic. Past
vulnerabilities such asSequoiademonstrate that file system drivers process complex data structures,
and can be vulnerable to memory corruption issues.This risk is
mitigated using block leveldm-verityanddm-cryptintegrity
protection, and by disabling auto-mounts. | Within the Confidential Space image |
| An attacker modifies early boot binaries on disk after they're
read and measured, before they're read and executed (diskTOCTOU). | Early boot components were built for bare metal machines, and
might not expect the cloud's dynamic environment. Boot components
might assume that disk contents cannot change during execution, which
is an incorrect assumption for cloud environments.This risk is mitigated by using defensive programming: disk contents are
read-only after using the read, measure, execute pattern.Thesecurity
reviewfor the Confidential Space image didn't identify
TOCTOU issues in the early boot components
such as UEFI,Shim, orGNU GRUB. | Within the Confidential Space image |
| An attacker modifies device drivers and user mode services on
disk after the kernel is loaded. | This threat is mitigated by a root file system with integrity
protection.Root-fsin the Confidential Space image is
integrity protected bydm-verity. The configuration (root-hash) is
passed in a kernel command argument, and then measured and attested
by Google Cloud Attestation. | Within the Confidential Space image |

#### Attacks on the container launcher

This table describes potential threats and mitigation strategies related to the
launcher.

| Threat | Mitigation | Mitigation implementation |
| --- | --- | --- |
| An attacker intercepts the network connection of the launcher or
image repository. | The connection to the image repository is protected by an
authenticated, encrypted TLS connection.An attacker can change the image URL and control the
workload binary. However these actions are reflected in the
attestation log.The image repository is not controlled using an access
list, therefore the image is assumed to be viewable by everyone. You
must ensure that the workload container image doesn't contain any
secrets. | Within the Confidential Space image |
| An attacker modifies the workload image on disk after it was
downloaded and measured. | This threat is mitigated by a writable partition that is
encrypted and its integrity is protected.The workload image and its temporary data are protected bydm-cryptusing ephemeral, per-boot keys.Thedm-cryptdisk encryption process does allow for rollback
attacks, where an attacker replaces disk contents with previously
seen ciphertexts and tags. These attacks are considered to be highly
complex in Confidential Space settings. | Within the Confidential Space image |
| An attacker modifies the launcher configuration in the metadata
server, and controls the image repository URL. | The attestation process detects unsafe configurations that load
non-authentic images. | Within Google Cloud Attestation |

#### Attacks on Google Cloud Attestation

This table describes potential threats and mitigation strategies to
Google Cloud Attestation.

| Threat | Mitigation | Mitigation implementation |
| --- | --- | --- |
| An attacker intercepts the network connection for the launcher
or Google Cloud Attestation and reads the secret token from the wire. | This threat is mitigated by having an authenticated, encrypted
TLS connection. This connection helps protect the token from passive
eavesdropping.An attacker cannot impersonate the service because they are
missing the TLS key. Even if successful, the attacker cannot create
valid OIDC tokens.An attacker cannot impersonate a valid client because the
client identity is guaranteed by the attestation protocol. | Within the network between your workload and the attestation
service. |
| An attacker exploits parsing discrepancies, which leads to
undetected changes in the attestation process. | This threat can occur because the measurements event log is
serialized and sent to Google Cloud Attestation, where it's parsed and
processed.A parsing discrepancy happens when the service and the runtime
OS don't agree on the semantics of the log.For example, if thecmdlinefield has a list of
arguments separated by a comma, then a string likea=1, b=2
c='3,d=e'(note the,din the value substring)
might be parsed differently by the kernel and the service.This risk is mitigated by having a parsing engine that correctly
reflects the OS behavior. In particular, thecmdlineis
processed as a whole string, and isn't broken up to key-value
pairs. | Within the Confidential Space image |
| An attacker uses all service resources, which brings the service
down in a denial of service (DoS) attack. The service is interrupted
for other Confidential Space users. | This reliability risk is mitigated by having a distributed,
elastic service that can be easily replicated and scaled out as
needed.Code prevents resource exhaustion by malicious
clients. | Within the workload |

#### Attacks on workloads

This table describes potential threats and mitigation strategies related to
workloads.

| Threat | Mitigation | Mitigation implementation |
| --- | --- | --- |
| An attacker reads runtime secrets from the writable
partition. | This threat is mitigated with an encrypted file system. The
writable file system is mounted usingdm-crypt. Swap is disabled,
and memory contents are not paged to
disk.As a defense-in-depth technique, OIDC tokens are scoped and
short-lived. | Within the Confidential Space image |
| An attacker reads runtime secrets from theserial console. | This threat is mitigated in the
Confidential Space image because credentials and
tokens are never printed to the serial console. Furthermore, cloud
logging is disabled. | Within the Confidential Space image |
| An attacker updates authorized SSH keys using theOSLoginpackage, and then connects
to the running instance. | This threat is mitigated in the
Confidential Space image because the defaultsystemdservices are masked, includingsshd. | Within the Confidential Space image |
| An attacker updates startup scripts in the metadata server,
which are automatically loaded by theguest
agent. | This threat is mitigated in the
Confidential Space image because the guest agent
package is disabled. | Within the Confidential Space image |
| An attacker pushes bad packages to the VM using theOS configagent. | This threat is mitigated in the
Confidential Space image because the OS config agent
is disabled. | Within the Confidential Space image |
| An attacker passes a malformed and encrypted dataset to the
workload. | This threat is mitigated by having defensive parsing code in the
workload. | Within the workload |
| An attacker passes a skewed or poisoned dataset to the workload
and attempts to learn information about the datasets from other
parties. | This threat is mitigated by implementing differential privacy
controls in the workload. | Within the workload |

## Security tests

Confidential Space went through a comprehensive security review
process at Google. This security review process included the following tests and
audits:

- **Negative flow end-to-end integration tests**
  These tests verified that
  attestation fails on bad measurements, such as when the code runs in an
  unexpected TEE environment or launches a modified workload container.
- **Manual audit of measured boot process**
  This review focused on
  identifying missing measurements and double-read bugs. Tests verified that
  code was written with security best practices in mind, and, when there was a
  failure, the code closed (shut down).
- **Manual audit of the build process for the
  Confidential Space image and launcher logic:**
  This review focused on package removal and attack surface
  reduction.
- **Manual audit of Google Cloud Attestation**
  This review focused on the
  implementation of the correct attestation protocol, and avoiding parsing
  issues.
- **Cryptography review by cyber-security experts**
  This review focused on
  the attestation protocol, file system encryption, and integrity solutions.
- **Privacy review by privacy experts**
  This review focused on the
  differential privacy controls in workloads that were authored by Google.
- **Continuous fuzz tests**
  These tests covered security critical components such
  as the vTPM and Google Cloud Attestation.

[NCC Group](https://www.nccgroup.com/),
an external pentesting organization, performed penetration tests on the system.
NCC [reviewed Confidential Space](https://www.nccgroup.com/research-blog/public-report-google-confidential-space-security-assessment/) as a secure
compute platform.

## What's next

- To get started with Confidential Space, see [Analyzing
  confidential data with
  Confidential Space](https://cloud.google.com/confidential-computing/confidential-vm/docs/analyze-with-confidential-space).
- To learn more about protecting data in use, see
  [Confidential Computing](https://cloud.google.com/confidential-computing).
- To learn more about Google infrastructure security, see
  [Google infrastructure security design overview](https://cloud.google.com/docs/security/infrastructure/design).

   Was this helpful?
