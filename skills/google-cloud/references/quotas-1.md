# Cloud Quotas API overviewStay organized with collectionsSave and categorize content based on your preferences. and more

# Cloud Quotas API overviewStay organized with collectionsSave and categorize content based on your preferences.

> Automate quota increase adjustment requests and programmatically adjust quotas with the Cloud Quotas API

# Cloud Quotas API overviewStay organized with collectionsSave and categorize content based on your preferences.

The Cloud Quotas API lets you programmatically adjust project-level
[quotas](https://cloud.google.com/docs/quotas/overview)
and automate project-level quota [adjustment requests](https://cloud.google.com/docs/quotas/overview#about_increase_requests). For
example, you can use the Cloud Quotas API to:

- **Automate quota adjustments**: You can use the Cloud Quotas API to request quota
  adjustments based on your own criteria. For example, to avoid quota
  exceeded errors, you can use the API to programmatically request a quota
  adjustment when Compute Engine resources reach 80% of the available quota.
- **Reuse quota configurations across projects**: The Cloud Quotas API can clone
  your quota configurations from project to project. If there is a known set of
  quotas that need to be increased for every new Google Cloud project, you can
  use the Cloud Quotas API to automate this in the creation logic of your project.
  Quota adjustment requests are subject to Google Cloud approval.
- **Serve customer quota requests**: If you are a SaaS provider integrated with
  Google Cloud, you might receive quota increase requests through a
  customer-facing portal other than the Google Cloud console. These requests must be
  forwarded to Google Cloud for processing. The Cloud Quotas API can automatically
  forward customer requests.
- **Enable client configuration version control**: The Cloud Quotas API is
  declarative. You can treat quota configurations as code and store
  configurations in your own version controlled system for history and rollback.

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

## Service endpoint

The service endpoint is a base URL that specifies the network address of an API
service. One service might have multiple endpoints. The Cloud Quotas API
service has the following endpoint and all URIs are relative to it:

`https://cloudquotas.googleapis.com`

## Required roles

To get the permissions that
      you need to access the `cloudquotas_quotaPreferences`, `cloudquotas_quotaInfos`, and `cloudquotas_quotaAdjusterSettings` resources,

      ask your administrator to grant you the

  Cloud Quotas Admin (`cloudquotas.admin`)
   IAM role on the project.

  For more information about granting roles, see [Manage access to projects, folders, and organizations](https://cloud.google.com/iam/docs/granting-changing-revoking-access).

This predefined role contains

        the permissions required to access the `cloudquotas_quotaPreferences`, `cloudquotas_quotaInfos`, and `cloudquotas_quotaAdjusterSettings` resources. To see the exact permissions that are
        required, expand the **Required permissions** section:

The following permissions are required to access the `cloudquotas_quotaPreferences`, `cloudquotas_quotaInfos`, and `cloudquotas_quotaAdjusterSettings` resources:

- ` cloudquotas.quotas.update `
- ` cloudquotas.quotas.get `
- ` monitoring.timeSeries.list `
- ` resourcemanager.projects.get `
- ` resourcemanager.projects.list`

You might also be able to get
          these permissions
        with [custom roles](https://cloud.google.com/iam/docs/creating-custom-roles) or
        other [predefined roles](https://cloud.google.com/iam/docs/roles-overview#predefined).

## API resource model

The Cloud Quotas API resource model consists of two resources:
`QuotaPreference` and `QuotaInfo`.

### Quota preference

The `QuotaPreference` resource represents your quota preference for a particular
[dimension combination](https://cloud.google.com/docs/quotas/configure-dimensions#dimension_precedence). Use
this resource to adjust the quotas in your projects, folders, or organizations.

#### Set a preferred value for a region

The following example shows a `QuotaPreference` resource in a
`CreateQuotaPreference` method.

```
{
    "service": "compute.googleapis.com",
    "quotaId": "GPUS-PER-GPU-FAMILY-per-project-region",
    "quotaConfig": {
        "preferredValue": 100
    },
    "dimensions": {
        "region": "us-central1"
    }
}
```

The `preferredValue` of 100 indicates that the
requester wants the `GPUS-PER-GPU-FAMILY-per-project-region` quota to be set to
that value. The dimensions field indicates the preference only applies to region
`us-central1`.

#### Verify the granted value

View your quota preference and look at the `grantedValue` field to verify the
granted value.

To view your quota preference using the Google Cloud CLI, run the following in
your terminal:

```
gcloud alpha quotas preferences describe QUOTA_PREFERENCE_ID --project=PROJECT
```

Replace the following:

- `QUOTA_PREFERENCE_ID`: the ID of your quota preference.
  This is the value that was specified when the quota preference was created.
- `PROJECT`: the ID or number of your Google Cloud
  project.

If you made a quota adjustment request and the request is partially approved,
a `stateDetail` field appears after the `grantedValue` field. The
`grantedValue` shows the adjustment that was made, and the `stateDetail` field
describes the partially approved state.

To see if the granted value is the final value approved, look at the
`reconciling` field. If your request is still undergoing evaluation, the
`reconciling` field is set to `true`. If the `reconciling` field is set to
`false` or is omitted, the granted value is the final value approved.

The following code snippets show examples of the quota preference object. They
use a demo quota preference with the ID
`compute_googleapis_com-gpus-us-central1`.

If you view your quota preference using the gcloud CLI, the
output looks similar to the following:

```
createTime: '2023-01-15T01:30:15.01Z'
dimensions:
    region: us-central1
name: projects/PROJECT_NUMBER/locations/global/quotaPreferences/compute_googleapis_com-gpus-us-central1
quotaConfig:
    grantedValue: '100'
    preferredValue: '100'
    traceId: 123acd-345df23
    requestOrigin: ORIGIN_UNSPECIFIED
service: compute.googleapis.com
quotaId: GPUS-PER-GPU-FAMILY-per-project-region
updateTime: '2023-01-16T02:35:16.01Z'
```

If you view your quota preference using the Cloud Quotas API, the
output looks similar to the following:

```
{
    "name": "projects/PROJECT_NUMBER/locations/global/quotaPreferences/compute_googleapis_com-gpus-us-central1",
    "service": "compute.googleapis.com",
    "quotaId": "GPUS-PER-GPU-FAMILY-per-project-region",
    "quotaConfig": {
        "preferredValue": 100,
        "grantedValue": 100,
        "traceId": "123acd-345df23",
        "requestOrigin": "ORIGIN_UNSPECIFIED"
    },
    "dimensions": {
        "region": "us-central1"
    },
    "createTime": "2023-01-15T01:30:15.01Z",
    "updateTime": "2023-01-16T02:35:16.01Z"
}
```

This output includes the following values:

- `PROJECT_NUMBER`: an automatically generated
  unique identifier for your project.

The response shows a `grantedValue` of 100, meaning
the `preferredValue` from the previous example has been approved and fulfilled.
Preferences for different dimensions are different `QuotaPreference`
resources. For example, `QuotaPreference` for CPU in regions `us-central1` and
`us-east1` are two distinct resources.

#### Quota preference is required

`QuotaPreference` resources are used to indicate your preferred value for a
particular quota. The current value for a particular quota is based on:

- `QuotaPreference` requests made by you.
- Approved quota increase requests by Google Cloud.
- Changes to quotas initiated by Google Cloud.

The ability to delete a `QuotaPreference` is not supported. However, you can set
a preferred quota value lower than the Google Cloud approved value to add further guardrails.

For more information on the `QuotaPreference` resource, see the [Cloud Quotas API Reference](https://cloud.google.com/docs/quotas/reference/rest).

For more information on the `QuotaPreference` queries, see
[Implement common use cases](https://cloud.google.com/docs/quotas/implement-common-use-cases).

### Quota info

`QuotaInfo` is a read-only resource that provides information about a particular
quota for a given project, folder, or organization. It displays information from
the quotas defined by Google Cloud services and any fulfilled quota
adjustments initiated by customers. The `QuotaInfo` resource contains
information such as the metadata, container type, and dimensions.

#### Set different quota values by region

The following `QuotaInfo` resource example shows that the CPU quota for the
project is 200 for region `us-central1` and 100 for all other regions.

```
{
    "name": "projects/PROJECT_NUMBER/locations/global/services/compute.googleapis.com/quotaInfos/CPUS-per-project-region",
    "quotaId": "CPUS-per-project-region",
    "metric": "compute.googleapis.com/cpus",
    "containerType": "PROJECT",
    "dimensions": [
        "region"
    ],
    "isPrecise": true,
    "quotaDisplayName": "CPUs per project per region",
    "metricDisplayName": "CPUs",
    "dimensionsInfo": [
        {
            "dimensions": {
                "region": "us-central1"
            },
            "details": {
                "quotaValue": 200,
                "resetValue": 200
            },
            "applicableLocations": [
                "us-central1",
            ]
        },
        {
            "details": {
                "quotaValue": 100,
                "resetValue": 100
            },
            "applicableLocations": [
                "us-central2",
                "us-west1",
                "us-east1"
            ]
        }
    ]
}
```

This output includes the following values:

- `PROJECT_NUMBER`: an automatically generated
  unique identifier for your project.

#### Set a global quota

The following `QuotaInfo` resource example shows a rate quota with a per minute
refresh interval. The dimensions are blank, which indicates that this is a
global quota. All quotas without a region or zone dimension are global.

```
{
    "name": "projects/PROJECT_NUMBER/locations/global/services/compute.googleapis.com/quotaInfos/ReadRequestsPerMinutePerProject",
    "quotaId": "ReadRequestsPerMinutePerProject",
    "metric": "compute.googleapis.com/read_requests",
    "refreshInterval": "minute",
    "containerType": "PROJECT",
    "dimensions": [],
    "isPrecise": false,
    "quotaDisplayName": "Read Requests per Minute",
    "metricDisplayName": "Read Requests",
    "dimensionsInfo": [
        {
            "details": {
                "quotaValue": 100,
                "resetValue": 200
            },
            "applicableLocations": [
                "global"
            ]
        }
    ]
}
```

This output includes the following values:

- `PROJECT_NUMBER`: an automatically generated
  unique identifier for your project.

For more details on the `QuotaInfo` resource, see the [Cloud Quotas API Reference](https://cloud.google.com/docs/quotas/reference/rest).

For more details on the `QuotaPreference` queries, see
[Implement common use cases](https://cloud.google.com/docs/quotas/implement-common-use-cases).

### Quota adjuster settings

The `QuotaAdjusterSettings` resource ([Preview](https://cloud.google.com/products#product-launch-stages))
represents your quota adjuster settings for a particular project. When enabled,
the quota adjuster monitors your usage of the specified resources and issues
quota adjustment requests when resource use approaches its quota value.

- To view the current quota adjuster settings for a project, use a
  [GET](https://cloud.google.com/docs/quotas/reference/rest/v1beta/projects.locations.quotaAdjusterSettings/getQuotaAdjusterSettings)
  operation to retrieve the `QuotaAdjusterSettings` resource.
- To enable quota adjuster for a project, use an
  [PATCH](https://cloud.google.com/docs/quotas/reference/rest/v1beta/projects.locations.quotaAdjusterSettings/updateQuotaAdjusterSettings)
  operation to set the following `QuotaAdjusterSettings` resource options:
  ```
  "quota_adjuster_settings" :{
       "name": "projects/PROJECT_NUMBER/locations/global/quotaAdjusterSettings",
       "enablement": ENABLED,
  }
  ```
  Replace `PROJECT_NUMBER` with the unique identifier for
  your project.

For details,
see [Enable the quota adjuster](https://cloud.google.com/docs/quotas/quota-adjuster#enable)
and [Disable the quota adjuster](https://cloud.google.com/docs/quotas/quota-adjuster#disable).

## Resource names

Resources are named entities and are identified by resource names. Resource
names are used in all requests and responses, and each resource must have
its own unique resource name. Each resource name is encoded by a set of fields.

### Quota preference resource

The naming convention for a `QuotaPreference` resource uses the following pattern:

```
projects/PROJECT_NUMBER/locations/global/quotaPreferences/QUOTA_PREFERENCE_ID
```

You can set the `quotaPreferenceId` when creating a quota preference, otherwise
an ID is generated. It is recommended that a `quotaPreferenceId` naming scheme
encodes the service name, quota ID, location and other dimensions. The
`quotaPreferenceId` must be unique for the project, folder, or organization.

As an example `quotaPreference`
One pattern to encode your quota preference ID is the following:

```
SERVICE_LOCATION_DIMENSION1-VALUES-IN-ORDER
```

The following example demonstrates this pattern:

```
compute_us-central1_nvidia-200
```

With a resource name, you should use the
[GET](https://cloud.google.com/docs/quotas/reference/rest/v1beta/organizations.locations.quotaPreferences/get)
method to retrieve a `QuotaPreference`. You can also call the
[PATCH](https://cloud.google.com/docs/quotas/reference/rest/v1beta/organizations.locations.quotaPreferences/patch)
method with the `allow_missing` option enabled to create or update a
`QuotaPreference`.

### Quota info resource

The naming convention for a `QuotaInfo` resource uses the following pattern:

```
projects/PROJECT_NUMBER/locations/global/services/SERVICE_NAME/quotaInfos/QUOTA_ID
```

### Quota adjuster settings resource

The naming convention for a `QuotaAdjusterSettings` resource uses the following pattern:

```
projects/PROJECT_NUMBER/locations/global/quotaAdjusterSettings
```

## What's next?

- [Implement common use cases](https://cloud.google.com/docs/quotas/implement-common-use-cases)
- Cloud Quotas API [reference](https://cloud.google.com/docs/quotas/reference/rest)
- Understand [quotas](https://cloud.google.com/docs/quotas/overview)

   Was this helpful?

---

# APIs and referenceStay organized with collectionsSave and categorize content based on your preferences.

> Get details about client libraries and APIs

# APIs and referenceStay organized with collectionsSave and categorize content based on your preferences.

- [Use REST APIs to configure and manage Cloud Quotas in your
      language of choice.](https://cloud.google.com/docs/quotas/reference/rest)
- [Get started with Cloud Quotas in C++, C#, Go, Java, Node.js, PHP,
      Python, or Ruby.](https://cloud.google.com/docs/quotas/reference/libraries)

- [To view and manage quotas using gcloud CLI commands, refer to
      these examples.](https://cloud.google.com/docs/quotas/gcloud-cli-examples)
- [For more about the syntax ofgcloud beta quotascommands, see the Google Cloud SDK reference.Important: These commands are in
        preview and might change without notice.](https://cloud.google.com/sdk/gcloud/reference/beta/quotas)

---

# Cloud Quotas audit loggingStay organized with collectionsSave and categorize content based on your preferences.

# Cloud Quotas audit loggingStay organized with collectionsSave and categorize content based on your preferences.

This document describes audit logging for Cloud Quotas. Google Cloud services
generate audit logs that record administrative and access activities within your Google Cloud resources.
For more information about Cloud Audit Logs, see the following:

- [Types of audit logs](https://cloud.google.com/logging/docs/audit#types)
- [Audit log entry structure](https://cloud.google.com/logging/docs/audit#audit_log_entry_structure)
- [Storing and routing audit logs](https://cloud.google.com/logging/docs/audit#storing_and_routing_audit_logs)
- [Cloud Logging pricing summary](https://cloud.google.com/stackdriver/pricing#logs-pricing-summary)
- [Enable Data Access audit logs](https://cloud.google.com/logging/docs/audit/configure-data-access)

## Service name

Cloud Quotas audit logs use the service name `cloudquotas.googleapis.com`.
Filter for this service:

```
protoPayload.serviceName="cloudquotas.googleapis.com"
```

## Methods by permission type

Each IAM permission has a `type` property, whose value is an enum
that can be one of four values: `ADMIN_READ`, `ADMIN_WRITE`,
`DATA_READ`, or `DATA_WRITE`. When you call a method,
Cloud Quotas generates an audit log whose category is dependent on the
`type` property of the permission required to perform the method.

Methods that require an IAM permission with the `type` property value
of `DATA_READ`, `DATA_WRITE`, or `ADMIN_READ` generate
[Data Access](https://cloud.google.com/logging/docs/audit#data-access) audit logs.

Methods that require an IAM permission with the `type` property value
of `ADMIN_WRITE` generate
[Admin Activity](https://cloud.google.com/logging/docs/audit#admin-activity) audit logs.

API methods in the following list that are marked with (LRO) are long-running operations (LROs).
These methods usually generate two audit log entries: one when the operation starts and
another when it ends. For more information see [Audit logs for long-running operations](https://cloud.google.com/logging/docs/audit/understanding-audit-logs#lro).

| Permission type | Methods |
| --- | --- |
| ADMIN_READ | google.api.cloudquotas.v1.CloudQuotas.GetQuotaInfogoogle.api.cloudquotas.v1.CloudQuotas.GetQuotaPreferencegoogle.api.cloudquotas.v1.CloudQuotas.ListQuotaInfosgoogle.api.cloudquotas.v1.CloudQuotas.ListQuotaPreferencesgoogle.api.cloudquotas.v1beta.CloudQuotas.GetQuotaInfogoogle.api.cloudquotas.v1beta.CloudQuotas.GetQuotaPreferencegoogle.api.cloudquotas.v1beta.CloudQuotas.ListQuotaInfosgoogle.api.cloudquotas.v1beta.CloudQuotas.ListQuotaPreferencesgoogle.api.cloudquotas.v1beta.QuotaAdjusterSettingsManager.GetQuotaAdjusterSettings |
| ADMIN_WRITE | google.api.cloudquotas.v1.CloudQuotas.CreateQuotaPreferencegoogle.api.cloudquotas.v1.CloudQuotas.UpdateQuotaPreferencegoogle.api.cloudquotas.v1beta.CloudQuotas.CreateQuotaPreferencegoogle.api.cloudquotas.v1beta.CloudQuotas.UpdateQuotaPreferencegoogle.api.cloudquotas.v1beta.QuotaAdjusterSettingsManager.UpdateQuotaAdjusterSettings |

## API interface audit logs

For information about how and which permissions are evaluated for each method,
see the Identity and Access Management documentation for Cloud Quotas.

### google.api.cloudquotas.v1.CloudQuotas

The following audit logs are associated with methods belonging to
`google.api.cloudquotas.v1.CloudQuotas`.

#### CreateQuotaPreference

- **Method**: `google.api.cloudquotas.v1.CloudQuotas.CreateQuotaPreference`
- **Audit log type**: [Admin activity](https://cloud.google.com/logging/docs/audit#admin-activity)
- **Permissions**:
  - `cloudquotas.quotas.update - ADMIN_WRITE`
- **Method is a long-running or streaming operation**:
  No.
- **Filter for this method**: `
      protoPayload.methodName="google.api.cloudquotas.v1.CloudQuotas.CreateQuotaPreference"
    `

#### GetQuotaInfo

- **Method**: `google.api.cloudquotas.v1.CloudQuotas.GetQuotaInfo`
- **Audit log type**: [Data access](https://cloud.google.com/logging/docs/audit#data-access)
- **Permissions**:
  - `cloudquotas.quotas.get - ADMIN_READ`
- **Method is a long-running or streaming operation**:
  No.
- **Filter for this method**: `
      protoPayload.methodName="google.api.cloudquotas.v1.CloudQuotas.GetQuotaInfo"
    `

#### GetQuotaPreference

- **Method**: `google.api.cloudquotas.v1.CloudQuotas.GetQuotaPreference`
- **Audit log type**: [Data access](https://cloud.google.com/logging/docs/audit#data-access)
- **Permissions**:
  - `cloudquotas.quotas.get - ADMIN_READ`
- **Method is a long-running or streaming operation**:
  No.
- **Filter for this method**: `
      protoPayload.methodName="google.api.cloudquotas.v1.CloudQuotas.GetQuotaPreference"
    `

#### ListQuotaInfos

- **Method**: `google.api.cloudquotas.v1.CloudQuotas.ListQuotaInfos`
- **Audit log type**: [Data access](https://cloud.google.com/logging/docs/audit#data-access)
- **Permissions**:
  - `cloudquotas.quotas.get - ADMIN_READ`
- **Method is a long-running or streaming operation**:
  No.
- **Filter for this method**: `
      protoPayload.methodName="google.api.cloudquotas.v1.CloudQuotas.ListQuotaInfos"
    `

#### ListQuotaPreferences

- **Method**: `google.api.cloudquotas.v1.CloudQuotas.ListQuotaPreferences`
- **Audit log type**: [Data access](https://cloud.google.com/logging/docs/audit#data-access)
- **Permissions**:
  - `cloudquotas.quotas.get - ADMIN_READ`
- **Method is a long-running or streaming operation**:
  No.
- **Filter for this method**: `
      protoPayload.methodName="google.api.cloudquotas.v1.CloudQuotas.ListQuotaPreferences"
    `

#### UpdateQuotaPreference

- **Method**: `google.api.cloudquotas.v1.CloudQuotas.UpdateQuotaPreference`
- **Audit log type**: [Admin activity](https://cloud.google.com/logging/docs/audit#admin-activity)
- **Permissions**:
  - `cloudquotas.quotas.update - ADMIN_WRITE`
- **Method is a long-running or streaming operation**:
  No.
- **Filter for this method**: `
      protoPayload.methodName="google.api.cloudquotas.v1.CloudQuotas.UpdateQuotaPreference"
    `

### google.api.cloudquotas.v1beta.CloudQuotas

The following audit logs are associated with methods belonging to
`google.api.cloudquotas.v1beta.CloudQuotas`.

#### CreateQuotaPreference

- **Method**: `google.api.cloudquotas.v1beta.CloudQuotas.CreateQuotaPreference`
- **Audit log type**: [Admin activity](https://cloud.google.com/logging/docs/audit#admin-activity)
- **Permissions**:
  - `cloudquotas.quotas.update - ADMIN_WRITE`
- **Method is a long-running or streaming operation**:
  No.
- **Filter for this method**: `
      protoPayload.methodName="google.api.cloudquotas.v1beta.CloudQuotas.CreateQuotaPreference"
    `

#### GetQuotaInfo

- **Method**: `google.api.cloudquotas.v1beta.CloudQuotas.GetQuotaInfo`
- **Audit log type**: [Data access](https://cloud.google.com/logging/docs/audit#data-access)
- **Permissions**:
  - `cloudquotas.quotas.get - ADMIN_READ`
- **Method is a long-running or streaming operation**:
  No.
- **Filter for this method**: `
      protoPayload.methodName="google.api.cloudquotas.v1beta.CloudQuotas.GetQuotaInfo"
    `

#### GetQuotaPreference

- **Method**: `google.api.cloudquotas.v1beta.CloudQuotas.GetQuotaPreference`
- **Audit log type**: [Data access](https://cloud.google.com/logging/docs/audit#data-access)
- **Permissions**:
  - `cloudquotas.quotas.get - ADMIN_READ`
- **Method is a long-running or streaming operation**:
  No.
- **Filter for this method**: `
      protoPayload.methodName="google.api.cloudquotas.v1beta.CloudQuotas.GetQuotaPreference"
    `

#### ListQuotaInfos

- **Method**: `google.api.cloudquotas.v1beta.CloudQuotas.ListQuotaInfos`
- **Audit log type**: [Data access](https://cloud.google.com/logging/docs/audit#data-access)
- **Permissions**:
  - `cloudquotas.quotas.get - ADMIN_READ`
- **Method is a long-running or streaming operation**:
  No.
- **Filter for this method**: `
      protoPayload.methodName="google.api.cloudquotas.v1beta.CloudQuotas.ListQuotaInfos"
    `

#### ListQuotaPreferences

- **Method**: `google.api.cloudquotas.v1beta.CloudQuotas.ListQuotaPreferences`
- **Audit log type**: [Data access](https://cloud.google.com/logging/docs/audit#data-access)
- **Permissions**:
  - `cloudquotas.quotas.get - ADMIN_READ`
- **Method is a long-running or streaming operation**:
  No.
- **Filter for this method**: `
      protoPayload.methodName="google.api.cloudquotas.v1beta.CloudQuotas.ListQuotaPreferences"
    `

#### UpdateQuotaPreference

- **Method**: `google.api.cloudquotas.v1beta.CloudQuotas.UpdateQuotaPreference`
- **Audit log type**: [Admin activity](https://cloud.google.com/logging/docs/audit#admin-activity)
- **Permissions**:
  - `cloudquotas.quotas.update - ADMIN_WRITE`
- **Method is a long-running or streaming operation**:
  No.
- **Filter for this method**: `
      protoPayload.methodName="google.api.cloudquotas.v1beta.CloudQuotas.UpdateQuotaPreference"
    `

### google.api.cloudquotas.v1beta.QuotaAdjusterSettingsManager

The following audit logs are associated with methods belonging to
`google.api.cloudquotas.v1beta.QuotaAdjusterSettingsManager`.

#### GetQuotaAdjusterSettings

- **Method**: `google.api.cloudquotas.v1beta.QuotaAdjusterSettingsManager.GetQuotaAdjusterSettings`
- **Audit log type**: [Data access](https://cloud.google.com/logging/docs/audit#data-access)
- **Permissions**:
  - `cloudquotas.quotas.get - ADMIN_READ`
- **Method is a long-running or streaming operation**:
  No.
- **Filter for this method**: `
      protoPayload.methodName="google.api.cloudquotas.v1beta.QuotaAdjusterSettingsManager.GetQuotaAdjusterSettings"
    `

#### UpdateQuotaAdjusterSettings

- **Method**: `google.api.cloudquotas.v1beta.QuotaAdjusterSettingsManager.UpdateQuotaAdjusterSettings`
- **Audit log type**: [Admin activity](https://cloud.google.com/logging/docs/audit#admin-activity)
- **Permissions**:
  - `cloudquotas.quotas.update - ADMIN_WRITE`
- **Method is a long-running or streaming operation**:
  No.
- **Filter for this method**: `
      protoPayload.methodName="google.api.cloudquotas.v1beta.QuotaAdjusterSettingsManager.UpdateQuotaAdjusterSettings"
    `

## System events

System Event audit logs are generated by GCP systems, not
direct user action. For more information, see
[System Event audit logs](https://cloud.google.com/logging/docs/audit#system-event).

| Method Name | Filter For This Event | Notes |
| --- | --- | --- |
| google.cloud.quotaadjuster.v1main.QuotaAdjusterService.AutoAdjustQuota | protoPayload.methodName="google.cloud.quotaadjuster.v1main.QuotaAdjusterService.AutoAdjustQuota" |  |

---

# Billing questionsStay organized with collectionsSave and categorize content based on your preferences.

> Get help with billing questions.

# Billing questionsStay organized with collectionsSave and categorize content based on your preferences.

Cloud Quotas is offered at no additional charge for Google Cloud
customers. You will be charged only for use of other Google Cloud
services. For information about the pricing of other Google Cloud
services, see the
[Google Cloud pricing calculator](https://cloud.google.com/products/calculator).

To get help with billing questions, use the following resources:

- To view billing reports, see [View your billing reports and cost trends](https://cloud.google.com/billing/docs/how-to/reports)
- To learn more about billing, read the
  [Cloud Billing documentation](https://cloud.google.com/billing/docs)
- To resolve billing concerns, use the
  [Google Cloud Billing Troubleshooter](https://support.google.com/cloud/troubleshooter/7279311)
- To request help with billing questions, contact
  [Cloud Billing Support](https://cloud.google.com/support/billing)
- To change or disable billing on a project, go to the **Billing** page in the
  Google Cloud console:
  [Go to Billing](https://console.cloud.google.com/billing/projects)
  For more information, see
  [Modify a project's billing settings](https://cloud.google.com/billing/docs/how-to/modify-project).

## What's Next

- [Learn more about viewing and managing quotas](https://cloud.google.com/docs/quotas/view-manage)
- [Request a quota adjustment](https://cloud.google.com/docs/quotas/help/request_increase)
- [Read the Cloud Quotas release notes](https://cloud.google.com/docs/quotas/release-notes)

   Was this helpful?

---

# Configure Cloud Quotas dimensionsStay organized with collectionsSave and categorize content based on your preferences.

> Configure Cloud Quotas dimensions

# Configure Cloud Quotas dimensionsStay organized with collectionsSave and categorize content based on your preferences.

Cloud Quotas dimensions represent different ways of measuring resource
usage in Google Cloud. Dimensions are typically a region, zone, Google Cloud
user, or product attribute.

The Cloud Quotas API represents dimensions as key-value pairs. The `key` is
the dimension name (for example, `region`). The `value` is the assigned value
for the dimension (for example, a region such as `us-central1`). Keys and values
are case sensitive.

For example, Compute Engine measures VM use by using different dimensions. The
`region` dimension measures the number of VMs you have in a given region.
Compute Engine also has a number of product attribute dimensions, including
`gpu_family`. The `gpu_family` dimension measures the number of GPUs of a
given family in your Google Cloud project.

## View dimensions

You can view the dimensions for quotas and system limits by looking in the
Google Cloud console, using the Google Cloud CLI, querying the REST API, or through
client libraries. To view dimensions that you haven't specified a value for, use
the gcloud CLI. Also use the gcloud CLI to view dimensions
for quotas and system limits that don't have regional or zonal dimensions if
your project doesn't already use the associated resource. This section shows how
to view dimensions by using the console and by using the gcloud CLI.

1. In the Google Cloud console, go to the
  **IAM & Admin>Quotas & System Limits** page:
  [Go to Quotas & System Limits](https://console.cloud.google.com/iam-admin/quotas)
  The table on this page displays dimensions in the **Dimensions** column.
2. If you don't see the **Dimensions** column, take the following steps.
  Otherwise, skip this step.
  1. Click  **Column display options**.
  2. Select **Dimensions**.
  3. Click **OK**. The **Dimensions** column appears in the table.
3. To filter the results, enter a property name or value in the field next to
   **Filter**.
  - To filter by product, begin entering the product name and select from the
    list that appears.
  - To filter by dimension, enter your dimension using the following format:
    `dimension_name:dimension_value`. For example, to see quotas and system limits
    defined for the us-central1 region, enter: `region:us-central`.

### Understand blank dimensions

Sometimes the **Dimensions** column is empty. This can happen for the
following reasons:

- The quota or system limit value is the default value and applies for all
  dimensions. For some quotas and system limits, the console shows a line
  that lists the default quota or system limit value for reference. Because
  the default applies to all dimension values, the **Dimensions** column is
  blank. Look at the **Name** column to identify these entries. The **Name**
  column indicates these entries with the word "default" in parenthesis at
  the end of the quota or system limit name.
  For example, the quota `SetIamPolicyRequestsPerMinutePerProject` is defined
  on the `region` dimension. The console shows a reference entry, and an
  entry for any regions or zones that either have use or have an adjusted
  quota value. In the **Name** column, the reference entry is listed as
  "SetIAMPolicy requests per minute per region (default)." For this entry,
  the **Dimensions** column is empty.
- No dimensions apply. For example, the Compute Engine quota
  `NETWORKS-per-project` isn't associated with a region, zone, or product
  attribute, so there are no dimensions to display.

You can use the gcloud CLI to view dimensions for a single quota or
system limit, or for all quotas and system limits associated with a given
product. Viewing dimensions for a single quota or system limit is usually
faster than viewing dimensions for all quotas and system limits associated
with a product. The response to a query for a single quota is typically about
200 lines. The response to a query for a product can exceed 2,000 lines.

### View dimensions for a single quota or system limit with gcloud

To view dimensions for a single quota or system limit using the
gcloud CLI, run the following command in your terminal:

```
gcloud beta quotas info describe QUOTA_ID --project=PROJECT_ID --service=SERVICE_ID
```

Replace the following:

- `QUOTA_ID`: the ID for the quota or system limit. If
  you don't know your quota ID, choose one of the following options:
  1. Find it by using the console as described in
    [Find your quota ID](https://cloud.google.com/docs/quotas/gcloud-cli-examples#find_your_quota_id).
  2. View all dimensions for the product associated with the quota or system
    limit you're interested in. This command doesn't require the quota ID.
    See the section
    [View dimensions for a product with gcloud CLI](#gcloud-view-product).
- `PROJECT_ID`: The ID of your Google Cloud
  project. To find your project ID, choose one of the following options:
  1. To find your project ID by using the console, see
    [Identifying projects](https://cloud.google.com/resource-manager/docs/creating-managing-projects#identifying_projects).
  2. If you set your current project as your default project in the
    gcloud CLI configuration, find your project ID get by running the
    following gcloud command in your terminal:
    ```
    gcloud config get-value project
    ```
- `SERVICE_ID`: the service ID of the product associated
  with the quota or system limit. For example, if the quota is for Compute Engine
  A2 CPUs, the service ID is `compute.googleapis.com`.

### View dimensions for a product with gcloud CLI

To view dimensions for a single quota or system limit using the
gcloud CLI, run the following command in your terminal:

```
gcloud beta quotas info list --project=PROJECT_ID --service=SERVICE_ID
```

Replace the following:

- `PROJECT_ID`: The ID of your Google Cloud
  project. To find your project ID, choose one of the following options:
  1. To find your project ID by using the console, see
    [Identifying projects](https://cloud.google.com/resource-manager/docs/creating-managing-projects#identifying_projects).
  2. If you set your current project as your default project in the
    gcloud CLI configuration, find your project ID get by running the
    following gcloud command in your terminal:
    ```
    gcloud config get-value project
    ```
- `SERVICE_ID`: the service ID of the product associated
  with the quota or system limit. For example, if the quota is for Compute Engine
  A2 CPUs, the service ID is `compute.googleapis.com`.

## Dimension precedence

Some use cases for the Cloud Quotas API have complex dimension setups.
Quotas can be configured at a more granular level than just regions and zones.
You can accomplish this granularity when you use service-specific dimensions.
For example, the `gpu_family` and `network_id` are service-specific dimensions
in the Compute Engine service. Dimensions are defined by each individual
service and each service might have a different set of service-specific
dimensions.

When working with either location dimensions or service-specific dimensions,
the following precedence is applied:

1. A quota preference configuration with all location and service-specific
  dimensions specified takes precedence over any other configuration.
2. Configurations that specify location dimensions only take precedence over
  configurations containing only service-specific dimensions.

## Combining dimensions

In a quota preference configuration, you can combine dimensions in the following
ways:

1. The configuration may contain *both* location dimensions and service-specific
  dimensions. This is the highest order in precedence.
2. The configuration may *only* contain location dimensions. This configuration
  applies to all service-specific dimensions, except the ones explicitly
  configured with method 1.
3. The configuration may *only* contain service-specific dimensions. This configuration
  applies to all locations except those explicitly configured with method 1 or 2.
4. If the configuration contains *any* service-specific dimensions, it must contain
  all service-specific dimensions.
5. You can have configurations *without any* dimensions. Such configurations
  apply to all locations and all service-specific dimensions, except the ones
  explicitly configured.

   Was this helpful?

---

# Configure VPC Service Controls for Cloud QuotasStay organized with collectionsSave and categorize content based on your preferences.

# Configure VPC Service Controls for Cloud QuotasStay organized with collectionsSave and categorize content based on your preferences.

Google Cloud Virtual Private Cloud (VPC) Service Controls lets you set up a
secure perimeter to guard against data exfiltration. Configure
Cloud Quotas with
[VPC Service Controls](https://cloud.google.com/vpc-service-controls/docs/overview) so that API
requests to Cloud Quotas stay within the VPC
service perimeter boundary.

## Limitations

Because VPC Service Controls enforces boundaries at the project level,
Cloud Quotas requests that originate from clients within the
perimeter can only access organization resources if the organization sets up an
[egress rule](https://cloud.google.com/vpc-service-controls/docs/ingress-egress-rules).
To set up an egress rule, see the VPC Service Controls instructions for
[configuring ingress and egress policies](https://cloud.google.com/vpc-service-controls/docs/configuring-ingress-egress-policies)

## Enforced actions

VPC Service Controls is only enforced on the following
Cloud Quotas actions:

- [Quota preference](https://cloud.google.com/docs/quotas/api-overview#quota_preference) creation,
  update, get and list.
- [Quota info](https://cloud.google.com/docs/quotas/api-overview#quota_info) get and list.

For examples of setting
[QuotaPreference](https://cloud.google.com/docs/quotas/api-overview#quota_preference) and
[QuotaInfo](https://cloud.google.com/docs/quotas/api-overview#quota_info), see the description of
the [API resource model](https://cloud.google.com/docs/quotas/api-overview#api_resource_model).
For reference information, see the
[REST API overview](https://cloud.google.com/docs/quotas/reference/rest).

## Set up

Follow these steps to restrict the Cloud Quotas API to your
VPC service perimeter:

1. Follow the instructions to [set up the Cloud Quotas API](https://cloud.google.com/docs/quotas/development-environment).
2. Follow the [VPC Service Controls Quickstart](https://cloud.google.com/vpc-service-controls/docs/set-up-service-perimeter)
  to complete the following tasks:
  1. [Create a service perimeter](https://cloud.google.com/vpc-service-controls/docs/set-up-service-perimeter#set-up-perimeter).
  2. [Add projects to the perimeter](https://cloud.google.com/vpc-service-controls/docs/set-up-service-perimeter#add-projects-perimeter) that you want to protect.
  3. Restrict the Cloud Quotas API. For example, see these instructions that
    add [other Google Cloud APIs to the VPC service
    perimeter](https://cloud.google.com/vpc-service-controls/docs/set-up-service-perimeter#secure-services-perimeter).

After setting up your service perimeter, VPC Service Controls checks calls
to the Cloud Quotas API to help make sure that the calls originate
from within the same perimeter.

## What's next

- Learn about [VPC Service Controls](https://cloud.google.com/vpc-service-controls/docs/overview).
- See the Cloud Quotas entry in the
  [VPC Service Controls supported products table](https://cloud.google.com/vpc-service-controls/docs/supported-products#table_quotas).
- Refer to the description of the Cloud Quotas
  [API resource model](https://cloud.google.com/docs/quotas/api-overview#api_resource_model) for examples.

   Was this helpful?
