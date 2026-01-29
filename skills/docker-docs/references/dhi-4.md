# Customize a Docker Hardened Image or chartDHI Enterprise and more

# Customize a Docker Hardened Image or chartDHI Enterprise

> Learn how to customize Docker Hardened Images (DHI) and charts.

# Customize a Docker Hardened Image or chartDHI Enterprise

   Table of contents

---

Subscription: Docker Hardened Images Enterprise

When you have a Docker Hardened Images subscription, you can customize Docker
Hardened Images (DHI) and charts to suit your specific needs using the Docker
Hub web interface. For images, this lets you select a base image, add packages,
add OCI artifacts (such as custom certificates or additional tools), and
configure settings. For charts, this lets you customize the image references.

Your customizations stay secure automatically. When the base Docker Hardened
Image or chart receives a security patch or your OCI artifacts are updated,
Docker automatically rebuilds your customizations in the background. This
ensures continuous compliance and protection by default, with no manual work
required. The rebuilt artifacts are signed and attested to the same SLSA Build
Level 3 standard as the base images and charts, ensuring a secure and verifiable
supply chain.

## Customize a Docker Hardened Image

To add a customized Docker Hardened Image to your organization, an organization
owner must first [mirror](https://docs.docker.com/dhi/how-to/mirror/) the DHI repository to your organization
on Docker Hub. Once the repository is mirrored, any user with access to the
mirrored DHI repository can create a customized image.

### Create an image customization

To customize a Docker Hardened Image, follow these steps:

1. Sign in to [Docker Hub](https://hub.docker.com).
2. Select **My Hub**.
3. In the namespace drop-down, select your organization that has a mirrored DHI
  repository.
4. Select **Hardened Images** > **Manage** > **Mirrored Images**.
5. For the mirrored DHI repository you want to customize, select the menu icon in the far right column.
6. Select **Customize**.
  At this point, the on-screen instructions will guide you through the
  customization process. You can continue with the following steps for more
  details.
7. Select the image version you want to customize.
8. Optional. Add packages.
  1. In the **Packages** drop-down, select the packages you want to add to the
    image.
    The packages available in the drop-down are OS system packages for the
    selected image variant. For example, if you are customizing the Alpine
    variant of the Python DHI, the list will include all Alpine system
    packages.
  2. In the **OCI artifacts** drop-down, first, select the repository that
    contains the OCI artifact image. Then, select the tag you want to use from
    that repository. Finally, specify the specific paths you want to include
    from the OCI artifact image.
    The OCI artifacts are images that you have previously
    built and pushed to a repository in the same namespace as the mirrored
    DHI. For example, you can add a custom root CA certificate or a another
    image that contains a tool you need, like adding Python to a Node.js
    image. For more details on how to create an OCI artifact image, see
    [Create an OCI artifact image](#create-an-oci-artifact-image-for-image-customization).
    When combining images that contain directories and files with the same
    path, images later in the list will overwrite files from earlier images.
    To manage this, you must select paths to include and optionally exclude
    from each OCI artifact image. This allows you to control which files are
    included in the final customized image.
    By default, no files are included from the OCI artifact image. You must
    explicitly include the paths you want. After including a path, you can
    then explicitly exclude files or directories underneath it.
    > Note
    >
    > When files necessary for runtime are overwritten by OCI artifacts, the
    > image build still succeeds, but you may have issues when running the
    > image.
  3. In the **Scripts** section, you can add, edit, or remove scripts.
    Scripts let you add files to the container image that you can access at runtime. They are not executed during
    the build process. This is useful for services that require pre-start initialization, such as setup scripts or
    file writes to directories like `/var/lock` or `/out`.
    You must specify the following:
    - The path where the script will be placed
    - The script content
    - The UID and GID ownership of the script
    - The octal file permissions of the script
9. Select **Next: Configure** to configure the following image settings:
  1. Specify the
    [environment variables](https://docs.docker.com/reference/dockerfile/#env) and their
    values that the image will contain.
  2. Add
    [labels](https://docs.docker.com/reference/dockerfile/#label) to the image.
  3. Add
    [annotations](https://docs.docker.com/build/metadata/annotations/) to the image.
  4. Specify the users to add to the image.
  5. Specify the user groups to add to the image.
  6. Select which
    [user](https://docs.docker.com/reference/dockerfile/#user) to run the images as.
  7. Add
    [ENTRYPOINT](https://docs.docker.com/reference/dockerfile/#entrypoint) arguments to the
    image. These arguments are appended to the base image's entrypoint.
  8. Add
    [CMD](https://docs.docker.com/reference/dockerfile/#cmd) arguments to the image. These
    arguments are appended to the base image's command.
  9. Override the default (`/`)
    [working
    directory](https://docs.docker.com/reference/dockerfile/#workdir) for the image.
  10. Specify a suffix for the customization name that is appended to the
    customized image's tag. For example, if you specify `custom` when
    customizing the `dhi-python:3.13` image, the customized image will be
    tagged as `dhi-python:3.13_custom`.
  11. Select the platforms you want to build the image for. You must select at
    least one platform.
10. Select **Next: Review customization**.
11. Select **Create Customization**.
  A summary of the customization appears. It may take some time for the image
  to build. Once built, it will appear in the **Tags** tab of the repository,
  and your team members can pull it like any other image.

### Create an OCI artifact image for image customization

An OCI artifact image is a Docker image that contains files or directories that
you want to include in your customized Docker Hardened Image (DHI). This can
include additional tools, libraries, or configuration files.

When creating an image to use as an OCI artifact, it should ideally be as
minimal as possible and contain only the necessary files.

For example, to distribute a custom root CA certificate as part of a trusted CA
bundle, you can use a multi-stage build. This approach registers your
certificate with the system and outputs an updated CA bundle, which can be
extracted into a minimal final image:

```dockerfile
# syntax=docker/dockerfile:1

FROM dhi.io/bash:5-dev AS certs

ENV DEBIAN_FRONTEND=noninteractive

RUN mkdir -p /usr/local/share/ca-certificates/my-rootca
COPY certs/rootCA.crt /usr/local/share/ca-certificates/my-rootca

RUN update-ca-certificates

FROM scratch
COPY --from=certs /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
```

You can follow this pattern to create other OCI artifacts, such as images
containing tools or libraries that you want to include in your customized DHI.
Install the necessary tools or libraries in the first stage, and then copy the
relevant files to the final stage that uses `FROM scratch`. This ensures that
your OCI artifact is minimal and contains only the necessary files.

In order for the OCI artifact to be available in a DHI customization, it must be built and
pushed to a repository in the same namespace as the mirrored DHI repository.

If you're customizing a DHI for multiple platforms (such as `linux/amd64` and
`linux/arm64`), build your OCI artifact for all the platforms using the
`--platform` flag:

```console
$ docker buildx build --platform linux/amd64,linux/arm64 \
  -t <your-namespace>/my-oci-artifact:latest \
  --push .
```

This creates a single image manifest that you can use for each platform. The
customization build system automatically selects the correct platform variant
when building each customized image.

> Important
>
> The customization UI will only allow you to select platforms that are
> available in all OCI artifacts you've added. If a platform is missing from
> any OCI artifact, you won't be able to select that platform for your
> customization.

Once pushed to a repository in your organization's namespace, the OCI artifact
automatically appears in the customization workflow when you select OCI
artifacts to add to your customized Docker Hardened Image.

#### Best practices for OCI artifacts

Follow these best practices when creating OCI artifacts for DHI customizations:

- Use multi-stage builds: Build or install dependencies in a builder stage,
  then copy only the necessary files to a `FROM scratch` final stage. This keeps
  the OCI artifact minimal and free of unnecessary build tools.
- Include only essential files: OCI artifacts should contain only the files
  you need to add to the customized image. Avoid including package managers,
  shells, or other utilities that won't be used in the final image.
- Match target platforms: Build your OCI artifact for all platforms you plan
  to use in your customizations. Use `docker buildx build --platform` to create
  multi-platform images when needed.
- Use specific tags: Tag your OCI artifacts with specific versions or dates
  (like `v1.0` or `20250101`) rather than relying solely on `latest`. This
  ensures reproducible builds and makes it easier to track which artifacts are
  used in which customizations.
- Enable immutable tags: Consider enabling [immutable
  tags](https://docs.docker.com/docker-hub/repos/manage/hub-images/immutable-tags/) for your
  OCI artifact repositories. This prevents accidental overwrites and ensures that
  each version of your OCI artifact remains unchanged, improving reproducibility
  and reliability of your customizations.

## Customize a DHI Helm chart

You can customize DHI Helm charts to meet your organization's specific needs.
Via the Docker Hub web interface, you can modify the image references to
reference mirrored images or customized images you've created. This lets you
create a custom, securely-built chart with references to images stored in Docker
Hub or other private registries. DHI securely packages customized Helm charts
that reference your repositories, wherever they are stored, by default.

To customize image references, an organization owner must [mirror](https://docs.docker.com/dhi/how-to/mirror/)
the DHI chart repository to your organization on Docker Hub.

You can create one chart customization per Helm chart repository. This is
different from image customizations, where you can create multiple
customizations per repository. If you need to make changes, you can edit your
existing customization. Alternatively, you can mirror the same Helm chart
repository again and add a new customization to the new mirror.

> Note
>
> You can customize Docker Hardened Image charts like any other Helm chart using
> standard Helm tools and practices, such as a `values.yaml` file, outside of
> Docker Hub. The following instructions describe how to customize image
> references for the chart using the Docker Hub web interface.

To customize a Docker Hardened Image Helm chart after it has been mirrored:

1. Sign in to [Docker Hub](https://hub.docker.com).
2. Select **My Hub**.
3. In the namespace drop-down, select your organization that has a mirrored DHI
  repository.
4. Select **Hardened Images** > **Manage** > **Mirrored Helm charts**.
5. For the mirrored DHI repository you want to customize, select the **Name**.
6. Select the **Customizations** tab.
7. Select **Create customization**.
  At this point, the on-screen instructions will guide you through the
  customization process.

## Edit or delete a customization

To edit or delete a DHI or chart customization, follow these steps:

1. Sign in to [Docker Hub](https://hub.docker.com).
2. Select **My Hub**.
3. In the namespace drop-down, select your organization that has a mirrored repository.
4. Select **Hardened Images** > **Manage**.
5. Select **Customizations**.
6. For the customized DHI repository you want to manage, select the menu icon in the far right column.
  From here, you can:
  - **Edit**: Edit the customization.
  - **Create new**: Create a new customization based on the source repository.
  - **Delete**: Delete the customization.
7. Follow the on-screen instructions to complete the edit or deletion.

---

# Debug a Docker Hardened Image container

> Learn how to use Docker Debug to troubleshoot Docker Hardened Images (DHI) locally or in production.

# Debug a Docker Hardened Image container

   Table of contents

---

Docker Hardened Images (DHI) prioritize minimalism and security, which means
they intentionally leave out many common debugging tools (like shells or package
managers). This makes direct troubleshooting difficult without introducing risk.
To address this, you can use [Docker
Debug](https://docs.docker.com/reference/cli/docker/debug/), a secure workflow that
temporarily attaches an ephemeral debug container to a running service or image
without modifying the original image.

This guide shows how to debug Docker Hardened Images locally during development.
With Docker Debug, you can also debug containers remotely using the `--host`
option.

## Use Docker Debug

### Step 1: Run a container from a Hardened Image

Start with a DHI-based container that simulates an issue:

```console
$ docker run -d --name myapp dhi.io/python:3.13 python -c "import time; time.sleep(300)"
```

This container doesn't include a shell or tools like `ps`, `top`, or `cat`.

If you try:

```console
$ docker exec -it myapp sh
```

You'll see:

```console
exec: "sh": executable file not found in $PATH
```

### Step 2: Use Docker Debug to inspect the container

Use the `docker debug` command to attach a temporary, tool-rich debug container to the running instance.

```console
$ docker debug myapp
```

From here, you can inspect running processes, network status, or mounted files.

For example, to check running processes:

```console
$ ps aux
```

Type `exit` to leave the container when done.

## Alternative debugging approaches

In addition to using Docker Debug, you can also use the following approaches for
debugging DHI containers.

### Use the -dev variant

Docker Hardened Images offer a `-dev` variant that includes a shell
and a package manager to install debugging tools. Simply replace the image tag
with `-dev`:

```console
$ docker run -it --rm dhi.io/python:3.13-dev sh
```

Type `exit` to leave the container when done. Note that using the `-dev` variant
increases the attack surface and it is not recommended as a runtime for
production environments.

### Mount debugging tools with image mounts

You can use the image mount feature to mount debugging tools into your container
without modifying the base image.

#### Step 1: Run a container from a Hardened Image

Start with a DHI-based container that simulates an issue:

```console
$ docker run -d --name myapp dhi.io/python:3.13 python -c "import time; time.sleep(300)"
```

#### Step 2: Mount debugging tools into the container

Run a new container that mounts a tool-rich image (like `busybox`) into
the running container's namespace:

```console
$ docker run --rm -it --pid container:myapp \
  --mount type=image,source=busybox,destination=/dbg,ro \
  dhi.io/python:3.13 /dbg/bin/sh
```

This mounts the BusyBox image at `/dbg`, giving you access to its tools while
keeping your original container image unchanged. Since the hardened Python image
doesn't include standard utilities, you need to use the full path to the mounted
tools:

```console
$ /dbg/bin/ls /
$ /dbg/bin/ps aux
$ /dbg/bin/cat /etc/os-release
```

Type `exit` to leave the container when done.

## What's next

This guide covered three approaches for debugging Docker Hardened Images:

- Docker Debug: Attach an ephemeral debug container without modifying the original image
- `-dev` variants: Use development images that include debugging tools
- Image mount: Mount tool-rich images like BusyBox to access debugging utilities

Each method helps you troubleshoot hardened containers while maintaining
security. Docker Debug and image mounts avoid modifying your production images,
while `-dev` variants provide convenience during development.

If you encounter issues related to permissions, ports, missing shells, or
package managers, see [Troubleshoot Docker Hardened Images](https://docs.docker.com/dhi/troubleshoot/)
for recommended solutions and workarounds.

---

# Use Extended Lifecycle Support for Docker Hardened ImagesDHI Enterprise

> Learn how to use Extended Lifecycle Support with Docker Hardened Images.

# Use Extended Lifecycle Support for Docker Hardened ImagesDHI Enterprise

   Table of contents

---

Subscription: Docker Hardened Images Enterprise

With a Docker Hardened Images subscription add-on, you can use Extended
Lifecycle Support (ELS) for Docker Hardened Images. ELS provides security
patches for end-of-life (EOL) image versions, letting you maintain secure,
compliant operations while planning upgrades on your own timeline. You can use
ELS images like any other Docker Hardened Image, but you must enable ELS for
each repository you want to use with ELS.

## Discover repositories with ELS support

To find images with ELS support:

1. Go to [Docker Hub](https://hub.docker.com) and sign in.
2. Select **My Hub**.
3. In the namespace drop-down, select your organization.
4. Select **Hardened Images** > **Catalog**.
5. In **Filter by**, select **Extended Lifecycle Support**.

## Enable ELS for a repository

To enable ELS for a repository, an organization owner must [mirror](https://docs.docker.com/dhi/how-to/mirror/)
the repository to your organization.

To enable ELS when mirroring:

1. Go to [Docker Hub](https://hub.docker.com) and sign in.
2. Select **My Hub**.
3. In the namespace drop-down, select your organization.
4. Select **Hardened Images** > **Catalog**.
5. Select a DHI repository to view its details.
6. Select **Use this image** > **Mirror repository**
7. Select **Enable support for end-of-life versions** and then follow the
  on-screen instructions.

## Disable ELS for a repository

To disable ELS for a repository, you must uncheck the ELS option in the mirrored
repository's **Settings** tab, or stop mirroring the repository. To stop mirroring, see
[Stop mirroring a repository](https://docs.docker.com/dhi/how-to/mirror/#stop-mirroring-a-repository).

To update settings:

1. Go to [Docker Hub](https://hub.docker.com) and sign in.
2. Select **My Hub**.
3. In the namespace drop-down, select your organization.
4. Select **Repositories** and then select the mirrored repository.
5. Select the **Settings** tab.
6. Uncheck the **Mirror end-of-life images** option.

## Manage ELS repositories

You can view and manage your mirrored repositories with ELS like any other
mirrored DHI repository. For more details, see [Manage images](https://docs.docker.com/dhi/how-to/manage/).

---

# Explore Docker Hardened Images

> Learn how to find and evaluate image repositories, variants, metadata, and attestations in the DHI catalog on Docker Hub.

# Explore Docker Hardened Images

   Table of contents

---

Docker Hardened Images (DHI) are a curated set of secure, production-ready
container images. This page explains how to explore available DHI repositories,
review image metadata, examine variant details, and understand the security
attestations provided. Use this information to evaluate and select the right
image variants for your applications.

## Explore Docker Hardened Images

To explore Docker Hardened Images (DHI):

1. Go to [Docker Hub](https://hub.docker.com) and sign in.
2. Select **My Hub**.
3. In the namespace drop-down, select your organization that has access to DHI.
4. Select **Hardened Images** > **Catalog**.

On the DHI page, you can browse images, search images, or filter images by
category.

## View repository details

To view repository details:

1. Go to [Docker Hub](https://hub.docker.com) and sign in.
2. Select **My Hub**.
3. In the namespace drop-down, select your organization that has access to DHI.
4. Select **Hardened Images** > **Catalog**.
5. Select a repository in the DHI catalog list.

The repository details page provides the following:

- Overview: A brief explanation of the image.
- Guides: Several guides on how to use the image and migrate your existing application.
- Tags: Select this option to [view image variants](#view-image-variants).
- Security summary: Select a tag name to view a quick security summary,
  including package count, total known vulnerabilities, and Scout health score.
- Recently pushed tags: A list of recently updated image variants and when they
  were last updated.
- Mirror to repository: Select this option to mirror the image to your
  organization's repository in order to use it. Only organization owners can mirror a repository.
- View in repository: After a repository has been mirrored, you can select this
  option to view where the repository has been mirrored, or mirror it to another repository.

## View image variants

Tags are used to identify image variants. Image variants are different builds of
the same application or framework tailored for different use-cases.

To explore image variants:

1. Go to [Docker Hub](https://hub.docker.com) and sign in.
2. Select **My Hub**.
3. In the namespace drop-down, select your organization that has access to DHI.
4. Select **Hardened Images** > **Catalog**.
5. Select a repository in the DHI catalog list.
6. Select **Tags**.

The **Tags** page provides the following information:

- Tags: A list of all available tags, also known as image variants.
- Compliance: Lists relevant compliance designations. For example, `FIPS` or `STIG`.
- Distribution: The distribution that the variant is based on. For example, `debian 12` or `alpine 3.21`.
- Package manager: The package manager that is available in the variant. For example, `apt`, `apk`, or `-` (no package manager).
- Shell: The shell that is available in the variant. For example, `bash`, `busybox`, or `-` (no shell).
- User: The user that the container runs as. For example, `root`, `nonroot (65532)`, or `node (1000)`.
- Last pushed: The amount of days ago that the image variant was last pushed.
- Vulnerabilities: The amount of vulnerabilities in the variant based on the severity.
- Health: The Scout health score for the variant. Select the score icon to get more details.

> Note
>
> Unlike most images on Docker Hub, Docker Hardened Images do not use the
> `latest` tag. Each image variant is published with a full semantic version tag
> (for example, `3.13`, `3.13-dev`) and is kept up to date. If you need to pin
> to a specific image release for reproducibility, you can reference the image
> by its [digest](https://docs.docker.com/dhi/core-concepts/digests/).

## View image variant details

To explore the details of an image variant:

1. Go to [Docker Hub](https://hub.docker.com) and sign in.
2. Select **My Hub**.
3. In the namespace drop-down, select your organization that has access to DHI.
4. Select **Hardened Images** > **Catalog**.
5. Select a repository in the DHI catalog list.
6. Select **Tags**.
7. Select the image variant's tag in the table.

The image variant details page provides the following information:

- Packages: A list of all packages included in the image variant. This section
  includes details about each package, including its name, version,
  distribution, and licensing information.
- Specifications: The specifications for the image variant include the following
  key details:
  - Source & Build Information: The image is built from the Dockerfile found
    here and the Git commit.
  - Build parameters
  - Entrypoint
  - CMD
  - User
  - Working directory
  - Environment Variables
  - Labels
  - Platform
- Vulnerabilities: The vulnerabilities section provides a list of known CVEs for
  the image variant, including:
  - CVE
  - Severity
  - Package
  - Fix version
  - Last detected
  - Status
  - Suppressed CVEs
- Attestations: Variants include comprehensive security attestations to verify
  the image's build process, contents, and security posture. These attestations
  are signed and can be verified using cosign. For a list of available
  attestations, see [Attestations](https://docs.docker.com/dhi/core-concepts/attestations/).

---

# Use a Docker Hardened Image chart

> Learn how to use a Docker Hardened Image chart.

# Use a Docker Hardened Image chart

   Table of contents

---

Docker Hardened Image (DHI) charts are Docker-provided [Helm
charts](https://helm.sh/docs/) built from upstream sources, designed for
compatibility with Docker Hardened Images. These charts are available as OCI
artifacts within the DHI catalog on Docker Hub. For more details, see
[Docker
Hardened Image charts](https://docs.docker.com/dhi/features/helm/).

DHI charts incorporate multiple layers of supply chain security that aren't present in upstream charts:

- SLSA Level 3 compliance: Each chart is built with SLSA Build Level 3 standards, including detailed build provenance
- Software Bill of Materials (SBOMs): Comprehensive SBOMs detail all components referenced within the chart
- Cryptographic signing: All associated metadata is cryptographically signed by Docker for integrity and authenticity
- Hardened configuration: Charts automatically reference Docker Hardened Images for secure deployments
- Tested compatibility: Charts are robustly tested to work out-of-the-box with Docker Hardened Images

You can use a DHI chart like any other Helm chart stored in an OCI registry.
When you have a Docker Hardened Images subscription, you can also customize DHI
charts to reference customized images and mirrored repositories. The customized
chart build pipeline ensures that your customizations are built securely, use
the latest base charts, and include attestations.

## Find a Docker Helm chart

To find a Docker Helm chart for DHI:

1. Go to the Hardened Images catalog in [Docker Hub](https://hub.docker.com/hardened-images/catalog) and sign in.
2. In the left sidebar, select **Hardened Images** > **Catalog**.
3. Select **Filter by** for **Helm Charts**.
4. Select a Helm chart repository to view its details.

## Mirror a Helm chart and/or its images to a third-party registry

If you want to mirror to your own third-party registry, you can follow the
instructions in
[Mirror a Docker Hardened Image repository](https://docs.docker.com/dhi/how-to/mirror/) for either the
chart, the image, or both.

The same `regctl` tool that is used for mirroring container images can also be used for mirroring Helm charts, as Helm
charts are OCI artifacts.

For example:

```console
regctl image copy \
    "${SRC_CHART_REPO}:${TAG}" \
    "${DEST_REG}/${DEST_CHART_REPO}:${TAG}" \
    --referrers \
    --referrers-src "${SRC_ATT_REPO}" \
    --referrers-tgt "${DEST_REG}/${DEST_CHART_REPO}" \
    --force-recursive
```

## Create a Kubernetes secret for pulling images

You need to create a Kubernetes secret for pulling images from `dhi.io`, Docker
Hub, or your own registry. This is necessary because Docker Hardened Image
repositories require authentication. If you mirror the images to your own
registry, you still need to create this secret if the registry requires
authentication.

1. For `dhi.io` or Docker Hub, create a
  [personal access token
  (PAT)](https://docs.docker.com/security/access-tokens/) using your Docker account or an
  [organization access token (OAT)](https://docs.docker.com/enterprise/security/access-tokens/).
  Ensure the token has at least read-only access to the Docker Hardened Image
  repositories.
2. Create a secret in Kubernetes using the following command. Replace `<your-secret-name>`, `<your-username>`,
  `<your-personal-access-token>`, and `<your-email>` with your own values.
  > Note
  >
  > You need to create this secret in each Kubernetes namespace that uses a
  > DHI. If you've mirror your DHIs to another registry, replace
  > `dhi.io` with your registry's hostname. Replace
  > `<your-username>`, `<your-access-token>`, and `<your-email>` with your own
  > values. `<your-username>` is Docker ID if using a PAT or your organization
  > name if using an OAT. `<your-secret-name>` is a name you choose for the
  > secret.
  ```console
  $ kubectl create secret docker-registry <your-secret-name> \
      --docker-server=dhi.io \
      --docker-username=<your-username> \
      --docker-password=<your-access-token> \
      --docker-email=<your-email>
  ```
  For example:
  ```console
  $ kubectl create secret docker-registry dhi-pull-secret \
      --docker-server=dhi.io \
      --docker-username=docs \
      --docker-password=dckr_pat_12345 \
      --docker-email=moby@example.com
  ```

## Install a Helm chart

To install a Helm chart from Docker Hardened Images:

1. Sign in to the registry using Helm:
  ```console
  $ echo $ACCESS_TOKEN | helm registry login dhi.io --username <your-username> --password-stdin
  ```
  Replace `<your-username>` and set `$ACCESS_TOKEN`.
2. Install the chart using `helm install`. Optionally, you can also use the `--dry-run` flag to test the installation without
  actually installing anything.
  ```console
  $ helm install <release-name> oci://dhi.io/<helm-chart-repository> --version <chart-version> \
    --set "imagePullSecrets[0].name=<your-secret-name>"
  ```
  Replace `<helm-chart-repository>` and `<chart-version>` accordingly. If the
  chart is in your own registry or another repository, replace
  `dhi.io/<helm-chart-repository>` with your own location. Replace
  `<your-secret-name>` with the name of the image pull secret created
  from [Create a Kubernetes secret for pulling images](#create-a-kubernetes-secret-for-pulling-images).

## Customize a Helm chart

You can customize Docker Hardened Image Helm charts to reference customized
images and mirrored repositories. For more details, see [Customize Docker
Hardened Images and charts](https://docs.docker.com/dhi/how-to/customize/).

## Verify a Helm chart and view its attestations

You can verify Helm charts. For more details, see [Verify Helm chart attestations](https://docs.docker.com/dhi/how-to/verify/#verify-helm-chart-attestations-with-docker-scout).

---

# Use a Docker Hardened Image in Kubernetes

> Learn how to use Docker Hardened Images in Kubernetes deployments.

# Use a Docker Hardened Image in Kubernetes

   Table of contents

---

## Authentication

To be able to use Docker Hardened Images in Kubernetes, you need to create a
Kubernetes secret for pulling images from your mirror or internal registry.

> Note
>
> You need to create this secret in each Kubernetes namespace that uses a DHI.

Create a secret using a Personal Access Token (PAT). Ensure the token has at
least read-only access to public repositories. For Docker Hardened Images
replace `<registry server>` with `dhi.io`. If you are using a mirrored
repository, replace it with your mirror's registry server, such as `docker.io`
for Docker Hub.

```console
$ kubectl create -n <kubernetes namespace> secret docker-registry <secret name> --docker-server=<registry server> \
        --docker-username=<registry user> --docker-password=<access token> \
        --docker-email=<registry email>
```

To tests the secrets use the following command:

```console
kubectl apply --wait -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: dhi-test
  namespace: <kubernetes namespace>
spec:
  containers:
  - name: test
    image: bash:5
    command: [ "sh", "-c", "echo 'Hello from DHI in Kubernetes!'" ]
  imagePullSecrets:
  - name: <secret name>
EOF
```

Get the status of the pod by running:

```console
$ kubectl get -n <kubernetes namespace> pods/dhi-test
```

The command should return the following result:

```console
NAME       READY   STATUS      RESTARTS     AGE
dhi-test   0/1     Completed   ...          ...
```

If instead, the result is the following, there might be an issue with your secret.

```console
NAME       READY   STATUS         RESTARTS   AGE
dhi-test   0/1     ErrImagePull   0          ...
```

Verify the output of the pod by running, which should return `Hello from DHI in Kubernetes!`

```console
kubectl logs -n <kubernetes namespace> pods/dhi-test
```

After a successful test, the test pod can be deleted with the following command:

```console
$ kubectl delete -n <kubernetes namespace> pods/dhi-test
```

---

# Manage Docker Hardened Images and chartsDHI Enterprise

> Learn how to manage your mirrored and customized Docker Hardened Images in your organization.

# Manage Docker Hardened Images and chartsDHI Enterprise

   Table of contents

---

Subscription: Docker Hardened Images Enterprise

On the **Manage** screen in Docker Hub, you can manage your mirrored Docker
Hardened Image (DHI) repositories, mirrored DHI chart repositories, and
customizations in your organization.

## Manage mirrored Docker Hardened Image repositories

To manage your mirrored DHI repositories:

1. Go to the [Docker Hub](https://hub.docker.com) and sign in.
2. Select **My Hub**.
3. In the namespace drop-down, select your organization.
4. Select **Hardened Images** > **Manage**.
5. Select **Mirrored Images**
6. Select the menu icon in the far right column of the repository you want to manage.
  From here, you can:
  - **Customize**: Create a customized image based on the source repository.
  - **Stop mirroring**: Stop mirroring the DHI repository.

## Manage customized Docker Hardened Image repositories

To manage your customized DHI repositories:

1. Go to [Docker Hub](https://hub.docker.com) and sign in.
2. Select **My Hub**.
3. In the namespace drop-down, select your organization.
4. Select **Hardened Images** > **Manage**.
5. Select **Customizations**.
  On this page, you can view your customized DHI
  repositories.
6. Select the menu icon in the far right column of the repository you want to manage.
  From here, you can:
  - **Edit**: Edit the customized image.
  - **Create new**: Create a new customized image based on the source repository.
  - **Delete**: Delete the customized image.
