# Settings Management and more

# Settings Management

> Understand how Settings Management works, who it's for, and the benefits it provides

# Settings Management

   Table of contents

---

Subscription: Business For: Administrators

Settings Management lets administrators configure and enforce Docker Desktop settings across end-user machines. It helps maintain consistent configurations and enhances security within your organization.

## Who should use Settings Management?

Settings Management is designed for organizations that:

- Need centralized control over Docker Desktop configurations
- Want to standardize Docker Desktop environments across teams
- Operate in regulated environments and must enforce compliance policies

## How Settings Management works

Administrators can define settings using one of these methods:

- [Admin Console](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/configure-admin-console/): Create and assign settings policies through the
  Docker Admin Console. This provides a web-based interface for managing settings
  across your organization.
- [admin-settings.jsonfile](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/configure-json-file/): Place a configuration file on the
  user's machine to enforce settings. This method works well for automated
  deployments and scripted installations.

Enforced settings override user-defined configurations and can't be modified by developers.

## Configurable settings

Settings Management supports a wide range of Docker Desktop features, including:

- Proxy configurations
- Network settings
- Container isolation options
- Registry access controls
- Resource limits
- Security policies
- Cloud policies

For a complete list of settings you can enforce, see the
[Settings reference](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/settings-reference/).

## Policy precedence

When multiple policies exist, Docker Desktop applies them in this order:

1. User-specific policies: Highest priority
2. Organization default policy: Applied when no user-specific policy exists
3. Local `admin-settings.json` file: Lowest priority, overridden by Admin Console policies
4. [Configuration profiles](https://docs.docker.com/enterprise/security/enforce-sign-in/methods/#configuration-profiles-method-mac-only): Super-set of Docker Admin Console policies. Available with Docker Desktop version 4.48 and later.

## Set up Settings Management

1. Check that you have
  [added and verified](https://docs.docker.com/enterprise/security/domain-management/#add-and-verify-a-domain) your organization's domain.
2. [Enforce sign-in](https://docs.docker.com/enterprise/security/enforce-sign-in/) to
  ensure all developers authenticate with your organization.
3. Choose a configuration method:
  - Use the `--admin-settings` installer flag on
    [macOS](https://docs.docker.com/desktop/setup/install/mac-install/#install-from-the-command-line) or
    [Windows](https://docs.docker.com/desktop/setup/install/windows-install/#install-from-the-command-line) to automatically create the `admin-settings.json`.
  - Manually create and configure the
    [admin-settings.jsonfile](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/configure-json-file/).
  - Create a settings policy in the [Docker Admin Console](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/configure-admin-console/).

After configuration, developers receive the enforced settings when they:

- Quit and relaunch Docker Desktop, then sign in
- Launch and sign in to Docker Desktop for the first time

> Note
>
> Docker Desktop doesn't automatically prompt users to restart or re-authenticate after a settings change. You may need to communicate these requirements to your developers.

## Developer experience

When settings are enforced:

- Settings options appear grayed out in Docker Desktop and can't be modified through the Dashboard, CLI, or configuration files
- If Enhanced Container Isolation is enabled, developers can't use privileged containers or similar methods to alter enforced settings within the Docker Desktop Linux VM

This ensures consistent environments while maintaining a clear visual indication of which settings are managed by administrators.

## View applied settings

When administrators apply Settings Management policies, Docker Desktop greys out most enforced settings in the GUI.

The Docker Desktop GUI doesn't currently display all centralized settings,
particularly Enhanced Container Isolation (ECI) settings that administrators
apply via the Admin Console.

As a workaround, you can check the `settings-store.json` file to view all
applied settings:

- Mac: `~/Library/Application Support/Docker/settings-store.json`
- Windows: `%APPDATA%\Docker\settings-store.json`
- Linux: `~/.docker/desktop/settings-store.json`

The `settings-store.json` file contains all settings, including those that
may not appear in the Docker Desktop GUI.

## Limitations

Settings Management has the following limitations:

- Doesn't work in air-gapped or offline environments
- Not compatible with environments that restrict authentication with Docker Hub

## Next steps

Get started with Settings Management:

- [Configure Settings Management with theadmin-settings.jsonfile](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/configure-json-file/)
- [Configure Settings Management with the Docker Admin Console](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/configure-admin-console/)

---

# Hardened Docker Desktop

> Security features that help organizations secure developer environments without impacting productivity

# Hardened Docker Desktop

   Table of contents

---

Subscription: Business For: Administrators

Hardened Docker Desktop provides a collection of security features designed to strengthen developer environments without compromising productivity or developer experience.

With Hardened Docker Desktop, you can enforce strict security policies that prevent developers and containers from bypassing organizational controls. You can also enhance container isolation to protect against security threats like malicious payloads that might breach the Docker Desktop Linux VM or underlying host system.

## Who should use Hardened Docker Desktop?

Hardened Docker Desktop is ideal for security-focused organizations that:

- Don't provide root or administrator access to developers' machines
- Want centralized control over Docker Desktop configurations
- Must meet specific compliance requirements

## How Hardened Docker Desktop works

Hardened Docker Desktop features work independently and together to create a defense-in-depth security strategy. They protect developer workstations against attacks across multiple layers, including Docker Desktop configuration, container image management, and container runtime security:

- Registry Access Management and Image Access Management prevent access to unauthorized container registries and image types, reducing exposure to malicious payloads
- Enhanced Container Isolation runs containers without root privileges inside a Linux user namespace, limiting the impact of malicious containers
- Air-gapped containers let you configure network restrictions for containers, preventing malicious containers from accessing your organization's internal network resources
- Settings Management locks down Docker Desktop configurations to enforce company policies and prevent developers from introducing insecure settings, whether intentionally or accidentally

## Next steps

Explore Hardened Docker Desktop features to understand how they can strengthen your organization's security posture:

[Settings ManagementLearn how Settings Management can secure your developers' workflows.](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/)[Enhanced Container IsolationUnderstand how Enhanced Container Isolation can prevent container attacks.](https://docs.docker.com/enterprise/security/hardened-desktop/enhanced-container-isolation/)[Registry Access ManagementControl the registries developers can access while using Docker Desktop.](https://docs.docker.com/enterprise/security/hardened-desktop/registry-access-management/)[Image Access ManagementControl the images developers can pull from Docker Hub.](https://docs.docker.com/enterprise/security/hardened-desktop/image-access-management/)[Air-Gapped ContainersRestrict containers from accessing unwanted network resources.](https://docs.docker.com/enterprise/security/hardened-desktop/air-gapped-containers/)

---

# Group mapping

> Automate team membership by syncing identity provider groups with Docker teams

# Group mapping

   Table of contents

---

Subscription: Business Requires: Docker Desktop
[4.42](https://docs.docker.com/desktop/release-notes/#4420) and later For: Administrators

Group mapping automatically synchronizes user groups from your identity provider (IdP) with teams in your Docker organization. For example, when you add a developer to the "backend-team" group in your IdP, they're automatically added to the corresponding team in Docker

This page explains how group mapping works, and how to set up group mapping.

> Tip
>
> Group mapping is ideal for adding users to multiple organizations or multiple teams within one organization. If you don't need to set up multi-organization or multi-team assignment, SCIM [user-level attributes](https://docs.docker.com/enterprise/security/provisioning/scim/#set-up-role-mapping) may be a better fit for your needs.

## Prerequisites

Before you being, you must have:

- SSO configured for your organization
- Administrator access to Docker Home and your identity provider

## How group mapping works

Group mapping keeps your Docker teams synchronized with your IdP groups through these key components:

- Authentication flow: When users sign in through SSO, your IdP shares user attributes with Docker including email, name, and group memberships.
- Automatic updates: Docker uses these attributes to create or update user profiles and manage team assignments based on IdP group changes.
- Unique identification: Docker uses email addresses as unique identifiers, so each Docker account must have a unique email address.
- Team synchronization: Users' team memberships in Docker automatically reflect changes made in your IdP groups.

## Set up group mapping

Group mapping setup involves configuring your identity provider to share group
information with Docker. This requires:

- Creating groups in your IdP using Docker's naming format
- Configuring attributes so your IdP sends group data during authentication
- Adding users to the appropriate groups
- Testing the connection to ensure groups sync properly

You can use group mapping with SSO only, or with both SSO and SCIM for enhanced
user lifecycle management.

### Group naming format

Create groups in your IdP using the format: `organization:team`.

For example:

- For the "developers" team in the "moby" organization: `mobdy:developers`
- For multi-organization access: `moby:backend` and `whale:desktop`

Docker creates teams automatically if they don't already exist when groups sync.

### Supported attributes

| Attribute | Description |
| --- | --- |
| id | Unique ID of the group in UUID format. This attribute is read-only. |
| displayName | Name of the group following the group mapping format:organization:team. |
| members | A list of users that are members of this group. |
| members(x).value | Unique ID of the user that is a member of this group. Members are referenced by ID. |

## Configure group mapping with SSO

Use group mapping with SSO connections that use the SAML authentication method.

> Note
>
> Group mapping with SSO isn't supported with the Azure AD (OIDC) authentication method. SCIM isn't required for these configurations.

The user interface for your IdP may differ slightly from the following steps. Refer to the [Okta documentation](https://help.okta.com/oie/en-us/content/topics/apps/define-group-attribute-statements.htm) to verify.

To set up group mapping:

1. Sign in to Okta and open your application.
2. Navigate to the **SAML Settings** page for your application.
3. In the **Group Attribute Statements (optional)** section, configure like the following:
  - **Name**: `groups`
  - **Name format**: `Unspecified`
  - **Filter**: `Starts with` + `organization:` where `organization` is the name of your organization
    The filter option will filter out the groups that aren't affiliated with your Docker organization.
4. Create your groups by selecting **Directory**, then **Groups**.
5. Add your groups using the format `organization:team` that matches the names of your organization(s) and team(s) in Docker.
6. Assign users to the group(s) that you create.

The next time you sync your groups with Docker, your users will map to the Docker groups you defined.

The user interface for your IdP may differ slightly from the following steps. Refer to the [Entra ID documentation](https://learn.microsoft.com/en-us/azure/active-directory/app-provisioning/customize-application-attributes) to verify.

To set up group mapping:

1. Sign in to Entra ID and open your application.
2. Select **Manage**, then **Single sign-on**.
3. Select **Add a group claim**.
4. In the Group Claims section, select **Groups assigned to the application** with the source attribute **Cloud-only group display names (Preview)**.
5. Select **Advanced options**, then the **Filter groups** option.
6. Configure the attribute like the following:
  - **Attribute to match**: `Display name`
  - **Match with**: `Contains`
  - **String**: `:`
7. Select **Save**.
8. Select **Groups**, **All groups**, then **New group** to create your group(s).
9. Assign users to the group(s) that you create.

The next time you sync your groups with Docker, your users will map to the Docker groups you defined.

## Configure group mapping with SCIM

Use group mapping with SCIM for more advanced user lifecycle management. Before you begin, make sure you [set up SCIM](https://docs.docker.com/enterprise/security/provisioning/scim/#enable-scim) first.

The user interface for your IdP may differ slightly from the following steps. Refer to the [Okta documentation](https://help.okta.com/en-us/Content/Topics/users-groups-profiles/usgp-enable-group-push.htm) to verify.

To set up your groups:

1. Sign in to Okta and open your application.
2. Select **Applications**, then **Provisioning**, and **Integration**.
3. Select **Edit** to enable groups on your connection, then select **Push groups**.
4. Select **Save**. Saving this configuration will add the **Push Groups** tab to your application.
5. Create your groups by navigating to **Directory** and selecting **Groups**.
6. Add your groups using the format `organization:team` that matches the names of your organization(s) and team(s) in Docker.
7. Assign users to the group(s) that you create.
8. Return to the **Integration** page, then select the **Push Groups** tab to open the view where you can control and manage how groups are provisioned.
9. Select **Push Groups**, then **Find groups by rule**.
10. Configure the groups by rule like the following:
  - Enter a rule name, for example `Sync groups with Docker Hub`
  - Match group by name, for example starts with `docker:` or contains `:` for multi-organization
  - If you enable **Immediately push groups by rule**, sync will happen as soon as there's a change to the group or group assignments. Enable this if you don't want to manually push groups.

Find your new rule under **By rule** in the **Pushed Groups** column. The groups that match that rule are listed in the groups table on the right-hand side.

To push the groups from this table:

1. Select **Group in Okta**.
2. Select the **Push Status** drop-down.
3. Select **Push Now**.

The user interface for your IdP may differ slightly from the following steps. Refer to the [Entra ID documentation](https://learn.microsoft.com/en-us/azure/active-directory/app-provisioning/customize-application-attributes) to verify.

Complete the following before configuring group mapping:

1. Sign in to Entra ID and go to your application.
2. In your application, select **Provisioning**, then **Mappings**.
3. Select **Provision Microsoft Entra ID Groups**.
4. Select **Show advanced options**, then **Edit attribute list**.
5. Update the `externalId` type to `reference`, then select the **Multi-Value** checkbox and choose the referenced object attribute `urn:ietf:params:scim:schemas:core:2.0:Group`.
6. Select **Save**, then **Yes** to confirm.
7. Go to **Provisioning**.
8. Toggle **Provision Status** to **On**, then select **Save**.

Next, set up group mapping:

1. Go to the application overview page.
2. Under **Provision user accounts**, select **Get started**.
3. Select **Add user/group**.
4. Create your group(s) using the `organization:team` format.
5. Assign the group to the provisioning group.
6. Select **Start provisioning** to start the sync.

To verify, select **Monitor**, then **Provisioning logs** to see that your groups were provisioned successfully. In your Docker organization, you can check that the groups were correctly provisioned and the members were added to the appropriate teams.

Once complete, a user who signs in to Docker through SSO is automatically added to the organizations and teams mapped in the IdP.

> Tip
>
> [Enable SCIM](https://docs.docker.com/enterprise/security/provisioning/scim/) to take advantage of automatic user provisioning and de-provisioning. If you don't enable SCIM users are only automatically provisioned. You have to de-provision them manually.

---

# Just

> Learn how Just-in-Time provisioning works with your SSO connection.

# Just-in-Time provisioning

   Table of contents

---

Subscription: Business Requires: Docker Desktop
[4.42](https://docs.docker.com/desktop/release-notes/#4420) and later For: Administrators

Just-in-Time (JIT) provisioning streamlines user onboarding by automatically creating and updating user accounts during SSO authentication. This eliminates manual account creation and ensures users have immediate access to your organization's resources. JIT verifies that users belong to the organization and assigns them to the appropriate teams based on your identity provider (IdP) configuration. When you create your SSO connection, JIT provisioning is turned on by default.

This page explains how JIT provisioning works, SSO authentication flows, and how to disable JIT provisioning.

## Prerequisites

Before you begin, you must have:

- SSO configured for your organization
- Administrator access to Docker Home and your identity provider

## SSO authentication with JIT provisioning enabled

When a user signs in with SSO and you have JIT provisioning enabled, the following steps occur automatically:

1. The system checks if a Docker account exists for the user's email address.
  - If an account exists: The system uses the existing account and updates the user's full name if necessary.
  - If no account exists: A new Docker account is created using basic user attributes (email, name, and surname). A unique username is generated based on the user's email, name, and random numbers to ensure all usernames are unique across the platform.
2. The system checks for any pending invitations to the SSO organization.
  - Invitation found: The invitation is automatically accepted.
  - Invitation includes a specific group: The user is added to that group within the SSO organization.
3. The system verifies if the IdP has shared group mappings during authentication.
  - Group mappings provided: The user is assigned to the relevant organizations and teams.
  - No group mappings provided: The system checks if the user is already part of the organization. If not, the user is added to the default organization and team configured in the SSO connection.

The following graphic provides an overview of SSO authentication with JIT enabled:

![JIT provisioning enabled workflow](https://docs.docker.com/enterprise/security/images/jit-enabled-flow.svg)  ![JIT provisioning enabled workflow](https://docs.docker.com/enterprise/security/images/jit-enabled-flow.svg)

## SSO authentication with JIT provisioning disabled

When JIT provisioning is disabled, the following actions occur during SSO authentication:

1. The system checks if a Docker account exists for the user's email address.
  - If an account exists: The system uses the existing account and updates the user's full name if necessary.
  - If no account exists: A new Docker account is created using basic user attributes (email, name, and surname). A unique username is generated based on the user's email, name, and random numbers to ensure all usernames are unique across the platform.
2. The system checks for any pending invitations to the SSO organization.
  - Invitation found: If the user is a member of the organization or has a pending invitation, sign-in is successful, and the invitation is automatically accepted.
  - No invitation found: If the user is not a member of the organization and has no pending invitation, the sign-in fails, and an `Access denied` error appears. The user must contact an administrator to be invited to the organization.

With JIT disabled, group mapping is only available if you have [SCIM enabled](https://docs.docker.com/enterprise/security/provisioning/scim/#enable-scim-in-docker). If SCIM is not enabled, users won't be auto-provisioned to groups.

The following graphic provides an overview of SSO authentication with JIT disabled:

![JIT provisioning disabled workflow](https://docs.docker.com/enterprise/security/images/jit-disabled-flow.svg)  ![JIT provisioning disabled workflow](https://docs.docker.com/enterprise/security/images/jit-disabled-flow.svg)

## Disable JIT provisioning

> Warning
>
> Disabling JIT provisioning may disrupt your users' access and workflows. With JIT disabled, users will not be automatically added to your organization. Users must already be a member of the organization or have a pending invitation to successfully sign in through SSO. To auto-provision users with JIT disabled, [use SCIM](https://docs.docker.com/enterprise/security/provisioning/scim/).

You may want to disable JIT provisioning for reasons such as the following:

- You have multiple organizations, have SCIM enabled, and want SCIM to be the source of truth for provisioning
- You want to control and restrict usage based on your organization's security configuration, and want to use SCIM to provision access

Users are provisioned with JIT by default. If you enable SCIM, you can disable JIT:

1. Go to [Docker Home](https://app.docker.com/) and select your organization from the top-left account drop-down.
2. Select **Admin Console**, then **SSO and SCIM**.
3. In the **SSO connections** table, select the **Action** icon, then select **Disable JIT provisioning**.
4. Select **Disable** to confirm.

## Next steps

- Configure
  [SCIM provisioning](https://docs.docker.com/enterprise/security/provisioning/scim/) for advanced user management.
- Set up
  [group mapping](https://docs.docker.com/enterprise/security/provisioning/group-mapping/) to automatically assign users to teams.
- Review
  [Troubleshoot provisioning](https://docs.docker.com/enterprise/troubleshoot/troubleshoot-provisioning/).

---

# SCIM provisioning

> Learn how System for Cross-domain Identity Management works and how to set it up.

# SCIM provisioning

   Table of contents

---

Subscription: Business Requires: Docker Desktop
[4.42](https://docs.docker.com/desktop/release-notes/#4420) and later For: Administrators

Automate user management for your Docker organization using System for
Cross-domain Identity Management (SCIM). SCIM automatically provisions and
de-provisions users, synchronizes team memberships, and keeps your Docker
organization in sync with your identity provider.

This page shows you how to automate user provisioning and de-provisioning for
Docker using SCIM.

## Prerequisites

Before you begin, you must have:

- SSO configured for your organization
- Administrator access to Docker Home and your identity provider

## How SCIM works

SCIM automates user provisioning and de-provisioning for Docker through your
identity provider. After you enable SCIM, any user assigned to your
Docker application in your identity provider is automatically provisioned and
added to your Docker organization. When a user is removed from the Docker
application in your identity provider, SCIM deactivates and removes them from
your Docker organization.

In addition to provisioning and removal, SCIM also syncs profile updates like
name changes made in your identity provider. You can use SCIM alongside Docker's
default Just-in-Time (JIT) provisioning or on its own with JIT disabled.

SCIM automates:

- Creating users
- Updating user profiles
- Removing and deactivating users
- Re-activating users
- Group mapping

> Note
>
> SCIM only manages users provisioned through your identity provider after
> SCIM is enabled. It cannot remove users who were manually added to your Docker
> organization before SCIM was set up.
>
>
>
> To remove those users, delete them manually from your Docker organization.
> For more information, see
> [Manage organization members](https://docs.docker.com/admin/organization/members/).

## Supported attributes

SCIM uses attributes (name, email, etc.) to sync user information between your
identity provider and Docker. Properly mapping these attributes in your identity
provider ensures that user provisioning works smoothly and prevents issues like
duplicate user accounts
when using single sign-on.

Docker supports the following SCIM attributes:

| Attribute | Description |
| --- | --- |
| userName | User's primary email address, used as the unique identifier |
| name.givenName | User's first name |
| name.familyName | User's surname |
| active | Indicates if a user is enabled or disabled, set to "false" to de-provision a user |

For additional details about supported attributes and SCIM, see
[Docker Hub API SCIM reference](https://docs.docker.com/reference/api/hub/latest/#tag/scim).

> Important
>
> By default, Docker uses Just-in-Time (JIT) provisioning for SSO. If SCIM is
> enabled, JIT values still take precedence and will overwrite attribute values
> set by SCIM. To avoid conflicts, make sure your JIT attribute values match
> your SCIM values.
>
>
>
> Alternatively, you can disable JIT provisioning to rely solely on SCIM.
> For details, see [Just-in-Time](https://docs.docker.com/enterprise/security/provisioning/just-in-time/).

## Enable SCIM in Docker

To enable SCIM:

1. Sign in to [Docker Home](https://app.docker.com).
2. Select **Admin Console**, then **SSO and SCIM**.
3. In the **SSO connections** table, select the **Actions** icon for your
  connection, then select **Setup SCIM**.
4. Copy the **SCIM Base URL** and **API Token** and paste the values into your
  IdP.

## Enable SCIM in your IdP

The user interface for your identity provider may differ slightly from the
following steps. You can refer to the documentation for your identity provider
to verify. For additional details, see the documentation for your identity
provider:

- [Okta](https://help.okta.com/en-us/Content/Topics/Apps/Apps_App_Integration_Wizard_SCIM.htm)
- [Entra ID/Azure AD SAML 2.0](https://learn.microsoft.com/en-us/azure/active-directory/app-provisioning/user-provisioning)

> Note
>
> Microsoft does not currently support SCIM and OIDC in the same non-gallery
> application in Entra ID. This page provides a verified workaround using a
> separate non-gallery app for SCIM provisioning. While Microsoft does not
> officially document this setup, it is widely used and supported in practice.

### Step one: Enable SCIM

1. Sign in to Okta and select **Admin** to open the admin portal.
2. Open the application you created when you configured your SSO connection.
3. On the application page, select the **General** tab, then
  **Edit App Settings**.
4. Enable SCIM provisioning, then select **Save**.
5. Navigate to the **Provisioning**, then select **Edit SCIM Connection**.
6. To configure SCIM in Okta, set up your connection using the following
  values and settings:
  - SCIM Base URL: SCIM connector base URL (copied from Docker Home)
  - Unique identifier field for users: `email`
  - Supported provisioning actions: **Push New Users** and
    **Push Profile Updates**
  - Authentication Mode: HTTP Header
  - SCIM Bearer Token: HTTP Header Authorization Bearer Token
    (copied from Docker Home)
7. Select **Test Connector Configuration**.
8. Review the test results and select **Save**.

### Step two: Enable synchronization

1. In Okta, select **Provisioning**.
2. Select **To App**, then **Edit**.
3. Enable **Create Users**, **Update User Attributes**, and **Deactivate Users**.
4. Select **Save**.
5. Remove unnecessary mappings. The necessary mappings are:
  - Username
  - Given name
  - Family name
  - Email

Next, [set up role mapping](#set-up-role-mapping).

Microsoft does not support SCIM and OIDC in the same non-gallery application.
You must create a second non-gallery application in Entra ID for SCIM
provisioning.

### Step one: Create a separate SCIM app

1. In the Azure Portal, go to **Microsoft Entra ID** >
  **Enterprise Applications** > **New application**.
2. Select **Create your own application**.
3. Name your application and choose
  **Integrate any other application you don't find in the gallery**.
4. Select **Create**.

### Step two: Configure SCIM provisioning

1. In your new SCIM application, go to **Provisioning** > **Get started**.
2. Set **Provisioning Mode** to **Automatic**.
3. Under **Admin Credentials**:
  - **Tenant URL**: Paste the **SCIM Base URL** from Docker Home.
  - **Secret Token**: Paste the **SCIM API token** from Docker Home.
4. Select **Test Connection** to verify.
5. Select **Save** to store credentials.

Next, [set up role mapping](#set-up-role-mapping).

1. In the Azure Portal, go to **Microsoft Entra ID** >
  **Enterprise Applications**, and select your Docker SAML app.
2. Select **Provisioning** > **Get started**.
3. Set **Provisioning Mode** to **Automatic**.
4. Under **Admin Credentials**:
  - **Tenant URL**: Paste the **SCIM Base URL** from Docker Home.
  - **Secret Token**: Paste the **SCIM API token** from Docker Home.
5. Select **Test Connection** to verify.
6. Select **Save** to store credentials.

Next, [set up role mapping](#set-up-role-mapping).

## Set up role mapping

You can assign [Docker roles](https://docs.docker.com/enterprise/security/roles-and-permissions/) to
users by adding optional SCIM attributes in your IdP. These attributes override
default role and team values set in your SSO configuration.

> Note
>
> Role mappings are supported for both SCIM and Just-in-Time (JIT)
> provisioning. For JIT, role mapping applies only when the user is first
> provisioned.

The following table lists the supported optional user-level attributes:

| Attribute | Possible values | Notes |
| --- | --- | --- |
| dockerRole | member,editor, orowner | If not set, the user defaults to thememberrole. Setting this attribute overrides the default.For role definitions, seeRoles and permissions. |
| dockerOrg | DockerorganizationName(e.g.,moby) | Overrides the default organization configured in your SSO connection.If unset, the user is provisioned to the default organization. IfdockerOrganddockerTeamare both set, the user is provisioned to the team within the specified organization. |
| dockerTeam | DockerteamName(e.g.,developers) | Provisions the user to the specified team in the default or specified organization. If the team doesn't exist, it is automatically created.You can still usegroup mappingto assign users to multiple teams across organizations. |

The external namespace used for these attributes is: `urn:ietf:params:scim:schemas:extension:docker:2.0:User`.
This value is required in your identity provider when creating custom SCIM attributes for Docker.

### Step one: Set up role mapping in Okta

1. Setup [SSO](https://docs.docker.com/enterprise/security/single-sign-on/configure/) and SCIM first.
2. In the Okta admin portal, go to **Directory**, select **Profile Editor**,
  and then **User (Default)**.
3. Select **Add Attribute** and configure the values for the role, organization,
  or team you want to add. Exact naming isn't required.
4. Return to the **Profile Editor** and select your application.
5. Select **Add Attribute** and enter the required values. The **External Name**
  and **External Namespace** must be exact.
  - The external name values for organization/team/role mapping are
    `dockerOrg`, `dockerTeam`, and `dockerRole` respectively, as listed in the previous table.
  - The external namespace is the same for all of them:
    `urn:ietf:params:scim:schemas:extension:docker:2.0:User`.
6. After creating the attributes, navigate to the top of the page and select
  **Mappings**, then **Okta User to YOUR APP**.
7. Go to the newly created attributes and map the variable names to the external
  names, then select **Save Mappings**. If you're using JIT provisioning, continue
  to the following steps.
8. Navigate to **Applications** and select **YOUR APP**.
9. Select **General**, then **SAML Settings**, and **Edit**.
10. Select **Step 2** and configure the mapping from the user attribute to the
  Docker variables.

### Step two: Assign roles by user

1. In the Okta Admin portal, select **Directory**, then **People**.
2. Select **Profile**, then **Edit**.
3. Select **Attributes** and update the attributes to the desired values.

### Step three: Assign roles by group

1. In the Okta Admin portal, select **Directory**, then **People**.
2. Select **YOUR GROUP**, then **Applications**.
3. Open **YOUR APPLICATION** and select the **Edit** icon.
4. Update the attributes to the desired values.

If a user doesn't already have attributes set up, users who are added to the
group will inherit these attributes upon provisioning.

### Step one: Configure attribute mappings

1. Complete the [SCIM provisioning setup](#enable-scim-in-docker).
2. In the Azure Portal, open **Microsoft Entra ID** >
  **Enterprise Applications**, and select your SCIM application.
3. Go to **Provisioning** > **Mappings** >
  **Provision Azure Active Directory Users**.
4. Add or update the following mappings:
  - `userPrincipalName` -> `userName`
  - `mail` -> `emails.value`
  - Optional. Map `dockerRole`, `dockerOrg`, or `dockerTeam` using one of the
    [mapping methods](#step-two-choose-a-role-mapping-method).
5. Remove any unsupported attributes to prevent sync errors.
6. Optional. Go to **Mappings** > **Provision Azure Active Directory Groups**:
  - If group provisioning causes errors, set **Enabled** to **No**.
  - If enabling, test group mappings carefully.
7. Select **Save** to apply mappings.

### Step two: Choose a role mapping method

You can map `dockerRole`, `dockerOrg`, or `dockerTeam` using one of the
following methods:

#### Expression mapping

Use this method if you only need to assign Docker roles like `member`, `editor`,
or `owner`.

1. In the **Edit Attribute** view, set the mapping type to **Expression**.
2. In the **Expression** field:
  1. If your App Roles match Docker roles exactly, use:
    SingleAppRoleAssignment([appRoleAssignments])
  2. If they don't match, use a switch expression: `Switch(SingleAppRoleAssignment([appRoleAssignments]), "My Corp Admins", "owner", "My Corp Editors", "editor", "My Corp Users", "member")`
3. Set:
  - **Target attribute**: `urn:ietf:params:scim:schemas:extension:docker:2.0:User:dockerRole`
  - **Match objects using this attribute**: No
  - **Apply this mapping**: Always
4. Save your changes.

> Warning
>
> You can't use `dockerOrg` or `dockerTeam` with this method. Expression mapping
> is only compatible with one attribute.

#### Direct mapping

Use this method if you need to map multiple attributes (`dockerRole` +
`dockerTeam`).

1. For each Docker attribute, choose a unique Entra extension attribute
  (`extensionAttribute1`, `extensionAttribute2`, etc.).
2. In the **Edit Attribute** view:
  - Set mapping type to **Direct**.
  - Set **Source attribute** to your selected extension attribute.
  - Set **Target attribute** to one of:
    - `dockerRole: urn:ietf:params:scim:schemas:extension:docker:2.0:User:dockerRole`
    - `dockerOrg: urn:ietf:params:scim:schemas:extension:docker:2.0:User:dockerOrg`
    - `dockerTeam: urn:ietf:params:scim:schemas:extension:docker:2.0:User:dockerTeam`
  - Set **Apply this mapping** to **Always**.
3. Save your changes.

To assign values, you'll need to use the Microsoft Graph API.

### Step three: Assign users and groups

For either mapping method:

1. In the SCIM app, go to **Users and Groups** > **Add user/group**.
2. Select the users or groups to provision to Docker.
3. Select **Assign**.

If you're using expression mapping:

1. Go to **App registrations** > your SCIM app > **App Roles**.
2. Create App Roles that match Docker roles.
3. Assign users or groups to App Roles under **Users and Groups**.

If you're using direct mapping:

1. Go to [Microsoft Graph Explorer](https://developer.microsoft.com/en-us/graph/graph-explorer)
  and sign in as a tenant admin.
2. Use Microsoft Graph API to assign attribute values. Example PATCH request:

```bash
PATCH https://graph.microsoft.com/v1.0/users/{user-id}
Content-Type: application/json

{
  "extensionAttribute1": "owner",
  "extensionAttribute2": "moby",
  "extensionAttribute3": "developers"
}
```

> Note
>
> You must use a different extension attribute for each SCIM field.

See the documentation for your IdP for additional details:

- [Okta](https://help.okta.com/en-us/Content/Topics/users-groups-profiles/usgp-add-custom-user-attributes.htm)
- [Entra ID/Azure AD](https://learn.microsoft.com/en-us/azure/active-directory/app-provisioning/customize-application-attributes#provisioning-a-custom-extension-attribute-to-a-scim-compliant-application)

## Test SCIM provisioning

After completing role mapping, you can test the configuration manually.

1. In the Okta admin portal, go to **Directory > People**.
2. Select a user you've assigned to your SCIM application.
3. Select **Provision User**.
4. Wait a few seconds, then check the Docker
  [Admin Console](https://app.docker.com/admin) under **Members**.
5. If the user doesn't appear, review logs in **Reports > System Log** and
  confirm SCIM settings in the app.

1. In the Azure Portal, go to **Microsoft Entra ID** > **Enterprise Applications**,
  and select your SCIM app.
2. Go to **Provisioning** > **Provision on demand**.
3. Select a user or group and choose **Provision**.
4. Confirm that the user appears in the Docker
  [Admin Console](https://app.docker.com/admin) under **Members**.
5. If needed, check **Provisioning logs** for errors.

## Migrate existing JIT users to SCIM

If you already have users provisioned through Just-in-Time (JIT) and want to
enable full SCIM lifecycle management, you need to migrate them. Users
originally created by JIT cannot be automatically de-provisioned through SCIM,
even after SCIM is enabled.

### Why migrate

Organizations using JIT provisioning may encounter limitations with user
lifecycle management, particularly around de-provisioning. Migrating to SCIM
provides:

- Automatic user de-provisioning when users leave your organization. This is
  the primary benefit for large organizations that need full automation.
- Continuous synchronization of user attributes
- Centralized user management through your identity provider
- Enhanced security through automated access control

> Important
>
> Users originally created through JIT provisioning cannot be automatically
> de-provisioned by SCIM, even after SCIM is enabled. To enable full lifecycle
> management including automatic de-provisioning through your identity provider,
> you must manually remove these users so SCIM can re-create them with proper
> lifecycle management capabilities.

This migration is most critical for larger organizations that require fully
automated user de-provisioning when employees leave the company.

### Prerequisites for migration

Before migrating, ensure you have:

- SCIM configured and tested in your organization
- A maintenance window for the migration

> Warning
>
> This migration temporarily disrupts user access. Plan to perform this
> migration during a low-usage window and communicate the timeline to affected
> users.

### Prepare for migration

#### Transfer ownership

Before removing users, ensure that any repositories, teams, or organization
resources they own are transferred to another administrator or service account.
When a user is removed from the organization, any resources they own may
become inaccessible.

1. Review repositories, organization resources, and team ownership for affected
  users.
2. Transfer ownership to another administrator.

> Warning
>
> If ownership is not transferred, repositories owned by removed users may
> become inaccessible when the user is removed. Ensure all critical resources
> are transferred before proceeding.

#### Verify identity provider configuration

1. Confirm all JIT-provisioned users are assigned to the Docker application in
  your identity provider.
2. Verify identity provider group to Docker team mappings are configured and
  tested.

Users not assigned to the Docker application in your identity provider are not
re-created by SCIM after removal.

#### Export user records

Export a list of JIT-provisioned users from Docker Admin Console:

1. Sign in to [Docker Home](https://app.docker.com) and select your
  organization.
2. Select **Admin Console**, then **Members**.
3. Select **Export members** to download the member list as CSV for backup and
  reference.

Keep this CSV list of JIT-provisioned users as a rollback reference if needed.

### Complete the migration

#### Disable JIT provisioning

> Important
>
> Before disabling JIT, ensure SCIM is fully configured and tested in your
> organization. Do not disable JIT until you have verified SCIM is working
> correctly.

1. Sign in to [Docker Home](https://app.docker.com) and select your organization.
2. Select **Admin Console**, then **SSO and SCIM**.
3. In the SSO connections table, select the **Actions** menu for your connection.
4. Select **Disable JIT provisioning**.
5. Select **Disable** to confirm.

Disabling JIT prevents new users from being automatically added through SSO
during the migration.

#### Remove JIT-origin users

> Important
>
> Users originally created through JIT provisioning cannot be automatically
> de-provisioned by SCIM, even after SCIM is enabled. To enable full lifecycle
> management including automatic de-provisioning through your identity provider,
> you must manually remove these users so SCIM can re-create them with proper
> lifecycle management capabilities.

This step is most critical for large organizations that require fully automated
user de-provisioning when employees leave the company.

1. Sign in to [Docker Home](https://app.docker.com) and select your organization.
2. Select **Admin Console**, then **Members**.
3. Identify and remove JIT-provisioned users in manageable batches.
4. Monitor for any errors during removal.

> Tip
>
> To efficiently identify JIT users, compare the member list exported before
> SCIM was enabled with the current member list. Users who existed before SCIM
> was enabled were likely provisioned via JIT.

#### Verify SCIM re-provisioning

After removing JIT users, SCIM automatically re-creates user accounts:

1. In your identity provider system log, confirm "create app user" events for
  Docker.
2. In Docker Admin Console, confirm users reappear with SCIM provisioning.
3. Verify users are added to the correct teams via group mapping.

#### Validate user access

Perform post-migration validation:

1. Select a subset of migrated users to test sign-in and access.
2. Verify team membership matches identity provider group assignments.
3. Confirm repository access is restored.
4. Test that de-provisioning works correctly by removing a test user from your
  identity provider.

Keep audit exports and logs for compliance purposes.

### Migration results

After completing the migration:

- All users in your organization are SCIM-provisioned
- User de-provisioning works reliably through your identity provider
- No new JIT users are created
- Consistent identity lifecycle management is maintained

### Troubleshoot migration issues

If a user fails to reappear after removal:

1. Check that the user is assigned to the Docker application in your identity
  provider.
2. Verify SCIM is enabled in both Docker and your identity provider.
3. Trigger a manual SCIM sync in your identity provider.
4. Check provisioning logs in your identity provider for errors.

For more troubleshooting guidance, see
[Troubleshoot provisioning](https://docs.docker.com/enterprise/troubleshoot/troubleshoot-provisioning/).

## Disable SCIM

If SCIM is disabled, any user provisioned through SCIM will remain in the
organization. Future changes for your users will not sync from your IdP.
User de-provisioning is only possible when manually removing the user from the
organization.

To disable SCIM:

1. Sign in to [Docker Home](https://app.docker.com).
2. Select **Admin Console**, then **SSO and SCIM**.
3. In the **SSO connections** table, select the **Actions** icon.
4. Select **Disable SCIM**.

## Next steps

- Set up
  [Group mapping](https://docs.docker.com/enterprise/security/provisioning/group-mapping/).
- [Troubleshoot provisioning](https://docs.docker.com/enterprise/troubleshoot/troubleshoot-provisioning/).
