# SSO user management FAQs and more

# SSO user management FAQs

> Frequently asked questions about managing users with Docker single sign-ons

# SSO user management FAQs

   Table of contents

---

## Do I need to manually add users to my organization?

No, you don't need to manually add users to your organization. Just ensure user accounts exist in your IdP. When users sign in to Docker with their domain email address, they're automatically added to the organization after successful authentication.

## Can users use different email addresses to authenticate through SSO?

All users must authenticate using the email domain specified during SSO setup. Users with email addresses that don't match the verified domain can sign in as guests with username and password if SSO isn't enforced, but only if they've been invited.

## How will users know they're being added to a Docker organization?

When SSO is turned on, users are prompted to authenticate through SSO the next time they sign in to Docker Hub or Docker Desktop. The system detects their domain email and prompts them to sign in with SSO credentials instead.

For CLI access, users must authenticate using personal access tokens.

## Can I convert existing users from non-SSO to SSO accounts?

Yes, you can convert existing users to SSO accounts. Ensure users have:

- Company domain email addresses and accounts in your IdP
- Docker Desktop version 4.4.2 or later
- Personal access tokens created to replace passwords for CLI access
- CI/CD pipelines updated to use PATs instead of passwords

For detailed instructions, see
[Configure single sign-on](https://docs.docker.com/enterprise/security/single-sign-on/configure/).

## Is Docker SSO fully synced with the IdP?

Docker SSO provides Just-in-Time (JIT) provisioning by default. Users are provisioned when they authenticate with SSO. If users leave the organization, administrators must manually
[remove the user](https://docs.docker.com/admin/organization/members/#remove-a-member-or-invitee) from the organization.

[SCIM](https://docs.docker.com/enterprise/security/provisioning/scim/) provides full synchronization with users and groups. When using SCIM, the recommended configuration is to turn off JIT so all auto-provisioning is handled by SCIM.

Additionally, you can use the
[Docker Hub API](https://docs.docker.com/reference/api/hub/latest/) to complete this process.

## How does turning off Just-in-Time provisioning affect user sign-in?

When JIT is turned off (available with SCIM in the Admin Console), users must be organization members or have pending invitations to access Docker. Users who don't meet these criteria get an "Access denied" error and need administrator invitations.

See
[SSO authentication with JIT provisioning disabled](https://docs.docker.com/enterprise/security/provisioning/just-in-time/#sso-authentication-with-jit-provisioning-disabled).

## Can someone join an organization without an invitation?

Not without SSO. Joining requires an invite from an organization owner. When SSO is enforced, users with verified domain emails can automatically join the organization when they sign in.

## What happens to existing licensed users when SCIM is turned on?

Turning on SCIM doesn't immediately remove or modify existing licensed users. They retain current access and roles, but you'll manage them through your IdP after SCIM is active. If SCIM is later turned off, previously SCIM-managed users remain in Docker but are no longer automatically updated based on your IdP.

## Is user information visible in Docker Hub?

All Docker accounts have public profiles associated with their namespace. If you don't want user information (like full names) to be visible, remove those attributes from your SSO and SCIM mappings, or use different identifiers to replace users' full names.

---

# Manage single sign

> Learn how to manage Single Sign-On for your organization or company.

# Manage single sign-on

   Table of contents

---

Subscription: Business Requires: Docker Desktop
[4.42](https://docs.docker.com/desktop/release-notes/#4420) and later For: Administrators

This page covers how to manage single sign-on (SSO) after initial setup,
including managing domains, connections, users, and provisioning
settings.

## Manage domains

### Add a domain

To add a domain to an existing SSO connection:

1. Sign in to [Docker Home](https://app.docker.com) and select your company or
  organization from the top-left account drop-down.
2. Select **Admin Console**, then **SSO and SCIM**.
3. In the SSO connections table, select the **Actions** menu for your
  connection, then select **Edit connection**.
4. Select **Next** to navigate to the domains section.
5. In the **Domains** section, select **Add domain**.
6. Enter the domain you want to add to the connection.
7. Select **Next** to confirm or change the connected organizations.
8. Select **Next** to confirm or change the default organization and
  team provisioning selections.
9. Review the connection details and select **Update connection**.

### Remove a domain from an SSO connection

> Important
>
> If you use multiple identity providers with the same domain, you must remove the domain from each SSO connection individually.

1. Sign in to [Docker Home](https://app.docker.com) and select your company or organization from the top-left account drop-down.
2. Select **Admin Console**, then **SSO and SCIM**.
3. In the **SSO connections** table, select the **Actions** menu for your connection, then
  **Edit connection**.
4. Select **Next** to navigate to the domains section.
5. In the **Domain** section, select the **X** icon next to the domain
  you want to remove.
6. Select **Next** to confirm or change the connected organizations.
7. Select **Next** to confirm or change the default organization and
  team provisioning selections.
8. Review the connection details and select **Update connection**.

> Note
>
> When you re-add a domain, Docker assigns a new TXT record value. You must complete domain verification again with the new TXT record.

## Manage SSO connections

### View connections

To view all configured SSO connections:

1. Sign in to [Docker Home](https://app.docker.com) and select your company or organization from the top-left account drop-down.
2. Select **Admin Console**, then **SSO and SCIM**.
3. View all configured connections in the **SSO connections** table.

### Edit a connection

To modify an existing SSO connection:

1. Sign in to [Docker Home](https://app.docker.com) and select your company or organization from the top-left account drop-down.
2. Select **Admin Console**, then **SSO and SCIM**.
3. In the **SSO connections** table, select the **Actions** menu for your connection, then
  **Edit connection**.
4. Follow the on-screen instructions to modify your connection settings.

### Delete a connection

To remove an SSO connection:

1. Sign in to [Docker Home](https://app.docker.com) and select your company or organization from the top-left account drop-down.
2. Select **Admin Console**, then **SSO and SCIM**.
3. In the **SSO connections** table, select the **Actions** menu for your connection, then
  **Delete connection**.
4. Follow the on-screen instructions to confirm the deletion.

> Warning
>
> Deleting an SSO connection removes access for all users who authenticate through
> that connection.

## Manage users and provisioning

Docker automatically provisions users through Just-in-Time (JIT) provisioning when they sign in via SSO. You can also manually manage users and configure different provisioning methods.

### How provisioning works

Docker supports the following provisioning methods:

- JIT provisioning (default): Users are automatically added to your organization
  when they sign in via SSO
- SCIM provisioning: Sync users and groups from your identity provider to Docker
- Group mapping: Sync user groups from your identity provider with teams in your Docker organization
- Manual provisioning: Turn off automatic provisioning and manually invite users

For more information on provisioning methods, see
[Provision users](https://docs.docker.com/enterprise/security/provisioning/).

### Add guest users

To invite users who don't authenticate through your identity provider:

1. Sign in to [Docker Home](https://app.docker.com/) and select
  your organization.
2. Select **Members**.
3. Select **Invite**.
4. Follow the on-screen instructions to invite the user.

The user receives an email invitation and can create a Docker account or sign
in with their existing account.

### Remove users

To remove a user from your organization:

1. Sign in to [Docker Home](https://app.docker.com/) and select
  your organization.
2. Select **Members**.
3. Find the user you want to remove and select the **Actions** menu next to their name.
4. Select **Remove** and confirm the removal.

The user loses access to your organization immediately upon removal.

---

# Single sign

> Learn how single sign-on works, how to set it up, and the required SSO attributes.

# Single sign-on overview

   Table of contents

---

Subscription: Business Requires: Docker Desktop
[4.42](https://docs.docker.com/desktop/release-notes/#4420) and later For: Administrators

Single sign-on (SSO) lets users access Docker by authenticating through their
identity providers (IdPs). SSO can be configured for an entire company,
including all associated organizations, or for a single organization that has a
Docker Business subscription.

## How SSO works

When SSO is enabled, Docker supports a non-IdP-initiated flow for user sign-in.
Instead of signing in with a Docker username and password, users are redirected
to your IdP’s sign-in page. Users must initiate the SSO authentication process
by signing in to Docker Hub or Docker Desktop.

The following diagram illustrates how SSO operates and is managed between
Docker Hub, Docker Desktop, and your IdP.

![SSO architecture](https://docs.docker.com/enterprise/security/single-sign-on/images/SSO.png)  ![SSO architecture](https://docs.docker.com/enterprise/security/single-sign-on/images/SSO.png)

## Set up SSO

To configure SSO in Docker, follow these steps:

1. [Configure your domain](https://docs.docker.com/enterprise/security/single-sign-on/configure/) by creating and verifying it.
2. [Create your SSO connection](https://docs.docker.com/enterprise/security/single-sign-on/connect/) in Docker and your IdP.
3. Link Docker to your identity provider.
4. Test your SSO connection.
5. Provision users in Docker.
6. Optional. [Enforce sign-in](https://docs.docker.com/enterprise/security/enforce-sign-in/).
7. [Manage your SSO configuration](https://docs.docker.com/enterprise/security/single-sign-on/manage/).

Once configuration is complete, users can sign in to Docker services using
their company email address. After signing in, users are added to your company,
assigned to an organization, and added to a team.

## Prerequisites

Before you begin, make sure the following conditions are met:

- Notify your company about the upcoming SSO sign-in process.
- Ensure all users have Docker Desktop version 4.42 or later installed.
- Confirm that each Docker user has a valid IdP account using the same
  email address as their Unique Primary Identifier (UPN).
- If you plan to
  [enforce SSO](https://docs.docker.com/enterprise/security/single-sign-on/connect/#optional-enforce-sso),
  users accessing Docker through the CLI must
  [create a personal access token (PAT)](https://docs.docker.com/docker-hub/access-tokens/). The PAT replaces their username and password for authentication.
- Ensure CI/CD pipelines use PATs or OATs instead of passwords.

> Important
>
> Docker plans to deprecate CLI password-based sign-in in future releases.
> Using a PAT ensures continued CLI access. For more information, see the
> [security announcement](https://docs.docker.com/security/security-announcements/#deprecation-of-password-logins-on-cli-when-sso-enforced).

## Next steps

- Start [configuring SSO](https://docs.docker.com/enterprise/security/single-sign-on/configure/).
- Read the
  [FAQs](https://docs.docker.com/enterprise/security/single-sign-on/faqs/general/).
- [Troubleshoot](https://docs.docker.com/enterprise/troubleshoot/troubleshoot-sso/) SSO issues.

---

# Security for enterprises

> Learn about enterprise level security features Docker has to offer and explore best practices

# Security for enterprises

   Table of contents

---

Docker provides security guardrails for both administrators and developers.

If you're an administrator, you can enforce sign-in across Docker products for your developers, and
scale, manage, and secure your instances of Docker Desktop with DevOps security controls like Enhanced Container Isolation and Registry Access Management.

## For administrators

Explore the security features Docker offers to satisfy your company's security policies.

[Settings ManagementLearn how Settings Management can secure your developers' workflows.](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/)[Enhanced Container IsolationUnderstand how Enhanced Container Isolation can prevent container attacks.](https://docs.docker.com/enterprise/security/hardened-desktop/enhanced-container-isolation/)[Registry Access ManagementControl the registries developers can access while using Docker Desktop.](https://docs.docker.com/enterprise/security/hardened-desktop/registry-access-management/)[Image Access ManagementControl the images developers can pull from Docker Hub.](https://docs.docker.com/enterprise/security/hardened-desktop/image-access-management/)[Air-Gapped ContainersRestrict containers from accessing unwanted network resources.](https://docs.docker.com/enterprise/security/hardened-desktop/air-gapped-containers/)[Enforce sign-inConfigure sign-in for members of your teams and organizations.](https://docs.docker.com/enterprise/security/enforce-sign-in/)[Domain managementIdentify uncaptured users in your organization.](https://docs.docker.com/enterprise/security/domain-management/)[Docker ScoutExplore how Docker Scout can help you create a more secure software supply chain.](https://docs.docker.com/scout/)[SSOLearn how to configure SSO for your company or organization.](https://docs.docker.com/enterprise/security/single-sign-on/)[SCIMSet up SCIM to automatically provision and deprovision users.](https://docs.docker.com/enterprise/security/provisioning/scim/)[Roles and permissionsAssign roles to individuals giving them different permissions within an organization.](https://docs.docker.com/enterprise/security/roles-and-permissions/)[Private marketplace for Extensions (Beta)Learn how to configure and set up a private marketplace with a curated list of extensions for your Docker Desktop users.](https://docs.docker.com/desktop/extensions/private-marketplace/)[Organization access tokensCreate organization access tokens as an alternative to a password.](https://docs.docker.com/enterprise/security/access-tokens/)

---

# Troubleshoot provisioning

> Troubleshoot common user provisioning issues with SCIM and Just-in-Time provisioning

# Troubleshoot provisioning

   Table of contents

---

This page helps troubleshoot common user provisioning issues including user roles, attributes, and unexpected account behavior with SCIM and Just-in-Time (JIT) provisioning.

## SCIM attribute values are overwritten or ignored

### Error message

Typically, this scenario does not produce an error message in Docker or your
IdP. This issue usually surfaces as incorrect role or team assignment.

### Causes

- JIT provisioning is enabled, and Docker is using values from your IdP's
  SSO login flow to provision the user, which overrides
  SCIM-provided attributes.
- SCIM was enabled after the user was already provisioned via JIT, so SCIM
  updates don't take effect.

### Affected environments

- Docker organizations using SCIM with SSO
- Users provisioned via JIT prior to SCIM setup

### Steps to replicate

1. Enable JIT and SSO for your Docker organization.
2. Sign in to Docker as a user via SSO.
3. Enable SCIM and set role/team attributes for that user.
4. SCIM attempts to update the user's attributes, but the role or team
  assignment does not reflect changes.

### Solutions

#### Disable JIT provisioning (recommended)

1. Sign in to [Docker Home](https://app.docker.com/).
2. Select **Admin Console**, then **SSO and SCIM**.
3. Find the relevant SSO connection.
4. Select the **actions menu** and choose **Edit**.
5. Disable **Just-in-Time provisioning**.
6. Save your changes.

With JIT disabled, Docker uses SCIM as the source of truth for user creation
and role assignment.

**Keep JIT enabled and match attributes**

If you prefer to keep JIT enabled:

- Make sure your IdP's SSO attribute mappings match the values being sent
  by SCIM.
- Avoid configuring SCIM to override attributes already set via JIT.

This option requires strict coordination between SSO and SCIM attributes
in your IdP configuration.

## SCIM updates don't apply to existing users

### Causes

User accounts were originally created manually or via JIT, and SCIM is not
linked to manage them.

### Solution

SCIM only manages users that it provisions. To allow SCIM to manage an
existing user:

1. Remove the user manually from the Docker [Admin Console](https://app.docker.com/admin).
2. Trigger provisioning from your IdP.
3. SCIM will re-create the user with correct attributes.

> Warning
>
> Deleting a user removes their resource ownership (e.g., repositories).
> Transfer ownership before removing the user.

---

# Troubleshoot single sign

> Troubleshoot common Docker single sign-on configuration and authentication issues

# Troubleshoot single sign-on

   Table of contents

---

This page describes common single sign-on (SSO) errors and their solutions. Issues can stem from your identity provider (IdP) configuration or Docker settings.

## Check for errors

If you experience SSO issues, check both Docker and your identity provider for errors first.

### Check Docker error logs

1. Sign in to [Docker Home](https://app.docker.com/) and select your organization from the top-left account drop-down.
2. Select **Admin Console**, then **SSO and SCIM**.
3. In the SSO connections table, select the **Action** menu and then **View error logs**.
4. For more details on specific errors, select **View error details** next to an error message.
5. Note any errors you see on this page for further troubleshooting.

### Check identity provider errors

1. Review your IdP’s logs or audit trails for any failed authentication or provisioning attempts.
2. Confirm that your IdP’s SSO settings match the values provided in Docker.
3. If applicable, confirm that you have configured user provisioning correctly and that it is enabled in your IdP.
4. If applicable, verify that your IdP correctly maps Docker's required user attributes.
5. Try provisioning a test user from your IdP and verify if they appear in Docker.

For further troubleshooting, check your IdP's documentation or contact their support team.

## Groups are not formatted correctly

### Error message

When this issue occurs, the following error message is common:

```text
Some of the groups assigned to the user are not formatted as '<organization name>:<team name>'. Directory groups will be ignored and user will be provisioned into the default organization and team.
```

### Causes

- Incorrect group name formatting in your identity provider (IdP): Docker requires groups to follow the format `<organization>:<team>`. If the groups assigned to a user do not follow this format, they will be ignored.
- Non-matching groups between IdP and Docker organization: If a group in your IdP does not have a corresponding team in Docker, it will not be recognized, and the user will be placed in the default organization and team.

### Affected environments

- Docker single sign-on setup using IdPs such as Okta or Azure AD
- Organizations using group-based role assignments in Docker

### Steps to replicate

To replicate this issue:

1. Attempt to sign in to Docker using SSO.
2. The user is assigned groups in the IdP but does not get placed in the expected Docker Team.
3. Review Docker logs or IdP logs to find the error message.

### Solutions

Update group names in your IdP:

1. Go to your IdP's group management section.
2. Check the groups assigned to the affected user.
3. Ensure each group follows the required format: `<organization>:<team>`
4. Update any incorrectly formatted groups to match this pattern.
5. Save changes and retry signing in with SSO.

## User is not assigned to the organization

### Error message

When this issue occurs, the following error message is common:

```text
User '$username' is not assigned to this SSO organization. Contact your administrator. TraceID: XXXXXXXXXXXXX
```

### Causes

- User is not assigned to the organization: If Just-in-Time (JIT) provisioning is disabled, the user may not be assigned to your organization.
- User is not invited to the organization: If JIT is disabled and you do not want to enable it, the user must be manually invited.
- SCIM provisioning is misconfigured: If you use SCIM for user provisioning, it may not be correctly syncing users from your IdP.

### Solutions

**Enable JIT provisioning**

JIT is enabled by default when you enable SSO. If you have JIT disabled and need
to re-enable it:

1. Sign in to [Docker Home](https://app.docker.com/) and select your organization from the top-left account drop-down.
2. Select **Admin Console**, then **SSO and SCIM**.
3. In the SSO connections table, select the **Action** menu and then **Enable JIT provisioning**.
4. Select **Enable** to confirm.

**Manually invite users**

When JIT is disabled, users are not automatically added to your organization when they authenticate through SSO.
To manually invite users, see
[Invite members](https://docs.docker.com/admin/organization/members/#invite-members)

**Configure SCIM provisioning**

If you have SCIM enabled, troubleshoot your SCIM connection using the following steps:

1. Sign in to [Docker Home](https://app.docker.com/) and select your organization from the top-left account drop-down.
2. Select **Admin Console**, then **SSO and SCIM**.
3. In the SSO connections table, select the **Action** menu and then **View error logs**. For more details on specific errors, select **View error details** next to an error message. Note any errors you see on this page.
4. Navigate back to the **SSO and SCIM** page of the Admin Console and verify your SCIM configuration:
  - Ensure that the SCIM Base URL and API Token in your IdP match those provided in the Docker Admin Console.
  - Verify that SCIM is enabled in both Docker and your IdP.
5. Ensure that the attributes being synced from your IdP match Docker's
  [supported attributes](https://docs.docker.com/enterprise/security/provisioning/scim/#supported-attributes) for SCIM.
6. Test user provisioning by trying to provision a test user through your IdP and verify if they appear in Docker.

## IdP-initiated sign in is not enabled for connection

### Error message

When this issue occurs, the following error message is common:

```text
IdP-Initiated sign in is not enabled for connection '$ssoConnection'.
```

### Causes

Docker does not support an IdP-initiated SAML flow. This error occurs when a user attempts to authenticate from your IdP, such as using the Docker SSO app tile on the sign in page.

### Solutions

**Authenticate from Docker apps**

The user must initiate authentication from Docker applications (Hub, Desktop, etc). The user needs to enter their email address in a Docker app and they will get redirected to the configured SSO IdP for their domain.

**Hide the Docker SSO app**

You can hide the Docker SSO app from users in your IdP. This prevents users from attempting to start authentication from the IdP dashboard. You must hide and configure this in your IdP.

## Not enough seats in organization

### Error message

When this issue occurs, the following error message is common:

```text
Not enough seats in organization '$orgName'. Add more seats or contact your administrator.
```

### Causes

This error occurs when the organization has no available seats for the user when provisioning via Just-in-Time (JIT) provisioning or SCIM.

### Solutions

**Add more seats to the organization**

Purchase additional Docker Business subscription seats. For details, see
[Manage subscription seats](https://docs.docker.com/subscription/manage-seats/).

**Remove users or pending invitations**

Review your organization members and pending invitations. Remove inactive users or pending invitations to free up seats. For more details, see
[Manage organization members](https://docs.docker.com/admin/organization/members/).

## Domain is not verified for SSO connection

### Error message

When this issue occurs, the following error message is common:

```text
Domain '$emailDomain' is not verified for your SSO connection. Contact your company administrator. TraceID: XXXXXXXXXXXXXX
```

### Causes

This error occurs if the IdP authenticated a user through SSO and the User Principal Name (UPN)
returned to Docker doesn’t match any of the verified domains associated to the
SSO connection configured in Docker.

### Solutions

**Verify UPN attribute mapping**

Ensure that the IdP SSO connection is returning the correct UPN value in the assertion attributes.

**Add and verify all domains**

Add and verify all domains and subdomains used as UPN by your IdP and associate them with your Docker SSO connection. For details, see
[Configure single sign-on](https://docs.docker.com/enterprise/security/single-sign-on/configure/).

## Unable to find session

### Error message

When this issue occurs, the following error message is common:

```text
We couldn't find your session. You may have pressed the back button, refreshed the page, opened too many sign-in dialogs, or there is some issue with cookies. Try signing in again. If the issue persists, contact your administrator.
```

### Causes

The following causes may create this issue:

- The user pressed the back or refresh button during authentication.
- The authentication flow lost track of the initial request, preventing completion.

### Solutions

**Do not disrupt the authentication flow**

Do not press the back or refresh button during sign-in.

**Restart authentication**

Close the browser tab and restart the authentication flow from the Docker application (Desktop, Hub, etc).

## Name ID is not an email address

### Error message

When this issue occurs, the following error message is common:

```text
The name ID sent by the identity provider is not an email address. Contact your company administrator.
```

### Causes

The following causes may create this issue:

- The IdP sends a Name ID (UPN) that does not comply with the email format required by Docker.
- Docker SSO requires the Name ID to be the primary email address of the user.

### Solutions

In your IdP, ensure the Name ID attribute format is correct:

1. Verify that the Name ID attribute format in your IdP is set to `EmailAddress`.
2. Adjust your IdP settings to return the correct Name ID format.
