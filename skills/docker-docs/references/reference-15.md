# Docker HUB API(2

# Docker HUB API(2

> Reference documentation and Swagger (OpenAPI) specification for the Docker Hub API.

- General
  - Changelog
  - Resources
  - Rate Limiting
  - Authentication
    - Types
      - Password
      - Personal Access Token (PAT)
      - Organization Access Token (OAT)
    - Labels
- API
  - Authentication
    - postCreate an authentication token
    - postSecond factor authentication
    - postCreate access token
  - Personal Access Tokens
    - postCreate personal access token
    - getList personal access tokens
    - patchUpdate personal access token
    - getGet personal access token
    - delDelete personal access token
  - Audit Logs
    - getList audit log actions
    - getList audit log events
  - Org Settings
    - getGet organization settings
    - putUpdate organization settings
  - Repositories
    - getList repository tags
    - headCheck repository tags
    - getRead repository tag
    - headCheck repository tag
    - patchUpdate repository immutable tags
    - postVerify repository immutable tags
    - postAssign a group (Team) to a repository for access
    - getList repositories in a namespace
    - postCreate a new repository
    - getGet repository in a namespace
    - headCheck repository in a namespace
  - SCIM
    - getGet service provider config
    - getList resource types
    - getGet a resource type
    - getList schemas
    - getGet a schema
    - getList users
    - postCreate user
    - getGet a user
    - putUpdate a user
  - Organizations
    - getList org members
    - getExport org members CSV
    - putUpdate org member (role)
    - delRemove member from org
  - Organization Access Tokens
    - postCreate access token
    - getList access tokens
    - getGet access token
    - patchUpdate access token
    - delDelete access token
  - Groups (Teams)
    - getGet groups of an organization
    - postCreate a new group
    - getGet a group of an organization
    - putUpdate the details for an organization group
    - patchUpdate some details for an organization group
    - delDelete an organization group
    - getList members of a group
    - postAdd a member to a group
    - delRemove a user from a group
  - Invites
    - getList org invites
    - delCancel an invite
    - patchResend an invite
    - postBulk create invites

[API docs by Redocly](https://redocly.com/redoc/)

# Docker HUB API(2-beta)

Download OpenAPI specification:[Download](https://docs.docker.com/reference/api/hub/latest.yaml)

Docker Hub is a service provided by Docker for finding and sharing container images with your team.

It is the world's largest library and community for container images.

In addition to the [Docker Hub UI](https://docs.docker.com/docker-hub/) and [Docker Hub CLI tool](https://github.com/docker/hub-tool#readme) (currently experimental), Docker provides an API that allows you to interact with Docker Hub.

Browse through the Docker Hub API documentation to explore the supported endpoints.

## Changelog

See the [Changelog](https://docs.docker.com/reference/api/hub/changelog) for a summary of changes across Docker Hub API versions.

## Resources

The following resources are available to interact with the documented API:

- [Docker Hub CLI tool](https://github.com/docker/hub-tool#readme) (currently experimental)

## Rate Limiting

The Docker Hub API is limited on the amount of requests you can perform per minute against it.

If you haven't hit the limit, each request to the API will return the following headers in the response.

- `X-RateLimit-Limit` - The limit of requests per minute.
- `X-RateLimit-Remaining` - The remaining amount of calls within the limit period.
- `X-RateLimit-Reset` - The unix timestamp of when the remaining resets.

If you have hit the limit, you will receive a response status of `429` and the `Retry-After` header in the response.

The [Retry-Afterheader](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Retry-After) specifies the number of seconds to wait until you can call the API again.

**Note**: These rate limits are separate from anti-abuse and Docker Hub download, or pull rate limiting.
To learn more about Docker Hub pull rate limiting, see [Usage and limits](https://docs.docker.com/docker-hub/usage/).

## Authentication

Most Docker Hub API endpoints require you to authenticate using your Docker credentials before using them.

Additionally, similar to the Docker Hub UI features, API endpoint responses may vary depending on your subscription (Personal, Pro, or Team) and your account's permissions.

To learn more about the features available in each subscription and to upgrade your existing subscription, see [Docker Pricing](https://www.docker.com/pricing).

## Types

The Docker Hub API supports the following authentication types.

You must use each authentication type with the [Create access token](#tag/authentication-api/operation/AuthCreateAccessToken) route to obtain a bearer token.

## Password

Using a username and password is the most powerful, yet least secure way
to authenticate with Docker as a user. It allows access to resources
for the user without scopes.

*In general, it is recommended to use a personal access token (PAT) instead.*

*The password authentication type is not available if your organization has SSO enforced.*

## Personal Access Token (PAT)

Using a username and PAT is the most secure way to authenticate with
Docker as a user. PATs are scoped to specific resources and scopes.

Currently, a PAT is a more secure password due to limited functionality.
In the future, we may add fine-grained access like organization
access tokens for enhanced usage and security.

## Organization Access Token (OAT)

Organization access tokens are scoped to specific resources and scopes
in an organization. They are managed by organization owners.

These tokens are meant for automation and are not meant to be used by
users.

## Labels

These labels will show up on routes in this reference that allow for use of bearer
tokens issued from them.

## Authentication

The authentication endpoints allow you to authenticate with Docker Hub APIs.

For more information, see [Authentication](#tag/authentication).

## Create an authentication tokenDeprecated

Creates and returns a bearer token in JWT format that you can use to authenticate with Docker Hub APIs.

The returned token is used in the HTTP Authorization header like `Authorization: Bearer {TOKEN}`.

*As of September 16, 2024, this route requires a personal access token (PAT) instead of a password if your organization has SSO enforced.*

  **Deprecated**: Use [[Create access token](#tag/authentication-api/operation/AuthCreateAccessToken)] instead.

##### Request Body schema:application/jsonrequired

Login details.

| usernamerequired | stringThe username of the Docker Hub account to authenticate with. |
| --- | --- |
| passwordrequired | stringThe password or personal access token (PAT) of the Docker Hub account to authenticate with. |

### Responses

### Request samples

- Payload

Content typeapplication/json`{"username": "myusername","password": "p@ssw0rd"}`

### Response samples

- 200
- 401

Content typeapplication/json`{"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"}`

## Second factor authentication

When a user has two-factor authentication (2FA) enabled, this is the second call to perform after `/v2/users/login` call.

Creates and returns a bearer token in JWT format that you can use to authenticate with Docker Hub APIs.

The returned token is used in the HTTP Authorization header like `Authorization: Bearer {TOKEN}`.

Most Docker Hub APIs require this token either to consume or to get detailed information. For example, to list images in a private repository.

##### Request Body schema:application/jsonrequired

Login details.

| login_2fa_tokenrequired | stringThe intermediate 2FA token returned from/v2/users/loginAPI. |
| --- | --- |
| coderequired | stringThe Time-based One-Time Password of the Docker Hub account to authenticate with. |

### Responses

### Request samples

- Payload

Content typeapplication/json`{"login_2fa_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c","code": 123456}`

### Response samples

- 200
- 401

Content typeapplication/json`{"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"}`

## Create access token

Creates and returns a short-lived access token in JWT format for use as a bearer when calling Docker APIs.

If successful, the access token returned should be used in the HTTP Authorization header like
`Authorization: Bearer {access_token}`.

*If your organization has SSO enforced, you must use a personal access token (PAT) instead of a password.*

##### Request Body schema:application/json

| identifierrequired | stringThe identifier of the account to create an access token for. If using a password or personal access token,
this must be a username. If using an organization access token, this must be an organization name. |
| --- | --- |
| secretrequired | stringThe secret of the account to create an access token for. This can be a password, personal access token, or
organization access token. |

### Responses

### Request samples

- Payload

Content typeapplication/json`{"identifier": "myusername","secret": "dckr_pat_124509ugsdjga93"}`

### Response samples

- 200
- 401

Content typeapplication/json`{"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"}`

## Personal Access Tokens

The Personal Access Token endpoints lets you manage personal access tokens. For more information, see [Access Tokens](https://docs.docker.com/security/access-tokens/).

You can use a personal access token instead of a password in the [Docker CLI](https://docs.docker.com/engine/reference/commandline/cli/) or in the [Create an authentication token](#operation/PostUsersLogin) route to obtain a bearer token.

### Scopes

For each scope grouping (in this case "repo"), you only need to define 1 scope as any lower scopes are assumed.
For example: If you define `repo:write`, the API assumes the scope of both `repo:read` *and* `repo:public_read` as well.
If you were to define both `repo:write` *and* `repo:read`, then `repo:read` is assumed by `repo:write` and ignored.

*Treat your personal access token like your password and keep it secret. You cannot retrieve your token after it is generated.*

## Create personal access token

Creates and returns a personal access token.

##### Authorizations:

*bearerAuth*

##### Request Body schema:application/jsonrequired

| token_labelrequired | string[ 1 .. 100 ] charactersFriendly name for you to identify the token. |
| --- | --- |
| scopesrequired | Array ofstringsValid scopes: "repo:admin", "repo:write", "repo:read", "repo:public_read" |
| expires_at | string<date-time>Optional expiration date for the token.
If omitted, the token will remain valid indefinitely. |

### Responses

### Request samples

- Payload

Content typeapplication/json`{"token_label": "My read only token","scopes": ["repo:read"],"expires_at": "2021-10-28T18:30:19.520861Z"}`

### Response samples

- 201
- 400
- 401

Content typeapplication/json`{"uuid": "b30bbf97-506c-4ecd-aabc-842f3cb484fb","client_id": "HUB","creator_ip": "127.0.0.1","creator_ua": "some user agent","created_at": "2021-07-20T12:00:00.000000Z","last_used": null,"generated_by": "manual","is_active": true,"token": "a7a5ef25-8889-43a0-8cc7-f2a94268e861","token_label": "My read only token","scopes": ["repo:read"],"expires_at": "2021-10-28T18:30:19.520861Z"}`

## List personal access tokens

Returns a paginated list of personal access tokens.

##### Authorizations:

*bearerAuth*

##### query Parameters

| page | numberDefault:1 |
| --- | --- |
| page_size | numberDefault:10 |

### Responses

### Response samples

- 200
- 400
- 401

Content typeapplication/json`{"count": 1,"next": null,"previous": null,"active_count": 1,"results": [{"uuid": "b30bbf97-506c-4ecd-aabc-842f3cb484fb","client_id": "HUB","creator_ip": "127.0.0.1","creator_ua": "some user agent","created_at": "2021-07-20T12:00:00.000000Z","last_used": null,"generated_by": "manual","is_active": true,"token": "","token_label": "My read only token","scopes": ["repo:read"],"expires_at": "2021-10-28T18:30:19.520861Z"}]}`

## Update personal access token

Updates a personal access token partially. You can either update the token's label or enable/disable it.

##### Authorizations:

*bearerAuth*

##### path Parameters

| uuidrequired | string |
| --- | --- |

##### Request Body schema:application/jsonrequired

| token_label | string[ 1 .. 100 ] characters |
| --- | --- |
| is_active | boolean |

### Responses

### Request samples

- Payload

Content typeapplication/json`{"token_label": "My read only token","is_active": false}`

### Response samples

- 200
- 400
- 401

Content typeapplication/json`{"uuid": "b30bbf97-506c-4ecd-aabc-842f3cb484fb","client_id": "HUB","creator_ip": "127.0.0.1","creator_ua": "some user agent","created_at": "2021-07-20T12:00:00.000000Z","last_used": null,"generated_by": "manual","is_active": true,"token": "a7a5ef25-8889-43a0-8cc7-f2a94268e861","token_label": "My read only token","scopes": ["repo:read"],"expires_at": "2021-10-28T18:30:19.520861Z"}`

## Get personal access token

Returns a personal access token by UUID.

##### Authorizations:

*bearerAuth*

##### path Parameters

| uuidrequired | string |
| --- | --- |

### Responses

### Response samples

- 200
- 401
- 404

Content typeapplication/json`{"uuid": "b30bbf97-506c-4ecd-aabc-842f3cb484fb","client_id": "HUB","creator_ip": "127.0.0.1","creator_ua": "some user agent","created_at": "2021-07-20T12:00:00.000000Z","last_used": null,"generated_by": "manual","is_active": true,"token": "","token_label": "My read only token","scopes": ["repo:read"],"expires_at": "2021-10-28T18:30:19.520861Z"}`

## Delete personal access token

Deletes a personal access token permanently. This cannot be undone.

##### Authorizations:

*bearerAuth*

##### path Parameters

| uuidrequired | string |
| --- | --- |

### Responses

### Response samples

- 401
- 404

Content typeapplication/json`{"detail": "string","message": "string"}`

## Audit Logs

The Audit Logs API endpoints allow you to query audit log events across a namespace.

For more information, see [Audit Logs](https://docs.docker.com/admin/organization/activity-logs/).

## List audit log actions

List audit log actions for a namespace to be used as a filter for querying audit log events.

##### Authorizations:

*bearerAuth*

##### path Parameters

| accountrequired | stringNamespace to query audit log actions for. |
| --- | --- |

### Responses

### Response samples

- 200
- 429
- 500
- default

Content typeapplication/json`{"actions": {"billing": {"actions": [{"name": "plan.upgrade","description": "Occurs when your organization’s billing plan is upgraded to a higher tier plan.","label": "Plan Upgraded"},{"name": "plan.downgrade","description": "Occurs when your organization’s billing plan is downgraded to a lower tier plan.","label": "Plan Downgraded"},{"name": "plan.seat_add","description": "Occurs when a seat is added to your organization’s billing plan.","label": "Seat Added"},{"name": "plan.seat_remove","description": "Occurs when a seat is removed from your organization’s billing plan.","label": "Seat Removed"},{"name": "plan.cycle_change","description": "Occurs when there is a change in the recurring interval that your organization is charged.","label": "Billing Cycle Changed"},{"name": "plan.downgrade_cancel","description": "Occurs when a scheduled plan downgrade for your organization is canceled.","label": "Plan Downgrade Canceled"},{"name": "plan.seat_removal_cancel","description": "Occurs when a scheduled seat removal for an organization’s billing plan is canceled.","label": "Seat Removal Canceled"},{"name": "plan.upgrade.request","description": "Occurs when a user in your organization requests a plan upgrade.","label": "Plan Upgrade Requested"},{"name": "plan.downgrade.request","description": "Occurs when a user in your organization requests a plan downgrade.","label": "Plan Downgrade Requested"},{"name": "plan.seat_add.request","description": "Occurs when a user in your organization requests an increase in the number of seats.","label": "Seat Addition Requested"},{"name": "plan.seat_removal.request","description": "Occurs when a user in your organization requests a decrease in the number of seats.","label": "Seat Removal Requested"},{"name": "plan.cycle_change.request","description": "Occurs when a user in your organization requests a change in the billing cycle.","label": "Billing Cycle Change Requested"},{"name": "plan.downgrade_cancel.request","description": "Occurs when a user in your organization requests a cancellation of a scheduled plan downgrade.","label": "Plan Downgrade Cancellation Requested"},{"name": "plan.seat_removal_cancel.request","description": "Occurs when a user in your organization requests a cancellation of a scheduled seat removal.","label": "Seat Removal Cancellation Requested"},{"name": "plan.product_change","description": "Occurs when there is a change in the product that your organization subscribes to.","label": "Billing Product Changed"}],"label": "Billing"},"enterprise": {"actions": [{"name": "setting.policy.create","description": "Details of adding an admin settings policy","label": "Policy created"},{"name": "setting.policy.update","description": "Details of updating an admin settings policy","label": "Policy updated"},{"name": "setting.policy.delete","description": "Details of deleting an admin settings policy","label": "Policy deleted"},{"name": "setting.policy.transfer","description": "Details of transferring an admin settings policy to another owner","label": "Policy transferred"},{"name": "sso.connection.create","description": "Details of creating a new org/company SSO connection","label": "Create SSO Connection"},{"name": "sso.connection.update","description": "Details of updating an existing org/company SSO connection","label": "Update SSO Connection"},{"name": "sso.connection.delete","description": "Details of deleting an existing org/company SSO connection","label": "Delete SSO Connection"},{"name": "sso.connection.enforcement_toggle","description": "Details of toggling enforcement on an existing org/company SSO connection","label": "Enforce SSO"},{"name": "sso.connection.scim_toggle","description": "Details of toggling SCIM on an existing org/company SSO connection","label": "Enforce SCIM"},{"name": "sso.connection.scim_token_refresh","description": "Details of a SCIM token refresh on an existing org/company SSO connection","label": "Refresh SCIM Token"},{"name": "sso.connection.connection_type_change","description": "Details of a connection type change on an existing org/company SSO connection","label": "Change SSO Connection Type"},{"name": "sso.connection.jit_toggle","description": "Details of a JIT toggle on an existing org/company SSO connection","label": "Toggle JIT provisioning"}],"label": "Enterprise"},"offload": {"actions": [{"name": "lease.start","description": "Details of the started Offload lease.","label": "Offload lease start"},{"name": "lease.end","description": "Details of the ended Offload lease.","label": "Offload lease end"}],"label": "Offload"},"oidc": {"actions": [{"name": "connection.create","description": "Details of creating an OIDC connection.","label": "OIDC connection created"},{"name": "connection.update","description": "Details of updating an OIDC connection.","label": "OIDC connection updated"},{"name": "connection.delete","description": "Details of deleting an OIDC connection.","label": "OIDC connection deleted"}],"label": "OIDC"},"org": {"actions": [{"name": "create","description": "Activities related to the creation of a new organization","label": "Organization Created"},{"name": "member.add","description": "Details of the member added to your organization","label": "Organization Member Added"},{"name": "member.remove","description": "Details about the member removed from your organization","label": "Organization Member Removed"},{"name": "member.role.change","description": "Details about the role changed for a member in your organization","label": "Member Role Changed"},{"name": "member.invite.send","description": "Details of the member invited to your organization","label": "Org Member Invited"},{"name": "team.create","description": "Activities related to the creation of a team","label": "Organization Created"},{"name": "team.update","description": "Activities related to the modification of a team","label": "Organization Deleted"},{"name": "team.delete","description": "Activities related to the deletion of a team","label": "Organization Deleted"},{"name": "team.member.add","description": "Details of the member added to your team","label": "Team Member Added"},{"name": "team.member.remove","description": "Details of the member removed from your team","label": "Team Member Removed"},{"name": "domain.create","description": "Details of the single sign-on domain added to your organization","label": "Single Sign-On domain added"},{"name": "domain.verify","description": "Details of the single sign-on domain verified for your organization","label": "Single Sign-On domain verified"},{"name": "domain.delete","description": "Details of the single sign-on domain removed from your organization","label": "Single Sign-On domain deleted"},{"name": "domain.auto-provisioning.toggle","description": "Details of toggling the Auto-Provisioning feature on a domain on or off","label": "Organization Auto-Provisioning Toggled"},{"name": "settings.update","description": "Details related to the organization setting that was updated","label": "Organization Settings Updated"},{"name": "registry_access.enabled","description": "Activities related to enabling Registry Access Management","label": "Registry Access Management enabled"},{"name": "registry_access.disabled","description": "Activities related to disabling Registry Access Management","label": "Registry Access Management disabled"},{"name": "registry_access.registry_added","description": "Activities related to the addition of a registry","label": "Registry Access Management registry added"},{"name": "registry_access.registry_updated","description": "Details related to the registry that was updated","label": "Registry Access Management registry updated"},{"name": "registry_access.registry_removed","description": "Activities related to the removal of a registry","label": "Registry Access Management registry removed"},{"name": "access_token.create","description": "Access token created in organization","label": "Access token created"},{"name": "access_token.update","description": "Access token updated in organization","label": "Access token updated"},{"name": "access_token.delete","description": "Access token deleted in organization","label": "Access token deleted"},{"name": "customrole.create","description": "A custom role was created","label": "Custom role created"},{"name": "customrole.update","description": "An existing custom role was updated","label": "Custom role updated"},{"name": "customrole.delete","description": "A custom role was deleted","label": "Custom role deleted"},{"name": "securepolicyconfigure.create","description": "A secure policy configuration was created","label": "Secure Policy Configuration created"},{"name": "securepolicyconfigure.update","description": "A secure policy configuration was updated","label": "Secure Policy Configuration updated"},{"name": "securepolicyconfigure.delete","description": "A secure policy configuration was deleted","label": "Secure Policy Configuration deleted"},{"name": "securepolicyclient.create","description": "A secure policy client was created","label": "Secure Policy Client created"},{"name": "securepolicyclient.update","description": "A secure policy client was updated","label": "Secure Policy Client updated"},{"name": "securepolicyclient.delete","description": "A secure policy client was deleted","label": "Secure Policy Client deleted"},{"name": "securepolicyprofile.create","description": "A secure policy profile was created","label": "Secure Policy Profile created"},{"name": "securepolicyprofile.update","description": "A secure policy profile was updated","label": "Secure Policy Profile updated"},{"name": "securepolicyprofile.delete","description": "A secure policy profile was deleted","label": "Secure Policy Profile deleted"}],"label": "Organization"},"repo": {"actions": [{"name": "create","description": "Activities related to the creation of a new repository","label": "Repository Created"},{"name": "update","description": "Activities related to the modification of a repository","label": "Repository Updated"},{"name": "delete","description": "Activities related to the deletion of a repository","label": "Repository Deleted"},{"name": "change_privacy","description": "Details related to the privacy policies that were updated","label": "Privacy Changed"},{"name": "category.updated","description": "Details related to updating a repository categories","label": "Categories updated"},{"name": "immutable.tags.updated","description": "Details related to updating tag immutability of a repository","label": "Tag immutability updated"},{"name": "tag.push","description": "Activities related to the tags pushed","label": "Tag Pushed"},{"name": "tag.delete","description": "Activities related to the tags deleted","label": "Tag Deleted"}],"label": "Repository"}}}`

## List audit log events

List audit log events for a given namespace.

##### Authorizations:

*bearerAuth*

##### path Parameters

| accountrequired | stringNamespace to query audit logs for. |
| --- | --- |

##### query Parameters

| action | stringaction name one of ["repo.tag.push", ...]. Optional parameter to filter specific audit log actions. |
| --- | --- |
| name | stringname. Optional parameter to filter audit log events to a specific name. For repository events, this is the name of the repository. For organization events, this is the name of the organization. For team member events, this is the username of the team member. |
| actor | stringactor name. Optional parameter to filter audit log events to the specific user who triggered the event. |
| from | string<date-time>Start of the time window you wish to query audit events for. |
| to | string<date-time>End of the time window you wish to query audit events for. |
| page | integer<int32>Default:1page - specify page number. Page number to get. |
| page_size | integer<int32>Default:25page_size - specify page size. Number of events to return per page. |

### Responses

### Response samples

- 200
- 429
- 500
- default

Content typeapplication/json`{"logs": [{"account": "docker","action": "repo.tag.push","name": "docker/example","actor": "docker","data": {"digest": "sha256:c1ae9c435032a276f80220c7d9b40f76266bbe79243d34f9cda30b76fe114dfa","tag": "latest"},"timestamp": "2021-02-19T01:34:35Z","action_description": "pushed the tag latest with the digest sha256:c1ae9c435032a to the repository docker/example\n"}]}`

## Org Settings

The Org Settings API endpoints allow you to manage your organization's settings.

## Get organization settings

Returns organization settings by name.

##### Authorizations:

*bearerAuth*

##### path Parameters

| namerequired | stringName of the organization. |
| --- | --- |

### Responses

### Response samples

- 200
- 401
- 403
- 404

Content typeapplication/json`{"restricted_images": {"enabled": true,"allow_official_images": true,"allow_verified_publishers": true}}`

## Update organization settings

Updates an organization's settings. Some settings are only used when the organization is on a business subscription.

*Only users with administrative privileges for the organization (owner role) can modify these settings.*

The following settings are only used on a business subscription:

- `restricted_images`

##### Authorizations:

*bearerAuth*

##### path Parameters

| namerequired | stringName of the organization. |
| --- | --- |

##### Request Body schema:application/jsonrequired

| required | object |
| --- | --- |

### Responses

### Request samples

- Payload

Content typeapplication/json`{"restricted_images": {"enabled": true,"allow_official_images": true,"allow_verified_publishers": true}}`

### Response samples

- 200
- 401
- 403
- 404

Content typeapplication/json`{"restricted_images": {"enabled": true,"allow_official_images": true,"allow_verified_publishers": true}}`

## Repositories

The repository endpoints allow you to access your repository's tags.

## List repository tags

##### Authorizations:

*bearerAuth*

##### path Parameters

| namespacerequired | string |
| --- | --- |
| repositoryrequired | string |

##### query Parameters

| page | integerPage number to get. Defaults to 1. |
| --- | --- |
| page_size | integerNumber of items to get per page. Defaults to 10. Max of 100. |

### Responses

### Response samples

- 200
- 403
- 404

Content typeapplication/json`{"count": 0,"next": "string","previous": "string","results": [{"id": 0,"images": {"architecture": "string","features": "string","variant": "string","digest": "string","layers": [{"digest": "string","size": 0,"instruction": "string"}],"os": "string","os_features": "string","os_version": "string","size": 0,"status": "active","last_pulled": "2021-01-05T21:06:53.506400Z","last_pushed": "2021-01-05T21:06:53.506400Z"},"creator": 0,"last_updated": "2021-01-05T21:06:53.506400Z","last_updater": 0,"last_updater_username": "string","name": "string","repository": 0,"full_size": 0,"v2": "string","status": "active","tag_last_pulled": "2021-01-05T21:06:53.506400Z","tag_last_pushed": "2021-01-05T21:06:53.506400Z"}]}`

## Check repository tags

##### Authorizations:

*bearerAuth*

##### path Parameters

| namespacerequired | string |
| --- | --- |
| repositoryrequired | string |

### Responses

### Response samples

- 403
- 404

Content typeapplication/json`{"detail": "string","message": "string"}`

## Read repository tag

##### Authorizations:

*bearerAuth*

##### path Parameters

| namespacerequired | string |
| --- | --- |
| repositoryrequired | string |
| tagrequired | string |

### Responses

### Response samples

- 200
- 403
- 404

Content typeapplication/json`{"id": 0,"images": {"architecture": "string","features": "string","variant": "string","digest": "string","layers": [{"digest": "string","size": 0,"instruction": "string"}],"os": "string","os_features": "string","os_version": "string","size": 0,"status": "active","last_pulled": "2021-01-05T21:06:53.506400Z","last_pushed": "2021-01-05T21:06:53.506400Z"},"creator": 0,"last_updated": "2021-01-05T21:06:53.506400Z","last_updater": 0,"last_updater_username": "string","name": "string","repository": 0,"full_size": 0,"v2": "string","status": "active","tag_last_pulled": "2021-01-05T21:06:53.506400Z","tag_last_pushed": "2021-01-05T21:06:53.506400Z"}`

## Check repository tag

##### Authorizations:

*bearerAuth*

##### path Parameters

| namespacerequired | string |
| --- | --- |
| repositoryrequired | string |
| tagrequired | string |

### Responses

### Response samples

- 403
- 404

Content typeapplication/json`{"detail": "string","message": "string"}`

## Update repository immutable tags

Updates the immutable tags configuration for this repository.

**Only users with administrative privileges for the repository can modify these settings.**

##### Authorizations:

*bearerAuth*

##### path Parameters

| namespacerequired | string |
| --- | --- |
| repositoryrequired | string |

##### Request Body schema:application/jsonrequired

| immutable_tagsrequired | booleanWhether immutable tags are enabled |
| --- | --- |
| immutable_tags_rulesrequired | Array ofstringsList of immutable tag rules |

### Responses

### Request samples

- Payload

Content typeapplication/json`{"immutable_tags": true,"immutable_tags_rules": ["v.*",".*-RELEASE"]}`

### Response samples

- 200
- 400
- 401
- 403
- 404

Content typeapplication/json`{"user": "string","name": "string","namespace": "string","repository_type": "string","status": 0,"status_description": "string","description": "string","is_private": true,"is_automated": true,"star_count": 0,"pull_count": 0,"last_updated": "2021-01-05T21:06:53.506400Z","last_modified": "2021-01-05T21:06:53.506400Z","date_registered": "2021-01-05T21:06:53.506400Z","collaborator_count": 0,"affiliation": "string","hub_user": "string","has_starred": true,"full_description": "string","permissions": {"read": true,"write": true,"admin": true},"media_types": ["string"],"content_types": ["string"],"categories": [{"name": "Databases","slug": "databases"}],"immutable_tags_settings": {"enabled": true,"rules": ["string"]},"storage_size": 0,"source": "string"}`

## Verify repository immutable tags

Validates  the immutable tags regex pass in parameter and returns a list of tags matching it in this repository.

**Only users with administrative privileges for the repository call this endpoint.**

##### Authorizations:

*bearerAuth*

##### path Parameters

| namespacerequired | string |
| --- | --- |
| repositoryrequired | string |

##### Request Body schema:application/jsonrequired

| regexrequired | string^[a-z0-9]+((\\.|_|__|-+)[a-z0-9]+)*(\\/[a-z0-...Immutable tags rule regex pattern. Must match format: [a-z0-9]+((\.||__|-+)[a-z0-9]+)*(\/[a-z0-9]+((\.||__|-+)[a-z0-9]+)) |
| --- | --- |

### Responses

### Request samples

- Payload

Content typeapplication/json`{"regex": "v.*"}`

### Response samples

- 200
- 400
- 401
- 403
- 404

Content typeapplication/json`{"tags": ["v1.0.0","v2.1.3","latest"]}`

## Assign a group (Team) to a repository for access

##### Authorizations:

*bearerAuth*

##### path Parameters

| namespacerequired | string |
| --- | --- |
| repositoryrequired | string |

##### Request Body schema:application/jsonrequired

| group_idrequired | integer<int64>The ID of the organization group to grant access to |
| --- | --- |
| permissionrequired | stringEnum:"read""write""admin"The permission level to grant to the group:read: Can view and pull from the repositorywrite: Can view, pull, and push to the repositoryadmin: Can view, pull, push, and manage repository settings |

### Responses

### Request samples

- Payload

Content typeapplication/json`{"group_id": 12345,"permission": "write"}`

### Response samples

- 200
- 400
- 401
- 403
- 404

Content typeapplication/json`{"group_name": "developers","permission": "write","group_id": 12345}`

## List repositories in a namespace

Returns a list of repositories within the specified namespace (organization or user).

Public repositories are accessible to everyone, while private repositories require appropriate authentication and permissions.

##### Authorizations:

*bearerAuth*None

##### path Parameters

| namespacerequired | string |
| --- | --- |

##### query Parameters

| page | integer>= 1Default:1Page number to get. Defaults to 1. |
| --- | --- |
| page_size | integer[ 1 .. 100 ]Default:10Number of repositories to get per page. Defaults to 10. Max of 100. |
| name | stringFilter repositories by name (partial match). |
| ordering | stringEnum:"name""-name""last_updated""-last_updated""pull_count""-pull_count"Order repositories by the specified field. Prefix with '-' for descending order.
Available options:name/-name: Repository name (ascending/descending)last_updated/-last_updated: Last update time (ascending/descending)pull_count/-pull_count: Number of pulls (ascending/descending) |

### Responses

### Response samples

- 200
- 400
- 401
- 403
- 404

Content typeapplication/json`{"count": 287,"next": "https://hub.docker.com/v2/namespaces/docker/repositories?page=2&page_size=2","previous": null,"results": [{"name": "highland_builder","namespace": "docker","repository_type": "image","status": 1,"status_description": "active","description": "Image for performing Docker build requests","is_private": false,"star_count": 7,"pull_count": 15722123,"last_updated": "2023-06-20T10:44:45.459826Z","last_modified": "2024-10-16T13:48:34.145251Z","date_registered": "2015-05-19T21:13:35.937763Z","affiliation": "","media_types": ["application/octet-stream","application/vnd.docker.container.image.v1+json","application/vnd.docker.distribution.manifest.v1+prettyjws"],"content_types": ["unrecognized","image"],"categories": [{"name": "Languages & frameworks","slug": "languages-and-frameworks"},{"name": "Integration & delivery","slug": "integration-and-delivery"},{"name": "Operating systems","slug": "operating-systems"}],"storage_size": 488723114800},{"name": "whalesay","namespace": "docker","repository_type": null,"status": 1,"status_description": "active","description": "An image for use in the Docker demo tutorial","is_private": false,"star_count": 757,"pull_count": 130737682,"last_updated": "2015-06-19T19:06:27.388123Z","last_modified": "2024-10-16T13:48:34.145251Z","date_registered": "2015-06-09T18:16:36.527329Z","affiliation": "","media_types": ["application/vnd.docker.distribution.manifest.v1+prettyjws"],"content_types": ["image"],"categories": [{"name": "Languages & frameworks","slug": "languages-and-frameworks"},{"name": "Integration & delivery","slug": "integration-and-delivery"}],"storage_size": 103666708}]}`

## Create a new repository

Creates a new repository within the specified namespace. The repository will be created
with the provided metadata including name, description, and privacy settings.

##### Authorizations:

None

##### path Parameters

| namespacerequired | string |
| --- | --- |

##### Request Body schema:application/jsonrequired

| namerequired | string[ 2 .. 255 ] characters^[a-z0-9]+(?:[._-][a-z0-9]+)*$The name of the repository. Must be 2-255 characters long and may only include
alphanumeric characters, periods (.), underscores (_), or hyphens (-).
Letters must be lowercase. |
| --- | --- |
| namespacerequired | stringThe namespace where the repository will be created |
| description | string<= 100 charactersShort description of the repository |
| full_description | string<= 25000 charactersDetailed description of the repository |
| registry | stringThe registry where the repository will be hosted |
| is_private | booleanDefault:falseWhether the repository should be private |

### Responses

### Request samples

- Payload

Content typeapplication/json`{"name": "my-app","namespace": "myorganization","description": "A sample application repository","full_description": "This is a comprehensive description of my application repository that contains additional details about the project.","registry": "docker.io","is_private": false}`

### Response samples

- 201
- 400
- 401
- 403
- 404
- 500

Content typeapplication/json`{"name": "my-app","namespace": "myorganization","repository_type": "image","status": 1,"status_description": "Active","description": "A sample application repository","is_private": false,"is_automated": false,"star_count": 0,"pull_count": 0,"last_updated": "2025-01-20T10:30:00Z","date_registered": "2025-01-20T10:30:00Z","collaborator_count": 0,"hub_user": "myorganization","has_starred": false,"full_description": "This is a comprehensive description of my application repository that contains additional details about the project.","media_types": [ ],"content_types": [ ],"categories": [ ],"immutable_tags_settings": {"enabled": false,"rules": [ ]},"storage_size": null,"source": null}`

## Get repository in a namespace

Returns a repository within the specified namespace (organization or user).

Public repositories are accessible to everyone, while private repositories require appropriate authentication and permissions.

##### Authorizations:

*bearerAuth*None

##### path Parameters

| namespacerequired | string |
| --- | --- |
| repositoryrequired | string |

### Responses

### Response samples

- 200
- 401
- 403
- 404
- 500

Content typeapplication/json`{"name": "my-app","namespace": "myorganization","repository_type": "image","status": 1,"status_description": "Active","description": "A sample application repository","is_private": false,"is_automated": false,"star_count": 0,"pull_count": 0,"last_updated": "2025-01-20T10:30:00Z","date_registered": "2025-01-20T10:30:00Z","collaborator_count": 0,"hub_user": "myorganization","has_starred": false,"full_description": "This is a comprehensive description of my application repository that contains additional details about the project.","media_types": [ ],"content_types": [ ],"categories": [ ],"immutable_tags_settings": {"enabled": false,"rules": [ ]},"storage_size": null,"source": null}`

## Check repository in a namespace

Check a repository within the specified namespace (organization or user).

Public repositories are accessible to everyone, while private repositories require appropriate authentication and permissions.

##### Authorizations:

*bearerAuth*None

##### path Parameters

| namespacerequired | string |
| --- | --- |
| repositoryrequired | string |

### Responses

### Response samples

- 200
- 401
- 403
- 404
- 500

Content typeapplication/json`{"name": "my-app","namespace": "myorganization","repository_type": "image","status": 1,"status_description": "Active","description": "A sample application repository","is_private": false,"is_automated": false,"star_count": 0,"pull_count": 0,"last_updated": "2025-01-20T10:30:00Z","date_registered": "2025-01-20T10:30:00Z","collaborator_count": 0,"hub_user": "myorganization","has_starred": false,"full_description": "This is a comprehensive description of my application repository that contains additional details about the project.","media_types": [ ],"content_types": [ ],"categories": [ ],"immutable_tags_settings": {"enabled": false,"rules": [ ]},"storage_size": null,"source": null}`

## SCIM

SCIM is a provisioning system that lets you manage users within your identity provider (IdP).

For more information, see [System for Cross-domain Identity management](https://docs.docker.com/security/for-admins/provisioning/scim/).

## Get service provider config

Returns a service provider config for Docker's configuration.

##### Authorizations:

*bearerSCIMAuth*

### Responses

### Response samples

- 200
- 401
- 500

Content typeapplication/scim+json`{"schemas": ["urn:ietf:params:scim:schemas:core:2.0:ServiceProviderConfig"],"documentationUri": "","patch": {"supported": false},"bulk": {"supported": false,"maxOperations": 0,"maxPayloadSize": 0},"filter": {"supported": true,"maxResults": 99999},"changePassword": {"supported": false},"sort": {"supported": true},"etag": {"supported": false},"authenticationSchemes": {"name": "OAuth 2.0 Bearer Token","description": "The OAuth 2.0 Bearer Token Authentication scheme. OAuth enables clients to access protected resources by obtaining an access token, which is defined in RFC 6750 as \"a string representing an access authorization issued to the client\", rather than using the resource owner's credentials directly.","specUri": "http://tools.ietf.org/html/rfc6750","type": "oauthbearertoken"}}`

## List resource types

Returns all resource types supported for the SCIM configuration.

##### Authorizations:

*bearerSCIMAuth*

### Responses

### Response samples

- 200
- 401
- 500

Content typeapplication/scim+json`{"schemas": ["urn:ietf:params:scim:api:messages:2.0:ListResponse"],"totalResults": 1,"resources": [{"schemas": ["urn:ietf:params:scim:schemas:core:2.0:ResourceType"],"id": "User","name": "User","description": "User","endpoint": "/Users","schema": "urn:ietf:params:scim:schemas:core:2.0:User"}]}`

## Get a resource type

Returns a resource type by name.

##### Authorizations:

*bearerSCIMAuth*

##### path Parameters

| namerequired | stringExample:User |
| --- | --- |

### Responses

### Response samples

- 200
- 401
- 404
- 500

Content typeapplication/scim+json`{"schemas": ["urn:ietf:params:scim:schemas:core:2.0:ResourceType"],"id": "User","name": "User","description": "User","endpoint": "/Users","schema": "urn:ietf:params:scim:schemas:core:2.0:User"}`

## List schemas

Returns all schemas supported for the SCIM configuration.

##### Authorizations:

*bearerSCIMAuth*

### Responses

### Response samples

- 200
- 401
- 500

Content typeapplication/scim+json`{"schemas": ["urn:ietf:params:scim:api:messages:2.0:ListResponse"],"totalResults": 1,"resources": [{"schemas": ["urn:ietf:params:scim:schemas:core:2.0:Schema"],"id": "urn:ietf:params:scim:schemas:core:2.0:User","name": "User","description": "User Account","attributes": [ ]}]}`

## Get a schema

Returns a schema by ID.

##### Authorizations:

*bearerSCIMAuth*

##### path Parameters

| idrequired | stringExample:urn:ietf:params:scim:schemas:core:2.0:User |
| --- | --- |

### Responses

### Response samples

- 200
- 401
- 404
- 500

Content typeapplication/scim+json`{"schemas": ["urn:ietf:params:scim:schemas:core:2.0:Schema"],"id": "urn:ietf:params:scim:schemas:core:2.0:User","name": "User","description": "User Account","attributes": [ ]}`

## List users

Returns paginated users for an organization. Use `startIndex` and `count` query parameters to receive paginated results.

**Sorting:**

Sorting allows you to specify the order in which resources are returned by specifying a combination of `sortBy` and `sortOrder` query parameters.

The `sortBy` parameter specifies the attribute whose value will be used to order the returned responses. The `sortOrder` parameter defines the order in which the `sortBy` parameter is applied. Allowed values are "ascending" and "descending".

**Filtering:**

You can request a subset of resources by specifying the `filter` query parameter containing a filter expression. Attribute names and attribute operators used in filters are case insensitive. The filter parameter must contain at least one valid expression. Each expression must contain an attribute name followed by an attribute operator and an optional value.

Supported operators are listed below.

- `eq` equal
- `ne` not equal
- `co` contains
- `sw` starts with
- `and` Logical "and"
- `or` Logical "or"
- `not` "Not" function
- `()` Precedence grouping

##### Authorizations:

*bearerSCIMAuth*

##### query Parameters

| startIndex | integer>= 1Example:startIndex=1 |
| --- | --- |
| count | integer[ 1 .. 200 ]Example:count=10 |
| filter | stringExample:filter=userName eq "jon.snow@docker.com" |
| attributes | stringExample:attributes=userName,displayNameComma delimited list of attributes to limit to in the response. |
| sortOrder | stringEnum:"ascending""descending" |
| sortBy | stringExample:sortBy=userNameUser attribute to sort by. |

### Responses

### Response samples

- 200
- 400
- 401
- 403
- 404
- 500

Content typeapplication/scim+json`{"schemas": ["urn:ietf:params:scim:api:messages:2.0:ListResponse"],"totalResults": 1,"startIndex": 1,"itemsPerPage": 10,"resources": [{"schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],"id": "d80f7c79-7730-49d8-9a41-7c42fb622d9c","userName": "jon.snow@docker.com","name": {"givenName": "Jon","familyName": "Snow"},"displayName": "jonsnow","active": true,"emails": [{"value": "jon.snow@docker.com","display": "jon.snow@docker.com","primary": true}],"groups": [{"value": "nightswatch","display": "nightswatch"}],"meta": {"resourceType": "User","location": "https://hub.docker.com/v2/scim/2.0/Users/d80f7c79-7730-49d8-9a41-7c42fb622d9c","created": "2022-05-20T00:54:18Z","lastModified": "2022-05-20T00:54:18Z"}}]}`

## Create user

Creates a user. If the user already exists by email, they are assigned to the organization on the "company" team.

##### Authorizations:

*bearerSCIMAuth*

##### Request Body schema:application/scim+jsonrequired

| schemasrequired | Array ofstrings(scim_user_schemas)[ itemsnon-empty] |
| --- | --- |
| userNamerequired | string(scim_user_username)The user's email address. This must be reachable via email. |
|  | object(scim_user_name) |

### Responses

### Request samples

- Payload

Content typeapplication/scim+json`{"schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],"userName": "jon.snow@docker.com","name": {"givenName": "Jon","familyName": "Snow"}}`

### Response samples

- 201
- 400
- 401
- 403
- 404
- 409
- 500

Content typeapplication/scim+json`{"schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],"id": "d80f7c79-7730-49d8-9a41-7c42fb622d9c","userName": "jon.snow@docker.com","name": {"givenName": "Jon","familyName": "Snow"},"displayName": "jonsnow","active": true,"emails": [{"value": "jon.snow@docker.com","display": "jon.snow@docker.com","primary": true}],"groups": [{"value": "nightswatch","display": "nightswatch"}],"meta": {"resourceType": "User","location": "https://hub.docker.com/v2/scim/2.0/Users/d80f7c79-7730-49d8-9a41-7c42fb622d9c","created": "2022-05-20T00:54:18Z","lastModified": "2022-05-20T00:54:18Z"}}`

## Get a user

Returns a user by ID.

##### Authorizations:

*bearerSCIMAuth*

##### path Parameters

| idrequired | stringExample:d80f7c79-7730-49d8-9a41-7c42fb622d9cThe user ID. |
| --- | --- |

### Responses

### Response samples

- 200
- 400
- 401
- 403
- 404
- 500

Content typeapplication/scim+json`{"schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],"id": "d80f7c79-7730-49d8-9a41-7c42fb622d9c","userName": "jon.snow@docker.com","name": {"givenName": "Jon","familyName": "Snow"},"displayName": "jonsnow","active": true,"emails": [{"value": "jon.snow@docker.com","display": "jon.snow@docker.com","primary": true}],"groups": [{"value": "nightswatch","display": "nightswatch"}],"meta": {"resourceType": "User","location": "https://hub.docker.com/v2/scim/2.0/Users/d80f7c79-7730-49d8-9a41-7c42fb622d9c","created": "2022-05-20T00:54:18Z","lastModified": "2022-05-20T00:54:18Z"}}`

## Update a user

Updates a user. This route is used to change the user's name, activate, and deactivate the user.

##### Authorizations:

*bearerSCIMAuth*

##### path Parameters

| idrequired | stringExample:d80f7c79-7730-49d8-9a41-7c42fb622d9cThe user ID. |
| --- | --- |

##### Request Body schema:application/scim+jsonrequired

| schemasrequired | Array ofstrings(scim_user_schemas)[ itemsnon-empty] |
| --- | --- |
|  | objectIf this is omitted from the request, the update will skip the update on it. We will only ever change the name, but not clear it. |
| enabled | booleanDefault:falseIf this is omitted from the request, it will default to false resulting in a deactivated user. |

### Responses

### Request samples

- Payload

Content typeapplication/scim+json`{"schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],"name": {"givenName": "Jon","familyName": "Snow"},"enabled": false}`

### Response samples

- 200
- 400
- 401
- 403
- 404
- 409
- 500

Content typeapplication/scim+json`{"schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],"id": "d80f7c79-7730-49d8-9a41-7c42fb622d9c","userName": "jon.snow@docker.com","name": {"givenName": "Jon","familyName": "Snow"},"displayName": "jonsnow","active": true,"emails": [{"value": "jon.snow@docker.com","display": "jon.snow@docker.com","primary": true}],"groups": [{"value": "nightswatch","display": "nightswatch"}],"meta": {"resourceType": "User","location": "https://hub.docker.com/v2/scim/2.0/Users/d80f7c79-7730-49d8-9a41-7c42fb622d9c","created": "2022-05-20T00:54:18Z","lastModified": "2022-05-20T00:54:18Z"}}`

## Organizations

The organization endpoints allow you to interact with and manage your organizations.

For more information, see [Organization administration overview](https://docs.docker.com/admin/organization/).

## List org members

Returns a list of members for an organization.

*The following fields are only visible to orgs with insights enabled.*

- `last_logged_in_at`
- `last_seen_at`
- `last_desktop_version`

To make visible, please see [View Insights for organization users](https://docs.docker.com/admin/organization/insights/#view-insights-for-organization-users).

##### Authorizations:

*bearerAuth*

##### path Parameters

| org_namerequired | stringExample:myorganizationName of the organization (namespace). |
| --- | --- |

##### query Parameters

| search | integerSearch term. |
| --- | --- |
| page | integerPage number (starts on 1). |
| page_size | integerNumber of items (rows) per page. |
| invites | booleanInclude invites in the response. |
| type | stringEnum:"all""invitee""member"Example:type=all |
| role | stringEnum:"owner""editor""member"Example:role=owner |

### Responses

### Response samples

- 200
- 400
- 401
- 403
- 404

Content typeapplication/json`[{"count": 120,"previous": "https://hub.docker.com/v2/some/resources/items?page=1&page_size=20","next": "https://hub.docker.com/v2/some/resources/items?page=3&page_size=20","results": [{"email": "example@docker.com","role": "Owner","groups": ["developers","owners"],"is_guest": false,"primary_email": "example@docker.com","last_logged_in_at": "2021-01-05T21:06:53.506400Z","last_seen_at": "2021-01-05T21:06:53.506400Z","last_desktop_version": "4.29.0","id": "0ab70deb065a43fcacd55d48caa945d8","company": "Docker Inc","date_joined": "2021-01-05T21:06:53.506400Z","full_name": "Jon Snow","gravatar_email": "string","gravatar_url": "string","location": "string","profile_url": "string","type": "User","username": "dockeruser"}]}]`

## Export org members CSV

Export members of an organization as a CSV

##### Authorizations:

*bearerAuth*

##### path Parameters

| org_namerequired | stringExample:myorganizationName of the organization (namespace). |
| --- | --- |

### Responses

### Response samples

- 400
- 401
- 403
- 404

Content typeapplication/json`{"errinfo": { },"detail": "string","message": "string"}`

## Update org member (role)

Updates the role of a member in the organization.
*Only users in the "owners" group of the organization can use this endpoint.*

##### Authorizations:

*bearerAuth*

##### path Parameters

| org_namerequired | stringExample:myorganizationName of the organization (namespace). |
| --- | --- |
| usernamerequired | stringExample:jonsnowUsername, identifier for the user (namespace, DockerID). |

##### Request Body schema:application/jsonrequired

| rolerequired | stringEnum:"owner""editor""member"Role of the member |
| --- | --- |

### Responses

### Request samples

- Payload

Content typeapplication/json`{"role": "owner"}`

### Response samples

- 200
- 400
- 401
- 403
- 404

Content typeapplication/json`{"email": "example@docker.com","role": "Owner","groups": ["developers","owners"],"is_guest": false,"primary_email": "example@docker.com","last_logged_in_at": "2021-01-05T21:06:53.506400Z","last_seen_at": "2021-01-05T21:06:53.506400Z","last_desktop_version": "4.29.0","id": "0ab70deb065a43fcacd55d48caa945d8","company": "Docker Inc","date_joined": "2021-01-05T21:06:53.506400Z","full_name": "Jon Snow","gravatar_email": "string","gravatar_url": "string","location": "string","profile_url": "string","type": "User","username": "dockeruser"}`

## Remove member from org

Removes the member from the org, ie. all groups in the org, unless they're the last owner

##### Authorizations:

*bearerAuth*

##### path Parameters

| org_namerequired | stringExample:myorganizationName of the organization (namespace). |
| --- | --- |
| usernamerequired | stringExample:jonsnowUsername, identifier for the user (namespace, DockerID). |

### Responses

### Response samples

- 400
- 401
- 403
- 404

Content typeapplication/json`{"errinfo": { },"detail": "string","message": "string"}`

## Organization Access Tokens

The organization access token endpoints allow you to manage organization access tokens (OATs). See [Organization access tokens](https://docs.docker.com/security/for-admins/access-tokens/) for more information.

## Create access token

Create an access token for an organization.

##### Authorizations:

*bearerAuth*

##### Request Body schema:application/jsonrequired

| label | stringLabel for the access token |
| --- | --- |
| description | stringDescription of the access token |
|  | Array ofobjects(orgAccessTokenResource)Resources this token has access to |
| expires_at | string or null<date-time>Expiration date for the token |

### Responses

### Request samples

- Payload

Content typeapplication/json`{"label": "My organization token","description": "Token for CI/CD pipeline","resources": [{"type": "TYPE_REPO","path": "myorg/myrepo","scopes": ["repo-pull"]}],"expires_at": "2023-05-20T00:54:18Z"}`

### Response samples

- 201
- 400
- 401
- 403
- 404

Content typeapplication/json`{"id": "a7a5ef25-8889-43a0-8cc7-f2a94268e861","label": "My organization token","created_by": "johndoe","is_active": true,"created_at": "2022-05-20T00:54:18Z","expires_at": "2023-05-20T00:54:18Z","last_used_at": "2022-06-15T12:30:45Z","token": "dckr_oat_7awgM4jG5SQvxcvmNzhKj8PQjxo","resources": [{"type": "TYPE_REPO","path": "myorg/myrepo","scopes": ["repo-pull"]}]}`

## List access tokens

List access tokens for an organization.

##### Authorizations:

*bearerAuth*

##### query Parameters

| page | numberDefault:1 |
| --- | --- |
| page_size | numberDefault:10 |

### Responses

### Response samples

- 200
- 401
- 403
- 404

Content typeapplication/json`{"total": 10,"next": "https://hub.docker.com/v2/orgs/docker/access-tokens?page=2&page_size=10","previous": "https://hub.docker.com/v2/orgs/docker/access-tokens?page=1&page_size=10","results": [{"id": "a7a5ef25-8889-43a0-8cc7-f2a94268e861","label": "My organization token","created_by": "johndoe","is_active": true,"created_at": "2022-05-20T00:54:18Z","expires_at": "2023-05-20T00:54:18Z","last_used_at": "2022-06-15T12:30:45Z"}]}`

## Get access token

Get details of a specific access token for an organization.

##### Authorizations:

*bearerAuth*

##### path Parameters

| org_namerequired | stringExample:myorganizationName of the organization (namespace). |
| --- | --- |
| access_token_idrequired | stringExample:a7a5ef25-8889-43a0-8cc7-f2a94268e861The ID of the access token to retrieve |

### Responses

### Response samples

- 200
- 401
- 403
- 404

Content typeapplication/json`{"id": "a7a5ef25-8889-43a0-8cc7-f2a94268e861","label": "My organization token","created_by": "johndoe","is_active": true,"created_at": "2022-05-20T00:54:18Z","expires_at": "2023-05-20T00:54:18Z","last_used_at": "2022-06-15T12:30:45Z","resources": [{"type": "TYPE_REPO","path": "myorg/myrepo","scopes": ["repo-pull"]}]}`

## Update access token

Update a specific access token for an organization.

##### Authorizations:

*bearerAuth*

##### path Parameters

| org_namerequired | stringExample:myorganizationName of the organization (namespace). |
| --- | --- |
| access_token_idrequired | stringExample:a7a5ef25-8889-43a0-8cc7-f2a94268e861The ID of the access token to retrieve |

##### Request Body schema:application/jsonrequired

| label | stringLabel for the access token |
| --- | --- |
| description | stringDescription of the access token |
|  | Array ofobjects(orgAccessTokenResource)Resources this token has access to |
| is_active | booleanWhether the token is active |

### Responses

### Request samples

- Payload

Content typeapplication/json`{"label": "My organization token","description": "Token for CI/CD pipeline","resources": [{"type": "TYPE_REPO","path": "myorg/myrepo","scopes": ["repo-pull"]}],"is_active": true}`

### Response samples

- 200
- 401
- 403
- 404

Content typeapplication/json`{"id": "a7a5ef25-8889-43a0-8cc7-f2a94268e861","label": "My organization token","created_by": "johndoe","is_active": true,"created_at": "2022-05-20T00:54:18Z","expires_at": "2023-05-20T00:54:18Z","last_used_at": "2022-06-15T12:30:45Z","resources": [{"type": "TYPE_REPO","path": "myorg/myrepo","scopes": ["repo-pull"]}]}`

## Delete access token

Delete a specific access token for an organization. This action cannot be undone.

##### Authorizations:

*bearerAuth*

##### path Parameters

| org_namerequired | stringExample:myorganizationName of the organization (namespace). |
| --- | --- |
| access_token_idrequired | stringExample:a7a5ef25-8889-43a0-8cc7-f2a94268e861The ID of the access token to retrieve |

### Responses

### Response samples

- 401
- 403
- 404

Content typeapplication/json`{"detail": "string","message": "string"}`

## Groups (Teams)

The groups endpoints allow you to manage your organization's teams and their members.

For more information, seee [Create and manage a team](https://docs.docker.com/admin/organization/manage-a-team/).

## Get groups of an organization

##### Authorizations:

*bearerAuth*

##### path Parameters

| org_namerequired | stringExample:myorganizationName of the organization (namespace). |
| --- | --- |

##### query Parameters

| page | integerPage number (starts on 1). |
| --- | --- |
| page_size | integerNumber of items (rows) per page. |
| username | stringGet groups for the specified username in the organization. |
| search | stringGet groups for the specified group in the organization. |

### Responses

### Response samples

- 200
- 401
- 403
- 404

Content typeapplication/json`{"count": 1,"next": null,"previous": null,"results": [{"id": 10,"uuid": "string","name": "mygroup","description": "Groups description","member_count": 10}]}`

## Create a new group

Create a new group within an organization.

##### Authorizations:

*bearerAuth*

##### path Parameters

| org_namerequired | stringExample:myorganizationName of the organization (namespace). |
| --- | --- |

##### Request Body schema:application/json

| namerequired | string |
| --- | --- |
| description | string |

### Responses

### Request samples

- Payload

Content typeapplication/json`{"name": "string","description": "string"}`

### Response samples

- 201
- 400
- 401
- 403

Content typeapplication/json`{"id": 10,"uuid": "string","name": "mygroup","description": "Groups description","member_count": 10}`

## Get a group of an organization

##### Authorizations:

*bearerAuth*

##### path Parameters

| org_namerequired | stringExample:myorganizationName of the organization (namespace). |
| --- | --- |
| group_namerequired | stringExample:developersName of the group (team) in the organization. |

### Responses

### Response samples

- 200
- 401
- 403
- 404

Content typeapplication/json`{"id": 10,"uuid": "string","name": "mygroup","description": "Groups description","member_count": 10}`

## Update the details for an organization group

##### Authorizations:

*bearerAuth*

##### path Parameters

| org_namerequired | stringExample:myorganizationName of the organization (namespace). |
| --- | --- |
| group_namerequired | stringExample:developersName of the group (team) in the organization. |

##### Request Body schema:application/json

| namerequired | string |
| --- | --- |
| description | string |

### Responses

### Request samples

- Payload

Content typeapplication/json`{"name": "string","description": "string"}`

### Response samples

- 200
- 401
- 403
- 404

Content typeapplication/json`{"id": 10,"uuid": "string","name": "mygroup","description": "Groups description","member_count": 10}`

## Update some details for an organization group

##### Authorizations:

*bearerAuth*

##### path Parameters

| org_namerequired | stringExample:myorganizationName of the organization (namespace). |
| --- | --- |
| group_namerequired | stringExample:developersName of the group (team) in the organization. |

##### Request Body schema:application/json

| name | string |
| --- | --- |
| description | string |

### Responses

### Request samples

- Payload

Content typeapplication/json`{"name": "string","description": "string"}`

### Response samples

- 200
- 401
- 403
- 404

Content typeapplication/json`{"id": 10,"uuid": "string","name": "mygroup","description": "Groups description","member_count": 10}`

## Delete an organization group

##### Authorizations:

*bearerAuth*

##### path Parameters

| org_namerequired | stringExample:myorganizationName of the organization (namespace). |
| --- | --- |
| group_namerequired | stringExample:developersName of the group (team) in the organization. |

### Responses

### Response samples

- 401
- 403
- 404

Content typeapplication/json`{"errinfo": { },"detail": "string","message": "string"}`

## List members of a group

List the members (users) that are in a group.
If user is owner of the org or has otherwise elevated permissions, they can search by email and the result will also contain emails.

##### Authorizations:

*bearerAuth*

##### path Parameters

| org_namerequired | stringExample:myorganizationName of the organization (namespace). |
| --- | --- |
| group_namerequired | stringExample:developersName of the group (team) in the organization. |

##### query Parameters

| page | integerPage number (starts on 1). |
| --- | --- |
| page_size | integerNumber of items (rows) per page. |
| search | stringSearch members by username, full_name or email. |

### Responses

### Response samples

- 200
- 401
- 403
- 404

Content typeapplication/json`{"count": 1,"next": null,"previous": null,"results": [{"id": "0ab70deb065a43fcacd55d48caa945d8","company": "Docker Inc","date_joined": "2021-01-05T21:06:53.506400Z","full_name": "John Snow","gravatar_email": "string","gravatar_url": "string","location": "string","profile_url": "string","type": "User","username": "dockeruser","email": "dockeruser@docker.com"}]}`

## Add a member to a group

##### Authorizations:

*bearerAuth*

##### path Parameters

| org_namerequired | stringExample:myorganizationName of the organization (namespace). |
| --- | --- |
| group_namerequired | stringExample:developersName of the group (team) in the organization. |

##### Request Body schema:application/jsonrequired

| memberrequired | string |
| --- | --- |

### Responses

### Request samples

- Payload

Content typeapplication/json`{"member": "jonsnow"}`

### Response samples

- 401
- 403
- 404
- 500

Content typeapplication/json`{"errinfo": { },"detail": "string","message": "string"}`

## Remove a user from a group

##### Authorizations:

*bearerAuth*

##### path Parameters

| org_namerequired | stringExample:myorganizationName of the organization (namespace). |
| --- | --- |
| group_namerequired | stringExample:developersName of the group (team) in the organization. |
| usernamerequired | stringExample:jonsnowUsername, identifier for the user (namespace, DockerID). |

### Responses

### Response samples

- 401
- 403
- 404

Content typeapplication/json`{"errinfo": { },"detail": "string","message": "string"}`

## Invites

The invites endpoints allow you to manage invites for users to join your Docker organization.

For more information, see [Invite members](https://docs.docker.com/admin/organization/members/#invite-members).

## List org invites

Return all pending invites for a given org, only team owners can call this endpoint

##### Authorizations:

*bearerAuth*

##### path Parameters

| org_namerequired | stringExample:myorganizationName of the organization (namespace). |
| --- | --- |

### Responses

### Response samples

- 200
- 401
- 403
- 404

Content typeapplication/json`{"data": [{"id": "e36eca69-4cc8-4f17-9845-ae8c2b832691","inviter_username": "moby","invitee": "invitee@docker.com","org": "docker","team": "owners","created_at": "2021-10-28T18:30:19.520861Z"}]}`

## Cancel an invite

Mark the invite as cancelled so it doesn't show up on the list of pending invites

##### Authorizations:

*bearerAuth*

##### path Parameters

| idrequired | string |
| --- | --- |

### Responses

### Response samples

- 401
- 403
- 404

Content typeapplication/json`{"errinfo": { },"detail": "string","message": "string"}`

## Resend an invite

Resend a pending invite to the user, any org owner can resend an invite

##### Authorizations:

*bearerAuth*

##### path Parameters

| idrequired | string |
| --- | --- |

### Responses

### Response samples

- 401
- 403
- 404

Content typeapplication/json`{"errinfo": { },"detail": "string","message": "string"}`

## Bulk create invites

Create multiple invites by emails or DockerIDs. Only a team owner can create invites.

##### Authorizations:

*bearerAuth*

##### header Parameters

| X-Analytics-Client-Feature | stringOptional string that indicates the feature used to submit the bulk invites (e.g.'file', 'web') |
| --- | --- |

##### Request Body schema:application/jsonrequired

| orgrequired | stringorganization name |
| --- | --- |
| team | stringteam name |
| role | stringrole for invitees |
| inviteesrequired | Array ofstringslist of invitees emails or Docker Ids |
| dry_run | booleanOptional, run through validation but don't actually change data. |

### Responses

### Request samples

- Payload

Content typeapplication/json`{"org": "docker","team": "owners","role": "member","invitees": ["invitee1DockerId","invitee2@docker.com","invitee3@docker.com"],"dry_run": true}`

### Response samples

- 202
- 400
- 409

Content typeapplication/json`{"invitees": {"invitees": [{"invitee": "invitee@docker.com","status": "invited","invite": {"id": "e36eca69-4cc8-4f17-9845-ae8c2b832691","inviter_username": "moby","invitee": "invitee@docker.com","org": "docker","team": "owners","created_at": "2021-10-28T18:30:19.520861Z"}},{"invitee": "invitee2@docker.com","status": "existing_org_member"},{"invitee": "invitee3@docker.com","status": "invalid_email_or_docker_id"}]}}`
