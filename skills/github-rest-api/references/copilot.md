# REST API endpoints for Copilot metrics and more

# REST API endpoints for Copilot metrics

> Use the REST API to view Copilot metrics.

You can use these endpoints to get a breakdown of aggregated metrics for various GitHub Copilot features. The API includes:

- Data for the last 100 days
- Numbers of active users and engaged users
- Breakdowns by language and IDE
- The option to view metrics for an enterprise, organization, or team

Note

The Copilot metrics endpoints are **not** available for GitHub Enterprise Cloud with data residency on GHE.com.

---

# REST API endpoints for Copilot user management

> Use the REST API to manage the GitHub Copilot Business subscription for your organization.

The REST API is now versioned. For more information, see "[About API versioning](https://docs.github.com/rest/overview/api-versions)."

# REST API endpoints for Copilot user management

Use the REST API to manage the GitHub Copilot Business subscription for your organization.

Note

These endpoints are in public preview and subject to change.

## Get Copilot seat information and settings for an organization

Note

This endpoint is in public preview and is subject to change.

Gets information about an organization's Copilot subscription, including seat breakdown
and feature policies. To configure these settings, go to your organization's settings on GitHub.com.
For more information, see "[Managing policies for Copilot in your organization](https://docs.github.com/copilot/managing-copilot/managing-policies-for-copilot-business-in-your-organization)."

Only organization owners can view details about the organization's Copilot Business or Copilot Enterprise subscription.

OAuth app tokens and personal access tokens (classic) need either the `manage_billing:copilot` or `read:org` scopes to use this endpoint.

### Fine-grained access tokens for "Get Copilot seat information and settings for an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have at least one of the following permission sets:

- "GitHub Copilot Business" organization permissions (read)
- "Administration" organization permissions (read)

### Parameters for "Get Copilot seat information and settings for an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

### HTTP response status codes for "Get Copilot seat information and settings for an organization"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 401 | Requires authentication |
| 403 | Forbidden |
| 404 | Resource not found |
| 422 | There is a problem with your account's associated payment method. |
| 500 | Internal Error |

### Code samples for "Get Copilot seat information and settings for an organization"

#### Request example

get/orgs/{org}/copilot/billing

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/copilot/billing`

OK

-
-

`Status: 200``{
"seat_breakdown": {
"total": 12,
"added_this_cycle": 9,
"pending_invitation": 0,
"pending_cancellation": 0,
"active_this_cycle": 12,
"inactive_this_cycle": 11
},
"seat_management_setting": "assign_selected",
"ide_chat": "enabled",
"platform_chat": "enabled",
"cli": "enabled",
"public_code_suggestions": "block",
"plan_type": "business"
}`

## List all Copilot seat assignments for an organization

Note

This endpoint is in public preview and is subject to change.

Lists all Copilot seats for which an organization with a Copilot Business or Copilot Enterprise subscription is currently being billed.
Only organization owners can view assigned seats.

Each seat object contains information about the assigned user's most recent Copilot activity. Users must have telemetry enabled in their IDE for Copilot in the IDE activity to be reflected in `last_activity_at`.
For more information about activity data, see [Metrics data properties for GitHub Copilot](https://docs.github.com/copilot/reference/metrics-data).

OAuth app tokens and personal access tokens (classic) need either the `manage_billing:copilot` or `read:org` scopes to use this endpoint.

### Fine-grained access tokens for "List all Copilot seat assignments for an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have at least one of the following permission sets:

- "GitHub Copilot Business" organization permissions (read)
- "Administration" organization permissions (read)

### Parameters for "List all Copilot seat assignments for an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| pageintegerThe page number of the results to fetch. For more information, see "Using pagination in the REST API."Default:1 |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:50 |

### HTTP response status codes for "List all Copilot seat assignments for an organization"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 401 | Requires authentication |
| 403 | Forbidden |
| 404 | Resource not found |
| 500 | Internal Error |

### Code samples for "List all Copilot seat assignments for an organization"

#### Request example

get/orgs/{org}/copilot/billing/seats

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/copilot/billing/seats`

Response

-
-

`Status: 200``{
"total_seats": 2,
"seats": [
{
"created_at": "2021-08-03T18:00:00-06:00",
"updated_at": "2021-09-23T15:00:00-06:00",
"pending_cancellation_date": null,
"last_activity_at": "2021-10-14T00:53:32-06:00",
"last_activity_editor": "vscode/1.77.3/copilot/1.86.82",
"last_authenticated_at": "2021-10-14T00:53:32-06:00",
"plan_type": "business",
"assignee": {
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
},
"assigning_team": {
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
},
{
"created_at": "2021-09-23T18:00:00-06:00",
"updated_at": "2021-09-23T15:00:00-06:00",
"pending_cancellation_date": "2021-11-01",
"last_activity_at": "2021-10-13T00:53:32-06:00",
"last_activity_editor": "vscode/1.77.3/copilot/1.86.82",
"last_authenticated_at": "2021-10-14T00:53:32-06:00",
"assignee": {
"login": "octokitten",
"id": 1,
"node_id": "MDQ76VNlcjE=",
"avatar_url": "https://github.com/images/error/octokitten_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/octokitten",
"html_url": "https://github.com/octokitten",
"followers_url": "https://api.github.com/users/octokitten/followers",
"following_url": "https://api.github.com/users/octokitten/following{/other_user}",
"gists_url": "https://api.github.com/users/octokitten/gists{/gist_id}",
"starred_url": "https://api.github.com/users/octokitten/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/octokitten/subscriptions",
"organizations_url": "https://api.github.com/users/octokitten/orgs",
"repos_url": "https://api.github.com/users/octokitten/repos",
"events_url": "https://api.github.com/users/octokitten/events{/privacy}",
"received_events_url": "https://api.github.com/users/octokitten/received_events",
"type": "User",
"site_admin": false
}
}
]
}`

## Add teams to the Copilot subscription for an organization

Note

This endpoint is in public preview and is subject to change.

Purchases a GitHub Copilot seat for all users within each specified team.
The organization will be billed for each seat based on the organization's Copilot plan. For more information about Copilot pricing, see "[About billing for GitHub Copilot in your organization](https://docs.github.com/copilot/managing-copilot/managing-github-copilot-in-your-organization/managing-the-copilot-subscription-for-your-organization/about-billing-for-github-copilot-in-your-organization)."

Only organization owners can purchase Copilot seats for their organization members. The organization must have a Copilot Business or Copilot Enterprise subscription and a configured suggestion matching policy.
For more information about setting up a Copilot subscription, see "[Subscribing to Copilot for your organization](https://docs.github.com/copilot/managing-copilot/managing-github-copilot-in-your-organization/managing-the-copilot-subscription-for-your-organization/subscribing-to-copilot-for-your-organization)."
For more information about setting a suggestion matching policy, see "[Managing policies for Copilot in your organization](https://docs.github.com/copilot/managing-copilot/managing-github-copilot-in-your-organization/setting-policies-for-copilot-in-your-organization/managing-policies-for-copilot-in-your-organization#policies-for-suggestion-matching)."

The response contains the total number of new seats that were created and existing seats that were refreshed.

OAuth app tokens and personal access tokens (classic) need either the `manage_billing:copilot` or `admin:org` scopes to use this endpoint.

### Fine-grained access tokens for "Add teams to the Copilot subscription for an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have at least one of the following permission sets:

- "GitHub Copilot Business" organization permissions (write)
- "Administration" organization permissions (write)

### Parameters for "Add teams to the Copilot subscription for an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| selected_teamsarray of stringsRequiredList of team names within the organization to which to grant access to GitHub Copilot. |

### HTTP response status codes for "Add teams to the Copilot subscription for an organization"

| Status code | Description |
| --- | --- |
| 201 | OK |
| 401 | Requires authentication |
| 403 | Forbidden |
| 404 | Resource not found |
| 422 | Copilot Business or Enterprise is not enabled for this organization, billing has not been set up for this organization, a public code suggestions policy has not been set for this organization, or the organization's Copilot access setting is set to enable Copilot for all users or is unconfigured. |
| 500 | Internal Error |

### Code samples for "Add teams to the Copilot subscription for an organization"

#### Request example

post/orgs/{org}/copilot/billing/selected_teams

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/copilot/billing/selected_teams \
  -d '{"selected_teams":["engteam1","engteam2","engteam3"]}'`

OK

-
-

`Status: 201``{
"seats_created": 5
}`

## Remove teams from the Copilot subscription for an organization

Note

This endpoint is in public preview and is subject to change.

Sets seats for all members of each team specified to "pending cancellation".
This will cause the members of the specified team(s) to lose access to GitHub Copilot at the end of the current billing cycle unless they retain access through another team.
For more information about disabling access to Copilot, see "[Revoking access to Copilot for members of your organization](https://docs.github.com/copilot/managing-copilot/managing-github-copilot-in-your-organization/managing-access-to-github-copilot-in-your-organization/revoking-access-to-copilot-for-members-of-your-organization)."

Only organization owners can cancel Copilot seats for their organization members.

The response contains the total number of seats set to "pending cancellation".

OAuth app tokens and personal access tokens (classic) need either the `manage_billing:copilot` or `admin:org` scopes to use this endpoint.

### Fine-grained access tokens for "Remove teams from the Copilot subscription for an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have at least one of the following permission sets:

- "GitHub Copilot Business" organization permissions (write)
- "Administration" organization permissions (write)

### Parameters for "Remove teams from the Copilot subscription for an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| selected_teamsarray of stringsRequiredThe names of teams from which to revoke access to GitHub Copilot. |

### HTTP response status codes for "Remove teams from the Copilot subscription for an organization"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 401 | Requires authentication |
| 403 | Forbidden |
| 404 | Resource not found |
| 422 | Copilot Business or Enterprise is not enabled for this organization, billing has not been set up for this organization, a public code suggestions policy has not been set for this organization, or the organization's Copilot access setting is set to enable Copilot for all users or is unconfigured. |
| 500 | Internal Error |

### Code samples for "Remove teams from the Copilot subscription for an organization"

#### Request example

delete/orgs/{org}/copilot/billing/selected_teams

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/copilot/billing/selected_teams \
  -d '{"selected_teams":["engteam1","engteam2","engteam3"]}'`

OK

-
-

`Status: 200``{
"seats_cancelled": 5
}`

## Add users to the Copilot subscription for an organization

Note

This endpoint is in public preview and is subject to change.

Purchases a GitHub Copilot seat for each user specified.
The organization will be billed for each seat based on the organization's Copilot plan. For more information about Copilot pricing, see "[About billing for GitHub Copilot in your organization](https://docs.github.com/copilot/managing-copilot/managing-github-copilot-in-your-organization/managing-the-copilot-subscription-for-your-organization/about-billing-for-github-copilot-in-your-organization)."

Only organization owners can purchase Copilot seats for their organization members. The organization must have a Copilot Business or Copilot Enterprise subscription and a configured suggestion matching policy.
For more information about setting up a Copilot subscription, see "[Subscribing to Copilot for your organization](https://docs.github.com/copilot/managing-copilot/managing-github-copilot-in-your-organization/managing-the-copilot-subscription-for-your-organization/subscribing-to-copilot-for-your-organization)."
For more information about setting a suggestion matching policy, see "[Managing policies for Copilot in your organization](https://docs.github.com/copilot/managing-copilot/managing-github-copilot-in-your-organization/setting-policies-for-copilot-in-your-organization/managing-policies-for-copilot-in-your-organization#policies-for-suggestion-matching)."

The response contains the total number of new seats that were created and existing seats that were refreshed.

OAuth app tokens and personal access tokens (classic) need either the `manage_billing:copilot` or `admin:org` scopes to use this endpoint.

### Fine-grained access tokens for "Add users to the Copilot subscription for an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have at least one of the following permission sets:

- "GitHub Copilot Business" organization permissions (write)
- "Administration" organization permissions (write)

### Parameters for "Add users to the Copilot subscription for an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| selected_usernamesarray of stringsRequiredThe usernames of the organization members to be granted access to GitHub Copilot. |

### HTTP response status codes for "Add users to the Copilot subscription for an organization"

| Status code | Description |
| --- | --- |
| 201 | OK |
| 401 | Requires authentication |
| 403 | Forbidden |
| 404 | Resource not found |
| 422 | Copilot Business or Enterprise is not enabled for this organization, billing has not been set up for this organization, a public code suggestions policy has not been set for this organization, or the organization's Copilot access setting is set to enable Copilot for all users or is unconfigured. |
| 500 | Internal Error |

### Code samples for "Add users to the Copilot subscription for an organization"

#### Request example

post/orgs/{org}/copilot/billing/selected_users

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/copilot/billing/selected_users \
  -d '{"selected_usernames":["cooluser1","hacker2","octocat"]}'`

OK

-
-

`Status: 201``{
"seats_created": 5
}`

## Remove users from the Copilot subscription for an organization

Note

This endpoint is in public preview and is subject to change.

Sets seats for all users specified to "pending cancellation".
This will cause the specified users to lose access to GitHub Copilot at the end of the current billing cycle unless they retain access through team membership.
For more information about disabling access to Copilot, see "[Revoking access to Copilot for members of your organization](https://docs.github.com/copilot/managing-copilot/managing-github-copilot-in-your-organization/managing-access-to-github-copilot-in-your-organization/revoking-access-to-copilot-for-members-of-your-organization)."

Only organization owners can cancel Copilot seats for their organization members.

The response contains the total number of seats set to "pending cancellation".

OAuth app tokens and personal access tokens (classic) need either the `manage_billing:copilot` or `admin:org` scopes to use this endpoint.

### Fine-grained access tokens for "Remove users from the Copilot subscription for an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have at least one of the following permission sets:

- "GitHub Copilot Business" organization permissions (write)
- "Administration" organization permissions (write)

### Parameters for "Remove users from the Copilot subscription for an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| selected_usernamesarray of stringsRequiredThe usernames of the organization members for which to revoke access to GitHub Copilot. |

### HTTP response status codes for "Remove users from the Copilot subscription for an organization"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 401 | Requires authentication |
| 403 | Forbidden |
| 404 | Resource not found |
| 422 | Copilot Business or Enterprise is not enabled for this organization, billing has not been set up for this organization, a public code suggestions policy has not been set for this organization, the seat management setting is set to enable Copilot for all users or is unconfigured, or a user's seat cannot be cancelled because it was assigned to them via a team. |
| 500 | Internal Error |

### Code samples for "Remove users from the Copilot subscription for an organization"

#### Request example

delete/orgs/{org}/copilot/billing/selected_users

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/copilot/billing/selected_users \
  -d '{"selected_usernames":["cooluser1","hacker2","octocat"]}'`

OK

-
-

`Status: 200``{
"seats_cancelled": 5
}`

## Get Copilot seat assignment details for a user

Note

This endpoint is in public preview and is subject to change.

Gets the GitHub Copilot seat details for a member of an organization who currently has access to GitHub Copilot.

The seat object contains information about the user's most recent Copilot activity. Users must have telemetry enabled in their IDE for Copilot in the IDE activity to be reflected in `last_activity_at`.
For more information about activity data, see [Metrics data properties for GitHub Copilot](https://docs.github.com/copilot/reference/metrics-data).

Only organization owners can view Copilot seat assignment details for members of their organization.

OAuth app tokens and personal access tokens (classic) need either the `manage_billing:copilot` or `read:org` scopes to use this endpoint.

### Fine-grained access tokens for "Get Copilot seat assignment details for a user"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have at least one of the following permission sets:

- "GitHub Copilot Business" organization permissions (read)
- "Administration" organization permissions (read)

### Parameters for "Get Copilot seat assignment details for a user"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| usernamestringRequiredThe handle for the GitHub user account. |

### HTTP response status codes for "Get Copilot seat assignment details for a user"

| Status code | Description |
| --- | --- |
| 200 | The user's GitHub Copilot seat details, including usage. |
| 401 | Requires authentication |
| 403 | Forbidden |
| 404 | Resource not found |
| 422 | Copilot Business or Enterprise is not enabled for this organization or the user has a pending organization invitation. |
| 500 | Internal Error |

### Code samples for "Get Copilot seat assignment details for a user"

#### Request example

get/orgs/{org}/members/{username}/copilot

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/members/USERNAME/copilot`

The user's GitHub Copilot seat details, including usage.

-
-

`Status: 200``{
"created_at": "2021-08-03T18:00:00-06:00",
"updated_at": "2021-09-23T15:00:00-06:00",
"pending_cancellation_date": null,
"last_activity_at": "2021-10-14T00:53:32-06:00",
"last_activity_editor": "vscode/1.77.3/copilot/1.86.82",
"last_authenticated_at": "2021-10-14T00:53:32-06:00",
"plan_type": "business",
"assignee": {
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
},
"assigning_team": {
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
}`
