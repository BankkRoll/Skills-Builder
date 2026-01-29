# REST API endpoints for Codespaces and more

# REST API endpoints for Codespaces

> Use the REST API to manage GitHub Codespaces.

## About GitHub Codespaces

You can manage Codespaces using the REST API. These endpoints are available for authenticated users, OAuth apps, and GitHub Apps. For more information, see [Codespaces documentation](https://docs.github.com/en/codespaces).

---

# REST API endpoints for Codespaces machines

> Use the REST API to manage availability of machine types for a codespace.

## About Codespaces machines

You can determine which machine types are available to create a codespace, either on a given repository or as an authenticated user. For more information, see [Changing the machine type for your codespace](https://docs.github.com/en/codespaces/customizing-your-codespace/changing-the-machine-type-for-your-codespace#about-machine-types).

You can also use this information when changing the machine of an existing codespace by updating its `machine` property. The machine update will take place the next time the codespace is restarted. For more information, see [Changing the machine type for your codespace](https://docs.github.com/en/codespaces/customizing-your-codespace/changing-the-machine-type-for-your-codespace).

---

# REST API endpoints for Codespaces organization secrets

> Use the REST API to manage your organization-level Codespaces secrets.

The REST API is now versioned. For more information, see "[About API versioning](https://docs.github.com/rest/overview/api-versions)."

# REST API endpoints for Codespaces organization secrets

Use the REST API to manage your organization-level Codespaces secrets.

Note

These endpoints are currently in public preview and subject to change.

## List organization secrets

Lists all Codespaces development environment secrets available at the organization-level without revealing their encrypted
values.

OAuth app tokens and personal access tokens (classic) need the `admin:org` scope to use this endpoint.

### Fine-grained access tokens for "List organization secrets"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Organization codespaces secrets" organization permissions (read)

### Parameters for "List organization secrets"

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

### HTTP response status codes for "List organization secrets"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "List organization secrets"

#### Request example

get/orgs/{org}/codespaces/secrets

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/codespaces/secrets`

Response

-
-

`Status: 200``{
"total_count": 2,
"secrets": [
{
"name": "GH_TOKEN",
"created_at": "2019-08-10T14:59:22Z",
"updated_at": "2020-01-10T14:59:22Z",
"visibility": "all"
},
{
"name": "GIST_ID",
"created_at": "2020-01-10T10:59:22Z",
"updated_at": "2020-01-11T11:59:22Z",
"visibility": "all"
}
]
}`

## Get an organization public key

Gets a public key for an organization, which is required in order to encrypt secrets. You need to encrypt the value of a secret before you can create or update secrets.
OAuth app tokens and personal access tokens (classic) need the `admin:org` scope to use this endpoint.

### Fine-grained access tokens for "Get an organization public key"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Organization codespaces secrets" organization permissions (read)

### Parameters for "Get an organization public key"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

### HTTP response status codes for "Get an organization public key"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "Get an organization public key"

#### Request example

get/orgs/{org}/codespaces/secrets/public-key

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/codespaces/secrets/public-key`

Response

-
-

`Status: 200``{
"key_id": "012345678912345678",
"key": "2Sg8iYjAxxmI2LvUXpJjkYrMxURPc8r+dB7TJyvv1234"
}`

## Get an organization secret

Gets an organization development environment secret without revealing its encrypted value.

OAuth app tokens and personal access tokens (classic) need the `admin:org` scope to use this endpoint.

### Fine-grained access tokens for "Get an organization secret"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Organization codespaces secrets" organization permissions (read)

### Parameters for "Get an organization secret"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| secret_namestringRequiredThe name of the secret. |

### HTTP response status codes for "Get an organization secret"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "Get an organization secret"

#### Request example

get/orgs/{org}/codespaces/secrets/{secret_name}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/codespaces/secrets/SECRET_NAME`

Response

-
-

`Status: 200``{
"name": "GH_TOKEN",
"created_at": "2019-08-10T14:59:22Z",
"updated_at": "2020-01-10T14:59:22Z",
"visibility": "all"
}`

## Create or update an organization secret

Creates or updates an organization development environment secret with an encrypted value. Encrypt your secret using
[LibSodium](https://libsodium.gitbook.io/doc/bindings_for_other_languages). For more information, see "[Encrypting secrets for the REST API](https://docs.github.com/rest/guides/encrypting-secrets-for-the-rest-api)."

OAuth app tokens and personal access tokens (classic) need the `admin:org` scope to use this endpoint.

### Fine-grained access tokens for "Create or update an organization secret"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Organization codespaces secrets" organization permissions (write)

### Parameters for "Create or update an organization secret"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| secret_namestringRequiredThe name of the secret. |

| Name, Type, Description |
| --- |
| encrypted_valuestringThe value for your secret, encrypted withLibSodiumusing the public key retrieved from theGet an organization public keyendpoint. |
| key_idstringThe ID of the key you used to encrypt the secret. |
| visibilitystringRequiredWhich type of organization repositories have access to the organization secret.selectedmeans only the repositories specified byselected_repository_idscan access the secret.Can be one of:all,private,selected |
| selected_repository_idsarray of integersAn array of repository IDs that can access the organization secret. You can only provide a list of repository IDs when thevisibilityis set toselected. You can manage the list of selected repositories using theList selected repositories for an organization secret,Set selected repositories for an organization secret, andRemove selected repository from an organization secretendpoints. |

### HTTP response status codes for "Create or update an organization secret"

| Status code | Description |
| --- | --- |
| 201 | Response when creating a secret |
| 204 | Response when updating a secret |
| 404 | Resource not found |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Create or update an organization secret"

#### Request examples

Select the example typeExample 1: Status Code 201 (application/json)Example 2: Status Code 204 (undefined)put/orgs/{org}/codespaces/secrets/{secret_name}

-
-
-

`curl -L \
  -X PUT \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/codespaces/secrets/SECRET_NAME \
  -d '{"encrypted_value":"c2VjcmV0","key_id":"012345678912345678","visibility":"selected","selected_repository_ids":[1296269,1296280]}'`

Response when creating a secret

-
-

`Status: 201`

## Delete an organization secret

Deletes an organization development environment secret using the secret name.

OAuth app tokens and personal access tokens (classic) need the `admin:org` scope to use this endpoint.

### Fine-grained access tokens for "Delete an organization secret"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Organization codespaces secrets" organization permissions (write)

### Parameters for "Delete an organization secret"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| secret_namestringRequiredThe name of the secret. |

### HTTP response status codes for "Delete an organization secret"

| Status code | Description |
| --- | --- |
| 204 | No Content |
| 404 | Resource not found |

### Code samples for "Delete an organization secret"

#### Request example

delete/orgs/{org}/codespaces/secrets/{secret_name}

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/codespaces/secrets/SECRET_NAME`

Response

`Status: 204`

## List selected repositories for an organization secret

Lists all repositories that have been selected when the `visibility`
for repository access to a secret is set to `selected`.

OAuth app tokens and personal access tokens (classic) need the `admin:org` scope to use this endpoint.

### Fine-grained access tokens for "List selected repositories for an organization secret"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Organization codespaces secrets" organization permissions (read)

### Parameters for "List selected repositories for an organization secret"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| secret_namestringRequiredThe name of the secret. |

| Name, Type, Description |
| --- |
| pageintegerThe page number of the results to fetch. For more information, see "Using pagination in the REST API."Default:1 |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |

### HTTP response status codes for "List selected repositories for an organization secret"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |

### Code samples for "List selected repositories for an organization secret"

#### Request example

get/orgs/{org}/codespaces/secrets/{secret_name}/repositories

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/codespaces/secrets/SECRET_NAME/repositories`

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

## Set selected repositories for an organization secret

Replaces all repositories for an organization development environment secret when the `visibility`
for repository access is set to `selected`. The visibility is set when you [Create
or update an organization secret](https://docs.github.com/rest/codespaces/organization-secrets#create-or-update-an-organization-secret).

OAuth app tokens and personal access tokens (classic) need the `admin:org` scope to use this endpoint.

### Fine-grained access tokens for "Set selected repositories for an organization secret"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Organization codespaces secrets" organization permissions (write)

### Parameters for "Set selected repositories for an organization secret"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| secret_namestringRequiredThe name of the secret. |

| Name, Type, Description |
| --- |
| selected_repository_idsarray of integersRequiredAn array of repository ids that can access the organization secret. You can only provide a list of repository ids when thevisibilityis set toselected. You can add and remove individual repositories using theSet selected repositories for an organization secretandRemove selected repository from an organization secretendpoints. |

### HTTP response status codes for "Set selected repositories for an organization secret"

| Status code | Description |
| --- | --- |
| 204 | No Content |
| 404 | Resource not found |
| 409 | Conflict when visibility type not set to selected |

### Code samples for "Set selected repositories for an organization secret"

#### Request example

put/orgs/{org}/codespaces/secrets/{secret_name}/repositories

-
-
-

`curl -L \
  -X PUT \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/codespaces/secrets/SECRET_NAME/repositories \
  -d '{"selected_repository_ids":[64780797]}'`

Response

`Status: 204`

## Add selected repository to an organization secret

Adds a repository to an organization development environment secret when the `visibility` for repository access is set to `selected`. The visibility is set when you [Create or update an organization secret](https://docs.github.com/rest/codespaces/organization-secrets#create-or-update-an-organization-secret).
OAuth app tokens and personal access tokens (classic) need the `admin:org` scope to use this endpoint.

### Fine-grained access tokens for "Add selected repository to an organization secret"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Organization codespaces secrets" organization permissions (write) and "Metadata" repository permissions (read)

### Parameters for "Add selected repository to an organization secret"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| secret_namestringRequiredThe name of the secret. |
| repository_idintegerRequired |

### HTTP response status codes for "Add selected repository to an organization secret"

| Status code | Description |
| --- | --- |
| 204 | No Content when repository was added to the selected list |
| 404 | Resource not found |
| 409 | Conflict when visibility type is not set to selected |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Add selected repository to an organization secret"

#### Request example

put/orgs/{org}/codespaces/secrets/{secret_name}/repositories/{repository_id}

-
-
-

`curl -L \
  -X PUT \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/codespaces/secrets/SECRET_NAME/repositories/REPOSITORY_ID`

No Content when repository was added to the selected list

`Status: 204`

## Remove selected repository from an organization secret

Removes a repository from an organization development environment secret when the `visibility`
for repository access is set to `selected`. The visibility is set when you [Create
or update an organization secret](https://docs.github.com/rest/codespaces/organization-secrets#create-or-update-an-organization-secret).

OAuth app tokens and personal access tokens (classic) need the `admin:org` scope to use this endpoint.

### Fine-grained access tokens for "Remove selected repository from an organization secret"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Organization codespaces secrets" organization permissions (write) and "Metadata" repository permissions (read)

### Parameters for "Remove selected repository from an organization secret"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| secret_namestringRequiredThe name of the secret. |
| repository_idintegerRequired |

### HTTP response status codes for "Remove selected repository from an organization secret"

| Status code | Description |
| --- | --- |
| 204 | Response when repository was removed from the selected list |
| 404 | Resource not found |
| 409 | Conflict when visibility type not set to selected |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Remove selected repository from an organization secret"

#### Request example

delete/orgs/{org}/codespaces/secrets/{secret_name}/repositories/{repository_id}

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/codespaces/secrets/SECRET_NAME/repositories/REPOSITORY_ID`

Response when repository was removed from the selected list

`Status: 204`

---

# REST API endpoints for Codespaces organizations

> Use the REST API to manage your organization members codespaces.

## About Codespaces organizations

You can manage Codespaces that are billed to your
organization. For more information,
see [Codespaces documentation](https://docs.github.com/en/codespaces).

---

# REST API endpoints for Codespaces repository secrets

> Use the REST API to manage secrets for repositories that the user has access to in a codespace.

## About Codespaces repository secrets

You can create, list, and delete secrets (such as access tokens for cloud services) for repositories that the user has access to. These secrets are made available to the codespace at runtime. For more information, see [Managing your account-specific secrets for GitHub Codespaces](https://docs.github.com/en/codespaces/managing-your-codespaces/managing-your-account-specific-secrets-for-github-codespaces).

---

# REST API endpoints for Codespaces user secrets

> Use the REST API manage secrets that the user has access to in a codespace.

## About Codespaces user secrets

You can create, list, and delete secrets (such as access tokens for cloud services) as well as assign secrets to repositories that the user has access to. These secrets are made available to the codespace at runtime. For more information, see [Managing your account-specific secrets for GitHub Codespaces](https://docs.github.com/en/codespaces/managing-your-codespaces/managing-your-account-specific-secrets-for-github-codespaces).
