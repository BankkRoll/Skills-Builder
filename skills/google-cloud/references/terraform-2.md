# Best practices for root modulesStay organized with collectionsSave and categorize content based on your preferences. and more

# Best practices for root modulesStay organized with collectionsSave and categorize content based on your preferences.

# Best practices for root modulesStay organized with collectionsSave and categorize content based on your preferences.

This document provides guidelines and recommendations to consider
when using root modules.

Root configurations or root modules are the working directories from which you
run the Terraform CLI. Make sure that root configurations adhere to the
following standards (and to the previous Terraform guidelines where applicable).
Explicit recommendations for root modules supersede the general guidelines.

This guide is not an introduction to Terraform. For an introduction to using
Terraform with Google Cloud, see [Get started with
Terraform](https://cloud.google.com/docs/terraform/get-started-with-terraform).

## Minimize the number of resources in each root module

It is important to keep a single root configuration from growing too large, with
too many resources stored in the same directory and state. *All* resources in a
particular root configuration are refreshed every time Terraform is run. This
can cause slow execution if too many resources are included in a single state. A
general rule: Don't include more than 100 resources (and ideally only a few
dozen) in a single state.

## Use separate directories for each application

To manage applications and projects independently of each other, put resources
for each application and project in their own Terraform directories. A service
might represent a particular application or a common service such as shared
networking. Nest all Terraform code for a particular service under *one*
directory (including subdirectories).

## Split applications into environment-specific subdirectories

When deploying services in Google Cloud, split the Terraform
configuration for the service into two top-level directories: a `modules`
directory that contains the actual configuration for the service, and an
`environments` directory that contains the root configurations for each
environment.

```
-- SERVICE-DIRECTORY/
   -- OWNERS
   -- modules/
      -- <service-name>/
         -- main.tf
         -- variables.tf
         -- outputs.tf
         -- provider.tf
         -- README
      -- ...other…
   -- environments/
      -- dev/
         -- backend.tf
         -- main.tf

      -- qa/
         -- backend.tf
         -- main.tf

      -- prod/
         -- backend.tf
         -- main.tf
```

## Use environment directories

To share code across environments, reference modules. Typically, this might be a
service module that includes the base shared Terraform configuration for the
service. In service modules, hard-code common inputs and only require
environment-specific inputs as variables.

Each environment directory must contain the following files:

- A `backend.tf` file, declaring the Terraform
  [backend](https://www.terraform.io/docs/backends/)
  state location (typically, [Cloud Storage](https://cloud.google.com/storage))
- A `main.tf` file that instantiates the service module

Each environment directory (`dev`, `qa`, `prod`) corresponds to a default
[Terraform workspace](https://www.terraform.io/docs/state/workspaces)
and deploys a version of the service to that environment. These workspaces
isolate environment-specific resources into their own contexts. *Use only the
default workspace*.

Having multiple
[CLI workspaces](https://developer.hashicorp.com/terraform/language/state/workspaces)
within an environment isn't recommended for the following reasons:

- It can be difficult to inspect the configuration in each workspace.
- Having a single shared backend for multiple workspaces isn't recommended
  because the shared backend becomes a single point of failure if it is used for
  environment separation.
- While code reuse is possible, code becomes harder to read having to switch
  based on the current workspace variable (for example,
  `terraform.workspace == "foo" ? this : that`).

For more information, see the following:

- [Workspaces](https://www.terraform.io/language/state/workspaces#when-to-use-multiple-workspaces)
- [When Not to Use Multiple Workspaces](https://developer.hashicorp.com/terraform/cli/workspaces#when-not-to-use-multiple-workspaces)

## Expose outputs through remote state

Make sure you're exposing useful outputs of module instances from a root module.

For example, the following code snippet passes through the project ID output
from the project factory module instance as an output of the root module.

```
# Project root module
terraform {
  backend "gcs" {
    bucket  = "BUCKET"
  }
}

module "project" {
  source  = "terraform-google-modules/project-factory/google"
  ...
}

output "project_id" {
  value       = module.project.project_id
  description = "The ID of the created project"
}
```

Other Terraform environments and applications can reference root module-level
outputs only.

By using
[remote state](https://www.terraform.io/language/state/remote-state-data),
you can reference root module outputs. To allow use by other dependent apps for
configuration, make sure you're exporting information that's related to a
service's endpoints, to remote state.

```
# Networks root module
data "terraform_remote_state" "network_project" {
  backend = "gcs"

  config = {
    bucket = "BUCKET"
  }
}

module "vpc" {
  source  = "terraform-google-modules/network/google"
  version = "~> 9.0"

  project_id   = data.terraform_remote_state.network_project.outputs.project_id
  network_name = "vpc-1"
  ...
}
```

Sometimes, such as when invoking a shared service module from environment
directories, it is appropriate to re-export the entire child module, as follows:

```
output "service" {
  value       = module.service
  description = "The service module outputs"
}
```

## Pin to minor provider versions

In root modules, declare each provider and pin to a *minor* version. This
allows automatic upgrade to new patch releases while still keeping a solid
target. For consistency, name the versions file `versions.tf`.

```
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0.0"
    }
  }
}
```

## Store variables in atfvarsfile

For root modules, provide variables by using a `.tfvars` variables file. For
consistency, name variable files `terraform.tfvars`.

Don't specify variables by using alternative
[var-files](https://www.terraform.io/language/values/variables#variable-definitions-tfvars-files)
or `var='key=val'` command-line options. Command-line options are ephemeral and
easy to forget. Using a default variables file is more predictable.

## Check in.terraform.lock.hclfile

For root modules, the `.terraform.lock.hcl` [dependency lock](https://www.terraform.io/language/files/dependency-lock)
file should be checked into source control. This allows for tracking and
reviewing changes in provider selections for a given configuration.

## What's next

- Learn about [general style and structure best practices for Terraform on Google Cloud](https://cloud.google.com/docs/terraform/best-practices/general-style-structure).
- Learn about [best practices when using reusable modules](https://cloud.google.com/docs/terraform/best-practices/reusable-modules).

   Was this helpful?

---

# Best practices for securityStay organized with collectionsSave and categorize content based on your preferences.

# Best practices for securityStay organized with collectionsSave and categorize content based on your preferences.

This document provides guidelines and recommendations for securely using
Terraform for Google Cloud. Terraform requires sensitive access to your
cloud infrastructure to operate. Following security best practices can help to
minimize the associated risks and improve your overall cloud security.

This guide is not an introduction to Terraform. For an introduction to using
Terraform with Google Cloud, see
[Get started with Terraform](https://cloud.google.com/docs/terraform/get-started-with-terraform).

## Use remote state

For Google Cloud customers, we recommend using the
[Cloud Storage state backend](https://www.terraform.io/docs/backends/types/gcs.html).
This approach locks the state to allow for collaboration as a team. It also
separates the state and all the potentially sensitive information from version
control.

Make sure that only the build system and highly privileged administrators can
access the bucket that is used for remote state.

To prevent accidentally committing development state to source control, use
[gitignore](https://github.com/github/gitignore/blob/master/Terraform.gitignore)
for Terraform state files.

## Encrypt state

Though Google Cloud buckets are encrypted at rest, you can use
[customer-supplied encryption keys](https://cloud.google.com/storage/docs/encryption#customer-supplied)
to provide an added layer of protection. Do this by using the
`GOOGLE_ENCRYPTION_KEY` environment variable. Even though no secrets should be
in the state file, always encrypt the state as an additional measure of defense.

## Don't store secrets in state

There are many resources and data providers in Terraform that store secret
values in plaintext in the state file. Where possible, avoid
storing secrets in state. Following are some examples of providers that store
secrets in plaintext:

- [vault_generic_secret](https://registry.terraform.io/providers/hashicorp/vault/latest/docs/resources/generic_secret)
- [tls_private_key](https://registry.terraform.io/providers/hashicorp/tls/latest/docs/resources/private_key)
- [google_service_account_key](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/google_service_account_key)
- [google_client_config](https://registry.terraform.io/providers/hashicorp/google/latest/docs/data-sources/client_config)

## Mark sensitive outputs

Instead of attempting to manually
[encrypt sensitive values](https://www.terraform.io/docs/extend/best-practices/sensitive-state.html),
rely on Terraform's built-in support for sensitive state management. When
exporting sensitive values to output, make sure that the values are marked as
[sensitive](https://www.terraform.io/docs/configuration/outputs.html#sensitive-suppressing-values-in-cli-output).

## Ensure separation of duties

If you can't run Terraform from an automated system where no users have access,
adhere to a separation of duties by separating permissions and directories. For
example, a network project would correspond with a network Terraform service
account or user whose access is limited to this project.

## Run pre-apply checks

When running Terraform in an automated pipeline, use a tool like
`gcloud terraform vet` to
[check plan output against policies](https://cloud.google.com/docs/terraform/policy-validation) before
it is applied. Doing so can detect security regressions before they happen.

## Run continuous audits

After the `terraform apply` command has executed, run automated security checks.
These checks can help to ensure that infrastructure doesn't drift into an
insecure state. The following tools are valid choices for this type of check:

- [Security Health Analytics](https://cloud.google.com/security-command-center/docs/how-to-use-security-health-analytics)
- [InSpec](https://inspec.io)
- [Serverspec](https://serverspec.org/)

## What's next

- Learn about [general style and structure best practices for Terraform on Google Cloud](https://cloud.google.com/docs/terraform/best-practices/general-style-structure).
- Learn about [best practices when using Terraform root modules](https://cloud.google.com/docs/terraform/best-practices/root-modules).

---

# Best practices for testingStay organized with collectionsSave and categorize content based on your preferences.

# Best practices for testingStay organized with collectionsSave and categorize content based on your preferences.

This document provides guidelines and recommendations for testing
Terraform for Google Cloud modules and configurations.

Testing Terraform modules and configurations sometimes follows different
patterns and conventions from testing application code. While testing
application code primarily involves testing the business logic of applications
themselves, fully testing infrastructure code requires deploying real cloud
resources to minimize the risk of production failures. There are a few
considerations when running Terraform tests:

- Running a Terraform test creates, modifies, and destroys real
  infrastructure, so your tests can potentially be time-consuming and expensive.
- *You cannot purely unit test an end-to-end architecture*. The best
  approach is to break up your architecture into modules and test those
  individually. The benefits of this approach include faster iterative
  development due to faster test runtime, reduced costs for each test, and
  reduced chances of test failures from factors beyond your control.
- *Avoid reusing state if possible*. There may be situations where you
  are testing with configurations that share data with other configurations,
  but ideally each test should be independent and should not reuse state
  across tests.

## Use less expensive test methods first

There are multiple methods that you can use to test Terraform. In ascending
order of cost, run time, and depth, they include the following:

- **Static analysis:** Testing the syntax and structure of your configuration
  without deploying any resources, using tools such as compilers, linters,
  and dry runs. To do so, use
  [terraform validate](https://www.terraform.io/cli/commands/validate)
- **Module integration testing**: To ensure that modules work correctly, test
  individual modules in isolation. Integration testing for modules
  involves deploying the module into a test environment and verifying that
  expected resources are created. There are several testing frameworks that
  make it easier to write tests, as follows:
  - [Google's blueprint testing framework](https://pkg.go.dev/github.com/GoogleCloudPlatform/cloud-foundation-toolkit/infra/blueprint-test)
  - [Terratest](https://terratest.gruntwork.io/)
  - [Kitchen-Terraform](https://newcontext-oss.github.io/kitchen-terraform/)
  - [InSpec](https://github.com/inspec/inspec-gcp)
  - [tftest](https://pypi.org/project/tftest/)
- **End-to-end testing:** By extending the integration testing approach to
  an entire environment, you can confirm that multiple modules work together.
  In this approach, deploy all modules that make up the architecture in a
  fresh test environment. Ideally, the test environment is as similar as
  possible to your production environment. This is costly but provides the
  greatest confidence that changes don't break your production environment.

## Start small

Make sure that your tests iteratively build on each other. Consider running
smaller tests first and then working up to more complex tests, using a
*fail fast* approach.

## Randomize project IDs and resource names

To avoid naming conflicts, make sure that your configurations have a globally
unique project ID and non-overlapping resource names within each project. To do
this, use namespaces for your resources. Terraform has a built-in
[random provider](https://registry.terraform.io/providers/hashicorp/random/latest/docs)
for this.

## Use a separate environment for testing

During testing, many resources are created and deleted. Ensure that the
environment is isolated from development or production projects to avoid
accidental deletions during resource cleanup. The best approach is to have each
test create a fresh project or folder. To avoid misconfiguration, consider
creating service accounts specifically for each test execution.

## Clean up all resources

Testing infrastructure code means that you are deploying actual resources.
To avoid incurring charges, consider implementing a clean-up step.

To destroy all remote objects managed by a particular configuration, use the
`terraform destroy` command. Some testing frameworks have a built-in cleanup
step for you. For example, if you are using Terratest, add
`defer terraform.Destroy(t, terraformOptions)` to your test. If you're using
 Kitchen-Terraform, delete your workspace using
`terraform kitchen delete WORKSPACE_NAME`.

After you run the `terraform destroy` command, also run additional clean-up
procedures to remove any resources that Terraform failed to destroy. Do this by
deleting any projects used for test execution or by using a tool like the
[project_cleanup](https://github.com/terraform-google-modules/terraform-google-scheduled-function/tree/master/modules/project_cleanup) module.

## Optimize test runtime

To optimize your test execution time, use the following approaches:

- **Run tests in parallel.** Some testing frameworks support running
  multiple Terraform tests simultaneously.
  - For example, with Terratest you can do this by adding
    `t.Parallel()` after the test function definition.
- **Test in stages.** Separate your tests into independent configurations
  that can be tested separately. This approach removes the need to go through
  all stages when running a test, and accelerates the iterative development
  cycle.
  - For example, in Kitchen-Terraform, split tests into
    separate suites. When iterating, execute each suite independently.
  - Similarly, using Terratest, wrap each stage of your test with
    `stage(t, STAGE_NAME, CORRESPONDING_TESTFUNCTION)`*.
    Set environment variables that indicate which tests to run. For example,SKIP*`STAGE_NAME="true"`.
  - The
    [blueprint testing framework](https://pkg.go.dev/github.com/GoogleCloudPlatform/cloud-foundation-toolkit/infra/blueprint-test)
    supports staged execution.

## What's next

- Learn about [general style and structure best practices for Terraform on Google Cloud](https://cloud.google.com/docs/terraform/best-practices/general-style-structure).
- Learn about [best practices when using Terraform root modules](https://cloud.google.com/docs/terraform/best-practices/root-modules).

   Was this helpful?

---

# Best practices for version controlStay organized with collectionsSave and categorize content based on your preferences.

# Best practices for version controlStay organized with collectionsSave and categorize content based on your preferences.

This document provides version control best practices to consider when using
Terraform for Google Cloud.

As with other forms of code, store infrastructure code in version control to
preserve history and allow easy rollbacks.

This guide is not an introduction to Terraform. For an introduction to using
Terraform with Google Cloud, see
[Get started with Terraform](https://cloud.google.com/docs/terraform/get-started-with-terraform).

## Use a default branching strategy

For all repositories that contain Terraform code, use the following strategy by
default:

- The `main` branch is the primary development branch and represents the
  latest approved code. The `main` branch is
  [protected](https://docs.gitlab.com/ee/user/project/protected_branches.html).
- Development happens on feature and bug-fix branches that branch off of the
  `main` branch.
  - Name feature branches `feature/$feature_name`.
  - Name bug-fix branches `fix/$bugfix_name`.
- When a feature or bug fix is complete, merge it back into the `main` branch
  with a pull request.
- To prevent merge conflicts, rebase branches before merging them.

## Use environment branches for root configurations

For repositories that include root configurations that are directly deployed to
Google Cloud, a safe rollout strategy is required. We recommend
having a separate *branch* for each environment. Thus, changes to the Terraform
configuration can be promoted by
[merging changes between the different branches](https://cloud.google.com/docs/terraform/resource-management/managing-infrastructure-as-code).

![Separate branch for each environment](https://docs.cloud.google.com/docs/terraform/images/folders-branches-environments.svg)

## Allow broad visibility

Make Terraform source code and repositories broadly visible and accessible
across engineering organizations, to infrastructure owners (for example, SREs)
and infrastructure stakeholders (for example, developers). This ensures that
infrastructure stakeholders can have a better understanding of the
infrastructure that they depend on.

Encourage infrastructure stakeholders to submit merge requests as part of the
change request process.

## Never commit secrets

Never commit secrets to source control, including in Terraform configuration.
Instead, upload them to a system like
[Secret Manager](https://cloud.google.com/secret-manager/docs) and reference them by using data
sources.

Keep in mind that such sensitive values might still end up in the state file
and might also be exposed as outputs.

## Organize repositories based on team boundaries

Although you can use separate directories to manage logical boundaries between
resources, organizational boundaries and logistics determine *repository*
structure. In general, use the design principle that configurations with
different approval and management requirements are separated into different
source control repositories. To illustrate this principle, these are some
possible repository configurations:

- **One central repository**: In this model, all Terraform code is
  centrally managed by a single platform team. This model works best when
  there is a dedicated infrastructure team responsible for all cloud
  management and approves any changes requested by other teams.
- **Team repositories:** In this model, each team is responsible for their
  own Terraform repository where they manage everything related to the
  infrastructure they own. For example, the security team might have a
  repository where all security controls are managed, and application teams
  each have their own Terraform repository to deploy and manage their
  application.
  Organizing repositories along team boundaries is the best structure for most
  enterprise scenarios.
- **Decoupled repositories**: In this model, each *logical* Terraform
  component is split into its own repository. For example, networking might
  have a dedicated repository, and there might be a separate project factory
  repository for project creation and management. This works best in highly
  decentralized environments where responsibilities frequently shift between
  teams.

### Sample repository structure

You can combine these principles to split Terraform configuration across
different repository types:

- Foundational
- Application and team-specific

#### Foundational repository

A *foundational* repository that contains major central
components, such as folders or org IAM. This repository
can be managed by the central cloud team.

- In this repository, include a directory for each major
  component (for example, folders, networks, and so on).
- In the component directories, include a separate folder for each
  environment (reflecting the directory structure guidance mentioned earlier).

![Foundational repository structure](https://docs.cloud.google.com/docs/terraform/images/repo-1-foundations.svg)

#### Application and team-specific repositories

Deploy *application and team-specific* repositories separately for each
team to manage their unique application-specific Terraform configuration.

![Application and team-specific repository structure](https://docs.cloud.google.com/docs/terraform/images/repo-n-application-platform-team-specific.svg)

## What's next

- Learn about [best practices for Terraform operations](https://cloud.google.com/docs/terraform/best-practices/operations).
- Learn about [best practices for using Terraform securely](https://cloud.google.com/docs/terraform/best-practices/security).

   Was this helpful?

---

# Best practices when working with Google Cloud resourcesStay organized with collectionsSave and categorize content based on your preferences.

# Best practices when working with Google Cloud resourcesStay organized with collectionsSave and categorize content based on your preferences.

Best practices for provisioning Google Cloud resources with Terraform, are
integrated into the [Cloud Foundation Toolkit](https://cloud.google.com/foundation-toolkit) modules that
Google maintains. This document reiterates some of these best practices.

This guide is not an introduction to Terraform. For an introduction to using
Terraform with Google Cloud, see
[Get started with Terraform](https://cloud.google.com/docs/terraform/get-started-with-terraform).

## Bake virtual machine images

In general, we recommend that you *bake* virtual machine images
[using a tool like Packer](https://cloud.google.com/compute/docs/images/image-management-best-practices#automated_baking).
Terraform then only needs to launch machines using the pre-baked images.

If pre-baked images are not available, Terraform can hand off new virtual
machines to a configuration management tool with a `provisioner` block. We
recommend that you avoid this method and only use it as a
[last resort](https://www.terraform.io/language/resources/provisioners/syntax#provisioners-are-a-last-resort).
To clean up old state associated with the instance, provisioners that require
teardown logic should use a `provisioner` block with `when = destroy`.

Terraform should provide VM configuration information to configuration
management with
[instance metadata](https://cloud.google.com/compute/docs/metadata/overview).

## Manage Identity and Access Management

When provisioning IAM associations with Terraform, several
different resources are available:

- `google_*_iam_policy` (for example, `google_project_iam_policy`)
- `google_*_iam_binding` (for example, `google_project_iam_binding`)
- `google_*_iam_member` (for example, `google_project_iam_member`)

`google_*_iam_policy` and `google_*_iam_binding` create *authoritative*
IAM associations, where the Terraform resources serve as the only
source of truth for what permissions can be assigned to the relevant resource.

If the permissions change outside of Terraform, Terraform on its next
execution overwrites all permissions to represent the policy as defined in your
configuration. This might make sense for resources that are wholly managed by a
particular Terraform configuration, but it means that roles that are
automatically managed by Google Cloud are removed—potentially disrupting
the functionality of some services.

To prevent this, we recommend using either `google_*_iam_member` resources
directly or the
[IAM module from Google](https://github.com/terraform-google-modules/terraform-google-iam).

## What's next

- Learn about [best practices for version control](https://cloud.google.com/docs/terraform/best-practices/version-control).
- Learn about [best practices for Terraform operations](https://cloud.google.com/docs/terraform/best-practices/operations).

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
