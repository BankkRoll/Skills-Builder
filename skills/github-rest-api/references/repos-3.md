# REST API endpoints for rule suites

# REST API endpoints for rule suites

> Use the REST API to manage rule suites for repositories.

## List repository rule suites

Lists suites of rule evaluations at the repository level.
For more information, see "[Managing rulesets for a repository](https://docs.github.com/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/managing-rulesets-for-a-repository#viewing-insights-for-rulesets)."

### Fine-grained access tokens for "List repository rule suites"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "List repository rule suites"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| refstringThe name of the ref. Cannot contain wildcard characters. Optionally prefix withrefs/heads/to limit to branches orrefs/tags/to limit to tags. Omit the prefix to search across all refs. When specified, only rule evaluations triggered for this ref will be returned. |
| time_periodstringThe time period to filter by.For example,daywill filter for rule suites that occurred in the past 24 hours, andweekwill filter for rule suites that occurred in the past 7 days (168 hours).Default:dayCan be one of:hour,day,week,month |
| actor_namestringThe handle for the GitHub user account to filter on. When specified, only rule evaluations triggered by this actor will be returned. |
| rule_suite_resultstringThe rule suite results to filter on. When specified, only suites with this result will be returned.Default:allCan be one of:pass,fail,bypass,all |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| pageintegerThe page number of the results to fetch. For more information, see "Using pagination in the REST API."Default:1 |

### HTTP response status codes for "List repository rule suites"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |
| 500 | Internal Error |

### Code samples for "List repository rule suites"

#### Request example

get/repos/{owner}/{repo}/rulesets/rule-suites

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/rulesets/rule-suites`

Response

-
-

`Status: 200``[
{
"id": 21,
"actor_id": 12,
"actor_name": "octocat",
"before_sha": "893f768e172fb1bc9c5d6f3dd48557e45f14e01d",
"after_sha": "dedd88641a362b6b4ea872da4847d6131a164d01",
"ref": "refs/heads/i-see-everything",
"repository_id": 404,
"repository_name": "octo-repo",
"pushed_at": "2023-07-06T08:43:03Z",
"result": "bypass"
},
{
"id": 25,
"actor_id": 11,
"actor_name": "not-octocat",
"before_sha": "48994e4e01ccc943624c6231f172702b82b233cc",
"after_sha": "ecfd5a1025fa271a33ca5608d089476a2df3c9a1",
"ref": "refs/heads/i-am-everything",
"repository_id": 404,
"repository_name": "octo-repo",
"pushed_at": "2023-07-07T08:43:03Z",
"result": "pass",
"evaluation_result": "fail"
}
]`

## Get a repository rule suite

Gets information about a suite of rule evaluations from within a repository.
For more information, see "[Managing rulesets for a repository](https://docs.github.com/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/managing-rulesets-for-a-repository#viewing-insights-for-rulesets)."

### Fine-grained access tokens for "Get a repository rule suite"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Get a repository rule suite"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| rule_suite_idintegerRequiredThe unique identifier of the rule suite result.
To get this ID, you can useGET /repos/{owner}/{repo}/rulesets/rule-suitesfor repositories andGET /orgs/{org}/rulesets/rule-suitesfor organizations. |

### HTTP response status codes for "Get a repository rule suite"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |
| 500 | Internal Error |

### Code samples for "Get a repository rule suite"

#### Request example

get/repos/{owner}/{repo}/rulesets/rule-suites/{rule_suite_id}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/rulesets/rule-suites/RULE_SUITE_ID`

Response

-
-

`Status: 200``{
"id": 21,
"actor_id": 12,
"actor_name": "octocat",
"before_sha": "893f768e172fb1bc9c5d6f3dd48557e45f14e01d",
"after_sha": "dedd88641a362b6b4ea872da4847d6131a164d01",
"ref": "refs/heads/i-see-everything",
"repository_id": 404,
"repository_name": "octo-repo",
"pushed_at": "2023-07-06T08:43:03Z",
"result": "bypass",
"evaluation_result": "fail",
"rule_evaluations": [
{
"rule_source": {
"type": "ruleset",
"id": 2,
"name": "Author email must be a GitHub email address"
},
"enforcement": "active",
"result": "pass",
"rule_type": "commit_author_email_pattern"
},
{
"rule_source": {
"type": "protected_branch"
},
"enforcement": "active",
"result": "fail",
"rule_type": "pull_request",
"details": "Changes must be made through a pull request."
},
{
"rule_source": {
"type": "ruleset",
"id": 3,
"name": "Evaluate commit message pattern"
},
"enforcement": "evaluate",
"result": "fail",
"rule_type": "commit_message_pattern"
}
]
}`
