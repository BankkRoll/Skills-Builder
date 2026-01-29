# REST API endpoints for secret scanning push protection and more

# REST API endpoints for secret scanning push protection

> Use the REST API to manage secret scanning push protection.

## List organization pattern configurations

Lists the secret scanning pattern configurations for an organization.

Personal access tokens (classic) need the `read:org` scope to use this endpoint.

### Fine-grained access tokens for "List organization pattern configurations"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" organization permissions (read)

### Parameters for "List organization pattern configurations"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

### HTTP response status codes for "List organization pattern configurations"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 403 | Forbidden |
| 404 | Resource not found |

### Code samples for "List organization pattern configurations"

#### Request example

get/orgs/{org}/secret-scanning/pattern-configurations

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/secret-scanning/pattern-configurations`

Response

-
-

`Status: 200``{
"pattern_config_version": "0ujsswThIGTUYm2K8FjOOfXtY1K",
"provider_pattern_overrides": [
{
"token_type": "GITHUB_PERSONAL_ACCESS_TOKEN",
"slug": "github_personal_access_token_legacy_v2",
"display_name": "GitHub Personal Access Token (Legacy v2)",
"alert_total": 15,
"alert_total_percentage": 36,
"false_positives": 2,
"false_positive_rate": 13,
"bypass_rate": 13,
"default_setting": "enabled",
"setting": "enabled",
"enterprise_setting": "enabled"
}
],
"custom_pattern_overrides": [
{
"token_type": "cp_2",
"custom_pattern_version": "0ujsswThIGTUYm2K8FjOOfXtY1K",
"slug": "custom-api-key",
"display_name": "Custom API Key",
"alert_total": 15,
"alert_total_percentage": 36,
"false_positives": 3,
"false_positive_rate": 20,
"bypass_rate": 20,
"default_setting": "disabled",
"setting": "enabled"
}
]
}`

## Update organization pattern configurations

Updates the secret scanning pattern configurations for an organization.

Personal access tokens (classic) need the `write:org` scope to use this endpoint.

### Fine-grained access tokens for "Update organization pattern configurations"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" organization permissions (write)

### Parameters for "Update organization pattern configurations"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| pattern_config_versionstring or nullThe version of the entity. This is used to confirm you're updating the current version of the entity and mitigate unintentionally overriding someone else's update. |
| provider_pattern_settingsarray of objectsPattern settings for provider patterns. |
| Name, Type, Descriptiontoken_typestringThe ID of the pattern to configure.push_protection_settingstringPush protection setting to set for the pattern.Can be one of:not-set,disabled,enabled |
| Name, Type, Description |
| token_typestringThe ID of the pattern to configure. |
| push_protection_settingstringPush protection setting to set for the pattern.Can be one of:not-set,disabled,enabled |
| custom_pattern_settingsarray of objectsPattern settings for custom patterns. |
| Name, Type, Descriptiontoken_typestringThe ID of the pattern to configure.custom_pattern_versionstring or nullThe version of the entity. This is used to confirm you're updating the current version of the entity and mitigate unintentionally overriding someone else's update.push_protection_settingstringPush protection setting to set for the pattern.Can be one of:disabled,enabled |
| Name, Type, Description |
| token_typestringThe ID of the pattern to configure. |
| custom_pattern_versionstring or nullThe version of the entity. This is used to confirm you're updating the current version of the entity and mitigate unintentionally overriding someone else's update. |
| push_protection_settingstringPush protection setting to set for the pattern.Can be one of:disabled,enabled |

### HTTP response status codes for "Update organization pattern configurations"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 400 | Bad Request |
| 403 | Forbidden |
| 404 | Resource not found |
| 409 | Conflict |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Update organization pattern configurations"

#### Request example

patch/orgs/{org}/secret-scanning/pattern-configurations

-
-
-

`curl -L \
  -X PATCH \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/secret-scanning/pattern-configurations \
  -d '{"pattern_config_version":"0ujsswThIGTUYm2K8FjOOfXtY1K","provider_pattern_settings":[{"token_type":"GITHUB_PERSONAL_ACCESS_TOKEN","push_protection_setting":"enabled"}],"custom_pattern_settings":[{"token_type":"cp_2","custom_pattern_version":"0ujsswThIGTUYm2K8FjOOfXtY1K","push_protection_setting":"enabled"}]}'`

Response

-
-

`Status: 200``{
"pattern_config_version": "0ujsswThIGTUYm2K8FjOOfXtY1K"
}`

---

# REST API endpoints for secret scanning

> Use the REST API to retrieve and update secret alerts from a repository.

## About secret scanning

You can use the API to:

- Enable or disable secret scanning and push protection for a repository. For more information, see [REST API endpoints for repositories](https://docs.github.com/en/rest/repos/repos#update-a-repository) and expand the "Properties of the `security_and_analysis` object" section.
- Retrieve and update secret scanning alerts from a repository. For further details, see the sections below.

For more information about secret scanning, see [About secret scanning](https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning).
