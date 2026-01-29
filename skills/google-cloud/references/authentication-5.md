# Authenticate for using RESTStay organized with collectionsSave and categorize content based on your preferences. and more

# Authenticate for using RESTStay organized with collectionsSave and categorize content based on your preferences.

# Authenticate for using RESTStay organized with collectionsSave and categorize content based on your preferences.

This page describes how to authenticate when you
make a REST request to a Google API.

For information about how to authenticate when you use Google client libraries,
see [Authenticate using client libraries](https://cloud.google.com/docs/authentication/client-libraries).

## Before you begin

To run the samples on this page, complete the following steps:

1. [Install](https://cloud.google.com/sdk/docs/install) the Google Cloud CLI.
2. If you're using an external identity provider (IdP), you must first
              [sign in to the gcloud CLI with your federated identity](https://cloud.google.com/iam/docs/workforce-log-in-gcloud).
3. To [initialize](https://cloud.google.com/sdk/docs/initializing) the gcloud CLI, run the following command:
  ```
  gcloud init
  ```
4. Enable the Cloud Resource Manager and Identity and Access Management (IAM) APIs:
  To enable APIs, you need the Service Usage Admin IAM
        role (`roles/serviceusage.serviceUsageAdmin`), which contains the
        `serviceusage.services.enable` permission. [Learn how to grant
        roles](https://cloud.google.com/iam/docs/granting-changing-revoking-access).
  ```
  gcloud services enable cloudresourcemanager.googleapis.com iam.googleapis.com
  ```

If you don't want to use the gcloud CLI, you can skip these steps
and use [service account impersonation](#impersonated-sa) or
[the metadata server](#metadata-server) to generate a token.

## Types of credentials

You can use the following types of credentials to authenticate a REST call:

- Your [gcloud CLI credentials](#user-creds).
  This approach is the easiest and most secure way to provide credentials to a
  REST method in a local development environment. If your user account has the
  necessary Identity and Access Management (IAM) permissions for the method you want to
  call, this is the preferred approach.
  Your gcloud credentials are not the same as the credentials you provide to ADC using the
  gcloud CLI. For more information, see
  [gcloud CLI authentication configuration and ADC configuration](https://cloud.google.com/docs/authentication/gcloud#gcloud-credentials).
- The [credentials provided to Application Default Credentials (ADC)](#rest-request).
  This method is the preferred option for authenticating a REST call in a
  production environment, because ADC finds credentials from the resource
  where your code is running (such as a Compute Engine virtual machine). You
  can also use ADC to authenticate in a local development environment. In this
  scenario, the gcloud CLI creates a file that contains your
  credentials in your local file system.
- The [credentials provided by impersonating a service account](#impersonated-sa).
  This method requires more setup. If you want to use your existing
  credentials to obtain short-lived credentials for another service account,
  such as testing with a service account locally or requesting temporary
  elevated privileges, use this approach.
- The [credentials returned by the metadata server](#metadata-server).
  This method works only in environments with access to a metadata server. The
  credentials returned by the metadata server are the same as the credentials
  that would be found by [Application Default Credentials](https://cloud.google.com/docs/authentication/application-default-credentials) using the
  attached service account, but you explicitly request the access token from
  the metadata server and then provide it with the REST request. Querying the
  metadata server for credentials requires an HTTP GET request; this method
  does not rely on the Google Cloud CLI.
- [API keys](#api-keys)
  You can use an API key with a REST request only for APIs that accepts API
  keys. In addition, the API key must not be restricted to prevent it from
  being used with the API.

### gcloud CLI credentials

To run the following example, you need the `resourcemanager.projects.get`
permission on the project. The `resourcemanager.projects.get` permission is
included in a variety of roles—for example, the
[Browser role](https://cloud.google.com/iam/docs/understanding-roles#project-roles) (`roles/browser`).

1. Use the
  [gcloud auth print-access-tokencommand](https://cloud.google.com/sdk/gcloud/reference/auth/print-access-token)
  to insert an access token generated from your user credentials.
  The following example gets details for the specified project. You can use the
  same pattern for any REST request.
  Before using any of the request data,
    make the following replacements:
  - `PROJECT_ID`: Your Google Cloud project ID or name.
  To send your request, choose one of these options:
  Execute the following command:
  ```
  curl -X GET \     -H "Authorization: Bearer $(gcloud auth print-access-token)" \     "https://cloudresourcemanager.googleapis.com/v3/projects/PROJECT_ID"
  ```
  Execute the following command:
  ```
  $cred = gcloud auth print-access-token$headers = @{ "Authorization" = "Bearer $cred" }Invoke-WebRequest `    -Method GET `    -Headers $headers `    -Uri "https://cloudresourcemanager.googleapis.com/v3/projects/PROJECT_ID" | Select-Object -Expand Content
  ```
  The details for your project are returned.

For APIs that require a quota project, you must set
one explicitly for the request. For more information, see
[Set the quota project with a REST request](#set-billing-project) on this page.

### Application Default Credentials

To run the following example, the principal associated with the credentials you
provide to ADC needs the `resourcemanager.projects.get` permission on the
project. The `resourcemanager.projects.get` permission is included in a variety
of roles—for example, the
[Browser role](https://cloud.google.com/iam/docs/understanding-roles#project-roles) (`roles/browser`).

1. [Provide credentials to ADC](https://cloud.google.com/docs/authentication/provide-credentials-adc).
  If you are running on a Google Cloud compute resource, you shouldn't
  provide your user credentials to ADC. Instead, use the attached service
  account to provide credentials. For more information, see
  [Set up ADC for a resource with an attached service account](https://cloud.google.com/docs/authentication/set-up-adc-attached-service-account).
2. Use the
  [gcloud auth application-default print-access-tokencommand](https://cloud.google.com/sdk/gcloud/reference/auth/application-default/print-access-token)
  to insert the access token returned by ADC into your REST request.
  The following example gets details for the specified project. You can use the
  same pattern for any REST request.
  Before using any of the request data,
    make the following replacements:
  - `PROJECT_ID`: Your Google Cloud project ID or name.
  To send your request, choose one of these options:
  Execute the following command:
  ```
  curl -X GET \     -H "Authorization: Bearer $(gcloud auth application-default print-access-token)" \     "https://cloudresourcemanager.googleapis.com/v3/projects/PROJECT_ID"
  ```
  Execute the following command:
  ```
  $cred = gcloud auth application-default print-access-token$headers = @{ "Authorization" = "Bearer $cred" }Invoke-WebRequest `    -Method GET `    -Headers $headers `    -Uri "https://cloudresourcemanager.googleapis.com/v3/projects/PROJECT_ID" | Select-Object -Expand Content
  ```
  The details for your project are returned.
  If your request returns an error message about end-user credentials not being supported by this
    API, see [Set the quota project with a REST request](#set-billing-project) on this
    page.

### Impersonated service account

The simplest way to impersonate a service account to generate an access token is by using
the gcloud CLI. However, if you need to generate the token
programmatically, or you don't want to use the gcloud CLI, you can
use impersonation to generate a short-lived token.

For more information about impersonating a service account, see
[Use service account impersonation](https://cloud.google.com/docs/authentication/use-service-account-impersonation).

1. Review the required permissions.
  - The prinicipal you want to use to perform the impersonation must have the `iam.serviceAccounts.getAccessToken`
    permission on the impersonated service account (also called the
    *privilege-bearing service account*). The
    `iam.serviceAccounts.getAccessToken` permission is included in the
    Service Account Token Creator role
    (`roles/iam.serviceAccountTokenCreator`). If you are using your user
    account, you need to add this permission even if you have the Owner role
    (`roles/owner`) on the project. For more information, see
    [Setting required permissions](https://cloud.google.com/iam/docs/create-short-lived-credentials-direct#sa-credentials-permissions).
2. Identify or create the privilege-bearing service account—the service account
  you will impersonate.
  The privilege-bearing service account must have the permissions required
  to make the API method call.

1. Use the
  [gcloud auth print-access-tokencommand](https://cloud.google.com/sdk/gcloud/reference/auth/print-access-token)
  with the
  [--impersonate-service-accountflag](https://cloud.google.com/sdk/gcloud/reference#--impersonate-service-account)
  to insert an access token for the privilege-bearing service account into
  your REST request.

The following example gets details for the specified project. You can use the
same pattern for any REST request.

To run this example, the service account you impersonate needs the
`resourcemanager.projects.get` permission. The `resourcemanager.projects.get`
permission is included in a variety of roles—for example, the
[Browser role](https://cloud.google.com/iam/docs/understanding-roles#project-roles) (`roles/browser`).

Make the following replacements:

- `PRIV_SA`: The email address of the privilege-bearing
  service account. For example, `my-sa@my-project.iam.gserviceaccount.com`.
- `PROJECT_ID`: Your Google Cloud project ID or name.

```
curl -X GET \
    -H "Authorization: Bearer $(gcloud auth print-access-token --impersonate-service-account=PRIV_SA)" \
    "https://cloudresourcemanager.googleapis.com/v3/projects/PROJECT_ID"
```

To generate a short-lived token by using service account impersonation,
follow the instructions provided in
[Create a short-lived access token](https://cloud.google.com/iam/docs/create-short-lived-credentials-direct#sa-credentials-oauth).

### Metadata server

To get an access token from the metadata server, you must make the REST call
using one of the services that has access to a metadata server:

- [Compute Engine](https://cloud.google.com/compute/docs/instances/verifying-instance-identity#request_signature)
- [App Engine standard environment](https://cloud.google.com/appengine/docs/standard/python3/runtime#metadata_server)
- [App Engine flexible environment](https://cloud.google.com/appengine/docs/flexible/python/runtime#metadata_server)
- [Cloud Run functions](https://cloud.google.com/functions/docs/securing/function-identity#metadata-server)
- [Cloud Run](https://cloud.google.com/run/docs/container-contract#metadata-server)
- [Google Kubernetes Engine](https://cloud.google.com/kubernetes-engine/docs/concepts/workload-identity#instance_metadata)
- [Cloud Build](https://cloud.google.com/build/docs/securing-builds/authorize-service-to-service-access)

You use a command-line tool such as `curl` to get an access token, and then
insert it into your REST request.

1. Query the metadata server for an access token:
  ```
  curl "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token" \
      -H "Metadata-Flavor: Google"
  ```
  The request returns a response similar to the following example:
  ```
  {
        "access_token":"ya29.AHES6ZRN3-HlhAPya30GnW_bHSb_QtAi85nHq39HE3C2LTrCARA",
        "expires_in":3599,
        "token_type":"Bearer"
   }
  ```
2. Insert the access token into your REST request, making the following
  replacements:
  - `ACCESS_TOKEN`: The access token returned in the
    previous step.
  - `PROJECT_ID`: Your Google Cloud project ID or name.
  ```
  curl -X GET \
      -H "Authorization: Bearer ACCESS_TOKEN" \
      "https://cloudresourcemanager.googleapis.com/v3/projects/PROJECT_ID"
  ```

### API keys

To include an API key with a REST API call, use the `x-goog-api-key` HTTP
header, as shown in the following example:

```
curl -X POST \
    -H "X-goog-api-key: API_KEY" \
    -H "Content-Type: application/json; charset=utf-8" \
    -d @request.json \
    "https://translation.googleapis.com/language/translate/v2"
```

If you can't use the HTTP header, you can use the `key` query parameter.
However, this method includes your API key in the URL, exposing your key to
theft through URL scans.

The following example shows how to use the `key` query parameter with a
Cloud Natural Language API request for
[documents.analyzeEntities](https://cloud.google.com/natural-language/docs/reference/rest/v1/documents/analyzeEntities).
Replace `API_KEY` with the key string of your API key.

```
POST https://language.googleapis.com/v1/documents:analyzeEntities?key=API_KEY
```

## Set the quota project with a REST request

To call some APIs with user credentials, you must also set the project that is
billed for your usage and used to track quota. If your API call returns an error
message saying that user credentials are not supported, or that the quota
project is not set, you must explicitly set the quota project for the request.
To set the quota project, include the `x-goog-user-project` header with your
request.

For more information about when you might encounter this issue, see
[User credentials not working](https://cloud.google.com/docs/authentication/troubleshoot-adc#user-creds-client-based).

You must have the `serviceusage.services.use` IAM permission for
a project to be able to designate it as your billing project. The
`serviceusage.services.use` permission is included in the Service Usage Consumer
IAM role. If you don't have the `serviceusage.services.use`
permission for any project, contact your security administrator or a project
owner who can give you the Service Usage Consumer role in the project.

The following example uses the Cloud Translation API to translate the word "hello" into Spanish. The Cloud Translation API is
an API that needs a quota project to be specified. To run the sample, create a
file named `request.json` with the request body content.

Before using any of the request data,
  make the following replacements:

- PROJECT_ID: The ID or name of the Google Cloud project to use as a billing project.

Request JSON body:

```
{
  "q": "hello",
  "source": "en",
  "target": "es"
}
```

To send your request, choose one of these options:

Save the request body in a file named `request.json`,
      and execute the following command:

```
curl -X POST \     -H "Authorization: Bearer $(gcloud auth print-access-token)" \     -H "x-goog-user-project: PROJECT_ID" \     -H "Content-Type: application/json; charset=utf-8" \     -d @request.json \     "https://translation.googleapis.com/language/translate/v2"
```

Save the request body in a file named `request.json`,
      and execute the following command:

```
$cred = gcloud auth print-access-token$headers = @{ "Authorization" = "Bearer $cred"; "x-goog-user-project" = "PROJECT_ID" }Invoke-WebRequest `    -Method POST `    -Headers $headers `    -ContentType: "application/json; charset=utf-8" `    -InFile request.json `    -Uri "https://translation.googleapis.com/language/translate/v2" | Select-Object -Expand Content
```

The translation request succeeds. You can try the command without the
  `x-goog-user-project` HTTP header to see what happens when you do not specify the
  billing project.

## What's next

- See an overview of [authentication](https://cloud.google.com/docs/authentication).
- Learn how to authenticate with [client libraries](https://cloud.google.com/docs/authentication/client-libraries).
- Understand [gcloud CLI authentication configuration and ADC configuration](https://cloud.google.com/docs/authentication/gcloud#gcloud-credentials).

---

# Set up ADC for a resource with an attached service accountStay organized with collectionsSave and categorize content based on your preferences.

> Discover how to set up Application Default Credentials for Cloud Client Libraries, Google API Client Libraries, and other environments.

# Set up ADC for a resource with an attached service accountStay organized with collectionsSave and categorize content based on your preferences.

Some Google Cloud services—such as Compute Engine, App Engine, and
Cloud Run functions—support attaching a
[user-managed service account](https://cloud.google.com/iam/docs/service-account-types#user-created) to some types of resources.
Generally, attaching a service account is supported when that service's
resources can run or include application code. When you attach a service account
to a resource, the code running on the resource can use that service account as
its identity.

Attaching a user-managed service account is the preferred way to provide
credentials to ADC for production code running on Google Cloud.

For help determining the roles that you need to provide to
your service account, see [Choose predefined roles](https://cloud.google.com/iam/docs/choose-predefined-roles).

For information about which resources you can attach a service account to, and
help with attaching the service account to the resource, see the
[IAM documentation on attaching a service account](https://cloud.google.com/iam/docs/attach-service-accounts#attaching-new-resource).

Set up authentication:

1. Ensure that you have the Create Service Accounts IAM role
      (`roles/iam.serviceAccountCreator`) and the Project IAM Admin role
      (`roles/resourcemanager.projectIamAdmin`). [Learn how to grant roles](https://cloud.google.com/iam/docs/granting-changing-revoking-access).
2. Create the service account:
  ```
  gcloud iam service-accounts create SERVICE_ACCOUNT_NAME
  ```
  Replace `SERVICE_ACCOUNT_NAME` with a name for the service account.
3. To provide access to your project and your resources, grant a role to the service account:
  ```
  gcloud projects add-iam-policy-binding PROJECT_ID --member="serviceAccount:SERVICE_ACCOUNT_NAME@PROJECT_ID.iam.gserviceaccount.com" --role=ROLE
  ```
  Replace the following:
  - `SERVICE_ACCOUNT_NAME`: the name of the service account
  - `PROJECT_ID`: the project ID where you created the service account
  - `ROLE`: the role to grant
4. To grant another role to the service account, run the command as you did in the previous step.
5. Grant the required role to the principal that
        will attach the service account to other resources.
  ```
  gcloud iam service-accounts add-iam-policy-binding SERVICE_ACCOUNT_NAME@PROJECT_ID.iam.gserviceaccount.com --member="user:USER_EMAIL" --role=roles/iam.serviceAccountUser
  ```
  Replace the following:
  - `SERVICE_ACCOUNT_NAME`: the name of the service account
  - `PROJECT_ID`: the project ID where you created the service account
  - `USER_EMAIL`: the email address for a Google Account

## What's next

- Understand best practices for using [service accounts](https://cloud.google.com/iam/docs/best-practices-service-accounts) and [service account keys](https://cloud.google.com/iam/docs/best-practices-for-managing-service-account-keys).
- Learn more about [how ADC finds credentials](https://cloud.google.com/docs/authentication/application-default-credentials).
- [Authenticate for using Cloud Client Libraries](https://cloud.google.com/docs/authentication/client-libraries).
- Explore [authentication methods](https://cloud.google.com/docs/authentication).

   Was this helpful?

---

# Set up ADC for a cloud

> Discover how to set up Application Default Credentials for Cloud Client Libraries, Google API Client Libraries, and other environments.

# Set up ADC for a cloud-based development environmentStay organized with collectionsSave and categorize content based on your preferences.

When you use a Google Cloud cloud-based development environment such as
  Cloud Shell or Cloud Code, the tool uses the credentials you provided
  when you signed in, and manages any authorizations required. You cannot use
  the gcloud CLI to configure ADC in these environments. If
  you need to use a different user account to configure ADC, or configure ADC
  using a service account, use a local development environment or a
  Google Cloud compute resource as your development environment.

## What's next

- Get more information about [Cloud Code](https://cloud.google.com/code/docs).
- Get more information about [Cloud Shell](https://cloud.google.com/shell/docs).
- Learn more about [how ADC finds credentials](https://cloud.google.com/docs/authentication/application-default-credentials).
- [Authenticate for using Cloud Client Libraries](https://cloud.google.com/docs/authentication/client-libraries).
- [Authenticate for using REST](https://cloud.google.com/docs/authentication/rest).
- Explore [authentication methods](https://cloud.google.com/docs/authentication).

   Was this helpful?

---

# Set up ADC for a containerized development environmentStay organized with collectionsSave and categorize content based on your preferences.

> Discover how to set up Application Default Credentials for Cloud Client Libraries, Google API Client Libraries, and other environments.

# Set up ADC for a containerized development environmentStay organized with collectionsSave and categorize content based on your preferences.

Authentication for containerized applications running on Cloud Run,
Google Kubernetes Engine, or GKE Enterprise is handled differently between local
testing environments and Google Cloud environments.

### Test containerized applications locally

To test your containerized application on your local workstation, you can
configure your container to authenticate with your
[local ADC file](https://cloud.google.com/docs/authentication/application-default-credentials#personal). For more information, see
[Configure ADC with your Google Account](https://cloud.google.com/docs/authentication/set-up-adc-local-dev-environment#google-idp).

To test your implementation, use a local Kubernetes implementation such as
[minikubeand thegcp-authaddon](https://minikube.sigs.k8s.io/docs/handbook/addons/gcp-auth/).

### Run containerized applications on Google Cloud

You set up authentication for Google Cloud containerized environments
differently depending on the environment:

- For Cloud Run, see
      [call Google Cloud APIs with the service identity](https://cloud.google.com/run/docs/securing/service-identity#call-apis-with-service-identity).
- For GKE, see
      [Access Google Cloud APIs from GKE workloads](https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity).
- For GKE Enterprise, see the
      [authentication overview](https://cloud.google.com/anthos/multicluster-management/gateway)
       and [Use fleet Workload Identity Federation for GKE](https://cloud.google.com/anthos/multicluster-management/fleets/workload-identity).
- For Knative serving, see
      [Using Workload Identity Federation for GKE for Knative serving](https://cloud.google.com/anthos/run/docs/securing/workload-identity).

## What's next

- Learn more about [how ADC finds credentials](https://cloud.google.com/docs/authentication/application-default-credentials).
- [Authenticate for using Cloud Client Libraries](https://cloud.google.com/docs/authentication/client-libraries).
- [Authenticate for using REST](https://cloud.google.com/docs/authentication/rest).
- Explore [authentication methods](https://cloud.google.com/docs/authentication).

   Was this helpful?

---

# Set up ADC for a local development environmentStay organized with collectionsSave and categorize content based on your preferences.

> Discover how to set up Application Default Credentials for Cloud Client Libraries, Google API Client Libraries, and other environments.

# Set up ADC for a local development environmentStay organized with collectionsSave and categorize content based on your preferences.

You can provide either [your user credentials](#local-user-cred) or
[service account credentials](#service-account) to ADC in a local development
environment.

## User credentials

When your code is running in a local development environment, such as a
development workstation, the best option is to use the credentials associated
with your [user account](https://cloud.google.com/docs/authentication#user-accounts).

How you configure ADC with your user account depends on whether your
[user account](https://cloud.google.com/docs/authentication#user-accounts) is managed by Google—in other words, it is a
Google Account—or by another identity provider (IdP), and federated by
using [Workforce Identity Federation](https://cloud.google.com/iam/docs/workforce-identity-federation).

To configure ADC with a Google Account, you use the Google Cloud CLI:

1. [Install](https://cloud.google.com/sdk/docs/install) the Google Cloud CLI.
  If you're using an external identity provider (IdP), you must first
          [sign in to the gcloud CLI with your federated identity](https://cloud.google.com/iam/docs/workforce-log-in-gcloud).
2. If you're using a local shell, then create local authentication credentials for your user
          account:
  ```
  gcloud auth application-default login
  ```
  You don't need to do this if you're using Cloud Shell.
  If an authentication error is returned, and you are using an external identity provider
          (IdP), confirm that you have
          [signed in to the gcloud CLI with your federated identity](https://cloud.google.com/iam/docs/workforce-log-in-gcloud).
  A sign-in screen appears. After you sign in, your credentials are stored in the
        [local credential file used by ADC](https://cloud.google.com/docs/authentication/application-default-credentials#personal).

To configure ADC for a user account managed by an external IdP and federated
with [Workforce Identity Federation](https://cloud.google.com/iam/docs/workforce-identity-federation):

1. [Install](https://cloud.google.com/sdk/docs/install) the Google Cloud CLI.
            After installation,
            [initialize](https://cloud.google.com/sdk/docs/initializing) the Google Cloud CLI by running the following command:
  ```
  gcloud init
  ```
  If you're using an external identity provider (IdP), you must first
          [sign in to the gcloud CLI with your federated identity](https://cloud.google.com/iam/docs/workforce-log-in-gcloud).
2. If you're using a local shell, then create local authentication credentials for your user
          account:
  ```
  gcloud auth application-default login
  ```
  You don't need to do this if you're using Cloud Shell.
  If an authentication error is returned, and you are using an external identity provider
          (IdP), confirm that you have
          [signed in to the gcloud CLI with your federated identity](https://cloud.google.com/iam/docs/workforce-log-in-gcloud).
  A sign-in screen appears. After you sign in, your credentials are stored in the
        [local credential file used by ADC](https://cloud.google.com/docs/authentication/application-default-credentials#personal).

### Tips for configuring ADC with your user credentials

When you configure ADC with your user account, you should be aware of the
following facts:

- ADC configured with a user account might not work for some APIs without extra
  configuration steps. If you see an error message about the API not being
  enabled in the project, or that there is no quota project available, see
  [User credentials not working](https://cloud.google.com/docs/authentication/troubleshoot-adc#user-creds-client-based).
- The local ADC file contains your refresh token. Any user with access to your
  file system can use it to get a valid access token. If you no longer need
  these local credentials, you can revoke them by using the
  [gcloud auth application-default revokecommand](https://cloud.google.com/sdk/gcloud/reference/auth/application-default/revoke).
- Your local ADC file is associated with your user account, not your
  gcloud CLI configuration. Changing to a different
  gcloud CLI configuration might change the identity used by the
  gcloud CLI, but it does not affect your local ADC file or the ADC
  configuration.

## Service account credentials

You can configure ADC with credentials from a
[service account](https://cloud.google.com/docs/authentication#service-accounts) by using service account impersonation or by
using a service account key.

### Service account impersonation

You can use service account impersonation to set up a local Application Default
  Credentials (ADC) file. Client libraries that support impersonation
  can use those credentials automatically. Local ADC files created by using
  impersonation are supported in the following languages:

- C#
- C++
- Go
- Java
- Node.js
- PHP
- Python
- Ruby
- Rust

You must have the Service Account Token Creator
    (`roles/iam.serviceAccountTokenCreator`) IAM role on the service account you are
    impersonating. For more information, see
    [Required roles](https://cloud.google.com/docs/authentication/use-service-account-impersonation#required-roles).

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

### Service account keys

If you cannot use a user account or service account impersonation for local
development, you can use a service account key.

To create a service account key and make it available to ADC:

1. Create a service account with the roles your application needs, and a key
      for that service account, by following the instructions in
      [Creating a service account key](https://cloud.google.com/iam/docs/keys-create-delete#creating).
2. Set the environment variable `GOOGLE_APPLICATION_CREDENTIALS`
      to the path of the JSON file that contains your credentials.
      This variable applies only to your current shell session, so if you open
      a new session, set the variable again.
  ```
  KEY_PATH
  ```
  Replace `KEY_PATH` with the path of the JSON file that contains your credentials.
  For example:
  ```
  export GOOGLE_APPLICATION_CREDENTIALS="/home/user/Downloads/service-account-file.json"
  ```
  For PowerShell:
  ```
  KEY_PATH
  ```
  Replace `KEY_PATH` with the path of the JSON file that contains your credentials.
  For example:
  ```
  $env:GOOGLE_APPLICATION_CREDENTIALS="C:\Users\username\Downloads\service-account-file.json"
  ```
  For command prompt:
  ```
  KEY_PATH
  ```
  Replace `KEY_PATH` with the path of the JSON file that contains your credentials.

## What's next

- Understand best practices for using [service account keys](https://cloud.google.com/iam/docs/best-practices-for-managing-service-account-keys).
- Learn more about [how ADC finds credentials](https://cloud.google.com/docs/authentication/application-default-credentials).
- [Authenticate for using Cloud Client Libraries](https://cloud.google.com/docs/authentication/client-libraries).
- [Authenticate for using REST](https://cloud.google.com/docs/authentication/rest).
- Explore [authentication methods](https://cloud.google.com/docs/authentication).

---

# Set up ADC for on

> Discover how to set up Application Default Credentials for Cloud Client Libraries, Google API Client Libraries, and other environments.

# Set up ADC for on-premises or another cloud providerStay organized with collectionsSave and categorize content based on your preferences.

If you are running your application outside of Google Cloud, you need to
provide credentials that are recognized by Google Cloud to
use Google Cloud services.

### Workload Identity Federation

The preferred way to authenticate with Google Cloud using credentials from
an external IdP is to use [Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation);
you create a credential configuration file and set the
`GOOGLE_APPLICATION_CREDENTIALS` environment variable to point to it. This
approach is more secure than creating a service account key.

For help with setting up Workload Identity Federation for ADC, see
[Workload Identity Federation with other clouds](https://cloud.google.com/iam/docs/workload-identity-federation-with-other-clouds).

### Service account key

If you are not able to configure Workload Identity Federation, then you must
create a service account, grant it the IAM roles that
your application requires, and create a key for the service account.

To create a service account key and make it available to ADC:

1. Create a service account with the roles your application needs, and a key
      for that service account, by following the instructions in
      [Creating a service account key](https://cloud.google.com/iam/docs/keys-create-delete#creating).
2. Set the environment variable `GOOGLE_APPLICATION_CREDENTIALS`
      to the path of the JSON file that contains your credentials.
      This variable applies only to your current shell session, so if you open
      a new session, set the variable again.
  ```
  KEY_PATH
  ```
  Replace `KEY_PATH` with the path of the JSON file that contains your credentials.
  For example:
  ```
  export GOOGLE_APPLICATION_CREDENTIALS="/home/user/Downloads/service-account-file.json"
  ```
  For PowerShell:
  ```
  KEY_PATH
  ```
  Replace `KEY_PATH` with the path of the JSON file that contains your credentials.
  For example:
  ```
  $env:GOOGLE_APPLICATION_CREDENTIALS="C:\Users\username\Downloads\service-account-file.json"
  ```
  For command prompt:
  ```
  KEY_PATH
  ```
  Replace `KEY_PATH` with the path of the JSON file that contains your credentials.

## What's next

- Learn about [Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation).
- Understand best practices for using [service account keys](https://cloud.google.com/iam/docs/best-practices-for-managing-service-account-keys).
- Learn more about [how ADC finds credentials](https://cloud.google.com/docs/authentication/application-default-credentials).
- Explore [authentication methods](https://cloud.google.com/docs/authentication).

   Was this helpful?
