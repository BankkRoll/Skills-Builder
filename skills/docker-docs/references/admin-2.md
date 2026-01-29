# Insights and more

# Insights

> Gain insights about your organization's users and their Docker usage.

# Insights

   Table of contents

---

Subscription: Business For: Administrators

Insights helps administrators visualize and understand how Docker is used within
their organizations. With Insights, administrators can ensure their teams are
fully equipped to utilize Docker to its fullest potential, leading to improved
productivity and efficiency across the organization.

Key benefits include:

- Uniform working environment: Establish and maintain standardized
  configurations across teams.
- Best practices: Promote and enforce usage guidelines to ensure optimal
  performance.
- Increased visibility: Monitor and drive adoption of organizational
  configurations and policies.
- Optimized license use: Ensure that developers have access to advanced
  features provided by a Docker subscription.

## Prerequisites

To use Insights, you must meet the following requirements:

- [Docker Business subscription](https://www.docker.com/pricing/)
- Administrators must
  [enforce sign-in](https://docs.docker.com/security/for-admins/enforce-sign-in/)
  for users
- Your Account Executive must turn on Insights for your organization

## View Insights for organization users

To access Insights, contact your Account Executive to have the
feature turned on. Once the feature is turned on, access Insights using the
following steps:

1. Sign in to [Docker Home](https://app.docker.com/) and choose
  your organization.
2. Select **Insights**. then select the period of time for the data.

> Note
>
> Insights data is not real-time and is updated daily. At the top-right of the
> Insights page, view the **Last updated** date to understand when the data was
> last updated.

Insights data is displayed in the following charts:

- [Docker Desktop users](#docker-desktop-users)
- [Builds](#builds)
- [Containers](#containers)
- [Docker Desktop usage](#docker-desktop-usage)
- [Docker Hub images](#docker-hub-images)
- [Extensions](#extensions)

### Docker Desktop users

Track active Docker Desktop users in your domain, differentiated by license
status. This chart helps you understand the engagement levels within your
organization, providing insights into how many users are actively using Docker
Desktop. Note that users who opt out of analytics aren't included in the active
counts.

The chart contains the following data:

| Data | Description |
| --- | --- |
| Active user | The number of users who have actively used Docker Desktop and either signed in with a Docker account that has a license in your organization or signed in to a Docker account with an email address from a domain associated with your organization.Users who don’t sign in to an account associated with your organization are not represented in the data. To ensure users sign in with an account associated with your organization, you canenforce sign-in. |
| Total organization members | The number of users who have used Docker Desktop, regardless of their Insights activity. |
| Users opted out of analytics | The number of users who are members of your organization that have opted out of sending analytics.When users opt out of sending analytics, you won't see any of their data in Insights. To ensure that the data includes all users, you can useSettings Managementto setanalyticsEnabledfor all your users. |
| Active users (graph) | The view over time for total active users. |

### Builds

Monitor development efficiency and the time your team invests in builds with
this chart. It provides a clear view of the build activity, helping you identify
patterns, optimize build times, and enhance overall development productivity.

The chart contains the following data:

| Data | Description |
| --- | --- |
| Average build per user | The average number of builds per active user. A build includes any time a user runs one of the following commands:docker builddocker buildx bdocker buildx bakedocker buildx builddocker buildx fdocker builder bdocker builder bakedocker builder builddocker builder fdocker compose builddocker compose up --builddocker image build |
| Average build time | The average build time per build. |
| Build success rate | The percentage of builds that were successful out of the total number of builds. A successful build includes any build that exits normally. |
| Total builds (graph) | The total number of builds separated into successful builds and failed builds. A successful build includes any build that exits normally. A failed build includes any build that exits abnormally. |

### Containers

View the total and average number of containers run by users with this chart. It
lets you gauge container usage across your organization, helping you understand
usage trends and manage resources effectively.

The chart contains the following data:

| Data | Description |
| --- | --- |
| Total containers run | The total number of containers run by active users. Containers run include those run using the Docker Desktop graphical user interface,docker run, ordocker compose. |
| Average number of containers run | The average number of containers run per active user. |
| Containers run by active users (graph) | The number of containers run over time by active users. |

### Docker Desktop usage

Explore Docker Desktop usage patterns with this chart to optimize your team's
workflows and ensure compatibility. It provides valuable insights into how
Docker Desktop is being utilized, enabling you to streamline processes and
improve efficiency.

The chart contains the following data:

| Data | Description |
| --- | --- |
| Most used version | The most used version of Docker Desktop by users in your organization. |
| Most used OS | The most used operating system by users. |
| Versions by active users (graph) | The number of active users using each version of Docker Desktop.To learn more about each version and release dates, see theDocker Desktop release notes. |
| Interface by active users (graph) | The number of active users grouped into the type of interface they used to interact with Docker Desktop.A CLI user is any active user who has run adockercommand. A GUI user is any active user who has interacted with the Docker Desktop graphical user interface. |

### Docker Hub images

Analyze image distribution activity with this chart and view the most utilized
Docker Hub images within your domain. This information helps you manage image
usage, ensuring that the most critical resources are readily available and
efficiently used.

> Note
>
> Data for images is only for Docker Hub. Data for third-party
> registries and mirrors aren't included.

The chart contains the following data:

| Data | Description |
| --- | --- |
| Total pulled images | The total number of images pulled by users from Docker Hub. |
| Total pushed images | The total number of images pushed by users to Docker Hub. |
| Top 10 pulled images | A list of the top 10 images pulled by users from Docker Hub and the number of times each image has been pulled. |

### Extensions

Monitor extension installation activity with this chart. It provides visibility
into the Docker Desktop extensions your teams are using, letting you track
adoption and identify popular tools that enhance productivity.

The chart contains the following data:

| Data | Description |
| --- | --- |
| Percentage of org with extensions installed | The percentage of users in your organization with at least one Docker Desktop extension installed. |
| Top 5 extensions installed in the organization | A list of the top 5 Docker Desktop extensions installed by users in your organization and the number of users who have installed each extension. |

## Export Docker Desktop user data

You can export Docker Desktop user data as a CSV file:

1. Open [Docker Home](https://app.docker.com) and select your organization from the top-left account drop-down.
2. Select **Admin Console** in the left-hand navigation menu.
3. Select **Desktop insights**.
4. Choose a timeframe for your insights data: **1 Week**, **1 Month**, or
  **3 Months**.
5. Select **Export** and choose **Docker Desktop users** from the drop-down.

Your export will automatically download. Open the file to view
the export data.

### Understanding export data

A Docker Desktop user export file contains the following data points:

- Name: User's name
- Username: User's Docker ID
- Email: User's email address associated with their Docker ID
- Type: User type
- Role: User
  [role](https://docs.docker.com/enterprise/security/roles-and-permissions/)
- Teams: Team(s) within your organization the user is a
  member of
- Date Joined: The date the user joined your organization
- Last Logged-In Date: The last date the user logged into Docker using
  their web browser (this includes Docker Hub and Docker Home)
- Docker Desktop Version: The version of Docker Desktop the user has
  installed
- Last Seen Date: The last date the user used the Docker Desktop application
- Opted Out Analytics: Whether the user has opted out of the
  [Send usage statistics](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/settings-reference/#send-usage-statistics) setting in Docker Desktop

## Troubleshoot Insights

If you’re experiencing issues with data in Insights, consider the following
solutions to resolve common problems:

- Update users to the latest version of Docker Desktop.
  Data is not shown for users using versions 4.16 or lower of Docker Desktop.
  In addition, older versions may not provide all data. Ensure all users have
  installed the latest version of Docker Desktop.
- Turn on **Send usage statistics** in Docker Desktop for all your users.
  If users have opted out of sending usage statistics for Docker Desktop, then
  their usage data will not be a part of Insights. To manage the setting at
  scale for all your users, you can use
  [Settings
  Management](https://docs.docker.com/desktop/hardened-desktop/settings-management/) and turn on the
  `analyticsEnabled` setting.
- Ensure users use Docker Desktop and aren't using the standalone
  version of Docker Engine.
  Only Docker Desktop can provide data for Insights. If a user installs Docker
  Engine outside of Docker Desktop, Docker Engine won't provide
  data for that user.
- Make sure users sign in to an account associated with your
  organization.
  Users who don’t sign in to an account associated with your organization are
  not represented in the data. To ensure users sign in with an account
  associated with your organization, you can
  [enforce
  sign-in](https://docs.docker.com/security/for-admins/enforce-sign-in/).

---

# Create and manage a team

> Learn how to create and manage teams for your organization

# Create and manage a team

   Table of contents

---

Subscription: Team  Business For: Administrators

You can create teams for your organization in the Admin Console or Docker Hub,
and configure team repository access in Docker Hub.

A team is a group of Docker users that belong to an organization. An
organization can have multiple teams. An organization owner can create new
teams and add members to an existing team using their Docker ID or email
address. Members aren't required to be part of a team to be associated with an
organization.

The organization owner can add additional organization owners to help them
manage users, teams, and repositories in the organization by assigning them
the owner role.

## What is an organization owner?

An organization owner is an administrator who has the following permissions:

- Manage repositories and add team members to the organization
- Access private repositories, all teams, billing information, and
  organization settings
- Specify [permissions](#permissions-reference) for each team in the
  organization
- Enable
  [SSO](https://docs.docker.com/enterprise/security/single-sign-on/) for the
  organization

When SSO is enabled for your organization, the organization owner can
also manage users. Docker can auto-provision Docker IDs for new end-users or
users who'd like to have a separate Docker ID for company use through SSO
enforcement.

Organization owners can add others with the owner role to help them
manage users, teams, and repositories in the organization.

For more information on roles, see
[Roles and permissions](https://docs.docker.com/enterprise/security/roles-and-permissions/).

## Create a team

1. Sign in to [Docker Home](https://app.docker.com) and select your
  organization.
2. Select **Teams**.

## Set team repository permissions

You must create a team before you are able to configure repository permissions.
For more details, see
[Create and manage a
team](https://docs.docker.com/admin/organization/manage-a-team/).

To set team repository permissions:

1. Sign in to [Docker Hub](https://hub.docker.com).
2. Select **My Hub** > **Repositories**.
  A list of your repositories appears.
3. Select a repository.
  The **General** page for the repository appears.
4. Select the **Permissions** tab.
5. Add, modify, or remove a team's repository permissions.
  - Add: Specify the **Team**, select the **Permission**, and then select **Add**.
  - Modify: Specify the new permission next to the team.
  - Remove: Select the **Remove permission** icon next to the team.

### Permissions reference

- `Read-only` access lets users view, search, and pull a private repository
  in the same way as they can a public repository.
- `Read & Write` access lets users pull, push, and view a repository. In
  addition, it lets users view, cancel, retry or trigger builds.
- `Admin` access lets users pull, push, view, edit, and delete a
  repository. You can also edit build settings and update the repository’s
  description, collaborator permissions, public/private visibility, and delete.

Permissions are cumulative. For example, if you have "Read & Write" permissions,
you automatically have "Read-only" permissions.

The following table shows what each permission level allows users to do:

| Action | Read-only | Read & Write | Admin |
| --- | --- | --- | --- |
| Pull a Repository | ✅ | ✅ | ✅ |
| View a Repository | ✅ | ✅ | ✅ |
| Push a Repository | ❌ | ✅ | ✅ |
| Edit a Repository | ❌ | ❌ | ✅ |
| Delete a Repository | ❌ | ❌ | ✅ |
| Update a Repository Description | ❌ | ❌ | ✅ |
| View Builds | ✅ | ✅ | ✅ |
| Cancel Builds | ❌ | ✅ | ✅ |
| Retry Builds | ❌ | ✅ | ✅ |
| Trigger Builds | ❌ | ✅ | ✅ |
| Edit Build Settings | ❌ | ❌ | ✅ |

> Note
>
> A user who hasn't verified their email address only has `Read-only` access to
> the repository, regardless of the rights their team membership has given them.

## Delete a team

Organization owners can delete a team. When you remove a team from your
organization, this action revokes member access to the team's permitted
resources. It won't remove users from other teams that they belong to, and it
won't delete any resources.

1. Sign in to [Docker Home](https://app.docker.com/) and select your
  organization.
2. Select **Teams**.
3. Select the **Actions** icon next to the name of the team you want to delete.
4. Select **Delete team**.
5. Review the confirmation message, then select **Delete**.

## More resources

- [Video: Docker teams](https://youtu.be/WKlT1O-4Du8?feature=shared&t=348)
- [Video: Roles, teams, and repositories](https://youtu.be/WKlT1O-4Du8?feature=shared&t=435)

---

# Manage Docker products

> Learn how to manage access and usage for Docker products for your organization

# Manage Docker products

   Table of contents

---

Subscription: Team  Business For: Administrators

In this section, learn how to manage access and view usage of the Docker
products for your organization. For more detailed information about each
product, including how to set up and configure them, see the following manuals:

- [Docker Desktop](https://docs.docker.com/desktop/)
- [Docker Hub](https://docs.docker.com/docker-hub/)
- [Docker Build Cloud](https://docs.docker.com/build-cloud/)
- [Docker Scout](https://docs.docker.com/scout/)
- [Testcontainers Cloud](https://testcontainers.com/cloud/docs/#getting-started)
- [Docker Offload](https://docs.docker.com/offload/)

## Manage product access for your organization

Access to the Docker products included in your subscription is turned on by
default for all users. For an overview of products included in your
subscription, see
[Docker subscriptions and features](https://www.docker.com/pricing/).

### Manage Docker Desktop access

To manage Docker Desktop access:

1. [Enforce sign-in](https://docs.docker.com/enterprise/security/enforce-sign-in/).
2. Manage members [manually](https://docs.docker.com/admin/organization/members/) or use
  [provisioning](https://docs.docker.com/enterprise/security/provisioning/).

With sign-in enforced, only users who are a member of your organization can
use Docker Desktop after signing in.

### Manage Docker Hub access

To manage Docker Hub access, sign in to
[Docker Home](https://app.docker.com/) and configure
[Registry Access Management](https://docs.docker.com/enterprise/security/hardened-desktop/registry-access-management/)
or
[Image Access Management](https://docs.docker.com/enterprise/security/hardened-desktop/image-access-management/).

### Manage Docker Build Cloud access

To initially set up and configure Docker Build Cloud, sign in to
[Docker Build Cloud](https://app.docker.com/build) and follow the
on-screen instructions.

To manage Docker Build Cloud access:

1. Sign in to [Docker Build Cloud](http://app.docker.com/build) as an
  organization owner.
2. Select **Account settings**.
3. Select **Lock access to Docker Build Account**.

### Manage Docker Scout access

To initially set up and configure Docker Scout, sign in to
[Docker Scout](https://scout.docker.com/) and follow the on-screen instructions.

To manage Docker Scout access:

1. Sign in to [Docker Scout](https://scout.docker.com/) as an organization
  owner.
2. Select your organization, then **Settings**.
3. To manage what repositories are enabled for Docker Scout analysis, select
  **Repository settings**. For more information on,
  see [repository settings](https://docs.docker.com/scout/explore/dashboard/#repository-settings).
4. To manage access to Docker Scout for use on local images with Docker Desktop,
  use
  [Settings Management](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/)
  and set `sbomIndexing` to `false` to disable, or to `true` to enable.

### Manage Testcontainers Cloud access

To initially set up and configure Testcontainers Cloud, sign in to
[Testcontainers Cloud](https://app.testcontainers.cloud/) and follow the
on-screen instructions.

To manage access to Testcontainers Cloud:

1. Sign in to the [Testcontainers Cloud](https://app.testcontainers.cloud/) and
  select **Account**.
2. Select **Settings**, then **Lock access to Testcontainers Cloud**.

### Manage Docker Offload access

> Note
>
> Docker Offload isn't included in the core Docker subscription plans. To make Docker Offload available, you must [sign
> up](https://www.docker.com/products/docker-offload/) and subscribe.

To manage Docker Offload access for your organization, use
[Settings
Management](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/):

1. Sign in to [Docker Home](https://app.docker.com/) as an organization owner.
2. Select **Admin Console** > **Desktop Settings Management**.
3. Configure the **Enable Docker Offload** setting to control whether Docker Offload features are available in Docker
  Desktop. You can configure this setting in five states:
  - **Always enabled**: Docker Offload is always enabled and users cannot disable it. The Offload
    toggle is always visible in Docker Desktop header. Recommended for VDI environments where local Docker execution is
    not possible.
  - **Enabled**: Docker Offload is enabled by default but users can disable it in Docker Desktop
    settings. Suitable for hybrid environments.
  - **Disabled**: Docker Offload is disabled by default but users can enable it in Docker Desktop
    settings.
  - **Always disabled**: Docker Offload is disabled and users cannot enable it. The option is
    visible but locked. Use when Docker Offload is not approved for organizational use.
  - **User defined**: No enforced default. Users choose whether to enable or disable Docker Offload in their
    Docker Desktop settings.
4. Select **Save**.

For more details on Settings Management, see the
[Settings
reference](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/settings-reference/#enable-docker-offload).

## Monitor product usage for your organization

To view usage for Docker products:

- Docker Desktop: View the **Insights** page in [Docker Home](https://app.docker.com/). For more details, see [Insights](https://docs.docker.com/admin/organization/insights/).
- Docker Hub: View the [Usagepage](https://hub.docker.com/usage) in Docker Hub.
- Docker Build Cloud: View the **Build minutes** page in [Docker Build Cloud](http://app.docker.com/build).
- Docker Scout: View the [Repository settingspage](https://scout.docker.com/settings/repos) in Docker Scout.
- Testcontainers Cloud: View the [Billingpage](https://app.testcontainers.cloud/dashboard/billing) in Testcontainers Cloud.
- Docker Offload: View the **Offload** > **Offload overview** page in [Docker Home](https://app.docker.com/). For more details, see
  [Docker Offload usage and billing](https://docs.docker.com/offload/usage/).

If your usage or seat count exceeds your subscription amount, you can
[scale your subscription](https://docs.docker.com/subscription/scale/) to meet your needs.

---

# Manage organization members

> Learn how to manage organization members in Docker Hub and Docker Admin Console.

# Manage organization members

   Table of contents

---

Learn how to manage members for your organization in Docker Hub and the Docker Admin Console.

## Invite members

Owners can invite new members to an organization via Docker ID, email address, or with a CSV file containing email addresses. If an invitee does not have a Docker account, they must create an account and verify their email address before they can accept an invitation to join the organization. When inviting members, their pending invitation occupies a seat.

### Invite members via Docker ID or email address

Use the following steps to invite members to your organization via Docker ID or email address.

1. Sign in to [Docker Home](https://app.docker.com) and select your organization from the top-left account drop-down.
2. Select **Members**, then **Invite**.
3. Select **Emails or usernames**.
4. Follow the on-screen instructions to invite members. Invite a maximum of 1000 members and separate multiple entries by comma, semicolon, or space.

> Note
>
> When you invite members, you assign them a role. See
> [Roles and permissions](https://docs.docker.com/enterprise/security/roles-and-permissions/) for
> details about the access permissions for each role.

Pending invitations appear in the table. Invitees receive an email with a link to Docker Hub where they can accept or decline the invitation.

### Invite members via CSV file

To invite multiple members to an organization via a CSV file containing email addresses:

1. Sign in to [Docker Home](https://app.docker.com) and select your organization from the top-left account drop-down.
2. Select **Members**, then **Invite**.
3. Select **CSV upload**.
4. Optional. Select **Download the template CSV file** to download an example CSV file. The following is an example of the contents of a valid CSV file.

```text
email
docker.user-0@example.com
docker.user-1@example.com
```

CSV file requirements:

- The file must contain a header row with at least one heading named email. Additional columns are allowed and are ignored in the import.
- The file must contain a maximum of 1000 email addresses (rows). To invite more than 1000 users, create multiple CSV files and perform all steps in this task for each file.

1. Create a new CSV file or export a CSV file from another application.

- To export a CSV file from another application, see the application’s documentation.
- To create a new CSV file, open a new file in a text editor, type email on the first line, type the user email addresses one per line on the following lines, and then save the file with a .csv extension.

1. Select **Browse files** and then select your CSV file, or drag and drop the CSV file into the **Select a CSV file to upload** box. You can only select one CSV file at a time.

> Note
>
> If the amount of email addresses in your CSV file exceeds the number of available seats in your organization, you cannot continue to invite members. To invite members, you can purchase more seats, or remove some email addresses from the CSV file and re-select the new file. To purchase more seats, see
> [Add seats](https://docs.docker.com/subscription/manage-seats/) to your subscription or [Contact sales](https://www.docker.com/pricing/contact-sales/).

1. After the CSV file has been uploaded, select **Review**.

Valid email addresses and any email addresses that have issues appear. Email addresses may have the following issues:

- Invalid email: The email address is not a valid address. The email address will be ignored if you send invites. You can correct the email address in the CSV file and re-import the file.
- Already invited: The user has already been sent an invite email and another invite email will not be sent.
- Member: The user is already a member of your organization and an invite email will not be sent.
- Duplicate: The CSV file has multiple occurrences of the same email address. The user will be sent only one invite email.

1. Follow the on-screen instructions to invite members.

> Note
>
> When you invite members, you assign them a role. See
> [Roles and permissions](https://docs.docker.com/enterprise/security/roles-and-permissions/) for
> details about the access permissions for each role.

Pending invitations appear in the table. The invitees receive an email with a link to Docker Hub where they can accept or decline the invitation.

### Invite members via API

You can bulk invite members using the Docker Hub API. For more information, see the [Bulk create invites](https://docs.docker.com/reference/api/hub/latest/#tag/invites/paths/~1v2~1invites~1bulk/post) API endpoint.

## Accept invitation

When an invitation is to a user's email address, they receive
a link to Docker Hub where they can accept or decline the invitation.
To accept an invitation:

1. Check your email inbox and open the Docker email with an invitation to
  join the Docker organization.
2. To open the link to Docker Hub, select the **click here** link.
  > Warning
  >
  > Invitation email links expire after 14 days. If your email link has expired,
  > you can sign in to [Docker Hub](https://hub.docker.com/) with the email
  > address the link was sent to and accept the invitation from the
  > **Notifications** panel.
3. The Docker create an account page will open. If you already have an account, select **Already have an account? Sign in**.
  If you do not have an account yet, create an account using the same email
  address you received the invitation through.
4. Optional. If you do not have an account and created one, you must navigate
  back to your email inbox and verify your email address using the Docker verification
  email.
5. Once you are signed in to Docker Hub, select **My Hub** from the top-level navigation menu.
6. Select **Accept** on your invitation.

After accepting an invitation, you are now a member of the organization.

## Manage invitations

After inviting members, you can resend or remove invitations as needed.

### Resend an invitation

You can send individual invitations, or bulk invitations from the Admin Console.

To resend an individual invitation:

1. Sign in to [Docker Home](https://app.docker.com/) and select your
  organization.
2. Select **Members**.
3. Select the **action menu** next to the invitee and select **Resend**.
4. Select **Invite** to confirm.

To bulk resend invitations:

1. Sign in to [Docker Home](https://app.docker.com/) and select your
  organization.
2. Select **Members**.
3. Use the **checkboxes** next to **Usernames** to bulk select users.
4. Select **Resend invites**.
5. Select **Resend** to confirm.

### Remove an invitation

To remove an invitation from the Admin Console:

1. Sign in to [Docker Home](https://app.docker.com/) and select your
  organization.
2. Select **Members**.
3. Select the **action menu** next to the invitee and select **Remove invitee**.
4. Select **Remove** to confirm.

## Manage members on a team

Use Docker Hub or the Admin Console to add or remove team members. Organization owners can add a member to one or more teams within an organization.

### Add a member to a team

To add a member to a team with the Admin Console:

1. Sign in to [Docker Home](https://app.docker.com/) and select your
  organization.
2. Select **Teams**.
3. Select the team name.
4. Select **Add member**. You can add the member by searching for their email address or username.
  > Note
  >
  > An invitee must first accept the invitation to join the organization before being added to the team.

### Remove members from teams

> Note
>
> If your organization uses single sign-on (SSO) with
> [SCIM](https://docs.docker.com/enterprise/security/provisioning/scim/) enabled, you should remove members from your identity provider (IdP). This will automatically remove members from Docker. If SCIM is disabled, you must manually manage members in Docker.

Organization owners can remove a member from a team in Docker Hub or Admin Console. Removing the member from the team will revoke their access to the permitted resources.

To remove a member from a specific team with the Admin Console:

1. Sign in to [Docker Home](https://app.docker.com/) and select your
  organization.
2. Select **Teams**.
3. Select the team name.
4. Select the **X** next to the user's name to remove them from the team.
5. When prompted, select **Remove** to confirm.

### Update a member role

Organization owners can manage
[roles](https://docs.docker.com/security/for-admins/roles-and-permissions/)
within an organization. If an organization is part of a company,
the company owner can also manage that organization's roles. If you have SSO enabled, you can use
[SCIM for role mapping](https://docs.docker.com/security/for-admins/provisioning/scim/).

> Note
>
> If you're the only owner of an organization, you need to assign a new owner
> before you can edit your role.

To update a member role in the Admin Console:

1. Sign in to [Docker Home](https://app.docker.com/) and select your
  organization.
2. Select **Members**.
3. Find the username of the member whose role you want to edit. Select the
  **Actions** menu, then **Edit role**.

## Export members CSV file

Subscription: Team  Business For: Administrators

Owners can export a CSV file containing all members. The CSV file for a company contains the following fields:

- Name: The user's name
- Username: The user's Docker ID
- Email: The user's email address
- Member of Organizations: All organizations the user is a member of within a company
- Invited to Organizations: All organizations the user is an invitee of within a company
- Account Created: The time and date when the user account was created

To export a CSV file of your members:

1. Sign in to [Docker Home](https://app.docker.com/) and select your
  organization.
2. Select **Members**.
3. Select the **download** icon to export a CSV file of all members.

---

# Onboard your organization

> Get started onboarding your Docker Team or Business organization.

# Onboard your organization

   Table of contents

---

Subscription: Team  Business For: Administrators

Learn how to onboard your organization using the Admin Console or Docker Hub.

Onboarding your organization includes:

- Identifying users to help you allocate your subscription seats
- Invite members and owners to your organization
- Secure authentication and authorization for your organization
- Enforce sign-in for Docker Desktop to ensure security best practices

These actions help administrators gain visibility into user activity and
enforce security settings. Organization members also receive increased pull
limits and other benefits when they are signed in.

## Prerequisites

Before you start onboarding your organization, ensure you:

- Have a Docker Team or Business subscription. For more details, see
  [Docker subscriptions and features](https://www.docker.com/pricing/).
  > Note
  >
  > When purchasing a self-serve subscription, the on-screen instructions
  > guide you through creating an organization. If you have purchased a
  > subscription through Docker Sales and you have not yet created an
  > organization, see
  > [Create an organization](https://docs.docker.com/admin/organization/orgs/).
- Familiarize yourself with Docker concepts and terminology in
  the [administration overview](https://docs.docker.com/admin/).

## Onboard with guided setup

The Admin Console has a guided setup to help you
onboard your organization. The guided setup's steps consist of basic onboarding
tasks. If you want to onboard outside of the guided setup,
see
[Recommended onboarding steps](https://docs.docker.com/admin/organization/onboard/#recommended-onboarding-steps).

To onboard using the guided setup,
navigate to the [Admin Console](https://app.docker.com) and
select **Guided setup** in the left-hand navigation.

The guided setup walks you through the following onboarding steps:

- **Invite your team**: Invite owners and members.
- **Manage user access**: Add and verify a domain, manage users with SSO, and
  enforce Docker Desktop sign-in.
- **Docker Desktop security**: Configure image access management, registry
  access management, and settings management.

## Recommended onboarding steps

### Step one: Identify your Docker users

Identifying your users helps you allocate seats efficiently and ensures they
receive your Docker subscription benefits.

1. Identify the Docker users in your organization.
  - If your organization uses device management software, like MDM or Jamf,
    you can use the device management software to help identify Docker users.
    See your device management software's documentation for details. You can
    identify Docker users by checking if Docker Desktop is installed at the
    following location on each user's machine:
    - Mac: `/Applications/Docker.app`
    - Windows: `C:\Program Files\Docker\Docker`
    - Linux: `/opt/docker-desktop`
  - If your organization doesn't use device management software or your
    users haven't installed Docker Desktop yet, you can survey your users to
    identify who is using Docker Desktop.
2. Ask users to update their Docker account's email address to one associated
  with your organization's domain, or create a new account with that email.
  - To update an account's email address, instruct your users to sign in
    to [Docker Hub](https://hub.docker.com), and update the email address to
    their email address in your organization's domain.
  - To create a new account, instruct your users to
    [sign up](https://hub.docker.com/signup) using their email address associated
    with your organization's domain. Ensure your users verify their email address.
3. Identify Docker accounts associated with your organization's domain:
  - Ask your Docker sales representative or
    [contact sales](https://www.docker.com/pricing/contact-sales/) to get a list
    of Docker accounts that use an email address in your organization's domain.

### Step two: Invite owners

Owners can help you onboard and manage your organization.

When you create an organization, you are the only owner. It is optional to
add additional owners.

To add an owner, invite a user and assign them the owner role. For more
details, see
[Invite members](https://docs.docker.com/admin/organization/members/) and
[Roles and permissions](https://docs.docker.com/enterprise/security/roles-and-permissions/).

### Step three: Invite members

When you add users to your organization, you gain visibility into their
activity and you can enforce security settings. Your members also
receive increased pull limits and other organization wide benefits when
they are signed in.

To add a member, invite a user and assign them the member role.
For more details, see
[Invite members](https://docs.docker.com/admin/organization/members/) and
[Roles and permissions](https://docs.docker.com/enterprise/security/roles-and-permissions/).

### Step four: Manage user access with SSO and SCIM

Configuring SSO and SCIM is optional and only available to Docker Business
subscribers. To upgrade a Docker Team subscription to a Docker Business
subscription, see
[Change your subscription](https://docs.docker.com/subscription/change/).

Use your identity provider (IdP) to manage members and provision them to Docker
automatically via SSO and SCIM. See the following for more details:

- [Configure SSO](https://docs.docker.com/enterprise/security/single-sign-on/configure/)
  to authenticate and add members when they sign in to Docker through your
  identity provider.
- Optional.
  [Enforce SSO](https://docs.docker.com/enterprise/security/single-sign-on/connect/) to
  ensure that when users sign in to Docker, they must use SSO.
  > Note
  >
  > Enforcing single sign-on (SSO) and enforcing Docker Desktop sign in
  > are different features. For more details, see
  > [Enforcing sign-in versus enforcing single sign-on (SSO)](https://docs.docker.com/enterprise/security/enforce-sign-in/#enforcing-sign-in-versus-enforcing-single-sign-on-sso).
- [Configure SCIM](https://docs.docker.com/enterprise/security/provisioning/scim/) to
  automatically provision, add, and de-provision members to Docker through
  your identity provider.

### Step five: Enforce sign-in for Docker Desktop

By default, members of your organization can use Docker Desktop without signing
in. When users don’t sign in as a member of your organization, they don’t
receive the
[benefits of your organization’s subscription](https://www.docker.com/pricing/)
and they can circumvent
[Docker’s security features](https://docs.docker.com/enterprise/security/hardened-desktop/).

There are multiple ways you can enforce sign-in, depending on your organization's
Docker configuration:

- [Registry key method (Windows only)](https://docs.docker.com/enterprise/security/enforce-sign-in/methods/#registry-key-method-windows-only)
- [.plistmethod (Mac only)](https://docs.docker.com/enterprise/security/enforce-sign-in/methods/#plist-method-mac-only)
- [registry.jsonmethod (All)](https://docs.docker.com/enterprise/security/enforce-sign-in/methods/#registryjson-method-all)

### Step six: Manage Docker Desktop security

Docker offers the following security features to manage your organization's
security posture:

- [Image Access Management](https://docs.docker.com/enterprise/security/hardened-desktop/image-access-management/): Control which types of images your developers can pull from Docker Hub.
- [Registry Access Management](https://docs.docker.com/enterprise/security/hardened-desktop/registry-access-management/): Define which registries your developers can access.
- [Settings management](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/): Set and control Docker Desktop settings for your users.

## What's next

- [Manage Docker products](https://docs.docker.com/admin/organization/manage-products/) to configure access and view usage.
- Configure
  [Hardened Docker Desktop](https://docs.docker.com/desktop/hardened-desktop/) to improve your organization’s security posture for containerized development.
- [Manage your domains](https://docs.docker.com/enterprise/security/domain-management/) to ensure that all Docker users in your domain are part of your organization.

Your Docker subscription provides many more additional features. To learn more,
see [Docker subscriptions and features](https://www.docker.com/pricing/).
