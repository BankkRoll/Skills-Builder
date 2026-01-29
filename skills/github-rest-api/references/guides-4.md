# Scripting with the REST API and Ruby and more

# Scripting with the REST API and Ruby

> Learn how to write a script using the Octokit.rb SDK to interact with the REST API.

## About Octokit.rb

If you want to write a script using Ruby to interact with the GitHub REST API, GitHub recommends that you use the Octokit.rb SDK. Octokit.rb is maintained by GitHub. The SDK implements best practices and makes it easier for you to interact with the REST API via Ruby. Octokit.rb works with all modern browsers, Node.rb, and Deno. For more information about Octokit.rb, see [the Octokit.rb README](https://github.com/octokit/octokit.rb/#readme).

## Prerequisites

This guide assumes that you are familiar with Ruby and the GitHub REST API. For more information about the REST API, see [Getting started with the REST API](https://docs.github.com/en/rest/guides/getting-started-with-the-rest-api).

You must install and import the `octokit` gem in order to use the Octokit.rb library. This guide uses import statements in accordance with Ruby's conventions. For more information about different installation methods, see [the Octokit.rb README's Installation section](https://github.com/octokit/octokit.rb/#installation).

## Instantiating and authenticating

Warning

Treat your authentication credentials like a password.

To keep your credentials secure, you can store your credentials as a secret and run your script through GitHub Actions. For more information, see [Using secrets in GitHub Actions](https://docs.github.com/en/actions/security-guides/encrypted-secrets).

> You can also store your credentials as a Codespaces secret and run your script in Codespaces. For more information, see [Managing your account-specific secrets for GitHub Codespaces](https://docs.github.com/en/codespaces/managing-your-codespaces/managing-encrypted-secrets-for-your-codespaces).

> If these options are not possible, consider using another CLI service to store your credentials securely.

### Authenticating with a personal access token

If you want to use the GitHub REST API for personal use, you can create a personal access token. For more information about creating a personal access token, see [Managing your personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens).

First, require the `octokit` library. Then, create an instance of `Octokit` by passing your personal access token as the `access_token` option. In the following example, replace `YOUR-TOKEN` with your personal access token.

```ruby
require 'octokit'

octokit = Octokit::Client.new(access_token: 'YOUR-TOKEN')
```

### Authenticating with a GitHub App

If you want to use the API on behalf of an organization or another user, GitHub recommends that you use a GitHub App. If an endpoint is available to GitHub Apps, the REST reference documentation for that endpoint will indicate what type of GitHub App token is required. For more information, see [Registering a GitHub App](https://docs.github.com/en/apps/creating-github-apps/setting-up-a-github-app/creating-a-github-app) and [About authentication with a GitHub App](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/about-authentication-with-a-github-app).

Instead of requiring `octokit`, create an instance of `Octokit::Client` by passing your GitHub App's information as options. In the following example, replace `APP_ID` with your app's ID, `PRIVATE_KEY` with your app's private key, and `INSTALLATION_ID` with the ID of the installation of your app that you want to authenticate on behalf of. You can find your app's ID and generate a private key on the settings page for your app. For more information, see [Managing private keys for GitHub Apps](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/managing-private-keys-for-github-apps). You can get an installation ID with the `GET /users/{username}/installation`, `GET /repos/{owner}/{repo}/installation`, or `GET /orgs/{org}/installation` endpoints. For more information, see [REST API endpoints for GitHub Apps](https://docs.github.com/en/rest/apps/apps).

```ruby
require 'octokit'

app = Octokit::Client.new(
  client_id: APP_ID,
  client_secret: PRIVATE_KEY,
  installation_id: INSTALLATION_ID
)

octokit = Octokit::Client.new(bearer_token: app.create_app_installation.access_token)
```

### Authenticating in GitHub Actions

If you want to use the API in a GitHub Actions workflow, GitHub recommends that you authenticate with the built-in `GITHUB_TOKEN` instead of creating a token. You can grant permissions to the `GITHUB_TOKEN` with the `permissions` key. For more information about `GITHUB_TOKEN`, see [Use GITHUB_TOKEN for authentication in workflows](https://docs.github.com/en/actions/security-guides/automatic-token-authentication#permissions-for-the-github_token).

If your workflow needs to access resources outside of the workflow's repository, then you will not be able to use `GITHUB_TOKEN`. In that case, store your credentials as a secret and replace `GITHUB_TOKEN` in the examples below with the name of your secret. For more information about secrets, see [Using secrets in GitHub Actions](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions).

If you use the `run` keyword to execute your Ruby script in your GitHub Actions workflows, you can store the value of `GITHUB_TOKEN` as an environment variable. Your script can access the environment variable as `ENV['VARIABLE_NAME']`.

For example, this workflow step stores `GITHUB_TOKEN` in an environment variable called `TOKEN`:

```yaml
- name: Run script
  env:
    TOKEN: ${{ secrets.GITHUB_TOKEN }}
  run: |
    ruby .github/actions-scripts/use-the-api.rb
```

The script that the workflow runs uses `ENV['TOKEN']` to authenticate:

```ruby
require 'octokit'

octokit = Octokit::Client.new(access_token: ENV['TOKEN'])
```

### Instantiating without authentication

You can use the REST API without authentication, although you will have a lower rate limit and will not be able to use some endpoints. To create an instance of `Octokit` without authenticating, do not pass the `access_token` option.

```ruby
require 'octokit'

octokit = Octokit::Client.new
```

## Making requests

Octokit supports multiple ways of making requests. You can use the `request` method to make requests if you know the HTTP verb and path for the endpoint. You can use the `rest` method if you want to take advantage of autocompletion in your IDE and typing. For paginated endpoints, you can use the `paginate` method to request multiple pages of data.

### Using therequestmethod to make requests

To use the `request` method to make requests, pass the HTTP method and path as the first argument. Pass any body, query, or path parameters in a hash as the second argument. For example, to make a `GET` request to `/repos/{owner}/{repo}/issues` and pass the `owner`, `repo`, and `per_page` parameters:

```ruby
octokit.request("GET /repos/{owner}/{repo}/issues", owner: "github", repo: "docs", per_page: 2)
```

The `request` method automatically passes the `Accept: application/vnd.github+json` header. To pass additional headers or a different `Accept` header, add a `headers` option to the hash that is passed as a second argument. The value of the `headers` option is a hash with the header names as keys and header values as values. For example, to send a `content-type` header with a value of `text/plain`:

```ruby
octokit.request("POST /markdown/raw", text: "Hello **world**", headers: { "content-type" => "text/plain" })
```

### Usingrestendpoint methods to make requests

Every REST API endpoint has an associated `rest` endpoint method in Octokit. These methods generally autocomplete in your IDE for convenience. You can pass any parameters as a hash to the method.

```ruby
octokit.rest.issues.list_for_repo(owner: "github", repo: "docs", per_page: 2)
```

### Making paginated requests

If the endpoint is paginated and you want to fetch more than one page of results, you can use the `paginate` method. `paginate` will fetch the next page of results until it reaches the last page and then return all of the results as an array. A few endpoints return paginated results as an array in an object, as opposed to returning the paginated results as an array. `paginate` always returns an array of items even if the raw result was an object.

For example, the following example gets all of the issues from the `github/docs` repository. Although it requests 100 issues at a time, the function won't return until the last page of data is reached.

```ruby
issue_data = octokit.paginate("GET /repos/{owner}/{repo}/issues", owner: "github", repo: "docs", per_page: 100)
```

The `paginate` method accepts an optional block, which you can use to process each page of results. This allows you to collect only the data that you want from the response. For example, the following example continues to fetch results until an issue that includes "test" in the title is returned. For the pages of data that were returned, only the issue title and author are stored.

```ruby
issue_data = octokit.paginate("GET /repos/{owner}/{repo}/issues", owner: "github", repo: "docs", per_page: 100) do |response, done|
  response.data.map do |issue|
    if issue.title.include?("test")
      done.call
    end
    { title: issue.title, author: issue.user.login }
  end
end
```

Instead of fetching all of the results at once, you can use `octokit.paginate.iterator()` to iterate through a single page at a time. For example, the following example fetches one page of results at a time and processes each object from the page before fetching the next page. Once an issue that includes "test" in the title is reached, the script stops the iteration and returns the issue title and issue author of each object that was processed. The iterator is the most memory-efficient method for fetching paginated data.

```ruby
iterator = octokit.paginate.iterator("GET /repos/{owner}/{repo}/issues", owner: "github", repo: "docs", per_page: 100)
issue_data = []
break_loop = false
iterator.each do |data|
  break if break_loop
  data.each do |issue|
    if issue.title.include?("test")
      break_loop = true
      break
    else
      issue_data << { title: issue.title, author: issue.user.login }
    end
  end
end
```

You can use the `paginate` method with the `rest` endpoint methods as well. Pass the `rest` endpoint method as the first argument and any parameters as the second argument.

```ruby
iterator = octokit.paginate.iterator(octokit.rest.issues.list_for_repo, owner: "github", repo: "docs", per_page: 100)
```

For more information about pagination, see [Using pagination in the REST API](https://docs.github.com/en/rest/guides/using-pagination-in-the-rest-api).

## Catching errors

### Catching all errors

Sometimes, the GitHub REST API will return an error. For example, you will get an error if your access token is expired or if you omitted a required parameter. Octokit.rb automatically retries the request when it gets an error other than `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`, and `422 Unprocessable Entity`. If an API error occurs even after retries, Octokit.rb throws an error that includes the HTTP status code of the response (`response.status`) and the response headers (`response.headers`). You should handle these errors in your code. For example, you can use a try/catch block to catch errors:

```ruby
begin
files_changed = []

iterator = octokit.paginate.iterator("GET /repos/{owner}/{repo}/pulls/{pull_number}/files", owner: "github", repo: "docs", pull_number: 22809, per_page: 100)
iterator.each do | data |
    files_changed.concat(data.map {
      | file_data | file_data.filename
    })
  end
rescue Octokit::Error => error
if error.response
puts "Error! Status: #{error.response.status}. Message: #{error.response.data.message}"
end
puts error
end
```

### Handling intended error codes

Sometimes, GitHub uses a 4xx status code to indicate a non-error response. If the endpoint you are using does this, you can add additional handling for specific errors. For example, the `GET /user/starred/{owner}/{repo}` endpoint will return a `404` if the repository is not starred. The following example uses the `404` response to indicate that the repository was not starred; all other error codes are treated as errors.

```ruby
begin
octokit.request("GET /user/starred/{owner}/{repo}", owner: "github", repo: "docs")
puts "The repository is starred by me"
rescue Octokit::NotFound => error
puts "The repository is not starred by me"
rescue Octokit::Error => error
puts "An error occurred while checking if the repository is starred: #{error&.response&.data&.message}"
end
```

### Handling rate limit errors

If you receive a rate limit error, you may want to retry your request after waiting. When you are rate limited, GitHub responds with a `403 Forbidden` error, and the `x-ratelimit-remaining` response header value will be `"0"`. The response headers will include a `x-ratelimit-reset` header, which tells you the time at which the current rate limit window resets, in UTC epoch seconds. You can retry your request after the time specified by `x-ratelimit-reset`.

```ruby
def request_retry(route, parameters)
 begin
 response = octokit.request(route, parameters)
 return response
 rescue Octokit::RateLimitExceeded => error
 reset_time_epoch_seconds = error.response.headers['x-ratelimit-reset'].to_i
 current_time_epoch_seconds = Time.now.to_i
 seconds_to_wait = reset_time_epoch_seconds - current_time_epoch_seconds
 puts "You have exceeded your rate limit. Retrying in #{seconds_to_wait} seconds."
 sleep(seconds_to_wait)
 retry
 rescue Octokit::Error => error
 puts error
 end
 end

 response = request_retry("GET /repos/{owner}/{repo}/issues", owner: "github", repo: "docs", per_page: 2)
```

## Using the response

The `request` method returns a response object if the request was successful. The response object contains `data` (the response body returned by the endpoint), `status` (the HTTP response code), `url` (the URL of the request), and `headers` (a hash containing the response headers). Unless otherwise specified, the response body is in JSON format. Some endpoints do not return a response body; in those cases, the `data` property is omitted.

```ruby
response = octokit.request("GET /repos/{owner}/{repo}/issues/{issue_number}", owner: "github", repo: "docs", issue_number: 11901)
 puts "The status of the response is: #{response.status}"
 puts "The request URL was: #{response.url}"
 puts "The x-ratelimit-remaining response header is: #{response.headers['x-ratelimit-remaining']}"
 puts "The issue title is: #{response.data['title']}"
```

Similarly, the `paginate` method returns a response object. If the `request` was successful, the `response` object contains data, status, url, and headers.

```ruby
response = octokit.paginate("GET /repos/{owner}/{repo}/issues", owner: "github", repo: "docs", per_page: 100)
puts "#{response.data.length} issues were returned"
puts "The title of the first issue is: #{response.data[0]['title']}"
```

## Example script

Here is a full example script that uses Octokit.rb. The script imports `Octokit` and creates a new instance of `Octokit`. If you want to authenticate with a GitHub App instead of a personal access token, you would import and instantiate `App` instead of `Octokit`. For more information, see [Authenticating with a GitHub App](#authenticating-with-a-github-app) in this guide.

The `get_changed_files` function gets all of the files changed for a pull request. The `comment_if_data_files_changed` function calls the `get_changed_files` function. If any of the files that the pull request changed include `/data/` in the file path, then the function will comment on the pull request.

```ruby
require "octokit"

 octokit = Octokit::Client.new(access_token: "YOUR-TOKEN")

 def get_changed_files(octokit, owner, repo, pull_number)
 files_changed = []

 begin
 iterator = octokit.paginate.iterator("GET /repos/{owner}/{repo}/pulls/{pull_number}/files", owner: owner, repo: repo, pull_number: pull_number, per_page: 100)
 iterator.each do | data |
     files_changed.concat(data.map {
       | file_data | file_data.filename
     })
   end
 rescue Octokit::Error => error
 if error.response
 puts "Error! Status: #{error.response.status}. Message: #{error.response.data.message}"
 end
 puts error
 end

 files_changed
 end

 def comment_if_data_files_changed(octokit, owner, repo, pull_number)
 changed_files = get_changed_files(octokit, owner, repo, pull_number)

 if changed_files.any ? {
   | file_name | /\/data\//i.match ? (file_name)
 }
 begin
 comment = octokit.create_pull_request_review_comment(owner, repo, pull_number, "It looks like you changed a data file. These files are auto-generated. \n\nYou must revert any changes to data files before your pull request will be reviewed.")
 comment.html_url
 rescue Octokit::Error => error
 if error.response
 puts "Error! Status: #{error.response.status}. Message: #{error.response.data.message}"
 end
 puts error
 end
 end
 end

# Example usage
owner = "github"
repo = "docs"
pull_number = 22809
comment_url = comment_if_data_files_changed(octokit, owner, repo, pull_number)

puts "A comment was added to the pull request: #{comment_url}"
```

Note

This is just a basic example. In practice, you may want to use error handling and conditional checks to handle various scenarios.

## Next steps

To learn more about working with the GitHub REST API and Octokit.rb, explore the following resources:

- To learn more about Octokit.rb see [the Octokit.rb documentation](https://github.com/octokit/octokit.rb/#readme).
- To find detailed information about GitHub's available REST API endpoints, including their request and response structures, see the [GitHub REST API documentation](https://docs.github.com/en/rest).

---

# Using pagination in the REST API

> Learn how to navigate through paginated responses from the REST API.

## About pagination

When a response from the REST API would include many results, GitHub will paginate the results and return a subset of the results. For example, `GET /repos/octocat/Spoon-Knife/issues` will only return 30 issues from the `octocat/Spoon-Knife` repository even though the repository includes over 1600 open issues. This makes the response easier to handle for servers and for people.

You can use the `link` header from the response to request additional pages of data. If an endpoint supports the `per_page` query parameter, you can control how many results are returned on a page.

This article demonstrates how to request additional pages of results for paginated responses, how to change the number of results returned on each page, and how to write a script to fetch multiple pages of results.

## Usinglinkheaders

When a response is paginated, the response headers will include a `link` header. If the endpoint does not support pagination, or if all results fit on a single page, the `link` header will be omitted.

The `link` header contains URLs that you can use to fetch additional pages of results. For example, the previous, next, first, and last page of results.

To see the response headers for a particular endpoint, you can use curl, GitHub CLI, or a library you're using to make requests. To see the response headers if you are using a library to make requests, follow the documentation for that library. To see the response headers if you are using curl or GitHub CLI, pass the `--include` flag with your request. For example:

```shell
curl --include --request GET \
--url "https://api.github.com/repos/octocat/Spoon-Knife/issues" \
--header "Accept: application/vnd.github+json"
```

If the response is paginated, the `link` header will look something like this:

```http
link: <https://api.github.com/repositories/1300192/issues?page=2>; rel="prev", <https://api.github.com/repositories/1300192/issues?page=4>; rel="next", <https://api.github.com/repositories/1300192/issues?page=515>; rel="last", <https://api.github.com/repositories/1300192/issues?page=1>; rel="first"
```

The `link` header provides the URL for the previous, next, first, and last page of results:

- The URL for the previous page is followed by `rel="prev"`.
- The URL for the next page is followed by `rel="next"`.
- The URL for the last page is followed by `rel="last"`.
- The URL for the first page is followed by `rel="first"`.

In some cases, only a subset of these links are available. For example, the link to the previous page won't be included if you are on the first page of results, and the link to the last page won't be included if it can't be calculated.

You can use the URLs from the `link` header to request another page of results. For example, to request the last page of results based on the previous example:

```shell
curl --include --request GET \
--url "https://api.github.com/repositories/1300192/issues?page=515" \
--header "Accept: application/vnd.github+json"
```

The URLs in the `link` header use query parameters to indicate which page of results to return. The query parameters in the `link` URLs may differ between endpoints, however each paginated endpoint will use the `page`, `before`/`after`, or `since` query parameters. (Some endpoints use the `since` parameter for something other than pagination.) In all cases, you can use the URLs in the `link` header to fetch additional pages of results. For more information about query parameters see [Getting started with the REST API](https://docs.github.com/en/rest/guides/getting-started-with-the-rest-api#using-query-parameters).

## Changing the number of items per page

If an endpoint supports the `per_page` query parameter, then you can control how many results are returned on a page. For more information about query parameters see [Getting started with the REST API](https://docs.github.com/en/rest/guides/getting-started-with-the-rest-api#using-query-parameters).

For example, this request uses the `per_page` query parameter to return two items per page:

```shell
curl --include --request GET \
--url "https://api.github.com/repos/octocat/Spoon-Knife/issues?per_page=2" \
--header "Accept: application/vnd.github+json"
```

The `per_page` parameter will automatically be included in the `link` header. For example:

```http
link: <https://api.github.com/repositories/1300192/issues?per_page=2&page=2>; rel="next", <https://api.github.com/repositories/1300192/issues?per_page=2&page=7715>; rel="last"
```

## Scripting with pagination

Instead of manually copying URLs from the `link` header, you can write a script to fetch multiple pages of results.

The following examples use JavaScript and GitHub's Octokit.js library. For more information about Octokit.js, see [Getting started with the REST API](https://docs.github.com/en/rest/guides/getting-started-with-the-rest-api?tool=javascript) and [the Octokit.js README](https://github.com/octokit/octokit.js/#readme).

### Example using the Octokit.js pagination method

To fetch paginated results with Octokit.js, you can use `octokit.paginate()`. `octokit.paginate()` will fetch the next page of results until it reaches the last page and then return all of the results as a single array. A few endpoints return paginated results as array in an object, as opposed to returning the paginated results as an array. `octokit.paginate()` always returns an array of items even if the raw result was an object.

For example, this script gets all of the issues from the `octocat/Spoon-Knife` repository. Although it requests 100 issues at a time, the function won't return until the last page of data is reached.

```javascript
import { Octokit } from "octokit";

const octokit = new Octokit({ });

const data = await octokit.paginate("GET /repos/{owner}/{repo}/issues", {
  owner: "octocat",
  repo: "Spoon-Knife",
  per_page: 100,
  headers: {
    "X-GitHub-Api-Version": "2022-11-28",
  },
});

console.log(data)
```

You can pass an optional map function to `octokit.paginate()` to end pagination before the last page is reached or to reduce memory usage by keeping only a subset of the response. You can also use `octokit.paginate.iterator()` to iterate through a single page at a time instead of requesting every page. For more information, see [the Octokit.js documentation](https://github.com/octokit/octokit.js#pagination).

### Example creating a pagination method

If you are using another language or library that doesn't have a pagination method, you can build your own pagination method. This example still uses the Octokit.js library to make requests, but does not rely on `octokit.paginate()`.

The `getPaginatedData` function makes a request to an endpoint with `octokit.request()`. The data from the response is processed by `parseData`, which handles cases where no data is returned or cases where the data that is returned is an object instead of an array. The processed data is then appended to a list that contains all of the paginated data collected so far. If the response includes a `link` header and if the `link` header includes a link for the next page, then the function uses a RegEx pattern (`nextPattern`) to get the URL for the next page. The function then repeats the previous steps, now using this new URL. Once the `link` header no longer includes a link to the next page, all of the results are returned.

```javascript
import { Octokit } from "octokit";

const octokit = new Octokit({ });

async function getPaginatedData(url) {
  const nextPattern = /(?<=<)([\S]*)(?=>; rel="next")/i;
  let pagesRemaining = true;
  let data = [];

  while (pagesRemaining) {
    const response = await octokit.request(`GET ${url}`, {
      per_page: 100,
      headers: {
        "X-GitHub-Api-Version":
          "2022-11-28",
      },
    });

    const parsedData = parseData(response.data)
    data = [...data, ...parsedData];

    const linkHeader = response.headers.link;

    pagesRemaining = linkHeader && linkHeader.includes(`rel=\"next\"`);

    if (pagesRemaining) {
      url = linkHeader.match(nextPattern)[0];
    }
  }

  return data;
}

function parseData(data) {
  // If the data is an array, return that
    if (Array.isArray(data)) {
      return data
    }

  // Some endpoints respond with 204 No Content instead of empty array
  //   when there is no data. In that case, return an empty array.
  if (!data) {
    return []
  }

  // Otherwise, the array of items that we want is in an object
  // Delete keys that don't include the array of items
  delete data.incomplete_results;
  delete data.repository_selection;
  delete data.total_count;
  // Pull out the array of items
  const namespaceKey = Object.keys(data)[0];
  data = data[namespaceKey];

  return data;
}

const data = await getPaginatedData("/repos/octocat/Spoon-Knife/issues");

console.log(data);
```

---

# Using the REST API to interact with checks

> You can use the REST API to build GitHub Apps that run powerful checks against code changes in a repository. You can create apps that perform continuous integration, code linting, or code scanning services and provide detailed feedback on commits.

## Overview

Rather than binary pass/fail build statuses, GitHub Apps can report rich statuses, annotate lines of code with detailed information, and re-run tests. REST API to manage checks is available exclusively to your GitHub Apps.

For an example of how to use the REST API with a GitHub App, see [Building CI checks with a GitHub App](https://docs.github.com/en/apps/creating-github-apps/guides/creating-ci-tests-with-the-checks-api).

You can use statuses with [protected branches](https://docs.github.com/en/rest/repos#branches) to prevent people from merging pull requests prematurely. For more information, see [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches#require-status-checks-before-merging).

## About check suites

When someone pushes code to a repository, GitHub creates a check suite for the last commit. A check suite is a collection of the [check runs](https://docs.github.com/en/rest/checks#check-runs) created by a single GitHub App for a specific commit. Check suites summarize the status and conclusion of the check runs that a suite includes.

The `status` can be `queued`, `in_progress`, `requested`, `waiting`, `pending`, or `completed`. Only GitHub Actions can set a status of `requested`, `waiting`, or `pending`.

If the status is `completed`, the conclusion can be any of the following:

- `action_required`
- `cancelled`
- `timed_out`
- `failure`
- `neutral`
- `skipped`
- `stale`
- `startup_failure`
- `success`

The check suite reports the highest priority check run `conclusion` in the check suite's `conclusion`. For example, if three check runs have conclusions of `timed_out`, `success`, and `neutral` the check suite conclusion will be `timed_out`.

By default, GitHub creates a check suite automatically when code is pushed to the repository. This default flow sends the `check_suite` event (with `requested` action) to all GitHub Apps that have the `checks:write` permission. When your GitHub App receives the `check_suite` event, it can create new check runs for the latest commit. GitHub automatically adds new check runs to the correct [check suite](https://docs.github.com/en/rest/checks#check-suites) based on the check run's repository and SHA.

If you don't want to use the default automatic flow, you can control when you create check suites. To change the default settings for the creation of check suites, use the [Update repository preferences for check suites](https://docs.github.com/en/rest/checks/suites#update-repository-preferences-for-check-suites) endpoint. All changes to the automatic flow settings are recorded in the audit log for the repository. If you have disabled the automatic flow, you can create a check suite using the [Create a check suite](https://docs.github.com/en/rest/checks/suites#create-a-check-suite) endpoint. You should continue to use the [Create a check run](https://docs.github.com/en/rest/checks/runs#create-a-check-run) endpoint to provide feedback on a commit.

Write permission for the REST API to interact with checks is only available to GitHub Apps. OAuth apps and authenticated users can view check runs and check suites, but they are not able to create them. If you aren't building a GitHub App, you might be interested in using the REST API to interact with [commit statuses](https://docs.github.com/en/rest/commits#commit-statuses).

To use the endpoints to manage check suites, the GitHub App must have the `checks:write` permission and can also subscribe to the [check_suite](https://docs.github.com/en/webhooks-and-events/webhooks/webhook-events-and-payloads#check_suite) webhook.

For information on how to authenticate as a GitHub App, see [About authentication with a GitHub App](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/about-authentication-with-a-github-app).

## About check runs

A check run is an individual test that is part of a check suite. Each run includes a status and conclusion.

The `status` can be `queued`, `in_progress`, `requested`, `waiting`, `pending`, or `completed`. Only GitHub Actions can set a status of `requested`, `waiting`, or `pending`.

If the status is `completed`, the conclusion can be any of the following:

- `action_required`
- `cancelled`
- `timed_out`
- `failure`
- `neutral`
- `skipped`
- `success`

If a check run is in an incomplete state for more than 14 days, then the check run's `conclusion` becomes `stale` and appears on GitHub as stale with . Only GitHub can mark check runs as `stale`. For more information about possible conclusions of a check run, see the [conclusionparameter](https://docs.github.com/en/rest/checks#create-a-check-run--parameters).

As soon as you receive the [check_suite](https://docs.github.com/en/webhooks-and-events/webhooks/webhook-events-and-payloads#check_suite) webhook, you can create the check run, even if the check is not complete. You can update the `status` of the check run as it completes with the values `queued`, `in_progress`, or `completed`, and you can update the `output` as more details become available. A check run can contain timestamps, a link to more details on your external site, detailed annotations for specific lines of code, and information about the analysis performed.

Annotations add information from your check run to specific lines of code. Each annotation includes an `annotation_level` property, which can be `notice`, `warning`, or `failure`. The annotation also includes `path`, `start_line`, and `end_line` to specify what location the annotation refers to. The annotation includes a `message` to describe the result. For more information, see [REST API endpoints for check runs](https://docs.github.com/en/rest/checks/runs).

A check can also be manually re-run in the GitHub UI. See [About status checks](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/collaborating-on-repositories-with-code-quality-features/about-status-checks#checks) for more details. When this occurs, the GitHub App that created the check run will receive the [check_run](https://docs.github.com/en/webhooks-and-events/webhooks/webhook-events-and-payloads#check_run) webhook requesting a new check run. If you create a check run without creating a check suite, GitHub creates the check suite for you automatically.

Write permission for the REST API to interact with checks is only available to GitHub Apps. OAuth apps and authenticated users can view check runs and check suites, but they are not able to create them. If you aren't building a GitHub App, you might be interested in using the REST API to interact with [commit statuses](https://docs.github.com/en/rest/commits#commit-statuses).

To use the endpoints to manage check runs, the GitHub App must have the `checks:write` permission and can also subscribe to the [check_run](https://docs.github.com/en/webhooks-and-events/webhooks/webhook-events-and-payloads#check_run) webhook.

## Check runs and requested actions

When you set up a check run with requested actions (not to be confused with GitHub Actions), you can display a button in the pull request view on GitHub that allows people to request your GitHub App to perform additional tasks.

For example, a code linting app could use requested actions to display a button in a pull request to automatically fix detected syntax errors.

To create a button that can request additional actions from your app, use the [actionsobject](https://docs.github.com/en/rest/checks/runs#create-a-check-run--parameters) when you [Create a check run](https://docs.github.com/en/rest/checks#create-a-check-run). For example, the `actions` object below displays a button in the **Checks** tab of a pull request with the label "Fix this." The button appears after the check run completes.

```json
"actions": [{
  "label": "Fix this",
  "description": "Let us fix that for you",
  "identifier": "fix_errors"
}]
```

When a user clicks the button, GitHub sends the [check_run.requested_actionwebhook](https://docs.github.com/en/webhooks-and-events/webhooks/webhook-events-and-payloads#check_run) to your app. When your app receives a `check_run.requested_action` webhook event, it can look for the `requested_action.identifier` key in the webhook payload to determine which button was clicked and perform the requested task.

For a detailed example of how to set up requested actions with the REST API, see [Building CI checks with a GitHub App](https://docs.github.com/en/apps/creating-github-apps/guides/creating-ci-tests-with-the-checks-api#part-2-creating-the-octo-rubocop-ci-test).

## Retention of checks data

GitHub retains checks data for 400 days. After 400 days, the data is archived. 10 days after archival, the data is permanently deleted.

To merge a pull request with checks that are both required and archived, you must rerun the checks.

---

# Using the REST API to interact with your Git database

> Use the REST API to read and write raw Git objects to your Git database on GitHub and to list and update your references (branch heads and tags).

## Overview

This basically allows you to reimplement a lot of Git functionality with the REST API - by creating raw objects directly into the database and updating branch references you could technically do just about anything that Git can do without having Git installed.

The REST API will return a `409 Conflict` if the Git repository is empty
or unavailable. An unavailable repository typically means GitHub is in the process of creating the repository. For an empty repository, you can use the [PUT /repos/{owner}/{repo}/contents/{path}](https://docs.github.com/en/rest/repos/contents#create-or-update-file-contents) REST API endpoint to create content and initialize the repository so you can use the API to manage the Git database. Contact us through the [GitHub Support portal](https://support.github.com) if this response status persists.

For more information on the Git object database, please read the
[Git Internals](https://git-scm.com/book/en/v2/Git-Internals-Plumbing-and-Porcelain) chapter of
the Pro Git book.

As an example, if you wanted to commit a change to a file in your
repository, you would:

- Get the current commit object
- Retrieve the tree it points to
- Retrieve the content of the blob object that tree has for that particular file path
- Change the content somehow and post a new blob object with that new content, getting a blob SHA back
- Post a new tree object with that file path pointer replaced with your new blob SHA getting a tree SHA back
- Create a new commit object with the current commit SHA as the parent and the new tree SHA, getting a commit SHA back
- Update the reference of your branch to point to the new commit SHA

It might seem complex, but it's actually pretty simple when you understand
the model and it opens up a ton of things you could potentially do with the API.

## Checking mergeability of pull requests

Warning

Please do not depend on using Git directly or [GET /repos/{owner}/{repo}/git/refs/{ref}](https://docs.github.com/en/rest/git/refs#get-a-reference) for updates to `merge` Git refs, because this content becomes outdated without warning.

A consuming API needs to explicitly request a pull request to create a *test* merge commit. A *test* merge commit is created when you view the pull request in the UI and the "Merge" button is displayed, or when you [get](https://docs.github.com/en/rest/pulls/pulls#get-a-pull-request), [create](https://docs.github.com/en/rest/pulls/pulls#create-a-pull-request), or [edit](https://docs.github.com/en/rest/pulls#update-a-pull-request) a pull request using the REST API. Without this request, the `merge` Git refs will fall out of date until the next time someone views the pull request.

If you are currently using polling methods that produce outdated `merge` Git refs, then GitHub recommends using the following steps to get the latest changes from the default branch:

1. Receive the pull request webhook.
2. Call [GET /repos/{owner}/{repo}/pulls/{pull_number}](https://docs.github.com/en/rest/pulls/pulls#get-a-pull-request) to start a background job for creating the merge commit candidate.
3. Poll your repository using [GET /repos/{owner}/{repo}/pulls/{pull_number}](https://docs.github.com/en/rest/pulls/pulls#get-a-pull-request) to see if the `mergeable` attribute is `true` or `false`. You can use Git directly or [GET /repos/{owner}/{repo}/git/refs/{ref}](https://docs.github.com/en/rest/git/refs#get-a-reference) for updates to `merge` Git refs only after performing the previous steps.

---

# Working with comments

> Using the REST API, you can access and manage comments in your pull requests, issues, or commits.

For any Pull Request, GitHub provides three kinds of comment views:
[comments on the Pull Request](https://github.com/octocat/Spoon-Knife/pull/1176#issuecomment-24114792) as a whole, [comments on a specific line](https://github.com/octocat/Spoon-Knife/pull/1176#discussion_r6252889) within the Pull Request,
and [comments on a specific commit](https://github.com/octocat/Spoon-Knife/commit/cbc28e7c8caee26febc8c013b0adfb97a4edd96e#commitcomment-4049848) within the Pull Request.

Each of these types of comments goes through a different portion of the GitHub API.
In this guide, we'll explore how you can access and manipulate each one. For every
example, we'll be using [this sample Pull Request made](https://github.com/octocat/Spoon-Knife/pull/1176) on the "octocat"
repository. As always, samples can be found in [our platform-samples repository](https://github.com/github/platform-samples/tree/master/api/ruby/working-with-comments).

## Pull Request Comments

To access comments on a Pull Request, you'll use [the endpoints to manage issues](https://docs.github.com/en/rest/issues/comments).
This may seem counterintuitive at first. But once you understand that a Pull
Request is just an Issue with code, it makes sense to use these endpoints to
create comments on a Pull Request.

We'll demonstrate fetching Pull Request comments by creating a Ruby script using
[Octokit.rb](https://github.com/octokit/octokit.rb). You'll also want to create a [personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token).

The following code should help you get started accessing comments from a Pull Request
using Octokit.rb:

```ruby
require 'octokit'

# !!! DO NOT EVER USE HARD-CODED VALUES IN A REAL APP !!!
# Instead, set and test environment variables, like below
client = Octokit::Client.new :access_token => ENV['MY_PERSONAL_TOKEN']

client.issue_comments("octocat/Spoon-Knife", 1176).each do |comment|
  username = comment[:user][:login]
  post_date = comment[:created_at]
  content = comment[:body]

  puts "#{username} made a comment on #{post_date}. It says:\n'#{content}'\n"
end
```

Here, we're specifically calling out to the API to get the comments (`issue_comments`),
providing both the repository's name (`octocat/Spoon-Knife`), and the Pull Request ID
we're interested in (`1176`). After that, it's simply a matter of iterating through
the comments to fetch information about each one.

## Pull Request Comments on a Line

Within the diff view, you can start a discussion on a particular aspect of a singular
change made within the Pull Request. These comments occur on the individual lines
within a changed file. The endpoint URL for this discussion comes from [the endpoint to manage pull request reviews](https://docs.github.com/en/rest/pulls/comments).

The following code fetches all the Pull Request comments made on files, given a single Pull Request number:

```ruby
require 'octokit'

# !!! DO NOT EVER USE HARD-CODED VALUES IN A REAL APP !!!
# Instead, set and test environment variables, like below
client = Octokit::Client.new :access_token => ENV['MY_PERSONAL_TOKEN']

client.pull_request_comments("octocat/Spoon-Knife", 1176).each do |comment|
  username = comment[:user][:login]
  post_date = comment[:created_at]
  content = comment[:body]
  path = comment[:path]
  position = comment[:position]

  puts "#{username} made a comment on #{post_date} for the file called #{path}, on line #{position}. It says:\n'#{content}'\n"
end
```

You'll notice that it's incredibly similar to the example above. The difference
between this view and the Pull Request comment is the focus of the conversation.
A comment made on a Pull Request should be reserved for discussion or ideas on
the overall direction of the code. A comment made as part of a Pull Request review should
deal specifically with the way a particular change was implemented within a file.

## Commit Comments

The last type of comments occur specifically on individual commits. For this reason,
they make use of [the endpoint to manage commit comments](https://docs.github.com/en/rest/commits#get-a-commit-comment).

To retrieve the comments on a commit, you'll want to use the SHA1 of the commit.
In other words, you won't use any identifier related to the Pull Request. Here's an example:

```ruby
require 'octokit'

# !!! DO NOT EVER USE HARD-CODED VALUES IN A REAL APP !!!
# Instead, set and test environment variables, like below
client = Octokit::Client.new :access_token => ENV['MY_PERSONAL_TOKEN']

client.commit_comments("octocat/Spoon-Knife", "cbc28e7c8caee26febc8c013b0adfb97a4edd96e").each do |comment|
  username = comment[:user][:login]
  post_date = comment[:created_at]
  content = comment[:body]

  puts "#{username} made a comment on #{post_date}. It says:\n'#{content}'\n"
end
```

Note that this API call will retrieve single line comments, as well as comments made
on the entire commit.
