# REST API endpoints for draft Project items and more

# REST API endpoints for draft Project items

> Use the REST API to manage draft items in Projects.

## Create draft item for organization owned project

Create draft issue item for the specified organization owned project.

### Fine-grained access tokens for "Create draft item for organization owned project"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Projects" organization permissions (write)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "Create draft item for organization owned project"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| project_numberintegerRequiredThe project's number. |

| Name, Type, Description |
| --- |
| titlestringRequiredThe title of the draft issue item to create in the project. |
| bodystringThe body content of the draft issue item to create in the project. |

### HTTP response status codes for "Create draft item for organization owned project"

| Status code | Description |
| --- | --- |
| 201 | Created |
| 304 | Not modified |
| 401 | Requires authentication |
| 403 | Forbidden |

## Create draft item for user owned project

Create draft issue item for the specified user owned project.

### Fine-grained access tokens for "Create draft item for user owned project"

This endpoint does not work with GitHub App user access tokens, GitHub App installation access tokens, or fine-grained personal access tokens.

### Parameters for "Create draft item for user owned project"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| user_idstringRequiredThe unique identifier of the user. |
| project_numberintegerRequiredThe project's number. |

| Name, Type, Description |
| --- |
| titlestringRequiredThe title of the draft issue item to create in the project. |
| bodystringThe body content of the draft issue item to create in the project. |

### HTTP response status codes for "Create draft item for user owned project"

| Status code | Description |
| --- | --- |
| 201 | Created |
| 304 | Not modified |
| 401 | Requires authentication |
| 403 | Forbidden |

---

# REST API endpoints for Project fields

> Use the REST API to manage Project fields

## List project fields for organization

List all fields for a specific organization-owned project.

### Fine-grained access tokens for "List project fields for organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Projects" organization permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "List project fields for organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| project_numberintegerRequiredThe project's number. |
| orgstringRequiredThe organization name. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| beforestringA cursor, as given in theLink header. If specified, the query only searches for results before this cursor. For more information, see "Using pagination in the REST API." |
| afterstringA cursor, as given in theLink header. If specified, the query only searches for results after this cursor. For more information, see "Using pagination in the REST API." |

### HTTP response status codes for "List project fields for organization"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 304 | Not modified |
| 401 | Requires authentication |
| 403 | Forbidden |

### Code samples for "List project fields for organization"

#### Request example

get/orgs/{org}/projectsV2/{project_number}/fields

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/projectsV2/PROJECT_NUMBER/fields`

Response

-
-

`Status: 200``[
{
"id": 12345,
"node_id": "PVTF_lADOABCD1234567890",
"name": "Priority",
"data_type": "single_select",
"project_url": "https://api.github.com/projects/67890",
"options": [
{
"id": "option_1",
"name": {
"html": "Low",
"raw": "Low"
},
"color": "GREEN",
"description": {
"html": "Low priority items",
"raw": "Low priority items"
}
},
{
"id": "option_2",
"name": {
"html": "Medium",
"raw": "Medium"
},
"color": "YELLOW",
"description": {
"html": "Medium priority items",
"raw": "Medium priority items"
}
},
{
"id": "option_3",
"name": {
"html": "High",
"raw": "High"
},
"color": "RED",
"description": {
"html": "High priority items",
"raw": "High priority items"
}
}
],
"created_at": "2022-04-28T12:00:00Z",
"updated_at": "2022-04-28T12:00:00Z"
},
{
"id": 67891,
"node_id": "PVTF_lADOABCD9876543210",
"name": "Status",
"data_type": "single_select",
"project_url": "https://api.github.com/projects/67890",
"options": [
{
"id": "option_4",
"name": {
"html": "Todo",
"raw": "Todo"
},
"color": "GRAY",
"description": {
"html": "Items to be worked on",
"raw": "Items to be worked on"
}
},
{
"id": "option_5",
"name": {
"html": "In Progress",
"raw": "In Progress"
},
"color": "BLUE",
"description": {
"html": "Items currently being worked on",
"raw": "Items currently being worked on"
}
},
{
"id": "option_6",
"name": {
"html": "Done",
"raw": "Done"
},
"color": "GREEN",
"description": {
"html": "Completed items",
"raw": "Completed items"
}
}
],
"created_at": "2022-04-29T10:30:00Z",
"updated_at": "2022-04-29T10:30:00Z"
},
{
"id": 24680,
"node_id": "PVTF_lADOABCD2468024680",
"name": "Team notes",
"data_type": "text",
"project_url": "https://api.github.com/projects/67890",
"created_at": "2022-05-15T08:00:00Z",
"updated_at": "2022-05-15T08:00:00Z"
},
{
"id": 13579,
"node_id": "PVTF_lADOABCD1357913579",
"name": "Story points",
"data_type": "number",
"project_url": "https://api.github.com/projects/67890",
"created_at": "2022-06-01T14:30:00Z",
"updated_at": "2022-06-01T14:30:00Z"
},
{
"id": 98765,
"node_id": "PVTF_lADOABCD9876598765",
"name": "Due date",
"data_type": "date",
"project_url": "https://api.github.com/projects/67890",
"created_at": "2022-06-10T09:15:00Z",
"updated_at": "2022-06-10T09:15:00Z"
},
{
"id": 11223,
"node_id": "PVTF_lADOABCD1122311223",
"name": "Sprint",
"data_type": "iteration",
"project_url": "https://api.github.com/projects/67890",
"configuration": {
"duration": 14,
"start_day": 1,
"iterations": [
{
"id": "iter_1",
"title": {
"html": "Sprint 1",
"raw": "Sprint 1"
},
"start_date": "2022-07-01",
"duration": 14
},
{
"id": "iter_2",
"title": {
"html": "Sprint 2",
"raw": "Sprint 2"
},
"start_date": "2022-07-15",
"duration": 14
}
]
},
"created_at": "2022-06-20T16:45:00Z",
"updated_at": "2022-06-20T16:45:00Z"
}
]`

## Add a field to an organization-owned project.

Add a field to an organization-owned project.

### Fine-grained access tokens for "Add a field to an organization-owned project."

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Projects" organization permissions (write)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "Add a field to an organization-owned project."

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| project_numberintegerRequiredThe project's number. |
| orgstringRequiredThe organization name. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| issue_field_idintegerRequiredThe ID of the IssueField to create the field for. |
| namestringRequiredThe name of the field. |
| data_typestringRequiredThe field's data type.Value:iteration |
| single_select_optionsarray of objectsThe options available for single select fields. At least one option must be provided when creating a single select field. |
| Name, Type, DescriptionnamestringThe display name of the option.colorstringThe color associated with the option.Can be one of:BLUE,GRAY,GREEN,ORANGE,PINK,PURPLE,RED,YELLOWdescriptionstringThe description of the option. |
| Name, Type, Description |
| namestringThe display name of the option. |
| colorstringThe color associated with the option.Can be one of:BLUE,GRAY,GREEN,ORANGE,PINK,PURPLE,RED,YELLOW |
| descriptionstringThe description of the option. |
| iteration_configurationobjectRequiredThe configuration for iteration fields. |
| Name, Type, Descriptionstart_datestringThe start date of the first iteration.durationintegerThe default duration for iterations in days. Individual iterations can override this value.iterationsarray of objectsZero or more iterations for the field.Name, Type, DescriptiontitlestringThe title of the iteration.start_datestringThe start date of the iteration.durationintegerThe duration of the iteration in days. |
| Name, Type, Description |
| start_datestringThe start date of the first iteration. |
| durationintegerThe default duration for iterations in days. Individual iterations can override this value. |
| iterationsarray of objectsZero or more iterations for the field. |
| Name, Type, DescriptiontitlestringThe title of the iteration.start_datestringThe start date of the iteration.durationintegerThe duration of the iteration in days. |
| Name, Type, Description |
| titlestringThe title of the iteration. |
| start_datestringThe start date of the iteration. |
| durationintegerThe duration of the iteration in days. |

### HTTP response status codes for "Add a field to an organization-owned project."

| Status code | Description |
| --- | --- |
| 201 | Response for adding a field to an organization-owned project. |
| 304 | Not modified |
| 401 | Requires authentication |
| 403 | Forbidden |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Add a field to an organization-owned project."

#### Request examples

Select the example typeCreate a text fieldCreate a number fieldCreate a date fieldCreate a single select fieldCreate an iteration fieldpost/orgs/{org}/projectsV2/{project_number}/fields

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/projectsV2/PROJECT_NUMBER/fields \
  -d '{"name":"Team notes","data_type":"text"}'`

Response for adding a field to an organization-owned project.

-
-

`Status: 201``{
"id": 24680,
"node_id": "PVTF_lADOABCD2468024680",
"name": "Team notes",
"data_type": "text",
"project_url": "https://api.github.com/projects/67890",
"created_at": "2022-05-15T08:00:00Z",
"updated_at": "2022-05-15T08:00:00Z"
}`

## Get project field for organization

Get a specific field for an organization-owned project.

### Fine-grained access tokens for "Get project field for organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Projects" organization permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "Get project field for organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| project_numberintegerRequiredThe project's number. |
| field_idintegerRequiredThe unique identifier of the field. |
| orgstringRequiredThe organization name. The name is not case sensitive. |

### HTTP response status codes for "Get project field for organization"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 304 | Not modified |
| 401 | Requires authentication |
| 403 | Forbidden |

### Code samples for "Get project field for organization"

#### Request example

get/orgs/{org}/projectsV2/{project_number}/fields/{field_id}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/projectsV2/PROJECT_NUMBER/fields/FIELD_ID`

Response

-
-

`Status: 200``{
"id": 12345,
"node_id": "PVTF_lADOABCD1234567890",
"name": "Priority",
"data_type": "single_select",
"project_url": "https://api.github.com/projects/67890",
"options": [
{
"id": "option_1",
"name": {
"html": "Low",
"raw": "Low"
},
"color": "GREEN",
"description": {
"html": "Low priority items",
"raw": "Low priority items"
}
},
{
"id": "option_2",
"name": {
"html": "Medium",
"raw": "Medium"
},
"color": "YELLOW",
"description": {
"html": "Medium priority items",
"raw": "Medium priority items"
}
},
{
"id": "option_3",
"name": {
"html": "High",
"raw": "High"
},
"color": "RED",
"description": {
"html": "High priority items",
"raw": "High priority items"
}
}
],
"created_at": "2022-04-28T12:00:00Z",
"updated_at": "2022-04-28T12:00:00Z"
}`

## List project fields for user

List all fields for a specific user-owned project.

### Fine-grained access tokens for "List project fields for user"

This endpoint does not work with GitHub App user access tokens, GitHub App installation access tokens, or fine-grained personal access tokens.

### Parameters for "List project fields for user"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| project_numberintegerRequiredThe project's number. |
| usernamestringRequiredThe handle for the GitHub user account. |

| Name, Type, Description |
| --- |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| beforestringA cursor, as given in theLink header. If specified, the query only searches for results before this cursor. For more information, see "Using pagination in the REST API." |
| afterstringA cursor, as given in theLink header. If specified, the query only searches for results after this cursor. For more information, see "Using pagination in the REST API." |

### HTTP response status codes for "List project fields for user"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 304 | Not modified |
| 401 | Requires authentication |
| 403 | Forbidden |

### Code samples for "List project fields for user"

#### Request example

get/users/{username}/projectsV2/{project_number}/fields

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/users/USERNAME/projectsV2/PROJECT_NUMBER/fields`

Response

-
-

`Status: 200``[
{
"id": 12345,
"node_id": "PVTF_lADOABCD1234567890",
"name": "Priority",
"data_type": "single_select",
"project_url": "https://api.github.com/projects/67890",
"options": [
{
"id": "option_1",
"name": {
"html": "Low",
"raw": "Low"
},
"color": "GREEN",
"description": {
"html": "Low priority items",
"raw": "Low priority items"
}
},
{
"id": "option_2",
"name": {
"html": "Medium",
"raw": "Medium"
},
"color": "YELLOW",
"description": {
"html": "Medium priority items",
"raw": "Medium priority items"
}
},
{
"id": "option_3",
"name": {
"html": "High",
"raw": "High"
},
"color": "RED",
"description": {
"html": "High priority items",
"raw": "High priority items"
}
}
],
"created_at": "2022-04-28T12:00:00Z",
"updated_at": "2022-04-28T12:00:00Z"
},
{
"id": 67891,
"node_id": "PVTF_lADOABCD9876543210",
"name": "Status",
"data_type": "single_select",
"project_url": "https://api.github.com/projects/67890",
"options": [
{
"id": "option_4",
"name": {
"html": "Todo",
"raw": "Todo"
},
"color": "GRAY",
"description": {
"html": "Items to be worked on",
"raw": "Items to be worked on"
}
},
{
"id": "option_5",
"name": {
"html": "In Progress",
"raw": "In Progress"
},
"color": "BLUE",
"description": {
"html": "Items currently being worked on",
"raw": "Items currently being worked on"
}
},
{
"id": "option_6",
"name": {
"html": "Done",
"raw": "Done"
},
"color": "GREEN",
"description": {
"html": "Completed items",
"raw": "Completed items"
}
}
],
"created_at": "2022-04-29T10:30:00Z",
"updated_at": "2022-04-29T10:30:00Z"
},
{
"id": 24680,
"node_id": "PVTF_lADOABCD2468024680",
"name": "Team notes",
"data_type": "text",
"project_url": "https://api.github.com/projects/67890",
"created_at": "2022-05-15T08:00:00Z",
"updated_at": "2022-05-15T08:00:00Z"
},
{
"id": 13579,
"node_id": "PVTF_lADOABCD1357913579",
"name": "Story points",
"data_type": "number",
"project_url": "https://api.github.com/projects/67890",
"created_at": "2022-06-01T14:30:00Z",
"updated_at": "2022-06-01T14:30:00Z"
},
{
"id": 98765,
"node_id": "PVTF_lADOABCD9876598765",
"name": "Due date",
"data_type": "date",
"project_url": "https://api.github.com/projects/67890",
"created_at": "2022-06-10T09:15:00Z",
"updated_at": "2022-06-10T09:15:00Z"
},
{
"id": 11223,
"node_id": "PVTF_lADOABCD1122311223",
"name": "Sprint",
"data_type": "iteration",
"project_url": "https://api.github.com/projects/67890",
"configuration": {
"duration": 14,
"start_day": 1,
"iterations": [
{
"id": "iter_1",
"title": {
"html": "Sprint 1",
"raw": "Sprint 1"
},
"start_date": "2022-07-01",
"duration": 14
},
{
"id": "iter_2",
"title": {
"html": "Sprint 2",
"raw": "Sprint 2"
},
"start_date": "2022-07-15",
"duration": 14
}
]
},
"created_at": "2022-06-20T16:45:00Z",
"updated_at": "2022-06-20T16:45:00Z"
}
]`

## Add field to user owned project

Add a field to a specified user owned project.

### Fine-grained access tokens for "Add field to user owned project"

This endpoint does not work with GitHub App user access tokens, GitHub App installation access tokens, or fine-grained personal access tokens.

### Parameters for "Add field to user owned project"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| usernamestringRequiredThe handle for the GitHub user account. |
| project_numberintegerRequiredThe project's number. |

| Name, Type, Description |
| --- |
| namestringRequiredThe name of the field. |
| data_typestringRequiredThe field's data type.Value:iteration |
| single_select_optionsarray of objectsThe options available for single select fields. At least one option must be provided when creating a single select field. |
| Name, Type, DescriptionnamestringThe display name of the option.colorstringThe color associated with the option.Can be one of:BLUE,GRAY,GREEN,ORANGE,PINK,PURPLE,RED,YELLOWdescriptionstringThe description of the option. |
| Name, Type, Description |
| namestringThe display name of the option. |
| colorstringThe color associated with the option.Can be one of:BLUE,GRAY,GREEN,ORANGE,PINK,PURPLE,RED,YELLOW |
| descriptionstringThe description of the option. |
| iteration_configurationobjectRequiredThe configuration for iteration fields. |
| Name, Type, Descriptionstart_datestringThe start date of the first iteration.durationintegerThe default duration for iterations in days. Individual iterations can override this value.iterationsarray of objectsZero or more iterations for the field.Name, Type, DescriptiontitlestringThe title of the iteration.start_datestringThe start date of the iteration.durationintegerThe duration of the iteration in days. |
| Name, Type, Description |
| start_datestringThe start date of the first iteration. |
| durationintegerThe default duration for iterations in days. Individual iterations can override this value. |
| iterationsarray of objectsZero or more iterations for the field. |
| Name, Type, DescriptiontitlestringThe title of the iteration.start_datestringThe start date of the iteration.durationintegerThe duration of the iteration in days. |
| Name, Type, Description |
| titlestringThe title of the iteration. |
| start_datestringThe start date of the iteration. |
| durationintegerThe duration of the iteration in days. |

### HTTP response status codes for "Add field to user owned project"

| Status code | Description |
| --- | --- |
| 201 | Created |
| 304 | Not modified |
| 401 | Requires authentication |
| 403 | Forbidden |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Add field to user owned project"

#### Request examples

Select the example typeCreate a text fieldCreate a number fieldCreate a date fieldCreate a single select fieldCreate an iteration fieldpost/users/{username}/projectsV2/{project_number}/fields

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/users/USERNAME/projectsV2/PROJECT_NUMBER/fields \
  -d '{"name":"Team notes","data_type":"text"}'`

Response

-
-

`Status: 201``{
"id": 24680,
"node_id": "PVTF_lADOABCD2468024680",
"name": "Team notes",
"data_type": "text",
"project_url": "https://api.github.com/projects/67890",
"created_at": "2022-05-15T08:00:00Z",
"updated_at": "2022-05-15T08:00:00Z"
}`

## Get project field for user

Get a specific field for a user-owned project.

### Fine-grained access tokens for "Get project field for user"

This endpoint does not work with GitHub App user access tokens, GitHub App installation access tokens, or fine-grained personal access tokens.

### Parameters for "Get project field for user"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| project_numberintegerRequiredThe project's number. |
| field_idintegerRequiredThe unique identifier of the field. |
| usernamestringRequiredThe handle for the GitHub user account. |

### HTTP response status codes for "Get project field for user"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 304 | Not modified |
| 401 | Requires authentication |
| 403 | Forbidden |

### Code samples for "Get project field for user"

#### Request example

get/users/{username}/projectsV2/{project_number}/fields/{field_id}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/users/USERNAME/projectsV2/PROJECT_NUMBER/fields/FIELD_ID`

Response

-
-

`Status: 200``{
"id": 12345,
"node_id": "PVTF_lADOABCD1234567890",
"name": "Priority",
"data_type": "single_select",
"project_url": "https://api.github.com/projects/67890",
"options": [
{
"id": "option_1",
"name": {
"html": "Low",
"raw": "Low"
},
"color": "GREEN",
"description": {
"html": "Low priority items",
"raw": "Low priority items"
}
},
{
"id": "option_2",
"name": {
"html": "Medium",
"raw": "Medium"
},
"color": "YELLOW",
"description": {
"html": "Medium priority items",
"raw": "Medium priority items"
}
},
{
"id": "option_3",
"name": {
"html": "High",
"raw": "High"
},
"color": "RED",
"description": {
"html": "High priority items",
"raw": "High priority items"
}
}
],
"created_at": "2022-04-28T12:00:00Z",
"updated_at": "2022-04-28T12:00:00Z"
}`
