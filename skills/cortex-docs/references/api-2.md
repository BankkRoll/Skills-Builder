# Eng Intel: User Labels and more

# Eng Intel: User Labels

### Required permissions

## Operations

### List user labels

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

pageSizeinteger · int32Required

Number of results to return per page, between 1 and 1000. Default 250.

Default:  `250`pageinteger · int32Required

Page number to return, 0-indexed. Default 0.

Default:  `0`200

Successfully retrieved user labels

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Retrieve user label

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

idstringRequired200

Successfully retrieved user label

application/json404

User label not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Update user label assignments

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

200

Successfully updated user label assignments

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

Last updated 2 months ago

Was this helpful?

---

# Entity Relationship Types (Beta)

### Required permissions

### Operations

### List relationship types

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

pageSizeinteger · int32Required

Number of results to return per page, between 1 and 1000. Default 250.

Default:  `250`pageinteger · int32Required

Page number to return, 0-indexed. Default 0.

Default:  `0`200

Successfully found entity relationship types

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Create relationship type

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

Request to create or update a relationship type

allowCyclesbooleanRequired

Whether cyclical relationships are allowed

Example: `false`createCatalogbooleanRequired

Whether to create a catalog page for this relationship type

Example: `false`definitionLocationstring · enumRequired

Defines where a relationship can be configured in entity descriptors

Example: `BOTH`Possible values :  descriptionstringOptional

Optional description explaining the relationship type

Example: `Defines the component hierarchy`destinationLabelPluralstringOptional

Plural label for destinations in the relationship

Example: `Parts`destinationLabelSingularstringOptional

Singular label for destinations in the relationship

Example: `Part`isSingleDestinationbooleanRequired

Whether an entity can have only one destination for this relationship type

Example: `false`isSingleSourcebooleanRequired

Whether an entity can have only one source for this relationship type

Example: `false`namestringRequired

Human-readable name for the relationship type

Example: `Component Hierarchy`sourceLabelPluralstringOptional

Plural label for sources in the relationship

Example: `Components`sourceLabelSingularstringOptional

Singular label for sources in the relationship

Example: `Component`tagstringRequired

Unique identifier tag for the relationship type

Example: `component-hierarchy`200

Successfully created relationship type

application/json400

Validation error creating relationship type

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Get a relationship type

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

relationshipTypeTagstringRequired200

Successfully found relationship type

application/json404

Relationship type not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Update relationship type

putAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

relationshipTypeTagstringRequired

Request to create or update a relationship type

allowCyclesbooleanRequired

Whether cyclical relationships are allowed

Example: `false`createCatalogbooleanRequired

Whether to create a catalog page for this relationship type

Example: `false`definitionLocationstring · enumRequired

Defines where a relationship can be configured in entity descriptors

Example: `BOTH`Possible values :  descriptionstringOptional

Optional description explaining the relationship type

Example: `Defines the component hierarchy`destinationLabelPluralstringOptional

Plural label for destinations in the relationship

Example: `Parts`destinationLabelSingularstringOptional

Singular label for destinations in the relationship

Example: `Part`isSingleDestinationbooleanRequired

Whether an entity can have only one destination for this relationship type

Example: `false`isSingleSourcebooleanRequired

Whether an entity can have only one source for this relationship type

Example: `false`namestringRequired

Human-readable name for the relationship type

Example: `Component Hierarchy`sourceLabelPluralstringOptional

Plural label for sources in the relationship

Example: `Components`sourceLabelSingularstringOptional

Singular label for sources in the relationship

Example: `Component`tagstringRequired

Unique identifier tag for the relationship type

Example: `component-hierarchy`200

Successfully updated relationship type

application/json400

Validation error updating relationship type

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Delete a relationship type

deleteAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

relationshipTypeTagstringRequired200

Successfully deleted relationship type

```
No content
```

204

No Content

400

Validation error deleting relationship type

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$

```
No content
```

Last updated 2 months ago

Was this helpful?

---

# Entity Relationships (Beta)

### Required permissions

### Operations

### List entity destinations for a relationship type

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

relationshipTypeTagstringRequireddepthstringOptional

Maximum depth to traverse in the relationship hierarchy. Defaults to 1 (i.e., direct relationships only).

Example: `2`includeArchivedbooleanOptional

If true will include relationships that traverse archived entities

Default:  `false`Example: `false`200

Successfully retrieved entity sources

application/json404

Entity or relationship type not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Update direct entity destinations for a given entity

putAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

relationshipTypeTagstringRequiredforcebooleanOptional

When true, overrides values that were defined in the catalog descriptor. Will be overwritten the next time the catalog descriptor is processed.

Updates to entity relationship destinations

destinationsstring[]Required

List of code tags for the entities to add as sources

Example: `["entity-1","entity-2"]`200

Successfully updated entity destinations

application/json400

Relationship validation error

application/json404

Entity or relationship type not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Add direct entity destinations for a given entity

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

relationshipTypeTagstringRequiredforcebooleanOptional

When true, overrides values that were defined in the catalog descriptor. Will be overwritten the next time the catalog descriptor is processed.

Updates to entity relationship destinations

destinationsstring[]Required

List of code tags for the entities to add as sources

Example: `["entity-1","entity-2"]`200

Successfully added entity destinations

application/json400

Relationship validation error

application/json404

Entity or relationship type not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### List entity sources for a relationship type

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

relationshipTypeTagstringRequireddepthstringOptional

Maximum depth to traverse in the relationship hierarchy. Defaults to 1 (i.e., direct relationships only).

Example: `2`includeArchivedbooleanOptional

If true will include relationships that traverse archived entities

Default:  `false`Example: `false`200

Successfully retrieved entity sources

application/json404

Entity or relationship type not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Update direct entity sources for a given entity

putAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

relationshipTypeTagstringRequiredforcebooleanOptional

When true, overrides values that were defined in the catalog descriptor. Will be overwritten the next time the catalog descriptor is processed.

Updates to entity relationship sources

sourcesstring[]Required

List of code tags for the entities to add as sources

Example: `["entity-1","entity-2"]`200

Successfully updated entity sources

application/json400

Relationship validation error

application/json404

Entity or relationship type not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Add direct entity sources for a given entity

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

relationshipTypeTagstringRequiredforcebooleanOptional

When true, overrides values that were defined in the catalog descriptor. Will be overwritten the next time the catalog descriptor is processed.

Updates to entity relationship sources

sourcesstring[]Required

List of code tags for the entities to add as sources

Example: `["entity-1","entity-2"]`200

Successfully added entity sources

application/json400

Relationship validation error

application/json404

Entity or relationship type not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### List entity relationships for a relationship type

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

relationshipTypeTagstringRequiredpageSizeinteger · int32Required

Number of results to return per page, between 1 and 1000. Default 250.

Default:  `250`pageinteger · int32Required

Page number to return, 0-indexed. Default 0.

Default:  `0`200

Successfully retrieved entity relationships

application/json404

Relationship type not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Update entity relationships for a relationship type

putAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

relationshipTypeTagstringRequiredforcebooleanOptional

When true, overrides values that were defined in the catalog descriptor. Will be overwritten the next time the catalog descriptor is processed.

Updates to entity relationships

200

Successfully updated entity relationships

application/json404

Relationship type not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Add entity relationships for a relationship type

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

relationshipTypeTagstringRequiredforcebooleanOptional

When true, overrides values that were defined in the catalog descriptor. Will be overwritten the next time the catalog descriptor is processed.

Updates to entity relationships

200

Successfully added entity relationships

application/json404

Relationship type not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

Last updated 2 months ago

Was this helpful?

---

# Entity Types

### Required permissions

## Operations

### List entity types

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

includeBuiltInbooleanOptional

When true, returns the built-in entity types that Cortex provides, such as `rds` and `s3`. Defaults to false.

pageSizeinteger · int32Required

Number of results to return per page, between 1 and 1000. Default 250.

Default:  `250`pageinteger · int32Required

Page number to return, 0-indexed. Default 0.

Default:  `0`200

Successfully found entity types

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Retrieve entity type

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

typestringRequired200

Successfully found entity types

application/json404

Entity type not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Create entity type

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

descriptionstringOptionaliconTagstringOptionalnamestringOptionalschemaobjectRequiredtypestringRequired200

Successfully created entity type

application/json400

Failed to create entity type

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Update entity type

putAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

typestringRequiredforcebooleanOptional

When true, schema will be updated even if it results in broken schemas for existing entities. Defaults to false.

descriptionstringOptionaliconTagstringOptionalnamestringOptionalschemaobjectRequired200

Successfully updated entity type

application/json400

Failed to update entity type

application/json404

Entity type not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Delete entity type

deleteAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

typestringRequired200

Successfully deleted entity type

```
No content
```

404

Entity type not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$

```
No content
```

Last updated 2 months ago

Was this helpful?

---

# GitOps Logs

### Required permissions

## Operations

### Retrieve GitOps logs

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

filestringOptional

File name the within repository

repositorystringOptional

Repository name as defined in your Git provider

shastringOptional

Commit SHA

errorOnlybooleanOptional

Filter by error only

operationstring · enumOptional

Filter by operation

Possible values :  pageinteger · int32Required

Page number to return, 0-indexed. Default 0.

Default:  `0`pageSizeinteger · int32Required

Number of results to return per page, between 1 and 1000. Default 250.

Default:  `250`fileNamestringOptionalscorecardTagstringRequired

Unique tag for the Scorecard.

workflowTagstringOptionaltagstringRequired

The entity tag (`x-cortex-tag`) that identifies the entity.

200

Retrieve GitOps logs based on given criteria

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

Last updated 2 months ago

Was this helpful?

---

# Groups

### Required permissions

## Operations

### Retrieve groups for entity

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

pageSizeinteger · int32Required

Number of results to return per page, between 1 and 1000. Default 250.

Default:  `250`pageinteger · int32Required

Page number to return, 0-indexed. Default 0.

Default:  `0`200

Successfully retrieved groups

application/json404

Entity not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Add groups to entity

putAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

200

Successfully created group memberships

application/json400

Bad Request

application/json404

Entity not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Delete groups from entity

deleteAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

200

Successfully deleted group memberships

```
No content
```

400

Bad Request

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

# Initiatives

### Required permissions

-
-

## Operations

### List Initiatives

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

includeDraftsbooleanOptional

Whether or not to include draft Initiatives in the response

Default:  `false`includeExpiredbooleanOptional

Whether or not to include expired Initiatives in the response

Default:  `false`pageSizeinteger · int32Required

Number of results to return per page, between 1 and 1000. Default 250.

Default:  `250`pageinteger · int32Required

Page number to return, 0-indexed. Default 0.

Default:  `0`200

Successfully retrieved Initiatives

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Get Initiative

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

cidstringRequired200

Successfully retrieved Initiative

application/json404

Initiative not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Create an Initiative

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

descriptionstringOptional

Optional description of the Initiative

isDraftbooleanRequired

Whether or not the Initiative is a draft

namestringRequired

Name of the Initiative

scorecardTagstringRequired

Tag of the scorecard associated with the Initiative

targetDatestring · dateRequired

Target date for the Initiative to be completed. Must be in the future

200

Successfully created Initiative

application/json400

Bad Request

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Update an Initiative

putAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

cidstringRequireddescriptionstringOptional

Optional description of the Initiative

isDraftbooleanRequired

Whether or not the Initiative is a draft

namestringRequired

Name of the Initiative

scorecardTagstringRequired

Tag of the scorecard associated with the Initiative

targetDatestring · dateRequired

Target date for the Initiative to be completed. Must be in the future

200

Successfully updated Initiative

application/json400

Bad Request

application/json404

Initiative not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Delete Initiative

deleteAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

cidstringRequired200

Successfully deleted Initiative

```
No content
```

404

Initiative not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$

```
No content
```

Last updated 2 months ago

Was this helpful?

---

# AWS API

### Required permissions

## Operations

### List AWS types

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

includeDisabledbooleanOptional

When true, includes all AWS types supported

Default:  `false`pageSizeinteger · int32Required

Number of results to return per page, between 1 and 1000. Default 250.

Default:  `250`pageinteger · int32Required

Page number to return, 0-indexed. Default 0.

Default:  `0`200

Successfully found AWS types

application/json404

AWS types not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Retrieve a configuration

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

accountIdstringRequired200

Successfully found configuration

application/json404

Configuration not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Retrieve configurations

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

200

Successfully found configurations

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Add a single configuration

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

accountIdstringRequired

The account ID for the AWS account

rolestringRequired

The IAM role Cortex would be assuming

200

Successfully added configuration

application/json400

Bad Request

application/json403

Forbidden

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Validate all configurations

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

200

Successfully validated all configurations

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Validate a configuration

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

accountIdstringRequired200

Successfully validated configuration

application/json404

Configuration not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Update configurations

putAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

200

Successfully replaced configurations

application/json400

Bad Request

application/json403

Forbidden

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Update configured AWS types

putAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

200

Successfully replaced AWS types

application/json400

Bad Request

application/json403

Forbidden

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Delete all configurations

deleteAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

200

Successfully deleted configurations

```
No content
```

403

Forbidden

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$

```
No content
```

### Delete a configuration

deleteAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

accountIdstringRequired200

Successfully deleted configuration

```
No content
```

403

Forbidden

application/json404

Configuration not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$

```
No content
```

### Get AWS resource details for an entity

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

200

Successfully retrieved AWS resource details

application/json404

Entity not found or no AWS resource details cached

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

Last updated 19 days ago

Was this helpful?

---

# Azure Active Directory (Entra ID) API

## Operations

### Retrieve a configuration

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

200

Successfully found configuration

application/json400

Bad Request

application/json404

Configuration not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Add a configuration

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

clientIdstringRequiredclientSecretstringRequiredgroupsFilterstringOptionaltenantIdstringRequired200

Successfully added configuration

application/json400

Bad Request

application/json403

Forbidden

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Replace the existing configuration

putAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

clientIdstringRequiredclientSecretstringRequiredgroupsFilterstringOptionaltenantIdstringRequired200

Successfully replaces configuration

application/json400

Bad Request

application/json403

Forbidden

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Validate a configuration

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

200

Successfully validated configuration

application/json404

Configuration not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Delete a configuration

deleteAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

200

Successfully deleted configuration

application/json400

Bad Request

application/json403

Forbidden

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

Last updated 2 months ago

Was this helpful?

---

# Azure DevOps API

### Required permissions

## Operations

### Retrieve configurations

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

200

Successfully found configurations

application/json400

Bad Request

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Retrieve default configuration

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

200

Successfully found default configuration

application/json400

Bad Request

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Retrieve a configuration

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

aliasstringRequired200

Successfully found configuration

application/json400

Bad Request

application/json404

Configuration not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Add a single configuration

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

or200

Successfully added configuration

application/json400

Bad Request

application/json403

Forbidden

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Validate all configurations

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

200

Successfully validated all configurations

application/json404

Configuration not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Add multiple configurations

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

200

Successfully added configurations

application/json403

Forbidden

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Validate a configuration

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

aliasstringRequired200

Successfully validated configuration

application/json404

Configuration not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Update a configuration

putAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

aliasstringRequiredor200

Successfully updated configuration

application/json400

Bad Request

application/json403

Forbidden

application/json404

Configuration not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Delete a configuration

deleteAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

aliasstringRequired200

Successfully deleted configuration

application/json400

Bad Request

application/json403

Forbidden

application/json404

Configuration not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Delete all configurations

deleteAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

200

Successfully deleted all configurations

```
No content
```

400

Bad Request

application/json403

Forbidden

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$

```
No content
```

Last updated 2 months ago

Was this helpful?

---

# Azure Resources API

### Required permissions

## Operations

### List Azure Resources types

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

includeDisabledbooleanOptional

Whether to include disabled Azure Resources types

Default:  `false`pageSizeinteger · int32Required

Number of results to return per page, between 1 and 1000. Default 250.

Default:  `250`pageinteger · int32Required

Page number to return, 0-indexed. Default 0.

Default:  `0`200

Successfully found Azure Resources types

application/json404

Azure Resources types not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Retrieve configurations

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

200

Successfully found configurations

application/json400

Bad Request

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Retrieve default configuration

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

200

Successfully found default configuration

application/json400

Bad Request

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Retrieve a configuration

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

aliasstringRequired200

Successfully found configuration

application/json400

Bad Request

application/json404

Configuration not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Add a single configuration

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

aliasstringRequiredazureTenantIdstringRequiredclientIdstringRequiredclientSecretstringRequiredisDefaultbooleanRequiredsubscriptionIdstringRequired200

Successfully added configuration

application/json400

Bad Request

application/json403

Forbidden

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Validate all configurations

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

200

Successfully validated all configurations

application/json404

Configuration not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Validate a configuration

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

aliasstringRequired200

Successfully validated configuration

application/json404

Configuration not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Add multiple configurations

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

200

Successfully added configurations

application/json403

Forbidden

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Update configured Azure Resources types

putAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

200

Successfully replaced Azure Resources types

application/json400

Bad Request

application/json404

Azure Resources types not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Update a configuration

putAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

aliasstringRequiredaliasstringRequiredazureTenantIdstringOptionalclientIdstringOptionalclientSecretstringOptionalisDefaultbooleanRequiredsubscriptionIdstringOptional200

Successfully updated configuration

application/json400

Bad Request

application/json403

Forbidden

application/json404

Configuration not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Delete all configurations

deleteAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

200

Successfully deleted all configurations

```
No content
```

400

Bad Request

application/json403

Forbidden

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$

```
No content
```

### Delete a configuration

deleteAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

aliasstringRequired200

Successfully deleted configuration

application/json400

Bad Request

application/json403

Forbidden

application/json404

Configuration not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

Last updated 2 months ago

Was this helpful?
