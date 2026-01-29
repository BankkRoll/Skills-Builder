# REST API endpoints for labels and more

# REST API endpoints for labels

> Use the REST API to manage labels for repositories, issues and pull requests.

## About labels

You can use the REST API to manage labels for a repository and add or remove labels to issues and pull requests. Every pull request is an issue, but not every issue is a pull request. For this reason, "shared" actions for both features, like managing assignees, labels, and milestones, are provided within the Issues endpoints.

---

# REST API endpoints for milestones

> Use the REST API to manage milestones.

## List milestones

Lists milestones for a repository.

### Fine-grained access tokens for "List milestones"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have at least one of the following permission sets:

- "Issues" repository permissions (read)
- "Pull requests" repository permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "List milestones"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| statestringThe state of the milestone. Eitheropen,closed, orall.Default:openCan be one of:open,closed,all |
| sortstringWhat to sort results by. Eitherdue_onorcompleteness.Default:due_onCan be one of:due_on,completeness |
| directionstringThe direction of the sort. Eitherascordesc.Default:ascCan be one of:asc,desc |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| pageintegerThe page number of the results to fetch. For more information, see "Using pagination in the REST API."Default:1 |

### HTTP response status codes for "List milestones"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |

### Code samples for "List milestones"

#### Request example

get/repos/{owner}/{repo}/milestones

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/milestones`

Response

-
-

`Status: 200``[
{
"url": "https://api.github.com/repos/octocat/Hello-World/milestones/1",
"html_url": "https://github.com/octocat/Hello-World/milestones/v1.0",
"labels_url": "https://api.github.com/repos/octocat/Hello-World/milestones/1/labels",
"id": 1002604,
"node_id": "MDk6TWlsZXN0b25lMTAwMjYwNA==",
"number": 1,
"state": "open",
"title": "v1.0",
"description": "Tracking milestone for version 1.0",
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
"open_issues": 4,
"closed_issues": 8,
"created_at": "2011-04-10T20:09:31Z",
"updated_at": "2014-03-03T18:58:10Z",
"closed_at": "2013-02-12T13:22:01Z",
"due_on": "2012-10-09T23:39:01Z"
}
]`

## Create a milestone

Creates a milestone.

### Fine-grained access tokens for "Create a milestone"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have at least one of the following permission sets:

- "Issues" repository permissions (write)
- "Pull requests" repository permissions (write)

### Parameters for "Create a milestone"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| titlestringRequiredThe title of the milestone. |
| statestringThe state of the milestone. Eitheropenorclosed.Default:openCan be one of:open,closed |
| descriptionstringA description of the milestone. |
| due_onstringThe milestone due date. This is a timestamp inISO 8601format:YYYY-MM-DDTHH:MM:SSZ. |

### HTTP response status codes for "Create a milestone"

| Status code | Description |
| --- | --- |
| 201 | Created |
| 404 | Resource not found |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Create a milestone"

#### Request example

post/repos/{owner}/{repo}/milestones

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/milestones \
  -d '{"title":"v1.0","state":"open","description":"Tracking milestone for version 1.0","due_on":"2012-10-09T23:39:01Z"}'`

Response

-
-

`Status: 201``{
"url": "https://api.github.com/repos/octocat/Hello-World/milestones/1",
"html_url": "https://github.com/octocat/Hello-World/milestones/v1.0",
"labels_url": "https://api.github.com/repos/octocat/Hello-World/milestones/1/labels",
"id": 1002604,
"node_id": "MDk6TWlsZXN0b25lMTAwMjYwNA==",
"number": 1,
"state": "open",
"title": "v1.0",
"description": "Tracking milestone for version 1.0",
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
"open_issues": 4,
"closed_issues": 8,
"created_at": "2011-04-10T20:09:31Z",
"updated_at": "2014-03-03T18:58:10Z",
"closed_at": "2013-02-12T13:22:01Z",
"due_on": "2012-10-09T23:39:01Z"
}`

## Get a milestone

Gets a milestone using the given milestone number.

### Fine-grained access tokens for "Get a milestone"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have at least one of the following permission sets:

- "Issues" repository permissions (read)
- "Pull requests" repository permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "Get a milestone"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| milestone_numberintegerRequiredThe number that identifies the milestone. |

### HTTP response status codes for "Get a milestone"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |

### Code samples for "Get a milestone"

#### Request example

get/repos/{owner}/{repo}/milestones/{milestone_number}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/milestones/MILESTONE_NUMBER`

Response

-
-

`Status: 200``{
"url": "https://api.github.com/repos/octocat/Hello-World/milestones/1",
"html_url": "https://github.com/octocat/Hello-World/milestones/v1.0",
"labels_url": "https://api.github.com/repos/octocat/Hello-World/milestones/1/labels",
"id": 1002604,
"node_id": "MDk6TWlsZXN0b25lMTAwMjYwNA==",
"number": 1,
"state": "open",
"title": "v1.0",
"description": "Tracking milestone for version 1.0",
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
"open_issues": 4,
"closed_issues": 8,
"created_at": "2011-04-10T20:09:31Z",
"updated_at": "2014-03-03T18:58:10Z",
"closed_at": "2013-02-12T13:22:01Z",
"due_on": "2012-10-09T23:39:01Z"
}`

## Update a milestone

### Fine-grained access tokens for "Update a milestone"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have at least one of the following permission sets:

- "Issues" repository permissions (write)
- "Pull requests" repository permissions (write)

### Parameters for "Update a milestone"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| milestone_numberintegerRequiredThe number that identifies the milestone. |

| Name, Type, Description |
| --- |
| titlestringThe title of the milestone. |
| statestringThe state of the milestone. Eitheropenorclosed.Default:openCan be one of:open,closed |
| descriptionstringA description of the milestone. |
| due_onstringThe milestone due date. This is a timestamp inISO 8601format:YYYY-MM-DDTHH:MM:SSZ. |

### HTTP response status codes for "Update a milestone"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "Update a milestone"

#### Request example

patch/repos/{owner}/{repo}/milestones/{milestone_number}

-
-
-

`curl -L \
  -X PATCH \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/milestones/MILESTONE_NUMBER \
  -d '{"title":"v1.0","state":"open","description":"Tracking milestone for version 1.0","due_on":"2012-10-09T23:39:01Z"}'`

Response

-
-

`Status: 200``{
"url": "https://api.github.com/repos/octocat/Hello-World/milestones/1",
"html_url": "https://github.com/octocat/Hello-World/milestones/v1.0",
"labels_url": "https://api.github.com/repos/octocat/Hello-World/milestones/1/labels",
"id": 1002604,
"node_id": "MDk6TWlsZXN0b25lMTAwMjYwNA==",
"number": 1,
"state": "open",
"title": "v1.0",
"description": "Tracking milestone for version 1.0",
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
"open_issues": 4,
"closed_issues": 8,
"created_at": "2011-04-10T20:09:31Z",
"updated_at": "2014-03-03T18:58:10Z",
"closed_at": "2013-02-12T13:22:01Z",
"due_on": "2012-10-09T23:39:01Z"
}`

## Delete a milestone

Deletes a milestone using the given milestone number.

### Fine-grained access tokens for "Delete a milestone"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have at least one of the following permission sets:

- "Issues" repository permissions (write)
- "Pull requests" repository permissions (write)

### Parameters for "Delete a milestone"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| milestone_numberintegerRequiredThe number that identifies the milestone. |

### HTTP response status codes for "Delete a milestone"

| Status code | Description |
| --- | --- |
| 204 | No Content |
| 404 | Resource not found |

### Code samples for "Delete a milestone"

#### Request example

delete/repos/{owner}/{repo}/milestones/{milestone_number}

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/milestones/MILESTONE_NUMBER`

Response

`Status: 204`

---

# REST API endpoints for sub

> Use the REST API to view, add, remove, and reprioritize sub-issues.

## Get parent issue

You can use the REST API to get the parent issue of a sub-issue.

This endpoint supports the following custom media types. For more information, see [Media types](https://docs.github.com/rest/using-the-rest-api/getting-started-with-the-rest-api#media-types).

- **application/vnd.github.raw+json**: Returns the raw markdown body. Response will include `body`. This is the default if you do not pass any specific media type.
- **application/vnd.github.text+json**: Returns a text only representation of the markdown body. Response will include `body_text`.
- **application/vnd.github.html+json**: Returns HTML rendered from the body's markdown. Response will include `body_html`.
- **application/vnd.github.full+json**: Returns raw, text, and HTML representations. Response will include `body`, `body_text`, and `body_html`.

### Fine-grained access tokens for "Get parent issue"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Issues" repository permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "Get parent issue"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| issue_numberintegerRequiredThe number that identifies the issue. |

### HTTP response status codes for "Get parent issue"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 301 | Moved permanently |
| 404 | Resource not found |
| 410 | Gone |

### Code samples for "Get parent issue"

#### Request example

get/repos/{owner}/{repo}/issues/{issue_number}/parent

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/issues/ISSUE_NUMBER/parent`

Response

-
-

`Status: 200``{
"id": 1,
"node_id": "MDU6SXNzdWUx",
"url": "https://api.github.com/repos/octocat/Hello-World/issues/1347",
"repository_url": "https://api.github.com/repos/octocat/Hello-World",
"labels_url": "https://api.github.com/repos/octocat/Hello-World/issues/1347/labels{/name}",
"comments_url": "https://api.github.com/repos/octocat/Hello-World/issues/1347/comments",
"events_url": "https://api.github.com/repos/octocat/Hello-World/issues/1347/events",
"html_url": "https://github.com/octocat/Hello-World/issues/1347",
"number": 1347,
"state": "open",
"title": "Found a bug",
"body": "I'm having a problem with this.",
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
},
"labels": [
{
"id": 208045946,
"node_id": "MDU6TGFiZWwyMDgwNDU5NDY=",
"url": "https://api.github.com/repos/octocat/Hello-World/labels/bug",
"name": "bug",
"description": "Something isn't working",
"color": "f29513",
"default": true
}
],
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
"assignees": [
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
],
"milestone": {
"url": "https://api.github.com/repos/octocat/Hello-World/milestones/1",
"html_url": "https://github.com/octocat/Hello-World/milestones/v1.0",
"labels_url": "https://api.github.com/repos/octocat/Hello-World/milestones/1/labels",
"id": 1002604,
"node_id": "MDk6TWlsZXN0b25lMTAwMjYwNA==",
"number": 1,
"state": "open",
"title": "v1.0",
"description": "Tracking milestone for version 1.0",
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
"open_issues": 4,
"closed_issues": 8,
"created_at": "2011-04-10T20:09:31Z",
"updated_at": "2014-03-03T18:58:10Z",
"closed_at": "2013-02-12T13:22:01Z",
"due_on": "2012-10-09T23:39:01Z"
},
"locked": true,
"active_lock_reason": "too heated",
"comments": 0,
"pull_request": {
"url": "https://api.github.com/repos/octocat/Hello-World/pulls/1347",
"html_url": "https://github.com/octocat/Hello-World/pull/1347",
"diff_url": "https://github.com/octocat/Hello-World/pull/1347.diff",
"patch_url": "https://github.com/octocat/Hello-World/pull/1347.patch"
},
"closed_at": null,
"created_at": "2011-04-22T13:33:48Z",
"updated_at": "2011-04-22T13:33:48Z",
"closed_by": {
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
"author_association": "COLLABORATOR",
"state_reason": "completed"
}`

## Remove sub-issue

You can use the REST API to remove a sub-issue from an issue.
Removing content too quickly using this endpoint may result in secondary rate limiting.
For more information, see "[Rate limits for the API](https://docs.github.com/rest/using-the-rest-api/rate-limits-for-the-rest-api#about-secondary-rate-limits)"
and "[Best practices for using the REST API](https://docs.github.com/rest/guides/best-practices-for-using-the-rest-api)."
This endpoint supports the following custom media types. For more information, see "[Media types](https://docs.github.com/rest/using-the-rest-api/getting-started-with-the-rest-api#media-types)."

- **application/vnd.github.raw+json**: Returns the raw markdown body. Response will include `body`. This is the default if you do not pass a specific media type.
- **application/vnd.github.text+json**: Returns a text only representation of the markdown body. Response will include `body_text`.
- **application/vnd.github.html+json**: Returns HTML rendered from the body's markdown. Response will include `body_html`.
- **application/vnd.github.full+json**: Returns raw, text, and HTML representations. Response will include `body`, `body_text`, and `body_html`.

### Fine-grained access tokens for "Remove sub-issue"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Issues" repository permissions (write)

### Parameters for "Remove sub-issue"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| issue_numberintegerRequiredThe number that identifies the issue. |

| Name, Type, Description |
| --- |
| sub_issue_idintegerRequiredThe id of the sub-issue to remove |

### HTTP response status codes for "Remove sub-issue"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 400 | Bad Request |
| 404 | Resource not found |

### Code samples for "Remove sub-issue"

#### Request example

delete/repos/{owner}/{repo}/issues/{issue_number}/sub_issue

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/issues/ISSUE_NUMBER/sub_issue \
  -d '{"sub_issue_id":6}'`

Response

-
-

`Status: 200``{
"id": 1,
"node_id": "MDU6SXNzdWUx",
"url": "https://api.github.com/repos/octocat/Hello-World/issues/1347",
"repository_url": "https://api.github.com/repos/octocat/Hello-World",
"labels_url": "https://api.github.com/repos/octocat/Hello-World/issues/1347/labels{/name}",
"comments_url": "https://api.github.com/repos/octocat/Hello-World/issues/1347/comments",
"events_url": "https://api.github.com/repos/octocat/Hello-World/issues/1347/events",
"html_url": "https://github.com/octocat/Hello-World/issues/1347",
"number": 1347,
"state": "open",
"title": "Found a bug",
"body": "I'm having a problem with this.",
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
},
"labels": [
{
"id": 208045946,
"node_id": "MDU6TGFiZWwyMDgwNDU5NDY=",
"url": "https://api.github.com/repos/octocat/Hello-World/labels/bug",
"name": "bug",
"description": "Something isn't working",
"color": "f29513",
"default": true
}
],
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
"assignees": [
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
],
"milestone": {
"url": "https://api.github.com/repos/octocat/Hello-World/milestones/1",
"html_url": "https://github.com/octocat/Hello-World/milestones/v1.0",
"labels_url": "https://api.github.com/repos/octocat/Hello-World/milestones/1/labels",
"id": 1002604,
"node_id": "MDk6TWlsZXN0b25lMTAwMjYwNA==",
"number": 1,
"state": "open",
"title": "v1.0",
"description": "Tracking milestone for version 1.0",
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
"open_issues": 4,
"closed_issues": 8,
"created_at": "2011-04-10T20:09:31Z",
"updated_at": "2014-03-03T18:58:10Z",
"closed_at": "2013-02-12T13:22:01Z",
"due_on": "2012-10-09T23:39:01Z"
},
"locked": true,
"active_lock_reason": "too heated",
"comments": 0,
"pull_request": {
"url": "https://api.github.com/repos/octocat/Hello-World/pulls/1347",
"html_url": "https://github.com/octocat/Hello-World/pull/1347",
"diff_url": "https://github.com/octocat/Hello-World/pull/1347.diff",
"patch_url": "https://github.com/octocat/Hello-World/pull/1347.patch"
},
"closed_at": null,
"created_at": "2011-04-22T13:33:48Z",
"updated_at": "2011-04-22T13:33:48Z",
"closed_by": {
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
"author_association": "COLLABORATOR",
"state_reason": "completed"
}`

## List sub-issues

You can use the REST API to list the sub-issues on an issue.

This endpoint supports the following custom media types. For more information, see [Media types](https://docs.github.com/rest/using-the-rest-api/getting-started-with-the-rest-api#media-types).

- **application/vnd.github.raw+json**: Returns the raw Markdown body. Response will include `body`. This is the default if you do not pass any specific media type.
- **application/vnd.github.text+json**: Returns a text only representation of the Markdown body. Response will include `body_text`.
- **application/vnd.github.html+json**: Returns HTML rendered from the body's Markdown. Response will include `body_html`.
- **application/vnd.github.full+json**: Returns raw, text, and HTML representations. Response will include `body`, `body_text`, and `body_html`.

### Fine-grained access tokens for "List sub-issues"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Issues" repository permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "List sub-issues"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| issue_numberintegerRequiredThe number that identifies the issue. |

| Name, Type, Description |
| --- |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| pageintegerThe page number of the results to fetch. For more information, see "Using pagination in the REST API."Default:1 |

### HTTP response status codes for "List sub-issues"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |
| 410 | Gone |

### Code samples for "List sub-issues"

#### Request example

get/repos/{owner}/{repo}/issues/{issue_number}/sub_issues

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/issues/ISSUE_NUMBER/sub_issues`

Response

-
-

`Status: 200``[
{
"id": 1,
"node_id": "MDU6SXNzdWUx",
"url": "https://api.github.com/repos/octocat/Hello-World/issues/1347",
"repository_url": "https://api.github.com/repos/octocat/Hello-World",
"labels_url": "https://api.github.com/repos/octocat/Hello-World/issues/1347/labels{/name}",
"comments_url": "https://api.github.com/repos/octocat/Hello-World/issues/1347/comments",
"events_url": "https://api.github.com/repos/octocat/Hello-World/issues/1347/events",
"html_url": "https://github.com/octocat/Hello-World/issues/1347",
"number": 1347,
"state": "open",
"title": "Found a bug",
"body": "I'm having a problem with this.",
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
},
"labels": [
{
"id": 208045946,
"node_id": "MDU6TGFiZWwyMDgwNDU5NDY=",
"url": "https://api.github.com/repos/octocat/Hello-World/labels/bug",
"name": "bug",
"description": "Something isn't working",
"color": "f29513",
"default": true
}
],
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
"assignees": [
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
],
"milestone": {
"url": "https://api.github.com/repos/octocat/Hello-World/milestones/1",
"html_url": "https://github.com/octocat/Hello-World/milestones/v1.0",
"labels_url": "https://api.github.com/repos/octocat/Hello-World/milestones/1/labels",
"id": 1002604,
"node_id": "MDk6TWlsZXN0b25lMTAwMjYwNA==",
"number": 1,
"state": "open",
"title": "v1.0",
"description": "Tracking milestone for version 1.0",
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
"open_issues": 4,
"closed_issues": 8,
"created_at": "2011-04-10T20:09:31Z",
"updated_at": "2014-03-03T18:58:10Z",
"closed_at": "2013-02-12T13:22:01Z",
"due_on": "2012-10-09T23:39:01Z"
},
"locked": true,
"active_lock_reason": "too heated",
"comments": 0,
"pull_request": {
"url": "https://api.github.com/repos/octocat/Hello-World/pulls/1347",
"html_url": "https://github.com/octocat/Hello-World/pull/1347",
"diff_url": "https://github.com/octocat/Hello-World/pull/1347.diff",
"patch_url": "https://github.com/octocat/Hello-World/pull/1347.patch"
},
"closed_at": null,
"created_at": "2011-04-22T13:33:48Z",
"updated_at": "2011-04-22T13:33:48Z",
"closed_by": {
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
"author_association": "COLLABORATOR",
"state_reason": "completed"
}
]`

## Add sub-issue

You can use the REST API to add sub-issues to issues.

Creating content too quickly using this endpoint may result in secondary rate limiting.
For more information, see "[Rate limits for the API](https://docs.github.com/rest/using-the-rest-api/rate-limits-for-the-rest-api#about-secondary-rate-limits)"
and "[Best practices for using the REST API](https://docs.github.com/rest/guides/best-practices-for-using-the-rest-api)."

This endpoint supports the following custom media types. For more information, see "[Media types](https://docs.github.com/rest/using-the-rest-api/getting-started-with-the-rest-api#media-types)."

- **application/vnd.github.raw+json**: Returns the raw markdown body. Response will include `body`. This is the default if you do not pass any specific media type.
- **application/vnd.github.text+json**: Returns a text only representation of the markdown body. Response will include `body_text`.
- **application/vnd.github.html+json**: Returns HTML rendered from the body's markdown. Response will include `body_html`.
- **application/vnd.github.full+json**: Returns raw, text, and HTML representations. Response will include `body`, `body_text`, and `body_html`.

### Fine-grained access tokens for "Add sub-issue"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Issues" repository permissions (write)

### Parameters for "Add sub-issue"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| issue_numberintegerRequiredThe number that identifies the issue. |

| Name, Type, Description |
| --- |
| sub_issue_idintegerRequiredThe id of the sub-issue to add. The sub-issue must belong to the same repository owner as the parent issue |
| replace_parentbooleanOption that, when true, instructs the operation to replace the sub-issues current parent issue |

### HTTP response status codes for "Add sub-issue"

| Status code | Description |
| --- | --- |
| 201 | Created |
| 403 | Forbidden |
| 404 | Resource not found |
| 410 | Gone |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Add sub-issue"

#### Request example

post/repos/{owner}/{repo}/issues/{issue_number}/sub_issues

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/issues/ISSUE_NUMBER/sub_issues \
  -d '{"sub_issue_id":1}'`

Response

-
-

`Status: 201``{
"id": 1,
"node_id": "MDU6SXNzdWUx",
"url": "https://api.github.com/repos/octocat/Hello-World/issues/1347",
"repository_url": "https://api.github.com/repos/octocat/Hello-World",
"labels_url": "https://api.github.com/repos/octocat/Hello-World/issues/1347/labels{/name}",
"comments_url": "https://api.github.com/repos/octocat/Hello-World/issues/1347/comments",
"events_url": "https://api.github.com/repos/octocat/Hello-World/issues/1347/events",
"html_url": "https://github.com/octocat/Hello-World/issues/1347",
"number": 1347,
"state": "open",
"title": "Found a bug",
"body": "I'm having a problem with this.",
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
},
"labels": [
{
"id": 208045946,
"node_id": "MDU6TGFiZWwyMDgwNDU5NDY=",
"url": "https://api.github.com/repos/octocat/Hello-World/labels/bug",
"name": "bug",
"description": "Something isn't working",
"color": "f29513",
"default": true
}
],
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
"assignees": [
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
],
"milestone": {
"url": "https://api.github.com/repos/octocat/Hello-World/milestones/1",
"html_url": "https://github.com/octocat/Hello-World/milestones/v1.0",
"labels_url": "https://api.github.com/repos/octocat/Hello-World/milestones/1/labels",
"id": 1002604,
"node_id": "MDk6TWlsZXN0b25lMTAwMjYwNA==",
"number": 1,
"state": "open",
"title": "v1.0",
"description": "Tracking milestone for version 1.0",
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
"open_issues": 4,
"closed_issues": 8,
"created_at": "2011-04-10T20:09:31Z",
"updated_at": "2014-03-03T18:58:10Z",
"closed_at": "2013-02-12T13:22:01Z",
"due_on": "2012-10-09T23:39:01Z"
},
"locked": true,
"active_lock_reason": "too heated",
"comments": 0,
"pull_request": {
"url": "https://api.github.com/repos/octocat/Hello-World/pulls/1347",
"html_url": "https://github.com/octocat/Hello-World/pull/1347",
"diff_url": "https://github.com/octocat/Hello-World/pull/1347.diff",
"patch_url": "https://github.com/octocat/Hello-World/pull/1347.patch"
},
"closed_at": null,
"created_at": "2011-04-22T13:33:48Z",
"updated_at": "2011-04-22T13:33:48Z",
"closed_by": {
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
"author_association": "COLLABORATOR",
"state_reason": "completed"
}`

## Reprioritize sub-issue

You can use the REST API to reprioritize a sub-issue to a different position in the parent list.

### Fine-grained access tokens for "Reprioritize sub-issue"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Issues" repository permissions (write)

### Parameters for "Reprioritize sub-issue"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| issue_numberintegerRequiredThe number that identifies the issue. |

| Name, Type, Description |
| --- |
| sub_issue_idintegerRequiredThe id of the sub-issue to reprioritize |
| after_idintegerThe id of the sub-issue to be prioritized after (either positional argument after OR before should be specified). |
| before_idintegerThe id of the sub-issue to be prioritized before (either positional argument after OR before should be specified). |

### HTTP response status codes for "Reprioritize sub-issue"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 403 | Forbidden |
| 404 | Resource not found |
| 422 | Validation failed, or the endpoint has been spammed. |
| 503 | Service unavailable |

### Code samples for "Reprioritize sub-issue"

#### Request example

patch/repos/{owner}/{repo}/issues/{issue_number}/sub_issues/priority

-
-
-

`curl -L \
  -X PATCH \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/issues/ISSUE_NUMBER/sub_issues/priority \
  -d '{"sub_issue_id":6,"after_id":5}'`

Response

-
-

`Status: 200``{
"id": 1,
"node_id": "MDU6SXNzdWUx",
"url": "https://api.github.com/repos/octocat/Hello-World/issues/1347",
"repository_url": "https://api.github.com/repos/octocat/Hello-World",
"labels_url": "https://api.github.com/repos/octocat/Hello-World/issues/1347/labels{/name}",
"comments_url": "https://api.github.com/repos/octocat/Hello-World/issues/1347/comments",
"events_url": "https://api.github.com/repos/octocat/Hello-World/issues/1347/events",
"html_url": "https://github.com/octocat/Hello-World/issues/1347",
"number": 1347,
"state": "open",
"title": "Found a bug",
"body": "I'm having a problem with this.",
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
},
"labels": [
{
"id": 208045946,
"node_id": "MDU6TGFiZWwyMDgwNDU5NDY=",
"url": "https://api.github.com/repos/octocat/Hello-World/labels/bug",
"name": "bug",
"description": "Something isn't working",
"color": "f29513",
"default": true
}
],
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
"assignees": [
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
],
"milestone": {
"url": "https://api.github.com/repos/octocat/Hello-World/milestones/1",
"html_url": "https://github.com/octocat/Hello-World/milestones/v1.0",
"labels_url": "https://api.github.com/repos/octocat/Hello-World/milestones/1/labels",
"id": 1002604,
"node_id": "MDk6TWlsZXN0b25lMTAwMjYwNA==",
"number": 1,
"state": "open",
"title": "v1.0",
"description": "Tracking milestone for version 1.0",
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
"open_issues": 4,
"closed_issues": 8,
"created_at": "2011-04-10T20:09:31Z",
"updated_at": "2014-03-03T18:58:10Z",
"closed_at": "2013-02-12T13:22:01Z",
"due_on": "2012-10-09T23:39:01Z"
},
"locked": true,
"active_lock_reason": "too heated",
"comments": 0,
"pull_request": {
"url": "https://api.github.com/repos/octocat/Hello-World/pulls/1347",
"html_url": "https://github.com/octocat/Hello-World/pull/1347",
"diff_url": "https://github.com/octocat/Hello-World/pull/1347.diff",
"patch_url": "https://github.com/octocat/Hello-World/pull/1347.patch"
},
"closed_at": null,
"created_at": "2011-04-22T13:33:48Z",
"updated_at": "2011-04-22T13:33:48Z",
"closed_by": {
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
"author_association": "COLLABORATOR",
"state_reason": "completed"
}`

---

# REST API endpoints for timeline events

> Use the REST API to receive events triggered by timeline activity in issues and pull requests.

## About timeline events

You can use the REST API to view different types of events triggered by timeline activity in issues and pull requests. For more information about the specific events that you can receive, see [Issue event types](https://docs.github.com/en/webhooks-and-events/events/issue-event-types). To view GitHub activity outside of issues and pull requests, see [GitHub event types](https://docs.github.com/en/webhooks-and-events/events/github-event-types).

You can use timeline events to display information about issues and pull requests or determine who should be notified of issue comments.

Every pull request is an issue, but not every issue is a pull request. For this reason, "shared" actions for both features, like managing assignees, labels, and milestones, are provided within the Issues endpoints.
