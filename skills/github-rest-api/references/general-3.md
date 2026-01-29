# Quickstart for GitHub REST API and more

# Quickstart for GitHub REST API

> Learn how to get started with the GitHub REST API.

## Introduction

This article describes how to quickly get started with the GitHub REST API using GitHub CLI, `curl`, or JavaScript. For a more detailed guide, see [Getting started with the REST API](https://docs.github.com/en/rest/guides/getting-started-with-the-rest-api).

## Using GitHub CLI in the command line

GitHub CLI is the easiest way to use the GitHub REST API from the command line.

1. Install GitHub CLI on macOS, Windows, or Linux. For more information, see [Installation](https://github.com/cli/cli?ref_product=cli&ref_type=engagement&ref_style=text#installation) in the GitHub CLI repository.
2. To authenticate to GitHub, run the following command from your terminal.
  ```shell
  gh auth login
  ```
3. Select where you want to authenticate to:
  - If you access GitHub at GitHub.com, select **GitHub.com**.
  - If you access GitHub at a different domain, select **Other**, then enter your hostname (for example: `octocorp.ghe.com`).
4. Follow the rest of the on-screen prompts.
  GitHub CLI automatically stores your Git credentials for you when you choose HTTPS as your preferred protocol for Git operations and answer "yes" to the prompt asking if you would like to authenticate to Git with your GitHub credentials. This can be useful as it allows you to use Git commands like `git push` and `git pull` without needing to set up a separate credential manager or use SSH.
5. Make a request using the GitHub CLI `api` subcommand, followed by the path. Use the `--method` or `-X` flag to specify the method. For more information, see the [GitHub CLIapidocumentation](https://cli.github.com/manual/gh_api).
  This example makes a request to the "Get Octocat" endpoint, which uses the method `GET` and the path `/octocat`. For the full reference documentation for this endpoint, see [REST API endpoints for meta data](https://docs.github.com/en/rest/meta/meta#get-octocat).
  ```shell
  gh api /octocat --method GET
  ```

## Using GitHub CLI in GitHub Actions

You can also use GitHub CLI in your GitHub Actions workflows. For more information, see [Using GitHub CLI in workflows](https://docs.github.com/en/actions/using-workflows/using-github-cli-in-workflows).

### Authenticating with an access token

Instead of using the `gh auth login` command, pass an access token as an environment variable called `GH_TOKEN`. GitHub recommends that you use the built-in `GITHUB_TOKEN` instead of creating a token. If this is not possible, store your token as a secret and replace `GITHUB_TOKEN` in the example below with the name of your secret. For more information about `GITHUB_TOKEN`, see [Use GITHUB_TOKEN for authentication in workflows](https://docs.github.com/en/actions/security-guides/automatic-token-authentication). For more information about secrets, see [Using secrets in GitHub Actions](https://docs.github.com/en/actions/security-guides/encrypted-secrets).

The following example workflow uses the [List repository issues](https://docs.github.com/en/rest/issues/issues#list-repository-issues) endpoint, and requests a list of issues in the `octocat/Spoon-Knife` repository.

```yaml
on:
  workflow_dispatch:
jobs:
  use_api:
    runs-on: ubuntu-latest
    permissions:
      issues: read
    steps:
      - env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          gh api https://api.github.com/repos/octocat/Spoon-Knife/issues
```

### Authenticating with a GitHub App

If you are authenticating with a GitHub App, you can create an installation access token within your workflow:

1. Store your GitHub App's ID as a configuration variable. In the following example, replace `APP_ID` with the name of the configuration variable. You can find your app ID on the settings page for your app or through the API. For more information, see [REST API endpoints for GitHub Apps](https://docs.github.com/en/rest/apps/apps#get-an-app). For more information about configuration variables, see [Store information in variables](https://docs.github.com/en/actions/learn-github-actions/variables#defining-configuration-variables-for-multiple-workflows).
2. Generate a private key for your app. Store the contents of the resulting file as a secret. (Store the entire contents of the file, including `-----BEGIN RSA PRIVATE KEY-----` and `-----END RSA PRIVATE KEY-----`.) In the following example, replace `APP_PEM` with the name of the secret. For more information, see [Managing private keys for GitHub Apps](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/managing-private-keys-for-github-apps). For more information about secrets, see [Using secrets in GitHub Actions](https://docs.github.com/en/actions/security-guides/encrypted-secrets).
3. Add a step to generate a token, and use that token instead of `GITHUB_TOKEN`. Note that this token will expire after 60 minutes. For example:
  ```yaml
  on:
    workflow_dispatch:
  jobs:
    track_pr:
      runs-on: ubuntu-latest
      steps:
        - name: Generate token
          id: generate-token
          uses: actions/create-github-app-token@v2
          with:
            app-id: ${{ vars.APP_ID }}
            private-key: ${{ secrets.APP_PEM }}
        - name: Use API
          env:
            GH_TOKEN: ${{ steps.generate-token.outputs.token }}
          run: |
            gh api https://api.github.com/repos/octocat/Spoon-Knife/issues
  ```

## Using Octokit.js

You can use Octokit.js to interact with the GitHub REST API in your JavaScript scripts. For more information, see [Scripting with the REST API and JavaScript](https://docs.github.com/en/rest/guides/scripting-with-the-rest-api-and-javascript).

1. Create an access token. For example, create a personal access token or a GitHub App user access token. You will use this token to authenticate your request, so you should give it any scopes or permissions that are required to access that endpoint. For more information, see [Authenticating to the REST API](https://docs.github.com/en/rest/overview/authenticating-to-the-rest-api) or [Identifying and authorizing users for GitHub Apps](https://docs.github.com/en/developers/apps/building-github-apps/identifying-and-authorizing-users-for-github-apps).
  Warning
  Treat your access token like a password.
  To keep your token secure, you can store your token as a secret and run your script through GitHub Actions. For more information, see the [Using Octokit.js in GitHub Actions](#using-octokitjs-in-github-actions) section.
  You can also store your token as a Codespaces secret and run your script in Codespaces. For more information, see [Managing encrypted secrets for your codespaces](https://docs.github.com/en/codespaces/managing-your-codespaces/managing-encrypted-secrets-for-your-codespaces).
  > If these options are not possible, consider using another CLI service to store your token securely.
2. Install `octokit`. For example, `npm install octokit`. For other ways to install or load `octokit`, see [the Octokit.js README](https://github.com/octokit/octokit.js/#readme).
3. Import `octokit` in your script. For example, `import { Octokit } from "octokit";`. For other ways to import `octokit`, see [the Octokit.js README](https://github.com/octokit/octokit.js/#readme).
4. Create an instance of `Octokit` with your token. Replace `YOUR-TOKEN` with your token.
  ```javascript
  const octokit = new Octokit({
    auth: 'YOUR-TOKEN'
  });
  ```
5. Use `octokit.request` to execute your request. Send the HTTP method and path as the first argument. Specify any path, query, and body parameters in an object as the second argument. For more information about parameters, see [Getting started with the REST API](https://docs.github.com/en/rest/guides/getting-started-with-the-rest-api#using-parameters).
  For example, in the following request the HTTP method is `GET`, the path is `/repos/{owner}/{repo}/issues`, and the parameters are `owner: "octocat"` and `repo: "Spoon-Knife"`.
  ```javascript
  await octokit.request("GET /repos/{owner}/{repo}/issues", {
    owner: "octocat",
    repo: "Spoon-Knife",
  });
  ```

## Using Octokit.js in GitHub Actions

You can also execute your JavaScript scripts in your GitHub Actions workflows. For more information, see [Workflow syntax for GitHub Actions](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#jobsjob_idstepsrun).

### Authenticating with an access token

GitHub recommends that you use the built-in `GITHUB_TOKEN` instead of creating a token. If this is not possible, store your token as a secret and replace `GITHUB_TOKEN` in the example below with the name of your secret. For more information about `GITHUB_TOKEN`, see [Use GITHUB_TOKEN for authentication in workflows](https://docs.github.com/en/actions/security-guides/automatic-token-authentication). For more information about secrets, see [Using secrets in GitHub Actions](https://docs.github.com/en/actions/security-guides/encrypted-secrets).

The following example workflow:

1. Checks out the repository content
2. Sets up Node.js
3. Installs `octokit`
4. Stores the value of `GITHUB_TOKEN` as an environment variable called `TOKEN` and runs `.github/actions-scripts/use-the-api.mjs`, which can access that environment variable as `process.env.TOKEN`

```yaml
on:
  workflow_dispatch:
jobs:
  use_api_via_script:
    runs-on: ubuntu-latest
    permissions:
      issues: read
    steps:
      - name: Check out repo content
        uses: actions/checkout@v5

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '16.17.0'
          cache: npm

      - name: Install dependencies
        run: npm install octokit

      - name: Run script
        run: |
          node .github/actions-scripts/use-the-api.mjs
        env:
          TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

The following is an example JavaScript script with the file path `.github/actions-scripts/use-the-api.mjs`.

```javascript
import { Octokit } from "octokit"

const octokit = new Octokit({
  auth: process.env.TOKEN
});

try {
  const result = await octokit.request("GET /repos/{owner}/{repo}/issues", {
      owner: "octocat",
      repo: "Spoon-Knife",
    });

  const titleAndAuthor = result.data.map(issue => {title: issue.title, authorID: issue.user.id})

  console.log(titleAndAuthor)

} catch (error) {
  console.log(`Error! Status: ${error.status}. Message: ${error.response.data.message}`)
}
```

### Authenticating with a GitHub App

If you are authenticating with a GitHub App, you can create an installation access token within your workflow:

1. Store your GitHub App's ID as a configuration variable. In the following example, replace `APP_ID` with the name of the configuration variable. You can find your app ID on the settings page for your app or through the App API. For more information, see [REST API endpoints for GitHub Apps](https://docs.github.com/en/rest/apps/apps#get-an-app). For more information about configuration variables, see [Store information in variables](https://docs.github.com/en/actions/learn-github-actions/variables#defining-configuration-variables-for-multiple-workflows).
2. Generate a private key for your app. Store the contents of the resulting file as a secret. (Store the entire contents of the file, including `-----BEGIN RSA PRIVATE KEY-----` and `-----END RSA PRIVATE KEY-----`.) In the following example, replace `APP_PEM` with the name of the secret. For more information, see [Managing private keys for GitHub Apps](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/managing-private-keys-for-github-apps). For more information about secrets, see [Using secrets in GitHub Actions](https://docs.github.com/en/actions/security-guides/encrypted-secrets).
3. Add a step to generate a token, and use that token instead of `GITHUB_TOKEN`. Note that this token will expire after 60 minutes. For example:
  ```yaml
  on:
    workflow_dispatch:
  jobs:
    use_api_via_script:
      runs-on: ubuntu-latest
      steps:
        - name: Check out repo content
          uses: actions/checkout@v5
        - name: Setup Node
          uses: actions/setup-node@v4
          with:
            node-version: '16.17.0'
            cache: npm
        - name: Install dependencies
          run: npm install octokit
        - name: Generate token
          id: generate-token
          uses: actions/create-github-app-token@v2
          with:
            app-id: ${{ vars.APP_ID }}
            private-key: ${{ secrets.APP_PEM }}
        - name: Run script
          run: |
            node .github/actions-scripts/use-the-api.mjs
          env:
            TOKEN: ${{ steps.generate-token.outputs.token }}
  ```

## Usingcurlin the command line

Note

If you want to make API requests from the command line, GitHub recommends that you use GitHub CLI, which simplifies authentication and requests. For more information about getting started with the REST API using GitHub CLI, see the GitHub CLI version of this article.

1. Install `curl` if it isn't already installed on your machine. To check if `curl` is installed, execute `curl --version` in the command line. If the output provides information about the version of `curl`, that means `curl` is installed. If you get a message similar to `command not found: curl`, you need to download and install `curl`. For more information, see [the curl project download page](https://curl.se/download.html).
2. Create an access token. For example, create a personal access token or a GitHub App user access token. You will use this token to authenticate your request, so you should give it any scopes or permissions that are required to access the endpoint. For more information, see [Authenticating to the REST API](https://docs.github.com/en/rest/overview/authenticating-to-the-rest-api).
  Warning
  Treat your access token like a password.
  To keep your token secure, you can store your token as a Codespaces secret and use the command line through Codespaces. For more information, see [Managing encrypted secrets for your codespaces](https://docs.github.com/en/codespaces/managing-your-codespaces/managing-encrypted-secrets-for-your-codespaces).
  > You can also use GitHub CLI instead of `curl`. GitHub CLI will take care of authentication for you. For more information, see the GitHub CLI version of this page.
  >
  >
  >
  > If these options are not possible, consider using another CLI service to store your token securely.
3. Use the `curl` command to make your request. Pass your token in an `Authorization` header. Replace `YOUR-TOKEN` with your token.
  ```shell
  curl --request GET \
  --url "https://api.github.com/repos/octocat/Spoon-Knife/issues" \
  --header "Accept: application/vnd.github+json" \
  --header "Authorization: Bearer YOUR-TOKEN"
  ```
  Note
  In most cases, you can use `Authorization: Bearer` or `Authorization: token` to pass a token. However, if you are passing a JSON web token (JWT), you must use `Authorization: Bearer`.

## Usingcurlcommands in GitHub Actions

You can also use `curl` commands in your GitHub Actions workflows.

### Authenticating with an access token

GitHub recommends that you use the built-in `GITHUB_TOKEN` instead of creating a token. If this is not possible, store your token as a secret and replace `GITHUB_TOKEN` in the example below with the name of your secret. For more information about `GITHUB_TOKEN`, see [Use GITHUB_TOKEN for authentication in workflows](https://docs.github.com/en/actions/security-guides/automatic-token-authentication). For more information about secrets, see [Using secrets in GitHub Actions](https://docs.github.com/en/actions/security-guides/encrypted-secrets).

```yaml
on:
  workflow_dispatch:
jobs:
  use_api:
    runs-on: ubuntu-latest
    permissions:
      issues: read
    steps:
      - env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          curl --request GET \
          --url "https://api.github.com/repos/octocat/Spoon-Knife/issues" \
          --header "Accept: application/vnd.github+json" \
          --header "Authorization: Bearer $GH_TOKEN"
```

### Authenticating with a GitHub App

If you are authenticating with a GitHub App, you can create an installation access token within your workflow:

1. Store your GitHub App's ID as a configuration variable. In the following example, replace `APP_ID` with the name of the configuration variable. You can find your app ID on the settings page for your app or through the App API. For more information, see [REST API endpoints for GitHub Apps](https://docs.github.com/en/rest/apps/apps#get-an-app). For more information about configuration variables, see [Store information in variables](https://docs.github.com/en/actions/learn-github-actions/variables#defining-configuration-variables-for-multiple-workflows).
2. Generate a private key for your app. Store the contents of the resulting file as a secret. (Store the entire contents of the file, including `-----BEGIN RSA PRIVATE KEY-----` and `-----END RSA PRIVATE KEY-----`.) In the following example, replace `APP_PEM` with the name of the secret. For more information, see [Managing private keys for GitHub Apps](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/managing-private-keys-for-github-apps). For more information about storing secrets, see [Using secrets in GitHub Actions](https://docs.github.com/en/actions/security-guides/encrypted-secrets).
3. Add a step to generate a token, and use that token instead of `GITHUB_TOKEN`. Note that this token will expire after 60 minutes. For example:
  ```yaml
  on:
    workflow_dispatch:
  jobs:
    use_api:
      runs-on: ubuntu-latest
      steps:
        - name: Generate token
          id: generate-token
          uses: actions/create-github-app-token@v2
          with:
            app-id: ${{ vars.APP_ID }}
            private-key: ${{ secrets.APP_PEM }}
        - name: Use API
          env:
            GH_TOKEN: ${{ steps.generate-token.outputs.token }}
          run: |
            curl --request GET \
            --url "https://api.github.com/repos/octocat/Spoon-Knife/issues" \
            --header "Accept: application/vnd.github+json" \
            --header "Authorization: Bearer $GH_TOKEN"
  ```

## Next steps

For a more detailed guide, see [Getting started with the REST API](https://docs.github.com/en/rest/guides/getting-started-with-the-rest-api).

---

# REST API endpoints for rate limits

> Use the REST API to check your current rate limit status.

The REST API is now versioned. For more information, see "[About API versioning](https://docs.github.com/rest/overview/api-versions)."

# REST API endpoints for rate limits

Use the REST API to check your current rate limit status.

- [REST API endpoints for rate limits](https://docs.github.com/en/rest/rate-limit/rate-limit)
  - [Get rate limit status for the authenticated user](https://docs.github.com/en/rest/rate-limit/rate-limit#get-rate-limit-status-for-the-authenticated-user)

---

# REST API endpoints for reactions

> Use the REST API to interact with reactions on GitHub.

The REST API is now versioned. For more information, see "[About API versioning](https://docs.github.com/rest/overview/api-versions)."

# REST API endpoints for reactions

Use the REST API to interact with reactions on GitHub.

- [REST API endpoints for reactions](https://docs.github.com/en/rest/reactions/reactions)
  - [List reactions for a commit comment](https://docs.github.com/en/rest/reactions/reactions#list-reactions-for-a-commit-comment)
  - [Create reaction for a commit comment](https://docs.github.com/en/rest/reactions/reactions#create-reaction-for-a-commit-comment)
  - [Delete a commit comment reaction](https://docs.github.com/en/rest/reactions/reactions#delete-a-commit-comment-reaction)
  - [List reactions for an issue comment](https://docs.github.com/en/rest/reactions/reactions#list-reactions-for-an-issue-comment)
  - [Create reaction for an issue comment](https://docs.github.com/en/rest/reactions/reactions#create-reaction-for-an-issue-comment)
  - [Delete an issue comment reaction](https://docs.github.com/en/rest/reactions/reactions#delete-an-issue-comment-reaction)
  - [List reactions for an issue](https://docs.github.com/en/rest/reactions/reactions#list-reactions-for-an-issue)
  - [Create reaction for an issue](https://docs.github.com/en/rest/reactions/reactions#create-reaction-for-an-issue)
  - [Delete an issue reaction](https://docs.github.com/en/rest/reactions/reactions#delete-an-issue-reaction)
  - [List reactions for a pull request review comment](https://docs.github.com/en/rest/reactions/reactions#list-reactions-for-a-pull-request-review-comment)
  - [Create reaction for a pull request review comment](https://docs.github.com/en/rest/reactions/reactions#create-reaction-for-a-pull-request-review-comment)
  - [Delete a pull request comment reaction](https://docs.github.com/en/rest/reactions/reactions#delete-a-pull-request-comment-reaction)
  - [List reactions for a release](https://docs.github.com/en/rest/reactions/reactions#list-reactions-for-a-release)
  - [Create reaction for a release](https://docs.github.com/en/rest/reactions/reactions#create-reaction-for-a-release)
  - [Delete a release reaction](https://docs.github.com/en/rest/reactions/reactions#delete-a-release-reaction)

---

# REST API endpoints for releases and release assets

> Use the REST API to create, modify, and delete releases and release assets.

The REST API is now versioned. For more information, see "[About API versioning](https://docs.github.com/rest/overview/api-versions)."

# REST API endpoints for releases and release assets

Use the REST API to create, modify, and delete releases and release assets.

- [REST API endpoints for releases](https://docs.github.com/en/rest/releases/releases)
  - [List releases](https://docs.github.com/en/rest/releases/releases#list-releases)
  - [Create a release](https://docs.github.com/en/rest/releases/releases#create-a-release)
  - [Generate release notes content for a release](https://docs.github.com/en/rest/releases/releases#generate-release-notes-content-for-a-release)
  - [Get the latest release](https://docs.github.com/en/rest/releases/releases#get-the-latest-release)
  - [Get a release by tag name](https://docs.github.com/en/rest/releases/releases#get-a-release-by-tag-name)
  - [Get a release](https://docs.github.com/en/rest/releases/releases#get-a-release)
  - [Update a release](https://docs.github.com/en/rest/releases/releases#update-a-release)
  - [Delete a release](https://docs.github.com/en/rest/releases/releases#delete-a-release)
- [REST API endpoints for release assets](https://docs.github.com/en/rest/releases/assets)
  - [Get a release asset](https://docs.github.com/en/rest/releases/assets#get-a-release-asset)
  - [Update a release asset](https://docs.github.com/en/rest/releases/assets#update-a-release-asset)
  - [Delete a release asset](https://docs.github.com/en/rest/releases/assets#delete-a-release-asset)
  - [List release assets](https://docs.github.com/en/rest/releases/assets#list-release-assets)
  - [Upload a release asset](https://docs.github.com/en/rest/releases/assets#upload-a-release-asset)

---

# REST API endpoints for repositories

> Use the REST API to create, manage and control the workflow of public and private GitHub repositories.

The REST API is now versioned. For more information, see "[About API versioning](https://docs.github.com/rest/overview/api-versions)."

# REST API endpoints for repositories

Use the REST API to create, manage and control the workflow of public and private GitHub repositories.

- [REST API endpoints for repositories](https://docs.github.com/en/rest/repos/repos)
  - [List organization repositories](https://docs.github.com/en/rest/repos/repos#list-organization-repositories)
  - [Create an organization repository](https://docs.github.com/en/rest/repos/repos#create-an-organization-repository)
  - [Get a repository](https://docs.github.com/en/rest/repos/repos#get-a-repository)
  - [Update a repository](https://docs.github.com/en/rest/repos/repos#update-a-repository)
  - [Delete a repository](https://docs.github.com/en/rest/repos/repos#delete-a-repository)
  - [List repository activities](https://docs.github.com/en/rest/repos/repos#list-repository-activities)
  - [Check if Dependabot security updates are enabled for a repository](https://docs.github.com/en/rest/repos/repos#check-if-dependabot-security-updates-are-enabled-for-a-repository)
  - [Enable Dependabot security updates](https://docs.github.com/en/rest/repos/repos#enable-dependabot-security-updates)
  - [Disable Dependabot security updates](https://docs.github.com/en/rest/repos/repos#disable-dependabot-security-updates)
  - [List CODEOWNERS errors](https://docs.github.com/en/rest/repos/repos#list-codeowners-errors)
  - [List repository contributors](https://docs.github.com/en/rest/repos/repos#list-repository-contributors)
  - [Create a repository dispatch event](https://docs.github.com/en/rest/repos/repos#create-a-repository-dispatch-event)
  - [Check if immutable releases are enabled for a repository](https://docs.github.com/en/rest/repos/repos#check-if-immutable-releases-are-enabled-for-a-repository)
  - [Enable immutable releases](https://docs.github.com/en/rest/repos/repos#enable-immutable-releases)
  - [Disable immutable releases](https://docs.github.com/en/rest/repos/repos#disable-immutable-releases)
  - [List repository languages](https://docs.github.com/en/rest/repos/repos#list-repository-languages)
  - [Check if private vulnerability reporting is enabled for a repository](https://docs.github.com/en/rest/repos/repos#check-if-private-vulnerability-reporting-is-enabled-for-a-repository)
  - [Enable private vulnerability reporting for a repository](https://docs.github.com/en/rest/repos/repos#enable-private-vulnerability-reporting-for-a-repository)
  - [Disable private vulnerability reporting for a repository](https://docs.github.com/en/rest/repos/repos#disable-private-vulnerability-reporting-for-a-repository)
  - [List repository tags](https://docs.github.com/en/rest/repos/repos#list-repository-tags)
  - [List repository teams](https://docs.github.com/en/rest/repos/repos#list-repository-teams)
  - [Get all repository topics](https://docs.github.com/en/rest/repos/repos#get-all-repository-topics)
  - [Replace all repository topics](https://docs.github.com/en/rest/repos/repos#replace-all-repository-topics)
  - [Transfer a repository](https://docs.github.com/en/rest/repos/repos#transfer-a-repository)
  - [Check if vulnerability alerts are enabled for a repository](https://docs.github.com/en/rest/repos/repos#check-if-vulnerability-alerts-are-enabled-for-a-repository)
  - [Enable vulnerability alerts](https://docs.github.com/en/rest/repos/repos#enable-vulnerability-alerts)
  - [Disable vulnerability alerts](https://docs.github.com/en/rest/repos/repos#disable-vulnerability-alerts)
  - [Create a repository using a template](https://docs.github.com/en/rest/repos/repos#create-a-repository-using-a-template)
  - [List public repositories](https://docs.github.com/en/rest/repos/repos#list-public-repositories)
  - [List repositories for the authenticated user](https://docs.github.com/en/rest/repos/repos#list-repositories-for-the-authenticated-user)
  - [Create a repository for the authenticated user](https://docs.github.com/en/rest/repos/repos#create-a-repository-for-the-authenticated-user)
  - [List repositories for a user](https://docs.github.com/en/rest/repos/repos#list-repositories-for-a-user)
- [REST API endpoints for repository attestations](https://docs.github.com/en/rest/repos/attestations)
  - [Create an attestation](https://docs.github.com/en/rest/repos/attestations#create-an-attestation)
  - [List attestations](https://docs.github.com/en/rest/repos/attestations#list-attestations)
- [REST API endpoints for repository autolinks](https://docs.github.com/en/rest/repos/autolinks)
  - [Get all autolinks of a repository](https://docs.github.com/en/rest/repos/autolinks#get-all-autolinks-of-a-repository)
  - [Create an autolink reference for a repository](https://docs.github.com/en/rest/repos/autolinks#create-an-autolink-reference-for-a-repository)
  - [Get an autolink reference of a repository](https://docs.github.com/en/rest/repos/autolinks#get-an-autolink-reference-of-a-repository)
  - [Delete an autolink reference from a repository](https://docs.github.com/en/rest/repos/autolinks#delete-an-autolink-reference-from-a-repository)
- [REST API endpoints for repository contents](https://docs.github.com/en/rest/repos/contents)
  - [Get repository content](https://docs.github.com/en/rest/repos/contents#get-repository-content)
  - [Create or update file contents](https://docs.github.com/en/rest/repos/contents#create-or-update-file-contents)
  - [Delete a file](https://docs.github.com/en/rest/repos/contents#delete-a-file)
  - [Get a repository README](https://docs.github.com/en/rest/repos/contents#get-a-repository-readme)
  - [Get a repository README for a directory](https://docs.github.com/en/rest/repos/contents#get-a-repository-readme-for-a-directory)
  - [Download a repository archive (tar)](https://docs.github.com/en/rest/repos/contents#download-a-repository-archive-tar)
  - [Download a repository archive (zip)](https://docs.github.com/en/rest/repos/contents#download-a-repository-archive-zip)
- [REST API endpoints for custom properties](https://docs.github.com/en/rest/repos/custom-properties)
  - [Get all custom property values for a repository](https://docs.github.com/en/rest/repos/custom-properties#get-all-custom-property-values-for-a-repository)
  - [Create or update custom property values for a repository](https://docs.github.com/en/rest/repos/custom-properties#create-or-update-custom-property-values-for-a-repository)
- [REST API endpoints for forks](https://docs.github.com/en/rest/repos/forks)
  - [List forks](https://docs.github.com/en/rest/repos/forks#list-forks)
  - [Create a fork](https://docs.github.com/en/rest/repos/forks#create-a-fork)
- [REST API endpoints for rule suites](https://docs.github.com/en/rest/repos/rule-suites)
  - [List repository rule suites](https://docs.github.com/en/rest/repos/rule-suites#list-repository-rule-suites)
  - [Get a repository rule suite](https://docs.github.com/en/rest/repos/rule-suites#get-a-repository-rule-suite)
- [REST API endpoints for rules](https://docs.github.com/en/rest/repos/rules)
  - [Get rules for a branch](https://docs.github.com/en/rest/repos/rules#get-rules-for-a-branch)
  - [Get all repository rulesets](https://docs.github.com/en/rest/repos/rules#get-all-repository-rulesets)
  - [Create a repository ruleset](https://docs.github.com/en/rest/repos/rules#create-a-repository-ruleset)
  - [Get a repository ruleset](https://docs.github.com/en/rest/repos/rules#get-a-repository-ruleset)
  - [Update a repository ruleset](https://docs.github.com/en/rest/repos/rules#update-a-repository-ruleset)
  - [Delete a repository ruleset](https://docs.github.com/en/rest/repos/rules#delete-a-repository-ruleset)
  - [Get repository ruleset history](https://docs.github.com/en/rest/repos/rules#get-repository-ruleset-history)
  - [Get repository ruleset version](https://docs.github.com/en/rest/repos/rules#get-repository-ruleset-version)
- [REST API endpoints for repository tags](https://docs.github.com/en/rest/repos/tags)
  - [Closing down - List tag protection states for a repository](https://docs.github.com/en/rest/repos/tags#closing-down---list-tag-protection-states-for-a-repository)
  - [Closing down - Create a tag protection state for a repository](https://docs.github.com/en/rest/repos/tags#closing-down---create-a-tag-protection-state-for-a-repository)
  - [Closing down - Delete a tag protection state for a repository](https://docs.github.com/en/rest/repos/tags#closing-down---delete-a-tag-protection-state-for-a-repository)
- [REST API endpoints for repository webhooks](https://docs.github.com/en/rest/repos/webhooks)
  - [List repository webhooks](https://docs.github.com/en/rest/repos/webhooks#list-repository-webhooks)
  - [Create a repository webhook](https://docs.github.com/en/rest/repos/webhooks#create-a-repository-webhook)
  - [Get a repository webhook](https://docs.github.com/en/rest/repos/webhooks#get-a-repository-webhook)
  - [Update a repository webhook](https://docs.github.com/en/rest/repos/webhooks#update-a-repository-webhook)
  - [Delete a repository webhook](https://docs.github.com/en/rest/repos/webhooks#delete-a-repository-webhook)
  - [Get a webhook configuration for a repository](https://docs.github.com/en/rest/repos/webhooks#get-a-webhook-configuration-for-a-repository)
  - [Update a webhook configuration for a repository](https://docs.github.com/en/rest/repos/webhooks#update-a-webhook-configuration-for-a-repository)
  - [List deliveries for a repository webhook](https://docs.github.com/en/rest/repos/webhooks#list-deliveries-for-a-repository-webhook)
  - [Get a delivery for a repository webhook](https://docs.github.com/en/rest/repos/webhooks#get-a-delivery-for-a-repository-webhook)
  - [Redeliver a delivery for a repository webhook](https://docs.github.com/en/rest/repos/webhooks#redeliver-a-delivery-for-a-repository-webhook)
  - [Ping a repository webhook](https://docs.github.com/en/rest/repos/webhooks#ping-a-repository-webhook)
  - [Test the push repository webhook](https://docs.github.com/en/rest/repos/webhooks#test-the-push-repository-webhook)

---

# REST API endpoints for search

> Use the REST API to search for specific items on GitHub.

The REST API is now versioned. For more information, see "[About API versioning](https://docs.github.com/rest/overview/api-versions)."

# REST API endpoints for search

Use the REST API to search for specific items on GitHub.

- [REST API endpoints for search](https://docs.github.com/en/rest/search/search)
  - [Search code](https://docs.github.com/en/rest/search/search#search-code)
  - [Search commits](https://docs.github.com/en/rest/search/search#search-commits)
  - [Search issues and pull requests](https://docs.github.com/en/rest/search/search#search-issues-and-pull-requests)
  - [Search labels](https://docs.github.com/en/rest/search/search#search-labels)
  - [Search repositories](https://docs.github.com/en/rest/search/search#search-repositories)
  - [Search topics](https://docs.github.com/en/rest/search/search#search-topics)
  - [Search users](https://docs.github.com/en/rest/search/search#search-users)

---

# REST API endpoints for secret scanning

> Use the REST API to retrieve and update secret alerts from a repository.

The REST API is now versioned. For more information, see "[About API versioning](https://docs.github.com/rest/overview/api-versions)."

# REST API endpoints for secret scanning

Use the REST API to retrieve and update secret alerts from a repository.

- [REST API endpoints for secret scanning](https://docs.github.com/en/rest/secret-scanning/secret-scanning)
  - [List secret scanning alerts for an organization](https://docs.github.com/en/rest/secret-scanning/secret-scanning#list-secret-scanning-alerts-for-an-organization)
  - [List secret scanning alerts for a repository](https://docs.github.com/en/rest/secret-scanning/secret-scanning#list-secret-scanning-alerts-for-a-repository)
  - [Get a secret scanning alert](https://docs.github.com/en/rest/secret-scanning/secret-scanning#get-a-secret-scanning-alert)
  - [Update a secret scanning alert](https://docs.github.com/en/rest/secret-scanning/secret-scanning#update-a-secret-scanning-alert)
  - [List locations for a secret scanning alert](https://docs.github.com/en/rest/secret-scanning/secret-scanning#list-locations-for-a-secret-scanning-alert)
  - [Create a push protection bypass](https://docs.github.com/en/rest/secret-scanning/secret-scanning#create-a-push-protection-bypass)
  - [Get secret scanning scan history for a repository](https://docs.github.com/en/rest/secret-scanning/secret-scanning#get-secret-scanning-scan-history-for-a-repository)
- [REST API endpoints for secret scanning push protection](https://docs.github.com/en/rest/secret-scanning/push-protection)
  - [List organization pattern configurations](https://docs.github.com/en/rest/secret-scanning/push-protection#list-organization-pattern-configurations)
  - [Update organization pattern configurations](https://docs.github.com/en/rest/secret-scanning/push-protection#update-organization-pattern-configurations)

---

# REST API endpoints for security advisories

> Use the REST API to view and manage security advisories.

The REST API is now versioned. For more information, see "[About API versioning](https://docs.github.com/rest/overview/api-versions)."

# REST API endpoints for security advisories

Use the REST API to view and manage security advisories.

- [REST API endpoints for global security advisories](https://docs.github.com/en/rest/security-advisories/global-advisories)
  - [List global security advisories](https://docs.github.com/en/rest/security-advisories/global-advisories#list-global-security-advisories)
  - [Get a global security advisory](https://docs.github.com/en/rest/security-advisories/global-advisories#get-a-global-security-advisory)
- [REST API endpoints for repository security advisories](https://docs.github.com/en/rest/security-advisories/repository-advisories)
  - [List repository security advisories for an organization](https://docs.github.com/en/rest/security-advisories/repository-advisories#list-repository-security-advisories-for-an-organization)
  - [List repository security advisories](https://docs.github.com/en/rest/security-advisories/repository-advisories#list-repository-security-advisories)
  - [Create a repository security advisory](https://docs.github.com/en/rest/security-advisories/repository-advisories#create-a-repository-security-advisory)
  - [Privately report a security vulnerability](https://docs.github.com/en/rest/security-advisories/repository-advisories#privately-report-a-security-vulnerability)
  - [Get a repository security advisory](https://docs.github.com/en/rest/security-advisories/repository-advisories#get-a-repository-security-advisory)
  - [Update a repository security advisory](https://docs.github.com/en/rest/security-advisories/repository-advisories#update-a-repository-security-advisory)
  - [Request a CVE for a repository security advisory](https://docs.github.com/en/rest/security-advisories/repository-advisories#request-a-cve-for-a-repository-security-advisory)
  - [Create a temporary private fork](https://docs.github.com/en/rest/security-advisories/repository-advisories#create-a-temporary-private-fork)

---

# REST API endpoints for teams

> Use the REST API to create and manage teams in your GitHub organization.

The REST API is now versioned. For more information, see "[About API versioning](https://docs.github.com/rest/overview/api-versions)."

# REST API endpoints for teams

Use the REST API to create and manage teams in your GitHub organization.

- [REST API endpoints for teams](https://docs.github.com/en/rest/teams/teams)
  - [List teams](https://docs.github.com/en/rest/teams/teams#list-teams)
  - [Create a team](https://docs.github.com/en/rest/teams/teams#create-a-team)
  - [Get a team by name](https://docs.github.com/en/rest/teams/teams#get-a-team-by-name)
  - [Update a team](https://docs.github.com/en/rest/teams/teams#update-a-team)
  - [Delete a team](https://docs.github.com/en/rest/teams/teams#delete-a-team)
  - [List team repositories](https://docs.github.com/en/rest/teams/teams#list-team-repositories)
  - [Check team permissions for a repository](https://docs.github.com/en/rest/teams/teams#check-team-permissions-for-a-repository)
  - [Add or update team repository permissions](https://docs.github.com/en/rest/teams/teams#add-or-update-team-repository-permissions)
  - [Remove a repository from a team](https://docs.github.com/en/rest/teams/teams#remove-a-repository-from-a-team)
  - [List child teams](https://docs.github.com/en/rest/teams/teams#list-child-teams)
  - [Get a team (Legacy)](https://docs.github.com/en/rest/teams/teams#get-a-team-legacy)
  - [Update a team (Legacy)](https://docs.github.com/en/rest/teams/teams#update-a-team-legacy)
  - [Delete a team (Legacy)](https://docs.github.com/en/rest/teams/teams#delete-a-team-legacy)
  - [List team repositories (Legacy)](https://docs.github.com/en/rest/teams/teams#list-team-repositories-legacy)
  - [Check team permissions for a repository (Legacy)](https://docs.github.com/en/rest/teams/teams#check-team-permissions-for-a-repository-legacy)
  - [Add or update team repository permissions (Legacy)](https://docs.github.com/en/rest/teams/teams#add-or-update-team-repository-permissions-legacy)
  - [Remove a repository from a team (Legacy)](https://docs.github.com/en/rest/teams/teams#remove-a-repository-from-a-team-legacy)
  - [List child teams (Legacy)](https://docs.github.com/en/rest/teams/teams#list-child-teams-legacy)
  - [List teams for the authenticated user](https://docs.github.com/en/rest/teams/teams#list-teams-for-the-authenticated-user)
- [REST API endpoints for team members](https://docs.github.com/en/rest/teams/members)
  - [List pending team invitations](https://docs.github.com/en/rest/teams/members#list-pending-team-invitations)
  - [List team members](https://docs.github.com/en/rest/teams/members#list-team-members)
  - [Get team membership for a user](https://docs.github.com/en/rest/teams/members#get-team-membership-for-a-user)
  - [Add or update team membership for a user](https://docs.github.com/en/rest/teams/members#add-or-update-team-membership-for-a-user)
  - [Remove team membership for a user](https://docs.github.com/en/rest/teams/members#remove-team-membership-for-a-user)
  - [List pending team invitations (Legacy)](https://docs.github.com/en/rest/teams/members#list-pending-team-invitations-legacy)
  - [List team members (Legacy)](https://docs.github.com/en/rest/teams/members#list-team-members-legacy)
  - [Get team member (Legacy)](https://docs.github.com/en/rest/teams/members#get-team-member-legacy)
  - [Add team member (Legacy)](https://docs.github.com/en/rest/teams/members#add-team-member-legacy)
  - [Remove team member (Legacy)](https://docs.github.com/en/rest/teams/members#remove-team-member-legacy)
  - [Get team membership for a user (Legacy)](https://docs.github.com/en/rest/teams/members#get-team-membership-for-a-user-legacy)
  - [Add or update team membership for a user (Legacy)](https://docs.github.com/en/rest/teams/members#add-or-update-team-membership-for-a-user-legacy)
  - [Remove team membership for a user (Legacy)](https://docs.github.com/en/rest/teams/members#remove-team-membership-for-a-user-legacy)

---

# REST API endpoints for users

> Use the REST API to get public and private information about authenticated users.

The REST API is now versioned. For more information, see "[About API versioning](https://docs.github.com/rest/overview/api-versions)."

# REST API endpoints for users

Use the REST API to get public and private information about authenticated users.

- [REST API endpoints for users](https://docs.github.com/en/rest/users/users)
  - [Get the authenticated user](https://docs.github.com/en/rest/users/users#get-the-authenticated-user)
  - [Update the authenticated user](https://docs.github.com/en/rest/users/users#update-the-authenticated-user)
  - [Get a user using their ID](https://docs.github.com/en/rest/users/users#get-a-user-using-their-id)
  - [List users](https://docs.github.com/en/rest/users/users#list-users)
  - [Get a user](https://docs.github.com/en/rest/users/users#get-a-user)
  - [Get contextual information for a user](https://docs.github.com/en/rest/users/users#get-contextual-information-for-a-user)
- [REST API endpoints for artifact attestations](https://docs.github.com/en/rest/users/attestations)
  - [List attestations by bulk subject digests](https://docs.github.com/en/rest/users/attestations#list-attestations-by-bulk-subject-digests)
  - [Delete attestations in bulk](https://docs.github.com/en/rest/users/attestations#delete-attestations-in-bulk)
  - [Delete attestations by subject digest](https://docs.github.com/en/rest/users/attestations#delete-attestations-by-subject-digest)
  - [Delete attestations by ID](https://docs.github.com/en/rest/users/attestations#delete-attestations-by-id)
  - [List attestations](https://docs.github.com/en/rest/users/attestations#list-attestations)
- [REST API endpoints for blocking users](https://docs.github.com/en/rest/users/blocking)
  - [List users blocked by the authenticated user](https://docs.github.com/en/rest/users/blocking#list-users-blocked-by-the-authenticated-user)
  - [Check if a user is blocked by the authenticated user](https://docs.github.com/en/rest/users/blocking#check-if-a-user-is-blocked-by-the-authenticated-user)
  - [Block a user](https://docs.github.com/en/rest/users/blocking#block-a-user)
  - [Unblock a user](https://docs.github.com/en/rest/users/blocking#unblock-a-user)
- [REST API endpoints for emails](https://docs.github.com/en/rest/users/emails)
  - [Set primary email visibility for the authenticated user](https://docs.github.com/en/rest/users/emails#set-primary-email-visibility-for-the-authenticated-user)
  - [List email addresses for the authenticated user](https://docs.github.com/en/rest/users/emails#list-email-addresses-for-the-authenticated-user)
  - [Add an email address for the authenticated user](https://docs.github.com/en/rest/users/emails#add-an-email-address-for-the-authenticated-user)
  - [Delete an email address for the authenticated user](https://docs.github.com/en/rest/users/emails#delete-an-email-address-for-the-authenticated-user)
  - [List public email addresses for the authenticated user](https://docs.github.com/en/rest/users/emails#list-public-email-addresses-for-the-authenticated-user)
- [REST API endpoints for followers](https://docs.github.com/en/rest/users/followers)
  - [List followers of the authenticated user](https://docs.github.com/en/rest/users/followers#list-followers-of-the-authenticated-user)
  - [List the people the authenticated user follows](https://docs.github.com/en/rest/users/followers#list-the-people-the-authenticated-user-follows)
  - [Check if a person is followed by the authenticated user](https://docs.github.com/en/rest/users/followers#check-if-a-person-is-followed-by-the-authenticated-user)
  - [Follow a user](https://docs.github.com/en/rest/users/followers#follow-a-user)
  - [Unfollow a user](https://docs.github.com/en/rest/users/followers#unfollow-a-user)
  - [List followers of a user](https://docs.github.com/en/rest/users/followers#list-followers-of-a-user)
  - [List the people a user follows](https://docs.github.com/en/rest/users/followers#list-the-people-a-user-follows)
  - [Check if a user follows another user](https://docs.github.com/en/rest/users/followers#check-if-a-user-follows-another-user)
- [REST API endpoints for GPG keys](https://docs.github.com/en/rest/users/gpg-keys)
  - [List GPG keys for the authenticated user](https://docs.github.com/en/rest/users/gpg-keys#list-gpg-keys-for-the-authenticated-user)
  - [Create a GPG key for the authenticated user](https://docs.github.com/en/rest/users/gpg-keys#create-a-gpg-key-for-the-authenticated-user)
  - [Get a GPG key for the authenticated user](https://docs.github.com/en/rest/users/gpg-keys#get-a-gpg-key-for-the-authenticated-user)
  - [Delete a GPG key for the authenticated user](https://docs.github.com/en/rest/users/gpg-keys#delete-a-gpg-key-for-the-authenticated-user)
  - [List GPG keys for a user](https://docs.github.com/en/rest/users/gpg-keys#list-gpg-keys-for-a-user)
- [REST API endpoints for Git SSH keys](https://docs.github.com/en/rest/users/keys)
  - [List public SSH keys for the authenticated user](https://docs.github.com/en/rest/users/keys#list-public-ssh-keys-for-the-authenticated-user)
  - [Create a public SSH key for the authenticated user](https://docs.github.com/en/rest/users/keys#create-a-public-ssh-key-for-the-authenticated-user)
  - [Get a public SSH key for the authenticated user](https://docs.github.com/en/rest/users/keys#get-a-public-ssh-key-for-the-authenticated-user)
  - [Delete a public SSH key for the authenticated user](https://docs.github.com/en/rest/users/keys#delete-a-public-ssh-key-for-the-authenticated-user)
  - [List public keys for a user](https://docs.github.com/en/rest/users/keys#list-public-keys-for-a-user)
- [REST API endpoints for social accounts](https://docs.github.com/en/rest/users/social-accounts)
  - [List social accounts for the authenticated user](https://docs.github.com/en/rest/users/social-accounts#list-social-accounts-for-the-authenticated-user)
  - [Add social accounts for the authenticated user](https://docs.github.com/en/rest/users/social-accounts#add-social-accounts-for-the-authenticated-user)
  - [Delete social accounts for the authenticated user](https://docs.github.com/en/rest/users/social-accounts#delete-social-accounts-for-the-authenticated-user)
  - [List social accounts for a user](https://docs.github.com/en/rest/users/social-accounts#list-social-accounts-for-a-user)
- [REST API endpoints for SSH signing keys](https://docs.github.com/en/rest/users/ssh-signing-keys)
  - [List SSH signing keys for the authenticated user](https://docs.github.com/en/rest/users/ssh-signing-keys#list-ssh-signing-keys-for-the-authenticated-user)
  - [Create a SSH signing key for the authenticated user](https://docs.github.com/en/rest/users/ssh-signing-keys#create-a-ssh-signing-key-for-the-authenticated-user)
  - [Get an SSH signing key for the authenticated user](https://docs.github.com/en/rest/users/ssh-signing-keys#get-an-ssh-signing-key-for-the-authenticated-user)
  - [Delete an SSH signing key for the authenticated user](https://docs.github.com/en/rest/users/ssh-signing-keys#delete-an-ssh-signing-key-for-the-authenticated-user)
  - [List SSH signing keys for a user](https://docs.github.com/en/rest/users/ssh-signing-keys#list-ssh-signing-keys-for-a-user)

---

# Using the REST API

> Learn how to use the GitHub REST API, follow best practices, and troubleshoot problems.

# Using the REST API

Learn how to use the GitHub REST API, follow best practices, and troubleshoot problems.

- [Getting started with the REST API](https://docs.github.com/en/rest/using-the-rest-api/getting-started-with-the-rest-api)
- [Rate limits for the REST API](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api)
- [Using pagination in the REST API](https://docs.github.com/en/rest/using-the-rest-api/using-pagination-in-the-rest-api)
- [Libraries for the REST API](https://docs.github.com/en/rest/using-the-rest-api/libraries-for-the-rest-api)
- [Best practices for using the REST API](https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api)
- [Troubleshooting the REST API](https://docs.github.com/en/rest/using-the-rest-api/troubleshooting-the-rest-api)
- [Timezones and the REST API](https://docs.github.com/en/rest/using-the-rest-api/timezones-and-the-rest-api)
- [Using CORS and JSONP to make cross-origin requests](https://docs.github.com/en/rest/using-the-rest-api/using-cors-and-jsonp-to-make-cross-origin-requests)
- [Issue event types](https://docs.github.com/en/rest/using-the-rest-api/issue-event-types)
- [GitHub event types](https://docs.github.com/en/rest/using-the-rest-api/github-event-types)
