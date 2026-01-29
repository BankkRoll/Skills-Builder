# REST API endpoints for issues

# REST API endpoints for issues

> Use the REST API to manage issues and pull requests.

## List issues assigned to the authenticated user

List issues assigned to the authenticated user across all visible repositories including owned repositories, member
repositories, and organization repositories. You can use the `filter` query parameter to fetch issues that are not
necessarily assigned to you.

Note

GitHub's REST API considers every pull request an issue, but not every issue is a pull request. For this reason, "Issues" endpoints may return both issues and pull requests in the response. You can identify pull requests by the `pull_request` key. Be aware that the `id` of a pull request returned from "Issues" endpoints will be an *issue id*. To find out the pull request id, use the "[List pull requests](https://docs.github.com/rest/pulls/pulls#list-pull-requests)" endpoint.

This endpoint supports the following custom media types. For more information, see "[Media types](https://docs.github.com/rest/using-the-rest-api/getting-started-with-the-rest-api#media-types)."

- **application/vnd.github.raw+json**: Returns the raw markdown body. Response will include `body`. This is the default if you do not pass any specific media type.
- **application/vnd.github.text+json**: Returns a text only representation of the markdown body. Response will include `body_text`.
- **application/vnd.github.html+json**: Returns HTML rendered from the body's markdown. Response will include `body_html`.
- **application/vnd.github.full+json**: Returns raw, text, and HTML representations. Response will include `body`, `body_text`, and `body_html`.

### Fine-grained access tokens for "List issues assigned to the authenticated user"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token does not require any permissions.

### Parameters for "List issues assigned to the authenticated user"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| filterstringIndicates which sorts of issues to return.assignedmeans issues assigned to you.createdmeans issues created by you.mentionedmeans issues mentioning you.subscribedmeans issues you're subscribed to updates for.allorreposmeans all issues you can see, regardless of participation or creation.Default:assignedCan be one of:assigned,created,mentioned,subscribed,repos,all |
| statestringIndicates the state of the issues to return.Default:openCan be one of:open,closed,all |
| labelsstringA list of comma separated label names. Example:bug,ui,@high |
| sortstringWhat to sort results by.Default:createdCan be one of:created,updated,comments |
| directionstringThe direction to sort the results by.Default:descCan be one of:asc,desc |
| sincestringOnly show results that were last updated after the given time. This is a timestamp inISO 8601format:YYYY-MM-DDTHH:MM:SSZ. |
| collabboolean |
| orgsboolean |
| ownedboolean |
| pullsboolean |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| pageintegerThe page number of the results to fetch. For more information, see "Using pagination in the REST API."Default:1 |

### HTTP response status codes for "List issues assigned to the authenticated user"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 304 | Not modified |
| 404 | Resource not found |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "List issues assigned to the authenticated user"

#### Request example

get/issues

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/issues`

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
"is_template": true,
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
"allow_rebase_merge": true,
"temp_clone_token": "ABTLWHOULUVAXGTRYU7OC2876QJ2O",
"allow_squash_merge": true,
"allow_auto_merge": false,
"delete_branch_on_merge": true,
"allow_merge_commit": true,
"subscribers_count": 42,
"network_count": 0,
"license": {
"key": "mit",
"name": "MIT License",
"url": "https://api.github.com/licenses/mit",
"spdx_id": "MIT",
"node_id": "MDc6TGljZW5zZW1pdA==",
"html_url": "https://github.com/licenses/mit"
},
"forks": 1,
"open_issues": 1,
"watchers": 1
},
"author_association": "COLLABORATOR"
}
]`

## List organization issues assigned to the authenticated user

List issues in an organization assigned to the authenticated user.

Note

GitHub's REST API considers every pull request an issue, but not every issue is a pull request. For this reason, "Issues" endpoints may return both issues and pull requests in the response. You can identify pull requests by the `pull_request` key. Be aware that the `id` of a pull request returned from "Issues" endpoints will be an *issue id*. To find out the pull request id, use the "[List pull requests](https://docs.github.com/rest/pulls/pulls#list-pull-requests)" endpoint.

This endpoint supports the following custom media types. For more information, see "[Media types](https://docs.github.com/rest/using-the-rest-api/getting-started-with-the-rest-api#media-types)."

- **application/vnd.github.raw+json**: Returns the raw markdown body. Response will include `body`. This is the default if you do not pass any specific media type.
- **application/vnd.github.text+json**: Returns a text only representation of the markdown body. Response will include `body_text`.
- **application/vnd.github.html+json**: Returns HTML rendered from the body's markdown. Response will include `body_html`.
- **application/vnd.github.full+json**: Returns raw, text, and HTML representations. Response will include `body`, `body_text`, and `body_html`.

### Fine-grained access tokens for "List organization issues assigned to the authenticated user"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token does not require any permissions.

### Parameters for "List organization issues assigned to the authenticated user"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| filterstringIndicates which sorts of issues to return.assignedmeans issues assigned to you.createdmeans issues created by you.mentionedmeans issues mentioning you.subscribedmeans issues you're subscribed to updates for.allorreposmeans all issues you can see, regardless of participation or creation.Default:assignedCan be one of:assigned,created,mentioned,subscribed,repos,all |
| statestringIndicates the state of the issues to return.Default:openCan be one of:open,closed,all |
| labelsstringA list of comma separated label names. Example:bug,ui,@high |
| typestringCan be the name of an issue type. |
| sortstringWhat to sort results by.Default:createdCan be one of:created,updated,comments |
| directionstringThe direction to sort the results by.Default:descCan be one of:asc,desc |
| sincestringOnly show results that were last updated after the given time. This is a timestamp inISO 8601format:YYYY-MM-DDTHH:MM:SSZ. |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| pageintegerThe page number of the results to fetch. For more information, see "Using pagination in the REST API."Default:1 |

### HTTP response status codes for "List organization issues assigned to the authenticated user"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |

### Code samples for "List organization issues assigned to the authenticated user"

#### Request example

get/orgs/{org}/issues

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/issues`

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
"is_template": true,
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
"allow_rebase_merge": true,
"temp_clone_token": "ABTLWHOULUVAXGTRYU7OC2876QJ2O",
"allow_squash_merge": true,
"allow_auto_merge": false,
"delete_branch_on_merge": true,
"allow_merge_commit": true,
"subscribers_count": 42,
"network_count": 0,
"license": {
"key": "mit",
"name": "MIT License",
"url": "https://api.github.com/licenses/mit",
"spdx_id": "MIT",
"node_id": "MDc6TGljZW5zZW1pdA==",
"html_url": "https://github.com/licenses/mit"
},
"forks": 1,
"open_issues": 1,
"watchers": 1
},
"author_association": "COLLABORATOR"
}
]`

## List repository issues

List issues in a repository. Only open issues will be listed.

Note

GitHub's REST API considers every pull request an issue, but not every issue is a pull request. For this reason, "Issues" endpoints may return both issues and pull requests in the response. You can identify pull requests by the `pull_request` key. Be aware that the `id` of a pull request returned from "Issues" endpoints will be an *issue id*. To find out the pull request id, use the "[List pull requests](https://docs.github.com/rest/pulls/pulls#list-pull-requests)" endpoint.

This endpoint supports the following custom media types. For more information, see "[Media types](https://docs.github.com/rest/using-the-rest-api/getting-started-with-the-rest-api#media-types)."

- **application/vnd.github.raw+json**: Returns the raw markdown body. Response will include `body`. This is the default if you do not pass any specific media type.
- **application/vnd.github.text+json**: Returns a text only representation of the markdown body. Response will include `body_text`.
- **application/vnd.github.html+json**: Returns HTML rendered from the body's markdown. Response will include `body_html`.
- **application/vnd.github.full+json**: Returns raw, text, and HTML representations. Response will include `body`, `body_text`, and `body_html`.

### Fine-grained access tokens for "List repository issues"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Issues" repository permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "List repository issues"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| milestonestringIf anintegeris passed, it should refer to a milestone by itsnumberfield. If the string*is passed, issues with any milestone are accepted. If the stringnoneis passed, issues without milestones are returned. |
| statestringIndicates the state of the issues to return.Default:openCan be one of:open,closed,all |
| assigneestringCan be the name of a user. Pass innonefor issues with no assigned user, and*for issues assigned to any user. |
| typestringCan be the name of an issue type. If the string*is passed, issues with any type are accepted. If the stringnoneis passed, issues without type are returned. |
| creatorstringThe user that created the issue. |
| mentionedstringA user that's mentioned in the issue. |
| labelsstringA list of comma separated label names. Example:bug,ui,@high |
| sortstringWhat to sort results by.Default:createdCan be one of:created,updated,comments |
| directionstringThe direction to sort the results by.Default:descCan be one of:asc,desc |
| sincestringOnly show results that were last updated after the given time. This is a timestamp inISO 8601format:YYYY-MM-DDTHH:MM:SSZ. |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| pageintegerThe page number of the results to fetch. For more information, see "Using pagination in the REST API."Default:1 |

### HTTP response status codes for "List repository issues"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 301 | Moved permanently |
| 404 | Resource not found |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "List repository issues"

#### Request example

get/repos/{owner}/{repo}/issues

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/issues`

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

## Create an issue

Any user with pull access to a repository can create an issue. If [issues are disabled in the repository](https://docs.github.com/articles/disabling-issues/), the API returns a `410 Gone` status.

This endpoint triggers [notifications](https://docs.github.com/github/managing-subscriptions-and-notifications-on-github/about-notifications). Creating content too quickly using this endpoint may result in secondary rate limiting. For more information, see "[Rate limits for the API](https://docs.github.com/rest/using-the-rest-api/rate-limits-for-the-rest-api#about-secondary-rate-limits)"
and "[Best practices for using the REST API](https://docs.github.com/rest/guides/best-practices-for-using-the-rest-api)."

This endpoint supports the following custom media types. For more information, see "[Media types](https://docs.github.com/rest/using-the-rest-api/getting-started-with-the-rest-api#media-types)."

- **application/vnd.github.raw+json**: Returns the raw markdown body. Response will include `body`. This is the default if you do not pass any specific media type.
- **application/vnd.github.text+json**: Returns a text only representation of the markdown body. Response will include `body_text`.
- **application/vnd.github.html+json**: Returns HTML rendered from the body's markdown. Response will include `body_html`.
- **application/vnd.github.full+json**: Returns raw, text, and HTML representations. Response will include `body`, `body_text`, and `body_html`.

### Fine-grained access tokens for "Create an issue"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Issues" repository permissions (write)

### Parameters for "Create an issue"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| titlestring or integerRequiredThe title of the issue. |
| bodystringThe contents of the issue. |
| assigneestring or nullLogin for the user that this issue should be assigned to.NOTE: Only users with push access can set the assignee for new issues. The assignee is silently dropped otherwise.This field is closing down. |
| milestonenull or string or integerThenumberof the milestone to associate this issue with.NOTE: Only users with push access can set the milestone for new issues. The milestone is silently dropped otherwise. |
| labelsarrayLabels to associate with this issue.NOTE: Only users with push access can set labels for new issues. Labels are silently dropped otherwise. |
| assigneesarray of stringsLogins for Users to assign to this issue.NOTE: Only users with push access can set assignees for new issues. Assignees are silently dropped otherwise. |
| typestring or nullThe name of the issue type to associate with this issue.NOTE: Only users with push access can set the type for new issues. The type is silently dropped otherwise. |

### HTTP response status codes for "Create an issue"

| Status code | Description |
| --- | --- |
| 201 | Created |
| 400 | Bad Request |
| 403 | Forbidden |
| 404 | Resource not found |
| 410 | Gone |
| 422 | Validation failed, or the endpoint has been spammed. |
| 503 | Service unavailable |

### Code samples for "Create an issue"

#### Request example

post/repos/{owner}/{repo}/issues

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/issues \
  -d '{"title":"Found a bug","body":"I'\''m having a problem with this.","assignees":["octocat"],"milestone":1,"labels":["bug"]}'`

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

## Get an issue

The API returns a [301 Moved Permanentlystatus](https://docs.github.com/rest/guides/best-practices-for-using-the-rest-api#follow-redirects) if the issue was
[transferred](https://docs.github.com/articles/transferring-an-issue-to-another-repository/) to another repository. If
the issue was transferred to or deleted from a repository where the authenticated user lacks read access, the API
returns a `404 Not Found` status. If the issue was deleted from a repository where the authenticated user has read
access, the API returns a `410 Gone` status. To receive webhook events for transferred and deleted issues, subscribe
to the [issues](https://docs.github.com/webhooks/event-payloads/#issues) webhook.

Note

GitHub's REST API considers every pull request an issue, but not every issue is a pull request. For this reason, "Issues" endpoints may return both issues and pull requests in the response. You can identify pull requests by the `pull_request` key. Be aware that the `id` of a pull request returned from "Issues" endpoints will be an *issue id*. To find out the pull request id, use the "[List pull requests](https://docs.github.com/rest/pulls/pulls#list-pull-requests)" endpoint.

This endpoint supports the following custom media types. For more information, see "[Media types](https://docs.github.com/rest/using-the-rest-api/getting-started-with-the-rest-api#media-types)."

- **application/vnd.github.raw+json**: Returns the raw markdown body. Response will include `body`. This is the default if you do not pass any specific media type.
- **application/vnd.github.text+json**: Returns a text only representation of the markdown body. Response will include `body_text`.
- **application/vnd.github.html+json**: Returns HTML rendered from the body's markdown. Response will include `body_html`.
- **application/vnd.github.full+json**: Returns raw, text, and HTML representations. Response will include `body`, `body_text`, and `body_html`.

### Fine-grained access tokens for "Get an issue"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Issues" repository permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "Get an issue"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| issue_numberintegerRequiredThe number that identifies the issue. |

### HTTP response status codes for "Get an issue"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 301 | Moved permanently |
| 304 | Not modified |
| 404 | Resource not found |
| 410 | Gone |

### Code samples for "Get an issue"

#### Request example

get/repos/{owner}/{repo}/issues/{issue_number}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/issues/ISSUE_NUMBER`

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

## Update an issue

Issue owners and users with push access or Triage role can edit an issue.

This endpoint supports the following custom media types. For more information, see "[Media types](https://docs.github.com/rest/using-the-rest-api/getting-started-with-the-rest-api#media-types)."

- **application/vnd.github.raw+json**: Returns the raw markdown body. Response will include `body`. This is the default if you do not pass any specific media type.
- **application/vnd.github.text+json**: Returns a text only representation of the markdown body. Response will include `body_text`.
- **application/vnd.github.html+json**: Returns HTML rendered from the body's markdown. Response will include `body_html`.
- **application/vnd.github.full+json**: Returns raw, text, and HTML representations. Response will include `body`, `body_text`, and `body_html`.

### Fine-grained access tokens for "Update an issue"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have at least one of the following permission sets:

- "Issues" repository permissions (write)
- "Pull requests" repository permissions (write)

### Parameters for "Update an issue"

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
| titlenull or string or integerThe title of the issue. |
| bodystring or nullThe contents of the issue. |
| assigneestring or nullUsername to assign to this issue.This field is closing down. |
| statestringThe open or closed state of the issue.Can be one of:open,closed |
| state_reasonstring or nullThe reason for the state change. Ignored unlessstateis changed.Can be one of:completed,not_planned,duplicate,reopened,null |
| milestonenull or string or integerThenumberof the milestone to associate this issue with or usenullto remove the current milestone. Only users with push access can set the milestone for issues. Without push access to the repository, milestone changes are silently dropped. |
| labelsarrayLabels to associate with this issue. Pass one or more labels toreplacethe set of labels on this issue. Send an empty array ([]) to clear all labels from the issue. Only users with push access can set labels for issues. Without push access to the repository, label changes are silently dropped. |
| assigneesarray of stringsUsernames to assign to this issue. Pass one or more user logins toreplacethe set of assignees on this issue. Send an empty array ([]) to clear all assignees from the issue. Only users with push access can set assignees for new issues. Without push access to the repository, assignee changes are silently dropped. |
| typestring or nullThe name of the issue type to associate with this issue or usenullto remove the current issue type. Only users with push access can set the type for issues. Without push access to the repository, type changes are silently dropped. |

### HTTP response status codes for "Update an issue"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 301 | Moved permanently |
| 403 | Forbidden |
| 404 | Resource not found |
| 410 | Gone |
| 422 | Validation failed, or the endpoint has been spammed. |
| 503 | Service unavailable |

### Code samples for "Update an issue"

#### Request example

patch/repos/{owner}/{repo}/issues/{issue_number}

-
-
-

`curl -L \
  -X PATCH \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/issues/ISSUE_NUMBER \
  -d '{"title":"Found a bug","body":"I'\''m having a problem with this.","assignees":["octocat"],"milestone":1,"state":"open","labels":["bug"]}'`

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

## Lock an issue

Users with push access can lock an issue or pull request's conversation.

Note that, if you choose not to pass any parameters, you'll need to set `Content-Length` to zero when calling out to this endpoint. For more information, see "[HTTP method](https://docs.github.com/rest/guides/getting-started-with-the-rest-api#http-method)."

### Fine-grained access tokens for "Lock an issue"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have at least one of the following permission sets:

- "Issues" repository permissions (write)
- "Pull requests" repository permissions (write)

### Parameters for "Lock an issue"

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
| lock_reasonstringThe reason for locking the issue or pull request conversation. Lock will fail if you don't use one of these reasons:off-topictoo heatedresolvedspamCan be one of:off-topic,too heated,resolved,spam |

### HTTP response status codes for "Lock an issue"

| Status code | Description |
| --- | --- |
| 204 | No Content |
| 403 | Forbidden |
| 404 | Resource not found |
| 410 | Gone |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Lock an issue"

#### Request example

put/repos/{owner}/{repo}/issues/{issue_number}/lock

-
-
-

`curl -L \
  -X PUT \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/issues/ISSUE_NUMBER/lock \
  -d '{"lock_reason":"off-topic"}'`

Response

`Status: 204`

## Unlock an issue

Users with push access can unlock an issue's conversation.

### Fine-grained access tokens for "Unlock an issue"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have at least one of the following permission sets:

- "Issues" repository permissions (write)
- "Pull requests" repository permissions (write)

### Parameters for "Unlock an issue"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| issue_numberintegerRequiredThe number that identifies the issue. |

### HTTP response status codes for "Unlock an issue"

| Status code | Description |
| --- | --- |
| 204 | No Content |
| 403 | Forbidden |
| 404 | Resource not found |

### Code samples for "Unlock an issue"

#### Request example

delete/repos/{owner}/{repo}/issues/{issue_number}/lock

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/issues/ISSUE_NUMBER/lock`

Response

`Status: 204`

## List user account issues assigned to the authenticated user

List issues across owned and member repositories assigned to the authenticated user.

Note

GitHub's REST API considers every pull request an issue, but not every issue is a pull request. For this reason, "Issues" endpoints may return both issues and pull requests in the response. You can identify pull requests by the `pull_request` key. Be aware that the `id` of a pull request returned from "Issues" endpoints will be an *issue id*. To find out the pull request id, use the "[List pull requests](https://docs.github.com/rest/pulls/pulls#list-pull-requests)" endpoint.

This endpoint supports the following custom media types. For more information, see "[Media types](https://docs.github.com/rest/using-the-rest-api/getting-started-with-the-rest-api#media-types)."

- **application/vnd.github.raw+json**: Returns the raw markdown body. Response will include `body`. This is the default if you do not pass any specific media type.
- **application/vnd.github.text+json**: Returns a text only representation of the markdown body. Response will include `body_text`.
- **application/vnd.github.html+json**: Returns HTML rendered from the body's markdown. Response will include `body_html`.
- **application/vnd.github.full+json**: Returns raw, text, and HTML representations. Response will include `body`, `body_text`, and `body_html`.

### Fine-grained access tokens for "List user account issues assigned to the authenticated user"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token does not require any permissions.

### Parameters for "List user account issues assigned to the authenticated user"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| filterstringIndicates which sorts of issues to return.assignedmeans issues assigned to you.createdmeans issues created by you.mentionedmeans issues mentioning you.subscribedmeans issues you're subscribed to updates for.allorreposmeans all issues you can see, regardless of participation or creation.Default:assignedCan be one of:assigned,created,mentioned,subscribed,repos,all |
| statestringIndicates the state of the issues to return.Default:openCan be one of:open,closed,all |
| labelsstringA list of comma separated label names. Example:bug,ui,@high |
| sortstringWhat to sort results by.Default:createdCan be one of:created,updated,comments |
| directionstringThe direction to sort the results by.Default:descCan be one of:asc,desc |
| sincestringOnly show results that were last updated after the given time. This is a timestamp inISO 8601format:YYYY-MM-DDTHH:MM:SSZ. |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| pageintegerThe page number of the results to fetch. For more information, see "Using pagination in the REST API."Default:1 |

### HTTP response status codes for "List user account issues assigned to the authenticated user"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 304 | Not modified |
| 404 | Resource not found |

### Code samples for "List user account issues assigned to the authenticated user"

#### Request example

get/user/issues

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/user/issues`

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
"is_template": true,
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
"allow_rebase_merge": true,
"temp_clone_token": "ABTLWHOULUVAXGTRYU7OC2876QJ2O",
"allow_squash_merge": true,
"allow_auto_merge": false,
"delete_branch_on_merge": true,
"allow_merge_commit": true,
"subscribers_count": 42,
"network_count": 0,
"license": {
"key": "mit",
"name": "MIT License",
"url": "https://api.github.com/licenses/mit",
"spdx_id": "MIT",
"node_id": "MDc6TGljZW5zZW1pdA==",
"html_url": "https://github.com/licenses/mit"
},
"forks": 1,
"open_issues": 1,
"watchers": 1
},
"author_association": "COLLABORATOR"
}
]`
