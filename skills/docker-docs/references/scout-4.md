# Integrate Docker Scout with Artifactory Container Registry and more

# Integrate Docker Scout with Artifactory Container Registry

> Integrate Artifactory Container Registry with Docker Scout

# Integrate Docker Scout with Artifactory Container Registry

   Table of contents

---

**Experimental**

The `docker scout watch` command is experimental.

Experimental features are intended for testing and feedback as their
functionality or design may change between releases without warning or
can be removed entirely in a future release.

Integrating Docker Scout with JFrog Artifactory lets you index and analyze
images from Artifactory. This integration is powered by a long-running
`docker scout watch` process. It pulls images from your selected repositories
(optionally filtered), can receive webhook callbacks from Artifactory, and
pushes image data to Docker Scout. View results in the Docker Scout Dashboard or
with `docker scout` CLI.

## How it works

You run
[docker scout watch](https://docs.docker.com/reference/cli/docker/scout/watch/) on a host you
control and configure the Artifactory-specific registry string via `--registry "key=value,..."`. The watch process can:

- Watch specific repositories or an entire registry
- Optionally ingest all existing images once
- Periodically refresh repository lists
- Receive webhook callbacks from Artifactory on a local port you choose

After the integration, Docker Scout automatically pulls and analyzes images
that you push to the Artifactory registry. Metadata about your images are stored on the
Docker Scout platform, but Docker Scout doesn't store the container images
themselves. For more information about how Docker Scout handles image data, see
[Data handling](https://docs.docker.com/scout/deep-dive/data-handling/).

### Artifactory-specific registry string options

These `type=artifactory` options override the generic registry handling for the `--registry` option:

| Key | Required | Description |
| --- | --- | --- |
| type | Yes | Must beartifactory. |
| registry | Yes | Docker/OCI registry hostname (e.g.,example.jfrog.io). |
| api | Yes | Artifactory REST API base URL (e.g.,https://example.jfrog.io/artifactory). |
| repository | Yes | Repository to watch (replaces--repository). |
| includes | No | Globs to include (e.g.,*/frontend*). |
| excludes | No | Globs to exclude (e.g.,*/legacy/*). |
| port | No | Local port to listen on for webhook callbacks. |
| subdomain-mode | No | trueorfalse; matches Artifactory’s Docker layout (subdomain versus repository-path). |

## Integrate an Artifactory registry

Use the following steps to integrate your Artifactory registry with Docker
Scout.

1. Pick the host on which to run `docker scout watch`.
  The host must have local or network access to your private registry and be able
  to access the Scout API (`https://api.scout.docker.com`) over the internet. If
  you're using webhook callbacks, Artifactory must also be able to reach the Scout
  client host on the configured port.
  Override the `--workers` option (default: `3`) for optimal performance based on
  the size of the host and the expected workload.
2. Ensure you are running the latest version of Scout.
  Check your current version:
  ```console
  $ docker scout version
  ```
  If necessary, [install the latest version of Scout](https://docs.docker.com/scout/install/).
3. Set up your Artifactory credentials.
  Store the credentials that the Scout client will use to authenticate with
  Artifactory. The following is an example using environment variables. Replace
  `<user>` and `<password-or-access-token>` with your actual values.
  ```console
  $ export DOCKER_SCOUT_ARTIFACTORY_API_USER=<user>
  $ export DOCKER_SCOUT_ARTIFACTORY_API_PASSWORD=<password-or-access-token>
  ```
  > Tip
  >
  > As a best practice, create a dedicated user with read-only access and use
  > an access token instead of a password.
  Store the credential that Artifactory will use to authenticate webhook
  callbacks. The following is an example using an environment variable. Replace
  `<random-64-128-character-secret>` with an actual secret.
  ```console
  $ export DOCKER_SCOUT_ARTIFACTORY_WEBHOOK_SECRET=<random-64-128-character-secret>
  ```
  > Tip
  >
  > As a best practice, generate a high-entropy random string of 64-128 characters.
4. Set up your Scout credentials.
  1. Generate an organization access token for accessing Scout. For more
    details, see
    [Create an organization access
    token](https://docs.docker.com/enterprise/security/access-tokens/#create-an-organization-access-token).
  2. Sign in to Docker using the organization access token.
    ```console
    $ docker login --username <your_organization_name>
    ```
    When prompted for a password, paste the organization access token you
    generated.
  3. Connect your local Docker environment to your organization's Docker Scout service.
    ```console
    $ docker scout enroll <your_organization_name>
    ```
5. Index existing images. You only need to do this once.
  Run `docker scout watch` with the `--all-images` option to index all images in the specified Artifactory repository. The following is an example command:
  ```console
  $ docker scout watch --registry \
  "type=artifactory,registry=example.jfrog.io,api=https://example.jfrog.io/artifactory,include=*/frontend*,exclude=*/dta/*,repository=docker-local,port=9000,subdomain-mode=true" \
  --all-images
  ```
6. Confirm the images have been indexed by viewing them on the [Scout
  Dashboard](https://scout.docker.com/).
7. Configure Artifactory callbacks.
  In your Artifactory UI or via REST API, configure webhooks for image
  push/update events. Set the endpoint to your `docker scout watch` host and
  port, and include the `DOCKER_SCOUT_ARTIFACTORY_WEBHOOK_SECRET` for
  authentication.
  For more information, see the [JFrog Artifactory Webhooks
  documentation](https://jfrog.com/help/r/jfrog-platform-administration-documentation/webhooks)
  or the [JFrog Artifactory REST API Webhooks
  documentation](https://jfrog.com/help/r/jfrog-rest-apis/webhooks).
8. Continuously watch for new or updated images.
  Run `docker scout watch` with the `--refresh-registry` option to watch for
  new images to index. The following is an example command:
  ```console
  $ docker scout watch --registry \
  "type=artifactory,registry=example.jfrog.io,api=https://example.jfrog.io/artifactory,include=*/frontend*,exclude=*/dta/*,repository=docker-local,port=9000,subdomain-mode=true" \
  --refresh-registry
  ```
9. Optional. Set up Scout integration for real-time notifications from popular
  collaboration platforms. For details, see [Integrate Docker Scout with
  Slack](https://docs.docker.com/scout/integrations/team-collaboration/slack/).

---

# Integrate Docker Scout with Amazon ECR

> Integrate Amazon Elastic Container Registry with Docker Scout

# Integrate Docker Scout with Amazon ECR

   Table of contents

---

Integrating Docker Scout with Amazon Elastic Container Registry (ECR) lets you
view image insights for images hosted in ECR repositories. After integrating
Docker Scout with ECR and activating Docker Scout for a repository, pushing an
image to the repository automatically triggers image analysis. You can view
image insights using the Docker Scout Dashboard, or the `docker scout` CLI
commands.

## How it works

To help you integrate Docker Scout with ECR, you can use a CloudFormation stack
template that creates and configures the necessary AWS resources for
integrating Docker Scout with your ECR registry. For more details about the AWS
resources, see [CloudFormation stack template](#cloudformation-stack-template).

The following diagram shows how the Docker Scout ECR integration works.

![How the ECR integration works](https://docs.docker.com/scout/images/Scout-ECR.png)  ![How the ECR integration works](https://docs.docker.com/scout/images/Scout-ECR.png)

After the integration, Docker Scout automatically pulls and analyzes images
that you push to the ECR registry. Metadata about your images are stored on the
Docker Scout platform, but Docker Scout doesn't store the container images
themselves. For more information about how Docker Scout handles image data, see
[Data handling](https://docs.docker.com/scout/deep-dive/data-handling/).

### CloudFormation stack template

The following table describes the configuration resources.

> Note
>
> Creating these resources incurs a small, recurring cost on the AWS account.
> The **Cost** column in the table represents an estimated monthly cost of the
> resources, when integrating an ECR registry that gets 100 images pushed per day.
>
>
>
> Additionally, an egress cost also applies when Docker Scout pulls the images
> from ECR. The egress cost is around $0.09 per GB.

| Resource type | Resource name | Description | Cost |
| --- | --- | --- | --- |
| AWS::SNSTopic::Topic | SNSTopic | SNS topic for notifying Docker Scout when the AWS resources have been created. | Free |
| AWS::SNS::TopicPolicy | TopicPolicy | Defines the topic for the initial setup notification. | Free |
| AWS::SecretsManager::Secret | ScoutAPICredentials | Stores the credentials used by EventBridge to fire events to Scout. | $0.42 |
| AWS::Events::ApiDestination | ApiDestination | Sets up the EventBridge connection to Docker Scout for sending ECR push and delete events. | $0.01 |
| AWS::Events::Connection | Connection | EventBridge connection credentials to Scout. | Free |
| AWS::Events::Rule | DockerScoutEcrRule | Defines the rule to send ECR pushes and deletes to Scout. | Free |
| AWS::Events::Rule | DockerScoutRepoDeletedRule | Defines the rule to send ECR repository deletes to Scout. | Free |
| AWS::IAM::Role | InvokeApiRole | Internal role to grant the event access toApiDestination. | Free |
| AWS::IAM::Role | AssumeRoleEcrAccess | This role has access toScoutAPICredentialsfor setting up the Docker Scout integration. | Free |

## Integrate your first registry

Create the CloudFormation stack in your AWS account to enable the Docker Scout
integration.

Prerequisites:

- You must have access to an AWS account with permission to create resources.
- You have be an owner of the Docker organization.

To create the stack:

1. Go to the [ECR integration page](https://scout.docker.com/settings/integrations/ecr/)
  on the Docker Scout Dashboard.
2. Select the **Create on AWS** button.
  This opens the **Create stack** wizard in the AWS CloudFormation console in
  a new browser tab. If you're not already signed in to AWS, you're redirected
  to the sign-in page first.
  If the button is grayed-out, it means you're lacking the necessary
  permissions in the Docker organization.
3. Follow the steps in the **Create stack** wizard until the end. Choose the
  AWS region you want to integrate. Complete the procedure by creating the
  resources.
  The fields in the wizard are pre-populated by the CloudFormation template,
  so you don't need to edit any of the fields.
4. When the resources have been created (the CloudFormation status shows
  `CREATE_COMPLETE` in the AWS console), return to the ECR integrations page
  in the Docker Scout Dashboard.
  The **Integrated registries** list shows the account ID and region for the
  ECR registry that you just integrated. If successful, the integration status
  is **Connected**.

The ECR integration is now active. For Docker Scout to start analyzing images
in the registry, you need to activate it for each repository in
[Repository settings](https://scout.docker.com/settings/repos/).

After activating repositories, images that you push are analyzed by Docker
Scout. The analysis results appear in the Docker Scout Dashboard.
If your repository already contains images, Docker Scout pulls and analyzes the
latest image version automatically.

## Integrate additional registries

To add additional registries:

1. Go to the [ECR integration page](https://scout.docker.com/settings/integrations/ecr/)
  on the Docker Scout Dashboard.
2. Select the **Add** button at the top of the list.
3. Complete the steps for creating the AWS resources.
4. When the resources have been created, return to the ECR integrations page in
  the Docker Scout Dashboard.
  The **Integrated registries** list shows the account ID and region for the
  ECR registry that you just integrated. If successful, the integration status
  is **Connected**.

Next, activate Docker Scout for the repositories that you want to analyze in
[Repository settings](https://scout.docker.com/settings/repos/).

## Remove integration

To remove an integrated ECR registry, you must be an owner of the Docker
organization.

1. Go to the [ECR integration page](https://scout.docker.com/settings/integrations/ecr/)
  on the Docker Scout Dashboard.
2. Find the registry that you want to remove in the list of integrated
  registries, and select the remove icon in the **Actions** column.
  If the remove icon is disabled, it means that you're lacking the necessary
  permissions in the Docker organization.
3. In the dialog that opens, confirm by selecting **Remove**.

> Important
>
> Removing the integration from the Docker Scout dashboard doesn't remove the
> AWS resources in your account.
>
>
>
> After removing the integration in Docker Scout, go to the AWS console and
> delete the **DockerScoutECRIntegration** CloudFormation stack for the integration
> that you want to remove.

## Troubleshooting

### Unable to integrate registry

Check the **Status** of the integration on the [ECR integration page](https://scout.docker.com/settings/integrations/ecr/)
in the Docker Scout Dashboard.

- If the status is **Pending** for a prolonged period of time, it's an
  indication that the integration was not yet completed on the AWS side. Select
  the **Pending** link to open the CloudFormation wizard, and complete all the
  steps.
- An **Error** status indicates that something's gone wrong in the back-end.
  You can try [removing the integration](#remove-integration) and recreating it
  again.

### ECR images not showing in the dashboard

If image analysis results for your ECR images aren't showing up in the Docker
Scout Dashboard:

- Ensure that you've activated Docker Scout for the repository. View and manage
  active repositories in [Repository settings](https://scout.docker.com/settings/repos/).
- Ensure that the AWS account ID and region for your registry is listed on the
  ECR integrations page.
  The account ID and region are included in the registry hostname:
  `<aws_account_id>.dkr.ecr.<region>.amazonaws.com/<image>`

---

# Integrate Docker Scout with GitHub

> Integrate Docker Scout using the GitHub app to get remediation advice directly in your repositories

# Integrate Docker Scout with GitHub

   Table of contents

---

Availability: Beta

The GitHub app integration for Docker Scout grants Docker Scout access to your
source code repository on GitHub. This improved visibility into how your image
gets created means Docker Scout can give you automated and contextual
remediation advice.

## How it works

When you enable the GitHub integration, Docker Scout can make a direct link
between the image analysis results and the source.

When analyzing your image, Docker Scout checks for
[provenance
attestations](https://docs.docker.com/build/metadata/attestations/slsa-provenance/) to detect the
location of the source code repository for the image. If the source location is
found, and you've enabled the GitHub app, Docker Scout parses the Dockerfile
used to create the image.

Parsing the Dockerfile reveals the base image tag used to build the image. By
knowing the base image tags used, Docker Scout can detect whether the tag is
outdated, meaning it's been changed to a different image digest. For example,
say you're using `alpine:3.18` as your base image, and at a later point in
time, the image maintainers release a patch version for version `3.18`,
containing security fixes. The `alpine:3.18` tag you've been using becomes
out-of-date; the `alpine:3.18` you're using is no longer the latest.

When this happens, Docker Scout detects the discrepancy and surfaces it through
the
[Up-to-Date Base Images policy](https://docs.docker.com/scout/policy/#up-to-date-base-images-policy).
When the GitHub integration's enabled, you'll also get automated suggestions on
how to update your base image. For more information about how Docker Scout can
help you automatically improve your supply chain conduct and security posture,
see [Remediation](https://docs.docker.com/scout/policy/remediation/).

## Setup

To integrate Docker Scout with your GitHub organization:

1. Go to [GitHub integration](https://scout.docker.com/settings/integrations/github/)
  on the Docker Scout Dashboard.
2. Select the **Integrate GitHub app** button to open GitHub.
3. Select the organization that you want to integrate.
4. Select whether you want to integrate all repositories in the GitHub
  organization or a manual selection of repositories.
5. Select **Install & Authorize** to add the Docker Scout app to the
  organization.
  This redirects you back to the Docker Scout Dashboard, which lists your
  active GitHub integrations.

The GitHub integration is now active.

---

# Integrate Docker Scout with Slack

> Integrate Docker Scout with Slack to receive real-time updates about vulnerabilities and policy compliance in Slack channels

# Integrate Docker Scout with Slack

   Table of contents

---

You can integrate Docker Scout with Slack by creating a Slack webhook and
adding it to the Docker Scout Dashboard. Docker Scout will notify you about
when a new vulnerability is disclosed, and it affects one or more of your
images.

![Slack notification from Docker Scout](https://docs.docker.com/scout/images/scout-slack-notification.png)Example Slack notification from Docker Scout ![Slack notification from Docker Scout](https://docs.docker.com/scout/images/scout-slack-notification.png)

## How it works

After configuring the integration, Docker Scout sends notifications about
changes to policy compliance and vulnerability exposure for your repositories,
to the Slack channels associated with the webhook.

> Note
>
> Notifications are only triggered for the *last pushed* image tags for each
> repository. "Last pushed" refers to the image tag that was most recently
> pushed to the registry and analyzed by Docker Scout. If the last pushed image
> is not by a newly disclosed CVE, then no notification will be triggered.

For more information about Docker Scout notifications,
see
[Notification settings](https://docs.docker.com/scout/explore/dashboard/#notification-settings)

## Setup

To add a Slack integration:

1. Create a webhook, see [Slack documentation](https://api.slack.com/messaging/webhooks).
2. Go to the [Slack integration page](https://scout.docker.com/settings/integrations/slack/) in the Docker Scout Dashboard.
3. In the **How to integrate** section, enter a **Configuration name**.
  Docker Scout uses this label as a display name for the integration,
  so you might want to change the default name into something more meaningful.
  For example the `#channel-name`, or the name of the team that this configuration belongs to.
4. Paste the webhook you just created in the **Slack webhook** field.
  Select the **Test webhook** button if you wish to verify the connection.
  Docker Scout will send a test message to the specified webhook.
5. Select whether you want to enable notifications for all your Scout-enabled image repositories,
  or enter the names of the repositories that you want to send notifications for.
6. When you're ready to enable the integration, select **Create**.

After creating the webhook, Docker Scout begins to send notifications updates
to the Slack channels associated with the webhook.

## Remove a Slack integration

To remove a Slack integration:

1. Go to the [Slack integration page](https://scout.docker.com/settings/integrations/slack/) in the Docker Scout Dashboard.
2. Select the **Remove** icon for the integration that you want to remove.
3. Confirm by selecting **Remove** again in the confirmation dialog.

---

# Integrating Docker Scout with other systems

> How to setup Docker Scout with other systems.

# Integrating Docker Scout with other systems

   Table of contents

---

By default, Docker Scout integrates with your Docker organization and your
Docker Scout-enabled repositories on Docker Hub. You can integrate Docker Scout
with additional third-party systems to get access to even more insights,
including real-time information about you running workloads.

## Integration categories

You'll get different insights depending on where and how you choose to integrate
Docker Scout.

### Container registries

Integrating Docker Scout with third-party container
registries enables Docker Scout to run image analysis on those repositories,
so that you can get insights into the composition of those images even if they
aren't hosted on Docker Hub.

The following container registry integrations are available:

- [Amazon Elastic Container Registry](https://docs.docker.com/scout/integrations/registry/ecr/)
- [Azure Container Registry](https://docs.docker.com/scout/integrations/registry/acr/)
- [JFrog Artifactory](https://docs.docker.com/scout/integrations/registry/artifactory/)

### Continuous Integration

Integrating Docker Scout with Continuous Integration (CI) systems is a great way
to get instant, automatic feedback about your security posture in your inner
loop. Analysis running in CI also gets the benefit of additional context that's
useful for getting even more insights.

The following CI integrations are available:

- [GitHub Actions](https://docs.docker.com/scout/integrations/ci/gha/)
- [GitLab](https://docs.docker.com/scout/integrations/ci/gitlab/)
- [Microsoft Azure DevOps Pipelines](https://docs.docker.com/scout/integrations/ci/azure/)
- [Circle CI](https://docs.docker.com/scout/integrations/ci/circle-ci/)
- [Jenkins](https://docs.docker.com/scout/integrations/ci/jenkins/)

### Environment monitoring

Environment monitoring refers to integrating Docker Scout with your deployments.
This can give you information in real-time about your running container workloads.

Integrating with environments lets you compare production workloads to other
versions, in your image repositories or in your other environments.

The following environment monitoring integrations are available

- [Sysdig](https://docs.docker.com/scout/integrations/environment/sysdig/)

For more information about environment integrations, see
[Environments](https://docs.docker.com/scout/integrations/environment/).

### Code quality

Integrating Docker Scout with code analysis tools enables quality checks
directly on source code, helping you keep track of bugs, security issues, test
coverage, and more. In addition to image analysis and environment monitoring,
code quality gates let you shift left your supply chain management with Docker
Scout.

Once you enable a code quality integration, Docker Scout includes the code
quality assessments as policy evaluation results for the repositories where
you've enabled the integration.

The following code quality integrations are available:

- [SonarQube](https://docs.docker.com/scout/integrations/code-quality/sonarqube/)

### Source code management

Integrate Docker Scout with your version control system to get guided
remediation advice on how to address issues detected by Docker Scout image
analysis, directly in your repositories.

The following source code management integrations are available:

- [GitHub](https://docs.docker.com/scout/integrations/source-code-management/github/) Beta

### Team collaboration

Integrations in this category let you integrate Docker Scout with collaboration
platforms for broadcasting notifications about your software supply chain in
real-time to team communication platforms.

The following team collaboration integrations are available:

- [Slack](https://docs.docker.com/scout/integrations/team-collaboration/slack/)

---

# Evaluate policy compliance in CI

> Configure your continuous integration pipelines to fail when Policy Evaluation for an image is worse compared to baseline

# Evaluate policy compliance in CI

   Table of contents

---

Adding Policy Evaluation to your continuous integration pipelines helps you
detect and prevent cases where code changes would cause policy compliance to
become worse compared to your baseline.

The recommended strategy for Policy Evaluation in a CI setting involves
evaluating a local image and comparing the results to a baseline. If the policy
compliance for the local image is worse than the specified baseline, the CI run
fails with an error. If policy compliance is better or unchanged, the CI run
succeeds.

This comparison is relative, meaning that it's only concerned with whether your
CI image is better or worse than your baseline. It's not an absolute check to
pass or fail all policies. By measuring relative to a baseline that you define,
you can quickly see if a change has a positive or negative impact on policy
compliance.

## How it works

When you do Policy Evaluation in CI, you run a local policy evaluation on the
image you build in your CI pipeline. To run a local evaluation, the image that
you evaluate must exist in the image store where your CI workflow is being run.
Either build or pull the image, and then run the evaluation.

To run policy evaluation and trigger failure if compliance for your local image
is worse than your comparison baseline, you need to specify the image version
to use as a baseline. You can hard-code a specific image reference, but a
better solution is to use [environments](https://docs.docker.com/scout/integrations/environment/)
to automatically infer the image version from an environment. The example that
follows uses environments to compare the CI image with the image in the
`production` environment.

## Example

The following example on how to run policy evaluation in CI uses the [Docker
Scout GitHub Action](https://github.com/marketplace/actions/docker-scout) to
execute the `compare` command on an image built in CI. The compare command has
a `to-env` input, which will run the comparison against an environment called
`production`. The `exit-on` input is set to `policy`, meaning that the
comparison fails only if policy compliance has worsened.

This example doesn't assume that you're using Docker Hub as your container
registry. As a result, this workflow uses the `docker/login-action` twice:

- Once for authenticating to your container registry.
- Once more for authenticating to Docker to pull the analysis results of your
  `production` image.

If you use Docker Hub as your container registry, you only need to authenticate
once.

> Note
>
> Due to a limitation in the Docker Engine, loading multi-platform images or
> images with attestations to the image store isn't supported.
>
>
>
> For the policy evaluation to work, you must load the image to the local image
> store of the runner. Ensure that you're building a single-platform image
> without attestations, and that you're loading the build results. Otherwise,
> the policy evaluation fails.

Also note the `pull-requests: write` permission for the job. The Docker Scout
GitHub Action adds a pull request comment with the evaluation results by
default, which requires this permission. For details, see
[Pull Request Comments](https://github.com/docker/scout-action#pull-request-comments).

```yaml
name: Docker

on:
  push:
    tags: ["*"]
    branches:
      - "main"
  pull_request:
    branches: ["**"]

env:
  REGISTRY: docker.io
  IMAGE_NAME: IMAGE_NAME
  DOCKER_ORG: ORG

jobs:
  build:
    permissions:
      pull-requests: write

    runs-on: ubuntu-latest
    steps:
      - name: Log into registry ${{ env.REGISTRY }}
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ secrets.REGISTRY_USER }}
          password: ${{ secrets.REGISTRY_TOKEN }}

      - name: Setup Docker buildx
        uses: docker/setup-buildx-action@v3

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.IMAGE_NAME }}

      - name: Build image
        id: build-and-push
        uses: docker/build-push-action@v4
        with:
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          sbom: ${{ github.event_name != 'pull_request' }}
          provenance: ${{ github.event_name != 'pull_request' }}
          push: ${{ github.event_name != 'pull_request' }}
          load: ${{ github.event_name == 'pull_request' }}

      - name: Authenticate with Docker
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USER }}
          password: ${{ secrets.DOCKER_PAT }}

      - name: Compare
        if: ${{ github.event_name == 'pull_request' }}
        uses: docker/scout-action@v1
        with:
          command: compare
          image: ${{ steps.meta.outputs.tags }}
          to-env: production
          platform: "linux/amd64"
          ignore-unchanged: true
          only-severities: critical,high
          organization: ${{ env.DOCKER_ORG }}
          exit-on: policy
```

The following screenshot shows what the GitHub PR comment looks like when a
policy evaluation check fails because policy has become worse in the PR image
compared to baseline.

![Policy evaluation comment in GitHub PR](https://docs.docker.com/scout/images/scout-policy-eval-ci.webp)  ![Policy evaluation comment in GitHub PR](https://docs.docker.com/scout/images/scout-policy-eval-ci.webp)

This example has demonstrated how to run policy evaluation in CI with GitHub
Actions. Docker Scout also supports other CI platforms. For more information,
see [Docker Scout CI
integrations](https://docs.docker.com/scout/integrations/#continuous-integration).

---

# Configure policies

> Learn how to configure, disable, or delete policies in Docker Scout

# Configure policies

   Table of contents

---

Some policy types are configurable. This means that you can create new,
customized version of that policy type with your own configuration parameters.
You can also disable a policy if you need to temporarily disregard it, or
delete a policy altogether if it doesn't match your needs.

> Note
>
> Historic evaluation results for the default policy configuration are removed
> if you delete or customize a policy.

## Add a policy

To add a new policy, select the policy type that you want to customize. All
custom policies use a policy type as a base.

You can edit the display name and description of the new policy to help
better communicate the compliant and non-compliant states of the policy.
You can not change the name of the policy type, only its display names.

The available configuration parameters for a policy depends on the
policy type that you're editing. For more information, refer to
[Policy types](https://docs.docker.com/scout/policy/#policy-types).

To add a policy:

1. Go to the [Policies page](https://scout.docker.com/reports/policy) in the Docker Scout Dashboard.
2. Select the **Add policy** button to open the policy configuration screen.
3. On the policy configuration screen, locate the policy type that you want to
  configure, and select **Configure** to open the policy configuration page.
  - If the **Configure** button is grayed out, it means the current policy
    has no configurable parameters.
  - If the button reads **Integrate**, it indicates that setup is required
    before the policy can be enabled. Selecting **Integrate** will direct you
    to the integration's setup guide.
4. Update the policy parameters.
5. Save the changes:
  - Select **Save policy** to commit the changes and enable the policy for
    your current organization.
  - Select **Save and disable** to save the policy configuration without enabling
    it.

## Edit a policy

Editing a policy lets you to modify its configuration without creating
a new one from scratch. This can be useful when policy parameters need adjustments
due to evolving requirements or changes in your organization's compliance goals.

To edit a policy:

1. Go to the [Policies page](https://scout.docker.com/reports/policy) in the Docker Scout Dashboard.
2. Select the policy you want to edit.
3. Select the **Edit** button.
4. Update the policy parameters.
5. Save the changes.

## Disable a policy

When you disable a policy, evaluation results for that policy are hidden, and
no longer appear in the Docker Scout Dashboard or in the CLI. Historic
evaluation results aren't deleted if you disable a policy, so if you change
your mind and re-enable a policy later, results from earlier evaluations will
still be available.

To disable a policy:

1. Go to the [Policies page](https://scout.docker.com/reports/policy) in the Docker Scout Dashboard.
2. Select the policy you want to disable.
3. Select the **Disable** button.

## Delete a policy

When you delete a policy, evaluation results for that policy are deleted as
well, and no longer appear in the Docker Scout Dashboard or in the CLI.

To delete a policy:

1. Go to the [Policies page](https://scout.docker.com/reports/policy) in the Docker Scout Dashboard.
2. Select the policy you want to delete.
3. Select the **Delete** button.

## Recover a deleted policy

If you've deleted a policy, you can recreate it by following the steps in [Add
a policy](#add-a-policy). On the policy configuration screen, select
**Configure** on the deleted policy that you wish to recreate.

---

# Remediation with Docker Scout

> Learn how Docker Scout can help you improve your software quality automatically, using remediation

# Remediation with Docker Scout

   Table of contents

---

Availability: Beta

Docker Scout helps you remediate supply chain or security issues by providing
recommendations based on policy evaluation results. Recommendations are
suggested actions you can take that improve policy compliance, or that add
metadata to images which enables Docker Scout to provide better evaluation
results and recommendations.

Docker Scout provides remediation advice for the default policies of the
following policy types:

- [Up-to-Date Base Images](#up-to-date-base-images-remediation)
- [Supply Chain Attestations](#supply-chain-attestations-remediation)

> Note
>
> Guided remediation is not supported for custom policies.

For images that violate policy, the recommendations focus on addressing
compliance issues and fixing violations. For images where Docker Scout is
unable to determine compliance, recommendations show you how to meet the
prerequisites that ensure Docker Scout can successfully evaluate the policy.

## View recommendations

Recommendations appear on the policy details pages of the Docker Scout
Dashboard. To get to this page:

1. Go to the [Policies page](https://scout.docker.com/reports/policy) in the Docker Scout Dashboard.
2. Select a policy in the list.

The policy details page groups evaluation results into two different tabs
depending on the policy status:

- Violations
- Compliance unknown

The **Violations** tab lists images that don't comply with the selected policy.
The **Compliance unknown** tab lists images that Docker Scout is unable to
determine the compliance status for. When compliance is unknown, Docker Scout
needs more information about the image.

To view recommended actions for an image, hover over one of the images in the
list to reveal a **View fixes** button.

![Remediation for policy violations](https://docs.docker.com/scout/images/remediation.png)  ![Remediation for policy violations](https://docs.docker.com/scout/images/remediation.png)

Select the **View fixes** button to opens the remediation side panel containing
recommended actions for your image.

If there are more than one recommendations available, the primary
recommendation displays as the **Recommended fix**. Additional recommendations
are listed as **Quick fixes**. Quick fixes are usually actions that provide a
temporary solution.

The side panel may also contain one or more help sections related to the
available recommendations.

## Up-to-Date Base Images remediation

The **Up-to-Date Base Images** policy checks whether the base image you use is
up-to-date. The recommended actions displayed in the remediation side panel
depend on how much information Docker Scout has about your image. The more
information that's available, the better the recommendations.

The following scenarios outline the different recommendations depending on the
information available about the image.

### No provenance attestations

For Docker Scout to be able to evaluate this policy, you must add
[provenance
attestations](https://docs.docker.com/build/metadata/attestations/slsa-provenance/) to your image. If
your image doesn't have provenance attestations, compliance is undeterminable.

### Provenance attestations available

With provenance attestations added, Docker Scout can correctly detect the base
image version that you're using. The version found in the attestations is
cross-referenced against the current version of the corresponding tag to
determine if it's up-to-date.

If there's a policy violation, the recommended actions show how to update your
base image version to the latest version, while also pinning the base image
version to a specific digest. For more information, see
[Pin base image
versions](https://docs.docker.com/build/building/best-practices/#pin-base-image-versions).

### GitHub integration enabled

If you're hosting the source code for your image on GitHub, you can enable the
[GitHub integration](https://docs.docker.com/scout/integrations/source-code-management/github/). This
integration enables Docker Scout to provide even more useful remediation
advice, and lets you initiate remediation for violations directly from the
Docker Scout Dashboard.

With the GitHub integration enabled, you can use the remediation side panel to
raise a pull request on the GitHub repository of the image. The pull request
automatically updates the base image version in your Dockerfile to the
up-to-date version.

This automated remediation pins your base image to a specific digest, while
helping you stay up-to-date as new versions become available. Pinning the base
image to a digest is important for reproducibility, and helps avoid unwanted
changes from making their way into your supply chain.

For more information about base image pinning, see
[Pin base image
versions](https://docs.docker.com/build/building/best-practices/#pin-base-image-versions).

## Supply Chain Attestations remediation

The default **Supply Chain Attestations** policy requires full provenance and
SBOM attestations on images. If your image is missing an attestation, or if an
attestation doesn't contain enough information, the policy is violated.

The recommendations available in the remediation side panel helps guide you to
what action you need to take to address the issues. For example, if your image
has a provenance attestation, but the attestation doesn't contain enough
information, you're recommended to re-build your image with
[mode=max](https://docs.docker.com/build/metadata/attestations/slsa-provenance/#max) provenance.
