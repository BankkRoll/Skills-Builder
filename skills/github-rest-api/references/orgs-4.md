# REST API endpoints for organizations and more

# REST API endpoints for organizations

> Use the REST API to interact with organizations.

## List organizations

Lists all organizations, in the order that they were created.

Note

Pagination is powered exclusively by the `since` parameter. Use the [Link header](https://docs.github.com/rest/guides/using-pagination-in-the-rest-api#using-link-headers) to get the URL for the next page of organizations.

### Fine-grained access tokens for "List organizations"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token does not require any permissions.

This endpoint can be used without authentication if only public resources are requested.

### Parameters for "List organizations"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| sinceintegerAn organization ID. Only return organizations with an ID greater than this ID. |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |

### HTTP response status codes for "List organizations"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 304 | Not modified |

### Code samples for "List organizations"

#### Request example

get/organizations

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/organizations`

Response

-
-

`Status: 200``[
{
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
}
]`

## Get an organization

Gets information about an organization.

When the value of `two_factor_requirement_enabled` is `true`, the organization requires all members, billing managers, outside collaborators, guest collaborators, repository collaborators, or everyone with access to any repository within the organization to enable [two-factor authentication](https://docs.github.com/articles/securing-your-account-with-two-factor-authentication-2fa/).

To see the full details about an organization, the authenticated user must be an organization owner.

OAuth app tokens and personal access tokens (classic) need the `admin:org` scope to see the full details about an organization.

To see information about an organization's GitHub plan, GitHub Apps need the `Organization plan` permission.

### Fine-grained access tokens for "Get an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token does not require any permissions.

This endpoint can be used without authentication if only public resources are requested.

### Parameters for "Get an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

### HTTP response status codes for "Get an organization"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |

### Code samples for "Get an organization"

#### Request example

get/orgs/{org}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG`

Response

-
-

`Status: 200``{
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
"description": "A great organization",
"name": "github",
"company": "GitHub",
"blog": "https://github.com/blog",
"location": "San Francisco",
"email": "octocat@github.com",
"twitter_username": "github",
"is_verified": true,
"has_organization_projects": true,
"has_repository_projects": true,
"public_repos": 2,
"public_gists": 1,
"followers": 20,
"following": 0,
"html_url": "https://github.com/octocat",
"created_at": "2008-01-14T04:33:35Z",
"type": "Organization",
"total_private_repos": 100,
"owned_private_repos": 100,
"private_gists": 81,
"disk_usage": 10000,
"collaborators": 8,
"billing_email": "mona@github.com",
"plan": {
"name": "Medium",
"space": 400,
"private_repos": 20,
"filled_seats": 4,
"seats": 5
},
"default_repository_permission": "read",
"default_repository_branch": "main",
"members_can_create_repositories": true,
"two_factor_requirement_enabled": true,
"members_allowed_repository_creation_type": "all",
"members_can_create_public_repositories": false,
"members_can_create_private_repositories": false,
"members_can_create_internal_repositories": false,
"members_can_create_pages": true,
"members_can_create_public_pages": true,
"members_can_create_private_pages": true,
"members_can_delete_repositories": true,
"members_can_change_repo_visibility": true,
"members_can_invite_outside_collaborators": true,
"members_can_delete_issues": false,
"display_commenter_full_name_setting_enabled": false,
"readers_can_create_discussions": true,
"members_can_create_teams": true,
"members_can_view_dependency_insights": true,
"members_can_fork_private_repositories": false,
"web_commit_signoff_required": false,
"updated_at": "2014-03-03T18:58:10Z",
"deploy_keys_enabled_for_repositories": false,
"dependency_graph_enabled_for_new_repositories": false,
"dependabot_alerts_enabled_for_new_repositories": false,
"dependabot_security_updates_enabled_for_new_repositories": false,
"advanced_security_enabled_for_new_repositories": false,
"secret_scanning_enabled_for_new_repositories": false,
"secret_scanning_push_protection_enabled_for_new_repositories": false,
"secret_scanning_push_protection_custom_link": "https://github.com/octo-org/octo-repo/blob/main/im-blocked.md",
"secret_scanning_push_protection_custom_link_enabled": false
}`

## Update an organization

Warning

**Closing down notice:** GitHub will replace and discontinue `members_allowed_repository_creation_type` in favor of more granular permissions. The new input parameters are `members_can_create_public_repositories`, `members_can_create_private_repositories` for all organizations and `members_can_create_internal_repositories` for organizations associated with an enterprise account using GitHub Enterprise Cloud or GitHub Enterprise Server 2.20+. For more information, see the [blog post](https://developer.github.com/changes/2019-12-03-internal-visibility-changes).

Warning

**Closing down notice:** Code security product enablement for new repositories through the organization API is closing down. Please use [code security configurations](https://docs.github.com/rest/code-security/configurations#set-a-code-security-configuration-as-a-default-for-an-organization) to set defaults instead. For more information on setting a default security configuration, see the [changelog](https://github.blog/changelog/2024-07-09-sunsetting-security-settings-defaults-parameters-in-the-organizations-rest-api/).

Updates the organization's profile and member privileges.

The authenticated user must be an organization owner to use this endpoint.

OAuth app tokens and personal access tokens (classic) need the `admin:org` or `repo` scope to use this endpoint.

### Fine-grained access tokens for "Update an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" organization permissions (write)

### Parameters for "Update an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| billing_emailstringBilling email address. This address is not publicized. |
| companystringThe company name. |
| emailstringThe publicly visible email address. |
| twitter_usernamestringThe Twitter username of the company. |
| locationstringThe location. |
| namestringThe shorthand name of the company. |
| descriptionstringThe description of the company. The maximum size is 160 characters. |
| has_organization_projectsbooleanWhether an organization can use organization projects. |
| has_repository_projectsbooleanWhether repositories that belong to the organization can use repository projects. |
| default_repository_permissionstringDefault permission level members have for organization repositories.Default:readCan be one of:read,write,admin,none |
| members_can_create_repositoriesbooleanWhether of non-admin organization members can create repositories.Note:A parameter can override this parameter. Seemembers_allowed_repository_creation_typein this table for details.Default:true |
| members_can_create_internal_repositoriesbooleanWhether organization members can create internal repositories, which are visible to all enterprise members. You can only allow members to create internal repositories if your organization is associated with an enterprise account using GitHub Enterprise Cloud or GitHub Enterprise Server 2.20+. For more information, see "Restricting repository creation in your organization" in the GitHub Help documentation. |
| members_can_create_private_repositoriesbooleanWhether organization members can create private repositories, which are visible to organization members with permission. For more information, see "Restricting repository creation in your organization" in the GitHub Help documentation. |
| members_can_create_public_repositoriesbooleanWhether organization members can create public repositories, which are visible to anyone. For more information, see "Restricting repository creation in your organization" in the GitHub Help documentation. |
| members_allowed_repository_creation_typestringSpecifies which types of repositories non-admin organization members can create.privateis only available to repositories that are part of an organization on GitHub Enterprise Cloud.Note:This parameter is closing down and will be removed in the future. Its return value ignores internal repositories. Using this parameter overrides values set inmembers_can_create_repositories. See the parameter deprecation notice in the operation description for details.Can be one of:all,private,none |
| members_can_create_pagesbooleanWhether organization members can create GitHub Pages sites. Existing published sites will not be impacted.Default:true |
| members_can_create_public_pagesbooleanWhether organization members can create public GitHub Pages sites. Existing published sites will not be impacted.Default:true |
| members_can_create_private_pagesbooleanWhether organization members can create private GitHub Pages sites. Existing published sites will not be impacted.Default:true |
| members_can_fork_private_repositoriesbooleanWhether organization members can fork private organization repositories.Default:false |
| web_commit_signoff_requiredbooleanWhether contributors to organization repositories are required to sign off on commits they make through GitHub's web interface.Default:false |
| blogstring |
| advanced_security_enabled_for_new_repositoriesbooleanEndpoint closing down notice.Please usecode security configurationsinstead.Whether GitHub Advanced Security is automatically enabled for new repositories and repositories transferred to this organization.To use this parameter, you must have admin permissions for the repository or be an owner or security manager for the organization that owns the repository. For more information, see "Managing security managers in your organization."You can check which security and analysis features are currently enabled by using aGET /orgs/{org}request. |
| dependabot_alerts_enabled_for_new_repositoriesbooleanEndpoint closing down notice.Please usecode security configurationsinstead.Whether Dependabot alerts are automatically enabled for new repositories and repositories transferred to this organization.To use this parameter, you must have admin permissions for the repository or be an owner or security manager for the organization that owns the repository. For more information, see "Managing security managers in your organization."You can check which security and analysis features are currently enabled by using aGET /orgs/{org}request. |
| dependabot_security_updates_enabled_for_new_repositoriesbooleanEndpoint closing down notice.Please usecode security configurationsinstead.Whether Dependabot security updates are automatically enabled for new repositories and repositories transferred to this organization.To use this parameter, you must have admin permissions for the repository or be an owner or security manager for the organization that owns the repository. For more information, see "Managing security managers in your organization."You can check which security and analysis features are currently enabled by using aGET /orgs/{org}request. |
| dependency_graph_enabled_for_new_repositoriesbooleanEndpoint closing down notice.Please usecode security configurationsinstead.Whether dependency graph is automatically enabled for new repositories and repositories transferred to this organization.To use this parameter, you must have admin permissions for the repository or be an owner or security manager for the organization that owns the repository. For more information, see "Managing security managers in your organization."You can check which security and analysis features are currently enabled by using aGET /orgs/{org}request. |
| secret_scanning_enabled_for_new_repositoriesbooleanEndpoint closing down notice.Please usecode security configurationsinstead.Whether secret scanning is automatically enabled for new repositories and repositories transferred to this organization.To use this parameter, you must have admin permissions for the repository or be an owner or security manager for the organization that owns the repository. For more information, see "Managing security managers in your organization."You can check which security and analysis features are currently enabled by using aGET /orgs/{org}request. |
| secret_scanning_push_protection_enabled_for_new_repositoriesbooleanEndpoint closing down notice.Please usecode security configurationsinstead.Whether secret scanning push protection is automatically enabled for new repositories and repositories transferred to this organization.To use this parameter, you must have admin permissions for the repository or be an owner or security manager for the organization that owns the repository. For more information, see "Managing security managers in your organization."You can check which security and analysis features are currently enabled by using aGET /orgs/{org}request. |
| secret_scanning_push_protection_custom_link_enabledbooleanWhether a custom link is shown to contributors who are blocked from pushing a secret by push protection. |
| secret_scanning_push_protection_custom_linkstringIfsecret_scanning_push_protection_custom_link_enabledis true, the URL that will be displayed to contributors who are blocked from pushing a secret. |
| deploy_keys_enabled_for_repositoriesbooleanControls whether or not deploy keys may be added and used for repositories in the organization. |

### HTTP response status codes for "Update an organization"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 409 | Conflict |
| 422 | Validation failed |

### Code samples for "Update an organization"

#### Request example

patch/orgs/{org}

-
-
-

`curl -L \
  -X PATCH \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG \
  -d '{"billing_email":"mona@github.com","company":"GitHub","email":"mona@github.com","twitter_username":"github","location":"San Francisco","name":"github","description":"GitHub, the company.","default_repository_permission":"read","members_can_create_repositories":true,"members_allowed_repository_creation_type":"all"}'`

Response

-
-

`Status: 200``{
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
"description": "A great organization",
"name": "github",
"company": "GitHub",
"blog": "https://github.com/blog",
"location": "San Francisco",
"email": "octocat@github.com",
"twitter_username": "github",
"is_verified": true,
"has_organization_projects": true,
"has_repository_projects": true,
"public_repos": 2,
"public_gists": 1,
"followers": 20,
"following": 0,
"html_url": "https://github.com/octocat",
"created_at": "2008-01-14T04:33:35Z",
"type": "Organization",
"total_private_repos": 100,
"owned_private_repos": 100,
"private_gists": 81,
"disk_usage": 10000,
"collaborators": 8,
"billing_email": "mona@github.com",
"plan": {
"name": "Medium",
"space": 400,
"private_repos": 20,
"filled_seats": 4,
"seats": 5
},
"default_repository_permission": "read",
"default_repository_branch": "main",
"members_can_create_repositories": true,
"two_factor_requirement_enabled": true,
"members_allowed_repository_creation_type": "all",
"members_can_create_public_repositories": false,
"members_can_create_private_repositories": false,
"members_can_create_internal_repositories": false,
"members_can_create_pages": true,
"members_can_create_public_pages": true,
"members_can_create_private_pages": true,
"members_can_delete_repositories": true,
"members_can_change_repo_visibility": true,
"members_can_invite_outside_collaborators": true,
"members_can_delete_issues": false,
"display_commenter_full_name_setting_enabled": false,
"readers_can_create_discussions": true,
"members_can_create_teams": true,
"members_can_view_dependency_insights": true,
"members_can_fork_private_repositories": false,
"web_commit_signoff_required": false,
"updated_at": "2014-03-03T18:58:10Z",
"deploy_keys_enabled_for_repositories": false,
"dependency_graph_enabled_for_new_repositories": false,
"dependabot_alerts_enabled_for_new_repositories": false,
"dependabot_security_updates_enabled_for_new_repositories": false,
"advanced_security_enabled_for_new_repositories": false,
"secret_scanning_enabled_for_new_repositories": false,
"secret_scanning_push_protection_enabled_for_new_repositories": false,
"secret_scanning_push_protection_custom_link": "https://github.com/octo-org/octo-repo/blob/main/im-blocked.md",
"secret_scanning_push_protection_custom_link_enabled": false
}`

## Delete an organization

Deletes an organization and all its repositories.

The organization login will be unavailable for 90 days after deletion.

Please review the Terms of Service regarding account deletion before using this endpoint:

[https://docs.github.com/site-policy/github-terms/github-terms-of-service](https://docs.github.com/site-policy/github-terms/github-terms-of-service)

### Fine-grained access tokens for "Delete an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" organization permissions (write)

### Parameters for "Delete an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

### HTTP response status codes for "Delete an organization"

| Status code | Description |
| --- | --- |
| 202 | Accepted |
| 403 | Forbidden |
| 404 | Resource not found |

### Code samples for "Delete an organization"

#### Request example

delete/orgs/{org}

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG`

Accepted

-
-

`Status: 202`

## List app installations for an organization

Lists all GitHub Apps in an organization. The installation count includes
all GitHub Apps installed on repositories in the organization.

The authenticated user must be an organization owner to use this endpoint.

OAuth app tokens and personal access tokens (classic) need the `admin:read` scope to use this endpoint.

### Fine-grained access tokens for "List app installations for an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" organization permissions (read)

### Parameters for "List app installations for an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| pageintegerThe page number of the results to fetch. For more information, see "Using pagination in the REST API."Default:1 |

### HTTP response status codes for "List app installations for an organization"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "List app installations for an organization"

#### Request example

get/orgs/{org}/installations

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/installations`

Response

-
-

`Status: 200``{
"total_count": 1,
"installations": [
{
"id": 25381,
"account": {
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
"repository_selection": "selected",
"access_tokens_url": "https://api.github.com/app/installations/25381/access_tokens",
"repositories_url": "https://api.github.com/installation/repositories",
"html_url": "https://github.com/organizations/octo-org/settings/installations/25381",
"app_id": 2218,
"target_id": 6811672,
"target_type": "Organization",
"permissions": {
"deployments": "write",
"metadata": "read",
"pull_requests": "read",
"statuses": "read"
},
"events": [
"deployment",
"deployment_status"
],
"created_at": "2017-05-16T08:47:09.000-07:00",
"updated_at": "2017-06-06T11:23:23.000-07:00",
"single_file_name": "config.yml",
"has_multiple_single_files": true,
"single_file_paths": [
"config.yml",
".github/issue_TEMPLATE.md"
],
"app_slug": "github-actions",
"suspended_at": null,
"suspended_by": null
}
]
}`

## Get immutable releases settings for an organization

Gets the immutable releases policy for repositories in an organization.

OAuth tokens and personal access tokens (classic) need the `admin:org` scope to use this endpoint.

### Fine-grained access tokens for "Get immutable releases settings for an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" organization permissions (read)

### Parameters for "Get immutable releases settings for an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

### HTTP response status codes for "Get immutable releases settings for an organization"

| Status code | Description |
| --- | --- |
| 200 | Immutable releases settings response |

### Code samples for "Get immutable releases settings for an organization"

#### Request example

get/orgs/{org}/settings/immutable-releases

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/settings/immutable-releases`

Immutable releases settings response

-
-

`Status: 200``{
"enforced_repositories": "all"
}`

## Set immutable releases settings for an organization

Sets the immutable releases policy for repositories in an organization.

OAuth tokens and personal access tokens (classic) need the `admin:org` scope to use this endpoint.

### Fine-grained access tokens for "Set immutable releases settings for an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" organization permissions (write)

### Parameters for "Set immutable releases settings for an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| enforced_repositoriesstringRequiredThe policy that controls how immutable releases are enforced in the organization.Can be one of:all,none,selected |
| selected_repository_idsarray of integersAn array of repository ids for which immutable releases enforcement should be applied. You can only provide a list of repository ids when theenforced_repositoriesis set toselected. You can add and remove individual repositories using theEnable a selected repository for immutable releases in an organizationandDisable a selected repository for immutable releases in an organizationendpoints. |

### HTTP response status codes for "Set immutable releases settings for an organization"

| Status code | Description |
| --- | --- |
| 204 | No Content |

### Code samples for "Set immutable releases settings for an organization"

#### Request example

put/orgs/{org}/settings/immutable-releases

-
-
-

`curl -L \
  -X PUT \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/settings/immutable-releases \
  -d '{"enforced_repositories":"all"}'`

Response

`Status: 204`

## List selected repositories for immutable releases enforcement

List all of the repositories that have been selected for immutable releases enforcement in an organization.

OAuth tokens and personal access tokens (classic) need the `admin:org` scope to use this endpoint.

### Fine-grained access tokens for "List selected repositories for immutable releases enforcement"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" organization permissions (read)

### Parameters for "List selected repositories for immutable releases enforcement"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| pageintegerThe page number of the results to fetch. For more information, see "Using pagination in the REST API."Default:1 |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |

### HTTP response status codes for "List selected repositories for immutable releases enforcement"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "List selected repositories for immutable releases enforcement"

#### Request example

get/orgs/{org}/settings/immutable-releases/repositories

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/settings/immutable-releases/repositories`

Response

-
-

`Status: 200``{
"total_count": 1,
"repositories": [
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
]
}`

## Set selected repositories for immutable releases enforcement

Replaces all repositories that have been selected for immutable releases enforcement in an organization. To use this endpoint, the organization immutable releases policy for `enforced_repositories` must be configured to `selected`.

OAuth tokens and personal access tokens (classic) need the `admin:org` scope to use this endpoint.

### Fine-grained access tokens for "Set selected repositories for immutable releases enforcement"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" organization permissions (write) and "Metadata" repository permissions (read)

### Parameters for "Set selected repositories for immutable releases enforcement"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| selected_repository_idsarray of integersRequiredAn array of repository ids for which immutable releases enforcement should be applied. You can only provide a list of repository ids when theenforced_repositoriesis set toselected. You can add and remove individual repositories using theEnable a selected repository for immutable releases in an organizationandDisable a selected repository for immutable releases in an organizationendpoints. |

### HTTP response status codes for "Set selected repositories for immutable releases enforcement"

| Status code | Description |
| --- | --- |
| 204 | No Content |

### Code samples for "Set selected repositories for immutable releases enforcement"

#### Request example

put/orgs/{org}/settings/immutable-releases/repositories

-
-
-

`curl -L \
  -X PUT \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/settings/immutable-releases/repositories \
  -d '{"selected_repository_ids":[64780797]}'`

Response

`Status: 204`

## Enable a selected repository for immutable releases in an organization

Adds a repository to the list of selected repositories that are enforced for immutable releases in an organization. To use this endpoint, the organization immutable releases policy for `enforced_repositories` must be configured to `selected`.

OAuth tokens and personal access tokens (classic) need the `admin:org` scope to use this endpoint.

### Fine-grained access tokens for "Enable a selected repository for immutable releases in an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" organization permissions (write) and "Metadata" repository permissions (read)

### Parameters for "Enable a selected repository for immutable releases in an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| repository_idintegerRequiredThe unique identifier of the repository. |

### HTTP response status codes for "Enable a selected repository for immutable releases in an organization"

| Status code | Description |
| --- | --- |
| 204 | No Content |

### Code samples for "Enable a selected repository for immutable releases in an organization"

#### Request example

put/orgs/{org}/settings/immutable-releases/repositories/{repository_id}

-
-
-

`curl -L \
  -X PUT \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/settings/immutable-releases/repositories/REPOSITORY_ID`

Response

`Status: 204`

## Disable a selected repository for immutable releases in an organization

Removes a repository from the list of selected repositories that are enforced for immutable releases in an organization. To use this endpoint, the organization immutable releases policy for `enforced_repositories` must be configured to `selected`.

OAuth tokens and personal access tokens (classic) need the `admin:org` scope to use this endpoint.

### Fine-grained access tokens for "Disable a selected repository for immutable releases in an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" organization permissions (write) and "Metadata" repository permissions (read)

### Parameters for "Disable a selected repository for immutable releases in an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| repository_idintegerRequiredThe unique identifier of the repository. |

### HTTP response status codes for "Disable a selected repository for immutable releases in an organization"

| Status code | Description |
| --- | --- |
| 204 | No Content |

### Code samples for "Disable a selected repository for immutable releases in an organization"

#### Request example

delete/orgs/{org}/settings/immutable-releases/repositories/{repository_id}

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/settings/immutable-releases/repositories/REPOSITORY_ID`

Response

`Status: 204`

## Enable or disable a security feature for an organization

Warning

**Closing down notice:** The ability to enable or disable a security feature for all eligible repositories in an organization is closing down. Please use [code security configurations](https://docs.github.com/rest/code-security/configurations) instead. For more information, see the [changelog](https://github.blog/changelog/2024-07-22-deprecation-of-api-endpoint-to-enable-or-disable-a-security-feature-for-an-organization/).

Enables or disables the specified security feature for all eligible repositories in an organization. For more information, see "[Managing security managers in your organization](https://docs.github.com/organizations/managing-peoples-access-to-your-organization-with-roles/managing-security-managers-in-your-organization)."

The authenticated user must be an organization owner or be member of a team with the security manager role to use this endpoint.

OAuth app tokens and personal access tokens (classic) need the `admin:org`, `write:org`, or `repo` scopes to use this endpoint.

### Fine-grained access tokens for "Enable or disable a security feature for an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" organization permissions (write)

### Parameters for "Enable or disable a security feature for an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| security_productstringRequiredThe security feature to enable or disable.Can be one of:dependency_graph,dependabot_alerts,dependabot_security_updates,advanced_security,code_scanning_default_setup,secret_scanning,secret_scanning_push_protection |
| enablementstringRequiredThe action to take.enable_allmeans to enable the specified security feature for all repositories in the organization.disable_allmeans to disable the specified security feature for all repositories in the organization.Can be one of:enable_all,disable_all |

| Name, Type, Description |
| --- |
| query_suitestringCodeQL query suite to be used. If you specify thequery_suiteparameter, the default setup will be configured with this query suite only on all repositories that didn't have default setup already configured. It will not change the query suite on repositories that already have default setup configured.
If you don't specify anyquery_suitein your request, the preferred query suite of the organization will be applied.Can be one of:default,extended |

### HTTP response status codes for "Enable or disable a security feature for an organization"

| Status code | Description |
| --- | --- |
| 204 | Action started |
| 422 | The action could not be taken due to an in progress enablement, or a policy is preventing enablement |

### Code samples for "Enable or disable a security feature for an organization"

#### Request example

post/orgs/{org}/{security_product}/{enablement}

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/SECURITY_PRODUCT/ENABLEMENT`

Action started

`Status: 204`

## List organizations for the authenticated user

List organizations for the authenticated user.

For OAuth app tokens and personal access tokens (classic), this endpoint only lists organizations that your authorization allows you to operate on in some way (e.g., you can list teams with `read:org` scope, you can publicize your organization membership with `user` scope, etc.). Therefore, this API requires at least `user` or `read:org` scope for OAuth app tokens and personal access tokens (classic). Requests with insufficient scope will receive a `403 Forbidden` response.

Note

Requests using a fine-grained access token will receive a `200 Success` response with an empty list.

### Fine-grained access tokens for "List organizations for the authenticated user"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token does not require any permissions.

### Parameters for "List organizations for the authenticated user"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| pageintegerThe page number of the results to fetch. For more information, see "Using pagination in the REST API."Default:1 |

### HTTP response status codes for "List organizations for the authenticated user"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 304 | Not modified |
| 401 | Requires authentication |
| 403 | Forbidden |

### Code samples for "List organizations for the authenticated user"

#### Request example

get/user/orgs

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/user/orgs`

Response

-
-

`Status: 200``[
{
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
}
]`

## List organizations for a user

List [public organization memberships](https://docs.github.com/articles/publicizing-or-concealing-organization-membership) for the specified user.

This method only lists *public* memberships, regardless of authentication. If you need to fetch all of the organization memberships (public and private) for the authenticated user, use the [List organizations for the authenticated user](https://docs.github.com/rest/orgs/orgs#list-organizations-for-the-authenticated-user) API instead.

### Fine-grained access tokens for "List organizations for a user"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token does not require any permissions.

This endpoint can be used without authentication if only public resources are requested.

### Parameters for "List organizations for a user"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| usernamestringRequiredThe handle for the GitHub user account. |

| Name, Type, Description |
| --- |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| pageintegerThe page number of the results to fetch. For more information, see "Using pagination in the REST API."Default:1 |

### HTTP response status codes for "List organizations for a user"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "List organizations for a user"

#### Request example

get/users/{username}/orgs

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/users/USERNAME/orgs`

Response

-
-

`Status: 200``[
{
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
}
]`

---

# REST API endpoints for outside collaborators

> Use the REST API to manage outside collaborators.

## List outside collaborators for an organization

List all users who are outside collaborators of an organization.

### Fine-grained access tokens for "List outside collaborators for an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Members" organization permissions (read)

### Parameters for "List outside collaborators for an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| filterstringFilter the list of outside collaborators.2fa_disabledmeans that only outside collaborators withouttwo-factor authenticationenabled will be returned.2fa_insecuremeans that only outside collaborators withinsecure 2FA methodswill be returned.Default:allCan be one of:2fa_disabled,2fa_insecure,all |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| pageintegerThe page number of the results to fetch. For more information, see "Using pagination in the REST API."Default:1 |

### HTTP response status codes for "List outside collaborators for an organization"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "List outside collaborators for an organization"

#### Request example

get/orgs/{org}/outside_collaborators

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/outside_collaborators`

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

## Convert an organization member to outside collaborator

When an organization member is converted to an outside collaborator, they'll only have access to the repositories that their current team membership allows. The user will no longer be a member of the organization. For more information, see "[Converting an organization member to an outside collaborator](https://docs.github.com/articles/converting-an-organization-member-to-an-outside-collaborator/)". Converting an organization member to an outside collaborator may be restricted by enterprise administrators. For more information, see "[Enforcing repository management policies in your enterprise](https://docs.github.com/admin/policies/enforcing-policies-for-your-enterprise/enforcing-repository-management-policies-in-your-enterprise#enforcing-a-policy-for-inviting-outside-collaborators-to-repositories)."

### Fine-grained access tokens for "Convert an organization member to outside collaborator"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Members" organization permissions (write)

### Parameters for "Convert an organization member to outside collaborator"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| usernamestringRequiredThe handle for the GitHub user account. |

| Name, Type, Description |
| --- |
| asyncbooleanWhen set totrue, the request will be performed asynchronously. Returns a 202 status code when the job is successfully queued.Default:false |

### HTTP response status codes for "Convert an organization member to outside collaborator"

| Status code | Description |
| --- | --- |
| 202 | User is getting converted asynchronously |
| 204 | User was converted |
| 403 | Forbidden if user is the last owner of the organization, not a member of the organization, or if the enterprise enforces a policy for inviting outside collaborators. For more information, see "Enforcing repository management policies in your enterprise." |
| 404 | Resource not found |

### Code samples for "Convert an organization member to outside collaborator"

#### Request examples

Select the example typeStatus code 202, asynchronous request (application/json)Status code 204, synchronous request (undefined)put/orgs/{org}/outside_collaborators/{username}

-
-
-

`curl -L \
  -X PUT \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/outside_collaborators/USERNAME \
  -d '{"async":true}'`

User is getting converted asynchronously

-
-

`Status: 202`

## Remove outside collaborator from an organization

Removing a user from this list will remove them from all the organization's repositories.

### Fine-grained access tokens for "Remove outside collaborator from an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Members" organization permissions (write)

### Parameters for "Remove outside collaborator from an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| usernamestringRequiredThe handle for the GitHub user account. |

### HTTP response status codes for "Remove outside collaborator from an organization"

| Status code | Description |
| --- | --- |
| 204 | No Content |
| 422 | Unprocessable Entity if user is a member of the organization |

### Code samples for "Remove outside collaborator from an organization"

#### Request example

delete/orgs/{org}/outside_collaborators/{username}

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/outside_collaborators/USERNAME`

Response

`Status: 204`
