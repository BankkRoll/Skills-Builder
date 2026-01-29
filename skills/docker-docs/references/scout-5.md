# Docker Scout health scores and more

# Docker Scout health scores

> Docker Scout health scores provide a supply chain assessment for Docker Hub images, grading them from A to F based on various security policies.

# Docker Scout health scores

   Table of contents

---

Subscription: Pro  Team  Business Availability: Beta

Docker Scout health scores provide a security assessment, and overall supply
chain health, of images on Docker Hub, helping you determine whether an image
meets established security best practices. The scores range from A to F, where
A represents the highest level of security and F the lowest, offering an
at-a-glance view of the security posture of your images.

Only users who are members of the organization that owns the repository, and
have at least “read” access to the repository, can view the health score. The
score is not visible to users outside the organization or members without
"read" access.

## Viewing health scores

To view the health score of an image in Docker Hub:

1. Go to Docker Hub and sign in.
2. Navigate to your organization's page.

In the list of repositories, you can see the health score of each repository
based on the latest pushed tag.

![Repository health score](https://docs.docker.com/scout/images/score-badges-repolist.png)  ![Repository health score](https://docs.docker.com/scout/images/score-badges-repolist.png)

To view the health score of an image in Docker Desktop:

1. Open Docker Desktop and sign in to your Docker account.
2. Navigate to the **Images** view and select the **Hub** tab.

In the list of repositories, the **Health** column displays the scores of the
different tags that have been pushed to Docker Hub.

![Repository health score](https://docs.docker.com/scout/images/score-badges-dd.png)  ![Repository health score](https://docs.docker.com/scout/images/score-badges-dd.png)

The health score badge is color-coded to indicate the overall health of the
repository:

- **Green**: A score of A or B.
- **Yellow**: A score of C.
- **Orange**: A score of D.
- **Red**: A score of E or F.
- **Gray**: An `N/A` score.

The score is also displayed on the Docker Hub page for a given repository,
along with each policy that contributed to the score.

![Scout "A" health score](https://docs.docker.com/scout/images/score-a-shiny.png)  ![Scout "A" health score](https://docs.docker.com/scout/images/score-a-shiny.png)

## Scoring system

Health scores are determined by evaluating images against Docker Scout
[policies](https://docs.docker.com/scout/policy/). These policies align with best practices for the
software supply chain.

If your image repositories are already enrolled with Docker Scout, the health
score is calculated automatically based on the policies that are enabled for
your organization. This also includes any custom policies that you have
configured.

If you're not using Docker Scout, the health scores show the compliance of your
images with the default policies, a set of supply chain rules recommended by
Docker as foundational standards for images. You can enable Docker Scout for
your organization and edit the policy configurations to get a more relevant
health score based on your specific policies.

### Scoring process

Each policy is assigned a points value based on its
[type](https://docs.docker.com/scout/policy/#policy-types). If the image is compliant
with a policy, it is awarded the points value for that policy type. The health
score of an image is calculated based on the percentage of points achieved
relative to the total possible points.

1. Policy compliance is evaluated for the image.
2. Points are awarded based on compliance with policies.
3. The points achieved percentage is calculated:
  ```text
  Percentage = (Points / Total) * 100
  ```
4. The final score is assigned based on the percentage of points achieved, as
  shown in the following table:
  | Points percentage (awarded out of total) | Score |
  | --- | --- |
  | More than 90% | A |
  | 71% to 90% | B |
  | 51% to 70% | C |
  | 31% to 50% | D |
  | 11% to 30% | E |
  | Less than 10% | F |

### N/A scores

Images can also be assigned an `N/A` score, which can happen when:

- The image is larger than 4GB (compressed size).
- The image architecture is not `linux/amd64` or `linux/arm64`.
- The image is too old and does not have fresh data for evaluation.

If you see an `N/A` score, consider the following:

- If the image is too large, try reducing the size of the image.
- If the image has an unsupported architecture, rebuild the image for a
  supported architecture.
- If the image is too old, push a new tag to trigger a fresh evaluation.

### Policy weights

Different policy types carry varying weights, which impact the score assigned
to an image during evaluation, as shown in the following table.

| Policy type | Points |
| --- | --- |
| Severity-Based Vulnerability | 20 |
| High-Profile Vulnerabilities | 20 |
| Supply Chain Attestations | 15 |
| Approved Base Images | 15 |
| Up-to-Date Base Images | 10 |
| SonarQube Quality Gates* | 10 |
| Default Non-Root User | 5 |
| Compliant Licenses | 5 |

* *This policy is not enabled by default and must be configured by the user.*

### Evaluation

Health scores are calculated for new images pushed to Docker Hub after the
feature is enabled. The health scores help you maintain high security standards
and ensure your applications are built on secure and reliable images.

### Repository scores

In addition to individual image scores (per tag or digest), each repository
receives a health score based on the latest pushed tag, providing an overall
view of the repository's security status.

### Example

For an image with a total possible score of 100 points:

- If the image only deviates from one policy, worth 5 points, its score will be
  95 out of 100. Since this score is above the 90th percentile, the image
  receives an A health score.
- If the image is non-compliant with more policies and scores 65 out of 100, it
  receives a C health score, reflecting its lower compliance.

## Improving your health score

To improve the health score of an image, take steps to ensure that the image is
compliant with the Docker Scout recommended [policies](https://docs.docker.com/scout/policy/).

1. Go to the [Docker Scout Dashboard](https://scout.docker.com/).
2. Sign in using your Docker ID.
3. Go to [Repository settings](https://scout.docker.com/settings/repos) and
  enable Docker Scout for your Docker Hub image repositories.
4. Analyze the [policy compliance](https://docs.docker.com/scout/policy/) for your repositories,
  and take actions to ensure your images are policy-compliant.

Since policies are weighted differently, prioritize the policies with the
highest scores for a greater impact on your image's overall score.

---

# View Docker Scout policy status

> The Docker Scout Dashboard and the `docker scout policy` command lets you view policy status of images.

# View Docker Scout policy status

   Table of contents

---

You can track policy status for your artifacts from the [Docker Scout
Dashboard](#dashboard), or using the [CLI](#cli).

## Dashboard

The **Overview** tab of the [Docker Scout Dashboard](https://scout.docker.com/)
displays a summary of recent changes in policy for your repositories.
This summary shows images that have seen the most change in their policy
evaluation between the most recent image and the previous image.

![Policy overview](https://docs.docker.com/scout/images/policy-overview.webp)  ![Policy overview](https://docs.docker.com/scout/images/policy-overview.webp)

### Policy status per repository

The **Images** tab shows the current policy status, and recent policy trend,
for all images in the selected environment. The **Policy status** column in the
list shows:

- Number of fulfilled policies versus the total number of policies
- Recent policy trends

![Policy status in the image list](https://docs.docker.com/scout/images/policy-image-list.webp)  ![Policy status in the image list](https://docs.docker.com/scout/images/policy-image-list.webp)

The policy trend, denoted by the directional arrows, indicates whether an image
is better, worse, or unchanged in terms of policy, compared to the previous
image in the same environment.

- The green arrow pointing upwards shows the number of policies that got better
  in the latest pushed image.
- The red arrow pointing downwards shows the number of policies that got worse
  in the latest pushed image.
- The bidirectional gray arrow shows the number of policies that were unchanged
  in the latest version of this image.

If you select a repository, you can open the **Policy** tab for a detailed
description of the policy delta for the most recently analyzed image and its
predecessor.

### Detailed results and remediation

To view the full evaluation results for an image, navigate to the image tag in
the Docker Scout Dashboard and open the **Policy** tab. This shows a breakdown
for all policy violations for the current image.

![Detailed Policy Evaluation results](https://docs.docker.com/scout/images/policy-detailed-results.webp)  ![Detailed Policy Evaluation results](https://docs.docker.com/scout/images/policy-detailed-results.webp)

This view also provides recommendations on how to improve improve policy status
for violated policies.

![Policy details in the tag view](https://docs.docker.com/scout/images/policy-tag-view.webp)  ![Policy details in the tag view](https://docs.docker.com/scout/images/policy-tag-view.webp)

For vulnerability-related policies, the policy details view displays the fix
version that removes the vulnerability, when a fix version is available. To fix
the issue, upgrade the package version to the fix version.

For licensing-related policies, the list shows all packages whose license
doesn't meet the policy criteria. To fix the issue, find a way to remove the
dependency to the violating package, for example by looking for an alternative
package distributed under a more appropriate license.

## CLI

To view policy status for an image from the CLI, use the `docker scout policy`
command.

```console
$ docker scout policy \
  --org dockerscoutpolicy \
  --platform linux/amd64 \
  dockerscoutpolicy/email-api-service:0.0.2

    ✓ Pulled
    ✓ Policy evaluation results found

​## Overview
​
​             │               Analyzed Image
​─────────────┼──────────────────────────────────────────────
​  Target     │  dockerscoutpolicy/email-api-service:0.0.2
​    digest   │  17b1fde0329c
​    platform │ linux/amd64
​
​
​## Policies
​
​Policy status  FAILED  (2/8 policies met, 3 missing data)
​
​  Status │                  Policy                             │           Results
​─────────┼─────────────────────────────────────────────────────┼──────────────────────────────
​  ✓      │ No copyleft licenses                                │    0 packages
​  !      │ Default non-root user                               │
​  !      │ No fixable critical or high vulnerabilities         │    2C     1H     0M     0L
​  ✓      │ No high-profile vulnerabilities                     │    0C     0H     0M     0L
​  ?      │ No outdated base images                             │    No data
​         │                                                     │    Learn more ↗
​  ?      │ SonarQube quality gates passed                      │    No data
​         │                                                     │    Learn more ↗
​  !      │ Supply chain attestations                           │    2 deviations
​  ?      │ No unapproved base images                           │    No data

...
```

For more information about the command, refer to the
[CLI
reference](https://docs.docker.com/reference/cli/docker/scout/policy/).

---

# Get started with Policy Evaluation in Docker Scout

> Policies in Docker Scout let you define supply chain rules and thresholds for your artifacts, and track how your artifacts perform against those requirements over time

# Get started with Policy Evaluation in Docker Scout

   Table of contents

---

In software supply chain management, maintaining the security and reliability
of artifacts is a top priority. Policy Evaluation in Docker Scout introduces a
layer of control, on top of existing analysis capabilities. It lets you define
supply chain rules for your artifacts, and helps you track how your artifacts
perform, relative to your rules and thresholds, over time.

Learn how you can use Policy Evaluation to ensure that your artifacts align
with established best practices.

## How Policy Evaluation works

When you activate Docker Scout for a repository, images that you push are
[automatically analyzed](https://docs.docker.com/scout/explore/analysis/). The analysis gives you insights
about the composition of your images, including what packages they contain and
what vulnerabilities they're exposed to. Policy Evaluation builds on top of the
image analysis feature, interpreting the analysis results against the rules
defined by policies.

A policy defines image quality criteria that your artifacts should fulfill.
For example, the **No AGPL v3 licenses** policy flags any image containing packages distributed under the AGPL v3 license.
If an image contains such a package, that image is non-compliant with this policy.
Some policies, such as the **No AGPL v3 licenses** policy, are configurable.
Configurable policies let you adjust the criteria to better match your organization's needs.

In Docker Scout, policies are designed to help you ratchet forward your
security and supply chain stature. Where other tools focus on providing a pass
or fail status, Docker Scout policies visualizes how small, incremental changes
affect policy status, even when your artifacts don't meet the policy
requirements (yet). By tracking how the fail gap changes over time, you more
easily see whether your artifact is improving or deteriorating relative to
policy.

Policies don't necessarily have to be related to application security and
vulnerabilities. You can use policies to measure and track other aspects of
supply chain management as well, such as open-source license usage and base
image up-to-dateness.

## Policy types

In Docker Scout, a *policy* is derived from a *policy type*. Policy types are
templates that define the core parameters of a policy. You can compare policy
types to classes in object-oriented programming, with each policy acting as an
instance created from its corresponding policy type.

Docker Scout supports the following policy types:

- [Severity-Based Vulnerability](#severity-based-vulnerability)
- [Compliant Licenses](#compliant-licenses)
- [Up-to-Date Base Images](#up-to-date-base-images)
- [High-Profile Vulnerabilities](#high-profile-vulnerabilities)
- [Supply Chain Attestations](#supply-chain-attestations)
- [Default Non-Root User](#default-non-root-user)
- [Approved Base Images](#approved-base-images)
- [SonarQube Quality Gates](#sonarqube-quality-gates)
- [Valid Docker Hardened Image (DHI) or DHI base image](#valid-docker-hardened-image-dhi-or-dhi-base-image)

Docker Scout automatically provides default policies for repositories where it
is enabled, except for the following policies, which are optional and must be
configured:

- The **SonarQube Quality Gates** policy, which requires
  [integration with SonarQube](https://docs.docker.com/scout/integrations/code-quality/sonarqube/)
  before use.
- The **Valid Docker Hardened Image (DHI) or DHI base image** policy, which can
  be configured if you want to enforce the use of Docker Hardened Images.

You can create custom policies from any of the supported policy types, or
delete a default policy if it isn't applicable to your project. For more
information, refer to [Configure policies](https://docs.docker.com/scout/policy/configure/).

### Severity-Based Vulnerability

The **Severity-Based Vulnerability** policy type checks whether your
artifacts are exposed to known vulnerabilities.

By default, this policy only flags critical and high severity vulnerabilities
where there's a fix version available. Essentially, this means that there's an
easy fix that you can deploy for images that fail this policy: upgrade the
vulnerable package to a version containing a fix for the vulnerability.

Images are deemed non-compliant with this policy if they contain one or more
vulnerabilities that fall outside the specified policy criteria.

You can configure the parameters of this policy by creating a custom version of the policy.
The following policy parameters are configurable in a custom version:

- **Age**: The minimum number of days since the vulnerability was first published
  The rationale for only flagging vulnerabilities of a certain minimum age is
  that newly discovered vulnerabilities shouldn't cause your evaluations to
  fail until you've had a chance to address them.

- **Severities**: Severity levels to consider (default: `Critical, High`)

- **Fixable vulnerabilities only**: Whether or not to only report
  vulnerabilities with a fix version available (enabled by default).
- **Package types**: List of package types to consider.
  This option lets you specify the package types, as [PURL package type definitions](https://github.com/package-url/purl-spec/blob/master/PURL-TYPES.rst),
  that you want to include in the policy evaluation. By default, the policy
  considers all package types.

For more information about configuring policies, see [Configure policies](https://docs.docker.com/scout/policy/configure/).

### Compliant Licenses

The **Compliant Licenses** policy type checks whether your images contain
packages distributed under an inappropriate license. Images are considered
non-compliant if they contain one or more packages with such a license.

You can configure the list of licenses that this policy should look out for,
and add exceptions by specifying an allow-list (in the form of PURLs).
See [Configure policies](https://docs.docker.com/scout/policy/configure/).

### Up-to-Date Base Images

The **Up-to-Date Base Images** policy type checks whether the base images you
use are up-to-date.

Images are considered non-compliant with this policy if the tag you used to
build your image points to a different digest than what you're using. If
there's a mismatch in digests, that means the base image you're using is out of
date.

Your images need provenance attestations for this policy to successfully
evaluate. For more information, see [No base image data](#no-base-image-data).

### High-Profile Vulnerabilities

The **High-Profile Vulnerabilities** policy type checks whether your images
contain vulnerabilities from Docker Scout’s curated list. This list is kept
up-to-date with newly disclosed vulnerabilities that are widely recognized to
be risky.

The list includes the following vulnerabilities:

- [CVE-2014-0160 (OpenSSL Heartbleed)](https://scout.docker.com/v/CVE-2014-0160)
- [CVE-2021-44228 (Log4Shell)](https://scout.docker.com/v/CVE-2021-44228)
- [CVE-2023-38545 (cURL SOCKS5 heap buffer overflow)](https://scout.docker.com/v/CVE-2023-38545)
- [CVE-2023-44487 (HTTP/2 Rapid Reset)](https://scout.docker.com/v/CVE-2023-44487)
- [CVE-2024-3094 (XZ backdoor)](https://scout.docker.com/v/CVE-2024-3094)
- [CVE-2024-47176 (OpenPrinting -cups-browsed)](https://scout.docker.com/v/CVE-2024-47176)
- [CVE-2024-47076 (OpenPrinting -libcupsfilters)](https://scout.docker.com/v/CVE-2024-47076)
- [CVE-2024-47175 (OpenPrinting -libppd)](https://scout.docker.com/v/CVE-2024-47175)
- [CVE-2024-47177 (OpenPrinting -cups-filters)](https://scout.docker.com/v/CVE-2024-47177)

You can customize this policy to change which CVEs that are considered
high-profile by configuring the policy. Custom configuration options include:

- **Excluded CVEs**: Specify the CVEs that you want this policy to ignore.
  Default: `[]` (none of the high-profile CVEs are ignored)
- **CISA KEV**: Enable tracking of vulnerabilities from CISA's Known Exploited Vulnerabilities (KEV) catalog
  The [CISA KEV catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
  includes vulnerabilities that are actively exploited in the wild. When enabled,
  the policy flags images that contain vulnerabilities from the CISA KEV catalog.
  Enabled by default.

For more information on policy configuration, see [Configure policies](https://docs.docker.com/scout/policy/configure/).

### Supply Chain Attestations

The **Supply Chain Attestations** policy type checks whether your images have
[SBOM](https://docs.docker.com/build/metadata/attestations/sbom/) and
[provenance](https://docs.docker.com/build/metadata/attestations/slsa-provenance/) attestations.

Images are considered non-compliant if they lack either an SBOM attestation or
a provenance attestation with *max mode* provenance. To ensure compliance,
update your build command to attach these attestations at build-time:

```console
$ docker buildx build --provenance=true --sbom=true -t IMAGE --push .
```

For more information about building with attestations, see
[Attestations](https://docs.docker.com/build/metadata/attestations/).

If you're using GitHub Actions to build and push your images,
learn how you can
[configure the action](https://docs.docker.com/build/ci/github-actions/attestations/)
to apply SBOM and provenance attestations.

### Default Non-Root User

By default, containers run as the `root` superuser with full system
administration privileges inside the container, unless the Dockerfile specifies
a different default user. Running containers as a privileged user weakens their
runtime security, as it means any code that runs in the container can perform
administrative actions.

The **Default Non-Root User** policy type detects images that are set to run as
the default `root` user. To comply with this policy, images must specify a
non-root user in the image configuration. Images are non-compliant with this
policy if they don't specify a non-root default user for the runtime stage.

For non-compliant images, evaluation results show whether or not the `root`
user was set explicitly for the image. This helps you distinguish between
policy violations caused by images where the `root` user is implicit, and
images where `root` is set on purpose.

The following Dockerfile runs as `root` by default despite not being explicitly set:

```Dockerfile
FROM alpine
RUN echo "Hi"
```

Whereas in the following case, the `root` user is explicitly set:

```Dockerfile
FROM alpine
USER root
RUN echo "Hi"
```

> Note
>
> This policy only checks for the default user of the image, as set in the
> image configuration blob. Even if you do specify a non-root default user,
> it's still possible to override the default user at runtime, for example by
> using the `--user` flag for the `docker run` command.

To make your images compliant with this policy, use the
[USER](https://docs.docker.com/reference/dockerfile/#user) Dockerfile instruction to set
a default user that doesn't have root privileges for the runtime stage.

The following Dockerfile snippets shows the difference between a compliant and
non-compliant image.

```dockerfile
FROM alpine AS builder
COPY Makefile ./src /
RUN make build

FROM alpine AS runtime
COPY --from=builder bin/production /app
ENTRYPOINT ["/app/production"]
```

```dockerfile
FROM alpine AS builder
COPY Makefile ./src /
RUN make build

FROM alpine AS runtime
COPY --from=builder bin/production /app
USER nonroot
ENTRYPOINT ["/app/production"]
```

### Approved Base Images

The **Approved Base Images** policy type ensures that the base images you use
in your builds are maintained and secure.

This policy checks whether the base images used in your builds match any of the
patterns specified in the policy configuration. The following table shows a few
example patterns for this policy.

| Use case | Pattern |
| --- | --- |
| Allow all images from Docker Hub | docker.io/* |
| Allow all Docker Official Images | docker.io/library/* |
| Allow images from a specific organization | docker.io/orgname/* |
| Allow tags of a specific repository | docker.io/orgname/repository:* |
| Allow images on a registry with hostnameregistry.example.com | registry.example.com/* |
| Allow slim tags of NodeJS images | docker.io/library/node:*-slim |

An asterisk (`*`) matches up until the character that follows, or until the end
of the image reference. Note that the `docker.io` prefix is required in order
to match Docker Hub images. This is the registry hostname of Docker Hub.

This policy is configurable with the following options:

- **Approved base image sources**
  Specify the image reference patterns that you want to allow. The policy
  evaluates the base image references against these patterns.
  Default: `[*]` (any reference is an allowed base image)
- **Only supported tags**
  Allow only supported tags when using Docker Official Images.
  When this option is enabled, images using unsupported tags of official images
  as their base image trigger a policy violation. Supported tags for official
  images are listed in the **Supported tags** section of the repository
  overview on Docker Hub.
  Enabled by default.
- **Only supported OS distributions**
  Allow only Docker Official Images of supported Linux distribution versions.
  When this option is enabled, images using unsupported Linux distributions
  that have reached end of life (such as `ubuntu:18.04`) trigger a policy violation.
  Enabling this option may cause the policy to report no data
  if the operating system version cannot be determined.
  Enabled by default.

Your images need provenance attestations for this policy to successfully
evaluate. For more information, see [No base image data](#no-base-image-data).

### SonarQube Quality Gates

The **SonarQube Quality Gates** policy type builds on the [SonarQube
integration](https://docs.docker.com/scout/integrations/code-quality/sonarqube/) to assess the quality
of your source code. This policy works by ingesting the SonarQube code analysis
results into Docker Scout.

You define the criteria for this policy using SonarQube's [quality
gates](https://docs.sonarsource.com/sonarqube/latest/user-guide/quality-gates/).
SonarQube evaluates your source code against the quality gates you've defined
in SonarQube. Docker Scout surfaces the SonarQube assessment as a Docker Scout
policy.

Docker Scout uses
[provenance](https://docs.docker.com/build/metadata/attestations/slsa-provenance/)
attestations or the `org.opencontainers.image.revision` OCI annotation to link
SonarQube analysis results with container images. In addition to enabling the
SonarQube integration, you must also make sure that your images have either the
attestation or the label.

![Git commit SHA links image with SonarQube analysis](https://docs.docker.com/scout/images/scout-sq-commit-sha.webp)  ![Git commit SHA links image with SonarQube analysis](https://docs.docker.com/scout/images/scout-sq-commit-sha.webp)

Once you push an image and policy evaluation completes, the results from the
SonarQube quality gates display as a policy in the Docker Scout Dashboard, and
in the CLI.

> Note
>
> Docker Scout can only access SonarQube analyses created after the integration
> is enabled. Docker Scout doesn't have access to historic evaluations. Trigger
> a SonarQube analysis and policy evaluation after enabling the integration to
> view the results in Docker Scout.

### Valid Docker Hardened Image (DHI) or DHI base image

The **Valid Docker Hardened Image (DHI) or DHI base image** policy type ensures
that your images are either Docker Hardened Images (DHI) or are built using a
DHI as the base image.

This policy validates images by checking for a valid Docker signed verification
summary attestation. The policy considers an image compliant if either:

- The image itself is a Docker Hardened Image with a valid Docker signed
  verification summary attestation, or
- The base image used in the build (identified from SLSA provenance
  attestations) has a valid Docker signed verification summary attestation

Images are non-compliant with this policy if they lack the required Docker
signed verification summary attestation and are not built from a base image
with such an attestation.

This policy has no configurable parameters.

## No base image data

There are cases when it's not possible to determine information about the base
images used in your builds. In such cases, the **Up-to-Date Base Images** and
**Approved Base Images** policies get flagged as having **No data**.

This "no data" state occurs when:

- Docker Scout doesn't know what base image tag you used
- The base image version you used has multiple tags, but not all tags are out
  of date

To make sure that Docker Scout always knows about your base image, you can
attach
[provenance attestations](https://docs.docker.com/build/metadata/attestations/slsa-provenance/)
at build-time. Docker Scout uses provenance attestations to find out the base
image version.

---

# Docker Scout quickstart

> Learn how to get started with Docker Scout to analyze images and fix vulnerabilities

# Docker Scout quickstart

   Table of contents

---

Docker Scout analyzes image contents and generates a detailed report of packages
and vulnerabilities that it detects. It can provide you with
suggestions for how to remediate issues discovered by image analysis.

This guide takes a vulnerable container image and shows you how to use Docker
Scout to identify and fix the vulnerabilities, compare image versions over time,
and share the results with your team.

## Step 1: Setup

[This example project](https://github.com/docker/scout-demo-service) contains
a vulnerable Node.js application that you can use to follow along.

1. Clone its repository:
  ```console
  $ git clone https://github.com/docker/scout-demo-service.git
  ```
2. Move into the directory:
  ```console
  $ cd scout-demo-service
  ```
3. Make sure you're signed in to your Docker account,
  either by running the `docker login` command or by signing in with Docker Desktop.
4. Build the image and push it to a `<ORG_NAME>/scout-demo:v1`,
  where `<ORG_NAME>` is the Docker Hub namespace you push to.
  ```console
  $ docker build --push -t ORG_NAME/scout-demo:v1 .
  ```

## Step 2: Enable Docker Scout

Docker Scout analyzes all local images by default. To analyze images in
remote repositories, you need to enable it first.
You can do this from Docker Hub, the Docker Scout Dashboard, and CLI.
[Find out how in the overview guide](https://docs.docker.com/scout).

1. Sign in to your Docker account with the `docker login` command or use the
  **Sign in** button in Docker Desktop.
2. Next, enroll your organization with Docker Scout, using the `docker scout enroll` command.
  ```console
  $ docker scout enroll ORG_NAME
  ```
3. Enable Docker Scout for your image repository with the `docker scout repo enable` command.
  ```console
  $ docker scout repo enable --org ORG_NAME ORG_NAME/scout-demo
  ```

## Step 3: Analyze image vulnerabilities

After building, use the `docker scout` CLI command to see vulnerabilities
detected by Docker Scout.

The example application for this guide uses a vulnerable version of Express.
The following command shows all CVEs affecting Express in the image you just
built:

```console
$ docker scout cves --only-package express
```

Docker Scout analyzes the image you built most recently by default,
so there's no need to specify the name of the image in this case.

Learn more about the `docker scout cves` command in the
[CLI reference documentation](https://docs.docker.com/reference/cli/docker/scout/cves).

## Step 4: Fix application vulnerabilities

After the Docker Scout analysis, a high vulnerability CVE-2022-24999 was found, caused by an outdated version of the **express** package.

The version 4.17.3 of the express package fixes the vulnerability. Therefore, update the `package.json` file to the new version:

```diff
"dependencies": {
-    "express": "4.17.1"
+    "express": "4.17.3"
   }
```

Rebuild the image with a new tag and push it to your Docker Hub repository:

```console
$ docker build --push -t ORG_NAME/scout-demo:v2 .
```

Run the `docker scout` command again and verify that HIGH CVE-2022-24999 is no longer present:

```console
$ docker scout cves --only-package express
    ✓ Provenance obtained from attestation
    ✓ Image stored for indexing
    ✓ Indexed 79 packages
    ✓ No vulnerable package detected

  ## Overview

                      │                  Analyzed Image
  ────────────────────┼───────────────────────────────────────────────────
    Target            │  mobywhale/scout-demo:v2
      digest          │  ef68417b2866
      platform        │ linux/arm64
      provenance      │ https://github.com/docker/scout-demo-service.git
                      │  7c3a06793fc8f97961b4a40c73e0f7ed85501857
      vulnerabilities │    0C     0H     0M     0L
      size            │ 19 MB
      packages        │ 1

  ## Packages and Vulnerabilities

  No vulnerable packages detected
```

## Step 5: Evaluate policy compliance

While inspecting vulnerabilities based on specific packages can be useful,
it isn't the most effective way to improve your supply chain conduct.

Docker Scout also supports policy evaluation,
a higher-level concept for detecting and fixing issues in your images.
Policies are a set of customizable rules that let organizations track whether
images are compliant with their supply chain requirements.

Because policy rules are specific to each organization,
you must specify which organization's policy you're evaluating against.
Use the `docker scout config` command to configure your Docker organization.

```console
$ docker scout config organization ORG_NAME
    ✓ Successfully set organization to ORG_NAME
```

Now you can run the `quickview` command to get an overview
of the compliance status for the image you just built.
The image is evaluated against the default policy configurations. You'll see output similar to the following:

```console
$ docker scout quickview

...
Policy status  FAILED  (2/6 policies met, 2 missing data)

  Status │                  Policy                      │           Results
─────────┼──────────────────────────────────────────────┼──────────────────────────────
  ✓      │ No copyleft licenses                         │    0 packages
  !      │ Default non-root user                        │
  !      │ No fixable critical or high vulnerabilities  │    2C    16H     0M     0L
  ✓      │ No high-profile vulnerabilities              │    0C     0H     0M     0L
  ?      │ No outdated base images                      │    No data
  ?      │ Supply chain attestations                    │    No data
```

Exclamation marks in the status column indicate a violated policy.
Question marks indicate that there isn't enough metadata to complete the evaluation.
A check mark indicates compliance.

## Step 6: Improve compliance

The output of the `quickview` command shows that there's room for improvement.
Some of the policies couldn't evaluate successfully (`No data`)
because the image lacks provenance and SBOM attestations.
The image also failed the check on a few of the evaluations.

Policy evaluation does more than just check for vulnerabilities.
Take the `Default non-root user` policy for example.
This policy helps improve runtime security by ensuring that
images aren't set to run as the `root` superuser by default.

To address this policy violation, edit the Dockerfile by adding a `USER`
instruction, specifying a non-root user:

```diff
CMD ["node","/app/app.js"]
  EXPOSE 3000
+ USER appuser
```

Additionally, to get a more complete policy evaluation result,
your image should have SBOM and provenance attestations attached to it.
Docker Scout uses the provenance attestations to determine how the image was
built so that it can provide a better evaluation result.

Before you can build an image with attestations,
you must enable the
[containerd image store](https://docs.docker.com/desktop/features/containerd/)
(or create a custom builder using the `docker-container` driver).
The classic image store doesn't support manifest lists,
which is how the provenance attestations are attached to an image.

Open **Settings** in Docker Desktop. Under the **General** section, make sure
that the **Use containerd for pulling and storing images** option is checked, then select **Apply**.
Note that changing image stores temporarily hides images and containers of the
inactive image store until you switch back.

With the containerd image store enabled, rebuild the image with a new `v3` tag.
This time, add the `--provenance=true` and `--sbom=true` flags.

```console
$ docker build --provenance=true --sbom=true --push -t ORG_NAME/scout-demo:v3 .
```

## Step 7: View in Dashboard

After pushing the updated image with attestations, it's time to view the
results through a different lens: the Docker Scout Dashboard.

1. Open the [Docker Scout Dashboard](https://scout.docker.com/).
2. Sign in with your Docker account.
3. Select **Images** in the left-hand navigation.

The images page lists your Scout-enabled repositories.

Select the row for the image you want to view, anywhere in the row except on a link, to open the **Image details** sidebar.

The sidebar shows a compliance overview for the last pushed tag of a repository.

> Note
>
> If policy results haven't appeared yet, try refreshing the page.
> It might take a few minutes before the results appear if this is your
> first time using the Docker Scout Dashboard.

Go back to the image list and select the image version, available in the **Most recent image** column.
Then, at the top right of the page, select the **Update base image** button to inspect the policy.

This policy checks whether base images you use are up-to-date.
It currently has a non-compliant status,
because the example image uses an old version `alpine` as a base image.

Close the **Recommended fixes for base image** modal. In the policy listing, select **View fixes** button, next to the policy name for details about the violation, and recommendations on how to address it.

In this case, the recommended action is to enable
[Docker Scout's GitHub integration](https://docs.docker.com/scout/integrations/source-code-management/github/),
which helps keep your base images up-to-date automatically.

> Tip
>
> You can't enable this integration for the demo app used in this guide.
> Feel free to push the code to a GitHub repository that you own,
> and try out the integration there!

## Summary

This quickstart guide has scratched the surface on some of the ways
Docker Scout can support software supply chain management:

- How to enable Docker Scout for your repositories
- Analyzing images for vulnerabilities
- Policy and compliance
- Fixing vulnerabilities and improving compliance

## What's next?

There's lots more to discover, from third-party integrations,
to policy customization, and runtime environment monitoring in real-time.

Check out the following sections:

- [Image analysis](https://docs.docker.com/scout/explore/analysis/)
- [Data sources](https://docs.docker.com/scout/advisory-db-sources)
- [Docker Scout Dashboard](https://docs.docker.com/scout/dashboard)
- [Integrations](https://docs.docker.com/scout/integrations/)
- [Policy evaluation](https://docs.docker.com/scout/policy/)

---

# Search code, repositories, users, issues, pull requests...

> Docker Scout CLI. Contribute to docker/scout-cli development by creating an account on GitHub.

# What's Changed

- CVE fixes [@cdupuis](https://github.com/cdupuis)
- Update dependencies [@cdupuis](https://github.com/cdupuis)
- Documentation updates [@craig-osterhout](https://github.com/craig-osterhout)
- Handle attestation source failures more gracefully [@chrispatrick](https://github.com/chrispatrick)
- Bug fixes including around VEX, versioning and indexing [@cdupuis](https://github.com/cdupuis)
