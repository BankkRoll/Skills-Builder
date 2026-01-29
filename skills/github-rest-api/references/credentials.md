# Revocation

# Revocation

> Use the REST API to revoke credentials that you have found exposed on GitHub or elsewhere.

## Revoke a list of credentials

Submit a list of credentials to be revoked. This endpoint is intended to revoke credentials the caller does not own and may have found exposed on GitHub.com or elsewhere. It can also be used for credentials associated with an old user account that you no longer have access to. Credential owners will be notified of the revocation.

This endpoint currently accepts the following credential types:

- Personal access tokens (classic)
- Fine-grained personal access tokens

Revoked credentials may impact users on GitHub Free, Pro, & Team and GitHub Enterprise Cloud, and GitHub Enterprise Cloud with Enterprise Managed Users.
GitHub cannot reactivate any credentials that have been revoked; new credentials will need to be generated.

To prevent abuse, this API is limited to only 60 unauthenticated requests per hour and a max of 1000 tokens per API request.

Note

Any authenticated requests will return a 403.

### Fine-grained access tokens for "Revoke a list of credentials"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token does not require any permissions.

### Parameters for "Revoke a list of credentials"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| credentialsarray of stringsRequiredA list of credentials to be revoked, up to 1000 per request. |

### HTTP response status codes for "Revoke a list of credentials"

| Status code | Description |
| --- | --- |
| 202 | Accepted |
| 422 | Validation failed, or the endpoint has been spammed. |
| 500 | Internal Error |

### Code samples for "Revoke a list of credentials"

#### Request example

post/credentials/revoke

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/credentials/revoke \
  -d '{"credentials":["ghp_1234567890abcdef1234567890abcdef12345678","ghp_abcdef1234567890abcdef1234567890abcdef12"]}'`

Accepted

-
-

`Status: 202`
