# REST API endpoints for deployment branch policies and more

# REST API endpoints for deployment branch policies

> Use the REST API to manage custom deployment branch policies.

## About deployment branch policies

You can use the REST API to specify custom name patterns that branches must match in order to deploy to an environment. The `deployment_branch_policy.custom_branch_policies` property for the environment must be set to `true` to use these endpoints. To update the `deployment_branch_policy` for an environment, see [REST API endpoints for deployment environments](https://docs.github.com/en/rest/deployments/environments#create-or-update-an-environment).

For more information about restricting environment deployments to certain branches, see [Managing environments for deployment](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment#deployment-branches).

---

# REST API endpoints for deployments

> Use the REST API to create and delete deployments and deployment environments.

## About deployments

Deployments are requests to deploy a specific ref (branch, SHA, tag). GitHub dispatches a [deploymentevent](https://docs.github.com/en/webhooks-and-events/webhooks/webhook-events-and-payloads#deployment) that external services can listen for and act on when new deployments are created. Deployments enable developers and organizations to build loosely coupled tooling around deployments, without having to worry about the implementation details of delivering different types of applications (e.g., web, native).

Deployment statuses allow external services to mark deployments with an `error`, `failure`, `pending`, `in_progress`, `queued`, or `success` state that systems listening to [deployment_statusevents](https://docs.github.com/en/webhooks-and-events/webhooks/webhook-events-and-payloads#deployment_status) can consume.

Deployment statuses can also include an optional `description` and `log_url`, which are highly recommended because they make deployment statuses more useful. The `log_url` is the full URL to the deployment output, and
the `description` is a high-level summary of what happened with the deployment.

GitHub dispatches `deployment` and `deployment_status` events when new deployments and deployment statuses are created. These events allow third-party integrations to receive and respond to deployment requests, and update the status of a deployment as progress is made.

Below is a simple sequence diagram for how these interactions would work.

```text
+---------+             +--------+            +-----------+        +-------------+
| Tooling |             | GitHub |            | 3rd Party |        | Your Server |
+---------+             +--------+            +-----------+        +-------------+
     |                      |                       |                     |
     |  Create Deployment   |                       |                     |
     |--------------------->|                       |                     |
     |                      |                       |                     |
     |  Deployment Created  |                       |                     |
     |<---------------------|                       |                     |
     |                      |                       |                     |
     |                      |   Deployment Event    |                     |
     |                      |---------------------->|                     |
     |                      |                       |     SSH+Deploys     |
     |                      |                       |-------------------->|
     |                      |                       |                     |
     |                      |   Deployment Status   |                     |
     |                      |<----------------------|                     |
     |                      |                       |                     |
     |                      |                       |   Deploy Completed  |
     |                      |                       |<--------------------|
     |                      |                       |                     |
     |                      |   Deployment Status   |                     |
     |                      |<----------------------|                     |
     |                      |                       |                     |
```

Keep in mind that GitHub is never actually accessing your servers. It's up to your third-party integration to interact with deployment events. Multiple systems can listen for deployment events, and it's up to each of those systems to decide whether they're responsible for pushing the code out to your servers, building native code, etc.

Note that the `repo_deployment` [OAuth scope](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/scopes-for-oauth-apps) grants targeted access to deployments and deployment statuses **without** granting access to repository code, while the `public_repo` and `repo` scopes grant permission to code as well.

### Inactive deployments

When you set the state of a deployment to `success`, then all prior non-transient, non-production environment deployments in the same repository with the same environment name will become `inactive`. To avoid this, you can set `auto_inactive` to `false` when creating the deployment status.

You can communicate that a transient environment no longer exists by setting its `state` to `inactive`. Setting the `state` to `inactive` shows the deployment as `destroyed` in GitHub and removes access to it.

---

# REST API endpoints for deployment environments

> Use the REST API to create, configure, and delete deployment environments.

## About deployment environments

For more information about environments, see [Managing environments for deployment](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment). To manage environment secrets, see [REST API endpoints for GitHub Actions Secrets](https://docs.github.com/en/rest/actions/secrets).

Environments, environment secrets, and deployment protection rules are available in public repositories for all current GitHub plans. They are not available on legacy plans, such as Bronze, Silver, or Gold. For access to environments, environment secrets, and deployment branches in private or internal repositories, you must use GitHub Pro, GitHub Team, or GitHub Enterprise. If you are on a GitHub Free, GitHub Pro, or GitHub Team plan, other deployment protection rules, such as a wait timer or required reviewers, are only available for public repositories.

---

# REST API endpoints for protection rules

> Use the REST API to create, configure, and delete deployment protection rules.

## Get all deployment protection rules for an environment

Gets all custom deployment protection rules that are enabled for an environment. Anyone with read access to the repository can use this endpoint. For more information about environments, see "[Using environments for deployment](https://docs.github.com/actions/deployment/targeting-different-environments/using-environments-for-deployment)."

For more information about the app that is providing this custom deployment rule, see the [documentation for theGET /apps/{app_slug}endpoint](https://docs.github.com/rest/apps/apps#get-an-app).

OAuth app tokens and personal access tokens (classic) need the `repo` scope to use this endpoint with a private repository.

### Fine-grained access tokens for "Get all deployment protection rules for an environment"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Actions" repository permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "Get all deployment protection rules for an environment"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| environment_namestringRequiredThe name of the environment. The name must be URL encoded. For example, any slashes in the name must be replaced with%2F. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |

### HTTP response status codes for "Get all deployment protection rules for an environment"

| Status code | Description |
| --- | --- |
| 200 | List of deployment protection rules |

### Code samples for "Get all deployment protection rules for an environment"

#### Request example

get/repos/{owner}/{repo}/environments/{environment_name}/deployment_protection_rules

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/environments/ENVIRONMENT_NAME/deployment_protection_rules`

List of deployment protection rules

-
-

`Status: 200``{
"total_count": 2,
"custom_deployment_protection_rules": [
{
"id": 3,
"node_id": "IEH37kRlcGxveW1lbnRTdGF0ddiv",
"enabled": true,
"app": {
"id": 1,
"node_id": "GHT58kRlcGxveW1lbnRTdTY!bbcy",
"slug": "a-custom-app",
"integration_url": "https://api.github.com/apps/a-custom-app"
}
},
{
"id": 4,
"node_id": "MDE2OkRlcGxveW1lbnRTdHJ41128",
"enabled": true,
"app": {
"id": 1,
"node_id": "UHVE67RlcGxveW1lbnRTdTY!jfeuy",
"slug": "another-custom-app",
"integration_url": "https://api.github.com/apps/another-custom-app"
}
}
]
}`

## Create a custom deployment protection rule on an environment

Enable a custom deployment protection rule for an environment.

The authenticated user must have admin or owner permissions to the repository to use this endpoint.

For more information about the app that is providing this custom deployment rule, see the [documentation for theGET /apps/{app_slug}endpoint](https://docs.github.com/rest/apps/apps#get-an-app), as well as the [guide to creating custom deployment protection rules](https://docs.github.com/actions/managing-workflow-runs-and-deployments/managing-deployments/creating-custom-deployment-protection-rules).

OAuth app tokens and personal access tokens (classic) need the `repo` scope to use this endpoint.

### Fine-grained access tokens for "Create a custom deployment protection rule on an environment"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Create a custom deployment protection rule on an environment"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| environment_namestringRequiredThe name of the environment. The name must be URL encoded. For example, any slashes in the name must be replaced with%2F. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| integration_idintegerThe ID of the custom app that will be enabled on the environment. |

### HTTP response status codes for "Create a custom deployment protection rule on an environment"

| Status code | Description |
| --- | --- |
| 201 | The enabled custom deployment protection rule |

### Code samples for "Create a custom deployment protection rule on an environment"

#### Request example

post/repos/{owner}/{repo}/environments/{environment_name}/deployment_protection_rules

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/environments/ENVIRONMENT_NAME/deployment_protection_rules \
  -d '{"integration_id":5}'`

The enabled custom deployment protection rule

-
-

`Status: 201``{
"id": 3,
"node_id": "IEH37kRlcGxveW1lbnRTdGF0ddiv",
"enabled": true,
"app": {
"id": 1,
"node_id": "GHT58kRlcGxveW1lbnRTdTY!bbcy",
"slug": "a-custom-app",
"integration_url": "https://api.github.com/apps/a-custom-app"
}
}`

## List custom deployment rule integrations available for an environment

Gets all custom deployment protection rule integrations that are available for an environment.

The authenticated user must have admin or owner permissions to the repository to use this endpoint.

For more information about environments, see "[Using environments for deployment](https://docs.github.com/actions/deployment/targeting-different-environments/using-environments-for-deployment)."

For more information about the app that is providing this custom deployment rule, see "[GET an app](https://docs.github.com/rest/apps/apps#get-an-app)".

OAuth app tokens and personal access tokens (classic) need the `repo` scope to use this endpoint with a private repository.

### Fine-grained access tokens for "List custom deployment rule integrations available for an environment"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (read)

### Parameters for "List custom deployment rule integrations available for an environment"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| environment_namestringRequiredThe name of the environment. The name must be URL encoded. For example, any slashes in the name must be replaced with%2F. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| pageintegerThe page number of the results to fetch. For more information, see "Using pagination in the REST API."Default:1 |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |

### HTTP response status codes for "List custom deployment rule integrations available for an environment"

| Status code | Description |
| --- | --- |
| 200 | A list of custom deployment rule integrations available for this environment. |

### Code samples for "List custom deployment rule integrations available for an environment"

#### Request example

get/repos/{owner}/{repo}/environments/{environment_name}/deployment_protection_rules/apps

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/environments/ENVIRONMENT_NAME/deployment_protection_rules/apps`

A list of custom deployment rule integrations available for this environment.

-
-

`Status: 200``[
{
"total_count": 2
},
{
"available_custom_deployment_protection_rule_integrations": [
{
"id": 1,
"node_id": "GHT58kRlcGxveW1lbnRTdTY!bbcy",
"slug": "a-custom-app",
"integration_url": "https://api.github.com/apps/a-custom-app"
},
{
"id": 2,
"node_id": "UHVE67RlcGxveW1lbnRTdTY!jfeuy",
"slug": "another-custom-app",
"integration_url": "https://api.github.com/apps/another-custom-app"
}
]
}
]`

## Get a custom deployment protection rule

Gets an enabled custom deployment protection rule for an environment. Anyone with read access to the repository can use this endpoint. For more information about environments, see "[Using environments for deployment](https://docs.github.com/actions/deployment/targeting-different-environments/using-environments-for-deployment)."

For more information about the app that is providing this custom deployment rule, see [GET /apps/{app_slug}](https://docs.github.com/rest/apps/apps#get-an-app).

OAuth app tokens and personal access tokens (classic) need the `repo` scope to use this endpoint with a private repository.

### Fine-grained access tokens for "Get a custom deployment protection rule"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Actions" repository permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "Get a custom deployment protection rule"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| environment_namestringRequiredThe name of the environment. The name must be URL encoded. For example, any slashes in the name must be replaced with%2F. |
| protection_rule_idintegerRequiredThe unique identifier of the protection rule. |

### HTTP response status codes for "Get a custom deployment protection rule"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "Get a custom deployment protection rule"

#### Request example

get/repos/{owner}/{repo}/environments/{environment_name}/deployment_protection_rules/{protection_rule_id}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/environments/ENVIRONMENT_NAME/deployment_protection_rules/PROTECTION_RULE_ID`

Response

-
-

`Status: 200``{
"id": 3,
"node_id": "IEH37kRlcGxveW1lbnRTdGF0ddiv",
"enabled": true,
"app": {
"id": 1,
"node_id": "GHT58kRlcGxveW1lbnRTdTY!bbcy",
"slug": "a-custom-app",
"integration_url": "https://api.github.com/apps/a-custom-app"
}
}`

## Disable a custom protection rule for an environment

Disables a custom deployment protection rule for an environment.

The authenticated user must have admin or owner permissions to the repository to use this endpoint.

OAuth app tokens and personal access tokens (classic) need the `repo` scope to use this endpoint.

### Fine-grained access tokens for "Disable a custom protection rule for an environment"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Disable a custom protection rule for an environment"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| environment_namestringRequiredThe name of the environment. The name must be URL encoded. For example, any slashes in the name must be replaced with%2F. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| protection_rule_idintegerRequiredThe unique identifier of the protection rule. |

### HTTP response status codes for "Disable a custom protection rule for an environment"

| Status code | Description |
| --- | --- |
| 204 | No Content |

### Code samples for "Disable a custom protection rule for an environment"

#### Request example

delete/repos/{owner}/{repo}/environments/{environment_name}/deployment_protection_rules/{protection_rule_id}

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/environments/ENVIRONMENT_NAME/deployment_protection_rules/PROTECTION_RULE_ID`

Response

`Status: 204`

---

# REST API endpoints for deployment statuses

> Use the REST API to manage deployment statuses.

## List deployment statuses

Users with pull access can view deployment statuses for a deployment:

### Fine-grained access tokens for "List deployment statuses"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Deployments" repository permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "List deployment statuses"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| deployment_idintegerRequireddeployment_id parameter |

| Name, Type, Description |
| --- |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| pageintegerThe page number of the results to fetch. For more information, see "Using pagination in the REST API."Default:1 |

### HTTP response status codes for "List deployment statuses"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |

### Code samples for "List deployment statuses"

#### Request example

get/repos/{owner}/{repo}/deployments/{deployment_id}/statuses

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/deployments/DEPLOYMENT_ID/statuses`

Response

-
-

`Status: 200``[
{
"url": "https://api.github.com/repos/octocat/example/deployments/42/statuses/1",
"id": 1,
"node_id": "MDE2OkRlcGxveW1lbnRTdGF0dXMx",
"state": "success",
"creator": {
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
"description": "Deployment finished successfully.",
"environment": "production",
"target_url": "https://example.com/deployment/42/output",
"created_at": "2012-07-20T01:19:13Z",
"updated_at": "2012-07-20T01:19:13Z",
"deployment_url": "https://api.github.com/repos/octocat/example/deployments/42",
"repository_url": "https://api.github.com/repos/octocat/example",
"environment_url": "https://test-branch.lab.acme.com",
"log_url": "https://example.com/deployment/42/output"
}
]`

## Create a deployment status

Users with `push` access can create deployment statuses for a given deployment.

OAuth app tokens and personal access tokens (classic) need the `repo_deployment` scope to use this endpoint.

### Fine-grained access tokens for "Create a deployment status"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Deployments" repository permissions (write)

### Parameters for "Create a deployment status"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| deployment_idintegerRequireddeployment_id parameter |

| Name, Type, Description |
| --- |
| statestringRequiredThe state of the status. When you set a transient deployment toinactive, the deployment will be shown asdestroyedin GitHub.Can be one of:error,failure,inactive,in_progress,queued,pending,success |
| target_urlstringThe target URL to associate with this status. This URL should contain output to keep the user updated while the task is running or serve as historical information for what happened in the deployment.NoteIt's recommended to use thelog_urlparameter, which replacestarget_url.Default:"" |
| log_urlstringThe full URL of the deployment's output. This parameter replacestarget_url. We will continue to accepttarget_urlto support legacy uses, but we recommend replacingtarget_urlwithlog_url. Settinglog_urlwill automatically settarget_urlto the same value. Default:""Default:"" |
| descriptionstringA short description of the status. The maximum description length is 140 characters.Default:"" |
| environmentstringName for the target deployment environment, which can be changed when setting a deploy status. For example,production,staging, orqa. If not defined, the environment of the previous status on the deployment will be used, if it exists. Otherwise, the environment of the deployment will be used. |
| environment_urlstringSets the URL for accessing your environment. Default:""Default:"" |
| auto_inactivebooleanAdds a newinactivestatus to all prior non-transient, non-production environment deployments with the same repository andenvironmentname as the created status's deployment. Aninactivestatus is only added to deployments that had asuccessstate. Default:true |

### HTTP response status codes for "Create a deployment status"

| Status code | Description |
| --- | --- |
| 201 | Created |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Create a deployment status"

#### Request example

post/repos/{owner}/{repo}/deployments/{deployment_id}/statuses

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/deployments/DEPLOYMENT_ID/statuses \
  -d '{"environment":"production","state":"success","log_url":"https://example.com/deployment/42/output","description":"Deployment finished successfully."}'`

Response

-
-

`Status: 201``{
"url": "https://api.github.com/repos/octocat/example/deployments/42/statuses/1",
"id": 1,
"node_id": "MDE2OkRlcGxveW1lbnRTdGF0dXMx",
"state": "success",
"creator": {
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
"description": "Deployment finished successfully.",
"environment": "production",
"target_url": "https://example.com/deployment/42/output",
"created_at": "2012-07-20T01:19:13Z",
"updated_at": "2012-07-20T01:19:13Z",
"deployment_url": "https://api.github.com/repos/octocat/example/deployments/42",
"repository_url": "https://api.github.com/repos/octocat/example",
"environment_url": "https://test-branch.lab.acme.com",
"log_url": "https://example.com/deployment/42/output"
}`

## Get a deployment status

Users with pull access can view a deployment status for a deployment:

### Fine-grained access tokens for "Get a deployment status"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Deployments" repository permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "Get a deployment status"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| deployment_idintegerRequireddeployment_id parameter |
| status_idintegerRequired |

### HTTP response status codes for "Get a deployment status"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |

### Code samples for "Get a deployment status"

#### Request example

get/repos/{owner}/{repo}/deployments/{deployment_id}/statuses/{status_id}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/deployments/DEPLOYMENT_ID/statuses/STATUS_ID`

Response

-
-

`Status: 200``{
"url": "https://api.github.com/repos/octocat/example/deployments/42/statuses/1",
"id": 1,
"node_id": "MDE2OkRlcGxveW1lbnRTdGF0dXMx",
"state": "success",
"creator": {
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
"description": "Deployment finished successfully.",
"environment": "production",
"target_url": "https://example.com/deployment/42/output",
"created_at": "2012-07-20T01:19:13Z",
"updated_at": "2012-07-20T01:19:13Z",
"deployment_url": "https://api.github.com/repos/octocat/example/deployments/42",
"repository_url": "https://api.github.com/repos/octocat/example",
"environment_url": "https://test-branch.lab.acme.com",
"log_url": "https://example.com/deployment/42/output"
}`
