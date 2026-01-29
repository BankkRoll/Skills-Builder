# API Versions and more

# API Versions

> Learn how to specify which REST API version to use whenever you make a request to the REST API.

## About API versioning

The GitHub REST API is versioned. The API version name is based on the date when the API version was released. For example, the API version `2022-11-28` was released on Mon, 28 Nov 2022.

Breaking changes are changes that can potentially break an integration. We will provide advance notice before releasing breaking changes. Breaking changes include:

- Removing an entire operation
- Removing or renaming a parameter
- Removing or renaming a response field
- Adding a new required parameter
- Making a previously optional parameter required
- Changing the type of a parameter or response field
- Removing enum values
- Adding a new validation rule to an existing parameter
- Changing authentication or authorization requirements

Any additive (non-breaking) changes will be available in all supported API versions. Additive changes are changes that should not break an integration. Additive changes include:

- Adding an operation
- Adding an optional parameter
- Adding an optional request header
- Adding a response field
- Adding a response header
- Adding enum values

When a new REST API version is released, the previous API version will be supported for at least 24 more months following the release of the new API version.

## Specifying an API version

You should use the `X-GitHub-Api-Version` header to specify an API version. For example:

```shell
curl --header "X-GitHub-Api-Version:2022-11-28" https://api.github.com/zen
```

Requests without the `X-GitHub-Api-Version` header will default to use the `2022-11-28` version.

If you specify an API version that is no longer supported, you will receive a `400` error.

## Upgrading to a new API version

Before upgrading to a new REST API version, you should read the changelog of breaking changes for the new API version to understand what breaking changes are included and to learn more about how to upgrade to that specific API version. For more information, see [Breaking changes](https://docs.github.com/en/rest/overview/breaking-changes).

When you update your integration to specify the new API version in the `X-GitHub-Api-Version` header, you'll also need to make any changes required for your integration to work with the new API version.

Once your integration is updated, test your integration to verify that it works with the new API version.

## Supported API versions

The following REST API versions are currently supported:

2022-11-28

You can also make an API request to get all of the supported API versions. For more information, see [REST API endpoints for meta data](https://docs.github.com/en/rest/meta/meta#get-all-api-versions).

---

# Authenticating to the REST API

> You can authenticate to the REST API to access more endpoints and have a higher rate limit.

## About authentication

Many REST API endpoints require authentication or return additional information if you are authenticated. Additionally, you can make more requests per hour when you are authenticated.

To authenticate your request, you will need to provide an authentication token with the required scopes or permissions. There a few different ways to get a token: You can create a personal access token, generate a token with a GitHub App, or use the built-in `GITHUB_TOKEN` in a GitHub Actions workflow.

After creating a token, you can authenticate your request by sending the token in the `Authorization` header of your request. For example, in the following request, replace `YOUR-TOKEN` with a reference to your token:

```shell
curl --request GET \
--url "https://api.github.com/octocat" \
--header "Authorization: Bearer YOUR-TOKEN" \
--header "X-GitHub-Api-Version: 2022-11-28"
```

Note

In most cases, you can use `Authorization: Bearer` or `Authorization: token` to pass a token. However, if you are passing a JSON web token (JWT), you must use `Authorization: Bearer`.

### Failed login limit

If you try to use a REST API endpoint without a token or with a token that has insufficient permissions, you will receive a `404 Not Found` or `403 Forbidden` response. Authenticating with invalid credentials will initially return a `401 Unauthorized` response.

After detecting several requests with invalid credentials within a short period, the API will temporarily reject all authentication attempts for that user (including ones with valid credentials) with a `403 Forbidden` response. For more information, see [Rate limits for the REST API](https://docs.github.com/en/rest/overview/rate-limits-for-the-rest-api).

## Authenticating with a personal access token

If you want to use the GitHub REST API for personal use, you can create a personal access token. If possible, GitHub recommends that you use a fine-grained personal access token instead of a personal access token (classic). For more information about creating a personal access token, see [Managing your personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token).

If you are using a fine-grained personal access token, your fine-grained personal access token requires specific permissions in order to access each REST API endpoint. The REST API reference document for each endpoint states whether the endpoint works with fine-grained personal access tokens and states what permissions are required in order for the token to use the endpoint. Some endpoints may require multiple permissions, and some endpoints may require one of multiple permissions. For an overview of which REST API endpoints a fine-grained personal access token can access with each permission, see [Permissions required for fine-grained personal access tokens](https://docs.github.com/en/rest/overview/permissions-required-for-fine-grained-personal-access-tokens).

If you are using a personal access token (classic), it requires specific scopes in order to access each REST API endpoint. For general guidance about what scopes to choose, see [Scopes for OAuth apps](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/scopes-for-oauth-apps#available-scopes).

Personal access tokens act as your identity (limited by the scopes or permissions you selected) when you make requests to the REST API. As such, it is important to keep your personal access tokens secure. For more information about keeping your personal access tokens secure, see [Keeping your API credentials secure](https://docs.github.com/en/rest/authentication/keeping-your-api-credentials-secure?apiVersion=2022-11-28).

### Personal access tokens and SAML SSO

If you use a personal access token (classic) to access an organization that enforces SAML single sign-on (SSO) for authentication, you will need to authorize your token after creation. Fine-grained personal access tokens are authorized during token creation, before access to the organization is granted. For more information, see [Authorizing a personal access token for use with single sign-on](https://docs.github.com/en/authentication/authenticating-with-saml-single-sign-on/authorizing-a-personal-access-token-for-use-with-saml-single-sign-on).

If you do not authorize your personal access token (classic) for SAML SSO before you try to use it to access a single organization that enforces SAML SSO, you may receive a `404 Not Found` or a `403 Forbidden` error. If you receive a `403 Forbidden` error, the `X-GitHub-SSO` header will include a URL that you can follow to authorize your token. The URL expires after one hour.

If you do not authorize your personal access token (classic) for SAML SSO before you try to use it to access multiple organizations, the API will not return results from the organizations that require SAML SSO and the `X-GitHub-SSO` header will indicate the ID of the organizations that require SAML SSO authorization of your personal access token (classic). For example: `X-GitHub-SSO: partial-results; organizations=21955855,20582480`.

## Authenticating with a token generated by an app

If you want to use the API for an organization or on behalf of another user, GitHub recommends that you use a GitHub App. For more information, see [About authentication with a GitHub App](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/about-authentication-with-a-github-app).

The REST API reference documentation for each endpoint states whether the endpoint works with GitHub Apps and states what permissions are required in order for the app to use the endpoint. Some endpoints may require multiple permissions, and some endpoints may require one of multiple permissions. For an overview of which REST API endpoints a GitHub App can access with each permission, see [Permissions required for GitHub Apps](https://docs.github.com/en/rest/overview/permissions-required-for-github-apps).

You can also create an OAuth token with an OAuth app to access the REST API. However, GitHub recommends that you use a GitHub App instead. GitHub Apps allow more control over the access and permission that the app has.

Access tokens created by apps are automatically authorized for SAML SSO.

### Using basic authentication

Some REST API endpoints for GitHub Apps and OAuth apps require you to use basic authentication to access the endpoint. You will use the app's client ID as the username and the app's client secret as the password.

For example:

```shell
curl --request POST \
--url "https://api.github.com/applications/YOUR_CLIENT_ID/token" \
--user "YOUR_CLIENT_ID:YOUR_CLIENT_SECRET" \
--header "Accept: application/vnd.github+json" \
--header "X-GitHub-Api-Version: 2022-11-28" \
--data '{
  "access_token": "ACCESS_TOKEN_TO_CHECK"
}'
```

The client ID and client secret are associated with the app, not with the owner of the app or a user who authorized the app. They are used to perform operations on behalf of the app, such as creating access tokens.

If you are the owner of a GitHub App or OAuth app, or if you are an app manager for a GitHub App, you can find the client ID and generate a client secret on the settings page for your app. To navigate to your app's settings page:

1. In the upper-right corner of any page on GitHub, click your profile picture.
2. Navigate to your account settings.
  - For an app owned by a personal account, click **Settings**.
  - For an app owned by an organization:
    1. Click **Your organizations**.
    2. To the right of the organization, click **Settings**.
3. In the left sidebar, click **Developer settings**.
4. In the left sidebar, click **GitHub Apps** or **OAuth apps**.
5. For GitHub Apps, to the right of the GitHub App you want to access, click **Edit**. For OAuth apps, click the app that you want to access.
6. Next to **Client ID**, you will see the client ID for your app.
7. Next to **Client secrets**, click **Generate a new client secret** to generate a client secret for your app.

## Authenticating in a GitHub Actions workflow

If you want to use the API in a GitHub Actions workflow, GitHub recommends that you authenticate with the built-in `GITHUB_TOKEN` instead of creating a token. You can grant permissions to the `GITHUB_TOKEN` with the `permissions` key. For more information, see [Use GITHUB_TOKEN for authentication in workflows](https://docs.github.com/en/actions/security-guides/automatic-token-authentication#permissions-for-the-github_token).

If this is not possible, you can store your token as a secret and use the name of your secret in your GitHub Actions workflow. For more information about secrets, see [Using secrets in GitHub Actions](https://docs.github.com/en/actions/security-guides/encrypted-secrets).

### Authenticating in a GitHub Actions workflow using GitHub CLI

To make an authenticated request to the API in a GitHub Actions workflow using GitHub CLI, you can store the value of `GITHUB_TOKEN` as an environment variable, and use the `run` keyword to execute the GitHub CLI `api` subcommand. For more information about the `run` keyword, see [Workflow syntax for GitHub Actions](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#jobsjob_idstepsrun).

In the following example workflow, replace `PATH` with the path of the endpoint. For more information about the path, see [Getting started with the REST API](https://docs.github.com/en/rest/guides/getting-started-with-the-rest-api?tool=cli#path).

```yaml
jobs:
  use_api:
    runs-on: ubuntu-latest
    permissions: {}
    steps:
      - env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          gh api /PATH
```

### Authenticating in a GitHub Actions workflow usingcurl

To make an authenticated request to the API in a GitHub Actions workflow using `curl`, you can store the value of `GITHUB_TOKEN` as an environment variable, and use the `run` keyword to execute a `curl` request to the API. For more information about the `run` keyword, see [Workflow syntax for GitHub Actions](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#jobsjob_idstepsrun).

In the following example workflow, replace `PATH` with the path of the endpoint. For more information about the path, see [Getting started with the REST API](https://docs.github.com/en/rest/guides/getting-started-with-the-rest-api?tool=cli#path).

```yaml
jobs:
  use_api:
    runs-on: ubuntu-latest
    permissions: {}
    steps:
      - env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          curl --request GET \
          --url "https://api.github.com/PATH" \
          --header "Authorization: Bearer $GH_TOKEN"
```

### Authenticating in a GitHub Actions workflow using JavaScript

For an example of how to authenticate in a GitHub Actions workflow using JavaScript, see [Scripting with the REST API and JavaScript](https://docs.github.com/en/rest/guides/scripting-with-the-rest-api-and-javascript#authenticating-in-github-actions).

## Authenticating with username and password

Authentication with username and password is not supported. If you try to authenticate with user name and password, you will receive a 4xx error.

## Further reading

- [Keeping your API credentials secure](https://docs.github.com/en/rest/overview/keeping-your-api-credentials-secure)
- [Getting started with the REST API](https://docs.github.com/en/rest/guides/getting-started-with-the-rest-api#authenticating)

---

# Breaking changes

> Learn about breaking changes that were introduced in each REST API version.

## About breaking changes in the REST API

The GitHub REST API is versioned. The API version name is based on the date when the API version was released. For example, the API version `2022-11-28` was released on Mon, 28 Nov 2022.

Breaking changes are changes that can potentially break an integration. We will provide advance notice before releasing breaking changes. Breaking changes include:

- Removing an entire operation
- Removing or renaming a parameter
- Removing or renaming a response field
- Adding a new required parameter
- Making a previously optional parameter required
- Changing the type of a parameter or response field
- Removing enum values
- Adding a new validation rule to an existing parameter
- Changing authentication or authorization requirements

Any additive (non-breaking) changes will be available in all supported API versions. Additive changes are changes that should not break an integration. Additive changes include:

- Adding an operation
- Adding an optional parameter
- Adding an optional request header
- Adding a response field
- Adding a response header
- Adding enum values

When a new REST API version is released, the previous API version will be supported for at least 24 more months following the release of the new API version.

For more information about API versions, see [API Versions](https://docs.github.com/en/rest/overview/api-versions).

## Upgrading to a new API version

Before upgrading to a new REST API version, you should read the section on this page that corresponds to the new API version to understand what breaking changes are included and to learn more about how to upgrade to that API version.

When you update your integration to specify the new API version in the `X-GitHub-Api-Version` header, you'll also need to make any changes required for your integration to work with the new API version.

Once your integration is updated, test your integration to verify that it works with the new API version.

## Breaking changes for 2022-11-28

Version `2022-11-28` is the first version of the GitHub REST API after date-based versioning was introduced. This version does not include any breaking changes.

---

# Comparing GitHub's REST API and GraphQL API

> Learn about GitHub's APIs to extend and customize your GitHub experience.

## About GitHub's APIs

GitHub provides two APIs: a REST API and a GraphQL API. You can interact with both APIs using GitHub CLI, curl, the official Octokit libraries, and third party libraries. Occasionally, a feature may be supported on one API but not the other.

You should use the API that best aligns with your needs and that you are most comfortable using. You don't need to exclusively use one API over the other. Node IDs let you move between the REST API and GraphQL API. For more information, see [Using global node IDs](https://docs.github.com/en/graphql/guides/using-global-node-ids).

This article discusses the benefits of each API. For more information about the GraphQL API, see [About the GraphQL API](https://docs.github.com/en/graphql/overview/about-the-graphql-api). For more information about the REST API, see [About the REST API](https://docs.github.com/en/rest/about-the-rest-api/about-the-rest-api).

## Choosing the GraphQL API

The GraphQL API returns exactly the data that you request. GraphQL also returns the data in a pre-known structure based on your request. In contrast, the REST API returns more data than you requested and returns it in a pre-determined structure. You can also accomplish the equivalent of multiple REST API request in a single GraphQL request. The ability to make fewer requests and fetch less data makes GraphQL appealing to developers of mobile applications.

For example, to get the GitHub login of ten of your followers, and the login of ten followers of each of your followers, you can send a single request like:

```graphql
{
  viewer {
    followers(first: 10) {
      nodes {
        login
        followers(first: 10) {
          nodes {
            login
          }
        }
      }
    }
  }
}
```

The response will be a JSON object that follows the structure of your request.

In contrast, to get this same information from the REST API, you would need to first make a request to `GET /user/followers`. The API would return the login of each follower, along with other data about the followers that you don't need. Then, for each follower, you would need to make a request to `GET /users/{username}/followers`. In total, you would need to make 11 requests to get the same information that you could get from a single GraphQL request, and you would receive excess data.

## Choosing the REST API

Because REST APIs have been around for longer than GraphQL APIs, some developers are more comfortable with the REST API. Since REST APIs use standard HTTP verbs and concepts, many developers are already familiar with the basic concepts to use the REST API.

For example, to create an issue in the `octocat/Spoon-Knife` repository, you would need to send a request to `POST /repos/octocat/Spoon-Knife/issues` with a JSON request body:

```json
{
  "title": "Bug with feature X",
  "body": "If you do A, then B happens"
}
```

In contrast, to make an issue using the GraphQL API, you would need to get the node ID of the `octocat/Spoon-Knife` repository and then send a request like:

```graphql
mutation {
  createIssue(
    input: {
      repositoryId: "MDEwOlJlcG9zaXRvcnkxMzAwMTky"
      title: "Bug with feature X"
      body: "If you do A, then B happens"}
  ) {
    issue {
      number
      url
    }
  }
}
```

---

# Keeping your API credentials secure

> Follow these best practices to keep your API credentials and tokens secure.

## Choose an appropriate authentication method

You should choose an authentication method that is appropriate for the task you want to accomplish.

- To use the API for personal use, you can create a personal access token.
- To use the API on behalf of an organization or another user, you should create a GitHub App.
- To use the API in a GitHub Actions workflow, you should authenticate with the built-in `GITHUB_TOKEN`.

For more information, see [About authentication to GitHub](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-authentication-to-github#authenticating-with-the-api).

## Limit the permissions of your credentials

When creating a personal access token, only select the minimum permissions or scopes needed, and set an expiration date for the minimum amount of time you'll need to use the token. GitHub recommends that you use fine-grained personal access tokens instead of personal access tokens (classic). For more information, see [Managing your personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#types-of-personal-access-tokens).

A token has the same capabilities to access resources and perform actions on those resources that the owner of the token has, and is further limited by any scopes or permissions granted to the token. A token cannot grant additional access capabilities to a user.

When creating a GitHub App, select the minimum permissions that your GitHub App will need. For more information, see [Best practices for creating a GitHub App](https://docs.github.com/en/apps/creating-github-apps/setting-up-a-github-app/best-practices-for-creating-a-github-app).

When authenticating with `GITHUB_TOKEN` in a GitHub Actions workflow, only give the minimum amount of permissions needed. For more information, see [Use GITHUB_TOKEN for authentication in workflows](https://docs.github.com/en/actions/security-guides/automatic-token-authentication#permissions-for-the-github_token).

## Store your authentication credentials securely

Treat authentication credentials the same way you would treat your passwords or other sensitive credentials.

- Don't share authentication credentials using an unencrypted messaging or email system.
- Don't pass your personal access token as plain text in the command line. For more information, see [Managing your personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#keeping-your-personal-access-tokens-secure).
- Don't push unencrypted authentication credentials like tokens or keys to any repository, even if the repository is private. Instead consider using a GitHub Actions secret or Codespaces secret. For more information, see [Using secrets in GitHub Actions](https://docs.github.com/en/actions/security-guides/encrypted-secrets) and [Managing your account-specific secrets for GitHub Codespaces](https://docs.github.com/en/codespaces/managing-your-codespaces/managing-encrypted-secrets-for-your-codespaces).
- You can use secret scanning to discover tokens, private keys, and other secrets that were pushed to a repository, or to block future pushes that contain secrets. For more information, see [About secret scanning](https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning).

## Limit who can access your authentication credentials

Don't share your personal access token with others. Instead of sharing a personal access token, consider creating a GitHub App. For more information, see [About creating GitHub Apps](https://docs.github.com/en/apps/creating-github-apps/setting-up-a-github-app/about-creating-github-apps).

If you need to share credentials with a team, store the credentials in a secure shared system. For example, you could store and share passwords securely using [1Password](https://1password.com/), or you could store keys in [Azure KeyVault](https://azure.microsoft.com/en-gb/products/key-vault) and manage access with your IAM (Identity and access management).

If you're creating a GitHub Actions workflow that needs to access the API, you can store your credentials in an encrypted secret, and access the encrypted secret from the workflow. For more information, see [Using secrets in GitHub Actions](https://docs.github.com/en/actions/security-guides/encrypted-secrets) and [Making authenticated API requests with a GitHub App in a GitHub Actions workflow](https://docs.github.com/en/apps/creating-github-apps/guides/making-authenticated-api-requests-with-a-github-app-in-a-github-actions-workflow).

## Use authentication credentials securely in your code

Never hardcode authentication credentials like tokens, keys, or app-related secrets into your code. Instead, consider using a secret manager such as [Azure Key Vault](https://azure.microsoft.com/products/key-vault) or [HashiCorp Vault](https://www.hashicorp.com/products/vault). For more information about securing GitHub App credentials, see [Best practices for creating a GitHub App](https://docs.github.com/en/apps/creating-github-apps/setting-up-a-github-app/best-practices-for-creating-a-github-app).

If you find another user's personal access token exposed on GitHub or elsewhere, you can submit a revocation request through the REST API. See [Revocation](https://docs.github.com/en/rest/credentials/revoke#revoke-a-list-of-credentials).

When using a personal access token in a script, consider storing your token as a GitHub Actions secret and running your script through GitHub Actions. You can also store your token as a Codespaces secret and run your script in Codespaces. For more information, see [Using secrets in GitHub Actions](https://docs.github.com/en/actions/security-guides/encrypted-secrets) and [Managing your account-specific secrets for GitHub Codespaces](https://docs.github.com/en/codespaces/managing-your-codespaces/managing-encrypted-secrets-for-your-codespaces).

If none of these options are possible, you can store authentication credentials in a `.env` file. Make sure to encrypt your `.env` file, and never push it to any repository.

## Prepare a remediation plan

You should create a plan to handle any security breaches in a timely manner. In the event that your token or other authentication credential is leaked, you will need to:

- Generate a new credential.
- Replace the old credential with the new one everywhere that you are storing or accessing the credential.
- Delete the old compromised credential.

For information about rotating compromised credentials for a GitHub App, see [Best practices for creating a GitHub App](https://docs.github.com/en/apps/creating-github-apps/setting-up-a-github-app/best-practices-for-creating-a-github-app).

For information about creating and deleting personal access tokens, see [Managing your personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens).

---

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
