# Best practices for using the REST API and more

# Best practices for using the REST API

> Follow these best practices when using GitHub's API.

## Avoid polling

You should subscribe to webhook events instead of polling the API for data. This will help your integration stay within the API rate limit. For more information, see [Webhooks documentation](https://docs.github.com/en/webhooks).

## Make authenticated requests

Authenticated requests have a higher primary rate limit than unauthenticated requests. To avoid exceeding the rate limit, you should make authenticated requests. For more information, see [Rate limits for the REST API](https://docs.github.com/en/rest/overview/rate-limits-for-the-rest-api).

## Avoid concurrent requests

To avoid exceeding secondary rate limits, you should make requests serially instead of concurrently. To achieve this, you can implement a queue system for requests.

## Pause between mutative requests

If you are making a large number of `POST`, `PATCH`, `PUT`, or `DELETE` requests, wait at least one second between each request. This will help you avoid secondary rate limits.

## Handle rate limit errors appropriately

If you receive a rate limit error, you should stop making requests temporarily according to these guidelines:

- If the `retry-after` response header is present, you should not retry your request until after that many seconds has elapsed.
- If the `x-ratelimit-remaining` header is `0`, you should not make another request until after the time specified by the `x-ratelimit-reset` header. The `x-ratelimit-reset` header is in UTC epoch seconds.
- Otherwise, wait for at least one minute before retrying. If your request continues to fail due to a secondary rate limit, wait for an exponentially increasing amount of time between retries, and throw an error after a specific number of retries.

Continuing to make requests while you are rate limited may result in the banning of your integration.

## Follow redirects

The GitHub REST API uses HTTP redirection where appropriate. You should assume that any
request may result in a redirection. Receiving an HTTP redirection is not an error, and you should follow the redirect.

A `301` status code indicates permanent redirection. You should repeat your request to the URL specified by the `location` header. Additionally, you should update your code to use this URL for future requests.

A `302` or `307` status code indicates temporary redirection. You should repeat your request to the URL specified by the `location` header. However, you should not update your code to use this URL for future requests.

Other redirection status codes may be used in accordance with HTTP specifications.

## Do not manually parse URLs

Many API endpoints return URL values for fields in the response body. You should not try to parse these URLs or to predict the structure of future URLs. This can cause your integration to break if GitHub changes the structure of the URL in the future. Instead, you should look for a field that contains the information that you need. For example, the endpoint to create an issue returns an `html_url` field with a value like `https://github.com/octocat/Hello-World/issues/1347` and a `number` field with a value like `1347`. If you need to know the number of the issue, use the `number` field instead of parsing the `html_url` field.

Similarly, you should not try to manually construct pagination queries. Instead, you should use the link headers to determine what pages of results you can request. For more information, see [Using pagination in the REST API](https://docs.github.com/en/rest/guides/using-pagination-in-the-rest-api).

## Use conditional requests if appropriate

Most endpoints return an `etag` header, and many endpoints return a `last-modified` header. You can use the values of these headers to make conditional `GET` requests. If the response has not changed, you will receive a `304 Not Modified` response. Making a conditional request does not count against your primary rate limit if a `304` response is returned and the request was made while correctly authorized with an `Authorization` header.

For example, if a previous request returned an `etag` header value of `644b5b0155e6404a9cc4bd9d8b1ae730`, you can use the `if-none-match` header in a future request:

```shell
curl -H "Authorization: Bearer YOUR-TOKEN" https://api.github.com/meta --include --header 'if-none-match: "644b5b0155e6404a9cc4bd9d8b1ae730"'
```

For example, if a previous request returned a `last-modified` header value of `Wed, 25 Oct 2023 19:17:59 GMT`, you can use the `if-modified-since` header in a future request:

```shell
curl -H "Authorization: Bearer YOUR-TOKEN" https://api.github.com/repos/github/docs --include --header 'if-modified-since: Wed, 25 Oct 2023 19:17:59 GMT'
```

Conditional requests for unsafe methods, such as `POST`, `PUT`, `PATCH`, and `DELETE` are not supported unless otherwise noted in the documentation for a specific endpoint.

## Do not ignore errors

You should not ignore repeated `4xx` and `5xx` error codes. Instead, you should ensure that you are correctly interacting with the API. For example, if an endpoint requests a string and you are passing it a numeric value, you will receive a validation error. Similarly, attempting to access an unauthorized or nonexistent endpoint will result in a `4xx` error.

Intentionally ignoring repeated validation errors may result in the suspension of your app for abuse.

## Further reading

- [Best practices for using webhooks](https://docs.github.com/en/webhooks/using-webhooks/best-practices-for-using-webhooks)
- [Best practices for creating a GitHub App](https://docs.github.com/en/apps/creating-github-apps/about-creating-github-apps/best-practices-for-creating-a-github-app)

---

# Building a CI server

> Build your own CI system using the Status API.

You can use the REST API to tie together commits with
a testing service, so that every push you make can be tested and represented
in a GitHub pull request. For more information about the relevant endpoints, see [REST API endpoints for commit statuses](https://docs.github.com/en/rest/commits/statuses).

This guide will use that API to demonstrate a setup that you can use.
In our scenario, we will:

- Run our CI suite when a Pull Request is opened (we'll set the CI status to pending).
- When the CI is finished, we'll set the Pull Request's status accordingly.

Our CI system and host server will be figments of our imagination. They could be
Travis, Jenkins, or something else entirely. The crux of this guide will be setting up
and configuring the server managing the communication.

If you haven't already, [downloadngrok](https://ngrok.com/), and learn how
to [use it](https://docs.github.com/en/webhooks-and-events/webhooks/configuring-your-server-to-receive-payloads#using-ngrok). We find it to be a very useful tool for exposing local
applications to the internet.

Note

Alternatively, you can use webhook forwarding to set up your local environment to receive webhooks. For more information, see [Using the GitHub CLI to forward webhooks for testing](https://docs.github.com/en/webhooks-and-events/webhooks/receiving-webhooks-with-the-github-cli).

Note: you can download the complete source code for this project
[from the platform-samples repo](https://github.com/github/platform-samples/tree/master/api/ruby/building-a-ci-server).

## Writing your server

We'll write a quick Sinatra app to prove that our local connections are working.
Let's start with this:

```ruby
require 'sinatra'
require 'json'

post '/event_handler' do
  payload = JSON.parse(params[:payload])
  "Well, it worked!"
end
```

(If you're unfamiliar with how Sinatra works, we recommend [reading the Sinatra guide](http://www.sinatrarb.com/).)

Start this server up. By default, Sinatra starts on port `4567`, so you'll want
to configure `ngrok` to start listening for that, too.

In order for this server to work, we'll need to set a repository up with a webhook. The webhook should be configured to fire whenever a pull request is created, or merged.

Go ahead and create a repository you're comfortable playing around in. Might we suggest [@octocat's Spoon/Knife repository](https://github.com/octocat/Spoon-Knife)?

After that, you'll create a new webhook in your repository, feeding it the URL that `ngrok` gave you, and choosing `application/x-www-form-urlencoded` as the content type.

Click **Update webhook**. You should see a body response of `Well, it worked!`.
Great! Click on **Let me select individual events**, and select the following:

- Status
- Pull Request

These are the events GitHub will send to our server whenever the relevant action
occurs. Let's update our server to *just* handle the Pull Request scenario right now:

```ruby
post '/event_handler' do
  @payload = JSON.parse(params[:payload])

  case request.env['HTTP_X_GITHUB_EVENT']
  when "pull_request"
    if @payload["action"] == "opened"
      process_pull_request(@payload["pull_request"])
    end
  end
end

helpers do
  def process_pull_request(pull_request)
    puts "It's #{pull_request['title']}"
  end
end
```

What's going on? Every event that GitHub sends out attached a `X-GitHub-Event`
HTTP header. We'll only care about the PR events for now. From there, we'll
take the payload of information, and return the title field. In an ideal scenario,
our server would be concerned with every time a pull request is updated, not just
when it's opened. That would make sure that every new push passes the CI tests.
But for this demo, we'll just worry about when it's opened.

To test out this proof-of-concept, make some changes in a branch in your test
repository, and open a pull request. Your server should respond accordingly!

## Working with statuses

With our server in place, we're ready to start our first requirement, which is
setting (and updating) CI statuses. Note that at any time you update your server,
you can click **Redeliver** to send the same payload. There's no need to make a
new pull request every time you make a change!

Since we're interacting with the GitHub API, we'll use [Octokit.rb](https://github.com/octokit/octokit.rb)
to manage our interactions. We'll configure that client with
[a personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token):

```ruby
# !!! DO NOT EVER USE HARD-CODED VALUES IN A REAL APP !!!
# Instead, set and test environment variables, like below
ACCESS_TOKEN = ENV['MY_PERSONAL_TOKEN']

before do
  @client ||= Octokit::Client.new(:access_token => ACCESS_TOKEN)
end
```

After that, we'll just need to update the pull request on GitHub to make clear
that we're processing on the CI:

```ruby
def process_pull_request(pull_request)
  puts "Processing pull request..."
  @client.create_status(pull_request['base']['repo']['full_name'], pull_request['head']['sha'], 'pending')
end
```

We're doing three very basic things here:

- We're looking up the full name of the repository
- We're looking up the last SHA of the pull request
- We're setting the status to "pending"

That's it! From here, you can run whatever process you need to in order to execute
your test suite. Maybe you're going to pass off your code to Jenkins, or call
on another web service via its API, like [Travis](https://api.travis-ci.com/docs/). After that, you'd
be sure to update the status once more. In our example, we'll just set it to `"success"`:

```ruby
def process_pull_request(pull_request)
  @client.create_status(pull_request['base']['repo']['full_name'], pull_request['head']['sha'], 'pending')
  sleep 2 # do busy work...
  @client.create_status(pull_request['base']['repo']['full_name'], pull_request['head']['sha'], 'success')
  puts "Pull request processed!"
end
```

## Conclusion

At GitHub, we've used a version of [Janky](https://github.com/github/janky) to manage our CI for years.
The basic flow is essentially the exact same as the server we've built above.
At GitHub, we:

- Fire to Jenkins when a pull request is created or updated (via Janky)
- Wait for a response on the state of the CI
- If the code is green, we merge the pull request

All of this communication is funneled back to our chat rooms. You don't need to
build your own CI setup to use this example.
You can always rely on [GitHub integrations](https://github.com/integrations).

---

# Delivering deployments

> Using the Deployments REST API, you can build custom tooling that interacts with your server and a third-party app.

You can use the REST API to deploy your projects hosted on GitHub on a server that you own. For more information about the endpoints to manage deployments and statuses, see [REST API endpoints for deployments](https://docs.github.com/en/rest/deployments). You can also use the REST API to coordinate your deployments the moment your code lands on the default branch. For more information, see [Building a CI server](https://docs.github.com/en/rest/guides/building-a-ci-server).

This guide will use the REST API to demonstrate a setup that you can use.
In our scenario, we will:

- Merge a pull request.
- When the CI is finished, we'll set the pull request's status accordingly.
- When the pull request is merged, we'll run our deployment to our server.

Our CI system and host server will be figments of our imagination. They could be
Heroku, Amazon, or something else entirely. The crux of this guide will be setting up
and configuring the server managing the communication.

If you haven't already, be sure to [downloadngrok](https://ngrok.com/), and learn how
to [use it](https://docs.github.com/en/webhooks-and-events/webhooks/configuring-your-server-to-receive-payloads#using-ngrok). We find it to be a very useful tool for exposing local
applications to the internet.

Note

Alternatively, you can use webhook forwarding to set up your local environment to receive webhooks. For more information, see [Using the GitHub CLI to forward webhooks for testing](https://docs.github.com/en/webhooks-and-events/webhooks/receiving-webhooks-with-the-github-cli).

Note: you can download the complete source code for this project
[from the platform-samples repo](https://github.com/github/platform-samples/tree/master/api/ruby/delivering-deployments).

## Writing your server

We'll write a quick Sinatra app to prove that our local connections are working.
Let's start with this:

```ruby
require 'sinatra'
require 'json'

post '/event_handler' do
  payload = JSON.parse(params[:payload])
  "Well, it worked!"
end
```

(If you're unfamiliar with how Sinatra works, we recommend [reading the Sinatra guide](http://www.sinatrarb.com/).)

Start this server up. By default, Sinatra starts on port `4567`, so you'll want
to configure `ngrok` to start listening for that, too.

In order for this server to work, we'll need to set a repository up with a webhook. The webhook should be configured to fire whenever a pull request is created, or merged.

Go ahead and create a repository you're comfortable playing around in. Might we
suggest [@octocat's Spoon/Knife repository](https://github.com/octocat/Spoon-Knife)?

After that, you'll create a new webhook in your repository, feeding it the URL that `ngrok` gave you, and choosing `application/x-www-form-urlencoded` as the content type.

Click **Update webhook**. You should see a body response of `Well, it worked!`.
Great! Click on **Let me select individual events.**, and select the following:

- Deployment
- Deployment status
- Pull Request

These are the events GitHub will send to our server whenever the relevant action
occurs. We'll configure our server to *just* handle when pull requests are merged
right now:

```ruby
post '/event_handler' do
  @payload = JSON.parse(params[:payload])

  case request.env['HTTP_X_GITHUB_EVENT']
  when "pull_request"
    if @payload["action"] == "closed" && @payload["pull_request"]["merged"]
      puts "A pull request was merged! A deployment should start now..."
    end
  end
end
```

What's going on? Every event that GitHub sends out attached a `X-GitHub-Event`
HTTP header. We'll only care about the PR events for now. When a pull request is
merged (its state is `closed`, and `merged` is `true`), we'll kick off a deployment.

To test out this proof-of-concept, make some changes in a branch in your test
repository, open a pull request, and merge it. Your server should respond accordingly!

## Working with deployments

With our server in place, the code being reviewed, and our pull request
merged, we want our project to be deployed.

We'll start by modifying our event listener to process pull requests when they're
merged, and start paying attention to deployments:

```ruby
when "pull_request"
  if @payload["action"] == "closed" && @payload["pull_request"]["merged"]
    start_deployment(@payload["pull_request"])
  end
when "deployment"
  process_deployment(@payload)
when "deployment_status"
  update_deployment_status
end
```

Based on the information from the pull request, we'll start by filling out the
`start_deployment` method:

```ruby
def start_deployment(pull_request)
  user = pull_request['user']['login']
  payload = JSON.generate(:environment => 'production', :deploy_user => user)
  @client.create_deployment(pull_request['head']['repo']['full_name'], pull_request['head']['sha'], {:payload => payload, :description => "Deploying my sweet branch"})
end
```

Deployments can have some metadata attached to them, in the form of a `payload`
and a `description`. Although these values are optional, it's helpful to use
for logging and representing information.

When a new deployment is created, a completely separate event is triggered. That's
why we have a new `switch` case in the event handler for `deployment`. You can
use this information to be notified when a deployment has been triggered.

Deployments can take a rather long time, so we'll want to listen for various events,
such as when the deployment was created, and what state it's in.

Let's simulate a deployment that does some work, and notice the effect it has on
the output. First, let's complete our `process_deployment` method:

```ruby
def process_deployment
  payload = JSON.parse(@payload['payload'])
  # you can send this information to your chat room, monitor, pager, etc.
  puts "Processing '#{@payload['description']}' for #{payload['deploy_user']} to #{payload['environment']}"
  sleep 2 # simulate work
  @client.create_deployment_status("repos/#{@payload['repository']['full_name']}/deployments/#{@payload['id']}", 'pending')
  sleep 2 # simulate work
  @client.create_deployment_status("repos/#{@payload['repository']['full_name']}/deployments/#{@payload['id']}", 'success')
end
```

Finally, we'll simulate storing the status information as console output:

```ruby
def update_deployment_status
  puts "Deployment status for #{@payload['id']} is #{@payload['state']}"
end
```

Let's break down what's going on. A new deployment is created by `start_deployment`,
which triggers the `deployment` event. From there, we call `process_deployment`
to simulate work that's going on. During that processing, we also make a call to
`create_deployment_status`, which lets a receiver know what's going on, as we
switch the status to `pending`.

After the deployment is finished, we set the status to `success`.

## Conclusion

At GitHub, we've used a version of [Heaven](https://github.com/atmos/heaven) to manage
our deployments for years. A common flow is essentially the same as the
server we've built above:

- Wait for a response on the state of the CI checks (success or failure)
- If the required checks succeed, merge the pull request
- Heaven takes the merged code, and deploys it to staging and production servers
- In the meantime, Heaven also notifies everyone about the build, via [Hubot](https://github.com/github/hubot) sitting in our chat rooms

That's it! You don't need to build your own deployment setup to use this example.
You can always rely on [GitHub integrations](https://github.com/integrations).

---

# Discovering resources for a user

> Learn how to find the repositories and organizations that your app can access for a user in a reliable way for your authenticated requests to the REST API.

When making authenticated requests to the GitHub API, applications often need to fetch the current user's repositories and organizations. In this guide, we'll explain how to reliably discover those resources.

To interact with the GitHub API, we'll be using [Octokit.rb](https://github.com/octokit/octokit.rb). You can find the complete source code for this project in the [platform-samples](https://github.com/github/platform-samples/tree/master/api/ruby/discovering-resources-for-a-user) repository.

## Getting started

If you haven't already, you should read the [Basics of Authentication](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authenticating-to-the-rest-api-with-an-oauth-app) guide before working through the examples below. The examples below assume that you have [registered an OAuth app](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authenticating-to-the-rest-api-with-an-oauth-app#registering-your-app) and that your [application has an OAuth token for a user](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authenticating-to-the-rest-api-with-an-oauth-app#making-authenticated-requests).

## Discover the repositories that your app can access for a user

In addition to having their own personal repositories, a user may be a collaborator on repositories owned by other users and organizations. Collectively, these are the repositories where the user has privileged access: either it's a private repository where the user has read or write access, or it's a public repository where the user has write access.

[OAuth scopes](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/scopes-for-oauth-apps) and [organization application policies](https://developer.github.com/changes/2015-01-19-an-integrators-guide-to-organization-application-policies/) determine which of those repositories your app can access for a user. Use the workflow below to discover those repositories.

As always, first we'll require [GitHub's Octokit.rb](https://github.com/octokit/octokit.rb) Ruby library. Then we'll configure Octokit.rb to automatically handle pagination for us. For more information about pagination, see [Using pagination in the REST API](https://docs.github.com/en/rest/guides/using-pagination-in-the-rest-api).

```ruby
require 'octokit'

Octokit.auto_paginate = true
```

Next, we'll pass in our application's [OAuth token for a given user](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authenticating-to-the-rest-api-with-an-oauth-app#making-authenticated-requests):

```ruby
# !!! DO NOT EVER USE HARD-CODED VALUES IN A REAL APP !!!
# Instead, set and test environment variables, like below.
client = Octokit::Client.new :access_token => ENV["OAUTH_ACCESS_TOKEN"]
```

Then, we're ready to fetch the [repositories that our application can access for the user](https://docs.github.com/en/rest/repos/repos#list-repositories-for-the-authenticated-user):

```ruby
client.repositories.each do |repository|
  full_name = repository[:full_name]
  has_push_access = repository[:permissions][:push]

  access_type = if has_push_access
                  "write"
                else
                  "read-only"
                end

  puts "User has #{access_type} access to #{full_name}."
end
```

## Discover the organizations that your app can access for a user

Applications can perform all sorts of organization-related tasks for a user. To perform these tasks, the app needs an [OAuth authorization](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/scopes-for-oauth-apps) with sufficient permission. For example, the `read:org` scope allows you to [list teams](https://docs.github.com/en/rest/teams/teams#list-teams), and the `user` scope lets you [publicize the user’s organization membership](https://docs.github.com/en/rest/orgs/members#set-public-organization-membership-for-the-authenticated-user). Once a user has granted one or more of these scopes to your app, you're ready to fetch the user’s organizations.

Just as we did when discovering repositories above, we'll start by requiring [GitHub's Octokit.rb](https://github.com/octokit/octokit.rb) Ruby library and configuring it to take care of pagination for us. For more information about pagination, see [Using pagination in the REST API](https://docs.github.com/en/rest/guides/using-pagination-in-the-rest-api).

```ruby
require 'octokit'

Octokit.auto_paginate = true
```

Next, we'll pass in our application's [OAuth token for a given user](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authenticating-to-the-rest-api-with-an-oauth-app#making-authenticated-requests) to initialize our API client:

```ruby
# !!! DO NOT EVER USE HARD-CODED VALUES IN A REAL APP !!!
# Instead, set and test environment variables, like below.
client = Octokit::Client.new :access_token => ENV["OAUTH_ACCESS_TOKEN"]
```

Then, we can [list the organizations that our application can access for the user](https://docs.github.com/en/rest/orgs/orgs#list-organizations-for-the-authenticated-user):

```ruby
client.organizations.each do |organization|
  puts "User belongs to the #{organization[:login]} organization."
end
```

### Return all of the user's organization memberships

If you've read the docs from cover to cover, you may have noticed an [API method for listing a user's public organization memberships](https://docs.github.com/en/rest/orgs/orgs#list-organizations-for-a-user). Most applications should avoid this API method. This method only returns the user's public organization memberships, not their private organization memberships.

As an application, you typically want all of the user's organizations that your app is authorized to access. The workflow above will give you exactly that.

---

# Encrypting secrets for the REST API

> In order to create or update a secret with the REST API, you must encrypt the value of the secret.

## About encrypting secrets

Several REST API endpoints let you create secrets on GitHub. To use these endpoints, you must encrypt the secret value using libsodium. For more information, see the [libsodium documentation](https://libsodium.gitbook.io/doc/bindings_for_other_languages).

In order to encrypt a secret, you need a Base64 encoded public key. You can get a public key from the REST API. To determine which endpoint to use to get the public key, look at the documentation for the `encrypted_value` parameter in the endpoint that you will use to create a secret .

## Example encrypting a secret using Node.js

If you are using Node.js, you can encrypt your secret using the libsodium-wrappers library. For more information, see [libsodium-wrappers](https://www.npmjs.com/package/libsodium-wrappers).

In the following example, replace `YOUR_SECRET` with the plain text value that you want to encrypt. Replace `YOUR_BASE64_KEY` with your Base64 encoded public key. The documentation for the endpoint that you will use to create a secret will tell you which endpoint you can use to get the public key. `ORIGINAL` is not a placeholder; it is a parameter for the libsodium-wrappers library.

```javascript
const sodium = require('libsodium-wrappers')

const secret = 'YOUR_SECRET'
const key = 'YOUR_BASE64_KEY'

//Check if libsodium is ready and then proceed.
sodium.ready.then(() => {
  // Convert the secret and key to a Uint8Array.
  let binkey = sodium.from_base64(key, sodium.base64_variants.ORIGINAL)
  let binsec = sodium.from_string(secret)

  // Encrypt the secret using libsodium
  let encBytes = sodium.crypto_box_seal(binsec, binkey)

  // Convert the encrypted Uint8Array to Base64
  let output = sodium.to_base64(encBytes, sodium.base64_variants.ORIGINAL)

  // Print the output
  console.log(output)
});
```

## Example encrypting a secret using Python

If you are using Python 3, you can encrypt your secret using the PyNaCl library. For more information, see [PyNaCl](https://pynacl.readthedocs.io/en/latest/public/#nacl-public-sealedbox).

In the following example, replace `YOUR_SECRET` with the plain text value that you want to encrypt. Replace `YOUR_BASE64_KEY` with your Base64 encoded public key. The documentation for the endpoint that you will use to create a secret will tell you which endpoint you can use to get the public key.

```python
from base64 import b64encode
from nacl import encoding, public

def encrypt(public_key: str, secret_value: str) -> str:
  """Encrypt a Unicode string using the public key."""
  public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
  sealed_box = public.SealedBox(public_key)
  encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
  return b64encode(encrypted).decode("utf-8")

encrypt("YOUR_BASE64_KEY", "YOUR_SECRET")
```

## Example encrypting a secret using C#

If you are using C#, you can encrypt your secret using the Sodium.Core package. For more information, see [Sodium.Core](https://www.nuget.org/packages/Sodium.Core/).

In the following example, replace `YOUR_SECRET` with the plain text value that you want to encrypt. Replace `YOUR_BASE64_KEY` with your Base64 encoded public key. The documentation for the endpoint that you will use to create a secret will tell you which endpoint you can use to get the public key.

```csharp
var secretValue = System.Text.Encoding.UTF8.GetBytes("YOUR_SECRET");
var publicKey = Convert.FromBase64String("YOUR_BASE64_KEY");

var sealedPublicKeyBox = Sodium.SealedPublicKeyBox.Create(secretValue, publicKey);

Console.WriteLine(Convert.ToBase64String(sealedPublicKeyBox));
```

## Example encrypting a secret using Ruby

If you are using Ruby, you can encrypt your secret using the RbNaCl gem. For more information, see [RbNaCl](https://github.com/RubyCrypto/rbnacl).

In the following example, replace `YOUR_SECRET` with the plain text value that you want to encrypt. Replace `YOUR_BASE64_KEY` with your Base64 encoded public key. The documentation for the endpoint that you will use to create a secret will tell you which endpoint you can use to get the public key.

```ruby
require "rbnacl"
require "base64"

key = Base64.decode64("YOUR_BASE64_KEY")
public_key = RbNaCl::PublicKey.new(key)

box = RbNaCl::Boxes::Sealed.from_public_key(public_key)
encrypted_secret = box.encrypt("YOUR_SECRET")

# Print the base64 encoded secret
puts Base64.strict_encode64(encrypted_secret)
```
