# Create a company and more

# Create a company

> Learn how to create a company to centrally manage multiple organizations.

# Create a company

   Table of contents

---

Subscription: Business For: Administrators

Learn how to create a new company in the Docker Admin Console, a centralized
dashboard for managing organizations.

## Prerequisites

Before you begin, you must:

- Be the owner of the organization you want to add to your company
- Have a Docker Business subscription

## Create a company

To create a new company:

1. Sign in to [Docker Home](https://app.docker.com/) and select your
  organization.
2. Select **Admin Console**, then **Company management**.
3. Select **Create a company**.
4. Enter a unique name for your company, then select **Continue**.
  > Tip
  >
  > The name for your company can't be the same as an existing user,
  > organization, or company namespace.
5. Review the migration details and then select **Create company**.

For more information on how you can add organizations to your company,
see [Add organizations to a company](https://docs.docker.com/admin/company/organizations/#add-organizations-to-a-company).

## Next steps

- [Manage organizations](https://docs.docker.com/admin/company/organizations/)
- [Manage company users](https://docs.docker.com/admin/company/users/)
- [Manage company owners](https://docs.docker.com/admin/company/owners/)

## More resources

- [Video: Create a company](https://youtu.be/XZ5_i6qiKho?feature=shared&t=359)

---

# Manage company organizations

> Learn how to manage organizations in a company.

# Manage company organizations

   Table of contents

---

Subscription: Business For: Administrators

Learn to manage the organizations in a company using the Docker Admin Console.

## View all organizations

1. Sign in to the [Docker Home](https://app.docker.com) and choose
  your company.
2. Select **Admin Console**, then **Organizations**.

The **Organizations** view displays all organizations under your company.

## Add seats to an organization

If you have a [self-serve](https://docs.docker.com/subscription/details/#self-serve)
subscription that has no pending subscription changes, you can add seats using
Docker Home. For more information about adding seats,
see
[Manage seats](https://docs.docker.com/subscription/manage-seats/#add-seats).

If you have a sales-assisted subscription, you must contact Docker support or
sales to add seats.

## Add organizations to a company

To add an organization to a company, ensure the following:

- You are a company owner.
- You are an organization owner of the organization you want to add.
- The organization has a Docker Business subscription.
- There’s no limit to how many organizations can exist under a company.

> Important
>
> Once you add an organization to a company, you can't remove it from the
> company.

1. Sign in to [Docker Home](https://app.docker.com) and select your company from
  the top-left account drop-down.
2. Select **Admin Console**, then **Organizations**.
3. Select **Add organization**.
4. Choose the organization you want to add from the drop-down menu.
5. Select **Add organization** to confirm.

## Manage an organization

1. Sign in to [Docker Home](https://app.docker.com) and select your company from
  the top-left account drop-down.
2. Select **Admin Console**, then **Organizations**.
3. Select the organization you want to manage.

For more details about managing an organization, see
[Organization administration](https://docs.docker.com/admin/organization/).

## More resources

- [Video: Managing a company and nested organizations](https://youtu.be/XZ5_i6qiKho?feature=shared&t=229)
- [Video: Adding nested organizations to a company](https://youtu.be/XZ5_i6qiKho?feature=shared&t=454)

---

# Manage company owners

> Learn how to add and remove company owners.

# Manage company owners

   Table of contents

---

Subscription: Business For: Administrators

A company can have multiple owners. Company owners have visibility across the
entire company and can manage settings that apply to all organizations under
that company. They also have the same access rights as organization owners but
don’t need to be members of any individual organization.

> Important
>
> Company owners do not occupy a seat unless they are added as a member of an
> organization under your company or SSO is enabled.

## Add a company owner

1. Sign in to [Docker Home](https://app.docker.com) and select your company from
  the top-left account drop-down.
2. Select **Admin Console**, then **Company owners**.
3. Select **Add owner**.
4. Specify the user's Docker ID to search for the user.
5. After you find the user, select **Add company owner**.

## Remove a company owner

1. Sign in to [Docker Home](https://app.docker.com) and select your company from
  the top-left account drop-down.
2. Select **Admin Console**, then **Company owners**.
3. Locate the company owner you want to remove and select the **Actions** menu.
4. Select **Remove as company owner**.

---

# Manage company members

> Learn how to manage company users in the Docker Admin Console.

# Manage company members

   Table of contents

---

Subscription: Business For: Administrators

Company owners can invite new members to an organization via Docker ID,
email address, or in bulk with a CSV file containing email
addresses.

If an invitee does not have a Docker account, they must create an account and
verify their email address before they can accept an invitation to join the
organization. Pending invitations occupy seats for the organization
the user is invited to.

## Invite members via Docker ID or email address

Use the following steps to invite members to your organization via Docker ID or
email address.

1. Sign in to [Docker Home](https://app.docker.com) and select
  your company.
2. On the **Organizations** page, select the organization you want
  to invite members to.
3. Select **Members**, then **Invite**.
4. Select **Emails or usernames**.
5. Follow the on-screen instructions to invite members.
  Invite a maximum of 1000 members and separate multiple entries by comma,
  semicolon, or space.
  > Note
  >
  > When you invite members, you assign them a role.
  > See
  > [Roles and permissions](https://docs.docker.com/security/for-admins/roles-and-permissions/)
  > for details about the access permissions for each role.
  Pending invitations appear on the Members page. The invitees receive an
  email with a link to Docker Hub where they can accept or decline the
  invitation.

## Invite members via CSV file

To invite multiple members to an organization via a CSV file containing email
addresses:

1. Sign in to [Docker Home](https://app.docker.com) and select
  your company.
2. On the **Organizations** page, select the organization you want
  to invite members to.
3. Select **Members**, then **Invite**.
4. Select **CSV upload**.
5. Select **Download the template CSV file** to optionally download an example
  CSV file. The following is an example of the contents of a valid CSV file.
  ```text
  email
  docker.user-0@example.com
  docker.user-1@example.com
  ```
  CSV file requirements:
  - The file must contain a header row with at least one heading named `email`.
    Additional columns are allowed and are ignored in the import.
  - The file must contain a maximum of 1000 email addresses (rows). To invite
    more than 1000 users, create multiple CSV files and perform all steps in
    this task for each file.
6. Create a new CSV file or export a CSV file from another application.
  - To export a CSV file from another application, see the application’s
    documentation.
  - To create a new CSV file, open a new file in a text editor, type `email`
    on the first line, type the user email addresses one per line on the
    following lines, and then save the file with a .csv extension.
7. Select **Browse files** and then select your CSV file, or drag and drop the
  CSV file into the **Select a CSV file to upload** box. You can only select
  one CSV file at a time.
  > Note
  >
  > If the amount of email addresses in your CSV file exceeds the number of
  > available seats in your organization, you cannot continue to invite members.
  > To invite members, you can purchase more seats, or remove some email
  > addresses from the CSV file and re-select the new file. To purchase more
  > seats, see
  > [Add seats to your subscription](https://docs.docker.com/subscription/add-seats/) or
  > [Contact sales](https://www.docker.com/pricing/contact-sales/).
8. After the CSV file has been uploaded, select **Review**.
  Valid email addresses and any email addresses that have issues will appear.
  Email addresses may have the following issues:
  - Invalid email: The email address is not a valid address. The email address
    will be ignored if you send invites. You can correct the email address in
    the CSV file and re-import the file.
  - Already invited: The user has already been sent an invite email and another
    invite email will not be sent.
  - Member: The user is already a member of your organization and an invite
    email will not be sent.
  - Duplicate: The CSV file has multiple occurrences of the same email address.
    The user will be sent only one invite email.
9. Follow the on-screen instructions to invite members.
  > Note
  >
  > When you invite members, you assign them a role.
  > See
  > [Roles and permissions](https://docs.docker.com/security/for-admins/roles-and-permissions/)
  > for details about the access permissions for each role.

Pending invitations appear on the Members page. The invitees receive an email
with a link to Docker Hub where they can accept or decline the invitation.

## Resend invitations to users

You can resend individual invitations, or bulk invitations from the Admin Console.

### Resend individual invitations

1. In [Docker Home](https://app.docker.com/), select your company from
  the top-left account drop-down.
2. Select **Admin Console**, then **Users**.
3. Select the **action menu** next to the invitee and select **Resend**.
4. Select **Invite** to confirm.

### Bulk resend invitation

1. In [Docker Home](https://app.docker.com/), select your company from
  the top-left account drop-down.
2. Select **Admin Console**, then **Users**.
3. Use the **checkboxes** next to **Usernames** to bulk select users.
4. Select **Resend invites**.
5. Select **Resend** to confirm.

## Invite members via API

You can bulk invite members using the Docker Hub API. For more information,
see the [Bulk create invites](https://docs.docker.com/reference/api/hub/latest/#tag/invites/paths/~1v2~1invites~1bulk/post) API endpoint.

## Manage members on a team

Use Docker Hub to add a member to a team or remove a member from a team. For
more details, see [Manage members](https://docs.docker.com/admin/organization/members/#manage-members-on-a-team).

---

# Company administration overview

> Learn how to manage multiple organizations using companies, including managing users, owners, and security.

# Company administration overview

   Table of contents

---

Subscription: Business For: Administrators

A company provides a single point of visibility across multiple organizations,
simplifying organization and settings management.

Organization owners with a Docker Business subscription can create a company
and manage it through the [Docker Admin Console](https://app.docker.com/admin).

The following diagram shows how a company relates to its associated
organizations.

![Diagram showing how companies relate to Docker organizations](https://docs.docker.com/admin/images/docker-admin-structure.webp)  ![Diagram showing how companies relate to Docker organizations](https://docs.docker.com/admin/images/docker-admin-structure.webp)

## Key features

With a company, administrators can:

- View and manage all nested organizations
- Configure company and organization settings centrally
- Control access to the company
- Have up to ten unique users assigned to the company owner role
- Configure SSO and SCIM for all nested organizations
- Enforce SSO for all users in the company

## Create and manage your company

Learn how to create and manage a company in the following sections.

[Create a companyGet started by learning how to create a company.](https://docs.docker.com/admin/company/new-company/)[Manage organizationsLearn how to add and manage organizations as well as seats within your company.](https://docs.docker.com/admin/company/organizations/)[Manage company ownersFind out more about company owners and how to manage them.](https://docs.docker.com/admin/company/owners/)[Manage usersExplore how to manage users in all organizations.](https://docs.docker.com/admin/company/users/)[Configure single sign-onDiscover how to configure SSO for your entire company.](https://docs.docker.com/security/for-admins/single-sign-on/)[Set up SCIMSet up SCIM to automatically provision and deprovision users in your company.](https://docs.docker.com/security/for-admins/provisioning/scim/)[Domain managementAdd and verify your company's domains.](https://docs.docker.com/security/for-admins/domain-management/)[FAQsExplore frequently asked questions about companies.](https://docs.docker.com/faq/admin/company-faqs/)

---

# FAQs on companies

> Company FAQs

# FAQs on companies

   Table of contents

---

### Some of my organizations don’t have a Docker Business subscription. Can I still use a parent company?

Yes, but you can only add organizations with a Docker Business subscription
to a company.

### What happens if one of my organizations downgrades from Docker Business, but I still need access as a company owner?

To access and manage child organizations, the organization must have a
Docker Business subscription. If the organization isn’t included in this
subscription, the owner of the organization must manage the organization
outside of the company.

### Do company owners occupy a subscription seat?

Company owners do not occupy a seat unless one of the following is true:

- They are added as a member of an organization under your company
- SSO is enabled

Although company owners have the same access as organization owners across all
organizations in the company, it's not necessary to add them to any
organization. Doing so will cause them to occupy a seat.

When you first create a company, your account is both a company owner and an
organization owner. In that case, your account will occupy a seat as long as
you remain an organization owner.

To avoid occupying a seat,
[assign another user as the organization owner](https://docs.docker.com/admin/organization/members/#update-a-member-role) and remove yourself from the organization.
You'll retain full administrative access as a company owner without using a
subscription seat.

### What permissions does the company owner have in the associated/nested organizations?

Company owners can navigate to the **Organizations** page to view all their
nested organizations in a single location. They can also view or edit organization members and change single sign-on (SSO) and System for Cross-domain Identity Management (SCIM) settings. Changes to company settings impact all users in each organization under the company.

For more information, see
[Roles and permissions](https://docs.docker.com/enterprise/security/roles-and-permissions/).

---

# FAQs on organizations

> Organization FAQs

# FAQs on organizations

   Table of contents

---

### How can I see how many active users are in my organization?

If your organization uses a Software Asset Management tool, you can use it to
find out how many users have Docker Desktop installed. If your organization
doesn't use this software, you can run an internal survey
to find out who is using Docker Desktop.

For more information, see [Identify your Docker users and their Docker accounts](https://docs.docker.com/admin/organization/onboard/#step-1-identify-your-docker-users-and-their-docker-accounts).

### Do users need to authenticate with Docker before an owner can add them to an organization?

No. Organization owners can invite users with their email addresses, and also
assign them to a team during the invite process.

### Can I force my organization's members to authenticate before using Docker Desktop and are there any benefits?

Yes. You can
[enforce sign-in](https://docs.docker.com/enterprise/security/enforce-sign-in/).

Some benefits of enforcing sign-in are:

- Administrators can enforce features like
  [Image Access Management](https://docs.docker.com/enterprise/security/hardened-desktop/image-access-management/) and
  [Registry Access Management](https://docs.docker.com/enterprise/security/hardened-desktop/registry-access-management/).
- Administrators can ensure compliance by blocking Docker Desktop usage for
  users who don't sign in as members of the organization.

### Can I convert my personal Docker ID to an organization account?

Yes. You can convert your user account to an organization account. Once you
convert a user account into an organization, it's not possible to
revert it to a personal user account.

For prerequisites and instructions, see
[Convert an account into an organization](https://docs.docker.com/admin/organization/convert-account/).

### Do organization invitees take up seats?

Yes. A user invited to an organization will take up one of the provisioned
seats, even if that user hasn’t accepted their invitation yet.

To manage invites, see
[Manage organization members](https://docs.docker.com/admin/organization/members/).

### Do organization owners take a seat?

Yes. Organization owners occupy a seat.

### What is the difference between user, invitee, seat, and member?

- User: Docker user with a Docker ID.
- Invitee: A user that an administrator has invited to join an organization but
  has not yet accepted their invitation.
- Seats: The number of purchased seats in an organization.
- Member: A user who has received and accepted an invitation to join an
  organization. Member can also refer to a member of a team within an
  organization.

### If I have two organizations and a user belongs to both organizations, do they take up two seats?

Yes. In a scenario where a user belongs to two organizations, they take up one
seat in each organization.

---

# Activity logs

> Learn how to access and interpret Docker activity logs for organizations and repositories.

# Activity logs

   Table of contents

---

Subscription: Team  Business For: Administrators

Activity logs display a chronological list of activities that occur at organization and repository levels. The activity log provides organization owners with a record of all
member activities.

With activity logs, owners can view and track:

- What changes were made
- The date when a change was made
- Who initiated the change

For example, activity logs display activities such as the date when a repository was created or deleted, the member who created the repository, the name of the repository, and when there was a change to the privacy settings.

Owners can also see the activity logs for their repository if the repository is part of the organization subscribed to a Docker Business or Team subscription.

## Access activity logs

To view activity logs in Docker Home:

1. Sign in to [Docker Home](https://app.docker.com) and select your
  organization.
2. Select **Admin Console**, then **Activity logs**.

To view activity logs using the Docker Hub API, use the [Audit logs endpoints](https://docs.docker.com/reference/api/hub/latest/#tag/audit-logs).

## Filter and customize activity logs

> Important
>
> Docker Home retains activity logs for 30 days. To retrieve
> activities beyond 30 days, you must use the
> [Docker Hub API](https://docs.docker.com/reference/api/hub/latest/#tag/audit-logs).

By default, the **Activity** tab displays all recorded events within
the last 30 days. To narrow your view, use the calendar to select a specific
date range. The log updates to show only the activities that occurred during
that period.

You can also filter by activity type. Use the **All Activities** drop-down to
focus on organization-level, repository-level, or billing-related events.
In Docker Hub, when viewing a repository, the **Activities** tab only shows
events for that repository.

After selecting a category—**Organization**, **Repository**, or **Billing**—use
the **All Actions** drop-down to refine the results even further by specific
event type.

> Note
>
> Events triggered by Docker Support appear under the username **dockersupport**.

## Types of activity log events

Refer to the following section for a list of events and their descriptions:

### Organization events

| Event | Description |
| --- | --- |
| Team Created | Activities related to the creation of a team |
| Team Updated | Activities related to the modification of a team |
| Team Deleted | Activities related to the deletion of a team |
| Team Member Added | Details of the member added to your team |
| Team Member Removed | Details of the member removed from your team |
| Team Member Invited | Details of the member invited to your team |
| Organization Member Added | Details of the member added to your organization |
| Organization Member Removed | Details about the member removed from your organization |
| Member Role Changed | Details about the role changed for a member in your organization |
| Organization Created | Activities related to the creation of a new organization |
| Organization Settings Updated | Details related to the organization setting that was updated |
| Registry Access Management enabled | Activities related to enabling Registry Access Management |
| Registry Access Management disabled | Activities related to disabling Registry Access Management |
| Registry Access Management registry added | Activities related to the addition of a registry |
| Registry Access Management registry removed | Activities related to the removal of a registry |
| Registry Access Management registry updated | Details related to the registry that was updated |
| Single Sign-On domain added | Details of the single sign-on domain added to your organization |
| Single Sign-On domain removed | Details of the single sign-on domain removed from your organization |
| Single Sign-On domain verified | Details of the single sign-on domain verified for your organization |
| Access token created | Access token created in organization |
| Access token updated | Access token updated in organization |
| Access token deleted | Access token deleted in organization |
| Policy created | Details of adding a settings policy |
| Policy updated | Details of updating a settings policy |
| Policy deleted | Details of deleting a settings policy |
| Policy transferred | Details of transferring a settings policy to another owner |
| Create SSO Connection | Details of creating a new org/company SSO connection |
| Update SSO Connection | Details of updating an existing org/company SSO connection |
| Delete SSO Connection | Details of deleting an existing org/company SSO connection |
| Enforce SSO | Details of toggling enforcement on an existing org/company SSO connection |
| Enforce SCIM | Details of toggling SCIM on an existing org/company SSO connection |
| Refresh SCIM Token | Details of a SCIM token refresh on an existing org/company SSO connection |
| Change SSO Connection Type | Details of a connection type change on an existing org/company SSO connection |
| Toggle JIT provisioning | Details of a JIT toggle on an existing org/company SSO connection |

### Repository events

> Note
>
> Event descriptions that include a user action can refer to a Docker username, personal access token (PAT) or organization access token (OAT). For example, if a user pushes a tag to a repository, the event would include the description: `<user-access-token>` pushed the tag to the repository.

| Event | Description |
| --- | --- |
| Repository Created | Activities related to the creation of a new repository |
| Repository Deleted | Activities related to the deletion of a repository |
| Repository Updated | Activities related to updating the description, full description, or status of a repository |
| Privacy Changed | Details related to the privacy policies that were updated |
| Tag Pushed | Activities related to the tags pushed |
| Tag Deleted | Activities related to the tags deleted |
| Categories Updated | Activities related to setting or updating categories of a repository |

### Billing events

| Event | Description |
| --- | --- |
| Plan Upgraded | Occurs when your organization’s billing plan is upgraded to a higher tier plan. |
| Plan Downgraded | Occurs when your organization’s billing plan is downgraded to a lower tier plan. |
| Seat Added | Occurs when a seat is added to your organization’s billing plan. |
| Seat Removed | Occurs when a seat is removed from your organization’s billing plan. |
| Billing Cycle Changed | Occurs when there is a change in the recurring interval that your organization is charged. |
| Plan Downgrade Canceled | Occurs when a scheduled plan downgrade for your organization is canceled. |
| Seat Removal Canceled | Occurs when a scheduled seat removal for an organization’s billing plan is canceled. |
| Plan Upgrade Requested | Occurs when a user in your organization requests a plan upgrade. |
| Plan Downgrade Requested | Occurs when a user in your organization requests a plan downgrade. |
| Seat Addition Requested | Occurs when a user in your organization requests an increase in the number of seats. |
| Seat Removal Requested | Occurs when a user in your organization requests a decrease in the number of seats. |
| Billing Cycle Change Requested | Occurs when a user in your organization requests a change in the billing cycle. |
| Plan Downgrade Cancellation Requested | Occurs when a user in your organization requests a cancellation of a scheduled plan downgrade. |
| Seat Removal Cancellation Requested | Occurs when a user in your organization requests a cancellation of a scheduled seat removal. |

### Offload events

| Event | Description |
| --- | --- |
| Offload Lease Start | Occurs when an Offload lease is started in your organization. |
| Offload Lease End | Occurs when an Offload lease is ended in your organization. |

---

# Convert an account into an organization

> Convert your Docker Hub user account into an organization

# Convert an account into an organization

   Table of contents

---

Subscription: Team  Business For: Administrators

Learn how to convert an existing user account into an organization. This is
useful if you need multiple users to access your account and the repositories
it’s connected to. Converting it to an organization gives you better control
over permissions for these users through
[teams](https://docs.docker.com/admin/organization/manage-a-team/) and
[roles](https://docs.docker.com/enterprise/security/roles-and-permissions/).

When you convert a user account to an organization, the account is migrated to
a Docker Team subscription by default.

## Prerequisites

Before you convert a user account to an organization, ensure that you meet the following requirements:

- The user account that you want to convert must not be a member of a company or any teams or organizations. You must remove the account from all teams, organizations, or the company.
  To do this:
  1. Navigate to **My Hub** and then select the organization you need to leave.
  2. Find your username in the **Members** tab.
  3. Select the **More options** menu and then select **Leave organization**.
  If the user account is the sole owner of any organization or company, assign another user the owner role and then remove yourself from the organization or company.
- You must have a separate Docker ID ready to assign as the owner of the organization during conversion.
  If you want to convert your user account into an organization account and you don't have any other user accounts, you need to create a new user account to assign it as the owner of the new organization. With the owner role assigned, this user account has full administrative access to configure and manage the organization. You can assign more users the owner role after the conversion.

## What happens when you convert your account

The following happens when you convert your account into
an organization:

- This process removes the email address for the account. Notifications are
  instead sent to organization owners. You'll be able to reuse the
  removed email address for another account after converting.
- The current subscription will automatically cancel and your new subscription
  will start.
- Repository namespaces and names won't change, but converting your account
  removes any repository collaborators. Once you convert the account, you'll need
  to add repository collaborators as team members.
- Existing automated builds appear as if they were set up by the first owner
  added to the organization.
- The user account that you add as the first owner will have full
  administrative access to configure and manage the organization.
- To transfer a user's personal access tokens (PATs) to your converted
  organization, you must designate the user as an organization owner. This will
  ensure any PATs associated with the user's account are transferred to the
  organization owner.

## Convert an account into an organization

> Important
>
> Converting an account into an organization is permanent. Back up any data
> or settings you want to retain.

1. Sign in to [Docker Home](https://app.docker.com/).
2. Select your avatar in the top-right corner to open the drop-down.
3. From **Account settings**, select **Convert**.
4. Review the warning displayed about converting a user account. This action
  cannot be undone and has considerable implications for your assets and the
  account.
5. Enter a **Username of new owner** to set an organization owner. The new
  Docker ID you specify becomes the organization’s owner. You cannot use the
  same Docker ID as the account you are trying to convert.
6. Select **Confirm**. The new owner receives a notification email. Use that
  owner account to sign in and manage the new organization.

---

# Deactivate an organization

> Learn how to deactivate a Docker organization and required prerequisite steps.

# Deactivate an organization

   Table of contents

---

For: Administrators

Learn how to deactivate a Docker organization, including required prerequisite
steps. For information about deactivating user
accounts, see [Deactivate a user account](https://docs.docker.com/accounts/deactivate-user-account/).

> Warning
>
> All Docker products and services that use your Docker account or organization
> account will be inaccessible after deactivating your account.

## Prerequisites

You must complete all the following steps before you can deactivate your
organization:

- Download any images and tags you want to keep:
  `docker pull -a <image>:<tag>`.
- If you have an active Docker subscription, [downgrade it to a free subscription](https://docs.docker.com/subscription/change/).
- Remove all other members within the organization.
- Unlink your [GitHub and Bitbucket accounts](https://docs.docker.com/docker-hub/repos/manage/builds/link-source/#unlink-a-github-user-account).
- For Business organizations,
  [remove your SSO connection](https://docs.docker.com/enterprise/security/single-sign-on/manage/#remove-an-organization).

## Deactivate

You can deactivate your organization using either the Admin Console or
Docker Hub.

> Warning
>
> This cannot be undone. Be sure you've gathered all the data you need from
> your organization before deactivating it.

1. Sign in to [Docker Home](https://app.docker.com) and select the organization
  you want to deactivate.
2. Select **Admin Console**, then **Deactivate**. If the **Deactivate**
  button is unavailable, confirm you've completed all [Prerequisites](#prerequisites).
3. Enter the organization name to confirm deactivation.
4. Select **Deactivate organization**.

---

# Organization information

> Learn how to manage settings for organizations using Docker Admin Console.

# Organization information

   Table of contents

---

Learn how to update your organization information using the Admin Console.

## Update organization information

General organization information appears on your organization landing page in the Admin Console.

This information includes:

- Organization Name
- Company
- Location
- Website
- Gravatar email: To add an avatar to your Docker account, create a [Gravatar account](https://gravatar.com/) and upload an avatar. Next, add your Gravatar email to your Docker account settings. It may take some time for your avatar to update in Docker.

To edit this information:

1. Sign in to the [Admin Console](https://app.docker.com/admin) and
  select your organization from the top-left account drop-down.
2. Enter or update your organization’s details, then select **Save**.

## Next steps

After configuring your organization information, you can:

- [Configure single sign-on (SSO)](https://docs.docker.com/enterprise/security/single-sign-on/configure/)
- [Set up SCIM provisioning](https://docs.docker.com/enterprise/security/provisioning/scim/)
- [Manage domains](https://docs.docker.com/enterprise/security/domain-management/)
- [Create a company](https://docs.docker.com/admin/company/new-company/)
