# REST API endpoints for community metrics and more

# REST API endpoints for community metrics

> Use the REST API to retrieve information about your community profile.

## Get community profile metrics

Returns all community profile metrics for a repository. The repository cannot be a fork.

The returned metrics include an overall health score, the repository description, the presence of documentation, the
detected code of conduct, the detected license, and the presence of ISSUE_TEMPLATE, PULL_REQUEST_TEMPLATE,
README, and CONTRIBUTING files.

The `health_percentage` score is defined as a percentage of how many of
the recommended community health files are present. For more information, see
"[About community profiles for public repositories](https://docs.github.com/communities/setting-up-your-project-for-healthy-contributions/about-community-profiles-for-public-repositories)."

`content_reports_enabled` is only returned for organization-owned repositories.

### Fine-grained access tokens for "Get community profile metrics"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Contents" repository permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "Get community profile metrics"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

### HTTP response status codes for "Get community profile metrics"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "Get community profile metrics"

#### Request example

get/repos/{owner}/{repo}/community/profile

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/community/profile`

Response

-
-

`Status: 200``{
"health_percentage": 100,
"description": "My first repository on GitHub!",
"documentation": null,
"files": {
"code_of_conduct": {
"name": "Contributor Covenant",
"key": "contributor_covenant",
"url": "https://api.github.com/codes_of_conduct/contributor_covenant",
"html_url": "https://github.com/octocat/Hello-World/blob/master/CODE_OF_CONDUCT.md"
},
"code_of_conduct_file": {
"url": "https://api.github.com/repos/octocat/Hello-World/contents/CODE_OF_CONDUCT.md",
"html_url": "https://github.com/octocat/Hello-World/blob/master/CODE_OF_CONDUCT.md"
},
"contributing": {
"url": "https://api.github.com/repos/octocat/Hello-World/contents/CONTRIBUTING",
"html_url": "https://github.com/octocat/Hello-World/blob/master/CONTRIBUTING"
},
"issue_template": {
"url": "https://api.github.com/repos/octocat/Hello-World/contents/ISSUE_TEMPLATE",
"html_url": "https://github.com/octocat/Hello-World/blob/master/ISSUE_TEMPLATE"
},
"pull_request_template": {
"url": "https://api.github.com/repos/octocat/Hello-World/contents/PULL_REQUEST_TEMPLATE",
"html_url": "https://github.com/octocat/Hello-World/blob/master/PULL_REQUEST_TEMPLATE"
},
"license": {
"name": "MIT License",
"key": "mit",
"spdx_id": "MIT",
"url": "https://api.github.com/licenses/mit",
"html_url": "https://github.com/octocat/Hello-World/blob/master/LICENSE",
"node_id": "MDc6TGljZW5zZW1pdA=="
},
"readme": {
"url": "https://api.github.com/repos/octocat/Hello-World/contents/README.md",
"html_url": "https://github.com/octocat/Hello-World/blob/master/README.md"
}
},
"updated_at": "2017-02-28T19:09:29Z",
"content_reports_enabled": true
}`

---

# REST API endpoints for repository statistics

> Use the REST API to fetch the data that GitHub uses for visualizing different types of repository activity.

## About repository statistics

You can use the REST API to fetch the data that GitHub uses for visualizing different types of repository activity.

### Best practices for caching

Computing repository statistics is an expensive operation, so we try to return cached
data whenever possible. If the data hasn't been cached when you query a repository's
statistics, you'll receive a `202` response; a background job is also fired to
start compiling these statistics. You should allow the job a short time to complete, and
then submit the request again. If the job has completed, that request will receive a
`200` response with the statistics in the response body.

Repository statistics are cached by the SHA of the repository's default branch; pushing to the default branch resets the statistics cache.

### Statistics exclude some types of commits

The statistics exposed by the API match the statistics shown by [different repository graphs](https://docs.github.com/en/repositories/viewing-activity-and-data-for-your-repository/about-repository-graphs).

To summarize this:

- All statistics exclude merge commits.
- Contributor statistics also exclude empty commits.

---

# REST API endpoints for repository traffic

> Use the REST API to retrieve information provided in your repository graph.

## About repository traffic

You can use these endpoints to retrieve information provided in your repository graph, for repositories that you have write access to. For more information, see [Viewing traffic to a repository](https://docs.github.com/en/repositories/viewing-activity-and-data-for-your-repository/viewing-traffic-to-a-repository).
