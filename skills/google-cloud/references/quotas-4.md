# Set up quota alerts and monitoringStay organized with collectionsSave and categorize content based on your preferences. and more

# Set up quota alerts and monitoringStay organized with collectionsSave and categorize content based on your preferences.

> Set up quota alerts and monitor quota usage

# Set up quota alerts and monitoringStay organized with collectionsSave and categorize content based on your preferences.

You can set up usage alerts and monitoring for your quotas. The
Cloud Quotas dashboard is integrated with
[Cloud Monitoring](https://cloud.google.com/monitoring/docs/monitoring-overview) for convenience.
This document describes how to set up alerts, create charts, and find more
information about using Cloud Monitoring for Cloud Quotas.

## Set up basic quota usage alerts

You can set up quota alerts from the
**IAM & Admin>Quotas & System Limits** page to get
notifications of quota events. For example, you can set up an alert to notify
you when your quota usage reaches a percentage of the maximum value. This
feature is only supported for project-level quotas.

To set up an alert for a specific quota or system limit, do the following:

1. Make sure that you have
  [permissions to create alerts](https://cloud.google.com/docs/quotas/permissions#permissions_create_alert)
2. In the Google Cloud console, go to the
  **IAM & Admin>Quotas & System Limits** page:
  [Go to Quotas & System Limits](https://console.cloud.google.com/iam-admin/quotas)
3. In the right-most column of the table, click  **More
  actions**, and then select **Create usage alert**. The **Alert policy
  templates** pane opens.
4. Under **Configure notifications**, select your notification channel. The
  notification channel is how you receive the alert—for example email,
  SMS, or Pub/Sub.
5. Click **Create**.

## Create charts

The Cloud Monitoring metrics explorer lets you create charts to view metrics.
You can use it to view metrics related to Cloud Quotas.

To view the metrics for a monitored resource by using the
Metrics Explorer, do the following:

1. In the Google Cloud console, go to the
      **Metrics explorer** page:
  [Go toMetrics explorer](https://console.cloud.google.com/monitoring/metrics-explorer)
  If you use the search bar to find this page, then select the result whose subheading is
  **Monitoring**.
2. In the toolbar of the Google Cloud console, select your Google Cloud project.
        For [App Hub](https://cloud.google.com/app-hub/docs/overview) configurations, select the
        App Hub host project or the app-enabled folder's management project.
3. In the **Metric** element, expand the **Select a metric** menu,
      enter `quota usage`
      in the filter bar, and then use the submenus to select a specific resource type and metric:
  1. In the **Active resources** menu, select **Consumer Quota**.
  2. In the **Active metric categories** menu, select **Quota**.
  3. In the **Active metrics** menu, select a metric from the list. To display both active and inactive
    metrics, click **Active** to clear the filter in the **Select a metric**
    menu.
  4. Click **Apply**.
4. To add filters, which remove time series from the query results, use the
        [Filterelement](https://cloud.google.com/monitoring/charts/metrics-selector#filter-option).
5. To combine time series, use the menus on the
        [Aggregationelement](https://cloud.google.com/monitoring/charts/metrics-selector#select_display).
        For example, to display the CPU utilization for your VMs, based on their zone, set the
        first menu to **Mean** and the second menu to **zone**.
  All time series are displayed when the first menu of the **Aggregation** element is set
        to **Unaggregated**. The default settings for the **Aggregation** element
        are determined by the metric type you selected.
6. For quota and other metrics that report one sample per day, do the following:
  1. In the **Display** pane,
              set the **Widget type** to **Stacked bar chart**.
  2. Set the time period to at least one week.

After you've found the quota usage information you want, you can use
Cloud Monitoring to create custom dashboards and alerts. For more
information, see [Do more with Cloud Monitoring](#do-more).

## Check quota metric support

Not all services support quota metrics in Cloud Monitoring. To see
applicable quota metrics for supported services, select **Consumer Quota** as
the resource type when building a chart or creating an alerting policy. Services
that don't support quota metrics aren't displayed.

- Common services that support quota metrics include Compute Engine,
  Dataflow, Spanner, Pub/Sub, Cloud Vision,
  Speech-to-Text, Cloud Monitoring, and Cloud Logging.
- Common services that don't support quota metrics include App Engine and
  Cloud SQL.

## Get metric names

Quotas and system limits have two types of names: display names and metric
names. Display names have spaces and capitalization that make them easier for
humans to read. Metric names are more likely to be lowercase and delimited by
underscores instead of spaces; the exact format depends on the service.

The following instructions show how to get quota and system limit metric names
using either the Google Cloud console or gcloud CLI.

1. In the Google Cloud console, go to the
  **IAM & Admin>Quotas & System Limits** page:
  [Go to Quotas & System Limits](https://console.cloud.google.com/iam-admin/quotas)
  The table on this page displays quotas and system limits that have usage or
  have adjusted values, and a reference entry for other quotas. The reference
  entry has the word "default" in parentheses at the end of the listing in
  the **Name** column. For
  example, `SetIAMPolicy requests per minute per region (default)` is the
  reference entry for the quota
  `SetIamPolicyRequestsPerMinutePerProject`.
2. If you don't see the **Metric** column, take the following steps.
  1. Click  **Column display options**.
  2. Select **Metric**.
  3. Click **OK**. The **Metric** column appears in the table.

The **Metric** column shows the metric names. To filter the results, enter a
property name or value in the field next to
 **Filter**.

To get the metric names for a Google Cloud service by
using the gcloud CLI, run the `quotas info list`
command. To skip lines that don't list metric names, pass the output to a
command such as `grep` with `metric:` as the search term, or use the
gcloud CLI
[--format](https://cloud.google.com/sdk/gcloud/reference#--format) flag:

```
gcloud beta quotas info list --project=PROJECT_ID_OR_NUMBER \
    --service=SERVICE_NAME --format="value(metric)"
```

Replace the following:

- `PROJECT_ID_OR_NUMBER`: the project ID or project
  number.
- `SERVICE_NAME`: the name of the service whose quota
  metrics you want to see—for example, the service name for
  Compute Engine is `compute.googleapis.com`. Include the
  `googleapis.com` portion of the service name.

## Do more with Cloud Monitoring

The [Cloud Monitoring](https://cloud.google.com/monitoring/docs/monitoring-overview) tools let you
monitor quota usage, values, and errors in depth. You can use these metrics to
create custom dashboards and alerts. For example, you can view quota usage over
time or receive an alert when you're approaching your quota value.

Cloud Monitoring supports a wide variety of metrics that you can combine
with filters and aggregations for new and insightful views into your quota
usage. For example, you can combine a metric for allocation quota usage with a
`quota_metric` filter on Cloud TPU names.

Pricing for Cloud Monitoring is described in the
[Google Cloud Observability pricing](https://cloud.google.com/stackdriver/pricing)
document.

The [Cloud Monitoring documentation](https://cloud.google.com/monitoring/docs/monitoring-overview)
is extensive, so here are a few documents to get you started:

- [Building charts](https://cloud.google.com/monitoring/charts):
  A comprehensive guide to creating charts and tables, and adding them to a
  custom dashboard.
- [Introduction to alerting](https://cloud.google.com/monitoring/alerts):
  An overview covering how alerting works and what your options are for creating
  an alert policy.
- [Managing alerting policies](https://cloud.google.com/monitoring/alerts/manage-alerts):
  A guide to various management tasks for your existing alerting policies—for
  example, view a policy, edit a policy, delete a policy, or add a policy to a
  dashboard.
- [Using quota metrics](https://cloud.google.com/monitoring/alerts/using-quota-metrics):
  A detailed document dedicated to quotas use cases, with examples covering topics
  such as how to create alerts for `quota/exceeded` errors.
- [Google Cloud metrics guide](https://cloud.google.com/monitoring/api/metrics_gcp_p_z#gcp-serviceruntime):
  A metrics reference document. The `serviceruntime` section lists the quotas
  metrics used for monitoring.

 Was this helpful?

---

# Cloud Quotas overviewStay organized with collectionsSave and categorize content based on your preferences.

> Use Google Cloud Cloud Quotas quota system to monitor and update your quota usage.

# Cloud Quotas overviewStay organized with collectionsSave and categorize content based on your preferences.

Google Cloud uses quotas to help ensure fairness and reduce
spikes in resource use and availability. A quota restricts how much of a
Google Cloud resource your Google Cloud project can use. Quotas
apply to a range of resource types, including hardware, software, and network
components. For example, quotas can restrict the number of API calls to a
service, the number of load balancers used concurrently by your project, or the
number of projects that you can create. Quotas protect the community of
Google Cloud users by preventing the overloading of services. Quotas also
help you to manage your own Google Cloud resources.

The Cloud Quotas system does the following:

- Monitors your consumption of Google Cloud products and services
- Restricts your consumption of those resources
- Provides a way to
      [request changes to the quota value](https://cloud.google.com/docs/quotas/help/request_increase)
      and [automate quota adjustments](https://cloud.google.com/docs/quotas/quota-adjuster)

In most cases, when you attempt to consume more of a resource than its quota
allows, the system blocks access to the resource, and the task that
you're trying to perform fails.

Quotas generally apply at the Google Cloud project
level. Your use of a resource in one project doesn't affect
your available quota in another project. Within a Google Cloud project, quotas
are shared across all applications and IP addresses.

Many services also have system limits. System limits are fixed constraints,
such as maximum file sizes or database schema limitations, which cannot be
increased or decreased.

To learn about the quotas and system limits for a product, see the product's
quotas and limits page—for example,
[Cloud Storage quotas and limits](https://cloud.google.com/storage/quotas).

The following links provide additional information related to resource usage:

- For resource pricing, see the product's pricing documentation—for example,
      [Cloud Storage pricing](https://cloud.google.com/storage/pricing)
- To generate a cost estimate based on your projected usage, use the
      [pricing calculator](https://cloud.google.com/products/calculator)
- For other API usage metrics, see
      [Monitoring API usage](https://cloud.google.com/apis/docs/monitoring)
- If you are a new Google Cloud user, you might be eligible for a
      [Free Trial](https://cloud.google.com/free/)

## Types of quotas

Google Cloud has three types of quotas:

- **Allocation quotas**: Allocation quotas restrict how much of a resource
  Google Cloud allocates to you. For example, Compute Engine applies an
  allocation quota to the number of VMs allocated for a Google Cloud
  project.
- **Rate quotas**: Rate quotas restrict the rate at which you can consume a
  resource. Rate quotas specify a time period, and the amount of the resource
  that you are permitted to consume over that time period.
- **Concurrent quotas**: Concurrent quotas restrict the number of operations that run
  concurrently. Concurrent quotas usually apply to long-running operations. For
  example, some Compute Engine `insert` operations can run for as long as one
  hour and are limited by a concurrent quota.

## Quotas and the Google Cloud hierarchy

Most quotas apply to one of the following levels of the Google Cloud
[hierarchy](https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy):

- **Project-level quotas**: Project-level quotas restrict your resource usage
  within a Google Cloud project. Using the resource in one project
  doesn't affect your available quota in another project.
- **Folder-level quotas**: Folder-level quotas restrict your resource usage
  within a Google Cloud folder. Child folders and projects contribute to
  your quota usage. Folders and projects outside of your folder don't affect
  your available quota.
- **Organization-level quotas**: Organization-level quotas restrict your
  resource usage within a Google Cloud organization. Child folders and
  projects contribute to your quota usage. Resource usage outside of your
  organization doesn't affect your available quota.

For example, the Compute Engine API has a project-level quota for the number of
queries you can make per minute. If one project reaches the quota value in less
than a minute, the project cannot make any more queries. Other projects can
continue to make queries.

Some quotas apply at the user level. For example, the number of
Google Cloud projects you can create is limited by a quota applied at the
level of the user or service account.

To identify the Google Cloud hierarchy level of the quotas for your
product, see the product's quotas and limits page—for example,
[Cloud Storage quotas and limits](https://cloud.google.com/storage/quotas).

## Regions and zones

Quotas are global, [regional, or zonal](https://cloud.google.com/compute/docs/regions-zones):

- **Global**: Global quotas restrict resource usage across all
      regions and zones. Resource usage in one region or zone reduces quota
      availability for all regions and zones.
- **Regional**: Regional quotas restrict resource usage in a
      Google Cloud region. Resource use in any zone in the region
      contributes to regional quota use.
      Resource usage in one region doesn't affect available quota in another
      region.
- **Zonal**: Zonal quotas restrict resource usage in a
      Google Cloud zone. Resource usage in one zone doesn't affect available
      zonal quota in another zone. If the resource is also subject to a regional
      quota, usage in one zone affects available quota in other zones by reducing
      the regional quota shared across zones, even though the zonal quota for
      other zones is unaffected.

Some resources have multiple location-based quotas. For example, a resource
might have both a regional quota and a zonal quota. The zonal quota restricts
the amount of use in each zone. The regional quota restricts the total use
across all zones in a given region.
To find out whether a quota is regional, zonal, or global, follow the
instructions to
[view dimensions](https://cloud.google.com/docs/quotas/configure-dimensions#view_dimensions).

Regions and zones are examples of quota dimensions. For more information about
working with dimensions, see
[Configure dimensions](https://cloud.google.com/docs/quotas/configure-dimensions).

## Manage quota values

Managing quota values and planning your resource use accordingly helps prevent
errors. Quota values are specific to your project, folder, and organization. For
example, you might request an adjustment to the value of a quota in one project,
but continue to use the default value in another project.

If you're using a
[free trial account](https://cloud.google.com/free/docs/frequently-asked-questions#limitations),
you might have lower quota values for some resources compared to the quota
values for a billed account. When you enable [billing](https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project)
for your project, the quota values increase for most services.

To get alerts
when you're approaching a quota value or system limit,
[Set up quota alerts](https://cloud.google.com/docs/quotas/set-up-quota-alerts). To learn what to do if
you run out of quota or reach a system limit, see
[When you run out of quota](#running_out).

### When you run out of quota

Usually, if you run out of quota the task that you're trying to perform fails
and you get a [quota error](https://cloud.google.com/docs/quotas/troubleshoot). For example, creating a
new project or calling an API throws a quota error if the task requires more
quota than you have. When this happens, the task continues to fail until you
have enough quota to accomplish the task.

If you want to keep your quota value, you can work within its constraints to
make your request:

- **Allocation quotas**: For allocation quotas, you can free up quota by deleting unused resources that
  count towards the quota or system limit that you want to consume. For example,
  you could have a quota value of 100 for a certain Compute Engine virtual
  machine. If you already have 99 of that virtual machine but you want to create
  ten more, your request will fail because adding ten more exceeds your quota
  value (you can still provision one more virtual machine). To free up resources,
  delete nine of the machines.
- **Rate quotas**: For rate quotas, your available quota resets automatically
  when the time period resets. For example, you could have a quota value of 1000
  requests per day for an API. If you already made 1000 requests to that API and
  you want to make 1000 more, wait until the next day. For per-day quotas, the
  time period resets at midnight Pacific Time. For per-minute quotas, the time
  period resets one minute after your first request in a rolling window.

If you want to change your quota value to accommodate more resource use, you can
request a quota adjustment. Using more resources can incur more costs. To learn
about quota adjustments, see
[About quota adjustments](#about_increase_requests).

### About quota adjustments

Most quota adjustment requests are evaluated by automated systems. Their
decision is based on criteria including the availability of resources, the
length of time you've used Google Cloud, and other factors. Requests that don't
meet the criteria are denied.

Evaluation criteria for automated reviews is not disclosed to ensure
fairness for all customers and prevent attempts to manipulate the process.
Sometimes quota adjustment requests are escalated to human reviewers, who also
follow criteria, but can consider your unique circumstances.

For quota adjustment requests that increase your quota value, you might be asked
to pay in advance. For example, you might be asked to make a payment if you
request more projects that will use paid Google Cloud services. The payment can
be applied to any charges you incur in the future and will be visible as a
credit in your account.

To learn how to request a quota adjustment, see
[Request a quota adjustment](https://cloud.google.com/docs/quotas/help/request_increase).

You don't need to have a paid Customer Care service to request a quota
adjustment. To automatically request quota adjustments when you're approaching
your quota value, you can use the
[quota adjuster](https://cloud.google.com/docs/quotas/quota-adjuster). To use the quota
adjuster, you must have enough usage history for the adjuster to make informed
predictions.

## What's next

- [Understand quota and system limit terminology](https://cloud.google.com/docs/quotas/terminology)
- [Quota permissions](https://cloud.google.com/docs/quotas/permissions)
- [View and manage quotas](https://cloud.google.com/docs/quotas/view-manage)
- [Monitor and alert](https://cloud.google.com/docs/quotas/set-up-quota-alerts)
- [Troubleshoot](https://cloud.google.com/docs/quotas/troubleshoot)

   Was this helpful?

---

# Quota permissionsStay organized with collectionsSave and categorize content based on your preferences.

> Discover the Google Cloud quota system that helps you monitor existing quota usage or update API quotas within specific projects.

# Quota permissionsStay organized with collectionsSave and categorize content based on your preferences.

The predefined
[Identity and Access Management (IAM)](https://cloud.google.com/iam/docs/overview)
role for permissions is named Quota Administrator. This role can be assigned at
the project, folder, and organization levels.

- If granted at the project level, the user will have permission to perform
  project-level operations.
- If granted at the folder level, the user will have permission to perform
  project-level operations for all projects in that folder.
- If granted at the organization level, the user will have permission to
  perform organization level operations. Because IAM permissions
  are inherited from the top level, this user will also be granted project and
  folder level permissions.

Users who are part of the Project Owners role can assign the Quota Administrator
role to other users at the project level. Users in the Organization Owner role
can assign the Quota Administrator role at the organization level.

## Permissions for viewing quota

To view your project quota in the Google Cloud console or to access your project quota
programmatically, you must have the following IAM permissions:

- `resourcemanager.projects.get`
- `resourcemanager.folders.get` if you want to view quota for an entire
  [Folder.](https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy#folders)
- `resourcemanager.organizations.get` if you want to view quota for an entire
  [Organization.](https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy#organizations)
- [monitoring.timeSeries.list](https://cloud.google.com/iam/docs/roles-permissions/monitoring#monitoring.timeSeries.list)
- [serviceusage.services.list](https://cloud.google.com/iam/docs/roles-permissions/serviceusage#serviceusage.services.list)
- [serviceusage.quotas.get](https://cloud.google.com/iam/docs/roles-permissions/serviceusage#serviceusage.quotas.get)

To learn which [roles](https://cloud.google.com/iam/docs/roles-overview) include
these permissions by default, see the
[IAM permissions reference](https://cloud.google.com/iam/docs/roles-permissions).

## Permissions for changing quota

To change your quota at the project level, folder level, or organization level,
you must have the following IAM permission:

- [serviceusage.quotas.update](https://cloud.google.com/iam/docs/roles-permissions/serviceusage#serviceusage.quotas.update)

This permission is included by default for the following
[roles](https://cloud.google.com/iam/docs/roles-overview): Owner, Editor, Quota Administrator, and
Service Usage Admin.

## Permissions for viewing quota increase requests

To view quota increase requests in the Google Cloud console, you must have the
following [IAM permissions](https://cloud.google.com/iam/docs/roles-permissions):

- `resourcemanager.projects.get`
- [serviceusage.services.list](https://cloud.google.com/iam/docs/roles-permissions/serviceusage#serviceusage.services.list)
- [serviceusage.quotas.get](https://cloud.google.com/iam/docs/roles-permissions/serviceusage#serviceusage.quotas.get)

## Permissions for creating an alert policy for a quota

To [set up quota alerts](https://cloud.google.com/docs/quotas/set-up-quota-alerts), you must have the
following permission:

- `monitoring.alertPolicies.create`

   Was this helpful?
