# Import your Google Cloud resources into Terraform stateStay organized with collectionsSave and categorize content based on your preferences. and more

# Import your Google Cloud resources into Terraform stateStay organized with collectionsSave and categorize content based on your preferences.

# Import your Google Cloud resources into Terraform stateStay organized with collectionsSave and categorize content based on your preferences.

Terraform can import existing infrastructure. This allows you to take resources
you've created by some other means and bring them under Terraform management.

You can import the state for any Google Cloud resource.

Terraform supports multiple ways to import resources:

- [One at a time](#import-resources-one-at-a-time) by using the [terraform import](https://developer.hashicorp.com/terraform/cli/commands/import) subcommand.
- [In bulk](#import-resources-in-bulk-in-code) by including an [importblock in the
  configuration](https://developer.hashicorp.com/terraform/tutorials/state/state-import) (requires Terraform  version 1.5 or later).
- In bulk by using a Google Cloud feature that lets you [import
  resources after doing a bulk export](#import-resources-after-doing-a-bulk-export).

## Import resources one at a time

The `import` command takes two arguments—the resource address and ID.
The [resource address](https://developer.hashicorp.com/terraform/cli/state/resource-addressing)
is an identifier that points to a resource instance within a configuration.
The ID is an identifier that identifies a resource in Google Cloud
that is being imported. Format for the ID differs based on resource type and
[is documented](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket#import)
for each resource supported by the provider. We recommend using the full
identifier, which includes the project ID when supported.

- Identify the resource address to be imported.
  ```
  resource "google_storage_bucket" "sample" {
   name          = "my-bucket"
   project       = "sample-project"
   location      = "US"
   force_destroy = true
  }
  ```
  For a sample resource such as Cloud Storage bucket defined earlier,
  this is `google_storage_bucket.sample`.
- To identify the resource ID format, see the [provider import
  documentation](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket#import) for the `google_storage_bucket` resource. In this case, it is of the
  form `project/name`, so the resource ID for the preceding sample is
  `sample-project/my-bucket`.
- Construct the `import` statement by using the resource address and ID, as
  follows:
  ```
  terraform import google_storage_bucket.sample sample-project/my-bucket
  ```
  Output:
  ```
  terraform import google_storage_bucket.sample sample-project/my-bucket
  google_storage_bucket.sample: Importing from ID "sample-project/my-bucket"...
  google_storage_bucket.sample: Import prepared!
  Prepared google_storage_bucket for import
  google_storage_bucket.sample: Refreshing state... [id=sample-project/my-bucket]
  Import successful!
  The resources that were imported are shown above. These resources are now in
  your Terraform state and will henceforth be managed by Terraform.
  ```

### Import resources within modules

Modules encapsulate one or more resources within a Terraform configuration.
Because importing requires a resource address, each resource within a module has to
be imported individually.

- Identify the resources within a module to be imported.
  ```
  module "gcs_bucket" {
   source  = "terraform-google-modules/cloud-storage/google//modules/simple_bucket"
   version = "~> 3.4"
   name       = "my-bucket"
   project_id = "sample-project"
   location   = "us-east1"
  }
  ```
  To identify resource addresses, you can inspect [module contents](https://github.com/terraform-google-modules/terraform-google-cloud-storage/blob/v3.4.0/modules/simple_bucket/main.tf).
  Alternatively, apply the configuration and use the errors surfaced by the
  provider. For example:
  ```
  terraform apply
  module.gcs_bucket.google_storage_bucket.bucket: Creating...
  ╷
  │ Error: googleapi: Error 409: Your previous request to create the named bucket succeeded and you already own it., conflict
  │
  │   with module.gcs_bucket.google_storage_bucket.bucket,
  ```
  By using the preceding log, you can identify the resource address that needs to be
  imported as `module.gcs_bucket.google_storage_bucket.bucket`.
- To identify the resource ID format, see the [provider import
  documentation](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket#import) for the `google_storage_bucket` resource. In this case, it is of
  the form `project/name`. The name can be identified from the plan output.
  Output:
  ```
  module.gcs_bucket.google_storage_bucket.bucket will be created
  + resource "google_storage_bucket" "bucket" {
      + name                        = "my-bucket"
      + project                     = "sample-project"
      ...
    }
  ```
  For the preceding sample, the resource ID is `sample-project/my-bucket`.
- Construct the `import` statement by using the resource address and ID, as
  follows:
  ```
  terraform import module.gcs_bucket.google_storage_bucket.bucket sample-project/my-bucket
  ```
  Output:
  ```
  terraform import module.gcs_bucket.google_storage_bucket.bucket sample-project/my-bucket
  module.gcs_bucket.google_storage_bucket.bucket: Importing from ID "sample-project/my-bucket"...
  module.gcs_bucket.google_storage_bucket.bucket: Import prepared!
  Prepared google_storage_bucket for import
  module.gcs_bucket.google_storage_bucket.bucket: Refreshing state... [id=sample-project/my-bucket]
  Import successful!
  The resources that were imported are shown above. These resources are now in
  your Terraform state and will henceforth be managed by Terraform.
  ```

## Import resources in bulk with a configuration-drivenimportblock

Terraform version 1.5 lets you add an `import` block to your Terraform
configuration. This allows import operations to be previewed during the `plan`
operation and executed using the `apply` operation.

You can also do automatic code generation for imported resources instead of
writing the code manually.

The `import` block takes two parameters:

- `id`: The provider-defined resource ID of the cloud resource to be imported.
  For the accepted provider-defined resource ID, see the **Import** section for
  the resource in Hashicorp's Google provider documentation. For example,
  `projects/{project}/global/networks/{name}` is a resource ID for a
  VPC network, as shown on the
  [google_compute_networkreference page](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/compute_network#import).
- `to`: The Terraform [resource
  address](https://developer.hashicorp.com/terraform/cli/state/resource-addressing)
  to be created. Usually in the form
  RESOURCE TYPE.NAME.

Here’s an example of an `import` block for a Virtual Private Cloud network:

```
import {
  # Provider-defined resource ID of the cloud resource to be imported
  id = "projects/PROJECT_ID/global/networks/my-network"

  # Terraform resource address to be created
  to = google_compute_network.my_network
}
```

If you have manually created your resource block, execute `terraform plan` to
preview the import operation.

If you want Terraform to generate the resource blocks for you, use the
`-generate-config-out` flag to specify the file to generate configuration.

For example:

```
terraform plan -generate-config-out=generated_resources.tf
```

After reviewing the generated code, run the `terraform apply` operation to
import the configuration to the Terraform state.

## Import resources created after doing a bulk export

Bulk export lets you export Google Cloud resources
as Terraform configurations and import Terraform state for those resources
so that you can manage your deployment in Terraform.

### Before you begin

- Prepare Cloud Shell.
  Launch [Cloud Shell](https://shell.cloud.google.com/), and set
  the default Google Cloud project where you want to generate Terraform code for the
  deployed resources.
  You only need to run this command once per project, and you can run it in any
  directory.
  ```
  export GOOGLE_CLOUD_PROJECT=PROJECT_ID
  ```
  Environment variables are overridden if you set explicit values in a
  Terraform configuration file.
- In Cloud Shell, install the command-line interface (CLI) for Config Connector.
  ```
  gcloud components install config-connector
  ```
  Config Connector lets you use Google Cloud's Terraform bulk-export tool.
  If you see `ERROR: (gcloud.components.install) You cannot perform this action
  because the Google Cloud CLI component manager is disabled for this
  installation`, run the following command instead:
  ```
  sudo apt-get install google-cloud-sdk-config-connector
  ```
- Enable the Cloud Asset API.
  ```
  gcloud services enable cloudasset.googleapis.com
  ```

### Generate Terraform code for your resources

1. If you haven't done so already, create the directory where you want to
  output the project's configuration.
  ```
  mkdir OUTPUT_DIRECTORY
  ```
2. Run the [gcloud beta resource-config bulk-export](https://cloud.google.com/sdk/gcloud/reference/beta/resource-config/bulk-export)
  command to output the project's entire configuration  to the
  `OUTPUT_DIRECTORY` path:
  ```
  gcloud beta resource-config bulk-export \
     --path=OUTPUT_DIRECTORY \
     --project=PROJECT_ID \
     --resource-format=terraform
  ```

### Create Terraform modules from the generated code

Run the [gcloud beta resource-config terraform
generate-import](https://cloud.google.com/sdk/gcloud/reference/beta/resource-config/terraform/generate-import)
command, pointing to the content in the output directory:

```
gcloud beta resource-config terraform generate-import OUTPUT_DIRECTORY
```

This command generates Terraform modules and an import script:

- The `gcloud-export-modules.tf` file. This file points to all of
  the modules from the sub-resources. The content of this file looks like this:
  ```
  provider "google" {
   project = "PROJECT_ID"
  }
  module "OUTPUT_DIRECTORY-projects-PROJECT_ID-ComputeFirewall" {
   source = "./OUTPUT_DIRECTORY/projects/PROJECT_ID/ComputeFirewall"
  }
  module "OUTPUT_DIRECTORY-projects-PROJECT_ID-ComputeBackendService-global" {
   source = "./OUTPUT_DIRECTORY/projects/PROJECT_ID/ComputeBackendService/global"
  }
  ```
  ...and so on.
- An executable shell script called something like
  `terraform_import_20220331-19-12-33.sh`.
  The shell script contains a list of `terraform import` commands:
  ```
  #!/bin/sh
  # Terraform Import Script generated by gcloud cli
  terraform import module.OUTPUT_DIRECTORY-projects-PROJECT_ID-ComputeFirewall.google_compute_firewall.allow_ssh projects/PROJECT_ID/global/firewalls/allow-ssh
  ```
  ...and so on.
  The `terraform import` commands are for importing the modules created by the
  `generate-import` command into the Terraform state.

### Import the modules into the Terraform state

1. Initialize it:
  ```
  terraform init
  ```
2. Run the script:
  ```
  ./terraform_import_20220331-19-12-33.sh
  ```
  Output:
  ```
  module.examples-projects-PROJECT_ID-ComputeInstance-us-central1-a.google_compute_instance.instance_1:
  Importing from ID
  "projects/PROJECT_ID/zones/us-central1-a/instances/instance-1"...
  module.examples-projects-PROJECT_ID-ComputeInstance-us-central1-a.google_compute_instance.instance_1:
  Import prepared!
   Prepared google_compute_instance for import
  module.examples-projects-PROJECT_ID-ComputeInstance-us-central1-a.google_compute_instance.instance_1:
  Refreshing state...
  [id=projects/PROJECT_ID/zones/us-central1-a/instances/instance-1]
  Import successful!
  The resources that were imported are shown above. These resources are now in
  your Terraform state and will henceforth be managed by Terraform.
  ```

## Next steps

- [Store state in a Cloud Storage
  bucket](https://cloud.google.com/docs/terraform/resource-management/store-state).

   Was this helpful?

---

# Managing infrastructure as code with Terraform,Cloud Build,and GitOpsStay organized with collectionsSave and categorize content based on your preferences.

# Managing infrastructure as code with Terraform,Cloud Build,and GitOpsStay organized with collectionsSave and categorize content based on your preferences.

This tutorial explains how to manage infrastructure as code with
[Terraform](https://cloud.google.com/docs/terraform)
and
[Cloud Build](https://cloud.google.com/build)
using the popular GitOps methodology. The term *GitOps* was
[first coined by Weaveworks](https://web.archive.org/web/20240202145840/https://www.weave.works/blog/gitops-operations-by-pull-request),
and its key concept is using a Git repository to store the environment
state that you want. Terraform is a
[HashiCorp](https://www.hashicorp.com/)
tool that enables you to predictably create, change, and improve
your cloud infrastructure by using code. In this tutorial, you use
[Cloud Build](https://cloud.google.com/build)
(a Google Cloud continuous integration service) to automatically
apply Terraform manifests to your environment.

This tutorial is for developers and operators who are looking for an elegant
strategy to predictably make changes to infrastructure. The article assumes you
are familiar with Google Cloud, Linux, and GitHub.

The [State of DevOps](https://cloud.google.com/devops/)
reports identified capabilities that drive software delivery performance. This
tutorial will help you with the following capabilities:

- [Version control](https://dora.dev/devops-capabilities/technical/version-control/)
- [Continuous integration](https://dora.dev/devops-capabilities/technical/continuous-integration/)
- [Continuous delivery](https://dora.dev/devops-capabilities/technical/continuous-delivery/)
- [Continuous testing](https://dora.dev/devops-capabilities/technical/test-automation/)

## Architecture

To demonstrate how this tutorial applies GitOps practices for managing
Terraform executions, consider the following architecture diagram. Note that it
uses GitHub branches—`dev` and `prod`—to represent actual environments. These
environments are defined by Virtual Private Cloud (VPC) networks—`dev` and
`prod`, respectively—into a Google Cloud project.

![Infrastructure with dev and prod environments.](https://cloud.google.com/static/docs/terraform/images/managing-infrastructure-as-code-infrastructure.svg)

The process starts when you push Terraform code to either the `dev` or `prod`
branch. In this scenario, Cloud Build triggers and then applies
Terraform manifests to achieve the state you want in the respective environment.
On the other hand, when you push Terraform code to any other branch—for example,
to a feature branch—Cloud Build runs to execute `terraform plan`, but
nothing is applied to any environment.

Ideally, either developers or operators must make infrastructure proposals to
[non-protected branches](https://help.github.com/en/articles/about-protected-branches)
and then submit them through
[pull requests](https://help.github.com/en/articles/about-pull-requests).
The
[Cloud Build GitHub app](https://github.com/marketplace/google-cloud-build),
discussed later in this tutorial, automatically triggers the build jobs and
links the `terraform plan` reports to these pull requests. This way, you can
discuss and review the potential changes with collaborators and add follow-up
commits before changes are merged into the base branch.

If no concerns are raised, you must first merge the changes to the `dev`
branch. This merge triggers an infrastructure deployment to the `dev`
environment, allowing you to test this environment. After you have tested and
are confident about what was deployed, you must merge the `dev` branch into the
`prod` branch to trigger the infrastructure installation to the production
environment.

## Objectives

- Set up your GitHub repository.
- Configure Terraform to store state in a Cloud Storage bucket.
- Grant permissions to your Cloud Build service account.
- Connect Cloud Build to your GitHub repository.
- Change your environment configuration in a feature branch.
- Promote changes to the development environment.
- Promote changes to the production environment.

## Costs

In this document, you use the following billable components of Google Cloud:

- [Cloud Build](https://cloud.google.com/build/pricing)
- [Cloud Storage](https://cloud.google.com/storage/pricing)
- [Compute Engine](https://cloud.google.com/compute/pricing)

To generate a cost estimate based on your projected usage,
      use the [pricing calculator](https://cloud.google.com/products/calculator).

      New Google Cloud users might be eligible for a [free trial](https://cloud.google.com/free).

When you finish the tasks that are described in this document, you can avoid
   continued billing by deleting the resources that you created. For more information, see
[Clean up](#clean-up).

## Prerequisites

1. In the Google Cloud console, activate Cloud Shell.
  [Activate Cloud Shell](https://console.cloud.google.com/?cloudshell=true)
  At the bottom of the Google Cloud console, a
        [Cloud Shell](https://cloud.google.com/shell/docs/how-cloud-shell-works)
        session starts and displays a command-line prompt. Cloud Shell is a shell environment
        with the Google Cloud CLI
        already installed and with values already set for
        your current project. It can take a few seconds for the session to initialize.
2. In Cloud Shell, get the ID of the project you just selected:
  ```
  gcloud config get-value project
  ```
  If this command doesn't return the project ID, configure Cloud Shell to
  use your project. Replace `PROJECT_ID` with your project
  ID.
  ```
  gcloud config set project PROJECT_ID
  ```
3. Enable the required APIs:
  ```
  gcloud services enable cloudbuild.googleapis.com compute.googleapis.com
  ```
  This step might take a few minutes to finish.
4. If you've never used Git in Cloud Shell, configure it with your
  name and email address:
  ```
  git config --global user.email "YOUR_EMAIL_ADDRESS"
  git config --global user.name "YOUR_NAME"
  ```
  Git uses this information to identify you as the author of the commits that you
  create in Cloud Shell.

## Setting up your GitHub repository

In this tutorial, you use a single Git repository to define your cloud
infrastructure. You orchestrate this infrastructure by having different
branches corresponding to different environments:

- The `dev` branch contains the latest changes that are applied to the
  development environment.
- The `prod` branch contains the latest changes that are applied to the
  production environment.

With this infrastructure, you can always reference the repository to know what
configuration is expected in each environment and to propose new changes by
first merging them into the `dev` environment. You then promote the changes by
merging the `dev` branch into the subsequent `prod` branch.

To get started, you fork the
[solutions-terraform-cloudbuild-gitops](https://github.com/GoogleCloudPlatform/solutions-terraform-cloudbuild-gitops.git)
repository.

1. On GitHub, navigate to
  [https://github.com/GoogleCloudPlatform/solutions-terraform-cloudbuild-gitops.git](https://github.com/GoogleCloudPlatform/solutions-terraform-cloudbuild-gitops.git).
2. In the top-right corner of the page, click **Fork**.
  ![Forking a repository.](https://cloud.google.com/static/docs/terraform/images/managing-infrastructure-as-code-fork-repository.png)
  Now you have a copy of the `solutions-terraform-cloudbuild-gitops`
  repository with source files.

1. In Cloud Shell, clone this forked repository, replacing
  `YOUR_GITHUB_USERNAME` with your GitHub username:
  ```
  cd ~
  git clone https://github.com/YOUR_GITHUB_USERNAME/solutions-terraform-cloudbuild-gitops.git
  cd ~/solutions-terraform-cloudbuild-gitops
  ```

The code in this repository is structured as follows:

- The `environments/` folder contains subfolders that represent environments,
  such as `dev` and `prod`, which provide logical separation between workloads
  at different stages of maturity, development and production, respectively.
  Although it's a good practice to have these environments as similar as
  possible, each subfolder has its own Terraform configuration to ensure they
  can have unique settings as necessary.
- The `modules/` folder contains inline Terraform modules. These modules
  represent logical groupings of related resources and are used to share code
  across different environments.
- The `cloudbuild.yaml` file is a build configuration file that contains
  instructions for Cloud Build, such as how to perform tasks based
  on a set of steps. This file specifies a conditional execution depending on
  the branch Cloud Build is fetching the code from, for example:
  - For `dev` and `prod` branches, the following steps are executed:
    1. `terraform init`
    2. `terraform plan`
    3. `terraform apply`
  - For any other branch, the following steps are executed:
    1. `terraform init` for all `environments` subfolders
    2. `terraform plan` for all `environments` subfolders

To ensure that the changes being proposed are appropriate for every environment,
`terraform init` and `terraform plan` are run for all `environments`
subfolders. Before merging the pull request, you can review the plans
to make sure that access isn't being granted to an unauthorized entity, for
example.

## Configuring Terraform to store state in a Cloud Storage bucket

By default, Terraform stores
[state](https://www.terraform.io/docs/state/)
locally in a file named `terraform.tfstate`. This default  configuration can
make Terraform usage difficult for teams, especially when many users run
Terraform at the same time and each machine has its own understanding of the
current infrastructure.

To help you avoid such issues, this section configures a
[remote state](https://www.terraform.io/docs/state/remote.html)
that points to a Cloud Storage bucket. Remote state is a feature of
[backends](https://www.terraform.io/docs/backends)
and, in this tutorial, is configured in the `backend.tf` files—for example:

```
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

terraform {
  backend "gcs" {
    bucket = "PROJECT_ID-tfstate"
    prefix = "env/dev"
  }
}
```

In the following steps, you create a Cloud Storage bucket and change a
few files to point to your new bucket and your Google Cloud project.

1. In Cloud Shell, create the Cloud Storage bucket:
  ```
  PROJECT_ID=$(gcloud config get-value project)
  gcloud storage buckets create gs://${PROJECT_ID}-tfstate
  ```
  1.  Enable
      [Object Versioning](https://cloud.google.com/storage/docs/object-versioning)
      to keep the history of your deployments:
  ```
  ```sh
  gcloud storage buckets update gs://${PROJECT_ID}-tfstate --versioning
  ```
  Enabling Object Versioning increases
  [storage costs](https://cloud.google.com/storage/pricing){: track-type="tutorial" track-name="internalLink" track-metadata-position="body" },
  which you can mitigate by configuring
  [Object Lifecycle Management](/storage/docs/lifecycle){: track-type="tutorial" track-name="internalLink" track-metadata-position="body" }
  to delete old state versions.
  ```
  1. Replace the `PROJECT_ID` placeholder with the project
    ID in both the `terraform.tfvars` and `backend.tf` files:
    ```
    cd ~/solutions-terraform-cloudbuild-gitops
    sed -i s/PROJECT_ID/$PROJECT_ID/g environments/*/terraform.tfvars
    sed -i s/PROJECT_ID/$PROJECT_ID/g environments/*/backend.tf
    ```
    On OS X/MacOS, you might need to add two quotation marks (`""`) after
    `sed -i`, as follows:
    ```
    cd ~/solutions-terraform-cloudbuild-gitops
    sed -i "" s/PROJECT_ID/$PROJECT_ID/g environments/*/terraform.tfvars
    sed -i "" s/PROJECT_ID/$PROJECT_ID/g environments/*/backend.tf
    ```
  2. Check whether all files were updated:
    ```
    git status
    ```
    The output looks like this:
    ```
    On branch dev
    Your branch is up-to-date with 'origin/dev'.
    Changes not staged for commit:
     (use "git add <file>..." to update what will be committed)
     (use "git checkout -- <file>..." to discard changes in working directory)
           modified:   environments/dev/backend.tf
           modified:   environments/dev/terraform.tfvars
           modified:   environments/prod/backend.tf
           modified:   environments/prod/terraform.tfvars
    no changes added to commit (use "git add" and/or "git commit -a")
    ```
  3. Commit and push your changes:
    ```
    git add --all
    git commit -m "Update project IDs and buckets"
    git push origin dev
    ```
    Depending on your GitHub configuration, you will have to authenticate to
    push the preceding changes.
  ## Granting permissions to your Cloud Build service account
  To allow
  [Cloud Build service account](https://cloud.google.com/build/docs/securing-builds/set-service-account-permissions)
  to run Terraform scripts with the goal of managing Google Cloud resources,
  you need to grant it appropriate access to your project. For simplicity,
  [project editor](https://cloud.google.com/iam/docs/understanding-roles#basic)
  access is granted in this tutorial. But when the project editor role has a
  wide-range permission, in production environments you must follow your company's
  IT security best practices, usually providing
  least-privileged access. For security best practices, see
  [Verify every access attempt explicitly](https://cloud.google.com/architecture/framework/security/implement-zero-trust#verify_every_access_attempt_explicitly).
  1. In Cloud Shell, retrieve the email for your project's
    Cloud Build service account:
    ```
    CLOUDBUILD_SA="$(gcloud projects describe $PROJECT_ID \
        --format 'value(projectNumber)')@cloudbuild.gserviceaccount.com"
    ```
  2. Grant the required access to your Cloud Build service account:
    ```
    gcloud projects add-iam-policy-binding $PROJECT_ID \
        --member serviceAccount:$CLOUDBUILD_SA --role roles/editor
    ```
  ## Directly connecting Cloud Build to your GitHub repository
  This section shows you how to install the
  [Cloud Build GitHub app](https://github.com/marketplace/google-cloud-build).
  This installation allows you to connect your GitHub repository with your
  Google Cloud project so that Cloud Build can automatically apply
  your Terraform manifests each time you create a new branch or push code to
  GitHub.
  The following steps provide instructions for installing the app only for the
  `solutions-terraform-cloudbuild-gitops` repository, but you can choose to
  install the app for more or all of your repositories.
  1. Go to the GitHub Marketplace page for the Cloud Build
    app:
    [Open the Cloud Build app page](https://github.com/marketplace/google-cloud-build)
    - If this is your first time configuring an app in GitHub: Click **Setup
      with Google Cloud Build** at the bottom of the page. Then click **Grant
      this app access to your GitHub account**.
    - If this is not the first time configuring an app in GitHub: Click
      **Configure access**. The **Applications** page of your personal
      account opens.
  2. Click **Configure** in the Cloud Build row.
  3. Select **Only select repositories**, then select
    **solutions-terraform-cloudbuild-gitops** to connect to the repository.
  4. Click **Save** or **Install**—the button label changes depending on
    your workflow. You are redirected to Google Cloud to continue the
    installation.
  5. Sign in with your Google Cloud account. If requested, authorize
    Cloud Build integration with GitHub.
  6. On the **Cloud Build** page, select your project. A
    wizard appears.
  7. In the **Select repository** section, select your GitHub account and the
    **solutions-terraform-cloudbuild-gitops** repository.
  8. If you agree with the terms and conditions, select the checkbox, then click
    **Connect**.
  9. In the **Create a trigger** section, click **Create a trigger**:
    1. Add a trigger name, such as `push-to-branch`. Note this trigger name
      because you will need it later.
    2. In the **Event** section, select **Push to a branch**.
    3. In the **Source** section, select `.*` in the **Branch** field.
    4. Click **Create**.
  The Cloud Build GitHub app is now configured, and your GitHub
  repository is linked to your Google Cloud project. From now on, changes to
  the GitHub repository trigger Cloud Build executions, which report
  the results back to GitHub by using
  [GitHub Checks](https://developer.github.com/v3/checks/).
  ## Changing your environment configuration in a new feature branch
  By now, you have most of your environment configured. So it's time to make some
  code changes in your development environment.
  1. On GitHub, navigate to the main page of your forked repository.
    ```
    https://github.com/YOUR_GITHUB_USERNAME/solutions-terraform-cloudbuild-gitops
    ```
  2. Make sure you are in the `dev` branch.
  3. To open the file for editing, go to the `modules/firewall/main.tf` file and
    click the pencil icon.
  4. On line 30, fix the `"http-server2"` typo in `target_tags` field.
    The value must be `"http-server"`.
  5. Add a commit message at the bottom of the page, such as "Fixing http
    firewall target", and select **Create a new branch for this commit and
    start a pull request**.
  6. Click **Propose changes**.
  7. On the following page, click **Create pull request** to open a new pull
    request with your change.
    After your pull request is open, a Cloud Build job is
    automatically initiated.
  8. Click **Show all checks** and wait for the check to become green.
    ![Show all checks in a pull request.](https://cloud.google.com/static/docs/terraform/images/managing-infrastructure-as-code-all-checks.png)
  9. Click **Details** to see more information, including the output of the
    `terraform plan` at **View more details on Google Cloud Build** link.
  Don't merge your pull request yet.
  Note that the Cloud Build job ran the pipeline defined in the
  `cloudbuild.yaml` file. As discussed previously, this pipeline has different
  behaviors depending on the branch being fetched. The build checks whether the
  `$BRANCH_NAME` variable matches any environment folder. If so,
  Cloud Build executes `terraform plan` for that environment.
  Otherwise, Cloud Build executes `terraform plan` for all environments
  to make sure that the proposed change is appropriate for all of them. If any of
  these plans fail to execute, the build fails.
  ```
  - id: 'tf plan'
    name: 'hashicorp/terraform:1.0.0'
    entrypoint: 'sh'
    args:
    - '-c'
    - |
        if [ -d "environments/$BRANCH_NAME/" ]; then
          cd environments/$BRANCH_NAME
          terraform plan
        else
          for dir in environments/*/
          do
            cd ${dir}
            env=${dir%*/}
            env=${env#*/}
            echo ""
            echo "*************** TERRAFORM PLAN ******************"
            echo "******* At environment: ${env} ********"
            echo "*************************************************"
            terraform plan || exit 1
            cd ../../
          done
        fi
  ```
  Similarly, the `terraform apply` command runs for environment branches, but it
  is completely ignored in any other case. In this section, you have submitted a
  code change to a new branch, so no infrastructure deployments were applied to
  your Google Cloud project.
  ```
  - id: 'tf apply'
    name: 'hashicorp/terraform:1.0.0'
    entrypoint: 'sh'
    args:
    - '-c'
    - |
        if [ -d "environments/$BRANCH_NAME/" ]; then
          cd environments/$BRANCH_NAME
          terraform apply -auto-approve
        else
          echo "***************************** SKIPPING APPLYING *******************************"
          echo "Branch '$BRANCH_NAME' does not represent an official environment."
          echo "*******************************************************************************"
        fi
  ```
  ## Enforcing Cloud Build execution success before merging branches
  To make sure merges can be applied only when respective Cloud Build
  executions are successful, proceed with the following steps:
  1. On GitHub, navigate to the main page of your forked repository.
    ```
    https://github.com/YOUR_GITHUB_USERNAME/solutions-terraform-cloudbuild-gitops
    ```
  2. Under your repository name, click **Settings**.
  3. In the left menu, click **Branches**.
  4. Under **Branch protection rules**, click **Add rule**.
  5. In **Branch name pattern**, type `dev`.
  6. In the **Protect matching branches** section, select **Require status
    checks to pass before merging**.
  7. Search for your Cloud Build trigger name created previously.
  8. Click **Create**.
  9. Repeat steps 3–7, setting **Branch name pattern** to `prod`.
  This configuration is important to
  [protect](https://help.github.com/en/articles/about-protected-branches)
  both the `dev` and `prod` branches. Meaning, commits must first be pushed to
  another branch, and only then they can be merged to the protected branch. In
  this tutorial, the protection requires that the Cloud Build execution
  be successful for the merge to be allowed.
  ## Promoting changes to the development environment
  You have a pull request waiting to be merged. It's time to apply the state you
  want to your `dev` environment.
  1. On GitHub, navigate to the main page of your forked repository.
    ```
    https://github.com/YOUR_GITHUB_USERNAME/solutions-terraform-cloudbuild-gitops
    ```
  2. Under your repository name, click **Pull requests**.
  3. Click the pull request you just created.
  4. Click **Merge pull request**, and then click **Confirm merge**.
    ![Confirm merge.](https://cloud.google.com/static/docs/terraform/images/managing-infrastructure-as-code-confirm-merge.png)
  5. Check that a new Cloud Build has been triggered:
    [Go to the Cloud Build page](https://console.cloud.google.com/cloud-build/builds)
  6. Open the build and check the logs.
    When the build finishes, you see something like this:
    ```
    Step #3 - "tf apply": external_ip = EXTERNAL_IP_VALUE
    Step #3 - "tf apply": firewall_rule = dev-allow-http
    Step #3 - "tf apply": instance_name = dev-apache2-instance
    Step #3 - "tf apply": network = dev
    Step #3 - "tf apply": subnet = dev-subnet-01
    ```
  7. Copy `EXTERNAL_IP_VALUE` and open the address in a web
    browser.
    ```
    http://EXTERNAL_IP_VALUE
    ```
    This provisioning might take a few seconds to boot the VM and to propagate
    the firewall rule. Eventually, you see **Environment: dev** in the
    web browser.
  8. Navigate to your Terraform state file in your Cloud Storage bucket.
    ```
    https://storage.cloud.google.com/PROJECT_ID-tfstate/env/dev/default.tfstate
    ```
  ## Promoting changes to the production environment
  Now that you have your development environment fully tested, you can promote
  your infrastructure code to production.
  1. On GitHub, navigate to the main page of your forked repository.
    ```
    https://github.com/YOUR_GITHUB_USERNAME/solutions-terraform-cloudbuild-gitops
    ```
  2. Under your repository name, click **Pull requests**.
  3. Click **New pull request**.
  4. For the **base repository**, select your just-forked repository.
  5. For **base**, select `prod` from your own base repository. For
    **compare**, select `dev`.
    ![Compare changes.](https://cloud.google.com/static/docs/terraform/images/managing-infrastructure-as-code-compare-changes.png)
  6. Click **Create pull request**.
  7. For **title**, enter a title such as `Promoting networking changes`, and
    then click **Create pull request**.
  8. Review the proposed changes, including the `terraform plan` details from
    Cloud Build, and then click **Merge pull request**.
  9. Click **Confirm merge**.
  10. In the Google Cloud console, open the **Build History** page to see
    your changes being applied to the production environment:
    [Go to the Cloud Build page](https://console.cloud.google.com/cloud-build/builds)
  11. Wait for the build to finish, and then check the logs.
    At the end of the logs, you see something like this:
    ```
    Step #3 - "tf apply": external_ip = EXTERNAL_IP_VALUE
    Step #3 - "tf apply": firewall_rule = prod-allow-http
    Step #3 - "tf apply": instance_name = prod-apache2-instance
    Step #3 - "tf apply": network = prod
    Step #3 - "tf apply": subnet = prod-subnet-01
    ```
  12. Copy `EXTERNAL_IP_VALUE` and open the address in a web
    browser.
    ```
    http://EXTERNAL_IP_VALUE
    ```
    This provisioning might take a few seconds to boot the VM and to propagate
    the firewall rule. Eventually, you see **Environment: prod** in the
    web browser.
  13. Navigate to your Terraform state file in your Cloud Storage bucket.
    ```
    https://storage.cloud.google.com/PROJECT_ID-tfstate/env/prod/default.tfstate
    ```
  You have successfully configured a serverless infrastructure-as-code pipeline on
  Cloud Build. In the future, you might want to try the following:
  - Add deployments for separate use cases.
  - Create additional environments to reflect your needs.
  - Use a project per environment instead of a VPC per environment.
  ## Cleanup
  After you've finished the tutorial, clean up the resources you created on
  Google Cloud so you won't be billed for them in the future.
  ### Deleting the project
  1. In the Google Cloud console, go to the **Manage resources** page.
    [Go to Manage resources](https://console.cloud.google.com/iam-admin/projects)
  2. In the project list, select the project that you
        want to delete, and then click **Delete**.
  3. In the dialog, type the project ID, and then click
        **Shut down** to delete the project.
  ### Deleting the GitHub repository
  To avoid blocking new pull requests on your GitHub repository, you can delete
  your branch protection rules:
  1. In GitHub, navigate to the main page of your forked repository.
  2. Under your repository name, click **Settings**.
  3. In the left menu, click **Branches**.
  4. Under the **Branch protection rules** section, click the **Delete** button
    for both `dev` and `prod` rows.
  Optionally, you can completely uninstall the Cloud Build app from
  GitHub:
  1. Go to your GitHub **Applications** settings.
    [Go to the GitHub applications page](https://github.com/settings/installations)
  2. In the **Installed GitHub Apps** tab, click **Configure** in the
    **Cloud Build** row. Then, in the **Danger zone** section,
    click the **Uninstall** button in the **Uninstall Google Cloud Builder**
    row.
    At the top of the page, you see a message saying "You're all set. A job
       has been queued to uninstall Google Cloud Build."
  3. In the **Authorized GitHub Apps** tab, click the **Revoke** button in the
    **Google Cloud Build** row, then **I understand, revoke access** in the
    popup.
  If you don't want to keep your GitHub repository:
  1. In GitHub, go to the main page of your forked repository.
  2. Under your repository name, click **Settings**.
  3. Scroll down to the **Danger Zone**.
  4. Click **Delete this repository**, and follow the confirmation steps.
  ## What's next
  - Consider using
    [Cloud Foundation Toolkit templates](https://cloud.google.com/foundation-toolkit)
    to quickly build a repeatable enterprise-ready foundation in
    Google Cloud.
  - Watch
    [Repeatable Google Cloud Environments at Scale With Cloud Build Infra-As-Code Pipelines](https://www.youtube.com/watch?v=3vfXQxWJazM)
    from Next' 19 about the GitOps workflow described in this tutorial.
  - Check out the
    [GitOps-style continuous delivery with Cloud Build](https://cloud.google.com/kubernetes-engine/docs/tutorials/gitops-cloud-build)
    tutorial.
  - Take a look at more advanced Cloud Build features:
    [Configuring the order of build steps](https://cloud.google.com/build/docs/configuring-builds/configure-build-step-order),
    [Building, testing, and deploying artifacts](https://cloud.google.com/build/docs/configuring-builds/build-test-deploy-artifacts),
    and
    [Creating custom build steps](https://cloud.google.com/build/docs/create-custom-build-steps).
  - Check out the blog on [Ensuring scale and compliance of your Terraform Deployment with Cloud Build](https://cloud.google.com/blog/products/devops-sre/terraform-gitops-with-google-cloud-build-and-storage).
  - Read our resources about
    [DevOps](https://cloud.google.com/devops/).
  - Learn more about the DevOps capabilities related to this tutorial:
    - [Version control](https://cloud.google.com/solutions/devops/devops-tech-version-control)
    - [Continuous integration](https://cloud.google.com/solutions/devops/devops-tech-continuous-integration)
    - [Continuous delivery](https://cloud.google.com/solutions/devops/devops-tech-continuous-delivery)
    - [Continuous testing](https://cloud.google.com/solutions/devops/devops-tech-test-automation)
  - Take the
    [DevOps quick check](https://dora.dev/quickcheck/)
    to understand where you stand in comparison with the rest of the industry.
