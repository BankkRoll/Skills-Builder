# REST API endpoints for organization migrations and more

# REST API endpoints for organization migrations

> Use the REST API to export one or more repositories so you can move them to  GitHub Enterprise Server.

## About organization migrations

These endpoints are only available to authenticated organization owners. For more information, see [Roles in an organization](https://docs.github.com/en/organizations/managing-peoples-access-to-your-organization-with-roles/roles-in-an-organization#permission-levels-for-an-organization) and [Authenticating to the REST API](https://docs.github.com/en/rest/overview/authenticating-to-the-rest-api).

You can use these endpoints to export one or more repositories so you can move them to a GitHub Enterprise Server instance. For more information, see [Exporting migration data from GitHub.com](https://docs.github.com/en/migrations/using-ghe-migrator/exporting-migration-data-from-githubcom).

---

# REST API endpoints for source imports

> Use the REST API to start an import from a Git source repository.

## About source imports

Warning

Due to very low levels of usage and available alternatives, the Source Imports API has been retired. For more details and alternatives, see the [changelog](https://gh.io/source-imports-api-deprecation).

You can use these endpoints to start an import from a Git repository hosted with another service. This is the same functionality as the GitHub Importer. For more information, see [Importing a repository with GitHub Importer](https://docs.github.com/en/migrations/importing-source-code/using-github-importer/importing-a-repository-with-github-importer). A typical source import would start the import and then (optionally) update the authors and/or update the preference for using Git LFS if large files exist in the import. You can also create a webhook that listens for the [RepositoryImportEvent](https://docs.github.com/en/webhooks-and-events/webhooks/webhook-events-and-payloads#repository_import) to find out the status of the import.

Note

These endpoints only support authentication using a personal access token (classic). For more information, see [Managing your personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token).

The following diagram provides a more detailed example:

```text
+---------+                     +--------+                              +---------------------+
| Tooling |                     | GitHub |                              | Original Repository |
+---------+                     +--------+                              +---------------------+
     |                              |                                              |
     |  Start import                |                                              |
     |----------------------------->|                                              |
     |                              |                                              |
     |                              |  Download source data                        |
     |                              |--------------------------------------------->|
     |                              |                        Begin streaming data  |
     |                              |<---------------------------------------------|
     |                              |                                              |
     |  Get import progress         |                                              |
     |----------------------------->|                                              |
     |       "status": "importing"  |                                              |
     |<-----------------------------|                                              |
     |                              |                                              |
     |  Get commit authors          |                                              |
     |----------------------------->|                                              |
     |                              |                                              |
     |  Map a commit author         |                                              |
     |----------------------------->|                                              |
     |                              |                                              |
     |                              |                                              |
     |                              |                       Finish streaming data  |
     |                              |<---------------------------------------------|
     |                              |                                              |
     |                              |  Rewrite commits with mapped authors         |
     |                              |------+                                       |
     |                              |      |                                       |
     |                              |<-----+                                       |
     |                              |                                              |
     |                              |  Update repository on GitHub                 |
     |                              |------+                                       |
     |                              |      |                                       |
     |                              |<-----+                                       |
     |                              |                                              |
     |  Map a commit author         |                                              |
     |----------------------------->|                                              |
     |                              |  Rewrite commits with mapped authors         |
     |                              |------+                                       |
     |                              |      |                                       |
     |                              |<-----+                                       |
     |                              |                                              |
     |                              |  Update repository on GitHub                 |
     |                              |------+                                       |
     |                              |      |                                       |
     |                              |<-----+                                       |
     |                              |                                              |
     |  Get large files             |                                              |
     |----------------------------->|                                              |
     |                              |                                              |
     |  opt_in to Git LFS           |                                              |
     |----------------------------->|                                              |
     |                              |  Rewrite commits for large files             |
     |                              |------+                                       |
     |                              |      |                                       |
     |                              |<-----+                                       |
     |                              |                                              |
     |                              |  Update repository on GitHub                 |
     |                              |------+                                       |
     |                              |      |                                       |
     |                              |<-----+                                       |
     |                              |                                              |
     |  Get import progress         |                                              |
     |----------------------------->|                                              |
     |        "status": "complete"  |                                              |
     |<-----------------------------|                                              |
     |                              |                                              |
     |                              |                                              |
```

---

# REST API endpoints for user migrations

> Use the REST API to review, backup, or migrate your user data stored on GitHub.

## About user migrations

These endpoints are only available to authenticated account owners. For more information, see [Authenticating to the REST API](https://docs.github.com/en/rest/overview/authenticating-to-the-rest-api).

You can use these endpoints to review, backup, or migrate your user data stored on GitHub.com. For a list of migration data that you can download, see [Download a user migration archive](#download-a-user-migration-archive).

To download an archive, you'll need to start a user migration first. Once the status of the migration is `exported`, you can download the migration.

Once you've created a migration archive, it will be available to download for seven days. But, you can delete the user migration archive sooner if you'd like. You can unlock your repository when the migration is `exported` to begin using your repository again or delete the repository if you no longer need the source data.
