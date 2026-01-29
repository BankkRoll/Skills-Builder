# REST API endpoints for API Insights and more

# REST API endpoints for API Insights

> Use the REST API to view statistics for API usage in an organization.

## Get route stats by actor

Get API request count statistics for an actor broken down by route within a specified time frame.

### Fine-grained access tokens for "Get route stats by actor"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "API Insights" organization permissions (read)

### Parameters for "Get route stats by actor"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| actor_typestringRequiredThe type of the actorCan be one of:installation,classic_pat,fine_grained_pat,oauth_app,github_app_user_to_server |
| actor_idintegerRequiredThe ID of the actor |

| Name, Type, Description |
| --- |
| min_timestampstringRequiredThe minimum timestamp to query for stats. This is a timestamp inISO 8601format:YYYY-MM-DDTHH:MM:SSZ. |
| max_timestampstringThe maximum timestamp to query for stats. Defaults to the time 30 days ago. This is a timestamp inISO 8601format:YYYY-MM-DDTHH:MM:SSZ. |
| pageintegerThe page number of the results to fetch. For more information, see "Using pagination in the REST API."Default:1 |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| directionstringThe direction to sort the results by.Default:descCan be one of:asc,desc |
| sortarrayThe property to sort the results by. |
| api_route_substringstringProviding a substring will filter results where the API route contains the substring. This is a case-insensitive search. |

### HTTP response status codes for "Get route stats by actor"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "Get route stats by actor"

#### Request example

get/orgs/{org}/insights/api/route-stats/{actor_type}/{actor_id}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/orgs/ORG/insights/api/route-stats/ACTOR_TYPE/ACTOR_ID?min_timestamp=MIN_TIMESTAMP"`

Response

-
-

`Status: 200``[
{
"http_method": "GET",
"api_route": "/repositories/:repository_id",
"total_request_count": 544665,
"rate_limited_request_count": 13,
"last_request_timestamp": "2024-09-18T15:43:03Z",
"last_rate_limited_timestamp": "2024-09-18T06:30:09Z"
}
]`

## Get subject stats

Get API request statistics for all subjects within an organization within a specified time frame. Subjects can be users or GitHub Apps.

### Fine-grained access tokens for "Get subject stats"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "API Insights" organization permissions (read)

### Parameters for "Get subject stats"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| min_timestampstringRequiredThe minimum timestamp to query for stats. This is a timestamp inISO 8601format:YYYY-MM-DDTHH:MM:SSZ. |
| max_timestampstringThe maximum timestamp to query for stats. Defaults to the time 30 days ago. This is a timestamp inISO 8601format:YYYY-MM-DDTHH:MM:SSZ. |
| pageintegerThe page number of the results to fetch. For more information, see "Using pagination in the REST API."Default:1 |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| directionstringThe direction to sort the results by.Default:descCan be one of:asc,desc |
| sortarrayThe property to sort the results by. |
| subject_name_substringstringProviding a substring will filter results where the subject name contains the substring. This is a case-insensitive search. |

### HTTP response status codes for "Get subject stats"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "Get subject stats"

#### Request example

get/orgs/{org}/insights/api/subject-stats

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/orgs/ORG/insights/api/subject-stats?min_timestamp=MIN_TIMESTAMP"`

Response

-
-

`Status: 200``[
{
"subject_type": "installation",
"subject_id": 954453,
"subject_name": "GitHub Actions",
"integration_id": 124345,
"total_request_count": 544665,
"rate_limited_request_count": 13,
"last_request_timestamp": "2024-09-18T15:43:03Z",
"last_rate_limited_timestamp": "2024-09-18T06:30:09Z"
}
]`

## Get summary stats

Get overall statistics of API requests made within an organization by all users and apps within a specified time frame.

### Fine-grained access tokens for "Get summary stats"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "API Insights" organization permissions (read)

### Parameters for "Get summary stats"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| min_timestampstringRequiredThe minimum timestamp to query for stats. This is a timestamp inISO 8601format:YYYY-MM-DDTHH:MM:SSZ. |
| max_timestampstringThe maximum timestamp to query for stats. Defaults to the time 30 days ago. This is a timestamp inISO 8601format:YYYY-MM-DDTHH:MM:SSZ. |

### HTTP response status codes for "Get summary stats"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "Get summary stats"

#### Request example

get/orgs/{org}/insights/api/summary-stats

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/orgs/ORG/insights/api/summary-stats?min_timestamp=MIN_TIMESTAMP"`

Response

-
-

`Status: 200``{
"total_request_count": 34225,
"rate_limited_request_count": 23
}`

## Get summary stats by user

Get overall statistics of API requests within the organization for a user.

### Fine-grained access tokens for "Get summary stats by user"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "API Insights" organization permissions (read)

### Parameters for "Get summary stats by user"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| user_idstringRequiredThe ID of the user to query for stats |

| Name, Type, Description |
| --- |
| min_timestampstringRequiredThe minimum timestamp to query for stats. This is a timestamp inISO 8601format:YYYY-MM-DDTHH:MM:SSZ. |
| max_timestampstringThe maximum timestamp to query for stats. Defaults to the time 30 days ago. This is a timestamp inISO 8601format:YYYY-MM-DDTHH:MM:SSZ. |

### HTTP response status codes for "Get summary stats by user"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "Get summary stats by user"

#### Request example

get/orgs/{org}/insights/api/summary-stats/users/{user_id}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/orgs/ORG/insights/api/summary-stats/users/USER_ID?min_timestamp=MIN_TIMESTAMP"`

Response

-
-

`Status: 200``{
"total_request_count": 34225,
"rate_limited_request_count": 23
}`

## Get summary stats by actor

Get overall statistics of API requests within the organization made by a specific actor. Actors can be GitHub App installations, OAuth apps or other tokens on behalf of a user.

### Fine-grained access tokens for "Get summary stats by actor"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "API Insights" organization permissions (read)

### Parameters for "Get summary stats by actor"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| actor_typestringRequiredThe type of the actorCan be one of:installation,classic_pat,fine_grained_pat,oauth_app,github_app_user_to_server |
| actor_idintegerRequiredThe ID of the actor |

| Name, Type, Description |
| --- |
| min_timestampstringRequiredThe minimum timestamp to query for stats. This is a timestamp inISO 8601format:YYYY-MM-DDTHH:MM:SSZ. |
| max_timestampstringThe maximum timestamp to query for stats. Defaults to the time 30 days ago. This is a timestamp inISO 8601format:YYYY-MM-DDTHH:MM:SSZ. |

### HTTP response status codes for "Get summary stats by actor"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "Get summary stats by actor"

#### Request example

get/orgs/{org}/insights/api/summary-stats/{actor_type}/{actor_id}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/orgs/ORG/insights/api/summary-stats/ACTOR_TYPE/ACTOR_ID?min_timestamp=MIN_TIMESTAMP"`

Response

-
-

`Status: 200``{
"total_request_count": 34225,
"rate_limited_request_count": 23
}`

## Get time stats

Get the number of API requests and rate-limited requests made within an organization over a specified time period.

### Fine-grained access tokens for "Get time stats"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "API Insights" organization permissions (read)

### Parameters for "Get time stats"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| min_timestampstringRequiredThe minimum timestamp to query for stats. This is a timestamp inISO 8601format:YYYY-MM-DDTHH:MM:SSZ. |
| max_timestampstringThe maximum timestamp to query for stats. Defaults to the time 30 days ago. This is a timestamp inISO 8601format:YYYY-MM-DDTHH:MM:SSZ. |
| timestamp_incrementstringRequiredThe increment of time used to breakdown the query results (5m, 10m, 1h, etc.) |

### HTTP response status codes for "Get time stats"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "Get time stats"

#### Request example

get/orgs/{org}/insights/api/time-stats

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/orgs/ORG/insights/api/time-stats?min_timestamp=MIN_TIMESTAMP&timestamp_increment=TIMESTAMP_INCREMENT"`

Response

-
-

`Status: 200``[
{
"timestamp": "2024-09-11T15:00:00Z",
"total_request_count": 34225,
"rate_limited_request_count": 0
},
{
"timestamp": "2024-09-11T15:05:00Z",
"total_request_count": 10587,
"rate_limited_request_count": 18
},
{
"timestamp": "2024-09-11T15:10:00Z",
"total_request_count": 43587,
"rate_limited_request_count": 14
},
{
"timestamp": "2024-09-11T15:15:00Z",
"total_request_count": 19463,
"rate_limited_request_count": 4
},
{
"timestamp": "2024-09-11T15:20:00Z",
"total_request_count": 60542,
"rate_limited_request_count": 3
},
{
"timestamp": "2024-09-11T15:25:00Z",
"total_request_count": 55872,
"rate_limited_request_count": 23
}
]`

## Get time stats by user

Get the number of API requests and rate-limited requests made within an organization by a specific user over a specified time period.

### Fine-grained access tokens for "Get time stats by user"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "API Insights" organization permissions (read)

### Parameters for "Get time stats by user"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| user_idstringRequiredThe ID of the user to query for stats |

| Name, Type, Description |
| --- |
| min_timestampstringRequiredThe minimum timestamp to query for stats. This is a timestamp inISO 8601format:YYYY-MM-DDTHH:MM:SSZ. |
| max_timestampstringThe maximum timestamp to query for stats. Defaults to the time 30 days ago. This is a timestamp inISO 8601format:YYYY-MM-DDTHH:MM:SSZ. |
| timestamp_incrementstringRequiredThe increment of time used to breakdown the query results (5m, 10m, 1h, etc.) |

### HTTP response status codes for "Get time stats by user"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "Get time stats by user"

#### Request example

get/orgs/{org}/insights/api/time-stats/users/{user_id}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/orgs/ORG/insights/api/time-stats/users/USER_ID?min_timestamp=MIN_TIMESTAMP&timestamp_increment=TIMESTAMP_INCREMENT"`

Response

-
-

`Status: 200``[
{
"timestamp": "2024-09-11T15:00:00Z",
"total_request_count": 34225,
"rate_limited_request_count": 0
},
{
"timestamp": "2024-09-11T15:05:00Z",
"total_request_count": 10587,
"rate_limited_request_count": 18
},
{
"timestamp": "2024-09-11T15:10:00Z",
"total_request_count": 43587,
"rate_limited_request_count": 14
},
{
"timestamp": "2024-09-11T15:15:00Z",
"total_request_count": 19463,
"rate_limited_request_count": 4
},
{
"timestamp": "2024-09-11T15:20:00Z",
"total_request_count": 60542,
"rate_limited_request_count": 3
},
{
"timestamp": "2024-09-11T15:25:00Z",
"total_request_count": 55872,
"rate_limited_request_count": 23
}
]`

## Get time stats by actor

Get the number of API requests and rate-limited requests made within an organization by a specific actor within a specified time period.

### Fine-grained access tokens for "Get time stats by actor"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "API Insights" organization permissions (read)

### Parameters for "Get time stats by actor"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| actor_typestringRequiredThe type of the actorCan be one of:installation,classic_pat,fine_grained_pat,oauth_app,github_app_user_to_server |
| actor_idintegerRequiredThe ID of the actor |

| Name, Type, Description |
| --- |
| min_timestampstringRequiredThe minimum timestamp to query for stats. This is a timestamp inISO 8601format:YYYY-MM-DDTHH:MM:SSZ. |
| max_timestampstringThe maximum timestamp to query for stats. Defaults to the time 30 days ago. This is a timestamp inISO 8601format:YYYY-MM-DDTHH:MM:SSZ. |
| timestamp_incrementstringRequiredThe increment of time used to breakdown the query results (5m, 10m, 1h, etc.) |

### HTTP response status codes for "Get time stats by actor"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "Get time stats by actor"

#### Request example

get/orgs/{org}/insights/api/time-stats/{actor_type}/{actor_id}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/orgs/ORG/insights/api/time-stats/ACTOR_TYPE/ACTOR_ID?min_timestamp=MIN_TIMESTAMP&timestamp_increment=TIMESTAMP_INCREMENT"`

Response

-
-

`Status: 200``[
{
"timestamp": "2024-09-11T15:00:00Z",
"total_request_count": 34225,
"rate_limited_request_count": 0
},
{
"timestamp": "2024-09-11T15:05:00Z",
"total_request_count": 10587,
"rate_limited_request_count": 18
},
{
"timestamp": "2024-09-11T15:10:00Z",
"total_request_count": 43587,
"rate_limited_request_count": 14
},
{
"timestamp": "2024-09-11T15:15:00Z",
"total_request_count": 19463,
"rate_limited_request_count": 4
},
{
"timestamp": "2024-09-11T15:20:00Z",
"total_request_count": 60542,
"rate_limited_request_count": 3
},
{
"timestamp": "2024-09-11T15:25:00Z",
"total_request_count": 55872,
"rate_limited_request_count": 23
}
]`

## Get user stats

Get API usage statistics within an organization for a user broken down by the type of access.

### Fine-grained access tokens for "Get user stats"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "API Insights" organization permissions (read)

### Parameters for "Get user stats"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| user_idstringRequiredThe ID of the user to query for stats |

| Name, Type, Description |
| --- |
| min_timestampstringRequiredThe minimum timestamp to query for stats. This is a timestamp inISO 8601format:YYYY-MM-DDTHH:MM:SSZ. |
| max_timestampstringThe maximum timestamp to query for stats. Defaults to the time 30 days ago. This is a timestamp inISO 8601format:YYYY-MM-DDTHH:MM:SSZ. |
| pageintegerThe page number of the results to fetch. For more information, see "Using pagination in the REST API."Default:1 |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| directionstringThe direction to sort the results by.Default:descCan be one of:asc,desc |
| sortarrayThe property to sort the results by. |
| actor_name_substringstringProviding a substring will filter results where the actor name contains the substring. This is a case-insensitive search. |

### HTTP response status codes for "Get user stats"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "Get user stats"

#### Request example

get/orgs/{org}/insights/api/user-stats/{user_id}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/orgs/ORG/insights/api/user-stats/USER_ID?min_timestamp=MIN_TIMESTAMP"`

Response

-
-

`Status: 200``[
{
"actor_type": "oauth_app",
"actor_id": 954453,
"actor_name": "GitHub Actions",
"oauth_application_id": 1245,
"total_request_count": 544665,
"rate_limited_request_count": 13,
"last_request_timestamp": "2024-09-18T15:43:03Z",
"last_rate_limited_timestamp": "2024-09-18T06:30:09Z"
}
]`

---

# REST API endpoints for artifact metadata

> Use these endpoints to retrieve and manage metadata for artifacts in your organization. Artifact metadata provides information about build artifacts, their provenance, and related details.

You can use these endpoints to upload storage and deployment records for software that your organization builds with GitHub Actions. The records are displayed on the organization's linked artifacts page. See [About linked artifacts](https://docs.github.com/en/code-security/concepts/supply-chain-security/linked-artifacts).

---

# REST API endpoints for artifact attestations

> Use the REST API to interact with artifact attestations.

## List attestations by bulk subject digests

List a collection of artifact attestations associated with any entry in a list of subject digests owned by an organization.

The collection of attestations returned by this endpoint is filtered according to the authenticated user's permissions; if the authenticated user cannot read a repository, the attestations associated with that repository will not be included in the response. In addition, when using a fine-grained access token the `attestations:read` permission is required.

**Please note:** in order to offer meaningful security benefits, an attestation's signature and timestamps **must** be cryptographically verified, and the identity of the attestation signer **must** be validated. Attestations can be verified using the [GitHub CLIattestation verifycommand](https://cli.github.com/manual/gh_attestation_verify). For more information, see [our guide on how to use artifact attestations to establish a build's provenance](https://docs.github.com/actions/security-guides/using-artifact-attestations-to-establish-provenance-for-builds).

### Fine-grained access tokens for "List attestations by bulk subject digests"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token does not require any permissions.

This endpoint can be used without authentication if only public resources are requested.

### Parameters for "List attestations by bulk subject digests"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| beforestringA cursor, as given in theLink header. If specified, the query only searches for results before this cursor. For more information, see "Using pagination in the REST API." |
| afterstringA cursor, as given in theLink header. If specified, the query only searches for results after this cursor. For more information, see "Using pagination in the REST API." |

| Name, Type, Description |
| --- |
| subject_digestsarray of stringsRequiredList of subject digests to fetch attestations for. |
| predicate_typestringOptional filter for fetching attestations with a given predicate type.
This option acceptsprovenance,sbom,release, or freeform text
for custom predicate types. |

### HTTP response status codes for "List attestations by bulk subject digests"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "List attestations by bulk subject digests"

#### Request example

post/orgs/{org}/attestations/bulk-list

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/attestations/bulk-list \
  -d '{"subject_digests":["sha256:abc123","sha512:def456"]}'`

Response

-
-

`Status: 200``{
"attestations_subject_digests": [
{
"sha256:abc": [
{
"bundle": {
"mediaType": "application/vnd.dev.sigstore.bundle.v0.3+json",
"verificationMaterial": {
"tlogEntries": [
{
"logIndex": "97913980",
"logId": {
"keyId": "wNI9atQGlz+VWfO6LRygH4QUfY/8W4RFwiT5i5WRgB0="
},
"kindVersion": {
"kind": "dsse",
"version": "0.0.1"
},
"integratedTime": "1716998992",
"inclusionPromise": {
"signedEntryTimestamp": "MEYCIQCeEsQAy+qXtULkh52wbnHrkt2R2JQ05P9STK/xmdpQ2AIhANiG5Gw6cQiMnwvUz1+9UKtG/vlC8dduq07wsFOViwSL"
},
"inclusionProof": {
"logIndex": "93750549",
"rootHash": "KgKiXoOl8rM5d4y6Xlbm2QLftvj/FYvTs6z7dJlNO60=",
"treeSize": "93750551",
"hashes": [
"8LI21mzwxnUSo0fuZeFsUrz2ujZ4QAL+oGeTG+5toZg=",
"nCb369rcIytNhGwWoqBv+eV49X3ZKpo/HJGKm9V+dck=",
"hnNQ9mUdSwYCfdV21pd87NucrdRRNZATowlaRR1hJ4A=",
"MBhhK33vlD4Tq/JKgAaXUI4VjmosWKe6+7RNpQ2ncNM=",
"XKWUE3stvGV1OHsIGiCGfn047Ok6uD4mFkh7BaicaEc=",
"Tgve40VPFfuei+0nhupdGpfPPR+hPpZjxgTiDT8WNoY=",
"wV+S/7tLtYGzkLaSb6UDqexNyhMvumHK/RpTNvEZuLU=",
"uwaWufty6sn6XqO1Tb9M3Vz6sBKPu0HT36mStxJNd7s=",
"jUfeMOXQP0XF1JAnCEETVbfRKMUwCzrVUzYi8vnDMVs=",
"xQKjzJAwwdlQG/YUYBKPXxbCmhMYKo1wnv+6vDuKWhQ=",
"cX3Agx+hP66t1ZLbX/yHbfjU46/3m/VAmWyG/fhxAVc=",
"sjohk/3DQIfXTgf/5XpwtdF7yNbrf8YykOMHr1CyBYQ=",
"98enzMaC+x5oCMvIZQA5z8vu2apDMCFvE/935NfuPw8="
],
"checkpoint": {
"envelope": "rekor.sigstore.dev - 2605736670972794746\\n93750551\\nKgKiXoOl8rM5d4y6Xlbm2QLftvj/FYvTs6z7dJlNO60=\\n\\n— rekor.sigstore.dev wNI9ajBEAiBkLzdjY8A9HReU7rmtjwZ+JpSuYtEr9SmvSwUIW7FBjgIgKo+vhkW3tqc+gc8fw9gza3xLoncA8a+MTaJYCaLGA9c=\\n"
}
},
"canonicalizedBody": "eyJhcGlWZXJzaW9uIjoiMC4wLjEiLCJraW5kIjoiZHNzZSIsInNwZWMiOnsiZW52ZWxvcGVIYXNoIjp7ImFsZ29yaXRobSI6InNoYTI1NiIsInZhbHVlIjoiM2I1YzkwNDk5MGFiYzE4NjI1ZWE3Njg4MzE1OGEwZmI4MTEwMjM4MGJkNjQwZjI5OWJlMzYwZWVkOTMxNjYwYiJ9LCJwYXlsb2FkSGFzaCI6eyJhbGdvcml0aG0iOiJzaGEyNTYiLCJ2YWx1ZSI6IjM4ZGNlZDJjMzE1MGU2OTQxMDViYjZiNDNjYjY3NzBiZTYzZDdhNGM4NjNiMTc2YTkwMmU1MGQ5ZTAyN2ZiMjMifSwic2lnbmF0dXJlcyI6W3sic2lnbmF0dXJlIjoiTUVRQ0lFR0lHQW03Z1pWTExwc3JQY2puZEVqaXVjdEUyL2M5K2o5S0d2YXp6M3JsQWlBZDZPMTZUNWhrelJNM0liUlB6bSt4VDQwbU5RWnhlZmQ3bGFEUDZ4MlhMUT09IiwidmVyaWZpZXIiOiJMUzB0TFMxQ1JVZEpUaUJEUlZKVVNVWkpRMEZVUlMwdExTMHRDazFKU1VkcVZFTkRRbWhUWjBGM1NVSkJaMGxWVjFsNGNVdHpjazFUTTFOMmJEVkphalZQUkdaQ1owMUtUeTlKZDBObldVbExiMXBKZW1vd1JVRjNUWGNLVG5wRlZrMUNUVWRCTVZWRlEyaE5UV015Ykc1ak0xSjJZMjFWZFZwSFZqSk5ValIzU0VGWlJGWlJVVVJGZUZaNllWZGtlbVJIT1hsYVV6RndZbTVTYkFwamJURnNXa2RzYUdSSFZYZElhR05PVFdwUmQwNVVTVFZOVkZsM1QxUlZlVmRvWTA1TmFsRjNUbFJKTlUxVVdYaFBWRlY1VjJwQlFVMUdhM2RGZDFsSUNrdHZXa2w2YWpCRFFWRlpTVXR2V2tsNmFqQkVRVkZqUkZGblFVVmtiV2RvVGs1M00yNVZMMHQxWlZGbmMzQkhTRmMzWjJnNVdFeEVMMWRrU1RoWlRVSUtLekJ3TUZZMGJ6RnJTRzgyWTAweGMwUktaM0pEWjFCUlZYcDRjSFZaZFc4cmVIZFFTSGxzTDJ0RWVXWXpSVXhxYTJGUFEwSlVUWGRuWjFWMlRVRTBSd3BCTVZWa1JIZEZRaTkzVVVWQmQwbElaMFJCVkVKblRsWklVMVZGUkVSQlMwSm5aM0pDWjBWR1FsRmpSRUY2UVdSQ1owNVdTRkUwUlVablVWVnhaa05RQ25aWVMwRjJVelJEWkdoUk1taGlXbGRLVTA5RmRsWnZkMGgzV1VSV1VqQnFRa0puZDBadlFWVXpPVkJ3ZWpGWmEwVmFZalZ4VG1wd1MwWlhhWGhwTkZrS1drUTRkMWRuV1VSV1VqQlNRVkZJTDBKR1FYZFViMXBOWVVoU01HTklUVFpNZVRsdVlWaFNiMlJYU1hWWk1qbDBUREpPYzJGVE9XcGlSMnQyVEcxa2NBcGtSMmd4V1drNU0ySXpTbkphYlhoMlpETk5kbHBIVm5kaVJ6azFZbGRXZFdSRE5UVmlWM2hCWTIxV2JXTjVPVzlhVjBaclkzazVNR051Vm5WaGVrRTFDa0puYjNKQ1owVkZRVmxQTDAxQlJVSkNRM1J2WkVoU2QyTjZiM1pNTTFKMllUSldkVXh0Um1wa1IyeDJZbTVOZFZveWJEQmhTRlpwWkZoT2JHTnRUbllLWW01U2JHSnVVWFZaTWpsMFRVSTRSME5wYzBkQlVWRkNaemM0ZDBGUlNVVkZXR1IyWTIxMGJXSkhPVE5ZTWxKd1l6TkNhR1JIVG05TlJGbEhRMmx6UndwQlVWRkNaemM0ZDBGUlRVVkxSMXBvV2xkWmVWcEhVbXRQUkVacFRVUmplazVxWXpCUFJGRjRUVEpGTTFsNldUQk9iVTVyVFVkS2JWbDZTVEpaZWtGM0NsbFVRWGRIUVZsTFMzZFpRa0pCUjBSMmVrRkNRa0ZSUzFKSFZuZGlSemsxWWxkV2RXUkVRVlpDWjI5eVFtZEZSVUZaVHk5TlFVVkdRa0ZrYW1KSGEzWUtXVEo0Y0UxQ05FZERhWE5IUVZGUlFtYzNPSGRCVVZsRlJVaEtiRnB1VFhaaFIxWm9Xa2hOZG1SSVNqRmliWE4zVDNkWlMwdDNXVUpDUVVkRWRucEJRZ3BEUVZGMFJFTjBiMlJJVW5kamVtOTJURE5TZG1FeVZuVk1iVVpxWkVkc2RtSnVUWFZhTW13d1lVaFdhV1JZVG14amJVNTJZbTVTYkdKdVVYVlpNamwwQ2sxR2QwZERhWE5IUVZGUlFtYzNPSGRCVVd0RlZHZDRUV0ZJVWpCalNFMDJUSGs1Ym1GWVVtOWtWMGwxV1RJNWRFd3lUbk5oVXpscVlrZHJka3h0WkhBS1pFZG9NVmxwT1ROaU0wcHlXbTE0ZG1RelRYWmFSMVozWWtjNU5XSlhWblZrUXpVMVlsZDRRV050Vm0xamVUbHZXbGRHYTJONU9UQmpibFoxWVhwQk5BcENaMjl5UW1kRlJVRlpUeTlOUVVWTFFrTnZUVXRIV21oYVYxbDVXa2RTYTA5RVJtbE5SR042VG1wak1FOUVVWGhOTWtVeldYcFpNRTV0VG10TlIwcHRDbGw2U1RKWmVrRjNXVlJCZDBoUldVdExkMWxDUWtGSFJIWjZRVUpEZDFGUVJFRXhibUZZVW05a1YwbDBZVWM1ZW1SSFZtdE5RMjlIUTJselIwRlJVVUlLWnpjNGQwRlJkMFZJUVhkaFlVaFNNR05JVFRaTWVUbHVZVmhTYjJSWFNYVlpNamwwVERKT2MyRlRPV3BpUjJ0M1QwRlpTMHQzV1VKQ1FVZEVkbnBCUWdwRVVWRnhSRU5vYlZsWFZtMU5iVkpyV2tSbmVGbHFRVE5OZWxrelRrUm5NRTFVVG1oT01rMHlUa1JhYWxwRVFtbGFiVTE1VG0xTmQwMUhSWGROUTBGSENrTnBjMGRCVVZGQ1p6YzRkMEZSTkVWRlozZFJZMjFXYldONU9XOWFWMFpyWTNrNU1HTnVWblZoZWtGYVFtZHZja0puUlVWQldVOHZUVUZGVUVKQmMwMEtRMVJKZUUxcVdYaE5la0V3VDFSQmJVSm5iM0pDWjBWRlFWbFBMMDFCUlZGQ1FtZE5SbTFvTUdSSVFucFBhVGgyV2pKc01HRklWbWxNYlU1MllsTTVhZ3BpUjJ0M1IwRlpTMHQzV1VKQ1FVZEVkbnBCUWtWUlVVdEVRV2N4VDFSamQwNUVZM2hOVkVKalFtZHZja0puUlVWQldVOHZUVUZGVTBKRk5FMVVSMmd3Q21SSVFucFBhVGgyV2pKc01HRklWbWxNYlU1MllsTTVhbUpIYTNaWk1uaHdUSGsxYm1GWVVtOWtWMGwyWkRJNWVXRXlXbk5pTTJSNlRESlNiR05IZUhZS1pWY3hiR0p1VVhWbFZ6RnpVVWhLYkZwdVRYWmhSMVpvV2toTmRtUklTakZpYlhOM1QwRlpTMHQzV1VKQ1FVZEVkbnBCUWtWM1VYRkVRMmh0V1ZkV2JRcE5iVkpyV2tSbmVGbHFRVE5OZWxrelRrUm5NRTFVVG1oT01rMHlUa1JhYWxwRVFtbGFiVTE1VG0xTmQwMUhSWGROUTBWSFEybHpSMEZSVVVKbk56aDNDa0ZTVVVWRmQzZFNaREk1ZVdFeVduTmlNMlJtV2tkc2VtTkhSakJaTW1kM1ZGRlpTMHQzV1VKQ1FVZEVkbnBCUWtaUlVTOUVSREZ2WkVoU2QyTjZiM1lLVERKa2NHUkhhREZaYVRWcVlqSXdkbGt5ZUhCTU1rNXpZVk01YUZrelVuQmlNalY2VEROS01XSnVUWFpQVkVrMFQxUkJNMDVVWXpGTmFUbG9aRWhTYkFwaVdFSXdZM2s0ZUUxQ1dVZERhWE5IUVZGUlFtYzNPSGRCVWxsRlEwRjNSMk5JVm1saVIyeHFUVWxIVEVKbmIzSkNaMFZGUVdSYU5VRm5VVU5DU0RCRkNtVjNRalZCU0dOQk0xUXdkMkZ6WWtoRlZFcHFSMUkwWTIxWFl6TkJjVXBMV0hKcVpWQkxNeTlvTkhCNVowTTRjRGR2TkVGQlFVZFFlRkl4ZW1KblFVRUtRa0ZOUVZORVFrZEJhVVZCS3pobmJGRkplRTlCYUZoQ1FVOVRObE1yT0ZweGQwcGpaSGQzVTNJdlZGZHBhSE16WkV4eFZrRjJiME5KVVVSaWVUbG9NUXBKWTNWRVJYSXJlbk5YYVV3NFVIYzFRMU5VZEd0c2RFbzBNakZ6UlRneFZuWjFOa0Z3VkVGTFFtZG5jV2hyYWs5UVVWRkVRWGRPYmtGRVFtdEJha0VyQ2tSSU4xQXJhR2cwVmtoWFprTlhXSFJ5UzFSdlFrdDFZa0pyUzNCbVYwTlpVWGhxV0UweWRsWXZibEJ4WWxwR1dVOVdXazlpWlRaQlRuSm5lV1J2V1VNS1RVWlZUV0l6ZUhwelJrNVJXWFp6UlZsUGFUSkxibkoyUmpCMFoyOXdiVmhIVm05NmJsb3JjUzh5UVVsRVZ6bEdNVVUzV1RaWk1EWXhaVzkxUVZsa1NBcFhkejA5Q2kwdExTMHRSVTVFSUVORlVsUkpSa2xEUVZSRkxTMHRMUzBLIn1dfX0="
}
],
"timestampVerificationData": {},
"certificate": {
"rawBytes": "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"
}
},
"dsseEnvelope": {
"payload": "eyJfdHlwZSI6Imh0dHBzOi8vaW4tdG90by5pby9TdGF0ZW1lbnQvdjEiLCJzdWJqZWN0IjpbeyJuYW1lIjoiZ2hfMi41MC4wX3dpbmRvd3NfYXJtNjQuemlwIiwiZGlnZXN0Ijp7InNoYTI1NiI6IjhhYWQxMjBiNDE2Mzg2YjQyNjllZjYyYzhmZGViY2FkMzFhNzA4NDcyOTc4MTdhMTQ5ZGFmOTI3ZWRjODU1NDgifX1dLCJwcmVkaWNhdGVUeXBlIjoiaHR0cHM6Ly9zbHNhLmRldi9wcm92ZW5hbmNlL3YxIiwicHJlZGljYXRlIjp7ImJ1aWxkRGVmaW5pdGlvbiI6eyJidWlsZFR5cGUiOiJodHRwczovL3Nsc2EtZnJhbWV3b3JrLmdpdGh1Yi5pby9naXRodWItYWN0aW9ucy1idWlsZHR5cGVzL3dvcmtmbG93L3YxIiwiZXh0ZXJuYWxQYXJhbWV0ZXJzIjp7IndvcmtmbG93Ijp7InJlZiI6InJlZnMvaGVhZHMvdHJ1bmsiLCJyZXBvc2l0b3J5IjoiaHR0cHM6Ly9naXRodWIuY29tL2NsaS9jbGkiLCJwYXRoIjoiLmdpdGh1Yi93b3JrZmxvd3MvZGVwbG95bWVudC55bWwifX0sImludGVybmFsUGFyYW1ldGVycyI6eyJnaXRodWIiOnsiZXZlbnRfbmFtZSI6IndvcmtmbG93X2Rpc3BhdGNoIiwicmVwb3NpdG9yeV9pZCI6IjIxMjYxMzA0OSIsInJlcG9zaXRvcnlfb3duZXJfaWQiOiI1OTcwNDcxMSJ9fSwicmVzb2x2ZWREZXBlbmRlbmNpZXMiOlt7InVyaSI6ImdpdCtodHRwczovL2dpdGh1Yi5jb20vY2xpL2NsaUByZWZzL2hlYWRzL3RydW5rIiwiZGlnZXN0Ijp7ImdpdENvbW1pdCI6ImZhZWYyZGRkODFiMDczNjc0ODQxM2E3YzY0NmNkMGJmYzI2YzAwYTAifX1dfSwicnVuRGV0YWlscyI6eyJidWlsZGVyIjp7ImlkIjoiaHR0cHM6Ly9naXRodWIuY29tL2FjdGlvbnMvcnVubmVyL2dpdGh1Yi1ob3N0ZWQifSwibWV0YWRhdGEiOnsiaW52b2NhdGlvbklkIjoiaHR0cHM6Ly9naXRodWIuY29tL2NsaS9jbGkvYWN0aW9ucy9ydW5zLzkyODkwNzU3NTIvYXR0ZW1wdHMvMSJ9fX19",
"payloadType": "application/vnd.in-toto+json",
"signatures": [
{
"sig": "MEQCIEGIGAm7gZVLLpsrPcjndEjiuctE2/c9+j9KGvazz3rlAiAd6O16T5hkzRM3IbRPzm+xT40mNQZxefd7laDP6x2XLQ=="
}
]
}
},
"repository_id": 1
},
{
"bundle": {
"mediaType": "application/vnd.dev.sigstore.bundle.v0.3+json",
"verificationMaterial": {
"tlogEntries": [
{
"logIndex": "97913980",
"logId": {
"keyId": "wNI9atQGlz+VWfO6LRygH4QUfY/8W4RFwiT5i5WRgB0="
},
"kindVersion": {
"kind": "dsse",
"version": "0.0.1"
},
"integratedTime": "1716998992",
"inclusionPromise": {
"signedEntryTimestamp": "MEYCIQCeEsQAy+qXtULkh52wbnHrkt2R2JQ05P9STK/xmdpQ2AIhANiG5Gw6cQiMnwvUz1+9UKtG/vlC8dduq07wsFOViwSL"
},
"inclusionProof": {
"logIndex": "93750549",
"rootHash": "KgKiXoOl8rM5d4y6Xlbm2QLftvj/FYvTs6z7dJlNO60=",
"treeSize": "93750551",
"hashes": [
"8LI21mzwxnUSo0fuZeFsUrz2ujZ4QAL+oGeTG+5toZg=",
"nCb369rcIytNhGwWoqBv+eV49X3ZKpo/HJGKm9V+dck=",
"hnNQ9mUdSwYCfdV21pd87NucrdRRNZATowlaRR1hJ4A=",
"MBhhK33vlD4Tq/JKgAaXUI4VjmosWKe6+7RNpQ2ncNM=",
"XKWUE3stvGV1OHsIGiCGfn047Ok6uD4mFkh7BaicaEc=",
"Tgve40VPFfuei+0nhupdGpfPPR+hPpZjxgTiDT8WNoY=",
"wV+S/7tLtYGzkLaSb6UDqexNyhMvumHK/RpTNvEZuLU=",
"uwaWufty6sn6XqO1Tb9M3Vz6sBKPu0HT36mStxJNd7s=",
"jUfeMOXQP0XF1JAnCEETVbfRKMUwCzrVUzYi8vnDMVs=",
"xQKjzJAwwdlQG/YUYBKPXxbCmhMYKo1wnv+6vDuKWhQ=",
"cX3Agx+hP66t1ZLbX/yHbfjU46/3m/VAmWyG/fhxAVc=",
"sjohk/3DQIfXTgf/5XpwtdF7yNbrf8YykOMHr1CyBYQ=",
"98enzMaC+x5oCMvIZQA5z8vu2apDMCFvE/935NfuPw8="
],
"checkpoint": {
"envelope": "rekor.sigstore.dev - 2605736670972794746\\n93750551\\nKgKiXoOl8rM5d4y6Xlbm2QLftvj/FYvTs6z7dJlNO60=\\n\\n— rekor.sigstore.dev wNI9ajBEAiBkLzdjY8A9HReU7rmtjwZ+JpSuYtEr9SmvSwUIW7FBjgIgKo+vhkW3tqc+gc8fw9gza3xLoncA8a+MTaJYCaLGA9c=\\n"
}
},
"canonicalizedBody": "eyJhcGlWZXJzaW9uIjoiMC4wLjEiLCJraW5kIjoiZHNzZSIsInNwZWMiOnsiZW52ZWxvcGVIYXNoIjp7ImFsZ29yaXRobSI6InNoYTI1NiIsInZhbHVlIjoiM2I1YzkwNDk5MGFiYzE4NjI1ZWE3Njg4MzE1OGEwZmI4MTEwMjM4MGJkNjQwZjI5OWJlMzYwZWVkOTMxNjYwYiJ9LCJwYXlsb2FkSGFzaCI6eyJhbGdvcml0aG0iOiJzaGEyNTYiLCJ2YWx1ZSI6IjM4ZGNlZDJjMzE1MGU2OTQxMDViYjZiNDNjYjY3NzBiZTYzZDdhNGM4NjNiMTc2YTkwMmU1MGQ5ZTAyN2ZiMjMifSwic2lnbmF0dXJlcyI6W3sic2lnbmF0dXJlIjoiTUVRQ0lFR0lHQW03Z1pWTExwc3JQY2puZEVqaXVjdEUyL2M5K2o5S0d2YXp6M3JsQWlBZDZPMTZUNWhrelJNM0liUlB6bSt4VDQwbU5RWnhlZmQ3bGFEUDZ4MlhMUT09IiwidmVyaWZpZXIiOiJMUzB0TFMxQ1JVZEpUaUJEUlZKVVNVWkpRMEZVUlMwdExTMHRDazFKU1VkcVZFTkRRbWhUWjBGM1NVSkJaMGxWVjFsNGNVdHpjazFUTTFOMmJEVkphalZQUkdaQ1owMUtUeTlKZDBObldVbExiMXBKZW1vd1JVRjNUWGNLVG5wRlZrMUNUVWRCTVZWRlEyaE5UV015Ykc1ak0xSjJZMjFWZFZwSFZqSk5ValIzU0VGWlJGWlJVVVJGZUZaNllWZGtlbVJIT1hsYVV6RndZbTVTYkFwamJURnNXa2RzYUdSSFZYZElhR05PVFdwUmQwNVVTVFZOVkZsM1QxUlZlVmRvWTA1TmFsRjNUbFJKTlUxVVdYaFBWRlY1VjJwQlFVMUdhM2RGZDFsSUNrdHZXa2w2YWpCRFFWRlpTVXR2V2tsNmFqQkVRVkZqUkZGblFVVmtiV2RvVGs1M00yNVZMMHQxWlZGbmMzQkhTRmMzWjJnNVdFeEVMMWRrU1RoWlRVSUtLekJ3TUZZMGJ6RnJTRzgyWTAweGMwUktaM0pEWjFCUlZYcDRjSFZaZFc4cmVIZFFTSGxzTDJ0RWVXWXpSVXhxYTJGUFEwSlVUWGRuWjFWMlRVRTBSd3BCTVZWa1JIZEZRaTkzVVVWQmQwbElaMFJCVkVKblRsWklVMVZGUkVSQlMwSm5aM0pDWjBWR1FsRmpSRUY2UVdSQ1owNVdTRkUwUlVablVWVnhaa05RQ25aWVMwRjJVelJEWkdoUk1taGlXbGRLVTA5RmRsWnZkMGgzV1VSV1VqQnFRa0puZDBadlFWVXpPVkJ3ZWpGWmEwVmFZalZ4VG1wd1MwWlhhWGhwTkZrS1drUTRkMWRuV1VSV1VqQlNRVkZJTDBKR1FYZFViMXBOWVVoU01HTklUVFpNZVRsdVlWaFNiMlJYU1hWWk1qbDBUREpPYzJGVE9XcGlSMnQyVEcxa2NBcGtSMmd4V1drNU0ySXpTbkphYlhoMlpETk5kbHBIVm5kaVJ6azFZbGRXZFdSRE5UVmlWM2hCWTIxV2JXTjVPVzlhVjBaclkzazVNR051Vm5WaGVrRTFDa0puYjNKQ1owVkZRVmxQTDAxQlJVSkNRM1J2WkVoU2QyTjZiM1pNTTFKMllUSldkVXh0Um1wa1IyeDJZbTVOZFZveWJEQmhTRlpwWkZoT2JHTnRUbllLWW01U2JHSnVVWFZaTWpsMFRVSTRSME5wYzBkQlVWRkNaemM0ZDBGUlNVVkZXR1IyWTIxMGJXSkhPVE5ZTWxKd1l6TkNhR1JIVG05TlJGbEhRMmx6UndwQlVWRkNaemM0ZDBGUlRVVkxSMXBvV2xkWmVWcEhVbXRQUkVacFRVUmplazVxWXpCUFJGRjRUVEpGTTFsNldUQk9iVTVyVFVkS2JWbDZTVEpaZWtGM0NsbFVRWGRIUVZsTFMzZFpRa0pCUjBSMmVrRkNRa0ZSUzFKSFZuZGlSemsxWWxkV2RXUkVRVlpDWjI5eVFtZEZSVUZaVHk5TlFVVkdRa0ZrYW1KSGEzWUtXVEo0Y0UxQ05FZERhWE5IUVZGUlFtYzNPSGRCVVZsRlJVaEtiRnB1VFhaaFIxWm9Xa2hOZG1SSVNqRmliWE4zVDNkWlMwdDNXVUpDUVVkRWRucEJRZ3BEUVZGMFJFTjBiMlJJVW5kamVtOTJURE5TZG1FeVZuVk1iVVpxWkVkc2RtSnVUWFZhTW13d1lVaFdhV1JZVG14amJVNTJZbTVTYkdKdVVYVlpNamwwQ2sxR2QwZERhWE5IUVZGUlFtYzNPSGRCVVd0RlZHZDRUV0ZJVWpCalNFMDJUSGs1Ym1GWVVtOWtWMGwxV1RJNWRFd3lUbk5oVXpscVlrZHJka3h0WkhBS1pFZG9NVmxwT1ROaU0wcHlXbTE0ZG1RelRYWmFSMVozWWtjNU5XSlhWblZrUXpVMVlsZDRRV050Vm0xamVUbHZXbGRHYTJONU9UQmpibFoxWVhwQk5BcENaMjl5UW1kRlJVRlpUeTlOUVVWTFFrTnZUVXRIV21oYVYxbDVXa2RTYTA5RVJtbE5SR042VG1wak1FOUVVWGhOTWtVeldYcFpNRTV0VG10TlIwcHRDbGw2U1RKWmVrRjNXVlJCZDBoUldVdExkMWxDUWtGSFJIWjZRVUpEZDFGUVJFRXhibUZZVW05a1YwbDBZVWM1ZW1SSFZtdE5RMjlIUTJselIwRlJVVUlLWnpjNGQwRlJkMFZJUVhkaFlVaFNNR05JVFRaTWVUbHVZVmhTYjJSWFNYVlpNamwwVERKT2MyRlRPV3BpUjJ0M1QwRlpTMHQzV1VKQ1FVZEVkbnBCUWdwRVVWRnhSRU5vYlZsWFZtMU5iVkpyV2tSbmVGbHFRVE5OZWxrelRrUm5NRTFVVG1oT01rMHlUa1JhYWxwRVFtbGFiVTE1VG0xTmQwMUhSWGROUTBGSENrTnBjMGRCVVZGQ1p6YzRkMEZSTkVWRlozZFJZMjFXYldONU9XOWFWMFpyWTNrNU1HTnVWblZoZWtGYVFtZHZja0puUlVWQldVOHZUVUZGVUVKQmMwMEtRMVJKZUUxcVdYaE5la0V3VDFSQmJVSm5iM0pDWjBWRlFWbFBMMDFCUlZGQ1FtZE5SbTFvTUdSSVFucFBhVGgyV2pKc01HRklWbWxNYlU1MllsTTVhZ3BpUjJ0M1IwRlpTMHQzV1VKQ1FVZEVkbnBCUWtWUlVVdEVRV2N4VDFSamQwNUVZM2hOVkVKalFtZHZja0puUlVWQldVOHZUVUZGVTBKRk5FMVVSMmd3Q21SSVFucFBhVGgyV2pKc01HRklWbWxNYlU1MllsTTVhbUpIYTNaWk1uaHdUSGsxYm1GWVVtOWtWMGwyWkRJNWVXRXlXbk5pTTJSNlRESlNiR05IZUhZS1pWY3hiR0p1VVhWbFZ6RnpVVWhLYkZwdVRYWmhSMVpvV2toTmRtUklTakZpYlhOM1QwRlpTMHQzV1VKQ1FVZEVkbnBCUWtWM1VYRkVRMmh0V1ZkV2JRcE5iVkpyV2tSbmVGbHFRVE5OZWxrelRrUm5NRTFVVG1oT01rMHlUa1JhYWxwRVFtbGFiVTE1VG0xTmQwMUhSWGROUTBWSFEybHpSMEZSVVVKbk56aDNDa0ZTVVVWRmQzZFNaREk1ZVdFeVduTmlNMlJtV2tkc2VtTkhSakJaTW1kM1ZGRlpTMHQzV1VKQ1FVZEVkbnBCUWtaUlVTOUVSREZ2WkVoU2QyTjZiM1lLVERKa2NHUkhhREZaYVRWcVlqSXdkbGt5ZUhCTU1rNXpZVk01YUZrelVuQmlNalY2VEROS01XSnVUWFpQVkVrMFQxUkJNMDVVWXpGTmFUbG9aRWhTYkFwaVdFSXdZM2s0ZUUxQ1dVZERhWE5IUVZGUlFtYzNPSGRCVWxsRlEwRjNSMk5JVm1saVIyeHFUVWxIVEVKbmIzSkNaMFZGUVdSYU5VRm5VVU5DU0RCRkNtVjNRalZCU0dOQk0xUXdkMkZ6WWtoRlZFcHFSMUkwWTIxWFl6TkJjVXBMV0hKcVpWQkxNeTlvTkhCNVowTTRjRGR2TkVGQlFVZFFlRkl4ZW1KblFVRUtRa0ZOUVZORVFrZEJhVVZCS3pobmJGRkplRTlCYUZoQ1FVOVRObE1yT0ZweGQwcGpaSGQzVTNJdlZGZHBhSE16WkV4eFZrRjJiME5KVVVSaWVUbG9NUXBKWTNWRVJYSXJlbk5YYVV3NFVIYzFRMU5VZEd0c2RFbzBNakZ6UlRneFZuWjFOa0Z3VkVGTFFtZG5jV2hyYWs5UVVWRkVRWGRPYmtGRVFtdEJha0VyQ2tSSU4xQXJhR2cwVmtoWFprTlhXSFJ5UzFSdlFrdDFZa0pyUzNCbVYwTlpVWGhxV0UweWRsWXZibEJ4WWxwR1dVOVdXazlpWlRaQlRuSm5lV1J2V1VNS1RVWlZUV0l6ZUhwelJrNVJXWFp6UlZsUGFUSkxibkoyUmpCMFoyOXdiVmhIVm05NmJsb3JjUzh5UVVsRVZ6bEdNVVUzV1RaWk1EWXhaVzkxUVZsa1NBcFhkejA5Q2kwdExTMHRSVTVFSUVORlVsUkpSa2xEUVZSRkxTMHRMUzBLIn1dfX0="
}
],
"timestampVerificationData": {},
"certificate": {
"rawBytes": "MIIGjTCCBhSgAwIBAgIUWYxqKsrMS3Svl5Ij5ODfBgMJO/IwCgYIKoZIzj0EAwMwNzEVMBMGA1UEChMMc2lnc3RvcmUuZGV2MR4wHAYDVQQDExVzaWdzdG9yZS1pbnRlcm1lZGlhdGUwHhcNMjQwNTI5MTYwOTUyWhcNMjQwNTI5MTYxOTUyWjAAMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEdmghNNw3nU/KueQgspGHW7gh9XLD/WdI8YMB+0p0V4o1kHo6cM1sDJgrCgPQUzxpuYuo+xwPHyl/kDyf3ELjkaOCBTMwggUvMA4GA1UdDwEB/wQEAwIHgDATBgNVHSUEDDAKBggrBgEFBQcDAzAdBgNVHQ4EFgQUqfCPvXKAvS4CdhQ2hbZWJSOEvVowHwYDVR0jBBgwFoAU39Ppz1YkEZb5qNjpKFWixi4YZD8wWgYDVR0RAQH/BFAwToZMaHR0cHM6Ly9naXRodWIuY29tL2NsaS9jbGkvLmdpdGh1Yi93b3JrZmxvd3MvZGVwbG95bWVudC55bWxAcmVmcy9oZWFkcy90cnVuazA5BgorBgEEAYO/MAEBBCtodHRwczovL3Rva2VuLmFjdGlvbnMuZ2l0aHVidXNlcmNvbnRlbnQuY29tMB8GCisGAQQBg78wAQIEEXdvcmtmbG93X2Rpc3BhdGNoMDYGCisGAQQBg78wAQMEKGZhZWYyZGRkODFiMDczNjc0ODQxM2E3YzY0NmNkMGJmYzI2YzAwYTAwGAYKKwYBBAGDvzABBAQKRGVwbG95bWVudDAVBgorBgEEAYO/MAEFBAdjbGkvY2xpMB4GCisGAQQBg78wAQYEEHJlZnMvaGVhZHMvdHJ1bmswOwYKKwYBBAGDvzABCAQtDCtodHRwczovL3Rva2VuLmFjdGlvbnMuZ2l0aHVidXNlcmNvbnRlbnQuY29tMFwGCisGAQQBg78wAQkETgxMaHR0cHM6Ly9naXRodWIuY29tL2NsaS9jbGkvLmdpdGh1Yi93b3JrZmxvd3MvZGVwbG95bWVudC55bWxAcmVmcy9oZWFkcy90cnVuazA4BgorBgEEAYO/MAEKBCoMKGZhZWYyZGRkODFiMDczNjc0ODQxM2E3YzY0NmNkMGJmYzI2YzAwYTAwHQYKKwYBBAGDvzABCwQPDA1naXRodWItaG9zdGVkMCoGCisGAQQBg78wAQwEHAwaaHR0cHM6Ly9naXRodWIuY29tL2NsaS9jbGkwOAYKKwYBBAGDvzABDQQqDChmYWVmMmRkZDgxYjA3MzY3NDg0MTNhN2M2NDZjZDBiZmMyNmMwMGEwMCAGCisGAQQBg78wAQ4EEgwQcmVmcy9oZWFkcy90cnVuazAZBgorBgEEAYO/MAEPBAsMCTIxMjYxMzA0OTAmBgorBgEEAYO/MAEQBBgMFmh0dHBzOi8vZ2l0aHViLmNvbS9jbGkwGAYKKwYBBAGDvzABEQQKDAg1OTcwNDcxMTBcBgorBgEEAYO/MAESBE4MTGh0dHBzOi8vZ2l0aHViLmNvbS9jbGkvY2xpLy5naXRodWIvd29ya2Zsb3dzL2RlcGxveW1lbnQueW1sQHJlZnMvaGVhZHMvdHJ1bmswOAYKKwYBBAGDvzABEwQqDChmYWVmMmRkZDgxYjA3MzY3NDg0MTNhN2M2NDZjZDBiZmMyNmMwMGEwMCEGCisGAQQBg78wARQEEwwRd29ya2Zsb3dfZGlzcGF0Y2gwTQYKKwYBBAGDvzABFQQ/DD1odHRwczovL2dpdGh1Yi5jb20vY2xpL2NsaS9hY3Rpb25zL3J1bnMvOTI4OTA3NTc1Mi9hdHRlbXB0cy8xMBYGCisGAQQBg78wARYECAwGcHVibGljMIGLBgorBgEEAdZ5AgQCBH0EewB5AHcA3T0wasbHETJjGR4cmWc3AqJKXrjePK3/h4pygC8p7o4AAAGPxR1zbgAABAMASDBGAiEA+8glQIxOAhXBAOS6S+8ZqwJcdwwSr/TWihs3dLqVAvoCIQDby9h1IcuDEr+zsWiL8Pw5CSTtkltJ421sE81Vvu6ApTAKBggqhkjOPQQDAwNnADBkAjA+DH7P+hh4VHWfCWXtrKToBKubBkKpfWCYQxjXM2vV/nPqbZFYOVZObe6ANrgydoYCMFUMb3xzsFNQYvsEYOi2KnrvF0tgopmXGVoznZ+q/2AIDW9F1E7Y6Y061eouAYdHWw=="
}
},
"dsseEnvelope": {
"payload": "eyJfdHlwZSI6Imh0dHBzOi8vaW4tdG90by5pby9TdGF0ZW1lbnQvdjEiLCJzdWJqZWN0IjpbeyJuYW1lIjoiZ2hfMi41MC4wX3dpbmRvd3NfYXJtNjQuemlwIiwiZGlnZXN0Ijp7InNoYTI1NiI6IjhhYWQxMjBiNDE2Mzg2YjQyNjllZjYyYzhmZGViY2FkMzFhNzA4NDcyOTc4MTdhMTQ5ZGFmOTI3ZWRjODU1NDgifX1dLCJwcmVkaWNhdGVUeXBlIjoiaHR0cHM6Ly9zbHNhLmRldi9wcm92ZW5hbmNlL3YxIiwicHJlZGljYXRlIjp7ImJ1aWxkRGVmaW5pdGlvbiI6eyJidWlsZFR5cGUiOiJodHRwczovL3Nsc2EtZnJhbWV3b3JrLmdpdGh1Yi5pby9naXRodWItYWN0aW9ucy1idWlsZHR5cGVzL3dvcmtmbG93L3YxIiwiZXh0ZXJuYWxQYXJhbWV0ZXJzIjp7IndvcmtmbG93Ijp7InJlZiI6InJlZnMvaGVhZHMvdHJ1bmsiLCJyZXBvc2l0b3J5IjoiaHR0cHM6Ly9naXRodWIuY29tL2NsaS9jbGkiLCJwYXRoIjoiLmdpdGh1Yi93b3JrZmxvd3MvZGVwbG95bWVudC55bWwifX0sImludGVybmFsUGFyYW1ldGVycyI6eyJnaXRodWIiOnsiZXZlbnRfbmFtZSI6IndvcmtmbG93X2Rpc3BhdGNoIiwicmVwb3NpdG9yeV9pZCI6IjIxMjYxMzA0OSIsInJlcG9zaXRvcnlfb3duZXJfaWQiOiI1OTcwNDcxMSJ9fSwicmVzb2x2ZWREZXBlbmRlbmNpZXMiOlt7InVyaSI6ImdpdCtodHRwczovL2dpdGh1Yi5jb20vY2xpL2NsaUByZWZzL2hlYWRzL3RydW5rIiwiZGlnZXN0Ijp7ImdpdENvbW1pdCI6ImZhZWYyZGRkODFiMDczNjc0ODQxM2E3YzY0NmNkMGJmYzI2YzAwYTAifX1dfSwicnVuRGV0YWlscyI6eyJidWlsZGVyIjp7ImlkIjoiaHR0cHM6Ly9naXRodWIuY29tL2FjdGlvbnMvcnVubmVyL2dpdGh1Yi1ob3N0ZWQifSwibWV0YWRhdGEiOnsiaW52b2NhdGlvbklkIjoiaHR0cHM6Ly9naXRodWIuY29tL2NsaS9jbGkvYWN0aW9ucy9ydW5zLzkyODkwNzU3NTIvYXR0ZW1wdHMvMSJ9fX19",
"payloadType": "application/vnd.in-toto+json",
"signatures": [
{
"sig": "MEQCIEGIGAm7gZVLLpsrPcjndEjiuctE2/c9+j9KGvazz3rlAiAd6O16T5hkzRM3IbRPzm+xT40mNQZxefd7laDP6x2XLQ=="
}
]
}
},
"repository_id": 1
}
]
}
]
}`

## Delete attestations in bulk

Delete artifact attestations in bulk by either subject digests or unique ID.

### Fine-grained access tokens for "Delete attestations in bulk"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Attestations" repository permissions (write)

### Parameters for "Delete attestations in bulk"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| subject_digestsarray of stringsRequiredList of subject digests associated with the artifact attestations to delete. |

### HTTP response status codes for "Delete attestations in bulk"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |

## Delete attestations by subject digest

Delete an artifact attestation by subject digest.

### Fine-grained access tokens for "Delete attestations by subject digest"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Attestations" repository permissions (write)

### Parameters for "Delete attestations by subject digest"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| subject_digeststringRequiredSubject Digest |

### HTTP response status codes for "Delete attestations by subject digest"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 204 | No Content |
| 404 | Resource not found |

### Code samples for "Delete attestations by subject digest"

#### Request examples

Select the example typeExample 1: Status Code 200Example 2: Status Code 204delete/orgs/{org}/attestations/digest/{subject_digest}

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/attestations/digest/SUBJECT_DIGEST`

Response

`Status: 200`

## List attestation repositories

List repositories owned by the provided organization that have created at least one attested artifact
Results will be sorted in ascending order by repository ID

### Fine-grained access tokens for "List attestation repositories"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Attestations" repository permissions (read)

### Parameters for "List attestation repositories"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| beforestringA cursor, as given in theLink header. If specified, the query only searches for results before this cursor. For more information, see "Using pagination in the REST API." |
| afterstringA cursor, as given in theLink header. If specified, the query only searches for results after this cursor. For more information, see "Using pagination in the REST API." |
| predicate_typestringOptional filter for fetching attestations with a given predicate type.
This option acceptsprovenance,sbom,release, or freeform text
for custom predicate types. |

### HTTP response status codes for "List attestation repositories"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "List attestation repositories"

#### Request example

get/orgs/{org}/attestations/repositories

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/attestations/repositories`

Response

-
-

`Status: 200``[
{
"id": 123,
"name": "foo"
},
{
"id": 456,
"name": "bar"
}
]`

## Delete attestations by ID

Delete an artifact attestation by unique ID that is associated with a repository owned by an org.

### Fine-grained access tokens for "Delete attestations by ID"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Attestations" repository permissions (write)

### Parameters for "Delete attestations by ID"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| attestation_idintegerRequiredAttestation ID |

### HTTP response status codes for "Delete attestations by ID"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 204 | No Content |
| 403 | Forbidden |
| 404 | Resource not found |

### Code samples for "Delete attestations by ID"

#### Request examples

Select the example typeExample 1: Status Code 200Example 2: Status Code 204delete/orgs/{org}/attestations/{attestation_id}

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/attestations/ATTESTATION_ID`

Response

`Status: 200`

## List attestations

List a collection of artifact attestations with a given subject digest that are associated with repositories owned by an organization.

The collection of attestations returned by this endpoint is filtered according to the authenticated user's permissions; if the authenticated user cannot read a repository, the attestations associated with that repository will not be included in the response. In addition, when using a fine-grained access token the `attestations:read` permission is required.

**Please note:** in order to offer meaningful security benefits, an attestation's signature and timestamps **must** be cryptographically verified, and the identity of the attestation signer **must** be validated. Attestations can be verified using the [GitHub CLIattestation verifycommand](https://cli.github.com/manual/gh_attestation_verify). For more information, see [our guide on how to use artifact attestations to establish a build's provenance](https://docs.github.com/actions/security-guides/using-artifact-attestations-to-establish-provenance-for-builds).

### Fine-grained access tokens for "List attestations"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token does not require any permissions.

This endpoint can be used without authentication if only public resources are requested.

### Parameters for "List attestations"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| subject_digeststringRequiredThe parameter should be set to the attestation's subject's SHA256 digest, in the formsha256:HEX_DIGEST. |

| Name, Type, Description |
| --- |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| beforestringA cursor, as given in theLink header. If specified, the query only searches for results before this cursor. For more information, see "Using pagination in the REST API." |
| afterstringA cursor, as given in theLink header. If specified, the query only searches for results after this cursor. For more information, see "Using pagination in the REST API." |
| predicate_typestringOptional filter for fetching attestations with a given predicate type.
This option acceptsprovenance,sbom,release, or freeform text
for custom predicate types. |

### HTTP response status codes for "List attestations"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "List attestations"

#### Request example

get/orgs/{org}/attestations/{subject_digest}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/attestations/SUBJECT_DIGEST`

Response

-
-

`Status: 200``{
"attestations": [
{
"bundle": {
"mediaType": "application/vnd.dev.sigstore.bundle.v0.3+json",
"verificationMaterial": {
"tlogEntries": [
{
"logIndex": "97913980",
"logId": {
"keyId": "wNI9atQGlz+VWfO6LRygH4QUfY/8W4RFwiT5i5WRgB0="
},
"kindVersion": {
"kind": "dsse",
"version": "0.0.1"
},
"integratedTime": "1716998992",
"inclusionPromise": {
"signedEntryTimestamp": "MEYCIQCeEsQAy+qXtULkh52wbnHrkt2R2JQ05P9STK/xmdpQ2AIhANiG5Gw6cQiMnwvUz1+9UKtG/vlC8dduq07wsFOViwSL"
},
"inclusionProof": {
"logIndex": "93750549",
"rootHash": "KgKiXoOl8rM5d4y6Xlbm2QLftvj/FYvTs6z7dJlNO60=",
"treeSize": "93750551",
"hashes": [
"8LI21mzwxnUSo0fuZeFsUrz2ujZ4QAL+oGeTG+5toZg=",
"nCb369rcIytNhGwWoqBv+eV49X3ZKpo/HJGKm9V+dck=",
"hnNQ9mUdSwYCfdV21pd87NucrdRRNZATowlaRR1hJ4A=",
"MBhhK33vlD4Tq/JKgAaXUI4VjmosWKe6+7RNpQ2ncNM=",
"XKWUE3stvGV1OHsIGiCGfn047Ok6uD4mFkh7BaicaEc=",
"Tgve40VPFfuei+0nhupdGpfPPR+hPpZjxgTiDT8WNoY=",
"wV+S/7tLtYGzkLaSb6UDqexNyhMvumHK/RpTNvEZuLU=",
"uwaWufty6sn6XqO1Tb9M3Vz6sBKPu0HT36mStxJNd7s=",
"jUfeMOXQP0XF1JAnCEETVbfRKMUwCzrVUzYi8vnDMVs=",
"xQKjzJAwwdlQG/YUYBKPXxbCmhMYKo1wnv+6vDuKWhQ=",
"cX3Agx+hP66t1ZLbX/yHbfjU46/3m/VAmWyG/fhxAVc=",
"sjohk/3DQIfXTgf/5XpwtdF7yNbrf8YykOMHr1CyBYQ=",
"98enzMaC+x5oCMvIZQA5z8vu2apDMCFvE/935NfuPw8="
],
"checkpoint": {
"envelope": "rekor.sigstore.dev - 2605736670972794746\\n93750551\\nKgKiXoOl8rM5d4y6Xlbm2QLftvj/FYvTs6z7dJlNO60=\\n\\n— rekor.sigstore.dev wNI9ajBEAiBkLzdjY8A9HReU7rmtjwZ+JpSuYtEr9SmvSwUIW7FBjgIgKo+vhkW3tqc+gc8fw9gza3xLoncA8a+MTaJYCaLGA9c=\\n"
}
},
"canonicalizedBody": "eyJhcGlWZXJzaW9uIjoiMC4wLjEiLCJraW5kIjoiZHNzZSIsInNwZWMiOnsiZW52ZWxvcGVIYXNoIjp7ImFsZ29yaXRobSI6InNoYTI1NiIsInZhbHVlIjoiM2I1YzkwNDk5MGFiYzE4NjI1ZWE3Njg4MzE1OGEwZmI4MTEwMjM4MGJkNjQwZjI5OWJlMzYwZWVkOTMxNjYwYiJ9LCJwYXlsb2FkSGFzaCI6eyJhbGdvcml0aG0iOiJzaGEyNTYiLCJ2YWx1ZSI6IjM4ZGNlZDJjMzE1MGU2OTQxMDViYjZiNDNjYjY3NzBiZTYzZDdhNGM4NjNiMTc2YTkwMmU1MGQ5ZTAyN2ZiMjMifSwic2lnbmF0dXJlcyI6W3sic2lnbmF0dXJlIjoiTUVRQ0lFR0lHQW03Z1pWTExwc3JQY2puZEVqaXVjdEUyL2M5K2o5S0d2YXp6M3JsQWlBZDZPMTZUNWhrelJNM0liUlB6bSt4VDQwbU5RWnhlZmQ3bGFEUDZ4MlhMUT09IiwidmVyaWZpZXIiOiJMUzB0TFMxQ1JVZEpUaUJEUlZKVVNVWkpRMEZVUlMwdExTMHRDazFKU1VkcVZFTkRRbWhUWjBGM1NVSkJaMGxWVjFsNGNVdHpjazFUTTFOMmJEVkphalZQUkdaQ1owMUtUeTlKZDBObldVbExiMXBKZW1vd1JVRjNUWGNLVG5wRlZrMUNUVWRCTVZWRlEyaE5UV015Ykc1ak0xSjJZMjFWZFZwSFZqSk5ValIzU0VGWlJGWlJVVVJGZUZaNllWZGtlbVJIT1hsYVV6RndZbTVTYkFwamJURnNXa2RzYUdSSFZYZElhR05PVFdwUmQwNVVTVFZOVkZsM1QxUlZlVmRvWTA1TmFsRjNUbFJKTlUxVVdYaFBWRlY1VjJwQlFVMUdhM2RGZDFsSUNrdHZXa2w2YWpCRFFWRlpTVXR2V2tsNmFqQkVRVkZqUkZGblFVVmtiV2RvVGs1M00yNVZMMHQxWlZGbmMzQkhTRmMzWjJnNVdFeEVMMWRrU1RoWlRVSUtLekJ3TUZZMGJ6RnJTRzgyWTAweGMwUktaM0pEWjFCUlZYcDRjSFZaZFc4cmVIZFFTSGxzTDJ0RWVXWXpSVXhxYTJGUFEwSlVUWGRuWjFWMlRVRTBSd3BCTVZWa1JIZEZRaTkzVVVWQmQwbElaMFJCVkVKblRsWklVMVZGUkVSQlMwSm5aM0pDWjBWR1FsRmpSRUY2UVdSQ1owNVdTRkUwUlVablVWVnhaa05RQ25aWVMwRjJVelJEWkdoUk1taGlXbGRLVTA5RmRsWnZkMGgzV1VSV1VqQnFRa0puZDBadlFWVXpPVkJ3ZWpGWmEwVmFZalZ4VG1wd1MwWlhhWGhwTkZrS1drUTRkMWRuV1VSV1VqQlNRVkZJTDBKR1FYZFViMXBOWVVoU01HTklUVFpNZVRsdVlWaFNiMlJYU1hWWk1qbDBUREpPYzJGVE9XcGlSMnQyVEcxa2NBcGtSMmd4V1drNU0ySXpTbkphYlhoMlpETk5kbHBIVm5kaVJ6azFZbGRXZFdSRE5UVmlWM2hCWTIxV2JXTjVPVzlhVjBaclkzazVNR051Vm5WaGVrRTFDa0puYjNKQ1owVkZRVmxQTDAxQlJVSkNRM1J2WkVoU2QyTjZiM1pNTTFKMllUSldkVXh0Um1wa1IyeDJZbTVOZFZveWJEQmhTRlpwWkZoT2JHTnRUbllLWW01U2JHSnVVWFZaTWpsMFRVSTRSME5wYzBkQlVWRkNaemM0ZDBGUlNVVkZXR1IyWTIxMGJXSkhPVE5ZTWxKd1l6TkNhR1JIVG05TlJGbEhRMmx6UndwQlVWRkNaemM0ZDBGUlRVVkxSMXBvV2xkWmVWcEhVbXRQUkVacFRVUmplazVxWXpCUFJGRjRUVEpGTTFsNldUQk9iVTVyVFVkS2JWbDZTVEpaZWtGM0NsbFVRWGRIUVZsTFMzZFpRa0pCUjBSMmVrRkNRa0ZSUzFKSFZuZGlSemsxWWxkV2RXUkVRVlpDWjI5eVFtZEZSVUZaVHk5TlFVVkdRa0ZrYW1KSGEzWUtXVEo0Y0UxQ05FZERhWE5IUVZGUlFtYzNPSGRCVVZsRlJVaEtiRnB1VFhaaFIxWm9Xa2hOZG1SSVNqRmliWE4zVDNkWlMwdDNXVUpDUVVkRWRucEJRZ3BEUVZGMFJFTjBiMlJJVW5kamVtOTJURE5TZG1FeVZuVk1iVVpxWkVkc2RtSnVUWFZhTW13d1lVaFdhV1JZVG14amJVNTJZbTVTYkdKdVVYVlpNamwwQ2sxR2QwZERhWE5IUVZGUlFtYzNPSGRCVVd0RlZHZDRUV0ZJVWpCalNFMDJUSGs1Ym1GWVVtOWtWMGwxV1RJNWRFd3lUbk5oVXpscVlrZHJka3h0WkhBS1pFZG9NVmxwT1ROaU0wcHlXbTE0ZG1RelRYWmFSMVozWWtjNU5XSlhWblZrUXpVMVlsZDRRV050Vm0xamVUbHZXbGRHYTJONU9UQmpibFoxWVhwQk5BcENaMjl5UW1kRlJVRlpUeTlOUVVWTFFrTnZUVXRIV21oYVYxbDVXa2RTYTA5RVJtbE5SR042VG1wak1FOUVVWGhOTWtVeldYcFpNRTV0VG10TlIwcHRDbGw2U1RKWmVrRjNXVlJCZDBoUldVdExkMWxDUWtGSFJIWjZRVUpEZDFGUVJFRXhibUZZVW05a1YwbDBZVWM1ZW1SSFZtdE5RMjlIUTJselIwRlJVVUlLWnpjNGQwRlJkMFZJUVhkaFlVaFNNR05JVFRaTWVUbHVZVmhTYjJSWFNYVlpNamwwVERKT2MyRlRPV3BpUjJ0M1QwRlpTMHQzV1VKQ1FVZEVkbnBCUWdwRVVWRnhSRU5vYlZsWFZtMU5iVkpyV2tSbmVGbHFRVE5OZWxrelRrUm5NRTFVVG1oT01rMHlUa1JhYWxwRVFtbGFiVTE1VG0xTmQwMUhSWGROUTBGSENrTnBjMGRCVVZGQ1p6YzRkMEZSTkVWRlozZFJZMjFXYldONU9XOWFWMFpyWTNrNU1HTnVWblZoZWtGYVFtZHZja0puUlVWQldVOHZUVUZGVUVKQmMwMEtRMVJKZUUxcVdYaE5la0V3VDFSQmJVSm5iM0pDWjBWRlFWbFBMMDFCUlZGQ1FtZE5SbTFvTUdSSVFucFBhVGgyV2pKc01HRklWbWxNYlU1MllsTTVhZ3BpUjJ0M1IwRlpTMHQzV1VKQ1FVZEVkbnBCUWtWUlVVdEVRV2N4VDFSamQwNUVZM2hOVkVKalFtZHZja0puUlVWQldVOHZUVUZGVTBKRk5FMVVSMmd3Q21SSVFucFBhVGgyV2pKc01HRklWbWxNYlU1MllsTTVhbUpIYTNaWk1uaHdUSGsxYm1GWVVtOWtWMGwyWkRJNWVXRXlXbk5pTTJSNlRESlNiR05IZUhZS1pWY3hiR0p1VVhWbFZ6RnpVVWhLYkZwdVRYWmhSMVpvV2toTmRtUklTakZpYlhOM1QwRlpTMHQzV1VKQ1FVZEVkbnBCUWtWM1VYRkVRMmh0V1ZkV2JRcE5iVkpyV2tSbmVGbHFRVE5OZWxrelRrUm5NRTFVVG1oT01rMHlUa1JhYWxwRVFtbGFiVTE1VG0xTmQwMUhSWGROUTBWSFEybHpSMEZSVVVKbk56aDNDa0ZTVVVWRmQzZFNaREk1ZVdFeVduTmlNMlJtV2tkc2VtTkhSakJaTW1kM1ZGRlpTMHQzV1VKQ1FVZEVkbnBCUWtaUlVTOUVSREZ2WkVoU2QyTjZiM1lLVERKa2NHUkhhREZaYVRWcVlqSXdkbGt5ZUhCTU1rNXpZVk01YUZrelVuQmlNalY2VEROS01XSnVUWFpQVkVrMFQxUkJNMDVVWXpGTmFUbG9aRWhTYkFwaVdFSXdZM2s0ZUUxQ1dVZERhWE5IUVZGUlFtYzNPSGRCVWxsRlEwRjNSMk5JVm1saVIyeHFUVWxIVEVKbmIzSkNaMFZGUVdSYU5VRm5VVU5DU0RCRkNtVjNRalZCU0dOQk0xUXdkMkZ6WWtoRlZFcHFSMUkwWTIxWFl6TkJjVXBMV0hKcVpWQkxNeTlvTkhCNVowTTRjRGR2TkVGQlFVZFFlRkl4ZW1KblFVRUtRa0ZOUVZORVFrZEJhVVZCS3pobmJGRkplRTlCYUZoQ1FVOVRObE1yT0ZweGQwcGpaSGQzVTNJdlZGZHBhSE16WkV4eFZrRjJiME5KVVVSaWVUbG9NUXBKWTNWRVJYSXJlbk5YYVV3NFVIYzFRMU5VZEd0c2RFbzBNakZ6UlRneFZuWjFOa0Z3VkVGTFFtZG5jV2hyYWs5UVVWRkVRWGRPYmtGRVFtdEJha0VyQ2tSSU4xQXJhR2cwVmtoWFprTlhXSFJ5UzFSdlFrdDFZa0pyUzNCbVYwTlpVWGhxV0UweWRsWXZibEJ4WWxwR1dVOVdXazlpWlRaQlRuSm5lV1J2V1VNS1RVWlZUV0l6ZUhwelJrNVJXWFp6UlZsUGFUSkxibkoyUmpCMFoyOXdiVmhIVm05NmJsb3JjUzh5UVVsRVZ6bEdNVVUzV1RaWk1EWXhaVzkxUVZsa1NBcFhkejA5Q2kwdExTMHRSVTVFSUVORlVsUkpSa2xEUVZSRkxTMHRMUzBLIn1dfX0="
}
],
"timestampVerificationData": {},
"certificate": {
"rawBytes": "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"
}
},
"dsseEnvelope": {
"payload": "eyJfdHlwZSI6Imh0dHBzOi8vaW4tdG90by5pby9TdGF0ZW1lbnQvdjEiLCJzdWJqZWN0IjpbeyJuYW1lIjoiZ2hfMi41MC4wX3dpbmRvd3NfYXJtNjQuemlwIiwiZGlnZXN0Ijp7InNoYTI1NiI6IjhhYWQxMjBiNDE2Mzg2YjQyNjllZjYyYzhmZGViY2FkMzFhNzA4NDcyOTc4MTdhMTQ5ZGFmOTI3ZWRjODU1NDgifX1dLCJwcmVkaWNhdGVUeXBlIjoiaHR0cHM6Ly9zbHNhLmRldi9wcm92ZW5hbmNlL3YxIiwicHJlZGljYXRlIjp7ImJ1aWxkRGVmaW5pdGlvbiI6eyJidWlsZFR5cGUiOiJodHRwczovL3Nsc2EtZnJhbWV3b3JrLmdpdGh1Yi5pby9naXRodWItYWN0aW9ucy1idWlsZHR5cGVzL3dvcmtmbG93L3YxIiwiZXh0ZXJuYWxQYXJhbWV0ZXJzIjp7IndvcmtmbG93Ijp7InJlZiI6InJlZnMvaGVhZHMvdHJ1bmsiLCJyZXBvc2l0b3J5IjoiaHR0cHM6Ly9naXRodWIuY29tL2NsaS9jbGkiLCJwYXRoIjoiLmdpdGh1Yi93b3JrZmxvd3MvZGVwbG95bWVudC55bWwifX0sImludGVybmFsUGFyYW1ldGVycyI6eyJnaXRodWIiOnsiZXZlbnRfbmFtZSI6IndvcmtmbG93X2Rpc3BhdGNoIiwicmVwb3NpdG9yeV9pZCI6IjIxMjYxMzA0OSIsInJlcG9zaXRvcnlfb3duZXJfaWQiOiI1OTcwNDcxMSJ9fSwicmVzb2x2ZWREZXBlbmRlbmNpZXMiOlt7InVyaSI6ImdpdCtodHRwczovL2dpdGh1Yi5jb20vY2xpL2NsaUByZWZzL2hlYWRzL3RydW5rIiwiZGlnZXN0Ijp7ImdpdENvbW1pdCI6ImZhZWYyZGRkODFiMDczNjc0ODQxM2E3YzY0NmNkMGJmYzI2YzAwYTAifX1dfSwicnVuRGV0YWlscyI6eyJidWlsZGVyIjp7ImlkIjoiaHR0cHM6Ly9naXRodWIuY29tL2FjdGlvbnMvcnVubmVyL2dpdGh1Yi1ob3N0ZWQifSwibWV0YWRhdGEiOnsiaW52b2NhdGlvbklkIjoiaHR0cHM6Ly9naXRodWIuY29tL2NsaS9jbGkvYWN0aW9ucy9ydW5zLzkyODkwNzU3NTIvYXR0ZW1wdHMvMSJ9fX19",
"payloadType": "application/vnd.in-toto+json",
"signatures": [
{
"sig": "MEQCIEGIGAm7gZVLLpsrPcjndEjiuctE2/c9+j9KGvazz3rlAiAd6O16T5hkzRM3IbRPzm+xT40mNQZxefd7laDP6x2XLQ=="
}
]
}
},
"repository_id": 1
},
{
"bundle": {
"mediaType": "application/vnd.dev.sigstore.bundle.v0.3+json",
"verificationMaterial": {
"tlogEntries": [
{
"logIndex": "97913980",
"logId": {
"keyId": "wNI9atQGlz+VWfO6LRygH4QUfY/8W4RFwiT5i5WRgB0="
},
"kindVersion": {
"kind": "dsse",
"version": "0.0.1"
},
"integratedTime": "1716998992",
"inclusionPromise": {
"signedEntryTimestamp": "MEYCIQCeEsQAy+qXtULkh52wbnHrkt2R2JQ05P9STK/xmdpQ2AIhANiG5Gw6cQiMnwvUz1+9UKtG/vlC8dduq07wsFOViwSL"
},
"inclusionProof": {
"logIndex": "93750549",
"rootHash": "KgKiXoOl8rM5d4y6Xlbm2QLftvj/FYvTs6z7dJlNO60=",
"treeSize": "93750551",
"hashes": [
"8LI21mzwxnUSo0fuZeFsUrz2ujZ4QAL+oGeTG+5toZg=",
"nCb369rcIytNhGwWoqBv+eV49X3ZKpo/HJGKm9V+dck=",
"hnNQ9mUdSwYCfdV21pd87NucrdRRNZATowlaRR1hJ4A=",
"MBhhK33vlD4Tq/JKgAaXUI4VjmosWKe6+7RNpQ2ncNM=",
"XKWUE3stvGV1OHsIGiCGfn047Ok6uD4mFkh7BaicaEc=",
"Tgve40VPFfuei+0nhupdGpfPPR+hPpZjxgTiDT8WNoY=",
"wV+S/7tLtYGzkLaSb6UDqexNyhMvumHK/RpTNvEZuLU=",
"uwaWufty6sn6XqO1Tb9M3Vz6sBKPu0HT36mStxJNd7s=",
"jUfeMOXQP0XF1JAnCEETVbfRKMUwCzrVUzYi8vnDMVs=",
"xQKjzJAwwdlQG/YUYBKPXxbCmhMYKo1wnv+6vDuKWhQ=",
"cX3Agx+hP66t1ZLbX/yHbfjU46/3m/VAmWyG/fhxAVc=",
"sjohk/3DQIfXTgf/5XpwtdF7yNbrf8YykOMHr1CyBYQ=",
"98enzMaC+x5oCMvIZQA5z8vu2apDMCFvE/935NfuPw8="
],
"checkpoint": {
"envelope": "rekor.sigstore.dev - 2605736670972794746\\n93750551\\nKgKiXoOl8rM5d4y6Xlbm2QLftvj/FYvTs6z7dJlNO60=\\n\\n— rekor.sigstore.dev wNI9ajBEAiBkLzdjY8A9HReU7rmtjwZ+JpSuYtEr9SmvSwUIW7FBjgIgKo+vhkW3tqc+gc8fw9gza3xLoncA8a+MTaJYCaLGA9c=\\n"
}
},
"canonicalizedBody": "eyJhcGlWZXJzaW9uIjoiMC4wLjEiLCJraW5kIjoiZHNzZSIsInNwZWMiOnsiZW52ZWxvcGVIYXNoIjp7ImFsZ29yaXRobSI6InNoYTI1NiIsInZhbHVlIjoiM2I1YzkwNDk5MGFiYzE4NjI1ZWE3Njg4MzE1OGEwZmI4MTEwMjM4MGJkNjQwZjI5OWJlMzYwZWVkOTMxNjYwYiJ9LCJwYXlsb2FkSGFzaCI6eyJhbGdvcml0aG0iOiJzaGEyNTYiLCJ2YWx1ZSI6IjM4ZGNlZDJjMzE1MGU2OTQxMDViYjZiNDNjYjY3NzBiZTYzZDdhNGM4NjNiMTc2YTkwMmU1MGQ5ZTAyN2ZiMjMifSwic2lnbmF0dXJlcyI6W3sic2lnbmF0dXJlIjoiTUVRQ0lFR0lHQW03Z1pWTExwc3JQY2puZEVqaXVjdEUyL2M5K2o5S0d2YXp6M3JsQWlBZDZPMTZUNWhrelJNM0liUlB6bSt4VDQwbU5RWnhlZmQ3bGFEUDZ4MlhMUT09IiwidmVyaWZpZXIiOiJMUzB0TFMxQ1JVZEpUaUJEUlZKVVNVWkpRMEZVUlMwdExTMHRDazFKU1VkcVZFTkRRbWhUWjBGM1NVSkJaMGxWVjFsNGNVdHpjazFUTTFOMmJEVkphalZQUkdaQ1owMUtUeTlKZDBObldVbExiMXBKZW1vd1JVRjNUWGNLVG5wRlZrMUNUVWRCTVZWRlEyaE5UV015Ykc1ak0xSjJZMjFWZFZwSFZqSk5ValIzU0VGWlJGWlJVVVJGZUZaNllWZGtlbVJIT1hsYVV6RndZbTVTYkFwamJURnNXa2RzYUdSSFZYZElhR05PVFdwUmQwNVVTVFZOVkZsM1QxUlZlVmRvWTA1TmFsRjNUbFJKTlUxVVdYaFBWRlY1VjJwQlFVMUdhM2RGZDFsSUNrdHZXa2w2YWpCRFFWRlpTVXR2V2tsNmFqQkVRVkZqUkZGblFVVmtiV2RvVGs1M00yNVZMMHQxWlZGbmMzQkhTRmMzWjJnNVdFeEVMMWRrU1RoWlRVSUtLekJ3TUZZMGJ6RnJTRzgyWTAweGMwUktaM0pEWjFCUlZYcDRjSFZaZFc4cmVIZFFTSGxzTDJ0RWVXWXpSVXhxYTJGUFEwSlVUWGRuWjFWMlRVRTBSd3BCTVZWa1JIZEZRaTkzVVVWQmQwbElaMFJCVkVKblRsWklVMVZGUkVSQlMwSm5aM0pDWjBWR1FsRmpSRUY2UVdSQ1owNVdTRkUwUlVablVWVnhaa05RQ25aWVMwRjJVelJEWkdoUk1taGlXbGRLVTA5RmRsWnZkMGgzV1VSV1VqQnFRa0puZDBadlFWVXpPVkJ3ZWpGWmEwVmFZalZ4VG1wd1MwWlhhWGhwTkZrS1drUTRkMWRuV1VSV1VqQlNRVkZJTDBKR1FYZFViMXBOWVVoU01HTklUVFpNZVRsdVlWaFNiMlJYU1hWWk1qbDBUREpPYzJGVE9XcGlSMnQyVEcxa2NBcGtSMmd4V1drNU0ySXpTbkphYlhoMlpETk5kbHBIVm5kaVJ6azFZbGRXZFdSRE5UVmlWM2hCWTIxV2JXTjVPVzlhVjBaclkzazVNR051Vm5WaGVrRTFDa0puYjNKQ1owVkZRVmxQTDAxQlJVSkNRM1J2WkVoU2QyTjZiM1pNTTFKMllUSldkVXh0Um1wa1IyeDJZbTVOZFZveWJEQmhTRlpwWkZoT2JHTnRUbllLWW01U2JHSnVVWFZaTWpsMFRVSTRSME5wYzBkQlVWRkNaemM0ZDBGUlNVVkZXR1IyWTIxMGJXSkhPVE5ZTWxKd1l6TkNhR1JIVG05TlJGbEhRMmx6UndwQlVWRkNaemM0ZDBGUlRVVkxSMXBvV2xkWmVWcEhVbXRQUkVacFRVUmplazVxWXpCUFJGRjRUVEpGTTFsNldUQk9iVTVyVFVkS2JWbDZTVEpaZWtGM0NsbFVRWGRIUVZsTFMzZFpRa0pCUjBSMmVrRkNRa0ZSUzFKSFZuZGlSemsxWWxkV2RXUkVRVlpDWjI5eVFtZEZSVUZaVHk5TlFVVkdRa0ZrYW1KSGEzWUtXVEo0Y0UxQ05FZERhWE5IUVZGUlFtYzNPSGRCVVZsRlJVaEtiRnB1VFhaaFIxWm9Xa2hOZG1SSVNqRmliWE4zVDNkWlMwdDNXVUpDUVVkRWRucEJRZ3BEUVZGMFJFTjBiMlJJVW5kamVtOTJURE5TZG1FeVZuVk1iVVpxWkVkc2RtSnVUWFZhTW13d1lVaFdhV1JZVG14amJVNTJZbTVTYkdKdVVYVlpNamwwQ2sxR2QwZERhWE5IUVZGUlFtYzNPSGRCVVd0RlZHZDRUV0ZJVWpCalNFMDJUSGs1Ym1GWVVtOWtWMGwxV1RJNWRFd3lUbk5oVXpscVlrZHJka3h0WkhBS1pFZG9NVmxwT1ROaU0wcHlXbTE0ZG1RelRYWmFSMVozWWtjNU5XSlhWblZrUXpVMVlsZDRRV050Vm0xamVUbHZXbGRHYTJONU9UQmpibFoxWVhwQk5BcENaMjl5UW1kRlJVRlpUeTlOUVVWTFFrTnZUVXRIV21oYVYxbDVXa2RTYTA5RVJtbE5SR042VG1wak1FOUVVWGhOTWtVeldYcFpNRTV0VG10TlIwcHRDbGw2U1RKWmVrRjNXVlJCZDBoUldVdExkMWxDUWtGSFJIWjZRVUpEZDFGUVJFRXhibUZZVW05a1YwbDBZVWM1ZW1SSFZtdE5RMjlIUTJselIwRlJVVUlLWnpjNGQwRlJkMFZJUVhkaFlVaFNNR05JVFRaTWVUbHVZVmhTYjJSWFNYVlpNamwwVERKT2MyRlRPV3BpUjJ0M1QwRlpTMHQzV1VKQ1FVZEVkbnBCUWdwRVVWRnhSRU5vYlZsWFZtMU5iVkpyV2tSbmVGbHFRVE5OZWxrelRrUm5NRTFVVG1oT01rMHlUa1JhYWxwRVFtbGFiVTE1VG0xTmQwMUhSWGROUTBGSENrTnBjMGRCVVZGQ1p6YzRkMEZSTkVWRlozZFJZMjFXYldONU9XOWFWMFpyWTNrNU1HTnVWblZoZWtGYVFtZHZja0puUlVWQldVOHZUVUZGVUVKQmMwMEtRMVJKZUUxcVdYaE5la0V3VDFSQmJVSm5iM0pDWjBWRlFWbFBMMDFCUlZGQ1FtZE5SbTFvTUdSSVFucFBhVGgyV2pKc01HRklWbWxNYlU1MllsTTVhZ3BpUjJ0M1IwRlpTMHQzV1VKQ1FVZEVkbnBCUWtWUlVVdEVRV2N4VDFSamQwNUVZM2hOVkVKalFtZHZja0puUlVWQldVOHZUVUZGVTBKRk5FMVVSMmd3Q21SSVFucFBhVGgyV2pKc01HRklWbWxNYlU1MllsTTVhbUpIYTNaWk1uaHdUSGsxYm1GWVVtOWtWMGwyWkRJNWVXRXlXbk5pTTJSNlRESlNiR05IZUhZS1pWY3hiR0p1VVhWbFZ6RnpVVWhLYkZwdVRYWmhSMVpvV2toTmRtUklTakZpYlhOM1QwRlpTMHQzV1VKQ1FVZEVkbnBCUWtWM1VYRkVRMmh0V1ZkV2JRcE5iVkpyV2tSbmVGbHFRVE5OZWxrelRrUm5NRTFVVG1oT01rMHlUa1JhYWxwRVFtbGFiVTE1VG0xTmQwMUhSWGROUTBWSFEybHpSMEZSVVVKbk56aDNDa0ZTVVVWRmQzZFNaREk1ZVdFeVduTmlNMlJtV2tkc2VtTkhSakJaTW1kM1ZGRlpTMHQzV1VKQ1FVZEVkbnBCUWtaUlVTOUVSREZ2WkVoU2QyTjZiM1lLVERKa2NHUkhhREZaYVRWcVlqSXdkbGt5ZUhCTU1rNXpZVk01YUZrelVuQmlNalY2VEROS01XSnVUWFpQVkVrMFQxUkJNMDVVWXpGTmFUbG9aRWhTYkFwaVdFSXdZM2s0ZUUxQ1dVZERhWE5IUVZGUlFtYzNPSGRCVWxsRlEwRjNSMk5JVm1saVIyeHFUVWxIVEVKbmIzSkNaMFZGUVdSYU5VRm5VVU5DU0RCRkNtVjNRalZCU0dOQk0xUXdkMkZ6WWtoRlZFcHFSMUkwWTIxWFl6TkJjVXBMV0hKcVpWQkxNeTlvTkhCNVowTTRjRGR2TkVGQlFVZFFlRkl4ZW1KblFVRUtRa0ZOUVZORVFrZEJhVVZCS3pobmJGRkplRTlCYUZoQ1FVOVRObE1yT0ZweGQwcGpaSGQzVTNJdlZGZHBhSE16WkV4eFZrRjJiME5KVVVSaWVUbG9NUXBKWTNWRVJYSXJlbk5YYVV3NFVIYzFRMU5VZEd0c2RFbzBNakZ6UlRneFZuWjFOa0Z3VkVGTFFtZG5jV2hyYWs5UVVWRkVRWGRPYmtGRVFtdEJha0VyQ2tSSU4xQXJhR2cwVmtoWFprTlhXSFJ5UzFSdlFrdDFZa0pyUzNCbVYwTlpVWGhxV0UweWRsWXZibEJ4WWxwR1dVOVdXazlpWlRaQlRuSm5lV1J2V1VNS1RVWlZUV0l6ZUhwelJrNVJXWFp6UlZsUGFUSkxibkoyUmpCMFoyOXdiVmhIVm05NmJsb3JjUzh5UVVsRVZ6bEdNVVUzV1RaWk1EWXhaVzkxUVZsa1NBcFhkejA5Q2kwdExTMHRSVTVFSUVORlVsUkpSa2xEUVZSRkxTMHRMUzBLIn1dfX0="
}
],
"timestampVerificationData": {},
"certificate": {
"rawBytes": "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"
}
},
"dsseEnvelope": {
"payload": "eyJfdHlwZSI6Imh0dHBzOi8vaW4tdG90by5pby9TdGF0ZW1lbnQvdjEiLCJzdWJqZWN0IjpbeyJuYW1lIjoiZ2hfMi41MC4wX3dpbmRvd3NfYXJtNjQuemlwIiwiZGlnZXN0Ijp7InNoYTI1NiI6IjhhYWQxMjBiNDE2Mzg2YjQyNjllZjYyYzhmZGViY2FkMzFhNzA4NDcyOTc4MTdhMTQ5ZGFmOTI3ZWRjODU1NDgifX1dLCJwcmVkaWNhdGVUeXBlIjoiaHR0cHM6Ly9zbHNhLmRldi9wcm92ZW5hbmNlL3YxIiwicHJlZGljYXRlIjp7ImJ1aWxkRGVmaW5pdGlvbiI6eyJidWlsZFR5cGUiOiJodHRwczovL3Nsc2EtZnJhbWV3b3JrLmdpdGh1Yi5pby9naXRodWItYWN0aW9ucy1idWlsZHR5cGVzL3dvcmtmbG93L3YxIiwiZXh0ZXJuYWxQYXJhbWV0ZXJzIjp7IndvcmtmbG93Ijp7InJlZiI6InJlZnMvaGVhZHMvdHJ1bmsiLCJyZXBvc2l0b3J5IjoiaHR0cHM6Ly9naXRodWIuY29tL2NsaS9jbGkiLCJwYXRoIjoiLmdpdGh1Yi93b3JrZmxvd3MvZGVwbG95bWVudC55bWwifX0sImludGVybmFsUGFyYW1ldGVycyI6eyJnaXRodWIiOnsiZXZlbnRfbmFtZSI6IndvcmtmbG93X2Rpc3BhdGNoIiwicmVwb3NpdG9yeV9pZCI6IjIxMjYxMzA0OSIsInJlcG9zaXRvcnlfb3duZXJfaWQiOiI1OTcwNDcxMSJ9fSwicmVzb2x2ZWREZXBlbmRlbmNpZXMiOlt7InVyaSI6ImdpdCtodHRwczovL2dpdGh1Yi5jb20vY2xpL2NsaUByZWZzL2hlYWRzL3RydW5rIiwiZGlnZXN0Ijp7ImdpdENvbW1pdCI6ImZhZWYyZGRkODFiMDczNjc0ODQxM2E3YzY0NmNkMGJmYzI2YzAwYTAifX1dfSwicnVuRGV0YWlscyI6eyJidWlsZGVyIjp7ImlkIjoiaHR0cHM6Ly9naXRodWIuY29tL2FjdGlvbnMvcnVubmVyL2dpdGh1Yi1ob3N0ZWQifSwibWV0YWRhdGEiOnsiaW52b2NhdGlvbklkIjoiaHR0cHM6Ly9naXRodWIuY29tL2NsaS9jbGkvYWN0aW9ucy9ydW5zLzkyODkwNzU3NTIvYXR0ZW1wdHMvMSJ9fX19",
"payloadType": "application/vnd.in-toto+json",
"signatures": [
{
"sig": "MEQCIEGIGAm7gZVLLpsrPcjndEjiuctE2/c9+j9KGvazz3rlAiAd6O16T5hkzRM3IbRPzm+xT40mNQZxefd7laDP6x2XLQ=="
}
]
}
},
"repository_id": 1
}
]
}`

---

# REST API endpoints for blocking users

> Use the REST API to block and unblock users in an organization.

## About blocking users

The token used to authenticate the call must have the `admin:org` scope in order to make any blocking calls for an organization. Otherwise, the response returns `HTTP 404`.

---

# REST API endpoints for custom properties

> Use the REST API to create and manage custom properties for an organization.

## About custom properties

You can use the REST API to create and manage custom properties for an organization. You can use custom properties to add metadata to repositories in your organization. For more information, see [Managing custom properties for repositories in your organization](https://docs.github.com/en/organizations/managing-organization-settings/managing-custom-properties-for-repositories-in-your-organization).

---

# REST API endpoints for issue types

> Use the REST API to interact with issue types in an organization.

## List issue types for an organization

Lists all issue types for an organization. OAuth app tokens and personal access tokens (classic) need the read:org scope to use this endpoint.

### Fine-grained access tokens for "List issue types for an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Issue Types" organization permissions (read)

### Parameters for "List issue types for an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

### HTTP response status codes for "List issue types for an organization"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |

### Code samples for "List issue types for an organization"

#### Request example

get/orgs/{org}/issue-types

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/issue-types`

Response

-
-

`Status: 200``[
{
"id": 410,
"node_id": "IT_kwDNAd3NAZo",
"name": "Task",
"description": "A specific piece of work",
"created_at": "2024-12-11T14:39:09Z",
"updated_at": "2024-12-11T14:39:09Z"
},
{
"id": 411,
"node_id": "IT_kwDNAd3NAZs",
"name": "Bug",
"description": "An unexpected problem or behavior",
"created_at": "2024-12-11T14:39:09Z",
"updated_at": "2024-12-11T14:39:09Z"
}
]`

## Create issue type for an organization

Create a new issue type for an organization.

You can find out more about issue types in [Managing issue types in an organization](https://docs.github.com/issues/tracking-your-work-with-issues/configuring-issues/managing-issue-types-in-an-organization).

To use this endpoint, the authenticated user must be an administrator for the organization. OAuth app tokens and
personal access tokens (classic) need the `admin:org` scope to use this endpoint.

### Fine-grained access tokens for "Create issue type for an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Issue Types" organization permissions (write)

### Parameters for "Create issue type for an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| namestringRequiredName of the issue type. |
| is_enabledbooleanRequiredWhether or not the issue type is enabled at the organization level. |
| descriptionstring or nullDescription of the issue type. |
| colorstring or nullColor for the issue type.Can be one of:gray,blue,green,yellow,orange,red,pink,purple,null |

### HTTP response status codes for "Create issue type for an organization"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Create issue type for an organization"

#### Request example

post/orgs/{org}/issue-types

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/issue-types \
  -d '{"name":"Epic","description":"An issue type for a multi-week tracking of work","is_enabled":true,"color":"green"}'`

Response

-
-

`Status: 200``{
"id": 410,
"node_id": "IT_kwDNAd3NAZo",
"name": "Task",
"description": "A specific piece of work",
"created_at": "2024-12-11T14:39:09Z",
"updated_at": "2024-12-11T14:39:09Z"
}`

## Update issue type for an organization

Updates an issue type for an organization.

You can find out more about issue types in [Managing issue types in an organization](https://docs.github.com/issues/tracking-your-work-with-issues/configuring-issues/managing-issue-types-in-an-organization).

To use this endpoint, the authenticated user must be an administrator for the organization. OAuth app tokens and
personal access tokens (classic) need the `admin:org` scope to use this endpoint.

### Fine-grained access tokens for "Update issue type for an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Issue Types" organization permissions (write)

### Parameters for "Update issue type for an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| issue_type_idintegerRequiredThe unique identifier of the issue type. |

| Name, Type, Description |
| --- |
| namestringRequiredName of the issue type. |
| is_enabledbooleanRequiredWhether or not the issue type is enabled at the organization level. |
| descriptionstring or nullDescription of the issue type. |
| colorstring or nullColor for the issue type.Can be one of:gray,blue,green,yellow,orange,red,pink,purple,null |

### HTTP response status codes for "Update issue type for an organization"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Update issue type for an organization"

#### Request example

put/orgs/{org}/issue-types/{issue_type_id}

-
-
-

`curl -L \
  -X PUT \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/issue-types/ISSUE_TYPE_ID \
  -d '{"name":"Epic","description":"An issue type for a multi-week tracking of work","is_enabled":true,"color":"green"}'`

Response

-
-

`Status: 200``{
"id": 410,
"node_id": "IT_kwDNAd3NAZo",
"name": "Task",
"description": "A specific piece of work",
"created_at": "2024-12-11T14:39:09Z",
"updated_at": "2024-12-11T14:39:09Z"
}`

## Delete issue type for an organization

Deletes an issue type for an organization.

You can find out more about issue types in [Managing issue types in an organization](https://docs.github.com/issues/tracking-your-work-with-issues/configuring-issues/managing-issue-types-in-an-organization).

To use this endpoint, the authenticated user must be an administrator for the organization. OAuth app tokens and
personal access tokens (classic) need the `admin:org` scope to use this endpoint.

### Fine-grained access tokens for "Delete issue type for an organization"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Issue Types" organization permissions (write)

### Parameters for "Delete issue type for an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization name. The name is not case sensitive. |
| issue_type_idintegerRequiredThe unique identifier of the issue type. |

### HTTP response status codes for "Delete issue type for an organization"

| Status code | Description |
| --- | --- |
| 204 | No Content |
| 404 | Resource not found |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Delete issue type for an organization"

#### Request example

delete/orgs/{org}/issue-types/{issue_type_id}

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/ORG/issue-types/ISSUE_TYPE_ID`

Response

`Status: 204`
