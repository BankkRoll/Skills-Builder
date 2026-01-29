# Prometheus API and more

# Prometheus API

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

### Add a single configuration

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

aliasstringRequiredhoststringRequiredisDefaultbooleanRequiredpasswordstringRequiredprometheusTenantIdstringOptionalusernamestringRequired200

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

### Update a configuration

putAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

aliasstringRequiredaliasstringRequiredisDefaultbooleanRequired200

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

# SonarQube API

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

### Add a single configuration

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

aliasstringRequiredhoststringRequiredisDefaultbooleanRequiredtokenstringRequired200

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

### Update a configuration

putAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

aliasstringRequiredaliasstringRequiredisDefaultbooleanRequired200

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

# Integrations APIs

[Azure Active Directory (Entra ID) API](https://docs.cortex.io/api/readme/integrations/azure-active-directory)[Azure Resources API](https://docs.cortex.io/api/readme/integrations/azure-resources)[AWS API](https://docs.cortex.io/api/readme/integrations/aws)[Azure DevOps API](https://docs.cortex.io/api/readme/integrations/azure-devops)[CircleCI API](https://docs.cortex.io/api/readme/integrations/circleci)[Coralogix API](https://docs.cortex.io/api/readme/integrations/coralogix)[Datadog API](https://docs.cortex.io/api/readme/integrations/datadog)[GitHub API](https://docs.cortex.io/api/readme/integrations/github)[GitLab API](https://docs.cortex.io/api/readme/integrations/gitlab)[incident.io API](https://docs.cortex.io/api/readme/integrations/incidentio)[LaunchDarkly API](https://docs.cortex.io/api/readme/integrations/launchdarkly)[New Relic API](https://docs.cortex.io/api/readme/integrations/new-relic)[PagerDuty API](https://docs.cortex.io/api/readme/integrations/pagerduty)[Prometheus API](https://docs.cortex.io/api/readme/integrations/prometheus)[SonarQube API](https://docs.cortex.io/api/readme/integrations/sonarqube)

Was this helpful?

---

# IP Allowlist

### Required permissions

## Operations

### Gets allowlist of IP addresses & ranges

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

pageSizeinteger · int32Required

Number of results to return per page, between 1 and 1000. Default 250.

Default:  `250`pageinteger · int32Required

Page number to return, 0-indexed. Default 0.

Default:  `0`200

Successfully retrieved IP allowlist

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Validates allowlist of IP addresses & ranges

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

200

Successfully validated allowlist

application/jsonResponseone ofor429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Replace existing allowlist with provided list of IP addresses & ranges

putAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

forcebooleanOptional

When true, entries will be updated even if the list doesn't contain the requestor's IP address

200

Successfully replaced allowlist

application/json400

Bad Request

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

Last updated 2 months ago

Was this helpful?

---

# Notification Logs

### Required permissions

## Operations

### Retrieve notification logs

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

notificationRunIdsinteger · int64[]Optional

The unique identifier of the notification run that this log is associated with.

recipientEmailsstring[]Optional

The email address that this notification was sent to.

recipientEntityIdsinteger · int64[]Optional

The unique identifiers of the entities that the notifications were sent to.

recipientChannelsstring[]Optional

The channel in Slack or MS Teams where the notification was sent.

fromDatestring · date-timeOptional

The ISO date and time to start the search from.

Example: `2021-01-01T00:00:00`untilDatestring · date-timeOptional

The ISO date and time to end the search at.

Example: `2021-01-01T00:00:00`pageSizeinteger · int32Required

Number of results to return per page, between 1 and 1000. Default 250.

Default:  `250`pageinteger · int32Required

Page number to return, 0-indexed. Default 0.

Default:  `0`orderBystring · enumOptional

Sort the results ascending or descending.

Default:  `DESC`Possible values :  200

Successfully retrieved notification logs

application/json403

Forbidden

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Retrieve notification runs

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

searchQueryanyOptional

A search query to filter the results.

includeObjectsbooleanOptional

Whether to include the objects associated with the notification run.

Default:  `false`fromDatestring · date-timeOptional

The ISO date and time to start the search from.

Example: `2021-01-01T00:00:00`untilDatestring · date-timeOptional

The ISO date and time to end the search at.

Example: `2021-01-01T00:00:00`deliveredOnlybooleanOptionalDefault:  `true`pageSizeinteger · int32Required

Number of results to return per page, between 1 and 1000. Default 250.

Default:  `250`pageinteger · int32Required

Page number to return, 0-indexed. Default 0.

Default:  `0`orderBystring · enumOptional

Sort the results ascending or descending.

Default:  `DESC`Possible values :  200

Successfully retrieved notification runs

application/json403

Forbidden

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

Last updated 2 months ago

Was this helpful?

---

# On call

### Required permissions

-

## Operations

### Retrieve current on-call for entity

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

200

Successfully retrieved current on-call

application/json404

Entity not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Retrieve on-call registration for entity

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

200

Successfully retrieved on-call registration

application/json404

Entity or registration not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

Last updated 2 months ago

Was this helpful?

---

# Packages

### Required permissions

## Operations

### List packages

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

200

All packages. If using pagination, we do not return page, total, or totalPages in the response. An empty array is returned once you reach the end.

application/json404

Entity not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### [csharp] Upload Nuget csproj

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

stringOptional200

Successfully saved packages

application/json404

Entity not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### [csharp] Upload Nuget packages.lock.json

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

stringOptional200

Successfully saved packages

application/json404

Entity not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### [csharp] Delete Nuget package

deleteAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

namestringRequired200

Successfully deleted package

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

### [golang] Upload go.sum

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

stringOptional200

Successfully saved packages

application/json404

Entity not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### [go] Delete Go package

deleteAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

namestringRequired200

Successfully deleted package

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

### [java] Upload single Java package

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

namestringRequired

Package name, like io.cortex.scorecards

Example: `io.cortex.scorecards`versionstringRequired

Semver package version

Example: `1.2.3`200

Successfully saved package

application/json404

Entity not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### [java] Upload multiple Java packages

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

namestringRequired

Package name, like io.cortex.scorecards

Example: `io.cortex.scorecards`versionstringRequired

Semver package version

Example: `1.2.3`200

Successfully saved packages

application/json404

Entity not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### [java] Upload maven pom.xml

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

stringOptional200

Successfully saved packages

application/json404

Entity not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### [java] Delete Java package

deleteAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

namestringRequired200

Successfully deleted package

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

### [js] Upload NPM/Yarn/PNPM package.json

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

stringOptional200

Successfully saved packages

application/json404

Entity not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### [js] Upload NPM package-lock.json

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

stringOptional200

Successfully saved packages

application/json404

Entity not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### [node] Delete Node package

deleteAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

namestringRequired200

Successfully deleted package

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

### [js] Upload pnpm-lock.yaml

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

stringOptional200

Successfully saved packages

application/json404

Entity not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### [js] Upload yarn.lock

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

stringOptional200

Successfully saved packages

application/json404

Entity not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### [python] Upload pipfile.lock

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

stringOptional200

Successfully saved packages

application/json404

Entity not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### [python] Upload requirements.txt

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

stringOptional200

Successfully saved packages

application/json404

Entity not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### [python] Delete Python package

deleteAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagOrIdstringRequired

Entity identifier - can be a tag or CID

namestringRequired200

Successfully deleted package

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

Was this helpful?

---

# Plugins

### Required permissions

## Operations

### Get all plugins

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

includeDraftsbooleanOptionalpageSizeinteger · int32Required

Number of results to return per page, between 1 and 1000. Default 250.

Default:  `250`pageinteger · int32Required

Page number to return, 0-indexed. Default 0.

Default:  `0`200

List of plugins

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Get plugin by tag

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagstringRequired

Unique identifier for the plugin

includeBlobbooleanOptional

When true, returns the plugin blob. Defaults to false.

Default:  `false`200

Metadata of the plugin

application/json404

Plugin not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Create a plugin

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

blobstringRequired

The raw source code of the plugin. This should be an HTML file

descriptionstringOptional

Description of the plugin

iconTagstringOptional

Icon tag for the plugin

isDraftbooleanRequired

Whether the plugin is generally available or not

minimumRoleRequiredstringRequired

The minimum role required to view the plugin, e.g. `VIEWER`, `USER`, `MANAGER`, `OWNER`, or the tag for a custom role. Learn more about each permission in our [docs](https://docs.cortex.io/docs/walkthroughs/workspace-settings/permissioning#roles-in-cortex).

namestringRequired

Display name of the plugin

proxyTagstringOptional

The identifier of the proxy to use for requests from this plugin

tagstringRequired

Unique identifier for the plugin

versionstringOptional

The version of the plugin

200

Metadata of the created plugin

application/json400

Invalid request

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Replace a plugin

putAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagstringRequired

Unique identifier for the plugin

blobstringRequired

The raw source code of the plugin. This should be an HTML file

descriptionstringOptional

Description of the plugin

iconTagstringOptional

Icon tag for the plugin

isDraftbooleanRequired

Whether the plugin is generally available or not

minimumRoleRequiredstringRequired

The minimum role required to view the plugin, e.g. `VIEWER`, `USER`, `MANAGER`, `OWNER`, or the tag for a custom role. Learn more about each permission in our [docs](https://docs.cortex.io/docs/walkthroughs/workspace-settings/permissioning#roles-in-cortex).

namestringRequired

Display name of the plugin

proxyTagstringOptional

The identifier of the proxy to use for requests from this plugin

versionstringOptional

The version of the plugin

200

Metadata of the replaced plugin

application/json400

Invalid request

application/json404

Plugin not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Delete a plugin

deleteAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

tagstringRequired

Unique identifier for the plugin

204

Plugin deleted

404

Plugin not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$

```
No content
```

Last updated 2 months ago

Was this helpful?

---

# Queries

### Required permissions

## Operations

### Retrieve query results

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

jobIdstringRequired

jobId of the query to retrieve

200

Successfully found query

application/json404

Query not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Run query

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

querystringRequired200

Successfully submitted query

application/json400

Bad request

application/json409

Conflict

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

Last updated 2 months ago

Was this helpful?

---

# SCIM

### Required permissions

## Operations

### Find users

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

attributesstringOptionalexcludedAttributesstringOptionalfilterstringOptionalstartIndexinteger · int32Optionalcountinteger · int32OptionalsortBystringOptionalsortOrderstringOptionaldomainstringOptional200

Returns list of requested users

application/jsonapplication/scim+jsonResponsestring429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Gets a user by id

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

idstringRequiredattributesstringOptionalexcludedAttributesstringOptional200

Returns requested user data

application/jsonapplication/scim+jsonResponsestring429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Creates a user

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

attributesstringOptionalexcludedAttributesstringOptionalstringOptional200

Returns created user data

application/jsonapplication/scim+jsonResponsestring429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Updates a user

putAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

idstringRequiredattributesstringOptionalexcludedAttributesstringOptionalstringOptional200

Returns updated user data

application/jsonapplication/scim+jsonResponsestring429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Patches a user

patchAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

idstringRequiredattributesstringOptionalexcludedAttributesstringOptionalstringOptional200

Returns patched user data

application/jsonapplication/scim+jsonResponsestring429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Deletes a user

deleteAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

idstringRequired200

Returns deleted user data

application/jsonapplication/scim+jsonResponsestring429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

Last updated 2 months ago

Was this helpful?
