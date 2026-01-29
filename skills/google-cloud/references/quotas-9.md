# Troubleshoot quota errorsStay organized with collectionsSave and categorize content based on your preferences. and more

# Troubleshoot quota errorsStay organized with collectionsSave and categorize content based on your preferences.

> If a project exceeds a quota value, it returns an error code.

# Troubleshoot quota errorsStay organized with collectionsSave and categorize content based on your preferences.

You might receive quota errors for a number of reasons, such as exceeding quota
values or not setting the quota on a project correctly. If you want to be alerted
when errors happen, you can create custom alerts for specific
quota errors, as described in
[Set up quota alerts](https://cloud.google.com/docs/quotas/set-up-quota-alerts).

## Exceeding rate quotas

Rate quotas reset after a predefined time interval that is specific to each
service. For more information, see the quotas documentation for the specific
service.

## Exceeding quota values

If your project exceeds its maximum quota value while using a service, Google Cloud
returns an error based on how you accessed the service:

- If you exceed a quota value with an API request, Google Cloud returns an HTTP
  `413 REQUEST ENTITY TOO LARGE` status code.
  Note that when using the BigQuery legacy streaming API in a production
  environment, you may receive a `413 REQUEST ENTITY TOO LARGE` status code
  if your HTTP requests are larger than 10 MB. You may also receive this error
  if you exceed 300 MB per second. For more information see
  [Streaming inserts.](https://cloud.google.com/bigquery/quotas#streaming_inserts)
- If you exceeded a quota value with an HTTP/REST request, Google Cloud returns an
  HTTP `429 TOO MANY REQUESTS` status code.
- If you exceed a quota for Compute Engine, Google Cloud typically returns an
  HTTP `403 QUOTA_EXCEEDED` status code, whether it was from API, HTTP/REST,
  or gRPC. If the quota is a rate quota, then `403 RATE_LIMIT_EXCEEDED` is returned.
- If you exceeded a quota value using [gRPC](https://grpc.io), Google Cloud returns a `ResourceExhausted`
  error. How this error appears to you depends on the service.
- If you exceeded a quota value using a Google Cloud CLI command, the
  gcloud CLI outputs a quota-exceeded error message and returns
  with the exit code `1`.
- If you received a `QUOTA_EXCEEDED` message during a service rollout,
  see the following section.

## Exceeding quota values during a service rollout

Google Cloud sometimes changes the default quota values for resources
and APIs. These changes take place gradually, which means that during the
rollout of a new default quota, the quota value that appears in the Google Cloud console
might not reflect the new quota value that is available to you.

If a quota rollout is in progress, you may receive an error message that states
`The future limit is the new default quota that will be available after a
service rollout completes.` If you see this error message, the cited quota value
and future value are correct, even if what appears in the Google Cloud console
is different.

- For additional information, [view the audit logs](https://cloud.google.com/logging/docs/audit#view-logs)
  and look for a `QUOTA_EXCEEDED` message.
  ```
  "status": {
        ...
        "message": "QUOTA_EXCEEDED",
        "details": [
          {
            ...
            "value": {
              "quotaExceeded": {
                ...
                "futureLimit": FUTUREVALUE
              }
            }
          }
        ]
      },
  ```
- To view charts that show current and peak usage,
  in the Google Cloud console, go to the
  [IAM & Admin>Quotas & System Limits](https://console.cloud.google.com/quotas?project=_)
  page and then click **Monitoring**.
  You might need to go to the end of the table.
- If you need more quota, you can
  [request a quota adjustment](https://cloud.google.com/docs/quotas/help/request_increase).

## Exceeding project quota

For more information about requesting additional *project quotas*, refer to the
[Project quota requests](https://support.google.com/cloud/answer/6330231)
support article.

## API error messages

If your quota project (also called a billing project) isn't set correctly, API
requests might return error messages that are similar to the following:

- `User credentials not supported by this API`
- `API not enabled in the project`
- `No quota project set`

These and other errors can often be fixed by setting the quota project.
For more information, see [Quota project overview](https://cloud.google.com/docs/quotas/quota-project).

## Google Cloud CLI errors

This section describes common issues encountered when getting started with the
Google Cloud CLI (gcloud CLI).

### Install and initialize

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

### Set your quota project

If you haven't set your quota project, gcloud CLI commands might
return an error like the following:

```
PERMISSION_DENIED: Your application is authenticating by using local Application Default Credentials.
The cloudquotas.googleapis.com API requires a quota project, which is not set by default.
```

To resolve this issue, add the `--billing-project` flag on your
gcloud CLI command to explicitly set the quota project, or rerun
`gcloud config set billing/quota_project CURRENT_PROJECT` to set the quota project
as the current project.

For more information, see the following:

- [Set the quota project programmatically](https://cloud.google.com/docs/quotas/set-quota-project#set-project-programmatically).
- [Set the billing project](https://cloud.google.com/sdk/gcloud/reference#--billing-project)
  through the gcloud CLI.

### Update gcloud CLI components

If you receive an error that the quotas command contains an `Invalid choice`,
you might have an older version of the gcloud CLI installed.
Update the gcloud CLI components with the following command:

```
gcloud components update
```

For more details about `gcloud beta quotas` commands and flags, see the
[gcloud beta quotas](https://cloud.google.com/sdk/gcloud/reference/beta/quotas)
section of the Google Cloud CLI reference.

   Was this helpful?

---

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

    Was this helpful?

---

# View ongoing rolloutsStay organized with collectionsSave and categorize content based on your preferences.

> View ongoing rollouts: see what new quota value rollouts are in progress

# View ongoing rolloutsStay organized with collectionsSave and categorize content based on your preferences.

Cloud Quotas lets you view quota value rollouts that are in progress.
This section explains how to view these rollouts from the Google Cloud console
and the Cloud Quotas API.

## Understand ongoing rollouts

When another Google Cloud service increases the default quota values for
resources and APIs, these changes take place gradually. This might result in
ongoing rollouts across different regions or resources. During the rollout,
the quota value that appears in the Google Cloud console or Cloud Quotas API
won't reflect the new, increased quota value until the rollout completes.

## View ongoing rollouts from the console

If there are ongoing quota rollouts in progress, an informational message
appears at the top of the Cloud Quotas page in the
console. The message appears similar to the following text,
which also contains a link. Click **quotas** to filter so that only quotas with
ongoing rollouts appear:

```
Values for quotas are being updated. This may take 2-3 weeks to complete.
```

The update rolling update
indicator appears next to the quota values impacted by ongoing rollouts.

If you don't see the update
rolling update indicator, follow these steps:

1. In the Google Cloud console, go to the
  **IAM & Admin>Quotas & System Limits** page:
  [Go to Quotas & System Limits](https://console.cloud.google.com/iam-admin/quotas)
2. Click the link to **quotas** in the informational message. This turns on the
  filter: **Has ongoing rollout: True**.
3. The table updates to show a
  update
  rolling update indicator next to quota values with ongoing rollouts.

The rolling update indicator also appears in the **Edit Quotas** and
monitoring **Quota usage chart**
panels to help you identify quotas with in progress rollouts.

## View ongoing rollouts from the Cloud Quotas API

You can also view ongoing rollouts using the Cloud Quotas API.
 For more information, see instructions on how to
 [set up the Cloud Quotas API](https://cloud.google.com/docs/quotas/development-environment)
 and
 [implement common use cases](https://cloud.google.com/docs/quotas/implement-common-use-cases).

The Cloud Quotas API resource model uses the `QuotaInfo` and
`QuotaPreference` resources to indicate ongoing rollouts:

- The `QuotaInfo` resource returns the previous quota value during ongoing rollouts.
  For quotas experiencing an ongoing rollout, a `rollout_info` field appears
  in the response under `QuotaDetails`. This field indicates that there is
  both an ongoing rollout and an increase in the quota value for the
  dimensions specified in each `dimensionsInfo` resource.
- The `QuotaPreference` resource returns the previous quota value during ongoing
  rollouts.

During ongoing rollouts, the following Cloud Quota APIs return the previous quota
value:

- [GetQuotaInfo](https://cloud.google.com/docs/quotas/reference/rest/v1/projects.locations.services.quotaInfos/get)
- [ListQuotaInfo](https://cloud.google.com/docs/quotas/reference/rest/v1/projects.locations.services.quotaInfos/list)
- [CreateQuotaPreference](https://cloud.google.com/docs/quotas/reference/rest/v1/projects.locations.quotaPreferences/create)
- [UpdateQuotaPreference](https://cloud.google.com/docs/quotas/reference/rest/v1/projects.locations.quotaPreferences/patch)

### Before you use the Cloud Quotas API

The following sections assume that you are familiar with the
Cloud Quotas API. Before you use the Cloud Quotas API, make sure that
you set up your development environment and are comfortable with the commands
to make GET requests for quota information:

- For an overview, see
  [Cloud Quotas API overview](https://cloud.google.com/docs/quotas/api-overview).
- For instructions on how to set up your development environment, see
  instructions on how to [set up the Cloud Quotas API](https://cloud.google.com/docs/quotas/development-environment).
- To see an example API request and response, see the example that shows how to
  [get quota info for a service specific dimension](https://cloud.google.com/docs/quotas/implement-common-use-cases#get_quota_info_for_a_service_specific_dimension).

### Example API response during a ongoing rollout

The following example shows the results of a regional quota supported in four
regions: us-central1, us-central2, us-west1, us-east1. Its default value is 200
in us-central1 and 100 in all other regions. This regional quota also has an
additional quota override of 300 in us-central2.

Assume that the service producer updates the default value to be `220` in
us-central1 and us-central2. The example that follows shows a QuotaInfo response
where the service config rollout is ongoing for us-central1 and us-central2:

- For each location, the `details` field displays the quota value before the
  rollout completes.
- For us-central1, the quota value is as `200` and the `rolloutInfo`
  field indicates that an ongoing rollout is in progress. The quota value
  changes to 220 only after the rollout completes.
- For us-central2, the quota value is `300` due to the quota override.
  The `rolloutInfo` field does not appear because the quota value remains
  unchanged after the rollout completes.
- For both us-west1 and us-east1, the value defaults to `100`.

```
"name": "projects/PROJECT_NUMBER/locations/global/services/compute.googleapis.com/quotaInfos/GPUS-PER-GPU-FAMILY-per-project-region",
"quotatId": "GPUS-PER-GPU-FAMILY-per-project-region",
"metric": "compute.googleapis.com/gpus_per_gpu_family",
"service": "compute.googleapis.com",
"isPrecise": true,
"containerType": "PROJECT",
"dimensions": [
  "gpu_family",
  "region"
],
"quotaDisplayName": "GPUs per GPU family",
"metricDisplayName": "GPUs",
"dimensionsInfos": [
 {
        "dimensions": { "region" : "us-central1" } ,
        "details": {
            "value": 200,
            "rolloutInfo": {
              "ongoingRollout": true
            }
        },
        "applicableLocations":  [ "us-central1" ] ,
},
 {
        "dimensions": { "region" : "us-central2" } ,
        "details": {
            "value": 300,
        },
        "applicableLocations":  [ "us-central2" ]
},
{
        "dimensions": {},
        "details": {
            "value": 100,
        },
         "applicableLocations": [ "us-west1", "us-east1" ]
}]
```

   Was this helpful?
