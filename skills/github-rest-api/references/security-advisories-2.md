# REST API endpoints for repository security advisories

# REST API endpoints for repository security advisories

> Use the REST API to view and manage repository security advisories.

## List repository security advisories for an organization

Lists repository security advisories for an organization.

The authenticated user must be an owner or security manager for the organization to use this endpoint.

OAuth app tokens and personal access tokens (classic) need the `repo` or `repository_advisories:write` scope to use this endpoint.

### Fine-grained access tokens for "List repository security advisories for an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Repository security advisories" repository permissions (write)

### Parameters for "List repository security advisories for an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| directionstringThe direction to sort the results by.Default:descCan be one of:asc,desc |
| sortstringThe property to sort the results by.Default:createdCan be one of:created,updated,published |
| beforestringA cursor, as given in theLink header. If specified, the query only searches for results before this cursor. For more information, see "Using pagination in the REST API." |
| afterstringA cursor, as given in theLink header. If specified, the query only searches for results after this cursor. For more information, see "Using pagination in the REST API." |
| per_pageintegerThe number of advisories to return per page. For more information, see "Using pagination in the REST API."Default:30 |
| statestringFilter by the state of the repository advisories. Only advisories of this state will be returned.Can be one of:triage,draft,published,closed |

### HTTP response status codes for "List repository security advisories for an organization"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 400 | Bad Request |
| 404 | Resource not found |

### Code samples for "List repository security advisories for an organization"

#### Request example

get/orgs/{org}/security-advisories

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/security-advisories`

Response

-
-

`Status: 200``[
{
"ghsa_id": "GHSA-abcd-1234-efgh",
"cve_id": "CVE-2050-00000",
"url": "https://api.github.com/repos/repo/a-package/security-advisories/GHSA-abcd-1234-efgh",
"html_url": "https://github.com/repo/a-package/security/advisories/GHSA-abcd-1234-efgh",
"summary": "A short summary of the advisory.",
"description": "A detailed description of what the advisory entails.",
"severity": "critical",
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
"publisher": {
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
"identifiers": [
{
"type": "GHSA",
"value": "GHSA-abcd-1234-efgh"
},
{
"type": "CVE",
"value": "CVE-2050-00000"
}
],
"state": "published",
"created_at": "2020-01-01T00:00:00Z",
"updated_at": "2020-01-02T00:00:00Z",
"published_at": "2020-01-03T00:00:00Z",
"closed_at": null,
"withdrawn_at": null,
"submission": null,
"vulnerabilities": [
{
"package": {
"ecosystem": "pip",
"name": "a-package"
},
"vulnerable_version_range": ">= 1.0.0, < 1.0.1",
"patched_versions": "1.0.1",
"vulnerable_functions": [
"function1"
]
},
{
"package": {
"ecosystem": "pip",
"name": "another-package"
},
"vulnerable_version_range": ">= 1.0.0, < 1.0.2",
"patched_versions": "1.0.2",
"vulnerable_functions": [
"function2"
]
}
],
"cvss": {
"vector_string": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
"score": 9.8
},
"cvss_severities": {
"cvss_v3": {
"vector_string": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
"score": 9.8
},
"cvss_v4": {
"vector_string": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N",
"score": 9.3
}
},
"cwes": [
{
"cwe_id": "CWE-123",
"name": "A CWE"
}
],
"cwe_ids": [
"CWE-123"
],
"credits": [
{
"login": "octocat",
"type": "analyst"
}
],
"credits_detailed": [
{
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
"type": "analyst",
"state": "accepted"
}
],
"collaborating_users": [
{
"login": "octokitten",
"id": 1,
"node_id": "MDQ6VXNlcjE=",
"avatar_url": "https://github.com/images/error/octokitten_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/octokitten",
"html_url": "https://github.com/octokitten",
"followers_url": "https://api.github.com/users/octokitten/followers",
"following_url": "https://api.github.com/users/octokitten/following{/other_user}",
"gists_url": "https://api.github.com/users/octokitten/gists{/gist_id}",
"starred_url": "https://api.github.com/users/octokitten/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/octokitten/subscriptions",
"organizations_url": "https://api.github.com/users/octokitten/orgs",
"repos_url": "https://api.github.com/users/octokitten/repos",
"events_url": "https://api.github.com/users/octokitten/events{/privacy}",
"received_events_url": "https://api.github.com/users/octokitten/received_events",
"type": "User",
"site_admin": false
}
],
"collaborating_teams": [
{
"name": "Justice League",
"id": 1,
"node_id": "MDQ6VGVhbTE=",
"slug": "justice-league",
"description": "A great team.",
"privacy": "closed",
"notification_setting": "notifications_enabled",
"url": "https://api.github.com/teams/1",
"html_url": "https://github.com/orgs/github/teams/justice-league",
"members_url": "https://api.github.com/teams/1/members{/member}",
"repositories_url": "https://api.github.com/teams/1/repos",
"permission": "admin",
"parent": null
}
],
"private_fork": null
},
{
"ghsa_id": "GHSA-1234-5678-9012",
"cve_id": "CVE-2051-0000",
"url": "https://api.github.com/repos/repo/a-package/security-advisories/GHSA-1234-5678-9012",
"html_url": "https://github.com/repo/a-package/security/advisories/GHSA-1234-5678-9012",
"summary": "A short summary of the advisory.",
"description": "A detailed description of what the advisory entails.",
"severity": "low",
"author": {
"login": "monauser",
"id": 2,
"node_id": "MDQ6VXNlcjE=",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/monauser",
"html_url": "https://github.com/monauser",
"followers_url": "https://api.github.com/users/monauser/followers",
"following_url": "https://api.github.com/users/monauser/following{/other_user}",
"gists_url": "https://api.github.com/users/monauser/gists{/gist_id}",
"starred_url": "https://api.github.com/users/monauser/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/monauser/subscriptions",
"organizations_url": "https://api.github.com/users/monauser/orgs",
"repos_url": "https://api.github.com/users/monauser/repos",
"events_url": "https://api.github.com/users/monauser/events{/privacy}",
"received_events_url": "https://api.github.com/users/monauser/received_events",
"type": "User",
"site_admin": false
},
"publisher": {
"login": "monalisa",
"id": 3,
"node_id": "MDQ6VXNlcjE=",
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
"site_admin": false
},
"identifiers": [
{
"type": "GHSA",
"value": "GHSA-1234-5678-9012"
},
{
"type": "CVE",
"value": "CVE-2051-00000"
}
],
"state": "published",
"created_at": "2020-01-03T00:00:00Z",
"updated_at": "2020-01-04T00:00:00Z",
"published_at": "2020-01-04T00:00:00Z",
"closed_at": null,
"withdrawn_at": null,
"submission": {
"accepted": true
},
"vulnerabilities": [
{
"package": {
"ecosystem": "pip",
"name": "a-package"
},
"vulnerable_version_range": ">= 1.0.0, < 1.0.1",
"patched_versions": "1.0.1",
"vulnerable_functions": [
"function1"
]
},
{
"package": {
"ecosystem": "pip",
"name": "another-package"
},
"vulnerable_version_range": ">= 1.0.0, < 1.0.2",
"patched_versions": "1.0.2",
"vulnerable_functions": [
"function2"
]
}
],
"cvss": {
"vector_string": "AV:P/AC:H/PR:H/UI:R/S:U/C:N/I:L/A:N",
"score": 1.6
},
"cvss_severities": {
"cvss_v3": {
"vector_string": "CVSS:3.1/AV:P/AC:H/PR:H/UI:R/S:U/C:N/I:L/A:N",
"score": 1.6
},
"cvss_v4": {
"vector_string": "CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N",
"score": 7.1
}
},
"cwes": [
{
"cwe_id": "CWE-456",
"name": "A CWE 2.0"
}
],
"cwe_ids": [
"CWE-456"
],
"credits": [
{
"login": "monauser",
"type": "reporter"
}
],
"credits_detailed": [
{
"user": {
"login": "monauser",
"id": 2,
"node_id": "MDQ6VXNlcjE=",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/monauser",
"html_url": "https://github.com/monauser",
"followers_url": "https://api.github.com/users/monauser/followers",
"following_url": "https://api.github.com/users/monauser/following{/other_user}",
"gists_url": "https://api.github.com/users/monauser/gists{/gist_id}",
"starred_url": "https://api.github.com/users/monauser/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/monauser/subscriptions",
"organizations_url": "https://api.github.com/users/monauser/orgs",
"repos_url": "https://api.github.com/users/monauser/repos",
"events_url": "https://api.github.com/users/monauser/events{/privacy}",
"received_events_url": "https://api.github.com/users/monauser/received_events",
"type": "User",
"site_admin": false
},
"type": "reporter",
"state": "accepted"
}
],
"collaborating_users": [
{
"login": "octokitten",
"id": 1,
"node_id": "MDQ6VXNlcjE=",
"avatar_url": "https://github.com/images/error/octokitten_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/octokitten",
"html_url": "https://github.com/octokitten",
"followers_url": "https://api.github.com/users/octokitten/followers",
"following_url": "https://api.github.com/users/octokitten/following{/other_user}",
"gists_url": "https://api.github.com/users/octokitten/gists{/gist_id}",
"starred_url": "https://api.github.com/users/octokitten/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/octokitten/subscriptions",
"organizations_url": "https://api.github.com/users/octokitten/orgs",
"repos_url": "https://api.github.com/users/octokitten/repos",
"events_url": "https://api.github.com/users/octokitten/events{/privacy}",
"received_events_url": "https://api.github.com/users/octokitten/received_events",
"type": "User",
"site_admin": false
}
],
"collaborating_teams": [
{
"name": "Justice League",
"id": 1,
"node_id": "MDQ6VGVhbTE=",
"slug": "justice-league",
"description": "A great team.",
"privacy": "closed",
"notification_setting": "notifications_enabled",
"url": "https://api.github.com/teams/1",
"html_url": "https://github.com/orgs/github/teams/justice-league",
"members_url": "https://api.github.com/teams/1/members{/member}",
"repositories_url": "https://api.github.com/teams/1/repos",
"permission": "admin",
"parent": null
}
],
"private_fork": {
"id": 217723378,
"node_id": "MDEwOlJlcG9zaXRvcnkyMTc3MjMzNzg=",
"name": "octo-repo-ghsa-1234-5678-9012",
"full_name": "octo-org/octo-repo-ghsa-1234-5678-9012",
"owner": {
"login": "octo-org",
"id": 6811672,
"node_id": "MDEyOk9yZ2FuaXphdGlvbjY4MTE2NzI=",
"avatar_url": "https://avatars3.githubusercontent.com/u/6811672?v=4",
"gravatar_id": "",
"url": "https://api.github.com/users/octo-org",
"html_url": "https://github.com/octo-org",
"followers_url": "https://api.github.com/users/octo-org/followers",
"following_url": "https://api.github.com/users/octo-org/following{/other_user}",
"gists_url": "https://api.github.com/users/octo-org/gists{/gist_id}",
"starred_url": "https://api.github.com/users/octo-org/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/octo-org/subscriptions",
"organizations_url": "https://api.github.com/users/octo-org/orgs",
"repos_url": "https://api.github.com/users/octo-org/repos",
"events_url": "https://api.github.com/users/octo-org/events{/privacy}",
"received_events_url": "https://api.github.com/users/octo-org/received_events",
"type": "Organization",
"site_admin": false
},
"private": true,
"html_url": "https://github.com/octo-org/octo-repo-ghsa-1234-5678-9012",
"description": null,
"fork": false,
"url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012",
"archive_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/{archive_format}{/ref}",
"assignees_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/assignees{/user}",
"blobs_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/git/blobs{/sha}",
"branches_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/branches{/branch}",
"collaborators_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/collaborators{/collaborator}",
"comments_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/comments{/number}",
"commits_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/commits{/sha}",
"compare_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/compare/{base}...{head}",
"contents_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/contents/{+path}",
"contributors_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/contributors",
"deployments_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/deployments",
"downloads_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/downloads",
"events_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/events",
"forks_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/forks",
"git_commits_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/git/commits{/sha}",
"git_refs_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/git/refs{/sha}",
"git_tags_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/git/tags{/sha}",
"hooks_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/hooks",
"issue_comment_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/issues/comments{/number}",
"issue_events_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/issues/events{/number}",
"issues_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/issues{/number}",
"keys_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/keys{/key_id}",
"labels_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/labels{/name}",
"languages_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/languages",
"merges_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/merges",
"milestones_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/milestones{/number}",
"notifications_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/notifications{?since,all,participating}",
"pulls_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/pulls{/number}",
"releases_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/releases{/id}",
"stargazers_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/stargazers",
"statuses_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/statuses/{sha}",
"subscribers_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/subscribers",
"subscription_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/subscription",
"tags_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/tags",
"teams_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/teams",
"trees_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/git/trees{/sha}"
}
}
]`

## List repository security advisories

Lists security advisories in a repository.

The authenticated user can access unpublished security advisories from a repository if they are a security manager or administrator of that repository, or if they are a collaborator on any security advisory.

OAuth app tokens and personal access tokens (classic) need the `repo` or `repository_advisories:read` scope to to get a published security advisory in a private repository, or any unpublished security advisory that the authenticated user has access to.

### Fine-grained access tokens for "List repository security advisories"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Repository security advisories" repository permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "List repository security advisories"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| directionstringThe direction to sort the results by.Default:descCan be one of:asc,desc |
| sortstringThe property to sort the results by.Default:createdCan be one of:created,updated,published |
| beforestringA cursor, as given in theLink header. If specified, the query only searches for results before this cursor. For more information, see "Using pagination in the REST API." |
| afterstringA cursor, as given in theLink header. If specified, the query only searches for results after this cursor. For more information, see "Using pagination in the REST API." |
| per_pageintegerThe number of advisories to return per page. For more information, see "Using pagination in the REST API."Default:30 |
| statestringFilter by state of the repository advisories. Only advisories of this state will be returned.Can be one of:triage,draft,published,closed |

### HTTP response status codes for "List repository security advisories"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 400 | Bad Request |
| 404 | Resource not found |

### Code samples for "List repository security advisories"

#### Request example

get/repos/{owner}/{repo}/security-advisories

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/security-advisories`

Response

-
-

`Status: 200``[
{
"ghsa_id": "GHSA-abcd-1234-efgh",
"cve_id": "CVE-2050-00000",
"url": "https://api.github.com/repos/repo/a-package/security-advisories/GHSA-abcd-1234-efgh",
"html_url": "https://github.com/repo/a-package/security/advisories/GHSA-abcd-1234-efgh",
"summary": "A short summary of the advisory.",
"description": "A detailed description of what the advisory entails.",
"severity": "critical",
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
"publisher": {
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
"identifiers": [
{
"type": "GHSA",
"value": "GHSA-abcd-1234-efgh"
},
{
"type": "CVE",
"value": "CVE-2050-00000"
}
],
"state": "published",
"created_at": "2020-01-01T00:00:00Z",
"updated_at": "2020-01-02T00:00:00Z",
"published_at": "2020-01-03T00:00:00Z",
"closed_at": null,
"withdrawn_at": null,
"submission": null,
"vulnerabilities": [
{
"package": {
"ecosystem": "pip",
"name": "a-package"
},
"vulnerable_version_range": ">= 1.0.0, < 1.0.1",
"patched_versions": "1.0.1",
"vulnerable_functions": [
"function1"
]
},
{
"package": {
"ecosystem": "pip",
"name": "another-package"
},
"vulnerable_version_range": ">= 1.0.0, < 1.0.2",
"patched_versions": "1.0.2",
"vulnerable_functions": [
"function2"
]
}
],
"cvss": {
"vector_string": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
"score": 9.8
},
"cvss_severities": {
"cvss_v3": {
"vector_string": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
"score": 9.8
},
"cvss_v4": {
"vector_string": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N",
"score": 9.3
}
},
"cwes": [
{
"cwe_id": "CWE-123",
"name": "A CWE"
}
],
"cwe_ids": [
"CWE-123"
],
"credits": [
{
"login": "octocat",
"type": "analyst"
}
],
"credits_detailed": [
{
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
"type": "analyst",
"state": "accepted"
}
],
"collaborating_users": [
{
"login": "octokitten",
"id": 1,
"node_id": "MDQ6VXNlcjE=",
"avatar_url": "https://github.com/images/error/octokitten_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/octokitten",
"html_url": "https://github.com/octokitten",
"followers_url": "https://api.github.com/users/octokitten/followers",
"following_url": "https://api.github.com/users/octokitten/following{/other_user}",
"gists_url": "https://api.github.com/users/octokitten/gists{/gist_id}",
"starred_url": "https://api.github.com/users/octokitten/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/octokitten/subscriptions",
"organizations_url": "https://api.github.com/users/octokitten/orgs",
"repos_url": "https://api.github.com/users/octokitten/repos",
"events_url": "https://api.github.com/users/octokitten/events{/privacy}",
"received_events_url": "https://api.github.com/users/octokitten/received_events",
"type": "User",
"site_admin": false
}
],
"collaborating_teams": [
{
"name": "Justice League",
"id": 1,
"node_id": "MDQ6VGVhbTE=",
"slug": "justice-league",
"description": "A great team.",
"privacy": "closed",
"notification_setting": "notifications_enabled",
"url": "https://api.github.com/teams/1",
"html_url": "https://github.com/orgs/github/teams/justice-league",
"members_url": "https://api.github.com/teams/1/members{/member}",
"repositories_url": "https://api.github.com/teams/1/repos",
"permission": "admin",
"parent": null
}
],
"private_fork": null
},
{
"ghsa_id": "GHSA-1234-5678-9012",
"cve_id": "CVE-2051-0000",
"url": "https://api.github.com/repos/repo/a-package/security-advisories/GHSA-1234-5678-9012",
"html_url": "https://github.com/repo/a-package/security/advisories/GHSA-1234-5678-9012",
"summary": "A short summary of the advisory.",
"description": "A detailed description of what the advisory entails.",
"severity": "low",
"author": {
"login": "monauser",
"id": 2,
"node_id": "MDQ6VXNlcjE=",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/monauser",
"html_url": "https://github.com/monauser",
"followers_url": "https://api.github.com/users/monauser/followers",
"following_url": "https://api.github.com/users/monauser/following{/other_user}",
"gists_url": "https://api.github.com/users/monauser/gists{/gist_id}",
"starred_url": "https://api.github.com/users/monauser/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/monauser/subscriptions",
"organizations_url": "https://api.github.com/users/monauser/orgs",
"repos_url": "https://api.github.com/users/monauser/repos",
"events_url": "https://api.github.com/users/monauser/events{/privacy}",
"received_events_url": "https://api.github.com/users/monauser/received_events",
"type": "User",
"site_admin": false
},
"publisher": {
"login": "monalisa",
"id": 3,
"node_id": "MDQ6VXNlcjE=",
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
"site_admin": false
},
"identifiers": [
{
"type": "GHSA",
"value": "GHSA-1234-5678-9012"
},
{
"type": "CVE",
"value": "CVE-2051-00000"
}
],
"state": "published",
"created_at": "2020-01-03T00:00:00Z",
"updated_at": "2020-01-04T00:00:00Z",
"published_at": "2020-01-04T00:00:00Z",
"closed_at": null,
"withdrawn_at": null,
"submission": {
"accepted": true
},
"vulnerabilities": [
{
"package": {
"ecosystem": "pip",
"name": "a-package"
},
"vulnerable_version_range": ">= 1.0.0, < 1.0.1",
"patched_versions": "1.0.1",
"vulnerable_functions": [
"function1"
]
},
{
"package": {
"ecosystem": "pip",
"name": "another-package"
},
"vulnerable_version_range": ">= 1.0.0, < 1.0.2",
"patched_versions": "1.0.2",
"vulnerable_functions": [
"function2"
]
}
],
"cvss": {
"vector_string": "AV:P/AC:H/PR:H/UI:R/S:U/C:N/I:L/A:N",
"score": 1.6
},
"cvss_severities": {
"cvss_v3": {
"vector_string": "CVSS:3.1/AV:P/AC:H/PR:H/UI:R/S:U/C:N/I:L/A:N",
"score": 1.6
},
"cvss_v4": {
"vector_string": "CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N",
"score": 7.1
}
},
"cwes": [
{
"cwe_id": "CWE-456",
"name": "A CWE 2.0"
}
],
"cwe_ids": [
"CWE-456"
],
"credits": [
{
"login": "monauser",
"type": "reporter"
}
],
"credits_detailed": [
{
"user": {
"login": "monauser",
"id": 2,
"node_id": "MDQ6VXNlcjE=",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/monauser",
"html_url": "https://github.com/monauser",
"followers_url": "https://api.github.com/users/monauser/followers",
"following_url": "https://api.github.com/users/monauser/following{/other_user}",
"gists_url": "https://api.github.com/users/monauser/gists{/gist_id}",
"starred_url": "https://api.github.com/users/monauser/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/monauser/subscriptions",
"organizations_url": "https://api.github.com/users/monauser/orgs",
"repos_url": "https://api.github.com/users/monauser/repos",
"events_url": "https://api.github.com/users/monauser/events{/privacy}",
"received_events_url": "https://api.github.com/users/monauser/received_events",
"type": "User",
"site_admin": false
},
"type": "reporter",
"state": "accepted"
}
],
"collaborating_users": [
{
"login": "octokitten",
"id": 1,
"node_id": "MDQ6VXNlcjE=",
"avatar_url": "https://github.com/images/error/octokitten_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/octokitten",
"html_url": "https://github.com/octokitten",
"followers_url": "https://api.github.com/users/octokitten/followers",
"following_url": "https://api.github.com/users/octokitten/following{/other_user}",
"gists_url": "https://api.github.com/users/octokitten/gists{/gist_id}",
"starred_url": "https://api.github.com/users/octokitten/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/octokitten/subscriptions",
"organizations_url": "https://api.github.com/users/octokitten/orgs",
"repos_url": "https://api.github.com/users/octokitten/repos",
"events_url": "https://api.github.com/users/octokitten/events{/privacy}",
"received_events_url": "https://api.github.com/users/octokitten/received_events",
"type": "User",
"site_admin": false
}
],
"collaborating_teams": [
{
"name": "Justice League",
"id": 1,
"node_id": "MDQ6VGVhbTE=",
"slug": "justice-league",
"description": "A great team.",
"privacy": "closed",
"notification_setting": "notifications_enabled",
"url": "https://api.github.com/teams/1",
"html_url": "https://github.com/orgs/github/teams/justice-league",
"members_url": "https://api.github.com/teams/1/members{/member}",
"repositories_url": "https://api.github.com/teams/1/repos",
"permission": "admin",
"parent": null
}
],
"private_fork": {
"id": 217723378,
"node_id": "MDEwOlJlcG9zaXRvcnkyMTc3MjMzNzg=",
"name": "octo-repo-ghsa-1234-5678-9012",
"full_name": "octo-org/octo-repo-ghsa-1234-5678-9012",
"owner": {
"login": "octo-org",
"id": 6811672,
"node_id": "MDEyOk9yZ2FuaXphdGlvbjY4MTE2NzI=",
"avatar_url": "https://avatars3.githubusercontent.com/u/6811672?v=4",
"gravatar_id": "",
"url": "https://api.github.com/users/octo-org",
"html_url": "https://github.com/octo-org",
"followers_url": "https://api.github.com/users/octo-org/followers",
"following_url": "https://api.github.com/users/octo-org/following{/other_user}",
"gists_url": "https://api.github.com/users/octo-org/gists{/gist_id}",
"starred_url": "https://api.github.com/users/octo-org/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/octo-org/subscriptions",
"organizations_url": "https://api.github.com/users/octo-org/orgs",
"repos_url": "https://api.github.com/users/octo-org/repos",
"events_url": "https://api.github.com/users/octo-org/events{/privacy}",
"received_events_url": "https://api.github.com/users/octo-org/received_events",
"type": "Organization",
"site_admin": false
},
"private": true,
"html_url": "https://github.com/octo-org/octo-repo-ghsa-1234-5678-9012",
"description": null,
"fork": false,
"url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012",
"archive_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/{archive_format}{/ref}",
"assignees_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/assignees{/user}",
"blobs_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/git/blobs{/sha}",
"branches_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/branches{/branch}",
"collaborators_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/collaborators{/collaborator}",
"comments_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/comments{/number}",
"commits_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/commits{/sha}",
"compare_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/compare/{base}...{head}",
"contents_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/contents/{+path}",
"contributors_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/contributors",
"deployments_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/deployments",
"downloads_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/downloads",
"events_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/events",
"forks_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/forks",
"git_commits_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/git/commits{/sha}",
"git_refs_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/git/refs{/sha}",
"git_tags_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/git/tags{/sha}",
"hooks_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/hooks",
"issue_comment_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/issues/comments{/number}",
"issue_events_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/issues/events{/number}",
"issues_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/issues{/number}",
"keys_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/keys{/key_id}",
"labels_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/labels{/name}",
"languages_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/languages",
"merges_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/merges",
"milestones_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/milestones{/number}",
"notifications_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/notifications{?since,all,participating}",
"pulls_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/pulls{/number}",
"releases_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/releases{/id}",
"stargazers_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/stargazers",
"statuses_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/statuses/{sha}",
"subscribers_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/subscribers",
"subscription_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/subscription",
"tags_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/tags",
"teams_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/teams",
"trees_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-1234-5678-9012/git/trees{/sha}"
}
}
]`

## Create a repository security advisory

Creates a new repository security advisory.

In order to create a draft repository security advisory, the authenticated user must be a security manager or administrator of that repository.

OAuth app tokens and personal access tokens (classic) need the `repo` or `repository_advisories:write` scope to use this endpoint.

### Fine-grained access tokens for "Create a repository security advisory"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Repository security advisories" repository permissions (write)

### Parameters for "Create a repository security advisory"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| summarystringRequiredA short summary of the advisory. |
| descriptionstringRequiredA detailed description of what the advisory impacts. |
| cve_idstring or nullThe Common Vulnerabilities and Exposures (CVE) ID. |
| vulnerabilitiesarray of objectsRequiredA product affected by the vulnerability detailed in a repository security advisory. |
| Name, Type, DescriptionpackageobjectRequiredThe name of the package affected by the vulnerability.Name, Type, DescriptionecosystemstringRequiredThe package's language or package management ecosystem.Can be one of:rubygems,npm,pip,maven,nuget,composer,go,rust,erlang,actions,pub,other,swiftnamestring or nullThe unique package name within its ecosystem.vulnerable_version_rangestring or nullThe range of the package versions affected by the vulnerability.patched_versionsstring or nullThe package version(s) that resolve the vulnerability.vulnerable_functionsarray of strings or nullThe functions in the package that are affected. |
| Name, Type, Description |
| packageobjectRequiredThe name of the package affected by the vulnerability. |
| Name, Type, DescriptionecosystemstringRequiredThe package's language or package management ecosystem.Can be one of:rubygems,npm,pip,maven,nuget,composer,go,rust,erlang,actions,pub,other,swiftnamestring or nullThe unique package name within its ecosystem. |
| Name, Type, Description |
| ecosystemstringRequiredThe package's language or package management ecosystem.Can be one of:rubygems,npm,pip,maven,nuget,composer,go,rust,erlang,actions,pub,other,swift |
| namestring or nullThe unique package name within its ecosystem. |
| vulnerable_version_rangestring or nullThe range of the package versions affected by the vulnerability. |
| patched_versionsstring or nullThe package version(s) that resolve the vulnerability. |
| vulnerable_functionsarray of strings or nullThe functions in the package that are affected. |
| cwe_idsarray of strings or nullA list of Common Weakness Enumeration (CWE) IDs. |
| creditsarray of objects or nullA list of users receiving credit for their participation in the security advisory. |
| Name, Type, DescriptionloginstringRequiredThe username of the user credited.typestringRequiredThe type of credit the user is receiving.Can be one of:analyst,finder,reporter,coordinator,remediation_developer,remediation_reviewer,remediation_verifier,tool,sponsor,other |
| Name, Type, Description |
| loginstringRequiredThe username of the user credited. |
| typestringRequiredThe type of credit the user is receiving.Can be one of:analyst,finder,reporter,coordinator,remediation_developer,remediation_reviewer,remediation_verifier,tool,sponsor,other |
| severitystring or nullThe severity of the advisory. You must choose between setting this field orcvss_vector_string.Can be one of:critical,high,medium,low,null |
| cvss_vector_stringstring or nullThe CVSS vector that calculates the severity of the advisory. You must choose between setting this field orseverity. |
| start_private_forkbooleanWhether to create a temporary private fork of the repository to collaborate on a fix.Default:false |

### HTTP response status codes for "Create a repository security advisory"

| Status code | Description |
| --- | --- |
| 201 | Created |
| 403 | Forbidden |
| 404 | Resource not found |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Create a repository security advisory"

#### Request example

post/repos/{owner}/{repo}/security-advisories

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/security-advisories \
  -d '{"summary":"A new important advisory","description":"A more in-depth description of what the problem is.","severity":"high","cve_id":null,"vulnerabilities":[{"package":{"name":"a-package","ecosystem":"npm"},"vulnerable_version_range":"< 1.0.0","patched_versions":"1.0.0","vulnerable_functions":["important_function"]}],"cwe_ids":["CWE-1101","CWE-20"],"credits":[{"login":"monalisa","type":"reporter"},{"login":"octocat","type":"analyst"}]}'`

Response

-
-

`Status: 201``{
"ghsa_id": "GHSA-abcd-1234-efgh",
"cve_id": "CVE-2050-00000",
"url": "https://api.github.com/repos/repo/a-package/security-advisories/GHSA-abcd-1234-efgh",
"html_url": "https://github.com/repo/a-package/security/advisories/GHSA-abcd-1234-efgh",
"summary": "A short summary of the advisory.",
"description": "A detailed description of what the advisory entails.",
"severity": "critical",
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
"publisher": {
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
"identifiers": [
{
"type": "GHSA",
"value": "GHSA-abcd-1234-efgh"
},
{
"type": "CVE",
"value": "CVE-2050-00000"
}
],
"state": "published",
"created_at": "2020-01-01T00:00:00Z",
"updated_at": "2020-01-02T00:00:00Z",
"published_at": "2020-01-03T00:00:00Z",
"closed_at": null,
"withdrawn_at": null,
"submission": null,
"vulnerabilities": [
{
"package": {
"ecosystem": "pip",
"name": "a-package"
},
"vulnerable_version_range": ">= 1.0.0, < 1.0.1",
"patched_versions": "1.0.1",
"vulnerable_functions": [
"function1"
]
},
{
"package": {
"ecosystem": "pip",
"name": "another-package"
},
"vulnerable_version_range": ">= 1.0.0, < 1.0.2",
"patched_versions": "1.0.2",
"vulnerable_functions": [
"function2"
]
}
],
"cvss": {
"vector_string": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
"score": 9.8
},
"cvss_severities": {
"cvss_v3": {
"vector_string": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
"score": 9.8
},
"cvss_v4": {
"vector_string": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N",
"score": 9.3
}
},
"cwes": [
{
"cwe_id": "CWE-123",
"name": "A CWE"
}
],
"cwe_ids": [
"CWE-123"
],
"credits": [
{
"login": "octocat",
"type": "analyst"
}
],
"credits_detailed": [
{
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
"type": "analyst",
"state": "accepted"
}
],
"collaborating_users": [
{
"login": "octokitten",
"id": 1,
"node_id": "MDQ6VXNlcjE=",
"avatar_url": "https://github.com/images/error/octokitten_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/octokitten",
"html_url": "https://github.com/octokitten",
"followers_url": "https://api.github.com/users/octokitten/followers",
"following_url": "https://api.github.com/users/octokitten/following{/other_user}",
"gists_url": "https://api.github.com/users/octokitten/gists{/gist_id}",
"starred_url": "https://api.github.com/users/octokitten/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/octokitten/subscriptions",
"organizations_url": "https://api.github.com/users/octokitten/orgs",
"repos_url": "https://api.github.com/users/octokitten/repos",
"events_url": "https://api.github.com/users/octokitten/events{/privacy}",
"received_events_url": "https://api.github.com/users/octokitten/received_events",
"type": "User",
"site_admin": false
}
],
"collaborating_teams": [
{
"name": "Justice League",
"id": 1,
"node_id": "MDQ6VGVhbTE=",
"slug": "justice-league",
"description": "A great team.",
"privacy": "closed",
"notification_setting": "notifications_enabled",
"url": "https://api.github.com/teams/1",
"html_url": "https://github.com/orgs/github/teams/justice-league",
"members_url": "https://api.github.com/teams/1/members{/member}",
"repositories_url": "https://api.github.com/teams/1/repos",
"permission": "admin",
"parent": null
}
],
"private_fork": {
"id": 217723378,
"node_id": "MDEwOlJlcG9zaXRvcnkyMTc3MjMzNzg=",
"name": "octo-repo-ghsa-abcd-1234-efgh",
"full_name": "octo-org/octo-repo-ghsa-abcd-1234-efgh",
"owner": {
"login": "octo-org",
"id": 6811672,
"node_id": "MDEyOk9yZ2FuaXphdGlvbjY4MTE2NzI=",
"avatar_url": "https://avatars3.githubusercontent.com/u/6811672?v=4",
"gravatar_id": "",
"url": "https://api.github.com/users/octo-org",
"html_url": "https://github.com/octo-org",
"followers_url": "https://api.github.com/users/octo-org/followers",
"following_url": "https://api.github.com/users/octo-org/following{/other_user}",
"gists_url": "https://api.github.com/users/octo-org/gists{/gist_id}",
"starred_url": "https://api.github.com/users/octo-org/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/octo-org/subscriptions",
"organizations_url": "https://api.github.com/users/octo-org/orgs",
"repos_url": "https://api.github.com/users/octo-org/repos",
"events_url": "https://api.github.com/users/octo-org/events{/privacy}",
"received_events_url": "https://api.github.com/users/octo-org/received_events",
"type": "Organization",
"site_admin": false
},
"private": true,
"html_url": "https://github.com/octo-org/octo-repo-ghsa-abcd-1234-efgh",
"description": null,
"fork": false,
"url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh",
"archive_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/{archive_format}{/ref}",
"assignees_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/assignees{/user}",
"blobs_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/git/blobs{/sha}",
"branches_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/branches{/branch}",
"collaborators_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/collaborators{/collaborator}",
"comments_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/comments{/number}",
"commits_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/commits{/sha}",
"compare_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/compare/{base}...{head}",
"contents_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/contents/{+path}",
"contributors_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/contributors",
"deployments_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/deployments",
"downloads_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/downloads",
"events_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/events",
"forks_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/forks",
"git_commits_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/git/commits{/sha}",
"git_refs_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/git/refs{/sha}",
"git_tags_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/git/tags{/sha}",
"hooks_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/hooks",
"issue_comment_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/issues/comments{/number}",
"issue_events_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/issues/events{/number}",
"issues_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/issues{/number}",
"keys_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/keys{/key_id}",
"labels_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/labels{/name}",
"languages_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/languages",
"merges_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/merges",
"milestones_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/milestones{/number}",
"notifications_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/notifications{?since,all,participating}",
"pulls_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/pulls{/number}",
"releases_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/releases{/id}",
"stargazers_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/stargazers",
"statuses_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/statuses/{sha}",
"subscribers_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/subscribers",
"subscription_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/subscription",
"tags_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/tags",
"teams_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/teams",
"trees_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/git/trees{/sha}"
}
}`

## Privately report a security vulnerability

Report a security vulnerability to the maintainers of the repository.
See "[Privately reporting a security vulnerability](https://docs.github.com/code-security/security-advisories/guidance-on-reporting-and-writing/privately-reporting-a-security-vulnerability)" for more information about private vulnerability reporting.

### Fine-grained access tokens for "Privately report a security vulnerability"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Repository security advisories" repository permissions (write)

### Parameters for "Privately report a security vulnerability"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| summarystringRequiredA short summary of the advisory. |
| descriptionstringRequiredA detailed description of what the advisory impacts. |
| vulnerabilitiesarray of objects or nullAn array of products affected by the vulnerability detailed in a repository security advisory. |
| Name, Type, DescriptionpackageobjectRequiredThe name of the package affected by the vulnerability.Name, Type, DescriptionecosystemstringRequiredThe package's language or package management ecosystem.Can be one of:rubygems,npm,pip,maven,nuget,composer,go,rust,erlang,actions,pub,other,swiftnamestring or nullThe unique package name within its ecosystem.vulnerable_version_rangestring or nullThe range of the package versions affected by the vulnerability.patched_versionsstring or nullThe package version(s) that resolve the vulnerability.vulnerable_functionsarray of strings or nullThe functions in the package that are affected. |
| Name, Type, Description |
| packageobjectRequiredThe name of the package affected by the vulnerability. |
| Name, Type, DescriptionecosystemstringRequiredThe package's language or package management ecosystem.Can be one of:rubygems,npm,pip,maven,nuget,composer,go,rust,erlang,actions,pub,other,swiftnamestring or nullThe unique package name within its ecosystem. |
| Name, Type, Description |
| ecosystemstringRequiredThe package's language or package management ecosystem.Can be one of:rubygems,npm,pip,maven,nuget,composer,go,rust,erlang,actions,pub,other,swift |
| namestring or nullThe unique package name within its ecosystem. |
| vulnerable_version_rangestring or nullThe range of the package versions affected by the vulnerability. |
| patched_versionsstring or nullThe package version(s) that resolve the vulnerability. |
| vulnerable_functionsarray of strings or nullThe functions in the package that are affected. |
| cwe_idsarray of strings or nullA list of Common Weakness Enumeration (CWE) IDs. |
| severitystring or nullThe severity of the advisory. You must choose between setting this field orcvss_vector_string.Can be one of:critical,high,medium,low,null |
| cvss_vector_stringstring or nullThe CVSS vector that calculates the severity of the advisory. You must choose between setting this field orseverity. |
| start_private_forkbooleanWhether to create a temporary private fork of the repository to collaborate on a fix.Default:false |

### HTTP response status codes for "Privately report a security vulnerability"

| Status code | Description |
| --- | --- |
| 201 | Created |
| 403 | Forbidden |
| 404 | Resource not found |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Privately report a security vulnerability"

#### Request example

post/repos/{owner}/{repo}/security-advisories/reports

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/security-advisories/reports \
  -d '{"summary":"A newly discovered vulnerability","description":"A more in-depth description of what the problem is.","severity":"high","vulnerabilities":[{"package":{"name":"a-package","ecosystem":"npm"},"vulnerable_version_range":"< 1.0.0","patched_versions":"1.0.0","vulnerable_functions":["important_function"]}],"cwe_ids":["CWE-123"]}'`

Response

-
-

`Status: 201``{
"ghsa_id": "GHSA-abcd-1234-efgh",
"cve_id": "CVE-2050-00000",
"url": "https://api.github.com/repos/repo/a-package/security-advisories/GHSA-abcd-1234-efgh",
"html_url": "https://github.com/repo/a-package/security/advisories/GHSA-abcd-1234-efgh",
"summary": "A newly discovered vulnerability",
"description": "A more in-depth description of what the problem is.",
"severity": "high",
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
"publisher": null,
"identifiers": [
{
"type": "GHSA",
"value": "GHSA-abcd-1234-efgh"
},
{
"type": "CVE",
"value": null
}
],
"state": "triage",
"created_at": "2020-01-01T00:00:00Z",
"updated_at": "2020-01-02T00:00:00Z",
"published_at": null,
"closed_at": null,
"withdrawn_at": null,
"submission": {
"accepted": false
},
"vulnerabilities": [
{
"package": {
"ecosystem": "npm",
"name": "a-package"
},
"vulnerable_version_range": "< 1.0.0",
"patched_versions": "1.0.0",
"vulnerable_functions": [
"important_function"
]
}
],
"cvss": null,
"cvss_severities": {
"cvss_v3": null,
"cvss_v4": null
},
"cwes": [
{
"cwe_id": "CWE-123",
"name": "A CWE"
}
],
"cwe_ids": [
"CWE-123"
],
"credits": [
{
"login": "octocat",
"type": "finder"
}
],
"credits_detailed": [
{
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
"type": "finder",
"state": "accepted"
}
],
"collaborating_users": [
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
"collaborating_teams": [
{
"name": "Justice League",
"id": 1,
"node_id": "MDQ6VGVhbTE=",
"slug": "justice-league",
"description": "A great team.",
"privacy": "closed",
"notification_setting": "notifications_enabled",
"url": "https://api.github.com/teams/1",
"html_url": "https://github.com/orgs/github/teams/justice-league",
"members_url": "https://api.github.com/teams/1/members{/member}",
"repositories_url": "https://api.github.com/teams/1/repos",
"permission": "admin",
"parent": null
}
],
"private_fork": null
}`

## Get a repository security advisory

Get a repository security advisory using its GitHub Security Advisory (GHSA) identifier.

Anyone can access any published security advisory on a public repository.

The authenticated user can access an unpublished security advisory from a repository if they are a security manager or administrator of that repository, or if they are a
collaborator on the security advisory.

OAuth app tokens and personal access tokens (classic) need the `repo` or `repository_advisories:read` scope to to get a published security advisory in a private repository, or any unpublished security advisory that the authenticated user has access to.

### Fine-grained access tokens for "Get a repository security advisory"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Repository security advisories" repository permissions (read)

### Parameters for "Get a repository security advisory"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| ghsa_idstringRequiredThe GHSA (GitHub Security Advisory) identifier of the advisory. |

### HTTP response status codes for "Get a repository security advisory"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 403 | Forbidden |
| 404 | Resource not found |

### Code samples for "Get a repository security advisory"

#### Request example

get/repos/{owner}/{repo}/security-advisories/{ghsa_id}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/security-advisories/GHSA_ID`

Response

-
-

`Status: 200``{
"ghsa_id": "GHSA-abcd-1234-efgh",
"cve_id": "CVE-2050-00000",
"url": "https://api.github.com/repos/repo/a-package/security-advisories/GHSA-abcd-1234-efgh",
"html_url": "https://github.com/repo/a-package/security/advisories/GHSA-abcd-1234-efgh",
"summary": "A short summary of the advisory.",
"description": "A detailed description of what the advisory entails.",
"severity": "critical",
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
"publisher": {
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
"identifiers": [
{
"type": "GHSA",
"value": "GHSA-abcd-1234-efgh"
},
{
"type": "CVE",
"value": "CVE-2050-00000"
}
],
"state": "published",
"created_at": "2020-01-01T00:00:00Z",
"updated_at": "2020-01-02T00:00:00Z",
"published_at": "2020-01-03T00:00:00Z",
"closed_at": null,
"withdrawn_at": null,
"submission": null,
"vulnerabilities": [
{
"package": {
"ecosystem": "pip",
"name": "a-package"
},
"vulnerable_version_range": ">= 1.0.0, < 1.0.1",
"patched_versions": "1.0.1",
"vulnerable_functions": [
"function1"
]
},
{
"package": {
"ecosystem": "pip",
"name": "another-package"
},
"vulnerable_version_range": ">= 1.0.0, < 1.0.2",
"patched_versions": "1.0.2",
"vulnerable_functions": [
"function2"
]
}
],
"cvss": {
"vector_string": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
"score": 9.8
},
"cvss_severities": {
"cvss_v3": {
"vector_string": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
"score": 9.8
},
"cvss_v4": {
"vector_string": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N",
"score": 9.3
}
},
"cwes": [
{
"cwe_id": "CWE-123",
"name": "A CWE"
}
],
"cwe_ids": [
"CWE-123"
],
"credits": [
{
"login": "octocat",
"type": "analyst"
}
],
"credits_detailed": [
{
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
"type": "analyst",
"state": "accepted"
}
],
"collaborating_users": [
{
"login": "octokitten",
"id": 1,
"node_id": "MDQ6VXNlcjE=",
"avatar_url": "https://github.com/images/error/octokitten_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/octokitten",
"html_url": "https://github.com/octokitten",
"followers_url": "https://api.github.com/users/octokitten/followers",
"following_url": "https://api.github.com/users/octokitten/following{/other_user}",
"gists_url": "https://api.github.com/users/octokitten/gists{/gist_id}",
"starred_url": "https://api.github.com/users/octokitten/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/octokitten/subscriptions",
"organizations_url": "https://api.github.com/users/octokitten/orgs",
"repos_url": "https://api.github.com/users/octokitten/repos",
"events_url": "https://api.github.com/users/octokitten/events{/privacy}",
"received_events_url": "https://api.github.com/users/octokitten/received_events",
"type": "User",
"site_admin": false
}
],
"collaborating_teams": [
{
"name": "Justice League",
"id": 1,
"node_id": "MDQ6VGVhbTE=",
"slug": "justice-league",
"description": "A great team.",
"privacy": "closed",
"notification_setting": "notifications_enabled",
"url": "https://api.github.com/teams/1",
"html_url": "https://github.com/orgs/github/teams/justice-league",
"members_url": "https://api.github.com/teams/1/members{/member}",
"repositories_url": "https://api.github.com/teams/1/repos",
"permission": "admin",
"parent": null
}
],
"private_fork": {
"id": 217723378,
"node_id": "MDEwOlJlcG9zaXRvcnkyMTc3MjMzNzg=",
"name": "octo-repo-ghsa-abcd-1234-efgh",
"full_name": "octo-org/octo-repo-ghsa-abcd-1234-efgh",
"owner": {
"login": "octo-org",
"id": 6811672,
"node_id": "MDEyOk9yZ2FuaXphdGlvbjY4MTE2NzI=",
"avatar_url": "https://avatars3.githubusercontent.com/u/6811672?v=4",
"gravatar_id": "",
"url": "https://api.github.com/users/octo-org",
"html_url": "https://github.com/octo-org",
"followers_url": "https://api.github.com/users/octo-org/followers",
"following_url": "https://api.github.com/users/octo-org/following{/other_user}",
"gists_url": "https://api.github.com/users/octo-org/gists{/gist_id}",
"starred_url": "https://api.github.com/users/octo-org/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/octo-org/subscriptions",
"organizations_url": "https://api.github.com/users/octo-org/orgs",
"repos_url": "https://api.github.com/users/octo-org/repos",
"events_url": "https://api.github.com/users/octo-org/events{/privacy}",
"received_events_url": "https://api.github.com/users/octo-org/received_events",
"type": "Organization",
"site_admin": false
},
"private": true,
"html_url": "https://github.com/octo-org/octo-repo-ghsa-abcd-1234-efgh",
"description": null,
"fork": false,
"url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh",
"archive_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/{archive_format}{/ref}",
"assignees_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/assignees{/user}",
"blobs_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/git/blobs{/sha}",
"branches_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/branches{/branch}",
"collaborators_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/collaborators{/collaborator}",
"comments_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/comments{/number}",
"commits_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/commits{/sha}",
"compare_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/compare/{base}...{head}",
"contents_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/contents/{+path}",
"contributors_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/contributors",
"deployments_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/deployments",
"downloads_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/downloads",
"events_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/events",
"forks_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/forks",
"git_commits_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/git/commits{/sha}",
"git_refs_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/git/refs{/sha}",
"git_tags_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/git/tags{/sha}",
"hooks_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/hooks",
"issue_comment_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/issues/comments{/number}",
"issue_events_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/issues/events{/number}",
"issues_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/issues{/number}",
"keys_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/keys{/key_id}",
"labels_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/labels{/name}",
"languages_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/languages",
"merges_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/merges",
"milestones_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/milestones{/number}",
"notifications_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/notifications{?since,all,participating}",
"pulls_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/pulls{/number}",
"releases_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/releases{/id}",
"stargazers_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/stargazers",
"statuses_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/statuses/{sha}",
"subscribers_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/subscribers",
"subscription_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/subscription",
"tags_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/tags",
"teams_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/teams",
"trees_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/git/trees{/sha}"
}
}`

## Update a repository security advisory

Update a repository security advisory using its GitHub Security Advisory (GHSA) identifier.

In order to update any security advisory, the authenticated user must be a security manager or administrator of that repository,
or a collaborator on the repository security advisory.

OAuth app tokens and personal access tokens (classic) need the `repo` or `repository_advisories:write` scope to use this endpoint.

### Fine-grained access tokens for "Update a repository security advisory"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Repository security advisories" repository permissions (write)

### Parameters for "Update a repository security advisory"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| ghsa_idstringRequiredThe GHSA (GitHub Security Advisory) identifier of the advisory. |

| Name, Type, Description |
| --- |
| summarystringA short summary of the advisory. |
| descriptionstringA detailed description of what the advisory impacts. |
| cve_idstring or nullThe Common Vulnerabilities and Exposures (CVE) ID. |
| vulnerabilitiesarray of objectsA product affected by the vulnerability detailed in a repository security advisory. |
| Name, Type, DescriptionpackageobjectRequiredThe name of the package affected by the vulnerability.Name, Type, DescriptionecosystemstringRequiredThe package's language or package management ecosystem.Can be one of:rubygems,npm,pip,maven,nuget,composer,go,rust,erlang,actions,pub,other,swiftnamestring or nullThe unique package name within its ecosystem.vulnerable_version_rangestring or nullThe range of the package versions affected by the vulnerability.patched_versionsstring or nullThe package version(s) that resolve the vulnerability.vulnerable_functionsarray of strings or nullThe functions in the package that are affected. |
| Name, Type, Description |
| packageobjectRequiredThe name of the package affected by the vulnerability. |
| Name, Type, DescriptionecosystemstringRequiredThe package's language or package management ecosystem.Can be one of:rubygems,npm,pip,maven,nuget,composer,go,rust,erlang,actions,pub,other,swiftnamestring or nullThe unique package name within its ecosystem. |
| Name, Type, Description |
| ecosystemstringRequiredThe package's language or package management ecosystem.Can be one of:rubygems,npm,pip,maven,nuget,composer,go,rust,erlang,actions,pub,other,swift |
| namestring or nullThe unique package name within its ecosystem. |
| vulnerable_version_rangestring or nullThe range of the package versions affected by the vulnerability. |
| patched_versionsstring or nullThe package version(s) that resolve the vulnerability. |
| vulnerable_functionsarray of strings or nullThe functions in the package that are affected. |
| cwe_idsarray of strings or nullA list of Common Weakness Enumeration (CWE) IDs. |
| creditsarray of objects or nullA list of users receiving credit for their participation in the security advisory. |
| Name, Type, DescriptionloginstringRequiredThe username of the user credited.typestringRequiredThe type of credit the user is receiving.Can be one of:analyst,finder,reporter,coordinator,remediation_developer,remediation_reviewer,remediation_verifier,tool,sponsor,other |
| Name, Type, Description |
| loginstringRequiredThe username of the user credited. |
| typestringRequiredThe type of credit the user is receiving.Can be one of:analyst,finder,reporter,coordinator,remediation_developer,remediation_reviewer,remediation_verifier,tool,sponsor,other |
| severitystring or nullThe severity of the advisory. You must choose between setting this field orcvss_vector_string.Can be one of:critical,high,medium,low,null |
| cvss_vector_stringstring or nullThe CVSS vector that calculates the severity of the advisory. You must choose between setting this field orseverity. |
| statestringThe state of the advisory.Can be one of:published,closed,draft |
| collaborating_usersarray of strings or nullA list of usernames who have been granted write access to the advisory. |
| collaborating_teamsarray of strings or nullA list of team slugs which have been granted write access to the advisory. |

### HTTP response status codes for "Update a repository security advisory"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 403 | Forbidden |
| 404 | Resource not found |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Update a repository security advisory"

#### Request examples

Select the example typeUpdating the severity and state.To add a credit to an advisory, send the whole array of values.patch/repos/{owner}/{repo}/security-advisories/{ghsa_id}

-
-
-

`curl -L \
  -X PATCH \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/security-advisories/GHSA_ID \
  -d '{"severity":"critical","state":"published"}'`

Response

-
-

`Status: 200``{
"ghsa_id": "GHSA-abcd-1234-efgh",
"cve_id": "CVE-2050-00000",
"url": "https://api.github.com/repos/repo/a-package/security-advisories/GHSA-abcd-1234-efgh",
"html_url": "https://github.com/repo/a-package/security/advisories/GHSA-abcd-1234-efgh",
"summary": "A short summary of the advisory.",
"description": "A detailed description of what the advisory entails.",
"severity": "critical",
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
"publisher": {
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
"identifiers": [
{
"type": "GHSA",
"value": "GHSA-abcd-1234-efgh"
},
{
"type": "CVE",
"value": "CVE-2050-00000"
}
],
"state": "published",
"created_at": "2020-01-01T00:00:00Z",
"updated_at": "2020-01-02T00:00:00Z",
"published_at": "2020-01-03T00:00:00Z",
"closed_at": null,
"withdrawn_at": null,
"submission": null,
"vulnerabilities": [
{
"package": {
"ecosystem": "pip",
"name": "a-package"
},
"vulnerable_version_range": ">= 1.0.0, < 1.0.1",
"patched_versions": "1.0.1",
"vulnerable_functions": [
"function1"
]
},
{
"package": {
"ecosystem": "pip",
"name": "another-package"
},
"vulnerable_version_range": ">= 1.0.0, < 1.0.2",
"patched_versions": "1.0.2",
"vulnerable_functions": [
"function2"
]
}
],
"cvss": {
"vector_string": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
"score": 9.8
},
"cvss_severities": {
"cvss_v3": {
"vector_string": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
"score": 9.8
},
"cvss_v4": {
"vector_string": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N",
"score": 9.3
}
},
"cwes": [
{
"cwe_id": "CWE-123",
"name": "A CWE"
}
],
"cwe_ids": [
"CWE-123"
],
"credits": [
{
"login": "octocat",
"type": "analyst"
}
],
"credits_detailed": [
{
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
"type": "analyst",
"state": "accepted"
}
],
"collaborating_users": [
{
"login": "octokitten",
"id": 1,
"node_id": "MDQ6VXNlcjE=",
"avatar_url": "https://github.com/images/error/octokitten_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/octokitten",
"html_url": "https://github.com/octokitten",
"followers_url": "https://api.github.com/users/octokitten/followers",
"following_url": "https://api.github.com/users/octokitten/following{/other_user}",
"gists_url": "https://api.github.com/users/octokitten/gists{/gist_id}",
"starred_url": "https://api.github.com/users/octokitten/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/octokitten/subscriptions",
"organizations_url": "https://api.github.com/users/octokitten/orgs",
"repos_url": "https://api.github.com/users/octokitten/repos",
"events_url": "https://api.github.com/users/octokitten/events{/privacy}",
"received_events_url": "https://api.github.com/users/octokitten/received_events",
"type": "User",
"site_admin": false
}
],
"collaborating_teams": [
{
"name": "Justice League",
"id": 1,
"node_id": "MDQ6VGVhbTE=",
"slug": "justice-league",
"description": "A great team.",
"privacy": "closed",
"notification_setting": "notifications_enabled",
"url": "https://api.github.com/teams/1",
"html_url": "https://github.com/orgs/github/teams/justice-league",
"members_url": "https://api.github.com/teams/1/members{/member}",
"repositories_url": "https://api.github.com/teams/1/repos",
"permission": "admin",
"parent": null
}
],
"private_fork": {
"id": 217723378,
"node_id": "MDEwOlJlcG9zaXRvcnkyMTc3MjMzNzg=",
"name": "octo-repo-ghsa-abcd-1234-efgh",
"full_name": "octo-org/octo-repo-ghsa-abcd-1234-efgh",
"owner": {
"login": "octo-org",
"id": 6811672,
"node_id": "MDEyOk9yZ2FuaXphdGlvbjY4MTE2NzI=",
"avatar_url": "https://avatars3.githubusercontent.com/u/6811672?v=4",
"gravatar_id": "",
"url": "https://api.github.com/users/octo-org",
"html_url": "https://github.com/octo-org",
"followers_url": "https://api.github.com/users/octo-org/followers",
"following_url": "https://api.github.com/users/octo-org/following{/other_user}",
"gists_url": "https://api.github.com/users/octo-org/gists{/gist_id}",
"starred_url": "https://api.github.com/users/octo-org/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/octo-org/subscriptions",
"organizations_url": "https://api.github.com/users/octo-org/orgs",
"repos_url": "https://api.github.com/users/octo-org/repos",
"events_url": "https://api.github.com/users/octo-org/events{/privacy}",
"received_events_url": "https://api.github.com/users/octo-org/received_events",
"type": "Organization",
"site_admin": false
},
"private": true,
"html_url": "https://github.com/octo-org/octo-repo-ghsa-abcd-1234-efgh",
"description": null,
"fork": false,
"url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh",
"archive_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/{archive_format}{/ref}",
"assignees_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/assignees{/user}",
"blobs_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/git/blobs{/sha}",
"branches_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/branches{/branch}",
"collaborators_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/collaborators{/collaborator}",
"comments_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/comments{/number}",
"commits_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/commits{/sha}",
"compare_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/compare/{base}...{head}",
"contents_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/contents/{+path}",
"contributors_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/contributors",
"deployments_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/deployments",
"downloads_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/downloads",
"events_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/events",
"forks_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/forks",
"git_commits_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/git/commits{/sha}",
"git_refs_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/git/refs{/sha}",
"git_tags_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/git/tags{/sha}",
"hooks_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/hooks",
"issue_comment_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/issues/comments{/number}",
"issue_events_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/issues/events{/number}",
"issues_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/issues{/number}",
"keys_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/keys{/key_id}",
"labels_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/labels{/name}",
"languages_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/languages",
"merges_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/merges",
"milestones_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/milestones{/number}",
"notifications_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/notifications{?since,all,participating}",
"pulls_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/pulls{/number}",
"releases_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/releases{/id}",
"stargazers_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/stargazers",
"statuses_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/statuses/{sha}",
"subscribers_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/subscribers",
"subscription_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/subscription",
"tags_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/tags",
"teams_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/teams",
"trees_url": "https://api.github.com/repos/octo-org/octo-repo-ghsa-abcd-1234-efgh/git/trees{/sha}"
}
}`

## Request a CVE for a repository security advisory

If you want a CVE identification number for the security vulnerability in your project, and don't already have one, you can request a CVE identification number from GitHub. For more information see "[Requesting a CVE identification number](https://docs.github.com/code-security/security-advisories/repository-security-advisories/publishing-a-repository-security-advisory#requesting-a-cve-identification-number-optional)."

You may request a CVE for public repositories, but cannot do so for private repositories.

In order to request a CVE for a repository security advisory, the authenticated user must be a security manager or administrator of that repository.

OAuth app tokens and personal access tokens (classic) need the `repo` or `repository_advisories:write` scope to use this endpoint.

### Fine-grained access tokens for "Request a CVE for a repository security advisory"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Repository security advisories" repository permissions (write)

### Parameters for "Request a CVE for a repository security advisory"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| ghsa_idstringRequiredThe GHSA (GitHub Security Advisory) identifier of the advisory. |

### HTTP response status codes for "Request a CVE for a repository security advisory"

| Status code | Description |
| --- | --- |
| 202 | Accepted |
| 400 | Bad Request |
| 403 | Forbidden |
| 404 | Resource not found |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Request a CVE for a repository security advisory"

#### Request example

post/repos/{owner}/{repo}/security-advisories/{ghsa_id}/cve

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/security-advisories/GHSA_ID/cve`

Accepted

-
-

`Status: 202`

## Create a temporary private fork

Create a temporary private fork to collaborate on fixing a security vulnerability in your repository.

Note

Forking a repository happens asynchronously. You may have to wait up to 5 minutes before you can access the fork.

### Fine-grained access tokens for "Create a temporary private fork"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Repository security advisories" repository permissions (read) and "Administration" repository permissions (write)

### Parameters for "Create a temporary private fork"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| ghsa_idstringRequiredThe GHSA (GitHub Security Advisory) identifier of the advisory. |

### HTTP response status codes for "Create a temporary private fork"

| Status code | Description |
| --- | --- |
| 202 | Accepted |
| 400 | Bad Request |
| 403 | Forbidden |
| 404 | Resource not found |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Create a temporary private fork"

#### Request example

post/repos/{owner}/{repo}/security-advisories/{ghsa_id}/forks

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/security-advisories/GHSA_ID/forks`

Response

-
-

`Status: 202``{
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
"license": {
"key": "mit",
"name": "MIT License",
"url": "https://api.github.com/licenses/mit",
"spdx_id": "MIT",
"node_id": "MDc6TGljZW5zZW1pdA==",
"html_url": "https://github.com/licenses/mit"
},
"language": null,
"forks_count": 9,
"forks": 9,
"stargazers_count": 80,
"watchers_count": 80,
"watchers": 80,
"size": 108,
"default_branch": "master",
"open_issues_count": 0,
"open_issues": 0,
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
"archived": false,
"disabled": false,
"visibility": "public",
"pushed_at": "2011-01-26T19:06:43Z",
"created_at": "2011-01-26T19:01:12Z",
"updated_at": "2011-01-26T19:14:43Z",
"permissions": {
"pull": true,
"push": false,
"admin": false
},
"allow_rebase_merge": true,
"template_repository": {
"id": 1296269,
"node_id": "MDEwOlJlcG9zaXRvcnkxMjk2MjY5",
"name": "Hello-World-Template",
"full_name": "octocat/Hello-World-Template",
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
"html_url": "https://github.com/octocat/Hello-World-Template",
"description": "This your first repo!",
"fork": false,
"url": "https://api.github.com/repos/octocat/Hello-World-Template",
"archive_url": "https://api.github.com/repos/octocat/Hello-World-Template/{archive_format}{/ref}",
"assignees_url": "https://api.github.com/repos/octocat/Hello-World-Template/assignees{/user}",
"blobs_url": "https://api.github.com/repos/octocat/Hello-World-Template/git/blobs{/sha}",
"branches_url": "https://api.github.com/repos/octocat/Hello-World-Template/branches{/branch}",
"collaborators_url": "https://api.github.com/repos/octocat/Hello-World-Template/collaborators{/collaborator}",
"comments_url": "https://api.github.com/repos/octocat/Hello-World-Template/comments{/number}",
"commits_url": "https://api.github.com/repos/octocat/Hello-World-Template/commits{/sha}",
"compare_url": "https://api.github.com/repos/octocat/Hello-World-Template/compare/{base}...{head}",
"contents_url": "https://api.github.com/repos/octocat/Hello-World-Template/contents/{+path}",
"contributors_url": "https://api.github.com/repos/octocat/Hello-World-Template/contributors",
"deployments_url": "https://api.github.com/repos/octocat/Hello-World-Template/deployments",
"downloads_url": "https://api.github.com/repos/octocat/Hello-World-Template/downloads",
"events_url": "https://api.github.com/repos/octocat/Hello-World-Template/events",
"forks_url": "https://api.github.com/repos/octocat/Hello-World-Template/forks",
"git_commits_url": "https://api.github.com/repos/octocat/Hello-World-Template/git/commits{/sha}",
"git_refs_url": "https://api.github.com/repos/octocat/Hello-World-Template/git/refs{/sha}",
"git_tags_url": "https://api.github.com/repos/octocat/Hello-World-Template/git/tags{/sha}",
"git_url": "git:github.com/octocat/Hello-World-Template.git",
"issue_comment_url": "https://api.github.com/repos/octocat/Hello-World-Template/issues/comments{/number}",
"issue_events_url": "https://api.github.com/repos/octocat/Hello-World-Template/issues/events{/number}",
"issues_url": "https://api.github.com/repos/octocat/Hello-World-Template/issues{/number}",
"keys_url": "https://api.github.com/repos/octocat/Hello-World-Template/keys{/key_id}",
"labels_url": "https://api.github.com/repos/octocat/Hello-World-Template/labels{/name}",
"languages_url": "https://api.github.com/repos/octocat/Hello-World-Template/languages",
"merges_url": "https://api.github.com/repos/octocat/Hello-World-Template/merges",
"milestones_url": "https://api.github.com/repos/octocat/Hello-World-Template/milestones{/number}",
"notifications_url": "https://api.github.com/repos/octocat/Hello-World-Template/notifications{?since,all,participating}",
"pulls_url": "https://api.github.com/repos/octocat/Hello-World-Template/pulls{/number}",
"releases_url": "https://api.github.com/repos/octocat/Hello-World-Template/releases{/id}",
"ssh_url": "git@github.com:octocat/Hello-World-Template.git",
"stargazers_url": "https://api.github.com/repos/octocat/Hello-World-Template/stargazers",
"statuses_url": "https://api.github.com/repos/octocat/Hello-World-Template/statuses/{sha}",
"subscribers_url": "https://api.github.com/repos/octocat/Hello-World-Template/subscribers",
"subscription_url": "https://api.github.com/repos/octocat/Hello-World-Template/subscription",
"tags_url": "https://api.github.com/repos/octocat/Hello-World-Template/tags",
"teams_url": "https://api.github.com/repos/octocat/Hello-World-Template/teams",
"trees_url": "https://api.github.com/repos/octocat/Hello-World-Template/git/trees{/sha}",
"clone_url": "https://github.com/octocat/Hello-World-Template.git",
"mirror_url": "git:git.example.com/octocat/Hello-World-Template",
"hooks_url": "https://api.github.com/repos/octocat/Hello-World-Template/hooks",
"svn_url": "https://svn.github.com/octocat/Hello-World-Template",
"homepage": "https://github.com",
"language": null,
"forks": 9,
"forks_count": 9,
"stargazers_count": 80,
"watchers_count": 80,
"watchers": 80,
"size": 108,
"default_branch": "master",
"open_issues": 0,
"open_issues_count": 0,
"is_template": true,
"license": {
"key": "mit",
"name": "MIT License",
"url": "https://api.github.com/licenses/mit",
"spdx_id": "MIT",
"node_id": "MDc6TGljZW5zZW1pdA==",
"html_url": "https://api.github.com/licenses/mit"
},
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
"network_count": 0
},
"temp_clone_token": "ABTLWHOULUVAXGTRYU7OC2876QJ2O",
"allow_squash_merge": true,
"allow_auto_merge": false,
"delete_branch_on_merge": true,
"allow_merge_commit": true,
"allow_forking": true,
"web_commit_signoff_required": false,
"subscribers_count": 42,
"network_count": 0,
"organization": {
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
"type": "Organization",
"site_admin": false
},
"parent": {
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
"html_url": "https://api.github.com/licenses/mit"
},
"forks": 1,
"open_issues": 1,
"watchers": 1
},
"source": {
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
"html_url": "https://api.github.com/licenses/mit"
},
"forks": 1,
"open_issues": 1,
"watchers": 1
}
}`
