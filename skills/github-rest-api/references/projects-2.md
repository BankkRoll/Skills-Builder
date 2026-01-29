# REST API endpoints for Project items

# REST API endpoints for Project items

> Use the REST API to manage Project items

## List items for an organization owned project

List all items for a specific organization-owned project accessible by the authenticated user.

### Fine-grained access tokens for "List items for an organization owned project"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Projects" organization permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "List items for an organization owned project"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| project_numberintegerRequiredThe project's number. |
| orgstringRequiredThe organization name. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| qstringSearch query to filter items, seeFiltering projectsfor more information. |
| fieldsLimit results to specific fields, by their IDs. If not specified, the title field will be returned.Example:fields[]=123&fields[]=456&fields[]=789orfields=123,456,789 |
| beforestringA cursor, as given in theLink header. If specified, the query only searches for results before this cursor. For more information, see "Using pagination in the REST API." |
| afterstringA cursor, as given in theLink header. If specified, the query only searches for results after this cursor. For more information, see "Using pagination in the REST API." |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |

### HTTP response status codes for "List items for an organization owned project"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 304 | Not modified |
| 401 | Requires authentication |
| 403 | Forbidden |

### Code samples for "List items for an organization owned project"

#### Request example

get/orgs/{org}/projectsV2/{project_number}/items

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/projectsV2/PROJECT_NUMBER/items`

Response

-
-

`Status: 200``{
"id": 13,
"node_id": "PVTI_lAAFAQ0",
"project_url": "https://api.github.com/orgs/github/projectsV2/1",
"content": {
"url": "https://api.github.com/repos/github/Hello-World/pulls/6",
"id": 10,
"node_id": "PR_kwABCg",
"html_url": "https://github.com/github/Hello-World/pull/6",
"diff_url": "https://github.com/github/Hello-World/pull/6.diff",
"patch_url": "https://github.com/github/Hello-World/pull/6.patch",
"issue_url": "https://api.github.com/repos/github/Hello-World/issues/6",
"number": 6,
"state": "open",
"locked": false,
"title": "Issue title",
"user": {
"login": "monalisa",
"id": 161,
"node_id": "U_kgDMoQ",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/monalisa",
"html_url": "https://github.com/monalisa",
"followers_url": "https://api.github.com/users/monalisa/followers",
"following_url": "https://api.github.com/users/monalisa/following{/other_user}",
"gists_url": "https://api.github.com/users/monalisa/gists{/gist_id}",
"starred_url": "https://api.github.com/users/monalisa/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/monalisa/subscriptions",
"organizations_url": "https://api.github.com/users/monalisa/orgs",
"repos_url": "https://api.github.com/users/monalisa/repos",
"events_url": "https://api.github.com/users/monalisa/events{/privacy}",
"received_events_url": "https://api.github.com/users/monalisa/received_events",
"type": "User",
"user_view_type": "public",
"site_admin": false
},
"body": "Issue body",
"created_at": "2025-08-01T18:44:50Z",
"updated_at": "2025-08-06T19:25:18Z",
"closed_at": null,
"merged_at": null,
"merge_commit_sha": "98e25bad5878e54d22e5338cbc905dd2deedfa34",
"assignee": {
"login": "octocat",
"id": 175,
"node_id": "U_kgDMrw",
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
"user_view_type": "public",
"site_admin": false
},
"assignees": [
{
"login": "octocat",
"id": 175,
"node_id": "U_kgDMrw",
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
"user_view_type": "public",
"site_admin": false
}
],
"requested_reviewers": [
{
"login": "monalisa",
"id": 2,
"node_id": "U_kgAC",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/monalisa",
"html_url": "https://github.com/monalisa",
"followers_url": "https://api.github.com/users/monalisa/followers",
"following_url": "https://api.github.com/users/monalisa/following{/other_user}",
"gists_url": "https://api.github.com/users/monalisa/gists{/gist_id}",
"starred_url": "https://api.github.com/users/monalisa/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/monalisa/subscriptions",
"organizations_url": "https://api.github.com/users/monalisa/orgs",
"repos_url": "https://api.github.com/users/monalisa/repos",
"events_url": "https://api.github.com/users/monalisa/events{/privacy}",
"received_events_url": "https://api.github.com/users/monalisa/received_events",
"type": "User",
"user_view_type": "public",
"site_admin": false
}
],
"requested_teams": [],
"labels": [
{
"id": 19,
"node_id": "LA_kwABEw",
"url": "https://api.github.com/repos/github/Hello-World/labels/bug%20:bug:",
"name": "bug :bug:",
"color": "efe24f",
"default": false,
"description": "Something isn't working"
},
{
"id": 26,
"node_id": "LA_kwABGg",
"url": "https://api.github.com/repos/github/Hello-World/labels/fun%20size%20%F0%9F%8D%AB",
"name": "fun size 🍫",
"color": "f29c24",
"default": false,
"description": "Extra attention is needed"
},
{
"id": 33,
"node_id": "LA_kwABIQ",
"url": "https://api.github.com/repos/github/Hello-World/labels/%F0%9F%9A%92%20wontfix",
"name": "🚒 wontfix",
"color": "5891ce",
"default": false,
"description": "This will not be worked on"
}
],
"milestone": {
"url": "https://api.github.com/repos/github/Hello-World/milestones/1",
"html_url": "https://github.com/github/Hello-World/milestone/1",
"labels_url": "https://api.github.com/repos/github/Hello-World/milestones/1/labels",
"id": 1,
"node_id": "MI_kwABAQ",
"number": 1,
"title": "Open milestone",
"description": null,
"creator": {
"login": "monalisa",
"id": 2,
"node_id": "U_kgAC",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/monalisa",
"html_url": "https://github.com/monalisa",
"followers_url": "https://api.github.com/users/monalisa/followers",
"following_url": "https://api.github.com/users/monalisa/following{/other_user}",
"gists_url": "https://api.github.com/users/monalisa/gists{/gist_id}",
"starred_url": "https://api.github.com/users/monalisa/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/monalisa/subscriptions",
"organizations_url": "https://api.github.com/users/monalisa/orgs",
"repos_url": "https://api.github.com/users/monalisa/repos",
"events_url": "https://api.github.com/users/monalisa/events{/privacy}",
"received_events_url": "https://api.github.com/users/monalisa/received_events",
"type": "User",
"user_view_type": "public",
"site_admin": false
},
"open_issues": 2,
"closed_issues": 1,
"state": "open",
"created_at": "2025-08-01T18:44:30Z",
"updated_at": "2025-08-06T19:14:15Z",
"due_on": null,
"closed_at": null
},
"draft": false,
"commits_url": "https://api.github.com/repos/github/Hello-World/pulls/6/commits",
"review_comments_url": "https://api.github.com/repos/github/Hello-World/pulls/6/comments",
"review_comment_url": "https://api.github.com/repos/github/Hello-World/pulls/comments{/number}",
"comments_url": "https://api.github.com/repos/github/Hello-World/issues/6/comments",
"statuses_url": "https://api.github.com/repos/github/Hello-World/statuses/a3258d3434ecb2058b2784c8eb8610c2e9937a0d",
"head": {
"label": "github:branch-2ee3da8fde8a1adfe6d0809a1a414e4f",
"ref": "branch-2ee3da8fde8a1adfe6d0809a1a414e4f",
"sha": "a3258d3434ecb2058b2784c8eb8610c2e9937a0d",
"user": {
"login": "github",
"id": 5,
"node_id": "O_kgAF",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/github",
"html_url": "https://github.com/github",
"followers_url": "https://api.github.com/users/github/followers",
"following_url": "https://api.github.com/users/github/following{/other_user}",
"gists_url": "https://api.github.com/users/github/gists{/gist_id}",
"starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/github/subscriptions",
"organizations_url": "https://api.github.com/users/github/orgs",
"repos_url": "https://api.github.com/users/github/repos",
"events_url": "https://api.github.com/users/github/events{/privacy}",
"received_events_url": "https://api.github.com/users/github/received_events",
"type": "Organization",
"user_view_type": "public",
"site_admin": false
},
"repo": {
"id": 1,
"node_id": "R_kgAB",
"name": "Hello-World",
"full_name": "github/Hello-World",
"private": false,
"owner": {
"login": "github",
"id": 5,
"node_id": "O_kgAF",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/github",
"html_url": "https://github.com/github",
"followers_url": "https://api.github.com/users/github/followers",
"following_url": "https://api.github.com/users/github/following{/other_user}",
"gists_url": "https://api.github.com/users/github/gists{/gist_id}",
"starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/github/subscriptions",
"organizations_url": "https://api.github.com/users/github/orgs",
"repos_url": "https://api.github.com/users/github/repos",
"events_url": "https://api.github.com/users/github/events{/privacy}",
"received_events_url": "https://api.github.com/users/github/received_events",
"type": "Organization",
"user_view_type": "public",
"site_admin": false
},
"html_url": "https://github.com/github/Hello-World",
"description": null,
"fork": false,
"url": "https://api.github.com/repos/github/Hello-World",
"forks_url": "https://api.github.com/repos/github/Hello-World/forks",
"keys_url": "https://api.github.com/repos/github/Hello-World/keys{/key_id}",
"collaborators_url": "https://api.github.com/repos/github/Hello-World/collaborators{/collaborator}",
"teams_url": "https://api.github.com/repos/github/Hello-World/teams",
"hooks_url": "https://api.github.com/repos/github/Hello-World/hooks",
"issue_events_url": "https://api.github.com/repos/github/Hello-World/issues/events{/number}",
"events_url": "https://api.github.com/repos/github/Hello-World/events",
"assignees_url": "https://api.github.com/repos/github/Hello-World/assignees{/user}",
"branches_url": "https://api.github.com/repos/github/Hello-World/branches{/branch}",
"tags_url": "https://api.github.com/repos/github/Hello-World/tags",
"blobs_url": "https://api.github.com/repos/github/Hello-World/git/blobs{/sha}",
"git_tags_url": "https://api.github.com/repos/github/Hello-World/git/tags{/sha}",
"git_refs_url": "https://api.github.com/repos/github/Hello-World/git/refs{/sha}",
"trees_url": "https://api.github.com/repos/github/Hello-World/git/trees{/sha}",
"statuses_url": "https://api.github.com/repos/github/Hello-World/statuses/{sha}",
"languages_url": "https://api.github.com/repos/github/Hello-World/languages",
"stargazers_url": "https://api.github.com/repos/github/Hello-World/stargazers",
"contributors_url": "https://api.github.com/repos/github/Hello-World/contributors",
"subscribers_url": "https://api.github.com/repos/github/Hello-World/subscribers",
"subscription_url": "https://api.github.com/repos/github/Hello-World/subscription",
"commits_url": "https://api.github.com/repos/github/Hello-World/commits{/sha}",
"git_commits_url": "https://api.github.com/repos/github/Hello-World/git/commits{/sha}",
"comments_url": "https://api.github.com/repos/github/Hello-World/comments{/number}",
"issue_comment_url": "https://api.github.com/repos/github/Hello-World/issues/comments{/number}",
"contents_url": "https://api.github.com/repos/github/Hello-World/contents/{+path}",
"compare_url": "https://api.github.com/repos/github/Hello-World/compare/{base}...{head}",
"merges_url": "https://api.github.com/repos/github/Hello-World/merges",
"archive_url": "https://api.github.com/repos/github/Hello-World/{archive_format}{/ref}",
"downloads_url": "https://api.github.com/repos/github/Hello-World/downloads",
"issues_url": "https://api.github.com/repos/github/Hello-World/issues{/number}",
"pulls_url": "https://api.github.com/repos/github/Hello-World/pulls{/number}",
"milestones_url": "https://api.github.com/repos/github/Hello-World/milestones{/number}",
"notifications_url": "https://api.github.com/repos/github/Hello-World/notifications{?since,all,participating}",
"labels_url": "https://api.github.com/repos/github/Hello-World/labels{/name}",
"releases_url": "https://api.github.com/repos/github/Hello-World/releases{/id}",
"deployments_url": "https://api.github.com/repos/github/Hello-World/deployments",
"created_at": "2025-08-01T18:44:14Z",
"updated_at": "2025-08-01T18:48:38Z",
"pushed_at": "2025-08-01T18:44:50Z",
"git_url": "git://github.localhost/github/Hello-World.git",
"ssh_url": "ssh://git@localhost:3035/github/Hello-World.git",
"clone_url": "https://github.com/github/Hello-World.git",
"svn_url": "https://github.com/github/Hello-World",
"homepage": null,
"size": 6,
"stargazers_count": 0,
"watchers_count": 0,
"language": null,
"has_issues": true,
"has_projects": true,
"has_downloads": true,
"has_wiki": true,
"has_pages": false,
"has_discussions": false,
"forks_count": 0,
"mirror_url": null,
"archived": false,
"disabled": false,
"open_issues_count": 3,
"license": null,
"allow_forking": true,
"is_template": false,
"web_commit_signoff_required": false,
"topics": [],
"visibility": "public",
"forks": 0,
"open_issues": 3,
"watchers": 0,
"default_branch": "main"
}
},
"base": {
"label": "github:branch-0f4ceb14cbe39e4786ffbabb776da599",
"ref": "branch-0f4ceb14cbe39e4786ffbabb776da599",
"sha": "9a9f5a8d77bdc2540412900d3c930fe36a82b5ed",
"user": {
"login": "github",
"id": 5,
"node_id": "O_kgAF",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/github",
"html_url": "https://github.com/github",
"followers_url": "https://api.github.com/users/github/followers",
"following_url": "https://api.github.com/users/github/following{/other_user}",
"gists_url": "https://api.github.com/users/github/gists{/gist_id}",
"starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/github/subscriptions",
"organizations_url": "https://api.github.com/users/github/orgs",
"repos_url": "https://api.github.com/users/github/repos",
"events_url": "https://api.github.com/users/github/events{/privacy}",
"received_events_url": "https://api.github.com/users/github/received_events",
"type": "Organization",
"user_view_type": "public",
"site_admin": false
},
"repo": {
"id": 1,
"node_id": "R_kgAB",
"name": "Hello-World",
"full_name": "github/Hello-World",
"private": false,
"owner": {
"login": "github",
"id": 5,
"node_id": "O_kgAF",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/github",
"html_url": "https://github.com/github",
"followers_url": "https://api.github.com/users/github/followers",
"following_url": "https://api.github.com/users/github/following{/other_user}",
"gists_url": "https://api.github.com/users/github/gists{/gist_id}",
"starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/github/subscriptions",
"organizations_url": "https://api.github.com/users/github/orgs",
"repos_url": "https://api.github.com/users/github/repos",
"events_url": "https://api.github.com/users/github/events{/privacy}",
"received_events_url": "https://api.github.com/users/github/received_events",
"type": "Organization",
"user_view_type": "public",
"site_admin": false
},
"html_url": "https://github.com/github/Hello-World",
"description": null,
"fork": false,
"url": "https://api.github.com/repos/github/Hello-World",
"forks_url": "https://api.github.com/repos/github/Hello-World/forks",
"keys_url": "https://api.github.com/repos/github/Hello-World/keys{/key_id}",
"collaborators_url": "https://api.github.com/repos/github/Hello-World/collaborators{/collaborator}",
"teams_url": "https://api.github.com/repos/github/Hello-World/teams",
"hooks_url": "https://api.github.com/repos/github/Hello-World/hooks",
"issue_events_url": "https://api.github.com/repos/github/Hello-World/issues/events{/number}",
"events_url": "https://api.github.com/repos/github/Hello-World/events",
"assignees_url": "https://api.github.com/repos/github/Hello-World/assignees{/user}",
"branches_url": "https://api.github.com/repos/github/Hello-World/branches{/branch}",
"tags_url": "https://api.github.com/repos/github/Hello-World/tags",
"blobs_url": "https://api.github.com/repos/github/Hello-World/git/blobs{/sha}",
"git_tags_url": "https://api.github.com/repos/github/Hello-World/git/tags{/sha}",
"git_refs_url": "https://api.github.com/repos/github/Hello-World/git/refs{/sha}",
"trees_url": "https://api.github.com/repos/github/Hello-World/git/trees{/sha}",
"statuses_url": "https://api.github.com/repos/github/Hello-World/statuses/{sha}",
"languages_url": "https://api.github.com/repos/github/Hello-World/languages",
"stargazers_url": "https://api.github.com/repos/github/Hello-World/stargazers",
"contributors_url": "https://api.github.com/repos/github/Hello-World/contributors",
"subscribers_url": "https://api.github.com/repos/github/Hello-World/subscribers",
"subscription_url": "https://api.github.com/repos/github/Hello-World/subscription",
"commits_url": "https://api.github.com/repos/github/Hello-World/commits{/sha}",
"git_commits_url": "https://api.github.com/repos/github/Hello-World/git/commits{/sha}",
"comments_url": "https://api.github.com/repos/github/Hello-World/comments{/number}",
"issue_comment_url": "https://api.github.com/repos/github/Hello-World/issues/comments{/number}",
"contents_url": "https://api.github.com/repos/github/Hello-World/contents/{+path}",
"compare_url": "https://api.github.com/repos/github/Hello-World/compare/{base}...{head}",
"merges_url": "https://api.github.com/repos/github/Hello-World/merges",
"archive_url": "https://api.github.com/repos/github/Hello-World/{archive_format}{/ref}",
"downloads_url": "https://api.github.com/repos/github/Hello-World/downloads",
"issues_url": "https://api.github.com/repos/github/Hello-World/issues{/number}",
"pulls_url": "https://api.github.com/repos/github/Hello-World/pulls{/number}",
"milestones_url": "https://api.github.com/repos/github/Hello-World/milestones{/number}",
"notifications_url": "https://api.github.com/repos/github/Hello-World/notifications{?since,all,participating}",
"labels_url": "https://api.github.com/repos/github/Hello-World/labels{/name}",
"releases_url": "https://api.github.com/repos/github/Hello-World/releases{/id}",
"deployments_url": "https://api.github.com/repos/github/Hello-World/deployments",
"created_at": "2025-08-01T18:44:14Z",
"updated_at": "2025-08-01T18:48:38Z",
"pushed_at": "2025-08-01T18:44:50Z",
"git_url": "git://github.localhost/github/Hello-World.git",
"ssh_url": "ssh://git@localhost:3035/github/Hello-World.git",
"clone_url": "https://github.com/github/Hello-World.git",
"svn_url": "https://github.com/github/Hello-World",
"homepage": null,
"size": 6,
"stargazers_count": 0,
"watchers_count": 0,
"language": null,
"has_issues": true,
"has_projects": true,
"has_downloads": true,
"has_wiki": true,
"has_pages": false,
"has_discussions": false,
"forks_count": 0,
"mirror_url": null,
"archived": false,
"disabled": false,
"open_issues_count": 3,
"license": null,
"allow_forking": true,
"is_template": false,
"web_commit_signoff_required": false,
"topics": [],
"visibility": "public",
"forks": 0,
"open_issues": 3,
"watchers": 0,
"default_branch": "main"
}
},
"_links": {
"self": {
"href": "https://api.github.com/repos/github/Hello-World/pulls/6"
},
"html": {
"href": "https://github.com/github/Hello-World/pull/6"
},
"issue": {
"href": "https://api.github.com/repos/github/Hello-World/issues/6"
},
"comments": {
"href": "https://api.github.com/repos/github/Hello-World/issues/6/comments"
},
"review_comments": {
"href": "https://api.github.com/repos/github/Hello-World/pulls/6/comments"
},
"review_comment": {
"href": "https://api.github.com/repos/github/Hello-World/pulls/comments{/number}"
},
"commits": {
"href": "https://api.github.com/repos/github/Hello-World/pulls/6/commits"
},
"statuses": {
"href": "https://api.github.com/repos/github/Hello-World/statuses/a3258d3434ecb2058b2784c8eb8610c2e9937a0d"
}
},
"author_association": "MEMBER",
"auto_merge": null,
"active_lock_reason": null
},
"content_type": "PullRequest",
"creator": {
"login": "monalisa",
"id": 2,
"node_id": "U_kgAC",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/monalisa",
"html_url": "https://github.com/monalisa",
"followers_url": "https://api.github.com/users/monalisa/followers",
"following_url": "https://api.github.com/users/monalisa/following{/other_user}",
"gists_url": "https://api.github.com/users/monalisa/gists{/gist_id}",
"starred_url": "https://api.github.com/users/monalisa/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/monalisa/subscriptions",
"organizations_url": "https://api.github.com/users/monalisa/orgs",
"repos_url": "https://api.github.com/users/monalisa/repos",
"events_url": "https://api.github.com/users/monalisa/events{/privacy}",
"received_events_url": "https://api.github.com/users/monalisa/received_events",
"type": "User",
"user_view_type": "public",
"site_admin": false
},
"created_at": "2025-08-01T18:44:51Z",
"updated_at": "2025-08-06T19:25:18Z",
"archived_at": null,
"item_url": "https://api.github.com/orgs/github/projectsV2/1/items/13",
"fields": [
{
"id": 1,
"name": "Title",
"type": "title",
"value": {
"raw": "It seemed to me that any civilization that had so far lost its head as to need to include a set of detailed instructions for use in a packet of toothpicks, was no longer a civilization in which I could live and stay sane.",
"html": "It seemed to me that any civilization that had so far lost its head as to need to include a set of detailed instructions for use in a packet of toothpicks, was no longer a civilization in which I could live and stay sane.",
"number": 6,
"url": "https://github.com/5/1/pull/6",
"issue_id": 12,
"state": "open",
"state_reason": null,
"is_draft": false
}
},
{
"id": 2,
"name": "Assignees",
"type": "assignees",
"value": [
{
"login": "octocat",
"id": 175,
"node_id": "U_kgDMrw",
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
"user_view_type": "public",
"site_admin": false
}
]
},
{
"id": 3,
"name": "Status",
"type": "single_select",
"value": {
"id": "98236657",
"name": {
"raw": "Done",
"html": "Done"
},
"color": "PURPLE",
"description": {
"raw": "This has been completed",
"html": "This has been completed"
}
}
},
{
"id": 4,
"name": "Labels",
"type": "labels",
"value": [
{
"id": 19,
"node_id": "LA_kwABEw",
"url": "https://api.github.com/repos/github/Hello-World/labels/bug%20:bug:",
"name": "bug :bug:",
"color": "efe24f",
"default": false,
"description": "Something isn't working"
},
{
"id": 26,
"node_id": "LA_kwABGg",
"url": "https://api.github.com/repos/github/Hello-World/labels/fun%20size%20%F0%9F%8D%AB",
"name": "fun size 🍫",
"color": "f29c24",
"default": false,
"description": "Extra attention is needed"
},
{
"id": 33,
"node_id": "LA_kwABIQ",
"url": "https://api.github.com/repos/github/Hello-World/labels/%F0%9F%9A%92%20wontfix",
"name": "🚒 wontfix",
"color": "5891ce",
"default": false,
"description": "This will not be worked on"
}
]
},
{
"id": 5,
"name": "Linked pull requests",
"type": "linked_pull_requests",
"value": []
},
{
"id": 6,
"name": "Milestone",
"type": "milestone",
"value": {
"url": "https://api.github.com/repos/github/Hello-World/milestones/1",
"html_url": "https://github.com/github/Hello-World/milestone/1",
"labels_url": "https://api.github.com/repos/github/Hello-World/milestones/1/labels",
"id": 1,
"node_id": "MI_kwABAQ",
"number": 1,
"title": "Open milestone",
"description": null,
"creator": {
"login": "octocat",
"id": 175,
"node_id": "U_kgDMrw",
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
"user_view_type": "public",
"site_admin": false
},
"open_issues": 2,
"closed_issues": 1,
"state": "open",
"created_at": "2025-08-01T18:44:30Z",
"updated_at": "2025-08-06T19:14:15Z",
"due_on": null,
"closed_at": null
}
},
{
"id": 7,
"name": "Repository",
"type": "repository",
"value": {
"id": 1,
"node_id": "R_kgAB",
"name": "Hello-World",
"full_name": "github/Hello-World",
"private": false,
"owner": {
"login": "github",
"id": 5,
"node_id": "O_kgAF",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/github",
"html_url": "https://github.com/github",
"followers_url": "https://api.github.com/users/github/followers",
"following_url": "https://api.github.com/users/github/following{/other_user}",
"gists_url": "https://api.github.com/users/github/gists{/gist_id}",
"starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/github/subscriptions",
"organizations_url": "https://api.github.com/users/github/orgs",
"repos_url": "https://api.github.com/users/github/repos",
"events_url": "https://api.github.com/users/github/events{/privacy}",
"received_events_url": "https://api.github.com/users/github/received_events",
"type": "Organization",
"user_view_type": "public",
"site_admin": false
},
"html_url": "https://github.com/github/Hello-World",
"description": null,
"fork": false,
"url": "https://api.github.com/repos/github/Hello-World",
"forks_url": "https://api.github.com/repos/github/Hello-World/forks",
"keys_url": "https://api.github.com/repos/github/Hello-World/keys{/key_id}",
"collaborators_url": "https://api.github.com/repos/github/Hello-World/collaborators{/collaborator}",
"teams_url": "https://api.github.com/repos/github/Hello-World/teams",
"hooks_url": "https://api.github.com/repos/github/Hello-World/hooks",
"issue_events_url": "https://api.github.com/repos/github/Hello-World/issues/events{/number}",
"events_url": "https://api.github.com/repos/github/Hello-World/events",
"assignees_url": "https://api.github.com/repos/github/Hello-World/assignees{/user}",
"branches_url": "https://api.github.com/repos/github/Hello-World/branches{/branch}",
"tags_url": "https://api.github.com/repos/github/Hello-World/tags",
"blobs_url": "https://api.github.com/repos/github/Hello-World/git/blobs{/sha}",
"git_tags_url": "https://api.github.com/repos/github/Hello-World/git/tags{/sha}",
"git_refs_url": "https://api.github.com/repos/github/Hello-World/git/refs{/sha}",
"trees_url": "https://api.github.com/repos/github/Hello-World/git/trees{/sha}",
"statuses_url": "https://api.github.com/repos/github/Hello-World/statuses/{sha}",
"languages_url": "https://api.github.com/repos/github/Hello-World/languages",
"stargazers_url": "https://api.github.com/repos/github/Hello-World/stargazers",
"contributors_url": "https://api.github.com/repos/github/Hello-World/contributors",
"subscribers_url": "https://api.github.com/repos/github/Hello-World/subscribers",
"subscription_url": "https://api.github.com/repos/github/Hello-World/subscription",
"commits_url": "https://api.github.com/repos/github/Hello-World/commits{/sha}",
"git_commits_url": "https://api.github.com/repos/github/Hello-World/git/commits{/sha}",
"comments_url": "https://api.github.com/repos/github/Hello-World/comments{/number}",
"issue_comment_url": "https://api.github.com/repos/github/Hello-World/issues/comments{/number}",
"contents_url": "https://api.github.com/repos/github/Hello-World/contents/{+path}",
"compare_url": "https://api.github.com/repos/github/Hello-World/compare/{base}...{head}",
"merges_url": "https://api.github.com/repos/github/Hello-World/merges",
"archive_url": "https://api.github.com/repos/github/Hello-World/{archive_format}{/ref}",
"downloads_url": "https://api.github.com/repos/github/Hello-World/downloads",
"issues_url": "https://api.github.com/repos/github/Hello-World/issues{/number}",
"pulls_url": "https://api.github.com/repos/github/Hello-World/pulls{/number}",
"milestones_url": "https://api.github.com/repos/github/Hello-World/milestones{/number}",
"notifications_url": "https://api.github.com/repos/github/Hello-World/notifications{?since,all,participating}",
"labels_url": "https://api.github.com/repos/github/Hello-World/labels{/name}",
"releases_url": "https://api.github.com/repos/github/Hello-World/releases{/id}",
"deployments_url": "https://api.github.com/repos/github/Hello-World/deployments"
}
},
{
"id": 8,
"name": "Type",
"type": "issue_type",
"value": null
},
{
"id": 9,
"name": "Reviewers",
"type": "reviewers",
"value": [
{
"type": "ReviewRequest",
"status": "pending",
"reviewer": {
"avatarUrl": "https://github.com/images/error/octocat_happy.gif",
"id": 2,
"login": "monalisa",
"url": "https://github.com/monalisa",
"name": "monalisa",
"type": "User"
}
}
]
},
{
"id": 10,
"name": "Parent issue",
"type": "parent_issue",
"value": null
},
{
"id": 11,
"name": "Sub-issues progress",
"type": "sub_issues_progress",
"value": null
}
]
}`

## Add item to organization owned project

Add an issue or pull request item to the specified organization owned project.

### Fine-grained access tokens for "Add item to organization owned project"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Projects" organization permissions (write)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "Add item to organization owned project"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| project_numberintegerRequiredThe project's number. |

### HTTP response status codes for "Add item to organization owned project"

| Status code | Description |
| --- | --- |
| 201 | Created |
| 304 | Not modified |
| 401 | Requires authentication |
| 403 | Forbidden |

### Code samples for "Add item to organization owned project"

#### Request examples

Select the example typeAdd an issue using its unique IDAdd a pull request using its unique IDAdd an issue using repository owner, name, and issue numberAdd a pull request using repository owner, name, and PR numberpost/orgs/{org}/projectsV2/{project_number}/items

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/projectsV2/PROJECT_NUMBER/items \
  -d '{"type":"Issue","id":3}'`

Response for adding an issue using its unique ID

-
-

`Status: 201``{
"value": {
"id": 17,
"node_id": "PVTI_lADOANN5s84ACbL0zgBueEI",
"content": {
"id": 38,
"node_id": "I_kwDOANN5s85FtLts",
"title": "Example Draft Issue",
"body": "This is a draft issue in the project.",
"created_at": "2022-04-28T12:00:00Z",
"updated_at": "2022-04-28T12:00:00Z",
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
"content_type": "DraftIssue",
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
"archived_at": null,
"project_url": "https://api.github.com/users/octocat/projectsV2/1",
"item_url": "https://api.github.com/users/octocat/projectsV2/items/17"
}
}`

## Get an item for an organization owned project

Get a specific item from an organization-owned project.

### Fine-grained access tokens for "Get an item for an organization owned project"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Projects" organization permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "Get an item for an organization owned project"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| project_numberintegerRequiredThe project's number. |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| item_idintegerRequiredThe unique identifier of the project item. |

| Name, Type, Description |
| --- |
| fieldsLimit results to specific fields, by their IDs. If not specified, the title field will be returned.Example: fields[]=123&fields[]=456&fields[]=789 or fields=123,456,789 |

### HTTP response status codes for "Get an item for an organization owned project"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 304 | Not modified |
| 401 | Requires authentication |
| 403 | Forbidden |

### Code samples for "Get an item for an organization owned project"

#### Request example

get/orgs/{org}/projectsV2/{project_number}/items/{item_id}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/projectsV2/PROJECT_NUMBER/items/ITEM_ID`

Response

-
-

`Status: 200``{
"id": 13,
"node_id": "PVTI_lAAFAQ0",
"project_url": "https://api.github.com/orgs/github/projectsV2/1",
"content": {
"url": "https://api.github.com/repos/github/Hello-World/pulls/6",
"id": 10,
"node_id": "PR_kwABCg",
"html_url": "https://github.com/github/Hello-World/pull/6",
"diff_url": "https://github.com/github/Hello-World/pull/6.diff",
"patch_url": "https://github.com/github/Hello-World/pull/6.patch",
"issue_url": "https://api.github.com/repos/github/Hello-World/issues/6",
"number": 6,
"state": "open",
"locked": false,
"title": "Issue title",
"user": {
"login": "monalisa",
"id": 161,
"node_id": "U_kgDMoQ",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/monalisa",
"html_url": "https://github.com/monalisa",
"followers_url": "https://api.github.com/users/monalisa/followers",
"following_url": "https://api.github.com/users/monalisa/following{/other_user}",
"gists_url": "https://api.github.com/users/monalisa/gists{/gist_id}",
"starred_url": "https://api.github.com/users/monalisa/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/monalisa/subscriptions",
"organizations_url": "https://api.github.com/users/monalisa/orgs",
"repos_url": "https://api.github.com/users/monalisa/repos",
"events_url": "https://api.github.com/users/monalisa/events{/privacy}",
"received_events_url": "https://api.github.com/users/monalisa/received_events",
"type": "User",
"user_view_type": "public",
"site_admin": false
},
"body": "Issue body",
"created_at": "2025-08-01T18:44:50Z",
"updated_at": "2025-08-06T19:25:18Z",
"closed_at": null,
"merged_at": null,
"merge_commit_sha": "98e25bad5878e54d22e5338cbc905dd2deedfa34",
"assignee": {
"login": "octocat",
"id": 175,
"node_id": "U_kgDMrw",
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
"user_view_type": "public",
"site_admin": false
},
"assignees": [
{
"login": "octocat",
"id": 175,
"node_id": "U_kgDMrw",
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
"user_view_type": "public",
"site_admin": false
}
],
"requested_reviewers": [
{
"login": "monalisa",
"id": 2,
"node_id": "U_kgAC",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/monalisa",
"html_url": "https://github.com/monalisa",
"followers_url": "https://api.github.com/users/monalisa/followers",
"following_url": "https://api.github.com/users/monalisa/following{/other_user}",
"gists_url": "https://api.github.com/users/monalisa/gists{/gist_id}",
"starred_url": "https://api.github.com/users/monalisa/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/monalisa/subscriptions",
"organizations_url": "https://api.github.com/users/monalisa/orgs",
"repos_url": "https://api.github.com/users/monalisa/repos",
"events_url": "https://api.github.com/users/monalisa/events{/privacy}",
"received_events_url": "https://api.github.com/users/monalisa/received_events",
"type": "User",
"user_view_type": "public",
"site_admin": false
}
],
"requested_teams": [],
"labels": [
{
"id": 19,
"node_id": "LA_kwABEw",
"url": "https://api.github.com/repos/github/Hello-World/labels/bug%20:bug:",
"name": "bug :bug:",
"color": "efe24f",
"default": false,
"description": "Something isn't working"
},
{
"id": 26,
"node_id": "LA_kwABGg",
"url": "https://api.github.com/repos/github/Hello-World/labels/fun%20size%20%F0%9F%8D%AB",
"name": "fun size 🍫",
"color": "f29c24",
"default": false,
"description": "Extra attention is needed"
},
{
"id": 33,
"node_id": "LA_kwABIQ",
"url": "https://api.github.com/repos/github/Hello-World/labels/%F0%9F%9A%92%20wontfix",
"name": "🚒 wontfix",
"color": "5891ce",
"default": false,
"description": "This will not be worked on"
}
],
"milestone": {
"url": "https://api.github.com/repos/github/Hello-World/milestones/1",
"html_url": "https://github.com/github/Hello-World/milestone/1",
"labels_url": "https://api.github.com/repos/github/Hello-World/milestones/1/labels",
"id": 1,
"node_id": "MI_kwABAQ",
"number": 1,
"title": "Open milestone",
"description": null,
"creator": {
"login": "monalisa",
"id": 2,
"node_id": "U_kgAC",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/monalisa",
"html_url": "https://github.com/monalisa",
"followers_url": "https://api.github.com/users/monalisa/followers",
"following_url": "https://api.github.com/users/monalisa/following{/other_user}",
"gists_url": "https://api.github.com/users/monalisa/gists{/gist_id}",
"starred_url": "https://api.github.com/users/monalisa/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/monalisa/subscriptions",
"organizations_url": "https://api.github.com/users/monalisa/orgs",
"repos_url": "https://api.github.com/users/monalisa/repos",
"events_url": "https://api.github.com/users/monalisa/events{/privacy}",
"received_events_url": "https://api.github.com/users/monalisa/received_events",
"type": "User",
"user_view_type": "public",
"site_admin": false
},
"open_issues": 2,
"closed_issues": 1,
"state": "open",
"created_at": "2025-08-01T18:44:30Z",
"updated_at": "2025-08-06T19:14:15Z",
"due_on": null,
"closed_at": null
},
"draft": false,
"commits_url": "https://api.github.com/repos/github/Hello-World/pulls/6/commits",
"review_comments_url": "https://api.github.com/repos/github/Hello-World/pulls/6/comments",
"review_comment_url": "https://api.github.com/repos/github/Hello-World/pulls/comments{/number}",
"comments_url": "https://api.github.com/repos/github/Hello-World/issues/6/comments",
"statuses_url": "https://api.github.com/repos/github/Hello-World/statuses/a3258d3434ecb2058b2784c8eb8610c2e9937a0d",
"head": {
"label": "github:branch-2ee3da8fde8a1adfe6d0809a1a414e4f",
"ref": "branch-2ee3da8fde8a1adfe6d0809a1a414e4f",
"sha": "a3258d3434ecb2058b2784c8eb8610c2e9937a0d",
"user": {
"login": "github",
"id": 5,
"node_id": "O_kgAF",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/github",
"html_url": "https://github.com/github",
"followers_url": "https://api.github.com/users/github/followers",
"following_url": "https://api.github.com/users/github/following{/other_user}",
"gists_url": "https://api.github.com/users/github/gists{/gist_id}",
"starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/github/subscriptions",
"organizations_url": "https://api.github.com/users/github/orgs",
"repos_url": "https://api.github.com/users/github/repos",
"events_url": "https://api.github.com/users/github/events{/privacy}",
"received_events_url": "https://api.github.com/users/github/received_events",
"type": "Organization",
"user_view_type": "public",
"site_admin": false
},
"repo": {
"id": 1,
"node_id": "R_kgAB",
"name": "Hello-World",
"full_name": "github/Hello-World",
"private": false,
"owner": {
"login": "github",
"id": 5,
"node_id": "O_kgAF",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/github",
"html_url": "https://github.com/github",
"followers_url": "https://api.github.com/users/github/followers",
"following_url": "https://api.github.com/users/github/following{/other_user}",
"gists_url": "https://api.github.com/users/github/gists{/gist_id}",
"starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/github/subscriptions",
"organizations_url": "https://api.github.com/users/github/orgs",
"repos_url": "https://api.github.com/users/github/repos",
"events_url": "https://api.github.com/users/github/events{/privacy}",
"received_events_url": "https://api.github.com/users/github/received_events",
"type": "Organization",
"user_view_type": "public",
"site_admin": false
},
"html_url": "https://github.com/github/Hello-World",
"description": null,
"fork": false,
"url": "https://api.github.com/repos/github/Hello-World",
"forks_url": "https://api.github.com/repos/github/Hello-World/forks",
"keys_url": "https://api.github.com/repos/github/Hello-World/keys{/key_id}",
"collaborators_url": "https://api.github.com/repos/github/Hello-World/collaborators{/collaborator}",
"teams_url": "https://api.github.com/repos/github/Hello-World/teams",
"hooks_url": "https://api.github.com/repos/github/Hello-World/hooks",
"issue_events_url": "https://api.github.com/repos/github/Hello-World/issues/events{/number}",
"events_url": "https://api.github.com/repos/github/Hello-World/events",
"assignees_url": "https://api.github.com/repos/github/Hello-World/assignees{/user}",
"branches_url": "https://api.github.com/repos/github/Hello-World/branches{/branch}",
"tags_url": "https://api.github.com/repos/github/Hello-World/tags",
"blobs_url": "https://api.github.com/repos/github/Hello-World/git/blobs{/sha}",
"git_tags_url": "https://api.github.com/repos/github/Hello-World/git/tags{/sha}",
"git_refs_url": "https://api.github.com/repos/github/Hello-World/git/refs{/sha}",
"trees_url": "https://api.github.com/repos/github/Hello-World/git/trees{/sha}",
"statuses_url": "https://api.github.com/repos/github/Hello-World/statuses/{sha}",
"languages_url": "https://api.github.com/repos/github/Hello-World/languages",
"stargazers_url": "https://api.github.com/repos/github/Hello-World/stargazers",
"contributors_url": "https://api.github.com/repos/github/Hello-World/contributors",
"subscribers_url": "https://api.github.com/repos/github/Hello-World/subscribers",
"subscription_url": "https://api.github.com/repos/github/Hello-World/subscription",
"commits_url": "https://api.github.com/repos/github/Hello-World/commits{/sha}",
"git_commits_url": "https://api.github.com/repos/github/Hello-World/git/commits{/sha}",
"comments_url": "https://api.github.com/repos/github/Hello-World/comments{/number}",
"issue_comment_url": "https://api.github.com/repos/github/Hello-World/issues/comments{/number}",
"contents_url": "https://api.github.com/repos/github/Hello-World/contents/{+path}",
"compare_url": "https://api.github.com/repos/github/Hello-World/compare/{base}...{head}",
"merges_url": "https://api.github.com/repos/github/Hello-World/merges",
"archive_url": "https://api.github.com/repos/github/Hello-World/{archive_format}{/ref}",
"downloads_url": "https://api.github.com/repos/github/Hello-World/downloads",
"issues_url": "https://api.github.com/repos/github/Hello-World/issues{/number}",
"pulls_url": "https://api.github.com/repos/github/Hello-World/pulls{/number}",
"milestones_url": "https://api.github.com/repos/github/Hello-World/milestones{/number}",
"notifications_url": "https://api.github.com/repos/github/Hello-World/notifications{?since,all,participating}",
"labels_url": "https://api.github.com/repos/github/Hello-World/labels{/name}",
"releases_url": "https://api.github.com/repos/github/Hello-World/releases{/id}",
"deployments_url": "https://api.github.com/repos/github/Hello-World/deployments",
"created_at": "2025-08-01T18:44:14Z",
"updated_at": "2025-08-01T18:48:38Z",
"pushed_at": "2025-08-01T18:44:50Z",
"git_url": "git://github.localhost/github/Hello-World.git",
"ssh_url": "ssh://git@localhost:3035/github/Hello-World.git",
"clone_url": "https://github.com/github/Hello-World.git",
"svn_url": "https://github.com/github/Hello-World",
"homepage": null,
"size": 6,
"stargazers_count": 0,
"watchers_count": 0,
"language": null,
"has_issues": true,
"has_projects": true,
"has_downloads": true,
"has_wiki": true,
"has_pages": false,
"has_discussions": false,
"forks_count": 0,
"mirror_url": null,
"archived": false,
"disabled": false,
"open_issues_count": 3,
"license": null,
"allow_forking": true,
"is_template": false,
"web_commit_signoff_required": false,
"topics": [],
"visibility": "public",
"forks": 0,
"open_issues": 3,
"watchers": 0,
"default_branch": "main"
}
},
"base": {
"label": "github:branch-0f4ceb14cbe39e4786ffbabb776da599",
"ref": "branch-0f4ceb14cbe39e4786ffbabb776da599",
"sha": "9a9f5a8d77bdc2540412900d3c930fe36a82b5ed",
"user": {
"login": "github",
"id": 5,
"node_id": "O_kgAF",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/github",
"html_url": "https://github.com/github",
"followers_url": "https://api.github.com/users/github/followers",
"following_url": "https://api.github.com/users/github/following{/other_user}",
"gists_url": "https://api.github.com/users/github/gists{/gist_id}",
"starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/github/subscriptions",
"organizations_url": "https://api.github.com/users/github/orgs",
"repos_url": "https://api.github.com/users/github/repos",
"events_url": "https://api.github.com/users/github/events{/privacy}",
"received_events_url": "https://api.github.com/users/github/received_events",
"type": "Organization",
"user_view_type": "public",
"site_admin": false
},
"repo": {
"id": 1,
"node_id": "R_kgAB",
"name": "Hello-World",
"full_name": "github/Hello-World",
"private": false,
"owner": {
"login": "github",
"id": 5,
"node_id": "O_kgAF",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/github",
"html_url": "https://github.com/github",
"followers_url": "https://api.github.com/users/github/followers",
"following_url": "https://api.github.com/users/github/following{/other_user}",
"gists_url": "https://api.github.com/users/github/gists{/gist_id}",
"starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/github/subscriptions",
"organizations_url": "https://api.github.com/users/github/orgs",
"repos_url": "https://api.github.com/users/github/repos",
"events_url": "https://api.github.com/users/github/events{/privacy}",
"received_events_url": "https://api.github.com/users/github/received_events",
"type": "Organization",
"user_view_type": "public",
"site_admin": false
},
"html_url": "https://github.com/github/Hello-World",
"description": null,
"fork": false,
"url": "https://api.github.com/repos/github/Hello-World",
"forks_url": "https://api.github.com/repos/github/Hello-World/forks",
"keys_url": "https://api.github.com/repos/github/Hello-World/keys{/key_id}",
"collaborators_url": "https://api.github.com/repos/github/Hello-World/collaborators{/collaborator}",
"teams_url": "https://api.github.com/repos/github/Hello-World/teams",
"hooks_url": "https://api.github.com/repos/github/Hello-World/hooks",
"issue_events_url": "https://api.github.com/repos/github/Hello-World/issues/events{/number}",
"events_url": "https://api.github.com/repos/github/Hello-World/events",
"assignees_url": "https://api.github.com/repos/github/Hello-World/assignees{/user}",
"branches_url": "https://api.github.com/repos/github/Hello-World/branches{/branch}",
"tags_url": "https://api.github.com/repos/github/Hello-World/tags",
"blobs_url": "https://api.github.com/repos/github/Hello-World/git/blobs{/sha}",
"git_tags_url": "https://api.github.com/repos/github/Hello-World/git/tags{/sha}",
"git_refs_url": "https://api.github.com/repos/github/Hello-World/git/refs{/sha}",
"trees_url": "https://api.github.com/repos/github/Hello-World/git/trees{/sha}",
"statuses_url": "https://api.github.com/repos/github/Hello-World/statuses/{sha}",
"languages_url": "https://api.github.com/repos/github/Hello-World/languages",
"stargazers_url": "https://api.github.com/repos/github/Hello-World/stargazers",
"contributors_url": "https://api.github.com/repos/github/Hello-World/contributors",
"subscribers_url": "https://api.github.com/repos/github/Hello-World/subscribers",
"subscription_url": "https://api.github.com/repos/github/Hello-World/subscription",
"commits_url": "https://api.github.com/repos/github/Hello-World/commits{/sha}",
"git_commits_url": "https://api.github.com/repos/github/Hello-World/git/commits{/sha}",
"comments_url": "https://api.github.com/repos/github/Hello-World/comments{/number}",
"issue_comment_url": "https://api.github.com/repos/github/Hello-World/issues/comments{/number}",
"contents_url": "https://api.github.com/repos/github/Hello-World/contents/{+path}",
"compare_url": "https://api.github.com/repos/github/Hello-World/compare/{base}...{head}",
"merges_url": "https://api.github.com/repos/github/Hello-World/merges",
"archive_url": "https://api.github.com/repos/github/Hello-World/{archive_format}{/ref}",
"downloads_url": "https://api.github.com/repos/github/Hello-World/downloads",
"issues_url": "https://api.github.com/repos/github/Hello-World/issues{/number}",
"pulls_url": "https://api.github.com/repos/github/Hello-World/pulls{/number}",
"milestones_url": "https://api.github.com/repos/github/Hello-World/milestones{/number}",
"notifications_url": "https://api.github.com/repos/github/Hello-World/notifications{?since,all,participating}",
"labels_url": "https://api.github.com/repos/github/Hello-World/labels{/name}",
"releases_url": "https://api.github.com/repos/github/Hello-World/releases{/id}",
"deployments_url": "https://api.github.com/repos/github/Hello-World/deployments",
"created_at": "2025-08-01T18:44:14Z",
"updated_at": "2025-08-01T18:48:38Z",
"pushed_at": "2025-08-01T18:44:50Z",
"git_url": "git://github.localhost/github/Hello-World.git",
"ssh_url": "ssh://git@localhost:3035/github/Hello-World.git",
"clone_url": "https://github.com/github/Hello-World.git",
"svn_url": "https://github.com/github/Hello-World",
"homepage": null,
"size": 6,
"stargazers_count": 0,
"watchers_count": 0,
"language": null,
"has_issues": true,
"has_projects": true,
"has_downloads": true,
"has_wiki": true,
"has_pages": false,
"has_discussions": false,
"forks_count": 0,
"mirror_url": null,
"archived": false,
"disabled": false,
"open_issues_count": 3,
"license": null,
"allow_forking": true,
"is_template": false,
"web_commit_signoff_required": false,
"topics": [],
"visibility": "public",
"forks": 0,
"open_issues": 3,
"watchers": 0,
"default_branch": "main"
}
},
"_links": {
"self": {
"href": "https://api.github.com/repos/github/Hello-World/pulls/6"
},
"html": {
"href": "https://github.com/github/Hello-World/pull/6"
},
"issue": {
"href": "https://api.github.com/repos/github/Hello-World/issues/6"
},
"comments": {
"href": "https://api.github.com/repos/github/Hello-World/issues/6/comments"
},
"review_comments": {
"href": "https://api.github.com/repos/github/Hello-World/pulls/6/comments"
},
"review_comment": {
"href": "https://api.github.com/repos/github/Hello-World/pulls/comments{/number}"
},
"commits": {
"href": "https://api.github.com/repos/github/Hello-World/pulls/6/commits"
},
"statuses": {
"href": "https://api.github.com/repos/github/Hello-World/statuses/a3258d3434ecb2058b2784c8eb8610c2e9937a0d"
}
},
"author_association": "MEMBER",
"auto_merge": null,
"active_lock_reason": null
},
"content_type": "PullRequest",
"creator": {
"login": "monalisa",
"id": 2,
"node_id": "U_kgAC",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/monalisa",
"html_url": "https://github.com/monalisa",
"followers_url": "https://api.github.com/users/monalisa/followers",
"following_url": "https://api.github.com/users/monalisa/following{/other_user}",
"gists_url": "https://api.github.com/users/monalisa/gists{/gist_id}",
"starred_url": "https://api.github.com/users/monalisa/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/monalisa/subscriptions",
"organizations_url": "https://api.github.com/users/monalisa/orgs",
"repos_url": "https://api.github.com/users/monalisa/repos",
"events_url": "https://api.github.com/users/monalisa/events{/privacy}",
"received_events_url": "https://api.github.com/users/monalisa/received_events",
"type": "User",
"user_view_type": "public",
"site_admin": false
},
"created_at": "2025-08-01T18:44:51Z",
"updated_at": "2025-08-06T19:25:18Z",
"archived_at": null,
"item_url": "https://api.github.com/orgs/github/projectsV2/1/items/13",
"fields": [
{
"id": 1,
"name": "Title",
"type": "title",
"value": {
"raw": "It seemed to me that any civilization that had so far lost its head as to need to include a set of detailed instructions for use in a packet of toothpicks, was no longer a civilization in which I could live and stay sane.",
"html": "It seemed to me that any civilization that had so far lost its head as to need to include a set of detailed instructions for use in a packet of toothpicks, was no longer a civilization in which I could live and stay sane.",
"number": 6,
"url": "https://github.com/5/1/pull/6",
"issue_id": 12,
"state": "open",
"state_reason": null,
"is_draft": false
}
},
{
"id": 2,
"name": "Assignees",
"type": "assignees",
"value": [
{
"login": "octocat",
"id": 175,
"node_id": "U_kgDMrw",
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
"user_view_type": "public",
"site_admin": false
}
]
},
{
"id": 3,
"name": "Status",
"type": "single_select",
"value": {
"id": "98236657",
"name": {
"raw": "Done",
"html": "Done"
},
"color": "PURPLE",
"description": {
"raw": "This has been completed",
"html": "This has been completed"
}
}
},
{
"id": 4,
"name": "Labels",
"type": "labels",
"value": [
{
"id": 19,
"node_id": "LA_kwABEw",
"url": "https://api.github.com/repos/github/Hello-World/labels/bug%20:bug:",
"name": "bug :bug:",
"color": "efe24f",
"default": false,
"description": "Something isn't working"
},
{
"id": 26,
"node_id": "LA_kwABGg",
"url": "https://api.github.com/repos/github/Hello-World/labels/fun%20size%20%F0%9F%8D%AB",
"name": "fun size 🍫",
"color": "f29c24",
"default": false,
"description": "Extra attention is needed"
},
{
"id": 33,
"node_id": "LA_kwABIQ",
"url": "https://api.github.com/repos/github/Hello-World/labels/%F0%9F%9A%92%20wontfix",
"name": "🚒 wontfix",
"color": "5891ce",
"default": false,
"description": "This will not be worked on"
}
]
},
{
"id": 5,
"name": "Linked pull requests",
"type": "linked_pull_requests",
"value": []
},
{
"id": 6,
"name": "Milestone",
"type": "milestone",
"value": {
"url": "https://api.github.com/repos/github/Hello-World/milestones/1",
"html_url": "https://github.com/github/Hello-World/milestone/1",
"labels_url": "https://api.github.com/repos/github/Hello-World/milestones/1/labels",
"id": 1,
"node_id": "MI_kwABAQ",
"number": 1,
"title": "Open milestone",
"description": null,
"creator": {
"login": "octocat",
"id": 175,
"node_id": "U_kgDMrw",
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
"user_view_type": "public",
"site_admin": false
},
"open_issues": 2,
"closed_issues": 1,
"state": "open",
"created_at": "2025-08-01T18:44:30Z",
"updated_at": "2025-08-06T19:14:15Z",
"due_on": null,
"closed_at": null
}
},
{
"id": 7,
"name": "Repository",
"type": "repository",
"value": {
"id": 1,
"node_id": "R_kgAB",
"name": "Hello-World",
"full_name": "github/Hello-World",
"private": false,
"owner": {
"login": "github",
"id": 5,
"node_id": "O_kgAF",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/github",
"html_url": "https://github.com/github",
"followers_url": "https://api.github.com/users/github/followers",
"following_url": "https://api.github.com/users/github/following{/other_user}",
"gists_url": "https://api.github.com/users/github/gists{/gist_id}",
"starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/github/subscriptions",
"organizations_url": "https://api.github.com/users/github/orgs",
"repos_url": "https://api.github.com/users/github/repos",
"events_url": "https://api.github.com/users/github/events{/privacy}",
"received_events_url": "https://api.github.com/users/github/received_events",
"type": "Organization",
"user_view_type": "public",
"site_admin": false
},
"html_url": "https://github.com/github/Hello-World",
"description": null,
"fork": false,
"url": "https://api.github.com/repos/github/Hello-World",
"forks_url": "https://api.github.com/repos/github/Hello-World/forks",
"keys_url": "https://api.github.com/repos/github/Hello-World/keys{/key_id}",
"collaborators_url": "https://api.github.com/repos/github/Hello-World/collaborators{/collaborator}",
"teams_url": "https://api.github.com/repos/github/Hello-World/teams",
"hooks_url": "https://api.github.com/repos/github/Hello-World/hooks",
"issue_events_url": "https://api.github.com/repos/github/Hello-World/issues/events{/number}",
"events_url": "https://api.github.com/repos/github/Hello-World/events",
"assignees_url": "https://api.github.com/repos/github/Hello-World/assignees{/user}",
"branches_url": "https://api.github.com/repos/github/Hello-World/branches{/branch}",
"tags_url": "https://api.github.com/repos/github/Hello-World/tags",
"blobs_url": "https://api.github.com/repos/github/Hello-World/git/blobs{/sha}",
"git_tags_url": "https://api.github.com/repos/github/Hello-World/git/tags{/sha}",
"git_refs_url": "https://api.github.com/repos/github/Hello-World/git/refs{/sha}",
"trees_url": "https://api.github.com/repos/github/Hello-World/git/trees{/sha}",
"statuses_url": "https://api.github.com/repos/github/Hello-World/statuses/{sha}",
"languages_url": "https://api.github.com/repos/github/Hello-World/languages",
"stargazers_url": "https://api.github.com/repos/github/Hello-World/stargazers",
"contributors_url": "https://api.github.com/repos/github/Hello-World/contributors",
"subscribers_url": "https://api.github.com/repos/github/Hello-World/subscribers",
"subscription_url": "https://api.github.com/repos/github/Hello-World/subscription",
"commits_url": "https://api.github.com/repos/github/Hello-World/commits{/sha}",
"git_commits_url": "https://api.github.com/repos/github/Hello-World/git/commits{/sha}",
"comments_url": "https://api.github.com/repos/github/Hello-World/comments{/number}",
"issue_comment_url": "https://api.github.com/repos/github/Hello-World/issues/comments{/number}",
"contents_url": "https://api.github.com/repos/github/Hello-World/contents/{+path}",
"compare_url": "https://api.github.com/repos/github/Hello-World/compare/{base}...{head}",
"merges_url": "https://api.github.com/repos/github/Hello-World/merges",
"archive_url": "https://api.github.com/repos/github/Hello-World/{archive_format}{/ref}",
"downloads_url": "https://api.github.com/repos/github/Hello-World/downloads",
"issues_url": "https://api.github.com/repos/github/Hello-World/issues{/number}",
"pulls_url": "https://api.github.com/repos/github/Hello-World/pulls{/number}",
"milestones_url": "https://api.github.com/repos/github/Hello-World/milestones{/number}",
"notifications_url": "https://api.github.com/repos/github/Hello-World/notifications{?since,all,participating}",
"labels_url": "https://api.github.com/repos/github/Hello-World/labels{/name}",
"releases_url": "https://api.github.com/repos/github/Hello-World/releases{/id}",
"deployments_url": "https://api.github.com/repos/github/Hello-World/deployments"
}
},
{
"id": 8,
"name": "Type",
"type": "issue_type",
"value": null
},
{
"id": 9,
"name": "Reviewers",
"type": "reviewers",
"value": [
{
"type": "ReviewRequest",
"status": "pending",
"reviewer": {
"avatarUrl": "https://github.com/images/error/octocat_happy.gif",
"id": 2,
"login": "monalisa",
"url": "https://github.com/monalisa",
"name": "monalisa",
"type": "User"
}
}
]
},
{
"id": 10,
"name": "Parent issue",
"type": "parent_issue",
"value": null
},
{
"id": 11,
"name": "Sub-issues progress",
"type": "sub_issues_progress",
"value": null
}
]
}`

## Update project item for organization

Update a specific item in an organization-owned project.

### Fine-grained access tokens for "Update project item for organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Projects" organization permissions (write)

### Parameters for "Update project item for organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| project_numberintegerRequiredThe project's number. |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| item_idintegerRequiredThe unique identifier of the project item. |

| Name, Type, Description |
| --- |
| fieldsarray of objectsRequiredA list of field updates to apply. |
| Name, Type, DescriptionidintegerRequiredThe ID of the project field to update.valuenull or string or numberRequiredThe new value for the field:For text, number, and date fields, provide the new value directly.For single select and iteration fields, provide the ID of the option or iteration.To clear the field, set this to null. |
| Name, Type, Description |
| idintegerRequiredThe ID of the project field to update. |
| valuenull or string or numberRequiredThe new value for the field:For text, number, and date fields, provide the new value directly.For single select and iteration fields, provide the ID of the option or iteration.To clear the field, set this to null. |

### HTTP response status codes for "Update project item for organization"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 401 | Requires authentication |
| 403 | Forbidden |
| 404 | Resource not found |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Update project item for organization"

#### Request examples

Select the example typeUpdate a text fieldUpdate a number fieldUpdate a date fieldUpdate a single select fieldUpdate an iteration fieldpatch/orgs/{org}/projectsV2/{project_number}/items/{item_id}

-
-
-

`curl -L \
  -X PATCH \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/projectsV2/PROJECT_NUMBER/items/ITEM_ID \
  -d '{"fields":[{"id":123,"value":"Updated text value"}]}'`

Response

-
-

`Status: 200``{
"id": 13,
"node_id": "PVTI_lAAFAQ0",
"project_url": "https://api.github.com/orgs/github/projectsV2/1",
"content": {
"url": "https://api.github.com/repos/github/Hello-World/pulls/6",
"id": 10,
"node_id": "PR_kwABCg",
"html_url": "https://github.com/github/Hello-World/pull/6",
"diff_url": "https://github.com/github/Hello-World/pull/6.diff",
"patch_url": "https://github.com/github/Hello-World/pull/6.patch",
"issue_url": "https://api.github.com/repos/github/Hello-World/issues/6",
"number": 6,
"state": "open",
"locked": false,
"title": "Issue title",
"user": {
"login": "monalisa",
"id": 161,
"node_id": "U_kgDMoQ",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/monalisa",
"html_url": "https://github.com/monalisa",
"followers_url": "https://api.github.com/users/monalisa/followers",
"following_url": "https://api.github.com/users/monalisa/following{/other_user}",
"gists_url": "https://api.github.com/users/monalisa/gists{/gist_id}",
"starred_url": "https://api.github.com/users/monalisa/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/monalisa/subscriptions",
"organizations_url": "https://api.github.com/users/monalisa/orgs",
"repos_url": "https://api.github.com/users/monalisa/repos",
"events_url": "https://api.github.com/users/monalisa/events{/privacy}",
"received_events_url": "https://api.github.com/users/monalisa/received_events",
"type": "User",
"user_view_type": "public",
"site_admin": false
},
"body": "Issue body",
"created_at": "2025-08-01T18:44:50Z",
"updated_at": "2025-08-06T19:25:18Z",
"closed_at": null,
"merged_at": null,
"merge_commit_sha": "98e25bad5878e54d22e5338cbc905dd2deedfa34",
"assignee": {
"login": "octocat",
"id": 175,
"node_id": "U_kgDMrw",
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
"user_view_type": "public",
"site_admin": false
},
"assignees": [
{
"login": "octocat",
"id": 175,
"node_id": "U_kgDMrw",
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
"user_view_type": "public",
"site_admin": false
}
],
"requested_reviewers": [
{
"login": "monalisa",
"id": 2,
"node_id": "U_kgAC",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/monalisa",
"html_url": "https://github.com/monalisa",
"followers_url": "https://api.github.com/users/monalisa/followers",
"following_url": "https://api.github.com/users/monalisa/following{/other_user}",
"gists_url": "https://api.github.com/users/monalisa/gists{/gist_id}",
"starred_url": "https://api.github.com/users/monalisa/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/monalisa/subscriptions",
"organizations_url": "https://api.github.com/users/monalisa/orgs",
"repos_url": "https://api.github.com/users/monalisa/repos",
"events_url": "https://api.github.com/users/monalisa/events{/privacy}",
"received_events_url": "https://api.github.com/users/monalisa/received_events",
"type": "User",
"user_view_type": "public",
"site_admin": false
}
],
"requested_teams": [],
"labels": [
{
"id": 19,
"node_id": "LA_kwABEw",
"url": "https://api.github.com/repos/github/Hello-World/labels/bug%20:bug:",
"name": "bug :bug:",
"color": "efe24f",
"default": false,
"description": "Something isn't working"
},
{
"id": 26,
"node_id": "LA_kwABGg",
"url": "https://api.github.com/repos/github/Hello-World/labels/fun%20size%20%F0%9F%8D%AB",
"name": "fun size 🍫",
"color": "f29c24",
"default": false,
"description": "Extra attention is needed"
},
{
"id": 33,
"node_id": "LA_kwABIQ",
"url": "https://api.github.com/repos/github/Hello-World/labels/%F0%9F%9A%92%20wontfix",
"name": "🚒 wontfix",
"color": "5891ce",
"default": false,
"description": "This will not be worked on"
}
],
"milestone": {
"url": "https://api.github.com/repos/github/Hello-World/milestones/1",
"html_url": "https://github.com/github/Hello-World/milestone/1",
"labels_url": "https://api.github.com/repos/github/Hello-World/milestones/1/labels",
"id": 1,
"node_id": "MI_kwABAQ",
"number": 1,
"title": "Open milestone",
"description": null,
"creator": {
"login": "monalisa",
"id": 2,
"node_id": "U_kgAC",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/monalisa",
"html_url": "https://github.com/monalisa",
"followers_url": "https://api.github.com/users/monalisa/followers",
"following_url": "https://api.github.com/users/monalisa/following{/other_user}",
"gists_url": "https://api.github.com/users/monalisa/gists{/gist_id}",
"starred_url": "https://api.github.com/users/monalisa/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/monalisa/subscriptions",
"organizations_url": "https://api.github.com/users/monalisa/orgs",
"repos_url": "https://api.github.com/users/monalisa/repos",
"events_url": "https://api.github.com/users/monalisa/events{/privacy}",
"received_events_url": "https://api.github.com/users/monalisa/received_events",
"type": "User",
"user_view_type": "public",
"site_admin": false
},
"open_issues": 2,
"closed_issues": 1,
"state": "open",
"created_at": "2025-08-01T18:44:30Z",
"updated_at": "2025-08-06T19:14:15Z",
"due_on": null,
"closed_at": null
},
"draft": false,
"commits_url": "https://api.github.com/repos/github/Hello-World/pulls/6/commits",
"review_comments_url": "https://api.github.com/repos/github/Hello-World/pulls/6/comments",
"review_comment_url": "https://api.github.com/repos/github/Hello-World/pulls/comments{/number}",
"comments_url": "https://api.github.com/repos/github/Hello-World/issues/6/comments",
"statuses_url": "https://api.github.com/repos/github/Hello-World/statuses/a3258d3434ecb2058b2784c8eb8610c2e9937a0d",
"head": {
"label": "github:branch-2ee3da8fde8a1adfe6d0809a1a414e4f",
"ref": "branch-2ee3da8fde8a1adfe6d0809a1a414e4f",
"sha": "a3258d3434ecb2058b2784c8eb8610c2e9937a0d",
"user": {
"login": "github",
"id": 5,
"node_id": "O_kgAF",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/github",
"html_url": "https://github.com/github",
"followers_url": "https://api.github.com/users/github/followers",
"following_url": "https://api.github.com/users/github/following{/other_user}",
"gists_url": "https://api.github.com/users/github/gists{/gist_id}",
"starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/github/subscriptions",
"organizations_url": "https://api.github.com/users/github/orgs",
"repos_url": "https://api.github.com/users/github/repos",
"events_url": "https://api.github.com/users/github/events{/privacy}",
"received_events_url": "https://api.github.com/users/github/received_events",
"type": "Organization",
"user_view_type": "public",
"site_admin": false
},
"repo": {
"id": 1,
"node_id": "R_kgAB",
"name": "Hello-World",
"full_name": "github/Hello-World",
"private": false,
"owner": {
"login": "github",
"id": 5,
"node_id": "O_kgAF",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/github",
"html_url": "https://github.com/github",
"followers_url": "https://api.github.com/users/github/followers",
"following_url": "https://api.github.com/users/github/following{/other_user}",
"gists_url": "https://api.github.com/users/github/gists{/gist_id}",
"starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/github/subscriptions",
"organizations_url": "https://api.github.com/users/github/orgs",
"repos_url": "https://api.github.com/users/github/repos",
"events_url": "https://api.github.com/users/github/events{/privacy}",
"received_events_url": "https://api.github.com/users/github/received_events",
"type": "Organization",
"user_view_type": "public",
"site_admin": false
},
"html_url": "https://github.com/github/Hello-World",
"description": null,
"fork": false,
"url": "https://api.github.com/repos/github/Hello-World",
"forks_url": "https://api.github.com/repos/github/Hello-World/forks",
"keys_url": "https://api.github.com/repos/github/Hello-World/keys{/key_id}",
"collaborators_url": "https://api.github.com/repos/github/Hello-World/collaborators{/collaborator}",
"teams_url": "https://api.github.com/repos/github/Hello-World/teams",
"hooks_url": "https://api.github.com/repos/github/Hello-World/hooks",
"issue_events_url": "https://api.github.com/repos/github/Hello-World/issues/events{/number}",
"events_url": "https://api.github.com/repos/github/Hello-World/events",
"assignees_url": "https://api.github.com/repos/github/Hello-World/assignees{/user}",
"branches_url": "https://api.github.com/repos/github/Hello-World/branches{/branch}",
"tags_url": "https://api.github.com/repos/github/Hello-World/tags",
"blobs_url": "https://api.github.com/repos/github/Hello-World/git/blobs{/sha}",
"git_tags_url": "https://api.github.com/repos/github/Hello-World/git/tags{/sha}",
"git_refs_url": "https://api.github.com/repos/github/Hello-World/git/refs{/sha}",
"trees_url": "https://api.github.com/repos/github/Hello-World/git/trees{/sha}",
"statuses_url": "https://api.github.com/repos/github/Hello-World/statuses/{sha}",
"languages_url": "https://api.github.com/repos/github/Hello-World/languages",
"stargazers_url": "https://api.github.com/repos/github/Hello-World/stargazers",
"contributors_url": "https://api.github.com/repos/github/Hello-World/contributors",
"subscribers_url": "https://api.github.com/repos/github/Hello-World/subscribers",
"subscription_url": "https://api.github.com/repos/github/Hello-World/subscription",
"commits_url": "https://api.github.com/repos/github/Hello-World/commits{/sha}",
"git_commits_url": "https://api.github.com/repos/github/Hello-World/git/commits{/sha}",
"comments_url": "https://api.github.com/repos/github/Hello-World/comments{/number}",
"issue_comment_url": "https://api.github.com/repos/github/Hello-World/issues/comments{/number}",
"contents_url": "https://api.github.com/repos/github/Hello-World/contents/{+path}",
"compare_url": "https://api.github.com/repos/github/Hello-World/compare/{base}...{head}",
"merges_url": "https://api.github.com/repos/github/Hello-World/merges",
"archive_url": "https://api.github.com/repos/github/Hello-World/{archive_format}{/ref}",
"downloads_url": "https://api.github.com/repos/github/Hello-World/downloads",
"issues_url": "https://api.github.com/repos/github/Hello-World/issues{/number}",
"pulls_url": "https://api.github.com/repos/github/Hello-World/pulls{/number}",
"milestones_url": "https://api.github.com/repos/github/Hello-World/milestones{/number}",
"notifications_url": "https://api.github.com/repos/github/Hello-World/notifications{?since,all,participating}",
"labels_url": "https://api.github.com/repos/github/Hello-World/labels{/name}",
"releases_url": "https://api.github.com/repos/github/Hello-World/releases{/id}",
"deployments_url": "https://api.github.com/repos/github/Hello-World/deployments",
"created_at": "2025-08-01T18:44:14Z",
"updated_at": "2025-08-01T18:48:38Z",
"pushed_at": "2025-08-01T18:44:50Z",
"git_url": "git://github.localhost/github/Hello-World.git",
"ssh_url": "ssh://git@localhost:3035/github/Hello-World.git",
"clone_url": "https://github.com/github/Hello-World.git",
"svn_url": "https://github.com/github/Hello-World",
"homepage": null,
"size": 6,
"stargazers_count": 0,
"watchers_count": 0,
"language": null,
"has_issues": true,
"has_projects": true,
"has_downloads": true,
"has_wiki": true,
"has_pages": false,
"has_discussions": false,
"forks_count": 0,
"mirror_url": null,
"archived": false,
"disabled": false,
"open_issues_count": 3,
"license": null,
"allow_forking": true,
"is_template": false,
"web_commit_signoff_required": false,
"topics": [],
"visibility": "public",
"forks": 0,
"open_issues": 3,
"watchers": 0,
"default_branch": "main"
}
},
"base": {
"label": "github:branch-0f4ceb14cbe39e4786ffbabb776da599",
"ref": "branch-0f4ceb14cbe39e4786ffbabb776da599",
"sha": "9a9f5a8d77bdc2540412900d3c930fe36a82b5ed",
"user": {
"login": "github",
"id": 5,
"node_id": "O_kgAF",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/github",
"html_url": "https://github.com/github",
"followers_url": "https://api.github.com/users/github/followers",
"following_url": "https://api.github.com/users/github/following{/other_user}",
"gists_url": "https://api.github.com/users/github/gists{/gist_id}",
"starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/github/subscriptions",
"organizations_url": "https://api.github.com/users/github/orgs",
"repos_url": "https://api.github.com/users/github/repos",
"events_url": "https://api.github.com/users/github/events{/privacy}",
"received_events_url": "https://api.github.com/users/github/received_events",
"type": "Organization",
"user_view_type": "public",
"site_admin": false
},
"repo": {
"id": 1,
"node_id": "R_kgAB",
"name": "Hello-World",
"full_name": "github/Hello-World",
"private": false,
"owner": {
"login": "github",
"id": 5,
"node_id": "O_kgAF",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/github",
"html_url": "https://github.com/github",
"followers_url": "https://api.github.com/users/github/followers",
"following_url": "https://api.github.com/users/github/following{/other_user}",
"gists_url": "https://api.github.com/users/github/gists{/gist_id}",
"starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/github/subscriptions",
"organizations_url": "https://api.github.com/users/github/orgs",
"repos_url": "https://api.github.com/users/github/repos",
"events_url": "https://api.github.com/users/github/events{/privacy}",
"received_events_url": "https://api.github.com/users/github/received_events",
"type": "Organization",
"user_view_type": "public",
"site_admin": false
},
"html_url": "https://github.com/github/Hello-World",
"description": null,
"fork": false,
"url": "https://api.github.com/repos/github/Hello-World",
"forks_url": "https://api.github.com/repos/github/Hello-World/forks",
"keys_url": "https://api.github.com/repos/github/Hello-World/keys{/key_id}",
"collaborators_url": "https://api.github.com/repos/github/Hello-World/collaborators{/collaborator}",
"teams_url": "https://api.github.com/repos/github/Hello-World/teams",
"hooks_url": "https://api.github.com/repos/github/Hello-World/hooks",
"issue_events_url": "https://api.github.com/repos/github/Hello-World/issues/events{/number}",
"events_url": "https://api.github.com/repos/github/Hello-World/events",
"assignees_url": "https://api.github.com/repos/github/Hello-World/assignees{/user}",
"branches_url": "https://api.github.com/repos/github/Hello-World/branches{/branch}",
"tags_url": "https://api.github.com/repos/github/Hello-World/tags",
"blobs_url": "https://api.github.com/repos/github/Hello-World/git/blobs{/sha}",
"git_tags_url": "https://api.github.com/repos/github/Hello-World/git/tags{/sha}",
"git_refs_url": "https://api.github.com/repos/github/Hello-World/git/refs{/sha}",
"trees_url": "https://api.github.com/repos/github/Hello-World/git/trees{/sha}",
"statuses_url": "https://api.github.com/repos/github/Hello-World/statuses/{sha}",
"languages_url": "https://api.github.com/repos/github/Hello-World/languages",
"stargazers_url": "https://api.github.com/repos/github/Hello-World/stargazers",
"contributors_url": "https://api.github.com/repos/github/Hello-World/contributors",
"subscribers_url": "https://api.github.com/repos/github/Hello-World/subscribers",
"subscription_url": "https://api.github.com/repos/github/Hello-World/subscription",
"commits_url": "https://api.github.com/repos/github/Hello-World/commits{/sha}",
"git_commits_url": "https://api.github.com/repos/github/Hello-World/git/commits{/sha}",
"comments_url": "https://api.github.com/repos/github/Hello-World/comments{/number}",
"issue_comment_url": "https://api.github.com/repos/github/Hello-World/issues/comments{/number}",
"contents_url": "https://api.github.com/repos/github/Hello-World/contents/{+path}",
"compare_url": "https://api.github.com/repos/github/Hello-World/compare/{base}...{head}",
"merges_url": "https://api.github.com/repos/github/Hello-World/merges",
"archive_url": "https://api.github.com/repos/github/Hello-World/{archive_format}{/ref}",
"downloads_url": "https://api.github.com/repos/github/Hello-World/downloads",
"issues_url": "https://api.github.com/repos/github/Hello-World/issues{/number}",
"pulls_url": "https://api.github.com/repos/github/Hello-World/pulls{/number}",
"milestones_url": "https://api.github.com/repos/github/Hello-World/milestones{/number}",
"notifications_url": "https://api.github.com/repos/github/Hello-World/notifications{?since,all,participating}",
"labels_url": "https://api.github.com/repos/github/Hello-World/labels{/name}",
"releases_url": "https://api.github.com/repos/github/Hello-World/releases{/id}",
"deployments_url": "https://api.github.com/repos/github/Hello-World/deployments",
"created_at": "2025-08-01T18:44:14Z",
"updated_at": "2025-08-01T18:48:38Z",
"pushed_at": "2025-08-01T18:44:50Z",
"git_url": "git://github.localhost/github/Hello-World.git",
"ssh_url": "ssh://git@localhost:3035/github/Hello-World.git",
"clone_url": "https://github.com/github/Hello-World.git",
"svn_url": "https://github.com/github/Hello-World",
"homepage": null,
"size": 6,
"stargazers_count": 0,
"watchers_count": 0,
"language": null,
"has_issues": true,
"has_projects": true,
"has_downloads": true,
"has_wiki": true,
"has_pages": false,
"has_discussions": false,
"forks_count": 0,
"mirror_url": null,
"archived": false,
"disabled": false,
"open_issues_count": 3,
"license": null,
"allow_forking": true,
"is_template": false,
"web_commit_signoff_required": false,
"topics": [],
"visibility": "public",
"forks": 0,
"open_issues": 3,
"watchers": 0,
"default_branch": "main"
}
},
"_links": {
"self": {
"href": "https://api.github.com/repos/github/Hello-World/pulls/6"
},
"html": {
"href": "https://github.com/github/Hello-World/pull/6"
},
"issue": {
"href": "https://api.github.com/repos/github/Hello-World/issues/6"
},
"comments": {
"href": "https://api.github.com/repos/github/Hello-World/issues/6/comments"
},
"review_comments": {
"href": "https://api.github.com/repos/github/Hello-World/pulls/6/comments"
},
"review_comment": {
"href": "https://api.github.com/repos/github/Hello-World/pulls/comments{/number}"
},
"commits": {
"href": "https://api.github.com/repos/github/Hello-World/pulls/6/commits"
},
"statuses": {
"href": "https://api.github.com/repos/github/Hello-World/statuses/a3258d3434ecb2058b2784c8eb8610c2e9937a0d"
}
},
"author_association": "MEMBER",
"auto_merge": null,
"active_lock_reason": null
},
"content_type": "PullRequest",
"creator": {
"login": "monalisa",
"id": 2,
"node_id": "U_kgAC",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/monalisa",
"html_url": "https://github.com/monalisa",
"followers_url": "https://api.github.com/users/monalisa/followers",
"following_url": "https://api.github.com/users/monalisa/following{/other_user}",
"gists_url": "https://api.github.com/users/monalisa/gists{/gist_id}",
"starred_url": "https://api.github.com/users/monalisa/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/monalisa/subscriptions",
"organizations_url": "https://api.github.com/users/monalisa/orgs",
"repos_url": "https://api.github.com/users/monalisa/repos",
"events_url": "https://api.github.com/users/monalisa/events{/privacy}",
"received_events_url": "https://api.github.com/users/monalisa/received_events",
"type": "User",
"user_view_type": "public",
"site_admin": false
},
"created_at": "2025-08-01T18:44:51Z",
"updated_at": "2025-08-06T19:25:18Z",
"archived_at": null,
"item_url": "https://api.github.com/orgs/github/projectsV2/1/items/13",
"fields": [
{
"id": 1,
"name": "Title",
"type": "title",
"value": {
"raw": "It seemed to me that any civilization that had so far lost its head as to need to include a set of detailed instructions for use in a packet of toothpicks, was no longer a civilization in which I could live and stay sane.",
"html": "It seemed to me that any civilization that had so far lost its head as to need to include a set of detailed instructions for use in a packet of toothpicks, was no longer a civilization in which I could live and stay sane.",
"number": 6,
"url": "https://github.com/5/1/pull/6",
"issue_id": 12,
"state": "open",
"state_reason": null,
"is_draft": false
}
},
{
"id": 2,
"name": "Assignees",
"type": "assignees",
"value": [
{
"login": "octocat",
"id": 175,
"node_id": "U_kgDMrw",
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
"user_view_type": "public",
"site_admin": false
}
]
},
{
"id": 3,
"name": "Status",
"type": "single_select",
"value": {
"id": "98236657",
"name": {
"raw": "Done",
"html": "Done"
},
"color": "PURPLE",
"description": {
"raw": "This has been completed",
"html": "This has been completed"
}
}
},
{
"id": 4,
"name": "Labels",
"type": "labels",
"value": [
{
"id": 19,
"node_id": "LA_kwABEw",
"url": "https://api.github.com/repos/github/Hello-World/labels/bug%20:bug:",
"name": "bug :bug:",
"color": "efe24f",
"default": false,
"description": "Something isn't working"
},
{
"id": 26,
"node_id": "LA_kwABGg",
"url": "https://api.github.com/repos/github/Hello-World/labels/fun%20size%20%F0%9F%8D%AB",
"name": "fun size 🍫",
"color": "f29c24",
"default": false,
"description": "Extra attention is needed"
},
{
"id": 33,
"node_id": "LA_kwABIQ",
"url": "https://api.github.com/repos/github/Hello-World/labels/%F0%9F%9A%92%20wontfix",
"name": "🚒 wontfix",
"color": "5891ce",
"default": false,
"description": "This will not be worked on"
}
]
},
{
"id": 5,
"name": "Linked pull requests",
"type": "linked_pull_requests",
"value": []
},
{
"id": 6,
"name": "Milestone",
"type": "milestone",
"value": {
"url": "https://api.github.com/repos/github/Hello-World/milestones/1",
"html_url": "https://github.com/github/Hello-World/milestone/1",
"labels_url": "https://api.github.com/repos/github/Hello-World/milestones/1/labels",
"id": 1,
"node_id": "MI_kwABAQ",
"number": 1,
"title": "Open milestone",
"description": null,
"creator": {
"login": "octocat",
"id": 175,
"node_id": "U_kgDMrw",
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
"user_view_type": "public",
"site_admin": false
},
"open_issues": 2,
"closed_issues": 1,
"state": "open",
"created_at": "2025-08-01T18:44:30Z",
"updated_at": "2025-08-06T19:14:15Z",
"due_on": null,
"closed_at": null
}
},
{
"id": 7,
"name": "Repository",
"type": "repository",
"value": {
"id": 1,
"node_id": "R_kgAB",
"name": "Hello-World",
"full_name": "github/Hello-World",
"private": false,
"owner": {
"login": "github",
"id": 5,
"node_id": "O_kgAF",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/github",
"html_url": "https://github.com/github",
"followers_url": "https://api.github.com/users/github/followers",
"following_url": "https://api.github.com/users/github/following{/other_user}",
"gists_url": "https://api.github.com/users/github/gists{/gist_id}",
"starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/github/subscriptions",
"organizations_url": "https://api.github.com/users/github/orgs",
"repos_url": "https://api.github.com/users/github/repos",
"events_url": "https://api.github.com/users/github/events{/privacy}",
"received_events_url": "https://api.github.com/users/github/received_events",
"type": "Organization",
"user_view_type": "public",
"site_admin": false
},
"html_url": "https://github.com/github/Hello-World",
"description": null,
"fork": false,
"url": "https://api.github.com/repos/github/Hello-World",
"forks_url": "https://api.github.com/repos/github/Hello-World/forks",
"keys_url": "https://api.github.com/repos/github/Hello-World/keys{/key_id}",
"collaborators_url": "https://api.github.com/repos/github/Hello-World/collaborators{/collaborator}",
"teams_url": "https://api.github.com/repos/github/Hello-World/teams",
"hooks_url": "https://api.github.com/repos/github/Hello-World/hooks",
"issue_events_url": "https://api.github.com/repos/github/Hello-World/issues/events{/number}",
"events_url": "https://api.github.com/repos/github/Hello-World/events",
"assignees_url": "https://api.github.com/repos/github/Hello-World/assignees{/user}",
"branches_url": "https://api.github.com/repos/github/Hello-World/branches{/branch}",
"tags_url": "https://api.github.com/repos/github/Hello-World/tags",
"blobs_url": "https://api.github.com/repos/github/Hello-World/git/blobs{/sha}",
"git_tags_url": "https://api.github.com/repos/github/Hello-World/git/tags{/sha}",
"git_refs_url": "https://api.github.com/repos/github/Hello-World/git/refs{/sha}",
"trees_url": "https://api.github.com/repos/github/Hello-World/git/trees{/sha}",
"statuses_url": "https://api.github.com/repos/github/Hello-World/statuses/{sha}",
"languages_url": "https://api.github.com/repos/github/Hello-World/languages",
"stargazers_url": "https://api.github.com/repos/github/Hello-World/stargazers",
"contributors_url": "https://api.github.com/repos/github/Hello-World/contributors",
"subscribers_url": "https://api.github.com/repos/github/Hello-World/subscribers",
"subscription_url": "https://api.github.com/repos/github/Hello-World/subscription",
"commits_url": "https://api.github.com/repos/github/Hello-World/commits{/sha}",
"git_commits_url": "https://api.github.com/repos/github/Hello-World/git/commits{/sha}",
"comments_url": "https://api.github.com/repos/github/Hello-World/comments{/number}",
"issue_comment_url": "https://api.github.com/repos/github/Hello-World/issues/comments{/number}",
"contents_url": "https://api.github.com/repos/github/Hello-World/contents/{+path}",
"compare_url": "https://api.github.com/repos/github/Hello-World/compare/{base}...{head}",
"merges_url": "https://api.github.com/repos/github/Hello-World/merges",
"archive_url": "https://api.github.com/repos/github/Hello-World/{archive_format}{/ref}",
"downloads_url": "https://api.github.com/repos/github/Hello-World/downloads",
"issues_url": "https://api.github.com/repos/github/Hello-World/issues{/number}",
"pulls_url": "https://api.github.com/repos/github/Hello-World/pulls{/number}",
"milestones_url": "https://api.github.com/repos/github/Hello-World/milestones{/number}",
"notifications_url": "https://api.github.com/repos/github/Hello-World/notifications{?since,all,participating}",
"labels_url": "https://api.github.com/repos/github/Hello-World/labels{/name}",
"releases_url": "https://api.github.com/repos/github/Hello-World/releases{/id}",
"deployments_url": "https://api.github.com/repos/github/Hello-World/deployments"
}
},
{
"id": 8,
"name": "Type",
"type": "issue_type",
"value": null
},
{
"id": 9,
"name": "Reviewers",
"type": "reviewers",
"value": [
{
"type": "ReviewRequest",
"status": "pending",
"reviewer": {
"avatarUrl": "https://github.com/images/error/octocat_happy.gif",
"id": 2,
"login": "monalisa",
"url": "https://github.com/monalisa",
"name": "monalisa",
"type": "User"
}
}
]
},
{
"id": 10,
"name": "Parent issue",
"type": "parent_issue",
"value": null
},
{
"id": 11,
"name": "Sub-issues progress",
"type": "sub_issues_progress",
"value": null
}
]
}`

## Delete project item for organization

Delete a specific item from an organization-owned project.

### Fine-grained access tokens for "Delete project item for organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Projects" organization permissions (write)

### Parameters for "Delete project item for organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| project_numberintegerRequiredThe project's number. |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| item_idintegerRequiredThe unique identifier of the project item. |

### HTTP response status codes for "Delete project item for organization"

| Status code | Description |
| --- | --- |
| 204 | No Content |
| 401 | Requires authentication |
| 403 | Forbidden |

### Code samples for "Delete project item for organization"

#### Request example

delete/orgs/{org}/projectsV2/{project_number}/items/{item_id}

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/projectsV2/PROJECT_NUMBER/items/ITEM_ID`

Response

`Status: 204`

## List items for an organization project view

List items in an organization project with the saved view's filter applied.

### Fine-grained access tokens for "List items for an organization project view"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Projects" organization permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "List items for an organization project view"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| project_numberintegerRequiredThe project's number. |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| view_numberintegerRequiredThe number that identifies the project view. |

| Name, Type, Description |
| --- |
| fieldsLimit results to specific fields, by their IDs. If not specified, the
title field will be returned.Example:fields[]=123&fields[]=456&fields[]=789orfields=123,456,789 |
| beforestringA cursor, as given in theLink header. If specified, the query only searches for results before this cursor. For more information, see "Using pagination in the REST API." |
| afterstringA cursor, as given in theLink header. If specified, the query only searches for results after this cursor. For more information, see "Using pagination in the REST API." |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |

### HTTP response status codes for "List items for an organization project view"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 304 | Not modified |
| 401 | Requires authentication |
| 403 | Forbidden |
| 404 | Resource not found |

### Code samples for "List items for an organization project view"

#### Request example

get/orgs/{org}/projectsV2/{project_number}/views/{view_number}/items

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/projectsV2/PROJECT_NUMBER/views/VIEW_NUMBER/items`

Response

-
-

`Status: 200``{
"id": 13,
"node_id": "PVTI_lAAFAQ0",
"project_url": "https://api.github.com/orgs/github/projectsV2/1",
"content": {
"url": "https://api.github.com/repos/github/Hello-World/pulls/6",
"id": 10,
"node_id": "PR_kwABCg",
"html_url": "https://github.com/github/Hello-World/pull/6",
"diff_url": "https://github.com/github/Hello-World/pull/6.diff",
"patch_url": "https://github.com/github/Hello-World/pull/6.patch",
"issue_url": "https://api.github.com/repos/github/Hello-World/issues/6",
"number": 6,
"state": "open",
"locked": false,
"title": "Issue title",
"user": {
"login": "monalisa",
"id": 161,
"node_id": "U_kgDMoQ",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/monalisa",
"html_url": "https://github.com/monalisa",
"followers_url": "https://api.github.com/users/monalisa/followers",
"following_url": "https://api.github.com/users/monalisa/following{/other_user}",
"gists_url": "https://api.github.com/users/monalisa/gists{/gist_id}",
"starred_url": "https://api.github.com/users/monalisa/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/monalisa/subscriptions",
"organizations_url": "https://api.github.com/users/monalisa/orgs",
"repos_url": "https://api.github.com/users/monalisa/repos",
"events_url": "https://api.github.com/users/monalisa/events{/privacy}",
"received_events_url": "https://api.github.com/users/monalisa/received_events",
"type": "User",
"user_view_type": "public",
"site_admin": false
},
"body": "Issue body",
"created_at": "2025-08-01T18:44:50Z",
"updated_at": "2025-08-06T19:25:18Z",
"closed_at": null,
"merged_at": null,
"merge_commit_sha": "98e25bad5878e54d22e5338cbc905dd2deedfa34",
"assignee": {
"login": "octocat",
"id": 175,
"node_id": "U_kgDMrw",
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
"user_view_type": "public",
"site_admin": false
},
"assignees": [
{
"login": "octocat",
"id": 175,
"node_id": "U_kgDMrw",
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
"user_view_type": "public",
"site_admin": false
}
],
"requested_reviewers": [
{
"login": "monalisa",
"id": 2,
"node_id": "U_kgAC",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/monalisa",
"html_url": "https://github.com/monalisa",
"followers_url": "https://api.github.com/users/monalisa/followers",
"following_url": "https://api.github.com/users/monalisa/following{/other_user}",
"gists_url": "https://api.github.com/users/monalisa/gists{/gist_id}",
"starred_url": "https://api.github.com/users/monalisa/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/monalisa/subscriptions",
"organizations_url": "https://api.github.com/users/monalisa/orgs",
"repos_url": "https://api.github.com/users/monalisa/repos",
"events_url": "https://api.github.com/users/monalisa/events{/privacy}",
"received_events_url": "https://api.github.com/users/monalisa/received_events",
"type": "User",
"user_view_type": "public",
"site_admin": false
}
],
"requested_teams": [],
"labels": [
{
"id": 19,
"node_id": "LA_kwABEw",
"url": "https://api.github.com/repos/github/Hello-World/labels/bug%20:bug:",
"name": "bug :bug:",
"color": "efe24f",
"default": false,
"description": "Something isn't working"
},
{
"id": 26,
"node_id": "LA_kwABGg",
"url": "https://api.github.com/repos/github/Hello-World/labels/fun%20size%20%F0%9F%8D%AB",
"name": "fun size 🍫",
"color": "f29c24",
"default": false,
"description": "Extra attention is needed"
},
{
"id": 33,
"node_id": "LA_kwABIQ",
"url": "https://api.github.com/repos/github/Hello-World/labels/%F0%9F%9A%92%20wontfix",
"name": "🚒 wontfix",
"color": "5891ce",
"default": false,
"description": "This will not be worked on"
}
],
"milestone": {
"url": "https://api.github.com/repos/github/Hello-World/milestones/1",
"html_url": "https://github.com/github/Hello-World/milestone/1",
"labels_url": "https://api.github.com/repos/github/Hello-World/milestones/1/labels",
"id": 1,
"node_id": "MI_kwABAQ",
"number": 1,
"title": "Open milestone",
"description": null,
"creator": {
"login": "monalisa",
"id": 2,
"node_id": "U_kgAC",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/monalisa",
"html_url": "https://github.com/monalisa",
"followers_url": "https://api.github.com/users/monalisa/followers",
"following_url": "https://api.github.com/users/monalisa/following{/other_user}",
"gists_url": "https://api.github.com/users/monalisa/gists{/gist_id}",
"starred_url": "https://api.github.com/users/monalisa/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/monalisa/subscriptions",
"organizations_url": "https://api.github.com/users/monalisa/orgs",
"repos_url": "https://api.github.com/users/monalisa/repos",
"events_url": "https://api.github.com/users/monalisa/events{/privacy}",
"received_events_url": "https://api.github.com/users/monalisa/received_events",
"type": "User",
"user_view_type": "public",
"site_admin": false
},
"open_issues": 2,
"closed_issues": 1,
"state": "open",
"created_at": "2025-08-01T18:44:30Z",
"updated_at": "2025-08-06T19:14:15Z",
"due_on": null,
"closed_at": null
},
"draft": false,
"commits_url": "https://api.github.com/repos/github/Hello-World/pulls/6/commits",
"review_comments_url": "https://api.github.com/repos/github/Hello-World/pulls/6/comments",
"review_comment_url": "https://api.github.com/repos/github/Hello-World/pulls/comments{/number}",
"comments_url": "https://api.github.com/repos/github/Hello-World/issues/6/comments",
"statuses_url": "https://api.github.com/repos/github/Hello-World/statuses/a3258d3434ecb2058b2784c8eb8610c2e9937a0d",
"head": {
"label": "github:branch-2ee3da8fde8a1adfe6d0809a1a414e4f",
"ref": "branch-2ee3da8fde8a1adfe6d0809a1a414e4f",
"sha": "a3258d3434ecb2058b2784c8eb8610c2e9937a0d",
"user": {
"login": "github",
"id": 5,
"node_id": "O_kgAF",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/github",
"html_url": "https://github.com/github",
"followers_url": "https://api.github.com/users/github/followers",
"following_url": "https://api.github.com/users/github/following{/other_user}",
"gists_url": "https://api.github.com/users/github/gists{/gist_id}",
"starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/github/subscriptions",
"organizations_url": "https://api.github.com/users/github/orgs",
"repos_url": "https://api.github.com/users/github/repos",
"events_url": "https://api.github.com/users/github/events{/privacy}",
"received_events_url": "https://api.github.com/users/github/received_events",
"type": "Organization",
"user_view_type": "public",
"site_admin": false
},
"repo": {
"id": 1,
"node_id": "R_kgAB",
"name": "Hello-World",
"full_name": "github/Hello-World",
"private": false,
"owner": {
"login": "github",
"id": 5,
"node_id": "O_kgAF",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/github",
"html_url": "https://github.com/github",
"followers_url": "https://api.github.com/users/github/followers",
"following_url": "https://api.github.com/users/github/following{/other_user}",
"gists_url": "https://api.github.com/users/github/gists{/gist_id}",
"starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/github/subscriptions",
"organizations_url": "https://api.github.com/users/github/orgs",
"repos_url": "https://api.github.com/users/github/repos",
"events_url": "https://api.github.com/users/github/events{/privacy}",
"received_events_url": "https://api.github.com/users/github/received_events",
"type": "Organization",
"user_view_type": "public",
"site_admin": false
},
"html_url": "https://github.com/github/Hello-World",
"description": null,
"fork": false,
"url": "https://api.github.com/repos/github/Hello-World",
"forks_url": "https://api.github.com/repos/github/Hello-World/forks",
"keys_url": "https://api.github.com/repos/github/Hello-World/keys{/key_id}",
"collaborators_url": "https://api.github.com/repos/github/Hello-World/collaborators{/collaborator}",
"teams_url": "https://api.github.com/repos/github/Hello-World/teams",
"hooks_url": "https://api.github.com/repos/github/Hello-World/hooks",
"issue_events_url": "https://api.github.com/repos/github/Hello-World/issues/events{/number}",
"events_url": "https://api.github.com/repos/github/Hello-World/events",
"assignees_url": "https://api.github.com/repos/github/Hello-World/assignees{/user}",
"branches_url": "https://api.github.com/repos/github/Hello-World/branches{/branch}",
"tags_url": "https://api.github.com/repos/github/Hello-World/tags",
"blobs_url": "https://api.github.com/repos/github/Hello-World/git/blobs{/sha}",
"git_tags_url": "https://api.github.com/repos/github/Hello-World/git/tags{/sha}",
"git_refs_url": "https://api.github.com/repos/github/Hello-World/git/refs{/sha}",
"trees_url": "https://api.github.com/repos/github/Hello-World/git/trees{/sha}",
"statuses_url": "https://api.github.com/repos/github/Hello-World/statuses/{sha}",
"languages_url": "https://api.github.com/repos/github/Hello-World/languages",
"stargazers_url": "https://api.github.com/repos/github/Hello-World/stargazers",
"contributors_url": "https://api.github.com/repos/github/Hello-World/contributors",
"subscribers_url": "https://api.github.com/repos/github/Hello-World/subscribers",
"subscription_url": "https://api.github.com/repos/github/Hello-World/subscription",
"commits_url": "https://api.github.com/repos/github/Hello-World/commits{/sha}",
"git_commits_url": "https://api.github.com/repos/github/Hello-World/git/commits{/sha}",
"comments_url": "https://api.github.com/repos/github/Hello-World/comments{/number}",
"issue_comment_url": "https://api.github.com/repos/github/Hello-World/issues/comments{/number}",
"contents_url": "https://api.github.com/repos/github/Hello-World/contents/{+path}",
"compare_url": "https://api.github.com/repos/github/Hello-World/compare/{base}...{head}",
"merges_url": "https://api.github.com/repos/github/Hello-World/merges",
"archive_url": "https://api.github.com/repos/github/Hello-World/{archive_format}{/ref}",
"downloads_url": "https://api.github.com/repos/github/Hello-World/downloads",
"issues_url": "https://api.github.com/repos/github/Hello-World/issues{/number}",
"pulls_url": "https://api.github.com/repos/github/Hello-World/pulls{/number}",
"milestones_url": "https://api.github.com/repos/github/Hello-World/milestones{/number}",
"notifications_url": "https://api.github.com/repos/github/Hello-World/notifications{?since,all,participating}",
"labels_url": "https://api.github.com/repos/github/Hello-World/labels{/name}",
"releases_url": "https://api.github.com/repos/github/Hello-World/releases{/id}",
"deployments_url": "https://api.github.com/repos/github/Hello-World/deployments",
"created_at": "2025-08-01T18:44:14Z",
"updated_at": "2025-08-01T18:48:38Z",
"pushed_at": "2025-08-01T18:44:50Z",
"git_url": "git://github.localhost/github/Hello-World.git",
"ssh_url": "ssh://git@localhost:3035/github/Hello-World.git",
"clone_url": "https://github.com/github/Hello-World.git",
"svn_url": "https://github.com/github/Hello-World",
"homepage": null,
"size": 6,
"stargazers_count": 0,
"watchers_count": 0,
"language": null,
"has_issues": true,
"has_projects": true,
"has_downloads": true,
"has_wiki": true,
"has_pages": false,
"has_discussions": false,
"forks_count": 0,
"mirror_url": null,
"archived": false,
"disabled": false,
"open_issues_count": 3,
"license": null,
"allow_forking": true,
"is_template": false,
"web_commit_signoff_required": false,
"topics": [],
"visibility": "public",
"forks": 0,
"open_issues": 3,
"watchers": 0,
"default_branch": "main"
}
},
"base": {
"label": "github:branch-0f4ceb14cbe39e4786ffbabb776da599",
"ref": "branch-0f4ceb14cbe39e4786ffbabb776da599",
"sha": "9a9f5a8d77bdc2540412900d3c930fe36a82b5ed",
"user": {
"login": "github",
"id": 5,
"node_id": "O_kgAF",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/github",
"html_url": "https://github.com/github",
"followers_url": "https://api.github.com/users/github/followers",
"following_url": "https://api.github.com/users/github/following{/other_user}",
"gists_url": "https://api.github.com/users/github/gists{/gist_id}",
"starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/github/subscriptions",
"organizations_url": "https://api.github.com/users/github/orgs",
"repos_url": "https://api.github.com/users/github/repos",
"events_url": "https://api.github.com/users/github/events{/privacy}",
"received_events_url": "https://api.github.com/users/github/received_events",
"type": "Organization",
"user_view_type": "public",
"site_admin": false
},
"repo": {
"id": 1,
"node_id": "R_kgAB",
"name": "Hello-World",
"full_name": "github/Hello-World",
"private": false,
"owner": {
"login": "github",
"id": 5,
"node_id": "O_kgAF",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/github",
"html_url": "https://github.com/github",
"followers_url": "https://api.github.com/users/github/followers",
"following_url": "https://api.github.com/users/github/following{/other_user}",
"gists_url": "https://api.github.com/users/github/gists{/gist_id}",
"starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/github/subscriptions",
"organizations_url": "https://api.github.com/users/github/orgs",
"repos_url": "https://api.github.com/users/github/repos",
"events_url": "https://api.github.com/users/github/events{/privacy}",
"received_events_url": "https://api.github.com/users/github/received_events",
"type": "Organization",
"user_view_type": "public",
"site_admin": false
},
"html_url": "https://github.com/github/Hello-World",
"description": null,
"fork": false,
"url": "https://api.github.com/repos/github/Hello-World",
"forks_url": "https://api.github.com/repos/github/Hello-World/forks",
"keys_url": "https://api.github.com/repos/github/Hello-World/keys{/key_id}",
"collaborators_url": "https://api.github.com/repos/github/Hello-World/collaborators{/collaborator}",
"teams_url": "https://api.github.com/repos/github/Hello-World/teams",
"hooks_url": "https://api.github.com/repos/github/Hello-World/hooks",
"issue_events_url": "https://api.github.com/repos/github/Hello-World/issues/events{/number}",
"events_url": "https://api.github.com/repos/github/Hello-World/events",
"assignees_url": "https://api.github.com/repos/github/Hello-World/assignees{/user}",
"branches_url": "https://api.github.com/repos/github/Hello-World/branches{/branch}",
"tags_url": "https://api.github.com/repos/github/Hello-World/tags",
"blobs_url": "https://api.github.com/repos/github/Hello-World/git/blobs{/sha}",
"git_tags_url": "https://api.github.com/repos/github/Hello-World/git/tags{/sha}",
"git_refs_url": "https://api.github.com/repos/github/Hello-World/git/refs{/sha}",
"trees_url": "https://api.github.com/repos/github/Hello-World/git/trees{/sha}",
"statuses_url": "https://api.github.com/repos/github/Hello-World/statuses/{sha}",
"languages_url": "https://api.github.com/repos/github/Hello-World/languages",
"stargazers_url": "https://api.github.com/repos/github/Hello-World/stargazers",
"contributors_url": "https://api.github.com/repos/github/Hello-World/contributors",
"subscribers_url": "https://api.github.com/repos/github/Hello-World/subscribers",
"subscription_url": "https://api.github.com/repos/github/Hello-World/subscription",
"commits_url": "https://api.github.com/repos/github/Hello-World/commits{/sha}",
"git_commits_url": "https://api.github.com/repos/github/Hello-World/git/commits{/sha}",
"comments_url": "https://api.github.com/repos/github/Hello-World/comments{/number}",
"issue_comment_url": "https://api.github.com/repos/github/Hello-World/issues/comments{/number}",
"contents_url": "https://api.github.com/repos/github/Hello-World/contents/{+path}",
"compare_url": "https://api.github.com/repos/github/Hello-World/compare/{base}...{head}",
"merges_url": "https://api.github.com/repos/github/Hello-World/merges",
"archive_url": "https://api.github.com/repos/github/Hello-World/{archive_format}{/ref}",
"downloads_url": "https://api.github.com/repos/github/Hello-World/downloads",
"issues_url": "https://api.github.com/repos/github/Hello-World/issues{/number}",
"pulls_url": "https://api.github.com/repos/github/Hello-World/pulls{/number}",
"milestones_url": "https://api.github.com/repos/github/Hello-World/milestones{/number}",
"notifications_url": "https://api.github.com/repos/github/Hello-World/notifications{?since,all,participating}",
"labels_url": "https://api.github.com/repos/github/Hello-World/labels{/name}",
"releases_url": "https://api.github.com/repos/github/Hello-World/releases{/id}",
"deployments_url": "https://api.github.com/repos/github/Hello-World/deployments",
"created_at": "2025-08-01T18:44:14Z",
"updated_at": "2025-08-01T18:48:38Z",
"pushed_at": "2025-08-01T18:44:50Z",
"git_url": "git://github.localhost/github/Hello-World.git",
"ssh_url": "ssh://git@localhost:3035/github/Hello-World.git",
"clone_url": "https://github.com/github/Hello-World.git",
"svn_url": "https://github.com/github/Hello-World",
"homepage": null,
"size": 6,
"stargazers_count": 0,
"watchers_count": 0,
"language": null,
"has_issues": true,
"has_projects": true,
"has_downloads": true,
"has_wiki": true,
"has_pages": false,
"has_discussions": false,
"forks_count": 0,
"mirror_url": null,
"archived": false,
"disabled": false,
"open_issues_count": 3,
"license": null,
"allow_forking": true,
"is_template": false,
"web_commit_signoff_required": false,
"topics": [],
"visibility": "public",
"forks": 0,
"open_issues": 3,
"watchers": 0,
"default_branch": "main"
}
},
"_links": {
"self": {
"href": "https://api.github.com/repos/github/Hello-World/pulls/6"
},
"html": {
"href": "https://github.com/github/Hello-World/pull/6"
},
"issue": {
"href": "https://api.github.com/repos/github/Hello-World/issues/6"
},
"comments": {
"href": "https://api.github.com/repos/github/Hello-World/issues/6/comments"
},
"review_comments": {
"href": "https://api.github.com/repos/github/Hello-World/pulls/6/comments"
},
"review_comment": {
"href": "https://api.github.com/repos/github/Hello-World/pulls/comments{/number}"
},
"commits": {
"href": "https://api.github.com/repos/github/Hello-World/pulls/6/commits"
},
"statuses": {
"href": "https://api.github.com/repos/github/Hello-World/statuses/a3258d3434ecb2058b2784c8eb8610c2e9937a0d"
}
},
"author_association": "MEMBER",
"auto_merge": null,
"active_lock_reason": null
},
"content_type": "PullRequest",
"creator": {
"login": "monalisa",
"id": 2,
"node_id": "U_kgAC",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/monalisa",
"html_url": "https://github.com/monalisa",
"followers_url": "https://api.github.com/users/monalisa/followers",
"following_url": "https://api.github.com/users/monalisa/following{/other_user}",
"gists_url": "https://api.github.com/users/monalisa/gists{/gist_id}",
"starred_url": "https://api.github.com/users/monalisa/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/monalisa/subscriptions",
"organizations_url": "https://api.github.com/users/monalisa/orgs",
"repos_url": "https://api.github.com/users/monalisa/repos",
"events_url": "https://api.github.com/users/monalisa/events{/privacy}",
"received_events_url": "https://api.github.com/users/monalisa/received_events",
"type": "User",
"user_view_type": "public",
"site_admin": false
},
"created_at": "2025-08-01T18:44:51Z",
"updated_at": "2025-08-06T19:25:18Z",
"archived_at": null,
"item_url": "https://api.github.com/orgs/github/projectsV2/1/items/13",
"fields": [
{
"id": 1,
"name": "Title",
"type": "title",
"value": {
"raw": "It seemed to me that any civilization that had so far lost its head as to need to include a set of detailed instructions for use in a packet of toothpicks, was no longer a civilization in which I could live and stay sane.",
"html": "It seemed to me that any civilization that had so far lost its head as to need to include a set of detailed instructions for use in a packet of toothpicks, was no longer a civilization in which I could live and stay sane.",
"number": 6,
"url": "https://github.com/5/1/pull/6",
"issue_id": 12,
"state": "open",
"state_reason": null,
"is_draft": false
}
},
{
"id": 2,
"name": "Assignees",
"type": "assignees",
"value": [
{
"login": "octocat",
"id": 175,
"node_id": "U_kgDMrw",
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
"user_view_type": "public",
"site_admin": false
}
]
},
{
"id": 3,
"name": "Status",
"type": "single_select",
"value": {
"id": "98236657",
"name": {
"raw": "Done",
"html": "Done"
},
"color": "PURPLE",
"description": {
"raw": "This has been completed",
"html": "This has been completed"
}
}
},
{
"id": 4,
"name": "Labels",
"type": "labels",
"value": [
{
"id": 19,
"node_id": "LA_kwABEw",
"url": "https://api.github.com/repos/github/Hello-World/labels/bug%20:bug:",
"name": "bug :bug:",
"color": "efe24f",
"default": false,
"description": "Something isn't working"
},
{
"id": 26,
"node_id": "LA_kwABGg",
"url": "https://api.github.com/repos/github/Hello-World/labels/fun%20size%20%F0%9F%8D%AB",
"name": "fun size 🍫",
"color": "f29c24",
"default": false,
"description": "Extra attention is needed"
},
{
"id": 33,
"node_id": "LA_kwABIQ",
"url": "https://api.github.com/repos/github/Hello-World/labels/%F0%9F%9A%92%20wontfix",
"name": "🚒 wontfix",
"color": "5891ce",
"default": false,
"description": "This will not be worked on"
}
]
},
{
"id": 5,
"name": "Linked pull requests",
"type": "linked_pull_requests",
"value": []
},
{
"id": 6,
"name": "Milestone",
"type": "milestone",
"value": {
"url": "https://api.github.com/repos/github/Hello-World/milestones/1",
"html_url": "https://github.com/github/Hello-World/milestone/1",
"labels_url": "https://api.github.com/repos/github/Hello-World/milestones/1/labels",
"id": 1,
"node_id": "MI_kwABAQ",
"number": 1,
"title": "Open milestone",
"description": null,
"creator": {
"login": "octocat",
"id": 175,
"node_id": "U_kgDMrw",
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
"user_view_type": "public",
"site_admin": false
},
"open_issues": 2,
"closed_issues": 1,
"state": "open",
"created_at": "2025-08-01T18:44:30Z",
"updated_at": "2025-08-06T19:14:15Z",
"due_on": null,
"closed_at": null
}
},
{
"id": 7,
"name": "Repository",
"type": "repository",
"value": {
"id": 1,
"node_id": "R_kgAB",
"name": "Hello-World",
"full_name": "github/Hello-World",
"private": false,
"owner": {
"login": "github",
"id": 5,
"node_id": "O_kgAF",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/github",
"html_url": "https://github.com/github",
"followers_url": "https://api.github.com/users/github/followers",
"following_url": "https://api.github.com/users/github/following{/other_user}",
"gists_url": "https://api.github.com/users/github/gists{/gist_id}",
"starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/github/subscriptions",
"organizations_url": "https://api.github.com/users/github/orgs",
"repos_url": "https://api.github.com/users/github/repos",
"events_url": "https://api.github.com/users/github/events{/privacy}",
"received_events_url": "https://api.github.com/users/github/received_events",
"type": "Organization",
"user_view_type": "public",
"site_admin": false
},
"html_url": "https://github.com/github/Hello-World",
"description": null,
"fork": false,
"url": "https://api.github.com/repos/github/Hello-World",
"forks_url": "https://api.github.com/repos/github/Hello-World/forks",
"keys_url": "https://api.github.com/repos/github/Hello-World/keys{/key_id}",
"collaborators_url": "https://api.github.com/repos/github/Hello-World/collaborators{/collaborator}",
"teams_url": "https://api.github.com/repos/github/Hello-World/teams",
"hooks_url": "https://api.github.com/repos/github/Hello-World/hooks",
"issue_events_url": "https://api.github.com/repos/github/Hello-World/issues/events{/number}",
"events_url": "https://api.github.com/repos/github/Hello-World/events",
"assignees_url": "https://api.github.com/repos/github/Hello-World/assignees{/user}",
"branches_url": "https://api.github.com/repos/github/Hello-World/branches{/branch}",
"tags_url": "https://api.github.com/repos/github/Hello-World/tags",
"blobs_url": "https://api.github.com/repos/github/Hello-World/git/blobs{/sha}",
"git_tags_url": "https://api.github.com/repos/github/Hello-World/git/tags{/sha}",
"git_refs_url": "https://api.github.com/repos/github/Hello-World/git/refs{/sha}",
"trees_url": "https://api.github.com/repos/github/Hello-World/git/trees{/sha}",
"statuses_url": "https://api.github.com/repos/github/Hello-World/statuses/{sha}",
"languages_url": "https://api.github.com/repos/github/Hello-World/languages",
"stargazers_url": "https://api.github.com/repos/github/Hello-World/stargazers",
"contributors_url": "https://api.github.com/repos/github/Hello-World/contributors",
"subscribers_url": "https://api.github.com/repos/github/Hello-World/subscribers",
"subscription_url": "https://api.github.com/repos/github/Hello-World/subscription",
"commits_url": "https://api.github.com/repos/github/Hello-World/commits{/sha}",
"git_commits_url": "https://api.github.com/repos/github/Hello-World/git/commits{/sha}",
"comments_url": "https://api.github.com/repos/github/Hello-World/comments{/number}",
"issue_comment_url": "https://api.github.com/repos/github/Hello-World/issues/comments{/number}",
"contents_url": "https://api.github.com/repos/github/Hello-World/contents/{+path}",
"compare_url": "https://api.github.com/repos/github/Hello-World/compare/{base}...{head}",
"merges_url": "https://api.github.com/repos/github/Hello-World/merges",
"archive_url": "https://api.github.com/repos/github/Hello-World/{archive_format}{/ref}",
"downloads_url": "https://api.github.com/repos/github/Hello-World/downloads",
"issues_url": "https://api.github.com/repos/github/Hello-World/issues{/number}",
"pulls_url": "https://api.github.com/repos/github/Hello-World/pulls{/number}",
"milestones_url": "https://api.github.com/repos/github/Hello-World/milestones{/number}",
"notifications_url": "https://api.github.com/repos/github/Hello-World/notifications{?since,all,participating}",
"labels_url": "https://api.github.com/repos/github/Hello-World/labels{/name}",
"releases_url": "https://api.github.com/repos/github/Hello-World/releases{/id}",
"deployments_url": "https://api.github.com/repos/github/Hello-World/deployments"
}
},
{
"id": 8,
"name": "Type",
"type": "issue_type",
"value": null
},
{
"id": 9,
"name": "Reviewers",
"type": "reviewers",
"value": [
{
"type": "ReviewRequest",
"status": "pending",
"reviewer": {
"avatarUrl": "https://github.com/images/error/octocat_happy.gif",
"id": 2,
"login": "monalisa",
"url": "https://github.com/monalisa",
"name": "monalisa",
"type": "User"
}
}
]
},
{
"id": 10,
"name": "Parent issue",
"type": "parent_issue",
"value": null
},
{
"id": 11,
"name": "Sub-issues progress",
"type": "sub_issues_progress",
"value": null
}
]
}`

## List items for a user owned project

List all items for a specific user-owned project accessible by the authenticated user.

### Fine-grained access tokens for "List items for a user owned project"

This endpoint does not work with GitHub App user access tokens, GitHub App installation access tokens, or fine-grained personal access tokens.

### Parameters for "List items for a user owned project"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| project_numberintegerRequiredThe project's number. |
| usernamestringRequiredThe handle for the GitHub user account. |

| Name, Type, Description |
| --- |
| beforestringA cursor, as given in theLink header. If specified, the query only searches for results before this cursor. For more information, see "Using pagination in the REST API." |
| afterstringA cursor, as given in theLink header. If specified, the query only searches for results after this cursor. For more information, see "Using pagination in the REST API." |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| qstringSearch query to filter items, seeFiltering projectsfor more information. |
| fieldsLimit results to specific fields, by their IDs. If not specified, the title field will be returned.Example:fields[]=123&fields[]=456&fields[]=789orfields=123,456,789 |

### HTTP response status codes for "List items for a user owned project"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 304 | Not modified |
| 401 | Requires authentication |
| 403 | Forbidden |

### Code samples for "List items for a user owned project"

#### Request example

get/users/{username}/projectsV2/{project_number}/items

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/users/USERNAME/projectsV2/PROJECT_NUMBER/items`

Response

-
-

`Status: 200``{
"id": 13,
"node_id": "PVTI_lAAFAQ0",
"project_url": "https://api.github.com/orgs/github/projectsV2/1",
"content": {
"url": "https://api.github.com/repos/github/Hello-World/pulls/6",
"id": 10,
"node_id": "PR_kwABCg",
"html_url": "https://github.com/github/Hello-World/pull/6",
"diff_url": "https://github.com/github/Hello-World/pull/6.diff",
"patch_url": "https://github.com/github/Hello-World/pull/6.patch",
"issue_url": "https://api.github.com/repos/github/Hello-World/issues/6",
"number": 6,
"state": "open",
"locked": false,
"title": "Issue title",
"user": {
"login": "monalisa",
"id": 161,
"node_id": "U_kgDMoQ",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/monalisa",
"html_url": "https://github.com/monalisa",
"followers_url": "https://api.github.com/users/monalisa/followers",
"following_url": "https://api.github.com/users/monalisa/following{/other_user}",
"gists_url": "https://api.github.com/users/monalisa/gists{/gist_id}",
"starred_url": "https://api.github.com/users/monalisa/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/monalisa/subscriptions",
"organizations_url": "https://api.github.com/users/monalisa/orgs",
"repos_url": "https://api.github.com/users/monalisa/repos",
"events_url": "https://api.github.com/users/monalisa/events{/privacy}",
"received_events_url": "https://api.github.com/users/monalisa/received_events",
"type": "User",
"user_view_type": "public",
"site_admin": false
},
"body": "Issue body",
"created_at": "2025-08-01T18:44:50Z",
"updated_at": "2025-08-06T19:25:18Z",
"closed_at": null,
"merged_at": null,
"merge_commit_sha": "98e25bad5878e54d22e5338cbc905dd2deedfa34",
"assignee": {
"login": "octocat",
"id": 175,
"node_id": "U_kgDMrw",
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
"user_view_type": "public",
"site_admin": false
},
"assignees": [
{
"login": "octocat",
"id": 175,
"node_id": "U_kgDMrw",
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
"user_view_type": "public",
"site_admin": false
}
],
"requested_reviewers": [
{
"login": "monalisa",
"id": 2,
"node_id": "U_kgAC",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/monalisa",
"html_url": "https://github.com/monalisa",
"followers_url": "https://api.github.com/users/monalisa/followers",
"following_url": "https://api.github.com/users/monalisa/following{/other_user}",
"gists_url": "https://api.github.com/users/monalisa/gists{/gist_id}",
"starred_url": "https://api.github.com/users/monalisa/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/monalisa/subscriptions",
"organizations_url": "https://api.github.com/users/monalisa/orgs",
"repos_url": "https://api.github.com/users/monalisa/repos",
"events_url": "https://api.github.com/users/monalisa/events{/privacy}",
"received_events_url": "https://api.github.com/users/monalisa/received_events",
"type": "User",
"user_view_type": "public",
"site_admin": false
}
],
"requested_teams": [],
"labels": [
{
"id": 19,
"node_id": "LA_kwABEw",
"url": "https://api.github.com/repos/github/Hello-World/labels/bug%20:bug:",
"name": "bug :bug:",
"color": "efe24f",
"default": false,
"description": "Something isn't working"
},
{
"id": 26,
"node_id": "LA_kwABGg",
"url": "https://api.github.com/repos/github/Hello-World/labels/fun%20size%20%F0%9F%8D%AB",
"name": "fun size 🍫",
"color": "f29c24",
"default": false,
"description": "Extra attention is needed"
},
{
"id": 33,
"node_id": "LA_kwABIQ",
"url": "https://api.github.com/repos/github/Hello-World/labels/%F0%9F%9A%92%20wontfix",
"name": "🚒 wontfix",
"color": "5891ce",
"default": false,
"description": "This will not be worked on"
}
],
"milestone": {
"url": "https://api.github.com/repos/github/Hello-World/milestones/1",
"html_url": "https://github.com/github/Hello-World/milestone/1",
"labels_url": "https://api.github.com/repos/github/Hello-World/milestones/1/labels",
"id": 1,
"node_id": "MI_kwABAQ",
"number": 1,
"title": "Open milestone",
"description": null,
"creator": {
"login": "monalisa",
"id": 2,
"node_id": "U_kgAC",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/monalisa",
"html_url": "https://github.com/monalisa",
"followers_url": "https://api.github.com/users/monalisa/followers",
"following_url": "https://api.github.com/users/monalisa/following{/other_user}",
"gists_url": "https://api.github.com/users/monalisa/gists{/gist_id}",
"starred_url": "https://api.github.com/users/monalisa/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/monalisa/subscriptions",
"organizations_url": "https://api.github.com/users/monalisa/orgs",
"repos_url": "https://api.github.com/users/monalisa/repos",
"events_url": "https://api.github.com/users/monalisa/events{/privacy}",
"received_events_url": "https://api.github.com/users/monalisa/received_events",
"type": "User",
"user_view_type": "public",
"site_admin": false
},
"open_issues": 2,
"closed_issues": 1,
"state": "open",
"created_at": "2025-08-01T18:44:30Z",
"updated_at": "2025-08-06T19:14:15Z",
"due_on": null,
"closed_at": null
},
"draft": false,
"commits_url": "https://api.github.com/repos/github/Hello-World/pulls/6/commits",
"review_comments_url": "https://api.github.com/repos/github/Hello-World/pulls/6/comments",
"review_comment_url": "https://api.github.com/repos/github/Hello-World/pulls/comments{/number}",
"comments_url": "https://api.github.com/repos/github/Hello-World/issues/6/comments",
"statuses_url": "https://api.github.com/repos/github/Hello-World/statuses/a3258d3434ecb2058b2784c8eb8610c2e9937a0d",
"head": {
"label": "github:branch-2ee3da8fde8a1adfe6d0809a1a414e4f",
"ref": "branch-2ee3da8fde8a1adfe6d0809a1a414e4f",
"sha": "a3258d3434ecb2058b2784c8eb8610c2e9937a0d",
"user": {
"login": "github",
"id": 5,
"node_id": "O_kgAF",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/github",
"html_url": "https://github.com/github",
"followers_url": "https://api.github.com/users/github/followers",
"following_url": "https://api.github.com/users/github/following{/other_user}",
"gists_url": "https://api.github.com/users/github/gists{/gist_id}",
"starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/github/subscriptions",
"organizations_url": "https://api.github.com/users/github/orgs",
"repos_url": "https://api.github.com/users/github/repos",
"events_url": "https://api.github.com/users/github/events{/privacy}",
"received_events_url": "https://api.github.com/users/github/received_events",
"type": "Organization",
"user_view_type": "public",
"site_admin": false
},
"repo": {
"id": 1,
"node_id": "R_kgAB",
"name": "Hello-World",
"full_name": "github/Hello-World",
"private": false,
"owner": {
"login": "github",
"id": 5,
"node_id": "O_kgAF",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/github",
"html_url": "https://github.com/github",
"followers_url": "https://api.github.com/users/github/followers",
"following_url": "https://api.github.com/users/github/following{/other_user}",
"gists_url": "https://api.github.com/users/github/gists{/gist_id}",
"starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/github/subscriptions",
"organizations_url": "https://api.github.com/users/github/orgs",
"repos_url": "https://api.github.com/users/github/repos",
"events_url": "https://api.github.com/users/github/events{/privacy}",
"received_events_url": "https://api.github.com/users/github/received_events",
"type": "Organization",
"user_view_type": "public",
"site_admin": false
},
"html_url": "https://github.com/github/Hello-World",
"description": null,
"fork": false,
"url": "https://api.github.com/repos/github/Hello-World",
"forks_url": "https://api.github.com/repos/github/Hello-World/forks",
"keys_url": "https://api.github.com/repos/github/Hello-World/keys{/key_id}",
"collaborators_url": "https://api.github.com/repos/github/Hello-World/collaborators{/collaborator}",
"teams_url": "https://api.github.com/repos/github/Hello-World/teams",
"hooks_url": "https://api.github.com/repos/github/Hello-World/hooks",
"issue_events_url": "https://api.github.com/repos/github/Hello-World/issues/events{/number}",
"events_url": "https://api.github.com/repos/github/Hello-World/events",
"assignees_url": "https://api.github.com/repos/github/Hello-World/assignees{/user}",
"branches_url": "https://api.github.com/repos/github/Hello-World/branches{/branch}",
"tags_url": "https://api.github.com/repos/github/Hello-World/tags",
"blobs_url": "https://api.github.com/repos/github/Hello-World/git/blobs{/sha}",
"git_tags_url": "https://api.github.com/repos/github/Hello-World/git/tags{/sha}",
"git_refs_url": "https://api.github.com/repos/github/Hello-World/git/refs{/sha}",
"trees_url": "https://api.github.com/repos/github/Hello-World/git/trees{/sha}",
"statuses_url": "https://api.github.com/repos/github/Hello-World/statuses/{sha}",
"languages_url": "https://api.github.com/repos/github/Hello-World/languages",
"stargazers_url": "https://api.github.com/repos/github/Hello-World/stargazers",
"contributors_url": "https://api.github.com/repos/github/Hello-World/contributors",
"subscribers_url": "https://api.github.com/repos/github/Hello-World/subscribers",
"subscription_url": "https://api.github.com/repos/github/Hello-World/subscription",
"commits_url": "https://api.github.com/repos/github/Hello-World/commits{/sha}",
"git_commits_url": "https://api.github.com/repos/github/Hello-World/git/commits{/sha}",
"comments_url": "https://api.github.com/repos/github/Hello-World/comments{/number}",
"issue_comment_url": "https://api.github.com/repos/github/Hello-World/issues/comments{/number}",
"contents_url": "https://api.github.com/repos/github/Hello-World/contents/{+path}",
"compare_url": "https://api.github.com/repos/github/Hello-World/compare/{base}...{head}",
"merges_url": "https://api.github.com/repos/github/Hello-World/merges",
"archive_url": "https://api.github.com/repos/github/Hello-World/{archive_format}{/ref}",
"downloads_url": "https://api.github.com/repos/github/Hello-World/downloads",
"issues_url": "https://api.github.com/repos/github/Hello-World/issues{/number}",
"pulls_url": "https://api.github.com/repos/github/Hello-World/pulls{/number}",
"milestones_url": "https://api.github.com/repos/github/Hello-World/milestones{/number}",
"notifications_url": "https://api.github.com/repos/github/Hello-World/notifications{?since,all,participating}",
"labels_url": "https://api.github.com/repos/github/Hello-World/labels{/name}",
"releases_url": "https://api.github.com/repos/github/Hello-World/releases{/id}",
"deployments_url": "https://api.github.com/repos/github/Hello-World/deployments",
"created_at": "2025-08-01T18:44:14Z",
"updated_at": "2025-08-01T18:48:38Z",
"pushed_at": "2025-08-01T18:44:50Z",
"git_url": "git://github.localhost/github/Hello-World.git",
"ssh_url": "ssh://git@localhost:3035/github/Hello-World.git",
"clone_url": "https://github.com/github/Hello-World.git",
"svn_url": "https://github.com/github/Hello-World",
"homepage": null,
"size": 6,
"stargazers_count": 0,
"watchers_count": 0,
"language": null,
"has_issues": true,
"has_projects": true,
"has_downloads": true,
"has_wiki": true,
"has_pages": false,
"has_discussions": false,
"forks_count": 0,
"mirror_url": null,
"archived": false,
"disabled": false,
"open_issues_count": 3,
"license": null,
"allow_forking": true,
"is_template": false,
"web_commit_signoff_required": false,
"topics": [],
"visibility": "public",
"forks": 0,
"open_issues": 3,
"watchers": 0,
"default_branch": "main"
}
},
"base": {
"label": "github:branch-0f4ceb14cbe39e4786ffbabb776da599",
"ref": "branch-0f4ceb14cbe39e4786ffbabb776da599",
"sha": "9a9f5a8d77bdc2540412900d3c930fe36a82b5ed",
"user": {
"login": "github",
"id": 5,
"node_id": "O_kgAF",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/github",
"html_url": "https://github.com/github",
"followers_url": "https://api.github.com/users/github/followers",
"following_url": "https://api.github.com/users/github/following{/other_user}",
"gists_url": "https://api.github.com/users/github/gists{/gist_id}",
"starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/github/subscriptions",
"organizations_url": "https://api.github.com/users/github/orgs",
"repos_url": "https://api.github.com/users/github/repos",
"events_url": "https://api.github.com/users/github/events{/privacy}",
"received_events_url": "https://api.github.com/users/github/received_events",
"type": "Organization",
"user_view_type": "public",
"site_admin": false
},
"repo": {
"id": 1,
"node_id": "R_kgAB",
"name": "Hello-World",
"full_name": "github/Hello-World",
"private": false,
"owner": {
"login": "github",
"id": 5,
"node_id": "O_kgAF",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/github",
"html_url": "https://github.com/github",
"followers_url": "https://api.github.com/users/github/followers",
"following_url": "https://api.github.com/users/github/following{/other_user}",
"gists_url": "https://api.github.com/users/github/gists{/gist_id}",
"starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/github/subscriptions",
"organizations_url": "https://api.github.com/users/github/orgs",
"repos_url": "https://api.github.com/users/github/repos",
"events_url": "https://api.github.com/users/github/events{/privacy}",
"received_events_url": "https://api.github.com/users/github/received_events",
"type": "Organization",
"user_view_type": "public",
"site_admin": false
},
"html_url": "https://github.com/github/Hello-World",
"description": null,
"fork": false,
"url": "https://api.github.com/repos/github/Hello-World",
"forks_url": "https://api.github.com/repos/github/Hello-World/forks",
"keys_url": "https://api.github.com/repos/github/Hello-World/keys{/key_id}",
"collaborators_url": "https://api.github.com/repos/github/Hello-World/collaborators{/collaborator}",
"teams_url": "https://api.github.com/repos/github/Hello-World/teams",
"hooks_url": "https://api.github.com/repos/github/Hello-World/hooks",
"issue_events_url": "https://api.github.com/repos/github/Hello-World/issues/events{/number}",
"events_url": "https://api.github.com/repos/github/Hello-World/events",
"assignees_url": "https://api.github.com/repos/github/Hello-World/assignees{/user}",
"branches_url": "https://api.github.com/repos/github/Hello-World/branches{/branch}",
"tags_url": "https://api.github.com/repos/github/Hello-World/tags",
"blobs_url": "https://api.github.com/repos/github/Hello-World/git/blobs{/sha}",
"git_tags_url": "https://api.github.com/repos/github/Hello-World/git/tags{/sha}",
"git_refs_url": "https://api.github.com/repos/github/Hello-World/git/refs{/sha}",
"trees_url": "https://api.github.com/repos/github/Hello-World/git/trees{/sha}",
"statuses_url": "https://api.github.com/repos/github/Hello-World/statuses/{sha}",
"languages_url": "https://api.github.com/repos/github/Hello-World/languages",
"stargazers_url": "https://api.github.com/repos/github/Hello-World/stargazers",
"contributors_url": "https://api.github.com/repos/github/Hello-World/contributors",
"subscribers_url": "https://api.github.com/repos/github/Hello-World/subscribers",
"subscription_url": "https://api.github.com/repos/github/Hello-World/subscription",
"commits_url": "https://api.github.com/repos/github/Hello-World/commits{/sha}",
"git_commits_url": "https://api.github.com/repos/github/Hello-World/git/commits{/sha}",
"comments_url": "https://api.github.com/repos/github/Hello-World/comments{/number}",
"issue_comment_url": "https://api.github.com/repos/github/Hello-World/issues/comments{/number}",
"contents_url": "https://api.github.com/repos/github/Hello-World/contents/{+path}",
"compare_url": "https://api.github.com/repos/github/Hello-World/compare/{base}...{head}",
"merges_url": "https://api.github.com/repos/github/Hello-World/merges",
"archive_url": "https://api.github.com/repos/github/Hello-World/{archive_format}{/ref}",
"downloads_url": "https://api.github.com/repos/github/Hello-World/downloads",
"issues_url": "https://api.github.com/repos/github/Hello-World/issues{/number}",
"pulls_url": "https://api.github.com/repos/github/Hello-World/pulls{/number}",
"milestones_url": "https://api.github.com/repos/github/Hello-World/milestones{/number}",
"notifications_url": "https://api.github.com/repos/github/Hello-World/notifications{?since,all,participating}",
"labels_url": "https://api.github.com/repos/github/Hello-World/labels{/name}",
"releases_url": "https://api.github.com/repos/github/Hello-World/releases{/id}",
"deployments_url": "https://api.github.com/repos/github/Hello-World/deployments",
"created_at": "2025-08-01T18:44:14Z",
"updated_at": "2025-08-01T18:48:38Z",
"pushed_at": "2025-08-01T18:44:50Z",
"git_url": "git://github.localhost/github/Hello-World.git",
"ssh_url": "ssh://git@localhost:3035/github/Hello-World.git",
"clone_url": "https://github.com/github/Hello-World.git",
"svn_url": "https://github.com/github/Hello-World",
"homepage": null,
"size": 6,
"stargazers_count": 0,
"watchers_count": 0,
"language": null,
"has_issues": true,
"has_projects": true,
"has_downloads": true,
"has_wiki": true,
"has_pages": false,
"has_discussions": false,
"forks_count": 0,
"mirror_url": null,
"archived": false,
"disabled": false,
"open_issues_count": 3,
"license": null,
"allow_forking": true,
"is_template": false,
"web_commit_signoff_required": false,
"topics": [],
"visibility": "public",
"forks": 0,
"open_issues": 3,
"watchers": 0,
"default_branch": "main"
}
},
"_links": {
"self": {
"href": "https://api.github.com/repos/github/Hello-World/pulls/6"
},
"html": {
"href": "https://github.com/github/Hello-World/pull/6"
},
"issue": {
"href": "https://api.github.com/repos/github/Hello-World/issues/6"
},
"comments": {
"href": "https://api.github.com/repos/github/Hello-World/issues/6/comments"
},
"review_comments": {
"href": "https://api.github.com/repos/github/Hello-World/pulls/6/comments"
},
"review_comment": {
"href": "https://api.github.com/repos/github/Hello-World/pulls/comments{/number}"
},
"commits": {
"href": "https://api.github.com/repos/github/Hello-World/pulls/6/commits"
},
"statuses": {
"href": "https://api.github.com/repos/github/Hello-World/statuses/a3258d3434ecb2058b2784c8eb8610c2e9937a0d"
}
},
"author_association": "MEMBER",
"auto_merge": null,
"active_lock_reason": null
},
"content_type": "PullRequest",
"creator": {
"login": "monalisa",
"id": 2,
"node_id": "U_kgAC",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/monalisa",
"html_url": "https://github.com/monalisa",
"followers_url": "https://api.github.com/users/monalisa/followers",
"following_url": "https://api.github.com/users/monalisa/following{/other_user}",
"gists_url": "https://api.github.com/users/monalisa/gists{/gist_id}",
"starred_url": "https://api.github.com/users/monalisa/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/monalisa/subscriptions",
"organizations_url": "https://api.github.com/users/monalisa/orgs",
"repos_url": "https://api.github.com/users/monalisa/repos",
"events_url": "https://api.github.com/users/monalisa/events{/privacy}",
"received_events_url": "https://api.github.com/users/monalisa/received_events",
"type": "User",
"user_view_type": "public",
"site_admin": false
},
"created_at": "2025-08-01T18:44:51Z",
"updated_at": "2025-08-06T19:25:18Z",
"archived_at": null,
"item_url": "https://api.github.com/orgs/github/projectsV2/1/items/13",
"fields": [
{
"id": 1,
"name": "Title",
"type": "title",
"value": {
"raw": "It seemed to me that any civilization that had so far lost its head as to need to include a set of detailed instructions for use in a packet of toothpicks, was no longer a civilization in which I could live and stay sane.",
"html": "It seemed to me that any civilization that had so far lost its head as to need to include a set of detailed instructions for use in a packet of toothpicks, was no longer a civilization in which I could live and stay sane.",
"number": 6,
"url": "https://github.com/5/1/pull/6",
"issue_id": 12,
"state": "open",
"state_reason": null,
"is_draft": false
}
},
{
"id": 2,
"name": "Assignees",
"type": "assignees",
"value": [
{
"login": "octocat",
"id": 175,
"node_id": "U_kgDMrw",
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
"user_view_type": "public",
"site_admin": false
}
]
},
{
"id": 3,
"name": "Status",
"type": "single_select",
"value": {
"id": "98236657",
"name": {
"raw": "Done",
"html": "Done"
},
"color": "PURPLE",
"description": {
"raw": "This has been completed",
"html": "This has been completed"
}
}
},
{
"id": 4,
"name": "Labels",
"type": "labels",
"value": [
{
"id": 19,
"node_id": "LA_kwABEw",
"url": "https://api.github.com/repos/github/Hello-World/labels/bug%20:bug:",
"name": "bug :bug:",
"color": "efe24f",
"default": false,
"description": "Something isn't working"
},
{
"id": 26,
"node_id": "LA_kwABGg",
"url": "https://api.github.com/repos/github/Hello-World/labels/fun%20size%20%F0%9F%8D%AB",
"name": "fun size 🍫",
"color": "f29c24",
"default": false,
"description": "Extra attention is needed"
},
{
"id": 33,
"node_id": "LA_kwABIQ",
"url": "https://api.github.com/repos/github/Hello-World/labels/%F0%9F%9A%92%20wontfix",
"name": "🚒 wontfix",
"color": "5891ce",
"default": false,
"description": "This will not be worked on"
}
]
},
{
"id": 5,
"name": "Linked pull requests",
"type": "linked_pull_requests",
"value": []
},
{
"id": 6,
"name": "Milestone",
"type": "milestone",
"value": {
"url": "https://api.github.com/repos/github/Hello-World/milestones/1",
"html_url": "https://github.com/github/Hello-World/milestone/1",
"labels_url": "https://api.github.com/repos/github/Hello-World/milestones/1/labels",
"id": 1,
"node_id": "MI_kwABAQ",
"number": 1,
"title": "Open milestone",
"description": null,
"creator": {
"login": "octocat",
"id": 175,
"node_id": "U_kgDMrw",
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
"user_view_type": "public",
"site_admin": false
},
"open_issues": 2,
"closed_issues": 1,
"state": "open",
"created_at": "2025-08-01T18:44:30Z",
"updated_at": "2025-08-06T19:14:15Z",
"due_on": null,
"closed_at": null
}
},
{
"id": 7,
"name": "Repository",
"type": "repository",
"value": {
"id": 1,
"node_id": "R_kgAB",
"name": "Hello-World",
"full_name": "github/Hello-World",
"private": false,
"owner": {
"login": "github",
"id": 5,
"node_id": "O_kgAF",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/github",
"html_url": "https://github.com/github",
"followers_url": "https://api.github.com/users/github/followers",
"following_url": "https://api.github.com/users/github/following{/other_user}",
"gists_url": "https://api.github.com/users/github/gists{/gist_id}",
"starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/github/subscriptions",
"organizations_url": "https://api.github.com/users/github/orgs",
"repos_url": "https://api.github.com/users/github/repos",
"events_url": "https://api.github.com/users/github/events{/privacy}",
"received_events_url": "https://api.github.com/users/github/received_events",
"type": "Organization",
"user_view_type": "public",
"site_admin": false
},
"html_url": "https://github.com/github/Hello-World",
"description": null,
"fork": false,
"url": "https://api.github.com/repos/github/Hello-World",
"forks_url": "https://api.github.com/repos/github/Hello-World/forks",
"keys_url": "https://api.github.com/repos/github/Hello-World/keys{/key_id}",
"collaborators_url": "https://api.github.com/repos/github/Hello-World/collaborators{/collaborator}",
"teams_url": "https://api.github.com/repos/github/Hello-World/teams",
"hooks_url": "https://api.github.com/repos/github/Hello-World/hooks",
"issue_events_url": "https://api.github.com/repos/github/Hello-World/issues/events{/number}",
"events_url": "https://api.github.com/repos/github/Hello-World/events",
"assignees_url": "https://api.github.com/repos/github/Hello-World/assignees{/user}",
"branches_url": "https://api.github.com/repos/github/Hello-World/branches{/branch}",
"tags_url": "https://api.github.com/repos/github/Hello-World/tags",
"blobs_url": "https://api.github.com/repos/github/Hello-World/git/blobs{/sha}",
"git_tags_url": "https://api.github.com/repos/github/Hello-World/git/tags{/sha}",
"git_refs_url": "https://api.github.com/repos/github/Hello-World/git/refs{/sha}",
"trees_url": "https://api.github.com/repos/github/Hello-World/git/trees{/sha}",
"statuses_url": "https://api.github.com/repos/github/Hello-World/statuses/{sha}",
"languages_url": "https://api.github.com/repos/github/Hello-World/languages",
"stargazers_url": "https://api.github.com/repos/github/Hello-World/stargazers",
"contributors_url": "https://api.github.com/repos/github/Hello-World/contributors",
"subscribers_url": "https://api.github.com/repos/github/Hello-World/subscribers",
"subscription_url": "https://api.github.com/repos/github/Hello-World/subscription",
"commits_url": "https://api.github.com/repos/github/Hello-World/commits{/sha}",
"git_commits_url": "https://api.github.com/repos/github/Hello-World/git/commits{/sha}",
"comments_url": "https://api.github.com/repos/github/Hello-World/comments{/number}",
"issue_comment_url": "https://api.github.com/repos/github/Hello-World/issues/comments{/number}",
"contents_url": "https://api.github.com/repos/github/Hello-World/contents/{+path}",
"compare_url": "https://api.github.com/repos/github/Hello-World/compare/{base}...{head}",
"merges_url": "https://api.github.com/repos/github/Hello-World/merges",
"archive_url": "https://api.github.com/repos/github/Hello-World/{archive_format}{/ref}",
"downloads_url": "https://api.github.com/repos/github/Hello-World/downloads",
"issues_url": "https://api.github.com/repos/github/Hello-World/issues{/number}",
"pulls_url": "https://api.github.com/repos/github/Hello-World/pulls{/number}",
"milestones_url": "https://api.github.com/repos/github/Hello-World/milestones{/number}",
"notifications_url": "https://api.github.com/repos/github/Hello-World/notifications{?since,all,participating}",
"labels_url": "https://api.github.com/repos/github/Hello-World/labels{/name}",
"releases_url": "https://api.github.com/repos/github/Hello-World/releases{/id}",
"deployments_url": "https://api.github.com/repos/github/Hello-World/deployments"
}
},
{
"id": 8,
"name": "Type",
"type": "issue_type",
"value": null
},
{
"id": 9,
"name": "Reviewers",
"type": "reviewers",
"value": [
{
"type": "ReviewRequest",
"status": "pending",
"reviewer": {
"avatarUrl": "https://github.com/images/error/octocat_happy.gif",
"id": 2,
"login": "monalisa",
"url": "https://github.com/monalisa",
"name": "monalisa",
"type": "User"
}
}
]
},
{
"id": 10,
"name": "Parent issue",
"type": "parent_issue",
"value": null
},
{
"id": 11,
"name": "Sub-issues progress",
"type": "sub_issues_progress",
"value": null
}
]
}`

## Add item to user owned project

Add an issue or pull request item to the specified user owned project.

### Fine-grained access tokens for "Add item to user owned project"

This endpoint does not work with GitHub App user access tokens, GitHub App installation access tokens, or fine-grained personal access tokens.

### Parameters for "Add item to user owned project"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| usernamestringRequiredThe handle for the GitHub user account. |
| project_numberintegerRequiredThe project's number. |

### HTTP response status codes for "Add item to user owned project"

| Status code | Description |
| --- | --- |
| 201 | Created |
| 304 | Not modified |
| 401 | Requires authentication |
| 403 | Forbidden |

### Code samples for "Add item to user owned project"

#### Request examples

Select the example typeAdd an issue using its unique IDAdd a pull request using its unique IDAdd an issue using repository owner, name, and issue numberAdd a pull request using repository owner, name, and PR numberpost/users/{username}/projectsV2/{project_number}/items

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/users/USERNAME/projectsV2/PROJECT_NUMBER/items \
  -d '{"type":"Issue","id":3}'`

Response for adding an issue using its unique ID

-
-

`Status: 201``{
"value": {
"id": 17,
"node_id": "PVTI_lADOANN5s84ACbL0zgBueEI",
"content": {
"id": 38,
"node_id": "I_kwDOANN5s85FtLts",
"title": "Example Draft Issue",
"body": "This is a draft issue in the project.",
"created_at": "2022-04-28T12:00:00Z",
"updated_at": "2022-04-28T12:00:00Z",
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
"content_type": "DraftIssue",
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
"archived_at": null,
"project_url": "https://api.github.com/users/octocat/projectsV2/1",
"item_url": "https://api.github.com/users/octocat/projectsV2/items/17"
}
}`

## Get an item for a user owned project

Get a specific item from a user-owned project.

### Fine-grained access tokens for "Get an item for a user owned project"

This endpoint does not work with GitHub App user access tokens, GitHub App installation access tokens, or fine-grained personal access tokens.

### Parameters for "Get an item for a user owned project"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| project_numberintegerRequiredThe project's number. |
| usernamestringRequiredThe handle for the GitHub user account. |
| item_idintegerRequiredThe unique identifier of the project item. |

| Name, Type, Description |
| --- |
| fieldsLimit results to specific fields, by their IDs. If not specified, the title field will be returned.Example: fields[]=123&fields[]=456&fields[]=789 or fields=123,456,789 |

### HTTP response status codes for "Get an item for a user owned project"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 304 | Not modified |
| 401 | Requires authentication |
| 403 | Forbidden |

### Code samples for "Get an item for a user owned project"

#### Request example

get/users/{username}/projectsV2/{project_number}/items/{item_id}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/users/USERNAME/projectsV2/PROJECT_NUMBER/items/ITEM_ID`

Response

-
-

`Status: 200``{
"id": 13,
"node_id": "PVTI_lAAFAQ0",
"project_url": "https://api.github.com/orgs/github/projectsV2/1",
"content": {
"url": "https://api.github.com/repos/github/Hello-World/pulls/6",
"id": 10,
"node_id": "PR_kwABCg",
"html_url": "https://github.com/github/Hello-World/pull/6",
"diff_url": "https://github.com/github/Hello-World/pull/6.diff",
"patch_url": "https://github.com/github/Hello-World/pull/6.patch",
"issue_url": "https://api.github.com/repos/github/Hello-World/issues/6",
"number": 6,
"state": "open",
"locked": false,
"title": "Issue title",
"user": {
"login": "monalisa",
"id": 161,
"node_id": "U_kgDMoQ",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/monalisa",
"html_url": "https://github.com/monalisa",
"followers_url": "https://api.github.com/users/monalisa/followers",
"following_url": "https://api.github.com/users/monalisa/following{/other_user}",
"gists_url": "https://api.github.com/users/monalisa/gists{/gist_id}",
"starred_url": "https://api.github.com/users/monalisa/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/monalisa/subscriptions",
"organizations_url": "https://api.github.com/users/monalisa/orgs",
"repos_url": "https://api.github.com/users/monalisa/repos",
"events_url": "https://api.github.com/users/monalisa/events{/privacy}",
"received_events_url": "https://api.github.com/users/monalisa/received_events",
"type": "User",
"user_view_type": "public",
"site_admin": false
},
"body": "Issue body",
"created_at": "2025-08-01T18:44:50Z",
"updated_at": "2025-08-06T19:25:18Z",
"closed_at": null,
"merged_at": null,
"merge_commit_sha": "98e25bad5878e54d22e5338cbc905dd2deedfa34",
"assignee": {
"login": "octocat",
"id": 175,
"node_id": "U_kgDMrw",
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
"user_view_type": "public",
"site_admin": false
},
"assignees": [
{
"login": "octocat",
"id": 175,
"node_id": "U_kgDMrw",
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
"user_view_type": "public",
"site_admin": false
}
],
"requested_reviewers": [
{
"login": "monalisa",
"id": 2,
"node_id": "U_kgAC",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/monalisa",
"html_url": "https://github.com/monalisa",
"followers_url": "https://api.github.com/users/monalisa/followers",
"following_url": "https://api.github.com/users/monalisa/following{/other_user}",
"gists_url": "https://api.github.com/users/monalisa/gists{/gist_id}",
"starred_url": "https://api.github.com/users/monalisa/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/monalisa/subscriptions",
"organizations_url": "https://api.github.com/users/monalisa/orgs",
"repos_url": "https://api.github.com/users/monalisa/repos",
"events_url": "https://api.github.com/users/monalisa/events{/privacy}",
"received_events_url": "https://api.github.com/users/monalisa/received_events",
"type": "User",
"user_view_type": "public",
"site_admin": false
}
],
"requested_teams": [],
"labels": [
{
"id": 19,
"node_id": "LA_kwABEw",
"url": "https://api.github.com/repos/github/Hello-World/labels/bug%20:bug:",
"name": "bug :bug:",
"color": "efe24f",
"default": false,
"description": "Something isn't working"
},
{
"id": 26,
"node_id": "LA_kwABGg",
"url": "https://api.github.com/repos/github/Hello-World/labels/fun%20size%20%F0%9F%8D%AB",
"name": "fun size 🍫",
"color": "f29c24",
"default": false,
"description": "Extra attention is needed"
},
{
"id": 33,
"node_id": "LA_kwABIQ",
"url": "https://api.github.com/repos/github/Hello-World/labels/%F0%9F%9A%92%20wontfix",
"name": "🚒 wontfix",
"color": "5891ce",
"default": false,
"description": "This will not be worked on"
}
],
"milestone": {
"url": "https://api.github.com/repos/github/Hello-World/milestones/1",
"html_url": "https://github.com/github/Hello-World/milestone/1",
"labels_url": "https://api.github.com/repos/github/Hello-World/milestones/1/labels",
"id": 1,
"node_id": "MI_kwABAQ",
"number": 1,
"title": "Open milestone",
"description": null,
"creator": {
"login": "monalisa",
"id": 2,
"node_id": "U_kgAC",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/monalisa",
"html_url": "https://github.com/monalisa",
"followers_url": "https://api.github.com/users/monalisa/followers",
"following_url": "https://api.github.com/users/monalisa/following{/other_user}",
"gists_url": "https://api.github.com/users/monalisa/gists{/gist_id}",
"starred_url": "https://api.github.com/users/monalisa/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/monalisa/subscriptions",
"organizations_url": "https://api.github.com/users/monalisa/orgs",
"repos_url": "https://api.github.com/users/monalisa/repos",
"events_url": "https://api.github.com/users/monalisa/events{/privacy}",
"received_events_url": "https://api.github.com/users/monalisa/received_events",
"type": "User",
"user_view_type": "public",
"site_admin": false
},
"open_issues": 2,
"closed_issues": 1,
"state": "open",
"created_at": "2025-08-01T18:44:30Z",
"updated_at": "2025-08-06T19:14:15Z",
"due_on": null,
"closed_at": null
},
"draft": false,
"commits_url": "https://api.github.com/repos/github/Hello-World/pulls/6/commits",
"review_comments_url": "https://api.github.com/repos/github/Hello-World/pulls/6/comments",
"review_comment_url": "https://api.github.com/repos/github/Hello-World/pulls/comments{/number}",
"comments_url": "https://api.github.com/repos/github/Hello-World/issues/6/comments",
"statuses_url": "https://api.github.com/repos/github/Hello-World/statuses/a3258d3434ecb2058b2784c8eb8610c2e9937a0d",
"head": {
"label": "github:branch-2ee3da8fde8a1adfe6d0809a1a414e4f",
"ref": "branch-2ee3da8fde8a1adfe6d0809a1a414e4f",
"sha": "a3258d3434ecb2058b2784c8eb8610c2e9937a0d",
"user": {
"login": "github",
"id": 5,
"node_id": "O_kgAF",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/github",
"html_url": "https://github.com/github",
"followers_url": "https://api.github.com/users/github/followers",
"following_url": "https://api.github.com/users/github/following{/other_user}",
"gists_url": "https://api.github.com/users/github/gists{/gist_id}",
"starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/github/subscriptions",
"organizations_url": "https://api.github.com/users/github/orgs",
"repos_url": "https://api.github.com/users/github/repos",
"events_url": "https://api.github.com/users/github/events{/privacy}",
"received_events_url": "https://api.github.com/users/github/received_events",
"type": "Organization",
"user_view_type": "public",
"site_admin": false
},
"repo": {
"id": 1,
"node_id": "R_kgAB",
"name": "Hello-World",
"full_name": "github/Hello-World",
"private": false,
"owner": {
"login": "github",
"id": 5,
"node_id": "O_kgAF",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/github",
"html_url": "https://github.com/github",
"followers_url": "https://api.github.com/users/github/followers",
"following_url": "https://api.github.com/users/github/following{/other_user}",
"gists_url": "https://api.github.com/users/github/gists{/gist_id}",
"starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/github/subscriptions",
"organizations_url": "https://api.github.com/users/github/orgs",
"repos_url": "https://api.github.com/users/github/repos",
"events_url": "https://api.github.com/users/github/events{/privacy}",
"received_events_url": "https://api.github.com/users/github/received_events",
"type": "Organization",
"user_view_type": "public",
"site_admin": false
},
"html_url": "https://github.com/github/Hello-World",
"description": null,
"fork": false,
"url": "https://api.github.com/repos/github/Hello-World",
"forks_url": "https://api.github.com/repos/github/Hello-World/forks",
"keys_url": "https://api.github.com/repos/github/Hello-World/keys{/key_id}",
"collaborators_url": "https://api.github.com/repos/github/Hello-World/collaborators{/collaborator}",
"teams_url": "https://api.github.com/repos/github/Hello-World/teams",
"hooks_url": "https://api.github.com/repos/github/Hello-World/hooks",
"issue_events_url": "https://api.github.com/repos/github/Hello-World/issues/events{/number}",
"events_url": "https://api.github.com/repos/github/Hello-World/events",
"assignees_url": "https://api.github.com/repos/github/Hello-World/assignees{/user}",
"branches_url": "https://api.github.com/repos/github/Hello-World/branches{/branch}",
"tags_url": "https://api.github.com/repos/github/Hello-World/tags",
"blobs_url": "https://api.github.com/repos/github/Hello-World/git/blobs{/sha}",
"git_tags_url": "https://api.github.com/repos/github/Hello-World/git/tags{/sha}",
"git_refs_url": "https://api.github.com/repos/github/Hello-World/git/refs{/sha}",
"trees_url": "https://api.github.com/repos/github/Hello-World/git/trees{/sha}",
"statuses_url": "https://api.github.com/repos/github/Hello-World/statuses/{sha}",
"languages_url": "https://api.github.com/repos/github/Hello-World/languages",
"stargazers_url": "https://api.github.com/repos/github/Hello-World/stargazers",
"contributors_url": "https://api.github.com/repos/github/Hello-World/contributors",
"subscribers_url": "https://api.github.com/repos/github/Hello-World/subscribers",
"subscription_url": "https://api.github.com/repos/github/Hello-World/subscription",
"commits_url": "https://api.github.com/repos/github/Hello-World/commits{/sha}",
"git_commits_url": "https://api.github.com/repos/github/Hello-World/git/commits{/sha}",
"comments_url": "https://api.github.com/repos/github/Hello-World/comments{/number}",
"issue_comment_url": "https://api.github.com/repos/github/Hello-World/issues/comments{/number}",
"contents_url": "https://api.github.com/repos/github/Hello-World/contents/{+path}",
"compare_url": "https://api.github.com/repos/github/Hello-World/compare/{base}...{head}",
"merges_url": "https://api.github.com/repos/github/Hello-World/merges",
"archive_url": "https://api.github.com/repos/github/Hello-World/{archive_format}{/ref}",
"downloads_url": "https://api.github.com/repos/github/Hello-World/downloads",
"issues_url": "https://api.github.com/repos/github/Hello-World/issues{/number}",
"pulls_url": "https://api.github.com/repos/github/Hello-World/pulls{/number}",
"milestones_url": "https://api.github.com/repos/github/Hello-World/milestones{/number}",
"notifications_url": "https://api.github.com/repos/github/Hello-World/notifications{?since,all,participating}",
"labels_url": "https://api.github.com/repos/github/Hello-World/labels{/name}",
"releases_url": "https://api.github.com/repos/github/Hello-World/releases{/id}",
"deployments_url": "https://api.github.com/repos/github/Hello-World/deployments",
"created_at": "2025-08-01T18:44:14Z",
"updated_at": "2025-08-01T18:48:38Z",
"pushed_at": "2025-08-01T18:44:50Z",
"git_url": "git://github.localhost/github/Hello-World.git",
"ssh_url": "ssh://git@localhost:3035/github/Hello-World.git",
"clone_url": "https://github.com/github/Hello-World.git",
"svn_url": "https://github.com/github/Hello-World",
"homepage": null,
"size": 6,
"stargazers_count": 0,
"watchers_count": 0,
"language": null,
"has_issues": true,
"has_projects": true,
"has_downloads": true,
"has_wiki": true,
"has_pages": false,
"has_discussions": false,
"forks_count": 0,
"mirror_url": null,
"archived": false,
"disabled": false,
"open_issues_count": 3,
"license": null,
"allow_forking": true,
"is_template": false,
"web_commit_signoff_required": false,
"topics": [],
"visibility": "public",
"forks": 0,
"open_issues": 3,
"watchers": 0,
"default_branch": "main"
}
},
"base": {
"label": "github:branch-0f4ceb14cbe39e4786ffbabb776da599",
"ref": "branch-0f4ceb14cbe39e4786ffbabb776da599",
"sha": "9a9f5a8d77bdc2540412900d3c930fe36a82b5ed",
"user": {
"login": "github",
"id": 5,
"node_id": "O_kgAF",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/github",
"html_url": "https://github.com/github",
"followers_url": "https://api.github.com/users/github/followers",
"following_url": "https://api.github.com/users/github/following{/other_user}",
"gists_url": "https://api.github.com/users/github/gists{/gist_id}",
"starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/github/subscriptions",
"organizations_url": "https://api.github.com/users/github/orgs",
"repos_url": "https://api.github.com/users/github/repos",
"events_url": "https://api.github.com/users/github/events{/privacy}",
"received_events_url": "https://api.github.com/users/github/received_events",
"type": "Organization",
"user_view_type": "public",
"site_admin": false
},
"repo": {
"id": 1,
"node_id": "R_kgAB",
"name": "Hello-World",
"full_name": "github/Hello-World",
"private": false,
"owner": {
"login": "github",
"id": 5,
"node_id": "O_kgAF",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/github",
"html_url": "https://github.com/github",
"followers_url": "https://api.github.com/users/github/followers",
"following_url": "https://api.github.com/users/github/following{/other_user}",
"gists_url": "https://api.github.com/users/github/gists{/gist_id}",
"starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/github/subscriptions",
"organizations_url": "https://api.github.com/users/github/orgs",
"repos_url": "https://api.github.com/users/github/repos",
"events_url": "https://api.github.com/users/github/events{/privacy}",
"received_events_url": "https://api.github.com/users/github/received_events",
"type": "Organization",
"user_view_type": "public",
"site_admin": false
},
"html_url": "https://github.com/github/Hello-World",
"description": null,
"fork": false,
"url": "https://api.github.com/repos/github/Hello-World",
"forks_url": "https://api.github.com/repos/github/Hello-World/forks",
"keys_url": "https://api.github.com/repos/github/Hello-World/keys{/key_id}",
"collaborators_url": "https://api.github.com/repos/github/Hello-World/collaborators{/collaborator}",
"teams_url": "https://api.github.com/repos/github/Hello-World/teams",
"hooks_url": "https://api.github.com/repos/github/Hello-World/hooks",
"issue_events_url": "https://api.github.com/repos/github/Hello-World/issues/events{/number}",
"events_url": "https://api.github.com/repos/github/Hello-World/events",
"assignees_url": "https://api.github.com/repos/github/Hello-World/assignees{/user}",
"branches_url": "https://api.github.com/repos/github/Hello-World/branches{/branch}",
"tags_url": "https://api.github.com/repos/github/Hello-World/tags",
"blobs_url": "https://api.github.com/repos/github/Hello-World/git/blobs{/sha}",
"git_tags_url": "https://api.github.com/repos/github/Hello-World/git/tags{/sha}",
"git_refs_url": "https://api.github.com/repos/github/Hello-World/git/refs{/sha}",
"trees_url": "https://api.github.com/repos/github/Hello-World/git/trees{/sha}",
"statuses_url": "https://api.github.com/repos/github/Hello-World/statuses/{sha}",
"languages_url": "https://api.github.com/repos/github/Hello-World/languages",
"stargazers_url": "https://api.github.com/repos/github/Hello-World/stargazers",
"contributors_url": "https://api.github.com/repos/github/Hello-World/contributors",
"subscribers_url": "https://api.github.com/repos/github/Hello-World/subscribers",
"subscription_url": "https://api.github.com/repos/github/Hello-World/subscription",
"commits_url": "https://api.github.com/repos/github/Hello-World/commits{/sha}",
"git_commits_url": "https://api.github.com/repos/github/Hello-World/git/commits{/sha}",
"comments_url": "https://api.github.com/repos/github/Hello-World/comments{/number}",
"issue_comment_url": "https://api.github.com/repos/github/Hello-World/issues/comments{/number}",
"contents_url": "https://api.github.com/repos/github/Hello-World/contents/{+path}",
"compare_url": "https://api.github.com/repos/github/Hello-World/compare/{base}...{head}",
"merges_url": "https://api.github.com/repos/github/Hello-World/merges",
"archive_url": "https://api.github.com/repos/github/Hello-World/{archive_format}{/ref}",
"downloads_url": "https://api.github.com/repos/github/Hello-World/downloads",
"issues_url": "https://api.github.com/repos/github/Hello-World/issues{/number}",
"pulls_url": "https://api.github.com/repos/github/Hello-World/pulls{/number}",
"milestones_url": "https://api.github.com/repos/github/Hello-World/milestones{/number}",
"notifications_url": "https://api.github.com/repos/github/Hello-World/notifications{?since,all,participating}",
"labels_url": "https://api.github.com/repos/github/Hello-World/labels{/name}",
"releases_url": "https://api.github.com/repos/github/Hello-World/releases{/id}",
"deployments_url": "https://api.github.com/repos/github/Hello-World/deployments",
"created_at": "2025-08-01T18:44:14Z",
"updated_at": "2025-08-01T18:48:38Z",
"pushed_at": "2025-08-01T18:44:50Z",
"git_url": "git://github.localhost/github/Hello-World.git",
"ssh_url": "ssh://git@localhost:3035/github/Hello-World.git",
"clone_url": "https://github.com/github/Hello-World.git",
"svn_url": "https://github.com/github/Hello-World",
"homepage": null,
"size": 6,
"stargazers_count": 0,
"watchers_count": 0,
"language": null,
"has_issues": true,
"has_projects": true,
"has_downloads": true,
"has_wiki": true,
"has_pages": false,
"has_discussions": false,
"forks_count": 0,
"mirror_url": null,
"archived": false,
"disabled": false,
"open_issues_count": 3,
"license": null,
"allow_forking": true,
"is_template": false,
"web_commit_signoff_required": false,
"topics": [],
"visibility": "public",
"forks": 0,
"open_issues": 3,
"watchers": 0,
"default_branch": "main"
}
},
"_links": {
"self": {
"href": "https://api.github.com/repos/github/Hello-World/pulls/6"
},
"html": {
"href": "https://github.com/github/Hello-World/pull/6"
},
"issue": {
"href": "https://api.github.com/repos/github/Hello-World/issues/6"
},
"comments": {
"href": "https://api.github.com/repos/github/Hello-World/issues/6/comments"
},
"review_comments": {
"href": "https://api.github.com/repos/github/Hello-World/pulls/6/comments"
},
"review_comment": {
"href": "https://api.github.com/repos/github/Hello-World/pulls/comments{/number}"
},
"commits": {
"href": "https://api.github.com/repos/github/Hello-World/pulls/6/commits"
},
"statuses": {
"href": "https://api.github.com/repos/github/Hello-World/statuses/a3258d3434ecb2058b2784c8eb8610c2e9937a0d"
}
},
"author_association": "MEMBER",
"auto_merge": null,
"active_lock_reason": null
},
"content_type": "PullRequest",
"creator": {
"login": "monalisa",
"id": 2,
"node_id": "U_kgAC",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/monalisa",
"html_url": "https://github.com/monalisa",
"followers_url": "https://api.github.com/users/monalisa/followers",
"following_url": "https://api.github.com/users/monalisa/following{/other_user}",
"gists_url": "https://api.github.com/users/monalisa/gists{/gist_id}",
"starred_url": "https://api.github.com/users/monalisa/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/monalisa/subscriptions",
"organizations_url": "https://api.github.com/users/monalisa/orgs",
"repos_url": "https://api.github.com/users/monalisa/repos",
"events_url": "https://api.github.com/users/monalisa/events{/privacy}",
"received_events_url": "https://api.github.com/users/monalisa/received_events",
"type": "User",
"user_view_type": "public",
"site_admin": false
},
"created_at": "2025-08-01T18:44:51Z",
"updated_at": "2025-08-06T19:25:18Z",
"archived_at": null,
"item_url": "https://api.github.com/orgs/github/projectsV2/1/items/13",
"fields": [
{
"id": 1,
"name": "Title",
"type": "title",
"value": {
"raw": "It seemed to me that any civilization that had so far lost its head as to need to include a set of detailed instructions for use in a packet of toothpicks, was no longer a civilization in which I could live and stay sane.",
"html": "It seemed to me that any civilization that had so far lost its head as to need to include a set of detailed instructions for use in a packet of toothpicks, was no longer a civilization in which I could live and stay sane.",
"number": 6,
"url": "https://github.com/5/1/pull/6",
"issue_id": 12,
"state": "open",
"state_reason": null,
"is_draft": false
}
},
{
"id": 2,
"name": "Assignees",
"type": "assignees",
"value": [
{
"login": "octocat",
"id": 175,
"node_id": "U_kgDMrw",
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
"user_view_type": "public",
"site_admin": false
}
]
},
{
"id": 3,
"name": "Status",
"type": "single_select",
"value": {
"id": "98236657",
"name": {
"raw": "Done",
"html": "Done"
},
"color": "PURPLE",
"description": {
"raw": "This has been completed",
"html": "This has been completed"
}
}
},
{
"id": 4,
"name": "Labels",
"type": "labels",
"value": [
{
"id": 19,
"node_id": "LA_kwABEw",
"url": "https://api.github.com/repos/github/Hello-World/labels/bug%20:bug:",
"name": "bug :bug:",
"color": "efe24f",
"default": false,
"description": "Something isn't working"
},
{
"id": 26,
"node_id": "LA_kwABGg",
"url": "https://api.github.com/repos/github/Hello-World/labels/fun%20size%20%F0%9F%8D%AB",
"name": "fun size 🍫",
"color": "f29c24",
"default": false,
"description": "Extra attention is needed"
},
{
"id": 33,
"node_id": "LA_kwABIQ",
"url": "https://api.github.com/repos/github/Hello-World/labels/%F0%9F%9A%92%20wontfix",
"name": "🚒 wontfix",
"color": "5891ce",
"default": false,
"description": "This will not be worked on"
}
]
},
{
"id": 5,
"name": "Linked pull requests",
"type": "linked_pull_requests",
"value": []
},
{
"id": 6,
"name": "Milestone",
"type": "milestone",
"value": {
"url": "https://api.github.com/repos/github/Hello-World/milestones/1",
"html_url": "https://github.com/github/Hello-World/milestone/1",
"labels_url": "https://api.github.com/repos/github/Hello-World/milestones/1/labels",
"id": 1,
"node_id": "MI_kwABAQ",
"number": 1,
"title": "Open milestone",
"description": null,
"creator": {
"login": "octocat",
"id": 175,
"node_id": "U_kgDMrw",
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
"user_view_type": "public",
"site_admin": false
},
"open_issues": 2,
"closed_issues": 1,
"state": "open",
"created_at": "2025-08-01T18:44:30Z",
"updated_at": "2025-08-06T19:14:15Z",
"due_on": null,
"closed_at": null
}
},
{
"id": 7,
"name": "Repository",
"type": "repository",
"value": {
"id": 1,
"node_id": "R_kgAB",
"name": "Hello-World",
"full_name": "github/Hello-World",
"private": false,
"owner": {
"login": "github",
"id": 5,
"node_id": "O_kgAF",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/github",
"html_url": "https://github.com/github",
"followers_url": "https://api.github.com/users/github/followers",
"following_url": "https://api.github.com/users/github/following{/other_user}",
"gists_url": "https://api.github.com/users/github/gists{/gist_id}",
"starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/github/subscriptions",
"organizations_url": "https://api.github.com/users/github/orgs",
"repos_url": "https://api.github.com/users/github/repos",
"events_url": "https://api.github.com/users/github/events{/privacy}",
"received_events_url": "https://api.github.com/users/github/received_events",
"type": "Organization",
"user_view_type": "public",
"site_admin": false
},
"html_url": "https://github.com/github/Hello-World",
"description": null,
"fork": false,
"url": "https://api.github.com/repos/github/Hello-World",
"forks_url": "https://api.github.com/repos/github/Hello-World/forks",
"keys_url": "https://api.github.com/repos/github/Hello-World/keys{/key_id}",
"collaborators_url": "https://api.github.com/repos/github/Hello-World/collaborators{/collaborator}",
"teams_url": "https://api.github.com/repos/github/Hello-World/teams",
"hooks_url": "https://api.github.com/repos/github/Hello-World/hooks",
"issue_events_url": "https://api.github.com/repos/github/Hello-World/issues/events{/number}",
"events_url": "https://api.github.com/repos/github/Hello-World/events",
"assignees_url": "https://api.github.com/repos/github/Hello-World/assignees{/user}",
"branches_url": "https://api.github.com/repos/github/Hello-World/branches{/branch}",
"tags_url": "https://api.github.com/repos/github/Hello-World/tags",
"blobs_url": "https://api.github.com/repos/github/Hello-World/git/blobs{/sha}",
"git_tags_url": "https://api.github.com/repos/github/Hello-World/git/tags{/sha}",
"git_refs_url": "https://api.github.com/repos/github/Hello-World/git/refs{/sha}",
"trees_url": "https://api.github.com/repos/github/Hello-World/git/trees{/sha}",
"statuses_url": "https://api.github.com/repos/github/Hello-World/statuses/{sha}",
"languages_url": "https://api.github.com/repos/github/Hello-World/languages",
"stargazers_url": "https://api.github.com/repos/github/Hello-World/stargazers",
"contributors_url": "https://api.github.com/repos/github/Hello-World/contributors",
"subscribers_url": "https://api.github.com/repos/github/Hello-World/subscribers",
"subscription_url": "https://api.github.com/repos/github/Hello-World/subscription",
"commits_url": "https://api.github.com/repos/github/Hello-World/commits{/sha}",
"git_commits_url": "https://api.github.com/repos/github/Hello-World/git/commits{/sha}",
"comments_url": "https://api.github.com/repos/github/Hello-World/comments{/number}",
"issue_comment_url": "https://api.github.com/repos/github/Hello-World/issues/comments{/number}",
"contents_url": "https://api.github.com/repos/github/Hello-World/contents/{+path}",
"compare_url": "https://api.github.com/repos/github/Hello-World/compare/{base}...{head}",
"merges_url": "https://api.github.com/repos/github/Hello-World/merges",
"archive_url": "https://api.github.com/repos/github/Hello-World/{archive_format}{/ref}",
"downloads_url": "https://api.github.com/repos/github/Hello-World/downloads",
"issues_url": "https://api.github.com/repos/github/Hello-World/issues{/number}",
"pulls_url": "https://api.github.com/repos/github/Hello-World/pulls{/number}",
"milestones_url": "https://api.github.com/repos/github/Hello-World/milestones{/number}",
"notifications_url": "https://api.github.com/repos/github/Hello-World/notifications{?since,all,participating}",
"labels_url": "https://api.github.com/repos/github/Hello-World/labels{/name}",
"releases_url": "https://api.github.com/repos/github/Hello-World/releases{/id}",
"deployments_url": "https://api.github.com/repos/github/Hello-World/deployments"
}
},
{
"id": 8,
"name": "Type",
"type": "issue_type",
"value": null
},
{
"id": 9,
"name": "Reviewers",
"type": "reviewers",
"value": [
{
"type": "ReviewRequest",
"status": "pending",
"reviewer": {
"avatarUrl": "https://github.com/images/error/octocat_happy.gif",
"id": 2,
"login": "monalisa",
"url": "https://github.com/monalisa",
"name": "monalisa",
"type": "User"
}
}
]
},
{
"id": 10,
"name": "Parent issue",
"type": "parent_issue",
"value": null
},
{
"id": 11,
"name": "Sub-issues progress",
"type": "sub_issues_progress",
"value": null
}
]
}`

## Update project item for user

Update a specific item in a user-owned project.

### Fine-grained access tokens for "Update project item for user"

This endpoint does not work with GitHub App user access tokens, GitHub App installation access tokens, or fine-grained personal access tokens.

### Parameters for "Update project item for user"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| project_numberintegerRequiredThe project's number. |
| usernamestringRequiredThe handle for the GitHub user account. |
| item_idintegerRequiredThe unique identifier of the project item. |

| Name, Type, Description |
| --- |
| fieldsarray of objectsRequiredA list of field updates to apply. |
| Name, Type, DescriptionidintegerRequiredThe ID of the project field to update.valuenull or string or numberRequiredThe new value for the field:For text, number, and date fields, provide the new value directly.For single select and iteration fields, provide the ID of the option or iteration.To clear the field, set this to null. |
| Name, Type, Description |
| idintegerRequiredThe ID of the project field to update. |
| valuenull or string or numberRequiredThe new value for the field:For text, number, and date fields, provide the new value directly.For single select and iteration fields, provide the ID of the option or iteration.To clear the field, set this to null. |

### HTTP response status codes for "Update project item for user"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 401 | Requires authentication |
| 403 | Forbidden |
| 404 | Resource not found |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Update project item for user"

#### Request examples

Select the example typeUpdate a text fieldUpdate a number fieldUpdate a date fieldUpdate a single select fieldUpdate an iteration fieldpatch/users/{username}/projectsV2/{project_number}/items/{item_id}

-
-
-

`curl -L \
  -X PATCH \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/users/USERNAME/projectsV2/PROJECT_NUMBER/items/ITEM_ID \
  -d '{"fields":[{"id":123,"value":"Updated text value"}]}'`

Response

-
-

`Status: 200``{
"id": 13,
"node_id": "PVTI_lAAFAQ0",
"project_url": "https://api.github.com/orgs/github/projectsV2/1",
"content": {
"url": "https://api.github.com/repos/github/Hello-World/pulls/6",
"id": 10,
"node_id": "PR_kwABCg",
"html_url": "https://github.com/github/Hello-World/pull/6",
"diff_url": "https://github.com/github/Hello-World/pull/6.diff",
"patch_url": "https://github.com/github/Hello-World/pull/6.patch",
"issue_url": "https://api.github.com/repos/github/Hello-World/issues/6",
"number": 6,
"state": "open",
"locked": false,
"title": "Issue title",
"user": {
"login": "monalisa",
"id": 161,
"node_id": "U_kgDMoQ",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/monalisa",
"html_url": "https://github.com/monalisa",
"followers_url": "https://api.github.com/users/monalisa/followers",
"following_url": "https://api.github.com/users/monalisa/following{/other_user}",
"gists_url": "https://api.github.com/users/monalisa/gists{/gist_id}",
"starred_url": "https://api.github.com/users/monalisa/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/monalisa/subscriptions",
"organizations_url": "https://api.github.com/users/monalisa/orgs",
"repos_url": "https://api.github.com/users/monalisa/repos",
"events_url": "https://api.github.com/users/monalisa/events{/privacy}",
"received_events_url": "https://api.github.com/users/monalisa/received_events",
"type": "User",
"user_view_type": "public",
"site_admin": false
},
"body": "Issue body",
"created_at": "2025-08-01T18:44:50Z",
"updated_at": "2025-08-06T19:25:18Z",
"closed_at": null,
"merged_at": null,
"merge_commit_sha": "98e25bad5878e54d22e5338cbc905dd2deedfa34",
"assignee": {
"login": "octocat",
"id": 175,
"node_id": "U_kgDMrw",
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
"user_view_type": "public",
"site_admin": false
},
"assignees": [
{
"login": "octocat",
"id": 175,
"node_id": "U_kgDMrw",
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
"user_view_type": "public",
"site_admin": false
}
],
"requested_reviewers": [
{
"login": "monalisa",
"id": 2,
"node_id": "U_kgAC",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/monalisa",
"html_url": "https://github.com/monalisa",
"followers_url": "https://api.github.com/users/monalisa/followers",
"following_url": "https://api.github.com/users/monalisa/following{/other_user}",
"gists_url": "https://api.github.com/users/monalisa/gists{/gist_id}",
"starred_url": "https://api.github.com/users/monalisa/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/monalisa/subscriptions",
"organizations_url": "https://api.github.com/users/monalisa/orgs",
"repos_url": "https://api.github.com/users/monalisa/repos",
"events_url": "https://api.github.com/users/monalisa/events{/privacy}",
"received_events_url": "https://api.github.com/users/monalisa/received_events",
"type": "User",
"user_view_type": "public",
"site_admin": false
}
],
"requested_teams": [],
"labels": [
{
"id": 19,
"node_id": "LA_kwABEw",
"url": "https://api.github.com/repos/github/Hello-World/labels/bug%20:bug:",
"name": "bug :bug:",
"color": "efe24f",
"default": false,
"description": "Something isn't working"
},
{
"id": 26,
"node_id": "LA_kwABGg",
"url": "https://api.github.com/repos/github/Hello-World/labels/fun%20size%20%F0%9F%8D%AB",
"name": "fun size 🍫",
"color": "f29c24",
"default": false,
"description": "Extra attention is needed"
},
{
"id": 33,
"node_id": "LA_kwABIQ",
"url": "https://api.github.com/repos/github/Hello-World/labels/%F0%9F%9A%92%20wontfix",
"name": "🚒 wontfix",
"color": "5891ce",
"default": false,
"description": "This will not be worked on"
}
],
"milestone": {
"url": "https://api.github.com/repos/github/Hello-World/milestones/1",
"html_url": "https://github.com/github/Hello-World/milestone/1",
"labels_url": "https://api.github.com/repos/github/Hello-World/milestones/1/labels",
"id": 1,
"node_id": "MI_kwABAQ",
"number": 1,
"title": "Open milestone",
"description": null,
"creator": {
"login": "monalisa",
"id": 2,
"node_id": "U_kgAC",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/monalisa",
"html_url": "https://github.com/monalisa",
"followers_url": "https://api.github.com/users/monalisa/followers",
"following_url": "https://api.github.com/users/monalisa/following{/other_user}",
"gists_url": "https://api.github.com/users/monalisa/gists{/gist_id}",
"starred_url": "https://api.github.com/users/monalisa/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/monalisa/subscriptions",
"organizations_url": "https://api.github.com/users/monalisa/orgs",
"repos_url": "https://api.github.com/users/monalisa/repos",
"events_url": "https://api.github.com/users/monalisa/events{/privacy}",
"received_events_url": "https://api.github.com/users/monalisa/received_events",
"type": "User",
"user_view_type": "public",
"site_admin": false
},
"open_issues": 2,
"closed_issues": 1,
"state": "open",
"created_at": "2025-08-01T18:44:30Z",
"updated_at": "2025-08-06T19:14:15Z",
"due_on": null,
"closed_at": null
},
"draft": false,
"commits_url": "https://api.github.com/repos/github/Hello-World/pulls/6/commits",
"review_comments_url": "https://api.github.com/repos/github/Hello-World/pulls/6/comments",
"review_comment_url": "https://api.github.com/repos/github/Hello-World/pulls/comments{/number}",
"comments_url": "https://api.github.com/repos/github/Hello-World/issues/6/comments",
"statuses_url": "https://api.github.com/repos/github/Hello-World/statuses/a3258d3434ecb2058b2784c8eb8610c2e9937a0d",
"head": {
"label": "github:branch-2ee3da8fde8a1adfe6d0809a1a414e4f",
"ref": "branch-2ee3da8fde8a1adfe6d0809a1a414e4f",
"sha": "a3258d3434ecb2058b2784c8eb8610c2e9937a0d",
"user": {
"login": "github",
"id": 5,
"node_id": "O_kgAF",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/github",
"html_url": "https://github.com/github",
"followers_url": "https://api.github.com/users/github/followers",
"following_url": "https://api.github.com/users/github/following{/other_user}",
"gists_url": "https://api.github.com/users/github/gists{/gist_id}",
"starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/github/subscriptions",
"organizations_url": "https://api.github.com/users/github/orgs",
"repos_url": "https://api.github.com/users/github/repos",
"events_url": "https://api.github.com/users/github/events{/privacy}",
"received_events_url": "https://api.github.com/users/github/received_events",
"type": "Organization",
"user_view_type": "public",
"site_admin": false
},
"repo": {
"id": 1,
"node_id": "R_kgAB",
"name": "Hello-World",
"full_name": "github/Hello-World",
"private": false,
"owner": {
"login": "github",
"id": 5,
"node_id": "O_kgAF",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/github",
"html_url": "https://github.com/github",
"followers_url": "https://api.github.com/users/github/followers",
"following_url": "https://api.github.com/users/github/following{/other_user}",
"gists_url": "https://api.github.com/users/github/gists{/gist_id}",
"starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/github/subscriptions",
"organizations_url": "https://api.github.com/users/github/orgs",
"repos_url": "https://api.github.com/users/github/repos",
"events_url": "https://api.github.com/users/github/events{/privacy}",
"received_events_url": "https://api.github.com/users/github/received_events",
"type": "Organization",
"user_view_type": "public",
"site_admin": false
},
"html_url": "https://github.com/github/Hello-World",
"description": null,
"fork": false,
"url": "https://api.github.com/repos/github/Hello-World",
"forks_url": "https://api.github.com/repos/github/Hello-World/forks",
"keys_url": "https://api.github.com/repos/github/Hello-World/keys{/key_id}",
"collaborators_url": "https://api.github.com/repos/github/Hello-World/collaborators{/collaborator}",
"teams_url": "https://api.github.com/repos/github/Hello-World/teams",
"hooks_url": "https://api.github.com/repos/github/Hello-World/hooks",
"issue_events_url": "https://api.github.com/repos/github/Hello-World/issues/events{/number}",
"events_url": "https://api.github.com/repos/github/Hello-World/events",
"assignees_url": "https://api.github.com/repos/github/Hello-World/assignees{/user}",
"branches_url": "https://api.github.com/repos/github/Hello-World/branches{/branch}",
"tags_url": "https://api.github.com/repos/github/Hello-World/tags",
"blobs_url": "https://api.github.com/repos/github/Hello-World/git/blobs{/sha}",
"git_tags_url": "https://api.github.com/repos/github/Hello-World/git/tags{/sha}",
"git_refs_url": "https://api.github.com/repos/github/Hello-World/git/refs{/sha}",
"trees_url": "https://api.github.com/repos/github/Hello-World/git/trees{/sha}",
"statuses_url": "https://api.github.com/repos/github/Hello-World/statuses/{sha}",
"languages_url": "https://api.github.com/repos/github/Hello-World/languages",
"stargazers_url": "https://api.github.com/repos/github/Hello-World/stargazers",
"contributors_url": "https://api.github.com/repos/github/Hello-World/contributors",
"subscribers_url": "https://api.github.com/repos/github/Hello-World/subscribers",
"subscription_url": "https://api.github.com/repos/github/Hello-World/subscription",
"commits_url": "https://api.github.com/repos/github/Hello-World/commits{/sha}",
"git_commits_url": "https://api.github.com/repos/github/Hello-World/git/commits{/sha}",
"comments_url": "https://api.github.com/repos/github/Hello-World/comments{/number}",
"issue_comment_url": "https://api.github.com/repos/github/Hello-World/issues/comments{/number}",
"contents_url": "https://api.github.com/repos/github/Hello-World/contents/{+path}",
"compare_url": "https://api.github.com/repos/github/Hello-World/compare/{base}...{head}",
"merges_url": "https://api.github.com/repos/github/Hello-World/merges",
"archive_url": "https://api.github.com/repos/github/Hello-World/{archive_format}{/ref}",
"downloads_url": "https://api.github.com/repos/github/Hello-World/downloads",
"issues_url": "https://api.github.com/repos/github/Hello-World/issues{/number}",
"pulls_url": "https://api.github.com/repos/github/Hello-World/pulls{/number}",
"milestones_url": "https://api.github.com/repos/github/Hello-World/milestones{/number}",
"notifications_url": "https://api.github.com/repos/github/Hello-World/notifications{?since,all,participating}",
"labels_url": "https://api.github.com/repos/github/Hello-World/labels{/name}",
"releases_url": "https://api.github.com/repos/github/Hello-World/releases{/id}",
"deployments_url": "https://api.github.com/repos/github/Hello-World/deployments",
"created_at": "2025-08-01T18:44:14Z",
"updated_at": "2025-08-01T18:48:38Z",
"pushed_at": "2025-08-01T18:44:50Z",
"git_url": "git://github.localhost/github/Hello-World.git",
"ssh_url": "ssh://git@localhost:3035/github/Hello-World.git",
"clone_url": "https://github.com/github/Hello-World.git",
"svn_url": "https://github.com/github/Hello-World",
"homepage": null,
"size": 6,
"stargazers_count": 0,
"watchers_count": 0,
"language": null,
"has_issues": true,
"has_projects": true,
"has_downloads": true,
"has_wiki": true,
"has_pages": false,
"has_discussions": false,
"forks_count": 0,
"mirror_url": null,
"archived": false,
"disabled": false,
"open_issues_count": 3,
"license": null,
"allow_forking": true,
"is_template": false,
"web_commit_signoff_required": false,
"topics": [],
"visibility": "public",
"forks": 0,
"open_issues": 3,
"watchers": 0,
"default_branch": "main"
}
},
"base": {
"label": "github:branch-0f4ceb14cbe39e4786ffbabb776da599",
"ref": "branch-0f4ceb14cbe39e4786ffbabb776da599",
"sha": "9a9f5a8d77bdc2540412900d3c930fe36a82b5ed",
"user": {
"login": "github",
"id": 5,
"node_id": "O_kgAF",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/github",
"html_url": "https://github.com/github",
"followers_url": "https://api.github.com/users/github/followers",
"following_url": "https://api.github.com/users/github/following{/other_user}",
"gists_url": "https://api.github.com/users/github/gists{/gist_id}",
"starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/github/subscriptions",
"organizations_url": "https://api.github.com/users/github/orgs",
"repos_url": "https://api.github.com/users/github/repos",
"events_url": "https://api.github.com/users/github/events{/privacy}",
"received_events_url": "https://api.github.com/users/github/received_events",
"type": "Organization",
"user_view_type": "public",
"site_admin": false
},
"repo": {
"id": 1,
"node_id": "R_kgAB",
"name": "Hello-World",
"full_name": "github/Hello-World",
"private": false,
"owner": {
"login": "github",
"id": 5,
"node_id": "O_kgAF",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/github",
"html_url": "https://github.com/github",
"followers_url": "https://api.github.com/users/github/followers",
"following_url": "https://api.github.com/users/github/following{/other_user}",
"gists_url": "https://api.github.com/users/github/gists{/gist_id}",
"starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/github/subscriptions",
"organizations_url": "https://api.github.com/users/github/orgs",
"repos_url": "https://api.github.com/users/github/repos",
"events_url": "https://api.github.com/users/github/events{/privacy}",
"received_events_url": "https://api.github.com/users/github/received_events",
"type": "Organization",
"user_view_type": "public",
"site_admin": false
},
"html_url": "https://github.com/github/Hello-World",
"description": null,
"fork": false,
"url": "https://api.github.com/repos/github/Hello-World",
"forks_url": "https://api.github.com/repos/github/Hello-World/forks",
"keys_url": "https://api.github.com/repos/github/Hello-World/keys{/key_id}",
"collaborators_url": "https://api.github.com/repos/github/Hello-World/collaborators{/collaborator}",
"teams_url": "https://api.github.com/repos/github/Hello-World/teams",
"hooks_url": "https://api.github.com/repos/github/Hello-World/hooks",
"issue_events_url": "https://api.github.com/repos/github/Hello-World/issues/events{/number}",
"events_url": "https://api.github.com/repos/github/Hello-World/events",
"assignees_url": "https://api.github.com/repos/github/Hello-World/assignees{/user}",
"branches_url": "https://api.github.com/repos/github/Hello-World/branches{/branch}",
"tags_url": "https://api.github.com/repos/github/Hello-World/tags",
"blobs_url": "https://api.github.com/repos/github/Hello-World/git/blobs{/sha}",
"git_tags_url": "https://api.github.com/repos/github/Hello-World/git/tags{/sha}",
"git_refs_url": "https://api.github.com/repos/github/Hello-World/git/refs{/sha}",
"trees_url": "https://api.github.com/repos/github/Hello-World/git/trees{/sha}",
"statuses_url": "https://api.github.com/repos/github/Hello-World/statuses/{sha}",
"languages_url": "https://api.github.com/repos/github/Hello-World/languages",
"stargazers_url": "https://api.github.com/repos/github/Hello-World/stargazers",
"contributors_url": "https://api.github.com/repos/github/Hello-World/contributors",
"subscribers_url": "https://api.github.com/repos/github/Hello-World/subscribers",
"subscription_url": "https://api.github.com/repos/github/Hello-World/subscription",
"commits_url": "https://api.github.com/repos/github/Hello-World/commits{/sha}",
"git_commits_url": "https://api.github.com/repos/github/Hello-World/git/commits{/sha}",
"comments_url": "https://api.github.com/repos/github/Hello-World/comments{/number}",
"issue_comment_url": "https://api.github.com/repos/github/Hello-World/issues/comments{/number}",
"contents_url": "https://api.github.com/repos/github/Hello-World/contents/{+path}",
"compare_url": "https://api.github.com/repos/github/Hello-World/compare/{base}...{head}",
"merges_url": "https://api.github.com/repos/github/Hello-World/merges",
"archive_url": "https://api.github.com/repos/github/Hello-World/{archive_format}{/ref}",
"downloads_url": "https://api.github.com/repos/github/Hello-World/downloads",
"issues_url": "https://api.github.com/repos/github/Hello-World/issues{/number}",
"pulls_url": "https://api.github.com/repos/github/Hello-World/pulls{/number}",
"milestones_url": "https://api.github.com/repos/github/Hello-World/milestones{/number}",
"notifications_url": "https://api.github.com/repos/github/Hello-World/notifications{?since,all,participating}",
"labels_url": "https://api.github.com/repos/github/Hello-World/labels{/name}",
"releases_url": "https://api.github.com/repos/github/Hello-World/releases{/id}",
"deployments_url": "https://api.github.com/repos/github/Hello-World/deployments",
"created_at": "2025-08-01T18:44:14Z",
"updated_at": "2025-08-01T18:48:38Z",
"pushed_at": "2025-08-01T18:44:50Z",
"git_url": "git://github.localhost/github/Hello-World.git",
"ssh_url": "ssh://git@localhost:3035/github/Hello-World.git",
"clone_url": "https://github.com/github/Hello-World.git",
"svn_url": "https://github.com/github/Hello-World",
"homepage": null,
"size": 6,
"stargazers_count": 0,
"watchers_count": 0,
"language": null,
"has_issues": true,
"has_projects": true,
"has_downloads": true,
"has_wiki": true,
"has_pages": false,
"has_discussions": false,
"forks_count": 0,
"mirror_url": null,
"archived": false,
"disabled": false,
"open_issues_count": 3,
"license": null,
"allow_forking": true,
"is_template": false,
"web_commit_signoff_required": false,
"topics": [],
"visibility": "public",
"forks": 0,
"open_issues": 3,
"watchers": 0,
"default_branch": "main"
}
},
"_links": {
"self": {
"href": "https://api.github.com/repos/github/Hello-World/pulls/6"
},
"html": {
"href": "https://github.com/github/Hello-World/pull/6"
},
"issue": {
"href": "https://api.github.com/repos/github/Hello-World/issues/6"
},
"comments": {
"href": "https://api.github.com/repos/github/Hello-World/issues/6/comments"
},
"review_comments": {
"href": "https://api.github.com/repos/github/Hello-World/pulls/6/comments"
},
"review_comment": {
"href": "https://api.github.com/repos/github/Hello-World/pulls/comments{/number}"
},
"commits": {
"href": "https://api.github.com/repos/github/Hello-World/pulls/6/commits"
},
"statuses": {
"href": "https://api.github.com/repos/github/Hello-World/statuses/a3258d3434ecb2058b2784c8eb8610c2e9937a0d"
}
},
"author_association": "MEMBER",
"auto_merge": null,
"active_lock_reason": null
},
"content_type": "PullRequest",
"creator": {
"login": "monalisa",
"id": 2,
"node_id": "U_kgAC",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/monalisa",
"html_url": "https://github.com/monalisa",
"followers_url": "https://api.github.com/users/monalisa/followers",
"following_url": "https://api.github.com/users/monalisa/following{/other_user}",
"gists_url": "https://api.github.com/users/monalisa/gists{/gist_id}",
"starred_url": "https://api.github.com/users/monalisa/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/monalisa/subscriptions",
"organizations_url": "https://api.github.com/users/monalisa/orgs",
"repos_url": "https://api.github.com/users/monalisa/repos",
"events_url": "https://api.github.com/users/monalisa/events{/privacy}",
"received_events_url": "https://api.github.com/users/monalisa/received_events",
"type": "User",
"user_view_type": "public",
"site_admin": false
},
"created_at": "2025-08-01T18:44:51Z",
"updated_at": "2025-08-06T19:25:18Z",
"archived_at": null,
"item_url": "https://api.github.com/orgs/github/projectsV2/1/items/13",
"fields": [
{
"id": 1,
"name": "Title",
"type": "title",
"value": {
"raw": "It seemed to me that any civilization that had so far lost its head as to need to include a set of detailed instructions for use in a packet of toothpicks, was no longer a civilization in which I could live and stay sane.",
"html": "It seemed to me that any civilization that had so far lost its head as to need to include a set of detailed instructions for use in a packet of toothpicks, was no longer a civilization in which I could live and stay sane.",
"number": 6,
"url": "https://github.com/5/1/pull/6",
"issue_id": 12,
"state": "open",
"state_reason": null,
"is_draft": false
}
},
{
"id": 2,
"name": "Assignees",
"type": "assignees",
"value": [
{
"login": "octocat",
"id": 175,
"node_id": "U_kgDMrw",
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
"user_view_type": "public",
"site_admin": false
}
]
},
{
"id": 3,
"name": "Status",
"type": "single_select",
"value": {
"id": "98236657",
"name": {
"raw": "Done",
"html": "Done"
},
"color": "PURPLE",
"description": {
"raw": "This has been completed",
"html": "This has been completed"
}
}
},
{
"id": 4,
"name": "Labels",
"type": "labels",
"value": [
{
"id": 19,
"node_id": "LA_kwABEw",
"url": "https://api.github.com/repos/github/Hello-World/labels/bug%20:bug:",
"name": "bug :bug:",
"color": "efe24f",
"default": false,
"description": "Something isn't working"
},
{
"id": 26,
"node_id": "LA_kwABGg",
"url": "https://api.github.com/repos/github/Hello-World/labels/fun%20size%20%F0%9F%8D%AB",
"name": "fun size 🍫",
"color": "f29c24",
"default": false,
"description": "Extra attention is needed"
},
{
"id": 33,
"node_id": "LA_kwABIQ",
"url": "https://api.github.com/repos/github/Hello-World/labels/%F0%9F%9A%92%20wontfix",
"name": "🚒 wontfix",
"color": "5891ce",
"default": false,
"description": "This will not be worked on"
}
]
},
{
"id": 5,
"name": "Linked pull requests",
"type": "linked_pull_requests",
"value": []
},
{
"id": 6,
"name": "Milestone",
"type": "milestone",
"value": {
"url": "https://api.github.com/repos/github/Hello-World/milestones/1",
"html_url": "https://github.com/github/Hello-World/milestone/1",
"labels_url": "https://api.github.com/repos/github/Hello-World/milestones/1/labels",
"id": 1,
"node_id": "MI_kwABAQ",
"number": 1,
"title": "Open milestone",
"description": null,
"creator": {
"login": "octocat",
"id": 175,
"node_id": "U_kgDMrw",
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
"user_view_type": "public",
"site_admin": false
},
"open_issues": 2,
"closed_issues": 1,
"state": "open",
"created_at": "2025-08-01T18:44:30Z",
"updated_at": "2025-08-06T19:14:15Z",
"due_on": null,
"closed_at": null
}
},
{
"id": 7,
"name": "Repository",
"type": "repository",
"value": {
"id": 1,
"node_id": "R_kgAB",
"name": "Hello-World",
"full_name": "github/Hello-World",
"private": false,
"owner": {
"login": "github",
"id": 5,
"node_id": "O_kgAF",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/github",
"html_url": "https://github.com/github",
"followers_url": "https://api.github.com/users/github/followers",
"following_url": "https://api.github.com/users/github/following{/other_user}",
"gists_url": "https://api.github.com/users/github/gists{/gist_id}",
"starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/github/subscriptions",
"organizations_url": "https://api.github.com/users/github/orgs",
"repos_url": "https://api.github.com/users/github/repos",
"events_url": "https://api.github.com/users/github/events{/privacy}",
"received_events_url": "https://api.github.com/users/github/received_events",
"type": "Organization",
"user_view_type": "public",
"site_admin": false
},
"html_url": "https://github.com/github/Hello-World",
"description": null,
"fork": false,
"url": "https://api.github.com/repos/github/Hello-World",
"forks_url": "https://api.github.com/repos/github/Hello-World/forks",
"keys_url": "https://api.github.com/repos/github/Hello-World/keys{/key_id}",
"collaborators_url": "https://api.github.com/repos/github/Hello-World/collaborators{/collaborator}",
"teams_url": "https://api.github.com/repos/github/Hello-World/teams",
"hooks_url": "https://api.github.com/repos/github/Hello-World/hooks",
"issue_events_url": "https://api.github.com/repos/github/Hello-World/issues/events{/number}",
"events_url": "https://api.github.com/repos/github/Hello-World/events",
"assignees_url": "https://api.github.com/repos/github/Hello-World/assignees{/user}",
"branches_url": "https://api.github.com/repos/github/Hello-World/branches{/branch}",
"tags_url": "https://api.github.com/repos/github/Hello-World/tags",
"blobs_url": "https://api.github.com/repos/github/Hello-World/git/blobs{/sha}",
"git_tags_url": "https://api.github.com/repos/github/Hello-World/git/tags{/sha}",
"git_refs_url": "https://api.github.com/repos/github/Hello-World/git/refs{/sha}",
"trees_url": "https://api.github.com/repos/github/Hello-World/git/trees{/sha}",
"statuses_url": "https://api.github.com/repos/github/Hello-World/statuses/{sha}",
"languages_url": "https://api.github.com/repos/github/Hello-World/languages",
"stargazers_url": "https://api.github.com/repos/github/Hello-World/stargazers",
"contributors_url": "https://api.github.com/repos/github/Hello-World/contributors",
"subscribers_url": "https://api.github.com/repos/github/Hello-World/subscribers",
"subscription_url": "https://api.github.com/repos/github/Hello-World/subscription",
"commits_url": "https://api.github.com/repos/github/Hello-World/commits{/sha}",
"git_commits_url": "https://api.github.com/repos/github/Hello-World/git/commits{/sha}",
"comments_url": "https://api.github.com/repos/github/Hello-World/comments{/number}",
"issue_comment_url": "https://api.github.com/repos/github/Hello-World/issues/comments{/number}",
"contents_url": "https://api.github.com/repos/github/Hello-World/contents/{+path}",
"compare_url": "https://api.github.com/repos/github/Hello-World/compare/{base}...{head}",
"merges_url": "https://api.github.com/repos/github/Hello-World/merges",
"archive_url": "https://api.github.com/repos/github/Hello-World/{archive_format}{/ref}",
"downloads_url": "https://api.github.com/repos/github/Hello-World/downloads",
"issues_url": "https://api.github.com/repos/github/Hello-World/issues{/number}",
"pulls_url": "https://api.github.com/repos/github/Hello-World/pulls{/number}",
"milestones_url": "https://api.github.com/repos/github/Hello-World/milestones{/number}",
"notifications_url": "https://api.github.com/repos/github/Hello-World/notifications{?since,all,participating}",
"labels_url": "https://api.github.com/repos/github/Hello-World/labels{/name}",
"releases_url": "https://api.github.com/repos/github/Hello-World/releases{/id}",
"deployments_url": "https://api.github.com/repos/github/Hello-World/deployments"
}
},
{
"id": 8,
"name": "Type",
"type": "issue_type",
"value": null
},
{
"id": 9,
"name": "Reviewers",
"type": "reviewers",
"value": [
{
"type": "ReviewRequest",
"status": "pending",
"reviewer": {
"avatarUrl": "https://github.com/images/error/octocat_happy.gif",
"id": 2,
"login": "monalisa",
"url": "https://github.com/monalisa",
"name": "monalisa",
"type": "User"
}
}
]
},
{
"id": 10,
"name": "Parent issue",
"type": "parent_issue",
"value": null
},
{
"id": 11,
"name": "Sub-issues progress",
"type": "sub_issues_progress",
"value": null
}
]
}`

## Delete project item for user

Delete a specific item from a user-owned project.

### Fine-grained access tokens for "Delete project item for user"

This endpoint does not work with GitHub App user access tokens, GitHub App installation access tokens, or fine-grained personal access tokens.

### Parameters for "Delete project item for user"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| project_numberintegerRequiredThe project's number. |
| usernamestringRequiredThe handle for the GitHub user account. |
| item_idintegerRequiredThe unique identifier of the project item. |

### HTTP response status codes for "Delete project item for user"

| Status code | Description |
| --- | --- |
| 204 | No Content |
| 401 | Requires authentication |
| 403 | Forbidden |

### Code samples for "Delete project item for user"

#### Request example

delete/users/{username}/projectsV2/{project_number}/items/{item_id}

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/users/USERNAME/projectsV2/PROJECT_NUMBER/items/ITEM_ID`

Response

`Status: 204`

## List items for a user project view

List items in a user project with the saved view's filter applied.

### Fine-grained access tokens for "List items for a user project view"

This endpoint does not work with GitHub App user access tokens, GitHub App installation access tokens, or fine-grained personal access tokens.

### Parameters for "List items for a user project view"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| project_numberintegerRequiredThe project's number. |
| usernamestringRequiredThe handle for the GitHub user account. |
| view_numberintegerRequiredThe number that identifies the project view. |

| Name, Type, Description |
| --- |
| fieldsLimit results to specific fields, by their IDs. If not specified, the
title field will be returned.Example:fields[]=123&fields[]=456&fields[]=789orfields=123,456,789 |
| beforestringA cursor, as given in theLink header. If specified, the query only searches for results before this cursor. For more information, see "Using pagination in the REST API." |
| afterstringA cursor, as given in theLink header. If specified, the query only searches for results after this cursor. For more information, see "Using pagination in the REST API." |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |

### HTTP response status codes for "List items for a user project view"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 304 | Not modified |
| 401 | Requires authentication |
| 403 | Forbidden |
| 404 | Resource not found |

### Code samples for "List items for a user project view"

#### Request example

get/users/{username}/projectsV2/{project_number}/views/{view_number}/items

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/users/USERNAME/projectsV2/PROJECT_NUMBER/views/VIEW_NUMBER/items`

Response

-
-

`Status: 200``{
"id": 13,
"node_id": "PVTI_lAAFAQ0",
"project_url": "https://api.github.com/orgs/github/projectsV2/1",
"content": {
"url": "https://api.github.com/repos/github/Hello-World/pulls/6",
"id": 10,
"node_id": "PR_kwABCg",
"html_url": "https://github.com/github/Hello-World/pull/6",
"diff_url": "https://github.com/github/Hello-World/pull/6.diff",
"patch_url": "https://github.com/github/Hello-World/pull/6.patch",
"issue_url": "https://api.github.com/repos/github/Hello-World/issues/6",
"number": 6,
"state": "open",
"locked": false,
"title": "Issue title",
"user": {
"login": "monalisa",
"id": 161,
"node_id": "U_kgDMoQ",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/monalisa",
"html_url": "https://github.com/monalisa",
"followers_url": "https://api.github.com/users/monalisa/followers",
"following_url": "https://api.github.com/users/monalisa/following{/other_user}",
"gists_url": "https://api.github.com/users/monalisa/gists{/gist_id}",
"starred_url": "https://api.github.com/users/monalisa/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/monalisa/subscriptions",
"organizations_url": "https://api.github.com/users/monalisa/orgs",
"repos_url": "https://api.github.com/users/monalisa/repos",
"events_url": "https://api.github.com/users/monalisa/events{/privacy}",
"received_events_url": "https://api.github.com/users/monalisa/received_events",
"type": "User",
"user_view_type": "public",
"site_admin": false
},
"body": "Issue body",
"created_at": "2025-08-01T18:44:50Z",
"updated_at": "2025-08-06T19:25:18Z",
"closed_at": null,
"merged_at": null,
"merge_commit_sha": "98e25bad5878e54d22e5338cbc905dd2deedfa34",
"assignee": {
"login": "octocat",
"id": 175,
"node_id": "U_kgDMrw",
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
"user_view_type": "public",
"site_admin": false
},
"assignees": [
{
"login": "octocat",
"id": 175,
"node_id": "U_kgDMrw",
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
"user_view_type": "public",
"site_admin": false
}
],
"requested_reviewers": [
{
"login": "monalisa",
"id": 2,
"node_id": "U_kgAC",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/monalisa",
"html_url": "https://github.com/monalisa",
"followers_url": "https://api.github.com/users/monalisa/followers",
"following_url": "https://api.github.com/users/monalisa/following{/other_user}",
"gists_url": "https://api.github.com/users/monalisa/gists{/gist_id}",
"starred_url": "https://api.github.com/users/monalisa/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/monalisa/subscriptions",
"organizations_url": "https://api.github.com/users/monalisa/orgs",
"repos_url": "https://api.github.com/users/monalisa/repos",
"events_url": "https://api.github.com/users/monalisa/events{/privacy}",
"received_events_url": "https://api.github.com/users/monalisa/received_events",
"type": "User",
"user_view_type": "public",
"site_admin": false
}
],
"requested_teams": [],
"labels": [
{
"id": 19,
"node_id": "LA_kwABEw",
"url": "https://api.github.com/repos/github/Hello-World/labels/bug%20:bug:",
"name": "bug :bug:",
"color": "efe24f",
"default": false,
"description": "Something isn't working"
},
{
"id": 26,
"node_id": "LA_kwABGg",
"url": "https://api.github.com/repos/github/Hello-World/labels/fun%20size%20%F0%9F%8D%AB",
"name": "fun size 🍫",
"color": "f29c24",
"default": false,
"description": "Extra attention is needed"
},
{
"id": 33,
"node_id": "LA_kwABIQ",
"url": "https://api.github.com/repos/github/Hello-World/labels/%F0%9F%9A%92%20wontfix",
"name": "🚒 wontfix",
"color": "5891ce",
"default": false,
"description": "This will not be worked on"
}
],
"milestone": {
"url": "https://api.github.com/repos/github/Hello-World/milestones/1",
"html_url": "https://github.com/github/Hello-World/milestone/1",
"labels_url": "https://api.github.com/repos/github/Hello-World/milestones/1/labels",
"id": 1,
"node_id": "MI_kwABAQ",
"number": 1,
"title": "Open milestone",
"description": null,
"creator": {
"login": "monalisa",
"id": 2,
"node_id": "U_kgAC",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/monalisa",
"html_url": "https://github.com/monalisa",
"followers_url": "https://api.github.com/users/monalisa/followers",
"following_url": "https://api.github.com/users/monalisa/following{/other_user}",
"gists_url": "https://api.github.com/users/monalisa/gists{/gist_id}",
"starred_url": "https://api.github.com/users/monalisa/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/monalisa/subscriptions",
"organizations_url": "https://api.github.com/users/monalisa/orgs",
"repos_url": "https://api.github.com/users/monalisa/repos",
"events_url": "https://api.github.com/users/monalisa/events{/privacy}",
"received_events_url": "https://api.github.com/users/monalisa/received_events",
"type": "User",
"user_view_type": "public",
"site_admin": false
},
"open_issues": 2,
"closed_issues": 1,
"state": "open",
"created_at": "2025-08-01T18:44:30Z",
"updated_at": "2025-08-06T19:14:15Z",
"due_on": null,
"closed_at": null
},
"draft": false,
"commits_url": "https://api.github.com/repos/github/Hello-World/pulls/6/commits",
"review_comments_url": "https://api.github.com/repos/github/Hello-World/pulls/6/comments",
"review_comment_url": "https://api.github.com/repos/github/Hello-World/pulls/comments{/number}",
"comments_url": "https://api.github.com/repos/github/Hello-World/issues/6/comments",
"statuses_url": "https://api.github.com/repos/github/Hello-World/statuses/a3258d3434ecb2058b2784c8eb8610c2e9937a0d",
"head": {
"label": "github:branch-2ee3da8fde8a1adfe6d0809a1a414e4f",
"ref": "branch-2ee3da8fde8a1adfe6d0809a1a414e4f",
"sha": "a3258d3434ecb2058b2784c8eb8610c2e9937a0d",
"user": {
"login": "github",
"id": 5,
"node_id": "O_kgAF",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/github",
"html_url": "https://github.com/github",
"followers_url": "https://api.github.com/users/github/followers",
"following_url": "https://api.github.com/users/github/following{/other_user}",
"gists_url": "https://api.github.com/users/github/gists{/gist_id}",
"starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/github/subscriptions",
"organizations_url": "https://api.github.com/users/github/orgs",
"repos_url": "https://api.github.com/users/github/repos",
"events_url": "https://api.github.com/users/github/events{/privacy}",
"received_events_url": "https://api.github.com/users/github/received_events",
"type": "Organization",
"user_view_type": "public",
"site_admin": false
},
"repo": {
"id": 1,
"node_id": "R_kgAB",
"name": "Hello-World",
"full_name": "github/Hello-World",
"private": false,
"owner": {
"login": "github",
"id": 5,
"node_id": "O_kgAF",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/github",
"html_url": "https://github.com/github",
"followers_url": "https://api.github.com/users/github/followers",
"following_url": "https://api.github.com/users/github/following{/other_user}",
"gists_url": "https://api.github.com/users/github/gists{/gist_id}",
"starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/github/subscriptions",
"organizations_url": "https://api.github.com/users/github/orgs",
"repos_url": "https://api.github.com/users/github/repos",
"events_url": "https://api.github.com/users/github/events{/privacy}",
"received_events_url": "https://api.github.com/users/github/received_events",
"type": "Organization",
"user_view_type": "public",
"site_admin": false
},
"html_url": "https://github.com/github/Hello-World",
"description": null,
"fork": false,
"url": "https://api.github.com/repos/github/Hello-World",
"forks_url": "https://api.github.com/repos/github/Hello-World/forks",
"keys_url": "https://api.github.com/repos/github/Hello-World/keys{/key_id}",
"collaborators_url": "https://api.github.com/repos/github/Hello-World/collaborators{/collaborator}",
"teams_url": "https://api.github.com/repos/github/Hello-World/teams",
"hooks_url": "https://api.github.com/repos/github/Hello-World/hooks",
"issue_events_url": "https://api.github.com/repos/github/Hello-World/issues/events{/number}",
"events_url": "https://api.github.com/repos/github/Hello-World/events",
"assignees_url": "https://api.github.com/repos/github/Hello-World/assignees{/user}",
"branches_url": "https://api.github.com/repos/github/Hello-World/branches{/branch}",
"tags_url": "https://api.github.com/repos/github/Hello-World/tags",
"blobs_url": "https://api.github.com/repos/github/Hello-World/git/blobs{/sha}",
"git_tags_url": "https://api.github.com/repos/github/Hello-World/git/tags{/sha}",
"git_refs_url": "https://api.github.com/repos/github/Hello-World/git/refs{/sha}",
"trees_url": "https://api.github.com/repos/github/Hello-World/git/trees{/sha}",
"statuses_url": "https://api.github.com/repos/github/Hello-World/statuses/{sha}",
"languages_url": "https://api.github.com/repos/github/Hello-World/languages",
"stargazers_url": "https://api.github.com/repos/github/Hello-World/stargazers",
"contributors_url": "https://api.github.com/repos/github/Hello-World/contributors",
"subscribers_url": "https://api.github.com/repos/github/Hello-World/subscribers",
"subscription_url": "https://api.github.com/repos/github/Hello-World/subscription",
"commits_url": "https://api.github.com/repos/github/Hello-World/commits{/sha}",
"git_commits_url": "https://api.github.com/repos/github/Hello-World/git/commits{/sha}",
"comments_url": "https://api.github.com/repos/github/Hello-World/comments{/number}",
"issue_comment_url": "https://api.github.com/repos/github/Hello-World/issues/comments{/number}",
"contents_url": "https://api.github.com/repos/github/Hello-World/contents/{+path}",
"compare_url": "https://api.github.com/repos/github/Hello-World/compare/{base}...{head}",
"merges_url": "https://api.github.com/repos/github/Hello-World/merges",
"archive_url": "https://api.github.com/repos/github/Hello-World/{archive_format}{/ref}",
"downloads_url": "https://api.github.com/repos/github/Hello-World/downloads",
"issues_url": "https://api.github.com/repos/github/Hello-World/issues{/number}",
"pulls_url": "https://api.github.com/repos/github/Hello-World/pulls{/number}",
"milestones_url": "https://api.github.com/repos/github/Hello-World/milestones{/number}",
"notifications_url": "https://api.github.com/repos/github/Hello-World/notifications{?since,all,participating}",
"labels_url": "https://api.github.com/repos/github/Hello-World/labels{/name}",
"releases_url": "https://api.github.com/repos/github/Hello-World/releases{/id}",
"deployments_url": "https://api.github.com/repos/github/Hello-World/deployments",
"created_at": "2025-08-01T18:44:14Z",
"updated_at": "2025-08-01T18:48:38Z",
"pushed_at": "2025-08-01T18:44:50Z",
"git_url": "git://github.localhost/github/Hello-World.git",
"ssh_url": "ssh://git@localhost:3035/github/Hello-World.git",
"clone_url": "https://github.com/github/Hello-World.git",
"svn_url": "https://github.com/github/Hello-World",
"homepage": null,
"size": 6,
"stargazers_count": 0,
"watchers_count": 0,
"language": null,
"has_issues": true,
"has_projects": true,
"has_downloads": true,
"has_wiki": true,
"has_pages": false,
"has_discussions": false,
"forks_count": 0,
"mirror_url": null,
"archived": false,
"disabled": false,
"open_issues_count": 3,
"license": null,
"allow_forking": true,
"is_template": false,
"web_commit_signoff_required": false,
"topics": [],
"visibility": "public",
"forks": 0,
"open_issues": 3,
"watchers": 0,
"default_branch": "main"
}
},
"base": {
"label": "github:branch-0f4ceb14cbe39e4786ffbabb776da599",
"ref": "branch-0f4ceb14cbe39e4786ffbabb776da599",
"sha": "9a9f5a8d77bdc2540412900d3c930fe36a82b5ed",
"user": {
"login": "github",
"id": 5,
"node_id": "O_kgAF",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/github",
"html_url": "https://github.com/github",
"followers_url": "https://api.github.com/users/github/followers",
"following_url": "https://api.github.com/users/github/following{/other_user}",
"gists_url": "https://api.github.com/users/github/gists{/gist_id}",
"starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/github/subscriptions",
"organizations_url": "https://api.github.com/users/github/orgs",
"repos_url": "https://api.github.com/users/github/repos",
"events_url": "https://api.github.com/users/github/events{/privacy}",
"received_events_url": "https://api.github.com/users/github/received_events",
"type": "Organization",
"user_view_type": "public",
"site_admin": false
},
"repo": {
"id": 1,
"node_id": "R_kgAB",
"name": "Hello-World",
"full_name": "github/Hello-World",
"private": false,
"owner": {
"login": "github",
"id": 5,
"node_id": "O_kgAF",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/github",
"html_url": "https://github.com/github",
"followers_url": "https://api.github.com/users/github/followers",
"following_url": "https://api.github.com/users/github/following{/other_user}",
"gists_url": "https://api.github.com/users/github/gists{/gist_id}",
"starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/github/subscriptions",
"organizations_url": "https://api.github.com/users/github/orgs",
"repos_url": "https://api.github.com/users/github/repos",
"events_url": "https://api.github.com/users/github/events{/privacy}",
"received_events_url": "https://api.github.com/users/github/received_events",
"type": "Organization",
"user_view_type": "public",
"site_admin": false
},
"html_url": "https://github.com/github/Hello-World",
"description": null,
"fork": false,
"url": "https://api.github.com/repos/github/Hello-World",
"forks_url": "https://api.github.com/repos/github/Hello-World/forks",
"keys_url": "https://api.github.com/repos/github/Hello-World/keys{/key_id}",
"collaborators_url": "https://api.github.com/repos/github/Hello-World/collaborators{/collaborator}",
"teams_url": "https://api.github.com/repos/github/Hello-World/teams",
"hooks_url": "https://api.github.com/repos/github/Hello-World/hooks",
"issue_events_url": "https://api.github.com/repos/github/Hello-World/issues/events{/number}",
"events_url": "https://api.github.com/repos/github/Hello-World/events",
"assignees_url": "https://api.github.com/repos/github/Hello-World/assignees{/user}",
"branches_url": "https://api.github.com/repos/github/Hello-World/branches{/branch}",
"tags_url": "https://api.github.com/repos/github/Hello-World/tags",
"blobs_url": "https://api.github.com/repos/github/Hello-World/git/blobs{/sha}",
"git_tags_url": "https://api.github.com/repos/github/Hello-World/git/tags{/sha}",
"git_refs_url": "https://api.github.com/repos/github/Hello-World/git/refs{/sha}",
"trees_url": "https://api.github.com/repos/github/Hello-World/git/trees{/sha}",
"statuses_url": "https://api.github.com/repos/github/Hello-World/statuses/{sha}",
"languages_url": "https://api.github.com/repos/github/Hello-World/languages",
"stargazers_url": "https://api.github.com/repos/github/Hello-World/stargazers",
"contributors_url": "https://api.github.com/repos/github/Hello-World/contributors",
"subscribers_url": "https://api.github.com/repos/github/Hello-World/subscribers",
"subscription_url": "https://api.github.com/repos/github/Hello-World/subscription",
"commits_url": "https://api.github.com/repos/github/Hello-World/commits{/sha}",
"git_commits_url": "https://api.github.com/repos/github/Hello-World/git/commits{/sha}",
"comments_url": "https://api.github.com/repos/github/Hello-World/comments{/number}",
"issue_comment_url": "https://api.github.com/repos/github/Hello-World/issues/comments{/number}",
"contents_url": "https://api.github.com/repos/github/Hello-World/contents/{+path}",
"compare_url": "https://api.github.com/repos/github/Hello-World/compare/{base}...{head}",
"merges_url": "https://api.github.com/repos/github/Hello-World/merges",
"archive_url": "https://api.github.com/repos/github/Hello-World/{archive_format}{/ref}",
"downloads_url": "https://api.github.com/repos/github/Hello-World/downloads",
"issues_url": "https://api.github.com/repos/github/Hello-World/issues{/number}",
"pulls_url": "https://api.github.com/repos/github/Hello-World/pulls{/number}",
"milestones_url": "https://api.github.com/repos/github/Hello-World/milestones{/number}",
"notifications_url": "https://api.github.com/repos/github/Hello-World/notifications{?since,all,participating}",
"labels_url": "https://api.github.com/repos/github/Hello-World/labels{/name}",
"releases_url": "https://api.github.com/repos/github/Hello-World/releases{/id}",
"deployments_url": "https://api.github.com/repos/github/Hello-World/deployments",
"created_at": "2025-08-01T18:44:14Z",
"updated_at": "2025-08-01T18:48:38Z",
"pushed_at": "2025-08-01T18:44:50Z",
"git_url": "git://github.localhost/github/Hello-World.git",
"ssh_url": "ssh://git@localhost:3035/github/Hello-World.git",
"clone_url": "https://github.com/github/Hello-World.git",
"svn_url": "https://github.com/github/Hello-World",
"homepage": null,
"size": 6,
"stargazers_count": 0,
"watchers_count": 0,
"language": null,
"has_issues": true,
"has_projects": true,
"has_downloads": true,
"has_wiki": true,
"has_pages": false,
"has_discussions": false,
"forks_count": 0,
"mirror_url": null,
"archived": false,
"disabled": false,
"open_issues_count": 3,
"license": null,
"allow_forking": true,
"is_template": false,
"web_commit_signoff_required": false,
"topics": [],
"visibility": "public",
"forks": 0,
"open_issues": 3,
"watchers": 0,
"default_branch": "main"
}
},
"_links": {
"self": {
"href": "https://api.github.com/repos/github/Hello-World/pulls/6"
},
"html": {
"href": "https://github.com/github/Hello-World/pull/6"
},
"issue": {
"href": "https://api.github.com/repos/github/Hello-World/issues/6"
},
"comments": {
"href": "https://api.github.com/repos/github/Hello-World/issues/6/comments"
},
"review_comments": {
"href": "https://api.github.com/repos/github/Hello-World/pulls/6/comments"
},
"review_comment": {
"href": "https://api.github.com/repos/github/Hello-World/pulls/comments{/number}"
},
"commits": {
"href": "https://api.github.com/repos/github/Hello-World/pulls/6/commits"
},
"statuses": {
"href": "https://api.github.com/repos/github/Hello-World/statuses/a3258d3434ecb2058b2784c8eb8610c2e9937a0d"
}
},
"author_association": "MEMBER",
"auto_merge": null,
"active_lock_reason": null
},
"content_type": "PullRequest",
"creator": {
"login": "monalisa",
"id": 2,
"node_id": "U_kgAC",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/monalisa",
"html_url": "https://github.com/monalisa",
"followers_url": "https://api.github.com/users/monalisa/followers",
"following_url": "https://api.github.com/users/monalisa/following{/other_user}",
"gists_url": "https://api.github.com/users/monalisa/gists{/gist_id}",
"starred_url": "https://api.github.com/users/monalisa/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/monalisa/subscriptions",
"organizations_url": "https://api.github.com/users/monalisa/orgs",
"repos_url": "https://api.github.com/users/monalisa/repos",
"events_url": "https://api.github.com/users/monalisa/events{/privacy}",
"received_events_url": "https://api.github.com/users/monalisa/received_events",
"type": "User",
"user_view_type": "public",
"site_admin": false
},
"created_at": "2025-08-01T18:44:51Z",
"updated_at": "2025-08-06T19:25:18Z",
"archived_at": null,
"item_url": "https://api.github.com/orgs/github/projectsV2/1/items/13",
"fields": [
{
"id": 1,
"name": "Title",
"type": "title",
"value": {
"raw": "It seemed to me that any civilization that had so far lost its head as to need to include a set of detailed instructions for use in a packet of toothpicks, was no longer a civilization in which I could live and stay sane.",
"html": "It seemed to me that any civilization that had so far lost its head as to need to include a set of detailed instructions for use in a packet of toothpicks, was no longer a civilization in which I could live and stay sane.",
"number": 6,
"url": "https://github.com/5/1/pull/6",
"issue_id": 12,
"state": "open",
"state_reason": null,
"is_draft": false
}
},
{
"id": 2,
"name": "Assignees",
"type": "assignees",
"value": [
{
"login": "octocat",
"id": 175,
"node_id": "U_kgDMrw",
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
"user_view_type": "public",
"site_admin": false
}
]
},
{
"id": 3,
"name": "Status",
"type": "single_select",
"value": {
"id": "98236657",
"name": {
"raw": "Done",
"html": "Done"
},
"color": "PURPLE",
"description": {
"raw": "This has been completed",
"html": "This has been completed"
}
}
},
{
"id": 4,
"name": "Labels",
"type": "labels",
"value": [
{
"id": 19,
"node_id": "LA_kwABEw",
"url": "https://api.github.com/repos/github/Hello-World/labels/bug%20:bug:",
"name": "bug :bug:",
"color": "efe24f",
"default": false,
"description": "Something isn't working"
},
{
"id": 26,
"node_id": "LA_kwABGg",
"url": "https://api.github.com/repos/github/Hello-World/labels/fun%20size%20%F0%9F%8D%AB",
"name": "fun size 🍫",
"color": "f29c24",
"default": false,
"description": "Extra attention is needed"
},
{
"id": 33,
"node_id": "LA_kwABIQ",
"url": "https://api.github.com/repos/github/Hello-World/labels/%F0%9F%9A%92%20wontfix",
"name": "🚒 wontfix",
"color": "5891ce",
"default": false,
"description": "This will not be worked on"
}
]
},
{
"id": 5,
"name": "Linked pull requests",
"type": "linked_pull_requests",
"value": []
},
{
"id": 6,
"name": "Milestone",
"type": "milestone",
"value": {
"url": "https://api.github.com/repos/github/Hello-World/milestones/1",
"html_url": "https://github.com/github/Hello-World/milestone/1",
"labels_url": "https://api.github.com/repos/github/Hello-World/milestones/1/labels",
"id": 1,
"node_id": "MI_kwABAQ",
"number": 1,
"title": "Open milestone",
"description": null,
"creator": {
"login": "octocat",
"id": 175,
"node_id": "U_kgDMrw",
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
"user_view_type": "public",
"site_admin": false
},
"open_issues": 2,
"closed_issues": 1,
"state": "open",
"created_at": "2025-08-01T18:44:30Z",
"updated_at": "2025-08-06T19:14:15Z",
"due_on": null,
"closed_at": null
}
},
{
"id": 7,
"name": "Repository",
"type": "repository",
"value": {
"id": 1,
"node_id": "R_kgAB",
"name": "Hello-World",
"full_name": "github/Hello-World",
"private": false,
"owner": {
"login": "github",
"id": 5,
"node_id": "O_kgAF",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/github",
"html_url": "https://github.com/github",
"followers_url": "https://api.github.com/users/github/followers",
"following_url": "https://api.github.com/users/github/following{/other_user}",
"gists_url": "https://api.github.com/users/github/gists{/gist_id}",
"starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/github/subscriptions",
"organizations_url": "https://api.github.com/users/github/orgs",
"repos_url": "https://api.github.com/users/github/repos",
"events_url": "https://api.github.com/users/github/events{/privacy}",
"received_events_url": "https://api.github.com/users/github/received_events",
"type": "Organization",
"user_view_type": "public",
"site_admin": false
},
"html_url": "https://github.com/github/Hello-World",
"description": null,
"fork": false,
"url": "https://api.github.com/repos/github/Hello-World",
"forks_url": "https://api.github.com/repos/github/Hello-World/forks",
"keys_url": "https://api.github.com/repos/github/Hello-World/keys{/key_id}",
"collaborators_url": "https://api.github.com/repos/github/Hello-World/collaborators{/collaborator}",
"teams_url": "https://api.github.com/repos/github/Hello-World/teams",
"hooks_url": "https://api.github.com/repos/github/Hello-World/hooks",
"issue_events_url": "https://api.github.com/repos/github/Hello-World/issues/events{/number}",
"events_url": "https://api.github.com/repos/github/Hello-World/events",
"assignees_url": "https://api.github.com/repos/github/Hello-World/assignees{/user}",
"branches_url": "https://api.github.com/repos/github/Hello-World/branches{/branch}",
"tags_url": "https://api.github.com/repos/github/Hello-World/tags",
"blobs_url": "https://api.github.com/repos/github/Hello-World/git/blobs{/sha}",
"git_tags_url": "https://api.github.com/repos/github/Hello-World/git/tags{/sha}",
"git_refs_url": "https://api.github.com/repos/github/Hello-World/git/refs{/sha}",
"trees_url": "https://api.github.com/repos/github/Hello-World/git/trees{/sha}",
"statuses_url": "https://api.github.com/repos/github/Hello-World/statuses/{sha}",
"languages_url": "https://api.github.com/repos/github/Hello-World/languages",
"stargazers_url": "https://api.github.com/repos/github/Hello-World/stargazers",
"contributors_url": "https://api.github.com/repos/github/Hello-World/contributors",
"subscribers_url": "https://api.github.com/repos/github/Hello-World/subscribers",
"subscription_url": "https://api.github.com/repos/github/Hello-World/subscription",
"commits_url": "https://api.github.com/repos/github/Hello-World/commits{/sha}",
"git_commits_url": "https://api.github.com/repos/github/Hello-World/git/commits{/sha}",
"comments_url": "https://api.github.com/repos/github/Hello-World/comments{/number}",
"issue_comment_url": "https://api.github.com/repos/github/Hello-World/issues/comments{/number}",
"contents_url": "https://api.github.com/repos/github/Hello-World/contents/{+path}",
"compare_url": "https://api.github.com/repos/github/Hello-World/compare/{base}...{head}",
"merges_url": "https://api.github.com/repos/github/Hello-World/merges",
"archive_url": "https://api.github.com/repos/github/Hello-World/{archive_format}{/ref}",
"downloads_url": "https://api.github.com/repos/github/Hello-World/downloads",
"issues_url": "https://api.github.com/repos/github/Hello-World/issues{/number}",
"pulls_url": "https://api.github.com/repos/github/Hello-World/pulls{/number}",
"milestones_url": "https://api.github.com/repos/github/Hello-World/milestones{/number}",
"notifications_url": "https://api.github.com/repos/github/Hello-World/notifications{?since,all,participating}",
"labels_url": "https://api.github.com/repos/github/Hello-World/labels{/name}",
"releases_url": "https://api.github.com/repos/github/Hello-World/releases{/id}",
"deployments_url": "https://api.github.com/repos/github/Hello-World/deployments"
}
},
{
"id": 8,
"name": "Type",
"type": "issue_type",
"value": null
},
{
"id": 9,
"name": "Reviewers",
"type": "reviewers",
"value": [
{
"type": "ReviewRequest",
"status": "pending",
"reviewer": {
"avatarUrl": "https://github.com/images/error/octocat_happy.gif",
"id": 2,
"login": "monalisa",
"url": "https://github.com/monalisa",
"name": "monalisa",
"type": "User"
}
}
]
},
{
"id": 10,
"name": "Parent issue",
"type": "parent_issue",
"value": null
},
{
"id": 11,
"name": "Sub-issues progress",
"type": "sub_issues_progress",
"value": null
}
]
}`
