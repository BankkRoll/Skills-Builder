# REST API endpoints for organization interactions and more

# REST API endpoints for organization interactions

> Use the REST API to temporarily restrict which type of user can comment, open issues, or create pull requests in the organization's public repositories.

## About organization interactions

Organization owners can temporarily restrict which type of user can comment, open issues, or create pull requests in the organization's public repositories. When restrictions are enabled, only the specified type of GitHub user will be able to participate in interactions. Restrictions automatically expire after a defined duration. Here's more about the types of GitHub users:

- **Existing users:** When you limit interactions to `existing_users`, new users with accounts less than 24 hours old who have not previously contributed and are not collaborators will be temporarily restricted in the organization.
- **Contributors only:** When you limit interactions to `contributors_only`, users who have not previously contributed and are not collaborators will be temporarily restricted in the organization.
- **Collaborators only:** When you limit interactions to `collaborators_only`, users who are not collaborators will be temporarily restricted in the organization.

Setting the interaction limit at the organization level will overwrite any interaction limits that are set for individual repositories owned by the organization. To set different interaction limits for individual repositories owned by the organization, use the [Repository](https://docs.github.com/en/rest/interactions/repos) interactions endpoints instead.

---

# REST API endpoints for repository interactions

> Use the REST API to temporarily restrict which type of user can comment, open issues, or create pull requests in a public repository.

## About repository interactions

People with owner or admin access can use the REST API to temporarily restrict which type of user can comment, open issues, or create pull requests in a public repository. When restrictions are enabled, only the specified type of GitHub user will be able to participate in interactions. Restrictions automatically expire after a defined duration. Here's more about the types of GitHub users:

- **Existing users:** When you limit interactions to `existing_users`, new users with accounts less than 24 hours old who have not previously contributed and are not collaborators will be temporarily restricted in the repository.
- **Contributors only:** When you limit interactions to `contributors_only`, users who have not previously contributed and are not collaborators will be temporarily restricted in the repository.
- **Collaborators only:** When you limit interactions to `collaborators_only`, users who are not collaborators will be temporarily restricted in the repository.

If an interaction limit is enabled for the user or organization that owns the repository, the limit cannot be changed for the individual repository. Instead, use the [User](https://docs.github.com/en/rest/interactions/user) or [Organization](https://docs.github.com/en/rest/interactions/orgs) interactions endpoints to change the interaction limit.

---

# REST API endpoints for user interactions

> Use the REST API to temporarily restrict which type of user can comment, open issues, or create pull requests in your public repositories.

## About user interactions

You can use the REST API to temporarily restrict which type of user can comment, open issues, or create pull requests on your public repositories. When restrictions are enabled, only the specified type of GitHub user will be able to participate in interactions. Restrictions automatically expire after a defined duration. Here's more about the types of GitHub users:

- **Existing users:** When you limit interactions to `existing_users`, new users with accounts less than 24 hours old who have not previously contributed and are not collaborators will be temporarily restricted from interacting with your repositories.
- **Contributors only:** When you limit interactions to `contributors_only`, users who have not previously contributed and are not collaborators will be temporarily restricted from interacting with your repositories.
- **Collaborators only:** When you limit interactions to `collaborators_only`, users who are not collaborators will be temporarily restricted from interacting with your repositories.

Setting the interaction limit at the user level will overwrite any interaction limits that are set for individual repositories owned by the user. To set different interaction limits for individual repositories owned by the user, use the [Repository](https://docs.github.com/en/rest/interactions/repos) interactions endpoints instead.
