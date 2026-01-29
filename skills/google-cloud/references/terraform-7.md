# Store Terraform state in a Cloud Storage bucketStay organized with collectionsSave and categorize content based on your preferences. and more

# Store Terraform state in a Cloud Storage bucketStay organized with collectionsSave and categorize content based on your preferences.

> This tutorial explains how to store Terraform state in a Cloud Storage bucket

# Store Terraform state in a Cloud Storage bucketStay organized with collectionsSave and categorize content based on your preferences.

In this tutorial, you learn how to store Terraform state in a Cloud Storage
bucket.

By default, Terraform stores [state](https://www.terraform.io/docs/state/)
locally in a file named `terraform.tfstate`. This default configuration can
make Terraform usage difficult for teams when multiple users run Terraform at
the same time and each machine has its own understanding of the current
infrastructure.

To help you avoid such issues, this page shows you how to configure a
[remote state](https://www.terraform.io/docs/state/remote.html) that points to a
Cloud Storage bucket. Remote state is a feature of
[Terraform backends](https://www.terraform.io/docs/backends).

## Objectives

This tutorial shows you how to do the following:

- Use Terraform to provision a Cloud Storage bucket to store
  Terraform state.
- Add templating in the Terraform configuration file to migrate the state from
  the local backend to the Cloud Storage bucket.

## Costs

In this document, you use the following billable components of Google Cloud:

- [Cloud Storage](https://cloud.google.com/storage/all-pricing)

To generate a cost estimate based on your projected usage,
      use the [pricing calculator](https://cloud.google.com/products/calculator).

      New Google Cloud users might be eligible for a [free trial](https://cloud.google.com/free).

When you finish the tasks that are described in this document, you can avoid
   continued billing by deleting the resources that you created. For more information, see
[Clean up](#clean-up).

Cloud Storage incurs costs for storage, read and write operations,
network egress, and replication.

The Cloud Storage bucket in this tutorial has [Object
Versioning](https://cloud.google.com/storage/docs/object-versioning) enabled to keep the history of your
deployments. Enabling Object Versioning increases storage costs, which you can
mitigate by configuring [Object Lifecycle Management](https://cloud.google.com/storage/docs/lifecycle)
to delete old state versions.

## Before you begin

1. In the Google Cloud console, activate Cloud Shell.
  [Activate Cloud Shell](https://console.cloud.google.com/?cloudshell=true)
  Cloud Shell is preinstalled with Terraform.
2. If you're using a local shell, perform the following steps:
  - [Install Terraform](https://developer.hashicorp.com/terraform/tutorials/gcp-get-started/install-cli).
  - Create local authentication credentials for your user account:
    ```
    gcloud auth application-default login
    ```
    If an authentication error is returned, and you are using an external identity provider
            (IdP), confirm that you have
            [signed in to the gcloud CLI with your federated identity](https://cloud.google.com/iam/docs/workforce-log-in-gcloud).
3. [Create or select a Google Cloud project](https://cloud.google.com/resource-manager/docs/creating-managing-projects).
  - **Select a project**: Selecting a project doesn't require a specific
          IAM role—you can select any project that you've been
          granted a role on.
  - **Create a project**: To create a project, you need the Project Creator role
          (`roles/resourcemanager.projectCreator`), which contains the
          `resourcemanager.projects.create` permission. [Learn how to grant
          roles](https://cloud.google.com/iam/docs/granting-changing-revoking-access).
  - Create a Google Cloud project:
    ```
    gcloud projects create PROJECT_ID
    ```
    Replace `PROJECT_ID` with a name for the Google Cloud project you are creating.
  - Select the Google Cloud project that you created:
    ```
    gcloud config set project PROJECT_ID
    ```
    Replace `PROJECT_ID` with your Google Cloud project name.
4. [Verify that billing is enabled for your Google Cloud project](https://cloud.google.com/billing/docs/how-to/verify-billing-enabled#confirm_billing_is_enabled_on_a_project).
5. Enable the Cloud Storage API:
  To enable APIs, you need the Service Usage Admin IAM
        role (`roles/serviceusage.serviceUsageAdmin`), which contains the
        `serviceusage.services.enable` permission. [Learn how to grant
        roles](https://cloud.google.com/iam/docs/granting-changing-revoking-access).
  ```
  gcloud services enable storage.googleapis.com
  ```
6. Grant roles to your user account. Run the following command once for each of the following
            IAM roles:
            `roles/storage.admin`
  ```
  gcloud projects add-iam-policy-binding PROJECT_ID --member="user:USER_IDENTIFIER" --role=ROLE
  ```
  Replace the following:
  - `PROJECT_ID`: Your project ID.
  - `USER_IDENTIFIER`: The identifier for your user
                account. For examples, see
                [Represent workforce pool users in IAM policies](https://cloud.google.com/iam/docs/workforce-identity-federation#representing-workforce-users).
  - `ROLE`: The IAM role that you grant to your user account.
  Alternately, you can create a
  [custom IAM role](https://cloud.google.com/iam/docs/roles-overview#custom) that contains
  the following permissions:
  - `storage.buckets.create`
  - `storage.buckets.list`
  - `storage.objects.get`
  - `storage.objects.create`
  - `storage.objects.delete`
  - `storage.objects.update`
  As a best practice, we recommend that access to the bucket and the state
  files stored there is controlled. Only a small set of users (for example,
  the main cloud administrator and the person acting as the alternative or
  backup administrator) should have admin permissions for the bucket. The
  other developers should have permissions to only write and read objects in
  the bucket.

## Prepare the environment

1. Clone the GitHub repository containing Terraform samples:
  ```
  git clone https://github.com/terraform-google-modules/terraform-docs-samples.git --single-branch
  ```
2. Change to the working directory:
  ```
  cd terraform-docs-samples/storage/remote_terraform_backend_template
  ```

## Review the Terraform files

1. Review the `main.tf` file:
  ```
  cat main.tf
  ```
  The output is similar to the following
  ```
  resource "random_id" "default" {
    byte_length = 8
  }
  resource "google_storage_bucket" "default" {
    name     = "${random_id.default.hex}-terraform-remote-backend"
    location = "US"
    force_destroy               = false
    public_access_prevention    = "enforced"
    uniform_bucket_level_access = true
    versioning {
      enabled = true
    }
  }
  resource "local_file" "default" {
    file_permission = "0644"
    filename        = "${path.module}/backend.tf"
    # You can store the template in a file and use the templatefile function for
    # more modularity, if you prefer, instead of storing the template inline as
    # we do here.
    content = <<-EOT
    terraform {
      backend "gcs" {
        bucket = "${google_storage_bucket.default.name}"
      }
    }
    EOT
  }
  ```
  This file describes the following resources:
  - `random_id`: This is appended to the Cloud Storage bucket name to
    ensure a unique name for the Cloud Storage bucket.
  - `google_storage_bucket`: The Cloud Storage bucket to store
    the state file. This bucket is configured to have the following
    properties:
    - `force_destroy` is set to `false` to ensure that the bucket is not
      deleted if there are objects in it. This ensures that the state
      information in the bucket isn't accidentally deleted.
    - `public_access_prevention` is set to `enforced` to make sure the
      bucket contents aren't accidentally exposed to the public.
    - `uniform_bucket_level_access` is set to `true` to allow controlling
      access to the bucket and its contents using
      [IAM permissions instead of access control lists](https://cloud.google.com/storage/docs/uniform-bucket-level-access).
    - `versioning` is enabled to ensure that earlier versions of the state
      are preserved in the bucket.
  - `local_file`: A local file. The contents of this file instructs Terraform
    to use Cloud Storage bucket as the remote backend once the
    bucket is created.

## Provision the Cloud Storage bucket

1. Initialize Terraform:
  ```
  terraform init
  ```
  When you run `terraform init` for the first time, the Cloud Storage
  bucket that you specified in the `main.tf` file doesn't exist yet, so
  Terraform initializes a local backend to store state in the local
  file system.
2. Apply the configuration to provision resources described in the `main.tf`
  file:
  ```
  terraform apply
  ```
  When prompted, enter `yes`.
  When you run `terraform apply` for the first time, Terraform provisions the
  Cloud Storage bucket for storing the state. It also creates a local
  file; the contents of this file instruct Terraform to use the
  Cloud Storage bucket as the remote backend to store state.

## Migrate state to Cloud Storage bucket

1. Migrate Terraform state to the remote Cloud Storage backend:
  ```
  terraform init -migrate-state
  ```
  Terraform detects that you already have a state file locally and prompts you
  to migrate the state to the new Cloud Storage bucket. When prompted,
  enter `yes`.

After running this command, your Terraform state is stored in the
Cloud Storage bucket. Terraform pulls the latest state from this bucket
before running a command, and pushes the latest state to the bucket after
running a command.

## Clean up

To avoid incurring charges to your Google Cloud account for the resources used in this
        tutorial, either delete the project that contains the resources, or keep the project and
        delete the individual resources.

### Delete the project

To avoid incurring charges to your Google Cloud account for the resources
used on this page, follow these steps.

1. Open the `main.tf` file.
2. In the `google_storage_bucket.default` resource, update the value of
  `force_destroy` to `true`.
3. Apply the updated configuration:
  ```
  terraform apply
  ```
  When prompted, enter `yes`.
4. Delete the state file:
  ```
  rm backend.tf
  ```
5. Reconfigure the backend to be local:
  ```
  terraform init -migrate-state
  ```
  When prompted, enter `yes`.
6. Run the following command to delete the Terraform resources:
  ```
  terraform destroy
  ```
  When prompted, enter `yes`.

## What's next

- Learn how to [manage infrastructure as code with Terraform, Cloud Build, and GitOps](https://cloud.google.com/docs/terraform/resource-management/managing-infrastructure-as-code)
- [Learn about policy validation](https://cloud.google.com/docs/terraform/policy-validation).

---

# ResourcesStay organized with collectionsSave and categorize content based on your preferences.

# ResourcesStay organized with collectionsSave and categorize content based on your preferences.

- [Details about documentation updates for Terraform on Google Cloud.](https://cloud.google.com/docs/terraform/release-notes)
- [How to get additional help with Terraform on Google Cloud.](https://cloud.google.com/docs/terraform/getting-support)

---

# Overview of Terraform on Google CloudStay organized with collectionsSave and categorize content based on your preferences.

# Overview of Terraform on Google CloudStay organized with collectionsSave and categorize content based on your preferences.

Hashicorp Terraform is an Infrastructure as code (IaC) tool that lets you
provision and manage cloud infrastructure. Terraform provides plugins called
*providers* that lets you interact with cloud providers and other
APIs. You can use the *Terraform provider for Google Cloud* to
provision and manage Google Cloud infrastructure.

## Benefits of using Terraform

This section explains some of the benefits of using Terraform to provision and
manage Google Cloud infrastructure:

- Terraform is the most commonly used tool to provision and automate
  Google Cloud infrastructure. You can use the
  [Google Cloud provider](https://registry.terraform.io/providers/hashicorp/google/latest/docs)
  to configure and manage all Google Cloud resources using the same
  declarative syntax and tooling.
- Terraform lets you specify your preferred end state for your infrastructure.
  You can then deploy the same configuration multiple times to create
  reproducible development, test, and production environments.
- Terraform lets you generate an execution plan that shows what Terraform will
  do when you apply your configuration. This lets you avoid any surprises when
  you modify your infrastructure through Terraform.
- Terraform lets you package and reuse common code in the form of
  [modules](https://registry.terraform.io/namespaces/terraform-google-modules).
  Modules present standard interfaces for creating cloud resources. They
  simplify projects by increasing readability and allow teams to organize
  infrastructure in readable blocks. Additionally, Google Cloud
  publishes a number of opinionated deployable modules as
  [blueprints](https://cloud.google.com/docs/terraform/blueprints/terraform-blueprints) and
  getting-started examples as [Jump Start
  Solutions](https://cloud.google.com/solutions?jump-start-solutions#section-3).
- Terraform records the current state of your infrastructure and lets you
  manage state effectively. The Terraform state file keeps track of all
  resources in a deployment.

## Using Terraform

Terraform has a declarative and configuration-oriented syntax, which you can use
to [author the infrastructure](https://developer.hashicorp.com/terraform/language)
that you want to provision. Using this syntax, you'll define your preferred
end-state for your infrastructure in a *Terraform configuration file*. You'll then
use the [Terraform CLI](https://cloud.google.com/docs/terraform/basic-commands) to provision
infrastructure based on the configuration file.

The following steps explain how Terraform works:

1. You describe the Google Cloud infrastructure you want to provision
  in a Terraform configuration file. You don't need to author code
  describing *how* to provision this configuration.
2. You run the `terraform plan` command, which evaluates your configuration
  and generates an execution plan. You can review the plan and make changes as
  needed.
3. Then, you run the `terraform apply` command, which performs the following
  actions:
  - It provisions your infrastructure based on your execution plan by invoking
    the corresponding Google Cloud APIs in the background.
  - It creates a *Terraform state file*, which is a JSON formatted mapping of
    resources in your configuration file to the resources in the
    real world infrastructure. Terraform uses this file to know the latest
    state of your infrastructure, and to determine when to create, update, and
    destroy resources.
4. Subsequently, when you run `terraform apply`, Terraform uses the mapping in
  the state file to compare the existing infrastructure to the code, and make
  updates as necessary:
  - If a resource object defined in the configuration file does not exist in
    the state file, Terraform creates it.
  - If a resource object exists in the state file, but has a different
    configuration from your configuration file, Terraform updates the
    resource to match your configuration file.
  - If a resource object in the state file matches your configuration
    file, Terraform leaves the resource unchanged.

## Google Cloud providers

There are two providers that let you provision and manage Google Cloud
infrastructure:

- `google`: Use this provider to provision and manage
  Google Cloud APIs.
- `google-beta`: Use this provider to provision and manage
  Google Cloud beta APIs.

For instructions on using these providers, see the
[Google Cloud provider configuration reference](https://registry.terraform.io/providers/hashicorp/google/latest/docs/guides/provider_reference).

`google` and `google-beta` providers are developed using a tool called
*Magic Modules*. Magic Modules allows contributors to make changes against a
single codebase and develop both `google` and `google-beta` providers
simultaneously.

You can contribute to the Google Cloud providers using Magic
Modules by following the instructions in the
[Magic Modules contribution guide](https://googlecloudplatform.github.io/magic-modules/get-started/generate-providers/).

## What's next

- Learn how to
  [create a basic web server on Compute Engine using Terraform](https://cloud.google.com/docs/terraform/get-started-with-terraform)
- Learn how to
  [store Terraform state in a Cloud Storage bucket](https://cloud.google.com/docs/terraform/resource-management/store-state)
- Look through the
  [Terraform modules and blueprints for Google Cloud](https://cloud.google.com/docs/terraform/blueprints/terraform-blueprints)
- Look through the various
  [Terraform for Google Cloud samples](https://cloud.google.com/docs/samples?language=terraform)

   Was this helpful?

---

# Understanding Google Cloud APIs and TerraformStay organized with collectionsSave and categorize content based on your preferences.

> Understanding Google Cloud APIs and Terraform

# Understanding Google Cloud APIs and TerraformStay organized with collectionsSave and categorize content based on your preferences.

This guide aims to clarify how Terraform interacts with Google Cloud APIs
(while differentiating between public and private APIs), and explain key concepts
like API enablement and resource import. This understanding is crucial for
effectively managing your Google Cloud resources with Terraform and avoiding
common pitfalls.

## Public versus private Google Cloud APIs

Google Cloud services expose various APIs that allow applications and tools
(like Terraform) to interact with and manage resources. These APIs broadly fall
into two categories:

### Public APIs

**Purpose:** These are the primary interfaces for customers and tools to create, configure, and manage Google Cloud resources (e.g., Compute Engine instances, Cloud Storage buckets, BigQuery datasets).

**Exposure:** Public APIs are well-documented, have defined REST endpoints, and are intended for external consumption. They are the APIs that the `google` Terraform provider is built to interact with.

**Examples:** `compute.googleapis.com`, `storage.googleapis.com`, `bigquery.googleapis.com`.

### Private (internal) APIs

**Purpose:** These APIs are internal to Google Cloud services, used by Google itself for the internal operation, orchestration, and provisioning of its managed services. They expose functionalities that are not meant for direct customer interaction or management.

**Exposure:** Private APIs are generally not publicly documented, don't have stable external endpoints, and are not designed for direct access by third-party tools like Terraform. They are an implementation detail of the service.

**Example:** `dataproc-control.googleapis.com` is an internal API that Dataproc uses for its operational control plane. Customers don't directly interact with or manage this API.

## API Enablement versus Resource Import in Terraform

Understanding the distinction between "enabling an API" and "importing a
resource" is fundamental to using Terraform effectively with Google Cloud.

### Enabling an API

- **What it means:** When you "enable an API" in Google Cloud, you are activating a specific Google Cloud service for your project. This grants your project the necessary permissions and access to use the functionalities of that service and create resources managed by it.

**Terraform context:** In Terraform, this is typically done using the `google_project_service` resource. This resource verifies that a specified public API (e.g., `compute.googleapis.com`) is enabled for your Google Cloud project.

**Purpose:** Enabling an API is a **prerequisite** for creating or managing resources that belong to that service. For example, you must enable `compute.googleapis.com` before you can create `google_compute_instance` resources.

**Example (Terraform):**

```
```hcl
resource "google_project_service" "compute_api" {
  project            = "your-gcp-project-id"
  service            = "compute.googleapis.com"
  disable_on_destroy = false
}
```
```

**Important Note:** The `google_project_service` resource is designed exclusively for managing the enablement state of **publicly accessible Google Cloud APIs**. It is not intended for, and won't work with, internal or private APIs. Attempting to use it for private APIs will result in errors, as those APIs are not exposed through the public API surface for such management.

### Importing a Resource

**What it means:** In Terraform, "importing" refers to bringing an **existing cloud resource** (one that was created manually or by another process outside of Terraform) under Terraform's management. When you import a resource, Terraform generates a state entry for it, allowing you to manage its lifecycle (updates, deletion) using your Terraform configuration.

**Terraform context:** This is achieved using the `terraform import` command, or by utilizing `import` blocks introduced in Terraform 1.5+.

**Purpose:** To gain control over resources that were not initially provisioned by Terraform.

**Example (Terraform CLI):**

```
```bash
terraform import google_compute_instance.my_instance projects/your-gcp-project-id/zones/us-central1-a/instances/my-vm
```
```

## Addressing Concerns about Private APIs (e.g.,dataproc-control.googleapis.com)

Customers sometimes encounter references to private APIs (like
`dataproc-control.googleapis.com` for Dataproc) in logs or documentation and
wonder if they need to enable or import them with Terraform.

**No Customer Action Required:** If an API is identified as a private or
internal Google Cloud API, you **don't** need to explicitly enable it using
`google_project_service` or attempt to import it with Terraform.

**Internal Management:** These APIs are crucial for the internal operation of
Google Cloud services. They are automatically managed by Google and are not
designed for direct customer interaction or management through public tools.

**No Impact on Service Usage:** Your inability to "import" or explicitly
manage such a private API using Terraform will **not** impact your ability to
use the associated Google Cloud service (e.g., Dataproc will function
correctly without you managing `dataproc-control.googleapis.com`). The
necessary internal API interactions are handled by Google.

**Focus on Public APIs:** When managing Google Cloud resources with Terraform,
your focus should solely be on enabling and configuring the **public APIs**
that correspond to the services and resources you intend to provision.

## Conclusion

By understanding the clear distinction between public and private Google Cloud
APIs, and the specific roles of "enabling" APIs versus "importing" resources in
Terraform, you can effectively manage your Google Cloud infrastructure. don't
attempt to explicitly manage or import private Google Cloud APIs; they are
internal components handled by Google. Focus your Terraform configurations on
the publicly exposed APIs and their corresponding resources.
