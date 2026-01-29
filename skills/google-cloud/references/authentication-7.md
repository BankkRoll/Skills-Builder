# Tokens overviewStay organized with collectionsSave and categorize content based on your preferences. and more

# Tokens overviewStay organized with collectionsSave and categorize content based on your preferences.

# Tokens overviewStay organized with collectionsSave and categorize content based on your preferences.

This document and the [Token types](https://cloud.google.com/docs/authentication/token-types) document
cover the multiple tokens used by Google Cloud for authentication and
authorization. They're intended for people who want to learn how token-based
authentication works, or who want to implement authentication without using the
[Cloud Client Libraries](https://cloud.google.com/apis/docs/cloud-client-libraries).

You don't need to know this information when you interact with Google Cloud
APIs using the Cloud Client Libraries, the Google Cloud console, or the
Google Cloud CLI—the process of selecting the right type of token, and
obtaining and refreshing those tokens is handled automatically for you.

## User authentication

When human users interact with Google Cloud, they don't interact with
Google Cloud APIs directly. Instead, they use a *client* to act on their behalf.
The client that they use might be a web application, a desktop application, or a
utility like the Google Cloud CLI or `curl`.

Because the client makes requests and not the user, Google Cloud can't request
identity information from the user directly to check if they have permission to
use an API. Instead, this identity is passed to the API through the client in
the form of a token, which is included in each API request.

A user authentication token encodes the following information:

- The identity of the user.
- The identity of the client.
- Assurance that the client is allowed to act on behalf of the user.

Authenticating the user and authorizing the client involves the following
parties:

- A user.
- A client that acts on behalf of the user.
- An authorization server, which Google APIs rely on to authenticate the client.
- A Google Cloud API that the client interacts with.

Clients can't issue tokens themselves. Instead, they must work with an
authorization server to do the following:

1. Authenticate the user.
2. Authenticate the client.
3. Authorize the client to act on the user's behalf.
4. Issue a token to the client.

 ![A relationship diagram of a user authenticating through a client](https://cloud.google.com/static/docs/authentication/images/user-token.svg)
A user who authenticates by signing in to their Google Account is a
[userprincipal](https://cloud.google.com/architecture/identity/overview-google-authentication#google_identities).
The principal has a [principal identifier](https://cloud.google.com/iam/docs/principal-identifiers)
similar to the following:

```
user:alex@example.com
```

A user who authenticates using
[workforce identity federation](https://cloud.google.com/iam/docs/workforce-identity-federation) and an
external identity provider is a *workforce identity pool* principal. The
principal has a principal identifier similar to the following:

```
principal://iam.googleapis.com/locations/global/workforcePools/POOL_ID/subject/raha@altostrat.com
```

## Workload authentication

Some clients need to interact with Google APIs on their own behalf. For example,
a scheduled job might need to read data from BigQuery or
Cloud Storage without any human user being involved.

Clients that act unattended and on their own behalf are referred to as
*workloads*. Unlike user authentication, workload authentication combines
authenticating the user and authorizing the client into a single step. Because
of this, a workload authentication token encodes the identity of only the
client.

Workload authentication and authorization involves the following parties:

- A workload, acting as both a client and a user, and on its own behalf.
- An authorization server, which Google APIs rely on to authenticate the client.
- A Google Cloud API that the client interacts with.

To access Google Cloud APIs, clients must work with an authorization server to
do the following:

1. Authenticate the client.
2. Authorize the client.
3. Issue a token to the client.

 ![A relationship diagram of a workload authenticating through a client](https://cloud.google.com/static/docs/authentication/images/workload-token.svg)

An authenticated workload is also referred to as a principal, but workloads use
different principal identifiers than users.

A workload that authenticates using a service account is a
[service accountprincipal](https://cloud.google.com/architecture/identity/overview-google-authentication#service_account).
The principal has a principal identifier similar to the following:

```
serviceAccount:my-service-account@my-project.iam.gserviceaccount.com
```

A workload that authenticates using
[workload identity federation](https://cloud.google.com/iam/docs/workload-identity-federation) is a
*workload identity pool* principal. The principal has a principal identifier
similar to the following:

```
principal://iam.googleapis.com/projects/PROJECT_NAME/locations/global/workloadIdentityPools/POOL_ID/subject/SUBJECT_ATTRIBUTE_VALUE
```

## Authorization servers

Google Cloud shares specific authentication and authorization facilities with
other Google services. Shared facilities include
[Sign in with Google](https://developers.google.com/identity/siwg), and the
[OpenID Connect](https://developers.google.com/identity/openid-connect/openid-connect)
and
[OAuth 2.0](https://developers.google.com/identity/protocols/oauth2) services
provided by [Google Identity](https://developers.google.com/identity).

Other authentication-related services, such as Workload Identity Federation and
Workforce Identity Federation, are specific to Google Cloud and can't be used for
other Google services.

Because of this split, Google Cloud uses two authorization servers. One is
shared with other Google services, and the other is specific to Google Cloud.
The following table describes the different servers and their properties.

| Authorization server | Authentication type | Authentication APIs | Principals |
| --- | --- | --- | --- |
| Google authorization server | User authenticationWorkload authentication | Google OAuth 2.0 APISAML | User (managed user)User (consumer account)Service account |
| Google Cloud Identity and Access Management (IAM) authorization server | User authenticationWorkload authentication | Security Token Service(STS) APIIAMService Account Credentials APIMetadata servers | Workforce identity pool principalWorkload identity pool principalService account |

The authorization servers are global services and can be accessed from any
[Google Cloud region](https://cloud.google.com/about/locations). However, not all regions contain
deployments of both authorization servers:

- The Google authorization server is available in select regions.
- The Google Cloud IAM authorization server is available in all regions.

To optimize reliability, use the Google Cloud IAM authorization
server whenever possible.

## What's next

Read about [token types](https://cloud.google.com/docs/authentication/token-types).

   Was this helpful?

---

# Troubleshoot your ADC setupStay organized with collectionsSave and categorize content based on your preferences.

# Troubleshoot your ADC setupStay organized with collectionsSave and categorize content based on your preferences.

This page describes some common problems you might encounter when using
Application Default Credentials (ADC).

For information about how ADC works, including where credentials are found, see
[How Application Default Credentials works](https://cloud.google.com/docs/authentication/application-default-credentials).

## User credentials not working

If your API request returns an error message about user credentials not being
supported by this API, the API not being enabled in the project, or no quota
project being set, review the following information.

There are two kinds of Google Cloud APIs:

- *Resource-based APIs*, which use the project associated with the resources
    being accessed for billing and quota.
- *Client-based APIs*, which use the project associated with the client
    accessing the resources for billing and quota.

When you provide user credentials to authenticate to a client-based API, you
must specify the project to use for billing and quota. This project is called
the *quota project*.

There are a number of ways to specify a quota project, including the following
options:

- Update your ADC file to use a different project as the quota project:
  ```
  gcloud auth application-default set-quota-project YOUR_PROJECT
  ```
- If you are using the gcloud CLI to call the API, you can set
  your quota project in your gcloud CLI config:
  ```
  gcloud config set billing/quota_project YOUR_PROJECT
  ```
- If you are calling the REST or RPC API directly, use the
  `x-goog-user-project` HTTP header to specify a quota project in each
  request. For details, see
  [Set the quota project with a REST request](https://cloud.google.com/docs/authentication/rest#set-billing-project).

You must have the `serviceusage.services.use` IAM permission for
a project to be able to designate it as your billing project. The
`serviceusage.services.use` permission is included in the Service Usage Consumer
IAM role. If you don't have the `serviceusage.services.use`
permission for any project, contact your security administrator or a project
owner who can give you the Service Usage Consumer role in the project.

For more information about quota projects, see
[Quota project overview](https://cloud.google.com/docs/quotas/quota-project). For information about additional ways
to set the quota project, see [Set the quota project](https://cloud.google.com/docs/quotas/set-quota-project).

## Incorrect credentials

If your credentials don't seem to be providing the access you expect, or aren't
found, check the following:

- If you are using the gcloud CLI to access Google Cloud in a
  local environment, make sure you understand which credentials you are using.
  When you use the gcloud CLI, you are using the credentials you
  provided to the gcloud CLI by using the `gcloud auth login`
  command. You are not using the credentials you provided to ADC. For more
  information about these two sets of credentials, see
  [gcloud CLI authentication configuration and ADC configuration](https://cloud.google.com/docs/authentication/gcloud#gcloud-credentials).
- Make sure that the `GOOGLE_APPLICATION_CREDENTIALS` environment variable is
  set *only* if you are using a service account key or other JSON file for ADC.
  The credentials pointed to by the environment variable take precedence over
  other credentials, including for Workload Identity Federation for GKE.
- Confirm that the principal making the request has the required
  IAM roles. If you are using user credentials, then the roles
  must be granted to the email address associated with the user account. If
  you are using a service account, then that service account must have the
  required roles.
- If you provide an API key with the API request, the API key takes precedence
  over ADC in any location. If you have set the `GOOGLE_APPLICATION_CREDENTIALS`
  environment variable and you are using an API key, the API might return a
  warning telling you that the credentials you provided to ADC are being
  ignored. To stop the warning, unset the `GOOGLE_APPLICATION_CREDENTIALS`
  environment variable.

## Unrecognized credential type

If your API request returns an error that includes `Error creating credential
from JSON. Unrecognized credential type`, make sure you are using a valid
credential. Client ID files are not supported to provide credentials for ADC.

## Error returned for local credentials from service account impersonation

Credentials from a local ADC file generated by using service account
impersonation are not supported by all of the authentication libraries. If your
call returns an error similar to `Neither metadata server or valid service
account credentials are found`, you can't use local impersonated credentials for
this task.

To avoid this error, create your ADC file from your user credentials or run your
code in an environment that has a metadata server available (such as
Compute Engine).

## Unknown project764086051850used for request

Project `764086051850` is the project used by the gcloud CLI. If you
see authentication errors referencing this project, you are trying to use
a client-based API and you have not set both your project and your quota
project for your configuration.

For more information, see [User credentials not working](#user-creds-client-based).

## Access blocked when using scopes

When you attempt to create a local ADC file, and an error similar to `This app
is blocked` or `Access blocked: Authorization Error` is returned, you might be
attempting to use scopes that aren't supported by the
[default ADC setup command](https://cloud.google.com/docs/authentication/set-up-adc-local-dev-environment#google-idp). Typically, this issue is caused by
adding scopes for applications outside of Google Cloud, such as Google
Drive.

By default, the access tokens generated from a local ADC file created with user credentials include
the [cloud-wide scopehttps://www.googleapis.com/auth/cloud-platform](https://cloud.google.com/docs/authentication#authorization-gcp).
To specify scopes explicitly, you use the
[--scopesflag](https://cloud.google.com/sdk/gcloud/reference/auth/application-default/login#--scopes)
with the `gcloud auth application-default login` command.

To add scopes for services outside of Google Cloud, such as Google Drive, you can do one of
the following:

- **OAuth authentication**:
      [Create an OAuth client ID](https://support.google.com/cloud/answer/6158849).
      Provide the client ID to the `gcloud auth application-default login` command
      by using the
      [--client-id-fileflag](https://cloud.google.com/sdk/gcloud/reference/auth/application-default/login#--client-id-file), and specify your scopes with the
      [--scopesflag](https://cloud.google.com/sdk/gcloud/reference/auth/application-default/login#--scopes).
- **Service account authentication**: Create a service account.
      [Impersonate the service account](https://cloud.google.com/docs/authentication/use-service-account-impersonation) by providing its email address to the
      `gcloud auth application-default login` command with the
         `--impersonate-service-account` flag, and specify your scopes with the
      [--scopesflag](https://cloud.google.com/sdk/gcloud/reference/auth/application-default/login#--scopes).

---

# Authentication and authorization use casesStay organized with collectionsSave and categorize content based on your preferences.

# Authentication and authorization use casesStay organized with collectionsSave and categorize content based on your preferences.

This page lists some common authentication and authorization use cases, with
links to more information about how to implement each use case.

For an overview of authentication at Google, see
[Authentication at Google](https://cloud.google.com/docs/authentication).

## Authenticate to Google APIs

Google APIs require a valid access token or API key with every request. How you
provide these required credentials depends on where your code is
running and what types of credentials the API accepts.

### Use the client libraries and Application Default Credentials

The recommended way to use Google APIs is to use a client library and
[Application Default Credentials (ADC)](https://cloud.google.com/docs/authentication/application-default-credentials).

[Application Default Credentials (ADC)](https://cloud.google.com/docs/authentication/application-default-credentials) is a strategy used by the authentication libraries
to automatically find credentials based on the application environment. The authentication libraries
make those credentials available to
[Cloud Client Libraries and Google API Client Libraries](https://cloud.google.com/apis/docs/client-libraries-explained).
When you use ADC, your code can run in either a development or production environment without
changing how your application authenticates to Google Cloud services and APIs.

How you [set up ADC](https://cloud.google.com/docs/authentication/provide-credentials-adc) depends on where your code is running.
ADC supports both [authenticating as a service account](https://cloud.google.com/docs/authentication/application-default-credentials#attached-sa) and
[authenticating as a user](https://cloud.google.com/docs/authentication/application-default-credentials#personal).

### Authenticate from Google Kubernetes Engine (GKE)

You use
[Workload Identity Federation for GKE](https://cloud.google.com/kubernetes-engine/docs/concepts/workload-identity) to
enable your workloads running on GKE to securely access
Google APIs. Workload Identity Federation for GKE lets a GKE service account
in your GKE cluster act as an Identity and Access Management (IAM)
service account.

### Authenticate from Knative serving

You authenticate your Knative serving services by using
[Workload Identity Federation for GKE](https://cloud.google.com/anthos/run/docs/securing/workload-identity),
which lets you access Google APIs.

### Use an API that accepts API keys

If an API supports [API keys](https://cloud.google.com/docs/authentication/api-keys), an API key can be
provided with a request instead of the access token.
API keys associate the request with a Google Cloud project
for billing and quota purposes.

To determine whether an API
supports API keys, see the documentation for your API.

### Use self-signed JSON Web Tokens (JWTs)

Some Google APIs support self-signed JSON Web Tokens (JWTs) instead of access
tokens. Using a self-signed JWT lets you avoid making a network request to
Google's authorization server. This approach requires that you
[create your own signed JWT](https://developers.google.com/identity/protocols/oauth2/service-account#jwt-auth).
For more information about tokens, see
[Tokens overview](https://cloud.google.com/docs/authentication/tokens).

### Use the authentication libraries and packages

If [ADC](#adc) and the OAuth implementation provided by the
Cloud Client Libraries or Google API Client Libraries isn't available
in your environment, you can use the authentication libraries and packages.

The following authentication libraries and packages are available:

- [C#](https://developers.google.com/api-client-library/dotnet/guide/aaa_oauth)
- [Go](https://pkg.go.dev/google.golang.org/api/transport)
- [Java](https://github.com/googleapis/google-auth-library-java)
- [Node.js](https://github.com/googleapis/google-auth-library-nodejs)
- [PHP](https://github.com/googleapis/google-auth-library-php)
- [Python](https://github.com/googleapis/google-auth-library-python)
- [Ruby](https://github.com/googleapis/google-auth-library-ruby)

You can also implement the OAuth 2.0 flow using Google's OAuth 2.0 endpoints.
This approach requires a more detailed understanding of how
[OAuth 2.0](https://datatracker.ietf.org/doc/html/rfc6749) and
[OpenID Connect](https://developers.google.com/identity/protocols/oauth2/openid-connect)
work. For more information, see
[Using OAuth 2.0 for Web Server Applications](https://developers.google.com/identity/protocols/oauth2/web-server).

## Google Cloud service-specific use cases

Some Google Cloud services support authentication flows specific to that
service.

### Provide time-limited access to a Cloud Storage resource using signed URLs

[Signed URLs](https://cloud.google.com/storage/docs/access-control/signed-urls) provide
[time-limited access to a specific Cloud Storage resource](https://cloud.google.com/storage/docs/access-control/signing-urls-with-helpers).

### Authenticate to GKE Enterprise clusters

You can authenticate to GKE Enterprise clusters using Google Cloud
identities or by using a third-party identity provider:

- [Authenticate with Google Cloud identities, by using the Connect gateway](https://cloud.google.com/anthos/multicluster-management/gateway).
- [Authenticate with a third-party identity provider that supports OIDC or LDAP, by using GKE Identity Service](https://cloud.google.com/anthos/identity).

### Configure an API deployed with API Gateway or Cloud Endpoints for authentication

API Gateway and Cloud Endpoints support service-to-service
authentication and user authentication with Firebase,
[Google-signed ID tokens](https://cloud.google.com/docs/authentication/token-types#identity-tokens),
Okta, Auth0, and JWTs.

For information, see the product documentation:

- [Choosing an authentication method for API Gateway](https://cloud.google.com/api-gateway/docs/authentication-method)
- [Choosing an authentication method for Cloud Endpoints](https://cloud.google.com/endpoints/docs/openapi/authentication-method)

## Authentication for applications hosted on Cloud Run or Cloud Run functions

Applications hosted on Cloud Run and Cloud Run functions require
[ID tokens](https://cloud.google.com/docs/authentication/token-types#identity-tokens) for
authentication.

For information about other ways to acquire an ID token, see
[Get an ID token](https://cloud.google.com/docs/authentication/get-id-token). For more information about ID tokens, see
[Identity tokens](https://cloud.google.com/docs/authentication/token-types#identity-tokens).

### Cloud Run

There are various ways to
[set up a Cloud Run service](https://cloud.google.com/run/docs/authenticating/overview),
depending on how the service will be invoked. You might also need to
[authenticate to other services from a Cloud Run service](https://cloud.google.com/run/docs/authenticating/service-to-service),
which requires an OIDC ID token.

To [authenticate users to your service from a web or mobile app](https://cloud.google.com/run/docs/authenticating/end-users),
you use Identity Platform or Firebase Authentication. You can also use
Identity-Aware Proxy (IAP) to
[authenticate internal users](https://cloud.google.com/run/docs/authenticating/end-users).

### Cloud Run functions

When you invoke a function, you must
[authenticate your invocation](https://cloud.google.com/functions/docs/securing/authenticating). You can
use user credentials or an OIDC ID token.

## Authenticate application users

There are various options for authenticating the end users of your application,
depending on the rest of your application environment. Use the following
descriptions to help you understand the option that's suitable for your
application.

| Authentication service | Description |
| --- | --- |
| Google Identity Services | Google Identity Services includes Sign In With Google, Google's
        user sign-in button, and Identity Services APIs and SDK. Google Identity
        Services is based on the OAuth 2.0 and OpenID Connect (OIDC) protocols.If you're creating a mobile application, and you want to authenticate
        users using Gmail and Google Workspace accounts, Sign In With
        Google could be a good option. Sign In With Google also supports
        using Google Accounts with an existing sign-in system.Sign In With Google provides Gmail and Google Workspace account
        sign-in, and support for one-time passwords (OTP). Sign in with Google
        is targeted toward Google-only accounts, or Google Accounts in an
        existing sign-in system, for mobile applications.Sign in With Google is available foriOS,Android,
        andweb applications. |
| Firebase Authentication | Firebase Authentication provides authentication services and libraries to
        authenticate users to your application for a wide array of user account
        types.If you want to accept user sign-ins from multiple platforms,
        Firebase Authentication could be a good option.Firebase Authentication provides authentication support for many
        user account types. Firebase Authentication supports password
        authentication and federated sign-in with Google, Facebook,
        Twitter, and other platforms.Firebase Authentication uses Identity Platform as its backend but serves a different audience:Firebase Authentication is aimed at consumer applications, and offers a subset of features
            compared to Identity Platform.Identity Platform is intended for building enterprise-focused SaaS applications.
            It lets you integrate with enterprise IdPs using inbound OIDC or SAML.For more information about the differences between these products, seeDifferences between Identity Platform and Firebase Authentication.The following links provide more information:Where do I start with Firebase Authentication?helps you understand some ways of using Firebase Authentication.For Python applications running in the App Engine standard environment, seeAuthenticating users with Firebase. |
| Identity Platform | Identity Platform is a customer identity and access management (CIAM)
        platform that helps organizations add enterprise-grade identity
        management capability to their applications.Identity Platformprovides a drop-in,
            customizable identity and authentication service for user
            sign-up and sign-in. Identity Platform supports multiple
            authentication methods: SAML, OIDC, email/password, social, phone,
            and custom options.Firebase Authentication uses Identity Platform as its backend but serves a different audience:Firebase Authentication is aimed at consumer applications, and offers a subset of features
            compared to Identity Platform.Identity Platform is intended for building enterprise-focused SaaS applications.
            It lets you integrate with enterprise IdPs using inbound OIDC or SAML.For more information about the differences between these products, seeDifferences between Identity Platform and Firebase Authentication. |
| OAuth 2.0 and OpenID Connect | OpenID Connect lets you handle and use authentication tokens with the
        most customization.If you want maximum control over your OAuth 2.0 implementation, and
        you're comfortable implementing OAuth 2.0 flows, consider this option.Google's OAuth 2.0 implementation conforms to theOpenID Connect specificationand isOpenID Certified.
        OpenID Connect is an identity layer on top of the OAuth 2.0 protocol.
        Your application can use OpenID Connect tovalidate the ID tokenandretrieve user profile information.OAuth 2.0 can be used to implement programmatic authentication to anIdentity-Aware Proxy-secured resource. |
| Identity-Aware Proxy (IAP) | IAP lets you control access to your
      application before requests reach your application resources.Unlike the other authentication services in this table, which are
          implemented within your application, IAP performs
          authentication before your application can be reached.With IAP, you establish a central authorization layer
        for applications and usesigned headersto secure your app. IAP-protected applications can be
        accessed only byprincipalsthat have the correctIAM role.
        When an end user tries to access an IAP-secured resource,
        IAP performs authentication and authorization checks
        for you. IAP doesn't protect against activity within a
        project, such as another service in the same project.For Google identities, IAP usesID tokens. For more information, seeProgrammatic authentication.For information about how IAP secures your
          application resources, see theIAP overview.The following language-specific tutorials are available for
            IAP:Authenticating users with GoAuthenticating users with Node.jsAuthenticating users with PHPAuthenticating users with PythonAuthenticating users with Ruby |
| App Engine Users API | For applications running in the App Engine standard environment, the Users API
      is available to provide user authentication for some
      languages. |
| Authorizing access for end-user resources | If your application accesses resources that are owned by your end
      user, you must secure their permission to do so. This use case is
      sometimes calledthree-legged OAuthor3LO, because
      there are three entities involved: the application, the authorization
      server, and the user. |

## Authentication and authorization options for Google Cloud and Google Workspace

Google Cloud and Google Workspace provide various options for
setting up access, enhancing account security, and administering accounts.

### Grant access to Google Cloud resources for external workloads

[Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation) lets you
grant on-premises or multi-cloud workloads access to Google Cloud
resources. Historically, this use case required the use of service account keys,
but Workload Identity Federation avoids the maintenance and
[security burden of using service account keys](https://cloud.google.com/iam/docs/best-practices-for-managing-service-account-keys).
Workload Identity Federation supports
[OIDC-compatible or SAML 2.0-compatible identity providers](https://cloud.google.com/iam/docs/workload-identity-federation#providers).

### Set up an identity provider

You can
[use Google as your identity provider](https://cloud.google.com/architecture/identity/overview-google-authentication#google_for_organizations),
by using Cloud Identity or Google Workspace. You can also
[federate a Cloud Identity or Google Workspace account with an external identity provider](https://cloud.google.com/architecture/identity/overview-google-authentication#external_identities). This approach uses SAML,
enabling your employees to use their existing identity and credentials to sign
in to Google services.

### Set up two-factor authentication

Requiring two-factor authentication is a best practice that helps to prevent bad
actors from accessing an account when they have gained access to the credentials
for that account. With two-factor authentication, a second piece of information
or identification from the user is required before that user is authenticated.
Google's provides several solutions that support the
[FIDO (Fast IDentity Online)](https://fidoalliance.org/certification/fido-certified-products/)
standard.

Identity Platform supports two-factor authentication for
[web](https://cloud.google.com/identity-platform/docs/web/mfa), [iOS](https://cloud.google.com/identity-platform/docs/ios/mfa),
and [Android](https://cloud.google.com/identity-platform/docs/android/mfa) apps.

Google Identity Services supports
[FIDO (Fast IDentity Online) authentication](https://developers.google.com/identity/fido).

Google supports various hardware solutions for two-factor authentication, such
as [Titan Keys](https://cloud.google.com/titan-security-key).

### Set up certificate-based access

Part of the Chrome Enterprise Premium zero trust solution, certificate-based access
[limits access to only authenticated users on a trusted device](https://cloud.google.com/chrome-enterprise-premium/docs/securing-resources-with-certificate-based-access),
identifying devices through their X.509 certificates. Certificate-based access
is also sometimes referred to as mutual Transport Layer Security (mTLS).

## General account and authentication information

### Get help with accessing a Google Account

If you need help with accessing or managing a Google Account, see the
[Google Account support page](https://support.google.com/accounts#topic=).

### Handle compromised credentials

If you believe that your credentials have been compromised, there are steps
you or your administrator can take to mitigate the situation. For more
information, see
[Handling compromised Google Cloud credentials](https://cloud.google.com/docs/security/compromised-credentials).

### Get help with certificate authority issues

If you see errors related to an issue with your certificate or certificate
authority (CA), including your root CA, see the
[Google Trust Services FAQ](https://pki.goog/faq) for more information.

---

# Use service account impersonationStay organized with collectionsSave and categorize content based on your preferences.

# Use service account impersonationStay organized with collectionsSave and categorize content based on your preferences.

When the principal you are using doesn't have the permissions you need to
accomplish your task, or you want to use a service account in a development
environment, you can use *service account impersonation*.

When you use service account impersonation, you start with an authenticated
principal (your user account or a service account) and request short-lived
credentials for a service account that has the authorization that your use case
requires. The authenticated principal must have the
[necessary permissions](#required-roles) to impersonate the service account.

Service account impersonation is more secure than using a service account key
because service account impersonation requires a prior authenticated identity,
and the credentials that are created by using impersonation do not persist.
In comparison, authenticating with a service account key requires no prior
authentication, and the persistent key is a high risk credential if exposed.

For more information about service account impersonation, see
[Service account impersonation](https://cloud.google.com/iam/docs/service-account-impersonation).

## Before you begin

Before you use service account impersonation, you need to enable the required
APIs and ensure that you have the required roles.

### Enable APIs

To impersonate a service account, you need to enable the
Service Account Credentials API in your project.

To enable APIs, you need the Service Usage Admin IAM
          role (`roles/serviceusage.serviceUsageAdmin`), which
          contains the `serviceusage.services.enable` permission. [Learn how to grant
          roles](https://cloud.google.com/iam/docs/granting-changing-revoking-access).

[Enable the API](https://console.cloud.google.com/flows/enableapi?apiid=iamcredentials.googleapis.com)

### Required roles

To get the permission that
      you need to impersonate a service account,

      ask your administrator to grant you the

      [Service Account Token Creator](https://cloud.google.com/iam/docs/roles-permissions/iam#iam.serviceAccountTokenCreator) (`roles/iam.serviceAccountTokenCreator`)
     IAM role on the service account.

  For more information about granting roles, see [Manage access to projects, folders, and organizations](https://cloud.google.com/iam/docs/granting-changing-revoking-access).

This predefined role contains the
        ` iam.serviceAccounts.getAccessToken`
        permission,
         which is required to
        impersonate a service account.

You might also be able to get
          this permission
        with [custom roles](https://cloud.google.com/iam/docs/creating-custom-roles) or
        other [predefined roles](https://cloud.google.com/iam/docs/roles-overview#predefined).

You must grant these roles to your account, even when you are working in a
project that you created.

For more information about roles required for impersonation, see
[Roles for service account authentication](https://cloud.google.com/iam/docs/service-account-permissions#directly-impersonate).

You can use service account impersonation using the following methods:

- [Use the gcloud CLI](#gcloud)
- [Set up Application Default Credentials for using client libraries](#adc)
- [Generate and manage short-lived credentials](#short-lived-creds)

## Use the gcloud CLI

The gcloud CLI provides a straightforward way to use service account
impersonation. This method works well when you need to use a service account
to access Google Cloud resources or services by using the
gcloud CLI.

You can impersonate a service account for a specific gcloud CLI
command or set up the gcloud CLI to use impersonation for every
command automatically.

### Use impersonation for a specific gcloud CLI command

To use impersonation for a specific gcloud CLI command, you use the
[--impersonate-service-accountflag](https://cloud.google.com/sdk/gcloud/reference#--impersonate-service-account). For example, the
following command lists storage buckets, using the identity and access provided
by the specified service account:

```
gcloud storage buckets list --impersonate-service-account=SERVICE_ACCT_EMAIL
```

When you use this flag, the gcloud CLI requests short-lived
credentials for the specified service account and uses them to authenticate
to the API and authorize the access. The principal that is logged in to the
gcloud CLI (usually your user account) must have the required
permission on the service account.

### Use impersonation with the gcloud CLI by default

To set up the gcloud CLI to use the identity and access provided by
a service account by default, you use the
[gcloud CLI config command](https://cloud.google.com/sdk/gcloud/reference/config):

```
gcloud config set auth/impersonate_service_account SERVICE_ACCT_EMAIL
```

With this config property set, the gcloud CLI requests short-lived
credentials for the specified service account and uses them to authenticate
to the API and authorize the access to the resource for every command.
The principal that is logged in to the gcloud CLI must have the
required permission on the service account.

## Set up Application Default Credentials for using client libraries

You can use service account impersonation to set up a local Application Default
  Credentials (ADC) file. Client libraries that support impersonation
  can use those credentials automatically. Local ADC files created by using
  impersonation are supported in the following languages:

- C#
- Go
- Java
- Node.js
- Python

Use service account impersonation to create a local ADC file:

```
gcloud auth application-default login --impersonate-service-account SERVICE_ACCT_EMAIL
```

You can now use client libraries using the supported languages the same way you would after
  setting up a local ADC file with user credentials. Credentials are automatically found by the
  authentication libraries. For more information, see
  [Authenticate for using client libraries](https://cloud.google.com/docs/authentication/client-libraries).

Credentials from a local ADC file generated by using service account impersonation are not
  supported by all of the authentication libraries. For more information, see
  [Error returned for local credentials from service account impersonation](https://cloud.google.com/docs/authentication/troubleshoot-adc#local-impersonated).

## Generate and manage short-lived credentials

If neither of the previous methods address your use case, you need to
generate and manage short-lived tokens. For example, if you need a different
type of short-lived credential (something other than an access token), or if
you need to use impersonation in a production environment, use this method.

For information about generating short-lived tokens, see
[Create short-lived credentials for a service account](https://cloud.google.com/iam/docs/create-short-lived-credentials-direct).

## What's next

- Learn more about [how ADC finds credentials](https://cloud.google.com/docs/authentication/application-default-credentials).
- Explore [authentication methods](https://cloud.google.com/docs/authentication).

   Was this helpful?
