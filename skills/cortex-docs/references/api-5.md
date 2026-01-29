# Scorecards and more

# Scorecards

### Required permissions

-
-
-

## Operations

### List Scorecards

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

showDraftsbooleanOptionalgroupsstring[]Optional

Filter based on groups, which correspond to the `x-cortex-groups` field in the Catalog Descriptor. Accepts a comma-delimited list of groups

entitiesstring[]Optional

Filter based on entity (either tags or CIDs). Accepts a comma-delimited list of entity tag or CIDs, please use only one type of identifier

teamsstring[]Optional

Filter based on team (either tags or CIDs). Accepts a comma-delimited list of team tag or CIDs, please use only one type of identifier

pageinteger · int32Required

Page number to return, 0-indexed. Default 0.

Default:  `0`pageSizeinteger · int32Required

Number of results to return per page, between 1 and 1000. Default 250.

Default:  `250`200

OK

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Retrieve Scorecard scores

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagstringRequired

Unique tag for the Scorecard

Example: `my-production-readiness-checklist`entityTagstringOptional

Entity tag (x-cortex-tag)

pageSizeinteger · int32Required

Number of results to return per page, between 1 and 1000. Default 250.

Default:  `250`pageinteger · int32Required

Page number to return, 0-indexed. Default 0.

Default:  `0`200

Scorecard scores

application/json404

Scorecard not found

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

### Retrieve Scorecard

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagstringRequired

Unique tag for the Scorecard

Example: `my-production-readiness-checklist`200

Successfully retrieved Scorecard

application/json404

Scorecard not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Retrieve Scorecard descriptor

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagstringRequired

Unique tag for the Scorecard

Example: `my-production-readiness-checklist`200

Successfully retrieved Scorecard descriptor

application/jsonResponsestring404

Scorecard not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Retrieve Scorecard shields.io badge

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

scorecardTagstringRequired

Unique tag for the Scorecard.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

200

Shields.io badge

application/json404

Entity or Scorecard not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Retrieve next steps for entity in Scorecard

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagstringRequired

Unique tag for the Scorecard

Example: `my-production-readiness-checklist`entityTagstringRequired

The entity tag (`x-cortex-tag`) that identifies the entity.

200

Any rules remaining for the entity to reach the next level in the Scorecard.

application/json404

Scorecard not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Create or update Scorecard

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

dryRunbooleanOptional

When true, this endpoint only validates the descriptor contents and returns any errors or warnings.

anyOptional200

Created Scorecard

application/json400

Bad Request

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Request Scorecard rule exemption

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagstringRequired

Unique tag for the Scorecard

Example: `my-production-readiness-checklist`entityTagstringRequired

The entity tag (`x-cortex-tag`) that identifies the entity.

daysinteger · int64 · nullableOptional

Number of days how long rule should be exempt. If not set, rule will be exempt until exempt until revoked.

reasonstringRequired

Reason for creating exemption

ruleIdentifierstringRequired

Identifier of the Scorecard rule to request exemption for

200

Successfully requested Scorecard rule exemption

application/json404

Scorecard not found, entity not found, or rule with given identifier not found within the Scorecard

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Evaluate entity scorecard score

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagstringRequired

Unique tag for the Scorecard

Example: `my-production-readiness-checklist`entityTagstringRequired

The entity tag (`x-cortex-tag`) that identifies the entity.

200

Scorecard score evaluation triggered successfully

```
No content
```

403

Unauthorized

404

Scorecard not found

409

Already evaluating scorecard

429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json500

Scorecard evaluation failed

$/$

```
No content
```

### Revoke Scorecard rule exemption

putAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagstringRequired

Unique tag for the Scorecard

Example: `my-production-readiness-checklist`entityTagstringRequired

The entity tag (`x-cortex-tag`) that identifies the entity.

reasonstringRequiredruleIdentifierstringRequired

Identifier of the Scorecard rule

200

Revoked Scorecard rule exemptions

application/json400

No approved exemptions to revoke found

application/json404

Scorecard not found, entity not found, or rule with given identifier not found within the Scorecard

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Approve Scorecard rule exemption

putAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagstringRequired

Unique tag for the Scorecard

Example: `my-production-readiness-checklist`entityTagstringRequired

The entity tag (`x-cortex-tag`) that identifies the entity.

ruleIdentifierstringRequired

Identifier of the Scorecard rule

200

Successfully approved Scorecard rule exemptions

application/json400

No pending exemptions to approve found

application/json404

Scorecard not found, entity not found, or rule with given identifier not found within the Scorecard

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Deny Scorecard rule exemption

putAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagstringRequired

Unique tag for the Scorecard

Example: `my-production-readiness-checklist`entityTagstringRequired

The entity tag (`x-cortex-tag`) that identifies the entity.

reasonstringRequiredruleIdentifierstringRequired

Identifier of the Scorecard rule

200

Denied Scorecard rule exemptions

application/json400

No pending exemptions to approve found

application/json404

Scorecard not found, entity not found, or rule with given identifier not found within the Scorecard

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Delete Scorecard

deleteAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagstringRequired

Unique tag for the Scorecard

Example: `my-production-readiness-checklist`200

Successfully deleted Scorecard

```
No content
```

404

Scorecard not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$

```
No content
```

Last updated 2 months ago

Was this helpful?

---

# Secrets

### Required permissions

-

### List secrets

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

pageSizeinteger · int32Required

Number of results to return per page, between 1 and 1000. Default 250.

Default:  `250`pageinteger · int32Required

Page number to return, 0-indexed. Default 0.

Default:  `0`200

Successfully retrieved secrets

application/json400

Bad Request

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Retrieve secret

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

200

Successfully retrieved secret

application/json404

Secret not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Create secret

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

namestringRequired

Human-readable name for the secret

Example: `My Secret`secretstringRequired

Value of the secret

Example: `my-secret-password`tagstringRequired

Unique identifier for the secret

Example: `my-secret`200

Successfully created secret

application/json400

Bad Request

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Update secret

putAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

namestringOptional

Human-readable name for the secret

Example: `My Secret`secretstringOptional

Value of the secret

Example: `my-secret-password`200

Successfully updated secret

application/json400

Bad Request

application/json404

Secret not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Delete secret

deleteAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

200

Secret successfully deleted

400

Bad Request

application/json404

Secret not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$

```
No content
```

Last updated 2 months ago

Was this helpful?

---

# Team Hierarchies

### Required permissions

## Operations

### Retrieve team relationships

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

200

Successfully found team relationships

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Replace all relationships

putAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

replacebooleanRequired

Supports only replace=true right now

Default:  `false`Example: `true`200

Successfully created team relationships

application/json400

Bad Request

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

Last updated 2 months ago

Was this helpful?

---

# Teams

### Required permissions

## Operations

### Retrieve list of teams or team details

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

includeTeamsWithoutMembersbooleanOptional

Include teams without members

Example: `false`teamTagstringOptional

Team identifier

Example: `my-team`200

Object containing a list of teams

application/json404

Team not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Retrieve team details

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

200

Successfully found team

Note: the response objects can also include an `idpGroup` or `cortexTeam` field depending on whether the team contains a `group` or only consists of individually defined `members`.

application/json404

Team not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Create a team

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

or200

Successfully created a team

application/json400

Bad Request

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### [Cortex managed teams] Update members in team

putAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

typestringRequired200

Successfully updated team members

application/json400

Bad Request

application/json403

Forbidden

application/json404

Team not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### [Cortex managed teams] Update members in team

putAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

teamTagstringRequiredtypestringRequired200

Successfully updated team members

application/json400

Bad Request

application/json403

Forbidden

application/json404

Team not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Update team metadata

putAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

teamTagstringRequiredor200

Successfully updated team

application/json400

Bad Request

application/json404

Team not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Update team metadata

putAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

or200

Successfully updated team

application/json400

Bad Request

application/json404

Team not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Archive team

putAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

200

Successfully archived team

application/json404

Team not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Unarchive team

putAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

200

Successfully unarchived team

application/json404

Team not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Delete team

deleteAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

teamTagstringRequired204

Successfully deleted team

application/json404

Team not found

application/json405

Team delete is not allowed

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Delete team by tag or ID

deleteAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

204

Successfully deleted team

application/json404

Team not found

application/json405

Team delete is not allowed

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

Last updated 2 months ago

Was this helpful?

---

# Workflows

### Required permissions

-
-
-

## Operations

### List workflows

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

includeActionsbooleanOptional

When true, returns the list of actions for each workflow. Defaults to false.

Default:  `false`searchQuerystringOptional

When set, only returns workflows with the given substring in the name or description.

pageSizeinteger · int32Required

Number of results to return per page, between 1 and 1000. Default 250.

Default:  `250`pageinteger · int32Required

Page number to return, 0-indexed. Default 0.

Default:  `0`200

Successfully found workflows

application/jsonapplication/yaml403

Access denied

application/jsonapplication/yaml429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Retrieve workflow

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

200

Successfully found workflow

application/jsonapplication/yaml403

Access denied

application/jsonapplication/yaml404

Workflow not found

application/jsonapplication/yaml429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Create or update workflow

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

descriptionstringOptional

Description of the workflow

failedRunResponseTemplatestringOptional

Template for the response when the workflow run fails

iconTagstringOptional

Icon tag for the workflow

isDraftbooleanRequired

Whether the workflow is a draft

isRunnableViaApibooleanOptional

Whether the workflow is runnable via the public API

namestringRequired

Name of the workflow

restrictActionCompletionToRunnerUserbooleanRequired

If true, only the user who started the workflow can complete actions. Defaults to false.

runResponseTemplatestringOptional

Template for the response when the workflow is completed successfully

tagstringRequired

Tag of the workflow

200

Workflow created successfully

application/jsonapplication/yaml400

Bad request

application/jsonapplication/yaml403

Access denied

application/jsonapplication/yaml429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Validates YAML descriptor

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

anyOptional200

Validation result

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Update asynchronous HTTP request Workflow block

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

callbackIdstringRequired

Callback ID; Provided by the Workflow block when it runs

messagestringRequired

Human readable message to be shown to the user

statusstring · enumRequired

Status of the callback request. `UPDATE` keeps the workflow paused

Possible values :  200

Successfully received Workflow callback

```
No content
```

400

Bad request

application/jsonapplication/yaml403

Access denied

application/jsonapplication/yaml404

Workflow run or block not found

application/jsonapplication/yaml406

Workflow block is not waiting for callback

application/jsonapplication/yaml429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$

```
No content
```

### Delete workflow

deleteAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

200

Workflow deleted successfully

```
No content
```

404

Workflow not found

application/jsonapplication/yaml429

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

# Workflows

### Required permissions

-
-
-

## Operations

### List workflows

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

includeActionsbooleanOptional

When true, returns the list of actions for each workflow. Defaults to false.

Default:  `false`searchQuerystringOptional

When set, only returns workflows with the given substring in the name or description.

pageSizeinteger · int32Required

Number of results to return per page, between 1 and 1000. Default 250.

Default:  `250`pageinteger · int32Required

Page number to return, 0-indexed. Default 0.

Default:  `0`200

Successfully found workflows

application/jsonapplication/yaml403

Access denied

application/jsonapplication/yaml429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Retrieve workflow

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

200

Successfully found workflow

application/jsonapplication/yaml403

Access denied

application/jsonapplication/yaml404

Workflow not found

application/jsonapplication/yaml429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Create or update workflow

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

descriptionstringOptional

Description of the workflow

failedRunResponseTemplatestringOptional

Template for the response when the workflow run fails

iconTagstringOptional

Icon tag for the workflow

isDraftbooleanRequired

Whether the workflow is a draft

isRunnableViaApibooleanOptional

Whether the workflow is runnable via the public API

namestringRequired

Name of the workflow

restrictActionCompletionToRunnerUserbooleanRequired

If true, only the user who started the workflow can complete actions. Defaults to false.

runResponseTemplatestringOptional

Template for the response when the workflow is completed successfully

tagstringRequired

Tag of the workflow

200

Workflow created successfully

application/jsonapplication/yaml400

Bad request

application/jsonapplication/yaml403

Access denied

application/jsonapplication/yaml429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Validates YAML descriptor

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

anyOptional200

Validation result

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Update asynchronous HTTP request Workflow block

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

callbackIdstringRequired

Callback ID; Provided by the Workflow block when it runs

messagestringRequired

Human readable message to be shown to the user

statusstring · enumRequired

Status of the callback request. `UPDATE` keeps the workflow paused

Possible values :  200

Successfully received Workflow callback

```
No content
```

400

Bad request

application/jsonapplication/yaml403

Access denied

application/jsonapplication/yaml404

Workflow run or block not found

application/jsonapplication/yaml406

Workflow block is not waiting for callback

application/jsonapplication/yaml429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$

```
No content
```

### Delete workflow

deleteAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

200

Workflow deleted successfully

```
No content
```

404

Workflow not found

application/jsonapplication/yaml429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$

```
No content
```

Last updated 2 months ago

Was this helpful?
