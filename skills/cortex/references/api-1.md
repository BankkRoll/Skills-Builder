# API Keys and more

# API Keys

### Required permissions

## Operations

### List API keys

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

pageSizeinteger · int32Required

Number of results to return per page, between 1 and 1000. Default 250.

Default:  `250`pageinteger · int32Required

Page number to return, 0-indexed. Default 0.

Default:  `0`200

Successfully found API keys

application/jsonapplication/yaml400

Bad request

application/jsonapplication/yaml429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Get API key

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

cidstringRequired

The unique, auto-generated identifier for the API key

Example: `ak1234567890abcdef`200

Successfully found API key

application/jsonapplication/yaml400

Bad request

application/jsonapplication/yaml404

API key not found

application/jsonapplication/yaml429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Create API key

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

descriptionstringOptional

Description of the API key

Example: `API Key used for entities scanner script`expirationDatestring · date-timeOptional

Expiration date of the API key. Format: ISO8601 with timezone offset

namestringRequired

Name of the API key

Example: `Entities scanner`200

Successfully created API key

application/jsonapplication/yaml400

Bad request

application/jsonapplication/yaml403

Access denied

application/jsonapplication/yaml429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Update API key

putAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

cidstringRequired

The unique, auto-generated identifier for the API key

Example: `ak1234567890abcdef`descriptionstringOptional

Description of the API key

Example: `API Key used for entities scanner script`namestringRequired

Name of the API key

Example: `Entities scanner`200

Successfully updated API key

application/jsonapplication/yaml400

Bad request

application/jsonapplication/yaml403

Access denied

application/jsonapplication/yaml404

API key not found

application/jsonapplication/yaml429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Delete API key

deleteAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

cidstringRequired

The unique, auto-generated identifier for the API key

Example: `ak1234567890abcdef`200

Successfully deleted API key

```
No content
```

400

Bad request

application/jsonapplication/yaml403

Access denied

application/jsonapplication/yaml404

API key not found

application/jsonapplication/yaml429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$

```
No content
```

Last updated 2 months ago

Was this helpful?

---

# Audit Logs

### Required permissions

### Retrieve audit logs

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

startTimestring · date-timeOptionalendTimestring · date-timeOptionalpageinteger · int32Required

Page number to return, 0-indexed. Default 0.

Default:  `0`pageSizeinteger · int32Required

Number of results to return per page, between 1 and 1000. Default 250.

Default:  `250`objectIdentifiersstring[]OptionalobjectTypesstring · enumOptional

Filter by Cortex object types (CATALOG, SERVICE, TEAM, SCORECARD, etc), integration configurations (AWS_CONFIGURATION, BITBUCKET_CONFIGURATION, etc), and more.

Possible values :  actorApiKeyIdentifiersstring[]OptionalactorEmailsstring[]OptionalactorIpAddressesstring[]OptionalactorRequestTypesstring · enumOptionalPossible values :  200

Successfully retrieved audit logs

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

Last updated 2 months ago

Was this helpful?

---

# Catalog Entities

### Required permissions

-
-
-

## Operations

### List entities

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

groupsstring[]Optional

Filter based on groups, which correspond to the `x-cortex-groups` field in the Catalog Descriptor. Accepts a comma-delimited list of groups

Default:  `[]`ownersstring[]Optional

Filter based on owner group names, which correspond to the `x-cortex-owners` field in the Catalog Descriptor. Accepts a comma-delimited list of owner group names

Default:  `[]`hierarchyDepthstringOptional

Depth of the parent / children hierarchy nodes. Can be 'full' or a valid integer

Default:  `full`gitRepositoriesstring[]Optional

Supports only GitHub repositories in the `org/repo` format

Default:  `[]`Example: `cortexapps%2Fbackend,cortexapps%2Ffrontend`includeHierarchyFieldsstring[]Optional

List of sub fields to include for hierarchies. Only supports 'groups'

Example: `groups`typesstring[]Optional

Filter the response to specific types of entities. By default, this includes services, resources, and domains. Corresponds to the `x-cortex-type` field in the entity descriptor.

Default:  `[]`Example: `service,rds,s3,domain`querystringOptional

Filter based on a [search query](https://docs.cortex.io/settings/search). This will search across entity properties. If provided, results will be sorted by relevance.

Default:  `""`includeArchivedbooleanOptional

Whether to include archived entities in the response

Default:  `false`includeMetadatabooleanOptional

Whether to include custom data for each entity in the response

Default:  `false`includeLinksbooleanOptional

Whether to include links for each entity in the response

Default:  `false`includeSlackChannelsbooleanOptional

Whether to include Slack channels for each entity in the response

includeOwnersbooleanOptional

Whether to include ownership information for each entity in the response

Default:  `false`includeNestedFieldsstring[]Optional

List of sub fields to include for different types

Example: `team:members`pageSizeinteger · int32Required

Number of results to return per page, between 1 and 1000. Default 250.

Default:  `250`pageinteger · int32Required

Page number to return, 0-indexed. Default 0.

Default:  `0`200

Successfully found entities

application/json400

Invalid filters

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### List entity descriptors

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

yamlbooleanOptional

When true, returns the YAML representation of the descriptors

typesstring[]Optional

Filter the response to specific types of entities. By default, this includes services, resources, and domains. Corresponds to the `x-cortex-type` field in the entity descriptor.

Example: `service,rds,s3,domain`pageSizeinteger · int32Required

Number of entities to return per page

pageinteger · int32Required

Page number to return, 0 indexed

200

Successfully retrieved entity descriptors

application/jsonResponseone ofor429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Retrieve entity details

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

hierarchyDepthstringOptional

Depth of the parent / children hierarchy nodes. Can be 'full' or a valid integer

Default:  `full`includeHierarchyFieldsstring[]Optional

List of sub fields to include for hierarchies. Only supports 'groups'

Example: `groups`includeOwnersbooleanOptional

Include ownership information, default is true

200

Successfully found entity

application/json404

Entity not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Retrieve most recent GitOps log for entity

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

200

Retrieve most recent GitOps log for entity

application/json404

Entity GitOps log not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Retrieve entity descriptor

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

yamlbooleanOptional

When true, returns the YAML representation of the descriptor

200

Successfully found entity descriptor

application/jsonResponseone ofstringOptionalorobjectOptional404

Entity not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Retrieve entity Scorecard scores

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

200

All entity Scorecard scores

application/json404

Entity not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Create or update entity

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

dryRunbooleanOptional

When true, this endpoint only validates the descriptor contents and returns any errors or warnings.

githubPullRequestinteger · int32Optional

Add a comment with validation errors on the pull request with the given ID

modestring · enumOptional

Mode of operation: UPSERT (default) creates or updates existing entity, CREATE fails if entity already exists.

Possible values :  anyOptional200

Indicates that the entity was accepted and processed successfully

application/json400

Invalid YAML (major errors or incorrectly formatted YAML)

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Archive an entity

putAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

200

Successfully archived entity

application/json404

Entity not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Unarchive an entity

putAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

200

Successfully unarchived entity

application/json404

Entity not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Create or patch entity

patchAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

dryRunbooleanOptional

When true, this endpoint only validates the descriptor contents and returns any errors or warnings.

deleteMarkerValuestringOptional

Delete keys with this value from the merged yaml, e.g. `__delete__`, if any values match this, they will not be included in merged YAML. For example `my_value: __delete__` will remove `my_value` from the merged YAML.

appendArraysbooleanOptional

Default merge behavior is to replace arrays, set this to true to append arrays instead. For simple types, duplicate values will be removed from the merged array.

failIfEntityDoesNotExistbooleanOptional

Default behavior is to upsert the entity, set `failIfEntityDoesNotExist=true` to fail (404) if the entity specified in `x-cortex-tag` does not exist.

anyOptional200

Indicates that the entity body was accepted, and the referenced `x-cortex-tag` existed and patched successfully

application/json201

Indicates that the entity body was accepted, and the referenced `x-cortex-tag` did not exist and was created successfully

application/json400

Invalid YAML (major errors or incorrectly formatted YAML)

application/json404

Specified entity does not exist (when failIfDoesNotExist is set to true)

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Delete entity

deleteAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

200

Successfully deleted entity

```
No content
```

404

Entity not found

application/json405

Entity delete is not allowed

429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$

```
No content
```

### Delete entities by type

deleteAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

typesstring[]Optional

A list of entity types or IDs delete

idsstring[]Optional200

Successfully deleted entities

```
No content
```

400

Invalid filters

application/json405

Entity delete is not allowed

429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$

```
No content
```

Last updated 2 months ago

Was this helpful?

---

# Custom Data (Advanced)

### Retrieve custom data for entity

get

Use this endpoint when attempting to delete custom data where the key contains non-alphanumeric characters. Otherwise, use the standard API under `Custom Data`.

AuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagstringRequired

Entity tag (x-cortex-tag), supports non-alphanumeric characters

keystringOptional

When set, returns the entity's value at this key. Otherwise, returns all custom data key/values for the entity.

200

Successfully retrieved custom data

application/json404

Entity not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Add custom data for entity

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagstringRequiredforcebooleanOptional

When true, overrides values that were defined in the catalog descriptor. Will be overwritten the next time the catalog descriptor is processed.

anyOptional200

Successfully created data

application/json400

Invalid custom data request

application/json404

Entity not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Delete custom data by key for entity

delete

Use this endpoint when attempting to delete custom data where the key contains non-alphanumeric characters. Otherwise, use the standard API under `Custom Data`.

AuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagstringRequiredkeystringRequiredforcebooleanOptional200

Successfully deleted custom data

404

Entity not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$

```
No content
```

Was this helpful?

---

# Custom Data

### Required permissions

## Operations

### List custom data for entity

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

pageSizeinteger · int32Required

Number of results to return per page, between 1 and 1000. Default 250.

Default:  `250`pageinteger · int32Required

Page number to return, 0-indexed. Default 0.

Default:  `0`200

Successfully retrieved custom data. If using pagination, we do not return page, total, or totalPages in the response.  An empty array is returned once you reach the end.

application/json404

Entity not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Retrieve custom data for entity

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagstringRequired

Entity tag (x-cortex-tag), supports non-alphanumeric characters

keystringOptional

When set, returns the entity's value at this key. Otherwise, returns all custom data key/values for the entity.

200

Successfully retrieved custom data

application/json404

Entity not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Retrieve custom data for entity by key

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

keystringRequired200

Successfully retrieved custom data for key

application/json404

Custom data not found for given entity and key

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Add custom data for entity

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

forcebooleanOptional

When true, overrides values that were defined in the catalog descriptor. Will be overwritten the next time the catalog descriptor is processed.

stringOptional200

Successfully created data

application/json400

Invalid custom data request

application/json404

Entity not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Add custom data via webhook

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

uuidstringRequiredobjectOptional200

OK

```
No content
```

429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$

```
No content
```

### Add custom data in bulk

putAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

forcebooleanOptional

When true, overrides values that were defined in the catalog descriptor. Will be overwritten the next time the catalog descriptor is processed.

anyOptional200

Successfully created/updated custom data

application/json400

Invalid custom data request

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Delete custom data for entity

deleteAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

keystringRequiredforcebooleanOptional

When true, overrides values that were defined in the catalog descriptor. Will be overwritten the next time the catalog descriptor is processed.

200

Successfully deleted custom data

```
No content
```

404

Entity not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$

```
No content
```

### Delete custom data by key for entity

deleteAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagstringRequiredkeystringRequiredforcebooleanOptional200

Successfully deleted custom data

```
No content
```

404

Entity not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$

```
No content
```

Last updated 2 months ago

Was this helpful?

---

# Custom Events

### Required permissions

## Operations

### List custom events for entity

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

typestringOptionaltimestampstring · date-timeOptionalDeprecated

Use 'startTime' instead

startTimestring · date-timeOptional

If provided, events with greater than or equal to timestamp will be returned (a date-time without a time-zone in the ISO-8601 calendar system)

endTimestring · date-timeOptional

If provided, events with less than or equal to timestamp will be returned (a date-time without a time-zone in the ISO-8601 calendar system)

pageSizeinteger · int32Required

Number of results to return per page, between 1 and 1000. Default 250.

Default:  `250`pageinteger · int32Required

Page number to return, 0-indexed. Default 0.

Default:  `0`200

Successfully retrieved custom events

application/json400

Bad Request

application/json404

Entity not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Retrieve custom event by UUID

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

uuidstring · uuidRequired200

Successfully retrieved custom event

application/json400

Bad Request

application/json404

Entity or custom event not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Create custom event for entity

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

descriptionstringOptional

Optional description of custom event

timestampstring · date-timeRequired

Time when event occurred

titlestringRequired

Name for custom event

Example: `Created K8s pod`typestringRequired

Type of custom event

Example: `POD_CREATION`urlstringOptional

Optional URL associated with custom event

Example: `https://cortex.io`200

Successfully created custom event

application/json400

Bad Request

application/json404

Entity not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Update custom event by UUID

putAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

uuidstring · uuidRequireddescriptionstringOptional

Optional description of custom event

timestampstring · date-timeRequired

Time when event occurred

titlestringRequired

Name for custom event

Example: `Created K8s pod`typestringRequired

Type of custom event

Example: `POD_CREATION`urlstringOptional

Optional URL associated with custom event

Example: `https://cortex.io`200

Successfully updated custom event

application/json400

Bad Request

application/json404

Entity or custom event not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Delete ALL custom events for an entity

deleteAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

typestringOptionaltimestampstring · date-timeOptionalDeprecated

Use 'startTime' instead

startTimestring · date-timeOptional

If provided, events with greater than or equal to timestamp will be deleted (a date-time without a time-zone in the ISO-8601 calendar system)

endTimestring · date-timeOptional

If provided, events with less than or equal to timestamp will be deleted (a date-time without a time-zone in the ISO-8601 calendar system)

200

Successfully deleted custom events

```
No content
```

204

No Content

400

Bad Request

404

Entity not found

429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$

```
No content
```

### Delete custom events by UUID

deleteAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

uuidstring · uuidRequired200

Successfully deleted custom event

```
No content
```

204

No Content

400

Bad Request

404

Entity or custom event not found

429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$

```
No content
```

Was this helpful?

---

# Custom Metrics

### Required permissions

## Operations

### Retrieve custom metrics data points

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

customMetricKeystringRequired

Key for the custom metric filter

tagOrIdstringRequired

Entity identifier - can be a tag or CID

startDatestring · date-timeOptional

Start date for the filter (inclusive). Default: 6 months

endDatestring · date-timeOptional

End date for the filter (inclusive)

pageSizeinteger · int32Required

Number of results to return per page, between 1 and 1000. Default 250.

Default:  `250`pageinteger · int32Required

Page number to return, 0-indexed. Default 0.

Default:  `0`200

Successfully retrieved custom metrics data points

application/json400

Invalid filters

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Add custom metrics data point

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

customMetricKeystringRequired

Key for the custom metric filter

tagOrIdstringRequired

Entity identifier - can be a tag or CID

Data point to be added

timestampstring · date-timeOptional

Timestamp for the data point. Note: It can't be earlier than 6 months

valuenumber · doubleRequired

Value for the data point

200

Successfully added data point

```
No content
```

400

Invalid filters

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$

```
No content
```

### Add custom metrics data points in bulk

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

customMetricKeystringRequired

Key for the custom metric filter

tagOrIdstringRequired

Entity identifier - can be a tag or CID

Data points to be added

200

Successfully added data points

```
No content
```

400

Invalid filters

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$

```
No content
```

### Delete custom metrics data points

deleteAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

customMetricKeystringRequired

Key for the custom metric filter

tagOrIdstringRequired

Entity identifier - can be a tag or CID

startDatestring · date-timeRequired

Start date for the deletion (inclusive)

endDatestring · date-timeRequired

End date for the deletion (inclusive)

204

Successfully deleted data points

400

Invalid filters

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$

```
No content
```

Last updated 2 months ago

Was this helpful?

---

# Dependencies

### Required permissions

## Operations

### Retrieve all dependencies for an entity

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

callerTagstringRequiredincludeOutgoingbooleanOptionalDefault:  `true`includeIncomingbooleanOptionalDefault:  `false`pageSizeinteger · int32Required

Number of results to return per page, between 1 and 1000. Default 250.

Default:  `250`pageinteger · int32Required

Page number to return, 0-indexed. Default 0.

Default:  `0`200

Successfully found entity dependencies

application/json404

Entity dependencies not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Retrieve dependency between entities

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

callerTagstringRequiredcalleeTagstringRequiredmethodstringOptionalpathstringOptional200

Successfully found dependency

application/json400

Invalid endpoint

application/json404

Dependency not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Create dependency from entity

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

callerTagstringRequired

The entity tag (x-cortex-tag) for the callee entity ("from" entity)

calleeTagstringRequired

The entity tag (x-cortex-tag) for the caller entity ("to" entity)

methodstringOptional

HTTP Method

Example: `POST`pathstringOptionaldescriptionstringOptionalmetadataobjectOptional201

Successfully created dependency

application/json400

Invalid endpoint

application/json404

Entity not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Create or update dependencies in bulk

putAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

200

Successfully created / updated dependencies

application/json400

Cannot modify dependency that is defined in cortex.yaml

application/json404

Entity not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Update dependency between entities

putAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

callerTagstringRequiredcalleeTagstringRequiredmethodstringOptionalpathstringOptionaldescriptionstringRequiredmetadataobjectRequired200

Successfully updated dependency

application/json400

Invalid endpoint

application/json404

Entity not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Delete dependency

deleteAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

callerTagstringRequiredcalleeTagstringRequiredmethodstringOptionalpathstringOptional204

Successfully deleted dependency

application/json400

Invalid endpoint

application/json404

Dependency not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Delete dependencies from entity

deleteAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

callerTagstringRequired204

Successfully deleted dependencies

application/json404

Caller not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Delete dependencies in bulk

deleteAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

204

Successfully deleted dependencies

400

Cannot modify dependency that is defined in cortex.yaml

application/json404

Entity not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$

```
No content
```

Last updated 2 months ago

Was this helpful?

---

# Deploys

### Required permissions

## Operations

### List deployments for entity

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

pageSizeinteger · int32Required

Number of results to return per page, between 1 and 1000. Default 250.

Default:  `250`pageinteger · int32Required

Page number to return, 0-indexed. Default 0.

Default:  `0`200

Successfully retrieved deployments

application/json404

Entity not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Add deployment for entity

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

environmentstringOptionalshastringOptionaltimestampstring · date-timeRequiredtitlestringRequiredtypestring · enumRequiredPossible values :  urlstringOptional200

Successfully created deployment

application/json404

Entity not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Update deployment by UUID

putAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

uuidstring · uuidRequiredenvironmentstringOptionalshastringOptionaltimestampstring · date-timeRequiredtitlestringRequiredtypestring · enumRequiredPossible values :  urlstringOptional200

Successfully updated deployment

application/json404

Entity or deployment not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Delete all deployments for all entities

deleteAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

200

Successfully deleted all deployments

application/json400

Bad Request

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Delete deployments for entity

deleteAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

environmentstringOptionalshastringOptionaltypestring · enumOptionalPossible values :  200

Successfully deleted deployments

application/json404

Entity not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Delete deployment by UUID

deleteAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

uuidstring · uuidRequired200

Successfully deleted deployment

application/json404

Entity or deployment not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Delete deploys by filter

deleteAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

environmentstringOptionalshastringOptionaltypestring · enumOptionalPossible values :  200

Successfully deleted deployment

application/json400

Trying to delete deploys without any filters

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

Last updated 2 months ago

Was this helpful?

---

# Discovery Audit

### Required permissions

## Operations

### Retrieve discovery audit report

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

typestring · enumOptional

Filter based on type of the event

Possible values :  sourcestring · enumOptional

Filter based on integration source

Possible values :  includeIgnoredbooleanOptional

Flag to include ignored events in result

Default:  `false`pageSizeinteger · int32Required

Number of results to return per page, between 1 and 1000. Default 250.

Default:  `250`pageinteger · int32Required

Page number to return, 0-indexed. Default 0.

Default:  `0`200

Successfully retrieved discovery audit report

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

Last updated 2 months ago

Was this helpful?

---

# Docs

### Required permissions

## Operations

### Retrieve OpenAPI docs for entity

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

namestringOptional

Name of the OpenAPI spec to return. If you have multiple OpenAPI specs configured for your entity as `x-cortex-links`, use this parameter to ensure the correct spec is returned. If this parameter is not specified, we will return the first OpenAPI spec found.

200

Successfully found documentation

application/json404

Documentation not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Update OpenAPI docs for entity

putAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

specstringRequired

Stringified JSON representation of the OpenAPI spec

200

Successfully updated documentation

application/json400

Invalid request

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Delete OpenAPI docs for entity

deleteAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

204

Successfully deleted documentation

429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$

```
No content
```

Last updated 2 months ago

Was this helpful?
