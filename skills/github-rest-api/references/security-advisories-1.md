# REST API endpoints for global security advisories

# REST API endpoints for global security advisories

> Use the REST API to view global security advisories.

## List global security advisories

Lists all global security advisories that match the specified parameters. If no other parameters are defined, the request will return only GitHub-reviewed advisories that are not malware.

By default, all responses will exclude advisories for malware, because malware are not standard vulnerabilities. To list advisories for malware, you must include the `type` parameter in your request, with the value `malware`. For more information about the different types of security advisories, see "[About the GitHub Advisory database](https://docs.github.com/code-security/security-advisories/global-security-advisories/about-the-github-advisory-database#about-types-of-security-advisories)."

### Fine-grained access tokens for "List global security advisories"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token does not require any permissions.

This endpoint can be used without authentication if only public resources are requested.

### Parameters for "List global security advisories"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ghsa_idstringIf specified, only advisories with this GHSA (GitHub Security Advisory) identifier will be returned. |
| typestringIf specified, only advisories of this type will be returned. By default, a request with no other parameters defined will only return reviewed advisories that are not malware.Default:reviewedCan be one of:reviewed,malware,unreviewed |
| cve_idstringIf specified, only advisories with this CVE (Common Vulnerabilities and Exposures) identifier will be returned. |
| ecosystemstringIf specified, only advisories for these ecosystems will be returned.Can be one of:rubygems,npm,pip,maven,nuget,composer,go,rust,erlang,actions,pub,other,swift |
| severitystringIf specified, only advisories with these severities will be returned.Can be one of:unknown,low,medium,high,critical |
| cwesIf specified, only advisories with these Common Weakness Enumerations (CWEs) will be returned.Example:cwes=79,284,22orcwes[]=79&cwes[]=284&cwes[]=22 |
| is_withdrawnbooleanWhether to only return advisories that have been withdrawn. |
| affectsIf specified, only return advisories that affect any ofpackageorpackage@version. A maximum of 1000 packages can be specified.
If the query parameter causes the URL to exceed the maximum URL length supported by your client, you must specify fewer packages.Example:affects=package1,package2@1.0.0,package3@2.0.0oraffects[]=package1&affects[]=package2@1.0.0 |
| publishedstringIf specified, only return advisories that were published on a date or date range.For more information on the syntax of the date range, see "Understanding the search syntax." |
| updatedstringIf specified, only return advisories that were updated on a date or date range.For more information on the syntax of the date range, see "Understanding the search syntax." |
| modifiedstringIf specified, only show advisories that were updated or published on a date or date range.For more information on the syntax of the date range, see "Understanding the search syntax." |
| epss_percentagestringIf specified, only return advisories that have an EPSS percentage score that matches the provided value.
The EPSS percentage represents the likelihood of a CVE being exploited. |
| epss_percentilestringIf specified, only return advisories that have an EPSS percentile score that matches the provided value.
The EPSS percentile represents the relative rank of the CVE's likelihood of being exploited compared to other CVEs. |
| beforestringA cursor, as given in theLink header. If specified, the query only searches for results before this cursor. For more information, see "Using pagination in the REST API." |
| afterstringA cursor, as given in theLink header. If specified, the query only searches for results after this cursor. For more information, see "Using pagination in the REST API." |
| directionstringThe direction to sort the results by.Default:descCan be one of:asc,desc |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| sortstringThe property to sort the results by.Default:publishedCan be one of:updated,published,epss_percentage,epss_percentile |

### HTTP response status codes for "List global security advisories"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 422 | Validation failed, or the endpoint has been spammed. |
| 429 | Too many requests |

### Code samples for "List global security advisories"

#### Request example

get/advisories

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/advisories`

Response

-
-

`Status: 200``[
{
"id": 1,
"ghsa_id": "GHSA-abcd-1234-efgh",
"cve_id": "CVE-2050-00000",
"url": "https://api.github.com/advisories/GHSA-abcd-1234-efgh",
"html_url": "https://github.com/advisories/GHSA-abcd-1234-efgh",
"repository_advisory_url": "https://api.github.com/repos/project/a-package/security-advisories/GHSA-abcd-1234-efgh",
"summary": "Heartbleed security advisory",
"description": "This bug allows an attacker to read portions of the affected server’s memory, potentially disclosing sensitive information.",
"type": "reviewed",
"severity": "high",
"source_code_location": "https://github.com/project/a-package",
"identifiers": [
{
"type": "GHSA",
"value": "GHSA-abcd-1234-efgh"
},
{
"type": "CVE",
"value": "CVE-2050-00000"
}
],
"references": [
"https://nvd.nist.gov/vuln/detail/CVE-2050-00000"
],
"published_at": "2023-03-23T02:30:56Z",
"updated_at": "2023-03-24T02:30:56Z",
"github_reviewed_at": "2023-03-23T02:30:56Z",
"nvd_published_at": "2023-03-25T02:30:56Z",
"withdrawn_at": null,
"vulnerabilities": [
{
"package": {
"ecosystem": "npm",
"name": "a-package"
},
"first_patched_version": "1.0.3",
"vulnerable_version_range": "<=1.0.2",
"vulnerable_functions": [
"a_function"
]
}
],
"cvss": {
"vector_string": "CVSS:3.1/AV:N/AC:H/PR:H/UI:R/S:C/C:H/I:H/A:H",
"score": 7.6
},
"cvss_severities": {
"cvss_v3": {
"vector_string": "CVSS:3.1/AV:N/AC:H/PR:H/UI:R/S:C/C:H/I:H/A:H",
"score": 7.6
},
"cvss_v4": {
"vector_string": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N",
"score": 9.3
}
},
"cwes": [
{
"cwe_id": "CWE-400",
"name": "Uncontrolled Resource Consumption"
}
],
"epss": [
{
"percentage": 0.00045,
"percentile": "0.16001e0"
}
],
"credits": [
{
"user": {
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
"type": "analyst"
}
]
}
]`

## Get a global security advisory

Gets a global security advisory using its GitHub Security Advisory (GHSA) identifier.

### Fine-grained access tokens for "Get a global security advisory"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token does not require any permissions.

This endpoint can be used without authentication if only public resources are requested.

### Parameters for "Get a global security advisory"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ghsa_idstringRequiredThe GHSA (GitHub Security Advisory) identifier of the advisory. |

### HTTP response status codes for "Get a global security advisory"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |

### Code samples for "Get a global security advisory"

#### Request example

get/advisories/{ghsa_id}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/advisories/GHSA_ID`

Response

-
-

`Status: 200``{
"ghsa_id": "GHSA-abcd-1234-efgh",
"cve_id": "CVE-2050-00000",
"url": "https://api.github.com/advisories/GHSA-abcd-1234-efgh",
"html_url": "https://github.com/advisories/GHSA-abcd-1234-efgh",
"repository_advisory_url": "https://api.github.com/repos/project/a-package/security-advisories/GHSA-abcd-1234-efgh",
"summary": "A short summary of the advisory.",
"description": "A detailed description of what the advisory entails.",
"type": "reviewed",
"severity": "high",
"source_code_location": "https://github.com/project/a-package",
"identifiers": [
{
"type": "GHSA",
"value": "GHSA-abcd-1234-efgh"
},
{
"type": "CVE",
"value": "CVE-2050-00000"
}
],
"references": [
"https://nvd.nist.gov/vuln/detail/CVE-2050-00000"
],
"published_at": "2023-03-23T02:30:56Z",
"updated_at": "2023-03-24T02:30:56Z",
"github_reviewed_at": "2023-03-23T02:30:56Z",
"nvd_published_at": "2023-03-25T02:30:56Z",
"withdrawn_at": null,
"vulnerabilities": [
{
"package": {
"ecosystem": "npm",
"name": "a-package"
},
"first_patched_version": "1.0.3",
"vulnerable_version_range": "<=1.0.2",
"vulnerable_functions": [
"a_function"
]
}
],
"cvss": {
"vector_string": "CVSS:3.1/AV:N/AC:H/PR:H/UI:R/S:C/C:H/I:H/A:H",
"score": 7.6
},
"cvss_severities": {
"cvss_v3": {
"vector_string": "CVSS:3.1/AV:N/AC:H/PR:H/UI:R/S:C/C:H/I:H/A:H",
"score": 7.6
},
"cvss_v4": {
"vector_string": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N",
"score": 9.3
}
},
"cwes": [
{
"cwe_id": "CWE-400",
"name": "Uncontrolled Resource Consumption"
}
],
"credits": [
{
"user": {
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
"type": "analyst"
}
]
}`
