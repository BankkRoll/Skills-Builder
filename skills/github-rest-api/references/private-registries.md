# Organization configurations

# Organization configurations

> Use the REST API to manage private registry configurations for organizations.

## List private registries for an organization

Lists all private registry configurations available at the organization-level without revealing their encrypted
values.

OAuth app tokens and personal access tokens (classic) need the `admin:org` scope to use this endpoint.

### Fine-grained access tokens for "List private registries for an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Organization private registries" organization permissions (read)

### Parameters for "List private registries for an organization"

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

### HTTP response status codes for "List private registries for an organization"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 400 | Bad Request |
| 404 | Resource not found |

### Code samples for "List private registries for an organization"

#### Request example

get/orgs/{org}/private-registries

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/private-registries`

Response

-
-

`Status: 200``{
"total_count": 1,
"configurations": [
{
"name": "MAVEN_REPOSITORY_SECRET",
"registry_type": "maven_repository",
"username": "monalisa",
"created_at": "2019-08-10T14:59:22Z",
"updated_at": "2020-01-10T14:59:22Z",
"visibility": "selected"
}
]
}`

## Create a private registry for an organization

Creates a private registry configuration with an encrypted value for an organization. Encrypt your secret using [LibSodium](https://libsodium.gitbook.io/doc/bindings_for_other_languages). For more information, see "[Encrypting secrets for the REST API](https://docs.github.com/rest/guides/encrypting-secrets-for-the-rest-api)."

OAuth app tokens and personal access tokens (classic) need the `admin:org` scope to use this endpoint.

### Fine-grained access tokens for "Create a private registry for an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Organization private registries" organization permissions (write)

### Parameters for "Create a private registry for an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| registry_typestringRequiredThe registry type.Can be one of:maven_repository,nuget_feed,goproxy_server,npm_registry,rubygems_server,cargo_registry,composer_repository,docker_registry,git_source,helm_registry,hex_organization,hex_repository,pub_repository,python_index,terraform_registry |
| urlstringRequiredThe URL of the private registry. |
| usernamestring or nullThe username to use when authenticating with the private registry. This field should be omitted if the private registry does not require a username for authentication. |
| replaces_basebooleanWhether this private registry should replace the base registry (e.g., npmjs.org for npm, rubygems.org for rubygems). When set totrue, Dependabot will only use this registry and will not fall back to the public registry. When set tofalse(default), Dependabot will use this registry for scoped packages but may fall back to the public registry for other packages.Default:false |
| encrypted_valuestringRequiredThe value for your secret, encrypted withLibSodiumusing the public key retrieved from theGet private registries public key for an organizationendpoint. |
| key_idstringRequiredThe ID of the key you used to encrypt the secret. |
| visibilitystringRequiredWhich type of organization repositories have access to the private registry.selectedmeans only the repositories specified byselected_repository_idscan access the private registry.Can be one of:all,private,selected |
| selected_repository_idsarray of integersAn array of repository IDs that can access the organization private registry. You can only provide a list of repository IDs whenvisibilityis set toselected. You can manage the list of selected repositories using theUpdate a private registry for an organizationendpoint. This field should be omitted ifvisibilityis set toallorprivate. |

### HTTP response status codes for "Create a private registry for an organization"

| Status code | Description |
| --- | --- |
| 201 | The organization private registry configuration |
| 404 | Resource not found |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Create a private registry for an organization"

#### Request examples

Select the example typeExample of a private registry configuration with private visibilityExample of a private registry configuration with selected visibilitypost/orgs/{org}/private-registries

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/private-registries \
  -d '{"registry_type":"maven_repository","url":"https://maven.pkg.github.com/organization/","username":"monalisa","replaces_base":true,"encrypted_value":"c2VjcmV0","key_id":"012345678912345678","visibility":"private"}'`

The organization private registry configuration

-
-

`Status: 201``{
"name": "MAVEN_REPOSITORY_SECRET",
"registry_type": "maven_repository",
"username": "monalisa",
"visibility": "selected",
"selected_repository_ids": [
1296269,
1296280
],
"created_at": "2019-08-10T14:59:22Z",
"updated_at": "2020-01-10T14:59:22Z"
}`

## Get private registries public key for an organization

Gets the org public key, which is needed to encrypt private registry secrets. You need to encrypt a secret before you can create or update secrets.

OAuth tokens and personal access tokens (classic) need the `admin:org` scope to use this endpoint.

### Fine-grained access tokens for "Get private registries public key for an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Organization private registries" organization permissions (read)

### Parameters for "Get private registries public key for an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

### HTTP response status codes for "Get private registries public key for an organization"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |

### Code samples for "Get private registries public key for an organization"

#### Request example

get/orgs/{org}/private-registries/public-key

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/private-registries/public-key`

Response

-
-

`Status: 200``{
"key_id": "012345678912345678",
"key": "2Sg8iYjAxxmI2LvUXpJjkYrMxURPc8r+dB7TJyvv1234"
}`

## Get a private registry for an organization

Get the configuration of a single private registry defined for an organization, omitting its encrypted value.

OAuth app tokens and personal access tokens (classic) need the `admin:org` scope to use this endpoint.

### Fine-grained access tokens for "Get a private registry for an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Organization private registries" organization permissions (read)

### Parameters for "Get a private registry for an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| secret_namestringRequiredThe name of the secret. |

### HTTP response status codes for "Get a private registry for an organization"

| Status code | Description |
| --- | --- |
| 200 | The specified private registry configuration for the organization |
| 404 | Resource not found |

### Code samples for "Get a private registry for an organization"

#### Request example

get/orgs/{org}/private-registries/{secret_name}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/private-registries/SECRET_NAME`

The specified private registry configuration for the organization

-
-

`Status: 200``{
"name": "MAVEN_REPOSITORY_SECRET",
"registry_type": "maven_repository",
"username": "monalisa",
"visibility": "private",
"created_at": "2019-08-10T14:59:22Z",
"updated_at": "2020-01-10T14:59:22Z"
}`

## Update a private registry for an organization

Updates a private registry configuration with an encrypted value for an organization. Encrypt your secret using [LibSodium](https://libsodium.gitbook.io/doc/bindings_for_other_languages). For more information, see "[Encrypting secrets for the REST API](https://docs.github.com/rest/guides/encrypting-secrets-for-the-rest-api)."

OAuth app tokens and personal access tokens (classic) need the `admin:org` scope to use this endpoint.

### Fine-grained access tokens for "Update a private registry for an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Organization private registries" organization permissions (write)

### Parameters for "Update a private registry for an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| secret_namestringRequiredThe name of the secret. |

| Name, Type, Description |
| --- |
| registry_typestringThe registry type.Can be one of:maven_repository,nuget_feed,goproxy_server,npm_registry,rubygems_server,cargo_registry,composer_repository,docker_registry,git_source,helm_registry,hex_organization,hex_repository,pub_repository,python_index,terraform_registry |
| urlstringThe URL of the private registry. |
| usernamestring or nullThe username to use when authenticating with the private registry. This field should be omitted if the private registry does not require a username for authentication. |
| replaces_basebooleanWhether this private registry should replace the base registry (e.g., npmjs.org for npm, rubygems.org for rubygems). When set totrue, Dependabot will only use this registry and will not fall back to the public registry. When set tofalse(default), Dependabot will use this registry for scoped packages but may fall back to the public registry for other packages.Default:false |
| encrypted_valuestringThe value for your secret, encrypted withLibSodiumusing the public key retrieved from theGet private registries public key for an organizationendpoint. |
| key_idstringThe ID of the key you used to encrypt the secret. |
| visibilitystringWhich type of organization repositories have access to the private registry.selectedmeans only the repositories specified byselected_repository_idscan access the private registry.Can be one of:all,private,selected |
| selected_repository_idsarray of integersAn array of repository IDs that can access the organization private registry. You can only provide a list of repository IDs whenvisibilityis set toselected. This field should be omitted ifvisibilityis set toallorprivate. |

### HTTP response status codes for "Update a private registry for an organization"

| Status code | Description |
| --- | --- |
| 204 | No Content |
| 404 | Resource not found |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Update a private registry for an organization"

#### Request example

patch/orgs/{org}/private-registries/{secret_name}

-
-
-

`curl -L \
  -X PATCH \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/private-registries/SECRET_NAME \
  -d '{"username":"monalisa","encrypted_value":"c2VjcmV0","key_id":"012345678912345678"}'`

Response

`Status: 204`

## Delete a private registry for an organization

Delete a private registry configuration at the organization-level.

OAuth app tokens and personal access tokens (classic) need the `admin:org` scope to use this endpoint.

### Fine-grained access tokens for "Delete a private registry for an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Organization private registries" organization permissions (write)

### Parameters for "Delete a private registry for an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| secret_namestringRequiredThe name of the secret. |

### HTTP response status codes for "Delete a private registry for an organization"

| Status code | Description |
| --- | --- |
| 204 | No Content |
| 400 | Bad Request |
| 404 | Resource not found |

### Code samples for "Delete a private registry for an organization"

#### Request example

delete/orgs/{org}/private-registries/{secret_name}

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/private-registries/SECRET_NAME`

Response

`Status: 204`
