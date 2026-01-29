# REST API endpoints for issue assignees and more

# REST API endpoints for issue assignees

> Use the REST API to manage assignees on issues and pull requests.

## About issue and pull request assignees

You can use the REST API to view, add, and remove assignees on issues and pull requests. Every pull request is an issue, but not every issue is a pull request. For this reason, "shared" actions for both features, like managing assignees, labels, and milestones, are provided within the Issues endpoints.

---

# REST API endpoints for issue comments

> Use the REST API to manage comments on issues and pull requests.

## About issue and pull request comments

You can use the REST API to create and manage comments on issues and pull requests. Every pull request is an issue, but not every issue is a pull request. For this reason, "shared" actions for both features, like managing assignees, labels, and milestones, are provided within the Issues endpoints. To manage pull request review comments, see [REST API endpoints for pull request review comments](https://docs.github.com/en/rest/pulls/comments).

---

# REST API endpoints for issue events

> Use the REST API to retrieve events triggered by activity in issues and pull requests.

## About events

You can use the REST API to view different types of events triggered by activity in issues and pull requests. For more information about the specific events that you can receive, see [Issue event types](https://docs.github.com/en/webhooks-and-events/events/issue-event-types). To view GitHub activity outside of issues and pull requests, you can use the [Events](https://docs.github.com/en/webhooks-and-events/events/github-event-types) endpoints.

Every pull request is an issue, but not every issue is a pull request. For this reason, "shared" actions for both features, like managing assignees, labels, and milestones, are provided within the Issues endpoints.

---

# REST API endpoints for issue dependencies

> Use the REST API to view, add, and remove issue dependencies.

## List dependencies an issue is blocked by

You can use the REST API to list the dependencies an issue is blocked by.

This endpoint supports the following custom media types. For more information, see [Media types](https://docs.github.com/rest/using-the-rest-api/getting-started-with-the-rest-api#media-types).

- **application/vnd.github.raw+json**: Returns the raw Markdown body. Response will include `body`. This is the default if you do not pass any specific media type.
- **application/vnd.github.text+json**: Returns a text only representation of the Markdown body. Response will include `body_text`.
- **application/vnd.github.html+json**: Returns HTML rendered from the body's Markdown. Response will include `body_html`.
- **application/vnd.github.full+json**: Returns raw, text, and HTML representations. Response will include `body`, `body_text`, and `body_html`.

### Fine-grained access tokens for "List dependencies an issue is blocked by"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Issues" repository permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "List dependencies an issue is blocked by"

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

### HTTP response status codes for "List dependencies an issue is blocked by"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 301 | Moved permanently |
| 404 | Resource not found |
| 410 | Gone |

### Code samples for "List dependencies an issue is blocked by"

#### Request example

get/repos/{owner}/{repo}/issues/{issue_number}/dependencies/blocked_by

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/issues/ISSUE_NUMBER/dependencies/blocked_by`

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

## Add a dependency an issue is blocked by

You can use the REST API to add a 'blocked by' relationship to an issue.

Creating content too quickly using this endpoint may result in secondary rate limiting.
For more information, see [Rate limits for the API](https://docs.github.com/rest/using-the-rest-api/rate-limits-for-the-rest-api#about-secondary-rate-limits)
and [Best practices for using the REST API](https://docs.github.com/rest/guides/best-practices-for-using-the-rest-api).

This endpoint supports the following custom media types. For more information, see [Media types](https://docs.github.com/rest/using-the-rest-api/getting-started-with-the-rest-api#media-types).

- **application/vnd.github.raw+json**: Returns the raw Markdown body. Response will include `body`. This is the default if you do not pass any specific media type.
- **application/vnd.github.text+json**: Returns a text only representation of the Markdown body. Response will include `body_text`.
- **application/vnd.github.html+json**: Returns HTML rendered from the body's Markdown. Response will include `body_html`.
- **application/vnd.github.full+json**: Returns raw, text, and HTML representations. Response will include `body`, `body_text`, and `body_html`.

### Fine-grained access tokens for "Add a dependency an issue is blocked by"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Issues" repository permissions (write)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "Add a dependency an issue is blocked by"

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
| issue_idintegerRequiredThe id of the issue that blocks the current issue |

### HTTP response status codes for "Add a dependency an issue is blocked by"

| Status code | Description |
| --- | --- |
| 201 | Created |
| 301 | Moved permanently |
| 403 | Forbidden |
| 404 | Resource not found |
| 410 | Gone |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Add a dependency an issue is blocked by"

#### Request example

post/repos/{owner}/{repo}/issues/{issue_number}/dependencies/blocked_by

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/issues/ISSUE_NUMBER/dependencies/blocked_by \
  -d '{"issue_id":1}'`

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

## Remove dependency an issue is blocked by

You can use the REST API to remove a dependency that an issue is blocked by.

Removing content too quickly using this endpoint may result in secondary rate limiting.
For more information, see [Rate limits for the API](https://docs.github.com/rest/using-the-rest-api/rate-limits-for-the-rest-api#about-secondary-rate-limits)
and [Best practices for using the REST API](https://docs.github.com/rest/guides/best-practices-for-using-the-rest-api).

This endpoint supports the following custom media types. For more information, see [Media types](https://docs.github.com/rest/using-the-rest-api/getting-started-with-the-rest-api#media-types).

- **application/vnd.github.raw+json**: Returns the raw Markdown body. Response will include `body`. This is the default if you do not pass a specific media type.
- **application/vnd.github.text+json**: Returns a text only representation of the Markdown body. Response will include `body_text`.
- **application/vnd.github.html+json**: Returns HTML rendered from the body's Markdown. Response will include `body_html`.
- **application/vnd.github.full+json**: Returns raw, text, and HTML representations. Response will include `body`, `body_text`, and `body_html`.

### Fine-grained access tokens for "Remove dependency an issue is blocked by"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Issues" repository permissions (write)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "Remove dependency an issue is blocked by"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| issue_numberintegerRequiredThe number that identifies the issue. |
| issue_idintegerRequiredThe id of the blocking issue to remove as a dependency |

### HTTP response status codes for "Remove dependency an issue is blocked by"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 301 | Moved permanently |
| 400 | Bad Request |
| 401 | Requires authentication |
| 403 | Forbidden |
| 404 | Resource not found |
| 410 | Gone |

### Code samples for "Remove dependency an issue is blocked by"

#### Request example

delete/repos/{owner}/{repo}/issues/{issue_number}/dependencies/blocked_by/{issue_id}

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/issues/ISSUE_NUMBER/dependencies/blocked_by/ISSUE_ID`

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

## List dependencies an issue is blocking

You can use the REST API to list the dependencies an issue is blocking.

This endpoint supports the following custom media types. For more information, see [Media types](https://docs.github.com/rest/using-the-rest-api/getting-started-with-the-rest-api#media-types).

- **application/vnd.github.raw+json**: Returns the raw Markdown body. Response will include `body`. This is the default if you do not pass any specific media type.
- **application/vnd.github.text+json**: Returns a text only representation of the Markdown body. Response will include `body_text`.
- **application/vnd.github.html+json**: Returns HTML rendered from the body's Markdown. Response will include `body_html`.
- **application/vnd.github.full+json**: Returns raw, text, and HTML representations. Response will include `body`, `body_text`, and `body_html`.

### Fine-grained access tokens for "List dependencies an issue is blocking"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Issues" repository permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "List dependencies an issue is blocking"

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

### HTTP response status codes for "List dependencies an issue is blocking"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 301 | Moved permanently |
| 404 | Resource not found |
| 410 | Gone |

### Code samples for "List dependencies an issue is blocking"

#### Request example

get/repos/{owner}/{repo}/issues/{issue_number}/dependencies/blocking

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/issues/ISSUE_NUMBER/dependencies/blocking`

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
