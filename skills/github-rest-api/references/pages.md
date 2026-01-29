# REST API endpoints for GitHub Pages

# REST API endpoints for GitHub Pages

> Use the REST API to interact with GitHub Pages sites and builds.

## Get a GitHub Pages site

Gets information about a GitHub Pages site.

OAuth app tokens and personal access tokens (classic) need the `repo` scope to use this endpoint.

### Fine-grained access tokens for "Get a GitHub Pages site"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Pages" repository permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "Get a GitHub Pages site"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

### HTTP response status codes for "Get a GitHub Pages site"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |

### Code samples for "Get a GitHub Pages site"

#### Request example

get/repos/{owner}/{repo}/pages

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/pages`

Response

-
-

`Status: 200``{
"url": "https://api.github.com/repos/github/developer.github.com/pages",
"status": "built",
"cname": "developer.github.com",
"custom_404": false,
"html_url": "https://developer.github.com",
"source": {
"branch": "master",
"path": "/"
},
"public": true,
"pending_domain_unverified_at": "2024-04-30T19:33:31Z",
"protected_domain_state": "verified",
"https_certificate": {
"state": "approved",
"description": "Certificate is approved",
"domains": [
"developer.github.com"
],
"expires_at": "2021-05-22"
},
"https_enforced": true
}`

## Create a GitHub Pages site

Configures a GitHub Pages site. For more information, see "[About GitHub Pages](https://docs.github.com/github/working-with-github-pages/about-github-pages)."

The authenticated user must be a repository administrator, maintainer, or have the 'manage GitHub Pages settings' permission.

OAuth app tokens and personal access tokens (classic) need the `repo` scope to use this endpoint.

### Fine-grained access tokens for "Create a GitHub Pages site"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Pages" repository permissions (write) and "Administration" repository permissions (write)

### Parameters for "Create a GitHub Pages site"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| build_typestringThe process in which the Page will be built. Possible values are"legacy"and"workflow".Can be one of:legacy,workflow |
| sourceobjectThe source branch and directory used to publish your Pages site. |
| Name, Type, DescriptionbranchstringRequiredThe repository branch used to publish your site's source files.pathstringThe repository directory that includes the source files for the Pages site. Allowed paths are/or/docs. Default:/Default:/Can be one of:/,/docs |
| Name, Type, Description |
| branchstringRequiredThe repository branch used to publish your site's source files. |
| pathstringThe repository directory that includes the source files for the Pages site. Allowed paths are/or/docs. Default:/Default:/Can be one of:/,/docs |

### HTTP response status codes for "Create a GitHub Pages site"

| Status code | Description |
| --- | --- |
| 201 | Created |
| 409 | Conflict |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Create a GitHub Pages site"

#### Request example

post/repos/{owner}/{repo}/pages

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/pages \
  -d '{"source":{"branch":"main","path":"/docs"}}'`

Response

-
-

`Status: 201``{
"url": "https://api.github.com/repos/github/developer.github.com/pages",
"status": "built",
"cname": "developer.github.com",
"custom_404": false,
"html_url": "https://developer.github.com",
"source": {
"branch": "master",
"path": "/"
},
"public": true,
"pending_domain_unverified_at": "2024-04-30T19:33:31Z",
"protected_domain_state": "verified",
"https_certificate": {
"state": "approved",
"description": "Certificate is approved",
"domains": [
"developer.github.com"
],
"expires_at": "2021-05-22"
},
"https_enforced": true
}`

## Update information about a GitHub Pages site

Updates information for a GitHub Pages site. For more information, see "[About GitHub Pages](https://docs.github.com/github/working-with-github-pages/about-github-pages).

The authenticated user must be a repository administrator, maintainer, or have the 'manage GitHub Pages settings' permission.

OAuth app tokens and personal access tokens (classic) need the `repo` scope to use this endpoint.

### Fine-grained access tokens for "Update information about a GitHub Pages site"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Pages" repository permissions (write) and "Administration" repository permissions (write)

### Parameters for "Update information about a GitHub Pages site"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| cnamestring or nullSpecify a custom domain for the repository. Sending anullvalue will remove the custom domain. For more about custom domains, see "Using a custom domain with GitHub Pages." |
| https_enforcedbooleanSpecify whether HTTPS should be enforced for the repository. |
| build_typestringThe process by which the GitHub Pages site will be built.workflowmeans that the site is built by a custom GitHub Actions workflow.legacymeans that the site is built by GitHub when changes are pushed to a specific branch.Can be one of:legacy,workflow |
| sourceobjectUpdate the source for the repository. Must include the branch name and path. |
| Name, Type, DescriptionbranchstringRequiredThe repository branch used to publish your site's source files.pathstringRequiredThe repository directory that includes the source files for the Pages site. Allowed paths are/or/docs.Can be one of:/,/docs |
| Name, Type, Description |
| branchstringRequiredThe repository branch used to publish your site's source files. |
| pathstringRequiredThe repository directory that includes the source files for the Pages site. Allowed paths are/or/docs.Can be one of:/,/docs |

### HTTP response status codes for "Update information about a GitHub Pages site"

| Status code | Description |
| --- | --- |
| 204 | No Content |
| 400 | Bad Request |
| 409 | Conflict |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Update information about a GitHub Pages site"

#### Request example

put/repos/{owner}/{repo}/pages

-
-
-

`curl -L \
  -X PUT \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/pages \
  -d '{"cname":"octocatblog.com","source":{"branch":"main","path":"/"}}'`

Response

`Status: 204`

## Delete a GitHub Pages site

Deletes a GitHub Pages site. For more information, see "[About GitHub Pages](https://docs.github.com/github/working-with-github-pages/about-github-pages).

The authenticated user must be a repository administrator, maintainer, or have the 'manage GitHub Pages settings' permission.

OAuth app tokens and personal access tokens (classic) need the `repo` scope to use this endpoint.

### Fine-grained access tokens for "Delete a GitHub Pages site"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Pages" repository permissions (write) and "Administration" repository permissions (write)

### Parameters for "Delete a GitHub Pages site"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

### HTTP response status codes for "Delete a GitHub Pages site"

| Status code | Description |
| --- | --- |
| 204 | No Content |
| 404 | Resource not found |
| 409 | Conflict |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Delete a GitHub Pages site"

#### Request example

delete/repos/{owner}/{repo}/pages

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/pages`

Response

`Status: 204`

## List GitHub Pages builds

Lists builts of a GitHub Pages site.

OAuth app tokens and personal access tokens (classic) need the `repo` scope to use this endpoint.

### Fine-grained access tokens for "List GitHub Pages builds"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Pages" repository permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "List GitHub Pages builds"

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

### HTTP response status codes for "List GitHub Pages builds"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "List GitHub Pages builds"

#### Request example

get/repos/{owner}/{repo}/pages/builds

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/pages/builds`

Response

-
-

`Status: 200``[
{
"url": "https://api.github.com/repos/github/developer.github.com/pages/builds/5472601",
"status": "built",
"error": {
"message": null
},
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
},
"commit": "351391cdcb88ffae71ec3028c91f375a8036a26b",
"duration": 2104,
"created_at": "2014-02-10T19:00:49Z",
"updated_at": "2014-02-10T19:00:51Z"
}
]`

## Request a GitHub Pages build

You can request that your site be built from the latest revision on the default branch. This has the same effect as pushing a commit to your default branch, but does not require an additional commit. Manually triggering page builds can be helpful when diagnosing build warnings and failures.

Build requests are limited to one concurrent build per repository and one concurrent build per requester. If you request a build while another is still in progress, the second request will be queued until the first completes.

### Fine-grained access tokens for "Request a GitHub Pages build"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Pages" repository permissions (write)

### Parameters for "Request a GitHub Pages build"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

### HTTP response status codes for "Request a GitHub Pages build"

| Status code | Description |
| --- | --- |
| 201 | Created |

### Code samples for "Request a GitHub Pages build"

#### Request example

post/repos/{owner}/{repo}/pages/builds

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/pages/builds`

Response

-
-

`Status: 201``{
"url": "https://api.github.com/repos/github/developer.github.com/pages/builds/latest",
"status": "queued"
}`

## Get latest Pages build

Gets information about the single most recent build of a GitHub Pages site.

OAuth app tokens and personal access tokens (classic) need the `repo` scope to use this endpoint.

### Fine-grained access tokens for "Get latest Pages build"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Pages" repository permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "Get latest Pages build"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

### HTTP response status codes for "Get latest Pages build"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "Get latest Pages build"

#### Request example

get/repos/{owner}/{repo}/pages/builds/latest

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/pages/builds/latest`

Response

-
-

`Status: 200``{
"url": "https://api.github.com/repos/github/developer.github.com/pages/builds/5472601",
"status": "built",
"error": {
"message": null
},
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
},
"commit": "351391cdcb88ffae71ec3028c91f375a8036a26b",
"duration": 2104,
"created_at": "2014-02-10T19:00:49Z",
"updated_at": "2014-02-10T19:00:51Z"
}`

## Get GitHub Pages build

Gets information about a GitHub Pages build.

OAuth app tokens and personal access tokens (classic) need the `repo` scope to use this endpoint.

### Fine-grained access tokens for "Get GitHub Pages build"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Pages" repository permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "Get GitHub Pages build"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| build_idintegerRequired |

### HTTP response status codes for "Get GitHub Pages build"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "Get GitHub Pages build"

#### Request example

get/repos/{owner}/{repo}/pages/builds/{build_id}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/pages/builds/BUILD_ID`

Response

-
-

`Status: 200``{
"url": "https://api.github.com/repos/github/developer.github.com/pages/builds/5472601",
"status": "built",
"error": {
"message": null
},
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
},
"commit": "351391cdcb88ffae71ec3028c91f375a8036a26b",
"duration": 2104,
"created_at": "2014-02-10T19:00:49Z",
"updated_at": "2014-02-10T19:00:51Z"
}`

## Create a GitHub Pages deployment

Create a GitHub Pages deployment for a repository.

The authenticated user must have write permission to the repository.

### Fine-grained access tokens for "Create a GitHub Pages deployment"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Pages" repository permissions (write)

### Parameters for "Create a GitHub Pages deployment"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| artifact_idnumberThe ID of an artifact that contains the .zip or .tar of static assets to deploy. The artifact belongs to the repository. Eitherartifact_idorartifact_urlare required. |
| artifact_urlstringThe URL of an artifact that contains the .zip or .tar of static assets to deploy. The artifact belongs to the repository. Eitherartifact_idorartifact_urlare required. |
| environmentstringThe target environment for this GitHub Pages deployment.Default:github-pages |
| pages_build_versionstringRequiredA unique string that represents the version of the build for this deployment.Default:GITHUB_SHA |
| oidc_tokenstringRequiredThe OIDC token issued by GitHub Actions certifying the origin of the deployment. |

### HTTP response status codes for "Create a GitHub Pages deployment"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 400 | Bad Request |
| 404 | Resource not found |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Create a GitHub Pages deployment"

#### Request example

post/repos/{owner}/{repo}/pages/deployments

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/pages/deployments \
  -d '{"artifact_url":"https://downloadcontent/","environment":"github-pages","pages_build_version":"4fd754f7e594640989b406850d0bc8f06a121251","oidc_token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IlV2R1h4SUhlY0JFc1JCdEttemUxUEhfUERiVSIsImtpZCI6IjUyRjE5N0M0ODFERTcwMTEyQzQ0MUI0QTlCMzdCNTNDN0ZDRjBEQjUifQ.eyJqdGkiOiJhMWIwNGNjNy0zNzZiLTQ1N2QtOTMzNS05NTY5YmVjZDExYTIiLCJzdWIiOiJyZXBvOnBhcGVyLXNwYS9taW55aTplbnZpcm9ubWVudDpQcm9kdWN0aW9uIiwiYXVkIjoiaHR0cHM6Ly9naXRodWIuY29tL3BhcGVyLXNwYSIsInJlZiI6InJlZnMvaGVhZHMvbWFpbiIsInNoYSI6ImEyODU1MWJmODdiZDk3NTFiMzdiMmM0YjM3M2MxZjU3NjFmYWM2MjYiLCJyZXBvc2l0b3J5IjoicGFwZXItc3BhL21pbnlpIiwicmVwb3NpdG9yeV9vd25lciI6InBhcGVyLXNwYSIsInJ1bl9pZCI6IjE1NDY0NTkzNjQiLCJydW5fbnVtYmVyIjoiMzQiLCJydW5fYXR0ZW1wdCI6IjYiLCJhY3RvciI6IllpTXlzdHkiLCJ3b3JrZmxvdyI6IkNJIiwiaGVhZF9yZWYiOiIiLCJiYXNlX3JlZiI6IiIsImV2ZW50X25hbWUiOiJwdXNoIiwicmVmX3R5cGUiOiJicmFuY2giLCJlbnZpcm9ubWVudCI6IlByb2R1Y3Rpb24iLCJqb2Jfd29ya2Zsb3dfcmVmIjoicGFwZXItc3BhL21pbnlpLy5naXRodWIvd29ya2Zsb3dzL2JsYW5rLnltbEByZWZzL2hlYWRzL21haW4iLCJpc3MiOiJodHRwczovL3Rva2VuLmFjdGlvbnMuZ2l0aHVidXNlcmNvbnRlbnQuY29tIiwibmJmIjoxNjM5MDAwODU2LCJleHAiOjE2MzkwMDE3NTYsImlhdCI6MTYzOTAwMTQ1Nn0.VP8WictbQECKozE2SgvKb2FqJ9hisWsoMkYRTqfBrQfZTCXi5IcFEdgDMB2X7a99C2DeUuTvHh9RMKXLL2a0zg3-Sd7YrO7a2ll2kNlnvyIypcN6AeIc7BxHsTTnZN9Ud_xmEsTrSRGOEKmzCFkULQ6N4zlVD0sidypmXlMemmWEcv_ZHqhioEI_VMp5vwXQurketWH7qX4oDgG4okyYtPrv5RQHbfQcVo9izaPJ_jnsDd0CBA0QOx9InjPidtIkMYQLyUgJy33HLJy86EFNUnAf8UhBQuQi5mAsEpEzBBuKpG3PDiPtYCHOk64JZkZGd5mR888a5sbHRiaF8hm8YA"}'`

Response

-
-

`Status: 200``{
"id": "4fd754f7e594640989b406850d0bc8f06a121251",
"status_url": "https://api.github.com/repos/github/developer.github.com/pages/deployments/4fd754f7e594640989b406850d0bc8f06a121251/status",
"page_url": "developer.github.com"
}`

## Get the status of a GitHub Pages deployment

Gets the current status of a GitHub Pages deployment.

The authenticated user must have read permission for the GitHub Pages site.

### Fine-grained access tokens for "Get the status of a GitHub Pages deployment"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Pages" repository permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "Get the status of a GitHub Pages deployment"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| pages_deployment_idRequiredThe ID of the Pages deployment. You can also give the commit SHA of the deployment. |

### HTTP response status codes for "Get the status of a GitHub Pages deployment"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |

### Code samples for "Get the status of a GitHub Pages deployment"

#### Request example

get/repos/{owner}/{repo}/pages/deployments/{pages_deployment_id}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/pages/deployments/PAGES_DEPLOYMENT_ID`

Response

-
-

`Status: 200``{
"status": "succeed"
}`

## Cancel a GitHub Pages deployment

Cancels a GitHub Pages deployment.

The authenticated user must have write permissions for the GitHub Pages site.

### Fine-grained access tokens for "Cancel a GitHub Pages deployment"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Pages" repository permissions (write)

### Parameters for "Cancel a GitHub Pages deployment"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| pages_deployment_idRequiredThe ID of the Pages deployment. You can also give the commit SHA of the deployment. |

### HTTP response status codes for "Cancel a GitHub Pages deployment"

| Status code | Description |
| --- | --- |
| 204 | A header with no content is returned. |
| 404 | Resource not found |

### Code samples for "Cancel a GitHub Pages deployment"

#### Request example

post/repos/{owner}/{repo}/pages/deployments/{pages_deployment_id}/cancel

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/pages/deployments/PAGES_DEPLOYMENT_ID/cancel`

A header with no content is returned.

`Status: 204`

## Get a DNS health check for GitHub Pages

Gets a health check of the DNS settings for the `CNAME` record configured for a repository's GitHub Pages.

The first request to this endpoint returns a `202 Accepted` status and starts an asynchronous background task to get the results for the domain. After the background task completes, subsequent requests to this endpoint return a `200 OK` status with the health check results in the response.

The authenticated user must be a repository administrator, maintainer, or have the 'manage GitHub Pages settings' permission to use this endpoint.

OAuth app tokens and personal access tokens (classic) need the `repo` scope to use this endpoint.

### Fine-grained access tokens for "Get a DNS health check for GitHub Pages"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write) and "Pages" repository permissions (write)

### Parameters for "Get a DNS health check for GitHub Pages"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

### HTTP response status codes for "Get a DNS health check for GitHub Pages"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 202 | Empty response |
| 400 | Custom domains are not available for GitHub Pages |
| 404 | Resource not found |
| 422 | There isn't a CNAME for this page |

### Code samples for "Get a DNS health check for GitHub Pages"

#### Request example

get/repos/{owner}/{repo}/pages/health

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/pages/health`

Response

-
-

`Status: 200``{
"domain": {
"host": "example.com",
"uri": "http://example.com/",
"nameservers": "default",
"dns_resolves": true,
"is_proxied": false,
"is_cloudflare_ip": false,
"is_fastly_ip": false,
"is_old_ip_address": false,
"is_a_record": true,
"has_cname_record": false,
"has_mx_records_present": false,
"is_valid_domain": true,
"is_apex_domain": true,
"should_be_a_record": true,
"is_cname_to_github_user_domain": false,
"is_cname_to_pages_dot_github_dot_com": false,
"is_cname_to_fastly": false,
"is_pointed_to_github_pages_ip": true,
"is_non_github_pages_ip_present": false,
"is_pages_domain": false,
"is_served_by_pages": true,
"is_valid": true,
"reason": null,
"responds_to_https": true,
"enforces_https": true,
"https_error": null,
"is_https_eligible": true,
"caa_error": null
},
"alt_domain": {
"host": "www.example.com",
"uri": "http://www.example.com/",
"nameservers": "default",
"dns_resolves": true,
"is_proxied": false,
"is_cloudflare_ip": false,
"is_fastly_ip": false,
"is_old_ip_address": false,
"is_a_record": true,
"has_cname_record": false,
"has_mx_records_present": false,
"is_valid_domain": true,
"is_apex_domain": true,
"should_be_a_record": true,
"is_cname_to_github_user_domain": false,
"is_cname_to_pages_dot_github_dot_com": false,
"is_cname_to_fastly": false,
"is_pointed_to_github_pages_ip": true,
"is_non_github_pages_ip_present": false,
"is_pages_domain": false,
"is_served_by_pages": true,
"is_valid": true,
"reason": null,
"responds_to_https": true,
"enforces_https": true,
"https_error": null,
"is_https_eligible": true,
"caa_error": null
}
}`
