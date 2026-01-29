# Create a Docker account and more

# Create a Docker account

> Learn how to register for a Docker ID and sign in to your account

# Create a Docker account

   Table of contents

---

You can create a free Docker account with your email address or by signing up
with your Google or GitHub account. After creating a unique Docker ID, you can
access all Docker products, including Docker Hub, Docker Desktop, and Docker Scout.

Your Docker ID becomes your username for hosted Docker services, and
[Docker forums](https://forums.docker.com/).

> Tip
>
> Explore [Docker's subscriptions](https://www.docker.com/pricing/) to see what else Docker can offer you.

## Create an account

Signing up with an email address, Google, or GitHub account requires additional verification to complete account creation:

- If you sign up with Google or GitHub, you must first verify your email address with that provider.
- If you sign up with an email address, Docker sends a verification email. Follow the procedures in that email to verify your account and complete the sign-up process.

Docker blocks sign-in until you've verified your account.

### Sign up with your email

1. Go to the [Docker sign-up page](https://app.docker.com/signup/) and enter a unique, valid email address.
2. Enter a username to use as your Docker ID. Once you create your Docker ID
  you can't reuse it in the future if you deactivate this account. Your username:
  - Must be between 4 and 30 characters long
  - Can only contain numbers and lowercase letters
3. Choose a password that's at least 9 characters long, then select **Sign Up**.
4. Verify your email address when you receive the Docker verification email. This completes the registration process.

### Sign up with Google or GitHub

1. Go to the [Docker sign-up page](https://app.docker.com/signup/).
2. Select your social provider, Google or GitHub.
3. Select the social account you want to link to your Docker account.
4. Select **Authorize Docker** to let Docker access your social account
  information. You will be re-routed to the sign-up page.
5. Enter a username to use as your Docker ID. Your username:
  - Must be between 4 and 30 characters long
  - Can only contain numbers and lowercase letters
6. Select **Sign up**.

## Sign in to your account

You can sign in with your email, Google or GitHub account, or from
the Docker CLI.

### Sign in with email or Docker ID

1. Go to the [Docker sign in page](https://login.docker.com).
2. Enter your email address or Docker ID and select **Continue**.
3. Enter your password and select **Continue**.

To reset your password, see [Reset your password](#reset-your-password).

### Sign in with Google or GitHub

You can sign in using your Google or GitHub credentials. If your social
account uses the same email address as an existing Docker ID, the
accounts are automatically linked.

If no Docker ID exists, Docker creates a new account for you.

Docker doesn't currently support linking multiple sign-in methods
to the same Docker ID.

### Sign in using the CLI

Use the `docker login` command to authenticate from the command line. For
details, see
[docker login](https://docs.docker.com/reference/cli/docker/login/).

> Warning
>
> The `docker login` command stores credentials in your home directory under
> `.docker/config.json`. The password is base64-encoded.
>
>
>
> To improve security, use
> [Docker credential helpers](https://github.com/docker/docker-credential-helpers).
> For even stronger protection, use a [personal access token](https://docs.docker.com/security/access-tokens/)
> instead of a password. This is especially useful in CI/CD environments
> or when credential helpers aren't available.

## Reset your password

To reset your password:

1. Go to the [Docker sign in page](https://login.docker.com/).
2. Enter your email address.
3. When prompted for your password, select **Forgot password?**.

## Troubleshooting

If you have a paid Docker subscription,
[contact the Support team](https://hub.docker.com/support/contact/) for assistance.

All Docker users can seek troubleshooting information and support through the
following resources, where Docker or the community respond on a best effort
basis:

- [Docker Community Forums](https://forums.docker.com/)
- [Docker Community Slack](http://dockr.ly/comm-slack)

---

# Deactivate a Docker account

> Learn how to deactivate a Docker user account.

# Deactivate a Docker account

   Table of contents

---

Learn how to deactivate an individual Docker account, including prerequisites required
for deactivation.

For information on deactivating an organization,
see [Deactivating an organization](https://docs.docker.com/admin/organization/deactivate-account/).

> Warning
>
> All Docker products and services that use your Docker account are
> inaccessible after deactivating your account.

## Prerequisites

Before deactivating your Docker account, ensure you meet the following requirements:

- If you are an organization or company owner, you must leave your organization
  or company before deactivating your Docker account:
  1. Sign in to [Docker Home](https://app.docker.com/admin) and choose
    your organization.
  2. Select **Members** and find your username.
  3. Select the **Actions** menu and then select **Leave organization**.
- If you are the sole owner of an organization, you must assign the owner role
  to another member of the organization and then remove yourself from the
  organization, or deactivate the organization. Similarly, if you are the sole
  owner of a company, either add someone else as a company owner and then remove
  yourself, or deactivate the company.
- If you have an active Docker subscription, [downgrade it to a Docker Personal subscription](https://docs.docker.com/subscription/change/).
- Download any images and tags you want to keep. Use `docker pull -a <image>:<tag>`.
- Unlink your [GitHub and account](https://docs.docker.com/docker-hub/repos/manage/builds/link-source/#unlink-a-github-user-account).

## Deactivate

Once you have completed all the previous steps, you can deactivate your account.

> Warning
>
> Deactivating your account is permanent and can't be undone. Make sure
> to back up any important data.

1. Sign in to [Docker Home](https://app.docker.com/login).
2. Select your avatar to open the drop-down menu.
3. Select **Account settings**.
4. Select **Deactivate**.
5. Select **Deactivate account**, then select again to confirm.

## Delete personal data

Deactivating your account does not delete your personal data. To request
personal data deletion, fill out Docker's
[Privacy request form](https://preferences.docker.com/).

---

# FAQs on Docker accounts

> Frequently asked questions about Docker accounts

# FAQs on Docker accounts

   Table of contents

---

### What is a Docker ID?

A Docker ID is a username for your Docker account that lets you access Docker
products. To create a Docker ID you need one of the following:

- An email address
- A social account
- A GitHub account

Your Docker ID must be between 4 and 30 characters long, and can only contain
numbers and lowercase letters. You can't use any special characters or spaces.

For more information, see
[Create a Docker ID](https://docs.docker.com/accounts/create-account/).

### Can I change my Docker ID?

No. You can't change your Docker ID once it's created. If you need a different
Docker ID, you must create a new Docker account with a new Docker ID.

Docker IDs can't be reused after deactivation.

### What if my Docker ID is taken?

All Docker IDs are first-come, first-served except for companies that have a
U.S. Trademark on a username.

If you have a trademark for your namespace,
[Docker Support](https://hub.docker.com/support/contact/) can retrieve the
Docker ID for you.

### What's an organization name or namespace?

The organization name, sometimes referred to as the organization namespace or
the organization ID, is the unique identifier of a Docker organization. The
organization name can't be the same as an existing Docker ID.

---

# Manage a Docker account

> Learn how to manage your Docker account.

# Manage a Docker account

   Table of contents

---

You can centrally manage your Docker account using Docker Home, including
adminstrative and security settings.

> Tip
>
> If your account is associated with an organization that enforces single
> sign-on (SSO), you may not have permissions to update your account settings.
> You must contact your administrator to update your settings.

## Update account information

Account information is visible on your **Account settings** page. You can
update the following account information:

- Full name
- Company
- Location
- Website
- Gravatar email

To add or update your avatar using Gravatar:

1. Create a [Gravatar account](https://gravatar.com/).
2. Create your avatar.
3. Add your Gravatar email to your Docker account settings.

It may take some time for your avatar to update in Docker.

## Update email address

To update your email address:

1. Sign in to your [Docker account](https://app.docker.com/login).
2. Select your avatar in the top-right corner and select **Account settings**.
3. Select **Email**.
4. Enter your new email address and your password to confirm the change.
5. Select **Send verification email**. Docker sends a verification
  link to your new email.

Your new email address will appear as unverified until you complete the
verification process. You can:

- Resend the verification email if needed.
- Remove the unverified email address at any time before verification.

To verify your email, open your email client and follow the instructions
in the Docker verification email.

> Note
>
> Docker accounts only support one verified email address at a time, which
> is used for account notifications and security-related communications. You
> can't add multiple verified email addresses to your account.

## Change your password

You can change your password by initiating a password reset via email. To change your password:

1. Sign in to your [Docker account](https://app.docker.com/login).
2. Select your avatar in the top-right corner and select **Account settings**.
3. Select **Password**, then **Reset password**.
4. Docker will send you a password reset email with instructions to reset
  your password.

## Manage two-factor authentication

To update your two-factor authentication (2FA) settings:

1. Sign in to your [Docker account](https://app.docker.com/login).
2. Select your avatar in the top-right corner and select **Account settings**.
3. Select **2FA**.

For more information, see
[Enable two-factor authentication](https://docs.docker.com/security/2fa/).

## Manage personal access tokens

To manage personal access tokens:

1. Sign in to your [Docker account](https://app.docker.com/login).
2. Select your avatar in the top-right corner and select **Account settings**.
3. Select **Personal access tokens**.

For more information, see
[Create and manage access tokens](https://docs.docker.com/security/access-tokens/).

## Manage connected accounts

You can unlink connected Google or GitHub accounts:

1. Sign in to your [Docker account](https://app.docker.com/login).
2. Select your avatar in the top-right corner and select **Account settings**.
3. Select **Connected accounts**.
4. Select **Disconnect** on your connected account.

To fully unlink your Docker account, you must also unlink Docker from Google
or GitHub. See Google or GitHub's documentation for more information:

- [Manage connections between your Google Account and third-parties](https://support.google.com/accounts/answer/13533235?hl=en)
- [Reviewing and revoking authorization of GitHub Apps](https://docs.github.com/en/apps/using-github-apps/reviewing-and-revoking-authorization-of-github-apps)

## Convert your account

For information on converting your account into an organization, see
[Convert an account into an organization](https://docs.docker.com/admin/organization/convert-account/).

## Deactivate your account

For information on deactivating your account, see
[Deactivating a user account](https://docs.docker.com/accounts/deactivate-user-account/).
