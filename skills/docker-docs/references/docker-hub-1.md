# Docker Hub catalogs and more

# Docker Hub catalogs

> Explore specialized Docker Hub collections like the generative AI catalogs.

# Docker Hub catalogs

   Table of contents

---

Docker Hub catalogs are your go-to collections of trusted, ready-to-use
container images and resources, tailored to meet specific development needs.
They make it easier to find high-quality, pre-verified content so you can
quickly build, deploy, and manage your applications with confidence. Catalogs in
Docker Hub:

- Simplify content discovery: Organized and curated content makes it easy to
  discover tools and resources tailored to your specific domain or technology.
- Reduce complexity: Trusted resources, vetted by Docker and its partners,
  ensure security, reliability, and adherence to best practices.
- Accelerate development: Quickly integrate advanced capabilities into your
  applications without the hassle of extensive research or setup.

The following sections provide an overview of the key catalogs available in Docker Hub.

## MCP Catalog

The [MCP Catalog](https://hub.docker.com/mcp/) is a centralized, trusted
registry for discovering, sharing, and running Model Context Protocol
(MCP)-compatible tools. Seamlessly integrated into Docker Hub, the catalog
includes:

- Over 100 verified MCP servers packaged as Docker images
- Tools from partners such as New Relic, Stripe, and Grafana
- Versioned releases with publisher verification
- Simplified pull-and-run support through Docker Desktop and Docker CLI

Each server runs in an isolated container to ensure consistent behavior and
minimize configuration headaches. For developers working with Claude Desktop or
other MCP clients, the catalog provides an easy way to extend functionality with
drop-in tools.

To learn more about MCP servers, see [MCP Catalog and Toolkit](https://docs.docker.com/ai/mcp-catalog-and-toolkit/).

## AI Models Catalog

The [AI Models Catalog](https://hub.docker.com/catalogs/models/) provides
curated, trusted models that work with [Docker Model
Runner](https://docs.docker.com/ai/model-runner/). This catalog is designed to make AI
development more accessible by offering pre-packaged, ready-to-use models that
you can pull, run, and interact with using familiar Docker tools.

With the AI Models Catalog and Docker Model Runner, you can:

- Pull and serve models from Docker Hub or any OCI-compliant registry
- Interact with models via OpenAI-compatible APIs
- Run and test models locally using Docker Desktop or CLI
- Package and publish models using the `docker model` CLI

Whether you're building generative AI applications, integrating LLMs into your
workflows, or experimenting with machine learning tools, the AI Models Catalog
simplifies the model management experience.

---

# Mirror the Docker Hub library

> Setting-up a local mirror for Docker Hub images

# Mirror the Docker Hub library

   Table of contents

---

## Use-case

If you have multiple instances of Docker running in your environment, such as
multiple physical or virtual machines all running Docker, each daemon goes out
to the internet and fetches an image it doesn't have locally, from the Docker
repository. You can run a local registry mirror and point all your daemons
there, to avoid this extra internet traffic.

> Note
>
> Docker Official Images are an intellectual property of Docker.

### Alternatives

Alternatively, if the set of images you are using is well delimited, you can
simply pull them manually and push them to a simple, local, private registry.

Furthermore, if your images are all built in-house, not using the Hub at all and
relying entirely on your local registry is the simplest scenario.

### Gotcha

It's currently not possible to mirror another private registry. Only the central
Hub can be mirrored.

> Note
>
> Mirrors of Docker Hub are still subject to Docker's
> [fair use policy](https://docs.docker.com/docker-hub/usage/#fair-use).

### Solution

The Registry can be configured as a pull through cache. In this mode a Registry
responds to all normal docker pull requests but stores all content locally.

### Using Registry Access Management (RAM) with a registry mirror

If Docker Hub access is restricted via your Registry Access Management (RAM) configuration, you will not be able to pull images originating from Docker Hub even if the images are available in your registry mirror.

You will encounter the following error:

```console
Error response from daemon: Access to docker.io has been restricted by your administrators.
```

If you are unable to allow access to Docker Hub, you can manually pull from your registry mirror and optionally, retag the image. For example:

```console
docker pull <your-registry-mirror>[:<port>]/library/busybox
docker tag <your-registry-mirror>[:<port>]/library/busybox:latest busybox:latest
```

## How does it work?

The first time you request an image from your local registry mirror, it pulls
the image from the public Docker registry and stores it locally before handing
it back to you. On subsequent requests, the local registry mirror is able to
serve the image from its own storage.

### What if the content changes on the Hub?

When a pull is attempted with a tag, the Registry checks the remote to
ensure if it has the latest version of the requested content. Otherwise, it
fetches and caches the latest content.

### What about my disk?

In environments with high churn rates, stale data can build up in the cache.
When running as a pull through cache the Registry periodically removes old
content to save disk space. Subsequent requests for removed content causes a
remote fetch and local re-caching.

To ensure best performance and guarantee correctness the Registry cache should
be configured to use the `filesystem` driver for storage.

## Run a Registry as a pull-through cache

The easiest way to run a registry as a pull through cache is to run the official
[Registry](https://hub.docker.com/_/registry) image.
At least, you need to specify `proxy.remoteurl` within `/etc/docker/registry/config.yml`
as described in the following subsection.

Multiple registry caches can be deployed over the same back-end. A single
registry cache ensures that concurrent requests do not pull duplicate data,
but this property does not hold true for a registry cache cluster.

### Configure the cache

To configure a Registry to run as a pull through cache, the addition of a
`proxy` section is required to the config file.

To access private images on the Docker Hub, a username and password can
be supplied.

```yaml
proxy:
  remoteurl: https://registry-1.docker.io
  username: [username]
  password: [password]
```

> Warning
>
> If you specify a username and password, it's very important to understand that
> private resources that this user has access to Docker Hub is made available on
> your mirror. You must secure your mirror by implementing authentication if
> you expect these resources to stay private!

> Warning
>
> For the scheduler to clean up old entries, `delete` must be enabled in the
> registry configuration.

### Configure the Docker daemon

Either pass the `--registry-mirror` option when starting `dockerd` manually,
or edit
[/etc/docker/daemon.json](https://docs.docker.com/reference/cli/dockerd/#daemon-configuration-file)
and add the `registry-mirrors` key and value, to make the change persistent.

```json
{
  "registry-mirrors": ["https://<my-docker-mirror-host>"]
}
```

Save the file and reload Docker for the change to take effect.

> Note
>
> Some log messages that appear to be errors are actually informational
> messages.
>
>
>
> Check the `level` field to determine whether the message is warning you about
> an error or is giving you information. For example, this log message is
> informational:
>
>
>
> ```text
> time="2017-06-02T15:47:37Z" level=info msg="error statting local store, serving from upstream: unknown blob" go.version=go1.7.4
> ```
>
>
>
> It's telling you that the file doesn't exist yet in the local cache and is
> being pulled from upstream.

---

# Docker Hub search

> Discover how to browse and search Docker Hub's extensive resources.

# Docker Hub search

   Table of contents

---

The [Docker Hub search interface](https://hub.docker.com/search) lets you
explore millions of resources. To help you find exactly what you need, it offers
a variety of filters that let you narrow your results or discover different
types of content.

## Filters

The search functionality includes filters to narrow down
results based on your requirements, such as products, categories, and trusted
content. This ensures that you can quickly find and access the resources best
suited to your project.

### Products

Docker Hub's content library features three products, each designed to meet
specific needs of developers and organizations. These products include images,
plugins, and extensions.

#### Images

Docker Hub hosts millions of container images, making it the go-to repository
for containerized applications and solutions. These images include:

- Operating system images: Foundational images for Linux distributions like
  Ubuntu, Debian, and Alpine, or Windows Server images.
- Database and storage images: Pre-configured databases such as MySQL,
  PostgreSQL, and MongoDB to simplify application development.
- Languages and frameworks-based images: Popular images for Java, Python,
  Node.js, Ruby, .NET, and more, offering pre-built environments for faster
  development.

Images in Docker Hub simplify the development process by providing pre-built,
reusable building blocks, reducing the need to start from scratch. Whether
you're a beginner building your first container or an enterprise managing
complex architectures, Docker Hub images provide a reliable foundation.

#### Plugins

Plugins in Docker Hub let you extend and customize Docker Engine to suit
specialized requirements. Plugins integrate directly with the Docker Engine and
provide capabilities such as:

- Network plugins: Enhance networking functionality, enabling integration with
  complex network infrastructures.
- Volume plugins: Provide advanced storage options, supporting persistent and
  distributed storage across various backends.
- Authorization plugins: Offer fine-grained access control to secure Docker
  environments.

By leveraging Docker plugins, teams can tailor Docker Engine to meet their
specific operational needs, ensuring compatibility with existing infrastructures
and workflows.

To learn more about plugins, see
[Docker Engine managed plugin
system](https://docs.docker.com/engine/extend/).

#### Extensions

Docker Hub offers extensions for Docker Desktop, which enhance its core
functionality. These extensions are purpose-built to streamline the software
development lifecycle. Extensions provide tools for:

- System optimization and monitoring: Manage resources and optimize Docker
  Desktop’s performance.
- Container management: Simplify container deployment and monitoring.
- Database management: Facilitate efficient database operations within
  containers.
- Kubernetes and cloud integration: Bridge local environments with cloud-native
  and Kubernetes workflows.
- Visualization tools: Gain insights into container resource usage through
  graphical representations.

Extensions help developers and teams create a more efficient and unified
workflow by reducing context switching and bringing essential tools into Docker
Desktop's interface.

To learn more about extensions, see
[Docker
Extensions](https://docs.docker.com/extensions/).

### Trusted content

Docker Hub's trusted content provides a curated selection of high-quality,
secure images designed to give developers confidence in the reliability and
security of the resources they use. These images are stable, regularly updated,
and adhere to industry best practices, making them a strong foundation for
building and deploying applications. Docker Hub's trusted content includes,
Docker Official Images, Verified Publisher images, and Docker-Sponsored Open
Source Software images.

For more details, see [Trusted content](https://docs.docker.com/docker-hub/image-library/trusted-content/).

### Categories

Docker Hub makes it easy to find and explore container images with categories.
Categories group images based on their primary use case, helping you quickly
locate the tools and resources you need to build, deploy, and run your
applications.

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

### Operating systems

The **Operating systems** filter lets you narrow your search to container
images compatible with specific host operating systems. This filter ensures that
the images you use align with your target environment, whether you're developing
for Linux-based systems, Windows, or both.

- **Linux**: Access a wide range of images tailored for Linux environments.
  These images provide foundational environments for building and running
  Linux-based applications in containers.
- **Windows**: Explore Windows container images.

> Note
>
> The **Operating systems** filter is only available for images. If you select
> the **Extensions** or **Plugins** filter, then the **Operating systems**
> filter isn't available.

### Architectures

The **Architectures** filter lets you find images built to support specific CPU
architectures. This ensures compatibility with your hardware environment, from
development machines to production servers.

- **ARM**: Select images compatible with ARM processors, commonly used in IoT
  devices and embedded systems.
- **ARM 64**: Locate 64-bit ARM-compatible images for modern ARM processors,
  such as those in AWS Graviton or Apple Silicon.
- **IBM POWER**: Find images optimized for IBM Power Systems, offering
  performance and reliability for enterprise workloads.
- **PowerPC 64 LE**: Access images designed for the little-endian PowerPC 64-bit
  architecture.
- **IBM Z**: Discover images tailored for IBM Z mainframes, ensuring
  compatibility with enterprise-grade hardware.
- **x86**: Choose images compatible with 32-bit x86 architectures, suitable for
  older systems or lightweight environments.
- **x86-64**: Filter images for modern 64-bit x86 systems, widely used in
  desktops, servers, and cloud infrastructures.

> Note
>
> The **Architectures** filter is only available for images. If you select the
> **Extensions** or **Plugins** filter, then the **Architectures** filter isn't
> available.

### Reviewed by Docker

The **Reviewed by Docker** filter provides an extra layer of assurance when
selecting extensions. This filter helps you identify whether a Docker Desktop
extension has been reviewed by Docker for quality and reliability.

- **Reviewed**: Extensions that have undergone Docker's review process, ensuring
  they meet high standards.
- **Not Reviewed**: Extensions that have not been reviewed by Docker.

> Note
>
> The **Reviewed by Docker** filter is only available for extensions. To make
> the filter available, you must select only the **Extensions** filter in **Products**.

---

# Trusted content

> Learn about Docker Hub's trusted content.

# Trusted content

   Table of contents

---

Docker Hub's trusted content provides a curated selection of high-quality,
secure images designed to give developers confidence in the reliability and
security of the resources they use. These images are stable, regularly updated,
and adhere to industry best practices, making them a strong foundation for
building and deploying applications. Docker Hub's trusted content includes,
Docker Official Images, Verified Publisher images, and Docker-Sponsored Open
Source Software images.

## Docker Official Images

The Docker Official Images are a curated set of Docker repositories hosted on
Docker Hub.

Docker recommends you use the Docker Official Images in your projects. These
images have clear documentation, promote best practices, and are regularly
updated. Docker Official Images support most common use cases, making them
perfect for new Docker users. Advanced users can benefit from more specialized
image variants as well as review Docker Official Images as part of your
`Dockerfile` learning process.

> Note
>
> Use of Docker Official Images is subject to [Docker's Terms of Service](https://www.docker.com/legal/docker-terms-service/).

These images provide essential base repositories that serve as the starting
point for the majority of users.

These include operating systems such as
[Ubuntu](https://hub.docker.com/_/ubuntu/) and
[Alpine](https://hub.docker.com/_/alpine/), programming language runtimes such as
[Python](https://hub.docker.com/_/python) and
[Node](https://hub.docker.com/_/node), and other essential tools such as
[memcached](https://hub.docker.com/_/memcached) and
[MySQL](https://hub.docker.com/_/mysql).

The images are some of the [most secure images](https://www.docker.com/blog/enhancing-security-and-transparency-with-docker-official-images/)
on Docker Hub. This is particularly important as Docker Official Images are
some of the most popular on Docker Hub. Typically, Docker Official images have
few or no packages containing CVEs.

The images exemplify
[Dockerfile best practices](https://docs.docker.com/build/building/best-practices/)
and provide clear documentation to serve as a reference for other Dockerfile authors.

Images that are part of this program have a special badge on Docker Hub making
it easier for you to identify projects that are part of Docker Official Images.

![Docker official image badge](https://docs.docker.com/docker-hub/images/official-image-badge-iso.png)  ![Docker official image badge](https://docs.docker.com/docker-hub/images/official-image-badge-iso.png)

### Supported tags and respective Dockerfile links

The repository description for each Docker Official Image contains a
**Supported tags and respective Dockerfile links** section that lists all the
current tags with links to the Dockerfiles that created the image with those
tags. The purpose of this section is to show what image variants are available.

![Example: supported tags for Ubuntu](https://docs.docker.com/docker-hub/images/supported_tags.webp)  ![Example: supported tags for Ubuntu](https://docs.docker.com/docker-hub/images/supported_tags.webp)

Tags listed on the same line all refer to the same underlying image. Multiple
tags can point to the same image. For example, in the previous screenshot taken
from the `ubuntu` Docker Official Images repository, the tags `24.04`,
`noble-20240225`, `noble`, and `devel` all refer to the same image.

The `latest` tag for a Docker Official Image is often optimized for ease of use
and includes a wide variety of useful software, such as developer and build tools.
By tagging an image as `latest`, the image maintainers are essentially suggesting
that image be used as the default. In other words, if you do not know what tag to
use or are unfamiliar with the underlying software, you should probably start with
the `latest` image. As your understanding of the software and image variants advances,
you may find other image variants better suit your needs.

### Slim images

A number of language stacks such as
[Node.js](https://hub.docker.com/_/node/),
[Python](https://hub.docker.com/_/python/), and
[Ruby](https://hub.docker.com/_/ruby/) have `slim` tag variants
designed to provide a lightweight, production-ready base image
with fewer packages.

A typical consumption pattern for `slim`
images is as the base image for the final stage of a
[multi-staged build](https://docs.docker.com/build/building/multi-stage/).
For example, you build your application in the first stage of the build
using the `latest` variant and then copy your application into the final
stage based upon the `slim` variant. Here is an example `Dockerfile`.

```dockerfile
FROM node:latest AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . ./
FROM node:slim
WORKDIR /app
COPY --from=build /app /app
CMD ["node", "app.js"]
```

### Alpine images

Many Docker Official Images repositories also offer `alpine` variants. These
images are built on top of the [Alpine Linux](https://www.alpinelinux.org/)
distribution rather than Debian or Ubuntu. Alpine Linux is focused on providing
a small, simple, and secure base for container images, and Docker Official
Images `alpine` variants typically aim to install only necessary packages. As a
result, Docker Official Images `alpine` variants are typically even smaller
than `slim` variants.

The main caveat to note is that Alpine Linux uses [musl libc](https://musl.libc.org/)
instead of [glibc](https://www.gnu.org/software/libc/). Additionally, to
minimize image size, it's uncommon for Alpine-based images to include tools
such as Git or Bash by default. Depending on the depth of libc requirements or
assumptions in your programs, you may find yourself running into issues due to
missing libraries or tools.

When you use Alpine images as a base, consider the following options in order
to make your program compatible with Alpine Linux and musl:

- Compile your program against musl libc
- Statically link glibc libraries into your program
- Avoid C dependencies altogether (for example, build Go programs without CGO)
- Add the software you need yourself in your Dockerfile.

Refer to the `alpine` image [description](https://hub.docker.com/_/alpine) on
Docker Hub for examples on how to install packages if you are unfamiliar.

### Codenames

Tags with words that look like Toy Story characters (for example, `bookworm`,
`bullseye`, and `trixie`) or adjectives (such as `jammy`, and
`noble`), indicate the codename of the Linux distribution they use as a base
image. Debian release codenames are [based on Toy Story characters](https://en.wikipedia.org/wiki/Debian_version_history#Naming_convention),
and Ubuntu's take the form of "Adjective Animal". For example, the
codename for Ubuntu 24.04 is "Noble Numbat".

Linux distribution indicators are helpful because many Docker Official Images
provide variants built upon multiple underlying distribution versions (for
example, `postgres:bookworm` and `postgres:bullseye`).

### Other tags

Docker Official Images tags may contain other hints to the purpose of
their image variant in addition to those described here. Often these
tag variants are explained in the Docker Official Images repository
documentation. Reading through the "How to use this image" and
"Image Variants" sections will help you to understand how to use these
variants.

### Troubleshooting failed pulls

If you're experiencing failed pulls of Docker Official Images, check whether
the `DOCKER_CONTENT_TRUST` environment variable is set to `1`. Starting in
August 2025, Docker Content Trust signing certificates for Docker Official
Images began expiring. To resolve pull failures, unset the `DOCKER_CONTENT_TRUST`
environment variable. For more details, see the
[DCT retirement blog post](https://www.docker.com/blog/retiring-docker-content-trust/).

## Verified Publisher images

The Docker Verified Publisher program provides high-quality images from
commercial publishers verified by Docker.

These images help development teams build secure software supply chains,
minimizing exposure to malicious content early in the process to save time and
money later.

Images that are part of this program have a special badge on Docker Hub making
it easier for users to identify projects that Docker has verified as
high-quality commercial publishers.

![Docker-Verified Publisher badge](https://docs.docker.com/docker-hub/images/verified-publisher-badge-iso.png)  ![Docker-Verified Publisher badge](https://docs.docker.com/docker-hub/images/verified-publisher-badge-iso.png)

## Docker-Sponsored Open Source Software images

The Docker-Sponsored Open Source Software (OSS) program provides images that are
published and maintained by open-source projects sponsored by Docker.

Images that are part of this program have a special badge on Docker Hub making
it easier for users to identify projects that Docker has verified as trusted,
secure, and active open-source projects.

![Docker-Sponsored Open Source badge](https://docs.docker.com/docker-hub/images/sponsored-badge-iso.png)  ![Docker-Sponsored Open Source badge](https://docs.docker.com/docker-hub/images/sponsored-badge-iso.png)

---

# Content library

> Learn about Docker Hub's library of images, extensions, and plugins.

# Content library

---

Docker Hub's content library is the world's largest collection of
container images, extensions, and plugins. It provides a central location to
discover pre-built images and tools designed to streamline your container
workflows, making it easier to share and collaborate.

In this section, learn about:

- [Search](https://docs.docker.com/docker-hub/image-library/search/): Discover how to browse and search Docker Hub's extensive resources.
- [Trusted content](https://docs.docker.com/docker-hub/image-library/trusted-content/): Dive into Docker Official Images,
  Verified Publisher content, and Sponsored Open Source images, all vetted for
  security and reliability to streamline your workflows.
- [Catalogs](https://docs.docker.com/docker-hub/image-library/catalogs/): Explore specialized collections like the generative AI catalog.
- [Mirroring](https://docs.docker.com/docker-hub/image-library/mirror/): Learn how to create a mirror of Docker Hub's
  container image library as a pull-through cache.

---

# Docker Hub quickstart

> Learn how to get started using Docker Hub

# Docker Hub quickstart

   Table of contents

---

Docker Hub provides a vast library of pre-built images and resources,
accelerating development workflows and reducing setup time. You can build upon
pre-built images from Docker Hub and then use repositories to share and
distribute your own images with your team or millions of other developers.

This guide shows you how to find and run a pre-built image. It then walks you
through creating a custom image and sharing it through Docker Hub.

## Prerequisites

- [Download and install Docker](https://docs.docker.com/get-started/get-docker/)
- A verified [Docker](https://app.docker.com/signup) account

## Step 1: Find an image in Docker Hub's library

You can search for content in Docker Hub itself, in the Docker Desktop
Dashboard, or by using the CLI.

To search or browse for content on Docker Hub:

1. Navigate to the [Docker Hub Explore page](https://hub.docker.com/explore).
  On the **Explore** page, you can browse by catalog or category, or use the search
  to quickly find content.
2. Under **Categories**, select **Web servers**.
  After the results are displayed, you can further filter the results using the
  filters on the left side of the page.
3. In the filters, select **Docker Official Image**.
  Filtering by Trusted Content ensures that you see only high-quality, secure
  images curated by Docker and verified publishing partners.
4. In the results, select the **nginx** image.
  Selecting the image opens the image's page where you can learn more about how
  to use the image. On the page, you'll also find the `docker pull` command to
  pull the image.

1. Open the Docker Desktop Dashboard.
2. Select the **Docker Hub** view.
  In the **Docker Hub** view, you can browse by catalog or category, or use the search
  to quickly find content.
3. Leave the search box empty and then select **Search**.
  The search results are shown with additional filters now next to the search box.
4. Select the search filter icon, and then select **Docker Official Image** and **Web Servers**.
5. In the results, select the **nginx** image.

1. Open a terminal window.
  > Tip
  >
  > The Docker Desktop Dashboard contains a built-in terminal. At the bottom of
  > the Dashboard, select **>_ Terminal** to open it.
2. In the terminal, run the following command.
  ```console
  $ docker search --filter is-official=true nginx
  ```
  Unlike the Docker Hub and Docker Desktop interfaces, you can't browse by
  category using the `docker search` command. For more details about the
  command, see
  [docker search](https://docs.docker.com/reference/cli/docker/search/).

Now that you've found an image, it's time to pull and run it on your device.

## Step 2: Pull and run an image from Docker Hub

You can run images from Docker Hub using the CLI or Docker Desktop Dashboard.

1. In the Docker Desktop Dashboard, select the **nginx** image in the **Docker
  Hub** view. For more details, see [Step 1: Find an image in Docker Hub's
  library](#step-1-find-an-image-in-docker-hubs-library).
2. On the **nginx** screen, select **Run**.
  If the image doesn't exist on your device, it is automatically pulled from
  Docker Hub. Pulling the image may take a few seconds or minutes depending on
  your connection. After the image has been pulled, a window appears in Docker
  Desktop and you can specify run options.
3. In the **Host port** option, specify `8080`.
4. Select **Run**.
  The container logs appear after the container starts.
5. Select the **8080:80** link to open the server, or visit
  [http://localhost:8080](http://localhost:8080) in your web browser.
6. In the Docker Desktop Dashboard, select the **Stop** button to stop the
  container.

1. Open a terminal window.
  > Tip
  >
  > The Docker Desktop Dashboard contains a built-in terminal. At the bottom of
  > the Dashboard, select **>_ Terminal** to open it.
2. In your terminal, run the following command to pull and run the Nginx image.
  ```console
  $ docker run -p 8080:80 --rm nginx
  ```
  The `docker run` command automatically pulls and runs the image without the
  need to run `docker pull` first. To learn more about the command and its
  options, see the [docker runCLI
  reference](https://docs.docker.com/reference/cli/docker/container/run/). After running the
  command, you should see output similar to the following.
  ```console
  Unable to find image 'nginx:latest' locally
  latest: Pulling from library/nginx
  a480a496ba95: Pull complete
  f3ace1b8ce45: Pull complete
  11d6fdd0e8a7: Pull complete
  f1091da6fd5c: Pull complete
  40eea07b53d8: Pull complete
  6476794e50f4: Pull complete
  70850b3ec6b2: Pull complete
  Digest: sha256:28402db69fec7c17e179ea87882667f1e054391138f77ffaf0c3eb388efc3ffb
  Status: Downloaded newer image for nginx:latest
  /docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
  /docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
  /docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
  10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
  10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
  /docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
  /docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
  /docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
  /docker-entrypoint.sh: Configuration complete; ready for start up
  2024/11/07 21:43:41 [notice] 1#1: using the "epoll" event method
  2024/11/07 21:43:41 [notice] 1#1: nginx/1.27.2
  2024/11/07 21:43:41 [notice] 1#1: built by gcc 12.2.0 (Debian 12.2.0-14)
  2024/11/07 21:43:41 [notice] 1#1: OS: Linux 6.10.11-linuxkit
  2024/11/07 21:43:41 [notice] 1#1: getrlimit(RLIMIT_NOFILE): 1048576:1048576
  2024/11/07 21:43:41 [notice] 1#1: start worker processes
  2024/11/07 21:43:41 [notice] 1#1: start worker process 29
  ...
  ```
3. Visit [http://localhost:8080](http://localhost:8080) to view the default
  Nginx page and verify that the container is running.
4. In the terminal, press Ctrl+C to stop the container.

You've now run a web server without any set up or configuration. Docker Hub
provides instant access to pre-built, ready-to-use container images, letting you
quickly pull and run applications without needing to install or configure
software manually. With Docker Hub's vast library of images, you can experiment
with and deploy applications effortlessly, boosting productivity and making it
easy to try out new tools, set up development environments, or build on top of
existing software.

You can also extend images from Docker Hub, letting you quickly build and
customize your own images to suit specific needs.

## Step 3: Build and push an image to Docker Hub

1. Create a
  [Dockerfile](https://docs.docker.com/reference/dockerfile/) to specify your application:
  ```dockerfile
  FROM nginx
  RUN echo "<h1>Hello world from Docker!</h1>" > /usr/share/nginx/html/index.html
  ```
  This Dockerfile extends the Nginx image from Docker Hub to create a
  simple website. With just a few lines, you can easily set up, customize, and
  share a static website using Docker.
2. Run the following command to build your image. Replace `<YOUR-USERNAME>` with your Docker ID.
  ```console
  $ docker build -t <YOUR-USERNAME>/nginx-custom .
  ```
  This command builds your image and tags it so that Docker understands which
  repository to push it to in Docker Hub. To learn more about the command and
  its options, see the [docker buildCLI
  reference](https://docs.docker.com/reference/cli/docker/buildx/build/). After running the
  command, you should see output similar to the following.
  ```console
  [+] Building 0.6s (6/6) FINISHED                      docker:desktop-linux
   => [internal] load build definition from Dockerfile                  0.0s
   => => transferring dockerfile: 128B                                  0.0s
   => [internal] load metadata for docker.io/library/nginx:latest       0.0s
   => [internal] load .dockerignore                                     0.0s
   => => transferring context: 2B                                       0.0s
   => [1/2] FROM docker.io/library/nginx:latest                         0.1s
   => [2/2] RUN echo "<h1>Hello world from Docker!</h1>" > /usr/share/  0.2s
   => exporting to image                                                0.1s
   => => exporting layers                                               0.0s
   => => writing image sha256:f85ab68f4987847713e87a95c39009a5c9f4ad78  0.0s
   => => naming to docker.io/mobyismyname/nginx-custom                  0.0s
  ```
3. Run the following command to test your image. Replace `<YOUR-USERNAME>` with
  your Docker ID.
  ```console
  $ docker run -p 8080:80 --rm <YOUR-USERNAME>/nginx-custom
  ```
4. Visit [http://localhost:8080](http://localhost:8080) to view the page. You
  should see `Hello world from Docker!`.
5. In the terminal, press CTRL+C to stop the container.
6. Sign in to Docker Desktop. You must be signed in before pushing an image to
  Docker Hub.
7. Run the following command to push your image to Docker Hub. Replace `<YOUR-USERNAME>` with your Docker ID.
  ```console
  $ docker push <YOUR-USERNAME>/nginx-custom
  ```
  > Note
  >
  > You must be signed in to Docker Hub through Docker Desktop or the command line, and you must also name your images correctly, as per the above steps.
  The command pushes the image to Docker Hub and automatically
  creates the repository if it doesn't exist. To learn more about the command,
  see the [docker pushCLI
  reference](https://docs.docker.com/reference/cli/docker/image/push/). After running the
  command, you should see output similar to the following.
  ```console
  Using default tag: latest
  The push refers to repository [docker.io/mobyismyname/nginx-custom]
  d0e011850342: Pushed
  e4e9e9ad93c2: Mounted from library/nginx
  6ac729401225: Mounted from library/nginx
  8ce189049cb5: Mounted from library/nginx
  296af1bd2844: Mounted from library/nginx
  63d7ce983cd5: Mounted from library/nginx
  b33db0c3c3a8: Mounted from library/nginx
  98b5f35ea9d3: Mounted from library/nginx
  latest: digest: sha256:7f5223ae866e725a7f86b856c30edd3b86f60d76694df81d90b08918d8de1e3f size: 1985
  ```

Now that you've created a repository and pushed your image, it's time to view
your repository and explore its options.

## Step 4: View your repository on Docker Hub and explore options

You can view your Docker Hub repositories in the Docker Hub or Docker Desktop interface.

1. Go to [Docker Hub](https://hub.docker.com) and sign in.
  After signing in, you should be on the **Repositories** page. If not, then go
  to the [Repositories](https://hub.docker.com/repositories/) page.
2. Find the **nginx-custom** repository and select that row.
  After selecting the repository, you should see more details and options for
  your repository.

1. Sign in to Docker Desktop.
2. Select the **Images** view.
3. Select the **Hub repositories** tab.
  A list of your Docker Hub repositories appears.
4. Find the **nginx-custom** repository, hover over the row, and then select **View in Hub**.
  Docker Hub opens and you are able to view more details about the image.

You've now verified that your repository exists on Docker Hub, and you've
discovered more options for it. View the next steps to learn more about some of
these options.

## Next steps

Add [repository information](https://docs.docker.com/docker-hub/repos/manage/information/) to help users find and use
your image.
