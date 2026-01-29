# ResourcesStay organized with collectionsSave and categorize content based on your preferences. and more

# ResourcesStay organized with collectionsSave and categorize content based on your preferences.

# ResourcesStay organized with collectionsSave and categorize content based on your preferences.

- [Terraform on Google Cloud provider reference documentation.](https://registry.terraform.io/providers/hashicorp/google/latest/docs)
- [How to authenticate to use Terraform on Google Cloud.](https://cloud.google.com/docs/terraform/authentication)

        Was this helpful?

---

# Authentication for TerraformStay organized with collectionsSave and categorize content based on your preferences.

# Authentication for TerraformStay organized with collectionsSave and categorize content based on your preferences.

This document describes how to authenticate to Google Cloud when using
Terraform.

Application Default Credentials (ADC) is the recommended way to authenticate to
Google Cloud when using Terraform. ADC is a strategy used by the
authentication libraries to automatically find credentials based on the
application environment. When you use ADC, Terraform can run in either a
development or production environment without changing how it authenticates to
Google Cloud services and APIs. For information about where ADC looks for
credentials and in what order, see [How Application Default Credentials
works](https://cloud.google.com/docs/authentication/application-default-credentials).

## Authenticate when using Terraform in a local development environment

When you're using Terraform in a local development environment, such as a
development workstation, you can authenticate using the credentials associated
with your [user account](https://cloud.google.com/docs/authentication#user-accounts) or [service
account](https://cloud.google.com/iam/docs/service-account-overview).

### Authenticate using a user account

To configure ADC with a user account, you use the Google Cloud CLI:

1. [Install](https://cloud.google.com/sdk/docs/install) the Google Cloud CLI.
            After installation,
            [initialize](https://cloud.google.com/sdk/docs/initializing) the Google Cloud CLI by running the following command:
  ```
  gcloud init
  ```
  If you're using an external identity provider (IdP), you must first
          [sign in to the gcloud CLI with your federated identity](https://cloud.google.com/iam/docs/workforce-log-in-gcloud).
2. If you're using a local shell, then create local authentication credentials for your user
          account:
  ```
  gcloud auth application-default login
  ```
  You don't need to do this if you're using Cloud Shell.
  If an authentication error is returned, and you are using an external identity provider
          (IdP), confirm that you have
          [signed in to the gcloud CLI with your federated identity](https://cloud.google.com/iam/docs/workforce-log-in-gcloud).
  A sign-in screen appears. After you sign in, your credentials are stored in the
        [local credential file used by ADC](https://cloud.google.com/docs/authentication/application-default-credentials#personal).

### Authenticate using service account impersonation

You can use service account impersonation to set up a local ADC file. Terraform
uses those credentials automatically.

1. Make sure you must have the Service Account Token Creator
  (`roles/iam.serviceAccountTokenCreator`) IAM role on the
  service account you are impersonating. For more information, see [Required
  roles](https://cloud.google.com/docs/authentication/use-service-account-impersonation#required-roles).
2. Use service account impersonation to create a local ADC file by running the
  following command:
  ```
  gcloud auth application-default login --impersonate-service-account SERVICE_ACCT_EMAIL
  ```

If you want to allow users to use a shared primary authentication source
and a variable service account per environment, set the
[impersonate_service_account](https://registry.terraform.io/providers/hashicorp/google/latest/docs/guides/provider_reference#impersonate_service_account)
field in your Terraform configuration file:

```
provider "google" {
  impersonate_service_account = "SERVICE_ACCT_EMAIL"
}
```

## Authenticate when running Terraform on Google Cloud

When running Terraform on a Google Cloud cloud-based development
environment such as Cloud Shell, the tool uses the credentials you provided
when you signed in for authentication.

When using Terraform with Google Cloud services such as Compute Engine,
App Engine, and Cloud Run functions, you can attach a [user-managed service
account](https://cloud.google.com/iam/docs/service-account-types#user-created) to resources. Generally,
attaching a service account is supported when that service's resources can run
or include application code. When you attach a service account to a resource,
the code running on the resource can use that service account as its identity.

Attaching a user-managed service account is the preferred way to provide
credentials to ADC for production code running on Google Cloud.

For help determining the roles that you need to provide to your service account,
see [Choose predefined roles](https://cloud.google.com/iam/docs/choose-predefined-roles).

For information about which resources you can attach a service account to, and
help with attaching the service account to the resource, see the
[IAM documentation on attaching a service
account](https://cloud.google.com/iam/docs/attach-service-accounts#attaching-new-resource).

Set up authentication:

1. Ensure that you have the Create Service Accounts IAM role
      (`roles/iam.serviceAccountCreator`) and the Project IAM Admin role
      (`roles/resourcemanager.projectIamAdmin`). [Learn how to grant roles](https://cloud.google.com/iam/docs/granting-changing-revoking-access).
2. Create the service account:
  ```
  gcloud iam service-accounts create SERVICE_ACCOUNT_NAME
  ```
  Replace `SERVICE_ACCOUNT_NAME` with a name for the service account.
3. To provide access to your project and your resources, grant a role to the service account:
  ```
  gcloud projects add-iam-policy-binding PROJECT_ID --member="serviceAccount:SERVICE_ACCOUNT_NAME@PROJECT_ID.iam.gserviceaccount.com" --role=ROLE
  ```
  Replace the following:
  - `SERVICE_ACCOUNT_NAME`: the name of the service account
  - `PROJECT_ID`: the project ID where you created the service account
  - `ROLE`: the role to grant
4. To grant another role to the service account, run the command as you did in the previous step.
5. Grant the required role to the principal that
        will attach the service account to other resources.
  ```
  gcloud iam service-accounts add-iam-policy-binding SERVICE_ACCOUNT_NAME@PROJECT_ID.iam.gserviceaccount.com --member="user:USER_EMAIL" --role=roles/iam.serviceAccountUser
  ```
  Replace the following:
  - `SERVICE_ACCOUNT_NAME`: the name of the service account
  - `PROJECT_ID`: the project ID where you created the service account
  - `USER_EMAIL`: the email address for a Google Account

## Authenticate when running Terraform on-premises or on a different cloud provider

If you are running your application outside of Google Cloud, you need to
provide credentials that are recognized by Google Cloud to use
Google Cloud services.

### Authenticate using Workload Identity Federation

The preferred way to authenticate with Google Cloud using credentials from
an external IdP is to use
[Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation). You can
create a credential configuration file and set the
`GOOGLE_APPLICATION_CREDENTIALS` environment variable to point to it. This
approach is more secure than creating a service account key. For instructions
on setting up Workload Identity Federation for ADC, see
[Workload Identity Federation with other clouds](https://cloud.google.com/iam/docs/workload-identity-federation-with-other-clouds).

## Authenticate using service account keys

When running Terraform in a local development environment, on premises, or
a different cloud provider, you can create a service account, grant it the
IAM roles that your application requires, and create a key for
the service account.

To create a service account key and make it available to ADC:

1. Create a service account with the roles your application needs, and a key
  for that service account, by following the instructions in [Creating a
  service account key](https://cloud.google.com/iam/docs/keys-create-delete#creating).
  Set the environment variable `GOOGLE_APPLICATION_CREDENTIALS`
      to the path of the JSON file that contains your credentials.
      This variable applies only to your current shell session, so if you open
      a new session, set the variable again.
  ```
  KEY_PATH
  ```
  Replace `KEY_PATH` with the path of the JSON file that contains your credentials.
  For example:
  ```
  export GOOGLE_APPLICATION_CREDENTIALS="/home/user/Downloads/service-account-file.json"
  ```
  For PowerShell:
  ```
  KEY_PATH
  ```
  Replace `KEY_PATH` with the path of the JSON file that contains your credentials.
  For example:
  ```
  $env:GOOGLE_APPLICATION_CREDENTIALS="C:\Users\username\Downloads\service-account-file.json"
  ```
  For command prompt:
  ```
  KEY_PATH
  ```
  Replace `KEY_PATH` with the path of the JSON file that contains your credentials.

## Authenticate to Cloud Storage backends

Terraform lets you configure Cloud Storage as a backend to store Terraform
state files. To authenticate to a [Cloud Storage backend](https://cloud.google.com/docs/terraform/resource-management/store-state),
use any of the methods described on this page. For information on
configuration variables related to authentication for Cloud Storage
backends, see the
[Terraform backends page for Cloud Storage](https://developer.hashicorp.com/terraform/language/settings/backends/gcs#configuration-variables).

## What's next

- Work through the [Terraform for Google Cloud quickstart](https://cloud.google.com/docs/terraform/create-vm-instance)
- Learn about the [basic Terraform commands](https://cloud.google.com/docs/terraform/basic-commands).

---

# Basic Terraform commandsStay organized with collectionsSave and categorize content based on your preferences.

# Basic Terraform commandsStay organized with collectionsSave and categorize content based on your preferences.

To apply your Terraform configuration in a Google Cloud project, complete the steps in the
   following sections.

## Prepare Cloud Shell

1. Launch [Cloud Shell](https://shell.cloud.google.com/).
2. Set the default Google Cloud project
        where you want to apply your Terraform configurations.
  You only need to run this command once per project, and you can run it in any directory.
  ```
  export GOOGLE_CLOUD_PROJECT=PROJECT_ID
  ```
  Environment variables are overridden if you set explicit values in the Terraform
        configuration file.

## Prepare the directory

Each Terraform configuration file must have its own directory (also
called a *root module*).

1. In [Cloud Shell](https://shell.cloud.google.com/), create a directory and a new
      file within that directory. The filename must have the
      `.tf` extension—for example `main.tf`. In this
      tutorial, the file is referred to as `main.tf`.
  ```
  mkdir DIRECTORY && cd DIRECTORY && touch main.tf
  ```
2. If you are following a tutorial, you can copy the sample code in each section or step.
  Copy the sample code into the newly created `main.tf`.
  Optionally, copy the code from GitHub. This is recommended
        when the Terraform snippet is part of an end-to-end solution.
3. Review and modify the sample parameters to apply to your environment.
4. Save your changes.
5. Initialize Terraform. You only need to do this once per directory.
  ```
  terraform init
  ```
  Optionally, to use the latest Google provider version, include the `-upgrade`
        option:
  ```
  terraform init -upgrade
  ```

## Apply the changes

1. Review the configuration and verify that the resources that Terraform is going to create or
      update match your expectations:
  ```
  terraform plan
  ```
  Make corrections to the configuration as necessary.
2. Apply the Terraform configuration by running the following command and entering `yes`
      at the prompt:
  ```
  terraform apply
  ```
  Wait until Terraform displays the "Apply complete!" message.
3. [Open your Google Cloud project](https://console.cloud.google.com/) to view
      the results. In the Google Cloud console, navigate to your resources in the UI to make sure
      that Terraform has created or updated them.

## Reformat

To reformat your Terraform configuration in the standard style, enter the
following command:

```
terraform fmt
```

## Validate

To check whether your configuration is valid, enter the following command:

```
terraform validate
```

## Delete changes

Remove resources previously applied with your Terraform configuration by running the following
   command and entering `yes` at the prompt:

```
terraform destroy
```

## Specify the project ID

If you run the `export GOOGLE_CLOUD_PROJECT` command, most resources can infer
the `project_id`.

Some resources, such as `project_iam_*`, cannot infer the project ID. As a
workaround, some samples use the [data "google_project"](https://registry.terraform.io/providers/hashicorp/google/latest/docs/data-sources/project)
data source. You can replace this data source with the project ID string or a
variable.

For a sample that uses this workaround, see
[sql_instance_iam_condition](https://github.com/terraform-google-modules/terraform-docs-samples/blob/main/cloud_sql/instance_iam_condition/main.tf).

## What's next

- [Learn more about Terraform's CLI features](https://www.terraform.io/cli/commands).

   Was this helpful?

---

# Best practices for cross

# Best practices for cross-configuration communicationStay organized with collectionsSave and categorize content based on your preferences.

This page provides guidelines and recommendations for
cross-configuration communication when using Terraform for Google Cloud.

This guide is not an introduction to Terraform. For an introduction to using
Terraform with Google Cloud, see
[Get started with Terraform](https://cloud.google.com/docs/terraform/get-started-with-terraform).

A common problem that arises when using Terraform is how to share information
across different Terraform configurations (possibly maintained by different
teams). Generally, information can be shared between configurations without
requiring that they be stored in a single configuration directory (or even a
single repository).

The recommended way to share information between different Terraform
configurations is by using remote state to reference other root modules.
[Cloud Storage](https://www.terraform.io/docs/backends/types/gcs.html)
or
[Terraform Enterprise](https://www.terraform.io/docs/backends/types/terraform-enterprise.html)
are the preferred state backends.

For querying resources that are not managed by Terraform, use data sources from
the
[Google provider](https://registry.terraform.io/providers/hashicorp/google/latest/docs).
For example, the default Compute Engine service account can be retrieved
[using a data source](https://registry.terraform.io/providers/hashicorp/google/latest/docs/data-sources/compute_default_service_account).
Don't use data sources to query resources that are managed by another Terraform
configuration. Doing so can create implicit dependencies on resource names and
structures that normal Terraform operations might unintentionally break.

## What's next

- Learn about [best practices for version control](https://cloud.google.com/docs/terraform/best-practices/version-control).
- Learn about [best practices when working with Google Cloud resources](https://cloud.google.com/docs/terraform/best-practices/working-with-resources).

   Was this helpful?

---

# Best practices on dependency managementStay organized with collectionsSave and categorize content based on your preferences.

# Best practices on dependency managementStay organized with collectionsSave and categorize content based on your preferences.

This document provides recommendations for expressing dependencies between
resources in your Terraform configuration.

## Favor implicit dependencies over explicit dependencies

Resource dependencies arise when one resource depends on the existence of other
resources. Terraform must be able to understand these dependencies to ensure
that resources are created in the correct order. For example, if resource A has
a dependency on resource B, resource B is created before resource A.

Terraform configuration dependencies can be established through
[implicit and explicit dependency declarations](https://developer.hashicorp.com/terraform/tutorials/configuration-language/dependencies).
Implicit dependencies are declared through
[expression references](https://developer.hashicorp.com/terraform/language/expressions/references),
while explicit dependencies are specified by using the
[depends_on](https://developer.hashicorp.com/terraform/language/meta-arguments/depends_on)
meta argument. The `depends_on` argument specifies that Terraform must complete
all the actions on the object(s) that a resource or a module depends on, before
proceeding with the dependent object.

While both approaches ensure a correct order of operations, implicit
dependencies often lead to more efficiency in planning for [updates and
replacement of resources](https://developer.hashicorp.com/terraform/language/meta-arguments/depends_on#processing-and-planning-consequences). This is because Terraform can
intelligently track the specific fields involved in an implicit dependency,
potentially avoiding changes to the dependent resource if those specific fields
remain unaltered within the dependency.

In comparison to implicit dependencies, explicit dependencies convey less
specific information. This means that Terraform can only formulate more
conservative plans for resource creation, updates, and replacement in the
absence of knowledge of the particular attributes that constitute the dependency.
In practice, this impacts the sequence in which resources are created by
Terraform and how Terraform determines whether resources require updates or
replacements.

We recommended using explicit dependencies with the `depends_on` meta argument
only as the last resort when a dependency between two resources is hidden and
can't be expressed through implicit dependencies.

In the following example, the required project services must be enabled before
creating a BigQuery dataset. This dependency is declared
explicitly:

Not recommended:

```
module "project_services" {
  source  = "terraform-google-modules/project-factory/google//modules/project_services"
  version = "~> 14.4"

  project_id = var.project_id
  activate_apis = [
    "bigquery.googleapis.com",
    "bigquerystorage.googleapis.com",
  ]
}

module "bigquery" {
  source       = "terraform-google-modules/bigquery/google"
  version      = "~> 5.4"

  dataset_id   = "demo_dataset"
  dataset_name = "demo_dataset"
  project_id   = var.project_id
  depends_on = [module.project_services] # <- explicit dependency
}
```

The following example replaces the explicit dependency with an implicit
dependency by referencing the `project_id` argument as the `project_id` output
attribute of the `project_services` resource:

Recommended:

```
module "bigquery" {
  source       = "terraform-google-modules/bigquery/google"
  version      = "~> 5.4"

  dataset_id   = "demo_dataset"
  dataset_name = "demo_dataset"
  project_id   = module.project_services.project_id # <- implicit dependency
}
```

The use of implicit dependencies allows for precise declarations of
dependencies, such as specifying the exact information that needs to be
collected from an upstream object. This also reduces the need for making changes
in multiple places, which in turn reduces the risk of errors.

## Reference output attributes from dependent resources

When you create implicit dependencies by referencing values from upstream
resources, make sure to only reference output attributes, specifically
[values that are not yet known](https://developer.hashicorp.com/terraform/language/expressions/references#values-not-yet-known).
This will ensure that Terraform waits for the upstream resources to be created
before provisioning the current resource.

In the following example, the `google_storage_bucket_object` resource references
the name argument of the `google_storage_bucket` resource. Arguments have known
values during the Terraform plan phase. This means that when Terraform creates
the `google_storage_bucket_object` resource, it doesn't wait for the
`google_storage_bucket` resource to be created because referencing a known
argument (the bucket name) doesn't create an implicit dependency between the
`google_storage_bucket_object` and the `google_storage_bucket`. This defeats the
purpose of the implicit dependency declaration between the two resources.

Not recommended:

```
# Cloud Storage bucket
resource "google_storage_bucket" "bucket" {
  name = "demo-bucket"
  location = "US"
}

resource "google_storage_bucket_object" "bucket_object" {
  name   = "demo-object"
  source = "./test.txt"
  bucket = google_storage_bucket.bucket.name # name is an input argument
}
```

Instead, `google_storage_bucket_object` resource must reference the `id`
output attribute of the `google_storage_bucket_object` resource. Since the `id`
field is an output attribute, its value is only set after the creation of its
resource has been executed. Therefore, Terraform will wait for the creation of
the `google_storage_bucket_object` resource to complete before beginning the
creation of the `google_storage_bucket_object` resource.

Recommended:

```
resource "google_storage_bucket_object" "bucket_object" {
  name   = "demo-object"
  source = "./test.txt"
  bucket = google_storage_bucket.bucket.id # id is an output attribute
}
```

Sometimes there is no obvious output attribute to reference. For example,
consider the following example where `module_a` takes the name of the generated
file as input. Inside `module_a`, the filename is used to read the file. If
you run this code as-is, you'll get a `no such file or directory` exception,
which is caused by Terraform attempting to read the file during its planning
phase, at which time the file hasn't been created yet. In this case, an
examination of the output attribute of the `local_file` resource reveals that
there are no obvious fields that you can use in place of the filename input
argument.

Not recommended:

```
resource "local_file" "generated_file" {
 filename = "./generated_file.text"
 content = templatefile("./template.tftpl", {
   project_id = var.project_id
 })
}

module "module_a" {
 source = "./modules/module-a"
 root_config_file_path = local_file.generated_file.filename
}
```

You can solve this problem by introducing an explicit dependency. As a best
practice, make sure add a comment on why the explicit dependency is needed:

Recommended:

```
module "module_a" {
 source = "./modules/module-a"
 root_config_file_path = local_file.generated_file.filename
 depends_on = [local_file.generated_file] # waiting for generated_file to be created
}
```

## What's next

- Learn about [best practices for cross-configuration communication](https://cloud.google.com/docs/terraform/best-practices/cross-config-communication).
- Learn about [best practices when working with Google Cloud resources](https://cloud.google.com/docs/terraform/best-practices/working-with-resources).

   Was this helpful?

---

# Best practices for general style and structureStay organized with collectionsSave and categorize content based on your preferences.

# Best practices for general style and structureStay organized with collectionsSave and categorize content based on your preferences.

This document provides basic style and structure recommendations for your
Terraform configurations. These recommendations apply to reusable Terraform
modules and to root configurations.

This guide is not an introduction to Terraform. For an introduction to using
Terraform with Google Cloud, see
[Get started with Terraform](https://cloud.google.com/docs/terraform/get-started-with-terraform).

## Follow a standard module structure

- Terraform modules must follow the
  [standard module structure](https://www.terraform.io/docs/modules/create.html).
- Start every module with a `main.tf` file, where resources are located by
  default.
- In every module, include a `README.md` file in Markdown format. In the
  `README.md` file, include basic documentation about the module.
- Place examples in an `examples/` folder, with a separate subdirectory for
  each example. For each example, include a detailed `README.md` file.
- Create  logical groupings of resources with their own files and
  descriptive names, such as `network.tf`, `instances.tf`, or `loadbalancer.tf`.
  - Avoid giving every resource its own file. Group resources by
    their shared purpose. For example, combine `google_dns_managed_zone`
    and `google_dns_record_set` in `dns.tf`.
- In the module's root directory, include only Terraform
  (`*.tf`) and repository metadata files (such as `README.md` and
  `CHANGELOG.md`).
- Place any additional documentation in a `docs/` subdirectory.

## Adopt a naming convention

- Name all configuration objects using underscores to delimit multiple
  words. This practice ensures consistency with the naming convention for
  resource types, data source types, and other predefined values. This
  convention does not apply to name
  [arguments](https://www.terraform.io/docs/glossary#argument).
  Recommended:
  ```
  resource "google_compute_instance" "web_server" {
    name = "web-server"
  }
  ```
  Not recommended:
  ```
  resource "google_compute_instance" "web-server" {
    name = "web-server"
  }
  ```
- To simplify references to a resource that is the only one of its type
  (for example, a single load balancer for an entire module), name the
  resource `main`.
  - It takes extra mental work to remember
    `some_google_resource.my_special_resource.id` versus
    `some_google_resource.main.id`.
- To differentiate resources of the same type from each other (for example,
  `primary` and `secondary`), provide meaningful resource names.
- Make resource names singular.
- In the resource name, don't repeat the resource type.
  For example:
  Recommended:
  ```
  resource "google_compute_global_address" "main" { ... }
  ```
  Not recommended:
  ```
  resource "google_compute_global_address" "main_global_address" { … }
  ```

## Use variables carefully

- Declare all variables in `variables.tf`.
- Give variables descriptive names that are relevant to their usage or
  purpose:
  - Inputs, local variables, and outputs representing numeric
    values—such as disk sizes or RAM size—*must* be named with
    units (such as `ram_size_gb`). Google Cloud APIs don't have standard
    units, so naming variables with units makes the expected
    input unit clear for configuration maintainers.
  - For units of storage, use binary unit prefixes (powers of 1024)—`kibi`,
    `mebi`, `gibi`. For all other units of measurement, use decimal
    unit prefixes (powers of 1000)—`kilo`, `mega`, `giga`. This usage
    matches the usage within Google Cloud.
  - To simplify conditional logic, give boolean variables positive names—for
    example, `enable_external_access`.
- Variables must have descriptions. Descriptions are automatically
  included in a published module's auto-generated documentation.
  Descriptions add additional context for new developers that descriptive
  names cannot provide.
- Give variables defined types.
- When appropriate, provide default values:
  - For variables that have environment-independent values (such as disk
    size), provide default values.
  - For variables that have environment-specific values (such as
    `project_id`), don't provide default values. This way, the calling module
    must provide meaningful values.
- Use empty defaults for variables (like empty strings or lists) only when
  leaving the variable empty is a valid preference that the underlying APIs
  don't reject.
- Be judicious in your use of variables. Only parameterize values that
  must vary for each instance or environment. When deciding whether to expose
  a variable, ensure that you have a concrete use case for changing that
  variable. If there's only a small chance that a variable might be needed,
  don't expose it.
  - Adding a variable with a default value is backwards-compatible.
  - Removing a variable is backwards-incompatible.
  - In cases where a literal is reused in multiple places, you can use a
    [local value](https://www.terraform.io/docs/configuration/locals.html)
    without exposing it as a variable.

## Expose outputs

- Organize all outputs in an `outputs.tf` file.
- Provide meaningful descriptions for all outputs.
- Document output descriptions in the `README.md` file. Auto-generate
  descriptions on commit with tools like
  [terraform-docs](https://github.com/terraform-docs/terraform-docs).
- Output all useful values that root modules might need to refer to or share.
  Especially for open source or heavily used modules, expose all outputs that
  have potential for consumption.
- Don't pass outputs directly through input variables, because doing so
  prevents them from being properly added to the dependency graph. To ensure
  that
  [implicit dependencies](https://learn.hashicorp.com/terraform/getting-started/dependencies.html)
  are created, make sure that outputs reference attributes from resources.
  Instead of referencing an input variable for an instance directly, pass
  the attribute through as shown here:
  Recommended:
  ```
  output "name" {
    description = "Name of instance"
    value       = google_compute_instance.main.name
  }
  ```
  Not recommended:
  ```
  output "name" {
    description = "Name of instance"
    value       = var.name
  }
  ```

## Use data sources

- Put
  [data sources](https://www.terraform.io/docs/configuration/data-sources.html)
  next to the resources that reference them. For example, if you are fetching
  an image to be used in launching an instance, place it alongside the
  instance instead of collecting data resources in their own file.
- If the number of data sources becomes large, consider moving them to a
  dedicated `data.tf` file.
- To fetch data relative to the current environment, use variable or resource
  [interpolation](https://www.terraform.io/language/expressions/strings#interpolation).

## Limit the use of custom scripts

- Use scripts only when necessary. The state of resources created
  through scripts is not accounted for or managed by Terraform.
  - Avoid custom scripts, if possible. Use them only when Terraform
    resources don't support the desired behavior.
  - Any custom scripts used must have a clearly documented reason for
    existing and ideally a deprecation plan.
- Terraform can call custom scripts through provisioners, including the
  local-exec provisioner.
- Put custom scripts called by Terraform in a `scripts/` directory.

## Include helper scripts in a separate directory

- Organize helper scripts that aren't called by Terraform in a
  `helpers/` directory.
- Document helper scripts in the `README.md` file with explanations and
  example invocations.
- If helper scripts accept arguments, provide argument-checking and
  `--help` output.

## Put static files in a separate directory

- Static files that Terraform references but doesn't execute (such as
  startup scripts loaded onto Compute Engine instances) must be organized
  into a `files/` directory.
- Place lengthy HereDocs in external files, separate from their HCL.
  Reference them with the
  [file()function](https://www.terraform.io/language/functions/file).
- For files that are read in by using the Terraform
  [templatefilefunction](https://www.terraform.io/docs/configuration/functions/templatefile.html),
  use the file extension `.tftpl`.
  - Templates must be placed in a `templates/` directory.

## Protect stateful resources

For stateful resources, such as databases, ensure that
[deletion protection](https://www.terraform.io/language/meta-arguments/lifecycle)
is enabled. For example:

```
resource "google_sql_database_instance" "main" {
  name = "primary-instance"
  settings {
    tier = "D0"
  }

  lifecycle {
    prevent_destroy = true
  }
}
```

## Use built-in formatting

All Terraform files must conform to the standards of `terraform fmt`.

### Limit the complexity of expressions

- Limit the complexity of any individual interpolated expressions. If
  many functions are needed in a single expression, consider splitting it out
  into multiple expressions by using
  [local values](https://www.terraform.io/docs/configuration/locals.html).
- Never have more than one ternary operation in a single line. Instead,
  use multiple local values to build up the logic.

## Usecountfor conditional values

To instantiate a resource conditionally, use the
[count](https://www.terraform.io/language/meta-arguments/count) meta-argument.
For example:

```
variable "readers" {
  description = "..."
  type        = list
  default     = []
}

resource "resource_type" "reference_name" {
  // Do not create this resource if the list of readers is empty.
  count = length(var.readers) == 0 ? 0 : 1
  ...
}
```

Be sparing when using user-specified variables to set the `count` variable for
resources. If a resource attribute is provided for such a variable (like
`project_id`) and that resource does not yet exist, Terraform can't
generate a plan. Instead, Terraform reports the error
[value of count cannot be computed](https://github.com/hashicorp/terraform/issues/17421).
In such cases, use a separate `enable_x` variable to compute the
conditional logic.

## Usefor_eachfor iterated resources

If you want to create multiple copies of a resource based on an input resource,
use the
[for_each](https://www.terraform.io/language/meta-arguments/for_each)
meta-argument.

## Publish modules to a registry

- **Reusable modules**: Publish reusable modules to a
  [module registry](https://www.terraform.io/internals/module-registry-protocol).
- **Open source modules**: Publish open source modules to the
  [Terraform Registry](https://registry.terraform.io/).
- **Private modules**: Publish private modules to a
  [private registry](https://www.terraform.io/cloud-docs/registry).

## What's next

- Learn about [best practices when using reusable modules](https://cloud.google.com/docs/terraform/best-practices/reusable-modules).
- Learn about [best practices when using Terraform root modules](https://cloud.google.com/docs/terraform/best-practices/root-modules).

   Was this helpful?

---

# Best practices for Terraform operationsStay organized with collectionsSave and categorize content based on your preferences.

# Best practices for Terraform operationsStay organized with collectionsSave and categorize content based on your preferences.

This document provides guidelines and recommendations for Terraform operations.

This guide is not an introduction to Terraform. For an introduction to using
Terraform with Google Cloud, see
[Get started with Terraform](https://cloud.google.com/docs/terraform/get-started-with-terraform).

## Always plan first

Always generate a plan first for Terraform executions.
[Save the plan to an output file](https://learn.hashicorp.com/tutorials/terraform/automate-terraform).
After an infrastructure owner approves it, execute the plan. Even when
developers are locally prototyping changes, they should generate a plan and
review the resources to be added, modified, and destroyed before applying the
plan.

## Implement an automated pipeline

To ensure consistent execution context, execute Terraform through automated
tooling. If a build system (like Jenkins) is already in use and widely adopted,
use it to run the `terraform plan` and `terraform apply` commands automatically.
If no existing system is available, adopt either
[Cloud Build](https://cloud.google.com/docs/terraform/resource-management/managing-infrastructure-as-code)
or
[Terraform Cloud](https://cloud.hashicorp.com/products/terraform).

## Use service account credentials for continuous integration

When Terraform is executed from a machine in a CI/CD pipeline, it should
inherit the service account credentials from the service executing the pipeline.
Wherever possible, run CI pipelines on Google Cloud because
Cloud Build, Google Kubernetes Engine, or Compute Engine inject credentials
without downloading service account keys.

For pipelines that run outside of Google Cloud, prefer
[workload identity federation](https://cloud.google.com/iam/docs/using-workload-identity-federation)
to obtain credentials without downloading service account keys.

## Avoid importing existing resources

Where possible, avoid importing existing resources
(using [terraform import](https://www.terraform.io/cli/import)), because doing
so can make it challenging to fully understand the provenance and configuration
of manually created resources. Instead, create new resources through Terraform
and delete the old resources.

In cases where deleting old resources would create significant toil,
use the `terraform import` command with explicit approval. After a resource is
imported into Terraform, manage it exclusively with Terraform.

Google provides a tool that you can use to import your
Google Cloud resources into Terraform state. For more information,
see [Import your Google Cloud resources into Terraform
state](https://cloud.google.com/docs/terraform/resource-management/import).

## Don't modify Terraform state manually

The Terraform state file is critical for maintaining the mapping between
Terraform configuration and Google Cloud resources. Corruption can lead
to major infrastructure problems. When modifications to the Terraform state are
necessary, use the [terraform state](https://www.terraform.io/cli/state)
command.

## Regularly review version pins

Pinning versions ensures stability but prevents bug fixes and other
improvements from being incorporated into your configuration. Therefore,
regularly review version pins for Terraform, Terraform providers, and modules.

To automate this process, use a tool such as
[Dependabot](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/about-dependabot-version-updates#supported-repositories-and-ecosystems).

## Use application default credentials when running locally

When developers are locally iterating on Terraform configuration, they should
authenticate by running
[gcloud auth application-default login](https://cloud.google.com/sdk/gcloud/reference/auth/application-default/login)
to generate application default credentials. Don't download service account
keys, because downloaded keys are harder to manage and secure.

## Set aliases to Terraform

To make local development easier, you can add aliases to your command shell
profile:

- `alias tf="terraform"`
- `alias terrafrom="terraform"`

## What's next

- Learn about [best practices to securely use Terraform](https://cloud.google.com/docs/terraform/best-practices/security).
- Learn about [best practices for testing Terraform modules and configurations](https://cloud.google.com/docs/terraform/best-practices/testing).

   Was this helpful?

---

# Best practices for reusable modulesStay organized with collectionsSave and categorize content based on your preferences.

# Best practices for reusable modulesStay organized with collectionsSave and categorize content based on your preferences.

This document provides guidelines and recommendations to consider when using
reusable Terraform modules.

This guide is not an introduction to Terraform. For an introduction to using
Terraform with Google Cloud, see
[Get started with Terraform](https://cloud.google.com/docs/terraform/get-started-with-terraform).

## Activate required APIs in modules

Terraform modules can activate any required services by using the
`google_project_service` resource or the
[project_services](https://github.com/terraform-google-modules/terraform-google-project-factory/tree/master/modules/project_services) module.
Including API activation makes demonstrations easier.

- If API activation is included in a module, then the API activation *must*
  be disableable by exposing an `enable_apis` variable that defaults to
  `true`.
- If API activation is included in a module, then the API activation *must*
  set `disable_services_on_destroy` to `false`, because this attribute can
  cause issues when working with multiple instances of the module.
  For example:
  ```
  module "project-services" {
    source  = "terraform-google-modules/project-factory/google//modules/project_services"
    version = "~> 12.0"
    project_id  = var.project_id
    enable_apis = var.enable_apis
    activate_apis = [
      "compute.googleapis.com",
      "pubsub.googleapis.com",
    ]
    disable_services_on_destroy = false
  }
  ```

## Include an owners file

For all shared modules, include an
[OWNERS](https://github.com/bkeepers/OWNERS)
file (or
[CODEOWNERS](https://blog.github.com/2017-07-06-introducing-code-owners/)
on GitHub), documenting who is responsible for the module. Before any pull
request is merged, an owner should approve it.

### Release tagged versions

Sometimes modules require breaking changes and you need to communicate the
effects to users so that they can pin their configurations to a specific
version.

Make sure that shared modules follow
[SemVer v2.0.0](https://semver.org/spec/v2.0.0.html)
when new versions are tagged or released.

When referencing a module, use a
[version constraint](https://www.terraform.io/language/expressions/version-constraints)
to pin to the *major* version. For example:

```
module "gke" {
  source  = "terraform-google-modules/kubernetes-engine/google"
  version = "~> 20.0"
}
```

## Don't configure providers or backends

Shared modules [must not configure providers or backends](https://developer.hashicorp.com/terraform/language/providers/configuration#provider-configuration-1).
Instead, configure providers and backends in root modules.

For shared modules, define the minimum required provider versions in a
[required_providers](https://www.terraform.io/language/modules/develop/providers#provider-version-constraints-in-modules)
block, as follows:

```
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.0.0"
    }
  }
}
```

Unless proven otherwise, assume that new provider versions will work.

## Expose labels as a variable

Allow flexibility in the labeling of resources through the module's interface.
Consider providing a `labels` variable with a default value of an empty map, as
follows:

```
variable "labels" {
  description = "A map of labels to apply to contained resources."
  default     = {}
  type        = "map"
}
```

## Expose outputs for all resources

Variables and outputs let you infer dependencies between modules and resources.
Without any outputs, users cannot properly order your module in relation to
their Terraform configurations.

For every resource defined in a shared module, include at least one output that
references the resource.

## Use inline submodules for complex logic

- Inline modules let you organize complex Terraform modules into
  smaller units and de-duplicate common resources.
- Place inline modules in `modules/$modulename`.
- Treat inline modules as private, not to be used by outside modules,
  unless the shared module's documentation specifically states otherwise.
- Terraform doesn't track refactored resources. If you start with several
  resources in the top-level module and then push them into submodules,
  Terraform tries to recreate all refactored resources. To mitigate this
  behavior, use
  [moved](https://www.terraform.io/language/modules/develop/refactoring#moved-block-syntax)
  blocks when refactoring.
- Outputs defined by internal modules aren't automatically exposed. To share
  outputs from internal modules, re-export them.

## What's next

- Learn about [general style and structure best practices for Terraform on Google Cloud](https://cloud.google.com/docs/terraform/best-practices/general-style-structure).
- Learn about [best practices when using Terraform root modules](https://cloud.google.com/docs/terraform/best-practices/root-modules).

   Was this helpful?
