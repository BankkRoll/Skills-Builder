# About the OpenAPI description for the REST API and more

# About the OpenAPI description for the REST API

> The GitHub REST API is fully described in an OpenAPI compliant document.

## About OpenAPI

OpenAPI is a specification for describing REST API interfaces. It describes the API without requiring access to the source code or additional documentation. The specification is both human and machine readable. For more information, see [the OpenAPI specification documentation](https://spec.openapis.org/oas/v3.1.0).

## About GitHub's OpenAPI description

GitHub's OpenAPI description of the REST API is publicly available. You can find the description in the open source [github/rest-api-description](https://github.com/github/rest-api-description) repository.

GitHub provides both 3.0 and 3.1 OpenAPI descriptions.

For each description, there is a version for each product: GitHub Free/GitHub Pro/GitHub Team (`api.github.com`), GitHub Enterprise Cloud (`ghec`), and each version of GitHub Enterprise Server (`ghes-X.X`).

For each product, if date-based versioning is supported, there is also a description for each date-based version. For more information, see [API Versions](https://docs.github.com/en/rest/overview/api-versions).

Each description is available in a bundled or in a dereferenced format. The bundled format uses `$ref` to refer to OpenAPI components that are shared between endpoints. The dereferenced format includes the fully expanded description.

## Using the GitHub OpenAPI description

Because the OpenAPI description is machine readable, you can use it to do things like:

- Generate libraries to facilitate using the REST API
- Validate and test an integration that uses the REST API
- Explore and interact with the REST API using third-party tools, such as Insomnia or Postman

For example, GitHub uses the OpenAPI description to generate the Octokit SDKs. GitHub also uses the OpenAPI description to generate the REST API reference documentation for each endpoint.

---

# About the REST API

> Get oriented to the REST API documentation.

You can use GitHub's API to build scripts and applications that automate processes, integrate with GitHub, and extend GitHub. For example, you could use the API to triage issues, build an analytics dashboard, or manage releases.

Each REST API endpoint is documented individually, and the endpoints are categorized by the resource that they primarily affect. For example, you can find endpoints relating to issues in [REST API endpoints for issues](https://docs.github.com/en/rest/issues).

## Getting started with the REST API

**If you are new to REST APIs**, you may find it helpful to refer to the Quickstart or Getting Started guide for an introduction. For more information, see:

- [Quickstart for GitHub REST API](https://docs.github.com/en/rest/quickstart)
- [Getting started with the REST API](https://docs.github.com/en/rest/guides/getting-started-with-the-rest-api)

**If you are familiar with REST APIs** but new to GitHub's REST API, you may find it helpful to refer to the authentication documentation. For more information, see:

- [Authenticating to the REST API](https://docs.github.com/en/rest/overview/authenticating-to-the-rest-api)

**If you are building scripts or applications** that use the REST API, you may find some of the following guides helpful. For examples of scripting with the REST API, see:

- [Scripting with the REST API and JavaScript](https://docs.github.com/en/rest/guides/scripting-with-the-rest-api-and-javascript)
- [Scripting with the REST API and Ruby](https://docs.github.com/en/rest/guides/scripting-with-the-rest-api-and-ruby)
- [Building a GitHub App that responds to webhook events](https://docs.github.com/en/apps/creating-github-apps/writing-code-for-a-github-app/building-a-github-app-that-responds-to-webhook-events)
- [Building a CLI with a GitHub App](https://docs.github.com/en/apps/creating-github-apps/writing-code-for-a-github-app/building-a-cli-with-a-github-app)
- [Automatically redelivering failed deliveries for a repository webhook](https://docs.github.com/en/webhooks/using-webhooks/automatically-redelivering-failed-deliveries-for-a-repository-webhook)

For a list of libraries to facilitate scripting with the REST API, see [Libraries for the REST API](https://docs.github.com/en/rest/overview/libraries-for-the-rest-api).

If you are building scripts or applications that use the REST API, you might also be interested in using webhooks to get notified about events or a GitHub App to access resources on behalf of a user or in an organization. For more information, see [About webhooks](https://docs.github.com/en/webhooks/about-webhooks) and [Deciding when to build a GitHub App](https://docs.github.com/en/apps/creating-github-apps/about-creating-github-apps/deciding-when-to-build-a-github-app).

## Further reading

- [Comparing GitHub's REST API and GraphQL API](https://docs.github.com/en/rest/overview/comparing-githubs-rest-api-and-graphql-api)
- [Best practices for using the REST API](https://docs.github.com/en/rest/guides/best-practices-for-using-the-rest-api)
- [Keeping your API credentials secure](https://docs.github.com/en/rest/overview/keeping-your-api-credentials-secure)
- [Troubleshooting the REST API](https://docs.github.com/en/rest/overview/troubleshooting-the-rest-api)

---

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
