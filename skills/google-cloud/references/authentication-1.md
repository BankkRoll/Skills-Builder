# Best practices for managing API keysStay organized with collectionsSave and categorize content based on your preferences. and more

# Best practices for managing API keysStay organized with collectionsSave and categorize content based on your preferences.

# Best practices for managing API keysStay organized with collectionsSave and categorize content based on your preferences.

When you use API keys in your applications, ensure that they are kept secure
during both storage and transmission. Publicly exposing your API keys can lead
to unexpected charges on your account or unauthorized access to your data. To
help keep your API keys secure, implement the following best practices.

## Add API key restrictions to your key

By adding restrictions, you can limit the ways an API key can be used, reducing
the impact of a compromised API key.

For more information, see
[Apply API key restrictions](https://cloud.google.com/docs/authentication/api-keys#api_key_restrictions).

## Avoid using query parameters to provide your API key to Google APIs

Providing your API key to APIs as a query parameter includes your API key in the
URL, exposing your key to theft through URL scans. Use the
[x-goog-api-keyHTTP header](https://cloud.google.com/docs/authentication/api-keys-use#using-with-rest)
or a [client library](https://cloud.google.com/docs/authentication/api-keys-use#using-with-client-libs)
instead.

## Delete unneeded API keys to minimize exposure to attacks

Retain only the API keys you are actively using to keep your attack surface as
small as possible.

## Don't include API keys in client code or commit them to code repositories

API keys hardcoded in the source code or stored in a repository are open to
interception or theft by bad actors. The client should pass requests to the
server, which can add the credential and issue the request.

## Don't use API keys bound to service accounts in production

API keys bound to service accounts are designed to accelerate the initial
experience for developers exploring Google Cloud APIs. Don't use them in
production environments. Instead,
[plan to migrate to more secure alternatives](#consider-alternatives) such as
[Identity and Access Management (IAM)](https://cloud.google.com/iam/docs/grant-role-console) policies and
[short-lived service account credentials](https://cloud.google.com/iam/docs/service-account-creds#short-lived-credentials),
following least-privilege security practices.

Here's why you should migrate from using an API key bound to a service account
to more secure practices as soon as possible:

- API keys are sent alongside requests. This makes it more likely that the key
  might be exposed or logged.
- API keys are bearer credentials. This means that if someone steals an API key
  that's bound to a service account, they can use it to authenticate as that
  service account and access the same resources that service account can.
- API keys bound to service accounts obscure the identity of the end user in
  audit logs. To track the actions of individual users, make sure each user has
  their own set of credentials.

## Implement strong monitoring and logging

Monitoring API usage can help alert you to unauthorized usage. For more
information, see
[Cloud Monitoring overview](https://cloud.google.com/monitoring/docs/monitoring-overview) and
[Cloud Logging overview](https://cloud.google.com/logging/docs/overview).

## Isolate API keys

Provide each team member with their own API key for each application. This can
help control access, provide an audit trail, and reduce the impact of a
compromised API key.

## Rotate your API keys periodically

Periodically create new API keys, update your applications to use the new API
keys, and delete the old keys.

For more information, see
[Rotate an API key](https://cloud.google.com/docs/authentication/api-keys#rotate).

## Consider a more secure method of authorizing access

For help with choosing an authentication method, see
[Authentication methods](https://cloud.google.com/docs/authentication).

---

# Use API keys to access APIsStay organized with collectionsSave and categorize content based on your preferences.

# Use API keys to access APIsStay organized with collectionsSave and categorize content based on your preferences.

This page describes how to use API keys to access Google Cloud APIs
and services that accept API keys.

Not all Google Cloud APIs accept API keys to authorize usage. Review
the documentation for the service or API that you want to use to
determine whether it accepts API keys.

For information about creating and managing API keys, including restricting
API keys, see [Manage API keys](https://cloud.google.com/docs/authentication/api-keys).

For information about using API keys with Google Maps Platform, see the
[Google Maps Platform documentation](https://developers.google.com/maps/api-key-best-practices).
For more information about the API Keys API, see the
[API Keys API documentation](https://cloud.google.com/api-keys/docs/overview).

## Before you begin

Select the tab for how you plan to use the samples on this page:

To use the .NET samples on this page in a local
      development environment, install and initialize the gcloud CLI, and
      then set up Application Default Credentials with your user credentials.

1. [Install](https://cloud.google.com/sdk/docs/install) the Google Cloud CLI.
2. If you're using an external identity provider (IdP), you must first
              [sign in to the gcloud CLI with your federated identity](https://cloud.google.com/iam/docs/workforce-log-in-gcloud).
3. If you're using a local shell, then create local authentication credentials for your user
          account:
  ```
  gcloud auth application-default login
  ```
  You don't need to do this if you're using Cloud Shell.
  If an authentication error is returned, and you are using an external identity provider
          (IdP), confirm that you have
          [signed in to the gcloud CLI with your federated identity](https://cloud.google.com/iam/docs/workforce-log-in-gcloud).

For more information, see
    [Set up ADC for a local development environment](https://cloud.google.com/docs/authentication/set-up-adc-local-dev-environment)
    in the Google Cloud authentication documentation.

To use the C++ samples on this page in a local
      development environment, install and initialize the gcloud CLI, and
      then set up Application Default Credentials with your user credentials.

1. [Install](https://cloud.google.com/sdk/docs/install) the Google Cloud CLI.
2. If you're using an external identity provider (IdP), you must first
              [sign in to the gcloud CLI with your federated identity](https://cloud.google.com/iam/docs/workforce-log-in-gcloud).
3. If you're using a local shell, then create local authentication credentials for your user
          account:
  ```
  gcloud auth application-default login
  ```
  You don't need to do this if you're using Cloud Shell.
  If an authentication error is returned, and you are using an external identity provider
          (IdP), confirm that you have
          [signed in to the gcloud CLI with your federated identity](https://cloud.google.com/iam/docs/workforce-log-in-gcloud).

For more information, see
    [Set up ADC for a local development environment](https://cloud.google.com/docs/authentication/set-up-adc-local-dev-environment)
    in the Google Cloud authentication documentation.

To use the Go samples on this page in a local
      development environment, install and initialize the gcloud CLI, and
      then set up Application Default Credentials with your user credentials.

1. [Install](https://cloud.google.com/sdk/docs/install) the Google Cloud CLI.
2. If you're using an external identity provider (IdP), you must first
              [sign in to the gcloud CLI with your federated identity](https://cloud.google.com/iam/docs/workforce-log-in-gcloud).
3. If you're using a local shell, then create local authentication credentials for your user
          account:
  ```
  gcloud auth application-default login
  ```
  You don't need to do this if you're using Cloud Shell.
  If an authentication error is returned, and you are using an external identity provider
          (IdP), confirm that you have
          [signed in to the gcloud CLI with your federated identity](https://cloud.google.com/iam/docs/workforce-log-in-gcloud).

For more information, see
    [Set up ADC for a local development environment](https://cloud.google.com/docs/authentication/set-up-adc-local-dev-environment)
    in the Google Cloud authentication documentation.

To use the Node.js samples on this page in a local
      development environment, install and initialize the gcloud CLI, and
      then set up Application Default Credentials with your user credentials.

1. [Install](https://cloud.google.com/sdk/docs/install) the Google Cloud CLI.
2. If you're using an external identity provider (IdP), you must first
              [sign in to the gcloud CLI with your federated identity](https://cloud.google.com/iam/docs/workforce-log-in-gcloud).
3. If you're using a local shell, then create local authentication credentials for your user
          account:
  ```
  gcloud auth application-default login
  ```
  You don't need to do this if you're using Cloud Shell.
  If an authentication error is returned, and you are using an external identity provider
          (IdP), confirm that you have
          [signed in to the gcloud CLI with your federated identity](https://cloud.google.com/iam/docs/workforce-log-in-gcloud).

For more information, see
    [Set up ADC for a local development environment](https://cloud.google.com/docs/authentication/set-up-adc-local-dev-environment)
    in the Google Cloud authentication documentation.

To use the Python samples on this page in a local
      development environment, install and initialize the gcloud CLI, and
      then set up Application Default Credentials with your user credentials.

1. [Install](https://cloud.google.com/sdk/docs/install) the Google Cloud CLI.
2. If you're using an external identity provider (IdP), you must first
              [sign in to the gcloud CLI with your federated identity](https://cloud.google.com/iam/docs/workforce-log-in-gcloud).
3. If you're using a local shell, then create local authentication credentials for your user
          account:
  ```
  gcloud auth application-default login
  ```
  You don't need to do this if you're using Cloud Shell.
  If an authentication error is returned, and you are using an external identity provider
          (IdP), confirm that you have
          [signed in to the gcloud CLI with your federated identity](https://cloud.google.com/iam/docs/workforce-log-in-gcloud).

For more information, see
    [Set up ADC for a local development environment](https://cloud.google.com/docs/authentication/set-up-adc-local-dev-environment)
    in the Google Cloud authentication documentation.

To use the REST API samples on this page in a local development environment, you use the
    credentials you provide to the gcloud CLI.

For more information, see
  [Authenticate for using REST](https://cloud.google.com/docs/authentication/rest)
  in the Google Cloud authentication documentation.

## Using an API key with REST

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

## Using an API key with client libraries

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

## What's next

- See an overview of [authentication methods](https://cloud.google.com/docs/authentication).
- Learn more about the [API Keys API](https://cloud.google.com/api-keys/docs/overview).

   Was this helpful?
