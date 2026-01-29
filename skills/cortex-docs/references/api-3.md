# CircleCI API and more

# CircleCI API

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

aliasstringRequiredapiKeystringRequiredhoststringOptionalisDefaultbooleanRequired200

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

aliasstringRequiredaliasstringRequiredhoststringOptionalisDefaultbooleanRequired200

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

---

# Coralogix API

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

### Add a single configuration

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

aliasstringRequiredapiKeystringRequiredisDefaultbooleanRequiredregionstring · enumRequiredPossible values :  200

Successfully added configuration

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

---

# Datadog API

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

aliasstringRequiredapiKeystringRequiredappKeystringRequiredcustomSubdomainstringOptionalenvironmentsstring[]RequiredisDefaultbooleanRequiredregionstring · enumRequiredPossible values :  200

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

aliasstringRequiredaliasstringRequiredenvironmentsstring[]RequiredisDefaultbooleanRequired200

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

# GitHub API

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

### Retrieve a single personal configuration

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

aliasstringRequired200

Successfully found configuration

application/json400

Bad Request

application/json403

Forbidden

application/json404

Configuration not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Retrieve a single app configuration

getAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

aliasstringRequired200

Successfully found configuration

application/json400

Bad Request

application/json403

Forbidden

application/json404

Configuration not found

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

### Add a single app configuration

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

aliasstringRequiredapiHoststringOptionalappUrlstringRequiredapplicationIdstringRequiredclientIdstringRequiredclientSecretstringRequiredisDefaultbooleanRequiredprivateKeystringRequired200

Successfully added configuration

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

aliasstringRequired200

Successfully validated configuration

application/json404

Configuration not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Add a single personal configuration

postAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

accessTokenstringRequiredaliasstringRequiredapiHoststringOptionalisDefaultbooleanRequired200

Successfully added configuration

application/json400

Bad Request

application/json403

Forbidden

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$$/$

### Update a single app configuration

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

### Delete a personal configuration

deleteAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

aliasstringRequired200

Successfully deleted configuration

```
No content
```

400

Bad Request

application/json403

Forbidden

application/json404

Configuration not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$

```
No content
```

### Update a single personal configuration

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

### Delete a single app configuration

deleteAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

aliasstringRequired200

Successfully deleted configuration

```
No content
```

400

Bad Request

application/json403

Forbidden

application/json404

Configuration not found

application/json429

The client has exceeded the rate limit by performing too many requests in a short period. Retry the request after a delay.

application/problem+json$/$

```
No content
```

Last updated 2 months ago

Was this helpful?

---

# GitLab API

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

aliasstringRequiredgroupNamesstring[]RequiredhidePersonalProjectsbooleanRequiredhoststringOptionalisDefaultbooleanRequiredpersonalAccessTokenstringRequired200

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

aliasstringRequiredaliasstringRequiredgroupNamesstring[]RequiredhidePersonalProjectsbooleanRequiredhoststringOptionalisDefaultbooleanRequired200

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

---

# incident.io API

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

aliasstringRequiredapiKeystringRequiredisDefaultbooleanRequired200

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

---

# LaunchDarkly API

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

aliasstringRequiredapiKeystringRequiredenvironmentstring · enumRequiredPossible values :  isDefaultbooleanRequired200

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

# New Relic API

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

accountIdinteger · int32RequiredaliasstringRequiredisDefaultbooleanRequiredpersonalKeystringRequiredregionstring · enumRequiredPossible values :  200

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

### Delete all configurations

deleteAuthorizationstringRequired

All requests to the Cortex API need to provide an `Authorization: Bearer <token>` header, where `<token>` is an API key created in the Settings page of your workspace.

200

Successfully deleted all configurations

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

---

# PagerDuty API

### Required permissions

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

isTokenReadonlybooleanRequiredtokenstringRequired200

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

isTokenReadonlybooleanRequiredtokenstringRequired200

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
