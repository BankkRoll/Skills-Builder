# REST API endpoints for collaborators and more

# REST API endpoints for collaborators

> Use the REST API to manage collaborators for a repository.

## List repository collaborators

For organization-owned repositories, the list of collaborators includes outside collaborators, organization members that are direct collaborators, organization members with access through team memberships, organization members with access through default organization permissions, and organization owners.
The `permissions` hash returned in the response contains the base role permissions of the collaborator. The `role_name` is the highest role assigned to the collaborator after considering all sources of grants, including: repo, teams, organization, and enterprise.
There is presently not a way to differentiate between an organization level grant and a repository level grant from this endpoint response.

Team members will include the members of child teams.

The authenticated user must have write, maintain, or admin privileges on the repository to use this endpoint. For organization-owned repositories, the authenticated user needs to be a member of the organization.
OAuth app tokens and personal access tokens (classic) need the `read:org` and `repo` scopes to use this endpoint.

### Fine-grained access tokens for "List repository collaborators"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Metadata" repository permissions (read)

### Parameters for "List repository collaborators"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| affiliationstringFilter collaborators returned by their affiliation.outsidemeans all outside collaborators of an organization-owned repository.directmeans all collaborators with permissions to an organization-owned repository, regardless of organization membership status.allmeans all collaborators the authenticated user can see.Default:allCan be one of:outside,direct,all |
| permissionstringFilter collaborators by the permissions they have on the repository. If not specified, all collaborators will be returned.Can be one of:pull,triage,push,maintain,admin |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| pageintegerThe page number of the results to fetch. For more information, see "Using pagination in the REST API."Default:1 |

### HTTP response status codes for "List repository collaborators"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |

### Code samples for "List repository collaborators"

#### Request example

get/repos/{owner}/{repo}/collaborators

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/collaborators`

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
"site_admin": false,
"permissions": {
"pull": true,
"triage": true,
"push": true,
"maintain": false,
"admin": false
},
"role_name": "write"
}
]`

## Check if a user is a repository collaborator

For organization-owned repositories, the list of collaborators includes outside collaborators, organization members that are direct collaborators, organization members with access through team memberships, organization members with access through default organization permissions, and organization owners.

Team members will include the members of child teams.

The authenticated user must have push access to the repository to use this endpoint.

OAuth app tokens and personal access tokens (classic) need the `read:org` and `repo` scopes to use this endpoint.

### Fine-grained access tokens for "Check if a user is a repository collaborator"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Metadata" repository permissions (read)

### Parameters for "Check if a user is a repository collaborator"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| usernamestringRequiredThe handle for the GitHub user account. |

### HTTP response status codes for "Check if a user is a repository collaborator"

| Status code | Description |
| --- | --- |
| 204 | Response if user is a collaborator |
| 404 | Not Found if user is not a collaborator |

### Code samples for "Check if a user is a repository collaborator"

#### Request example

get/repos/{owner}/{repo}/collaborators/{username}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/collaborators/USERNAME`

Response if user is a collaborator

`Status: 204`

## Add a repository collaborator

Add a user to a repository with a specified level of access. If the repository is owned by an organization, this API does not add the user to the organization - a user that has repository access without being an organization member is called an "outside collaborator" (if they are not an Enterprise Managed User) or a "repository collaborator" if they are an Enterprise Managed User. These users are exempt from some organization policies - see "[Adding outside collaborators to repositories](https://docs.github.com/organizations/managing-user-access-to-your-organizations-repositories/managing-outside-collaborators/adding-outside-collaborators-to-repositories-in-your-organization)" to learn more about these collaborator types.

This endpoint triggers [notifications](https://docs.github.com/github/managing-subscriptions-and-notifications-on-github/about-notifications).

Adding an outside collaborator may be restricted by enterprise and organization administrators. For more information, see "[Enforcing repository management policies in your enterprise](https://docs.github.com/admin/policies/enforcing-policies-for-your-enterprise/enforcing-repository-management-policies-in-your-enterprise#enforcing-a-policy-for-inviting-outside-collaborators-to-repositories)" and "[Setting permissions for adding outside collaborators](https://docs.github.com/organizations/managing-organization-settings/setting-permissions-for-adding-outside-collaborators)" for organization settings.

For more information on permission levels, see "[Repository permission levels for an organization](https://docs.github.com/github/setting-up-and-managing-organizations-and-teams/repository-permission-levels-for-an-organization#permission-levels-for-repositories-owned-by-an-organization)". There are restrictions on which permissions can be granted to organization members when an organization base role is in place. In this case, the role being given must be equal to or higher than the org base permission. Otherwise, the request will fail with:

```
Cannot assign {member} permission of {role name}
```

Note that, if you choose not to pass any parameters, you'll need to set `Content-Length` to zero when calling out to this endpoint. For more information, see "[HTTP method](https://docs.github.com/rest/guides/getting-started-with-the-rest-api#http-method)."

The invitee will receive a notification that they have been invited to the repository, which they must accept or decline. They may do this via the notifications page, the email they receive, or by using the [API](https://docs.github.com/rest/collaborators/invitations).

For Enterprise Managed Users, this endpoint does not send invitations - these users are automatically added to organizations and repositories. Enterprise Managed Users can only be added to organizations and repositories within their enterprise.

**Updating an existing collaborator's permission level**

The endpoint can also be used to change the permissions of an existing collaborator without first removing and re-adding the collaborator. To change the permissions, use the same endpoint and pass a different `permission` parameter. The response will be a `204`, with no other indication that the permission level changed.

**Rate limits**

You are limited to sending 50 invitations to a repository per 24 hour period. Note there is no limit if you are inviting organization members to an organization repository.

### Fine-grained access tokens for "Add a repository collaborator"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Add a repository collaborator"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| usernamestringRequiredThe handle for the GitHub user account. |

| Name, Type, Description |
| --- |
| permissionstringThe permission to grant the collaborator.Only valid on organization-owned repositories.We accept the following permissions to be set:pull,triage,push,maintain,adminand you can also specify a custom repository role name, if the owning organization has defined any.Default:push |

### HTTP response status codes for "Add a repository collaborator"

| Status code | Description |
| --- | --- |
| 201 | Response when a new invitation is created |
| 204 | Response when:an existing collaborator is added as a collaboratoran organization member is added as an individual collaboratoran existing team member (whose team is also a repository collaborator) is added as an individual collaborator |
| 403 | Forbidden |
| 422 | Response when:validation failed, or the endpoint has been spammedan Enterprise Managed User (EMU) account was invited to a repository in an enterprise with personal user accounts |

### Code samples for "Add a repository collaborator"

#### Request example

put/repos/{owner}/{repo}/collaborators/{username}

-
-
-

`curl -L \
  -X PUT \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/collaborators/USERNAME \
  -d '{"permission":"triage"}'`

Response when a new invitation is created

-
-

`Status: 201``{
"id": 1,
"node_id": "MDEwOlJlcG9zaXRvcnkxMjk2MjY5",
"repository": {
"id": 1296269,
"node_id": "MDEwOlJlcG9zaXRvcnkxMjk2MjY5",
"name": "Hello-World",
"full_name": "octocat/Hello-World",
"owner": {
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
"private": false,
"html_url": "https://github.com/octocat/Hello-World",
"description": "This your first repo!",
"fork": false,
"url": "https://api.github.com/repos/octocat/Hello-World",
"archive_url": "https://api.github.com/repos/octocat/Hello-World/{archive_format}{/ref}",
"assignees_url": "https://api.github.com/repos/octocat/Hello-World/assignees{/user}",
"blobs_url": "https://api.github.com/repos/octocat/Hello-World/git/blobs{/sha}",
"branches_url": "https://api.github.com/repos/octocat/Hello-World/branches{/branch}",
"collaborators_url": "https://api.github.com/repos/octocat/Hello-World/collaborators{/collaborator}",
"comments_url": "https://api.github.com/repos/octocat/Hello-World/comments{/number}",
"commits_url": "https://api.github.com/repos/octocat/Hello-World/commits{/sha}",
"compare_url": "https://api.github.com/repos/octocat/Hello-World/compare/{base}...{head}",
"contents_url": "https://api.github.com/repos/octocat/Hello-World/contents/{+path}",
"contributors_url": "https://api.github.com/repos/octocat/Hello-World/contributors",
"deployments_url": "https://api.github.com/repos/octocat/Hello-World/deployments",
"downloads_url": "https://api.github.com/repos/octocat/Hello-World/downloads",
"events_url": "https://api.github.com/repos/octocat/Hello-World/events",
"forks_url": "https://api.github.com/repos/octocat/Hello-World/forks",
"git_commits_url": "https://api.github.com/repos/octocat/Hello-World/git/commits{/sha}",
"git_refs_url": "https://api.github.com/repos/octocat/Hello-World/git/refs{/sha}",
"git_tags_url": "https://api.github.com/repos/octocat/Hello-World/git/tags{/sha}",
"git_url": "git:github.com/octocat/Hello-World.git",
"issue_comment_url": "https://api.github.com/repos/octocat/Hello-World/issues/comments{/number}",
"issue_events_url": "https://api.github.com/repos/octocat/Hello-World/issues/events{/number}",
"issues_url": "https://api.github.com/repos/octocat/Hello-World/issues{/number}",
"keys_url": "https://api.github.com/repos/octocat/Hello-World/keys{/key_id}",
"labels_url": "https://api.github.com/repos/octocat/Hello-World/labels{/name}",
"languages_url": "https://api.github.com/repos/octocat/Hello-World/languages",
"merges_url": "https://api.github.com/repos/octocat/Hello-World/merges",
"milestones_url": "https://api.github.com/repos/octocat/Hello-World/milestones{/number}",
"notifications_url": "https://api.github.com/repos/octocat/Hello-World/notifications{?since,all,participating}",
"pulls_url": "https://api.github.com/repos/octocat/Hello-World/pulls{/number}",
"releases_url": "https://api.github.com/repos/octocat/Hello-World/releases{/id}",
"ssh_url": "git@github.com:octocat/Hello-World.git",
"stargazers_url": "https://api.github.com/repos/octocat/Hello-World/stargazers",
"statuses_url": "https://api.github.com/repos/octocat/Hello-World/statuses/{sha}",
"subscribers_url": "https://api.github.com/repos/octocat/Hello-World/subscribers",
"subscription_url": "https://api.github.com/repos/octocat/Hello-World/subscription",
"tags_url": "https://api.github.com/repos/octocat/Hello-World/tags",
"teams_url": "https://api.github.com/repos/octocat/Hello-World/teams",
"trees_url": "https://api.github.com/repos/octocat/Hello-World/git/trees{/sha}",
"hooks_url": "http://api.github.com/repos/octocat/Hello-World/hooks"
},
"invitee": {
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
"inviter": {
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
"permissions": "write",
"created_at": "2016-06-13T14:52:50-05:00",
"url": "https://api.github.com/user/repository_invitations/1296269",
"html_url": "https://github.com/octocat/Hello-World/invitations"
}`

## Remove a repository collaborator

Removes a collaborator from a repository.

To use this endpoint, the authenticated user must either be an administrator of the repository or target themselves for removal.

This endpoint also:

- Cancels any outstanding invitations sent by the collaborator
- Unassigns the user from any issues
- Removes access to organization projects if the user is not an organization member and is not a collaborator on any other organization repositories.
- Unstars the repository
- Updates access permissions to packages

Removing a user as a collaborator has the following effects on forks:

- If the user had access to a fork through their membership to this repository, the user will also be removed from the fork.
- If the user had their own fork of the repository, the fork will be deleted.
- If the user still has read access to the repository, open pull requests by this user from a fork will be denied.

Note

A user can still have access to the repository through organization permissions like base repository permissions.

Although the API responds immediately, the additional permission updates might take some extra time to complete in the background.

For more information on fork permissions, see "[About permissions and visibility of forks](https://docs.github.com/pull-requests/collaborating-with-pull-requests/working-with-forks/about-permissions-and-visibility-of-forks)".

### Fine-grained access tokens for "Remove a repository collaborator"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Remove a repository collaborator"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| usernamestringRequiredThe handle for the GitHub user account. |

### HTTP response status codes for "Remove a repository collaborator"

| Status code | Description |
| --- | --- |
| 204 | No Content when collaborator was removed from the repository. |
| 403 | Forbidden |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Remove a repository collaborator"

#### Request example

delete/repos/{owner}/{repo}/collaborators/{username}

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/collaborators/USERNAME`

No Content when collaborator was removed from the repository.

`Status: 204`

## Get repository permissions for a user

Checks the repository permission and role of a collaborator.

The `permission` attribute provides the legacy base roles of `admin`, `write`, `read`, and `none`, where the
`maintain` role is mapped to `write` and the `triage` role is mapped to `read`.
The `role_name` attribute provides the name of the assigned role, including custom roles. The
`permission` can also be used to determine which base level of access the collaborator has to the repository.

The calculated permissions are the highest role assigned to the collaborator after considering all sources of grants, including: repo, teams, organization, and enterprise.
There is presently not a way to differentiate between an organization level grant and a repository level grant from this endpoint response.

### Fine-grained access tokens for "Get repository permissions for a user"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Metadata" repository permissions (read)

### Parameters for "Get repository permissions for a user"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| usernamestringRequiredThe handle for the GitHub user account. |

### HTTP response status codes for "Get repository permissions for a user"

| Status code | Description |
| --- | --- |
| 200 | if user has admin permissions |
| 404 | Resource not found |

### Code samples for "Get repository permissions for a user"

#### Request example

get/repos/{owner}/{repo}/collaborators/{username}/permission

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/collaborators/USERNAME/permission`

if user has admin permissions

-
-

`Status: 200``{
"permission": "admin",
"role_name": "admin",
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

---

# REST API endpoints for repository invitations

> Use the REST API to view and manage invitations to collaborate on a repository.

## About repository invitations

You can view and manage invitations to collaborate on a repository. The invited users (or external services on behalf of invited users) can choose to accept or decline the invitations.

To add a user as a collaborator, use the Collaborators endpoints instead. For more information, see [REST API endpoints for collaborators](https://docs.github.com/en/rest/collaborators/collaborators#add-a-repository-collaborator).

Note that the `repo:invite` [OAuth scope](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/scopes-for-oauth-apps) grants targeted
access to invitations **without** also granting access to repository code, while the
`repo` scope grants permission to code as well as invitations.
