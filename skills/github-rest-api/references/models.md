# REST API endpoints for models catalog and more

# REST API endpoints for models catalog

> Use the REST API to get a list of models available for use, including details like ID, supported input/output modalities, and rate limits.

## About GitHub Models catalog

You can use the REST API to explore available models in the GitHub Models catalog.

---

# REST API endpoints for model embeddings

> Use the REST API to work with embedding requests for models.

## Run an embedding request attributed to an organization

This endpoint allows you to run an embedding request attributed to a specific organization. You must be a member of the organization and have enabled models to use this endpoint.
The token used to authenticate must have the `models: read` permission if using a fine-grained PAT or GitHub App minted token.
The request body should contain the model ID and the input text(s) for the embedding request. The response will include the generated embeddings.

### Parameters for "Run an embedding request attributed to an organization"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| orgstringRequiredThe organization login associated with the organization to which the request is to be attributed. |

| Name, Type, Description |
| --- |
| api-versionstringThe API version to use. Optional, but required for some features. |

| Name, Type, Description |
| --- |
| modelstringRequiredID of the specific model to use for the request. The model ID should be in the format of {publisher}/{model_name} where "openai/text-embedding-3-small" is an example of a model ID. You can find supported models in the catalog/models endpoint. |
| inputstring or arrayRequiredInput text to embed, encoded as a string or array of strings. To embed multiple inputs in a single request, pass an array of strings. Each input must not exceed the max input tokens for the model, cannot be an empty string, and any array must be 2048 dimensions or less. |
| encoding_formatstringThe format to return the embeddings in. Can be either float or base64.Default:floatCan be one of:float,base64 |
| dimensionsintegerThe number of dimensions the resulting output embeddings should have. Only supported in text-embedding-3 and later models. |
| userstringA unique identifier representing your end-user, which can help us to monitor and detect abuse. |

### HTTP response status codes for "Run an embedding request attributed to an organization"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "Run an embedding request attributed to an organization"

#### Request example

post/orgs/{org}/inference/embeddings

-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://models.github.ai/orgs/ORG/inference/embeddings \
  -d '{"model":"openai/text-embedding-3-small","input":["The food was delicious and the waiter was very friendly.","I had a great time at the restaurant."]}'`

#### Response

-
-

`Status: 200``{
"object": "list",
"data": [
{
"object": "embedding",
"index": 0,
"embedding": [
0.0023064255,
-0.009327292,
-0.0028842222
]
}
],
"model": "openai/text-embedding-3-small",
"usage": {
"prompt_tokens": 8,
"total_tokens": 8
}
}`

## Run an embedding request

This endpoint allows you to run an embedding request. The token used to authenticate must have the `models: read` permission if using a fine-grained PAT or GitHub App minted token.
The request body should contain the model ID and the input text(s) for the embedding request. The response will include the generated embeddings.

### Parameters for "Run an embedding request"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| api-versionstringThe API version to use. Optional, but required for some features. |

| Name, Type, Description |
| --- |
| modelstringRequiredID of the specific model to use for the request. The model ID should be in the format of {publisher}/{model_name} where "openai/text-embedding-3-small" is an example of a model ID. You can find supported models in the catalog/models endpoint. |
| inputstring or arrayRequiredInput text to embed, encoded as a string or array of strings. To embed multiple inputs in a single request, pass an array of strings. Each input must not exceed the max input tokens for the model, cannot be an empty string, and any array must be 2048 dimensions or less. |
| encoding_formatstringThe format to return the embeddings in. Can be either float or base64.Default:floatCan be one of:float,base64 |
| dimensionsintegerThe number of dimensions the resulting output embeddings should have. Only supported in text-embedding-3 and later models. |
| userstringA unique identifier representing your end-user, which can help us to monitor and detect abuse. |

### HTTP response status codes for "Run an embedding request"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "Run an embedding request"

#### Request example

post/inference/embeddings

-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://models.github.ai/inference/embeddings \
  -d '{"model":"openai/text-embedding-3-small","input":["The food was delicious and the waiter was very friendly.","I had a great time at the restaurant."]}'`

#### Response

-
-

`Status: 200``{
"object": "list",
"data": [
{
"object": "embedding",
"index": 0,
"embedding": [
0.0023064255,
-0.009327292,
-0.0028842222
]
}
],
"model": "openai/text-embedding-3-small",
"usage": {
"prompt_tokens": 8,
"total_tokens": 8
}
}`

---

# REST API endpoints for models inference

> Use the REST API to submit a chat completion request to a specified model, with or without organizational attribution.

## About GitHub Models inference

You can use the REST API to run inference requests using the GitHub Models platform. The API requires the `models: read` scope when using a fine-grained personal access token or when authenticating using a GitHub App.

The API supports:

- Accessing top models from OpenAI, DeepSeek, Microsoft, Llama, and more.
- Running chat-based inference requests with full control over sampling and response parameters.
- Streaming or non-streaming completions.
- Organizational attribution and usage tracking.
