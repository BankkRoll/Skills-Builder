# REST API endpoints for GitHub Actions artifacts and more

# REST API endpoints for GitHub Actions artifacts

> Use the REST API to interact with artifacts in GitHub Actions.

## About artifacts in GitHub Actions

You can use the REST API to download, delete, and retrieve information about workflow artifacts in GitHub Actions. Artifacts enable you to share data between jobs in a workflow and store data once that workflow has completed. For more information, see [Store and share data with workflow artifacts](https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts).

---

# REST API endpoints for GitHub Actions cache

> Use the REST API to interact with the cache for repositories in GitHub Actions.

## About the cache in GitHub Actions

You can use the REST API to query and manage the cache for repositories in GitHub Actions. You can also install a GitHub CLI extension to manage your caches from the command line. For more information, see [Dependency caching reference](https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows#managing-caches).

---

# GitHub

> Use the REST API to interact with GitHub-hosted runners in GitHub Actions.

## List GitHub-hosted runners for an organization

Lists all GitHub-hosted runners configured in an organization.

OAuth app tokens and personal access tokens (classic) need the `manage_runner:org` scope to use this endpoint.

### Fine-grained access tokens for "List GitHub-hosted runners for an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" organization permissions (read)

### Parameters for "List GitHub-hosted runners for an organization"

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

### HTTP response status codes for "List GitHub-hosted runners for an organization"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "List GitHub-hosted runners for an organization"

#### Request example

get/orgs/{org}/actions/hosted-runners

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/actions/hosted-runners`

Response

-
-

`Status: 200``{
"total_count": 2,
"runners": [
{
"id": 5,
"name": "My hosted ubuntu runner",
"runner_group_id": 2,
"platform": "linux-x64",
"image": {
"id": "ubuntu-20.04",
"size": 86
},
"machine_size_details": {
"id": "4-core",
"cpu_cores": 4,
"memory_gb": 16,
"storage_gb": 150
},
"status": "Ready",
"maximum_runners": 10,
"public_ip_enabled": true,
"public_ips": [
{
"enabled": true,
"prefix": "20.80.208.150",
"length": 31
}
],
"last_active_on": "2022-10-09T23:39:01Z"
},
{
"id": 7,
"name": "My hosted Windows runner",
"runner_group_id": 2,
"platform": "win-x64",
"image": {
"id": "windows-latest",
"size": 256
},
"machine_size_details": {
"id": "8-core",
"cpu_cores": 8,
"memory_gb": 32,
"storage_gb": 300
},
"status": "Ready",
"maximum_runners": 20,
"public_ip_enabled": false,
"public_ips": [],
"last_active_on": "2023-04-26T15:23:37Z"
}
]
}`

## Create a GitHub-hosted runner for an organization

Creates a GitHub-hosted runner for an organization.
OAuth tokens and personal access tokens (classic) need the `manage_runners:org` scope to use this endpoint.

### Fine-grained access tokens for "Create a GitHub-hosted runner for an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" organization permissions (write)

### Parameters for "Create a GitHub-hosted runner for an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| namestringRequiredName of the runner. Must be between 1 and 64 characters and may only contain upper and lowercase letters a-z, numbers 0-9, '.', '-', and '_'. |
| imageobjectRequiredThe image of runner. To list all available images, useGET /actions/hosted-runners/images/github-ownedorGET /actions/hosted-runners/images/partner. |
| Name, Type, DescriptionidstringThe unique identifier of the runner image.sourcestringThe source of the runner image.Can be one of:github,partner,customversionstring or nullThe version of the runner image to deploy. This is relevant only for runners using custom images. |
| Name, Type, Description |
| idstringThe unique identifier of the runner image. |
| sourcestringThe source of the runner image.Can be one of:github,partner,custom |
| versionstring or nullThe version of the runner image to deploy. This is relevant only for runners using custom images. |
| sizestringRequiredThe machine size of the runner. To list available sizes, useGET actions/hosted-runners/machine-sizes |
| runner_group_idintegerRequiredThe existing runner group to add this runner to. |
| maximum_runnersintegerThe maximum amount of runners to scale up to. Runners will not auto-scale above this number. Use this setting to limit your cost. |
| enable_static_ipbooleanWhether this runner should be created with a static public IP. Note limit on account. To list limits on account, useGET actions/hosted-runners/limits |
| image_genbooleanWhether this runner should be used to generate custom images.Default:false |

### HTTP response status codes for "Create a GitHub-hosted runner for an organization"

| Status code | Description |
| --- | --- |
| 201 | Created |

### Code samples for "Create a GitHub-hosted runner for an organization"

#### Request example

post/orgs/{org}/actions/hosted-runners

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/actions/hosted-runners \
  -d '{"name":"My Hosted runner","image":{"id":"ubuntu-latest","source":"github"},"runner_group_id":1,"size":"4-core","maximum_runners":50,"enable_static_ip":false}'`

Response

-
-

`Status: 201``{
"id": 5,
"name": "My hosted ubuntu runner",
"runner_group_id": 2,
"platform": "linux-x64",
"image": {
"id": "ubuntu-20.04",
"size": 86
},
"machine_size_details": {
"id": "4-core",
"cpu_cores": 4,
"memory_gb": 16,
"storage_gb": 150
},
"status": "Ready",
"maximum_runners": 10,
"public_ip_enabled": true,
"public_ips": [
{
"enabled": true,
"prefix": "20.80.208.150",
"length": 31
}
],
"last_active_on": "2022-10-09T23:39:01Z"
}`

## List custom images for an organization

List custom images for an organization.

OAuth tokens and personal access tokens (classic) need the `manage_runners:org` scope to use this endpoint.

### Fine-grained access tokens for "List custom images for an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Hosted runner custom images" organization permissions (read)

### Parameters for "List custom images for an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

### HTTP response status codes for "List custom images for an organization"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "List custom images for an organization"

#### Request example

get/orgs/{org}/actions/hosted-runners/images/custom

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/actions/hosted-runners/images/custom`

Response

-
-

`Status: 200``{
"total_count": 2,
"image_versions": [
{
"version": "1.1.0",
"size_gb": 75,
"state": "Ready",
"created_on": "2024-11-09T23:39:01Z"
},
{
"version": "1.0.0",
"size_gb": 75,
"state": "Ready",
"created_on": "2024-11-08T20:39:01Z"
}
]
}`

## Get a custom image definition for GitHub Actions Hosted Runners

Get a custom image definition for GitHub Actions Hosted Runners.

OAuth tokens and personal access tokens (classic) need the `manage_runners:org` scope to use this endpoint.

### Fine-grained access tokens for "Get a custom image definition for GitHub Actions Hosted Runners"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Hosted runner custom images" organization permissions (read)

### Parameters for "Get a custom image definition for GitHub Actions Hosted Runners"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| image_definition_idintegerRequiredImage definition ID of custom image |

### HTTP response status codes for "Get a custom image definition for GitHub Actions Hosted Runners"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "Get a custom image definition for GitHub Actions Hosted Runners"

#### Request example

get/orgs/{org}/actions/hosted-runners/images/custom/{image_definition_id}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/actions/hosted-runners/images/custom/IMAGE_DEFINITION_ID`

Response

-
-

`Status: 200``{
"id": 1,
"platform": "linux-x64",
"name": "CustomImage",
"source": "custom",
"versions_count": 4,
"total_versions_size": 200,
"latest_version": "1.3.0",
"state": "Ready"
}`

## Delete a custom image from the organization

Delete a custom image from the organization.

OAuth tokens and personal access tokens (classic) need the `manage_runners:org` scope to use this endpoint.

### Fine-grained access tokens for "Delete a custom image from the organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Hosted runner custom images" organization permissions (write)

### Parameters for "Delete a custom image from the organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| image_definition_idintegerRequiredImage definition ID of custom image |

### HTTP response status codes for "Delete a custom image from the organization"

| Status code | Description |
| --- | --- |
| 204 | No Content |

### Code samples for "Delete a custom image from the organization"

#### Request example

delete/orgs/{org}/actions/hosted-runners/images/custom/{image_definition_id}

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/actions/hosted-runners/images/custom/IMAGE_DEFINITION_ID`

Response

`Status: 204`

## List image versions of a custom image for an organization

List image versions of a custom image for an organization.

OAuth tokens and personal access tokens (classic) need the `manage_runners:org` scope to use this endpoint.

### Fine-grained access tokens for "List image versions of a custom image for an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Hosted runner custom images" organization permissions (read)

### Parameters for "List image versions of a custom image for an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| image_definition_idintegerRequiredImage definition ID of custom image |
| orgstringRequiredThe organization name. The name is not case sensitive. |

### HTTP response status codes for "List image versions of a custom image for an organization"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "List image versions of a custom image for an organization"

#### Request example

get/orgs/{org}/actions/hosted-runners/images/custom/{image_definition_id}/versions

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/actions/hosted-runners/images/custom/IMAGE_DEFINITION_ID/versions`

Response

-
-

`Status: 200``{
"total_count": 2,
"image_versions": [
{
"version": "1.1.0",
"size_gb": 75,
"state": "Ready",
"created_on": "2024-11-09T23:39:01Z"
},
{
"version": "1.0.0",
"size_gb": 75,
"state": "Ready",
"created_on": "2024-11-08T20:39:01Z"
}
]
}`

## Get an image version of a custom image for GitHub Actions Hosted Runners

Get an image version of a custom image for GitHub Actions Hosted Runners.

OAuth tokens and personal access tokens (classic) need the `manage_runners:org` scope to use this endpoint.

### Fine-grained access tokens for "Get an image version of a custom image for GitHub Actions Hosted Runners"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Hosted runner custom images" organization permissions (read)

### Parameters for "Get an image version of a custom image for GitHub Actions Hosted Runners"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| image_definition_idintegerRequiredImage definition ID of custom image |
| versionstringRequiredVersion of a custom image |

### HTTP response status codes for "Get an image version of a custom image for GitHub Actions Hosted Runners"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "Get an image version of a custom image for GitHub Actions Hosted Runners"

#### Request example

get/orgs/{org}/actions/hosted-runners/images/custom/{image_definition_id}/versions/{version}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/actions/hosted-runners/images/custom/IMAGE_DEFINITION_ID/versions/VERSION`

Response

-
-

`Status: 200``{
"version": "1.0.0",
"size_gb": 75,
"state": "Ready",
"created_on": "2024-11-08T20:39:01Z"
}`

## Delete an image version of custom image from the organization

Delete an image version of custom image from the organization.

OAuth tokens and personal access tokens (classic) need the `manage_runners:org` scope to use this endpoint.

### Fine-grained access tokens for "Delete an image version of custom image from the organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Hosted runner custom images" organization permissions (write)

### Parameters for "Delete an image version of custom image from the organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| image_definition_idintegerRequiredImage definition ID of custom image |
| versionstringRequiredVersion of a custom image |

### HTTP response status codes for "Delete an image version of custom image from the organization"

| Status code | Description |
| --- | --- |
| 204 | No Content |

### Code samples for "Delete an image version of custom image from the organization"

#### Request example

delete/orgs/{org}/actions/hosted-runners/images/custom/{image_definition_id}/versions/{version}

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/actions/hosted-runners/images/custom/IMAGE_DEFINITION_ID/versions/VERSION`

Response

`Status: 204`

## Get GitHub-owned images for GitHub-hosted runners in an organization

Get the list of GitHub-owned images available for GitHub-hosted runners for an organization.

### Fine-grained access tokens for "Get GitHub-owned images for GitHub-hosted runners in an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" organization permissions (read)

### Parameters for "Get GitHub-owned images for GitHub-hosted runners in an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

### HTTP response status codes for "Get GitHub-owned images for GitHub-hosted runners in an organization"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "Get GitHub-owned images for GitHub-hosted runners in an organization"

#### Request example

get/orgs/{org}/actions/hosted-runners/images/github-owned

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/actions/hosted-runners/images/github-owned`

Response

-
-

`Status: 200``{
"id": "ubuntu-20.04",
"platform": "linux-x64",
"size_gb": 86,
"display_name": "20.04",
"source": "github"
}`

## Get partner images for GitHub-hosted runners in an organization

Get the list of partner images available for GitHub-hosted runners for an organization.

### Fine-grained access tokens for "Get partner images for GitHub-hosted runners in an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" organization permissions (read)

### Parameters for "Get partner images for GitHub-hosted runners in an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

### HTTP response status codes for "Get partner images for GitHub-hosted runners in an organization"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "Get partner images for GitHub-hosted runners in an organization"

#### Request example

get/orgs/{org}/actions/hosted-runners/images/partner

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/actions/hosted-runners/images/partner`

Response

-
-

`Status: 200``{
"id": "ubuntu-20.04",
"platform": "linux-x64",
"size_gb": 86,
"display_name": "20.04",
"source": "github"
}`

## Get limits on GitHub-hosted runners for an organization

Get the GitHub-hosted runners limits for an organization.

### Fine-grained access tokens for "Get limits on GitHub-hosted runners for an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" organization permissions (read)

### Parameters for "Get limits on GitHub-hosted runners for an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

### HTTP response status codes for "Get limits on GitHub-hosted runners for an organization"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "Get limits on GitHub-hosted runners for an organization"

#### Request example

get/orgs/{org}/actions/hosted-runners/limits

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/actions/hosted-runners/limits`

Response

-
-

`Status: 200``{
"public_ips": {
"current_usage": 17,
"maximum": 50
}
}`

## Get GitHub-hosted runners machine specs for an organization

Get the list of machine specs available for GitHub-hosted runners for an organization.

### Fine-grained access tokens for "Get GitHub-hosted runners machine specs for an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" organization permissions (read)

### Parameters for "Get GitHub-hosted runners machine specs for an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

### HTTP response status codes for "Get GitHub-hosted runners machine specs for an organization"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "Get GitHub-hosted runners machine specs for an organization"

#### Request example

get/orgs/{org}/actions/hosted-runners/machine-sizes

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/actions/hosted-runners/machine-sizes`

Response

-
-

`Status: 200``{
"id": "4-core",
"cpu_cores": 4,
"memory_gb": 16,
"storage_gb": 150
}`

## Get platforms for GitHub-hosted runners in an organization

Get the list of platforms available for GitHub-hosted runners for an organization.

### Fine-grained access tokens for "Get platforms for GitHub-hosted runners in an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" organization permissions (read)

### Parameters for "Get platforms for GitHub-hosted runners in an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

### HTTP response status codes for "Get platforms for GitHub-hosted runners in an organization"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "Get platforms for GitHub-hosted runners in an organization"

#### Request example

get/orgs/{org}/actions/hosted-runners/platforms

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/actions/hosted-runners/platforms`

Response

-
-

`Status: 200``{
"total_count": 1,
"platforms": [
"linux-x64",
"win-x64"
]
}`

## Get a GitHub-hosted runner for an organization

Gets a GitHub-hosted runner configured in an organization.

OAuth app tokens and personal access tokens (classic) need the `manage_runners:org` scope to use this endpoint.

### Fine-grained access tokens for "Get a GitHub-hosted runner for an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" organization permissions (read)

### Parameters for "Get a GitHub-hosted runner for an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| hosted_runner_idintegerRequiredUnique identifier of the GitHub-hosted runner. |

### HTTP response status codes for "Get a GitHub-hosted runner for an organization"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "Get a GitHub-hosted runner for an organization"

#### Request example

get/orgs/{org}/actions/hosted-runners/{hosted_runner_id}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/actions/hosted-runners/HOSTED_RUNNER_ID`

Response

-
-

`Status: 200``{
"id": 5,
"name": "My hosted ubuntu runner",
"runner_group_id": 2,
"platform": "linux-x64",
"image": {
"id": "ubuntu-20.04",
"size": 86
},
"machine_size_details": {
"id": "4-core",
"cpu_cores": 4,
"memory_gb": 16,
"storage_gb": 150
},
"status": "Ready",
"maximum_runners": 10,
"public_ip_enabled": true,
"public_ips": [
{
"enabled": true,
"prefix": "20.80.208.150",
"length": 31
}
],
"last_active_on": "2022-10-09T23:39:01Z"
}`

## Update a GitHub-hosted runner for an organization

Updates a GitHub-hosted runner for an organization.
OAuth app tokens and personal access tokens (classic) need the `manage_runners:org` scope to use this endpoint.

### Fine-grained access tokens for "Update a GitHub-hosted runner for an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" organization permissions (write)

### Parameters for "Update a GitHub-hosted runner for an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| hosted_runner_idintegerRequiredUnique identifier of the GitHub-hosted runner. |

| Name, Type, Description |
| --- |
| namestringName of the runner. Must be between 1 and 64 characters and may only contain upper and lowercase letters a-z, numbers 0-9, '.', '-', and '_'. |
| runner_group_idintegerThe existing runner group to add this runner to. |
| maximum_runnersintegerThe maximum amount of runners to scale up to. Runners will not auto-scale above this number. Use this setting to limit your cost. |
| enable_static_ipbooleanWhether this runner should be updated with a static public IP. Note limit on account. To list limits on account, useGET actions/hosted-runners/limits |
| sizestringThe machine size of the runner. To list available sizes, useGET actions/hosted-runners/machine-sizes |
| image_idstringThe unique identifier of the runner image. To list all available images, useGET /actions/hosted-runners/images/github-ownedorGET /actions/hosted-runners/images/partner. |
| image_versionstring or nullThe version of the runner image to deploy. This is relevant only for runners using custom images. |

### HTTP response status codes for "Update a GitHub-hosted runner for an organization"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "Update a GitHub-hosted runner for an organization"

#### Request example

patch/orgs/{org}/actions/hosted-runners/{hosted_runner_id}

-
-
-

`curl -L \
  -X PATCH \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/actions/hosted-runners/HOSTED_RUNNER_ID \
  -d '{"name":"My larger runner","runner_group_id":1,"maximum_runners":50,"enable_static_ip":false}'`

Response

-
-

`Status: 200``{
"id": 5,
"name": "My hosted ubuntu runner",
"runner_group_id": 2,
"platform": "linux-x64",
"image": {
"id": "ubuntu-20.04",
"size": 86
},
"machine_size_details": {
"id": "4-core",
"cpu_cores": 4,
"memory_gb": 16,
"storage_gb": 150
},
"status": "Ready",
"maximum_runners": 10,
"public_ip_enabled": true,
"public_ips": [
{
"enabled": true,
"prefix": "20.80.208.150",
"length": 31
}
],
"last_active_on": "2022-10-09T23:39:01Z"
}`

## Delete a GitHub-hosted runner for an organization

Deletes a GitHub-hosted runner for an organization.

### Fine-grained access tokens for "Delete a GitHub-hosted runner for an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" organization permissions (write)

### Parameters for "Delete a GitHub-hosted runner for an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| hosted_runner_idintegerRequiredUnique identifier of the GitHub-hosted runner. |

### HTTP response status codes for "Delete a GitHub-hosted runner for an organization"

| Status code | Description |
| --- | --- |
| 202 | Accepted |

### Code samples for "Delete a GitHub-hosted runner for an organization"

#### Request example

delete/orgs/{org}/actions/hosted-runners/{hosted_runner_id}

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/actions/hosted-runners/HOSTED_RUNNER_ID`

Response

-
-

`Status: 202``{
"id": 5,
"name": "My hosted ubuntu runner",
"runner_group_id": 2,
"platform": "linux-x64",
"image": {
"id": "ubuntu-20.04",
"size": 86
},
"machine_size_details": {
"id": "4-core",
"cpu_cores": 4,
"memory_gb": 16,
"storage_gb": 150
},
"status": "Ready",
"maximum_runners": 10,
"public_ip_enabled": true,
"public_ips": [
{
"enabled": true,
"prefix": "20.80.208.150",
"length": 31
}
],
"last_active_on": "2022-10-09T23:39:01Z"
}`

---

# REST API endpoints for GitHub Actions OIDC

> Use the REST API to interact with JWTs for OIDC subject claims in GitHub Actions.

## About GitHub Actions OIDC

You can use the REST API to query and manage a customization template for an OpenID Connect (OIDC) subject claim. For more information, see [OpenID Connect](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect).

---

# REST API endpoints for GitHub Actions permissions

> Use the REST API to interact with permissions for GitHub Actions.

## About permissions for GitHub Actions

You can use the REST API to set permissions for the organizations and repositories that are allowed to run GitHub Actions, and the actions and reusable workflows that are allowed to run. For more information, see [Billing and usage](https://docs.github.com/en/actions/learn-github-actions/usage-limits-billing-and-administration#disabling-or-limiting-github-actions-for-your-repository-or-organization).

---

# REST API endpoints for GitHub Actions Secrets

> Use the REST API to interact with secrets in GitHub Actions.

## About secrets in GitHub Actions

You can use the REST API to create, update, delete, and retrieve information about secrets that can be used in workflows in GitHub Actions. Secrets allow you to store sensitive information, such as access tokens, in your repository, repository environments, or organization. For more information, see [Secrets](https://docs.github.com/en/actions/security-for-github-actions/security-guides/about-secrets).

---

# REST API endpoints for self

> Use the REST API to interact with self-hosted runner groups for GitHub Actions.

## About self-hosted runner groups in GitHub Actions

You can use the REST API to manage groups of self-hosted runners in GitHub Actions. For more information, see [Managing access to self-hosted runners using groups](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/managing-access-to-self-hosted-runners-using-groups).

These endpoints are available for authenticated users, OAuth apps, and GitHub Apps. Access tokens require [reposcope](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/scopes-for-oauth-apps#available-scopes) for private repositories and [public_reposcope](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/scopes-for-oauth-apps#available-scopes) for public repositories. GitHub Apps must have the `administration` permission for repositories or the `organization_self_hosted_runners` permission for organizations. Authenticated users must have admin access to repositories or organizations, or the `manage_runners:enterprise` scope for enterprises to use these endpoints.

---

# REST API endpoints for self

> Use the REST API to interact with self-hosted runners in GitHub Actions.

## About self-hosted runners in GitHub Actions

You can use the REST API to register, view, and delete self-hosted runners in GitHub Actions. Self-hosted runners allow you to host your own runners and customize the environment used to run jobs in your GitHub Actions workflows. For more information, see [Managing self-hosted runners](https://docs.github.com/en/actions/how-tos/managing-self-hosted-runners).

---

# REST API endpoints for GitHub Actions variables

> Use the REST API to interact with variables in GitHub Actions.

## About variables in GitHub Actions

You can use the REST API to create, update, delete, and retrieve information about variables that can be used in workflows in GitHub Actions. Variables allow you to store non-sensitive information, such as a username, in your repository, repository environments, or organization. For more information, see [Store information in variables](https://docs.github.com/en/actions/learn-github-actions/variables) in the GitHub Actions documentation.

---

# REST API endpoints for workflow jobs

> Use the REST API to interact with workflow jobs in GitHub Actions.

## About workflow jobs in GitHub Actions

You can use the REST API to view logs and workflow jobs in GitHub Actions. A workflow job is a set of steps that execute on the same runner. For more information, see [Workflow syntax for GitHub Actions](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions).

---

# REST API endpoints for workflow runs

> Use the REST API to interact with workflow runs in GitHub Actions.

## About workflow runs in GitHub Actions

You can use the REST API to view, re-run, cancel, and view logs for workflow runs in GitHub Actions. A workflow run is an instance of your workflow that runs when the pre-configured event occurs. For more information, see [Managing workflow runs](https://docs.github.com/en/actions/managing-workflow-runs).

---

# REST API endpoints for workflows

> Use the REST API to interact with workflows in GitHub Actions.

## About workflows in GitHub Actions

You can use the REST API to view workflows for a repository in GitHub Actions. Workflows automate your software development life cycle with a wide range of tools and services. For more information, see [Workflows](https://docs.github.com/en/actions/using-workflows/about-workflows) in the GitHub Actions documentation.
