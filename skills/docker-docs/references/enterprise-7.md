# Provision users and more

# Provision users

> Learn about provisioning users for your SSO configuration.

# Provision users

   Table of contents

---

Subscription: Business Requires: Docker Desktop
[4.42](https://docs.docker.com/desktop/release-notes/#4420) and later For: Administrators

After configuring your SSO connection, the next step is to provision users. This process ensures that users can access your organization through automated user management.

This page provides an overview of user provisioning and the supported provisioning methods.

## What is provisioning?

Provisioning helps manage users by automating tasks like account creation, updates, and deactivation based on data from your identity provider (IdP). There are three methods for user provisioning, each offering benefits for different organizational needs:

| Provisioning method | Description | Default setting in Docker | Recommended for |
| --- | --- | --- | --- |
| Just-in-Time (JIT) | Automatically creates and provisions user accounts when they first sign in via SSO | Enabled by default | Organizations needing minimal setup, smaller teams, or low-security environments |
| System for Cross-domain Identity Management (SCIM) | Continuously syncs user data between your IdP and Docker, ensuring user attributes remain updated without manual intervention | Disabled by default | Larger organizations or environments with frequent changes in user information or roles |
| Group mapping | Maps user groups from your IdP to specific roles and permissions within Docker, enabling fine-grained access control based on group membership | Disabled by default | Organizations requiring strict access control and role-based user management |

## Default provisioning setup

By default, Docker enables JIT provisioning when you configure an SSO connection. With JIT enabled, user accounts are automatically created the first time a user signs in using your SSO flow.

JIT provisioning may not provide sufficient control or security for some organizations. In such cases, SCIM or group mapping can be configured to give administrators more control over user access and attributes.

## SSO attributes

When a user signs in through SSO, Docker obtains several attributes from your IdP to manage the user's identity and permissions. These attributes include:

- Email address: The unique identifier for the user
- Full name: The user's complete name
- Groups: Optional. Used for group-based access control
- Docker Org: Optional. Specifies the organization the user belongs to
- Docker Team: Optional. Defines the team the user belongs to within the organization
- Docker Role: Optional. Determines the user's permissions within Docker
- Docker session minutes: Optional. Sets the session duration before users must re-authenticate with their IdP. Must be a positive integer greater than 0. If not provided, default session timeouts apply

> Note
>
> Default session timeouts apply when Docker session minutes is not specified. Docker Desktop sessions expire after 90 days or 30 days of inactivity. Docker Hub and Docker Home sessions expire after 24 hours.

## SAML attribute mapping

If your organization uses SAML for SSO, Docker retrieves these attributes from the SAML assertion message. Different IdPs may use different names for these attributes.

| SSO Attribute | SAML Assertion Message Attributes |
| --- | --- |
| Email address | "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier","http://schemas.xmlsoap.org/ws/2005/05/identity/claims/upn","http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress",email |
| Full name | "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name",name,"http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname","http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname" |
| Groups (optional) | "http://schemas.xmlsoap.org/claims/Group","http://schemas.microsoft.com/ws/2008/06/identity/claims/groups",Groups,groups |
| Docker Org (optional) | dockerOrg |
| Docker Team (optional) | dockerTeam |
| Docker Role (optional) | dockerRole |
| Docker session minutes (optional) | dockerSessionMinutes, must be a positive integer > 0 |

## Next steps

Choose the provisioning method that best fits your organization's needs:

[Just-in-Time (JIT) provisioningSet up automatic user creation on first sign-in. Ideal for smaller teams with minimal setup requirements.](https://docs.docker.com/enterprise/security/provisioning/just-in-time/)[SCIM provisioningEnable continuous user data synchronization between your IdP and Docker. Best for larger organizations.](https://docs.docker.com/enterprise/security/provisioning/scim/)[Group mappingConfigure role-based access control using IdP groups. Perfect for strict access control requirements.](https://docs.docker.com/enterprise/security/provisioning/group-mapping/)

---

# Core roles

> Control access to content, registry, and organization management with roles in your organization.

# Core roles

   Table of contents

---

For: Administrators

Core roles are Docker's built-in roles with predefined permission sets.
This page provides an overview of Docker's core roles and permissions for each role.

## What are core roles?

Docker organizations have three core roles:

- **Member**: Non-administrative role with basic access. Members can view other organization members and pull images from repositories they have access to.
- **Editor**: Partial administrative access. Editors can create, edit, and delete repositories. They can also manage team permissions for repositories.
- **Owner**: Full administrative access. Owners can manage all organization settings, including repositories, teams, members, billing, and security features.

> Note
>
> A company owner has the same organization management permissions as an organization owner, but there are some content and registry permissions that company owners don't have (for example, repository pull/push). For more information, see
> [Company overview](https://docs.docker.com/admin/company/).

### Content and registry permissions

These permissions apply organization-wide, including all repositories in your organization's namespace.

| Permission | Member | Editor | Owner |
| --- | --- | --- | --- |
| Explore images and extensions | ✅ | ✅ | ✅ |
| Star, favorite, vote, and comment on content | ✅ | ✅ | ✅ |
| Pull images | ✅ | ✅ | ✅ |
| Create and publish an extension | ✅ | ✅ | ✅ |
| Become a Verified, Official, or Open Source publisher | ❌ | ❌ | ✅ |
| Edit and delete publisher repository logos | ❌ | ✅ | ✅ |
| Observe content engagement as a publisher | ❌ | ❌ | ✅ |
| Create public and private repositories | ❌ | ✅ | ✅ |
| Edit and delete repositories | ❌ | ✅ | ✅ |
| Manage tags | ❌ | ✅ | ✅ |
| View repository activity | ❌ | ❌ | ✅ |
| Set up Automated builds | ❌ | ❌ | ✅ |
| Edit build settings | ❌ | ❌ | ✅ |
| View teams | ✅ | ✅ | ✅ |
| Assign team permissions to repositories | ❌ | ✅ | ✅ |

When you add members to teams, you can grant additional repository permissions
beyond their organization role:

1. Role permissions: Applied organization-wide (member or editor)
2. Team permissions: Additional permissions for specific repositories

### Organization management permissions

| Permission | Member | Editor | Owner |
| --- | --- | --- | --- |
| Create teams | ❌ | ❌ | ✅ |
| Manage teams (including delete) | ❌ | ❌ | ✅ |
| Configure the organization's settings (including linked services) | ❌ | ❌ | ✅ |
| Add organizations to a company | ❌ | ❌ | ✅ |
| Invite members | ❌ | ❌ | ✅ |
| Manage members | ❌ | ❌ | ✅ |
| Manage member roles and permissions | ❌ | ❌ | ✅ |
| View member activity | ❌ | ❌ | ✅ |
| Export and reporting | ❌ | ❌ | ✅ |
| Image Access Management | ❌ | ❌ | ✅ |
| Registry Access Management | ❌ | ❌ | ✅ |
| Set up Single Sign-On (SSO) and SCIM | ❌ | ❌ | ✅ * |
| Require Docker Desktop sign-in | ❌ | ❌ | ✅ * |
| Manage billing information (for example, billing address) | ❌ | ❌ | ✅ |
| Manage payment methods (for example, credit card or invoice) | ❌ | ❌ | ✅ |
| View billing history | ❌ | ❌ | ✅ |
| Manage subscriptions | ❌ | ❌ | ✅ |
| Manage seats | ❌ | ❌ | ✅ |
| Upgrade and downgrade plans | ❌ | ❌ | ✅ |

** If not part of a company*

### Docker Scout permissions

| Permission | Member | Editor | Owner |
| --- | --- | --- | --- |
| View and compare analysis results | ✅ | ✅ | ✅ |
| Upload analysis records | ✅ | ✅ | ✅ |
| Activate and deactivate Docker Scout for a repository | ❌ | ✅ | ✅ |
| Create environments | ❌ | ❌ | ✅ |
| Manage registry integrations | ❌ | ❌ | ✅ |

### Docker Build Cloud permissions

| Permission | Member | Editor | Owner |
| --- | --- | --- | --- |
| Use a cloud builder | ✅ | ✅ | ✅ |
| Create and remove builders | ✅ | ✅ | ✅ |
| Configure builder settings | ✅ | ✅ | ✅ |
| Buy minutes | ❌ | ❌ | ✅ |
| Manage subscription | ❌ | ❌ | ✅ |

---

# Custom roles

> Create tailored permission sets for your organization with custom roles

# Custom roles

   Table of contents

---

For: Administrators

Custom roles allow you to create tailored permission sets that match your
organization's specific needs. This page covers custom roles and steps
to create and manage them.

## What are custom roles?

Custom roles let you create tailored permission sets for your organization. You
can assign custom roles to individual users or teams.
Users and teams get either a core role or custom role, but not both.

Use custom roles when Docker's core roles don't fit your needs.

## Prerequisites

To configure custom roles, you need owner permissions in your Docker
organization.

## Create a custom role

Before you can assign a custom role to users, you must create one in the
Admin Console:

1. Sign in to [Docker Home](https://app.docker.com).
2. Select **Admin Console**.
3. Under **User management**, select **Roles** > **Create role**.
4. Create a name and describe what the role is for:
  - Provide a **Label**
  - Enter a unique **Name** identifier (can't be changed later)
  - Add an optional **Description**
5. Set permissions for the role by expanding permission categories and selecting
  the checkboxes for permissions. For a full list of available permissions, see
  the [custom roles permissions reference](#custom-roles-permissions-reference).
6. Select **Review** to review your custom roles configuration and see a summary
  of selected permissions.
7. Select **Create**.

With a custom role created, you can now [assign custom roles to users](#assign-custom-roles).

## Edit a custom role

1. Sign in to [Docker Home](https://app.docker.com).
2. Select **Admin Console**.
3. Under **User management**, select **Roles**.
4. Find your custom role from the list, and select the **Actions menu**.
5. Select **Edit**.
6. You can edit the following custom role settings:
  - Label
  - Description
  - Permissions
7. After you have finished editing, select **Save**.

## Assign custom roles

1. Sign in to [Docker Home](https://app.docker.com).
2. Select **Members**.
3. Locate the member you want to assign a custom role to, then select the
  **Actions menu**.
4. In the drop-down, select **Change role**.
5. In the **Select a role** drop-down, select your custom role.
6. Select **Save**.

1. Sign in to [Docker Home](https://app.docker.com).
2. Select **Members**.
3. Use the checkboxes in the username column to select all users you want
  to assign a custom role to.
4. Select **Change role**.
5. In the **Select a role** drop-down, select your custom role or a core role.
6. Select **Save**.

1. Sign in to [Docker Home](https://app.docker.com).
2. Select **Teams**.
3. Locate the team you want to assign a custom role to, then select
  the **Actions menu**.
4. Select **Assign role**.
5. Select your custom role, then select **Assign**.

The role column will update to the newly assigned role.

## View role assignments

To see which users and teams are assigned to roles:

1. Sign in to [Docker Home](https://app.docker.com).
2. Select **Admin Console**.
3. Under **User management**, select **Roles**.
4. In the roles list, view the **Users** and **Teams** columns to see
  assignment counts.
5. Select a specific role to view its permissions and assignments in detail.

## Reassign custom roles

1. Sign in to [Docker Home](https://app.docker.com).
2. Select **Members**.
3. Locate the member you want to reassign, then select the **Actions menu**.
4. Select **Change role**.
5. In the **Select a role** drop-down, select the new role.
6. Select **Save**.

1. Sign in to [Docker Home](https://app.docker.com).
2. Select **Members**.
3. Use the checkboxes in the username column to select all users you want
  to reassign.
4. Select **Change role**.
5. In the **Select a role** drop-down, select the new role.
6. Select **Save**.

1. Sign in to [Docker Home](https://app.docker.com).
2. Select **Teams**.
3. Locate the team, then select the **Actions menu**.
4. Select **Change role**.
5. In the pop-up window, select a role from the drop-down menu, then
  select **Save**.

## Delete a custom role

Before deleting a custom role, you must reassign all users and teams to different roles.

1. Sign in to [Docker Home](https://app.docker.com).
2. Select **Admin Console**.
3. Under **User management**, select **Roles**.
4. Find your custom role from the list, and select the **Actions menu**.
5. If the role has assigned users or teams:
  - Navigate to the **Members** page and change the role for all users assigned to this custom role
  - Navigate to the **Teams** page and reassign all teams that have this custom role
6. Once no users or teams are assigned, return to **Roles**.
7. Find your custom role and select the **Actions menu**.
8. Select **Delete**.
9. In the confirmation window, select **Delete** to confirm.

## Custom roles permissions reference

Custom roles are built by selecting specific permissions across different categories. The following tables list all available permissions you can assign to a custom role.

### Organization management

| Permission | Description |
| --- | --- |
| View teams | View teams and team members |
| Manage teams | Create, update, and delete teams and team members |
| Manage registry access | Control which registries members can access |
| Manage image access | Set policies for which images members can pull and use |
| Update organization information | Update organization information such as name and location |
| Member management | Manage organization members, invites, and roles |
| View custom roles | View existing custom roles and their permissions |
| Manage custom roles | Full access to custom role management and assignment |
| Manage organization access tokens | Create, update, and delete repositories in this org. Push/pull or registry actions not included |
| View activity logs | Access organization audit logs and activity history |
| View domains | View domains and domain audit settings |
| Manage domains | Manage verified domains and domain audit settings |
| View SSO and SCIM | View single sign-on and user provisioning configurations |
| Manage SSO and SCIM | Full access to SSO and SCIM management |
| Manage Desktop settings | Configure Docker Desktop settings policies and view usage reports |

### Docker Hub

| Permission | Description |
| --- | --- |
| View repositories | View repository details and contents |
| Manage repositories | Create, update, and delete repositories and their contents |

### Billing

| Permission | Description |
| --- | --- |
| View billing | View organization billing information |
| Manage billing | Complete access to managing organization billing |

---

# Core roles

> Control access to content, registry, and organization management with roles in your organization.

# Core roles

   Table of contents

---

For: Administrators

Core roles are Docker's built-in roles with predefined permission sets.
This page provides an overview of Docker's core roles and permissions for each role.

## What are core roles?

Docker organizations have three core roles:

- **Member**: Non-administrative role with basic access. Members can view other organization members and pull images from repositories they have access to.
- **Editor**: Partial administrative access. Editors can create, edit, and delete repositories. They can also manage team permissions for repositories.
- **Owner**: Full administrative access. Owners can manage all organization settings, including repositories, teams, members, billing, and security features.

> Note
>
> A company owner has the same organization management permissions as an organization owner, but there are some content and registry permissions that company owners don't have (for example, repository pull/push). For more information, see
> [Company overview](https://docs.docker.com/admin/company/).

### Content and registry permissions

These permissions apply organization-wide, including all repositories in your organization's namespace.

| Permission | Member | Editor | Owner |
| --- | --- | --- | --- |
| Explore images and extensions | ✅ | ✅ | ✅ |
| Star, favorite, vote, and comment on content | ✅ | ✅ | ✅ |
| Pull images | ✅ | ✅ | ✅ |
| Create and publish an extension | ✅ | ✅ | ✅ |
| Become a Verified, Official, or Open Source publisher | ❌ | ❌ | ✅ |
| Edit and delete publisher repository logos | ❌ | ✅ | ✅ |
| Observe content engagement as a publisher | ❌ | ❌ | ✅ |
| Create public and private repositories | ❌ | ✅ | ✅ |
| Edit and delete repositories | ❌ | ✅ | ✅ |
| Manage tags | ❌ | ✅ | ✅ |
| View repository activity | ❌ | ❌ | ✅ |
| Set up Automated builds | ❌ | ❌ | ✅ |
| Edit build settings | ❌ | ❌ | ✅ |
| View teams | ✅ | ✅ | ✅ |
| Assign team permissions to repositories | ❌ | ✅ | ✅ |

When you add members to teams, you can grant additional repository permissions
beyond their organization role:

1. Role permissions: Applied organization-wide (member or editor)
2. Team permissions: Additional permissions for specific repositories

### Organization management permissions

| Permission | Member | Editor | Owner |
| --- | --- | --- | --- |
| Create teams | ❌ | ❌ | ✅ |
| Manage teams (including delete) | ❌ | ❌ | ✅ |
| Configure the organization's settings (including linked services) | ❌ | ❌ | ✅ |
| Add organizations to a company | ❌ | ❌ | ✅ |
| Invite members | ❌ | ❌ | ✅ |
| Manage members | ❌ | ❌ | ✅ |
| Manage member roles and permissions | ❌ | ❌ | ✅ |
| View member activity | ❌ | ❌ | ✅ |
| Export and reporting | ❌ | ❌ | ✅ |
| Image Access Management | ❌ | ❌ | ✅ |
| Registry Access Management | ❌ | ❌ | ✅ |
| Set up Single Sign-On (SSO) and SCIM | ❌ | ❌ | ✅ * |
| Require Docker Desktop sign-in | ❌ | ❌ | ✅ * |
| Manage billing information (for example, billing address) | ❌ | ❌ | ✅ |
| Manage payment methods (for example, credit card or invoice) | ❌ | ❌ | ✅ |
| View billing history | ❌ | ❌ | ✅ |
| Manage subscriptions | ❌ | ❌ | ✅ |
| Manage seats | ❌ | ❌ | ✅ |
| Upgrade and downgrade plans | ❌ | ❌ | ✅ |

** If not part of a company*

### Docker Scout permissions

| Permission | Member | Editor | Owner |
| --- | --- | --- | --- |
| View and compare analysis results | ✅ | ✅ | ✅ |
| Upload analysis records | ✅ | ✅ | ✅ |
| Activate and deactivate Docker Scout for a repository | ❌ | ✅ | ✅ |
| Create environments | ❌ | ❌ | ✅ |
| Manage registry integrations | ❌ | ❌ | ✅ |

### Docker Build Cloud permissions

| Permission | Member | Editor | Owner |
| --- | --- | --- | --- |
| Use a cloud builder | ✅ | ✅ | ✅ |
| Create and remove builders | ✅ | ✅ | ✅ |
| Configure builder settings | ✅ | ✅ | ✅ |
| Buy minutes | ❌ | ❌ | ✅ |
| Manage subscription | ❌ | ❌ | ✅ |

---

# Configure single sign

> Learn how to configure single sign-on for your organization or company.

# Configure single sign-on

   Table of contents

---

Subscription: Business Requires: Docker Desktop
[4.42](https://docs.docker.com/desktop/release-notes/#4420) and later For: Administrators

Learn how to set up single sign-on (SSO) for your Docker organization by adding
and verifying the domains your members use to sign in.

## Step one: Add a domain

> Note
>
> Docker supports multiple identity provider (IdP) configurations. You can
> associate one domain with more than one IdP.

To add a domain:

1. Sign in to [Docker Home](https://app.docker.com) and choose your
  organization. If it's part of a company, select the company first to manage
  the domain at that level.
2. Select **Admin Console**, then **Domain management**.
3. Select **Add a domain**.
4. Enter your domain in the text box and select **Add domain**.
5. In the modal, copy the **TXT Record Value** provided for domain verification.

## Step two: Verify your domain

To confirm domain ownership, add a TXT record to your Domain Name System (DNS)
host using the TXT Record Value from Docker. DNS propagation can take up to
72 hours. Docker automatically checks for the record during this time.

> Tip
>
> When adding a record name, **use@or leave it empty** for root domains like `example.com`. **Avoid common values** like `docker`, `docker-verification`, `www`, or your domain name itself. Always **check your DNS provider's documentation** to verify their specific record name requirements.

1. To add your TXT record to AWS, see [Creating records by using the Amazon Route 53 console](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resource-record-sets-creating.html).
2. Wait up to 72 hours for TXT record verification.
3. After the record is live, go to **Domain management** in the [Admin Console](https://app.docker.com/admin) and select **Verify**.

1. To add your TXT record to Google Cloud DNS, see [Verifying your domain with a TXT record](https://cloud.google.com/identity/docs/verify-domain-txt).
2. Wait up to 72 hours for TXT record verification.
3. After the record is live, go to **Domain management** in the [Admin Console](https://app.docker.com/admin) and select **Verify**.

1. To add your TXT record to GoDaddy, see [Add a TXT record](https://www.godaddy.com/help/add-a-txt-record-19232).
2. Wait up to 72 hours for TXT record verification.
3. After the record is live, go to **Domain management** in the [Admin Console](https://app.docker.com/admin) and select **Verify**.

1. Sign in to your domain host.
2. Add a TXT record to your DNS settings and save the record.
3. Wait up to 72 hours for TXT record verification.
4. After the record is live, go to **Domain management** in the [Admin Console](https://app.docker.com/admin) and select **Verify**.

## Next steps

- [Connect Docker and your IdP](https://docs.docker.com/enterprise/security/single-sign-on/connect/).
- [Troubleshoot](https://docs.docker.com/enterprise/troubleshoot/troubleshoot-sso/) SSO issues.

---

# Connect single sign

> Connect Docker and your identity provider, test the setup, and enable enforcement

# Connect single sign-on

   Table of contents

---

Subscription: Business Requires: Docker Desktop
[4.42](https://docs.docker.com/desktop/release-notes/#4420) and later For: Administrators

Setting up a single sign-on (SSO) connection involves configuring both Docker
and your identity provider (IdP). This guide walks you through setup
in Docker, setup in your IdP, and final connection.

> Tip
>
> You’ll copy and paste values between Docker and your IdP. Complete this guide
> in one session with separate browser windows open for Docker and your IdP.

## Supported identity providers

Docker supports any SAML 2.0 or OIDC-compatible identity provider. This guide
provides detailed setup instructions for the most commonly
used providers: Okta and Microsoft Entra ID.

If you're using a
different IdP, the general process remains the same:

1. Configure the connection in Docker.
2. Set up the application in your IdP using the values from Docker.
3. Complete the connection by entering your IdP's values back into Docker.
4. Test the connection.

## Prerequisites

Before you begin:

- Verify your domain
- Set up an account with your identity provider (IdP)
- Complete the steps in the [Configure single sign-on](https://docs.docker.com/enterprise/security/single-sign-on/configure/) guide

## Step one: Create an SSO connection in Docker

> Note
>
> You must
> [verify at least one domain](https://docs.docker.com/enterprise/security/single-sign-on/configure/) before creating an SSO connection.

1. Sign in to [Docker Home](https://app.docker.com) and choose your
  organization.
2. Select **Admin Console**, then **SSO and SCIM**.
3. Select **Create Connection** and provide a name for the connection.
4. Select an authentication method: **SAML** or **Azure AD (OIDC)**.
5. Copy the required values for your IdP:
  - Okta SAML: **Entity ID**, **ACS URL**
  - Azure OIDC: **Redirect URL**

Keep this window open to paste values from your IdP later.

## Step two: Create an SSO connection in your IdP

Use the following tabs based on your IdP provider.

1. Sign in to your Okta account and open the Admin portal.
2. Select **Administration** and then **Create App Integration**.
3. Select **SAML 2.0**, then **Next**.
4. Name your app "Docker".
5. Optional. Upload a logo.
6. Paste values from Docker:
  - Docker ACS URL -> **Single Sign On URL**
  - Docker Entity ID -> **Audience URI (SP Entity ID)**
7. Configure the following settings:
  - Name ID format: `EmailAddress`
  - Application username: `Email`
  - Update application on: `Create and update`
8. Optional. Add SAML attributes. See
  [SSO attributes](https://docs.docker.com/enterprise/security/provisioning/#sso-attributes).
9. Select **Next**.
10. Select the **This is an internal app that we have created** checkbox.
11. Select **Finish**.

1. Sign in to Microsoft Entra (formerly Azure AD).
2. Select **Default Directory** > **Add** > **Enterprise Application**.
3. Choose **Create your own application**, name it "Docker", and choose **Non-gallery**.
4. After creating your app, go to **Single Sign-On** and select **SAML**.
5. Select **Edit** on the **Basic SAML configuration** section.
6. Edit **Basic SAML configuration** and paste values from Docker:
  - Docker Entity ID -> **Identifier**
  - Docker ACS URL -> **Reply URL**
7. Optional. Add SAML attributes. See
  [SSO attributes](https://docs.docker.com/enterprise/security/provisioning/#sso-attributes).
8. Save the configuration.
9. From the **SAML Signing Certificate** section, download your **Certificate (Base64)**.

### Register the app

1. Sign in to Microsoft Entra (formerly Azure AD).
2. Select **App Registration** > **New Registration**.
3. Name the application "Docker".
4. Set account types and paste the **Redirect URI** from Docker.
5. Select **Register**.
6. Copy the **Client ID**.

### Create client secrets

1. In your app, go to **Certificates & secrets**.
2. Select **New client secret**, describe and configure duration, then **Add**.
3. Copy the **value** of the new secret.

### Set API permissions

1. In your app, go to **API permissions**.
2. Select **Grant admin consent** and confirm.
3. Select **Add a permissions** > **Delegated permissions**.
4. Search and select `User.Read`.
5. Confirm that admin consent is granted.

## Step three: Connect Docker to your IdP

Complete the integration by pasting your IdP values into Docker.

1. In Okta, select your app and go to **View SAML setup instructions**.
2. Copy the **SAML Sign-in URL** and **x509 Certificate**.
  > Important
  >
  > Copy the entire certificate, including `----BEGIN CERTIFICATE----` and `----END CERTIFICATE----` lines.
3. Return to the Docker Admin Console.
4. Paste the **SAML Sign-in URL** and **x509 Certificate** values.
5. Optional. Select a default team.
6. Review and select **Create connection**.

1. Open your downloaded **Certificate (Base64)** in a text editor.
2. Copy the following values:
  - From Azure AD: **Login URL**
  - **Certificate (Base64)** contents
  > Important
  >
  > Copy the entire certificate, including `----BEGIN CERTIFICATE----` and `----END CERTIFICATE----` lines.
3. Return to the Docker Admin Console.
4. Paste the **Login URL** and **Certificate (Base64)** values.
5. Optional. Select a default team.
6. Review and select **Create connection**.

1. Return to the Docker Admin Console.
2. Paste the following values:
  - **Client ID**
  - **Client Secret**
  - **Azure AD Domain**
3. Optional. Select a default team.
4. Review and select **Create connection**.

## Step four: Test the connection

1. Open an incognito browser window.
2. Sign in to the Admin Console using your **domain email address**.
3. The browser will redirect to your identity provider's sign in page to authenticate. If you have [multiple IdPs](#optional-configure-multiple-idps), choose the sign sign-in option **Continue with SSO**.
4. Authenticate through your domain email instead of using your Docker ID.

If you're using the CLI, you must authenticate using a personal access token.

## Optional: Configure multiple IdPs

Docker supports multiple IdP configurations. To use multiple IdPs with one domain:

- Repeat Steps 1-4 on this page for each IdP.
- Each connection must use the same domain.
- Users will select **Continue with SSO** to choose their IdP at sign in.

## Optional: Enforce SSO

> Important
>
> If SSO is not enforced, users can still sign in using Docker usernames and passwords.

Enforcing SSO requires users to use SSO when signing into Docker. This centralizes authentication and enforces policies set by the IdP.

1. Sign in to [Docker Home](https://app.docker.com/) and select
  your organization or company.
2. Select **Admin Console**, then **SSO and SCIM**.
3. In the SSO connections table, select the **Action** menu, then **Enable enforcement**.
4. Follow the on-screen instructions.
5. Select **Turn on enforcement**.

When SSO is enforced, your users are unable to modify their email address and
password, convert a user account to an organization, or set up 2FA through
Docker Hub. If you want to use 2FA, you must enable 2FA through your IdP.

## Next steps

- [Provision users](https://docs.docker.com/enterprise/security/provisioning/).
- [Enforce sign-in](https://docs.docker.com/enterprise/security/enforce-sign-in/).
- [Create personal access tokens](https://docs.docker.com/enterprise/security/access-tokens/).
- [Troubleshoot SSO](https://docs.docker.com/enterprise/troubleshoot/troubleshoot-sso/) issues.

---

# SSO domain FAQs

> Frequently asked questions about domain verification and management for Docker single sign-on

# SSO domain FAQs

   Table of contents

---

## Can I add sub-domains?

Yes, you can add sub-domains to your SSO connection. All email addresses must use domains you've added to the connection. Verify that your DNS provider supports multiple TXT records for the same domain.

## Do I need to keep the DNS TXT record permanently?

You can remove the TXT record after one-time verification to add the domain. However, if your organization changes identity providers and needs to set up SSO again, you'll need to verify the domain again.

## Can I verify the same domain for multiple organizations?

You can't verify the same domain for multiple organizations at the organization level. To verify one domain for multiple organizations, you must have a Docker Business subscription and create a company. Companies allow centralized management of organizations and domain verification at the company level.

---

# SSO enforcement FAQs

> Frequently asked questions about Docker single sign-on enforcement and its effects on users

# SSO enforcement FAQs

   Table of contents

---

## Does Docker SSO support authenticating through the command line?

When SSO is enforced,
[passwords are prevented from accessing the Docker CLI](https://docs.docker.com/security/security-announcements/#deprecation-of-password-logins-on-cli-when-sso-enforced). You must use a personal access token (PAT) for CLI authentication instead.

Each user must create a PAT to access the CLI. To learn how to create a PAT, see
[Manage personal access tokens](https://docs.docker.com/security/access-tokens/). Users who already used a PAT before SSO enforcement can continue using that PAT.

## How does SSO affect automation systems and CI/CD pipelines?

Before enforcing SSO, you must
[create personal access tokens](https://docs.docker.com/security/access-tokens/) to replace passwords in automation systems and CI/CD pipelines.

## Can I turn on SSO without enforcing it immediately?

Yes, you can turn on SSO without enforcement. Users can choose between Docker ID (standard email and password) or domain-verified email address (SSO) at the sign-in screen.

## SSO is enforced, but a user can sign in using a username and password. Why is this happening?

Guest users who aren't part of your registered domain but have been invited to your organization don't sign in through your SSO identity provider. SSO enforcement only applies to users who belong to your verified domain.

## Can I test SSO functionality before going to production?

Yes, you can create a test organization with a 5-seat Business subscription. When testing, turn on SSO but don't enforce it, or all domain email users will be forced to sign in to the test environment.

## What is enforcing SSO versus enforcing sign-in?

These are separate features you can use independently or together:

- Enforcing SSO ensures users sign in using SSO credentials instead of their Docker ID, enabling better credential management.
- Enforcing sign-in to Docker Desktop ensures users always sign in to accounts that are members of your organization, so security settings and subscription benefits are always applied.

For more details, see
[Enforce sign-in for Desktop](https://docs.docker.com/enterprise/security/enforce-sign-in/#enforcing-sign-in-versus-enforcing-single-sign-on-sso).

---

# General SSO FAQs

> Frequently asked questions about Docker single sign-on

# General SSO FAQs

   Table of contents

---

## What SSO flows does Docker support?

Docker supports Service Provider Initiated (SP-initiated) SSO flow. Users must sign in to Docker Hub or Docker Desktop to initiate the SSO authentication process.

## Does Docker SSO support multi-factor authentication?

When an organization uses SSO, multi-factor authentication is controlled at the identity provider level, not on the Docker platform.

## Can I retain my Docker ID when using SSO?

Users with personal Docker IDs retain ownership of their repositories, images, and assets. When SSO is enforced, existing accounts with company domain emails are connected to the organization. Users signing in without existing accounts automatically have new accounts and Docker IDs created.

## Are there any firewall rules required for SSO configuration?

No specific firewall rules are required as long as `login.docker.com` is accessible. This domain is commonly accessible by default, but some organizations may need to allow it in their firewall settings if SSO setup encounters issues.

## Does Docker use my IdP's default session timeout?

Yes, Docker supports your IdP's session timeout using a custom `dockerSessionMinutes` SAML attribute instead of the standard `SessionNotOnOrAfter` element. See
[SSO attributes](https://docs.docker.com/enterprise/security/provisioning/#sso-attributes) for more information.

---

# SSO identity provider FAQs

> Frequently asked questions about Docker SSO and identity provider configuration

# SSO identity provider FAQs

   Table of contents

---

## Can I use multiple identity providers with Docker SSO?

Yes, Docker supports multiple IdP configurations. A domain can be associated with multiple IdPs. Docker supports Entra ID (formerly Azure AD) and identity providers that support SAML 2.0.

## Can I change my identity provider after configuring SSO?

Yes. Delete your existing IdP configuration in your Docker SSO connection, then
[configure SSO using your new IdP](https://docs.docker.com/enterprise/security/single-sign-on/connect/). If you had already turned on enforcement, turn off enforcement before updating the provider connection.

## What information do I need from my identity provider to configure SSO?

To turn on SSO in Docker, you need the following from your IdP:

- SAML: Entity ID, ACS URL, Single Logout URL, and the public X.509 certificate
- Entra ID (formerly Azure AD): Client ID, Client Secret, AD Domain

## What happens if my existing certificate expires?

If your certificate expires, contact your identity provider to retrieve a new X.509 certificate. Then update the certificate in the
[SSO configuration settings](https://docs.docker.com/enterprise/security/single-sign-on/manage/#manage-sso-connections) in the Docker Admin Console.

## What happens if my IdP goes down when SSO is turned on?

If SSO is enforced, users can't access Docker Hub when your IdP is down. Users can still access Docker Hub images from the CLI using personal access tokens.

If SSO is turned on but not enforced, users can fall back to username/password authentication.

## Do bot accounts need seats to access organizations using SSO?

Yes, bot accounts need seats like regular users, requiring a non-aliased domain email in the IdP and using a seat in Docker Hub. You can add bot accounts to your IdP and create access tokens to replace other credentials.

## Does SAML SSO use Just-in-Time provisioning?

The SSO implementation uses Just-in-Time (JIT) provisioning by default. You can optionally turn off JIT in the Admin Console if you turn on auto-provisioning using SCIM. See
[Just-in-Time provisioning](https://docs.docker.com/security/for-admins/provisioning/just-in-time/).

## My Entra ID SSO connection isn't working and shows an error. How can I troubleshoot this?

Confirm that you've configured the necessary API permissions in Entra ID for your SSO connection. You need to grant administrator consent within your Entra ID tenant. See [Entra ID (formerly Azure AD) documentation](https://learn.microsoft.com/en-us/azure/active-directory/manage-apps/grant-admin-consent?pivots=portal#grant-admin-consent-in-app-registrations).
