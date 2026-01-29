# Infrastructure as Code on Google CloudStay organized with collectionsSave and categorize content based on your preferences. and more

# Infrastructure as Code on Google CloudStay organized with collectionsSave and categorize content based on your preferences.

# Infrastructure as Code on Google CloudStay organized with collectionsSave and categorize content based on your preferences.

Infrastructure as Code (IaC) is the process of provisioning and managing software
application infrastructure using *code* instead of graphical user interfaces or
command-line scripts.

Provisioning application infrastructure typically involves setting up and
managing virtual machines, database connections, storage, and other
infrastructure elements. Manually managing this infrastructure is time consuming
and error prone, especially when managing applications at scale.

IaC lets you define your infrastructure with configuration files, which allow
you to build, change, and manage your infrastructure in a safe and repeatable
way. You can define resource configurations that you can version, reuse, and
share. IaC lets you specify the desired state of your infrastructure. You can
then deploy the same configuration multiple times to create reproducible
development, test, and production environments.

IaC allows you to treat your infrastructure provisioning and configuration in
the same manner as you handle application code. You can store your provisioning
configuration logic in source control and you can take advantage of continuous
integration and continuous deployment (CI/CD) pipelines.

## Benefits of IaC

Using IaC to set up and manage your application infrastructure is a best
practice for a number of common use cases. [Google manages its
systems with
IaC](https://www.usenix.org/publications/loginonline/prodspec-and-annealing-intent-based-actuation-google-production),
and established it as a [standard
practice](https://sre.google/workbook/configuration-design/) internally.

IaC offers the following benefits:

- You can define your infrastructure based on your requirements and
  reuse the same configuration to create multiple environments consistently.
- You can automate the creation and management of your cloud resources,
  including for deployment and test environments.
- You can treat infrastructure changes like you treat application changes. For
  example, you can ensure that changes to the configuration are reviewed and
  automatically validated. Managing production environments through
  change-controlled processes using IaC is a best practice.
- You can keep a history of all configuration changes. Changes can be audited
  and reverted.
- You can have a single source of truth for your cloud infrastructure.

## IaC tools for Google Cloud

Google Cloud is tightly integrated with many IaC tools. Choose one of the
following tools depending on your use case:

- **Terraform**
  In general, to configure and manage Google Cloud infrastructure using
  code, use the Terraform provider for Google Cloud.
  HashiCorp Terraform is an IaC tool that lets you define
  resources in cloud and on-premises in human-readable configuration files
  that you can version, reuse, and share. You can then use a consistent
  workflow to provision and manage all of your infrastructure throughout its
  lifecycle. For more information, see
  [Overview of Terraform on Google Cloud](https://cloud.google.com/docs/terraform/terraform-overview).
- **Infrastructure Manager**
  If you're looking to automate the deployment of your Terraform
  configuration, use Infrastructure Manager (Infra Manager).
  Infra Manager automates the deployment and management of
  Google Cloud infrastructure resources using Terraform.
  Infra Manager lets you deploy programmatically to
  Google Cloud, allowing you to use this service rather than maintaining
  a different toolchain to work with Terraform on Google Cloud. For more
  information, see [Infra Manager
  overview](https://cloud.google.com/infrastructure-manager/docs/overview).
- **Terraform Cloud and Terraform Enterprise**
  If you require full change management with Terraform across your
  organization, use Terraform Cloud or Terraform Enterprise.
  Terraform Cloud is a software as a service (SaaS) application that runs Terraform in a stable,
  remote environment and securely stores state and secrets. Terraform Cloud
  also integrates with the Terraform CLI and connects to common version
  control systems (VCS) like GitHub, GitLab, and Bitbucket. When you connect a
  Terraform Cloud workspace to a VCS repository, new commits and changes can
  automatically trigger Terraform plans. Terraform Cloud also offers an API,
  allowing you to integrate it into existing workflows.
  Terraform Enterprise lets you set up a self-hosted distribution of Terraform
  Cloud. It offers customizable resource limits and is ideal for organizations
  with strict security and compliance requirements.
  For more information, see the [Terraform Editions page in the Hashicorp
  documentation](https://developer.hashicorp.com/terraform/intro/terraform-editions).
- **Cloud Development Kit for Terraform**
  If you want to generate infrastructure with a general-purpose programming
  language instead of using Hashicorp Configuration Language (HCL), use Cloud
  Development Kit for Terraform (CDKTF).
  [CDKTF](https://developer.hashicorp.com/terraform/cdktf)
  lets you configure Terraform using a programming language to define and
  provision Google Cloud infrastructure and lets you use your existing
  toolchain for processes like testing and dependency management.
- **Pulumi**
  [Pulumi](https://www.pulumi.com/docs/clouds/gcp/)
  is another tool you can use to provision infrastructure using programming
  languages. You can use Google Cloud provider for Pulumi to author
  infrastructure code using programming languages such as TypeScript, Python,
  Go, C#, Java or YAML.
- **Config Controller and Config Connector**
  To manage Google Cloud resources through Kubernetes, use
  Config Controller and Config Connector.
  Config Controller and Config Connector let you configure
  Google Cloud services and resources using Kubernetes tooling. You can
  use GitOps tools like
  [Config Sync](https://cloud.google.com/anthos-config-management/docs/config-sync-overview), and
  Kubernetes APIs, and you can configure and use platform-engineering
  primitives such as admission webhooks and operators.
  For more information see the
  [Config Controller overview](https://cloud.google.com/anthos-config-management/docs/concepts/config-controller-overview)
  and [Config Connector overview](https://cloud.google.com/config-connector/docs/overview).
- **Crossplane**
  Another option to manage Google Cloud resources through Kubernetes is
  by using Crossplane.
  Crossplane connects your Kubernetes cluster to external, non-Kubernetes
  resources, and allows platform teams to build custom Kubernetes APIs to
  consume those resources. Crossplane acts as a
  [Kubernetes controller](https://kubernetes.io/docs/concepts/architecture/controller/)
  to watch the state of the external resources and provide state enforcement.
  With Crossplane installed in a Kubernetes cluster, users only communicate
  with Kubernetes. Crossplane manages the communication to external resources
  like Google Cloud. If something modifies or deletes a resource outside
  of Kubernetes, Crossplane reverses the change or recreates the deleted
  resource.
  For more information, see the
  [Crossplane documentation](https://docs.crossplane.io/v1.18/).
- **Ansible**
  If you want to automate provisioning, configuration management, application
  deployment, orchestration, and other IT processes, use Ansible. For more
  information, see [Ansible for
  Google Cloud](https://docs.ansible.com/ansible/latest/collections/google/cloud/).

## What's next

- Learn more about [Terraform](https://cloud.google.com/docs/terraform/terraform-overview)
- Learn how to
  [create a basic web server on Compute Engine using Terraform](https://cloud.google.com/docs/terraform/get-started-with-terraform)
- Learn how to
  [store Terraform state in a Cloud Storage bucket](https://cloud.google.com/docs/terraform/resource-management/store-state)

   Was this helpful?

---

# Install TerraformStay organized with collectionsSave and categorize content based on your preferences.

# Install TerraformStay organized with collectionsSave and categorize content based on your preferences.

This page describes the steps to install Terraform for
Google Cloud in [Cloud Shell](https://cloud.google.com/shell/docs) and in a local shell.
Cloud Shell is an interactive shell environment for Google Cloud
that lets you learn and experiment with Google Cloud and manage your
projects and resources from your web browser.

For a introductory guide to using Terraform with Google Cloud, see the
[Terraform for Google Cloud Quickstart](https://cloud.google.com/docs/terraform/create-vm-instance).

1. To use an online terminal with the gcloud CLI and Terraform
  already set up, activate Cloud Shell:
  At the bottom of this page, a Cloud Shell session starts and
  displays a command-line prompt. It can take a few seconds for the session
  to initialize.
2. Run the following command to verify that Terraform is available:
  ```
  terraform
  ```
  The output should be similar to the following:
  ```
  Usage: terraform [global options] <subcommand> [args]
  The available commands for execution are listed below.
  The primary workflow commands are given first, followed by
  less common or more advanced commands.
  Main commands:
    init          Prepare your working directory for other commands
    validate      Check whether the configuration is valid
    plan          Show changes required by the current configuration
    apply         Create or update infrastructure
    destroy       Destroy previously-created infrastructure
  ```
3. To use Terraform with Google Cloud, you should ensure the
   following tasks are completed within Google Cloud:
  - [Create or have a Google Cloud project](https://cloud.google.com/resource-manager/docs/creating-managing-projects).
  - [Enable billing](https://cloud.google.com/billing/docs/how-to/verify-billing-enabled#confirm_billing_is_enabled_on_a_project)
    for the Google Cloud project.
  - [Enable APIs](https://cloud.google.com/apis/docs/getting-started#enabling_apis) for the
    Google Cloud services you intend to work with.
  - [Set up authentication](https://cloud.google.com/docs/terraform/authentication) for
    Terraform.

1. Use the [installation instructions](https://developer.hashicorp.com/terraform/tutorials/gcp-get-started/install-cli)
   provided by Terraform.
2. Run the following command to verify that Terraform is available:
  ```
  terraform
  ```
  The output should be similar to the following:
  ```
  Usage: terraform [global options] <subcommand> [args]
  The available commands for execution are listed below.
  The primary workflow commands are given first, followed by
  less common or more advanced commands.
  Main commands:
    init          Prepare your working directory for other commands
    validate      Check whether the configuration is valid
    plan          Show changes required by the current configuration
    apply         Create or update infrastructure
    destroy       Destroy previously-created infrastructure
  ```
3. To use Terraform with Google Cloud, you should ensure the
   following tasks are completed within Google Cloud:
  - [Create or have a Google Cloud project](https://cloud.google.com/resource-manager/docs/creating-managing-projects).
  - [Enable billing](https://cloud.google.com/billing/docs/how-to/verify-billing-enabled#confirm_billing_is_enabled_on_a_project)
    for the Google Cloud project.
  - [Enable APIs](https://cloud.google.com/apis/docs/getting-started#enabling_apis) for the
    Google Cloud services you intend to work with.
  - [Set up authentication](https://cloud.google.com/docs/terraform/authentication) for
    Terraform.

## What's next

- Work through the
  [Terraform for Google Cloud quickstart](https://cloud.google.com/docs/terraform/create-vm-instance)
- Learn about the [basic Terraform commands](https://cloud.google.com/docs/terraform/basic-commands).

   Was this helpful?

---

# Terraform on Google Cloud maturity modelStay organized with collectionsSave and categorize content based on your preferences.

# Terraform on Google Cloud maturity modelStay organized with collectionsSave and categorize content based on your preferences.

This page explains the maturity model for Terraform on Google Cloud.
This model provides best practices, recommendations, and learning materials that
meet you at your level of comfort and expertise with Terraform on
Google Cloud.

## Overview

Terraform on Google Cloud has three user personas (Learners, Builders, and
Operators), and three stages of the maturity model (Adopt, Build, and Scale).

As organizations advance through the process of adopting, building, and scaling
Terraform on Google Cloud for their infrastructure use-cases, they need
accessible learning materials that provide the guidance they need wherever
they are at on their journey.

Determine which of these personas represent you the best and look
at the associated content to find resources that will help you and your
organization advance through the maturity stages, enabling you to apply your use
case to Terraform on Google Cloud at scale.

![Terraform on Google Cloud maturity model diagram](https://cloud.google.com/static/docs/terraform/images/terraform-maturity.png)

### Adopt (Learner)

Learners are beginning their journey on Google Cloud and focus on
opinionated guidance to learn how to use Terraform on Google Cloud and adopt it for their use case.

They may have some knowledge of Bash or other scripting languages,
but they don't use automation or CI/CD today to provision infrastructure.

You may be a **Learner** if you are:

- a developer
- new to Google Cloud, Infrastructure as Code, or Terraform

### Build (Builder)

Builders have experience with Infrastructure as Code and use Google Cloud
to build their projects.

They work with foundational infrastructure and a few applications on
Google Cloud. Builders plan on growing their cloud usage, specific use
cases, and customizations, and think about scaling and onboarding more teams or applications.

You may be a **Builder** if you are:

- a developer
- on a platform admin team
- on a Cloud team
- a SRE
- familiar with working on Google Cloud, Terraform, and have a
  Infrastructure as Code operation model

### Scale (Operator)

Operators are experienced with Google Cloud and use Terraform to provision infrastructure for their workloads at scale.

They scale and grow cloud usage, specific use cases, customizations, and onboard
more teams and workloads. Operators set policies and self serve workflows for
workload teams.

You may be an **Operator** if you are:

- on a platform admin team
- on a Cloud team
- a SRE
- experienced operating a Google Cloud, and a Terraform operation model at scale

## Criteria

This table details some of the criteria for each maturity stage to help you
determine which fits best with your level of familiarity with Terraform on
Google Cloud and your use case.

|  | Adopt | Build | Scale |
| --- | --- | --- | --- |
| Method | UI, CLI, and/or Terraform as a Service | Infrastructure as Code via Infra Manager | Infrastructure as Code via (1) Terraform OSS + Custom Pipelines or (2) Terraform Enterprise on Google Cloud |
| Automation | None or Limited | Limited | Yes |
| Consistency | None or Limited | Limited | Yes |
| Configuration | Unstructured, stored in a variety of locations | Structured, stored in a central location | Structured, stored in a version control system and versioned |
| Deployment | Manual | Automated using a CI/CD pipeline | Automated using a CI/CD pipeline |
| State | Not stored | Stored in a central location | Stored in a central location |
| Drift | Not monitored or managed | Monitored and managed | Monitored and managed |
| Documentation | Not maintained | Maintained | Well-documented |
| Review and Approval | Not required | Required | Required |
| Integration with Cloud Management Platform | Not integrated | Not integrated | Integrated with a cloud management platform |
| Range of Cloud Resources | Limited | Wide | Wide |
| Cost Optimization | Some concern | Some concern | Used |
| Security | Not a concern | Some concern | High concern |
| Compliance | Not a concern | Some concern | High concern |

## Recommendations

The following table lists some recommended topics based on the maturity stage of your
organization and your use case with Terraform on Google Cloud.

|  | Adopt | Build | Scale |
| --- | --- | --- | --- |
| Discover & Learn | Terraform on Google Cloud Landing pageHashiCorp Terraform docs | Terraform on Google Cloud docsHashiCorp Terraform docs | Architecture Center |
| Training & Tutorials | Get Started - Google Cloud (HashiCorp Learning Center)Get started with TerraformBasic Terraform commandsBest practicesCloud Skill Boost for Terraform(Beginner) | Manage infrastructure as codeCloud Skill Boost for Terraform(Intermediate)Cloud Foundations Toolkit 101Reuse Configuration with Modules | Export resources into TerraformImport resources into Terraform stateCloud Skill Boost for Terraform(Advanced)Policy:gcloud terraform vet |
| Templates/Ready to use | Jump Start SolutionsGoogle Cloud Terraform modules on GitHubTerraform Registry | Customize Jump Start SolutionsCustomize Terraform Blueprints and ModulesCreate your own Terraform BlueprintCreate your own Terraform module | Google Cloud Terraform modules on GitHub(customize for scale)Create & publish your own standardized Terraform Blueprints and modules |
| Deploy & Manage | Infrastructure ManagerCloud Shell + Terraform | Infrastructure ManagerTerraform GitOps with Cloud Build (CI/CD)Terraform Cloud or Enterprise on Google Cloud | Terraform GitOps with Cloud Build (CI/CD)Terraform Cloud or Enterprise on Google CloudGetting started with Terraform CDK in GCP |
|  | Support |  |  |
|  | Google Cloud Cloud Customer CareGoogle Cloud + HashiCorp Support (Priority support if customer has support for both) |  |  |

---

# Create CAI constraintsStay organized with collectionsSave and categorize content based on your preferences.

# Create CAI constraintsStay organized with collectionsSave and categorize content based on your preferences.

## Before you begin

- [Create a policy library](https://cloud.google.com/docs/terraform/policy-validation/create-policy-library).

## Constraint Framework

`gcloud beta terraform vet` uses
[Constraint Framework](https://github.com/open-policy-agent/frameworks/tree/master/constraint#opa-constraint-framework)
policies, which consist of *constraints* and *constraint templates*. The
difference between the two is as follows:

- A constraint template is like a function declaration; it defines a rule in
  [Rego](https://www.openpolicyagent.org/docs/how-do-i-write-policies.html)
  and optionally takes input parameters.
- A constraint is a file that references a constraint template and defines the
  input parameters to pass to it and the resources covered by the policy.

This allows you to avoid repetition. You can write a constraint template with a
generic policy, then write any number of constraints that provide different
input parameters or different resource matching rules.

## CAI Assets vs Terraform resources

Cloud Asset Inventory Assets are a standard Google data export format that is
available
[for many Google Cloud resources](https://cloud.google.com/docs/cloud-asset-inventory/overview#supported_resource_types).
CAI data is only usually available after a resource has been created or updated.
However, by converting Terraform resource changes to CAI Asset data,
`gcloud beta terraform vet` allows you to write a policy one time and use it both
before apply and as an audit check with compatible tools.

### Compatible tools

*The following tools are not official Google products and are not supported.*
However, they might be compatible with policies written for `gcloud beta terraform vet`:

- [CFT Scorecard](https://github.com/GoogleCloudPlatform/cloud-foundation-toolkit/blob/master/cli/docs/scorecard.md)
- [Forseti](https://opensource.google/projects/forsetisecurity)

## Create a constraint template

Before you develop your constraint template, verify that the Asset you want to
write a policy for is supported by both
[Cloud Asset Inventory](https://cloud.google.com/asset-inventory/docs/supported-asset-types)
and by [gcloud beta terraform vet](#supported-resources).

Creating a constraint template takes the following steps:

1. Collect sample data.
2. Write
  [Rego](https://www.openpolicyagent.org/docs/how-do-i-write-policies.html).
3. Test your Rego.
4. Set up a constraint template skeleton.
5. Inline your Rego.
6. Set up a constraint.

### Collect sample data

In order to write a constraint template, you need to have sample data to operate
on. CAI-based constraints operate on **CAI Asset data**. Gather sample data by
creating resources of the appropriate type and exporting those resources as
JSON, as described in the
[CAI quickstart](https://cloud.google.com/resource-manager/docs/cloud-asset-inventory/quickstart-cloud-asset-inventory).

Here is an example JSON export for a Compute Address:

```
[
  {
    "name": "//compute.googleapis.com/projects/789/regions/us-central1/addresses/my-internal-address",
    "asset_type": "compute.googleapis.com/Address",
    "ancestors: [
      "organization/123",
      "folder/456",
      "project/789"
    ],
    "resource": {
      "version": "v1",
      "discovery_document_uri": "https://www.googleapis.com/discovery/v1/apis/compute/v1/rest",
      "discovery_name": "Address",
      "parent": "//cloudresourcemanager.googleapis.com/projects/789",
      "data": {
        "address": "10.0.42.42",
        "addressType": "INTERNAL",
        "name": "my-internal-address",
        "region": "projects/789/global/regions/us-central1"
      }
    }
  },
]
```

### Write Rego

After you have sample data, you can write the logic for your constraint template
in
[Rego](https://www.openpolicyagent.org/docs/how-do-i-write-policies.html).
Your Rego must have a `violations` rule. The asset being reviewed is available
as `input.review`. Constraint parameters are available as `input.parameters`.
For example, to require that `compute.googleapis.com/Address` assets have an
allowed `addressType`, write:

```
# validator/gcp_compute_address_address_type_allowlist_constraint_v1.rego
package templates.gcp.GCPComputeAddressAddressTypeAllowlistConstraintV1

violation[{
  "msg": message,
  "details": metadata,
}] {
  asset := input.review
  asset.asset_type == "compute.googleapis.com/Address"

  allowed_address_types := input.parameters.allowed_address_types
  count({asset.resource.data.addressType} & allowed_address_types) >= 1
  message := sprintf(
    "Compute address %s has a disallowed address_type: %s",
    [asset.name, asset.resource.data.addressType]
  )
  metadata := {"asset": asset.name}
}
```

#### Name your constraint template

The previous example uses the name
`GCPComputeAddressAddressTypeAllowlistConstraintV1`. This is a unique identifier
for each constraint template. We recommend following these naming guidelines:

- General format: `GCP{resource}{feature}Constraint{version}`. Use CamelCase.
  (In other words, capitalize each new word.)
- For single-resource constraints, follow
  [gcloud](https://cloud.google.com/sdk/gcloud/) group names for resource
  naming. For example, use "compute" instead of "gce", "sql" instead of
  "cloud-sql", and "container-cluster" instead of "gke".
- If a template applies to more than one type of resource, omit the resource
  part and only include the feature (example:
  "GCPAddressTypeAllowlistConstraintV1").
- The version number does not follow semver form; it is just a single number.
  This effectively makes every version of a template an unique template.

We recommend using a name for your Rego file that matches the constraint
template name, but using snake_case. In other words, convert the name to
lowercase separate words with `_`. For the previous example, the recommended
filename is `gcp_compute_address_address_type_allowlist_constraint_v1.rego`

### Test your Rego

You can test your Rego manually with the
[Rego Playground](https://play.openpolicyagent.org/). Make sure to
use non-sensitive data.

We recommend writing
[automated tests](https://www.openpolicyagent.org/docs/how-do-i-test-policies.html).
Put your collected sample data in `validator/test/fixtures/<constraint
filename>/assets/data.json` and reference it in your test file like this:

```
# validator/gcp_compute_address_address_type_allowlist_constraint_v1_test.rego
package templates.gcp.GCPComputeAddressAddressTypeAllowlistConstraintV1

import data.test.fixtures.gcp_compute_address_address_type_allowlist_constraint_v1_test.assets as assets

test_violation_with_disallowed_address_type {
  parameters := {
    "allowed_address_types": "EXTERNAL"
  }
  violations := violation with input.review as assets[_]
    with input.parameters as parameters
  count(violations) == 1
}
```

Place your Rego and your test in the `validator` folder in your policy library.

### Set up a constraint template skeleton

After you have a working and tested Rego rule, you must package it as a
constraint template. Constraint Framework uses Kubernetes Custom Resource
Definitions as the container for the policy Rego.

The constraint template also defines what parameters are allowed as inputs from
constraints, using the
[OpenAPI V3](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.0.md#schemaObject)
schema.

Use the same name for the skeleton as you used for your Rego. In particular:

- Use the same filename as for your Rego. Example:
  `gcp_compute_address_address_type_allowlist_constraint_v1.yaml`
- `spec.crd.spec.names.kind` must contain the template name
- `metadata.name` must contain the template name, but lower-cased

Place the constraint template skeleton in `policies/templates`.

For the example above:

```
# policies/templates/gcp_compute_address_address_type_allowlist_constraint_v1.yaml
apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: gcpcomputeaddressaddresstypeallowlistconstraintv1
spec:
  crd:
    spec:
      names:
        kind: GCPComputeAddressAddressTypeAllowlistConstraintV1
      validation:
        openAPIV3Schema:
          properties:
            allowed_address_types:
              description: "A list of address_types allowed, for example: ['INTERNAL']"
              type: array
              items:
                type: string
  targets:
    - target: validation.gcp.forsetisecurity.org
      rego: |
            #INLINE("validator/gcp_compute_address_address_type_allowlist_constraint_v1.rego")
            #ENDINLINE
```

### Inline your Rego

At this point, following the previous example, your directory layout looks like
this:

```
| policy-library/
|- validator/
||- gcp_compute_address_address_type_allowlist_constraint_v1.rego
||- gcp_compute_address_address_type_allowlist_constraint_v1_test.rego
|- policies
||- templates
|||- gcp_compute_address_address_type_allowlist_constraint_v1.yaml
```

If you cloned the
[Google-provided policy-library repository](https://github.com/GoogleCloudPlatform/policy-library),
you can run `make build` to automatically update your constraint templates in
`policies/templates` with the Rego defined in `validator`.

### Set up a constraint

Constraints contain three pieces of information that `gcloud beta terraform vet` needs
to properly enforce and report violations:

- `severity`: `low`, `medium`, or `high`
- `match`: parameters for determining if a constraint applies to a particular
  resource. The following match parameters are supported:
  - `ancestries`: A list of ancestry paths to include using glob-style
    matching
  - `excludedAncestries`: (Optional) A list of ancestry paths to exclude
    using glob-style matching.
- `parameters`: Values for the constraint template's input parameters.

Make sure that `kind` contains the constraint template name. We recommend
setting `metadata.name` to a descriptive slug.

For example, to only allow `INTERNAL` address types using the previous example
constraint template, write:

```
# policies/constraints/gcp_compute_address_internal_only.yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: GCPComputeAddressAddressTypeAllowlistConstraintV1
metadata:
  name: gcp_compute_address_internal_only
spec:
  severity: high
  match:
    ancestries:
    - "**"
  parameters:
    allowed_address_types:
    - "INTERNAL"
```

Matching examples:

| Ancestry path matcher | Description |
| --- | --- |
| organizations/** | All organizations |
| organizations/123/** | Everything in organization 123 |
| organizations/123/folders/** | Everything in organization 123 that is under a folder |
| organizations/123/folders/456 | Everything in folder 456 in organization 123 |
| organizations/123/folders/456/projects/789 | Everything in project 789 in folder 456 in organization 123 |

If a resource address matches values in `ancestries` and `excludedAncestries`,
it is excluded.

## Limitations

Terraform plan data gives the best available representation of actual state
after apply. However, in many cases, the state after apply might not be known
because it is calculated on the server side. In these cases, the data is not
available in the converted CAI Assets either.

Building CAI ancestry paths is part of the process when validating policies. It
uses the default project provided to get around unknown project IDs. In the
case where a default project is not provided, the ancestry path defaults to
`organizations/unknown`.

You can disallow unknown ancestry by adding the following constraint:

```
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: GCPAlwaysViolatesConstraintV1
metadata:
  name: disallow_unknown_ancestry
  annotations:
    description: |
      Unknown ancestry is not allowed; use --project=<project> to set a
      default ancestry
spec:
  severity: high
  match:
    ancestries:
    - "organizations/unknown"
  parameters: {}
```

### Supported resources

If you want `gcloud beta terraform vet` to add support for a resource that is not on
this list, open an
[enhancement request](https://github.com/GoogleCloudPlatform/terraform-google-conversion/issues/new?assignees=&labels=enhancement&projects=&template=enhancement.md)
and consider
[contributing code](https://github.com/GoogleCloudPlatform/terraform-google-conversion/blob/main/docs/contributing/index.md).

The list of supported resources depends on which version of `gcloud beta terraform vet`
is installed. The current list of supported resources follows:

| Terraform resource | Cloud Asset Inventory Assets |
| --- | --- |
| google_access_context_manager_access_policy_iam_binding | accesscontextmanager.googleapis.com/AccessPolicy |
| google_access_context_manager_access_policy_iam_member | accesscontextmanager.googleapis.com/AccessPolicy |
| google_access_context_manager_access_policy_iam_policy | accesscontextmanager.googleapis.com/AccessPolicy |
| google_access_context_manager_service_perimeter | accesscontextmanager.googleapis.com/ServicePerimeter |
| google_apigee_environment_iam_binding | apigee.googleapis.com/Environment |
| google_apigee_environment_iam_member | apigee.googleapis.com/Environment |
| google_apigee_environment_iam_policy | apigee.googleapis.com/Environment |
| google_bigquery_dataset | bigquery.googleapis.com/Dataset |
| google_bigquery_dataset_iam_binding | bigquery.googleapis.com/Dataset |
| google_bigquery_dataset_iam_member | bigquery.googleapis.com/Dataset |
| google_bigquery_dataset_iam_policy | bigquery.googleapis.com/Dataset |
| google_bigquery_table | bigquery.googleapis.com/Table |
| google_bigquery_table_iam_binding | bigquery.googleapis.com/Table |
| google_bigquery_table_iam_member | bigquery.googleapis.com/Table |
| google_bigquery_table_iam_policy | bigquery.googleapis.com/Table |
| google_bigtable_instance | bigtableadmin.googleapis.com/Cluster, bigtableadmin.googleapis.com/Instance |
| google_binary_authorization_attestor_iam_binding | binaryauthorization.googleapis.com/Attestor |
| google_binary_authorization_attestor_iam_member | binaryauthorization.googleapis.com/Attestor |
| google_binary_authorization_attestor_iam_policy | binaryauthorization.googleapis.com/Attestor |
| google_cloud_run_domain_mapping | run.googleapis.com/DomainMapping |
| google_cloud_run_service | run.googleapis.com/Service |
| google_cloud_run_service_iam_binding | run.googleapis.com/Service |
| google_cloud_run_service_iam_member | run.googleapis.com/Service |
| google_cloud_run_service_iam_policy | run.googleapis.com/Service |
| google_cloudfunctions_function | cloudfunctions.googleapis.com/CloudFunction |
| google_cloudfunctions_function_iam_binding | cloudfunctions.googleapis.com/CloudFunction |
| google_cloudfunctions_function_iam_member | cloudfunctions.googleapis.com/CloudFunction |
| google_cloudfunctions_function_iam_policy | cloudfunctions.googleapis.com/CloudFunction |
| google_compute_address | compute.googleapis.com/Address |
| google_compute_backend_service_iam_binding | compute.googleapis.com/BackendService |
| google_compute_backend_service_iam_member | compute.googleapis.com/BackendService |
| google_compute_backend_service_iam_policy | compute.googleapis.com/BackendService |
| google_compute_disk | compute.googleapis.com/Disk |
| google_compute_disk_iam_binding | compute.googleapis.com/Disk |
| google_compute_disk_iam_member | compute.googleapis.com/Disk |
| google_compute_disk_iam_policy | compute.googleapis.com/Disk |
| google_compute_firewall | compute.googleapis.com/Firewall |
| google_compute_forwarding_rule | compute.googleapis.com/ForwardingRule |
| google_compute_global_address | compute.googleapis.com/GlobalAddress |
| google_compute_global_forwarding_rule | compute.googleapis.com/GlobalForwardingRule |
| google_compute_image_iam_binding | compute.googleapis.com/Image |
| google_compute_image_iam_member | compute.googleapis.com/Image |
| google_compute_image_iam_policy | compute.googleapis.com/Image |
| google_compute_instance | compute.googleapis.com/Instance |
| google_compute_instance_iam_binding | compute.googleapis.com/Instance |
| google_compute_instance_iam_member | compute.googleapis.com/Instance |
| google_compute_instance_iam_policy | compute.googleapis.com/Instance |
| google_compute_network | compute.googleapis.com/Network |
| google_compute_region_backend_service_iam_binding | compute.googleapis.com/RegionBackendService |
| google_compute_region_backend_service_iam_member | compute.googleapis.com/RegionBackendService |
| google_compute_region_backend_service_iam_policy | compute.googleapis.com/RegionBackendService |
| google_compute_region_disk_iam_binding | compute.googleapis.com/RegionDisk |
| google_compute_region_disk_iam_member | compute.googleapis.com/RegionDisk |
| google_compute_region_disk_iam_policy | compute.googleapis.com/RegionDisk |
| google_compute_security_policy | compute.googleapis.com/SecurityPolicy |
| google_compute_snapshot | compute.googleapis.com/Snapshot |
| google_compute_ssl_policy | compute.googleapis.com/SslPolicy |
| google_compute_subnetwork | compute.googleapis.com/Subnetwork |
| google_compute_subnetwork_iam_binding | compute.googleapis.com/Subnetwork |
| google_compute_subnetwork_iam_member | compute.googleapis.com/Subnetwork |
| google_compute_subnetwork_iam_policy | compute.googleapis.com/Subnetwork |
| google_container_cluster | container.googleapis.com/Cluster |
| google_container_node_pool | container.googleapis.com/NodePool |
| google_data_catalog_entry_group_iam_binding | datacatalog.googleapis.com/EntryGroup |
| google_data_catalog_entry_group_iam_member | datacatalog.googleapis.com/EntryGroup |
| google_data_catalog_entry_group_iam_policy | datacatalog.googleapis.com/EntryGroup |
| google_data_catalog_tag_template_iam_binding | datacatalog.googleapis.com/TagTemplate |
| google_data_catalog_tag_template_iam_member | datacatalog.googleapis.com/TagTemplate |
| google_data_catalog_tag_template_iam_policy | datacatalog.googleapis.com/TagTemplate |
| google_dns_managed_zone | dns.googleapis.com/ManagedZone |
| google_dns_policy | dns.googleapis.com/Policy |
| google_endpoints_service_consumers_iam_binding | servicemanagement.googleapis.com/ServiceConsumers |
| google_endpoints_service_consumers_iam_member | servicemanagement.googleapis.com/ServiceConsumers |
| google_endpoints_service_consumers_iam_policy | servicemanagement.googleapis.com/ServiceConsumers |
| google_endpoints_service_iam_binding | servicemanagement.googleapis.com/Service |
| google_endpoints_service_iam_member | servicemanagement.googleapis.com/Service |
| google_endpoints_service_iam_policy | servicemanagement.googleapis.com/Service |
| google_filestore_instance | file.googleapis.com/Instance |
| google_folder_iam_binding | cloudresourcemanager.googleapis.com/Folder |
| google_folder_iam_member | cloudresourcemanager.googleapis.com/Folder |
| google_folder_iam_policy | cloudresourcemanager.googleapis.com/Folder |
| google_folder_organization_policy | cloudresourcemanager.googleapis.com/Folder |
| google_healthcare_consent_store_iam_binding | healthcare.googleapis.com/ConsentStore |
| google_healthcare_consent_store_iam_member | healthcare.googleapis.com/ConsentStore |
| google_healthcare_consent_store_iam_policy | healthcare.googleapis.com/ConsentStore |
| google_iap_tunnel_iam_binding | iap.googleapis.com/Tunnel |
| google_iap_tunnel_iam_member | iap.googleapis.com/Tunnel |
| google_iap_tunnel_iam_policy | iap.googleapis.com/Tunnel |
| google_iap_tunnel_instance_iam_binding | iap.googleapis.com/TunnelInstance |
| google_iap_tunnel_instance_iam_member | iap.googleapis.com/TunnelInstance |
| google_iap_tunnel_instance_iam_policy | iap.googleapis.com/TunnelInstance |
| google_iap_web_iam_binding | iap.googleapis.com/Web |
| google_iap_web_iam_member | iap.googleapis.com/Web |
| google_iap_web_iam_policy | iap.googleapis.com/Web |
| google_kms_crypto_key | cloudkms.googleapis.com/CryptoKey |
| google_kms_crypto_key_iam_binding | cloudkms.googleapis.com/CryptoKey |
| google_kms_crypto_key_iam_member | cloudkms.googleapis.com/CryptoKey |
| google_kms_crypto_key_iam_policy | cloudkms.googleapis.com/CryptoKey |
| google_kms_key_ring | cloudkms.googleapis.com/KeyRing |
| google_kms_key_ring_iam_binding | cloudkms.googleapis.com/KeyRing |
| google_kms_key_ring_iam_member | cloudkms.googleapis.com/KeyRing |
| google_kms_key_ring_iam_policy | cloudkms.googleapis.com/KeyRing |
| google_monitoring_alert_policy | monitoring.googleapis.com/AlertPolicy |
| google_monitoring_notification_channel | monitoring.googleapis.com/NotificationChannel |
| google_notebooks_instance_iam_binding | notebooks.googleapis.com/Instance |
| google_notebooks_instance_iam_member | notebooks.googleapis.com/Instance |
| google_notebooks_instance_iam_policy | notebooks.googleapis.com/Instance |
| google_notebooks_runtime_iam_binding | notebooks.googleapis.com/Runtime |
| google_notebooks_runtime_iam_member | notebooks.googleapis.com/Runtime |
| google_notebooks_runtime_iam_policy | notebooks.googleapis.com/Runtime |
| google_organization_iam_binding | cloudresourcemanager.googleapis.com/Organization |
| google_organization_iam_custom_role | iam.googleapis.com/Role |
| google_organization_iam_member | cloudresourcemanager.googleapis.com/Organization |
| google_organization_iam_policy | cloudresourcemanager.googleapis.com/Organization |
| google_organization_policy | cloudresourcemanager.googleapis.com/Organization |
| google_privateca_ca_pool_iam_binding | privateca.googleapis.com/CaPool |
| google_privateca_ca_pool_iam_member | privateca.googleapis.com/CaPool |
| google_privateca_ca_pool_iam_policy | privateca.googleapis.com/CaPool |
| google_privateca_certificate_template_iam_binding | privateca.googleapis.com/CertificateTemplate |
| google_privateca_certificate_template_iam_member | privateca.googleapis.com/CertificateTemplate |
| google_privateca_certificate_template_iam_policy | privateca.googleapis.com/CertificateTemplate |
| google_project | cloudbilling.googleapis.com/ProjectBillingInfo, cloudresourcemanager.googleapis.com/Project |
| google_project_iam_binding | cloudresourcemanager.googleapis.com/Project |
| google_project_iam_custom_role | iam.googleapis.com/Role |
| google_project_iam_member | cloudresourcemanager.googleapis.com/Project |
| google_project_iam_policy | cloudresourcemanager.googleapis.com/Project |
| google_project_organization_policy | cloudresourcemanager.googleapis.com/Project |
| google_project_service | serviceusage.googleapis.com/Service |
| google_pubsub_lite_reservation | pubsublite.googleapis.com/Reservation |
| google_pubsub_lite_subscription | pubsublite.googleapis.com/Subscription |
| google_pubsub_lite_topic | pubsublite.googleapis.com/Topic |
| google_pubsub_schema | pubsub.googleapis.com/Schema |
| google_pubsub_subscription | pubsub.googleapis.com/Subscription |
| google_pubsub_subscription_iam_binding | pubsub.googleapis.com/Subscription |
| google_pubsub_subscription_iam_member | pubsub.googleapis.com/Subscription |
| google_pubsub_subscription_iam_policy | pubsub.googleapis.com/Subscription |
| google_pubsub_topic | pubsub.googleapis.com/Topic |
| google_pubsub_topic_iam_binding | pubsub.googleapis.com/Topic |
| google_pubsub_topic_iam_member | pubsub.googleapis.com/Topic |
| google_pubsub_topic_iam_policy | pubsub.googleapis.com/Topic |
| google_redis_instance | redis.googleapis.com/Instance |
| google_secret_manager_secret_iam_binding | secretmanager.googleapis.com/Secret |
| google_secret_manager_secret_iam_member | secretmanager.googleapis.com/Secret |
| google_secret_manager_secret_iam_policy | secretmanager.googleapis.com/Secret |
| google_spanner_database | spanner.googleapis.com/Database |
| google_spanner_database_iam_binding | spanner.googleapis.com/Database |
| google_spanner_database_iam_member | spanner.googleapis.com/Database |
| google_spanner_database_iam_policy | spanner.googleapis.com/Database |
| google_spanner_instance | spanner.googleapis.com/Instance |
| google_spanner_instance_iam_binding | spanner.googleapis.com/Instance |
| google_spanner_instance_iam_member | spanner.googleapis.com/Instance |
| google_spanner_instance_iam_policy | spanner.googleapis.com/Instance |
| google_sql_database | sqladmin.googleapis.com/Database |
| google_sql_database_instance | sqladmin.googleapis.com/Instance |
| google_storage_bucket | storage.googleapis.com/Bucket |
| google_storage_bucket_iam_binding | storage.googleapis.com/Bucket |
| google_storage_bucket_iam_member | storage.googleapis.com/Bucket |
| google_storage_bucket_iam_policy | storage.googleapis.com/Bucket |
| google_vpc_access_connector | vpcaccess.googleapis.com/Connector |

   Was this helpful?

---

# Create a policy libraryStay organized with collectionsSave and categorize content based on your preferences.

# Create a policy libraryStay organized with collectionsSave and categorize content based on your preferences.

As an organization administrator, you need to define policies that developers adhere to when applying infrastructure as code. Your organization's set of policies is represented as a policy library. This page helps you create a centralized policy repository and add constraints.

## Before you begin

- You need an empty Git repository for storing your organization's policy library.
- You need to configure Git to connect securely. For example, if your git repository is on GitHub, you can follow the process outlined in [Connecting to GitHub with SSH](https://docs.github.com/en/authentication/connecting-to-github-with-ssh).

## Duplicate the sample library

Google provides a sample repository that includes a set of pre-defined constraint templates which you can modify for your personal use.

1. Clone the policy library sample repository and duplicate it to your POLICY_LIBRARY_REPO:
  ```
  git clone https://github.com/GoogleCloudPlatform/policy-library.git
  cd policy-library
  git remote set-url origin POLICY_LIBRARY_REPO
  git push origin main
  ```
2. Examine the available constraint templates in `policies/templates`:
  `ls policies/templates`
3. Select the constraint templates you want to use. For this example, choose `gcp_storage_location_v1.yaml`, which enforces location for Cloud Storage buckets.
4. Create constraint YAML files corresponding to those templates under `policies/constraints`.
5. From inside your local copy of the `policy-library` repository, use the following commands to commit and push your changes:
  ```
  git add --all .
  git commit -m "Initial commit of policy library constraints"
  git push -u origin main
  ```

### Library structure

A policy library repository contains the following directories:

- `policies/` – This directory contains two subdirectories:
  - `constraints/` – This directory is initially empty. Place your constraint files here.
  - `templates/` – This directory contains pre-defined constraint templates.
- `validator/` – This directory contains the `.rego` files and their associated unit tests. You don't need to touch this directory unless you intend to modify existing constraint templates or create new ones. Running `make build` inlines the Rego content in the corresponding constraint template files.

## Periodic updates

Periodically you should pull any changes from the public repository, which might contain new templates and Rego files.

```
git remote add public https://github.com/GoogleCloudPlatform/policy-library.git
git pull public main
git push origin main
```

## Next steps

The policy library contains a number of constraint templates and a `samples`
folder with example constraints. Read
[Create Terraform constraints](https://cloud.google.com/docs/terraform/policy-validation/create-terraform-constraints)
or
[Create CAI constraints](https://cloud.google.com/docs/terraform/policy-validation/create-cai-constraints)
for details on how to write and use constraint templates and constraints.

   Was this helpful?
