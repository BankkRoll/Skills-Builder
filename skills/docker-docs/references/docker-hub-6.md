# Webhooks and more

# Webhooks

> Docker Hub Webhooks

# Webhooks

   Table of contents

---

You can use webhooks to cause an action in another service in response to a push event in the repository. Webhooks are POST requests sent to a URL you define in Docker Hub.

## Create a webhook

To create a webhook:

1. In your chosen repository, select the **Webhooks** tab.
2. Provide a name for the webhook.
3. Provide a destination webhook URL. This is where webhook POST requests are delivered.
4. Select **Create**.

## View webhook delivery history

To view the history of the webhook:

1. Hover over your webhook under the **Current Webhooks section**.
2. Select the **Menu options** icon.
3. Select **View History**.

You can then view the delivery history, and whether delivering the POST request was successful or not.

## Example webhook payload

Webhook payloads have the following JSON format:

```json
{
  "callback_url": "https://registry.hub.docker.com/u/svendowideit/testhook/hook/2141b5bi5i5b02bec211i4eeih0242eg11000a/",
  "push_data": {
    "pushed_at": 1417566161,
    "pusher": "trustedbuilder",
    "tag": "latest"
  },
  "repository": {
    "comment_count": 0,
    "date_created": 1417494799,
    "description": "",
    "dockerfile": "#\n# BUILD\u0009\u0009docker build -t svendowideit/apt-cacher .\n# RUN\u0009\u0009docker run -d -p 3142:3142 -name apt-cacher-run apt-cacher\n#\n# and then you can run containers with:\n# \u0009\u0009docker run -t -i -rm -e http_proxy http://192.168.1.2:3142/ debian bash\n#\nFROM\u0009\u0009ubuntu\n\n\nVOLUME\u0009\u0009[/var/cache/apt-cacher-ng]\nRUN\u0009\u0009apt-get update ; apt-get install -yq apt-cacher-ng\n\nEXPOSE \u0009\u00093142\nCMD\u0009\u0009chmod 777 /var/cache/apt-cacher-ng ; /etc/init.d/apt-cacher-ng start ; tail -f /var/log/apt-cacher-ng/*\n",
    "full_description": "Docker Hub based automated build from a GitHub repo",
    "is_official": false,
    "is_private": true,
    "is_trusted": true,
    "name": "testhook",
    "namespace": "svendowideit",
    "owner": "svendowideit",
    "repo_name": "svendowideit/testhook",
    "repo_url": "https://registry.hub.docker.com/u/svendowideit/testhook/",
    "star_count": 0,
    "status": "Active"
  }
}
```

> Note
>
> The `callback_url` field is a legacy field and is no longer supported.

---

# Personal settings for repositories

> Learn about personal repository settings in Docker Hub

# Personal settings for repositories

   Table of contents

---

For your account, you can set personal settings for repositories, including
default repository privacy and autobuild notifications.

## Default repository privacy

When creating a new repository in Docker Hub, you are able to specify the
repository visibility. You can also change the visibility at any time in Docker Hub.

The default setting is useful if you use the `docker push` command to push to a
repository that doesn't exist yet. In this case, Docker Hub automatically
creates the repository with your default repository privacy.

### Configure default repository privacy

1. Sign in to [Docker Hub](https://hub.docker.com).
2. Select **My Hub** > **Settings** > **Default privacy**.
3. Select the **Default privacy** for any new repository created.
  - **Public**: All new repositories appear in Docker Hub search results and can be
    pulled by everyone.
  - **Private**: All new repositories don't appear in Docker Hub search results
    and are only accessible to you and collaborators. In addition, if the
    repository is created in an organization's namespace, then the repository
    is accessible to those with applicable roles or permissions.
4. Select **Save**.

## Autobuild notifications

You can send notifications to your email for all your repositories using
autobuilds.

### Configure autobuild notifications

1. Sign in to [Docker Hub](https://hub.docker.com).
2. Select **My Hub** > **Repositories** > **Settings** > **Notifications**.
3. Select the notifications to receive by email.
  - **Off**: No notifications.
  - **Only failures**: Only notifications about failed builds.
  - **Everything**: Notifications for successful and failed builds.
4. Select **Save**.

---

# Repositories

> Learn how to manage repositories on Docker Hub

# Repositories

---

A Docker Hub repository is a collection of container images, enabling you to
store, manage, and share Docker images publicly or privately. Each repository
serves as a dedicated space where you can store images associated with a
particular application, microservice, or project. Content in repositories is
organized by tags, which represent different versions of the same application,
allowing users to pull the right version when needed.

In this section, learn how to:

- [Create](https://docs.docker.com/docker-hub/repos/create/) a repository.
- Manage a repository, including how to manage:
  - [Repository information](https://docs.docker.com/docker-hub/repos/manage/information/): Add descriptions,
    overviews, and categories to help users understand the purpose and usage of
    your repository. Clear repository information aids discoverability and
    usability.
  - [Access](https://docs.docker.com/docker-hub/repos/manage/access/): Control who can access your repositories with
    flexible options. Make repositories public or private, add collaborators,
    and, for organizations, manage roles and teams to maintain security and
    control.
  - [Images](https://docs.docker.com/docker-hub/repos/manage/hub-images/): Repositories support diverse
    content types, including OCI artifacts, and allow version control through
    tagging. Push new images and manage existing content across repositories
    for flexibility.
  - [Image security insights](https://docs.docker.com/docker-hub/repos/manage/vulnerability-scanning/): Utilize
    continuous Docker Scout analysis and static vulnerability scanning to
    detect, understand, and address security issues within container images.
  - [Webhooks](https://docs.docker.com/docker-hub/repos/manage/webhooks/): Automate responses to repository events
    like image pushes or updates by setting up webhooks, which can trigger
    notifications or actions in external systems, streamlining workflows.
  - [Automated builds](https://docs.docker.com/docker-hub/repos/manage/builds/): Integrate with GitHub or
    Bitbucket for automated builds. Every code change triggers an image
    rebuild, supporting continuous integration and delivery.
  - [Trusted content](https://docs.docker.com/docker-hub/repos/manage/trusted-content/): Contribute to Docker
    Official Images or manage repositories in the Verified Publisher and
    Sponsored Open Source programs, including tasks like setting logos,
    accessing analytics, and enabling vulnerability scanning.
- [Archive](https://docs.docker.com/docker-hub/repos/archive/) an outdated or unsupported repository.
- [Delete](https://docs.docker.com/docker-hub/repos/delete/) a repository.
- [Manage personal settings](https://docs.docker.com/docker-hub/repos/settings/): For your account, you can set personal
  settings for repositories, including default repository privacy and autobuild
  notifications.

---

# Service accounts

> Docker Service accounts

# Service accounts

   Table of contents

---

> Important
>
> As of December 10, 2024, Enhanced Service Account add-ons are no longer
> available. Existing Service Account agreements will be honored until their
> current term expires, but new purchases or renewals of Enhanced Service
> Account add-ons are no longer available and customers must renew under a new
> subscription.
>
>
>
> Docker recommends transitioning to
> [Organization Access Tokens
> (OATs)](https://docs.docker.com/enterprise/security/access-tokens/), which can provide similar
> functionality.

A service account is a Docker ID used for automated management of container images or containerized applications. Service accounts are typically used in automated workflows, and don't share Docker IDs with the members in the organization. Common use cases for service accounts include mirroring content on Docker Hub, or tying in image pulls from your CI/CD process.

## Enhanced Service Account add-on tiers

Refer to the following table for details on the Enhanced Service Account add-ons:

| Tier | Pull Rates Per Day* |
| --- | --- |
| 1 | 5,000-10,000 |
| 2 | 10,000-25,000 |
| 3 | 25,000-50,000 |
| 4 | 50,000-100,000 |
| 5 | 100,000+ |

*The service account may exceed Pulls by up to 25% for up to 20 days during the year without incurring additional fees. Reports on consumption are available upon request.

---

# Troubleshoot Docker Hub

> Learn how to troubleshoot common Docker Hub issues.

# Troubleshoot Docker Hub

   Table of contents

---

If you experience issues with Docker Hub, refer to the following solutions.

## You have reached your pull rate limit (429 response code)

### Error message

When this issue occurs, you receive following error message in the Docker CLI or
in the Docker Engine logs:

```text
You have reached your pull rate limit. You may increase the limit by authenticating and upgrading: https://www.docker.com/increase-rate-limits
```

### Possible causes

- You have reached your pull rate limit as an authenticated Docker Personal
  user.
- You have reached your pull rate limit as an unauthenticated user based on your
  IPv4 address or IPv6 /64 subnet.

### Solution

You can use one of the following solutions:

- [Authenticate](https://docs.docker.com/docker-hub/usage/pulls/#authentication) or
  [upgrade](https://docs.docker.com/subscription/change/#upgrade-your-subscription) your Docker
  account.
- [View your pull rate limit](https://docs.docker.com/docker-hub/usage/pulls/#view-hourly-pull-rate-and-limit),
  wait until your pull rate limit decreases, and then try again.

## Too many requests (429 response code)

### Error message

When this issue occurs, you receive following error message in the Docker CLI or
in the Docker Engine logs:

```text
Too Many Requests
```

### Possible causes

- You have reached the [Abuse rate limit](https://docs.docker.com/docker-hub/usage/#abuse-rate-limit).

### Solution

1. Check for broken CI/CD pipelines accessing Docker Hub and fix them.
2. Implement a retry with back-off solution in your automated scripts to ensure
  that you're not resending thousands of requests per minute.

## 500 response code

### Error message

When this issue occurs, the following error message is common in the Docker CLI
or in the Docker Engine logs:

```text
Unexpected status code 500
```

### Possible causes

- There is a temporary Docker Hub service issue.

### Solution

1. View the [Docker System Status Page](https://www.dockerstatus.com/) and
  verify that all services are operational.
2. Try accessing Docker Hub again. It may be a temporary issue.
3. [Contact Docker Support](https://www.docker.com/support/) to report the issue.

---

# Best practices for optimizing Docker Hub usage

> Learn how to optimize and manage your Docker Hub usage.

# Best practices for optimizing Docker Hub usage

---

Use the following steps to help optimize and manage your Docker Hub usage for
both individuals and organizations:

1. [View your Docker Hub usage](https://hub.docker.com/usage).
2. Use the Docker Hub usage data to identify which accounts consume the most
  data, determine peak usage times, and identify which images are related to
  the most data usage. In addition, look for usage trends, such as the
  following:
  - Inefficient pull behavior: Identify frequently accessed repositories to
    assess whether you can optimize caching practices or consolidate usage to
    reduce pulls.
  - Inefficient automated systems: Check which automated tools, such as CI/CD
    pipelines, may be causing higher pull rates, and configure them to avoid
    unnecessary image pulls.
3. Optimize image pulls by:
  - Using caching: Implement local image caching via
    [mirroring](https://docs.docker.com/docker-hub/mirror/) or within your CI/CD pipelines to reduce
    redundant pulls.
  - Automating manual workflows: Avoid unnecessary pulls by configuring automated
    systems to pull only when a new version of an image is available.
4. Optimize your storage by:
  - Regularly auditing and [removing entire repositories](https://docs.docker.com/docker-hub/repos/delete/) with untagged, unused, or outdated images.
  - Using [Image Management](https://docs.docker.com/docker-hub/repos/manage/hub-images/manage/) to remove stale and outdated images within a repository.
5. For organizations, monitor and enforce organizational policies by doing the
  following:
  - Routinely [view Docker Hub usage](https://hub.docker.com/usage) to monitor usage.
  - [Enforce sign-in](https://docs.docker.com/security/for-admins/enforce-sign-in/) to ensure that you
    can monitor the usage of your users and users receive higher usage limits.
  - Look for duplicate user accounts in Docker and remove accounts from your organization
    as needed.

---

# Docker Hub pull usage and limits

> Learn about pull usage and limits for Docker Hub.

# Docker Hub pull usage and limits

   Table of contents

---

Unauthenticated and Docker Personal users are subject to a 6-hour pull rate limit
on Docker Hub. In contrast, Docker Pro, Team, and Business users benefit from
an unlimited pull rate.

The following pull usage and limits apply based on your subscription, subject to
fair use:

| User type | Pull rate limit per 6 hours |
| --- | --- |
| Business (authenticated) | Unlimited |
| Team (authenticated) | Unlimited |
| Pro (authenticated) | Unlimited |
| Personal (authenticated) | 200 |
| Unauthenticated Users | 100 per IPv4 address or IPv6 /64 subnet |

## Pull definition

A pull is defined as the following:

- A Docker pull includes both a version check and any download that
  occurs as a result of the pull. Depending on the client, a `docker pull` can
  verify the existence of an image or tag without downloading it by performing
  a version check.
- Version checks do not count towards usage pricing.
- A pull for a normal image makes one pull for a [single
  manifest](https://github.com/opencontainers/image-spec/blob/main/manifest.md).
- A pull for a multi-arch image will count as one pull for each
  different architecture.

## Pull attribution

Pulls from authenticated users can be attributed to either a personal or an
[organization namespace](https://docs.docker.com/accounts/general-faqs/#whats-an-organization-name-or-namespace).

Attribution is based on the following:

- Private pulls: Pulls for private repositories are attributed to the
  repository's namespace owner.
- Public pulls: When pulling images from a public repository, attribution is
  determined based on domain affiliation and organization membership.
- Verified domain ownership: When pulling an image from an account linked to a
  verified domain, the attribution is set to be the owner of that
  [domain](https://docs.docker.com/enterprise/security/single-sign-on/faqs/domain-faqs/).
- Single organization membership:
  - If the owner of the verified domain is a company and the user is part of
    only one organization within that
    [company](https://docs.docker.com/admin/faqs/company-faqs/#what-features-are-supported-at-the-company-level),
    the pull is attributed to that specific organization.
  - If the user is part of only one organization, the pull is attributed to
    that specific organization.
- Multiple organization memberships: If the user is part of multiple
  organizations under the company, the pull is attributed to the user's personal
  namespace.

### Authentication

To ensure correct attribution of your pulls, you must authenticate with Docker
Hub. The following sections provide information on how to sign in to Docker Hub
to authenticate your pulls.

#### Docker Desktop

If you are using Docker Desktop, you can sign in to Docker Hub from the Docker
Desktop menu.

Select **Sign in / Create Docker ID** from the Docker Desktop menu and follow
the on-screen instructions to complete the sign-in process.

#### Docker Engine

If you're using a standalone version of Docker Engine, run the `docker login`
command from a terminal to authenticate with Docker Hub. For information on how
to use the command, see
[docker login](https://docs.docker.com/reference/cli/docker/login/).

#### Docker Swarm

If you're running Docker Swarm, you must use the `--with-registry-auth` flag to
authenticate with Docker Hub. For more information, see
[Create a
service](https://docs.docker.com/reference/cli/docker/service/create/#with-registry-auth). If you
are using a Docker Compose file to deploy an application stack, see
[docker
stack deploy](https://docs.docker.com/reference/cli/docker/stack/deploy/).

#### GitHub Actions

If you're using GitHub Actions to build and push Docker images to Docker Hub,
see [login action](https://github.com/docker/login-action#dockerhub). If you are
using another Action, you must add your username and access token in a similar
way for authentication.

#### Kubernetes

If you're running Kubernetes, follow the instructions in [Pull an Image from a
Private
Registry](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/)
for information on authentication.

#### Third-party platforms

If you're using any third-party platforms, follow your provider’s instructions on using registry authentication.

> Note
>
> When pulling images via a third-party platform, the platform may use the same
> IPv4 address or IPv6 /64 subnet to pull images for multiple users. Even if you
> are authenticated, pulls attributed to a single IPv4 address or IPv6 /64 subnet
> may cause [abuse rate limiting](https://docs.docker.com/docker-hub/usage/#abuse-rate-limit).

- [Artifactory](https://www.jfrog.com/confluence/display/JFROG/Advanced+Settings#AdvancedSettings-RemoteCredentials)
- [AWS CodeBuild](https://aws.amazon.com/blogs/devops/how-to-use-docker-images-from-a-private-registry-in-aws-codebuild-for-your-build-environment/)
- [AWS ECS/Fargate](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/private-auth.html)
- [Azure Pipelines](https://docs.microsoft.com/en-us/azure/devops/pipelines/library/service-endpoints?view=azure-devops&tabs=yaml#sep-docreg)
- [Chipper CI](https://docs.chipperci.com/builds/docker/#rate-limit-auth)
- [CircleCI](https://circleci.com/docs/2.0/private-images/)
- [Codefresh](https://codefresh.io/docs/docs/docker-registries/external-docker-registries/docker-hub/)
- [Drone.io](https://docs.drone.io/pipeline/docker/syntax/images/#pulling-private-images)
- [GitLab](https://docs.gitlab.com/ee/user/packages/container_registry/#authenticate-with-the-container-registry)
- [LayerCI](https://layerci.com/docs/advanced-workflows#logging-in-to-docker)
- [TeamCity](https://www.jetbrains.com/help/teamcity/integrating-teamcity-with-docker.html#Conforming+with+Docker+download+rate+limits)

## View monthly pulls and included usage

You can view your monthly pulls on the [Usage page](https://hub.docker.com/usage/pulls) in Docker Hub.

On that page, you can also send a report to your email that contains a comma
separated file with the following detailed information.

| CSV column | Definition | Usage guidance |
| --- | --- | --- |
| datehour | The date and hour (yyyy/mm/dd/hh) of the pull that resulted in the data transfer. | This helps in identifying peak usage times and patterns. |
| user_name | The Docker ID of the user that pulled the image | This lets organization owners track data consumption per user and manage resources effectively. |
| repository | The name of the repository of the image that was pulled. | This lets you identify which repositories are most frequently accessed and consume most of the data transfer. |
| access_token_name | Name of the access token that was used for authentication with Docker CLI.generatedtokens are automatically generated by the Docker client when a user signs in. | Personal access tokens are usually used to authenticate automated tools (Docker Desktop, CI/CD tools, etc.). This is useful for identifying which automated system issued the pull. |
| ips | The IP address that was used to pull the image. This field is aggregated, so more than one IP address may appear, representing all the IPs used to pull an image within the same date and hour. | This helps you understand the origin of the data transfer, which is useful for diagnosing and identifying patterns in automated or manual pulls. |
| repository_privacy | The privacy state of the image repository that was pulled. This can either bepublicorprivate. | This distinguishes between public and private repositories to identify which data transfer threshold the pull impacts. |
| tag | The tag for the image. The tag is only available if the pull included a tag. | This helps in identifying the image. Tags are often used to identify specific versions or variants of an image. |
| digest | The unique image digest for the image. | This helps in identifying the image. |
| version_checks | The number of version checks accumulated for the date and hour of each image repository. Depending on the client, a pull can do a version check to verify the existence of an image or tag without downloading it. | This helps identify the frequency of version checks, which you can use to analyze usage trends and potential unexpected behaviors. |
| pulls | The number of pulls accumulated for the date and hour of each image repository. | This helps identify the frequency of repository pulls, which you can use to analyze usage trends and potential unexpected behaviors. |

## View pull rate and limit

The pull rate limit is calculated on a 6-hour basis. There is no pull rate
limit for users or automated systems with a paid subscription. Unauthenticated
and Docker Personal users using Docker Hub will experience rate limits on image
pulls.

When you issue a pull and you are over the limit, Docker Hub returns a
`429` response code with the following body when the manifest is requested:

```text
You have reached your pull rate limit. You may increase the limit by authenticating and upgrading: https://www.docker.com/increase-rate-limits
```

This error message appears in the Docker CLI or in the Docker Engine logs.

To view your current pull rate and limit:

> Note
>
> To check your limits, you need `curl`, `grep`, and `jq` installed.

1. Get a token.
  - To get a token anonymously, if you are pulling anonymously:
    ```console
    $ TOKEN=$(curl "https://auth.docker.io/token?service=registry.docker.io&scope=repository:ratelimitpreview/test:pull" | jq -r .token)
    ```
  - To get a token with a user account, if you are authenticated, insert your
    username and password in the following command:
    ```console
    $ TOKEN=$(curl --user 'username:password' "https://auth.docker.io/token?service=registry.docker.io&scope=repository:ratelimitpreview/test:pull" | jq -r .token)
    ```
2. Get the headers that contain your limits. These headers are returned on both
  GET and HEAD requests. Using GET emulates a real pull and counts towards the
  limit. Using HEAD won't.
  ```console
  $ curl --head -H "Authorization: Bearer $TOKEN" https://registry-1.docker.io/v2/ratelimitpreview/test/manifests/latest
  ```
3. Examine the headers. You should see the following headers.
  ```text
  ratelimit-limit: 100;w=21600
  ratelimit-remaining: 20;w=21600
  docker-ratelimit-source: 192.0.2.1
  ```
  In the previous example, the pull limit is 100 pulls per 21600 seconds (6
  hours), and there are 20 pulls remaining.
  If you don't see any `ratelimit` header, it could be because the image or your IP
  is unlimited in partnership with a publisher, provider, or an open source
  organization. It could also mean that the user you are pulling as is part of a
  paid Docker subscription. Pulling that image won't count toward pull rate limits if you
  don't see these headers.

---

# Docker Hub usage and limits

> Learn about usage and limits for Docker Hub.

# Docker Hub usage and limits

   Table of contents

---

The following table provides an overview of the included usage and limits for each
user type, subject to fair use:

| User type | Pull rate limit per 6 hours | Number of public repositories | Number of private repositories |
| --- | --- | --- | --- |
| Business (authenticated) | Unlimited | Unlimited | Unlimited |
| Team (authenticated) | Unlimited | Unlimited | Unlimited |
| Pro (authenticated) | Unlimited | Unlimited | Unlimited |
| Personal (authenticated) | 200 | Unlimited | Up to 1 |
| Unauthenticated users | 100 per IPv4 address or IPv6 /64 subnet | Not applicable | Not applicable |

For more details, see [Pull usage and limits](https://docs.docker.com/docker-hub/usage/pulls/).

## Fair use

When utilizing the Docker Platform, users should be aware that excessive data
transfer, pull rates, or data storage can lead to throttling, or additional
charges. To ensure fair resource usage and maintain service quality, we reserve
the right to impose restrictions or apply additional charges to accounts
exhibiting excessive data and storage consumption.

### Abuse rate limit

Docker Hub has an abuse rate limit to protect the application and
infrastructure. This limit applies to all requests to Hub properties including
web pages, APIs, and image pulls. The limit is applied per IPv4 address or per
IPv6 /64 subnet, and while the limit changes over time depending on load and
other factors, it's in the order of thousands of requests per minute. The abuse
limit applies to all users equally regardless of account level.

You can differentiate between the pull rate limit and abuse rate limit by
looking at the error code. The abuse limit returns a simple `429 Too Many Requests` response. The pull limit returns a longer error message that includes
a link to documentation.
