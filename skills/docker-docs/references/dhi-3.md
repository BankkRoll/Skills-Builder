# Understanding roles and responsibilities for Docker Hardened Images and more

# Understanding roles and responsibilities for Docker Hardened Images

> Understand the division of responsibilities between Docker, upstream projects, and you when using Docker Hardened Images.

# Understanding roles and responsibilities for Docker Hardened Images

   Table of contents

---

Docker Hardened Images (DHIs) are curated and maintained by Docker, and built
using upstream open source components. To deliver security, reliability, and
compliance, responsibilities are shared among three groups:

- Upstream maintainers: the developers and communities responsible for the
  open source software included in each image.
- Docker: the provider of hardened, signed, and maintained container images.
- You (the customer): the consumer who runs and, optionally, customizes DHIs
  in your environment.

This topic outlines who handles what, so you can use DHIs effectively and
securely.

## Releases

- Upstream: Publishes and maintains official releases of the software
  components included in DHIs. This includes versioning, changelogs, and
  deprecation notices.
- Docker: Builds, hardens, and signs Docker Hardened Images based on
  upstream versions. Docker maintains these images in line with upstream release
  timelines and internal policies.
- You: Ensure you're staying on supported versions of DHIs and upstream
  projects. Using outdated or unsupported components can introduce security
  risk.

## Patching

- Upstream: Maintains and updates the source code for each component,
  including fixing vulnerabilities in libraries and dependencies.
- Docker: Rebuilds and re-releases images with upstream patches applied. Docker
  monitors for vulnerabilities and publishes updates to affected images. Only
  DHI Enterprise includes SLAs. DHI Free offers a secure baseline but no
  guaranteed remediation timelines.
- You: Apply DHI updates in your environments and patch any software or
  dependencies you install on top of the base image.

## Testing

- Upstream: Defines the behavior and functionality of the original software,
  and is responsible for validating core features.
- Docker: Validates that DHIs start, run, and behave consistently with
  upstream expectations. Docker also runs security scans and includes a [testing
  attestation](https://docs.docker.com/dhi/core-concepts/attestations/) with each image.
- You: Test your application on top of DHIs and validate that any changes or
  customizations function as expected in your environment.

## Security and compliance

- Docker: Publishes signed SBOMs, VEX documents, provenance data, and CVE
  scan results with each image to support compliance and supply chain security.
  - For free DHI users: All security metadata and transparency features are
    included at no cost.
  - For DHI Enterprise users: Additional compliance variants (like FIPS and
    STIG) and customization capabilities are available, with automatic rebuilds
    when base images are patched.
- You: Integrate DHIs into your security and compliance workflows, including
  vulnerability management and auditing.

## Support

- Docker:
  - For free DHI users: Community support and public documentation are available.
  - For DHI Enterprise users: Access to Docker's enterprise support team for
    mission-critical applications.
- You: Monitor Docker's release notes, security advisories, and documentation
  for updates and best practices.

## Summary

Docker Hardened Images give you a secure foundation, complete with signed
metadata and upstream transparency. Your role is to make informed use of these
images, apply updates promptly, and validate that your configurations and
applications meet your internal requirements.

---

# Scanner integrations

> Learn which vulnerability scanners work with Docker Hardened Images and how to choose the right scanner for accurate vulnerability assessment.

# Scanner integrations

   Table of contents

---

Docker Hardened Images work with various vulnerability scanners. However, to get
accurate results that reflect the actual security posture of these images, your
scanner needs to understand the VEX (Vulnerability Exploitability eXchange)
attestations included with each image.

## Scanners with VEX support

The following scanners can read and apply VEX attestations included with Docker
Hardened Images to deliver more accurate vulnerability assessments:

- [Docker Scout](https://docs.docker.com/scout/): Automatically applies VEX statements with
  zero configuration. Integrated directly into Docker Desktop and the Docker CLI.
- [Trivy](https://trivy.dev/): Supports VEX through VEX Hub for automatic
  updates or local VEX files for air-gapped environments.
- [Grype](https://github.com/anchore/grype): Supports VEX via the `--vex`
  flag for local VEX file processing.
- [Wiz](https://www.wiz.io/): Automatically applies VEX statements with
  zero configuration.

For step-by-step instructions, see
[Scan Docker Hardened Images](https://docs.docker.com/dhi/how-to/scan/).

## Choosing a scanner for Docker Hardened Images

When selecting a scanner for use with Docker Hardened Images, whether it
supports open standards like OpenVEX is the key differentiator.

Docker Hardened Images include signed VEX attestations that follow the
[OpenVEX standard](https://openvex.dev/). OpenVEX is an open standard that meets
the minimum requirements for VEX defined by CISA (Cybersecurity and
Infrastructure Security Agency), the U.S. government agency responsible for
cybersecurity guidance. These attestations document which vulnerabilities don't
apply to the image and why, helping you focus on real risks. To understand what
VEX is and how it works, see the
[VEX core concept](https://docs.docker.com/dhi/core-concepts/vex/).

Because OpenVEX is an open standard with government backing, it has strong
industry momentum and any tool can implement it without vendor-specific
integrations. This matters when you bring in third-party auditors with their own
scanning tools, or when you want to use multiple security tools in your
pipeline. With VEX, these tools can all read and verify the same vulnerability
data directly from your images.

Without open standards like VEX, vendors make exploitability decisions using
proprietary methods, making it difficult to verify claims or compare results
across tools. This fragments your security toolchain and creates inconsistent
vulnerability assessments across different scanning tools.

### Benefits of scanners with VEX support

Scanners that support open standards like OpenVEX and can interpret VEX attestations
from Docker Hardened Images offer the following benefits:

- Accurate vulnerability counts: Automatically filter out vulnerabilities
  that don't apply to your specific image, often reducing false positives
  dramatically.
- Transparency and auditability: Verify exactly why vulnerabilities are or
  aren't flagged; security teams and compliance officers can review the reasoning
  rather than trusting a vendor's black box.
- Scanner flexibility: Switch between any VEX-enabled scanner (Docker Scout,
  Trivy, Grype, etc.) without losing vulnerability context or rebuilding
  exclusion lists.
- Consistent results: VEX-enabled scanners interpret the same data the
  same way, eliminating discrepancies between tools.
- Faster workflows: Focus on real risks rather than researching why reported
  CVEs don't actually affect your deployment.

### Scanners without VEX support

Scanners that can't read VEX attestations will report vulnerabilities that don't
apply to Docker Hardened Images. This creates operational challenges:

- Manual filtering required: You'll need to maintain scanner-specific ignore
  lists to replicate what VEX statements already document.
- Higher false positive rates: Expect to see more reported vulnerabilities
  that don't represent real risks.
- Increased investigation time: Security teams spend time researching why
  CVEs don't apply instead of addressing actual vulnerabilities. With Docker
  Hardened Images, security experts at Docker manage this investigation for
  you, thoroughly vetting each justification before adding it to a VEX statement.
- CI/CD friction: Build pipelines may fail on vulnerabilities that aren't
  exploitable in your images.

### VEX-based vulnerability handling versus proprietary approaches

Docker Hardened Images use VEX attestations based on the OpenVEX open standard to document vulnerability exploitability. OpenVEX is an open standard that is recognized by government agencies such as CISA. This open standards approach differs from how some other image vendors handle vulnerabilities using proprietary methods.

#### Docker Hardened Images with VEX

The image includes signed attestations that explain which vulnerabilities don't
apply and why. Any VEX-enabled scanner can read these attestations, giving you:

- Tool flexibility: Use any scanner that supports OpenVEX (Docker Scout,
  Trivy, Grype, Wiz, etc.)
- Complete transparency: Review the exact reasoning for each vulnerability
  assessment
- Full auditability: Security teams and compliance officers can independently
  verify all vulnerability assessments and reasoning
- Historical visibility: VEX statements remain with the image, so you can
  always check vulnerability status, even for older versions

#### Proprietary vulnerability handling

Some image vendors use proprietary advisory feeds or internal databases instead
of VEX. While this may result in fewer reported vulnerabilities, it creates
significant limitations:

- Tool dependency: You must use the vendor's preferred scanning tools to see
  their vulnerability filtering, while standard scanners will still report all
  CVEs; scanners must implement proprietary feeds rather than using open
  standards that work with all images
- No transparency: Proprietary feeds act as "black boxes" - vulnerabilities
  simply disappear from vendor tools with no explanation
- Limited verifiability: Security teams have no way to independently verify
  why vulnerabilities are excluded or whether the reasoning is sound
- Maintenance challenges: If you scan older image versions with standard
  tools, you can't determine which vulnerabilities actually applied at that
  time, making long-term security tracking difficult
- Ecosystem incompatibility: Your existing security tools (SCA, policy
  engines, compliance scanners) can't access or verify the vendor's proprietary
  vulnerability data

The fundamental difference: VEX-based approaches explain vulnerability
assessments using open standards that any tool can verify and audit. Proprietary
approaches hide vulnerabilities in vendor-specific systems where the reasoning
can't be independently validated.

For Docker Hardened Images, use VEX-enabled scanners to get accurate results
that work across your entire security toolchain.

## What to expect from different scanners

When scanning Docker Hardened Images with different tools, you'll see
significant differences in reported vulnerability counts.

### What VEX-enabled scanners filter automatically

When you scan Docker Hardened Images with VEX-enabled scanners, they
automatically exclude vulnerabilities that don't apply:

- Hardware-specific vulnerabilities: Issues that only affect specific
  hardware architectures (for example, Power10 processors) that are irrelevant to
  containerized workloads.
- Unreachable code paths: CVEs in code that exists in the package but isn't
  executed in the image's runtime configuration.
- Build-time only issues: Vulnerabilities in build tools or dependencies
  that don't exist in the final runtime image.
- Temporary identifiers: Placeholder vulnerability IDs (like Debian's
  `TEMP-xxxxxxx`) that aren't intended for external tracking.

### Using scanners without VEX support

If your scanner doesn't support VEX, you'll need to manually exclude
vulnerabilities through scanner-specific mechanisms like ignore lists or policy
exceptions. This requires:

- Reviewing VEX statements from Docker Hardened Images
- Translating VEX justifications into your scanner's format
- Maintaining these exclusions as new vulnerabilities are discovered
- Repeating this process if you switch scanners or add additional scanning tools

## What's next

Learn how to
[scan Docker Hardened Images](https://docs.docker.com/dhi/how-to/scan/) with
VEX-compliant scanners.

---

# How Docker Hardened Images are tested

> See how Docker Hardened Images are automatically tested for standards compliance, functionality, and security.

# How Docker Hardened Images are tested

   Table of contents

---

Docker Hardened Images (DHIs) are designed to be secure, minimal, and
production-ready. To ensure their reliability and security, Docker employs a
comprehensive testing strategy, which you can independently verify using signed
attestations and open tooling.

Every image is tested for standards compliance, functionality, and security. The
results of this testing are embedded as signed attestations, which can be
[inspected and verified](#view-and-verify-the-test-attestation) programmatically
using the Docker Scout CLI.

## Testing strategy overview

The testing process for DHIs focuses on two main areas:

- Image standards compliance: Ensuring that each image adheres to strict size,
  security, and compatibility standards.
- Application functionality: Verifying that applications within the images
  function correctly.

## Image standards compliance

Each DHI undergoes rigorous checks to meet the following standards:

- Minimal attack surface: Images are built to be as small as possible, removing
  unnecessary components to reduce potential vulnerabilities.
- Near-zero known CVEs: Images are scanned using tools like Docker Scout to
  ensure they are free from known Common Vulnerabilities and Exposures (CVEs).
- Multi-architecture support: DHIs are built for multiple architectures
  (`linux/amd64` and `linux/arm64`) to ensure broad compatibility.
- Kubernetes compatibility: Images are tested to run seamlessly within
  Kubernetes clusters, ensuring they meet the requirements for container
  orchestration environments.

## Application functionality testing

Docker tests Docker Hardened Images to ensure they behave as expected in typical
usage scenarios. This includes verifying that:

- Applications start and run successfully in containerized environments.
- Runtime behavior aligns with upstream expectations.
- Build variants (like `-dev` images) support common development and build tasks.

The goal is to ensure that DHIs work out of the box for the most common use
cases while maintaining the hardened, minimal design.

## Automated testing and CI/CD integration

Docker integrates automated testing into its Continuous Integration/Continuous
Deployment (CI/CD) pipelines:

- Automated scans: Each image build triggers automated scans for vulnerabilities
  and compliance checks.
- Reproducible builds: Build processes are designed to be reproducible, ensuring
  consistency across different environments.
- Continuous monitoring: Docker continuously monitors for new vulnerabilities
  and updates images accordingly to maintain security standards.

## Testing attestation

Docker provides a test attestation that details the testing and validation
processes each DHI has undergone.

### View and verify the test attestation

You can view and verify this attestation using the Docker Scout CLI.

1. Use the `docker scout attest get` command with the test predicate type:
  ```console
  $ docker scout attest get \
    --predicate-type https://scout.docker.com/tests/v0.1 \
    --predicate \
    dhi.io/<image>:<tag>
  ```
  > Note
  >
  > If the image exists locally on your device, you must prefix the image name with `registry://`. For example, use
  > `registry://dhi.io/python` instead of `dhi.io/python`.
  For example:
  ```console
  $ docker scout attest get \
    --predicate-type https://scout.docker.com/tests/v0.1 \
    --predicate \
    dhi.io/python:3.13
  ```
  This contains a list of tests and their results.
  Example output:
  ```console
  v SBOM obtained from attestation, 101 packages found
      v Provenance obtained from attestation
      {
        "reportFormat": "CTRF",
        "results": {
          "summary": {
            "failed": 0,
            "passed": 1,
            "skipped": 0,
            "start": 1749216533,
            "stop": 1749216574,
            "tests": 1
          },
          "tests": [
            {
              ...
  ```
2. Verify the test attestation signature. To ensure the attestation is authentic
  and signed by Docker, run:
  ```console
  docker scout attest get \
    --predicate-type https://scout.docker.com/tests/v0.1 \
    --verify \
    dhi.io/<image>:<tag> --platform <platform>
  ```
  Example output:
  ```console
  v SBOM obtained from attestation, 101 packages found
   v Provenance obtained from attestation
   v cosign verify registry.scout.docker.com/docker/dhi-python@sha256:70c8299c4d3cb4d5432734773c45ae58d8acc2f2f07803435c65515f662136d5 \
       --key https://registry.scout.docker.com/keyring/dhi/latest.pub --experimental-oci11
     Verification for registry.scout.docker.com/docker/dhi-python@sha256:70c8299c4d3cb4d5432734773c45ae58d8acc2f2f07803435c65515f662136d5 --
     The following checks were performed on each of these signatures:
       - The cosign claims were validated
       - Existence of the claims in the transparency log was verified offline
       - The signatures were verified against the specified public key
   i Signature payload
   ...
  ```

If the attestation is valid, Docker Scout will confirm the signature and show
the matching `cosign verify` command.

To view other attestations, such as SBOMs or vulnerability reports, see [Verify
an image](https://docs.docker.com/dhi/how-to/verify/).

---

# What are hardened images and why use them?

> Learn what a hardened image is, why it matters, and how Docker Hardened Images offer stronger security, compliance, and operational efficiency.

# What are hardened images and why use them?

   Table of contents

---

In today’s diverse software environments, container images are often designed
for flexibility and broad compatibility. While that makes them ideal for many
use cases, it can also result in images that include more components than needed
for specific workloads. Docker Hardened Images take a minimal-by-design approach
to help reduce image size, limit the attack surface, and streamline security and
compliance workflows.

Hardened images solve this by minimizing what's in the container image. Less
software means fewer vulnerabilities, faster deployments, and fewer red
dashboards to chase down every week.

For platform engineers and security teams, hardened images offer a way out of
the CVE triage cycle, letting you focus on delivering secure, compliant
infrastructure without constant firefighting.

## What is a hardened image?

A hardened image is a container image that has been deliberately minimized and
secured to reduce vulnerabilities and meet stringent security and compliance
requirements. Unlike standard images, which may include non-essential components
that increase risk, hardened images are streamlined to include only what’s
needed to run your application securely.

## Benefits of hardened images

- Reduced attack surface: By removing non-essential components, hardened images
  limit potential entry points for attackers.
- Improved security posture: Regular updates and vulnerability scans help ensure
  hardened images remain secure over time.
- Compliance facilitation: Inclusion of signed metadata like SBOMs supports
  meeting regulatory and organizational compliance standards.
- Operational efficiency: Smaller image sizes lead to faster pulls, lower runtime overhead, and reduced cloud resource costs.

## What is a Docker Hardened Image?

Docker Hardened Images (DHIs) take hardened images even further by combining
minimal, secure design with enterprise-grade support and tooling. Built with
security at the core, these images are continuously maintained, tested, and
validated to meet today’s toughest software supply chain and compliance
standards.

Docker Hardened Images are secure by default, minimal by design, and maintained
so you don’t have to.

## How Docker Hardened Images differ from generic hardened images

- SLSA-compliant builds: Docker Hardened Images are built to meet [SLSA Build
  Level 3](https://docs.docker.com/dhi/core-concepts/slsa/), ensuring a tamper-resistant, verifiable,
  and auditable build process that protects against supply chain threats.
- Distroless approach: Unlike traditional base images that bundle an entire OS
  with shells, package managers, and debugging tools, [distroless
  images](https://docs.docker.com/dhi/core-concepts/distroless/) retain only the minimal OS components
  required to run your application. By excluding unnecessary tooling and
  libraries, they reduce the attack surface by up to 95% and can improve
  performance and image size.
- Continuous maintenance: All DHIs are continuously monitored and updated to
  maintain near-zero known exploitable [CVEs](https://docs.docker.com/dhi/core-concepts/cves/), helping
  your teams avoid patch fatigue and surprise alerts.
- Compliance-ready: Each image includes cryptographically signed metadata:
  - [SBOMs](https://docs.docker.com/dhi/core-concepts/sbom/) that show what's in the image
  - [VEX documents](https://docs.docker.com/dhi/core-concepts/vex/) to identify which vulnerabilities
    are actually exploitable
  - [Build provenance](https://docs.docker.com/dhi/core-concepts/provenance/) that proves how and where
    the image was built
- Compatibility-focused design: Docker Hardened Images provide a minimal runtime
  environment while maintaining compatibility with common Linux distributions.
  They remove non-essential components like shells and package managers to
  enhance security, yet retain a small base layer built on familiar distribution
  standards. Images are typically available with musl libc (Alpine-based) and
  glibc (Debian-based), supporting a broad range of application compatibility
  needs.

## Why use Docker Hardened Images?

Docker Hardened Images (DHIs) are secure by default, minimal by design, and
maintained so you don't have to. They offer:

- Images built for peace of mind: Ultra-minimal and distroless, DHIs eliminate up to 95% of the traditional container attack surface.
- No more patch panic: With continuous CVE scanning and SLA-backed remediation, Docker helps you stay ahead of threats.
- Audit-ready images: All DHIs include signed SBOMs, VEX, and provenance that support security and compliance workflows.
- Images that work with your stack: Available in Alpine and Debian flavors, DHIs drop into your existing Dockerfiles and pipelines.
- Images backed by enterprise support: Get peace of mind with Docker's support and rapid response to critical vulnerabilities.

---

# Explore Docker Hardened Images

> Learn about Docker Hardened Images, their purpose, how they are built and tested, and the shared responsibility model for security.

# Explore Docker Hardened Images

   Table of contents

---

Docker Hardened Images (DHI) are minimal, secure, and production-ready container
base and application images maintained by Docker. Designed to reduce
vulnerabilities and simplify compliance, DHI integrates easily into your
existing Docker-based workflows with little to no retooling required.

This section helps you understand what Docker Hardened Images are, how they're
built and tested, the different types available, and how responsibility is
shared between Docker and you as a user. For a complete list of DHI features and
capabilities, see
[Features](https://docs.docker.com/dhi/features/).

## Learn more about Docker Hardened Images

[What are hardened images and why use them?Learn what a hardened image is, how Docker Hardened Images are built, what sets them apart from typical base and application images, and why you should use them.](https://docs.docker.com/dhi/explore/what/)[Build processLearn how Docker builds, tests, and maintains Docker Hardened Images through an automated, security-focused pipeline.](https://docs.docker.com/dhi/explore/build-process/)[Image typesLearn about the different image types, distributions, and variants offered in the Docker Hardened Images catalog.](https://docs.docker.com/dhi/explore/available/)[Scanner integrationsDiscover which vulnerability scanners integrate with Docker Hardened Images and support open standards like OpenVEX.](https://docs.docker.com/dhi/explore/scanner-integrations/)[Image testingSee how Docker Hardened Images are automatically tested for standards compliance, functionality, and security.](https://docs.docker.com/dhi/explore/test/)[Responsibility overviewUnderstand Docker's role and your responsibilities when using Docker Hardened Images as part of your secure software supply chain.](https://docs.docker.com/dhi/explore/responsibility/)[Give feedbackDocker welcomes all contributions and feedback.](https://docs.docker.com/dhi/explore/feedback)

---

# Docker Hardened Images features

> Docker Hardened Images provide total transparency, minimal attack surface, and enterprise-grade security for every application—free and open source.

# Docker Hardened Images features

   Table of contents

---

Docker Hardened Images (DHI) are minimal, secure, and production-ready container
base and application images maintained by Docker. Designed to reduce
vulnerabilities and simplify compliance, DHI integrates easily into your
existing Docker-based workflows with little to no retooling required.

DHI provides security for everyone:

- [DHI Free](#dhi-free-features) provides core security features available to
  everyone with no licensing restrictions under Apache 2.0
- [DHI Enterprise subscription
  features](#dhi-enterprise-subscription-features) add
  SLA-backed security updates, compliance variants (like FIPS and STIG), image
  customization, and optional Extended Lifecycle Support (ELS) for post-EOL
  coverage

## DHI Free features

DHI's core features are open and free to use, share, and build on with no
licensing surprises, backed by an Apache 2.0 license.

### Security by default

- Near-zero CVEs: Continuously scanned and patched to maintain minimal known
  exploitable vulnerabilities, with no SLA-backed time commitments for non-DHI
  Enterprise users
- Minimal attack surface: Distroless variants reduce attack surface by up to 95% by removing unnecessary components
- Non-root execution: Run as non-root by default, following the principle of least privilege
- Transparent vulnerability reporting: Every CVE is visible and assessed using public data—no suppressed feeds or proprietary scoring

### Total transparency

Every image includes complete, verifiable security metadata:

- SLSA Build Level 3 provenance: Verifiable, tamper-resistant builds that meet supply chain security standards
- Signed SBOMs: Complete Software Bill of Materials for every component
- VEX statements: Vulnerability Exploitability eXchange documents provide context about known CVEs
- Cryptographic signatures: All images and metadata are signed for authenticity

### Built for developers

- Familiar foundations: Built on Alpine and Debian, requiring minimal changes to adopt
- glibc and musl support: Available in both variants for broad application compatibility
- Development and runtime variants: Use dev images for building, minimal runtime images for production
- Drop-in compatibility: Works seamlessly with existing Docker workflows, CI/CD pipelines, and tools

### Continuous maintenance

- Automatic patching: Images are rebuilt and updated when upstream security
  patches become available, with no SLA-backed time commitments for non-DHI
  Enterprise users
- Scanner integration: Direct integration with scanners and other security platforms

### Kubernetes and Helm chart support

Docker Hardened Image (DHI) charts are Docker-provided Helm charts built from
upstream sources, designed for compatibility with Docker Hardened Images. These
charts are available as OCI artifacts within the DHI catalog on Docker Hub. DHI
charts are robustly tested after building to ensure they work out-of-the-box
with Docker Hardened Images. This removes friction in migration and reduces
developer workload in implementing the charts, ensuring seamless compatibility.

Like the hardened images, DHI charts incorporate multiple layers of security
metadata to ensure transparency and trust:

- SLSA Level 3 compliance: Each chart is built with Docker's SLSA Build Level 3
  system, including a detailed build provenance, and meeting the standards set
  by the Supply-chain Levels for Software Artifacts (SLSA) framework.
- Software Bill of Materials (SBOMs): Comprehensive SBOMs are provided,
  detailing all components referenced within the chart to facilitate
  vulnerability management and compliance audits.
- Cryptographic signing: All associated metadata is cryptographically signed by
  Docker, ensuring integrity and authenticity.
- Hardened configuration: Charts automatically reference Docker hardened images,
  ensuring security in deployments.

## DHI Enterprise subscription features

For organizations with strict security requirements, regulatory demands, or
operational needs, DHI Enterprise delivers additional capabilities.

### Compliance variantsDHI Enterprise

- FIPS-enabled images: For regulated industries and government systems
- STIG-ready images: Meet DoD Security Technical Implementation Guide requirements

### SLA-backed securityDHI Enterprise

- CVE remediation SLA: 7-day SLA for critical and high severity vulnerabilities,
  with SLA commitments for other severity levels
- ELS CVE remediation SLA: Extended Lifecycle Support images have SLA commitments
  for CVE remediation, even after upstream end-of-life
- Enterprise support: Access to Docker's support team for mission-critical applications

### Customization and controlDHI Enterprise

- Build custom images: Add your own packages, tools, certificates, and configurations
- Secure build infrastructure: Customizations built on Docker's trusted infrastructure
- Full chain of trust: Customized images maintain provenance and cryptographic signing
- Automatic updates: Custom images are automatically rebuilt when base images are patched

### Extended Lifecycle SupportDHI Enterprise add-on

- Post-EOL security coverage: Continue receiving patches for years after upstream support ends
- Continuous compliance: Updated SBOMs, provenance, and signing for audit requirements
- Production continuity: Keep production running securely without forced migrations

## Learn more

- [Explore how DHI images are built and more](https://docs.docker.com/dhi/explore/)
- [Get started using DHIs](https://docs.docker.com/dhi/get-started/)
- [Contact Docker for DHI Enterprise](https://www.docker.com/pricing/contact-sales/)

---

# Docker Hardened Images quickstart

> Follow a quickstart guide to explore and run a Docker Hardened Image.

# Docker Hardened Images quickstart

   Table of contents

---

This guide shows you how to go from zero to running a Docker Hardened Image
(DHI) using a real example. At the end, you'll compare the DHI to a standard
Docker image to better understand the differences. While the steps use a
specific image as an example, they can be applied to any DHI.

> Note
>
> Docker Hardened Images are freely available to everyone with no subscription
> required, no usage restrictions, and no vendor lock-in. You can upgrade to a
> DHI Enterprise subscription when you require enterprise features like FIPS or
> STIG compliance variants, customization capabilities, or SLA-backed support.

## Step 1: Find an image to use

1. Go to the Hardened Images catalog in [Docker
  Hub](https://hub.docker.com/hardened-images/catalog).
2. Use the search bar or filters to find an image (e.g., `python`, `node`,
  `golang`). For this guide, use the Python image as an example.
3. Select the Python repository to view its details.

Continue to the next step to pull and run the image. To dive deeper into exploring
images see [Explore Docker Hardened Images](https://docs.docker.com/dhi/how-to/explore/).

## Step 2: Pull and run the image

You can pull and run a DHI like any other Docker image. Note that Docker Hardened
Images are designed to be minimal and secure, so they may not include all the
tools or libraries you expect in a typical image. You can view the typical
differences in [Considerations when adopting
DHIs](https://docs.docker.com/dhi/how-to/use/#considerations-when-adopting-dhis).

> Tip
>
> On every repository page in the DHI catalog, you'll find instructions for
> pulling and scanning the image by selecting **Use this image**.

The following example demonstrates that you can run the Python image and execute
a simple Python command just like you would with any other Docker image:

1. Open a terminal and sign in to the Docker Hardened Images registry using your
  Docker ID credentials.
  ```console
  $ docker login dhi.io
  ```
2. Pull the image:
  ```console
  $ docker pull dhi.io/python:3.13
  ```
3. Run the image to confirm everything works:
  ```console
  $ docker run --rm dhi.io/python:3.13 python -c "print('Hello from DHI')"
  ```
  This starts a container from the `python:3.13` image and runs a simple
  Python script that prints `Hello from DHI`.

To dive deeper into using images, see:

- [Use a Docker Hardened Image](https://docs.docker.com/dhi/how-to/use/) for general usage
- [Use in Kubernetes](https://docs.docker.com/dhi/how-to/k8s/) for Kubernetes deployments
- [Use a Helm chart](https://docs.docker.com/dhi/how-to/helm/) for deploying with Helm

## Step 3: Compare with the other images

You can quickly compare DHIs with other images to see the security
improvements and differences. This comparison helps you understand the value of
using hardened images.

Run the following command to see a summary comparison between the Docker
Hardened Image for Python and the non-hardened Docker Official Image for Python
from Docker Hub:

```console
$ docker scout compare dhi.io/python:3.13 \
    --to python:3.13 \
    --platform linux/amd64 \
    --ignore-unchanged \
    2>/dev/null | sed -n '/## Overview/,/^  ## /p' | head -n -1
```

Example output:

```plaintext
## Overview

                      │                    Analyzed Image                     │               Comparison Image
  ────────────────────┼───────────────────────────────────────────────────────┼───────────────────────────────────────────────
    Target            │  dhi.io/python:3.13                                   │  python:3.13
      digest          │  c215e9da9f84                                         │  7f48e892134c
      tag             │  3.13                                                 │  3.13
      platform        │ linux/amd64                                           │ linux/amd64
      provenance      │ https://github.com/docker-hardened-images/definitions │ https://github.com/docker-library/python.git
                      │  77a629b3d0db035700206c2a4e7ed904e5902ea8             │  3f2d7e4c339ab883455b81a873519f1d0f2cd80a
      vulnerabilities │    0C     0H     0M     0L                            │    0C     1H     5M   141L     2?
                      │           -1     -5   -141     -2                     │
      size            │ 35 MB (-377 MB)                                       │ 412 MB
      packages        │ 80 (-530)                                             │ 610
                      │                                                       │
```

> Note
>
> This is example output. Your results may vary depending on newly discovered
> CVEs and image updates.
>
>
>
> Docker maintains near-zero CVEs in Docker Hardened Images. For DHI Enterprise
> subscriptions, when new CVEs are discovered, the CVEs are remediated within
> the industry-leading SLA timeframe. Learn more about the [SLA-backed security
> features](https://docs.docker.com/dhi/features/#sla-backed-security).

This comparison shows that the Docker Hardened Image:

- Removes vulnerabilities: 1 high, 5 medium, 141 low, and 2 unspecified severity CVEs removed
- Reduces size: From 412 MB down to 35 MB (91% reduction)
- Minimizes packages: From 610 packages down to 80 (87% reduction)

To dive deeper into comparing images see [Compare Docker Hardened Images](https://docs.docker.com/dhi/how-to/compare/).

## What's next

You've pulled and run your first Docker Hardened Image. Here are a few ways to keep going:

- [Migrate existing applications to DHIs](https://docs.docker.com/dhi/migration/migrate-with-ai/): Use
  Docker's AI assistant to update your Dockerfiles to use Docker Hardened Images
  as the base.
- [Start a trial](https://hub.docker.com/hardened-images/start-free-trial) to
  explore the benefits of a DHI Enterprise subscription, such as access to FIPS
  and STIG variants, customized images, and SLA-backed updates.
- [Mirror a repository](https://docs.docker.com/dhi/how-to/mirror/): After subscribing to DHI Enterprise
  or starting a trial, learn how to mirror a DHI repository to enable
  customization, access compliance variants, and get SLA-backed updates.
- [Verify DHIs](https://docs.docker.com/dhi/how-to/verify/): Use tools like
  [Docker Scout](https://docs.docker.com/scout/) or
  Cosign to inspect and verify signed attestations, like SBOMs and provenance.
- [Scan DHIs](https://docs.docker.com/dhi/how-to/scan/): Analyze the image with Docker
  Scout or other scanners to identify known CVEs.

---

# Compare Docker Hardened Images

> Learn how to compare Docker Hardened Images with other container images to evaluate security improvements and differences.

# Compare Docker Hardened Images

   Table of contents

---

Docker Hardened Images (DHIs) are designed to provide enhanced security,
minimized attack surfaces, and production-ready foundations for your
applications. Comparing a DHI to a standard image helps you understand the
security improvements, package differences, and overall benefits of adopting
hardened images.

This page explains how to use Docker Scout to compare a Docker Hardened Image
with another image, such as a Docker Official Image (DOI) or a custom image, to
evaluate differences in vulnerabilities, packages, and configurations.

## Compare images using Docker Scout

Docker Scout provides a built-in comparison feature that lets you analyze the
differences between two images. This is useful for:

- Evaluating the security improvements when migrating from a standard image to a
  DHI
- Understanding package and vulnerability differences between image variants
- Assessing the impact of customizations or updates

### Basic comparison

To compare a Docker Hardened Image with another image, use the
[docker scout compare](https://docs.docker.com/reference/cli/docker/scout/compare/) command:

```console
$ docker scout compare dhi.io/<image>:<tag> \
    --to <comparison-image>:<tag> \
    --platform <platform>
```

For example, to compare a DHI Node.js image with the official Node.js image:

```console
$ docker scout compare dhi.io/node:22-debian13 \
    --to node:22 \
    --platform linux/amd64
```

This command provides a detailed comparison including:

- Vulnerability differences (CVEs added, removed, or changed)
- Package differences (packages added, removed, or updated)
- Overall security posture improvements

### Filter unchanged packages

To focus only on the differences and ignore unchanged packages, use the
`--ignore-unchanged` flag:

```console
$ docker scout compare dhi.io/node:22-debian13 \
    --to node:22 \
    --platform linux/amd64 \
    --ignore-unchanged
```

This output highlights only the packages and vulnerabilities that differ between
the two images, making it easier to identify the security improvements and
changes.

### Show overview only

For a concise overview of the comparison results, you can extract just the
overview section using standard shell tools:

```console
$ docker scout compare dhi.io/node:22-debian13 \
    --to node:22 \
    --platform linux/amd64 \
    --ignore-unchanged \
    2>/dev/null | sed -n '/## Overview/,/^  ## /p' | head -n -1
```

The result is a clean summary showing the key differences between the two
images. Example output:

```console
## Overview

                      │                    Analyzed Image                     │              Comparison Image
  ────────────────────┼───────────────────────────────────────────────────────┼─────────────────────────────────────────────
    Target            │  dhi.io/node:22-debian13                              │  node:22
      digest          │  55d471f61608                                         │  9ee3220f602f
      tag             │  22-debian13                                          │  22
      platform        │ linux/amd64                                           │ linux/amd64
      provenance      │ https://github.com/docker-hardened-images/definitions │ https://github.com/nodejs/docker-node.git
                      │  9fe491f53122b84eebba81e13f20157c18c10de2             │  bf78d7603fbea92cd3652edb3b2edadd6f5a3fe8
      vulnerabilities │    0C     0H     0M     0L                            │    0C     1H     3M   153L     4?
                      │           -1     -3   -153     -4                     │
      size            │ 41 MB (-367 MB)                                       │ 408 MB
      packages        │ 19 (-726)                                             │ 745
                      │                                                       │
```

## Interpret comparison results

The comparison output includes the following sections.

### Overview

The overview section provides high-level statistics about both images:

- Target and comparison image details (digest, tag, platform, provenance)
- Vulnerability counts for each image
- Size comparison
- Package counts

Look for:

- Vulnerability reductions (negative numbers in the delta row)
- Size reductions showing storage efficiency
- Package count reductions indicating a minimal attack surface

### Environment Variables

The environment variables section shows environment variables that differ between
the two images, prefixed with `+` for added or `-` for removed.

Look for:

- Removed environment variables that may have been necessary for your specific use-case

### Labels

The labels section displays labels that differ between the two images, prefixed
with `+` for added or `-` for removed.

### Packages and Vulnerabilities

The packages and vulnerabilities section lists all package differences and their
associated security vulnerabilities. Packages are prefixed with:

- `-` for packages removed from the target image (not present in the compared image)
- `+` for packages added to the target image (not present in the base image)
- `↑` for packages upgraded in the target image
- `↓` for packages downgraded in the target image

For packages with associated vulnerabilities, the CVEs are listed with their
severity levels and identifiers.

Look for:

- Removed packages and vulnerabilities: Indicates a reduced attack surface in the DHI
- Added packages: May indicate DHI-specific tooling or dependencies
- Upgraded packages: Shows version updates that may include security fixes

## When to compare images

### Evaluate migration benefits

Before migrating from a Docker Official Image to a DHI, compare them to
understand the security improvements. For example:

```console
$ docker scout compare dhi.io/python:3.13 \
    --to python:3.13 \
    --platform linux/amd64 \
    --ignore-unchanged
```

This helps justify the migration by showing concrete vulnerability reductions
and package minimization.

### Assess customization impact

After customizing a DHI, compare the customized version with the original to
ensure you haven't introduced new vulnerabilities. For example:

```console
$ docker scout compare <your-namespace>/dhi-python:3.13-custom \
    --to dhi.io/python:3.13 \
    --platform linux/amd64
```

### Track updates over time

Compare different versions of the same DHI to see what changed between releases. For example:

```console
$ docker scout compare dhi.io/node:22-debian13 \
    --to dhi.io/node:20-debian12 \
    --platform linux/amd64 \
    --ignore-unchanged
```
