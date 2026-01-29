# Titanium hardware security architecture at GoogleStay organized with collectionsSave and categorize content based on your preferences.

# Titanium hardware security architecture at GoogleStay organized with collectionsSave and categorize content based on your preferences.

> Discover how Google infrastructure uses moonrise-replace357c9e1be20048f4bc3009beef375fffmoonrise-replace components to enhance security.

# Titanium hardware security architecture at GoogleStay organized with collectionsSave and categorize content based on your preferences.

*This content was last updated in September 2024, and represents the status quo
as of the time it was written. Google's security policies and systems may change
going forward, as we continually improve protection for our customers*.

Titanium hardware security architecture serves as the foundation for Google's
services and underpins many of the security countermeasures in Google
infrastructure. Titanium hardware includes security microcontrollers, hardware
adaptors, and offload processors that were developed specifically to address
specific attack vectors for Google infrastructure.

[Titanium hardware](https://cloud.google.com/titanium) is the latest advancement
to Google's ever-evolving and comprehensive infrastructure security and helps
protect the integrity, confidentiality, and availability of user data. Titanium
hardware builds on infrastructure such as [cryptographic hardware offload
cards](https://cloud.google.com/blog/products/identity-security/announcing-psp-security-protocol-is-now-open-source)
that provide encryption-in-transit and internal microservices that provide
[data-at-rest
encryption](https://cloud.google.com/docs/security/infrastructure/design#encryption_at_rest).

This document describes how Titanium hardware components work together to create
a security architecture that helps protect the physical attack surface of Google
systems and mitigate threats to customer data. This document also describes how
Titanium hardware enables specific security controls at the software layer, the
evolution of the architecture beyond initial cryptographic hardware offloads,
and the real-world threats that the Titanium hardware security architecture is
designed to mitigate across Google's customer and deployment base.

## Titanium hardware security architecture

The Titanium hardware security architecture is designed to defend against a
spectrum of scenarios and threat actors. The following architecture diagram
shows Titanium's independent, yet interlocking, components.

![Titanium architecture components](https://cloud.google.com/static/docs/security/images/titanium-architecture.svg)

The Titanium hardware security architecture includes the following components:

- [Caliptra root of trust for measurement
  (RTM)](https://www.opencompute.org/documents/caliptra-silicon-rot-services-09012022-pdf):
  helps enforce a security perimeter for each silicon package. Caliptra RTM
  provides attestation and a unique ID to root cryptographic services.
- [Titan chip
  RoT](https://cloud.google.com/docs/security/titan-hardware-chip):
  interposes between a platform's boot flash and its main boot devices such as
  the baseboard management controller (BMC), the platform controller hub (PCH),
  and the CPU. Titan chips provide a physically tamper-resistant hardware-based
  RoT that helps establish a strong identity. Titan chips also help with code
  authorization and revocation for machines, cards, or peripherals.
- [Titanium offload processor
  (TOPS)](https://cloud.google.com/titanium): provides
  cryptographic controls to help protect the confidentiality and integrity of
  data at rest and data in transit.
- **Custom motherboards**: provide resiliency at scale against DoS attacks from
  faulty or malicious software, as well as protection against physical attacks.
  In the diagram, for example, the chip package and Titan RoT are on a custom
  motherboard that is separate from the custom motherboards for Titanium TOP or
  the motherboards for other infrastructure.
- [Confidential Computing
  enclaves](https://cloud.google.com/security/products/confidential-computing):
  help enforce isolation against Google's [administrative
  privileges](https://cloud.google.com/docs/security/production-services-protection),
  improve isolation with other tenants, and add verifiability using attestation.
  Attestation can give assurance that the environment has not been altered.
- **Backend fault-tolerant regionalized services**: help prevent escalation of
  privilege across services, zones, or from administrative access.

In the diagram, *Other infrastructure* refers to network fabrics and replicated
backend storage.

## Design principles of Titanium hardware security architecture

Our Titanium hardware components and their interactions are developed using the
following fundamental principles:

- **No single point of failure**: Google architecture is designed to avoid
  single points of failure, such as single load-bearing components with multiple
  responsibilities. [Building Secure and Reliable
  Systems](https://sre.google/books/) discusses the importance of avoiding
  single points of failure. This principle is applied throughout our physical
  infrastructure, across all regions, and even down to the silicon in chips.
  This resiliency throughout our global infrastructure helps keep customer data
  safe and available.
  For example, [live migration](https://cloud.google.com/compute/docs/instances/live-migration-process)
  with Confidential Computing helps to preserve the encrypted memory on supported
  host machines. Live migration helps to ensure that a long-running VM is not a
  single point of failure due to maintenance events or [responding to
  vulnerabilities](https://cloud.google.com/blog/products/identity-security/google-researchers-discover-reptar-a-new-cpu-vulnerability).
- **The perimeter is the silicon package**: because a server system contains
  multiple interconnected and separate system-on-chips, our architecture
  fundamentally distrusts all connectors, fabrics, printed circuit board
  assemblies (PCBAs), PCBA traces, and cables. Though component separation is
  useful for modularity, separation can also become a weakness when it offers
  adversaries well-defined targets from which to snoop plaintext data. Data
  within the silicon package itself is encrypted and authenticated by private
  cryptographic assets within the package.
  Moving the perimeter into the silicon itself helps minimize implicit trust.
  This principle addresses threats against data confidentiality that occur as
  data center serving conditions become increasingly diverse. For example,
  setting the perimeter into the silicon package helps address threats from
  rogue hardware operations.
- **Zero trust and compartmentalizing risk**: multi-party controls on
  administrative actions help ensure that no personnel account (or compromised
  personnel account) can unilaterally cause the threats that are discussed in
  this paper. The architecture separates services into layers and zones to
  compartmentalize and contain risk. Even with enclaves, which are typically
  hardware rooted, the architecture accounts for the discovery of hardware
  vulnerabilities and the need to remediate while components remain in
  operation.
  For example, if an attacker maliciously compromises a chip's behavior inside
  an active system that is running customer workloads in our data centers, the
  architecture is designed to identify and isolate that compromised chip. That
  machine can then be taken out of service. Even if the machine isn't taken out
  of service, the attacker must defeat additional trust boundaries and
  compromise multiple credentials to move laterally and gain influence over
  further systems, users, or regions.
  Independent failure domains and isolation technologies help limit the affected
  area of a compromise. These domains and technologies add natural control
  points for detection, and limit the amount of additional complexity that must
  be introduced.
  For more information about our zero-trust implementation, see
  [BeyondProd](https://cloud.google.com/docs/security/beyondprod).
- **Transparent security**: Google invests in multiple transparency efforts,
  including open sourcing, responsible disclosure of research and findings, and
  partnering with the ecosystem of hardware manufacturers. Google global
  infrastructure applies [Kerckhoffs'
  principle](https://en.wikipedia.org/wiki/Kerckhoffs%27s_principle), which
  states that a cryptosystem should be secure, even if everything about the
  system, except the key, is public knowledge.
  For example, we contribute to open source projects and use these projects in
  our security hardware designs and our security software. The following table
  describes some of the open source projects that we contribute to and use.
  | Open source project | Description | Titanium component |
  | --- | --- | --- |
  | BoringSSL | Used inFIPS
  140-3 level 1encryption libraries | BoringSSL |
  | Caliptra | Used in roots of trust (RoT) at the silicon level | Caliptra RTM |
  | OpenTitan | Used in RoT for a chip in a system architecture | Titan chips |
  | Syzkaller | Used for coverage-guided kernel fuzzing | Host ring0 and User VM Distros |
  | PSP | Used inFIPS
  140-3 level 1encryption libraries | Titanium Offload Processor |
- **Physical and logical defense in depth**: Google relies on [physical data
  center security](https://www.google.com/about/datacenters/data-security/) to
  help protect our capital investments and our systems. These security controls
  are an initial layer of defense, so we deliberately invest in additional
  *logical* controls to harden our systems against physical threats. Titanium
  adds to our defense in depth by adding compartmentalization in our hardware
  that provides additional defenses against [specific infrastructure
  threats](#infrastructure-threats).
  For example, our data centers have metal detectors that can accurately detect
  storage media exfiltration attempts. However, our data-at-rest encryption
  strategy is deliberately engineered not to rely on physical media custody.
  These logical and physical controls are independent and complementary layers.
  Our combined physical and logical security controls help us stay vigilant
  against insider threats and help protect the confidentiality of our users'
  data.

## Security benefits of Titanium architectural components

The following table highlights some important security benefits that are
achieved with the Titanium security architecture components, both at the
hardware and software layer. These security benefits are described in more
detail in the following sections.

| Security benefits | Architecture component |
| --- | --- |
| Silicon-level trust perimeter on system-on-chips (SoCs) such as CPUs or
GPUs | Caliptra RTM |
| Silicon-level verifiability | Caliptra RTM |
| Cryptographic identity at the hardware level | Caliptra RTM, Titan RoT |
| Verification that the expected binaries are running | Caliptra RTM, Titan RoT |
| Persistent threats mitigation across boots | Caliptra RTM, Titan RoT |
| Protection of the confidentiality of data at rest and data in
transit | TOPs for cryptography |
| Offloading processor-level protection (beyond a physical card) | TOPs for cryptography |
| Security by design, resistance to physical attacks, and resilience
capabilities supporting full system firmware recovery from a single Titan
RoT | Custom motherboards |
| Purpose-built boards with only essential connectors, which helps mitigate
against physical tampering attempts | Custom motherboards |
| Cryptographic workload isolation from machine-wide system software and
administrative human access | Confidential Computing enclaves |
| Tamper resistance through DRAM encryption (to enable data-in-use encryption) | Confidential Computing enclaves |
| Minimized affected area and bulkhead for an attacker with local
access | Backend fault-tolerant regionalized services |
| Multi-levels of compartmentalization | Backend fault-tolerant regionalized services |

### Caliptra root of trust for measurement

[Caliptra
RTM](https://cloud.google.com/blog/topics/systems/google-security-innovation-at-the-ocp-regional-summit)
helps build trust and transparency for the firmware within our ecosystem that
runs on system-on-chips (SoCs) such as CPUs, GPUs, and TPUs.

Caliptra RTM has the following benefits:

- **Provides a root cryptographic service**: Caliptra RTM helps detect corrupted
  critical code and configuration through strong end-to-end cryptographic
  integrity verification. Caliptra RTM can cryptographically measure its code
  and configuration, sign these measurements with a unique and
  hardware-protected attestation key, and report measurements that attest to the
  authenticity and integrity of the device. Caliptra RTM provides a
  cryptographic device identity and a set of firmware and configuration
  integrity measurements for the motherboard.
- **Mitigates** [physical supply chain
  security](https://www.cisa.gov/sites/default/files/publications/defending_against_software_supply_chain_attacks_508.pdf):
  Caliptra RTM helps ensure that the hardware is authentic and is running
  intended firmware and software. In combination with software supply chain
  security, Caliptra RTM lets the system verify the authenticity and integrity
  of firmware and software, whether created by Google or a third-party. This
  verification process lets Caliptra RTM maintain authenticity and integrity
  across authorized updates and helps ensure that configurations remain as
  intended and are attested.
- **Protects against physical intrusions that require direct access to running
  hardware**: Because Caliptra RTM is built into the chip's silicon layers, a
  PCBA interposer or rogue chip that tries to deliver the wrong firmware to an
  application-specific integrated circuit (ASIC) cannot successfully attack the
  RoT. For example, attackers can bypass an external RoT's detection
  capabilities by tampering with the relatively low-speed SPI bus. However, an
  RoT that is embedded within an SoC or ASIC becomes more difficult for an
  attacker to compromise.

### Titan chip root of trust

Titan is designed to cryptographically maintain device identity, defend against
bad software pushes, and enforce code authenticity using revocation.

A [strong cryptographic device
identity](https://cloud.google.com/docs/security/infrastructure/design#secure_boot_stack_and_machine_identity)
helps ensure that the fleet is composed exclusively of validated machines that
are running the expected binaries and can identify and authenticate legitimate
access. Legitimate access is rooted at the hardware level.

By default, production machines use trusted boot to help ensure that only
authenticated software can run. Trusted boot verifies the digital signature of
all boot components and doesn't permit a machine to participate in the
production environment if authentication fails.

As an additional preventative control, machine code revocation prevents software
changes that are no longer authorized from being applied. The revocation
capability in Titan chips helps mitigate not only malicious attacks (for
example, rollback or replay attacks), but also non-malicious stability or
resilience bugs (for example, by preventing accidental reinstallation of buggy
old firmware).

For more information, see [How Google enforces boot integrity on production
machines](https://cloud.google.com/docs/security/boot-integrity).

### Titanium offload processors for cryptography

Titanium offload processors (TOPs) for cryptography help provide security
during offloading of I/O. These TOPs are protected with Titan or
Caliptra RTM. TOPs deploy widespread authenticated encryption of data in transit
and authenticated encryption of data at rest at low cost. Authenticated
encryption means that customer data has cryptographic assurance of
confidentiality and integrity. Because TOPs manage the cryptography, they
*deprivilege* many system components. TOPs enable enhanced architectural
properties, like availability, while minimizing the potential for loss of data
secrecy.

### Custom motherboards

The custom motherboards in Google infrastructure are designed to provide
[hardware
provenance](https://cloud.google.com/docs/security/infrastructure/design#hardware-design).
The motherboards support attestation at multiple layers. Motherboard designs
safeguard customer data, even in the highly unlikely event that an attacker
physically attaches a malicious device to a machine. Titanium motherboard
designs help enable reliable deployment of additional hardening mechanisms, such
as depopulated debug ports, read-only serial consoles, bus connector intrusion,
and extrusion signaling.

TLS and ALTS are the only accepted protocols exposed by our BMC network stack
when a machine is turned on. For machines that use a third-party COTS design,
such as our X4 instances, TOPs proxy any management traffic that is unique to
that third-party design. Proxying management traffic means that our
infrastructure doesn't depend on third-party designs for authentication,
authorization, transport security, or network security.

Titanium custom motherboards are designed to have built-in recovery and backup
mechanisms to ensure availability and recoverability. They can restore
themselves from most crashes or from firmware corruption. Our latest designs
enable rebuilding the entire machine from a single working Titan RoT. These
motherboards use feature-dedicated power componentry and reset signaling to help
ensure the electrical independence of Titan RoTs from the rest of the platform,
and help protect their control over the platform's firmware payloads for the
purposes of authentication and recovery.

### Confidential Computing enclaves

[Confidential Computing](https://cloud.google.com/confidential-computing/confidential-vm/docs/confidential-vm-overview)
creates a Trusted Execution Environment (TEE) or enclave to help isolate
customer sensitive workloads from Google administrative access. When the data is
handled by the CPU or GPU, Confidential Computing provides a technical
preventative control through compute isolation and in-memory encryption.
Confidential Computing helps ensure that even a malicious hypervisor cannot
access a VM. For customer workloads, Confidential Computing provides a
layer of data secrecy insulation from the possibility of unintended Google
personnel access or faulty automated system-software actions at scale.

One example of advanced security that is enabled by the Titanium architecture is
[Confidential mode for Hyperdisk Balanced](https://cloud.google.com/compute/docs/about-confidential-vm).
Confidential mode for Hyperdisk Balanced combines Titanium-based block storage
offloads, Confidential Computing, and
Cloud HSM to create a hardware-rooted TEE. In other words, Confidential mode
for Hyperdisk Balanced is a hyperdisk-balanced offering. Confidential mode for
Hyperdisk Balance isolates infrastructure so that sensitive keys are exclusively
processed in a hardware-rooted TEE. For information about the third-party review
of the cryptographic operations, see [Public Report – Confidential Mode for
Hyperdisk – DEK Protection
Analysis](https://research.nccgroup.com/2024/04/12/public-report-confidential-mode-for-hyperdisk-dek-protection-analysis/).

### Backend fault-tolerant regionalized services

Backend fault-tolerant regionalized services help minimize the affected area from
an attacker with local access. Google infrastructure is designed to
compartmentalize services, systems, and zones from lateral movement of
privileged insiders or compromised services.

We are working to include [regional
information](https://cloud.google.com/compute/docs/regions-zones) in an
increasingly broad set of our internal identity and access management systems.
Regional information strengthens cryptographic isolation so that an attacker who
obtains local access must compromise multiple credentials from distinct
infrastructure services to continue to move laterally.

If an attack triggers a preventative control that would take a production
machine out of the environment (for example, cause the system to power off), our
fault-tolerant backend infrastructure helps ensure the continued availability of
customer data and services on nearby machines. For more information about our
infrastructure controls, see
[BeyondProd](https://cloud.google.com/docs/security/beyondprod)
and [How Google protects its production
services](https://cloud.google.com/docs/security/production-services-protection).

## Attack vectors for Google Cloud infrastructure

This section describes specific physical and logical threats that make up some
of the attack surface of Google Cloud. The Titanium hardware security
architecture is specifically designed to address a unique set of threats to
Google infrastructure and the user data that we store.

### Infrastructure threats

Titanium architecture is designed to defend against the following multiple
categories of threats:

- **Rogue insider with physical access**: Our personnel need access to physical
  devices in data centers to deploy, maintain, and repair hardware. This access
  represents a potential attack vector because rogue personnel or contractors
  have a legitimate business reason to physically repair some of the machines in
  our data centers.
- **Rogue insider with logical access**: Similar to physical access to the data
  center, personnel are required to develop, maintain, test, debug, tune, and
  support multiple levels of the Google software stack. These personnel include
  developers, SREs, and customer-facing cloud engineers.
  For more information about our defenses against this threat, see [How Google
  protects its production
  services](https://cloud.google.com/docs/security/production-services-protection).
- **External attacker with logical access**: External attackers can gain a
  foothold inside of a Google Cloud environment and attempt to transfer
  laterally to other machines to obtain access to sensitive data. A common
  tactic used by external attackers is to begin by compromising a legitimate
  personnel or contractor account.

The following diagram shows which part of the cloud environment is most
vulnerable to these threats.

![Vulnerabilities to these threats.](https://cloud.google.com/static/docs/security/images/titanium-threat-vulnerability.svg)

### Attack surface to data center servers

The following table describes attack surfaces that are typical aspects of data
center servers. The Titanium hardware security architecture is designed to
provide strong defenses against such threats.

| Attacker | Target | Attack surface | Risk |
| --- | --- | --- | --- |
| Rogue insider with physical access | Storage media (SSDs, HDDs, or boot drives) | Physical drives and connectors | This attack could steal a drive, and attempt to access it with the attacker's
tools. |
| DIMM | Physical memory connectors | This attack could freeze the DIMM, take it out of the data center, and
try to access the data on it using the attacker's own tools. This threat is sometimes
called acold bootattack. |  |
| Server | USB or PCIe connectors | This attack could connect malicious hardware to the server. Using the
malicious hardware, the attacker could attempt to gain code execution or
exfiltrate resident data. |  |
| Motherboard | Joint test access group (JTAG) eXtended Debug Port (XDP) | This attack could connect a hardware debugging tool to gain code
execution or access to data that is processed on the CPU. |  |
| Network | Ethernet cables | This attack could tap an ethernet cable to gain access to all the data
that is being transferred between devices. Any cleartext traffic could then be
observed. |  |
| Motherboard | Firmware | This attack could introduce persistent malicious firmware. This firmware
could be pre-installed from a compromised manufacturer, interdicted in transit,
or updated by an insider. This threat can lead to pre-hacked hardware with
rootkits that provide backdoor access to the server. |  |
| Rogue insider with logical access | Compute workload (for example, VMs) | Login points | This attack could use insider credentials to directly access VMs or
hosts, and the data on them. |
| Fabric router | Physical or administrative access | This attack could gain root control over a fabric router to eavesdrop on
all traffic and exfiltrate or tamper with any cleartext data that is in transit
on the fabric. |  |
| Motherboard | Firmware | This attack could push defective firmware images to motherboards,
making them permanently inoperable and rendering data unrecoverable.An attacker
could push known-vulnerable firmware to machines to regain control using
exploits that enable remote code execution. |  |
| External attacker with logical access | Server | VMs | This attack could launch public side-channel attack patterns on VMs.
These attacks could leak data from instances running on the same hardware, or
from host system software. |
| SSDs | VMs | This attack could use direct access to PCIe SSDs to attempt to infer
co-tenant data. |  |
| Memory | VMs | This attack vector could use side channels to search memory for valuable
encryption keys. |  |
| Server | Bare-metal VMs | This attack vector could use bare-metal instances to scan all peripherals
to find a vulnerable component that would let them persist in the machine and
attack subsequent tenants. |  |

## Mapping Titanium hardware components to threats

The Titanium hardware security architecture uses a multi-layer approach to help
address specific [infrastructure threats](#infrastructure-threats) and to
prevent single points of failure. These threats may originate from mistakes or
from rogue actors. The threats span hardware operations and can exploit
vulnerabilities in servers, networks, and the control plane. No single solution
exists that can address all of these attack vectors, but the combined features
of Titanium help protect our users data and our cloud computing instances.

### Scenario: Rogue hardware operations

Rogue hardware operations pose a threat to data security, as they can lead to
the exfiltration of data from data centers and the modification of hardware and
firmware. Google's Titanium hardware security architecture helps defend against
these threats by using a variety of security measures, including cryptographic
RoTs, custom motherboards, and I/O processors. These components work together to
provide a layered defense that is resistant to a wide range of attacks.

The following table describes some of the rogue hardware threats and how
Titanium architecture can mitigate them.

| Threat | Titanium mitigation |
| --- | --- |
| An attacker exfiltrates individual data drives from the data centers to
access the data on them. | Data-at-rest encryption keysfor storage products and services
are never stored persistently on the machines to which storage media is
attached. The built-in self-encryption capabilities of storage media are also
enabled for defense in depth, and use keys that are never stored persistently on
the media itself.Caliptra RTMslet Google include root-of-trust
hardware identity and firmware integrity among the authorization conditions that
are required to release keys from a key management service to storage service
instances. Machines that are somehow maliciously configured with unintended
firmware can't access the keys that are needed to decrypt stored data. The RoTs
embedded inside the silicon packages anchor the relevant cryptographic
identities within the chip package.Single-function interposersare the main part of our data plane security and encrypt data at every
processing step. TOPs provide the following benefits:Serve as silicon interposers to ensure all NVMe commands that originate from
workloads are sanitized appropriately before the commands reach third-party SSD
media.Include custom Google SSD designs with private cryptographic controllers to
manage keys and perform encryption directly in the hardware data path.Enable cost-effective scale-out storage that is both encrypted and integrity
protected.Proven software solutions like dm-crypt are used for lower-performance drives
where reducing the attack surface is paramount, such as some boot drive use
cases. |
| An attacker taps a network cable and reads bytes on the wire or
fiber. | TOPsencrypt data in transit, which removes the opportunity for a
threat to sniff valuable data on the network.Our NICs use the PSP
hardware offload standard. This standard provides cost-effective encryption with minimal decrease in performance. These implementations are FIPS
compliant.Customer data is encrypted when it transits Top of Rack (ToR)
or fabric switches. Some machine-learning infrastructure uses proprietary transport security mechanisms. |
| An attacker replaces flash chips that hold mutable code in the data
center or the supply chain to run malicious code on the servers. | Titan chipsare designed to reject the attack and don't provide
access to the credentials that are stored inside. Even if an attacker rewrites
the content of non-volatile flash chips, the Titan RoT securely reports a
measurement of the code to Google's control plane, which is designed to block
the device. Google routinely revokes deprecated or known-vulnerable code at
global scale in our fleet by using Titan chips. |
| An attacker inserts adversarial devices in physical interfaces of data
center servers or cards to run malicious code or exfiltrate data. | Custom motherboard designsremove the interfaces that are used
to insert adversarial devices.Input-Output Memory Management Unit
(IOMMU)configurations are in place to prevent PCIe screamers in all of our
firmware. (PCIe screamers are designed to read and write arbitrary packets on the PCIe fabric.) As the industry matures, we are complementing this protection with PCI
IDE to additionally mitigate against more sophisticated PCI
interposers.ALTS and TLSare the only accepted authentication
and authorization network connections for control and management functions on
TOPs and BMCs.Caliptra RTMsblock any non-approved firmware. Our
trusted peripherals attest their hardware identity and code integrity to our
control plane, and no server is admitted to production if the attestation record
does not match the hardware and software intent. |
| An attacker uses a cold boot attack in the data center to access data in
RAM. | Confidential Computing in-memory encryptionprotects any
sensitive data or encryption keys in RAM. DRAM encryption is also enabled in
machines that are deployed without Confidential Computing in lower
assurance edge data centers. |

### Scenario: Exploitation of servers or networks by rogue users

Attackers might use the public cloud to host their malicious workloads on our
shared infrastructure and to deposit data in our public services. External
adversaries, from single individuals to nation states, might also attempt to
gain remote privileged access.

To mitigate these actions, the Titanium hardware security architecture uses
Titan chips and Caliptra RTM to provision runtime credentials in a secure manner
and limit privileges on hardware and operating systems.
Confidential Computing helps protect against manipulation of system memory
– whether physically or using hypervisor attacks – and Titan chips reject or
detect unauthorized software upgrades.

The following table describes some of the server and network exploitation
threats and how Titanium architecture can mitigate them.

| Threat | Titanium mitigation |
| --- | --- |
| An attacker exploits a vulnerability to escape their VM and gains access
to data and other VMs running on the same machine. | Confidential Computing enclavescurtail the exfiltration of
workload data, whether in process or at rest. This mitigation blocks a
VM-escaped attacker from accessing data in use.Titan chips and
Caliptra RTMsblock the attacker from having persistent access. Any
attempts for persistent access are likely to be detected because the machine
configuration won't match the configuration and code policy for that server.
This match is required before the machine can host production workloads after a
reboot. |
| An attacker launches public side-channel attack patterns on VMs. | Our fleet management system, usingTitan chips, can revoke known-vulnerable software. Revocation can block any subsequent attacks that target
these known vulnerabilities. Titan-based integrity measurements also provide
high confidence that mitigations, which might need to be urgently deployed, have
been deployed to the target machines.We reinforce this approach by
remaining at the forefront of side-channel investigation and mitigation, through
techniques like retpoline and core scheduling, and advanced research onMeltdown, Spectre,Zenbleed,Downfall, and others. |
| An attacker uses direct access to SSDs that provide storage to multiple
tenants to attempt to infer co-tenant data. | Data-at-rest encryptionhelps protect against logical and
physical attacks with a variety of interposers. For resources that aren'tshared,
each tenants' data is encrypted using different keys, which mitigates the
opportunity for direct access attacks against the SSD. |
| An attacker scans memory and uses side channels to search for data
encryption keys or credentials. | Titan chipsenable provisioning of per-machine sealed
credentials. Even if an attacker gains root access on one machine, its
credentials are bound solely to the private identity of the local Titan
chip. |
| An attacker purchases bare-metal instances and scans all peripherals to
try to gain persistent access. | Titan chipsreject any unauthorized software upgrade, including
malicious pushes for persistent control. Our machine workflow positively
confirms expected integrity measurements across a full system attested power
cycle between bare-metal customers. |

### Scenario: Exploitation of servers or networks by rogue control plane behavior

Rogue control plane insiders can attempt to exploit Google's systems in a number
of ways, including attempting to gain root control over a fabric router, pushing
defective firmware images to motherboards, and eavesdropping on network traffic.
The Titanium hardware security architecture defends against these threats by
using a variety of mechanisms, including Titan chips, Caliptra RTMs, custom
motherboards, and backend fault-tolerant isolated services.

The following table describes some of the control plane threats and how Titanium
architecture can mitigate them.

| Threat | Titanium mitigation |
| --- | --- |
| An attacker uses insider credentials to access Compute Engine VMs that
are serving as the foundational layer for customer environments. | TOPshelp ensure that administrators don't have access to
customer environments. Without access, Google personnel can't use their
credentials to access the privileged hardware and software layer that is
underneath our customers' VMs. Google insider access to customer data is blocked
because data is only accessible through defined APIs. |
| An attacker pushes defective firmware images at scale to motherboards,
permanently bricking them. | Titan chips RoTsreject any unauthorized software upgrade,
including malicious pushes for persistent control.Custom motherboard
designsuse an alternate network of signals that interconnect all of our
RoTs to the platform RoT. The platform RoT holds backup firmware for critical
devices. Even if networking and PCI were bricked by an attacker, the out-of-band
(OOB) network can heal the system. |
| An attacker pushes deprecated known-vulnerable production firmware to
machines to regain control using public vulnerabilities. | Titan chipsreject bad pushes and help enforce revocation of
known-vulnerable code. They attest the firmware version that is deployed
on the machine and reject the machine at the control plane. This mitigation
helps prevent any jobs from running on an unhealthy machine, and triggers
investigation or repair as necessary. |
| An attacker abuses silicon debugging capabilities that are necessary for
business continuity, which provide the highest conceivable level of data access
in server systems. | Caliptra RTMhelps ensure that all parameters that enable
invasive debug interfaces, whether logically connected or through direct
physical insertion, are trustworthily configured, cryptographically measured,
and reported to our control plane using an attestation protocol. Only machines
in the intended state gain access to serve production workloads. |
| An attacker gains control of one backend service so that they can access
customer environments. | Backend fault-tolerant regionalized servicesare regionalized
credential infrastructure that don't permit unilateral human access. In addition
to preventing operator login onto compute nodes, operators also cannot log in to
the control plane to retrieve key
material.Confidential Computing enclavesin the Titanium
architecture isolate our backend authorization and key provisioning services
from machine root privileges.Key hierarchieshelp protect the
signing and authorization keys of most services. With key hierarchies, the root
keys are in air-gapped keys that are held in HSMs and in safes, or keys that are
held in production by aPaxos quorumof in-memory data stores. |

## What's next

- Read the [Infrastructure security design
  overview](https://cloud.google.com/docs/security/infrastructure/design).
- Implement
  [Confidential Computing](https://cloud.google.com/security/products/confidential-computing).

   Was this helpful?
