# Audit logs and more

# Audit logs

> Review the actions that members of your organization perform.

Audit logs are available on [Custom plans](https://mintlify.com/pricing?ref=audit-logs). Use audit logs to monitor and track actions performed by members of your organization. Audit logs provide a record of activities for security, compliance, and troubleshooting purposes.

- **Monitor security**: Track authentication attempts and permission changes.
- **Ensure compliance**: Maintain records of all organizational activities.
- **Troubleshoot issues**: Investigate failed actions and their causes.
- **Track changes**: Review who made specific changes and when.

## ​View audit logs

 Go to the [Audit log](https://dashboard.mintlify.com/settings/organization/audit-logs) page of your dashboard to view audit logs. Click on any log entry to expand it and view detailed information, including:

| Field | Description |
| --- | --- |
| Timestamp | Date and time when the action occurred |
| Actor | Email address of the user who performed the action |
| Action | What action the user performed |
| Category | Type of resource affected |
| Outcome | Whether the action succeeded or failed |
| Metadata | Additional context about the action |

### ​Filter logs

 Filter audit logs to find specific activities. **Date range**: Select a preset date range to view logs over a specific period. **Category**: Filter logs by the type of action.

| Category | Description |
| --- | --- |
| Organization | Organization settings updates and deletion requests. |
| Member | Team member invitations, removals, and role changes. |
| Deployment | Deployment configuration changes including custom domains, authentication, and Git sources. |
| Preview deployment | Preview deployment creation, updates, and authentication changes. |
| API key | API key and discovery API key creation and deletion. |
| Assistant | Assistant setting updates like deflection email, web search sites, and starter questions. |
| PDF export | PDF export generation and deletion. |
| Integration | GitHub, Slack, and Discord installations and removals. |
| Billing | Subscription updates, add-on purchases, and invoice views. |
| Quota | Overage policy and alert configuration changes. |
| User | Individual user notification settings. |
| Suggestions | Suggestion configurations and repository management. |
| Audit log | Audit log views and exports. |
| Auth | Login attempts, logouts, and session creations. |

## ​Export audit logs

 Export audit logs to CSV for analysis, compliance reporting, or long-term archival.

1. Navigate to the [Audit log](https://dashboard.mintlify.com/settings/organization/audit-logs) page of your dashboard.
2. Optionally, apply filters to narrow down the logs you want to export.
3. Click **Export CSV**.
4. Mintlify sends you an email with a download link when the export is ready.

---

# Editor permissions

> Allow more members of your team to update your documentation.

An editor has access to your dashboard and web editor. Anyone can contribute to your documentation by working locally and pushing changes to your repository, but there are key differences in how changes get deployed:

- **Editor changes**: When an editor publishes through the web editor or merges a pull request into your docs repository, changes deploy to your live site automatically.
- **Non-editor changes**: When a non-editor merges a pull request into your repository, you must manually trigger a deployment from your dashboard for those changes to appear on your live site.

## ​Add editors

 By default, the team member who created your Mintlify organization has editor access. Add additional editors in the [Members](https://dashboard.mintlify.com/settings/organization/members) page of your dashboard. Editor seats are billed based on usage, and you can have as many editors as you need. See our [pricing page](https://mintlify.com/pricing) for more details.

---

# Roles

> Assign Owner, Admin, or Editor roles to manage team access and permissions.

RBAC functionality is available on [Custom plans](https://mintlify.com/pricing?ref=rbac). Mintlify provides two dashboard access levels: Editor and Admin. The following describes actions that are limited to the Admin role:

|  | Editor | Admin |
| --- | --- | --- |
| Update user roles | ❌ | ✅ |
| Delete users | ❌ | ✅ |
| Invite admin users | ❌ | ✅ |
| Manage & update billing | ❌ | ✅ |
| Update custom domain | ❌ | ✅ |
| Update Git source | ❌ | ✅ |
| Delete org | ❌ | ✅ |

 Other actions on the dashboard are available to both roles. You can invite as many admins as you want, but we recommend limiting admin
access to users who need it.

---

# Single sign

> Set up SAML or OIDC with identity providers for team authentication.

SSO functionality is available on [Custom plans](https://mintlify.com/pricing?ref=sso). Use single sign-on to your dashboard via SAML and OIDC. If you use Okta, Google Workspace, or Microsoft Entra, we have provider-specific documentation for setting up SSO. If you use another provider, please [contact us](mailto:support@mintlify.com).

## ​Okta

- SAML
- OIDC

1

Create an application

Under `Applications`, click to create a new app integration using SAML 2.0.2

Configure integration

Enter the following:

- Single sign-on URL (provided by Mintlify)
- Audience URI (provided by Mintlify)
- Name ID Format: `EmailAddress`
- Attribute Statements:
  | Name | Name format | Value |
  | --- | --- | --- |
  | firstName | Basic | user.firstName |
  | lastName | Basic | user.lastName |

3

Send us your IdP information

Once the application is set up, navigate to the sign-on tab and send us the metadata URL.
We’ll enable the connection from our side using this information.1

Create an application

Under `Applications`, click to create a new app integration using OIDC.
You should choose the `Web Application` application type.2

Configure integration

Select the authorization code grant type and enter the Redirect URI provided by Mintlify.3

Send us your IdP information

Once the application is set up, navigate to the General tab and locate the client ID & client secret.
Please securely provide us with these, along with your Okta instance URL (for example, `<your-tenant-name>.okta.com`). You can send these via a service like 1Password or SendSafely.

## ​Google Workspace

- SAML

1

Create an application

Under `Web and mobile apps`, select `Add custom SAML app` from the `Add app` dropdown.![Screenshot of the Google Workspace SAML application creation page with the "Add custom SAML app" menu item highlighted](https://mintcdn.com/mintlify/GiucHIlvP3i5L17o/images/gsuite-add-custom-saml-app.png?fit=max&auto=format&n=GiucHIlvP3i5L17o&q=85&s=2c06c394d98ccd65df92aefceaeb75bd)2

Send us your IdP information

Copy the provided SSO URL, Entity ID, and x509 certificate and send it to the Mintlify team.![Screenshot of the Google Workspace SAML application page with the SSO URL, Entity ID, and x509 certificate highlighted. The specific values for each of these are blurred out.](https://mintcdn.com/mintlify/GiucHIlvP3i5L17o/images/gsuite-saml-metadata.png?fit=max&auto=format&n=GiucHIlvP3i5L17o&q=85&s=e9e47998599205dc051e9402cba63756)3

Configure integration

On the Service provider details page, enter the following:

- ACS URL (provided by Mintlify)
- Entity ID (provided by Mintlify)
- Name ID format: `EMAIL`
- Name ID: `Basic Information > Primary email`

![Screenshot of the Service provider details page with the ACS URL and Entity ID input fields highlighted.](https://mintcdn.com/mintlify/GiucHIlvP3i5L17o/images/gsuite-sp-details.png?fit=max&auto=format&n=GiucHIlvP3i5L17o&q=85&s=a410a25f000fe2bc4d735a6ebe7754da)On the next page, enter the following attribute statements:

| Google Directory Attribute | App Attribute |
| --- | --- |
| First name | firstName |
| Last name | lastName |

Once this step is complete and users are assigned to the application, let our team know and we’ll enable SSO for your account!

## ​Microsoft Entra

- SAML

1

Create an application

1. Under “Enterprise applications,” select **New application**.
2. Select **Create your own application** and choose “Integrate any other application you don’t find in the gallery (Non-gallery).”

2

Configure SAML

Navigate to the Single Sign-On setup page and select **SAML**. Under “Basic SAML Configuration,” enter the following:

- Identifier (Entity ID): The Audience URI provided by Mintlify.
- Reply URL (Assertion Consumer Service URL): The ACS URL provided by Mintlify.

Leave the other values blank and select **Save**.3

Configure Attributes & Claims

Edit the Attributes & Claims section:

1. Select **Unique User Identifier (Name ID)** under “Required Claim.”
2. Change the Source attribute to use `user.primaryauthoritativeemail`.
3. Under Additional claims, create the following claims:
  | Name | Value |
  | --- | --- |
  | firstName | user.givenname |
  | lastName | user.surname |

4

Send Mintlify your IdP information

Once the application is set up, navigate to the “SAML Certificates” section and send us the App Federation Metadata URL.
We’ll enable the connection from our side using this information.5

Assign Users

Navigate to “Users and groups” in your Entra application and add the users who should have access to your dashboard.
