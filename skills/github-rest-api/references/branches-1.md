# REST API endpoints for protected branches

# REST API endpoints for protected branches

> Use the REST API to manage protected branches.

## Get branch protection

Protected branches are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, GitHub Enterprise Cloud, and GitHub Enterprise Server. For more information, see [GitHub's products](https://docs.github.com/github/getting-started-with-github/githubs-products) in the GitHub Help documentation.

### Fine-grained access tokens for "Get branch protection"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (read)

### Parameters for "Get branch protection"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| branchstringRequiredThe name of the branch. Cannot contain wildcard characters. To use wildcard characters in branch names, usethe GraphQL API. |

### HTTP response status codes for "Get branch protection"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |

### Code samples for "Get branch protection"

#### Request example

get/repos/{owner}/{repo}/branches/{branch}/protection

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/branches/BRANCH/protection`

Response

-
-

`Status: 200``{
"url": "https://api.github.com/repos/octocat/Hello-World/branches/master/protection",
"required_status_checks": {
"url": "https://api.github.com/repos/octocat/Hello-World/branches/master/protection/required_status_checks",
"contexts": [
"continuous-integration/travis-ci"
],
"contexts_url": "https://api.github.com/repos/octocat/Hello-World/branches/master/protection/required_status_checks/contexts",
"enforcement_level": "non_admins"
},
"enforce_admins": {
"url": "https://api.github.com/repos/octocat/Hello-World/branches/master/protection/enforce_admins",
"enabled": true
},
"required_pull_request_reviews": {
"url": "https://api.github.com/repos/octocat/Hello-World/branches/master/protection/required_pull_request_reviews",
"dismissal_restrictions": {
"url": "https://api.github.com/repos/octocat/Hello-World/branches/master/protection/dismissal_restrictions",
"users_url": "https://api.github.com/repos/octocat/Hello-World/branches/master/protection/dismissal_restrictions/users",
"teams_url": "https://api.github.com/repos/octocat/Hello-World/branches/master/protection/dismissal_restrictions/teams",
"users": [
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
"teams": [
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
],
"apps": [
{
"id": 1,
"slug": "octoapp",
"node_id": "MDExOkludGVncmF0aW9uMQ==",
"owner": {
"login": "github",
"id": 1,
"node_id": "MDEyOk9yZ2FuaXphdGlvbjE=",
"url": "https://api.github.com/orgs/github",
"repos_url": "https://api.github.com/orgs/github/repos",
"events_url": "https://api.github.com/orgs/github/events",
"hooks_url": "https://api.github.com/orgs/github/hooks",
"issues_url": "https://api.github.com/orgs/github/issues",
"members_url": "https://api.github.com/orgs/github/members{/member}",
"public_members_url": "https://api.github.com/orgs/github/public_members{/member}",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"description": "A great organization"
},
"name": "Octocat App",
"description": "",
"external_url": "https://example.com",
"html_url": "https://github.com/apps/octoapp",
"created_at": "2017-07-08T16:18:44-04:00",
"updated_at": "2017-07-08T16:18:44-04:00",
"permissions": {
"metadata": "read",
"contents": "read",
"issues": "write",
"single_file": "write"
},
"events": [
"push",
"pull_request"
]
}
]
},
"dismiss_stale_reviews": true,
"require_code_owner_reviews": true,
"required_approving_review_count": 2,
"require_last_push_approval": true
},
"restrictions": {
"url": "https://api.github.com/repos/octocat/Hello-World/branches/master/protection/restrictions",
"users_url": "https://api.github.com/repos/octocat/Hello-World/branches/master/protection/restrictions/users",
"teams_url": "https://api.github.com/repos/octocat/Hello-World/branches/master/protection/restrictions/teams",
"apps_url": "https://api.github.com/repos/octocat/Hello-World/branches/master/protection/restrictions/apps",
"users": [
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
"teams": [
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
],
"apps": [
{
"id": 1,
"slug": "octoapp",
"node_id": "MDExOkludGVncmF0aW9uMQ==",
"owner": {
"login": "github",
"id": 1,
"node_id": "MDEyOk9yZ2FuaXphdGlvbjE=",
"url": "https://api.github.com/orgs/github",
"repos_url": "https://api.github.com/orgs/github/repos",
"events_url": "https://api.github.com/orgs/github/events",
"hooks_url": "https://api.github.com/orgs/github/hooks",
"issues_url": "https://api.github.com/orgs/github/issues",
"members_url": "https://api.github.com/orgs/github/members{/member}",
"public_members_url": "https://api.github.com/orgs/github/public_members{/member}",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"description": "A great organization"
},
"name": "Octocat App",
"description": "",
"external_url": "https://example.com",
"html_url": "https://github.com/apps/octoapp",
"created_at": "2017-07-08T16:18:44-04:00",
"updated_at": "2017-07-08T16:18:44-04:00",
"permissions": {
"metadata": "read",
"contents": "read",
"issues": "write",
"single_file": "write"
},
"events": [
"push",
"pull_request"
]
}
]
},
"required_linear_history": {
"enabled": true
},
"allow_force_pushes": {
"enabled": true
},
"allow_deletions": {
"enabled": true
},
"required_conversation_resolution": {
"enabled": true
},
"lock_branch": {
"enabled": true
},
"allow_fork_syncing": {
"enabled": true
}
}`

## Update branch protection

Protected branches are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, GitHub Enterprise Cloud, and GitHub Enterprise Server. For more information, see [GitHub's products](https://docs.github.com/github/getting-started-with-github/githubs-products) in the GitHub Help documentation.

Protecting a branch requires admin or owner permissions to the repository.

Note

Passing new arrays of `users` and `teams` replaces their previous values.

Note

The list of users, apps, and teams in total is limited to 100 items.

### Fine-grained access tokens for "Update branch protection"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Update branch protection"

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
| required_status_checksobject or nullRequiredRequire status checks to pass before merging. Set tonullto disable. |
| Name, Type, DescriptionstrictbooleanRequiredRequire branches to be up to date before merging.contextsarray of stringsRequiredClosing down notice: The list of status checks to require in order to merge into this branch. If any of these checks have recently been set by a particular GitHub App, they will be required to come from that app in future for the branch to merge. Usechecksinstead ofcontextsfor more fine-grained control.checksarray of objectsThe list of status checks to require in order to merge into this branch.Name, Type, DescriptioncontextstringRequiredThe name of the required checkapp_idintegerThe ID of the GitHub App that must provide this check. Omit this field to automatically select the GitHub App that has recently provided this check, or any app if it was not set by a GitHub App. Pass -1 to explicitly allow any app to set the status. |
| Name, Type, Description |
| strictbooleanRequiredRequire branches to be up to date before merging. |
| contextsarray of stringsRequiredClosing down notice: The list of status checks to require in order to merge into this branch. If any of these checks have recently been set by a particular GitHub App, they will be required to come from that app in future for the branch to merge. Usechecksinstead ofcontextsfor more fine-grained control. |
| checksarray of objectsThe list of status checks to require in order to merge into this branch. |
| Name, Type, DescriptioncontextstringRequiredThe name of the required checkapp_idintegerThe ID of the GitHub App that must provide this check. Omit this field to automatically select the GitHub App that has recently provided this check, or any app if it was not set by a GitHub App. Pass -1 to explicitly allow any app to set the status. |
| Name, Type, Description |
| contextstringRequiredThe name of the required check |
| app_idintegerThe ID of the GitHub App that must provide this check. Omit this field to automatically select the GitHub App that has recently provided this check, or any app if it was not set by a GitHub App. Pass -1 to explicitly allow any app to set the status. |
| enforce_adminsboolean or nullRequiredEnforce all configured restrictions for administrators. Set totrueto enforce required status checks for repository administrators. Set tonullto disable. |
| required_pull_request_reviewsobject or nullRequiredRequire at least one approving review on a pull request, before merging. Set tonullto disable. |
| Name, Type, Descriptiondismissal_restrictionsobjectSpecify which users, teams, and apps can dismiss pull request reviews. Pass an emptydismissal_restrictionsobject to disable. User and teamdismissal_restrictionsare only available for organization-owned repositories. Omit this parameter for personal repositories.Name, Type, Descriptionusersarray of stringsThe list of userlogins with dismissal accessteamsarray of stringsThe list of teamslugs with dismissal accessappsarray of stringsThe list of appslugs with dismissal accessdismiss_stale_reviewsbooleanSet totrueif you want to automatically dismiss approving reviews when someone pushes a new commit.require_code_owner_reviewsbooleanBlocks merging pull requests untilcode ownersreview them.required_approving_review_countintegerSpecify the number of reviewers required to approve pull requests. Use a number between 1 and 6 or 0 to not require reviewers.require_last_push_approvalbooleanWhether the most recent push must be approved by someone other than the person who pushed it. Default:false.Default:falsebypass_pull_request_allowancesobjectAllow specific users, teams, or apps to bypass pull request requirements.Name, Type, Descriptionusersarray of stringsThe list of userlogins allowed to bypass pull request requirements.teamsarray of stringsThe list of teamslugs allowed to bypass pull request requirements.appsarray of stringsThe list of appslugs allowed to bypass pull request requirements. |
| Name, Type, Description |
| dismissal_restrictionsobjectSpecify which users, teams, and apps can dismiss pull request reviews. Pass an emptydismissal_restrictionsobject to disable. User and teamdismissal_restrictionsare only available for organization-owned repositories. Omit this parameter for personal repositories. |
| Name, Type, Descriptionusersarray of stringsThe list of userlogins with dismissal accessteamsarray of stringsThe list of teamslugs with dismissal accessappsarray of stringsThe list of appslugs with dismissal access |
| Name, Type, Description |
| usersarray of stringsThe list of userlogins with dismissal access |
| teamsarray of stringsThe list of teamslugs with dismissal access |
| appsarray of stringsThe list of appslugs with dismissal access |
| dismiss_stale_reviewsbooleanSet totrueif you want to automatically dismiss approving reviews when someone pushes a new commit. |
| require_code_owner_reviewsbooleanBlocks merging pull requests untilcode ownersreview them. |
| required_approving_review_countintegerSpecify the number of reviewers required to approve pull requests. Use a number between 1 and 6 or 0 to not require reviewers. |
| require_last_push_approvalbooleanWhether the most recent push must be approved by someone other than the person who pushed it. Default:false.Default:false |
| bypass_pull_request_allowancesobjectAllow specific users, teams, or apps to bypass pull request requirements. |
| Name, Type, Descriptionusersarray of stringsThe list of userlogins allowed to bypass pull request requirements.teamsarray of stringsThe list of teamslugs allowed to bypass pull request requirements.appsarray of stringsThe list of appslugs allowed to bypass pull request requirements. |
| Name, Type, Description |
| usersarray of stringsThe list of userlogins allowed to bypass pull request requirements. |
| teamsarray of stringsThe list of teamslugs allowed to bypass pull request requirements. |
| appsarray of stringsThe list of appslugs allowed to bypass pull request requirements. |
| restrictionsobject or nullRequiredRestrict who can push to the protected branch. User, app, and teamrestrictionsare only available for organization-owned repositories. Set tonullto disable. |
| Name, Type, Descriptionusersarray of stringsRequiredThe list of userlogins with push accessteamsarray of stringsRequiredThe list of teamslugs with push accessappsarray of stringsThe list of appslugs with push access |
| Name, Type, Description |
| usersarray of stringsRequiredThe list of userlogins with push access |
| teamsarray of stringsRequiredThe list of teamslugs with push access |
| appsarray of stringsThe list of appslugs with push access |
| required_linear_historybooleanEnforces a linear commit Git history, which prevents anyone from pushing merge commits to a branch. Set totrueto enforce a linear commit history. Set tofalseto disable a linear commit Git history. Your repository must allow squash merging or rebase merging before you can enable a linear commit history. Default:false. For more information, see "Requiring a linear commit history" in the GitHub Help documentation. |
| allow_force_pushesboolean or nullPermits force pushes to the protected branch by anyone with write access to the repository. Set totrueto allow force pushes. Set tofalseornullto block force pushes. Default:false. For more information, see "Enabling force pushes to a protected branch" in the GitHub Help documentation." |
| allow_deletionsbooleanAllows deletion of the protected branch by anyone with write access to the repository. Set tofalseto prevent deletion of the protected branch. Default:false. For more information, see "Enabling force pushes to a protected branch" in the GitHub Help documentation. |
| block_creationsbooleanIf set totrue, therestrictionsbranch protection settings which limits who can push will also block pushes which create new branches, unless the push is initiated by a user, team, or app which has the ability to push. Set totrueto restrict new branch creation. Default:false. |
| required_conversation_resolutionbooleanRequires all conversations on code to be resolved before a pull request can be merged into a branch that matches this rule. Set tofalseto disable. Default:false. |
| lock_branchbooleanWhether to set the branch as read-only. If this is true, users will not be able to push to the branch. Default:false.Default:false |
| allow_fork_syncingbooleanWhether users can pull changes from upstream when the branch is locked. Set totrueto allow fork syncing. Set tofalseto prevent fork syncing. Default:false.Default:false |

### HTTP response status codes for "Update branch protection"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 403 | Forbidden |
| 404 | Resource not found |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Update branch protection"

#### Request example

put/repos/{owner}/{repo}/branches/{branch}/protection

-
-
-

`curl -L \
  -X PUT \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/branches/BRANCH/protection \
  -d '{"required_status_checks":{"strict":true,"contexts":["continuous-integration/travis-ci"]},"enforce_admins":true,"required_pull_request_reviews":{"dismissal_restrictions":{"users":["octocat"],"teams":["justice-league"]},"dismiss_stale_reviews":true,"require_code_owner_reviews":true,"required_approving_review_count":2,"require_last_push_approval":true,"bypass_pull_request_allowances":{"users":["octocat"],"teams":["justice-league"]}},"restrictions":{"users":["octocat"],"teams":["justice-league"],"apps":["super-ci"]},"required_linear_history":true,"allow_force_pushes":true,"allow_deletions":true,"block_creations":true,"required_conversation_resolution":true,"lock_branch":true,"allow_fork_syncing":true}'`

Response

-
-

`Status: 200``{
"url": "https://api.github.com/repos/octocat/hello-world/branches/main/protection",
"required_status_checks": {
"url": "https://api.github.com/repos/octocat/hello-world/branches/main/protection/required_status_checks",
"strict": true,
"contexts": [
"continuous-integration/travis-ci"
],
"contexts_url": "https://api.github.com/repos/octocat/hello-world/branches/main/protection/required_status_checks/contexts",
"checks": [
{
"context": "continuous-integration/travis-ci",
"app_id": null
}
]
},
"restrictions": {
"url": "https://api.github.com/repos/octocat/hello-world/branches/main/protection/restrictions",
"users_url": "https://api.github.com/repos/octocat/hello-world/branches/main/protection/restrictions/users",
"teams_url": "https://api.github.com/repos/octocat/hello-world/branches/main/protection/restrictions/teams",
"apps_url": "https://api.github.com/repos/octocat/hello-world/branches/main/protection/restrictions/apps",
"users": [],
"teams": [],
"apps": []
},
"required_pull_request_reviews": {
"url": "https://api.github.com/repos/octocat/hello-world/branches/main/protection/required_pull_request_reviews",
"dismiss_stale_reviews": true,
"require_code_owner_reviews": true,
"required_approving_review_count": 2,
"require_last_push_approval": true,
"dismissal_restrictions": {
"url": "https://api.github.com/repos/octocat/hello-world/branches/main/protection/dismissal_restrictions",
"users_url": "https://api.github.com/repos/octocat/hello-world/branches/main/protection/dismissal_restrictions/users",
"teams_url": "https://api.github.com/repos/octocat/hello-world/branches/main/protection/dismissal_restrictions/teams",
"users": [],
"teams": [],
"apps": []
}
},
"required_signatures": {
"url": "https://api.github.com/repos/octocat/hello-world/branches/main/protection/required_signatures",
"enabled": false
},
"enforce_admins": {
"url": "https://api.github.com/repos/octocat/hello-world/branches/main/protection/enforce_admins",
"enabled": true
},
"required_linear_history": {
"enabled": true
},
"allow_force_pushes": {
"enabled": true
},
"allow_deletions": {
"enabled": true
},
"block_creations": {
"enabled": true
},
"required_conversation_resolution": {
"enabled": true
},
"lock_branch": {
"enabled": true
},
"allow_fork_syncing": {
"enabled": true
}
}`

## Delete branch protection

Protected branches are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, GitHub Enterprise Cloud, and GitHub Enterprise Server. For more information, see [GitHub's products](https://docs.github.com/github/getting-started-with-github/githubs-products) in the GitHub Help documentation.

### Fine-grained access tokens for "Delete branch protection"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Delete branch protection"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| branchstringRequiredThe name of the branch. Cannot contain wildcard characters. To use wildcard characters in branch names, usethe GraphQL API. |

### HTTP response status codes for "Delete branch protection"

| Status code | Description |
| --- | --- |
| 204 | No Content |
| 403 | Forbidden |

### Code samples for "Delete branch protection"

#### Request example

delete/repos/{owner}/{repo}/branches/{branch}/protection

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/branches/BRANCH/protection`

Response

`Status: 204`

## Get admin branch protection

Protected branches are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, GitHub Enterprise Cloud, and GitHub Enterprise Server. For more information, see [GitHub's products](https://docs.github.com/github/getting-started-with-github/githubs-products) in the GitHub Help documentation.

### Fine-grained access tokens for "Get admin branch protection"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (read)

### Parameters for "Get admin branch protection"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| branchstringRequiredThe name of the branch. Cannot contain wildcard characters. To use wildcard characters in branch names, usethe GraphQL API. |

### HTTP response status codes for "Get admin branch protection"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "Get admin branch protection"

#### Request example

get/repos/{owner}/{repo}/branches/{branch}/protection/enforce_admins

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/branches/BRANCH/protection/enforce_admins`

Response

-
-

`Status: 200``{
"url": "https://api.github.com/repos/octocat/Hello-World/branches/master/protection/enforce_admins",
"enabled": true
}`

## Set admin branch protection

Protected branches are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, GitHub Enterprise Cloud, and GitHub Enterprise Server. For more information, see [GitHub's products](https://docs.github.com/github/getting-started-with-github/githubs-products) in the GitHub Help documentation.

Adding admin enforcement requires admin or owner permissions to the repository and branch protection to be enabled.

### Fine-grained access tokens for "Set admin branch protection"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Set admin branch protection"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| branchstringRequiredThe name of the branch. Cannot contain wildcard characters. To use wildcard characters in branch names, usethe GraphQL API. |

### HTTP response status codes for "Set admin branch protection"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "Set admin branch protection"

#### Request example

post/repos/{owner}/{repo}/branches/{branch}/protection/enforce_admins

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/branches/BRANCH/protection/enforce_admins`

Response

-
-

`Status: 200``{
"url": "https://api.github.com/repos/octocat/Hello-World/branches/master/protection/enforce_admins",
"enabled": true
}`

## Delete admin branch protection

Protected branches are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, GitHub Enterprise Cloud, and GitHub Enterprise Server. For more information, see [GitHub's products](https://docs.github.com/github/getting-started-with-github/githubs-products) in the GitHub Help documentation.

Removing admin enforcement requires admin or owner permissions to the repository and branch protection to be enabled.

### Fine-grained access tokens for "Delete admin branch protection"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Delete admin branch protection"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| branchstringRequiredThe name of the branch. Cannot contain wildcard characters. To use wildcard characters in branch names, usethe GraphQL API. |

### HTTP response status codes for "Delete admin branch protection"

| Status code | Description |
| --- | --- |
| 204 | No Content |
| 404 | Resource not found |

### Code samples for "Delete admin branch protection"

#### Request example

delete/repos/{owner}/{repo}/branches/{branch}/protection/enforce_admins

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/branches/BRANCH/protection/enforce_admins`

Response

`Status: 204`

## Get pull request review protection

Protected branches are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, GitHub Enterprise Cloud, and GitHub Enterprise Server. For more information, see [GitHub's products](https://docs.github.com/github/getting-started-with-github/githubs-products) in the GitHub Help documentation.

### Fine-grained access tokens for "Get pull request review protection"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (read)

### Parameters for "Get pull request review protection"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| branchstringRequiredThe name of the branch. Cannot contain wildcard characters. To use wildcard characters in branch names, usethe GraphQL API. |

### HTTP response status codes for "Get pull request review protection"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "Get pull request review protection"

#### Request example

get/repos/{owner}/{repo}/branches/{branch}/protection/required_pull_request_reviews

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/branches/BRANCH/protection/required_pull_request_reviews`

Response

-
-

`Status: 200``{
"url": "https://api.github.com/repos/octocat/Hello-World/branches/master/protection/required_pull_request_reviews",
"dismissal_restrictions": {
"url": "https://api.github.com/repos/octocat/Hello-World/branches/master/protection/dismissal_restrictions",
"users_url": "https://api.github.com/repos/octocat/Hello-World/branches/master/protection/dismissal_restrictions/users",
"teams_url": "https://api.github.com/repos/octocat/Hello-World/branches/master/protection/dismissal_restrictions/teams",
"users": [
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
"teams": [
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
],
"apps": [
{
"id": 1,
"slug": "octoapp",
"node_id": "MDExOkludGVncmF0aW9uMQ==",
"owner": {
"login": "github",
"id": 1,
"node_id": "MDEyOk9yZ2FuaXphdGlvbjE=",
"url": "https://api.github.com/orgs/github",
"repos_url": "https://api.github.com/orgs/github/repos",
"events_url": "https://api.github.com/orgs/github/events",
"hooks_url": "https://api.github.com/orgs/github/hooks",
"issues_url": "https://api.github.com/orgs/github/issues",
"members_url": "https://api.github.com/orgs/github/members{/member}",
"public_members_url": "https://api.github.com/orgs/github/public_members{/member}",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"description": "A great organization"
},
"name": "Octocat App",
"description": "",
"external_url": "https://example.com",
"html_url": "https://github.com/apps/octoapp",
"created_at": "2017-07-08T16:18:44-04:00",
"updated_at": "2017-07-08T16:18:44-04:00",
"permissions": {
"metadata": "read",
"contents": "read",
"issues": "write",
"single_file": "write"
},
"events": [
"push",
"pull_request"
]
}
]
},
"dismiss_stale_reviews": true,
"require_code_owner_reviews": true,
"required_approving_review_count": 2,
"require_last_push_approval": true
}`

## Update pull request review protection

Protected branches are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, GitHub Enterprise Cloud, and GitHub Enterprise Server. For more information, see [GitHub's products](https://docs.github.com/github/getting-started-with-github/githubs-products) in the GitHub Help documentation.

Updating pull request review enforcement requires admin or owner permissions to the repository and branch protection to be enabled.

Note

Passing new arrays of `users` and `teams` replaces their previous values.

### Fine-grained access tokens for "Update pull request review protection"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Update pull request review protection"

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
| dismissal_restrictionsobjectSpecify which users, teams, and apps can dismiss pull request reviews. Pass an emptydismissal_restrictionsobject to disable. User and teamdismissal_restrictionsare only available for organization-owned repositories. Omit this parameter for personal repositories. |
| Name, Type, Descriptionusersarray of stringsThe list of userlogins with dismissal accessteamsarray of stringsThe list of teamslugs with dismissal accessappsarray of stringsThe list of appslugs with dismissal access |
| Name, Type, Description |
| usersarray of stringsThe list of userlogins with dismissal access |
| teamsarray of stringsThe list of teamslugs with dismissal access |
| appsarray of stringsThe list of appslugs with dismissal access |
| dismiss_stale_reviewsbooleanSet totrueif you want to automatically dismiss approving reviews when someone pushes a new commit. |
| require_code_owner_reviewsbooleanBlocks merging pull requests untilcode ownershave reviewed. |
| required_approving_review_countintegerSpecifies the number of reviewers required to approve pull requests. Use a number between 1 and 6 or 0 to not require reviewers. |
| require_last_push_approvalbooleanWhether the most recent push must be approved by someone other than the person who pushed it. Default:falseDefault:false |
| bypass_pull_request_allowancesobjectAllow specific users, teams, or apps to bypass pull request requirements. |
| Name, Type, Descriptionusersarray of stringsThe list of userlogins allowed to bypass pull request requirements.teamsarray of stringsThe list of teamslugs allowed to bypass pull request requirements.appsarray of stringsThe list of appslugs allowed to bypass pull request requirements. |
| Name, Type, Description |
| usersarray of stringsThe list of userlogins allowed to bypass pull request requirements. |
| teamsarray of stringsThe list of teamslugs allowed to bypass pull request requirements. |
| appsarray of stringsThe list of appslugs allowed to bypass pull request requirements. |

### HTTP response status codes for "Update pull request review protection"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Update pull request review protection"

#### Request example

patch/repos/{owner}/{repo}/branches/{branch}/protection/required_pull_request_reviews

-
-
-

`curl -L \
  -X PATCH \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/branches/BRANCH/protection/required_pull_request_reviews \
  -d '{"dismissal_restrictions":{"users":["octocat"],"teams":["justice-league"],"apps":["octoapp"]},"bypass_pull_request_allowances":{"users":["octocat"],"teams":["justice-league"],"apps":["octoapp"]},"dismiss_stale_reviews":true,"require_code_owner_reviews":true,"required_approving_review_count":2,"require_last_push_approval":true}'`

Response

-
-

`Status: 200``{
"url": "https://api.github.com/repos/octocat/Hello-World/branches/master/protection/required_pull_request_reviews",
"dismissal_restrictions": {
"url": "https://api.github.com/repos/octocat/Hello-World/branches/master/protection/dismissal_restrictions",
"users_url": "https://api.github.com/repos/octocat/Hello-World/branches/master/protection/dismissal_restrictions/users",
"teams_url": "https://api.github.com/repos/octocat/Hello-World/branches/master/protection/dismissal_restrictions/teams",
"users": [
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
"teams": [
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
],
"apps": [
{
"id": 1,
"slug": "octoapp",
"node_id": "MDExOkludGVncmF0aW9uMQ==",
"owner": {
"login": "github",
"id": 1,
"node_id": "MDEyOk9yZ2FuaXphdGlvbjE=",
"url": "https://api.github.com/orgs/github",
"repos_url": "https://api.github.com/orgs/github/repos",
"events_url": "https://api.github.com/orgs/github/events",
"hooks_url": "https://api.github.com/orgs/github/hooks",
"issues_url": "https://api.github.com/orgs/github/issues",
"members_url": "https://api.github.com/orgs/github/members{/member}",
"public_members_url": "https://api.github.com/orgs/github/public_members{/member}",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"description": "A great organization"
},
"name": "Octocat App",
"description": "",
"external_url": "https://example.com",
"html_url": "https://github.com/apps/octoapp",
"created_at": "2017-07-08T16:18:44-04:00",
"updated_at": "2017-07-08T16:18:44-04:00",
"permissions": {
"metadata": "read",
"contents": "read",
"issues": "write",
"single_file": "write"
},
"events": [
"push",
"pull_request"
]
}
]
},
"dismiss_stale_reviews": true,
"require_code_owner_reviews": true,
"required_approving_review_count": 2,
"require_last_push_approval": true
}`

## Delete pull request review protection

Protected branches are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, GitHub Enterprise Cloud, and GitHub Enterprise Server. For more information, see [GitHub's products](https://docs.github.com/github/getting-started-with-github/githubs-products) in the GitHub Help documentation.

### Fine-grained access tokens for "Delete pull request review protection"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Delete pull request review protection"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| branchstringRequiredThe name of the branch. Cannot contain wildcard characters. To use wildcard characters in branch names, usethe GraphQL API. |

### HTTP response status codes for "Delete pull request review protection"

| Status code | Description |
| --- | --- |
| 204 | No Content |
| 404 | Resource not found |

### Code samples for "Delete pull request review protection"

#### Request example

delete/repos/{owner}/{repo}/branches/{branch}/protection/required_pull_request_reviews

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/branches/BRANCH/protection/required_pull_request_reviews`

Response

`Status: 204`

## Get commit signature protection

Protected branches are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, GitHub Enterprise Cloud, and GitHub Enterprise Server. For more information, see [GitHub's products](https://docs.github.com/github/getting-started-with-github/githubs-products) in the GitHub Help documentation.

When authenticated with admin or owner permissions to the repository, you can use this endpoint to check whether a branch requires signed commits. An enabled status of `true` indicates you must sign commits on this branch. For more information, see [Signing commits with GPG](https://docs.github.com/articles/signing-commits-with-gpg) in GitHub Help.

Note

You must enable branch protection to require signed commits.

### Fine-grained access tokens for "Get commit signature protection"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (read)

### Parameters for "Get commit signature protection"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| branchstringRequiredThe name of the branch. Cannot contain wildcard characters. To use wildcard characters in branch names, usethe GraphQL API. |

### HTTP response status codes for "Get commit signature protection"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |

### Code samples for "Get commit signature protection"

#### Request example

get/repos/{owner}/{repo}/branches/{branch}/protection/required_signatures

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/branches/BRANCH/protection/required_signatures`

Response

-
-

`Status: 200``{
"url": "https://api.github.com/repos/octocat/Hello-World/branches/master/protection/required_signatures",
"enabled": true
}`

## Create commit signature protection

Protected branches are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, GitHub Enterprise Cloud, and GitHub Enterprise Server. For more information, see [GitHub's products](https://docs.github.com/github/getting-started-with-github/githubs-products) in the GitHub Help documentation.

When authenticated with admin or owner permissions to the repository, you can use this endpoint to require signed commits on a branch. You must enable branch protection to require signed commits.

### Fine-grained access tokens for "Create commit signature protection"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Create commit signature protection"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| branchstringRequiredThe name of the branch. Cannot contain wildcard characters. To use wildcard characters in branch names, usethe GraphQL API. |

### HTTP response status codes for "Create commit signature protection"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |

### Code samples for "Create commit signature protection"

#### Request example

post/repos/{owner}/{repo}/branches/{branch}/protection/required_signatures

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/branches/BRANCH/protection/required_signatures`

Response

-
-

`Status: 200``{
"url": "https://api.github.com/repos/octocat/Hello-World/branches/master/protection/required_signatures",
"enabled": true
}`

## Delete commit signature protection

Protected branches are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, GitHub Enterprise Cloud, and GitHub Enterprise Server. For more information, see [GitHub's products](https://docs.github.com/github/getting-started-with-github/githubs-products) in the GitHub Help documentation.

When authenticated with admin or owner permissions to the repository, you can use this endpoint to disable required signed commits on a branch. You must enable branch protection to require signed commits.

### Fine-grained access tokens for "Delete commit signature protection"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Delete commit signature protection"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| branchstringRequiredThe name of the branch. Cannot contain wildcard characters. To use wildcard characters in branch names, usethe GraphQL API. |

### HTTP response status codes for "Delete commit signature protection"

| Status code | Description |
| --- | --- |
| 204 | No Content |
| 404 | Resource not found |

### Code samples for "Delete commit signature protection"

#### Request example

delete/repos/{owner}/{repo}/branches/{branch}/protection/required_signatures

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/branches/BRANCH/protection/required_signatures`

Response

`Status: 204`

## Get status checks protection

Protected branches are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, GitHub Enterprise Cloud, and GitHub Enterprise Server. For more information, see [GitHub's products](https://docs.github.com/github/getting-started-with-github/githubs-products) in the GitHub Help documentation.

### Fine-grained access tokens for "Get status checks protection"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (read)

### Parameters for "Get status checks protection"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| branchstringRequiredThe name of the branch. Cannot contain wildcard characters. To use wildcard characters in branch names, usethe GraphQL API. |

### HTTP response status codes for "Get status checks protection"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |

### Code samples for "Get status checks protection"

#### Request example

get/repos/{owner}/{repo}/branches/{branch}/protection/required_status_checks

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/branches/BRANCH/protection/required_status_checks`

Response

-
-

`Status: 200``{
"url": "https://api.github.com/repos/octocat/Hello-World/branches/master/protection/required_status_checks",
"strict": true,
"contexts": [
"continuous-integration/travis-ci"
],
"contexts_url": "https://api.github.com/repos/octocat/Hello-World/branches/master/protection/required_status_checks/contexts"
}`

## Update status check protection

Protected branches are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, GitHub Enterprise Cloud, and GitHub Enterprise Server. For more information, see [GitHub's products](https://docs.github.com/github/getting-started-with-github/githubs-products) in the GitHub Help documentation.

Updating required status checks requires admin or owner permissions to the repository and branch protection to be enabled.

### Fine-grained access tokens for "Update status check protection"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Update status check protection"

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
| strictbooleanRequire branches to be up to date before merging. |
| contextsarray of stringsClosing down notice: The list of status checks to require in order to merge into this branch. If any of these checks have recently been set by a particular GitHub App, they will be required to come from that app in future for the branch to merge. Usechecksinstead ofcontextsfor more fine-grained control. |
| checksarray of objectsThe list of status checks to require in order to merge into this branch. |
| Name, Type, DescriptioncontextstringRequiredThe name of the required checkapp_idintegerThe ID of the GitHub App that must provide this check. Omit this field to automatically select the GitHub App that has recently provided this check, or any app if it was not set by a GitHub App. Pass -1 to explicitly allow any app to set the status. |
| Name, Type, Description |
| contextstringRequiredThe name of the required check |
| app_idintegerThe ID of the GitHub App that must provide this check. Omit this field to automatically select the GitHub App that has recently provided this check, or any app if it was not set by a GitHub App. Pass -1 to explicitly allow any app to set the status. |

### HTTP response status codes for "Update status check protection"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Update status check protection"

#### Request example

patch/repos/{owner}/{repo}/branches/{branch}/protection/required_status_checks

-
-
-

`curl -L \
  -X PATCH \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/branches/BRANCH/protection/required_status_checks \
  -d '{"strict":true,"contexts":["continuous-integration/travis-ci"]}'`

Response

-
-

`Status: 200``{
"url": "https://api.github.com/repos/octocat/Hello-World/branches/master/protection/required_status_checks",
"strict": true,
"contexts": [
"continuous-integration/travis-ci"
],
"contexts_url": "https://api.github.com/repos/octocat/Hello-World/branches/master/protection/required_status_checks/contexts"
}`

## Remove status check protection

Protected branches are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, GitHub Enterprise Cloud, and GitHub Enterprise Server. For more information, see [GitHub's products](https://docs.github.com/github/getting-started-with-github/githubs-products) in the GitHub Help documentation.

### Fine-grained access tokens for "Remove status check protection"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Remove status check protection"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| branchstringRequiredThe name of the branch. Cannot contain wildcard characters. To use wildcard characters in branch names, usethe GraphQL API. |

### HTTP response status codes for "Remove status check protection"

| Status code | Description |
| --- | --- |
| 204 | No Content |

### Code samples for "Remove status check protection"

#### Request example

delete/repos/{owner}/{repo}/branches/{branch}/protection/required_status_checks

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/branches/BRANCH/protection/required_status_checks`

Response

`Status: 204`

## Get all status check contexts

Protected branches are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, GitHub Enterprise Cloud, and GitHub Enterprise Server. For more information, see [GitHub's products](https://docs.github.com/github/getting-started-with-github/githubs-products) in the GitHub Help documentation.

### Fine-grained access tokens for "Get all status check contexts"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (read)

### Parameters for "Get all status check contexts"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| branchstringRequiredThe name of the branch. Cannot contain wildcard characters. To use wildcard characters in branch names, usethe GraphQL API. |

### HTTP response status codes for "Get all status check contexts"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |

### Code samples for "Get all status check contexts"

#### Request example

get/repos/{owner}/{repo}/branches/{branch}/protection/required_status_checks/contexts

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/branches/BRANCH/protection/required_status_checks/contexts`

Response

-
-

`Status: 200``[
"continuous-integration/travis-ci"
]`

## Add status check contexts

Protected branches are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, GitHub Enterprise Cloud, and GitHub Enterprise Server. For more information, see [GitHub's products](https://docs.github.com/github/getting-started-with-github/githubs-products) in the GitHub Help documentation.

### Fine-grained access tokens for "Add status check contexts"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Add status check contexts"

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
| contextsarray of stringsRequiredThe name of the status checks |

### HTTP response status codes for "Add status check contexts"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 403 | Forbidden |
| 404 | Resource not found |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Add status check contexts"

#### Request example

post/repos/{owner}/{repo}/branches/{branch}/protection/required_status_checks/contexts

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/branches/BRANCH/protection/required_status_checks/contexts \
  -d '{"contexts":["continuous-integration/travis-ci","continuous-integration/jenkins"]}'`

Response

-
-

`Status: 200``[
"continuous-integration/travis-ci",
"continuous-integration/jenkins"
]`

## Set status check contexts

Protected branches are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, GitHub Enterprise Cloud, and GitHub Enterprise Server. For more information, see [GitHub's products](https://docs.github.com/github/getting-started-with-github/githubs-products) in the GitHub Help documentation.

### Fine-grained access tokens for "Set status check contexts"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Set status check contexts"

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
| contextsarray of stringsRequiredThe name of the status checks |

### HTTP response status codes for "Set status check contexts"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Set status check contexts"

#### Request example

put/repos/{owner}/{repo}/branches/{branch}/protection/required_status_checks/contexts

-
-
-

`curl -L \
  -X PUT \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/branches/BRANCH/protection/required_status_checks/contexts \
  -d '{"contexts":["continuous-integration/travis-ci"]}'`

Response

-
-

`Status: 200``[
"continuous-integration/travis-ci"
]`

## Remove status check contexts

Protected branches are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, GitHub Enterprise Cloud, and GitHub Enterprise Server. For more information, see [GitHub's products](https://docs.github.com/github/getting-started-with-github/githubs-products) in the GitHub Help documentation.

### Fine-grained access tokens for "Remove status check contexts"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Remove status check contexts"

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
| contextsarray of stringsRequiredThe name of the status checks |

### HTTP response status codes for "Remove status check contexts"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Remove status check contexts"

#### Request example

delete/repos/{owner}/{repo}/branches/{branch}/protection/required_status_checks/contexts

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/branches/BRANCH/protection/required_status_checks/contexts \
  -d '{"contexts":["continuous-integration/jenkins"]}'`

Response

-
-

`Status: 200``[
"continuous-integration/travis-ci"
]`

## Get access restrictions

Protected branches are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, GitHub Enterprise Cloud, and GitHub Enterprise Server. For more information, see [GitHub's products](https://docs.github.com/github/getting-started-with-github/githubs-products) in the GitHub Help documentation.

Lists who has access to this protected branch.

Note

Users, apps, and teams `restrictions` are only available for organization-owned repositories.

### Fine-grained access tokens for "Get access restrictions"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (read)

### Parameters for "Get access restrictions"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| branchstringRequiredThe name of the branch. Cannot contain wildcard characters. To use wildcard characters in branch names, usethe GraphQL API. |

### HTTP response status codes for "Get access restrictions"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |

### Code samples for "Get access restrictions"

#### Request example

get/repos/{owner}/{repo}/branches/{branch}/protection/restrictions

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/branches/BRANCH/protection/restrictions`

Response

-
-

`Status: 200``{
"url": "https://api.github.com/repos/octocat/Hello-World/branches/master/protection/restrictions",
"users_url": "https://api.github.com/repos/octocat/Hello-World/branches/master/protection/restrictions/users",
"teams_url": "https://api.github.com/repos/octocat/Hello-World/branches/master/protection/restrictions/teams",
"apps_url": "https://api.github.com/repos/octocat/Hello-World/branches/master/protection/restrictions/apps",
"users": [
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
"teams": [
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
],
"apps": [
{
"id": 1,
"slug": "octoapp",
"node_id": "MDExOkludGVncmF0aW9uMQ==",
"owner": {
"login": "github",
"id": 1,
"node_id": "MDEyOk9yZ2FuaXphdGlvbjE=",
"url": "https://api.github.com/orgs/github",
"repos_url": "https://api.github.com/orgs/github/repos",
"events_url": "https://api.github.com/orgs/github/events",
"hooks_url": "https://api.github.com/orgs/github/hooks",
"issues_url": "https://api.github.com/orgs/github/issues",
"members_url": "https://api.github.com/orgs/github/members{/member}",
"public_members_url": "https://api.github.com/orgs/github/public_members{/member}",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"description": "A great organization"
},
"name": "Octocat App",
"description": "",
"external_url": "https://example.com",
"html_url": "https://github.com/apps/octoapp",
"created_at": "2017-07-08T16:18:44-04:00",
"updated_at": "2017-07-08T16:18:44-04:00",
"permissions": {
"metadata": "read",
"contents": "read",
"issues": "write",
"single_file": "write"
},
"events": [
"push",
"pull_request"
]
}
]
}`

## Delete access restrictions

Protected branches are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, GitHub Enterprise Cloud, and GitHub Enterprise Server. For more information, see [GitHub's products](https://docs.github.com/github/getting-started-with-github/githubs-products) in the GitHub Help documentation.

Disables the ability to restrict who can push to this branch.

### Fine-grained access tokens for "Delete access restrictions"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Delete access restrictions"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| branchstringRequiredThe name of the branch. Cannot contain wildcard characters. To use wildcard characters in branch names, usethe GraphQL API. |

### HTTP response status codes for "Delete access restrictions"

| Status code | Description |
| --- | --- |
| 204 | No Content |

### Code samples for "Delete access restrictions"

#### Request example

delete/repos/{owner}/{repo}/branches/{branch}/protection/restrictions

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/branches/BRANCH/protection/restrictions`

Response

`Status: 204`

## Get apps with access to the protected branch

Protected branches are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, GitHub Enterprise Cloud, and GitHub Enterprise Server. For more information, see [GitHub's products](https://docs.github.com/github/getting-started-with-github/githubs-products) in the GitHub Help documentation.

Lists the GitHub Apps that have push access to this branch. Only GitHub Apps that are installed on the repository and that have been granted write access to the repository contents can be added as authorized actors on a protected branch.

### Fine-grained access tokens for "Get apps with access to the protected branch"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (read)

### Parameters for "Get apps with access to the protected branch"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| branchstringRequiredThe name of the branch. Cannot contain wildcard characters. To use wildcard characters in branch names, usethe GraphQL API. |

### HTTP response status codes for "Get apps with access to the protected branch"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |

### Code samples for "Get apps with access to the protected branch"

#### Request example

get/repos/{owner}/{repo}/branches/{branch}/protection/restrictions/apps

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/branches/BRANCH/protection/restrictions/apps`

Response

-
-

`Status: 200``[
{
"id": 1,
"slug": "octoapp",
"node_id": "MDExOkludGVncmF0aW9uMQ==",
"owner": {
"login": "github",
"id": 1,
"node_id": "MDEyOk9yZ2FuaXphdGlvbjE=",
"url": "https://api.github.com/orgs/github",
"repos_url": "https://api.github.com/orgs/github/repos",
"events_url": "https://api.github.com/orgs/github/events",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"html_url": "https://github.com/octocat",
"followers_url": "https://api.github.com/users/octocat/followers",
"following_url": "https://api.github.com/users/octocat/following{/other_user}",
"gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
"starred_url": "https://api.github.com/users/octocat/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/octocat/subscriptions",
"organizations_url": "https://api.github.com/users/octocat/orgs",
"received_events_url": "https://api.github.com/users/octocat/received_events",
"type": "User",
"site_admin": true
},
"name": "Octocat App",
"description": "",
"external_url": "https://example.com",
"html_url": "https://github.com/apps/octoapp",
"created_at": "2017-07-08T16:18:44-04:00",
"updated_at": "2017-07-08T16:18:44-04:00",
"permissions": {
"metadata": "read",
"contents": "read",
"issues": "write",
"single_file": "write"
},
"events": [
"push",
"pull_request"
]
}
]`

## Add app access restrictions

Protected branches are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, GitHub Enterprise Cloud, and GitHub Enterprise Server. For more information, see [GitHub's products](https://docs.github.com/github/getting-started-with-github/githubs-products) in the GitHub Help documentation.

Grants the specified apps push access for this branch. Only GitHub Apps that are installed on the repository and that have been granted write access to the repository contents can be added as authorized actors on a protected branch.

### Fine-grained access tokens for "Add app access restrictions"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Add app access restrictions"

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
| appsarray of stringsRequiredThe GitHub Apps that have push access to this branch. Use the slugified version of the app name.Note: The list of users, apps, and teams in total is limited to 100 items. |

### HTTP response status codes for "Add app access restrictions"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Add app access restrictions"

#### Request example

post/repos/{owner}/{repo}/branches/{branch}/protection/restrictions/apps

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/branches/BRANCH/protection/restrictions/apps \
  -d '{"apps":["octoapp"]}'`

Response

-
-

`Status: 200``[
{
"id": 1,
"slug": "octoapp",
"node_id": "MDExOkludGVncmF0aW9uMQ==",
"owner": {
"login": "github",
"id": 1,
"node_id": "MDEyOk9yZ2FuaXphdGlvbjE=",
"url": "https://api.github.com/orgs/github",
"repos_url": "https://api.github.com/orgs/github/repos",
"events_url": "https://api.github.com/orgs/github/events",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"html_url": "https://github.com/octocat",
"followers_url": "https://api.github.com/users/octocat/followers",
"following_url": "https://api.github.com/users/octocat/following{/other_user}",
"gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
"starred_url": "https://api.github.com/users/octocat/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/octocat/subscriptions",
"organizations_url": "https://api.github.com/users/octocat/orgs",
"received_events_url": "https://api.github.com/users/octocat/received_events",
"type": "User",
"site_admin": true
},
"name": "Octocat App",
"description": "",
"external_url": "https://example.com",
"html_url": "https://github.com/apps/octoapp",
"created_at": "2017-07-08T16:18:44-04:00",
"updated_at": "2017-07-08T16:18:44-04:00",
"permissions": {
"metadata": "read",
"contents": "read",
"issues": "write",
"single_file": "write"
},
"events": [
"push",
"pull_request"
]
}
]`

## Set app access restrictions

Protected branches are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, GitHub Enterprise Cloud, and GitHub Enterprise Server. For more information, see [GitHub's products](https://docs.github.com/github/getting-started-with-github/githubs-products) in the GitHub Help documentation.

Replaces the list of apps that have push access to this branch. This removes all apps that previously had push access and grants push access to the new list of apps. Only GitHub Apps that are installed on the repository and that have been granted write access to the repository contents can be added as authorized actors on a protected branch.

### Fine-grained access tokens for "Set app access restrictions"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Set app access restrictions"

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
| appsarray of stringsRequiredThe GitHub Apps that have push access to this branch. Use the slugified version of the app name.Note: The list of users, apps, and teams in total is limited to 100 items. |

### HTTP response status codes for "Set app access restrictions"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Set app access restrictions"

#### Request example

put/repos/{owner}/{repo}/branches/{branch}/protection/restrictions/apps

-
-
-

`curl -L \
  -X PUT \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/branches/BRANCH/protection/restrictions/apps \
  -d '{"apps":["octoapp"]}'`

Response

-
-

`Status: 200``[
{
"id": 1,
"slug": "octoapp",
"node_id": "MDExOkludGVncmF0aW9uMQ==",
"owner": {
"login": "github",
"id": 1,
"node_id": "MDEyOk9yZ2FuaXphdGlvbjE=",
"url": "https://api.github.com/orgs/github",
"repos_url": "https://api.github.com/orgs/github/repos",
"events_url": "https://api.github.com/orgs/github/events",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"html_url": "https://github.com/octocat",
"followers_url": "https://api.github.com/users/octocat/followers",
"following_url": "https://api.github.com/users/octocat/following{/other_user}",
"gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
"starred_url": "https://api.github.com/users/octocat/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/octocat/subscriptions",
"organizations_url": "https://api.github.com/users/octocat/orgs",
"received_events_url": "https://api.github.com/users/octocat/received_events",
"type": "User",
"site_admin": true
},
"name": "Octocat App",
"description": "",
"external_url": "https://example.com",
"html_url": "https://github.com/apps/octoapp",
"created_at": "2017-07-08T16:18:44-04:00",
"updated_at": "2017-07-08T16:18:44-04:00",
"permissions": {
"metadata": "read",
"contents": "read",
"issues": "write",
"single_file": "write"
},
"events": [
"push",
"pull_request"
]
}
]`

## Remove app access restrictions

Protected branches are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, GitHub Enterprise Cloud, and GitHub Enterprise Server. For more information, see [GitHub's products](https://docs.github.com/github/getting-started-with-github/githubs-products) in the GitHub Help documentation.

Removes the ability of an app to push to this branch. Only GitHub Apps that are installed on the repository and that have been granted write access to the repository contents can be added as authorized actors on a protected branch.

### Fine-grained access tokens for "Remove app access restrictions"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Remove app access restrictions"

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
| appsarray of stringsRequiredThe GitHub Apps that have push access to this branch. Use the slugified version of the app name.Note: The list of users, apps, and teams in total is limited to 100 items. |

### HTTP response status codes for "Remove app access restrictions"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Remove app access restrictions"

#### Request example

delete/repos/{owner}/{repo}/branches/{branch}/protection/restrictions/apps

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/branches/BRANCH/protection/restrictions/apps \
  -d '{"apps":["my-app"]}'`

Response

-
-

`Status: 200``[
{
"id": 1,
"slug": "octoapp",
"node_id": "MDExOkludGVncmF0aW9uMQ==",
"owner": {
"login": "github",
"id": 1,
"node_id": "MDEyOk9yZ2FuaXphdGlvbjE=",
"url": "https://api.github.com/orgs/github",
"repos_url": "https://api.github.com/orgs/github/repos",
"events_url": "https://api.github.com/orgs/github/events",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"html_url": "https://github.com/octocat",
"followers_url": "https://api.github.com/users/octocat/followers",
"following_url": "https://api.github.com/users/octocat/following{/other_user}",
"gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
"starred_url": "https://api.github.com/users/octocat/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/octocat/subscriptions",
"organizations_url": "https://api.github.com/users/octocat/orgs",
"received_events_url": "https://api.github.com/users/octocat/received_events",
"type": "User",
"site_admin": true
},
"name": "Octocat App",
"description": "",
"external_url": "https://example.com",
"html_url": "https://github.com/apps/octoapp",
"created_at": "2017-07-08T16:18:44-04:00",
"updated_at": "2017-07-08T16:18:44-04:00",
"permissions": {
"metadata": "read",
"contents": "read",
"issues": "write",
"single_file": "write"
},
"events": [
"push",
"pull_request"
]
}
]`

## Get teams with access to the protected branch

Protected branches are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, GitHub Enterprise Cloud, and GitHub Enterprise Server. For more information, see [GitHub's products](https://docs.github.com/github/getting-started-with-github/githubs-products) in the GitHub Help documentation.

Lists the teams who have push access to this branch. The list includes child teams.

### Fine-grained access tokens for "Get teams with access to the protected branch"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (read)

### Parameters for "Get teams with access to the protected branch"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| branchstringRequiredThe name of the branch. Cannot contain wildcard characters. To use wildcard characters in branch names, usethe GraphQL API. |

### HTTP response status codes for "Get teams with access to the protected branch"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |

### Code samples for "Get teams with access to the protected branch"

#### Request example

get/repos/{owner}/{repo}/branches/{branch}/protection/restrictions/teams

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/branches/BRANCH/protection/restrictions/teams`

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

## Add team access restrictions

Protected branches are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, GitHub Enterprise Cloud, and GitHub Enterprise Server. For more information, see [GitHub's products](https://docs.github.com/github/getting-started-with-github/githubs-products) in the GitHub Help documentation.

Grants the specified teams push access for this branch. You can also give push access to child teams.

### Fine-grained access tokens for "Add team access restrictions"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Add team access restrictions"

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
| teamsarray of stringsRequiredThe slug values for teams |

### HTTP response status codes for "Add team access restrictions"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Add team access restrictions"

#### Request example

post/repos/{owner}/{repo}/branches/{branch}/protection/restrictions/teams

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/branches/BRANCH/protection/restrictions/teams \
  -d '{"teams":["justice-league"]}'`

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

## Set team access restrictions

Protected branches are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, GitHub Enterprise Cloud, and GitHub Enterprise Server. For more information, see [GitHub's products](https://docs.github.com/github/getting-started-with-github/githubs-products) in the GitHub Help documentation.

Replaces the list of teams that have push access to this branch. This removes all teams that previously had push access and grants push access to the new list of teams. Team restrictions include child teams.

### Fine-grained access tokens for "Set team access restrictions"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Set team access restrictions"

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
| teamsarray of stringsRequiredThe slug values for teams |

### HTTP response status codes for "Set team access restrictions"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Set team access restrictions"

#### Request example

put/repos/{owner}/{repo}/branches/{branch}/protection/restrictions/teams

-
-
-

`curl -L \
  -X PUT \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/branches/BRANCH/protection/restrictions/teams \
  -d '{"teams":["justice-league"]}'`

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

## Remove team access restrictions

Protected branches are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, GitHub Enterprise Cloud, and GitHub Enterprise Server. For more information, see [GitHub's products](https://docs.github.com/github/getting-started-with-github/githubs-products) in the GitHub Help documentation.

Removes the ability of a team to push to this branch. You can also remove push access for child teams.

### Fine-grained access tokens for "Remove team access restrictions"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Remove team access restrictions"

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
| teamsarray of stringsRequiredThe slug values for teams |

### HTTP response status codes for "Remove team access restrictions"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Remove team access restrictions"

#### Request example

delete/repos/{owner}/{repo}/branches/{branch}/protection/restrictions/teams

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/branches/BRANCH/protection/restrictions/teams \
  -d '{"teams":["octocats"]}'`

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

## Get users with access to the protected branch

Protected branches are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, GitHub Enterprise Cloud, and GitHub Enterprise Server. For more information, see [GitHub's products](https://docs.github.com/github/getting-started-with-github/githubs-products) in the GitHub Help documentation.

Lists the people who have push access to this branch.

### Fine-grained access tokens for "Get users with access to the protected branch"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (read)

### Parameters for "Get users with access to the protected branch"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| branchstringRequiredThe name of the branch. Cannot contain wildcard characters. To use wildcard characters in branch names, usethe GraphQL API. |

### HTTP response status codes for "Get users with access to the protected branch"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |

### Code samples for "Get users with access to the protected branch"

#### Request example

get/repos/{owner}/{repo}/branches/{branch}/protection/restrictions/users

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/branches/BRANCH/protection/restrictions/users`

Response

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
"site_admin": false
}
]`

## Add user access restrictions

Protected branches are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, GitHub Enterprise Cloud, and GitHub Enterprise Server. For more information, see [GitHub's products](https://docs.github.com/github/getting-started-with-github/githubs-products) in the GitHub Help documentation.

Grants the specified people push access for this branch.

| Type | Description |
| --- | --- |
| array | Usernames for people who can have push access.Note: The list of users, apps, and teams in total is limited to 100 items. |

### Fine-grained access tokens for "Add user access restrictions"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Add user access restrictions"

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
| usersarray of stringsRequiredThe username for users |

### HTTP response status codes for "Add user access restrictions"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Add user access restrictions"

#### Request example

post/repos/{owner}/{repo}/branches/{branch}/protection/restrictions/users

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/branches/BRANCH/protection/restrictions/users \
  -d '{"users":["octocat"]}'`

Response

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
"site_admin": false
}
]`

## Set user access restrictions

Protected branches are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, GitHub Enterprise Cloud, and GitHub Enterprise Server. For more information, see [GitHub's products](https://docs.github.com/github/getting-started-with-github/githubs-products) in the GitHub Help documentation.

Replaces the list of people that have push access to this branch. This removes all people that previously had push access and grants push access to the new list of people.

| Type | Description |
| --- | --- |
| array | Usernames for people who can have push access.Note: The list of users, apps, and teams in total is limited to 100 items. |

### Fine-grained access tokens for "Set user access restrictions"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Set user access restrictions"

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
| usersarray of stringsRequiredThe username for users |

### HTTP response status codes for "Set user access restrictions"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Set user access restrictions"

#### Request example

put/repos/{owner}/{repo}/branches/{branch}/protection/restrictions/users

-
-
-

`curl -L \
  -X PUT \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/branches/BRANCH/protection/restrictions/users \
  -d '{"users":["octocat"]}'`

Response

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
"site_admin": false
}
]`

## Remove user access restrictions

Protected branches are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, GitHub Enterprise Cloud, and GitHub Enterprise Server. For more information, see [GitHub's products](https://docs.github.com/github/getting-started-with-github/githubs-products) in the GitHub Help documentation.

Removes the ability of a user to push to this branch.

| Type | Description |
| --- | --- |
| array | Usernames of the people who should no longer have push access.Note: The list of users, apps, and teams in total is limited to 100 items. |

### Fine-grained access tokens for "Remove user access restrictions"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Remove user access restrictions"

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
| usersarray of stringsRequiredThe username for users |

### HTTP response status codes for "Remove user access restrictions"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Remove user access restrictions"

#### Request example

delete/repos/{owner}/{repo}/branches/{branch}/protection/restrictions/users

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/branches/BRANCH/protection/restrictions/users \
  -d '{"users":["octocat"]}'`

Response

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
"site_admin": false
}
]`
