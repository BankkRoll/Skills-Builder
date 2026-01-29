# Configurations

# Configurations

> Use the REST API to create and manage security configurations for your organization.

## Get code security configurations for an enterprise

Lists all code security configurations available in an enterprise.

The authenticated user must be an administrator of the enterprise in order to use this endpoint.

OAuth app tokens and personal access tokens (classic) need the `read:enterprise` scope to use this endpoint.

### Fine-grained access tokens for "Get code security configurations for an enterprise"

This endpoint does not work with GitHub App user access tokens, GitHub App installation access tokens, or fine-grained personal access tokens.

### Parameters for "Get code security configurations for an enterprise"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| enterprisestringRequiredThe slug version of the enterprise name. |

| Name, Type, Description |
| --- |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| beforestringA cursor, as given in theLink header. If specified, the query only searches for results before this cursor. For more information, see "Using pagination in the REST API." |
| afterstringA cursor, as given in theLink header. If specified, the query only searches for results after this cursor. For more information, see "Using pagination in the REST API." |

### HTTP response status codes for "Get code security configurations for an enterprise"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 403 | Forbidden |
| 404 | Resource not found |

### Code samples for "Get code security configurations for an enterprise"

#### Request example

get/enterprises/{enterprise}/code-security/configurations

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/enterprises/ENTERPRISE/code-security/configurations`

Response

-
-

`Status: 200``[
{
"id": 17,
"target_type": "global",
"name": "GitHub recommended",
"description": "Suggested settings for Dependabot, secret scanning, and code scanning.",
"advanced_security": "enabled",
"dependency_graph": "enabled",
"dependency_graph_autosubmit_action": "not_set",
"dependency_graph_autosubmit_action_options": {
"labeled_runners": false
},
"dependabot_alerts": "enabled",
"dependabot_security_updates": "not_set",
"code_scanning_default_setup": "enabled",
"code_scanning_default_setup_options": {
"runner_type": "not_set",
"runner_label": null
},
"secret_scanning": "enabled",
"secret_scanning_push_protection": "enabled",
"secret_scanning_validity_checks": "enabled",
"secret_scanning_non_provider_patterns": "enabled",
"private_vulnerability_reporting": "enabled",
"enforcement": "enforced",
"url": "https://api.github.com/enterprises/octo-enterprise/code-security/configurations/17",
"html_url": "https://github.com/organizations/octo-enterprise/settings/security_analysis/configurations/17/view",
"created_at": "2023-12-04T15:58:07Z",
"updated_at": "2023-12-04T15:58:07Z"
},
{
"id": 1326,
"target_type": "enterprise",
"name": "High risk settings",
"description": "This is a code security configuration for octo-enterprise high risk repositories",
"advanced_security": "enabled",
"dependency_graph": "enabled",
"dependency_graph_autosubmit_action": "enabled",
"dependency_graph_autosubmit_action_options": {
"labeled_runners": false
},
"dependabot_alerts": "enabled",
"dependabot_security_updates": "enabled",
"code_scanning_default_setup": "enabled",
"code_scanning_default_setup_options": {
"runner_type": "not_set",
"runner_label": null
},
"secret_scanning": "enabled",
"secret_scanning_push_protection": "enabled",
"secret_scanning_validity_checks": "disabled",
"secret_scanning_non_provider_patterns": "disabled",
"private_vulnerability_reporting": "enabled",
"enforcement": "enforced",
"url": "https://api.github.com/enterprises/octo-enterprise/code-security/configurations/1326",
"html_url": "https://github.com/enterprises/octo-enterprise/settings/security_analysis/configurations/1326/edit",
"created_at": "2024-05-10T00:00:00Z",
"updated_at": "2024-05-10T00:00:00Z"
}
]`

## Create a code security configuration for an enterprise

Creates a code security configuration in an enterprise.

The authenticated user must be an administrator of the enterprise in order to use this endpoint.

OAuth app tokens and personal access tokens (classic) need the `admin:enterprise` scope to use this endpoint.

### Fine-grained access tokens for "Create a code security configuration for an enterprise"

This endpoint does not work with GitHub App user access tokens, GitHub App installation access tokens, or fine-grained personal access tokens.

### Parameters for "Create a code security configuration for an enterprise"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| enterprisestringRequiredThe slug version of the enterprise name. |

| Name, Type, Description |
| --- |
| namestringRequiredThe name of the code security configuration. Must be unique within the enterprise. |
| descriptionstringRequiredA description of the code security configuration |
| advanced_securitystringThe enablement status of GitHub Advanced Security features.enabledwill enable both Code Security and Secret Protection features.Warningcode_securityandsecret_protectionare deprecated values for this field. Prefer the individualcode_securityandsecret_protectionfields to set the status of these features.Default:disabledCan be one of:enabled,disabled,code_security,secret_protection |
| code_securitystringThe enablement status of GitHub Code Security features.Can be one of:enabled,disabled,not_set |
| dependency_graphstringThe enablement status of Dependency GraphDefault:enabledCan be one of:enabled,disabled,not_set |
| dependency_graph_autosubmit_actionstringThe enablement status of Automatic dependency submissionDefault:disabledCan be one of:enabled,disabled,not_set |
| dependency_graph_autosubmit_action_optionsobjectFeature options for Automatic dependency submission |
| Name, Type, Descriptionlabeled_runnersbooleanWhether to use runners labeled with 'dependency-submission' or standard GitHub runners.Default:false |
| Name, Type, Description |
| labeled_runnersbooleanWhether to use runners labeled with 'dependency-submission' or standard GitHub runners.Default:false |
| dependabot_alertsstringThe enablement status of Dependabot alertsDefault:disabledCan be one of:enabled,disabled,not_set |
| dependabot_security_updatesstringThe enablement status of Dependabot security updatesDefault:disabledCan be one of:enabled,disabled,not_set |
| code_scanning_optionsobject or nullSecurity Configuration feature options for code scanning |
| Name, Type, Descriptionallow_advancedboolean or nullWhether to allow repos which use advanced setup |
| Name, Type, Description |
| allow_advancedboolean or nullWhether to allow repos which use advanced setup |
| code_scanning_default_setupstringThe enablement status of code scanning default setupDefault:disabledCan be one of:enabled,disabled,not_set |
| code_scanning_default_setup_optionsobject or nullFeature options for code scanning default setup |
| Name, Type, Descriptionrunner_typestringWhether to use labeled runners or standard GitHub runners.Can be one of:standard,labeled,not_setrunner_labelstring or nullThe label of the runner to use for code scanning default setup when runner_type is 'labeled'. |
| Name, Type, Description |
| runner_typestringWhether to use labeled runners or standard GitHub runners.Can be one of:standard,labeled,not_set |
| runner_labelstring or nullThe label of the runner to use for code scanning default setup when runner_type is 'labeled'. |
| code_scanning_delegated_alert_dismissalstringThe enablement status of code scanning delegated alert dismissalDefault:disabledCan be one of:enabled,disabled,not_set |
| secret_protectionstringThe enablement status of GitHub Secret Protection features.Can be one of:enabled,disabled,not_set |
| secret_scanningstringThe enablement status of secret scanningDefault:disabledCan be one of:enabled,disabled,not_set |
| secret_scanning_push_protectionstringThe enablement status of secret scanning push protectionDefault:disabledCan be one of:enabled,disabled,not_set |
| secret_scanning_validity_checksstringThe enablement status of secret scanning validity checksDefault:disabledCan be one of:enabled,disabled,not_set |
| secret_scanning_non_provider_patternsstringThe enablement status of secret scanning non provider patternsDefault:disabledCan be one of:enabled,disabled,not_set |
| secret_scanning_generic_secretsstringThe enablement status of Copilot secret scanningDefault:disabledCan be one of:enabled,disabled,not_set |
| secret_scanning_delegated_alert_dismissalstringThe enablement status of secret scanning delegated alert dismissalDefault:disabledCan be one of:enabled,disabled,not_set |
| private_vulnerability_reportingstringThe enablement status of private vulnerability reportingDefault:disabledCan be one of:enabled,disabled,not_set |
| enforcementstringThe enforcement status for a security configurationDefault:enforcedCan be one of:enforced,unenforced |

### HTTP response status codes for "Create a code security configuration for an enterprise"

| Status code | Description |
| --- | --- |
| 201 | Successfully created code security configuration |
| 400 | Bad Request |
| 403 | Forbidden |
| 404 | Resource not found |

### Code samples for "Create a code security configuration for an enterprise"

#### Request example

post/enterprises/{enterprise}/code-security/configurations

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/enterprises/ENTERPRISE/code-security/configurations \
  -d '{"name":"High rish settings","description":"This is a code security configuration for octo-enterprise","advanced_security":"enabled","dependabot_alerts":"enabled","dependabot_security_updates":"not_set","secret_scanning":"enabled"}'`

Successfully created code security configuration

-
-

`Status: 201``{
"id": 1325,
"target_type": "enterprise",
"name": "High risk settings",
"description": "This is a code security configuration for octo-enterprise",
"advanced_security": "enabled",
"dependency_graph": "enabled",
"dependency_graph_autosubmit_action": "enabled",
"dependency_graph_autosubmit_action_options": {
"labeled_runners": false
},
"dependabot_alerts": "enabled",
"dependabot_security_updates": "not_set",
"code_scanning_default_setup": "disabled",
"code_scanning_delegated_alert_dismissal": "disabled",
"secret_scanning": "enabled",
"secret_scanning_push_protection": "disabled",
"secret_scanning_delegated_bypass": "disabled",
"secret_scanning_validity_checks": "disabled",
"secret_scanning_non_provider_patterns": "disabled",
"secret_scanning_generic_secrets": "disabled",
"secret_scanning_delegated_alert_dismissal": "disabled",
"private_vulnerability_reporting": "disabled",
"enforcement": "enforced",
"url": "https://api.github.com/enterprises/octo-enterprise/code-security/configurations/1325",
"html_url": "https://github.com/enterprises/octo-enterprise/settings/security_analysis/configurations/1325/edit",
"created_at": "2024-05-01T00:00:00Z",
"updated_at": "2024-05-01T00:00:00Z"
}`

## Get default code security configurations for an enterprise

Lists the default code security configurations for an enterprise.

The authenticated user must be an administrator of the enterprise in order to use this endpoint.

OAuth app tokens and personal access tokens (classic) need the `read:enterprise` scope to use this endpoint.

### Fine-grained access tokens for "Get default code security configurations for an enterprise"

This endpoint does not work with GitHub App user access tokens, GitHub App installation access tokens, or fine-grained personal access tokens.

### Parameters for "Get default code security configurations for an enterprise"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| enterprisestringRequiredThe slug version of the enterprise name. |

### HTTP response status codes for "Get default code security configurations for an enterprise"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "Get default code security configurations for an enterprise"

#### Request example

get/enterprises/{enterprise}/code-security/configurations/defaults

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/enterprises/ENTERPRISE/code-security/configurations/defaults`

Response

-
-

`Status: 200``[
{
"default_for_new_repos": "public",
"configuration": {
"id": 1325,
"target_type": "organization",
"name": "octo-org recommended settings",
"description": "This is a code security configuration for octo-org",
"advanced_security": "enabled",
"dependency_graph": "enabled",
"dependency_graph_autosubmit_action": "not_set",
"dependency_graph_autosubmit_action_options": {
"labeled_runners": false
},
"dependabot_alerts": "enabled",
"dependabot_security_updates": "not_set",
"code_scanning_default_setup": "enabled",
"code_scanning_default_setup_options": {
"runner_type": "not_set",
"runner_label": null
},
"code_scanning_options": {
"allow_advanced": false
},
"secret_scanning": "enabled",
"secret_scanning_push_protection": "enabled",
"secret_scanning_delegated_bypass": "enabled",
"secret_scanning_delegated_bypass_options": {
"reviewers": [
{
"security_configuration_id": 1325,
"reviewer_id": 5678,
"reviewer_type": "TEAM"
}
]
},
"secret_scanning_validity_checks": "enabled",
"secret_scanning_non_provider_patterns": "enabled",
"private_vulnerability_reporting": "enabled",
"enforcement": "enforced",
"url": "https://api.github.com/orgs/octo-org/code-security/configurations/1325",
"html_url": "https://github.com/organizations/octo-org/settings/security_products/configurations/edit/1325",
"created_at": "2024-05-01T00:00:00Z",
"updated_at": "2024-05-01T00:00:00Z"
}
},
{
"default_for_new_repos": "private_and_internal",
"configuration": {
"id": 17,
"target_type": "global",
"name": "GitHub recommended",
"description": "Suggested settings for Dependabot, secret scanning, and code scanning.",
"advanced_security": "enabled",
"dependency_graph": "enabled",
"dependency_graph_autosubmit_action": "not_set",
"dependency_graph_autosubmit_action_options": {
"labeled_runners": false
},
"dependabot_alerts": "enabled",
"dependabot_security_updates": "not_set",
"code_scanning_default_setup": "enabled",
"code_scanning_default_setup_options": {
"runner_type": "not_set",
"runner_label": null
},
"code_scanning_options": {
"allow_advanced": false
},
"secret_scanning": "enabled",
"secret_scanning_push_protection": "enabled",
"secret_scanning_delegated_bypass": "disabled",
"secret_scanning_validity_checks": "disabled",
"private_vulnerability_reporting": "enabled",
"enforcement": "enforced",
"url": "https://api.github.com/orgs/octo-org/code-security/configurations/17",
"html_url": "https://github.com/organizations/octo-org/settings/security_products/configurations/view",
"created_at": "2023-12-04T15:58:07Z",
"updated_at": "2023-12-04T15:58:07Z"
}
}
]`

## Retrieve a code security configuration of an enterprise

Gets a code security configuration available in an enterprise.

The authenticated user must be an administrator of the enterprise in order to use this endpoint.

OAuth app tokens and personal access tokens (classic) need the `read:enterprise` scope to use this endpoint.

### Fine-grained access tokens for "Retrieve a code security configuration of an enterprise"

This endpoint does not work with GitHub App user access tokens, GitHub App installation access tokens, or fine-grained personal access tokens.

### Parameters for "Retrieve a code security configuration of an enterprise"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| enterprisestringRequiredThe slug version of the enterprise name. |
| configuration_idintegerRequiredThe unique identifier of the code security configuration. |

### HTTP response status codes for "Retrieve a code security configuration of an enterprise"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 304 | Not modified |
| 403 | Forbidden |
| 404 | Resource not found |

### Code samples for "Retrieve a code security configuration of an enterprise"

#### Request example

get/enterprises/{enterprise}/code-security/configurations/{configuration_id}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/enterprises/ENTERPRISE/code-security/configurations/CONFIGURATION_ID`

Response

-
-

`Status: 200``{
"id": 1325,
"target_type": "enterprise",
"name": "High risk settings",
"description": "This is a code security configuration for octo-enterprise",
"advanced_security": "enabled",
"dependency_graph": "enabled",
"dependency_graph_autosubmit_action": "enabled",
"dependency_graph_autosubmit_action_options": {
"labeled_runners": false
},
"dependabot_alerts": "enabled",
"dependabot_security_updates": "not_set",
"code_scanning_default_setup": "disabled",
"code_scanning_delegated_alert_dismissal": "disabled",
"secret_scanning": "enabled",
"secret_scanning_push_protection": "disabled",
"secret_scanning_delegated_bypass": "disabled",
"secret_scanning_validity_checks": "disabled",
"secret_scanning_non_provider_patterns": "disabled",
"secret_scanning_generic_secrets": "disabled",
"secret_scanning_delegated_alert_dismissal": "disabled",
"private_vulnerability_reporting": "disabled",
"enforcement": "enforced",
"url": "https://api.github.com/enterprises/octo-enterprise/code-security/configurations/1325",
"html_url": "https://github.com/enterprises/octo-enterprise/settings/security_analysis/configurations/1325/edit",
"created_at": "2024-05-01T00:00:00Z",
"updated_at": "2024-05-01T00:00:00Z"
}`

## Update a custom code security configuration for an enterprise

Updates a code security configuration in an enterprise.

The authenticated user must be an administrator of the enterprise in order to use this endpoint.

OAuth app tokens and personal access tokens (classic) need the `admin:enterprise` scope to use this endpoint.

### Fine-grained access tokens for "Update a custom code security configuration for an enterprise"

This endpoint does not work with GitHub App user access tokens, GitHub App installation access tokens, or fine-grained personal access tokens.

### Parameters for "Update a custom code security configuration for an enterprise"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| enterprisestringRequiredThe slug version of the enterprise name. |
| configuration_idintegerRequiredThe unique identifier of the code security configuration. |

| Name, Type, Description |
| --- |
| namestringThe name of the code security configuration. Must be unique across the enterprise. |
| descriptionstringA description of the code security configuration |
| advanced_securitystringThe enablement status of GitHub Advanced Security features.enabledwill enable both Code Security and Secret Protection features.Warningcode_securityandsecret_protectionare deprecated values for this field. Prefer the individualcode_securityandsecret_protectionfields to set the status of these features.Can be one of:enabled,disabled,code_security,secret_protection |
| code_securitystringThe enablement status of GitHub Code Security features.Can be one of:enabled,disabled,not_set |
| dependency_graphstringThe enablement status of Dependency GraphCan be one of:enabled,disabled,not_set |
| dependency_graph_autosubmit_actionstringThe enablement status of Automatic dependency submissionCan be one of:enabled,disabled,not_set |
| dependency_graph_autosubmit_action_optionsobjectFeature options for Automatic dependency submission |
| Name, Type, Descriptionlabeled_runnersbooleanWhether to use runners labeled with 'dependency-submission' or standard GitHub runners. |
| Name, Type, Description |
| labeled_runnersbooleanWhether to use runners labeled with 'dependency-submission' or standard GitHub runners. |
| dependabot_alertsstringThe enablement status of Dependabot alertsCan be one of:enabled,disabled,not_set |
| dependabot_security_updatesstringThe enablement status of Dependabot security updatesCan be one of:enabled,disabled,not_set |
| code_scanning_default_setupstringThe enablement status of code scanning default setupCan be one of:enabled,disabled,not_set |
| code_scanning_default_setup_optionsobject or nullFeature options for code scanning default setup |
| Name, Type, Descriptionrunner_typestringWhether to use labeled runners or standard GitHub runners.Can be one of:standard,labeled,not_setrunner_labelstring or nullThe label of the runner to use for code scanning default setup when runner_type is 'labeled'. |
| Name, Type, Description |
| runner_typestringWhether to use labeled runners or standard GitHub runners.Can be one of:standard,labeled,not_set |
| runner_labelstring or nullThe label of the runner to use for code scanning default setup when runner_type is 'labeled'. |
| code_scanning_optionsobject or nullSecurity Configuration feature options for code scanning |
| Name, Type, Descriptionallow_advancedboolean or nullWhether to allow repos which use advanced setup |
| Name, Type, Description |
| allow_advancedboolean or nullWhether to allow repos which use advanced setup |
| code_scanning_delegated_alert_dismissalstringThe enablement status of code scanning delegated alert dismissalDefault:disabledCan be one of:enabled,disabled,not_set |
| secret_protectionstringThe enablement status of GitHub Secret Protection features.Can be one of:enabled,disabled,not_set |
| secret_scanningstringThe enablement status of secret scanningCan be one of:enabled,disabled,not_set |
| secret_scanning_push_protectionstringThe enablement status of secret scanning push protectionCan be one of:enabled,disabled,not_set |
| secret_scanning_validity_checksstringThe enablement status of secret scanning validity checksCan be one of:enabled,disabled,not_set |
| secret_scanning_non_provider_patternsstringThe enablement status of secret scanning non-provider patternsCan be one of:enabled,disabled,not_set |
| secret_scanning_generic_secretsstringThe enablement status of Copilot secret scanningDefault:disabledCan be one of:enabled,disabled,not_set |
| secret_scanning_delegated_alert_dismissalstringThe enablement status of secret scanning delegated alert dismissalDefault:disabledCan be one of:enabled,disabled,not_set |
| private_vulnerability_reportingstringThe enablement status of private vulnerability reportingCan be one of:enabled,disabled,not_set |
| enforcementstringThe enforcement status for a security configurationCan be one of:enforced,unenforced |

### HTTP response status codes for "Update a custom code security configuration for an enterprise"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 304 | Not modified |
| 403 | Forbidden |
| 404 | Resource not found |
| 409 | Conflict |

### Code samples for "Update a custom code security configuration for an enterprise"

#### Request example

patch/enterprises/{enterprise}/code-security/configurations/{configuration_id}

-
-
-

`curl -L \
  -X PATCH \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/enterprises/ENTERPRISE/code-security/configurations/CONFIGURATION_ID \
  -d '{"name":"octo-enterprise recommended settings v2","secret_scanning":"disabled","code_scanning_default_setup":"enabled"}'`

Response

-
-

`Status: 200``{
"id": 1325,
"target_type": "enterprise",
"name": "High risk settings",
"description": "This is a code security configuration for octo-enterprise",
"advanced_security": "enabled",
"dependency_graph": "enabled",
"dependency_graph_autosubmit_action": "enabled",
"dependency_graph_autosubmit_action_options": {
"labeled_runners": false
},
"dependabot_alerts": "enabled",
"dependabot_security_updates": "not_set",
"code_scanning_default_setup": "disabled",
"code_scanning_delegated_alert_dismissal": "disabled",
"secret_scanning": "enabled",
"secret_scanning_push_protection": "disabled",
"secret_scanning_delegated_bypass": "disabled",
"secret_scanning_validity_checks": "disabled",
"secret_scanning_non_provider_patterns": "disabled",
"secret_scanning_generic_secrets": "disabled",
"secret_scanning_delegated_alert_dismissal": "disabled",
"private_vulnerability_reporting": "disabled",
"enforcement": "enforced",
"url": "https://api.github.com/enterprises/octo-enterprise/code-security/configurations/1325",
"html_url": "https://github.com/enterprises/octo-enterprise/settings/security_analysis/configurations/1325/edit",
"created_at": "2024-05-01T00:00:00Z",
"updated_at": "2024-05-01T00:00:00Z"
}`

## Delete a code security configuration for an enterprise

Deletes a code security configuration from an enterprise.
Repositories attached to the configuration will retain their settings but will no longer be associated with
the configuration.

The authenticated user must be an administrator for the enterprise to use this endpoint.

OAuth app tokens and personal access tokens (classic) need the `admin:enterprise` scope to use this endpoint.

### Fine-grained access tokens for "Delete a code security configuration for an enterprise"

This endpoint does not work with GitHub App user access tokens, GitHub App installation access tokens, or fine-grained personal access tokens.

### Parameters for "Delete a code security configuration for an enterprise"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| enterprisestringRequiredThe slug version of the enterprise name. |
| configuration_idintegerRequiredThe unique identifier of the code security configuration. |

### HTTP response status codes for "Delete a code security configuration for an enterprise"

| Status code | Description |
| --- | --- |
| 204 | A header with no content is returned. |
| 400 | Bad Request |
| 403 | Forbidden |
| 404 | Resource not found |
| 409 | Conflict |

### Code samples for "Delete a code security configuration for an enterprise"

#### Request example

delete/enterprises/{enterprise}/code-security/configurations/{configuration_id}

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/enterprises/ENTERPRISE/code-security/configurations/CONFIGURATION_ID`

A header with no content is returned.

`Status: 204`

## Attach an enterprise configuration to repositories

Attaches an enterprise code security configuration to repositories. If the repositories specified are already attached to a configuration, they will be re-attached to the provided configuration.

If insufficient GHAS licenses are available to attach the configuration to a repository, only free features will be enabled.

The authenticated user must be an administrator for the enterprise to use this endpoint.

OAuth app tokens and personal access tokens (classic) need the `admin:enterprise` scope to use this endpoint.

### Fine-grained access tokens for "Attach an enterprise configuration to repositories"

This endpoint does not work with GitHub App user access tokens, GitHub App installation access tokens, or fine-grained personal access tokens.

### Parameters for "Attach an enterprise configuration to repositories"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| enterprisestringRequiredThe slug version of the enterprise name. |
| configuration_idintegerRequiredThe unique identifier of the code security configuration. |

| Name, Type, Description |
| --- |
| scopestringRequiredThe type of repositories to attach the configuration to.Can be one of:all,all_without_configurations |

### HTTP response status codes for "Attach an enterprise configuration to repositories"

| Status code | Description |
| --- | --- |
| 202 | Accepted |
| 403 | Forbidden |
| 404 | Resource not found |
| 409 | Conflict |

### Code samples for "Attach an enterprise configuration to repositories"

#### Request example

post/enterprises/{enterprise}/code-security/configurations/{configuration_id}/attach

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/enterprises/ENTERPRISE/code-security/configurations/CONFIGURATION_ID/attach \
  -d '{"scope":"all"}'`

Accepted

-
-

`Status: 202`

## Set a code security configuration as a default for an enterprise

Sets a code security configuration as a default to be applied to new repositories in your enterprise.

This configuration will be applied by default to the matching repository type when created, but only for organizations within the enterprise that do not already have a default code security configuration set.

The authenticated user must be an administrator for the enterprise to use this endpoint.

OAuth app tokens and personal access tokens (classic) need the `admin:enterprise` scope to use this endpoint.

### Fine-grained access tokens for "Set a code security configuration as a default for an enterprise"

This endpoint does not work with GitHub App user access tokens, GitHub App installation access tokens, or fine-grained personal access tokens.

### Parameters for "Set a code security configuration as a default for an enterprise"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| enterprisestringRequiredThe slug version of the enterprise name. |
| configuration_idintegerRequiredThe unique identifier of the code security configuration. |

| Name, Type, Description |
| --- |
| default_for_new_reposstringSpecify which types of repository this security configuration should be applied to by default.Can be one of:all,none,private_and_internal,public |

### HTTP response status codes for "Set a code security configuration as a default for an enterprise"

| Status code | Description |
| --- | --- |
| 200 | Default successfully changed. |
| 403 | Forbidden |
| 404 | Resource not found |

### Code samples for "Set a code security configuration as a default for an enterprise"

#### Request example

put/enterprises/{enterprise}/code-security/configurations/{configuration_id}/defaults

-
-
-

`curl -L \
  -X PUT \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/enterprises/ENTERPRISE/code-security/configurations/CONFIGURATION_ID/defaults \
  -d '{"default_for_new_repos":"all"}'`

Default successfully changed.

-
-

`Status: 200``{
"default_for_new_repos": "all",
"configuration": {
"value": {
"id": 1325,
"target_type": "organization",
"name": "octo-org recommended settings",
"description": "This is a code security configuration for octo-org",
"advanced_security": "enabled",
"dependency_graph": "enabled",
"dependency_graph_autosubmit_action": "enabled",
"dependency_graph_autosubmit_action_options": {
"labeled_runners": false
},
"dependabot_alerts": "enabled",
"dependabot_security_updates": "not_set",
"code_scanning_default_setup": "disabled",
"code_scanning_default_setup_options": {
"runner_type": "not_set",
"runner_label": null
},
"code_scanning_options": {
"allow_advanced": false
},
"code_scanning_delegated_alert_dismissal": "disabled",
"secret_scanning": "enabled",
"secret_scanning_push_protection": "disabled",
"secret_scanning_delegated_bypass": "disabled",
"secret_scanning_validity_checks": "disabled",
"secret_scanning_non_provider_patterns": "disabled",
"secret_scanning_generic_secrets": "disabled",
"secret_scanning_delegated_alert_dismissal": "disabled",
"private_vulnerability_reporting": "disabled",
"enforcement": "enforced",
"url": "https://api.github.com/orgs/octo-org/code-security/configurations/1325",
"html_url": "https://github.com/organizations/octo-org/settings/security_products/configurations/edit/1325",
"created_at": "2024-05-01T00:00:00Z",
"updated_at": "2024-05-01T00:00:00Z"
}
}
}`

## Get repositories associated with an enterprise code security configuration

Lists the repositories associated with an enterprise code security configuration in an organization.

The authenticated user must be an administrator of the enterprise in order to use this endpoint.

OAuth app tokens and personal access tokens (classic) need the `read:enterprise` scope to use this endpoint.

### Fine-grained access tokens for "Get repositories associated with an enterprise code security configuration"

This endpoint does not work with GitHub App user access tokens, GitHub App installation access tokens, or fine-grained personal access tokens.

### Parameters for "Get repositories associated with an enterprise code security configuration"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| enterprisestringRequiredThe slug version of the enterprise name. |
| configuration_idintegerRequiredThe unique identifier of the code security configuration. |

| Name, Type, Description |
| --- |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| beforestringA cursor, as given in theLink header. If specified, the query only searches for results before this cursor. For more information, see "Using pagination in the REST API." |
| afterstringA cursor, as given in theLink header. If specified, the query only searches for results after this cursor. For more information, see "Using pagination in the REST API." |
| statusstringA comma-separated list of statuses. If specified, only repositories with these attachment statuses will be returned.Can be:all,attached,attaching,removed,enforced,failed,updating,removed_by_enterpriseDefault:all |

### HTTP response status codes for "Get repositories associated with an enterprise code security configuration"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 403 | Forbidden |
| 404 | Resource not found |

### Code samples for "Get repositories associated with an enterprise code security configuration"

#### Request example

get/enterprises/{enterprise}/code-security/configurations/{configuration_id}/repositories

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/enterprises/ENTERPRISE/code-security/configurations/CONFIGURATION_ID/repositories`

Example of code security configuration repositories

-
-

`Status: 200``[
{
"status": "attached",
"repository": {
"value": {
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
}
}
]`

## Get code security configurations for an organization

Lists all code security configurations available in an organization.

The authenticated user must be an administrator or security manager for the organization to use this endpoint.

OAuth app tokens and personal access tokens (classic) need the `read:org` scope to use this endpoint.

### Fine-grained access tokens for "Get code security configurations for an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" organization permissions (read)

### Parameters for "Get code security configurations for an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| target_typestringThe target type of the code security configurationDefault:allCan be one of:global,all |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| beforestringA cursor, as given in theLink header. If specified, the query only searches for results before this cursor. For more information, see "Using pagination in the REST API." |
| afterstringA cursor, as given in theLink header. If specified, the query only searches for results after this cursor. For more information, see "Using pagination in the REST API." |

### HTTP response status codes for "Get code security configurations for an organization"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 403 | Forbidden |
| 404 | Resource not found |

### Code samples for "Get code security configurations for an organization"

#### Request example

get/orgs/{org}/code-security/configurations

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/code-security/configurations`

Response

-
-

`Status: 200``[
{
"id": 17,
"target_type": "global",
"name": "GitHub recommended",
"description": "Suggested settings for Dependabot, secret scanning, and code scanning.",
"advanced_security": "enabled",
"dependency_graph": "enabled",
"dependency_graph_autosubmit_action": "not_set",
"dependency_graph_autosubmit_action_options": {
"labeled_runners": false
},
"dependabot_alerts": "enabled",
"dependabot_security_updates": "not_set",
"code_scanning_default_setup": "enabled",
"code_scanning_delegated_alert_dismissal": "enabled",
"secret_scanning": "enabled",
"secret_scanning_push_protection": "enabled",
"secret_scanning_delegated_bypass": "enabled",
"secret_scanning_delegated_bypass_options": {
"reviewers": [
{
"security_configuration_id": 17,
"reviewer_id": 5678,
"reviewer_type": "TEAM"
}
]
},
"secret_scanning_validity_checks": "enabled",
"secret_scanning_non_provider_patterns": "enabled",
"secret_scanning_delegated_alert_dismissal": "not_set",
"private_vulnerability_reporting": "enabled",
"enforcement": "enforced",
"url": "https://api.github.com/orgs/octo-org/code-security/configurations/17",
"html_url": "https://github.com/organizations/octo-org/settings/security_products/configurations/view",
"created_at": "2023-12-04T15:58:07Z",
"updated_at": "2023-12-04T15:58:07Z"
},
{
"id": 1326,
"target_type": "organization",
"name": "High risk settings",
"description": "This is a code security configuration for octo-org high risk repositories",
"advanced_security": "enabled",
"dependency_graph": "enabled",
"dependency_graph_autosubmit_action": "enabled",
"dependency_graph_autosubmit_action_options": {
"labeled_runners": false
},
"dependabot_alerts": "enabled",
"dependabot_security_updates": "enabled",
"code_scanning_default_setup": "enabled",
"code_scanning_delegated_alert_dismissal": "enabled",
"secret_scanning": "enabled",
"secret_scanning_push_protection": "enabled",
"secret_scanning_delegated_bypass": "disabled",
"secret_scanning_validity_checks": "disabled",
"secret_scanning_non_provider_patterns": "disabled",
"secret_scanning_delegated_alert_dismissal": "disabled",
"private_vulnerability_reporting": "enabled",
"enforcement": "enforced",
"url": "https://api.github.com/orgs/octo-org/code-security/configurations/1326",
"html_url": "https://github.com/organizations/octo-org/settings/security_products/configurations/edit/1326",
"created_at": "2024-05-10T00:00:00Z",
"updated_at": "2024-05-10T00:00:00Z"
}
]`

## Create a code security configuration

Creates a code security configuration in an organization.

The authenticated user must be an administrator or security manager for the organization to use this endpoint.

OAuth app tokens and personal access tokens (classic) need the `write:org` scope to use this endpoint.

### Fine-grained access tokens for "Create a code security configuration"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" organization permissions (write)

### Parameters for "Create a code security configuration"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| namestringRequiredThe name of the code security configuration. Must be unique within the organization. |
| descriptionstringRequiredA description of the code security configuration |
| advanced_securitystringThe enablement status of GitHub Advanced Security features.enabledwill enable both Code Security and Secret Protection features.Warningcode_securityandsecret_protectionare deprecated values for this field. Prefer the individualcode_securityandsecret_protectionfields to set the status of these features.Default:disabledCan be one of:enabled,disabled,code_security,secret_protection |
| code_securitystringThe enablement status of GitHub Code Security features.Can be one of:enabled,disabled,not_set |
| dependency_graphstringThe enablement status of Dependency GraphDefault:enabledCan be one of:enabled,disabled,not_set |
| dependency_graph_autosubmit_actionstringThe enablement status of Automatic dependency submissionDefault:disabledCan be one of:enabled,disabled,not_set |
| dependency_graph_autosubmit_action_optionsobjectFeature options for Automatic dependency submission |
| Name, Type, Descriptionlabeled_runnersbooleanWhether to use runners labeled with 'dependency-submission' or standard GitHub runners.Default:false |
| Name, Type, Description |
| labeled_runnersbooleanWhether to use runners labeled with 'dependency-submission' or standard GitHub runners.Default:false |
| dependabot_alertsstringThe enablement status of Dependabot alertsDefault:disabledCan be one of:enabled,disabled,not_set |
| dependabot_security_updatesstringThe enablement status of Dependabot security updatesDefault:disabledCan be one of:enabled,disabled,not_set |
| code_scanning_optionsobject or nullSecurity Configuration feature options for code scanning |
| Name, Type, Descriptionallow_advancedboolean or nullWhether to allow repos which use advanced setup |
| Name, Type, Description |
| allow_advancedboolean or nullWhether to allow repos which use advanced setup |
| code_scanning_default_setupstringThe enablement status of code scanning default setupDefault:disabledCan be one of:enabled,disabled,not_set |
| code_scanning_default_setup_optionsobject or nullFeature options for code scanning default setup |
| Name, Type, Descriptionrunner_typestringWhether to use labeled runners or standard GitHub runners.Can be one of:standard,labeled,not_setrunner_labelstring or nullThe label of the runner to use for code scanning default setup when runner_type is 'labeled'. |
| Name, Type, Description |
| runner_typestringWhether to use labeled runners or standard GitHub runners.Can be one of:standard,labeled,not_set |
| runner_labelstring or nullThe label of the runner to use for code scanning default setup when runner_type is 'labeled'. |
| code_scanning_delegated_alert_dismissalstringThe enablement status of code scanning delegated alert dismissalDefault:not_setCan be one of:enabled,disabled,not_set |
| secret_protectionstringThe enablement status of GitHub Secret Protection features.Can be one of:enabled,disabled,not_set |
| secret_scanningstringThe enablement status of secret scanningDefault:disabledCan be one of:enabled,disabled,not_set |
| secret_scanning_push_protectionstringThe enablement status of secret scanning push protectionDefault:disabledCan be one of:enabled,disabled,not_set |
| secret_scanning_delegated_bypassstringThe enablement status of secret scanning delegated bypassDefault:disabledCan be one of:enabled,disabled,not_set |
| secret_scanning_delegated_bypass_optionsobjectFeature options for secret scanning delegated bypass |
| Name, Type, Descriptionreviewersarray of objectsThe bypass reviewers for secret scanning delegated bypassName, Type, Descriptionreviewer_idintegerRequiredThe ID of the team or role selected as a bypass reviewerreviewer_typestringRequiredThe type of the bypass reviewerCan be one of:TEAM,ROLE |
| Name, Type, Description |
| reviewersarray of objectsThe bypass reviewers for secret scanning delegated bypass |
| Name, Type, Descriptionreviewer_idintegerRequiredThe ID of the team or role selected as a bypass reviewerreviewer_typestringRequiredThe type of the bypass reviewerCan be one of:TEAM,ROLE |
| Name, Type, Description |
| reviewer_idintegerRequiredThe ID of the team or role selected as a bypass reviewer |
| reviewer_typestringRequiredThe type of the bypass reviewerCan be one of:TEAM,ROLE |
| secret_scanning_validity_checksstringThe enablement status of secret scanning validity checksDefault:disabledCan be one of:enabled,disabled,not_set |
| secret_scanning_non_provider_patternsstringThe enablement status of secret scanning non provider patternsDefault:disabledCan be one of:enabled,disabled,not_set |
| secret_scanning_generic_secretsstringThe enablement status of Copilot secret scanningDefault:disabledCan be one of:enabled,disabled,not_set |
| secret_scanning_delegated_alert_dismissalstringThe enablement status of secret scanning delegated alert dismissalCan be one of:enabled,disabled,not_set |
| private_vulnerability_reportingstringThe enablement status of private vulnerability reportingDefault:disabledCan be one of:enabled,disabled,not_set |
| enforcementstringThe enforcement status for a security configurationDefault:enforcedCan be one of:enforced,unenforced |

### HTTP response status codes for "Create a code security configuration"

| Status code | Description |
| --- | --- |
| 201 | Successfully created code security configuration |

### Code samples for "Create a code security configuration"

#### Request example

post/orgs/{org}/code-security/configurations

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/code-security/configurations \
  -d '{"name":"octo-org recommended settings","description":"This is a code security configuration for octo-org","advanced_security":"enabled","dependabot_alerts":"enabled","dependabot_security_updates":"not_set","secret_scanning":"enabled"}'`

Successfully created code security configuration

-
-

`Status: 201``{
"id": 1325,
"target_type": "organization",
"name": "octo-org recommended settings",
"description": "This is a code security configuration for octo-org",
"advanced_security": "enabled",
"dependency_graph": "enabled",
"dependency_graph_autosubmit_action": "enabled",
"dependency_graph_autosubmit_action_options": {
"labeled_runners": false
},
"dependabot_alerts": "enabled",
"dependabot_security_updates": "not_set",
"code_scanning_default_setup": "disabled",
"code_scanning_default_setup_options": {
"runner_type": "not_set",
"runner_label": null
},
"code_scanning_options": {
"allow_advanced": false
},
"code_scanning_delegated_alert_dismissal": "disabled",
"secret_scanning": "enabled",
"secret_scanning_push_protection": "disabled",
"secret_scanning_delegated_bypass": "disabled",
"secret_scanning_validity_checks": "disabled",
"secret_scanning_non_provider_patterns": "disabled",
"secret_scanning_generic_secrets": "disabled",
"secret_scanning_delegated_alert_dismissal": "disabled",
"private_vulnerability_reporting": "disabled",
"enforcement": "enforced",
"url": "https://api.github.com/orgs/octo-org/code-security/configurations/1325",
"html_url": "https://github.com/organizations/octo-org/settings/security_products/configurations/edit/1325",
"created_at": "2024-05-01T00:00:00Z",
"updated_at": "2024-05-01T00:00:00Z"
}`

## Get default code security configurations

Lists the default code security configurations for an organization.

The authenticated user must be an administrator or security manager for the organization to use this endpoint.

OAuth app tokens and personal access tokens (classic) need the `read:org` scope to use this endpoint.

### Fine-grained access tokens for "Get default code security configurations"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" organization permissions (read)

### Parameters for "Get default code security configurations"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

### HTTP response status codes for "Get default code security configurations"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 304 | Not modified |
| 403 | Forbidden |
| 404 | Resource not found |

### Code samples for "Get default code security configurations"

#### Request example

get/orgs/{org}/code-security/configurations/defaults

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/code-security/configurations/defaults`

Response

-
-

`Status: 200``[
{
"default_for_new_repos": "public",
"configuration": {
"id": 1325,
"target_type": "organization",
"name": "octo-org recommended settings",
"description": "This is a code security configuration for octo-org",
"advanced_security": "enabled",
"dependency_graph": "enabled",
"dependency_graph_autosubmit_action": "not_set",
"dependency_graph_autosubmit_action_options": {
"labeled_runners": false
},
"dependabot_alerts": "enabled",
"dependabot_security_updates": "not_set",
"code_scanning_default_setup": "enabled",
"code_scanning_default_setup_options": {
"runner_type": "not_set",
"runner_label": null
},
"code_scanning_options": {
"allow_advanced": false
},
"secret_scanning": "enabled",
"secret_scanning_push_protection": "enabled",
"secret_scanning_delegated_bypass": "enabled",
"secret_scanning_delegated_bypass_options": {
"reviewers": [
{
"security_configuration_id": 1325,
"reviewer_id": 5678,
"reviewer_type": "TEAM"
}
]
},
"secret_scanning_validity_checks": "enabled",
"secret_scanning_non_provider_patterns": "enabled",
"private_vulnerability_reporting": "enabled",
"enforcement": "enforced",
"url": "https://api.github.com/orgs/octo-org/code-security/configurations/1325",
"html_url": "https://github.com/organizations/octo-org/settings/security_products/configurations/edit/1325",
"created_at": "2024-05-01T00:00:00Z",
"updated_at": "2024-05-01T00:00:00Z"
}
},
{
"default_for_new_repos": "private_and_internal",
"configuration": {
"id": 17,
"target_type": "global",
"name": "GitHub recommended",
"description": "Suggested settings for Dependabot, secret scanning, and code scanning.",
"advanced_security": "enabled",
"dependency_graph": "enabled",
"dependency_graph_autosubmit_action": "not_set",
"dependency_graph_autosubmit_action_options": {
"labeled_runners": false
},
"dependabot_alerts": "enabled",
"dependabot_security_updates": "not_set",
"code_scanning_default_setup": "enabled",
"code_scanning_default_setup_options": {
"runner_type": "not_set",
"runner_label": null
},
"code_scanning_options": {
"allow_advanced": false
},
"secret_scanning": "enabled",
"secret_scanning_push_protection": "enabled",
"secret_scanning_delegated_bypass": "disabled",
"secret_scanning_validity_checks": "disabled",
"private_vulnerability_reporting": "enabled",
"enforcement": "enforced",
"url": "https://api.github.com/orgs/octo-org/code-security/configurations/17",
"html_url": "https://github.com/organizations/octo-org/settings/security_products/configurations/view",
"created_at": "2023-12-04T15:58:07Z",
"updated_at": "2023-12-04T15:58:07Z"
}
}
]`

## Detach configurations from repositories

Detach code security configuration(s) from a set of repositories.
Repositories will retain their settings but will no longer be associated with the configuration.

The authenticated user must be an administrator or security manager for the organization to use this endpoint.

OAuth app tokens and personal access tokens (classic) need the `write:org` scope to use this endpoint.

### Fine-grained access tokens for "Detach configurations from repositories"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" organization permissions (write)

### Parameters for "Detach configurations from repositories"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| selected_repository_idsarray of integersAn array of repository IDs to detach from configurations. Up to 250 IDs can be provided. |

### HTTP response status codes for "Detach configurations from repositories"

| Status code | Description |
| --- | --- |
| 204 | A header with no content is returned. |
| 400 | Bad Request |
| 403 | Forbidden |
| 404 | Resource not found |
| 409 | Conflict |

### Code samples for "Detach configurations from repositories"

#### Request example

delete/orgs/{org}/code-security/configurations/detach

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/code-security/configurations/detach \
  -d '{"selected_repository_ids":[32,91]}'`

A header with no content is returned.

`Status: 204`

## Get a code security configuration

Gets a code security configuration available in an organization.

The authenticated user must be an administrator or security manager for the organization to use this endpoint.

OAuth app tokens and personal access tokens (classic) need the `write:org` scope to use this endpoint.

### Fine-grained access tokens for "Get a code security configuration"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" organization permissions (read)

### Parameters for "Get a code security configuration"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| configuration_idintegerRequiredThe unique identifier of the code security configuration. |

### HTTP response status codes for "Get a code security configuration"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 304 | Not modified |
| 403 | Forbidden |
| 404 | Resource not found |

### Code samples for "Get a code security configuration"

#### Request example

get/orgs/{org}/code-security/configurations/{configuration_id}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/code-security/configurations/CONFIGURATION_ID`

Response

-
-

`Status: 200``{
"id": 1325,
"target_type": "organization",
"name": "octo-org recommended settings",
"description": "This is a code security configuration for octo-org",
"advanced_security": "enabled",
"dependency_graph": "enabled",
"dependency_graph_autosubmit_action": "enabled",
"dependency_graph_autosubmit_action_options": {
"labeled_runners": false
},
"dependabot_alerts": "enabled",
"dependabot_security_updates": "not_set",
"code_scanning_default_setup": "disabled",
"code_scanning_default_setup_options": {
"runner_type": "not_set",
"runner_label": null
},
"code_scanning_options": {
"allow_advanced": false
},
"code_scanning_delegated_alert_dismissal": "disabled",
"secret_scanning": "enabled",
"secret_scanning_push_protection": "disabled",
"secret_scanning_delegated_bypass": "disabled",
"secret_scanning_validity_checks": "disabled",
"secret_scanning_non_provider_patterns": "disabled",
"secret_scanning_generic_secrets": "disabled",
"secret_scanning_delegated_alert_dismissal": "disabled",
"private_vulnerability_reporting": "disabled",
"enforcement": "enforced",
"url": "https://api.github.com/orgs/octo-org/code-security/configurations/1325",
"html_url": "https://github.com/organizations/octo-org/settings/security_products/configurations/edit/1325",
"created_at": "2024-05-01T00:00:00Z",
"updated_at": "2024-05-01T00:00:00Z"
}`

## Update a code security configuration

Updates a code security configuration in an organization.

The authenticated user must be an administrator or security manager for the organization to use this endpoint.

OAuth app tokens and personal access tokens (classic) need the `write:org` scope to use this endpoint.

### Fine-grained access tokens for "Update a code security configuration"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" organization permissions (write)

### Parameters for "Update a code security configuration"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| configuration_idintegerRequiredThe unique identifier of the code security configuration. |

| Name, Type, Description |
| --- |
| namestringThe name of the code security configuration. Must be unique within the organization. |
| descriptionstringA description of the code security configuration |
| advanced_securitystringThe enablement status of GitHub Advanced Security features.enabledwill enable both Code Security and Secret Protection features.Warningcode_securityandsecret_protectionare deprecated values for this field. Prefer the individualcode_securityandsecret_protectionfields to set the status of these features.Can be one of:enabled,disabled,code_security,secret_protection |
| code_securitystringThe enablement status of GitHub Code Security features.Can be one of:enabled,disabled,not_set |
| dependency_graphstringThe enablement status of Dependency GraphCan be one of:enabled,disabled,not_set |
| dependency_graph_autosubmit_actionstringThe enablement status of Automatic dependency submissionCan be one of:enabled,disabled,not_set |
| dependency_graph_autosubmit_action_optionsobjectFeature options for Automatic dependency submission |
| Name, Type, Descriptionlabeled_runnersbooleanWhether to use runners labeled with 'dependency-submission' or standard GitHub runners. |
| Name, Type, Description |
| labeled_runnersbooleanWhether to use runners labeled with 'dependency-submission' or standard GitHub runners. |
| dependabot_alertsstringThe enablement status of Dependabot alertsCan be one of:enabled,disabled,not_set |
| dependabot_security_updatesstringThe enablement status of Dependabot security updatesCan be one of:enabled,disabled,not_set |
| code_scanning_default_setupstringThe enablement status of code scanning default setupCan be one of:enabled,disabled,not_set |
| code_scanning_default_setup_optionsobject or nullFeature options for code scanning default setup |
| Name, Type, Descriptionrunner_typestringWhether to use labeled runners or standard GitHub runners.Can be one of:standard,labeled,not_setrunner_labelstring or nullThe label of the runner to use for code scanning default setup when runner_type is 'labeled'. |
| Name, Type, Description |
| runner_typestringWhether to use labeled runners or standard GitHub runners.Can be one of:standard,labeled,not_set |
| runner_labelstring or nullThe label of the runner to use for code scanning default setup when runner_type is 'labeled'. |
| code_scanning_optionsobject or nullSecurity Configuration feature options for code scanning |
| Name, Type, Descriptionallow_advancedboolean or nullWhether to allow repos which use advanced setup |
| Name, Type, Description |
| allow_advancedboolean or nullWhether to allow repos which use advanced setup |
| code_scanning_delegated_alert_dismissalstringThe enablement status of code scanning delegated alert dismissalDefault:disabledCan be one of:enabled,disabled,not_set |
| secret_protectionstringThe enablement status of GitHub Secret Protection features.Can be one of:enabled,disabled,not_set |
| secret_scanningstringThe enablement status of secret scanningCan be one of:enabled,disabled,not_set |
| secret_scanning_push_protectionstringThe enablement status of secret scanning push protectionCan be one of:enabled,disabled,not_set |
| secret_scanning_delegated_bypassstringThe enablement status of secret scanning delegated bypassCan be one of:enabled,disabled,not_set |
| secret_scanning_delegated_bypass_optionsobjectFeature options for secret scanning delegated bypass |
| Name, Type, Descriptionreviewersarray of objectsThe bypass reviewers for secret scanning delegated bypassName, Type, Descriptionreviewer_idintegerRequiredThe ID of the team or role selected as a bypass reviewerreviewer_typestringRequiredThe type of the bypass reviewerCan be one of:TEAM,ROLE |
| Name, Type, Description |
| reviewersarray of objectsThe bypass reviewers for secret scanning delegated bypass |
| Name, Type, Descriptionreviewer_idintegerRequiredThe ID of the team or role selected as a bypass reviewerreviewer_typestringRequiredThe type of the bypass reviewerCan be one of:TEAM,ROLE |
| Name, Type, Description |
| reviewer_idintegerRequiredThe ID of the team or role selected as a bypass reviewer |
| reviewer_typestringRequiredThe type of the bypass reviewerCan be one of:TEAM,ROLE |
| secret_scanning_validity_checksstringThe enablement status of secret scanning validity checksCan be one of:enabled,disabled,not_set |
| secret_scanning_non_provider_patternsstringThe enablement status of secret scanning non-provider patternsCan be one of:enabled,disabled,not_set |
| secret_scanning_generic_secretsstringThe enablement status of Copilot secret scanningCan be one of:enabled,disabled,not_set |
| secret_scanning_delegated_alert_dismissalstringThe enablement status of secret scanning delegated alert dismissalCan be one of:enabled,disabled,not_set |
| private_vulnerability_reportingstringThe enablement status of private vulnerability reportingCan be one of:enabled,disabled,not_set |
| enforcementstringThe enforcement status for a security configurationCan be one of:enforced,unenforced |

### HTTP response status codes for "Update a code security configuration"

| Status code | Description |
| --- | --- |
| 200 | Response when a configuration is updated |
| 204 | Response when no new updates are made |

### Code samples for "Update a code security configuration"

#### Request example

patch/orgs/{org}/code-security/configurations/{configuration_id}

-
-
-

`curl -L \
  -X PATCH \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/code-security/configurations/CONFIGURATION_ID \
  -d '{"name":"octo-org recommended settings v2","secret_scanning":"disabled","code_scanning_default_setup":"enabled"}'`

Response when a configuration is updated

-
-

`Status: 200``{
"id": 1325,
"target_type": "organization",
"name": "octo-org recommended settings v2",
"description": "This is a code security configuration for octo-org",
"advanced_security": "enabled",
"dependency_graph": "enabled",
"dependency_graph_autosubmit_action": "enabled",
"dependency_graph_autosubmit_action_options": {
"labeled_runners": false
},
"dependabot_alerts": "enabled",
"dependabot_security_updates": "not_set",
"code_scanning_default_setup": "enabled",
"code_scanning_default_setup_options": {
"runner_type": "not_set",
"runner_label": null
},
"code_scanning_options": {
"allow_advanced": false
},
"code_scanning_delegated_alert_dismissal": "disabled",
"secret_scanning": "disabled",
"secret_scanning_push_protection": "disabled",
"secret_scanning_delegated_bypass": "disabled",
"secret_scanning_validity_checks": "disabled",
"secret_scanning_non_provider_patterns": "disabled",
"secret_scanning_generic_secrets": "disabled",
"secret_scanning_delegated_alert_dismissal": "disabled",
"private_vulnerability_reporting": "disabled",
"enforcement": "enforced",
"url": "https://api.github.com/orgs/octo-org/code-security/configurations/1325",
"html_url": "https://github.com/organizations/octo-org/settings/security_products/configurations/edit/1325",
"created_at": "2024-05-01T00:00:00Z",
"updated_at": "2024-05-01T00:00:00Z"
}`

## Delete a code security configuration

Deletes the desired code security configuration from an organization.
Repositories attached to the configuration will retain their settings but will no longer be associated with
the configuration.

The authenticated user must be an administrator or security manager for the organization to use this endpoint.

OAuth app tokens and personal access tokens (classic) need the `write:org` scope to use this endpoint.

### Fine-grained access tokens for "Delete a code security configuration"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" organization permissions (write)

### Parameters for "Delete a code security configuration"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| configuration_idintegerRequiredThe unique identifier of the code security configuration. |

### HTTP response status codes for "Delete a code security configuration"

| Status code | Description |
| --- | --- |
| 204 | A header with no content is returned. |
| 400 | Bad Request |
| 403 | Forbidden |
| 404 | Resource not found |
| 409 | Conflict |

### Code samples for "Delete a code security configuration"

#### Request example

delete/orgs/{org}/code-security/configurations/{configuration_id}

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/code-security/configurations/CONFIGURATION_ID`

A header with no content is returned.

`Status: 204`

## Attach a configuration to repositories

Attach a code security configuration to a set of repositories. If the repositories specified are already attached to a configuration, they will be re-attached to the provided configuration.

If insufficient GHAS licenses are available to attach the configuration to a repository, only free features will be enabled.

The authenticated user must be an administrator or security manager for the organization to use this endpoint.

OAuth app tokens and personal access tokens (classic) need the `write:org` scope to use this endpoint.

### Fine-grained access tokens for "Attach a configuration to repositories"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" organization permissions (write)

### Parameters for "Attach a configuration to repositories"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| configuration_idintegerRequiredThe unique identifier of the code security configuration. |

| Name, Type, Description |
| --- |
| scopestringRequiredThe type of repositories to attach the configuration to.selectedmeans the configuration will be attached to only the repositories specified byselected_repository_idsCan be one of:all,all_without_configurations,public,private_or_internal,selected |
| selected_repository_idsarray of integersAn array of repository IDs to attach the configuration to. You can only provide a list of repository ids when thescopeis set toselected. |

### HTTP response status codes for "Attach a configuration to repositories"

| Status code | Description |
| --- | --- |
| 202 | Accepted |

### Code samples for "Attach a configuration to repositories"

#### Request example

post/orgs/{org}/code-security/configurations/{configuration_id}/attach

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/code-security/configurations/CONFIGURATION_ID/attach \
  -d '{"scope":"selected","selected_repository_ids":[32,91]}'`

Accepted

-
-

`Status: 202`

## Set a code security configuration as a default for an organization

Sets a code security configuration as a default to be applied to new repositories in your organization.

This configuration will be applied to the matching repository type (all, none, public, private and internal) by default when they are created.

The authenticated user must be an administrator or security manager for the organization to use this endpoint.

OAuth app tokens and personal access tokens (classic) need the `write:org` scope to use this endpoint.

### Fine-grained access tokens for "Set a code security configuration as a default for an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" organization permissions (write)

### Parameters for "Set a code security configuration as a default for an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| configuration_idintegerRequiredThe unique identifier of the code security configuration. |

| Name, Type, Description |
| --- |
| default_for_new_reposstringSpecify which types of repository this security configuration should be applied to by default.Can be one of:all,none,private_and_internal,public |

### HTTP response status codes for "Set a code security configuration as a default for an organization"

| Status code | Description |
| --- | --- |
| 200 | Default successfully changed. |
| 403 | Forbidden |
| 404 | Resource not found |

### Code samples for "Set a code security configuration as a default for an organization"

#### Request example

put/orgs/{org}/code-security/configurations/{configuration_id}/defaults

-
-
-

`curl -L \
  -X PUT \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/code-security/configurations/CONFIGURATION_ID/defaults \
  -d '{"default_for_new_repos":"all"}'`

Default successfully changed.

-
-

`Status: 200``{
"default_for_new_repos": "all",
"configuration": {
"value": {
"id": 1325,
"target_type": "organization",
"name": "octo-org recommended settings",
"description": "This is a code security configuration for octo-org",
"advanced_security": "enabled",
"dependency_graph": "enabled",
"dependency_graph_autosubmit_action": "enabled",
"dependency_graph_autosubmit_action_options": {
"labeled_runners": false
},
"dependabot_alerts": "enabled",
"dependabot_security_updates": "not_set",
"code_scanning_default_setup": "disabled",
"code_scanning_default_setup_options": {
"runner_type": "not_set",
"runner_label": null
},
"code_scanning_options": {
"allow_advanced": false
},
"code_scanning_delegated_alert_dismissal": "disabled",
"secret_scanning": "enabled",
"secret_scanning_push_protection": "disabled",
"secret_scanning_delegated_bypass": "disabled",
"secret_scanning_validity_checks": "disabled",
"secret_scanning_non_provider_patterns": "disabled",
"secret_scanning_generic_secrets": "disabled",
"secret_scanning_delegated_alert_dismissal": "disabled",
"private_vulnerability_reporting": "disabled",
"enforcement": "enforced",
"url": "https://api.github.com/orgs/octo-org/code-security/configurations/1325",
"html_url": "https://github.com/organizations/octo-org/settings/security_products/configurations/edit/1325",
"created_at": "2024-05-01T00:00:00Z",
"updated_at": "2024-05-01T00:00:00Z"
}
}
}`

## Get repositories associated with a code security configuration

Lists the repositories associated with a code security configuration in an organization.

The authenticated user must be an administrator or security manager for the organization to use this endpoint.

OAuth app tokens and personal access tokens (classic) need the `read:org` scope to use this endpoint.

### Fine-grained access tokens for "Get repositories associated with a code security configuration"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" organization permissions (read)

### Parameters for "Get repositories associated with a code security configuration"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| configuration_idintegerRequiredThe unique identifier of the code security configuration. |

| Name, Type, Description |
| --- |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| beforestringA cursor, as given in theLink header. If specified, the query only searches for results before this cursor. For more information, see "Using pagination in the REST API." |
| afterstringA cursor, as given in theLink header. If specified, the query only searches for results after this cursor. For more information, see "Using pagination in the REST API." |
| statusstringA comma-separated list of statuses. If specified, only repositories with these attachment statuses will be returned.Can be:all,attached,attaching,detached,removed,enforced,failed,updating,removed_by_enterpriseDefault:all |

### HTTP response status codes for "Get repositories associated with a code security configuration"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 403 | Forbidden |
| 404 | Resource not found |

### Code samples for "Get repositories associated with a code security configuration"

#### Request example

get/orgs/{org}/code-security/configurations/{configuration_id}/repositories

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/code-security/configurations/CONFIGURATION_ID/repositories`

Example of code security configuration repositories

-
-

`Status: 200``[
{
"status": "attached",
"repository": {
"value": {
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
}
}
]`

## Get the code security configuration associated with a repository

Get the code security configuration that manages a repository's code security settings.

The authenticated user must be an administrator or security manager for the organization to use this endpoint.

OAuth app tokens and personal access tokens (classic) need the `repo` scope to use this endpoint.

### Fine-grained access tokens for "Get the code security configuration associated with a repository"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (read)

### Parameters for "Get the code security configuration associated with a repository"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

### HTTP response status codes for "Get the code security configuration associated with a repository"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 204 | A header with no content is returned. |
| 304 | Not modified |
| 403 | Forbidden |
| 404 | Resource not found |

### Code samples for "Get the code security configuration associated with a repository"

#### Request example

get/repos/{owner}/{repo}/code-security-configuration

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/code-security-configuration`

Response

-
-

`Status: 200``{
"status": "attached",
"configuration": {
"id": 1325,
"target_type": "organization",
"name": "octo-org recommended settings",
"description": "This is a code security configuration for octo-org",
"advanced_security": "enabled",
"dependency_graph": "enabled",
"dependency_graph_autosubmit_action": "enabled",
"dependency_graph_autosubmit_action_options": {
"labeled_runners": false
},
"dependabot_alerts": "enabled",
"dependabot_security_updates": "not_set",
"code_scanning_default_setup": "disabled",
"code_scanning_delegated_alert_dismissal": "disabled",
"secret_scanning": "enabled",
"secret_scanning_push_protection": "disabled",
"secret_scanning_delegated_bypass": "disabled",
"secret_scanning_validity_checks": "disabled",
"secret_scanning_non_provider_patterns": "disabled",
"secret_scanning_generic_secrets": "disabled",
"secret_scanning_delegated_alert_dismissal": "disabled",
"private_vulnerability_reporting": "disabled",
"enforcement": "enforced",
"url": "https://api.github.com/orgs/octo-org/code-security/configurations/1325",
"html_url": "https://github.com/organizations/octo-org/settings/security_products/configurations/edit/1325",
"created_at": "2024-05-01T00:00:00Z",
"updated_at": "2024-05-01T00:00:00Z"
}
}`
