# Rendering data as graphs and more

# Rendering data as graphs

> Learn how to visualize the programming languages from your repository using the D3.js library and Ruby Octokit.

In this guide, we're going to use the API to fetch information about repositories
that we own, and the programming languages that make them up. Then, we'll
visualize that information in a couple of different ways using the [D3.js](https://d3js.org/) library. To
interact with the GitHub API, we'll be using the excellent Ruby library, [Octokit](https://github.com/octokit/octokit.rb).

If you haven't already, you should read the [Basics of Authentication](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authenticating-to-the-rest-api-with-an-oauth-app)
guide before starting this example. You can find the complete source code for this project in the [platform-samples](https://github.com/github/platform-samples/tree/master/api/ruby/rendering-data-as-graphs) repository.

Let's jump right in!

## Setting up an OAuth app

First, [register a new application](https://github.com/settings/applications/new) on GitHub. Set the main and callback
URLs to `http://localhost:4567/`. As [before](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authenticating-to-the-rest-api-with-an-oauth-app), we're going to handle authentication for the API by
implementing a Rack middleware using [sinatra-auth-github](https://github.com/atmos/sinatra_auth_github):

```ruby
require 'sinatra/auth/github'

module Example
  class MyGraphApp < Sinatra::Base
    # !!! DO NOT EVER USE HARD-CODED VALUES IN A REAL APP !!!
    # Instead, set and test environment variables, like below
    # if ENV['GITHUB_CLIENT_ID'] && ENV['GITHUB_CLIENT_SECRET']
    #  CLIENT_ID        = ENV['GITHUB_CLIENT_ID']
    #  CLIENT_SECRET    = ENV['GITHUB_CLIENT_SECRET']
    # end

    CLIENT_ID = ENV['GH_GRAPH_CLIENT_ID']
    CLIENT_SECRET = ENV['GH_GRAPH_SECRET_ID']

    enable :sessions

    set :github_options, {
      :scopes    => "repo",
      :secret    => CLIENT_SECRET,
      :client_id => CLIENT_ID,
      :callback_url => "/"
    }

    register Sinatra::Auth::Github

    get '/' do
      if !authenticated?
        authenticate!
      else
        access_token = github_user["token"]
      end
    end
  end
end
```

Set up a similar *config.ru* file as in the previous example:

```ruby
ENV['RACK_ENV'] ||= 'development'
require "rubygems"
require "bundler/setup"

require File.expand_path(File.join(File.dirname(__FILE__), 'server'))

run Example::MyGraphApp
```

## Fetching repository information

This time, in order to talk to the GitHub API, we're going to use the [Octokit
Ruby library](https://github.com/octokit/octokit.rb). This is much easier than directly making a bunch of
REST calls. Plus, Octokit was developed by a GitHubber, and is actively maintained,
so you know it'll work.

Authentication with the API via Octokit is easy. Just pass your login
and token to the `Octokit::Client` constructor:

```ruby
if !authenticated?
  authenticate!
else
  octokit_client = Octokit::Client.new(:login => github_user.login, :oauth_token => github_user.token)
end
```

Let's do something interesting with the data about our repositories. We're going
to see the different programming languages they use, and count which ones are used
most often. To do that, we'll first need a list of our repositories from the API.
With Octokit, that looks like this:

```ruby
repos = client.repositories
```

Next, we'll iterate over each repository, and count the language that GitHub
associates with it:

```ruby
language_obj = {}
repos.each do |repo|
  # sometimes language can be nil
  if repo.language
    if !language_obj[repo.language]
      language_obj[repo.language] = 1
    else
      language_obj[repo.language] += 1
    end
  end
end

languages.to_s
```

When you restart your server, your web page should display something
that looks like this:

```ruby
{"JavaScript"=>13, "PHP"=>1, "Perl"=>1, "CoffeeScript"=>2, "Python"=>1, "Java"=>3, "Ruby"=>3, "Go"=>1, "C++"=>1}
```

So far, so good, but not very human-friendly. A visualization
would be great in helping us understand how these language counts are distributed. Let's feed
our counts into D3 to get a neat bar graph representing the popularity of the languages we use.

## Visualizing language counts

D3.js, or just D3, is a comprehensive library for creating many kinds of charts, graphs, and interactive visualizations.
Using D3 in detail is beyond the scope of this guide, but for a good introductory article,
check out [D3 for Mortals](http://recursion.org/d3-for-mere-mortals/).

D3 is a JavaScript library, and likes working with data as arrays. So, let's convert our Ruby hash into
a JSON array for use by JavaScript in the browser.

```ruby
languages = []
language_obj.each do |lang, count|
  languages.push :language => lang, :count => count
end

erb :lang_freq, :locals => { :languages => languages.to_json}
```

We're simply iterating over each key-value pair in our object and pushing them into
a new array. The reason we didn't do this earlier is because we didn't want to iterate
over our `language_obj` object while we were creating it.

Now, *lang_freq.erb* is going to need some JavaScript to support rendering a bar graph.
For now, you can just use the code provided here, and refer to the resources linked above
if you want to learn more about how D3 works:

```html
<!DOCTYPE html>
<meta charset="utf-8">
<html>
  <head>
    <script src="//cdnjs.cloudflare.com/ajax/libs/d3/3.0.1/d3.v3.min.js"></script>
    <style>
    svg {
      padding: 20px;
    }
    rect {
      fill: #2d578b
    }
    text {
      fill: white;
    }
    text.yAxis {
      font-size: 12px;
      font-family: Helvetica, sans-serif;
      fill: black;
    }
    </style>
  </head>
  <body>
    <p>Check this sweet data out:</p>
    <div id="lang_freq"></div>

  </body>
  <script>
    var data = <%= languages %>;

    var barWidth = 40;
    var width = (barWidth + 10) * data.length;
    var height = 300;

    var x = d3.scale.linear().domain([0, data.length]).range([0, width]);
    var y = d3.scale.linear().domain([0, d3.max(data, function(datum) { return datum.count; })]).
      rangeRound([0, height]);

    // add the canvas to the DOM
    var languageBars = d3.select("#lang_freq").
      append("svg:svg").
      attr("width", width).
      attr("height", height);

    languageBars.selectAll("rect").
      data(data).
      enter().
      append("svg:rect").
      attr("x", function(datum, index) { return x(index); }).
      attr("y", function(datum) { return height - y(datum.count); }).
      attr("height", function(datum) { return y(datum.count); }).
      attr("width", barWidth);

    languageBars.selectAll("text").
      data(data).
      enter().
      append("svg:text").
      attr("x", function(datum, index) { return x(index) + barWidth; }).
      attr("y", function(datum) { return height - y(datum.count); }).
      attr("dx", -barWidth/2).
      attr("dy", "1.2em").
      attr("text-anchor", "middle").
      text(function(datum) { return datum.count;});

    languageBars.selectAll("text.yAxis").
      data(data).
      enter().append("svg:text").
      attr("x", function(datum, index) { return x(index) + barWidth; }).
      attr("y", height).
      attr("dx", -barWidth/2).
      attr("text-anchor", "middle").
      text(function(datum) { return datum.language;}).
      attr("transform", "translate(0, 18)").
      attr("class", "yAxis");
  </script>
</html>
```

Phew! Again, don't worry about what most of this code is doing. The relevant part
here is a line way at the top--`var data = <%= languages %>;`--which indicates
that we're passing our previously created `languages` array into ERB for manipulation.

As the "D3 for Mortals" guide suggests, this isn't necessarily the best use of
D3. But it does serve to illustrate how you can use the library, along with Octokit,
to make some really amazing things.

## Combining different API calls

Now it's time for a confession: the `language` attribute within repositories
only identifies the "primary" language defined. That means that if you have
a repository that combines several languages, the one with the most bytes of code
is considered to be the primary language.

Let's combine a few API calls to get a *true* representation of which language
has the greatest number of bytes written across all our code. A [treemap](https://www.d3-graph-gallery.com/treemap.html)
should be a great way to visualize the sizes of our coding languages used, rather
than simply the count. We'll need to construct an array of objects that looks
something like this:

```json
[ { "name": "language1", "size": 100},
  { "name": "language2", "size": 23}
  ...
]
```

Since we already have a list of repositories above, let's inspect each one, and
call the [GET /repos/{owner}/{repo}/languages endpoint](https://docs.github.com/en/rest/repos/repos#list-repository-languages):

```ruby
repos.each do |repo|
  repo_name = repo.name
  repo_langs = octokit_client.languages("#{github_user.login}/#{repo_name}")
end
```

From there, we'll cumulatively add each language found to a list of languages:

```ruby
repo_langs.each do |lang, count|
  if !language_obj[lang]
    language_obj[lang] = count
  else
    language_obj[lang] += count
  end
end
```

After that, we'll format the contents into a structure that D3 understands:

```ruby
language_obj.each do |lang, count|
  language_byte_count.push :name => "#{lang} (#{count})", :count => count
end

# some mandatory formatting for D3
language_bytes = [ :name => "language_bytes", :elements => language_byte_count]
```

(For more information on D3 tree map magic, check out [this simple tutorial](https://docs.github.com/en/rest/repos/repos#list-repository-languages).)

To wrap up, we pass this JSON information over to the same ERB template:

```ruby
erb :lang_freq, :locals => { :languages => languages.to_json, :language_byte_count => language_bytes.to_json}
```

Like before, here's a bunch of JavaScript that you can drop
directly into your template:

```html
<div id="byte_freq"></div>
<script>
  var language_bytes = <%= language_byte_count %>
  var childrenFunction = function(d){return d.elements};
  var sizeFunction = function(d){return d.count;};
  var colorFunction = function(d){return Math.floor(Math.random()*20)};
  var nameFunction = function(d){return d.name;};

  var color = d3.scale.linear()
              .domain([0,10,15,20])
              .range(["grey","green","yellow","red"]);

  drawTreemap(5000, 2000, '#byte_freq', language_bytes, childrenFunction, nameFunction, sizeFunction, colorFunction, color);

  function drawTreemap(height,width,elementSelector,language_bytes,childrenFunction,nameFunction,sizeFunction,colorFunction,colorScale){

      var treemap = d3.layout.treemap()
          .children(childrenFunction)
          .size([width,height])
          .value(sizeFunction);

      var div = d3.select(elementSelector)
          .append("div")
          .style("position","relative")
          .style("width",width + "px")
          .style("height",height + "px");

      div.data(language_bytes).selectAll("div")
          .data(function(d){return treemap.nodes(d);})
          .enter()
          .append("div")
          .attr("class","cell")
          .style("background",function(d){ return colorScale(colorFunction(d));})
          .call(cell)
          .text(nameFunction);
  }

  function cell(){
      this
          .style("left",function(d){return d.x + "px";})
          .style("top",function(d){return d.y + "px";})
          .style("width",function(d){return d.dx - 1 + "px";})
          .style("height",function(d){return d.dy - 1 + "px";});
  }
</script>
```

Et voila! Beautiful rectangles containing your repo languages, with relative
proportions that are easy to see at a glance. You might need to
tweak the height and width of your treemap, passed as the first two
arguments to `drawTreemap` above, to get all the information to show up properly.

---

# Scripting with the REST API and JavaScript

> Write a script using the Octokit.js SDK to interact with the REST API.

## About Octokit.js

If you want to write a script using JavaScript to interact with GitHub's REST API, GitHub recommends that you use the Octokit.js SDK. Octokit.js is maintained by GitHub. The SDK implements best practices and makes it easier for you to interact with the REST API via JavaScript. Octokit.js works with all modern browsers, Node.js, and Deno. For more information about Octokit.js, see [the Octokit.js README](https://github.com/octokit/octokit.js/#readme).

## Prerequisites

This guide assumes that you are familiar with JavaScript and the GitHub REST API. For more information about the REST API, see [Getting started with the REST API](https://docs.github.com/en/rest/guides/getting-started-with-the-rest-api).

You must install and import `octokit` in order to use the Octokit.js library. This guide uses import statements in accordance with ES6. For more information about different installation and import methods, see [the Octokit.js README's Usage section](https://github.com/octokit/octokit.js/#usage).

## Instantiating and authenticating

Warning

Treat your authentication credentials like a password.

To keep your credentials secure, you can store your credentials as a secret and run your script through GitHub Actions. For more information, see [Using secrets in GitHub Actions](https://docs.github.com/en/actions/security-guides/encrypted-secrets).

> You can also store your credentials as a Codespaces secret and run your script in Codespaces. For more information, see [Managing your account-specific secrets for GitHub Codespaces](https://docs.github.com/en/codespaces/managing-your-codespaces/managing-encrypted-secrets-for-your-codespaces).

> If these options are not possible, consider using another CLI service to store your credentials securely.

### Authenticating with a personal access token

If you want to use the GitHub REST API for personal use, you can create a personal access token. For more information about creating a personal access token, see [Managing your personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token).

First, import `Octokit` from `octokit`. Then, pass your personal access token when you create an instance of `Octokit`. In the following example, replace `YOUR-TOKEN` with a reference to your personal access token.

```javascript
import { Octokit } from "octokit";

const octokit = new Octokit({
  auth: 'YOUR-TOKEN',
});
```

### Authenticating with a GitHub App

If you want to use the API on behalf of an organization or another user, GitHub recommends that you use a GitHub App. If an endpoint is available to GitHub Apps, the REST reference documentation for that endpoint will indicate what type of GitHub App token is required. For more information, see [Registering a GitHub App](https://docs.github.com/en/apps/creating-github-apps/setting-up-a-github-app/creating-a-github-app) and [About authentication with a GitHub App](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/about-authentication-with-a-github-app).

Instead of importing `Octokit` from `octokit`, import `App`. In the following example, replace `APP_ID` with a reference to your app's ID. Replace `PRIVATE_KEY` with a reference to your app's private key. Replace `INSTALLATION_ID` with the ID of the installation of your app that you want to authenticate on behalf of. You can find your app's ID and generate a private key on the settings page for your app. For more information, see [Managing private keys for GitHub Apps](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/managing-private-keys-for-github-apps). You can get an installation ID with the `GET /users/{username}/installation`, `GET /repos/{owner}/{repo}/installation`, or `GET /orgs/{org}/installation` endpoints. For more information, see [REST API endpoints for GitHub Apps](https://docs.github.com/en/rest/apps/apps).

```javascript
import { App } from "octokit";

const app = new App({
  appId: APP_ID,
  privateKey: PRIVATE_KEY,
});

const octokit = await app.getInstallationOctokit(INSTALLATION_ID);
```

### Authenticating in GitHub Actions

If you want to use the API in a GitHub Actions workflow, GitHub recommends that you authenticate with the built-in `GITHUB_TOKEN` instead of creating a token. You can grant permissions to the `GITHUB_TOKEN` with the `permissions` key. For more information about `GITHUB_TOKEN`, see [Use GITHUB_TOKEN for authentication in workflows](https://docs.github.com/en/actions/security-guides/automatic-token-authentication#permissions-for-the-github_token).

If your workflow needs to access resources outside of the workflow's repository, then you will not be able to use `GITHUB_TOKEN`. In that case, store your credentials as a secret and replace `GITHUB_TOKEN` in the examples below with the name of your secret. For more information about secrets, see [Using secrets in GitHub Actions](https://docs.github.com/en/actions/security-guides/encrypted-secrets).

If you use the `run` keyword to execute your JavaScript script in your GitHub Actions workflows, you can store the value of `GITHUB_TOKEN` as an environment variable. Your script can access the environment variable as `process.env.VARIABLE_NAME`.

For example, this workflow step stores `GITHUB_TOKEN` in an environment variable called `TOKEN`:

```yaml
- name: Run script
  env:
    TOKEN: ${{ secrets.GITHUB_TOKEN }}
  run: |
    node .github/actions-scripts/use-the-api.mjs
```

The script that the workflow runs uses `process.env.TOKEN` to authenticate:

```javascript
import { Octokit } from "octokit";

const octokit = new Octokit({
  auth: process.env.TOKEN,
});
```

### Instantiating without authentication

You can use the REST API without authentication, although you will have a lower rate limit and will not be able to use some endpoints. To create an instance of `Octokit` without authenticating, do not pass the `auth` argument.

```javascript
import { Octokit } from "octokit";

const octokit = new Octokit({ });
```

## Making requests

Octokit supports multiple ways of making requests. You can use the `request` method to make requests if you know the HTTP verb and path for the endpoint. You can use the `rest` method if you want to take advantage of autocompletion in your IDE and typing. For paginated endpoints, you can use the `paginate` method to request multiple pages of data.

### Using therequestmethod to make requests

To use the `request` method to make requests, pass the HTTP method and path as the first argument. Pass any body, query, or path parameters in an object as the second argument. For example, to make a `GET` request to `/repos/{owner}/{repo}/issues` and pass the `owner`, `repo`, and `per_page` parameters:

```javascript
await octokit.request("GET /repos/{owner}/{repo}/issues", {
  owner: "github",
  repo: "docs",
  per_page: 2
});
```

The `request` method automatically passes the `Accept: application/vnd.github+json` header. To pass additional headers or a different `Accept` header, add a `headers` property to the object that is passed as a second argument. The value of the `headers` property is an object with the header names as keys and header values as values. For example, to send a `content-type` header with a value of `text/plain` and a `x-github-api-version` header with a value of `2022-11-28`:

```javascript
await octokit.request("POST /markdown/raw", {
  text: "Hello **world**",
  headers: {
    "content-type": "text/plain",
    "x-github-api-version": "2022-11-28",
  },
});
```

### Usingrestendpoint methods to make requests

Every REST API endpoint has an associated `rest` endpoint method in Octokit. These methods generally autocomplete in your IDE for convenience. You can pass any parameters as an object to the method.

```javascript
await octokit.rest.issues.listForRepo({
  owner: "github",
  repo: "docs",
  per_page: 2
});
```

Additionally, if you are using a typed language such as TypeScript, you can import types to use with these methods. For more information, see [the TypeScript section in the plugin-rest-endpoint-methods.js README](https://github.com/octokit/plugin-rest-endpoint-methods.js/#typescript).

### Making paginated requests

If the endpoint is paginated and you want to fetch more than one page of results, you can use the `paginate` method. `paginate` will fetch the next page of results until it reaches the last page and then return all of the results as a single array. A few endpoints return paginated results as array in an object, as opposed to returning the paginated results as an array. `paginate` always returns an array of items even if the raw result was an object.

For example, the following example gets all of the issues from the `github/docs` repository. Although it requests 100 issues at a time, the function won't return until the last page of data is reached.

```javascript
const issueData = await octokit.paginate("GET /repos/{owner}/{repo}/issues", {
  owner: "github",
  repo: "docs",
  per_page: 100,
  headers: {
    "x-github-api-version": "2022-11-28",
  },
});
```

The `paginate` method accepts an optional map function, which you can use to collect only the data that you want from the response. This reduces memory usage by your script. The map function can take a second argument, `done`, which you can call to end the pagination before the last page is reached. This lets you fetch a subset of pages. For example, the following example continues to fetch results until an issue that includes "test" in the title is returned. For the pages of data that were returned, only the issue title and author are stored.

```javascript
const issueData = await octokit.paginate("GET /repos/{owner}/{repo}/issues", {
  owner: "github",
  repo: "docs",
  per_page: 100,
  headers: {
    "x-github-api-version": "2022-11-28",
  },
},
    (response, done) => response.data.map((issue) => {
    if (issue.title.includes("test")) {
      done()
    }
    return ({title: issue.title, author: issue.user.login})
  })
);
```

Instead of fetching all of the results at once, you can use `octokit.paginate.iterator()` to iterate through a single page at a time. For example, the following example fetches one page of results at a time and processes each object from the page before fetching the next page. Once an issue that includes "test" in the title is reached, the script stops the iteration and returns the issue title and issue author of each object that was processed. The iterator is the most memory efficient method for fetching paginated data.

```javascript
const iterator = octokit.paginate.iterator("GET /repos/{owner}/{repo}/issues", {
  owner: "github",
  repo: "docs",
  per_page: 100,
  headers: {
    "x-github-api-version": "2022-11-28",
  },
});

let issueData = []
let breakLoop = false
for await (const {data} of iterator) {
  if (breakLoop) break
  for (const issue of data) {
    if (issue.title.includes("test")) {
      breakLoop = true
      break
    } else {
      issueData = [...issueData, {title: issue.title, author: issue.user.login}];
    }
  }
}
```

You can use the `paginate` method with the `rest` endpoint methods as well. Pass the `rest` endpoint method as the first argument. Pass any parameters as the second argument.

```javascript
const iterator = octokit.paginate.iterator(octokit.rest.issues.listForRepo, {
  owner: "github",
  repo: "docs",
  per_page: 100,
  headers: {
    "x-github-api-version": "2022-11-28",
  },
});
```

For more information about pagination, see [Using pagination in the REST API](https://docs.github.com/en/rest/guides/using-pagination-in-the-rest-api).

## Catching errors

### Catching all errors

Sometimes, the GitHub REST API will return an error. For example, you will get an error if your access token is expired or if you omitted a required parameter. Octokit.js automatically retries the request when it gets an error other than `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`, and `422 Unprocessable Entity`. If an API error occurs even after retries, Octokit.js throws an error that includes the HTTP status code of the response (`response.status`) and the response headers (`response.headers`). You should handle these errors in your code. For example, you can use a try/catch block to catch errors:

```javascript
let filesChanged = []

try {
  const iterator = octokit.paginate.iterator("GET /repos/{owner}/{repo}/pulls/{pull_number}/files", {
    owner: "github",
    repo: "docs",
    pull_number: 22809,
    per_page: 100,
    headers: {
      "x-github-api-version": "2022-11-28",
    },
  });

  for await (const {data} of iterator) {
    filesChanged = [...filesChanged, ...data.map(fileData => fileData.filename)];
  }
} catch (error) {
  if (error.response) {
    console.error(`Error! Status: ${error.response.status}. Message: ${error.response.data.message}`)
  }
  console.error(error)
}
```

### Handling intended error codes

Sometimes, GitHub uses a 4xx status code to indicate a non-error response. If the endpoint you are using does this, you can add additional handling for specific errors. For example, the `GET /user/starred/{owner}/{repo}` endpoint will return a `404` if the repository is not starred. The following example uses the `404` response to indicate that the repository was not starred; all other errors codes are treated as errors.

```javascript
try {
  await octokit.request("GET /user/starred/{owner}/{repo}", {
    owner: "github",
    repo: "docs",
    headers: {
      "x-github-api-version": "2022-11-28",
    },
  });

  console.log(`The repository is starred by me`);

} catch (error) {
  if (error.status === 404) {
    console.log(`The repository is not starred by me`);
  } else {
    console.error(`An error occurred while checking if the repository is starred: ${error?.response?.data?.message}`);
  }
}
```

### Handling rate limit errors

If you receive a rate limit error, you may want to retry your request after waiting. When you are rate limited, GitHub responds with a `403 Forbidden` error and the `x-ratelimit-remaining` response header value will be `"0"`. The response headers will include a `x-ratelimit-reset` header, which tells you the time at which the current rate limit window resets, in UTC epoch seconds. You can retry your request after the time specified by `x-ratelimit-reset`.

```javascript
async function requestRetry(route, parameters) {
  try {
    const response = await octokit.request(route, parameters);
    return response
  } catch (error) {
    if (error.response && error.status === 403 && error.response.headers['x-ratelimit-remaining'] === '0') {
      const resetTimeEpochSeconds = error.response.headers['x-ratelimit-reset'];
      const currentTimeEpochSeconds = Math.floor(Date.now() / 1000);
      const secondsToWait = resetTimeEpochSeconds - currentTimeEpochSeconds;
      console.log(`You have exceeded your rate limit. Retrying in ${secondsToWait} seconds.`);
      setTimeout(requestRetry, secondsToWait * 1000, route, parameters);
    } else {
      console.error(error);
    }
  }
}

const response = await requestRetry("GET /repos/{owner}/{repo}/issues", {
    owner: "github",
    repo: "docs",
    per_page: 2
  })
```

## Using the response

The `request` method returns a promise that resolves to an object if the request was successful. The object properties are `data` (the response body returned by the endpoint), `status` (the HTTP response code), `url` (the URL of the request), and `headers` (an object containing the response headers). Unless otherwise specified, the response body is in JSON format. Some endpoints do not return a response body; in those cases, the `data` property is omitted.

```javascript
const response = await octokit.request("GET /repos/{owner}/{repo}/issues/{issue_number}", {
  owner: "github",
  repo: "docs",
  issue_number: 11901,
  headers: {
    "x-github-api-version": "2022-11-28",
  },
});

console.log(`The status of the response is: ${response.status}`)
console.log(`The request URL was: ${response.url}`)
console.log(`The x-ratelimit-remaining response header is: ${response.headers["x-ratelimit-remaining"]}`)
console.log(`The issue title is: ${response.data.title}`)
```

Similarly, the `paginate` method returns a promise. If the request was successful, the promise resolves to an array of data returned by the endpoint. Unlike the `request` method, the `paginate` method does not return the status code, URL, or headers.

```javascript
const data = await octokit.paginate("GET /repos/{owner}/{repo}/issues", {
  owner: "github",
  repo: "docs",
  per_page: 100,
  headers: {
    "x-github-api-version": "2022-11-28",
  },
});

console.log(`${data.length} issues were returned`)
console.log(`The title of the first issue is: ${data[0].title}`)
```

## Example script

Here is a full example script that uses Octokit.js. The script imports `Octokit` and creates a new instance of `Octokit`. If you wanted to authenticate with a GitHub App instead of a personal access token, you would import and instantiate `App` instead of `Octokit`. For more information, see [Authenticating with a GitHub App](#authenticating-with-a-github-app).

The `getChangedFiles` function gets all of the files changed for a pull request. The `commentIfDataFilesChanged` function calls the `getChangedFiles` function. If any of the files that the pull request changed include `/data/` in the file path, then the function will comment on the pull request.

```javascript
import { Octokit } from "octokit";

const octokit = new Octokit({
  auth: 'YOUR-TOKEN',
});

async function getChangedFiles({owner, repo, pullNumber}) {
  let filesChanged = []

  try {
    const iterator = octokit.paginate.iterator("GET /repos/{owner}/{repo}/pulls/{pull_number}/files", {
      owner: owner,
      repo: repo,
      pull_number: pullNumber,
      per_page: 100,
      headers: {
        "x-github-api-version": "2022-11-28",
      },
    });

    for await (const {data} of iterator) {
      filesChanged = [...filesChanged, ...data.map(fileData => fileData.filename)];
    }
  } catch (error) {
    if (error.response) {
      console.error(`Error! Status: ${error.response.status}. Message: ${error.response.data.message}`)
    }
    console.error(error)
  }

  return filesChanged
}

async function commentIfDataFilesChanged({owner, repo, pullNumber}) {
  const changedFiles = await getChangedFiles({owner, repo, pullNumber});

  const filePathRegex = new RegExp(/\/data\//, "i");
  if (!changedFiles.some(fileName => filePathRegex.test(fileName))) {
    return;
  }

  try {
    const {data: comment} = await octokit.request("POST /repos/{owner}/{repo}/issues/{issue_number}/comments", {
      owner: owner,
      repo: repo,
      issue_number: pullNumber,
      body: `It looks like you changed a data file. These files are auto-generated. \n\nYou must revert any changes to data files before your pull request will be reviewed.`,
      headers: {
        "x-github-api-version": "2022-11-28",
      },
    });

    return comment.html_url;
  } catch (error) {
    if (error.response) {
      console.error(`Error! Status: ${error.response.status}. Message: ${error.response.data.message}`)
    }
    console.error(error)
  }
}

await commentIfDataFilesChanged({owner: "github", repo: "docs", pullNumber: 191});
```

## Next steps

- To learn more about Octokit.js see [the Octokit.js documentation](https://github.com/octokit/octokit.js/#readme).
- For some real life examples, look at how GitHub Docs uses Octokit.js by [searching the GitHub Docs repository](https://github.com/search?q=repo%3Agithub%2Fdocs%20path%3A.github%20octokit&type=code).
