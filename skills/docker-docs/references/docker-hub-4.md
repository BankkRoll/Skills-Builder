# Software artifacts on Docker Hub and more

# Software artifacts on Docker Hub

> You can use Docker Hub to store software artifacts packaged as OCI artifacts.

# Software artifacts on Docker Hub

   Table of contents

---

You can use Docker Hub to store any kind of software artifact, not just
container images. A software artifact is any item produced during the software
development process that contributes to the creation, maintenance, or
understanding of the software. Docker Hub supports OCI artifacts by leveraging
the config property on the image manifest.

## What are OCI artifacts?

OCI artifacts are any arbitrary files related to a software application. Some
examples include:

- Helm charts
- Software Bill of Materials (SBOM)
- Digital signatures
- Provenance data
- Attestations
- Vulnerability reports

Docker Hub supporting OCI artifacts means you can use one repository for storing
and distributing container images as well as other assets.

A common use case for OCI artifacts is
[Helm charts](https://helm.sh/docs/topics/charts/). Helm charts is a packaging
format that defines a Kubernetes deployment for an application. Since Kubernetes
is a popular runtime for containers, it makes sense to host application images
and deployment templates all in one place.

## Using OCI artifacts with Docker Hub

You manage OCI artifacts on Docker Hub in a similar way you would container
images.

Pushing and pulling OCI artifacts to and from a registry is done using a
registry client. [ORAS CLI](https://oras.land/docs/installation)
is a command-line tool that provides the capability of managing
OCI artifacts in a registry. If you use Helm charts, the
[Helm CLI](https://helm.sh/docs/intro/install/) provides built-in
functionality for pushing and pulling charts to and from a registry.

Registry clients invoke HTTP requests to the Docker Hub registry API. The
registry API conforms to a standard protocol defined in the
[OCI distribution specification](https://github.com/opencontainers/distribution-spec).

## Examples

This section shows some examples on using OCI artifacts with Docker Hub.

### Push a Helm chart

The following procedure shows how to push a Helm chart as an OCI artifact to
Docker Hub.

Prerequisites:

- Helm version 3.0.0 or later

Steps:

1. Create a new Helm chart
  ```console
  $ helm create demo
  ```
  This command generates a boilerplate template chart.
2. Package the Helm chart into a tarball.
  ```console
  $ helm package demo
  Successfully packaged chart and saved it to: /Users/hubuser/demo-0.1.0.tgz
  ```
3. Sign in to Docker Hub with Helm, using your Docker credentials.
  ```console
  $ helm registry login registry-1.docker.io -u hubuser
  ```
4. Push the chart to a Docker Hub repository.
  ```console
  $ helm push demo-0.1.0.tgz oci://registry-1.docker.io/docker
  ```
  This uploads the Helm chart tarball to a `demo` repository in the `docker`
  namespace.
5. Go to the repository page on Docker Hub. The **Tags** section of the page
  shows the Helm chart tag.
  ![List of repository tags](https://docs.docker.com/docker-hub/repos/manage/hub-images/images/oci-helm.png)  ![List of repository tags](https://docs.docker.com/docker-hub/repos/manage/hub-images/images/oci-helm.png)
6. Select the tag name to go to the page for that tag.
  The page lists a few useful commands for working with Helm charts.
  ![Tag page of a Helm chart artifact](https://docs.docker.com/docker-hub/repos/manage/hub-images/images/oci-helm-tagview.png)  ![Tag page of a Helm chart artifact](https://docs.docker.com/docker-hub/repos/manage/hub-images/images/oci-helm-tagview.png)

### Push a volume

The following procedure shows how to push container volume as an OCI artifact to
Docker Hub.

Prerequisites:

- ORAS CLI version 0.15 or later

Steps:

1. Create a dummy file to use as volume content.
  ```console
  $ touch myvolume.txt
  ```
2. Sign in to Docker Hub using the ORAS CLI.
  ```console
  $ oras login -u hubuser registry-1.docker.io
  ```
3. Push the file to Docker Hub.
  ```console
  $ oras push registry-1.docker.io/docker/demo:0.0.1 \
    --artifact-type=application/vnd.docker.volume.v1+tar.gz \
    myvolume.txt:text/plain
  ```
  This uploads the volume to a `demo` repository in the `docker` namespace. The
  `--artifact-type` flag specifies a special media type that makes Docker Hub
  recognize the artifact as a container volume.
4. Go to the repository page on Docker Hub. The **Tags** section on that page
  shows the volume tag.
  ![Repository page showing a volume in the tag list](https://docs.docker.com/docker-hub/repos/manage/hub-images/images/oci-volume.png)  ![Repository page showing a volume in the tag list](https://docs.docker.com/docker-hub/repos/manage/hub-images/images/oci-volume.png)

### Push a generic artifact file

The following procedure shows how to push a generic OCI artifact to Docker Hub.

Prerequisites:

- ORAS CLI version 0.15 or later

Steps:

1. Create your artifact file.
  ```console
  $ touch myartifact.txt
  ```
2. Sign in to Docker Hub using the ORAS CLI.
  ```console
  $ oras login -u hubuser registry-1.docker.io
  ```
3. Push the file to Docker Hub.
  ```console
  $ oras push registry-1.docker.io/docker/demo:0.0.1 myartifact.txt:text/plain
  ```
4. Go to the repository page on Docker Hub. The **Tags** section on that page
  shows the artifact tag.
  ![Repository page showing an artifact in the tag list](https://docs.docker.com/docker-hub/repos/manage/hub-images/images/oci-artifact.png)  ![Repository page showing an artifact in the tag list](https://docs.docker.com/docker-hub/repos/manage/hub-images/images/oci-artifact.png)

---

# Push images to a repository

> Learn how to add content to a repository on Docker Hub.

# Push images to a repository

---

To add content to a repository on Docker Hub, you need to tag your Docker image
and then push it to your repository. This process lets you share your
images with others or use them in different environments.

1. Tag your Docker image.
  The `docker tag` command assigns a tag to your Docker image, which includes
  your Docker Hub namespace and the repository name. The general syntax is:
  ```console
  $ docker tag [SOURCE_IMAGE[:TAG]] [NAMESPACE/REPOSITORY[:TAG]]
  ```
  Example:
  If your local image is called `my-app` and you want to tag it for the
  repository `my-namespace/my-repo` with the tag `v1.0`, run:
  ```console
  $ docker tag my-app my-namespace/my-repo:v1.0
  ```
2. Push the image to Docker Hub.
  Use the `docker push` command to upload your tagged image to the specified
  repository on Docker Hub.
  Example:
  ```console
  $ docker push my-namespace/my-repo:v1.0
  ```
  This command pushes the image tagged `v1.0` to the `my-namespace/my-repo` repository.
3. Verify the image on Docker Hub.

---

# Tags on Docker Hub

> Discover how to manage repository tags on Docker Hub.

# Tags on Docker Hub

   Table of contents

---

Tags let you manage multiple versions of images within a single Docker Hub
repository. By adding a specific `:<tag>` to each image, such as
`docs/base:testing`, you can organize and differentiate image versions for
various use cases. If no tag is specified, the image defaults to the `latest`
tag.

## Tag a local image

To tag a local image, use one of the following methods:

- When you build an image, use `docker build -t <org-or-user-namespace>/<repo-name>[:<tag>`.
- Re-tag an existing local image with `docker tag <existing-image> <org-or-user-namespace>/<repo-name>[:<tag>]`.
- When you commit changes, use `docker commit <existing-container> <org-or-user-namespace>/<repo-name>[:<tag>]`.

Then, you can push this image to the repository designated by its name or tag:

```console
$ docker push <org-or-user-namespace>/<repo-name>:<tag>
```

The image is then uploaded and available for use in Docker Hub.

## View repository tags

You can view the available tags and the size of the associated image.

1. Sign in to [Docker Hub](https://hub.docker.com).
2. Select **My Hub** > **Repositories**.
  A list of your repositories appears.
3. Select a repository.
  The **General** page for the repository appears.
4. Select the **Tags** tab.

You can select a tag's digest to see more details.

## Delete repository tags

Only the repository owner or other team members with granted permissions can
delete tags.

1. Sign in to [Docker Hub](https://hub.docker.com).
2. Select **My Hub** > **Repositories**.
  A list of your repositories appears.
3. Select a repository.
  The **General** page for the repository appears.
4. Select the **Tags** tab.
5. Select the corresponding checkbox next to the tags to delete.
6. Select **Delete**.
  A confirmation dialog appears.
7. Select **Delete**.

---

# Image management

> Learn how to manage images in Docker Hub repositories

# Image management

---

Docker Hub provides powerful features for managing and organizing your
repository content, ensuring that your images and artifacts are accessible,
version-controlled, and easy to share. This section covers key image management
tasks, including tagging, pushing images, transferring images between
repositories, and supported software artifacts.

- [Tags](https://docs.docker.com/docker-hub/repos/manage/hub-images/tags/): Tags help you version and organize different iterations of
  your images within a single repository. This topic explains tagging and
  provides guidance on how to create, view, and delete tags in Docker Hub.
- [Image Management](https://docs.docker.com/docker-hub/repos/manage/hub-images/manage/): Manage your images and image indexes to
  optimize your repository storage.
- [Software artifacts](https://docs.docker.com/docker-hub/repos/manage/hub-images/oci-artifacts/): Docker Hub supports OCI (Open
  Container Initiative) artifacts, allowing you to store, manage, and distribute
  a range of content beyond standard Docker images, including Helm charts,
  vulnerability reports, and more. This section provides an overview of OCI
  artifacts as well as some examples of pushing them to Docker Hub.
- [Push images to Hub](https://docs.docker.com/docker-hub/repos/manage/hub-images/push/): Docker Hub enables you to push local images
  to it, making them available for your team or the Docker community. Learn how
  to configure your images and use the `docker push` command to upload them to
  Docker Hub.
- [Move images between repositories](https://docs.docker.com/docker-hub/repos/manage/hub-images/move/): Organizing content across
  different repositories can help streamline collaboration and resource
  management. This topic details how to move images from one Docker Hub
  repository to another, whether for personal consolidation or to share images
  with an organization.

---

# Repository information

> Learn how to describe and optimize your Docker Hub repositories for better discoverability.

# Repository information

   Table of contents

---

Each repository can include a description, an overview, and categories to help
users understand its purpose and usage. Adding clear repository information
ensures that others can find your images and use them effectively.

You can only modify the repository information of repositories that aren't
archived. If a repository is archived, you must unarchive it to modify the
information. For more details, see [Unarchive a repository](https://docs.docker.com/docker-hub/repos/archive/#unarchive-a-repository).

## Repository description

The description appears in search results when using the `docker search` command
and in the search results on Docker Hub.

Consider the following repository description best practices.

- Summarize the purpose. Clearly state what the image does in a concise and
  specific manner. Make it clear if it's for a particular application, tool, or
  platform, or has a distinct use case.
- Highlight key features or benefits. Briefly mention the primary benefits or
  unique features that differentiate the image. Examples include high
  performance, ease of use, lightweight build, or compatibility with specific
  frameworks or operating systems.
- Include relevant keywords. Use keywords that users may search for to increase
  visibility, such as technology stacks, use cases, or environments.
- Keep it concise. The description can be a maximum of 100 characters. Aim to
  stay within one or two sentences for the description to ensure it's easy to
  read in search results. Users should quickly understand the image's value.
- Focus on the audience. Consider your target audience (developers, system
  administrators, etc.) and write the description to address their needs
  directly.

Following these practices can help make the description more engaging and
effective in search results, driving more relevant traffic to your repository.

### Add or update a repository description

1. Sign in to [Docker Hub](https://hub.docker.com).
2. Select **My Hub** > **Repositories**.
  A list of your repositories appears.
3. Select a repository.
  The **General** page for the repository appears.
4. Select the pencil icon under the description field.
5. Specify a description.
  The description can be up to 100 characters long.
6. Select **Update**.

## Repository overview

An overview describes what your image does and how to run it. It displays in the
public view of your repository when the repository has at least one image. If
automated builds are enabled, the overview will be synced from the source code
repository's `README.md` file on each successful build.

Consider the following repository overview best practices.

- Describe what the image is, the features it offers, and why it should be used.
  Can include examples of usage or the team behind the project.
- Explain how to get started with running a container using the image. You can
  include a minimal example of how to use the image in a Dockerfile.
- List the key image variants and tags to use them, as well as use cases for the
  variants.
- Link to documentation or support sites, communities, or mailing lists for
  additional resources.
- Provide contact information for the image maintainers.
- Include the license for the image and where to find more details if needed.

### Add or update a repository overview

1. Sign in to [Docker Hub](https://hub.docker.com).
2. Select **My Hub** > **Repositories**.
  A list of your repositories appears.
3. Select a repository.
  The **General** page for the repository appears.
4. Under **Repository overview**, select **Edit** or **Add overview**.
  The **Write** and **Preview** tabs appear.
5. Under **Write**, specify your repository overview.
  You can use basic Markdown and use the **Preview** tab to preview the formatting.
6. Select **Update**.

## Repository categories

You can tag Docker Hub repositories with categories, representing the primary
intended use cases for your images. This lets users more easily find and
explore content for the problem domain that they're interested in.

### Available categories

The Docker Hub content team maintains a curated list of categories.

The categories include:

- **API management**: Tools for creating, publishing, analyzing, and securing
  APIs.
- **Content management system:** Software applications to create and manage
  digital content through templates, procedures, and standard formats.
- **Data science:** Tools and software to support analyzing data and generating
  actionable insights.
- **Developer tools:** Software and utilities that assist developers in
  creating, debugging, maintaining, and supporting applications and systems.
- **Databases & storage:** Systems for storing, retrieving, and managing data.
- **Languages & frameworks:** Programming language runtimes and frameworks.
- **Integration & delivery:** Tools for Continuous Integration (CI) and
  Continuous Delivery (CD).
- **Internet of things:** Tools supporting Internet of Things (IoT)
  applications.
- **Machine learning & AI:** Tools and frameworks optimized for artificial
  intelligence and machine learning projects, such as pre-installed libraries
  and frameworks for data analysis, model training, and deployment.
- **Message queues:** Message queuing systems optimized for reliable, scalable,
  and efficient message handling.
- **Monitoring & Observability:** Tools to track software and system performance
  through metrics, logs, and traces, as well as observability to explore the
  system’s state and diagnose issues.
- **Networking:** Repositories that support data exchange and connecting
  computers and other devices to share resources.
- **Operating systems:** Software that manages all other programs on a computer
  and serves as an intermediary between users and the computer hardware, while
  overseeing applications and system resources.
- **Security:** Tools to protect a computer system or network from theft,
  unauthorized access, or damage to their hardware, software, or electronic
  data, as well as from service disruption.
- **Web servers:** Software to serve web pages, HTML files, and other assets to
  users or other systems.
- **Web analytics:** Tools to collect, measure, analyze, and report on web data
  and website visitor engagement.

### Auto-generated categories

> Note
>
> Auto-generated categories only apply to Docker Verified Publishers and
> Docker-Sponsored Open Source program participants.

For repositories that pre-date the Categories feature in Docker Hub,
categories have been automatically generated and applied, using OpenAI, based
on the repository title and description.

As an owner of a repository that has been auto-categorized, you can manually
edit the categories if you think they're inaccurate. See [Manage categories for
a repository](#manage-categories-for-a-repository).

The auto-generated categorization was a one-time effort to help seed categories
onto repositories created before the feature existed. Categories are not
assigned to new repositories automatically.

### Manage categories for a repository

You can tag a repository with up to three categories.

To edit the categories of a repository:

1. Sign in to [Docker Hub](https://hub.docker.com).
2. Select **My Hub** > **Repositories**.
  A list of your repositories appears.
3. Select a repository.
  The **General** page for the repository appears.
4. Select the pencil icon under the description field.
5. Select the categories you want to apply.
6. Select **Update**.

If you're missing a category, use the
[Give feedback link](https://docker.qualtrics.com/jfe/form/SV_03CrMyAkCWVylKu)
to let us know what categories you'd like to see.

---

# Docker

> Learn about the Docker-Sponsored Open Source Program and how it works

# Docker-Sponsored Open Source Program

   Table of contents

---

[Docker-Sponsored Open Source images](https://hub.docker.com/search?badges=open_source) are published and maintained by open-source projects sponsored by Docker through the program.

Images that are part of this program have a special badge on Docker Hub making it easier for users to identify projects that Docker has verified as trusted, secure, and active open-source projects.

![Docker-Sponsored Open Source badge](https://docs.docker.com/docker-hub/images/sponsored-badge-iso.png)  ![Docker-Sponsored Open Source badge](https://docs.docker.com/docker-hub/images/sponsored-badge-iso.png)

The Docker-Sponsored Open Source (DSOS) Program provides several features and benefits to non-commercial open source developers.

The program grants the following perks to eligible projects:

- Repository logo
- Verified Docker-Sponsored Open Source badge
- Insights and analytics
- Access to [Docker Scout](#docker-scout) for software supply chain management
- Removal of rate limiting for developers
- Improved discoverability on Docker Hub

These benefits are valid for one year and publishers can renew annually if the project still meets the program requirements. Program members and all users pulling public images from the project namespace get access to unlimited pulls and unlimited egress.

### Repository logo

DSOS organizations can upload custom images for individual repositories on Docker Hub.
This lets you override the default organization-level logo on a per-repository basis.

Only a user with an owner or editor role for the organization can change the repository logo.

#### Image requirements

- The supported filetypes for the logo image are JPEG and PNG.
- The minimum allowed image size in pixels is 120×120.
- The maximum allowed image size in pixels is 1000×1000.
- The maximum allowed image file size is 5MB.

#### Set the repository logo

1. Sign in to [Docker Hub](https://hub.docker.com).
2. Go to the page of the repository that you want to change the logo for.
3. Select the upload logo button, represented by a camera icon
  (
  ![camera icon](https://docs.docker.com/docker-hub/images/upload_logo_sm.png)
  )
  overlaying the current repository logo.
4. In the dialog that opens, select the PNG image that you want to upload to
  set it as the logo for the repository.

#### Remove the logo

Select the **Clear** button (
![clear button](https://docs.docker.com/docker-hub/images/clear_logo_sm.png)
) to remove a logo.

Removing the logo makes the repository default to using the organization logo, if set, or the following default logo if not.

![Default logo which is a 3D grey cube](https://docs.docker.com/docker-hub/images/default_logo_sm.png)  ![Default logo which is a 3D grey cube](https://docs.docker.com/docker-hub/images/default_logo_sm.png)

### Verified Docker-Sponsored Open Source badge

Docker verifies that developers can trust images with this badge on Docker Hub as an active open source project.

![Fluent org with a Docker-Sponsored Open Source badge](https://docs.docker.com/docker-hub/images/sponsored-badge.png)  ![Fluent org with a Docker-Sponsored Open Source badge](https://docs.docker.com/docker-hub/images/sponsored-badge.png)

### Insights and analytics

The
[insights and analytics](https://docs.docker.com/docker-hub/publish/insights-analytics) service provides usage metrics for how
the community uses Docker images, granting insight into user behavior.

The usage metrics show the number of image pulls by tag or by digest, and breakdowns by
geolocation, cloud provider, client, and more.

You can select the time span for which you want to view analytics data. You can also export the data in either a summary or raw format.

### Docker Scout

DSOS projects can enable Docker Scout on up to 100 repositories for free. Docker
Scout provides automatic image analysis, policy evaluation for improved supply
chain management, integrations with third-party systems like CI platforms and
source code management, and more.

You can enable Docker Scout on a per-repository basis. For information about
how to use this product, refer to the
[Docker Scout documentation](https://docs.docker.com/scout/).

### Who's eligible for the Docker-Sponsored Open Source program?

To qualify for the program, a publisher must share the project namespace in public repositories, meet [the Open Source Initiative definition](https://opensource.org/docs/osd), and be in active development with no pathway to commercialization.

Find out more by heading to the
[Docker-Sponsored Open Source Program](https://www.docker.com/community/open-source/application/) application page.

---

# Docker Verified Publisher Program

> Learn what the Docker Verified Publisher Program is and how it works

# Docker Verified Publisher Program

   Table of contents

---

[The Docker Verified Publisher
Program](https://hub.docker.com/search?badges=verified_publisher) provides
high-quality images from commercial publishers verified by Docker.

These images help development teams build secure software supply chains,
minimizing exposure to malicious content early in the process to save time and
money later.

## Who's eligible to become a verified publisher?

Any independent software vendor who distributes software on Docker Hub can join
the Verified Publisher Program. Find out more by heading to the [Docker Verified
Publisher Program](https://www.docker.com/partners/programs) page.

> Note
>
> DVP entitlements are applied per namespace (organization). If you operate
> multiple Docker Hub namespaces, each requires a separate DVP application and
> verification process.

## Program benefits

The Docker Verified Publisher Program (DVP) provides several features and
benefits to Docker Hub publishers. The program grants the following perks based
on participation tier:

- [Enterprise-grade infrastructure](#enterprise-grade-infrastructure): High
  availability hosting with 99.9% uptime
- [Verified publisher badge](#verified-publisher-badge): Special badge
  identifying high-quality commercial publishers
- [Repository logo](#repository-logo): Upload custom logos for individual
  repositories
- [Insights and analytics](#insights-and-analytics): Detailed usage metrics and
  community engagement data
- [Vulnerability analysis](#vulnerability-analysis): Automated security scanning
  with Docker Scout
- [Priority search ranking](#priority-search-ranking): Enhanced discoverability
  in Docker Hub search results
- [Removal of rate limiting](#removal-of-rate-limiting): Unrestricted pulls for
  development teams
- [Co-marketing opportunities](#co-marketing-opportunities): Joint promotional
  activities with Docker

### Enterprise-grade infrastructure

The Docker Verified Publisher Program runs on Docker Hub's enterprise-scale
infrastructure, serving millions of developers globally. Your published content
benefits from:

- High availability and uptime: Docker's systems are designed for failover
  across multiple availability zones, with load-balanced autoscaling, enabling
  99.9% uptime.
- Global delivery and fast downloads: Docker leverages Cloudflare's CDN and
  caching (with Cache Reserve) to achieve cache hit ratios more than 99%,
  reducing reliance on origin traffic and ensuring fast access for developers
  everywhere.
- Durability: Docker maintains a documented backup policy and performs full
  daily backups of production data.

You simply push your images to Docker Hub as usual, and Docker takes care of the
rest, serving your image to millions of developers worldwide.

![DVP flow in Docker Hub](https://docs.docker.com/docker-hub/repos/manage/trusted-content/images/dvp-hub-flow.svg)  ![DVP flow in Docker Hub](https://docs.docker.com/docker-hub/repos/manage/trusted-content/images/dvp-hub-flow.svg)

To learn more, see [Availability at
Docker](https://www.docker.com/trust/availability/).

### Verified publisher badge

Images that are part of this program have a special badge on Docker Hub making
it easier for users to identify projects that Docker has verified as
high-quality commercial publishers.

![Docker-Sponsored Open Source
badge](https://docs.docker.com/docker-hub/images/verified-publisher-badge.png)  ![Docker-Sponsored Open Source
badge](https://docs.docker.com/docker-hub/images/verified-publisher-badge.png)

### Repository logo

DVP organizations can upload custom images for individual repositories on Docker
Hub. This lets you override the default organization-level logo on a
per-repository basis.

To manage the repository logo, see [Manage repository logo](#manage-repository-logo).

### Vulnerability analysis

[Docker Scout](https://docs.docker.com/scout/) provides automatic vulnerability analysis
for DVP images published to Docker Hub.
Scanning images ensures that the published content is secure, and proves to
developers that they can trust the image.

You can enable analysis on a per-repository basis. For more about using this
feature, see
[Basic vulnerability
scanning](https://docs.docker.com/docker-hub/repos/manage/vulnerability-scanning/).

### Priority search ranking

Verified publisher images receive enhanced visibility in Docker Hub search
results, making it easier for developers to discover your content. This improved
discoverability helps drive adoption of your images within the developer
community.

### Removal of rate limiting

Verified publisher images are exempt from standard [Docker Hub rate
limits](https://docs.docker.com/docker-hub/usage/), ensuring developers can pull your images
without restrictions. **This applies to all users, including unauthenticated users**,
who get unlimited pulls for DVP images. This eliminates potential barriers to adoption and
provides a seamless experience for users of your content.

DVP partners can verify this unlimited access by checking the absence of rate
limiting headers when pulling their images. When pulling DVP images, users won't
see `ratelimit-limit` or `ratelimit-remaining` headers, indicating unlimited
access. For more details on checking rate limits, see [View pull rate and
limit](https://docs.docker.com/docker-hub/usage/pulls/#view-pull-rate-and-limit).

### Co-marketing opportunities

Docker collaborates with verified publishers on joint marketing initiatives,
including blog posts, case studies, webinars, and conference presentations.
These opportunities help amplify your brand visibility within the Docker
ecosystem.

### Insights and analytics

The insights and analytics service provides usage metrics for how
the community uses Docker images, granting insight into user behavior.

There is both a [web interface](https://docs.docker.com/docker-hub/repos/manage/trusted-content/insights-analytics/) and an
[API](https://docs.docker.com/reference/api/dvp/latest/) for accessing the analytics data.

The usage metrics show the number of image pulls by tag or by digest,
geolocation, cloud provider, client, and more.

## Manage repository logo

After joining the Docker Verified Publisher Program, you can set a custom logo
for each repository in your organization. The following requirements apply:

- The supported filetypes for the logo image are JPEG and PNG.
- The minimum allowed image size in pixels is 120×120.
- The maximum allowed image size in pixels is 1000×1000.
- The maximum allowed image file size is 5MB.

Only a user with an owner or editor role for the organization can change the repository logo.

### Set the repository logo

1. Sign in to [Docker Hub](https://hub.docker.com).
2. Go to the page of the repository that you want to change the logo for.
3. Select the upload logo button, represented by a camera icon (
  ![camera icon](https://docs.docker.com/docker-hub/images/upload_logo_sm.png)
  ) overlaying the
  current repository logo.
4. In the dialog that opens, select the PNG image that you want to upload to
  set it as the logo for the repository.

### Remove the logo

Select the **Clear** button (
![clear button](https://docs.docker.com/docker-hub/images/clear_logo_sm.png)
) to remove a logo.

Removing the logo makes the repository default to using the organization logo,
if set, or the following default logo if not.

![Default logo which is a 3D grey cube](https://docs.docker.com/docker-hub/images/default_logo_sm.png)  ![Default logo which is a 3D grey cube](https://docs.docker.com/docker-hub/images/default_logo_sm.png)
