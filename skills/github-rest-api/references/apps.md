# REST API endpoints for GitHub Apps and more

# REST API endpoints for GitHub Apps

> Use the REST API to interact with GitHub Apps

## About GitHub Apps

If you are using your app with GitHub Actions and want to modify workflow files, you must authenticate on behalf of the user with an OAuth token that includes the `workflow` scope. The user must have admin or write permission to the repository that contains the workflow file. For more information, see [Scopes for OAuth apps](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/scopes-for-oauth-apps#available-scopes).

This page lists endpoints that you can access while authenticated as a GitHub App. For more information, see [Authenticating as a GitHub App](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/authenticating-as-a-github-app).

See [REST API endpoints for GitHub App installations](https://docs.github.com/en/rest/apps/installations) for a list of endpoints that require authentication as a GitHub App installation.

---

# REST API endpoints for GitHub App installations

> Use the REST API to get information about GitHub App installations and perform actions within those installations.

## About GitHub App installations

A GitHub App installation refers to the installation of the app on an organization or user account. For information on how to authenticate as an installation and limit access to specific repositories, see [Authenticating as a GitHub App installation](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/authenticating-as-a-github-app-installation).

To list all GitHub App installations for an organization, see [REST API endpoints for organizations](https://docs.github.com/en/rest/orgs/orgs#list-app-installations-for-an-organization).

---

# REST API endpoints for GitHub Marketplace

> Use the REST API to interact with GitHub Marketplace

## About GitHub Marketplace

For more information about GitHub Marketplace, see [GitHub Marketplace](https://docs.github.com/en/apps/publishing-apps-to-github-marketplace).

These endpoints allow you to see which customers are using a pricing plan, see a customer's purchases, and see if an account has an active subscription.

### Testing with stubbed endpoints

You can [test your GitHub App](https://docs.github.com/en/apps/publishing-apps-to-github-marketplace/using-the-github-marketplace-api-in-your-app/testing-your-app) with **stubbed data**. Stubbed data is hard-coded, fake data that will not change based on actual subscriptions.

To test with stubbed data, use a stubbed endpoint in place of its production counterpart. This allows you to test whether the API logic succeeds before listing GitHub Apps on GitHub Marketplace.

Make sure to replace stubbed endpoints with production endpoints before deploying your GitHub App.

---

# REST API endpoints for OAuth authorizations

> Use the REST API to interact with OAuth apps and OAuth authorizations of GitHub Apps

## About OAuth apps and OAuth authorizations of GitHub Apps

You can use these endpoints to manage the OAuth tokens that OAuth apps or GitHub Apps use to access people's accounts on GitHub.

Tokens for OAuth apps have the prefix `gho_`, while OAuth tokens for GitHub Apps, used for authenticating on behalf of the user, have the prefix `ghu_`. You can use the following endpoints for both types of OAuth tokens.

---

# REST API endpoints for GitHub App webhooks

> Use the REST API to interact with webhooks for OAuth apps

## About webhooks for GitHub Apps

A GitHub App's webhook allows your server to receive HTTP `POST` payloads whenever certain events happen for a GitHub App. For more information, see [Webhooks documentation](https://docs.github.com/en/webhooks) and [Using webhooks with GitHub Apps](https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/using-webhooks-with-github-apps).
