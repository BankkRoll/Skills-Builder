# Software Bill of Materials (SBOMs) and more

# Software Bill of Materials (SBOMs)

> Learn what SBOMs are, why they matter, and how Docker Hardened Images include signed SBOMs to support transparency and compliance.

# Software Bill of Materials (SBOMs)

   Table of contents

---

## What is an SBOM?

An SBOM is a detailed inventory that lists all components, libraries, and
dependencies used in building a software application. It provides transparency
into the software supply chain by documenting each component's version, origin,
and relationship to other components. Think of it as a "recipe" for your
software, detailing every ingredient and how they come together.

Metadata included in an SBOM for describing software artifacts may include:

- Name of the artifact
- Version
- License type
- Authors
- Unique package identifier

## Why are SBOMs important?

In today's software landscape, applications often comprise numerous components
from various sources, including open-source libraries, third-party services, and
proprietary code. This complexity can obscure visibility into potential
vulnerabilities and complicate compliance efforts. SBOMs address these
challenges by providing a detailed inventory of all components within an
application.

The significance of SBOMs is underscored by several key factors:

- Enhanced transparency: SBOMs offer a comprehensive view of all components that
  constitute an application, enabling organizations to identify and assess risks
  associated with third-party libraries and dependencies.
- Proactive vulnerability management: By maintaining an up-to-date SBOM,
  organizations can swiftly identify and address vulnerabilities in software
  components, reducing the window of exposure to potential exploits.
- Regulatory compliance: Many regulations and industry standards now require
  organizations to maintain control over the software components they use. An
  SBOM facilitates compliance by providing a clear and accessible record.
- Improved incident response: In the event of a security breach, an SBOM
  enables organizations to quickly identify affected components and take
  appropriate action, minimizing potential damage.

## Docker Hardened Image SBOMs

Docker Hardened Images come with built-in SBOMs, ensuring that every component
in the image is documented and verifiable. These SBOMs are cryptographically
signed, providing a tamper-evident record of the image's contents. This
integration simplifies audits and enhances trust in the software supply chain.

## View SBOMs in Docker Hardened Images

To view the SBOM of a Docker Hardened Image, you can use the `docker scout sbom`
command. Replace `<image-name>:<tag>` with the image name and tag.

```console
$ docker scout sbom dhi.io/<image-name>:<tag>
```

## Verify the SBOM of a Docker Hardened Image

Since Docker Hardened Images come with signed SBOMs, you can use Docker Scout to
verify the authenticity and integrity of the SBOM attached to the image. This
ensures that the SBOM has not been tampered with and that the image's contents
are trustworthy.

To verify the SBOM of a Docker Hardened Image using Docker Scout, use the following command:

```console
$ docker scout attest get dhi.io/<image-name>:<tag> \
   --predicate-type https://scout.docker.com/sbom/v0.1 --verify --platform <platform>
```

For example, to verify the SBOM attestation for the `node:20.19-debian12` image:

```console
$ docker scout attest get dhi.io/node:20.19-debian12 \
   --predicate-type https://scout.docker.com/sbom/v0.1 --verify --platform linux/amd64
```

## Resources

For more details about SBOM attestations and Docker Build, see
[SBOM
attestations](https://docs.docker.com/build/metadata/attestations/sbom/).

To learn more about Docker Scout and working with SBOMs, see [Docker Scout SBOMs](https://docs.docker.com/scout/how-tos/view-create-sboms/).

---

# Code signing

> Understand how Docker Hardened Images are cryptographically signed using Cosign to verify authenticity, integrity, and secure provenance.

# Code signing

   Table of contents

---

## What is code signing?

Code signing is the process of applying a cryptographic signature to software
artifacts, such as Docker images, to verify their integrity and authenticity. By
signing an image, you ensure that it has not been altered since it was signed
and that it originates from a trusted source.

In the context of Docker Hardened Images (DHIs), code signing is achieved using
[Cosign](https://docs.sigstore.dev/), a tool developed by the Sigstore project.
Cosign enables secure and verifiable signing of container images, enhancing
trust and security in the software supply chain.

## Why is code signing important?

Code signing plays a crucial role in modern software development and
cybersecurity:

- Authenticity: Verifies that the image was created by a trusted source.
- Integrity: Ensures that the image has not been tampered with since it was
  signed.
- Compliance: Helps meet regulatory and organizational security requirements.

## Docker Hardened Image code signing

Each DHI is cryptographically signed using Cosign, ensuring that the images have
not been tampered with and originate from a trusted source.

## Why sign your own images?

Docker Hardened Images are signed by Docker to prove their origin and integrity,
but if you're building application images that extend or use DHIs as a base, you
should sign your own images as well.

By signing your own images, you can:

- Prove the image was built by your team or pipeline
- Ensure your build hasn't been tampered with after it's pushed
- Support software supply chain frameworks like SLSA
- Enable image verification in deployment workflows

This is especially important in CI/CD environments where you build and push
images frequently, or in any scenario where image provenance must be auditable.

## How to view and use code signatures

### View signatures

You can verify that a Docker Hardened Image is signed and trusted using either Docker Scout or Cosign.

To lists all attestations, including signature metadata, attached to the image, use the following command:

```console
$ docker scout attest list <image-name>:<tag>
```

> Note
>
> If the image exists locally on your device, you must prefix the image name with `registry://`. For example, use
> `registry://dhi.io/python` instead of `dhi.io/python`.

To verify a specific signed attestation (e.g., SBOM, VEX, provenance):

```console
$ docker scout attest get \
  --predicate-type <predicate-uri> \
  --verify \
  <image-name>:<tag>
```

> Note
>
> If the image exists locally on your device, you must prefix the image name with `registry://`. For example, use
> `registry://dhi.io/python:3.13` instead of `dhi.io/python:3.13`.

For example:

```console
$ docker scout attest get \
  --predicate-type https://openvex.dev/ns/v0.2.0 \
  --verify \
  dhi.io/python:3.13
```

If valid, Docker Scout will confirm the signature and display signature payload, as well as the equivalent Cosign command to verify the image.

### Sign images

To sign a Docker image, use [Cosign](https://docs.sigstore.dev/). Replace
`<image-name>:<tag>` with the image name and tag.

```console
$ cosign sign <image-name>:<tag>
```

This command will prompt you to authenticate via an OIDC provider (such as
GitHub, Google, or Microsoft). Upon successful authentication, Cosign will
generate a short-lived certificate and sign the image. The signature will be
stored in a transparency log and associated with the image in the registry.

---

# Supply

> Learn how Docker Hardened Images comply with SLSA Build Level 3 and how to verify provenance for secure, tamper-resistant builds.

# Supply-chain Levels for Software Artifacts (SLSA)

   Table of contents

---

## What is SLSA?

Supply-chain Levels for Software Artifacts (SLSA) is a security framework
designed to enhance the integrity and security of software supply chains.
Developed by Google and maintained by the Open Source Security Foundation
(OpenSSF), SLSA provides a set of guidelines and best practices to prevent
tampering, improve integrity, and secure packages and infrastructure in software
projects.

SLSA defines [four build levels (0–3)](https://slsa.dev/spec/latest/build-track-basics) of
increasing security rigor, focusing on areas such as build provenance, source
integrity, and build environment security. Each level builds upon the previous
one, offering a structured approach to achieving higher levels of software
supply chain security.

## Why is SLSA important?

SLSA is crucial for modern software development due to the increasing complexity
and interconnectedness of software supply chains. Supply chain attacks, such as
the SolarWinds breach, have highlighted the vulnerabilities in software
development processes. By implementing SLSA, organizations can:

- Ensure artifact integrity: Verify that software artifacts have not been
  tampered with during the build and deployment processes.
- Enhance build provenance: Maintain verifiable records of how and when software
  artifacts were produced, providing transparency and accountability.
- Secure build environments: Implement controls to protect build systems from
  unauthorized access and modifications.
- Mitigate supply chain risks: Reduce the risk of introducing vulnerabilities or
  malicious code into the software supply chain.

## What is SLSA Build Level 3?

SLSA Build Level 3, Hardened Builds, is the highest of four progressive levels in
the SLSA framework. It introduces strict requirements to ensure that software
artifacts are built securely and traceably. To meet Level 3, a build must:

- Be fully automated and scripted to prevent manual tampering
- Use a trusted build service that enforces source and builder authentication
- Generate a signed, tamper-resistant provenance record describing how the artifact was built
- Capture metadata about the build environment, source repository, and build steps

This level provides strong guarantees that the software was built from the
expected source in a controlled, auditable environment, which significantly
reduces the risk of supply chain attacks.

## Docker Hardened Images and SLSA

Docker Hardened Images (DHIs) are secure-by-default container images
purpose-built for modern production environments. Each DHI is cryptographically
signed and complies with the [SLSA Build Level 3
standard](https://slsa.dev/spec/latest/build-track-basics#build-l3), ensuring
verifiable build provenance and integrity.

By integrating SLSA-compliant DHIs into your development and deployment processes, you can:

- Achieve higher security levels: Utilize images that meet stringent security
  standards, reducing the risk of vulnerabilities and attacks.
- Simplify compliance: Leverage built-in features like signed Software Bills of
  Materials (SBOMs) and vulnerability exception (VEX) statements to facilitate
  compliance with regulations such as FedRAMP.
- Enhance transparency: Access detailed information about the components and
  build process of each image, promoting transparency and trust.
- Streamline audits: Utilize verifiable build records and signatures to simplify
  security audits and assessments.

## Get and verify SLSA provenance for Docker Hardened Images

Each Docker Hardened Image (DHI) is cryptographically signed and includes
attestations. These attestations provide verifiable build provenance and
demonstrate adherence to SLSA Build Level 3 standards.

To get and verify SLSA provenance for a DHI, you can use Docker Scout.

```console
$ docker scout attest get dhi.io/<image>:<tag> \
  --predicate-type https://slsa.dev/provenance/v0.2 \
  --verify
```

For example:

```console
$ docker scout attest get dhi.io/node:20.19-debian12 \
  --predicate-type https://slsa.dev/provenance/v0.2 \
  --verify
```

## Resources

For more details about SLSA definitions and Docker Build, see
[SLSA
definitions](https://docs.docker.com/build/metadata/attestations/slsa-definitions/).

---

# Software Supply Chain Security

> Learn how Docker Hardened Images help secure every stage of your software supply chain with signed metadata, provenance, and minimal attack surface.

# Software Supply Chain Security

   Table of contents

---

## What is Software Supply Chain Security (SSCS)?

SSCS encompasses practices and strategies designed to safeguard the entire
lifecycle of software development from initial code creation to deployment and
maintenance. It focuses on securing all components. This includes code,
dependencies, build processes, and distribution channels in order to prevent
malicious actors from compromising the software supply chain. Given the
increasing reliance on open-source libraries and third-party components,
ensuring the integrity and security of these elements is paramount

## Why is SSCS important?

The significance of SSCS has escalated due to the rise in sophisticated
cyberattacks targeting software supply chains. Recent incidents and the
exploitation of vulnerabilities in open-source components have underscored the
critical need for robust supply chain security measures. Compromises at any
stage of the software lifecycle can lead to widespread vulnerabilities, data
breaches, and significant financial losses.

## How Docker Hardened Images contribute to SSCS

Docker Hardened Images (DHI) are purpose-built container images designed with
security at their core, addressing the challenges of modern software supply
chain security. By integrating DHI into your development and deployment
pipelines, you can enhance your organization's SSCS posture through the
following features:

- Minimal attack surface: DHIs are engineered to be ultra-minimal, stripping
  away unnecessary components and reducing the attack surface by up to 95%. This
  distroless approach minimizes potential entry points for malicious actors.
- Cryptographic signing and provenance: Each DHI is cryptographically signed,
  ensuring authenticity and integrity. Build provenance is maintained, providing
  verifiable evidence of the image's origin and build process, aligning with
  standards like SLSA (Supply-chain Levels for Software Artifacts).
- Software Bill of Materials (SBOM): DHIs include a comprehensive SBOM,
  detailing all components and dependencies within the image. This transparency
  aids in vulnerability management and compliance tracking, enabling teams to
  assess and mitigate risks effectively.
- Continuous maintenance and rapid CVE remediation: Docker maintains DHIs with
  regular updates and security patches, backed by an SLA for addressing critical
  and high-severity vulnerabilities. This proactive approach helps ensure that
  images remain secure and compliant with enterprise standards.

---

# Secure Software Development Lifecycle

> See how Docker Hardened Images support a secure SDLC by integrating with scanning, signing, and debugging tools.

# Secure Software Development Lifecycle

   Table of contents

---

## What is a Secure Software Development Lifecycle?

A Secure Software Development Lifecycle (SSDLC) integrates security practices
into every phase of software delivery, from design and development to deployment
and monitoring. It’s not just about writing secure code, but about embedding
security throughout the tools, environments, and workflows used to build and
ship software.

SSDLC practices are often guided by compliance frameworks, organizational
policies, and supply chain security standards such as SLSA (Supply-chain Levels
for Software Artifacts) or NIST SSDF.

## Why SSDLC matters

Modern applications depend on fast, iterative development, but rapid delivery
often introduces security risks if protections aren’t built in early. An SSDLC
helps:

- Prevent vulnerabilities before they reach production
- Ensure compliance through traceable and auditable workflows
- Reduce operational risk by maintaining consistent security standards
- Enable secure automation in CI/CD pipelines and cloud-native environments

By making security a first-class citizen in each stage of software delivery,
organizations can shift left and reduce both cost and complexity.

## How Docker supports a secure SDLC

Docker provides tools and secure content that make SSDLC practices easier to
adopt across the container lifecycle. With [Docker Hardened
Images](https://docs.docker.com/dhi/) (DHIs), [Docker
Debug](https://docs.docker.com/reference/cli/docker/debug/), and [Docker
Scout](https://docs.docker.com/scout/), teams can add security without losing
velocity.

### Plan and design

During planning, teams define architectural constraints, compliance goals, and
threat models. Docker Hardened Images help at this stage by providing:

- Secure-by-default base images for common languages and runtimes
- Verified metadata including SBOMs, provenance, and VEX documents
- Support for both glibc and musl across multiple Linux distributions

You can use DHI metadata and attestations to support design reviews, threat
modeling, or architecture sign-offs.

### Develop

In development, security should be transparent and easy to apply. Docker
Hardened Images support secure-by-default development:

- Dev variants include shells, package managers, and compilers for convenience
- Minimal runtime variants reduce attack surface in final images
- Multi-stage builds let you separate build-time tools from runtime environments

[Docker Debug](https://docs.docker.com/reference/cli/docker/debug/) helps developers:

- Temporarily inject debugging tools into minimal containers
- Avoid modifying base images during troubleshooting
- Investigate issues securely, even in production-like environments

### Build and test

Build pipelines are an ideal place to catch issues early. Docker Scout
integrates with Docker Hub and the CLI to:

- Scan for known CVEs using multiple vulnerability databases
- Trace vulnerabilities to specific layers and dependencies
- Interpret signed VEX data to suppress known-irrelevant issues
- Export JSON scan reports for CI/CD workflows

Build pipelines that use Docker Hardened Images benefit from:

- Reproducible, signed images
- Minimal build surfaces to reduce exposure
- Built-in compliance with SLSA Build Level 3 standards

### Release and deploy

Security automation is critical as you release software at scale. Docker
supports this phase by enabling:

- Signature verification and provenance validation before deployment
- Policy enforcement gates using Docker Scout
- Safe, non-invasive container inspection using Docker Debug

DHIs ship with the metadata and signatures required to automate image
verification during deployment.

### Monitor and improve

Security continues after release. With Docker tools, you can:

- Continuously monitor image vulnerabilities through Docker Hub
- Get CVE remediation guidance and patch visibility using Docker Scout
- Receive updated DHI images with rebuilt and re-signed secure layers
- Debug running workloads with Docker Debug without modifying the image

## Summary

Docker helps teams embed security throughout the SSDLC by combining secure
content (DHIs) with developer-friendly tooling (Docker Scout and Docker Debug).
These integrations promote secure practices without introducing friction, making
it easier to adopt compliance and supply chain security across your software
delivery lifecycle.

---

# STIGDHI Enterprise

> Learn how Docker Hardened Images provide STIG-ready container images with verifiable security scan attestations for government and enterprise compliance requirements.

# STIGDHI Enterprise

   Table of contents

---

Subscription: Docker Hardened Images Enterprise

## What is STIG?

[Security Technical Implementation Guides
(STIGs)](https://public.cyber.mil/stigs/) are configuration standards published
by the U.S. Defense Information Systems Agency (DISA). They define security
requirements for operating systems, applications, databases, and other
technologies used in U.S. Department of Defense (DoD) environments.

STIGs help ensure that systems are configured securely and consistently to
reduce vulnerabilities. They are often based on broader requirements like the
DoD's General Purpose Operating System Security Requirements Guide (GPOS SRG).

## Why STIG guidance matters

Following STIG guidance is critical for organizations that work with or support
U.S. government systems. It demonstrates alignment with DoD security standards
and helps:

- Accelerate Authority to Operate (ATO) processes for DoD systems
- Reduce the risk of misconfiguration and exploitable weaknesses
- Simplify audits and reporting through standardized baselines

Even outside of federal environments, STIGs are used by security-conscious
organizations as a benchmark for hardened system configurations.

STIGs are derived from broader NIST guidance, particularly [NIST Special
Publication 800-53](https://csrc.nist.gov/publications/sp800), which defines a
catalog of security and privacy controls for federal systems. Organizations
pursuing compliance with 800-53 or related frameworks (such as FedRAMP) can use
STIGs as implementation guides that help meet applicable control requirements.

## How Docker Hardened Images help apply STIG guidance

Docker Hardened Images (DHIs) include STIG variants that are scanned against
custom STIG-based profiles and include signed STIG scan attestations. These
attestations can support audits and compliance reporting.

While Docker Hardened Images are available to all, the STIG variant requires a
Docker subscription.

Docker creates custom STIG-based profiles for images based on the GPOS SRG and
DoD Container Hardening Process Guide. Because DISA has not published a STIG
specifically for containers, these profiles help apply STIG-like guidance to
container environments in a consistent, reviewable way and are designed to
reduce false positives common in container images.

## Identify images that include STIG scan results

Docker Hardened Images that include STIG scan results are labeled as **STIG** in
the Docker Hardened Images catalog.

To find DHI repositories with STIG image variants, [explore
images](https://docs.docker.com/dhi/how-to/explore/) and:

- Use the **STIG** filter on the catalog page
- Look for **STIG** labels on individual image listings

To find a STIG image variant within a repository, go to the **Tags** tab in the
repository, and find images labeled with **STIG** in the **Compliance** column.

## Use a STIG variant

To use a STIG variant, you must [mirror](https://docs.docker.com/dhi/how-to/mirror/) the repository
and then pull the STIG image from your mirrored repository.

## View and verify STIG scan results

Docker provides a signed [STIG scan
attestation](https://docs.docker.com/dhi/core-concepts/attestations/) for each STIG-ready image.
These attestations include:

- A summary of the scan results, including the number of passed, failed, and not
  applicable checks
- The name and version of the STIG profile used
- Full output in both HTML and XCCDF (XML) formats

### View STIG scan attestations

You can retrieve and inspect a STIG scan attestation using the Docker Scout CLI:

```console
$ docker scout attest get \
  --predicate-type https://docker.com/dhi/stig/v0.1 \
  --verify \
  --predicate \
  dhi.io/<image>:<tag>
```

### Extract HTML report

To extract and view the human-readable HTML report:

```console
$ docker scout attest get dhi.io/<image>:<tag> \
  --predicate-type https://docker.com/dhi/stig/v0.1 \
  --verify \
  --predicate \
  | jq -r '.[0].output[] | select(.format == "html").content | @base64d' > stig_report.html
```

### Extract XCCDF report

To extract the XML (XCCDF) report for integration with other tools:

```console
$ docker scout attest get dhi.io/<image>:<tag> \
  --predicate-type https://docker.com/dhi/stig/v0.1 \
  --verify \
  --predicate \
  | jq -r '.[0].output[] | select(.format == "xccdf").content | @base64d' > stig_report.xml
```

### View STIG scan summary

To view just the scan summary without the full reports:

```console
$ docker scout attest get dhi.io/<image>:<tag> \
  --predicate-type https://docker.com/dhi/stig/v0.1 \
  --verify \
  --predicate \
  | jq -r '.[0] | del(.output)'
```

---

# Vulnerability Exploitability eXchange (VEX)

> Learn how VEX helps you prioritize real risks by identifying which vulnerabilities in Docker Hardened Images are actually exploitable.

# Vulnerability Exploitability eXchange (VEX)

   Table of contents

---

## What is VEX?

Vulnerability Exploitability eXchange (VEX) is a specification for documenting
the exploitability status of vulnerabilities within software components. VEX is
primarily defined through industry standards such as CSAF (OASIS) and CycloneDX
VEX, with the U.S. Cybersecurity and Infrastructure Security Agency (CISA)
encouraging its adoption. VEX complements CVE (Common Vulnerabilities and
Exposures) identifiers by adding producer-asserted status information,
indicating whether a vulnerability is exploitable in the product as shipped.
This helps organizations prioritize remediation efforts by identifying
vulnerabilities that do not affect their specific product configurations.

## Why is VEX important?

VEX enhances traditional vulnerability management by:

- Suppressing non-applicable vulnerabilities: By providing product-level
  exploitability assertions from the supplier, VEX helps filter out
  vulnerabilities that do not affect the product as shipped.
- Prioritizing remediation: Organizations can focus resources on addressing
  vulnerabilities that the producer has confirmed are exploitable in the
  product, improving efficiency in vulnerability management.
- Supporting vulnerability documentation: VEX statements can support audit
  discussions and help document why certain vulnerabilities do not require
  remediation.

This approach is particularly beneficial when working with complex software
components where not all reported CVEs apply to the specific product
configuration.

## How Docker Hardened Images integrate VEX

To enhance vulnerability management, Docker Hardened Images (DHI) incorporate
VEX reports, providing context-specific assessments of known vulnerabilities.

This integration allows you to:

- Consume producer assertions: Review Docker's assertions about whether known
  vulnerabilities in the image's components are exploitable in the product as
  shipped.
- Prioritize actions: Focus remediation efforts on vulnerabilities that Docker
  has confirmed are exploitable in the image, optimizing resource allocation.
- Support audit documentation: Use VEX statements to document why certain
  reported vulnerabilities do not require immediate action.

By combining the security features of DHI with VEX's product-level
exploitability assertions, organizations can achieve a more effective and
efficient approach to vulnerability management.

> Tip
>
> To understand which scanners support VEX and why it matters for your security
> workflow, see
> [Scanner integrations](https://docs.docker.com/dhi/explore/scanner-integrations/).

## Use VEX to suppress non-applicable CVEs

Docker Hardened Images include VEX attestations that can be consumed by
vulnerability scanners to suppress non-applicable CVEs. For detailed
instructions on scanning with VEX support across different tools including
Docker Scout, Trivy, and Grype, see
[Scan Docker Hardened
Images](https://docs.docker.com/dhi/how-to/scan/).

---

# Core concepts

> Learn the core concepts behind Docker Hardened Images, including security metadata, vulnerability management, image structure, and verification.

# Core concepts

   Table of contents

---

Docker Hardened Images (DHIs) are built on a foundation of secure software
supply chain practices. This section explains the core concepts behind that
foundation, from signed attestations and immutable digests to standards like SLSA
and VEX.

Start here if you want to understand how Docker Hardened Images support compliance,
transparency, and security.

## Security metadata and attestations

[AttestationsReview the full set of signed attestations included with each Docker Hardened Image, such as SBOMs, VEX, build provenance, and scan results.](https://docs.docker.com/dhi/core-concepts/attestations/)[Software Bill of Materials (SBOMs)Learn what SBOMs are, why they matter, and how Docker Hardened Images include signed SBOMs to support transparency and compliance.](https://docs.docker.com/dhi/core-concepts/sbom/)[Supply-chain Levels for Software Artifacts (SLSA)Learn how Docker Hardened Images comply with SLSA Build Level 3 and how to verify provenance for secure, tamper-resistant builds.](https://docs.docker.com/dhi/core-concepts/slsa/)[Image provenanceLearn how build provenance metadata helps trace the origin of Docker Hardened Images and support compliance with SLSA.](https://docs.docker.com/dhi/core-concepts/provenance/)

## Compliance standards

[FIPSLearn how Docker Hardened Images support FIPS 140 by using validated cryptographic modules and providing signed attestations for compliance audits.](https://docs.docker.com/dhi/core-concepts/fips/)[STIGLearn how Docker Hardened Images provide STIG-ready container images with verifiable security scan attestations for government and enterprise compliance requirements.](https://docs.docker.com/dhi/core-concepts/stig/)[CIS BenchmarksLearn how Docker Hardened Images help you meet Center for Internet Security (CIS) Docker Benchmark requirements for secure container configuration and deployment.](https://docs.docker.com/dhi/core-concepts/cis/)

## Vulnerability and risk management

[Common Vulnerabilities and Exposures (CVEs)Understand what CVEs are, how Docker Hardened Images reduce exposure, and how to scan images for vulnerabilities using popular tools.](https://docs.docker.com/dhi/core-concepts/cves/)[Vulnerability Exploitability eXchange (VEX)Learn how VEX helps you prioritize real risks by identifying which vulnerabilities in Docker Hardened Images are actually exploitable.](https://docs.docker.com/dhi/core-concepts/vex/)[Software Supply Chain SecurityLearn how Docker Hardened Images help secure every stage of your software supply chain with signed metadata, provenance, and minimal attack surface.](https://docs.docker.com/dhi/core-concepts/sscs/)[Secure Software Development Lifecycle (SSDLC)See how Docker Hardened Images support a secure SDLC by integrating with scanning, signing, and debugging tools.](https://docs.docker.com/dhi/core-concepts/ssdlc/)

## Image structure and behavior

[Distroless imagesLearn how Docker Hardened Images use distroless variants to minimize attack surface and remove unnecessary components.](https://docs.docker.com/dhi/core-concepts/distroless/)[glibc and musl support in Docker Hardened ImagesCompare glibc and musl variants of DHIs to choose the right base image for your application’s compatibility, size, and performance needs.](https://docs.docker.com/dhi/core-concepts/glibc-musl/)[Image immutabilityUnderstand how image digests, read-only containers, and signed metadata ensure Docker Hardened Images are tamper-resistant and immutable.](https://docs.docker.com/dhi/core-concepts/immutability/)[Image hardeningLearn how Docker Hardened Images are designed for security, with minimal components, nonroot execution, and secure-by-default configurations.](https://docs.docker.com/dhi/core-concepts/hardening/)

## Verification and traceability

[DigestsLearn how to use immutable image digests to guarantee consistency and verify the exact Docker Hardened Image you're running.](https://docs.docker.com/dhi/core-concepts/digests/)[Code signingUnderstand how Docker Hardened Images are cryptographically signed using Cosign to verify authenticity, integrity, and secure provenance.](https://docs.docker.com/dhi/core-concepts/signatures/)

---

# Available types of Docker Hardened Images

> Learn about the different image types, distributions, and variants offered in the Docker Hardened Images catalog.

# Available types of Docker Hardened Images

   Table of contents

---

Docker Hardened Images (DHI) is a comprehensive catalog of
security-hardened container images built to meet diverse
development and production needs.

## Framework and application images

DHI includes a selection of popular frameworks and application images, each
hardened and maintained to ensure security and compliance. These images
integrate seamlessly into existing workflows, allowing developers to focus on
building applications without compromising on security.

For example, you might find repositories like the following in the DHI catalog:

- `node`: framework for Node.js applications
- `python`: framework for Python applications
- `nginx`: web server image

## Base image distributions

Docker Hardened Images are available in different base image options, giving you
flexibility to choose the best match for your environment and workload
requirements:

- Debian-based images: A good fit if you're already working in glibc-based
  environments. Debian is widely used and offers strong compatibility across
  many language ecosystems and enterprise systems.
- Alpine-based images: A smaller and more lightweight option using musl libc.
  These images tend to be small and are therefore faster to pull and have a
  reduced footprint.

Each image maintains a minimal and secure runtime layer by removing
non-essential components like shells, package managers, and debugging tools.
This helps reduce the attack surface while retaining compatibility with common
runtime environments. To maintain this lean, secure foundation, DHI standardizes
on Debian for glibc-based images, which provides broad compatibility while
minimizing complexity and maintenance overhead.

Example tags include:

- `3.9.23-alpine3.21`: Alpine-based image for Python 3.9.23
- `3.9.23-debian12`: Debian-based image for Python 3.9.23

If you're not sure which to choose, start with the base you're already familiar
with. Debian tends to offer the broadest compatibility.

## Development and runtime variants

To accommodate different stages of the application lifecycle, DHI offers all
language framework images and select application images in two variants:

- Development (dev) images: Equipped with necessary development tools and
  libraries, these images facilitate the building and testing of applications in a
  secure environment. They include a shell, package manager, a root user, and
  other tools needed for development.
- Runtime images: Stripped of development tools, these images contain only the
  essential components needed to run applications, ensuring a minimal attack
  surface in production.

This separation supports multi-stage builds, enabling developers to compile code
in a secure build environment and deploy it using a lean runtime image.

For example, you might find tags like the following in a DHI repository:

- `3.9.23-debian12`: runtime image for Python 3.9.23
- `3.9.23-debian12-dev`: development image for Python 3.9.23

## FIPs and STIG variantsDHI Enterprise

Subscription: Docker Hardened Images Enterprise

Some Docker Hardened Images include a `-fips` variant. These variants use
cryptographic modules that have been validated under [FIPS
140](https://docs.docker.com/dhi/core-concepts/fips/), a U.S. government standard for secure
cryptographic operations.

FIPS variants are designed to help organizations meet regulatory and compliance
requirements related to cryptographic use in sensitive or regulated
environments.

You can recognize FIPS variants by their tag that includes `-fips`.

For example:

- `3.13-fips`: FIPS variant of the Python 3.13 image
- `3.9.23-debian12-fips`: FIPS variant of the Debian-based Python 3.9.23 image

FIPS variants can be used in the same way as any other Docker Hardened Image and
are ideal for teams operating in regulated industries or under compliance
frameworks that require cryptographic validation.

In addition to FIPS variants, some Docker Hardened Images also include
STIG-ready variants. These images are scanned against custom STIG-based
profiles and come with signed STIG scan attestations to support audits and
compliance reporting. To identify STIG-ready variants, look for the **STIG**
in the **Compliance** column of the image tags list in the Docker Hub catalog.

## Compatibility variants

Some Docker Hardened Images include a compatiability variant. These variants
provide additional tools and configurations for specific use cases without
bloating the minimal base images.

Compatibility variants are created to support:

- Helm chart compatibility: Applications deployed via Helm charts and
  Kubernetes that require specific runtime configurations or utilities for
  seamless integration with popular Helm charts.
- Special application use-cases: Applications that need optional tools not
  included in the minimal image.

By offering these as separate image flavors, DHI ensures that the minimal images
remain lean and secure, while providing the tools you need in dedicated
variants. This approach maintains a minimal attack surface for standard
deployments while supporting specialized requirements when needed.

You can recognize compatibility variants by their tag that includes `-compat`.

Use compatibility variants when your deployment requires additional tools beyond
the minimal runtime, such as when using Helm charts or applications with
specific tooling requirements.

---

# How Docker Hardened Images are built

> Learn how Docker builds, tests, and maintains Docker Hardened Images through an automated, security-focused pipeline.

# How Docker Hardened Images are built

   Table of contents

---

Docker Hardened Images are built through an automated pipeline that monitors
upstream sources, applies security updates, and publishes signed artifacts.
This page explains the build process for both base DHI images and DHI Enterprise
customized images.

With a DHI Enterprise subscription, the automated security update pipeline for
both base and customized images is backed by SLA commitments, including a 7-day
SLA for critical and high severity vulnerabilities. Only DHI Enterprise includes
SLAs. DHI Free offers a secure baseline but no guaranteed remediation timelines.

## Build triggers

Builds start automatically. You don't trigger them manually. The system monitors
for changes and starts builds in two scenarios:

- [Upstream updates](#upstream-updates)
- [Customization changes](#customization-changes)

### Upstream updates

New releases, package updates, or CVE fixes from upstream projects trigger base
image rebuilds. These builds go through quality checks to ensure security and
reliability.

#### Monitoring for updates

Docker continuously monitors upstream projects for new releases, package
updates, and security advisories. When changes are detected, the system
automatically queues affected images for rebuild using a SLSA Build Level
3-compliant build system.

Docker uses three strategies to track updates:

- GitHub releases: Monitors specific GitHub repositories for new releases and
  automatically updates the image definition when a new version is published.
- GitHub tags: Tracks tags in GitHub repositories to detect new versions.
- Package repositories: Monitors Alpine Linux, Debian, and Ubuntu package
  repositories through Docker Scout's package database to detect updated
  packages.

In addition to explicit upstream tracking, Docker also monitors transitive
dependencies. When a package update is detected (for example, a security patch
for a library), Docker automatically identifies and rebuilds all images within
the support window that use that package.

### Customization changesDHI Enterprise

Subscription: Docker Hardened Images Enterprise

Updates to your OCI artifact customizations trigger rebuilds of your customized
images.

When you customize a DHI image with DHI Enterprise, your changes are packaged as
OCI artifacts that layer on top of the base image. Docker monitors your artifact
repositories and automatically rebuilds your customized images whenever you push
updates.

The rebuild process fetches the current base image, applies your OCI artifacts,
signs the result, and publishes it automatically. You don't need to manage
builds or maintain CI pipelines for your customized images.

Customized images are also rebuilt automatically when the base DHI image they
depend on receives updates, ensuring your images always include the latest
security patches.

## Build pipeline

The following sections describe the build pipeline architecture and workflow for
Docker Hardened Images based on:

- [Base image pipeline](#base-image-pipeline)
- [Customized image pipeline](#customized-image-pipeline)

### Base image pipeline

Each Docker Hardened Image is built through an automated pipeline:

1. Monitoring: Docker monitors upstream sources for updates (new releases,
  package updates, security advisories).
2. Rebuild trigger: When changes are detected, an automated rebuild starts.
3. AI guardrail: An AI system fetches upstream diffs and scans them with
  language-aware checks. The guardrail focuses on high-leverage issues that can
  cause significant problems, such as inverted error checks, ignored failures,
  resource mishandling, or suspicious contributor activity. When it spots
  potential risks, it blocks the PR from auto-merging.
4. Human review: If the AI identifies risks with high confidence,
  Docker engineers review the flagged code, reproduce the issue, and decide on
  the appropriate action. Engineers often contribute fixes back to upstream
  projects, improving the code for the entire community. When fixes are accepted
  upstream, the DHI build pipeline applies the patch immediately to protect
  customers while the fix moves through the upstream release process.
5. Testing: Images undergo comprehensive testing for compatibility and
  functionality.
6. Signing and attestations: Docker signs each image and generates
  attestations (SBOMs, VEX documents, build provenance).
7. Publishing: The signed image is published to the DHI registry and the
  attestations are published to the Docker Scout registry.
8. Cascade rebuilds: If any customized images use this base, their rebuilds
  are automatically triggered.

Docker responds quickly to critical vulnerabilities. By building essential
components from source rather than waiting for packaged updates, Docker can
patch critical and high severity CVEs within days of upstream fixes and publish
updated images with new attestations. For DHI Enterprise subscriptions, this
rapid response is backed by a 7-day SLA for critical and high severity
vulnerabilities.

The following diagram shows the base image build flow:

### Customized image pipelineDHI Enterprise

Subscription: Docker Hardened Images Enterprise

When you customize a DHI image with DHI Enterprise, the build process is simplified:

1. Monitoring: Docker monitors your OCI artifact repositories for changes.
2. Rebuild trigger: When you push updates to your OCI artifacts, or when the base
  DHI image is updated, an automated rebuild starts.
3. Fetch base image: The latest base DHI image is fetched.
4. Apply customizations: Your OCI artifacts are applied to the base image.
5. Signing and attestations: Docker signs the customized image and generates
  attestations (SBOMs, VEX documents, build provenance).
6. Publishing: The signed customized image is published to Docker Hub and the
  attestations are published to the Docker Scout registry.

Docker handles the entire process automatically, so you don't need to manage
builds for your customized images. However, you're responsible for testing your
customized images and managing any CVEs introduced by your OCI artifacts.

The following diagram shows the customized image build flow:

---

# Give feedback

> How to interact with the DHI team

# Give feedback

   Table of contents

---

Committed to maintaining the quality, security, and reliability of the Docker Hardened Images (DHI)
a repository has been created as a point of contact to encourage the community to collaborate
in improving the Hardened Images ecosystem.

## Questions or discussions

You can use the [GitHub Discussions
board](https://github.com/orgs/docker-hardened-images/discussions) to engage
with the DHI team for:

- General questions about DHIs
- Best practices and recommendations
- Security tips and advice
- Show and tell your implementations
- Community announcements

## Reporting bugs or issues

You can [open a new issue](https://github.com/docker-hardened-images/catalog/issues) for topics such as:

- Bug reports
- Feature requests
- Documentation improvements
- Security vulnerabilities (see security policy)

It's encouraged to first search existing issues to see if it’s already been reported.
The DHI team reviews reports regularly and appreciates clear, actionable feedback.

## Responsible security disclosure

It is forbidden to post details of vulnerabilities before coordinated disclosure and resolution.

If you discover a security vulnerability, report it responsibly by following Docker’s [security disclosure](https://www.docker.com/trust/vulnerability-disclosure-policy/).
