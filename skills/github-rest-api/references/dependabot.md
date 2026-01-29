# REST API endpoints for Dependabot alerts and more

# REST API endpoints for Dependabot alerts

> Use the REST API to interact with Dependabot alerts for a repository.

Note

The ability to use the REST API to manage Dependabot alerts is currently in public preview and subject to change.

## About Dependabot alerts

You can view Dependabot alerts for a repository and update individual alerts with the REST API. For more information, see [About Dependabot alerts](https://docs.github.com/en/code-security/dependabot/dependabot-alerts/about-dependabot-alerts).

---

# REST API endpoints for Dependabot repository access

> Use the REST API to manage which repositories Dependabot can access within an organization.

## About Dependabot repository access

You can list repositories that Dependabot already has access to and set a default repository access level for Dependabot.

---

# REST API endpoints for Dependabot secrets

> Use the REST API to manage Dependabot secrets for an organization or repository.

## About Dependabot secrets

You can create, update, delete, and retrieve information about encrypted secrets using the REST API. Secrets allow you to store sensitive information, such as access tokens, in your repository, repository environments, or organization. For more information, see [Configuring access to private registries for Dependabot](https://docs.github.com/en/code-security/dependabot/working-with-dependabot/configuring-access-to-private-registries-for-dependabot#storing-credentials-for-dependabot-to-use).

These endpoints are available for authenticated users, OAuth apps, and GitHub Apps. Access tokens require [reposcope](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/scopes-for-oauth-apps#available-scopes) for private repositories and [public_reposcope](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/scopes-for-oauth-apps#available-scopes) for public repositories. GitHub Apps must have the `dependabot_secrets` permission to use these endpoints. Authenticated users must have collaborator access to a repository to create, update, or read secrets.
