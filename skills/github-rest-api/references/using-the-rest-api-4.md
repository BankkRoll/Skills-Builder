# Libraries for the REST API and more

# Libraries for the REST API

> You can use the official Octokit libraries and other third-party libraries to extend and simplify how you use the GitHub API.

## About libraries

You can use libraries to extend and simplify the way your application interacts with GitHub's API. Each library provides pre-built code for a specific programming language. After integrating a library into your project, you can use the pre-built code modules to interact with GitHub's API via a specific programming language.

GitHub maintains official Octokit libraries for some languages. There are also third-party libraries that you can use with GitHub's API, which are not maintained by GitHub.

## Official GitHub libraries

GitHub maintains these official client libraries for the GitHub API. These repositories are open source, and community contributions are welcome.

For more information, see [Scripting with the REST API and JavaScript](https://docs.github.com/en/rest/guides/scripting-with-the-rest-api-and-javascript) and [Scripting with the REST API and Ruby](https://docs.github.com/en/rest/guides/scripting-with-the-rest-api-and-ruby).

- JavaScript: [octokit.js](https://github.com/octokit/octokit.js)
- Ruby: [octokit.rb](https://github.com/octokit/octokit.rb)
- .NET: [octokit.net](https://github.com/octokit/octokit.net)
- Terraform: [terraform-provider-github](https://github.com/integrations/terraform-provider-github)

## Third-party libraries

The following are examples of third-party libraries that you can use to interact with the GitHub API in various programming languages.

These third-party libraries are not maintained by GitHub. Libraries provided by third parties are governed by separate terms of service, privacy policy, and support documentation.

### Clojure

- Tentacles: [clj-commons/tentacles](https://github.com/clj-commons/tentacles)

### Dart

- github.dart: [SpinlockLabs/github.dart](https://github.com/SpinlockLabs/github.dart)

### Emacs Lisp

- gh.el: [sigma/gh.el](https://github.com/sigma/gh.el)

### Go

- go-github: [google/go-github](https://github.com/google/go-github)

### Haskell

- haskell-github: [haskell-github/github](https://github.com/fpco/github)

### Java

- GitHub API for Java, an object oriented representation of the GitHub API: [hub4j/github-api](https://hub4j.github.io/github-api/)
- JCabi GitHub API, based on Java7 JSON API (JSR-353), simplifies tests with a runtime GitHub stub, and covers the entire API: [github.jcabi.com (Personal Website)](https://github.jcabi.com)

### JavaScript

- NodeJS GitHub library: [pksunkara/octonode](https://github.com/pksunkara/octonode)
- Github.js wrapper around the GitHub API: [github-tools/github](https://github.com/github-tools/github)
- Promise-Based CoffeeScript library for the Browser or NodeJS: [philschatz/github-client](https://github.com/philschatz/github-client)

### Julia

- GitHub.jl: [JuliaWeb/GitHub.jl](https://github.com/JuliaWeb/GitHub.jl)

### OCaml

- ocaml-github: [mirage/ocaml-github](https://github.com/mirage/ocaml-github)

### Perl

- Pithub: [plu/Pithub](https://github.com/plu/Pithub)
- Net::GitHub: [fayland/perl-net-github](https://github.com/fayland/perl-net-github)

### PHP

- PHP GitHub API: [KnpLabs/php-github-api](https://github.com/KnpLabs/php-github-api)
- GitHub Joomla! Package: [joomla-framework/github-api](https://github.com/joomla-framework/github-api)
- GitHub bridge for Laravel: [GrahamCampbell/Laravel-GitHub](https://github.com/GrahamCampbell/Laravel-GitHub)

### PowerShell

- PowerShellForGitHub: [microsoft/PowerShellForGitHub](https://github.com/microsoft/PowerShellForGitHub)

### Python

- gidgethub: [gidgethub/gidgethub](https://github.com/gidgethub/gidgethub)
- ghapi: [fastai/ghapi](https://github.com/fastai/ghapi)
- PyGithub: [PyGithub/PyGithub](https://github.com/PyGithub/PyGithub)
- libsaas: [duckboard/libsaas](https://github.com/ducksboard/libsaas)
- github3.py: [sigmavirus24/github3.py](https://github.com/sigmavirus24/github3.py)
- agithub: [mozilla/agithub](https://github.com/mozilla/agithub)
- github-flask: [github-flask (Official Website)](http://github-flask.readthedocs.org)
- githubkit: [yanyongyu/githubkit](https://github.com/yanyongyu/githubkit)
- octokit.py: [khornberg/octokit.py](https://github.com/khornberg/octokit.py)

### Ruby

- GitHub API Gem: [piotrmurach/github](https://github.com/piotrmurach/github)

### Rust

- Octocrab: [XAMPPRocky/octocrab](https://github.com/XAMPPRocky/octocrab)

### Scala

- Github4s: [47deg/github4s](https://github.com/47deg/github4s)

### Shell

- ok.sh: [whiteinge/ok.sh](https://github.com/whiteinge/ok.sh)

---

# Rate limits for the REST API

> Learn about REST API rate limits, how to avoid exceeding them, and what to do if you do exceed them.

## About primary rate limits

GitHub limits the number of REST API requests that you can make within a specific amount of time. This limit helps prevent abuse and denial-of-service attacks, and ensures that the API remains available for all users.

Some endpoints, like the search endpoints, have more restrictive limits. For more information about these endpoints, see [REST API endpoints for rate limits](https://docs.github.com/en/rest/rate-limit/rate-limit). The GraphQL API also has a separate primary rate limit. See [Rate limits and query limits for the GraphQL API](https://docs.github.com/en/graphql/overview/resource-limitations).

In general, you can calculate your primary rate limit for the REST API based on your method of authentication, as described below.

### Primary rate limit for unauthenticated users

You can make unauthenticated requests if you are only fetching public data. Unauthenticated requests are associated with the originating IP address, not with the user or application that made the request.

The primary rate limit for unauthenticated requests is 60 requests per hour.

### Primary rate limit for authenticated users

You can use a personal access token to make API requests. Additionally, you can authorize a GitHub App or OAuth app, which can then make API requests on your behalf.

All of these requests count towards your personal rate limit of 5,000 requests per hour. Requests made on your behalf by a GitHub App that is owned by a GitHub Enterprise Cloud organization have a higher rate limit of 15,000 requests per hour. Similarly, requests made on your behalf by a OAuth app that is owned or approved by a GitHub Enterprise Cloud organization have a higher rate limit of 15,000 requests per hour if you are a member of the GitHub Enterprise Cloud organization. However, requests made by a higher-limit app reduce the remaining budget available for lower-limit authentication methods. For example, if an app with a 15,000 request limit makes 10,000 requests on your behalf, you will have exhausted the 5,000 request budget for your personal access tokens, even though the app has 5,000 requests remaining.

### Primary rate limit for Git LFS access

API requests are required when you upload or download Git LFS content. These count towards a separate rate limiting bucket with a limit of 300 requests per minute for unauthenticated requests and 3,000 requests per minute for authenticated requests.

Git LFS uses a batch API which processes 100 Git LFS objects per API request by default. That means unauthenticated users can download 30,000 Git LFS objects per minute and authenticated users can upload/download 300,000 Git LFS objects per minute.

### Primary rate limit for GitHub App installations

GitHub Apps authenticating with an installation access token use the installation's minimum rate limit of 5,000 requests per hour. If the installation is on a GitHub Enterprise Cloud organization, the installation has a rate limit of 15,000 requests per hour.

For installations that are not on a GitHub Enterprise Cloud organization, the rate limit for the installation will scale with the number of users and repositories. Installations that have more than 20 repositories receive another 50 requests per hour for each repository. Installations that are on an organization that have more than 20 users receive another 50 requests per hour for each user. The rate limit cannot increase beyond 12,500 requests per hour.

Primary rate limits for GitHub App user access tokens (as opposed to installation access tokens) are dictated by the primary rate limits for the authenticated user. This rate limit is combined with any requests that another GitHub App or OAuth app makes on that user's behalf and any requests that the user makes with a personal access token. For more information, see [Rate limits for the REST API](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api#primary-rate-limit-for-authenticated-users).

### Primary rate limit for OAuth apps

Primary rate limits for OAuth access tokens generated by a OAuth app are dictated by the primary rate limits for authenticated users. This rate limit is combined with any requests that another GitHub App or OAuth app makes on that user's behalf and any requests that the user makes with a personal access token. See [Primary rate limit for authenticated users](#primary-rate-limit-for-authenticated-users).

OAuth apps can also use their client ID and client secret to fetch public data. For example:

```shell
curl -u YOUR_CLIENT_ID:YOUR_CLIENT_SECRET -I https://api.github.com/meta
```

For these requests, the rate limit is 5,000 requests per hour per OAuth app. If the app is owned by a GitHub Enterprise Cloud organization, the rate limit is 15,000 requests per hour.

Note

Never include your app's client secret in client-side code or in code that runs on a user device. The client secret can be used to generate OAuth access tokens for users who have authorized your app, so you should always keep the client secret secure.

### Primary rate limit forGITHUB_TOKENin GitHub Actions

You can use the built-in `GITHUB_TOKEN` to authenticate requests in GitHub Actions workflows. See [Use GITHUB_TOKEN for authentication in workflows](https://docs.github.com/en/actions/security-guides/automatic-token-authentication).

The rate limit for `GITHUB_TOKEN` is 1,000 requests per hour per repository. For requests to resources that belong to a GitHub Enterprise Cloud account, the limit is 15,000 requests per hour per repository.

## About secondary rate limits

In addition to primary rate limits, GitHub enforces secondary rate limits in order to prevent abuse and keep the API available for all users.

You may encounter a secondary rate limit if you:

- *Make too many concurrent requests.* No more than 100 concurrent requests are allowed. This limit is shared across the REST API and GraphQL API.
- *Make too many requests to a single endpoint per minute.* No more than 900 points per minute are allowed for REST API endpoints, and no more than 2,000 points per minute are allowed for the GraphQL API endpoint. For more information about points, see [Calculating points for the secondary rate limit](#calculating-points-for-the-secondary-rate-limit).
- *Make too many requests per minute.* No more than 90 seconds of CPU time per 60 seconds of real time is allowed. No more than 60 seconds of this CPU time may be for the GraphQL API. You can roughly estimate the CPU time by measuring the total response time for your API requests.
- *Make too many requests that consume excessive compute resources in a short period of time.*
- *Create too much content on GitHub in a short amount of time.* In general, no more than 80 content-generating requests per minute and no more than 500 content-generating requests per hour are allowed. Some endpoints have lower content creation limits. Content creation limits include actions taken on the GitHub web interface as well as via the REST API and GraphQL API.

These secondary rate limits are subject to change without notice. You may also encounter a secondary rate limit for undisclosed reasons.

### Calculating points for the secondary rate limit

Some secondary rate limits are determined by the point values of requests. For GraphQL requests, these point values are separate from the point value calculations for the primary rate limit.

| Request | Points |
| --- | --- |
| GraphQL requests without mutations | 1 |
| GraphQL requests with mutations | 5 |
| Most REST APIGET,HEAD, andOPTIONSrequests | 1 |
| Most REST APIPOST,PATCH,PUT, orDELETErequests | 5 |

Some REST API endpoints have a different point cost that is not shared publicly.

## Checking the status of your rate limit

You can use the headers that are sent with each response to determine the current status of your primary rate limit.

| Header name | Description |
| --- | --- |
| x-ratelimit-limit | The maximum number of requests that you can make per hour |
| x-ratelimit-remaining | The number of requests remaining in the current rate limit window |
| x-ratelimit-used | The number of requests you have made in the current rate limit window |
| x-ratelimit-reset | The time at which the current rate limit window resets, in UTC epoch seconds |
| x-ratelimit-resource | The rate limit resource that the request counted against. For more information about the different resources, seeREST API endpoints for rate limits. |

You can also call the `GET /rate_limit` endpoint to check your rate limit. Calling this endpoint does not count against your primary rate limit, but it can count against your secondary rate limit. See [REST API endpoints for rate limits](https://docs.github.com/en/rest/rate-limit/rate-limit). When possible, you should use the rate limit response headers instead of calling the API to check your rate limit.

There is not a way to check the status of your secondary rate limit.

## Exceeding the rate limit

If you exceed your primary rate limit, you will receive a `403` or `429` response, and the `x-ratelimit-remaining` header will be `0`. You should not retry your request until after the time specified by the `x-ratelimit-reset` header.

If you exceed a secondary rate limit, you will receive a `403` or `429` response and an error message that indicates that you exceeded a secondary rate limit. If the `retry-after` response header is present, you should not retry your request until after that many seconds has elapsed. If the `x-ratelimit-remaining` header is `0`, you should not retry your request until after the time, in UTC epoch seconds, specified by the `x-ratelimit-reset` header. Otherwise, wait for at least one minute before retrying. If your request continues to fail due to a secondary rate limit, wait for an exponentially increasing amount of time between retries, and throw an error after a specific number of retries.

Continuing to make requests while you are rate limited may result in the banning of your integration.

## Staying under the rate limit

You should follow best practices to help you stay under the rate limits. See [Best practices for using the REST API](https://docs.github.com/en/rest/guides/best-practices-for-using-the-rest-api).

## Getting a higher rate limit

If you want a higher primary rate limit, consider making authenticated requests instead of unauthenticated requests. Authenticated requests have a significantly higher rate limit than unauthenticated requests.

If you are using a personal access token for automation in your organization, consider whether a GitHub App will work instead. The rate limit for GitHub Apps using an installation access token scales with the number of repositories and number of organization users. See [About creating GitHub Apps](https://docs.github.com/en/apps/creating-github-apps/about-creating-github-apps/about-creating-github-apps).

If you are using GitHub Apps or OAuth apps, consider upgrading to GitHub Enterprise Cloud. GitHub Apps or OAuth apps have higher rate limits for organizations that use GitHub Enterprise Cloud.

---

# Timezones and the REST API

> Some REST API endpoints allow you to specify timezone information with your request.

Some requests that create new data, such as creating a new commit, allow you to provide timezone information when specifying or generating timestamps.

Note that these rules apply only to data passed to the API, not to data returned by the API. Timestamps returned by the API are in UTC time, ISO 8601 format.

## Determining the timezone for a request

To determine timezone information for applicable API calls, we apply these rules in order of priority:

1. [Explicitly providing an ISO 8601 timestamp with timezone information](#explicitly-providing-an-iso-8601-timestamp-with-timezone-information)
2. [Using theTime-Zoneheader](#using-the-time-zone-header)
3. [Using the last known timezone for the user](#using-the-last-known-timezone-for-the-user)
4. [Defaulting to UTC without other timezone information](#defaulting-to-utc-without-other-timezone-information)

### Explicitly providing an ISO 8601 timestamp with timezone information

For API calls that allow for a timestamp to be specified, we use that exact timestamp. These timestamps look something like `2014-02-27T15:05:06+01:00`.

An example of this is the API to manage commits. For more information, see [REST API endpoints for Git commits](https://docs.github.com/en/rest/git/commits#create-a-commit).

### Using theTime-Zoneheader

It is possible to supply a `Time-Zone` header, which defines a timezone according to the [list of names from the Olson database](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones).

```shell
curl -H "Time-Zone: Europe/Amsterdam" -X POST https://api.github.com/repos/github-linguist/linguist/contents/new_file.md
```

This means that we generate a timestamp for the moment your API call is made, in the timezone this header defines.

For example, the API to manage contents generates a git commit for each addition or change, and it uses the current time as the timestamp. For more information, see [REST API endpoints for repository contents](https://docs.github.com/en/rest/repos/contents). The `Time-Zone` header will determine the timezone used for generating that current timestamp.

### Using the last known timezone for the user

If no `Time-Zone` header is specified and you make an authenticated call to the API, we use the last known timezone for the authenticated user. The last known timezone is updated whenever you browse the GitHub website.

### Defaulting to UTC without other timezone information

If the steps above don't result in any information, we use UTC as the timezone.

---

# Troubleshooting the REST API

> Learn how to diagnose and resolve common problems for the REST API.

## Rate limit errors

GitHub enforces rate limits to ensure that the API stays available for all users. For more information, see [Rate limits for the REST API](https://docs.github.com/en/rest/overview/rate-limits-for-the-rest-api).

If you exceed your primary rate limit, you will receive a `403 Forbidden` or `429 Too Many Requests ` response, and the `x-ratelimit-remaining` header will be `0`. If you exceed a secondary rate limit, you will receive a `403 Forbidden` or `429 Too Many Requests ` response and an error message that indicates that you exceeded a secondary rate limit.

If you receive a rate limit error, you should stop making requests temporarily according to these guidelines:

- If the `retry-after` response header is present, you should not retry your request until after that many seconds has elapsed.
- If the `x-ratelimit-remaining` header is `0`, you should not make another request until after the time specified by the `x-ratelimit-reset` header. The `x-ratelimit-reset` header is in UTC epoch seconds.
- Otherwise, wait for at least one minute before retrying. If your request continues to fail due to a secondary rate limit, wait for an exponentially increasing amount of time between retries, and throw an error after a specific number of retries.

Continuing to make requests while you are rate limited may result in the banning of your integration.

For more information about how to avoid exceeding the rate limits, see [Best practices for using the REST API](https://docs.github.com/en/rest/guides/best-practices-for-using-the-rest-api).

## 404 Not Foundfor an existing resource

If you make a request to access a private resource and your request isn't properly authenticated, you will receive a `404 Not Found` response. GitHub uses a `404 Not Found` response instead of a `403 Forbidden` response to avoid confirming the existence of private repositories.

If you get a `404 Not Found` response when you know that the resource that you are requesting exists, you should check your authentication. For example:

- If you are using a personal access token (classic), you should ensure that:
  - The token has the scopes that are required to use the endpoint. For more information, see [Scopes for OAuth apps](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/scopes-for-oauth-apps#available-scopes) and [Managing your personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token).
  - The owner of the token has any permissions that are required to use the endpoint. For example, if an endpoint can only be used by organization owners, only users that are owners of the affected organization can use the endpoint.
  - The token has not been expired or revoked. For more information, see [Token expiration and revocation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/token-expiration-and-revocation).
- If you are using a fine-grained personal access token, you should ensure that:
  - The token has the permissions that are required to use the endpoint. For more information about the required permissions, see the documentation for the endpoint.
  - The resource owner that was specified for the token matches the owner of the resource that the endpoint will affect. For more information, see [Managing your personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token).
  - The token has access to any private repositories that the endpoint will affect. For more information, see [Managing your personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token).
  - The owner of the token has any permissions that are required to use the endpoint. For example, if an endpoint can only be used by organization owners, only users that are owners of the affected organization can use the endpoint.
  - The token has not been expired or revoked. For more information, see [Token expiration and revocation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/token-expiration-and-revocation).
- If you are using a GitHub App installation access token, you should ensure that:
  - The GitHub App has the permissions that are required to use the endpoint. For more information about the required permissions, see the documentation for the endpoint.
  - The endpoint is only affecting resources owned by the account where the GitHub App is installed.
  - The GitHub App has access to any repositories that the endpoint will affect.
  - The token has not been expired or revoked. For more information, see [Token expiration and revocation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/token-expiration-and-revocation).
- If you are using a GitHub App user access token, you should ensure that:
  - The GitHub App has the permissions that are required to use the endpoint. For more information about the required permissions, see the documentation for the endpoint.
  - The user that authorized the token has any permissions that are required to use the endpoint. For example, if an endpoint can only be used by organization owners, only users that are owners of the affected organization can use the endpoint.
  - The GitHub App has access to any repositories that the endpoint will affect.
  - The user has access to any repositories that the endpoint will affect.
  - The user has approved any updated permissions for your GitHub App. For more information, see [Approving updated permissions for a GitHub App](https://docs.github.com/en/apps/using-github-apps/approving-updated-permissions-for-a-github-app).
- If you are using an OAuth app user access token, you should ensure that:
  - The token has the scopes that are required to use the endpoint. For more information, see [Scopes for OAuth apps](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/scopes-for-oauth-apps#available-scopes).
  - The user that authorized the token has any permissions that are required to use the endpoint. For example, if an endpoint can only be used by organization owners, only users that are owners of the affected organization can use the endpoint.
  - The organization has not blocked OAuth app access, if you are using an endpoint that will affect resources owned by an organization. App owners cannot see whether their app is blocked, but they can instruct users of the app to check this. For more information, see [About OAuth app access restrictions](https://docs.github.com/en/organizations/managing-oauth-access-to-your-organizations-data/about-oauth-app-access-restrictions).
  - The token has not been expired or revoked. For more information, see [Token expiration and revocation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/token-expiration-and-revocation).
- If you are using `GITHUB_TOKEN` in a GitHub Actions workflow, you should ensure that:
  - The endpoint is only affecting resources owned by the repository where the workflow is running. If you need to access resources outside of that repository, such as resources owned by an organization or resources owned by another repository, you should use a personal access token or an access token for a GitHub App.

For more information about authentication, see [Authenticating to the REST API](https://docs.github.com/en/rest/overview/authenticating-to-the-rest-api).

You should also check for typos in your URL. For example, adding a trailing slash to the endpoint will result in a `404 Not Found`. You can refer to the reference documentation for the endpoint to confirm that you have the correct URL.

Additionally, any path parameters must be URL encoded. For example, any slashes in the parameter value must be replaced with `%2F`. If you don't properly encode any slashes in the parameter name, the endpoint URL will be misinterpreted.

## Missing results

Most endpoints that return a list of resources support pagination. For most of these endpoints, only the first 30 resources are returned by default. In order to see all of the resources, you need to paginate through the results. For more information, see [Using pagination in the REST API](https://docs.github.com/en/rest/guides/using-pagination-in-the-rest-api).

If you are using pagination correctly and still do not see all of the results that you expect, you should confirm that the authentication credentials that you used have access to all of the expected resources. For example, if you are using a GitHub App installation access token, if the installation was only granted access to a subset of repositories in an organization, any request for all repositories in that organization will return only the repositories that the app installation can access.

## Requires authentication when using basic authentication

Basic authentication with your username and password is not supported. Instead, you should use a personal access token or an access token for a GitHub App or OAuth app. For more information, see [Authenticating to the REST API](https://docs.github.com/en/rest/overview/authenticating-to-the-rest-api).

## Timeouts

If GitHub takes more than 10 seconds to process an API request, GitHub will terminate the request and you will receive a timeout response and a "Server Error" message.

GitHub reserves the right to change the timeout window to protect the speed and reliability of the API.

You can check the status of the REST API at [githubstatus.com](https://www.githubstatus.com/) to determine whether the timeout is due to a problem with the API. You can also try to simplify your request or try your request later. For example, if you are requesting 100 items on a page, you can try requesting fewer items.

## Resource not accessible

If you are using a GitHub App or fine-grained personal access token and you receive a "Resource not accessible by integration" or "Resource not accessible by personal access token" error, then your token has insufficient permissions. For more information about the required permissions, see the documentation for the endpoint.

You can use the `X-Accepted-GitHub-Permissions` header to identify the permissions that are required to access the REST API endpoint.

The value of the `X-Accepted-GitHub-Permissions` header is a comma separated list of the permissions that are required to use the endpoint. Occasionally, you can choose from multiple permission sets. In these cases, multiple comma-separated lists will be separated by a semicolon.

For example:

- `X-Accepted-GitHub-Permissions: contents=read` means that your GitHub App or fine-grained personal access token needs read access to the contents permission.
- `X-Accepted-GitHub-Permissions: pull_requests=write,contents=read` means that your GitHub App or fine-grained personal access token needs write access to the pull request permission and read access to the contents permission.
- `X-Accepted-GitHub-Permissions: pull_requests=read,contents=read; issues=read,contents=read` means that your GitHub App or fine-grained personal access token needs either read access to the pull request permission and read access to the contents permission, or read access to the issues permission and read access to the contents permission.

## Problems parsing JSON

If you send invalid JSON in the request body, you may receive a `400 Bad Request` response and a "Problems parsing JSON" error message. You can use a linter or JSON validator to help you identify errors in your JSON.

## Body should be a JSON object

If the endpoint expects a JSON object and you do not format your request body as a JSON object, you may receive a `400 Bad Request` response and a "Body should be a JSON object" error message.

## Invalid request

If you omit required parameters or you use the wrong type for a parameter, you may receive a `422 Unprocessable Entity` response and an "Invalid request" error message. For example, you will get this error if you specify a parameter value as an array but the endpoint is expecting a string. You can refer to the reference documentation for the endpoint to verify that you are using the correct parameter types and that you are including all of the required parameters.

## Validation Failed

If your request could not be processed, you may receive a `422 Unprocessable Entity` response and a "Validation Failed" error message. The response body will include an `errors` property, which includes a `code` property to help you diagnose the problem.

| Code | Description |
| --- | --- |
| missing | A resource does not exist. |
| missing_field | A parameter that was required was not specified. Review the documentation for the endpoint to see what parameters are required. |
| invalid | The formatting of a parameter is invalid. Review the endpoint documentation for more specific information. |
| already_exists | Another resource has the same value as one of your parameters. This can happen in resources that must have some unique key (such as label names). |
| unprocessable | The parameters that were provided were invalid. |
| custom | Refer to themessageproperty to diagnose the error. |

## Not a supported version

You should use the `X-GitHub-Api-Version` header to specify an API version. For example:

```shell
curl --header "X-GitHub-Api-Version:2022-11-28" https://api.github.com/zen
```

If you specify a version that does not exist, you will receive a `400 Bad Request` error and a message about the version not being supported.

For more information, see [API Versions](https://docs.github.com/en/rest/overview/api-versions).

## User agent required

Requests without a valid `User-Agent` header will be rejected. You should use your username or the name of your application for the `User-Agent` value.

curl sends a valid `User-Agent` header by default.

## Other errors

If you observe an error that is not addressed here, you should refer to the error message that the API gives you. Most error messages will provide a clue about what is wrong and a link to relevant documentation.

If you observe unexpected failures, you can use [githubstatus.com](https://www.githubstatus.com/) or the [GitHub status API](https://www.githubstatus.com/api) to check for incidents affecting the API.

## Further reading

- [Best practices for using the REST API](https://docs.github.com/en/rest/guides/best-practices-for-using-the-rest-api)
- [Troubleshooting webhooks](https://docs.github.com/en/webhooks/testing-and-troubleshooting-webhooks/troubleshooting-webhooks)
- [Best practices for creating a GitHub App](https://docs.github.com/en/apps/creating-github-apps/about-creating-github-apps/best-practices-for-creating-a-github-app)

---

# Using CORS and JSONP to make cross

> You can make API requests across domains using cross-origin resource sharing (CORS) and JSONP callbacks.

## About cross-origin requests

A cross-origin request is a request made to a different domain than the one originating the request. For security reasons, most web browsers block cross-origin requests. However, you can use cross-origin resource sharing (CORS) and JSONP callbacks to make cross-origin requests.

## Cross-origin resource sharing (CORS)

The REST API supports cross-origin resource sharing (CORS) for AJAX requests from any origin. For more information, see the [CORS W3C Recommendation](http://www.w3.org/TR/cors/) and the [HTML 5 Security Guide](https://code.google.com/archive/p/html5security/wikis/CrossOriginRequestSecurity.wiki)

Here's a sample request sent from a browser hitting
`http://example.com`:

```shell
$ curl -I https://api.github.com -H "Origin: http://example.com"
HTTP/2 302
Access-Control-Allow-Origin: *
Access-Control-Expose-Headers: ETag, Link, x-ratelimit-limit, x-ratelimit-remaining, x-ratelimit-reset, X-OAuth-Scopes, X-Accepted-OAuth-Scopes, X-Poll-Interval
```

This is what the CORS preflight request looks like:

```shell
$ curl -I https://api.github.com -H "Origin: http://example.com" -X OPTIONS
HTTP/2 204
Access-Control-Allow-Origin: *
Access-Control-Allow-Headers: Authorization, Content-Type, If-Match, If-Modified-Since, If-None-Match, If-Unmodified-Since, X-Requested-With
Access-Control-Allow-Methods: GET, POST, PATCH, PUT, DELETE
Access-Control-Expose-Headers: ETag, Link, x-ratelimit-limit, x-ratelimit-remaining, x-ratelimit-reset, X-OAuth-Scopes, X-Accepted-OAuth-Scopes, X-Poll-Interval
Access-Control-Max-Age: 86400
```

## JSON-P callbacks

You can send a `?callback` parameter to any GET call to have the results
wrapped in a JSON function. This is typically used when browsers want to embed GitHub content in web pages and avoid cross-domain problems. The response includes the same data output as the regular API, plus the relevant HTTP Header information.

```shell
$ curl https://api.github.com?callback=foo

> /**/foo({
>   "meta": {
>     "status": 200,
>     "x-ratelimit-limit": "5000",
>     "x-ratelimit-remaining": "4966",
>     "x-ratelimit-reset": "1372700873",
>     "Link": [ // pagination headers and other links
>       ["https://api.github.com?page=2", {"rel": "next"}]
>     ]
>   },
>   "data": {
>     // the data
>   }
> })
```

You can write a JavaScript handler to process the callback. Here's a minimal example you can try:

```html
<html>
<head>
<script type="text/javascript">
function foo(response) {
  var meta = response.meta;
  var data = response.data;
  console.log(meta);
  console.log(data);
}

var script = document.createElement('script');
script.src = 'https://api.github.com?callback=foo';

document.getElementsByTagName('head')[0].appendChild(script);
</script>
</head>

<body>
  <p>Open up your browser's console.</p>
</body>
</html>
```

All of the headers have the same string value as the HTTP Headers, except `Link`. `Link` headers are pre-parsed for you and come through as an array of `[url, options]` tuples.

For example, a link that looks like this:

```shell
Link: <url1>; rel="next", <url2>; rel="foo"; bar="baz"
```

will look like this in the Callback output:

```json
{
  "Link": [
    [
      "url1",
      {
        "rel": "next"
      }
    ],
    [
      "url2",
      {
        "rel": "foo",
        "bar": "baz"
      }
    ]
  ]
}
```
