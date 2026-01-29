# REST API endpoints for personal access tokens and more

# REST API endpoints for personal access tokens

> Use the REST API to manage fine-grained personal access tokens.

## List requests to access organization resources with fine-grained personal access tokens

Lists requests from organization members to access organization resources with a fine-grained personal access token.

Only GitHub Apps can use this endpoint.

### Fine-grained access tokens for "List requests to access organization resources with fine-grained personal access tokens"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)

The fine-grained token must have the following permission set:

- "Personal access token requests" organization permissions (read)

### Parameters for "List requests to access organization resources with fine-grained personal access tokens"

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
| sortstringThe property by which to sort the results.Default:created_atValue:created_at |
| directionstringThe direction to sort the results by.Default:descCan be one of:asc,desc |
| ownerarrayA list of owner usernames to use to filter the results. |
| repositorystringThe name of the repository to use to filter the results. |
| permissionstringThe permission to use to filter the results. |
| last_used_beforestringOnly show fine-grained personal access tokens used before the given time. This is a timestamp inISO 8601format:YYYY-MM-DDTHH:MM:SSZ. |
| last_used_afterstringOnly show fine-grained personal access tokens used after the given time. This is a timestamp inISO 8601format:YYYY-MM-DDTHH:MM:SSZ. |
| token_idarrayThe ID of the token |

### HTTP response status codes for "List requests to access organization resources with fine-grained personal access tokens"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 403 | Forbidden |
| 404 | Resource not found |
| 422 | Validation failed, or the endpoint has been spammed. |
| 500 | Internal Error |

### Code samples for "List requests to access organization resources with fine-grained personal access tokens"

#### Request example

get/orgs/{org}/personal-access-token-requests

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/personal-access-token-requests`

Response

-
-

`Status: 200``[
{
"id": 25381,
"reason": "I need to access the GitHub API",
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
"repository_selection": "all",
"repositories_url": "https://api.github.com/organizations/652551/personal-access-token-requests/25381/repositories",
"permissions": {
"organization": {
"members": "read"
},
"repository": {
"metadata": "read"
}
},
"created_at": "2023-05-16T08:47:09.000-07:00",
"token_id": 98716,
"token_name": "Some Token",
"token_expired": false,
"token_expires_at": "2023-11-16T08:47:09.000-07:00",
"token_last_used_at": null
}
]`

## Review requests to access organization resources with fine-grained personal access tokens

Approves or denies multiple pending requests to access organization resources via a fine-grained personal access token.

Only GitHub Apps can use this endpoint.

### Fine-grained access tokens for "Review requests to access organization resources with fine-grained personal access tokens"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)

The fine-grained token must have the following permission set:

- "Personal access token requests" organization permissions (write)

### Parameters for "Review requests to access organization resources with fine-grained personal access tokens"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| pat_request_idsarray of integersUnique identifiers of the requests for access via fine-grained personal access token. Must be formed of between 1 and 100pat_request_idvalues. |
| actionstringRequiredAction to apply to the requests.Can be one of:approve,deny |
| reasonstring or nullReason for approving or denying the requests. Max 1024 characters. |

### HTTP response status codes for "Review requests to access organization resources with fine-grained personal access tokens"

| Status code | Description |
| --- | --- |
| 202 | Accepted |
| 403 | Forbidden |
| 404 | Resource not found |
| 422 | Validation failed, or the endpoint has been spammed. |
| 500 | Internal Error |

### Code samples for "Review requests to access organization resources with fine-grained personal access tokens"

#### Request example

post/orgs/{org}/personal-access-token-requests

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/personal-access-token-requests \
  -d '{"pat_request_ids":[42,73],"action":"deny","reason":"Access is too broad."}'`

Accepted

-
-

`Status: 202`

## Review a request to access organization resources with a fine-grained personal access token

Approves or denies a pending request to access organization resources via a fine-grained personal access token.

Only GitHub Apps can use this endpoint.

### Fine-grained access tokens for "Review a request to access organization resources with a fine-grained personal access token"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)

The fine-grained token must have the following permission set:

- "Personal access token requests" organization permissions (write)

### Parameters for "Review a request to access organization resources with a fine-grained personal access token"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| pat_request_idintegerRequiredUnique identifier of the request for access via fine-grained personal access token. |

| Name, Type, Description |
| --- |
| actionstringRequiredAction to apply to the request.Can be one of:approve,deny |
| reasonstring or nullReason for approving or denying the request. Max 1024 characters. |

### HTTP response status codes for "Review a request to access organization resources with a fine-grained personal access token"

| Status code | Description |
| --- | --- |
| 204 | A header with no content is returned. |
| 403 | Forbidden |
| 404 | Resource not found |
| 422 | Validation failed, or the endpoint has been spammed. |
| 500 | Internal Error |

### Code samples for "Review a request to access organization resources with a fine-grained personal access token"

#### Request example

post/orgs/{org}/personal-access-token-requests/{pat_request_id}

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/personal-access-token-requests/PAT_REQUEST_ID \
  -d '{"action":"deny","reason":"This request is denied because the access is too broad."}'`

A header with no content is returned.

`Status: 204`

## List repositories requested to be accessed by a fine-grained personal access token

Lists the repositories a fine-grained personal access token request is requesting access to.

Only GitHub Apps can use this endpoint.

### Fine-grained access tokens for "List repositories requested to be accessed by a fine-grained personal access token"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)

The fine-grained token must have the following permission set:

- "Personal access token requests" organization permissions (read)

### Parameters for "List repositories requested to be accessed by a fine-grained personal access token"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| pat_request_idintegerRequiredUnique identifier of the request for access via fine-grained personal access token. |

| Name, Type, Description |
| --- |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| pageintegerThe page number of the results to fetch. For more information, see "Using pagination in the REST API."Default:1 |

### HTTP response status codes for "List repositories requested to be accessed by a fine-grained personal access token"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 403 | Forbidden |
| 404 | Resource not found |
| 500 | Internal Error |

### Code samples for "List repositories requested to be accessed by a fine-grained personal access token"

#### Request example

get/orgs/{org}/personal-access-token-requests/{pat_request_id}/repositories

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/personal-access-token-requests/PAT_REQUEST_ID/repositories`

Response

-
-

`Status: 200``[
{
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
"clone_url": "https://github.com/octocat/Hello-World.git",
"mirror_url": "git:git.example.com/octocat/Hello-World",
"hooks_url": "https://api.github.com/repos/octocat/Hello-World/hooks",
"svn_url": "https://svn.github.com/octocat/Hello-World",
"homepage": "https://github.com",
"language": null,
"forks_count": 9,
"stargazers_count": 80,
"watchers_count": 80,
"size": 108,
"default_branch": "master",
"open_issues_count": 0,
"is_template": false,
"topics": [
"octocat",
"atom",
"electron",
"api"
],
"has_issues": true,
"has_projects": true,
"has_wiki": true,
"has_pages": false,
"has_downloads": true,
"has_discussions": false,
"archived": false,
"disabled": false,
"visibility": "public",
"pushed_at": "2011-01-26T19:06:43Z",
"created_at": "2011-01-26T19:01:12Z",
"updated_at": "2011-01-26T19:14:43Z",
"permissions": {
"admin": false,
"push": false,
"pull": true
},
"security_and_analysis": {
"advanced_security": {
"status": "enabled"
},
"secret_scanning": {
"status": "enabled"
},
"secret_scanning_push_protection": {
"status": "disabled"
},
"secret_scanning_non_provider_patterns": {
"status": "disabled"
}
}
}
]`

## List fine-grained personal access tokens with access to organization resources

Lists approved fine-grained personal access tokens owned by organization members that can access organization resources.

Only GitHub Apps can use this endpoint.

### Fine-grained access tokens for "List fine-grained personal access tokens with access to organization resources"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)

The fine-grained token must have the following permission set:

- "Personal access tokens" organization permissions (read)

### Parameters for "List fine-grained personal access tokens with access to organization resources"

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
| sortstringThe property by which to sort the results.Default:created_atValue:created_at |
| directionstringThe direction to sort the results by.Default:descCan be one of:asc,desc |
| ownerarrayA list of owner usernames to use to filter the results. |
| repositorystringThe name of the repository to use to filter the results. |
| permissionstringThe permission to use to filter the results. |
| last_used_beforestringOnly show fine-grained personal access tokens used before the given time. This is a timestamp inISO 8601format:YYYY-MM-DDTHH:MM:SSZ. |
| last_used_afterstringOnly show fine-grained personal access tokens used after the given time. This is a timestamp inISO 8601format:YYYY-MM-DDTHH:MM:SSZ. |
| token_idarrayThe ID of the token |

### HTTP response status codes for "List fine-grained personal access tokens with access to organization resources"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 403 | Forbidden |
| 404 | Resource not found |
| 422 | Validation failed, or the endpoint has been spammed. |
| 500 | Internal Error |

### Code samples for "List fine-grained personal access tokens with access to organization resources"

#### Request example

get/orgs/{org}/personal-access-tokens

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/personal-access-tokens`

Response

-
-

`Status: 200``[
{
"id": 25381,
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
"repository_selection": "all",
"repositories_url": "https://api.github.com/organizations/652551/personal-access-tokens/25381/repositories",
"permissions": {
"organization": {
"members": "read"
},
"repository": {
"metadata": "read"
}
},
"access_granted_at": "2023-05-16T08:47:09.000-07:00",
"token_id": 98716,
"token_name": "Some Token",
"token_expired": false,
"token_expires_at": "2023-11-16T08:47:09.000-07:00",
"token_last_used_at": null
}
]`

## Update the access to organization resources via fine-grained personal access tokens

Updates the access organization members have to organization resources via fine-grained personal access tokens. Limited to revoking a token's existing access.

Only GitHub Apps can use this endpoint.

### Fine-grained access tokens for "Update the access to organization resources via fine-grained personal access tokens"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)

The fine-grained token must have the following permission set:

- "Personal access tokens" organization permissions (write)

### Parameters for "Update the access to organization resources via fine-grained personal access tokens"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| actionstringRequiredAction to apply to the fine-grained personal access token.Value:revoke |
| pat_idsarray of integersRequiredThe IDs of the fine-grained personal access tokens. |

### HTTP response status codes for "Update the access to organization resources via fine-grained personal access tokens"

| Status code | Description |
| --- | --- |
| 202 | Accepted |
| 403 | Forbidden |
| 404 | Resource not found |
| 422 | Validation failed, or the endpoint has been spammed. |
| 500 | Internal Error |

### Code samples for "Update the access to organization resources via fine-grained personal access tokens"

#### Request example

post/orgs/{org}/personal-access-tokens

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/personal-access-tokens \
  -d '{"action":"revoke","pat_ids":[1296269,1296280]}'`

Accepted

-
-

`Status: 202`

## Update the access a fine-grained personal access token has to organization resources

Updates the access an organization member has to organization resources via a fine-grained personal access token. Limited to revoking the token's existing access. Limited to revoking a token's existing access.

Only GitHub Apps can use this endpoint.

### Fine-grained access tokens for "Update the access a fine-grained personal access token has to organization resources"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)

The fine-grained token must have the following permission set:

- "Personal access tokens" organization permissions (write)

### Parameters for "Update the access a fine-grained personal access token has to organization resources"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| pat_idintegerRequiredThe unique identifier of the fine-grained personal access token. |

| Name, Type, Description |
| --- |
| actionstringRequiredAction to apply to the fine-grained personal access token.Value:revoke |

### HTTP response status codes for "Update the access a fine-grained personal access token has to organization resources"

| Status code | Description |
| --- | --- |
| 204 | A header with no content is returned. |
| 403 | Forbidden |
| 404 | Resource not found |
| 422 | Validation failed, or the endpoint has been spammed. |
| 500 | Internal Error |

### Code samples for "Update the access a fine-grained personal access token has to organization resources"

#### Request example

post/orgs/{org}/personal-access-tokens/{pat_id}

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/personal-access-tokens/PAT_ID \
  -d '{"action":"revoke"}'`

A header with no content is returned.

`Status: 204`

## List repositories a fine-grained personal access token has access to

Lists the repositories a fine-grained personal access token has access to.

Only GitHub Apps can use this endpoint.

### Fine-grained access tokens for "List repositories a fine-grained personal access token has access to"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)

The fine-grained token must have the following permission set:

- "Personal access tokens" organization permissions (read)

### Parameters for "List repositories a fine-grained personal access token has access to"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| pat_idintegerRequiredUnique identifier of the fine-grained personal access token. |

| Name, Type, Description |
| --- |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| pageintegerThe page number of the results to fetch. For more information, see "Using pagination in the REST API."Default:1 |

### HTTP response status codes for "List repositories a fine-grained personal access token has access to"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 403 | Forbidden |
| 404 | Resource not found |
| 500 | Internal Error |

### Code samples for "List repositories a fine-grained personal access token has access to"

#### Request example

get/orgs/{org}/personal-access-tokens/{pat_id}/repositories

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/personal-access-tokens/PAT_ID/repositories`

Response

-
-

`Status: 200``[
{
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
"clone_url": "https://github.com/octocat/Hello-World.git",
"mirror_url": "git:git.example.com/octocat/Hello-World",
"hooks_url": "https://api.github.com/repos/octocat/Hello-World/hooks",
"svn_url": "https://svn.github.com/octocat/Hello-World",
"homepage": "https://github.com",
"language": null,
"forks_count": 9,
"stargazers_count": 80,
"watchers_count": 80,
"size": 108,
"default_branch": "master",
"open_issues_count": 0,
"is_template": false,
"topics": [
"octocat",
"atom",
"electron",
"api"
],
"has_issues": true,
"has_projects": true,
"has_wiki": true,
"has_pages": false,
"has_downloads": true,
"has_discussions": false,
"archived": false,
"disabled": false,
"visibility": "public",
"pushed_at": "2011-01-26T19:06:43Z",
"created_at": "2011-01-26T19:01:12Z",
"updated_at": "2011-01-26T19:14:43Z",
"permissions": {
"admin": false,
"push": false,
"pull": true
},
"security_and_analysis": {
"advanced_security": {
"status": "enabled"
},
"secret_scanning": {
"status": "enabled"
},
"secret_scanning_push_protection": {
"status": "disabled"
},
"secret_scanning_non_provider_patterns": {
"status": "disabled"
}
}
}
]`

---

# REST API endpoints for custom properties

> Use the REST API to create and manage custom properties for an organization.

## About custom properties

You can use the REST API to create and manage custom properties for an organization. You can use custom properties to add metadata to repositories in your organization. For more information, see [Managing custom properties for repositories in your organization](https://docs.github.com/en/organizations/managing-organization-settings/managing-custom-properties-for-repositories-in-your-organization).

---

# REST API endpoints for rule suites

> Use the REST API to manage rule suites for organizations.

## List organization rule suites

Lists suites of rule evaluations at the organization level.
For more information, see "[Managing rulesets for repositories in your organization](https://docs.github.com/organizations/managing-organization-settings/managing-rulesets-for-repositories-in-your-organization#viewing-insights-for-rulesets)."

### Fine-grained access tokens for "List organization rule suites"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" organization permissions (write)

### Parameters for "List organization rule suites"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| refstringThe name of the ref. Cannot contain wildcard characters. Optionally prefix withrefs/heads/to limit to branches orrefs/tags/to limit to tags. Omit the prefix to search across all refs. When specified, only rule evaluations triggered for this ref will be returned. |
| repository_namestringThe name of the repository to filter on. |
| time_periodstringThe time period to filter by.For example,daywill filter for rule suites that occurred in the past 24 hours, andweekwill filter for rule suites that occurred in the past 7 days (168 hours).Default:dayCan be one of:hour,day,week,month |
| actor_namestringThe handle for the GitHub user account to filter on. When specified, only rule evaluations triggered by this actor will be returned. |
| rule_suite_resultstringThe rule suite results to filter on. When specified, only suites with this result will be returned.Default:allCan be one of:pass,fail,bypass,all |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| pageintegerThe page number of the results to fetch. For more information, see "Using pagination in the REST API."Default:1 |

### HTTP response status codes for "List organization rule suites"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |
| 500 | Internal Error |

### Code samples for "List organization rule suites"

#### Request example

get/orgs/{org}/rulesets/rule-suites

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/rulesets/rule-suites`

Response

-
-

`Status: 200``[
{
"id": 21,
"actor_id": 12,
"actor_name": "octocat",
"before_sha": "893f768e172fb1bc9c5d6f3dd48557e45f14e01d",
"after_sha": "dedd88641a362b6b4ea872da4847d6131a164d01",
"ref": "refs/heads/i-see-everything",
"repository_id": 404,
"repository_name": "octo-repo",
"pushed_at": "2023-07-06T08:43:03Z",
"result": "bypass"
},
{
"id": 25,
"actor_id": 11,
"actor_name": "not-octocat",
"before_sha": "48994e4e01ccc943624c6231f172702b82b233cc",
"after_sha": "ecfd5a1025fa271a33ca5608d089476a2df3c9a1",
"ref": "refs/heads/i-am-everything",
"repository_id": 404,
"repository_name": "octo-repo",
"pushed_at": "2023-07-07T08:43:03Z",
"result": "pass",
"evaluation_result": "fail"
}
]`

## Get an organization rule suite

Gets information about a suite of rule evaluations from within an organization.
For more information, see "[Managing rulesets for repositories in your organization](https://docs.github.com/organizations/managing-organization-settings/managing-rulesets-for-repositories-in-your-organization#viewing-insights-for-rulesets)."

### Fine-grained access tokens for "Get an organization rule suite"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" organization permissions (write)

### Parameters for "Get an organization rule suite"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| rule_suite_idintegerRequiredThe unique identifier of the rule suite result.
To get this ID, you can useGET /repos/{owner}/{repo}/rulesets/rule-suitesfor repositories andGET /orgs/{org}/rulesets/rule-suitesfor organizations. |

### HTTP response status codes for "Get an organization rule suite"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |
| 500 | Internal Error |

### Code samples for "Get an organization rule suite"

#### Request example

get/orgs/{org}/rulesets/rule-suites/{rule_suite_id}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/rulesets/rule-suites/RULE_SUITE_ID`

Response

-
-

`Status: 200``{
"id": 21,
"actor_id": 12,
"actor_name": "octocat",
"before_sha": "893f768e172fb1bc9c5d6f3dd48557e45f14e01d",
"after_sha": "dedd88641a362b6b4ea872da4847d6131a164d01",
"ref": "refs/heads/i-see-everything",
"repository_id": 404,
"repository_name": "octo-repo",
"pushed_at": "2023-07-06T08:43:03Z",
"result": "bypass",
"evaluation_result": "fail",
"rule_evaluations": [
{
"rule_source": {
"type": "ruleset",
"id": 2,
"name": "Author email must be a GitHub email address"
},
"enforcement": "active",
"result": "pass",
"rule_type": "commit_author_email_pattern"
},
{
"rule_source": {
"type": "protected_branch"
},
"enforcement": "active",
"result": "fail",
"rule_type": "pull_request",
"details": "Changes must be made through a pull request."
},
{
"rule_source": {
"type": "ruleset",
"id": 3,
"name": "Evaluate commit message pattern"
},
"enforcement": "evaluate",
"result": "fail",
"rule_type": "commit_message_pattern"
}
]
}`
