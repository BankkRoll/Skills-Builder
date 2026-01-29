# About Docker Offload and more

# About Docker Offload

> Learn about Docker Offload, its features, and how it works.

# About Docker Offload

   Table of contents

---

Docker Offload is a fully managed service for building and running containers in
the cloud using the Docker tools you already know, including Docker Desktop, the
Docker CLI, and Docker Compose. It extends your local development workflow into a
scalable, cloud-powered environment, enabling developers to work efficiently even
in virtual desktop infrastructure (VDI) environments or systems that don't support
nested virtualization.

## Key features

Docker Offload includes the following capabilities to support modern container
workflows:

- Ephemeral cloud runners: Automatically provision and tear down cloud
  environments for each container session.
- Hybrid workflows: Seamlessly transition between local and remote execution
  using Docker Desktop or CLI.
- Secure communication: Use encrypted tunnels between Docker Desktop and cloud
  environments with support for secure secrets and image pulling.
- Port forwarding and bind mounts: Retain a local development experience even
  when running containers in the cloud.
- VDI-friendly: [Use Docker Desktop](https://docs.docker.com/desktop/setup/vm-vdi/) in virtual desktop environments or systems that
  don't support nested virtualization.

## Why use Docker Offload?

Docker Offload is designed to support modern development teams working across
local and cloud environments. It helps you:

- Offload heavy builds and runs to fast, scalable infrastructure
- Run containers that require more resources than your local setup can provide
- Use Docker Compose to manage complex, multi-service apps that need cloud
  resources
- Maintain consistent environments without managing custom infrastructure
- Develop efficiently in restricted or low-powered environments like VDIs

Docker Offload is ideal for high-velocity development workflows
that need the flexibility of the cloud without sacrificing the simplicity of
local tools.

## How Docker Offload works

Docker Offload replaces the need to build or run containers locally by connecting
Docker Desktop to secure, dedicated cloud resources.

### Running containers with Docker Offload

When you use Docker Offload to build or run containers, a Docker Desktop creates a secure
SSH tunnel to a Docker daemon running in the cloud. Your containers are started
and managed entirely in that remote environment.

Here's what happens:

1. Docker Desktop connects to the cloud and triggers container creation.
2. Docker Offload builds or pulls the required images and starts containers in the cloud.
3. The connection stays open while the containers run.
4. When the containers stop running, the environment shuts down and is cleaned
  up automatically.

This setup avoids the overhead of running containers locally and enables fast,
reliable containers even on low-powered machines, including machines that do not
support nested virtualization. This makes Docker Offload ideal for developers
using environments such as virtual desktops, cloud-hosted development machines,
or older hardware.

Despite running remotely, features like bind mounts and port forwarding continue
to work seamlessly, providing a local-like experience from within Docker Desktop
and the CLI.

Docker Offload automatically transitions between active and idle states based on
usage. You're only charged when actively building or running containers. When
idle for more than 5 minutes, the session ends and resources are cleaned up. For
details about how this works and how to configure idle timeout, see [Active and
idle states](https://docs.docker.com/offload/configuration/#understand-active-and-idle-states).

## What's next

Get hands-on with Docker Offload by following the
[Docker Offload quickstart](https://docs.docker.com/offload/quickstart/).

---

# Configure Docker Offload

> Learn how to configure build settings for Docker Offload.

# Configure Docker Offload

   Table of contents

---

Availability: Early Access
Requires: Docker Desktop 4.50 and later

You can configure Docker Offload settings at different levels depending on your role. Organization owners can manage
settings for all users in their organization, while individual developers can configure their own Docker Desktop
settings when allowed by their organization.

## Manage settings for your organization

For organization owners, you can manage Docker Offload settings for all users in your organization. For more details,
see [Manage Docker products](https://docs.docker.com/admin/organization/manage-products/). To view usage and configure billing for Docker
Offload, see
[Docker Offload usage and billing](https://docs.docker.com/offload/usage/).

## Configure settings in Docker Desktop

For developers, you can manage Docker Offload settings in Docker Desktop. To manage settings:

1. Open the Docker Desktop Dashboard and sign in.
2. Select the settings icon in the Docker Desktop Dashboard header.
3. In **Settings**, select **Docker Offload**.
  Here you can:
  - Toggle **Enable Docker Offload**. When enabled, you can start Offload sessions.
  - Select **Idle timeout**. This is the duration of time between no activity and Docker Offload entering idle mode.
    For details about idle timeout, see [Understand active and idle states](#understand-active-and-idle-states).

### Understand active and idle states

Docker Offload automatically transitions between active and idle states to help
you control costs while maintaining a seamless development experience.

#### When your session is active

Your Docker Offload environment is active when you're building images, running
containers, or actively interacting with them, such as viewing logs or
maintaining an open network connection. During active state:

- Usage is charged
- A remote Docker Engine is connected to your local machine
- All container operations execute in the cloud environment

#### When your session is idle

When there's no activity, Docker Offload transitions to idle state. During idle
state:

- You are not charged for usage
- The remote connection is suspended
- No containers are running in the cloud

The idle transition delay can be configured in Docker Desktop settings, ranging
from 10 seconds to 1 hour. This setting determines how long Docker Offload
waits after detecting inactivity before transitioning to idle state.

#### How your session is preserved

If your session has been idle for less than 5 minutes and you resume activity,
your previous containers and images are preserved and remain available. This
allows you to pick up right where you left off.

However, if the idle period exceeds 5 minutes, a new session starts with a
clean environment and any containers, images, or volumes from the previous
session are deleted.

> Note
>
> Transitioning from active to idle and back to active within 5 minutes will be
> charged as continuous usage.

---

# Give feedback

> Find a way to provide feedback that's right for you

# Give feedback

   Table of contents

---

There are several ways you can provide feedback on Docker Offload.

## Quick survey

The fastest way to share your thoughts is to fill out this short
[Docker Offload feedback
survey](https://docker.qualtrics.com/jfe/form/SV_br8Ki4CCdqeIYl0). It only takes
a minute and helps the Docker team improve your experience.

## In-product feedback

On each Docker Desktop Dashboard view, there is a **Give feedback** link. This
opens a feedback form where you can share ideas directly with the Docker Team.

## Report bugs or problems on GitHub

To report bugs or problems, visit the [Docker Desktop issue tracker](https://github.com/docker/desktop-feedback).

---

# Optimize Docker Offload usage

> Learn how to optimize your Docker Offload usage.

# Optimize Docker Offload usage

   Table of contents

---

Docker Offload builds and runs your containers remotely, not on the machine where you invoke the
commands. This means that files must be transferred from your local system to the
cloud over the network.

Transferring files over the network introduces higher latency and lower
bandwidth compared to local transfers.

Even with optimizations, large projects or slower network connections can lead to longer transfer times. Here are
several ways to optimize your setup for Docker Offload:

- [Use.dockerignorefiles](#dockerignore-files)
- [Choose slim base images](#slim-base-images)
- [Use multi-stage builds](#multi-stage-builds)
- [Fetch remote files during the build](#fetch-remote-files-in-build)
- [Leverage multi-threaded tools](#multi-threaded-tools)

For general Dockerfile tips, see
[Building best practices](https://docs.docker.com/build/building/best-practices/).

## dockerignore files

A
[.dockerignorefile](https://docs.docker.com/build/concepts/context/#dockerignore-files)
lets you specify which local files should *not* be included in the build
context. Files excluded by these patterns won’t be uploaded to Docker Offload
during a build.

Typical items to ignore:

- `.git` – avoids transferring your version history. (Note: you won’t be able to run `git` commands in the build.)
- Build artifacts or locally generated binaries.
- Dependency folders such as `node_modules`, if those are restored in the build
  process.

As a rule of thumb, your `.dockerignore` should be similar to your `.gitignore`.

## Slim base images

Smaller base images in your `FROM` instructions can reduce final image size and
improve build performance. The [alpine](https://hub.docker.com/_/alpine) image
is a good example of a minimal base.

For fully static binaries, you can use [scratch](https://hub.docker.com/_/scratch), which is an empty base image.

## Multi-stage builds

[Multi-stage builds](https://docs.docker.com/build/building/multi-stage/) let you separate build-time
and runtime environments in your Dockerfile. This not only reduces the size of
the final image but also allows for parallel stage execution during the build.

Use `COPY --from` to copy files from earlier stages or external images. This
approach helps minimize unnecessary layers and reduce final image size.

## Fetch remote files in build

When possible, download large files from the internet during the build itself
instead of bundling them in your local context. This avoids network transfer
from your client to Docker Offload.

You can do this using:

- The Dockerfile
  [ADDinstruction](https://docs.docker.com/reference/dockerfile/#add)
- `RUN` commands like `wget`, `curl`, or `rsync`

### Multi-threaded tools

Some build tools, such as `make`, are single-threaded by default. If the tool
supports it, configure it to run in parallel. For example, use `make --jobs=4`
to run four jobs simultaneously.

Taking advantage of available CPU resources in the cloud can significantly
improve build time.

---

# Docker Offload quickstart

> Learn how to use Docker Offload to build and run your container images faster, both locally and in CI.

# Docker Offload quickstart

   Table of contents

---

Availability: Early Access
Requires: Docker Desktop 4.50 and later

[Docker Offload](https://docs.docker.com/offload/about/) lets you build and run containers in the cloud while using your local Docker Desktop tools
and workflow. This means faster builds, access to powerful cloud resources, and a seamless development
experience.

This quickstart covers the steps developers need to get started with Docker Offload.

> Note
>
> If you're an organization owner, to get started you must [sign up](https://www.docker.com/products/docker-offload/)
> and subscribe your organization to use Docker Offload. After subscribing, see the following:
>
>
>
> - [Manage Docker products](https://docs.docker.com/admin/organization/manage-products/) to learn how to manage access for the developers
>   in your organization.
> - [Usage and billing](https://docs.docker.com/offload/usage/) to learn how set up billing and monitor usage.

## Prerequisites

- You must have
  [Docker Desktop](https://docs.docker.com/desktop/) installed. Docker Offload works with Docker Desktop version 4.50 or later.
- You must have access to Docker Offload. Your organization owner must [sign
  up](https://www.docker.com/products/docker-offload/) your organization.
- You must have committed usage available or on-demand usage enabled for your organization. This is set up by your
  organization owner. For more details, see
  [Docker Offload usage and billing](https://docs.docker.com/offload/usage/).

## Step 1: Verify access to Docker Offload

To access Docker Offload, you must be part of an organization that has subscribed to Docker Offload. As a developer, you
can verify this by checking if the Docker Offload toggle appears in the Docker Desktop Dashboard header.

1. Start Docker Desktop and sign in.
2. In the Docker Desktop Dashboard header, look for the Docker Offload toggle.

![Offload toggle](https://docs.docker.com/offload/images/offload-toggle.png)  ![Offload toggle](https://docs.docker.com/offload/images/offload-toggle.png)

If you see the Docker Offload toggle, you have access to Docker Offload and can proceed to the next step. If you don't
see the Docker Offload toggle, check if Docker Offload is disabled in your [Docker Desktop
settings](https://docs.docker.com/offload/configuration/), and then contact your administrator to verify that your organization has subscribed to
Docker Offload and that they have enabled access for your organization.

## Step 2: Start Docker Offload

You can start Docker Offload from the CLI or in the header of the Docker Desktop Dashboard. The following steps describe
how to start Docker Offload using the CLI.

1. Start Docker Desktop and sign in.
2. Open a terminal and run the following command to start Docker Offload:
  ```console
  $ docker offload start
  ```
  > Tip
  >
  > To learn more about the Docker Offload CLI commands, see the
  > [Docker Offload CLI
  > reference](https://docs.docker.com/reference/cli/docker/offload/).
3. If you are a member of multiple organizations that have access to Docker Offload, you have the option to select a
  profile. The selected organization is responsible for any usage.

When Docker Offload is started, you'll see a cloud icon
(
![Offload mode icon](https://docs.docker.com/offload/images/cloud-mode.png)
)
in the Docker Desktop Dashboard header, and the Docker Desktop Dashboard appears purple. You can run
`docker offload status` in a terminal to check the status of Docker Offload.

## Step 3: Run a container with Docker Offload

After starting Docker Offload, Docker Desktop connects to a secure cloud environment
that mirrors your local experience. When you run builds or containers, they
execute remotely, but behave just like local ones.

To verify that Docker Offload is working, run a container:

```console
$ docker run --rm hello-world
```

If Docker Offload is working, you'll see `Hello from Docker!` in the terminal output.

## Step 4: Monitor your Offload usage

When Docker Offload is started and you have started session (for example, you've ran a container), then you can see
current session duration estimate in the Docker Desktop Dashboard footer next to the hourglass icon
(
![Offload session duration](https://docs.docker.com/offload/images/hourglass-icon.png)
).

Also, when Docker Offload is started, you can view detailed session information by selecting **Offload** > **Insights**
in the left navigation of the Docker Desktop Dashboard.

## Step 5: Stop Docker Offload

Docker Offload automatically
[idles](https://docs.docker.com/offload/configuration/#understand-active-and-idle-states) after a period of
inactivity. You can stop it at any time. To stop Docker Offload:

```console
$ docker offload stop
```

When you stop Docker Offload, the cloud environment is terminated and all running containers and images are removed.
When Docker Offload has been idle for around 5 minutes, the environment is also terminated and all running containers
and images are removed.

To start Docker Offload again, run the `docker offload start` command.

## What's next

Configure your idle timeout in Docker Desktop. For more information, see [Configure Docker Offload](https://docs.docker.com/offload/configuration/).

---

# Troubleshoot Docker Offload

> Learn how to troubleshoot issues with Docker Offload.

# Troubleshoot Docker Offload

---

Docker Offload requires:

- Authentication
- An active internet connection
- No restrictive proxy or firewall blocking traffic to Docker Cloud
- Access to Docker Offload
- Docker Desktop 4.50 or later

Docker Desktop uses Offload to run both builds and containers in the cloud.
If builds or containers are failing to run, falling back to local, or reporting
session errors, use the following steps to help resolve the issue.

1. Ensure Docker Offload is enabled in Docker Desktop:
  1. Open Docker Desktop and sign in.
  2. Go to **Settings** > **Docker Offload**.
  3. Ensure that **Enable Docker Offload** is toggled on.
2. Use the following command to check if the connection is active:
  ```console
  $ docker offload status
  ```
3. To get more information, run the following command:
  ```console
  $ docker offload diagnose
  ```
4. If you're not connected, start a new session:
  ```console
  $ docker offload start
  ```
5. Verify authentication with `docker login`.
6. If needed, you can sign out and then sign in again:
  ```console
  $ docker logout
  $ docker login
  ```
7. Verify your usage and billing. For more information, see
  [Docker Offload usage](https://docs.docker.com/offload/usage/).

---

# Docker Offload usage and billing

> Learn about Docker Offload usage and how to monitor your cloud resources.

# Docker Offload usage and billing

   Table of contents

---

Availability: Early Access
Requires: Docker Desktop 4.50 and later

> Note
>
> All free trial usage granted for the Docker Offload Beta expire after 90 days from the time they are granted. To
> continue using Docker Offload Beta after your usage expires, you can enable on-demand usage at [Docker Home
> Billing](https://app.docker.com/billing).

## Understand usage and billing models

Docker Offload offers two usage models to fit different team needs and usage patterns:

- Committed usage: This provides a committed amount of cloud compute time for your organization.
- On-demand usage: This provides pay-as-you-go flexibility. You can enable or disable on-demand usage in
  [Billing](#manage-billing).

## Manage billing

For Docker Offload, you can view and configure billing on the **Docker Offload**
page in [Docker Home Billing](https://app.docker.com/billing). On this page, you
can:

- View your committed usage
- View rates for cloud resources
- Manage on-demand billing, including setting a monthly limit
- Track your organization's Docker Offload usage
- Add or change payment methods

You must be an organization owner to manage billing. For more general information about billing, see
[Billing](https://docs.docker.com/billing/).

## Monitor your usage

The **Offload overview** page in Docker Home provides visibility into
how you are using cloud resources to build and run containers.

To monitor your usage:

1. Sign in to [Docker Home](https://app.docker.com/).
2. Select the account for which you want to monitor usage.
3. Select **Offload** > **Offload overview**.

The following widgets are available:

- My recent sessions: This widget shows your total session time as well as a break down of your most recent sessions'
  duration.
- My top 10 images: This widget shows the top 10 images used in Docker Offload in run sessions. It provides insight into
  which images are most frequently used, helping you understand your container usage patterns.
- My active sessions: This widget displays any currently active Docker Offload sessions.

### View recent activity

The **Recent activity** page in Docker Home provides detailed information about your recent Docker Offload sessions.
This includes session ID, start date and time, duration, and number of containers.

To view the **Recent activity** page:

1. Sign in to [Docker Home](https://app.docker.com/).
2. Select the account for which you want to manage Docker Offload.
3. Select **Offload** > **Recent activity**.
