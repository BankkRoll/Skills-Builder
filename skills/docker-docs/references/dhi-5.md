# Mirror a Docker Hardened Image repositoryDHI Enterprise and more

# Mirror a Docker Hardened Image repositoryDHI Enterprise

> Learn how to mirror an image into your organization's namespace and optionally push it to another private registry.

# Mirror a Docker Hardened Image repositoryDHI Enterprise

   Table of contents

---

Subscription: Docker Hardened Images Enterprise

Mirroring requires a DHI Enterprise subscription. Without a DHI Enterprise
subscription, you can pull Docker Hardened Images directly from `dhi.io` without
mirroring. With a DHI Enterprise subscription, you must mirror to get:

- Compliance variants (FIPS-enabled or STIG-ready images)
- Extended Lifecycle Support (ELS) variants (requires add-on)
- Image or Helm chart customization
- Air-gapped or restricted network environments
- SLA-backed security updates

## How to mirror

This topic covers two types of mirroring for Docker Hardened Image (DHI)
repositories:

- [Mirror to Docker Hub](#mirror-a-dhi-repository-to-docker-hub): Mirror a DHI
  repository to your organization's namespace on Docker Hub. This requires a DHI
  Enterprise subscription and is used to [customize an image or
  chart](https://docs.docker.com/dhi/how-to/customize/) and access compliance variants and ELS variants
  (requires add-on). This must be done through the Docker Hub web interface.
- [Mirror to a third-party
  registry](#mirror-a-dhi-repository-to-a-third-party-registry): Mirror a
  repository to another container registry, such as Amazon ECR, Google Artifact
  Registry, or a private Harbor instance.

## Mirror a DHI repository to Docker Hub

Mirroring a repository to Docker Hub requires a DHI Enterprise subscription and
enables access to compliance variants, Extended Lifecycle Support (ELS) variants
(requires add-on), and customization capabilities:

- Image repositories: Mirroring lets you customize images by adding packages,
  OCI artifacts (such as custom certificates or additional tools), environment
  variables, labels, and other configuration settings. For more details, see
  [Customize a Docker Hardened Image](https://docs.docker.com/dhi/how-to/customize/#customize-a-docker-hardened-image).
- Chart repositories: Mirroring lets you customize image references within
  the chart. This is particularly useful when using customized images or when
  you've mirrored images to a third-party registry and need the chart to
  reference those custom locations. For more details, see [Customize a Docker
  Hardened Helm chart](https://docs.docker.com/dhi/how-to/customize/#customize-a-docker-hardened-helm-chart).

Only organization owners can perform mirroring. Once mirrored, the repository
becomes available in your organization's namespace, and you can customize it as
needed.

To mirror a Docker Hardened Image repository:

1. Go to [Docker Hub](https://hub.docker.com) and sign in.
2. Select **My Hub**.
3. In the namespace drop-down, select your organization.
4. Select **Hardened Images** > **Catalog**.
5. Select a DHI repository to view its details.
6. Mirror the repository:
  - To mirror an image repository, select **Use this image** > **Mirror
    repository**, and then follow the on-screen instructions. If you have the ELS add-on, you can also
    select **Enable support for end-of-life versions**.
  - To mirror a Helm chart repository, select **Get Helm chart**, and then follow the on-screen instructions.

It may take a few minutes for all the tags to finish mirroring.

After mirroring a repository, the repository appears in your organization's
repository list, prefixed by `dhi-`. It will continue to receive updated images.

Once mirrored, the repository works like any other private repository on Docker
Hub and you can now customize it. To learn more about customization, see
[Customize a Docker Hardened Image or chart](https://docs.docker.com/dhi/how-to/customize/).

### Webhook integration for syncing and alerts

To keep external registries or systems in sync with your mirrored Docker
Hardened Images, and to receive notifications when updates occur, you can
configure a
[webhook](https://docs.docker.com/docker-hub/repos/manage/webhooks/) on the mirrored
repository in Docker Hub. A webhook sends a `POST` request to a URL you define
whenever a new image tag is pushed or updated.

For example, you might configure a webhook to call a CI/CD system at
`https://ci.example.com/hooks/dhi-sync` whenever a new tag is mirrored. The
automation triggered by this webhook can pull the updated image from Docker Hub
and push it to an internal registry such as Amazon ECR, Google Artifact
Registry, or GitHub Container Registry.

Other common webhook use cases include:

- Triggering validation or vulnerability scanning workflows
- Signing or promoting images
- Sending notifications to downstream systems

#### Example webhook payload

When a webhook is triggered, Docker Hub sends a JSON payload like the following:

```json
{
  "callback_url": "https://registry.hub.docker.com/u/exampleorg/dhi-python/hook/abc123/",
  "push_data": {
    "pushed_at": 1712345678,
    "pusher": "trustedbuilder",
    "tag": "3.13-alpine3.21"
  },
  "repository": {
    "name": "dhi-python",
    "namespace": "exampleorg",
    "repo_name": "exampleorg/dhi-python",
    "repo_url": "https://hub.docker.com/r/exampleorg/dhi-python",
    "is_private": true,
    "status": "Active",
    ...
  }
}
```

### Stop mirroring a repository

Only organization owners can stop mirroring a repository. After you stop
mirroring, the repository remains, but it will
no longer receive updates. You can still use the last images or charts that were mirrored,
but the repository will not receive new tags or updates from the original
repository.

> Note
>
> If you only want to stop mirroring ELS versions, you can uncheck the ELS
> option in the mirrored repository's **Settings** tab. For more details, see
> [Disable ELS for a repository](https://docs.docker.com/dhi/how-to/els/#disable-els-for-a-repository).

To stop mirroring a repository:

1. Go to [Docker Hub](https://hub.docker.com) and sign in.
2. Select **My Hub**.
3. In the namespace drop-down, select your organization that has access to DHI.
4. Select **Hardened Images** > **Manage**.
5. Select the **Mirrored Images** or **Mirrored Helm charts** tab.
6. In the far right column of the repository you want to stop mirroring, select the menu icon.
7. Select **Stop mirroring**.

## Mirror a DHI repository to a third-party registry

You can optionally mirror a DHI repository to another container registry, such as Amazon
ECR, Google Artifact Registry, GitHub Container Registry, or a private Harbor
instance.

You can use any standard workflow to mirror the image, such as the
[Docker CLI](https://docs.docker.com/reference/cli/docker/),
[Docker Hub Registry
API](https://docs.docker.com/reference/api/registry/latest/), third-party registry tools, or CI/CD
automation.

However, to preserve the full security context, including attestations, you must
also mirror its associated OCI artifacts. DHI repositories store the image
layers on `dhi.io` (or `docker.io` for customized images) and the signed
attestations in a separate registry (`registry.scout.docker.com`).

To copy both, you can use [regctl](https://regclient.org/cli/regctl/), an
OCI-aware CLI that supports mirroring images along with attached artifacts such
as SBOMs, vulnerability reports, and SLSA provenance. For ongoing synchronization,
you can use [regsync](https://regclient.org/cli/regsync/).

### Example mirroring withregctl

The following example shows how to mirror a specific tag of a Docker Hardened
Image from Docker Hub to another registry, along with its associated
attestations using `regctl`. You must [installregctl](https://github.com/regclient/regclient) first.

The example assumes you have mirrored the DHI repository to your organization's
namespace on Docker Hub as described in the previous section. You can apply the
same steps to a non-mirrored image by updating the the `SRC_ATT_REPO` and
`SRC_REPO` variables accordingly.

1. Set environment variables for your specific environment. Replace the
  placeholders with your actual values.
  In this example, you use a Docker username to represent a member of the Docker
  Hub organization that the DHI repositories are mirrored in. Prepare a
  [personal access token (PAT)](https://docs.docker.com/security/access-tokens/) for the user
  with `read only` access. Alternatively, you can use an organization namespace and
  an [organization access token
  (OAT)](https://docs.docker.com/enterprise/security/access-tokens/) to sign in to Docker Hub, but OATs
  are not yet supported for `registry.scout.docker.com`.
  ```console
  $ export DOCKER_USERNAME="YOUR_DOCKER_USERNAME"
  $ export DOCKER_PAT="YOUR_DOCKER_PAT"
  $ export DOCKER_ORG="YOUR_DOCKER_ORG"
  $ export DEST_REG="registry.example.com"
  $ export DEST_REPO="mirror/dhi-python"
  $ export DEST_REG_USERNAME="YOUR_DESTINATION_REGISTRY_USERNAME"
  $ export DEST_REG_TOKEN="YOUR_DESTINATION_REGISTRY_TOKEN"
  $ export SRC_REPO="docker.io/${DOCKER_ORG}/dhi-python"
  $ export SRC_ATT_REPO="registry.scout.docker.com/${DOCKER_ORG}/dhi-python"
  $ export TAG="3.13-alpine3.21"
  ```
2. Sign in via `regctl` to Docker Hub, the Scout registry that contains
  the attestations, and your destination registry.
  ```console
  $ echo $DOCKER_PAT | regctl registry login -u "$DOCKER_USERNAME" --pass-stdin docker.io
  $ echo $DOCKER_PAT | regctl registry login -u "$DOCKER_USERNAME" --pass-stdin registry.scout.docker.com
  $ echo $DEST_REG_TOKEN | regctl registry login -u "$DEST_REG_USERNAME" --pass-stdin "$DEST_REG"
  ```
3. Mirror the image and attestations using `--referrers` and referrer endpoints:
  ```console
  $ regctl image copy \
       "${SRC_REPO}:${TAG}" \
       "${DEST_REG}/${DEST_REPO}:${TAG}" \
       --referrers \
       --referrers-src "${SRC_ATT_REPO}" \
       --referrers-tgt "${DEST_REG}/${DEST_REPO}" \
       --force-recursive
  ```
4. Verify that artifacts were preserved.
  First, get a digest for a specific tag and platform. For example, `linux/amd64`.
  ```console
  DIGEST="$(regctl manifest head "${DEST_REG}/${DEST_REPO}:${TAG}" --platform linux/amd64)"
  ```
  List attached artifacts (SBOM, provenance, VEX, vulnerability reports).
  ```console
  $ regctl artifact list "${DEST_REG}/${DEST_REPO}@${DIGEST}"
  ```
  Or, list attached artifacts with `docker scout`.
  ```console
  $ docker scout attest list "registry://${DEST_REG}/${DEST_REPO}@${DIGEST}"
  ```

### Example ongoing mirroring withregsync

`regsync` automates pulling from your organizations mirrored DHI repositories on
Docker Hub and pushing to your external registry including attestations. It
reads a YAML configuration file and can filter tags.

The following example uses a `regsync.yaml` file that syncs Node 24 and Python
3.12 Debian 13 variants, excluding Alpine and Debian 12.

regsync.yaml

```yaml
version: 1
# Optional: inline creds if not relying on prior CLI logins
# creds:
#   - registry: docker.io
#     user: <your-docker-username>
#     pass: "{{file \"/run/secrets/docker_token\"}}"
#   - registry: registry.scout.docker.com
#     user: <your-docker-username>
#     pass: "{{file \"/run/secrets/docker_token\"}}"
#   - registry: registry.example.com
#     user: <service-user>
#     pass: "{{file \"/run/secrets/dest_token\"}}"

sync:
  - source: docker.io/<your-org>/dhi-node
    target: registry.example.com/mirror/dhi-node
    type: repository
    fastCopy: true
    referrers: true
    referrerSource: registry.scout.docker.com/<your-org>/dhi-node
    referrerTarget: registry.example.com/mirror/dhi-node
    tags:
      allow: [ "24.*" ]
      deny: [ ".*alpine.*", ".*debian12.*" ]

  - source: docker.io/<your-org>/dhi-python
    target: registry.example.com/mirror/dhi-python
    type: repository
    fastCopy: true
    referrers: true
    referrerSource: registry.scout.docker.com/<your-org>/dhi-python
    referrerTarget: registry.example.com/mirror/dhi-python
    tags:
      allow: [ "3.12.*" ]
      deny: [ ".*alpine.*", ".*debian12.*" ]
```

To do a dry run with the configuration file, you can run the following command.
You must [installregsync](https://github.com/regclient/regclient) first.

```console
$ regsync check -c regsync.yaml
```

To run the sync with the configuration file:

```console
$ regsync once -c regsync.yaml
```

## What next

After mirroring, see [Pull a DHI](https://docs.docker.com/dhi/how-to/use/#pull-a-dhi) to learn how to pull and use mirrored images.

---

# Enforce Docker Hardened Image usage with policies

> Learn how to use image policies with Docker Scout for Docker Hardened Images.

# Enforce Docker Hardened Image usage with policies

   Table of contents

---

When you have a Docker Hardened Images Enterprise subscription, mirroring a
Docker Hardened Image (DHI) repository automatically enables
[Docker
Scout](https://docs.docker.com/scout/), allowing you to start enforcing security and compliance
policies for your images without additional setup. Using Docker Scout policies,
you can define and apply rules that ensure only approved and secure images, such
as those based on DHIs, are used across your environments.

Docker Scout includes a dedicated [Valid Docker Hardened Image (DHI) or DHI
base
image](https://docs.docker.com/scout/policy/#valid-docker-hardened-image-dhi-or-dhi-base-image)
policy type that validates whether your images are Docker Hardened Images or are
built using a DHI as the base image. This policy checks for valid Docker signed
verification summary attestations.

With policy evaluation built into Docker Scout, you can monitor image compliance
in real time, integrate checks into your CI/CD workflows, and maintain
consistent standards for image security and provenance.

## View existing policies

To see the current policies applied to a mirrored DHI repository:

1. Go to the mirrored DHI repository in [Docker Hub](https://hub.docker.com).
2. Select **View on Scout**.
  This opens the [Docker Scout dashboard](https://scout.docker.com), where you
  can see which policies are currently active and whether your images meet the
  policy criteria.

Docker Scout automatically evaluates policy compliance when new images are
pushed. Each policy includes a compliance result and a link to the affected
images and layers.

## Evaluate DHI policy compliance for your images

When you enable Docker Scout for your repositories, you can configure the
[Valid Docker Hardened Image (DHI) or DHI base
image](https://docs.docker.com/scout/policy/#valid-docker-hardened-image-dhi-or-dhi-base-image)
policy. This optional policy validates whether your images are DHIs or built with DHI
base images by checking for Docker signed verification summary attestations.

The following example shows how to build an image using a DHI base image and
evaluate its compliance with the DHI policy.

### Example: Build and evaluate a DHI-based image

#### Step 1: Use a DHI base image in your Dockerfile

Create a Dockerfile that uses a Docker Hardened Image mirrored repository as the
base. For example:

```dockerfile
# Dockerfile
FROM <your-namespace>/dhi-python:3.13-alpine3.21

ENTRYPOINT ["python", "-c", "print('Hello from a DHI-based image')"]
```

#### Step 2: Build and push the image

Open a terminal and navigate to the directory containing your Dockerfile. Then,
build and push the image to your Docker Hub repository:

```console
$ docker build \
  --push \
  -t <your-namespace>/my-dhi-app:v1 .
```

#### Step 3: Enable Docker Scout

To enable Docker Scout for your organization and the repository, run the
following commands in your terminal:

```console
$ docker login
$ docker scout enroll <your-namespace>
$ docker scout repo enable --org <your-namespace> <your-namespace>/my-dhi-app
```

#### Step 4: Configure the DHI policy

Once Docker Scout is enabled, you can configure the **Valid Docker Hardened
Image (DHI) or DHI base image** policy for your organization:

1. Go to the [Docker Scout dashboard](https://scout.docker.com).
2. Select your organization and navigate to **Policies**.
3. Configure the **Valid Docker Hardened Image (DHI) or DHI base image** policy
  to enable it for your repositories.

For more information on configuring policies, see
[Configure policies](https://docs.docker.com/scout/policy/configure/).

#### Step 5: View policy compliance

Once the DHI policy is configured and active, you can view compliance results:

1. Go to the [Docker Scout dashboard](https://scout.docker.com).
2. Select your organization and navigate to **Images**.
3. Find your image, `<your-namespace>/my-dhi-app:v1`, and select the link in the **Compliance** column.

This shows the policy compliance results for your image. The **Valid Docker
Hardened Image (DHI) or DHI base image** policy evaluates whether your image has
a valid Docker signed verification summary attestation or if its base image has
such an attestation.

You can now
[evaluate policy compliance in your CI](https://docs.docker.com/scout/policy/ci/).

---

# Scan Docker Hardened Images

> Learn how to scan Docker Hardened Images for known vulnerabilities using Docker Scout, Grype, Trivy, or Wiz.

# Scan Docker Hardened Images

   Table of contents

---

Docker Hardened Images (DHIs) are designed to be secure by default, but like any
container image, it's important to scan them regularly as part of your
vulnerability management process.

## Scan with OpenVEX-compliant scanners

To get accurate vulnerability assessments, use scanners that support
[VEX](https://docs.docker.com/dhi/core-concepts/vex/) attestations. The following scanners can
read and apply the VEX statements included with Docker Hardened Images:

- [Docker Scout](#docker-scout): Automatically applies VEX statements with zero configuration
- [Trivy](#trivy): Supports VEX through VEX Hub or local VEX files
- [Grype](#grype): Supports VEX via the `--vex` flag
- [Wiz](#wiz): Automatically applies VEX statements with
  zero configuration

For guidance on choosing the right scanner and understanding the differences
between VEX-enabled and non-VEX scanners, see
[Scanner
integrations](https://docs.docker.com/dhi/explore/scanner-integrations/).

## Docker Scout

Docker Scout is integrated into Docker Desktop and the Docker CLI. It provides
vulnerability insights, CVE summaries, and direct links to remediation guidance.

### Scan a DHI using Docker Scout

To scan a Docker Hardened Image using Docker Scout, run the following
command:

```console
$ docker login dhi.io
$ docker scout cves dhi.io/<image>:<tag> --platform <platform>
```

Example output:

```plaintext
v SBOM obtained from attestation, 101 packages found
    v Provenance obtained from attestation
    v VEX statements obtained from attestation
    v No vulnerable package detected
    ...
```

For more detailed filtering and JSON output, see [Docker Scout CLI reference](https://docs.docker.com/reference/cli/docker/scout/).

### Automate DHI scanning in CI/CD with Docker Scout

Integrating Docker Scout into your CI/CD pipeline enables you to automatically
verify that images built from Docker Hardened Images remain free from known
vulnerabilities during the build process. This proactive approach ensures the
continued security integrity of your images throughout the development
lifecycle.

#### Example GitHub Actions workflow

The following is a sample GitHub Actions workflow that builds an image and scans
it using Docker Scout:

```yaml
name: DHI Vulnerability Scan

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ "**" ]

env:
  REGISTRY: docker.io
  IMAGE_NAME: ${{ github.repository }}
  SHA: ${{ github.event.pull_request.head.sha || github.event.after }}

jobs:
  scan:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
      pull-requests: write

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Build Docker image
        run: |
          docker build -t ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ env.SHA }} .

      - name: Run Docker Scout CVE scan
        uses: docker/scout-action@v1
        with:
          command: cves
          image: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ env.SHA }}
          only-severities: critical,high
          exit-code: true
```

The `exit-code: true` parameter ensures that the workflow fails if any critical or
high-severity vulnerabilities are detected, preventing the deployment of
insecure images.

For more details on using Docker Scout in CI, see
[Integrating Docker
Scout with other systems](https://docs.docker.com/scout/integrations/).

## Grype

[Grype](https://github.com/anchore/grype) is an open-source scanner that checks
container images against vulnerability databases like the NVD and distro
advisories.

### Scan a DHI using Grype

To scan a Docker Hardened Image using Grype with VEX filtering, first export
the VEX attestation and then scan with the `--vex` flag:

```console
$ docker login dhi.io
$ docker pull dhi.io/<image>:<tag>
$ docker scout vex get dhi.io/<image>:<tag> --output vex.json
$ grype dhi.io/<image>:<tag> --vex vex.json
```

The `--vex` flag applies VEX statements during the scan, filtering out known
non-exploitable CVEs for accurate results.

For more information on exporting VEX attestations, see [Export VEX
attestations](#export-vex-attestations).

## Trivy

[Trivy](https://github.com/aquasecurity/trivy) is an open-source vulnerability
scanner for containers and other artifacts. It detects vulnerabilities in OS
packages and application dependencies.

### Scan a DHI using Trivy

After installing Trivy, you can scan a Docker Hardened Image by pulling
the image and running the scan command:

```console
$ docker login dhi.io
$ docker pull dhi.io/<image>:<tag>
$ trivy image --scanners vuln dhi.io/<image>:<tag>
```

To filter vulnerabilities using VEX statements, Trivy supports multiple
approaches. Docker recommends using VEX Hub, which provides a seamless workflow
for automatically downloading and applying VEX statements from configured
repositories.

#### Using VEX Hub (recommended)

Configure Trivy to download the Docker Hardened Images advisories repository
from VEX Hub. Run the following commands to set up the VEX repository:

```console
$ trivy vex repo init
$ cat << REPO > ~/.trivy/vex/repository.yaml
repositories:
  - name: default
    url: https://github.com/aquasecurity/vexhub
    enabled: true
    username: ""
    password: ""
    token: ""
  - name: dhi-vex
    url: https://github.com/docker-hardened-images/advisories
    enabled: true
REPO
$ trivy vex repo list
$ trivy vex repo download
```

After setting up VEX Hub, you can scan a Docker Hardened Image with VEX filtering:

```console
$ docker login dhi.io
$ docker pull dhi.io/<image>:<tag>
$ trivy image --scanners vuln --vex repo dhi.io/<image>:<tag>
```

For example, scanning the `dhi.io/python:3.13` image:

```console
$ trivy image --scanners vuln --vex repo dhi.io/python:3.13
```

Example output:

```plaintext
Report Summary

┌─────────────────────────────────────────────────────────────────────────────┬────────────┬─────────────────┐
│                                   Target                                    │    Type    │ Vulnerabilities │
├─────────────────────────────────────────────────────────────────────────────┼────────────┼─────────────────┤
│ dhi.io/python:3.13 (debian 13.2)                                            │   debian   │        0        │
├─────────────────────────────────────────────────────────────────────────────┼────────────┼─────────────────┤
│ opt/python-3.13.11/lib/python3.13/site-packages/pip-25.3.dist-info/METADATA │ python-pkg │        0        │
└─────────────────────────────────────────────────────────────────────────────┴────────────┴─────────────────┘
Legend:
- '-': Not scanned
- '0': Clean (no security findings detected)
```

The `--vex repo` flag applies VEX statements from the configured repository during the scan,
which filters out known non-exploitable CVEs.

#### Using local VEX files

In addition to VEX Hub, Trivy also supports the use of local VEX files for
vulnerability filtering. You can download the VEX attestation that Docker
Hardened Images provide and use it directly with Trivy.

First, download the VEX attestation for your image:

```console
$ docker scout vex get dhi.io/<image>:<tag> --output vex.json
```

Then scan the image with the local VEX file:

```console
$ trivy image --scanners vuln --vex vex.json dhi.io/<image>:<tag>
```

## Wiz

[Wiz](https://www.wiz.io/) is a cloud security platform that includes container
image scanning capabilities with support for DHI VEX attestations. Wiz CLI
automatically consumes VEX statements from Docker Hardened Images to provide
accurate vulnerability assessments.

### Scan a DHI using Wiz CLI

After acquiring a Wiz subscription and installing the Wiz CLI, you can scan a
Docker Hardened Image by pulling the image and running the scan command:

```console
$ docker login dhi.io
$ docker pull dhi.io/<image>:<tag>
$ wiz docker scan --image dhi.io/<image>:<tag>
```

## Export VEX attestations

For scanners that need local VEX files (like Grype or Trivy with local files),
you can export the VEX attestations from Docker Hardened Images.

> Note
>
> By default, VEX attestations are fetched from `registry.scout.docker.com`. Ensure that you can access this registry
> if your network has outbound restrictions. You can also mirror the attestations to an alternate registry. For more
> details, see [Mirror to a third-party registry](https://docs.docker.com/dhi/how-to/mirror/#mirror-to-a-third-party-registry).

Export VEX attestations to a JSON file:

```console
$ docker scout vex get dhi.io/<image>:<tag> --output vex.json
```

> Note
>
> The `docker scout vex get` command requires [Docker Scout
> CLI](https://github.com/docker/scout-cli/) version 1.18.3 or later.
>
>
>
> If the image exists locally on your device, you must prefix the image name with `registry://`. For example, use
> `registry://docs/dhi-python:3.13` instead of `docs/dhi-python:3.13`.

---

# Use a Docker Hardened Image

> Learn how to pull, run, and reference Docker Hardened Images in Dockerfiles, CI pipelines, and standard development workflows.

# Use a Docker Hardened Image

   Table of contents

---

You can use a Docker Hardened Image (DHI) just like any other image on Docker
Hub. DHIs follow the same familiar usage patterns. Pull them with `docker pull`,
reference them in your Dockerfile, and run containers with `docker run`.

The key difference is that DHIs are security-focused and intentionally minimal
to reduce the attack surface. This means some variants don't include a shell or
package manager, and may run as a nonroot user by default.

> Important
>
> You must authenticate to the Docker Hardened Images registry (`dhi.io`) to
> pull images. Use your Docker ID credentials (the same username and password
> you use for Docker Hub) when signing in. If you don't have a Docker account,
> [create one](https://docs.docker.com/accounts/create-account/) for free.
>
>
>
> Run `docker login dhi.io` to authenticate.

## Considerations when adopting DHIs

Docker Hardened Images are intentionally minimal to improve security. If you're updating existing Dockerfiles or frameworks to use DHIs, keep the following considerations in mind:

| Feature | Details |
| --- | --- |
| No shell or package manager | Runtime images don’t include a shell or package manager. Use-devor-sdkvariants in build stages to run shell commands or install packages, and then copy artifacts to a minimal runtime image. |
| Non-root runtime | Runtime DHIs default to running as a non-root user. Ensure your application doesn't require privileged access and that all needed files are readable and executable by a non-root user. |
| Ports | Applications running as non-root users can't bind to ports below 1024 in older versions of Docker or in some Kubernetes configurations. Use ports above 1024 for compatibility. |
| Entry point | DHIs may not include a default entrypoint or might use a different one than the original image you're familiar with. Check the image configuration and update yourCMDorENTRYPOINTdirectives accordingly. |
| Multi-stage builds | Always use multi-stage builds for frameworks: a-devimage for building or installing dependencies, and a minimal runtime image for the final stage. |
| TLS certificates | DHIs include standard TLS certificates. You do not need to manually install CA certs. |

If you're migrating an existing application, see [Migrate an existing application to use Docker Hardened Images](https://docs.docker.com/dhi/migration/).

## Use a DHI in a Dockerfile

To use a DHI as the base image for your container, specify it in the `FROM` instruction in your Dockerfile:

```dockerfile
FROM dhi.io/<image>:<tag>
```

Replace the image name and tag with the variant you want to use. For example,
use a `-dev` tag if you need a shell or package manager during build stages:

```dockerfile
FROM dhi.io/python:3.13-dev AS build
```

To learn how to explore available variants, see [Explore images](https://docs.docker.com/dhi/how-to/explore/).

> Tip
>
> Use a multi-stage Dockerfile to separate build and runtime stages, using a
> `-dev` variant in build stages and a minimal runtime image in the final stage.

## Pull a DHI

Just like any other image, you can pull DHIs using tools such as
the Docker CLI or within your CI pipelines.

You can pull Docker Hardened Images from three different locations depending on your needs:

- Directly from `dhi.io`
- From a mirror on Docker Hub
- From a mirror on a third-party registry

To understand which approach is right for your use case, see [Mirror a Docker Hardened Image repository](https://docs.docker.com/dhi/how-to/mirror/).

The following sections show how to pull images from each location.

### Pull directly from dhi.io

After authenticating to `dhi.io`, you can pull images using standard Docker commands:

```console
$ docker login dhi.io
$ docker pull dhi.io/python:3.13
```

Reference images in your Dockerfile:

```dockerfile
FROM dhi.io/python:3.13
COPY . /app
CMD ["python", "/app/main.py"]
```

### Pull from a mirror on Docker Hub

Once you've mirrored a repository to Docker Hub, you can pull images from your organization's namespace:

```console
$ docker login
$ docker pull <your-namespace>/dhi-python:3.13
```

Reference mirrored images in your Dockerfile:

```dockerfile
FROM <your-namespace>/dhi-python:3.13
COPY . /app
CMD ["python", "/app/main.py"]
```

To learn how to mirror repositories, see [Mirror a DHI repository to Docker Hub](https://docs.docker.com/dhi/how-to/mirror/#mirror-a-dhi-repository-to-docker-hub).

### Pull from a mirror on a third-party registry

Once you've mirrored a repository to your third-party registry, you can pull images:

```console
$ docker pull <your-registry>/<your-namespace>/python:3.13
```

Reference third-party mirrored images in your Dockerfile:

```dockerfile
FROM <your-registry>/<your-namespace>/python:3.13
COPY . /app
CMD ["python", "/app/main.py"]
```

To learn more, see [Mirror to a third-party registry](https://docs.docker.com/dhi/how-to/mirror/#mirror-to-a-third-party-registry).

## Run a DHI

After pulling the image, you can run it using `docker run`. For example:

```console
$ docker run --rm dhi.io/python:3.13 python -c "print('Hello from DHI')"
```

## Use a DHI in CI/CD pipelines

Docker Hardened Images work just like any other image in your CI/CD pipelines.
You can reference them in Dockerfiles, pull them as part of a pipeline step, or
run containers based on them during builds and tests.

Unlike typical container images, DHIs also include signed
[attestations](https://docs.docker.com/dhi/core-concepts/attestations/) such as SBOMs and provenance
metadata. You can incorporate these into your pipeline to support supply chain
security, policy checks, or audit requirements if your tooling supports it.

To strengthen your software supply chain, consider adding your own attestations
when building images from DHIs. This lets you document how the image was
built, verify its integrity, and enable downstream validation and policy
enforcement using tools like Docker Scout.

To learn how to attach attestations during the build process, see
[Docker Build
Attestations](https://docs.docker.com/build/metadata/attestations/).

## Use a static image for compiled executables

Docker Hardened Images include a `static` image repository designed specifically
for running compiled executables in an extremely minimal and secure runtime.

Unlike a non-hardened `FROM scratch` image, the DHI `static` image includes all
the attestations needed to verify its integrity and provenance. Although it is
minimal, it includes the common packages needed to run containers securely, such
as `ca-certificates`.

Use a `-dev` or other builder image in an earlier stage to compile your binary,
and copy the output into a `static` image.

The following example shows a multi-stage Dockerfile that builds a Go application
and runs it in a minimal static image:

```dockerfile
#syntax=docker/dockerfile:1

FROM dhi.io/golang:1.22-dev AS build
WORKDIR /app
COPY . .
RUN CGO_ENABLED=0 go build -o myapp

FROM dhi.io/static:20230311
COPY --from=build /app/myapp /myapp
ENTRYPOINT ["/myapp"]
```

This pattern ensures a hardened runtime environment with no unnecessary
components, reducing the attack surface to a bare minimum.

## Use dev variants for framework-based applications

If you're building applications with frameworks that require package managers or
build tools (such as Python, Node.js, or Go), use a `-dev` variant during the
development or build stage. These variants include essential utilities like
shells, compilers, and package managers to support local iteration and CI
workflows.

Use `-dev` images in your inner development loop or in isolated CI stages to
maximize productivity. Once you're ready to produce artifacts for production,
switch to a smaller runtime variant to reduce the attack surface and image size.

Dev variants are typically configured with no `ENTRYPOINT` and a default `CMD` that
launches a shell (for example, ["/bin/bash"]). In those cases, running the
container without additional arguments starts an interactive shell by default.

The following example shows how to build a Python app using a `-dev` variant and
run it using the smaller runtime variant:

```dockerfile
#syntax=docker/dockerfile:1

FROM dhi.io/python:3.13-alpine3.21-dev AS builder

ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

WORKDIR /app

RUN python -m venv /app/venv
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

FROM dhi.io/python:3.13-alpine3.21

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

COPY image.py image.png ./
COPY --from=builder /app/venv /app/venv

ENTRYPOINT [ "python", "/app/image.py" ]
```

This pattern separates the build environment from the runtime environment,
helping reduce image size and improve security by removing unnecessary tooling
from the final image.

## Use compliance variantsDHI Enterprise

Subscription: Docker Hardened Images Enterprise

When you have a Docker Hardened Images Enterprise subscription, you can access
compliance variants such as FIPS-enabled and STIG-ready images. These
variants help meet regulatory and compliance requirements for secure
deployments.

To use a compliance variant, you must first [mirror](https://docs.docker.com/dhi/how-to/mirror/) the
repository, and then pull the compliance image from your mirrored repository.

---

# Verify a Docker Hardened Image or chart

> Use Docker Scout or cosign to verify signed attestations like SBOMs, provenance, and vulnerability data for Docker Hardened Images and charts.

# Verify a Docker Hardened Image or chart

   Table of contents

---

Docker Hardened Images (DHI) and charts include signed attestations that verify
the build process, contents, and security posture. These attestations are
available for each image variant and chart and can be verified using
[cosign](https://docs.sigstore.dev/) or the Docker Scout CLI.

Docker's public key for DHI images and charts is published at:

- [https://registry.scout.docker.com/keyring/dhi/latest.pub](https://registry.scout.docker.com/keyring/dhi/latest.pub)
- [https://github.com/docker-hardened-images/keyring](https://github.com/docker-hardened-images/keyring)

> Important
>
> You must authenticate to the Docker Hardened Images registry (`dhi.io`) to
> pull images. Use your Docker ID credentials (the same username and password
> you use for Docker Hub) when signing in. If you don't have a Docker account,
> [create one](https://docs.docker.com/accounts/create-account/) for free.
>
>
>
> Run `docker login dhi.io` to authenticate.

## Verify image attestations with Docker Scout

You can use the
[Docker Scout](https://docs.docker.com/scout/) CLI to list and retrieve attestations for Docker
Hardened Images.

> Note
>
> Before you run `docker scout attest` commands, ensure any image that you have
> pulled locally is up to date with the remote image. You can do this by running
> `docker pull`. If you don't do this, you may see `No attestation found`.

### Why use Docker Scout instead of cosign directly?

While you can use cosign to verify attestations manually, the Docker Scout CLI
offers several key advantages when working with Docker Hardened Images and charts:

- Purpose-built experience: Docker Scout understands the structure of DHI
  attestations and naming conventions, so you don't have to construct full
  digests or URIs manually.
- Automatic platform resolution: With Scout, you can specify the platform (e.g.,
  `--platform linux/amd64`), and it automatically verifies the correct image
  variant. Cosign requires you to look up the digest yourself.
- Human-readable summaries: Scout returns summaries of attestation contents
  (e.g., package counts, provenance steps), whereas cosign only returns raw
  signature validation output.
- One-step validation: The `--verify` flag in `docker scout attest get` validates
  the attestation and shows the equivalent cosign command, making it easier to
  understand what's happening behind the scenes.
- Integrated with Docker Hub and DHI trust model: Docker Scout is tightly
  integrated with Docker’s attestation infrastructure and public keyring,
  ensuring compatibility and simplifying verification for users within the
  Docker ecosystem.

In short, Docker Scout streamlines the verification process and reduces the chances of human error, while still giving
you full visibility and the option to fall back to cosign when needed.

### List available attestations

To list attestations for a mirrored DHI image:

> Note
>
> If the image exists locally on your device, you must prefix the image name with `registry://`. For example, use
> `registry://dhi.io/python:3.13` instead of `dhi.io/python:3.13`.

```console
$ docker scout attest list dhi.io/<image>:<tag>
```

This command shows all available attestations, including SBOMs, provenance, vulnerability reports, and more.

### Retrieve a specific attestation

To retrieve a specific attestation, use the `--predicate-type` flag with the full predicate type URI:

```console
$ docker scout attest get \
  --predicate-type https://cyclonedx.org/bom/v1.6 \
  dhi.io/<image>:<tag>
```

> Note
>
> If the image exists locally on your device, you must prefix the image name with `registry://`. For example, use
> `registry://dhi.io/python:3.13` instead of `dhi.io/python:3.13`.

For example:

```console
$ docker scout attest get \
  --predicate-type https://cyclonedx.org/bom/v1.6 \
  dhi.io/python:3.13
```

To retrieve only the predicate body:

```console
$ docker scout attest get \
  --predicate-type https://cyclonedx.org/bom/v1.6 \
  --predicate \
  dhi.io/<image>:<tag>
```

For example:

```console
$ docker scout attest get \
  --predicate-type https://cyclonedx.org/bom/v1.6 \
  --predicate \
  dhi.io/python:3.13
```

### Validate the attestation with Docker Scout

To validate the attestation using Docker Scout, you can use the `--verify` flag:

```console
$ docker scout attest get dhi.io/<image>:<tag> \
   --predicate-type https://scout.docker.com/sbom/v0.1 --verify
```

> Note
>
> If the image exists locally on your device, you must prefix the image name
> with `registry://`. For example, use `registry://dhi.io/node:20.19-debian12`
> instead of `dhi.io/node:20.19-debian12`.

For example, to verify the SBOM attestation for the `dhi.io/node:20.19-debian12` image:

```console
$ docker scout attest get dhi.io/node:20.19-debian12 \
   --predicate-type https://scout.docker.com/sbom/v0.1 --verify
```

#### Handle missing transparency log entries

When using `--verify`, you may sometimes see an error like:

```text
ERROR no matching signatures: signature not found in transparency log
```

This occurs because Docker Hardened Images don't always record attestations in
the public [Rekor](https://docs.sigstore.dev/logging/overview/) transparency
log. In cases where an attestation would contain private user information (for
example, your organization's namespace in the image reference), writing it to
Rekor would expose that information publicly.

Even if the Rekor entry is missing, the attestation is still signed with
Docker's public key and can be verified offline by skipping the Rekor
transparency log check.

To skip the transparency log check and validate against Docker's key, use the
`--skip-tlog` flag:

```console
$ docker scout attest get \
  --predicate-type https://cyclonedx.org/bom/v1.6 \
  dhi.io/<image>:<tag> \
  --verify --skip-tlog
```

> Note
>
> The `--skip-tlog` flag is only available in Docker Scout CLI version 1.18.2 and
> later.
>
>
>
> If the image exists locally on your device, you must prefix the image name with `registry://`. For example, use
> `registry://dhi.io/python:3.13` instead of `dhi.io/python:3.13`.

This is equivalent to using `cosign` with the `--insecure-ignore-tlog=true`
flag, which validates the signature against Docker's published public key, but
ignores the transparency log check.

### Show the equivalent cosign command

When using the `--verify` flag, it also prints the corresponding
[cosign](https://docs.sigstore.dev/) command to verify the image signature:

```console
$ docker scout attest get \
  --predicate-type https://cyclonedx.org/bom/v1.6 \
  --verify \
  dhi.io/<image>:<tag>
```

> Note
>
> If the image exists locally on your device, you must prefix the image name with `registry://`. For example, use
> `registry://dhi.io/python:3.13` instead of `dhi.io/python:3.13`.

For example:

```console
$ docker scout attest get \
  --predicate-type https://cyclonedx.org/bom/v1.6 \
  --verify \
  dhi.io/python:3.13
```

If verification succeeds, Docker Scout prints the full `cosign verify` command.

Example output:

```console
v SBOM obtained from attestation, 101 packages found
    v Provenance obtained from attestation
    v cosign verify ...
```

> Important
>
> When using cosign, you must first authenticate to both the DHI registry
> and the Docker Scout registry.
>
>
>
> For example:
>
>
>
> ```console
> $ docker login dhi.io
> $ docker login registry.scout.docker.com
> $ cosign verify ...
> ```

## Verify Helm chart attestations with Docker Scout

Docker Hardened Image Helm charts include the same comprehensive attestations
as container images. The verification process for charts is identical to that
for images, using the same Docker Scout CLI commands.

### List available chart attestations

To list attestations for a DHI Helm chart:

```console
$ docker scout attest list dhi.io/<chart>:<version>
```

For example, to list attestations for the external-dns chart:

```console
$ docker scout attest list dhi.io/external-dns-chart:1.20.0
```

This command shows all available chart attestations, including SBOMs, provenance, vulnerability reports, and more.

### Retrieve a specific chart attestation

To retrieve a specific attestation from a Helm chart, use the `--predicate-type` flag with the full predicate type URI:

```console
$ docker scout attest get \
  --predicate-type https://cyclonedx.org/bom/v1.6 \
  dhi.io/<chart>:<version>
```

For example:

```console
$ docker scout attest get \
  --predicate-type https://cyclonedx.org/bom/v1.6 \
  dhi.io/external-dns-chart:1.20.0
```

To retrieve only the predicate body:

```console
$ docker scout attest get \
  --predicate-type https://cyclonedx.org/bom/v1.6 \
  --predicate \
  dhi.io/<chart>:<version>
```

### Validate chart attestations with Docker Scout

To validate a chart attestation using Docker Scout, use the `--verify` flag:

```console
$ docker scout attest get dhi.io/<chart>:<version> \
   --predicate-type https://scout.docker.com/sbom/v0.1 --verify
```

For example, to verify the SBOM attestation for the external-dns chart:

```console
$ docker scout attest get dhi.io/external-dns-chart:1.20.0 \
   --predicate-type https://scout.docker.com/sbom/v0.1 --verify
```

The same `--skip-tlog` flag described in [Handle missing transparency log
entries](#handle-missing-transparency-log-entries) can also be used with chart
attestations when needed.

## Available DHI attestations

See [available
attestations](https://docs.docker.com/dhi/core-concepts/attestations/#image-attestations) for a list
of attestations available for each DHI image and [Helm chart
attestations](https://docs.docker.com/dhi/core-concepts/attestations/#helm-chart-attestations) for a
list of attestations available for each DHI chart.

## Explore attestations on Docker Hub

You can also browse attestations visually when [exploring an image
variant](https://docs.docker.com/dhi/how-to/explore/#view-image-variant-details). The **Attestations** section
lists each available attestation with its:

- Type (e.g. SBOM, VEX)
- Predicate type URI
- Digest reference for use with `cosign`

These attestations are generated and signed automatically as part of the Docker
Hardened Image or chart build process.
