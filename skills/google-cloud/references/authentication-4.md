# Authenticate for using the gcloud CLIStay organized with collectionsSave and categorize content based on your preferences. and more

# Authenticate for using the gcloud CLIStay organized with collectionsSave and categorize content based on your preferences.

# Authenticate for using the gcloud CLIStay organized with collectionsSave and categorize content based on your preferences.

This page describes various ways to sign in to the gcloud CLI.
The Google Cloud CLI is a command-line tool you can use for Google Cloud
administration. Most services support the gcloud CLI.

If you plan to use client libraries or third-party development tools that
support Application Default Credentials (ADC) in a local development
environment, you need to configure ADC in your local environment. For more
information, see
[Set up Application Default Credentials for a local development environment](https://cloud.google.com/docs/authentication/set-up-adc-local-dev-environment).

How you authenticate to and use the gcloud CLI depends on where you
are running the tool:

- [In a local environment](#local)
- [Using Cloud Shell](#cloud-shell)
- [On Google Cloud compute resources](#on-gcp)

## Local environment

For most use cases, you can use your user credentials to
sign in to the gcloud CLI, but you can also use a service account.

When you sign in to the gcloud CLI in a local environment, the tool
places your access and refresh tokens in your home directory. Any user with
access to your file system can use those credentials. For more information, see
[Mitigating compromised OAuth tokens for Google Cloud CLI](https://cloud.google.com/architecture/bps-for-mitigating-gcloud-oauth-tokens).

The following table describes your options for signing in to the
gcloud CLI and how that affects the credentials used by the tool
to authenticate and authorize to Google APIs.

| Credential type | Authentication command | Notes | More information |
| --- | --- | --- | --- |
| User credentials | One of the following:gcloud init:
          Authorizes access and performs other common setup steps.gcloud auth login:
          Authorizes access only. | The gcloud CLI uses your user credentials for authentication
        and authorization for all Google APIs.To use a service account for authorization to Google APIs, useservice account impersonation. | Initialize the gcloud CLIUse service account impersonation |
| gcloud config set auth/login_config_fileWORKFORCE_IDENTITY_FEDERATION_LOGIN_CONFIGURATION_FILEgcloud auth login | Workforce Identity Federation enables users managed by an identity
      provider other than Google to access Google Cloud resources. | Sign in to the gcloud CLI with your federated identityWorkforce Identity Federation |  |
| Service account | gcloud auth login --cred-file=WORKLOAD_IDENTITY_FEDERATION_CREDENTIAL_FILE | Workload Identity Federation enables workloads running outside of
      Google Cloud to access Google Cloud resources. | Authenticate a workload |
| gcloud auth login --cred-file=SERVICE_ACCT_KEY | This method is not recommended, because using service account keys
        increases risk.To use a service account for authorization to Google APIs, sign in to
        the gcloud CLI with your user credentials, and then useservice account impersonation. | Best practices for managing service account keysUse service account impersonation |  |

## Cloud Shell

When you use Cloud Shell, you don't need to sign in to the
gcloud CLI, but you do need to authorize the use of your account
before using any development tools from Cloud Shell. After you do that,
the gcloud CLI uses your user credentials to access Google APIs.

For more information, see [Authorize with Cloud Shell](https://cloud.google.com/shell/docs/auth).

## Google Cloud compute resources

When you use the gcloud CLI on Google Cloud compute resources
such as Compute Engine virtual machines, you don't need to initialize or sign
in to the gcloud CLI, because it gets its credentials and
configuration information from the hosting compute resource by using the
metadata server.

| Credential type | Authentication command | Notes | More information |
| --- | --- | --- | --- |
| Service account | Not applicable | The gcloud CLI uses the service account attached to the
      compute resource for authentication and authorization for all Google APIs. | Set up ADC for a resource with an attached service account |

## gcloud CLI authentication configuration and ADC configuration

When you sign in to the gcloud CLI, you use the
[gcloud auth logincommand](https://cloud.google.com/sdk/gcloud/reference/auth/login) to authenticate a principal to the gcloud CLI.
The gcloud CLI uses that principal for authentication and authorization to
manage Google Cloud resources and services. This is your *gcloud CLI authentication configuration*.

When you use the gcloud CLI to configure ADC, you use
the [gcloud auth application-default login](https://cloud.google.com/sdk/gcloud/reference/auth/application-default/login) command. This
command uses the principal you provide to configure ADC for your
local environment. This is your *ADC configuration*.

Your gcloud CLI authentication configuration is distinct from your
ADC configuration. They can use the same principal or different principals. The
gcloud CLI does not use ADC to access Google Cloud resources.

The following table shows the two commands and what they do:

| Command | Description |
| --- | --- |
| gcloud auth login | Accepts credentials that are used to authenticate to and
        authorize access to Google Cloud services. |
| gcloud auth application-default login | Generates a local ADC file based on the credentials you provide
        to the command. |

Generally you use the same account to sign in to the gcloud CLI
and to configure ADC, but you can use different accounts if needed.

## What's next

- Learn more about [how ADC finds credentials](https://cloud.google.com/docs/authentication/application-default-credentials).
- [Authenticate for using Cloud Client Libraries](https://cloud.google.com/docs/authentication/client-libraries).
- Explore [authentication methods](https://cloud.google.com/docs/authentication).

   Was this helpful?

---

# Get an ID tokenStay organized with collectionsSave and categorize content based on your preferences.

# Get an ID tokenStay organized with collectionsSave and categorize content based on your preferences.

This page describes some ways to acquire a Google-signed OpenID Connect (OIDC)
ID token.

You need a Google-signed ID token for the following authentication
use cases:

- [Accessing a Cloud Run service](https://cloud.google.com/run/docs/authenticating/service-to-service)
- [Invoking a Cloud Run function](https://cloud.google.com/functions/docs/securing/authenticating)
- [Authenticating a user to an
         application secured by Identity-Aware Proxy (IAP)](https://cloud.google.com/iap/docs/authentication-howto)
- [Making a request
        to an API deployed with API Gateway or Cloud Endpoints](https://cloud.google.com/api-gateway/docs/authentication-method)

For information about ID token contents and lifetimes, see
[ID tokens](https://cloud.google.com/docs/authentication/token-types#identity-tokens).

ID tokens have a specific service or application that they can be used for,
specified by the value of their `aud` claim. This document uses the term
*target service* to refer to the service or application that the ID token can be
used to authenticate to.

When you get the ID token, you can include it in an
`Authorization` header in the request to the target service.

## Methods for getting an ID token

There are various ways to get an ID token. This page describes the following
methods:

- [Get an ID token from the metadata server](#metadata-server)
- [Use a connecting service to generate an
        ID token](#connecting-service)
- [Generate an ID token by impersonating a service
        account](#impersonation)
- [Generate a generic ID token for development with
        Cloud Run and Cloud Run functions](#generic-dev)

If you need an ID token to be accepted by an application not hosted on
Google Cloud, you can probably use these methods. However, you should
determine what ID token claims the application requires.

### Get an ID token from the metadata server

When your code is running on a resource that can have a
[service account attached to it](https://cloud.google.com/iam/docs/attach-service-accounts#attaching-to-resources),
the metadata server for the associated service can usually provide an ID token.
The metadata server generates ID tokens for the attached service account. You
cannot get an ID token based on user credentials from the metadata server.

You can get an ID token from the metadata server when your code is running
on the following Google Cloud services:

- [Compute Engine](https://cloud.google.com/compute/docs/instances/verifying-instance-identity#request_signature)
- [App Engine standard environment](https://cloud.google.com/appengine/docs/standard/python3/runtime#metadata_server)
- [App Engine flexible environment](https://cloud.google.com/appengine/docs/flexible/python/runtime#metadata_server)
- [Cloud Run functions](https://cloud.google.com/functions/docs/securing/function-identity#metadata-server)
- [Cloud Run](https://cloud.google.com/run/docs/container-contract#metadata-server)
- [Google Kubernetes Engine](https://cloud.google.com/kubernetes-engine/docs/concepts/workload-identity#instance_metadata)
- [Cloud Build](https://cloud.google.com/build/docs/securing-builds/authorize-service-to-service-access)

To retrieve an ID token from the metadata server, you query the identity
endpoint for the service account, as shown in this example.

Replace `AUDIENCE` with the URI for the target service,
for example `http://www.example.com`.

```
curl -H "Metadata-Flavor: Google" \
  'http://metadata/computeMetadata/v1/instance/service-accounts/default/identity?audience=AUDIENCE'
```

Replace `AUDIENCE` with the URI for the target service,
for example `http://www.example.com`.

```
$value = (Invoke-RestMethod `
  -Headers @{'Metadata-Flavor' = 'Google'} `
  -Uri "http://metadata/computeMetadata/v1/instance/service-accounts/default/identity?audience=AUDIENCE")
$value
```

To run this code sample, you must install the
[Auth Client Library for Java](https://github.com/googleapis/google-auth-library-java).

```
import com.google.auth.oauth2.GoogleCredentials;
import com.google.auth.oauth2.IdTokenCredentials;
import com.google.auth.oauth2.IdTokenProvider;
import com.google.auth.oauth2.IdTokenProvider.Option;
import java.io.IOException;
import java.security.GeneralSecurityException;
import java.util.Arrays;

public class IdTokenFromMetadataServer {

  public static void main(String[] args) throws IOException, GeneralSecurityException {
    // TODO(Developer): Replace the below variables before running the code.

    // The url or target audience to obtain the ID token for.
    String url = "https://example.com";

    getIdTokenFromMetadataServer(url);
  }

  // Use the Google Cloud metadata server to create an identity token and add it to the
  // HTTP request as part of an Authorization header.
  public static void getIdTokenFromMetadataServer(String url) throws IOException {
    // Construct the GoogleCredentials object which obtains the default configuration from your
    // working environment.
    GoogleCredentials googleCredentials = GoogleCredentials.getApplicationDefault();

    IdTokenCredentials idTokenCredentials =
        IdTokenCredentials.newBuilder()
            .setIdTokenProvider((IdTokenProvider) googleCredentials)
            .setTargetAudience(url)
            // Setting the ID token options.
            .setOptions(Arrays.asList(Option.FORMAT_FULL, Option.LICENSES_TRUE))
            .build();

    // Get the ID token.
    // Once you've obtained the ID token, you can use it to make an authenticated call to the
    // target audience.
    String idToken = idTokenCredentials.refreshAccessToken().getTokenValue();
    System.out.println("Generated ID token.");
  }
}
```

```
import (
	"context"
	"fmt"
	"io"

	"golang.org/x/oauth2/google"
	"google.golang.org/api/idtoken"
	"google.golang.org/api/option"
)

// getIdTokenFromMetadataServer uses the Google Cloud metadata server environment
// to create an identity token and add it to the HTTP request as part of an Authorization header.
func getIdTokenFromMetadataServer(w io.Writer, url string) error {
	// url := "http://www.example.com"

	ctx := context.Background()

	// Construct the GoogleCredentials object which obtains the default configuration from your
	// working environment.
	credentials, err := google.FindDefaultCredentials(ctx)
	if err != nil {
		return fmt.Errorf("failed to generate default credentials: %w", err)
	}

	ts, err := idtoken.NewTokenSource(ctx, url, option.WithCredentials(credentials))
	if err != nil {
		return fmt.Errorf("failed to create NewTokenSource: %w", err)
	}

	// Get the ID token.
	// Once you've obtained the ID token, you can use it to make an authenticated call
	// to the target audience.
	_, err = ts.Token()
	if err != nil {
		return fmt.Errorf("failed to receive token: %w", err)
	}
	fmt.Fprintf(w, "Generated ID token.\n")

	return nil
}
```

To run this code sample, you must install the
[Google Auth Library for Node.js](https://github.com/googleapis/google-auth-library-nodejs)

```
/**
 * TODO(developer):
 *  1. Uncomment and replace these variables before running the sample.
 */
// const targetAudience = 'http://www.example.com';

const {GoogleAuth} = require('google-auth-library');

async function getIdTokenFromMetadataServer() {
  const googleAuth = new GoogleAuth();

  const client = await googleAuth.getIdTokenClient(targetAudience);

  // Get the ID token.
  // Once you've obtained the ID token, you can use it to make an authenticated call
  // to the target audience.
  await client.idTokenProvider.fetchIdToken(targetAudience);
  console.log('Generated ID token.');
}

getIdTokenFromMetadataServer();
```

To run this code sample, you must install the
[Google Auth Python Library](https://github.com/googleapis/google-auth-library-python).

```
import google
import google.oauth2.credentials
from google.auth import compute_engine
import google.auth.transport.requests

def idtoken_from_metadata_server(url: str):
    """
    Use the Google Cloud metadata server in the Cloud Run (or AppEngine or Kubernetes etc.,)
    environment to create an identity token and add it to the HTTP request as part of an
    Authorization header.

    Args:
        url: The url or target audience to obtain the ID token for.
            Examples: http://www.example.com
    """

    request = google.auth.transport.requests.Request()
    # Set the target audience.
    # Setting "use_metadata_identity_endpoint" to "True" will make the request use the default application
    # credentials. Optionally, you can also specify a specific service account to use by mentioning
    # the service_account_email.
    credentials = compute_engine.IDTokenCredentials(
        request=request, target_audience=url, use_metadata_identity_endpoint=True
    )

    # Get the ID token.
    # Once you've obtained the ID token, use it to make an authenticated call
    # to the target audience.
    credentials.refresh(request)
    # print(credentials.token)
    print("Generated ID token.")
```

To run this code sample, you must install the
[Google Auth Library for Ruby](https://github.com/googleapis/google-auth-library-ruby).

```
require "googleauth"

##
# Uses the Google Cloud metadata server environment to create an identity token
# and add it to the HTTP request as part of an Authorization header.
#
# @param url [String] The url or target audience to obtain the ID token for
#   (e.g. "http://www.example.com")
#
def auth_cloud_idtoken_metadata_server url:
  # Create the GCECredentials client.
  id_client = Google::Auth::GCECredentials.new target_audience: url

  # Get the ID token.
  # Once you've obtained the ID token, you can use it to make an authenticated call
  # to the target audience.
  id_client.fetch_access_token
  puts "Generated ID token."

  id_client.refresh!
end
```

### Use a connecting service to generate an ID token

Some Google Cloud services help you call other services. These connecting
services might help determine when the call gets made, or manage a workflow that
includes calling the service. The following services can automatically include
an ID token, with the appropriate value for the `aud` claim, when they initiate
a call to a service that requires an ID token:

  Cloud Scheduler
    Cloud Scheduler is a fully managed enterprise-grade cron job
    scheduler. You can configure Cloud Scheduler to include either an
    ID token or an access token when it invokes another service. For more
    information, see [Using authentication with HTTP Targets](https://cloud.google.com/scheduler/docs/http-target-auth).
   Cloud Tasks
    Cloud Tasks lets you manage the execution of distributed
    tasks. You can configure a task to include either an ID token or an access
    token when it calls a service. For more information, see
    [Using HTTP Target tasks with authentication tokens](https://cloud.google.com/tasks/docs/creating-http-target-tasks#token).
   Pub/Sub
    Pub/Sub enables asynchronous communication between services.
    You can configure Pub/Sub to include an ID token with a
    message. For more information, see
    [Authentication for push subscription](https://cloud.google.com/pubsub/docs/push#authentication).
   Workflows
    Workflows is a fully managed orchestration platform that
    executes services in an order that you define: a *workflow*. You can
    define a workflow to include either an ID token or an access token when it
    invokes another service. For more information, see
    [Make authenticated requests from a workflow](https://cloud.google.com/workflows/docs/authenticate-from-workflow).

### Generate an ID token by impersonating a service account

Service account impersonation allows a principal to generate short-lived
credentials for a trusted service account. The principal can then use these
credentials to authenticate as the service account.

Before a principal can impersonate a service account, it must have an
IAM role on that service account that enables impersonation.
If the principal is itself another service account, it might seem easier to
simply provide the required permissions directly to that service account, and
enable it to impersonate itself. This configuration, known as
self-impersonation, creates a security vulnerability, because it lets the
service account create an access token that can be refreshed in perpetuity.

Service account impersonation should always involve two
principals: a principal that represents the caller, and the service account that
is being impersonated, called the privilege-bearing service account.

To generate an ID token by impersonating a service account, you use the
following general process.

For step-by-step instructions, see
[Create an ID token](https://cloud.google.com/iam/docs/create-short-lived-credentials-direct#sa-credentials-oidc).

1. Identify or [create a service account](https://cloud.google.com/iam/docs/service-accounts-create#creating) to be the privilege-bearing
  service account.
2. Identify the required roles to invoke the target service. Grant these
        roles to the service account on the target service:
  - For [Cloud Run services](https://cloud.google.com/run/docs/authenticating/service-to-service#set-up-sa),
            grant the Cloud Run Invoker role (`roles/run.invoker`).
  - For
            [Cloud Run functions](https://cloud.google.com/functions/docs/securing/authenticating),
            grant the Cloud Functions Invoker role
            (`roles/cloudfunctions.invoker`).
  - For other target services, see the product documentation for the
            service.
3. Identify the principal that will perform the impersonation, and set up
  [Application Default Credentials (ADC)](https://cloud.google.com/docs/authentication/provide-credentials-adc) to use the credentials for
  this principal.
  For development environments, the principal is usually the user account you
  provided to ADC by using the gcloud CLI. However, if you're
  running on a resource with a service account attached, the attached service
  account is the principal.
4. Grant the principal the Service Account OpenID Connect Identity
    Token Creator role (`roles/iam.serviceAccountOpenIdTokenCreator`).
5. Use the [IAM Credentials API](https://cloud.google.com/iam/docs/reference/credentials/rest) to generate
  the ID token for the authorized service account.
  Replace the following:
  - AUDIENCE: The URI for the target service&mdashfor example,
    `http://www.example.com`.
  - SERVICE_ACCOUNT_EMAIL: The email address of the
    privilege-bearing service account.
  ```
  curl -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  -d '{"audience": "AUDIENCE", "includeEmail": "true"}' \
  https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/SERVICE_ACCOUNT_EMAIL:generateIdToken
  ```

### Generate a generic ID token for development with Cloud Run and Cloud Run functions

You can use the gcloud CLI to get an ID token for your user
credentials that can be used with any Cloud Run service or
Cloud Run function that the caller has the required IAM permissions to
invoke. This token will not work for any other application.

- To generate a generic ID token, you use the
  [gcloud auth print-identity-tokencommand](https://cloud.google.com/sdk/gcloud/reference/auth/print-identity-token):
  ```
  gcloud auth print-identity-token
  ```

## What's next

- Understand [ID tokens](https://cloud.google.com/docs/authentication/token-types#identity-tokens).
- Use shell commands to
  [query the Compute Engine metadata server](https://cloud.google.com/compute/docs/metadata/querying-metadata).
- Learn more about [authentication methods](https://cloud.google.com/docs/authentication).

   Was this helpful?

---

# Identity management products and featuresStay organized with collectionsSave and categorize content based on your preferences.

# Identity management products and featuresStay organized with collectionsSave and categorize content based on your preferences.

Google has various products and technologies that provide identity and
access management capabilities. This page lists some of these products, to help
you understand what these products offer and how they differ from one another.

If you need help with understanding a specific authentication use case, see
[Authentication and authorization use cases](https://cloud.google.com/docs/authentication/use-cases).

## Product list

- [Chrome Enterprise Premium](#bce)
- [Cloud Identity](#cloud-identity)
- [Firebase Authentication](#firebase)
- [Google Identity Services](#google-identity)
- [Google Workspace](#workspace)
- [Identity and Access Management (IAM)](#iam)
- [Identity-Aware Proxy (IAP)](#iap)
- [Identity Platform](#identity-platform)
- [Workforce Identity Federation](#wfif)
- [Workload Identity Federation for GKE](#wli)
- [Workload Identity Federation](#wlif)

### Chrome Enterprise Premium

[Chrome Enterprise Premium](https://cloud.google.com/beyondcorp-enterprise) is a zero-trust solution that lets
you provide secure access with integrated threat and data protection. You can
provide an organization's workforce access to web applications securely from
anywhere, without the need for a VPN. Chrome Enterprise Premium includes
[IAP](#iap), Endpoint Verification, and Chrome Enterprise.

For more information about Chrome Enterprise Premium, see the
[Chrome Enterprise Premium overview](https://cloud.google.com/chrome-enterprise-premium/docs/overview).

### Cloud Identity

[Cloud Identity](https://cloud.google.com/identity) is an Identity as a Service (IDaaS) solution that
centrally manages users and groups. It's built in to both Google Cloud
and [Google Workspace](#workspace). If you are not adopting
Google Workspace, Cloud Identity is available as a
standalone product.

For information about Cloud Identity, see
[Overview of Cloud Identity](https://cloud.google.com/identity/docs/overview).

Cloud Identity is not related to
[Identity Platform](#identity-platform).

### Firebase Authentication

[Firebase Authentication](https://firebase.google.com/docs/auth) is the authentication
solution provided by Firebase, a backend platform for building Web,
Android, and iOS applications. Firebase Authentication includes authentication support
for a wide array of user account types.

Firebase Authentication uses Identity Platform as its backend but serves a different audience:

- Firebase Authentication is aimed at consumer applications, and offers a subset of features
              compared to Identity Platform.
- Identity Platform is intended for building enterprise-focused SaaS applications.
              It lets you integrate with enterprise IdPs using inbound OIDC or SAML.

For more information about the differences between these products, see
        [Differences between Identity Platform and Firebase Authentication](https://cloud.google.com/identity-platform/docs/product-comparison).

For information about Firebase Authentication, see
[Where do I start with Firebase Authentication?](https://firebase.google.com/docs/auth/where-to-start)

For a comparison between end-user authentication options, see
[Authenticate application users](https://cloud.google.com/docs/authentication/use-cases#app-users).

### Google Identity Services

[Google Identity Services](https://developers.google.com/identity) is a suite of
identity products that support user authentication using Google Accounts,
for mobile apps and web platforms. Google Identity Services include the
[Sign In With Google](https://developers.google.com/identity/one-tap/android)
button, the One Tap sign-in module, and authentication libraries you can use to
implement OAuth 2.0 flows in your application.

If you're creating applications that use Google Cloud APIs and resources
exclusively, consider using [Identity Platform](#identity-platform),
which is based on Google Identity Services, instead.

For a comparison between end-user authentication options, see
[Authenticate application users](https://cloud.google.com/docs/authentication/use-cases#app-users).

### Google Workspace

[Google Workspace](https://workspace.google.com/) is a suite of business
productivity and collaboration tools based on Google identities (Google
Accounts). Google Workspace includes the functionality provided by
[Cloud Identity](#cloud-identity) for user management.
[Google Accounts](https://www.google.com/account/about/) provide access to
Google's products and services, including Google Cloud.

### Identity and Access Management (IAM)

[IAM](https://cloud.google.com/iam) provides fine-grained access control for
Google Cloud resources.

For information, see the [IAM overview](https://cloud.google.com/iam/docs/overview).

### Identity-Aware Proxy (IAP)

[Identity-Aware Proxy](https://cloud.google.com/iap) provides a centralized way to support authentication and
authorization for your applications and virtual machines (VMs).
IAP can be used for applications running in Google Cloud
or on-premises.

For information, see
[Identity-Aware Proxy overview](https://cloud.google.com/iap/docs/concepts-overview).

For a comparison between end-user authentication options, see
[Authenticate application users](https://cloud.google.com/docs/authentication/use-cases#app-users).

### Identity Platform

[Identity Platform](https://cloud.google.com/identity-platform) is a customer identity and
access management (CIAM) platform that lets users sign in to your applications
and services. Identity Platform supports a variety of ways to sign in,
including email and password, Google, Facebook, and Apple.
Identity Platform also supports SMS-based multi-factor authentication
(MFA).

For information about authentication using Identity Platform,
see [Authentication](https://cloud.google.com/identity-platform/docs/concepts-authentication).

Identity Platform is not related to
[Cloud Identity](#cloud-identity) or [Identity-Aware Proxy](#iap).

Firebase Authentication uses Identity Platform as its backend but serves a different audience:

- Firebase Authentication is aimed at consumer applications, and offers a subset of features
              compared to Identity Platform.
- Identity Platform is intended for building enterprise-focused SaaS applications.
              It lets you integrate with enterprise IdPs using inbound OIDC or SAML.

For more information about the differences between these products, see
        [Differences between Identity Platform and Firebase Authentication](https://cloud.google.com/identity-platform/docs/product-comparison).

For a comparison between end-user authentication options, see
[Authenticate application users](https://cloud.google.com/docs/authentication/use-cases#app-users).

### Workforce Identity Federation

[Workforce Identity Federation](https://cloud.google.com/iam/docs/workforce-identity-federation) is an
IAM feature that lets you configure and secure granular access
for your workforce—employees and partners—by federating identities
from an external identity provider (IdP).

Workforce Identity Federation is not the same as
[Workload Identity Federation](#wlif).
Workforce Identity Federation and Workload Identity Federation
both aggregate identities; Workforce Identity Federation aggregates human
users, whereas Workload Identity Federation aggregates machine workloads.

### Workload Identity Federation for GKE

[Workload Identity Federation for GKE](https://cloud.google.com/kubernetes-engine/docs/concepts/workload-identity)
lets a Kubernetes service account in your GKE
cluster act as an IAM service account. Workload Identity Federation for GKE
is the recommended way for your workloads running on GKE to
access Google Cloud services in a secure and manageable way.

Workload Identity Federation for GKE is not related to [Workload Identity Federation](#wlif).

### Workload Identity Federation

[Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation) lets
you grant on-premises or multicloud workloads access to Google Cloud
resources. It does so by federating identities from an external IdP, without
requiring a service account key.

Workload Identity Federation is not related to [Workload Identity Federation for GKE](#wli).

Workload Identity Federation is not the same as
[Workforce Identity Federation](#wfif). Workload Identity Federation and
Workforce Identity Federation both aggregate identities;
Workload Identity Federation aggregates machine workloads, while
Workforce Identity Federation aggregates human users.

## What's next

- Review a list of [authentication and authorization use cases](https://cloud.google.com/docs/authentication/use-cases).

   Was this helpful?

---

# Multi

# Multi-factor authentication requirement for Google CloudStay organized with collectionsSave and categorize content based on your preferences.

Google Cloud strives to provide its customers with the strongest security
possible. We prioritize protecting your identity, to help keep your account and
sensitive information safe. To help keep this commitment, Google is phasing in
the requirement that all Google Cloud customers enable
*multi-factor authentication* (MFA) for their accounts.

MFA, also known as *2-step verification* (2SV), is an important security
measure. In addition to your password, MFA requires another proof of identity,
known as an *authentication factor*, to successfully sign in to an account.
Requiring an additional factor makes it much harder for your account to be
compromised by hackers. Even if your password is stolen, hackers still need an
additional factor to be able to access your account.

If you're using a Google Account and have already [enabled MFA](#enable-google),
you don't need to take further action. You can check whether MFA is enabled for
your account by opening the **Security** tab of your
[Google Account settings page](https://myaccount.google.com/security). The
**2-Step Verification** setting is displayed in the
**How you sign in to Google** section.

If you're using a third-party identity provider (IdP) to manage single sign-on
(SSO) in to Google Cloud, you can use the MFA provided by that IdP to
comply with Google Cloud's MFA requirement.

If you have questions that aren't answered in this document, contact
[Cloud Customer Care](https://cloud.google.com/support-hub).

## Timelines for MFA enforcement

The timeline for MFA enforcement for Google Cloud depends on your account
type, as shown in the following table.

| Account type | Description | Enforcement start date |
| --- | --- | --- |
| Personal Google Accounts | User accounts you created for your own use, including Gmail
      accounts, that are used asprincipalsin Google Cloud. | On or after May 12, 2025 |
| Enterprise Cloud Identity accounts (not using SSO) | User accounts with usernames and passwords created and managed by your
      Google Workspace administrator in Cloud Identity. | During or after Q4 2025 |
| Enterprise accounts using federated authentication | User accounts created and managed by your Google Workspace
      administrator that use Google Workspace SSO,Cloud IdentitySSO, orWorkforce Identity Federation. | During or after Q1 2026 |
| Reseller accounts | User accounts created and managed in a Google Cloud reseller domain. End
      users of the reseller are not affected. | On or after April 28, 2025 |

If you don't have MFA enabled, the Google Cloud console displays reminders to
enable MFA at least 90 days before, and leading up to MFA enforcement. In
addition, an email is sent with an MFA requirement reminder at least 90 days
before MFA enforcement.

For resellers and their users, the Google Cloud console displays reminders to
enable MFA at least 60 days before, and leading up to MFA enforcement.
Similarly, an email reminder is sent at least 60 days before MFA enforcement.

When the requirement is enforced for your account, you must have MFA enabled to
sign in to the Google Cloud console or the Firebase console.

## Scope of MFA enforcement

When the Google Cloud MFA requirement is enforced for your account, if you
don't have MFA enabled, you won't be able to use the following Google Cloud
interfaces:

- The [Google Cloud console](https://cloud.google.com/cloud-console)
- The [Firebase console](https://console.firebase.google.com/)

Google Cloud MFA enforcement doesn't affect service accounts. Only user
accounts are affected. However, if you use your Google Account to impersonate a
service account, and MFA is enforced for your account, you must have MFA enabled
to sign in to the Google Cloud console.

Access to the following interfaces and services is **not** affected by the
Google Cloud MFA enforcement:

- Google Workspace, including Gmail, Google Drive, Google Sheets,
  and Google Slides. However, Google Workspace has a separate MFA
  requirement. Contact
  [your Google Workspace administrator](https://support.google.com/a/answer/6208960)
  for more information.
- YouTube.

Your applications and workloads running on Google Cloud, including
applications secured by Identity-Aware Proxy (IAP), aren't affected by MFA
enforcement. However, your developers won't be able to use the
Google Cloud console to manage those applications. In other words, your
control plane is affected by MFA enforcement, but not your data plane.

## Opt out of MFA enforcement

Gmail accounts used for Google Cloud can't be opted out of the MFA
requirement.

Exemptions for enterprise accounts and reseller accounts are available for
specific use cases where implementing MFA is not feasible. For more information,
contact [Cloud Customer Care](https://cloud.google.com/support-hub).

## Enable MFA for Google Accounts

You can enable MFA, also known as *2-step verification* (2SV), on the **Security** tab
  of your
  [Google Account settings page](https://myaccount.google.com/security). For
  step-by-step instructions, see
  [Turn on 2-Step Verification](https://support.google.com/accounts/answer/185839?sjid=8549799716107395240-NC).

If you don't see the **2-Step Verification** option for your account, your administrator might
  have disabled it. Contact [your administrator](https://support.google.com/a/answer/6208960) for assistance.

### Additional factors for Google Accounts

Personal Google Accounts and enterprise accounts that use Google as their
identity provider (IdP) can use any of the following additional factors with
Google Cloud:

- **Authenticator apps**: you can set up an authenticator application, such as
  [Google Authenticator](https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2),
  or [Authy](https://www.authy.com/), on your mobile or desktop device to act as
  your second factor.
- **Backup codes**: you can create backup codes and use them as your second
  factor. Backup codes must be stored securely, and can be used only once, so
  this method should be used only when you have no other method available. For
  more information, see
  [Sign in with backup codes](https://support.google.com/accounts/answer/1187538).
- **Google Prompts**: if you are signed into your Google Account on another
  device, you can receive a prompt on that device asking you whether it is you
  signing in. You can confirm that it's you in a browser, on a tablet, or your
  phone. For more information, see
  [Sign in with Google prompts](https://support.google.com/accounts/answer/7026266).
- **Physical security key**: you can touch a physical security key to provide
  your second factor. For more information, see
  [Use a security key for 2-Step Verification](https://support.google.com/accounts/answer/6103523).
- **SMS codes**: you can use a code sent to your phone number as a second
  factor. Before you can use SMS as a second factor, your phone number must be
  associated with your Google Account.

## Enable MFA for third-party identity providers

Refer to your third-party IdP's documentation to learn how to enable MFA.

## Recover account access if a factor is lost or stolen

See [Fix common issues with 2-Step verification](https://support.google.com/accounts/answer/185834)
for steps to recover your account.

   Was this helpful?

---

# Set up Application Default CredentialsStay organized with collectionsSave and categorize content based on your preferences.

> Discover how to set up Application Default Credentials for Cloud Client Libraries, Google API Client Libraries, and other environments.

# Set up Application Default CredentialsStay organized with collectionsSave and categorize content based on your preferences.

How you set up Application Default Credentials (ADC) for use by
Cloud Client Libraries, Google API Client Libraries, and the REST and RPC APIs depends
on the environment where your code is running.

For information about where ADC looks for credentials and in what order,
see [How Application Default Credentials works](https://cloud.google.com/docs/authentication/application-default-credentials).

If you are using API keys, then you don't need to set up
ADC. For more information, see [Use API keys to access APIs](https://cloud.google.com/docs/authentication/api-keys-use).

## Provide credentials to ADC

Select the environment where your code is running:

- [Local development environment](https://cloud.google.com/docs/authentication/set-up-adc-local-dev-environment)
- [Resource with an attached service account](https://cloud.google.com/docs/authentication/set-up-adc-attached-service-account)
- [Containerized environment](https://cloud.google.com/docs/authentication/set-up-adc-containerized-environment)
- [On-premises or another cloud provider](https://cloud.google.com/docs/authentication/set-up-adc-on-premises)
- [Cloud-based development environment](https://cloud.google.com/docs/authentication/set-up-adc-cloud-dev-environment)

## What's next

- Learn more about [how ADC finds credentials](https://cloud.google.com/docs/authentication/application-default-credentials).
- [Authenticate for using Cloud Client Libraries](https://cloud.google.com/docs/authentication/client-libraries).
- [Authenticate for using REST](https://cloud.google.com/docs/authentication/rest).
- Explore [authentication methods](https://cloud.google.com/docs/authentication).

   Was this helpful?

---

# ReauthenticationStay organized with collectionsSave and categorize content based on your preferences.

# ReauthenticationStay organized with collectionsSave and categorize content based on your preferences.

This page describes some scenarios when you might need to authenticate again,
even if you previously authenticated successfully.

## Google Workspace session configuration

If you are accessing Google Cloud by using a Google Workspace user
account, your Google Workspace administrator can configure the maximum
session length, and whether reauthentication is required when the session
expires. The credentials provided by local Application Default Credentials (ADC)
files also expire when the session expires. You must refresh them by running the
[gcloud auth application-default logincommand](https://cloud.google.com/sdk/gcloud/reference/auth/application-default/login)
again.

If you have questions about your Google Workspace session configuration,
contact your Google Workspace administrator. For information about
setting the Google Workspace session length, see
[Set session length for Google Cloud services](https://support.google.com/a/answer/9368756).

## Identity-Aware Proxy reauthentication

IAP can be configured to require reauthentication to protected
services and applications after a specific period of time. For more information,
see [IAP reauthentication](https://cloud.google.com/iap/docs/configuring-reauth).

## Refresh token expiration

Refresh tokens can expire due to session length, or for other reasons. When they
expire, you must authenticate again. For more information, see
[Refresh token expiration](https://developers.google.com/identity/protocols/oauth2#expiration) in the Google Identity documentation.

## Sensitive actions

The following Google Cloud actions are considered *sensitive actions*:

- Billing assignment changes
- IAM allow policy changes at the organization, folder, or
  project level

To ensure that these sensitive actions aren't initiated by bad actors using
credential theft, Google Cloud adds an extra layer of security by
requiring reauthentication.

Reauthentication for sensitive actions is in the process of rolling out across
Google Cloud accounts. The rollout is expected to be complete in 2026.

### When reauthentication is required

When you initiate a sensitive action, you are required to reenter your password
or complete multi-factor authentication (MFA) if all of the following conditions
are met:

- The action is initiated in the Google Cloud console.
- You have not reauthenticated in the last 15 minutes.
- Your user account is managed by Google.

User accounts managed by an external identity provider (IdP) and federated by
using Workforce Identity Federation are not required to reauthenticate.

## Disable reauthentication

Reauthenticating for sensitive actions is enabled by default. To apply for an
exception, [contact support](https://console.cloud.google.com/support) with your reason for the
exception.

   Was this helpful?
