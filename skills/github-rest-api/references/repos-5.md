# REST API endpoints for repository tags and more

# REST API endpoints for repository tags

> Use the REST API to manage tags for a repository.

## Closing down - List tag protection states for a repository

Warning

**Closing down notice:** This operation is closing down and will be removed after August 30, 2024. Use the "[Repository Rulesets](https://docs.github.com/rest/repos/rules#get-all-repository-rulesets)" endpoint instead.

This returns the tag protection states of a repository.

This information is only available to repository administrators.

### Fine-grained access tokens for "Closing down - List tag protection states for a repository"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (read)

### Parameters for "Closing down - List tag protection states for a repository"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

### HTTP response status codes for "Closing down - List tag protection states for a repository"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 403 | Forbidden |
| 404 | Resource not found |

### Code samples for "Closing down - List tag protection states for a repository"

#### Request example

get/repos/{owner}/{repo}/tags/protection

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/tags/protection`

Response

-
-

`Status: 200``[
{
"id": 2,
"pattern": "v1.*"
}
]`

## Closing down - Create a tag protection state for a repository

Warning

**Closing down notice:** This operation is closing down and will be removed after August 30, 2024. Use the "[Repository Rulesets](https://docs.github.com/rest/repos/rules#create-a-repository-ruleset)" endpoint instead.

This creates a tag protection state for a repository.
This endpoint is only available to repository administrators.

### Fine-grained access tokens for "Closing down - Create a tag protection state for a repository"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Closing down - Create a tag protection state for a repository"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| patternstringRequiredAn optional glob pattern to match against when enforcing tag protection. |

### HTTP response status codes for "Closing down - Create a tag protection state for a repository"

| Status code | Description |
| --- | --- |
| 201 | Created |
| 403 | Forbidden |
| 404 | Resource not found |

### Code samples for "Closing down - Create a tag protection state for a repository"

#### Request example

post/repos/{owner}/{repo}/tags/protection

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/tags/protection \
  -d '{"pattern":"v1.*"}'`

Response

-
-

`Status: 201``{
"enabled": true
}`

## Closing down - Delete a tag protection state for a repository

Warning

**Closing down notice:** This operation is closing down and will be removed after August 30, 2024. Use the "[Repository Rulesets](https://docs.github.com/rest/repos/rules#delete-a-repository-ruleset)" endpoint instead.

This deletes a tag protection state for a repository.
This endpoint is only available to repository administrators.

### Fine-grained access tokens for "Closing down - Delete a tag protection state for a repository"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Closing down - Delete a tag protection state for a repository"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| tag_protection_idintegerRequiredThe unique identifier of the tag protection. |

### HTTP response status codes for "Closing down - Delete a tag protection state for a repository"

| Status code | Description |
| --- | --- |
| 204 | No Content |
| 403 | Forbidden |
| 404 | Resource not found |

### Code samples for "Closing down - Delete a tag protection state for a repository"

#### Request example

delete/repos/{owner}/{repo}/tags/protection/{tag_protection_id}

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/tags/protection/TAG_PROTECTION_ID`

Response

`Status: 204`

---

# REST API endpoints for repository webhooks

> Use the REST API to create and manage webhooks for your repositories.

## About repository webhooks

Repository webhooks allow your server to receive HTTP `POST` payloads whenever certain events happen in a repository. For more information, see [Webhooks documentation](https://docs.github.com/en/webhooks).
