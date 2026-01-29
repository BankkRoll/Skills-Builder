# About the REST API and more

# About the REST API

> Learn more about the GitHub REST API and what you can do with it.

# About the REST API

Learn more about the GitHub REST API and what you can do with it.

- [About the REST API](https://docs.github.com/en/rest/about-the-rest-api/about-the-rest-api)
- [Comparing GitHub's REST API and GraphQL API](https://docs.github.com/en/rest/about-the-rest-api/comparing-githubs-rest-api-and-graphql-api)
- [API Versions](https://docs.github.com/en/rest/about-the-rest-api/api-versions)
- [Breaking changes](https://docs.github.com/en/rest/about-the-rest-api/breaking-changes)
- [About the OpenAPI description for the REST API](https://docs.github.com/en/rest/about-the-rest-api/about-the-openapi-description-for-the-rest-api)

---

# REST API endpoints for GitHub Actions

> Use the REST API to interact with GitHub Actions for an organization or repository.

The REST API is now versioned. For more information, see "[About API versioning](https://docs.github.com/rest/overview/api-versions)."

# REST API endpoints for GitHub Actions

Use the REST API to interact with GitHub Actions for an organization or repository.

- [REST API endpoints for GitHub Actions artifacts](https://docs.github.com/en/rest/actions/artifacts)
  - [List artifacts for a repository](https://docs.github.com/en/rest/actions/artifacts#list-artifacts-for-a-repository)
  - [Get an artifact](https://docs.github.com/en/rest/actions/artifacts#get-an-artifact)
  - [Delete an artifact](https://docs.github.com/en/rest/actions/artifacts#delete-an-artifact)
  - [Download an artifact](https://docs.github.com/en/rest/actions/artifacts#download-an-artifact)
  - [List workflow run artifacts](https://docs.github.com/en/rest/actions/artifacts#list-workflow-run-artifacts)
- [REST API endpoints for GitHub Actions cache](https://docs.github.com/en/rest/actions/cache)
  - [Get GitHub Actions cache retention limit for an enterprise](https://docs.github.com/en/rest/actions/cache#get-github-actions-cache-retention-limit-for-an-enterprise)
  - [Set GitHub Actions cache retention limit for an enterprise](https://docs.github.com/en/rest/actions/cache#set-github-actions-cache-retention-limit-for-an-enterprise)
  - [Get GitHub Actions cache storage limit for an enterprise](https://docs.github.com/en/rest/actions/cache#get-github-actions-cache-storage-limit-for-an-enterprise)
  - [Set GitHub Actions cache storage limit for an enterprise](https://docs.github.com/en/rest/actions/cache#set-github-actions-cache-storage-limit-for-an-enterprise)
  - [Get GitHub Actions cache retention limit for an organization](https://docs.github.com/en/rest/actions/cache#get-github-actions-cache-retention-limit-for-an-organization)
  - [Set GitHub Actions cache retention limit for an organization](https://docs.github.com/en/rest/actions/cache#set-github-actions-cache-retention-limit-for-an-organization)
  - [Get GitHub Actions cache storage limit for an organization](https://docs.github.com/en/rest/actions/cache#get-github-actions-cache-storage-limit-for-an-organization)
  - [Set GitHub Actions cache storage limit for an organization](https://docs.github.com/en/rest/actions/cache#set-github-actions-cache-storage-limit-for-an-organization)
  - [Get GitHub Actions cache usage for an organization](https://docs.github.com/en/rest/actions/cache#get-github-actions-cache-usage-for-an-organization)
  - [List repositories with GitHub Actions cache usage for an organization](https://docs.github.com/en/rest/actions/cache#list-repositories-with-github-actions-cache-usage-for-an-organization)
  - [Get GitHub Actions cache retention limit for a repository](https://docs.github.com/en/rest/actions/cache#get-github-actions-cache-retention-limit-for-a-repository)
  - [Set GitHub Actions cache retention limit for a repository](https://docs.github.com/en/rest/actions/cache#set-github-actions-cache-retention-limit-for-a-repository)
  - [Get GitHub Actions cache storage limit for a repository](https://docs.github.com/en/rest/actions/cache#get-github-actions-cache-storage-limit-for-a-repository)
  - [Set GitHub Actions cache storage limit for a repository](https://docs.github.com/en/rest/actions/cache#set-github-actions-cache-storage-limit-for-a-repository)
  - [Get GitHub Actions cache usage for a repository](https://docs.github.com/en/rest/actions/cache#get-github-actions-cache-usage-for-a-repository)
  - [List GitHub Actions caches for a repository](https://docs.github.com/en/rest/actions/cache#list-github-actions-caches-for-a-repository)
  - [Delete GitHub Actions caches for a repository (using a cache key)](https://docs.github.com/en/rest/actions/cache#delete-github-actions-caches-for-a-repository-using-a-cache-key)
  - [Delete a GitHub Actions cache for a repository (using a cache ID)](https://docs.github.com/en/rest/actions/cache#delete-a-github-actions-cache-for-a-repository-using-a-cache-id)
- [GitHub-hosted runners](https://docs.github.com/en/rest/actions/hosted-runners)
  - [List GitHub-hosted runners for an organization](https://docs.github.com/en/rest/actions/hosted-runners#list-github-hosted-runners-for-an-organization)
  - [Create a GitHub-hosted runner for an organization](https://docs.github.com/en/rest/actions/hosted-runners#create-a-github-hosted-runner-for-an-organization)
  - [List custom images for an organization](https://docs.github.com/en/rest/actions/hosted-runners#list-custom-images-for-an-organization)
  - [Get a custom image definition for GitHub Actions Hosted Runners](https://docs.github.com/en/rest/actions/hosted-runners#get-a-custom-image-definition-for-github-actions-hosted-runners)
  - [Delete a custom image from the organization](https://docs.github.com/en/rest/actions/hosted-runners#delete-a-custom-image-from-the-organization)
  - [List image versions of a custom image for an organization](https://docs.github.com/en/rest/actions/hosted-runners#list-image-versions-of-a-custom-image-for-an-organization)
  - [Get an image version of a custom image for GitHub Actions Hosted Runners](https://docs.github.com/en/rest/actions/hosted-runners#get-an-image-version-of-a-custom-image-for-github-actions-hosted-runners)
  - [Delete an image version of custom image from the organization](https://docs.github.com/en/rest/actions/hosted-runners#delete-an-image-version-of-custom-image-from-the-organization)
  - [Get GitHub-owned images for GitHub-hosted runners in an organization](https://docs.github.com/en/rest/actions/hosted-runners#get-github-owned-images-for-github-hosted-runners-in-an-organization)
  - [Get partner images for GitHub-hosted runners in an organization](https://docs.github.com/en/rest/actions/hosted-runners#get-partner-images-for-github-hosted-runners-in-an-organization)
  - [Get limits on GitHub-hosted runners for an organization](https://docs.github.com/en/rest/actions/hosted-runners#get-limits-on-github-hosted-runners-for-an-organization)
  - [Get GitHub-hosted runners machine specs for an organization](https://docs.github.com/en/rest/actions/hosted-runners#get-github-hosted-runners-machine-specs-for-an-organization)
  - [Get platforms for GitHub-hosted runners in an organization](https://docs.github.com/en/rest/actions/hosted-runners#get-platforms-for-github-hosted-runners-in-an-organization)
  - [Get a GitHub-hosted runner for an organization](https://docs.github.com/en/rest/actions/hosted-runners#get-a-github-hosted-runner-for-an-organization)
  - [Update a GitHub-hosted runner for an organization](https://docs.github.com/en/rest/actions/hosted-runners#update-a-github-hosted-runner-for-an-organization)
  - [Delete a GitHub-hosted runner for an organization](https://docs.github.com/en/rest/actions/hosted-runners#delete-a-github-hosted-runner-for-an-organization)
- [REST API endpoints for GitHub Actions OIDC](https://docs.github.com/en/rest/actions/oidc)
  - [Get the customization template for an OIDC subject claim for an organization](https://docs.github.com/en/rest/actions/oidc#get-the-customization-template-for-an-oidc-subject-claim-for-an-organization)
  - [Set the customization template for an OIDC subject claim for an organization](https://docs.github.com/en/rest/actions/oidc#set-the-customization-template-for-an-oidc-subject-claim-for-an-organization)
  - [Get the customization template for an OIDC subject claim for a repository](https://docs.github.com/en/rest/actions/oidc#get-the-customization-template-for-an-oidc-subject-claim-for-a-repository)
  - [Set the customization template for an OIDC subject claim for a repository](https://docs.github.com/en/rest/actions/oidc#set-the-customization-template-for-an-oidc-subject-claim-for-a-repository)
- [REST API endpoints for GitHub Actions permissions](https://docs.github.com/en/rest/actions/permissions)
  - [Get GitHub Actions permissions for an organization](https://docs.github.com/en/rest/actions/permissions#get-github-actions-permissions-for-an-organization)
  - [Set GitHub Actions permissions for an organization](https://docs.github.com/en/rest/actions/permissions#set-github-actions-permissions-for-an-organization)
  - [Get artifact and log retention settings for an organization](https://docs.github.com/en/rest/actions/permissions#get-artifact-and-log-retention-settings-for-an-organization)
  - [Set artifact and log retention settings for an organization](https://docs.github.com/en/rest/actions/permissions#set-artifact-and-log-retention-settings-for-an-organization)
  - [Get fork PR contributor approval permissions for an organization](https://docs.github.com/en/rest/actions/permissions#get-fork-pr-contributor-approval-permissions-for-an-organization)
  - [Set fork PR contributor approval permissions for an organization](https://docs.github.com/en/rest/actions/permissions#set-fork-pr-contributor-approval-permissions-for-an-organization)
  - [Get private repo fork PR workflow settings for an organization](https://docs.github.com/en/rest/actions/permissions#get-private-repo-fork-pr-workflow-settings-for-an-organization)
  - [Set private repo fork PR workflow settings for an organization](https://docs.github.com/en/rest/actions/permissions#set-private-repo-fork-pr-workflow-settings-for-an-organization)
  - [List selected repositories enabled for GitHub Actions in an organization](https://docs.github.com/en/rest/actions/permissions#list-selected-repositories-enabled-for-github-actions-in-an-organization)
  - [Set selected repositories enabled for GitHub Actions in an organization](https://docs.github.com/en/rest/actions/permissions#set-selected-repositories-enabled-for-github-actions-in-an-organization)
  - [Enable a selected repository for GitHub Actions in an organization](https://docs.github.com/en/rest/actions/permissions#enable-a-selected-repository-for-github-actions-in-an-organization)
  - [Disable a selected repository for GitHub Actions in an organization](https://docs.github.com/en/rest/actions/permissions#disable-a-selected-repository-for-github-actions-in-an-organization)
  - [Get allowed actions and reusable workflows for an organization](https://docs.github.com/en/rest/actions/permissions#get-allowed-actions-and-reusable-workflows-for-an-organization)
  - [Set allowed actions and reusable workflows for an organization](https://docs.github.com/en/rest/actions/permissions#set-allowed-actions-and-reusable-workflows-for-an-organization)
  - [Get self-hosted runners settings for an organization](https://docs.github.com/en/rest/actions/permissions#get-self-hosted-runners-settings-for-an-organization)
  - [Set self-hosted runners settings for an organization](https://docs.github.com/en/rest/actions/permissions#set-self-hosted-runners-settings-for-an-organization)
  - [List repositories allowed to use self-hosted runners in an organization](https://docs.github.com/en/rest/actions/permissions#list-repositories-allowed-to-use-self-hosted-runners-in-an-organization)
  - [Set repositories allowed to use self-hosted runners in an organization](https://docs.github.com/en/rest/actions/permissions#set-repositories-allowed-to-use-self-hosted-runners-in-an-organization)
  - [Add a repository to the list of repositories allowed to use self-hosted runners in an organization](https://docs.github.com/en/rest/actions/permissions#add-a-repository-to-the-list-of-repositories-allowed-to-use-self-hosted-runners-in-an-organization)
  - [Remove a repository from the list of repositories allowed to use self-hosted runners in an organization](https://docs.github.com/en/rest/actions/permissions#remove-a-repository-from-the-list-of-repositories-allowed-to-use-self-hosted-runners-in-an-organization)
  - [Get default workflow permissions for an organization](https://docs.github.com/en/rest/actions/permissions#get-default-workflow-permissions-for-an-organization)
  - [Set default workflow permissions for an organization](https://docs.github.com/en/rest/actions/permissions#set-default-workflow-permissions-for-an-organization)
  - [Get GitHub Actions permissions for a repository](https://docs.github.com/en/rest/actions/permissions#get-github-actions-permissions-for-a-repository)
  - [Set GitHub Actions permissions for a repository](https://docs.github.com/en/rest/actions/permissions#set-github-actions-permissions-for-a-repository)
  - [Get the level of access for workflows outside of the repository](https://docs.github.com/en/rest/actions/permissions#get-the-level-of-access-for-workflows-outside-of-the-repository)
  - [Set the level of access for workflows outside of the repository](https://docs.github.com/en/rest/actions/permissions#set-the-level-of-access-for-workflows-outside-of-the-repository)
  - [Get artifact and log retention settings for a repository](https://docs.github.com/en/rest/actions/permissions#get-artifact-and-log-retention-settings-for-a-repository)
  - [Set artifact and log retention settings for a repository](https://docs.github.com/en/rest/actions/permissions#set-artifact-and-log-retention-settings-for-a-repository)
  - [Get fork PR contributor approval permissions for a repository](https://docs.github.com/en/rest/actions/permissions#get-fork-pr-contributor-approval-permissions-for-a-repository)
  - [Set fork PR contributor approval permissions for a repository](https://docs.github.com/en/rest/actions/permissions#set-fork-pr-contributor-approval-permissions-for-a-repository)
  - [Get private repo fork PR workflow settings for a repository](https://docs.github.com/en/rest/actions/permissions#get-private-repo-fork-pr-workflow-settings-for-a-repository)
  - [Set private repo fork PR workflow settings for a repository](https://docs.github.com/en/rest/actions/permissions#set-private-repo-fork-pr-workflow-settings-for-a-repository)
  - [Get allowed actions and reusable workflows for a repository](https://docs.github.com/en/rest/actions/permissions#get-allowed-actions-and-reusable-workflows-for-a-repository)
  - [Set allowed actions and reusable workflows for a repository](https://docs.github.com/en/rest/actions/permissions#set-allowed-actions-and-reusable-workflows-for-a-repository)
  - [Get default workflow permissions for a repository](https://docs.github.com/en/rest/actions/permissions#get-default-workflow-permissions-for-a-repository)
  - [Set default workflow permissions for a repository](https://docs.github.com/en/rest/actions/permissions#set-default-workflow-permissions-for-a-repository)
- [REST API endpoints for GitHub Actions Secrets](https://docs.github.com/en/rest/actions/secrets)
  - [List organization secrets](https://docs.github.com/en/rest/actions/secrets#list-organization-secrets)
  - [Get an organization public key](https://docs.github.com/en/rest/actions/secrets#get-an-organization-public-key)
  - [Get an organization secret](https://docs.github.com/en/rest/actions/secrets#get-an-organization-secret)
  - [Create or update an organization secret](https://docs.github.com/en/rest/actions/secrets#create-or-update-an-organization-secret)
  - [Delete an organization secret](https://docs.github.com/en/rest/actions/secrets#delete-an-organization-secret)
  - [List selected repositories for an organization secret](https://docs.github.com/en/rest/actions/secrets#list-selected-repositories-for-an-organization-secret)
  - [Set selected repositories for an organization secret](https://docs.github.com/en/rest/actions/secrets#set-selected-repositories-for-an-organization-secret)
  - [Add selected repository to an organization secret](https://docs.github.com/en/rest/actions/secrets#add-selected-repository-to-an-organization-secret)
  - [Remove selected repository from an organization secret](https://docs.github.com/en/rest/actions/secrets#remove-selected-repository-from-an-organization-secret)
  - [List repository organization secrets](https://docs.github.com/en/rest/actions/secrets#list-repository-organization-secrets)
  - [List repository secrets](https://docs.github.com/en/rest/actions/secrets#list-repository-secrets)
  - [Get a repository public key](https://docs.github.com/en/rest/actions/secrets#get-a-repository-public-key)
  - [Get a repository secret](https://docs.github.com/en/rest/actions/secrets#get-a-repository-secret)
  - [Create or update a repository secret](https://docs.github.com/en/rest/actions/secrets#create-or-update-a-repository-secret)
  - [Delete a repository secret](https://docs.github.com/en/rest/actions/secrets#delete-a-repository-secret)
  - [List environment secrets](https://docs.github.com/en/rest/actions/secrets#list-environment-secrets)
  - [Get an environment public key](https://docs.github.com/en/rest/actions/secrets#get-an-environment-public-key)
  - [Get an environment secret](https://docs.github.com/en/rest/actions/secrets#get-an-environment-secret)
  - [Create or update an environment secret](https://docs.github.com/en/rest/actions/secrets#create-or-update-an-environment-secret)
  - [Delete an environment secret](https://docs.github.com/en/rest/actions/secrets#delete-an-environment-secret)
- [REST API endpoints for self-hosted runner groups](https://docs.github.com/en/rest/actions/self-hosted-runner-groups)
  - [List self-hosted runner groups for an organization](https://docs.github.com/en/rest/actions/self-hosted-runner-groups#list-self-hosted-runner-groups-for-an-organization)
  - [Create a self-hosted runner group for an organization](https://docs.github.com/en/rest/actions/self-hosted-runner-groups#create-a-self-hosted-runner-group-for-an-organization)
  - [Get a self-hosted runner group for an organization](https://docs.github.com/en/rest/actions/self-hosted-runner-groups#get-a-self-hosted-runner-group-for-an-organization)
  - [Update a self-hosted runner group for an organization](https://docs.github.com/en/rest/actions/self-hosted-runner-groups#update-a-self-hosted-runner-group-for-an-organization)
  - [Delete a self-hosted runner group from an organization](https://docs.github.com/en/rest/actions/self-hosted-runner-groups#delete-a-self-hosted-runner-group-from-an-organization)
  - [List GitHub-hosted runners in a group for an organization](https://docs.github.com/en/rest/actions/self-hosted-runner-groups#list-github-hosted-runners-in-a-group-for-an-organization)
  - [List repository access to a self-hosted runner group in an organization](https://docs.github.com/en/rest/actions/self-hosted-runner-groups#list-repository-access-to-a-self-hosted-runner-group-in-an-organization)
  - [Set repository access for a self-hosted runner group in an organization](https://docs.github.com/en/rest/actions/self-hosted-runner-groups#set-repository-access-for-a-self-hosted-runner-group-in-an-organization)
  - [Add repository access to a self-hosted runner group in an organization](https://docs.github.com/en/rest/actions/self-hosted-runner-groups#add-repository-access-to-a-self-hosted-runner-group-in-an-organization)
  - [Remove repository access to a self-hosted runner group in an organization](https://docs.github.com/en/rest/actions/self-hosted-runner-groups#remove-repository-access-to-a-self-hosted-runner-group-in-an-organization)
  - [List self-hosted runners in a group for an organization](https://docs.github.com/en/rest/actions/self-hosted-runner-groups#list-self-hosted-runners-in-a-group-for-an-organization)
  - [Set self-hosted runners in a group for an organization](https://docs.github.com/en/rest/actions/self-hosted-runner-groups#set-self-hosted-runners-in-a-group-for-an-organization)
  - [Add a self-hosted runner to a group for an organization](https://docs.github.com/en/rest/actions/self-hosted-runner-groups#add-a-self-hosted-runner-to-a-group-for-an-organization)
  - [Remove a self-hosted runner from a group for an organization](https://docs.github.com/en/rest/actions/self-hosted-runner-groups#remove-a-self-hosted-runner-from-a-group-for-an-organization)
- [REST API endpoints for self-hosted runners](https://docs.github.com/en/rest/actions/self-hosted-runners)
  - [List self-hosted runners for an organization](https://docs.github.com/en/rest/actions/self-hosted-runners#list-self-hosted-runners-for-an-organization)
  - [List runner applications for an organization](https://docs.github.com/en/rest/actions/self-hosted-runners#list-runner-applications-for-an-organization)
  - [Create configuration for a just-in-time runner for an organization](https://docs.github.com/en/rest/actions/self-hosted-runners#create-configuration-for-a-just-in-time-runner-for-an-organization)
  - [Create a registration token for an organization](https://docs.github.com/en/rest/actions/self-hosted-runners#create-a-registration-token-for-an-organization)
  - [Create a remove token for an organization](https://docs.github.com/en/rest/actions/self-hosted-runners#create-a-remove-token-for-an-organization)
  - [Get a self-hosted runner for an organization](https://docs.github.com/en/rest/actions/self-hosted-runners#get-a-self-hosted-runner-for-an-organization)
  - [Delete a self-hosted runner from an organization](https://docs.github.com/en/rest/actions/self-hosted-runners#delete-a-self-hosted-runner-from-an-organization)
  - [List labels for a self-hosted runner for an organization](https://docs.github.com/en/rest/actions/self-hosted-runners#list-labels-for-a-self-hosted-runner-for-an-organization)
  - [Add custom labels to a self-hosted runner for an organization](https://docs.github.com/en/rest/actions/self-hosted-runners#add-custom-labels-to-a-self-hosted-runner-for-an-organization)
  - [Set custom labels for a self-hosted runner for an organization](https://docs.github.com/en/rest/actions/self-hosted-runners#set-custom-labels-for-a-self-hosted-runner-for-an-organization)
  - [Remove all custom labels from a self-hosted runner for an organization](https://docs.github.com/en/rest/actions/self-hosted-runners#remove-all-custom-labels-from-a-self-hosted-runner-for-an-organization)
  - [Remove a custom label from a self-hosted runner for an organization](https://docs.github.com/en/rest/actions/self-hosted-runners#remove-a-custom-label-from-a-self-hosted-runner-for-an-organization)
  - [List self-hosted runners for a repository](https://docs.github.com/en/rest/actions/self-hosted-runners#list-self-hosted-runners-for-a-repository)
  - [List runner applications for a repository](https://docs.github.com/en/rest/actions/self-hosted-runners#list-runner-applications-for-a-repository)
  - [Create configuration for a just-in-time runner for a repository](https://docs.github.com/en/rest/actions/self-hosted-runners#create-configuration-for-a-just-in-time-runner-for-a-repository)
  - [Create a registration token for a repository](https://docs.github.com/en/rest/actions/self-hosted-runners#create-a-registration-token-for-a-repository)
  - [Create a remove token for a repository](https://docs.github.com/en/rest/actions/self-hosted-runners#create-a-remove-token-for-a-repository)
  - [Get a self-hosted runner for a repository](https://docs.github.com/en/rest/actions/self-hosted-runners#get-a-self-hosted-runner-for-a-repository)
  - [Delete a self-hosted runner from a repository](https://docs.github.com/en/rest/actions/self-hosted-runners#delete-a-self-hosted-runner-from-a-repository)
  - [List labels for a self-hosted runner for a repository](https://docs.github.com/en/rest/actions/self-hosted-runners#list-labels-for-a-self-hosted-runner-for-a-repository)
  - [Add custom labels to a self-hosted runner for a repository](https://docs.github.com/en/rest/actions/self-hosted-runners#add-custom-labels-to-a-self-hosted-runner-for-a-repository)
  - [Set custom labels for a self-hosted runner for a repository](https://docs.github.com/en/rest/actions/self-hosted-runners#set-custom-labels-for-a-self-hosted-runner-for-a-repository)
  - [Remove all custom labels from a self-hosted runner for a repository](https://docs.github.com/en/rest/actions/self-hosted-runners#remove-all-custom-labels-from-a-self-hosted-runner-for-a-repository)
  - [Remove a custom label from a self-hosted runner for a repository](https://docs.github.com/en/rest/actions/self-hosted-runners#remove-a-custom-label-from-a-self-hosted-runner-for-a-repository)
- [REST API endpoints for GitHub Actions variables](https://docs.github.com/en/rest/actions/variables)
  - [List organization variables](https://docs.github.com/en/rest/actions/variables#list-organization-variables)
  - [Create an organization variable](https://docs.github.com/en/rest/actions/variables#create-an-organization-variable)
  - [Get an organization variable](https://docs.github.com/en/rest/actions/variables#get-an-organization-variable)
  - [Update an organization variable](https://docs.github.com/en/rest/actions/variables#update-an-organization-variable)
  - [Delete an organization variable](https://docs.github.com/en/rest/actions/variables#delete-an-organization-variable)
  - [List selected repositories for an organization variable](https://docs.github.com/en/rest/actions/variables#list-selected-repositories-for-an-organization-variable)
  - [Set selected repositories for an organization variable](https://docs.github.com/en/rest/actions/variables#set-selected-repositories-for-an-organization-variable)
  - [Add selected repository to an organization variable](https://docs.github.com/en/rest/actions/variables#add-selected-repository-to-an-organization-variable)
  - [Remove selected repository from an organization variable](https://docs.github.com/en/rest/actions/variables#remove-selected-repository-from-an-organization-variable)
  - [List repository organization variables](https://docs.github.com/en/rest/actions/variables#list-repository-organization-variables)
  - [List repository variables](https://docs.github.com/en/rest/actions/variables#list-repository-variables)
  - [Create a repository variable](https://docs.github.com/en/rest/actions/variables#create-a-repository-variable)
  - [Get a repository variable](https://docs.github.com/en/rest/actions/variables#get-a-repository-variable)
  - [Update a repository variable](https://docs.github.com/en/rest/actions/variables#update-a-repository-variable)
  - [Delete a repository variable](https://docs.github.com/en/rest/actions/variables#delete-a-repository-variable)
  - [List environment variables](https://docs.github.com/en/rest/actions/variables#list-environment-variables)
  - [Create an environment variable](https://docs.github.com/en/rest/actions/variables#create-an-environment-variable)
  - [Get an environment variable](https://docs.github.com/en/rest/actions/variables#get-an-environment-variable)
  - [Update an environment variable](https://docs.github.com/en/rest/actions/variables#update-an-environment-variable)
  - [Delete an environment variable](https://docs.github.com/en/rest/actions/variables#delete-an-environment-variable)
- [REST API endpoints for workflow jobs](https://docs.github.com/en/rest/actions/workflow-jobs)
  - [Get a job for a workflow run](https://docs.github.com/en/rest/actions/workflow-jobs#get-a-job-for-a-workflow-run)
  - [Download job logs for a workflow run](https://docs.github.com/en/rest/actions/workflow-jobs#download-job-logs-for-a-workflow-run)
  - [List jobs for a workflow run attempt](https://docs.github.com/en/rest/actions/workflow-jobs#list-jobs-for-a-workflow-run-attempt)
  - [List jobs for a workflow run](https://docs.github.com/en/rest/actions/workflow-jobs#list-jobs-for-a-workflow-run)
- [REST API endpoints for workflow runs](https://docs.github.com/en/rest/actions/workflow-runs)
  - [Re-run a job from a workflow run](https://docs.github.com/en/rest/actions/workflow-runs#re-run-a-job-from-a-workflow-run)
  - [List workflow runs for a repository](https://docs.github.com/en/rest/actions/workflow-runs#list-workflow-runs-for-a-repository)
  - [Get a workflow run](https://docs.github.com/en/rest/actions/workflow-runs#get-a-workflow-run)
  - [Delete a workflow run](https://docs.github.com/en/rest/actions/workflow-runs#delete-a-workflow-run)
  - [Get the review history for a workflow run](https://docs.github.com/en/rest/actions/workflow-runs#get-the-review-history-for-a-workflow-run)
  - [Approve a workflow run for a fork pull request](https://docs.github.com/en/rest/actions/workflow-runs#approve-a-workflow-run-for-a-fork-pull-request)
  - [Get a workflow run attempt](https://docs.github.com/en/rest/actions/workflow-runs#get-a-workflow-run-attempt)
  - [Download workflow run attempt logs](https://docs.github.com/en/rest/actions/workflow-runs#download-workflow-run-attempt-logs)
  - [Cancel a workflow run](https://docs.github.com/en/rest/actions/workflow-runs#cancel-a-workflow-run)
  - [Review custom deployment protection rules for a workflow run](https://docs.github.com/en/rest/actions/workflow-runs#review-custom-deployment-protection-rules-for-a-workflow-run)
  - [Force cancel a workflow run](https://docs.github.com/en/rest/actions/workflow-runs#force-cancel-a-workflow-run)
  - [Download workflow run logs](https://docs.github.com/en/rest/actions/workflow-runs#download-workflow-run-logs)
  - [Delete workflow run logs](https://docs.github.com/en/rest/actions/workflow-runs#delete-workflow-run-logs)
  - [Get pending deployments for a workflow run](https://docs.github.com/en/rest/actions/workflow-runs#get-pending-deployments-for-a-workflow-run)
  - [Review pending deployments for a workflow run](https://docs.github.com/en/rest/actions/workflow-runs#review-pending-deployments-for-a-workflow-run)
  - [Re-run a workflow](https://docs.github.com/en/rest/actions/workflow-runs#re-run-a-workflow)
  - [Re-run failed jobs from a workflow run](https://docs.github.com/en/rest/actions/workflow-runs#re-run-failed-jobs-from-a-workflow-run)
  - [Get workflow run usage](https://docs.github.com/en/rest/actions/workflow-runs#get-workflow-run-usage)
  - [List workflow runs for a workflow](https://docs.github.com/en/rest/actions/workflow-runs#list-workflow-runs-for-a-workflow)
- [REST API endpoints for workflows](https://docs.github.com/en/rest/actions/workflows)
  - [List repository workflows](https://docs.github.com/en/rest/actions/workflows#list-repository-workflows)
  - [Get a workflow](https://docs.github.com/en/rest/actions/workflows#get-a-workflow)
  - [Disable a workflow](https://docs.github.com/en/rest/actions/workflows#disable-a-workflow)
  - [Create a workflow dispatch event](https://docs.github.com/en/rest/actions/workflows#create-a-workflow-dispatch-event)
  - [Enable a workflow](https://docs.github.com/en/rest/actions/workflows#enable-a-workflow)
  - [Get workflow usage](https://docs.github.com/en/rest/actions/workflows#get-workflow-usage)

---

# REST API endpoints for activity

> Use the REST API to list events and feeds and manage notifications, starring, and watching.

The REST API is now versioned. For more information, see "[About API versioning](https://docs.github.com/rest/overview/api-versions)."

# REST API endpoints for activity

Use the REST API to list events and feeds and manage notifications, starring, and watching.

- [REST API endpoints for events](https://docs.github.com/en/rest/activity/events)
  - [List public events](https://docs.github.com/en/rest/activity/events#list-public-events)
  - [List public events for a network of repositories](https://docs.github.com/en/rest/activity/events#list-public-events-for-a-network-of-repositories)
  - [List public organization events](https://docs.github.com/en/rest/activity/events#list-public-organization-events)
  - [List repository events](https://docs.github.com/en/rest/activity/events#list-repository-events)
  - [List events for the authenticated user](https://docs.github.com/en/rest/activity/events#list-events-for-the-authenticated-user)
  - [List organization events for the authenticated user](https://docs.github.com/en/rest/activity/events#list-organization-events-for-the-authenticated-user)
  - [List public events for a user](https://docs.github.com/en/rest/activity/events#list-public-events-for-a-user)
  - [List events received by the authenticated user](https://docs.github.com/en/rest/activity/events#list-events-received-by-the-authenticated-user)
  - [List public events received by a user](https://docs.github.com/en/rest/activity/events#list-public-events-received-by-a-user)
- [REST API endpoints for feeds](https://docs.github.com/en/rest/activity/feeds)
  - [Get feeds](https://docs.github.com/en/rest/activity/feeds#get-feeds)
- [REST API endpoints for notifications](https://docs.github.com/en/rest/activity/notifications)
  - [List notifications for the authenticated user](https://docs.github.com/en/rest/activity/notifications#list-notifications-for-the-authenticated-user)
  - [Mark notifications as read](https://docs.github.com/en/rest/activity/notifications#mark-notifications-as-read)
  - [Get a thread](https://docs.github.com/en/rest/activity/notifications#get-a-thread)
  - [Mark a thread as read](https://docs.github.com/en/rest/activity/notifications#mark-a-thread-as-read)
  - [Mark a thread as done](https://docs.github.com/en/rest/activity/notifications#mark-a-thread-as-done)
  - [Get a thread subscription for the authenticated user](https://docs.github.com/en/rest/activity/notifications#get-a-thread-subscription-for-the-authenticated-user)
  - [Set a thread subscription](https://docs.github.com/en/rest/activity/notifications#set-a-thread-subscription)
  - [Delete a thread subscription](https://docs.github.com/en/rest/activity/notifications#delete-a-thread-subscription)
  - [List repository notifications for the authenticated user](https://docs.github.com/en/rest/activity/notifications#list-repository-notifications-for-the-authenticated-user)
  - [Mark repository notifications as read](https://docs.github.com/en/rest/activity/notifications#mark-repository-notifications-as-read)
- [REST API endpoints for starring](https://docs.github.com/en/rest/activity/starring)
  - [List stargazers](https://docs.github.com/en/rest/activity/starring#list-stargazers)
  - [List repositories starred by the authenticated user](https://docs.github.com/en/rest/activity/starring#list-repositories-starred-by-the-authenticated-user)
  - [Check if a repository is starred by the authenticated user](https://docs.github.com/en/rest/activity/starring#check-if-a-repository-is-starred-by-the-authenticated-user)
  - [Star a repository for the authenticated user](https://docs.github.com/en/rest/activity/starring#star-a-repository-for-the-authenticated-user)
  - [Unstar a repository for the authenticated user](https://docs.github.com/en/rest/activity/starring#unstar-a-repository-for-the-authenticated-user)
  - [List repositories starred by a user](https://docs.github.com/en/rest/activity/starring#list-repositories-starred-by-a-user)
- [REST API endpoints for watching](https://docs.github.com/en/rest/activity/watching)
  - [List watchers](https://docs.github.com/en/rest/activity/watching#list-watchers)
  - [Get a repository subscription](https://docs.github.com/en/rest/activity/watching#get-a-repository-subscription)
  - [Set a repository subscription](https://docs.github.com/en/rest/activity/watching#set-a-repository-subscription)
  - [Delete a repository subscription](https://docs.github.com/en/rest/activity/watching#delete-a-repository-subscription)
  - [List repositories watched by the authenticated user](https://docs.github.com/en/rest/activity/watching#list-repositories-watched-by-the-authenticated-user)
  - [List repositories watched by a user](https://docs.github.com/en/rest/activity/watching#list-repositories-watched-by-a-user)

---

# REST API endpoints for apps

> Use the REST API to retrieve information about GitHub Apps and GitHub App installations.

The REST API is now versioned. For more information, see "[About API versioning](https://docs.github.com/rest/overview/api-versions)."

# REST API endpoints for apps

Use the REST API to retrieve information about GitHub Apps and GitHub App installations.

- [REST API endpoints for GitHub Apps](https://docs.github.com/en/rest/apps/apps)
  - [Get the authenticated app](https://docs.github.com/en/rest/apps/apps#get-the-authenticated-app)
  - [Create a GitHub App from a manifest](https://docs.github.com/en/rest/apps/apps#create-a-github-app-from-a-manifest)
  - [List installation requests for the authenticated app](https://docs.github.com/en/rest/apps/apps#list-installation-requests-for-the-authenticated-app)
  - [List installations for the authenticated app](https://docs.github.com/en/rest/apps/apps#list-installations-for-the-authenticated-app)
  - [Get an installation for the authenticated app](https://docs.github.com/en/rest/apps/apps#get-an-installation-for-the-authenticated-app)
  - [Delete an installation for the authenticated app](https://docs.github.com/en/rest/apps/apps#delete-an-installation-for-the-authenticated-app)
  - [Create an installation access token for an app](https://docs.github.com/en/rest/apps/apps#create-an-installation-access-token-for-an-app)
  - [Suspend an app installation](https://docs.github.com/en/rest/apps/apps#suspend-an-app-installation)
  - [Unsuspend an app installation](https://docs.github.com/en/rest/apps/apps#unsuspend-an-app-installation)
  - [Create a scoped access token](https://docs.github.com/en/rest/apps/apps#create-a-scoped-access-token)
  - [Get an app](https://docs.github.com/en/rest/apps/apps#get-an-app)
  - [Get an organization installation for the authenticated app](https://docs.github.com/en/rest/apps/apps#get-an-organization-installation-for-the-authenticated-app)
  - [Get a repository installation for the authenticated app](https://docs.github.com/en/rest/apps/apps#get-a-repository-installation-for-the-authenticated-app)
  - [Get a user installation for the authenticated app](https://docs.github.com/en/rest/apps/apps#get-a-user-installation-for-the-authenticated-app)
- [REST API endpoints for GitHub App installations](https://docs.github.com/en/rest/apps/installations)
  - [List repositories accessible to the app installation](https://docs.github.com/en/rest/apps/installations#list-repositories-accessible-to-the-app-installation)
  - [Revoke an installation access token](https://docs.github.com/en/rest/apps/installations#revoke-an-installation-access-token)
  - [List app installations accessible to the user access token](https://docs.github.com/en/rest/apps/installations#list-app-installations-accessible-to-the-user-access-token)
  - [List repositories accessible to the user access token](https://docs.github.com/en/rest/apps/installations#list-repositories-accessible-to-the-user-access-token)
  - [Add a repository to an app installation](https://docs.github.com/en/rest/apps/installations#add-a-repository-to-an-app-installation)
  - [Remove a repository from an app installation](https://docs.github.com/en/rest/apps/installations#remove-a-repository-from-an-app-installation)
- [REST API endpoints for GitHub Marketplace](https://docs.github.com/en/rest/apps/marketplace)
  - [Get a subscription plan for an account](https://docs.github.com/en/rest/apps/marketplace#get-a-subscription-plan-for-an-account)
  - [List plans](https://docs.github.com/en/rest/apps/marketplace#list-plans)
  - [List accounts for a plan](https://docs.github.com/en/rest/apps/marketplace#list-accounts-for-a-plan)
  - [Get a subscription plan for an account (stubbed)](https://docs.github.com/en/rest/apps/marketplace#get-a-subscription-plan-for-an-account-stubbed)
  - [List plans (stubbed)](https://docs.github.com/en/rest/apps/marketplace#list-plans-stubbed)
  - [List accounts for a plan (stubbed)](https://docs.github.com/en/rest/apps/marketplace#list-accounts-for-a-plan-stubbed)
  - [List subscriptions for the authenticated user](https://docs.github.com/en/rest/apps/marketplace#list-subscriptions-for-the-authenticated-user)
  - [List subscriptions for the authenticated user (stubbed)](https://docs.github.com/en/rest/apps/marketplace#list-subscriptions-for-the-authenticated-user-stubbed)
- [REST API endpoints for OAuth authorizations](https://docs.github.com/en/rest/apps/oauth-applications)
  - [Delete an app authorization](https://docs.github.com/en/rest/apps/oauth-applications#delete-an-app-authorization)
  - [Check a token](https://docs.github.com/en/rest/apps/oauth-applications#check-a-token)
  - [Reset a token](https://docs.github.com/en/rest/apps/oauth-applications#reset-a-token)
  - [Delete an app token](https://docs.github.com/en/rest/apps/oauth-applications#delete-an-app-token)
- [REST API endpoints for GitHub App webhooks](https://docs.github.com/en/rest/apps/webhooks)
  - [Get a webhook configuration for an app](https://docs.github.com/en/rest/apps/webhooks#get-a-webhook-configuration-for-an-app)
  - [Update a webhook configuration for an app](https://docs.github.com/en/rest/apps/webhooks#update-a-webhook-configuration-for-an-app)
  - [List deliveries for an app webhook](https://docs.github.com/en/rest/apps/webhooks#list-deliveries-for-an-app-webhook)
  - [Get a delivery for an app webhook](https://docs.github.com/en/rest/apps/webhooks#get-a-delivery-for-an-app-webhook)
  - [Redeliver a delivery for an app webhook](https://docs.github.com/en/rest/apps/webhooks#redeliver-a-delivery-for-an-app-webhook)

---

# Authenticating to the REST API

> Learn how to authenticate your REST API requests.

# Authenticating to the REST API

Learn how to authenticate your REST API requests.

- [Authenticating to the REST API](https://docs.github.com/en/rest/authentication/authenticating-to-the-rest-api)
- [Keeping your API credentials secure](https://docs.github.com/en/rest/authentication/keeping-your-api-credentials-secure)
- [Endpoints available for GitHub App installation access tokens](https://docs.github.com/en/rest/authentication/endpoints-available-for-github-app-installation-access-tokens)
- [Endpoints available for GitHub App user access tokens](https://docs.github.com/en/rest/authentication/endpoints-available-for-github-app-user-access-tokens)
- [Endpoints available for fine-grained personal access tokens](https://docs.github.com/en/rest/authentication/endpoints-available-for-fine-grained-personal-access-tokens)
- [Permissions required for GitHub Apps](https://docs.github.com/en/rest/authentication/permissions-required-for-github-apps)
- [Permissions required for fine-grained personal access tokens](https://docs.github.com/en/rest/authentication/permissions-required-for-fine-grained-personal-access-tokens)

---

# REST API endpoints for billing

> Use the REST API to get billing information.

The REST API is now versioned. For more information, see "[About API versioning](https://docs.github.com/rest/overview/api-versions)."

# REST API endpoints for billing

Use the REST API to get billing information.

- [Budgets](https://docs.github.com/en/rest/billing/budgets)
  - [Get all budgets for an organization](https://docs.github.com/en/rest/billing/budgets#get-all-budgets-for-an-organization)
  - [Get a budget by ID for an organization](https://docs.github.com/en/rest/billing/budgets#get-a-budget-by-id-for-an-organization)
  - [Update a budget for an organization](https://docs.github.com/en/rest/billing/budgets#update-a-budget-for-an-organization)
  - [Delete a budget for an organization](https://docs.github.com/en/rest/billing/budgets#delete-a-budget-for-an-organization)
- [Billing usage](https://docs.github.com/en/rest/billing/usage)
  - [Get billing premium request usage report for an organization](https://docs.github.com/en/rest/billing/usage#get-billing-premium-request-usage-report-for-an-organization)
  - [Get billing usage report for an organization](https://docs.github.com/en/rest/billing/usage#get-billing-usage-report-for-an-organization)
  - [Get billing usage summary for an organization](https://docs.github.com/en/rest/billing/usage#get-billing-usage-summary-for-an-organization)
  - [Get billing premium request usage report for a user](https://docs.github.com/en/rest/billing/usage#get-billing-premium-request-usage-report-for-a-user)
  - [Get billing usage report for a user](https://docs.github.com/en/rest/billing/usage#get-billing-usage-report-for-a-user)
  - [Get billing usage summary for a user](https://docs.github.com/en/rest/billing/usage#get-billing-usage-summary-for-a-user)

---

# REST API endpoints for branches and their settings

> Use the REST API to modify branches and their protection settings.

The REST API is now versioned. For more information, see "[About API versioning](https://docs.github.com/rest/overview/api-versions)."

# REST API endpoints for branches and their settings

Use the REST API to modify branches and their protection settings.

- [REST API endpoints for branches](https://docs.github.com/en/rest/branches/branches)
  - [List branches](https://docs.github.com/en/rest/branches/branches#list-branches)
  - [Get a branch](https://docs.github.com/en/rest/branches/branches#get-a-branch)
  - [Rename a branch](https://docs.github.com/en/rest/branches/branches#rename-a-branch)
  - [Sync a fork branch with the upstream repository](https://docs.github.com/en/rest/branches/branches#sync-a-fork-branch-with-the-upstream-repository)
  - [Merge a branch](https://docs.github.com/en/rest/branches/branches#merge-a-branch)
- [REST API endpoints for protected branches](https://docs.github.com/en/rest/branches/branch-protection)
  - [Get branch protection](https://docs.github.com/en/rest/branches/branch-protection#get-branch-protection)
  - [Update branch protection](https://docs.github.com/en/rest/branches/branch-protection#update-branch-protection)
  - [Delete branch protection](https://docs.github.com/en/rest/branches/branch-protection#delete-branch-protection)
  - [Get admin branch protection](https://docs.github.com/en/rest/branches/branch-protection#get-admin-branch-protection)
  - [Set admin branch protection](https://docs.github.com/en/rest/branches/branch-protection#set-admin-branch-protection)
  - [Delete admin branch protection](https://docs.github.com/en/rest/branches/branch-protection#delete-admin-branch-protection)
  - [Get pull request review protection](https://docs.github.com/en/rest/branches/branch-protection#get-pull-request-review-protection)
  - [Update pull request review protection](https://docs.github.com/en/rest/branches/branch-protection#update-pull-request-review-protection)
  - [Delete pull request review protection](https://docs.github.com/en/rest/branches/branch-protection#delete-pull-request-review-protection)
  - [Get commit signature protection](https://docs.github.com/en/rest/branches/branch-protection#get-commit-signature-protection)
  - [Create commit signature protection](https://docs.github.com/en/rest/branches/branch-protection#create-commit-signature-protection)
  - [Delete commit signature protection](https://docs.github.com/en/rest/branches/branch-protection#delete-commit-signature-protection)
  - [Get status checks protection](https://docs.github.com/en/rest/branches/branch-protection#get-status-checks-protection)
  - [Update status check protection](https://docs.github.com/en/rest/branches/branch-protection#update-status-check-protection)
  - [Remove status check protection](https://docs.github.com/en/rest/branches/branch-protection#remove-status-check-protection)
  - [Get all status check contexts](https://docs.github.com/en/rest/branches/branch-protection#get-all-status-check-contexts)
  - [Add status check contexts](https://docs.github.com/en/rest/branches/branch-protection#add-status-check-contexts)
  - [Set status check contexts](https://docs.github.com/en/rest/branches/branch-protection#set-status-check-contexts)
  - [Remove status check contexts](https://docs.github.com/en/rest/branches/branch-protection#remove-status-check-contexts)
  - [Get access restrictions](https://docs.github.com/en/rest/branches/branch-protection#get-access-restrictions)
  - [Delete access restrictions](https://docs.github.com/en/rest/branches/branch-protection#delete-access-restrictions)
  - [Get apps with access to the protected branch](https://docs.github.com/en/rest/branches/branch-protection#get-apps-with-access-to-the-protected-branch)
  - [Add app access restrictions](https://docs.github.com/en/rest/branches/branch-protection#add-app-access-restrictions)
  - [Set app access restrictions](https://docs.github.com/en/rest/branches/branch-protection#set-app-access-restrictions)
  - [Remove app access restrictions](https://docs.github.com/en/rest/branches/branch-protection#remove-app-access-restrictions)
  - [Get teams with access to the protected branch](https://docs.github.com/en/rest/branches/branch-protection#get-teams-with-access-to-the-protected-branch)
  - [Add team access restrictions](https://docs.github.com/en/rest/branches/branch-protection#add-team-access-restrictions)
  - [Set team access restrictions](https://docs.github.com/en/rest/branches/branch-protection#set-team-access-restrictions)
  - [Remove team access restrictions](https://docs.github.com/en/rest/branches/branch-protection#remove-team-access-restrictions)
  - [Get users with access to the protected branch](https://docs.github.com/en/rest/branches/branch-protection#get-users-with-access-to-the-protected-branch)
  - [Add user access restrictions](https://docs.github.com/en/rest/branches/branch-protection#add-user-access-restrictions)
  - [Set user access restrictions](https://docs.github.com/en/rest/branches/branch-protection#set-user-access-restrictions)
  - [Remove user access restrictions](https://docs.github.com/en/rest/branches/branch-protection#remove-user-access-restrictions)

---

# REST API endpoints for security campaigns

> Use the REST API to create and manage security campaigns for your organization.

The REST API is now versioned. For more information, see "[About API versioning](https://docs.github.com/rest/overview/api-versions)."

# REST API endpoints for security campaigns

Use the REST API to create and manage security campaigns for your organization.

- [REST API endpoints for security campaigns](https://docs.github.com/en/rest/campaigns/campaigns)
  - [List campaigns for an organization](https://docs.github.com/en/rest/campaigns/campaigns#list-campaigns-for-an-organization)
  - [Create a campaign for an organization](https://docs.github.com/en/rest/campaigns/campaigns#create-a-campaign-for-an-organization)
  - [Get a campaign for an organization](https://docs.github.com/en/rest/campaigns/campaigns#get-a-campaign-for-an-organization)
  - [Update a campaign](https://docs.github.com/en/rest/campaigns/campaigns#update-a-campaign)
  - [Delete a campaign for an organization](https://docs.github.com/en/rest/campaigns/campaigns#delete-a-campaign-for-an-organization)

---

# REST API endpoints for checks

> Use the REST API to build GitHub Apps that run powerful checks against the code changes in a repository.

You can create apps that perform continuous integration, code linting, or code scanning services and provide detailed feedback on commits. For more information, see [Using the REST API to interact with checks](https://docs.github.com/en/rest/guides/using-the-rest-api-to-interact-with-checks) and [Building CI checks with a GitHub App](https://docs.github.com/en/apps/creating-github-apps/writing-code-for-a-github-app/building-ci-checks-with-a-github-app).

---

# REST API endpoints for GitHub Classroom

> Use the REST API to interact with GitHub Classroom.

The REST API is now versioned. For more information, see "[About API versioning](https://docs.github.com/rest/overview/api-versions)."

# REST API endpoints for GitHub Classroom

Use the REST API to interact with GitHub Classroom.

- [REST API endpoints for GitHub Classroom](https://docs.github.com/en/rest/classroom/classroom)
  - [Get an assignment](https://docs.github.com/en/rest/classroom/classroom#get-an-assignment)
  - [List accepted assignments for an assignment](https://docs.github.com/en/rest/classroom/classroom#list-accepted-assignments-for-an-assignment)
  - [Get assignment grades](https://docs.github.com/en/rest/classroom/classroom#get-assignment-grades)
  - [List classrooms](https://docs.github.com/en/rest/classroom/classroom#list-classrooms)
  - [Get a classroom](https://docs.github.com/en/rest/classroom/classroom#get-a-classroom)
  - [List assignments for a classroom](https://docs.github.com/en/rest/classroom/classroom#list-assignments-for-a-classroom)

---

# REST API endpoints for code scanning

> Use the REST API to retrieve and update code scanning alerts from a repository.

The REST API is now versioned. For more information, see "[About API versioning](https://docs.github.com/rest/overview/api-versions)."

# REST API endpoints for code scanning

Use the REST API to retrieve and update code scanning alerts from a repository.

- [REST API endpoints for code scanning](https://docs.github.com/en/rest/code-scanning/code-scanning)
  - [List code scanning alerts for an organization](https://docs.github.com/en/rest/code-scanning/code-scanning#list-code-scanning-alerts-for-an-organization)
  - [List code scanning alerts for a repository](https://docs.github.com/en/rest/code-scanning/code-scanning#list-code-scanning-alerts-for-a-repository)
  - [Get a code scanning alert](https://docs.github.com/en/rest/code-scanning/code-scanning#get-a-code-scanning-alert)
  - [Update a code scanning alert](https://docs.github.com/en/rest/code-scanning/code-scanning#update-a-code-scanning-alert)
  - [Get the status of an autofix for a code scanning alert](https://docs.github.com/en/rest/code-scanning/code-scanning#get-the-status-of-an-autofix-for-a-code-scanning-alert)
  - [Create an autofix for a code scanning alert](https://docs.github.com/en/rest/code-scanning/code-scanning#create-an-autofix-for-a-code-scanning-alert)
  - [Commit an autofix for a code scanning alert](https://docs.github.com/en/rest/code-scanning/code-scanning#commit-an-autofix-for-a-code-scanning-alert)
  - [List instances of a code scanning alert](https://docs.github.com/en/rest/code-scanning/code-scanning#list-instances-of-a-code-scanning-alert)
  - [List code scanning analyses for a repository](https://docs.github.com/en/rest/code-scanning/code-scanning#list-code-scanning-analyses-for-a-repository)
  - [Get a code scanning analysis for a repository](https://docs.github.com/en/rest/code-scanning/code-scanning#get-a-code-scanning-analysis-for-a-repository)
  - [Delete a code scanning analysis from a repository](https://docs.github.com/en/rest/code-scanning/code-scanning#delete-a-code-scanning-analysis-from-a-repository)
  - [List CodeQL databases for a repository](https://docs.github.com/en/rest/code-scanning/code-scanning#list-codeql-databases-for-a-repository)
  - [Get a CodeQL database for a repository](https://docs.github.com/en/rest/code-scanning/code-scanning#get-a-codeql-database-for-a-repository)
  - [Delete a CodeQL database](https://docs.github.com/en/rest/code-scanning/code-scanning#delete-a-codeql-database)
  - [Create a CodeQL variant analysis](https://docs.github.com/en/rest/code-scanning/code-scanning#create-a-codeql-variant-analysis)
  - [Get the summary of a CodeQL variant analysis](https://docs.github.com/en/rest/code-scanning/code-scanning#get-the-summary-of-a-codeql-variant-analysis)
  - [Get the analysis status of a repository in a CodeQL variant analysis](https://docs.github.com/en/rest/code-scanning/code-scanning#get-the-analysis-status-of-a-repository-in-a-codeql-variant-analysis)
  - [Get a code scanning default setup configuration](https://docs.github.com/en/rest/code-scanning/code-scanning#get-a-code-scanning-default-setup-configuration)
  - [Update a code scanning default setup configuration](https://docs.github.com/en/rest/code-scanning/code-scanning#update-a-code-scanning-default-setup-configuration)
  - [Upload an analysis as SARIF data](https://docs.github.com/en/rest/code-scanning/code-scanning#upload-an-analysis-as-sarif-data)
  - [Get information about a SARIF upload](https://docs.github.com/en/rest/code-scanning/code-scanning#get-information-about-a-sarif-upload)

---

# REST API endpoints for code security settings

> Use the REST API to create and manage code security configurations for your organization.

The REST API is now versioned. For more information, see "[About API versioning](https://docs.github.com/rest/overview/api-versions)."

# REST API endpoints for code security settings

Use the REST API to create and manage code security configurations for your organization.

- [Configurations](https://docs.github.com/en/rest/code-security/configurations)
  - [Get code security configurations for an enterprise](https://docs.github.com/en/rest/code-security/configurations#get-code-security-configurations-for-an-enterprise)
  - [Create a code security configuration for an enterprise](https://docs.github.com/en/rest/code-security/configurations#create-a-code-security-configuration-for-an-enterprise)
  - [Get default code security configurations for an enterprise](https://docs.github.com/en/rest/code-security/configurations#get-default-code-security-configurations-for-an-enterprise)
  - [Retrieve a code security configuration of an enterprise](https://docs.github.com/en/rest/code-security/configurations#retrieve-a-code-security-configuration-of-an-enterprise)
  - [Update a custom code security configuration for an enterprise](https://docs.github.com/en/rest/code-security/configurations#update-a-custom-code-security-configuration-for-an-enterprise)
  - [Delete a code security configuration for an enterprise](https://docs.github.com/en/rest/code-security/configurations#delete-a-code-security-configuration-for-an-enterprise)
  - [Attach an enterprise configuration to repositories](https://docs.github.com/en/rest/code-security/configurations#attach-an-enterprise-configuration-to-repositories)
  - [Set a code security configuration as a default for an enterprise](https://docs.github.com/en/rest/code-security/configurations#set-a-code-security-configuration-as-a-default-for-an-enterprise)
  - [Get repositories associated with an enterprise code security configuration](https://docs.github.com/en/rest/code-security/configurations#get-repositories-associated-with-an-enterprise-code-security-configuration)
  - [Get code security configurations for an organization](https://docs.github.com/en/rest/code-security/configurations#get-code-security-configurations-for-an-organization)
  - [Create a code security configuration](https://docs.github.com/en/rest/code-security/configurations#create-a-code-security-configuration)
  - [Get default code security configurations](https://docs.github.com/en/rest/code-security/configurations#get-default-code-security-configurations)
  - [Detach configurations from repositories](https://docs.github.com/en/rest/code-security/configurations#detach-configurations-from-repositories)
  - [Get a code security configuration](https://docs.github.com/en/rest/code-security/configurations#get-a-code-security-configuration)
  - [Update a code security configuration](https://docs.github.com/en/rest/code-security/configurations#update-a-code-security-configuration)
  - [Delete a code security configuration](https://docs.github.com/en/rest/code-security/configurations#delete-a-code-security-configuration)
  - [Attach a configuration to repositories](https://docs.github.com/en/rest/code-security/configurations#attach-a-configuration-to-repositories)
  - [Set a code security configuration as a default for an organization](https://docs.github.com/en/rest/code-security/configurations#set-a-code-security-configuration-as-a-default-for-an-organization)
  - [Get repositories associated with a code security configuration](https://docs.github.com/en/rest/code-security/configurations#get-repositories-associated-with-a-code-security-configuration)
  - [Get the code security configuration associated with a repository](https://docs.github.com/en/rest/code-security/configurations#get-the-code-security-configuration-associated-with-a-repository)

---

# REST API endpoints for codes of conduct

> Use the REST API to get information about codes of conduct.

The REST API is now versioned. For more information, see "[About API versioning](https://docs.github.com/rest/overview/api-versions)."

# REST API endpoints for codes of conduct

Use the REST API to get information about codes of conduct.

- [REST API endpoints for codes of conduct](https://docs.github.com/en/rest/codes-of-conduct/codes-of-conduct)
  - [Get all codes of conduct](https://docs.github.com/en/rest/codes-of-conduct/codes-of-conduct#get-all-codes-of-conduct)
  - [Get a code of conduct](https://docs.github.com/en/rest/codes-of-conduct/codes-of-conduct#get-a-code-of-conduct)

---

# REST API endpoints for Codespaces

> Use the REST API to manage GitHub Codespaces.

The REST API is now versioned. For more information, see "[About API versioning](https://docs.github.com/rest/overview/api-versions)."

# REST API endpoints for Codespaces

Use the REST API to manage GitHub Codespaces.

- [REST API endpoints for Codespaces](https://docs.github.com/en/rest/codespaces/codespaces)
  - [List codespaces in a repository for the authenticated user](https://docs.github.com/en/rest/codespaces/codespaces#list-codespaces-in-a-repository-for-the-authenticated-user)
  - [Create a codespace in a repository](https://docs.github.com/en/rest/codespaces/codespaces#create-a-codespace-in-a-repository)
  - [List devcontainer configurations in a repository for the authenticated user](https://docs.github.com/en/rest/codespaces/codespaces#list-devcontainer-configurations-in-a-repository-for-the-authenticated-user)
  - [Get default attributes for a codespace](https://docs.github.com/en/rest/codespaces/codespaces#get-default-attributes-for-a-codespace)
  - [Check if permissions defined by a devcontainer have been accepted by the authenticated user](https://docs.github.com/en/rest/codespaces/codespaces#check-if-permissions-defined-by-a-devcontainer-have-been-accepted-by-the-authenticated-user)
  - [Create a codespace from a pull request](https://docs.github.com/en/rest/codespaces/codespaces#create-a-codespace-from-a-pull-request)
  - [List codespaces for the authenticated user](https://docs.github.com/en/rest/codespaces/codespaces#list-codespaces-for-the-authenticated-user)
  - [Create a codespace for the authenticated user](https://docs.github.com/en/rest/codespaces/codespaces#create-a-codespace-for-the-authenticated-user)
  - [Get a codespace for the authenticated user](https://docs.github.com/en/rest/codespaces/codespaces#get-a-codespace-for-the-authenticated-user)
  - [Update a codespace for the authenticated user](https://docs.github.com/en/rest/codespaces/codespaces#update-a-codespace-for-the-authenticated-user)
  - [Delete a codespace for the authenticated user](https://docs.github.com/en/rest/codespaces/codespaces#delete-a-codespace-for-the-authenticated-user)
  - [Export a codespace for the authenticated user](https://docs.github.com/en/rest/codespaces/codespaces#export-a-codespace-for-the-authenticated-user)
  - [Get details about a codespace export](https://docs.github.com/en/rest/codespaces/codespaces#get-details-about-a-codespace-export)
  - [Create a repository from an unpublished codespace](https://docs.github.com/en/rest/codespaces/codespaces#create-a-repository-from-an-unpublished-codespace)
  - [Start a codespace for the authenticated user](https://docs.github.com/en/rest/codespaces/codespaces#start-a-codespace-for-the-authenticated-user)
  - [Stop a codespace for the authenticated user](https://docs.github.com/en/rest/codespaces/codespaces#stop-a-codespace-for-the-authenticated-user)
- [REST API endpoints for Codespaces machines](https://docs.github.com/en/rest/codespaces/machines)
  - [List available machine types for a repository](https://docs.github.com/en/rest/codespaces/machines#list-available-machine-types-for-a-repository)
  - [List machine types for a codespace](https://docs.github.com/en/rest/codespaces/machines#list-machine-types-for-a-codespace)
- [REST API endpoints for Codespaces organization secrets](https://docs.github.com/en/rest/codespaces/organization-secrets)
  - [List organization secrets](https://docs.github.com/en/rest/codespaces/organization-secrets#list-organization-secrets)
  - [Get an organization public key](https://docs.github.com/en/rest/codespaces/organization-secrets#get-an-organization-public-key)
  - [Get an organization secret](https://docs.github.com/en/rest/codespaces/organization-secrets#get-an-organization-secret)
  - [Create or update an organization secret](https://docs.github.com/en/rest/codespaces/organization-secrets#create-or-update-an-organization-secret)
  - [Delete an organization secret](https://docs.github.com/en/rest/codespaces/organization-secrets#delete-an-organization-secret)
  - [List selected repositories for an organization secret](https://docs.github.com/en/rest/codespaces/organization-secrets#list-selected-repositories-for-an-organization-secret)
  - [Set selected repositories for an organization secret](https://docs.github.com/en/rest/codespaces/organization-secrets#set-selected-repositories-for-an-organization-secret)
  - [Add selected repository to an organization secret](https://docs.github.com/en/rest/codespaces/organization-secrets#add-selected-repository-to-an-organization-secret)
  - [Remove selected repository from an organization secret](https://docs.github.com/en/rest/codespaces/organization-secrets#remove-selected-repository-from-an-organization-secret)
- [REST API endpoints for Codespaces organizations](https://docs.github.com/en/rest/codespaces/organizations)
  - [List codespaces for the organization](https://docs.github.com/en/rest/codespaces/organizations#list-codespaces-for-the-organization)
  - [Manage access control for organization codespaces](https://docs.github.com/en/rest/codespaces/organizations#manage-access-control-for-organization-codespaces)
  - [Add users to Codespaces access for an organization](https://docs.github.com/en/rest/codespaces/organizations#add-users-to-codespaces-access-for-an-organization)
  - [Remove users from Codespaces access for an organization](https://docs.github.com/en/rest/codespaces/organizations#remove-users-from-codespaces-access-for-an-organization)
  - [List codespaces for a user in organization](https://docs.github.com/en/rest/codespaces/organizations#list-codespaces-for-a-user-in-organization)
  - [Delete a codespace from the organization](https://docs.github.com/en/rest/codespaces/organizations#delete-a-codespace-from-the-organization)
  - [Stop a codespace for an organization user](https://docs.github.com/en/rest/codespaces/organizations#stop-a-codespace-for-an-organization-user)
- [REST API endpoints for Codespaces repository secrets](https://docs.github.com/en/rest/codespaces/repository-secrets)
  - [List repository secrets](https://docs.github.com/en/rest/codespaces/repository-secrets#list-repository-secrets)
  - [Get a repository public key](https://docs.github.com/en/rest/codespaces/repository-secrets#get-a-repository-public-key)
  - [Get a repository secret](https://docs.github.com/en/rest/codespaces/repository-secrets#get-a-repository-secret)
  - [Create or update a repository secret](https://docs.github.com/en/rest/codespaces/repository-secrets#create-or-update-a-repository-secret)
  - [Delete a repository secret](https://docs.github.com/en/rest/codespaces/repository-secrets#delete-a-repository-secret)
- [REST API endpoints for Codespaces user secrets](https://docs.github.com/en/rest/codespaces/secrets)
  - [List secrets for the authenticated user](https://docs.github.com/en/rest/codespaces/secrets#list-secrets-for-the-authenticated-user)
  - [Get public key for the authenticated user](https://docs.github.com/en/rest/codespaces/secrets#get-public-key-for-the-authenticated-user)
  - [Get a secret for the authenticated user](https://docs.github.com/en/rest/codespaces/secrets#get-a-secret-for-the-authenticated-user)
  - [Create or update a secret for the authenticated user](https://docs.github.com/en/rest/codespaces/secrets#create-or-update-a-secret-for-the-authenticated-user)
  - [Delete a secret for the authenticated user](https://docs.github.com/en/rest/codespaces/secrets#delete-a-secret-for-the-authenticated-user)
  - [List selected repositories for a user secret](https://docs.github.com/en/rest/codespaces/secrets#list-selected-repositories-for-a-user-secret)
  - [Set selected repositories for a user secret](https://docs.github.com/en/rest/codespaces/secrets#set-selected-repositories-for-a-user-secret)
  - [Add a selected repository to a user secret](https://docs.github.com/en/rest/codespaces/secrets#add-a-selected-repository-to-a-user-secret)
  - [Remove a selected repository from a user secret](https://docs.github.com/en/rest/codespaces/secrets#remove-a-selected-repository-from-a-user-secret)

---

# REST API endpoints for collaborators

> Use the REST API to add, invite, and remove collaborators from a repository.

The REST API is now versioned. For more information, see "[About API versioning](https://docs.github.com/rest/overview/api-versions)."

# REST API endpoints for collaborators

Use the REST API to add, invite, and remove collaborators from a repository.

- [REST API endpoints for collaborators](https://docs.github.com/en/rest/collaborators/collaborators)
  - [List repository collaborators](https://docs.github.com/en/rest/collaborators/collaborators#list-repository-collaborators)
  - [Check if a user is a repository collaborator](https://docs.github.com/en/rest/collaborators/collaborators#check-if-a-user-is-a-repository-collaborator)
  - [Add a repository collaborator](https://docs.github.com/en/rest/collaborators/collaborators#add-a-repository-collaborator)
  - [Remove a repository collaborator](https://docs.github.com/en/rest/collaborators/collaborators#remove-a-repository-collaborator)
  - [Get repository permissions for a user](https://docs.github.com/en/rest/collaborators/collaborators#get-repository-permissions-for-a-user)
- [REST API endpoints for repository invitations](https://docs.github.com/en/rest/collaborators/invitations)
  - [List repository invitations](https://docs.github.com/en/rest/collaborators/invitations#list-repository-invitations)
  - [Update a repository invitation](https://docs.github.com/en/rest/collaborators/invitations#update-a-repository-invitation)
  - [Delete a repository invitation](https://docs.github.com/en/rest/collaborators/invitations#delete-a-repository-invitation)
  - [List repository invitations for the authenticated user](https://docs.github.com/en/rest/collaborators/invitations#list-repository-invitations-for-the-authenticated-user)
  - [Accept a repository invitation](https://docs.github.com/en/rest/collaborators/invitations#accept-a-repository-invitation)
  - [Decline a repository invitation](https://docs.github.com/en/rest/collaborators/invitations#decline-a-repository-invitation)

---

# REST API endpoints for commits

> Use the REST API to interact with commits.

The REST API is now versioned. For more information, see "[About API versioning](https://docs.github.com/rest/overview/api-versions)."

# REST API endpoints for commits

Use the REST API to interact with commits.

- [REST API endpoints for commits](https://docs.github.com/en/rest/commits/commits)
  - [List commits](https://docs.github.com/en/rest/commits/commits#list-commits)
  - [List branches for HEAD commit](https://docs.github.com/en/rest/commits/commits#list-branches-for-head-commit)
  - [List pull requests associated with a commit](https://docs.github.com/en/rest/commits/commits#list-pull-requests-associated-with-a-commit)
  - [Get a commit](https://docs.github.com/en/rest/commits/commits#get-a-commit)
  - [Compare two commits](https://docs.github.com/en/rest/commits/commits#compare-two-commits)
- [REST API endpoints for commit comments](https://docs.github.com/en/rest/commits/comments)
  - [List commit comments for a repository](https://docs.github.com/en/rest/commits/comments#list-commit-comments-for-a-repository)
  - [Get a commit comment](https://docs.github.com/en/rest/commits/comments#get-a-commit-comment)
  - [Update a commit comment](https://docs.github.com/en/rest/commits/comments#update-a-commit-comment)
  - [Delete a commit comment](https://docs.github.com/en/rest/commits/comments#delete-a-commit-comment)
  - [List commit comments](https://docs.github.com/en/rest/commits/comments#list-commit-comments)
  - [Create a commit comment](https://docs.github.com/en/rest/commits/comments#create-a-commit-comment)
- [REST API endpoints for commit statuses](https://docs.github.com/en/rest/commits/statuses)
  - [Get the combined status for a specific reference](https://docs.github.com/en/rest/commits/statuses#get-the-combined-status-for-a-specific-reference)
  - [List commit statuses for a reference](https://docs.github.com/en/rest/commits/statuses#list-commit-statuses-for-a-reference)
  - [Create a commit status](https://docs.github.com/en/rest/commits/statuses#create-a-commit-status)

---

# REST API endpoints for Copilot

> Use the REST API to monitor and manage GitHub Copilot.

The REST API is now versioned. For more information, see "[About API versioning](https://docs.github.com/rest/overview/api-versions)."

# REST API endpoints for Copilot

Use the REST API to monitor and manage GitHub Copilot.

- [REST API endpoints for Copilot metrics](https://docs.github.com/en/rest/copilot/copilot-metrics)
  - [Get Copilot metrics for an organization](https://docs.github.com/en/rest/copilot/copilot-metrics#get-copilot-metrics-for-an-organization)
  - [Get Copilot metrics for a team](https://docs.github.com/en/rest/copilot/copilot-metrics#get-copilot-metrics-for-a-team)
- [REST API endpoints for Copilot user management](https://docs.github.com/en/rest/copilot/copilot-user-management)
  - [Get Copilot seat information and settings for an organization](https://docs.github.com/en/rest/copilot/copilot-user-management#get-copilot-seat-information-and-settings-for-an-organization)
  - [List all Copilot seat assignments for an organization](https://docs.github.com/en/rest/copilot/copilot-user-management#list-all-copilot-seat-assignments-for-an-organization)
  - [Add teams to the Copilot subscription for an organization](https://docs.github.com/en/rest/copilot/copilot-user-management#add-teams-to-the-copilot-subscription-for-an-organization)
  - [Remove teams from the Copilot subscription for an organization](https://docs.github.com/en/rest/copilot/copilot-user-management#remove-teams-from-the-copilot-subscription-for-an-organization)
  - [Add users to the Copilot subscription for an organization](https://docs.github.com/en/rest/copilot/copilot-user-management#add-users-to-the-copilot-subscription-for-an-organization)
  - [Remove users from the Copilot subscription for an organization](https://docs.github.com/en/rest/copilot/copilot-user-management#remove-users-from-the-copilot-subscription-for-an-organization)
  - [Get Copilot seat assignment details for a user](https://docs.github.com/en/rest/copilot/copilot-user-management#get-copilot-seat-assignment-details-for-a-user)

---

# Credentials

> Get started, troubleshoot, and make the most of GitHub. Documentation for new users, developers, administrators, and all of GitHub's products.

The REST API is now versioned. For more information, see "[About API versioning](https://docs.github.com/rest/overview/api-versions)."

# Credentials

- [Revocation](https://docs.github.com/en/rest/credentials/revoke)
  - [Revoke a list of credentials](https://docs.github.com/en/rest/credentials/revoke#revoke-a-list-of-credentials)

---

# REST API endpoints for Dependabot

> Use the REST API to interact with Dependabot alerts and secrets for an organization or repository.

The REST API is now versioned. For more information, see "[About API versioning](https://docs.github.com/rest/overview/api-versions)."

# REST API endpoints for Dependabot

Use the REST API to interact with Dependabot alerts and secrets for an organization or repository.

- [REST API endpoints for Dependabot alerts](https://docs.github.com/en/rest/dependabot/alerts)
  - [List Dependabot alerts for an enterprise](https://docs.github.com/en/rest/dependabot/alerts#list-dependabot-alerts-for-an-enterprise)
  - [List Dependabot alerts for an organization](https://docs.github.com/en/rest/dependabot/alerts#list-dependabot-alerts-for-an-organization)
  - [List Dependabot alerts for a repository](https://docs.github.com/en/rest/dependabot/alerts#list-dependabot-alerts-for-a-repository)
  - [Get a Dependabot alert](https://docs.github.com/en/rest/dependabot/alerts#get-a-dependabot-alert)
  - [Update a Dependabot alert](https://docs.github.com/en/rest/dependabot/alerts#update-a-dependabot-alert)
- [REST API endpoints for Dependabot repository access](https://docs.github.com/en/rest/dependabot/repository-access)
  - [Lists the repositories Dependabot can access in an organization](https://docs.github.com/en/rest/dependabot/repository-access#lists-the-repositories-dependabot-can-access-in-an-organization)
  - [Updates Dependabot's repository access list for an organization](https://docs.github.com/en/rest/dependabot/repository-access#updates-dependabots-repository-access-list-for-an-organization)
  - [Set the default repository access level for Dependabot](https://docs.github.com/en/rest/dependabot/repository-access#set-the-default-repository-access-level-for-dependabot)
- [REST API endpoints for Dependabot secrets](https://docs.github.com/en/rest/dependabot/secrets)
  - [List organization secrets](https://docs.github.com/en/rest/dependabot/secrets#list-organization-secrets)
  - [Get an organization public key](https://docs.github.com/en/rest/dependabot/secrets#get-an-organization-public-key)
  - [Get an organization secret](https://docs.github.com/en/rest/dependabot/secrets#get-an-organization-secret)
  - [Create or update an organization secret](https://docs.github.com/en/rest/dependabot/secrets#create-or-update-an-organization-secret)
  - [Delete an organization secret](https://docs.github.com/en/rest/dependabot/secrets#delete-an-organization-secret)
  - [List selected repositories for an organization secret](https://docs.github.com/en/rest/dependabot/secrets#list-selected-repositories-for-an-organization-secret)
  - [Set selected repositories for an organization secret](https://docs.github.com/en/rest/dependabot/secrets#set-selected-repositories-for-an-organization-secret)
  - [Add selected repository to an organization secret](https://docs.github.com/en/rest/dependabot/secrets#add-selected-repository-to-an-organization-secret)
  - [Remove selected repository from an organization secret](https://docs.github.com/en/rest/dependabot/secrets#remove-selected-repository-from-an-organization-secret)
  - [List repository secrets](https://docs.github.com/en/rest/dependabot/secrets#list-repository-secrets)
  - [Get a repository public key](https://docs.github.com/en/rest/dependabot/secrets#get-a-repository-public-key)
  - [Get a repository secret](https://docs.github.com/en/rest/dependabot/secrets#get-a-repository-secret)
  - [Create or update a repository secret](https://docs.github.com/en/rest/dependabot/secrets#create-or-update-a-repository-secret)
  - [Delete a repository secret](https://docs.github.com/en/rest/dependabot/secrets#delete-a-repository-secret)

---

# REST API endpoints for the dependency graph

> Use the REST API to view dependency changes and their security impact on your repository.

The REST API is now versioned. For more information, see "[About API versioning](https://docs.github.com/rest/overview/api-versions)."

# REST API endpoints for the dependency graph

Use the REST API to view dependency changes and their security impact on your repository.

- [REST API endpoints for dependency review](https://docs.github.com/en/rest/dependency-graph/dependency-review)
  - [Get a diff of the dependencies between commits](https://docs.github.com/en/rest/dependency-graph/dependency-review#get-a-diff-of-the-dependencies-between-commits)
- [REST API endpoints for dependency submission](https://docs.github.com/en/rest/dependency-graph/dependency-submission)
  - [Create a snapshot of dependencies for a repository](https://docs.github.com/en/rest/dependency-graph/dependency-submission#create-a-snapshot-of-dependencies-for-a-repository)
- [REST API endpoints for software bill of materials (SBOM)](https://docs.github.com/en/rest/dependency-graph/sboms)
  - [Export a software bill of materials (SBOM) for a repository.](https://docs.github.com/en/rest/dependency-graph/sboms#export-a-software-bill-of-materials-sbom-for-a-repository)

---

# REST API endpoints for deploy keys

> Use the REST API to create and manage deploy keys.

The REST API is now versioned. For more information, see "[About API versioning](https://docs.github.com/rest/overview/api-versions)."

# REST API endpoints for deploy keys

Use the REST API to create and manage deploy keys.

- [REST API endpoints for deploy keys](https://docs.github.com/en/rest/deploy-keys/deploy-keys)
  - [List deploy keys](https://docs.github.com/en/rest/deploy-keys/deploy-keys#list-deploy-keys)
  - [Create a deploy key](https://docs.github.com/en/rest/deploy-keys/deploy-keys#create-a-deploy-key)
  - [Get a deploy key](https://docs.github.com/en/rest/deploy-keys/deploy-keys#get-a-deploy-key)
  - [Delete a deploy key](https://docs.github.com/en/rest/deploy-keys/deploy-keys#delete-a-deploy-key)

---

# REST API endpoints for deployments

> Use the REST API to create and delete deploy keys, deployments, and deployment environments.

The REST API is now versioned. For more information, see "[About API versioning](https://docs.github.com/rest/overview/api-versions)."

# REST API endpoints for deployments

Use the REST API to create and delete deploy keys, deployments, and deployment environments.

- [REST API endpoints for deployments](https://docs.github.com/en/rest/deployments/deployments)
  - [List deployments](https://docs.github.com/en/rest/deployments/deployments#list-deployments)
  - [Create a deployment](https://docs.github.com/en/rest/deployments/deployments#create-a-deployment)
  - [Get a deployment](https://docs.github.com/en/rest/deployments/deployments#get-a-deployment)
  - [Delete a deployment](https://docs.github.com/en/rest/deployments/deployments#delete-a-deployment)
- [REST API endpoints for deployment branch policies](https://docs.github.com/en/rest/deployments/branch-policies)
  - [List deployment branch policies](https://docs.github.com/en/rest/deployments/branch-policies#list-deployment-branch-policies)
  - [Create a deployment branch policy](https://docs.github.com/en/rest/deployments/branch-policies#create-a-deployment-branch-policy)
  - [Get a deployment branch policy](https://docs.github.com/en/rest/deployments/branch-policies#get-a-deployment-branch-policy)
  - [Update a deployment branch policy](https://docs.github.com/en/rest/deployments/branch-policies#update-a-deployment-branch-policy)
  - [Delete a deployment branch policy](https://docs.github.com/en/rest/deployments/branch-policies#delete-a-deployment-branch-policy)
- [REST API endpoints for deployment environments](https://docs.github.com/en/rest/deployments/environments)
  - [List environments](https://docs.github.com/en/rest/deployments/environments#list-environments)
  - [Get an environment](https://docs.github.com/en/rest/deployments/environments#get-an-environment)
  - [Create or update an environment](https://docs.github.com/en/rest/deployments/environments#create-or-update-an-environment)
  - [Delete an environment](https://docs.github.com/en/rest/deployments/environments#delete-an-environment)
- [REST API endpoints for protection rules](https://docs.github.com/en/rest/deployments/protection-rules)
  - [Get all deployment protection rules for an environment](https://docs.github.com/en/rest/deployments/protection-rules#get-all-deployment-protection-rules-for-an-environment)
  - [Create a custom deployment protection rule on an environment](https://docs.github.com/en/rest/deployments/protection-rules#create-a-custom-deployment-protection-rule-on-an-environment)
  - [List custom deployment rule integrations available for an environment](https://docs.github.com/en/rest/deployments/protection-rules#list-custom-deployment-rule-integrations-available-for-an-environment)
  - [Get a custom deployment protection rule](https://docs.github.com/en/rest/deployments/protection-rules#get-a-custom-deployment-protection-rule)
  - [Disable a custom protection rule for an environment](https://docs.github.com/en/rest/deployments/protection-rules#disable-a-custom-protection-rule-for-an-environment)
- [REST API endpoints for deployment statuses](https://docs.github.com/en/rest/deployments/statuses)
  - [List deployment statuses](https://docs.github.com/en/rest/deployments/statuses#list-deployment-statuses)
  - [Create a deployment status](https://docs.github.com/en/rest/deployments/statuses#create-a-deployment-status)
  - [Get a deployment status](https://docs.github.com/en/rest/deployments/statuses#get-a-deployment-status)

---

# REST API endpoints for emojis

> Use the REST API to list and view all the available emojis to use on GitHub.

The REST API is now versioned. For more information, see "[About API versioning](https://docs.github.com/rest/overview/api-versions)."

# REST API endpoints for emojis

Use the REST API to list and view all the available emojis to use on GitHub.

- [REST API endpoints for emojis](https://docs.github.com/en/rest/emojis/emojis)
  - [Get emojis](https://docs.github.com/en/rest/emojis/emojis#get-emojis)

---

# Enterprise teams

> Use the REST API to create and manage enterprise teams in your GitHub enterprise.

The REST API is now versioned. For more information, see "[About API versioning](https://docs.github.com/rest/overview/api-versions)."

# Enterprise teams

Use the REST API to create and manage enterprise teams in your GitHub enterprise.

- [REST API endpoints for enterprise teams](https://docs.github.com/en/rest/enterprise-teams/enterprise-teams)
  - [List enterprise teams](https://docs.github.com/en/rest/enterprise-teams/enterprise-teams#list-enterprise-teams)
  - [Create an enterprise team](https://docs.github.com/en/rest/enterprise-teams/enterprise-teams#create-an-enterprise-team)
  - [Get an enterprise team](https://docs.github.com/en/rest/enterprise-teams/enterprise-teams#get-an-enterprise-team)
  - [Update an enterprise team](https://docs.github.com/en/rest/enterprise-teams/enterprise-teams#update-an-enterprise-team)
  - [Delete an enterprise team](https://docs.github.com/en/rest/enterprise-teams/enterprise-teams#delete-an-enterprise-team)
- [REST API endpoints for enterprise team memberships](https://docs.github.com/en/rest/enterprise-teams/enterprise-team-members)
  - [List members in an enterprise team](https://docs.github.com/en/rest/enterprise-teams/enterprise-team-members#list-members-in-an-enterprise-team)
  - [Bulk add team members](https://docs.github.com/en/rest/enterprise-teams/enterprise-team-members#bulk-add-team-members)
  - [Bulk remove team members](https://docs.github.com/en/rest/enterprise-teams/enterprise-team-members#bulk-remove-team-members)
  - [Get enterprise team membership](https://docs.github.com/en/rest/enterprise-teams/enterprise-team-members#get-enterprise-team-membership)
  - [Add team member](https://docs.github.com/en/rest/enterprise-teams/enterprise-team-members#add-team-member)
  - [Remove team membership](https://docs.github.com/en/rest/enterprise-teams/enterprise-team-members#remove-team-membership)
- [REST API endpoints for enterprise team organizations](https://docs.github.com/en/rest/enterprise-teams/enterprise-team-organizations)
  - [Get organization assignments](https://docs.github.com/en/rest/enterprise-teams/enterprise-team-organizations#get-organization-assignments)
  - [Add organization assignments](https://docs.github.com/en/rest/enterprise-teams/enterprise-team-organizations#add-organization-assignments)
  - [Remove organization assignments](https://docs.github.com/en/rest/enterprise-teams/enterprise-team-organizations#remove-organization-assignments)
  - [Get organization assignment](https://docs.github.com/en/rest/enterprise-teams/enterprise-team-organizations#get-organization-assignment)
  - [Add an organization assignment](https://docs.github.com/en/rest/enterprise-teams/enterprise-team-organizations#add-an-organization-assignment)
  - [Delete an organization assignment](https://docs.github.com/en/rest/enterprise-teams/enterprise-team-organizations#delete-an-organization-assignment)

---

# REST API endpoints for gists and gist comments

> Use the REST API to list, create, update and delete the public gists on GitHub.

The REST API is now versioned. For more information, see "[About API versioning](https://docs.github.com/rest/overview/api-versions)."

# REST API endpoints for gists and gist comments

Use the REST API to list, create, update and delete the public gists on GitHub.

- [REST API endpoints for gists](https://docs.github.com/en/rest/gists/gists)
  - [List gists for the authenticated user](https://docs.github.com/en/rest/gists/gists#list-gists-for-the-authenticated-user)
  - [Create a gist](https://docs.github.com/en/rest/gists/gists#create-a-gist)
  - [List public gists](https://docs.github.com/en/rest/gists/gists#list-public-gists)
  - [List starred gists](https://docs.github.com/en/rest/gists/gists#list-starred-gists)
  - [Get a gist](https://docs.github.com/en/rest/gists/gists#get-a-gist)
  - [Update a gist](https://docs.github.com/en/rest/gists/gists#update-a-gist)
  - [Delete a gist](https://docs.github.com/en/rest/gists/gists#delete-a-gist)
  - [List gist commits](https://docs.github.com/en/rest/gists/gists#list-gist-commits)
  - [List gist forks](https://docs.github.com/en/rest/gists/gists#list-gist-forks)
  - [Fork a gist](https://docs.github.com/en/rest/gists/gists#fork-a-gist)
  - [Check if a gist is starred](https://docs.github.com/en/rest/gists/gists#check-if-a-gist-is-starred)
  - [Star a gist](https://docs.github.com/en/rest/gists/gists#star-a-gist)
  - [Unstar a gist](https://docs.github.com/en/rest/gists/gists#unstar-a-gist)
  - [Get a gist revision](https://docs.github.com/en/rest/gists/gists#get-a-gist-revision)
  - [List gists for a user](https://docs.github.com/en/rest/gists/gists#list-gists-for-a-user)
- [REST API endpoints for gist comments](https://docs.github.com/en/rest/gists/comments)
  - [List gist comments](https://docs.github.com/en/rest/gists/comments#list-gist-comments)
  - [Create a gist comment](https://docs.github.com/en/rest/gists/comments#create-a-gist-comment)
  - [Get a gist comment](https://docs.github.com/en/rest/gists/comments#get-a-gist-comment)
  - [Update a gist comment](https://docs.github.com/en/rest/gists/comments#update-a-gist-comment)
  - [Delete a gist comment](https://docs.github.com/en/rest/gists/comments#delete-a-gist-comment)

---

# REST API endpoints for Git database

> Use the REST API to interact with raw Git objects in your Git database on GitHub and to list and update Git references (branch heads and tags).

## About Git database

The REST API gives you access to read and write raw Git objects to your Git database on GitHub and to list and update your references (branch heads and tags). For more information about using the REST API to interact with your Git database, see [Using the REST API to interact with your Git database](https://docs.github.com/en/rest/guides/using-the-rest-api-to-interact-with-your-git-database).

---

# REST API endpoints for gitignore

> Use the REST API to get .gitignore templates that can be used to ignore files and directories.

The REST API is now versioned. For more information, see "[About API versioning](https://docs.github.com/rest/overview/api-versions)."

# REST API endpoints for gitignore

Use the REST API to get `.gitignore` templates that can be used to ignore files and directories.

- [REST API endpoints for gitignore](https://docs.github.com/en/rest/gitignore/gitignore)
  - [Get all gitignore templates](https://docs.github.com/en/rest/gitignore/gitignore#get-all-gitignore-templates)
  - [Get a gitignore template](https://docs.github.com/en/rest/gitignore/gitignore#get-a-gitignore-template)

---

# Guides

> Learn about getting started with the REST API, authentication, and how to use the REST API for a variety of tasks.

This section of the documentation is intended to get you up-and-running with
real-world GitHub API applications. We'll go over everything you need to know, from authentication to results manipulation to integrating results with other apps.
Every tutorial will include a project, and each project will be saved and documented in our public
[platform-samples](https://github.com/github/platform-samples) repository.
