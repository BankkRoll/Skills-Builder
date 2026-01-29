# REST API endpoints for repositories

# REST API endpoints for repositories

> Use the REST API to manage repositories on GitHub.

## List organization repositories

Lists repositories for the specified organization.

Note

In order to see the `security_and_analysis` block for a repository you must have admin permissions for the repository or be an owner or security manager for the organization that owns the repository. For more information, see "[Managing security managers in your organization](https://docs.github.com/organizations/managing-peoples-access-to-your-organization-with-roles/managing-security-managers-in-your-organization)."

### Fine-grained access tokens for "List organization repositories"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Metadata" repository permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "List organization repositories"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| typestringSpecifies the types of repositories you want returned.Default:allCan be one of:all,public,private,forks,sources,member |
| sortstringThe property to sort the results by.Default:createdCan be one of:created,updated,pushed,full_name |
| directionstringThe order to sort by. Default:ascwhen usingfull_name, otherwisedesc.Can be one of:asc,desc |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| pageintegerThe page number of the results to fetch. For more information, see "Using pagination in the REST API."Default:1 |

### HTTP response status codes for "List organization repositories"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "List organization repositories"

#### Request example

get/orgs/{org}/repos

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/repos`

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

## Create an organization repository

Creates a new repository in the specified organization. The authenticated user must be a member of the organization.

OAuth app tokens and personal access tokens (classic) need the `public_repo` or `repo` scope to create a public repository, and `repo` scope to create a private repository.

### Fine-grained access tokens for "Create an organization repository"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Create an organization repository"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| namestringRequiredThe name of the repository. |
| descriptionstringA short description of the repository. |
| homepagestringA URL with more information about the repository. |
| privatebooleanWhether the repository is private.Default:false |
| visibilitystringThe visibility of the repository.Can be one of:public,private |
| has_issuesbooleanEithertrueto enable issues for this repository orfalseto disable them.Default:true |
| has_projectsbooleanEithertrueto enable projects for this repository orfalseto disable them.Note:If you're creating a repository in an organization that has disabled repository projects, the default isfalse, and if you passtrue, the API returns an error.Default:true |
| has_wikibooleanEithertrueto enable the wiki for this repository orfalseto disable it.Default:true |
| has_downloadsbooleanWhether downloads are enabled.Default:true |
| is_templatebooleanEithertrueto make this repo available as a template repository orfalseto prevent it.Default:false |
| team_idintegerThe id of the team that will be granted access to this repository. This is only valid when creating a repository in an organization. |
| auto_initbooleanPasstrueto create an initial commit with empty README.Default:false |
| gitignore_templatestringDesired language or platform.gitignore templateto apply. Use the name of the template without the extension. For example, "Haskell". |
| license_templatestringChoose anopen source license templatethat best suits your needs, and then use thelicense keywordas thelicense_templatestring. For example, "mit" or "mpl-2.0". |
| allow_squash_mergebooleanEithertrueto allow squash-merging pull requests, orfalseto prevent squash-merging.Default:true |
| allow_merge_commitbooleanEithertrueto allow merging pull requests with a merge commit, orfalseto prevent merging pull requests with merge commits.Default:true |
| allow_rebase_mergebooleanEithertrueto allow rebase-merging pull requests, orfalseto prevent rebase-merging.Default:true |
| allow_auto_mergebooleanEithertrueto allow auto-merge on pull requests, orfalseto disallow auto-merge.Default:false |
| delete_branch_on_mergebooleanEithertrueto allow automatically deleting head branches when pull requests are merged, orfalseto prevent automatic deletion.The authenticated user must be an organization owner to set this property totrue.Default:false |
| use_squash_pr_title_as_defaultbooleanEithertrueto allow squash-merge commits to use pull request title, orfalseto use commit message. **This property is closing down. Please usesquash_merge_commit_titleinstead.Default:false |
| squash_merge_commit_titlestringRequired when usingsquash_merge_commit_message.The default value for a squash merge commit title:PR_TITLE- default to the pull request's title.COMMIT_OR_PR_TITLE- default to the commit's title (if only one commit) or the pull request's title (when more than one commit).Can be one of:PR_TITLE,COMMIT_OR_PR_TITLE |
| squash_merge_commit_messagestringThe default value for a squash merge commit message:PR_BODY- default to the pull request's body.COMMIT_MESSAGES- default to the branch's commit messages.BLANK- default to a blank commit message.Can be one of:PR_BODY,COMMIT_MESSAGES,BLANK |
| merge_commit_titlestringRequired when usingmerge_commit_message.The default value for a merge commit title.PR_TITLE- default to the pull request's title.MERGE_MESSAGE- default to the classic title for a merge message (e.g., Merge pull request #123 from branch-name).Can be one of:PR_TITLE,MERGE_MESSAGE |
| merge_commit_messagestringThe default value for a merge commit message.PR_TITLE- default to the pull request's title.PR_BODY- default to the pull request's body.BLANK- default to a blank commit message.Can be one of:PR_BODY,PR_TITLE,BLANK |
| custom_propertiesobjectThe custom properties for the new repository. The keys are the custom property names, and the values are the corresponding custom property values. |

### HTTP response status codes for "Create an organization repository"

| Status code | Description |
| --- | --- |
| 201 | Created |
| 403 | Forbidden |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Create an organization repository"

#### Request example

post/orgs/{org}/repos

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/repos \
  -d '{"name":"Hello-World","description":"This is your first repository","homepage":"https://github.com","private":false,"has_issues":true,"has_projects":true,"has_wiki":true}'`

Response

-
-

`Status: 201``{
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

## Get a repository

The `parent` and `source` objects are present when the repository is a fork. `parent` is the repository this repository was forked from, `source` is the ultimate source for the network.

Note

- In order to see the `security_and_analysis` block for a repository you must have admin permissions for the repository or be an owner or security manager for the organization that owns the repository. For more information, see "[Managing security managers in your organization](https://docs.github.com/organizations/managing-peoples-access-to-your-organization-with-roles/managing-security-managers-in-your-organization)."
- To view merge-related settings, you must have the `contents:read` and `contents:write` permissions.

### Fine-grained access tokens for "Get a repository"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Metadata" repository permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "Get a repository"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

### HTTP response status codes for "Get a repository"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 301 | Moved permanently |
| 403 | Forbidden |
| 404 | Resource not found |

### Code samples for "Get a repository"

#### Request example

get/repos/{owner}/{repo}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO`

Default response

-
-

`Status: 200``{
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
"has_discussions": false,
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
"subscribers_count": 42,
"network_count": 0,
"license": {
"key": "mit",
"name": "MIT License",
"spdx_id": "MIT",
"url": "https://api.github.com/licenses/mit",
"node_id": "MDc6TGljZW5zZW1pdA=="
},
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
"watchers": 1,
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
}`

## Update a repository

**Note**: To edit a repository's topics, use the [Replace all repository topics](https://docs.github.com/rest/repos/repos#replace-all-repository-topics) endpoint.

### Fine-grained access tokens for "Update a repository"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Update a repository"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| namestringThe name of the repository. |
| descriptionstringA short description of the repository. |
| homepagestringA URL with more information about the repository. |
| privatebooleanEithertrueto make the repository private orfalseto make it public. Default:false.Note: You will get a422error if the organization restrictschanging repository visibilityto organization owners and a non-owner tries to change the value of private.Default:false |
| visibilitystringThe visibility of the repository.Can be one of:public,private |
| security_and_analysisobject or nullSpecify which security and analysis features to enable or disable for the repository.To use this parameter, you must have admin permissions for the repository or be an owner or security manager for the organization that owns the repository. For more information, see "Managing security managers in your organization."For example, to enable GitHub Advanced Security, use this data in the body of thePATCHrequest:{ "security_and_analysis": {"advanced_security": { "status": "enabled" } } }.You can check which security and analysis features are currently enabled by using aGET /repos/{owner}/{repo}request. |
| Name, Type, Descriptionadvanced_securityobjectUse thestatusproperty to enable or disable GitHub Advanced Security for this repository.
For more information, see "About GitHub Advanced
Security."For standalone Code Scanning or Secret Protection products, this parameter cannot be used.Name, Type, DescriptionstatusstringCan beenabledordisabled.code_securityobjectUse thestatusproperty to enable or disable GitHub Code Security for this repository.Name, Type, DescriptionstatusstringCan beenabledordisabled.secret_scanningobjectUse thestatusproperty to enable or disable secret scanning for this repository. For more information, see "About secret scanning."Name, Type, DescriptionstatusstringCan beenabledordisabled.secret_scanning_push_protectionobjectUse thestatusproperty to enable or disable secret scanning push protection for this repository. For more information, see "Protecting pushes with secret scanning."Name, Type, DescriptionstatusstringCan beenabledordisabled.secret_scanning_ai_detectionobjectUse thestatusproperty to enable or disable secret scanning AI detection for this repository. For more information, see "Responsible detection of generic secrets with AI."Name, Type, DescriptionstatusstringCan beenabledordisabled.secret_scanning_non_provider_patternsobjectUse thestatusproperty to enable or disable secret scanning non-provider patterns for this repository. For more information, see "Supported secret scanning patterns."Name, Type, DescriptionstatusstringCan beenabledordisabled. |
| Name, Type, Description |
| advanced_securityobjectUse thestatusproperty to enable or disable GitHub Advanced Security for this repository.
For more information, see "About GitHub Advanced
Security."For standalone Code Scanning or Secret Protection products, this parameter cannot be used. |
| Name, Type, DescriptionstatusstringCan beenabledordisabled. |
| Name, Type, Description |
| statusstringCan beenabledordisabled. |
| code_securityobjectUse thestatusproperty to enable or disable GitHub Code Security for this repository. |
| Name, Type, DescriptionstatusstringCan beenabledordisabled. |
| Name, Type, Description |
| statusstringCan beenabledordisabled. |
| secret_scanningobjectUse thestatusproperty to enable or disable secret scanning for this repository. For more information, see "About secret scanning." |
| Name, Type, DescriptionstatusstringCan beenabledordisabled. |
| Name, Type, Description |
| statusstringCan beenabledordisabled. |
| secret_scanning_push_protectionobjectUse thestatusproperty to enable or disable secret scanning push protection for this repository. For more information, see "Protecting pushes with secret scanning." |
| Name, Type, DescriptionstatusstringCan beenabledordisabled. |
| Name, Type, Description |
| statusstringCan beenabledordisabled. |
| secret_scanning_ai_detectionobjectUse thestatusproperty to enable or disable secret scanning AI detection for this repository. For more information, see "Responsible detection of generic secrets with AI." |
| Name, Type, DescriptionstatusstringCan beenabledordisabled. |
| Name, Type, Description |
| statusstringCan beenabledordisabled. |
| secret_scanning_non_provider_patternsobjectUse thestatusproperty to enable or disable secret scanning non-provider patterns for this repository. For more information, see "Supported secret scanning patterns." |
| Name, Type, DescriptionstatusstringCan beenabledordisabled. |
| Name, Type, Description |
| statusstringCan beenabledordisabled. |
| has_issuesbooleanEithertrueto enable issues for this repository orfalseto disable them.Default:true |
| has_projectsbooleanEithertrueto enable projects for this repository orfalseto disable them.Note:If you're creating a repository in an organization that has disabled repository projects, the default isfalse, and if you passtrue, the API returns an error.Default:true |
| has_wikibooleanEithertrueto enable the wiki for this repository orfalseto disable it.Default:true |
| is_templatebooleanEithertrueto make this repo available as a template repository orfalseto prevent it.Default:false |
| default_branchstringUpdates the default branch for this repository. |
| allow_squash_mergebooleanEithertrueto allow squash-merging pull requests, orfalseto prevent squash-merging.Default:true |
| allow_merge_commitbooleanEithertrueto allow merging pull requests with a merge commit, orfalseto prevent merging pull requests with merge commits.Default:true |
| allow_rebase_mergebooleanEithertrueto allow rebase-merging pull requests, orfalseto prevent rebase-merging.Default:true |
| allow_auto_mergebooleanEithertrueto allow auto-merge on pull requests, orfalseto disallow auto-merge.Default:false |
| delete_branch_on_mergebooleanEithertrueto allow automatically deleting head branches when pull requests are merged, orfalseto prevent automatic deletion.Default:false |
| allow_update_branchbooleanEithertrueto always allow a pull request head branch that is behind its base branch to be updated even if it is not required to be up to date before merging, or false otherwise.Default:false |
| use_squash_pr_title_as_defaultbooleanEithertrueto allow squash-merge commits to use pull request title, orfalseto use commit message. **This property is closing down. Please usesquash_merge_commit_titleinstead.Default:false |
| squash_merge_commit_titlestringRequired when usingsquash_merge_commit_message.The default value for a squash merge commit title:PR_TITLE- default to the pull request's title.COMMIT_OR_PR_TITLE- default to the commit's title (if only one commit) or the pull request's title (when more than one commit).Can be one of:PR_TITLE,COMMIT_OR_PR_TITLE |
| squash_merge_commit_messagestringThe default value for a squash merge commit message:PR_BODY- default to the pull request's body.COMMIT_MESSAGES- default to the branch's commit messages.BLANK- default to a blank commit message.Can be one of:PR_BODY,COMMIT_MESSAGES,BLANK |
| merge_commit_titlestringRequired when usingmerge_commit_message.The default value for a merge commit title.PR_TITLE- default to the pull request's title.MERGE_MESSAGE- default to the classic title for a merge message (e.g., Merge pull request #123 from branch-name).Can be one of:PR_TITLE,MERGE_MESSAGE |
| merge_commit_messagestringThe default value for a merge commit message.PR_TITLE- default to the pull request's title.PR_BODY- default to the pull request's body.BLANK- default to a blank commit message.Can be one of:PR_BODY,PR_TITLE,BLANK |
| archivedbooleanWhether to archive this repository.falsewill unarchive a previously archived repository.Default:false |
| allow_forkingbooleanEithertrueto allow private forks, orfalseto prevent private forks.Default:false |
| web_commit_signoff_requiredbooleanEithertrueto require contributors to sign off on web-based commits, orfalseto not require contributors to sign off on web-based commits.Default:false |

### HTTP response status codes for "Update a repository"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 307 | Temporary Redirect |
| 403 | Forbidden |
| 404 | Resource not found |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Update a repository"

#### Request example

patch/repos/{owner}/{repo}

-
-
-

`curl -L \
  -X PATCH \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO \
  -d '{"name":"Hello-World","description":"This is your first repository","homepage":"https://github.com","private":true,"has_issues":true,"has_projects":true,"has_wiki":true}'`

Response

-
-

`Status: 200``{
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

## Delete a repository

Deleting a repository requires admin access.

If an organization owner has configured the organization to prevent members from deleting organization-owned
repositories, you will get a `403 Forbidden` response.

OAuth app tokens and personal access tokens (classic) need the `delete_repo` scope to use this endpoint.

### Fine-grained access tokens for "Delete a repository"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Delete a repository"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

### HTTP response status codes for "Delete a repository"

| Status code | Description |
| --- | --- |
| 204 | No Content |
| 307 | Temporary Redirect |
| 403 | If an organization owner has configured the organization to prevent members from deleting organization-owned repositories, a member will get this response: |
| 404 | Resource not found |
| 409 | Conflict |

### Code samples for "Delete a repository"

#### Request example

delete/repos/{owner}/{repo}

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO`

Response

`Status: 204`

## List repository activities

Lists a detailed history of changes to a repository, such as pushes, merges, force pushes, and branch changes, and associates these changes with commits and users.

For more information about viewing repository activity,
see "[Viewing activity and data for your repository](https://docs.github.com/repositories/viewing-activity-and-data-for-your-repository)."

### Fine-grained access tokens for "List repository activities"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Contents" repository permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "List repository activities"

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
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| beforestringA cursor, as given in theLink header. If specified, the query only searches for results before this cursor. For more information, see "Using pagination in the REST API." |
| afterstringA cursor, as given in theLink header. If specified, the query only searches for results after this cursor. For more information, see "Using pagination in the REST API." |
| refstringThe Git reference for the activities you want to list.Thereffor a branch can be formatted either asrefs/heads/BRANCH_NAMEorBRANCH_NAME, whereBRANCH_NAMEis the name of your branch. |
| actorstringThe GitHub username to use to filter by the actor who performed the activity. |
| time_periodstringThe time period to filter by.For example,daywill filter for activity that occurred in the past 24 hours, andweekwill filter for activity that occurred in the past 7 days (168 hours).Can be one of:day,week,month,quarter,year |
| activity_typestringThe activity type to filter by.For example, you can choose to filter by "force_push", to see all force pushes to the repository.Can be one of:push,force_push,branch_creation,branch_deletion,pr_merge,merge_queue_merge |

### HTTP response status codes for "List repository activities"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "List repository activities"

#### Request example

get/repos/{owner}/{repo}/activity

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/activity`

Response

-
-

`Status: 200``[
{
"id": 1296269,
"node_id": "MDEwOlJlcG9zaXRvcnkxMjk2MjY5",
"before": "6dcb09b5b57875f334f61aebed695e2e4193db5e",
"after": "827efc6d56897b048c772eb4087f854f46256132",
"ref": "refs/heads/main",
"pushed_at": "2011-01-26T19:06:43Z",
"push_type": "normal",
"pusher": {
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
}
]`

## Check if Dependabot security updates are enabled for a repository

Shows whether Dependabot security updates are enabled, disabled or paused for a repository. The authenticated user must have admin read access to the repository. For more information, see "[Configuring Dependabot security updates](https://docs.github.com/articles/configuring-automated-security-fixes)".

### Fine-grained access tokens for "Check if Dependabot security updates are enabled for a repository"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (read)

### Parameters for "Check if Dependabot security updates are enabled for a repository"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

### HTTP response status codes for "Check if Dependabot security updates are enabled for a repository"

| Status code | Description |
| --- | --- |
| 200 | Response if Dependabot is enabled |
| 404 | Not Found if Dependabot is not enabled for the repository |

### Code samples for "Check if Dependabot security updates are enabled for a repository"

#### Request example

get/repos/{owner}/{repo}/automated-security-fixes

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/automated-security-fixes`

Response if Dependabot is enabled

-
-

`Status: 200``{
"enabled": true,
"paused": false
}`

## Enable Dependabot security updates

Enables Dependabot security updates for a repository. The authenticated user must have admin access to the repository. For more information, see "[Configuring Dependabot security updates](https://docs.github.com/articles/configuring-automated-security-fixes)".

### Fine-grained access tokens for "Enable Dependabot security updates"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Enable Dependabot security updates"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

### HTTP response status codes for "Enable Dependabot security updates"

| Status code | Description |
| --- | --- |
| 204 | No Content |

### Code samples for "Enable Dependabot security updates"

#### Request example

put/repos/{owner}/{repo}/automated-security-fixes

-
-
-

`curl -L \
  -X PUT \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/automated-security-fixes`

Response

`Status: 204`

## Disable Dependabot security updates

Disables Dependabot security updates for a repository. The authenticated user must have admin access to the repository. For more information, see "[Configuring Dependabot security updates](https://docs.github.com/articles/configuring-automated-security-fixes)".

### Fine-grained access tokens for "Disable Dependabot security updates"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Disable Dependabot security updates"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

### HTTP response status codes for "Disable Dependabot security updates"

| Status code | Description |
| --- | --- |
| 204 | No Content |

### Code samples for "Disable Dependabot security updates"

#### Request example

delete/repos/{owner}/{repo}/automated-security-fixes

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/automated-security-fixes`

Response

`Status: 204`

## List CODEOWNERS errors

List any syntax errors that are detected in the CODEOWNERS
file.

For more information about the correct CODEOWNERS syntax,
see "[About code owners](https://docs.github.com/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)."

### Fine-grained access tokens for "List CODEOWNERS errors"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Contents" repository permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "List CODEOWNERS errors"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| refstringA branch, tag or commit name used to determine which version of the CODEOWNERS file to use. Default: the repository's default branch (e.g.main) |

### HTTP response status codes for "List CODEOWNERS errors"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |

### Code samples for "List CODEOWNERS errors"

#### Request example

get/repos/{owner}/{repo}/codeowners/errors

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/codeowners/errors`

Response

-
-

`Status: 200``{
"errors": [
{
"line": 3,
"column": 1,
"kind": "Invalid pattern",
"source": "***/*.rb @monalisa",
"suggestion": "Did you mean `**/*.rb`?",
"message": "Invalid pattern on line 3: Did you mean `**/*.rb`?\n\n  ***/*.rb @monalisa\n  ^",
"path": ".github/CODEOWNERS"
},
{
"line": 7,
"column": 7,
"kind": "Invalid owner",
"source": "*.txt docs@",
"suggestion": null,
"message": "Invalid owner on line 7:\n\n  *.txt docs@\n        ^",
"path": ".github/CODEOWNERS"
}
]
}`

## List repository contributors

Lists contributors to the specified repository and sorts them by the number of commits per contributor in descending order. This endpoint may return information that is a few hours old because the GitHub REST API caches contributor data to improve performance.

GitHub identifies contributors by author email address. This endpoint groups contribution counts by GitHub user, which includes all associated email addresses. To improve performance, only the first 500 author email addresses in the repository link to GitHub users. The rest will appear as anonymous contributors without associated GitHub user information.

### Fine-grained access tokens for "List repository contributors"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Metadata" repository permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "List repository contributors"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| anonstringSet to1ortrueto include anonymous contributors in results. |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| pageintegerThe page number of the results to fetch. For more information, see "Using pagination in the REST API."Default:1 |

### HTTP response status codes for "List repository contributors"

| Status code | Description |
| --- | --- |
| 200 | If repository contains content |
| 204 | Response if repository is empty |
| 403 | Forbidden |
| 404 | Resource not found |

### Code samples for "List repository contributors"

#### Request example

get/repos/{owner}/{repo}/contributors

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/contributors`

If repository contains content

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
"contributions": 32
}
]`

## Create a repository dispatch event

You can use this endpoint to trigger a webhook event called `repository_dispatch` when you want activity that happens outside of GitHub to trigger a GitHub Actions workflow or GitHub App webhook. You must configure your GitHub Actions workflow or GitHub App to run when the `repository_dispatch` event occurs. For an example `repository_dispatch` webhook payload, see "[RepositoryDispatchEvent](https://docs.github.com/webhooks/event-payloads/#repository_dispatch)."

The `client_payload` parameter is available for any extra information that your workflow might need. This parameter is a JSON payload that will be passed on when the webhook event is dispatched. For example, the `client_payload` can include a message that a user would like to send using a GitHub Actions workflow. Or the `client_payload` can be used as a test to debug your workflow.

This input example shows how you can use the `client_payload` as a test to debug your workflow.

OAuth app tokens and personal access tokens (classic) need the `repo` scope to use this endpoint.

### Fine-grained access tokens for "Create a repository dispatch event"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Contents" repository permissions (write)

### Parameters for "Create a repository dispatch event"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| event_typestringRequiredA custom webhook event name. Must be 100 characters or fewer. |
| client_payloadobjectJSON payload with extra information about the webhook event that your action or workflow may use. The maximum number of top-level properties is 10. The total size of the JSON payload must be less than 64KB. |

### HTTP response status codes for "Create a repository dispatch event"

| Status code | Description |
| --- | --- |
| 204 | No Content |
| 404 | Resource not found |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Create a repository dispatch event"

#### Request example

post/repos/{owner}/{repo}/dispatches

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/dispatches \
  -d '{"event_type":"on-demand-test","client_payload":{"unit":false,"integration":true}}'`

Response

`Status: 204`

## Check if immutable releases are enabled for a repository

Shows whether immutable releases are enabled or disabled. Also identifies whether immutability is being
enforced by the repository owner.  The authenticated user must have admin read access to the repository.

### Fine-grained access tokens for "Check if immutable releases are enabled for a repository"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (read)

### Parameters for "Check if immutable releases are enabled for a repository"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

### HTTP response status codes for "Check if immutable releases are enabled for a repository"

| Status code | Description |
| --- | --- |
| 200 | Response if immutable releases are enabled |
| 404 | Not Found if immutable releases are not enabled for the repository |

### Code samples for "Check if immutable releases are enabled for a repository"

#### Request example

get/repos/{owner}/{repo}/immutable-releases

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/immutable-releases`

Response if immutable releases are enabled

-
-

`Status: 200``{
"enabled": true,
"enforced_by_owner": false
}`

## Enable immutable releases

Enables immutable releases for a repository. The authenticated user must have admin access to the repository.

### Fine-grained access tokens for "Enable immutable releases"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Enable immutable releases"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

### HTTP response status codes for "Enable immutable releases"

| Status code | Description |
| --- | --- |
| 204 | A header with no content is returned. |
| 409 | Conflict |

### Code samples for "Enable immutable releases"

#### Request example

put/repos/{owner}/{repo}/immutable-releases

-
-
-

`curl -L \
  -X PUT \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/immutable-releases`

A header with no content is returned.

`Status: 204`

## Disable immutable releases

Disables immutable releases for a repository. The authenticated user must have admin access to the repository.

### Fine-grained access tokens for "Disable immutable releases"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Disable immutable releases"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

### HTTP response status codes for "Disable immutable releases"

| Status code | Description |
| --- | --- |
| 204 | A header with no content is returned. |
| 409 | Conflict |

### Code samples for "Disable immutable releases"

#### Request example

delete/repos/{owner}/{repo}/immutable-releases

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/immutable-releases`

A header with no content is returned.

`Status: 204`

## List repository languages

Lists languages for the specified repository. The value shown for each language is the number of bytes of code written in that language.

### Fine-grained access tokens for "List repository languages"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Metadata" repository permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "List repository languages"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

### HTTP response status codes for "List repository languages"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "List repository languages"

#### Request example

get/repos/{owner}/{repo}/languages

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/languages`

Response

-
-

`Status: 200``{
"C": 78769,
"Python": 7769
}`

## Check if private vulnerability reporting is enabled for a repository

Returns a boolean indicating whether or not private vulnerability reporting is enabled for the repository. For more information, see "[Evaluating the security settings of a repository](https://docs.github.com/code-security/security-advisories/working-with-repository-security-advisories/evaluating-the-security-settings-of-a-repository)".

### Fine-grained access tokens for "Check if private vulnerability reporting is enabled for a repository"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Metadata" repository permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "Check if private vulnerability reporting is enabled for a repository"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

### HTTP response status codes for "Check if private vulnerability reporting is enabled for a repository"

| Status code | Description |
| --- | --- |
| 200 | Private vulnerability reporting status |
| 422 | Bad Request |

### Code samples for "Check if private vulnerability reporting is enabled for a repository"

#### Request example

get/repos/{owner}/{repo}/private-vulnerability-reporting

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/private-vulnerability-reporting`

Private vulnerability reporting status

-
-

`Status: 200``{
"enabled": true
}`

## Enable private vulnerability reporting for a repository

Enables private vulnerability reporting for a repository. The authenticated user must have admin access to the repository. For more information, see "[Privately reporting a security vulnerability](https://docs.github.com/code-security/security-advisories/guidance-on-reporting-and-writing/privately-reporting-a-security-vulnerability)."

### Fine-grained access tokens for "Enable private vulnerability reporting for a repository"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Enable private vulnerability reporting for a repository"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

### HTTP response status codes for "Enable private vulnerability reporting for a repository"

| Status code | Description |
| --- | --- |
| 204 | A header with no content is returned. |
| 422 | Bad Request |

### Code samples for "Enable private vulnerability reporting for a repository"

#### Request example

put/repos/{owner}/{repo}/private-vulnerability-reporting

-
-
-

`curl -L \
  -X PUT \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/private-vulnerability-reporting`

A header with no content is returned.

`Status: 204`

## Disable private vulnerability reporting for a repository

Disables private vulnerability reporting for a repository. The authenticated user must have admin access to the repository. For more information, see "[Privately reporting a security vulnerability](https://docs.github.com/code-security/security-advisories/guidance-on-reporting-and-writing/privately-reporting-a-security-vulnerability)".

### Fine-grained access tokens for "Disable private vulnerability reporting for a repository"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Disable private vulnerability reporting for a repository"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

### HTTP response status codes for "Disable private vulnerability reporting for a repository"

| Status code | Description |
| --- | --- |
| 204 | A header with no content is returned. |
| 422 | Bad Request |

### Code samples for "Disable private vulnerability reporting for a repository"

#### Request example

delete/repos/{owner}/{repo}/private-vulnerability-reporting

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/private-vulnerability-reporting`

A header with no content is returned.

`Status: 204`

## List repository tags

### Fine-grained access tokens for "List repository tags"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Metadata" repository permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "List repository tags"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| pageintegerThe page number of the results to fetch. For more information, see "Using pagination in the REST API."Default:1 |

### HTTP response status codes for "List repository tags"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "List repository tags"

#### Request example

get/repos/{owner}/{repo}/tags

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/tags`

Response

-
-

`Status: 200``[
{
"name": "v0.1",
"commit": {
"sha": "c5b97d5ae6c19d5c5df71a34c7fbeeda2479ccbc",
"url": "https://api.github.com/repos/octocat/Hello-World/commits/c5b97d5ae6c19d5c5df71a34c7fbeeda2479ccbc"
},
"zipball_url": "https://github.com/octocat/Hello-World/zipball/v0.1",
"tarball_url": "https://github.com/octocat/Hello-World/tarball/v0.1",
"node_id": "MDQ6VXNlcjE="
}
]`

## List repository teams

Lists the teams that have access to the specified repository and that are also visible to the authenticated user.

For a public repository, a team is listed only if that team added the public repository explicitly.

OAuth app tokens and personal access tokens (classic) need the `public_repo` or `repo` scope to use this endpoint with a public repository, and `repo` scope to use this endpoint with a private repository.

### Fine-grained access tokens for "List repository teams"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (read)

### Parameters for "List repository teams"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| pageintegerThe page number of the results to fetch. For more information, see "Using pagination in the REST API."Default:1 |

### HTTP response status codes for "List repository teams"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |

### Code samples for "List repository teams"

#### Request example

get/repos/{owner}/{repo}/teams

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/teams`

Response

-
-

`Status: 200``[
{
"id": 1,
"node_id": "MDQ6VGVhbTE=",
"url": "https://api.github.com/teams/1",
"html_url": "https://github.com/orgs/github/teams/justice-league",
"name": "Justice League",
"slug": "justice-league",
"description": "A great team.",
"privacy": "closed",
"notification_setting": "notifications_enabled",
"permission": "admin",
"members_url": "https://api.github.com/teams/1/members{/member}",
"repositories_url": "https://api.github.com/teams/1/repos",
"parent": null
}
]`

## Get all repository topics

### Fine-grained access tokens for "Get all repository topics"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Metadata" repository permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "Get all repository topics"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| pageintegerThe page number of the results to fetch. For more information, see "Using pagination in the REST API."Default:1 |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |

### HTTP response status codes for "Get all repository topics"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |

### Code samples for "Get all repository topics"

#### Request example

get/repos/{owner}/{repo}/topics

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/topics`

Response

-
-

`Status: 200``{
"names": [
"octocat",
"atom",
"electron",
"api"
]
}`

## Replace all repository topics

### Fine-grained access tokens for "Replace all repository topics"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Replace all repository topics"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| namesarray of stringsRequiredAn array of topics to add to the repository. Pass one or more topics toreplacethe set of existing topics. Send an empty array ([]) to clear all topics from the repository.Note:Topicnameswill be saved as lowercase. |

### HTTP response status codes for "Replace all repository topics"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Replace all repository topics"

#### Request example

put/repos/{owner}/{repo}/topics

-
-
-

`curl -L \
  -X PUT \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/topics \
  -d '{"names":["octocat","atom","electron","api"]}'`

Response

-
-

`Status: 200``{
"names": [
"octocat",
"atom",
"electron",
"api"
]
}`

## Transfer a repository

A transfer request will need to be accepted by the new owner when transferring a personal repository to another user. The response will contain the original `owner`, and the transfer will continue asynchronously. For more details on the requirements to transfer personal and organization-owned repositories, see [about repository transfers](https://docs.github.com/articles/about-repository-transfers/).

### Fine-grained access tokens for "Transfer a repository"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Transfer a repository"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| new_ownerstringRequiredThe username or organization name the repository will be transferred to. |
| new_namestringThe new name to be given to the repository. |
| team_idsarray of integersID of the team or teams to add to the repository. Teams can only be added to organization-owned repositories. |

### HTTP response status codes for "Transfer a repository"

| Status code | Description |
| --- | --- |
| 202 | Accepted |

### Code samples for "Transfer a repository"

#### Request example

post/repos/{owner}/{repo}/transfer

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/transfer \
  -d '{"new_owner":"github","team_ids":[12,345],"new_name":"octorepo"}'`

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
"allow_forking": true,
"subscribers_count": 42,
"network_count": 0
}
}`

## Check if vulnerability alerts are enabled for a repository

Shows whether dependency alerts are enabled or disabled for a repository. The authenticated user must have admin read access to the repository. For more information, see "[About security alerts for vulnerable dependencies](https://docs.github.com/articles/about-security-alerts-for-vulnerable-dependencies)".

### Fine-grained access tokens for "Check if vulnerability alerts are enabled for a repository"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (read)

### Parameters for "Check if vulnerability alerts are enabled for a repository"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

### HTTP response status codes for "Check if vulnerability alerts are enabled for a repository"

| Status code | Description |
| --- | --- |
| 204 | Response if repository is enabled with vulnerability alerts |
| 404 | Not Found if repository is not enabled with vulnerability alerts |

### Code samples for "Check if vulnerability alerts are enabled for a repository"

#### Request example

get/repos/{owner}/{repo}/vulnerability-alerts

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/vulnerability-alerts`

Response if repository is enabled with vulnerability alerts

`Status: 204`

## Enable vulnerability alerts

Enables dependency alerts and the dependency graph for a repository. The authenticated user must have admin access to the repository. For more information, see "[About security alerts for vulnerable dependencies](https://docs.github.com/articles/about-security-alerts-for-vulnerable-dependencies)".

### Fine-grained access tokens for "Enable vulnerability alerts"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Enable vulnerability alerts"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

### HTTP response status codes for "Enable vulnerability alerts"

| Status code | Description |
| --- | --- |
| 204 | No Content |

### Code samples for "Enable vulnerability alerts"

#### Request example

put/repos/{owner}/{repo}/vulnerability-alerts

-
-
-

`curl -L \
  -X PUT \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/vulnerability-alerts`

Response

`Status: 204`

## Disable vulnerability alerts

Disables dependency alerts and the dependency graph for a repository.
The authenticated user must have admin access to the repository. For more information,
see "[About security alerts for vulnerable dependencies](https://docs.github.com/articles/about-security-alerts-for-vulnerable-dependencies)".

### Fine-grained access tokens for "Disable vulnerability alerts"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Disable vulnerability alerts"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

### HTTP response status codes for "Disable vulnerability alerts"

| Status code | Description |
| --- | --- |
| 204 | No Content |

### Code samples for "Disable vulnerability alerts"

#### Request example

delete/repos/{owner}/{repo}/vulnerability-alerts

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/vulnerability-alerts`

Response

`Status: 204`

## Create a repository using a template

Creates a new repository using a repository template. Use the `template_owner` and `template_repo` route parameters to specify the repository to use as the template. If the repository is not public, the authenticated user must own or be a member of an organization that owns the repository. To check if a repository is available to use as a template, get the repository's information using the [Get a repository](https://docs.github.com/rest/repos/repos#get-a-repository) endpoint and check that the `is_template` key is `true`.

OAuth app tokens and personal access tokens (classic) need the `public_repo` or `repo` scope to create a public repository, and `repo` scope to create a private repository.

### Fine-grained access tokens for "Create a repository using a template"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write) and "Contents" repository permissions (read)

### Parameters for "Create a repository using a template"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| template_ownerstringRequiredThe account owner of the template repository. The name is not case sensitive. |
| template_repostringRequiredThe name of the template repository without the.gitextension. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| ownerstringThe organization or person who will own the new repository. To create a new repository in an organization, the authenticated user must be a member of the specified organization. |
| namestringRequiredThe name of the new repository. |
| descriptionstringA short description of the new repository. |
| include_all_branchesbooleanSet totrueto include the directory structure and files from all branches in the template repository, and not just the default branch. Default:false.Default:false |
| privatebooleanEithertrueto create a new private repository orfalseto create a new public one.Default:false |

### HTTP response status codes for "Create a repository using a template"

| Status code | Description |
| --- | --- |
| 201 | Created |

### Code samples for "Create a repository using a template"

#### Request example

post/repos/{template_owner}/{template_repo}/generate

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/TEMPLATE_OWNER/TEMPLATE_REPO/generate \
  -d '{"owner":"octocat","name":"Hello-World","description":"This is your first repository","include_all_branches":false,"private":false}'`

Response

-
-

`Status: 201``{
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

## List public repositories

Lists all public repositories in the order that they were created.

Note:

- For GitHub Enterprise Server, this endpoint will only list repositories available to all users on the enterprise.
- Pagination is powered exclusively by the `since` parameter. Use the [Link header](https://docs.github.com/rest/guides/using-pagination-in-the-rest-api#using-link-headers) to get the URL for the next page of repositories.

### Fine-grained access tokens for "List public repositories"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Metadata" repository permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "List public repositories"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| sinceintegerA repository ID. Only return repositories with an ID greater than this ID. |

### HTTP response status codes for "List public repositories"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 304 | Not modified |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "List public repositories"

#### Request example

get/repositories

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repositories`

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
"hooks_url": "http://api.github.com/repos/octocat/Hello-World/hooks"
}
]`

## List repositories for the authenticated user

Lists repositories that the authenticated user has explicit permission (`:read`, `:write`, or `:admin`) to access.

The authenticated user has explicit permission to access repositories they own, repositories where they are a collaborator, and repositories that they can access through an organization membership.

### Fine-grained access tokens for "List repositories for the authenticated user"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Metadata" repository permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "List repositories for the authenticated user"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| visibilitystringLimit results to repositories with the specified visibility.Default:allCan be one of:all,public,private |
| affiliationstringComma-separated list of values. Can include:owner: Repositories that are owned by the authenticated user.collaborator: Repositories that the user has been added to as a collaborator.organization_member: Repositories that the user has access to through being a member of an organization. This includes every repository on every team that the user is on.Default:owner,collaborator,organization_member |
| typestringLimit results to repositories of the specified type. Will cause a422error if used in the same request asvisibilityoraffiliation.Default:allCan be one of:all,owner,public,private,member |
| sortstringThe property to sort the results by.Default:full_nameCan be one of:created,updated,pushed,full_name |
| directionstringThe order to sort by. Default:ascwhen usingfull_name, otherwisedesc.Can be one of:asc,desc |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| pageintegerThe page number of the results to fetch. For more information, see "Using pagination in the REST API."Default:1 |
| sincestringOnly show repositories updated after the given time. This is a timestamp inISO 8601format:YYYY-MM-DDTHH:MM:SSZ. |
| beforestringOnly show repositories updated before the given time. This is a timestamp inISO 8601format:YYYY-MM-DDTHH:MM:SSZ. |

### HTTP response status codes for "List repositories for the authenticated user"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 304 | Not modified |
| 401 | Requires authentication |
| 403 | Forbidden |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "List repositories for the authenticated user"

#### Request example

get/user/repos

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/user/repos`

Default response

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
]`

## Create a repository for the authenticated user

Creates a new repository for the authenticated user.

OAuth app tokens and personal access tokens (classic) need the `public_repo` or `repo` scope to create a public repository, and `repo` scope to create a private repository.

### Fine-grained access tokens for "Create a repository for the authenticated user"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Create a repository for the authenticated user"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| namestringRequiredThe name of the repository. |
| descriptionstringA short description of the repository. |
| homepagestringA URL with more information about the repository. |
| privatebooleanWhether the repository is private.Default:false |
| has_issuesbooleanWhether issues are enabled.Default:true |
| has_projectsbooleanWhether projects are enabled.Default:true |
| has_wikibooleanWhether the wiki is enabled.Default:true |
| has_discussionsbooleanWhether discussions are enabled.Default:false |
| team_idintegerThe id of the team that will be granted access to this repository. This is only valid when creating a repository in an organization. |
| auto_initbooleanWhether the repository is initialized with a minimal README.Default:false |
| gitignore_templatestringThe desired language or platform to apply to the .gitignore. |
| license_templatestringThe license keyword of the open source license for this repository. |
| allow_squash_mergebooleanWhether to allow squash merges for pull requests.Default:true |
| allow_merge_commitbooleanWhether to allow merge commits for pull requests.Default:true |
| allow_rebase_mergebooleanWhether to allow rebase merges for pull requests.Default:true |
| allow_auto_mergebooleanWhether to allow Auto-merge to be used on pull requests.Default:false |
| delete_branch_on_mergebooleanWhether to delete head branches when pull requests are mergedDefault:false |
| squash_merge_commit_titlestringRequired when usingsquash_merge_commit_message.The default value for a squash merge commit title:PR_TITLE- default to the pull request's title.COMMIT_OR_PR_TITLE- default to the commit's title (if only one commit) or the pull request's title (when more than one commit).Can be one of:PR_TITLE,COMMIT_OR_PR_TITLE |
| squash_merge_commit_messagestringThe default value for a squash merge commit message:PR_BODY- default to the pull request's body.COMMIT_MESSAGES- default to the branch's commit messages.BLANK- default to a blank commit message.Can be one of:PR_BODY,COMMIT_MESSAGES,BLANK |
| merge_commit_titlestringRequired when usingmerge_commit_message.The default value for a merge commit title.PR_TITLE- default to the pull request's title.MERGE_MESSAGE- default to the classic title for a merge message (e.g., Merge pull request #123 from branch-name).Can be one of:PR_TITLE,MERGE_MESSAGE |
| merge_commit_messagestringThe default value for a merge commit message.PR_TITLE- default to the pull request's title.PR_BODY- default to the pull request's body.BLANK- default to a blank commit message.Can be one of:PR_BODY,PR_TITLE,BLANK |
| has_downloadsbooleanWhether downloads are enabled.Default:true |
| is_templatebooleanWhether this repository acts as a template that can be used to generate new repositories.Default:false |

### HTTP response status codes for "Create a repository for the authenticated user"

| Status code | Description |
| --- | --- |
| 201 | Created |
| 304 | Not modified |
| 400 | Bad Request |
| 401 | Requires authentication |
| 403 | Forbidden |
| 404 | Resource not found |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Create a repository for the authenticated user"

#### Request example

post/user/repos

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/user/repos \
  -d '{"name":"Hello-World","description":"This is your first repo!","homepage":"https://github.com","private":false,"is_template":true}'`

Response

-
-

`Status: 201``{
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

## List repositories for a user

Lists public repositories for the specified user.

### Fine-grained access tokens for "List repositories for a user"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Metadata" repository permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "List repositories for a user"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| usernamestringRequiredThe handle for the GitHub user account. |

| Name, Type, Description |
| --- |
| typestringLimit results to repositories of the specified type.Default:ownerCan be one of:all,owner,member |
| sortstringThe property to sort the results by.Default:full_nameCan be one of:created,updated,pushed,full_name |
| directionstringThe order to sort by. Default:ascwhen usingfull_name, otherwisedesc.Can be one of:asc,desc |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| pageintegerThe page number of the results to fetch. For more information, see "Using pagination in the REST API."Default:1 |

### HTTP response status codes for "List repositories for a user"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "List repositories for a user"

#### Request example

get/users/{username}/repos

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/users/USERNAME/repos`

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
