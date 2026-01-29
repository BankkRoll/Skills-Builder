# REST API endpoints for network configurations and more

# REST API endpoints for network configurations

> REST API endpoints for network configurations

## List hosted compute network configurations for an organization

Lists all hosted compute network configurations configured in an organization.

OAuth app tokens and personal access tokens (classic) need the `read:network_configurations` scope to use this endpoint.

### Fine-grained access tokens for "List hosted compute network configurations for an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Network configurations" organization permissions (read)

### Parameters for "List hosted compute network configurations for an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| pageintegerThe page number of the results to fetch. For more information, see "Using pagination in the REST API."Default:1 |

### HTTP response status codes for "List hosted compute network configurations for an organization"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "List hosted compute network configurations for an organization"

#### Request example

get/orgs/{org}/settings/network-configurations

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/settings/network-configurations`

Response

-
-

`Status: 200``{
"total_count": 2,
"network_configurations": [
{
"id": "123456789ABCDEF",
"name": "My network configuration",
"compute_service": "actions",
"network_settings_ids": [
"23456789ABDCEF1",
"3456789ABDCEF12"
],
"created_on": "2022-10-09T23:39:01Z"
},
{
"id": "456789ABDCEF123",
"name": "My other configuration",
"compute_service": "none",
"network_settings_ids": [
"56789ABDCEF1234",
"6789ABDCEF12345"
],
"created_on": "2023-04-26T15:23:37Z"
}
]
}`

## Create a hosted compute network configuration for an organization

Creates a hosted compute network configuration for an organization.

OAuth app tokens and personal access tokens (classic) need the `write:network_configurations` scope to use this endpoint.

### Fine-grained access tokens for "Create a hosted compute network configuration for an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Network configurations" organization permissions (write)

### Parameters for "Create a hosted compute network configuration for an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| namestringRequiredName of the network configuration. Must be between 1 and 100 characters and may only contain upper and lowercase letters a-z, numbers 0-9, '.', '-', and '_'. |
| compute_servicestringThe hosted compute service to use for the network configuration.Can be one of:none,actions |
| network_settings_idsarray of stringsRequiredA list of identifiers of the network settings resources to use for the network configuration. Exactly one resource identifier must be specified in the list. |

### HTTP response status codes for "Create a hosted compute network configuration for an organization"

| Status code | Description |
| --- | --- |
| 201 | Created |

### Code samples for "Create a hosted compute network configuration for an organization"

#### Request example

post/orgs/{org}/settings/network-configurations

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/settings/network-configurations \
  -d '{"name":"my-network-configuration","network_settings_ids":["23456789ABDCEF1"],"compute_service":"actions"}'`

Response

-
-

`Status: 201``{
"id": "123456789ABCDEF",
"name": "My network configuration",
"compute_service": "actions",
"network_settings_ids": [
"23456789ABDCEF1",
"3456789ABDCEF12"
],
"created_on": "2022-10-09T23:39:01Z"
}`

## Get a hosted compute network configuration for an organization

Gets a hosted compute network configuration configured in an organization.

OAuth app tokens and personal access tokens (classic) need the `read:network_configurations` scope to use this endpoint.

### Fine-grained access tokens for "Get a hosted compute network configuration for an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Network configurations" organization permissions (read)

### Parameters for "Get a hosted compute network configuration for an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| network_configuration_idstringRequiredUnique identifier of the hosted compute network configuration. |

### HTTP response status codes for "Get a hosted compute network configuration for an organization"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "Get a hosted compute network configuration for an organization"

#### Request example

get/orgs/{org}/settings/network-configurations/{network_configuration_id}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/settings/network-configurations/NETWORK_CONFIGURATION_ID`

Response

-
-

`Status: 200``{
"id": "123456789ABCDEF",
"name": "My network configuration",
"compute_service": "actions",
"network_settings_ids": [
"23456789ABDCEF1",
"3456789ABDCEF12"
],
"created_on": "2022-10-09T23:39:01Z"
}`

## Update a hosted compute network configuration for an organization

Updates a hosted compute network configuration for an organization.

OAuth app tokens and personal access tokens (classic) need the `write:network_configurations` scope to use this endpoint.

### Fine-grained access tokens for "Update a hosted compute network configuration for an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Network configurations" organization permissions (write)

### Parameters for "Update a hosted compute network configuration for an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| network_configuration_idstringRequiredUnique identifier of the hosted compute network configuration. |

| Name, Type, Description |
| --- |
| namestringName of the network configuration. Must be between 1 and 100 characters and may only contain upper and lowercase letters a-z, numbers 0-9, '.', '-', and '_'. |
| compute_servicestringThe hosted compute service to use for the network configuration.Can be one of:none,actions |
| network_settings_idsarray of stringsA list of identifiers of the network settings resources to use for the network configuration. Exactly one resource identifier must be specified in the list. |

### HTTP response status codes for "Update a hosted compute network configuration for an organization"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "Update a hosted compute network configuration for an organization"

#### Request example

patch/orgs/{org}/settings/network-configurations/{network_configuration_id}

-
-
-

`curl -L \
  -X PATCH \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/settings/network-configurations/NETWORK_CONFIGURATION_ID \
  -d '{"name":"my-network-configuration","network_settings_ids":["23456789ABDCEF1"],"compute_service":"actions"}'`

Response

-
-

`Status: 200``{
"id": "123456789ABCDEF",
"name": "My network configuration",
"compute_service": "actions",
"network_settings_ids": [
"23456789ABDCEF1",
"3456789ABDCEF12"
],
"created_on": "2022-10-09T23:39:01Z"
}`

## Delete a hosted compute network configuration from an organization

Deletes a hosted compute network configuration from an organization.

OAuth app tokens and personal access tokens (classic) need the `write:network_configurations` scope to use this endpoint.

### Fine-grained access tokens for "Delete a hosted compute network configuration from an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Network configurations" organization permissions (write)

### Parameters for "Delete a hosted compute network configuration from an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| network_configuration_idstringRequiredUnique identifier of the hosted compute network configuration. |

### HTTP response status codes for "Delete a hosted compute network configuration from an organization"

| Status code | Description |
| --- | --- |
| 204 | No Content |

### Code samples for "Delete a hosted compute network configuration from an organization"

#### Request example

delete/orgs/{org}/settings/network-configurations/{network_configuration_id}

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/settings/network-configurations/NETWORK_CONFIGURATION_ID`

Response

`Status: 204`

## Get a hosted compute network settings resource for an organization

Gets a hosted compute network settings resource configured for an organization.

OAuth app tokens and personal access tokens (classic) need the `read:network_configurations` scope to use this endpoint.

### Fine-grained access tokens for "Get a hosted compute network settings resource for an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Network configurations" organization permissions (read)

### Parameters for "Get a hosted compute network settings resource for an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| network_settings_idstringRequiredUnique identifier of the hosted compute network settings. |

### HTTP response status codes for "Get a hosted compute network settings resource for an organization"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "Get a hosted compute network settings resource for an organization"

#### Request example

get/orgs/{org}/settings/network-settings/{network_settings_id}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/settings/network-settings/NETWORK_SETTINGS_ID`

Response

-
-

`Status: 200``{
"id": "220F78DACB92BBFBC5E6F22DE1CCF52309D",
"network_configuration_id": "934E208B3EE0BD60CF5F752C426BFB53562",
"name": "my_network_settings",
"subnet_id": "/subscriptions/14839728-3ad9-43ab-bd2b-fa6ad0f75e2a/resourceGroups/my-rg/providers/Microsoft.Network/virtualNetworks/my-vnet/subnets/my-subnet",
"region": "eastus"
}`

---

# REST API endpoints for organization roles

> Use the REST API to interact with organization roles.

## Get all organization roles for an organization

Lists the organization roles available in this organization. For more information on organization roles, see "[Using organization roles](https://docs.github.com/organizations/managing-peoples-access-to-your-organization-with-roles/using-organization-roles)."

To use this endpoint, the authenticated user must be one of:

- An administrator for the organization.
- A user, or a user on a team, with the fine-grained permissions of `read_organization_custom_org_role` in the organization.

OAuth app tokens and personal access tokens (classic) need the `admin:org` scope to use this endpoint.

### Fine-grained access tokens for "Get all organization roles for an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Custom organization roles" organization permissions (read)

### Parameters for "Get all organization roles for an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

### HTTP response status codes for "Get all organization roles for an organization"

| Status code | Description |
| --- | --- |
| 200 | Response - list of organization roles |
| 404 | Resource not found |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Get all organization roles for an organization"

#### Request example

get/orgs/{org}/organization-roles

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/organization-roles`

Response - list of organization roles

-
-

`Status: 200``{
"total_count": 2,
"roles": [
{
"id": 8030,
"name": "Custom Role Manager",
"description": "Permissions to manage custom roles within an org",
"permissions": [
"write_organization_custom_repo_role",
"write_organization_custom_org_role",
"read_organization_custom_repo_role",
"read_organization_custom_org_role"
],
"organization": {
"login": "github",
"id": 9919,
"node_id": "MDEyOk9yZ2FuaXphdGlvbjk5MTk=",
"avatar_url": "https://avatars.githubusercontent.com/u/9919?v=4",
"gravatar_id": "",
"url": "https://api.github.com/users/github",
"html_url": "https://github.com/github",
"followers_url": "https://api.github.com/users/github/followers",
"following_url": "https://api.github.com/users/github/following{/other_user}",
"gists_url": "https://api.github.com/users/github/gists{/gist_id}",
"starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/github/subscriptions",
"organizations_url": "https://api.github.com/users/github/orgs",
"repos_url": "https://api.github.com/users/github/repos",
"events_url": "https://api.github.com/users/github/events{/privacy}",
"received_events_url": "https://api.github.com/users/github/received_events",
"type": "Organization",
"site_admin": false
},
"created_at": "2022-07-04T22:19:11Z",
"updated_at": "2022-07-04T22:20:11Z"
},
{
"id": 8031,
"name": "Auditor",
"description": "Permissions to read the organization audit log",
"permissions": [
"read_audit_logs"
],
"organization": {
"login": "github",
"id": 9919,
"node_id": "MDEyOk9yZ2FuaXphdGlvbjk5MTk=",
"avatar_url": "https://avatars.githubusercontent.com/u/9919?v=4",
"gravatar_id": "",
"url": "https://api.github.com/users/github",
"html_url": "https://github.com/github",
"followers_url": "https://api.github.com/users/github/followers",
"following_url": "https://api.github.com/users/github/following{/other_user}",
"gists_url": "https://api.github.com/users/github/gists{/gist_id}",
"starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/github/subscriptions",
"organizations_url": "https://api.github.com/users/github/orgs",
"repos_url": "https://api.github.com/users/github/repos",
"events_url": "https://api.github.com/users/github/events{/privacy}",
"received_events_url": "https://api.github.com/users/github/received_events",
"type": "Organization",
"site_admin": false
},
"created_at": "2022-07-04T22:19:11Z",
"updated_at": "2022-07-04T22:20:11Z"
}
]
}`

## Remove all organization roles for a team

Removes all assigned organization roles from a team. For more information on organization roles, see "[Using organization roles](https://docs.github.com/organizations/managing-peoples-access-to-your-organization-with-roles/using-organization-roles)."

The authenticated user must be an administrator for the organization to use this endpoint.

OAuth app tokens and personal access tokens (classic) need the `admin:org` scope to use this endpoint.

### Fine-grained access tokens for "Remove all organization roles for a team"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Members" organization permissions (write)

### Parameters for "Remove all organization roles for a team"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| team_slugstringRequiredThe slug of the team name. |

### HTTP response status codes for "Remove all organization roles for a team"

| Status code | Description |
| --- | --- |
| 204 | No Content |

### Code samples for "Remove all organization roles for a team"

#### Request example

delete/orgs/{org}/organization-roles/teams/{team_slug}

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/organization-roles/teams/TEAM_SLUG`

Response

`Status: 204`

## Assign an organization role to a team

Assigns an organization role to a team in an organization. For more information on organization roles, see "[Using organization roles](https://docs.github.com/organizations/managing-peoples-access-to-your-organization-with-roles/using-organization-roles)."

The authenticated user must be an administrator for the organization to use this endpoint.

OAuth app tokens and personal access tokens (classic) need the `admin:org` scope to use this endpoint.

### Fine-grained access tokens for "Assign an organization role to a team"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Members" organization permissions (write)

### Parameters for "Assign an organization role to a team"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| team_slugstringRequiredThe slug of the team name. |
| role_idintegerRequiredThe unique identifier of the role. |

### HTTP response status codes for "Assign an organization role to a team"

| Status code | Description |
| --- | --- |
| 204 | No Content |
| 404 | Response if the organization, team or role does not exist. |
| 422 | Response if the organization roles feature is not enabled for the organization, or validation failed. |

### Code samples for "Assign an organization role to a team"

#### Request example

put/orgs/{org}/organization-roles/teams/{team_slug}/{role_id}

-
-
-

`curl -L \
  -X PUT \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/organization-roles/teams/TEAM_SLUG/ROLE_ID`

Response

`Status: 204`

## Remove an organization role from a team

Removes an organization role from a team. For more information on organization roles, see "[Using organization roles](https://docs.github.com/organizations/managing-peoples-access-to-your-organization-with-roles/using-organization-roles)."

The authenticated user must be an administrator for the organization to use this endpoint.

OAuth app tokens and personal access tokens (classic) need the `admin:org` scope to use this endpoint.

### Fine-grained access tokens for "Remove an organization role from a team"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Members" organization permissions (write)

### Parameters for "Remove an organization role from a team"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| team_slugstringRequiredThe slug of the team name. |
| role_idintegerRequiredThe unique identifier of the role. |

### HTTP response status codes for "Remove an organization role from a team"

| Status code | Description |
| --- | --- |
| 204 | No Content |

### Code samples for "Remove an organization role from a team"

#### Request example

delete/orgs/{org}/organization-roles/teams/{team_slug}/{role_id}

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/organization-roles/teams/TEAM_SLUG/ROLE_ID`

Response

`Status: 204`

## Remove all organization roles for a user

Revokes all assigned organization roles from a user. For more information on organization roles, see "[Using organization roles](https://docs.github.com/organizations/managing-peoples-access-to-your-organization-with-roles/using-organization-roles)."

The authenticated user must be an administrator for the organization to use this endpoint.

OAuth app tokens and personal access tokens (classic) need the `admin:org` scope to use this endpoint.

### Fine-grained access tokens for "Remove all organization roles for a user"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Members" organization permissions (write)

### Parameters for "Remove all organization roles for a user"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| usernamestringRequiredThe handle for the GitHub user account. |

### HTTP response status codes for "Remove all organization roles for a user"

| Status code | Description |
| --- | --- |
| 204 | No Content |

### Code samples for "Remove all organization roles for a user"

#### Request example

delete/orgs/{org}/organization-roles/users/{username}

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/organization-roles/users/USERNAME`

Response

`Status: 204`

## Assign an organization role to a user

Assigns an organization role to a member of an organization. For more information on organization roles, see "[Using organization roles](https://docs.github.com/organizations/managing-peoples-access-to-your-organization-with-roles/using-organization-roles)."

The authenticated user must be an administrator for the organization to use this endpoint.

OAuth app tokens and personal access tokens (classic) need the `admin:org` scope to use this endpoint.

### Fine-grained access tokens for "Assign an organization role to a user"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Members" organization permissions (write)

### Parameters for "Assign an organization role to a user"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| usernamestringRequiredThe handle for the GitHub user account. |
| role_idintegerRequiredThe unique identifier of the role. |

### HTTP response status codes for "Assign an organization role to a user"

| Status code | Description |
| --- | --- |
| 204 | No Content |
| 404 | Response if the organization, user or role does not exist. |
| 422 | Response if the organization roles feature is not enabled enabled for the organization, the validation failed, or the user is not an organization member. |

### Code samples for "Assign an organization role to a user"

#### Request example

put/orgs/{org}/organization-roles/users/{username}/{role_id}

-
-
-

`curl -L \
  -X PUT \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/organization-roles/users/USERNAME/ROLE_ID`

Response

`Status: 204`

## Remove an organization role from a user

Remove an organization role from a user. For more information on organization roles, see "[Using organization roles](https://docs.github.com/organizations/managing-peoples-access-to-your-organization-with-roles/using-organization-roles)."

The authenticated user must be an administrator for the organization to use this endpoint.

OAuth app tokens and personal access tokens (classic) need the `admin:org` scope to use this endpoint.

### Fine-grained access tokens for "Remove an organization role from a user"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Members" organization permissions (write)

### Parameters for "Remove an organization role from a user"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| usernamestringRequiredThe handle for the GitHub user account. |
| role_idintegerRequiredThe unique identifier of the role. |

### HTTP response status codes for "Remove an organization role from a user"

| Status code | Description |
| --- | --- |
| 204 | No Content |

### Code samples for "Remove an organization role from a user"

#### Request example

delete/orgs/{org}/organization-roles/users/{username}/{role_id}

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/organization-roles/users/USERNAME/ROLE_ID`

Response

`Status: 204`

## Get an organization role

Gets an organization role that is available to this organization. For more information on organization roles, see "[Using organization roles](https://docs.github.com/organizations/managing-peoples-access-to-your-organization-with-roles/using-organization-roles)."

To use this endpoint, the authenticated user must be one of:

- An administrator for the organization.
- A user, or a user on a team, with the fine-grained permissions of `read_organization_custom_org_role` in the organization.

OAuth app tokens and personal access tokens (classic) need the `admin:org` scope to use this endpoint.

### Fine-grained access tokens for "Get an organization role"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Custom organization roles" organization permissions (read)

### Parameters for "Get an organization role"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| role_idintegerRequiredThe unique identifier of the role. |

### HTTP response status codes for "Get an organization role"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Get an organization role"

#### Request example

get/orgs/{org}/organization-roles/{role_id}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/organization-roles/ROLE_ID`

Response

-
-

`Status: 200``{
"id": 8030,
"name": "Custom Role Manager",
"description": "Permissions to manage custom roles within an org",
"permissions": [
"write_organization_custom_repo_role",
"write_organization_custom_org_role",
"read_organization_custom_repo_role",
"read_organization_custom_org_role"
],
"organization": {
"login": "github",
"id": 1,
"node_id": "MDEyOk9yZ2FuaXphdGlvbjE=",
"url": "https://api.github.com/orgs/github",
"repos_url": "https://api.github.com/orgs/github/repos",
"events_url": "https://api.github.com/orgs/github/events",
"hooks_url": "https://api.github.com/orgs/github/hooks",
"issues_url": "https://api.github.com/orgs/github/issues",
"members_url": "https://api.github.com/orgs/github/members{/member}",
"public_members_url": "https://api.github.com/orgs/github/public_members{/member}",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"description": "A great organization"
},
"created_at": "2022-07-04T22:19:11Z",
"updated_at": "2022-07-04T22:20:11Z"
}`

## List teams that are assigned to an organization role

Lists the teams that are assigned to an organization role. For more information on organization roles, see "[Using organization roles](https://docs.github.com/organizations/managing-peoples-access-to-your-organization-with-roles/using-organization-roles)."

To use this endpoint, you must be an administrator for the organization.

OAuth app tokens and personal access tokens (classic) need the `admin:org` scope to use this endpoint.

### Fine-grained access tokens for "List teams that are assigned to an organization role"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Members" organization permissions (read)

### Parameters for "List teams that are assigned to an organization role"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| role_idintegerRequiredThe unique identifier of the role. |

| Name, Type, Description |
| --- |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| pageintegerThe page number of the results to fetch. For more information, see "Using pagination in the REST API."Default:1 |

### HTTP response status codes for "List teams that are assigned to an organization role"

| Status code | Description |
| --- | --- |
| 200 | Response - List of assigned teams |
| 404 | Response if the organization or role does not exist. |
| 422 | Response if the organization roles feature is not enabled or validation failed. |

### Code samples for "List teams that are assigned to an organization role"

#### Request example

get/orgs/{org}/organization-roles/{role_id}/teams

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/organization-roles/ROLE_ID/teams`

Response - List of assigned teams

-
-

`Status: 200``[
{
"id": 1,
"node_id": "MDQ6VGVhbTE=",
"url": "https://api.github.com/teams/1",
"html_url": "https://github.com/orgs/github/teams/justice-league",
"name": "Justice League",
"slug": "justice-league",
"description": "A great team.",
"privacy": "closed",
"notification_setting": "notifications_enabled",
"permission": "admin",
"members_url": "https://api.github.com/teams/1/members{/member}",
"repositories_url": "https://api.github.com/teams/1/repos",
"parent": null
}
]`

## List users that are assigned to an organization role

Lists organization members that are assigned to an organization role. For more information on organization roles, see "[Using organization roles](https://docs.github.com/organizations/managing-peoples-access-to-your-organization-with-roles/using-organization-roles)."

To use this endpoint, you must be an administrator for the organization.

OAuth app tokens and personal access tokens (classic) need the `admin:org` scope to use this endpoint.

### Fine-grained access tokens for "List users that are assigned to an organization role"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Members" organization permissions (read)

### Parameters for "List users that are assigned to an organization role"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| role_idintegerRequiredThe unique identifier of the role. |

| Name, Type, Description |
| --- |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| pageintegerThe page number of the results to fetch. For more information, see "Using pagination in the REST API."Default:1 |

### HTTP response status codes for "List users that are assigned to an organization role"

| Status code | Description |
| --- | --- |
| 200 | Response - List of assigned users |
| 404 | Response if the organization or role does not exist. |
| 422 | Response if the organization roles feature is not enabled or validation failed. |

### Code samples for "List users that are assigned to an organization role"

#### Request example

get/orgs/{org}/organization-roles/{role_id}/users

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/organization-roles/ROLE_ID/users`

Response - List of assigned users

-
-

`Status: 200``[
{
"login": "octocat",
"id": 1,
"node_id": "MDQ6VXNlcjE=",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/octocat",
"html_url": "https://github.com/octocat",
"followers_url": "https://api.github.com/users/octocat/followers",
"following_url": "https://api.github.com/users/octocat/following{/other_user}",
"gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
"starred_url": "https://api.github.com/users/octocat/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/octocat/subscriptions",
"organizations_url": "https://api.github.com/users/octocat/orgs",
"repos_url": "https://api.github.com/users/octocat/repos",
"events_url": "https://api.github.com/users/octocat/events{/privacy}",
"received_events_url": "https://api.github.com/users/octocat/received_events",
"type": "User",
"site_admin": false
}
]`
