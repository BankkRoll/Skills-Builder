# REST API endpoints for deploy keys

# REST API endpoints for deploy keys

> Use the REST API to create and manage deploy keys.

## About deploy keys

You can launch projects from a repository on GitHub.com to your server by using a deploy key, which is an SSH key that grants access to a single repository. GitHub attaches the public part of the key directly to your repository instead of a personal account, and the private part of the key remains on your server. For more information, see [Delivering deployments](https://docs.github.com/en/rest/guides/delivering-deployments).

Deploy keys can either be set up using the following API endpoints, or by using the GitHub web interface. To learn how to set deploy keys up in the web interface, see [Managing deploy keys](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/managing-deploy-keys).

There are a few cases when a deploy key will be deleted by other activity:

- If the deploy key is created with a personal access token, deleting the personal access token will also delete the deploy key. Regenerating the personal access token will not delete the deploy key.
- If the deploy key is created with an OAuth app token, revoking the token will also delete the deploy key.

Conversely, these activities will not delete a deploy key:

- If the deploy key is created with a GitHub App user access token, revoking the token will not delete the deploy key.
- If the deploy key is created with a GitHub App installation access token, uninstalling or deleting the app will not delete the deploy key.
- If the deploy key is created with a personal access token, regenerating the personal access token will not delete the deploy key.
