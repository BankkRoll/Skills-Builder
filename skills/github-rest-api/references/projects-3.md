# REST API endpoints for Projects and more

# REST API endpoints for Projects

> Use the REST API to manage Projects

## List projects for organization

List all projects owned by a specific organization accessible by the authenticated user.

### Fine-grained access tokens for "List projects for organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Projects" organization permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "List projects for organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| qstringLimit results to projects of the specified type. |
| beforestringA cursor, as given in theLink header. If specified, the query only searches for results before this cursor. For more information, see "Using pagination in the REST API." |
| afterstringA cursor, as given in theLink header. If specified, the query only searches for results after this cursor. For more information, see "Using pagination in the REST API." |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |

### HTTP response status codes for "List projects for organization"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 304 | Not modified |
| 401 | Requires authentication |
| 403 | Forbidden |

### Code samples for "List projects for organization"

#### Request example

get/orgs/{org}/projectsV2

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/projectsV2`

Response

-
-

`Status: 200``{
"id": 2,
"node_id": "MDc6UHJvamVjdDEwMDI2MDM=",
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
"creator": {
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
"title": "My Projects",
"description": "A board to manage my personal projects.",
"public": true,
"closed_at": null,
"created_at": "2011-04-10T20:09:31Z",
"updated_at": "2014-03-03T18:58:10Z",
"number": 2,
"short_description": null,
"deleted_at": null,
"deleted_by": null,
"state": "open",
"latest_status_update": {
"id": 3,
"node_id": "PVTSU_lAECAQM",
"creator": {
"login": "hubot",
"id": 2,
"node_id": "MDQ6VXNlcjI=",
"avatar_url": "https://github.com/images/error/hubot_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/hubot",
"html_url": "https://github.com/hubot",
"followers_url": "https://api.github.com/users/hubot/followers",
"following_url": "https://api.github.com/users/hubot/following{/other_user}",
"gists_url": "https://api.github.com/users/hubot/gists{/gist_id}",
"starred_url": "https://api.github.com/users/hubot/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/hubot/subscriptions",
"organizations_url": "https://api.github.com/users/hubot/orgs",
"repos_url": "https://api.github.com/users/hubot/repos",
"events_url": "https://api.github.com/users/hubot/events{/privacy}",
"received_events_url": "https://api.github.com/users/hubot/received_events",
"type": "User",
"site_admin": false
},
"body": "DONE",
"start_date": "2025-07-23",
"target_date": "2025-07-26",
"status": "COMPLETE",
"created_at": "2025-07-11T16:19:28Z",
"updated_at": "2025-07-11T16:19:28Z"
},
"is_template": true
}`

## Get project for organization

Get a specific organization-owned project.

### Fine-grained access tokens for "Get project for organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Projects" organization permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "Get project for organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| project_numberintegerRequiredThe project's number. |
| orgstringRequiredThe organization name. The name is not case sensitive. |

### HTTP response status codes for "Get project for organization"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 304 | Not modified |
| 401 | Requires authentication |
| 403 | Forbidden |

### Code samples for "Get project for organization"

#### Request example

get/orgs/{org}/projectsV2/{project_number}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/projectsV2/PROJECT_NUMBER`

Response

-
-

`Status: 200``{
"id": 2,
"node_id": "MDc6UHJvamVjdDEwMDI2MDM=",
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
"creator": {
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
"title": "My Projects",
"description": "A board to manage my personal projects.",
"public": true,
"closed_at": null,
"created_at": "2011-04-10T20:09:31Z",
"updated_at": "2014-03-03T18:58:10Z",
"number": 2,
"short_description": null,
"deleted_at": null,
"deleted_by": null,
"state": "open",
"latest_status_update": {
"id": 3,
"node_id": "PVTSU_lAECAQM",
"creator": {
"login": "hubot",
"id": 2,
"node_id": "MDQ6VXNlcjI=",
"avatar_url": "https://github.com/images/error/hubot_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/hubot",
"html_url": "https://github.com/hubot",
"followers_url": "https://api.github.com/users/hubot/followers",
"following_url": "https://api.github.com/users/hubot/following{/other_user}",
"gists_url": "https://api.github.com/users/hubot/gists{/gist_id}",
"starred_url": "https://api.github.com/users/hubot/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/hubot/subscriptions",
"organizations_url": "https://api.github.com/users/hubot/orgs",
"repos_url": "https://api.github.com/users/hubot/repos",
"events_url": "https://api.github.com/users/hubot/events{/privacy}",
"received_events_url": "https://api.github.com/users/hubot/received_events",
"type": "User",
"site_admin": false
},
"body": "DONE",
"start_date": "2025-07-23",
"target_date": "2025-07-26",
"status": "COMPLETE",
"created_at": "2025-07-11T16:19:28Z",
"updated_at": "2025-07-11T16:19:28Z"
},
"is_template": true
}`

## List projects for user

List all projects owned by a specific user accessible by the authenticated user.

### Fine-grained access tokens for "List projects for user"

This endpoint does not work with GitHub App user access tokens, GitHub App installation access tokens, or fine-grained personal access tokens.

### Parameters for "List projects for user"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| usernamestringRequiredThe handle for the GitHub user account. |

| Name, Type, Description |
| --- |
| qstringLimit results to projects of the specified type. |
| beforestringA cursor, as given in theLink header. If specified, the query only searches for results before this cursor. For more information, see "Using pagination in the REST API." |
| afterstringA cursor, as given in theLink header. If specified, the query only searches for results after this cursor. For more information, see "Using pagination in the REST API." |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |

### HTTP response status codes for "List projects for user"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 304 | Not modified |
| 401 | Requires authentication |
| 403 | Forbidden |

### Code samples for "List projects for user"

#### Request example

get/users/{username}/projectsV2

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/users/USERNAME/projectsV2`

Response

-
-

`Status: 200``{
"id": 2,
"node_id": "MDc6UHJvamVjdDEwMDI2MDM=",
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
"creator": {
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
"title": "My Projects",
"description": "A board to manage my personal projects.",
"public": true,
"closed_at": null,
"created_at": "2011-04-10T20:09:31Z",
"updated_at": "2014-03-03T18:58:10Z",
"number": 2,
"short_description": null,
"deleted_at": null,
"deleted_by": null,
"state": "open",
"latest_status_update": {
"id": 3,
"node_id": "PVTSU_lAECAQM",
"creator": {
"login": "hubot",
"id": 2,
"node_id": "MDQ6VXNlcjI=",
"avatar_url": "https://github.com/images/error/hubot_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/hubot",
"html_url": "https://github.com/hubot",
"followers_url": "https://api.github.com/users/hubot/followers",
"following_url": "https://api.github.com/users/hubot/following{/other_user}",
"gists_url": "https://api.github.com/users/hubot/gists{/gist_id}",
"starred_url": "https://api.github.com/users/hubot/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/hubot/subscriptions",
"organizations_url": "https://api.github.com/users/hubot/orgs",
"repos_url": "https://api.github.com/users/hubot/repos",
"events_url": "https://api.github.com/users/hubot/events{/privacy}",
"received_events_url": "https://api.github.com/users/hubot/received_events",
"type": "User",
"site_admin": false
},
"body": "DONE",
"start_date": "2025-07-23",
"target_date": "2025-07-26",
"status": "COMPLETE",
"created_at": "2025-07-11T16:19:28Z",
"updated_at": "2025-07-11T16:19:28Z"
},
"is_template": true
}`

## Get project for user

Get a specific user-owned project.

### Fine-grained access tokens for "Get project for user"

This endpoint does not work with GitHub App user access tokens, GitHub App installation access tokens, or fine-grained personal access tokens.

### Parameters for "Get project for user"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| project_numberintegerRequiredThe project's number. |
| usernamestringRequiredThe handle for the GitHub user account. |

### HTTP response status codes for "Get project for user"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 304 | Not modified |
| 401 | Requires authentication |
| 403 | Forbidden |

### Code samples for "Get project for user"

#### Request example

get/users/{username}/projectsV2/{project_number}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/users/USERNAME/projectsV2/PROJECT_NUMBER`

Response

-
-

`Status: 200``{
"id": 2,
"node_id": "MDc6UHJvamVjdDEwMDI2MDM=",
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
"creator": {
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
"title": "My Projects",
"description": "A board to manage my personal projects.",
"public": true,
"closed_at": null,
"created_at": "2011-04-10T20:09:31Z",
"updated_at": "2014-03-03T18:58:10Z",
"number": 2,
"short_description": null,
"deleted_at": null,
"deleted_by": null,
"state": "open",
"latest_status_update": {
"id": 3,
"node_id": "PVTSU_lAECAQM",
"creator": {
"login": "hubot",
"id": 2,
"node_id": "MDQ6VXNlcjI=",
"avatar_url": "https://github.com/images/error/hubot_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/hubot",
"html_url": "https://github.com/hubot",
"followers_url": "https://api.github.com/users/hubot/followers",
"following_url": "https://api.github.com/users/hubot/following{/other_user}",
"gists_url": "https://api.github.com/users/hubot/gists{/gist_id}",
"starred_url": "https://api.github.com/users/hubot/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/hubot/subscriptions",
"organizations_url": "https://api.github.com/users/hubot/orgs",
"repos_url": "https://api.github.com/users/hubot/repos",
"events_url": "https://api.github.com/users/hubot/events{/privacy}",
"received_events_url": "https://api.github.com/users/hubot/received_events",
"type": "User",
"site_admin": false
},
"body": "DONE",
"start_date": "2025-07-23",
"target_date": "2025-07-26",
"status": "COMPLETE",
"created_at": "2025-07-11T16:19:28Z",
"updated_at": "2025-07-11T16:19:28Z"
},
"is_template": true
}`

---

# REST API endpoints for Project views

> Use the REST API to manage Project views

## Create a view for an organization-owned project

Create a new view in an organization-owned project. Views allow you to customize how items in a project are displayed and filtered.

### Fine-grained access tokens for "Create a view for an organization-owned project"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Projects" organization permissions (write)

### Parameters for "Create a view for an organization-owned project"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| project_numberintegerRequiredThe project's number. |

| Name, Type, Description |
| --- |
| namestringRequiredThe name of the view. |
| layoutstringRequiredThe layout of the view.Can be one of:table,board,roadmap |
| filterstringThe filter query for the view. SeeFiltering projectsfor more information. |
| visible_fieldsarray of integersvisible_fieldsis not applicable toroadmaplayout views.
Fortableandboardlayouts, this represents the field IDs that should be visible in the view. If not provided, the default visible fields will be used. |

### HTTP response status codes for "Create a view for an organization-owned project"

| Status code | Description |
| --- | --- |
| 201 | Response for creating a view in an organization-owned project. |
| 304 | Not modified |
| 401 | Requires authentication |
| 403 | Forbidden |
| 404 | Resource not found |
| 422 | Validation failed, or the endpoint has been spammed. |
| 503 | Service unavailable |

### Code samples for "Create a view for an organization-owned project"

#### Request examples

Select the example typeCreate a table viewCreate a board view with filterCreate a roadmap viewpost/orgs/{org}/projectsV2/{project_number}/views

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/projectsV2/PROJECT_NUMBER/views \
  -d '{"name":"All Issues","layout":"table","filter":"is:issue","visible_fields":[123,456,789]}'`

Response for creating a table view

-
-

`Status: 201``{
"value": {
"id": 1,
"number": 1,
"name": "Sprint Board",
"layout": "board",
"node_id": "PVTV_lADOANN5s84ACbL0zgBueEI",
"project_url": "https://api.github.com/orgs/octocat/projectsV2/1",
"html_url": "https://github.com/orgs/octocat/projects/1/views/1",
"creator": {
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
"created_at": "2022-04-28T12:00:00Z",
"updated_at": "2022-04-28T12:00:00Z",
"filter": "is:issue is:open",
"visible_fields": [
123,
456,
789
],
"sort_by": [
[
123,
"asc"
],
[
456,
"desc"
]
],
"group_by": [
123
],
"vertical_group_by": [
456
]
}
}`

## Create a view for a user-owned project

Create a new view in a user-owned project. Views allow you to customize how items in a project are displayed and filtered.

### Fine-grained access tokens for "Create a view for a user-owned project"

This endpoint does not work with GitHub App user access tokens, GitHub App installation access tokens, or fine-grained personal access tokens.

### Parameters for "Create a view for a user-owned project"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| user_idstringRequiredThe unique identifier of the user. |
| project_numberintegerRequiredThe project's number. |

| Name, Type, Description |
| --- |
| namestringRequiredThe name of the view. |
| layoutstringRequiredThe layout of the view.Can be one of:table,board,roadmap |
| filterstringThe filter query for the view. SeeFiltering projectsfor more information. |
| visible_fieldsarray of integersvisible_fieldsis not applicable toroadmaplayout views.
Fortableandboardlayouts, this represents the field IDs that should be visible in the view. If not provided, the default visible fields will be used. |

### HTTP response status codes for "Create a view for a user-owned project"

| Status code | Description |
| --- | --- |
| 201 | Response for creating a view in a user-owned project. |
| 304 | Not modified |
| 401 | Requires authentication |
| 403 | Forbidden |
| 404 | Resource not found |
| 422 | Validation failed, or the endpoint has been spammed. |
| 503 | Service unavailable |

### Code samples for "Create a view for a user-owned project"

#### Request examples

Select the example typeCreate a table viewCreate a board view with filterCreate a roadmap viewpost/users/{user_id}/projectsV2/{project_number}/views

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/users/USER_ID/projectsV2/PROJECT_NUMBER/views \
  -d '{"name":"All Issues","layout":"table","filter":"is:issue","visible_fields":[123,456,789]}'`

Response for creating a table view

-
-

`Status: 201``{
"value": {
"id": 1,
"number": 1,
"name": "Sprint Board",
"layout": "board",
"node_id": "PVTV_lADOANN5s84ACbL0zgBueEI",
"project_url": "https://api.github.com/orgs/octocat/projectsV2/1",
"html_url": "https://github.com/orgs/octocat/projects/1/views/1",
"creator": {
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
"created_at": "2022-04-28T12:00:00Z",
"updated_at": "2022-04-28T12:00:00Z",
"filter": "is:issue is:open",
"visible_fields": [
123,
456,
789
],
"sort_by": [
[
123,
"asc"
],
[
456,
"desc"
]
],
"group_by": [
123
],
"vertical_group_by": [
456
]
}
}`
