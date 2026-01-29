# Budgets and more

# Budgets

> Use the REST API to get budget information.

## Get all budgets for an organization

Note

This endpoint is in public preview and is subject to change.

Gets all budgets for an organization. The authenticated user must be an organization admin or billing manager.

### Fine-grained access tokens for "Get all budgets for an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" organization permissions (read)

### Parameters for "Get all budgets for an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

### HTTP response status codes for "Get all budgets for an organization"

| Status code | Description |
| --- | --- |
| 200 | Response when getting all budgets |
| 403 | Forbidden |
| 404 | Resource not found |
| 500 | Internal Error |

### Code samples for "Get all budgets for an organization"

#### Request example

get/organizations/{org}/settings/billing/budgets

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/organizations/ORG/settings/billing/budgets`

Response when getting all budgets

-
-

`Status: 200``{
"budgets": [
{
"id": "2066deda-923f-43f9-88d2-62395a28c0cdd",
"budget_type": "ProductPricing",
"budget_product_skus": [
"actions"
],
"budget_scope": "enterprise",
"budget_amount": 1000,
"prevent_further_usage": true,
"budget_alerting": {
"will_alert": true,
"alert_recipients": [
"enterprise-admin",
"billing-manager"
]
}
},
{
"id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
"budget_type": "SkuPricing",
"budget_product_skus": [
"actions_linux"
],
"budget_scope": "organization",
"budget_amount": 500,
"prevent_further_usage": false,
"budget_alerting": {
"will_alert": true,
"alert_recipients": [
"org-owner"
]
}
},
{
"id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
"budget_type": "ProductPricing",
"budget_product_skus": [
"packages"
],
"budget_scope": "cost_center",
"budget_amount": 250,
"prevent_further_usage": true,
"budget_alerting": {
"will_alert": false,
"alert_recipients": []
}
}
]
}`

## Get a budget by ID for an organization

Note

This endpoint is in public preview and is subject to change.

Gets a budget by ID. The authenticated user must be an organization admin or billing manager.

### Fine-grained access tokens for "Get a budget by ID for an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" organization permissions (read)

### Parameters for "Get a budget by ID for an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| budget_idstringRequiredThe ID corresponding to the budget. |

### HTTP response status codes for "Get a budget by ID for an organization"

| Status code | Description |
| --- | --- |
| 200 | Response when updating a budget |
| 400 | Bad Request |
| 403 | Forbidden |
| 404 | Resource not found |
| 500 | Internal Error |
| 503 | Service unavailable |

### Code samples for "Get a budget by ID for an organization"

#### Request example

get/organizations/{org}/settings/billing/budgets/{budget_id}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/organizations/ORG/settings/billing/budgets/BUDGET_ID`

Response when updating a budget

-
-

`Status: 200``{
"id": "2066deda-923f-43f9-88d2-62395a28c0cdd",
"budget_type": "ProductPricing",
"budget_product_sku": "actions_linux",
"budget_scope": "repository",
"budget_entity_name": "example-repo-name",
"budget_amount": 0,
"prevent_further_usage": true,
"budget_alerting": {
"will_alert": true,
"alert_recipients": [
"mona",
"lisa"
]
}
}`

## Update a budget for an organization

Note

This endpoint is in public preview and is subject to change.

Updates an existing budget for an organization. The authenticated user must be an organization admin or billing manager.

### Fine-grained access tokens for "Update a budget for an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" organization permissions (write)

### Parameters for "Update a budget for an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| budget_idstringRequiredThe ID corresponding to the budget. |

| Name, Type, Description |
| --- |
| budget_amountintegerThe budget amount in whole dollars. For license-based products, this represents the number of licenses. |
| prevent_further_usagebooleanWhether to prevent additional spending once the budget is exceeded |
| budget_alertingobject |
| Name, Type, Descriptionwill_alertbooleanWhether alerts are enabled for this budgetalert_recipientsarray of stringsArray of user login names who will receive alerts |
| Name, Type, Description |
| will_alertbooleanWhether alerts are enabled for this budget |
| alert_recipientsarray of stringsArray of user login names who will receive alerts |
| budget_scopestringThe scope of the budgetCan be one of:enterprise,organization,repository,cost_center |
| budget_entity_namestringThe name of the entity to apply the budget to |
| budget_typestringThe type of pricing for the budgetCan be one of:ProductPricing,SkuPricing |
| budget_product_skustringA single product or SKU that will be covered in the budget |

### HTTP response status codes for "Update a budget for an organization"

| Status code | Description |
| --- | --- |
| 200 | Budget updated successfully |
| 400 | Bad Request |
| 401 | Requires authentication |
| 403 | Forbidden |
| 404 | Budget not found or feature not enabled |
| 422 | Validation failed, or the endpoint has been spammed. |
| 500 | Internal server error |

### Code samples for "Update a budget for an organization"

#### Request example

patch/organizations/{org}/settings/billing/budgets/{budget_id}

-
-
-

`curl -L \
  -X PATCH \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/organizations/ORG/settings/billing/budgets/BUDGET_ID \
  -d '{"prevent_further_usage":false,"budget_amount":10,"budget_alerting":{"will_alert":false,"alert_recipients":[]}}'`

Budget updated successfully

-
-

`Status: 200``{
"message": "Budget successfully updated.",
"budget": {
"id": "2066deda-923f-43f9-88d2-62395a28c0cdd",
"budget_type": "ProductPricing",
"budget_product_sku": "actions_linux",
"budget_scope": "repository",
"budget_entity_name": "org-name/example-repo-name",
"budget_amount": 0,
"prevent_further_usage": true,
"budget_alerting": {
"will_alert": true,
"alert_recipients": [
"mona",
"lisa"
]
}
}
}`

## Delete a budget for an organization

Note

This endpoint is in public preview and is subject to change.

Deletes a budget by ID for an organization. The authenticated user must be an organization admin or billing manager.

### Fine-grained access tokens for "Delete a budget for an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" organization permissions (write)

### Parameters for "Delete a budget for an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| budget_idstringRequiredThe ID corresponding to the budget. |

### HTTP response status codes for "Delete a budget for an organization"

| Status code | Description |
| --- | --- |
| 200 | Response when deleting a budget |
| 400 | Bad Request |
| 403 | Forbidden |
| 404 | Resource not found |
| 500 | Internal Error |
| 503 | Service unavailable |

### Code samples for "Delete a budget for an organization"

#### Request example

delete/organizations/{org}/settings/billing/budgets/{budget_id}

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/organizations/ORG/settings/billing/budgets/BUDGET_ID`

Response when deleting a budget

-
-

`Status: 200``{
"message": "Budget successfully deleted.",
"budget_id": "2c1feb79-3947-4dc8-a16e-80cbd732cc0b"
}`

---

# Billing usage

> Use the REST API to get billing usage information.

The endpoints on this page return usage that is billed to the account associated with the endpoint. For help deciding which level of usage to report on, see [Automating usage reporting with the REST API](https://docs.github.com/en/billing/tutorials/automate-usage-reporting#step-1-decide-what-level-to-report-on).

- User endpoints return Copilot usage that is billed directly to an individual user’s personal account. These endpoints are only applicable if the user has purchased their own Copilot plan.
- If a user’s Copilot license is managed and billed through an organization or enterprise, their usage is not included in user-level endpoints. In that case, you must use the organization- or enterprise-level endpoints instead.

To view enterprise-level endpoints, select the dropdown menu at the top of the page and switch from Free, Pro, & Team to GitHub Enterprise Cloud.
