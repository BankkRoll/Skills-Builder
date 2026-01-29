# Titan hardware chipStay organized with collectionsSave and categorize content based on your preferences.

# Titan hardware chipStay organized with collectionsSave and categorize content based on your preferences.

> Learn how the Titan hardware chip works in the Titanium hardware security architecture at Google.

# Titan hardware chipStay organized with collectionsSave and categorize content based on your preferences.

*This content was last updated in January 2025, and represents the status quo as
of the time it was written. Google's security policies and systems may change
going forward, as we continually improve protection for our customers*.

The Titan chip is a purpose-built chip that establishes the hardware root of
trust for platforms in Google Cloud data centers. The Titan chip is a low-power
microcontroller that is deployed on platforms such as servers, network
infrastructure, and other data center peripherals.

The Titan chip is an important component of the [Titanium hardware
security
architecture](https://cloud.google.com/docs/security/titanium-hardware-security-architecture),
which provides a foundational security layer that helps protect against physical
attacks and threats to user data. The Titan chip lets Google securely identify
and measure platform firmware and configuration. It is designed to protect
against privileged software attacks and rootkits, from the machine boot process
forward.

This document describes the chip architecture and security benefits of the Titan
chip. The Titan chip supports a minimal trusted computing base (TCB) that lets
the chip provide the following benefits:

- A hardware root of trust that creates a strong identity for a machine
- Integrity verification of platform firmware, both at boot time and update
  time
- [Remote credential
  sealing](https://cloud.google.com/docs/security/boot-integrity#credential-sealing-process)
  flows that underpin Google's machine credential management system

## The Titan chip family

The earliest Titan chips were designed in 2014. Later generations incorporated
the experience that was gained during iterative manufacturing, integration, and
deployment processes. For more information about how Google has contributed our
knowledge about the Titan chip to the open-source hardware security community,
see [opentitan.org](https://opentitan.org).

Titan chips include the following components:

- Secure processor
- AES and SHA cryptographic coprocessor
- Hardware random number generator
- Sophisticated key hierarchy
- Embedded static RAM (SRAM), flash, and ROM

## Titan manufacturing identity

During the Titan chip manufacturing process, each Titan chip generates unique
key material. This key material is certified and used to produce endorsement records.
These endorsement records are stored in one or more registry databases, and are
cryptographically protected using air-gapped and multi-party controls.

When Titan-enabled platforms are integrated into the Google production network,
the backend systems can verify that these platforms are equipped with authentic
Titan chips. Authentic Titan chips are provisioned with keys that were
registered and certified during the Titan manufacturing process. For more
information about how services use the Titan identity system, see [Credential
sealing
process](https://cloud.google.com/docs/security/boot-integrity#credential-sealing-process).

Later-generation Titan chip identities are generated and certified in accordance
with industry standards such as [Device Identifier Composition Engine
(DICE)](https://trustedcomputinggroup.org/what-is-a-device-identifier-composition-engine-dice/).
The original Titan chips were certified using a custom Google design, because
these chips were manufactured before relevant industry standards were
introduced. Google's experience in manufacturing and deploying secure hardware
motivates us to increase participation in standards processes, and newer
standards such as DICE, Trusted Platform Module (TPM), and Security Protocol and
Data Mode (SPDM) include changes that reflect our experience.

## Titan integration

When the Titan chip is integrated into a platform, it provides security
protections to an application processor (AP). For example, Titan might be paired
with a CPU that runs workloads, a baseboard management controller (BMC), or an
accelerator for workloads such as machine learning.

Titan communicates with the AP using the serial peripheral interface (SPI) bus.
Titan interposes between the AP and the AP's boot firmware flash chip, ensuring
that Titan can read and measure every byte of that firmware before the firmware
is run at boot time.

The following steps occur when a Titan-enabled platform powers on:

1. Titan keeps the CPU in reset mode while Titan's internal application
  processor runs immutable code (the *boot ROM*) from its embedded
  read-only memory.
2. Titan runs a built-in self-test to verify that all memory (including the ROM)
  hasn't been tampered with.
3. Titan's boot ROM verifies Titan's firmware using public key cryptography and
  mixes the identity of the verified firmware into Titan's key hierarchy.
4. Titan's boot ROM loads Titan's verified firmware.
5. Titan firmware verifies the contents of the AP's boot firmware flash using
  public key cryptography. Titan blocks the AP's access to its boot firmware
  flash until the verification process completes successfully.
6. After verification, the Titan chip releases the AP from reset, allowing the
  AP to boot.
7. The AP firmware performs additional configuration, which might include
  launching further boot images. The AP can capture measurements of these boot
  images and send the measurements to Titan for secure monitoring.

These steps achieve *first-instruction integrity* because Google can identify
the boot firmware and OS that was booted on the machine from the very first
instruction that runs during the startup cycle. For APs with CPUs that accept
microcode updates, the boot process also lets Google know which microcode
patches were fetched before the boot firmware's first instruction. For more
information, see [Measured boot
process](https://cloud.google.com/docs/security/boot-integrity#measured-boot-process).

This flow is similar to the boot process that is performed by platforms that are
equipped with a TPM. However, Titan chips include features that are not
generally available on standard TPMs, such as Titan's internal firmware
self-attestation or AP firmware upgrade security, as described in the following
sections.

Standard TPM integrations can be vulnerable to physical interposer attacks.
Newer Titan integrations at Google mitigate these attacks by using
integrated roots of trust. For more information, see
[TPM Transport Security: Defeating Active Interposers with DICE (YouTube)](https://www.youtube.com/watch?v=DKfbkOTYzOU).

## Secure Titan firmware upgrade

The Titan chip's firmware is signed by a key that is held in an offline HSM,
which is protected by quorum-based controls. Titan's boot ROM verifies Titan
firmware's signature whenever the chip boots.

Titan firmware is signed with a security version number (SVN), which conveys the
security state of the image. If a firmware image includes a vulnerability fix,
the image's SVN is incremented. Titan hardware lets the production network
strongly attest to the SVN of Titan's firmware, even if older firmware might
have had vulnerabilities. The upgrade process lets us recover from these
vulnerabilities at scale, even if they affect Titan's own firmware. For more
information, see [Recovering from vulnerabilities in root-of-trust
firmware](https://cloud.google.com/docs/security/boot-integrity#recovering_from_vulnerabilities_in_root-of-trust_firmware).

Google contributed to the latest version of the TPM Library specification, which
now includes features that let other TPMs provide similar self-attestation
assurances. For more information, see the [TPM Firmware-Limited and SVN-Limited
Objects section
(PDF)](https://trustedcomputinggroup.org/wp-content/uploads/TPM-2.0-1.83-Part-1-Architecture.pdf#page=288)
of version 1.83 of the TPM Architecture specification. These TPM features were
implemented and deployed on our latest Titan chips.

## Secure AP firmware upgrade

In addition to Titan's firmware, we also cryptographically sign the firmware
that runs on the AP. Titan verifies this signature as part of the platform boot
process. It also verifies this signature whenever the AP firmware is updated,
enforcing that only authentic AP firmware images can be written to the AP's boot
firmware flash chip. This verification process mitigates attacks that attempt to
install persistent backdoors or render the platform unbootable. Signature
verification also provides defense in depth for Google's platforms in the event
that a CPU has a vulnerability in its own microcode authentication mechanism.

## What's next

Learn more about our [boot integrity
process](https://cloud.google.com/docs/security/boot-integrity).

   Was this helpful?
