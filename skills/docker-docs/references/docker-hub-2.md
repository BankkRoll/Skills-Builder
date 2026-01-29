# Docker Hub release notes and more

# Docker Hub release notes

> Learn about the new features, bug fixes, and breaking changes for Docker Hub

# Docker Hub release notes

   Table of contents

---

Here you can learn about the latest changes, new features, bug fixes, and
known issues for each Docker Hub release.

## 2025-02-18

### New

- You can delete images and image indexes using [Image Management](https://docs.docker.com/docker-hub/repos/manage/hub-images/manage/).

## 2024-12-12

### New

- The AI Catalog in Docker Hub is available directly through Docker Desktop.

## 2024-03-23

### New

- You can tag Docker Hub repositories with [categories](https://docs.docker.com/docker-hub/repos/manage/information/#repository-categories).

## 2023-12-11

- The Advanced Image Management feature, along with the corresponding API endpoints, has been retired.
  See [docker/roadmap#534](https://github.com/docker/roadmap/issues/534).
  The following API endpoints have been removed:
  ```text
  /namespaces/{namespace}/repositories/{repository}/images
  /namespaces/{namespace}/repositories/{repository}/images/{digest}/tags
  /namespaces/{namespace}/repositories/{repository}/images-summary
  /namespaces/{namespace}/delete-images
  ```

## 2023-08-28

- Organizations with SSO enabled can assign members to roles, organizations, and teams with [SCIM role mapping](https://docs.docker.com/enterprise/security/provisioning/scim/#set-up-role-mapping).

## 2023-07-26

### New

- Organizations can assign the
  [editor role](https://docs.docker.com/enterprise/security/roles-and-permissions/) to members to grant additional permissions without full administrative access.

## 2023-05-09

### New

- Docker Business subscribers can now [create a company](https://docs.docker.com/admin/company/new-company/) in Docker Hub to manage organizations and settings.

## 2023-03-07

### New

- You can now automatically sync user updates with your Docker organizations and teams with [Group Mapping](https://docs.docker.com/enterprise/security/provisioning/group-mapping/) for SSO and SCIM provisioning.

## 2022-12-12

### New

- The new domain audit feature lets you audit your domains for users who aren't a member of your organization.

## 2022-09-26

### New

- The new [autobuild feature](https://docs.docker.com/docker-hub/repos/manage/builds/manage-builds/#check-your-active-builds) lets you view your in-progress logs every 30 seconds instead of when the build is complete.

## 2022-09-21

### Bug fixes and enhancements

- In Docker Hub, you can now download a
  [registry.json](https://docs.docker.com/enterprise/security/enforce-sign-in/) file or copy the commands to create a registry.json file to enforce sign-in for your organization.

## 2022-09-19

### Bug fixes and enhancements

- You can now [export a CSV file of members](https://docs.docker.com/admin/organization/members/#export-members) from organizations that you own.

## 2022-07-22

### Bug fixes and enhancements

- You can now invite members to your organization with a CSV file containing their email addresses. The CSV file can either be a file you create for this specific purpose or one that’s extracted from another in-house system.

## 2022-07-19

### Bug fixes and enhancements

- SCIM is now available for organizations with a Docker Business subscription using an Entra ID (formerly Azure AD) identity provider.

## 2022-06-23

### New

- With [SCIM](https://docs.docker.com/enterprise/security/provisioning/scim/), you can manage users within your Okta identity provider (IdP). In addition, you can enable SCIM on organizations that are part of the Docker Business subscription.

## 2022-05-24

### New

- [Registry Access Management](https://docs.docker.com/enterprise/security/hardened-desktop/registry-access-management/) is now available for all Docker Business subscriptions. When enabled, your users can access specific registries in Docker Hub.

## 2022-05-03

### New

- Organization owners can [invite new members](https://docs.docker.com/admin/organization/members/#invite-members) to an organization via Docker ID or email address.

## 2021-11-15

### New

- You can now purchase or upgrade to a Docker Business subscription using a credit card. To learn more, see [Upgrade your subscription](https://docs.docker.com/subscription/change/).

## 2021-08-31

### New

Docker has [announced](https://www.docker.com/blog/updating-product-subscriptions/) updates and extensions to the product subscriptions to increase productivity, collaboration, and added security for our developers and businesses. Docker subscription tiers now include Personal, Pro, Team, and Business.

The updated [Docker Subscription Service Agreement](https://www.docker.com/legal/docker-subscription-service-agreement) includes a change to the terms for **Docker Desktop**.

- Docker Desktop **remains free** for small businesses (fewer than 250 employees AND less than $10 million in annual revenue), personal use, education, and non-commercial open source projects.
- It requires a paid subscription (**Pro, Team, or Business**), for as little as $5 a month, for professional use in larger enterprises.
- The effective date of these terms is August 31, 2021. There is a grace period until January 31, 2022 for those that will require a paid subscription to use Docker Desktop.
- The Docker Pro and Docker Team subscriptions now **include commercial use** of Docker Desktop.
- The existing Docker Free subscription has been renamed **Docker Personal**.
- **No changes** to Docker Engine or any other upstream **open source** Docker or Moby project.
  To understand how these changes affect you, read the [FAQs](https://www.docker.com/pricing/faq). For more information, see [Docker subscription overview](https://docs.docker.com/subscription/).

## 2021-05-05

### Enhancement

When managing the content of your repositories, you can now filter the results based on the currentness of the tags and more easily identify your untagged images.

For Docker Hub API documentation, see
[Docker Hub API Reference](https://docs.docker.com/reference/api/hub/latest/#operation/GetNamespacesRepositoriesImages).

## 2021-04-13

### Enhancement

The **Billing Details** page now shows any organizations you own, in addition to your personal account. This allows you to clearly identify the billing details of your chosen namespace, and enables you to switch between your personal and your organization accounts to view or update the details.

## 2021-04-09

### Enhancement

You can now specify any email address to receive billing-related emails for your organization. The email address doesn't have to be associated with an organization owner account. You must be an owner of the organization to update any billing details.

To change the email address receiving billing-related emails, log into Docker Hub and navigate to the **Billing** tab of your organization. Select **Payment Methods** > **Billing Information**. Enter the new email address that you'd like to use in the **Email** field. Click **Update** for the changes to take effect.

For details on how to update your billing information, see [Update billing information](https://docs.docker.com/billing/).

## 2021-03-22

### New feature

**Advanced Image Management dashboard**

Docker introduces the Advanced Image Management dashboard that enables you to view and manage Docker images in your repositories.

## 2021-01-25

### New feature

Docker introduces Audit logs, a new feature that allows team owners to view a list of activities that occur at organization and repository levels. This feature begins tracking the activities from the release date, that is, **from 25 January 2021**.

For more information about this feature and for instructions on how to use it, see [Activity logs](https://docs.docker.com/admin/organization/activity-logs/).

## 2020-11-10

### New feature

The **Repositories** view now shows which images have gone stale because they haven't been pulled or pushed recently. For more information, see [repository tags](https://docs.docker.com/docker-hub/repos/manage/access/#view-repository-tags).

## 2020-10-07

### New feature

Docker introduces Hub Vulnerability Scanning which enables you to automatically scan Docker images for vulnerabilities using Snyk. For more information, see [Hub Vulnerability Scanning](https://docs.docker.com/docker-hub/repos/manage/vulnerability-scanning/).

## 2020-05-14

### New features

- Docker has announced a new, per-seat pricing model to accelerate developer workflows for cloud-native development. The previous private repository/concurrent autobuild-based plans have been replaced with new **Pro** and **Team** plans that include unlimited private repositories. For more information, see [Docker subscription](https://docs.docker.com/subscription/).
- Docker has enabled download rate limits for downloads and pull requests on Docker Hub. This caps the number of objects that users can download within a specified timeframe. For more information, see
  [Usage and limits](https://docs.docker.com/docker-hub/usage/).

## 2019-11-04

### Enhancements

- The [repositories page](https://docs.docker.com/docker-hub/repos/) and all
  related settings and tabs have been updated and moved from `cloud.docker.com`
  to `hub.docker.com`. You can access the page at its new URL: [https://hub.docker.com/repositories](https://hub.docker.com/repositories).

### Known Issues

- Scan results don't appear for some official images.

## 2019-10-21

### New features

- **Beta:** Docker Hub now supports two-factor authentication (2FA). Enable it in your account settings, under the **Security** section.
  > If you lose both your 2FA authentication device and recovery code, you may
  > not be able to recover your account.

### Enhancements

- As a security measure, when two-factor authentication is enabled, the Docker CLI requires a personal access token instead of a password to log in.

### Known Issues

- Scan results don't appear for some official images.

## 2019-10-02

### Enhancements

- You can now manage teams and members straight from your [organization page](https://hub.docker.com/orgs).
  Each organization page now breaks down into these tabs:
  - **New:** Members - manage your members directly from this page (delete,
    add, or open their teams)
  - **New:** Teams - search by team or username, and open up any team page to
    manage the team
  - **New:** Invitees (conditional tab, only if an invite exists) - resend or
    remove invitations from this tab
  - Repositories
  - Settings
  - Billing

### Bug fixes

- Fixed an issue where Kinematic could not connect and log in to Docker Hub.

### Known Issues

- Scan results don't appear for some official images.

## 2019-09-19

### New features

- You can now
  [create personal access tokens](https://docs.docker.com/security/access-tokens/) in Docker Hub and use them to authenticate from the Docker CLI. Find them in your account settings, under the new **Security** section.

### Known Issues

- Scan results don't appear for some official images.

## 2019-09-16

### Enhancements

- The [billing page](https://docs.docker.com/subscription/change/) for personal accounts has been updated. You can access the page at its new URL: [https://hub.docker.com/billing/plan](https://hub.docker.com/billing/plan).

### Known Issues

- Scan results don't appear for some official images.

## 2019-09-05

### Enhancements

- The `Tags` tab on an image page now provides additional information for each tag:
  - A list of digests associated with the tag
  - The architecture it was built on
  - The OS
  - The user who most recently updated an image for a specific tag
- The security scan summary for Docker Official Images has been updated.

### Known Issues

- Scan results don't appear for some official images.

---

# Archive or unarchive a repository

> Learn how to archive or unarchive a repository on Docker Hub

# Archive or unarchive a repository

   Table of contents

---

You can archive a repository on Docker Hub to mark it as read-only and indicate
that it's no longer actively maintained. This helps prevent the use of outdated
or unsupported images in workflows. Archived repositories can also be unarchived
if needed.

Docker Hub highlights repositories that haven't been updated in over a year by
displaying an icon (
![outdated icon](https://docs.docker.com/docker-hub/repos/images/outdated-icon.webp)
) next to them on the [Repositoriespage](https://hub.docker.com/repositories/). Consider reviewing these
highlighted repositories and archiving them if necessary.

When a repository is archived, the following occurs:

- The repository information can't be modified.
- New images can't be pushed to the repository.
- An **Archived** label is displayed on the public repository page.
- Users can still pull the images.

You can unarchive an archived repository to remove the archived state. When
unarchived, the following occurs:

- The repository information can be modified.
- New images can be pushed to the repository.
- The **Archived** label is removed on the public repository page.

## Archive a repository

1. Sign in to [Docker Hub](https://hub.docker.com).
2. Select **My Hub** > **Repositories**.
  A list of your repositories appears.
3. Select a repository.
  The **General** page for the repository appears.
4. Select the **Settings** tab.
5. Select **Archive repository**.
6. Enter the name of your repository to confirm.
7. Select **Archive**.

## Unarchive a repository

1. Sign in to [Docker Hub](https://hub.docker.com).
2. Select **My Hub** > **Repositories**.
  A list of your repositories appears.
3. Select a repository.
  The **General** page for the repository appears.
4. Select the **Settings** tab.
5. Select **Unarchive repository**.

---

# Create a repository

> Learn how to create a repository on Docker Hub

# Create a repository

---

1. Sign in to [Docker Hub](https://hub.docker.com).
2. Select **My Hub** > **Repositories**.
3. Near the top-right corner, select **Create repository**.
4. Select a **Namespace**.
  You can choose to locate it under your own user account, or under any
  organization where you are an owner or editor.
5. Specify the **Repository Name**.
  The repository name needs to:
  - Be unique
  - Have between 2 and 255 characters
  - Only contain lowercase letters, numbers, hyphens (`-`), and underscores
    (`_`)
  > Note
  >
  > You can't rename a Docker Hub repository once it's created.
6. Specify the **Short description**.
  The description can be up to 100 characters. It appears in search results.
7. Select the default visibility.
  - **Public**: The repository appears in Docker Hub search results and can be
    pulled by everyone.
  - **Private**: The repository doesn't appear in Docker Hub search results and
    is only accessible to you and collaborators. In addition, if you selected
    an organization's namespace, then the repository is accessible to those
    with applicable roles or permissions. For more details, see
    [Roles and
    permissions](https://docs.docker.com/enterprise/security/roles-and-permissions/).
  > Note
  >
  > For organizations creating a new repository, if you're unsure which
  > visibility to choose, then Docker recommends that you select **Private**.
8. Select **Create**.

After the repository is created, the **General** page appears. You are now able to manage:

- [Repository information](https://docs.docker.com/docker-hub/repos/manage/information/)
- [Access](https://docs.docker.com/docker-hub/repos/manage/access/)
- [Images](https://docs.docker.com/docker-hub/repos/manage/hub-images/)
- [Automated builds](https://docs.docker.com/docker-hub/repos/manage/builds/)
- [Webhooks](https://docs.docker.com/docker-hub/repos/manage/webhooks/)
- [Image security insights](https://docs.docker.com/docker-hub/repos/manage/vulnerability-scanning/)

---

# Delete a repository

> Learn how to delete a repository on Docker Hub

# Delete a repository

---

> Warning
>
> Deleting a repository deletes all the images it contains and its build
> settings. This action can't be undone.

1. Sign in to [Docker Hub](https://hub.docker.com).
2. Select **My Hub** > **Repositories**.
  A list of your repositories appears.
3. Select a repository.
  The **General** page for the repository appears.
4. Select the **Settings** tab.
5. Select **Delete repository**.
6. Enter the name of your repository to confirm.
7. Select **Delete Repository Forever**.

---

# Access management

> Discover how to manage access to repositories on Docker Hub.

# Access management

   Table of contents

---

In this topic learn about the features available to manage access to your
repositories. This includes visibility, collaborators, roles, teams, and
organization access tokens.

## Repository visibility

The most basic repository access is controlled via the visibility. A
repository's visibility can be public or private.

With public visibility, the repository appears in Docker Hub search results and
can be pulled by everyone. To manage push access to public personal
repositories, you can use collaborators. To manage push access to public
organization repositories, you can use roles, teams, or organization access
tokens.

With private visibility, the repository doesn't appear in Docker Hub search
results and is only accessible to those with granted permission. To manage push
and pull access to private personal repositories, you can use collaborators. To
manage push and pull access to private organization repositories, you can use
roles, teams, or organization access tokens.

### Change repository visibility

When creating a repository in Docker Hub, you can set the repository visibility.
In addition, you can set the default repository visibility when a repository is
created in your personal repository settings. The following describes how to
change the visibility after the repository has been created.

To change repository visibility:

1. Sign in to [Docker Hub](https://hub.docker.com).
2. Select **My Hub** > **Repositories**.
3. Select a repository.
  The **General** page for the repository appears.
4. Select the **Settings** tab.
5. Under **Visibility settings**, select one of the following:
  - **Make public**: The repository appears in Docker Hub search results and can be
    pulled by everyone.
  - **Make private**: The repository doesn't appear in Docker Hub search results
    and is only accessible to you and collaborators. In addition, if the
    repository is in an organization's namespace, then the repository
    is accessible to those with applicable roles or permissions.
6. Type the repository's name to verify the change.
7. Select **Make public** or **Make private**.

## Collaborators

A collaborator is someone you want to give `push` and `pull` access to a
personal repository. Collaborators aren't able to perform any administrative
tasks such as deleting the repository or changing its visibility from private to
public. In addition, collaborators can't add other collaborators.

Only personal repositories can use collaborators. You can add unlimited
collaborators to public repositories, and Docker Pro accounts can add up to 1
collaborator on private repositories.

Organization repositories can't use collaborators, but can use member roles,
teams, or organization access tokens to manage access.

### Manage collaborators

1. Sign in to [Docker Hub](https://hub.docker.com).
2. Select **My Hub** > **Repositories**.
  A list of your repositories appears.
3. Select a repository.
  The **General** page for the repository appears.
4. Select the **Collaborators** tab.
5. Add or remove collaborators based on their Docker username.

You can choose collaborators and manage their access to a private
repository from that repository's **Settings** page.

## Organization roles

Organizations can use roles for individuals, giving them different
permissions in the organization. For more details, see
[Roles and
permissions](https://docs.docker.com/enterprise/security/roles-and-permissions/).

## Organization teams

Organizations can use teams. A team can be assigned fine-grained repository
access.

### Configure team repository permissions

You must create a team before you are able to configure repository permissions.
For more details, see
[Create and manage a
team](https://docs.docker.com/admin/organization/manage-a-team/).

To configure team repository permissions:

1. Sign in to [Docker Hub](https://hub.docker.com).
2. Select **My Hub** > **Repositories**.
  A list of your repositories appears.
3. Select a repository.
  The **General** page for the repository appears.
4. Select the **Permissions** tab.
5. Add, modify, or remove a team's repository permissions.
  - Add: Specify the **Team**, select the **Permission**, and then select **Add**.
  - Modify: Specify the new permission next to the team.
  - Remove: Select the **Remove permission** icon next to the team.

## Organization access tokens (OATs)

Organizations can use OATs. OATs let you assign fine-grained repository access
permissions to tokens. For more details, see
[Organization access
tokens](https://docs.docker.com/enterprise/security/access-tokens/).

## Gated distribution

Availability: Early Access

Gated distribution allows publishers to securely share private container images with external customers or partners, without giving them full organization access or visibility into your teams, collaborators, or other repositories.

This feature is ideal for commercial software publishers who want to control who can pull specific images while preserving a clean separation between internal users and external consumers.

If you are interested in Gated Distribution contact the [Docker Sales Team](https://www.docker.com/pricing/contact-sales/) for more information.

### Key features

- **Private repository distribution**: Content is stored in private repositories and only accessible to explicitly invited users.
- **External access without organization membership**: External users don't need to be added to your internal organization to pull images.
- **Pull-only permissions**: External users receive pull-only access and cannot push or modify repository content.
- **Invite-only access**: Access is granted through authenticated email invites, managed via API.

### Invite distributor members via API

> Note
>
> When you invite members, you assign them a role. See
> [Roles and permissions](https://docs.docker.com/enterprise/security/roles-and-permissions/) for details about the access permissions for each role.

Distributor members (used for gated distribution) can only be invited using the Docker Hub API. UI-based invitations are not currently supported for this role. To invite distributor members, use the Bulk create invites API endpoint.

To invite distributor members:

1. Use the [Authentication API](https://docs.docker.com/reference/api/hub/latest/#tag/authentication-api/operation/AuthCreateAccessToken) to generate a bearer token for your Docker Hub account.
2. Create a team in the Hub UI or use the [Teams API](https://docs.docker.com/reference/api/hub/latest/#tag/groups/paths/~1v2~1orgs~1%7Borg_name%7D~1groups/post).
3. Grant repository access to the team:
  - In the Hub UI: Navigate to your repository settings and add the team with "Read-only" permissions
  - Using the [Repository Teams API](https://docs.docker.com/reference/api/hub/latest/#tag/repositories/paths/~1v2~1repositories~1%7Bnamespace%7D~1%7Brepository%7D~1groups/post): Assign the team to your repositories with "read-only" access level
4. Use the [Bulk create invites endpoint](https://docs.docker.com/reference/api/hub/latest/#tag/invites/paths/~1v2~1invites~1bulk/post) to send email invites with the distributor member role. In the request body, set the "role" field to "distributor_member".
5. The invited user will receive an email with a link to accept the invite. After signing in with their Docker ID, they'll be granted pull-only access to the specified private repository as a distributor member.

---

# Advanced options for autobuild and autotest

> Automated builds

# Advanced options for autobuild and autotest

   Table of contents

---

> Note
>
> Automated builds require a
> Docker Pro, Team, or Business subscription.

The following options allow you to customize your automated build and automated
test processes.

## Environment variables for building and testing

Several utility environment variables are set by the build process, and are
available during automated builds, automated tests, and while executing
hooks.

> Note
>
> These environment variables are only available to the build and test
> processes and don't affect your service's run environment.

- `SOURCE_BRANCH`: the name of the branch or the tag that is currently being tested.
- `SOURCE_COMMIT`: the SHA1 hash of the commit being tested.
- `COMMIT_MSG`: the message from the commit being tested and built.
- `DOCKER_REPO`: the name of the Docker repository being built.
- `DOCKERFILE_PATH`: the dockerfile currently being built.
- `DOCKER_TAG`: the Docker repository tag being built.
- `IMAGE_NAME`: the name and tag of the Docker repository being built. (This variable is a combination of `DOCKER_REPO`:`DOCKER_TAG`.)

If you are using these build environment variables in a
`docker-compose.test.yml` file for automated testing, declare them in your `sut`
service's environment as shown below.

```yaml
services:
  sut:
    build: .
    command: run_tests.sh
    environment:
      - SOURCE_BRANCH
```

## Override build, test or push commands

Docker Hub allows you to override and customize the `build`, `test` and `push`
commands during automated build and test processes using hooks. For example, you
might use a build hook to set build arguments used only during the build
process. You can also set up [custom build phase hooks](#custom-build-phase-hooks)
to perform actions in between these commands.

> Important
>
> Use these hooks with caution. The contents of these hook files replace the
> basic `docker` commands, so you must include a similar build, test or push
> command in the hook or your automated process does not complete.

To override these phases, create a folder called `hooks` in your source code
repository at the same directory level as your Dockerfile. Create a file called
`hooks/build`, `hooks/test`, or `hooks/push` and include commands that the
builder process can execute, such as `docker` and `bash` commands (prefixed
appropriately with `#!/bin/bash`).

These hooks run on an instance of [Ubuntu](https://releases.ubuntu.com/),
which includes interpreters
such as Perl or Python, and utilities such as `git` or `curl`. Refer to the
[Ubuntu documentation](https://ubuntu.com/)
for the full list of available interpreters and utilities.

## Custom build phase hooks

You can run custom commands between phases of the build process by creating
hooks. Hooks allow you to provide extra instructions to the autobuild and
autotest processes.

Create a folder called `hooks` in your source code repository at the same
directory level as your Dockerfile. Place files that define the hooks in that
folder. Hook files can include both `docker` commands, and `bash` commands as
long as they are prefixed appropriately with `#!/bin/bash`. The builder executes
the commands in the files before and after each step.

The following hooks are available:

- `hooks/post_checkout`
- `hooks/pre_build`
- `hooks/post_build`
- `hooks/pre_test`
- `hooks/post_test`
- `hooks/pre_push` (only used when executing a build rule or [Automated build](https://docs.docker.com/docker-hub/repos/manage/builds/) )
- `hooks/post_push` (only used when executing a build rule or [Automated build](https://docs.docker.com/docker-hub/repos/manage/builds/) )

### Build hook examples

#### Override the "build" phase to set variables

Docker Hub allows you to define build environment variables either in the hook
files, or from the automated build interface, which you can then reference in hooks.

The following example defines a build hook that uses `docker build` arguments to
set the variable `CUSTOM` based on the value of variable defined using the
Docker Hub build settings. `$DOCKERFILE_PATH` is a variable that you provide
with the name of the Dockerfile you want to build, and `$IMAGE_NAME` is the name
of the image being built.

```console
$ docker build --build-arg CUSTOM=$VAR -f $DOCKERFILE_PATH -t $IMAGE_NAME .
```

> Important
>
> A `hooks/build` file overrides the basic `docker build` command used by the builder, so you must include a similar build command in the hook or
> the automated build fails.

Refer to the
[docker build documentation](https://docs.docker.com/reference/cli/docker/buildx/build/#build-arg)
to learn more about Docker build-time variables.

#### Push to multiple repositories

By default the build process pushes the image only to the repository where the
build settings are configured. If you need to push the same image to multiple
repositories, you can set up a `post_push` hook to add additional tags and push
to more repositories.

```console
$ docker tag $IMAGE_NAME $DOCKER_REPO:$SOURCE_COMMIT
$ docker push $DOCKER_REPO:$SOURCE_COMMIT
```

## Source repository or branch clones

When Docker Hub pulls a branch from a source code repository, it performs
a shallow clone, it clones only the tip of the specified branch. This has the advantage
of minimizing the amount of data transfer necessary from the repository and
speeding up the build because it pulls only the minimal code necessary.

As a result, if you need to perform a custom action that relies on a different
branch, such as a `post_push` hook, you can't checkout that branch unless
you do one of the following:

- You can get a shallow checkout of the target branch by doing the following:
  ```console
  $ git fetch origin branch:mytargetbranch --depth 1
  ```
- You can also "unshallow" the clone, which fetches the whole Git history (and
  potentially takes a long time / moves a lot of data) by using the `--unshallow`
  flag on the fetch:
  ```console
  $ git fetch --unshallow origin
  ```

---

# Automated repository tests

> Automated tests

# Automated repository tests

   Table of contents

---

> Note
>
> Automated builds require a
> Docker Pro, Team, or Business subscription.

Docker Hub can automatically test changes to your source code repositories
using containers. You can enable `Autotest` on any Docker Hub repository
to run tests on each pull request to the source code repository to create a
continuous integration testing service.

Enabling `Autotest` builds an image for testing purposes, but does not
automatically push the built image to the Docker repository. If you want to push
built images to your Docker Hub repository, enable [Automated Builds](https://docs.docker.com/docker-hub/repos/manage/builds/).

## Set up automated test files

To set up your automated tests, create a `docker-compose.test.yml` file which
defines a `sut` service that lists the tests to be run.
The `docker-compose.test.yml` file should be located in the same directory that
contains the Dockerfile used to build the image.

For example:

```yaml
services:
  sut:
    build: .
    command: run_tests.sh
```

The previous example builds the repository, and runs the `run_tests.sh` file inside
a container using the built image.

You can define any number of linked services in this file. The only requirement
is that `sut` is defined. Its return code determines if tests passed or not.
Tests pass if the `sut` service returns `0`, and fail otherwise.

> Note
>
> Only the `sut` service and all other services listed in
> [depends_on](https://docs.docker.com/reference/compose-file/services/#depends_on) are
> started. If you have services that poll for changes in other services, be sure
> to include the polling services in the
> [depends_on](https://docs.docker.com/reference/compose-file/services/#depends_on)
> list to make sure all of your services start.

You can define more than one `docker-compose.test.yml` file if needed. Any file
that ends in `.test.yml` is used for testing, and the tests run sequentially.
You can also use [custom build hooks](https://docs.docker.com/docker-hub/repos/manage/builds/advanced/#override-build-test-or-push-commands)
to further customize your test behavior.

> Note
>
> If you enable automated builds, they also run any tests defined
> in the `test.yml` files.

## Enable automated tests on a repository

To enable testing on a source code repository, you must first create an
associated build-repository in Docker Hub. Your `Autotest` settings are
configured on the same page as [automated builds](https://docs.docker.com/docker-hub/repos/manage/builds/), however
you do not need to enable autobuilds to use autotest. Autobuild is enabled per
branch or tag, and you do not need to enable it at all.

Only branches that are configured to use autobuild push images to the
Docker repository, regardless of the Autotest settings.

1. Sign in to Docker Hub and select **My Hub** > **Repositories**.
2. Select the repository you want to enable `Autotest` on.
3. From the repository view, select the **Builds** tab.
4. Select **Configure automated builds**.
5. Configure the automated build settings as explained in [Automated builds](https://docs.docker.com/docker-hub/repos/manage/builds/).
  At minimum you must configure:
  - The source code repository
  - The build location
  - At least one build rule
6. Choose your **Autotest** option.
  The following options are available:
  - `Off`: No additional test builds. Tests only run if they're configured
    as part of an automated build.
  - `Internal pull requests`: Run a test build for any pull requests
    to branches that match a build rule, but only when the pull request comes
    from the same source repository.
  - `Internal and external pull requests`: Run a test build for any
    pull requests to branches that match a build rule, including when the
    pull request originated in an external source repository.
  > Important
  >
  > For security purposes, autotest on external pull requests is
  > limited on public repositories. Private images are not pulled and
  > environment variables defined in Docker Hub are not
  > available. Automated builds continue to work as usual.
7. Select **Save** to save the settings, or select **Save and build** to save and
  run an initial test.

## Check your test results

From the repository's details page, select **Timeline**.

From this tab you can see any pending, in-progress, successful, and failed
builds and test runs for the repository.

You can choose any timeline entry to view the logs for each test run.

---

# Configure automated builds from GitHub and BitBucket

> Link to GitHub and BitBucket

# Configure automated builds from GitHub and BitBucket

   Table of contents

---

> Note
>
> Automated builds require a Docker Pro, Team, or Business subscription.

To automate building and testing of your images, you link to your hosted source
code service to Docker Hub so that it can access your source code
repositories. You can configure this link for user accounts or
organizations.

If you are linking a source code provider to create autobuilds for a team, follow the instructions to [create a service account](https://docs.docker.com/docker-hub/repos/manage/builds/#service-users-for-team-autobuilds) for the team before linking the account as described below.

## Link to a GitHub user account

1. Sign in to Docker Hub.
2. Select **My Hub** > **Settings** > **Linked accounts**.
3. Select **Link provider** for the source provider you want to link.
  If you want to unlink your current GitHub account and relink to a new GitHub account, make sure to completely sign out of [GitHub](https://github.com/) before linking via Docker Hub.
4. Review the settings for the **Docker Hub Builder** OAuth application.
  ![Granting access to GitHub account](https://docs.docker.com/docker-hub/repos/manage/builds/images/authorize-builder.png)  ![Granting access to GitHub account](https://docs.docker.com/docker-hub/repos/manage/builds/images/authorize-builder.png)
  > Note
  >
  > If you are the owner of any GitHub organizations, you might see
  > options to grant Docker Hub access to them from this screen. You can also
  > individually edit an organization's third-party access settings to grant or
  > revoke Docker Hub's access. See
  > [Grant access to a GitHub organization](https://docs.docker.com/docker-hub/repos/manage/builds/link-source/#grant-access-to-a-github-organization)
  > to learn more.
5. Select **Authorize docker** to save the link.

### Grant access to a GitHub organization

If you are the owner of a GitHub organization, you can grant or revoke Docker
Hub's access to the organization's repositories. Depending on the GitHub
organization's settings, you may need to be an organization owner.

If the organization has not had specific access granted or revoked before, you
can often grant access at the same time as you link your user account. In this
case, a **Grant access** button appears next to the organization name in the
link accounts screen, as shown below. If this button does not appear, you must
manually grant the application's access.

To manually grant Docker Hub access to a GitHub organization:

1. Link your user account using the instructions above.
2. From your GitHub Account settings, locate the **Organization settings**
  section at the lower left.
3. Select the organization you want to give Docker Hub access to.
4. Select **Third-party access**.
  The page displays a list of third party applications and their access
  status.
5. Select the pencil icon next to **Docker Hub Builder**.
6. Select **Grant access** next to the organization.

### Revoke access to a GitHub organization

To revoke Docker Hub's access to an organization's GitHub repositories:

1. From your GitHub Account settings, locate the **Organization settings** section at the lower left.
2. Select the organization you want to revoke Docker Hub's access to.
3. From the Organization Profile menu, select **Third-party access**.
  The page displays a list of third party applications and their access status.
4. Select the pencil icon next to Docker Hub Builder.
5. On the next page, select **Deny access**.

### Unlink a GitHub user account

To revoke Docker Hub's access to your GitHub account, you must unlink it both
from Docker Hub, and from your GitHub account.

1. Select **My Hub** > **Settings** > **Linked accounts**.
2. Select **Unlink provider** next to the source provider you want to remove.
3. Go to your GitHub account's **Settings** page.
4. Select **Applications** in the left navigation bar.
5. Select the `...` menu to the right of the Docker Hub Builder application and select **Revoke**.

> Note
>
> Each repository that is configured as an automated build source
> contains a webhook that notifies Docker Hub of changes in the repository.
> This webhook is not automatically removed when you revoke access to a source
> code provider.

## Link to a Bitbucket user account

1. Sign in to Docker Hub using your Docker ID.
2. Select **My Hub** > **Settings** > **Linked accounts**.
3. Select **Link provider** for the source provider you want to link.
4. If necessary, sign in to Bitbucket.
5. On the page that appears, select **Grant access**.

### Unlink a Bitbucket user account

To permanently revoke Docker Hub's access to your Bitbucket account, you must
unlink it both from Docker Hub, and revoke authorization in your Bitbucket account.

1. Sign in to Docker Hub.
2. Select **My Hub** > **Settings** > **Linked accounts**.
3. Select **Unlink provider** next to the source provider you want to remove.

> Important
>
> After unlinking the account on Docker Hub, you must also revoke the authorization on the Bitbucket end.

To revoke authorization in your Bitbucket account:

1. Go to your Bitbucket account and navigate to [Bitbucket settings](https://bitbucket.org/account/settings/app-authorizations/).
2. On the page that appears, select **OAuth**.
3. Select **Revoke** next to the Docker Hub line.

![Bitbucket Authorization revocation page](https://docs.docker.com/docker-hub/repos/manage/builds/images/bitbucket-revoke.png)  ![Bitbucket Authorization revocation page](https://docs.docker.com/docker-hub/repos/manage/builds/images/bitbucket-revoke.png)

> Note
>
> Each repository that is configured as an automated build source
> contains a webhook that notifies Docker Hub of changes in the repository. This
> webhook is not automatically removed when you revoke access to a source code
> provider.

---

# Manage autobuilds

> How to manage autobuilds in Docker Hub

# Manage autobuilds

   Table of contents

---

> Note
>
> Automated builds require a Docker Pro, Team, or Business subscription.

## Cancel or retry a build

While a build is in queue or running, a **Cancel** icon appears next to its build
report link on the **General** tab and on the **Builds** tab. You can also select
**Cancel** on the **Build report** page, or from the **Timeline** tab's logs
display for the build.

![List of builds showing the cancel icon](https://docs.docker.com/docker-hub/repos/manage/builds/images/build-cancelicon.png)  ![List of builds showing the cancel icon](https://docs.docker.com/docker-hub/repos/manage/builds/images/build-cancelicon.png)

## Check your active builds

A summary of a repository's builds appears both on the repository **General**
tab, and in the **Builds** tab. The **Builds** tab also displays a color coded
bar chart of the build queue times and durations. Both views display the
pending, in progress, successful, and failed builds for any tag of the
repository.

![Active builds](https://docs.docker.com/docker-hub/repos/manage/builds/images/index-active.png)  ![Active builds](https://docs.docker.com/docker-hub/repos/manage/builds/images/index-active.png)

From either location, you can select a build job to view its build report. The
build report shows information about the build job. This includes the source
repository and branch, or tag, the build logs, the build duration, creation time and location, and the user account the build occurred in.

> Note
>
> You can now view the progress of your builds every 30 seconds when you refresh the **Builds** page. With the in-progress build logs, you can debug your builds before they're finished.

![Build report](https://docs.docker.com/docker-hub/repos/manage/builds/images/index-report.png)  ![Build report](https://docs.docker.com/docker-hub/repos/manage/builds/images/index-report.png)

## Disable an automated build

Automated builds are enabled per branch or tag, and can be disabled and
re-enabled. You might do this when you want to only build manually for
a while, for example when you are doing major refactoring in your code. Disabling autobuilds doesn't disable [autotests](https://docs.docker.com/docker-hub/repos/manage/builds/automated-testing/).

To disable an automated build:

1. In [Docker Hub](https://hub.docker.com), go to **My Hub** > **Repositories**, select a repository, and select the **Builds** tab.
2. Select **Configure automated builds** to edit the repository's build settings.
3. In the **Build Rules** section, locate the branch or tag you no longer want
  to automatically build.
4. Select the **Autobuild** toggle next to the configuration line. When disabled the toggle is gray.
5. Select **Save**.
