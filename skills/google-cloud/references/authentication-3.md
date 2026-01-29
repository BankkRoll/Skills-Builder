# How Application Default Credentials worksStay organized with collectionsSave and categorize content based on your preferences. and more

# How Application Default Credentials worksStay organized with collectionsSave and categorize content based on your preferences.

# How Application Default Credentials worksStay organized with collectionsSave and categorize content based on your preferences.

This page describes the locations where Application Default Credentials (ADC)
looks for credentials. Understanding how ADC works can help you understand which
credentials ADC is using, and how it's finding them.

Application Default Credentials (ADC) is a strategy used by the authentication libraries
to automatically find credentials based on the application environment. The authentication libraries
make those credentials available to
[Cloud Client Libraries and Google API Client Libraries](https://cloud.google.com/apis/docs/client-libraries-explained).
When you use ADC, your code can run in either a development or production environment without
changing how your application authenticates to Google Cloud services and APIs.

For information about how to provide credentials to ADC, including how to
generate a local ADC file, see
[Set up Application Default Credentials](https://cloud.google.com/docs/authentication/provide-credentials-adc).

## Search order

ADC searches for credentials in the following locations:

1. [GOOGLE_APPLICATION_CREDENTIALSenvironment variable](#GAC)
2. [A credential file created by using thegcloud auth application-default logincommand](#personal)
3. [The attached service account, returned by the metadata server](#attached-sa)

The order of the locations ADC checks for credentials is not related to
the relative merit of each location. For help with
understanding the best ways to provide credentials to ADC, see
[Set up Application Default Credentials](https://cloud.google.com/docs/authentication/provide-credentials-adc).

### GOOGLE_APPLICATION_CREDENTIALS environment variable

You can use the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to provide
the location of a credential JSON file. This JSON file can be one of the
following types of files:

- A credential configuration file for Workforce Identity Federation
  Workforce Identity Federation lets you use an external identity provider
  (IdP) to authenticate and authorize users to access Google Cloud
  resources. For more information, see
  [Workforce Identity Federation](https://cloud.google.com/iam/docs/workforce-identity-federation) in the
  Identity and Access Management (IAM) documentation.
- A credential configuration file for Workload Identity Federation
  Workload Identity Federation lets you use an external
  IdP to authenticate and authorize workloads to access
  Google Cloud resources. For more information, see
  [Authenticating by using client libraries, the gcloud CLI, or Terraform](https://cloud.google.com/iam/docs/using-workload-identity-federation#generate-automatic)
  in the Identity and Access Management (IAM) documentation.
- A service account key
  Service account keys create a security risk and are not recommended. Unlike
  the other credential file types, compromised service account keys can be
  used by a bad actor without any additional information. For more
  information, see
  [Best practices for using and managing service account keys](https://cloud.google.com/iam/docs/best-practices-for-managing-service-account-keys).

### A credential file created by using thegcloud auth application-default logincommand

You can [provide credentials to ADC](https://cloud.google.com/docs/authentication/set-up-adc-local-dev-environment) by running the
[gcloud auth application-default login](https://cloud.google.com/sdk/gcloud/reference/auth/application-default/login) command. This
command creates a JSON file containing the credentials you provide (either from
your user account or from impersonating a service account) and places it in a
well-known location on your file system. The location depends on your
operating system:

- Linux, macOS: `$HOME/.config/gcloud/application_default_credentials.json`
- Windows: `%APPDATA%\gcloud\application_default_credentials.json`

The credentials you provide to ADC by using the gcloud CLI are
distinct from your gcloud credentials—the credentials the
gcloud CLI uses to authenticate to Google Cloud. For more
information about these two sets of credentials, see
[gcloud CLI authentication configuration and ADC configuration](https://cloud.google.com/docs/authentication/gcloud#gcloud-credentials).

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

### The attached service account

Many Google Cloud services let you attach a service account that can be
used to provide credentials for accessing Google Cloud APIs. If ADC does
not find credentials it can use in either the `GOOGLE_APPLICATION_CREDENTIALS`
environment variable or the well-known location for local ADC credentials,
it uses the [metadata server](https://cloud.google.com/compute/docs/metadata/overview) to get credentials for the
service where the code is running.

Using the credentials from the attached service account is the preferred method
for finding credentials in a production environment on Google Cloud. To
use the attached service account, follow these steps:

1. Create a user-managed service account.
2. Grant that service account the [least privileged](https://cloud.google.com/iam/docs/using-iam-securely#least_privilege)
  IAM roles possible.
3. Attach the service account to the resource where your code is running.

For help with creating a service account, see
[Creating and managing service accounts](https://cloud.google.com/iam/docs/service-accounts-create). For help with attaching
a service account, see [Attaching a service account to a resource](https://cloud.google.com/iam/docs/attach-service-accounts#attaching-to-resources).
For help with determining the required IAM roles for your service
account, see [Choose predefined roles](https://cloud.google.com/iam/docs/choose-predefined-roles).

## What's next

- Learn the best ways to [provide credentials to ADC](https://cloud.google.com/docs/authentication/provide-credentials-adc).
- [Authenticate using the Cloud Client Libraries](https://cloud.google.com/docs/authentication/client-libraries).
- Explore [authentication methods](https://cloud.google.com/docs/authentication).
- Learn about [client libraries](https://cloud.google.com/apis/docs/client-libraries-explained).

---

# Authenticate for using client librariesStay organized with collectionsSave and categorize content based on your preferences.

# Authenticate for using client librariesStay organized with collectionsSave and categorize content based on your preferences.

This page describes how you can use client libraries to access Google APIs.

Client libraries make it easier to access [Google Cloud APIs](https://cloud.google.com/apis/docs/overview)
using a supported language. You can use Google Cloud APIs directly by
making raw requests to the server, but client libraries provide simplifications
that significantly reduce the amount of code you need to write. This is
especially true for authentication, because the client libraries support
[Application Default Credentials (ADC)](https://cloud.google.com/docs/authentication/application-default-credentials).

If you accept credential configurations (JSON, files, or streams) from an
external source (for example, a customer), review the
[security requirements when using credential configurations from an external source](#external-credentials).

## Use Application Default Credentials with client libraries

To use Application Default Credentials to authenticate your application, you
 must first [set up ADC](https://cloud.google.com/docs/authentication/provide-credentials-adc) for the
 environment where your application is running. When you use the client
 library to create a client, the client library automatically checks for and
 uses the credentials you have provided to ADC to authenticate to the APIs
 your code uses. Your application does not need to explicitly authenticate
 or manage tokens; these requirements are managed automatically by the
 authentication libraries.

For a local development environment, you can set up ADC
[with your user credentials](https://cloud.google.com/docs/authentication/set-up-adc-local-dev-environment) or
[with service account impersonation](https://cloud.google.com/docs/authentication/use-service-account-impersonation#adc)
by using the gcloud CLI. For production environments,
you set up ADC by [attaching a service account](https://cloud.google.com/docs/authentication/set-up-adc-attached-service-account).

### Example client creation

The following code samples create a client for the Cloud Storage service.
Your code is likely to need different clients; these samples are meant only to
show how you can create a client and use it without any code to explicitly
authenticate.

Before you can run the following samples, you must complete the following steps:

- [Set up ADC for your environment](https://cloud.google.com/docs/authentication/provide-credentials-adc)
- [Install the Cloud Storage client library](https://cloud.google.com/storage/docs/reference/libraries)

```
import (
	"context"
	"fmt"
	"io"

	"cloud.google.com/go/storage"
	"google.golang.org/api/iterator"
)

// authenticateImplicitWithAdc uses Application Default Credentials
// to automatically find credentials and authenticate.
func authenticateImplicitWithAdc(w io.Writer, projectId string) error {
	// projectId := "your_project_id"

	ctx := context.Background()

	// NOTE: Replace the client created below with the client required for your application.
	// Note that the credentials are not specified when constructing the client.
	// The client library finds your credentials using ADC.
	client, err := storage.NewClient(ctx)
	if err != nil {
		return fmt.Errorf("NewClient: %w", err)
	}
	defer client.Close()

	it := client.Buckets(ctx, projectId)
	for {
		bucketAttrs, err := it.Next()
		if err == iterator.Done {
			break
		}
		if err != nil {
			return err
		}
		fmt.Fprintf(w, "Bucket: %v\n", bucketAttrs.Name)
	}

	fmt.Fprintf(w, "Listed all storage buckets.\n")

	return nil
}
```

```
import com.google.api.gax.paging.Page;
import com.google.cloud.storage.Bucket;
import com.google.cloud.storage.Storage;
import com.google.cloud.storage.StorageOptions;
import java.io.IOException;

public class AuthenticateImplicitWithAdc {

  public static void main(String[] args) throws IOException {
    // TODO(Developer):
    //  1. Before running this sample,
    //  set up Application Default Credentials as described in
    //  https://cloud.google.com/docs/authentication/external/set-up-adc
    //  2. Replace the project variable below.
    //  3. Make sure you have the necessary permission to list storage buckets
    //  "storage.buckets.list"
    String projectId = "your-google-cloud-project-id";
    authenticateImplicitWithAdc(projectId);
  }

  // When interacting with Google Cloud Client libraries, the library can auto-detect the
  // credentials to use.
  public static void authenticateImplicitWithAdc(String project) throws IOException {

    // *NOTE*: Replace the client created below with the client required for your application.
    // Note that the credentials are not specified when constructing the client.
    // Hence, the client library will look for credentials using ADC.
    //
    // Initialize client that will be used to send requests. This client only needs to be created
    // once, and can be reused for multiple requests.
    Storage storage = StorageOptions.newBuilder().setProjectId(project).build().getService();

    System.out.println("Buckets:");
    Page<Bucket> buckets = storage.list();
    for (Bucket bucket : buckets.iterateAll()) {
      System.out.println(bucket.toString());
    }
    System.out.println("Listed all storage buckets.");
  }
}
```

```
/**
 * TODO(developer):
 *  1. Uncomment and replace these variables before running the sample.
 *  2. Set up ADC as described in https://cloud.google.com/docs/authentication/external/set-up-adc
 *  3. Make sure you have the necessary permission to list storage buckets "storage.buckets.list"
 *    (https://cloud.google.com/storage/docs/access-control/iam-permissions#bucket_permissions)
 */
// const projectId = 'YOUR_PROJECT_ID';

const {Storage} = require('@google-cloud/storage');

async function authenticateImplicitWithAdc() {
  // This snippet demonstrates how to list buckets.
  // NOTE: Replace the client created below with the client required for your application.
  // Note that the credentials are not specified when constructing the client.
  // The client library finds your credentials using ADC.
  const storage = new Storage({
    projectId,
  });
  const [buckets] = await storage.getBuckets();
  console.log('Buckets:');

  for (const bucket of buckets) {
    console.log(`- ${bucket.name}`);
  }

  console.log('Listed all storage buckets.');
}

authenticateImplicitWithAdc();
```

```
// Imports the Cloud Storage client library.
use Google\Cloud\Storage\StorageClient;

/**
 * Authenticate to a cloud client library using a service account implicitly.
 *
 * @param string $projectId The Google project ID.
 */
function auth_cloud_implicit($projectId)
{
    $config = [
        'projectId' => $projectId,
    ];

    # If you don't specify credentials when constructing the client, the
    # client library will look for credentials in the environment.
    $storage = new StorageClient($config);

    # Make an authenticated API request (listing storage buckets)
    foreach ($storage->buckets() as $bucket) {
        printf('Bucket: %s' . PHP_EOL, $bucket->name());
    }
}
```

```
from google.cloud import storage

def authenticate_implicit_with_adc(project_id="your-google-cloud-project-id"):
    """
    When interacting with Google Cloud Client libraries, the library can auto-detect the
    credentials to use.

    // TODO(Developer):
    //  1. Before running this sample,
    //  set up ADC as described in https://cloud.google.com/docs/authentication/external/set-up-adc
    //  2. Replace the project variable.
    //  3. Make sure that the user account or service account that you are using
    //  has the required permissions. For this sample, you must have "storage.buckets.list".
    Args:
        project_id: The project id of your Google Cloud project.
    """

    # This snippet demonstrates how to list buckets.
    # *NOTE*: Replace the client created below with the client required for your application.
    # Note that the credentials are not specified when constructing the client.
    # Hence, the client library will look for credentials using ADC.
    storage_client = storage.Client(project=project_id)
    buckets = storage_client.list_buckets()
    print("Buckets:")
    for bucket in buckets:
        print(bucket.name)
    print("Listed all storage buckets.")
```

```
def authenticate_implicit_with_adc project_id:
  # The ID of your Google Cloud project
  # project_id = "your-google-cloud-project-id"

  ###
  # When interacting with Google Cloud Client libraries, the library can auto-detect the
  # credentials to use.
  # TODO(Developer):
  #   1. Before running this sample,
  #      set up ADC as described in https://cloud.google.com/docs/authentication/external/set-up-adc
  #   2. Replace the project variable.
  #   3. Make sure that the user account or service account that you are using
  #      has the required permissions. For this sample, you must have "storage.buckets.list".
  ###

  require "google/cloud/storage"

  # This sample demonstrates how to list buckets.
  # *NOTE*: Replace the client created below with the client required for your application.
  # Note that the credentials are not specified when constructing the client.
  # Hence, the client library will look for credentials using ADC.
  storage = Google::Cloud::Storage.new project_id: project_id
  buckets = storage.buckets
  puts "Buckets: "
  buckets.each do |bucket|
    puts bucket.name
  end
  puts "Plaintext: Listed all storage buckets."
end
```

## Use API keys with client libraries

You can use an API keys only with client libraries for APIs that accept API
keys. In addition, the API key must not have an API restriction that prevents it
from being used for the API.

For more information about API keys created in express mode, see the
[Google Cloud express mode FAQ](https://cloud.google.com/resources/cloud-express-faqs).

This example uses the Cloud Natural Language API, which accepts API keys,
  to demonstrate how you would provide an API key to the library.

To run this sample, you must install the
[Natural Language client library](https://cloud.google.com/dotnet/docs/reference/Google.Cloud.Language.V2/latest).

```
using Google.Cloud.Language.V1;
using System;

public class UseApiKeySample
{
    public void AnalyzeSentiment(string apiKey)
    {
        LanguageServiceClient client = new LanguageServiceClientBuilder
        {
            ApiKey = apiKey
        }.Build();

        string text = "Hello, world!";

        AnalyzeSentimentResponse response = client.AnalyzeSentiment(Document.FromPlainText(text));
        Console.WriteLine($"Text: {text}");
        Sentiment sentiment = response.DocumentSentiment;
        Console.WriteLine($"Sentiment: {sentiment.Score}, {sentiment.Magnitude}");
        Console.WriteLine("Successfully authenticated using the API key");
    }
}
```

To run this sample, you must install the
[Natural Language client library](https://cloud.google.com/cpp/docs/reference/language/latest).

```
#include "google/cloud/language/v1/language_client.h"
#include "google/cloud/credentials.h"
#include "google/cloud/options.h"

void AuthenticateWithApiKey(std::vector<std::string> const& argv) {
  if (argv.size() != 2) {
    throw google::cloud::testing_util::Usage{
        "authenticate-with-api-key <project-id> <api-key>"};
  }
  namespace gc = ::google::cloud;
  auto options = gc::Options{}.set<gc::UnifiedCredentialsOption>(
      gc::MakeApiKeyCredentials(argv[1]));
  auto client = gc::language_v1::LanguageServiceClient(
      gc::language_v1::MakeLanguageServiceConnection(options));

  auto constexpr kText = "Hello, world!";

  google::cloud::language::v1::Document d;
  d.set_content(kText);
  d.set_type(google::cloud::language::v1::Document::PLAIN_TEXT);

  auto response = client.AnalyzeSentiment(d, {});
  if (!response) throw std::move(response.status());
  auto const& sentiment = response->document_sentiment();
  std::cout << "Text: " << kText << "\n";
  std::cout << "Sentiment: " << sentiment.score() << ", "
            << sentiment.magnitude() << "\n";
  std::cout << "Successfully authenticated using the API key\n";
}
```

To run this sample, you must install the
[Natural Language client library](https://cloud.google.com/go/docs/reference/cloud.google.com/go/language/latest).

```
import (
	"context"
	"fmt"
	"io"

	language "cloud.google.com/go/language/apiv1"
	"cloud.google.com/go/language/apiv1/languagepb"
	"google.golang.org/api/option"
)

// authenticateWithAPIKey authenticates with an API key for Google Language
// service.
func authenticateWithAPIKey(w io.Writer, apiKey string) error {
	// apiKey := "api-key-string"

	ctx := context.Background()

	// Initialize the Language Service client and set the API key.
	client, err := language.NewClient(ctx, option.WithAPIKey(apiKey))
	if err != nil {
		return fmt.Errorf("NewClient: %w", err)
	}
	defer client.Close()

	text := "Hello, world!"
	// Make a request to analyze the sentiment of the text.
	res, err := client.AnalyzeSentiment(ctx, &languagepb.AnalyzeSentimentRequest{
		Document: &languagepb.Document{
			Source: &languagepb.Document_Content{
				Content: text,
			},
			Type: languagepb.Document_PLAIN_TEXT,
		},
	})
	if err != nil {
		return fmt.Errorf("AnalyzeSentiment: %w", err)
	}

	fmt.Fprintf(w, "Text: %s\n", text)
	fmt.Fprintf(w, "Sentiment score: %v\n", res.DocumentSentiment.Score)
	fmt.Fprintln(w, "Successfully authenticated using the API key.")

	return nil
}
```

To run this sample, you must install the
[Natural Language client library](https://cloud.google.com/nodejs/docs/reference/language/latest).

```
const {
  v1: {LanguageServiceClient},
} = require('@google-cloud/language');

/**
 * Authenticates with an API key for Google Language service.
 *
 * @param {string} apiKey An API Key to use
 */
async function authenticateWithAPIKey(apiKey) {
  const language = new LanguageServiceClient({apiKey});

  // Alternatively:
  // const {GoogleAuth} = require('google-auth-library');
  // const auth = new GoogleAuth({apiKey});
  // const language = new LanguageServiceClient({auth});

  const text = 'Hello, world!';

  const [response] = await language.analyzeSentiment({
    document: {
      content: text,
      type: 'PLAIN_TEXT',
    },
  });

  console.log(`Text: ${text}`);
  console.log(
    `Sentiment: ${response.documentSentiment.score}, ${response.documentSentiment.magnitude}`,
  );
  console.log('Successfully authenticated using the API key');
}

authenticateWithAPIKey();
```

To run this sample, you must install the
[Natural Language client library](https://cloud.google.com/python/docs/reference/language/latest).

```
from google.cloud import language_v1

def authenticate_with_api_key(api_key_string: str) -> None:
    """
    Authenticates with an API key for Google Language service.

    TODO(Developer): Replace this variable before running the sample.

    Args:
        api_key_string: The API key to authenticate to the service.
    """

    # Initialize the Language Service client and set the API key
    client = language_v1.LanguageServiceClient(
        client_options={"api_key": api_key_string}
    )

    text = "Hello, world!"
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Make a request to analyze the sentiment of the text.
    sentiment = client.analyze_sentiment(
        request={"document": document}
    ).document_sentiment

    print(f"Text: {text}")
    print(f"Sentiment: {sentiment.score}, {sentiment.magnitude}")
    print("Successfully authenticated using the API key")
```

To run this sample, you must install the
[Natural Language client library](https://cloud.google.com/ruby/docs/reference/google-cloud-language/latest).

```
require "googleauth"
require "google/cloud/language/v1"

def authenticate_with_api_key api_key_string
  # Authenticates with an API key for Google Language service.
  #
  # TODO(Developer): Uncomment the following line and set the value before running this sample.
  #
  # api_key_string = "mykey12345"
  #
  # Note: You can also set the API key via environment variable:
  #   export GOOGLE_API_KEY=your-api-key
  # and use Google::Auth::APIKeyCredentials.from_env method to load it.
  # Example:
  #   credentials = Google::Auth::APIKeyCredentials.from_env
  #   if credentials.nil?
  #     puts "No API key found in environment"
  #     exit
  #   end

  # Initialize API key credentials using the class factory method
  credentials = Google::Auth::APIKeyCredentials.make_creds api_key: api_key_string

  # Initialize the Language Service client with the API key credentials
  client = Google::Cloud::Language::V1::LanguageService::Client.new do |config|
    config.credentials = credentials
  end

  # Create a document to analyze
  text = "Hello, world!"
  document = {
    content: text,
    type: :PLAIN_TEXT
  }

  # Make a request to analyze the sentiment of the text
  sentiment = client.analyze_sentiment(document: document).document_sentiment

  puts "Text: #{text}"
  puts "Sentiment: #{sentiment.score}, #{sentiment.magnitude}"
  puts "Successfully authenticated using the API key"
end
```

When you use API keys in your applications, ensure that they are kept secure
during both storage and transmission. Publicly exposing your API keys can
lead to unexpected charges on your account. For more information, see
[Best practices for managing API keys](https://cloud.google.com/docs/authentication/api-keys-best-practices).

## Security requirements when using credential configurations from an external source

Typically, you generate credential configurations by using gcloud CLI
commands or by using the Google Cloud console. For example, you can use the
gcloud CLI to generate a local ADC file or a login configuration
file. Similarly, you can use the Google Cloud console to create and download
a service account key.

For some use cases, however, credential configurations are provided to you by an
external entity; these credential configurations are intended to be used to
authenticate to Google APIs.

Some types of credential configurations include endpoints and file paths, which
the authentication libraries use to acquire a token. When you accept credential
configurations from an external source, you must validate the configuration
before using it. If you don't validate the configuration, a malicious actor
could use the credential to compromise your systems and data.

### Validate credential configurations from external sources

How you need to validate your external credentials depends on what types of
credential your application accepts.

#### Validate service account keys

If your application accepts *only* service account keys, use a credential
loader specific to service account keys, as shown in the following examples. The
type-specific credential loader parses only the fields present for service
account keys, which don't expose any vulnerabilities.

```
var saCredential = CredentialFactory.FromStream<ServiceAccountCredential>(stream);
```

```
auto cred = google::cloud::MakeServiceAccountCredentials(json)
```

```
ServiceAccountCredentials credentials =
      ServiceAccountCredentials.fromStream(credentialsStream);
```

```
const keys = JSON.parse(json_input)
const authClient = JWT.fromJSON(keys);
```

```
$cred = new Google\Auth\Credentials\ServiceAccountCredentials($scope, $jsonKey);
```

```
cred = service_account.Credentials.from_service_account_info(json_data)
```

```
creds = Google::Auth::ServiceAccountCredentials.make_creds(json_key_io: json_stream)
```

If you can't use a type-specific credential loader, validate the credential by
confirming that the value for the `type` field is `service_account`. If the
value for the `type` field is any other value, don't use the service account
key.

#### Validate other credential configurations

If your application accepts *any* type of credential besides a service account
key, you must perform additional verification. Examples of other types of
credential configurations include
[ADC credential files](https://cloud.google.com/docs/authentication/application-default-credentials#personal),
[Workload Identity Federation credential files](https://cloud.google.com/iam/docs/workload-identity-federation-with-other-clouds#create-cred-config),
or [Workforce Identity Federation login configuration files](https://cloud.google.com/iam/docs/workforce-obtaining-short-lived-credentials#create-login-config).

The following table lists the fields you need to validate, if they are present
in your credentials. Not all of these fields are present for all credential
configurations.

| Field | Purpose | Expected value |
| --- | --- | --- |
| service_account_impersonation_url | The authentication libraries use this field to access an endpoint to
      generate an access token for the service account being impersonated. | https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/service account email:generateAccessToken |
| token_url | The authentication libraries send an external token to this endpoint to
      exchange it for afederated access token. | https://sts.googleapis.com/v1/token |
| credential_source.file | The authentication libraries read an external token from the file at the
      location specified by this field and send it to thetoken_urlendpoint. | The path for a file containing an external token. You should
      recognize this path. |
| credential_source.url | An endpoint that returns an external token. The authentication libraries
      send a request to this URL and send the response to thetoken_urlendpoint. | One of the following items:A well-known endpoint provided by your cloud provider.An endpoint that you have explicitly set up to provide tokens. |
| credential_source.executable.command | If theGOOGLE_EXTERNAL_ACCOUNT_ALLOW_EXECUTABLESenvironment variable is set to1, the authentication
      libraries run this command or executable file. | An executable file or command that returns an external token.
      You should recognize this command and validate that it is safe. |
| credential_source.aws.url | The authentication libraries issue a request to this URL to retrieve
      an AWS security token. | Either one of these exact values:http://169.254.169.254/latest/meta-data/iam/security-credentialshttp://[fd00:ec2::254]/latest/meta-data/iam/security-credentials |
| credential_source.aws.region_url | The authentication libraries issue a request to this URL to retrieve
      the active AWS region. | Either one of these exact values:http://169.254.169.254/latest/meta-data/placement/availability-zonehttp://[fd00:ec2::254]/latest/meta-data/placement/availability-zone |
| credential_source.aws.imdsv2_session_token_url | The authentication libraries issue a request to this URL to retrieve
      the AWS session token. | Either one of these exact values:http://169.254.169.254/latest/api/tokenhttp://[fd00:ec2::254]/latest/api/token |

## What's next

- Learn more about [Application Default Credentials](https://cloud.google.com/docs/authentication/application-default-credentials).
- Learn more about [API keys](https://cloud.google.com/docs/authentication/api-keys).
- See an overview of [Authentication methods](https://cloud.google.com/docs/authentication).

   Was this helpful?

---

# Authenticate for using client librariesStay organized with collectionsSave and categorize content based on your preferences.

# Authenticate for using client librariesStay organized with collectionsSave and categorize content based on your preferences.

This page describes how you can use client libraries to access Google APIs.

Client libraries make it easier to access [Google Cloud APIs](https://cloud.google.com/apis/docs/overview)
using a supported language. You can use Google Cloud APIs directly by
making raw requests to the server, but client libraries provide simplifications
that significantly reduce the amount of code you need to write. This is
especially true for authentication, because the client libraries support
[Application Default Credentials (ADC)](https://cloud.google.com/docs/authentication/application-default-credentials).

If you accept credential configurations (JSON, files, or streams) from an
external source (for example, a customer), review the
[security requirements when using credential configurations from an external source](#external-credentials).

## Use Application Default Credentials with client libraries

To use Application Default Credentials to authenticate your application, you
 must first [set up ADC](https://cloud.google.com/docs/authentication/provide-credentials-adc) for the
 environment where your application is running. When you use the client
 library to create a client, the client library automatically checks for and
 uses the credentials you have provided to ADC to authenticate to the APIs
 your code uses. Your application does not need to explicitly authenticate
 or manage tokens; these requirements are managed automatically by the
 authentication libraries.

For a local development environment, you can set up ADC
[with your user credentials](https://cloud.google.com/docs/authentication/set-up-adc-local-dev-environment) or
[with service account impersonation](https://cloud.google.com/docs/authentication/use-service-account-impersonation#adc)
by using the gcloud CLI. For production environments,
you set up ADC by [attaching a service account](https://cloud.google.com/docs/authentication/set-up-adc-attached-service-account).

### Example client creation

The following code samples create a client for the Cloud Storage service.
Your code is likely to need different clients; these samples are meant only to
show how you can create a client and use it without any code to explicitly
authenticate.

Before you can run the following samples, you must complete the following steps:

- [Set up ADC for your environment](https://cloud.google.com/docs/authentication/provide-credentials-adc)
- [Install the Cloud Storage client library](https://cloud.google.com/storage/docs/reference/libraries)

```
import (
	"context"
	"fmt"
	"io"

	"cloud.google.com/go/storage"
	"google.golang.org/api/iterator"
)

// authenticateImplicitWithAdc uses Application Default Credentials
// to automatically find credentials and authenticate.
func authenticateImplicitWithAdc(w io.Writer, projectId string) error {
	// projectId := "your_project_id"

	ctx := context.Background()

	// NOTE: Replace the client created below with the client required for your application.
	// Note that the credentials are not specified when constructing the client.
	// The client library finds your credentials using ADC.
	client, err := storage.NewClient(ctx)
	if err != nil {
		return fmt.Errorf("NewClient: %w", err)
	}
	defer client.Close()

	it := client.Buckets(ctx, projectId)
	for {
		bucketAttrs, err := it.Next()
		if err == iterator.Done {
			break
		}
		if err != nil {
			return err
		}
		fmt.Fprintf(w, "Bucket: %v\n", bucketAttrs.Name)
	}

	fmt.Fprintf(w, "Listed all storage buckets.\n")

	return nil
}
```

```
import com.google.api.gax.paging.Page;
import com.google.cloud.storage.Bucket;
import com.google.cloud.storage.Storage;
import com.google.cloud.storage.StorageOptions;
import java.io.IOException;

public class AuthenticateImplicitWithAdc {

  public static void main(String[] args) throws IOException {
    // TODO(Developer):
    //  1. Before running this sample,
    //  set up Application Default Credentials as described in
    //  https://cloud.google.com/docs/authentication/external/set-up-adc
    //  2. Replace the project variable below.
    //  3. Make sure you have the necessary permission to list storage buckets
    //  "storage.buckets.list"
    String projectId = "your-google-cloud-project-id";
    authenticateImplicitWithAdc(projectId);
  }

  // When interacting with Google Cloud Client libraries, the library can auto-detect the
  // credentials to use.
  public static void authenticateImplicitWithAdc(String project) throws IOException {

    // *NOTE*: Replace the client created below with the client required for your application.
    // Note that the credentials are not specified when constructing the client.
    // Hence, the client library will look for credentials using ADC.
    //
    // Initialize client that will be used to send requests. This client only needs to be created
    // once, and can be reused for multiple requests.
    Storage storage = StorageOptions.newBuilder().setProjectId(project).build().getService();

    System.out.println("Buckets:");
    Page<Bucket> buckets = storage.list();
    for (Bucket bucket : buckets.iterateAll()) {
      System.out.println(bucket.toString());
    }
    System.out.println("Listed all storage buckets.");
  }
}
```

```
/**
 * TODO(developer):
 *  1. Uncomment and replace these variables before running the sample.
 *  2. Set up ADC as described in https://cloud.google.com/docs/authentication/external/set-up-adc
 *  3. Make sure you have the necessary permission to list storage buckets "storage.buckets.list"
 *    (https://cloud.google.com/storage/docs/access-control/iam-permissions#bucket_permissions)
 */
// const projectId = 'YOUR_PROJECT_ID';

const {Storage} = require('@google-cloud/storage');

async function authenticateImplicitWithAdc() {
  // This snippet demonstrates how to list buckets.
  // NOTE: Replace the client created below with the client required for your application.
  // Note that the credentials are not specified when constructing the client.
  // The client library finds your credentials using ADC.
  const storage = new Storage({
    projectId,
  });
  const [buckets] = await storage.getBuckets();
  console.log('Buckets:');

  for (const bucket of buckets) {
    console.log(`- ${bucket.name}`);
  }

  console.log('Listed all storage buckets.');
}

authenticateImplicitWithAdc();
```

```
// Imports the Cloud Storage client library.
use Google\Cloud\Storage\StorageClient;

/**
 * Authenticate to a cloud client library using a service account implicitly.
 *
 * @param string $projectId The Google project ID.
 */
function auth_cloud_implicit($projectId)
{
    $config = [
        'projectId' => $projectId,
    ];

    # If you don't specify credentials when constructing the client, the
    # client library will look for credentials in the environment.
    $storage = new StorageClient($config);

    # Make an authenticated API request (listing storage buckets)
    foreach ($storage->buckets() as $bucket) {
        printf('Bucket: %s' . PHP_EOL, $bucket->name());
    }
}
```

```
from google.cloud import storage

def authenticate_implicit_with_adc(project_id="your-google-cloud-project-id"):
    """
    When interacting with Google Cloud Client libraries, the library can auto-detect the
    credentials to use.

    // TODO(Developer):
    //  1. Before running this sample,
    //  set up ADC as described in https://cloud.google.com/docs/authentication/external/set-up-adc
    //  2. Replace the project variable.
    //  3. Make sure that the user account or service account that you are using
    //  has the required permissions. For this sample, you must have "storage.buckets.list".
    Args:
        project_id: The project id of your Google Cloud project.
    """

    # This snippet demonstrates how to list buckets.
    # *NOTE*: Replace the client created below with the client required for your application.
    # Note that the credentials are not specified when constructing the client.
    # Hence, the client library will look for credentials using ADC.
    storage_client = storage.Client(project=project_id)
    buckets = storage_client.list_buckets()
    print("Buckets:")
    for bucket in buckets:
        print(bucket.name)
    print("Listed all storage buckets.")
```

```
def authenticate_implicit_with_adc project_id:
  # The ID of your Google Cloud project
  # project_id = "your-google-cloud-project-id"

  ###
  # When interacting with Google Cloud Client libraries, the library can auto-detect the
  # credentials to use.
  # TODO(Developer):
  #   1. Before running this sample,
  #      set up ADC as described in https://cloud.google.com/docs/authentication/external/set-up-adc
  #   2. Replace the project variable.
  #   3. Make sure that the user account or service account that you are using
  #      has the required permissions. For this sample, you must have "storage.buckets.list".
  ###

  require "google/cloud/storage"

  # This sample demonstrates how to list buckets.
  # *NOTE*: Replace the client created below with the client required for your application.
  # Note that the credentials are not specified when constructing the client.
  # Hence, the client library will look for credentials using ADC.
  storage = Google::Cloud::Storage.new project_id: project_id
  buckets = storage.buckets
  puts "Buckets: "
  buckets.each do |bucket|
    puts bucket.name
  end
  puts "Plaintext: Listed all storage buckets."
end
```

## Use API keys with client libraries

You can use an API keys only with client libraries for APIs that accept API
keys. In addition, the API key must not have an API restriction that prevents it
from being used for the API.

For more information about API keys created in express mode, see the
[Google Cloud express mode FAQ](https://cloud.google.com/resources/cloud-express-faqs).

This example uses the Cloud Natural Language API, which accepts API keys,
  to demonstrate how you would provide an API key to the library.

To run this sample, you must install the
[Natural Language client library](https://cloud.google.com/dotnet/docs/reference/Google.Cloud.Language.V2/latest).

```
using Google.Cloud.Language.V1;
using System;

public class UseApiKeySample
{
    public void AnalyzeSentiment(string apiKey)
    {
        LanguageServiceClient client = new LanguageServiceClientBuilder
        {
            ApiKey = apiKey
        }.Build();

        string text = "Hello, world!";

        AnalyzeSentimentResponse response = client.AnalyzeSentiment(Document.FromPlainText(text));
        Console.WriteLine($"Text: {text}");
        Sentiment sentiment = response.DocumentSentiment;
        Console.WriteLine($"Sentiment: {sentiment.Score}, {sentiment.Magnitude}");
        Console.WriteLine("Successfully authenticated using the API key");
    }
}
```

To run this sample, you must install the
[Natural Language client library](https://cloud.google.com/cpp/docs/reference/language/latest).

```
#include "google/cloud/language/v1/language_client.h"
#include "google/cloud/credentials.h"
#include "google/cloud/options.h"

void AuthenticateWithApiKey(std::vector<std::string> const& argv) {
  if (argv.size() != 2) {
    throw google::cloud::testing_util::Usage{
        "authenticate-with-api-key <project-id> <api-key>"};
  }
  namespace gc = ::google::cloud;
  auto options = gc::Options{}.set<gc::UnifiedCredentialsOption>(
      gc::MakeApiKeyCredentials(argv[1]));
  auto client = gc::language_v1::LanguageServiceClient(
      gc::language_v1::MakeLanguageServiceConnection(options));

  auto constexpr kText = "Hello, world!";

  google::cloud::language::v1::Document d;
  d.set_content(kText);
  d.set_type(google::cloud::language::v1::Document::PLAIN_TEXT);

  auto response = client.AnalyzeSentiment(d, {});
  if (!response) throw std::move(response.status());
  auto const& sentiment = response->document_sentiment();
  std::cout << "Text: " << kText << "\n";
  std::cout << "Sentiment: " << sentiment.score() << ", "
            << sentiment.magnitude() << "\n";
  std::cout << "Successfully authenticated using the API key\n";
}
```

To run this sample, you must install the
[Natural Language client library](https://cloud.google.com/go/docs/reference/cloud.google.com/go/language/latest).

```
import (
	"context"
	"fmt"
	"io"

	language "cloud.google.com/go/language/apiv1"
	"cloud.google.com/go/language/apiv1/languagepb"
	"google.golang.org/api/option"
)

// authenticateWithAPIKey authenticates with an API key for Google Language
// service.
func authenticateWithAPIKey(w io.Writer, apiKey string) error {
	// apiKey := "api-key-string"

	ctx := context.Background()

	// Initialize the Language Service client and set the API key.
	client, err := language.NewClient(ctx, option.WithAPIKey(apiKey))
	if err != nil {
		return fmt.Errorf("NewClient: %w", err)
	}
	defer client.Close()

	text := "Hello, world!"
	// Make a request to analyze the sentiment of the text.
	res, err := client.AnalyzeSentiment(ctx, &languagepb.AnalyzeSentimentRequest{
		Document: &languagepb.Document{
			Source: &languagepb.Document_Content{
				Content: text,
			},
			Type: languagepb.Document_PLAIN_TEXT,
		},
	})
	if err != nil {
		return fmt.Errorf("AnalyzeSentiment: %w", err)
	}

	fmt.Fprintf(w, "Text: %s\n", text)
	fmt.Fprintf(w, "Sentiment score: %v\n", res.DocumentSentiment.Score)
	fmt.Fprintln(w, "Successfully authenticated using the API key.")

	return nil
}
```

To run this sample, you must install the
[Natural Language client library](https://cloud.google.com/nodejs/docs/reference/language/latest).

```
const {
  v1: {LanguageServiceClient},
} = require('@google-cloud/language');

/**
 * Authenticates with an API key for Google Language service.
 *
 * @param {string} apiKey An API Key to use
 */
async function authenticateWithAPIKey(apiKey) {
  const language = new LanguageServiceClient({apiKey});

  // Alternatively:
  // const {GoogleAuth} = require('google-auth-library');
  // const auth = new GoogleAuth({apiKey});
  // const language = new LanguageServiceClient({auth});

  const text = 'Hello, world!';

  const [response] = await language.analyzeSentiment({
    document: {
      content: text,
      type: 'PLAIN_TEXT',
    },
  });

  console.log(`Text: ${text}`);
  console.log(
    `Sentiment: ${response.documentSentiment.score}, ${response.documentSentiment.magnitude}`,
  );
  console.log('Successfully authenticated using the API key');
}

authenticateWithAPIKey();
```

To run this sample, you must install the
[Natural Language client library](https://cloud.google.com/python/docs/reference/language/latest).

```
from google.cloud import language_v1

def authenticate_with_api_key(api_key_string: str) -> None:
    """
    Authenticates with an API key for Google Language service.

    TODO(Developer): Replace this variable before running the sample.

    Args:
        api_key_string: The API key to authenticate to the service.
    """

    # Initialize the Language Service client and set the API key
    client = language_v1.LanguageServiceClient(
        client_options={"api_key": api_key_string}
    )

    text = "Hello, world!"
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Make a request to analyze the sentiment of the text.
    sentiment = client.analyze_sentiment(
        request={"document": document}
    ).document_sentiment

    print(f"Text: {text}")
    print(f"Sentiment: {sentiment.score}, {sentiment.magnitude}")
    print("Successfully authenticated using the API key")
```

To run this sample, you must install the
[Natural Language client library](https://cloud.google.com/ruby/docs/reference/google-cloud-language/latest).

```
require "googleauth"
require "google/cloud/language/v1"

def authenticate_with_api_key api_key_string
  # Authenticates with an API key for Google Language service.
  #
  # TODO(Developer): Uncomment the following line and set the value before running this sample.
  #
  # api_key_string = "mykey12345"
  #
  # Note: You can also set the API key via environment variable:
  #   export GOOGLE_API_KEY=your-api-key
  # and use Google::Auth::APIKeyCredentials.from_env method to load it.
  # Example:
  #   credentials = Google::Auth::APIKeyCredentials.from_env
  #   if credentials.nil?
  #     puts "No API key found in environment"
  #     exit
  #   end

  # Initialize API key credentials using the class factory method
  credentials = Google::Auth::APIKeyCredentials.make_creds api_key: api_key_string

  # Initialize the Language Service client with the API key credentials
  client = Google::Cloud::Language::V1::LanguageService::Client.new do |config|
    config.credentials = credentials
  end

  # Create a document to analyze
  text = "Hello, world!"
  document = {
    content: text,
    type: :PLAIN_TEXT
  }

  # Make a request to analyze the sentiment of the text
  sentiment = client.analyze_sentiment(document: document).document_sentiment

  puts "Text: #{text}"
  puts "Sentiment: #{sentiment.score}, #{sentiment.magnitude}"
  puts "Successfully authenticated using the API key"
end
```

When you use API keys in your applications, ensure that they are kept secure
during both storage and transmission. Publicly exposing your API keys can
lead to unexpected charges on your account. For more information, see
[Best practices for managing API keys](https://cloud.google.com/docs/authentication/api-keys-best-practices).

## Security requirements when using credential configurations from an external source

Typically, you generate credential configurations by using gcloud CLI
commands or by using the Google Cloud console. For example, you can use the
gcloud CLI to generate a local ADC file or a login configuration
file. Similarly, you can use the Google Cloud console to create and download
a service account key.

For some use cases, however, credential configurations are provided to you by an
external entity; these credential configurations are intended to be used to
authenticate to Google APIs.

Some types of credential configurations include endpoints and file paths, which
the authentication libraries use to acquire a token. When you accept credential
configurations from an external source, you must validate the configuration
before using it. If you don't validate the configuration, a malicious actor
could use the credential to compromise your systems and data.

### Validate credential configurations from external sources

How you need to validate your external credentials depends on what types of
credential your application accepts.

#### Validate service account keys

If your application accepts *only* service account keys, use a credential
loader specific to service account keys, as shown in the following examples. The
type-specific credential loader parses only the fields present for service
account keys, which don't expose any vulnerabilities.

```
var saCredential = CredentialFactory.FromStream<ServiceAccountCredential>(stream);
```

```
auto cred = google::cloud::MakeServiceAccountCredentials(json)
```

```
ServiceAccountCredentials credentials =
      ServiceAccountCredentials.fromStream(credentialsStream);
```

```
const keys = JSON.parse(json_input)
const authClient = JWT.fromJSON(keys);
```

```
$cred = new Google\Auth\Credentials\ServiceAccountCredentials($scope, $jsonKey);
```

```
cred = service_account.Credentials.from_service_account_info(json_data)
```

```
creds = Google::Auth::ServiceAccountCredentials.make_creds(json_key_io: json_stream)
```

If you can't use a type-specific credential loader, validate the credential by
confirming that the value for the `type` field is `service_account`. If the
value for the `type` field is any other value, don't use the service account
key.

#### Validate other credential configurations

If your application accepts *any* type of credential besides a service account
key, you must perform additional verification. Examples of other types of
credential configurations include
[ADC credential files](https://cloud.google.com/docs/authentication/application-default-credentials#personal),
[Workload Identity Federation credential files](https://cloud.google.com/iam/docs/workload-identity-federation-with-other-clouds#create-cred-config),
or [Workforce Identity Federation login configuration files](https://cloud.google.com/iam/docs/workforce-obtaining-short-lived-credentials#create-login-config).

The following table lists the fields you need to validate, if they are present
in your credentials. Not all of these fields are present for all credential
configurations.

| Field | Purpose | Expected value |
| --- | --- | --- |
| service_account_impersonation_url | The authentication libraries use this field to access an endpoint to
      generate an access token for the service account being impersonated. | https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/service account email:generateAccessToken |
| token_url | The authentication libraries send an external token to this endpoint to
      exchange it for afederated access token. | https://sts.googleapis.com/v1/token |
| credential_source.file | The authentication libraries read an external token from the file at the
      location specified by this field and send it to thetoken_urlendpoint. | The path for a file containing an external token. You should
      recognize this path. |
| credential_source.url | An endpoint that returns an external token. The authentication libraries
      send a request to this URL and send the response to thetoken_urlendpoint. | One of the following items:A well-known endpoint provided by your cloud provider.An endpoint that you have explicitly set up to provide tokens. |
| credential_source.executable.command | If theGOOGLE_EXTERNAL_ACCOUNT_ALLOW_EXECUTABLESenvironment variable is set to1, the authentication
      libraries run this command or executable file. | An executable file or command that returns an external token.
      You should recognize this command and validate that it is safe. |
| credential_source.aws.url | The authentication libraries issue a request to this URL to retrieve
      an AWS security token. | Either one of these exact values:http://169.254.169.254/latest/meta-data/iam/security-credentialshttp://[fd00:ec2::254]/latest/meta-data/iam/security-credentials |
| credential_source.aws.region_url | The authentication libraries issue a request to this URL to retrieve
      the active AWS region. | Either one of these exact values:http://169.254.169.254/latest/meta-data/placement/availability-zonehttp://[fd00:ec2::254]/latest/meta-data/placement/availability-zone |
| credential_source.aws.imdsv2_session_token_url | The authentication libraries issue a request to this URL to retrieve
      the AWS session token. | Either one of these exact values:http://169.254.169.254/latest/api/tokenhttp://[fd00:ec2::254]/latest/api/token |

## What's next

- Learn more about [Application Default Credentials](https://cloud.google.com/docs/authentication/application-default-credentials).
- Learn more about [API keys](https://cloud.google.com/docs/authentication/api-keys).
- See an overview of [Authentication methods](https://cloud.google.com/docs/authentication).
