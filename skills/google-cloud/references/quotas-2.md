# Use custom organization policiesStay organized with collectionsSave and categorize content based on your preferences. and more

# Use custom organization policiesStay organized with collectionsSave and categorize content based on your preferences.

# Use custom organization policiesStay organized with collectionsSave and categorize content based on your preferences.

This page shows you how to use Organization Policy Service custom constraints to restrict
specific operations on the following Google Cloud resources:

- `cloudquotas.googleapis.com/QuotaPreference`

To learn more about Organization Policy, see
[Custom organization policies](https://cloud.google.com/resource-manager/docs/organization-policy/overview#custom-organization-policies).

## About organization policies and constraints

The Google Cloud Organization Policy Service gives you centralized, programmatic
control over your organization's resources. As the
[organization policy administrator](https://cloud.google.com/iam/docs/understanding-roles#orgpolicy.policyAdmin), you can define an organization
policy, which is a set of restrictions called *constraints* that apply to
Google Cloud resources and descendants of those resources in the
[Google Cloud resource hierarchy](https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy). You can enforce organization
policies at the organization, folder, or project level.

Organization Policy provides built-in [managed constraints](https://cloud.google.com/resource-manager/docs/organization-policy/org-policy-constraints)
for various Google Cloud services. However, if you want more granular,
customizable control over the specific fields that are restricted in your
organization policies, you can also create *custom constraints* and use those
custom constraints in an organization policy.

### Policy inheritance

By default, organization policies are inherited by the descendants of the
resources on which you enforce the policy. For example, if you enforce a policy
on a folder, Google Cloud enforces the policy on all projects in the
folder. To learn more about this behavior and how to change it, refer to
[Hierarchy evaluation rules](https://cloud.google.com/resource-manager/docs/organization-policy/understanding-hierarchy#disallow_inheritance).

## Limitations

Custom organization policy enforcement restricts operations that create or
update `QuotaPreference` resources. The following limitations apply because some
quota change scenarios don't create or update `QuotaPreference` resources:

- **When using the Service Usage API**: Quota value changes initiated
  through the [Service Usage API](https://cloud.google.com/service-usage/docs/overview) aren't
  subject to custom organization policy enforcement because they don't change
  `QuotaPreference` resources. To restrict quota value changes initiated
  through the Service Usage API, implement an
  [IAM deny policy](https://cloud.google.com/iam/docs/deny-overview) on the
  `serviceusage.quota.update` permission.
- **When initiating quota changes in the Google Cloud console**: Quota value
  changes initiated using the Google Cloud console aren't subject to custom
  organization policy enforcement because the Google Cloud console does not
  create `QuotaPreference` resources.

## Before you begin

1. Ensure that you know your
  [organization ID](https://cloud.google.com/resource-manager/docs/creating-managing-organization#retrieving_your_organization_id).

### Required roles

To get the permissions that
      you need to manage custom organization policies,

      ask your administrator to grant you the

      [Organization Policy Administrator](https://cloud.google.com/iam/docs/roles-permissions/orgpolicy#orgpolicy.policyAdmin) (`roles/orgpolicy.policyAdmin`)
     IAM role on the organization resource.

  For more information about granting roles, see [Manage access to projects, folders, and organizations](https://cloud.google.com/iam/docs/granting-changing-revoking-access).

You might also be able to get
        the required permissions through [custom
        roles](https://cloud.google.com/iam/docs/creating-custom-roles) or other [predefined
        roles](https://cloud.google.com/iam/docs/roles-overview#predefined).

## Set up a custom constraint

A custom constraint is defined in a YAML file by the resources, methods,
conditions, and actions that are supported by the service on which you are
enforcing the organization policy. Conditions for your custom constraints are
defined using
[Common Expression Language (CEL)](https://github.com/google/cel-spec/blob/master/doc/intro.md). For more information about how to build
conditions in custom constraints using CEL, see the CEL section of
[Creating and managing custom constraints](https://cloud.google.com/resource-manager/docs/organization-policy/creating-managing-custom-constraints#common_expression_language).

To create a custom constraint, do the following:

1. In the Google Cloud console, go to the **Organization policies** page.
  [Go to Organization policies](https://console.cloud.google.com/iam-admin/orgpolicies)
2. From the project picker, select the project that you want to set the organization
          policy for.
3. Click  **Custom constraint**.
4. In the **Display name** box, enter a human-readable name for the constraint. This name is
          used in error messages and can be used for identification and debugging. Don't use PII or
          sensitive data in display names because this name could be exposed in error messages. This
          field can contain up to 200 characters.
5. In the **Constraint ID** box, enter the name that you want for your new custom
          constraint. A custom constraint can only contain letters (including upper and lowercase) or
          numbers, for example `custom.disableGkeAutoUpgrade`. This field can contain up to
          70 characters, not counting the prefix (`custom.`), for example,
          `organizations/123456789/customConstraints/custom`. Don't include PII or
          sensitive data in your constraint ID, because it could be exposed in error messages.
6. In the **Description** box, enter a human-readable description of the constraint. This
          description is used as an error message when the policy is violated. Include details about
          why the policy violation occurred and how to resolve the policy violation. Don't include
          PII or sensitive data in your description, because it could be exposed in error messages.
          This field can contain up to 2000 characters.
7. In the **Resource type** box, select the name of the Google Cloud REST resource
          containing the object and field that you want to restrict—for example,
          `container.googleapis.com/NodePool`. Most resource types support up to 20 custom
          constraints. If you attempt to create more custom constraints, the operation fails.
8. Under **Enforcement method**, select whether to enforce the constraint on a REST
          **CREATE** method or on both **CREATE** and **UPDATE** methods. If you enforce the
          constraint with the **UPDATE** method on a resource that violates the constraint, changes
          to that resource are blocked by the organization policy unless the change resolves the
          violation.
9. To define a condition, click  **Edit condition**.
10. Under **Action**, select whether to allow or deny the evaluated method if the condition
          is met.
11. Click **Create constraint**.

1. To create a custom constraint, create a YAML file using the following format:
2. After you have created the YAML file for a new custom constraint, you must set it up to make
          it available for organization policies in your organization. To set up a custom constraint,
          use the
          [gcloud org-policies set-custom-constraint](https://cloud.google.com/sdk/gcloud/reference/org-policies/set-custom-constraint) command:
3. To verify that the custom constraint exists, use the
          [gcloud org-policies list-custom-constraints](https://cloud.google.com/sdk/gcloud/reference/org-policies/list-custom-constraints) command:

## Enforce a custom organization policy

You can enforce a constraint by creating an organization policy that references it, and then
applying that organization policy to a Google Cloud resource.

1. In the Google Cloud console, go to the **Organization policies** page.
  [Go to Organization policies](https://console.cloud.google.com/iam-admin/orgpolicies)
2. From the project picker, select the project that you want to set the
          organization policy for.
3. From the list on the **Organization policies** page, select your constraint to view
          the **Policy details** page for that constraint.
4. To configure the organization policy for this resource, click **Manage policy**.
5. On the **Edit policy** page, select **Override parent's policy**.
6. Click **Add a rule**.
7. In the **Enforcement** section, select whether this organization policy is enforced or
          not.
8. Optional: To make the organization policy conditional on a tag, click
          **Add condition**. Note that if you add a conditional rule to an organization
          policy, you must add at least one unconditional rule or the policy cannot be saved. For more
          information, see
          [Setting an organization policy with tags](https://cloud.google.com/resource-manager/docs/organization-policy/tags-organization-policy).
9. Click **Test changes** to simulate the effect of the organization policy. For more
          information, see [Test organization policy changes with Policy Simulator](https://cloud.google.com/policy-intelligence/docs/test-organization-policies).
10. To enforce the organization policy in dry-run mode, click **Set dry run policy**. For
          more information, see [Create an organization policy in dry-run mode](https://cloud.google.com/resource-manager/docs/organization-policy/dry-run-policy).
11. After you verify that the organization policy in dry-run mode works as intended, set the
          live policy by clicking **Set policy**.

1. To create an organization policy with boolean rules, create a policy YAML file that
          references the constraint:
2. To enforce the organization policy in
          [dry-run mode](https://cloud.google.com/resource-manager/docs/organization-policy/dry-run-policy), run
          the following command with the `dryRunSpec` flag:
3. After you verify that the organization policy in dry-run mode works as intended, set the
          live policy with the `org-policies set-policy` command and the `spec`
          flag:

## Test the custom organization policy

The following examples create a custom constraint and policy that deny all
`QuotaPreference` settings in a specific project for the
`compute.googleapis.com` service, which has a `CPUS-per-project-region`
quota ID.

Before you begin, you need to know the following:

- Your organization ID
- Your project ID

In the examples that follow, replace `ORGANIZATION_ID` and
`PROJECT_ID` with the strings for your configuration.

### Create an example constraint

The following code snippet shows an example of creating a quota preference
constraint. When creating your own quota preference constraints, update these
fields as needed for your configuration.

1. Save the following file as `quota-constraint.yaml`:
  ```
  name: organizations/ORGANIZATION_ID/customConstraints/custom.restrictCPUsPerProjectRegion
  resourceTypes:
    - cloudquotas.googleapis.com/QuotaPreference
  methodTypes:
    - CREATE
    - UPDATE
  condition: "resource.service == 'compute.googleapis.com' && resource.quotaId == 'CPUS-per-project-region'"
  actionType: DENY
  displayName: Restrict quota update for compute CPUS-per-project-region
  description: Deny quota change for the 'CPUS-per-project-region' quota ID of 'compute.googleapis.com' service.
  ```
  Replace the following:
  - `ORGANIZATION_ID`: your organization ID.
    For help finding your organization ID, see
    [Getting your organization resource ID](https://cloud.google.com/resource-manager/docs/creating-managing-organization#retrieving_your_organization_id).
  This defines a constraint where quota cannot be changed for the
  `CPUS-per-project-region` quota ID of `compute.googleapis.com` service.
2. Apply the constraint:
  ```
  gcloud org-policies set-custom-constraint quota-constraint.yaml
  ```
3. Verify that the constraint exists:
  ```
  gcloud org-policies list-custom-constraints --organization=ORGANIZATION_ID
  ```
4. The output is similar to the following:
  ```
  CUSTOM_CONSTRAINT                    ACTION_TYPE  METHOD_TYPES   RESOURCE_TYPES                              DISPLAY_NAME
  custom.restrictCPUsPerProjectRegion  DENY         CREATE,UPDATE  cloudquotas.googleapis.com/QuotaPreference  Restrict quota update for compute CPUS-per-project-region
  ```

### Create the policy

1. Save the following file as `quota-policy.yaml`:
  ```
  name: projects/PROJECT_ID/policies/custom.restrictCPUsPerProjectRegion
  spec:
    rules:
    - enforce: true
  ```
  Replace `PROJECT_ID` with your project ID.
2. Apply the policy:
  ```
  gcloud org-policies set-policy quota-policy.yaml
  ```
3. Verify that the policy exists:
  ```
  gcloud org-policies list --project=PROJECT_ID
  ```
  The output is similar to the following:
  ```
  CONSTRAINT                           LIST_POLICY  BOOLEAN_POLICY  ETAG
  custom.restrictCPUsPerProjectRegion  -            SET             CNXIq78GEODKiK4D-
  ```

After you apply the policy, wait for about two minutes for Google Cloud to
start enforcing the policy.

### Test the policy

To test the policy, create a quota preference request:

- For example, run the following gcloud CLI command to create
  a quota preference for Compute Engine:
  ```
  gcloud beta quotas preferences create \
      --service=compute.googleapis.com \
      --quota-id=CPUS-per-project-region \
      --preferred-value=30 \
      --project=PROJECT_ID
  ```
- The output is similar to the following:
  ```
  Operation denied by org policy on resource 'projects/PROJECT_ID/locations/global': ["customConstraints/custom.restrictCPUsPerProjectRegion": "Deny quota change for the 'CPUS-per-project-region' quota ID of 'compute.googleapis.com' service."]
  ```

### Delete the example policy and constraint

After you have tested the policy, you can delete it:

1. Delete the policy:
  ```
  gcloud org-policies delete custom.restrictCPUsPerProjectRegion --project=PROJECT_ID
  ```
2. Delete the constraint:
  ```
  gcloud org-policies delete-custom-constraint custom.restrictCPUsPerProjectRegion \
    --organization=ORGANIZATION_ID
  ```

## Example custom organization policies for common use cases

This table provides syntax examples for some common custom constraints.

| Description | Constraint syntax |
| --- | --- |
| Don't allow changes for a specific service's quota ID | name:organizations/ORGANIZATION_ID/customConstraints/custom.restrictCPUsPerProjectRegionQuotaresourceTypes:-cloudquotas.googleapis.com/QuotaPreferencemethodTypes:-CREATE-UPDATEcondition:|-resource.service == 'compute.googleapis.com'&&resource.quotaId == 'CPUS-per-project-region'actionType:DENYdisplayName:Deny quota update for compute CPUS-per-project-regiondescription:Deny quota change for the 'CPUS-per-project-region' quota ID of 'compute.googleapis.com' service. |
| Restrict quota value to be under a specified value | name:organizations/ORGANIZATION_ID/customConstraints/custom.restrictCPUsPerProjectRegionQuotaLimitresourceTypes:-cloudquotas.googleapis.com/QuotaPreferencemethodTypes:-CREATE-UPDATEcondition:|-resource.service == 'compute.googleapis.com'&&resource.quotaId == 'CPUS-per-project-region'&&resource.quotaConfig.preferredValue <= 25actionType:ALLOWdisplayName:Restrict quota update for compute CPUS-per-project-regiondescription:Restrict quota change for the 'CPUS-per-project-region' quota ID of 'compute.googleapis.com' service. |

## Cloud Quotas supported resources

The following table lists the Cloud Quotas resources that you can
reference in custom constraints:

| Resource | Field |
| --- | --- |
| cloudquotas.googleapis.com/QuotaPreference | resource.dimensions |
| resource.name |  |
| resource.quotaConfig.preferredValue |  |
| resource.quotaId |  |
| resource.service |  |

## What's next

- Learn more about
    [Organization Policy Service](https://cloud.google.com/resource-manager/docs/organization-policy/overview).
- Learn more about how to
    [create and manage organization policies](https://cloud.google.com/resource-manager/docs/organization-policy/using-constraints).
- See the full list of managed
    [organization policy constraints](https://cloud.google.com/resource-manager/docs/organization-policy/org-policy-constraints).

   Was this helpful?

---

# Set up the Cloud Quotas APIStay organized with collectionsSave and categorize content based on your preferences.

# Set up the Cloud Quotas APIStay organized with collectionsSave and categorize content based on your preferences.

To use the Cloud Quotas API, you must first enable it for your
Google Cloud project. This document describes how to enable the Cloud Quotas API.

## Enable the API

You can enable the Cloud Quotas API by using the Google Cloud console or the
[Google Cloud CLI](https://cloud.google.com/sdk/gcloud).

1. Go to the Google Cloud console **API Library** page.
  [Go to API Library](https://console.cloud.google.com/project/_/apis/library/cloudquotas.googleapis.com)
2. Select the Google Cloud project that you want to access the API.
3. On the API Library page, enable **Cloud Quotas API**.
4. Make sure that your user account has the required [IAM
  roles](https://cloud.google.com/docs/quotas/permissions).

## Before you begin

Authenticate to the gcloud CLI before you use it to enable
APIs. For more information about the authentication process, see
[Authorize the gcloud CLI](https://cloud.google.com/sdk/docs/authorizing).

## Enable the API

1. Run the [gcloud services enable](https://cloud.google.com/sdk/gcloud/reference/services/enable)
  command and specify the Cloud Quotas API:
  ```
  gcloud services enable cloudquotas.googleapis.com --project=PROJECT_ID
  ```
  Replace `PROJECT_ID` with the ID of the project
  that needs access to the Cloud Quotas API. You can find your project ID on the
  [Welcome](https://console.cloud.google.com/welcome) page of the Google Cloud console.
2. To confirm that the Cloud Quotas API is enabled in your project, run the
  [gcloud services list](https://cloud.google.com/sdk/gcloud/reference/services/list) command
  and filter for `cloudquotas.googleapis.com` by passing the output to a
  command such as `grep` or using a gcloud CLI
  [filter](https://cloud.google.com/sdk/gcloud/reference/topic/filters):
  ```
  gcloud services list --filter="cloudquotas.googleapis.com"
  ```

## What's next

- About the [Cloud Quotas API](https://cloud.google.com/docs/quotas/api-overview)
- Cloud Quotas API [reference](https://cloud.google.com/docs/quotas/reference/rest)

   Was this helpful?

---

# Manage quotas using the gcloud beta CLIStay organized with collectionsSave and categorize content based on your preferences.

> Examples for using gcloud CLI to manage quotas

# Manage quotas using the gcloud beta CLIStay organized with collectionsSave and categorize content based on your preferences.

The following sections contain example
[gcloud beta quotas info](https://cloud.google.com/sdk/gcloud/reference/beta/quotas/info)
and
[gcloud beta quotas preferences](https://cloud.google.com/sdk/gcloud/reference/beta/quotas/preferences)
commands. These commands allow you to view and manage `QuotaInfo` and
`QuotaPreference` resources.

You can use the Google Cloud CLI (gcloud CLI) to get current
quotas values and specify quota preferences for some Google Cloud APIs and
services.

## Limitations

Cloud Quotas has the following limitations:

- In most cases, quota *increase* adjustments must be made at the
  [project-level](https://cloud.google.com/resource-manager/docs/creating-managing-projects).
  A limited number of products support
  [organization-level](https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy#organizations)
  quota increase adjustments. To see if a Google Cloud product supports
  organization-level quota increase adjustments, refer to the documentation
  for that product.
- You can request quota *decrease* adjustments for
  project-, organization-, and
  [folder-level](https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy#folders)
  quotas.

## Before you begin

Before you use the gcloud CLI, make sure that you
[install and initialize the gcloud CLI](#install_initialize_gcloud).

You may also need your `QUOTA_ID` value. If so, see the
[instructions for finding your quota ID](#find_your_quota_id).

### Install and initialize the gcloud CLI

To use the gcloud CLI for Cloud Quotas, be sure to install and
initialize components:

1. [Install](https://cloud.google.com/sdk/docs/install) the gcloud CLI.
  If you're using Cloud Shell, you can skip this step because
  gcloud CLI comes pre-installed.
2. [Initialize](https://cloud.google.com/sdk/docs/initializing) the gcloud CLI.
3. [Install the beta component](https://cloud.google.com/sdk/docs/components#alpha_and_beta_components)
  by running the following command:
  ```
  gcloud components install beta
  ```

### Find your quota ID

Several gcloud CLI commands in this document refer to your quota ID
value. You can find the quota ID using the Google Cloud console, the
gcloud CLI, client libraries, or the REST API. This section shows how
to find the quota ID using either the Google Cloud console or gcloud CLI.

1. In the Google Cloud console, go to the
  **IAM & Admin>Quotas & System Limits** page:
  [Go to Quotas & System Limits](https://console.cloud.google.com/iam-admin/quotas)
2. Click **Filter** to filter for your service.
3. If you don't see the **Limit name** column, click the icon
   **Column display options...**. Select
  **Limit name** and click **OK**.
4. The **Limit name** column shows the quota ID.

To find the quota ID value by using the gcloud CLI, run the
following command to list your quota information for the specified service:

1. Enter the following gcloud CLI command in a terminal window:
  ```
  gcloud beta quotas info list --service=SERVICE_NAME --project=PROJECT_ID_OR_NUMBER \
  --billing-project=BILLING_PROJECT_ID_OR_NUMBER
  ```
  Replace the following:
  - `SERVICE_NAME`: the service name with quotas that you want to
    see—for example, the service name for Compute Engine is `compute.googleapis.com`.
  - `PROJECT_ID_OR_NUMBER`: the project ID or project number.
    To find your project ID using the Google Cloud console, navigate to the
    Resource Manager page:
    [Go to Resource Manager](https://console.cloud.google.com/cloud-resource-manager)
  - `BILLING_PROJECT_ID_OR_NUMBER`: the ID or project
    number of the project whose Cloud Quotas API quota you want to
    use for executing this command. This can be different from the
    project containing the service that you're finding the quota ID
    for.
    If you already [set the billing project](https://cloud.google.com/sdk/gcloud/reference#--billing-project)
    when setting up the gcloud CLI, this flag is optional.
    Otherwise, omitting it might cause a
    [permission denied error](https://cloud.google.com/docs/quotas/troubleshoot#gcloud_cli_errors).
    For more information, see
    [Set the quota project](https://cloud.google.com/docs/quotas/set-quota-project#set-project-programmatically).
2. The output from the `gcloud beta quotas info list` command contains text
  similar to the following sample:
  ```
  ...
  "quotaInfos": [
      ...
      {
          "name": "projects/PROJECT_NUMBER/locations/global/services/compute.googleapis.com/quotaInfos/CPUS-per-project-region",
          "quotaId": "CPUS-per-project-region",
          "metric": "compute.googleapis.com/cpus",
          "containerType": "PROJECT",
          "dimensions": [
              "region"
          ],
          "dimensionsInfo": [
              {
                  "details": {
                      "value": 20
                  },
                  "applicableLocations": [
                      "us-central1",
                      "us-central2",
                      "us-west1",
                      "us-east1"
                  ]
                  ...
              }
          ]
      },
      ...
  ]
  ...
  ```
3. Look for the value that corresponds to `quotaId` and use it when specifying
  `QUOTA_ID` in the following sections.

## Example gcloud quota information commands

This section provides examples that show how to use `gcloud beta quotas info`
commands to view quota information for a particular service or for an
organization.

`QuotaInfo` is a read-only resource that provides metadata and quota value
information about a particular quota for a given project, folder or
organization.

### View quota information for a particular service

To view quota information for a particular service, run the following command:

```
gcloud beta quotas info describe QUOTA_ID --service=SERVICE_NAME \
    --project=PROJECT_ID_OR_NUMBER --billing-project=BILLING_PROJECT_ID_OR_NUMBER
```

Replace the following:

- `QUOTA_ID`: the quota ID value.
  To find this value, see [Find your quota ID](#find_your_quota_id).
- `SERVICE_NAME`: the service name with quotas that you want
  to see—for example, the service name for Compute Engine is
  `compute.googleapis.com`.
- `PROJECT_ID_OR_NUMBER`: the project ID or project number.
- `BILLING_PROJECT_ID_OR_NUMBER`: the ID or project number of
  the project whose Cloud Quotas API quota you want to use for executing
  this command. This can be different from the project containing the service
  that you're viewing quota info for.
  If you already [set the billing project](https://cloud.google.com/sdk/gcloud/reference#--billing-project)
  when setting up the gcloud CLI, this flag is optional.
  Otherwise, omitting it might cause a
  [permission denied error](https://cloud.google.com/docs/quotas/troubleshoot#gcloud_cli_errors).
  For more information, see
  [Set the quota project](https://cloud.google.com/docs/quotas/set-quota-project#set-project-programmatically).

### View quota information for an organization

To view the same service's quota details for an organization, run the following command:

```
gcloud beta quotas info list --service=SERVICE_NAME --organization=ORGANIZATION_ID \
    --billing-project=BILLING_PROJECT_ID_OR_NUMBER
```

Replace the following:

- `SERVICE_NAME`: the service name with quotas that you want
  to see—for example, the service name for Compute Engine is
  `compute.googleapis.com`.
- `ORGANIZATION_ID`: the ID of your organization.
- `BILLING_PROJECT_ID_OR_NUMBER`: the ID or project number of
  the project whose Cloud Quotas API quota you want to use for executing
  this command. This can be different from the project containing the service
  that you're viewing quota info for.
  If you already [set the billing project](https://cloud.google.com/sdk/gcloud/reference#--billing-project)
  when setting up the gcloud CLI, this flag is optional.
  Otherwise, omitting it might cause a
  [permission denied error](https://cloud.google.com/docs/quotas/troubleshoot#gcloud_cli_errors).
  For more information, see
  [Set the quota project](https://cloud.google.com/docs/quotas/set-quota-project#set-project-programmatically).

## Example gcloud quota preferences commands

This section provides examples that show how to use `gcloud beta quotas preferences`
commands to check existing quota preferences and adjust the quota value.

The `QuotaPreference` resource represents your preference for a particular
dimension combination. A dimension is an attribute that represents a region
or a zone, or a service-specific dimension, such as `gpu_family`
or `network_id`.

### Check for existing preferences

To check for existing preferences, run the following command:

```
gcloud beta quotas preferences list --project=PROJECT_ID_OR_NUMBER \
    --billing-project=BILLING_PROJECT_ID_OR_NUMBER
```

Replace the following:

- `PROJECT_ID_OR_NUMBER` : the project ID or project number.
- `BILLING_PROJECT_ID_OR_NUMBER`: the ID or project number of
  the project whose Cloud Quotas API quota you want to use for executing
  this command. This can be different from the project containing the service
  that you're checking quota preferences for.
  If you already [set the billing project](https://cloud.google.com/sdk/gcloud/reference#--billing-project)
  when setting up the gcloud CLI, this flag is optional.
  Otherwise, omitting it might cause a
  [permission denied error](https://cloud.google.com/docs/quotas/troubleshoot#gcloud_cli_errors).
  For more information, see
  [Set the quota project](https://cloud.google.com/docs/quotas/set-quota-project#set-project-programmatically).

### Check for existing preferences with pending quota adjustments

To check for existing preferences with pending quota adjustments, add the
`--reconciling-only=true` flag as shown in the following command:

```
gcloud beta quotas preferences list --project=PROJECT_ID_OR_NUMBER --reconciling-only=true \
    --billing-project=BILLING_PROJECT_ID_OR_NUMBER
```

Replace the following:

- `PROJECT_ID_OR_NUMBER` : the project ID or project number.
- `BILLING_PROJECT_ID_OR_NUMBER`: the ID or project number of
  the project whose Cloud Quotas API quota you want to use for executing
  this command. This can be different from the project containing the service
  that you're checking quota preferences for.
  If you already [set the billing project](https://cloud.google.com/sdk/gcloud/reference#--billing-project)
  when setting up the gcloud CLI, this flag is optional.
  Otherwise, omitting it might cause a
  [permission denied error](https://cloud.google.com/docs/quotas/troubleshoot#gcloud_cli_errors).
  For more information, see
  [Set the quota project](https://cloud.google.com/docs/quotas/set-quota-project#set-project-programmatically).

### Request a quota increase adjustment when a quota preference hasn't been set yet

To request a quota adjustment using the gcloud CLI, run the following
command:

```
gcloud beta quotas preferences create --project=PROJECT_ID_OR_NUMBER \
    --service=SERVICE_NAME \
    --quota-id=QUOTA_ID \
    --dimensions=DIMENSIONS \
    --preferred-value=PREFERRED_VALUE \
    --billing-project=BILLING_PROJECT_ID_OR_NUMBER \
    --email=EMAIL \
    --justification=JUSTIFICATION \
    --preference-id=PREFERENCE_ID
```

Replace the following:

- `PROJECT_ID_OR_NUMBER`: the project ID or project number.
- `SERVICE_NAME`: the service name with quotas that you want
      to adjust—for example, the service name for Compute Engine is
      `compute.googleapis.com`.
- `QUOTA_ID`: the quota ID value.
      To find this value, see
      [Find your quota ID](https://cloud.google.com/docs/quotas/gcloud-cli-examples#find_your_quota_id).
- `DIMENSIONS`: the dimensions to adjust, specified as a
      comma-separated list of key-value pairs—for example,
      `region=us-east4,gpu_family=NVIDIA_H100`.
      For more information on quota dimensions, see
      [Configure Cloud Quotas dimensions](https://cloud.google.com/docs/quotas/configure-dimensions).
- `PREFERRED_VALUE`: the preferred quota value.
- `BILLING_PROJECT_ID_OR_NUMBER`: the ID or project number of the
      project whose Cloud Quotas API quota you want to use for executing this command. This can be
      different from the project containing the service that you're requesting a quota adjustment
      for.
  If you already [set the billing project](https://cloud.google.com/sdk/gcloud/reference#--billing-project)
      when setting up the gcloud CLI, this flag is optional.
      Otherwise, omitting it might cause a
      [permission denied error](https://cloud.google.com/docs/quotas/troubleshoot#gcloud_cli_errors).
      For more information, see
      [Set the quota project](https://cloud.google.com/docs/quotas/set-quota-project#set-project-programmatically).
- `EMAIL`: an email address that can be used as a contact, in
      case Google Cloud needs more information before additional quota can be granted.
- `JUSTIFICATION`: an optional string that explains your request.
- `PREFERENCE_ID`: an optional preference ID; if you don't
      specify a preference ID, the API generates a Universally Unique Identifier
      (UUID) for you.

The output looks similar to the following:

```
{
    "createTime":"CREATE_TIME",
    "dimensions":{
        "DIMENSION_KEY_1":"DIMENSION_VALUE_1",
        "DIMENSION_KEY_2":"DIMENSION_VALUE_2"
    },
    "etag":"ETAG_VALUE",
    "name":"projects/PROJECT_ID_OR_NUMBER/locations/global/quotaPreferences/PREFERENCE_ID",
    "quotaConfig":{
        "grantedValue":"GRANTED_VALUE",
        "preferredValue":"PREFERRED_VALUE",
        "traceId":"TRACE_ID"
    },
    "quotaId":"QUOTA_ID",
    "reconciling":true,
    "service":"SERVICE_NAME",
    "updateTime":"UPDATE_TIME",
}
```

### Request a quota increase adjustment when a quota preference has been set

To request a quota increase adjustment for a specific region and there is already a
preference, run the following command:

```
gcloud beta quotas preferences update PREFERENCE_ID --preferred-value=PREFERRED_VALUE \
    --quota-id=QUOTA_ID --service=SERVICE_NAME --project=PROJECT_ID_OR_NUMBER \
    --billing-project=BILLING_PROJECT_ID_OR_NUMBER --email=EMAIL  \
    --justification=JUSTIFICATION
```

Replace the following:

- `PREFERENCE_ID`: the preference ID, which is required as
  the first argument when using the `gcloud beta quotas preferences update`
  command.
- `PREFERRED_VALUE`: the preferred quota value.
- `QUOTA_ID`: the quota ID value.
  To find this value, see [Find your quota ID](#find_your_quota_id).
- `SERVICE_NAME`: the service name with quotas that you want
  to see—for example, the service name for Compute Engine is
  `compute.googleapis.com`.
- `PROJECT_ID_OR_NUMBER`: the project ID or project number.
- `BILLING_PROJECT_ID_OR_NUMBER`: the ID or project number of
  the project whose Cloud Quotas API quota you want to use for executing
  this command. This can be different from the project containing the service
  that you're requesting a quota adjustment for.
  If you already [set the billing project](https://cloud.google.com/sdk/gcloud/reference#--billing-project)
  when setting up the gcloud CLI, this flag is optional.
  Otherwise, omitting it might cause a
  [permission denied error](https://cloud.google.com/docs/quotas/troubleshoot#gcloud_cli_errors).
  For more information, see
  [Set the quota project](https://cloud.google.com/docs/quotas/set-quota-project#set-project-programmatically).
- `EMAIL`: an email address that can be used as a contact, in
  case Google Cloud needs more information before additional quota can be granted.
- `JUSTIFICATION`: an optional string that explains your request.

### View an existing quota preference

To view the details of the quota preference that you just created,
run the following command:

```
gcloud beta quotas preferences describe PREFERENCE_ID \
    --project=PROJECT_ID_OR_NUMBER \
    --billing-project=BILLING_PROJECT_ID_OR_NUMBER
```

Replace the following:

- `PREFERENCE_ID`: the preference ID, which is required as
  the first argument when using the `gcloud beta quotas preferences describe`
  command.
- `PROJECT_ID_OR_NUMBER`: the project ID or project number.
- `BILLING_PROJECT_ID_OR_NUMBER`: the ID or project number of
  the project whose Cloud Quotas API quota you want to use for executing
  this command. This can be different from the project containing the service
  that you're viewing the quota preference for.
  If you already [set the billing project](https://cloud.google.com/sdk/gcloud/reference#--billing-project)
  when setting up the gcloud CLI, this flag is optional.
  Otherwise, omitting it might cause a
  [permission denied error](https://cloud.google.com/docs/quotas/troubleshoot#gcloud_cli_errors).
  For more information, see
  [Set the quota project](https://cloud.google.com/docs/quotas/set-quota-project#set-project-programmatically).

The output would contain data specific to your configuration and look similar
to the following example output:

```
createTime: 'CREATE_TIME'
dimensions:
  gpu_family: NVIDIA_H100
  region: us-east4
etag: ETAG_VALUE
name: projects/12345/locations/global/quotaPreferences/PREFERENCE_ID
quotaConfig:
  grantedValue: '0'
  preferredValue: '128'
  traceId: TRACE_ID
quotaId: GPUS-PER-GPU-FAMILY-per-project-region
reconciling: true
service: compute.googleapis.com
updateTime: 'UPDATE_TIME'
```

## Enable quota adjuster through a client project

A client project refers to the project used by an application or user to access
and interact with Google Cloud resources, while a resource project is the
underlying project where those resources are stored and managed.

To enable quota adjuster through a client project using
the gcloud CLI, follow these steps:

1. Create a client project:
  ```
  gcloud projects create CLIENT_PROJECT_ID
  gcloud config set project CLIENT_PROJECT_ID
  ```
  Replace `CLIENT_PROJECT_ID` with the ID for the project
  you want to create. Project IDs are immutable and can be set only during
  project creation. They must start with a lowercase letter and can have
  lowercase ASCII letters, digits or hyphens. Project IDs must be between
  6 and 30 characters.
2. Enable the Cloud Quotas API on the client project:
  ```
  gcloud services enable cloudquotas.googleapis.com
  ```
3. Create a
  [service account](https://cloud.google.com/iam/docs/service-accounts-create) in the client project:
  ```
  gcloud iam service-accounts create SA_NAME \
    --display-name SA_DISPLAY_NAME \
    --project=CLIENT_PROJECT_ID
  ```
  Replace the following:
  - `SA_NAME`: the internal name of the new service account.
    Used to generate an IAM_ACCOUNT (an IAM internal email
    address used as an identifier of service account), which must be passed to
    subsequent commands.
  - `SA_DISPLAY_NAME`: the display name of the
    service account.
  - `CLIENT_PROJECT_ID`: the ID of the client project.
4. Create a [service account key](https://cloud.google.com/iam/docs/keys-create-delete):
  ```
  gcloud iam service-accounts keys create KEY_FILE \
    --iam-account=SA_NAME@CLIENT_PROJECT_ID.iam.gserviceaccount.com
  ```
  Replace the following:
  - `KEY_FILE`: the path to the JSON service account key file.
  - `SA_NAME@CLIENT_PROJECT_ID.iam.gserviceaccount.com`:
    the service account email address.
5. Grant IAM permissions to the service account:
  ```
  gcloud projects add-iam-policy-binding CLIENT_PROJECT_ID \
    --member="serviceAccount:SA_NAME@CLIENT_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/serviceusage.serviceUsageConsumer"
  gcloud projects add-iam-policy-binding RESOURCE_PROJECT_ID \
    --member="serviceAccount:SA_NAME@CLIENT_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/cloudquotas.admin"
  ```
  Replace the following:
  - `CLIENT_PROJECT_ID`: the ID of the client project.
  - `RESOURCE_PROJECT_ID`: the ID of the resource project.
  - `SA_NAME@CLIENT_PROJECT_ID.iam.gserviceaccount.com`:
    the service account email address.
6. Activate the service account using the service account key that you created earlier:
  ```
  gcloud auth activate-service-account --key-file=KEY_FILE
  ```
7. Enable quota adjuster on your resource project by specifying
  the project and the enablement setting:
  ```
  gcloud beta quotas adjuster settings update --project=RESOURCE_PROJECT_ID \
    --enablement=enabled
  ```
  The enablement setting is required when using the gcloud CLI and
  must be set to `enabled` or `disabled`.
8. Optional: To view the current quota adjuster settings, run the
  following command:
  ```
  gcloud beta quotas adjuster settings describe --project=RESOURCE_PROJECT_ID
  ```
  The output is similar to the following example:
  ```
  enablement: ENABLED
  etag: 8izmJp6EI__mOfLyhkQU9
  name: projects/RESOURCE_PROJECT_ID/locations/global/quotaAdjusterSettings
  updateTime: '2025-01-10T17:22:37.883221181Z'
  ```

To enable quota adjuster for multiple client projects, follow the previous
steps 5 to 8. When doing so, make sure the following conditions are met:

- The Cloud Quotas API is enabled on the client project.
- The service account has the `cloudquotas.admin` IAM role on
  all the resource projects that you want to enable
  quota adjuster on.

## Other services with quota-related gcloud CLI commands

In addition to `gcloud beta quotas`, some services have their own command-line access
to quota and resource usage information.

For example, Compute Engine lets you access quota information. For details,
see the following Compute Engine sections:

- [Allocation quotas](https://cloud.google.com/compute/quotas#checking_your_quota)
- The [gcloud CLI compute overview](https://cloud.google.com/compute/docs/gcloud-compute)
- The [gcloud CLI compute](https://cloud.google.com/sdk/gcloud/reference/compute)
  section of the Google Cloud SDK reference

## What's next

- To troubleshoot issues with `gcloud beta quotas` commands,
  see [Troubleshooting gcloud CLI errors](https://cloud.google.com/docs/quotas/troubleshoot#gcloud_cli_errors).
- For details about `gcloud beta quotas` commands and flags, see the
  [gcloud beta quotas](https://cloud.google.com/sdk/gcloud/reference/beta/quotas)
  section of the Google Cloud CLI reference.
- For more information about quotas terminology, see
  [Understand quota and system limit terminology](https://cloud.google.com/docs/quotas/terminology).

   Was this helpful?
