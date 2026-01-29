# Install Docker Scout and more

# Install Docker Scout

> Installation instructions for the Docker Scout CLI plugin

# Install Docker Scout

   Table of contents

---

The Docker Scout CLI plugin comes pre-installed with Docker Desktop.

If you run Docker Engine without Docker Desktop,
Docker Scout doesn't come pre-installed,
but you can install it as a standalone binary.

## Installation script

To install the latest version of the plugin, run the following commands:

```console
$ curl -fsSL https://raw.githubusercontent.com/docker/scout-cli/main/install.sh -o install-scout.sh
$ sh install-scout.sh
```

> Note
>
> Always examine scripts downloaded from the internet before running them
> locally. Before installing, make yourself familiar with potential risks and
> limitations of the convenience script.

## Manual installation

1. Download the latest release from the [releases page](https://github.com/docker/scout-cli/releases).
2. Create a subdirectory under `$HOME/.docker` called `scout`.
  ```console
  $ mkdir -p $HOME/.docker/scout
  ```
3. Extract the archive and move the `docker-scout` binary to the `$HOME/.docker/scout` directory.
4. Make the binary executable: `chmod +x $HOME/.docker/scout/docker-scout`.
5. Add the `scout` subdirectory to your `.docker/config.json` as a plugin directory:
  ```json
  {
    "cliPluginsExtraDirs": [
      "/home/USER/.docker/scout"
    ]
  }
  ```
  Substitute `<USER>` with your username on the system.
  > Note
  >
  > The path for `cliPluginsExtraDirs` must be an absolute path.

1. Download the latest release from the [releases page](https://github.com/docker/scout-cli/releases).
2. Create a subdirectory under `$HOME/.docker` called `scout`.
  ```console
  $ mkdir -p $HOME/.docker/scout
  ```
3. Extract the archive and move the `docker-scout` binary to the `$HOME/.docker/scout` directory.
4. Make the binary executable:
  ```console
  $ chmod +x $HOME/.docker/scout/docker-scout
  ```
5. Authorize the binary to be executable on macOS:
  ```console
  xattr -d com.apple.quarantine $HOME/.docker/scout/docker-scout
  ```
6. Add the `scout` subdirectory to your `.docker/config.json` as a plugin directory:
  ```json
  {
    "cliPluginsExtraDirs": [
      "/Users/USER/.docker/scout"
    ]
  }
  ```
  Substitute `<USER>` with your username on the system.
  > Note
  >
  > The path for `cliPluginsExtraDirs` must be an absolute path.

1. Download the latest release from the [releases page](https://github.com/docker/scout-cli/releases).
2. Create a subdirectory under `%USERPROFILE%/.docker` called `scout`.
  ```console
  % mkdir %USERPROFILE%\.docker\scout
  ```
3. Extract the archive and move the `docker-scout.exe` binary to the `%USERPROFILE%\.docker\scout` directory.
4. Add the `scout` subdirectory to your `.docker\config.json` as a plugin directory:
  ```json
  {
    "cliPluginsExtraDirs": [
      "C:\Users\USER\.docker\scout"
    ]
  }
  ```
  Substitute `<USER>` with your username on the system.
  > Note
  >
  > The path for `cliPluginsExtraDirs` must be an absolute path.

## Container image

The Docker Scout CLI plugin is also available as a [container image](https://hub.docker.com/r/docker/scout-cli).
Use the `docker/scout-cli` to run `docker scout` commands without installing the CLI plugin on your host.

```console
$ docker run -it \
  -e DOCKER_SCOUT_HUB_USER=<your Docker Hub user name> \
  -e DOCKER_SCOUT_HUB_PASSWORD=<your Docker Hub PAT>  \
  docker/scout-cli <command>
```

## GitHub Action

The Docker Scout CLI plugin is also available as a [GitHub action](https://github.com/docker/scout-action).
You can use it in your GitHub workflows to automatically analyze images and evaluate policy compliance with each push.

Docker Scout also integrates with many more CI/CD tools, such as Jenkins, GitLab, and Azure DevOps.
Learn more about the [integrations](https://docs.docker.com/scout/integrations/) available for Docker Scout.

---

# Integrate Docker Scout with Microsoft Azure DevOps Pipelines

> How to integrate Docker Scout with Microsoft Azure DevOps Pipelines

# Integrate Docker Scout with Microsoft Azure DevOps Pipelines

---

The following examples runs in an Azure DevOps-connected repository containing
a Docker image's definition and contents. Triggered by a commit to the main
branch, the pipeline builds the image and uses Docker Scout to create a CVE
report.

First, set up the rest of the workflow and set up the variables available to all
pipeline steps. Add the following to an *azure-pipelines.yml* file:

```yaml
trigger:
  - main

resources:
  - repo: self

variables:
  tag: "$(Build.BuildId)"
  image: "vonwig/nodejs-service"
```

This sets up the workflow to use a particular container image for the
application and tag each new image build with the build ID.

Add the following to the YAML file:

```yaml
stages:
  - stage: Build
    displayName: Build image
    jobs:
      - job: Build
        displayName: Build
        pool:
          vmImage: ubuntu-latest
        steps:
          - task: Docker@2
            displayName: Build an image
            inputs:
              command: build
              dockerfile: "$(Build.SourcesDirectory)/Dockerfile"
              repository: $(image)
              tags: |
                $(tag)
          - task: CmdLine@2
            displayName: Find CVEs on image
            inputs:
              script: |
                # Install the Docker Scout CLI
                curl -sSfL https://raw.githubusercontent.com/docker/scout-cli/main/install.sh | sh -s --
                # Login to Docker Hub required for Docker Scout CLI
                echo $(DOCKER_HUB_PAT) | docker login -u $(DOCKER_HUB_USER) --password-stdin
                # Get a CVE report for the built image and fail the pipeline when critical or high CVEs are detected
                docker scout cves $(image):$(tag) --exit-code --only-severity critical,high
```

This creates the flow mentioned previously. It builds and tags the image using
the checked-out Dockerfile, downloads the Docker Scout CLI, and then runs the
`cves` command against the new tag to generate a CVE report. It only shows
critical or high-severity vulnerabilities.

---

# Integrate Docker Scout with Circle CI

> How to integrate Docker Scout with Circle CI

# Integrate Docker Scout with Circle CI

---

The following examples runs when triggered in CircleCI. When triggered, it
checks out the "docker/scout-demo-service:latest" image and tag and then uses
Docker Scout to create a CVE report.

Add the following to a *.circleci/config.yml* file.

First, set up the rest of the workflow. Add the following to the YAML file:

```yaml
version: 2.1

jobs:
  build:
    docker:
      - image: cimg/base:stable
    environment:
      IMAGE_TAG: docker/scout-demo-service:latest
```

This defines the container image the workflow uses and an environment variable
for the image.

Add the following to the YAML file to define the steps for the workflow:

```yaml
steps:
  # Checkout the repository files
  - checkout

  # Set up a separate Docker environment to run `docker` commands in
  - setup_remote_docker:
      version: 20.10.24

  # Install Docker Scout and login to Docker Hub
  - run:
      name: Install Docker Scout
      command: |
        env
        curl -sSfL https://raw.githubusercontent.com/docker/scout-cli/main/install.sh | sh -s -- -b /home/circleci/bin
        echo $DOCKER_HUB_PAT | docker login -u $DOCKER_HUB_USER --password-stdin

  # Build the Docker image
  - run:
      name: Build Docker image
      command: docker build -t $IMAGE_TAG .

  # Run Docker Scout
  - run:
      name: Scan image for CVEs
      command: |
        docker-scout cves $IMAGE_TAG --exit-code --only-severity critical,high
```

This checks out the repository files and then sets up a separate Docker
environment to run commands in.

It installs Docker Scout, logs into Docker Hub, builds the Docker image, and
then runs Docker Scout to generate a CVE report. It only shows critical or
high-severity vulnerabilities.

Finally, add a name for the workflow and the workflow's jobs:

```yaml
workflows:
  build-docker-image:
    jobs:
      - build
```

---

# Integrate Docker Scout with GitHub Actions

> How to integrate Docker Scout with GitHub Actions

# Integrate Docker Scout with GitHub Actions

   Table of contents

---

The following example shows how to set up a Docker Scout workflow with GitHub
Actions. Triggered by a pull request, the action builds the image and uses
Docker Scout to compare the new version to the version of that image running in
production.

This workflow uses the
[docker/scout-action](https://github.com/docker/scout-action) GitHub Action to
run the `docker scout compare` command to visualize how images for pull request
stack up against the image you run in production.

## Prerequisites

- This example assumes that you have an existing image repository, in Docker Hub
  or in another registry, where you've enabled Docker Scout.
- This example makes use of [environments](https://docs.docker.com/scout/integrations/environment/), to compare
  the image built in the pull request with a different version of the same image
  in an environment called `production`.

## Steps

First, set up the GitHub Action workflow to build an image. This isn't specific
to Docker Scout here, but you'll need to build an image to have
something to compare with.

Add the following to a GitHub Actions YAML file:

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
  # Hostname of your registry
  REGISTRY: docker.io
  # Image repository, without hostname and tag
  IMAGE_NAME: ${{ github.repository }}
  SHA: ${{ github.event.pull_request.head.sha || github.event.after }}

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write

    steps:
      # Authenticate to the container registry
      - name: Authenticate to registry ${{ env.REGISTRY }}
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ secrets.REGISTRY_USER }}
          password: ${{ secrets.REGISTRY_TOKEN }}

      - name: Setup Docker buildx
        uses: docker/setup-buildx-action@v3

      # Extract metadata (tags, labels) for Docker
      - name: Extract Docker metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          labels: |
            org.opencontainers.image.revision=${{ env.SHA }}
          tags: |
            type=edge,branch=$repo.default_branch
            type=semver,pattern=v{{version}}
            type=sha,prefix=,suffix=,format=short

      # Build and push Docker image with Buildx
      # (don't push on PR, load instead)
      - name: Build and push Docker image
        id: build-and-push
        uses: docker/build-push-action@v6
        with:
          sbom: ${{ github.event_name != 'pull_request' }}
          provenance: ${{ github.event_name != 'pull_request' }}
          push: ${{ github.event_name != 'pull_request' }}
          load: ${{ github.event_name == 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

This creates workflow steps to:

1. Set up Docker buildx.
2. Authenticate to the registry.
3. Extract metadata from Git reference and GitHub events.
4. Build and push the Docker image to the registry.

> Note
>
> This CI workflow runs a local analysis and evaluation of your image. To
> evaluate the image locally, you must ensure that the image is loaded the
> local image store of your runner.
>
>
>
> This comparison doesn't work if you push the image to a registry, or if you
> build an image that can't be loaded to the runner's local image store. For
> example, multi-platform images or images with SBOM or provenance attestation
> can't be loaded to the local image store.

With this setup out of the way, you can add the following steps to run the
image comparison:

```yaml
# You can skip this step if Docker Hub is your registry
      # and you already authenticated before
      - name: Authenticate to Docker
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USER }}
          password: ${{ secrets.DOCKER_PAT }}

      # Compare the image built in the pull request with the one in production
      - name: Docker Scout
        id: docker-scout
        if: ${{ github.event_name == 'pull_request' }}
        uses: docker/scout-action@v1
        with:
          command: compare
          image: ${{ steps.meta.outputs.tags }}
          to-env: production
          ignore-unchanged: true
          only-severities: critical,high
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

The compare command analyzes the image and evaluates policy compliance, and
cross-references the results with the corresponding image in the `production`
environment. This example only includes critical and high-severity
vulnerabilities, and excludes vulnerabilities that exist in both images,
showing only what's changed.

The GitHub Action outputs the comparison results in a pull request comment by
default.

![A screenshot showing the results of Docker Scout output in a GitHub Action](https://docs.docker.com/scout/images/gha-output.webp)  ![A screenshot showing the results of Docker Scout output in a GitHub Action](https://docs.docker.com/scout/images/gha-output.webp)

Expand the **Policies** section to view the difference in policy compliance
between the two images. Note that while the new image in this example isn't
fully compliant, the output shows that the standing for the new image has
improved compared to the baseline.

![GHA policy evaluation output](https://docs.docker.com/scout/images/gha-policy-eval.webp)  ![GHA policy evaluation output](https://docs.docker.com/scout/images/gha-policy-eval.webp)

---

# Integrate Docker Scout with GitLab CI/CD

> How to integrate Docker Scout with GitLab CI

# Integrate Docker Scout with GitLab CI/CD

   Table of contents

---

The following examples runs in GitLab CI in a repository containing a Docker
image's definition and contents. Triggered by a commit, the pipeline builds the
image. If the commit was to the default branch, it uses Docker Scout to get a
CVE report. If the commit was to a different branch, it uses Docker Scout to
compare the new version to the current published version.

## Steps

First, set up the rest of the workflow. There's a lot that's not specific to
Docker Scout but needed to create the images to compare.

Add the following to a `.gitlab-ci.yml` file at the root of your repository.

```yaml
docker-build:
  image: docker:latest
  stage: build
  services:
    - docker:dind
  before_script:
    - docker login -u "$CI_REGISTRY_USER" -p "$CI_REGISTRY_PASSWORD" $CI_REGISTRY

    # Install curl and the Docker Scout CLI
    - |
      apk add --update curl
      curl -sSfL https://raw.githubusercontent.com/docker/scout-cli/main/install.sh | sh -s --
      apk del curl
      rm -rf /var/cache/apk/*
    # Login to Docker Hub required for Docker Scout CLI
    - echo "$DOCKER_HUB_PAT" | docker login -u "$DOCKER_HUB_USER" --password-stdin
```

This sets up the workflow to build Docker images with Docker-in-Docker mode,
running Docker inside a container.

It then downloads `curl` and the Docker Scout CLI plugin, logs into the Docker
registry using environment variables defined in your repository's settings.

Add the following to the YAML file:

```yaml
script:
  - |
    if [[ "$CI_COMMIT_BRANCH" == "$CI_DEFAULT_BRANCH" ]]; then
      tag=""
      echo "Running on default branch '$CI_DEFAULT_BRANCH': tag = 'latest'"
    else
      tag=":$CI_COMMIT_REF_SLUG"
      echo "Running on branch '$CI_COMMIT_BRANCH': tag = $tag"
    fi
  - docker build --pull -t "$CI_REGISTRY_IMAGE${tag}" .
  - |
    if [[ "$CI_COMMIT_BRANCH" == "$CI_DEFAULT_BRANCH" ]]; then
      # Get a CVE report for the built image and fail the pipeline when critical or high CVEs are detected
      docker scout cves "$CI_REGISTRY_IMAGE${tag}" --exit-code --only-severity critical,high
    else
      # Compare image from branch with latest image from the default branch and fail if new critical or high CVEs are detected
      docker scout compare "$CI_REGISTRY_IMAGE${tag}" --to "$CI_REGISTRY_IMAGE:latest" --exit-code --only-severity critical,high --ignore-unchanged
    fi

  - docker push "$CI_REGISTRY_IMAGE${tag}"
```

This creates the flow mentioned previously. If the commit was to the default
branch, Docker Scout generates a CVE report. If the commit was to a different
branch, Docker Scout compares the new version to the current published version.
It only shows critical or high-severity vulnerabilities and ignores
vulnerabilities that haven't changed since the last analysis.

Add the following to the YAML file:

```yaml
rules:
  - if: $CI_COMMIT_BRANCH
    exists:
      - Dockerfile
```

These final lines ensure that the pipeline only runs if the commit contains a
Dockerfile and if the commit was to the CI branch.

## Video walkthrough

The following is a video walkthrough of the process of setting up the workflow with GitLab.

---

# Integrate Docker Scout with Jenkins

> How to integrate Docker Scout with Jenkins

# Integrate Docker Scout with Jenkins

---

You can add the following stage and steps definition to a `Jenkinsfile` to run
Docker Scout as part of a Jenkins pipeline. The pipeline needs a `DOCKER_HUB`
credential containing the username and password for authenticating to Docker
Hub. It also needs an environment variable defined for the image and tag.

```groovy
pipeline {
    agent {
        // Agent details
    }

    environment {
        DOCKER_HUB = credentials('jenkins-docker-hub-credentials')
        IMAGE_TAG  = 'myorg/scout-demo-service:latest'
    }

    stages {
        stage('Analyze image') {
            steps {
                // Install Docker Scout
                sh 'curl -sSfL https://raw.githubusercontent.com/docker/scout-cli/main/install.sh | sh -s -- -b /usr/local/bin'

                // Log into Docker Hub
                sh 'echo $DOCKER_HUB_PSW | docker login -u $DOCKER_HUB_USR --password-stdin'

                // Analyze and fail on critical or high vulnerabilities
                sh 'docker-scout cves $IMAGE_TAG --exit-code --only-severity critical,high'
            }
        }
    }
}
```

This installs Docker Scout, logs into Docker Hub, and then runs Docker Scout to
generate a CVE report for an image and tag. It only shows critical or
high-severity vulnerabilities.

> Note
>
> If you're seeing a `permission denied` error related to the image cache, try
> setting the
> [DOCKER_SCOUT_CACHE_DIR](https://docs.docker.com/scout/how-tos/configure-cli/) environment
> variable to a writable directory. Or alternatively, disable local caching
> entirely with `DOCKER_SCOUT_NO_CACHE=true`.

---

# Using Docker Scout in continuous integration

> How to setup Docker Scout in continuous integration pipelines

# Using Docker Scout in continuous integration

---

You can analyze Docker images in continuous integration pipelines as you build
them using a GitHub action or the Docker Scout CLI plugin.

Available integrations:

- [GitHub Actions](https://docs.docker.com/scout/integrations/ci/gha/)
- [GitLab](https://docs.docker.com/scout/integrations/ci/gitlab/)
- [Microsoft Azure DevOps Pipelines](https://docs.docker.com/scout/integrations/ci/azure/)
- [Circle CI](https://docs.docker.com/scout/integrations/ci/circle-ci/)
- [Jenkins](https://docs.docker.com/scout/integrations/ci/jenkins/)

You can also add runtime integration as part of your CI/CD pipeline, which lets
you assign an image to an environment, such as `production` or `staging`, when
you deploy it. For more information, see [Environment monitoring](https://docs.docker.com/scout/integrations/environment/).

---

# Integrate Docker Scout with SonarQube

> Evaluate your images with the SonarQube quality gates defined in your projects

# Integrate Docker Scout with SonarQube

   Table of contents

---

The SonarQube integration enables Docker Scout to surface SonarQube quality
gate checks through Policy Evaluation, under a new
[SonarQube Quality Gates
Policy](https://docs.docker.com/scout/policy/#sonarqube-quality-gates-policy).

## How it works

This integration uses [SonarQube
webhooks](https://docs.sonarsource.com/sonarqube/latest/project-administration/webhooks/)
to notify Docker Scout of when a SonarQube project analysis has completed. When
the webhook is called, Docker Scout receives the analysis results, and stores
them in the database.

When you push a new image to a repository, Docker Scout evaluates the results
of the SonarQube analysis record corresponding to the image. Docker Scout uses
Git provenance metadata on the images, from provenance attestations or an OCI
annotations, to link image repositories with SonarQube analysis results.

> Note
>
> Docker Scout doesn't have access to historic SonarQube analysis records. Only
> analysis results recorded after the integration is enabled will be available
> to Docker Scout.

Both self-managed SonarQube instances and SonarCloud are supported.

## Prerequisites

To integrate Docker Scout with SonarQube, ensure that:

- Your image repository is [integrated with Docker Scout](https://docs.docker.com/scout/integrations/#container-registries).
- Your images are built with
  [provenance attestations](https://docs.docker.com/build/metadata/attestations/slsa-provenance/),
  or the `org.opencontainers.image.revision` annotation,
  containing information about the Git repository.

## Enable the SonarQube integration

1. Go to the [SonarQube integrations page](https://scout.docker.com/settings/integrations/sonarqube/)
  on the Docker Scout Dashboard.
2. In the **How to integrate** section, enter a configuration name for this
  integration. Docker Scout uses this label as a display name for the
  integration, and to name the webhook.
3. Select **Next**.
4. Enter the configuration details for your SonarQube instance. Docker Scout
  uses this information to create SonarQube webhook.
  In SonarQube, [generate a newUser token](https://docs.sonarsource.com/sonarqube/latest/user-guide/user-account/generating-and-using-tokens/#generating-a-token).
  The token requires 'Administer' permission on the specified project, or
  global 'Administer' permission.
  Enter the token, your SonarQube URL, and the ID of your SonarQube
  organization. The SonarQube organization is required if you're using
  SonarCloud.
5. Select **Enable configuration**.
  Docker Scout performs a connection test to verify that the provided details
  are correct, and that the token has the necessary permissions.
6. After a successful connection test, you're redirected to the SonarQube
  integration overview, which lists all your SonarQube integrations and their
  statuses.

From the integration overview page, you can go directly to the
**SonarQube Quality Gates Policy**.
This policy will have no results initially. To start seeing evaluation results
for this policy, trigger a new SonarQube analysis of your project and push the
corresponding image to a repository. For more information, refer to the
[policy description](https://docs.docker.com/scout/policy/#sonarqube-quality-gates).

---

# Generic environment integration with CLI

> Integrate your runtime environments with Docker Scout using the CLI client

# Generic environment integration with CLI

   Table of contents

---

You can create a generic environment integration by running the Docker Scout
CLI client in your CI workflows. The CLI client is available as a binary on
GitHub and as a container image on Docker Hub. Use the client to invoke the
`docker scout environment` command to assign your images to environments.

For more information about how to use the `docker scout environment` command,
refer to the
[CLI reference](https://docs.docker.com/reference/cli/docker/scout/environment/).

## Examples

Before you start, set the following environment variables in your CI system:

- `DOCKER_SCOUT_HUB_USER`: your Docker Hub username
- `DOCKER_SCOUT_HUB_PASSWORD`: your Docker Hub personal access token

Make sure the variables are accessible to your project.

```yaml
version: 2.1

jobs:
  record_environment:
    machine:
      image: ubuntu-2204:current
    image: namespace/repo
    steps:
      - run: |
          if [[ -z "$CIRCLE_TAG" ]]; then
            tag="$CIRCLE_TAG"
            echo "Running tag '$CIRCLE_TAG'"
          else
            tag="$CIRCLE_BRANCH"
            echo "Running on branch '$CI_COMMIT_BRANCH'"
          fi
          echo "tag = $tag"
      - run: docker run -it \
          -e DOCKER_SCOUT_HUB_USER=$DOCKER_SCOUT_HUB_USER \
          -e DOCKER_SCOUT_HUB_PASSWORD=$DOCKER_SCOUT_HUB_PASSWORD \
          docker/scout-cli:1.0.2 environment \
          --org "MY_DOCKER_ORG" \
          "ENVIRONMENT" ${image}:${tag}
```

The following example uses the [Docker executor](https://docs.gitlab.com/runner/executors/docker.html).

```yaml
variables:
  image: namespace/repo

record_environment:
  image: docker/scout-cli:1.0.2
  script:
    - |
      if [[ -z "$CI_COMMIT_TAG" ]]; then
        tag="latest"
        echo "Running tag '$CI_COMMIT_TAG'"
      else
        tag="$CI_COMMIT_REF_SLUG"
        echo "Running on branch '$CI_COMMIT_BRANCH'"
      fi
      echo "tag = $tag"
    - environment --org MY_DOCKER_ORG "PRODUCTION" ${image}:${tag}
```

```yaml
trigger:
  - main

resources:
  - repo: self

variables:
  tag: "$(Build.BuildId)"
  image: "namespace/repo"

stages:
  - stage: Docker Scout
    displayName: Docker Scout environment integration
    jobs:
      - job: Record
        displayName: Record environment
        pool:
          vmImage: ubuntu-latest
        steps:
          - task: Docker@2
          - script: docker run -it \
              -e DOCKER_SCOUT_HUB_USER=$DOCKER_SCOUT_HUB_USER \
              -e DOCKER_SCOUT_HUB_PASSWORD=$DOCKER_SCOUT_HUB_PASSWORD \
              docker/scout-cli:1.0.2 environment \
              --org "MY_DOCKER_ORG" \
              "ENVIRONMENT" $(image):$(tag)
```

```groovy
stage('Analyze image') {
    steps {
        // Install Docker Scout
        sh 'curl -sSfL https://raw.githubusercontent.com/docker/scout-cli/main/install.sh | sh -s -- -b /usr/local/bin'

        // Log into Docker Hub
        sh 'echo $DOCKER_SCOUT_HUB_PASSWORD | docker login -u $DOCKER_SCOUT_HUB_USER --password-stdin'

        // Analyze and fail on critical or high vulnerabilities
        sh 'docker-scout environment --org "MY_DOCKER_ORG" "ENVIRONMENT" $IMAGE_TAG
    }
}
```

---

# Integrate Docker Scout with Sysdig

> Integrate your runtime environments with Docker Scout using Sysdig

# Integrate Docker Scout with Sysdig

   Table of contents

---

The Sysdig integration enables Docker Scout to automatically detect the images
you're using for your running workloads. Activating this integration gives you
real-time insights about your security posture, and lets you compare your
builds with what's running in production.

## How it works

The Sysdig Agent captures the images of your container workloads. Docker Scout
integrates with the Sysdig API to discover the images in your cluster. This
integration uses Sysdig's Risk Spotlight feature. For more information, see
[Risk Spotlight Integrations (Sysdig docs)](https://docs.sysdig.com/en/docs/sysdig-secure/integrations-for-sysdig-secure/risk-spotlight-integrations/).

> Tip
>
> Sysdig offers a free trial for Docker users to try out the new Docker Scout integration.
>
> [Sign up](https://sysdig.com/free-trial-for-docker-customers/)

Each Sysdig integration maps to an environment. When you enable a Sysdig
integration, you specify the environment name for that cluster, such as
`production` or `staging`. Docker Scout assigns the images in the cluster to
the corresponding environment. This lets you use the environment filters to see
vulnerability status and policy compliance for an environment.

Only images analyzed by Docker Scout can be assigned to an environment. The
Sysdig runtime integration doesn't trigger image analysis by itself. To analyze
images automatically, enable a [registry integration](https://docs.docker.com/scout/integrations/#container-registries).

Image analysis must not necessarily precede the runtime integration, but the
environment assignment only takes place once Docker Scout has analyzed the
image.

## Prerequisites

- Install the Sysdig Agent in the cluster that you want to integrate, see [Install Sysdig Agent (Sysdig docs)](https://docs.sysdig.com/en/docs/installation/sysdig-monitor/install-sysdig-agent/).
- Enable profiling for Risk Spotlight Integrations in Sysdig, see [Profiling (Sysdig docs)](https://docs.sysdig.com/en/docs/sysdig-secure/policies/profiling/#enablement).
- You must be an organization owner to enable the integration in the Docker Scout Dashboard.

## Integrate an environment

1. Go to the [Sysdig integration page](https://scout.docker.com/settings/integrations/sysdig/)
  on the Docker Scout Dashboard.
2. In the **How to integrate** section, enter a configuration name for this
  integration. Docker Scout uses this label as a display name for the
  integration.
3. Select **Next**.
4. Enter a Risk Spotlight API token and select the region in the drop-down list.
  The Risk Spotlight API token is the Sysdig token that Docker Scout needs to
  integrate with Sysdig. For more instructions on how to generate a Risk
  Spotlight token, See [Risk Spotlight Integrations (Sysdig docs)](https://docs.sysdig.com/en/docs/sysdig-secure/integrations-for-sysdig-secure/risk-spotlight-integrations/docker-scout/#generate-a-token-for-the-integration).
  The region corresponds to the `global.sysdig.region` configuration parameter
  set when deploying the Sysdig Agent.
5. Select **Next**.
  After selecting **Next**, Docker Scout connects to Sysdig and retrieves the
  cluster names for your Sysdig account. Cluster names correspond to the
  `global.clusterConfig.name` configuration parameter set when deploying
  Sysdig Agents.
  An error displays if Docker Scout fails to connect to Sysdig using the
  provided token. If there's an error, you won't be able to continue the
  integration. Go back and verify that the configuration details are correct.
6. Select a cluster name in the drop-down list.
7. Select **Next**.
8. Assign an environment name for this cluster.
  You can reuse an existing environment or create a new one.
9. Select **Enable integration**.

After enabling the integration, Docker Scout automatically detects images
running in the cluster, and assigns those images to the environment associated
with the cluster. For more information about environments, see [Environment
monitoring](https://docs.docker.com/scout/integrations/environment/).

> Note
>
> Docker Scout only detects images that have been analyzed. To trigger an image
> analysis, enable a [registry integration](https://docs.docker.com/scout/integrations/#container-registries)
> and push an image to your registry.
>
>
>
> If you created a new environment for this integration, the environment
> appears in Docker Scout when at least one image has been analyzed.

To integrate more clusters, go to the [Sysdig integrations page](https://scout.docker.com/settings/integrations/sysdig/)
and select the **Add** button.

---

# Integrating Docker Scout with environments

> Docker Scout can integrate with runtime environments to give you real-time insights about your software supply chain.

# Integrating Docker Scout with environments

   Table of contents

---

You can integrate Docker Scout with your runtime environments, and get insights
for your running workloads. This gives you a real-time view of your security
status for your deployed artifacts.

Docker Scout lets you define multiple environments, and assign images to
different environments. This gives you a complete overview of your software
supply chain, and lets you view and compare deltas between environments, for
example staging and production.

How you define and name your environments is up to you. You can use patterns
that are meaningful to you and that matches how you ship your applications.

## Assign to environments

Each environment contains references to a number of images. These references
represent containers currently running in that particular environment.

For example, say you're running `myorg/webapp:3.1` in production, you can
assign that tag to your `production` environment. You might be running a
different version of the same image in staging, in which case you can assign
that version of the image to the `staging` environment.

To add environments to Docker Scout, you can:

- Use the `docker scout env <environment> <image>` CLI command to record images to environments manually
- Enable a runtime integration to automatically detect images in your environments.

Docker Scout supports the following runtime integrations:

- [Docker Scout GitHub Action](https://github.com/marketplace/actions/docker-scout#record-an-image-deployed-to-an-environment)
- [CLI client](https://docs.docker.com/scout/integrations/environment/cli/)
- [Sysdig integration](https://docs.docker.com/scout/integrations/environment/sysdig/)

> Note
>
> Only organization owners can create new environments and set up integrations.
> Additionally, Docker Scout only assigns an image to an environment if the
> image
> [has been analyzed](https://docs.docker.com/scout/explore/analysis/), either manually or
> through a
> [registry integration](https://docs.docker.com/scout/integrations/#container-registries).

## List environments

To see all of the available environments for an organization, you can use the
`docker scout env` command.

```console
$ docker scout env
```

By default, this prints all environments for your personal Docker organization.
To list environments for another organization that you're a part of, use the
`--org` flag.

```console
$ docker scout env --org <org>
```

You can use the `docker scout config` command to change the default
organization. This changes the default organization for all `docker scout`
commands, not just `env`.

```console
$ docker scout config organization <org>
```

## Comparing between environments

Assigning images to environments lets you make comparisons with and between
environments. This is useful for things like GitHub pull requests, for
comparing the image built from the code in the PR to the corresponding image in
staging or production.

You can also compare with streams using the `--to-env` flag on the
[docker scout compare](https://docs.docker.com/reference/cli/docker/scout/compare/)
CLI command:

```console
$ docker scout compare --to-env production myorg/webapp:latest
```

## View images for an environment

To view the images for an environment:

1. Go to the [Images page](https://scout.docker.com/) in the Docker Scout Dashboard.
2. Open the **Environments** drop-down menu.
3. Select the environment that you want to view.

The list displays all images that have been assigned to the selected
environment. If you've deployed multiple versions of the same image in an
environment, all versions of the image appear in the list.

Alternatively, you can use the `docker scout env` command to view the images from the terminal.

```console
$ docker scout env production
docker/scout-demo-service:main@sha256:ef08dca54c4f371e7ea090914f503982e890ec81d22fd29aa3b012351a44e1bc
```

### Mismatching image tags

When you've selected an environment on the **Images** tab, tags in the list
represent the tag that was used to deploy the image. Tags are mutable, meaning
that you can change the image digest that a tag refers to. If Docker Scout
detects that a tag refers to an outdated digest, a warning icon displays next
to the image name.

---

# Integrate Docker Scout with Azure Container Registry

> Integrate Azure Container Registry with Docker Scout

# Integrate Docker Scout with Azure Container Registry

   Table of contents

---

Integrating Docker Scout with Azure Container Registry (ACR) lets you view
image insights for images hosted in ACR repositories. After integrating Docker
Scout with ACR and activating Docker Scout for a repository, pushing an image
to the repository automatically triggers image analysis. You can view image
insights using the Docker Scout Dashboard, or the `docker scout` CLI commands.

## How it works

To help you integrate your Azure Container Registry with Docker Scout, you can
use a custom Azure Resource Manager (ARM) template that automatically creates
the necessary infrastructure in Azure for you:

- An EventGrid Topic and Subscription for Image push and delete events.
- A read-only authorization token for the registry, used to list repositories,
  and ingest the images.

When the resources have been created in Azure, you can enable the integration
for image repositories in the integrated ACR instance. Once you've enabled a
repository, pushing new images triggers image analysis automatically. The
analysis results appear in the Docker Scout Dashboard.

If you enable the integration on a repository that already contains images,
Docker Scout pulls and analyzes the latest image version automatically.

### ARM template

The following table describes the configuration resources.

> Note
>
> Creating these resources incurs a small, recurring cost on the Azure account.
> The **Cost** column in the table represents an estimated monthly cost of the
> resources, when integrating an ACR registry that gets 100 images pushed per
> day.
>
>
>
> The Egress cost varies depending on usage, but it’s around $0.1 per GB, and
> the first 100 GB are free.

| Azure | Resource | Cost |
| --- | --- | --- |
| Event Grid system topic | Subscribe to Azure Container Registry events (image push and image delete) | Free |
| Event subscription | Send Event Grid events to Scout via a Webhook subscription | $0.60 for every 1M messages. First 100k for free. |
| Registry Token | Read-only token used for Scout to list the repositories, and pull images from the registry | Free |

The following JSON document shows the ARM template Docker Scout uses to create
the Azure resources.

```json
{
   "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
   "contentVersion": "1.0.0.0",
   "parameters": {
      "DockerScoutWebhook": {
         "metadata": {
            "description": "EventGrid's subscription Webhook"
         },
         "type": "String"
      },
      "RegistryName": {
         "metadata": {
            "description": "Name of the registry to add Docker Scout"
         },
         "type": "String"
      },
      "systemTopics_dockerScoutRepository": {
         "defaultValue": "docker-scout-repository",
         "metadata": {
            "description": "EventGrid's topic name"
         },
         "type": "String"
      }
   },
   "resources": [
      {
         "apiVersion": "2023-06-01-preview",
         "identity": {
            "type": "None"
         },
         "location": "[resourceGroup().location]",
         "name": "[parameters('systemTopics_dockerScoutRepository')]",
         "properties": {
            "source": "[extensionResourceId(resourceGroup().Id , 'Microsoft.ContainerRegistry/Registries', parameters('RegistryName'))]",
            "topicType": "Microsoft.ContainerRegistry.Registries"
         },
         "type": "Microsoft.EventGrid/systemTopics"
      },
      {
         "apiVersion": "2023-06-01-preview",
         "dependsOn": [
            "[resourceId('Microsoft.EventGrid/systemTopics', parameters('systemTopics_dockerScoutRepository'))]"
         ],
         "name": "[concat(parameters('systemTopics_dockerScoutRepository'), '/image-change')]",
         "properties": {
            "destination": {
               "endpointType": "WebHook",
               "properties": {
                  "endpointUrl": "[parameters('DockerScoutWebhook')]",
                  "maxEventsPerBatch": 1,
                  "preferredBatchSizeInKilobytes": 64
               }
            },
            "eventDeliverySchema": "EventGridSchema",
            "filter": {
               "enableAdvancedFilteringOnArrays": true,
               "includedEventTypes": [
                  "Microsoft.ContainerRegistry.ImagePushed",
                  "Microsoft.ContainerRegistry.ImageDeleted"
               ]
            },
            "labels": [],
            "retryPolicy": {
               "eventTimeToLiveInMinutes": 1440,
               "maxDeliveryAttempts": 30
            }
         },
         "type": "Microsoft.EventGrid/systemTopics/eventSubscriptions"
      },
      {
         "apiVersion": "2023-01-01-preview",
         "name": "[concat(parameters('RegistryName'), '/docker-scout-readonly-token')]",
         "properties": {
            "credentials": {},
            "scopeMapId": "[resourceId('Microsoft.ContainerRegistry/registries/scopeMaps', parameters('RegistryName'), '_repositories_pull_metadata_read')]"
         },
         "type": "Microsoft.ContainerRegistry/registries/tokens"
      }
   ],
   "variables": {}
}
```

## Integrate a registry

1. Go to [ACR integration page](https://scout.docker.com/settings/integrations/azure/) on the
  Docker Scout Dashboard.
2. In the **How to integrate** section, enter the **Registry hostname** of the
  registry you want to integrate.
3. Select **Next**.
4. Select **Deploy to Azure** to open the template deployment wizard in Azure.
  You may be prompted to sign in to your Azure account if you're not already
  signed in.
5. In the template wizard, configure your deployment:
  - **Resource group**: enter the same resource group as you're using for the
    container registry. The Docker Scout resources must be deployed to the
    same resource group as the registry.
  - **Registry name**: the field is pre-filled with the subdomain of the
    registry hostname.
6. Select **Review + create**, and then **Create** to deploy the template.
7. Wait until the deployment is complete.
8. In the **Deployment details** section click on the newly created resource
  of the type **Container registry token**. Generate a new password for this token.
  Alternatively, use the search function in Azure to navigate to the
  **Container registry** resource that you're looking to integrate, and
  generate the new password for the created access token.
9. Copy the generated password and head back to the Docker Scout Dashboard to
  finalize the integration.
10. Paste the generated password into the **Registry token** field.
11. Select **Enable integration**.

After selecting **Enable integration**, Docker Scout performs a connection test
to verify the integration. If the verification was successful, you're
redirected to the Azure registry summary page, which shows you all your Azure
integrations for the current organization.

Next, activate Docker Scout for the repositories that you want to analyze in
[Repository settings](https://scout.docker.com/settings/repos/).

After activating repositories, images that you push are analyzed by Docker
Scout. The analysis results appear in the Docker Scout Dashboard.
If your repository already contains images, Docker Scout pulls and analyzes the
latest image version automatically.

## Remove an integration

> Important
>
> Removing the integration in the Docker Scout Dashboard doesn't automatically
> remove the resources created in Azure.

To remove an ACR integration:

1. Go to the [ACR integration page](https://scout.docker.com/settings/integrations/azure/)
  on the Docker Scout Dashboard.
2. Find the ACR integration that you want to remove, and select the **Remove**
  button.
3. In the dialog that opens, confirm by selecting **Remove**.
4. After removing the integration in the Docker Scout Dashboard, also remove
  the Azure resources related to the integration:
  - The `docker-scout-readonly-token` token for the container registry.
  - The `docker-scout-repository` Event Grid System Topic.
