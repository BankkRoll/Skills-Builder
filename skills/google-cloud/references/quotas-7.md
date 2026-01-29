# Method: folders.locations.quotaPreferences.createStay organized with collectionsSave and categorize content based on your preferences. and more

# Method: folders.locations.quotaPreferences.createStay organized with collectionsSave and categorize content based on your preferences.

# Method: folders.locations.quotaPreferences.createStay organized with collectionsSave and categorize content based on your preferences.

Creates a new QuotaPreference that declares the desired value for a quota.

### HTTP request

`POST https://cloudquotas.googleapis.com/v1/{parent=folders/*/locations/*}/quotaPreferences`

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

# Method: folders.locations.quotaPreferences.getStay organized with collectionsSave and categorize content based on your preferences.

# Method: folders.locations.quotaPreferences.getStay organized with collectionsSave and categorize content based on your preferences.

Gets details of a single QuotaPreference.

### HTTP request

`GET https://cloudquotas.googleapis.com/v1/{name=folders/*/locations/*/quotaPreferences/*}`

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

# Method: folders.locations.quotaPreferences.listStay organized with collectionsSave and categorize content based on your preferences.

# Method: folders.locations.quotaPreferences.listStay organized with collectionsSave and categorize content based on your preferences.

Lists QuotaPreferences in a given project, folder or organization.

### HTTP request

`GET https://cloudquotas.googleapis.com/v1/{parent=folders/*/locations/*}/quotaPreferences`

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

# Method: folders.locations.quotaPreferences.patchStay organized with collectionsSave and categorize content based on your preferences.

# Method: folders.locations.quotaPreferences.patchStay organized with collectionsSave and categorize content based on your preferences.

Updates the parameters of a single QuotaPreference. It can updates the config in any states, not just the ones pending approval.

### HTTP request

`PATCH https://cloudquotas.googleapis.com/v1/{quotaPreference.name=folders/*/locations/*/quotaPreferences/*}`

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

# REST Resource: folders.locations.quotaPreferencesStay organized with collectionsSave and categorize content based on your preferences.

# REST Resource: folders.locations.quotaPreferencesStay organized with collectionsSave and categorize content based on your preferences.

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

### QuotaConfig

The preferred quota configuration.

| JSON representation |
| --- |
| {"preferredValue":string,"stateDetail":string,"grantedValue":string,"traceId":string,"annotations":{string:string,...},"requestOrigin":enum (Origin)} |

| Fields |
| --- |
| preferredValue |
| stateDetail |
| grantedValue |
| traceId |
| annotations |
| requestOrigin |

### Origin

The enumeration of the origins of quota preference requests.

| Enums |
| --- |
| ORIGIN_UNSPECIFIED |
| CLOUD_CONSOLE |
| AUTO_ADJUSTER |

| Methods |
| --- |
| create |
| get |
| list |
| patch |

---

# Method: folders.locations.services.quotaInfos.getStay organized with collectionsSave and categorize content based on your preferences.

# Method: folders.locations.services.quotaInfos.getStay organized with collectionsSave and categorize content based on your preferences.

Retrieve the QuotaInfo of a quota for a project, folder or organization.

### HTTP request

`GET https://cloudquotas.googleapis.com/v1/{name=folders/*/locations/*/services/*/quotaInfos/*}`

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

---

# Method: folders.locations.services.quotaInfos.listStay organized with collectionsSave and categorize content based on your preferences.

# Method: folders.locations.services.quotaInfos.listStay organized with collectionsSave and categorize content based on your preferences.

Lists QuotaInfos of all quotas for a given project, folder or organization.

### HTTP request

`GET https://cloudquotas.googleapis.com/v1/{parent=folders/*/locations/*/services/*}/quotaInfos`

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

           Was this helpful?

---

# REST Resource: folders.locations.services.quotaInfosStay organized with collectionsSave and categorize content based on your preferences.

# REST Resource: folders.locations.services.quotaInfosStay organized with collectionsSave and categorize content based on your preferences.

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

### ContainerType

The enumeration of the types of a cloud resource container.

| Enums |
| --- |
| CONTAINER_TYPE_UNSPECIFIED |
| PROJECT |
| FOLDER |
| ORGANIZATION |

### QuotaIncreaseEligibility

Eligibility information regarding requesting increase adjustment of a quota.

| JSON representation |
| --- |
| {"isEligible":boolean,"ineligibilityReason":enum (IneligibilityReason)} |

| Fields |
| --- |
| isEligible |
| ineligibilityReason |

### IneligibilityReason

The enumeration of reasons when it is ineligible to request increase adjustment.

| Enums |
| --- |
| INELIGIBILITY_REASON_UNSPECIFIED |
| NO_VALID_BILLING_ACCOUNT |
| NOT_SUPPORTED |
| NOT_ENOUGH_USAGE_HISTORY |
| OTHER |

### DimensionsInfo

The detailed quota information such as effective quota value for a combination of dimensions.

| JSON representation |
| --- |
| {"dimensions":{string:string,...},"details":{object (QuotaDetails)},"applicableLocations":[string]} |

| Fields |
| --- |
| dimensions |
| details |
| applicableLocations[] |

### QuotaDetails

The quota details for a map of dimensions.

| JSON representation |
| --- |
| {"value":string,"rolloutInfo":{object (RolloutInfo)}} |

| Fields |
| --- |
| value |
| rolloutInfo |

### RolloutInfo

[Output only] Rollout information of a quota.

| JSON representation |
| --- |
| {"ongoingRollout":boolean} |

| Fields |
| --- |
| ongoingRollout |

| Methods |
| --- |
| get |
| list |

     Was this helpful?

---

# ListQuotaInfosResponseStay organized with collectionsSave and categorize content based on your preferences.

# ListQuotaInfosResponseStay organized with collectionsSave and categorize content based on your preferences.

Message for response to listing QuotaInfos

| JSON representation |
| --- |
| See more code actions.Light code themeDark code theme{"quotaInfos":[{object (QuotaInfo)}],"nextPageToken":string} |

| Fields |
| --- |
| quotaInfos[] |
| nextPageToken |

     Was this helpful?

---

# ListQuotaPreferencesResponseStay organized with collectionsSave and categorize content based on your preferences.

# ListQuotaPreferencesResponseStay organized with collectionsSave and categorize content based on your preferences.

Message for response to listing QuotaPreferences

| JSON representation |
| --- |
| See more code actions.Light code themeDark code theme{"quotaPreferences":[{object (QuotaPreference)}],"nextPageToken":string,"unreachable":[string]} |

| Fields |
| --- |
| quotaPreferences[] |
| nextPageToken |
| unreachable[] |

     Was this helpful?

---

# Method: organizations.locations.quotaPreferences.createStay organized with collectionsSave and categorize content based on your preferences.

# Method: organizations.locations.quotaPreferences.createStay organized with collectionsSave and categorize content based on your preferences.

Creates a new QuotaPreference that declares the desired value for a quota.

### HTTP request

`POST https://cloudquotas.googleapis.com/v1/{parent=organizations/*/locations/*}/quotaPreferences`

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

# Method: organizations.locations.quotaPreferences.getStay organized with collectionsSave and categorize content based on your preferences.

# Method: organizations.locations.quotaPreferences.getStay organized with collectionsSave and categorize content based on your preferences.

Gets details of a single QuotaPreference.

### HTTP request

`GET https://cloudquotas.googleapis.com/v1/{name=organizations/*/locations/*/quotaPreferences/*}`

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

           Was this helpful?

---

# Method: organizations.locations.quotaPreferences.listStay organized with collectionsSave and categorize content based on your preferences.

# Method: organizations.locations.quotaPreferences.listStay organized with collectionsSave and categorize content based on your preferences.

Lists QuotaPreferences in a given project, folder or organization.

### HTTP request

`GET https://cloudquotas.googleapis.com/v1/{parent=organizations/*/locations/*}/quotaPreferences`

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

           Was this helpful?

---

# Method: organizations.locations.quotaPreferences.patchStay organized with collectionsSave and categorize content based on your preferences.

# Method: organizations.locations.quotaPreferences.patchStay organized with collectionsSave and categorize content based on your preferences.

Updates the parameters of a single QuotaPreference. It can updates the config in any states, not just the ones pending approval.

### HTTP request

`PATCH https://cloudquotas.googleapis.com/v1/{quotaPreference.name=organizations/*/locations/*/quotaPreferences/*}`

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

# REST Resource: organizations.locations.quotaPreferencesStay organized with collectionsSave and categorize content based on your preferences.

# REST Resource: organizations.locations.quotaPreferencesStay organized with collectionsSave and categorize content based on your preferences.

## Resource: QuotaPreference

QuotaPreference represents the preferred quota configuration specified for a project, folder or organization. There is only one QuotaPreference resource for a quota value targeting a unique set of dimensions.

| JSON representation |
| --- |
| See more code actions.Light code themeDark code theme{"name":string,"dimensions":{string:string,...},"quotaConfig":{object (QuotaConfig)},"etag":string,"createTime":string,"updateTime":string,"service":string,"quotaId":string,"reconciling":boolean,"justification":string,"contactEmail":string} |

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

# Method: organizations.locations.services.quotaInfos.getStay organized with collectionsSave and categorize content based on your preferences.

# Method: organizations.locations.services.quotaInfos.getStay organized with collectionsSave and categorize content based on your preferences.

Retrieve the QuotaInfo of a quota for a project, folder or organization.

### HTTP request

`GET https://cloudquotas.googleapis.com/v1/{name=organizations/*/locations/*/services/*/quotaInfos/*}`

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

---

# Method: organizations.locations.services.quotaInfos.listStay organized with collectionsSave and categorize content based on your preferences.

# Method: organizations.locations.services.quotaInfos.listStay organized with collectionsSave and categorize content based on your preferences.

Lists QuotaInfos of all quotas for a given project, folder or organization.

### HTTP request

`GET https://cloudquotas.googleapis.com/v1/{parent=organizations/*/locations/*/services/*}/quotaInfos`

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

           Was this helpful?

---

# REST Resource: organizations.locations.services.quotaInfosStay organized with collectionsSave and categorize content based on your preferences.

# REST Resource: organizations.locations.services.quotaInfosStay organized with collectionsSave and categorize content based on your preferences.

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

# Method: projects.locations.quotaPreferences.createStay organized with collectionsSave and categorize content based on your preferences.

# Method: projects.locations.quotaPreferences.createStay organized with collectionsSave and categorize content based on your preferences.

Creates a new QuotaPreference that declares the desired value for a quota.

### HTTP request

`POST https://cloudquotas.googleapis.com/v1/{parent=projects/*/locations/*}/quotaPreferences`

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

`GET https://cloudquotas.googleapis.com/v1/{name=projects/*/locations/*/quotaPreferences/*}`

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

`GET https://cloudquotas.googleapis.com/v1/{parent=projects/*/locations/*}/quotaPreferences`

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

`PATCH https://cloudquotas.googleapis.com/v1/{quotaPreference.name=projects/*/locations/*/quotaPreferences/*}`

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

---

# Method: projects.locations.services.quotaInfos.getStay organized with collectionsSave and categorize content based on your preferences.

# Method: projects.locations.services.quotaInfos.getStay organized with collectionsSave and categorize content based on your preferences.

Retrieve the QuotaInfo of a quota for a project, folder or organization.

### HTTP request

`GET https://cloudquotas.googleapis.com/v1/{name=projects/*/locations/*/services/*/quotaInfos/*}`

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

---

# Method: projects.locations.services.quotaInfos.listStay organized with collectionsSave and categorize content based on your preferences.

# Method: projects.locations.services.quotaInfos.listStay organized with collectionsSave and categorize content based on your preferences.

Lists QuotaInfos of all quotas for a given project, folder or organization.

### HTTP request

`GET https://cloudquotas.googleapis.com/v1/{parent=projects/*/locations/*/services/*}/quotaInfos`

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

# Method: folders.locations.quotaPreferences.createStay organized with collectionsSave and categorize content based on your preferences.

# Method: folders.locations.quotaPreferences.createStay organized with collectionsSave and categorize content based on your preferences.

Creates a new QuotaPreference that declares the desired value for a quota.

### HTTP request

`POST https://cloudquotas.googleapis.com/v1beta/{parent=folders/*/locations/*}/quotaPreferences`

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

# Method: folders.locations.quotaPreferences.getStay organized with collectionsSave and categorize content based on your preferences.

# Method: folders.locations.quotaPreferences.getStay organized with collectionsSave and categorize content based on your preferences.

Gets details of a single QuotaPreference.

### HTTP request

`GET https://cloudquotas.googleapis.com/v1beta/{name=folders/*/locations/*/quotaPreferences/*}`

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

# Method: folders.locations.quotaPreferences.listStay organized with collectionsSave and categorize content based on your preferences.

# Method: folders.locations.quotaPreferences.listStay organized with collectionsSave and categorize content based on your preferences.

Lists QuotaPreferences in a given project, folder or organization.

### HTTP request

`GET https://cloudquotas.googleapis.com/v1beta/{parent=folders/*/locations/*}/quotaPreferences`

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

# Method: folders.locations.quotaPreferences.patchStay organized with collectionsSave and categorize content based on your preferences.

# Method: folders.locations.quotaPreferences.patchStay organized with collectionsSave and categorize content based on your preferences.

Updates the parameters of a single QuotaPreference. It can updates the config in any states, not just the ones pending approval.

### HTTP request

`PATCH https://cloudquotas.googleapis.com/v1beta/{quotaPreference.name=folders/*/locations/*/quotaPreferences/*}`

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

           Was this helpful?

---

# REST Resource: folders.locations.quotaPreferencesStay organized with collectionsSave and categorize content based on your preferences.

# REST Resource: folders.locations.quotaPreferencesStay organized with collectionsSave and categorize content based on your preferences.

## Resource: QuotaPreference

QuotaPreference represents the preferred quota configuration specified for a project, folder or organization. There is only one QuotaPreference resource for a quota value targeting a unique set of dimensions.

| JSON representation |
| --- |
| See more code actions.Light code themeDark code theme{"name":string,"dimensions":{string:string,...},"quotaConfig":{object (QuotaConfig)},"etag":string,"createTime":string,"updateTime":string,"service":string,"quotaId":string,"reconciling":boolean,"justification":string,"contactEmail":string} |

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

### QuotaConfig

The preferred quota configuration.

| JSON representation |
| --- |
| {"preferredValue":string,"stateDetail":string,"grantedValue":string,"traceId":string,"annotations":{string:string,...},"requestOrigin":enum (Origin)} |

| Fields |
| --- |
| preferredValue |
| stateDetail |
| grantedValue |
| traceId |
| annotations |
| requestOrigin |

### Origin

The enumeration of the origins of quota preference requests.

| Enums |
| --- |
| ORIGIN_UNSPECIFIED |
| CLOUD_CONSOLE |
| AUTO_ADJUSTER |

| Methods |
| --- |
| create |
| get |
| list |
| patch |

     Was this helpful?

---

# Method: folders.locations.services.quotaInfos.getStay organized with collectionsSave and categorize content based on your preferences.

# Method: folders.locations.services.quotaInfos.getStay organized with collectionsSave and categorize content based on your preferences.

Retrieve the QuotaInfo of a quota for a project, folder or organization.

### HTTP request

`GET https://cloudquotas.googleapis.com/v1beta/{name=folders/*/locations/*/services/*/quotaInfos/*}`

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

---

# Method: folders.locations.services.quotaInfos.listStay organized with collectionsSave and categorize content based on your preferences.

# Method: folders.locations.services.quotaInfos.listStay organized with collectionsSave and categorize content based on your preferences.

Lists QuotaInfos of all quotas for a given project, folder or organization.

### HTTP request

`GET https://cloudquotas.googleapis.com/v1beta/{parent=folders/*/locations/*/services/*}/quotaInfos`

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

           Was this helpful?

---

# REST Resource: folders.locations.services.quotaInfosStay organized with collectionsSave and categorize content based on your preferences.

# REST Resource: folders.locations.services.quotaInfosStay organized with collectionsSave and categorize content based on your preferences.

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

### ContainerType

The enumeration of the types of a cloud resource container.

| Enums |
| --- |
| CONTAINER_TYPE_UNSPECIFIED |
| PROJECT |
| FOLDER |
| ORGANIZATION |

### QuotaIncreaseEligibility

Eligibility information regarding requesting increase adjustment of a quota.

| JSON representation |
| --- |
| {"isEligible":boolean,"ineligibilityReason":enum (IneligibilityReason)} |

| Fields |
| --- |
| isEligible |
| ineligibilityReason |

### IneligibilityReason

The enumeration of reasons when it is ineligible to request increase adjustment.

| Enums |
| --- |
| INELIGIBILITY_REASON_UNSPECIFIED |
| NO_VALID_BILLING_ACCOUNT |
| NOT_SUPPORTED |
| NOT_ENOUGH_USAGE_HISTORY |
| OTHER |

### DimensionsInfo

The detailed quota information such as effective quota value for a combination of dimensions.

| JSON representation |
| --- |
| {"dimensions":{string:string,...},"details":{object (QuotaDetails)},"applicableLocations":[string]} |

| Fields |
| --- |
| dimensions |
| details |
| applicableLocations[] |

### QuotaDetails

The quota details for a map of dimensions.

| JSON representation |
| --- |
| {"value":string,"rolloutInfo":{object (RolloutInfo)}} |

| Fields |
| --- |
| value |
| rolloutInfo |

### RolloutInfo

[Output only] Rollout information of a quota.

| JSON representation |
| --- |
| {"ongoingRollout":boolean} |

| Fields |
| --- |
| ongoingRollout |

| Methods |
| --- |
| get |
| list |

     Was this helpful?

---

# ListQuotaInfosResponseStay organized with collectionsSave and categorize content based on your preferences.

# ListQuotaInfosResponseStay organized with collectionsSave and categorize content based on your preferences.

Message for response to listing QuotaInfos

| JSON representation |
| --- |
| See more code actions.Light code themeDark code theme{"quotaInfos":[{object (QuotaInfo)}],"nextPageToken":string} |

| Fields |
| --- |
| quotaInfos[] |
| nextPageToken |

     Was this helpful?

---

# ListQuotaPreferencesResponseStay organized with collectionsSave and categorize content based on your preferences.

# ListQuotaPreferencesResponseStay organized with collectionsSave and categorize content based on your preferences.

Message for response to listing QuotaPreferences

| JSON representation |
| --- |
| See more code actions.Light code themeDark code theme{"quotaPreferences":[{object (QuotaPreference)}],"nextPageToken":string,"unreachable":[string]} |

| Fields |
| --- |
| quotaPreferences[] |
| nextPageToken |
| unreachable[] |

     Was this helpful?

---

# Method: organizations.locations.quotaPreferences.createStay organized with collectionsSave and categorize content based on your preferences.

# Method: organizations.locations.quotaPreferences.createStay organized with collectionsSave and categorize content based on your preferences.

Creates a new QuotaPreference that declares the desired value for a quota.

### HTTP request

`POST https://cloudquotas.googleapis.com/v1beta/{parent=organizations/*/locations/*}/quotaPreferences`

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

# Method: organizations.locations.quotaPreferences.getStay organized with collectionsSave and categorize content based on your preferences.

# Method: organizations.locations.quotaPreferences.getStay organized with collectionsSave and categorize content based on your preferences.

Gets details of a single QuotaPreference.

### HTTP request

`GET https://cloudquotas.googleapis.com/v1beta/{name=organizations/*/locations/*/quotaPreferences/*}`

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

           Was this helpful?

---

# Method: organizations.locations.quotaPreferences.listStay organized with collectionsSave and categorize content based on your preferences.

# Method: organizations.locations.quotaPreferences.listStay organized with collectionsSave and categorize content based on your preferences.

Lists QuotaPreferences in a given project, folder or organization.

### HTTP request

`GET https://cloudquotas.googleapis.com/v1beta/{parent=organizations/*/locations/*}/quotaPreferences`

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

# Method: organizations.locations.quotaPreferences.patchStay organized with collectionsSave and categorize content based on your preferences.

# Method: organizations.locations.quotaPreferences.patchStay organized with collectionsSave and categorize content based on your preferences.

Updates the parameters of a single QuotaPreference. It can updates the config in any states, not just the ones pending approval.

### HTTP request

`PATCH https://cloudquotas.googleapis.com/v1beta/{quotaPreference.name=organizations/*/locations/*/quotaPreferences/*}`

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

# REST Resource: organizations.locations.quotaPreferencesStay organized with collectionsSave and categorize content based on your preferences.

# REST Resource: organizations.locations.quotaPreferencesStay organized with collectionsSave and categorize content based on your preferences.

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

---

# Method: organizations.locations.services.quotaInfos.getStay organized with collectionsSave and categorize content based on your preferences.

# Method: organizations.locations.services.quotaInfos.getStay organized with collectionsSave and categorize content based on your preferences.

Retrieve the QuotaInfo of a quota for a project, folder or organization.

### HTTP request

`GET https://cloudquotas.googleapis.com/v1beta/{name=organizations/*/locations/*/services/*/quotaInfos/*}`

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

# Method: organizations.locations.services.quotaInfos.listStay organized with collectionsSave and categorize content based on your preferences.

# Method: organizations.locations.services.quotaInfos.listStay organized with collectionsSave and categorize content based on your preferences.

Lists QuotaInfos of all quotas for a given project, folder or organization.

### HTTP request

`GET https://cloudquotas.googleapis.com/v1beta/{parent=organizations/*/locations/*/services/*}/quotaInfos`

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
