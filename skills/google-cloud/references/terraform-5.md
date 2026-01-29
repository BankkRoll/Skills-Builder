# Create Terraform constraintsStay organized with collectionsSave and categorize content based on your preferences. and more

# Create Terraform constraintsStay organized with collectionsSave and categorize content based on your preferences.

# Create Terraform constraintsStay organized with collectionsSave and categorize content based on your preferences.

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

## Create a constraint template

To create a constraint template, follow these steps:

1. Collect sample data.
2. Write
  [Rego](https://www.openpolicyagent.org/docs/how-do-i-write-policies.html).
3. Test your Rego.
4. Set up a constraint template skeleton.
5. Inline your Rego.
6. Set up a constraint.

### Collect sample data

In order to write a constraint template, you need to have sample data to operate
on. Terraform-based constraints operate on **resource change data**, which comes
from the `resource_changes` key of
[Terraform plan JSON](https://www.terraform.io/docs/internals/json-format.html).

For example, your JSON might look like this:

```
// tfplan.json
{
  "format_version": "0.2",
  "terraform_version": "1.0.10",
  "resource_changes": [
    {
      "address": "google_compute_address.internal_with_subnet_and_address",
      "mode": "managed",
      "type": "google_compute_address",
      "name": "internal_with_subnet_and_address",
      "provider_name": "registry.terraform.io/hashicorp/google",
      "change": {
        "actions": [
          "create"
        ],
        "before": null,
        "after": {
          "address": "10.0.42.42",
          "address_type": "INTERNAL",
          "description": null,
          "name": "my-internal-address",
          "network": null,
          "prefix_length": null,
          "region": "us-central1",
          "timeouts": null
        },
        "after_unknown": {
          "creation_timestamp": true,
          "id": true,
          "network_tier": true,
          "project": true,
          "purpose": true,
          "self_link": true,
          "subnetwork": true,
          "users": true
        },
        "before_sensitive": false,
        "after_sensitive": {
          "users": []
        }
      }
    }
  ],
  // other data
}
```

### Write Rego

After you have sample data, you can write the logic for your constraint template
in
[Rego](https://www.openpolicyagent.org/docs/how-do-i-write-policies.html).
Your Rego must have a `violations` rule. The resource change being reviewed is
available as `input.review`. Constraint parameters are available as
`input.parameters`. For example, to require that `google_compute_address`
resources have an allowed `address_type`, write:

```
# validator/tf-compute-address-address-type-allowlist-constraint-v1.rego
package templates.gcp.TFComputeAddressAddressTypeAllowlistConstraintV1

violation[{
  "msg": message,
  "details": metadata,
}] {
  resource := input.review
  resource.type == "google_compute_address"

  allowed_address_types := input.parameters.allowed_address_types
  count({resource.change.after.address_type} & allowed_address_types) >= 1
  message := sprintf(
    "Compute address %s has a disallowed address_type: %s",
    [resource.address, resource.change.after.address_type]
  )
  metadata := {"resource": resource.name}
}
```

#### Name your constraint template

The previous example uses the name
`TFComputeAddressAddressTypeAllowlistConstraintV1`. This is a unique identifier
for each constraint template. We recommend following these naming guidelines:

- General format: `TF{resource}{feature}Constraint{version}`. Use CamelCase.
  (In other words, capitalize each new word.)
- For single-resource constraints, follow the
  [Terraform provider's](https://registry.terraform.io/providers/hashicorp/google/latest/docs)
  conventions for product naming. For example, for `google_tags_tag` the
  product name is `tags` even though the API name is `resourcemanager`.
- If a template applies to more than one type of resource, omit the resource
  part and only include the feature (example:
  "TFAddressTypeAllowlistConstraintV1").
- The version number does not follow semver form; it is just a single number.
  This effectively makes every version of a template an unique template.

We recommend using a name for your Rego file that matches the constraint
template name, but using snake_case. In other words, convert the name to
lowercase separate words with `_`. For the previous example, the recommended
filename is `tf-compute-address-address-type-allowlist-constraint-v1.rego`

### Test your Rego

You can test your Rego manually with the
[Rego Playground](https://play.openpolicyagent.org/). Make sure to
use non-sensitive data.

We recommend writing
[automated tests](https://www.openpolicyagent.org/docs/how-do-i-test-policies.html).
Put your collected sample data in `validator/test/fixtures/<constraint
filename>/resource_changes/data.json` and reference it in your test file like
this:

```
# validator/tf-compute-address-address-type-allowlist-constraint-v1-test.rego
package templates.gcp.TFComputeAddressAddressTypeAllowlistConstraintV1

import data.test.fixtures.tf-compute-address-address-type-allowlist-constraint-v1-test.resource_changes as resource_changes

test_violation_with_disallowed_address_type {
  parameters := {
    "allowed_address_types": "EXTERNAL"
  }
  violations := violation with input.review as resource_changes[_]
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
  `tf-compute-address-address-type-allowlist-constraint-v1.yaml`
- `spec.crd.spec.names.kind` must contain the template name
- `metadata.name` must contain the template name, but lower-cased

Place the constraint template skeleton in `policies/templates`.

For example:

```
# policies/templates/tf-compute-address-address-type-allowlist-constraint-v1.yaml
apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: tfcomputeaddressaddresstypeallowlistconstraintv1
spec:
  crd:
    spec:
      names:
        kind: TFComputeAddressAddressTypeAllowlistConstraintV1
      validation:
        openAPIV3Schema:
          properties:
            allowed_address_types:
              description: "A list of address_types allowed, for example: ['INTERNAL']"
              type: array
              items:
                type: string
  targets:
    - target: validation.resourcechange.terraform.cloud.google.com
      rego: |
            #INLINE("validator/tf-compute-address-address-type-allowlist-constraint-v1.rego")
            #ENDINLINE
```

### Inline your Rego

At this point, following the previous example, your directory layout looks like
this:

```
| policy-library/
|- validator/
||- tf-compute-address-address-type-allowlist-constraint-v1.rego
||- tf-compute-address-address-type-allowlist-constraint-v1-test.rego
|- policies
||- templates
|||- tf-compute-address-address-type-allowlist-constraint-v1.yaml
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
  - `addresses`: A list of resource addresses to include using glob-style
    matching
  - `excludedAddresses`: (Optional) A list of resource addresses to exclude
    using glob-style matching.
- `parameters`: Values for the constraint template's input parameters.

Make sure that `kind` contains the constraint template name. We recommend
setting `metadata.name` to a descriptive slug.

For example, to only allow `INTERNAL` address types using the previous example
constraint template, write:

```
# policies/constraints/tf_compute_address_internal_only.yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: TFComputeAddressAddressTypeAllowlistConstraintV1
metadata:
  name: tf_compute_address_internal_only
spec:
  severity: high
  match:
    addresses:
    - "**"
  parameters:
    allowed_address_types:
    - "INTERNAL"
```

Matching examples:

| Address matcher | Description |
| --- | --- |
| module.** | All resources in any module |
| module.my_module.** | Everything in modulemy_module |
| **.google_compute_global_forwarding_rule.* | All google_compute_global_forwarding_rule resources in any module |
| module.my_module.google_compute_global_forwarding_rule.* | All google_compute_global_forwarding_rule resources in `my_module` |

If a resource address matches values in `addresses` and `excludedAddresses`, it
is excluded.

## Limitations

Terraform plan data gives the best available representation of actual state
after apply. However, in many cases, the state after apply might not be known
because it is calculated on the server side.

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

## Supported resources

You can create resource change constraints for any Terraform resource from any
Terraform provider.

   Was this helpful?

---

# Migrate from terraform

# Migrate from terraform-validatorStay organized with collectionsSave and categorize content based on your preferences.

`gcloud beta terraform vet` is a replacement for the open-source
[terraform-validator](https://github.com/GoogleCloudPlatform/terraform-validator/)
project, with a few minor differences. If you are migrating your CI/CD pipeline
to use `gcloud beta terraform vet`, you will need to make the following changes.

## 1.Update the command and args

- Replace `terraform-validator validate` with `gcloud beta terraform vet`
- Replace `--policy-path` with `--policy-library`

Basic example:

```
# Old
terraform-validator validate ./tfplan.json --policy-path=/path/to/policy-library

# New
gcloud beta terraform vet ./tfplan.json --policy-library=/path/to/policy-library
```

With [service account impersonation](https://cloud.google.com/sdk/gcloud/reference#--impersonate-service-account):

```
# Old
GOOGLE_IMPERSONATE_SERVICE_ACCOUNT=account@project.iam.gserviceaccount.com
terraform-validator validate ./tfplan.json --policy-path=/path/to/policy-library

# New
gcloud beta terraform vet ./tfplan.json --policy-library=/path/to/policy-library \
  --impersonate-service-account=account@project.iam.gserviceaccount.com
```

## 2.(Optional) Upgrade constraint templates

`terraform-validator` documentation historically gave instructions on how to
write `v1alpha1` Constraint Framework policies; there is a newer format that we
recommend for
[writing new policies](https://github.com/GoogleCloudPlatform/policy-library/blob/main/docs/constraint_template_authoring.md).
You can also
[upgrade existing policies to use the new format](https://github.com/GoogleCloudPlatform/policy-library/blob/main/docs/constraint_template_authoring.md#updating-from-v1alpha1-templates)

For policies sourced from
[github.com/GoogleCloudPlatform/policy-library](https://github.com/GoogleCloudPlatform/policy-library),
we recommend staying in sync with the remote repository.

   Was this helpful?

---

# gcloud beta terraform vet quickstartStay organized with collectionsSave and categorize content based on your preferences.

# gcloud beta terraform vet quickstartStay organized with collectionsSave and categorize content based on your preferences.

This quickstart shows you how to apply a constraint that enforces a domain restriction. You'll test that constraint and intentionally throw an error. Then you'll modify the constraint so that your domain passes.

## Before you begin

- You need a [Google Cloud project](https://cloud.google.com/resource-manager/docs/creating-managing-projects).
- You need the following [Identity and Access Management (IAM) permissions](https://cloud.google.com/resource-manager/docs/access-control-proj) for that project:
  - `resourcemanager.projects.getIamPolicy` – This permission can be granted with the Security Reviewer role for the organization.
  - `resourcemanager.projects.get` – This permission can be granted with the Project Viewer role for the organization.

To get you started quickly, these instructions use a Cloud Shell that's pre-installed with Terraform, and with a [cloned Policy Library repository](https://cloud.google.com/docs/terraform/policy_validation/create_policy_library#duplicate_the_sample_library). The instructions assume you already have a Google Cloud account.

## Quickstart

1. Go to the Cloud Shell and clone the policy library.
  [Clone policy library](https://console.cloud.google.com/cloudshell/open?cloudshell_git_repo=https://github.com/GoogleCloudPlatform/policy-library.git)
2. Copy the sample IAM domain restriction constraint into
  the `policies/constraints` directory.
  ```
  cp samples/iam_service_accounts_only.yaml policies/constraints
  ```
3. Examine the constraint you copied by printing it to the terminal.
  ```
  cat policies/constraints/iam_service_accounts_only.yaml
  ```
  The output looks like this:
  ```
  # This constraint checks that all IAM policy members are in the
  # "gserviceaccount.com" domain.
  apiVersion: constraints.gatekeeper.sh/v1alpha1
  kind: GCPIAMAllowedPolicyMemberDomainsConstraintV2
  metadata:
    name: service_accounts_only
    annotations:
      description: Checks that members that have been granted IAM roles belong to allowlisted
        domains.
  spec:
    severity: high
    match:
      target: # {"$ref":"#/definitions/io.k8s.cli.setters.target"}
      - "organizations/**"
    parameters:
      domains:
      - gserviceaccount.com
  ```
  Notice `gserviceaccount.com` at the bottom. This specifies that only members
  from the `gserviceaccount.com` domain can be present in an IAM
  policy.
4. To verify that the policy works as expected, create the following Terraform
  `main.tf` file in the current directory. You can use nano, vim, or the
  Cloud Shell Editor to create `policy-library/main.tf`.
  ```
  terraform {
    required_providers {
      google = {
        source = "hashicorp/google"
        version = "~> 3.84"
      }
    }
  }
  resource "google_project_iam_binding" "sample_iam_binding" {
    project = "PROJECT_ID"
    role    = "roles/viewer"
    members = [
      "user:EMAIL_ADDRESS"
    ]
  }
  ```
  Replace the following:
  - `PROJECT_ID`: your project ID.
  - `EMAIL_ADDRESS`: a sample email address. This can be
    any valid email address. For example, `user@example.com`.
5. Initialize Terraform and generate a Terraform plan using the following:
  ```
  terraform init
  ```
6. Export the Terraform plan, if asked, click **Authorize** when prompted:
  ```
  terraform plan -out=test.tfplan
  ```
7. Convert the Terraform plan to JSON:
  ```
  terraform show -json ./test.tfplan > ./tfplan.json
  ```
8. Install the terraform-tools component:
  ```
  sudo apt-get install google-cloud-sdk-terraform-tools
  ```
9. Enter the following command to validate that your Terraform plan complies with your policies:
  ```
  gcloud beta terraform vet tfplan.json --policy-library=. --format=json
  ```
  Since the email address you provided in the IAM policy binding does not belong to a service account, the plan violates the constraint you set up.
  ```
  [
  {
    "constraint": "GCPIAMAllowedPolicyMemberDomainsConstraintV2.service_accounts_only",
    "constraint_config": {
      "api_version": "constraints.gatekeeper.sh/v1alpha1",
      "kind": "GCPIAMAllowedPolicyMemberDomainsConstraintV2",
      "metadata": {
        "annotations": {
          "description": "Checks that members that have been granted IAM roles belong to allowlisted domains.",
          "validation.gcp.forsetisecurity.org/originalName": "service_accounts_only",
          "validation.gcp.forsetisecurity.org/yamlpath": "policies/constraints/iam_service_accounts_only.yaml"
        },
        "name": "service-accounts-only"
      },
      "spec": {
        "match": {
          "target": [
            "organizations/**"
          ]
        },
        "parameters": {
          "domains": [
            "gserviceaccount.com"
          ]
        },
        "severity": "high"
      }
    },
    "message": "IAM policy for //cloudresourcemanager.googleapis.com/projects/PROJECT_ID contains member from unexpected domain: user:user@example.com",
    "metadata": {
      "ancestry_path": "organizations/ORG_ID/projects/PROJECT_ID",
      "constraint": {
        "annotations": {
          "description": "Checks that members that have been granted IAM roles belong to allowlisted domains.",
          "validation.gcp.forsetisecurity.org/originalName": "service_accounts_only",
          "validation.gcp.forsetisecurity.org/yamlpath": "policies/constraints/iam_service_accounts_only.yaml"
        },
        "labels": {},
        "parameters": {
          "domains": [
            "gserviceaccount.com"
          ]
        }
      },
      "details": {
        "member": "user:user@example.com",
        "resource": "//cloudresourcemanager.googleapis.com/projects/PROJECT_ID"
      }
    },
    "resource": "//cloudresourcemanager.googleapis.com/projects/PROJECT_ID",
    "severity": "high"
  }
  ]
  ```
10. To allow another domain (your email), edit `policy-library/policies/constraints/iam_service_accounts_only.yaml` and append your email domain to the domains allowlist. In the following example, we've added `example.com`, but you'd enter the domain for your own email address:
  ```
  apiVersion: constraints.gatekeeper.sh/v1alpha1
  kind: GCPIAMAllowedPolicyMemberDomainsConstraintV1
  metadata:
    name: service_accounts_only
  spec:
    severity: high
    match:
      target: ["organizations/**"]
    parameters:
      domains:
        - gserviceaccount.com
        - example.com
  ```
11. Now validate your Terraform plan again, and this should result in no violations found:
  ```
  gcloud beta terraform vet tfplan.json --policy-library=. --format=json
  ```
  Expected output:
  ```
  []
  ```

## Troubleshooting

If you receive the following error, `"Error 403: The caller does not have permission, forbidden"`, then you either didn't replace `PROJECT_ID` in `policy-library/main.tf` with the name of your project, or you don't have the necessary permissions on the project you specified.

After editing the project name and/or permissions (`resourcemanager.projects.getIamPolicy` and `resourcemanager.projects.get`), go back and export the Terraform plan again, and then convert the Terraform plan to JSON.

---

# Troubleshoot gcloud beta terraform vetStay organized with collectionsSave and categorize content based on your preferences.

# Troubleshoot gcloud beta terraform vetStay organized with collectionsSave and categorize content based on your preferences.

## Why is a violation I expected not throwing an error?

If you test your validation logic and find that the constraint isn't throwing an
error when it should be, this might be a result of one or more of the following:

- **Is your policy-library set up correctly?** Verify that your policy library
  contains a `policies/constraints` directory, which contains the constraint
  you are expecting to cause a violation.
- **Is the Terraform resource that contains the violation a supported
  resource?** `gcloud beta terraform vet` can only check for violations for resources
  that are supported in its version. Re-run your command with
  `--verbosity=debug` and look for a message like: `unsupported resource:
  google_resource_name`. Or you can check whether your resource is in the list
  of
  [supported resources](https://cloud.google.com/docs/cloud-asset-inventory/overview#supported_resource_types).
- **Is your constraint targeting the correct Terraform resource?**
  1. Check the `kind` field of the constraint. It should be something like:
    `GCPAppengineLocationConstraintV1`
  2. Search the `policies/templates` directory for a policy that has the same
    value for `spec.crd.spec.names.kind`
  3. In the `rego` field, look for something like: `asset.asset_type ==
    "appengine.googleapis.com/Application"`. This is the
    [CAI Asset Type](https://cloud.google.com/asset-inventory/docs/supported-asset-types) that the
    constraint targets.
  4. Make sure that the CAI Asset Type is in the list of
    [supported resources](https://cloud.google.com/docs/cloud-asset-inventory/overview#supported_resource_types).

## Why am I getting an error saying that no project is defined?

Resource Ancestry is used to build an accurate CAI Asset Name. If
`gcloud beta terraform vet` can't automatically determine the ancestry for a CAI Asset,
it will return an error saying: `project: required field is not set`. You can
provide a default project with the `--project` flag or by setting one using
[gcloud config](https://cloud.google.com/sdk/gcloud/reference/config).

## Why am I getting an error sayinggetting resource ancestry for project PROJECT_ID: googleapi: Error 403: The caller does not have permission,forbidden?

Run the command with `--verbosity=debug` and look for a message like `Terraform
is using this identity:`. It should be followed by an email address, which is
the account being used for API requests.

- If there is no email address, then
  [make sure that your authentication is working properly](https://cloud.google.com/sdk/gcloud/reference/auth).
- If there is an email address, but it's not the service account that you
  wanted to impersonate, then
  [make sure that your service account impersonation is set up correctly](https://cloud.google.com/sdk/gcloud/reference#--impersonate-service-account)
- If the correct email address is showing, make sure that it has the following
  permissions on the project:
  - `getIamPolicy`
  - `resourcemanager.projects.get`

   Was this helpful?

---

# Validate policiesStay organized with collectionsSave and categorize content based on your preferences.

# Validate policiesStay organized with collectionsSave and categorize content based on your preferences.

## Before you begin

### InstallGoogle Cloud CLI

To use `gcloud beta terraform vet` you must first install Google Cloud CLI:

1. Install Google Cloud CLI but skip the `gcloud init` command.
2. Run the following commands to install the terraform-tools component:
  ```
  gcloud components update
  gcloud components install terraform-tools
  ```
3. Verify that the gcloud CLI is installed by running the following command:
  ```
  gcloud beta terraform vet --help
  ```

### Get required permissions

The Google Cloud account that you use for validation must have the following permissions:

- `getIamPolicy`: `gcloud beta terraform vet` needs to get full Identity and Access Management (IAM)
  policies and merge them with members and bindings to get an accurate end state to validate.
- `resourcemanager.projects.get`: `gcloud beta terraform vet` needs to get project ancestry from the API in order to accurately construct a full CAI Asset Name for any projects that validated resources are related to.
- `resourcemanager.folders.get`: `gcloud beta terraform vet` needs to get folder ancestry
  from the API in order to accurately construct a full CAI Asset Name if the validated
  resources contain any folder-related resources.

### Set up a policy library

You need to [create a policy library](https://cloud.google.com/docs/terraform/policy_validation/create_policy_library) to use this tool.

## Validate policies

### 1. Generate a Terraform plan

`gcloud beta terraform vet` is compatible with Terraform 0.12+. `gcloud beta terraform vet` takes `terraform plan` JSON as its input. You can generate the JSON file by running the following commands in your Terraform directory:

```
terraform plan -out=tfplan.tfplan
terraform show -json ./tfplan.tfplan > ./tfplan.json
```

### 2. Rungcloud beta terraform vet

`gcloud beta terraform vet` lets you validate your `terraform plan` JSON against your organization's POLICY_LIBRARY_REPO. For example:

```
git clone POLICY_LIBRARY_REPO POLICY_LIBRARY_DIR
gcloud beta terraform vet tfplan.json --policy-library=POLICY_LIBRARY_DIR
```

When you execute this command, `gcloud beta terraform vet` retrieves project data by using Google Cloud APIs that are necessary for an accurate validation of your plan.

#### Flags

- `--policy-library=POLICY_LIBRARY_DIR` - Directory that contains a policy library.
- `--project=PROJECT_ID` - `gcloud beta terraform vet` accepts an optional `--project` flag. This flag specifies the [default project](https://cloud.google.com/sdk/gcloud/reference/config/set) when building the ancestry (from the Google Cloud resource hierarchy) for any resource that doesn't have an explicit project set.
- `--format=FORMAT` - The default is yaml. The supported formats are: `default`, `json`, `none`, `text`, `yaml`. For more details run $ [gcloud topic formats](https://cloud.google.com/sdk/gcloud/reference/topic/formats).

#### Exit code and output

- If all constraints are validated, the command returns exit code 0 and does not display violations.
- If violations are found, `gcloud beta terraform vet` returns exit code 2, and displays a list of violations. For example, JSON output might look like:

```
[
  {
    "constraint": "GCPIAMAllowedPolicyMemberDomainsConstraintV2.service_accounts_only",
    "constraint_config": {
      "api_version": "constraints.gatekeeper.sh/v1alpha1",
      "kind": "GCPIAMAllowedPolicyMemberDomainsConstraintV2",
      "metadata": {
        "annotations": {
          "description": "Checks that members that have been granted IAM roles belong to allowlisted domains.",
          "validation.gcp.forsetisecurity.org/originalName": "service_accounts_only",
          "validation.gcp.forsetisecurity.org/yamlpath": "policies/constraints/iam_service_accounts_only.yaml"
        },
        "name": "service-accounts-only"
      },
      "spec": {
        "match": {
          "target": [
            "organizations/**"
          ]
        },
        "parameters": {
          "domains": [
            "gserviceaccount.com"
          ]
        },
        "severity": "high"
      }
    },
    "message": "IAM policy for //cloudresourcemanager.googleapis.com/projects/PROJECT_ID contains member from unexpected domain: user:me@example.com",
    "metadata": {
      "ancestry_path": "organizations/ORG_ID/projects/PROJECT_ID",
      "constraint": {
        "annotations": {
          "description": "Checks that members that have been granted IAM roles belong to allowlisted domains.",
          "validation.gcp.forsetisecurity.org/originalName": "service_accounts_only",
          "validation.gcp.forsetisecurity.org/yamlpath": "policies/constraints/iam_service_accounts_only.yaml"
        },
        "labels": {},
        "parameters": {
          "domains": [
            "gserviceaccount.com"
          ]
        }
      },
      "details": {
        "member": "user:me@example.com",
        "resource": "//cloudresourcemanager.googleapis.com/projects/PROJECT_ID"
      }
    },
    "resource": "//cloudresourcemanager.googleapis.com/projects/PROJECT_ID",
    "severity": "high"
  }
]
```

## CI/CD example

A bash script for using `gcloud beta terraform vet` in a CI/CD pipeline might look like
this:

```
terraform plan -out=tfplan.tfplan
terraform show -json ./tfplan.tfplan > ./tfplan.json
git clone POLICY_LIBRARY_REPO POLICY_LIBRARY_DIR
VIOLATIONS=$(gcloud beta terraform vet tfplan.json --policy-library=POLICY_LIBRARY_DIR --format=json)
retVal=$?
if [ $retVal -eq 2 ]; then
  # Optional: parse the VIOLATIONS variable as json and check the severity level
  echo "$VIOLATIONS"
  echo "Violations found; not proceeding with terraform apply"
  exit 1
fi
if [ $retVal -ne 0]; then
  echo "Error during gcloud beta terraform vet; not proceeding with terraform apply"
  exit 1
fi

echo "No policy violations detected; proceeding with terraform apply"

terraform apply
```

Developers can also use `gcloud beta terraform vet` locally to test Terraform changes
prior to running your CI/CD pipeline.

   Was this helpful?

---

# Policy validationStay organized with collectionsSave and categorize content based on your preferences.

# Policy validationStay organized with collectionsSave and categorize content based on your preferences.

Businesses are shifting towards infrastructure-as-code, and with that change
comes a concern that configuration errors can cause security and governance
violations. To address this, security and cloud administrators need to be able
to set up guardrails that make sure everyone in their organization follows
security best practices. These guardrails are in the form of *constraints*.

Constraints define your organization's source of truth for security and
governance requirements. The constraints must be compatible with tools across
every stage of the application lifecycle, from development, to deployment, and
even to an audit of deployed resources.

[gcloud beta terraform vet](https://cloud.google.com/sdk/gcloud/reference/beta/terraform/vet) is a tool for
enforcing policy compliance as part of an infrastructure CI/CD pipeline. When
you run this tool, `gcloud beta terraform vet` retrieves project data with Google Cloud
APIs that are necessary for accurate validation of your plan. You can use
`gcloud beta terraform vet` to detect policy violations and provide warnings or halt
deployments before they reach production. The same set of constraints that you
use with `gcloud beta terraform vet` can also be used with any other tool that
supports the same framework.

With `gcloud beta terraform vet` you can:

- Enforce your organization's policy at any stage of application development
- Remove manual errors by automating policy validation
- Reduce learning time by using a single paradigm for all policy management

## Support

Until `gcloud beta terraform vet` is generally available (GA), regular support channels
might not be available. For support with `gcloud beta terraform vet`,
[open a ticket](https://github.com/GoogleCloudPlatform/terraform-google-conversion/issues/new/choose)
on the `terraform-google-conversion` GitHub repository.

## Documentation

`gcloud beta terraform vet`  includes the following resources:

- [Quickstart](https://cloud.google.com/docs/terraform/policy-validation/quickstart) – How to implement a constraint that throws an error, and then modify the constraint so the validation check passes.
- [Create a policy library](https://cloud.google.com/docs/terraform/policy-validation/create-policy-library) – How to create a centralized policy repository.
- [Create Terraform constraints](https://cloud.google.com/docs/terraform/policy-validation/create-terraform-constraints) – How to add Terraform-based constraints.
- [Create CAI constraints](https://cloud.google.com/docs/terraform/policy-validation/create-cai-constraints) – How to add CAI-based constraints.
- [Validate policies](https://cloud.google.com/docs/terraform/policy-validation/validate-policies) – How to validate policy compliance with `gcloud beta terraform vet`.
- [Troubleshooting](https://cloud.google.com/docs/terraform/policy-validation/troubleshooting) – Potential problems and solutions to fix them.
- [Migrate from terraform-validator](https://cloud.google.com/docs/terraform/policy-validation/migrate-from-terraform-validator) - How to migrate to `gcloud beta terraform vet` from [terraform-validator](https://github.com/GoogleCloudPlatform/terraform-validator).

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

---

# Troubleshoot gcloud beta terraform vetStay organized with collectionsSave and categorize content based on your preferences.

# Troubleshoot gcloud beta terraform vetStay organized with collectionsSave and categorize content based on your preferences.

## Why is a violation I expected not throwing an error?

If you test your validation logic and find that the constraint isn't throwing an
error when it should be, this might be a result of one or more of the following:

- **Is your policy-library set up correctly?** Verify that your policy library
  contains a `policies/constraints` directory, which contains the constraint
  you are expecting to cause a violation.
- **Is the Terraform resource that contains the violation a supported
  resource?** `gcloud beta terraform vet` can only check for violations for resources
  that are supported in its version. Re-run your command with
  `--verbosity=debug` and look for a message like: `unsupported resource:
  google_resource_name`. Or you can check whether your resource is in the list
  of
  [supported resources](https://cloud.google.com/docs/cloud-asset-inventory/overview#supported_resource_types).
- **Is your constraint targeting the correct Terraform resource?**
  1. Check the `kind` field of the constraint. It should be something like:
    `GCPAppengineLocationConstraintV1`
  2. Search the `policies/templates` directory for a policy that has the same
    value for `spec.crd.spec.names.kind`
  3. In the `rego` field, look for something like: `asset.asset_type ==
    "appengine.googleapis.com/Application"`. This is the
    [CAI Asset Type](https://cloud.google.com/asset-inventory/docs/supported-asset-types) that the
    constraint targets.
  4. Make sure that the CAI Asset Type is in the list of
    [supported resources](https://cloud.google.com/docs/cloud-asset-inventory/overview#supported_resource_types).

## Why am I getting an error saying that no project is defined?

Resource Ancestry is used to build an accurate CAI Asset Name. If
`gcloud beta terraform vet` can't automatically determine the ancestry for a CAI Asset,
it will return an error saying: `project: required field is not set`. You can
provide a default project with the `--project` flag or by setting one using
[gcloud config](https://cloud.google.com/sdk/gcloud/reference/config).

## Why am I getting an error sayinggetting resource ancestry for project PROJECT_ID: googleapi: Error 403: The caller does not have permission,forbidden?

Run the command with `--verbosity=debug` and look for a message like `Terraform
is using this identity:`. It should be followed by an email address, which is
the account being used for API requests.

- If there is no email address, then
  [make sure that your authentication is working properly](https://cloud.google.com/sdk/gcloud/reference/auth).
- If there is an email address, but it's not the service account that you
  wanted to impersonate, then
  [make sure that your service account impersonation is set up correctly](https://cloud.google.com/sdk/gcloud/reference#--impersonate-service-account)
- If the correct email address is showing, make sure that it has the following
  permissions on the project:
  - `getIamPolicy`
  - `resourcemanager.projects.get`

   Was this helpful?

---

# Terraform on Google Cloud release notesStay organized with collectionsSave and categorize content based on your preferences.

# Terraform on Google Cloud release notesStay organized with collectionsSave and categorize content based on your preferences.

This page contains the release notes for Terraform on Google Cloud documentation updates.

For Google Provider updates, see the [terraform-provider-google/CHANGELOG.md](https://github.com/hashicorp/terraform-provider-google/blob/main/CHANGELOG.md).

For `gcloud terraform` releases, see the [Google Cloud SDK release notes](https://cloud.google.com/sdk/docs/release-notes#terraform).

You can see the latest product updates for all of Google Cloud on the
        [Google Cloud](https://cloud.google.com/release-notes) page, browse and filter all release notes in the
        [Google Cloud console](https://console.cloud.google.com/release-notes),
        or programmatically access release notes in
        [BigQuery](https://console.cloud.google.com/bigquery?p=bigquery-public-data&d=google_cloud_release_notes&t=release_notes&page=table).

To get the latest product updates delivered to you, add the URL of this page to your
        [feed
          reader](https://wikipedia.org/wiki/Comparison_of_feed_aggregators), or add the
        [feed URL](https://docs.cloud.google.com/feeds/terraform-release-notes.xml) directly.

## September 16,2024

  Change

Multiple Terraform samples added to [BigQuery](https://cloud.google.com/bigquery/docs/introduction) documentation. For example, see the Terraform tabs on the following pages:

- [Tag tables and datasets](https://cloud.google.com/bigquery/docs/tags)
- [Creating and managing tags](https://cloud.google.com/resource-manager/docs/tags/tags-creating-and-managing)

## September 18,2023

  Change

Multiple Terraform samples added to [Looker documentation](https://cloud.google.com/looker/docs/looker-core). For example, see the Terraform tabs on the following pages:

- [Enable CMEK for Looker (Google Cloud core)](https://cloud.google.com/looker/docs/looker-core-cmek)
- [Create a Looker (Google Cloud core) instance](https://cloud.google.com/looker/docs/looker-core-instance-create)
- [Looker (Google Cloud core) overview](https://cloud.google.com/looker/docs/looker-core-overview)

## February 23,2023

  Change

Published a [new page that lists all of the Terraform resource samples](https://cloud.google.com/docs/terraform/samples). The new page allows for filtering by keyword and category.

## December 19,2022

  Change

Published an update to the [Terraform blueprints page](https://cloud.google.com/docs/terraform/blueprints/terraform-blueprints). The new page allows for filtering by keyword and category.

## September 02, 2022

  Change

Multiple Terraform samples added to the [Cloud Run documentation](https://cloud.google.com/run/docs). For example, see the Terraform tabs on the following pages:

- [Configure Cloud Run Service to send requests using a static IP address](https://cloud.google.com/run/docs/configuring/static-outbound-ip#command-line#terraform)
- [Write, deploy, and call a Cloud Run service from a Pub/Sub push subscription](https://cloud.google.com/run/docs/tutorials/pubsub)
- [Authentication between Services](https://cloud.google.com/run/docs/authenticating/service-to-service#terraform)
- [Manage traffic to your Cloud Run Services with gradual rollouts (canary test) and rollbacks](https://cloud.google.com/run/docs/rollouts-rollbacks-traffic-migration#terraform)
- [Configure Cloud Run Service timeouts](https://cloud.google.com/run/docs/configuring/request-timeout#terraform)

## August 01, 2022

  Change

Multiple Terraform samples added to the [Cloud SQL documentation](https://cloud.google.com/sql/docs).  For example, see the Terraform tabs on the following pages:

- [Create instance](https://cloud.google.com/sql/docs/mysql/create-instance)
- [Create database](https://cloud.google.com/sql/docs/mysql/create-manage-databases)
- [Configure private services access](https://cloud.google.com/sql/docs/mysql/configure-private-services-access)
- [Configure SSL/TLS certificates](https://cloud.google.com/sql/docs/mysql/configure-ssl-instance)

## May 04, 2022

  Change

Documented [Best practices for using Terraform](https://cloud.google.com/docs/terraform/best-practices-for-terraform) across multiple team members and work streams.

## March 17, 2022

  Feature

Added support for [Policy validation](https://cloud.google.com/docs/terraform/policy-validation) to enforce policies as part of a CI/CD pipeline. This feature is available in **Preview**.

## March 01, 2022

  Feature

Google Cloud resource export and import:

- [Export your Google Cloud resources into Terraform format](https://cloud.google.com/docs/terraform/resource-management/export)
- [Import your Google Cloud resources into Terraform state](https://cloud.google.com/docs/terraform/resource-management/import)

These features are available in **Preview**.

## December 07, 2021

  Change

Added page: [Terraform blueprints available for Google Cloud](https://cloud.google.com/docs/terraform/blueprints/terraform-blueprints).

---

# Export your Google Cloud resources to Terraform formatStay organized with collectionsSave and categorize content based on your preferences.

# Export your Google Cloud resources to Terraform formatStay organized with collectionsSave and categorize content based on your preferences.

You've deployed resources in Google Cloud, and now need to manage your
infrastructure as code (IaC) with Terraform. Google provides a tool that you
can use to generate Terraform code for resources in a project, folder, or
organization.

## Roles

To get the permissions that
      you need to export assets to Terraform,

      ask your administrator to grant you the
    following IAM roles on the organization, folder, or project:

- [Service Usage Consumer](https://cloud.google.com/iam/docs/roles-permissions/serviceusage#serviceusage.serviceUsageConsumer) (`roles/serviceusage.serviceUsageConsumer`)
- If writing state to an existing bucket (`--storage-path=BUCKET`):
  - [Storage Object Creator](https://cloud.google.com/iam/docs/roles-permissions/storage#storage.objectCreator) (`roles/storage.objectCreator`)
  - [Storage Object Viewer](https://cloud.google.com/iam/docs/roles-permissions/storage#storage.objectViewer) (`roles/storage.objectViewer`)
- If writing state to a new bucket:
        [Storage Object Viewer](https://cloud.google.com/iam/docs/roles-permissions/storage#storage.objectViewer) (`roles/storage.objectViewer`)

For more information about granting roles, see [Manage access to projects, folders, and organizations](https://cloud.google.com/iam/docs/granting-changing-revoking-access).

You might also be able to get
        the required permissions through [custom
        roles](https://cloud.google.com/iam/docs/creating-custom-roles) or other [predefined
        roles](https://cloud.google.com/iam/docs/roles-overview#predefined).

## Before you begin

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
- Create a service account to use for this export:
  ```
  gcloud beta services identity create --service=cloudasset.googleapis.com
  ```
- Ensure that the [Cloud Asset Service
  Agent](https://cloud.google.com/iam/docs/service-agents)
  (`gcp-sa-cloudasset.iam.gserviceaccount.com`) has the
  `roles/servicenetworking.serviceAgent` role:
  ```
  gcloud projects add-iam-policy-binding PROJECT_ID \
    --member=serviceAccount:service-PROJECT_NUMBER@gcp-sa-cloudasset.iam.gserviceaccount.com \
    --role=roles/servicenetworking.serviceAgent
  ```
- Ensure that the [Cloud Asset Service
  Agent](https://cloud.google.com/iam/docs/service-agents)
  (`gcp-sa-cloudasset.iam.gserviceaccount.com`) has the
  `roles/storage.objectAdmin` role:
  ```
  gcloud projects add-iam-policy-binding PROJECT_ID \
    --member=serviceAccount:service-PROJECT_NUMBER@gcp-sa-cloudasset.iam.gserviceaccount.com \
    --role=roles/storage.objectAdmin
  ```

## Limitations

Some resource types aren't supported for export to Terraform format
 even though they are supported by the Terraform Google provider. For a
list of resource types that are supported for export to Terraform format, run
the [gcloud beta resource-config list-resource-types](https://cloud.google.com/sdk/gcloud/reference/beta/resource-config/list-resource-types) command.

## Export the entire project configuration to Terraform HCL code

The [gcloud beta resource-config bulk-export --resource-format=terraform](https://cloud.google.com/sdk/gcloud/reference/beta/resource-config/bulk-export) command exports
resources configured in the project, folder, or
organization and prints them to the screen in [HCL code format](https://www.terraform.io/language/configuration-0-11/syntax).

```
gcloud beta resource-config bulk-export \
  --project=PROJECT_ID \
  --resource-format=terraform
```

### Write the output to a directory structure

1. If you haven't done so already, create the directory where you want to
  output the project's configuration:
  ```
  mkdir OUTPUT_DIRECTORY
  ```
2. Export the project's entire configuration to the directory:
  ```
  gcloud beta resource-config bulk-export \
   --path=OUTPUT_DIRECTORY \
   --project=PROJECT_ID \
   --resource-format=terraform
  ```
  The `--path` flag specifies the location to output the HCL code.

After running the command, the HCL code for each resource is output to a
separate `.tf` file in the following directory structure:

```
OUTPUT_DIRECTORY/projects/PROJECT_ID/RESOURCE_TYPE
```

### Write the output to a single file

If you don't want to print the output to the screen or create separate `.tf`
files, you can write all of the output to a single file, as shown in this
example:

```
gcloud beta resource-config bulk-export \
  --resource-format=terraform \
  --project=PROJECT_ID \
  >> gcp_resources.tf
```

## Filter the output

Filter the output of the bulk export command by specifying resource types.

### List the supported resource types to filter on

For a list of resource types that are supported for export to Terraform format,
run the [gcloud beta resource-config list-resource-types](https://cloud.google.com/sdk/gcloud/reference/beta/resource-config/list-resource-types) command:

```
gcloud beta resource-config list-resource-types
```

Optionally, write the output to a file:

```
gcloud beta resource-config list-resource-types >> strings.txt
```

In the output, the resource type for Compute Engine VMs is listed as:

```
KRM KIND: ComputeInstance
```

You can ignore the `KRM KIND:` prefix.

### Export a single resource type

Use a string, such as `ComputeInstance`, to export specific resource types for
your project in HCL code format:

```
gcloud beta resource-config bulk-export \
  --resource-types=RESOURCE_TYPE \
  --project=PROJECT_ID \
  --resource-format=terraform
```

The `--resource-types` flag specifies the resource type to output.

### Export multiple resource types

Export VM instances and firewall rules in HCL code format:

```
gcloud beta resource-config bulk-export \
  --resource-types=ComputeFirewall,ComputeInstance \
  --project=PROJECT_ID \
  --resource-format=terraform
```

### Use a file to specify the resource types to export

1. Create a directory called `tf-output`.
  ```
  cd && mkdir tf-output && cd tf-output
  ```
2. Create a file called `types.txt`, and add a list of resource types. For
  example:
  ```
  ComputeBackendBucket
  ComputeBackendService
  ComputeForwardingRule
  ```
3. Run the `gcloud beta resource-config bulk-export` command with the
  `--resource-types-file` flag:
  ```
  gcloud beta resource-config bulk-export \
   --resource-types-file=types.txt \
   --path=tf-output \
   --project=PROJECT_ID \
   --resource-format=terraform
  ```

If the project doesn't contain any of a particular resource type, the command
succeeds but nothing is output for that resource type.

## Troubleshooting

If you see the following error:

"Permission denied during export. Please ensure the Cloud Asset Inventory API is
enabled."

Make sure that you have followed the instructions in the
[Before you begin](#before-you-begin) section.

## Next steps

- [Import your Google Cloud resources into Terraform
  state](https://cloud.google.com/docs/terraform/resource-management/import).
