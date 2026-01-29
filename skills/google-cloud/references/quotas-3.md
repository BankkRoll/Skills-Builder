# View and manage quotasStay organized with collectionsSave and categorize content based on your preferences. and more

# View and manage quotasStay organized with collectionsSave and categorize content based on your preferences.

> Discover the Google Cloud quota system that helps you monitor existing quota usage or update API quotas within specific projects.

# View and manage quotasStay organized with collectionsSave and categorize content based on your preferences.

This document describes how you can view quota values in the
Google Cloud console. You can also manage quotas from the
Google Cloud console, Cloud Quotas API, and Google Cloud CLI
(gcloud CLI).

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

The tasks in this document require Identity and Access Management (IAM) roles.

### Required roles

To get the permissions that
      you need to request quota adjustments,

      ask your administrator to grant you the
    following IAM roles on the project, folder, or organization:

- To view quotas:
        [Quota Viewer](https://cloud.google.com/iam/docs/roles-permissions/servicemanagement#servicemanagement.quotaViewer) (`roles/servicemanagement.quotaViewer`)
- To request quota adjustments:
        [Quota Administrator](https://cloud.google.com/iam/docs/roles-permissions/servicemanagement#servicemanagement.quotaAdmin) (`roles/servicemanagement.quotaAdmin`)

For more information about granting roles, see [Manage access to projects, folders, and organizations](https://cloud.google.com/iam/docs/granting-changing-revoking-access).

These predefined roles contain

        the permissions required to request quota adjustments. To see the exact permissions that are
        required, expand the **Required permissions** section:

The following permissions are required to request quota adjustments:

- To request quota adjustments:
                    ` serviceusage.quotas.update`

You might also be able to get
          these permissions
        with [custom roles](https://cloud.google.com/iam/docs/creating-custom-roles) or
        other [predefined roles](https://cloud.google.com/iam/docs/roles-overview#predefined).

## View quotas in the Google Cloud console

You can view your current quota values in two different areas of the
[Google Cloud console](https://console.cloud.google.com/):

- The [Quotas & System Limits](https://console.cloud.google.com/quotas?project=_) page, which lists
  all quota usage and values for your project.
- The [Google Cloud console API dashboard](https://console.cloud.google.com/apis/dashboard),
  which lists quota information for a particular API, including resource
  usage over time.

### View the quotas for your project

The **IAM & Admin>Quotas & System Limits** page displays a table
with configurable columns. The **Service** and **Quota** columns provide general
information about which quota is being described.
For example, the **Service** might be **Cloud Logging API** and the **Quota**
might be **Log ingestion requests per minute**. The **Quota** field also
describes how the quota is evaluated. Rate quotas are evaluated per minute, per
100 seconds, or per day. Quotas without any of these statements are allocation
quotas.

To view quota usage and values for all resources in your project, follow these
steps:

1. In the Google Cloud console, go to the
  **IAM & Admin>Quotas & System Limits** page:
  [Go to Quotas & System Limits](https://console.cloud.google.com/iam-admin/quotas)
2. To focus on the information that you need, filter and sort the list as
  follows:
  - To filter the list, enter the properties and values in the field. For
    example, to view the BigQuery API quotas, select
    **Service**, and then select **BigQuery API**.
  - To sort the list, click the heading of the column you want to sort by. For
    example, to sort alphabetically by the quota name, click the
    **Quota** column heading.
  By default, the list is sorted to show your most used quotas first, which
  helps you see quotas that are at risk of being exceeded.
3. Optional: To inspect the aggregate quota usage at the folder and
  organization levels, select the organization or folder from the resource
  selector.

You can find additional information about the quota by using the
**Metric**, **Limit name**, and **Monitored resource** columns. These
columns provide the detailed information needed to chart a quota.

For information about your quota usage, view the
**Current usage percentage** and **Current usage** columns.
Current usage is calculated according to the following criteria:

- For per-minute rate quotas:
  - The *average* per minute usage in the past 10 minutes.
- For per-day rate quotas:
  - The *total* usage so far in the current day, according to Pacific
    Standard Time.
- For allocation quotas:
  - The most recent value. For example, this number
    might show the number of load balancers in use by your project.
- For concurrent quotas:
  - The most recent value. For example, this number
    might show the number of in-flight insert_operations for a given service.

You can learn more about quotas for a specific service by reading the
documentation for that service. For example, Compute Engine quota is
documented in [Resource quotas](https://cloud.google.com/compute/quotas).

### View and export quota usage over time

You can view quota usage over time with charts. The Quotas & System Limits page
of the console provides charts for each individual quota or system limit that's
in the Quotas & System Limits table. After you view a chart, you can export it.
To view and export a chart, follow these steps:

1. In the Google Cloud console, go to the
  **IAM & Admin>Quotas & System Limits** page:
  [Go to Quotas & System Limits](https://console.cloud.google.com/iam-admin/quotas)
2. Find the quota or system limit that you're interested in. In the entry
  for this quota or system limit, click
  **Show usage chart**. The chart view opens.
3. In the chart view, set the time period. The default is 7 days. To change
  this, click the time period menu and select your time period.
4. To export the chart, click  **More chart options**, and then select **Download** > **Download PNG**. The chart downloads as a PNG file.

To do more with charts, see
[Set up quota alerts and monitoring](https://cloud.google.com/docs/quotas/set-up-quota-alerts).

### View API-specific quotas

To view detailed quota information for a particular API, including usage
over time, visit the quota page for the API in the Google Cloud console.
Depending on the API, these limits can include *requests per day*,
*requests per minute*, and *requests per minute per user*.
Some APIs set very low limits until you
[enable billing on your project](https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project).

If there is no value for a given quota, the value appears as `Unlimited`.

You can view the current limits for a particular API in two different areas of
the Google Cloud console:
on the Google Cloud console **Quotas & System Limits** page
or **APIs & Services** page. Use the console view that you prefer:

- To view API-specific quotas from the **Quotas & System Limits** page using
  a filter:
  1. In the Google Cloud console, go to the
    **IAM & Admin>Quotas & System Limits** page:
    [Go to Quotas & System Limits](https://console.cloud.google.com/iam-admin/quotas)
  2. Click **Filter** and select **Service** from
    the menu that appears.
  3. Select or enter the service name that you want to view.
    The page displays quotas and system limit information for the
    specified API. The numbers that appear in the `Value` column are the
    default quota values, unless you made a quota adjustment.
- To view API-specific quotas from the **APIs & Services** page:
  1. Go to the **APIs & Services** page:
    [Go to APIs & Services](https://console.cloud.google.com/apis/dashboard?project=_)
  2. Select your project.
  3. Click the API name for the service you want to view.
  4. Click the **Quotas & System Limits** tab.
    The page displays quotas and system limit information for the
    specified API. The numbers that appear in the `Value` column are the
    default quota values, unless you made a quota adjustment.

To see usage over time, click **Show usage chart**.

### Filter quotas

To filter the list of quotas by specific properties:

1. In the Google Cloud console, go to the
  **IAM & Admin>Quotas & System Limits** page:
  [Go to Quotas & System Limits](https://console.cloud.google.com/iam-admin/quotas)
2. Click **Filter** to
  query your quotas by a specific property name or value.

## Manage your quotas using the console

Depending on your resource usage, you might want to adjust the quota
values of your project up or down. This section describes how to change the provided quota
values. To see the values, in the **Details** column, click **All Quotas**.

### Request a quota adjustment

Cloud Quotas adjustment requests are subject to review. If your quota
adjustment request requires review, you receive an email acknowledging receipt
of your request. If you need further assistance, respond to the email. After
reviewing your request, you receive an email notification indicating whether
your request was approved.

You can request a quota adjustment by using the Google Cloud console, the
Cloud Quotas API, or the Google Cloud CLI. The following instructions show
how to request a new quota value by using the Google Cloud console or by making a
REST request to the Cloud Quotas API.

To request a quota adjustment, follow these steps:

1. In the Google Cloud console, go to the
  **IAM & Admin>Quotas & System Limits** page:
  [Go to Quotas & System Limits](https://console.cloud.google.com/iam-admin/quotas)
      If prompted to select a project, select the project that you want to
      adjust.
2. Find the quota that you want to adjust and open the **Quota changes**
  dialog:
  - **Quotas that aren't in the table:**
    - Search for your quota in the
      **Filter** search box. Don't specify the region or zone (if applicable)
      because quotas that don't have use or adjusted values don't show in the
      table.
    - Find any entry for your quota in the table. This can
      be the default entry or any entry with history regardless of region or
      zone.
    - In the line for the entry, click  **More actions > Configure additional regions/zones**.
    - Select the region
      or zone that you want to adjust. Click **Edit**.
  - **All other quotas:**
    - Search for your quota in the **Filter** search box.
    - In the line for the entry, select the checkbox for your quota.
    - Click **Edit**.
  The **Quota changes** dialog appears.
3. If you see a link to **Apply for higher quota** above the **New value**
  field and you want to increase your quota value beyond the number indicated
  on the screen, follow the link. Fill out the form, submit it, and skip the
  remaining steps here. Otherwise, continue following this guide.
4. In the **New value** field, enter the increased quota value that you
  want. If a **Request description** field appears, enter a description.
  Click **Done**.
  - If you see a checkbox with the text "I understand that this request will
    remove any overrides," your quota value is set below the default.
    Adjusting the quota value to or beyond the default removes the override.
    To proceed, select the checkbox. Learn more about
    [quota overrides](https://cloud.google.com/docs/quotas/view-manage#create_override).
  If a **Next** button appears, click **Next** and fill out your contact
  details in the screen that follows.
5. Click **Submit request**.

If you find that you can't request an adjustment from the console, request the
increase from [Cloud Customer Care](https://cloud.google.com/support).

To learn more about how the quota increase process works, see
[About quota adjustments](https://cloud.google.com/docs/quotas/overview#about_increase_requests).

#### Batching requests for quota adjustments

You can batch requests for quota adjustments by selecting the checkbox for
each quota that you want to include. However, batching requests can increase
the amount of time it takes for Google Cloud to review your request.

To reduce review time, group quota adjustment requests by product and area. For
example, if you want to request adjustments to networking and Compute Engine
VM quotas, create one request for the networking quotas and another request for
the Compute Engine VM quotas.

To request a quota adjustment from the Cloud Quotas API, use the
following code sample. Fill in the editable placeholders with your values. To
learn about the placeholder fields, see the descriptions following the code
sample.

```
POST projects/PROJECT_NUMBER/locations/global/quotaPreferences?quotaPreferenceId=QUOTA_PREFERENCE_ID {
    "service": "SERVICE_ID",
    "quotaId": "QUOTA_ID",
    "quotaConfig": { "preferredValue": "NEW_QUOTA_VALUE" },
    "dimensions": { "DIMENSION_1": "VALUE_1", "DIMENSION_2": "VALUE_2" },
    "justification": "JUSTIFICATION",
    "contactEmail": "EMAIL"
}
```

Replace the following:

- `PROJECT_NUMBER`: Your Google Cloud project
  number. You can find your project number on the
  [Welcome](https://console.cloud.google.com/welcome)
  page of the Google Cloud console or by running the following
  gcloud CLI command:
  ```
  PROJECT=$(gcloud info --format='value(config.project)')
  gcloud projects describe ${PROJECT} --format="value(projectNumber)"
  ```
- `QUOTA_PREFERENCE_ID`: The ID of the quota
  preference you're updating.
- `QUOTA_ID`: The ID of the quota that you're updating.
- `SERVICE_ID`: The ID of the Google Cloud that
  the quota you're adjusting belongs to. This is usually of the form
  `SERVICE_NAME`.googleapis.com. For example, the
  Compute Engine service name is `compute.googleapis.com`.
- `DIMENSION_1`: The type of dimension that you want
  to adjust—for example, `region` or `zone`—. You can include
  multiple dimensions. Separate each dimension by following its value—
  for example, `VALUE_1`—with a comma. To adjust
  all dimensions of the quota, omit this line.
- `VALUE_1`: The value of the preceding dimension. For
  example, if preceding dimension is `region`, enter a region such as
  `us-central1`.
- `JUSTIFICATION`: The reason for this request.
- `EMAIL`: An email address that can be used as a
  contact, in case Google Cloud needs more information to make a decision
  before additional quota can be granted.

#### Example request

The following is an example of a quota value increase request for the
Compute Engine quota `PUS-PER-GPU-FAMILY-per-project-region`. It requests
a quota value of 100 for machines of the GPU family `NVIDIA_H100` that are
in the region `us-central1`.

```
POST projects/123/locations/global/quotaPreferences?quotaPreferenceId=my_quota_preference_ID {
    "service": "compute.googleapis.com",
    "quotaId": "GPUS-PER-GPU-FAMILY-per-project-region",
    "quotaConfig": { "preferredValue": 100 },
    "dimensions": { "region": "us-central1", "gpu_family": "NVIDIA_H100" },
    "justification": "My justification.",
    "contactEmail": "222larabrown@gmail.com"
}
```

### View quota increase requests

You can see pending and past quota increase requests in the
Google Cloud console.

To see pending quota increase requests:

1. Ensure that you have [permission to view quota increase requests.](https://cloud.google.com/docs/quotas/permissions#permissions_increase)
2. In the Google Cloud console, go to the
  **IAM & Admin>Quotas & System Limits** page:
  [Go to Quotas & System Limits](https://console.cloud.google.com/iam-admin/quotas)
3. A  **Pending** icon appears next to the quota values that are pending a
  decision on previously submitted increase requests. Click
   **Pending** to view details of
  the pending requests.

Pending requests are also shown in the **Quota changes** form when a
quota adjustment is about to be submitted.

To view all quota increase requests, which includes pending and past requests:

1. In the Google Cloud console, go to the
  **IAM & Admin>Quotas & System Limits** page:
  [Go to Quotas & System Limits](https://console.cloud.google.com/iam-admin/quotas)
2. Click the **Increase Requests** tab.
3. Click **Filter** to
  query your quota increase requests by a specific property.

When an organization or folder is selected, the page shows all quota increase
requests for all projects within the organization or folder.

### Create a quota override

To restrict usage of a particular resource, create a *quota override* by
changing the quota value to a value less than the default quota value.
Creating a quota override is sometimes referred to as *capping usage*.

To create a quota override, follow the steps to
[update a quota value](#requesting_higher_quota).

Quota overrides are not available to all services. For service-specific
information, check the quota and system limits documentation for your service.

### Reset a quota value

To reset the quota value after an override has been applied, follow these steps:

1. In the Google Cloud console, go to the
  **IAM & Admin>Quotas & System Limits** page:
  [Go to Quotas & System Limits](https://console.cloud.google.com/iam-admin/quotas)
2. Enter text in the **Filter**
  search box to search for your quota. Set **Has override: True** to
  show only quotas that have an override.
3. On the Quotas page,  **Override** appears next to the quota limits that have an override.
  Click **Override** to view
  details of this quota and an option to reset the value.
4. To acknowledge that a reset removes your overrides, click the checkbox
  preceding **Reset value** and then click **Reset value** to reset the quota.

To reset a quota manually, follow the same steps as for
[requesting a higher quota limit](#requesting_higher_quota). Make sure that you
set the **New value** equal to the **Default value** displayed below the quota
name in the **Quota changes** form.

## Manage quotas using the Cloud Quotas API

You can use the Cloud Quotas API to get current quota information and
set quota preferences for Google Cloud APIs and services. For more information,
see the following:

- For an overview, see
  [Cloud Quotas API overview](https://cloud.google.com/docs/quotas/api-overview).
- For instructions on how to set up your development environment, see
  [Set up the Cloud Quotas API](https://cloud.google.com/docs/quotas/development-environment).
- For examples that show how to use the Cloud Quotas API to adjust quotas and
  automate quota adjustments in your Google Cloud projects, folders, or
  organization, see [Implement common use cases](https://cloud.google.com/docs/quotas/implement-common-use-cases).

## Manage quotas using the gcloud CLI

To use the gcloud CLI, make sure you have
[installed](https://cloud.google.com/sdk/docs/install)
and [initialized](https://cloud.google.com/sdk/docs/initializing) the latest version of the
gcloud CLI, including the [beta commands](https://cloud.google.com/sdk/docs/components#alpha_and_beta_components)
component. If you're using Cloud Shell to interact with Google Cloud, the
gcloud CLI is installed for you.

See the following sections for more information:

- For example `gcloud beta quotas info` and `gcloud beta quotas preferences`
  commands, see
  [Use the gcloud CLI to view and manage quotas](https://cloud.google.com/docs/quotas/gcloud-cli-examples).
- For a complete list of `gcloud beta quotas` commands and flags, see the
  [gcloud beta quotas](https://cloud.google.com/sdk/gcloud/reference/beta/quotas)
  section of the Google Cloud CLI reference.
  - [gcloud beta quotas info](https://cloud.google.com/sdk/gcloud/reference/beta/quotas/info)
  - [gcloud beta quotas preferences](https://cloud.google.com/sdk/gcloud/reference/beta/quotas/preferences)

## Request project quota

For more information about requesting additional *project quotas*, refer to the
[Project quota requests](https://support.google.com/cloud/answer/6330231)
support article.

## What's next

- Set up the [quota adjuster](https://cloud.google.com/docs/quotas/quota-adjuster) to monitor and
  submit quota adjustment requests for you.
- Use the [Cloud Quotas API](https://cloud.google.com/docs/quotas/api-overview) to manage your quotas at
  the project level.
- Control access using [IAM](https://cloud.google.com/docs/quotas/permissions) or
  [VPC Service Controls](https://cloud.google.com/docs/quotas/configure-vpc-service-controls).
- Configure your [quota project](https://cloud.google.com/docs/quotas/quota-project).
- [Monitor](https://cloud.google.com/docs/quotas/monitor) and
  [troubleshoot](https://cloud.google.com/docs/quotas/troubleshoot) quotas.

---

# Implement common use casesStay organized with collectionsSave and categorize content based on your preferences.

> Implement common quota use-cases. Use API to automate quota adjustments.

# Implement common use casesStay organized with collectionsSave and categorize content based on your preferences.

This document describes how to implement common use cases using the
Cloud Quotas API.
This API lets you programmatically adjust
[quotas](https://cloud.google.com/docs/quotas/overview)
and automate
[quota adjustments](https://cloud.google.com/docs/quotas/overview#about_increase_requests)
in your Google Cloud projects, folders, or organization.

To learn more, see the Cloud Quotas API
[overview](https://cloud.google.com/docs/quotas/api-overview) and
[reference](https://cloud.google.com/docs/quotas/reference/rest).

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

## Track usage and request an increase when usage is over 80%

This example tracks quota usage with Cloud Monitoring and then requests
an increase when the usage is over 80%.

1. Call the `QuotaInfo` resource for your service to determine the current
  `quotaValue`. The service in this example is `compute.googleapis.com`:
  ```
  GET projects/PROJECT_NUMBER/locations/global/services/compute.googleapis.com/quotaInfos
  ```
  Replace `PROJECT_NUMBER` with the project number for
  your project.
2. To find the CPUs per project and the applicable locations, look through the
  `QuotaInfo` response for the `CPUS-per-project-region` quota ID. The
  `quotaValue` is 20.
  ```
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
                "dimensions": [],
                "details": {
                    "quotaValue": 20,
                    "resetValue": 20
                },
                "applicableLocations": [
                    "us-central1",
                    "us-central2",
                    "us-west1",
                    "us-east1"
                ]
            }
        ]
    },
    ...
  ]
  ```
3. Call the Cloud Monitoring API to find the quota usage. In the following
  example, the region `us-central1` has been specified. Supported quota
  metrics are listed under
  [serviceruntime](https://cloud.google.com/monitoring/api/metrics_gcp_p_z#gcp-serviceruntime).
  ```
  {
  "name": "projects/PROJECT_NUMBER"
    "filter": "metric.type=\"serviceruntime.googleapis.com/quota/allocation/usage\" AND
    metric.labels.quota_metric=\"compute.googleapis.com/cpus\" AND resource.type=\"consumer_quota\" AND
    resource.label.location=\"us-central1\" ",
    "interval": {
    "startTime": "2023-11-10T18:18:18.0000Z",
    "endTime": "2023-11-17T18:18:18.0000Z"
    },
    "aggregation": {
    "alignmentPeriod": "604800s", // 7 days
    "perSeriesAligner": "ALIGN_MAX",
    "crossSeriesReducer": "REDUCE_MAX"
    }
  }
  ```
4. To determine your usage, handle the response from the Cloud Monitoring API.
  Compare the value from Cloud Monitoring to the `quotaValue` in earlier
  steps to determine the usage.
  In the following example response the usage value in Cloud Monitoring is 19
  in the `us-central1` region. The `quotaValue` for all regions is 20. The usage
  is greater than 80% of the quota, and a quota preference update can be
  initiated.
  ```
  time_series {
  metric {
  labels {
  key: "quota_metric"
  value: "compute.googleapis.com/cpus"
  }
    type: "serviceruntime.googleapis.com/quota/allocation/usage"
  }
  resource {
    type: "consumer_quota"
    labels {
      key: "project_id"
      value: "PROJECT_ID"
    }
    labels {
      key: "location"
      value: "us-central1"
    }
  }
  metric_kind: GAUGE
  value_type: INT64
  points {
    interval {
      start_time {
        seconds: "2023-11-10T18:18:18.0000Z"
      }
      end_time {
        seconds: "2023-11-17T18:18:18.0000Z"
      }
    }
    value {
      int64_value: 19
    }
  }
  }
  ```
5. To avoid duplicated quota preferences, call `ListQuotaPreferences` first to
  check if there are any pending requests. The `reconciling=true` flag calls
  pending requests.
  ```
  GET projects/PROJECT_NUMBER/locations/global/quotaPreferences?filter=service=%22compute.googleapis.com%22%20AND%20quotaId=%22CPUS-per-project-region%22%20AND%20reconciling=true
  ```
  Replace `PROJECT_NUMBER` with the project number for your
  project.
6. Call `UpdateQuotaPreference` to increase the quota value for region
  `us-central1`. In the following example, a new preferred value of 100 has been
  specified.
  The field `allow_missing` is set to `true`. This tells the system to create a
  `QuotaPreference` resource where none exists with the provided name.
  ```
  PATCH projects/PROJECT_NUMBER/locations/global/quotaPreferences/compute_googleapis_com-cpus-us-central1?allowMissing=true {
  "service": "compute.googleapis.com",
  "quotaId": "CPUS-per-project-region",
  "quotaConfig": { "preferredValue": 100 },
  "dimensions": { "region": "us-central1" },
  "justification": "JUSTIFICATION",
  "contactEmail": "EMAIL"
  }
  ```
  Replace the following:
  - `PROJECT_NUMBER`: The unique identifier for your
    project.
  - `JUSTIFICATION`: An optional string that explains
    your request.
  - `EMAIL`: An email address that can be used as a
    contact, in case Google Cloud needs more information before additional quota
    can be granted.
7. Call `GetQuotaPreference` to check the status of the quota preference change:
  ```
  GET projects/PROJECT_NUMBER/locations/global/quotaPreferences/compute_googleapis_com-cpus-us-central1
  ```
  Replace `PROJECT_NUMBER` with the project number for your
  project.
  While Google Cloud evaluates the requested quota value, the reconciling status
  of your quota is set to `true`.
  Sometimes Google Cloud approves part of your increase request instead of
  approving the full increase. If the request is partially approved, the quota
  preference includes a `stateDetail` field. The `stateDetail` field describes
  the partially approved state. The `grantedValue` field shows the adjustment
  that was made to partially fulfill your request.
  To see if the granted value is the final value approved, look at the
  `reconciling` field. If your request is still undergoing evaluation, the
  `reconciling` field is set to `true`. If the `reconciling` field is set to
  `false` or is omitted, the granted value is the final value approved.
  In the following example, the requested quota value is 100 and the
  `reconciling` field indicates that the request is undergoing review.
  ```
  "name": "projects/PROJECT_NUMBER/locations/global/quotaPreferences/compute_googleapis_com-cpus-us-central1",
  "service": "compute.googleapis.com",
  "quotaId": "CPUS-per-project-region",
  "quotaConfig": {
    "preferredValue": 100,
    "grantedValue": 50,
    "traceId": "123acd-345df23",
    "requestOrigin": "ORIGIN_UNSPECIFIED"
  },
  "dimensions": { "region": "us-central1" },
  "reconciling": true,
  "createTime": "2023-01-15T01:30:15.01Z",
  "updateTime": "2023-01-16T02:35:16.01Z"
  ```
  After the quota preference has been processed, the `reconciling`
  field is set to `false`. The `grantedValue` is the same as
  the `preferredValue`. The preferred quota is fully granted.
  When Google Cloud denies or partially approves a customer request, the
  granted quota value can still be less than the preferred value.

## Decrease a quota

The following example decreases the number of TPUs to 10 in each
region.

1. Get the quota ID and the current quota value with a `ListQuotaInfos` call:
  ```
  GET projects/PROJECT_NUMBER/locations/global/services/compute.googleapis.com/quotaInfos
  ```
  Replace `PROJECT_NUMBER` with the project number for
  your project.
2. Look through the response fields to find a `QuotaInfo` entry for
  `V2-TPUS-per-project-region`.
  ```
  "quotaInfos": [
    ...
    {
        "name": "projects/PROJECT_NUMBER/locations/global/services/compute.googleapis.com/quotaInfos/V2-TPUS-per-project-region",
        "quotaId": "V2-TPUS-per-project-region",
        "metric": "compute.googleapis.com/Tpus",
        "containerType": "PROJECT",
        "dimensions": [
            "region"
        ],
        "dimensionsInfo": [
            {
                "dimensions": [],
                "details": {
                    "quotaValue": 20,
                    "resetValue": 20
                },
                "applicableLocations": [
                    "us-central1",
                    "us-central2",
                    "us-west1",
                    "us-east1"
                ]
            }
        ]
    },
    ...
  ]
  ```
  In this response the quota ID is `V2-TPUS-per-project-region`, and the current
  `quotaValue` is 20.
3. Reduce TPU quota in each region to 10 with a `CreateQuotaPreferenceRequest`.
  Set the `preferredValue` to 10.
  ```
  POST projects/PROJECT_NUMBER/locations/global/quotaPreferences?quotaPreferenceId=compute_googleapis_com-Tpu-all-regions {
    "quotaConfig": {
        "preferredValue": 10
    },
    "dimensions": [],
    "service": "compute.googleapis.com",
    "quotaId": "V2-TPUS-per-project-region",
    "justification": "JUSTIFICATION",
    "contactEmail": "EMAIL"
  }
  ```
  Replace the following:
  - `PROJECT_NUMBER`: The unique identifier for your
    project.
  - `JUSTIFICATION`: An optional string that explains
    your request.
  - `EMAIL`: An email address that can be used as a
    contact, in case Google Cloud needs more information before additional quota
    can be granted.
4. Confirm the new quota value with a `GetQuotaInfo` call that defines the quota
  ID as `V2-TPUS-per-project-region`.
  ```
  GET projects/PROJECT_NUMBER/locations/global/services/compute.googleapis.com/quotaInfos/V2-TPUS-per-project-region
  ```
  Replace `PROJECT_NUMBER` with the project number for
  your project.
  The following is an example response, the `value` is 10 and it is applicable
  in all regions.
  ```
  "name": "projects/PROJECT_NUMBER/locations/global/services/compute.googleapis.com/quotaInfos/V2-TPUS-per-project-region",
  "quotaId": "V2-TPUS-per-project-region",
  "metric": "compute.googleapis.com/v2_tpus",
  "containerType": "PROJECT",
  "dimensions": [
    "region"
  ],
  "dimensionsInfo": [
    {
        "dimensions": [],
        "details": {
            "value": 10,
        },
        "applicableLocations": [
            "us-central1",
            "us-central2",
            "us-west1",
            "us-east1"
        ]
    }
  ]
  ```

## Copy quota preferences to another project

The following example copies all quota preferences from
one project to another. It's written in Java, but you can use any programming
language.

1. Call `ListQuotaPreferences` on the source project with no filter:
  ```
  GET projects/PROJECT_NUMBER1/locations/global/quotaPreferences
  ```
  PROJECT_NUMBER1 is the project number for the source project. The
  response contains all quota preferences for the source project.
2. For each quota preference in the response, call `UpdateQuotaPreference` and
  define the following fields:
  - `name` - The updated name field is taken from the response, and the source
    project number (PROJECT_NUMBER1) is replaced with the destination
    project number (PROJECT_NUMBER2).
  - `service`, `quotaId`, `preferredValue`, `dimensions` - These fields can be
    taken directly from the response as is.
  ```
  for (QuotaPreference srcPreference : listResponse.getQuotaPreferences()) {
    QuotaPreference.Builder targetPreference = QuotaPreference.newBuilder()
        .setName(srcPreference.getName().replace("PROJECT_NUMBER1", "PROJECT_NUMBER2"))
        .setService(srcPreference.getService())
        .setQuotaId(srcPreference.getQuotaId())
        .setJustification(srcPreference.getJustification())
        .setContactEmail(srcPreference.getContactEmail())
        .setQuotaConfig(
            QuotaConfig.newBuilder().setPreferredValue(srcPreference.getQuotaConfig().getPreferredValue()))
        .putAllDimensions(srcPreference.getDimensionsMap());
    UpdateQuotaPreferenceRequest updateRequest = UpdateQuotaPreferenceRequest.newBuilder()
        .setQuotaPreference(targetPreference)
        .setAllowMissing(true)
        .build();
    cloudQuotas.updateQuotaPreference(updateRequest);
  }
  ```
3. Call `ListQuotaPreferences` to verify the status of the quota preferences for
  the destination project:
  ```
  GET projects/PROJECT_NUMBER2/locations/global/quotaPreferences
  ```
  Replace `PROJECT_NUMBER2` with the project number for
  your destination project.

## List pending quota requests

To list all pending quota preference requests for a project, call
`ListQuotaPreferences` with the filter `reconciling=true`.

```
GET projects/PROJECT_NUMBER/locations/global/quotaPreferences?reconciling=true
```

Replace `PROJECT_NUMBER` with the project number for your
project.

The response for this request returns the latest pending
quota preference. Because Cloud Quotas API is a declarative API, the
latest quota preference is what the system tries to fulfill.

An example response looks similar to the following:

```
"quotaPreferences": [
    {
      "name": "projects/PROJECT_NUMBER/locations/global/quotaPreferences/compute_googleapis_com-cpus-us-central1",
      "service": "compute.googleapis.com",
      "quotaId": "CPUS-per-project-region",
      "quotaConfig": {
        "preferredValue": 100,
        "grantedValue": 30,
        "traceId": "123acd-345df23",
        "requestOrigin": "ORIGIN_UNSPECIFIED"
      },
      "dimensions": {
        "region": "us-central1"
      },
      "reconciling": true,
      "createTime": "2023-01-15T01:30:15.01Z",
      "updateTime": "2023-01-16T02:35:16.01Z"
    },
    {
      "name": "projects/PROJECT_NUMBER/locations/global/quotaPreferences/compute_googleapis_com-cpus-cross-regions",
      "service": "compute.googleapis.com",
      "quotaId": "CPUS-per-project-region",
      "quotaConfig": {
        "preferredValue": 10,
        "grantedValue": 5,
        "traceId": "456asd-678df43",
        "requestOrigin": "ORIGIN_UNSPECIFIED"
      },
      "reconciling": true,
      "createTime": "2023-01-15T01:35:15.01Z",
      "updateTime": "2023-01-15T01:35:15.01Z"
    }
  ]
```

## Request group quota increases

To request increases for a group of quotas in a new project, store the preferred
quotas for the new project in a CSV file with the following values:
service name, quota ID, preferred quota value, dimensions.

For each row in the CSV file, read the contents into the fields `serviceName`,
`quotaId`, `preferredValue`, and `dimensionMap`.

```
CreateQuotaPreferenceRequest request =
  CreateQuotaPreferenceRequest.newBuilder()
     .setParent("projects/PROJECT_NUMBER/locations/global")
     .setQuotaPreferenceId(buildYourOwnQuotaPreferenceId(serviceName, quotaId, dimensionMap))
     .setQuotaPreference(
        QuotaPreference.newBuilder()
            .setService(serviceName)
            .setQuotaId(quotaId)
            .setJustification(justification)
            .setContactEmail(contactEmail)
            .setQuotaConfig(QuotaConfig.newBuilder().setPreferredValue(preferredValue))
            .putAllDimensions(dimensionMap))
  .build();
cloudQuotas.createQuotaPreference(request);
```

Replace `PROJECT_NUMBER` with the project number for your
project.

Because the target project is new, it is safe to call the
`CreateQuotaPreference` method as you read and assign the fields. Alternatively,
you can call the `UpdateQuotaPreference` method with `allow_missing` set to `true`.

The method `buildYourOwnQuotaPreferenceId` builds a quota preference ID
from service name, quota ID, and a map of dimensions according to your naming
scheme. Alternatively, you can choose not to set quota preference ID. A quota
preference ID is generated for you.

## Request adjustments on quotas that have no usage

Quota adjustment requests follow the same process regardless of whether or not
the quota you're adjusting has usage. To learn how to request a quota
adjustment, see
[Request a quota adjustment](https://cloud.google.com/docs/quotas/view-manage#requesting_higher_quota).

## Get quota info for a service specific dimension

GPU family is a service specific dimension. The following example request uses the
`GPUS-PER-GPU-FAMILY-per-project-region` quota ID to get the `QuotaInfo` resource.

```
GET projects/PROJECT_NUMBER/locations/global/services/compute.googleapis.com/quotaInfos/GPUS-PER-GPU-FAMILY-per-project-region
```

Replace `PROJECT_NUMBER` with the project number for your
project.

This is an example response. For each unique `gpu_family` key, the `quotaValue`
and `applicableLocations` is different:

```
"name": "projects/PROJECT_NUMBER/locations/global/services/compute.googleapis.com/quotaInfos/GpusPerProjectPerRegion",
"quotatName": "CPUS-per-project-region",
"metric": "compute.googleapis.com/gpus_per_gpu_family",
"isPrecise": true,
"quotaDisplayName": "GPUs per GPU family",
"metricDisplayName": "GPUs",
"dimensions": [
    "region",
    "gpu_family"
],
"dimensionsInfo": [
    {
        "dimensions": {
            "region": "us-central1",
            "gpu_family": "NVIDIA_H200"
        },
        "details": {
            "quotaValue": 30,
            "resetValue": 30,
        },
        "applicableLocations": [
            "us-central1"
        ]
    },
    {
        "dimensions": {
            "region": "us-central1"
            }
        "details": {
            "quotaValue": 100,
            "resetValue": 100,
        },
        "applicableLocations": [
            "us-central1"
        ]
    },
    {
        "dimensions": {
            "gpu_familly": "NVIDIA_H100"
            }
        "details": {
            "quotaValue": 10,
        },
        "applicableLocations": [
            "us-central2",
            "us-west1",
            "us-east1"
        ]
    }
      {
        "dimensions": [],
        "details": {
            "quotaValue": 50,
            "resetValue": 50,
        },
        "applicableLocations": [
            "us-central1",
            "us-central2",
            "us-west1",
            "us-east1"
        ]
    }
]
```

## Create a quota preference for a service specific dimension

The following example demonstrates how to create a quota for a given region and
GPU family with a preferred value of 100. The target location is specified in the
map of dimensions with the key `region`, and the target GPU family with the key
`gpu_family`.

The following `CreateQuotaPreference` example specifies a GPU family of
`NVIDIA_H100` and a region of `us-central1`.

```
POST projects/PROJECT_NUMBER/locations/global/quotaPreferences?quotaPreferenceId=compute_googleapis_com-gpus-us-central1-NVIDIA_H100 {
    "service": "compute.googleapis.com",
    "quotaId": "GPUS-PER-GPU-FAMILY-per-project-region",
    "quotaConfig": {
        "preferredValue": 100
    },
    "dimensions": {"region": "us-central1", "gpu_family": "NVIDIA_H100"},
    "justification": "JUSTIFICATION",
    "contactEmail": ""EMAIL"
}
```

Replace the following:

- `PROJECT_NUMBER`: The unique identifier for your
  project.
- `JUSTIFICATION`: An optional string that explains your
  request.
- `EMAIL`: An email address that can be used as a
  contact, in case Google Cloud needs more information before additional
  quota can be granted.

## Update a quota preference for a service specific dimension

The following sample code gets the current value for the dimension
`{"region" : "us-central1"; gpu_family:"NVIDIA_H100"},`
and then sets the preferred value to double the value. It's written in Java, but you
can use any programming language.

```
// Get the current quota value for the target dimensions
Map<String, String> targetDimensions = Maps.createHashMap("region", "us-central1", "gpu_family", "NVIDIA_H100");
long currentQuotaValue = 0;
QuotaInfo quotaInfo = cloudQuotas.GetQuotaInfo(
    "projects/PROJECT_NUMBER/locations/global/services/" + serviceName + "quotaInfos/" + quotaId;
for (dimensionsInfo : quotaInfo.getDimensionsInfoList()) {
    If (targetDimensions.entrySet().containsAll(dimensionsInfo.getDimensionsMap().entrySet()) {
       currentQuotaValue = dimensionsInfo.getDetails().getValue();
       break;
    })
}

// Set the preferred quota value to double the current value for the target dimensions
QuotaPreference.Builder targetPreference = QuotaPreference.newBuilder()
        .setName(buildYourOwnQuotaPreferenceId(serviceName, quotaId, targetDimensions))
        .setService(serviceName)
        .setQuotaId(quotaId)
        .setJustification(justification)
        .setContactEmail(contactEmail)
        .setQuotaConfig(QuotaConfig.newBuilder().setPreferredValue(currentQuotaValue * 2))
        .putAllDimensions(targetDimensions));
UpdateQuotaPreferenceRequest updateRequest = UpdateQuotaPreferenceRequest.newBuilder()
        .setQuotaPreference(targetPreference)
        .setAllowMissing(true)
        .build();
 cloudQuotas.updateQuotaPreference(updateRequest);
```

Replace `PROJECT_NUMBER` with the unique identifier for
your project.

## What's next

- About the [Cloud Quotas API](https://cloud.google.com/docs/quotas/api-overview)
- Cloud Quotas API [reference](https://cloud.google.com/docs/quotas/reference/rest)
- Understand [quotas](https://cloud.google.com/docs/quotas/overview)

   Was this helpful?

---

# Known issuesStay organized with collectionsSave and categorize content based on your preferences.

> Known issues for Cloud Quotas

# Known issuesStay organized with collectionsSave and categorize content based on your preferences.

The following are known issues within Cloud Quotas.

## Quota values during rollouts

Google Cloud sometimes increases the default quota values for resources and
APIs. These changes take place gradually, which means that during the rollout,
the quota value that appears in the Google Cloud console or Cloud Quotas API
won't reflect the new, increased quota value until the rollout completes.

If a quota rollout is in progress, an informational message appears at the top
of the Cloud Quotas page and the rolling update indicator appears
next to the quota values impacted by ongoing rollouts.
For details, see
[View ongoing rollouts](https://cloud.google.com/docs/quotas/view-ongoing-rollouts).

For troubleshooting steps, see
[Exceeding quota values during a service rollout](https://cloud.google.com/docs/quotas/troubleshoot#exceeding_quota_values_during_a_service_rollout).

## Quota preferencecontactEmailfield is required

To update the `QuotaPreference` value through the Cloud Quotas API,
the `contactEmail` field is required. This email address cannot be a group
email.

For examples of using `QuotaPreference` in the API, see
[Implement common use cases](https://cloud.google.com/docs/quotas/implement-common-use-cases).

## Cloud Quotas limitations in the Google Cloud console

The following limitations apply when you use Cloud Quotas in the
Google Cloud console.

- **Per-user quota usage doesn't appear:** The Google Cloud console doesn't display
  per-user quota usage.
