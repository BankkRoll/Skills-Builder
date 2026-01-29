# REST Resource: organizations.locations.services.quotaInfosStay organized with collectionsSave and categorize content based on your preferences. and more

# REST Resource: organizations.locations.services.quotaInfosStay organized with collectionsSave and categorize content based on your preferences.

# REST Resource: organizations.locations.services.quotaInfosStay organized with collectionsSave and categorize content based on your preferences.

## Resource: QuotaInfo

QuotaInfo represents information about a particular quota for a given project, folder or organization.

| JSON representation |
| --- |
| See more code actions.Light code themeDark code theme{"name":string,"quotaId":string,"metric":string,"service":string,"isPrecise":boolean,"refreshInterval":string,"containerType":enum (ContainerType),"dimensions":[string],"metricDisplayName":string,"quotaDisplayName":string,"metricUnit":string,"quotaIncreaseEligibility":{object (QuotaIncreaseEligibility)},"isFixed":boolean,"dimensionsInfos":[{object (DimensionsInfo)}],"isConcurrent":boolean,"serviceRequestQuotaUri":string} |

| Fields |
| --- |
| name |
| quotaId |
| metric |
| service |
| isPrecise |
| refreshInterval |
| containerType |
| dimensions[] |
| metricDisplayName |
| quotaDisplayName |
| metricUnit |
| quotaIncreaseEligibility |
| isFixed |
| dimensionsInfos[] |
| isConcurrent |
| serviceRequestQuotaUri |

| Methods |
| --- |
| get |
| list |

     Was this helpful?

---

# Method: projects.locations.quotaAdjusterSettings.getQuotaAdjusterSettingsStay organized with collectionsSave and categorize content based on your preferences.

# Method: projects.locations.quotaAdjusterSettings.getQuotaAdjusterSettingsStay organized with collectionsSave and categorize content based on your preferences.

RPC Method for getting QuotaAdjusterSettings based on the request

### HTTP request

`GET https://cloudquotas.googleapis.com/v1beta/{name=projects/*/locations/*/quotaAdjusterSettings}`

The URL uses [gRPC Transcoding](https://google.aip.dev/127) syntax.

### Path parameters

| Parameters |
| --- |
| name |

### Request body

The request body must be empty.

### Response body

If successful, the response body contains an instance of `QuotaAdjusterSettings`.

### Authorization scopes

Requires the following OAuth scope:

- `https://www.googleapis.com/auth/cloud-platform`

For more information, see the [Authentication Overview](https://cloud.google.com/docs/authentication#authorization-gcp).

### IAM Permissions

Requires the following [IAM](https://cloud.google.com/iam/docs) permission on the `name` resource:

- `cloudquotas.quotas.get`

For more information, see the [IAM documentation](https://cloud.google.com/iam/docs).

---

# Method: projects.locations.quotaAdjusterSettings.updateQuotaAdjusterSettingsStay organized with collectionsSave and categorize content based on your preferences.

# Method: projects.locations.quotaAdjusterSettings.updateQuotaAdjusterSettingsStay organized with collectionsSave and categorize content based on your preferences.

RPC Method for updating QuotaAdjusterSettings based on the request

### HTTP request

`PATCH https://cloudquotas.googleapis.com/v1beta/{quotaAdjusterSettings.name=projects/*/locations/*/quotaAdjusterSettings}`

The URL uses [gRPC Transcoding](https://google.aip.dev/127) syntax.

### Path parameters

| Parameters |
| --- |
| quotaAdjusterSettings.name |

### Query parameters

| Parameters |
| --- |
| updateMask |
| validateOnly |

### Request body

The request body contains an instance of `QuotaAdjusterSettings`.

### Response body

If successful, the response body contains an instance of `QuotaAdjusterSettings`.

### Authorization scopes

Requires the following OAuth scope:

- `https://www.googleapis.com/auth/cloud-platform`

For more information, see the [Authentication Overview](https://cloud.google.com/docs/authentication#authorization-gcp).

### IAM Permissions

Requires the following [IAM](https://cloud.google.com/iam/docs) permission on the `name` resource:

- `cloudquotas.quotas.update`

For more information, see the [IAM documentation](https://cloud.google.com/iam/docs).

---

# REST Resource: projects.locations.quotaAdjusterSettingsStay organized with collectionsSave and categorize content based on your preferences.

# REST Resource: projects.locations.quotaAdjusterSettingsStay organized with collectionsSave and categorize content based on your preferences.

## Resource: QuotaAdjusterSettings

The QuotaAdjusterSettings resource defines the settings for the Quota Adjuster.

| JSON representation |
| --- |
| {"name":string,"enablement":enum (Enablement),"updateTime":string,"etag":string} |

| Fields |
| --- |
| name |
| enablement |
| updateTime |
| etag |

## Enablement

The enablement status of the quota adjuster.

| Enums |
| --- |
| ENABLEMENT_UNSPECIFIED |
| ENABLED |
| DISABLED |

| Methods |
| --- |
| getQuotaAdjusterSettings |
| updateQuotaAdjusterSettings |

     Was this helpful?

---

# Method: projects.locations.quotaPreferences.createStay organized with collectionsSave and categorize content based on your preferences.

# Method: projects.locations.quotaPreferences.createStay organized with collectionsSave and categorize content based on your preferences.

Creates a new QuotaPreference that declares the desired value for a quota.

### HTTP request

`POST https://cloudquotas.googleapis.com/v1beta/{parent=projects/*/locations/*}/quotaPreferences`

The URL uses [gRPC Transcoding](https://google.aip.dev/127) syntax.

### Path parameters

| Parameters |
| --- |
| parent |

### Query parameters

| Parameters |
| --- |
| quotaPreferenceId |
| ignoreSafetyChecks[] |

### Request body

The request body contains an instance of `QuotaPreference`.

### Response body

If successful, the response body contains a newly created instance of `QuotaPreference`.

### Authorization scopes

Requires the following OAuth scope:

- `https://www.googleapis.com/auth/cloud-platform`

For more information, see the [Authentication Overview](https://cloud.google.com/docs/authentication#authorization-gcp).

### IAM Permissions

Requires the following [IAM](https://cloud.google.com/iam/docs) permission on the `parent` resource:

- `cloudquotas.quotas.update`

For more information, see the [IAM documentation](https://cloud.google.com/iam/docs).

---

# Method: projects.locations.quotaPreferences.getStay organized with collectionsSave and categorize content based on your preferences.

# Method: projects.locations.quotaPreferences.getStay organized with collectionsSave and categorize content based on your preferences.

Gets details of a single QuotaPreference.

### HTTP request

`GET https://cloudquotas.googleapis.com/v1beta/{name=projects/*/locations/*/quotaPreferences/*}`

The URL uses [gRPC Transcoding](https://google.aip.dev/127) syntax.

### Path parameters

| Parameters |
| --- |
| name |

### Request body

The request body must be empty.

### Response body

If successful, the response body contains an instance of `QuotaPreference`.

### Authorization scopes

Requires the following OAuth scope:

- `https://www.googleapis.com/auth/cloud-platform`

For more information, see the [Authentication Overview](https://cloud.google.com/docs/authentication#authorization-gcp).

### IAM Permissions

Requires the following [IAM](https://cloud.google.com/iam/docs) permission on the `name` resource:

- `cloudquotas.quotas.get`

For more information, see the [IAM documentation](https://cloud.google.com/iam/docs).

---

# Method: projects.locations.quotaPreferences.listStay organized with collectionsSave and categorize content based on your preferences.

# Method: projects.locations.quotaPreferences.listStay organized with collectionsSave and categorize content based on your preferences.

Lists QuotaPreferences in a given project, folder or organization.

### HTTP request

`GET https://cloudquotas.googleapis.com/v1beta/{parent=projects/*/locations/*}/quotaPreferences`

The URL uses [gRPC Transcoding](https://google.aip.dev/127) syntax.

### Path parameters

| Parameters |
| --- |
| parent |

### Query parameters

| Parameters |
| --- |
| pageSize |
| pageToken |
| filter |
| orderBy |

### Request body

The request body must be empty.

### Response body

If successful, the response body contains an instance of `ListQuotaPreferencesResponse`.

### Authorization scopes

Requires the following OAuth scope:

- `https://www.googleapis.com/auth/cloud-platform`

For more information, see the [Authentication Overview](https://cloud.google.com/docs/authentication#authorization-gcp).

### IAM Permissions

Requires the following [IAM](https://cloud.google.com/iam/docs) permission on the `parent` resource:

- `cloudquotas.quotas.get`

For more information, see the [IAM documentation](https://cloud.google.com/iam/docs).

---

# Method: projects.locations.quotaPreferences.patchStay organized with collectionsSave and categorize content based on your preferences.

# Method: projects.locations.quotaPreferences.patchStay organized with collectionsSave and categorize content based on your preferences.

Updates the parameters of a single QuotaPreference. It can updates the config in any states, not just the ones pending approval.

### HTTP request

`PATCH https://cloudquotas.googleapis.com/v1beta/{quotaPreference.name=projects/*/locations/*/quotaPreferences/*}`

The URL uses [gRPC Transcoding](https://google.aip.dev/127) syntax.

### Path parameters

| Parameters |
| --- |
| quotaPreference.name |

### Query parameters

| Parameters |
| --- |
| updateMask |
| allowMissing |
| validateOnly |
| ignoreSafetyChecks[] |

### Request body

The request body contains an instance of `QuotaPreference`.

### Response body

If successful, the response body contains an instance of `QuotaPreference`.

### Authorization scopes

Requires the following OAuth scope:

- `https://www.googleapis.com/auth/cloud-platform`

For more information, see the [Authentication Overview](https://cloud.google.com/docs/authentication#authorization-gcp).

### IAM Permissions

Requires the following [IAM](https://cloud.google.com/iam/docs) permission on the `name` resource:

- `cloudquotas.quotas.update`

For more information, see the [IAM documentation](https://cloud.google.com/iam/docs).

---

# REST Resource: projects.locations.quotaPreferencesStay organized with collectionsSave and categorize content based on your preferences.

# REST Resource: projects.locations.quotaPreferencesStay organized with collectionsSave and categorize content based on your preferences.

## Resource: QuotaPreference

QuotaPreference represents the preferred quota configuration specified for a project, folder or organization. There is only one QuotaPreference resource for a quota value targeting a unique set of dimensions.

| JSON representation |
| --- |
| {"name":string,"dimensions":{string:string,...},"quotaConfig":{object (QuotaConfig)},"etag":string,"createTime":string,"updateTime":string,"service":string,"quotaId":string,"reconciling":boolean,"justification":string,"contactEmail":string} |

| Fields |
| --- |
| name |
| dimensions |
| quotaConfig |
| etag |
| createTime |
| updateTime |
| service |
| quotaId |
| reconciling |
| justification |
| contactEmail |

| Methods |
| --- |
| create |
| get |
| list |
| patch |

     Was this helpful?

---

# Method: projects.locations.services.quotaInfos.getStay organized with collectionsSave and categorize content based on your preferences.

# Method: projects.locations.services.quotaInfos.getStay organized with collectionsSave and categorize content based on your preferences.

Retrieve the QuotaInfo of a quota for a project, folder or organization.

### HTTP request

`GET https://cloudquotas.googleapis.com/v1beta/{name=projects/*/locations/*/services/*/quotaInfos/*}`

The URL uses [gRPC Transcoding](https://google.aip.dev/127) syntax.

### Path parameters

| Parameters |
| --- |
| name |

### Request body

The request body must be empty.

### Response body

If successful, the response body contains an instance of `QuotaInfo`.

### Authorization scopes

Requires the following OAuth scope:

- `https://www.googleapis.com/auth/cloud-platform`

For more information, see the [Authentication Overview](https://cloud.google.com/docs/authentication#authorization-gcp).

### IAM Permissions

Requires the following [IAM](https://cloud.google.com/iam/docs) permission on the `name` resource:

- `cloudquotas.quotas.get`

For more information, see the [IAM documentation](https://cloud.google.com/iam/docs).

           Was this helpful?

---

# Method: projects.locations.services.quotaInfos.listStay organized with collectionsSave and categorize content based on your preferences.

# Method: projects.locations.services.quotaInfos.listStay organized with collectionsSave and categorize content based on your preferences.

Lists QuotaInfos of all quotas for a given project, folder or organization.

### HTTP request

`GET https://cloudquotas.googleapis.com/v1beta/{parent=projects/*/locations/*/services/*}/quotaInfos`

The URL uses [gRPC Transcoding](https://google.aip.dev/127) syntax.

### Path parameters

| Parameters |
| --- |
| parent |

### Query parameters

| Parameters |
| --- |
| pageSize |
| pageToken |

### Request body

The request body must be empty.

### Response body

If successful, the response body contains an instance of `ListQuotaInfosResponse`.

### Authorization scopes

Requires the following OAuth scope:

- `https://www.googleapis.com/auth/cloud-platform`

For more information, see the [Authentication Overview](https://cloud.google.com/docs/authentication#authorization-gcp).

### IAM Permissions

Requires the following [IAM](https://cloud.google.com/iam/docs) permission on the `parent` resource:

- `cloudquotas.quotas.get`

For more information, see the [IAM documentation](https://cloud.google.com/iam/docs).

---

# REST Resource: projects.locations.services.quotaInfosStay organized with collectionsSave and categorize content based on your preferences.

# REST Resource: projects.locations.services.quotaInfosStay organized with collectionsSave and categorize content based on your preferences.

## Resource: QuotaInfo

QuotaInfo represents information about a particular quota for a given project, folder or organization.

| JSON representation |
| --- |
| {"name":string,"quotaId":string,"metric":string,"service":string,"isPrecise":boolean,"refreshInterval":string,"containerType":enum (ContainerType),"dimensions":[string],"metricDisplayName":string,"quotaDisplayName":string,"metricUnit":string,"quotaIncreaseEligibility":{object (QuotaIncreaseEligibility)},"isFixed":boolean,"dimensionsInfos":[{object (DimensionsInfo)}],"isConcurrent":boolean,"serviceRequestQuotaUri":string} |

| Fields |
| --- |
| name |
| quotaId |
| metric |
| service |
| isPrecise |
| refreshInterval |
| containerType |
| dimensions[] |
| metricDisplayName |
| quotaDisplayName |
| metricUnit |
| quotaIncreaseEligibility |
| isFixed |
| dimensionsInfos[] |
| isConcurrent |
| serviceRequestQuotaUri |

| Methods |
| --- |
| get |
| list |

---

# QuotaSafetyCheckStay organized with collectionsSave and categorize content based on your preferences.

# QuotaSafetyCheckStay organized with collectionsSave and categorize content based on your preferences.

Enumerations of quota safety checks.

| Enums |
| --- |
| QUOTA_SAFETY_CHECK_UNSPECIFIED |
| QUOTA_DECREASE_BELOW_USAGE |
| QUOTA_DECREASE_PERCENTAGE_TOO_HIGH |

     Was this helpful?

---

# Cloud Quotas APIStay organized with collectionsSave and categorize content based on your preferences.

# Cloud Quotas APIStay organized with collectionsSave and categorize content based on your preferences.

Cloud Quotas API provides Google Cloud service consumers with management and observability for resource usage, quotas, and restrictions of the services they consume.

## Service: cloudquotas.googleapis.com

To call this service, we recommend that you use the Google-provided [client libraries](https://cloud.google.com/apis/docs/client-libraries-explained). If your application needs to use your own libraries to call this service, use the following information when you make the API requests.

### Discovery document

A [Discovery Document](https://developers.google.com/discovery/v1/reference/apis) is a machine-readable specification for describing and consuming REST APIs. It is used to build client libraries, IDE plugins, and other tools that interact with Google APIs. One service may provide multiple discovery documents. This service provides the following discovery documents:

- [https://cloudquotas.googleapis.com/$discovery/rest?version=v1](https://cloudquotas.googleapis.com/$discovery/rest?version=v1)
- [https://cloudquotas.googleapis.com/$discovery/rest?version=v1beta](https://cloudquotas.googleapis.com/$discovery/rest?version=v1beta)

### Service endpoint

A [service endpoint](https://cloud.google.com/apis/design/glossary#api_service_endpoint) is a base URL that specifies the network address of an API service. One service might have multiple service endpoints. This service has the following service endpoint and all URIs below are relative to this service endpoint:

- `https://cloudquotas.googleapis.com`

## REST Resource:v1beta.folders.locations.quotaPreferences

| Methods |
| --- |
| create |
| get |
| list |
| patch |

## REST Resource:v1beta.folders.locations.services.quotaInfos

| Methods |
| --- |
| get |
| list |

## REST Resource:v1beta.organizations.locations.quotaPreferences

| Methods |
| --- |
| create |
| get |
| list |
| patch |

## REST Resource:v1beta.organizations.locations.services.quotaInfos

| Methods |
| --- |
| get |
| list |

## REST Resource:v1beta.projects.locations.quotaAdjusterSettings

| Methods |
| --- |
| getQuotaAdjusterSettings |
| updateQuotaAdjusterSettings |

## REST Resource:v1beta.projects.locations.quotaPreferences

| Methods |
| --- |
| create |
| get |
| list |
| patch |

## REST Resource:v1beta.projects.locations.services.quotaInfos

| Methods |
| --- |
| get |
| list |

## REST Resource:v1.folders.locations.quotaPreferences

| Methods |
| --- |
| create |
| get |
| list |
| patch |

## REST Resource:v1.folders.locations.services.quotaInfos

| Methods |
| --- |
| get |
| list |

## REST Resource:v1.organizations.locations.quotaPreferences

| Methods |
| --- |
| create |
| get |
| list |
| patch |

## REST Resource:v1.organizations.locations.services.quotaInfos

| Methods |
| --- |
| get |
| list |

## REST Resource:v1.projects.locations.quotaPreferences

| Methods |
| --- |
| create |
| get |
| list |
| patch |

## REST Resource:v1.projects.locations.services.quotaInfos

| Methods |
| --- |
| get |
| list |

---

# Cloud Quotas release notesStay organized with collectionsSave and categorize content based on your preferences.

# Cloud Quotas release notesStay organized with collectionsSave and categorize content based on your preferences.

This document lists production updates to Cloud Quotas.
Check this document for announcements about new or updated features, bug fixes,
known issues, and deprecated functionality.

You can see the latest product updates for all of Google Cloud on the
        [Google Cloud](https://cloud.google.com/release-notes) page, browse and filter all release notes in the
        [Google Cloud console](https://console.cloud.google.com/release-notes),
        or programmatically access release notes in
        [BigQuery](https://console.cloud.google.com/bigquery?p=bigquery-public-data&d=google_cloud_release_notes&t=release_notes&page=table).

To get the latest product updates delivered to you, add the URL of this page to your
        [feed
          reader](https://wikipedia.org/wiki/Comparison_of_feed_aggregators), or add the
        [feed URL](https://docs.cloud.google.com/feeds/cloudquotas-release-notes.xml) directly.

## June 05,2025

 VERSION_UNSPECIFIED  Feature

IAM roles for the Cloud Quotas is generally available ([GA](https://cloud.google.com/products#product-launch-stages)). For more information, see the IAM documentation page for [Cloud Quotas roles and permissions](https://cloud.google.com/iam/docs/roles-permissions/cloudquotas).

## May 12,2025

 v1 & v1beta  Feature

You can use custom constraints with Organization Policy to provide more granular control over specific fields for some Cloud Quotas resources. For more information, see [Use custom organization policies](https://cloud.google.com/docs/quotas/custom-constraints). This feature is available in [Preview](https://cloud.google.com/products#product-launch-stages).

## February 03,2025

 v1beta  Feature

Terraform support for quota adjuster is available in [Preview](https://cloud.google.com/products?hl=en#product-launch-stages). For more information, see [Terraform support for Cloud Quotas](https://cloud.google.com/docs/quotas/terraform-support-for-cloud-quotas).

## January 30,2025

 v1beta  Feature

Quota adjuster is available in [Preview](https://cloud.google.com/products#product-launch-stages) via the [API](https://cloud.google.com/docs/quotas/reference/rest/v1beta/projects.locations.quotaAdjusterSettings), [gcloud quotas beta](https://cloud.google.com/sdk/gcloud/reference/beta/quotas/adjuster/settings) CLI and [Cloud Client Libraries](https://cloud.google.com/docs/quotas/reference/libraries). For more information, see the documentation about how to [enable the quota adjuster](https://cloud.google.com/docs/quotas/quota-adjuster#enable) for a project through the Cloud Quotas API.

  v1beta  Feature

The following [Google Cloud CLI command](https://cloud.google.com/sdk/gcloud/reference/beta/quotas/adjuster/settings) is available in beta:

- `gcloud beta quotas adjuster settings`

For more information, see [View quotas using the gcloud beta CLI](https://cloud.google.com/docs/quotas/gcloud-cli-examples).

## January 17, 2025

 v1beta  Feature

The following [Google Cloud CLI commands](https://cloud.google.com/sdk/gcloud/reference/beta/quotas) are available in beta:

- `gcloud beta quotas info`
- `gcloud beta quotas preferences`

For more information, see [View quotas using the gcloud beta CLI](https://cloud.google.com/docs/quotas/gcloud-cli-examples).

## July 12, 2024

 v1  Feature

The Ongoing rollouts feature is generally available ([GA](https://cloud.google.com/products#product-launch-stages)). For more information, see View ongoing rollouts.

## June 18, 2024

 v1  Feature

The following [Google Cloud CLI commands](https://cloud.google.com/sdk/gcloud/reference/alpha/quotas) are available in alpha:

- `gcloud alpha quotas info`
- `gcloud alpha quotas preferences`

For more information, see [View quotas using the gcloud alpha CLI](https://cloud.google.com/docs/quotas/gcloud-cli-examples).

## May 01, 2024

 v1  Feature

The Quota adjuster feature is generally available ([GA](https://cloud.google.com/products#product-launch-stages)). For more information, see the Cloud Quotas documentation about [Quota adjuster](https://cloud.google.com/docs/quotas/quota-adjuster).

## April 29, 2024

 v1  Feature

Cloud Quotas support for [VPC Service Controls](https://cloud.google.com/docs/quotas/configure-vpc-service-controls) is generally available ([GA](https://cloud.google.com/products#product-launch-stages)).

## April 10, 2024

 v1  Feature

Cloud Quotas support for [Terraform](https://cloud.google.com/docs/quotas/terraform-support-for-cloud-quotas) is generally available ([GA](https://cloud.google.com/products#product-launch-stages)).

## March 25, 2024

 v1  Feature

The [Cloud Quotas API](https://cloud.google.com/docs/quotas/api-overview) is generally available ([GA](https://cloud.google.com/products#product-launch-stages)). For more information, see the Cloud Quotas [API overview](https://cloud.google.com/docs/quotas/api-overview) and [REST API reference](https://cloud.google.com/docs/quotas/reference/rest).

## March 14, 2024

 v1  Feature

Cloud Quotas support for VPC Service Controls is available in [Preview](https://cloud.google.com/products?product-launch-stages).

## December 12, 2023

 v1  Feature

The [Cloud Quotas API](https://cloud.google.com/docs/quotas/api-overview) is available in [Preview](https://cloud.google.com/products#product-launch-stages).

## October 03, 2023

 v1  Feature

The Cloud Quotas [Quota adjuster](https://cloud.google.com/docs/quotas/quota-adjuster) feature is available in [Preview](https://cloud.google.com/products#product-launch-stages).

     Was this helpful?

---

# Set the quota projectStay organized with collectionsSave and categorize content based on your preferences.

> How to set the quota project for client-based APIs

# Set the quota projectStay organized with collectionsSave and categorize content based on your preferences.

This document describes how to set a quota project for your
[client-based APIs.](https://cloud.google.com/docs/quotas/quota-project#project-client-based)
For information about what the quota project
is, how to set the quota API, and how the quota project is determined,
see [About the quota project.](https://cloud.google.com/docs/quotas/quota-project)

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

There are several ways to set quota projects. If the quota project is specified
by more than one method, the following precedence is applied:

1. Programmatically
2. Environment variable
3. Credentials used to authenticate the request

## Set the quota project programmatically

You can explicitly set the quota project in your application. This method
overrides all other definitions. The [principal](https://cloud.google.com/docs/authentication#principal)
used to authenticate the request must have the required permission on the
specified quota project.

How you set the quota project programmatically depends on whether
you're using a client library, the gcloud CLI, or REST API request.

### Client library

You can set the value for the quota project by using client options when you
create the client. This method works well if you want to control the value for
your quota project from your application, regardless of what environment it's
running in.

For more information about implementing client options, see your client library
documentation.

### gcloud CLI

You can set the quota project for all gcloud CLI commands by using
the `billing/quota_project` property in your gcloud CLI configuration. You can
also set the quota project for a specific command by using the `--billing-project`
flag, which takes precedence over the configuration property.

For more information about `gcloud` CLI configurations, see the
[gcloud configdocumentation](https://cloud.google.com/sdk/gcloud/reference/config).
For more information about the `--billing-project` flag, see the
[--billing-projectdocumentation](https://cloud.google.com/sdk/gcloud/reference#--billing-project).

### REST request

You can specify the quota project in a REST request using the
[x-goog-user-projectheader.](https://cloud.google.com/apis/docs/system-parameters#definitions)
The principal making the request must have the required permissions on the quota
 project.

For more information and sample code, see
[Set the quota project with a REST request](https://cloud.google.com/docs/authentication/rest#set-billing-project).

## Set the quota project using an environment variable

Client libraries for some languages support setting the quota project using an
environment variable. This approach can be helpful if you want to set the quota
project differently in different shells, or to override the quota project
associated with the credential. The principal for any request must have the
required permissions on the quota project specified by the environment variable.

The environment variable is language dependent:

| Language | Environment variable |
| --- | --- |
| C++ | GOOGLE_CLOUD_CPP_USER_PROJECT |
| C# | GOOGLE_CLOUD_QUOTA_PROJECT |
| Go | GOOGLE_CLOUD_QUOTA_PROJECT |
| Java | GOOGLE_CLOUD_QUOTA_PROJECT |
| Node.js | GOOGLE_CLOUD_QUOTA_PROJECT |
| Python | GOOGLE_CLOUD_QUOTA_PROJECT |
| PHP | GOOGLE_CLOUD_QUOTA_PROJECT |
| Ruby | Not available |

## Set the quota project using authentication credentials

If the quota project isn't specified, the authentication libraries try to
determine it from the credentials that were used for the request. This process
depends on the type of credentials that were used to authenticate the request:

- **Service account** – The project associated with the service account is
  used as the quota project.
- **User credentials** – For a local development environment,
  [Application Default Credentials](https://cloud.google.com/docs/authentication/application-default-credentials)
  finds your user credentials from the local ADC file. That file can also specify
  a quota project. If you have the project set in your Google Cloud CLI config, and you
  have the required permissions on that project, the quota project is set by
  default when you create the local ADC file. You can also set the ADC quota
  project by using the
  [auth application-default set-quota-projectcommand.](https://cloud.google.com/sdk/gcloud/reference/auth/application-default/set-quota-project)
- **API keys** – When you use an API key to provide credentials for a request,
  the project associated with the API key is used as the quota project.

## Permissions required to set and use the quota project

To get the permission that
      you need to set a project as the quota project, or use that quota project in a request,

      ask your administrator to grant you the

      [Service Usage Consumer](https://cloud.google.com/iam/docs/roles-permissions/serviceusage#serviceusage.serviceUsageConsumer) (`roles/serviceusage.serviceUsageConsumer`)
     IAM role on the project.

  For more information about granting roles, see [Manage access to projects, folders, and organizations](https://cloud.google.com/iam/docs/granting-changing-revoking-access).

This predefined role contains the
        ` serviceusage.services.use`
        permission,
         which is required to
        set a project as the quota project, or use that quota project in a request.

You might also be able to get
          this permission
        with [custom roles](https://cloud.google.com/iam/docs/creating-custom-roles) or
        other [predefined roles](https://cloud.google.com/iam/docs/roles-overview#predefined).

If you use a project you created as your quota project, you have the necessary
permissions.

For more information about permissions, see [Quota permissions](https://cloud.google.com/docs/quotas/permissions).

## Set the quota user

Some APIs also limit the number of requests per user, which is different from
the per project quotas described in prior sections of this document.

By default, the system uses the authenticated principal. If there is no
authenticated principal, the system uses the client IP address.

If you need to override the quota user, you can set the `quotaUser` parameter
through the Cloud API [System parameters](https://cloud.google.com/apis/docs/system-parameters). If you
do specify a `quotaUser` or `X-Goog-Quota-User`, a valid API key with IP address
restrictions must be used to identify the quota project. Otherwise, the
`quotaUser` parameter is ignored.

To learn more about Cloud API system parameters and their definitions, see the
system parameters [definitions table](https://cloud.google.com/apis/docs/system-parameters#definitions).

## What's next

- About the [quota project](https://cloud.google.com/docs/quotas/quota-project)
- Learn more about [Application Default Credentials](https://cloud.google.com/docs/authentication/application-default-credentials)
- Get more information about [authentication](https://cloud.google.com/docs/authentication)
- Understand [quotas](https://cloud.google.com/docs/quotas/overview)

   Was this helpful?

---

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

# Quota and system limit terminologyStay organized with collectionsSave and categorize content based on your preferences.

> Understand the terminology that Google Cloud uses to describe quotas and system limits.

# Quota and system limit terminologyStay organized with collectionsSave and categorize content based on your preferences.

Quotas and system limits restrict your use of Google Cloud resources to
support resource availability for all Google Cloud users. Quotas have default
values, and can typically be adjusted. System limits are fixed values that
cannot be changed.

The following table lists additional quota terminology and definitions.

| Term | Description |
| --- | --- |
| Dimension | A dimension is an attribute that represents a region or a zone, or a service-specific dimension, such asgpu_familyornetwork_id.The Cloud Quotas API represents dimensions as key-value pairs, where the key is the dimension name, and the value is the value of the named dimension—for example, {"key" : "region", "value" : "us-central1"}. |
| Quota | Usually,quotarefers to a Google Cloud resource and its
      unit of measurement. For example, the quotaCPUS-PER-VM-FAMILY-per-project-regiondefines the
      number of Compute Engine virtual CPUs (vCPUs) available to your
      project for a specific VM family in a particular region. Occasionally,
      Google Cloud documentation uses the wordquotain its more
      general sense, meaning a limited allowance. |
| Quota adjustment | A request to increase or decrease a quota value. Quota adjustment
    requests are subject to review by Google Cloud. |
| Quota adjuster settings (Preview) | This resource represents your quota adjuster settings for a particular
      project. When enabled, the quota adjuster monitors your usage for the
      specified resources and issues quota adjustment requests when resource
      usage approaches its quota value. |
| Quota info | QuotaInfois a read-only resource that provides metadata and quota value information about a particular quota for a given project, folder or organization. TheQuotaInforesource contains:Metadata such as name and dimension.Quota values for different quota dimensions.Cloud Quotas obtains information from the quotas defined by Google Cloud services and any fulfilled quota adjustments that you initiate.Note: BecauseQuotaInfois constructed by incorporating information from different sources, a default quota configuration exists even if you have not created aQuotaPreferenceresource. Until you express a preferred state throughquotaPreference.createorquotaPreference.update,QuotaInforelies on the default quota information available to determine what quota value to enforce. |
| Quota preference | AQuotaPreferenceresource represents your quota
    preferences for a particular dimension combination. You can use this
    resource to make quota adjustments requests and specify behavior for
    adjustment requests. You can set quota preferences by using the
    Google Cloud console, the Cloud Quotas API, or the
    Google Cloud CLI. |
| Quota value | The maximum for a given quota. This value can be adjusted for most
    quotas. |
| System limit | A fixed value; typically, an architectural constraint. System limits cannot be adjusted. |

---

# Terraform support for Cloud QuotasStay organized with collectionsSave and categorize content based on your preferences.

# Terraform support for Cloud QuotasStay organized with collectionsSave and categorize content based on your preferences.

[Terraform](https://www.terraform.io/)
is an Infrastructure as code (IaC) tool that you can use to provision resources
and permissions for Cloud Quotas. To learn how to use Terraform
to provision infrastructure on Google Cloud, refer to the
[Terraform on Google Cloud documentation](https://cloud.google.com/docs/terraform).

You can use Terraform to do the following with Cloud Quotas:

- Retrieve the `QuotaInfo` data source of a quota for a project, folder or
  organization.
- List `QuotaInfos` data source of all quotas for a given project, folder or
  organization.
- Create a new, or update an existing, `QuotaPreference` quota configuration
  that specifies the preferred value for a quota.

## Before you begin

Before you begin, you need access to Terraform:

- If you're getting started, note that [Cloud Shell](https://cloud.google.com/shell/docs) has
  Terraform already integrated, and you can follow this step by step
  tutorial,
  [Deploy a basic Flask web server](https://cloud.google.com/docs/terraform/get-started-with-terraform)
  using Terraform and Cloud Shell.
- If you'd prefer to install Terraform yourself, see HashiCorp's
  [Terraform installation instructions](https://developer.hashicorp.com/terraform/tutorials/gcp-get-started/install-cli).

To use Terraform with Cloud Quotas,
[create a configuration file](https://developer.hashicorp.com/terraform/language)
to describe your infrastructure, and then
[apply the configuration file](https://developer.hashicorp.com/terraform/cli/commands/apply)
to create an execution plan and perform operations to provision your
infrastructure.

## Terraform resources and data sources

The following lists contain links to Cloud Quotas Terraform
resources and data source samples that appear in the
[Terraform registry](https://registry.terraform.io/providers/hashicorp/google/latest/docs/).

### Resources

Cloud Quotas provides the following Terraform resources:

- [google_cloud_quotas_quota_preference](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/cloud_quotas_quota_preference)
- [google_cloud_quotas_quota_adjuster_settings](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/cloud_quotas_quota_adjuster_settings) ([Preview](https://cloud.google.com/products#product-launch-stages))

### Data sources

Cloud Quotas provides the following Terraform data sources:

- [google_cloud_quotas_quota_info](https://registry.terraform.io/providers/hashicorp/google/latest/docs/data-sources/cloud_quotas_quota_info)
- [google_cloud_quotas_quota_infos](https://registry.terraform.io/providers/hashicorp/google/latest/docs/data-sources/cloud_quotas_quota_infos)

## What's next

Learn more about Terraform:

- [What is Terraform?](https://developer.hashicorp.com/terraform/intro)
- [Terraform Developer website](https://developer.hashicorp.com/terraform/)
- [Terraform Language Documentation](https://developer.hashicorp.com/terraform/language)
- [Terraform CLI Documentation](https://developer.hashicorp.com/terraform/cli)

   Was this helpful?
