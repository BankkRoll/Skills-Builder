# Quota adjusterStay organized with collectionsSave and categorize content based on your preferences. and more

# Quota adjusterStay organized with collectionsSave and categorize content based on your preferences.

> Quota adjuster observes your resource consumption and proactively submits a quota increase request on your behalf when usage nears a maximum specified value.

# Quota adjusterStay organized with collectionsSave and categorize content based on your preferences.

This document describes how to adjust
quotas by using the quota adjuster system.

The quota adjuster observes your resource consumption and
proactively submits quota adjustment requests on your behalf. Monitoring your
resource use and submitting quota adjustment requests proactively prevents
outages caused by reaching your quota value. Using the
quota adjuster reduces the need to watch for unplanned increases
in your resource use, and lets you submit fewer manual requests for quota
adjustments.

## How the quota adjuster works

When you [enable the quota adjuster](#enable), it monitors all
applicable quotas and applies the following logic:

- Quota adjuster checks if the peak usage has approached the quota
  value
  during a specified duration.
- If so, the quota adjuster attempts to increase the quota
  value (typically around 10-20%).

If it's possible to increase the quota value, the increase is approved and
the value adjusted. You can still manually request increases to quota
values at any time, whether or not the quota adjuster is enabled.

The quota adjuster only submits quota adjustment requests to
increase the value of a quota. It doesn't attempt to lower the value. For quotas
that have a
[manual quota cap](https://cloud.google.com/docs/quotas/view-manage#create_override),
the quota adjuster doesn't submit quota adjustment requests.

You can [view requests](#view-quota-adjustment-requests) made by the
quota adjuster in the Quotas & System Limits page of
Google Cloud console. You can also set up [alerts](#alerts) to monitor changes
initiated by the quota adjuster.

## Limitations

The quota adjuster has the following limitations:

- Quota adjuster settings are only available on a per-project
  basis.
- Quota adjuster settings are only accessible from the
  Google Cloud console.
- The quota adjuster isn't available for all quotas. To learn
  more, see [Availability](#availability) in this document.

## Availability

Quota adjuster availability depends on your Google Cloud project and
is only available for some Google Cloud quotas.

### Eligibility based on usage history

The quota adjuster requires a sufficient volume of historical
usage data in order to accurately determine when to request additional quota.
For this reason, the option to enable the quota adjuster is only
available on projects with enough historical activity to support accurate
predictions.

### Supported quotas

The quota adjuster isn't available for all
Google Cloud quotas. A Google Cloud service might support the
quota adjuster for all, some, or none of its quotas.
If you enable the quota adjuster on your project, it
applies to all supported quotas.

When a Google Cloud service adds or expands
quota adjuster support for its quotas, the
quota adjuster automatically monitors and adjusts these
newly supported quotas for your project. This happens even if these
specific quotas weren't supported when you initially enabled the
quota adjuster.

The following table lists quotas supported by the quota adjuster.

| Service | Quotas |
| --- | --- |
| Artifact Registry API | Requests per project in the Asia multi-region per minute |
| Artifact Registry API | Requests per project in the Europe multi-region per minute |
| Artifact Registry API | Requests per project in the US multi-region per minute |
| Artifact Registry API | Requests per project per region per minute per region |
| Cloud Build API | Build and Operation Get requests per minute |
| Cloud Build API | Build and Operation Get requests per minute per user |
| Cloud Build API | Concurrent Build CPUs (Regional Default Pool) |
| Cloud Build API | Concurrent Builds (Non-regional Default Pool) |
| Cloud Key Management Service API | Cryptographic requests per minute |
| Cloud Key Management Service API | Read requests per minute |
| Cloud Key Management Service API | Write requests per minute |
| Cloud Logging API | Log write bytes per minute per region |
| Cloud Resource Manager API | Read requests per minute |
| Cloud Run Admin API | Job run requests per minute per region |
| Cloud Run Admin API | Read requests per minute per region |
| Cloud Run Admin API | Total CPU allocation, in milli vCPU, per project per region |
| Cloud Run Admin API | Write requests per minute per region |
| Cloud Trace API | Write requests (free) per minute |
| Compute Engine API | Affinity groups |
| Compute Engine API | Backend buckets |
| Compute Engine API | C2 CPUs |
| Compute Engine API | C2D CPUs |
| Compute Engine API | C3 CPUs |
| Compute Engine API | Commitments |
| Compute Engine API | Committed A2 CPUs |
| Compute Engine API | Committed CPUs |
| Compute Engine API | Committed licenses |
| Compute Engine API | Committed local SSD disk reserved (GB) |
| Compute Engine API | Committed M3 CPUs |
| Compute Engine API | Committed Memory Optimized CPUs |
| Compute Engine API | Committed N2 CPUs |
| Compute Engine API | Committed N2D CPUs |
| Compute Engine API | Committed T2D CPUs |
| Compute Engine API | CPUs |
| Compute Engine API | CPUs per VM family |
| Compute Engine API | Cross Project Networking Service projects |
| Compute Engine API | Custom static routes per VPC Network |
| Compute Engine API | External passthrough Network Load Balancer backend services |
| Compute Engine API | External passthrough Network Load Balancer forwarding rules |
| Compute Engine API | External protocol forwarding rules |
| Compute Engine API | Firewall rules |
| Compute Engine API | Forwarding rules |
| Compute Engine API | Global external managed backend services |
| Compute Engine API | Global External Managed Forwarding Rules |
| Compute Engine API | Global external proxy LB backend services |
| Compute Engine API | Global internal traffic director backend services |
| Compute Engine API | GPU count per GPU family |
| Compute Engine API | GPUs (all regions) |
| Compute Engine API | Health checks |
| Compute Engine API | Images |
| Compute Engine API | In-use IP addresses |
| Compute Engine API | In-use regional external IPv4 addresses |
| Compute Engine API | In-use snapshot schedules |
| Compute Engine API | Instance groups |
| Compute Engine API | Instance templates |
| Compute Engine API | Instances Per peering group |
| Compute Engine API | Instances per VPC Network |
| Compute Engine API | Internal IP addresses |
| Compute Engine API | Internal passthrough Network Load Balancer backend services |
| Compute Engine API | Internal passthrough Network Load Balancer forwarding rules per peering group |
| Compute Engine API | Internal passthrough Network Load Balancer forwarding rules per VPC network |
| Compute Engine API | IP Aliases per peering group |
| Compute Engine API | IP Aliases per VPC Network |
| Compute Engine API | Local SSD disk per VM family (GB) |
| Compute Engine API | M1 CPUs |
| Compute Engine API | M2 CPUs |
| Compute Engine API | M3 CPUs |
| Compute Engine API | Managed instance groups |
| Compute Engine API | N2 CPUs |
| Compute Engine API | N2D CPUs |
| Compute Engine API | Network endpoint groups |
| Compute Engine API | Network firewall policies |
| Compute Engine API | Network load balancing security policies |
| Compute Engine API | Network load balancing security policy rule attributes |
| Compute Engine API | Networks |
| Compute Engine API | NVIDIA A2 CPUs |
| Compute Engine API | Peerings Per VPC Network |
| Compute Engine API | Persistent Disk IOPS |
| Compute Engine API | Persistent Disk SSD (GB) |
| Compute Engine API | Persistent Disk Standard (GB) |
| Compute Engine API | Preemptible CPUs |
| Compute Engine API | Preemptible Local SSD (GB) |
| Compute Engine API | Preemptible NVIDIA A100 80GB GPUs |
| Compute Engine API | Preemptible NVIDIA A100 GPUs |
| Compute Engine API | Preemptible NVIDIA H100 GPUs |
| Compute Engine API | Preemptible NVIDIA H100 MEGA GPUs |
| Compute Engine API | Preemptible NVIDIA K80 GPUs |
| Compute Engine API | Preemptible NVIDIA L4 GPUs |
| Compute Engine API | Preemptible NVIDIA L4 Virtual Workstation GPUs |
| Compute Engine API | Preemptible NVIDIA P100 GPUs |
| Compute Engine API | Preemptible NVIDIA P100 Virtual Workstation GPUs |
| Compute Engine API | Preemptible NVIDIA P4 GPUs |
| Compute Engine API | Preemptible NVIDIA P4 Virtual Workstation GPUs |
| Compute Engine API | Preemptible NVIDIA T4 GPUs |
| Compute Engine API | Preemptible NVIDIA T4 Virtual Workstation GPUs |
| Compute Engine API | Preemptible NVIDIA V100 GPUs |
| Compute Engine API | Public advertised prefixes |
| Compute Engine API | Regional external managed backend services |
| Compute Engine API | Regional External Managed Forwarding Rules per region per VPC Network |
| Compute Engine API | Regional Instance templates |
| Compute Engine API | Regional internal managed backend services |
| Compute Engine API | Regional internal traffic director backend services |
| Compute Engine API | Regional managed instance groups |
| Compute Engine API | Regional security policies |
| Compute Engine API | Regional security policy rules with an advanced match condition |
| Compute Engine API | Regional Target TCP proxies |
| Compute Engine API | Routers |
| Compute Engine API | Routes |
| Compute Engine API | Security policies |
| Compute Engine API | Security policy rules |
| Compute Engine API | Security policy rules language rules |
| Compute Engine API | Snapshots |
| Compute Engine API | SSL certificates |
| Compute Engine API | Static BYOIP IP addresses |
| Compute Engine API | Static IP addresses |
| Compute Engine API | Subnet ranges Per peering group |
| Compute Engine API | Subnetwork ranges per VPC Network |
| Compute Engine API | T2A CPUs |
| Compute Engine API | T2D CPUs |
| Compute Engine API | Target HTTP proxies |
| Compute Engine API | Target HTTPS proxies |
| Compute Engine API | Target SSL proxies |
| Compute Engine API | Target TCP proxies |
| Compute Engine API | Target VPN gateways |
| Compute Engine API | Total Local SSD disk reserved (GB) |
| Compute Engine API | URL maps |
| Compute Engine API | VM instances |
| Compute Engine API | VPN gateways |
| Compute Engine API | VPN tunnels |
| Connect gateway API | Gateway Connection Requests per minute |
| Dialogflow API | All other requests per minute |
| Filestore API | Backups per region |
| Filestore API | Basic HDD (Standard) capacity (GB) per region |
| Filestore API | Basic SSD (Premium) capacity (GB) per region |
| Filestore API | Zonal & Regional 1-10 TiB (Enterprise) capacity (GB) per region |
| Filestore API | Zonal & Regional 10-100 TiB (High Scale) capacity (GB) per region |
| Google Cloud Memorystore for Redis API | Total Redis capacity (GB) per region |
| Google Cloud Memorystore for Redis API | Total Redis Cluster units per project per region |
| Memorystore API | Total Memorystore units per project per region |
| Vertex AI API | Custom model serving CPUs per region |
| Vertex AI API | Custom model serving Nvidia T4 GPUs per region |
| Vertex AI API | Custom model training Nvidia T4 GPUs per region |
| Vertex AI API | Generate content requests per minute per project per base model |
| Vertex AI API | Regional online prediction requests per minute per project per base modelNote: To see the full list of available dimensions, expand this entry in the Google Cloud console. |
| Vertex AI API | Resource management (CRUD) requests per minute per region |
| Vertex AI API | Restricted image training TPU V3 pod cores per region |

## Enable the quota adjuster

To enable the quota adjuster, you must have the following
IAM permissions:

- `cloudquotas.quotas.update`
- `cloudquotas.quotas.get`

To enable the quota adjuster on your Google Cloud console project,
select the appropriate tab and follow the instructions:

To enable the quota adjuster on your Google Cloud project
from the Google Cloud console, follow these steps:

1. In the Google Cloud console, go to the
  **IAM & Admin>Quotas & System Limits** page:
  [Go to Quotas & System Limits](https://console.cloud.google.com/iam-admin/quotas)
2. Click the **Configurations** tab.
3. Click the **Enable** toggle.

When the **Status** column reads **Enabled**, the
quota adjuster monitors your usage and issues quota adjustment
requests when resource use approaches its quota value.

1. To enable the quota adjuster on your Google Cloud project
  using the REST API ([Preview](https://cloud.google.com/products#product-launch-stages)), make an
  HTTP request to update quota adjuster settings:
  ```
  PATCH https://cloudquotas.googleapis.com/v1beta/projects/PROJECT_ID_OR_NUMBER/locations/global/quotaAdjusterSettings
  ```
2. In the request body, specify the quota adjuster settings resource and set
  the `enablement` field to `ENABLED`. You can also specify an ETag, but
  doing so is optional:
  ```
  {
    name: projects/PROJECT_ID_OR_NUMBER/locations/global/quotaAdjusterSettings
    enablement: ENABLED
    etag: OPTIONAL_ETAG
  }
  ```
  Replace the following:
  - `PROJECT_ID_OR_NUMBER`: the project ID or project
    number of the project for which you want to enable the
    quota adjuster.
  - `OPTIONAL_ETAG`: an optional ETag string for the
    quota adjuster settings.
  This updates the enablement status to `enabled`.

To enable the quota adjuster on your Google Cloud project
using the gcloud CLI ([Preview](https://cloud.google.com/products#product-launch-stages)),
follow these steps:

1. Authenticate using the gcloud CLI:
  ```
  gcloud auth login
  ```
2. Enable quota adjuster settings:
  ```
  gcloud beta quotas adjuster settings update --project=PROJECT_ID_OR_NUMBER --enablement=enabled
  ```
  Replace `PROJECT_ID_OR_NUMBER` with the project ID
  or project number of the project for which you want to enable the
  quota adjuster.
3. Verify the enablement status:
  ```
  gcloud beta quotas adjuster settings describe --project=PROJECT_ID_OR_NUMBER
  ```
  As long as you have the required permissions, this returns the status
  as `enabled`.

## View quota adjustment requests

To view quota adjustment requests, you must have the following
IAM permissions:

- `resourcemanager.projects.get`
- `serviceusage.services.list`
- `serviceusage.quotas.get`

To view quota adjustment requests issued by the quota adjuster:

1. In the Google Cloud console, go to the
  **IAM & Admin>Quotas & System Limits** page:
  [Go to Quotas & System Limits](https://console.cloud.google.com/iam-admin/quotas)
2. Click the **Increase Requests** tab. The **Increase Requests** view shows
  increase requests for your project, including both manually requested
  increases and requests issued by the quota adjuster.
3. Click the **Filter** field.
4. Select **Type** from the menu, and enter `Auto`. This filters for requests
  made by the quota adjuster.

## Set up quota adjuster alerts

To receive alerts from the quota adjuster:

1. In the Google Cloud console, go to the
  **IAM & Admin>Quotas & System Limits** page:
  [Go to Quotas & System Limits](https://console.cloud.google.com/iam-admin/quotas)
2. Click the **Configurations** tab.
3. Click **Create Alert.**
4. Choose one or both of the alert templates:
  1. **All adjustments by Quota Adjuster** sends an alert
    every time the
    quota adjuster issues a quota adjustment request for the
    project.
  2. **Quota Adjuster errors and failures** sends alerts only when the
    quota adjuster attempts to increase a quota value and is
    unable to do so.
5. Optional: Adjust the default values for the minimum amount of
  time between alerts and the incident autoclose duration by clicking
  **Show Options**.
6. Select the **Notification Channel** to receive alerts. To adjust your
  notification channel settings or create a new notification channel, click
  **Manage Notification Channels**.
7. Click **Create**.

## Edit or delete quota adjuster alerts

You can edit or delete quota adjuster alerts in the
Google Cloud console:

1. Go to the **Policies** page in the Cloud Monitoring console.
  [Go to Policies](https://console.cloud.google.com/monitoring/alerting/policies)
2. Search for your quota adjuster alert policy.
  quota adjuster alert policies have the following names:
  - `Quota adjuster errors and failures`
  - `All adjustments by quota adjuster`
3. In the row showing your quota adjuster alert policy, click
   **View more**.
4. Click **Edit** or **Delete**.

## Disable the quota adjuster

To disable the quota adjuster, you must have the following
IAM permissions:

- `cloudquotas.quotas.update`
- `cloudquotas.quotas.get`

To disable the quota adjuster on your Google Cloud console project,
select the appropriate tab and follow the instructions:

1. In the Google Cloud console, go to the
  **IAM & Admin>Quotas & System Limits** page:
  [Go to Quotas & System Limits](https://console.cloud.google.com/iam-admin/quotas)
2. Click the **Configurations** tab.
3. Click the **Enable** toggle. The toggle turns gray.

When the toggle is gray and the status column reads **Not Enabled**, the quota
adjuster no longer monitors your usage or issues quota adjustment requests.

1. To disable the quota adjuster on your Google Cloud project
  using the REST API ([Preview](https://cloud.google.com/products#product-launch-stages)), make an
  HTTP request to update quota adjuster settings:
  ```
  PATCH https://cloudquotas.googleapis.com/v1beta/projects/PROJECT_ID_OR_NUMBER/locations/global/quotaAdjusterSettings
  ```
2. In the request body, specify the quota adjuster settings resource and set
  the `enablement` field to `DISABLED`. You can also specify an ETag, but
  doing so is optional:
  ```
  {
    name: projects/PROJECT_ID_OR_NUMBER/locations/global/quotaAdjusterSettings
    enablement: DISABLED
    etag: OPTIONAL_ETAG
  }
  ```
  Replace the following:
  - `PROJECT_ID_OR_NUMBER`: the project ID or project
    number of the project for which you want to disable the
    quota adjuster.
  - `OPTIONAL_ETAG`: an optional ETag string for the
    quota adjuster settings.
  This updates the enablement status to `disabled`.

To disable the quota adjuster on your Google Cloud project
using the gcloud CLI ([Preview](https://cloud.google.com/products#product-launch-stages)),
follow these steps:

1. Authenticate to the gcloud CLI:
  ```
  gcloud auth login
  ```
2. Disable quota adjuster settings:
  ```
  gcloud beta quotas adjuster settings update --project=PROJECT_ID_OR_NUMBER --enablement=disabled
  ```
  Replace `PROJECT_ID_OR_NUMBER` with the project ID
  or project number of the project for which you want to disable the
  quota adjuster.
3. Verify the enablement state:
  ```
  gcloud beta quotas adjuster settings describe --project=PROJECT_ID_OR_NUMBER
  ```
  As long as you have the required permissions, this returns the status
  as `disabled`.

## Troubleshoot quota increase denials

It's possible that a quota increase initiated by the quota
adjuster will be denied. This sometimes occurs when Google Cloud is unable to
increase the quota for a particular project, resource, or region beyond a
certain value. You may still request a manual quota increase in these scenarios.

To receive notifications when a quota adjustment request made by the quota
adjuster is denied, set up [quota adjuster alerts](#alerts).

   Was this helpful?

---

# Quota project overviewStay organized with collectionsSave and categorize content based on your preferences.

> Understand quota projects, and how the quota project is determined for resource-based APIs, and client-based APIs.

# Quota project overviewStay organized with collectionsSave and categorize content based on your preferences.

This document describes the *quota project* and how the quota project is
determined. Make sure that your quota project is set correctly to help avoid
errors and failed requests to the Cloud APIs.

You must specify a quota project because every request to a Google Cloud API is
counted against a quota and because quotas are enforced by project. For more
information, see [How to set the quota
project](https://cloud.google.com/docs/quotas/set-quota-project)
.

Note for gcloud CLI users: the *quota project* is sometimes referred
to as the *billing project*. This is because the [billing_projectflag](https://cloud.google.com/sdk/gcloud/reference#--billing-project)
takes precedence over the [billing/quota_projectproperty](https://cloud.google.com/sdk/gcloud/reference/config/set#quota_project) in your
gcloud CLI configuration.

## How the quota project is determined

How the quota project is determined depends on the type of API method that you
use: *resource-based API* or *client-based API*. In rare cases, a service might
have both types of API methods.

### Resource-based APIs

For resource-based Cloud APIs, the project that provides quota for
an API call is also the project that contains the resource that is being
accessed. For example, when you create a Compute Engine instance, you must
specify the project for that new instance. The project then contains the newly
created instance. Later, if you perform operations on the Compute Engine
instance, the project that contains the instance provides the quota for the
request. This applies regardless of whether you use the Google Cloud CLI, REST
API, or client libraries.

You cannot change the quota project used by a request to a resource-based API.
The request always uses the project that contains the resource that the request
is operating on.

### Client-based APIs

If an API is not a resource-based API, it's a client-based API. For example, the
Cloud Translation API is a commonly used client-based API.

Requests can fail if you make a request to a client-based API and the quota
project cannot be identified. The quota project can be set in multiple ways and
is verified by checking the following options. They appear in the order of
precedence:

- **Specified in request**: The quota project that was specified in the
  [request](https://cloud.google.com/docs/quotas/set-quota-project#set-project-programmatically).
  (When using client libraries, you can also use [environment
  variables](https://cloud.google.com/docs/quotas/set-quota-project#set-project-variable)
  in your requests.)
- **API key**: If you use an API key to provide credentials for a
  request, the project associated with the API key is used as the quota
  project.
- **Google Cloud CLI credentials**: If you use the gcloud CLI
  to get your access token, and you've authenticated to the
  gcloud CLI with your user credentials, the gcloud CLI
  shared project is sometimes used as the quota project. However, not all
  client-based APIs fall back on the shared project.
- **Service account**: If the principal for the API call is a service
  account, including by impersonation, the project associated with the service
  account is used as the quota project.
- **Workforce identity federation**: If the principal for the API is a
  workforce identity federation user, the
  [workforce pools user project](https://cloud.google.com/iam/docs/workforce-identity-federation#workforce-pools-user-project)
  is used as the quota project.

If none of the previous checks yield a quota project, the request fails.

#### About the gcloud CLI shared project for client-based APIs

If you use the gcloud CLI to make a request to a client-based API
without setting the quota project, the request might fall back on the
*gcloud CLI shared project*, or the request might fail. The
gcloud CLI shared project is used by all gcloud CLI
requests in all projects, so if many other gcloud CLI requests are
also using this project as their quota project, the quota for the shared project
might temporarily be depleted. If this happens, your request fails with an
out-of-quota error message.

#### Identify the current quota project for client-based APIs

The method for identifying the quota project depends on how your project is
configured:

- If an API method is configured to use a resource-based API, the client
  project uses the resource project as the quota project.
- If a user project override is in place, use the
  [gcloud [command] --log-httpcommand](https://cloud.google.com/sdk/gcloud/reference#--log-http)
  to print a log and check the quota project that appears in the
  `x-goog-user-project` field.
- If an API key was used for authentication, use the
  [gcloud [command] --log-httpcommand](https://cloud.google.com/sdk/gcloud/reference#--log-http)
  to print a log and check the quota project that appears in the
  `x-goog-api-key` field.

For other configurations, the quota project doesn't appear in HTTP headers.

## Determine if an API is resource-based or client-based

It can be difficult to determine which type of API you're using. However,
activation and quotas are enforced in the same way. For example, if a service
account from project A calls a read method in project B, and neither project has
the API enabled, the `API not enabled` error message indicates which project is
checked for activation. The project checked for activation is the same project
checked for
[rate quota](https://cloud.google.com/docs/quotas/overview#types_of_quota).

## What's next

- Learn how to set the [quota
  project](https://cloud.google.com/docs/quotas/set-quota-project)
- Learn more about [Application Default
  Credentials](https://cloud.google.com/docs/authentication/application-default-credentials)
- Get more information about
  [authentication](https://cloud.google.com/docs/authentication)
- Understand [quotas](https://cloud.google.com/docs/quotas/overview)
- For gcloud CLI users:
  - For more information about
    gcloud CLI configurations, see the
    [gcloud config](https://cloud.google.com/sdk/gcloud/reference/config)
    reference documentation
  - For more information about the `--billing_project` flag, see the [Google Cloud SDK reference](https://cloud.google.com/sdk/gcloud/reference#--billing-project)

   Was this helpful?

---

# Quotas and system limitsStay organized with collectionsSave and categorize content based on your preferences.

> Review quotas and system limits for Cloud Quotas.

# Quotas and system limitsStay organized with collectionsSave and categorize content based on your preferences.

This document lists the quotas and system limits that apply to
  Cloud Quotas.

- *Quotas* have default values, but you can typically request
      adjustments.
- *System limits* are fixed values that can't be changed.

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

For more information, see the
 [Cloud Quotas overview](https://cloud.google.com/docs/quotas/overview).

## Rate quotas

The following quotas apply to Cloud Quotas API requests:

| Quota | Value |
| --- | --- |
| Read requests per minute, per project | 1200 |
| Update requests per minute, per project | 60 |
| Quota increase requests per day, per project | 300 |

## Request a quota adjustment

To adjust most quotas, use the Google Cloud console.
  For more information, see
  [Request a quota adjustment](https://cloud.google.com/docs/quotas/help/request_increase).
