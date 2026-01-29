# REST API endpoints for commit comments and more

# REST API endpoints for commit comments

> Use the REST API to interact with commit comments.

## About commit comments

You can create, edit, and view commit comments using the REST API. A commit comment is a comment made on a specific commit. For more information, see [Working with comments](https://docs.github.com/en/rest/guides/working-with-comments#commit-comments).

---

# REST API endpoints for commits

> Use the REST API to interact with commits.

## List commits

**Signature verification object**

The response will include a `verification` object that describes the result of verifying the commit's signature. The following fields are included in the `verification` object:

| Name | Type | Description |
| --- | --- | --- |
| verified | boolean | Indicates whether GitHub considers the signature in this commit to be verified. |
| reason | string | The reason for verified value. Possible values and their meanings are enumerated in table below. |
| signature | string | The signature that was extracted from the commit. |
| payload | string | The value that was signed. |
| verified_at | string | The date the signature was verified by GitHub. |

These are the possible values for `reason` in the `verification` object:

| Value | Description |
| --- | --- |
| expired_key | The key that made the signature is expired. |
| not_signing_key | The "signing" flag is not among the usage flags in the GPG key that made the signature. |
| gpgverify_error | There was an error communicating with the signature verification service. |
| gpgverify_unavailable | The signature verification service is currently unavailable. |
| unsigned | The object does not include a signature. |
| unknown_signature_type | A non-PGP signature was found in the commit. |
| no_user | No user was associated with thecommitteremail address in the commit. |
| unverified_email | Thecommitteremail address in the commit was associated with a user, but the email address is not verified on their account. |
| bad_email | Thecommitteremail address in the commit is not included in the identities of the PGP key that made the signature. |
| unknown_key | The key that made the signature has not been registered with any user's account. |
| malformed_signature | There was an error parsing the signature. |
| invalid | The signature could not be cryptographically verified using the key whose key-id was found in the signature. |
| valid | None of the above errors applied, so the signature is considered to be verified. |

### Fine-grained access tokens for "List commits"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Contents" repository permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "List commits"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| shastringSHA or branch to start listing commits from. Default: the repository’s default branch (usuallymain). |
| pathstringOnly commits containing this file path will be returned. |
| authorstringGitHub username or email address to use to filter by commit author. |
| committerstringGitHub username or email address to use to filter by commit committer. |
| sincestringOnly show results that were last updated after the given time. This is a timestamp inISO 8601format:YYYY-MM-DDTHH:MM:SSZ. Due to limitations of Git, timestamps must be between 1970-01-01 and 2099-12-31 (inclusive) or unexpected results may be returned. |
| untilstringOnly commits before this date will be returned. This is a timestamp inISO 8601format:YYYY-MM-DDTHH:MM:SSZ. Due to limitations of Git, timestamps must be between 1970-01-01 and 2099-12-31 (inclusive) or unexpected results may be returned. |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| pageintegerThe page number of the results to fetch. For more information, see "Using pagination in the REST API."Default:1 |

### HTTP response status codes for "List commits"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 400 | Bad Request |
| 404 | Resource not found |
| 409 | Conflict |
| 500 | Internal Error |

### Code samples for "List commits"

#### Request example

get/repos/{owner}/{repo}/commits

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/commits`

Response

-
-

`Status: 200``[
{
"url": "https://api.github.com/repos/octocat/Hello-World/commits/6dcb09b5b57875f334f61aebed695e2e4193db5e",
"sha": "6dcb09b5b57875f334f61aebed695e2e4193db5e",
"node_id": "MDY6Q29tbWl0NmRjYjA5YjViNTc4NzVmMzM0ZjYxYWViZWQ2OTVlMmU0MTkzZGI1ZQ==",
"html_url": "https://github.com/octocat/Hello-World/commit/6dcb09b5b57875f334f61aebed695e2e4193db5e",
"comments_url": "https://api.github.com/repos/octocat/Hello-World/commits/6dcb09b5b57875f334f61aebed695e2e4193db5e/comments",
"commit": {
"url": "https://api.github.com/repos/octocat/Hello-World/git/commits/6dcb09b5b57875f334f61aebed695e2e4193db5e",
"author": {
"name": "Monalisa Octocat",
"email": "support@github.com",
"date": "2011-04-14T16:00:49Z"
},
"committer": {
"name": "Monalisa Octocat",
"email": "support@github.com",
"date": "2011-04-14T16:00:49Z"
},
"message": "Fix all the bugs",
"tree": {
"url": "https://api.github.com/repos/octocat/Hello-World/tree/6dcb09b5b57875f334f61aebed695e2e4193db5e",
"sha": "6dcb09b5b57875f334f61aebed695e2e4193db5e"
},
"comment_count": 0,
"verification": {
"verified": false,
"reason": "unsigned",
"signature": null,
"payload": null,
"verified_at": null
}
},
"author": {
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
"committer": {
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
"parents": [
{
"url": "https://api.github.com/repos/octocat/Hello-World/commits/6dcb09b5b57875f334f61aebed695e2e4193db5e",
"sha": "6dcb09b5b57875f334f61aebed695e2e4193db5e"
}
]
}
]`

## List branches for HEAD commit

Protected branches are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, GitHub Enterprise Cloud, and GitHub Enterprise Server. For more information, see [GitHub's products](https://docs.github.com/github/getting-started-with-github/githubs-products) in the GitHub Help documentation.

Returns all branches where the given commit SHA is the HEAD, or latest commit for the branch.

### Fine-grained access tokens for "List branches for HEAD commit"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Contents" repository permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "List branches for HEAD commit"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| commit_shastringRequiredThe SHA of the commit. |

### HTTP response status codes for "List branches for HEAD commit"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 409 | Conflict |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "List branches for HEAD commit"

#### Request example

get/repos/{owner}/{repo}/commits/{commit_sha}/branches-where-head

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/commits/COMMIT_SHA/branches-where-head`

Response

-
-

`Status: 200``[
{
"name": "branch_5",
"commit": {
"sha": "c5b97d5ae6c19d5c5df71a34c7fbeeda2479ccbc",
"url": "https://api.github.com/repos/octocat/Hello-World/commits/c5b97d5ae6c19d5c5df71a34c7fbeeda2479ccbc"
},
"protected": false
}
]`

## List pull requests associated with a commit

Lists the merged pull request that introduced the commit to the repository. If the commit is not present in the default branch, it will return merged and open pull requests associated with the commit.

To list the open or merged pull requests associated with a branch, you can set the `commit_sha` parameter to the branch name.

### Fine-grained access tokens for "List pull requests associated with a commit"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Pull requests" repository permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "List pull requests associated with a commit"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| commit_shastringRequiredThe SHA of the commit. |

| Name, Type, Description |
| --- |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| pageintegerThe page number of the results to fetch. For more information, see "Using pagination in the REST API."Default:1 |

### HTTP response status codes for "List pull requests associated with a commit"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 409 | Conflict |

### Code samples for "List pull requests associated with a commit"

#### Request example

get/repos/{owner}/{repo}/commits/{commit_sha}/pulls

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/commits/COMMIT_SHA/pulls`

Response

-
-

`Status: 200``[
{
"url": "https://api.github.com/repos/octocat/Hello-World/pulls/1347",
"id": 1,
"node_id": "MDExOlB1bGxSZXF1ZXN0MQ==",
"html_url": "https://github.com/octocat/Hello-World/pull/1347",
"diff_url": "https://github.com/octocat/Hello-World/pull/1347.diff",
"patch_url": "https://github.com/octocat/Hello-World/pull/1347.patch",
"issue_url": "https://api.github.com/repos/octocat/Hello-World/issues/1347",
"commits_url": "https://api.github.com/repos/octocat/Hello-World/pulls/1347/commits",
"review_comments_url": "https://api.github.com/repos/octocat/Hello-World/pulls/1347/comments",
"review_comment_url": "https://api.github.com/repos/octocat/Hello-World/pulls/comments{/number}",
"comments_url": "https://api.github.com/repos/octocat/Hello-World/issues/1347/comments",
"statuses_url": "https://api.github.com/repos/octocat/Hello-World/statuses/6dcb09b5b57875f334f61aebed695e2e4193db5e",
"number": 1347,
"state": "open",
"locked": true,
"title": "Amazing new feature",
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
"body": "Please pull these awesome changes in!",
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
"active_lock_reason": "too heated",
"created_at": "2011-01-26T19:01:12Z",
"updated_at": "2011-01-26T19:01:12Z",
"closed_at": "2011-01-26T19:01:12Z",
"merged_at": "2011-01-26T19:01:12Z",
"merge_commit_sha": "e5bd3914e2e596debea16f433f57875b5b90bcd6",
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
},
{
"login": "hubot",
"id": 1,
"node_id": "MDQ6VXNlcjE=",
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
"site_admin": true
}
],
"requested_reviewers": [
{
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
}
],
"requested_teams": [
{
"id": 1,
"node_id": "MDQ6VGVhbTE=",
"url": "https://api.github.com/teams/1",
"html_url": "https://github.com/orgs/github/teams/justice-league",
"name": "Justice League",
"slug": "justice-league",
"description": "A great team.",
"privacy": "closed",
"permission": "admin",
"notification_setting": "notifications_enabled",
"members_url": "https://api.github.com/teams/1/members{/member}",
"repositories_url": "https://api.github.com/teams/1/repos",
"parent": null
}
],
"head": {
"label": "octocat:new-topic",
"ref": "new-topic",
"sha": "6dcb09b5b57875f334f61aebed695e2e4193db5e",
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
"repo": {
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
"template_repository": null,
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
}
},
"base": {
"label": "octocat:master",
"ref": "master",
"sha": "6dcb09b5b57875f334f61aebed695e2e4193db5e",
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
"repo": {
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
"template_repository": null,
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
}
},
"_links": {
"self": {
"href": "https://api.github.com/repos/octocat/Hello-World/pulls/1347"
},
"html": {
"href": "https://github.com/octocat/Hello-World/pull/1347"
},
"issue": {
"href": "https://api.github.com/repos/octocat/Hello-World/issues/1347"
},
"comments": {
"href": "https://api.github.com/repos/octocat/Hello-World/issues/1347/comments"
},
"review_comments": {
"href": "https://api.github.com/repos/octocat/Hello-World/pulls/1347/comments"
},
"review_comment": {
"href": "https://api.github.com/repos/octocat/Hello-World/pulls/comments{/number}"
},
"commits": {
"href": "https://api.github.com/repos/octocat/Hello-World/pulls/1347/commits"
},
"statuses": {
"href": "https://api.github.com/repos/octocat/Hello-World/statuses/6dcb09b5b57875f334f61aebed695e2e4193db5e"
}
},
"author_association": "OWNER",
"auto_merge": null,
"draft": false
}
]`

## Get a commit

Returns the contents of a single commit reference. You must have `read` access for the repository to use this endpoint.

Note

If there are more than 300 files in the commit diff and the default JSON media type is requested, the response will include pagination link headers for the remaining files, up to a limit of 3000 files. Each page contains the static commit information, and the only changes are to the file listing.

This endpoint supports the following custom media types. For more information, see "[Media types](https://docs.github.com/rest/using-the-rest-api/getting-started-with-the-rest-api#media-types)." Pagination query parameters are not supported for these media types.

- **application/vnd.github.diff**: Returns the diff of the commit. Larger diffs may time out and return a 5xx status code.
- **application/vnd.github.patch**: Returns the patch of the commit. Diffs with binary data will have no `patch` property. Larger diffs may time out and return a 5xx status code.
- **application/vnd.github.sha**: Returns the commit's SHA-1 hash. You can use this endpoint to check if a remote reference's SHA-1 hash is the same as your local reference's SHA-1 hash by providing the local SHA-1 reference as the ETag.

**Signature verification object**

The response will include a `verification` object that describes the result of verifying the commit's signature. The following fields are included in the `verification` object:

| Name | Type | Description |
| --- | --- | --- |
| verified | boolean | Indicates whether GitHub considers the signature in this commit to be verified. |
| reason | string | The reason for verified value. Possible values and their meanings are enumerated in table below. |
| signature | string | The signature that was extracted from the commit. |
| payload | string | The value that was signed. |
| verified_at | string | The date the signature was verified by GitHub. |

These are the possible values for `reason` in the `verification` object:

| Value | Description |
| --- | --- |
| expired_key | The key that made the signature is expired. |
| not_signing_key | The "signing" flag is not among the usage flags in the GPG key that made the signature. |
| gpgverify_error | There was an error communicating with the signature verification service. |
| gpgverify_unavailable | The signature verification service is currently unavailable. |
| unsigned | The object does not include a signature. |
| unknown_signature_type | A non-PGP signature was found in the commit. |
| no_user | No user was associated with thecommitteremail address in the commit. |
| unverified_email | Thecommitteremail address in the commit was associated with a user, but the email address is not verified on their account. |
| bad_email | Thecommitteremail address in the commit is not included in the identities of the PGP key that made the signature. |
| unknown_key | The key that made the signature has not been registered with any user's account. |
| malformed_signature | There was an error parsing the signature. |
| invalid | The signature could not be cryptographically verified using the key whose key-id was found in the signature. |
| valid | None of the above errors applied, so the signature is considered to be verified. |

### Fine-grained access tokens for "Get a commit"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Contents" repository permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "Get a commit"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| refstringRequiredThe commit reference. Can be a commit SHA, branch name (heads/BRANCH_NAME), or tag name (tags/TAG_NAME). For more information, see "Git References" in the Git documentation. |

| Name, Type, Description |
| --- |
| pageintegerThe page number of the results to fetch. For more information, see "Using pagination in the REST API."Default:1 |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |

### HTTP response status codes for "Get a commit"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |
| 409 | Conflict |
| 422 | Validation failed, or the endpoint has been spammed. |
| 500 | Internal Error |
| 503 | Service unavailable |

### Code samples for "Get a commit"

#### Request example

get/repos/{owner}/{repo}/commits/{ref}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/commits/REF`

Response

-
-

`Status: 200``{
"url": "https://api.github.com/repos/octocat/Hello-World/commits/6dcb09b5b57875f334f61aebed695e2e4193db5e",
"sha": "6dcb09b5b57875f334f61aebed695e2e4193db5e",
"node_id": "MDY6Q29tbWl0NmRjYjA5YjViNTc4NzVmMzM0ZjYxYWViZWQ2OTVlMmU0MTkzZGI1ZQ==",
"html_url": "https://github.com/octocat/Hello-World/commit/6dcb09b5b57875f334f61aebed695e2e4193db5e",
"comments_url": "https://api.github.com/repos/octocat/Hello-World/commits/6dcb09b5b57875f334f61aebed695e2e4193db5e/comments",
"commit": {
"url": "https://api.github.com/repos/octocat/Hello-World/git/commits/6dcb09b5b57875f334f61aebed695e2e4193db5e",
"author": {
"name": "Monalisa Octocat",
"email": "mona@github.com",
"date": "2011-04-14T16:00:49Z"
},
"committer": {
"name": "Monalisa Octocat",
"email": "mona@github.com",
"date": "2011-04-14T16:00:49Z"
},
"message": "Fix all the bugs",
"tree": {
"url": "https://api.github.com/repos/octocat/Hello-World/tree/6dcb09b5b57875f334f61aebed695e2e4193db5e",
"sha": "6dcb09b5b57875f334f61aebed695e2e4193db5e"
},
"comment_count": 0,
"verification": {
"verified": false,
"reason": "unsigned",
"signature": null,
"payload": null,
"verified_at": null
}
},
"author": {
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
"committer": {
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
"parents": [
{
"url": "https://api.github.com/repos/octocat/Hello-World/commits/6dcb09b5b57875f334f61aebed695e2e4193db5e",
"sha": "6dcb09b5b57875f334f61aebed695e2e4193db5e"
}
],
"stats": {
"additions": 104,
"deletions": 4,
"total": 108
},
"files": [
{
"filename": "file1.txt",
"additions": 10,
"deletions": 2,
"changes": 12,
"status": "modified",
"raw_url": "https://github.com/octocat/Hello-World/raw/7ca483543807a51b6079e54ac4cc392bc29ae284/file1.txt",
"blob_url": "https://github.com/octocat/Hello-World/blob/7ca483543807a51b6079e54ac4cc392bc29ae284/file1.txt",
"patch": "@@ -29,7 +29,7 @@\n....."
}
]
}`

## Compare two commits

Compares two commits against one another. You can compare refs (branches or tags) and commit SHAs in the same repository, or you can compare refs and commit SHAs that exist in different repositories within the same repository network, including fork branches. For more information about how to view a repository's network, see "[Understanding connections between repositories](https://docs.github.com/repositories/viewing-activity-and-data-for-your-repository/understanding-connections-between-repositories)."

This endpoint is equivalent to running the `git log BASE..HEAD` command, but it returns commits in a different order. The `git log BASE..HEAD` command returns commits in reverse chronological order, whereas the API returns commits in chronological order.

This endpoint supports the following custom media types. For more information, see "[Media types](https://docs.github.com/rest/using-the-rest-api/getting-started-with-the-rest-api#media-types)."

- **application/vnd.github.diff**: Returns the diff of the commit.
- **application/vnd.github.patch**: Returns the patch of the commit. Diffs with binary data will have no `patch` property.

The API response includes details about the files that were changed between the two commits. This includes the status of the change (if a file was added, removed, modified, or renamed), and details of the change itself. For example, files with a `renamed` status have a `previous_filename` field showing the previous filename of the file, and files with a `modified` status have a `patch` field showing the changes made to the file.

When calling this endpoint without any paging parameter (`per_page` or `page`), the returned list is limited to 250 commits, and the last commit in the list is the most recent of the entire comparison.

**Working with large comparisons**

To process a response with a large number of commits, use a query parameter (`per_page` or `page`) to paginate the results. When using pagination:

- The list of changed files is only shown on the first page of results, and it includes up to 300 changed files for the entire comparison.
- The results are returned in chronological order, but the last commit in the returned list may not be the most recent one in the entire set if there are more pages of results.

For more information on working with pagination, see "[Using pagination in the REST API](https://docs.github.com/rest/guides/using-pagination-in-the-rest-api)."

**Signature verification object**

The response will include a `verification` object that describes the result of verifying the commit's signature. The `verification` object includes the following fields:

| Name | Type | Description |
| --- | --- | --- |
| verified | boolean | Indicates whether GitHub considers the signature in this commit to be verified. |
| reason | string | The reason for verified value. Possible values and their meanings are enumerated in table below. |
| signature | string | The signature that was extracted from the commit. |
| payload | string | The value that was signed. |
| verified_at | string | The date the signature was verified by GitHub. |

These are the possible values for `reason` in the `verification` object:

| Value | Description |
| --- | --- |
| expired_key | The key that made the signature is expired. |
| not_signing_key | The "signing" flag is not among the usage flags in the GPG key that made the signature. |
| gpgverify_error | There was an error communicating with the signature verification service. |
| gpgverify_unavailable | The signature verification service is currently unavailable. |
| unsigned | The object does not include a signature. |
| unknown_signature_type | A non-PGP signature was found in the commit. |
| no_user | No user was associated with thecommitteremail address in the commit. |
| unverified_email | Thecommitteremail address in the commit was associated with a user, but the email address is not verified on their account. |
| bad_email | Thecommitteremail address in the commit is not included in the identities of the PGP key that made the signature. |
| unknown_key | The key that made the signature has not been registered with any user's account. |
| malformed_signature | There was an error parsing the signature. |
| invalid | The signature could not be cryptographically verified using the key whose key-id was found in the signature. |
| valid | None of the above errors applied, so the signature is considered to be verified. |

### Fine-grained access tokens for "Compare two commits"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Contents" repository permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "Compare two commits"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| baseheadstringRequiredThe base branch and head branch to compare. This parameter expects the formatBASE...HEAD. Both must be branch names inrepo. To compare with a branch that exists in a different repository in the same network asrepo, thebaseheadparameter expects the formatUSERNAME:BASE...USERNAME:HEAD. |

| Name, Type, Description |
| --- |
| pageintegerThe page number of the results to fetch. For more information, see "Using pagination in the REST API."Default:1 |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |

### HTTP response status codes for "Compare two commits"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |
| 500 | Internal Error |
| 503 | Service unavailable |

### Code samples for "Compare two commits"

#### Request example

get/repos/{owner}/{repo}/compare/{basehead}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/compare/BASEHEAD`

Response

-
-

`Status: 200``{
"url": "https://api.github.com/repos/octocat/Hello-World/compare/master...topic",
"html_url": "https://github.com/octocat/Hello-World/compare/master...topic",
"permalink_url": "https://github.com/octocat/Hello-World/compare/octocat:bbcd538c8e72b8c175046e27cc8f907076331401...octocat:0328041d1152db8ae77652d1618a02e57f745f17",
"diff_url": "https://github.com/octocat/Hello-World/compare/master...topic.diff",
"patch_url": "https://github.com/octocat/Hello-World/compare/master...topic.patch",
"base_commit": {
"url": "https://api.github.com/repos/octocat/Hello-World/commits/6dcb09b5b57875f334f61aebed695e2e4193db5e",
"sha": "6dcb09b5b57875f334f61aebed695e2e4193db5e",
"node_id": "MDY6Q29tbWl0NmRjYjA5YjViNTc4NzVmMzM0ZjYxYWViZWQ2OTVlMmU0MTkzZGI1ZQ==",
"html_url": "https://github.com/octocat/Hello-World/commit/6dcb09b5b57875f334f61aebed695e2e4193db5e",
"comments_url": "https://api.github.com/repos/octocat/Hello-World/commits/6dcb09b5b57875f334f61aebed695e2e4193db5e/comments",
"commit": {
"url": "https://api.github.com/repos/octocat/Hello-World/git/commits/6dcb09b5b57875f334f61aebed695e2e4193db5e",
"author": {
"name": "Monalisa Octocat",
"email": "mona@github.com",
"date": "2011-04-14T16:00:49Z"
},
"committer": {
"name": "Monalisa Octocat",
"email": "mona@github.com",
"date": "2011-04-14T16:00:49Z"
},
"message": "Fix all the bugs",
"tree": {
"url": "https://api.github.com/repos/octocat/Hello-World/tree/6dcb09b5b57875f334f61aebed695e2e4193db5e",
"sha": "6dcb09b5b57875f334f61aebed695e2e4193db5e"
},
"comment_count": 0,
"verification": {
"verified": false,
"reason": "unsigned",
"signature": null,
"payload": null,
"verified_at": null
}
},
"author": {
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
"committer": {
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
"parents": [
{
"url": "https://api.github.com/repos/octocat/Hello-World/commits/6dcb09b5b57875f334f61aebed695e2e4193db5e",
"sha": "6dcb09b5b57875f334f61aebed695e2e4193db5e"
}
]
},
"merge_base_commit": {
"url": "https://api.github.com/repos/octocat/Hello-World/commits/6dcb09b5b57875f334f61aebed695e2e4193db5e",
"sha": "6dcb09b5b57875f334f61aebed695e2e4193db5e",
"node_id": "MDY6Q29tbWl0NmRjYjA5YjViNTc4NzVmMzM0ZjYxYWViZWQ2OTVlMmU0MTkzZGI1ZQ==",
"html_url": "https://github.com/octocat/Hello-World/commit/6dcb09b5b57875f334f61aebed695e2e4193db5e",
"comments_url": "https://api.github.com/repos/octocat/Hello-World/commits/6dcb09b5b57875f334f61aebed695e2e4193db5e/comments",
"commit": {
"url": "https://api.github.com/repos/octocat/Hello-World/git/commits/6dcb09b5b57875f334f61aebed695e2e4193db5e",
"author": {
"name": "Monalisa Octocat",
"email": "mona@github.com",
"date": "2011-04-14T16:00:49Z"
},
"committer": {
"name": "Monalisa Octocat",
"email": "mona@github.com",
"date": "2011-04-14T16:00:49Z"
},
"message": "Fix all the bugs",
"tree": {
"url": "https://api.github.com/repos/octocat/Hello-World/tree/6dcb09b5b57875f334f61aebed695e2e4193db5e",
"sha": "6dcb09b5b57875f334f61aebed695e2e4193db5e"
},
"comment_count": 0,
"verification": {
"verified": false,
"reason": "unsigned",
"signature": null,
"payload": null,
"verified_at": null
}
},
"author": {
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
"committer": {
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
"parents": [
{
"url": "https://api.github.com/repos/octocat/Hello-World/commits/6dcb09b5b57875f334f61aebed695e2e4193db5e",
"sha": "6dcb09b5b57875f334f61aebed695e2e4193db5e"
}
]
},
"status": "behind",
"ahead_by": 1,
"behind_by": 2,
"total_commits": 1,
"commits": [
{
"url": "https://api.github.com/repos/octocat/Hello-World/commits/6dcb09b5b57875f334f61aebed695e2e4193db5e",
"sha": "6dcb09b5b57875f334f61aebed695e2e4193db5e",
"node_id": "MDY6Q29tbWl0NmRjYjA5YjViNTc4NzVmMzM0ZjYxYWViZWQ2OTVlMmU0MTkzZGI1ZQ==",
"html_url": "https://github.com/octocat/Hello-World/commit/6dcb09b5b57875f334f61aebed695e2e4193db5e",
"comments_url": "https://api.github.com/repos/octocat/Hello-World/commits/6dcb09b5b57875f334f61aebed695e2e4193db5e/comments",
"commit": {
"url": "https://api.github.com/repos/octocat/Hello-World/git/commits/6dcb09b5b57875f334f61aebed695e2e4193db5e",
"author": {
"name": "Monalisa Octocat",
"email": "mona@github.com",
"date": "2011-04-14T16:00:49Z"
},
"committer": {
"name": "Monalisa Octocat",
"email": "mona@github.com",
"date": "2011-04-14T16:00:49Z"
},
"message": "Fix all the bugs",
"tree": {
"url": "https://api.github.com/repos/octocat/Hello-World/tree/6dcb09b5b57875f334f61aebed695e2e4193db5e",
"sha": "6dcb09b5b57875f334f61aebed695e2e4193db5e"
},
"comment_count": 0,
"verification": {
"verified": false,
"reason": "unsigned",
"signature": null,
"payload": null,
"verified_at": null
}
},
"author": {
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
"committer": {
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
"parents": [
{
"url": "https://api.github.com/repos/octocat/Hello-World/commits/6dcb09b5b57875f334f61aebed695e2e4193db5e",
"sha": "6dcb09b5b57875f334f61aebed695e2e4193db5e"
}
]
}
],
"files": [
{
"sha": "bbcd538c8e72b8c175046e27cc8f907076331401",
"filename": "file1.txt",
"status": "added",
"additions": 103,
"deletions": 21,
"changes": 124,
"blob_url": "https://github.com/octocat/Hello-World/blob/6dcb09b5b57875f334f61aebed695e2e4193db5e/file1.txt",
"raw_url": "https://github.com/octocat/Hello-World/raw/6dcb09b5b57875f334f61aebed695e2e4193db5e/file1.txt",
"contents_url": "https://api.github.com/repos/octocat/Hello-World/contents/file1.txt?ref=6dcb09b5b57875f334f61aebed695e2e4193db5e",
"patch": "@@ -132,7 +132,7 @@ module Test @@ -1000,7 +1000,7 @@ module Test"
}
]
}`

---

# REST API endpoints for commit statuses

> Use the REST API to interact with commit statuses.

## About commit statuses

You can use the REST API to allow external services to mark commits with an `error`, `failure`, `pending`, or `success` state, which is then reflected in pull requests involving those commits. Statuses can also include an optional `description` and `target_url`, and we highly recommend providing them as they make statuses much more useful in the GitHub UI.

As an example, one common use is for continuous integration services to mark commits as passing or failing builds using status. The `target_url` would be the full URL to the build output, and the `description` would be the high level summary of what happened with the build.

Statuses can include a `context` to indicate what service is providing that status. For example, you may have your continuous integration service push statuses with a context of `ci`, and a security audit tool push statuses with a context of `security`. You can then use the REST API to [Get the combined status for a specific reference](https://docs.github.com/en/rest/commits/statuses#get-the-combined-status-for-a-specific-reference) to retrieve the whole status for a commit.

Note that the `repo:status` [OAuth scope](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/scopes-for-oauth-apps) grants targeted access to statuses **without** also granting access to repository code, while the `repo` scope grants permission to code as well as statuses.

If you are developing a GitHub App  and want to provide more detailed information about an external service, you may want to use the REST API to manage checks. For more information, see [REST API endpoints for checks](https://docs.github.com/en/rest/checks).
