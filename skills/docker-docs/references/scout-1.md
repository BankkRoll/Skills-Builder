# Advisory database sources and matching service and more

# Advisory database sources and matching service

> More details on the advisory database and CVE-to-package matching service behind Docker Scout analysis.

# Advisory database sources and matching service

   Table of contents

---

Reliable information sources are key for Docker Scout's ability to
surface relevant and accurate assessments of your software artifacts.
Given the diversity of sources and methodologies in the industry,
discrepancies in vulnerability assessment results can and do happen.
This page describes how the Docker Scout advisory database
and its CVE-to-package matching approach works to deal with these discrepancies.

## Advisory database sources

Docker Scout aggregates vulnerability data from multiple sources.
The data is continuously updated to ensure that your security posture
is represented using the latest available information, in real-time.

Docker Scout uses the following package repositories and security trackers:

- [AlmaLinux Security Advisory](https://errata.almalinux.org/)
- [Alpine secdb](https://secdb.alpinelinux.org/)
- [Amazon Linux Security Center](https://alas.aws.amazon.com/)
- [Bitnami Vulnerability Database](https://github.com/bitnami/vulndb)
- [CISA Known Exploited Vulnerability Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
- [CISA Vulnrichment](https://github.com/cisagov/vulnrichment)
- [Chainguard Security Feed](https://packages.cgr.dev/chainguard/osv/all.json)
- [Debian Security Bug Tracker](https://security-tracker.debian.org/tracker/)
- [Exploit Prediction Scoring System (EPSS)](https://api.first.org/epss/)
- [GitHub Advisory Database](https://github.com/advisories/)
- [GitLab Advisory Database](https://gitlab.com/gitlab-org/advisories-community/)
- [Golang VulnDB](https://github.com/golang/vulndb)
- [National Vulnerability Database](https://nvd.nist.gov/)
- [Oracle Linux Security](https://linux.oracle.com/security/)
- [Photon OS 3.0 Security Advisories](https://github.com/vmware/photon/wiki/Security-Updates-3)
- [Python Packaging Advisory Database](https://github.com/pypa/advisory-database)
- [RedHat Security Data](https://www.redhat.com/security/data/metrics/)
- [Rocky Linux Security Advisory](https://errata.rockylinux.org/)
- [RustSec Advisory Database](https://github.com/rustsec/advisory-db)
- [SUSE Security CVRF](http://ftp.suse.com/pub/projects/security/cvrf/)
- [Ubuntu CVE Tracker](https://people.canonical.com/~ubuntu-security/cve/)
- [Wolfi Security Feed](https://packages.wolfi.dev/os/security.json)
- [inTheWild, a community-driven open database of vulnerability exploitation](https://github.com/gmatuz/inthewilddb)

When you enable Docker Scout for your Docker organization,
a new database instance is provisioned on the Docker Scout platform.
The database stores the Software Bill of Materials (SBOM) and other metadata about your images.
When a security advisory has new information about a vulnerability,
your SBOM is cross-referenced with the CVE information to detect how it affects you.

For more details on how image analysis works, see the
[image analysis page](https://docs.docker.com/scout/explore/analysis/).

## Severity and scoring priority

Docker Scout uses two main principles when determining severity and scoring for
CVEs:

- Source priority
- CVSS version preference

For source priority, Docker Scout follows this order:

1. Vendor advisories: Scout always uses the severity and scoring data from the
  source that matches the package and version. For example, Debian data for
  Debian packages.
2. NIST scoring data: If the vendor doesn't provide scoring data for a CVE,
  Scout falls back to NIST scoring data.

For CVSS version preference, once Scout has selected a source, it prefers CVSS
v4 over v3 when both are available, as v4 is the more modern and precise scoring
model.

## Vulnerability matching

Traditional tools often rely on broad [Common Product Enumeration (CPE)](https://en.wikipedia.org/wiki/Common_Platform_Enumeration) matching,
which can lead to many false-positive results.

Docker Scout uses [Package URLs (PURLs)](https://github.com/package-url/purl-spec)
to match packages against CVEs, which yields more precise identification of vulnerabilities.
PURLs significantly reduce the chances of false positives, focusing only on genuinely affected packages.

## Supported package ecosystems

Docker Scout supports the following package ecosystems:

- .NET
- GitHub packages
- Go
- Java
- JavaScript
- PHP
- Python
- RPM
- Ruby
- `alpm` (Arch Linux)
- `apk` (Alpine Linux)
- `deb` (Debian Linux and derivatives)

---

# Data collection and storage in Docker Scout

> How Docker Scout handles image metadata

# Data collection and storage in Docker Scout

   Table of contents

---

Docker Scout's image analysis works by collecting metadata from the container
images that you analyze. This metadata is stored on the Docker Scout platform.

## Data transmission

This section describes the data that Docker Scout collects and sends to the
platform.

### Image metadata

Docker Scout collects the following image metadata:

- Image creation timestamp
- Image digest
- Ports exposed by the image
- Environment variable names and values
- Name and value of image labels
- Order of image layers
- Hardware architecture
- Operating system type and version
- Registry URL and type

Image digests are created for each layer of an image when the image is built
and pushed to a registry. They are SHA256 digests of the contents of a layer.
Docker Scout doesn't create the digests; they're read from the image manifest.

The digests are matched against your own private images and Docker's database
of public images to identify images that share the same layers. The image that
shares most of the layers is considered a base image match for the image that's
currently being analyzed.

### SBOM metadata

Software Bill of Material (SBOM) metadata is used to match package types
and versions with vulnerability data to infer whether an image is affected.
When the Docker Scout platform receives information from security advisories
about new CVEs or other risk factors, such as leaked secrets, it cross-references
this information with the SBOM. If there's a match, Docker Scout displays the
results in the user interfaces where Docker Scout data is surfaced,
such as the Docker Scout Dashboard and in Docker Desktop.

Docker Scout collects the following SBOM metadata:

- Package URLs (PURL)
- Package author and description
- License IDs
- Package name and namespace
- Package scheme and size
- Package type and version
- Filepath within the image
- The type of direct dependency
- Total package count

The PURLs in Docker Scout follow the
[purl-spec](https://github.com/package-url/purl-spec) specification. Package
information is derived from the contents of image, including OS-level programs
and packages, and application-level packages such as maven, npm, and so on.

### Environment metadata

If you integrate Docker Scout with your runtime environment via the
[Sysdig integration](https://docs.docker.com/scout/integrations/environment/sysdig/),
Docker Scout collects the following data points about your deployments:

- Kubernetes namespace
- Workload name
- Workload type (for example, DaemonSet)

### Local analysis

For images analyzed locally on a developer's machine, Docker Scout only
transmits PURLs and layer digests. This data isn't persistently stored on the
Docker Scout platform; it's only used to run the analysis.

### Provenance

For images with
[provenance attestations](https://docs.docker.com/build/metadata/attestations/slsa-provenance/),
Docker Scout stores the following data in addition to the SBOM:

- Materials
- Base image
- VCS information
- Dockerfile

## Data storage

For the purposes of providing the Docker Scout service, data is stored using:

- Amazon Web Services (AWS) on servers located in US East
- Google Cloud Platform (GCP) on servers located in US East

Data is used according to the processes described at
[docker.com/legal](https://www.docker.com/legal/) to provide the key
capabilities of Docker Scout.

---

# Docker Scout image analysis

> Docker Scout image analysis provides a detailed view into the composition of your images and the vulnerabilities that they contain

# Docker Scout image analysis

   Table of contents

---

When you activate image analysis for a repository,
Docker Scout automatically analyzes new images that you push to that repository.

Image analysis extracts the Software Bill of Material (SBOM)
and other image metadata,and evaluates it against vulnerability data from
[security advisories](https://docs.docker.com/scout/deep-dive/advisory-db-sources/).

If you run image analysis as a one-off task using the CLI or Docker Desktop,
Docker Scout won't store any data about your image.
If you enable Docker Scout for your container image repositories however,
Docker Scout saves a metadata snapshot of your images after the analysis.
As new vulnerability data becomes available, Docker Scout recalibrates the analysis using the metadata snapshot, which means your security status for images is updated in real-time.
This dynamic evaluation means there's no need to re-analyze images when new CVE information is disclosed.

Docker Scout image analysis is available by default for Docker Hub repositories.
You can also integrate third-party registries and other services. To learn more,
see
[Integrating Docker Scout with other systems](https://docs.docker.com/scout/integrations/).

## Activate Docker Scout on a repository

Docker Personal comes with 1 Scout-enabled repository. You can upgrade your
Docker subscription if you need additional repositories.
See [Subscriptions and features](https://www.docker.com/pricing/)
to learn how many Scout-enabled
repositories come with each subscription tier.

Before you can activate image analysis on a repository in a third-party registry,
the registry must be integrated with Docker Scout for your Docker organization.
Docker Hub is integrated by default. For more information, see
See
[Container registry integrations](https://docs.docker.com/scout/integrations/#container-registries)

> Note
>
> You must have the **Editor** or **Owner** role in the Docker organization to
> activate image analysis on a repository.

To activate image analysis:

1. Go to [Repository settings](https://scout.docker.com/settings/repos) in the Docker Scout Dashboard.
2. Select the repositories that you want to enable.
3. Select **Enable image analysis**.

If your repositories already contain images,
Docker Scout pulls and analyzes the latest images automatically.

## Analyze registry images

To trigger image analysis for an image in a registry, push the image to a
registry that's integrated with Docker Scout, to a repository where image
analysis is activated.

> Note
>
> Image analysis on the Docker Scout platform has a maximum image file size
> limit of 10 GB, unless the image has an SBOM attestation.
> See [Maximum image size](#maximum-image-size).

1. Sign in with your Docker ID, either using the `docker login` command or the
  **Sign in** button in Docker Desktop.
2. Build and push the image that you want to analyze.
  ```console
  $ docker build --push --tag <org>/<image:tag> --provenance=true --sbom=true .
  ```
  Building with the `--provenance=true` and `--sbom=true` flags attaches
  [build attestations](https://docs.docker.com/build/metadata/attestations/) to the image. Docker
  Scout uses attestations to provide more fine-grained analysis results.
  > Note
  >
  > The default `docker` driver only supports build attestations if you use the
  > [containerd image store](https://docs.docker.com/desktop/features/containerd/).
3. Go to the [Images page](https://scout.docker.com/reports/images) in the Docker Scout Dashboard.
  The image appears in the list shortly after you push it to the registry.
  It may take a few minutes for the analysis results to appear.

## Analyze images locally

You can analyze local images with Docker Scout using Docker Desktop or the
`docker scout` commands for the Docker CLI.

### Docker Desktop

> Note
>
> Docker Desktop background indexing supports images up to 10 GB in size.
> See [Maximum image size](#maximum-image-size).

To analyze an image locally using the Docker Desktop GUI:

1. Pull or build the image that you want to analyze.
2. Go to the **Images** view in the Docker Dashboard.
3. Select one of your local images in the list.
  This opens the [Image details view](https://docs.docker.com/scout/explore/image-details-view/), showing a
  breakdown of packages and vulnerabilities found by the Docker Scout analysis
  for the image you selected.

### CLI

The `docker scout` CLI commands provide a command line interface for using Docker
Scout from your terminal.

- `docker scout quickview`: summary of the specified image, see [Quickview](#quickview)
- `docker scout cves`: local analysis of the specified image, see [CVEs](#cves)
- `docker scout compare`: analyzes and compares two images

By default, the results are printed to standard output.
You can also export results to a file in a structured format,
such as Static Analysis Results Interchange Format (SARIF).

#### Quickview

The `docker scout quickview` command provides an overview of the
vulnerabilities found in a given image and its base image.

```console
$ docker scout quickview traefik:latest
    ✓ SBOM of image already cached, 311 packages indexed

  Your image  traefik:latest  │    0C     2H     8M     1L
  Base image  alpine:3        │    0C     0H     0M     0L
```

If your the base image is out of date, the `quickview` command also shows how
updating your base image would change the vulnerability exposure of your image.

```console
$ docker scout quickview postgres:13.1
    ✓ Pulled
    ✓ Image stored for indexing
    ✓ Indexed 187 packages

  Your image  postgres:13.1                 │   17C    32H    35M    33L
  Base image  debian:buster-slim            │    9C    14H     9M    23L
  Refreshed base image  debian:buster-slim  │    0C     1H     6M    29L
                                            │    -9    -13     -3     +6
  Updated base image  debian:stable-slim    │    0C     0H     0M    17L
                                            │    -9    -14     -9     -6
```

#### CVEs

The `docker scout cves` command gives you a complete view of all the
vulnerabilities in the image. This command supports several flags that lets you
specify more precisely which vulnerabilities you're interested in, for example,
by severity or package type:

```console
$ docker scout cves --format only-packages --only-vuln-packages \
  --only-severity critical postgres:13.1
    ✓ SBOM of image already cached, 187 packages indexed
    ✗ Detected 10 vulnerable packages with a total of 17 vulnerabilities

     Name            Version         Type        Vulnerabilities
───────────────────────────────────────────────────────────────────────────
  dpkg        1.19.7                 deb      1C     0H     0M     0L
  glibc       2.28-10                deb      4C     0H     0M     0L
  gnutls28    3.6.7-4+deb10u6        deb      2C     0H     0M     0L
  libbsd      0.9.1-2                deb      1C     0H     0M     0L
  libksba     1.3.5-2                deb      2C     0H     0M     0L
  libtasn1-6  4.13-3                 deb      1C     0H     0M     0L
  lz4         1.8.3-1                deb      1C     0H     0M     0L
  openldap    2.4.47+dfsg-3+deb10u5  deb      1C     0H     0M     0L
  openssl     1.1.1d-0+deb10u4       deb      3C     0H     0M     0L
  zlib        1:1.2.11.dfsg-1        deb      1C     0H     0M     0L
```

For more information about these commands and how to use them, refer to the CLI
reference documentation:

- [docker scout quickview](https://docs.docker.com/reference/cli/docker/scout/quickview/)
- [docker scout cves](https://docs.docker.com/reference/cli/docker/scout/cves/)

## Vulnerability severity assessment

Docker Scout assigns a severity rating to vulnerabilities based on
vulnerability data from
[advisory sources](https://docs.docker.com/scout/deep-dive/advisory-db-sources/).
Advisories are ranked and prioritized depending on the type of package that's
affected by a vulnerability. For example, if a vulnerability affects an OS
package, the severity level assigned by the distribution maintainer is
prioritized.

If the preferred advisory source has assigned a severity rating to a CVE, but
not a CVSS score, Docker Scout falls back to displaying a CVSS score from
another source. The severity rating from the preferred advisory and the CVSS
score from the fallback advisory are displayed together. This means a
vulnerability can have a severity rating of `LOW` with a CVSS score of 9.8, if
the preferred advisory assigns a `LOW` rating but no CVSS score, and a fallback
advisory assigns a CVSS score of 9.8.

Vulnerabilities that haven't been assigned a CVSS score in any source are
categorized as **Unspecified** (U).

Docker Scout doesn't implement a proprietary vulnerability metrics system. All
metrics are inherited from security advisories that Docker Scout integrates
with. Advisories may use different thresholds for classifying vulnerabilities,
but most of them adhere to the CVSS v3.0 specification, which maps CVSS scores
to severity ratings according to the following table:

| CVSS score | Severity rating |
| --- | --- |
| 0.1 – 3.9 | Low(L) |
| 4.0 – 6.9 | Medium(M) |
| 7.0 – 8.9 | High(H) |
| 9.0 – 10.0 | Critical(C) |

For more information, see [Vulnerability Metrics (NIST)](https://nvd.nist.gov/vuln-metrics/cvss).

Note that, given the advisory prioritization and fallback mechanism described
earlier, severity ratings displayed in Docker Scout may deviate from this
rating system.

## Maximum image size

Image analysis on the Docker Scout platform, and analysis triggered by background
indexing in Docker Desktop, has an image file size limit of 10 GB (uncompressed).
To analyze images larger than that:

- Attach an
  [SBOM attestation](https://docs.docker.com/build/metadata/attestations/sbom/) at build-time. When an image includes an SBOM attestation, Docker Scout uses it instead of generating one, so the 10 GB limit doesn’t apply.
- Alternatively, you can use the [CLI](#cli) to analyze the image locally. The 10 GB limit doesn’t apply when using the CLI. If the image includes an SBOM attestation, the CLI uses it to complete the analysis faster.

---

# Dashboard

> The Docker Scout Dashboard helps review and share the analysis of images.

# Dashboard

   Table of contents

---

The [Docker Scout Dashboard](https://scout.docker.com/) helps you share the
analysis of images in an organization with your team. Developers can now see an
overview of their security status across all their images from Docker Hub, and
get remediation advice at their fingertips. It helps team members in roles such
as security, compliance, and operations to know what vulnerabilities and issues
they need to focus on.

## Overview

![A screenshot of the Docker Scout Dashboard overview](https://docs.docker.com/scout/images/dashboard-overview.webp)  ![A screenshot of the Docker Scout Dashboard overview](https://docs.docker.com/scout/images/dashboard-overview.webp)

The **Overview** tab provides a summary for the repositories in the selected
organization.

At the top of this page, you can select which **Environment** to view.
By default, the most recently pushed images are shown. To learn more about
environments, see
[Environment monitoring](https://docs.docker.com/scout/integrations/environment/).

The **Policy** boxes show your current compliance rating for each policy, and a
trend indication for the selected environment. The trend describes the policy
delta for the most recent images compared to the previous version.
For more information about policies, see
[Policy Evaluation](https://docs.docker.com/scout/policy/).

The vulnerability chart shows the total number of vulnerabilities for images in
the selected environment over time. You can configure the timescale for the
chart using the drop-down menu.

Use the header menu at the top of the website to access the different main
sections of the Docker Scout Dashboard:

- **Policies**: shows the policy compliance for the organization, see [Policies](#policies)
- **Images**: lists all Docker Scout-enabled repositories in the organization, see [Images](#images)
- **Base images**: lists all base images used by repositories in an organization
- **Packages**: lists all packages across repositories in the organization
- **Vulnerabilities**: lists all CVEs in the organization's images, see [Vulnerabilities](#vulnerabilities)
- **Integrations**: create and manage third-party integrations, see [Integrations](#integrations)
- **Settings**: manage repository settings, see [Settings](#settings)

## Policies

The **Policies** view shows a breakdown of policy compliance for all of the
images in the selected organization and environment. You can use the **Image**
drop-down menu to view a policy breakdown for a specific environment.

For more information about policies, see
[Policy Evaluation](https://docs.docker.com/scout/policy/).

## Images

The **Images** view shows all images in Scout-enabled repositories for the selected environment.
You can filter the list by selecting a different environment, or by repository name using the text filter.

![Screenshot of the images view](https://docs.docker.com/scout/images/dashboard-images.webp)  ![Screenshot of the images view](https://docs.docker.com/scout/images/dashboard-images.webp)

For each repository, the list displays the following details:

- The repository name (image reference without the tag or digest)
- The most recent tag of the image in the selected environment
- Operating systems and architectures for the most recent tag
- Vulnerabilities status for the most recent tag
- Policy status for the most recent tag

Selecting a repository link takes you to a list of all images in that repository that have been analyzed.
From here you can view the full analysis results for a specific image,
and compare tags to view the differences in packages and vulnerabilities

Selecting an image link takes you to a details view for the selected tag or digest.
This view contains two tabs that detail the composition and policy compliance for the image:

- **Policy status** shows the policy evaluation results for the selected image.
  Here you also have links for details about the policy violations.
  For more information about policy, see
  [Policy Evaluation](https://docs.docker.com/scout/policy/).
- **Image layers** shows a breakdown of the image analysis results.
  You can get a complete view of the vulnerabilities your image contains
  and understand how they got in.

## Vulnerabilities

The **Vulnerabilities** view shows a list of all vulnerabilities for images in the organization.
This list includes details about CVE such as the severity and Common Vulnerability Scoring System (CVSS) score,
as well as whether there's a fix version available.
The CVSS score displayed here is the highest score out of all available
[sources](https://docs.docker.com/scout/deep-dive/advisory-db-sources/).

Selecting the links on this page opens the vulnerability details page,
This page is a publicly visible page, and shows detailed information about a CVE.
You can share the link to a particular CVE description with other people
even if they're not a member of your Docker organization or signed in to Docker Scout.

If you are signed in, the **My images** tab on this page lists all of your images
affected by the CVE.

## Integrations

The **Integrations** page lets you create and manage your Docker Scout
integrations, such as environment integrations and registry integrations. For
more information on how to get started with integrations, see
[Integrating Docker Scout with other systems](https://docs.docker.com/scout/integrations/).

## Settings

The settings menu in the Docker Scout Dashboard contains:

- [Repository settings](#repository-settings) for enabling and disabling repositories
- [Notifications](#notification-settings) for managing your notification preferences for Docker Scout.

### Repository settings

When you enable Docker Scout for a repository,
Docker Scout analyzes new tags automatically when you push to that repository.
To enable repositories in Amazon ECR, Azure ACR, or other third-party registries,
you first need to integrate them.
See
[Container registry integrations](https://docs.docker.com/scout/integrations/#container-registries)

### Notification settings

The [Notification settings](https://scout.docker.com/settings/notifications)
page is where you can change the preferences for receiving notifications from
Docker Scout. Notification settings are personal, and changing notification
settings only affects your personal account, not the entire organization.

The purpose of notifications in Docker Scout is to raise awareness about
upstream changes that affect you. Docker Scout will notify you about when a new
vulnerability is disclosed in a security advisory, and it affects one or more
of your images. You will not receive notifications about changes to
vulnerability exposure or policy compliance as a result of pushing a new image.

> Note
>
> Notifications are only triggered for the *last pushed* image tags for each
> repository. "Last pushed" refers to the image tag that was most recently
> pushed to the registry and analyzed by Docker Scout. If the last pushed image
> is not affected by a newly disclosed CVE, then no notification will be
> triggered.

The available notification settings are:

- **Repository scope**
  Here you can select whether you want to enable notifications for all
  repositories, or only for specific repositories. These settings apply to the
  currently selected organization, and can be changed for each organization you
  are a member of.
  - **All repositories**: select this option to receive notifications for all
    repositories that you have access to.
  - **Specific repositories**: select this option to receive notifications for
    specific repositories. You can then enter the names of repositories you
    want to receive notifications for.
- **Delivery preferences**
  These settings control how you receive notifications from Docker Scout. They
  apply to all organizations that you're a member of.
  - **Notification pop-ups**: select this check-box to receive notification
    pop-up messages in the Docker Scout Dashboard.
  - **OS notifications**: select this check-box to receive OS-level notifications
    from your browser if you have the Docker Scout Dashboard open in a browser
    tab.
  To enable OS notifications, Docker Scout needs permissions to send
  notifications using the browser API.

From this page, you can also go to the settings for Team collaboration
integrations, such as the
[Slack](https://docs.docker.com/scout/integrations/team-collaboration/slack/)
integration.

You can also configure your notification settings in Docker Desktop by going
to **Settings** > **Notifications**.

---

# Manage vulnerability exceptions

> Exceptions let you provide additional context and documentation for how vulnerabilities affect your artifacts, and provides the ability to suppress non-applicable vulnerabilities

# Manage vulnerability exceptions

   Table of contents

---

Vulnerabilities found in container images sometimes need additional context.
Just because an image contains a vulnerable package, it doesn't mean that the
vulnerability is exploitable. **Exceptions** in Docker Scout lets you
acknowledge accepted risks or address false positives in image analysis.

By negating non-applicable vulnerabilities, you can make it easier for yourself
and downstream consumers of your images to understand the security implications
of a vulnerability in the context of an image.

In Docker Scout, exceptions are automatically factored into the results.
If an image contains an exception that flags a CVE as non-applicable,
then that CVE is excluded from analysis results.

## Create exceptions

To create an exception for an image, you can:

- Create an exception in the
  [GUI](https://docs.docker.com/scout/how-tos/create-exceptions-gui/) of
  Docker Scout Dashboard or Docker Desktop.
- Create a
  [VEX](https://docs.docker.com/scout/how-tos/create-exceptions-vex/) document and attach
  it to the image.

The recommended way to create exceptions is to use Docker Scout Dashboard or
Docker Desktop. The GUI provides a user-friendly interface for creating
exceptions. It also lets you create exceptions for multiple images, or your
entire organization, all at once.

## View exceptions

To view exceptions for images, you need to have the appropriate permissions.

- Exceptions created
  [using the GUI](https://docs.docker.com/scout/how-tos/create-exceptions-gui/)
  are visible to members of your Docker organization. Unauthenticated users or
  users who aren't members of your organization cannot see these exceptions.
- Exceptions created
  [using VEX documents](https://docs.docker.com/scout/how-tos/create-exceptions-vex/)
  are visible to anyone who can pull the image, since the VEX document is
  stored in the image manifest or on filesystem of the image.

### View exceptions in Docker Scout Dashboard or Docker Desktop

The [Exceptionstab](https://scout.docker.com/reports/vulnerabilities/exceptions)
of the Vulnerabilities page in Docker Scout Dashboard lists all exceptions for
for all images in your organization. From here, you can see more details about
each exception, the CVEs being suppressed, the images that exceptions apply to,
the type of exception and how it was created, and more.

For exceptions created using the
[GUI](https://docs.docker.com/scout/how-tos/create-exceptions-gui/),
selecting the action menu lets you edit or remove the exception.

To view all exceptions for a specific image tag:

1. Go to the [Images page](https://scout.docker.com/reports/images).
2. Select the tag that you want to inspect.
3. Open the **Exceptions** tab.

1. Open the **Images** view in Docker Desktop.
2. Open the **Hub** tab.
3. Select the tag you want to inspect.
4. Open the **Exceptions** tab.

### View exceptions in the CLI

Availability: Experimental
Requires: Docker Scout CLI
[1.15.0](https://docs.docker.com/scout/release-notes/cli/#1150) and later

Vulnerability exceptions are highlighted in the CLI when you run `docker scout cves <image>`. If a CVE is suppressed by an exception, a `SUPPRESSED` label
appears next to the CVE ID. Details about the exception are also displayed.

![SUPPRESSED label in the CLI output](https://docs.docker.com/scout/images/suppressed-cve-cli.png)  ![SUPPRESSED label in the CLI output](https://docs.docker.com/scout/images/suppressed-cve-cli.png)

> Important
>
> In order to view exceptions in the CLI, you must configure the CLI to use
> the same Docker organization that you used to create the exceptions.
>
>
>
> To configure an organization for the CLI, run:
>
>
>
> ```console
> $ docker scout configure organization <organization>
> ```
>
>
>
> Replace `<organization>` with the name of your Docker organization.
>
>
>
> You can also set the organization on a per-command basis by using the
> `--org` flag:
>
>
>
> ```console
> $ docker scout cves --org <organization> <image>
> ```

To exclude suppressed CVEs from the output, use the `--ignore-suppressed` flag:

```console
$ docker scout cves --ignore-suppressed <image>
```

---

# Image details view

> The Docker Scout image detail view analyzes images to show their hierarchy, layers, packages, and vulnerabilities

# Image details view

   Table of contents

---

The image details view shows a breakdown of the Docker Scout analysis. You can
access the image view from the Docker Scout Dashboard, the Docker Desktop
**Images** view, and from the image tag page on Docker Hub. The image details
show a breakdown of the image hierarchy (base images), image layers, packages,
and vulnerabilities.

![The image details view in Docker Desktop](https://docs.docker.com/scout/images/dd-image-view.png)  ![The image details view in Docker Desktop](https://docs.docker.com/scout/images/dd-image-view.png)

Docker Desktop first analyzes images locally, where it generates a software bill of materials (SBOM).
Docker Desktop, Docker Hub, and the Docker Scout Dashboard and CLI all use the [package URL (PURL) links](https://github.com/package-url/purl-spec)
in this SBOM to query for matching Common Vulnerabilities and Exposures (CVEs) in
[Docker Scout's advisory database](https://docs.docker.com/scout/deep-dive/advisory-db-sources/).

## Image hierarchy

The image you inspect may have one or more base images represented under
**Image hierarchy**. This means the author of the image used other images as
starting points when building the image. Often these base images are either
operating system images such as Debian, Ubuntu, and Alpine, or programming
language images such as PHP, Python, and Java.

Selecting each image in the chain lets you see which layers originate from each
base image. Selecting the **ALL** row selects all layers and base images.

One or more of the base images may have updates available, which may include
updated security patches that remove vulnerabilities from your image. Any base
images with available updates are noted to the right of **Image hierarchy**.

## Layers

A Docker image consists of layers. Image layers are listed from top to bottom,
with the earliest layer at the top and the most recent layer at the bottom.
Often, the layers at the top of the list originate from a base image, and the
layers towards the bottom added by the image author, often using
commands in a Dockerfile. Selecting a base image under **Image hierarchy**
highlights with layers originate from a base image.

Selecting individual or multiple layers filters the packages and vulnerabilities
on the right-hand side to show what the selected layers added.

## Vulnerabilities

The **Vulnerabilities** tab displays a list of vulnerabilities and exploits detected in the image. The list is grouped by package, and sorted in order of severity.

You can find further information on the vulnerability or exploit, including if a fix is available, by expanding the list item.

## Remediation recommendations

When you inspect an image in Docker Desktop or Docker Hub,
Docker Scout can provide recommendations for improving the security of that image.

### Recommendations in Docker Desktop

To view security recommendations for an image in Docker Desktop:

1. Go to the **Images** view in Docker Desktop.
2. Select the image tag that you want to view recommendations for.
3. Near the top, select the **Recommended fixes** drop-down button.

The drop-down menu lets you choose whether you want to see recommendations for
the current image or any base images used to build it:

- [Recommendations for this image](#recommendations-for-current-image)
  provides recommendations for the current image that you're inspecting.
- [Recommendations for base image](#recommendations-for-base-image) provides
  recommendations for base images used to build the image.

If the image you're viewing has no associated base images, the drop-down menu only
shows the option to view recommendations for the current image.

### Recommendations in Docker Hub

To view security recommendations for an image in Docker Hub:

1. Go to the repository page for an image where you have activated Docker Scout
  image analysis.
2. Open the **Tags** tab.
3. Select the tag that you want to view recommendations for.
4. Select the **View recommended base image fixes** button.
  This opens a window which gives you recommendations for you can improve the
  security of your image by using better base images. See
  [Recommendations for base image](#recommendations-for-base-image) for more
  details.

### Recommendations for current image

The recommendations for the current image view helps you determine whether the image
version that you're using is out of date. If the tag you're using is referencing an
old digest, the view shows a recommendation to update the tag by pulling the
latest version.

Select the **Pull new image** button to get the updated version. Check the
checkbox to remove the old version after pulling the latest.

### Recommendations for base image

The base image recommendations view contains two tabs for toggling between
different types of recommendations:

- **Refresh base image**
- **Change base image**

These base image recommendations are only actionable if you're the author of the
image you're inspecting. This is because changing the base image for an image
requires you to update the Dockerfile and re-build the image.

#### Refresh base image

This tab shows if the selected base image tag is the latest available version,
or if it's outdated.

If the base image tag used to build the current image isn't the latest, then the
delta between the two versions shows in this window. The delta information
includes:

- The tag name, and aliases, of the recommended (newer) version
- The age of the current base image version
- The age of the latest available version
- The number of CVEs affecting each version

At the bottom of the window, you also receive command snippets that you can
run to re-build the image using the latest version.

#### Change base image

This tab shows different alternative tags that you can use, and outlines the
benefits and disadvantages of each tag version. Selecting the base image shows
recommended options for that tag.

For example, if the image you're inspecting is using an old version of `debian`
as a base image, it shows recommendations for newer and more secure versions
of `debian` to use. By providing more than one alternative to choose from, you
can see for yourself how the options compare with each other, and decide which
one to use.

![Base image recommendations](https://docs.docker.com/scout/images/change-base-image.png)  ![Base image recommendations](https://docs.docker.com/scout/images/change-base-image.png)

Select a tag recommendation to see further details of the recommendation.
It shows the benefits and potential disadvantages of the tag, why it's a
recommended, and how to update your Dockerfile to use this version.
