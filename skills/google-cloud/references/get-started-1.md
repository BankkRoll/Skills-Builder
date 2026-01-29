# Set up API accessStay organized with collectionsSave and categorize content based on your preferences. and more

# Set up API accessStay organized with collectionsSave and categorize content based on your preferences.

# Set up API accessStay organized with collectionsSave and categorize content based on your preferences.

Google Cloud APIs help you programmatically access Google Cloud
services from the command line, through automated scripts, or in your own
applications.

For example, you might want to develop an application that helps administrators
analyze how their resources are utilized
across multiple cloud providers. To do this, you need to access log data from
your Google Cloud resources.

To set up API access, implement the following:

- [Google Cloud APIs: Access services programmatically](#apis)
- [Cloud Client Libraries: Access APIs with your preferred language](#libraries)
- [Set up authentication credentials](#authenticate)

## Before you begin

To make sure you can set up APIs and use tools, ask your administrators to
complete the following tasks:

- Create an account that you use to sign in and use Google Cloud
  products, including Google Cloud console and Google Cloud CLI.
- Create a project that serves as an access boundary for your
  Google Cloud resources.
- Enable billing on your project so you can pay for service and API usage.

For detailed instructions to complete setup steps, see [Google Cloud Setup guided flow](https://cloud.google.com/docs/enterprise/cloud-setup).

## Google Cloud APIs: Access services programmatically

Google Cloud APIs are programmatic interfaces to Google Cloud
services. You can use APIs to access computing, networking, storage, and other
services. For example, you might create a
resource utilization application that pulls log data from your
Google Cloud resources. To retrieve the required data, you use the
Cloud Logging API.

You can access Google Cloud APIs using REST calls or client libraries. We
recommend that you use client libraries, which are available for many popular
programming languages. You can also access Cloud APIs with the Google Cloud CLI
tools or Google Cloud console.

For steps to enable an API, see [Getting started](https://cloud.google.com/apis/docs/getting-started)
in the Cloud APIs documentation.

## Cloud Client Libraries: Access APIs with your preferred language

Cloud Client Libraries help you access Google Cloud APIs from a supported
language of your choice. Each library supports your preferred language
conventions and simplifies the code that you write in your application. The
client libraries can handle common API processes, including authentication,
error handling, retry, and payload validation. For example, if your preferred
development language is Java, you might use the Cloud Logging with Java
library.

To choose and install a library, see
[Cloud Client Libraries](https://cloud.google.com/apis/docs/cloud-client-libraries).

## Set up authentication credentials

Application Default Credentials (ADC) is a strategy used by the authentication
libraries to automatically find credentials based on the application
environment. The authentication libraries make those credentials available to
Cloud Client Libraries and Google API Client Libraries. When you use ADC, your code
can run in either a development or production environment without changing how
your application authenticates to Google Cloud services and APIs.

For setup steps, see [Set up Application Default
Credentials](https://cloud.google.com/docs/authentication/provide-credentials-adc).

## What's next?

- [Streamline your workflows with developer tools](https://cloud.google.com/docs/get-started/developer-tools)
- [Google Cloud samples](https://cloud.google.com/docs/samples)

   Was this helpful?

---

# Authorization and access controlStay organized with collectionsSave and categorize content based on your preferences.

> A beginner-friendly introduction to authorization and access control with IAM in Google Cloud.

# Authorization and access controlStay organized with collectionsSave and categorize content based on your preferences.

Identity and Access Management (IAM) is a tool that lets you control who can do what in
your Google Cloud environment.

Access is controlled with IAM permissions, which are required to
work with any resource in a Google Cloud environment. When you're given
the permissions to work with a resource, you are *authorized* to access that
resource. Without the proper authorization, you can't access Google Cloud
resources.

## Permissions and roles

To work with a resource, your user account must have the relevant
permissions to access that resource.

Typically, your IAM administrator is responsible for controlling
access to resources. Your administrator can give you permissions to access a
single resource or all the resources in a project, folder, or organization.
Administrators grant the relevant permissions to your user account in bundles
called *roles*. As long as your user account has a role with the appropriate
permissions, you can use that role to access Google Cloud resources.

Generally, the workflow to perform an action on any resource in your
Google Cloud environment looks like this:

1. You want to perform an action on a resource—for example, upload an
  object to a Cloud Storage bucket—but you don't have the appropriate
  permissions. Without the permissions, you can't perform the action.
2. You can request the permissions you need from your IAM
  administrator through your preferred request management system or directly
  from the permission error message in the Google Cloud console.
3. Your IAM administrator grants a role that contains the
  appropriate permissions to your user account. You can now
  perform the action.

## Using IAM as an administrator

Administrators are typically responsible for granting roles to users so they can
access Google Cloud resources. Users are represented by authenticated
identities known as *principals*.

Granting roles to a principal on a resource involves editing the *allow policy*
that's attached to the resource. Allow policies list which principals have
access to the resource and what actions they can perform on the resource.
IAM uses allow policies to determine whether a principal has the
required permissions to access the resource. Therefore, to grant a
principal access to a particular resource, you must update the allow
policy for the resource with the principal and the roles that you want to grant.

Administrators can grant roles to principals on the following types of resources:

- **Projects, folders, and organizations**: These resources are the container
  resources used to structure your [resource
  hierarchy](https://cloud.google.com/iam/docs/resource-hierarchy-access-control). Roles that you grant
  on these container resources apply to all of the service-specific resources
  they contain.
- **Service-specific resources**: These resources are the features or components
  offered by a service. For example, Compute Engine has resources like
  instances, disks, and subnetworks. Granting roles on a service-specific
  resource provides more granular access control than granting roles on a
  container resource, because it limits a user's access to just that resource.

## Advanced access control with IAM

Allow policies are the most common method for controlling access to a
Google Cloud environment with IAM. But
IAM also offers other, more advanced
options for access control, including the following:

- Additional policy types, like deny and principal access boundary
  policies
- Conditional attribute-based access controls
- Temporary access controls like Privileged Access Manager (PAM)

## Other forms of access control

Although IAM is the primary method of access control for
Google Cloud, there are other Google Cloud services that can affect
a user's access to resources.

The following are some examples of other services that can affect a user's
access:

- [Access Context Manager](https://cloud.google.com/access-context-manager/docs/overview):
      Access Context Manager lets you define fine-grained, attribute-based access
      control for projects and resources in Google Cloud.
- [Identity-Aware Proxy (IAP)](https://cloud.google.com/iap/docs/concepts-overview): IAP
      uses an application-level access control model where you establish a
      central authorization layer for applications accessed by HTTPS.
- [Organization Policy Service](https://cloud.google.com/resource-manager/docs/organization-policy/overview):
      Organization Policy lets you configure constraints across your resource
      hierarchy to give you centralized and programmatic control over your
      organization's cloud resources.
- [VPC Service Controls](https://cloud.google.com/vpc-service-controls/docs/overview):
      VPC Service Controls lets you define perimeters that help protect the
      Google Cloud resources and data of Google Cloud services that
      you explicitly specify.

## What's next

- For a more in-depth description of the IAM system and
  how it works, see the [IAM
  overview page](https://cloud.google.com/iam/docs/overview) in the IAM documentation.
- For information on IAM error messages, see
  [Troubleshoot permission error
  messages](https://cloud.google.com/iam/docs/permission-error-messages) in the IAM documentation.
