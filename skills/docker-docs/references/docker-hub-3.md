# Set up automated builds and more

# Set up automated builds

> Set up automated builds

# Set up automated builds

   Table of contents

---

> Note
>
> Automated builds require a
> Docker Pro, Team, or Business subscription.

## Configure automated builds

You can configure repositories in Docker Hub so that they automatically
build an image each time you push new code to your source provider. If you have
[automated tests](https://docs.docker.com/docker-hub/repos/manage/builds/automated-testing/) configured, the new image is only pushed
when the tests succeed.

1. In [Docker Hub](https://hub.docker.com), go to **My Hub** > **Repositories**, and select a repository to view its details.
2. Select the **Builds** tab.
3. Select either GitHub or Bitbucket to connect where the image's source code is stored.
  > Note
  >
  > You may be redirected to the settings page to [link the code repository
  > service](https://docs.docker.com/docker-hub/repos/manage/builds/link-source/). Otherwise, if you are editing the build settings
  > for an existing automated build, select **Configure automated builds**.
4. Select the **source repository** to build the Docker images from.
  > Note
  >
  > You might need to specify an organization or user from
  > the source code provider. Once you select a user, source code
  > repositories appear in the **Select repository** drop-down list.
5. Optional. Enable [autotests](https://docs.docker.com/docker-hub/repos/manage/builds/automated-testing/#enable-automated-tests-on-a-repository).
6. Review the default **Build Rules**.
  Build rules control what Docker Hub builds into images from the contents
  of the source code repository, and how the resulting images are tagged
  within the Docker repository.
  A default build rule is set up for you, which you can edit or delete. This
  default rule sets builds from the `Branch` in your source code repository
  called `master` or `main`, and creates a Docker image tagged with `latest`.
  For more information, see [set up build rules](#set-up-build-rules).
7. Optional. Select the **plus** icon to add and [configure more build rules](#set-up-build-rules).
8. For each branch or tag, enable or disable the **Autobuild** toggle.
  Only branches or tags with autobuild enabled are built, tested, and have
  the resulting image pushed to the repository. Branches with autobuild
  disabled are built for test purposes (if enabled at the repository
  level), but the built Docker image isn't pushed to the repository.
9. For each branch or tag, enable or disable the **Build Caching** toggle.
  [Build caching](https://docs.docker.com/build/building/best-practices/#leverage-build-cache)
  can save time if you are building a large image frequently or have
  many dependencies. Leave the build caching disabled to
  make sure all of your dependencies are resolved at build time, or if
  you have a large layer that's quicker to build locally.
10. Select **Save** to save the settings, or select **Save and build** to save and
  run an initial test.
  > Note
  >
  > A webhook is automatically added to your source code repository to notify
  > Docker Hub on every push. Only pushes to branches that are listed as the
  > source for one or more tags, trigger a build.

### Set up build rules

By default when you set up automated builds, a basic build rule is created for you.
This default rule watches for changes to the `master` or `main` branch in your source code
repository, and builds the `master` or `main` branch into a Docker image tagged with
`latest`.

In the **Build Rules** section, enter one or more sources to build.

For each source:

- Select the **Source type** to build either a tag or a branch. This
  tells the build system what to look for in the source code repository.
- Enter the name of the **Source** branch or tag you want to build.
  The first time you configure automated builds, a default build rule is set up
  for you. This default set builds from the `Branch` in your source code called
  `master`, and creates a Docker image tagged with `latest`.
  You can also use a regex to select which source branches or tags to build.
  To learn more, see
  [regexes](#regexes-and-automated-builds).
- Enter the tag to apply to Docker images built from this source.
  If you configured a regex to select the source, you can reference the
  capture groups and use its result as part of the tag. To learn more, see
  [regexes](#regexes-and-automated-builds).
- Specify the **Dockerfile location** as a path relative to the root of the source code repository. If the Dockerfile is at the repository root, leave this path set to `/`.

> Note
>
> When Docker Hub pulls a branch from a source code repository, it performs a
> shallow clone - only the tip of the specified branch. Refer to
> [Advanced options for autobuild and autotest](https://docs.docker.com/docker-hub/repos/manage/builds/advanced/#source-repository-or-branch-clones)
> for more information.

### Environment variables for builds

You can set the values for environment variables used in your build processes
when you configure an automated build. Add your build environment variables by
selecting the **plus** icon next to the **Build environment variables** section, and
then entering a variable name and the value.

When you set variable values from the Docker Hub UI, you can use them by the
commands you set in `hooks` files. However, they're stored so that only users who have `admin` access to the Docker Hub repository can see their values. This
means you can use them to store access tokens or other information that
should remain secret.

> Note
>
> The variables set on the build configuration screen are used during
> the build processes only and shouldn't get confused with the environment
> values used by your service, for example to create service links.

## Advanced automated build options

At the minimum you need a build rule composed of a source branch, or tag, and a
destination Docker tag to set up an automated build. You can also:

- Change where the build looks for the Dockerfile
- Set a path to the files the build should use (the build context)
- Set up multiple static tags or branches to build from
- Use regular expressions (regexes) to dynamically select source code to build and
  create dynamic tags

All of these options are available from the **Build configuration** screen for
each repository. In [Docker Hub](https://hub.docker.com), select **My Hub** > **Repositories**, and select the name of the repository you want to edit. Select the **Builds** tab, and then select **Configure Automated builds**.

### Tag and branch builds

You can configure your automated builds so that pushes to specific branches or tags triggers a build.

1. In the **Build Rules** section, select the **plus** icon to add more sources to build.
2. Select the **Source type** to build either a tag or a branch.
  > Note
  >
  > This tells the build system what type of source to look for in the code
  > repository.
3. Enter the name of the **Source** branch or tag you want to build.
  > Note
  >
  > You can enter a name, or use a regex to match which source branch or tag
  > names to build. To learn more, see [regexes](https://docs.docker.com/docker-hub/repos/manage/builds/#regexes-and-automated-builds).
4. Enter the tag to apply to Docker images built from this source.
  > Note
  >
  > If you configured a regex to select the source, you can reference the
  > capture groups and use its result as part of the tag. To learn more, see
  > [regexes](https://docs.docker.com/docker-hub/repos/manage/builds/#regexes-and-automated-builds).
5. Repeat steps 2 through 4 for each new build rule you set up.

### Set the build context and Dockerfile location

Depending on how you arrange the files in your source code repository, the
files required to build your images may not be at the repository root. If that's
the case, you can specify a path where the build looks for the files.

The build context is the path to the files needed for the build, relative to
the root of the repository. Enter the path to these files in the **Build context** field. Enter `/` to set the build context as the root of the source code repository.

> Note
>
> If you delete the default path `/` from the **Build context** field and leave
> it blank, the build system uses the path to the Dockerfile as the build
> context. However, to avoid confusion it's recommended that you specify the
> complete path.

You can specify the **Dockerfile location** as a path relative to the build
context. If the Dockerfile is at the root of the build context path, leave the
Dockerfile path set to `/`. If the build context field is blank, set the path
to the Dockerfile from the root of the source repository.

### Regexes and automated builds

You can specify a regular expression (regex) so that only matching branches or
tags are built. You can also use the results of the regex to create the Docker
tag that's applied to the built image.

You can use up to nine regular expression capture groups, or expressions enclosed in parentheses, to select a source to build, and reference
these in the **Docker Tag** field using `{\1}` through `{\9}`.

### Build images with BuildKit

Autobuilds use the BuildKit build system by default. If you want to use the legacy
Docker build system, add the [environment variable](https://docs.docker.com/docker-hub/repos/manage/builds/#environment-variables-for-builds) `DOCKER_BUILDKIT=0`. Refer to the
[BuildKit](https://docs.docker.com/build/buildkit/)
page for more information on BuildKit.

## Autobuild for teams

When you create an automated build repository in your own user account, you
can start, cancel, and retry builds, and edit and delete your own repositories.

These same actions are also available for team repositories from Docker Hub if
you are an owner. If you are a member of a
team with `write` permissions you can start, cancel, and retry builds in your
team's repositories, but you cannot edit the team repository settings or delete
the team repositories. If your user account has `read` permission, or if you're
a member of a team with `read` permission, you can view the build configuration
including any testing settings.

| Action/Permission | Read | Write | Admin | Owner |
| --- | --- | --- | --- | --- |
| view build details | x | x | x | x |
| start, cancel, retry |  | x | x | x |
| edit build settings |  |  | x | x |
| delete build |  |  |  | x |

### Service users for team autobuilds

> Note
>
> Only owners can set up automated builds for teams.

When you set up automated builds for teams, you grant Docker Hub access to
your source code repositories using OAuth tied to a specific user account. This
means that Docker Hub has access to everything that the linked source provider
account can access.

For organizations and teams, it's recommended you create a dedicated service account to grant access to the source provider. This ensures that no
builds break as individual users' access permissions change, and that an
individual user's personal projects aren't exposed to an entire organization.

This service account should have access to any repositories to be built,
and must have administrative access to the source code repositories so it can
manage deploy keys. If needed, you can limit this account to only a specific
set of repositories required for a specific build.

If you are building repositories with linked private submodules (private
dependencies), you also need to add an override `SSH_PRIVATE` environment
variable to automated builds associated with the account. For more information, see [Troubleshoot](https://docs.docker.com/docker-hub/repos/manage/builds/troubleshoot/#build-repositories-with-linked-private-submodules)

1. Create a service user account on your source provider, and generate SSH keys for it.
2. Create a "build" team in your organization.
3. Ensure that the new "build" team has access to each repository and submodule you need to build.
  1. On GitHub or Bitbucket, go to the repository's **Settings** page.
  2. Add the new "build" team to the list of approved users.
    - GitHub: Add the team in **Collaborators and Teams**.
    - Bitbucket: Add the team in **Access management**.
4. Add the service user to the "build" team on the source provider.
5. Sign in to Docker Hub as an owner, switch to the organization, and follow the instructions to [link to source code repository](https://docs.docker.com/docker-hub/repos/manage/builds/link-source/) using the service account.
  > Note
  >
  > You may need to sign out of your individual account on the source code provider to create the link to the service account.
6. Optional. Use the SSH keys you generated to set up any builds with private submodules, using the service account and [the previous instructions](https://docs.docker.com/docker-hub/repos/manage/builds/troubleshoot/#build-repositories-with-linked-private-submodules).

## What's Next?

- [Customize your build process](https://docs.docker.com/docker-hub/repos/manage/builds/advanced/) with environment variables, hooks, and more
- [Add automated tests](https://docs.docker.com/docker-hub/repos/manage/builds/automated-testing/)
- [Manage your builds](https://docs.docker.com/docker-hub/repos/manage/builds/manage-builds/)
- [Troubleshoot](https://docs.docker.com/docker-hub/repos/manage/builds/troubleshoot/)

---

# Troubleshoot your autobuilds

> How to troubleshoot Automated builds

# Troubleshoot your autobuilds

   Table of contents

---

> Note
>
> Automated builds require a
> Docker Pro, Team, or Business subscription.

## Failing builds

If a build fails, a **Retry** icon appears next to the build report line on the
**General** and **Builds** tabs. The **Build report** page and **Timeline logs** also display a **Retry** button.

![Timeline view showing the retry build button](https://docs.docker.com/docker-hub/repos/manage/builds/images/retry-build.png)  ![Timeline view showing the retry build button](https://docs.docker.com/docker-hub/repos/manage/builds/images/retry-build.png)

> Note
>
> If you are viewing the build details for a repository that belongs to an
> organization, the **Cancel** and **Retry** buttons only appear if you have `Read & Write` access to the repository.

Automated builds have a 4-hour execution time limit. If a build reaches this time limit, it's
automatically cancelled, and the build logs display the following message:

```text
2022-11-02T17:42:27Z The build was cancelled or exceeded the maximum execution time.
```

This log message is the same as when you actively cancel a build. To identify
whether a build was automatically cancelled, check the build duration.

## Build repositories with linked private submodules

Docker Hub sets up a deploy key in your source code repository that allows it
to clone the repository and build it. This key only works for a single,
specific code repository. If your source code repository uses private Git
submodules, or requires that you clone other private repositories to build,
Docker Hub cannot access these additional repositories, your build cannot complete,
and an error is logged in your build timeline.

To work around this, you can set up your automated build using the `SSH_PRIVATE`
environment variable to override the deployment key and grant Docker Hub's build
system access to the repositories.

> Note
>
> If you are using autobuild for teams, use the process below
> instead, and configure a service user for your source code provider. You can
> also do this for an individual account to limit Docker Hub's access to your
> source repositories.

1. Generate a SSH keypair that you use for builds only, and add the public key to your source code provider account.
  This step is optional, but allows you to revoke the build-only keypair without removing other access.
2. Copy the private half of the keypair to your clipboard.
3. In Docker Hub, navigate to the build page for the repository that has linked private submodules. (If necessary, [follow the steps here](https://docs.docker.com/docker-hub/repos/manage/builds/#configure-automated-builds) to configure the automated build.)
4. At the bottom of the screen, select the **plus** icon next to **Build Environment variables**.
5. Enter `SSH_PRIVATE` as the name for the new environment variable.
6. Paste the private half of the keypair into the **Value** field.
7. Select **Save**, or **Save and Build** to validate that the build now completes.

> Note
>
> You must configure your private git submodules using git clone over SSH
> (`git@submodule.tld:some-submodule.git`) rather than HTTPS.

---

# Automated builds

> how automated builds work

# Automated builds

---

Subscription: Pro  Team  Business

Docker Hub can automatically build images from source code in an external
repository and automatically push the built image to your Docker repositories.

![An automated build dashboard](https://docs.docker.com/docker-hub/repos/manage/builds/images/index-dashboard.png)  ![An automated build dashboard](https://docs.docker.com/docker-hub/repos/manage/builds/images/index-dashboard.png)

When you set up automated builds, also called autobuilds, you create a list of
branches and tags that you want to build into Docker images. When you push code
to a source-code branch, for example in GitHub, for one of those listed image
tags, the push uses a webhook to trigger a new build, which produces a Docker
image. The built image is then pushed to Docker Hub.

> Note
>
> You can still use `docker push` to push pre-built images to
> repositories with automated builds configured.

If you have automated tests configured, these run after building, but before
pushing to the registry. You can use these tests to create a continuous
integration workflow where a build that fails its tests doesn't push the built
image. Automated tests don't push images to the registry on their own. [Learn about automated image testing](https://docs.docker.com/docker-hub/repos/manage/builds/automated-testing/).

Depending on your [subscription](https://www.docker.com/pricing),
you may get concurrent builds, which means that `N` autobuilds can be run at the
same time. `N` is configured according to your subscription. Once `N+1` builds
are running, any additional builds go into a queue to be run later.

The maximum number of pending builds in the queue is 30 and Docker Hub discards further
requests. The number of concurrent builds for Pro is 5 and
for Team and Business is 15.
Automated builds can handle images of up to 10 GB in size.

---

# Export organization repositories to CSV

> Learn how to export a complete list of your organization's Docker Hub repositories using the API.

# Export organization repositories to CSV

   Table of contents

---

This guide shows you how to export a complete list of repositories from your
Docker Hub organization, including private repositories. You'll use an
Organization Access Token (OAT) to authenticate with the Docker Hub API and
export repository details to a CSV file for reporting or analysis.

The exported data includes repository name, visibility status, last updated
date, pull count, and star count.

## Prerequisites

Before you begin, ensure you have:

- Administrator access to a Docker Hub organization
- `curl` installed for making API requests
- `jq` installed for JSON parsing
- A spreadsheet application to view the CSV

## Create an organization access token

Organization access tokens let you authenticate API requests without
interactive login steps.

1. Navigate to your organization in [Docker Home](https://app.docker.com) and select **Admin Console**.
2. Select **Access tokens** from the sidebar.
3. Select **Generate access token**.
4. Configure the token permissions:
  - Under **Repository permissions**, add every repository you want the
    token to access
  - Assign at least **Image Pull** (read) access to each repository
  - You can add up to 50 repositories per token
5. Copy the generated token and store it securely.

> Important
>
> If you only enable **Read public repositories**, the API will only return
> public repositories. To include private repositories in your export, you must
> explicitly add them to the token's repository permissions.

## Authenticate with the Docker Hub API

Exchange your organization access token for a JWT bearer token that you'll use
for subsequent API requests.

1. Set your organization name and access token as variables:
  ```bash
  ORG="<your-org>"
  OAT="<your_org_access_token>"
  ```
2. Call the authentication endpoint to get a JWT:
  ```bash
  TOKEN=$(
    curl -s https://hub.docker.com/v2/users/login \
      -H 'Content-Type: application/json' \
      -d "{\"username\":\"$ORG\",\"password\":\"$OAT\"}" \
    | jq -r '.token'
  )
  ```
3. Verify the token was retrieved successfully:
  ```console
  $ echo "Got JWT: ${#TOKEN} chars"
  ```

You'll use this JWT as a Bearer token in the `Authorization` header for all
subsequent API calls.

## Retrieve all repositories

The Docker Hub API paginates repository lists. This script retrieves all pages
and combines the results.

1. Set the page size and initial API endpoint:
  ```bash
  PAGE_SIZE=100
  URL="https://hub.docker.com/v2/namespaces/$ORG/repositories?page_size=$PAGE_SIZE"
  ```
2. Paginate through all results:
  ```bash
  ALL=$(
    while [ -n "$URL" ] && [ "$URL" != "null" ]; do
      RESP=$(curl -s "$URL" -H "Authorization: Bearer $TOKEN")
      echo "$RESP" | jq -c '.results[]'
      URL=$(echo "$RESP" | jq -r '.next')
    done | jq -s '.'
  )
  ```
3. Verify the number of repositories retrieved:
  ```console
  $ echo "$ALL" | jq 'length'
  ```

The script continues requesting the `next` URL from each response until
pagination is complete.

## Export to CSV

Generate a CSV file with repository details that you can open in
spreadsheet applications.

Run the following command to create `repos.csv`:

```bash
echo "$ALL" | jq -r '
  (["namespace","name","is_private","last_updated","pull_count","star_count"] | @csv),
  (.[] | [
    .namespace, .name, .is_private, .last_updated, (.pull_count//0), (.star_count//0)
  ] | @csv)
' > repos.csv
```

Verify the export completed:

```console
$ echo "Rows:" $(wc -l < repos.csv)
```

Open the `repos.csv` file in your preferred
spreadsheet application to view and analyze your repository data.

## Troubleshooting

### Only public repositories appear

Your organization access token may only have **Read public repositories**
enabled, or it lacks permissions for specific private repositories.

To fix this:

1. Navigate to your organization's access tokens in Docker Hub
2. Select the token you created
3. Add private repositories to the token's permissions with at
  least **Image Pull** access
4. Regenerate the JWT and retry the export

### API returns 403 or missing fields

Ensure you're using the JWT from the `/v2/users/login` endpoint as a
Bearer token in the `Authorization` header, not the organization access
token directly.

Verify your authentication:

```console
$ curl -s "https://hub.docker.com/v2/namespaces/$ORG/repositories?page_size=1" \
  -H "Authorization: Bearer $TOKEN" | jq
```

If this returns an error, re-run the authentication step to get a fresh JWT.

### Need access to all repositories

Organization access tokens are scoped to specific repositories you select
during token creation. To export all repositories, you have two options:

1. Add all repositories to the organization access token (up to 50 repositories)
2. Use a Personal Access Token (PAT) from an administrator account that has
  access across the entire organization

The choice between these approaches depends on your organization's security
policies.

---

# Bulk migrate images

> Learn how to migrate multiple Docker images and tags between organizations using scripts and automation.

# Bulk migrate images

   Table of contents

---

This guide shows you how to migrate Docker images in bulk between Docker Hub
organizations or namespaces. Whether you're consolidating repositories, changing
organization structure, or moving images to a new account, these techniques help
you migrate efficiently while preserving image integrity.

The topic is structured to build up in scale:

1. [Migrate a single image tag](#migrate-a-single-image-tag)
2. [Migrate all tags for a repository](#migrate-all-tags-for-a-repository)
3. [Migrate multiple repositories](#migrate-multiple-repositories)

The recommended tool for this workflow is `crane`. An equivalent alternative
using `regctl` is also shown. Both tools perform registry-to-registry copies
without pulling images locally and preserve multi-architecture images.

`crane` is recommended for its simplicity and focused image-copying workflow.
`regctl` is also a good choice, particularly if you already use it for broader
registry management tasks beyond image copying.

> Note
>
> The main workflows in this topic operate on tagged images only. Untagged
> manifests or content no longer reachable from tags are not migrated. In
> practice, these are usually unused artifacts, but be aware of this limitation
> before migration. While you can migrate specific untagged manifests using
> [digest references](#migrate-by-digest), there is no API to enumerate untagged
> manifests in a repository.

## Prerequisites

Before you begin, ensure you have:

- One of the following installed and available in your `$PATH`:
  - [crane](https://github.com/google/go-containerregistry)
  - [regctl](https://regclient.org/usage/regctl/)
- Push access to both the source and destination organizations
- Registry authentication configured for your chosen tool

## Authenticate to registries

Both tools authenticate directly against registries:

- `crane` uses Docker credential helpers and `~/.docker/config.json`. See the
  [crane documentation](https://github.com/google/go-containerregistry/tree/main/cmd/crane/doc).
- `regctl` uses its own configuration file and can import Docker credentials.
  See the [regctl documentation](https://github.com/regclient/regclient/tree/main/docs).

Follow the authentication instructions for your registry and tool of choice.

## Migrate a single image tag

This is the simplest and most common migration scenario.

The following example script copies the image manifest directly between
registries and preserves multi-architecture images when present. Repeat this
process for each tag you want to migrate. Replace the environment variable
values with your source and destination organization names, repository name, and
tag.

```bash
#!/usr/bin/env bash
set -euo pipefail

SRC_ORG="oldorg"
DEST_ORG="neworg"
REPO="myapp"
TAG="1.2.3"

SRC_IMAGE="${SRC_ORG}/${REPO}:${TAG}"
DEST_IMAGE="${DEST_ORG}/${REPO}:${TAG}"

# Using crane (recommended)
crane cp "${SRC_IMAGE}" "${DEST_IMAGE}"

# Using regctl (alternative)
# regctl image copy "${SRC_IMAGE}" "${DEST_IMAGE}"
```

### Migrate by digest

To migrate a specific image by digest instead of tag, use the digest in the
source reference. This is useful when you need to migrate an exact image
version, even if the tag has been updated. Replace the environment variable
values with your source and destination organization names, repository name,
digest, and tag. You can choose between `crane` and `regctl` for the copy
operation.

```bash
#!/usr/bin/env bash
set -euo pipefail

SRC_ORG="oldorg"
DEST_ORG="neworg"
REPO="myapp"
DIGEST="sha256:abcd1234..."
TAG="stable"

SRC_IMAGE="${SRC_ORG}/${REPO}@${DIGEST}"
DEST_IMAGE="${DEST_ORG}/${REPO}:${TAG}"

# Using crane
crane cp "${SRC_IMAGE}" "${DEST_IMAGE}"

# Using regctl
# regctl image copy "${SRC_IMAGE}" "${DEST_IMAGE}"
```

## Migrate all tags for a repository

To migrate every tagged image in a repository, use the Docker Hub API to
enumerate tags and copy each one. The following example script retrieves all
tags for a given repository and migrates them in a loop. This approach scales to
repositories with many tags without overwhelming local resources. Note that
there is a rate limit on Docker Hub requests, so you may need to add delays or
pagination handling for large repositories.

Replace the environment variable values with your source and destination
organization names and repository name. If your source repository is private,
also set `HUB_USER` and `HUB_TOKEN` with credentials that have pull access. You
can also choose between `crane` and `regctl` for the copy operation.

```bash
#!/usr/bin/env bash
set -euo pipefail

# Use environment variables if set, otherwise use defaults
SRC_ORG="${SRC_ORG:-oldorg}"
DEST_ORG="${DEST_ORG:-neworg}"
REPO="${REPO:-myapp}"

# Optional: for private repositories
# HUB_USER="your-username"
# HUB_TOKEN="your-access-token"
# AUTH="-u ${HUB_USER}:${HUB_TOKEN}"
AUTH=""

TOOL="crane"   # or: TOOL="regctl"

TAGS_URL="https://hub.docker.com/v2/repositories/${SRC_ORG}/${REPO}/tags?page_size=100"

while [[ -n "${TAGS_URL}" && "${TAGS_URL}" != "null" ]]; do
  RESP=$(curl -fsSL ${AUTH} "${TAGS_URL}")

  echo "${RESP}" | jq -r '.results[].name' | while read -r TAG; do
    [[ -z "${TAG}" ]] && continue

    SRC_IMAGE="${SRC_ORG}/${REPO}:${TAG}"
    DEST_IMAGE="${DEST_ORG}/${REPO}:${TAG}"

    echo "Migrating ${SRC_IMAGE} → ${DEST_IMAGE}"

    case "${TOOL}" in
      crane)
        crane cp "${SRC_IMAGE}" "${DEST_IMAGE}"
        ;;
      regctl)
        regctl image copy "${SRC_IMAGE}" "${DEST_IMAGE}"
        ;;
    esac
  done

  TAGS_URL=$(echo "${RESP}" | jq -r '.next')
done
```

> Note
>
> Docker Hub automatically creates the destination repository on first push if
> your account has permission.

## Migrate multiple repositories

To migrate several repositories, create a list and run the single-repository
script for each one.

For example, create a `repos.txt` file with repository names:

```text
api
web
worker
```

Save the script from the previous section as `migrate-single-repo.sh`. Then, run
the following example script that processes each repository in the file. Replace
the environment variable values with your source and destination organization
names.

```bash
#!/usr/bin/env bash
set -euo pipefail

SRC_ORG="oldorg"
DEST_ORG="neworg"

while read -r REPO; do
  [[ -z "${REPO}" ]] && continue
  echo "==== Migrating repo: ${REPO}"
  SRC_ORG="${SRC_ORG}" DEST_ORG="${DEST_ORG}" REPO="${REPO}" ./migrate-single-repo.sh
done < repos.txt
```

## Verify migration integrity

After copying, verify that source and destination match by comparing digests.

### Basic digest verification

The following example script retrieves the image digest for a specific tag from
both source and destination and compares them. If the digests match, the
migration is successful. Replace the environment variable values with your
source and destination organization names, repository name, and tag. You can
choose between `crane` and `regctl` for retrieving digests.

```bash
#!/usr/bin/env bash
set -euo pipefail

SRC_ORG="oldorg"
DEST_ORG="neworg"
REPO="myapp"
TAG="1.2.3"

SRC_IMAGE="${SRC_ORG}/${REPO}:${TAG}"
DEST_IMAGE="${DEST_ORG}/${REPO}:${TAG}"

# Using crane
SRC_DIGEST=$(crane digest "${SRC_IMAGE}")
DEST_DIGEST=$(crane digest "${DEST_IMAGE}")

# Using regctl (alternative)
# SRC_DIGEST=$(regctl image digest "${SRC_IMAGE}")
# DEST_DIGEST=$(regctl image digest "${DEST_IMAGE}")

echo "Source:      ${SRC_DIGEST}"
echo "Destination: ${DEST_DIGEST}"

if [[ "${SRC_DIGEST}" == "${DEST_DIGEST}" ]]; then
  echo "✓ Migration verified: digests match"
else
  echo "✗ Migration failed: digests do not match"
  exit 1
fi
```

### Multi-arch verification

For multi-architecture images, also verify the manifest list to ensure all
platforms were copied correctly. Replace the environment variable values with
your source and destination organization names, repository name, and tag. You
can choose between `crane` and `regctl` for retrieving manifests.

```bash
#!/usr/bin/env bash
set -euo pipefail

SRC_ORG="oldorg"
DEST_ORG="neworg"
REPO="myapp"
TAG="1.2.3"

SRC_IMAGE="${SRC_ORG}/${REPO}:${TAG}"
DEST_IMAGE="${DEST_ORG}/${REPO}:${TAG}"

# Using crane
SRC_MANIFEST=$(crane manifest "${SRC_IMAGE}")
DEST_MANIFEST=$(crane manifest "${DEST_IMAGE}")

# Using regctl (alternative)
# SRC_MANIFEST=$(regctl image manifest --format raw-body "${SRC_IMAGE}")
# DEST_MANIFEST=$(regctl image manifest --format raw-body "${DEST_IMAGE}")

# Check if it's a manifest list (multi-arch)
if echo "${SRC_MANIFEST}" | jq -e '.manifests' > /dev/null 2>&1; then
  echo "Multi-arch image detected"

  # Compare platform list
  SRC_PLATFORMS=$(echo "${SRC_MANIFEST}" | jq -r '.manifests[] | "\(.platform.os)/\(.platform.architecture)"' | sort)
  DEST_PLATFORMS=$(echo "${DEST_MANIFEST}" | jq -r '.manifests[] | "\(.platform.os)/\(.platform.architecture)"' | sort)

  if [[ "${SRC_PLATFORMS}" == "${DEST_PLATFORMS}" ]]; then
    echo "✓ Platform list matches:"
    echo "${SRC_PLATFORMS}"
  else
    echo "✗ Platform lists do not match"
    echo "Source platforms:"
    echo "${SRC_PLATFORMS}"
    echo "Destination platforms:"
    echo "${DEST_PLATFORMS}"
    exit 1
  fi
else
  echo "Single-arch image"
fi
```

## Complete the migration

After migrating your images, complete these additional steps:

1. Copy repository metadata in the Docker Hub UI or via API:
  - README content
  - Repository description
  - Topics and tags
2. Configure repository settings to match the source:
  - Visibility (public or private)
  - Team permissions and access controls
3. Reconfigure integrations in the destination organization:
  - Webhooks
  - Automated builds
  - Security scanners
4. Update image references in your projects:
  - Change `FROM oldorg/repo:tag` to `FROM neworg/repo:tag` in Dockerfiles
  - Update deployment configurations
  - Update documentation
5. Deprecate the old location:
  - Update the source repository description to point to the new location
  - Consider adding a grace period before making the old repository private or
    read-only

---

# Immutable tags on Docker Hub

> Learn about immutable tags and how they help maintain image version consistency on Docker Hub.

# Immutable tags on Docker Hub

   Table of contents

---

Availability: Beta

Immutable tags provide a way to ensure that specific image versions remain unchanged once they are published to Docker Hub. This feature helps maintain consistency and reliability in your container deployments by preventing accidental overwrites of important image versions.

## What are immutable tags?

Immutable tags are image tags that, once pushed to Docker Hub, cannot be overwritten or deleted. This ensures that a specific version of an image remains exactly the same throughout its lifecycle, providing:

- Version consistency
- Reproducible builds
- Protection against accidental overwrites
- Better security and compliance

## Enable immutable tags

To enable immutable tags for your repository:

1. Sign in to [Docker Hub](https://hub.docker.com).
2. Select **My Hub** > **Repositories**.
3. Select the repository where you want to enable immutable tags.
4. Go to **Settings** > **General**.
5. Under **Tag mutability settings**, select one of the following options:
  - **All tags are mutable (Default)**:
    Tags can be changed to reference a different image. This lets you retarget a tag without creating a new one.
  - **All tags are immutable**:
    Tags cannot be updated to point to a different image after creation. This ensures consistency and prevents accidental changes. This includes the `latest` tag.
  - **Specific tags are immutable**:
    Define specific tags that cannot be updated after creation using regex values.
6. Select **Save**.

Once enabled, all tags are locked to their specific images, ensuring that each tag always points to the same image version and cannot be modified.

> Note
>
> This implementation of regular expressions follows the [Go regexp package](https://pkg.go.dev/regexp), which is based on the RE2 engine. For more information, visit [RE2 Regular Expression Syntax](https://github.com/google/re2/wiki/Syntax).

## Working with immutable tags

When immutable tags are enabled:

- You cannot push a new image with the same tag name
- You must use a new tag name for each new image version

To push an image, create a new tag for your updated image and push it to the repository.

---

# Image Management

> Discover how to delete image tags.

# Image Management

   Table of contents

---

Availability: Beta

Images and image indexes are the foundation of container images within a
repository. The following diagram shows the relationship between images and
image indexes.

![a pretty wide image](https://docs.docker.com/docker-hub/repos/manage/hub-images/images/image-index.svg)  ![a pretty wide image](https://docs.docker.com/docker-hub/repos/manage/hub-images/images/image-index.svg)

This structure enables multi-architecture support through a single reference. It
is important to note that images are not always referenced by an image index.
The following objects are shown in the diagram.

- Image index: An image that points to multiple architecture-specific images
  (like AMD and ARM), letting a single reference work across different
  platforms.
- Image: Individual container images that contain the actual configuration and
  layers for a specific architecture and operating system.

## Manage repository images and image indexes

1. Sign in to [Docker Hub](https://hub.docker.com).
2. Select **My Hub** > **Repositories**.
3. In the list, select a repository.
4. Select **Image Management**.
5. Search, filter, or sort the items.
  - Search: In the search box above the list, specify your search.
  - Filter: In the **Filter by** drop-down, select **Tagged**, **Image index**,
    or **Image**.
  - Sort: Select the column title for **Size**, **Last pushed**, or **Last
    pulled**.
  > Note
  >
  > Images that haven't been pulled in over 6 months are marked as **Stale** in
  > the **Status** column.
6. Optional. Delete one or more items.
  1. Select the checkboxes next to the items in the list. Selecting any
    top-level index also removes any underlying images that aren't referenced
    elsewhere.
  2. Select **Preview and delete**.
  3. In the window that appears, verify the items that will be deleted and the
    amount of storage you will reclaim.
  4. Select **Delete forever**.
  > Note
  >
  > If you would like to delete in bulk, you can use the
  > [deletion API endpoint](https://docs.docker.com/reference/api/registry/latest/#tag/delete).

---

# Move images between repositories

> Discover how to move images between repositories.

# Move images between repositories

   Table of contents

---

Consolidating and organizing your Docker images across repositories can
streamline your workflows, whether you're managing personal projects or
contributing to an organization. This topic explains how to move images between
Docker Hub repositories, ensuring that your content remains accessible and
organized under the correct accounts or namespaces.

> Note
>
> For bulk migrations, multi-arch images, or scripted workflows, see
> [Bulk
> migrate Docker images](https://docs.docker.com/docker-hub/repos/manage/hub-images/bulk-migrate/).

## Personal to personal

When consolidating personal repositories, you can pull private images from the initial repository and push them into another repository owned by you. To avoid losing your private images, perform the following steps:

1. [Sign up](https://app.docker.com/signup) for a new Docker account with a personal subscription. (Be sure to verify your account after you've signed up.)
2. Sign in to [Docker](https://app.docker.com/login) using your original Docker account
3. Pull your images:
  ```console
  $ docker pull namespace1/docker101tutorial
  ```
4. Tag your private images with your newly created Docker username, for example:
  ```console
  $ docker tag namespace1/docker101tutorial new_namespace/docker101tutorial
  ```
5. Using `docker login` from the CLI, sign in with your newly created Docker account, and push your newly tagged private images to your new Docker account namespace:
  ```console
  $ docker push new_namespace/docker101tutorial
  ```

The private images that existed in your previous account are now available in your new account.

## Personal to an organization

To avoid losing your private images, you can pull your private images from your
personal account and push them to an organization that's owned by you.

1. Navigate to [Docker Hub](https://hub.docker.com) and select **My Hub**.
2. Select the applicable organization and verify that your user account is a member of the organization.
3. Sign in to [Docker Hub](https://hub.docker.com) using your original Docker account, and pull your images:
  ```console
  $ docker pull namespace1/docker101tutorial
  ```
4. Tag your images with your new organization namespace:
  ```console
  $ docker tag namespace1/docker101tutorial <new_org>/docker101tutorial
  ```
5. Push your newly tagged images to your new org namespace:
  ```console
  $ docker push new_org/docker101tutorial
  ```

The private images that existed in your user account are now available for your organization.
