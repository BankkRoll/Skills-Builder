# REST API endpoints for branches

# REST API endpoints for branches

> Use the REST API to modify branches and their protection settings.

## List branches

### Fine-grained access tokens for "List branches"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Contents" repository permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "List branches"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| protectedbooleanSetting totruereturns only branches protected by branch protections or rulesets. When set tofalse, only unprotected branches are returned. Omitting this parameter returns all branches. |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| pageintegerThe page number of the results to fetch. For more information, see "Using pagination in the REST API."Default:1 |

### HTTP response status codes for "List branches"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |

### Code samples for "List branches"

#### Request example

get/repos/{owner}/{repo}/branches

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/branches`

Response

-
-

`Status: 200``[
{
"name": "master",
"commit": {
"sha": "c5b97d5ae6c19d5c5df71a34c7fbeeda2479ccbc",
"url": "https://api.github.com/repos/octocat/Hello-World/commits/c5b97d5ae6c19d5c5df71a34c7fbeeda2479ccbc"
},
"protected": true,
"protection": {
"required_status_checks": {
"enforcement_level": "non_admins",
"contexts": [
"ci-test",
"linter"
]
}
},
"protection_url": "https://api.github.com/repos/octocat/hello-world/branches/master/protection"
}
]`

## Get a branch

### Fine-grained access tokens for "Get a branch"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Contents" repository permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "Get a branch"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| branchstringRequiredThe name of the branch. Cannot contain wildcard characters. To use wildcard characters in branch names, usethe GraphQL API. |

### HTTP response status codes for "Get a branch"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 301 | Moved permanently |
| 404 | Resource not found |

### Code samples for "Get a branch"

#### Request example

get/repos/{owner}/{repo}/branches/{branch}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/branches/BRANCH`

Response

-
-

`Status: 200``{
"name": "main",
"commit": {
"sha": "7fd1a60b01f91b314f59955a4e4d4e80d8edf11d",
"node_id": "MDY6Q29tbWl0MTI5NjI2OTo3ZmQxYTYwYjAxZjkxYjMxNGY1OTk1NWE0ZTRkNGU4MGQ4ZWRmMTFk",
"commit": {
"author": {
"name": "The Octocat",
"email": "octocat@nowhere.com",
"date": "2012-03-06T23:06:50Z"
},
"committer": {
"name": "The Octocat",
"email": "octocat@nowhere.com",
"date": "2012-03-06T23:06:50Z"
},
"message": "Merge pull request #6 from Spaceghost/patch-1\n\nNew line at end of file.",
"tree": {
"sha": "b4eecafa9be2f2006ce1b709d6857b07069b4608",
"url": "https://api.github.com/repos/octocat/Hello-World/git/trees/b4eecafa9be2f2006ce1b709d6857b07069b4608"
},
"url": "https://api.github.com/repos/octocat/Hello-World/git/commits/7fd1a60b01f91b314f59955a4e4d4e80d8edf11d",
"comment_count": 77,
"verification": {
"verified": false,
"reason": "unsigned",
"signature": null,
"payload": null,
"verified_at": null
}
},
"url": "https://api.github.com/repos/octocat/Hello-World/commits/7fd1a60b01f91b314f59955a4e4d4e80d8edf11d",
"html_url": "https://github.com/octocat/Hello-World/commit/7fd1a60b01f91b314f59955a4e4d4e80d8edf11d",
"comments_url": "https://api.github.com/repos/octocat/Hello-World/commits/7fd1a60b01f91b314f59955a4e4d4e80d8edf11d/comments",
"author": {
"login": "octocat",
"id": 583231,
"node_id": "MDQ6VXNlcjU4MzIzMQ==",
"avatar_url": "https://avatars.githubusercontent.com/u/583231?v=4",
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
"id": 583231,
"node_id": "MDQ6VXNlcjU4MzIzMQ==",
"avatar_url": "https://avatars.githubusercontent.com/u/583231?v=4",
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
"sha": "553c2077f0edc3d5dc5d17262f6aa498e69d6f8e",
"url": "https://api.github.com/repos/octocat/Hello-World/commits/553c2077f0edc3d5dc5d17262f6aa498e69d6f8e",
"html_url": "https://github.com/octocat/Hello-World/commit/553c2077f0edc3d5dc5d17262f6aa498e69d6f8e"
},
{
"sha": "762941318ee16e59dabbacb1b4049eec22f0d303",
"url": "https://api.github.com/repos/octocat/Hello-World/commits/762941318ee16e59dabbacb1b4049eec22f0d303",
"html_url": "https://github.com/octocat/Hello-World/commit/762941318ee16e59dabbacb1b4049eec22f0d303"
}
]
},
"_links": {
"self": "https://api.github.com/repos/octocat/Hello-World/branches/main",
"html": "https://github.com/octocat/Hello-World/tree/main"
},
"protected": false,
"protection": {
"enabled": false,
"required_status_checks": {
"enforcement_level": "off",
"contexts": [],
"checks": []
}
},
"protection_url": "https://api.github.com/repos/octocat/Hello-World/branches/main/protection"
}`

## Rename a branch

Renames a branch in a repository.

Note

Although the API responds immediately, the branch rename process might take some extra time to complete in the background. You won't be able to push to the old branch name while the rename process is in progress. For more information, see "[Renaming a branch](https://docs.github.com/github/administering-a-repository/renaming-a-branch)".

The authenticated user must have push access to the branch. If the branch is the default branch, the authenticated user must also have admin or owner permissions.

In order to rename the default branch, fine-grained access tokens also need the `administration:write` repository permission.

### Fine-grained access tokens for "Rename a branch"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Contents" repository permissions (write)

### Parameters for "Rename a branch"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| branchstringRequiredThe name of the branch. Cannot contain wildcard characters. To use wildcard characters in branch names, usethe GraphQL API. |

| Name, Type, Description |
| --- |
| new_namestringRequiredThe new name of the branch. |

### HTTP response status codes for "Rename a branch"

| Status code | Description |
| --- | --- |
| 201 | Created |
| 403 | Forbidden |
| 404 | Resource not found |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Rename a branch"

#### Request example

post/repos/{owner}/{repo}/branches/{branch}/rename

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/branches/BRANCH/rename \
  -d '{"new_name":"my_renamed_branch"}'`

Response

-
-

`Status: 201``{
"name": "master",
"commit": {
"sha": "7fd1a60b01f91b314f59955a4e4d4e80d8edf11d",
"node_id": "MDY6Q29tbWl0N2ZkMWE2MGIwMWY5MWIzMTRmNTk5NTVhNGU0ZDRlODBkOGVkZjExZA==",
"commit": {
"author": {
"name": "The Octocat",
"date": "2012-03-06T15:06:50-08:00",
"email": "octocat@nowhere.com"
},
"url": "https://api.github.com/repos/octocat/Hello-World/git/commits/7fd1a60b01f91b314f59955a4e4d4e80d8edf11d",
"message": "Merge pull request #6 from Spaceghost/patch-1\n\nNew line at end of file.",
"tree": {
"sha": "b4eecafa9be2f2006ce1b709d6857b07069b4608",
"url": "https://api.github.com/repos/octocat/Hello-World/git/trees/b4eecafa9be2f2006ce1b709d6857b07069b4608"
},
"committer": {
"name": "The Octocat",
"date": "2012-03-06T15:06:50-08:00",
"email": "octocat@nowhere.com"
},
"verification": {
"verified": false,
"reason": "unsigned",
"signature": null,
"payload": null,
"verified_at": null
},
"comment_count": 0
},
"author": {
"gravatar_id": "",
"avatar_url": "https://secure.gravatar.com/avatar/7ad39074b0584bc555d0417ae3e7d974?d=https://a248.e.akamai.net/assets.github.com%2Fimages%2Fgravatars%2Fgravatar-140.png",
"url": "https://api.github.com/users/octocat",
"id": 583231,
"login": "octocat",
"node_id": "MDQ6VXNlcjE=",
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
"site_admin": true
},
"parents": [
{
"sha": "553c2077f0edc3d5dc5d17262f6aa498e69d6f8e",
"url": "https://api.github.com/repos/octocat/Hello-World/commits/553c2077f0edc3d5dc5d17262f6aa498e69d6f8e"
},
{
"sha": "762941318ee16e59dabbacb1b4049eec22f0d303",
"url": "https://api.github.com/repos/octocat/Hello-World/commits/762941318ee16e59dabbacb1b4049eec22f0d303"
}
],
"url": "https://api.github.com/repos/octocat/Hello-World/commits/7fd1a60b01f91b314f59955a4e4d4e80d8edf11d",
"committer": {
"gravatar_id": "",
"avatar_url": "https://secure.gravatar.com/avatar/7ad39074b0584bc555d0417ae3e7d974?d=https://a248.e.akamai.net/assets.github.com%2Fimages%2Fgravatars%2Fgravatar-140.png",
"url": "https://api.github.com/users/octocat",
"id": 583231,
"login": "octocat",
"node_id": "MDQ6VXNlcjE=",
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
"site_admin": true
},
"html_url": "https://github.com/octocat/Hello-World/commit/6dcb09b5b57875f334f61aebed695e2e4193db5e",
"comments_url": "https://api.github.com/repos/octocat/Hello-World/commits/6dcb09b5b57875f334f61aebed695e2e4193db5e/comments"
},
"_links": {
"html": "https://github.com/octocat/Hello-World/tree/master",
"self": "https://api.github.com/repos/octocat/Hello-World/branches/master"
},
"protected": true,
"protection": {
"required_status_checks": {
"enforcement_level": "non_admins",
"contexts": [
"ci-test",
"linter"
]
}
},
"protection_url": "https://api.github.com/repos/octocat/hello-world/branches/master/protection"
}`

## Sync a fork branch with the upstream repository

Sync a branch of a forked repository to keep it up-to-date with the upstream repository.

### Fine-grained access tokens for "Sync a fork branch with the upstream repository"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Contents" repository permissions (write)

### Parameters for "Sync a fork branch with the upstream repository"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| branchstringRequiredThe name of the branch which should be updated to match upstream. |

### HTTP response status codes for "Sync a fork branch with the upstream repository"

| Status code | Description |
| --- | --- |
| 200 | The branch has been successfully synced with the upstream repository |
| 409 | The branch could not be synced because of a merge conflict |
| 422 | The branch could not be synced for some other reason |

### Code samples for "Sync a fork branch with the upstream repository"

#### Request example

post/repos/{owner}/{repo}/merge-upstream

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/merge-upstream \
  -d '{"branch":"main"}'`

The branch has been successfully synced with the upstream repository

-
-

`Status: 200``{
"message": "Successfully fetched and fast-forwarded from upstream defunkt:main",
"merge_type": "fast-forward",
"base_branch": "defunkt:main"
}`

## Merge a branch

### Fine-grained access tokens for "Merge a branch"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Contents" repository permissions (write)

### Parameters for "Merge a branch"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| basestringRequiredThe name of the base branch that the head will be merged into. |
| headstringRequiredThe head to merge. This can be a branch name or a commit SHA1. |
| commit_messagestringCommit message to use for the merge commit. If omitted, a default message will be used. |

### HTTP response status codes for "Merge a branch"

| Status code | Description |
| --- | --- |
| 201 | Successful Response (The resulting merge commit) |
| 204 | Response when already merged |
| 403 | Forbidden |
| 404 | Not Found when the base or head does not exist |
| 409 | Conflict when there is a merge conflict |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Merge a branch"

#### Request example

post/repos/{owner}/{repo}/merges

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/merges \
  -d '{"base":"master","head":"cool_feature","commit_message":"Shipped cool_feature!"}'`

Successful Response (The resulting merge commit)

-
-

`Status: 201``{
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
