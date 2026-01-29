# REST API endpoints for organization members

# REST API endpoints for organization members

> Use the REST API to manage memberships in your organization.

## List failed organization invitations

The return hash contains `failed_at` and `failed_reason` fields which represent the time at which the invitation failed and the reason for the failure.

### Fine-grained access tokens for "List failed organization invitations"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Members" organization permissions (read)

### Parameters for "List failed organization invitations"

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

### HTTP response status codes for "List failed organization invitations"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |

### Code samples for "List failed organization invitations"

#### Request example

get/orgs/{org}/failed_invitations

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/failed_invitations`

Response

-
-

`Status: 200``[
{
"id": 1,
"login": "monalisa",
"node_id": "MDQ6VXNlcjE=",
"email": "octocat@github.com",
"role": "direct_member",
"created_at": "2016-11-30T06:46:10-08:00",
"failed_at": "",
"failed_reason": "",
"inviter": {
"login": "other_user",
"id": 1,
"node_id": "MDQ6VXNlcjE=",
"avatar_url": "https://github.com/images/error/other_user_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/other_user",
"html_url": "https://github.com/other_user",
"followers_url": "https://api.github.com/users/other_user/followers",
"following_url": "https://api.github.com/users/other_user/following{/other_user}",
"gists_url": "https://api.github.com/users/other_user/gists{/gist_id}",
"starred_url": "https://api.github.com/users/other_user/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/other_user/subscriptions",
"organizations_url": "https://api.github.com/users/other_user/orgs",
"repos_url": "https://api.github.com/users/other_user/repos",
"events_url": "https://api.github.com/users/other_user/events{/privacy}",
"received_events_url": "https://api.github.com/users/other_user/received_events",
"type": "User",
"site_admin": false
},
"team_count": 2,
"invitation_teams_url": "https://api.github.com/organizations/2/invitations/1/teams",
"invitation_source": "member"
}
]`

## List pending organization invitations

The return hash contains a `role` field which refers to the Organization
Invitation role and will be one of the following values: `direct_member`, `admin`,
`billing_manager`, or `hiring_manager`. If the invitee is not a GitHub
member, the `login` field in the return hash will be `null`.

### Fine-grained access tokens for "List pending organization invitations"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Members" organization permissions (read)

### Parameters for "List pending organization invitations"

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
| rolestringFilter invitations by their member role.Default:allCan be one of:all,admin,direct_member,billing_manager,hiring_manager |
| invitation_sourcestringFilter invitations by their invitation source.Default:allCan be one of:all,member,scim |

### HTTP response status codes for "List pending organization invitations"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |

### Code samples for "List pending organization invitations"

#### Request example

get/orgs/{org}/invitations

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/invitations`

Response

-
-

`Status: 200``[
{
"id": 1,
"login": "monalisa",
"node_id": "MDQ6VXNlcjE=",
"email": "octocat@github.com",
"role": "direct_member",
"created_at": "2016-11-30T06:46:10-08:00",
"failed_at": "",
"failed_reason": "",
"inviter": {
"login": "other_user",
"id": 1,
"node_id": "MDQ6VXNlcjE=",
"avatar_url": "https://github.com/images/error/other_user_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/other_user",
"html_url": "https://github.com/other_user",
"followers_url": "https://api.github.com/users/other_user/followers",
"following_url": "https://api.github.com/users/other_user/following{/other_user}",
"gists_url": "https://api.github.com/users/other_user/gists{/gist_id}",
"starred_url": "https://api.github.com/users/other_user/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/other_user/subscriptions",
"organizations_url": "https://api.github.com/users/other_user/orgs",
"repos_url": "https://api.github.com/users/other_user/repos",
"events_url": "https://api.github.com/users/other_user/events{/privacy}",
"received_events_url": "https://api.github.com/users/other_user/received_events",
"type": "User",
"site_admin": false
},
"team_count": 2,
"invitation_teams_url": "https://api.github.com/organizations/2/invitations/1/teams",
"invitation_source": "member"
}
]`

## Create an organization invitation

Invite people to an organization by using their GitHub user ID or their email address. In order to create invitations in an organization, the authenticated user must be an organization owner.

This endpoint triggers [notifications](https://docs.github.com/github/managing-subscriptions-and-notifications-on-github/about-notifications). Creating content too quickly using this endpoint may result in secondary rate limiting. For more information, see "[Rate limits for the API](https://docs.github.com/rest/using-the-rest-api/rate-limits-for-the-rest-api#about-secondary-rate-limits)"
and "[Best practices for using the REST API](https://docs.github.com/rest/guides/best-practices-for-using-the-rest-api)."

### Fine-grained access tokens for "Create an organization invitation"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Members" organization permissions (write)

### Parameters for "Create an organization invitation"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| invitee_idintegerRequired unless you provideemail. GitHub user ID for the person you are inviting. |
| emailstringRequired unless you provideinvitee_id. Email address of the person you are inviting, which can be an existing GitHub user. |
| rolestringThe role for the new member.admin- Organization owners with full administrative rights to the organization and complete access to all repositories and teams.direct_member- Non-owner organization members with ability to see other members and join teams by invitation.billing_manager- Non-owner organization members with ability to manage the billing settings of your organization.reinstate- The previous role assigned to the invitee before they were removed from your organization. Can be one of the roles listed above. Only works if the invitee was previously part of your organization.Default:direct_memberCan be one of:admin,direct_member,billing_manager,reinstate |
| team_idsarray of integersSpecify IDs for the teams you want to invite new members to. |

### HTTP response status codes for "Create an organization invitation"

| Status code | Description |
| --- | --- |
| 201 | Created |
| 404 | Resource not found |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Create an organization invitation"

#### Request example

post/orgs/{org}/invitations

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/invitations \
  -d '{"email":"octocat@github.com","role":"direct_member","team_ids":[12,26]}'`

Response

-
-

`Status: 201``{
"id": 1,
"login": "monalisa",
"node_id": "MDQ6VXNlcjE=",
"email": "octocat@github.com",
"role": "direct_member",
"created_at": "2016-11-30T06:46:10-08:00",
"inviter": {
"login": "other_user",
"id": 1,
"node_id": "MDQ6VXNlcjE=",
"avatar_url": "https://github.com/images/error/other_user_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/other_user",
"html_url": "https://github.com/other_user",
"followers_url": "https://api.github.com/users/other_user/followers",
"following_url": "https://api.github.com/users/other_user/following{/other_user}",
"gists_url": "https://api.github.com/users/other_user/gists{/gist_id}",
"starred_url": "https://api.github.com/users/other_user/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/other_user/subscriptions",
"organizations_url": "https://api.github.com/users/other_user/orgs",
"repos_url": "https://api.github.com/users/other_user/repos",
"events_url": "https://api.github.com/users/other_user/events{/privacy}",
"received_events_url": "https://api.github.com/users/other_user/received_events",
"type": "User",
"site_admin": false
},
"team_count": 2,
"invitation_teams_url": "https://api.github.com/organizations/2/invitations/1/teams",
"invitation_source": "member"
}`

## Cancel an organization invitation

Cancel an organization invitation. In order to cancel an organization invitation, the authenticated user must be an organization owner.

This endpoint triggers [notifications](https://docs.github.com/github/managing-subscriptions-and-notifications-on-github/about-notifications).

### Fine-grained access tokens for "Cancel an organization invitation"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Members" organization permissions (write)

### Parameters for "Cancel an organization invitation"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| invitation_idintegerRequiredThe unique identifier of the invitation. |

### HTTP response status codes for "Cancel an organization invitation"

| Status code | Description |
| --- | --- |
| 204 | No Content |
| 404 | Resource not found |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Cancel an organization invitation"

#### Request example

delete/orgs/{org}/invitations/{invitation_id}

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/invitations/INVITATION_ID`

Response

`Status: 204`

## List organization invitation teams

List all teams associated with an invitation. In order to see invitations in an organization, the authenticated user must be an organization owner.

### Fine-grained access tokens for "List organization invitation teams"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Members" organization permissions (read)

### Parameters for "List organization invitation teams"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| invitation_idintegerRequiredThe unique identifier of the invitation. |

| Name, Type, Description |
| --- |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| pageintegerThe page number of the results to fetch. For more information, see "Using pagination in the REST API."Default:1 |

### HTTP response status codes for "List organization invitation teams"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |

### Code samples for "List organization invitation teams"

#### Request example

get/orgs/{org}/invitations/{invitation_id}/teams

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/invitations/INVITATION_ID/teams`

Response

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

## List organization members

List all users who are members of an organization. If the authenticated user is also a member of this organization then both concealed and public members will be returned.

### Fine-grained access tokens for "List organization members"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Members" organization permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "List organization members"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| filterstringFilter members returned in the list.2fa_disabledmeans that only members withouttwo-factor authenticationenabled will be returned.2fa_insecuremeans that only members withinsecure 2FA methodswill be returned. These options are only available for organization owners.Default:allCan be one of:2fa_disabled,2fa_insecure,all |
| rolestringFilter members returned by their role.Default:allCan be one of:all,admin,member |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| pageintegerThe page number of the results to fetch. For more information, see "Using pagination in the REST API."Default:1 |

### HTTP response status codes for "List organization members"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "List organization members"

#### Request example

get/orgs/{org}/members

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/members`

Response

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

## Check organization membership for a user

Check if a user is, publicly or privately, a member of the organization.

### Fine-grained access tokens for "Check organization membership for a user"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Members" organization permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "Check organization membership for a user"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| usernamestringRequiredThe handle for the GitHub user account. |

### HTTP response status codes for "Check organization membership for a user"

| Status code | Description |
| --- | --- |
| 204 | Response if requester is an organization member and user is a member |
| 302 | Response if requester is not an organization member |
| 404 | Not Found if requester is an organization member and user is not a member |

### Code samples for "Check organization membership for a user"

#### Request example

get/orgs/{org}/members/{username}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/members/USERNAME`

Response if requester is an organization member and user is a member

`Status: 204`

## Remove an organization member

Removing a user from this list will remove them from all teams and they will no longer have any access to the organization's repositories.

Note

If a user has both direct membership in the organization as well as indirect membership via an enterprise team, only their direct membership will be removed. Their indirect membership via an enterprise team remains until the user is removed from the enterprise team.

### Fine-grained access tokens for "Remove an organization member"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Members" organization permissions (write)

### Parameters for "Remove an organization member"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| usernamestringRequiredThe handle for the GitHub user account. |

### HTTP response status codes for "Remove an organization member"

| Status code | Description |
| --- | --- |
| 204 | No Content |
| 403 | Forbidden |

### Code samples for "Remove an organization member"

#### Request example

delete/orgs/{org}/members/{username}

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/members/USERNAME`

Response

`Status: 204`

## Get organization membership for a user

In order to get a user's membership with an organization, the authenticated user must be an organization member. The `state` parameter in the response can be used to identify the user's membership status.

### Fine-grained access tokens for "Get organization membership for a user"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Members" organization permissions (read)

### Parameters for "Get organization membership for a user"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| usernamestringRequiredThe handle for the GitHub user account. |

### HTTP response status codes for "Get organization membership for a user"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 403 | Forbidden |
| 404 | Resource not found |

### Code samples for "Get organization membership for a user"

#### Request example

get/orgs/{org}/memberships/{username}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/memberships/USERNAME`

Response if user has an active admin membership with organization

-
-

`Status: 200``{
"url": "https://api.github.com/orgs/octocat/memberships/defunkt",
"state": "active",
"role": "admin",
"organization_url": "https://api.github.com/orgs/octocat",
"direct_membership": true,
"enterprise_teams_providing_indirect_membership": [
"ent:justice-league",
"ent:security-managers"
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
"user": {
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
}`

## Set organization membership for a user

Only authenticated organization owners can add a member to the organization or update the member's role.

- If the authenticated user is *adding* a member to the organization, the invited user will receive an email inviting them to the organization. The user's [membership status](https://docs.github.com/rest/orgs/members#get-organization-membership-for-a-user) will be `pending` until they accept the invitation.
- Authenticated users can *update* a user's membership by passing the `role` parameter. If the authenticated user changes a member's role to `admin`, the affected user will receive an email notifying them that they've been made an organization owner. If the authenticated user changes an owner's role to `member`, no email will be sent.

**Rate limits**

To prevent abuse, organization owners are limited to creating 50 organization invitations for an organization within a 24 hour period. If the organization is more than one month old or on a paid plan, the limit is 500 invitations per 24 hour period.

### Fine-grained access tokens for "Set organization membership for a user"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Members" organization permissions (write)

### Parameters for "Set organization membership for a user"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| usernamestringRequiredThe handle for the GitHub user account. |

| Name, Type, Description |
| --- |
| rolestringThe role to give the user in the organization. Can be one of:admin- The user will become an owner of the organization.member- The user will become a non-owner member of the organization.Default:memberCan be one of:admin,member |

### HTTP response status codes for "Set organization membership for a user"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 403 | Forbidden |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Set organization membership for a user"

#### Request example

put/orgs/{org}/memberships/{username}

-
-
-

`curl -L \
  -X PUT \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/memberships/USERNAME \
  -d '{"role":"member"}'`

Response if user has an active admin membership with organization

-
-

`Status: 200``{
"url": "https://api.github.com/orgs/octocat/memberships/defunkt",
"state": "active",
"role": "admin",
"organization_url": "https://api.github.com/orgs/octocat",
"direct_membership": true,
"enterprise_teams_providing_indirect_membership": [
"ent:justice-league",
"ent:security-managers"
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
"user": {
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
}`

## Remove organization membership for a user

In order to remove a user's membership with an organization, the authenticated user must be an organization owner.

If the specified user is an active member of the organization, this will remove them from the organization. If the specified user has been invited to the organization, this will cancel their invitation. The specified user will receive an email notification in both cases.

Note

If a user has both direct membership in the organization as well as indirect membership via an enterprise team, only their direct membership will be removed. Their indirect membership via an enterprise team remains until the user is removed from the enterprise team.

### Fine-grained access tokens for "Remove organization membership for a user"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Members" organization permissions (write)

### Parameters for "Remove organization membership for a user"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| usernamestringRequiredThe handle for the GitHub user account. |

### HTTP response status codes for "Remove organization membership for a user"

| Status code | Description |
| --- | --- |
| 204 | No Content |
| 403 | Forbidden |
| 404 | Resource not found |

### Code samples for "Remove organization membership for a user"

#### Request example

delete/orgs/{org}/memberships/{username}

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/memberships/USERNAME`

Response

`Status: 204`

## List public organization members

Members of an organization can choose to have their membership publicized or not.

### Fine-grained access tokens for "List public organization members"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Members" organization permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "List public organization members"

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

### HTTP response status codes for "List public organization members"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "List public organization members"

#### Request example

get/orgs/{org}/public_members

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/public_members`

Response

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

## Check public organization membership for a user

Check if the provided user is a public member of the organization.

### Fine-grained access tokens for "Check public organization membership for a user"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Members" organization permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "Check public organization membership for a user"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| usernamestringRequiredThe handle for the GitHub user account. |

### HTTP response status codes for "Check public organization membership for a user"

| Status code | Description |
| --- | --- |
| 204 | Response if user is a public member |
| 404 | Not Found if user is not a public member |

### Code samples for "Check public organization membership for a user"

#### Request example

get/orgs/{org}/public_members/{username}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/public_members/USERNAME`

Response if user is a public member

`Status: 204`

## Set public organization membership for the authenticated user

The user can publicize their own membership. (A user cannot publicize the membership for another user.)

Note that you'll need to set `Content-Length` to zero when calling out to this endpoint. For more information, see "[HTTP method](https://docs.github.com/rest/guides/getting-started-with-the-rest-api#http-method)."

### Fine-grained access tokens for "Set public organization membership for the authenticated user"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Members" organization permissions (write)

### Parameters for "Set public organization membership for the authenticated user"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| usernamestringRequiredThe handle for the GitHub user account. |

### HTTP response status codes for "Set public organization membership for the authenticated user"

| Status code | Description |
| --- | --- |
| 204 | No Content |
| 403 | Forbidden |

### Code samples for "Set public organization membership for the authenticated user"

#### Request example

put/orgs/{org}/public_members/{username}

-
-
-

`curl -L \
  -X PUT \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/public_members/USERNAME`

Response

`Status: 204`

## Remove public organization membership for the authenticated user

Removes the public membership for the authenticated user from the specified organization, unless public visibility is enforced by default.

### Fine-grained access tokens for "Remove public organization membership for the authenticated user"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Members" organization permissions (write)

### Parameters for "Remove public organization membership for the authenticated user"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| usernamestringRequiredThe handle for the GitHub user account. |

### HTTP response status codes for "Remove public organization membership for the authenticated user"

| Status code | Description |
| --- | --- |
| 204 | No Content |

### Code samples for "Remove public organization membership for the authenticated user"

#### Request example

delete/orgs/{org}/public_members/{username}

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/public_members/USERNAME`

Response

`Status: 204`

## List organization memberships for the authenticated user

Lists all of the authenticated user's organization memberships.

### Fine-grained access tokens for "List organization memberships for the authenticated user"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token does not require any permissions.

### Parameters for "List organization memberships for the authenticated user"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| statestringIndicates the state of the memberships to return. If not specified, the API returns both active and pending memberships.Can be one of:active,pending |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| pageintegerThe page number of the results to fetch. For more information, see "Using pagination in the REST API."Default:1 |

### HTTP response status codes for "List organization memberships for the authenticated user"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 304 | Not modified |
| 401 | Requires authentication |
| 403 | Forbidden |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "List organization memberships for the authenticated user"

#### Request example

get/user/memberships/orgs

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/user/memberships/orgs`

Response

-
-

`Status: 200``[
{
"url": "https://api.github.com/orgs/octocat/memberships/defunkt",
"state": "active",
"role": "admin",
"organization_url": "https://api.github.com/orgs/octocat",
"direct_membership": true,
"enterprise_teams_providing_indirect_membership": [],
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
"user": {
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
},
{
"url": "https://api.github.com/orgs/invitocat/memberships/defunkt",
"state": "pending",
"role": "admin",
"organization_url": "https://api.github.com/orgs/invitocat",
"direct_membership": false,
"enterprise_teams_providing_indirect_membership": [
"ent:justice-league",
"ent:security-managers"
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
"user": {
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
}
]`

## Get an organization membership for the authenticated user

If the authenticated user is an active or pending member of the organization, this endpoint will return the user's membership. If the authenticated user is not affiliated with the organization, a `404` is returned. This endpoint will return a `403` if the request is made by a GitHub App that is blocked by the organization.

### Fine-grained access tokens for "Get an organization membership for the authenticated user"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Members" organization permissions (read)

### Parameters for "Get an organization membership for the authenticated user"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

### HTTP response status codes for "Get an organization membership for the authenticated user"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 403 | Forbidden |
| 404 | Resource not found |

### Code samples for "Get an organization membership for the authenticated user"

#### Request example

get/user/memberships/orgs/{org}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/user/memberships/orgs/ORG`

Response

-
-

`Status: 200``{
"url": "https://api.github.com/orgs/invitocat/memberships/defunkt",
"state": "pending",
"role": "admin",
"organization_url": "https://api.github.com/orgs/invitocat",
"direct_membership": true,
"enterprise_teams_providing_indirect_membership": [
"ent:justice-league",
"ent:security-managers"
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
"user": {
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
}`

## Update an organization membership for the authenticated user

Converts the authenticated user to an active member of the organization, if that user has a pending invitation from the organization.

### Fine-grained access tokens for "Update an organization membership for the authenticated user"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Members" organization permissions (write)

### Parameters for "Update an organization membership for the authenticated user"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| statestringRequiredThe state that the membership should be in. Only"active"will be accepted.Value:active |

### HTTP response status codes for "Update an organization membership for the authenticated user"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 403 | Forbidden |
| 404 | Resource not found |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Update an organization membership for the authenticated user"

#### Request example

patch/user/memberships/orgs/{org}

-
-
-

`curl -L \
  -X PATCH \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/user/memberships/orgs/ORG \
  -d '{"state":"active"}'`

Response

-
-

`Status: 200``{
"url": "https://api.github.com/orgs/octocat/memberships/defunkt",
"state": "active",
"role": "admin",
"organization_url": "https://api.github.com/orgs/octocat",
"direct_membership": true,
"enterprise_teams_providing_indirect_membership": [
"ent:justice-league",
"ent:security-managers"
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
"user": {
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
}`
